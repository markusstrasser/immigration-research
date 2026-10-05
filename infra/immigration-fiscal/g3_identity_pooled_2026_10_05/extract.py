#!/usr/bin/env python3
"""Submit, wait for and download the pooled IPUMS-CPS ASEC extract for the G3 non-identifier test.

Why: carryover_identity_2026_09_27 §4 needs ~540 G3 non-identifiers (Mexico-born grandparent,
adult does not report Mexican origin) to pin the closing share c; ASEC 2022-25 gives 44-55.
Pooling ASEC 1994+ with IPUMS parent pointers (MOMLOC/POPLOC) finds G3 through the co-resident
parent's own MBPL/FBPL. Reuses the transport of acquire/ipums_cps_second_gen.py (key never printed).

Usage, from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/extract.py run
  ... status --number N | download --number N | ddi --number N   (DDI codebook → _cache/asec_pooled.xml)
"""
import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("acq", HERE.parent / "acquire" / "ipums_cps_second_gen.py")
acq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acq)

DESCRIPTION = "immigration-research g3_identity_pooled_2026_10_05: ASEC 1994+, parent pointers, G3 non-identifiers"
VARIABLES = ["CPSIDP", "PERNUM", "MOMLOC", "POPLOC", "MOMLOC2", "POPLOC2", "MOMRULE", "POPRULE",
             "RELATE", "AGE", "SEX", "RACE", "HISPAN", "BPL", "MBPL", "FBPL", "NATIVITY", "STATEFIP",
             "EDUC", "EMPSTAT", "LABFORCE", "INCWAGE", "INCTOT", "UHRSWORKLY", "WKSWORK1", "ASECWT"]
OUT = HERE / "_cache" / "asec_pooled.csv.gz"


def submit(key: str, variables: list[str]) -> int:
    samples = acq.asec_samples(key)
    body = {"description": DESCRIPTION, "dataStructure": {"rectangular": {"on": "P"}}, "dataFormat": "csv",
            "samples": {s: {} for s in samples}, "variables": {v: {} for v in variables}}
    r = acq.call("POST", f"/extracts?collection=cps&version=2", key, json=body)
    n = r.json()["number"]
    print(f"  ✓ submitted extract {n}: {len(samples)} samples {samples[0]}…{samples[-1]}, {len(variables)} variables")
    return n


def download(key: str, number: int) -> None:
    # acq.download writes to data_root()/external/cps/cps_2ndgen.csv.gz; redirect to this lane's _cache.
    acq.data_root = lambda: HERE / "_cache" / "_dl"
    out = acq.download(key, number)
    out.replace(OUT)
    man = out.with_name("cps_2ndgen.manifest.json")
    m = json.loads(man.read_text()); m["path"] = str(OUT); m["description"] = DESCRIPTION
    (HERE / "_cache" / "asec_pooled.manifest.json").write_text(json.dumps(m, indent=2))
    man.unlink()
    print(f"  ✓ {OUT}")


def ddi(key: str, number: int) -> None:
    # The DDI codebook carries every variable's code labels; analyze.py reads them from here.
    url = acq.status(key, number)["downloadLinks"]["ddiCodebook"]["url"]
    r = acq.requests.get(url, headers={"Authorization": key}, timeout=(30, 120))
    r.raise_for_status()
    (HERE / "_cache" / "asec_pooled.xml").write_bytes(r.content)
    print(f"  ✓ {HERE / '_cache' / 'asec_pooled.xml'} ({len(r.content)} bytes)")


def main() -> None:
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["run", "submit", "status", "download", "ddi"])
    p.add_argument("--number", type=int)
    a = p.parse_args()
    key = acq.api_key()
    if a.command == "status":
        info = acq.status(key, a.number); print(json.dumps({k: info.get(k) for k in ("number", "status")}))
    elif a.command == "download":
        download(key, a.number)
    elif a.command == "ddi":
        ddi(key, a.number)
    else:
        n = submit(key, VARIABLES)
        if a.command == "run":
            acq.wait(key, n); download(key, n)


if __name__ == "__main__":
    main()

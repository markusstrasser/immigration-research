#!/usr/bin/env python3
"""Submit, wait for and download the IPUMS-CPS basic monthly extract for the G3 non-identifier test.

Why: the ASEC pool (extract.py) reaches 325 unique G3 non-identifiers at 25+, short of the ~540 that
carryover_identity_2026_09_27 §4 sets. Parental birthplace is asked in the basic monthly CPS since
January 1994. The CPS samples addresses on a 4-8-4 rotation, and only households entering in
December-March ever pass through a March sample, so the monthly files hold about twice the ASEC's
unique people. Keeping months-in-sample 1 and 5 (MISH, the two fresh interviews of each household)
counts each household about once per spell and keeps the file small.

Samples: every monthly sample from January 1994 on (IPUMS names them _MMb or _MMs; the March ASEC,
described "ASEC", is excluded). Key never printed; transport from acquire/ipums_cps_second_gen.py.

Usage, from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/extract_monthly.py submit
  ... status --number N | download --number N | ddi --number N | run
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("acq", HERE.parent / "acquire" / "ipums_cps_second_gen.py")
acq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acq)

DESCRIPTION = "immigration-research g3_identity_pooled_2026_10_05: basic monthly 1994+, MIS 1 and 5, parent pointers"
FIRST_YEAR = 1994
VARIABLES = ["CPSID", "CPSIDP", "CPSIDV", "PERNUM", "MOMLOC", "POPLOC", "MOMLOC2", "POPLOC2", "MOMRULE",
             "POPRULE", "RELATE", "AGE", "SEX", "RACE", "HISPAN", "BPL", "MBPL", "FBPL", "NATIVITY",
             "STATEFIP", "EDUC", "EMPSTAT", "LABFORCE", "WTFINL"]
CASE_SELECT = {"MISH": ["1", "5"]}
OUT = HERE / "_cache" / "monthly_mis15.csv.gz"
DDI = HERE / "_cache" / "monthly_mis15.xml"


def monthly_samples(key: str) -> list[str]:
    rows, page = [], 1
    while True:
        data = acq.call("GET", f"/metadata/cps/samples?version=2&pageSize=500&pageNumber={page}", key).json()
        rows += data.get("data", [])
        if not data.get("links", {}).get("nextPage") or not data.get("data"):
            break
        page += 1
    names = sorted(r["name"] for r in rows
                   if int(r["name"][3:7]) >= FIRST_YEAR and "ASEC" not in (r.get("description") or ""))
    months = {n[3:10] for n in names}
    if len(months) != len(names):
        raise SystemExit(f"[FAILED] more than one monthly sample for a month: {len(names)} names, {len(months)} months")
    if len(names) < 380:
        raise SystemExit(f"[FAILED] only {len(names)} monthly samples from {FIRST_YEAR}")
    return names


def submit(key: str) -> int:
    samples = monthly_samples(key)
    variables = {v: {} for v in VARIABLES}
    for v, codes in CASE_SELECT.items():
        variables[v] = {"caseSelections": {"general": codes}}
    body = {"description": DESCRIPTION, "dataStructure": {"rectangular": {"on": "P"}}, "dataFormat": "csv",
            "caseSelectWho": "households", "samples": {s: {} for s in samples}, "variables": variables}
    n = acq.call("POST", "/extracts?collection=cps&version=2", key, json=body).json()["number"]
    print(f"  ✓ submitted extract {n}: {len(samples)} monthly samples {samples[0]}…{samples[-1]}, "
          f"{len(variables)} variables, MISH 1 and 5")
    return n


def download(key: str, number: int) -> None:
    acq.data_root = lambda: HERE / "_cache" / "_dl"
    out = acq.download(key, number)
    out.replace(OUT)
    man = out.with_name("cps_2ndgen.manifest.json")
    m = json.loads(man.read_text())
    m["path"] = str(OUT)
    m["description"] = DESCRIPTION
    (HERE / "_cache" / "monthly_mis15.manifest.json").write_text(json.dumps(m, indent=2))
    man.unlink()
    print(f"  ✓ {OUT}")


def ddi(key: str, number: int) -> None:
    url = acq.status(key, number)["downloadLinks"]["ddiCodebook"]["url"]
    r = requests.get(url, headers={"Authorization": key}, timeout=120)
    r.raise_for_status()
    DDI.write_bytes(r.content)
    print(f"  ✓ {DDI} ({len(r.content)} bytes)")


def main() -> None:
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["run", "submit", "status", "download", "ddi"])
    p.add_argument("--number", type=int)
    a = p.parse_args()
    key = acq.api_key()
    if a.command == "status":
        info = acq.status(key, a.number)
        print(json.dumps({k: info.get(k) for k in ("number", "status")}))
    elif a.command == "download":
        download(key, a.number)
    elif a.command == "ddi":
        ddi(key, a.number)
    elif a.command == "submit":
        submit(key)
    else:
        n = submit(key)
        acq.wait(key, n)
        download(key, n)
        ddi(key, n)


if __name__ == "__main__":
    main()

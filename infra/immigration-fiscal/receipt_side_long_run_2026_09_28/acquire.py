#!/usr/bin/env python3
"""Fetch the public inputs of the receipt-side long-run lane into _cache/ (idempotent, pinned).

  fhfa_land   FHFA Working Paper 19-01 land prices, Version 4.0 (June 2024): land share of single-family
              property value for counties, CBSAs, states and the nation, annual panel 2012-2022.
  bea_s7      BEA NIPA Section 7 workbook (Table 7.4.5, housing sector output and taxes on production).
  tract_puma  Census 2020 tract-to-PUMA relationship file (tracts nest in counties and in PUMAs).
  msa99       Census 1999 MSA/PMSA definitions with county FIPS codes, the metro units of Saiz (2010).
  iuf22       Census 2022 Individual Unit File (property tax by type of local government, FY2022).
  pl2020      Census 2020 PL 94-171 tract population (P1_001N), one API call per state and DC.

Fetches go through curl (Python urllib fails TLS here). The Census key travels to curl on stdin inside a
config line, never in argv; every logged URL passes through redact(). No personal identifier is sent:
the user agent is generic.

  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/receipt_side_long_run_2026_09_28/acquire.py
  uv run --no-project python3 infra/immigration-fiscal/receipt_side_long_run_2026_09_28/acquire.py --check

Without --check, a missing file is fetched and inputs/pins.json gains its sha256 (a pinned file that
changed stops the run). With --check, nothing is fetched: every pinned file must exist with its sha256.
The analysis scripts verify the same pins when they read a file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
PINS = HERE / "inputs" / "pins.json"
UA = "research-script/1.0"
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19", "20",
          "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
          "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]
FILES = {
    "fhfa_land_prices_2024_06.xlsx": "https://www.fhfa.gov/document/land-prices_2024_20_june.xlsx",
    "bea_Section7All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx",
    "census_2020_tract_to_puma.txt": "https://www2.census.gov/geo/docs/maps-data/data/rel2020/2020_Census_Tract_to_2020_PUMA.txt",
    "census_1999_msa_fips.txt": "https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/1999/historical-delineation-files/99mfips.txt",
    "census_2022_individual_unit_file.zip": "https://www2.census.gov/programs-surveys/gov-finances/tables/2022/2022_Individual_Unit_File.zip",
}
PL_URL = "https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=tract:*&in=state:{st}&key={key}"


def redact(s: str) -> str:
    return re.sub(r"key=[^&\s\"']+", "key=<redacted>", s)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curl_to(url: str, out: Path, attempts: int = 4) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".part")
    cfg = f'url = "{url}"\noutput = "{tmp}"\nuser-agent = "{UA}"\n'
    for a in range(1, attempts + 1):
        r = subprocess.run(["curl", "-sS", "--fail", "-L", "--max-time", "600", "--config", "-"],
                           input=cfg.encode(), capture_output=True)
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.replace(out)
            return
        print(f"  ! attempt {a} {redact(url)}: rc={r.returncode} {redact(r.stderr.decode(errors='replace'))[:160]}")
        time.sleep(4 * a)
    if tmp.exists():
        tmp.unlink()
    raise SystemExit(f"[BLOCKED] could not fetch {redact(url)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify pinned files only; fetch nothing")
    args = ap.parse_args()
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    wanted = dict(FILES)
    for st in STATES:
        wanted[f"pl2020_tracts/{st}.json"] = PL_URL.format(st=st, key="{key}")
    if args.check:
        bad = [name for name in wanted if name not in pins or not (CACHE / name).exists()
               or sha256(CACHE / name) != pins[name]["sha256"]]
        if bad:
            raise SystemExit(f"[BLOCKED] missing or changed inputs: {', '.join(bad[:8])}{' ...' if len(bad) > 8 else ''}")
        print(f"ok: {len(wanted)} pinned inputs")
        return
    key = None
    for name, url in wanted.items():
        out = CACHE / name
        if not out.exists():
            if "{key}" in url:
                key = key or os.environ.get("CENSUS_API_KEY", "")
                if not key:
                    raise SystemExit("[BLOCKED] CENSUS_API_KEY missing; source acquire/config.local.env with set -a")
                curl_to(url.replace("{key}", key), out)
            else:
                curl_to(url, out)
            print(f"fetched {name} ({out.stat().st_size:,} bytes)")
        digest = sha256(out)
        if name in pins and pins[name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {name} changed: pinned {pins[name]['sha256'][:12]}, now {digest[:12]}")
        pins[name] = {"url": redact(url.replace("{key}", "KEY")), "bytes": out.stat().st_size, "sha256": digest}
    PINS.write_text(json.dumps(dict(sorted(pins.items())), indent=1) + "\n")
    print(f"pinned {len(pins)} inputs in {PINS.relative_to(HERE)}")


if __name__ == "__main__":
    sys.exit(main())

"""Pull QWI state-level panel: state x year x quarter x education x industry.

Uses Census QWI 'se' endpoint (sex+education dimensions).
Output: parquet at data/lehd/qwi_state_panel.parquet

Cell key: state x year x quarter x education x industry x sex
Coverage: all 50 states + DC, 2003-2023, 4 quarters, E1-E4 education,
8 industries (00 total + 11 Ag + 23 Constr + 31-33 Mfg + 56 Admin + 72 Food + 81 Other + 62 Health),
sex=0 (total only)
"""
from __future__ import annotations
import os
import sys
import time
import json
from pathlib import Path
import requests
import pandas as pd

OUT = Path(__file__).parent.parent / "data" / "lehd"
OUT.mkdir(parents=True, exist_ok=True)
PARQUET = OUT / "qwi_state_panel.parquet"
LOG = OUT / "pull_log.txt"

API = "https://api.census.gov/data/timeseries/qwi/se"

STATES = [
    "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18",
    "19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
    "34","35","36","37","38","39","40","41","42","44","45","46","47","48","49",
    "50","51","53","54","55","56",
]
YEARS = list(range(2003, 2024))
QUARTERS = [1, 2, 3, 4]
EDUCATION = ["E1", "E2", "E3", "E4"]
INDUSTRIES = ["00", "11", "23", "31-33", "44-45", "56", "62", "72", "81"]
GET = "Emp,EmpS,EarnS,EarnBeg,Payroll,sEmp,sEarnS"


def _log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def fetch(state: str, year: int, quarter: int) -> list[dict]:
    """One API call for a single state-year-quarter; loops education x industry inside."""
    rows = []
    for ind in INDUSTRIES:
        for edu in EDUCATION:
            params = {
                "get": GET,
                "for": f"state:{state}",
                "year": str(year),
                "quarter": str(quarter),
                "education": edu,
                "sex": "0",
                "industry": ind,
            }
            try:
                r = requests.get(API, params=params, timeout=30)
            except requests.RequestException as exc:
                _log(f"net-fail {state} {year}Q{quarter} {ind}/{edu}: {exc}")
                continue
            if r.status_code == 204 or not r.text.strip():
                continue
            if r.status_code != 200:
                _log(f"http-{r.status_code} {state} {year}Q{quarter} {ind}/{edu}: {r.text[:120]}")
                continue
            try:
                data = r.json()
            except json.JSONDecodeError:
                _log(f"json-fail {state} {year}Q{quarter} {ind}/{edu}")
                continue
            if not data or len(data) < 2:
                continue
            header = data[0]
            for row in data[1:]:
                rows.append(dict(zip(header, row)))
    return rows


def main() -> int:
    if PARQUET.exists():
        existing = pd.read_parquet(PARQUET)
        done_keys = set(zip(existing["state"], existing["year"].astype(str), existing["quarter"].astype(str)))
        _log(f"resume: {len(existing)} existing rows; {len(done_keys)} state-year-quarter keys covered")
    else:
        existing = pd.DataFrame()
        done_keys = set()

    all_rows: list[dict] = []
    flush_every = 200  # state-year-quarters between writes
    pulled = 0
    for state in STATES:
        for year in YEARS:
            for quarter in QUARTERS:
                if (state, str(year), str(quarter)) in done_keys:
                    continue
                rows = fetch(state, year, quarter)
                all_rows.extend(rows)
                pulled += 1
                if pulled % 25 == 0:
                    _log(f"pulled {pulled} sytriples; running rows={len(all_rows)}")
                if pulled % flush_every == 0:
                    _flush(existing, all_rows)
                    existing = pd.read_parquet(PARQUET)
                    all_rows = []
    if all_rows:
        _flush(existing, all_rows)
    _log("done")
    return 0


def _flush(existing: pd.DataFrame, new_rows: list[dict]) -> None:
    if not new_rows:
        return
    new = pd.DataFrame(new_rows)
    for c in ("Emp", "EmpS", "EarnS", "EarnBeg", "Payroll"):
        if c in new.columns:
            new[c] = pd.to_numeric(new[c], errors="coerce")
    combined = pd.concat([existing, new], ignore_index=True) if len(existing) else new
    combined.to_parquet(PARQUET, index=False)
    _log(f"flushed -> total rows={len(combined)} ({PARQUET.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    sys.exit(main())

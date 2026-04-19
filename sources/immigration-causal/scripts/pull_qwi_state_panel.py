"""Pull QWI state-level panel — BATCHED VERSION.

One API call per (industry, education) pair returns ALL states × ALL quarters.
Total: 9 industries × 4 educations = 36 calls, each returns ~17k rows.

Output: data/lehd/qwi_state_panel.parquet
"""
from __future__ import annotations
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

STATES = ",".join([
    "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18",
    "19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
    "34","35","36","37","38","39","40","41","42","44","45","46","47","48","49",
    "50","51","53","54","55","56",
])
EDUCATION = ["E1", "E2", "E3", "E4"]
INDUSTRIES = ["00", "11", "23", "31-33", "44-45", "56", "62", "72", "81"]
GET = "Emp,EmpS,EarnS,EarnBeg,Payroll"
TIME_RANGE = "from+2003-Q1+to+2023-Q4"


def _log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def fetch(industry: str, education: str) -> list[dict]:
    """One API call for all states × all quarters of given (industry, education)."""
    url = (
        f"{API}?get={GET}&for=state:{STATES}&time={TIME_RANGE}"
        f"&education={education}&sex=0&industry={industry}"
    )
    try:
        r = requests.get(url, timeout=120)
    except requests.RequestException as exc:
        _log(f"net-fail {industry}/{education}: {exc}")
        return []
    if r.status_code == 204:
        return []
    if r.status_code != 200:
        _log(f"http-{r.status_code} {industry}/{education}: {r.text[:160]}")
        return []
    try:
        data = r.json()
    except json.JSONDecodeError:
        _log(f"json-fail {industry}/{education}")
        return []
    if not data or len(data) < 2:
        return []
    header = data[0]
    return [dict(zip(header, row)) for row in data[1:]]


def main() -> int:
    all_rows: list[dict] = []
    n_pairs = len(INDUSTRIES) * len(EDUCATION)
    pair_idx = 0
    for ind in INDUSTRIES:
        for edu in EDUCATION:
            pair_idx += 1
            t0 = time.time()
            rows = fetch(ind, edu)
            dt = time.time() - t0
            _log(f"[{pair_idx:2d}/{n_pairs}] ind={ind:6s} edu={edu}  rows={len(rows):,}  {dt:.1f}s")
            all_rows.extend(rows)
            time.sleep(0.5)  # polite

    df = pd.DataFrame(all_rows)
    for c in ("Emp", "EmpS", "EarnS", "EarnBeg", "Payroll"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "time" in df.columns:
        df["year"] = df["time"].str[:4].astype(int)
        df["quarter"] = df["time"].str[-1].astype(int)
    df.to_parquet(PARQUET, index=False)
    _log(f"DONE: {len(df):,} rows -> {PARQUET} ({PARQUET.stat().st_size/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

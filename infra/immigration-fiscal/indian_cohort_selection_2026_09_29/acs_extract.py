#!/usr/bin/env python3
"""Slim ACS one-year person PUMS 2005-2024 (no 2020) to the India-linked households.

Keeps every person in a household (SERIALNO) that holds at least one India-born person (POBP 210),
with the columns the cohort and future-G2 analyses need. Column names are upper-cased (2005 uses
lower-case `sporder`). Nothing is recoded here; blanks stay null.

Output: `_cache/acs_india_<YEAR>.parquet` (ignored). Skips years already extracted.

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/acs_extract.py [YEAR ...]
"""
from __future__ import annotations

import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[2]
DATA = REPO / "sources" / "immigration-fiscal" / "data"
CACHE = LANE / "_cache"
INDIA = 210

ZIPS = {2019: DATA / "external/acs_pums_2019_1yr/csv_pus.zip",
        2023: DATA / "census/acs_pums_2023_person.zip",
        2024: DATA / "external/acs_pums_2024_1yr/csv_pus.zip"}
for _y in list(range(2005, 2019)) + [2021, 2022]:
    ZIPS[_y] = DATA / f"external/acs_pums_years/csv_pus_{_y}.zip"

WANT = set("""SERIALNO SPORDER PWGTP AGEP SEX HISP RAC1P NATIVITY POBP CIT YOEP SCHL FOD1P SOCP
NAICSP COW WAGP SEMP ADJINC ADJUST REL RELP RELSHIPP ESR HINS3 HINS4 HINS5 HINS6 SSP SSIP MIL PAP
WKHP ST LANX LANP""".split())
STR_COLS = {"SERIALNO", "SOCP", "NAICSP"}


def extract(year: int) -> str:
    out = CACHE / f"acs_india_{year}.parquet"
    if out.exists():
        return f"{year}: exists"
    frames = []
    with zipfile.ZipFile(ZIPS[year]) as z:
        for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
            header = pd.read_csv(z.open(name), nrows=0).columns
            cols = [c for c in header if c.upper() in WANT]
            dtype = {c: str for c in cols if c.upper() in STR_COLS}
            for chunk in pd.read_csv(z.open(name), usecols=cols, dtype=dtype, chunksize=500_000,
                                     low_memory=False):
                chunk.columns = [c.upper() for c in chunk.columns]
                frames.append(chunk)
    d = pd.concat(frames, ignore_index=True)
    n_all = len(d)
    hh = set(d.loc[d.POBP == INDIA, "SERIALNO"])
    d = d[d.SERIALNO.isin(hh)].copy()
    d["YEAR"] = year
    CACHE.mkdir(exist_ok=True)
    tmp = out.with_suffix(".parquet.tmp")
    d.to_parquet(tmp, index=False)
    tmp.rename(out)
    return f"{year}: {n_all:,} persons read, {len(hh):,} households, {len(d):,} kept"


def main(argv: list[str]) -> int:
    years = [int(a) for a in argv] or sorted(ZIPS)
    missing = [y for y in years if not ZIPS[y].exists()]
    if missing:
        raise SystemExit(f"[BLOCKED] missing ACS zips: {missing}")
    with ProcessPoolExecutor(max_workers=4) as ex:
        for msg in ex.map(extract, years):
            print(msg, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

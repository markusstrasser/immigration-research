#!/usr/bin/env python3
"""Extract the ACS 2024 1-year PUMS person columns this lane needs.

Input (read-only): ~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip
Output: _cache/acs2024_ancestry_subset.parquet (gitignored)

Columns: identifiers, person weight + 80 replicate weights, age, citizenship,
nativity, place of birth, recoded detailed Hispanic origin, both ancestry entries,
race, state.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ZIP = Path.home() / "research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"

BASE = ["SERIALNO", "SPORDER", "PWGTP", "AGEP", "CIT", "NATIVITY", "POBP",
        "HISP", "ANC1P", "ANC2P", "RAC1P", "STATE", "SCHL", "WAGP", "PINCP"]
REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = BASE + REPS

DTYPE = {"SERIALNO": "string", "SPORDER": "Int16", "AGEP": "Int16", "CIT": "Int8",
         "NATIVITY": "Int8", "POBP": "Int16", "HISP": "Int16",
         "ANC1P": "Int16", "ANC2P": "Int16", "RAC1P": "Int8", "STATE": "Int16",
         "SCHL": "Int8"}
for c in ["PWGTP", *REPS, "WAGP", "PINCP"]:
    DTYPE[c] = "Int32"


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    out = CACHE / "acs2024_ancestry_subset.parquet"
    if out.exists():
        print(f"cached: {out} ({out.stat().st_size/1e6:.1f} MB) — skipping", flush=True)
        return 0
    frames = []
    with zipfile.ZipFile(ZIP) as z:
        names = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        print(f"members: {names}", flush=True)
        for name in names:
            print(f"reading {name}", flush=True)
            n = 0
            with z.open(name) as fh:
                for chunk in pd.read_csv(fh, usecols=COLS, dtype=DTYPE,
                                         chunksize=250_000, low_memory=False):
                    frames.append(chunk)
                    n += len(chunk)
                    print(f"  {name}: {n:,} rows", flush=True)
    d = pd.concat(frames, ignore_index=True)
    print(f"total person rows: {len(d):,}", flush=True)
    d = d.sort_values(["SERIALNO", "SPORDER"], kind="mergesort").reset_index(drop=True)
    d.to_parquet(out, index=False, compression="zstd")
    print(f"wrote {out} ({out.stat().st_size/1e6:.1f} MB)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Extract the columns this lane needs from ACS 2024 1-year PUMS person files.

Input : ~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip
Output: _cache/acs2024_person_subset.parquet  (gitignored)

Read-only on the raw zip. Streams in chunks so peak memory stays modest.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ZIP = Path.home() / "research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"

BASE = ["SERIALNO", "SPORDER", "PWGTP", "AGEP", "CIT", "CITWP", "YOEP", "DECADE",
        "NATIVITY", "POBP", "ESR", "COW", "OCCP", "MIL", "HINS3", "HINS4", "HINS5",
        "SSP", "SSIP", "PAP", "RELSHIPP", "WAGP", "STATE", "SCHL"]
REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = BASE + REPS

DTYPE = {"SERIALNO": "string", "CIT": "Int8", "NATIVITY": "Int8", "POBP": "Int16",
         "ESR": "Int8", "COW": "Int8", "OCCP": "Int32", "MIL": "Int8",
         "HINS3": "Int8", "HINS4": "Int8", "HINS5": "Int8", "RELSHIPP": "Int8",
         "AGEP": "Int16", "YOEP": "Int16", "CITWP": "Int16", "DECADE": "Int8",
         "SCHL": "Int8", "STATE": "Int16", "SPORDER": "Int16"}
for c in ["PWGTP", *REPS]:
    DTYPE[c] = "Int32"
for c in ["SSP", "SSIP", "PAP", "WAGP"]:
    DTYPE[c] = "Int32"


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    out = CACHE / "acs2024_person_subset.parquet"
    if out.exists():
        print(f"cached: {out} ({out.stat().st_size/1e6:.1f} MB) — skipping extraction",
              flush=True)
        return 0
    frames = []
    with zipfile.ZipFile(ZIP) as z:
        names = [n for n in z.namelist() if n.endswith(".csv")]
        print(f"members: {names}", flush=True)
        for name in sorted(names):
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
    d.to_parquet(out, index=False, compression="zstd")
    print(f"wrote {out} ({out.stat().st_size/1e6:.1f} MB)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

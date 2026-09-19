#!/usr/bin/env python3
"""Arm A step 1: subset ACS 2024 1-year PUMS person records to the columns this
lane needs and write one parquet to _cache/.

Input : _cache/pums/psam_pusa.csv, psam_pusb.csv (extracted from the read-only
        raw zip at ~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/)
Output: _cache/pums_subset_2024.parquet  (kept out of derived/: >5 MB)

All columns are read as VARCHAR (all_varchar) so that leading-zero codes such as
HISP='02' survive, then cast explicitly. No type sniffing.
"""
import sys
import duckdb
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
SRC = CACHE / "pums"
OUT = CACHE / "pums_subset_2024.parquet"

KEEP_STR = ["STATE", "PUMA", "HISP", "NATIVITY", "POBP", "CIT", "COW", "OCCP",
            "SOCP", "INDP", "ESR", "SCHL", "RAC1P", "SEX", "WKL"]
KEEP_INT = ["AGEP", "PWGTP", "WAGP", "SEMP", "PERNP", "INTP", "ADJINC", "WKHP",
            "YOEP"] + [f"PWGTP{i}" for i in range(1, 81)]


def main() -> None:
    files = sorted(SRC.glob("psam_pus*.csv"))
    if len(files) != 2:
        sys.exit(f"expected 2 PUMS csv files, found {len(files)}")
    cols = ", ".join(
        [f"CAST({c} AS VARCHAR) AS {c}" for c in KEEP_STR]
        + [f"TRY_CAST({c} AS BIGINT) AS {c}" for c in KEEP_INT]
    )
    con = duckdb.connect()
    con.execute("PRAGMA threads=6")
    src = "[" + ", ".join(f"'{f}'" for f in files) + "]"
    q = (
        f"COPY (SELECT {cols} FROM read_csv({src}, all_varchar=true, header=true)) "
        f"TO '{OUT}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    print(f"building {OUT.name} from {[f.name for f in files]}", flush=True)
    con.execute(q)
    n, wpop = con.execute(
        f"SELECT COUNT(*), SUM(PWGTP) FROM read_parquet('{OUT}')"
    ).fetchone()
    print(f"rows={n:,} weighted_population={wpop:,}", flush=True)
    # content validation: ACS 2024 1-yr resident population is ~340.1 million
    if not (3.30e8 < wpop < 3.50e8):
        sys.exit(f"FAIL weighted population {wpop:,} outside plausible range")
    if n < 3_300_000:
        sys.exit(f"FAIL row count {n:,} below expected ~3.42M")
    print("OK", flush=True)


if __name__ == "__main__":
    main()

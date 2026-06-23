#!/usr/bin/env python3
"""Load the IPUMS USA Borjas/BGH supply-shock panel into the context warehouse.

Source extract (built manually at usa.ipums.org, logged-in session, 2026-06-23):
  Samples : 1980 5% + 1990 5% + 2000 5% census + 2010 ACS + 2023 ACS
  Vars    : YEAR SAMPLE SERIAL PERWT GQ STATEFIP AGE BPL(+BPLD) CITIZEN YRIMMIG
            EDUC(+EDUCD) RACE(+RACED) EMPSTAT(+EMPSTATD) WKSWORK1 INCTOT
            (+ IPUMS technical preselected)
            FOREIGN-BORN = BPL >= 150 (foreign country). NATIVITY was requested but did
            not materialize in the extract; BPL is the canonical source anyway (NATIVITY
            derives from it). Validated: FB share 6.7%(1980)->15.4%(2023), low-educ cells
            50-80% FB — matches the Census series. The cell rebuild
            (borjas_supply_shock_cell off real decennial data) should use BPL>=150.
  Format  : CSV (.csv.gz), rectangular person

Lands the raw person-level panel as `ipums_usa_borjas_panel` in
immigration_microdata.duckdb — a LOCAL-ONLY warehouse. IPUMS microdata is
license-restricted and MUST NOT be redistributed, so it is kept out of the
aggregate warehouses and the unified release; the education x experience x year
cell aggregation (refreshing borjas_supply_shock_cell / bgh_outcomes_cell off
real decennial data instead of the ACS-2023 proxy) reads from here and writes
the (redistributable) aggregate cells into the context warehouse.

Skips gracefully if the extract has not been downloaded yet.

Run: uv run --with duckdb python load_ipums_borjas_panel.py
"""
from __future__ import annotations

import sys

from paths import data_root, microdata_duckdb_path

TABLE = "ipums_usa_borjas_panel"
# IPUMS writes usa_NNNNN.csv.gz; accept either the gz or expanded csv, any extract number.
SEARCH_DIRS = ["external/ipums/usa_extract", "external/ipums"]


def _find_csv():
    root = data_root()
    for sub in SEARCH_DIRS:
        d = root / sub
        if not d.exists():
            continue
        hits = sorted(d.glob("usa_*.csv.gz")) + sorted(d.glob("usa_*.csv"))
        if hits:
            return hits[-1]  # highest extract number / newest
    return None


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb not installed — run via: uv run --with duckdb python load_ipums_borjas_panel.py")

    csv = _find_csv()
    if csv is None:
        print(f"  ! IPUMS extract not found under {data_root()}/{SEARCH_DIRS[0]} — skip "
              "(download usa_*.csv.gz from usa.ipums.org first)")
        return

    db = microdata_duckdb_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db))
    con.execute(
        f'CREATE OR REPLACE TABLE {TABLE} AS '
        f"SELECT * FROM read_csv_auto('{csv}', sample_size=-1)"
    )
    n = con.execute(f"SELECT count(*) FROM {TABLE}").fetchone()[0]
    cols = [r[0] for r in con.execute(f"DESCRIBE {TABLE}").fetchall()]
    # per-sample row counts if YEAR present
    by_year = []
    if "YEAR" in cols:
        by_year = con.execute(
            f"SELECT YEAR, count(*) n FROM {TABLE} GROUP BY YEAR ORDER BY YEAR"
        ).fetchall()
    con.close()

    print(f"  ✓ loaded {TABLE} from {csv.name}: {n:,} person records, {len(cols)} columns")
    if by_year:
        print("    by year: " + ", ".join(f"{y}={c:,}" for y, c in by_year))
    print(f"    columns: {', '.join(cols)}")


if __name__ == "__main__":
    build()

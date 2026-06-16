#!/usr/bin/env python3
"""Load stage6 Tier A panels into immigration_context.duckdb."""
from __future__ import annotations

import sys
from pathlib import Path

from paths import derived_root, duckdb_path

DERIVED = derived_root()
STAGE6 = DERIVED / "stage6"
DUCKDB_PATH = duckdb_path()

TABLES = [
    "razin_wahba_host_immigration_socx_2000",
    "bilateral_migration_skill_panel",
    "oecd_social_spending_host",
    "un_wpp_total_population_forecast",
    "imf_gdp_per_capita_panel",
    "demographic_push_forecast",
    "borjas_supply_shock_cell_2023",
    "bgh_outcomes_cell_2023",
]


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb required")

    if not DUCKDB_PATH.exists():
        print(f"WARN: skip tier-A context load — {DUCKDB_PATH} missing", file=sys.stderr)
        return

    con = duckdb.connect(str(DUCKDB_PATH))
    loaded = 0
    for table in TABLES:
        p = STAGE6 / f"{table}.csv"
        if not p.exists():
            continue
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{p}')")
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {n} rows")
        loaded += 1

    tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
    if "bilateral_migration_skill_panel" in tables and "razin_wahba_host_immigration_socx_2000" in tables:
        con.execute("""
            CREATE OR REPLACE VIEW v_razin_wahba_regime_test AS
            SELECT
              b.host_country,
              b.source_regime,
              b.skill_diff_migration_rate_2000_pct,
              b.mobility_regime_free,
              b.socx_pct_gdp_avg_1980_1990,
              b.socx_per_capita_ppp_usd_1974_1990,
              h.low_edu_share_immigration_2000,
              h.high_edu_share_immigration_2000,
              h.mobility_regime AS host_mobility_regime
            FROM bilateral_migration_skill_panel b
            LEFT JOIN razin_wahba_host_immigration_socx_2000 h
              ON b.host_country = h.host_country
        """)
    if "demographic_push_forecast" in tables:
        con.execute("""
            CREATE OR REPLACE VIEW v_hanson_demographic_push AS
            SELECT *
            FROM demographic_push_forecast
            WHERE origin_iso3 IN ('MEX','SLV','GTM','HND','DOM')
            ORDER BY origin_iso3, year
        """)
    if "borjas_supply_shock_cell_2023" in tables:
        con.execute("""
            CREATE OR REPLACE VIEW v_borjas_cell_immigrant_share AS
            SELECT education_bucket, experience_group, immigrant_share, avg_earnings, year
            FROM borjas_supply_shock_cell_2023
            ORDER BY education_bucket, experience_group
        """)
    con.close()
    print(f"Loaded {loaded} Tier A tables into {DUCKDB_PATH}")


if __name__ == "__main__":
    build()

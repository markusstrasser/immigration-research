#!/usr/bin/env python3
"""Build the real Borjas/BGH supply-shock cell panel from IPUMS decennial microdata.

Replaces the single-year ACS-2023 proxy (borjas_supply_shock_cell_2023) with real
education x experience x year cells across 1980/1990/2000/2010/2023 — actual
supply-shock variation over four decades.

Reads `ipums_usa_borjas_panel` from the local-only immigration_microdata.duckdb;
writes the AGGREGATE cell table `borjas_supply_shock_panel` into the context
warehouse (aggregates are redistributable → flow into the unified release) plus a
CSV in the derived root for reproducibility.

Design (documented deviations from the ACS male-only anchor):
- ALL workers, both sexes (SEX was not in the extract). The anchor used males only;
  this panel is internally consistent all-sex across every year. immigrant_share is
  robust to this; pooled-sex avg income mixes the gender gap (caveat below).
- Foreign-born = BPL >= 150 (validated vs Census: 6.7%%->15.4%% 1980-2023). NATIVITY
  was not in the extract; BPL is the canonical source.
- avg_total_income is NOMINAL INCTOT (total personal income, not wage) with IPUMS
  N/A codes dropped — DEFLATE (CPI) before any cross-year earnings comparison, and
  prefer INCWAGE for a pure wage analysis. Reported as a secondary outcome.
- employment_rate = employed (EMPSTAT=1) / working-age population (emp-pop ratio).

Run: uv run --with duckdb python build_borjas_supply_shock_panel.py
"""
from __future__ import annotations

import sys

from paths import derived_root, duckdb_path, microdata_duckdb_path

TABLE = "borjas_supply_shock_panel"
SOURCE = "ipums_usa_5pct+acs_1980_2023_allsex_bpl"

# IPUMS EDUC general -> 4 standard buckets; assumed years of schooling for potential experience
EDUC_SQL = """
  CASE WHEN EDUC BETWEEN 1 AND 5 THEN 'HSD'   -- < high school
       WHEN EDUC = 6              THEN 'HSG'   -- high school grad
       WHEN EDUC BETWEEN 7 AND 9  THEN 'SMC'   -- some college
       WHEN EDUC BETWEEN 10 AND 11 THEN 'COL'  -- college+
  END"""
EDUC_YEARS_SQL = "CASE WHEN EDUC BETWEEN 1 AND 5 THEN 10 WHEN EDUC=6 THEN 12 WHEN EDUC BETWEEN 7 AND 9 THEN 14 ELSE 16 END"


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb not installed — run via: uv run --with duckdb python build_borjas_supply_shock_panel.py")

    md = microdata_duckdb_path()
    ctx = duckdb_path()
    if not md.exists():
        print(f"  ! IPUMS microdata {md} absent — skip supply-shock panel "
              "(needs the manual IPUMS extract; load_ipums_borjas_panel.py)")
        return
    if not ctx.exists():
        sys.exit(f"missing context warehouse {ctx} — run reproduce.sh build context first")

    con = duckdb.connect(str(ctx))
    con.execute(f"ATTACH '{md}' AS md (READ_ONLY)")

    # one row per year x education x experience-band
    con.execute(f"""
        CREATE OR REPLACE TABLE {TABLE} AS
        WITH base AS (
            SELECT
                YEAR AS year,
                {EDUC_SQL} AS education_bucket,
                LEAST(40, GREATEST(0, AGE - ({EDUC_YEARS_SQL}) - 6)) AS potential_exp,
                BPL >= 150 AS is_foreign_born,
                EMPSTAT = 1 AS employed,
                INCTOT NOT IN (9999998, 9999999) AS inc_valid,
                INCTOT, PERWT
            FROM md.ipums_usa_borjas_panel
            WHERE AGE BETWEEN 18 AND 64 AND EDUC BETWEEN 1 AND 11
        ),
        celled AS (
            SELECT *,
                CASE WHEN potential_exp <= 5 THEN '01-05'
                     WHEN potential_exp <= 10 THEN '06-10'
                     WHEN potential_exp <= 15 THEN '11-15'
                     WHEN potential_exp <= 20 THEN '16-20'
                     WHEN potential_exp <= 25 THEN '21-25'
                     WHEN potential_exp <= 30 THEN '26-30'
                     WHEN potential_exp <= 35 THEN '31-35'
                     ELSE '36-40' END AS experience_group
            FROM base
        )
        SELECT
            year,
            education_bucket,
            experience_group,
            SUM(CASE WHEN is_foreign_born THEN PERWT ELSE 0 END) AS immigrant_weight,
            SUM(CASE WHEN NOT is_foreign_born THEN PERWT ELSE 0 END) AS native_weight,
            SUM(CASE WHEN is_foreign_born THEN PERWT ELSE 0 END) / NULLIF(SUM(PERWT), 0) AS immigrant_share,
            SUM(CASE WHEN employed THEN PERWT ELSE 0 END) / NULLIF(SUM(PERWT), 0) AS employment_rate,
            SUM(CASE WHEN inc_valid THEN INCTOT * PERWT ELSE 0 END)
                / NULLIF(SUM(CASE WHEN inc_valid THEN PERWT ELSE 0 END), 0) AS avg_total_income_nominal,
            COUNT(*) AS n_unweighted,
            '{SOURCE}' AS source
        FROM celled
        GROUP BY 1, 2, 3
        ORDER BY 1, 2, 3
    """)

    rows = con.execute(f"SELECT count(*) FROM {TABLE}").fetchone()[0]
    # write CSV for reproducibility
    out_dir = derived_root() / "tier_a"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"{TABLE}.csv"
    con.execute(f"COPY (SELECT * FROM {TABLE}) TO '{out_csv}' (HEADER)")

    # quick validation surface: low-education immigrant share over time
    val = con.execute(f"""
        SELECT year,
               round(100*SUM(CASE WHEN education_bucket='HSD' THEN immigrant_weight END)
                     / NULLIF(SUM(CASE WHEN education_bucket='HSD' THEN immigrant_weight+native_weight END),0),1) AS hsd_imm_share,
               round(100*SUM(immigrant_weight)/NULLIF(SUM(immigrant_weight+native_weight),0),1) AS all_imm_share
        FROM {TABLE} GROUP BY year ORDER BY year
    """).fetchall()
    con.close()

    print(f"  ✓ wrote {TABLE}: {rows} cells (5 years x 4 educ x 8 exp), CSV → {out_csv}")
    print("  supply-shock check — immigrant share of workers, by year:")
    print("    year   <HS-dropout    all")
    for y, hsd, alls in val:
        print(f"    {y}     {hsd:>6}%      {alls:>5}%")
    print("  (the <HS column IS the low-skill supply shock; rising = more immigrant competition)")


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""First-generation immigrant assimilation profile by origin × years-in-US (synthetic cohorts).

THE EMPIRICAL CONTENT for cluster-V's persistence/decay question that this warehouse CAN
test — and a precise statement of the one it CANNOT.

WHAT THIS MEASURES (and the honest bound):
  How the FIRST-GENERATION immigrant<->native gap (employment, income) closes with
  YEARS-SINCE-ARRIVAL, by origin region, using SYNTHETIC COHORTS: each (origin x
  arrival-decade) cell is tracked across the 1980/1990/2000/2010/2023 census years, so a
  cohort's outcomes are followed as it ages in the US. Tracking within a fixed arrival
  cohort removes Borjas's cohort-quality confound (a cross-section years-in-US profile
  conflates assimilation with secular decline in arrival-cohort quality).

  This bears on cluster-V's V04 (assimilation speed) and V08 (the convergence null): fast
  first-gen convergence is evidence AGAINST strong fixed-trait persistence.

WHAT THIS IS NOT:
  This is WITHIN-first-generation assimilation, NOT cross-generational cultural transmission.
  The true 2nd-generation-by-origin decay (V02) needs PARENTAL birthplace, which IPUMS-USA
  dropped after 1970 and this extract lacks (BPL/CITIZEN/YRIMMIG only, no FBPL/MBPL). That
  test requires an IPUMS-CPS extract (father's/mother's birthplace) — a separate gated
  acquisition. Do NOT read first-gen convergence here as the 2nd-gen transmission rate.

  Output is a REDISTRIBUTABLE AGGREGATE (cell means, no microdata) → flows to the unified
  release like the other IPUMS-derived tables. The raw microdata stays local-only.

Run: PNY_DATA_ROOT=/Volumes/2TBPNY/projects-offload/research-sources/immigration-fiscal/data \\
     uv run --with duckdb python build_immigrant_assimilation_profile.py   (skips if microdata absent)
"""
from __future__ import annotations

import sys

from paths import duckdb_path, microdata_duckdb_path

# IPUMS BPL general-code → origin region. foreign-born = BPL>=150.
REGION_CASE = """
  CASE
    WHEN BPL=200 THEN 'Mexico'
    WHEN BPL=210 THEN 'Central America'
    WHEN BPL IN (250,260) THEN 'Caribbean'
    WHEN BPL=300 THEN 'South America'
    WHEN BPL BETWEEN 400 AND 499 THEN 'Europe'
    WHEN BPL BETWEEN 500 AND 599 THEN 'Asia'
    WHEN BPL BETWEEN 600 AND 699 THEN 'Africa'
    WHEN BPL=150 THEN 'Canada'
    ELSE 'Other'
  END
"""

# arrival-decade bins from YRIMMIG; the synthetic-cohort key tracked across census years.
COHORT_CASE = """
  CASE
    WHEN YRIMMIG=0 THEN NULL
    WHEN YRIMMIG<1970 THEN 'pre-1970'
    WHEN YRIMMIG<1980 THEN '1970s'
    WHEN YRIMMIG<1990 THEN '1980s'
    WHEN YRIMMIG<2000 THEN '1990s'
    WHEN YRIMMIG<2010 THEN '2000s'
    WHEN YRIMMIG<2020 THEN '2010s'
    ELSE '2020s'
  END
"""


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python build_immigrant_assimilation_profile.py")

    md = microdata_duckdb_path()
    if not md.exists():
        print(f"  ! IPUMS microdata not at {md} (set PNY_DATA_ROOT to the SSD root); skipping")
        return

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing context warehouse {db} — run reproduce.sh build context first")

    con = duckdb.connect(str(db))
    con.execute(f"ATTACH '{md}' AS md (READ_ONLY)")
    T = "md.ipums_usa_borjas_panel"

    # working-age, valid-income filters; emp=EMPSTAT 1; income from INCTOT (drop NIU/topcode sentinels)
    base_filter = "AGE BETWEEN 25 AND 64"
    inc_ok = "INCTOT > 0 AND INCTOT < 9999998"

    # immigrant cells: origin region x arrival cohort x census year
    con.execute(f"""
        CREATE OR REPLACE TABLE immigrant_assimilation_profile AS
        WITH imm AS (
            SELECT YEAR,
                   {REGION_CASE} AS origin_region,
                   {COHORT_CASE} AS arrival_cohort,
                   YEAR - YRIMMIG AS years_in_us,
                   PERWT,
                   CASE WHEN EMPSTAT=1 THEN 1.0 ELSE 0.0 END AS employed,
                   CASE WHEN {inc_ok} THEN ln(INCTOT) END AS log_inc
            FROM {T}
            WHERE BPL>=150 AND {base_filter} AND YRIMMIG>0
        ),
        nat AS (
            SELECT YEAR,
                   sum(PERWT*CASE WHEN EMPSTAT=1 THEN 1.0 ELSE 0.0 END)/sum(PERWT) AS nat_emp_rate,
                   sum(PERWT*CASE WHEN {inc_ok} THEN ln(INCTOT) END)
                     FILTER (WHERE {inc_ok})/sum(PERWT) FILTER (WHERE {inc_ok}) AS nat_log_inc
            FROM {T}
            WHERE BPL<150 AND {base_filter}
            GROUP BY YEAR
        )
        SELECT i.YEAR AS census_year,
               i.origin_region,
               i.arrival_cohort,
               round(sum(i.PERWT*i.years_in_us)/sum(i.PERWT),1) AS mean_years_in_us,
               round(sum(i.PERWT*i.employed)/sum(i.PERWT),4) AS emp_rate,
               round(n.nat_emp_rate,4) AS native_emp_rate,
               round(sum(i.PERWT*i.employed)/sum(i.PERWT) - n.nat_emp_rate,4) AS emp_gap,
               round(sum(i.PERWT*i.log_inc) FILTER (WHERE i.log_inc IS NOT NULL)
                     /sum(i.PERWT) FILTER (WHERE i.log_inc IS NOT NULL),4) AS mean_log_inc,
               round(n.nat_log_inc,4) AS native_log_inc,
               round(sum(i.PERWT*i.log_inc) FILTER (WHERE i.log_inc IS NOT NULL)
                     /sum(i.PERWT) FILTER (WHERE i.log_inc IS NOT NULL) - n.nat_log_inc,4) AS log_inc_gap,
               round(sum(i.PERWT)) AS weighted_n,
               count(*) AS n_obs
        FROM imm i JOIN nat n USING (YEAR)
        WHERE i.arrival_cohort IS NOT NULL
        GROUP BY 1,2,3,n.nat_emp_rate,n.nat_log_inc
        HAVING count(*) >= 100
        ORDER BY origin_region, arrival_cohort, census_year
    """)

    n = con.execute("SELECT count(*) FROM immigrant_assimilation_profile").fetchone()[0]

    # headline: Mexican synthetic cohorts — does the income gap to natives close with years-in-US?
    head = con.execute("""
        SELECT arrival_cohort, census_year, mean_years_in_us, emp_gap, log_inc_gap, weighted_n
        FROM immigrant_assimilation_profile
        WHERE origin_region='Mexico' AND arrival_cohort IN ('1980s','1990s')
        ORDER BY arrival_cohort, census_year
    """).fetchall()

    # export aggregate CSV
    from paths import derived_root
    out = derived_root() / "lifetime"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY immigrant_assimilation_profile TO '{out / 'immigrant_assimilation_profile.csv'}' (HEADER)")
    con.close()

    print(f"  ✓ immigrant_assimilation_profile: {n} cells (origin x arrival-cohort x census-year, n_obs>=100)")
    print("  headline — Mexican synthetic cohorts, gap to native (25-64):")
    print("    cohort | year | yrs-in-US | emp_gap | log_inc_gap | wt")
    for r in head:
        print(f"    {r[0]:>6} | {r[1]} | {r[2]:>5.0f} | {r[3]:+.3f} | {r[4]:+.3f} | {int(r[5]):,}")


if __name__ == "__main__":
    build()

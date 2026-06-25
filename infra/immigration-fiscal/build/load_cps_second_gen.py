#!/usr/bin/env python3
"""Cluster-V V02 — 2nd-generation-by-origin cultural-transmission test (IPUMS-CPS).

THE test the IPUMS-USA panel cannot do: true CROSS-GENERATIONAL decay. IPUMS-USA dropped
parental birthplace after 1970; IPUMS-CPS keeps it (FBPL/MBPL) and a constructed NATIVITY
generation code — so we can compare 2nd-generation immigrants (US-born, foreign-born parents)
to the 3rd+ native baseline, BY parental origin, holding US institutions constant. That is the
epidemiological identification of transmitted culture (V02) and the cross-generational bound on
ethnic-capital persistence (V04) — both of which the first-gen `immigrant_assimilation_profile`
can only approximate.

GATED INPUT (not in the repo). Stage an IPUMS-CPS ASEC extract as CSV at:
    <data_root>/external/cps/cps_2ndgen.csv[.gz]
Build it at https://cps.ipums.org with samples = ASEC 1994→ and variables:
    YEAR SERIAL PERNUM ASECWT AGE SEX NATIVITY BPL FBPL MBPL CITIZEN YRIMMIG
    EMPSTAT LABFORCE INCTOT EDUC
Choose CSV output (Data Format → "Comma delimited (.csv)"). Spec + caveats:
    research/immigration-gated-data-specs-2026-06-25.md  (§1 IPUMS-CPS).
This script SKIPS cleanly if the extract is absent (same pattern as the gated crime loaders).

NATIVITY codes (IPUMS): 1 = both parents native-born (3rd+); 2 = father foreign / mother native;
3 = mother foreign / father native; 4 = both parents foreign (core 2nd-gen); 5 = foreign-born (1st-gen).
Parental origin = FBPL (fall back to MBPL when father is native), mapped to region via the same
BPL scheme as the IPUMS-USA loaders.

Output (REDISTRIBUTABLE AGGREGATE → flows to the unified release; raw CPS stays local):
    cps_second_gen_by_origin — generation × parental-origin region × outcome means, ASECWT-weighted.

Run: PNY_DATA_ROOT=<ssd> uv run --with duckdb python load_cps_second_gen.py   (skips if absent)
"""
from __future__ import annotations

import sys

from paths import data_root, derived_root, duckdb_path

# IPUMS BPL general-code → origin region (same scheme as build_immigrant_assimilation_profile.py).
# Applied to the PARENTAL birthplace (FBPL, or MBPL when father native).
REGION_CASE = """
  CASE
    WHEN bpl_origin=200 THEN 'Mexico'
    WHEN bpl_origin=210 THEN 'Central America'
    WHEN bpl_origin IN (250,260) THEN 'Caribbean'
    WHEN bpl_origin=300 THEN 'South America'
    WHEN bpl_origin BETWEEN 400 AND 499 THEN 'Europe'
    WHEN bpl_origin BETWEEN 500 AND 599 THEN 'Asia'
    WHEN bpl_origin BETWEEN 600 AND 699 THEN 'Africa'
    WHEN bpl_origin=150 THEN 'Canada'
    ELSE 'Other'
  END
"""

GEN_CASE = """
  CASE NATIVITY
    WHEN 1 THEN '3rd+_native_parentage'
    WHEN 2 THEN '2nd_father_foreign'
    WHEN 3 THEN '2nd_mother_foreign'
    WHEN 4 THEN '2nd_both_foreign'
    WHEN 5 THEN '1st_foreign_born'
    ELSE 'unknown'
  END
"""


def _find_extract(d):
    for name in ("cps_2ndgen.csv", "cps_2ndgen.csv.gz"):
        p = d / "external" / "cps" / name
        if p.exists():
            return p
    return None


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python load_cps_second_gen.py")

    src = _find_extract(data_root())
    if src is None:
        print(f"  ! IPUMS-CPS extract not staged at {data_root()/'external'/'cps'/'cps_2ndgen.csv'} "
              f"(gated — see immigration-gated-data-specs-2026-06-25.md); skipping")
        return

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing context warehouse {db} — run reproduce.sh build context first")

    con = duckdb.connect(str(db))
    con.execute(f"CREATE OR REPLACE TEMP VIEW _cps AS SELECT * FROM read_csv_auto('{src}', header=true)")

    # working-age; parental origin = father's BPL, fall back to mother's when father US-born (<150).
    # NATIVITY 1 (3rd+) has no foreign parent → origin 'native_baseline'.
    con.execute(f"""
        CREATE OR REPLACE TABLE cps_second_gen_by_origin AS
        WITH base AS (
            SELECT
                CAST(NATIVITY AS INT) AS NATIVITY,
                CAST(ASECWT AS DOUBLE) AS w,
                CASE WHEN CAST(FBPL AS INT) >= 150 THEN CAST(FBPL AS INT)
                     WHEN CAST(MBPL AS INT) >= 150 THEN CAST(MBPL AS INT)
                     ELSE NULL END AS bpl_origin,
                -- [VERIFY-AT-EXTRACT against the DDI] CPS EMPSTAT: 10=at work, 12=has job not at work = employed
                CASE WHEN CAST(EMPSTAT AS INT) IN (10,12) THEN 1.0 ELSE 0.0 END AS employed,
                -- [VERIFY-AT-EXTRACT] CPS INCTOT NIU sentinel is 999999999; keep real (incl. topcoded) income only
                CASE WHEN CAST(INCTOT AS BIGINT) BETWEEN 1 AND 99999998 THEN ln(CAST(INCTOT AS DOUBLE)) END AS log_inc,
                CAST(EDUC AS INT) AS educ,
                CASE WHEN CAST(SEX AS INT)=2 AND CAST(LABFORCE AS INT)=2 THEN 1.0
                     WHEN CAST(SEX AS INT)=2 THEN 0.0 END AS female_in_lf
            FROM _cps
            WHERE CAST(AGE AS INT) BETWEEN 25 AND 64
        )
        SELECT
            {GEN_CASE} AS generation,
            CASE WHEN NATIVITY=1 THEN 'native_baseline' ELSE {REGION_CASE} END AS parental_origin,
            round(sum(w*employed)/sum(w),4) AS emp_rate,
            round(sum(w*log_inc) FILTER (WHERE log_inc IS NOT NULL)
                  /sum(w) FILTER (WHERE log_inc IS NOT NULL),4) AS mean_log_inc,
            round(sum(w*educ)/sum(w),2) AS mean_educ,
            round(sum(w*female_in_lf) FILTER (WHERE female_in_lf IS NOT NULL)
                  /sum(w) FILTER (WHERE female_in_lf IS NOT NULL),4) AS female_lfp,
            round(sum(w)) AS weighted_n,
            count(*) AS n_obs
        FROM base
        WHERE NATIVITY IN (1,2,3,4,5)
        GROUP BY 1,2
        HAVING count(*) >= 100
        ORDER BY generation, parental_origin
    """)

    n = con.execute("SELECT count(*) FROM cps_second_gen_by_origin").fetchone()[0]
    out = derived_root() / "lifetime"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY cps_second_gen_by_origin TO '{out / 'cps_second_gen_by_origin.csv'}' (HEADER)")

    # headline: does the immigrant<->native gap DECAY from 1st to 2nd generation, by origin?
    head = con.execute("""
        SELECT parental_origin,
               max(CASE WHEN generation='1st_foreign_born'  THEN mean_log_inc END) AS g1_loginc,
               max(CASE WHEN generation='2nd_both_foreign'   THEN mean_log_inc END) AS g2_loginc,
               (SELECT mean_log_inc FROM cps_second_gen_by_origin WHERE generation='3rd+_native_parentage') AS native_loginc
        FROM cps_second_gen_by_origin
        WHERE parental_origin NOT IN ('native_baseline','Other')
        GROUP BY parental_origin ORDER BY parental_origin
    """).fetchall()
    con.close()

    print(f"  ✓ cps_second_gen_by_origin: {n} cells (generation × parental-origin, n_obs>=100)")
    print("  V02 decay — log-income gap to native baseline, 1st-gen → 2nd-gen (both-foreign):")
    print("    origin | 1st_loginc | 2nd_loginc | native_loginc")
    for r in head:
        f = lambda x: f"{x:.3f}" if x is not None else "  —  "
        print(f"    {r[0]:>16} | {f(r[1])} | {f(r[2])} | {f(r[3])}")


if __name__ == "__main__":
    build()

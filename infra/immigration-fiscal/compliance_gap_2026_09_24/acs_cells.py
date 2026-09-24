#!/usr/bin/env python3
"""ACS workers by state of work x industry cell x year, with nativity and imputed-status counts.

Input: _cache/ipums/workers*.parquet (acs_prepare.py), ACS 1-year 2005-2024, employed persons.
Output: _cache/panel/acs_cells.parquet, one row per state x cell x year x half, where half is
'all' or the household split 0/1 (SERIAL parity) used to break the shared sampling error between
a share and a ratio built on the same ACS counts.

State is the state of work (PWSTATE2, 1-56) and, for people not at work in the reference week,
the state of residence, because QCEW counts jobs where the establishment is.

Worker classes (CLASSWKRD): private wage and salary 22 and non-profit 23 (QCEW's private
ownership includes non-profits), incorporated self-employed 14 (UI-covered as corporate officers in
most states; a sensitivity), unincorporated self-employed 13, unpaid family 29, government 24-28.

Groups: foreign-born is BPL >= 150 with CITIZEN 2 or 3; Mexico-born noncitizen is BPL 200 and
CITIZEN 3; imputed unauthorized follows the Borjas (2017) residual rules that the ACS carries
(../status_impute_2026_09_16 ports them to the CPS): a foreign-born noncitizen who arrived in 1980
or later, was not born in Cuba, has no Social Security or SSI income, no Medicaid, Medicare, VA or
TRICARE coverage, is not a veteran, does not work for government, and has no spouse who is US-born
or a citizen. The ACS lacks two of the paper's rules (public or subsidised housing; licensed
occupations), so this flag over-counts slightly. It also takes in temporary visa holders such as
H-1B workers (imputed "unauthorized" in professional services earn about $97k on average), so a
variant keeps only those without a bachelor's degree (ws_unauth_noba). Insurance items start in
2008, so the flag is NULL before 2008.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/acs_cells.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import acs_case_sql  # noqa: E402

SRC = HERE / "_cache" / "ipums"
OUT = HERE / "_cache" / "panel" / "acs_cells.parquet"

PERSON = f"""
SELECT "YEAR" AS year,
  CASE WHEN PWSTATE2 BETWEEN 1 AND 56 THEN PWSTATE2 ELSE STATEFIP END AS st,
  {acs_case_sql()} AS cell,
  (SERIAL % 2)::VARCHAR AS half,
  PERWT AS w,
  CLASSWKRD AS cw,
  CASE WHEN INCWAGE BETWEEN 0 AND 999997 THEN INCWAGE ELSE NULL END AS wage,
  (BPL >= 150 AND CITIZEN IN (2, 3)) AS fb,
  (BPL >= 150 AND CITIZEN = 3) AS fbnc,
  (BPL = 200 AND CITIZEN = 3) AS mexnc,
  (BPL = 200) AS mexborn,
  (HISPAN BETWEEN 1 AND 4) AS hisp,
  (EDUC <= 6) AS hs_or_less,
  (EDUC <= 9) AS no_ba,
  CASE WHEN "YEAR" < 2008 THEN NULL ELSE
    (BPL >= 150 AND CITIZEN = 3 AND YRIMMIG >= 1980 AND BPL <> 250
     AND coalesce(INCSS, 0) IN (0, 99999) AND coalesce(INCSUPP, 0) IN (0, 99999)
     AND HINSCAID <> 2 AND HINSCARE <> 2 AND HINSVA <> 2 AND HINSTRI <> 2
     AND VETSTAT <> 2 AND CLASSWKRD NOT BETWEEN 24 AND 28
     AND NOT (coalesce(BPL_SP, 0) BETWEEN 1 AND 120) AND coalesce(CITIZEN_SP, 0) NOT IN (1, 2))
  END AS unauth
FROM read_parquet('{SRC}/workers*.parquet')
"""

AGG = """
SELECT year, st, cell, half,
  count(*) FILTER (WHERE cw IN (22, 23)) AS n_ws,
  sum(w) FILTER (WHERE cw IN (22, 23)) AS ws,
  sum(w) FILTER (WHERE cw = 22) AS ws_forprofit,
  sum(w) FILTER (WHERE cw = 14) AS se_inc,
  sum(w) FILTER (WHERE cw = 13) AS se_uninc,
  sum(w) FILTER (WHERE cw = 29) AS unpaid,
  sum(w) FILTER (WHERE cw BETWEEN 24 AND 28) AS govt,
  sum(w) AS all_emp,
  count(*) AS n_all,
  sum(w) FILTER (WHERE cw IN (22, 23) AND fb) AS ws_fb,
  sum(w) FILTER (WHERE cw IN (22, 23) AND fbnc) AS ws_fbnc,
  sum(w) FILTER (WHERE cw IN (22, 23) AND mexnc) AS ws_mexnc,
  sum(w) FILTER (WHERE cw IN (22, 23) AND mexborn) AS ws_mexborn,
  sum(w) FILTER (WHERE cw IN (22, 23) AND hisp) AS ws_hisp,
  sum(w) FILTER (WHERE cw IN (22, 23) AND unauth) AS ws_unauth,
  sum(w) FILTER (WHERE cw IN (22, 23) AND unauth AND no_ba) AS ws_unauth_noba,
  sum(w) FILTER (WHERE cw IN (22, 23) AND hs_or_less) AS ws_hsless,
  sum(w) FILTER (WHERE fbnc) AS all_fbnc,
  sum(w) FILTER (WHERE mexnc) AS all_mexnc,
  sum(w) FILTER (WHERE unauth) AS all_unauth,
  sum(w) FILTER (WHERE cw = 13 AND mexnc) AS se_uninc_mexnc,
  sum(w) FILTER (WHERE cw = 13 AND unauth) AS se_uninc_unauth,
  sum(w * wage) FILTER (WHERE cw IN (22, 23)) AS ws_wagebill,
  sum(w * wage) FILTER (WHERE cw IN (22, 23) AND unauth) AS ws_wagebill_unauth,
  sum(w * wage) FILTER (WHERE cw IN (22, 23) AND unauth AND no_ba) AS ws_wagebill_unauth_noba,
  sum(w * wage) FILTER (WHERE cw IN (22, 23) AND mexnc) AS ws_wagebill_mexnc
FROM p WHERE cell IS NOT NULL AND st BETWEEN 1 AND 56
GROUP BY GROUPING SETS ((year, st, cell, half), (year, st, cell))
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='3GB'; SET threads=4; SET preserve_insertion_order=false")
    con.execute(f"CREATE TEMP VIEW p AS {PERSON}")
    unmapped = con.execute("""SELECT count(*), sum(w) FROM p
        WHERE cell IS NULL AND cw IN (22, 23)""").fetchone()
    con.execute(f"""COPY (SELECT * REPLACE (coalesce(half, 'all') AS half) FROM ({AGG}))
        TO '{OUT}' (FORMAT parquet)""")
    rows, cells, years, states = con.execute(f"""SELECT count(*), count(DISTINCT cell), count(DISTINCT year),
        count(DISTINCT st) FROM '{OUT}' WHERE half = 'all'""").fetchone()
    print(f"✓ {OUT.name}: {rows:,} state x cell x year rows ('all'), {cells} cells, {years} years, {states} states")
    print(f"  private wage/salary records outside the partition (public administration, military, unknown): "
          f"{unmapped[0]:,} ({(unmapped[1] or 0) / 1e6 / 20:.2f}m a year)")


if __name__ == "__main__":
    main()

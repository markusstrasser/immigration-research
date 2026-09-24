#!/usr/bin/env python3
"""Test A: what enforcement finds, by industry cell, FY2010-2024 (WHD) and 2010-2024 (OSHA).

WHD (wage and hour): back wages found, employees owed and civil money penalties per case, per
employee, per employee-year of the findings period, per covered worker (QCEW private employment of
the cell) and as a share of the cell's QCEW payroll. OSHA: inspections of private establishments
opened in each year, penalties (current, after settlement, summed over the inspection's
non-deleted violations), per inspection, per covered worker and as a share of payroll.

Every per-year figure is computed one year at a time and then averaged; min and max over years are
reported. Enforcement records show violations where inspectors looked, not prevalence. Per case
they overstate the typical firm (inspectors look where violations are likely); per covered worker
they understate total violations (most firms are never inspected).

The WHD case file has no case-closing date ("Findings Start Date and Findings End Date are not
equal to Case Open Date and Case Close Date, which are not included in the dataset", DOL API
dataset 10362 metadata, saved as _cache/papers/dol_whd_enforcement_metadata.txt), although the
same metadata says "The dataset contains all concluded WHD compliance actions since FY 2005".
Cases are dated by the fiscal year of FINDINGS_END_DATE. The gate compares the file with DOL's
published "All Acts" table (reads/LIT_COMPLIANCE_COSTS.md section 2) on that basis and on the
record load date.

Outputs: derived/whd_gate.csv, derived/enforcement_by_cell.csv, derived/enforcement_by_cell_year.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/enforcement.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import CELLS, FOCUS  # noqa: E402

DOL = HERE / "_cache" / "dol"
PANEL = HERE / "_cache" / "panel"
DER = HERE / "derived"
YEARS = (2010, 2024)
PUBLISHED = {  # DOL WHD "All Acts" table: concluded actions, back wages, employees receiving BW, CMPs
    2013: (33146, 249954412, 269250, 16169087), 2014: (29483, 240831606, 270570, 12416855),
    2015: (27914, 246780891, 240340, 12231179), 2016: (28589, 266566178, 283677, 14761891),
    2017: (28771, 270403906, 240608, 13810028), 2018: (28397, 304914114, 265027, 15741194),
    2019: (26876, 322490774, 313941, 19522169), 2020: (26096, 257829604, 229934, 17871969),
    2021: (24746, 234362486, 193796, 20399042), 2022: (20422, 213161638, 152970, 21613896),
    2023: (20215, 212325391, 163768, 25834687), 2024: (17300, 202676115, 151989, 35920310),
    2025: (16924, 259294764, 176957, 58699936),
}


def naics_cell_sql(col: str) -> str:
    """Map a NAICS code string (2-6 digits) to the lane's cells; NULL for government or unknown."""
    rules = [("56173", "c56173"), ("5617", "c5617z"), ("7224", "c7224"), ("722", "c722z"), ("721", "c721"),
             ("814", "c814"), ("111", "c111"), ("112", "c112"), ("115", "c115"), ("113", "c11r"),
             ("114", "c11r"), ("21", "c21"), ("22", "c22"), ("23", "c23"), ("31", "c31"), ("32", "c31"),
             ("33", "c31"), ("42", "c42"), ("44", "c44"), ("45", "c44"), ("48", "c48"), ("49", "c48"),
             ("51", "c51"), ("52", "c52"), ("53", "c53"), ("54", "c54"), ("55", "c55"), ("56", "c56r"),
             ("61", "c61"), ("62", "c62"), ("71", "c71"), ("81", "c81r")]
    return "CASE " + " ".join(f"WHEN {col} LIKE '{p}%' THEN '{c}'" for p, c in rules) + " ELSE NULL END"


def fy(col: str) -> str:
    d = f"try_cast(substr({col}, 1, 10) AS DATE)"
    return f"(year({d}) + (month({d}) >= 10)::INT)"


def main() -> None:
    DER.mkdir(exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='3GB'; SET threads=4")
    con.execute(f"""CREATE TEMP TABLE w AS SELECT case_id, naic_cd,
        {naics_cell_sql('naic_cd')} AS cell, naic_cd LIKE '09%' OR naic_cd LIKE '92%' AS govt,
        {fy('findings_end_date')} AS fy_end, {fy('load_dt')} AS fy_load,
        try_cast(substr(findings_start_date, 1, 10) AS DATE) AS f0, try_cast(substr(findings_end_date, 1, 10) AS DATE) AS f1,
        coalesce(try_cast(bw_atp_amt AS DOUBLE), 0) AS bw, coalesce(try_cast(ee_atp_cnt AS BIGINT), 0) AS ee,
        coalesce(try_cast(cmp_assd AS DOUBLE), 0) AS cmp, coalesce(try_cast(case_violtn_cnt AS BIGINT), 0) AS viol,
        coalesce(try_cast(flsa_mw_bw_atp_amt AS DOUBLE), 0) AS bw_mw, coalesce(try_cast(flsa_ot_bw_atp_amt AS DOUBLE), 0) AS bw_ot,
        coalesce(try_cast(h2a_bw_atp_amt AS DOUBLE), 0) + coalesce(try_cast(mspa_bw_atp_amt AS DOUBLE), 0) AS bw_farmlabor,
        coalesce(try_cast(dbra_bw_atp_amt AS DOUBLE), 0) AS bw_dbra
        FROM read_csv('{DOL}/whd_cases.csv.gz', header=true, all_varchar=true)""")
    # --- gate: file against DOL's published fiscal-year totals
    gate = []
    for basis in ("fy_end", "fy_load"):
        got = dict((r[0], r[1:]) for r in con.execute(
            f"SELECT {basis}, count(*), sum(bw), sum(ee), sum(cmp) FROM w GROUP BY 1").fetchall())
        for year, (n_pub, bw_pub, ee_pub, cmp_pub) in PUBLISHED.items():
            n, bw, ee, cmp_ = got.get(year, (0, 0, 0, 0))
            gate.append({"basis": basis, "fiscal_year": year, "cases_file": n, "cases_published": n_pub,
                         "cases_ratio": n / n_pub, "bw_file": bw, "bw_published": bw_pub, "bw_ratio": bw / bw_pub,
                         "employees_file": ee, "employees_published": ee_pub, "employees_ratio": ee / ee_pub,
                         "cmp_file": cmp_, "cmp_published": cmp_pub,
                         "match_within_2pct": abs(n / n_pub - 1) <= 0.02 and abs(bw / bw_pub - 1) <= 0.02})
    g = pd.DataFrame(gate)
    g.to_csv(DER / "whd_gate.csv", index=False, lineterminator="\n", float_format="%.4f")
    # --- QCEW national denominators by cell and year
    q = con.execute(f"""SELECT year, cell, emp, wages FROM '{PANEL}/qcew_cells.parquet'
        WHERE st = 0 AND cell LIKE 'c%'""").df()
    # --- WHD by cell x fiscal year
    whd = con.execute(f"""SELECT fy_end AS year, cell, count(*) AS cases, count(*) FILTER (WHERE viol > 0) AS cases_viol,
        count(*) FILTER (WHERE bw > 0) AS cases_bw, sum(bw) AS bw, sum(ee) AS ee, sum(cmp) AS cmp,
        sum(bw_mw) AS bw_mw, sum(bw_ot) AS bw_ot, sum(bw_farmlabor) AS bw_farmlabor, sum(bw_dbra) AS bw_dbra,
        sum(ee * greatest(date_diff('day', f0, f1), 1) / 365.25) FILTER (WHERE bw > 0 AND f0 IS NOT NULL
            AND f1 IS NOT NULL AND f1 >= f0) AS ee_years,
        sum(bw) FILTER (WHERE bw > 0 AND f0 IS NOT NULL AND f1 IS NOT NULL AND f1 >= f0) AS bw_dated
        FROM w WHERE cell IS NOT NULL AND NOT govt AND fy_end BETWEEN {YEARS[0]} AND {YEARS[1]}
        GROUP BY 1, 2""").df()
    # --- OSHA: private-sector inspections opened in the year, penalties summed per inspection
    con.execute(f"""CREATE TEMP TABLE pen AS SELECT activity_nr, sum(coalesce(try_cast(current_penalty AS DOUBLE), 0)) AS pen,
        sum(coalesce(try_cast(initial_penalty AS DOUBLE), 0)) AS pen0, count(*) AS n_viol
        FROM read_csv('{DOL}/osha_violations.csv.gz', header=true, all_varchar=true) GROUP BY 1""")
    osha = con.execute(f"""SELECT year(try_cast(substr(open_date, 1, 10) AS DATE)) AS year,
        {naics_cell_sql('i.naics_code')} AS cell, count(*) AS insp,
        count(*) FILTER (WHERE insp_type IN ('H', 'I', 'K')) AS insp_programmed,
        count(*) FILTER (WHERE pen.n_viol > 0) AS insp_viol, sum(coalesce(pen.pen, 0)) AS penalties,
        sum(coalesce(pen.pen0, 0)) AS penalties_initial
        FROM read_csv('{DOL}/osha_inspections.csv.gz', header=true, all_varchar=true) i
        LEFT JOIN pen USING (activity_nr)
        WHERE owner_type = 'A' GROUP BY 1, 2""").df()
    osha = osha[osha.cell.notna() & osha.year.between(*YEARS)]
    cy = (q[q.year.between(*YEARS)].merge(whd, on=["year", "cell"], how="left")
          .merge(osha, on=["year", "cell"], how="left").fillna(0))
    cy["bw_per_case_bw"] = cy.bw / cy.cases_bw.where(cy.cases_bw > 0)
    cy["bw_per_employee"] = cy.bw / cy.ee.where(cy.ee > 0)
    cy["bw_per_employee_year"] = cy.bw_dated / cy.ee_years.where(cy.ee_years > 0)
    cy["qcew_pay_per_job"] = cy.wages / cy.emp
    cy["underpay_share_found"] = cy.bw_per_employee_year / cy.qcew_pay_per_job
    cy["bw_per_covered_worker"] = cy.bw / cy.emp
    cy["bw_share_payroll"] = cy.bw / cy.wages
    cy["cmp_per_covered_worker"] = cy.cmp / cy.emp
    cy["pen_per_insp"] = cy.penalties / cy.insp.where(cy.insp > 0)
    cy["pen_per_covered_worker"] = cy.penalties / cy.emp
    cy["pen_share_payroll"] = cy.penalties / cy.wages
    cy["whd_cases_per_10k_workers"] = cy.cases / cy.emp * 1e4
    cy["osha_insp_per_10k_workers"] = cy.insp / cy.emp * 1e4
    cy["label"] = cy.cell.map(lambda c: CELLS[c]["label"])
    cy.sort_values(["cell", "year"]).to_csv(DER / "enforcement_by_cell_year.csv", index=False,
                                            lineterminator="\n", float_format="%.6g")
    cols = ["cases", "bw", "ee", "cmp", "insp", "penalties", "bw_per_case_bw", "bw_per_employee",
            "bw_per_employee_year", "underpay_share_found", "bw_per_covered_worker", "bw_share_payroll",
            "pen_per_insp", "pen_per_covered_worker", "pen_share_payroll", "whd_cases_per_10k_workers",
            "osha_insp_per_10k_workers"]
    agg = cy.groupby(["cell", "label"])[cols].agg(["mean", "min", "max"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    agg = agg.reset_index()
    agg["focus"] = agg.cell.isin(FOCUS)
    agg["osha_programmed_share"] = agg.cell.map(cy.groupby("cell").insp_programmed.sum() / cy.groupby("cell").insp.sum())
    agg = agg.sort_values("bw_share_payroll_mean", ascending=False)
    agg.to_csv(DER / "enforcement_by_cell.csv", index=False, lineterminator="\n", float_format="%.6g")
    pd.set_option("display.width", 250)
    print(g[g.basis == "fy_end"][["fiscal_year", "cases_ratio", "bw_ratio", "employees_ratio", "match_within_2pct"]]
          .to_string(index=False, float_format="%.3f"))
    print(g[g.basis == "fy_load"][["fiscal_year", "cases_ratio", "bw_ratio", "employees_ratio", "match_within_2pct"]]
          .to_string(index=False, float_format="%.3f"))
    show = ["cell", "cases_mean", "bw_mean", "bw_per_employee_mean", "bw_per_employee_year_mean",
            "underpay_share_found_mean", "bw_per_covered_worker_mean", "bw_share_payroll_mean",
            "pen_per_insp_mean", "pen_per_covered_worker_mean", "pen_share_payroll_mean", "osha_programmed_share"]
    print(agg[show].to_string(index=False, float_format="%.5g"))


if __name__ == "__main__":
    main()

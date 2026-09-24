#!/usr/bin/env python3
"""Test A synthesis: the cost edge from paying the group's workers off the books, by industry.

Per dollar of off-books wages, an employer avoids:
  E1  the employer's legally required costs: Social Security and Medicare, federal and state
      unemployment tax and workers' compensation. Measured for private industry by BLS's Employer
      Costs for Employee Compensation (ECEC, Table 4, June 2026: "legally required benefits" per
      hour over "wages and salaries" per hour). ECEC excludes farms and private households; for
      those the statutory 7.65% (IRS Pub 15, 2024) plus the industry's measured UI contributions per
      dollar of wages (QCEW 2023, national private) is the floor, and workers' compensation is
      unmeasured (0 to 3% of wages, assumed).
  E2  the employee's Social Security and Medicare (7.65%), which the employer keeps only if it can
      pay a correspondingly lower cash wage: 0 (low), half (central), all (high).
  E3  wage-and-hour underpayment: 0 (low); the WHD depth among workers found underpaid, back wages
      per employee-year of the findings period over the industry's average QCEW pay (central);
      twice that (high) unless a survey rate is set in E3_SURVEY_HIGH.

Off-books payroll attributable to the group in a cell and year = slope x the group's ACS wage bill
that year, where the slope is the uncovered-share slope on the imputed-unauthorized share
(uncovered.py): central is the across-state estimate; low and high are the smallest and largest of
its four variants, bounded to [0, 1]. Dollar figures are computed one year at a time; 2024 is the
account's stationary year. Cells whose slope is not identified (agriculture: state UI coverage
rules differ; private households: 22 states) are not priced.

Level check (added after the slope results): the national uncovered share calibrated on the
low-exposure industries (uncovered.py, U_cal), floored at zero, times the cell's ACS wage and
salary workers, as if all of it were the group's, priced at the group's mean pay and the central
edge rate. It disagrees with the slope reading; RESULT.md reports both.

Outputs: derived/edges_by_industry.csv (rates), derived/edges_by_industry_year.csv (dollars by
cell and year), derived/edges_totals.csv (priced cells summed: 2024, and the 2012-2023 mean,
minimum and maximum of the annual totals).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/edges.py
"""
from __future__ import annotations

import csv
import html
import io
import re
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import CELLS  # noqa: E402

DER = HERE / "derived"
PAPERS = HERE / "_cache" / "papers"
ECEC_HTML = PAPERS / "ecec_t04.html"
ECEC_TXT = PAPERS / "ecec_t04_2026q2.txt"
ECEC_URL = "https://www.bls.gov/news.release/ecec.t04.htm"
ACCOUNT_YEAR = 2024
FICA = 0.0765          # IRS Pub 15 (2024): 6.2% + 1.45% each for employer and employee
WC_ASSUMED = (0.0, 0.015, 0.03)   # farms and households only: ECEC does not cover them
E3_SURVEY_HIGH = None  # a survey-based underpayment rate, if one is adopted (None -> 2 x WHD depth)
ECEC_ROW = {"c23": "Construction industry", "c56173": "Administrative and waste services industry",
            "c5617z": "Administrative and waste services industry",
            "c722z": "Accommodation and food services industry", "all": "Private industry workers"}
QCEW_NAICS = {"c111": "111", "c112": "112", "c115": "115", "c814": "814", "c23": "23", "c56173": "561730",
              "c5617z": "5617", "c722z": "722"}
PRICED = ["c23", "c56173", "c5617z", "c722z"]
UNPRICED = {"c111": "slope negative across states: state UI coverage of farms differs (small-farm exemptions)",
            "c112": "slope not distinguishable from zero; farm UI coverage rules differ by state",
            "c115": "farm labour contractors: the ACS codes their workers to crop production, QCEW to 115",
            "c814": "22 states with usable cells; slope not distinguishable from zero"}
BROWSER = ["-H", 'sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
           "-H", "sec-ch-ua-mobile: ?0", "-H", 'sec-ch-ua-platform: "macOS"',
           "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "-H", "Accept-Language: en-US,en;q=0.9", "-H", "Upgrade-Insecure-Requests: 1",
           "-H", "Sec-Fetch-Site: none", "-H", "Sec-Fetch-Mode: navigate", "-H", "Sec-Fetch-User: ?1",
           "-H", "Sec-Fetch-Dest: document"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")


def ecec() -> dict[str, dict]:
    if not ECEC_TXT.exists():
        PAPERS.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["curl", "-sS", "--fail", "--compressed", "-A", UA, *BROWSER, "-o", str(ECEC_HTML), ECEC_URL])
        if r.returncode != 0:
            raise SystemExit(f"[BLOCKED] {ECEC_URL}: curl exit {r.returncode}")
        t = ECEC_HTML.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
        t = re.sub(r"(?i)</tr>", "\n", t)
        t = re.sub(r"(?i)</t[hd]>", " | ", t)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        t = re.sub(r"[ \t\r\f\v]+", " ", t)
        ECEC_TXT.write_text(re.sub(r"\n\s*\n+", "\n", t))
    text = ECEC_TXT.read_text()
    if "[June 2026]" not in text:
        raise SystemExit("[FAILED] ECEC Table 4 is not the June 2026 release this script was written for")
    lines = [l.strip().rstrip("|").strip() for l in text.split("\n")]
    out = {}
    for key, label in ECEC_ROW.items():
        i = lines.index(label)
        nums = []
        for l in lines[i + 1:]:
            if re.fullmatch(r"-?\d+(\.\d+)?", l):
                nums.append(float(l))
                if len(nums) == 16:
                    break
            elif nums:
                break
        if len(nums) != 16 or abs(nums[1] - 100.0) > 1e-9:
            raise SystemExit(f"[FAILED] ECEC row '{label}': {nums}")
        out[key] = {"label": label, "total": nums[0], "wages": nums[2], "lrb": nums[14], "lrb_pct_comp": nums[15],
                    "lrb_over_wages": nums[14] / nums[2]}
    return out


def ui_rates() -> dict[str, float]:
    text = (HERE / "_cache" / "qcew" / "api_US000_2023.csv").read_text()
    rows = {r["industry_code"]: r for r in csv.DictReader(io.StringIO(text)) if r["own_code"] == "5"}
    return {c: int(rows[n]["annual_contributions"]) / int(rows[n]["total_annual_wages"]) for c, n in QCEW_NAICS.items()}


def edge_rates(c: str, e: dict, ui: dict, depth: float) -> tuple[tuple, tuple, tuple, str]:
    if c in ECEC_ROW:
        r = e[c]
        e1 = (r["lrb_over_wages"],) * 3
        basis = f"ECEC June 2026, {r['label']}: legally required ${r['lrb']:.2f} / wages ${r['wages']:.2f} an hour"
    else:
        e1 = tuple(FICA + ui[c] + w for w in WC_ASSUMED)
        basis = f"7.65% FICA + QCEW 2023 UI contributions {ui[c]:.4f} of wages + workers' comp {WC_ASSUMED} assumed"
    e2 = (0.0, FICA / 2, FICA)
    e3 = (0.0, depth, E3_SURVEY_HIGH if E3_SURVEY_HIGH is not None else 2 * depth)
    return e1, e2, e3, basis


def main() -> None:
    e = ecec()
    ui = ui_rates()
    slopes = pd.read_csv(DER / "uncovered_slopes.csv")
    enf = pd.read_csv(DER / "enforcement_by_cell.csv").set_index("cell")
    con = duckdb.connect()
    # the group's private wage and salary pay and workers, each year on its own
    wb = con.execute(f"""SELECT year, cell, sum(ws_wagebill_unauth) AS wb, sum(ws_unauth) AS workers
        FROM '{HERE}/_cache/panel/acs_cells.parquet' WHERE half = 'all' AND year BETWEEN 2012 AND {ACCOUNT_YEAR}
        GROUP BY 1, 2""").df().set_index(["year", "cell"])
    # level check: the national uncovered share calibrated on low-exposure industries, as if all of
    # it were the group's (an upper bound on the group's off-books count under that calibration)
    nat = pd.read_csv(DER / "uncovered_national_by_cell_year.csv").set_index(["year", "cell"])
    rates, yearly = [], []
    for c in PRICED + list(UNPRICED):
        depth = float(enf.loc[c, "underpay_share_found_mean"])
        e1, e2, e3, basis = edge_rates(c, e, ui, depth)
        edge = tuple(a + b + d for a, b, d in zip(e1, e2, e3))
        rate = {"cell": c, "industry": CELLS[c]["label"], "e1_employer_legal_low": e1[0], "e1_central": e1[1],
                "e1_high": e1[2], "e2_employee_fica_captured_low": e2[0], "e2_central": e2[1], "e2_high": e2[2],
                "e3_underpayment_low": e3[0], "e3_central": e3[1], "e3_high": e3[2], "edge_low": edge[0],
                "edge_central": edge[1], "edge_high": edge[2], "ui_contributions_over_wages": ui[c],
                "whd_depth_found_workers": depth, "e1_basis": basis, "priced": c in PRICED,
                "not_priced_reason": UNPRICED.get(c, "")}
        if c in PRICED:
            s = slopes[(slopes["sample"] == c) & (slopes.x == "m_unauth")]
            central = float(s[s.spec.str.endswith(", across states")].coef.iloc[0])
            b = (max(0.0, float(s.coef.min())), min(max(central, 0.0), 1.0), min(1.0, float(s.coef.max())))
            rate.update(slope_low=b[0], slope_central=b[1], slope_high=b[2])
            for year in range(2012, ACCOUNT_YEAR + 1):
                row = {"year": year, "cell": c, "group_wagebill_bn": wb.loc[(year, c), "wb"] / 1e9,
                       "group_workers_m": wb.loc[(year, c), "workers"] / 1e6}
                for k, tag in enumerate(("low", "central", "high")):
                    off = b[k] * wb.loc[(year, c), "wb"]
                    row[f"offbooks_payroll_bn_{tag}"] = off / 1e9
                    row[f"offbooks_workers_m_{tag}"] = b[k] * wb.loc[(year, c), "workers"] / 1e6
                    row[f"edge_bn_{tag}"] = edge[k] * off / 1e9
                    # the edge split: payroll taxes (employer FICA and UI, plus the employee FICA the
                    # employer keeps), workers' compensation premiums (the rest of E1), underpayment (E3)
                    row[f"taxes_bn_{tag}"] = (FICA + ui[c] + e2[k]) * off / 1e9
                    row[f"workers_comp_bn_{tag}"] = max(e1[k] - FICA - ui[c], 0.0) * off / 1e9
                    row[f"underpayment_bn_{tag}"] = e3[k] * off / 1e9
                    row[f"employee_fica_kept_by_worker_bn_{tag}"] = (FICA - e2[k]) * off / 1e9
                lev_workers = max(float(nat.loc[(year, c), "U_cal"]), 0.0) * float(nat.loc[(year, c), "ws"])
                lev_pay = lev_workers * wb.loc[(year, c), "wb"] / wb.loc[(year, c), "workers"]
                row["levelcheck_offbooks_workers_m"] = lev_workers / 1e6
                row["levelcheck_offbooks_payroll_bn"] = lev_pay / 1e9
                row["levelcheck_edge_bn_central"] = edge[1] * lev_pay / 1e9
                yearly.append(row)
        rates.append(rate)
    rates = pd.DataFrame(rates)
    rates.to_csv(DER / "edges_by_industry.csv", index=False, lineterminator="\n", float_format="%.5g")
    yearly = pd.DataFrame(yearly)
    yearly.to_csv(DER / "edges_by_industry_year.csv", index=False, lineterminator="\n", float_format="%.5g")
    cols = [c for c in yearly.columns if c.endswith(("_low", "_central", "_high"))] + [
        "group_wagebill_bn", "group_workers_m", "levelcheck_offbooks_workers_m", "levelcheck_offbooks_payroll_bn"]
    by_year = yearly.groupby("year")[cols].sum()
    summary = pd.DataFrame({"account_year_2024": by_year.loc[ACCOUNT_YEAR],
                            "mean_of_years_2012_2023": by_year.loc[2012:2023].mean(),
                            "min_2012_2023": by_year.loc[2012:2023].min(),
                            "max_2012_2023": by_year.loc[2012:2023].max()})
    summary.to_csv(DER / "edges_totals.csv", lineterminator="\n", float_format="%.5g")
    pd.set_option("display.width", 250)
    print(rates[["cell", "edge_low", "edge_central", "edge_high", "slope_low", "slope_central", "slope_high",
                 "ui_contributions_over_wages", "whd_depth_found_workers"]].to_string(index=False, float_format="%.4g"))
    print(yearly[yearly.year == ACCOUNT_YEAR][["cell", "group_wagebill_bn", "offbooks_payroll_bn_central",
                                               "offbooks_workers_m_central", "edge_bn_low", "edge_bn_central",
                                               "edge_bn_high"]].to_string(index=False, float_format="%.4g"))
    print(summary.round(3).to_string())
    print("ECEC legally required over wages:", {k: round(v["lrb_over_wages"], 4) for k, v in e.items()})


if __name__ == "__main__":
    main()

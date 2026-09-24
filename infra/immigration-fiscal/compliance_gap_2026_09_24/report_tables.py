#!/usr/bin/env python3
"""Print the RESULT.md tables from the lane's derived files, so every number in them can be
re-derived: python3 report_tables.py > /tmp/tables.md, then compare with RESULT.md.

Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/compliance_gap_2026_09_24/report_tables.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import CELLS, FOCUS  # noqa: E402

DER = HERE / "derived"
PRICED = ["c23", "c56173", "c5617z", "c722z"]


def cs(c, s, d=3):
    return f"{c:+.{d}f} ({s:.{d}f})"


def table(head, rows):
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join("---" for _ in head) + "|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")
    print()


def enforcement():
    e = pd.read_csv(DER / "enforcement_by_cell.csv").set_index("cell")
    print("### Enforcement, mean of annual values 2010-2024\n")
    rows = []
    for c in FOCUS + ["c54", "c52"]:
        r = e.loc[c]
        rows.append([CELLS[c]["label"], f"{r.cases_mean:,.0f}", f"{r.bw_mean / 1e6:.1f}", f"{r.bw_per_case_bw_mean:,.0f}",
                     f"{r.bw_per_employee_mean:,.0f}", f"{100 * r.underpay_share_found_mean:.1f}",
                     f"{r.bw_per_covered_worker_mean:.2f}", f"{100 * r.bw_share_payroll_mean:.4f}",
                     f"{r.cmp_mean / 1e6:.2f}", f"{r.insp_mean:,.0f}", f"{r.pen_per_insp_mean:,.0f}",
                     f"{r.pen_per_covered_worker_mean:.2f}", f"{100 * r.pen_share_payroll_mean:.4f}",
                     f"{100 * r.osha_programmed_share:.0f}"])
    table(["Industry", "WHD cases/yr", "back wages $m/yr", "per case $", "per employee found $",
           "per employee-year, % of covered pay", "per covered worker $", "% of covered payroll", "WHD penalties $m/yr",
           "OSHA inspections/yr", "OSHA penalty per inspection $", "per covered worker $", "% of covered payroll",
           "programmed %"], rows)


def edges():
    r = pd.read_csv(DER / "edges_by_industry.csv").set_index("cell")
    print("### Edge per dollar of off-books wages\n")
    rows = []
    for c in r.index:
        x = r.loc[c]
        sl = f"{x.slope_low:.2f} / {x.slope_central:.2f} / {x.slope_high:.2f}" if x.priced else "not identified"
        rows.append([x.industry, f"{100 * x.e1_central:.1f}" + ("" if c in PRICED else f" ({100 * x.e1_employer_legal_low:.1f}-{100 * x.e1_high:.1f})"),
                     f"{100 * x.ui_contributions_over_wages:.2f}", "0 / 3.8 / 7.65",
                     f"0 / {100 * x.e3_central:.1f} / {100 * x.e3_high:.1f}",
                     f"{100 * x.edge_low:.1f} / {100 * x.edge_central:.1f} / {100 * x.edge_high:.1f}", sl])
    table(["Industry", "E1 employer legally required, % of wages", "of which state UI (QCEW 2023) %",
           "E2 employee FICA kept, % (low/central/high)", "E3 underpayment, %", "edge, % of off-books wages",
           "off-books share of the group's wage workers (slope)"], rows)
    y = pd.read_csv(DER / "edges_by_industry_year.csv")
    y24 = y[y.year == 2024].set_index("cell")
    print("### Edge in dollars, 2024 (account year)\n")
    rows = []
    for c in PRICED:
        x = y24.loc[c]
        rows.append([CELLS[c]["label"], f"{x.group_wagebill_bn:.1f}", f"{x.group_workers_m:.2f}",
                     f"{x.offbooks_payroll_bn_low:.1f} / {x.offbooks_payroll_bn_central:.1f} / {x.offbooks_payroll_bn_high:.1f}",
                     f"{x.offbooks_workers_m_low:.2f} / {x.offbooks_workers_m_central:.2f} / {x.offbooks_workers_m_high:.2f}",
                     f"{x.edge_bn_low:.2f} / {x.edge_bn_central:.2f} / {x.edge_bn_high:.2f}"])
    table(["Industry", "group's wage bill $bn", "group's wage workers m", "off-books pay $bn (low/central/high)",
           "off-books workers m", "edge $bn"], rows)
    t = pd.read_csv(DER / "edges_totals.csv", index_col=0)
    print("### Totals, four priced industries\n")
    rows = []
    for k, lab in (("offbooks_payroll_bn", "off-books pay, $bn"), ("offbooks_workers_m", "off-books workers, m"),
                   ("edge_bn", "edge, $bn"), ("taxes_bn", "of which payroll taxes, $bn"),
                   ("workers_comp_bn", "of which workers' comp (and FUTA), $bn"),
                   ("underpayment_bn", "of which underpayment, $bn"),
                   ("employee_fica_kept_by_worker_bn", "employee FICA kept by the worker, $bn")):
        rows.append([lab] + [f"{t.loc[f'{k}_{lv}', col]:.2f}" for col in ("account_year_2024", "mean_of_years_2012_2023")
                             for lv in ("low", "central", "high")])
    table(["Item", "2024 low", "2024 central", "2024 high", "2012-23 mean low", "central", "high"], rows)
    print("### Level check: national uncovered share calibrated on low-exposure industries, all of it the group's\n")
    rows = [[lab, f"{t.loc[k, 'account_year_2024']:.2f}", f"{t.loc[k, 'mean_of_years_2012_2023']:.2f}",
             f"{t.loc[k, 'min_2012_2023']:.2f}", f"{t.loc[k, 'max_2012_2023']:.2f}"]
            for k, lab in (("levelcheck_offbooks_workers_m", "off-books workers, m"),
                           ("levelcheck_offbooks_payroll_bn", "off-books pay, $bn"),
                           ("levelcheck_edge_bn_central", "edge at the central rate, $bn"))]
    table(["Item", "2024", "2012-23 mean", "2012-23 min", "2012-23 max"], rows)


def uncovered():
    u = pd.read_csv(DER / "uncovered_summary_by_cell.csv")
    print("### Uncovered share by industry, 2012-2023 (each year, then averaged)\n")
    rows = []
    for _, r in u.iterrows():
        tag = "focus" if r.focus else ("low exposure" if r.low_exposure else "")
        rows.append([r.label, tag, f"{r.acs_ws_m:.2f}", f"{r.qcew_emp_m:.2f}", f"{r.U_raw:.3f} ({r.U_raw_min:.3f} to {r.U_raw_max:.3f})",
                     f"{r.U_cal:.3f}", f"{r.U_inc:.3f}", f"{100 * r.share_mexnc:.1f}", f"{100 * r.share_unauth:.1f}"])
    table(["Industry", "set", "ACS private wage and salary workers m", "QCEW jobs m", "U raw (min to max over years)",
           "U calibrated", "U with incorporated self-employed", "Mexico-born noncitizen %", "imputed unauthorized %"], rows)
    s = pd.read_csv(DER / "uncovered_slopes.csv")
    print("### Slopes of the uncovered share on the group's share\n")
    rows = [[r.spec, r["sample"], r.x, cs(r.coef, r.se), int(r.n), int(r.clusters) if pd.notna(r.clusters) else ""]
            for _, r in s.iterrows()]
    table(["Specification", "sample", "regressor", "slope (SE)", "n", "clusters"], rows)


def everify():
    s = pd.read_csv(DER / "everify_summary.csv")
    print("### P1 E-Verify, post average (event time 0 to +5) and pre-trend test\n")
    rows = [[r.variant, r.cells, r.outcome, cs(r.post_avg, r.post_se, 4), f"{r.pre_joint_p:.4f}", int(r.n), int(r.clusters)]
            for _, r in s.iterrows()]
    table(["Variant", "cells", "outcome", "post average (SE)", "pre-trend p", "n", "states"], rows)
    c = pd.read_csv(DER / "everify_event_study.csv")
    m = c[c.variant == "main"]
    order = ["et_m4", "et_m3", "et_m2", "et_p0", "et_p1", "et_p2", "et_p3", "et_p4", "et_p5"]
    print("### P1 event-time coefficients, main variant (reference −1)\n")
    outs = [("focus vs low-exposure cells", o) for o in ("U", "ln_estabs", "ln_emp", "ln_wkwage", "m_mexnc", "se_mexnc_per_ws")]
    outs += [("detail series vs low-exposure cells", o) for o in ("ln_estabs", "ln_emp", "ln_wkwage")]
    rows = []
    for cells, o in outs:
        d = m[(m.cells == cells) & (m.outcome == o)].set_index("term")
        rows.append([("detail: " if cells.startswith("detail") else "") + o] +
                    [cs(d.loc[t, "Estimate"], d.loc[t, "Std. Error"], 3) if t in d.index else "" for t in order])
    table(["Outcome"] + ["−4", "−3", "−2", "0", "+1", "+2", "+3", "+4", "+5"], rows)
    t = pd.read_csv(DER / "everify_trend_break_exploratory.csv")
    print("### Exploratory trend break (not pre-registered)\n")
    rows = [[r.cells, r.outcome, cs(r.pre_trend, r.pre_trend_se, 4), cs(r.level_shift, r.level_shift_se, 4),
             cs(r.slope_change, r.slope_change_se, 4), int(r.n)] for _, r in t.iterrows()]
    table(["Cells", "outcome", "pre-trend per year", "level shift at 0", "slope change after 0", "n"], rows)


def panel():
    p = pd.read_csv(DER / "panel_c.csv")
    print("### P2 panel associations (every specification)\n")
    ymap = {"d_ln_estabs": "estabs", "dy_estabs": "estabs", "d_ln_emp": "emp", "dy_emp": "emp",
            "d_ln_wkwage": "wkwage", "dy_wkwage": "wkwage"}
    p["out"] = p.y.map(ymap)
    p["note2"] = p.note.fillna("").str.startswith("mechanical")
    keys = []
    for _, r in p.iterrows():
        k = (r.design, r["sample"], r.x if r.x != "x_focus" else f"x_focus [{r.note.split('regressor ')[-1]}]")
        if k not in keys:
            keys.append(k)
    rows = []
    for k in keys:
        design, sample, x = k
        sub = p[(p.design == design) & (p["sample"] == sample) & ((p.x == x) | (p.x == "x_focus") & (x.startswith("x_focus")) &
                                                               p.note.fillna("").str.endswith(x.split("[")[-1].rstrip("]")))]
        vals = {}
        for _, r in sub.iterrows():
            star = "‡" if r.note2 else ""
            vals[r.out] = cs(r.coef, r.se) + star
        rows.append([design, sample, x, vals.get("estabs", ""), vals.get("emp", ""), vals.get("wkwage", ""),
                     int(sub.n.iloc[0]) if len(sub) else ""])
    table(["Design", "sample", "regressor", "ln establishments", "ln employment", "ln weekly wage", "n"], rows)
    print("‡ mechanical: U contains QCEW employment.\n")


def composition():
    c = pd.read_csv(DER / "composition_check.csv")
    print("### Wage association against composition\n")
    rows = [[r.industry, f"{100 * r.m_unauth:.1f}", f"{r.pay_ratio:.2f}",
             "" if pd.isna(r.b_offbooks) else f"{r.b_offbooks:.2f}", f"{r.composition_slope:+.3f}",
             "" if pd.isna(r.get("ld_coef")) else cs(r.ld_coef, r.ld_se, 2),
             "" if pd.isna(r.get("ld_states")) else int(r.ld_states)] for _, r in c.iterrows()]
    table(["Industry", "group share %", "group pay / others' pay", "off-books share used", "composition-only slope",
           "long difference net of low-exposure cells (SE)", "states"], rows)


def self_employed():
    a = pd.read_parquet(HERE / "_cache" / "panel" / "acs_cells.parquet")
    a = a[(a.half == "all") & a.cell.isin(FOCUS) & a.year.between(2012, 2024)]
    g = a.groupby(["year", "cell"])[["se_uninc", "se_uninc_unauth", "se_uninc_mexnc", "se_inc", "ws", "ws_unauth"]].sum()
    g["share"] = g.se_uninc_unauth / g.se_uninc
    q = pd.read_parquet(HERE / "_cache" / "panel" / "qcew_cells.parquet")
    q = q[(q.st == 0) & (q.year == 2024)].set_index("cell")
    print("### The group's own businesses: unincorporated self-employed, ACS\n")
    rows = []
    for c in FOCUS:
        y24 = g.loc[(2024, c)]
        mean_share = g.xs(c, level="cell").loc[2012:2023, "share"].mean()
        rows.append([CELLS[c]["label"], f"{y24.se_uninc / 1e3:,.0f}", f"{y24.se_uninc_unauth / 1e3:,.0f}",
                     f"{100 * y24.share:.1f}", f"{100 * mean_share:.1f}", f"{y24.se_uninc_mexnc / 1e3:,.0f}",
                     f"{y24.se_inc / 1e3:,.0f}", f"{q.loc[c, 'estabs'] / 1e3:,.0f}"])
    table(["Industry", "unincorporated self-employed 2024, thousand", "of whom imputed unauthorized, thousand",
           "share 2024 %", "share 2012-23 mean %", "Mexico-born noncitizen, thousand", "incorporated self-employed, thousand",
           "QCEW establishments 2024, thousand"], rows)


def winners():
    w = pd.read_csv(DER / "winners_losers_rows.csv")
    print("### Winners and losers, 2024, $bn a year\n")
    rows = []
    four = "construction (NAICS 23), landscaping (NAICS 561730), janitorial (NAICS 5617) and restaurants (NAICS 722)"
    for _, r in w.iterrows():
        val = "unpriced" if r.basis == "unpriced" else f"{r.bn_low:.2f} / {r.bn_central:.2f} / {r.bn_high:.2f}"
        per = "" if pd.isna(r.per_person_usd) else f"{r.per_person_usd:,.0f}"
        who = r.group.replace(f" in {four} (mostly the group: a within-group item)", "").replace(
            f" in {four} (within-group item)", "").replace(f" in {four}", "").replace(f"of {four}", "of the four industries")
        rows.append([who, r.channel.split(":")[0], r.direction, val, per, r.basis, r.relation_to_account])
    table(["Who", "channel", "sign", "$bn low / central / high", "$ per person", "basis", "relation to the account"], rows)


if __name__ == "__main__":
    for f in (enforcement, edges, uncovered, self_employed, everify, panel, composition, winners):
        f()

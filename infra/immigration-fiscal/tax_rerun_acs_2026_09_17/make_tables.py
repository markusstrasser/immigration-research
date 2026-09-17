#!/usr/bin/env python3
"""Assemble the deliverables from the two survey arms.

Reads the per-survey outputs written by cps_tax.py and acs_tax.py and writes
derived/taxcalc_gaps.csv, derived/anchor_ratios.csv, derived/audit.json and
derived/tables.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"

PAIRS = [("mexico_born", "Mexico-born"),
         ("usborn_mexican_selfid", "US-born Mexican self-ID"),
         ("all_native", "All natives")]
# CPS-only ledger categories, reported for completeness
CPS_ONLY = [("mexican_second_gen", "Mexican second generation"),
            ("mexican_third_plus_selfid", "Mexican third-plus self-ID"),
            ("third_plus_nh_white", "Third-plus NH white (ledger reference)")]


def fmt(v, nd=0):
    if pd.isna(v):
        return "n/a"
    return f"{v:,.{nd}f}"


def main():
    cg = pd.read_csv(OUT / "cps_tax_gaps.csv")
    ag = pd.read_csv(OUT / "acs_tax_gaps.csv")
    cc = pd.read_csv(OUT / "cps_tax_cells.csv")
    ac = pd.read_csv(OUT / "acs_tax_cells.csv")
    anchor = pd.read_csv(OUT / "cps_anchor.csv")
    acs_tot = pd.read_csv(OUT / "acs_totals.csv")
    cps_audit = json.loads((OUT / "cps_audit.json").read_text())
    acs_audit = json.loads((OUT / "acs_audit.json").read_text())

    gaps = pd.concat([cg, ag], ignore_index=True)
    gaps.to_csv(OUT / "taxcalc_gaps.csv", index=False)
    anchor.to_csv(OUT / "anchor_ratios.csv", index=False)

    def gap(df, group, var):
        r = df[df.group.eq(group) & df.variable.eq(var)]
        if len(r) != 1:
            return (np.nan, np.nan, np.nan)
        return (float(r.common_age_gap_per_person.iloc[0]),
                float(r.common_age_gap_se.iloc[0]),
                float(r.age_matched_gap_bn.iloc[0]))

    lines = ["# Tax-Calculator gaps, ACS versus CPS", "",
             f"taxcalc {cps_audit['taxcalc_version']}, tax year "
             f"{cps_audit['tax_year']}, current law.", ""]

    # ---- headline comparison ---------------------------------------------
    lines += ["## Common-age gap per standardized person versus native non-Hispanic whites", "",
              "Reference age shares are the white group's own full-weight shares in that",
              "survey. `iitax` is federal income tax after refundable credits; a negative",
              "gap means the group pays that much less per standardized person.", "",
              "| Group | Measure | ACS $ (SE) | CPS same mapping $ (SE) | ACS/CPS | CPS full mapping $ (SE) |",
              "|---|---|---|---|---|---|"]
    ratios = {}
    for key, label in PAIRS:
        for var, name in [("iitax", "federal income tax"), ("payroll", "payroll tax")]:
            a = gap(ag, key, f"{var}_acsmap")
            c = gap(cg, key, f"{var}_acsmap")
            f = gap(cg, key, f"{var}_full")
            r = a[0] / c[0] if c[0] else np.nan
            ratios[(key, var)] = dict(acs=a[0], cps_acsmap=c[0], cps_full=f[0], ratio=r)
            lines.append(f"| {label} | {name} | {fmt(a[0])} ({fmt(a[1])}) | "
                         f"{fmt(c[0])} ({fmt(c[1])}) | {r:.2f} | {fmt(f[0])} ({fmt(f[1])}) |")
    lines.append("")

    lines += ["CPS-only categories, full CPS income mapping:", "",
              "| Group | Federal income tax $ (SE) | Payroll tax $ (SE) |", "|---|---|---|"]
    for key, label in CPS_ONLY:
        i = gap(cg, key, "iitax_full")
        p = gap(cg, key, "payroll_full")
        lines.append(f"| {label} | {fmt(i[0])} ({fmt(i[1])}) | {fmt(p[0])} ({fmt(p[1])}) |")
    lines.append("")

    # ---- ACS/CPS difference, treating the two surveys as independent -----
    diff_rows = []
    for key, label in PAIRS:
        for var, name in [("iitax", "federal income tax"), ("payroll", "payroll tax")]:
            a = gap(ag, key, f"{var}_acsmap")
            c = gap(cg, key, f"{var}_acsmap")
            se = float(np.hypot(a[1], c[1]))
            dd = a[0] - c[0]
            diff_rows.append(dict(group=key, variable=var, acs=a[0], acs_se=a[1],
                                  cps=c[0], cps_se=c[1], difference=dd,
                                  difference_se=se, z=dd / se if se else np.nan,
                                  ci_overlap=bool(abs(dd) < 1.96 * se)))
    pd.DataFrame(diff_rows).to_csv(OUT / "acs_cps_tax_difference.csv", index=False)
    lines += ["## ACS minus CPS, same income mapping, surveys treated as independent", "",
              "| Group | Measure | Difference $ | SE | z | 95% intervals overlap |",
              "|---|---|---|---|---|---|"]
    for r in diff_rows:
        lines.append(f"| {r['group']} | {r['variable']} | {fmt(r['difference'])} | "
                     f"{fmt(r['difference_se'])} | {r['z']:.2f} | "
                     f"{'yes' if r['ci_overlap'] else 'NO'} |")
    lines.append("")

    # ---- CPS: taxcalc against the Census tax model, same gap estimator ----
    lines += ["## CPS gap computed from the Census tax model instead of taxcalc", "",
              "| Group | taxcalc iitax $ | Census FEDTAX_AC as recorded $ | Census FEDTAX_AC reallocated $ | taxcalc payroll $ | Census FICA $ |",
              "|---|---|---|---|---|---|"]
    for key, label in PAIRS + CPS_ONLY:
        lines.append(f"| {label} | {fmt(gap(cg, key, 'iitax_full')[0])} | "
                     f"{fmt(gap(cg, key, 'FEDTAX_AC')[0])} | "
                     f"{fmt(gap(cg, key, 'FEDTAX_AC_alloc')[0])} | "
                     f"{fmt(gap(cg, key, 'payroll_full')[0])} | "
                     f"{fmt(gap(cg, key, 'FICA')[0])} |")
    lines.append("")

    # ---- age-matched aggregate -------------------------------------------
    lines += ["## Age-matched aggregate gap, $bn", "",
              "| Group | Measure | ACS $bn | CPS same mapping $bn | CPS full mapping $bn |",
              "|---|---|---|---|---|"]
    for key, label in PAIRS:
        for var, name in [("iitax", "federal income tax"), ("payroll", "payroll tax")]:
            a = gap(ag, key, f"{var}_acsmap")
            c = gap(cg, key, f"{var}_acsmap")
            f = gap(cg, key, f"{var}_full")
            lines.append(f"| {label} | {name} | {fmt(a[2], 1)} | {fmt(c[2], 1)} | {fmt(f[2], 1)} |")
    lines.append("")

    # ---- anchor ----------------------------------------------------------
    lines += ["## Anchor on CPS: taxcalc against the Census tax model", "",
              "Full-weight totals over the civilian household population, $bn.", "",
              "| Group | taxcalc iitax | Census FEDTAX_AC | ratio | taxcalc payroll | Census FICA | ratio |",
              "|---|---|---|---|---|---|---|"]
    for _, r in anchor.iterrows():
        lines.append(f"| {r.group} | {fmt(r.iitax_full_bn, 1)} | {fmt(r.FEDTAX_AC_bn, 1)} | "
                     f"{r.ratio_iitax:.3f} | {fmt(r.payroll_full_bn, 1)} | "
                     f"{fmt(r.FICA_bn, 1)} | {r.ratio_payroll:.3f} |")
    lines.append("")

    if "eitc_taxcalc_bn" in anchor.columns:
        lines += ["### Refundable credits, taxcalc against the Census model, $bn", "",
                  "| Group | EITC taxcalc | EITC Census | ACTC taxcalc | ACTC Census |",
                  "|---|---|---|---|---|"]
        for _, r in anchor.iterrows():
            lines.append(f"| {r.group} | {fmt(r.eitc_taxcalc_bn, 1)} | {fmt(r.eitc_census_bn, 1)} | "
                         f"{fmt(r.actc_taxcalc_bn, 1)} | {fmt(r.actc_census_bn, 1)} |")
        lines.append("")

    # ---- per-person by age band ------------------------------------------
    lines += ["## Per-person amounts by age band", "",
              "| Survey | Group | Band | Population | iitax $ | payroll $ | Census FEDTAX_AC $ | Census FICA $ |",
              "|---|---|---|---|---|---|---|---|"]
    for df, survey in [(cc, "CPS"), (ac, "ACS")]:
        icol = "mean_iitax_full" if survey == "CPS" else "mean_iitax_acsmap"
        pcol = "mean_payroll_full" if survey == "CPS" else "mean_payroll_acsmap"
        for key, _ in PAIRS + (CPS_ONLY if survey == "CPS" else []):
            sub = df[df.group.eq(key)]
            for _, r in sub.iterrows():
                lines.append(
                    f"| {survey} | {key} | {r.band} | {fmt(r.population)} | "
                    f"{fmt(r[icol])} | {fmt(r[pcol])} | "
                    f"{fmt(r.get('mean_FEDTAX_AC', np.nan))} | {fmt(r.get('mean_FICA', np.nan))} |")
    lines.append("")

    lines += ["## ACS national totals, $bn", "",
              "| Group | Population | iitax $bn | payroll $bn |", "|---|---|---|---|"]
    for _, r in acs_tot.iterrows():
        lines.append(f"| {r.group} | {fmt(r.population)} | {fmt(r.iitax_bn, 1)} | {fmt(r.payroll_bn, 1)} |")
    lines.append("")

    (OUT / "tables.md").write_text("\n".join(lines))

    audit = {
        "lane": "tax_rerun_acs_2026_09_17",
        "acs_cps_difference": diff_rows,
        "question": ("one federal tax calculator on tax units built from both "
                     "surveys; ACS versus CPS common-age federal income-tax and "
                     "payroll-tax gaps per standardized person"),
        "taxcalc_version": cps_audit["taxcalc_version"],
        "tax_year": cps_audit["tax_year"],
        "policy": cps_audit["policy"],
        "headline_ratios": {f"{k[0]}::{k[1]}": v for k, v in ratios.items()},
        "cps": cps_audit,
        "acs": acs_audit,
    }
    (OUT / "audit.json").write_text(json.dumps(audit, indent=2, default=float))
    print(f"[done] wrote {OUT/'tables.md'}, taxcalc_gaps.csv, anchor_ratios.csv, audit.json")
    for k, v in ratios.items():
        print(f"  {k}: ACS {v['acs']:,.0f} CPS(acsmap) {v['cps_acsmap']:,.0f} "
              f"ratio {v['ratio']:.3f} CPS(full) {v['cps_full']:,.0f}")


if __name__ == "__main__":
    main()

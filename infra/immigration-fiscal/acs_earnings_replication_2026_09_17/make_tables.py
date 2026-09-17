#!/usr/bin/env python3
"""Assemble the ACS-vs-CPS side-by-side markdown tables from derived/*.csv."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"

PAIRS = [
    # (label, ACS group, CPS group, CPS reference)
    ("Mexico-born", "mexico_born", "mexico_born", "native_nh_white"),
    ("US-born Mexican self-ID", "usborn_mexican_selfid", "usborn_mexican_selfid", "native_nh_white"),
    ("All natives", "all_native", "all_native", "native_nh_white"),
]
VARPAIR = [("WAGP", "WSAL_VAL", "wages"), ("PINCP", "PTOTVAL", "total personal income")]


def ci(e, s):
    return f"{e:,.0f} [{e - 1.96 * s:,.0f}, {e + 1.96 * s:,.0f}]"


def main():
    a = pd.read_csv(D / "acs_gaps.csv")
    c = pd.read_csv(D / "cps_gaps.csv")
    out = []

    out.append("| Domain | Group | Measure | ACS gap $/std person [95%] | CPS gap $/std person [95%] | ACS/CPS |")
    out.append("|---|---|---|---|---|---|")
    ratios = {}
    for domain in ["national", "CA", "TX"]:
        for label, ag, cg, cref in PAIRS:
            for av, cv, vlabel in VARPAIR:
                ar = a[(a.domain == domain) & (a.group == ag) & (a.variable == av)]
                cr = c[(c.domain == domain) & (c.group == cg) & (c.variable == cv)
                       & (c.reference == cref)]
                if ar.empty or cr.empty:
                    continue
                ae, ase = float(ar.common_age_gap_per_person.iloc[0]), float(ar.common_age_gap_se.iloc[0])
                ce, cse = float(cr.common_age_gap_per_person.iloc[0]), float(cr.common_age_gap_se.iloc[0])
                r = ae / ce if ce else float("nan")
                ratios[(domain, label, vlabel)] = r
                out.append(f"| {domain} | {label} | {vlabel} | {ci(ae, ase)} | {ci(ce, cse)} | {r:.2f} |")

    out.append("")
    out.append("### Age-matched aggregate gap, $bn (group minus age-matched native NH white)")
    out.append("")
    out.append("| Domain | Group | Measure | ACS $bn (SE) | CPS $bn (SE) |")
    out.append("|---|---|---|---|---|")
    for domain in ["national", "CA", "TX"]:
        for label, ag, cg, cref in PAIRS:
            for av, cv, vlabel in VARPAIR:
                ar = a[(a.domain == domain) & (a.group == ag) & (a.variable == av)]
                cr = c[(c.domain == domain) & (c.group == cg) & (c.variable == cv)
                       & (c.reference == cref)]
                if ar.empty or cr.empty:
                    continue
                out.append(f"| {domain} | {label} | {vlabel} | "
                           f"{float(ar.age_matched_gap_bn.iloc[0]):,.1f} ({float(ar.age_matched_gap_bn_se.iloc[0]):,.1f}) | "
                           f"{float(cr.age_matched_gap_bn.iloc[0]):,.1f} ({float(cr.age_matched_gap_bn_se.iloc[0]):,.1f}) |")

    out.append("")
    out.append("### CPS-only generation split (ACS cannot reproduce: no parent birthplace)")
    out.append("")
    out.append("| Group | Reference | Measure | Gap $/std person [95%] |")
    out.append("|---|---|---|---|")
    for cg in ["mexican_second_gen", "mexican_third_plus_selfid"]:
        for cref in ["native_nh_white", "third_plus_nh_white"]:
            for _, cv, vlabel in VARPAIR:
                cr = c[(c.domain == "national") & (c.group == cg) & (c.variable == cv)
                       & (c.reference == cref)]
                if cr.empty:
                    continue
                e, s = float(cr.common_age_gap_per_person.iloc[0]), float(cr.common_age_gap_se.iloc[0])
                out.append(f"| {cg} | {cref} | {vlabel} | {ci(e, s)} |")

    text = "\n".join(out)
    (D / "tables.md").write_text(text)
    print(text)

    # gate numbers
    ac = pd.read_csv(D / "acs_cells.csv")
    cc = pd.read_csv(D / "cps_cells.csv")
    g2 = {}
    for grp in ["mexico_born", "usborn_mexican_selfid", "native_nh_white", "all_native"]:
        av = float(ac[(ac.domain == "national") & (ac.group == grp) & (ac.band == "all")].population.iloc[0])
        cv = float(cc[(cc.domain == "national") & (cc.group == grp) & (cc.band == "all")].population.iloc[0])
        g2[grp] = {"acs": av, "cps": cv, "acs_over_cps": av / cv}
    print("\nGATE2 " + json.dumps(g2, indent=1))
    audit = json.loads((D / "audit.json").read_text())
    print("\nGATE3 " + json.dumps(audit["gate3_household_population"], indent=1))
    print("\nACS_SHA " + audit["acs_zip_sha256"])
    print("ACS_ROWS " + str(audit["household_person_records"]))


if __name__ == "__main__":
    main()

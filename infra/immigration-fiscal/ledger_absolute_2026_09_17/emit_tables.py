#!/usr/bin/env python3
"""Print the markdown tables the RESULT reports, straight from `derived/`.

A formatting helper only: it computes nothing and reads no microdata.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DER = HERE / "derived"
UNION = "mexican_observed_total"
GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid", UNION,
          "third_plus_nh_white", "all_native"]
SHORT = {"mexico_born": "Mexico-born", "mexican_second_gen": "2nd gen",
         "mexican_third_plus_selfid": "3rd+ self-ID", UNION: "union",
         "third_plus_nh_white": "3rd+ NH white", "all_native": "all natives"}


def main() -> None:
    audit = json.loads((DER / "audit.json").read_text())
    items = pd.read_csv(DER / "items_by_group.csv")
    water = pd.read_csv(DER / "waterfall.csv")
    arms = pd.read_csv(DER / "arms_matrix.csv")
    curve = pd.read_csv(DER / "marginality_curve.csv")
    centrals = audit["central_arms"]

    print("### Waterfall, central arms, $bn\n")
    order = water[water.group == UNION].sort_values("step")
    head = ["step", "item"] + [SHORT[g] for g in GROUPS[:4]] + ["union se", "flag"]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for _, row in order.iterrows():
        cells = [str(int(row.step)), f"{row['item']}"]
        for g in GROUPS[:4]:
            v = water[(water.group == g) & (water.step == row.step)].cumulative_bn.iloc[0]
            cells.append(f"{v:+,.1f}")
        cells.append(f"{row.se_bn:,.1f}")
        cells.append(row.flag)
        print("| " + " | ".join(cells) + " |")

    print("\n### Per standardized person, union and the white reference\n")
    ends = water.sort_values("step").groupby("group").tail(1).set_index("group")
    print("| group | complete absolute $bn | per person $ |")
    print("|---|---|---|")
    for g in GROUPS:
        print(f"| {SHORT[g]} | {ends.loc[g, 'cumulative_bn']:+,.1f} | "
              f"{ends.loc[g, 'cumulative_per_person']:+,.0f} |")

    print("\n### Items, union\n")
    print("| item | arm | central | union $bn | per person $ | se $bn | "
          "common-age gap vs white $/person | source |")
    print("|---|---|---|---|---|---|---|---|")
    for _, r in items[items.group == UNION].iterrows():
        star = "yes" if centrals.get(r["item"]) == r["arm"] else ""
        print(f"| {r['item']} | {r['arm']} | {star} | {r.total_bn:+,.2f} | "
              f"{r.per_person:+,.0f} | {r.se_bn:,.2f} | "
              f"{r.common_age_gap_per_person_vs_white:+,.0f} | {r.source} |")

    print("\n### Arms matrix, union absolute $bn\n")
    print(f"{len(arms)} combinations, from {arms.union_absolute_bn.min():+,.1f}bn to "
          f"{arms.union_absolute_bn.max():+,.1f}bn.\n")
    lo = arms.loc[arms.union_absolute_bn.idxmin()]
    hi = arms.loc[arms.union_absolute_bn.idxmax()]
    print("| corner | F | E | C | R | union $bn |")
    print("|---|---|---|---|---|---|")
    for label, row in [("most negative", lo), ("least negative", hi)]:
        print(f"| {label} | {row.F_arm} | {row.E_arm} | {row.C_arm} | {row.R_arm} | "
              f"{row.union_absolute_bn:+,.1f} |")

    print("\n### Marginality curve\n")
    print("| m | union absolute $bn | per person $ |")
    print("|---|---|---|")
    for _, r in curve[curve.m.isin([0.0, 0.25, 0.5, 0.75, 1.0])].iterrows():
        print(f"| {r.m:.2f} | {r.union_absolute_bn:+,.1f} | {r.union_per_person:+,.0f} |")
    m_star = curve.break_even_m_star.iloc[0]
    print(f"\nBreak-even m\\* = {m_star:.4f}" if pd.notna(m_star) else "\nNo finite m\\*")

    print("\n### Dropped for want of a verified parameter\n")
    for item in audit["items_dropped"]:
        print(f"- **{item['item']}** — {item['reason']}")
    if not audit["items_dropped"]:
        print("- none")

    print("\n### What remains unpriced\n")
    for line in audit["unpriced"]:
        print(f"- {line}")


if __name__ == "__main__":
    main()

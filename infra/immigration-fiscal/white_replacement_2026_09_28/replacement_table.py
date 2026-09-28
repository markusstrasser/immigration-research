"""The replacement delta, cost of the union minus cost of a 40.9M NH white slice, collected from the lane's outputs.

Reads derived/rekey_summary.csv, accrual_beside.csv, spill_summary.csv and victim_cost_white_summary.csv (run
rekey_white.py, accrual_white.py, spillovers_white.py and victim_cost_white.py first). Positive = the union costs other
residents more than the white slice would. Output: derived/replacement_table.csv.
"""
import csv
from pathlib import Path

import pandas as pd

DER = Path(__file__).resolve().parent / "derived"
SLICES = {"A1_third_plus_nh_white": "A1 third-plus, own ages", "A2_us_born_nh_white": "A2 US-born, own ages",
          "A3_third_plus_nh_white_at_union_ages": "A3 third-plus rates, union ages",
          "A4_third_plus_nh_white_stationary": "A4 third-plus rates, stationary"}
UNION_VICTIMS = {"lower bound": 23.4535, "central": 28.9229}   # [DATA: crime_victim_cost_2026_09_23/derived/arms.csv]


def main():
    s = pd.read_csv(DER / "rekey_summary.csv")
    acc = pd.read_csv(DER / "accrual_beside.csv")
    sp = pd.read_csv(DER / "spill_summary.csv")
    vc = pd.read_csv(DER / "victim_cost_white_summary.csv")
    rows = []

    def add(block, item, slice_, end, value, low=None, high=None, note=""):
        rows.append({"block": block, "item": item, "slice": slice_, "end": end, "delta_bn": f"{value:.4f}",
                     "low_bn": "" if low is None else f"{low:.4f}", "high_bn": "" if high is None else f"{high:.4f}",
                     "per_member": f"{value * 1e9 / 40_896_574.152351856:.0f}", "note": note})

    for lab, name in SLICES.items():
        for end in ("low", "high"):
            r = s[(s.group == lab) & (s.end == end)].iloc[0]
            u = s[(s.group == "mexican_origin_rough") & (s.end == end)].iloc[0]
            add("A cash", "white slice's cost to others", name, end, r.cost)
            add("A cash", "union's cost to others (rough)", name, end, u.cost)
            add("A cash", "delta, like for like (central rules)", name, end, r.delta_like_for_like_bn)
            add("A cash", "delta against the engine's union", name, end, r.delta_vs_engine_union_bn)
            add("A cash", "delta, top tail spread by CPS income tax", name, end, r.delta_like_for_like_top_tail_proportional_bn)
            add("A cash", "delta, capital-side taxes respond", name, end, r.delta_like_for_like_capital_taxes_respond_bn)
            add("A cash", "delta, both arms", name, end, r.delta_like_for_like_both_arms_bn)
            add("A cash", "old-age net (Social Security, Medicare, their taxes), white slice", name, end, r.old_age_net)
            add("A cash", "old-age net, union (rough)", name, end, u.old_age_net)
            for scen in ("payable", "scheduled"):
                a = acc[(acc.group == lab) & (acc.scenario == scen) & (acc.end == end)].iloc[0]
                add("A accrual", f"delta, like for like, {scen} benefits", name, end, a.delta_like_for_like_accrual_bn)
                add("A accrual", f"white slice's cost on accrual, {scen}", name, end, a.cost_accrual_bn)
                arms = r.delta_like_for_like_both_arms_bn - r.delta_like_for_like_bn
                add("A accrual", f"delta, {scen} benefits, both arms", name, end, a.delta_like_for_like_accrual_bn + arms)
    for spec, item in (("CRY joint: scale by education + college gradient net of CES (sigma 2, CRY weights) [central]",
                        "scale and schooling, CRY joint (central)"),
                       ("CRY place effect by education, conditional on college share [central]", "scale alone (central)"),
                       ("CRY college gradient net of CES, sigma 2, CRY-implied weights [central]", "schooling alone (central)"),
                       ("Ciccone-Peri joint, Table 4 col 2: scale + average schooling", "Ciccone-Peri joint, col 2"),
                       ("Ciccone-Peri joint, Table 4 col 1: scale + average schooling", "Ciccone-Peri joint, col 1"),
                       ("Moretti earnings-weighted, col 6 (2SLS land grant, 1990), 2024 others weights", "Moretti col 6, 2024 weights"),
                       ("Moretti earnings-weighted, col 3 (2SLS age structure, 1980-90), 1980-1990 weights", "Moretti col 3, 1980-90 weights"),
                       ("Iranzo-Peri basic, Table 8 col 1", "Iranzo-Peri Table 8 col 1"),
                       ("Iranzo-Peri sector-demand control, Table 9 col 4", "Iranzo-Peri Table 9 col 4")):
        r = sp[(sp.geography == "CZ 1990") & (sp.spec == spec)].iloc[0]
        add("B spillovers", item, "US-born NH white, own settlement", "both", r.delta_cost_bn, r.delta_low_bn, r.delta_high_bn,
            f"gains: union {r.gain_bn_union:.1f}, white {r.gain_bn_white:.1f}")
    v = vc.set_index(["scope", "victims"])
    for key, union_key, label in (("non-white victims (lower bound)", "lower bound", "all co-ethnic victims in-group"),
                                  ("outside a random slice (central)", "central", "each group's central")):
        for scope in ("40.9M slice", "40.9M slice at union ages"):
            w = float(v.loc[(scope, key), "full_bn"])
            add("E victims", f"{label}: union {UNION_VICTIMS[union_key]:.1f} less white", scope, "both",
                UNION_VICTIMS[union_key] - w, note=f"white slice {w:.2f}")
    with open(DER / "replacement_table.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    t = pd.DataFrame(rows)
    pd.set_option("display.width", 220)
    pd.set_option("display.max_colwidth", 70)
    print(t[t.slice.str.startswith("A1") | ~t.block.str.startswith("A")].to_string(index=False))


if __name__ == "__main__":
    main()

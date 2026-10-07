#!/usr/bin/env python3
"""Checks on propagate.py's outputs, recomputed independently where possible.

Run from the repository root after propagate.py:
    uv run --no-project python3 infra/immigration-fiscal/identity_loss_propagation_2026_09_27/verify.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import propagate as P  # noqa: E402

OUT = HERE / "derived"
FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'✓' if ok else '✗'} {name}{f' — {detail}' if detail else ''}")
    if not ok:
        FAILS.append(name)


def main() -> int:
    lo = P.losses()
    p3 = P.pop_p3()
    S = P.schedules(p3, lo)
    arms = pd.read_csv(OUT / "arms.csv")
    pop = pd.read_csv(OUT / "population_arms.csv")
    lin_d = pd.read_csv(OUT / "lineage_arms.csv")
    audit = json.loads((OUT / "audit.json").read_text())

    print("[schedules]")
    check("brief's G4 ~0.78 (one step, Mexican)", abs(P.rate(S["b_one_step"], p3, 4) - 0.78) < 0.005,
          f"{P.rate(S['b_one_step'], p3, 4):.4f}")
    check("brief's G5 ~0.69 (compounding)", abs(P.rate(S["c_compound"], p3, 5) - 0.69) < 0.005,
          f"{P.rate(S['c_compound'], p3, 5):.4f}")
    check("(d) step is the 9.0% Hispanic loss", abs(S["d_compound_hisp"]["step"] - 0.0901374) < 1e-6)
    for key, s in S.items():
        for rho in P.RHOS:
            k = np.arange(400)
            brute = float(((1 - rho) * rho ** k * np.array([P.rate(s, p3, 4 + i) for i in k])).sum())
            if abs(brute - P.p_eff(s, p3, rho)) > 1e-12:
                check(f"p_eff closed form {key} rho {rho}", False)
    check("p_eff closed form equals the truncated sum, every arm and rho", True)

    print("[population]")
    m = pd.read_csv(P.POP_DIR / "derived/arm3_multiplier.csv")
    q = dict(zip(m["quantity"], m["children"]))
    A = q["A: self-identified Mexican, two US-area-born parents"]
    s3 = q["A and B: 3rd-generation identifiers"] / A
    s4 = q["A not B: 4th-plus identifiers (no Mexico-born grandparent)"] / A
    b = pd.read_csv(P.POP_DIR / "derived/arm3_correction_bounds.csv")
    g3 = float(b.iloc[0].self_id_third_plus)
    g12 = float(b.iloc[0].corrected_union - b.iloc[0].corrected_third_plus)
    worst = 0.0
    for _, r in pop.iterrows():
        mine = g12 + g3 * s3 / p3 + g3 * s4 / r.p_eff_fourth_plus
        worst = max(worst, abs(mine / 1e6 - r.union_M))
    check("union recomputed from the multiplier table (CSV rounding only)", worst < 5e-6,
          f"max |diff| {worst * 1e6:.2f} persons")
    a = pop[pop.arm == "a_current"].iloc[0]
    check("arm (a) is the published 42.78M / 45.0M",
          round(a.union_M, 2) == 42.78 and round(a.union_pes_M, 1) == 45.0,
          f"{a.union_M:.3f} / {a.union_pes_M:.3f}")
    check("union rises monotonically as p_eff falls",
          bool((pop.sort_values("p_eff_fourth_plus").union_M.diff().dropna() <= 0).all()))
    # Generation split: 1 - p3 of the corrected third-plus is lost at the G3 rate in every arm,
    # the rest of the added persons later; the aggregate adds them at (1 - C3) and 1 of the
    # self-ID gap.
    split_central = pd.read_csv(P.POP_DIR / "derived/arm5_generation_split.csv")
    split_central = split_central[split_central.c3_source.str.endswith(P.CENTRAL)]
    sp = split_central.iloc[0]
    c3_split, gap3 = float(sp.c3), float(sp.selfid_third_plus_gap_per_person)
    f5 = pd.read_csv(P.POP_DIR / "derived/arm5_fiscal_implication.csv")
    before = float(f5.aggregate_gap_bn_before.iloc[0]) * 1e9
    pop_before = float(f5.population_before.iloc[0])
    worst_n = worst_bn = worst_pp = 0.0
    for _, r in pop.iterrows():
        g3r = min(r.added_M, (1 - p3) * r.corrected_third_plus_M)
        worst_n = max(worst_n, abs(g3r - r.g3_rate_attriters_M),
                      abs(r.added_M - g3r - r.later_loss_attriters_M))
        agg = (before + 1e6 * (g3r * gap3 * (1 - c3_split) + (r.added_M - g3r) * gap3)) / 1e9
        worst_bn = max(worst_bn, abs(agg - r.aggregate_gap_bn_after_split))
        pp = r.aggregate_gap_bn_after_split * 1e9 / (pop_before + r.added_M * 1e6)
        worst_pp = max(worst_pp, abs(pp - r.gap_per_person_after_split))
    check("split counts: G3-rate = (1 - p3) x corrected third-plus, later = the rest",
          worst_n < 2e-7, f"max |diff| {worst_n * 1e6:.2f} persons")
    check("split aggregate recomputed from counts and the self-ID gap (CSV rounding only)",
          worst_bn < 0.011, f"max |diff| ${worst_bn:.3f}bn")
    check("split per person = aggregate / population after, every arm (CSV rounding only)",
          worst_pp < 0.25, f"max |diff| ${worst_pp:.3f}")
    pub = split_central[split_central.population_assumption.str.startswith("4th-plus identifies at the measured")]
    check("arm (a) under the split is the population lane's published central split row",
          len(pub) == 1 and a.gap_per_person_after_split == pub.gap_per_person_after.iloc[0]
          and a.aggregate_gap_bn_after_split == pub.aggregate_gap_bn_after.iloc[0],
          f"{a.gap_per_person_after_split:,.1f} / {a.aggregate_gap_bn_after_split:.2f}bn"
          f" (C3 {c3_split}, {sp.c3_source})")

    print("[lineage]")
    lin = P.Lin()
    stored = pd.read_csv(P.LIN_DIR / "derived/sensitivities.csv").set_index("sensitivity")
    for name, (srow, over, rate) in P.LIN_ARMS.items():
        o = P.lin_over(lin, over)
        if "mix_from_gen" in o:
            continue
        up, upL = lin.gap(o, rate, fn=P.L.lineage)
        cp, cpL = lin.gap(o, rate)
        cf, _ = lin.gap({**o, "attr_for": lin.attr_for(S["a_current"], o.get("attr"))}, rate)
        same = all(np.array_equal(upL[g][1], cpL[g][1]) for g in upL) and up == cp == cf
        check(f"copy == upstream lineage(), bitwise: {name}", same)
        if srow is not None:
            check(f"reproduces stored {name}",
                  abs(up - float(stored.loc[srow, "gap_lineage_fiscal"])) < 1e-6)
    c0 = lin.gap({}, 0.0, fn=P.L.lineage)[0]
    c3 = lin.gap({}, 0.03, fn=P.L.lineage)[0]
    check(f"centrals are propagate.LIN_CENTRAL, {P.LIN_CENTRAL[0]:,.0f} / {P.LIN_CENTRAL[1]:,.0f} since the ledger's "
          "item T (−1,288,162 / −513,398 after audit §E; brief: −1,297,150 / −514,635)",
          round(c0) == P.LIN_CENTRAL[0] and round(c3) == P.LIN_CENTRAL[1], f"{c0:,.6f} / {c3:,.6f}")
    poison = {k: float("nan") for k in lin.attr}
    check("central ignores the attrition inputs (NaN-poisoned attr, same gap)",
          lin.gap({"attr": poison}, 0.0, fn=P.L.lineage)[0] == c0)

    # Generation split: later losses keep the whole gap, so no schedule moves row 2a.
    split_rows = lin_d[lin_d.lineage_row.str.startswith("2a G4+ attrition-corrected")]
    check("generation split: no schedule moves row 2a (later losses close nothing)",
          bool((split_rows.delta.abs() < 1e-6).all()), f"max |delta| ${split_rows.delta.abs().max():.2e}")
    # Years convention: a flat schedule scales the G4+ blend linearly,
    # new - central = (share_b/share_a)(2a - central).
    years = {"convergence": "attrition_mixed", "attr": lin.attr_years}
    g2a = lin.gap(years, 0.0, fn=P.L.lineage)[0]
    share_a = lin.attr_years["attriter_share"]
    share_b = 1 - P.rate(S["b_one_step"], lin.attr_years["fourth_plus_identification_rate"], 4)
    pred = c0 + (share_b / share_a) * (g2a - c0)
    got = float(lin_d[(lin_d.arm == "b_one_step")
                      & (lin_d.lineage_row == "2a years convention (sensitivity), 0%")].new_gap.iloc[0])
    check("years convention: (b) on 2a equals the linear rescaling of the attrition effect",
          abs(pred - got) < 1e-6, f"{got:,.2f} vs {pred:,.2f}")

    print("[arms.csv]")
    check("delta = new − old on every row", bool(np.allclose(arms.new - arms.old, arms.delta, atol=1e-9)))
    check("arm (a) changes nothing", bool((arms[arms.arm == "a_current"].delta.abs() < 1e-9).all()))
    moved = arms[(arms.consumer == "lineage_cost") & (arms.delta.abs() > 1e-6)].metric.unique()
    check("only mixed-profile lineage rows move",
          all("mixed profile" in x or "2a" in x for x in moved), "; ".join(sorted(moved)))
    check("sponsored-parent lane pins convergence 'selfid'", audit["checks"]["sponsored_lane_pins_selfid"])

    print("[upstream untouched]")
    lin_audit = json.loads((P.LIN_DIR / "derived/audit.json").read_text())["inputs_sha256"]
    bad = [k for k, v in lin_audit.items()
           if (P.FISCAL / k).exists() and hashlib.sha256((P.FISCAL / k).read_bytes()).hexdigest() != v]
    check("lineage lane's recorded input hashes still match", not bad, ", ".join(bad))

    print(f"\n{'PASS' if not FAILS else 'FAIL: ' + ', '.join(FAILS)}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())

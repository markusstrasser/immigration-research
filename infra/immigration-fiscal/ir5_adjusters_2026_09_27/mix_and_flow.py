#!/usr/bin/env python3
"""Arms C and the FY2024 Mexican IR-5 flow at the adjuster/new-arrival mix.

Reads derived/adjuster_values.csv (adjusters.py), derived/nis_ir5_channels.csv and
derived/nis_ir5_adjuster_types.csv (nis_adjusters.py), the tail lane's per_admission.csv and
flow_valuation.csv (read-only), and the cohort lane's consular IR-5 visa counts (read-only).

  arm C for a type    = arm B minus the counterfactual with departures (adjusters.DEPART; C_low has
                        the most departures, C_high the fewest)
  adjuster average    = type values weighted by the NIS-2003 Mexican adjuster type shares
                        ("nis_all"), or by the shares among adjusters who never entered without
                        documents ("nis_no_ewi")
  FY2024 flow         = 63,050 admissions; new arrivals = Mexico-born IR-5 visas issued abroad in
                        FY2024 (11,760, State RVO Table VIII), the rest adjusters
  break-even floor    = the public-care floor (per year, for a senior outside Medicare and federal
                        Medicaid) at which an adjuster costs the same as a new arrival; every value
                        is linear in it, so a line through the four floor variants gives it exactly
  age mix             = NIS-2003 Mexican age distribution by channel, with a common odds shift so the
                        flow's share aged 55+ equals the tail lane's FY2024 central (38%) or upper
                        (48%) bound; ages map to the tail lane's grid (<50 -> 45, 50-54 -> 50,
                        55-59 -> 55, 60-64 -> 60, 65+ -> 65)

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/mix_and_flow.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TAIL = ROOT / "infra/immigration-fiscal/late_arrival_tail_2026_09_27"
COHORT = ROOT / "infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27"
OUT = HERE / "derived"
sys.path.insert(0, str(HERE))
from adjusters import DEPART, TYPES  # noqa: E402

GRID = (45, 50, 55, 60, 65)
TYPE_NAMES = tuple(TYPES)


def channel_mixes() -> dict[str, dict[str, dict[int, float]]]:
    s = pd.read_csv(OUT / "nis_ir5_channels.csv")
    s = s[s.group == "mexico"]
    base = {}
    for ch in ("new", "adjust", "both"):
        v = s[s.channel == ch].set_index("stat").estimate
        m = {45: v.age_0_44 + v.age_45_49, 50: v.age_50_54, 55: v.age_55_59, 60: v.age_60_64,
             65: v.age_65_74 + v.age_75_plus}
        tot = sum(m.values())
        assert abs(tot - 1) < 1e-5, (ch, tot)  # the CSV rounds each share to 6 decimals
        base[ch] = {a: x / tot for a, x in m.items()}
    return base


def rescale(mix: dict[int, float], k: float) -> dict[int, float]:
    old = mix[55] + mix[60] + mix[65]
    o = old / (1 - old)
    s = k * o / (1 + k * o)
    young = mix[45] + mix[50]
    return {45: (1 - s) * mix[45] / young, 50: (1 - s) * mix[50] / young,
            55: s * mix[55] / old, 60: s * mix[60] / old, 65: s * mix[65] / old}


def solve_k(new: dict, adj: dict, share_new: float, target: float) -> float:
    lo, hi = 1e-6, 1e6
    for _ in range(200):
        k = np.sqrt(lo * hi)
        s = share_new * sum(rescale(new, k)[a] for a in (55, 60, 65)) + \
            (1 - share_new) * sum(rescale(adj, k)[a] for a in (55, 60, 65))
        lo, hi = (k, hi) if s < target else (lo, k)
    return float(np.sqrt(lo * hi))


def main() -> None:
    vals = pd.read_csv(OUT / "adjuster_values.csv")
    types = pd.read_csv(OUT / "nis_ir5_adjuster_types.csv")
    tshare = {f"nis_{smp}": dict(zip(g.type, g.weighted_share)) for smp, g in types.groupby("sample")}
    tail_pa = pd.read_csv(TAIL / "derived/per_admission.csv")
    tail_flow = pd.read_csv(TAIL / "derived/flow_valuation.csv")
    tail_nis = pd.read_csv(TAIL / "derived/ir5_age_nis2003.csv").set_index("group").loc["mexico"]
    visas = pd.read_csv(COHORT / "reads/ir5_mexico_iv_issued.csv").set_index("fy").ir5_iv_issued_mexico
    flow = pd.read_csv(TAIL / "derived/ir5_flow.csv")
    admissions = float(flow[(flow.country == "mexico") & (flow.fy == 2024)].ir5_parents.iloc[0])
    share_new = float(visas.loc[2024]) / admissions

    # gate: this lane's NIS "both" age mix equals the tail lane's NIS-2003 Mexican mix
    base = channel_mixes()
    tail_base = {45: tail_nis.age_0_44 + tail_nis.age_45_49, 50: tail_nis.age_50_54,
                 55: tail_nis.age_55_59, 60: tail_nis.age_60_64, 65: tail_nis.age_65_74 + tail_nis.age_75_120}
    for a in GRID:
        assert abs(base["both"][a] - tail_base[a]) < 2e-3, (a, base["both"][a], tail_base[a])

    rows = []
    key_cols = ["variant", "counterfactual", "case", "real_rate", "adjust_age"]
    # profiles without a variant (residence variants exist for the long types only) take central
    full = []
    for (variant, cf), g in vals.groupby(["variant", "counterfactual"]):
        for prof in ("new_arrival",) + TYPE_NAMES:
            have = vals[(vals.profile == prof) & (vals.variant == variant) & (vals.counterfactual == cf)]
            if len(have):
                full.append(have)
            else:
                full.append(vals[(vals.profile == prof) & (vals.variant == "central")
                                 & (vals.counterfactual == cf)].assign(variant=variant))
    vals = pd.concat(full, ignore_index=True)
    v = vals.set_index(["profile"] + key_cols)
    # arm values per type, and adjuster averages
    arm_rows = []
    for (variant, cf, case, rate, age), _ in vals[vals.profile == "T0_recent"].groupby(key_cols):
        new_b = v.loc[("new_arrival", variant, cf, case, rate, age), "npv_factual_armB"]
        per = {}
        for t in TYPE_NAMES:
            r = v.loc[(t, variant, cf, case, rate, age)]
            per[t] = {"A": r.npv_armA, "B": r.npv_factual_armB}
            for lvl in DEPART:
                per[t][f"C_{lvl}"] = r.npv_factual_armB - r[f"npv_cf_depart_{lvl}"]
        for t, d in per.items():
            for arm, x in d.items():
                arm_rows.append({"profile": t, "arm": arm, "variant": variant, "counterfactual": cf,
                                 "case": case, "real_rate": rate, "adjust_age": age, "npv": round(x, 1)})
        for smp, sh in tshare.items():
            for arm in per["T0_recent"]:
                x = sum(sh[t] * per[t][arm] for t in TYPE_NAMES)
                arm_rows.append({"profile": f"adjuster_{smp}", "arm": arm, "variant": variant,
                                 "counterfactual": cf, "case": case, "real_rate": rate, "adjust_age": age,
                                 "npv": round(x, 1)})
        arm_rows.append({"profile": "new_arrival", "arm": "B", "variant": variant, "counterfactual": cf,
                         "case": case, "real_rate": rate, "adjust_age": age, "npv": round(new_b, 1)})
    arms = pd.DataFrame(arm_rows).drop_duplicates()
    arms.to_csv(OUT / "arms_by_age.csv", index=False, lineterminator="\n")

    # FY2024 flow
    tail_ref = tail_flow[(tail_flow.mix == "fy2024_central") & (tail_flow.flow == "fy2024")
                         & (tail_flow.arm == "statutory") & (tail_flow.case == "central")
                         & (tail_flow.survival == "group_specific") & (tail_flow.real_rate == 0.03)]
    assert len(tail_ref) == 1
    a_idx = arms.set_index(["profile", "arm", "variant", "counterfactual", "case", "real_rate", "adjust_age"]).npv
    for target_name, target in (("fy2024_central", 0.38), ("fy2024_upper", 0.48)):
        k = solve_k(base["new"], base["adjust"], share_new, target)
        mix_new, mix_adj = rescale(base["new"], k), rescale(base["adjust"], k)
        mix_all = rescale(base["both"], solve_k(base["both"], base["both"], 1.0, target))
        for (variant, cf, case, rate), _ in arms[arms.profile == "adjuster_nis_all"].groupby(
                ["variant", "counterfactual", "case", "real_rate"]):
            nb = sum(mix_new[a] * a_idx[("new_arrival", "B", variant, cf, case, rate, a)] for a in GRID)
            nb_all = sum(mix_all[a] * a_idx[("new_arrival", "B", variant, cf, case, rate, a)] for a in GRID)
            # adjusters valued as new arrivals at their own ages: separates the age mix from the clocks
            na_adj = sum(mix_adj[a] * a_idx[("new_arrival", "B", variant, cf, case, rate, a)] for a in GRID)
            for smp in tshare:
                for arm in ("A", "B", "C_central", "C_low", "C_high"):
                    adj = sum(mix_adj[a] * a_idx[(f"adjuster_{smp}", arm, variant, cf, case, rate, a)]
                              for a in GRID)
                    mean = share_new * nb + (1 - share_new) * adj
                    rows.append({"age_mix": target_name, "type_mix": smp, "arm": arm, "variant": variant,
                                 "counterfactual": cf, "case": case, "real_rate": rate,
                                 "admissions": admissions, "share_new_arrivals": round(share_new, 6),
                                 "mean_new_arrival": round(nb, 1), "mean_adjuster": round(adj, 1),
                                 "mean_adjuster_as_new_arrival": round(na_adj, 1),
                                 "mean_per_admission": round(mean, 1),
                                 "all_as_new_arrivals": round(nb_all, 1),
                                 "flow_bn": round(mean * admissions / 1e9, 3),
                                 "flow_adjusters_as_new_bn": round(
                                     (share_new * nb + (1 - share_new) * na_adj) * admissions / 1e9, 3),
                                 "flow_all_as_new_bn": round(nb_all * admissions / 1e9, 3)})
    fl = pd.DataFrame(rows)
    # gate: all admissions valued as new arrivals with the tail lane's statutory arm (PTC off)
    # reproduces its FY2024 flow at the central mix
    chk = fl[(fl.age_mix == "fy2024_central") & (fl.variant == "ptc_off") & (fl.counterfactual == "central")
             & (fl.case == "central") & (fl.real_rate == 0.03)].flow_all_as_new_bn.iloc[0]
    assert abs(chk - float(tail_ref.flow_npv_bn.iloc[0])) < 0.01, (chk, tail_ref.flow_npv_bn.iloc[0])
    fl.to_csv(OUT / "flow_fy2024.csv", index=False, lineterminator="\n")

    # break-even: the stay probability p* (common to all adjusters) at which an adjuster costs the same
    # as a new arrival of the same age: p* = (B - N) / (B - A); below p* the adjuster costs more
    be = []
    for (variant, case, rate, age), _ in arms[arms.counterfactual == "central"].groupby(
            ["variant", "case", "real_rate", "adjust_age"]):
        n = a_idx[("new_arrival", "B", variant, "central", case, rate, age)]
        for prof in ("adjuster_nis_all", "adjuster_nis_no_ewi") + TYPE_NAMES:
            A = a_idx[(prof, "A", variant, "central", case, rate, age)]
            B = a_idx[(prof, "B", variant, "central", case, rate, age)]
            c = a_idx[(prof, "C_central", variant, "central", case, rate, age)]
            be.append({"variant": variant, "case": case, "real_rate": rate, "adjust_age": age,
                       "profile": prof, "new_arrival": round(n, 1), "armA": round(A, 1), "armB": round(B, 1),
                       "armC_central": round(c, 1),
                       "p_stay_breakeven": round((B - n) / (B - A), 4) if B != A else np.nan,
                       "p_stay_central_implied": round((B - c) / (B - A), 4) if B != A else np.nan})
    pd.DataFrame(be).to_csv(OUT / "breakeven.csv", index=False, lineterminator="\n")

    # break-even care floor, per case (each case keeps its Medicare weight and price level)
    prov = json.loads((OUT / "adjuster_provenance.json").read_text())
    floor_of = {"central": prov["bar_price_per_year"]} | prov["bar_price_variants"]
    fb = []
    for (case, rate, age), _ in arms[(arms.counterfactual == "central") & (arms.variant == "central")].groupby(
            ["case", "real_rate", "adjust_age"]):
        f = np.array([floor_of[vn][case] for vn in floor_of])
        n = np.array([a_idx[("new_arrival", "B", vn, "central", case, rate, age)] for vn in floor_of])
        for prof in ("adjuster_nis_all", "adjuster_nis_no_ewi"):
            for arm in ("A", "C_low", "C_central", "C_high"):
                c = np.array([a_idx[(prof, arm, vn, "central", case, rate, age)] for vn in floor_of])
                gap = c - n  # positive: the adjuster costs less than a new arrival
                slope, icpt = np.polyfit(f, gap, 1)
                resid = float(np.abs(gap - (slope * f + icpt)).max())
                assert resid < 1.0, (case, rate, age, prof, arm, resid)  # linear up to CSV rounding
                fb.append({"case": case, "real_rate": rate, "adjust_age": age, "profile": prof, "arm": arm,
                           "floor_central": floor_of["central"][case],
                           "gap_at_central_floor": round(float(slope * floor_of["central"][case] + icpt), 1),
                           "gap_per_1000_of_floor": round(float(slope) * 1000, 1),
                           "floor_breakeven": round(float(-icpt / slope), 1) if slope > 0 else np.nan,
                           "fit_max_residual": round(resid, 3)})
    pd.DataFrame(fb).to_csv(OUT / "breakeven_floor.csv", index=False, lineterminator="\n")
    show = fl[(fl.variant == "central") & (fl.counterfactual == "central") & (fl.case == "central")
              & fl.real_rate.isin([0.0, 0.03]) & (fl.age_mix == "fy2024_central")]
    print(show[["type_mix", "arm", "real_rate", "mean_new_arrival", "mean_adjuster", "mean_per_admission",
                "all_as_new_arrivals", "flow_bn", "flow_all_as_new_bn"]].to_string())


if __name__ == "__main__":
    main()

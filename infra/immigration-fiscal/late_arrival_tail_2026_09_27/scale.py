#!/usr/bin/env python3
"""Flow valuation: per-admission remaining-lifetime values x the annual Mexican IR-5 flow.

This values a year's admissions over their remaining lives. It is not an annual-account line:
the complete annual account already contains every Mexico-born resident at every age.

Age mixes at admission (IR-5 age by country is unpublished; see RESULT.md section 1):
  nis2003       NIS-2003 Mexican parents of US citizens (weighted; 75% aged 55+).
  fy2024_central 38% aged 55+ (NIS ratio applied to the FY2024 profile bound), NIS proportions
                within 55+ and within <55.
  fy2024_upper  48% aged 55+ (the FY2024 profile bound: every Mexican LPR aged 55+ an IR-5).
Arrival ages map to the nearest computed arrival age: <50 -> 45, 50-54 -> 50, 55-59 -> 55,
60-64 -> 60, 65+ -> 65 (65+ arrivals are valued at 65, which overstates their remaining years).

Run: uv run --no-project python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/scale.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"


def mixes() -> dict[str, dict[int, float]]:
    nis = pd.read_csv(OUT / "ir5_age_nis2003.csv").set_index("group").loc["mexico"]
    lt50 = nis.age_0_44 + nis.age_45_49
    base = {45: lt50, 50: nis.age_50_54, 55: nis.age_55_59, 60: nis.age_60_64,
            65: nis.age_65_74 + nis.age_75_120}
    assert abs(sum(base.values()) - 1) < 1e-3, sum(base.values())
    out = {"nis2003": base}
    old = base[55] + base[60] + base[65]
    for name, s55 in (("fy2024_central", 0.38), ("fy2024_upper", 0.48)):
        young = base[45] + base[50]
        out[name] = {45: (1 - s55) * base[45] / young, 50: (1 - s55) * base[50] / young,
                     55: s55 * base[55] / old, 60: s55 * base[60] / old, 65: s55 * base[65] / old}
    return out


def main() -> None:
    pa = pd.read_csv(OUT / "per_admission.csv")
    flow = pd.read_csv(OUT / "ir5_flow.csv")
    mx = flow[flow.country == "mexico"].set_index("fy").ir5_parents
    flows = {"fy2024": float(mx.loc[2024]), "mean_fy2015_2024": float(mx.loc[2015:2024].mean())}
    rows = []
    for mix_name, mix in mixes().items():
        for (arm, case, surv, rate), g in pa.groupby(["arm", "case", "survival", "real_rate"]):
            v = g.set_index("arrival_age")
            per_parent = sum(w * v.npv_parent[a] for a, w in mix.items())
            per_gap = sum(w * v.gap_vs_white[a] for a, w in mix.items())
            for fname, n in flows.items():
                rows.append({"mix": mix_name, "flow": fname, "admissions": n, "arm": arm,
                             "case": case, "survival": surv, "real_rate": rate,
                             "mean_npv_per_parent": round(per_parent, 1),
                             "mean_gap_vs_white_per_parent": round(per_gap, 1),
                             "flow_npv_bn": round(per_parent * n / 1e9, 3),
                             "flow_gap_vs_white_bn": round(per_gap * n / 1e9, 3)})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "flow_valuation.csv", index=False, lineterminator="\n")
    show = df[(df.survival == "group_specific") & (df.real_rate.isin([0.0, 0.03]))
              & (df.case.isin(["central", "n/a"]))]
    print(show.to_string())


if __name__ == "__main__":
    main()

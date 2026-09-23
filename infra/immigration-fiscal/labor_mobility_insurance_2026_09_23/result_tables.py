"""Print the RESULT.md specification tables as markdown from the lane's derived CSVs.

Every computed specification is in derived/*.csv; these tables show the ones RESULT.md quotes, in
the same wording, so the text can be checked against the files:
  1 population responses (ck_population.csv), men with high school or less, Mexican-share control
  2 smoothing (ck_smoothing.csv), all panels and specs, difference and continuous gradient
  3 pricing per episode (insurance_episode.csv)
  4 mobility by nativity (mobility_summary.csv)
  5 Borjas Table 8 reproduction and the 2024 restatement (borjas_*.csv)
"""
from pathlib import Path

import pandas as pd

DERIVED = Path(__file__).resolve().parent / "derived"


def cs(b, se):
    return f"{b:.3f} ({se:.3f})"


def population():
    p = pd.read_csv(DERIVED / "ck_population.csv")
    p = p[(p["sex"] == "men") & (p["educ"] == "hs_or_less")]
    main = p[p["spec"].str.endswith("mexshare_control")]
    print("| Period | Spec | Natives | Mexico-born | US-born Mexican-origin | Other natives | First-stage F (Mexico-born) |")
    print("|---|---|---:|---:|---:|---:|---:|")
    for (per, spec), d in main.groupby(["period", "spec"], sort=False):
        d = d.set_index("group")
        f = d.loc["mex_fb", "first_stage_F"] if "first_stage_F" in d and pd.notna(d.loc["mex_fb", "first_stage_F"]) else None
        print(f"| {per} | {spec.replace('_mexshare_control', '')} | " + " | ".join(
            cs(d.loc[g, "coef"], d.loc[g, "se"]) for g in ("natives", "mex_fb", "mex_nb", "oth_nb"))
            + f" | {'' if f is None else f'{f:.1f}'} |")
    pl = p[p["spec"].str.startswith("PLACEBO")]
    print("\nPlacebo, 2016-2019 population change on the COVID shocks:\n")
    print("| Period | Spec | Natives | Mexico-born | US-born Mexican-origin | Other foreign-born |")
    print("|---|---|---:|---:|---:|---:|")
    for (per, spec), d in pl.groupby(["period", "spec"], sort=False):
        d = d.set_index("group")
        print(f"| {per} | {spec} | " + " | ".join(cs(d.loc[g, "coef"], d.loc[g, "se"])
                                              for g in ("natives", "mex_fb", "mex_nb", "oth_fb")) + " |")


def smoothing():
    s = pd.read_csv(DERIVED / "ck_smoothing.csv")
    print("| Period | Panel | Spec | Below median | Above median | Difference | Gradient per unit eta | F (below, above) |")
    print("|---|---|---|---:|---:|---:|---:|---|")
    for (per, panel, spec), d in s.groupby(["period", "panel", "spec"], sort=False):
        d = d.set_index("sample")
        fs = ("" if spec == "ols" else
              f"{d.loc['below_median', 'first_stage_F']:.1f}, {d.loc['above_median', 'first_stage_F']:.1f}")
        print(f"| {per} | {panel} | {spec} | " + " | ".join(
            cs(d.loc[k, "coef"], d.loc[k, "se"]) for k in
            ("below_median", "above_median", "difference", "slope_gradient_per_unit_eta")) + f" | {fs} |")


def episodes():
    e = pd.read_csv(DERIVED / "insurance_episode.csv")
    e = e[e["beneficiaries"] == "other_natives"]
    print("| Spec | Shock period | Metros | g per unit share (SE) | Jobs kept (bust) | Jobs forgone (mild) | Net jobs | Kept $bn | Forgone $bn | Net $bn (SE) |")
    print("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in e.iterrows():
        print(f"| {r['spec']} | {r['period']} | {r['metros']} ({r['n_metros']}) | {cs(r['g'], r['g_se'])} | "
              f"{r['protection_jobs']:,.0f} | {r['crowding_jobs']:,.0f} | {r['net_jobs']:,.0f} | "
              f"{r['protection_bn']:.2f} | {r['crowding_bn']:.2f} | {r['net_bn']:.2f} ({r['net_bn_se']:.2f}) |")


def mobility():
    m = pd.read_csv(DERIVED / "mobility_summary.csv")
    m = m[(m["lowed"] == "hs_or_less") & (m["sex"] == "men")]
    names = {"moved_abroad": "From abroad", "moved_interstate": "Between states", "long_distance": "Either"}
    print("| Rate, % a year (SE) | Group | 2006-2010 | 2019-2024 | 2024 |")
    print("|---|---|---:|---:|---:|")
    for meas, lab in names.items():
        for g in ("mex_fb", "mex_nb", "oth_nb", "oth_fb", "mex_fb_minus_oth_nb", "mex_nb_minus_oth_nb"):
            d = m[(m["measure"] == meas) & (m["group"] == g)].set_index("period")
            print(f"| {lab} | {g} | " + " | ".join(f"{d.loc[p, 'rate_pct']:.2f} ({d.loc[p, 'se_pct']:.2f})"
                                                 for p in ("2006_2010", "2019_2024", "2024")) + " |")


def borjas():
    t = pd.read_csv(DERIVED / "borjas_table8_reproduction.csv")
    print("| lambda | k | Cost | Printed $bn | Reproduced, 0.1 grid | 0.01 grid |")
    print("|---:|---:|---|---:|---:|---:|")
    for _, r in t.iterrows():
        print(f"| {r['lambda']} | {r['k']} | {r['cost']} | {r['printed_gain_bn']} | {r['gain_bn']:.2f} | {r['gain_bn_fine_grid']:.2f} |")
    b = pd.read_csv(DERIVED / "borjas_2024.csv")
    print("\n| Scenario | Sorting | lambda | theta | Low | Medium | High | Prohibitive |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for (sc, so, lam), d in b.groupby(["scenario", "sorting", "lambda"], sort=False):
        d = d.set_index("cost")
        print(f"| {sc} | {so} | {lam} | {d['theta'].iloc[0]:.3f} | " + " | ".join(
            f"{d.loc[c, 'gain_bn_2024_fine_grid']:.2f}" for c in ("low", "medium", "high", "prohibitive")) + " |")


if __name__ == "__main__":
    for title, fn in (("1 Population responses", population), ("2 Smoothing", smoothing),
                      ("3 Pricing per episode", episodes), ("4 Mobility", mobility), ("5 Borjas", borjas)):
        print(f"\n### {title}\n")
        fn()

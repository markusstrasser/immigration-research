"""Who inside "other residents" gains and loses wages from the Mexican-origin union's presence.

Reads the executed nest grid (production_nativity_nest_2026_09_22) and its CPS branch earnings;
no model is re-run. wage_pct = 100*(without/with - 1) per branch and skill cell, so the union's
presence changes a branch's earnings by -(wage_pct/100) * with-target earnings, hours held fixed.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
NEST = HERE.parent / "production_nativity_nest_2026_09_22" / "derived"
SOURCED_EPS = [float("inf"), 17.9, 8.7, 3.0]

s = pd.read_csv(NEST / "nest_scenarios.csv")
b = pd.read_csv(NEST / "branch_composition.csv")
earn = b.pivot_table(index=["proxy", "split", "skill"], columns="branch", values="earnings_estimate")

s = s[(s.excluded_capital_owner_share == 0) & (s.nest_option == "A_by_nativity")
      & s.sigma_NI.isin(SOURCED_EPS)].copy()
assert len(s), "empty nest grid selection"
for cell in (0, 1):
    for branch, tag in (("native_non_union", "native"), ("other_foreign_born", "otherfb")):
        base = s.apply(lambda r: earn.loc[(r.proxy, r.split, cell), branch], axis=1) / 1e9
        w = s[f"wage_pct_{tag.replace('otherfb', 'other_fb')}_cell{cell}"] / 100
        s[f"{tag}_cell{cell}_wage_pct_vs_absent"] = (1 / (1 + w) - 1) * 100
        s[f"{tag}_cell{cell}_earnings_bn"] = -w * base

keep = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
        "labor_supply_elasticity", "sigma_NI", "native_cell0_wage_pct_vs_absent",
        "native_cell1_wage_pct_vs_absent", "native_cell0_earnings_bn", "native_cell1_earnings_bn",
        "otherfb_cell0_earnings_bn", "otherfb_cell1_earnings_bn", "native_production_gain_bn",
        "other_immigrant_production_gain_bn"]
out = s[keep].drop_duplicates()
out.to_csv(HERE / "derived" / "wage_distribution_grid.csv", index=False)

summary = (out[(out.capital_adjustment == 1.0) & (out.sigma_NI == float("inf"))]
           .groupby(["split", "sigma"])[keep[8:]].agg(["min", "max"]).round(2))
summary.columns = ["_".join(c) for c in summary.columns]
summary.to_csv(HERE / "derived" / "wage_distribution_long_run_default.csv")
by_eps = (out[out.capital_adjustment == 1.0].groupby("sigma_NI")[keep[8:]].agg(["min", "max"]).round(2))
by_eps.columns = ["_".join(c) for c in by_eps.columns]
by_eps.to_csv(HERE / "derived" / "wage_distribution_by_epsilon_long_run.csv")
print(summary.to_string())
print(by_eps.to_string())

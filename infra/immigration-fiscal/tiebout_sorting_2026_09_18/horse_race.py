"""Horse race: Mexican-origin share against the top-1% effective tax rate, both entered
in the same regression, reported per standard deviation so the magnitudes are comparable.

Uses the panel built by `analyze_state.py` (derived/state_panel.csv). Year fixed effects,
standard errors clustered on state. Also reports the Asian and Cuban shares in the same
race, and the same race with metro-level data for the native population response.

Output: derived/horse_race.csv
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(HERE, "derived")

STATE_Y = {"net_out_all": "net out-migration, all filers (SOI)",
           "net_out_top": "net out-migration, $200k+ filers (SOI)",
           "net_agi": "net AGI outflow (SOI)",
           "net_agi_top": "net AGI outflow, $200k+ (SOI)",
           "net_out_native_acs": "net out-migration of natives (ACS)",
           "net_out_hi_acs": "net out-migration of $75k+ movers (ACS)"}
XS = ["mex_share", "asian_share", "cuban_share", "tax_top1"]
CTRL = ["lpop", "rent", "coll", "hhinc"]


def race(d, y, xs, ctrl, fe_col=None, cluster="st"):
    cols = [y] + xs + ctrl + ([fe_col] if fe_col else [])
    s = d[cols + [cluster, "year"]].dropna()
    X = s[xs + ctrl].copy()
    X = pd.concat([X, pd.get_dummies(s["year"], prefix="y", drop_first=True).astype(float)],
                  axis=1)
    if fe_col:
        X = pd.concat([X, pd.get_dummies(s[fe_col], prefix="f", drop_first=True)
                       .astype(float)], axis=1)
    X = sm.add_constant(X, has_constant="add")
    m = sm.OLS(s[y], X).fit(cov_type="cluster", cov_kwds={"groups": s[cluster]})
    out = []
    ysd = s[y].std()
    for x in xs:
        sd = s[x].std()
        ci = m.conf_int()
        out.append(dict(outcome=y, regressor=x, n=len(s),
                        coef=m.params[x], se=m.bse[x],
                        lo=ci.loc[x, 0], hi=ci.loc[x, 1],
                        per_sd=m.params[x] * sd,
                        per_sd_lo=ci.loc[x, 0] * sd, per_sd_hi=ci.loc[x, 1] * sd,
                        beta_std=m.params[x] * sd / ysd))
    return out


def main():
    d = pd.read_csv(os.path.join(DERIVED, "state_panel.csv"))
    rows = []
    for y in STATE_Y:
        rows += race(d, y, XS, CTRL)
    r = pd.DataFrame(rows)
    r["arm"] = "state, year FE"
    # region fixed effects on top
    rows2 = []
    for y in STATE_Y:
        rows2 += race(d, y, XS, CTRL, fe_col="region")
    r2 = pd.DataFrame(rows2)
    r2["arm"] = "state, year+region FE"
    out = pd.concat([r, r2], ignore_index=True)
    out.to_csv(os.path.join(DERIVED, "horse_race.csv"), index=False)
    pd.set_option("display.width", 220)
    for arm in out.arm.unique():
        print("\n===", arm, "===")
        print(out[out.arm == arm][["outcome", "regressor", "n", "coef", "se",
                                   "per_sd", "per_sd_lo", "per_sd_hi", "beta_std"]]
              .to_string(index=False, float_format=lambda v: "%.4f" % v))
    print("\nregressor standard deviations across the state panel:")
    print(d[XS].std().round(3).to_string())


if __name__ == "__main__":
    main()

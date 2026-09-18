"""Single-instrument placebo the lane did not run.

estimate.py's IV-placebo-pre arm uses the multi-origin instrument Zm, which has a dead first
stage in this period (Shea partial R2 ~ 1e-4), so that placebo cannot fail or pass. This script
runs the placebo the brief actually specified: the conventional single-origin Mexican
instrument Z for window (t0, t1) against the native no-college outcome change over the
PREVIOUS window (t0-5, t0). Reported as the reduced-form slope of the pre-window outcome
change on Z (weighted, HC1), next to the same reduced form on the current window's change,
and as the pre-window IV coefficient (dX_lag instrumented by Z_current) for scale.

Windows with an available lag: 2010-15 (lag 2005-10), 2013-18 (lag 2008-13), 2018-23 (lag 2013-18).
"""
import pandas as pd, numpy as np, statsmodels.api as sm
from linearmodels.iv import IV2SLS
import estimate as E

def wls(y, x, w):
    X = sm.add_constant(x)
    r = sm.WLS(y, X, weights=w).fit(cov_type="HC1")
    return r.params.iloc[1], r.bse.iloc[1]

def main():
    panel, base = E.load()
    zm = E.load_multi_origin()
    nat_mex, nat_fb = E.national(panel, "t_mex1864"), E.national(panel, "t_fb1864")
    rows = []
    for out, oname, wcol in E.OUTCOMES[:2] + E.OUTCOMES[4:5]:
        for (t0, t1), (l0, l1) in [((2010, 2015), (2005, 2010)), ((2013, 2018), (2008, 2013)),
                                   ((2018, 2023), (2013, 2018))]:
            m = E.build_window(panel, base, nat_mex, nat_fb, zm, "B", t0, t1, "mex_share", out, 50_000, wcol)
            ml = E.build_window(panel, base, nat_mex, nat_fb, zm, "B", l0, l1, "mex_share", out, 50_000, wcol)
            j = m.merge(ml[["cbsa", "dX", "dy"]], on="cbsa", suffixes=("", "_pre"))
            b_cur, se_cur = wls(j.dy, j.Z, j.w)          # reduced form, current window
            b_pre, se_pre = wls(j.dy_pre, j.Z, j.w)      # placebo reduced form
            iv = IV2SLS(j.dy_pre, sm.add_constant(pd.DataFrame(index=j.index)), j[["dX_pre"]], j[["Z"]],
                        weights=j.w).fit(cov_type="robust")
            rows.append(dict(outcome=oname, window=f"{t0}-{t1}", pre_window=f"{l0}-{l1}", n_metro=len(j),
                             rf_current=b_cur, rf_current_se=se_cur, rf_pre=b_pre, rf_pre_se=se_pre,
                             iv_pre_coef=float(iv.params["dX_pre"]), iv_pre_se=float(iv.std_errors["dX_pre"]),
                             corr_Z_dXpre=float(np.corrcoef(j.Z, j.dX_pre)[0, 1])))
    d = pd.DataFrame(rows)
    d.to_csv(E.DERIVED / "placebo_single.csv", index=False)
    pd.set_option("display.width", 250)
    print(d.round(3).to_string(index=False))

if __name__ == "__main__":
    main()

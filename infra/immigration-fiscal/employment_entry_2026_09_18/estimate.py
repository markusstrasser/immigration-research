"""Long-difference OLS / shift-share IV / Jaeger-Ruist-Stuhler multiple-instrument estimates
of native entry-age employment on the metro immigrant population share.

Coefficient units throughout: percentage-point change in the native employment (or
participation) rate per 1 percentage-point rise in the immigrant share of the metro
population aged 18-64.

Estimators per arm and window (t0 -> t1):
  OLS            dy = a + b dX
  IV-single      dX instrumented by Z  = base_share_2000(one group) * national shift / pop
  IV-multi       dX instrumented by Zm = SUM_o base_share_2000(o) * national shift(o) / pop
  IV-JRS         dy = a + b dX + g dX_lag, (dX, dX_lag) instrumented by (Zm, Zm_lag)
  IV-multi-same  IV-multi refit on the JRS sample, so the JRS contrast is like-for-like
  IV-placebo-pre Zm against the outcome change in the PREVIOUS window

The JRS arm uses the MULTI-origin instrument by necessity: with one origin group the
current and lagged predicted inflows are the same metro base share times a scalar and are
collinear across metros, so the two-endogenous system is not identified. The reported
`corr_Z_Zlag` columns make that visible for both instrument sets.
"""
import itertools, pathlib
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"

# Endpoint years pulled: 2005, 2008, 2010, 2013, 2015, 2018, 2023.
# The lagged window each JRS arm needs is shown in brackets.
WINDOWS = {"5y": [(2005, 2010), (2008, 2013), (2010, 2015), (2013, 2018), (2018, 2023)],
           "10y": [(2005, 2015), (2008, 2018), (2013, 2023)]}
# lag window for (t0,t1) is (t0-(t1-t0), t0); only these exist in the pulled years
LAGS = {(2010, 2015): (2005, 2010), (2013, 2018): (2008, 2013), (2018, 2023): (2013, 2018),
        (2015, 2025): None}
# (column, label, weight column)
OUTCOMES = [("epop1829", "E/POP 18-29", "pop1829"), ("lfp1829", "LFP 18-29", "pop1829"),
            ("epop1624", "E/POP 16-24", "pop1624"), ("lfp1624", "LFP 16-24", "pop1624"),
            ("epopc1829", "E/POP 18-29 COLLEGE (control)", "popc"),
            ("lfpc1829", "LFP 18-29 COLLEGE (control)", "popc")]
SEXES = [("1", "men"), ("2", "women"), ("B", "both")]
TREATS = [("mex_share", "Mexico-born"), ("fb_share", "all foreign-born")]
MIN_POPS = [50_000, 25_000]


def load():
    p = pd.read_csv(DERIVED / "metro_year_panel.csv", dtype={"cbsa": str, "sex": str})
    base = pd.read_csv(DERIVED / "metro_base_2000.csv", dtype={"cbsa": str})
    sums = [c for c in ["pop1829", "emp1829", "cemp1829", "lf1829",
                        "pop1624", "emp1624", "cemp1624", "lf1624",
                        "popc", "empc", "lfc"] if c in p.columns]
    agg = {c: "sum" for c in sums}
    agg.update({c: "first" for c in ["t_pop1864", "t_mex1864", "t_fb1864"]})
    both = p.groupby(["cbsa", "cbsa_title", "year"], as_index=False).agg(agg)
    for b in ("1829", "1624"):
        both[f"epop{b}"] = 100 * both[f"emp{b}"] / both[f"pop{b}"]
        both[f"lfp{b}"] = 100 * both[f"lf{b}"] / both[f"pop{b}"]
    if "popc" in both.columns:
        both["epopc1829"] = 100 * both["empc"] / both["popc"]
        both["lfpc1829"] = 100 * both["lfc"] / both["popc"]
    both["mex_share"] = 100 * both["t_mex1864"] / both["t_pop1864"]
    both["fb_share"] = 100 * both["t_fb1864"] / both["t_pop1864"]
    both["sex"] = "B"
    cols = [c for c in p.columns if c in both.columns]
    return pd.concat([p[cols], both[cols]], ignore_index=True), base


def load_multi_origin():
    mb = pd.read_csv(DERIVED / "metro_origin_base.csv", dtype={"cbsa": str})
    ns = pd.read_csv(DERIVED / "national_origin_stock.csv")
    piv = ns.pivot(index="year", columns="origin", values="natl_stock")
    W = mb.pivot(index="cbsa", columns="origin", values="base_share").fillna(0.0)
    common = [c for c in piv.columns if c in W.columns]
    return W[common], piv[common]


def zmulti(W, piv, t0, t1):
    d = (piv.loc[t1] - piv.loc[t0]).reindex(W.columns).fillna(0.0)
    return W.values @ d.values


def national(panel, col):
    return panel[panel.sex == "B"].groupby("year")[col].sum()


def build_window(panel, base, nat_mex, nat_fb, zm, sex, t0, t1, treat, outcome, min_pop,
                 wcol="pop1829"):
    a = panel[(panel.year == t0) & (panel.sex == sex)]
    b = panel[(panel.year == t1) & (panel.sex == sex)]
    m = a.merge(b, on="cbsa", suffixes=("_0", "_1"))
    m = m.merge(base[["cbsa", "mex_base_share_natl", "fb_base_share_natl"]],
                on="cbsa", how="inner")
    m["dy"] = m[f"{outcome}_1"] - m[f"{outcome}_0"]
    m["dX"] = m[f"{treat}_1"] - m[f"{treat}_0"]
    natl = nat_mex if treat == "mex_share" else nat_fb
    bshare = "mex_base_share_natl" if treat == "mex_share" else "fb_base_share_natl"
    m["Z"] = 100.0 * m[bshare] * (natl[t1] - natl[t0]) / m["t_pop1864_0"]
    W, piv = zm
    pred = pd.Series(zmulti(W, piv, t0, t1), index=W.index, name="predfb")
    m = m.merge(pred, left_on="cbsa", right_index=True, how="left")
    m["Zm"] = 100.0 * m["predfb"] / m["t_pop1864_0"]
    m["w"] = m[f"{wcol}_0"]
    # the floor is defined on the pooled cell, so single-sex arms keep the same metros
    floor = min_pop if sex == "B" else min_pop / 2.0
    m = m[m["w"] >= floor]
    return m[["cbsa", "dy", "dX", "Z", "Zm", "w"]].dropna()


def _fs_diag(r, name):
    """First-stage F and Shea's partial R-squared.

    Shea's partial R-squared is the diagnostic that matters for the JRS arm: with two
    endogenous regressors and two near-collinear instruments the individual first-stage F
    can look large while the system is effectively underidentified, which is the failure
    JRS report for every decade after the 1970s. Shea's measure collapses toward zero in
    exactly that case; linearmodels exposes no Kleibergen-Paap statistic.
    """
    out = {"first_stage_F": np.nan, "shea_partial_r2": np.nan}
    try:
        d = r.first_stage.diagnostics
        fcol = next((c for c in d.columns if c.lower().startswith("f.stat")), None)
        if fcol:
            out["first_stage_F"] = float(d.loc[name, fcol])
        scol = next((c for c in d.columns if "shea" in c.lower()), None)
        if scol:
            out["shea_partial_r2"] = float(d.loc[name, scol])
    except Exception:
        pass
    return out


def run(m, endog=None, instr=None, extra_exog=None, cluster=None):
    y, wt = m["dy"], m["w"]
    ex = pd.DataFrame({"const": np.ones(len(m))}, index=m.index)
    if endog is None:
        ex["dX"] = m["dX"]
        x = z = None
        key = "dX"
    else:
        x, z = m[list(endog)], m[list(instr)]
        key = endog[0]
    if extra_exog is not None:
        ex = pd.concat([ex, extra_exog], axis=1)
    mod = IV2SLS(y, ex, x, z, weights=wt)
    r = (mod.fit(cov_type="clustered", clusters=cluster) if cluster is not None
         else mod.fit(cov_type="robust"))
    b, se = float(r.params[key]), float(r.std_errors[key])
    d = dict(coef=b, se=se, ci_lo=b - 1.96 * se, ci_hi=b + 1.96 * se)
    d.update({"first_stage_F": np.nan, "shea_partial_r2": np.nan} if endog is None
             else _fs_diag(r, key))
    if endog is not None and len(endog) > 1:
        d["coef_lag"] = float(r.params[endog[1]])
        d["se_lag"] = float(r.std_errors[endog[1]])
    return d


def arm_rows(m, j, rec, extra=None, cluster=None):
    out = []
    out.append({**rec, "estimator": "OLS", **run(m, extra_exog=extra, cluster=cluster)})
    out.append({**rec, "estimator": "IV-single",
                **run(m, ("dX",), ("Z",), extra, cluster)})
    out.append({**rec, "estimator": "IV-multi",
                **run(m, ("dX",), ("Zm",), extra, cluster)})
    if j is not None and len(j) >= 30:
        ex_j = extra
        cl_j = j["cbsa"] if cluster is not None else None
        if extra is not None:
            ex_j = pd.get_dummies(j["win"], prefix="w", drop_first=True).astype(float)
            ex_j.index = j.index
        rj = dict(rec); rj["n_metro"] = len(j)
        # Correlation between the current and lagged predicted inflows, computed WITHIN each
        # window and averaged. Computing it on the stacked sample would mix windows that differ
        # in scale and sign and would not describe the collinearity the 2SLS actually faces.
        def _rho(a, b):
            if "win" in j.columns:
                vals = [float(np.corrcoef(g[a], g[b])[0, 1])
                        for _, g in j.groupby("win") if len(g) > 5]
                vals = [v for v in vals if np.isfinite(v)]
                return float(np.mean(vals)) if vals else np.nan
            return float(np.corrcoef(j[a], j[b])[0, 1])
        rho_m = _rho("Zm", "Zm_lag")
        rho_1 = _rho("Z", "Z_lag")
        out.append({**rj, "estimator": "IV-multi-same-sample",
                    **run(j, ("dX",), ("Zm",), ex_j, cl_j),
                    "corr_Zm_Zmlag": rho_m, "corr_Z_Zlag": rho_1})
        out.append({**rj, "estimator": "IV-JRS",
                    **run(j, ("dX", "dX_lag"), ("Zm", "Zm_lag"), ex_j, cl_j),
                    "corr_Zm_Zmlag": rho_m, "corr_Z_Zlag": rho_1})
        jp = j.copy(); jp["dy"] = jp["dy_lag"]
        out.append({**rj, "estimator": "IV-placebo-pre",
                    **run(jp, ("dX",), ("Zm",), ex_j, cl_j),
                    "corr_Zm_Zmlag": rho_m, "corr_Z_Zlag": rho_1})
    return out


def main():
    panel, base = load()
    zm = load_multi_origin()
    nat_mex, nat_fb = national(panel, "t_mex1864"), national(panel, "t_fb1864")
    rows = []
    for min_pop in MIN_POPS:
        for (treat, tname), (sex, sname), (out, oname, wcol) in itertools.product(
                TREATS, SEXES, OUTCOMES):
            for wlab, wins in WINDOWS.items():
                stack, jstack = [], []
                for (t0, t1) in wins:
                    try:
                        m = build_window(panel, base, nat_mex, nat_fb, zm, sex,
                                         t0, t1, treat, out, min_pop, wcol)
                    except KeyError:
                        continue
                    if len(m) < 30:
                        continue
                    lag0, lag1 = LAGS.get((t0, t1), (t0 - (t1 - t0), t0)) or (None, None)
                    j = None
                    if lag0 is None:
                        lag0, lag1 = -1, -1
                    try:
                        ml = build_window(panel, base, nat_mex, nat_fb, zm, sex,
                                          lag0, lag1, treat, out, min_pop, wcol)
                        if len(ml) >= 30:
                            j = m.merge(ml[["cbsa", "dX", "Z", "Zm", "dy"]], on="cbsa",
                                        suffixes=("", "_lag"))
                    except KeyError:
                        pass
                    rec = dict(min_pop=min_pop, treatment=tname, sex=sname, outcome=oname,
                               window=f"{t0}-{t1}", length=wlab, n_metro=len(m))
                    rows += arm_rows(m, j, rec)
                    mm = m.copy(); mm["win"] = f"{t0}-{t1}"; stack.append(mm)
                    if j is not None and len(j) >= 30:
                        jj = j.copy(); jj["win"] = f"{t0}-{t1}"; jstack.append(jj)
                if stack:
                    S = pd.concat(stack, ignore_index=True)
                    D = pd.get_dummies(S["win"], prefix="w", drop_first=True).astype(float)
                    D.index = S.index
                    J = pd.concat(jstack, ignore_index=True) if jstack else None
                    rec = dict(min_pop=min_pop, treatment=tname, sex=sname, outcome=oname,
                               window="POOLED", length=wlab, n_metro=len(S))
                    rows += arm_rows(S, J, rec, extra=D, cluster=S["cbsa"])
    df = pd.DataFrame(rows)
    df.to_csv(DERIVED / "estimates.csv", index=False)
    print("estimate rows:", len(df))
    head = df[(df.min_pop == 50_000) & (df.window == "POOLED") & (df.length == "5y")
              & (df.outcome == "E/POP 18-29") & (df.sex == "both")]
    print(head.to_string(index=False))


if __name__ == "__main__":
    main()

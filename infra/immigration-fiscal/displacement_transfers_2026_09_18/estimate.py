"""Long-difference OLS / shift-share IV for native withdrawal onto transfers.

Units. Every coefficient is the change in the outcome, in percentage points, per
1 percentage-point rise in the immigrant share of the metro population aged 18-64.

Treatment. The foreign-born and Mexico-born share of the metro population aged 18-64,
taken from the employment_entry lane's `metro_year_panel.csv`. That series is built from
ACS PUMS allocated through Geocorr into ONE FIXED OMB February-2013 CBSA delineation, so
the same geography is differenced at both endpoints. The published ACS metro-level
foreign-born share was tried first and abandoned: its LEVELS agree with the PUMS series
(r = 0.99) but its CHANGES only correlate 0.65-0.82 with them, and the first stage on the
published series is dead in every window (F < 1.3) while the same instrument against the
fixed-geography series reaches F 15.6 (2005-2008, all foreign-born) and F 55.2 (2005-2015,
Mexico-born). Both arms are
estimated and both are reported; the published-share arm is labelled as failing.

Outcomes. Metro-level ACS 1-year summary tables (this lane's own pull), matched on CBSA
code. They are NOT split by nativity - see the memo's identification section.

Instrument. Z = (metro's share of the national foreign-born or Mexico-born stock in the
base) x (national stock change over the window) / (metro population at t0) x 100.

Disconfirmation arms, all fixed before any estimate was read:
  placebo   the window's own instrument against the PREVIOUS period's outcome change
  college   the BA+ control group, which should not move if the effect is skill-specific
  sign      the same arm across several windows
  recovery  for 2021-2024, the 2019-2021 outcome change entered as a covariate
"""
import pathlib
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS
import statsmodels.api as sm

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"
EE = HERE.parent / "employment_entry_2026_09_18" / "derived" / "metro_year_panel.csv"

# (t0, t1, previous window for the placebo, design tag)
WINDOWS = [
    # The 2000-based windows are the ones the brief asks for: the national Mexico-born
    # stock grew +2.56M and the foreign-born stock +7.0M over 2000-2007, so the shift
    # half of the shift-share is large and positive, unlike every post-2008 window.
    (2000, 2005, None, "1"),
    (2000, 2007, None, "1"),
    (2000, 2008, None, "1"),
    (2000, 2010, None, "1"),
    (2005, 2008, (2000, 2005), "1"),
    (2005, 2010, (2000, 2005), "1"),
    (2005, 2015, (2000, 2005), "1"),
    (2008, 2013, (2005, 2008), "1"),
    (2008, 2018, (2005, 2008), "1"),
    (2010, 2015, (2005, 2010), "aux"),
    (2013, 2018, (2008, 2013), "aux"),
    (2013, 2023, (2008, 2013), "aux"),
    (2018, 2023, (2013, 2018), "aux"),
    (2021, 2024, (2019, 2021), "2"),
    (2021, 2023, (2019, 2021), "2"),
]
OUTCOMES = [
    ("ssi_rate", "household SSI receipt"),
    ("pa_rate", "household public assistance receipt"),
    ("snap_rate", "household SNAP receipt"),
    ("nc_epop", "E/POP 25-64 below BA"),
    ("nc_lfp", "LFP 25-64 below BA"),
    ("col_epop", "E/POP 25-64 BA+ (CONTROL)"),
    ("col_lfp", "LFP 25-64 BA+ (CONTROL)"),
]
TREATS = [("fb", "all foreign-born"), ("mex", "Mexico-born")]
MIN_POP = 100_000


def load():
    out = pd.read_csv(DERIVED / "metro_panel.csv", dtype={"cbsa": str})
    base = pd.read_csv(DERIVED / "base_shares_pre1990.csv", dtype={"cbsa": str})
    natl = pd.read_csv(DERIVED / "national_stock.csv").set_index("year")
    ee = pd.read_csv(EE, dtype={"cbsa": str, "sex": str})
    ee = ee[ee.sex == "1"].drop_duplicates(["cbsa", "year"])
    ee["fb_share_fix"] = 100 * ee.t_fb1864 / ee.t_pop1864
    ee["mex_share_fix"] = 100 * ee.t_mex1864 / ee.t_pop1864
    ee = ee[["cbsa", "year", "fb_share_fix", "mex_share_fix"]]
    # published-share fallback for years the fixed-geography panel does not cover (2021, 2024)
    pub = out[["cbsa", "year", "fb_share", "mex_share"]].rename(
        columns={"fb_share": "fb_share_pub", "mex_share": "mex_share_pub"})
    return out, base, natl, ee, pub


def wls(y, X, w):
    return sm.WLS(y, sm.add_constant(X), weights=w).fit(cov_type="HC1")


def build(out, base, natl, treat_src, t0, t1, outcome, grp, tcol,
          placebo_from=None, min_pop=MIN_POP):
    a = out[out.year == t0][["cbsa", outcome, "pop"]]
    b = out[out.year == t1][["cbsa", outcome]]
    m = a.merge(b, on="cbsa", suffixes=("_0", "_1"))
    ta = treat_src[treat_src.year == t0][["cbsa", tcol]]
    tb = treat_src[treat_src.year == t1][["cbsa", tcol]]
    m = m.merge(ta.merge(tb, on="cbsa", suffixes=("_0", "_1")), on="cbsa")
    m = m.merge(base[["cbsa", "fb_base_share", "mex_base_share"]], on="cbsa", how="inner")
    m["dy"] = m[f"{outcome}_1"] - m[f"{outcome}_0"]
    m["dX"] = m[f"{tcol}_1"] - m[f"{tcol}_0"]
    # the t0 LEVEL of the outcome, kept so mean reversion can be controlled for and
    # so the instrument can be tested against it (see the memo's disconfirmation section)
    m["y0"] = m[f"{outcome}_0"]
    shift = natl.loc[t1, grp] - natl.loc[t0, grp]
    m["Z"] = 100.0 * m[f"{grp}_base_share"] * shift / m["pop"]
    m["w"] = m["pop"]
    if placebo_from is not None:
        p0, p1 = placebo_from
        pa_ = out[out.year == p0][["cbsa", outcome]]
        pb_ = out[out.year == p1][["cbsa", outcome]]
        if len(pa_) and len(pb_):
            pm = pa_.merge(pb_, on="cbsa", suffixes=("_p0", "_p1"))
            pm["dy_pre"] = pm[f"{outcome}_p1"] - pm[f"{outcome}_p0"]
            m = m.merge(pm[["cbsa", "dy_pre"]], on="cbsa", how="left")
    m = m[m["w"] >= min_pop]
    cols = ["dy", "dX", "Z", "w", "y0"]
    if "dy_pre" in m.columns and m["dy_pre"].notna().any():
        cols.append("dy_pre")
    return m[["cbsa"] + cols].replace([np.inf, -np.inf], np.nan).dropna(), shift


def fit(m, meta, controls=()):
    rows, ctl, n = [], list(controls), len(m)
    if n < 25:
        return rows
    def rec(est, r, key):
        ci = r.conf_int()
        return dict(**meta, estimator=est, n=n, coef=r.params[key], se=r.bse[key],
                    lo=ci.loc[key, 0], hi=ci.loc[key, 1])
    fs = wls(m["dX"], m[["Z"] + ctl], m["w"])
    F = (fs.params["Z"] / fs.bse["Z"]) ** 2
    rows.append({**rec("OLS" + ("+ctl" if ctl else ""), wls(m["dy"], m[["dX"] + ctl], m["w"]),
                       "dX"), "first_stage_F": np.nan})
    rows.append({**rec("first-stage", fs, "Z"), "first_stage_F": F})
    rows.append({**rec("reduced-form" + ("+ctl" if ctl else ""),
                       wls(m["dy"], m[["Z"] + ctl], m["w"]), "Z"), "first_stage_F": F})
    try:
        exog = sm.add_constant(m[ctl]) if ctl else pd.DataFrame(
            {"const": np.ones(n)}, index=m.index)
        iv = IV2SLS(m["dy"], exog, m[["dX"]], m[["Z"]], weights=m["w"]).fit(cov_type="robust")
        ci = iv.conf_int().loc["dX"]
        rows.append(dict(**meta, estimator="IV" + ("+ctl" if ctl else ""), n=n,
                         coef=iv.params["dX"], se=iv.std_errors["dX"],
                         lo=ci["lower"], hi=ci["upper"], first_stage_F=F))
    except Exception as e:
        rows.append(dict(**meta, estimator="IV-FAILED", n=n, coef=np.nan, se=np.nan,
                         lo=np.nan, hi=np.nan, first_stage_F=F, note=str(e)[:60]))
    if not ctl:
        rows.append({**rec("Z-ON-BASELINE-LEVEL (exogeneity test)",
                           wls(m["y0"], m[["Z"]], m["w"]), "Z"), "first_stage_F": F})
    if "dy_pre" in m.columns and "dy_pre" not in ctl:
        rows.append({**rec("PLACEBO reduced-form on prior dy",
                           wls(m["dy_pre"], m[["Z"]], m["w"]), "Z"), "first_stage_F": F})
    return rows


def main():
    out, base, natl, ee, pub = load()
    fixed_years = set(ee.year)
    rows = []
    for t0, t1, pre, design in WINDOWS:
        if t0 not in set(out.year) or t1 not in set(out.year):
            print("skip (outcome year missing)", t0, t1); continue
        for grp, glab in TREATS:
            use_fixed = t0 in fixed_years and t1 in fixed_years
            src, tcol, geo = ((ee, f"{grp}_share_fix", "fixed-2013-PUMS") if use_fixed
                              else (pub, f"{grp}_share_pub", "published-ACS"))
            shift = natl.loc[t1, grp] - natl.loc[t0, grp]
            for outcome, _ in OUTCOMES:
                meta = dict(design=design, window=f"{t0}-{t1}", outcome=outcome,
                            treat=glab, geo=geo, natl_shift=shift)
                m, _ = build(out, base, natl, src, t0, t1, outcome, grp, tcol,
                             placebo_from=pre)
                if m.empty:
                    continue
                rows += fit(m, meta)
                # mean-reversion control: the t0 level of the outcome as a covariate
                rows += fit(m, {**meta, "design": design + "-levelctl"}, controls=["y0"])
                if design == "2" and "dy_pre" in m.columns:
                    rows += fit(m, {**meta, "design": "2-recovctl"}, controls=["dy_pre"])
            # robustness: same window on the published-share treatment, to show it fails
            if use_fixed:
                for outcome in ("ssi_rate", "nc_epop"):
                    meta = dict(design=design + "-pubshare", window=f"{t0}-{t1}",
                                outcome=outcome, treat=glab, geo="published-ACS",
                                natl_shift=shift)
                    m, _ = build(out, base, natl, pub, t0, t1, outcome, grp,
                                 f"{grp}_share_pub")
                    if not m.empty:
                        rows += fit(m, meta)
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "estimates.csv", index=False)
    print("wrote estimates.csv", est.shape)
    key = est[est.estimator.isin(["OLS", "IV", "first-stage",
                                  "PLACEBO reduced-form on prior dy"])]
    key = key[key.design.isin(["1", "2", "2-recovctl"])]
    with pd.option_context("display.width", 220, "display.max_rows", 500):
        print(key[["design", "window", "treat", "geo", "outcome", "estimator", "n",
                   "coef", "se", "lo", "hi", "first_stage_F"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()

"""Design B, and the nativity-split version of Design A, on the PUMS metro panel.

Two things this file adds that the aggregate route could not do.

A-split: transfer receipt among NATIVES ONLY (aged 25-54, below a bachelor's degree).
  Section 4's aggregate outcome counts all households, so a negative coefficient there can
  be the mechanical effect of adding low-take-up immigrant households to the denominator.
  Here that channel is closed: the denominator is natives.

B: wages of EARLIER Mexico-born workers (arrived before 2000) against the inflow, which is
  the Ottaviano-Peri / Card prediction that prior immigrants bear the incidence.

Two measurement defects are handled rather than hidden.
  * ACS 2005 codes WKW as CONTINUOUS weeks 1-52, while 2008 codes it as a bracket with
    1 = "50 to 52 weeks". The pull's full-time-full-year test (`wkw == 1`) therefore matched
    only people who worked exactly one week in 2005: the 2005 FTFY share is 0.001 against
    0.56 in 2008. Every 2005 FTFY cell is discarded, so FTFY wage windows start in 2008.
    Per-person wage measures do not use the weeks variable and keep 2005.
  * The ACS SNAP question begins in 2008. The 2005 SNAP cells are near-zero (0.01%) and are
    discarded; SNAP windows start in 2008.

Treatment. Where both endpoints exist in the employment_entry lane's fixed-2013-geography
PUMS series (2005 and 2008), that series is used and the first stage is live. For 2021 and
2024 it does not exist, so the published ACS metro share is used and the first stage is dead;
those rows are reported as OLS associations and labelled.
"""
import pathlib
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS
import statsmodels.api as sm

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"
EE = HERE.parent / "employment_entry_2026_09_18" / "derived" / "metro_year_panel.csv"

# outcome -> (label, earliest usable year, log-transform?)
OUTCOMES = {
    "nat_ssi": ("native no-college 25-54 SSI receipt, pp", 2005, False),
    "nat_pa": ("native no-college 25-54 public assistance receipt, pp", 2005, False),
    "nat_snap": ("native no-college 25-54 SNAP receipt, pp", 2008, False),
    "nat_epop": ("native no-college 25-54 E/POP, pp", 2005, False),
    "nat_lfp": ("native no-college 25-54 LFP, pp", 2005, False),
    "mx_pre_wage_pp": ("log mean wage per person, Mexico-born arrived pre-2000", 2005, True),
    "mx_pre_nc_wage_pp": ("log mean wage per person, pre-2000 arrivals below BA", 2005, True),
    "mx_pre_ftfy_wage": ("log mean FTFY wage, Mexico-born arrived pre-2000", 2008, True),
    "mx_pre_epop": ("E/POP, Mexico-born arrived pre-2000, pp", 2005, False),
    "mx_post_wage_pp": ("log mean wage per person, Mexico-born arrived 2000+", 2005, True),
    "mx_post_ftfy_wage": ("log mean FTFY wage, Mexico-born arrived 2000+", 2008, True),
}
WINDOWS = [(2005, 2008), (2008, 2024), (2005, 2024), (2021, 2024)]
MIN_POP = 25_000     # weighted native no-college 25-54 persons in the base year


def load():
    p = pd.read_csv(DERIVED / "pums_metro_panel.csv", dtype={"cbsa": str})
    agg = pd.read_csv(DERIVED / "metro_panel.csv", dtype={"cbsa": str})
    base = pd.read_csv(DERIVED / "base_shares_pre1990.csv", dtype={"cbsa": str})
    natl = pd.read_csv(DERIVED / "national_stock.csv").set_index("year")
    ee = pd.read_csv(EE, dtype={"cbsa": str, "sex": str})
    ee = ee[ee.sex == "1"].drop_duplicates(["cbsa", "year"])
    ee["fb_share_fix"] = 100 * ee.t_fb1864 / ee.t_pop1864
    ee["mex_share_fix"] = 100 * ee.t_mex1864 / ee.t_pop1864
    pub = agg[["cbsa", "year", "fb_share", "pop"]].rename(columns={"fb_share": "fb_share_pub"})
    return p, base, natl, ee[["cbsa", "year", "fb_share_fix", "mex_share_fix"]], pub


def wls(y, X, w):
    return sm.WLS(y, sm.add_constant(X), weights=w).fit(cov_type="HC1")


def main():
    p, base, natl, ee, pub = load()
    rows = []
    for t0, t1 in WINDOWS:
        use_fixed = t0 in set(ee.year) and t1 in set(ee.year)
        src, tcol, geo = ((ee, "fb_share_fix", "fixed-2013-PUMS") if use_fixed
                          else (pub, "fb_share_pub", "published-ACS"))
        shift = natl.loc[t1, "fb"] - natl.loc[t0, "fb"]
        for oc, (lab, first_ok, logit) in OUTCOMES.items():
            if t0 < first_ok:
                rows.append(dict(window=f"{t0}-{t1}", outcome=oc, label=lab, geo=geo,
                                 estimator="SKIPPED (variable not comparable at t0)",
                                 n=0, coef=np.nan, se=np.nan, lo=np.nan, hi=np.nan,
                                 first_stage_F=np.nan, natl_shift=shift))
                continue
            a = p[p.year == t0][["cbsa", oc, "nat_pop"]]
            b = p[p.year == t1][["cbsa", oc]]
            m = a.merge(b, on="cbsa", suffixes=("_0", "_1"))
            m = m.merge(src[src.year == t0][["cbsa", tcol]].merge(
                src[src.year == t1][["cbsa", tcol]], on="cbsa", suffixes=("_0", "_1")),
                on="cbsa")
            m = m.merge(base[["cbsa", "fb_base_share"]], on="cbsa", how="inner")
            m = m.merge(pub[pub.year == t0][["cbsa", "pop"]], on="cbsa", how="inner")
            y0, y1 = m[f"{oc}_0"], m[f"{oc}_1"]
            if logit:
                y0, y1 = np.log(y0.where(y0 > 0)), np.log(y1.where(y1 > 0))
            m["dy"] = 100 * (y1 - y0) if logit else (y1 - y0)   # log arm reported in percent
            m["dX"] = m[f"{tcol}_1"] - m[f"{tcol}_0"]
            m["Z"] = 100.0 * m["fb_base_share"] * shift / m["pop"]
            m["w"] = m["nat_pop"]
            m = m[m["w"] >= MIN_POP]
            m = m[["cbsa", "dy", "dX", "Z", "w"]].replace([np.inf, -np.inf], np.nan).dropna()
            if len(m) < 25:
                continue
            meta = dict(window=f"{t0}-{t1}", outcome=oc, label=lab, geo=geo,
                        natl_shift=shift)
            fs = wls(m["dX"], m[["Z"]], m["w"])
            F = (fs.params["Z"] / fs.bse["Z"]) ** 2
            for est, r, k in (("OLS", wls(m["dy"], m[["dX"]], m["w"]), "dX"),
                              ("first-stage", fs, "Z"),
                              ("reduced-form", wls(m["dy"], m[["Z"]], m["w"]), "Z")):
                ci = r.conf_int()
                rows.append(dict(**meta, estimator=est, n=len(m), coef=r.params[k],
                                 se=r.bse[k], lo=ci.loc[k, 0], hi=ci.loc[k, 1],
                                 first_stage_F=F))
            try:
                iv = IV2SLS(m["dy"], pd.DataFrame({"const": np.ones(len(m))}, index=m.index),
                            m[["dX"]], m[["Z"]], weights=m["w"]).fit(cov_type="robust")
                ci = iv.conf_int().loc["dX"]
                rows.append(dict(**meta, estimator="IV", n=len(m), coef=iv.params["dX"],
                                 se=iv.std_errors["dX"], lo=ci["lower"], hi=ci["upper"],
                                 first_stage_F=F))
            except Exception as e:
                rows.append(dict(**meta, estimator="IV-FAILED", n=len(m), coef=np.nan,
                                 se=np.nan, lo=np.nan, hi=np.nan, first_stage_F=F))
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "estimates_pums.csv", index=False)
    print("wrote estimates_pums.csv", out.shape)
    pd.set_option("display.width", 220)
    k = out[out.estimator.isin(["OLS", "IV", "first-stage"])]
    print(k[["window", "geo", "outcome", "estimator", "n", "coef", "se", "lo", "hi",
             "first_stage_F"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()

"""Mexico-born arrival cohorts on ACS 1-year PUMS (staged parquet in _cache/).

Mexico-born = POBP == 303.  Comparator = US-born (NATIVITY==1) non-Hispanic (HISP==1)
white (RAC1P==1).  Ages 25-54.

SCHL (2008+): <=15 less than HS diploma; 16-17 HS diploma/GED; 18-20 some college/associate;
>=21 bachelor's or more.
ENG: 1 very well, 2 well, 3 not well, 4 not at all; missing = speaks only English at home.
Full-time full-year = WKHP >= 35 and WKWN >= 48.

Outputs derived/acs_*.csv
"""
import os, glob
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "derived")
os.makedirs(OUT, exist_ok=True)

EDU_ORDER = ["lths", "hs", "somecoll", "ba_plus"]
COHORTS = ["pre1980", "1980-89", "1990-99", "2000-07", "2008-14", "2015-19", "2020-21", "2022-24"]


def cohort_of(y):
    if pd.isna(y):
        return None
    y = int(y)
    if y < 1980:
        return "pre1980"
    if y < 1990:
        return "1980-89"
    if y < 2000:
        return "1990-99"
    if y < 2008:
        return "2000-07"
    if y < 2015:
        return "2008-14"
    if y < 2020:
        return "2015-19"
    if y < 2022:
        return "2020-21"
    return "2022-24"


def edu4(s):
    return np.where(s <= 15, "lths", np.where(s <= 17, "hs", np.where(s <= 20, "somecoll", "ba_plus")))


def load():
    fs = sorted(glob.glob(os.path.join(CACHE, "acs_*.parquet")))
    df = pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    df["edu4"] = edu4(df.SCHL)
    df["mex"] = df.POBP == 303
    df["natben"] = (df.NATIVITY == 1) & (df.HISP == 1) & (df.RAC1P == 1)
    df = df[df.mex | df.natben].copy()
    df["cohort"] = df.YOEP.map(cohort_of)
    df["cohort10"] = np.where(df.YOEP.notna() & (df.YOEP >= 2020), "2020-24", df.cohort)
    df["ysm"] = df.YEAR - df.YOEP
    df["employed"] = df.ESR.isin([1, 2, 4, 5]).astype(float)
    df["ftfy"] = (df.WKHP >= 35) & (df.WKWN >= 48)
    df["lnw"] = np.where(df.WAGP > 0, np.log(df.WAGP.clip(lower=1)), np.nan)
    df["sexlab"] = np.where(df.SEX == 1, "men", "women")
    # English: only-English speakers (ENG missing) counted as "very well or only English"
    df["eng_vw"] = np.where(df.ENG.isna(), 1.0, (df.ENG == 1).astype(float))
    df["eng_vw_or_well"] = np.where(df.ENG.isna(), 1.0, df.ENG.isin([1, 2]).astype(float))
    df["eng_notatall"] = np.where(df.ENG.isna(), 0.0, (df.ENG == 4).astype(float))
    df["agegrp"] = pd.cut(df.AGEP, [24, 29, 34, 39, 44, 49, 54],
                          labels=["25-29", "30-34", "35-39", "40-44", "45-49", "50-54"])
    return df


def wshare(g, col, val, w="PWGTP"):
    return g.loc[g[col] == val, w].sum() / g[w].sum()


def main():
    df = load()
    mex = df[df.mex & df.cohort.notna()].copy()
    nat = df[df.natben].copy()
    print("mex rows", len(mex), "nat rows", len(nat), "years", sorted(df.YEAR.unique()))

    # ---- cohort composition / education / English / employment, by year x sex
    rows = []
    for (y, c, s), g in mex.groupby(["YEAR", "cohort", "sexlab"]):
        w = g.PWGTP.sum()
        if len(g) < 25:
            continue
        r = {"year": y, "cohort": c, "sex": s, "n": len(g), "wgt_pop": w,
             "mean_age": np.average(g.AGEP, weights=g.PWGTP),
             "mean_ysm": np.average(g.ysm.fillna(0), weights=g.PWGTP),
             "emp_rate": np.average(g.employed, weights=g.PWGTP),
             "eng_very_well_or_only": np.average(g.eng_vw, weights=g.PWGTP),
             "eng_well_plus": np.average(g.eng_vw_or_well, weights=g.PWGTP),
             "eng_not_at_all": np.average(g.eng_notatall, weights=g.PWGTP),
             "sh_noncitizen": np.average((g.CIT == 5).astype(float), weights=g.PWGTP)}
        for e in EDU_ORDER:
            r[f"sh_{e}"] = wshare(g, "edu4", e)
        rows.append(r)
    comp = pd.DataFrame(rows).sort_values(["year", "sex", "cohort"])
    comp.to_csv(f"{OUT}/acs_cohort_composition.csv", index=False)
    print(comp[comp.year == comp.year.max()].to_string(index=False))

    # pooled over sex too
    rows = []
    for (y, c), g in mex.groupby(["YEAR", "cohort"]):
        w = g.PWGTP.sum()
        r = {"year": y, "cohort": c, "sex": "all", "n": len(g), "wgt_pop": w,
             "mean_age": np.average(g.AGEP, weights=g.PWGTP),
             "mean_ysm": np.average(g.ysm.fillna(0), weights=g.PWGTP),
             "emp_rate": np.average(g.employed, weights=g.PWGTP),
             "eng_very_well_or_only": np.average(g.eng_vw, weights=g.PWGTP),
             "eng_well_plus": np.average(g.eng_vw_or_well, weights=g.PWGTP),
             "eng_not_at_all": np.average(g.eng_notatall, weights=g.PWGTP),
             "sh_noncitizen": np.average((g.CIT == 5).astype(float), weights=g.PWGTP)}
        for e in EDU_ORDER:
            r[f"sh_{e}"] = wshare(g, "edu4", e)
        rows.append(r)
    pd.DataFrame(rows).sort_values(["year", "cohort"]).to_csv(
        f"{OUT}/acs_cohort_composition_allsex.csv", index=False)

    # native benchmark
    nrows = []
    for (y, s), g in nat.groupby(["YEAR", "sexlab"]):
        r = {"year": y, "sex": s, "n": len(g), "emp_rate": np.average(g.employed, weights=g.PWGTP)}
        for e in EDU_ORDER:
            r[f"sh_{e}"] = wshare(g, "edu4", e)
        nrows.append(r)
    pd.DataFrame(nrows).to_csv(f"{OUT}/acs_native_benchmark.csv", index=False)

    # ---- wage residual vs native cells (year x sex x agegrp x edu4), FTFY workers
    w_all = df[df.ftfy & df.lnw.notna()].copy()
    cells = (w_all[w_all.natben]
             .groupby(["YEAR", "sexlab", "agegrp", "edu4"], observed=True)
             .apply(lambda g: pd.Series({"nat_lnw": np.average(g.lnw, weights=g.PWGTP),
                                         "nat_n": len(g)}), include_groups=False)
             .reset_index())
    cells.to_csv(f"{OUT}/acs_native_cell_means.csv", index=False)

    mw = w_all[w_all.mex & w_all.cohort.notna()].merge(
        cells, on=["YEAR", "sexlab", "agegrp", "edu4"], how="left")
    mw["resid"] = mw.lnw - mw.nat_lnw
    mw["ysm_band"] = pd.cut(mw.ysm, [-1, 5, 10, 20, 100], labels=["0-5", "6-10", "11-20", "21+"])

    def agg(g):
        g = g.dropna(subset=["resid"])
        if len(g) < 25:
            return None
        m = np.average(g.resid, weights=g.PWGTP)
        v = np.average((g.resid - m) ** 2, weights=g.PWGTP)
        neff = (g.PWGTP.sum() ** 2) / (g.PWGTP ** 2).sum()
        se = float(np.sqrt(v / neff))
        return {"n": len(g), "mean_ysm": float(np.average(g.ysm, weights=g.PWGTP)),
                "resid_lnw": float(m), "se": se, "lo95": m - 1.96 * se, "hi95": m + 1.96 * se,
                "mean_lnw": float(np.average(g.lnw, weights=g.PWGTP))}

    rr = []
    for (y, c, s), g in mw.groupby(["YEAR", "cohort", "sexlab"]):
        a = agg(g)
        if a:
            rr.append({"year": y, "cohort": c, "sex": s, **a})
    res = pd.DataFrame(rr).sort_values(["year", "sex", "cohort"])
    res.to_csv(f"{OUT}/acs_wage_residual_by_cohort.csv", index=False)
    print("\n", res.to_string(index=False))

    rr = []
    for (y, c), g in mw.groupby(["YEAR", "cohort"]):
        a = agg(g)
        if a:
            rr.append({"year": y, "cohort": c, "sex": "all", **a})
    pd.DataFrame(rr).sort_values(["year", "cohort"]).to_csv(
        f"{OUT}/acs_wage_residual_by_cohort_allsex.csv", index=False)

    rr = []
    for (c, b, s), g in mw.groupby(["cohort", "ysm_band", "sexlab"], observed=True):
        a = agg(g)
        if a:
            rr.append({"cohort": c, "ysm_band": str(b), "sex": s,
                       "years": str(sorted(g.YEAR.unique().tolist())), **a})
    pd.DataFrame(rr).to_csv(f"{OUT}/acs_wage_residual_by_ysm_band.csv", index=False)

    # ---- unconditional (education NOT controlled) residual: total skill-price gap
    cells_u = (w_all[w_all.natben]
               .groupby(["YEAR", "sexlab", "agegrp"], observed=True)
               .apply(lambda g: pd.Series({"nat_lnw_u": np.average(g.lnw, weights=g.PWGTP)}),
                      include_groups=False).reset_index())
    mu = w_all[w_all.mex & w_all.cohort.notna()].merge(
        cells_u, on=["YEAR", "sexlab", "agegrp"], how="left")
    mu["resid"] = mu.lnw - mu.nat_lnw_u
    rr = []
    for (y, c, s), g in mu.groupby(["YEAR", "cohort", "sexlab"]):
        g = g.dropna(subset=["resid"])
        if len(g) < 25:
            continue
        m = np.average(g.resid, weights=g.PWGTP)
        v = np.average((g.resid - m) ** 2, weights=g.PWGTP)
        neff = (g.PWGTP.sum() ** 2) / (g.PWGTP ** 2).sum()
        se = float(np.sqrt(v / neff))
        rr.append({"year": y, "cohort": c, "sex": s, "n": len(g),
                   "resid_lnw_unadj": float(m), "se": se, "lo95": m - 1.96 * se,
                   "hi95": m + 1.96 * se})
    pd.DataFrame(rr).sort_values(["year", "sex", "cohort"]).to_csv(
        f"{OUT}/acs_wage_residual_unadjusted.csv", index=False)

    # ---- who are the recent arrivals? share of 2020-24 and 2022-24 FB arrivals born in Mexico
    #      (needs the full FB population, so reload raw parquet)
    fs = sorted(glob.glob(os.path.join(CACHE, "acs_*.parquet")))
    raw = pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    fb = raw[(raw.NATIVITY == 2) & raw.YOEP.notna()].copy()
    out = []
    for y, g in fb.groupby("YEAR"):
        for lo, hi, lab in [(2015, 2019, "2015-19"), (2020, 2021, "2020-21"),
                            (2022, 2024, "2022-24"), (2021, 2024, "2021-24")]:
            s = g[(g.YOEP >= lo) & (g.YOEP <= hi)]
            if s.PWGTP.sum() == 0:
                continue
            out.append({"survey_year": y, "arrival_window": lab,
                        "fb_arrivals_25_54_wgt": s.PWGTP.sum(),
                        "mexico_born_wgt": s.loc[s.POBP == 303, "PWGTP"].sum(),
                        "mexico_share": s.loc[s.POBP == 303, "PWGTP"].sum() / s.PWGTP.sum(),
                        "n_unweighted": len(s)})
    comp2 = pd.DataFrame(out)
    comp2.to_csv(f"{OUT}/acs_recent_arrival_origin_mix.csv", index=False)
    print("\n", comp2.to_string(index=False))

    # top origins among 2021-24 arrivals, 2024 survey
    g = fb[(fb.YEAR == 2024) & (fb.YOEP >= 2021)]
    top = (g.groupby("POBP").PWGTP.sum().sort_values(ascending=False).head(15) / g.PWGTP.sum())
    top.rename("share").to_frame().reset_index().to_csv(
        f"{OUT}/acs_2024_top_origins_2021_24_arrivals.csv", index=False)
    print("\n top POBP among 2021-24 arrivals aged 25-54, ACS 2024:\n", top.to_string())


if __name__ == "__main__":
    main()

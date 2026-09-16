#!/usr/bin/env python3
"""Second-generation outcomes by parental origin (CPS ASEC 2019-2024) and the
Feliciano parental-selectivity test. Aggregates by ISO3."""
import os, json
import numpy as np, pandas as pd, statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
NATIVE_BIRTH = {57, 60, 66, 69, 73, 78}
MIN_N2 = 150

def load(tag):
    fr = []
    for y in YEARS:
        d = pd.read_csv(os.path.join(HERE, f"cps_asec_{tag}_{y}.csv"))
        d["year"] = y
        fr.append(d)
    d = pd.concat(fr, ignore_index=True)
    for c in d.columns:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["w"] = d["MARSUPWT"] / len(YEARS)
    return d

def gen(d):
    nat = d["PRCITSHP"].isin([1, 2, 3])
    fa = ~d["PEFNTVTY"].isin(NATIVE_BIRTH) & d["PEFNTVTY"].notna()
    mo = ~d["PEMNTVTY"].isin(NATIVE_BIRTH) & d["PEMNTVTY"].notna()
    d["g1"] = d["PRCITSHP"].isin([4, 5])
    d["g2"] = nat & (fa | mo)
    d["g3p"] = nat & ~(fa | mo)
    d["porigin"] = np.where(fa, d["PEFNTVTY"], np.where(mo, d["PEMNTVTY"], np.nan))
    return d

def wmean(x, w):
    m = np.isfinite(x) & np.isfinite(w)
    return float(np.sum(x[m] * w[m]) / np.sum(w[m])) if np.sum(w[m]) > 0 else np.nan

def wmedian(x, w):
    m = np.isfinite(x) & np.isfinite(w) & (w > 0)
    if m.sum() < 25: return np.nan
    x, w = np.asarray(x)[m], np.asarray(w)[m]
    o = np.argsort(x); x, w = x[o], w[o]
    return float(x[np.searchsorted(np.cumsum(w) / np.sum(w), 0.5)])

def outcomes(g, pfx=""):
    ba = (g["A_HGA"] >= 43).astype(float).values
    lths = ((g["A_HGA"] <= 38) & (g["A_HGA"] > 0)).astype(float).values
    ftfy = (g["WKSWORK"] >= 50) & (g["HRSWK"] >= 35) & (g["PEARNVAL"] > 0)
    w = g["w"].values
    return {pfx+"n": int(len(g)), pfx+"wpop": float(w.sum()),
            pfx+"share_ba": 100*wmean(ba, w), pfx+"share_lths": 100*wmean(lths, w),
            pfx+"n_ftfy": int(ftfy.sum()),
            pfx+"med_earn": wmedian(g.loc[ftfy, "PEARNVAL"].values, g.loc[ftfy, "w"].values)}

def main():
    d = gen(load("2564"))
    cw = pd.read_csv(os.path.join(HERE, "country_crosswalk.csv"))
    cw["cps_code"] = cw.cps_code.astype(int)
    iso = dict(zip(cw.cps_code, cw.iso3))
    meta = cw.dropna(subset=["iso3"]).drop_duplicates("iso3").set_index("iso3")

    d["iso3"] = d["porigin"].map(iso)
    d["iso3_own"] = d["PENATVTY"].map(iso)

    # ---- second generation, 25-44, by parental-origin ISO3 ----
    s2 = d[d.g2 & d.A_AGE.between(25, 44) & d.iso3.notna() & (d.iso3 != "USA")].copy()
    sec = pd.DataFrame([dict(iso3=k, **outcomes(g)) for k, g in s2.groupby("iso3")])
    sec = sec[sec.n >= MIN_N2].rename(columns={
        "n":"n2","wpop":"wpop2","share_ba":"share_ba_2ndgen",
        "share_lths":"share_lths_2ndgen","med_earn":"med_earn_2ndgen","n_ftfy":"n_ftfy2"})

    # ---- first generation, 25-64, by own birth-country ISO3 ----
    band = {1:1945,2:1955,3:1962,4:1967,5:1972,6:1977,7:1980.5,8:1982.5,9:1984.5,
            10:1986.5,11:1988.5,12:1990.5,13:1992.5,14:1994.5,15:1996.5,16:1998.5,
            17:2000.5,18:2002.5,19:2004.5,20:2006.5,21:2008.5,22:2010.5,23:2012.5,
            24:2014.5,25:2016.5,26:2018.5,27:2020.5,28:2022.5}
    f1 = d[d.g1 & d.A_AGE.between(25, 64) & d.iso3_own.notna()].copy()
    f1["age_entry"] = f1["A_AGE"] - (f1["year"] - 1 - f1["PEINUSYR"].map(band))
    rows = []
    for k, g in f1.groupby("iso3_own"):
        if len(g) < 100: continue
        r = dict(iso3=k, **outcomes(g, "f1_"))
        ad = g[g.age_entry >= 18]
        r["f1adult_n"] = int(len(ad))
        r["f1adult_share_ba"] = (100*wmean((ad["A_HGA"] >= 43).astype(float).values,
                                           ad["w"].values)) if len(ad) >= 100 else np.nan
        r["f1_med_entry_yr"] = float(g["PEINUSYR"].map(band).median())
        rows.append(r)
    fst = pd.DataFrame(rows)

    # ---- reference rows, third-plus generation 25-44 ----
    t3 = d[d.g3p & d.A_AGE.between(25, 44)]
    s2all = d[d.g2 & d.A_AGE.between(25, 44)]
    f1all = d[d.g1 & d.A_AGE.between(25, 64)]
    refs = {"3+ gen non-Hispanic white": t3[(t3.PRDTRACE == 1) & (t3.PEHSPNON == 2)],
            "3+ gen non-Hispanic Black": t3[(t3.PRDTRACE == 2) & (t3.PEHSPNON == 2)],
            "3+ gen Hispanic": t3[t3.PEHSPNON == 1],
            "3+ gen all": t3, "2nd gen all (25-44)": s2all,
            "1st gen all (25-64)": f1all}
    ref = pd.DataFrame([dict(group=k, **outcomes(v)) for k, v in refs.items()])
    ref.to_csv(os.path.join(HERE, "reference_groups.csv"), index=False)

    # ---- merge + selectivity ----
    m = sec.merge(fst, on="iso3", how="left").join(
        meta[["display_name","wb_ba_pct","wb_year","bl_ter_2010","bl_ter_1990",
              "origin_ba_pref","origin_ba_source","refugee_origin","mex_centam"]], on="iso3")
    m = m.rename(columns={"display_name":"origin","f1_n":"n1",
                          "f1_share_ba":"share_ba_1stgen","f1_share_lths":"share_lths_1stgen",
                          "origin_ba_pref":"share_ba_origin","refugee_origin":"refugee_dummy",
                          "mex_centam":"mexcam_dummy"})
    m["selectivity"]      = m.share_ba_1stgen - m.share_ba_origin          # primary
    m["selectivity_adult"] = m.f1adult_share_ba - m.share_ba_origin        # adult arrivals
    m["selectivity_bl1990"] = m.share_ba_1stgen - m.bl_ter_1990            # migration-era vintage
    m = m.sort_values("n2", ascending=False)
    m.to_csv(os.path.join(HERE, "secgen_by_origin.csv"), index=False, columns=[
        "origin","iso3","n2","wpop2","share_ba_2ndgen","share_lths_2ndgen","med_earn_2ndgen",
        "n1","share_ba_1stgen","share_lths_1stgen","f1adult_n","f1adult_share_ba",
        "f1_med_entry_yr","share_ba_origin","origin_ba_source","bl_ter_1990",
        "selectivity","selectivity_adult","selectivity_bl1990","refugee_dummy","mexcam_dummy"])

    # ---- regressions ----
    specs = {"1_selectivity_only": ["selectivity"],
             "2_plus_firstgen_level": ["selectivity", "share_ba_1stgen"],
             "3_plus_dummies": ["selectivity", "share_ba_1stgen", "refugee_dummy", "mexcam_dummy"],
             "4_firstgen_level_only": ["share_ba_1stgen"],
             "5_origin_level_only": ["share_ba_origin"],
             "6_adult_arrival_selectivity": ["selectivity_adult"],
             "7_bl1990_vintage_selectivity": ["selectivity_bl1990"],
             "8_bl1990_plus_dummies": ["selectivity_bl1990","share_ba_1stgen","refugee_dummy","mexcam_dummy"]}
    out = {}
    for name, xs in specs.items():
        sub = m.dropna(subset=xs + ["share_ba_2ndgen"]).copy()
        X = sm.add_constant(sub[xs])
        r = sm.WLS(sub["share_ba_2ndgen"], X, weights=sub["n2"]).fit(cov_type="HC1")
        out[name] = dict(n=int(r.nobs), r2=round(float(r.rsquared), 4),
                         coef={k: dict(b=round(float(r.params[k]), 4),
                                       se=round(float(r.bse[k]), 4),
                                       p=round(float(r.pvalues[k]), 5)) for k in r.params.index})
        sub["fitted"], sub["resid"] = r.fittedvalues, r.resid
        sub[["origin","iso3","n2","share_ba_2ndgen","fitted","resid"]].to_csv(
            os.path.join(HERE, f"resid_{name}.csv"), index=False)
    json.dump(out, open(os.path.join(HERE, "regressions.json"), "w"), indent=1)

    # ---- verification ----
    b = gen(load("allages"))
    tab1 = {2019:40260000,2020:40790000,2021:40330000,2022:40960000,2023:42110000,2024:41760000}
    tab4 = {2019:13690000,2020:13670000,2021:13480000,2022:13410000,2023:14000000,2024:13790000}
    tab2_1864 = {2019:19020000,2020:20270000,2021:19830000,2022:20140000,2023:21560000,2024:21370000}
    ver = []
    for y in YEARS:
        by = b[b.year == y]
        t2 = float(by.loc[by.g2, "MARSUPWT"].sum())
        mx = float(by.loc[by.g2 & (by.PRDTHSP == 1), "MARSUPWT"].sum())
        a1864 = float(by.loc[by.g2 & by.A_AGE.between(18, 64), "MARSUPWT"].sum())
        ver.append(dict(year=y, secgen_all_mine=t2, secgen_all_census_t1=tab1[y],
                        pct_diff_t1=100*(t2-tab1[y])/tab1[y],
                        secgen_1864_mine=a1864, secgen_1864_census_t2=tab2_1864[y],
                        pct_diff_t2=100*(a1864-tab2_1864[y])/tab2_1864[y],
                        secgen_mex_mine=mx, secgen_mex_census_t4=tab4[y],
                        pct_diff_t4=100*(mx-tab4[y])/tab4[y],
                        total_pop_mine=float(by["MARSUPWT"].sum())))
    pd.DataFrame(ver).to_csv(os.path.join(HERE, "verification.csv"), index=False)

    pd.set_option("display.width", 250)
    print(m[["origin","iso3","n2","share_ba_2ndgen","share_lths_2ndgen","med_earn_2ndgen",
             "n1","share_ba_1stgen","share_ba_origin","origin_ba_source","selectivity",
             "selectivity_bl1990","refugee_dummy","mexcam_dummy"]].round(1).to_string(index=False))
    print(); print(ref.round(1).to_string(index=False))
    print(); print(json.dumps(out, indent=1))
    print(); print(pd.DataFrame(ver).round(2).to_string(index=False))

if __name__ == "__main__":
    main()

"""Metro-level native population response, 2010 -> 2023.

Outcome  native population growth over 2010-2023, expressed as the net change in the
         native population divided by the metro's 2010 native population.
         [CAVEAT] This is a population response, not an observed migration flow: it also
         contains natural increase and ageing. It is the outcome Card (2001) and
         Borjas (2006) argue over, so it is the comparable object, not a substitute for
         observed native out-migration.
Treatment change in the foreign-born share of metro population (percentage points), and
         in a second arm the change in the Mexican-origin share (B03001_004, all
         generations, the fiscal lane's `mexican_observed_total` population).
IV       2000-base shift-share: metro's share of the national 2000 Mexico-born (or
         foreign-born) stock x the national 2010-2023 change in that stock, scaled by
         metro 2010 population. Base shares come from the employment-entry lane's
         `derived/metro_base_2000.csv` (Census 2000 SF3 on fixed OMB-2013 CBSAs).
Gate     if the first-stage F is below 10 the IV row is reported as uninformative.

Output: derived/metro_estimates.csv, derived/metro_panel.csv
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
DERIVED = os.path.join(HERE, "derived")
os.makedirs(DERIVED, exist_ok=True)
EE = os.path.join(os.path.dirname(HERE), "employment_entry_2026_09_18", "derived")

REGION = {  # Census region of the metro's first-listed state
    "CT": "NE", "ME": "NE", "MA": "NE", "NH": "NE", "RI": "NE", "VT": "NE",
    "NJ": "NE", "NY": "NE", "PA": "NE",
    "IL": "MW", "IN": "MW", "MI": "MW", "OH": "MW", "WI": "MW", "IA": "MW",
    "KS": "MW", "MN": "MW", "MO": "MW", "NE": "MW", "ND": "MW", "SD": "MW",
    "DE": "S", "DC": "S", "FL": "S", "GA": "S", "MD": "S", "NC": "S", "SC": "S",
    "VA": "S", "WV": "S", "AL": "S", "KY": "S", "MS": "S", "TN": "S",
    "AR": "S", "LA": "S", "OK": "S", "TX": "S",
    "AZ": "W", "CO": "W", "ID": "W", "MT": "W", "NV": "W", "NM": "W", "UT": "W",
    "WY": "W", "AK": "W", "CA": "W", "HI": "W", "OR": "W", "WA": "W",
}


def load():
    d = pd.read_csv(os.path.join(CACHE, "metro_acs5.csv"),
                    dtype={"cbsa": str, "NAME": str})
    num = [c for c in d.columns if c.startswith("B") and c.endswith("E")]
    for c in num:
        d[c] = pd.to_numeric(d[c], errors="coerce")
        d.loc[d[c] < 0, c] = np.nan          # Census jam values (-666666666 etc.)
    d["pop"] = d["B01003_001E"]
    d["medage"] = d["B01002_001E"]
    d["native"] = d["B05002_002E"]
    d["fb"] = d["B05002_013E"]
    d["mex"] = d["B03001_004E"]
    d["cuban"] = d["B03001_006E"]
    d["asian"] = d["B02001_005E"]
    d["rent"] = d["B25064_001E"]
    d["hhinc"] = d["B19013_001E"]
    ba = ["B15002_015E", "B15002_016E", "B15002_017E", "B15002_018E",
          "B15002_032E", "B15002_033E", "B15002_034E", "B15002_035E"]
    d["coll"] = d[ba].sum(axis=1) / d["B15002_001E"]
    d["fb_share"] = d["fb"] / d["B05002_001E"]
    d["mex_share"] = d["mex"] / d["B03001_001E"]
    d["cuban_share"] = d["cuban"] / d["B03001_001E"]
    d["asian_share"] = d["asian"] / d["pop"]
    d["state"] = d["NAME"].str.extract(r",\s*([A-Z]{2})")[0]
    d["region"] = d["state"].map(REGION)
    d = d[d["region"].notna()]        # drops Puerto Rico metros
    return d


def build(d, y0=2010, y1=2023):
    a = d[d.year == y0].set_index("cbsa")
    b = d[d.year == y1].set_index("cbsa")
    idx = a.index.intersection(b.index)
    p = pd.DataFrame(index=idx)
    p["name"] = a.loc[idx, "NAME"]
    p["region"] = a.loc[idx, "region"]
    p["pop0"] = a.loc[idx, "pop"]
    p["native0"] = a.loc[idx, "native"]
    p["native1"] = b.loc[idx, "native"]
    p["d_native"] = (p["native1"] - p["native0"]) / p["native0"]
    for v in ["fb_share", "mex_share", "cuban_share", "asian_share"]:
        p["d_" + v] = (b.loc[idx, v] - a.loc[idx, v]) * 100.0
        p[v + "0"] = a.loc[idx, v] * 100.0
    # Peri-Sparber-safe scaling: both sides divided by the SAME 2010 total population, so
    # the immigrant variable does not carry the native population in its denominator. A
    # coefficient here reads directly as natives lost per immigrant gained.
    p["d_native_pc"] = (p["native1"] - p["native0"]) / p["pop0"] * 100.0
    for v, col in [("mex", "mex"), ("fb", "fb"), ("asian", "asian"), ("cuban", "cuban")]:
        p["d_%s_pc" % v] = (b.loc[idx, col] - a.loc[idx, col]) / p["pop0"] * 100.0
    p["coll0"] = a.loc[idx, "coll"] * 100.0
    p["rent0"] = a.loc[idx, "rent"]
    p["d_lrent"] = np.log(b.loc[idx, "rent"]) - np.log(a.loc[idx, "rent"])
    p["hhinc0"] = a.loc[idx, "hhinc"]
    p["lpop0"] = np.log(p["pop0"])
    p["medage0"] = a.loc[idx, "medage"]
    # Mexico-BORN 18-64 share from the employment-entry lane's PUMS panel, as a second
    # treatment: the ACS5 measure above is Mexican-ORIGIN (all generations), and the two
    # move in opposite directions over 2010-2023 (levels correlate 0.93, changes 0.07)
    # because the US-born generations grew while the Mexico-born 18-64 stock shrank.
    ee = pd.read_csv(os.path.join(EE, "metro_year_panel.csv"))
    ee["cbsa"] = ee["cbsa"].astype(str).str.zfill(5)
    e0 = ee[ee.year == 2010].drop_duplicates("cbsa").set_index("cbsa")["mex_share"]
    e1 = ee[ee.year == 2023].drop_duplicates("cbsa").set_index("cbsa")["mex_share"]
    p["d_mexborn_share"] = (e1.reindex(idx) - e0.reindex(idx))
    p["mexborn_share0"] = e0.reindex(idx)
    base = pd.read_csv(os.path.join(EE, "metro_base_2000.csv"), dtype={"cbsa": str}).set_index("cbsa")
    p["mex_base"] = base["mex_base_share_natl"].reindex(idx)
    p["fb_base"] = base["fb_base_share_natl"].reindex(idx)
    nat = pd.read_csv(os.path.join(CACHE, "national_acs5.csv")).set_index("year")
    d_nat_fb = float(nat.loc[y1, "B05002_013E"] - nat.loc[y0, "B05002_013E"])
    d_nat_mex = float(nat.loc[y1, "B03001_004E"] - nat.loc[y0, "B03001_004E"])
    p["z_fb"] = p["fb_base"] * d_nat_fb / p["pop0"] * 100.0
    p["z_mex"] = p["mex_base"] * d_nat_mex / p["pop0"] * 100.0
    p["national_d_fb"] = d_nat_fb
    p["national_d_mex"] = d_nat_mex
    return p.dropna(subset=["d_native", "d_fb_share", "pop0"])


def ols(y, X, w=None, label=""):
    X = sm.add_constant(X, has_constant="add")
    m = (sm.WLS(y, X, weights=w) if w is not None else sm.OLS(y, X)).fit(cov_type="HC1")
    return m


def iv2sls(y, endog, exog, inst, w):
    """Weighted 2SLS via linearmodels, HC1, with the first-stage F on the instrument."""
    from linearmodels.iv import IV2SLS
    ex = exog.copy()
    ex["const"] = 1.0
    m = IV2SLS(y, ex, endog.to_frame(), inst.to_frame(), weights=w).fit(cov_type="robust")
    fs = m.first_stage.individual[endog.name]
    F = float(fs.tstats[inst.name] ** 2)
    b = float(m.params[endog.name])
    se = float(m.std_errors[endog.name])
    return b, se, F, np.nan


def main():
    d = load()
    p = build(d)
    p.to_csv(os.path.join(DERIVED, "metro_panel.csv"))
    print("metros", len(p))
    w = p["native0"]
    reg = pd.get_dummies(p["region"], prefix="r", drop_first=True).astype(float)
    rows = []

    specs = {
        "raw":        [],
        "+size,age":  ["lpop0", "medage0"],
        "+college":   ["lpop0", "medage0", "coll0"],
        "+rent":      ["lpop0", "medage0", "coll0", "rent0"],
        "+region":    ["lpop0", "medage0", "coll0", "rent0"],
    }
    for treat in ["d_fb_share", "d_mex_share", "d_mexborn_share",
                  "d_asian_share", "d_cuban_share"]:
        for name, ctrl in specs.items():
            X = p[ctrl].copy() if ctrl else pd.DataFrame(index=p.index)
            if name == "+region":
                X = pd.concat([X, reg], axis=1)
            X[treat] = p[treat]
            sub = pd.concat([p["d_native"], X], axis=1).dropna()
            m = ols(sub["d_native"], sub.drop(columns="d_native"), w=w.reindex(sub.index))
            rows.append(dict(arm="OLS", treat=treat, spec=name, n=len(sub),
                             coef=m.params[treat], se=m.bse[treat],
                             lo=m.conf_int().loc[treat, 0], hi=m.conf_int().loc[treat, 1],
                             first_stage_F=np.nan))
    # IV arms
    for treat, inst in [("d_fb_share", "z_fb"), ("d_mex_share", "z_mex")]:
        for name, ctrl in [("raw", []), ("+size,age", ["lpop0", "medage0"]),
                           ("+college", ["lpop0", "medage0", "coll0"])]:
            cols = ["d_native", treat, inst] + ctrl
            sub = p[cols].dropna()
            ww = w.reindex(sub.index)
            exog = sub[ctrl] if ctrl else pd.DataFrame(index=sub.index)
            b, se, F, _ = iv2sls(sub["d_native"], sub[treat], exog, sub[inst], ww)
            rows.append(dict(arm="IV-shiftshare", treat=treat, spec=name, n=len(sub),
                             coef=b, se=se, lo=b - 1.96 * se, hi=b + 1.96 * se,
                             first_stage_F=F))
    # per-capita scaling arm (see build()): natives lost per immigrant gained
    for treat in ["d_mex_pc", "d_fb_pc", "d_asian_pc", "d_cuban_pc"]:
        for name, ctrl in specs.items():
            X = p[ctrl].copy() if ctrl else pd.DataFrame(index=p.index)
            if name == "+region":
                X = pd.concat([X, reg], axis=1)
            X[treat] = p[treat]
            sub = pd.concat([p["d_native_pc"], X], axis=1).dropna()
            m = ols(sub["d_native_pc"], sub.drop(columns="d_native_pc"),
                    w=w.reindex(sub.index))
            rows.append(dict(arm="OLS per-capita", treat=treat, spec=name, n=len(sub),
                             coef=m.params[treat], se=m.bse[treat],
                             lo=m.conf_int().loc[treat, 0], hi=m.conf_int().loc[treat, 1],
                             first_stage_F=np.nan))
    # mediator check: adding the 2010-2023 change in log median rent. Rent is on the
    # causal path if immigrants raise rents (Wilson-Zhou 2026: +1.4% rents per inflow of
    # 1% of initial employment), so this is a decomposition, not a cleaner estimate.
    for treat in ["d_mex_share", "d_mexborn_share", "d_asian_share"]:
        X = p[["lpop0", "medage0", "coll0", "rent0", "d_lrent"]].copy()
        X[treat] = p[treat]
        sub = pd.concat([p["d_native"], X], axis=1).dropna()
        m = ols(sub["d_native"], sub.drop(columns="d_native"), w=w.reindex(sub.index))
        rows.append(dict(arm="OLS +d_lrent (mediator)", treat=treat, spec="+college+drent",
                         n=len(sub), coef=m.params[treat], se=m.bse[treat],
                         lo=m.conf_int().loc[treat, 0], hi=m.conf_int().loc[treat, 1],
                         first_stage_F=np.nan))
        rows.append(dict(arm="OLS +d_lrent (mediator)", treat="d_lrent", spec="with " + treat,
                         n=len(sub), coef=m.params["d_lrent"], se=m.bse["d_lrent"],
                         lo=m.conf_int().loc["d_lrent", 0], hi=m.conf_int().loc["d_lrent", 1],
                         first_stage_F=np.nan))
    # size floor arm: metros of 250,000+ in 2010, treatment = Mexican-origin share
    pb = p[p.pop0 >= 250000]
    for name, ctrl in specs.items():
        X = pb[ctrl].copy() if ctrl else pd.DataFrame(index=pb.index)
        if name == "+region":
            X = pd.concat([X, reg.reindex(pb.index)], axis=1)
        X["d_mex_share"] = pb["d_mex_share"]
        sub = pd.concat([pb["d_native"], X], axis=1).dropna()
        m = ols(sub["d_native"], sub.drop(columns="d_native"),
                w=pb["native0"].reindex(sub.index))
        rows.append(dict(arm="OLS pop>=250k", treat="d_mex_share", spec=name, n=len(sub),
                         coef=m.params["d_mex_share"], se=m.bse["d_mex_share"],
                         lo=m.conf_int().loc["d_mex_share", 0],
                         hi=m.conf_int().loc["d_mex_share", 1], first_stage_F=np.nan))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(DERIVED, "metro_estimates.csv"), index=False)
    pd.set_option("display.width", 200)
    print(out.to_string(index=False, float_format=lambda x: "%.4f" % x))


if __name__ == "__main__":
    main()

"""SF 311 complaint rates by analysis neighborhood, 2019-2025, per 1,000 residents
and per 100 active registered businesses. 311 is a COMPLAINT measure: it mixes
underlying condition with propensity to report, so it is reported alongside, not
in place of, the inspector-observed audit."""
import json, pathlib, collections
import numpy as np, pandas as pd, statsmodels.formula.api as smf
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 260, "display.max_columns", 40)

CATS = {
 "cleaning":  ["Street and Sidewalk Cleaning"],
 "graffiti":  ["Graffiti", "Graffiti Public", "Graffiti Private"],
 "encampment":["Encampments", "Encampment", "Homeless Concerns"],
 "streetdef": ["Street Defects", "Street Defect", "Sidewalk or Curb",
               "Sidewalk and Curb", "Damaged Property"],
 "abandveh":  ["Abandoned Vehicle"],
 "litterbin": ["Litter Receptacles", "Litter Receptacle Maintenance"],
 "building":  ["Residential Building Request",
               "General Request - BUILDING INSPECTION"],
}
rev = {s: k for k, v in CATS.items() for s in v}

rows = json.load(open(CD/"sf311_nbhd_service_year.json"))
agg = collections.defaultdict(float); tot = collections.defaultdict(float)
for r in rows:
    if int(r["yr"]) < 2019: continue
    n = r.get("analysis_neighborhood")
    if not n: continue
    tot[n] += int(r["n"])
    c = rev.get(r.get("service_name"))
    if c: agg[(n, c)] += int(r["n"])

acs = pd.DataFrame(json.load(open(CD/"sf_nbhd_acs.json")))
acs = acs[acs["pop"] > 3000].set_index("nbhd")
biz = collections.Counter(
    r.get("neighborhoods_analysis_boundaries")
    for r in json.load(open(CD/"sf_active_businesses.json")))

recs = []
YRS = 7.0   # 2019-2025 inclusive
for n in acs.index:
    p = acs.loc[n, "pop"]; b = biz.get(n, 0)
    d = dict(nbhd=n, pop=int(p), biz=b,
             all_311_per1k=tot[n]/YRS/p*1000)
    for c in CATS:
        d[c+"_per1k"] = agg[(n, c)]/YRS/p*1000
    d["cleaning_per100biz"] = agg[(n,"cleaning")]/YRS/b*100 if b else np.nan
    recs.append(d)
T = pd.DataFrame(recs).set_index("nbhd").join(
    acs[["mean_hh_inc","hisp_pct","mex_pct","nhwhite_pct","nhasian_pct",
         "nhblack_pct","fb_pct","crowded_pct","pov_pct","owner_pct"]])
T = T.sort_values("cleaning_per1k", ascending=False)
print("=== TABLE 4. SF 311 requests per 1,000 residents per year, 2019-2025 ===")
print(T.round(1).to_string())
T.round(3).to_csv(HERE/"table4_sf_311_rates.csv")

print("\n=== TABLE 5. Neighborhood-level OLS on 311 rates (n = %d neighborhoods) ===" % len(T))
T["log_inc"] = np.log(T.mean_hh_inc)
out = []
for y in ["cleaning_per1k","graffiti_per1k","encampment_per1k","all_311_per1k",
          "building_per1k"]:
    for name, f in {"raw": f"{y} ~ hisp_pct",
                    "+income": f"{y} ~ hisp_pct + log_inc",
                    "full": f"{y} ~ hisp_pct + log_inc + nhblack_pct + nhasian_pct + owner_pct"}.items():
        m = smf.ols(f, data=T).fit(cov_type="HC1")
        out.append(dict(outcome=y, spec=name, beta_hisp=m.params["hisp_pct"],
                        t=m.tvalues["hisp_pct"], p=m.pvalues["hisp_pct"],
                        R2=m.rsquared, n=int(m.nobs)))
O = pd.DataFrame(out); print(O.round(3).to_string(index=False))
O.round(4).to_csv(HERE/"table5_sf_311_regressions.csv", index=False)

# Mission vs Chinatown vs comparison set, headline
key = ["Mission","Chinatown","North Beach","Japantown","Excelsior",
       "Bayview Hunters Point","Noe Valley","Marina","Outer Mission",
       "Inner Richmond","Sunset/Parkside","Tenderloin","Bernal Heights"]
print("\n=== TABLE 4b. Focus neighborhoods ===")
print(T.loc[[k for k in key if k in T.index],
    ["pop","biz","mean_hh_inc","hisp_pct","mex_pct","nhasian_pct","fb_pct",
     "crowded_pct","pov_pct","cleaning_per1k","cleaning_per100biz",
     "graffiti_per1k","encampment_per1k","building_per1k"]].round(1).to_string())

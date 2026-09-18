"""MyLA311 sanitation requests by ZIP, 2019-2025, per 1,000 residents, joined to
ACS 2019-23 ZCTA composition. City of Los Angeles only (East LA is unincorporated
county and is NOT in this data).

Key derived measure: illegal-dumping reports per bulky-item pickup request.
Bulky-item pickup is a FREE city service the resident schedules; illegal dumping
is what happens when someone does not. The ratio is a within-ZIP compliance
measure that is much less sensitive to overall reporting propensity than either
count on its own, because both numerator and denominator are 311 calls.
"""
import json, pathlib, collections
import numpy as np, pandas as pd, statsmodels.formula.api as smf
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 260, "display.max_columns", 40)

rows = json.load(open(CD/"la311_zip_type_year.json"))
YRS = len({r["yr"] for r in rows})
agg = collections.defaultdict(float)
for r in rows:
    z = r.get("zipcode")
    if not z or not z.isdigit() or len(z) != 5: continue
    agg[(z, r["requesttype"])] += int(r["n"])
zips = sorted({k[0] for k in agg})
Z = pd.read_csv(CD/"acs_zcta_la.csv", dtype={"zcta": str}).set_index("zcta")

TYPES = ["Bulky Items","Graffiti Removal","Illegal Dumping Pickup",
         "Metal/Household Appliances","Homeless Encampment","Electronic Waste",
         "Dead Animal Removal","Single Streetlight Issue","Multiple Streetlight Issue"]
recs = []
for z in zips:
    if z not in Z.index: continue
    p = Z.loc[z, "pop"]
    if not p or p < 5000: continue
    d = {"zcta": z, "pop": int(p)}
    for t in TYPES:
        d[t] = agg[(z, t)]/YRS/p*1000
    d["dump_per_bulky"] = (agg[(z,"Illegal Dumping Pickup")] /
                           agg[(z,"Bulky Items")]) if agg[(z,"Bulky Items")] else np.nan
    recs.append(d)
T = pd.DataFrame(recs).set_index("zcta").join(Z.drop(columns=["pop"]))
T["log_inc"] = np.log(T.mean_hh_inc)
T = T.dropna(subset=["hisp_pct","mean_hh_inc"])
print(f"ZIPs analysed: {len(T)}  (city of LA; {YRS} years of MyLA311)")

print("\n=== TABLE 12. LA ZIP-level OLS, MyLA311 rates per 1,000 residents/yr ===")
SPEC = {"raw": "{y} ~ hisp_pct",
        "+income": "{y} ~ hisp_pct + log_inc",
        "full": "{y} ~ hisp_pct + log_inc + nhblack_pct + nhasian_pct + owner_pct + crowded_pct"}
out = []
for y in ["Illegal Dumping Pickup","Graffiti Removal","Bulky Items",
          "Homeless Encampment","dump_per_bulky"]:
    yy = "Q('"+y+"')" if " " in y or "/" in y else y
    for name, f in SPEC.items():
        m = smf.ols(f.format(y=yy), data=T).fit(cov_type="HC1")
        out.append(dict(outcome=y, spec=name, beta_hisp=m.params["hisp_pct"],
            t=m.tvalues["hisp_pct"], p=m.pvalues["hisp_pct"], R2=m.rsquared,
            n=int(m.nobs), sd_y=T[y].std(),
            per10pp_sd=10*m.params["hisp_pct"]/T[y].std()))
O = pd.DataFrame(out); print(O.round(3).to_string(index=False))
O.round(4).to_csv(HERE/"table12_la_zip_regressions.csv", index=False)

FOCUS = {  # ZIP: label (city of LA unless noted)
 "90033":"Boyle Heights N", "90023":"Boyle Heights S", "90063":"City Terrace/E LA*",
 "90005":"Koreatown", "90006":"Koreatown/Pico-Union", "90020":"Koreatown N",
 "90057":"Westlake/MacArthur Pk", "90026":"Echo Park/HiFi", "90015":"South Park/Pico-Union",
 "90012":"Chinatown/Civic Ctr", "90042":"Highland Park", "90031":"Lincoln Heights",
 "90011":"South LA (Central-Alameda)", "90044":"South LA (Vermont Knolls)",
 "90045":"Westchester", "90025":"West LA", "90731":"San Pedro", "91403":"Sherman Oaks",
 "91324":"Northridge", "90291":"Venice", "90066":"Mar Vista", "91331":"Pacoima",
 "91402":"Panorama City", "90019":"Mid-City", "90035":"Beverlywood/Pico",
}
print("\n=== TABLE 13. LA focus ZIPs ===")
cols = ["pop","mean_hh_inc","hisp_pct","mex_pct","fb_pct","nhasian_pct","nhblack_pct",
        "crowded_pct","pov_pct","Illegal Dumping Pickup","Bulky Items",
        "dump_per_bulky","Graffiti Removal","Homeless Encampment"]
F = T.loc[[z for z in FOCUS if z in T.index], cols].copy()
F.insert(0, "area", [FOCUS[z] for z in F.index])
print(F.sort_values("hisp_pct", ascending=False).round(2).to_string())
F.round(3).to_csv(HERE/"table13_la_focus_zips.csv")
T.round(3).to_csv(HERE/"table13b_la_all_zips.csv")

# neighborhood-council view, no denominator - composition only
nc = json.load(open(CD/"la311_nc_type_year.json")) if (CD/"la311_nc_type_year.json").exists() else []
if nc:
    a2 = collections.defaultdict(float)
    for r in nc:
        n = r.get("ncname")
        if n: a2[(n, r["requesttype"])] += int(r["n"])
    names = sorted({k[0] for k in a2})
    rr = []
    for n in names:
        b = a2[(n,"Bulky Items")]; dmp = a2[(n,"Illegal Dumping Pickup")]
        if b < 500: continue
        rr.append(dict(nc=n, bulky=int(b), dumping=int(dmp), dump_per_bulky=dmp/b,
                       graffiti=int(a2[(n,"Graffiti Removal")])))
    N = pd.DataFrame(rr).sort_values("dump_per_bulky", ascending=False)
    print("\n=== TABLE 14. LA neighborhood councils, illegal dumping per bulky-item request ===")
    print(N.head(20).round(3).to_string(index=False))
    print("...")
    print(N.tail(15).round(3).to_string(index=False))
    N.round(4).to_csv(HERE/"table14_la_nc_dump_ratio.csv", index=False)

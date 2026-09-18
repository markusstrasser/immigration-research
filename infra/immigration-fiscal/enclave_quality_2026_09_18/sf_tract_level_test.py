"""H1 at the census-tract level, which removes most of the aggregation problem.

The Controller publishes a route-centroid coordinate crosswalk as an attachment to
`qya8-uhsz`. Joining it point-in-polygon to 2020 census tracts lets each audited
blockface carry the composition and income of its own tract rather than a
neighborhood-group mean, giving roughly 200 units of variation instead of 24.
"""
import json, pathlib, collections
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
from shapely.ops import transform

HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 250, "display.max_columns", 50)

# ---- tract polygons ----
xw = json.load(open(CD/"sf_tract_nbhd_2020.json"))
polys, geoids, nhoods = [], [], []
for r in xw:
    if not r.get("the_geom") or not r.get("geoid"): continue
    polys.append(shape(r["the_geom"])); geoids.append(r["geoid"])
    nhoods.append(r["neighborhoods_analysis_boundaries"])
tree = STRtree(polys)
LAT0 = 37.76
mla, mlo = 111320.0, 111320.0*np.cos(np.radians(LAT0))
area_km2 = {g: transform(lambda x, y: (x*mlo, y*mla), p).area/1e6
            for g, p in zip(geoids, polys)}

def locate(lon, lat):
    pt = Point(lon, lat)
    for i in tree.query(pt):
        if polys[i].contains(pt): return geoids[i], nhoods[i]
    # fall back to nearest polygon centroid for points on a boundary
    d = [(pt.distance(p), i) for i, p in enumerate(polys)]
    _, i = min(d)
    return geoids[i], nhoods[i]

# ---- tract ACS ----
acs = json.load(open(CD/"acs_sf_tracts_2023.json"))
def f(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return np.nan
    return np.nan if x < 0 else x
T = {}
for g, rec in acs.items():
    pop = f(rec.get("B01003_001E")); hh = f(rec.get("B11001_001E"))
    occ = f(rec.get("B25014_001E"))
    if not pop or pop < 200 or not hh or hh < 50: continue
    crowd = sum(f(rec.get(k)) or 0 for k in
        ["B25014_005E","B25014_006E","B25014_007E","B25014_011E","B25014_012E","B25014_013E"])
    T[g] = dict(
        t_pop=pop, t_hh=hh,
        t_inc=(f(rec.get("B19025_001E")) or np.nan)/hh,
        t_hisp=100*(f(rec.get("B03003_003E")) or 0)/pop,
        t_mex=100*(f(rec.get("B03001_004E")) or 0)/pop,
        t_asian=100*(f(rec.get("B03002_006E")) or 0)/pop,
        t_black=100*(f(rec.get("B03002_004E")) or 0)/pop,
        t_white=100*(f(rec.get("B03002_003E")) or 0)/pop,
        t_fb=100*(f(rec.get("B05002_013E")) or 0)/pop,
        t_owner=100*(f(rec.get("B25003_002E")) or 0)/(f(rec.get("B25003_001E")) or np.nan),
        t_crowd=100*crowd/occ if occ else np.nan,
        t_pov=100*(f(rec.get("B17001_002E")) or 0)/(f(rec.get("B17001_001E")) or np.nan),
        t_pre1940=100*(f(rec.get("B25034_011E")) or 0)/(f(rec.get("B25034_001E")) or np.nan),
        t_area=area_km2.get(g, np.nan))
print("tracts with usable ACS:", len(T))

# ---- street homelessness by tract ----
tents = json.load(open(CD/"sf_tents.json"))
nq = len({t["observed_month"][:7] for t in tents})
hom = collections.defaultdict(float)
for t in tents:
    try: lon, lat = float(t["longitude"]), float(t["latitude"])
    except Exception: continue
    g, _ = locate(lon, lat)
    hom[g] += sum(float(t.get(k) or 0) for k in
                  ("tents","structures","passenger_vehicles","other_vehicles"))
print("tent-count quarters:", nq)

# ---- routes -> tracts ----
cw = pd.read_excel(CD/"route_coords.xlsx", sheet_name="Crosswalk")
cw.columns = ["route_id", "route_location", "lon", "lat"]
cw["route_id"] = cw.route_id.astype(str).str.strip()
loc = {}
for r in cw.itertuples():
    if pd.isna(r.lon) or pd.isna(r.lat): continue
    loc[r.route_id] = locate(r.lon, r.lat)
print("routes with coordinates:", len(loc))

ev = pd.DataFrame(json.load(open(CD/"sf_street_eval_2022_2025.json")))
ev["route_id"] = ev.route_id.astype(str).str.strip()
ev["geoid"] = ev.route_id.map(lambda r: loc.get(r, (None, None))[0])
print(f"evaluations: {len(ev)}; matched to a tract: {ev.geoid.notna().sum()} "
      f"({100*ev.geoid.notna().mean():.1f}%)")

num = lambda s: pd.to_numeric(ev[s], errors="coerce")
ev["sidewalk_litter"] = num("select_the_statement_that_1")
ev["street_litter"]   = num("select_the_statement_that")
ev["litter_bad"]      = (ev.sidewalk_litter >= 4).astype(float)
ev["dumping_any"]     = (num("how_many_large_abandoned").fillna(0) > 0).astype(float)
ev["graffiti_tot"]    = sum(num(c).fillna(0) for c in
    ["how_many_instances_of_graffiti","how_many_instances_of_graffiti_1",
     "how_many_instances_of_graffiti_2"])
ev["feces"]           = num("how_many_instances_of_feces").fillna(0)
ev["commercial"]      = (num("is_this_route_predominantly") == 1).astype(float)
ev["period"]          = ev["evaluation_period"]
ev["nbhd_group"]      = ev["analysis_neighborhoods"]

tr = pd.DataFrame(T).T
tr.index.name = "geoid"
d = ev.dropna(subset=["geoid"]).join(tr, on="geoid")
d = d.dropna(subset=["t_inc", "t_hisp", "sidewalk_litter"])
d["log_inc"] = np.log(d.t_inc.clip(lower=10000))
d["log_dens"] = np.log((d.t_pop/d.t_area).clip(lower=1))
d["log_hom"] = np.log1p(d.geoid.map(lambda g: hom[g]/nq)/d.t_area)
print(f"analysis sample: {len(d)} evaluations across {d.geoid.nunique()} tracts")

OUT = ["sidewalk_litter","street_litter","litter_bad","dumping_any","graffiti_tot","feces"]
SPECS = {
 "raw":                        "{y} ~ {k}",
 "+tract income":              "{y} ~ {k} + log_inc",
 "+land use, period":          "{y} ~ {k} + log_inc + commercial + C(period)",
 "+density, homelessness":     "{y} ~ {k} + log_inc + commercial + C(period) + log_dens + log_hom",
 "+tenure, crowding, race":    "{y} ~ {k} + log_inc + commercial + C(period) + log_dens + log_hom + t_owner + t_crowd + t_black + t_asian",
 "+poverty instead of income": "{y} ~ {k} + t_pov + commercial + C(period) + log_dens + log_hom",
 "+neighborhood-group FE":     "{y} ~ {k} + log_inc + commercial + C(period) + log_dens + log_hom + C(nbhd_group)",
}
for key, label in [("t_hisp", "Hispanic share"), ("t_mex", "Mexican-origin share")]:
    rows = []
    for y in OUT:
        for name, f_ in SPECS.items():
            m = smf.ols(f_.format(y=y, k=key), data=d).fit(
                cov_type="cluster", cov_kwds={"groups": d.geoid})
            rows.append(dict(outcome=y, spec=name, beta=m.params[key],
                             t=m.tvalues[key], p=m.pvalues[key],
                             per10pp_sd=10*m.params[key]/d[y].std(),
                             n=int(m.nobs), tracts=d.geoid.nunique(), R2=m.rsquared))
    R = pd.DataFrame(rows)
    print(f"\n=== TABLE 22 ({key}). Tract-level test, {label}, "
          f"cluster-robust by tract ===")
    print(R.round(4).to_string(index=False))
    R.round(5).to_csv(HERE/f"table22_sf_tract_level_{key}.csv", index=False)

# within-neighborhood-group variation only, the tightest specification
print("\n=== TABLE 23. Within-neighborhood-group, tract-level, sidewalk litter ===")
rows = []
for key in ["t_hisp", "t_mex", "t_asian", "t_black", "t_pov", "t_crowd"]:
    m = smf.ols(f"sidewalk_litter ~ {key} + log_inc + commercial + C(period) "
                f"+ log_dens + log_hom + C(nbhd_group)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.geoid})
    rows.append(dict(regressor=key, beta=m.params[key], t=m.tvalues[key],
                     p=m.pvalues[key], per10pp_sd=10*m.params[key]/d.sidewalk_litter.std(),
                     n=int(m.nobs)))
print(pd.DataFrame(rows).round(4).to_string(index=False))
pd.DataFrame(rows).round(5).to_csv(HERE/"table23_sf_within_group.csv", index=False)

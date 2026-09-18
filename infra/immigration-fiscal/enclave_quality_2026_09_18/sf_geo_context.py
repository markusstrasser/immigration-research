"""Neighborhood land area (from 2020 tract polygons) and observed street-homelessness
density (SF HSH quarterly tent/structure/vehicle count, point-in-polygon)."""
import json, pathlib, collections, requests, time, sys
import numpy as np, pandas as pd
from shapely.geometry import shape, Point
from shapely.ops import unary_union
from shapely.strtree import STRtree
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"

xw = json.load(open(CD/"sf_tract_nbhd_2020.json"))
polys, names = [], []
for r in xw:
    if not r.get("the_geom"): continue
    polys.append(shape(r["the_geom"])); names.append(r["neighborhoods_analysis_boundaries"])
tree = STRtree(polys)

# land area: equal-area-ish local projection, m^2
LAT0 = 37.76
mdegla, mdeglo = 111320.0, 111320.0*np.cos(np.radians(LAT0))
def area_km2(p):
    from shapely.ops import transform
    return transform(lambda x, y: (x*mdeglo, y*mdegla), p).area/1e6
area = collections.defaultdict(float)
for p, n in zip(polys, names): area[n] += area_km2(p)

# tent counts
P = CD/"sf_tents.json"
if not P.exists():
    rows, off = [], 0
    while True:
        r = requests.get("https://data.sf.gov/resource/w9ip-yrij.json",
            params={"$limit":20000,"$offset":off}, timeout=180,
            headers={"User-Agent":"research/1.0"}); r.raise_for_status()
        d = r.json(); rows += d; off += len(d)
        if len(d) < 20000: break
    P.write_text(json.dumps(rows))
tents = json.load(open(P))
print("tent-count observations:", len(tents))
periods = sorted({t["observed_month"][:7] for t in tents})
print("periods:", periods[0], "->", periods[-1], f"({len(periods)} quarters)")

cnt = collections.defaultdict(float)
unmatched = 0
for t in tents:
    try: pt = Point(float(t["longitude"]), float(t["latitude"]))
    except Exception: unmatched += 1; continue
    hit = None
    for i in tree.query(pt):
        if polys[i].contains(pt): hit = names[i]; break
    if hit is None: unmatched += 1; continue
    tot = sum(float(t.get(k) or 0) for k in
              ("tents","structures","passenger_vehicles","other_vehicles"))
    cnt[hit] += tot
print("points outside SF tracts:", unmatched)
nq = len(periods)
rows = [dict(nbhd=n, area_km2=area[n], tents_struct_veh_per_quarter=cnt[n]/nq)
        for n in area]
df = pd.DataFrame(rows)
acs = pd.DataFrame(json.load(open(CD/"sf_nbhd_acs.json")))
df = df.merge(acs[["nbhd","pop","hisp_pct","mean_hh_inc"]], on="nbhd", how="left")
df["pop_density_per_km2"] = df["pop"]/df.area_km2
df["street_homeless_per_km2"] = df.tents_struct_veh_per_quarter/df.area_km2
df = df.sort_values("street_homeless_per_km2", ascending=False)
pd.set_option("display.width",200)
print(df.round(1).to_string(index=False))
df.round(4).to_csv(HERE/"sf_nbhd_geo_context.csv", index=False)

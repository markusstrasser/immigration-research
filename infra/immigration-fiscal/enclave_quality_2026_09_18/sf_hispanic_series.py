"""Hispanic share of population over time, SF focus neighborhoods (gentrification steel-man).
2011-2019 use 2010 tract boundaries, 2021-2023 use 2020 boundaries; the break is flagged."""
import json, pathlib, requests, collections, time, sys
import pandas as pd
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
key = None
for line in (HERE.parent/"acquire"/"config.local.env").read_text().splitlines():
    line = line.strip().removeprefix("export ")
    if line.startswith("CENSUS_API_KEY"): key = line.split("=",1)[1].strip().strip('"\'')

p10 = CD/"sf_tract_nbhd_2010.json"
if not p10.exists():
    for a in range(6):
        try:
            r = requests.get("https://data.sf.gov/resource/m46u-xzix.json",
                params={"$limit":2000,
                        "$select":"geoid,tractce10,nhood"},
                timeout=180, headers={"User-Agent":"research/1.0"})
            r.raise_for_status(); p10.write_text(json.dumps(r.json())); break
        except Exception as e:
            print("xw retry", e, file=sys.stderr); time.sleep(5)
    else:
        raise SystemExit("crosswalk fetch failed")
x10 = json.load(open(p10))
print("2010 crosswalk keys:", {k for k in x10[0] if k != "the_geom"})
def gid(r):
    g = r.get("geoid") or r.get("geoid10")
    if g: return g
    t = r.get("tractce") or r.get("tractce10")
    return "06075"+t if t else None
t10 = {gid(r): r.get("neighborhoods_analysis_boundaries") or r.get("nhood") for r in x10}
t20 = {r["geoid"]: r["neighborhoods_analysis_boundaries"]
       for r in json.load(open(CD/"sf_tract_nbhd_2020.json")) if r.get("geoid")}
print("2010 tracts:", len([k for k in t10 if k]), " 2020 tracts:", len(t20))

FOCUS = ["Mission","Chinatown","Excelsior","North Beach","Bernal Heights",
         "Outer Mission","Marina","Noe Valley","Japantown","Tenderloin"]
series = []
for yr in [2011, 2013, 2015, 2017, 2019, 2021, 2023]:
    xw = t10 if yr <= 2019 else t20
    u = (f"https://api.census.gov/data/{yr}/acs/acs5?get=NAME,B01003_001E,B03003_003E,"
         f"B03001_004E&for=tract:*&in=state:06%20county:075&key={key}")
    for a in range(5):
        try:
            rr = requests.get(u, timeout=180); rr.raise_for_status(); dd = rr.json(); break
        except Exception as e:
            print("retry", yr, e, file=sys.stderr); time.sleep(5)
    else:
        print("FAILED", yr); continue
    h = dd[0]
    agg = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for row in dd[1:]:
        rec = dict(zip(h, row)); g = rec["state"]+rec["county"]+rec["tract"]
        n = xw.get(g)
        if n not in FOCUS: continue
        for i, v in enumerate(["B01003_001E","B03003_003E","B03001_004E"]):
            try: f = float(rec[v])
            except (TypeError, ValueError): f = 0.0
            agg[n][i] += max(f, 0.0)
    for n, (p, hsp, mex) in agg.items():
        series.append(dict(year=yr, nbhd=n, pop=int(p), hisp_n=int(hsp), mex_n=int(mex),
                           hisp_pct=round(100*hsp/p, 1) if p else None,
                           mex_pct=round(100*mex/p, 1) if p else None))
    print("year", yr, "ok", flush=True)
S = pd.DataFrame(series)
pd.set_option("display.width", 200)
print("\n=== Hispanic share of population (%) ===")
print(S.pivot(index="nbhd", columns="year", values="hisp_pct").to_string())
print("\n=== Hispanic population count ===")
print(S.pivot(index="nbhd", columns="year", values="hisp_n").to_string())
print("\n=== Total population ===")
print(S.pivot(index="nbhd", columns="year", values="pop").to_string())
S.to_csv(HERE/"table11_sf_hispanic_share_series.csv", index=False)

"""(a) ACS 2019-23 ZCTA covariates (national pull, filtered later to LA ZIPs).
   (b) Mission District Hispanic-share series, for the gentrification steel-man."""
import json, pathlib, requests, collections
import pandas as pd, numpy as np
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
key = None
for line in (HERE.parent/"acquire"/"config.local.env").read_text().splitlines():
    line = line.strip().removeprefix("export ")
    if line.startswith("CENSUS_API_KEY"): key = line.split("=",1)[1].strip().strip('"\'')

VARS = ["B01003_001E","B19025_001E","B11001_001E","B03003_003E","B03001_004E",
        "B05002_013E","B03002_003E","B03002_004E","B03002_006E","B25003_001E",
        "B25003_002E","B25014_001E","B25014_005E","B25014_006E","B25014_007E",
        "B25014_011E","B25014_012E","B25014_013E","B17001_001E","B17001_002E"]
P = CD/"acs_zcta_2023.json"
if not P.exists():
    url = ("https://api.census.gov/data/2023/acs/acs5?get=NAME,"+",".join(VARS)
           + "&for=zip%20code%20tabulation%20area:*&key="+key)
    r = requests.get(url, timeout=300); r.raise_for_status()
    P.write_text(json.dumps(r.json()))
rows = json.loads(P.read_text()); hdr = rows[0]
Z = pd.DataFrame(rows[1:], columns=hdr)
for v in VARS: Z[v] = pd.to_numeric(Z[v], errors="coerce").where(lambda s: s >= 0)
Z = Z.rename(columns={"zip code tabulation area":"zcta"})
Z["pop"] = Z.B01003_001E
Z["mean_hh_inc"] = Z.B19025_001E/Z.B11001_001E
Z["hisp_pct"] = 100*Z.B03003_003E/Z["pop"]
Z["mex_pct"] = 100*Z.B03001_004E/Z["pop"]
Z["fb_pct"] = 100*Z.B05002_013E/Z["pop"]
Z["nhwhite_pct"] = 100*Z.B03002_003E/Z["pop"]
Z["nhblack_pct"] = 100*Z.B03002_004E/Z["pop"]
Z["nhasian_pct"] = 100*Z.B03002_006E/Z["pop"]
Z["owner_pct"] = 100*Z.B25003_002E/Z.B25003_001E
Z["crowded_pct"] = 100*(Z.B25014_005E+Z.B25014_006E+Z.B25014_007E+
                        Z.B25014_011E+Z.B25014_012E+Z.B25014_013E)/Z.B25014_001E
Z["pov_pct"] = 100*Z.B17001_002E/Z.B17001_001E
Z["hh"] = Z.B11001_001E
Z[["zcta","pop","hh","mean_hh_inc","hisp_pct","mex_pct","fb_pct","nhwhite_pct",
   "nhblack_pct","nhasian_pct","owner_pct","crowded_pct","pov_pct"]].to_csv(
   CD/"acs_zcta_2023.csv", index=False)
print("ZCTAs:", len(Z))

# ---------- (b) Mission Hispanic share series ----------
xw10 = CD/"sf_tract_nbhd_2010.json"
if not xw10.exists():
    r = requests.get("https://data.sf.gov/resource/m46u-xzix.json",
        params={"$limit":2000,"$select":"geoid,tractce,neighborhoods_analysis_boundaries"},
        timeout=120, headers={"User-Agent":"research/1.0"}); r.raise_for_status()
    xw10.write_text(json.dumps(r.json()))
x10 = json.load(open(xw10))
print("2010-crosswalk sample:", x10[:1])
t10 = {r.get("geoid") or ("06075"+r["tractce"]): r["neighborhoods_analysis_boundaries"]
       for r in x10}
x20 = json.load(open(CD/"sf_tract_nbhd_2020.json"))
t20 = {r["geoid"]: r["neighborhoods_analysis_boundaries"] for r in x20 if r.get("geoid")}

FOCUS = ["Mission","Chinatown","Excelsior","North Beach","Bernal Heights",
         "Outer Mission","Marina","Noe Valley"]
series = []
for yr in [2011, 2013, 2015, 2017, 2019, 2021, 2023]:
    xw = t10 if yr <= 2019 else t20
    u = (f"https://api.census.gov/data/{yr}/acs/acs5?get=NAME,B01003_001E,B03003_003E,"
         f"B03001_004E&for=tract:*&in=state:06%20county:075&key={key}")
    rr = requests.get(u, timeout=180)
    if rr.status_code != 200:
        print("skip", yr, rr.status_code); continue
    dd = rr.json(); h = dd[0]
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
        series.append(dict(year=yr, nbhd=n, pop=int(p),
                           hisp_pct=100*hsp/p if p else None,
                           mex_pct=100*mex/p if p else None,
                           hisp_n=int(hsp)))
S = pd.DataFrame(series)
piv = S.pivot(index="nbhd", columns="year", values="hisp_pct").round(1)
popv = S.pivot(index="nbhd", columns="year", values="hisp_n")
pd.set_option("display.width", 200)
print("\n=== TABLE 11a. Hispanic share of population, ACS 5-year, SF neighborhoods ===")
print("NOTE: 2011-2019 use 2010 tract boundaries, 2021-2023 use 2020 boundaries.")
print(piv.to_string())
print("\n=== TABLE 11b. Hispanic population count ===")
print(popv.to_string())
S.to_csv(HERE/"table11_sf_hispanic_share_series.csv", index=False)

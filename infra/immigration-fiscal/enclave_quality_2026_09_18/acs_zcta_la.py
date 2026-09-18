"""ACS 2019-23 ZCTA covariates for the ZIPs that appear in MyLA311."""
import json, pathlib, requests, time, sys, collections
import pandas as pd, numpy as np
HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
key = None
for line in (HERE.parent/"acquire"/"config.local.env").read_text().splitlines():
    line = line.strip().removeprefix("export ")
    if line.startswith("CENSUS_API_KEY"): key = line.split("=",1)[1].strip().strip('"\'')

rows = json.load(open(CD/"la311_zip_type_year.json"))
zips = sorted({r["zipcode"] for r in rows if r.get("zipcode")
               and r["zipcode"].isdigit() and len(r["zipcode"]) == 5})
print("distinct ZIPs in MyLA311 so far:", len(zips))

VARS = ["B01003_001E","B19025_001E","B11001_001E","B03003_003E","B03001_004E",
        "B05002_013E","B03002_003E","B03002_004E","B03002_006E","B25003_001E",
        "B25003_002E","B25014_001E","B25014_005E","B25014_006E","B25014_007E",
        "B25014_011E","B25014_012E","B25014_013E","B17001_001E","B17001_002E",
        "B25001_001E"]
out = []
for i in range(0, len(zips), 40):
    ch = zips[i:i+40]
    url = ("https://api.census.gov/data/2023/acs/acs5?get=NAME,"+",".join(VARS)
           + "&for=zip%20code%20tabulation%20area:" + ",".join(ch) + "&key=" + key)
    for a in range(5):
        try:
            r = requests.get(url, timeout=180); r.raise_for_status()
            d = r.json(); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(5)
    else:
        print("FAILED chunk", i); continue
    h = d[0]; out += [dict(zip(h, row)) for row in d[1:]]
    print("chunk", i, len(d)-1, flush=True)
Z = pd.DataFrame(out).rename(columns={"zip code tabulation area":"zcta"})
for v in VARS: Z[v] = pd.to_numeric(Z[v], errors="coerce").where(lambda s: s >= 0)
Z["pop"] = Z.B01003_001E; Z["hh"] = Z.B11001_001E
Z["hu"] = Z.B25001_001E
Z["mean_hh_inc"] = Z.B19025_001E/Z.hh
Z["hisp_pct"] = 100*Z.B03003_003E/Z["pop"]; Z["mex_pct"] = 100*Z.B03001_004E/Z["pop"]
Z["fb_pct"] = 100*Z.B05002_013E/Z["pop"]
Z["nhwhite_pct"] = 100*Z.B03002_003E/Z["pop"]
Z["nhblack_pct"] = 100*Z.B03002_004E/Z["pop"]
Z["nhasian_pct"] = 100*Z.B03002_006E/Z["pop"]
Z["owner_pct"] = 100*Z.B25003_002E/Z.B25003_001E
Z["crowded_pct"] = 100*(Z.B25014_005E+Z.B25014_006E+Z.B25014_007E+
                        Z.B25014_011E+Z.B25014_012E+Z.B25014_013E)/Z.B25014_001E
Z["pov_pct"] = 100*Z.B17001_002E/Z.B17001_001E
cols = ["zcta","pop","hh","hu","mean_hh_inc","hisp_pct","mex_pct","fb_pct",
        "nhwhite_pct","nhblack_pct","nhasian_pct","owner_pct","crowded_pct","pov_pct"]
Z[cols].to_csv(CD/"acs_zcta_la.csv", index=False)
print("saved", len(Z), "ZCTAs")

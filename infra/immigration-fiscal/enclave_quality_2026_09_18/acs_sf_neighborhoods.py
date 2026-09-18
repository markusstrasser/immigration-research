"""ACS 2019-2023 5yr tract data for San Francisco County, aggregated to
DataSF Analysis Neighborhoods via the published 2020-tract crosswalk."""
import json, os, sys, pathlib, requests

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"; CACHE.mkdir(exist_ok=True)

# load key without printing it
key = None
for line in (HERE.parent / "acquire" / "config.local.env").read_text().splitlines():
    line = line.strip()
    if line.startswith("export "): line = line[7:]
    if line.startswith("CENSUS_API_KEY"):
        key = line.split("=", 1)[1].strip().strip('"').strip("'")
assert key, "no census key"

VARS = [
    "B01003_001E",              # total pop
    "B19025_001E",              # aggregate household income
    "B11001_001E",              # households
    "B19013_001E",              # median hh income
    "B03003_003E",              # Hispanic/Latino
    "B03001_004E",              # Mexican
    "B03001_008E",              # Central American
    "B05002_013E",              # foreign born
    "B03002_003E",              # White alone, not Hispanic
    "B03002_006E",              # Asian alone, not Hispanic
    "B03002_004E",              # Black alone, not Hispanic
    "B25001_001E",              # housing units
    "B25003_001E", "B25003_002E", "B25003_003E",   # tenure
    "B25014_001E", "B25014_005E", "B25014_006E", "B25014_007E",
    "B25014_011E", "B25014_012E", "B25014_013E",   # crowding
    "B25034_001E", "B25034_010E", "B25034_011E",   # yr built: total, 1950-59, <=1939
    "B25064_001E",              # median gross rent
    "B17001_001E", "B17001_002E",  # poverty universe / below
]

def fetch(varlist, tag):
    out = {}
    for i in range(0, len(varlist), 45):
        chunk = varlist[i:i+45]
        url = ("https://api.census.gov/data/2023/acs/acs5?get=NAME," + ",".join(chunk)
               + "&for=tract:*&in=state:06%20county:075&key=" + key)
        r = requests.get(url, timeout=120); r.raise_for_status()
        rows = r.json(); hdr = rows[0]
        for row in rows[1:]:
            rec = dict(zip(hdr, row))
            geoid = rec["state"] + rec["county"] + rec["tract"]
            out.setdefault(geoid, {"NAME": rec["NAME"]}).update(
                {k: rec[k] for k in chunk})
    p = CACHE / f"acs_{tag}.json"; p.write_text(json.dumps(out))
    return out

acs = fetch(VARS, "sf_tracts_2023")
xw = json.load(open(CACHE / "sf_tract_nbhd_2020.json"))
t2n = {r["geoid"]: r["neighborhoods_analysis_boundaries"] for r in xw if r.get("geoid")}

import collections
agg = collections.defaultdict(lambda: collections.defaultdict(float))
missing = []
for geoid, rec in acs.items():
    n = t2n.get(geoid)
    if n is None:
        missing.append(geoid); continue
    for k, v in rec.items():
        if k == "NAME": continue
        try: x = float(v)
        except (TypeError, ValueError): continue
        if x < 0: continue          # ACS jam values
        if k == "B19013_001E" or k == "B25064_001E": continue  # medians not aggregable
        agg[n][k] += x
    agg[n]["ntracts"] += 1

print(f"tracts in ACS: {len(acs)}; unmatched to a neighborhood: {len(missing)}")
rows = []
for n, a in agg.items():
    pop = a["B01003_001E"]; hh = a["B11001_001E"]
    occ = a["B25014_001E"]
    crowd = a["B25014_005E"]+a["B25014_006E"]+a["B25014_007E"]+a["B25014_011E"]+a["B25014_012E"]+a["B25014_013E"]
    severe = a["B25014_006E"]+a["B25014_007E"]+a["B25014_012E"]+a["B25014_013E"]
    rows.append(dict(
        nbhd=n, tracts=int(a["ntracts"]), pop=int(pop), hh=int(hh),
        mean_hh_inc=a["B19025_001E"]/hh if hh else None,
        hisp_pct=100*a["B03003_003E"]/pop if pop else None,
        mex_pct=100*a["B03001_004E"]/pop if pop else None,
        centam_pct=100*a["B03001_008E"]/pop if pop else None,
        fb_pct=100*a["B05002_013E"]/pop if pop else None,
        nhwhite_pct=100*a["B03002_003E"]/pop if pop else None,
        nhasian_pct=100*a["B03002_006E"]/pop if pop else None,
        nhblack_pct=100*a["B03002_004E"]/pop if pop else None,
        hu=int(a["B25001_001E"]),
        owner_pct=100*a["B25003_002E"]/a["B25003_001E"] if a["B25003_001E"] else None,
        crowded_pct=100*crowd/occ if occ else None,
        severe_crowded_pct=100*severe/occ if occ else None,
        pre1940_pct=100*a["B25034_011E"]/a["B25034_001E"] if a["B25034_001E"] else None,
        pov_pct=100*a["B17001_002E"]/a["B17001_001E"] if a["B17001_001E"] else None,
    ))
rows.sort(key=lambda r: -r["pop"])
(CACHE / "sf_nbhd_acs.json").write_text(json.dumps(rows, indent=1))

import pandas as pd
df = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.max_columns", 50)
print(df.round(1).to_string(index=False))

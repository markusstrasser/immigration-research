"""ACS 5-year metro covariates for the 2010 and 2023 endpoints.

The 1-year file publishes B03001 (Hispanic origin detail) for only 63-101 metros, so
the Mexican-origin share has to come from the 5-year file, which covers every metro.
2010 = the 2006-2010 window, 2023 = the 2019-2023 window.
"""
import os, json, csv, time, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache")
KEY = os.environ["CENSUS_API_KEY"]
GEO = "metropolitan%20statistical%20area/micropolitan%20statistical%20area:*"
VARS = ["B01003_001E", "B01002_001E",
        "B03001_001E", "B03001_004E", "B03001_006E",
        "B05002_001E", "B05002_002E", "B05002_013E", "B02001_005E",
        "B25064_001E", "B19013_001E",
        "B15002_001E", "B15002_015E", "B15002_016E", "B15002_017E", "B15002_018E",
        "B15002_032E", "B15002_033E", "B15002_034E", "B15002_035E"]


def get(url):
    for a in range(5):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            print("retry", a, e, flush=True)
            time.sleep(15 * (a + 1))
    raise RuntimeError(url.split("&key=")[0])


rows = []
for y in (2010, 2023):
    d = get("https://api.census.gov/data/%d/acs/acs5?get=NAME,%s&for=%s&key=%s"
            % (y, ",".join(VARS), GEO, KEY))
    h = d[0]
    g = [x for x in h if x.startswith("metropolitan")][0]
    for r in d[1:]:
        rec = dict(zip(h, r))
        rec["year"] = y
        rec["cbsa"] = rec[g]
        rows.append(rec)
    print(y, len(d) - 1, flush=True)
out = os.path.join(CACHE, "metro_acs5.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["year", "cbsa", "NAME"] + VARS, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print("wrote", out, len(rows))

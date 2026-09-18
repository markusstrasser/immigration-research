"""ACS 1-year metro (CBSA) covariates, 2010-2024 (no 2020 1-year release).

Mexican origin is B03001_004 (Hispanic origin: Mexican, all generations), which is the
population the fiscal-gap lane calls `mexican_observed_total`, not Mexico-born only.
"""
import os, sys, csv, json, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
KEY = os.environ["CENSUS_API_KEY"]
GEO = "metropolitan%20statistical%20area/micropolitan%20statistical%20area:*"
VARS = ["B01003_001E", "B03001_001E", "B03001_004E", "B03001_006E",
        "B05002_001E", "B05002_002E", "B05002_013E", "B02001_005E",
        "B25064_001E", "B19013_001E",
        "B15003_001E", "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]
YEARS = [y for y in range(2010, 2025) if y != 2020]


def get(url):
    for a in range(5):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            sys.stderr.write("retry %d: %s\n" % (a, e))
            time.sleep(15 * (a + 1))
    raise RuntimeError(url.split("&key=")[0])


def main():
    out = os.path.join(CACHE, "metro_covariates.csv")
    rows = []
    for y in YEARS:
        d = get("https://api.census.gov/data/%d/acs/acs1?get=NAME,%s&for=%s&key=%s"
                % (y, ",".join(VARS), GEO, KEY))
        hdr = d[0]
        gcol = [h for h in hdr if h.startswith("metropolitan")][0]
        for r in d[1:]:
            rec = dict(zip(hdr, r))
            rec["year"] = y
            rec["cbsa"] = rec[gcol]
            rows.append(rec)
        print("year", y, "areas", len(d) - 1, flush=True)
    cols = ["year", "cbsa", "NAME"] + VARS
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("wrote", out, len(rows))


if __name__ == "__main__":
    main()

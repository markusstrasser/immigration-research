"""ACS 1-year state covariates, 2011-2024 (no 2020 1-year release).

Tables: B03001 (Hispanic origin detail), B05002 (nativity), B02001 (race),
B25064 (median gross rent), B25077 (median home value), B19013 (median HH income),
B15003 (educational attainment 25+), B01003 (total population).
"""
import os, sys, csv, json, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
KEY = os.environ["CENSUS_API_KEY"]

VARS = [
    "B01003_001E",                                  # total population
    "B03001_001E", "B03001_004E", "B03001_006E",    # hispanic total / Mexican / Cuban
    "B05002_001E", "B05002_013E",                   # nativity total / foreign born
    "B02001_005E",                                  # Asian alone
    "B25064_001E", "B25077_001E", "B19013_001E",    # rent, home value, HH income
    "B15003_001E", "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E",
]
YEARS = [y for y in range(2011, 2025) if y != 2020]


def get(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            sys.stderr.write("retry %d: %s\n" % (a, e))
            time.sleep(10 * (a + 1))
    raise RuntimeError(url.split("&key=")[0])


def main():
    out = os.path.join(CACHE, "state_covariates.csv")
    rows = []
    for y in YEARS:
        d = get("https://api.census.gov/data/%d/acs/acs1?get=NAME,%s&for=state:*&key=%s"
                % (y, ",".join(VARS), KEY))
        hdr = d[0]
        for r in d[1:]:
            rec = dict(zip(hdr, r))
            rec["year"] = y
            rows.append(rec)
        print("year", y, "states", len(d) - 1, flush=True)
    cols = ["year", "state", "NAME"] + VARS
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("wrote", out, len(rows))


if __name__ == "__main__":
    main()

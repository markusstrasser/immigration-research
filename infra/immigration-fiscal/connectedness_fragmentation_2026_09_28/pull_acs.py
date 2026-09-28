"""Pull ACS 5-year 2014-2018 covariates for counties and ZCTAs into _cache/acs/.

2018 matches the Social Capital Atlas's Facebook friendship snapshot (2018 population
denominators). Needs CENSUS_API_KEY in the environment; the key is never written or printed.
Raw API JSON is saved unmodified (the key is only in the request URL), with URL-without-key,
UTC time and sha256 in _cache/acs/manifest.json.
"""
import hashlib, json, os, re, sys, time, urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
OUT = LANE / "_cache" / "acs"
YEAR = 2018
VARS = {
    "B01003_001E": "pop",
    "B03001_003E": "hisp",
    "B03001_004E": "mexican",
    "B03002_003E": "nh_white",
    "B03002_004E": "nh_black",
    "B05002_013E": "foreign_born",
    "B19013_001E": "med_hh_income",
    "B19013H_001E": "med_hh_income_nhwhite",
    "B19301_001E": "per_capita_income",
    "B17001_001E": "pov_universe",
    "B17001_002E": "pov_below",
    "B15003_001E": "ed_universe",
    "B15003_022E": "ed_ba",
    "B15003_023E": "ed_ma",
    "B15003_024E": "ed_prof",
    "B15003_025E": "ed_phd",
}


def redact(s):
    return re.sub(r"key=[^&\s]+", "key=<redacted>", str(s))


def fetch(geo_for, geo_in=None):
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("[BLOCKED] CENSUS_API_KEY not set")
    base = f"https://api.census.gov/data/{YEAR}/acs/acs5?get=NAME,{','.join(VARS)}&for={geo_for}"
    if geo_in:
        base += f"&in={geo_in}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(base + f"&key={key}", timeout=180) as r:
                return base, r.read()
        except Exception as e:  # noqa: BLE001
            print(f"retry {attempt}: {redact(e)}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    sys.exit(f"[BLOCKED] fetch failed: {redact(base)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    jobs = [("county", "county:*", None), ("zcta", "zip%20code%20tabulation%20area:*", None)]
    for name, gf, gi in jobs:
        url, body = fetch(gf, gi)
        json.loads(body)  # fail loud on a non-JSON error page
        (OUT / f"acs5_{YEAR}_{name}.json").write_bytes(body)
        manifest[name] = {
            "url": url,
            "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "variables": VARS,
        }
        print(name, len(body), manifest[name]["sha256"][:12])
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")


if __name__ == "__main__":
    main()

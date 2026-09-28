"""Pull ACS 5-year 2014-2018 named-component covariates into _cache/acs/ (added 2026-09-28 after the
operator's instruction to replace any diversity index with named components).

County and ZCTA: Asian share (B03002_006), limited-English households by language (C16002),
Hispanic adults' schooling (C15002I). Tract, by state: B03002 counts used to build county
Hispanic / NH-white residential dissimilarity and exposure. Needs CENSUS_API_KEY; the key is
never written or printed. URL-without-key, UTC time and sha256 go to _cache/acs/manifest_components.json.
"""
import hashlib, json, os, re, sys, time, urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
OUT = LANE / "_cache" / "acs"
YEAR = 2018
COMP = {
    "B03002_006E": "nh_asian",
    "C16002_001E": "hh_total",
    "C16002_004E": "hh_lep_spanish",
    "C16002_007E": "hh_lep_indoeuro",
    "C16002_010E": "hh_lep_asian",
    "C16002_013E": "hh_lep_other",
    "C15002I_001E": "hisp_ad_universe",
    "C15002I_006E": "hisp_ad_ba_m",
    "C15002I_011E": "hisp_ad_ba_f",
}
TRACT = {"B03002_001E": "pop", "B03002_003E": "nh_white", "B03002_004E": "nh_black",
         "B03002_006E": "nh_asian", "B03002_012E": "hisp"}
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19",
          "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53",
          "54", "55", "56"]


def redact(s):
    return re.sub(r"key=[^&\s]+", "key=<redacted>", str(s))


def fetch(vars_, geo_for, geo_in=None):
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("[BLOCKED] CENSUS_API_KEY not set")
    base = f"https://api.census.gov/data/{YEAR}/acs/acs5?get=NAME,{','.join(vars_)}&for={geo_for}"
    if geo_in:
        base += f"&in={geo_in}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(base + f"&key={key}", timeout=180) as r:
                body = r.read()
            json.loads(body)  # fail loud on a non-JSON error page
            return base, body
        except Exception as e:  # noqa: BLE001
            print(f"retry {attempt}: {redact(e)}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    sys.exit(f"[BLOCKED] fetch failed: {redact(base)}")


def save(manifest, name, url, body, vars_):
    (OUT / f"{name}.json").write_bytes(body)
    manifest[name] = {"url": url, "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "variables": vars_}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tract").mkdir(exist_ok=True)
    manifest = {}
    for name, gf in (("comp_county", "county:*"), ("comp_zcta", "zip%20code%20tabulation%20area:*")):
        url, body = fetch(COMP, gf)
        save(manifest, name, url, body, COMP)
        print(name, len(body))
    for i, st in enumerate(STATES, 1):
        url, body = fetch(TRACT, "tract:*", f"state:{st}")
        save(manifest, f"tract/tract_{st}", url, body, TRACT)
        print(f"[{i}/{len(STATES)}] tract {st} {len(body)}")
    (OUT / "manifest_components.json").write_text(json.dumps(manifest, indent=1) + "\n")


if __name__ == "__main__":
    main()

"""Metro-level (CBSA) aggregate panel from ACS 1-year summary tables.

Payloads are tens of KB per year, so this route reaches 2005 and 2000-era windows that the
PUMS route cannot afford. The cost is that outcomes are NOT split by nativity: SSI, public
assistance and SNAP receipt are household-level for all households in the metro, and the
B23006 employment cells cover the whole 25-64 population. The nativity-split versions come
from the PUMS lane; this panel is what makes the pre-2008 windows estimable at all.

Tables
  B19056  household SSI receipt                 _001 total, _002 with SSI
  B19057  household public assistance income    _001 total, _002 with PA
  B22010  household SNAP receipt (2008+)        _001 total, _002 received SNAP
  B23006  education by employment status, 25-64
  B05002  nativity                              _001 total, _013 foreign born
  B05006  place of birth for the foreign-born   Mexico leaf resolved per year
  B01003  total population
Geography: CBSA (metropolitan and micropolitan statistical areas), as published.
"""
import json, os, pathlib, sys, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache" / "metro"
CACHE.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
GEO = "metropolitan statistical area/micropolitan statistical area:*"
YEARS = [int(y) for y in os.environ.get(
    "METRO_YEARS", "2005,2006,2007,2008,2010,2013,2015,2018,2019,2021,2022,2023,2024").split(",")]

NC_TOT = ["B23006_002E", "B23006_009E", "B23006_016E"]
NC_LF = ["B23006_003E", "B23006_010E", "B23006_017E"]
NC_EMP = ["B23006_004E", "B23006_006E", "B23006_011E", "B23006_013E",
          "B23006_018E", "B23006_020E"]
COL_TOT, COL_LF = ["B23006_023E"], ["B23006_024E"]
COL_EMP = ["B23006_025E", "B23006_027E"]


def api(url, tries=4, timeout=180):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(5 + 5 * t)
    raise RuntimeError(str(last))


def get(year, cols):
    q = {"get": "NAME," + ",".join(cols), "for": GEO}
    if KEY:
        q["key"] = KEY
    d = api(f"https://api.census.gov/data/{year}/acs/acs1?" + urllib.parse.urlencode(q))
    h = {n: i for i, n in enumerate(d[0])}
    geo = "metropolitan statistical area/micropolitan statistical area"
    out = {}
    for r in d[1:]:
        rec = {"NAME": r[h["NAME"]]}
        for c in cols:
            try:
                v = float(r[h[c]])
            except (TypeError, ValueError):
                v = None
            rec[c] = None if (v is not None and v < 0) else v
        out[r[h[geo]]] = rec
    return out


def mexico_leaf(year):
    p = CACHE.parent / f"b05006_{year}.json"
    if not p.exists():
        q = {"key": KEY} if KEY else {}
        d = api(f"https://api.census.gov/data/{year}/acs/acs1/groups/B05006.json?"
                + urllib.parse.urlencode(q))
        p.write_text(json.dumps(d))
    v = json.loads(p.read_text())["variables"]
    cands = [k for k in v if k.endswith("E") and not k.endswith("EA")
             and v[k]["label"].rstrip(":").endswith("Mexico")]
    if not cands:
        raise RuntimeError(f"no Mexico leaf in B05006 for {year}")
    return sorted(cands)[0]


def do(year):
    out = CACHE / f"metro_{year}.json"
    if out.exists():
        return f"skip {year}"
    mex = mexico_leaf(year)
    blocks = {
        "inc": ["B19056_001E", "B19056_002E", "B19057_001E", "B19057_002E"],
        "emp": NC_TOT + NC_LF + NC_EMP + COL_TOT + COL_LF + COL_EMP,
        "nat": ["B05002_001E", "B05002_013E", mex, "B01003_001E"],
    }
    if year >= 2008:
        blocks["snap"] = ["B22010_001E", "B22010_002E"]
    merged = {}
    for name, cols in blocks.items():
        d = get(year, cols)
        for cbsa, rec in d.items():
            m = merged.setdefault(cbsa, {"cbsa": cbsa, "NAME": rec["NAME"], "year": year})
            for c in cols:
                m[c] = rec[c]
        time.sleep(1)
    for m in merged.values():
        m["MEXLEAF"] = mex
    out.write_text(json.dumps(merged))
    return f"ok {year} cbsas={len(merged)}"


if __name__ == "__main__":
    for y in YEARS:
        try:
            print(do(y), flush=True)
        except Exception as e:
            print(f"FAIL {y}: {e}", flush=True)

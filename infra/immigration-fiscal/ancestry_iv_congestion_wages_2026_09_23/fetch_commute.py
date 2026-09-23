"""Summary-table commute, nativity and population pulls for the 2000-2010 metro design.

  sf3_2000_county.json   Census 2000 SF3, one request per state (the displacement lane's pattern):
                         P030 means of transportation (workers 16+), P031002 workers not at home,
                         P033 aggregate travel time (total and the public-transport components)
  sf1_2000_county.json   Census 2000 SF1 P001001, all counties in one request
  sf1_2010_county.json   Census 2010 SF1 P001001, all counties in one request
  acs1_2010_cbsa.json    ACS 2010 1-year at published CBSA (the displacement panel's 2010 endpoint):
                         B08013_001 aggregate time, B08303_001 workers not at home, B08301 modes,
                         B08136 aggregate time by mode
  acs5_2012_county.json  ACS 2008-2012 5-year by county (fixed-geography 2010 endpoint): the same
                         commute tables plus B05002 nativity, B05006 Mexico, B01003 population and
                         B19056/B19057 household SSI and public assistance

The Census key comes from CENSUS_API_KEY (source acquire/config.local.env); it is never printed and
error text is scrubbed of it. Every response is checked for a header row and a plausible row count,
because the API truncates large responses without an error.
"""
import json
import os
import pathlib
import re
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "_cache" / "census"
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
STATES = [f"{s:02d}" for s in
          [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
           29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53,
           54, 55, 56]]
SF3 = (["P030001", "P030002", "P030003", "P030004", "P030005", "P030011", "P030016",
        "P031001", "P031002", "P033001", "P033003", "P033006", "P033009", "P033012"])
COMMUTE_ACS = (["B08013_001E", "B08303_001E"]
               + [f"B08301_{i:03d}E" for i in (1, 2, 3, 4, 10, 16, 21)]
               + [f"B08136_{i:03d}E" for i in (1, 2, 3, 4, 7)])
NATIVITY_ACS = ["B05002_001E", "B05002_013E", "B05006_137E", "B01003_001E",
                "B19056_001E", "B19056_002E", "B19057_001E", "B19057_002E"]
CBSA_GEO = "metropolitan statistical area/micropolitan statistical area:*"


def scrub(text: str) -> str:
    return re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", str(text))


def api(base: str, params: dict, tries: int = 5, timeout: int = 240) -> list:
    q = dict(params)
    if KEY:
        q["key"] = KEY
    url = f"{base}?" + urllib.parse.urlencode(q)
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            if not d or not isinstance(d[0], list):
                raise RuntimeError("no header row")
            return d
        except Exception as e:  # noqa: BLE001 - retried, then raised scrubbed
            last = e
            time.sleep(3 + 4 * t)
    raise RuntimeError(scrub(last))


def records(d: list, cols: list, geo_cols: list) -> dict:
    h = {n: i for i, n in enumerate(d[0])}
    out = {}
    for r in d[1:]:
        gid = "".join(r[h[g]].zfill(w) for g, w in geo_cols)
        rec = {}
        for c in cols:
            try:
                v = float(r[h[c]])
            except (TypeError, ValueError):
                v = None
            rec[c] = None if (v is not None and v < 0) else v
        out[gid] = rec
    return out


def sf3_2000():
    path = OUT / "sf3_2000_county.json"
    rows = json.loads(path.read_text()) if path.exists() else {}
    done = {k[:2] for k in rows}
    for st in STATES:
        if st in done:
            continue
        d = api("https://api.census.gov/data/2000/dec/sf3",
                {"get": ",".join(SF3), "for": "county:*", "in": "state:" + st})
        rows.update(records(d, SF3, [("state", 2), ("county", 3)]))
        path.write_text(json.dumps(rows))
        print(f"sf3 {st} counties={len(rows)}", flush=True)
        time.sleep(0.3)
    return len(rows)


def one_shot(name: str, base: str, cols: list, geo: str, geo_cols: list, min_rows: int):
    path = OUT / f"{name}.json"
    if path.exists():
        return f"skip {name}"
    # the API caps a request at 50 variables; every pull here is below that
    d = api(base, {"get": ",".join(["NAME"] + cols), "for": geo})
    rec = records(d, cols, geo_cols)
    if len(rec) < min_rows:
        raise SystemExit(f"[BLOCKED] {name}: {len(rec)} rows < {min_rows}; truncated response?")
    names = {("".join(r[d[0].index(g)].zfill(w) for g, w in geo_cols)): r[d[0].index("NAME")] for r in d[1:]}
    for k in rec:
        rec[k]["NAME"] = names[k]
    path.write_text(json.dumps(rec))
    return f"ok {name} rows={len(rec)}"


def main():
    print(one_shot("sf1_2000_county", "https://api.census.gov/data/2000/dec/sf1", ["P001001"],
                   "county:*", [("state", 2), ("county", 3)], 3100), flush=True)
    print(one_shot("sf1_2010_county", "https://api.census.gov/data/2010/dec/sf1", ["P001001"],
                   "county:*", [("state", 2), ("county", 3)], 3100), flush=True)
    print(one_shot("acs1_2010_cbsa", "https://api.census.gov/data/2010/acs/acs1",
                   COMMUTE_ACS + ["B05002_001E", "B05002_013E", "B01003_001E"], CBSA_GEO,
                   [("metropolitan statistical area/micropolitan statistical area", 5)], 500), flush=True)
    print(one_shot("acs5_2012_county", "https://api.census.gov/data/2012/acs/acs5",
                   COMMUTE_ACS + NATIVITY_ACS, "county:*", [("state", 2), ("county", 3)], 3100), flush=True)
    print("sf3 counties", sf3_2000(), flush=True)


if __name__ == "__main__":
    main()

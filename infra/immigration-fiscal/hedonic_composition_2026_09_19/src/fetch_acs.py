#!/usr/bin/env python3
"""Fetch ACS 5-year tract tables for three vintages into _cache/acs/<year>/<state>.json.

Idempotent: an existing, parseable cache file is never re-fetched, so a second
run performs zero network calls and leaves derived/ untouched.
"""
import json, os, sys, time, pathlib
from concurrent.futures import ThreadPoolExecutor
import threading
import requests

WORKERS = 8
_local = threading.local()

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
YEARS = [2013, 2018, 2023]

# Vintage-stable core variables (verified present in 2013/2018/2023 acs5).
CORE = [
    "B03002_001E", "B03002_003E", "B03002_012E",   # total, NH white alone, Hispanic
    "B05002_001E", "B05002_013E",                   # nativity universe, foreign born
    "B25064_001E",                                  # median gross rent
    "B25077_001E",                                  # median home value
    "B25003_001E", "B25003_002E", "B25003_003E",    # tenure: total, owner, renter
    "B19013_001E",                                  # median household income
    "B15003_001E", "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E",
    "B25035_001E",                                  # median year structure built
    "B25002_001E", "B25002_003E",                   # housing units total, vacant
    "B25024_001E", "B25024_002E",                   # structure: total, 1-unit detached
    "B03001_004E",                                  # Hispanic of Mexican origin
]

# B05006 origin aggregates, resolved per vintage by normalised label path.
B05006_PATHS = {
    "eur":  ["Total", "Europe"],
    "asia": ["Total", "Asia"],
    "afr":  ["Total", "Africa"],
    "oce":  ["Total", "Oceania"],
    "carib": ["Total", "Americas", "Latin America", "Caribbean"],
    "camer": ["Total", "Americas", "Latin America", "Central America"],
    "samer": ["Total", "Americas", "Latin America", "South America"],
    "namer": ["Total", "Americas", "Northern America"],
    "mex":  ["Total", "Americas", "Latin America", "Central America", "Mexico"],
}

STATES = ["01","02","04","05","06","08","09","10","11","12","13","15","16","17","18",
          "19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
          "34","35","36","37","38","39","40","41","42","44","45","46","47","48","49",
          "50","51","53","54","55","56"]


def norm(label):
    parts = [p.strip().rstrip(":") for p in label.split("!!")]
    if parts and parts[0] == "Estimate":
        parts = parts[1:]
    return [p for p in parts if p]


def resolve_b05006(year):
    """Map origin key -> B05006 variable id for this vintage, by exact label path."""
    with open(CACHE / f"grp_B05006_{year}.json") as fh:
        meta = json.load(fh)["variables"]
    index = {}
    for vid, info in meta.items():
        if not vid.startswith("B05006_") or not vid.endswith("E"):
            continue
        index[tuple(norm(info.get("label", "")))] = vid
    out = {}
    for key, path in B05006_PATHS.items():
        vid = index.get(tuple(path))
        if vid is None:
            raise SystemExit(f"[fatal] {year}: no B05006 line for path {path}")
        out[key] = vid
    return out


def _session():
    if not hasattr(_local, "s"):
        _local.s = requests.Session()
    return _local.s


def fetch(year, state, varlist, key, session=None):
    session = session or _session()
    dest = CACHE / "acs" / str(year) / f"{state}.json"
    if dest.exists():
        try:
            with open(dest) as fh:
                rows = json.load(fh)
            if isinstance(rows, list) and len(rows) > 1:
                return len(rows) - 1, True
        except Exception:
            dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {"get": ",".join(varlist), "for": "tract:*",
              "in": f"state:{state} county:*", "key": key}
    last = None
    for attempt in range(5):
        try:
            r = session.get(url, params=params, timeout=180)
            if r.status_code == 200:
                rows = r.json()
                tmp = dest.with_suffix(".tmp")
                with open(tmp, "w") as fh:
                    json.dump(rows, fh)
                tmp.replace(dest)
                return len(rows) - 1, False
            last = f"HTTP {r.status_code}: {r.text[:180]}"
        except Exception as exc:
            last = repr(exc)
        time.sleep(3 * (attempt + 1))
    raise SystemExit(f"[fatal] {year} state {state} failed: {last}")


def main():
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise SystemExit("[fatal] CENSUS_API_KEY not in environment")
    manifest = {}
    for year in YEARS:
        b05 = resolve_b05006(year)
        manifest[str(year)] = b05
        varlist = CORE + [b05[k] for k in sorted(b05)]
        print(f"[{year}] {len(varlist)} variables; B05006 mex={b05['mex']}", flush=True)
        done = [0]
        lock = threading.Lock()

        def work(st):
            n, cached = fetch(year, st, varlist, key)
            with lock:
                done[0] += 1
                print(f"[{year}] {done[0]:>2}/{len(STATES)} state {st}: {n} tracts"
                      f"{' (cached)' if cached else ''}", flush=True)
            return n

        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(work, STATES))
    with open(CACHE / "b05006_manifest.json", "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
    print("[done] manifest written", flush=True)


if __name__ == "__main__":
    main()

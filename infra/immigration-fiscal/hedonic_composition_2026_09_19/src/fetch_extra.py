#!/usr/bin/env python3
"""Two extra pulls: ZCTA composition (for the Zillow arm) and tract margins of
error (for the attenuation correction). Both idempotent."""
import json, os, pathlib, threading, time
from concurrent.futures import ThreadPoolExecutor
import requests

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
YEARS = [2013, 2018, 2023]
_local = threading.local()

ZCTA_VARS = ["B03002_001E", "B03002_003E", "B03002_012E", "B05002_001E",
             "B05002_013E", "B03001_004E", "B25003_001E", "B25003_002E",
             "B25003_003E", "B19013_001E", "B15003_001E", "B15003_022E",
             "B15003_023E", "B15003_024E", "B15003_025E", "B25002_001E",
             "B25002_003E", "B25024_001E", "B25024_002E", "B25035_001E",
             "B25064_001E", "B25077_001E"]
# Margins of error for the share numerators and denominators.
MOE_VARS = ["B03002_001M", "B03002_012M", "B05002_001M", "B05002_013M",
            "B03001_004M", "B03002_001E", "B03002_012E", "B05002_001E",
            "B05002_013E", "B03001_004E"]
STATES = ["01","02","04","05","06","08","09","10","11","12","13","15","16","17","18",
          "19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
          "34","35","36","37","38","39","40","41","42","44","45","46","47","48","49",
          "50","51","53","54","55","56"]


def sess():
    if not hasattr(_local, "s"):
        _local.s = requests.Session()
    return _local.s


def get(url, params, dest):
    if dest.exists():
        try:
            rows = json.load(open(dest))
            if isinstance(rows, list) and len(rows) > 1:
                return len(rows) - 1, True
        except Exception:
            dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for a in range(5):
        try:
            r = sess().get(url, params=params, timeout=300)
            if r.status_code == 200:
                rows = r.json()
                tmp = dest.with_suffix(".tmp")
                json.dump(rows, open(tmp, "w"))
                tmp.replace(dest)
                return len(rows) - 1, False
            last = f"HTTP {r.status_code} {r.text[:150]}"
        except Exception as e:
            last = repr(e)
        time.sleep(3 * (a + 1))
    raise SystemExit(f"[fatal] {dest}: {last}")


def main():
    key = os.environ["CENSUS_API_KEY"]
    for y in YEARS:
        n, c = get(f"https://api.census.gov/data/{y}/acs/acs5",
                   {"get": ",".join(ZCTA_VARS),
                    "for": "zip code tabulation area:*", "key": key},
                   CACHE / "zcta" / f"{y}.json")
        print(f"[zcta {y}] {n} ZCTAs{' (cached)' if c else ''}", flush=True)
    for y in YEARS:
        done, lock = [0], threading.Lock()

        def work(st, y=y):
            n, c = get(f"https://api.census.gov/data/{y}/acs/acs5",
                       {"get": ",".join(MOE_VARS), "for": "tract:*",
                        "in": f"state:{st} county:*", "key": key},
                       CACHE / "moe" / str(y) / f"{st}.json")
            with lock:
                done[0] += 1
                print(f"[moe {y}] {done[0]}/{len(STATES)} {st}: {n}"
                      f"{' (cached)' if c else ''}", flush=True)

        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(work, STATES))
    print("[done]", flush=True)


if __name__ == "__main__":
    main()

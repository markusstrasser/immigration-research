"""Hispanic share of public-school enrollment by state, grade (K–8) and fall year, 1998–2023, for the
cohort-lagged exposure specifications. CCD district membership summed by FIPS, race and grade through
the Urban Institute Education Data API (public, no key). Race by grade starts in fall 1998 (34 states;
45 in 2000; complete later); states without race-by-grade counts are left out, never imputed.

Writes derived/state_grade_shares.csv. Raw summaries are cached in _cache/grade_shares/.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/acquire_grade_shares.py
"""
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "grade_shares"
OUT = HERE / "derived" / "state_grade_shares.csv"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"}
URL = "https://educationdata.urban.org/api/v1/school-districts/ccd/enrollment/summaries"
YEARS = range(1998, 2024)
GRADES = range(0, 9)  # 0 = kindergarten
FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA",
        15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD",
        25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
        35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC",
        46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}


def fetch(job):
    year, grade = job
    path = CACHE / f"race_g{grade}_{year}.json"
    if path.exists():
        return path
    for attempt in range(6):
        try:
            r = requests.get(URL, params={"var": "enrollment", "stat": "sum", "by": "fips,race", "grade": grade,
                                          "year": year}, headers=UA, timeout=300)
            r.raise_for_status()
            d = r.json()
            assert d.get("next") is None
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(d["results"], sort_keys=True))
            return path
        except (requests.RequestException, ValueError, AssertionError) as e:
            print("retry", path.name, type(e).__name__, flush=True)
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(path.name)


def main():
    jobs = [(y, g) for y in YEARS for g in GRADES]
    with ThreadPoolExecutor(max_workers=3) as ex:
        for i, p in enumerate(ex.map(fetch, jobs), 1):
            if i % 20 == 0:
                print(f"[{i}/{len(jobs)}] {p.name}", flush=True)
    rows = []
    for year, grade in jobs:
        res = json.loads((CACHE / f"race_g{grade}_{year}.json").read_text())
        by = {}
        for x in res:
            if x["fips"] in FIPS and x["enrollment"] is not None and x["enrollment"] > 0:
                by.setdefault(x["fips"], {})[x["race"]] = x["enrollment"]
        for f, d in by.items():
            known = sum(v for k, v in d.items() if k in (1, 2, 3, 4, 5, 6, 7))
            if known <= 0:
                continue
            rows.append({"state": FIPS[f], "fall_year": year, "grade": grade, "total": d.get(99, ""),
                         "known_race": known, "hispanic": d.get(3, 0),
                         "hisp_share": round(100 * d.get(3, 0) / known, 4)})
    rows.sort(key=lambda r: (r["state"], r["fall_year"], r["grade"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["state", "fall_year", "grade", "total", "known_race", "hispanic",
                                           "hisp_share"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()

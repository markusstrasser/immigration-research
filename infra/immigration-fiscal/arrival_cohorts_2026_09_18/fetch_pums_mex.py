"""Mexico-born ACS 1-year PUMS via the Census API, one state at a time.

Whole-year POBP=303 calls drop on this link; state × AGEP=25:54 completes. Never prints
CENSUS_API_KEY. Writes _cache/states_<year>/st_<fips>.json; english_cohorts.py refuses a
year until all 51 files (50 states + DC) are present.

Usage: CENSUS_API_KEY must be in the environment.
  uv run --no-project python3 fetch_pums_mex.py [year ...]
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
GET = "PWGTP,AGEP,SEX,SCHL,ENG,YOEP,CIT,ESR,WAGP,WKHP"
STATES = [
    f"{s:02d}"
    for s in (
        1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
        42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56,
    )
]
TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "180"))
DEFAULT_YEARS = [2016, 2018, 2021, 2022]
# predicate vars are echoed; empty states (e.g. VT 2022) return HTTP 200 with no body
HEADER = [
    "PWGTP", "AGEP", "SEX", "SCHL", "ENG", "YOEP", "CIT", "ESR", "WAGP", "WKHP",
    "POBP", "AGEP", "state",
]


def redact(text: str, key: str) -> str:
    if not key:
        return text
    return text.replace(key, "[REDACTED]")


def valid_pums(raw) -> bool:
    return isinstance(raw, list) and len(raw) >= 1 and isinstance(raw[0], list)


def fetch(url: str, key: str, tries: int = 3):
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                body = resp.read().decode("utf-8", "replace")
            if not body.strip():
                return [HEADER]
            if not body.rstrip().endswith("]]"):
                raise ValueError("truncated JSON (does not end in ]] )")
            raw = json.loads(body)
            if isinstance(raw, dict) and "error" in raw:
                raise RuntimeError(raw["error"])
            if not valid_pums(raw):
                raise ValueError("not a PUMS table")
            return raw
        except Exception as exc:
            last = type(exc).__name__
            time.sleep(2 + attempt * 3)
    raise RuntimeError(last or "fetch failed")


def state_url(year: int, fips: str, key: str) -> str:
    q = urllib.parse.urlencode(
        {
            "get": GET,
            "POBP": "303",
            "AGEP": "25:54",
            "for": f"state:{fips}",
            "key": key,
        }
    )
    return f"https://api.census.gov/data/{year}/acs/acs1/pums?{q}"


def fetch_year(year: int, key: str) -> int:
    parquet = CACHE / f"acs_{year}.parquet"
    if parquet.exists():
        print(f"[skip] {year} parquet already staged")
        return 0
    dest = CACHE / f"states_{year}"
    dest.mkdir(parents=True, exist_ok=True)
    fail = 0
    for fips in STATES:
        path = dest / f"st_{fips}.json"
        if path.exists():
            try:
                raw = json.loads(path.read_text())
                if valid_pums(raw):
                    continue
            except Exception:
                path.unlink(missing_ok=True)
        try:
            raw = fetch(state_url(year, fips, key), key)
            path.write_text(json.dumps(raw))
            n = max(0, len(raw) - 1)
            print(f"  {year} st={fips} rows={n}")
        except Exception as exc:
            fail += 1
            print(f"  {year} st={fips} FAIL {redact(str(exc), key)}")
            time.sleep(2)
    have = len(list(dest.glob("st_*.json")))
    print(f"[{'ok' if have == 51 and fail == 0 else 'partial'}] {year} {have}/51 states fail={fail}")
    return fail


def main():
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY is not set")
    years = [int(y) for y in (sys.argv[1:] or DEFAULT_YEARS)]
    CACHE.mkdir(parents=True, exist_ok=True)
    fail = 0
    for year in years:
        fail += fetch_year(year, key)
    raise SystemExit(fail)


if __name__ == "__main__":
    main()

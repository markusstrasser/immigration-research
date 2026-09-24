"""District-year CCD directory (teachers, English learners, membership) and membership by race.

Source: Urban Institute Education Data Portal, which redistributes NCES CCD by LEA and year (the
"year" is the fall of the school year: 2015 = fall 2015 = SY2015-16 = Census F-33 FY2016).
  school-districts/ccd/directory/{year}/?fips=S      teachers_total_fte, english_language_learners
  school-districts/ccd/enrollment/{year}/grade-99/race/?fips=S&sex=99   race 3 Hispanic, 99 total

Fetched with curl (Python urllib fails TLS on this machine); every body must parse as JSON and the
rows collected across pages must equal the API's own `count`, otherwise the file is not written.
Resumable: a state-year file already on disk is skipped. Writes _cache/ccd/<kind>_<year>_<fips>.csv.

    KINDS=dir,enr YEARS=2000,2005 WORKERS=6 uv run --no-project \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/pull_ccd.py
"""
import concurrent.futures as cf
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "_cache" / "ccd"
BASE = "https://educationdata.urban.org/api/v1/school-districts/ccd"
STATES = [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
          32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
DIR_COLS = ["year", "fips", "leaid", "lea_name", "agency_type", "agency_charter_indicator", "enrollment",
            "english_language_learners", "teachers_total_fte", "number_of_schools", "spec_ed_students",
            "urban_centric_locale", "county_code"]
RACES = {99: "enr_total", 3: "enr_hisp", 1: "enr_white"}


def get(url, tries=5):
    last = None
    for t in range(tries):
        r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "600", "-A", "research/1.0", url],
                           capture_output=True, text=True)
        if r.returncode == 0:
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError as e:
                last = f"bad JSON ({len(r.stdout)} chars): {e}"
        else:
            last = f"curl rc={r.returncode}: {r.stderr.strip()[:160]}"
        time.sleep(10 * (t + 1))
    raise RuntimeError(f"{url} :: {last}")


def pages(url):
    rows, count = [], None
    while url:
        d = get(url)
        count = d.get("count") if count is None else count
        rows += d.get("results", [])
        url = d.get("next")
    if count is not None and count != len(rows):
        raise RuntimeError(f"collected {len(rows)} rows, API count {count}")
    return rows


def write(path, cols, rows):
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def do_dir(year, fips):
    p = OUT / f"dir_{year}_{fips:02d}.csv"
    if p.exists():
        return f"skip dir {year} {fips}"
    rows = pages(f"{BASE}/directory/{year}/?fips={fips}")
    write(p, DIR_COLS, rows)
    return f"ok dir {year} {fips} n={len(rows)}"


def do_enr(year, fips):
    p = OUT / f"enr_{year}_{fips:02d}.csv"
    if p.exists():
        return f"skip enr {year} {fips}"
    rows = pages(f"{BASE}/enrollment/{year}/grade-99/race/?fips={fips}&sex=99")
    acc = {}
    for r in rows:
        rc = r.get("race")
        if rc not in RACES:
            continue
        a = acc.setdefault(r["leaid"], {"year": year, "fips": fips, "leaid": r["leaid"]})
        v = r.get("enrollment")
        a[RACES[rc]] = None if v is None or v < 0 else v    # CCD negative codes: missing / n.a. / suppressed
    write(p, ["year", "fips", "leaid"] + list(RACES.values()), list(acc.values()))
    return f"ok enr {year} {fips} n={len(acc)}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    years = [int(y) for y in os.environ.get("YEARS", "2015").split(",")]
    kinds = os.environ.get("KINDS", "dir,enr").split(",")
    fn = {"dir": do_dir, "enr": do_enr}
    jobs = [(fn[k], y, s) for y in years for k in kinds for s in STATES]
    fails = []
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "6"))) as ex:
        futs = {ex.submit(f, y, s): (f.__name__, y, s) for f, y, s in jobs}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            try:
                print(f"[{i}/{len(jobs)}] {fut.result()}", flush=True)
            except Exception as e:
                fails.append((futs[fut], str(e)[:200]))
                print(f"[{i}/{len(jobs)}] FAIL {futs[fut]}: {str(e)[:200]}", flush=True)
    print(f"done; {len(fails)} failures", flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

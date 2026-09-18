"""District-year panel from the Urban Institute Education Data Portal (NCES CCD + Census F-33).

Three endpoints per state-year, no key required:
  ccd/finance      Census F-33 district finance as redistributed by Urban (2000-2020 only;
                   2021+ returns count 0, checked 2026-09-18)
  ccd/enrollment   membership by race, grade 99 (all grades). Race codes: 1 White, 2 Black,
                   3 Hispanic, 4 Asian, 99 Total
  ccd/directory    county_code, cbsa, english_language_learners, locale, agency type

The F-33 is the same source the repo's ledger_absolute_2026_09_17/district_differential.py
reads locally for FY2024; Urban is used here only because the panel needs 2000-2020 and
only the FY2024 file is staged locally.

Writes _cache/dist/<kind>_<year>_<fips>.csv.
"""
import concurrent.futures as cf
import csv, json, os, pathlib, sys, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
OUT = HERE / "_cache" / "dist"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://educationdata.urban.org/api/v1/school-districts/ccd"
YEARS = [int(y) for y in os.environ.get("DIST_YEARS", "2000,2005,2010,2015,2020").split(",")]
STATES = [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
          33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]
TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "240"))

FIN_COLS = ["year", "fips", "leaid", "enrollment_fall_responsible", "rev_total",
            "rev_local_total", "rev_local_prop_tax", "rev_state_total", "rev_fed_total",
            "exp_current_elsec_total", "exp_current_instruction_total"]
DIR_COLS = ["year", "fips", "leaid", "county_code", "cbsa", "enrollment",
            "english_language_learners", "urban_centric_locale", "agency_type",
            "agency_charter_indicator", "lea_name"]
RACES = {99: "enr_total", 1: "enr_white", 2: "enr_black", 3: "enr_hisp", 4: "enr_asian"}


def get(url, tries=4):
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(5 * (t + 1))
    raise RuntimeError(f"{url[:120]} :: {last}")


def pages(url):
    """Follow Urban's cursor pagination."""
    rows = []
    while url:
        d = get(url)
        rows += d.get("results", [])
        url = d.get("next")
    return rows


def write(path, cols, rows):
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.rename(path)


def do_fin(year, fips):
    p = OUT / f"fin_{year}_{fips:02d}.csv"
    if p.exists():
        return f"skip fin {year} {fips}"
    rows = pages(f"{BASE}/finance/{year}/?fips={fips}")
    write(p, FIN_COLS, rows)
    return f"ok fin {year} {fips} n={len(rows)}"


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
    rows = pages(f"{BASE}/enrollment/{year}/grade-99/race/?fips={fips}")
    acc = {}
    for r in rows:
        rc = r.get("race")
        if rc not in RACES:
            continue
        if r.get("sex") not in (99, None):
            continue
        k = r["leaid"]
        a = acc.setdefault(k, {"year": year, "fips": fips, "leaid": k})
        v = r.get("enrollment")
        # CCD uses negative sentinels (-1 missing, -2 not applicable, -3 suppressed)
        a[RACES[rc]] = None if v is None or v < 0 else v
    cols = ["year", "fips", "leaid"] + list(RACES.values())
    write(p, cols, list(acc.values()))
    return f"ok enr {year} {fips} n={len(acc)}"


def main():
    jobs = []
    for y in YEARS:
        for s in STATES:
            jobs += [(do_fin, y, s), (do_dir, y, s), (do_enr, y, s)]
    fails = []
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "6"))) as ex:
        futs = {ex.submit(fn, y, s): (fn.__name__, y, s) for fn, y, s in jobs}
        for fut in cf.as_completed(futs):
            tag = futs[fut]
            try:
                print(fut.result(), flush=True)
            except Exception as e:
                fails.append((tag, str(e)[:160]))
                print(f"FAIL {tag}: {str(e)[:160]}", flush=True)
    print(f"done; {len(fails)} failures", flush=True)
    for f in fails:
        print("  ", f, flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

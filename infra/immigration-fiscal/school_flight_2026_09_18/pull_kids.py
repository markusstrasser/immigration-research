"""ACS 1-year PUMS cells for children 5-17: school type x race/ethnicity x nativity, by PUMA.

One call per state-year over AGEP 5:17, splitting the age range whenever the Census
API truncates (same pattern as employment_entry_2026_09_18/pull_pums3.py, whose
docstring records that the link resets large responses).

Variables
  SCH       1 = not attending, 2 = public school/college, 3 = private school/college/HOME SCHOOL
  RAC1P     1 = White alone, 2 = Black alone, 6 = Asian alone
  HISP      1 = not Hispanic; >1 = Hispanic (any race)
  NATIVITY  1 = native-born, 2 = foreign-born
  AGEP      5-12 treated as elementary, 13-17 as secondary (SCHG coding is not
            comparable across 2005-2007 and 2008+, so age is used instead)

Cells are written per state-year to _cache/kids/kids_<year>_<state>.csv with counts
weighted by PWGTP. Home school sits inside SCH=3 from the 2008 questionnaire wording
onward; that is a known contaminant of the private-share series and is flagged in the memo.
"""
import concurrent.futures as cf
import csv, json, os, pathlib, sys, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
CELLS = HERE / "_cache" / "kids"
CELLS.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
YEARS = [int(y) for y in os.environ.get(
    "PUMS_YEARS", "2005,2008,2010,2013,2015,2018,2023").split(",")]
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "240"))
BIG = {"06", "48", "36", "12", "17", "42", "39", "13", "37", "26", "34", "53", "51", "04"}

# group key -> (race/ethnicity label, nativity label)
FIELDS = ["year", "state", "puma", "grp", "lvl", "pub", "priv", "noschool"]


def api(url, tries=3):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(4)
    raise RuntimeError(str(last))


def pums_split(year, state, cols, lo, hi, depth=0):
    if depth == 0 and state in BIG and hi - lo >= 6:
        hdr, rows = None, []
        a = lo
        step = max(3, (hi - lo + 1) // 3)
        while a <= hi:
            b = min(a + step - 1, hi)
            h, r = pums_split(year, state, cols, a, b, 1)
            hdr = hdr or h
            rows += r
            a = b + 1
        return hdr, rows
    q = {"get": ",".join(cols), "for": "state:" + state, "AGEP": f"{lo}:{hi}"}
    if KEY:
        q["key"] = KEY
    url = f"https://api.census.gov/data/{year}/acs/acs1/pums?" + urllib.parse.urlencode(q)
    try:
        d = api(url)
        return d[0], d[1:]
    except Exception:
        if lo >= hi or depth >= 6:
            raise
        mid = (lo + hi) // 2
        h, r1 = pums_split(year, state, cols, lo, mid, depth + 1)
        _, r2 = pums_split(year, state, cols, mid + 1, hi, depth + 1)
        return h, r1 + r2


def group(rac, hisp, nat):
    """Mutually exclusive groups. Hispanic takes precedence over race, as in CCD/NCES."""
    if hisp is None or rac is None or nat is None:
        return None
    if hisp > 1:
        return "hisp_fb" if nat == 2 else "hisp_nb"
    if nat == 2:
        return "nonhisp_fb"
    if rac == 1:
        return "wnh_nb"
    if rac == 2:
        return "bnh_nb"
    if rac == 6:
        return "anh_nb"
    return "onh_nb"


def num(x, d=None):
    try:
        return int(x)
    except (TypeError, ValueError):
        return d


def do(year, state):
    out = CELLS / f"kids_{year}_{state}.csv"
    if out.exists():
        return f"skip {year} {state}"
    cols = ["PUMA", "SCH", "AGEP", "RAC1P", "HISP", "NATIVITY", "PWGTP"]
    hdr, rows = pums_split(year, state, cols, 5, 17)
    ix = {c: i for i, c in enumerate(hdr)}
    acc = {}
    for r in rows:
        puma = str(r[ix["PUMA"]]).zfill(5)
        sch = num(r[ix["SCH"]])
        age = num(r[ix["AGEP"]])
        g = group(num(r[ix["RAC1P"]]), num(r[ix["HISP"]]), num(r[ix["NATIVITY"]]))
        w = num(r[ix["PWGTP"]], 0)
        if g is None or sch is None or age is None or not (5 <= age <= 17):
            continue
        lvl = "elem" if age <= 12 else "sec"
        k = (puma, g, lvl)
        a = acc.setdefault(k, [0, 0, 0])
        if sch == 2:
            a[0] += w
        elif sch == 3:
            a[1] += w
        else:
            a[2] += w
    tmp = out.with_suffix(".tmp")
    with tmp.open("w", newline="") as f:
        w_ = csv.writer(f)
        w_.writerow(FIELDS)
        for (puma, g, lvl), (pub, priv, no) in sorted(acc.items()):
            w_.writerow([year, state, puma, g, lvl, pub, priv, no])
    tmp.rename(out)
    return f"ok {year} {state} rows={len(rows)} cells={len(acc)}"


def main():
    jobs = [(y, s) for y in YEARS for s in STATES]
    workers = int(os.environ.get("WORKERS", "4"))
    fails = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(do, y, s): (y, s) for y, s in jobs}
        for fut in cf.as_completed(futs):
            y, s = futs[fut]
            try:
                print(fut.result(), flush=True)
            except Exception as e:
                fails.append((y, s, str(e)[:160]))
                print(f"FAIL {y} {s}: {str(e)[:160]}", flush=True)
    print(f"done; {len(fails)} failures", flush=True)
    for f in fails:
        print("  ", f, flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

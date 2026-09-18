"""PUMA cells for the entry-employment panel, with the selection pushed onto the server.

The link to api.census.gov sustains only a couple of hundred KB/s in aggregate and resets
large responses, so every row that is not needed is a row not requested. Three calls per
state-year:

  A  PUMS ages 16-29, NATIVITY=1, SCHL below bachelor's  -> the outcome cells
  B  PUMS ages 18-64, NATIVITY=2                         -> the treatment numerators
  C  ACS summary B01001 at PUMA level                    -> total population 18-64

Definitions:
  native      NATIVITY=1            foreign-born NATIVITY=2      Mexico-born POBP=303
  no college  SCHL 1-12 (2005-2007), 1-20 (2008+)
  employed    ESR in (1,2,4,5)      in labour force ESR in (1,2,3,4,5)
  outcomes exclude institutional group quarters (TYPE/TYPEHUGQ=2)
  treatment numerator and denominator both INCLUDE group quarters, so they match
  the published B01001 denominator

Foreign-born is NATIVITY-based throughout, so a person born in Mexico to US-citizen parents
counts as native in both the numerator and the denominator.
"""
import concurrent.futures as cf
import csv, json, os, pathlib, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
CELLS = HERE / "_cache" / "cells3"
CELLS.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
# Only the window endpoints are needed: every 5- and 10-year difference in the design ends
# on one of these years. The link to the Census API is too slow for a full annual panel.
YEARS = [int(y) for y in os.environ.get(
    "PUMS_YEARS", "2005,2008,2010,2013,2015,2018,2023").split(",")]
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
AGE_VARS = ([f"B01001_{i:03d}E" for i in range(7, 20)] +
            [f"B01001_{i:03d}E" for i in range(31, 44)])
EMP, CIV, LF = {"1", "2", "4", "5"}, {"1", "2"}, {"1", "2", "3", "4", "5"}
FIELDS = ["year", "state", "puma", "sex", "pop1829", "emp1829", "cemp1829", "lf1829",
          "pop1624", "emp1624", "cemp1624", "lf1624", "pop1864", "mex1864", "fb1864"]
TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "210"))


def gq_var(y):
    return "TYPEHUGQ" if y >= 2020 else "TYPE"


def cut(y):
    return 12 if y <= 2007 else 20


def api(url, tries=2):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(3)
    raise RuntimeError(str(last))


# States whose single-call responses are large enough that the server routinely resets them.
BIG = {"06", "48", "36", "12", "17", "42", "39", "13", "37", "26", "34", "53", "51", "04"}


def pums_split(year, state, cols, lo, hi, extra=None, depth=0):
    """Fetch one age range, halving it whenever the server truncates or stalls.

    For the largest states the first call is split up front rather than after a failure,
    because a reset costs the whole transfer that preceded it."""
    if depth == 0 and state in BIG and hi - lo >= 6:
        step = max(3, (hi - lo + 1) // 4)
        hdr, rows = None, []
        a = lo
        while a <= hi:
            b = min(a + step - 1, hi)
            h, r = pums_split(year, state, cols, a, b, extra, 1)
            hdr = hdr or h
            rows += r
            a = b + 1
        return hdr, rows
    q = {"get": ",".join(cols), "for": "state:" + state, "AGEP": f"{lo}:{hi}"}
    q.update(extra or {})
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
        h, r1 = pums_split(year, state, cols, lo, mid, extra, depth + 1)
        _, r2 = pums_split(year, state, cols, mid + 1, hi, extra, depth + 1)
        return h, r1 + r2


def summary(year, state):
    q = {"get": ",".join(AGE_VARS), "for": "public use microdata area:*",
         "in": "state:" + state}
    if KEY:
        q["key"] = KEY
    return api(f"https://api.census.gov/data/{year}/acs/acs1?" + urllib.parse.urlencode(q), 4)


def num(x, d=None):
    try:
        return int(x)
    except (TypeError, ValueError):
        return d


def do(year, state):
    out = CELLS / f"cells_{year}_{state}.csv"
    if out.exists():
        return f"skip {year} {state}"
    gq = gq_var(year)
    cells = {}

    def cell(puma, sex):
        k = (str(puma).strip().zfill(5), sex)
        if k not in cells:
            cells[k] = dict.fromkeys(FIELDS[4:], 0.0)
        return cells[k]

    ah, arows = pums_split(year, state, ["PWGTP", "AGEP", "SEX", "ESR", gq, "PUMA"], 16, 29,
                           {"NATIVITY": "1", "SCHL": f"1:{cut(year)}"})
    h = {n: i for i, n in enumerate(ah)}
    for r in arows:
        if r[h[gq]] == "2":
            continue
        w, age = num(r[h["PWGTP"]]), num(r[h["AGEP"]])
        puma = r[h["PUMA"]]
        if w is None or age is None or not puma:
            continue
        esr = r[h["ESR"]]
        c = cell(puma, r[h["SEX"]])
        if 18 <= age <= 29:
            c["pop1829"] += w
            c["emp1829"] += w if esr in EMP else 0
            c["cemp1829"] += w if esr in CIV else 0
            c["lf1829"] += w if esr in LF else 0
        if 16 <= age <= 24:
            c["pop1624"] += w
            c["emp1624"] += w if esr in EMP else 0
            c["cemp1624"] += w if esr in CIV else 0
            c["lf1624"] += w if esr in LF else 0

    bh, brows = pums_split(year, state, ["PWGTP", "POBP", "PUMA"], 18, 64,
                           {"NATIVITY": "2"})
    hb = {n: i for i, n in enumerate(bh)}
    for r in brows:
        w = num(r[hb["PWGTP"]])
        puma = r[hb["PUMA"]]
        if w is None or not puma:
            continue
        c = cell(puma, "T")
        c["fb1864"] += w
        if num(r[hb["POBP"]], -1) == 303:
            c["mex1864"] += w

    s = summary(year, state)
    hs = {n: i for i, n in enumerate(s[0])}
    for r in s[1:]:
        tot = sum(max(num(r[hs[v]], 0) or 0, 0) for v in AGE_VARS)
        cell(r[hs["public use microdata area"]], "T")["pop1864"] += tot

    tmp = out.with_suffix(".tmp%d" % os.getpid())
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for (puma, sex), c in sorted(cells.items()):
            w.writerow({"year": year, "state": state, "puma": puma, "sex": sex,
                        **{k: round(v, 3) for k, v in c.items()}})
    tmp.rename(out)
    return f"ok {year} {state} pumas={len({p for p, _ in cells})}"


def main():
    tasks = [(y, s) for y in YEARS for s in STATES]
    if os.environ.get("SHUFFLE"):
        import random; random.seed(3); random.shuffle(tasks)
    stride, off = int(os.environ.get("STRIDE", "1")), int(os.environ.get("OFFSET", "0"))
    if stride > 1:
        tasks = tasks[off::stride]
    n = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "7"))) as ex:
        futs = {ex.submit(do, y, s): (y, s) for y, s in tasks}
        for fut in cf.as_completed(futs):
            y, s = futs[fut]; n += 1
            try:
                print(f"[{n}/{len(tasks)}] {fut.result()}", flush=True)
            except Exception as e:
                print(f"[{n}/{len(tasks)}] FAIL {y} {s}: {e}", flush=True)


if __name__ == "__main__":
    main()

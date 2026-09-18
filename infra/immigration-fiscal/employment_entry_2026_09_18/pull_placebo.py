"""Control-group pull: native BACHELOR'S-OR-ABOVE 18-29 employment, by PUMA and year.

This is the disconfirming test for the main design. Young college-educated natives compete
far less directly with low-skill immigrants, but they live in the same local labour markets,
so they are exposed to the same local demand shocks. If the shift-share instrument moves
their employment rate as much as it moves the no-college rate, the design is picking up
metro demand rather than skill-specific competition.

Small pull: SCHL 21-24 and NATIVITY 1 filtered server-side.
"""
import concurrent.futures as cf
import csv, json, os, pathlib, urllib.parse, urllib.request, time

HERE = pathlib.Path(__file__).parent
OUT = HERE / "_cache" / "cells_coll"
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
# Only the window endpoints are needed: every 5- and 10-year difference in the design ends
# on one of these years. The link to the Census API is too slow for a full annual panel.
YEARS = [int(y) for y in os.environ.get(
    "PUMS_YEARS", "2005,2008,2010,2013,2015,2018,2023").split(",")]
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
EMP, LF = {"1", "2", "4", "5"}, {"1", "2", "3", "4", "5"}


def schl_range(y):
    # bachelor's and above: 13-16 in the pre-2008 scheme, 21-24 from 2008
    return "13:16" if y <= 2007 else "21:24"


def gq_var(y):
    return "TYPEHUGQ" if y >= 2020 else "TYPE"


def api(url, tries=4):
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=900) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            if t == tries - 1:
                raise RuntimeError(str(e))
            time.sleep(6 * (t + 1))


def do(year, state):
    out = OUT / f"coll_{year}_{state}.csv"
    if out.exists():
        return f"skip {year} {state}"
    gq = gq_var(year)
    q = {"get": ",".join(["PWGTP", "ESR", "SEX", gq, "PUMA"]),
         "AGEP": "18:29", "SCHL": schl_range(year), "NATIVITY": "1",
         "for": "state:" + state}
    if KEY:
        q["key"] = KEY
    d = api(f"https://api.census.gov/data/{year}/acs/acs1/pums?" + urllib.parse.urlencode(q))
    h = {n: i for i, n in enumerate(d[0])}
    cells = {}
    for r in d[1:]:
        if r[h[gq]] == "2":
            continue
        puma = str(r[h["PUMA"]]).strip().zfill(5)
        try:
            w = float(r[h["PWGTP"]])
        except (TypeError, ValueError):
            continue
        esr = r[h["ESR"]]
        c = cells.setdefault((puma, r[h["SEX"]]), {"popc": 0.0, "empc": 0.0, "lfc": 0.0})
        c["popc"] += w
        c["empc"] += w if esr in EMP else 0
        c["lfc"] += w if esr in LF else 0
    tmp = out.with_suffix(".tmp%d" % os.getpid())
    with tmp.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["year", "state", "puma", "sex", "popc", "empc", "lfc"])
        wr.writeheader()
        for (puma, sex), c in sorted(cells.items()):
            wr.writerow({"year": year, "state": state, "puma": puma, "sex": sex,
                         **{k: round(v, 3) for k, v in c.items()}})
    tmp.rename(out)
    return f"ok {year} {state} pumas={len({p for p, _ in cells})}"


def main():
    tasks = [(y, s) for y in YEARS for s in STATES]
    n = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "12"))) as ex:
        futs = {ex.submit(do, y, s): (y, s) for y, s in tasks}
        for fut in cf.as_completed(futs):
            y, s = futs[fut]; n += 1
            try:
                print(f"[{n}/{len(tasks)}] {fut.result()}", flush=True)
            except Exception as e:
                print(f"[{n}/{len(tasks)}] FAIL {y} {s}: {e}", flush=True)


if __name__ == "__main__":
    main()

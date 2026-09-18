"""PUMA-level cells for the displacement-to-transfers lane.

Two server-filtered calls per state-year, because api.census.gov sustains only tens of
KB/s on this link and resets large responses.

  A  natives (NATIVITY=1) aged 18-64  -> employment, LFP and transfer-receipt cells,
     split by education (no-college = SCHL below bachelor's) and age band
  B  Mexico-born (POBP=303) aged 25-54 -> wage cells split by arrival cohort (YOEP)

Definitions
  no college   SCHL 1-12 (2005-2007), 1-20 (2008+)          [ACS recode break at 2008]
  employed     ESR in (1,2,4,5)     in labour force ESR in (1,2,3,4,5)
  SSI receipt  SSIP > 0             public assistance  PAP > 0
  SNAP         FS == 1 (household-level recipiency, asked from 2008)
  institutional group quarters (TYPE/TYPEHUGQ == 2) excluded from every cell
"""
import concurrent.futures as cf
import csv, json, os, pathlib, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
CELLS = HERE / "_cache" / "cells2"
CELLS.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
YEARS = [int(y) for y in os.environ.get("PUMS_YEARS", "2005,2008,2021,2024").split(",")]
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
EMP, LF = {"1", "2", "4", "5"}, {"1", "2", "3", "4", "5"}
TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "240"))
BIG = {"06", "48", "36", "12", "17", "42", "39", "13", "37", "26", "34", "53", "51", "04",
       "25", "29", "47", "18", "27", "22", "21", "45", "08", "24", "55", "32"}

# native cells: <band>_<edu>_<measure>
BANDS = ["2554"]
EDUS = ["nc"]
MEAS = ["pop", "emp", "lf", "ssi", "pa", "snap"]
NFIELDS = [f"{b}_{e}_{m}" for b in BANDS for e in EDUS for m in MEAS]
# Mexico-born wage cells: <cohort>_<measure>, cohort pre2000 / post2000
MCOH = ["pre2000", "post2000"]
MMEAS = ["n", "emp", "wagesum", "ftfy_n", "ftfy_wagesum", "nc_n", "nc_wagesum"]
MFIELDS = [f"mx_{c}_{m}" for c in MCOH for m in MMEAS]
FIELDS = ["year", "state", "puma"] + NFIELDS + MFIELDS


def gq_var(y):
    return "TYPEHUGQ" if y >= 2020 else "TYPE"


def cut(y):
    return 12 if y <= 2007 else 20


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


def pums_split(year, state, cols, lo, hi, extra=None, depth=0):
    """Fetch one AGEP range, halving whenever the server truncates or stalls."""
    if depth == 0 and state in BIG and hi - lo >= 6:
        step = max(2, (hi - lo + 1) // 6)
        hdr, rows, a = None, [], lo
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
        if lo >= hi or depth >= 7:
            raise
        mid = (lo + hi) // 2
        h, r1 = pums_split(year, state, cols, lo, mid, extra, depth + 1)
        _, r2 = pums_split(year, state, cols, mid + 1, hi, extra, depth + 1)
        return h, r1 + r2


def num(x, d=None):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return d


def do(year, state):
    out = CELLS / f"cells_{year}_{state}.csv"
    if out.exists():
        return f"skip {year} {state}"
    gq, ncut = gq_var(year), cut(year)
    cells = {}

    def cell(puma):
        k = str(puma).strip().zfill(5)
        if k not in cells:
            cells[k] = dict.fromkeys(FIELDS[3:], 0.0)
        return cells[k]

    # --- A: natives 25-54 below a bachelor's ------------------------------
    # Both the nativity and the education selection are pushed onto the server: this link
    # sustains ~100 KB/s in aggregate, so a row not requested is the only row that is cheap.
    # The 18-29 employment band is not re-pulled here - the employment_entry lane's
    # metro_year_panel.csv already carries it for 2005, 2008, 2010, 2013, 2015, 2018, 2023.
    cols = ["PWGTP", "ESR", "PUMA", "SSIP", "PAP", "FS", gq]
    ah, arows = pums_split(year, state, cols, 25, 54,
                           {"NATIVITY": "1", "SCHL": f"1:{ncut}"})
    h = {n: i for i, n in enumerate(ah)}
    for r in arows:
        if r[h[gq]] == "2":
            continue
        w = num(r[h["PWGTP"]])
        puma = r[h["PUMA"]]
        if w is None or not puma:
            continue
        esr = r[h["ESR"]]
        ssi = 1 if (num(r[h["SSIP"]], 0) or 0) > 0 else 0
        pa = 1 if (num(r[h["PAP"]], 0) or 0) > 0 else 0
        snap = 1 if r[h["FS"]] == "1" else 0
        c = cell(puma)
        p = "2554_nc_"
        c[p + "pop"] += w
        c[p + "emp"] += w if esr in EMP else 0
        c[p + "lf"] += w if esr in LF else 0
        c[p + "ssi"] += w * ssi
        c[p + "pa"] += w * pa
        c[p + "snap"] += w * snap

    # --- B: Mexico-born 25-54 --------------------------------------------
    bcols = ["PWGTP", "AGEP", "SCHL", "ESR", "PUMA", "YOEP", "WAGP", "WKHP", "WKW" if year <= 2018 else "WKWN", gq]
    try:
        bh, brows = pums_split(year, state, bcols, 25, 54, {"POBP": "303"})
    except Exception:
        bcols = [c for c in bcols if c not in ("WKW", "WKWN")]
        bh, brows = pums_split(year, state, bcols, 25, 54, {"POBP": "303"})
    hb = {n: i for i, n in enumerate(bh)}
    wkcol = "WKWN" if "WKWN" in hb else ("WKW" if "WKW" in hb else None)
    for r in brows:
        if r[hb[gq]] == "2":
            continue
        w, yoe = num(r[hb["PWGTP"]]), num(r[hb["YOEP"]])
        puma = r[hb["PUMA"]]
        if w is None or yoe is None or not puma:
            continue
        coh = "pre2000" if yoe < 2000 else "post2000"
        wage = num(r[hb["WAGP"]], 0) or 0
        wkhp = num(r[hb["WKHP"]], 0) or 0
        wkw = num(r[hb[wkcol]], 0) or 0 if wkcol else 0
        # WKW is a bracket code 1..6 (1 = 50-52 weeks) before 2019; WKWN is weeks.
        ftfy = wkhp >= 35 and ((wkw == 1) if wkcol == "WKW" else (wkw >= 50))
        schl = num(r[hb["SCHL"]])
        c = cell(puma)
        p = f"mx_{coh}_"
        c[p + "n"] += w
        c[p + "emp"] += w if r[hb["ESR"]] in EMP else 0
        c[p + "wagesum"] += w * wage
        if ftfy:
            c[p + "ftfy_n"] += w
            c[p + "ftfy_wagesum"] += w * wage
        if schl is not None and schl <= ncut:
            c[p + "nc_n"] += w
            c[p + "nc_wagesum"] += w * wage

    tmp = out.with_suffix(".tmp%d" % os.getpid())
    with tmp.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=FIELDS)
        wr.writeheader()
        for puma, c in sorted(cells.items()):
            wr.writerow({"year": year, "state": state, "puma": puma,
                         **{k: round(v, 2) for k, v in c.items()}})
    tmp.rename(out)
    return f"ok {year} {state} pumas={len(cells)}"


def main():
    tasks = [(y, s) for y in YEARS for s in STATES]
    stride, off = int(os.environ.get("STRIDE", "1")), int(os.environ.get("OFFSET", "0"))
    if stride > 1:
        tasks = tasks[off::stride]
    n = 0
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "8"))) as ex:
        futs = {ex.submit(do, y, s): (y, s) for y, s in tasks}
        for fut in cf.as_completed(futs):
            y, s = futs[fut]; n += 1
            try:
                print(f"[{n}/{len(tasks)}] {fut.result()}", flush=True)
            except Exception as e:
                print(f"[{n}/{len(tasks)}] FAIL {y} {s}: {e}", flush=True)


if __name__ == "__main__":
    main()

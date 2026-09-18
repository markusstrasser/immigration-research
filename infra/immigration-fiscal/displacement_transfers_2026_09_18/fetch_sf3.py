"""Census 2000 SF3 county tables: the 2000 endpoint of the pre-2008 windows, and the
pre-1990 base shares that make the shift-share instrument predetermined.

Tables
  P063     SSI in 1999 for households               _001 total HH, _002 with SSI
  P064     public assistance income in 1999          _001 total HH, _002 with PA
  P043     sex by employment status, 16+             (whole-population E/POP and LFP)
  PCT020   place of birth by year of entry by citizenship, for the foreign-born
  P001     total population

PCT020 is the reason this script exists. It gives, per county and per origin group, the
count of foreign-born residents who entered the US **before 1990**. That is a 1990-vintage
settlement pattern observed in 2000, and it is predetermined with respect to every window
this lane estimates (2000-2007 onward), which the 2000 total stock is not. The prior lane's
instrument used the Census 2000 *total* stock as the base, which is contemporaneous with the
start of the 2000-2007 window and mechanically correlated with its treatment.

Output: _cache/sf3/*.json, one file per table.
"""
import json, os, pathlib, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
OUT = HERE / "_cache" / "sf3"
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
BASE = "https://api.census.gov/data/2000/dec/sf3"
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]


def api(url, tries=4, timeout=180):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(4 + 4 * t)
    raise RuntimeError(str(last))


def labels(group):
    p = OUT / f"labels_{group}.json"
    if not p.exists():
        q = urllib.parse.urlencode({"key": KEY} if KEY else {})
        p.write_text(json.dumps(api(f"{BASE}/groups/{group}.json?{q}")))
    return json.loads(p.read_text())["variables"]


def fetch_vars(name, cols):
    """County-level pull, in column chunks (the API caps a get= list at 50 variables)."""
    out = OUT / f"{name}.json"
    if out.exists():
        return f"skip {name}"
    rows = {}
    for i in range(0, len(cols), 45):
        chunk = cols[i:i + 45]
        for st in STATES:
            q = {"get": "NAME," + ",".join(chunk), "for": "county:*", "in": "state:" + st}
            if KEY:
                q["key"] = KEY
            d = api(f"{BASE}?" + urllib.parse.urlencode(q))
            h = {n: j for j, n in enumerate(d[0])}
            for r in d[1:]:
                fips = r[h["state"]].zfill(2) + r[h["county"]].zfill(3)
                rec = rows.setdefault(fips, {"cofips": fips, "NAME": r[h["NAME"]]})
                for c in chunk:
                    try:
                        rec[c] = float(r[h[c]])
                    except (TypeError, ValueError):
                        rec[c] = None
            time.sleep(0.3)
        print(f"  {name} chunk {i//45} done, counties={len(rows)}", flush=True)
    out.write_text(json.dumps(rows))
    return f"ok {name} counties={len(rows)}"


def pct020_spec():
    """Leaf origin groups of PCT020, and for each the pre-1990 entry columns.

    A leaf is an origin whose label has no deeper origin beneath it. The entry-period
    split sits directly under the origin, so the columns wanted are the '1980 to 1989'
    and 'before 1980' totals (not their naturalized/not-a-citizen children).
    """
    v = labels("PCT020")
    est = {k: v[k]["label"] for k in v if k.startswith("PCT020")}
    origins = {}
    for k, lab in est.items():
        parts = [p for p in lab.split("!!") if p]
        if not parts or parts[0] != "Total":
            continue
        body = parts[1:]
        # entry-period node sits at the end for an origin total; citizenship one deeper
        idx = [i for i, p in enumerate(body) if p.startswith("Year of entry")]
        if len(idx) != 1 or idx[0] != len(body) - 1:
            continue
        origin = "|".join(body[:idx[0]])
        period = body[idx[0]]
        origins.setdefault(origin, {})[period] = k
    # keep only the deepest origins (no other origin extends this one)
    keys = list(origins)
    leaves = [o for o in keys if not any(x != o and x.startswith(o + "|") for x in keys)]
    pre90 = {}
    for o in leaves:
        cols = [c for p, c in origins[o].items()
                if "1980 to 1989" in p or "before 1980" in p]
        if cols:
            pre90[o] = sorted(cols)
    return pre90


if __name__ == "__main__":
    spec = pct020_spec()
    (OUT / "pct020_pre1990_spec.json").write_text(json.dumps(spec, indent=1))
    print("PCT020 leaf origins:", len(spec))
    allcols = sorted({c for cols in spec.values() for c in cols})
    print("PCT020 pre-1990 columns:", len(allcols))
    for name, cols in [
        ("p063_ssi", ["P063001", "P063002"]),
        ("p064_pa", ["P064001", "P064002"]),
        ("p043_emp", [f"P043{i:03d}" for i in range(1, 16)]),
        ("p001_pop", ["P001001"]),
        ("pct020_pre1990", allcols),
    ]:
        try:
            print(fetch_vars(name, cols), flush=True)
        except Exception as e:
            print(f"FAIL {name}: {e}", flush=True)

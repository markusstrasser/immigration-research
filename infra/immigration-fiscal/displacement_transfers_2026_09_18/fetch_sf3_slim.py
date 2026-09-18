"""Census 2000 SF3 county pull, minimal column set, one request per state.

The full-table version of this pull was abandoned: another lane in this session is pulling
ACS PUMS over the same throttled api.census.gov link and sustained throughput fell to
roughly 500 B/s, so the 20-column PCT020 pull would not have finished. Everything this
lane actually needs fits in ten columns:

  P064001/2                household public assistance income in 1999: total / with PA
  P022004..P022009         foreign-born who entered BEFORE 1990 (all origins)
  PCT020059, PCT020062     Mexico-born who entered 1980-89 and before 1980

P022 replaces the 20-column sum over PCT020's origin leaves: it is the same universe
(foreign-born by year of entry) published without the origin dimension, and the origin
dimension is only needed for Mexico, which PCT020 supplies in two columns.

Output: _cache/sf3/slim.json  {cofips: {col: value}}
"""
import json, os, pathlib, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
OUT = HERE / "_cache" / "sf3"
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
BASE = "https://api.census.gov/data/2000/dec/sf3"
COLS = (["P064001", "P064002"]
        + [f"P022{i:03d}" for i in range(4, 10)]
        + ["PCT020059", "PCT020062"])
STATES = [f"{s:02d}" for s in
          [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
           33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]


def api(url, tries=5, timeout=240):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(3 + 3 * t)
    raise RuntimeError(str(last))


def main():
    out = OUT / "slim.json"
    rows = json.loads(out.read_text()) if out.exists() else {}
    done = {k[:2] for k in rows}
    for st in STATES:
        if st in done:
            continue
        q = {"get": ",".join(COLS), "for": "county:*", "in": "state:" + st}
        if KEY:
            q["key"] = KEY
        try:
            d = api(f"{BASE}?" + urllib.parse.urlencode(q))
        except Exception as e:
            print(f"FAIL {st}: {e}", flush=True)
            continue
        h = {n: i for i, n in enumerate(d[0])}
        for r in d[1:]:
            fips = r[h["state"]].zfill(2) + r[h["county"]].zfill(3)
            rec = {}
            for c in COLS:
                try:
                    rec[c] = float(r[h[c]])
                except (TypeError, ValueError):
                    rec[c] = None
            rows[fips] = rec
        out.write_text(json.dumps(rows))
        print(f"ok {st} counties={len(rows)}", flush=True)
        time.sleep(0.3)
    print("done", len(rows))


if __name__ == "__main__":
    main()

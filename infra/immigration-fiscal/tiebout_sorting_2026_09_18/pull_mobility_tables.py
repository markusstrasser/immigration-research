"""ACS 1-year state migration flows by nativity and by income, 2010-2024.

Four published tables, two universes:
  B07007  current residence x citizenship status  -> IN-migrants to the state
  B07407  residence 1 year ago x citizenship      -> OUT-migrants from the state
  B07010  current residence x individual income   -> IN-migrants by income bracket
  B07410  residence 1 year ago x individual income-> OUT-migrants by income bracket
"Moved from different state" (B07007/B07010) and its mirror in the 1-year-ago universe
are the domestic interstate flows; "moved from abroad" is a separate line and is excluded.

These replace a per-state PUMS microdata pull, which the Census API served far too slowly
to finish (about 2.5 minutes per large state). The published tables give the same flows for
every state and year, but they do not cross nativity with income; SOI supplies the income
dimension for filers and B07010/B07410 for all residents.

Output: _cache/mobility_<group>.csv
"""
import os, sys, csv, json, time, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache")
KEY = os.environ["CENSUS_API_KEY"]
YEARS = [y for y in range(2010, 2025) if y != 2020]
GROUPS = ["B07007", "B07407", "B07010", "B07410"]


def get(url):
    for a in range(5):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            sys.stderr.write("retry %d %s\n" % (a, e))
            time.sleep(10 * (a + 1))
    raise RuntimeError(url.split("&key=")[0])


for g in GROUPS:
    out = os.path.join(CACHE, "mobility_%s.csv" % g)
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print("skip", g, flush=True)
        continue
    rows, cols = [], None
    for y in YEARS:
        d = get("https://api.census.gov/data/%d/acs/acs1?get=NAME,group(%s)&for=state:*&key=%s"
                % (y, g, KEY))
        hdr = d[0]
        keep = [i for i, h in enumerate(hdr)
                if h == "NAME" or h == "state" or (h.endswith("E") and not h.endswith("EA"))]
        names = [hdr[i] for i in keep]
        if cols is None:
            cols = ["year"] + names
        for r in d[1:]:
            rec = dict(zip(names, [r[i] for i in keep]))
            rec["year"] = y
            rows.append(rec)
        print(g, y, len(d) - 1, flush=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("wrote", out, len(rows), flush=True)

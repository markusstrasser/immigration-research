"""SF Commercial Vacancy Tax registry (Taxable Commercial Spaces, rzkk-54yv):
one row per storefront x tax year, with vacancy and filing status."""
import json, pathlib, requests, time, sys
CD = pathlib.Path(__file__).parent/"_cache"
rows, off = [], 0
while True:
    for a in range(4):
        try:
            r = requests.get("https://data.sf.gov/resource/rzkk-54yv.json",
                params={"$limit":20000,"$offset":off,"$order":"lin,taxyear"},
                timeout=240, headers={"User-Agent":"research/1.0"}); r.raise_for_status()
            d = r.json(); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(6)
    else: raise SystemExit(1)
    rows += d; off += len(d); print("got", off, flush=True)
    if len(d) < 20000: break
(CD/"sf_taxable_commercial_spaces.json").write_text(json.dumps(rows))
print("TOTAL", len(rows))
import collections
print(collections.Counter(r.get("taxyear") for r in rows).most_common())

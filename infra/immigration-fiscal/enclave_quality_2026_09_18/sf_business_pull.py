"""Active registered business locations in San Francisco (DataSF g8m3-pdis)."""
import json, pathlib, requests, time, sys
HERE = pathlib.Path(__file__).parent; CACHE = HERE/"_cache"
OUT = CACHE/"sf_active_businesses.json"
base = "https://data.sf.gov/resource/g8m3-pdis.json"
sel = ("uniqueid,dba_name,full_business_address,business_zip,location_start_date,"
       "location_end_date,location,neighborhoods_analysis_boundaries,supervisor_district")
where = "location_end_date IS NULL AND city='San Francisco' AND location IS NOT NULL"
rows, off = [], 0
while True:
    p = {"$select": sel, "$where": where, "$limit": 50000, "$offset": off,
         "$order": "uniqueid"}
    for a in range(4):
        try:
            r = requests.get(base, params=p, timeout=300,
                             headers={"User-Agent": "research/1.0"}); r.raise_for_status()
            d = r.json(); break
        except Exception as e:
            print("retry", a, e, file=sys.stderr); time.sleep(8)
    else: raise SystemExit("failed")
    rows += d; off += len(d)
    print("fetched", off, flush=True)
    if len(d) < 50000: break
OUT.write_text(json.dumps(rows))
print("active business locations:", len(rows))
from collections import Counter
c = Counter(r.get("neighborhoods_analysis_boundaries","?") for r in rows)
for k, v in c.most_common(45): print(f"{v:7d}  {k}")

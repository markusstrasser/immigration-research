"""SF 311 cases aggregated by analysis neighborhood x service_name x year, 2015-2025.
Socrata SoQL group-by, one year per request to keep each query small."""
import json, pathlib, time, requests, sys
HERE = pathlib.Path(__file__).parent; CACHE = HERE/"_cache"; CACHE.mkdir(exist_ok=True)
OUT = CACHE/"sf311_nbhd_service_year.json"
base = "https://data.sf.gov/resource/vw6y-z8j6.json"
rows = []
if OUT.exists():
    rows = json.loads(OUT.read_text())
done = {int(r["yr"]) for r in rows} if rows else set()
for yr in range(2015, 2026):
    if yr in done:
        print("skip", yr); continue
    params = {
        "$select": "analysis_neighborhood,service_name,count(1) AS n",
        "$where": f"requested_datetime >= '{yr}-01-01' AND requested_datetime < '{yr+1}-01-01'",
        "$group": "analysis_neighborhood,service_name",
        "$limit": "50000",
    }
    for attempt in range(4):
        try:
            r = requests.get(base, params=params, timeout=300,
                             headers={"User-Agent": "research/1.0"})
            r.raise_for_status()
            d = r.json()
            break
        except Exception as e:
            print(f"  {yr} attempt {attempt}: {e}", file=sys.stderr); time.sleep(10)
    else:
        print("FAILED", yr); continue
    for x in d: x["yr"] = yr
    rows.extend(d)
    print(yr, len(d), "groups", sum(int(x['n']) for x in d), "cases", flush=True)
    OUT.write_text(json.dumps(rows))
print("total rows", len(rows))

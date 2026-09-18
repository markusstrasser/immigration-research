import json, pathlib, requests, time, sys
HERE = pathlib.Path(__file__).parent; CACHE = HERE/"_cache"
rows, off = [], 0
while True:
    for a in range(4):
        try:
            r = requests.get("https://data.sf.gov/resource/qya8-uhsz.json",
                params={"$limit": 2000, "$offset": off, "$order": "objectid"},
                timeout=180, headers={"User-Agent":"research/1.0"}); r.raise_for_status()
            d = r.json(); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(6)
    else: raise SystemExit(1)
    rows += d; off += len(d); print("got", off, flush=True)
    if len(d) < 2000: break
(CACHE/"sf_street_eval_2022_2025.json").write_text(json.dumps(rows))
print("TOTAL", len(rows))

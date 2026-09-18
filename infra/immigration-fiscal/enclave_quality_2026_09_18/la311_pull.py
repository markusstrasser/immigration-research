"""MyLA311 service requests aggregated by ZIP and by neighborhood council,
2019-2025, for sanitation categories."""
import json, pathlib, requests, time, sys
CD = pathlib.Path(__file__).parent/"_cache"
SETS = {2019:"pvft-t768", 2020:"rq3b-xjk8", 2021:"97z7-y5bt", 2022:"i5ke-k6by",
        2023:"4a4x-mna2", 2024:"b7dx-7gc3", 2025:"h73f-gn57"}
def pull(rid, group, tag):
    p = {"$select": f"{group},requesttype,count(1) AS n",
         "$group": f"{group},requesttype", "$limit": 50000}
    for a in range(5):
        try:
            r = requests.get(f"https://data.lacity.org/resource/{rid}.json",
                params=p, timeout=300, headers={"User-Agent":"research/1.0"})
            r.raise_for_status(); return r.json()
        except Exception as e:
            print("retry", tag, e, file=sys.stderr); time.sleep(8)
    return []
for group, name in (("zipcode","zip"), ("ncname","nc")):
    out = CD/f"la311_{name}_type_year.json"
    rows = json.loads(out.read_text()) if out.exists() else []
    done = {r["yr"] for r in rows}
    for yr, rid in SETS.items():
        if yr in done: continue
        d = pull(rid, group, f"{yr}/{name}")
        for x in d: x["yr"] = yr
        rows += d
        print(name, yr, len(d), sum(int(x["n"]) for x in d), flush=True)
        out.write_text(json.dumps(rows))
    print(name, "TOTAL", len(rows))

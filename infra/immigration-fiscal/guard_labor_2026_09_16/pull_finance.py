"""State+local police protection and corrections direct expenditure, 2022, from Census govslocalfin timeseries."""
import json, os, pathlib, urllib.request, csv, re
HERE = pathlib.Path(__file__).resolve().parent; CACHE = HERE/"_cache"
KEY = os.environ["CENSUS_API_KEY"]
FIPS = [f for f in ("%02d"%i for i in range(1,57)) if f not in {"03","07","14","43","52"}]
labels = {}
rows = []
for st in FIPS:
    p = CACHE/f"gf_{st}.json"
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(
            f"https://api.census.gov/data/timeseries/govslocalfin?get=NAME,AGG_DESC,AGG_DESC_LABEL,AMOUNT&for=state:{st}&time=2022&key={KEY}", timeout=300).read())
    d = json.loads(p.read_text()); h = {c:i for i,c in enumerate(d[0])}
    m = {}
    for r in d[1:]:
        lab = r[h["AGG_DESC_LABEL"]]; labels[lab] = r[h["AGG_DESC"]]
        m[lab] = int(r[h["AMOUNT"]])
    rows.append((st, d[1][h["NAME"]], m))
P="Expenditure - Direct Expenditure - General Expenditure - Police Protection - Total Expenditure"
C="Expenditure - Direct Expenditure - General Expenditure - Correction - Total Expenditure"
with open(HERE/"state_finance.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["state","name","police_exp_k","corrections_exp_k"])
    for st,name,m in rows: w.writerow([st,name,m[P],m[C]])
print("states:",len(rows),"| CA police $k:",dict((s,m) for s,n,m in rows)["06"][P])

"""Rural / open-space comparison: Wildlife Conservation Board approved
acquisition projects, 2015-2024, deflated to 2024 dollars with CPI-U.

Source: WCB Approved Projects (ds672) feature service, California Department
of Fish and Wildlife / WCB.
https://services2.arcgis.com/Uq9r85Potqm3MfRV/arcgis/rest/services/biosds672_fpu/FeatureServer/0
"""
import csv, json, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")

cpi = defaultdict(list)
with open(os.path.join(CACHE, "cpi.csv")) as fh:
    for r in csv.DictReader(fh):
        v = r["CPIAUCSL"].strip()
        if v and v != ".":
            cpi[r["observation_date"][:4]].append(float(v))
CPI = {y: statistics.mean(v) for y, v in cpi.items()}
BASE = CPI["2024"]

rows = json.load(open(os.path.join(CACHE, "wcb_raw.json")))
COUNTIES = ["Los Angeles", "Orange", "San Diego", "Santa Clara", "San Bernardino"]

out = []
for c in COUNTIES:
    vals = []
    for x in rows:
        if x["County"] != c or x["Type"] != "Acquisition":
            continue
        try:
            cost = float(x["TotalCost"] or 0); ac = float(x["Acres"] or 0)
        except (TypeError, ValueError):
            continue
        if cost <= 0 or ac <= 0:
            continue
        yr = str(x["dtmBoardAp"])[:4]
        if not (isinstance(x["dtmBoardAp"], (int, float)) and x["dtmBoardAp"] > 0):
            continue
        import datetime
        yr = str(datetime.datetime.fromtimestamp(x["dtmBoardAp"] / 1000, datetime.UTC).year)
        if not yr.isdigit() or not (2015 <= int(yr) <= 2024):
            continue
        vals.append(cost / ac * BASE / CPI[yr])
    if not vals:
        continue
    v = sorted(vals)
    q1, q3 = statistics.quantiles(v, n=4, method="inclusive")[0], statistics.quantiles(v, n=4, method="inclusive")[2]
    out.append({"county": c, "n_projects": len(v),
                "median_per_acre_2024": round(statistics.median(v)),
                "q1_per_acre_2024": round(q1), "q3_per_acre_2024": round(q3)})

with open(os.path.join(HERE, "rural_wcb_summary.csv"), "w", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(out)
for r in out:
    print(r)

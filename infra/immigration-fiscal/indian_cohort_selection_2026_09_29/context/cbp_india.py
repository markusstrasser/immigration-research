"""CBP nationwide encounters, citizenship = INDIA, by fiscal year x land-border region x component.

Inputs: CBP 'Nationwide Encounters' AOR CSVs (cbp.gov/newsroom/stats/nationwide-encounters).
Encounters are events, not unique persons. Latest release wins for each FY; overlaps are cross-checked.
"""
import csv, collections, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[4]
LANE = pathlib.Path(__file__).resolve().parents[1]
FILES = [  # (path, FYs taken from this file) -- newest release first
    (ROOT / "sources/immigration-fiscal/data/external/cbp/nationwide-encounters-fy22-fy25-aor.csv", {2022, 2023, 2024, 2025}),
    (ROOT / "sources/immigration-fiscal/data/external/cbp/nationwide-encounters-fy21-fy24-aor.csv", set()),
    (LANE / "_cache/context/ne-fy20-fy23-aor.csv", {2020, 2021}),
]
def load(p):
    t = collections.Counter()
    with open(p, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r["Citizenship"] or "").strip() == "INDIA":
                t[(int(r["Fiscal Year"]), r["Land Border Region"], r["Component"])] += int(r["Encounter Count"].replace(",", ""))
    return t
tabs = {p: load(p) for p, _ in FILES}
for p, _ in FILES:
    print(p.name, hashlib.sha256(p.read_bytes()).hexdigest(), file=sys.stderr)
# cross-check overlapping FYs between releases
fytot = {p: collections.Counter() for p in tabs}
for p, t in tabs.items():
    for (fy, _, _), n in t.items(): fytot[p][fy] += n
for p in tabs: print("FY totals", p.name, dict(sorted(fytot[p].items())), file=sys.stderr)
rows = []
for p, fys in FILES:
    for (fy, reg, comp), n in sorted(tabs[p].items()):
        if fy in fys: rows.append([fy, reg, comp, n, p.name])
out = LANE / "context/cbp_india_encounters_fy2020_2025.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["fiscal_year", "land_border_region", "component", "encounters", "source_file"])
    w.writerows(sorted(rows))
summ = collections.defaultdict(collections.Counter)
for fy, reg, comp, n, _ in rows:
    summ[fy]["total"] += n
    key = {"Southwest Land Border": "swb", "Northern Land Border": "nb", "Other": "other"}[reg]
    summ[fy][key] += n
    summ[fy]["usbp" if comp == "U.S. Border Patrol" else "ofo"] += n
    if key == "swb" and comp == "U.S. Border Patrol": summ[fy]["swb_usbp"] += n
    if key == "nb" and comp == "U.S. Border Patrol": summ[fy]["nb_usbp"] += n
cols = ["total", "swb", "swb_usbp", "nb", "nb_usbp", "other", "usbp", "ofo"]
with open(LANE / "context/cbp_india_encounters_summary.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["fiscal_year"] + cols)
    for fy in sorted(summ):
        w.writerow([fy] + [summ[fy][c] for c in cols]); print(fy, [summ[fy][c] for c in cols])

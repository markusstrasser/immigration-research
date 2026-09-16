"""ACS 2020-2024 5-year PUMS: institutional GQ rates, native men 18-39, by detailed Hispanic origin and Asian
detail, to de-noise the small-origin cells in memo §5 / ladder 74. Same construction as pull_and_compute.py
(TYPEHUGQ=2 institutional; NATIVITY=1 native), pooled five years."""
import csv, json, os, pathlib, urllib.request
HERE = pathlib.Path(__file__).resolve().parent
KEY = os.environ.get("CENSUS_API_KEY", "")
BASE = "https://api.census.gov/data/2024/acs/acs5/pums?tabulate=weight(PWGTP)&col+TYPEHUGQ&row+NATIVITY&SEX=1&AGEP=18:39"
HISP = {"02": "Mexican", "03": "Puerto Rican", "04": "Cuban", "05": "Dominican", "07": "Guatemalan", "08": "Honduran",
        "11": "Salvadoran", "16": "Colombian", "24": "Other Hispanic (generic)"}
ASIAN = {"4000": "Chinese", "4008": "Filipino", "4001": "Hmong", "4015": "Indian", "4003": "Korean",
         "4010": "Laotian", "4014": "Vietnamese", "4007": "Cambodian"}  # 2024 RAC2P codes (rac2p_2024.json)
def fetch(tag, pred):
    out = HERE / f"acs5_{tag}.json"
    if not out.exists():
        out.write_bytes(urllib.request.urlopen(f"{BASE}&{pred}&key={KEY}", timeout=180).read())
    return json.loads(out.read_text())
def rates(tab):
    cols = {list(c.values())[0]: i for i, c in enumerate(tab[0][:-1])}
    res = {}
    for r in tab[1:]:
        tot = sum(r[i] for i in cols.values()); res[r[-1]] = (r[cols["2"]], tot, r[cols["2"]] / tot * 100)
    return res
rows = []
def add(block, name, tab):
    for nat, (inst, tot, pct) in rates(tab).items():
        rows.append((block, name, "native" if nat == "1" else "foreign_born", inst, tot, round(pct, 3)))
add("nh_race", "NH White", fetch("nhwhite", "HISP=01&RAC1P=1"))
add("nh_race", "NH Black", fetch("nhblack", "HISP=01&RAC1P=2"))
for code, name in HISP.items():
    add("hispanic_origin", name, fetch(f"hisp{code}", f"HISP={code}"))
# RAC2P is not exposed on the 5-year PUMS API (unknown predicate/dimension, 2026-09-16); Asian detail stays 1-year only.
white = next(r[5] for r in rows if r[1] == "NH White" and r[2] == "native")
with open(HERE / "acs5_2020_2024_origins.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["block", "group", "nativity", "institutional", "population", "pct", "ratio_to_nh_white_native"])
    for r in rows:
        w.writerow([*r, round(r[5] / white, 3)])
print(f"{'group':28}{'nativity':>13}{'inst':>10}{'pop':>12}{'pct':>7}{'ratio':>7}")
for r in rows:
    print(f"{r[1]:28}{r[2]:>13}{r[3]:10,}{r[4]:12,}{r[5]:7.3f}{r[5]/white:7.2f}")

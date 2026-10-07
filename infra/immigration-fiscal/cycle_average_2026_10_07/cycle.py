"""Cycle position of income-year 2024 and a first-order cost of a cycle-average year.

Inputs: FRED fredgraph CSVs in inputs/ (BLS CPS LNU04000009, UNRATENSA=LNU04000000,
LNU02300009, LNU02300000; CBO GDPPOT, BEA GDPC1). Writes derived/annual.csv, derived/result.json.
"""
import csv, json, pathlib
import numpy as np

HERE = pathlib.Path(__file__).parent
IN, OUT = HERE / "inputs", HERE / "derived"
RECEIPTS_BN = 488.5   # group receipts after data corrections (backcast memo; corrections lane)
LABOR_SHARE = (0.75, 0.90)   # [ASSUMPTION] share of receipts that scales with employment
TRANSFER_PER_JOB = (5_000, 15_000)  # [ASSUMPTION] UI+SNAP+Medicaid per lost job, $
EMPLOYED_M = 18.0     # [ASSUMPTION] employed members, ~39.7M x 0.70 adults x 0.65 EPOP


def annual(name):
    d = {}
    for r in csv.DictReader(open(IN / f"{name}.csv")):
        v = list(r.values())
        if v[1] in ("", "."):
            continue
        d.setdefault(int(v[0][:4]), []).append(float(v[1]))
    return {y: sum(x) / len(x) for y, x in d.items()}


uh, ut = annual("LNU04000009"), annual("UNRATENSA")
eh, et = annual("LNU02300009"), annual("LNU02300000")
pot, gdp = annual("GDPPOT"), annual("GDPC1")
years = list(range(2005, 2025))
rows = []
for y in years:
    rows.append(dict(year=y, u_hisp=uh[y], u_total=ut[y], u_gap=uh[y] - ut[y],
                     epop_hisp=eh[y], epop_total=et[y],
                     output_gap_pct=100 * (gdp[y] / pot[y] - 1)))
OUT.mkdir(exist_ok=True)
with open(OUT / "annual.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})

# Hispanic EPOP on a linear trend plus the output gap, 2005-2024 excluding nothing.
X = np.array([[1, r["year"] - 2024, r["output_gap_pct"]] for r in rows])
fits = {}
for key in ("epop_hisp", "epop_total"):
    b = np.linalg.lstsq(X, np.array([r[key] for r in rows]), rcond=None)[0]
    fits[key] = b.tolist()
gap24 = rows[-1]["output_gap_pct"]
res = {"output_gap_2024": gap24, "u_hisp_2024": uh[2024], "u_total_2024": ut[2024],
       "fits_const_trend_gap": fits, "windows": {}}
for lab, (a, z) in {"2005-2024": (2005, 2024), "2007-2019": (2007, 2019)}.items():
    sel = [r for r in rows if a <= r["year"] <= z]
    g = sum(r["output_gap_pct"] for r in sel) / len(sel)
    ug = sum(r["u_gap"] for r in sel) / len(sel)
    win = {"mean_output_gap": g, "mean_u_gap": ug, "u_gap_2024": rows[-1]["u_gap"]}
    for key in ("epop_hisp", "epop_total"):
        win[f"d_{key}_pp"] = fits[key][2] * (g - gap24)
    # group's own shortfall (absolute) and its excess over the nation (relative)
    for lab2, dpp in (("absolute", win["d_epop_hisp_pp"]),
                      ("excess", win["d_epop_hisp_pp"] - win["d_epop_total_pp"] * eh[2024] / et[2024])):
        frac = dpp / eh[2024]
        lo = -frac * (RECEIPTS_BN * LABOR_SHARE[0] + EMPLOYED_M * TRANSFER_PER_JOB[0] / 1e3)
        hi = -frac * (RECEIPTS_BN * LABOR_SHARE[1] + EMPLOYED_M * TRANSFER_PER_JOB[1] / 1e3)
        win[lab2] = {"d_epop_pp": dpp, "frac_jobs": frac, "cost_bn": [lo, hi]}
    res["windows"][lab] = win
json.dump(res, open(OUT / "result.json", "w"), indent=1, sort_keys=True)
open(OUT / "result.json", "a").write("\n")
print(json.dumps(res, indent=1))

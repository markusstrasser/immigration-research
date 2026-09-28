"""Per-capita CE 2024 spending by reference-person group: total and the energy lines.

Ratios feed the PM2.5 scaling (Tessum's Hispanic figure -> Mexican-origin union) and the
CO2 footprint arm. Each FMLI record is one CU-quarter; spending = previous-quarter (PQ) +
current-quarter (CQ) parts, both inside the three-month reference period, so pooling the five
files and dividing by weighted persons gives a ratio that annualization would not change.
"""
import csv
import io
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
ZIP = HERE.parent / "consumption_key_2026_09_24/_cache/sources/intrvw24.zip"
FILES = ["fmli241x.csv", "fmli242.csv", "fmli243.csv", "fmli244.csv", "fmli251.csv"]
LINES = {"total": "TOTEXP", "gasoline": "GASMO", "electricity": "ELCTRC", "natural_gas": "NTLGAS",
         "other_fuels": "ALLFUL", "transport": "TRANS", "housing": "HOUS", "utilities": "UTIL"}
KEEP = ["NEWID", "FINLWT21", "FAM_SIZE", "HORREF1", "HISP_REF", "REF_RACE"] + [
    f"{v}{q}" for v in LINES.values() for q in ("PQ", "CQ")]

frames = []
with zipfile.ZipFile(ZIP) as z:
    for f in FILES:
        d = pd.read_csv(z.open(f"intrvw24/{f}"), usecols=lambda c: c in KEEP, low_memory=False)
        frames.append(d)
d = pd.concat(frames, ignore_index=True)
for c in KEEP[1:]:
    d[c] = pd.to_numeric(d[c], errors="coerce")
for name, v in LINES.items():
    d[name] = d[f"{v}PQ"].fillna(0) + d[f"{v}CQ"].fillna(0)
d["energy_home"] = d.electricity + d.natural_gas + d.other_fuels
d["energy_all"] = d.energy_home + d.gasoline
groups = {
    "all": d.FINLWT21 > 0,
    "hispanic": d.HISP_REF.eq(1),
    "mexican_origin": d.HORREF1.isin([1, 2, 3]),  # same definition as consumption_key_2026_09_24/ce_pumd.py
    "nh_black": d.REF_RACE.eq(2) & d.HISP_REF.ne(1),
}
rows = []
cols = list(LINES) + ["energy_home", "energy_all"]
for g, m in groups.items():
    x = d[m]
    persons = (x.FINLWT21 * x.FAM_SIZE).sum()
    row = {"group": g, "cu_quarters": int(m.sum()), "weighted_persons_q": persons,
           "persons_per_cu": persons / x.FINLWT21.sum()}
    for c in cols:
        row[f"{c}_pc_q"] = (x.FINLWT21 * x[c]).sum() / persons
    rows.append(row)
out = pd.DataFrame(rows)
base = out.set_index("group").loc["all"]
for c in cols:
    out[f"{c}_ratio_to_all"] = out[f"{c}_pc_q"] / base[f"{c}_pc_q"]
out.to_csv(HERE / "derived/ce_group_spending.csv", index=False, lineterminator="\n")
show = ["group", "cu_quarters", "persons_per_cu"] + [f"{c}_ratio_to_all" for c in cols]
print(out[show].round(3).to_string(index=False))
print("mex/hisp total ratio", round(out.set_index("group").loc["mexican_origin", "total_pc_q"] /
                                  out.set_index("group").loc["hispanic", "total_pc_q"], 4))

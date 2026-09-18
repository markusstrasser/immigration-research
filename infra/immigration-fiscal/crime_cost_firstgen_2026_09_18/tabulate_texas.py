"""Tabulate Light–He–Robey (PNAS 2020, openICPSR 124923) Texas felony arrests by status × offence, 2012–2018."""
import pandas as pd
pd.set_option("display.width", 250)
C = "infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/_cache/light_texas/"
def load(f):
    d = pd.read_stata(C + f)
    d["category"] = d["category"].astype("string").fillna("NA")
    return d
for f in ["detailed_category.dta", "detailed_category_pew.dta", "big_category.dta", "felony_report.dta"]:
    d = load(f)
    print(f"\n=== {f}  years {sorted(d.year.unique())}")
    ch = [c for c in d.columns if c.endswith("_charge") or c == "total_charge_incidents"]
    print(d.groupby("category")[ch].sum().to_string())
    pop = [c for c in ["tot_citizen", "pop_undoc", "tot_legal2_immi", "tot_pop"] if c in d.columns]
    print(d.groupby("year")[pop].first().to_string())

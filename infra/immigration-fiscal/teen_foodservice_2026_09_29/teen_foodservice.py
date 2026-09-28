"""Who works in fast food and food preparation, and teen employment, by race and nativity. CPS ASEC 2025 (March 2025).

Question (operator, 2026-09-29): is the "lazy white teen who won't flip burgers" a myth, and are Black
workers the ones missing from menial jobs?
Employed = PEMLR 1 or 2 in the March reference week. Occupation = PEIOOCC, Census 2018 codes:
food-service = 4020 cooks, 4030 food preparation, 4055 fast food and counter, 4110 waiters,
4120 non-restaurant servers, 4130 dining attendants and bussers, 4140 dishwashers, 4150 hosts.
Foreign-born = PRCITSHP 4 or 5. The survey observes jobs held, not how well the work is done.
"""
import csv
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ZIP = HERE.parents[2] / "sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
FOOD = {4020, 4030, 4055, 4110, 4120, 4130, 4140, 4150}
FAST = {4055}


def load():
    with zipfile.ZipFile(ZIP) as z, z.open("pppub25.csv") as f:
        p = pd.read_csv(f, usecols=["A_AGE", "PRDTRACE", "PEHSPNON", "PRCITSHP", "PEMLR", "PEIOOCC", "MARSUPWT", "A_ENRLW"])
    p["w"] = p["MARSUPWT"] / 100
    hisp = p["PEHSPNON"] == 1
    fb = p["PRCITSHP"].isin([4, 5])
    p["grp"] = "Other US-born"
    p.loc[~hisp & (p["PRDTRACE"] == 1) & ~fb, "grp"] = "White US-born"
    p.loc[~hisp & (p["PRDTRACE"] == 2) & ~fb, "grp"] = "Black US-born"
    p.loc[hisp & ~fb, "grp"] = "Hispanic US-born"
    p.loc[fb, "grp"] = "Foreign-born"
    p["emp"] = p["PEMLR"].isin([1, 2])
    return p


def main():
    p = load()
    rows = []
    teen = p[(p["A_AGE"] >= 16) & (p["A_AGE"] <= 19)]
    young = p[(p["A_AGE"] >= 16) & (p["A_AGE"] <= 24)]
    food = p[p["emp"] & p["PEIOOCC"].isin(FOOD)]
    fast = p[p["emp"] & p["PEIOOCC"].isin(FAST)]
    allemp = p[p["emp"] & (p["A_AGE"] >= 16)]
    for g in ["White US-born", "Black US-born", "Hispanic US-born", "Other US-born", "Foreign-born"]:
        t, y = teen[teen["grp"] == g], young[young["grp"] == g]
        rows.append(dict(
            group=g,
            teen_16_19_pop_m=round(t["w"].sum() / 1e6, 2),
            teen_employment_rate=round((t["w"] * t["emp"]).sum() / t["w"].sum(), 3),
            teen_n=len(t),
            young_16_24_employment_rate=round((y["w"] * y["emp"]).sum() / y["w"].sum(), 3),
            share_of_all_workers=round(allemp.loc[allemp["grp"] == g, "w"].sum() / allemp["w"].sum(), 3),
            share_of_food_service_workers=round(food.loc[food["grp"] == g, "w"].sum() / food["w"].sum(), 3),
            share_of_fast_food_counter_workers=round(fast.loc[fast["grp"] == g, "w"].sum() / fast["w"].sum(), 3),
            food_n=int((food["grp"] == g).sum()),
        ))
    (HERE / "derived").mkdir(exist_ok=True)
    with open(HERE / "derived/teen_foodservice.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"food-service workers {food['w'].sum()/1e6:.2f}M (n={len(food)}); fast food/counter {fast['w'].sum()/1e6:.2f}M (n={len(fast)})")


if __name__ == "__main__":
    main()

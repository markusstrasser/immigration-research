"""Does ACS earnings allocation narrow or widen the Mexican-origin vs native NH white gap?

Household residents 25-54 with positive earnings (PERNP > 0, ADJINC applied). For each group and
education cell, compares allocated (FPERNP=1) with reported earnings, then the group/white ratio
of mean earnings with and without allocated records. Writes derived/acs_earn_alloc_<YEAR>.csv.
Usage: acs_earn_alloc.py YEAR [YEAR ...]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def edu(schl):
    return pd.cut(schl, [0, 15, 17, 20, 21, 24], labels=["lt_hs", "hs", "some_col", "ba", "grad"])


def run(year):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{year}.parquet",
                        columns=["RELSHIPP", "AGEP", "HISP", "RAC1P", "NATIVITY", "POBP", "SCHL",
                                 "PERNP", "FPERNP", "ADJINC", "PWGTP", "WAGP"])
    d = d[d.RELSHIPP.lt(37) & d.AGEP.between(25, 54) & d.PERNP.gt(0)].copy()
    d["earn"] = d.PERNP * d.ADJINC / 1e6
    d["edu"] = edu(d.SCHL)
    d["alloc"] = d.FPERNP.eq(1)
    groups = {"mexico_born": d.POBP.eq(303), "usborn_mexican": d.NATIVITY.eq(1) & d.HISP.eq(2),
              "native_nh_white": d.NATIVITY.eq(1) & d.HISP.eq(1) & d.RAC1P.eq(1)}
    rows = []
    for g, m in groups.items():
        s = d[m]
        wm = lambda t: float(np.average(t.earn, weights=t.PWGTP)) if len(t) else np.nan
        rows.append(dict(year=year, group=g, edu="all", n=len(s),
                         alloc_share=float(np.average(s.alloc, weights=s.PWGTP)),
                         mean_all=wm(s), mean_reported=wm(s[~s.alloc]), mean_allocated=wm(s[s.alloc])))
        for e, t in s.groupby("edu", observed=True):
            rows.append(dict(year=year, group=g, edu=str(e), n=len(t),
                             alloc_share=float(np.average(t.alloc, weights=t.PWGTP)),
                             mean_all=wm(t), mean_reported=wm(t[~t.alloc]), mean_allocated=wm(t[t.alloc])))
    r = pd.DataFrame(rows)
    r["allocated_over_reported"] = r.mean_allocated / r.mean_reported
    w = r[r.group.eq("native_nh_white")].set_index("edu")
    for col in ["mean_all", "mean_reported"]:
        r[f"ratio_to_white_{col}"] = r[col] / r.edu.map(w[col])
    r.to_csv(HERE / "derived" / f"acs_earn_alloc_{year}.csv", index=False)
    return r


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    for y in map(int, sys.argv[1:]):
        print(run(y).round(3).to_string(index=False))

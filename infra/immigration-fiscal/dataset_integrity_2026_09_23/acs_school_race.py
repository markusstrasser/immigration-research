"""Two ACS checks per year: (1) school attendance items for children 5-17 in households
(allocation of SCH/SCHG, public K-12 share, national pupil total vs NCES), (2) the race coding
break: native non-Hispanic white alone vs alone-or-in-combination and the multiracial white group.
Writes derived/acs_school_<YEAR>.csv and derived/acs_race_<YEAR>.csv.
Usage: acs_school_race.py YEAR [YEAR ...]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def wshare(mask, w):
    return float((w * mask).sum() / w.sum())


def school(d, year):
    k = d[d.RELSHIPP.lt(37) & d.AGEP.between(5, 17)]
    groups = {"all": pd.Series(True, index=k.index),
              "hisp02_child": k.HISP.eq(2),
              "native_nh_white_child": k.NATIVITY.eq(1) & k.HISP.eq(1) & k.RAC1P.eq(1)}
    rows = []
    for g, m in groups.items():
        s = k[m]
        pupil = s.SCH.eq(2) & s.SCHG.between(2, 14)
        rows.append(dict(year=year, group=g, n=len(s), children=float(s.PWGTP.sum()),
                         public_k12_share=wshare(pupil, s.PWGTP),
                         private_share=wshare(s.SCH.eq(3), s.PWGTP),
                         not_attending_share=wshare(s.SCH.eq(1), s.PWGTP),
                         FSCHP=wshare(s.FSCHP.eq(1), s.PWGTP),
                         FSCHGP=wshare(s.FSCHGP.eq(1), s.PWGTP),
                         pupil_total_all_ages_hh_and_gq=float(
                             d.PWGTP[d.SCH.eq(2) & d.SCHG.between(2, 14)].sum()) if g == "all" else np.nan))
    return pd.DataFrame(rows)


def race(d, year):
    n = d[d.NATIVITY.eq(1) & d.HISP.eq(1)]
    rows = []
    for label, m in [("nh_white_alone", n.RAC1P.eq(1)),
                     ("nh_white_in_combination_multirace", n.RACWHT.eq(1) & n.RAC1P.ne(1)),
                     ("nh_some_other_race_alone", n.RAC1P.eq(8)),
                     ("nh_all", pd.Series(True, index=n.index))]:
        s = n[m]
        a = s[s.AGEP.between(25, 64)]
        rows.append(dict(year=year, group=label, pop_m=float(s.PWGTP.sum()) / 1e6,
                         share_ba_plus_25_64=wshare(a.SCHL.ge(21), a.PWGTP),
                         share_lt_hs_25_64=wshare(a.SCHL.le(15), a.PWGTP),
                         mean_age=float(np.average(s.AGEP, weights=s.PWGTP)),
                         inst_rate_18_64=wshare(s.RELSHIPP[s.AGEP.between(18, 64)].eq(37),
                                                s.PWGTP[s.AGEP.between(18, 64)])))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    cols = ["RELSHIPP", "AGEP", "HISP", "RAC1P", "RACWHT", "NATIVITY", "SCH", "SCHG", "SCHL",
            "FSCHP", "FSCHGP", "PWGTP"]
    for y in map(int, sys.argv[1:]):
        d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet", columns=cols)
        s = school(d, y); s.to_csv(HERE / "derived" / f"acs_school_{y}.csv", index=False)
        r = race(d, y); r.to_csv(HERE / "derived" / f"acs_race_{y}.csv", index=False)
        print(s.round(4).to_string(index=False)); print(r.round(4).to_string(index=False))

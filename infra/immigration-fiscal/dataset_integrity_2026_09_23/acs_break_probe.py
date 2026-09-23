"""Where does the post-2019 'no schooling completed' jump sit, and how stable are the
institutional Hispanic-origin counts year to year?

(1) SCHL=1 share among ages 25+ (households), reported education only (FSCHLP=0), for:
    Mexico-born who arrived at age 20+ in 1975-2009 (the ladder-197 fixed population), split by
    English ability (ENG 3-4 = 'not well'/'not at all' vs other); Central American-born; natives
    65+. (2) Institutional 18-64 weighted counts by HISP code and nativity.
Writes derived/acs_noschool_break.csv, derived/acs_inst_hisp_series.csv.
Usage: acs_break_probe.py YEAR [YEAR ...]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CENTRAL_AMERICA = {310, 311, 312, 313, 314, 315, 316}  # Belize..Panama POBP codes (2019+ dictionary)


def share(t):
    return float((t.PWGTP * t.SCHL.eq(1)).sum() / t.PWGTP.sum()) if len(t) else np.nan


def main(years):
    nos, inst = [], []
    for y in years:
        d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet")
        if "RELSHIPP" not in d:  # pre-2019 RELP: 16 institutional, 17 other GQ
            d["RELSHIPP"] = d.RELP.map({16: 37, 17: 38}).fillna(0)
        hh = d[d.RELSHIPP.lt(37) & d.AGEP.ge(25) & d.FSCHLP.ne(1)]
        arr_age = hh.YOEP - (y - hh.AGEP)
        mex = hh[hh.POBP.eq(303) & hh.YOEP.between(1975, 2009) & arr_age.ge(20)]
        cells = {
            "mexborn_fixed_all": mex,
            "mexborn_fixed_poor_english": mex[mex.ENG.isin([3, 4])],
            "mexborn_fixed_english_well": mex[mex.ENG.isin([1, 2]) | mex.ENG.isna()],
            "central_american_born_25plus": hh[hh.POBP.isin(CENTRAL_AMERICA)],
            "native_65plus": hh[hh.NATIVITY.eq(1) & hh.AGEP.ge(65)],
        }
        for k, t in cells.items():
            nos.append(dict(year=y, cell=k, n=len(t), no_schooling_share=share(t)))
        # allocation rate of education in the fixed Mexican population (all records)
        allm = d[d.RELSHIPP.lt(37) & d.AGEP.ge(25) & d.POBP.eq(303)]
        nos.append(dict(year=y, cell="mexborn_25plus_FSCHLP_rate", n=len(allm),
                        no_schooling_share=float((allm.PWGTP * allm.FSCHLP.eq(1)).sum() / allm.PWGTP.sum())))
        i = d[d.RELSHIPP.eq(37) & d.AGEP.between(18, 64)]
        for (h, fb), t in i.groupby([np.where(i.HISP.eq(1), 0, np.where(i.HISP.isin([2, 24]), i.HISP, 99)),
                                     i.NATIVITY.eq(2)]):
            inst.append(dict(year=y, hisp=int(h), foreign_born=bool(fb), n=len(t), weighted=float(t.PWGTP.sum())))
    a = pd.DataFrame(nos); b = pd.DataFrame(inst)
    a.to_csv(HERE / "derived" / "acs_noschool_break.csv", index=False)
    b.to_csv(HERE / "derived" / "acs_inst_hisp_series.csv", index=False)
    pd.set_option("display.width", 200)
    print(a.pivot(index="cell", columns="year", values="no_schooling_share").round(4).to_string())
    print(b.pivot_table(index=["hisp", "foreign_born"], columns="year", values="weighted").round(0).to_string())


if __name__ == "__main__":
    main([int(y) for y in sys.argv[1:]])

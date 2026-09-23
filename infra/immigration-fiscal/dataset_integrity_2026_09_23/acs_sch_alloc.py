"""Public K-12 share among children 5-17 (households) by SCH allocation status and group."""
import sys
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
rows = []
for y in map(int, sys.argv[1:]):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet",
                        columns=["RELSHIPP", "AGEP", "HISP", "RAC1P", "NATIVITY", "SCH", "SCHG", "FSCHP", "PWGTP"])
    k = d[d.RELSHIPP.lt(37) & d.AGEP.between(5, 17)].copy()
    k["pupil"] = k.SCH.eq(2) & k.SCHG.between(2, 14)
    k["grp"] = "other"
    k.loc[k.HISP.eq(2), "grp"] = "hisp02"
    k.loc[k.NATIVITY.eq(1) & k.HISP.eq(1) & k.RAC1P.eq(1), "grp"] = "native_nh_white"
    for (g, a), t in k.groupby(["grp", k.FSCHP.eq(1)]):
        rows.append(dict(year=y, group=g, sch_allocated=bool(a), n=len(t), pop=float(t.PWGTP.sum()),
                         public_k12=float((t.PWGTP * t.pupil).sum() / t.PWGTP.sum()),
                         private_or_home=float((t.PWGTP * t.SCH.eq(3)).sum() / t.PWGTP.sum())))
r = pd.DataFrame(rows); r.to_csv(HERE / "derived" / "acs_sch_alloc.csv", index=False)
print(r.round(4).to_string(index=False))

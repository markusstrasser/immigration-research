"""Mexico-born (POBP=303) institutional residents 18-64 by Hispanic-origin code and year:
does the generic 'Other Hispanic' code absorb people whose birthplace is Mexico?"""
import sys
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
rows = []
for y in map(int, sys.argv[1:]):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet",
                        columns=["RELSHIPP", "AGEP", "HISP", "POBP", "PWGTP", "FPOBP"])
    for res, m in [("inst", d.RELSHIPP.eq(37)), ("household", d.RELSHIPP.lt(37))]:
        t = d[m & d.AGEP.between(18, 64) & d.POBP.eq(303)]
        w = t.PWGTP.sum()
        rows.append(dict(year=y, residence=res, n=len(t), mexico_born=float(w),
                         hisp02=float(t.PWGTP[t.HISP.eq(2)].sum() / w),
                         hisp24=float(t.PWGTP[t.HISP.eq(24)].sum() / w),
                         not_hispanic=float(t.PWGTP[t.HISP.eq(1)].sum() / w),
                         other_code=float(t.PWGTP[~t.HISP.isin([1, 2, 24])].sum() / w)))
r = pd.DataFrame(rows); r.to_csv(HERE / "derived" / "acs_mexborn_inst_hisp.csv", index=False)
print(r.round(4).to_string(index=False))

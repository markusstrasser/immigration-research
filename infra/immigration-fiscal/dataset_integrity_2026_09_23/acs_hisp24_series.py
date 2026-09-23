"""Share of Hispanic adults 18-64 coded generic 'Other Hispanic' (HISP 24) by residence and year,
and the Mexican-coded share of Hispanic institutional residents, natives and foreign-born."""
import sys
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
rows = []
for y in map(int, sys.argv[1:]):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet",
                        columns=["RELSHIPP", "AGEP", "HISP", "NATIVITY", "PWGTP", "FHISP"])
    h = d[d.AGEP.between(18, 64) & d.HISP.gt(1)]
    for res, m in [("household", h.RELSHIPP.lt(37)), ("inst", h.RELSHIPP.eq(37)), ("noninst_gq", h.RELSHIPP.eq(38))]:
        for nat in (1, 2):
            t = h[m & h.NATIVITY.eq(nat)]
            w = t.PWGTP.sum()
            rows.append(dict(year=y, residence=res, nativity=nat, hispanic_pop=float(w),
                             hisp24_share=float(t.PWGTP[t.HISP.eq(24)].sum() / w),
                             mexican_share=float(t.PWGTP[t.HISP.eq(2)].sum() / w),
                             fhisp_share=float(t.PWGTP[t.FHISP.eq(1)].sum() / w)))
r = pd.DataFrame(rows); r.to_csv(HERE / "derived" / "acs_hisp24_series.csv", index=False)
pd.set_option("display.width", 200)
print(r.pivot_table(index=["residence", "nativity"], columns="year", values=["hisp24_share", "mexican_share"]).round(3).to_string())

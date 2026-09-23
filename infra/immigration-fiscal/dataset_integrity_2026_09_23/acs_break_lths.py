"""Fixed Mexico-born population (arrived 1975-2009 at 20+, 25+, households, education reported):
share below high school, share with no schooling, and mean years (SCHL mapped to years), by year."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
HERE = Path(__file__).resolve().parent
YEARS_OF = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10, 14: 11,
            15: 12, 16: 12, 17: 12, 18: 13, 19: 14, 20: 14, 21: 16, 22: 18, 23: 19, 24: 20}
rows = []
for y in map(int, sys.argv[1:]):
    d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet")
    if "RELSHIPP" not in d:
        d["RELSHIPP"] = d.RELP.map({16: 37, 17: 38}).fillna(0)
    h = d[d.RELSHIPP.lt(37) & d.AGEP.ge(25) & d.FSCHLP.ne(1) & d.POBP.eq(303) & d.YOEP.between(1975, 2009)]
    h = h[(h.YOEP - (y - h.AGEP)).ge(20)]
    w = h.PWGTP
    rows.append(dict(year=y, n=len(h), lt_hs=float((w * h.SCHL.le(15)).sum() / w.sum()),
                     no_school=float((w * h.SCHL.eq(1)).sum() / w.sum()),
                     grades_1_6=float((w * h.SCHL.between(4, 9)).sum() / w.sum()),
                     mean_years=float(np.average(h.SCHL.map(YEARS_OF), weights=w))))
r = pd.DataFrame(rows); r.to_csv(HERE / "derived" / "acs_break_lths.csv", index=False)
print(r.round(4).to_string(index=False))

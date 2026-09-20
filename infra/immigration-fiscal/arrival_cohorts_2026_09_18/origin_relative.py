"""Mean years of schooling of Mexico-born US arrivals at entry, against the Mexican origin trend.

Migrant side: IPUMS panel, Mexico-born aged 25-54, arrived within the previous five years, in each
survey. Harmonised EDUC is mapped to years of schooling at category midpoints; the mapping is crude
in levels but the same in every survey year, so the CHANGE across surveys is the object of interest.

Origin side: INEGI, grado promedio de escolaridad, population aged 15 and over, Censo de Poblacion
y Vivienda 2000/2010/2020, Conteo 2005, Encuesta Intercensal 2015 --
https://cuentame.inegi.org.mx/poblacion/escolaridad.aspx (fetched 2026-09-18):
  2000 7.5 | 2005 8.1 | 2010 8.6 | 2015 9.2 | 2020 9.7 years.
The age bases differ (origin 15+, migrants 25-54), so levels are NOT comparable; the comparison is
between the two SLOPES.
"""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import os
import duckdb
import numpy as np
import pandas as pd

DB = str(_data_paths.microdata_duckdb_path(require_exists=False))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "derived")

YRS = {1: 2.5, 2: 6.5, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 18}
INEGI = {2000: 7.5, 2005: 8.1, 2010: 8.6, 2015: 9.2, 2020: 9.7}

con = duckdb.connect(DB, read_only=True)
d = con.execute("""
SELECT YEAR, AGE, YRIMMIG, EDUC, PERWT FROM ipums_usa_borjas_panel
WHERE BPL = 200 AND AGE BETWEEN 25 AND 54 AND YRIMMIG > 0
""").fetchdf()
con.close()
d["ysm"] = d.YEAR - d.YRIMMIG
d["yrs"] = d.EDUC.map(YRS)

rows = []
for y in sorted(d.YEAR.unique()):
    g = d[(d.YEAR == y) & (d.ysm >= 0) & (d.ysm <= 5)].dropna(subset=["yrs"])
    rows.append({"survey_year": int(y), "arrival_window": f"{int(y)-5}-{int(y)}", "n": len(g),
                 "migrant_mean_years_at_entry": float(np.average(g.yrs, weights=g.PERWT))})
m = pd.DataFrame(rows)
m["inegi_15plus_mean_years"] = m.survey_year.map(
    lambda y: INEGI.get(y, INEGI.get(min(INEGI, key=lambda k: abs(k - y)))
                        if y >= 2000 else np.nan))
m["inegi_reference_year"] = m.survey_year.map(
    lambda y: (y if y in INEGI else min(INEGI, key=lambda k: abs(k - y))) if y >= 2000 else None)
m["migrant_minus_origin"] = m.migrant_mean_years_at_entry - m.inegi_15plus_mean_years
m.to_csv(f"{OUT}/origin_relative_mean_years.csv", index=False)
print(m.to_string(index=False))

base = m[m.survey_year == 2000].iloc[0]
last = m[m.survey_year == 2023].iloc[0]
print(f"\nMigrant entry-cohort mean years, 2000 survey -> 2023 survey: "
      f"{base.migrant_mean_years_at_entry:.2f} -> {last.migrant_mean_years_at_entry:.2f} "
      f"(+{last.migrant_mean_years_at_entry - base.migrant_mean_years_at_entry:.2f})")
print(f"INEGI origin 15+ mean years, 2000 -> 2020: 7.5 -> 9.7 (+2.20)")
print(f"Difference in slopes (migrant minus origin): "
      f"{(last.migrant_mean_years_at_entry - base.migrant_mean_years_at_entry) - 2.20:+.2f} years")

"""0-5-year check for the 1990-94 arrival cohort, which the census-based main table can observe
only at 6-10 years since arrival (2000 census).

Source: the repository's IPUMS-CPS ASEC extract (sources/immigration-fiscal/data/external/cps/
cps_2ndgen.csv.gz, extract 1, 2026-09-22). Mexico-born (BPL 20000) adults in the March 1994 and
1995 ASEC who arrived 1990 to early 1994/1995 (YRIMMIG codes 12 = 1990-91, 14 = 1992-94 in 1994,
15 = 1992-95 in 1995) at age 20+. Placed with the same 2000-census origin reference as position.py.
The two March samples share rotation groups, so SEs cluster on the CPS household id (CPSID).

  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/cps_check.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import position as P  # noqa: E402
from levels import FIVE  # noqa: E402

ROOT = HERE.parents[2]
CPS = ROOT / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz"
# IPUMS-CPS EDUC -> shared scale interval. 081 "some college but no degree" spans <1 and 1+ years.
EDUC = {2: (0, 0), 10: (1, 4), 11: (1, 1), 12: (2, 2), 13: (3, 3), 14: (4, 4), 20: (5, 6), 21: (5, 5),
        22: (6, 6), 30: (7, 8), 31: (7, 7), 32: (8, 8), 40: (9, 9), 50: (10, 10), 60: (11, 11), 70: (13, 13),
        71: (12, 12), 72: (12, 13), 73: (13, 13), 80: (14, 15), 81: (13, 14), 90: (14, 15), 91: (15, 15),
        92: (15, 15), 100: (14, 15), 110: (16, 16), 111: (16, 16), 120: (16, 16), 121: (16, 16),
        122: (16, 16), 123: (16, 16), 124: (16, 16), 125: (16, 16)}
ARRIVAL_MID = {(1994, 12): 1991.0, (1994, 14): 1993.1, (1995, 12): 1991.0, (1995, 15): 1993.6}


def main() -> None:
    d = pd.read_csv(CPS, usecols=["YEAR", "SERIAL", "CPSID", "ASECWT", "AGE", "SEX", "BPL", "YRIMMIG", "CITIZEN",
                                  "EDUC"])
    d = d[(d.BPL == 20000) & d.YEAR.isin([1994, 1995]) & d.EDUC.isin(list(EDUC))].copy()
    d["arr_mid"] = [ARRIVAL_MID.get((y, c), np.nan) for y, c in zip(d.YEAR, d.YRIMMIG)]
    d = d[d.arr_mid.notna()].copy()
    d["BIRTHYR"] = d.YEAR - d.AGE - 1          # March survey: most birthdays still ahead
    d["arr_age"] = d.arr_mid - (d.BIRTHYR + 0.5)
    d = d[d.arr_age >= 20].copy()
    d["lo"] = d.EDUC.map(lambda c: EDUC[c][0])
    d["hi"] = d.EDUC.map(lambda c: EDUC[c][1])
    d["sex"] = d.SEX.map({1: "H", 2: "M"})
    d["PERWT"] = d.ASECWT
    d["SERIAL"] = np.where(d.CPSID > 0, d.CPSID.astype(str), d.YEAR.astype(str) + "_" + d.SERIAL.astype(str))
    d["YEAR"] = 0   # cluster key is CPSID alone (the same household can appear in both Marches)
    migrants = P.load_migrants()
    emp = P.empirical_splits(migrants)
    origin = P.Origin(P.OUT / "origin_levels.csv")
    rows = []
    for sx in ("P", "H", "M"):
        g = d if sx == "P" else d[d.sex == sx]
        r = P.summarize(g, origin, emp, 1990, "nearest")
        rows.append({"check": "CPS ASEC 1994+1995, Mexico-born arrived 1990-early 1995 at age 20+, ref 2000 census",
                     "sex": sx, **{k: r[k] for k in ("n", "wN", "ridit", "ridit_se", "q1", "q5",
                                                     "mig_c1_none_primary_incomplete", "mex_c1_none_primary_incomplete",
                                                     "mig_c5_tertiary", "mex_c5_tertiary",
                                                     "diff_c1_none_primary_incomplete", "diff_c5_tertiary", "position")}})
    main_tab = pd.read_csv(P.OUT / "position_main.csv")
    census = main_tab[main_tab.cohort == "1990-1994"].set_index("sex")
    out = pd.DataFrame(rows)
    out["census2000_ridit_6to10ysm"] = out.sex.map(census.ridit)
    out.to_csv(P.OUT / "cps_check_1990_94.csv", index=False, float_format="%.5f")
    print(out.drop(columns="check").to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()

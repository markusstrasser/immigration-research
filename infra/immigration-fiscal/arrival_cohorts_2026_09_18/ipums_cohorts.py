"""Mexico-born arrival cohorts on the local IPUMS census/ACS panel (1980/1990/2000/2010/2023).

Panel: $DERIVED_ROOT/immigration_microdata.duckdb, table ipums_usa_borjas_panel (read-only).
Available person vars: YEAR STATEFIP AGE RACE RACED BPL BPLD CITIZEN YRIMMIG EDUC EDUCD
EMPSTAT EMPSTATD WKSWORK1 INCTOT PERWT.  NOTE: no SEX, no HISPAN, no SPEAKENG, no INCWAGE,
no UHRSWORK in this extract -- those come from the ACS PUMS lane (acs_cohorts.py).

Outputs derived/ipums_*.csv
"""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import os
import duckdb
import pandas as pd
import numpy as np

DB = str(_data_paths.microdata_duckdb_path(require_exists=False))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "derived")
os.makedirs(OUT, exist_ok=True)

COHORT_SQL = """
CASE
  WHEN YRIMMIG < 1980 THEN 'pre1980'
  WHEN YRIMMIG < 1990 THEN '1980-89'
  WHEN YRIMMIG < 2000 THEN '1990-99'
  WHEN YRIMMIG < 2008 THEN '2000-07'
  WHEN YRIMMIG < 2015 THEN '2008-14'
  WHEN YRIMMIG < 2020 THEN '2015-19'
  ELSE '2020-24'
END
"""

# IPUMS harmonised EDUC -> 4 categories. EDUC is used instead of EDUCD because the 1980 census
# codes grade 12 as EDUCD 60 (no 62/63 diploma split), which would misclassify 1980 HS completers.
# EDUC<=5 below grade 12; EDUC=6 grade 12 (incl. 12th-no-diploma); 7-9 some college; >=10 BA+.
EDU_SQL = """
CASE
  WHEN EDUC <= 5 THEN 'lths'
  WHEN EDUC = 6 THEN 'hs'
  WHEN EDUC <= 9 THEN 'somecoll'
  ELSE 'ba_plus'
END
"""

BASE = f"""
SELECT YEAR, AGE, RACE, BPL, CITIZEN, YRIMMIG, EDUC, EDUCD, EMPSTAT,
       WKSWORK1, INCTOT, PERWT,
       {EDU_SQL} AS edu4,
       CASE WHEN BPL = 200 THEN 'mex' WHEN BPL < 150 AND RACE = 1 THEN 'usb_white' ELSE 'other' END AS grp,
       CASE WHEN BPL = 200 THEN {COHORT_SQL} ELSE NULL END AS cohort,
       CASE WHEN BPL = 200 AND YRIMMIG > 0 THEN YEAR - YRIMMIG ELSE NULL END AS ysm
FROM ipums_usa_borjas_panel
WHERE AGE BETWEEN 25 AND 54
  AND (BPL = 200 OR (BPL < 150 AND RACE = 1))
"""


def wmean(df, col, w="PERWT"):
    d = df[[col, w]].dropna()
    if d[w].sum() == 0:
        return np.nan
    return float(np.average(d[col], weights=d[w]))


def main():
    con = duckdb.connect(DB, read_only=True)
    df = con.execute(BASE).fetchdf()
    con.close()
    print("rows", len(df))

    # INCTOT missing codes
    df["inctot"] = df["INCTOT"].where(~df["INCTOT"].isin([9999999, 9999998, -9999999]))
    df["fullyear"] = (df["WKSWORK1"] >= 48)
    df["employed"] = (df["EMPSTAT"] == 1).astype(float)
    df["inlf"] = df["EMPSTAT"].isin([1, 2])

    mex = df[(df.grp == "mex") & df.cohort.notna() & (df.YRIMMIG > 0)].copy()
    nat = df[df.grp == "usb_white"].copy()

    # ---- (1) education distribution by cohort x year
    rows = []
    for (y, c), g in mex.groupby(["YEAR", "cohort"]):
        w = g.PERWT.sum()
        if w == 0:
            continue
        r = {"year": y, "cohort": c, "n": len(g), "wgt": w,
             "mean_ysm": wmean(g, "ysm"), "mean_age": wmean(g, "AGE")}
        for e in ["lths", "hs", "somecoll", "ba_plus"]:
            r[f"sh_{e}"] = g.loc[g.edu4 == e, "PERWT"].sum() / w
        r["emp_rate"] = float(np.average(g.employed, weights=g.PERWT))
        rows.append(r)
    edu = pd.DataFrame(rows).sort_values(["cohort", "year"])
    edu.to_csv(f"{OUT}/ipums_edu_by_cohort_year.csv", index=False)
    print(edu.to_string(index=False))

    # native benchmark education by year (for reference)
    nrows = []
    for y, g in nat.groupby("YEAR"):
        w = g.PERWT.sum()
        r = {"year": y, "n": len(g), "wgt": w}
        for e in ["lths", "hs", "somecoll", "ba_plus"]:
            r[f"sh_{e}"] = g.loc[g.edu4 == e, "PERWT"].sum() / w
        r["emp_rate"] = float(np.average(g.employed, weights=g.PERWT))
        nrows.append(r)
    pd.DataFrame(nrows).to_csv(f"{OUT}/ipums_native_white_benchmark.csv", index=False)

    # ---- (2) log-income residual vs US-born white, same year x age-group x education
    work = df[(df.fullyear) & (df.inctot > 0)].copy()
    work["lninc"] = np.log(work["inctot"])
    work["agegrp"] = pd.cut(work.AGE, [24, 29, 34, 39, 44, 49, 54], labels=["25-29", "30-34", "35-39", "40-44", "45-49", "50-54"])

    # native cell means
    cell = (work[work.grp == "usb_white"]
            .groupby(["YEAR", "agegrp", "edu4"], observed=True)
            .apply(lambda g: pd.Series({"nat_lninc": np.average(g.lninc, weights=g.PERWT),
                                        "nat_n": len(g)}), include_groups=False)
            .reset_index())
    cell.to_csv(f"{OUT}/ipums_native_cell_means.csv", index=False)

    mw = work[(work.grp == "mex") & work.cohort.notna() & (work.YRIMMIG > 0)].merge(
        cell, on=["YEAR", "agegrp", "edu4"], how="left")
    mw["resid"] = mw.lninc - mw.nat_lninc
    mw["ysm_band"] = pd.cut(mw.ysm, [-1, 5, 10, 20, 100], labels=["0-5", "6-10", "11-20", "21+"])

    rr = []
    for (y, c), g in mw.groupby(["YEAR", "cohort"], observed=True):
        g = g.dropna(subset=["resid"])
        if len(g) < 30:
            continue
        m = np.average(g.resid, weights=g.PERWT)
        # weighted se, design-naive
        v = np.average((g.resid - m) ** 2, weights=g.PERWT)
        neff = (g.PERWT.sum() ** 2) / (g.PERWT ** 2).sum()
        se = np.sqrt(v / neff)
        rr.append({"year": y, "cohort": c, "n": len(g), "mean_ysm": wmean(g, "ysm"),
                   "resid_lninc": m, "se": se, "lo95": m - 1.96 * se, "hi95": m + 1.96 * se,
                   "emp_rate_cohort": float(np.average(
                       mex[(mex.YEAR == y) & (mex.cohort == c)].employed,
                       weights=mex[(mex.YEAR == y) & (mex.cohort == c)].PERWT))})
    res = pd.DataFrame(rr).sort_values(["cohort", "year"])
    res.to_csv(f"{OUT}/ipums_wage_residual_by_cohort_year.csv", index=False)
    print("\n", res.to_string(index=False))

    # residual by ysm band (pooled across years) -- the Borjas cohort-quality object
    rb = []
    for (c, b), g in mw.groupby(["cohort", "ysm_band"], observed=True):
        g = g.dropna(subset=["resid"])
        if len(g) < 30:
            continue
        m = np.average(g.resid, weights=g.PERWT)
        v = np.average((g.resid - m) ** 2, weights=g.PERWT)
        neff = (g.PERWT.sum() ** 2) / (g.PERWT ** 2).sum()
        se = np.sqrt(v / neff)
        rb.append({"cohort": c, "ysm_band": b, "n": len(g), "years": sorted(g.YEAR.unique().tolist()),
                   "resid_lninc": m, "se": se, "lo95": m - 1.96 * se, "hi95": m + 1.96 * se})
    pd.DataFrame(rb).to_csv(f"{OUT}/ipums_wage_residual_by_ysm_band.csv", index=False)
    print("\n", pd.DataFrame(rb).to_string(index=False))


if __name__ == "__main__":
    main()

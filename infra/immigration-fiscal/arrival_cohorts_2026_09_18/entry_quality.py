"""Entry-quality series: Mexico-born observed at a FIXED duration since arrival in each survey.

For each survey year Y in the IPUMS panel (1980, 1990, 2000, 2010, 2023), take Mexico-born aged
25-54 with years since migration 0-3 (and, separately, 0-5). Because duration is held fixed, the
cross-survey comparison is a comparison of arrival cohorts at the same point in their US careers:
the Borjas 1985/1995 cohort-quality object, before most return migration has had time to occur.

Reported per survey year:
  * education distribution (harmonised EDUC, see ipums_cohorts.py for the coding note)
  * employment rate
  * mean log total income of full-year workers (WKSWORK1>=48), as a residual against US-born
    white men and women of the same age group in the same survey, both WITHOUT an education
    control (the unconditional entry gap, comparable to the 70-to-30 log point series in ladder
    entry 92) and WITH one (the within-education gap)

Outputs derived/entry_*.csv
"""
import os
import duckdb
import numpy as np
import pandas as pd

DB = "/Users/alien/research-data/immigration-fiscal/derived/immigration_microdata.duckdb"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")
os.makedirs(OUT, exist_ok=True)

SQL = """
SELECT YEAR, AGE, RACE, BPL, YRIMMIG, EMPSTAT, WKSWORK1, INCTOT, PERWT,
  CASE WHEN EDUC <= 5 THEN 'lths' WHEN EDUC = 6 THEN 'hs'
       WHEN EDUC <= 9 THEN 'somecoll' ELSE 'ba_plus' END AS edu4,
  CASE WHEN BPL = 200 THEN 'mex' ELSE 'usb_white' END AS grp
FROM ipums_usa_borjas_panel
WHERE AGE BETWEEN 25 AND 54 AND (BPL = 200 OR (BPL < 150 AND RACE = 1))
"""


def wagg(g, col):
    m = float(np.average(g[col], weights=g.PERWT))
    v = float(np.average((g[col] - m) ** 2, weights=g.PERWT))
    neff = (g.PERWT.sum() ** 2) / (g.PERWT ** 2).sum()
    return m, float(np.sqrt(v / neff))


def main():
    con = duckdb.connect(DB, read_only=True)
    df = con.execute(SQL).fetchdf()
    con.close()
    df["ysm"] = np.where(df.grp == "mex", df.YEAR - df.YRIMMIG, np.nan)
    df["employed"] = (df.EMPSTAT == 1).astype(float)
    df["inc"] = df.INCTOT.where(~df.INCTOT.isin([9999999, 9999998, -9999999]))
    df["agegrp"] = pd.cut(df.AGE, [24, 29, 34, 39, 44, 49, 54],
                          labels=["25-29", "30-34", "35-39", "40-44", "45-49", "50-54"])
    # WKSWORK1 (continuous weeks worked) is absent from the 2010 ACS in this extract -- IPUMS
    # supplies it only for the censuses and for ACS 2019+. So run two worker definitions:
    #   ftfy  = WKSWORK1 >= 48 (full-year), available 1980/1990/2000/2023
    #   emp   = EMPSTAT == 1 with positive income, available in every survey year
    # The second is the one that lets 2010 enter the series.
    defs = {"ftfy": df[(df.WKSWORK1 >= 48) & (df.inc > 0)].copy(),
            "emp": df[(df.EMPSTAT == 1) & (df.inc > 0)].copy()}
    work = defs["ftfy"]
    work["lninc"] = np.log(work.inc)
    defs["emp"]["lninc"] = np.log(defs["emp"].inc)

    rows = []
    for wdef, wk in defs.items():
        nat = wk[wk.grp == "usb_white"]
        cell_u = (nat.groupby(["YEAR", "agegrp"], observed=True)
                  .apply(lambda g: pd.Series({"nat_u": np.average(g.lninc, weights=g.PERWT)}),
                         include_groups=False).reset_index())
        cell_c = (nat.groupby(["YEAR", "agegrp", "edu4"], observed=True)
                  .apply(lambda g: pd.Series({"nat_c": np.average(g.lninc, weights=g.PERWT)}),
                         include_groups=False).reset_index())
        mw = (wk[wk.grp == "mex"].merge(cell_u, on=["YEAR", "agegrp"], how="left")
              .merge(cell_c, on=["YEAR", "agegrp", "edu4"], how="left"))
        mw["res_u"] = mw.lninc - mw.nat_u
        mw["res_c"] = mw.lninc - mw.nat_c

        for maxysm in (3, 5):
            for y in sorted(df.YEAR.unique()):
                g = df[(df.grp == "mex") & (df.YEAR == y) & (df.ysm >= 0) & (df.ysm <= maxysm)
                       & (df.YRIMMIG > 0)]
                if len(g) < 100:
                    continue
                gw = mw[(mw.YEAR == y) & (mw.ysm >= 0) & (mw.ysm <= maxysm) & (mw.YRIMMIG > 0)]
                r = {"worker_def": wdef, "max_ysm": maxysm, "survey_year": y,
                     "arrival_window": f"{int(y - maxysm)}-{int(y)}",
                     "n": len(g), "wgt_pop": float(g.PERWT.sum()),
                     "mean_age": float(np.average(g.AGE, weights=g.PERWT)),
                     "mean_ysm": float(np.average(g.ysm, weights=g.PERWT)),
                     "emp_rate": float(np.average(g.employed, weights=g.PERWT))}
                for e in ["lths", "hs", "somecoll", "ba_plus"]:
                    r[f"sh_{e}"] = float(g.loc[g.edu4 == e, "PERWT"].sum() / g.PERWT.sum())
                gwu = gw.dropna(subset=["res_u"])
                gwc = gw.dropna(subset=["res_c"])
                if len(gwu) >= 50:
                    m, se = wagg(gwu, "res_u")
                    r.update({"n_workers": len(gwu), "resid_uncond": m, "se_uncond": se,
                              "lo95_uncond": m - 1.96 * se, "hi95_uncond": m + 1.96 * se})
                if len(gwc) >= 50:
                    m, se = wagg(gwc, "res_c")
                    r.update({"resid_cond_edu": m, "se_cond": se,
                              "lo95_cond": m - 1.96 * se, "hi95_cond": m + 1.96 * se})
                rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(f"{OUT}/entry_quality_fixed_duration_ipums.csv", index=False)
    cols = ["worker_def", "max_ysm", "survey_year", "arrival_window", "n", "mean_age", "mean_ysm", "sh_lths",
            "sh_hs", "sh_somecoll", "sh_ba_plus", "emp_rate", "resid_uncond", "lo95_uncond",
            "hi95_uncond", "resid_cond_edu", "lo95_cond", "hi95_cond"]
    print(out[cols].to_string(index=False))


if __name__ == "__main__":
    main()

"""Two auxiliary calculations for the arrival-cohort memo.

(A) Age-standardised education shares at each cohort's FIRST observation at ages 25-54 in the
    IPUMS panel, so the cross-cohort comparison is not driven by age composition. Standard
    population = the 2000 census Mexico-born 25-54 age distribution.

(B) A return-migration accounting bound. Ladder entry 92 (Akee, Chin & Crown, NBER w35582)
    reports that a fifth to a third of Mexican arrivals leave within ten years and that leavers
    are negatively selected. For each cohort observed twice ten years apart we ask: if the entire
    within-cohort drift in the <HS share were return migration, what <HS share would the leavers
    need to have had? And symmetrically, how much does stayer-only measurement inflate a cohort's
    log-income residual for a given leaver share L and leaver-stayer residual gap delta.

Outputs derived/bound_*.csv
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
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")
os.makedirs(OUT, exist_ok=True)

SQL = """
SELECT YEAR, AGE, YRIMMIG, EDUCD, PERWT,
  CASE WHEN YRIMMIG < 1980 THEN 'pre1980'
       WHEN YRIMMIG < 1990 THEN '1980-89'
       WHEN YRIMMIG < 2000 THEN '1990-99'
       WHEN YRIMMIG < 2008 THEN '2000-07'
       WHEN YRIMMIG < 2015 THEN '2008-14'
       WHEN YRIMMIG < 2020 THEN '2015-19'
       ELSE '2020-24' END AS cohort,
  CASE WHEN EDUC <= 5 THEN 'lths' WHEN EDUC = 6 THEN 'hs'
       WHEN EDUC <= 9 THEN 'somecoll' ELSE 'ba_plus' END AS edu4
FROM ipums_usa_borjas_panel
WHERE BPL = 200 AND AGE BETWEEN 25 AND 54 AND YRIMMIG > 0
"""

# each cohort's first observation at 25-54 in this panel, and the next observation ten years on
FIRST = {"pre1980": (1980, 1990), "1980-89": (1990, 2000), "1990-99": (2000, 2010),
         "2000-07": (2010, None), "2008-14": (2010, None), "2015-19": (2023, None),
         "2020-24": (2023, None)}


def main():
    con = duckdb.connect(DB, read_only=True)
    df = con.execute(SQL).fetchdf()
    con.close()
    df["agegrp"] = pd.cut(df.AGE, [24, 29, 34, 39, 44, 49, 54],
                          labels=["25-29", "30-34", "35-39", "40-44", "45-49", "50-54"])

    std = df[df.YEAR == 2000].groupby("agegrp", observed=True).PERWT.sum()
    std = std / std.sum()

    rows = []
    for c, (y0, y1) in FIRST.items():
        for lab, y in [("first", y0), ("plus10", y1)]:
            if y is None:
                continue
            g = df[(df.cohort == c) & (df.YEAR == y)]
            if len(g) < 100:
                continue
            crude, adj = {}, {}
            for e in ["lths", "hs", "somecoll", "ba_plus"]:
                crude[e] = g.loc[g.edu4 == e, "PERWT"].sum() / g.PERWT.sum()
                by = g.groupby("agegrp", observed=True).apply(
                    lambda h: h.loc[h.edu4 == e, "PERWT"].sum() / h.PERWT.sum()
                    if h.PERWT.sum() > 0 else np.nan, include_groups=False)
                w = std.reindex(by.index)
                m = by.notna()
                adj[e] = float((by[m] * w[m]).sum() / w[m].sum())
            rows.append({"cohort": c, "obs": lab, "year": y, "n": len(g),
                         "mean_ysm": float(np.average(y - g.YRIMMIG, weights=g.PERWT)),
                         "mean_age": float(np.average(g.AGE, weights=g.PERWT)),
                         **{f"crude_{k}": v for k, v in crude.items()},
                         **{f"agestd_{k}": v for k, v in adj.items()}})
    a = pd.DataFrame(rows)
    a.to_csv(f"{OUT}/bound_agestd_education_first_obs.csv", index=False)
    print(a.to_string(index=False))

    # (B1) implied leaver <HS share if all within-cohort drift were return migration
    rows = []
    for c in a.cohort.unique():
        s = a[a.cohort == c]
        if set(s.obs) != {"first", "plus10"}:
            continue
        s0 = float(s[s.obs == "first"].crude_lths.iloc[0])
        s1 = float(s[s.obs == "plus10"].crude_lths.iloc[0])
        for L in [0.20, 0.25, 0.33]:
            sL = (s0 - (1 - L) * s1) / L
            rows.append({"cohort": c, "lths_first": s0, "lths_plus10": s1,
                         "drift_pp": 100 * (s1 - s0), "leaver_share_L": L,
                         "implied_leaver_lths_share": sL,
                         "feasible": bool(0.0 <= sL <= 1.0)})
    b1 = pd.DataFrame(rows)
    b1.to_csv(f"{OUT}/bound_implied_leaver_education.csv", index=False)
    print("\n", b1.to_string(index=False))

    # (B2) how much stayer-only measurement inflates a cohort's residual
    rows = []
    for L in [0.20, 0.25, 0.33]:
        for d in [0.05, 0.10, 0.20, 0.30]:
            rows.append({"leaver_share_L": L, "leaver_stayer_resid_gap_delta": d,
                         "stayer_minus_true_cohort_mean": L * d})
    b2 = pd.DataFrame(rows)
    b2.to_csv(f"{OUT}/bound_stayer_residual_inflation.csv", index=False)
    print("\n", b2.to_string(index=False))


if __name__ == "__main__":
    main()


def undercount_sensitivity():
    """How much can differential ACS undercount of recent unauthorised arrivals move the
    2018-2023 cohort's education distribution?

    Suppose the true 2018-2023 Mexican arrival cohort aged 25-54 is k times the surveyed count,
    and every missed person has less than a high-school education (the most adverse assumption).
    Then the true <HS share is (s + (k-1)) / k where s is the surveyed <HS share.
    Benchmarks are the surveyed <HS shares of earlier cohorts at the same 0-5 year duration,
    which are themselves undercounted, so this is a one-sided stress test, not a correction.
    """
    s_2023 = 0.332533   # entry_quality_fixed_duration_ipums.csv, max_ysm=5, survey_year=2023
    bench = {"1975-80 (1980 census)": 0.824507, "1985-90 (1990 census)": 0.663731,
             "1995-00 (2000 census)": 0.614503, "2005-10 (2010 ACS)": 0.517343}
    rows = []
    for k in [1.0, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0]:
        adj = (s_2023 + (k - 1)) / k
        r = {"undercount_factor_k": k, "implied_lths_share_2018_23": adj}
        for b, v in bench.items():
            r[f"still_below_{b}"] = bool(adj < v)
        rows.append(r)
    d = pd.DataFrame(rows)
    d.to_csv(f"{OUT}/bound_undercount_sensitivity.csv", index=False)
    print("\n", d.to_string(index=False))


if True:
    undercount_sensitivity()

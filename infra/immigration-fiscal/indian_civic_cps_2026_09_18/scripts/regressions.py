"""Raw vs adjusted birthplace coefficients for turnout, volunteering and giving.

Main specification is a weighted linear probability model (WLS with HC1 robust SEs),
reference category = US-born non-Hispanic white. A weighted logit is run alongside and
its average marginal effect reported as a functional-form check.

Controls: age, age^2, sex, education (7 collapsed levels), family income (5 brackets),
metropolitan status, survey-year fixed effects.
NOT controlled: years in the United States. PEINUSYR is absent from both the Census API
and the public-use files for the November and September CPS supplements (verified
2026-09-18: only the allocation flag PXINUSYR is carried), so years-since-entry cannot
enter these models. derived/asec_naturalization_by_entry.csv supplies the
years-since-entry picture from the ASEC instead.

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" --with statsmodels python3 \
       scripts/regressions.py
Outputs: derived/regression_turnout.csv, derived/regression_civic.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CACHE, adults, assign_groups, load, write_csv  # noqa: E402

GROUPS = ["1 India-born", "2 China-born", "3 Mexico-born", "4 Other foreign-born",
          "5 Indian 2nd gen"]
REF = "6 US-born NH white"


def educ_level(e: pd.Series) -> pd.Series:
    return pd.cut(e.astype(float), [0, 38, 39, 42, 43, 44, 99],
                  labels=["lt_hs", "hs", "some_col", "ba", "ma", "prof_phd"])


def inc_level(h: pd.Series) -> pd.Series:
    return pd.cut(h.astype(float), [0, 7, 11, 13, 15, 16],
                  labels=["lt25k", "25_50k", "50_75k", "75_150k", "150k_plus"])


def design(d: pd.DataFrame, adjusted: bool) -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame(index=d.index)
    for g in GROUPS:
        X[g] = d.grp.eq(g).astype(float)
    for y in sorted(d.year.unique())[1:]:
        X[f"year_{y}"] = d.year.eq(y).astype(float)
    if adjusted:
        age = d.PRTAGE.astype(float)
        X["age"] = age
        X["age2"] = age ** 2 / 100.0
        X["female"] = d.PESEX.eq(2).astype(float)
        X["metro"] = d.GTMETSTA.eq(1).astype(float)
        X["metro_unknown"] = d.GTMETSTA.eq(3).astype(float)
        for col, series, drop in (("ed", educ_level(d.PEEDUCA), "hs"),
                                  ("inc", inc_level(d.HEFAMINC), "50_75k")):
            dm = pd.get_dummies(series, prefix=col, dtype=float)
            dm = dm.loc[:, dm.sum() > 0]        # categories nobody in this subset occupies
            # Drop one category as the reference. If the intended one is empty in this subset
            # (the BA+ arm has no "hs"), the surviving dummies would sum to the intercept and
            # make the design singular, so fall back to the largest category present.
            ref = next((c for c in dm.columns if c.endswith(drop)), None)
            if ref is None and len(dm.columns):
                ref = dm.sum().idxmax()
            if ref is not None:
                dm = dm.drop(columns=[ref])
            X = pd.concat([X, dm], axis=1)
    # A restricted arm (BA+ only, a single year, a small subgroup) can empty out an
    # education or income category, leaving an all-zero dummy column that makes X'X
    # singular. Drop any column with no variation; the intercept absorbs it.
    X = X.loc[:, X.nunique() > 1]
    X = sm.add_constant(X, has_constant="add")
    return X.astype(float), d


def fit(d: pd.DataFrame, y: pd.Series, w: pd.Series, adjusted: bool, label: str,
        outcome: str) -> pd.DataFrame:
    X, _ = design(d, adjusted)
    keep = y.notna() & w.gt(0) & X.notna().all(axis=1)
    X, yy, ww = X[keep], y[keep].astype(float), w[keep].astype(float)
    # Fail loud rather than let statsmodels pseudo-invert a rank-deficient design: those
    # coefficients are not uniquely determined, and they moved by up to 4 points when a
    # collinear dummy block was present (2026-09-18).
    rank = np.linalg.matrix_rank(X.to_numpy(float))
    if rank < X.shape[1]:
        raise RuntimeError(f"rank-deficient design for {label}/{outcome}: "
                           f"rank {rank} < {X.shape[1]} columns ({list(X.columns)})")
    m = sm.WLS(yy, X, weights=ww).fit(cov_type="HC1")
    try:
        g = sm.GLM(yy, X, family=sm.families.Binomial(), var_weights=ww).fit()
        pr = g.predict(X)
        ame = {k: float(g.params[k] * np.average(pr * (1 - pr), weights=ww)) for k in GROUPS}
    except Exception as e:                                     # noqa: BLE001
        print(f"[warn] logit failed for {label}/{outcome}: {e}")
        ame = {k: float("nan") for k in GROUPS}
    rows = []
    for g_ in GROUPS:
        rows.append(dict(outcome=outcome, spec=label,
                         model="adjusted" if adjusted else "raw", group=g_,
                         coef_lpm=float(m.params[g_]), se_lpm=float(m.bse[g_]),
                         t=float(m.tvalues[g_]), ame_logit=ame[g_],
                         n=int(len(yy)), r2=float(m.rsquared)))
    return pd.DataFrame(rows)


def main() -> None:
    out = []

    # ---------- turnout, citizens 18+, pooled November supplements ----------
    frames = []
    for y in [2016, 2018, 2020, 2022, 2024]:
        p = CACHE / f"cps_voting_{y}.json"
        if not p.exists():
            continue
        d = adults(assign_groups(load(p)), "PWSSWGT")
        d["year"] = y
        frames.append(d)
    if frames:
        v = pd.concat(frames, ignore_index=True)
        v = v[v.PRCITSHP.isin([1, 2, 3, 4]) & v.grp.notna()]
        v = v[v.grp.isin(GROUPS + [REF])].copy()
        y_cen = v.PES1.eq(1).astype(float)                      # Census convention
        w = v.PWSSWGT
        for adj in (False, True):
            out.append(fit(v, y_cen, w, adj, "citizens_18plus", "turnout_census_convention"))
        vr = v[v.PES1.isin([1, 2])]
        for adj in (False, True):
            out.append(fit(vr, vr.PES1.eq(1).astype(float), vr.PWSSWGT, adj,
                           "citizens_respondents_only", "turnout_reported_only"))
        vb = v[v.PEEDUCA >= 43]
        for adj in (False, True):
            out.append(fit(vb, vb.PES1.eq(1).astype(float), vb.PWSSWGT, adj,
                           "citizens_BA_plus", "turnout_census_convention"))
        # No "naturalized only" regression: that subset contains no native-born observations,
        # so the reference category (US-born NH white) and the 2nd-generation dummy are both
        # empty and the design is singular. The arm is reported in derived/voting_arms.csv.
        va = v[(v.PRTAGE >= 25) & (v.PRTAGE <= 54)]
        for adj in (False, True):
            out.append(fit(va, va.PES1.eq(1).astype(float), va.PWSSWGT, adj,
                           "citizens_age_25_54", "turnout_census_convention"))
        t = pd.concat(out, ignore_index=True)
        t = t.sort_values(["outcome", "spec", "model", "group"], kind="stable").reset_index(drop=True)
        write_csv(t, "regression_turnout.csv")
        print("[done] regression_turnout.csv")

    # ---------- volunteering / giving / civic contact, adults 18+ ----------
    out2 = []
    frames = []
    for y in [2019, 2021, 2023]:
        p = CACHE / f"cps_volunteer_{y}.json"
        if not p.exists():
            continue
        d = adults(assign_groups(load(p)), "PWNRWGT")
        d["year"] = y
        d["self_resp"] = d.PUSLFPRX.isin([1, 3])
        frames.append(d)
    if frames:
        c = pd.concat(frames, ignore_index=True)
        c = c[c.grp.isin(GROUPS + [REF])].copy()
        for outcome, var in [("volunteered_org", "PES16"), ("donated_nonpolitical", "PES18"),
                             ("group_membership", "PES15"), ("contacted_official", "PES13")]:
            sub = c[c[var].isin([1, 2])]
            yv = sub[var].eq(1).astype(float)
            for adj in (False, True):
                out2.append(fit(sub, yv, sub.PWNRWGT, adj, "adults_18plus", outcome))
            s2 = sub[sub.self_resp]
            for adj in (False, True):
                out2.append(fit(s2, s2[var].eq(1).astype(float), s2.PWNRWGT, adj,
                                "self_respondent_only", outcome))
            s3 = sub[sub.PEEDUCA >= 43]
            for adj in (False, True):
                out2.append(fit(s3, s3[var].eq(1).astype(float), s3.PWNRWGT, adj,
                                "BA_plus_only", outcome))
        t2 = pd.concat(out2, ignore_index=True)
        t2 = t2.sort_values(["outcome", "spec", "model", "group"], kind="stable").reset_index(drop=True)
        write_csv(t2, "regression_civic.csv")
        print("[done] regression_civic.csv")


if __name__ == "__main__":
    main()

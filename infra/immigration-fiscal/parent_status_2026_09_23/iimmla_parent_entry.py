#!/usr/bin/env python3
"""Adult outcomes of US-born Mexican-origin children by how their parents entered the US (IIMMLA 2004).

Question (operator, 2026-09-23): are the children of illegal immigrants doing worse or better?

IIMMLA (ICPSR 22627; five-county Los Angeles, 2004, respondents aged 20-40) asked each respondent
whether their foreign-born mother (Q127A) and father (Q144A) entered "as a permanent resident; that
is, did she have her green card?" (1 yes, 2 no, 3 entered illegally [volunteered], 4 entered as a
US citizen), which temporary documents they entered with (Q128_A-D / Q145_A-D: student or tourist
visa, temporary work visa, border crossing card, refugee), and their status at the interview
(Q122/Q139 citizen, Q124/Q141 green card). Almost every parent of the US-born respondents had
legalized by 2004, so the contrast measured here is entry status, not lifelong status.

The file has no survey weight; every estimate is unweighted (quota sample), as in iimmla_2026_09_17.
Outcome definitions and skip repairs are copied from iimmla_2026_09_17/iimmla_tab.py.

Run from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/parent_status_2026_09_23/iimmla_parent_entry.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "iimmla_2026_09_17/raw/ICPSR_22627/DS0001/22627-0001-Data.tsv"
MEXICO = 43                      # QS12AM / QS12BF country code
# iimmla_2026_09_17/RESULT.md table 1, "Mexican 2nd": n and outcome percentages
PUBLISHED = {"n": 553, "no_hs": 19.0, "ba_plus": 16.8, "arrested": 17.4, "incarcerated": 11.2}
OUTCOMES = ["years_school", "no_hs", "ba_plus", "employed", "inc_mid", "inc_ge30k",
            "arrested", "incarcerated", "any_welfare"]


def yn(s, yes=1, na=(-9, -8, -7, 3, 4, 9, 10)):
    v = s.where(~s.isin(na))
    return (v == yes).astype(float).where(v.notna())


def outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Outcome columns, same definitions and skip repairs as iimmla_2026_09_17/iimmla_tab.py."""
    o = pd.DataFrame(index=df.index)
    o["years_school"] = df.educmax.astype(float)
    o["no_hs"] = (df.educred5 == 0).astype(float)
    o["ba_plus"] = (df.educred5 >= 4).astype(float)
    o["arrested"] = df.evarre.astype(float)
    o["incarcerated"] = df.evpriso.astype(float)
    o["employed"] = df.q2_1.where(df.q2_1 != -9).astype(float)
    medicaid, tanf = yn(df.q177_c), yn(df.q177_e)
    asked = np.where(medicaid.notna() | tanf.notna(),
                     ((medicaid == 1) | (tanf == 1)).astype(float), np.nan)
    hi_inc_skip = df.q176a.isin([5, 6, 7]) & (df.q177_c == -9)
    o["any_welfare"] = np.where(hi_inc_skip, 0.0, asked)
    inc = df.q171a.where(df.q171a.between(1, 8)).copy()
    hh = df.q176a.where(df.q176a.between(1, 7))
    sole = df.q175a == 1
    fill = inc.isna() & sole & (df.q175b == 1)
    inc.loc[fill] = hh[fill] + 1
    inc.loc[inc.isna() & sole & (df.q175b == 2)] = 1
    inc.loc[inc.isna() & (df.q175a == 0)] = 1
    mid = {1: 0, 2: 6000, 3: 16000, 4: 25000, 5: 40000, 6: 60000, 7: 85000, 8: 125000}
    o["inc_mid"] = inc.map(mid)
    o["inc_ge30k"] = (inc >= 5).astype(float).where(inc.notna())
    return o


def entry_status(df: pd.DataFrame, entry: str, docs: list[str]) -> pd.Series:
    """legal_entry / visa_or_card / no_papers / unknown for one parent."""
    code = df[entry]
    doc = df[docs]
    any_doc = doc.eq(1).any(axis=1)
    all_no = doc.eq(2).all(axis=1)
    s = pd.Series("unknown", index=df.index)
    s[code.isin([1, 4])] = "legal_entry"
    s[code.eq(2) & any_doc] = "visa_or_card"
    s[code.eq(3) | (code.eq(2) & all_no)] = "no_papers"
    s[code.eq(2) & ~any_doc & ~all_no] = "no_green_card_docs_unknown"
    return s


def ols_hc1(y: np.ndarray, X: np.ndarray):
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    n, k = X.shape
    meat = (X * e[:, None] ** 2).T @ X
    V = XtX_inv @ meat @ XtX_inv * n / (n - k)
    return beta, np.sqrt(np.diag(V))


def controls(df: pd.DataFrame) -> pd.DataFrame:
    c = pd.DataFrame(index=df.index)
    age = df.age.astype(float)
    c["age"], c["age2"] = age, age ** 2
    c["male"] = (df.gender == 1).astype(float)          # codebook: 0 female, 1 male
    for par, col in (("mom", "q133a"), ("dad", "q150a")):
        ed = df[col].where(df[col].between(1, 6))
        for level in (2, 3, 4, 5, 6):                    # 1 = did not complete high school
            c[f"{par}_ed{level}"] = ed.eq(level).astype(float)
        c[f"{par}_ed_missing"] = ed.isna().astype(float)
    return c


def gap(o, c, treat, base, outcome):
    keep = (treat | base) & o[outcome].notna()
    X = np.column_stack([np.ones(keep.sum()), treat[keep].astype(float), c[keep].to_numpy()])
    X = X[:, np.r_[0, 1, 2 + np.flatnonzero(X[:, 2:].std(0) > 0)]]   # drop constant controls
    y = o.loc[keep, outcome].to_numpy(float)
    beta, se = ols_hc1(y, X)
    raw = o.loc[keep & treat, outcome].mean() - o.loc[keep & base, outcome].mean()
    return raw, beta[1], se[1], int((keep & treat).sum()), int((keep & base).sum())


def main():
    df = pd.read_csv(RAW, sep="\t", low_memory=False)
    df.columns = [c.lower() for c in df.columns]
    o, c = outcomes(df), controls(df)
    m2 = (df.ethnos10 == 1) & (df.generat3 == 2)

    # Gate: reproduce the IIMMLA lane's Mexican second-generation row.
    got = {"n": int(m2.sum()), "no_hs": 100 * o.no_hs[m2].mean(), "ba_plus": 100 * o.ba_plus[m2].mean(),
           "arrested": 100 * o.arrested[m2].mean(), "incarcerated": 100 * o.incarcerated[m2].mean()}
    for k, v in PUBLISHED.items():
        if abs(got[k] - v) > 0.05 + 1e-9:
            raise ValueError(f"gate: Mexican 2nd gen {k} {got[k]:.2f} vs published {v}")

    mom = entry_status(df, "q127a", ["q128_a", "q128_b", "q128_c", "q128_d"])
    dad = entry_status(df, "q144a", ["q145_a", "q145_b", "q145_c", "q145_d"])
    mom_mx, dad_mx = df.qs12am.eq(MEXICO), df.qs12bf.eq(MEXICO)
    mom_never = df.q122.eq(2) & df.q124.eq(2)
    dad_never = df.q139.eq(2) & df.q141.eq(2)

    rows, gaps = [], []
    for parent, st, mx, never in (("mother", mom, mom_mx, mom_never), ("father", dad, dad_mx, dad_never)):
        base = m2 & mx & st.eq("legal_entry")
        groups = {
            "legal_entry": base,
            "no_green_card_any": m2 & mx & st.isin(["visa_or_card", "no_papers", "no_green_card_docs_unknown"]),
            "no_papers": m2 & mx & st.eq("no_papers"),
            "visa_or_card": m2 & mx & st.eq("visa_or_card"),
            "never_legalized_by_2004": m2 & mx & never,
        }
        for g, mask in groups.items():
            r = {"parent": parent, "group": g, "n": int(mask.sum())}
            for out in OUTCOMES:
                r[out] = round(float(o.loc[mask, out].mean()), 4)
            r["parent_no_hs_share"] = round(float(df.loc[mask, "q133a" if parent == "mother" else "q150a"]
                                                  .where(lambda s: s.between(1, 6)).eq(1).mean()), 4)
            rows.append(r)
        for g in ("no_green_card_any", "no_papers"):
            for out in OUTCOMES:
                raw, adj, se, nt, nb = gap(o, c, groups[g], base, out)
                gaps.append({"parent": parent, "contrast": f"{g} minus legal_entry", "outcome": out,
                             "raw_diff": round(raw, 4), "adjusted_diff": round(adj, 4),
                             "adjusted_se_hc1": round(se, 4), "n_treat": nt, "n_base": nb})

    # Family level: any Mexico-born parent entered without a green card vs all entered with one.
    fb_par = [(mom, mom_mx), (dad, dad_mx)]
    any_ngc = m2 & ((mom_mx & mom.isin(["visa_or_card", "no_papers", "no_green_card_docs_unknown"]))
                    | (dad_mx & dad.isin(["visa_or_card", "no_papers", "no_green_card_docs_unknown"])))
    all_legal = m2 & (mom_mx | dad_mx)
    for st, mx in fb_par:
        all_legal &= ~mx | st.eq("legal_entry")
    for out in OUTCOMES:
        raw, adj, se, nt, nb = gap(o, c, any_ngc, all_legal, out)
        gaps.append({"parent": "family", "contrast": "any parent without green card minus all with",
                     "outcome": out, "raw_diff": round(raw, 4), "adjusted_diff": round(adj, 4),
                     "adjusted_se_hc1": round(se, 4), "n_treat": nt, "n_base": nb})

    out_dir = HERE / "derived"
    out_dir.mkdir(exist_ok=True)
    means, diffs = pd.DataFrame(rows), pd.DataFrame(gaps)
    means.to_csv(out_dir / "iimmla_second_gen_by_parent_entry.csv", index=False)
    diffs.to_csv(out_dir / "iimmla_entry_status_gaps.csv", index=False)
    pd.set_option("display.width", 220)
    print(f"gate ✓ Mexican 2nd gen reproduces the lane: {got}")
    print(means.to_string(index=False))
    print()
    print(diffs.to_string(index=False))


if __name__ == "__main__":
    main()

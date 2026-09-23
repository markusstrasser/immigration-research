#!/usr/bin/env python3
"""Legal status of Mexico-born parents of US-born minor children, by education (CPS ASEC 2025).

Question (operator, 2026-09-23): are almost none of the low-education Mexico-born parents legal?

Status is the Borjas (2017) residual imputation from `status_impute_2026_09_16` (rules quoted in
that lane's `impute_status.py` and RESULT.md). Two rule sets are reported:
  * `borjas_paper_rules` -- the paper's rules as that lane runs them;
  * `no_medicaid_rule` -- rule (c) without Medicaid. California's Medi-Cal covered income-eligible
    unauthorized adults in 2024, so the paper's rule calls those adults legal.
Status is the parent's imputed status in March 2025, not at the child's birth.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/parent_status_2026_09_23/parent_status.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

CPS = ROOT / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
MEXICO = 303
CALIFORNIA = 6
REPS = [f"pwwgt{i}" for i in range(1, 161)]
IMPUTE_FIELDS = ["PH_SEQ", "A_LINENO", "A_SPOUSE", "PRCITSHP", "PENATVTY", "PEINUSYR", "SS_VAL",
                 "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER", "PRPERTYP",
                 "A_CLSWKR", "PEIOOCC"]
PERSON = IMPUTE_FIELDS + ["PPPOS", "A_AGE", "A_HGA", "PEPAR1", "PEPAR2", "MARSUPWT"]
EDU = [("below_high_school", range(31, 39)), ("high_school", [39]),
       ("some_college", [40, 41, 42]), ("bachelor_plus", range(43, 47))]
# status_impute_2026_09_16/status_counts.csv, borjas_paper_rules, Mexico-born 25-64, millions
PUBLISHED_MEX_25_64 = {"borjas_paper_rules": 3.9170610819750302, "no_medicaid_rule": 4.778136460024849}


def load(extra=()):
    with zipfile.ZipFile(CPS) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON + [c for c in extra if c not in PERSON])
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT", "GESTFIPS"])
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"] + REPS)
    d = d.merge(r.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], how="left",
                validate="one_to_one")
    if d[REPS + ["pwwgt0"]].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    if (d.MARSUPWT / 100 - d.pwwgt0).abs().max() >= .01:
        raise ValueError("Full-weight merge validation failed")
    state = d.PH_SEQ.map(hh.set_index("H_SEQ").GESTFIPS)
    if state.isna().any():
        raise ValueError("Person record without a household state")
    d = pd.concat([d, state.astype(int).rename("state")], axis=1)
    return d, hh


def edu_label(hga: np.ndarray) -> np.ndarray:
    out = np.full(len(hga), "not_adult_coded", dtype=object)
    for name, codes in EDU:
        out[np.isin(hga, list(codes))] = name
    return out


def share(W: np.ndarray, den: np.ndarray, num: np.ndarray):
    """Weighted share num/den with its SDR standard error (4/160 * sum of squared deviations)."""
    tot = W[den].sum(0)
    part = W[den & num].sum(0)
    theta = np.divide(part, tot, out=np.full_like(tot, np.nan), where=tot > 0)
    se = float(np.sqrt(4 / 160 * ((theta[1:] - theta[0]) ** 2).sum()))
    return float(theta[0]), se, float(tot[0] / 1e6), int(den.sum())


def main():
    d, hh = load()
    W = d[["pwwgt0"] + REPS].to_numpy(float)
    edu = edu_label(d.A_HGA.to_numpy())

    # Parent pointers: PEPAR1/PEPAR2 are the parent's A_LINENO inside the household (-1 = none).
    row_of = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_arrays([d.PH_SEQ, d.A_LINENO]))
    if row_of.index.duplicated().any():
        raise ValueError("PH_SEQ + A_LINENO is not unique")
    prow = {}
    for col in ("PEPAR1", "PEPAR2"):
        want = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d[col].to_numpy()])
        prow[col] = row_of.reindex(want).to_numpy()
        present = d[col].gt(0).to_numpy()
        if np.isnan(prow[col][present]).any():
            raise ValueError(f"{col} points at a line number missing from its household")

    kid = ((d.A_AGE < 18) & (d.PRCITSHP == 1)).to_numpy()          # US-born minors
    is_parent = np.zeros(len(d), bool)
    for col in prow:
        rows = prow[col][kid]
        is_parent[rows[~np.isnan(rows)].astype(int)] = True

    parent_rows, kid_rows = [], []
    for name, use_med in (("borjas_paper_rules", True), ("no_medicaid_rule", False)):
        s = impute(d, hh, use_medicaid_rule=use_med)
        fb, legal, unauth = s["foreign_born"], s["legal"], s["unauthorized"]
        mex = fb & d.PENATVTY.eq(MEXICO).to_numpy()

        # Positive control: reproduce the published Mexico-born 25-64 count for this rule set.
        age = d.A_AGE.to_numpy()
        got = W[mex & unauth & (age >= 25) & (age <= 64), 0].sum() / 1e6
        if abs(got - PUBLISHED_MEX_25_64[name]) > 0.005:
            raise ValueError(f"{name}: Mexico-born 25-64 unauthorized {got:.4f}M "
                             f"vs published {PUBLISHED_MEX_25_64[name]:.4f}M")

        # Parents: Mexico-born parents of at least one US-born minor in the household.
        groups = [(g, edu == g) for g, _ in EDU] + [("all", np.ones(len(d), bool))]
        for region, reg in (("US", np.ones(len(d), bool)),
                            ("California", d.state.eq(CALIFORNIA).to_numpy()),
                            ("rest_of_US", ~d.state.eq(CALIFORNIA).to_numpy())):
            for g, gm in groups:
                sh, se, pop, n = share(W, mex & is_parent & gm & reg, unauth)
                parent_rows.append({"rules": name, "region": region, "education": g,
                                    "parents_millions": round(pop, 3), "n": n,
                                    "share_unauthorized": round(sh, 4), "se": round(se, 4)})
            # Comparison: all Mexico-born adults 25-64 (parents or not), same rules.
            sh, se, pop, n = share(W, mex & reg & (age >= 25) & (age <= 64), unauth)
            parent_rows.append({"rules": name, "region": region, "education": "all_adults_25_64",
                                "parents_millions": round(pop, 3), "n": n,
                                "share_unauthorized": round(sh, 4), "se": round(se, 4)})

        # Children: US-born minors with at least one Mexico-born parent present.
        p_mex = np.zeros(len(d), bool)
        n_par = np.zeros(len(d), int)
        n_legal_par = np.zeros(len(d), int)
        top_hga = np.full(len(d), -1)
        hga = d.A_HGA.to_numpy()
        for col in prow:
            r = prow[col]
            ok = kid & ~np.isnan(r)
            ri = r[ok].astype(int)
            p_mex[ok] |= mex[ri]
            n_par[ok] += 1
            n_legal_par[ok] += legal[ri].astype(int)
            top_hga[ok] = np.maximum(top_hga[ok], hga[ri])
        base = kid & p_mex
        no_legal = base & (n_legal_par == 0)
        top = edu_label(top_hga)
        for g, gm in [(g, top == g) for g, _ in EDU] + [("all", np.ones(len(d), bool))]:
            sh, se, pop, n = share(W, base & gm, no_legal)
            kid_rows.append({"rules": name, "highest_parent_education": g,
                             "children_millions": round(pop, 3), "n": n,
                             "share_no_legal_parent_present": round(sh, 4), "se": round(se, 4)})

    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    pr, kr = pd.DataFrame(parent_rows), pd.DataFrame(kid_rows)
    pr.to_csv(out / "mexico_born_parents_by_status.csv", index=False)
    kr.to_csv(out / "usborn_children_by_parent_status.csv", index=False)
    pd.set_option("display.width", 200)
    print(pr.to_string(index=False))
    print()
    print(kr.to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""US-born children of Mexico-born parents today, by their parents' imputed legal status (CPS ASEC 2025).

Question (operator, 2026-09-23): are the children of illegal immigrants doing worse or better?

Groups among US-born children with at least one co-resident Mexico-born parent:
  * no_legal_parent -- every co-resident parent imputed unauthorized;
  * immigrant_parents_legal -- every co-resident parent foreign-born, at least one imputed legal;
  * us_born_parent -- a US-born parent is present.
Reference: children whose co-resident parents are all US-born non-Hispanic white.
Minors 0-17: poverty, insurance, family resources, parents' earnings. Young adults 18-24 still
living with a parent: schooling, college, work, idleness (CPS counts dormitory students at home).

Status comes from parent_status.py (Borjas rules, with and without the Medicaid clause). Several
rules read program receipt or government employment, so the legal cell mechanically absorbs
program users; poverty and insurance comparisons carry that bias, schooling and work less so.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/parent_status_2026_09_23/cps_children_outcomes.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from parent_status import CALIFORNIA, MEXICO, REPS, edu_label, impute, load  # noqa: E402

EXTRA = ["PEHSPNON", "PRDTRACE", "SPM_POOR", "PERLIS", "NOW_COV", "SPM_RESOURCES", "SPM_NUMPER",
         "PEARNVAL", "A_ENRLW", "A_HSCOL", "PEMLR"]
MINOR_OUT = ["spm_poor", "official_poor", "uninsured", "resources_per_person", "parents_earnings"]
YOUNG_OUT = ["hs_plus_19_24", "college_18_24", "employed", "neet"]


def parent_pointers(d: pd.DataFrame) -> dict:
    row_of = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_arrays([d.PH_SEQ, d.A_LINENO]))
    out = {}
    for col in ("PEPAR1", "PEPAR2"):
        want = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d[col].to_numpy()])
        out[col] = row_of.reindex(want).to_numpy()
    return out


def wls_sdr(y, X, W):
    """Coefficients under the full weight and each replicate; SDR standard errors."""
    betas = []
    for j in range(W.shape[1]):
        w = W[:, j]
        XtW = X.T * w
        betas.append(np.linalg.solve(XtW @ X, XtW @ y))
    B = np.array(betas)
    se = np.sqrt(4 / 160 * ((B[1:] - B[0]) ** 2).sum(0))
    return B[0], se


def wmean_sdr(v, W):
    m = (W * v[:, None]).sum(0) / W.sum(0)
    return float(m[0]), float(np.sqrt(4 / 160 * ((m[1:] - m[0]) ** 2).sum()))


def main():
    d, hh = load(extra=EXTRA)
    W = d[["pwwgt0"] + REPS].to_numpy(float)
    prow = parent_pointers(d)
    age, hga = d.A_AGE.to_numpy(), d.A_HGA.to_numpy()
    us_born = d.PRCITSHP.eq(1).to_numpy()
    nh_white = (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy()
    fb = d.PRCITSHP.isin([4, 5]).to_numpy()
    ca = d.state.eq(CALIFORNIA).to_numpy()

    o = pd.DataFrame(index=d.index)
    o["spm_poor"] = d.SPM_POOR.eq(1).astype(float)
    o["official_poor"] = d.PERLIS.eq(1).astype(float).where(d.PERLIS.ge(1))
    o["uninsured"] = d.NOW_COV.eq(2).astype(float)
    o["resources_per_person"] = d.SPM_RESOURCES / d.SPM_NUMPER
    o["hs_plus_19_24"] = (d.A_HGA >= 39).astype(float).where(d.A_AGE.between(19, 24))
    o["college_18_24"] = (d.A_HSCOL.eq(2) | (d.A_HGA >= 40)).astype(float)
    o["employed"] = d.PEMLR.isin([1, 2]).astype(float)
    o["neet"] = (~d.A_ENRLW.eq(1) & ~d.PEMLR.isin([1, 2])).astype(float)

    earn = d.PEARNVAL.to_numpy(float)
    pen = d.PENATVTY.to_numpy()
    n_par = np.zeros(len(d), int)
    all_white = np.ones(len(d), bool)
    any_usb = np.zeros(len(d), bool)
    all_fb = np.ones(len(d), bool)
    par_earn = np.zeros(len(d))
    top_hga = np.full(len(d), -1)
    rows_mex = np.zeros(len(d), bool)
    for col, r in prow.items():
        ok = ~np.isnan(r)
        ri = r[ok].astype(int)
        n_par[ok] += 1
        all_white[ok] &= us_born[ri] & nh_white[ri]
        any_usb[ok] |= us_born[ri]
        all_fb[ok] &= fb[ri]
        par_earn[ok] += earn[ri]
        top_hga[ok] = np.maximum(top_hga[ok], hga[ri])
        rows_mex[ok] |= fb[ri] & (pen[ri] == MEXICO)
    o["parents_earnings"] = par_earn
    has_par = n_par > 0
    two_par = (n_par == 2).astype(float)
    top = edu_label(top_hga)
    minor = us_born & (age < 18) & has_par
    young = us_born & (age >= 18) & (age <= 24) & has_par
    white_ref = has_par & all_white

    mean_rows, gap_rows = [], []
    for rules, use_med in (("borjas_paper_rules", True), ("no_medicaid_rule", False)):
        legal = impute(d, hh, use_medicaid_rule=use_med)["legal"]
        n_legal = np.zeros(len(d), int)
        for col, r in prow.items():
            ok = ~np.isnan(r)
            n_legal[ok] += legal[r[ok].astype(int)].astype(int)
        mexfam = rows_mex & has_par
        grp = {
            "no_legal_parent": mexfam & (n_legal == 0),
            "immigrant_parents_legal": mexfam & (n_legal > 0) & all_fb,
            "us_born_parent": mexfam & any_usb,
            "white_us_born_parents": white_ref,
        }
        for stage, base, outs in (("minor_0_17", minor, MINOR_OUT), ("young_adult_18_24", young, YOUNG_OUT)):
            for g, gm in grp.items():
                for edu_cell in ["all", "below_high_school", "high_school", "some_college", "bachelor_plus"]:
                    mask = base & gm & (np.ones(len(d), bool) if edu_cell == "all" else top == edu_cell)
                    r = {"rules": rules, "stage": stage, "group": g, "highest_parent_education": edu_cell,
                         "n": int(mask.sum()), "weighted_millions": round(W[mask, 0].sum() / 1e6, 3)}
                    for out in outs:
                        v = o[out].to_numpy(float)
                        ok = mask & ~np.isnan(v)
                        if ok.sum() >= 30:
                            m, se = wmean_sdr(v[ok], W[ok])
                            r[out], r[out + "_se"] = round(m, 4), round(se, 4)
                    mean_rows.append(r)
            # Adjusted gap: no legal parent minus legal immigrant parents, same-family-type controls.
            for out in outs:
                v = o[out].to_numpy(float)
                keep = base & (grp["no_legal_parent"] | grp["immigrant_parents_legal"]) & ~np.isnan(v)
                treat = grp["no_legal_parent"][keep].astype(float)
                cols = [np.ones(keep.sum()), treat, ca[keep].astype(float), two_par[keep]]
                for a in sorted(set(age[keep]))[1:]:
                    cols.append((age[keep] == a).astype(float))
                for cell in ("high_school", "some_college", "bachelor_plus"):
                    cols.append((top[keep] == cell).astype(float))
                X = np.column_stack(cols)
                raw_t, _ = wmean_sdr(v[keep][treat == 1], W[keep][treat == 1])
                raw_b, _ = wmean_sdr(v[keep][treat == 0], W[keep][treat == 0])
                beta, se = wls_sdr(v[keep], X, W[keep])
                gap_rows.append({"rules": rules, "stage": stage, "outcome": out,
                                 "no_legal_parent_mean": round(raw_t, 4), "legal_immigrant_parents_mean": round(raw_b, 4),
                                 "raw_diff": round(raw_t - raw_b, 4), "adjusted_diff": round(float(beta[1]), 4),
                                 "adjusted_se_sdr": round(float(se[1]), 4),
                                 "n_treat": int(treat.sum()), "n_base": int((treat == 0).sum())})

    out_dir = HERE / "derived"
    out_dir.mkdir(exist_ok=True)
    means, gaps = pd.DataFrame(mean_rows), pd.DataFrame(gap_rows)
    means.to_csv(out_dir / "cps_children_outcomes_means.csv", index=False)
    gaps.to_csv(out_dir / "cps_children_outcomes_gaps.csv", index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    show = means[means.highest_parent_education.eq("all")]
    print(show.drop(columns=[c for c in show.columns if c.endswith("_se")]).to_string(index=False))
    print()
    print(gaps.to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""California's imputed unauthorized residents and their Medi-Cal coverage, ACS 2024 1-year PUMS.

Status is the ACS mapping of the Borjas (2017) rules in
`unauthorized_population_size_2026_09_19/acs_residual.py`, imported unmodified. Two rules cannot be
applied as written on the ACS (that lane's docstring): (f) public housing or rent subsidy has no
PUMS item and is dropped; (i) spouse linkage exists only between the reference person and a
single spouse record. Rule (c) reads coverage at the interview (HINS3 Medicare, HINS4 Medicaid or
other means-tested, HINS5 TRICARE) plus Social Security and SSI income in the past 12 months,
where the CPS reads coverage at any time in the prior calendar year.

`no_medicaid_rule` passes `impute()` a copy of the frame with HINS4 set to "No" (2), which removes
Medicaid from rule (c) and changes nothing else.

Input: the lane's `_cache/acs2024_person_subset.parquet` (built from the local csv_pus.zip by its
`extract_pums.py`). Run from the repository root:
    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
        infra/immigration-fiscal/california_medical_status_2026_09_23/acs_ca_status.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANE = ROOT / "unauthorized_population_size_2026_09_19"
sys.path.insert(0, str(LANE))
import acs_residual as A  # noqa: E402

PARQUET = LANE / "_cache/acs2024_person_subset.parquet"
REPS = [f"PWGTP{i}" for i in range(1, 81)]
CALIFORNIA = 6
MEXICO = 303
AGE_BANDS = [("0-18", 0, 18), ("19-25", 19, 25), ("26-49", 26, 49), ("50-64", 50, 64),
             ("65+", 65, 200), ("50+", 50, 200), ("all", 0, 200)]
# unauthorized_population_size_2026_09_19/derived/acs2024_summary_cuba.json and
# acs2024_residual_by_region.csv (rounded to persons there).
GATE = {"national": 12_973_901, "mexico_born": 3_963_961}


def main():
    cols = ["SERIALNO", "SPORDER", "STATE", "PWGTP", "AGEP", "CIT", "YOEP", "NATIVITY", "POBP", "COW",
            "OCCP", "MIL", "HINS3", "HINS4", "HINS5", "SSP", "SSIP", "RELSHIPP"]
    d = pd.read_parquet(PARQUET, columns=cols)
    w = d.PWGTP.to_numpy(float)

    res = {"borjas_paper_rules": A.impute(d)}
    d_nm = d.copy()
    d_nm["HINS4"] = 2
    res["no_medicaid_rule"] = A.impute(d_nm)

    paper = res["borjas_paper_rules"]["unauthorized"]
    mex = (d.POBP.to_numpy() == MEXICO)
    got = {"national": w[paper].sum(), "mexico_born": w[paper & mex].sum()}
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    gate = pd.DataFrame([{"count": k, "published": v, "reproduced": round(got[k]),
                          "pass": abs(got[k] - v) <= 1} for k, v in GATE.items()])
    gate.to_csv(out / "acs_gate.csv", index=False)
    print(gate.to_string(index=False), flush=True)
    if not gate["pass"].all():
        raise SystemExit("[BLOCKED] ACS gate failed; no new numbers written")

    # Replicate weights for California rows only, joined on the person key.
    ca_rows = np.flatnonzero(d.STATE.to_numpy() == CALIFORNIA)
    rw = pd.read_parquet(PARQUET, columns=["SERIALNO", "SPORDER"] + REPS,
                         filters=[("STATE", "==", CALIFORNIA)])
    key = d.iloc[ca_rows][["SERIALNO", "SPORDER"]].reset_index(drop=True)
    rw = key.merge(rw, on=["SERIALNO", "SPORDER"], how="left", validate="one_to_one")
    if rw[REPS].isna().any().any():
        raise ValueError("California replicate join incomplete")
    Wca = np.column_stack([w[ca_rows], rw[REPS].to_numpy(float)])

    def total(m):
        t = Wca[m].sum(0)
        return float(t[0]), float(np.sqrt(4 / 80 * ((t[1:] - t[0]) ** 2).sum())), int(m.sum())

    def ratio(num, den):
        a, b = Wca[num & den].sum(0), Wca[den].sum(0)
        th = np.divide(a, b, out=np.full_like(b, np.nan), where=b > 0)
        return float(th[0]), float(np.sqrt(4 / 80 * ((th[1:] - th[0]) ** 2).sum()))

    c = d.iloc[ca_rows].reset_index(drop=True)
    age = c.AGEP.to_numpy()
    hins4 = c.HINS4.to_numpy() == 1
    household = ~c.SERIALNO.astype(str).str.contains("GQ").to_numpy()
    cmex = c.POBP.to_numpy() == MEXICO
    rows = []
    for rules, r in res.items():
        u = r["unauthorized"][ca_rows]
        moved = res["no_medicaid_rule"]["unauthorized"][ca_rows] & ~paper[ca_rows]
        for pop, pm in (("all_persons", np.ones(len(c), bool)), ("household_population", household)):
            for grp, gm in (("all_foreign_born", np.ones(len(c), bool)), ("mexico_born", cmex)):
                for band, lo, hi in AGE_BANDS:
                    den = u & pm & gm & (age >= lo) & (age <= hi)
                    p, pse, n = total(den)
                    k, kse, kn = total(den & hins4)
                    sh, shse = ratio(hins4, den)
                    mv, mvse, mvn = total(moved & pm & gm & (age >= lo) & (age <= hi))
                    rows.append({"rules": rules, "population": pop, "group": grp, "age": band,
                                 "unauthorized": round(p), "se": round(pse), "n": n,
                                 "medicaid_now": round(k), "medicaid_now_se": round(kse), "medicaid_now_n": kn,
                                 "medicaid_share": round(sh, 4), "medicaid_share_se": round(shse, 4),
                                 "moved_by_medicaid_clause": round(mv) if rules == "no_medicaid_rule" else 0,
                                 "moved_se": round(mvse) if rules == "no_medicaid_rule" else 0,
                                 "moved_n": mvn if rules == "no_medicaid_rule" else 0})
    t = pd.DataFrame(rows)
    t.to_csv(out / "acs_ca_counts_by_age.csv", index=False)

    # All Californians with Medicaid/means-tested coverage at interview, for the survey-vs-DHCS
    # calibration against total certified eligibles.
    rows = []
    groups = AGE_BANDS + [("19-44", 19, 44), ("45-64", 45, 64)]
    for pop, pm in (("all_persons", np.ones(len(c), bool)), ("household_population", household)):
        for band, lo, hi in groups:
            k, kse, kn = total(pm & hins4 & (age >= lo) & (age <= hi))
            rows.append({"population": pop, "age": band, "medicaid_now_all_residents": round(k),
                         "se": round(kse), "n": kn})
    pd.DataFrame(rows).to_csv(out / "acs_ca_all_medicaid.csv", index=False)

    # Why no senior stays unauthorized: every noncitizen 65+ with HINS4 also carries HINS3.
    noncit65 = (c.CIT.to_numpy() == 5) & (age >= 65) & hins4
    mc, _, mcn = total(noncit65)
    both, _, _ = total(noncit65 & (c.HINS3.to_numpy() == 1))
    pd.DataFrame([{"region": "California", "noncitizens_65plus_with_HINS4": round(mc), "n": mcn,
                   "share_with_HINS3": round(both / mc, 4)}]).to_csv(out / "acs_65plus_medicare.csv", index=False)

    pd.set_option("display.width", 220)
    show = t[(t.population == "all_persons")]
    print(show.to_string(index=False))
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()

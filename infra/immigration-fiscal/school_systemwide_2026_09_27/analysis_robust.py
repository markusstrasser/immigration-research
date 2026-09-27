"""Robustness of the Test 2 estimates that carry the verdict: leave-one-state-out, a state-label
permutation test, and the cohort-lagged English-learner measure under the same controls.

Writes derived/robust_leave_one_out.csv, derived/robust_permutation.csv and derived/robust_lag_el.csv.
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_robust.py
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_lags import add_measures  # noqa: E402
from analysis_naep import FIELDS, TREAT, fmt, record, stack, write  # noqa: E402
from panel import MAIN_YEARS, build  # noqa: E402
from stats_util import ols  # noqa: E402

OUT = HERE / "derived"
REPS = 2000
SEED = 20260928


def leave_one_out(p):
    rows = []
    for tkey in ("el", "hisp"):
        col = TREAT[tkey][0]
        d = stack(p, MAIN_YEARS, "white")
        for weight in (None, "ccd_total"):
            full = ols(d, "z", [col], fe=["cell_state", "cell_year"], cluster="state", weight=weight)[col]
            for s in sorted(d.state.unique()):
                r = ols(d[d.state != s], "z", [col], fe=["cell_state", "cell_year"], cluster="state", weight=weight)[col]
                rows.append({"treatment": tkey, "weight": weight or "none", "dropped": s,
                             "beta_per10": fmt(10 * r["coef"]), "se": fmt(10 * r["se"]),
                             "full_beta_per10": fmt(10 * full["coef"])})
    return rows


def permutation(p):
    """Shuffle which state's share series each state receives (cell and year kept), 2,000 draws."""
    rows = []
    rng = np.random.default_rng(SEED)
    for tkey in ("el", "hisp", "imm"):
        col = TREAT[tkey][0]
        yrs = [y for y in MAIN_YEARS if y >= (2007 if tkey == "imm" else 2003)]
        d = stack(p, yrs, "white").dropna(subset=["z", col]).reset_index(drop=True)
        base = ols(d, "z", [col], fe=["cell_state", "cell_year"], cluster="state")[col]["coef"]
        lookup = {(c, s, y): v for c, s, y, v in zip(d.cell, d.state, d.year, d[col])}
        states = sorted(d.state.unique())
        draws = []
        for _ in range(REPS):
            perm = dict(zip(states, rng.permutation(states)))
            x = np.array([lookup.get((c, perm[s], y), np.nan) for c, s, y in zip(d.cell, d.state, d.year)])
            dd = d.assign(xp=x)
            draws.append(ols(dd, "z", ["xp"], fe=["cell_state", "cell_year"], cluster="state")["xp"]["coef"])
        draws = np.array(draws)
        rows.append({"treatment": tkey, "outcome": "white", "beta_per10": fmt(10 * base),
                     "perm_p_two_sided": fmt((np.sum(np.abs(draws) >= abs(base) - 1e-15) + 1) / (REPS + 1)),
                     "perm_sd_per10": fmt(10 * draws.std(ddof=1)), "reps": REPS, "seed": SEED,
                     "years": f"{min(yrs)}-{max(yrs)}"})
    return rows


def lag_el(p):
    """The grade-4 K–1 CCD English-learner measure and the grade-8 same-cohort NAEP measure under the
    main-table controls."""
    q = add_measures(p)
    q["ccd_w"] = q.ccd_total
    rows = []
    for measure, G in (("el_ccd_k1", 4), ("el_g4_lag", 8)):
        d = stack(q[q.grade == G], MAIN_YEARS, "white").dropna(subset=[measure, "z"])
        specs = [("twfe", {}), ("twfe_region_year", {"fe_extra": ["region_cell_year"]}),
                 ("twfe_weighted", {"weight": "ccd_w"}), ("twfe_no_TX", {"drop": "TX"}), ("twfe_no_CA", {"drop": "CA"})]
        for spec, kw in specs:
            dd = d[d.state != kw["drop"]] if "drop" in kw else d
            res = ols(dd, "z", [measure], fe=["cell_state", "cell_year"] + kw.get("fe_extra", []), cluster="state",
                      weight=kw.get("weight"))
            record(rows, res, measure, test="naep_lag_robust", spec=spec, treatment=measure, outcome="white",
                   cell=f"grade{G}", units="SD", years=f"{dd.year.min()}-{dd.year.max()}", note="")
        # lead: the share of the next cohort (next wave) added
        dd = d.sort_values(["cell", "state", "year"]).copy()
        dd["lead"] = dd.groupby(["cell", "state"])[measure].shift(-1)
        dd = dd.dropna(subset=["lead"])
        res = ols(dd, "z", [measure, "lead"], fe=["cell_state", "cell_year"], cluster="state")
        record(rows, res, "lead", test="naep_lag_robust", spec="lead", treatment=measure, outcome="white",
               cell=f"grade{G}", units="SD", years=f"{dd.year.min()}-{dd.year.max()}",
               note="next wave's value of the lagged measure, current value held fixed")
    return rows


def main():
    p = build()
    loo = leave_one_out(p)
    with (OUT / "robust_leave_one_out.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(loo[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(loo)
    perm = permutation(p)
    with (OUT / "robust_permutation.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(perm[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(perm)
    write(OUT / "robust_lag_el.csv", lag_el(p), FIELDS)
    print("done")


if __name__ == "__main__":
    main()

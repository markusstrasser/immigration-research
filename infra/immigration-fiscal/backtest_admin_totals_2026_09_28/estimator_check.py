#!/usr/bin/env python3
"""Does the delta estimator work on this frame? A synthetic check on the frame's own replicates, no external figure.

For each keyed prediction of the adopted reading and each allocation, 160 synthetic "truths" are drawn from the
replicates: P* = P + 2 (P_k - P) and g* = g + 2 (g_k - g). A successive-difference replicate deviates from the full
sample by half the sampling standard deviation, so the factor 2 gives each truth one sampling draw of noise. The
administrative shares a key with misstatement delta would produce, A = P* (1 + delta g*) / (1 + delta g*bar), are
then scored exactly as phase 2 will score the real ones: estimators.delta_fit on the full-sample P and g,
estimators.delta_se over the replicates, estimators.call at the declared tolerance (derived/power.csv). The model
has no misfit here, so the check measures bias and calibration under sampling noise only.

Writes derived/estimator_check.csv: mean and spread of the estimate, mean scored SE, 95% coverage, and how often
the call is a miss, a hit or no power, at delta = 0 and +-0.3.

Run from the repository root after predict.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backtest_admin_totals_2026_09_28/estimator_check.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from estimators import Z, call, delta_fit, delta_se  # noqa: E402

FRAME = "asec2025_adopted"
SERIES = {"1_refundable_credits": "credits_ssn", "2_ssi": "ssi", "2_oasdi": "social_security"}
DELTAS = (0.0, 0.3, -0.3)
COLS = [f"r{k}" for k in range(161)]


def main() -> None:
    reps = pd.read_csv(HERE / "derived/state_replicates.csv.gz")
    power = pd.read_csv(HERE / "derived/power.csv")
    rows = []
    for check, series in SERIES.items():
        s = reps[(reps.frame == FRAME) & (reps.check == check) & (reps.series == series)]
        P = s[s.quantity == "share"][COLS].to_numpy()
        for allocation in ("shared", "personal"):
            g = s[s.quantity == f"group_share_{allocation}"][COLS].to_numpy()
            tolerance = power.loc[(power.frame == FRAME) & (power.statistic == f"delta_{series}_{allocation}"),
                                  "tolerance"].item()
            for truth in DELTAS:
                est, se, calls = [], [], []
                for k in range(1, 161):
                    p_true = np.clip(P[:, 0] + 2 * (P[:, k] - P[:, 0]), 1e-9, None)
                    p_true /= p_true.sum()
                    g_true = np.clip(g[:, 0] + 2 * (g[:, k] - g[:, 0]), 0.0, 1.0)
                    A = p_true * (1 + truth * g_true) / (1 + truth * (p_true * g_true).sum())
                    fit = delta_fit(A, P[:, 0], g[:, 0])
                    scored = delta_se(fit, [delta_fit(A, P[:, j], g[:, j])["delta"] for j in range(161)])
                    est.append(fit["delta"])
                    se.append(scored)
                    calls.append(call(fit["delta"], scored, tolerance))
                est, se, calls = np.array(est), np.array(se), np.array(calls)
                rows.append(dict(check=check, series=series, allocation=allocation, delta_true=truth,
                                 tolerance=tolerance, mean_estimate=est.mean(), sd_estimate=est.std(ddof=1),
                                 mean_scored_se=se.mean(), coverage_95=np.mean(np.abs(est - truth) <= Z * se),
                                 share_miss=np.mean(calls == "miss"), share_hit=np.mean(calls == "hit"),
                                 share_no_power=np.mean(calls == "no power")))
                print(f"  ✓ {series} {allocation} delta {truth:+.1f}: mean {est.mean():+.3f}, sd {est.std(ddof=1):.3f}, "
                      f"scored SE {se.mean():.3f}; miss {np.mean(calls == 'miss'):.2f}")
    pd.DataFrame(rows).to_csv(HERE / "derived/estimator_check.csv", index=False, float_format="%.10g",
                              lineterminator="\n")


if __name__ == "__main__":
    main()

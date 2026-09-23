"""Independent check of the key estimates in derived/estimates.csv.

Recomputes, without iv.py's partialling-out, the break-free stacked Bartik 2SLS, the brief's main
2012-2022 two-instrument 2SLS and its OLS: full design matrices with every fixed-effect dummy,
two stages by least squares on all exogenous columns, and the full cluster sandwich (CR1). The
Anderson-Rubin bounds of the stacked Bartik spec are checked by direct regressions of y - b x on the
instrument and controls at the reported ends (statistic at the 5% chi-square critical value).
Exits non-zero on any mismatch.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import estimate as E  # noqa: E402  (data constructors only; no estimator is reused)

CRIT = 3.841458820694124


def design(d, controls):
    fe = pd.get_dummies(d.fe, drop_first=True, dtype=float).to_numpy()
    return np.column_stack([np.ones(len(d))] + [d[c].to_numpy(float) for c in controls] + [fe])


def sandwich(X, u, groups, k):
    xtx_inv = np.linalg.pinv(X.T @ X)
    G = pd.Series(range(len(groups))).groupby(groups).indices
    meat = np.zeros((X.shape[1], X.shape[1]))
    for idx in G.values():
        s = X[idx].T @ u[idx]
        meat += np.outer(s, s)
    n, g = X.shape[0], len(G)
    return xtx_inv @ meat @ xtx_inv * g / (g - 1) * (n - 1) / (n - k)


def full_2sls(d, instruments, weighted=True, controls=("lnpop0",)):
    s = np.sqrt(d.w.to_numpy(float) / d.w.mean()) if weighted else np.ones(len(d))
    W = design(d, controls) * s[:, None]
    y, x = d.dy.to_numpy(float) * s, d.dx.to_numpy(float) * s
    k = np.linalg.matrix_rank(W)
    if not instruments:
        X = np.column_stack([x, W])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        V = sandwich(X, y - X @ b, d.state.to_numpy(), k + 1)
        return b[0], math.sqrt(V[0, 0])
    Z = np.column_stack([d[z].to_numpy(float) * s for z in instruments] + [W])
    xhat = Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    Xh = np.column_stack([xhat, W])
    b = np.linalg.lstsq(Xh, y, rcond=None)[0]
    u = y - np.column_stack([x, W]) @ b
    V = sandwich(Xh, u, d.state.to_numpy(), k + 1)
    return b[0], math.sqrt(V[0, 0])


def ar_direct(d, z, b0, weighted=True, controls=("lnpop0",)):
    s = np.sqrt(d.w.to_numpy(float) / d.w.mean()) if weighted else np.ones(len(d))
    W = design(d, controls) * s[:, None]
    r = (d.dy.to_numpy(float) - b0 * d.dx.to_numpy(float)) * s
    X = np.column_stack([d[z].to_numpy(float) * s, W])
    coef = np.linalg.lstsq(X, r, rcond=None)[0]
    V = sandwich(X, r - X @ coef, d.state.to_numpy(), np.linalg.matrix_rank(X))
    return coef[0] ** 2 / V[0, 0]


def main():
    est = pd.read_csv(HERE / "derived" / "estimates.csv", dtype={"window": str})
    def stored(window, inst, note=None):
        m = est[(est.window == window) & (est.outcome == "admin") & (est["sample"] == "all") & est.weighted
                & (est.controls == "lnpop0") & (est.instruments.fillna("") == inst)]
        m = m[m.note.isna()] if note is None else m[m.note == note]
        assert len(m) == 1, (window, inst, len(m))
        return m.iloc[0]
    fails = 0
    checks = [("stacked 0712+1217", ("bartik",), E.stacked_early("admin"), "2007 shares for both periods"),
              ("1222", ("bartik", "imm"), E.long_difference("1222", "admin"), None),
              ("1222", (), E.long_difference("1222", "admin"), None),
              ("0717", ("bartik",), E.long_difference("0717", "admin"), None)]
    for window, inst, d, note in checks:
        r = stored(window, "+".join(inst), note)
        b, se = full_2sls(d, inst)
        ok = abs(b - r.beta) < 1e-4 * max(1, abs(b)) and abs(se - r.se) < 1e-4 * max(1, se)
        fails += not ok
        print(f"  {'PASS' if ok else 'FAIL'} {window} {'+'.join(inst) or 'OLS'}: full-matrix {b:.5f} ({se:.5f}) "
              f"vs stored {r.beta:.5f} ({r.se:.5f})")
    d = E.stacked_early("admin")
    r = stored("stacked 0712+1217", "bartik", "2007 shares for both periods")
    for end in ("ar_lo", "ar_hi"):
        stat = ar_direct(d, "bartik", r[end])
        ok = abs(stat - CRIT) < 1e-3 * CRIT
        fails += not ok
        print(f"  {'PASS' if ok else 'FAIL'} Anderson-Rubin {end} {r[end]:.4f}: direct statistic {stat:.4f} vs 3.8415")
    if fails:
        print(f"[BLOCKED] {fails} verification failures")
        return 1
    print("all verification checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

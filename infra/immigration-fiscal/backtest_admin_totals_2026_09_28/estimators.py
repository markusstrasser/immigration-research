"""Frozen scoring estimators for the back-test; predict.py uses them for the power screen, score.py for the scores.

`delta_fit` reads a key's misstatement for the group off state totals. If the group's true dollars on a key are
(1 + delta) times what the key puts on it and everyone else's are right, a state's true share of the national total
is A_s = P_s (1 + delta g_s) / (1 + delta g), where P_s is the key's predicted share, g_s the group's share of the
state's predicted amount and g = sum_s P_s g_s the group's national share. So r_s = A_s / P_s - 1 equals
beta (g_s - g) with beta = delta / (1 + delta g). The fit is weighted least squares of r_s on (g_s - g) through the
origin, weights P_s (both have P-weighted mean zero), with HC1 and HC3 standard errors; delta = beta / (1 - beta g).
"""
from __future__ import annotations

import numpy as np

Z = 1.96
CHI2_95 = {5: 11.0705}  # 95th percentile of chi-square, 5 df (NIST/SEMATECH e-Handbook, table 1.3.6.7.4)


def delta_fit(A, P, g) -> dict[str, float]:
    A, P, g = (np.asarray(x, float) for x in (A, P, g))
    gbar = float((P * g).sum() / P.sum())
    r, x, w = A / P - 1, g - gbar, P / P.sum()
    sxx = float((w * x * x).sum())
    beta = float((w * x * r).sum() / sxx)
    e = r - beta * x
    n = len(A)
    lever = w * x * x / sxx  # leverage of each state in the one-regressor weighted fit
    se_hc1 = float(np.sqrt(n / (n - 1) * (w * w * x * x * e * e).sum()) / sxx)
    se_hc3 = float(np.sqrt((w * w * x * x * e * e / (1 - lever) ** 2).sum()) / sxx)
    scale = (1 - beta * gbar) ** 2
    return {"beta": beta, "delta": beta / (1 - beta * gbar), "se_hc1": se_hc1 / scale, "se_hc3": se_hc3 / scale,
            "gbar": gbar, "max_leverage": float(lever.max())}


def delta_fit_controlled(A, P, g, h) -> dict[str, float]:
    """delta_fit with a second share as control: h_s, other foreign-born persons' share of the state's predicted
    amount. Model A_s = P_s (1 + delta g_s + gamma h_s) / (1 + delta g + gamma h), fitted as weighted least
    squares of r_s on (g_s - g) and (h_s - h) through the origin, weights P_s, HC3 covariance; delta =
    beta_g / (1 - beta_g g - beta_h h). A declared diagnostic: does a miss follow the group or immigrants at large?"""
    A, P, g, h = (np.asarray(x, float) for x in (A, P, g, h))
    w = P / P.sum()
    gbar, hbar = float((w * g).sum()), float((w * h).sum())
    X = np.column_stack([g - gbar, h - hbar])
    r = A / P - 1
    inv = np.linalg.inv(X.T @ (w[:, None] * X))
    b = inv @ (X.T @ (w * r))
    e = r - X @ b
    lever = w * np.einsum("ij,jk,ik->i", X, inv, X)
    V = inv @ (X.T @ ((w * w * e * e / (1 - lever) ** 2)[:, None] * X)) @ inv
    den = 1 - b[0] * gbar - b[1] * hbar
    grad = np.array([1 - b[1] * hbar, b[0] * hbar]) / den ** 2
    return {"delta": float(b[0] / den), "gamma": float(b[1] / den), "se_hc3": float(np.sqrt(grad @ V @ grad)),
            "gbar": gbar, "hbar": hbar}


def delta_se(fit: dict[str, float], replicate_deltas) -> float:
    """The scored standard error of delta, the larger of two estimates. The replicate term is the spread of delta
    over the frame's 160 replicates with the administrative shares held (successive-difference formula; index 0 is
    the full sample): the frame's sampling error alone. The fit's HC3 term reads the residuals, which carry that
    sampling error and the state model's misfit, and it corrects for the leverage of the largest states. Adding
    the two in quadrature would count the sampling error twice."""
    reps = np.asarray(replicate_deltas, float)
    replicate = float(np.sqrt(4 / 160 * np.square(reps[1:] - reps[0]).sum()))
    return max(fit["se_hc3"], replicate)


def implied_share(s: float, delta: float) -> float:
    """The group's share of a key's national total when its true dollars are (1 + delta) times the key's."""
    return s * (1 + delta) / (1 + delta * s)


def slope_on(A, P, pi) -> dict[str, float]:
    """The brief's descriptive slope: P-weighted least squares of r_s = A_s / P_s - 1 on the state's group
    population share pi_s, with intercept; HC1 standard error."""
    A, P, pi = (np.asarray(x, float) for x in (A, P, pi))
    w = P / P.sum()
    r = A / P - 1
    x = pi - (w * pi).sum()
    y = r - (w * r).sum()
    sxx = float((w * x * x).sum())
    b = float((w * x * y).sum() / sxx)
    e = y - b * x
    n = len(A)
    return {"slope": b, "se_hc1": float(np.sqrt(n / (n - 2) * (w * w * x * x * e * e).sum()) / sxx)}


def dissimilarity(A, X) -> float:
    """Half the summed absolute share differences: the fraction of the national total placed in the wrong state."""
    return float(0.5 * np.abs(np.asarray(A, float) - np.asarray(X, float)).sum())


def call(error: float, se: float, tolerance: float) -> str:
    """The pre-registered verdict for one statistic: a miss is material (beyond the tolerance) and significant
    (beyond 1.96 standard errors); a result that is not a miss has no power when its 95% interval is wider than
    twice the tolerance; anything else is a hit."""
    if abs(error) > tolerance and abs(error) > Z * se:
        return "miss"
    if Z * se > 2 * tolerance:
        return "no power"
    return "hit"


def wald(A, P, cov) -> float:
    """Wald statistic of cell shares A against predicted shares P with covariance cov, dropping the last cell
    (shares sum to one)."""
    diff = (np.asarray(A, float) - np.asarray(P, float))[:-1]
    return float(diff @ np.linalg.solve(np.asarray(cov, float)[:-1, :-1], diff))


def replicate_cov(cells) -> np.ndarray:
    """Covariance of cell shares from a cells x 161 array (successive-difference replicates; column 0 full)."""
    cells = np.asarray(cells, float)
    dev = cells[:, 1:] - cells[:, :1]
    return 4 / 160 * dev @ dev.T


def distribution_call(A, P, cov, tolerance: float, noise: float) -> str:
    """The pre-registered verdict for a distribution over k cells: a miss is material (dissimilarity beyond the
    tolerance) and significant (Wald statistic beyond the 95th percentile of chi-square with k - 1 degrees of
    freedom); a result that is not a miss has no power when sampling noise alone is expected to produce a
    dissimilarity beyond the tolerance; anything else is a hit."""
    k = len(np.asarray(P))
    if dissimilarity(A, P) > tolerance and wald(A, P, cov) > CHI2_95[k - 1]:
        return "miss"
    if noise > tolerance:
        return "no power"
    return "hit"

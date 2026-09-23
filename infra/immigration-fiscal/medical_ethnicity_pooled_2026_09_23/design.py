"""Survey-design primitives for the pooled MEPS lane.

The estimator is the with-replacement stratified-PSU Taylor linearization that
`build/meps_health_transport_2024.py::donor_model` and the 2024 lane
(`meps_mexican_origin_medical_2026_09_22/meps_mexican.py`) use:

    z_i = w_i (y_i - theta) / W   in the domain, 0 outside
    V   = sum_h n_h/(n_h - 1) sum_a (z_ha - zbar_h)^2

Every estimate is carried as (value, PSU totals of its influence values), so
ratios, differences and dollar-weighted sums across cells are exact linear
compositions and their variances come from one formula. Records with zero
weight carry zero influence, which is how MEPS asks subpopulations to be handled
(HC-036 documentation, section 5.0: read all respondents, flag the domain).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

Z95 = 1.959963984540054  # standard normal 0.975 quantile [CALCULATION: constant]


class Design:
    def __init__(self, stratum: np.ndarray, psu: np.ndarray, weight: np.ndarray):
        stratum = np.asarray(stratum).astype(np.int64)
        psu = np.asarray(psu).astype(np.int64)
        pos = np.asarray(weight) > 0
        key = stratum * 1000 + psu
        uniq = np.unique(key[pos])
        self.n_psu = len(uniq)
        self.psu_index = np.full(len(key), -1, dtype=np.int64)
        idx = np.searchsorted(uniq, key)
        hit = pos & (idx < len(uniq))
        hit[hit] = uniq[idx[hit]] == key[hit]
        self.psu_index[hit] = idx[hit]
        strata_of_psu = uniq // 1000
        self.strata = np.unique(strata_of_psu)
        self.stratum_of_psu = np.searchsorted(self.strata, strata_of_psu)
        counts = np.bincount(self.stratum_of_psu)
        if (counts < 2).any():
            raise ValueError("lonely PSU stratum; no silent variance fallback")
        self.n_h = counts
        self.mult = counts / (counts - 1.0)

    def totals(self, z: np.ndarray) -> np.ndarray:
        keep = self.psu_index >= 0
        return np.bincount(self.psu_index[keep], weights=z[keep], minlength=self.n_psu)

    def var(self, T: np.ndarray) -> float:
        """Variance from a PSU-total vector."""
        sums = np.bincount(self.stratum_of_psu, weights=T)
        means = sums / self.n_h
        dev = T - means[self.stratum_of_psu]
        ss = np.bincount(self.stratum_of_psu, weights=dev * dev)
        return float((self.mult * ss).sum())


@dataclass
class Est:
    value: float
    T: np.ndarray          # PSU totals of the linearized influence values
    n: int = 0             # unweighted records behind the estimate (domain size)
    W: float = 0.0         # weighted domain size

    def se(self, design: Design) -> float:
        if not np.isfinite(self.value):
            return float("nan")
        return float(np.sqrt(design.var(self.T)))


def mean(design: Design, y: np.ndarray, w: np.ndarray, mask: np.ndarray) -> Est:
    wm = w * mask
    W = wm.sum()
    if W <= 0:
        return Est(float("nan"), np.zeros(design.n_psu), 0, 0.0)
    theta = float((wm * y).sum() / W)
    z = wm * (y - theta) / W
    return Est(theta, design.totals(z), int(mask.sum()), float(W))


def total(design: Design, y: np.ndarray, w: np.ndarray, mask: np.ndarray) -> Est:
    wm = w * mask
    return Est(float((wm * y).sum()), design.totals(wm * y), int(mask.sum()), float(wm.sum()))


def combo(parts: list[tuple[float, Est]]) -> Est:
    value = sum(a * e.value for a, e in parts)
    T = sum(a * e.T for a, e in parts)
    return Est(float(value), T, sum(e.n for _, e in parts), 0.0)


def ratio(num: Est, den: Est) -> Est:
    if not (np.isfinite(num.value) and np.isfinite(den.value)) or den.value == 0:
        return Est(float("nan"), np.zeros_like(num.T), num.n, 0.0)
    r = num.value / den.value
    return Est(r, (num.T - r * den.T) / den.value, num.n, 0.0)


def log_est(e: Est) -> Est:
    if not np.isfinite(e.value) or e.value <= 0:
        return Est(float("nan"), np.zeros_like(e.T), e.n, 0.0)
    return Est(float(np.log(e.value)), e.T / e.value, e.n, e.W)


def exp_est(e: Est) -> Est:
    v = float(np.exp(e.value))
    return Est(v, v * e.T, e.n, e.W)


def weighted_quantile(y: np.ndarray, w: np.ndarray, q: float) -> float:
    """Smallest y with cumulative weight share >= q (type-1 inverse CDF)."""
    order = np.argsort(y, kind="mergesort")
    ys, ws = y[order], w[order]
    cw = np.cumsum(ws)
    if cw[-1] <= 0:
        return float("nan")
    k = int(np.searchsorted(cw, q * cw[-1], side="left"))
    return float(ys[min(k, len(ys) - 1)])


def chi2_sf(x: float, k: int) -> float:
    """Upper tail of a chi-square with k degrees of freedom, via the regularized
    incomplete gamma function Q(k/2, x/2) (series / continued fraction, Numerical
    Recipes 6.2). No scipy in this environment."""
    a, x2 = k / 2.0, x / 2.0
    if x2 <= 0:
        return 1.0
    from math import exp, lgamma, log
    gln = lgamma(a)
    if x2 < a + 1:
        ap, s, delt = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1
            delt *= x2 / ap
            s += delt
            if abs(delt) < abs(s) * 1e-14:
                break
        return 1.0 - s * exp(-x2 + a * log(x2) - gln)
    b = x2 + 1 - a
    c, d = 1.0 / 1e-300, 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        delt = d * c
        h *= delt
        if abs(delt - 1) < 1e-14:
            break
    return exp(-x2 + a * log(x2) - gln) * h

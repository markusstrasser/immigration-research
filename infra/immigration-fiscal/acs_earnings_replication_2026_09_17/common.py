"""Shared age-band and gap machinery for the ACS/CPS earnings replication."""
from __future__ import annotations

import numpy as np

BAND_EDGES = [18, 25, 35, 45, 55, 65, 75]
BAND_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
NBANDS = len(BAND_LABELS)


def bands_of(age: np.ndarray) -> np.ndarray:
    return np.digitize(np.asarray(age), BAND_EDGES)


def cell_totals(mask: np.ndarray, band: np.ndarray, weights: np.ndarray,
                values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Per (band, replicate) weighted population and value totals for one group.

    weights: (n_person, n_rep) with column 0 the full weight.
    Returns {"n": (B,R)} plus {name: (B,R)} weighted sums.
    """
    idx = band[mask]
    w = weights[mask]
    nrep = w.shape[1]
    out = {}
    n = np.zeros((NBANDS, nrep))
    for r in range(nrep):
        n[:, r] = np.bincount(idx, weights=w[:, r], minlength=NBANDS)
    out["n"] = n
    for name, v in values.items():
        vv = v[mask]
        tot = np.zeros((NBANDS, nrep))
        for r in range(nrep):
            tot[:, r] = np.bincount(idx, weights=w[:, r] * vv, minlength=NBANDS)
        out[name] = tot
    return out


def sdr(vec: np.ndarray, denom: int) -> tuple[float, float]:
    """Point estimate (replicate 0) and successive-difference SE.

    denom is 80 for ACS (4/80) and 160 for CPS (4/160).
    """
    vec = np.asarray(vec, dtype=float)
    return float(vec[0]), float(np.sqrt(4.0 / denom * np.square(vec[1:] - vec[0]).sum()))


def safe_div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=float)
    np.divide(a, b, out=out, where=b > 0)
    return out


def common_age_gap(group: dict, ref: dict, key: str, shares: np.ndarray) -> np.ndarray:
    """Common-age per-person gap vector over replicates.

    sum_b s_b [Y_gb/N_gb - Y_rb/N_rb] with fixed full-weight reference shares s.
    """
    g = safe_div(group[key], group["n"])
    r = safe_div(ref[key], ref["n"])
    return shares @ (g - r)


def age_matched_total_gap(group: dict, ref: dict, key: str) -> np.ndarray:
    """sum_b [Y_gb - (N_gb/N_rb) Y_rb] over replicates; reference schedule per replicate."""
    ratio = safe_div(group["n"], ref["n"])
    return (group[key] - ratio * ref[key]).sum(axis=0)


def crude_mean(group: dict, key: str) -> np.ndarray:
    return safe_div(group[key].sum(axis=0), group["n"].sum(axis=0))

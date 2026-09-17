"""Small linear-account / replicate helpers, with shared-donor uncertainty."""
from __future__ import annotations

import numpy as np


def summarize(values, gradient, donor_cov):
    values = np.asarray(values, dtype=float)
    gradient = np.asarray(gradient, dtype=float)
    if values.shape != (161,) or not np.isfinite(values).all():
        raise ValueError("Expected 161 finite CPS estimates")
    cps = 4 / 160 * np.square(values[1:] - values[0]).sum()
    health = float(gradient @ donor_cov @ gradient)
    if health < -1e-5:
        raise ValueError("Negative donor variance")
    se = float(np.sqrt(cps + max(health, 0)))
    return dict(estimate=float(values[0]), se_cps=float(np.sqrt(cps)),
                se_meps=float(np.sqrt(max(health, 0))), se_joint=se,
                ci95_low=float(values[0] - 1.96 * se),
                ci95_high=float(values[0] + 1.96 * se))


def sufficient(values, exposures, weights, masks, bands, band_count=8,
               population_weights=None, health_weights=None):
    """Arrays: group x band x component/cell x replicate; exact band coverage."""
    output = {}
    for group, mask in masks.items():
        ns, ys, hs = [], [], []
        for band in range(band_count):
            selected = np.asarray(mask) & (bands == band)
            w = weights[selected]
            population_w = w if population_weights is None else population_weights[selected]
            health_w = w if health_weights is None else health_weights[selected]
            n = population_w.sum(axis=0)
            if not np.isfinite(n).all() or (n <= 0).any():
                raise ValueError(f"Nonpositive/nonfinite population: {group}, band {band}")
            ns.append(n)
            ys.append(values[selected].T @ w)
            hs.append(exposures[selected].T @ health_w)
        output[group] = dict(n=np.array(ns), y=np.array(ys), h=np.array(hs))
    return output


def account(cell, coefficients, medical_means):
    """Balance total per age band and replicate; public medical sign negative."""
    y = np.einsum("bkr,k->br", cell["y"], coefficients)
    y -= np.einsum("bjr,j->br", cell["h"], medical_means)
    return y


def contrast(target, reference, coefficients, medical_means, matched=True):
    """Recompute populations and reference schedule in every replicate."""
    tg = account(target, coefficients, medical_means)
    rf = account(reference, coefficients, medical_means)
    if matched:
        ratio = target["n"] / reference["n"]
        gap = (tg - ratio * rf).sum(axis=0)
        derivative = -(target["h"][:, :, 0] - ratio[:, 0, None] * reference["h"][:, :, 0]).sum(axis=0)
    else:
        ratio = target["n"].sum(axis=0) / reference["n"].sum(axis=0)
        gap = tg.sum(axis=0) - ratio * rf.sum(axis=0)
        derivative = -(target["h"][:, :, 0].sum(axis=0) - ratio[0] * reference["h"][:, :, 0].sum(axis=0))
    return gap, derivative


def sum_cells(cells):
    return {key: sum(cell[key] for cell in cells) for key in ["n", "y", "h"]}


def standardized_gap(target, reference, coefficients, medical_means, age_shares):
    """Per-person gap at one fixed age distribution, conditional on its shares."""
    shares = np.asarray(age_shares)
    if shares.shape != (len(target["n"]),) or not np.isclose(shares.sum(), 1) or (shares < 0).any():
        raise ValueError("Invalid age-standard shares")
    value = (shares[:, None] * (account(target, coefficients, medical_means)/target["n"]
                               - account(reference, coefficients, medical_means)/reference["n"])).sum(axis=0)
    gradient = -(shares[:, None] * (target["h"][:, :, 0]/target["n"][:, 0, None]
                                    - reference["h"][:, :, 0]/reference["n"][:, 0, None])).sum(axis=0)
    return value, gradient

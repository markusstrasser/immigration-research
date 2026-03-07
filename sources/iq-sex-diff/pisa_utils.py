"""Shared utilities for PISA 2018 analysis scripts."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd


def weighted_group_standardize(values: np.ndarray, groups: np.ndarray, weights: np.ndarray) -> np.ndarray:
    out = np.full(values.shape, np.nan, dtype=float)
    for group in pd.unique(groups):
        mask = groups == group
        x = values[mask]
        w = weights[mask]
        valid = ~np.isnan(x)
        if valid.sum() == 0:
            continue
        xv = x[valid]
        wv = w[valid]
        mean = np.average(xv, weights=wv)
        var = np.average((xv - mean) ** 2, weights=wv)
        sd = math.sqrt(var) if var > 0 else 1.0
        z = np.full(x.shape, np.nan, dtype=float)
        z[valid] = (xv - mean) / sd
        out[mask] = z
    return out


def weighted_demean(values: np.ndarray, groups: np.ndarray, weights: np.ndarray) -> np.ndarray:
    out = np.full(values.shape, np.nan, dtype=float)
    for group in pd.unique(groups):
        mask = groups == group
        x = values[mask]
        w = weights[mask]
        valid = ~np.isnan(x)
        if valid.sum() == 0:
            continue
        xv = x[valid]
        wv = w[valid]
        mean = np.average(xv, weights=wv)
        y = np.full(x.shape, np.nan, dtype=float)
        y[valid] = xv - mean
        out[mask] = y
    return out

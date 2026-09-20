"""Reject corrupt or incomplete verification inputs before numerical replay."""
import numpy as np


def finite_values(values):
    if not np.isfinite(np.asarray(values, dtype=float)).all():
        raise ValueError("Nonfinite verification values")


def exact_models(frame, keys, expected, numeric):
    observed = list(frame[keys].itertuples(index=False, name=None))
    if len(observed) != len(set(observed)) or set(observed) != set(expected):
        raise ValueError("Incomplete, duplicated or unexpected model coverage")
    finite_values(frame[numeric])

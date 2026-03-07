#!/usr/bin/env python3
"""Shared TIMSS/TIMSS Advanced helpers."""

from __future__ import annotations

import math
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import numpy as np
import pandas as pd
import pyreadstat


ROOT = Path(__file__).resolve().parent

SEX_FEMALE = 1.0
SEX_MALE = 2.0
MIN_N_PER_SEX = 30
JK_SUM_MULTIPLIER = 0.5


def member_country_code(member: str) -> str:
    stem = Path(member).stem.upper()
    return stem[3:6]


def load_sav_from_zip(zip_path: Path, member: str, usecols: list[str]) -> pd.DataFrame:
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with ZipFile(zip_path) as archive:
            archive.extract(member, temp_path)
        frame, _ = pyreadstat.read_sav(
            temp_path / member,
            usecols=usecols,
            apply_value_formats=False,
        )
    return frame


def coerce_numeric(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for column in out.columns:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def weighted_effect(
    values: np.ndarray,
    weights: np.ndarray,
    sex: np.ndarray,
) -> tuple[float, int, int] | None:
    female_mask = sex == SEX_FEMALE
    male_mask = sex == SEX_MALE
    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0) & (female_mask | male_mask)
    if not valid.any():
        return None
    female = valid & female_mask
    male = valid & male_mask
    n_female = int(female.sum())
    n_male = int(male.sum())
    if n_female < MIN_N_PER_SEX or n_male < MIN_N_PER_SEX:
        return None

    female_values = values[female]
    male_values = values[male]
    female_weights = weights[female]
    male_weights = weights[male]
    mu_f = np.average(female_values, weights=female_weights)
    mu_m = np.average(male_values, weights=male_weights)
    var_f = np.average((female_values - mu_f) ** 2, weights=female_weights)
    var_m = np.average((male_values - mu_m) ** 2, weights=male_weights)
    pooled = (
        female_weights.sum() * var_f + male_weights.sum() * var_m
    ) / (female_weights.sum() + male_weights.sum())
    if pooled <= 0:
        return None
    d = (mu_f - mu_m) / math.sqrt(pooled)
    return float(d), n_female, n_male


def jackknife_effect(
    values: np.ndarray,
    weights: np.ndarray,
    sex: np.ndarray,
    jkzone: np.ndarray,
    jkrep: np.ndarray,
) -> tuple[float, float, int, int] | None:
    full = weighted_effect(values, weights, sex)
    if full is None:
        return None
    point, n_female, n_male = full
    zones = sorted({int(z) for z in jkzone[np.isfinite(jkzone)]})
    replicate_estimates: list[float] = []
    for zone in zones:
        zone_mask = jkzone == zone
        rep_a = weights.copy()
        rep_a[zone_mask & (jkrep == 0)] = 0.0
        rep_a[zone_mask & (jkrep == 1)] = 2.0 * rep_a[zone_mask & (jkrep == 1)]
        est_a = weighted_effect(values, rep_a, sex)
        if est_a is None:
            return None
        replicate_estimates.append(est_a[0])

        rep_b = weights.copy()
        rep_b[zone_mask & (jkrep == 0)] = 2.0 * rep_b[zone_mask & (jkrep == 0)]
        rep_b[zone_mask & (jkrep == 1)] = 0.0
        est_b = weighted_effect(values, rep_b, sex)
        if est_b is None:
            return None
        replicate_estimates.append(est_b[0])

    sampling_var = JK_SUM_MULTIPLIER * float(
        np.sum((np.asarray(replicate_estimates, dtype=float) - point) ** 2)
    )
    return point, sampling_var, n_female, n_male


def plausible_value_summary(
    frame: pd.DataFrame,
    pv_columns: list[str],
) -> dict[str, float | int] | None:
    estimates: list[float] = []
    sampling_vars: list[float] = []
    n_female = n_male = 0
    sex = frame["ITSEX"].to_numpy(dtype=float)
    weights = frame["TOTWGT"].to_numpy(dtype=float)
    jkzone = frame["JKZONE"].to_numpy(dtype=float)
    jkrep = frame["JKREP"].to_numpy(dtype=float)

    for index, pv_col in enumerate(pv_columns):
        if pv_col not in frame.columns:
            continue
        values = frame[pv_col].to_numpy(dtype=float)
        result = jackknife_effect(values, weights, sex, jkzone, jkrep)
        if result is None:
            continue
        point, sampling_var, nf, nm = result
        if index == 0:
            n_female, n_male = nf, nm
        estimates.append(point)
        sampling_vars.append(sampling_var)

    if len(estimates) < 2:
        return None

    point = float(np.mean(estimates))
    sampling_var = float(np.mean(sampling_vars))
    imputation_var = float((1.0 + 1.0 / len(estimates)) * np.var(estimates, ddof=1))
    total_var = sampling_var + imputation_var
    se = math.sqrt(total_var)
    return {
        "point_estimate_d": point,
        "se_d": se,
        "ci_low": point - 1.96 * se,
        "ci_high": point + 1.96 * se,
        "sampling_var": sampling_var,
        "imputation_var": imputation_var,
        "total_var": total_var,
        "n_female": n_female,
        "n_male": n_male,
        "n_pvs_used": len(estimates),
        "n_jk_replicates": int(2 * len({int(z) for z in jkzone[np.isfinite(jkzone)]})),
    }

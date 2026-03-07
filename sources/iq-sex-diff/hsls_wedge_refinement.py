#!/usr/bin/env python3
"""HSLS refinement pass adding pre-follow-up behavior/identity and teacher-climate blocks."""

from __future__ import annotations

import io
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf


DATA_DIR = Path(__file__).resolve().parent / "data" / "hsls"
ZIP_PATH = DATA_DIR / "HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip"
SAV_MEMBER = "hsls_17_student_pets_sr_v1_0.sav"

USECOLS = [
    "X1SEX",
    "X1TXMTSCOR",
    "X2TXMTSCOR",
    "X3TCOVERAGE",
    "X3THIMATH",
    "X3TGPAMAT",
    "X3TGPAHIMTH",
    "W3W1W2STUTR",
    "S1NOHWDN",
    "S1HRMHOMEWK",
    "X1MTHEFF",
    "X1SCHOOLBEL",
    "S1MTEACHER",
    "S1MTCHFAIR",
    "S1MTCHTREAT",
    "S1MTCHMFDIFF",
    "S1MTCHCONF",
    "S1MTCHINTRST",
    "S1MTCHEASY",
]

OUT_EXTRACT = DATA_DIR / "hsls_wedge_refinement_extract.parquet"
OUT_GAPS = DATA_DIR / "hsls_wedge_refinement_gaps.tsv"
OUT_MODELS = DATA_DIR / "hsls_wedge_refinement_models.tsv"


def weighted_mean(x: pd.Series, w: pd.Series) -> float:
    return float(np.average(x, weights=w))


def weighted_var(x: pd.Series, w: pd.Series) -> float:
    mean = weighted_mean(x, w)
    return float(np.average((x - mean) ** 2, weights=w))


def weighted_standardize(x: pd.Series, w: pd.Series) -> pd.Series:
    valid = x.notna() & w.gt(0)
    if valid.sum() < 50:
        return pd.Series(np.nan, index=x.index)
    mean = weighted_mean(x.loc[valid], w.loc[valid])
    var = weighted_var(x.loc[valid], w.loc[valid])
    if not math.isfinite(var) or var <= 0:
        return pd.Series(np.nan, index=x.index)
    return (x - mean) / math.sqrt(var)


def recode_missing(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in USECOLS:
        if col == "X1SEX":
            out.loc[~out[col].isin([1, 2]), col] = np.nan
        elif col in {"S1NOHWDN"}:
            out.loc[~out[col].isin([1, 2, 3, 4]), col] = np.nan
        elif col in {"S1HRMHOMEWK"}:
            out.loc[~out[col].isin([1, 2, 3, 4, 5, 6]), col] = np.nan
        elif col in {"S1MTEACHER"}:
            out.loc[~out[col].isin([0, 1]), col] = np.nan
        elif col in {"S1MTCHFAIR", "S1MTCHTREAT", "S1MTCHMFDIFF", "S1MTCHCONF", "S1MTCHINTRST", "S1MTCHEASY"}:
            out.loc[~out[col].isin([1, 2, 3, 4]), col] = np.nan
        else:
            out.loc[out[col] < 0, col] = np.nan
    return out


def load_hsls() -> pd.DataFrame:
    with zipfile.ZipFile(ZIP_PATH) as zf:
        data = io.BytesIO(zf.read(SAV_MEMBER))
    df, _ = pyreadstat.read_sav(data, usecols=USECOLS)
    return recode_missing(df)


def build_extract(df: pd.DataFrame) -> pd.DataFrame:
    core = df[df["X1SEX"].isin([1, 2])].copy()
    core["female"] = (core["X1SEX"] == 2).astype(int)
    core["w"] = core["W3W1W2STUTR"]
    core = core[(core["w"] > 0) & (core["X3TCOVERAGE"] == 1)].copy()
    core["precalc_plus"] = core["X3THIMATH"].isin([10, 11, 12, 13]).astype(float).where(core["X3THIMATH"].notna())

    for col in ["X1TXMTSCOR", "X2TXMTSCOR", "X3TGPAMAT", "X3TGPAHIMTH", "X1MTHEFF", "X1SCHOOLBEL", "S1HRMHOMEWK"]:
        core[f"{col}_z"] = weighted_standardize(core[col], core["w"])

    core["S1NOHWDN_pos"] = 5 - core["S1NOHWDN"]
    core["S1MTEACHER_pos"] = core["S1MTEACHER"]
    for col in ["S1NOHWDN_pos", "S1MTEACHER_pos"]:
        core[f"{col}_z"] = weighted_standardize(core[col], core["w"])

    for col in ["S1MTCHFAIR", "S1MTCHCONF", "S1MTCHINTRST", "S1MTCHEASY"]:
        core[f"{col}_pos"] = 5 - core[col]
        core[f"{col}_pos_z"] = weighted_standardize(core[f"{col}_pos"], core["w"])
    for col in ["S1MTCHTREAT", "S1MTCHMFDIFF"]:
        core[f"{col}_pos"] = core[col]
        core[f"{col}_pos_z"] = weighted_standardize(core[f"{col}_pos"], core["w"])

    behavior_stack = pd.concat(
        [
            core["X1MTHEFF_z"],
            core["X1SCHOOLBEL_z"],
            core["S1NOHWDN_pos_z"],
            core["S1HRMHOMEWK_z"],
            core["S1MTEACHER_pos_z"],
        ],
        axis=1,
    )
    climate_stack = pd.concat(
        [
            core["S1MTCHFAIR_pos_z"],
            core["S1MTCHCONF_pos_z"],
            core["S1MTCHINTRST_pos_z"],
            core["S1MTCHEASY_pos_z"],
            core["S1MTCHTREAT_pos_z"],
            core["S1MTCHMFDIFF_pos_z"],
        ],
        axis=1,
    )
    core["base_behavior_identity_index_z"] = behavior_stack.mean(axis=1, skipna=True).where(
        behavior_stack.notna().sum(axis=1) >= 4
    )
    core["teacher_climate_index_z"] = climate_stack.mean(axis=1, skipna=True).where(
        climate_stack.notna().sum(axis=1) >= 4
    )
    return core


def fit_gap(core: pd.DataFrame, outcome: str) -> dict[str, float | int | str]:
    sample = core[[outcome, "female", "w"]].dropna().copy()
    fit = smf.wls(f"{outcome} ~ female", data=sample, weights=sample["w"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "outcome": outcome,
        "n": int(fit.nobs),
        "beta_female": float(fit.params["female"]),
        "se_female": float(fit.bse["female"]),
        "ci95_low": float(low),
        "ci95_high": float(high),
        "r_squared": float(getattr(fit, "rsquared", np.nan)),
    }


def build_gap_table(core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for outcome in ["base_behavior_identity_index_z", "teacher_climate_index_z"]:
        rows.append(fit_gap(core, outcome))
    return pd.DataFrame(rows)


def fit_model(sample: pd.DataFrame, formula: str) -> dict[str, float | int | str]:
    fit = smf.wls(formula, data=sample, weights=sample["w"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "formula": formula,
        "n": int(fit.nobs),
        "beta_female": float(fit.params["female"]),
        "se_female": float(fit.bse["female"]),
        "ci95_low": float(low),
        "ci95_high": float(high),
        "r_squared": float(getattr(fit, "rsquared", np.nan)),
    }


def build_model_table(core: pd.DataFrame) -> pd.DataFrame:
    specs = [
        {
            "name": "x2_mechanism",
            "outcome": "X2TXMTSCOR_z",
            "base": "X2TXMTSCOR_z ~ female",
            "adjusted": "X2TXMTSCOR_z ~ female + X1TXMTSCOR_z + base_behavior_identity_index_z + teacher_climate_index_z",
        },
        {
            "name": "gpa_mechanism",
            "outcome": "X3TGPAMAT_z",
            "base": "X3TGPAMAT_z ~ female",
            "adjusted": "X3TGPAMAT_z ~ female + X1TXMTSCOR_z + X2TXMTSCOR_z + base_behavior_identity_index_z + teacher_climate_index_z",
        },
        {
            "name": "high_gpa_mechanism",
            "outcome": "X3TGPAHIMTH_z",
            "base": "X3TGPAHIMTH_z ~ female",
            "adjusted": "X3TGPAHIMTH_z ~ female + X1TXMTSCOR_z + X2TXMTSCOR_z + base_behavior_identity_index_z + teacher_climate_index_z",
        },
        {
            "name": "precalc_mechanism",
            "outcome": "precalc_plus",
            "base": "precalc_plus ~ female",
            "adjusted": "precalc_plus ~ female + X1TXMTSCOR_z + base_behavior_identity_index_z + teacher_climate_index_z",
        },
    ]
    rows = []
    for spec in specs:
        adjusted_terms = [term.strip() for term in spec["adjusted"].split("~", 1)[1].split("+")]
        sample = core[[spec["outcome"], "w"] + adjusted_terms].dropna().copy()
        if len(sample) < 300:
            continue
        base = fit_model(sample, spec["base"])
        base.update({"model": spec["name"], "stage": "same_sample_base", "outcome": spec["outcome"]})
        rows.append(base)
        adj = fit_model(sample, spec["adjusted"])
        adj.update({"model": spec["name"], "stage": "adjusted", "outcome": spec["outcome"]})
        rows.append(adj)
    return pd.DataFrame(rows)


def write_outputs(core: pd.DataFrame, gaps: pd.DataFrame, models: pd.DataFrame) -> None:
    core.to_parquet(OUT_EXTRACT, index=False)
    gaps.to_csv(OUT_GAPS, sep="\t", index=False)
    models.to_csv(OUT_MODELS, sep="\t", index=False)


def main() -> None:
    raw = load_hsls()
    core = build_extract(raw)
    gaps = build_gap_table(core)
    models = build_model_table(core)
    write_outputs(core, gaps, models)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""First-pass NELS late-school wedge replication using public-use surfaces."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nels"
SAV_PATH = DATA_DIR / "nels_88_00_byf4stu_v1_0.SAV"

USECOLS = [
    "SEX",
    "F4TRSCWT",
    "F4QWT",
    "BY2XMSTD",
    "BY2XRSTD",
    "F12XMSTD",
    "F22XMSTD",
    "F2RHMA_C",
    "F2RTRPRG",
    "F2RTROUT",
    "F2S29E",
    "F1T1_14",
    "F1S39A",
    "F1S7H",
    "F1S7I",
    "F1S40C",
    "F1S36A2",
    "F1S36B2",
    "F1S38",
]

BINARY_OUTCOMES = {
    "recognized_good_grades",
    "academic_honors_rec",
    "academic_or_rigorous_program",
    "rigorous_academic_program",
}

OUT_EXTRACT = DATA_DIR / "nels_wedge_extract.parquet"
OUT_GAPS = DATA_DIR / "nels_wedge_overall.tsv"
OUT_PROGRAM = DATA_DIR / "nels_wedge_by_program.tsv"
OUT_MODELS = DATA_DIR / "nels_wedge_models.tsv"
OUT_BEHAVIOR_DATA = DATA_DIR / "nels_behavior_f2math_model_data.csv"


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: pd.Series, weights: pd.Series) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_standardize(values: pd.Series, weights: pd.Series) -> pd.Series:
    valid = values.notna() & weights.gt(0)
    if valid.sum() < 50:
        return pd.Series(np.nan, index=values.index)
    mean = weighted_mean(values.loc[valid], weights.loc[valid])
    var = weighted_var(values.loc[valid], weights.loc[valid])
    if not math.isfinite(var) or var <= 0:
        return pd.Series(np.nan, index=values.index)
    return (values - mean) / math.sqrt(var)


def weighted_gap(sub: pd.DataFrame, column: str) -> dict[str, float | int | str]:
    female = sub[sub["female"] == 1]
    male = sub[sub["female"] == 0]
    female_mean = weighted_mean(female[column], female["w"])
    male_mean = weighted_mean(male[column], male["w"])
    row: dict[str, float | int | str] = {
        "metric": column,
        "n": int(len(sub)),
        "weighted_n": float(sub["w"].sum()),
        "female_mean": female_mean,
        "male_mean": male_mean,
        "female_minus_male": female_mean - male_mean,
    }
    if column not in BINARY_OUTCOMES:
        female_var = weighted_var(female[column], female["w"])
        male_var = weighted_var(male[column], male["w"])
        pooled = math.sqrt((female_var + male_var) / 2.0)
        row["weighted_d_female_minus_male"] = (female_mean - male_mean) / pooled if pooled > 0 else math.nan
    return row


def recode_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in USECOLS:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out.loc[~out["SEX"].isin([1, 2]), "SEX"] = np.nan
    for col in ["F4TRSCWT", "F4QWT"]:
        out.loc[out[col] < 0, col] = np.nan

    for col in ["BY2XMSTD", "BY2XRSTD", "F12XMSTD", "F22XMSTD"]:
        out.loc[(out[col] < 0) | (out[col] > 90), col] = np.nan
    out.loc[(out["F2RHMA_C"] < 0) | (out["F2RHMA_C"] >= 9.9), "F2RHMA_C"] = np.nan

    out.loc[~out["F2RTRPRG"].isin([1, 2, 3, 4, 5, 6]), "F2RTRPRG"] = np.nan
    out.loc[~out["F2RTROUT"].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]), "F2RTROUT"] = np.nan
    out.loc[~out["F2S29E"].isin([1, 2]), "F2S29E"] = np.nan
    out.loc[~out["F1T1_14"].isin([2, 3]), "F1T1_14"] = np.nan
    out.loc[~out["F1S39A"].isin([2, 3, 4, 5, 6, 7, 8, 9]), "F1S39A"] = np.nan
    out.loc[~out["F1S7H"].isin([1, 2, 3, 4]), "F1S7H"] = np.nan
    out.loc[~out["F1S7I"].isin([1, 2, 3, 4]), "F1S7I"] = np.nan
    out.loc[~out["F1S40C"].isin([1, 2, 3, 4]), "F1S40C"] = np.nan
    out.loc[~out["F1S36A2"].isin([0, 1, 2, 3, 4, 5, 6, 7]), "F1S36A2"] = np.nan
    out.loc[~out["F1S36B2"].isin([0, 1, 2, 3, 4, 5, 6, 7]), "F1S36B2"] = np.nan
    out.loc[~out["F1S38"].isin([1, 2, 3, 4]), "F1S38"] = np.nan
    return out


def load_nels() -> tuple[pd.DataFrame, dict[int, str]]:
    df, meta = pyreadstat.read_sav(SAV_PATH, usecols=USECOLS)
    df = recode_frame(df)
    labelset = meta.variable_to_label["F2RTRPRG"]
    program_labels = {
        int(code): label for code, label in meta.value_labels[labelset].items() if 1 <= int(code) <= 6
    }
    return df, program_labels


def build_extract(df: pd.DataFrame, program_labels: dict[int, str]) -> pd.DataFrame:
    core = df[df["SEX"].isin([1, 2])].copy()
    core["female"] = (core["SEX"] == 2).astype(int)
    core["w"] = core["F4TRSCWT"]
    core = core[core["w"] > 0].copy()

    core["program_label"] = core["F2RTRPRG"].astype("Int64").map(program_labels)
    core["recognized_good_grades"] = (core["F2S29E"] == 1).astype(float).where(core["F2S29E"].notna())
    core["academic_honors_rec"] = (core["F1T1_14"] == 2).astype(float).where(core["F1T1_14"].notna())
    core["math_grade_quality"] = (10 - core["F1S39A"]).where(core["F1S39A"].notna())
    core["academic_or_rigorous_program"] = core["F2RTRPRG"].isin([1, 2]).astype(float).where(core["F2RTRPRG"].notna())
    core["rigorous_academic_program"] = core["F2RTRPRG"].eq(1).astype(float).where(core["F2RTRPRG"].notna())
    core["teacher_interest_pos"] = (5 - core["F1S7H"]).where(core["F1S7H"].notna())
    core["teacher_praise_pos"] = (5 - core["F1S7I"]).where(core["F1S7I"].notna())
    core["homework_done_pos"] = core["F1S40C"].where(core["F1S40C"].notna())
    core["homework_hours_num"] = core["F1S36A2"].where(core["F1S36A2"].notna())
    core["math_homework_hours_num"] = core["F1S36B2"].where(core["F1S36B2"].notna())
    core["importance_grades_pos"] = core["F1S38"].where(core["F1S38"].notna())

    z_cols = [
        "BY2XMSTD",
        "BY2XRSTD",
        "F12XMSTD",
        "F22XMSTD",
        "F2RHMA_C",
        "math_grade_quality",
        "teacher_interest_pos",
        "teacher_praise_pos",
        "homework_done_pos",
        "homework_hours_num",
        "math_homework_hours_num",
        "importance_grades_pos",
    ]
    for col in z_cols:
        core[f"{col}_z"] = weighted_standardize(core[col], core["w"])

    behavior_stack = pd.concat(
        [
            core["teacher_interest_pos_z"],
            core["teacher_praise_pos_z"],
            core["homework_done_pos_z"],
            core["homework_hours_num_z"],
            core["math_homework_hours_num_z"],
            core["importance_grades_pos_z"],
        ],
        axis=1,
    )
    core["behavior_index_z"] = behavior_stack.mean(axis=1, skipna=True).where(behavior_stack.notna().sum(axis=1) >= 4)
    return core


def build_overall_table(core: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "BY2XMSTD",
        "F12XMSTD",
        "F22XMSTD",
        "F2RHMA_C",
        "math_grade_quality",
        "recognized_good_grades",
        "academic_honors_rec",
        "academic_or_rigorous_program",
        "rigorous_academic_program",
        "behavior_index_z",
    ]
    rows = []
    for metric in metrics:
        sub = core[core[metric].notna()].copy()
        if len(sub) < 100:
            continue
        rows.append(weighted_gap(sub, metric))
    return pd.DataFrame(rows)


def build_program_table(core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for level, sub in core.groupby("F2RTRPRG", sort=True):
        valid = sub[sub["F22XMSTD"].notna()].copy()
        if len(valid) < 100:
            continue
        gap = weighted_gap(valid, "F22XMSTD")
        rows.append(
            {
                "program_code": int(level),
                "program_label": valid["program_label"].iloc[0],
                **gap,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values("program_code").reset_index(drop=True)


def fit_wls(sample: pd.DataFrame, formula: str) -> dict[str, float | int | str]:
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
            "name": "f12_math_anchor",
            "outcome": "F12XMSTD_z",
            "base": "F12XMSTD_z ~ female",
            "adjusted": "F12XMSTD_z ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "f22_math_anchor",
            "outcome": "F22XMSTD_z",
            "base": "F22XMSTD_z ~ female",
            "adjusted": "F22XMSTD_z ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "transcript_math_units",
            "outcome": "F2RHMA_C_z",
            "base": "F2RHMA_C_z ~ female",
            "adjusted": "F2RHMA_C_z ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "math_grade_quality",
            "outcome": "math_grade_quality_z",
            "base": "math_grade_quality_z ~ female",
            "adjusted": "math_grade_quality_z ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "recognized_good_grades",
            "outcome": "recognized_good_grades",
            "base": "recognized_good_grades ~ female",
            "adjusted": "recognized_good_grades ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "academic_honors_rec",
            "outcome": "academic_honors_rec",
            "base": "academic_honors_rec ~ female",
            "adjusted": "academic_honors_rec ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "academic_or_rigorous_program",
            "outcome": "academic_or_rigorous_program",
            "base": "academic_or_rigorous_program ~ female",
            "adjusted": "academic_or_rigorous_program ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
        {
            "name": "rigorous_academic_program",
            "outcome": "rigorous_academic_program",
            "base": "rigorous_academic_program ~ female",
            "adjusted": "rigorous_academic_program ~ female + BY2XMSTD_z + BY2XRSTD_z",
        },
    ]
    rows = []
    for spec in specs:
        terms = [term.strip() for term in spec["adjusted"].split("~", 1)[1].split("+")]
        sample = core[[spec["outcome"], "w"] + terms].dropna().copy()
        if len(sample) < 300:
            continue
        base = fit_wls(sample, spec["base"])
        base.update({"model": spec["name"], "stage": "same_sample_base", "outcome": spec["outcome"]})
        rows.append(base)
        adj = fit_wls(sample, spec["adjusted"])
        adj.update({"model": spec["name"], "stage": "adjusted_anchor", "outcome": spec["outcome"]})
        rows.append(adj)
    return pd.DataFrame(rows)


def write_outputs(core: pd.DataFrame, gaps: pd.DataFrame, program: pd.DataFrame, models: pd.DataFrame) -> None:
    core.to_parquet(OUT_EXTRACT, index=False)
    gaps.to_csv(OUT_GAPS, sep="\t", index=False)
    program.to_csv(OUT_PROGRAM, sep="\t", index=False)
    models.to_csv(OUT_MODELS, sep="\t", index=False)
    export_cols = [
        "F22XMSTD_z",
        "behavior_index_z",
        "female",
        "BY2XMSTD_z",
        "BY2XRSTD_z",
    ]
    core.loc[:, export_cols].to_csv(OUT_BEHAVIOR_DATA, index=False)


def main() -> None:
    raw, program_labels = load_nels()
    core = build_extract(raw, program_labels)
    gaps = build_overall_table(core)
    program = build_program_table(core)
    models = build_model_table(core)
    write_outputs(core, gaps, program, models)


if __name__ == "__main__":
    main()

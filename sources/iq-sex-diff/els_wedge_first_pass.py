#!/usr/bin/env python3
"""First-pass ELS late-school wedge replication using public-use surfaces."""

from __future__ import annotations

import io
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "els"
ZIP_PATH = DATA_DIR / "ELS_2002-12_PETS_v1_0_Student_SPSS_Datasets.zip"
SAV_MEMBER = "els_02_12_byf3pststu_v1_0.sav"
SAV_PATH = DATA_DIR / SAV_MEMBER

USECOLS = [
    "STU_ID",
    "BYSEX",
    "BYSTUWT",
    "F1QWT",
    "F1TRSCWT",
    "F1RTRFLG",
    "BYTXMSTD",
    "BYTXRSTD",
    "F1TXMSTD",
    "F1HIMATH",
    "BYMATHSE",
    "F1MATHSE",
    "BYACTCTL",
    "BYHMWRK",
    "BYSCSAF2",
    "BYS24C",
    "BYS24F",
    "BYP77O",
    "BYS23C",
    "BYS37",
    "BYTM19",
    "F1RHTUNP",
]

RAW_CONTINUOUS = {
    "BYTXMSTD",
    "BYTXRSTD",
    "F1TXMSTD",
    "BYMATHSE",
    "F1MATHSE",
    "BYACTCTL",
    "BYSCSAF2",
    "F1RHTUNP",
}

BINARY_OUTCOMES = {"recognized_good_grades", "algebra2_plus", "trig_precalc_calc"}
LADDER_MIN_N = 100

OUT_EXTRACT = DATA_DIR / "els_wedge_extract.parquet"
OUT_GAPS = DATA_DIR / "els_wedge_overall.tsv"
OUT_LADDER = DATA_DIR / "els_wedge_by_ladder.tsv"
OUT_MODELS = DATA_DIR / "els_wedge_models.tsv"
OUT_BEHAVIOR_DATA = DATA_DIR / "els_behavior_math_model_data.csv"


def ensure_sav() -> None:
    if SAV_PATH.exists():
        return
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(DATA_DIR)


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
        if col == "STU_ID":
            continue
        out[col] = pd.to_numeric(out[col], errors="coerce")
        if col == "BYSEX":
            out.loc[~out[col].isin([1, 2]), col] = np.nan
        elif col == "F1RTRFLG":
            out.loc[out[col] < 0, col] = np.nan
        elif col == "F1HIMATH":
            out.loc[~out[col].isin([1, 2, 3, 4, 5, 6]), col] = np.nan
        elif col in {"BYS23C", "BYTM19"}:
            out.loc[~out[col].isin([0, 1]), col] = np.nan
        elif col in {"BYS24C", "BYS24F"}:
            out.loc[~out[col].isin([1, 2, 3, 4, 5]), col] = np.nan
        elif col in {"BYP77O", "BYS37"}:
            out.loc[~out[col].isin([1, 2, 3, 4]), col] = np.nan
        elif col == "BYHMWRK":
            out.loc[out[col] < 0, col] = np.nan
            out[col] = out[col].replace({97: 26.0, 98: 21.0, 99: 47.0})
        elif col in RAW_CONTINUOUS:
            out.loc[out[col] < 0, col] = np.nan
    return out


def load_els() -> tuple[pd.DataFrame, dict[int, str]]:
    ensure_sav()
    with SAV_PATH.open("rb") as handle:
        df, meta = pyreadstat.read_sav(io.BytesIO(handle.read()), usecols=USECOLS)
    df = recode_frame(df)
    labelset = meta.variable_to_label["F1HIMATH"]
    ladder_labels = {
        int(code): label
        for code, label in meta.value_labels[labelset].items()
        if int(code) > 0
    }
    return df, ladder_labels


def build_extract(df: pd.DataFrame, ladder_labels: dict[int, str]) -> pd.DataFrame:
    core = df[df["BYSEX"].isin([1, 2])].copy()
    core["female"] = (core["BYSEX"] == 2).astype(int)
    core["sex_label"] = core["female"].map({0: "male", 1: "female"})
    core["w"] = core["F1TRSCWT"]
    core["w_by"] = core["BYSTUWT"]
    core = core[(core["w"] > 0) & core["F1RTRFLG"].ge(1)].copy()
    core["highest_math_label"] = core["F1HIMATH"].astype("Int64").map(ladder_labels)
    core["algebra2_plus"] = core["F1HIMATH"].ge(5).astype(float).where(core["F1HIMATH"].notna())
    core["trig_precalc_calc"] = core["F1HIMATH"].eq(6).astype(float).where(core["F1HIMATH"].notna())
    core["recognized_good_grades"] = core["BYS23C"]
    core["math_teacher_honors_rec"] = core["BYTM19"]
    core["importance_good_grades"] = core["BYS37"]
    core["discipline_ok"] = (5 - core["BYP77O"]).where(core["BYP77O"].notna())
    core["absent_num"] = core["BYS24C"].map({1: 0.0, 2: 1.5, 3: 4.5, 4: 8.0, 5: 10.0})
    core["suspend_num"] = core["BYS24F"].map({1: 0.0, 2: 1.5, 3: 4.5, 4: 8.0, 5: 10.0})
    core["log_homework"] = np.log1p(core["BYHMWRK"])

    z_cols = [
        "BYTXMSTD",
        "BYTXRSTD",
        "F1TXMSTD",
        "BYMATHSE",
        "F1MATHSE",
        "BYACTCTL",
        "BYSCSAF2",
        "discipline_ok",
        "absent_num",
        "suspend_num",
        "log_homework",
        "F1RHTUNP",
    ]
    for col in z_cols:
        core[f"{col}_z"] = weighted_standardize(core[col], core["w"])

    behavior_stack = pd.concat(
        [
            core["BYACTCTL_z"],
            core["BYSCSAF2_z"],
            core["discipline_ok_z"],
            core["log_homework_z"],
            -core["absent_num_z"],
            -core["suspend_num_z"],
        ],
        axis=1,
    )
    behavior_count = behavior_stack.notna().sum(axis=1)
    core["behavior_index_z"] = behavior_stack.mean(axis=1, skipna=True).where(behavior_count >= 4)

    return core


def build_overall_table(core: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "BYTXMSTD",
        "F1TXMSTD",
        "BYMATHSE",
        "F1MATHSE",
        "behavior_index_z",
        "recognized_good_grades",
        "algebra2_plus",
        "trig_precalc_calc",
    ]
    rows = []
    for metric in metrics:
        sub = core[core[metric].notna()].copy()
        if len(sub) < 100:
            continue
        rows.append(weighted_gap(sub, metric))
    return pd.DataFrame(rows)


def build_ladder_table(core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for level, sub in core.groupby("F1HIMATH", sort=True):
        if len(sub) < LADDER_MIN_N:
            continue
        valid = sub[sub["F1TXMSTD"].notna()].copy()
        if len(valid) < LADDER_MIN_N:
            continue
        gap = weighted_gap(valid, "F1TXMSTD")
        rows.append(
            {
                "highest_math_level": int(level),
                "highest_math_label": valid["highest_math_label"].iloc[0],
                **gap,
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values("highest_math_level").reset_index(drop=True)


def fit_wls(sample: pd.DataFrame, formula: str, weight_col: str) -> dict[str, float | int | str]:
    fit = smf.wls(formula, data=sample, weights=sample[weight_col]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "formula": formula,
        "n": int(fit.nobs),
        "weight_col": weight_col,
        "beta_female": float(fit.params["female"]),
        "se_female": float(fit.bse["female"]),
        "ci95_low": float(low),
        "ci95_high": float(high),
        "r_squared": float(getattr(fit, "rsquared", np.nan)),
    }


def build_model_table(core: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    specs = [
        {
            "name": "f1math_by_anchor_behavior",
            "outcome": "F1TXMSTD_z",
            "formula": "F1TXMSTD_z ~ female + BYTXMSTD_z + BYTXRSTD_z + behavior_index_z",
        },
        {
            "name": "algebra2_plus_by_anchor_behavior",
            "outcome": "algebra2_plus",
            "formula": "algebra2_plus ~ female + BYTXMSTD_z + BYTXRSTD_z + behavior_index_z",
        },
        {
            "name": "trig_precalc_calc_by_anchor_behavior",
            "outcome": "trig_precalc_calc",
            "formula": "trig_precalc_calc ~ female + BYTXMSTD_z + BYTXRSTD_z + behavior_index_z",
        },
        {
            "name": "f1mathse_by_anchor_behavior",
            "outcome": "F1MATHSE_z",
            "formula": "F1MATHSE_z ~ female + BYTXMSTD_z + BYTXRSTD_z + BYMATHSE_z + behavior_index_z",
        },
        {
            "name": "recognized_by_anchor_effort",
            "outcome": "recognized_good_grades",
            "formula": "recognized_good_grades ~ female + BYTXMSTD_z + BYTXRSTD_z + BYACTCTL_z",
            "weight_col": "w",
        },
        {
            "name": "math_teacher_honors_rec_by_anchor_effort",
            "outcome": "math_teacher_honors_rec",
            "formula": "math_teacher_honors_rec ~ female + BYTXMSTD_z + BYTXRSTD_z + BYACTCTL_z",
            "weight_col": "w_by",
        },
    ]

    rows = []
    behavior_export = None
    for spec in specs:
        outcome = spec["outcome"]
        weight_col = spec.get("weight_col", "w")
        terms = [term.strip() for term in spec["formula"].split("~", 1)[1].split("+")]
        sample = core[[outcome, weight_col] + terms].dropna().copy()
        sample = sample[sample[weight_col] > 0].copy()
        if len(sample) < 300:
            continue
        base_formula = f"{outcome} ~ female"
        base_row = fit_wls(sample, base_formula, weight_col)
        base_row.update({"model": spec["name"], "stage": "same_sample_base", "outcome": outcome})
        rows.append(base_row)

        full_row = fit_wls(sample, spec["formula"], weight_col)
        full_row.update({"model": spec["name"], "stage": "adjusted", "outcome": outcome})
        rows.append(full_row)

        if spec["name"] == "f1math_by_anchor_behavior":
            behavior_export = sample.rename(columns={"female": "Female"})

    return pd.DataFrame(rows), behavior_export


def write_outputs(
    core: pd.DataFrame,
    overall: pd.DataFrame,
    ladder: pd.DataFrame,
    models: pd.DataFrame,
    behavior_export: pd.DataFrame | None,
) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    core.to_parquet(OUT_EXTRACT, index=False)
    overall.to_csv(OUT_GAPS, sep="\t", index=False)
    ladder.to_csv(OUT_LADDER, sep="\t", index=False)
    models.to_csv(OUT_MODELS, sep="\t", index=False)
    if behavior_export is not None:
        behavior_export.to_csv(OUT_BEHAVIOR_DATA, index=False)


def main() -> None:
    df, ladder_labels = load_els()
    core = build_extract(df, ladder_labels)
    overall = build_overall_table(core)
    ladder = build_ladder_table(core)
    models, behavior_export = build_model_table(core)
    write_outputs(core, overall, ladder, models, behavior_export)


if __name__ == "__main__":
    main()

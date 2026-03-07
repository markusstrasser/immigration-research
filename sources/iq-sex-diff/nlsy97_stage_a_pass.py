#!/usr/bin/env python3
"""Stage A NLSY97 pass: process, precision, and school-exposure audit."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from nlsy97_stats_pipeline import fit_weighted_gap, load_frame, pooled_weighted_sd, standardize_scores
from stage0_config import NLSY97


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"

PROCESS_CATEGORICAL = [
    "computer_use",
    "computer_test",
    "effort",
    "room_comfort",
    "room_quiet",
]

PROCESS_EXTRA_CATEGORICAL = ["prev_taken"]

PROCESS_CONTINUOUS = [
    "numerical_operations_items_complete",
    "coding_speed_items_complete",
    "arithmetic_reasoning_post_variance",
    "math_knowledge_post_variance",
]

SCHOOL_CATEGORICAL = [
    "avg_grade_recent",
    "science_experiment",
    "science_equipment",
    "shop_attention",
]

SCHOOL_EXTRA_CATEGORICAL = [
    "grade_fall_1997",
]

TARGET_SCORES = [
    "arithmetic_reasoning_z",
    "math_knowledge_z",
    "quantitative_z",
    "quantitative_plus_numerical_operations_z",
    "numerical_operations_z",
    "math_verbal_percentile_z",
    "clerical_speed_z",
    "verbal_z",
    "mechanical_z",
]


def add_quantitative_stress_surface(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    female_mask = frame["sex"].eq(NLSY97["sex"]["female"])
    valid_base = frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]]) & frame["weight_1997"].gt(0)

    raw_name = "quantitative_plus_numerical_operations_raw"
    z_name = "quantitative_plus_numerical_operations_z"
    frame[raw_name] = frame[
        ["arithmetic_reasoning", "math_knowledge", "numerical_operations"]
    ].mean(axis=1, skipna=False)
    valid = valid_base & frame[raw_name].notna()
    if valid.sum() >= 30:
        pooled_sd = pooled_weighted_sd(
            frame.loc[valid, raw_name],
            frame.loc[valid, "weight_1997"],
            female_mask[valid],
        )
        if pooled_sd is not None:
            overall_mean = float(
                np.average(frame.loc[valid, raw_name], weights=frame.loc[valid, "weight_1997"])
            )
            frame[z_name] = (frame[raw_name] - overall_mean) / pooled_sd
    return frame


def prepare_design(
    sample: pd.DataFrame,
    categorical: list[str],
    continuous: list[str],
) -> pd.DataFrame:
    design = pd.DataFrame(index=sample.index)
    design["female"] = sample["female"].astype(float)

    for column in continuous:
        series = sample[column].astype(float)
        sd = float(series.std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            continue
        design[column] = (series - float(series.mean())) / sd

    for column in categorical:
        series = sample[column]
        if series.nunique(dropna=True) <= 1:
            continue
        codes = series.round().astype("Int64").astype(str)
        dummies = pd.get_dummies(codes, prefix=column, drop_first=True, dtype=float)
        if not dummies.empty:
            design = pd.concat([design, dummies], axis=1)

    return sm.add_constant(design, has_constant="add")


def same_sample_model(
    frame: pd.DataFrame,
    outcome: str,
    model_name: str,
    categorical: list[str],
    continuous: list[str],
    unrestricted_beta: float | None,
) -> dict[str, float | int | str] | None:
    required = ["sex", "weight_1997", outcome] + categorical + continuous
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
    )
    for column in required:
        valid &= frame[column].notna()

    sample = frame.loc[valid, required].copy()
    if len(sample) < 100:
        return None

    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    base_design = sm.add_constant(sample[["female"]], has_constant="add")
    full_design = prepare_design(sample, categorical, continuous)

    base_fit = sm.WLS(sample[outcome], base_design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    full_fit = sm.WLS(sample[outcome], full_design, weights=sample["weight_1997"]).fit(cov_type="HC1")

    base_beta = float(base_fit.params["female"])
    adjusted_beta = float(full_fit.params["female"])
    attenuation = None
    if abs(base_beta) > 1e-12:
        attenuation = 1.0 - (adjusted_beta / base_beta)

    base_low, base_high = base_fit.conf_int().loc["female"]
    adj_low, adj_high = full_fit.conf_int().loc["female"]
    result: dict[str, float | int | str] = {
        "score_name": outcome.removesuffix("_z"),
        "model_name": model_name,
        "n_obs": int(full_fit.nobs),
        "n_female": int(sample["female"].sum()),
        "n_male": int((1.0 - sample["female"]).sum()),
        "unrestricted_beta_sd": unrestricted_beta if unrestricted_beta is not None else "",
        "same_sample_base_sd": base_beta,
        "base_ci_low": float(base_low),
        "base_ci_high": float(base_high),
        "adjusted_beta_sd": adjusted_beta,
        "adjusted_ci_low": float(adj_low),
        "adjusted_ci_high": float(adj_high),
        "attenuation_share": attenuation if attenuation is not None else "",
        "n_controls": int(full_design.shape[1] - 2),
    }
    return result


def weighted_covariate_gap(
    frame: pd.DataFrame,
    column: str,
    kind: str,
) -> list[dict[str, float | int | str]]:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[column].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", column]].copy()
    if len(sample) < 100:
        return []
    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)

    if kind == "continuous":
        sd = float(sample[column].std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            return []
        sample["y"] = (sample[column] - float(sample[column].mean())) / sd
        design = sm.add_constant(sample[["female"]], has_constant="add")
        fit = sm.WLS(sample["y"], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
        low, high = fit.conf_int().loc["female"]
        return [
            {
                "covariate_name": column,
                "kind": kind,
                "category": "z_score",
                "n_obs": int(fit.nobs),
                "female_minus_male": float(fit.params["female"]),
                "ci_low": float(low),
                "ci_high": float(high),
            }
        ]

    rows: list[dict[str, float | int | str]] = []
    coded = sample[column].round().astype("Int64")
    categories = sorted(coded.dropna().unique().tolist())
    female_total = float(sample.loc[sample["female"].eq(1.0), "weight_1997"].sum())
    male_total = float(sample.loc[sample["female"].eq(0.0), "weight_1997"].sum())
    if female_total <= 0 or male_total <= 0:
        return []
    for category in categories:
        female_mask = sample["female"].eq(1.0) & coded.eq(category)
        male_mask = sample["female"].eq(0.0) & coded.eq(category)
        female_share = float(sample.loc[female_mask, "weight_1997"].sum() / female_total)
        male_share = float(sample.loc[male_mask, "weight_1997"].sum() / male_total)
        rows.append(
            {
                "covariate_name": column,
                "kind": kind,
                "category": int(category),
                "n_obs": int(len(sample)),
                "female_minus_male": female_share - male_share,
                "ci_low": "",
                "ci_high": "",
            }
        )
    return rows


def write_table(path: Path, fieldnames: list[str], rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    extra_fields = NLSY97["stage_a_fields"]
    print("Loading widened NLSY97 Stage A frame...")
    frame, _ = load_frame(extra_fields=extra_fields)
    frame, standardized = standardize_scores(frame)
    frame = add_quantitative_stress_surface(frame)

    extract_path = DATA_DIR / "nlsy97_stage_a_extract.parquet"
    frame.reset_index().to_parquet(extract_path, index=False)

    unrestricted = {}
    for outcome in TARGET_SCORES:
        result = fit_weighted_gap(frame, outcome)
        unrestricted[outcome] = None if result is None else float(result["beta_sd"])

    model_specs = [
        (
            "process_core",
            PROCESS_CATEGORICAL,
            PROCESS_CONTINUOUS,
        ),
        (
            "process_extended",
            PROCESS_CATEGORICAL + PROCESS_EXTRA_CATEGORICAL,
            PROCESS_CONTINUOUS,
        ),
        (
            "school_core",
            SCHOOL_CATEGORICAL,
            [],
        ),
        (
            "school_extended",
            SCHOOL_CATEGORICAL + SCHOOL_EXTRA_CATEGORICAL,
            [],
        ),
        (
            "process_plus_school_core",
            PROCESS_CATEGORICAL + SCHOOL_CATEGORICAL,
            PROCESS_CONTINUOUS,
        ),
        (
            "process_plus_school_extended",
            PROCESS_CATEGORICAL + PROCESS_EXTRA_CATEGORICAL + SCHOOL_CATEGORICAL,
            PROCESS_CONTINUOUS,
        ),
        (
            "process_plus_school_full",
            PROCESS_CATEGORICAL
            + PROCESS_EXTRA_CATEGORICAL
            + SCHOOL_CATEGORICAL
            + SCHOOL_EXTRA_CATEGORICAL,
            PROCESS_CONTINUOUS,
        ),
    ]

    model_rows: list[dict[str, float | int | str]] = []
    for outcome in TARGET_SCORES:
        for model_name, categorical, continuous in model_specs:
            row = same_sample_model(
                frame=frame,
                outcome=outcome,
                model_name=model_name,
                categorical=categorical,
                continuous=continuous,
                unrestricted_beta=unrestricted.get(outcome),
            )
            if row is not None:
                model_rows.append(row)

    covariate_rows = []
    for name, meta in extra_fields.items():
        covariate_rows.extend(weighted_covariate_gap(frame, name, meta["kind"]))

    models_path = DATA_DIR / "nlsy97_stage_a_models.tsv"
    covariates_path = DATA_DIR / "nlsy97_stage_a_covariate_gaps.tsv"
    write_table(
        models_path,
        [
            "score_name",
            "model_name",
            "n_obs",
            "n_female",
            "n_male",
            "unrestricted_beta_sd",
            "same_sample_base_sd",
            "base_ci_low",
            "base_ci_high",
            "adjusted_beta_sd",
            "adjusted_ci_low",
            "adjusted_ci_high",
            "attenuation_share",
            "n_controls",
        ],
        model_rows,
    )
    write_table(
        covariates_path,
        ["covariate_name", "kind", "category", "n_obs", "female_minus_male", "ci_low", "ci_high"],
        covariate_rows,
    )

    print(f"Wrote {extract_path}")
    print(f"Wrote {models_path}")
    print(f"Wrote {covariates_path}")
    for score in [
        "arithmetic_reasoning",
        "math_knowledge",
        "quantitative",
        "quantitative_plus_numerical_operations",
        "numerical_operations",
        "math_verbal_percentile",
    ]:
        print(f"\n{score}")
        for row in model_rows:
            if row["score_name"] != score:
                continue
            print(
                f"  {row['model_name']:<20} "
                f"base={row['same_sample_base_sd']:+.3f} "
                f"adj={row['adjusted_beta_sd']:+.3f} "
                f"atten={row['attenuation_share']:+.3f} "
                f"n={row['n_obs']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

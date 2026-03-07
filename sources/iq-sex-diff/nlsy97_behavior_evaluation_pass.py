#!/usr/bin/env python3
"""Late-school NLSY97 pass separating behavior/compliance from climate/fairness surfaces."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from nlsy97_stats_pipeline import load_frame
from stage0_config import NLSY97


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"

NEW_FIELDS = {
    "days_absent_1997": {"code": "R0069300", "kind": "continuous"},
    "late_without_excuse_1997": {"code": "R0069200", "kind": "continuous"},
    "teachers_good_1997": {"code": "R0069400", "kind": "categorical"},
    "teacher_interest_1997": {"code": "R0069500", "kind": "categorical"},
    "students_disrupt_1997": {"code": "R0069600", "kind": "categorical"},
    "students_graded_fairly_1997": {"code": "R0069700", "kind": "categorical"},
    "cheating_tests_homework_1997": {"code": "R0069800", "kind": "categorical"},
    "discipline_fair_1997": {"code": "R0069900", "kind": "categorical"},
    "feel_safe_school_1997": {"code": "R0070000", "kind": "categorical"},
    "spend_time_homework_1997": {"code": "R0072900", "kind": "categorical"},
    "homework_weekdays_1997": {"code": "R0073000", "kind": "continuous"},
    "homework_wkday_hours_1997": {"code": "R0073100", "kind": "continuous"},
    "homework_wkday_minutes_1997": {"code": "R0073200", "kind": "continuous"},
    "homework_wkend_hours_1997": {"code": "R0073300", "kind": "continuous"},
    "homework_wkend_minutes_1997": {"code": "R0073400", "kind": "continuous"},
    "suspension_days_1997": {"code": "E5271700", "kind": "continuous"},
    "cv_sample_type_1997": {"code": "R1235800", "kind": "categorical"},
    "cv_school_size_1997": {"code": "R1235900", "kind": "continuous"},
    "cv_student_teacher_ratio_1997": {"code": "R1236000", "kind": "continuous"},
}

OUT_EXTRACT = DATA_DIR / "nlsy97_behavior_evaluation_extract.parquet"
OUT_GAPS = DATA_DIR / "nlsy97_behavior_gaps.tsv"
OUT_MODELS = DATA_DIR / "nlsy97_behavior_block_models.tsv"
OUT_IPW = DATA_DIR / "nlsy97_behavior_ipw_models.tsv"
OUT_CAUSAL = DATA_DIR / "nlsy97_behavior_causal_models.tsv"
OUT_CAUSAL_DATA = DATA_DIR / "nlsy97_behavior_causal_model_data.csv"


def clean_nonnegative(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return values.where(values >= 0)


def clean_likert(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    values = values.where(values.isin([1, 2, 3, 4]))
    return values


def weighted_standardize(series: pd.Series, weights: pd.Series) -> pd.Series:
    valid = series.notna() & weights.gt(0)
    if valid.sum() < 30:
        return pd.Series(np.nan, index=series.index)
    mean = float(np.average(series.loc[valid], weights=weights.loc[valid]))
    var = float(np.average((series.loc[valid] - mean) ** 2, weights=weights.loc[valid]))
    if not math.isfinite(var) or var <= 0:
        return pd.Series(np.nan, index=series.index)
    return (series - mean) / math.sqrt(var)


def weighted_gap(frame: pd.DataFrame, column: str) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[column].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", column]].copy()
    if len(sample) < 100:
        return None
    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    design = sm.add_constant(sample[["female"]], has_constant="add")
    fit = sm.WLS(sample[column], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "measure": column,
        "n_obs": int(fit.nobs),
        "female_beta": float(fit.params["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
    }


def write_table(path: Path, fieldnames: list[str], rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def build_frame() -> pd.DataFrame:
    base = pd.read_parquet(DATA_DIR / "nlsy97_transcript_deep_extract.parquet")
    extra, _ = load_frame(extra_fields=NEW_FIELDS)
    add_cols = [name for name in NEW_FIELDS if name not in base.columns]
    frame = base.join(extra[add_cols], how="left")

    for name in [
        "days_absent_1997",
        "late_without_excuse_1997",
        "homework_weekdays_1997",
        "homework_wkday_hours_1997",
        "homework_wkday_minutes_1997",
        "homework_wkend_hours_1997",
        "homework_wkend_minutes_1997",
        "suspension_days_1997",
        "cv_school_size_1997",
        "cv_student_teacher_ratio_1997",
    ]:
        frame[name] = clean_nonnegative(frame[name])

    for name in [
        "teachers_good_1997",
        "teacher_interest_1997",
        "students_disrupt_1997",
        "students_graded_fairly_1997",
        "cheating_tests_homework_1997",
        "discipline_fair_1997",
        "feel_safe_school_1997",
    ]:
        frame[name] = clean_likert(frame[name])

    frame["spend_time_homework_1997"] = clean_nonnegative(frame["spend_time_homework_1997"]).where(
        pd.to_numeric(frame["spend_time_homework_1997"], errors="coerce").isin([0, 1])
    )
    frame["cv_sample_type_1997"] = clean_nonnegative(frame["cv_sample_type_1997"])

    frame["female"] = frame["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    frame["suspension_any_1997"] = frame["suspension_days_1997"].fillna(0).gt(0).astype(float)

    weekday_minutes = (
        frame["homework_wkday_hours_1997"].fillna(0) * 60
        + frame["homework_wkday_minutes_1997"].fillna(0)
    )
    weekend_minutes = (
        frame["homework_wkend_hours_1997"].fillna(0) * 60
        + frame["homework_wkend_minutes_1997"].fillna(0)
    )
    frame["homework_total_minutes_1997"] = frame["homework_weekdays_1997"].fillna(0) * weekday_minutes + weekend_minutes
    no_homework = frame["spend_time_homework_1997"].eq(0)
    frame.loc[no_homework, "homework_total_minutes_1997"] = 0.0

    positive_school_items = {
        "teachers_good_pos_1997": "teachers_good_1997",
        "teacher_interest_pos_1997": "teacher_interest_1997",
        "students_graded_fairly_pos_1997": "students_graded_fairly_1997",
        "discipline_fair_pos_1997": "discipline_fair_1997",
        "feel_safe_school_pos_1997": "feel_safe_school_1997",
    }
    for new_name, source in positive_school_items.items():
        frame[new_name] = 5 - frame[source]

    frame["students_disrupt_pos_1997"] = frame["students_disrupt_1997"]
    frame["cheating_tests_homework_pos_1997"] = frame["cheating_tests_homework_1997"]

    for column in [
        "days_absent_1997",
        "late_without_excuse_1997",
        "homework_weekdays_1997",
        "homework_total_minutes_1997",
        "cv_school_size_1997",
        "cv_student_teacher_ratio_1997",
        "suspension_any_1997",
        "teachers_good_pos_1997",
        "teacher_interest_pos_1997",
        "students_graded_fairly_pos_1997",
        "discipline_fair_pos_1997",
        "feel_safe_school_pos_1997",
        "students_disrupt_pos_1997",
        "cheating_tests_homework_pos_1997",
    ]:
        source = frame[column]
        if column in {"days_absent_1997", "late_without_excuse_1997", "homework_total_minutes_1997"}:
            source = np.log1p(source)
        frame[f"{column}_z"] = weighted_standardize(source, frame["weight_1997"])

    behavior_components = [
        -frame["days_absent_1997_z"],
        -frame["late_without_excuse_1997_z"],
        frame["homework_weekdays_1997_z"],
        frame["homework_total_minutes_1997_z"],
        -frame["suspension_any_1997_z"],
    ]
    behavior_stack = pd.concat(behavior_components, axis=1)
    behavior_count = behavior_stack.notna().sum(axis=1)
    frame["behavior_compliance_index_z"] = behavior_stack.mean(axis=1, skipna=True).where(behavior_count >= 3)

    climate_components = [
        frame["teachers_good_pos_1997_z"],
        frame["teacher_interest_pos_1997_z"],
        frame["students_graded_fairly_pos_1997_z"],
        frame["discipline_fair_pos_1997_z"],
        frame["feel_safe_school_pos_1997_z"],
        frame["students_disrupt_pos_1997_z"],
        frame["cheating_tests_homework_pos_1997_z"],
    ]
    climate_stack = pd.concat(climate_components, axis=1)
    climate_count = climate_stack.notna().sum(axis=1)
    frame["climate_fairness_index_z"] = climate_stack.mean(axis=1, skipna=True).where(climate_count >= 4)

    frame["transcript_observed"] = frame["transcript_gpa_math_hstr_z"].notna().astype(float)
    frame["joint_late_school_sample"] = (
        frame["math_knowledge_z"].notna()
        & frame["arithmetic_reasoning_z"].notna()
        & frame["transcript_gpa_math_hstr_z"].notna()
        & frame["piat_standard_1997_z"].notna()
        & frame["age_months_1997"].notna()
        & frame["behavior_compliance_index_z"].notna()
        & frame["climate_fairness_index_z"].notna()
        & frame["cv_sample_type_1997"].notna()
        & frame["cv_school_size_1997_z"].notna()
        & frame["cv_student_teacher_ratio_1997_z"].notna()
        & frame["weight_1997"].gt(0)
    )
    return frame


def fit_block_models(frame: pd.DataFrame) -> list[dict[str, float | int | str]]:
    outcomes = ["math_knowledge_z", "arithmetic_reasoning_z", "transcript_gpa_math_hstr_z"]
    formulas = {
        "base_context": "{y} ~ female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997)",
        "plus_behavior": "{y} ~ female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997) + behavior_compliance_index_z",
        "plus_climate": "{y} ~ female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997) + climate_fairness_index_z",
        "plus_behavior_climate": "{y} ~ female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997) + behavior_compliance_index_z + climate_fairness_index_z",
    }
    rows: list[dict[str, float | int | str]] = []
    for outcome in outcomes:
        for model_name, template in formulas.items():
            needed = [
                outcome,
                "female",
                "piat_standard_1997_z",
                "age_months_1997",
                "cv_school_size_1997_z",
                "cv_student_teacher_ratio_1997_z",
                "cv_sample_type_1997",
            ]
            if "behavior" in model_name:
                needed.append("behavior_compliance_index_z")
            if "climate" in model_name:
                needed.append("climate_fairness_index_z")
            sample = frame.loc[frame["weight_1997"].gt(0), needed + ["weight_1997"]].dropna()
            if len(sample) < 250:
                continue
            fit = smf.wls(template.format(y=outcome), data=sample, weights=sample["weight_1997"]).fit(cov_type="HC1")
            low, high = fit.conf_int().loc["female"]
            row: dict[str, float | int | str] = {
                "outcome": outcome,
                "model_name": model_name,
                "n_obs": int(fit.nobs),
                "female_beta": float(fit.params["female"]),
                "female_ci_low": float(low),
                "female_ci_high": float(high),
                "female_p": float(fit.pvalues["female"]),
                "r_squared": float(fit.rsquared),
            }
            for name in ["behavior_compliance_index_z", "climate_fairness_index_z"]:
                if name in fit.params:
                    row[f"{name}_beta"] = float(fit.params[name])
                    row[f"{name}_p"] = float(fit.pvalues[name])
                else:
                    row[f"{name}_beta"] = math.nan
                    row[f"{name}_p"] = math.nan
            rows.append(row)
    return rows


def fit_ipw_models(frame: pd.DataFrame) -> list[dict[str, float | int | str]]:
    selection_sample = frame.loc[
        frame["weight_1997"].gt(0)
        & frame["piat_standard_1997_z"].notna()
        & frame["age_months_1997"].notna()
        & frame["behavior_compliance_index_z"].notna()
        & frame["climate_fairness_index_z"].notna()
        & frame["cv_sample_type_1997"].notna()
        & frame["cv_school_size_1997_z"].notna()
        & frame["cv_student_teacher_ratio_1997_z"].notna(),
        [
            "transcript_observed",
            "female",
            "piat_standard_1997_z",
            "age_months_1997",
            "behavior_compliance_index_z",
            "climate_fairness_index_z",
            "cv_sample_type_1997",
            "cv_school_size_1997_z",
            "cv_student_teacher_ratio_1997_z",
            "weight_1997",
        ],
    ].dropna()
    select_fit = smf.glm(
        "transcript_observed ~ female + piat_standard_1997_z + age_months_1997 + behavior_compliance_index_z + climate_fairness_index_z + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997)",
        data=selection_sample,
        family=sm.families.Binomial(),
        freq_weights=selection_sample["weight_1997"],
    ).fit()
    selection_sample["p_obs"] = np.clip(select_fit.predict(selection_sample), 0.05, 0.95)

    observed = selection_sample.loc[selection_sample["transcript_observed"].eq(1.0), ["p_obs"]].copy()
    observed["caseid"] = observed.index
    frame = frame.join(observed.set_index("caseid"), how="left")
    frame["ipw_transcript"] = 1.0 / frame["p_obs"]

    rows: list[dict[str, float | int | str]] = []
    for outcome in ["math_knowledge_z", "transcript_gpa_math_hstr_z"]:
        sample = frame.loc[
            frame["weight_1997"].gt(0)
            & frame["transcript_observed"].eq(1.0)
            & frame[outcome].notna()
            & frame["piat_standard_1997_z"].notna()
            & frame["age_months_1997"].notna()
            & frame["cv_sample_type_1997"].notna()
            & frame["cv_school_size_1997_z"].notna()
            & frame["cv_student_teacher_ratio_1997_z"].notna(),
            [
                outcome,
                "female",
                "piat_standard_1997_z",
                "age_months_1997",
                "cv_sample_type_1997",
                "cv_school_size_1997_z",
                "cv_student_teacher_ratio_1997_z",
                "weight_1997",
                "ipw_transcript",
            ],
        ].dropna()
        if len(sample) < 250:
            continue
        for weighting in ["survey_only", "survey_x_ipw"]:
            weights = sample["weight_1997"] if weighting == "survey_only" else sample["weight_1997"] * sample["ipw_transcript"]
            fit = smf.wls(
                f"{outcome} ~ female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997)",
                data=sample,
                weights=weights,
            ).fit(cov_type="HC1")
            low, high = fit.conf_int().loc["female"]
            rows.append(
                {
                    "outcome": outcome,
                    "weighting": weighting,
                    "n_obs": int(fit.nobs),
                    "female_beta": float(fit.params["female"]),
                    "female_ci_low": float(low),
                    "female_ci_high": float(high),
                    "female_p": float(fit.pvalues["female"]),
                    "r_squared": float(fit.rsquared),
                }
            )
    return rows


def fit_causal_models(frame: pd.DataFrame) -> list[dict[str, float | int | str]]:
    outcomes = ["math_knowledge_z", "transcript_gpa_math_hstr_z"]
    rows: list[dict[str, float | int | str]] = []
    model_data_rows: list[dict[str, float | int | str]] = []
    for outcome in outcomes:
        cols = [
            outcome,
            "behavior_compliance_index_z",
            "female",
            "piat_standard_1997_z",
            "age_months_1997",
            "cv_sample_type_1997",
            "cv_school_size_1997_z",
            "cv_student_teacher_ratio_1997_z",
            "weight_1997",
        ]
        sample = frame.loc[frame["weight_1997"].gt(0), cols].dropna()
        if len(sample) < 250:
            continue
        formula = f"{outcome} ~ behavior_compliance_index_z + female + piat_standard_1997_z + age_months_1997 + cv_school_size_1997_z + cv_student_teacher_ratio_1997_z + C(cv_sample_type_1997)"
        fit = smf.wls(formula, data=sample, weights=sample["weight_1997"]).fit(cov_type="HC1")
        low, high = fit.conf_int().loc["behavior_compliance_index_z"]
        rows.append(
            {
                "outcome": outcome,
                "treatment": "behavior_compliance_index_z",
                "n_obs": int(fit.nobs),
                "beta": float(fit.params["behavior_compliance_index_z"]),
                "ci_low": float(low),
                "ci_high": float(high),
                "p_value": float(fit.pvalues["behavior_compliance_index_z"]),
                "female_beta": float(fit.params["female"]),
                "r_squared": float(fit.rsquared),
                "formula": formula,
            }
        )
        for record in sample.to_dict(orient="records"):
            model_data_rows.append({"outcome_name": outcome, **record})

    if model_data_rows:
        fieldnames = sorted({key for row in model_data_rows for key in row})
        with OUT_CAUSAL_DATA.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(model_data_rows)
    return rows


def main() -> int:
    frame = build_frame()
    OUT_EXTRACT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUT_EXTRACT, index=True)

    gap_rows = []
    for measure in [
        "behavior_compliance_index_z",
        "climate_fairness_index_z",
        "days_absent_1997_z",
        "late_without_excuse_1997_z",
        "homework_total_minutes_1997_z",
        "suspension_any_1997_z",
        "teachers_good_pos_1997_z",
        "teacher_interest_pos_1997_z",
        "students_graded_fairly_pos_1997_z",
        "discipline_fair_pos_1997_z",
        "feel_safe_school_pos_1997_z",
    ]:
        result = weighted_gap(frame, measure)
        if result is not None:
            gap_rows.append(result)
    write_table(OUT_GAPS, list(gap_rows[0].keys()), gap_rows)

    model_rows = fit_block_models(frame)
    write_table(OUT_MODELS, list(model_rows[0].keys()), model_rows)

    ipw_rows = fit_ipw_models(frame)
    write_table(OUT_IPW, list(ipw_rows[0].keys()), ipw_rows)

    causal_rows = fit_causal_models(frame)
    write_table(OUT_CAUSAL, list(causal_rows[0].keys()), causal_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

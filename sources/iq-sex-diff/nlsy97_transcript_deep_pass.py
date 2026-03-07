#!/usr/bin/env python3
"""Deeper NLSY97 late-school wedge pass using 1997 course exposure plus transcript destinations."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from nlsy97_stats_pipeline import load_frame, pooled_weighted_sd, standardize_scores
from stage0_config import NLSY97


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"

EXTRA_FIELDS = {
    "age_months_1997": {"code": "R1193900", "kind": "continuous"},
    "piat_standard_1997": {"code": "R1210800", "kind": "continuous"},
    "asvab_test_month": {"code": "R9708601", "kind": "categorical"},
    "asvab_test_year": {"code": "R9708602", "kind": "categorical"},
    "avg_grade_recent": {"code": "R9700100", "kind": "categorical"},
    "grade_fall_1997": {"code": "R9708800", "kind": "categorical"},
    "math_honors_1": {"code": "R0064600", "kind": "categorical"},
    "math_honors_2": {"code": "R0064700", "kind": "categorical"},
    "math_honors_3": {"code": "R0064800", "kind": "categorical"},
    "math_honors_4": {"code": "R0064900", "kind": "categorical"},
    "math_honors_5": {"code": "R0065000", "kind": "categorical"},
    "math_honors_6": {"code": "R0065100", "kind": "categorical"},
    "math_course_1_basic": {"code": "R9700400", "kind": "categorical"},
    "math_course_2_algebra1": {"code": "R9700401", "kind": "categorical"},
    "math_course_3_geometry": {"code": "R9700402", "kind": "categorical"},
    "math_course_4_algebra2": {"code": "R9700403", "kind": "categorical"},
    "math_course_5_trig": {"code": "R9700404", "kind": "categorical"},
    "math_course_6_precalc": {"code": "R9700405", "kind": "categorical"},
    "math_course_7_calculus": {"code": "R9700406", "kind": "categorical"},
    "math_course_8_other_advanced": {"code": "R9700407", "kind": "categorical"},
    "math_course_9_other_math": {"code": "R9700408", "kind": "categorical"},
    "math_course_10_none": {"code": "R9700409", "kind": "categorical"},
    "transcript_voc_spec_hstr": {"code": "R9860000", "kind": "categorical"},
    "transcript_sch_pgm_hstr": {"code": "R9860100", "kind": "categorical"},
    "transcript_mathpipe_hstr": {"code": "R9860200", "kind": "categorical"},
    "transcript_total_math_hstr": {"code": "R9864300", "kind": "continuous"},
    "transcript_total_academic_math_hstr": {"code": "R9864400", "kind": "continuous"},
    "transcript_total_academic_nolo_math_hstr": {"code": "R9864500", "kind": "continuous"},
    "transcript_total_advanced_math_hstr": {"code": "R9864600", "kind": "continuous"},
    "transcript_pr_sch_calc_hstr": {"code": "R9870200", "kind": "categorical"},
    "transcript_pr_sch_ap_hstr": {"code": "R9870300", "kind": "categorical"},
    "transcript_pr_sch_ib_hstr": {"code": "R9870400", "kind": "categorical"},
    "transcript_gpa_overall_hstr": {"code": "R9871900", "kind": "continuous"},
    "transcript_gpa_math_hstr": {"code": "R9872200", "kind": "continuous"},
    "transcript_ap_calc_hstr": {"code": "R9794200", "kind": "continuous"},
    "transcript_prob_flag_hstr": {"code": "R9872500", "kind": "categorical"},
}

SURFACE_SPECS = {
    "piat_standard_1997": {"z_name": "piat_standard_1997_z", "scale": 1.0},
    "transcript_total_math_hstr": {"z_name": "transcript_total_math_hstr_z", "scale": 100.0},
    "transcript_total_academic_math_hstr": {
        "z_name": "transcript_total_academic_math_hstr_z",
        "scale": 100.0,
    },
    "transcript_total_academic_nolo_math_hstr": {
        "z_name": "transcript_total_academic_nolo_math_hstr_z",
        "scale": 100.0,
    },
    "transcript_total_advanced_math_hstr": {
        "z_name": "transcript_total_advanced_math_hstr_z",
        "scale": 100.0,
    },
    "transcript_gpa_overall_hstr": {"z_name": "transcript_gpa_overall_hstr_z", "scale": 100.0},
    "transcript_gpa_math_hstr": {"z_name": "transcript_gpa_math_hstr_z", "scale": 100.0},
}

PIPE_LABELS = {
    100: "100_none",
    200: "200_non_academic",
    300: "300_low_academic",
    400: "400_middle_academic_1",
    500: "500_middle_academic_2",
    600: "600_advanced_academic_1",
    700: "700_advanced_academic_2",
    800: "800_advanced_academic_3",
}

PIPE_GROUP_LABELS = {
    100: "low_or_none",
    200: "low_or_none",
    300: "low_or_none",
    400: "middle",
    500: "middle",
    600: "advanced",
    700: "advanced",
    800: "advanced",
}

HIGHEST_LABELS = {
    0: "0_none",
    1: "1_basic_or_other",
    2: "2_algebra1",
    3: "3_geometry",
    4: "4_algebra2",
    5: "5_trig",
    6: "6_precalc",
    7: "7_calculus_or_other_advanced",
}

OVERLAP_SURFACES = [
    "piat_standard_1997_z",
    "arithmetic_reasoning_z",
    "math_knowledge_z",
    "quantitative_z",
]

TRANSCRIPT_SURFACES = [
    "transcript_gpa_math_hstr_z",
    "transcript_total_math_hstr_z",
    "transcript_total_academic_math_hstr_z",
    "transcript_total_academic_nolo_math_hstr_z",
    "transcript_total_advanced_math_hstr_z",
]

OUT_EXTRACT = DATA_DIR / "nlsy97_transcript_deep_extract.parquet"
OUT_OVERLAP = DATA_DIR / "nlsy97_transcript_deep_overlap_extract.parquet"
OUT_SURFACE = DATA_DIR / "nlsy97_transcript_deep_surface_gaps.tsv"
OUT_PIPE = DATA_DIR / "nlsy97_transcript_deep_by_mathpipe.tsv"
OUT_HIGHEST = DATA_DIR / "nlsy97_transcript_deep_by_highest.tsv"
OUT_MODELS = DATA_DIR / "nlsy97_transcript_deep_models.tsv"
OUT_TRANSCRIPT = DATA_DIR / "nlsy97_transcript_deep_transcript_models.tsv"
OUT_BINARY = DATA_DIR / "nlsy97_transcript_deep_binary.tsv"
OUT_DIAG = DATA_DIR / "nlsy97_transcript_deep_diagnostics.tsv"


def clean_binary(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    values = values.where(values >= 0)
    return values.where(values.isin([0, 1]))


def clean_continuous(series: pd.Series, scale: float = 1.0) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    values = values.where(values >= 0)
    if scale != 1.0:
        values = values / scale
    return values


def standardize_extra_surface(frame: pd.DataFrame, source_name: str, z_name: str) -> pd.DataFrame:
    frame = frame.copy()
    female_mask = frame["sex"].eq(NLSY97["sex"]["female"])
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[source_name].notna()
    )
    if valid.sum() < 30:
        return frame
    pooled_sd = pooled_weighted_sd(
        frame.loc[valid, source_name],
        frame.loc[valid, "weight_1997"],
        female_mask[valid],
    )
    if pooled_sd is None:
        return frame
    overall_mean = float(np.average(frame.loc[valid, source_name], weights=frame.loc[valid, "weight_1997"]))
    frame[z_name] = (frame[source_name] - overall_mean) / pooled_sd
    return frame


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_d(values: np.ndarray, female: np.ndarray, weights: np.ndarray) -> tuple[float, float, float]:
    mask_f = female == 1
    mask_m = female == 0
    if mask_f.sum() == 0 or mask_m.sum() == 0:
        return math.nan, math.nan, math.nan
    vf = values[mask_f]
    vm = values[mask_m]
    wf = weights[mask_f]
    wm = weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    var_f = weighted_var(vf, wf)
    var_m = weighted_var(vm, wm)
    pooled = math.sqrt(max((var_f + var_m) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def write_table(path: Path, fieldnames: list[str], rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def clean_and_derive(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["age_months_1997"] = clean_continuous(frame["age_months_1997"])
    frame["asvab_test_month"] = clean_continuous(frame["asvab_test_month"])
    frame["asvab_test_year"] = clean_continuous(frame["asvab_test_year"])
    frame["avg_grade_recent"] = clean_continuous(frame["avg_grade_recent"])
    frame["grade_fall_1997"] = clean_continuous(frame["grade_fall_1997"])

    for column, spec in SURFACE_SPECS.items():
        frame[column] = clean_continuous(frame[column], scale=spec["scale"])

    categorical_cols = [
        "transcript_voc_spec_hstr",
        "transcript_sch_pgm_hstr",
        "transcript_mathpipe_hstr",
        "transcript_pr_sch_calc_hstr",
        "transcript_pr_sch_ap_hstr",
        "transcript_pr_sch_ib_hstr",
        "transcript_prob_flag_hstr",
    ]
    for column in categorical_cols:
        frame[column] = clean_continuous(frame[column])

    honors_cols = [f"math_honors_{idx}" for idx in range(1, 7)]
    for column in honors_cols:
        frame[column] = clean_binary(frame[column])
    honors = frame[honors_cols].copy()
    honors_observed = honors.notna().any(axis=1)
    frame["math_honors_any_1997"] = np.where(honors_observed, (honors == 1).any(axis=1).astype(float), np.nan)
    frame["math_honors_depth_1997"] = np.where(honors_observed, honors.fillna(0.0).sum(axis=1), np.nan)

    course_cols = [
        "math_course_1_basic",
        "math_course_2_algebra1",
        "math_course_3_geometry",
        "math_course_4_algebra2",
        "math_course_5_trig",
        "math_course_6_precalc",
        "math_course_7_calculus",
        "math_course_8_other_advanced",
        "math_course_9_other_math",
        "math_course_10_none",
    ]
    for column in course_cols:
        frame[column] = clean_binary(frame[column])

    observed_courses = frame[course_cols].notna().any(axis=1)
    math_course_set = course_cols[:9]
    frame["selfreport_math_course_count_1997"] = np.where(
        observed_courses,
        frame[math_course_set].fillna(0.0).sum(axis=1),
        np.nan,
    )
    frame["selfreport_algebra2_plus_1997"] = np.where(
        observed_courses,
        (frame[[
            "math_course_4_algebra2",
            "math_course_5_trig",
            "math_course_6_precalc",
            "math_course_7_calculus",
            "math_course_8_other_advanced",
        ]].fillna(0.0).sum(axis=1) > 0).astype(float),
        np.nan,
    )
    frame["selfreport_precalc_plus_1997"] = np.where(
        observed_courses,
        (frame[[
            "math_course_6_precalc",
            "math_course_7_calculus",
            "math_course_8_other_advanced",
        ]].fillna(0.0).sum(axis=1) > 0).astype(float),
        np.nan,
    )
    frame["selfreport_calc_plus_1997"] = np.where(
        observed_courses,
        (frame[[
            "math_course_7_calculus",
            "math_course_8_other_advanced",
        ]].fillna(0.0).sum(axis=1) > 0).astype(float),
        np.nan,
    )

    highest = pd.Series(np.nan, index=frame.index, dtype=float)
    highest.loc[observed_courses] = 0.0
    rank_map = [
        ("math_course_1_basic", 1),
        ("math_course_9_other_math", 1),
        ("math_course_2_algebra1", 2),
        ("math_course_3_geometry", 3),
        ("math_course_4_algebra2", 4),
        ("math_course_5_trig", 5),
        ("math_course_6_precalc", 6),
        ("math_course_7_calculus", 7),
        ("math_course_8_other_advanced", 7),
    ]
    for column, rank in rank_map:
        mask = frame[column].eq(1)
        highest.loc[mask] = np.fmax(highest.loc[mask].fillna(0.0), float(rank))
    none_mask = frame["math_course_10_none"].eq(1) & frame[math_course_set].fillna(0.0).sum(axis=1).eq(0)
    highest.loc[none_mask] = 0.0
    frame["selfreport_highest_math_1997"] = highest
    frame["selfreport_highest_math_label"] = frame["selfreport_highest_math_1997"].map(HIGHEST_LABELS)

    frame["transcript_mathpipe_label"] = frame["transcript_mathpipe_hstr"].map(PIPE_LABELS)
    frame["transcript_mathpipe_group"] = frame["transcript_mathpipe_hstr"].map(PIPE_GROUP_LABELS)
    frame["transcript_ap_calc_any_hstr"] = np.where(
        frame["transcript_ap_calc_hstr"].notna(),
        (frame["transcript_ap_calc_hstr"] > 0).astype(float),
        np.nan,
    )
    return frame


def unique_preserve(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in seq:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def build_design(
    sample: pd.DataFrame,
    continuous: list[str],
    categorical: list[str],
    binary: list[str],
    include_female: bool = True,
) -> pd.DataFrame:
    design = pd.DataFrame(index=sample.index)
    if include_female:
        design["female"] = sample["female"].astype(float)

    for column in unique_preserve(continuous):
        series = sample[column].astype(float)
        sd = float(series.std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            continue
        design[column] = (series - float(series.mean())) / sd

    for column in unique_preserve(binary):
        if sample[column].nunique(dropna=True) <= 1:
            continue
        design[column] = sample[column].astype(float)

    for column in unique_preserve(categorical):
        series = sample[column]
        if series.nunique(dropna=True) <= 1:
            continue
        if column.endswith("_label") or column.endswith("_group"):
            codes = series.astype(str)
        else:
            codes = series.round().astype("Int64").astype(str)
        dummies = pd.get_dummies(codes, prefix=column, drop_first=True, dtype=float)
        if not dummies.empty:
            design = pd.concat([design, dummies], axis=1)

    return sm.add_constant(design, has_constant="add")


def fit_progression_model(
    frame: pd.DataFrame,
    outcome: str,
    reference_surface: str,
    sample_name: str,
    model_name: str,
    continuous: list[str],
    categorical: list[str],
    binary: list[str],
) -> dict[str, float | int | str] | None:
    continuous = unique_preserve(continuous)
    categorical = unique_preserve(categorical)
    binary = unique_preserve(binary)
    required = unique_preserve(["sex", "weight_1997", outcome, reference_surface] + continuous + categorical + binary)
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
    design = build_design(sample, continuous=continuous, categorical=categorical, binary=binary)
    fit = sm.WLS(sample[outcome], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "sample_name": sample_name,
        "outcome": outcome.removesuffix("_z"),
        "reference_surface": reference_surface.removesuffix("_z"),
        "model_name": model_name,
        "n_obs": int(fit.nobs),
        "n_female": int(sample["female"].sum()),
        "n_male": int((1.0 - sample["female"]).sum()),
        "female_beta_sd": float(fit.params["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
        "n_controls": int(design.shape[1] - 2),
    }


def summarize_surface_gap(frame: pd.DataFrame, surface_name: str, sample_name: str) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[surface_name].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", surface_name]].copy()
    if len(sample) < 100:
        return None
    female = sample["sex"].eq(NLSY97["sex"]["female"]).astype(int).to_numpy()
    values = sample[surface_name].to_numpy(dtype=float)
    weights = sample["weight_1997"].to_numpy(dtype=float)
    mean_f, mean_m, d = weighted_d(values, female, weights)
    model = sm.WLS(
        sample[surface_name],
        sm.add_constant(sample["sex"].eq(NLSY97["sex"]["female"]).astype(float), has_constant="add"),
        weights=sample["weight_1997"],
    ).fit(cov_type="HC1")
    low, high = model.conf_int().iloc[1]
    return {
        "sample_name": sample_name,
        "surface_name": surface_name.removesuffix("_z"),
        "n_obs": int(model.nobs),
        "female_mean": mean_f,
        "male_mean": mean_m,
        "female_beta_sd": float(model.params.iloc[1]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(model.pvalues.iloc[1]),
        "d_female_minus_male": d,
    }


def summarize_binary_gap(frame: pd.DataFrame, surface_name: str, sample_name: str) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[surface_name].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", surface_name]].copy()
    if len(sample) < 100:
        return None
    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    fit = sm.WLS(sample[surface_name], sm.add_constant(sample["female"], has_constant="add"), weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "sample_name": sample_name,
        "surface_name": surface_name,
        "n_obs": int(fit.nobs),
        "female_minus_male_share": float(fit.params["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
    }


def summarize_by_group(
    frame: pd.DataFrame,
    group_col: str,
    outcome_cols: list[str],
    sample_name: str,
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    valid_base = frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]]) & frame["weight_1997"].gt(0)
    for (group,), sub in frame.loc[valid_base & frame[group_col].notna()].groupby([group_col], observed=True):
        if len(sub) < 80:
            continue
        female = sub["sex"].eq(NLSY97["sex"]["female"]).astype(int).to_numpy()
        weights = sub["weight_1997"].to_numpy(dtype=float)
        for outcome in outcome_cols:
            work = sub.loc[sub[outcome].notna(), ["sex", "weight_1997", outcome]].copy()
            if len(work) < 50 or work["sex"].nunique() < 2:
                continue
            f = work["sex"].eq(NLSY97["sex"]["female"]).astype(int).to_numpy()
            w = work["weight_1997"].to_numpy(dtype=float)
            v = work[outcome].to_numpy(dtype=float)
            mean_f, mean_m, d = weighted_d(v, f, w)
            rows.append(
                {
                    "sample_name": sample_name,
                    "group_col": group_col,
                    "group_value": str(group),
                    "surface_name": outcome.removesuffix("_z"),
                    "n_obs": int(len(work)),
                    "female_mean": mean_f,
                    "male_mean": mean_m,
                    "d_female_minus_male": d,
                }
            )
    return rows


def main() -> int:
    frame, _ = load_frame(extra_fields=EXTRA_FIELDS)
    frame = clean_and_derive(frame)
    frame, _ = standardize_scores(frame)
    for source_name, spec in SURFACE_SPECS.items():
        frame = standardize_extra_surface(frame, source_name, spec["z_name"])

    frame.reset_index().to_parquet(OUT_EXTRACT, index=False)

    overlap = frame.loc[
        frame["piat_standard_1997_z"].notna()
        & frame["age_months_1997"].notna()
        & frame["asvab_test_month"].notna()
        & frame["asvab_test_year"].notna()
    ].copy()
    overlap.reset_index().to_parquet(OUT_OVERLAP, index=False)

    surface_rows: list[dict[str, float | int | str]] = []
    for sample_name, sample_frame in [
        ("full_valid", frame),
        ("piat_overlap", overlap),
    ]:
        for surface in OVERLAP_SURFACES + TRANSCRIPT_SURFACES:
            row = summarize_surface_gap(sample_frame, surface, sample_name)
            if row is not None:
                surface_rows.append(row)

    binary_rows: list[dict[str, float | int | str]] = []
    for sample_name, sample_frame in [("full_valid", frame), ("piat_overlap", overlap)]:
        for surface in [
            "math_honors_any_1997",
            "selfreport_algebra2_plus_1997",
            "selfreport_precalc_plus_1997",
            "selfreport_calc_plus_1997",
            "transcript_ap_calc_any_hstr",
        ]:
            row = summarize_binary_gap(sample_frame, surface, sample_name)
            if row is not None:
                binary_rows.append(row)

    pipe_rows = summarize_by_group(
        overlap,
        "transcript_mathpipe_group",
        [
            "piat_standard_1997_z",
            "arithmetic_reasoning_z",
            "math_knowledge_z",
            "quantitative_z",
            "transcript_gpa_math_hstr_z",
            "transcript_total_advanced_math_hstr_z",
        ],
        "piat_overlap",
    )
    highest_rows = summarize_by_group(
        overlap,
        "selfreport_highest_math_label",
        [
            "piat_standard_1997_z",
            "arithmetic_reasoning_z",
            "math_knowledge_z",
            "quantitative_z",
            "transcript_gpa_math_hstr_z",
        ],
        "piat_overlap",
    )

    model_rows: list[dict[str, float | int | str]] = []
    progression_specs = [
        (
            "base_same_sample",
            [],
            [],
            [],
        ),
        (
            "design_same_sample",
            ["age_months_1997"],
            ["asvab_test_month", "asvab_test_year"],
            [],
        ),
        (
            "exposure_same_sample",
            ["age_months_1997"],
            ["asvab_test_month", "asvab_test_year", "selfreport_highest_math_label"],
            [],
        ),
        (
            "evaluation_stress",
            ["age_months_1997", "math_honors_depth_1997"],
            [
                "asvab_test_month",
                "asvab_test_year",
                "selfreport_highest_math_label",
                "avg_grade_recent",
                "grade_fall_1997",
            ],
            [],
        ),
        (
            "offer_stress",
            ["age_months_1997"],
            [
                "asvab_test_month",
                "asvab_test_year",
                "selfreport_highest_math_label",
                "transcript_pr_sch_calc_hstr",
                "transcript_pr_sch_ap_hstr",
                "transcript_pr_sch_ib_hstr",
                "transcript_sch_pgm_hstr",
            ],
            [],
        ),
        (
            "destination_stress",
            ["age_months_1997", "transcript_total_advanced_math_hstr_z"],
            [
                "asvab_test_month",
                "asvab_test_year",
                "selfreport_highest_math_label",
                "transcript_mathpipe_group",
            ],
            [],
        ),
    ]

    for outcome in ["arithmetic_reasoning_z", "math_knowledge_z", "quantitative_z"]:
        for model_name, continuous, categorical, binary in progression_specs:
            row = fit_progression_model(
                overlap,
                outcome=outcome,
                reference_surface="piat_standard_1997_z",
                sample_name="piat_overlap",
                model_name=model_name,
                continuous=continuous + ["piat_standard_1997_z"],
                categorical=categorical,
                binary=binary,
            )
            if row is not None:
                model_rows.append(row)

    transcript_rows: list[dict[str, float | int | str]] = []
    transcript_specs = [
        (
            "outcome_on_piat_design",
            ["piat_standard_1997_z", "age_months_1997"],
            ["asvab_test_month", "asvab_test_year"],
            [],
        ),
        (
            "outcome_on_piat_exposure",
            ["piat_standard_1997_z", "age_months_1997"],
            ["asvab_test_month", "asvab_test_year", "selfreport_highest_math_label"],
            [],
        ),
        (
            "outcome_on_piat_evaluation_stress",
            ["piat_standard_1997_z", "age_months_1997", "math_honors_depth_1997"],
            [
                "asvab_test_month",
                "asvab_test_year",
                "selfreport_highest_math_label",
                "avg_grade_recent",
                "grade_fall_1997",
            ],
            [],
        ),
        (
            "outcome_on_piat_offer_stress",
            ["piat_standard_1997_z", "age_months_1997"],
            [
                "asvab_test_month",
                "asvab_test_year",
                "selfreport_highest_math_label",
                "transcript_pr_sch_calc_hstr",
                "transcript_pr_sch_ap_hstr",
                "transcript_pr_sch_ib_hstr",
                "transcript_sch_pgm_hstr",
            ],
            [],
        ),
    ]
    for outcome in TRANSCRIPT_SURFACES:
        for model_name, continuous, categorical, binary in transcript_specs:
            row = fit_progression_model(
                frame,
                outcome=outcome,
                reference_surface="piat_standard_1997_z",
                sample_name="transcript_full",
                model_name=model_name,
                continuous=continuous,
                categorical=categorical,
                binary=binary,
            )
            if row is not None:
                transcript_rows.append(row)

    diag_rows: list[dict[str, float | int | str]] = []
    for column in [
        "transcript_prob_flag_hstr",
        "transcript_mathpipe_hstr",
        "selfreport_highest_math_1997",
        "transcript_pr_sch_calc_hstr",
        "transcript_pr_sch_ap_hstr",
        "transcript_pr_sch_ib_hstr",
    ]:
        counts = frame[column].value_counts(dropna=False).sort_index()
        for key, value in counts.items():
            diag_rows.append({"field": column, "value": "NaN" if pd.isna(key) else str(key), "n": int(value)})

    write_table(
        OUT_SURFACE,
        ["sample_name", "surface_name", "n_obs", "female_mean", "male_mean", "female_beta_sd", "ci_low", "ci_high", "p_value", "d_female_minus_male"],
        surface_rows,
    )
    write_table(
        OUT_BINARY,
        ["sample_name", "surface_name", "n_obs", "female_minus_male_share", "ci_low", "ci_high", "p_value"],
        binary_rows,
    )
    write_table(
        OUT_PIPE,
        ["sample_name", "group_col", "group_value", "surface_name", "n_obs", "female_mean", "male_mean", "d_female_minus_male"],
        pipe_rows,
    )
    write_table(
        OUT_HIGHEST,
        ["sample_name", "group_col", "group_value", "surface_name", "n_obs", "female_mean", "male_mean", "d_female_minus_male"],
        highest_rows,
    )
    write_table(
        OUT_MODELS,
        ["sample_name", "outcome", "reference_surface", "model_name", "n_obs", "n_female", "n_male", "female_beta_sd", "ci_low", "ci_high", "p_value", "n_controls"],
        model_rows,
    )
    write_table(
        OUT_TRANSCRIPT,
        ["sample_name", "outcome", "reference_surface", "model_name", "n_obs", "n_female", "n_male", "female_beta_sd", "ci_low", "ci_high", "p_value", "n_controls"],
        transcript_rows,
    )
    write_table(OUT_DIAG, ["field", "value", "n"], diag_rows)

    print(f"Wrote {OUT_EXTRACT}")
    print(f"Wrote {OUT_OVERLAP}")
    print(f"Wrote {OUT_SURFACE}")
    print(f"Wrote {OUT_BINARY}")
    print(f"Wrote {OUT_PIPE}")
    print(f"Wrote {OUT_HIGHEST}")
    print(f"Wrote {OUT_MODELS}")
    print(f"Wrote {OUT_TRANSCRIPT}")
    print(f"Wrote {OUT_DIAG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

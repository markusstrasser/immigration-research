#!/usr/bin/env python3
"""Canonical Add Health public school-surface pass.

Purpose:
- treat Add Health as a school-performance / evaluation-family replication
- use wave I parent background as the pre-treatment SES block
- keep CLUSTER2 as design structure for SEs, not as a fixed-effect control
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA = ROOT / "data" / "addhealth"

OUT_EXTRACT = DATA / "addhealth_school_surface_extract.parquet"
OUT_GRADE_GAPS = DATA / "addhealth_school_surface_grade_gaps.tsv"
OUT_PROFILE_GAPS = DATA / "addhealth_school_surface_relative_gaps.tsv"
OUT_OUTCOME_GAPS = DATA / "addhealth_school_surface_attainment_gaps.tsv"
OUT_PARENT_GAPS = DATA / "addhealth_school_surface_parent_background.tsv"
OUT_MODELS = DATA / "addhealth_school_surface_models.tsv"
OUT_JOINT = DATA / "addhealth_school_surface_joint_models.tsv"
OUT_GRADE_MODELS = DATA / "addhealth_school_surface_grade_models.tsv"
OUT_MATH_MODEL = DATA / "addhealth_school_surface_math_h4ed2_model.csv"
OUT_ENGLISH_MODEL = DATA / "addhealth_school_surface_english_h4ed2_model.csv"
OUT_JOINT_MODEL = DATA / "addhealth_school_surface_joint_h4ed2_model.csv"


def read_tsv(path: Path, cols: list[str]) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", usecols=cols, low_memory=False)


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def clean_grade(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    valid = values.where(values.isin([1, 2, 3, 4]))
    return 5 - valid


def clean_pvt(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where((values >= 1) & (values < 300))


def clean_h4ed2(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where((values >= 1) & (values <= 13))


def map_parent_education(series: pd.Series) -> pd.Series:
    """Approximate years-of-schooling map from Add Health parent education codes."""
    values = clean_numeric(series)
    mapping = {
        1: 8.0,
        2: 10.0,
        3: 11.0,
        4: 12.0,
        5: 12.0,
        6: 12.5,
        7: 14.0,
        8: 16.0,
        9: 18.0,
        10: 0.0,
    }
    return values.map(mapping)


def map_parent_professional(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.isin([1, 2, 3, 4]).astype(float).where(values.between(1, 16))


def map_parent_public_assist(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.map({0: 0.0, 1: 1.0})


def resident_parent_present(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where(values < 90).notna().astype(float)


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_gap(values: np.ndarray, female: np.ndarray, weights: np.ndarray) -> tuple[float, float, float]:
    positive = weights > 0
    values = values[positive]
    female = female[positive]
    weights = weights[positive]
    mask_f = female == 1
    mask_m = female == 0
    if mask_f.sum() == 0 or mask_m.sum() == 0:
        return math.nan, math.nan, math.nan
    vf, vm = values[mask_f], values[mask_m]
    wf, wm = weights[mask_f], weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    pooled = math.sqrt(max((weighted_var(vf, wf) + weighted_var(vm, wm)) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def summarize(df: pd.DataFrame, outcomes: list[str], weight_col: str, sample: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome in outcomes:
        work = df.dropna(subset=[outcome, "female", weight_col]).copy()
        work = work[work[weight_col] > 0].copy()
        if work.empty:
            continue
        mean_f, mean_m, d = weighted_gap(
            work[outcome].to_numpy(dtype=float),
            work["female"].to_numpy(dtype=int),
            work[weight_col].to_numpy(dtype=float),
        )
        rows.append(
            {
                "sample": sample,
                "outcome": outcome,
                "n": int(len(work)),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
            }
        )
    return pd.DataFrame(rows)


def fit_single_treatment_models(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    common_controls = (
        "female + age_w2 + pvtstd1 + parent_ed_max + any_parent_professional "
        "+ any_parent_public_assist + resident_mother + resident_father"
    )
    specs = [
        ("math_grade_points", OUT_MATH_MODEL),
        ("english_grade_points", OUT_ENGLISH_MODEL),
    ]
    for treatment, out_csv in specs:
        cols = [
            "h4ed2",
            treatment,
            "female",
            "age_w2",
            "pvtstd1",
            "parent_ed_max",
            "any_parent_professional",
            "any_parent_public_assist",
            "resident_mother",
            "resident_father",
            "cluster2",
            "analysis_weight_w4",
        ]
        work = df.dropna(subset=cols).copy()
        work = work[work["analysis_weight_w4"] > 0].copy()
        work.to_csv(out_csv, index=False)

        formula = f"h4ed2 ~ {treatment} + {common_controls}"
        model = smf.wls(formula, data=work, weights=work["analysis_weight_w4"]).fit(
            cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
        )
        coef = float(model.params[treatment])
        se = float(model.bse[treatment])
        rows.append(
            {
                "model_group": "single_treatment",
                "outcome": "h4ed2",
                "treatment": treatment,
                "n": int(model.nobs),
                "clusters": int(work["cluster2"].nunique()),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model.rsquared),
                "formula": formula,
                "weight": "analysis_weight_w4",
                "covariance": "cluster2",
            }
        )
    return pd.DataFrame(rows)


def fit_joint_model(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "h4ed2",
        "math_grade_points",
        "english_grade_points",
        "female",
        "age_w2",
        "pvtstd1",
        "parent_ed_max",
        "any_parent_professional",
        "any_parent_public_assist",
        "resident_mother",
        "resident_father",
        "cluster2",
        "analysis_weight_w4",
    ]
    work = df.dropna(subset=cols).copy()
    work = work[work["analysis_weight_w4"] > 0].copy()
    work.to_csv(OUT_JOINT_MODEL, index=False)
    formula = (
        "h4ed2 ~ math_grade_points + english_grade_points + female + age_w2 + pvtstd1 "
        "+ parent_ed_max + any_parent_professional + any_parent_public_assist "
        "+ resident_mother + resident_father"
    )
    model = smf.wls(formula, data=work, weights=work["analysis_weight_w4"]).fit(
        cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
    )
    rows = []
    for treatment in ["math_grade_points", "english_grade_points"]:
        coef = float(model.params[treatment])
        se = float(model.bse[treatment])
        rows.append(
            {
                "model_group": "joint_predictive",
                "outcome": "h4ed2",
                "treatment": treatment,
                "n": int(model.nobs),
                "clusters": int(work["cluster2"].nunique()),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model.rsquared),
                "formula": formula,
                "weight": "analysis_weight_w4",
                "covariance": "cluster2",
            }
        )
    return pd.DataFrame(rows)


def fit_grade_models(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    outcomes = ["math_grade_points", "english_grade_points", "math_minus_english"]
    controls = (
        "female + age_w2 + pvtstd1 + parent_ed_max + any_parent_professional "
        "+ any_parent_public_assist + resident_mother + resident_father"
    )
    for outcome in outcomes:
        cols = [
            outcome,
            "female",
            "age_w2",
            "pvtstd1",
            "parent_ed_max",
            "any_parent_professional",
            "any_parent_public_assist",
            "resident_mother",
            "resident_father",
            "cluster2",
            "w2_weight",
        ]
        work = df.dropna(subset=cols).copy()
        work = work[work["w2_weight"] > 0].copy()
        formula = f"{outcome} ~ {controls}"
        model = smf.wls(formula, data=work, weights=work["w2_weight"]).fit(
            cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
        )
        coef = float(model.params["female"])
        se = float(model.bse["female"])
        rows.append(
            {
                "model_group": "female_residual_grade_surface",
                "outcome": outcome,
                "term": "female",
                "n": int(model.nobs),
                "clusters": int(work["cluster2"].nunique()),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model.rsquared),
                "formula": formula,
                "weight": "w2_weight",
                "covariance": "cluster2",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    w1 = read_tsv(
        DATA / "wave1" / "w1inhome_dvn.tab",
        ["AID", "BIO_SEX", "H1RM1", "H1RF1", "H1RM4", "H1RF4", "H1RM9", "H1RF9"],
    ).rename(
        columns={
            "AID": "aid",
            "BIO_SEX": "bio_sex_w1",
            "H1RM1": "mom_ed_raw",
            "H1RF1": "dad_ed_raw",
            "H1RM4": "mom_occ_raw",
            "H1RF4": "dad_occ_raw",
            "H1RM9": "mom_public_assist_raw",
            "H1RF9": "dad_public_assist_raw",
        }
    )
    w2 = read_tsv(
        DATA / "wave2" / "w2inhome_dvn.tab",
        ["aid", "bio_sex2", "calcage2", "h2ed7", "h2ed8", "h2ed9", "h2ed10"],
    ).rename(
        columns={
            "aid": "aid",
            "bio_sex2": "bio_sex_w2",
            "calcage2": "age_w2",
            "h2ed7": "english_grade_raw",
            "h2ed8": "math_grade_raw",
            "h2ed9": "history_grade_raw",
            "h2ed10": "science_grade_raw",
        }
    )
    w2w = read_tsv(DATA / "wave2" / "w2weight.tab", ["AID", "CLUSTER2", "GSWGT2"]).rename(
        columns={"AID": "aid", "CLUSTER2": "cluster2", "GSWGT2": "w2_weight"}
    )
    pvt = read_tsv(DATA / "wave3" / "w3pvt_dvn.tab", ["AID", "PVTSTD1", "PVTSTD3C", "PVTSTD3L"]).rename(
        columns={"AID": "aid", "PVTSTD1": "pvtstd1", "PVTSTD3C": "pvtstd3c", "PVTSTD3L": "pvtstd3l"}
    )
    w4 = read_tsv(DATA / "wave4" / "w4inhome_dvn.tab", ["AID", "H4ED1", "H4ED2"]).rename(
        columns={"AID": "aid", "H4ED1": "h4ed1", "H4ED2": "h4ed2"}
    )
    w4w = read_tsv(DATA / "wave4" / "w4weight.tab", ["AID", "GSWGT4", "GSWGT4_2"]).rename(
        columns={"AID": "aid", "GSWGT4": "w4_weight", "GSWGT4_2": "w4_weight_2"}
    )

    df = w1.merge(w2, on="aid", how="inner")
    df = df.merge(w2w, on="aid", how="left")
    df = df.merge(pvt, on="aid", how="left")
    df = df.merge(w4, on="aid", how="left")
    df = df.merge(w4w, on="aid", how="left")

    df["female"] = clean_numeric(df["bio_sex_w2"]).map({1: 0, 2: 1})
    df["age_w2"] = clean_numeric(df["age_w2"]).where(lambda s: (s >= 11) & (s <= 25))
    df["english_grade_points"] = clean_grade(df["english_grade_raw"])
    df["math_grade_points"] = clean_grade(df["math_grade_raw"])
    df["history_grade_points"] = clean_grade(df["history_grade_raw"])
    df["science_grade_points"] = clean_grade(df["science_grade_raw"])
    df["pvtstd1"] = clean_pvt(df["pvtstd1"])
    df["pvtstd3c"] = clean_pvt(df["pvtstd3c"])
    df["pvtstd3l"] = clean_pvt(df["pvtstd3l"])
    df["h4ed1"] = clean_numeric(df["h4ed1"]).where(lambda s: s.isin([1, 2, 3, 4]))
    df["h4ed2"] = clean_h4ed2(df["h4ed2"])
    df["some_college_plus"] = (df["h4ed2"] >= 6).astype(float).where(df["h4ed2"].notna())
    df["bachelor_plus"] = (df["h4ed2"] >= 7).astype(float).where(df["h4ed2"].notna())
    df["w2_weight"] = clean_numeric(df["w2_weight"]).where(lambda s: s > 0)
    df["w4_weight"] = clean_numeric(df["w4_weight"]).where(lambda s: s > 0)
    df["w4_weight_2"] = clean_numeric(df["w4_weight_2"]).where(lambda s: s > 0)
    df["analysis_weight_w4"] = df["w4_weight_2"].fillna(df["w4_weight"])
    df["cluster2"] = clean_numeric(df["cluster2"])

    df["mother_ed_years"] = map_parent_education(df["mom_ed_raw"])
    df["father_ed_years"] = map_parent_education(df["dad_ed_raw"])
    df["parent_ed_max"] = df[["mother_ed_years", "father_ed_years"]].max(axis=1)
    df["parent_ed_min"] = df[["mother_ed_years", "father_ed_years"]].min(axis=1)
    df["resident_mother"] = resident_parent_present(df["mom_ed_raw"])
    df["resident_father"] = resident_parent_present(df["dad_ed_raw"])
    df["mother_professional"] = map_parent_professional(df["mom_occ_raw"])
    df["father_professional"] = map_parent_professional(df["dad_occ_raw"])
    df["any_parent_professional"] = df[["mother_professional", "father_professional"]].max(axis=1)
    df["mother_public_assist"] = map_parent_public_assist(df["mom_public_assist_raw"])
    df["father_public_assist"] = map_parent_public_assist(df["dad_public_assist_raw"])
    df["any_parent_public_assist"] = df[["mother_public_assist", "father_public_assist"]].max(axis=1)

    df["math_minus_english"] = df["math_grade_points"] - df["english_grade_points"]
    df["math_minus_history"] = df["math_grade_points"] - df["history_grade_points"]
    df["math_minus_science"] = df["math_grade_points"] - df["science_grade_points"]

    grade_gaps = summarize(
        df,
        ["english_grade_points", "math_grade_points", "history_grade_points", "science_grade_points"],
        "w2_weight",
        "wave2_grades",
    )
    profile_gaps = summarize(
        df,
        ["math_minus_english", "math_minus_history", "math_minus_science"],
        "w2_weight",
        "wave2_relative",
    )
    outcome_gaps = summarize(
        df,
        ["h4ed2", "some_college_plus", "bachelor_plus"],
        "analysis_weight_w4",
        "wave4_attainment",
    )
    parent_gaps = summarize(
        df,
        ["parent_ed_max", "resident_mother", "resident_father", "any_parent_professional", "any_parent_public_assist"],
        "w2_weight",
        "wave1_parent_background",
    )
    models = fit_single_treatment_models(df)
    joint = fit_joint_model(df)
    grade_models = fit_grade_models(df)

    df.to_parquet(OUT_EXTRACT, index=False)
    grade_gaps.to_csv(OUT_GRADE_GAPS, sep="\t", index=False)
    profile_gaps.to_csv(OUT_PROFILE_GAPS, sep="\t", index=False)
    outcome_gaps.to_csv(OUT_OUTCOME_GAPS, sep="\t", index=False)
    parent_gaps.to_csv(OUT_PARENT_GAPS, sep="\t", index=False)
    models.to_csv(OUT_MODELS, sep="\t", index=False)
    joint.to_csv(OUT_JOINT, sep="\t", index=False)
    grade_models.to_csv(OUT_GRADE_MODELS, sep="\t", index=False)

    print(f"wrote {OUT_EXTRACT}")
    print(f"wrote {OUT_GRADE_GAPS}")
    print(f"wrote {OUT_PROFILE_GAPS}")
    print(f"wrote {OUT_OUTCOME_GAPS}")
    print(f"wrote {OUT_PARENT_GAPS}")
    print(f"wrote {OUT_MODELS}")
    print(f"wrote {OUT_JOINT}")
    print(f"wrote {OUT_GRADE_MODELS}")


if __name__ == "__main__":
    main()

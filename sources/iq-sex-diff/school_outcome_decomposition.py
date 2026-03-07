#!/usr/bin/env python3
"""Descriptive school/outcome decomposition across public cohorts."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "school_outcome_decomposition"
ADDHEALTH_PATH = ROOT / "data" / "addhealth" / "addhealth_school_surface_extract.parquet"
FFCWS_PATH = ROOT / "data" / "ffcws" / "ffcws_achievement_extract.parquet"


def fit_addhealth() -> pd.DataFrame:
    df = pd.read_parquet(ADDHEALTH_PATH).copy()
    needed = [
        "h4ed2",
        "female",
        "age_w2",
        "parent_ed_max",
        "any_parent_professional",
        "any_parent_public_assist",
        "resident_mother",
        "resident_father",
        "pvtstd1",
        "math_grade_points",
        "english_grade_points",
        "analysis_weight_w4",
        "cluster2",
    ]
    work = df.dropna(subset=needed).copy()
    formulas = [
        ("bg_only", "h4ed2 ~ female + age_w2 + parent_ed_max + any_parent_professional + any_parent_public_assist + resident_mother + resident_father"),
        ("plus_pvt", "h4ed2 ~ female + age_w2 + parent_ed_max + any_parent_professional + any_parent_public_assist + resident_mother + resident_father + pvtstd1"),
        ("plus_math_grade", "h4ed2 ~ female + age_w2 + parent_ed_max + any_parent_professional + any_parent_public_assist + resident_mother + resident_father + pvtstd1 + math_grade_points"),
        ("plus_english_grade", "h4ed2 ~ female + age_w2 + parent_ed_max + any_parent_professional + any_parent_public_assist + resident_mother + resident_father + pvtstd1 + english_grade_points"),
        ("plus_both_grades", "h4ed2 ~ female + age_w2 + parent_ed_max + any_parent_professional + any_parent_public_assist + resident_mother + resident_father + pvtstd1 + math_grade_points + english_grade_points"),
    ]
    rows = []
    base_abs = None
    for model_name, formula in formulas:
        model = smf.wls(formula, data=work, weights=work["analysis_weight_w4"]).fit(
            cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
        )
        female_beta = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        if base_abs is None:
            base_abs = abs(female_beta)
        rows.append(
            {
                "cohort": "addhealth",
                "outcome": "h4ed2",
                "model_name": model_name,
                "n": int(model.nobs),
                "female_beta": female_beta,
                "female_ci_low": female_beta - 1.96 * se if pd.notna(se) else math.nan,
                "female_ci_high": female_beta + 1.96 * se if pd.notna(se) else math.nan,
                "female_pct_of_bg_only": abs(female_beta) / base_abs if base_abs else math.nan,
                "pvt_beta": model.params.get("pvtstd1", math.nan),
                "math_grade_beta": model.params.get("math_grade_points", math.nan),
                "english_grade_beta": model.params.get("english_grade_points", math.nan),
                "r_squared": float(model.rsquared),
            }
        )
    return pd.DataFrame(rows)


def fit_ffcws() -> pd.DataFrame:
    df = pd.read_parquet(FFCWS_PATH).copy()
    needed = [
        "college_years",
        "female",
        "ch5age_years",
        "cm1inpov",
        "mother_education_cat",
        "mother_race_cat",
        "family_structure",
        "ch5ppvt_z",
        "ch5wj9_z",
        "ch5wj10_z",
        "k7natwt",
    ]
    work = df.dropna(subset=needed).copy()
    formulas = [
        ("bg_only", "college_years ~ female + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure)"),
        ("plus_ppvt", "college_years ~ female + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure) + ch5ppvt_z"),
        ("plus_passage", "college_years ~ female + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure) + ch5wj9_z"),
        ("plus_applied", "college_years ~ female + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure) + ch5wj10_z"),
        ("plus_joint_battery", "college_years ~ female + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure) + ch5ppvt_z + ch5wj9_z + ch5wj10_z"),
    ]
    rows = []
    base_abs = None
    for model_name, formula in formulas:
        model = smf.wls(formula, data=work, weights=work["k7natwt"]).fit(cov_type="HC1")
        female_beta = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        if base_abs is None:
            base_abs = abs(female_beta)
        rows.append(
            {
                "cohort": "ffcws",
                "outcome": "college_years",
                "model_name": model_name,
                "n": int(model.nobs),
                "female_beta": female_beta,
                "female_ci_low": female_beta - 1.96 * se if pd.notna(se) else math.nan,
                "female_ci_high": female_beta + 1.96 * se if pd.notna(se) else math.nan,
                "female_pct_of_bg_only": abs(female_beta) / base_abs if base_abs else math.nan,
                "ppvt_beta": model.params.get("ch5ppvt_z", math.nan),
                "passage_beta": model.params.get("ch5wj9_z", math.nan),
                "applied_beta": model.params.get("ch5wj10_z", math.nan),
                "r_squared": float(model.rsquared),
            }
        )
    return pd.DataFrame(rows)


def build_summary(addhealth: pd.DataFrame, ffcws: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for frame in [addhealth, ffcws]:
        cohort = frame["cohort"].iat[0]
        base = frame.loc[frame["model_name"] == "bg_only", "female_beta"].iat[0]
        final = frame.iloc[-1]["female_beta"]
        rows.append(
            {
                "cohort": cohort,
                "base_female_beta": base,
                "final_female_beta": final,
                "attenuation_abs": abs(base) - abs(final),
                "attenuation_pct": 1.0 - (abs(final) / abs(base) if base else math.nan),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    addhealth = fit_addhealth()
    ffcws = fit_ffcws()
    summary = build_summary(addhealth, ffcws)
    addhealth.to_csv(DATA_DIR / "addhealth_attainment_decomposition.tsv", sep="\t", index=False)
    ffcws.to_csv(DATA_DIR / "ffcws_attainment_decomposition.tsv", sep="\t", index=False)
    summary.to_csv(DATA_DIR / "school_outcome_decomposition_summary.tsv", sep="\t", index=False)
    print("wrote decomposition outputs")


if __name__ == "__main__":
    main()

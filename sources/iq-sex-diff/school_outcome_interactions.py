#!/usr/bin/env python3
"""Predictive-validity interaction pass for school/test surfaces by sex."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "school_outcome_interactions"
ADDHEALTH_PATH = ROOT / "data" / "addhealth" / "addhealth_school_surface_extract.parquet"
FFCWS_PATH = ROOT / "data" / "ffcws" / "ffcws_achievement_extract.parquet"


def slope_summary(model, var: str, interaction: str | None = None) -> dict[str, float]:
    params = model.params
    cov = model.cov_params()

    male_beta = params.get(var, math.nan)
    male_var = cov.loc[var, var] if var in cov.index and var in cov.columns else math.nan
    male_se = math.sqrt(male_var) if pd.notna(male_var) and male_var >= 0 else math.nan

    if interaction and interaction in params.index:
        female_beta = params.get(var, 0.0) + params.get(interaction, 0.0)
        if var in cov.index and interaction in cov.index:
            female_var = (
                cov.loc[var, var]
                + cov.loc[interaction, interaction]
                + 2.0 * cov.loc[var, interaction]
            )
            female_se = math.sqrt(female_var) if female_var >= 0 else math.nan
        else:
            female_se = math.nan
        interaction_beta = params.get(interaction, math.nan)
        interaction_se = model.bse.get(interaction, math.nan)
    else:
        female_beta = male_beta
        female_se = male_se
        interaction_beta = math.nan
        interaction_se = math.nan

    return {
        "male_beta": male_beta,
        "male_ci_low": male_beta - 1.96 * male_se if pd.notna(male_se) else math.nan,
        "male_ci_high": male_beta + 1.96 * male_se if pd.notna(male_se) else math.nan,
        "female_beta": female_beta,
        "female_ci_low": female_beta - 1.96 * female_se if pd.notna(female_se) else math.nan,
        "female_ci_high": female_beta + 1.96 * female_se if pd.notna(female_se) else math.nan,
        "interaction_beta": interaction_beta,
        "interaction_ci_low": interaction_beta - 1.96 * interaction_se if pd.notna(interaction_se) else math.nan,
        "interaction_ci_high": interaction_beta + 1.96 * interaction_se if pd.notna(interaction_se) else math.nan,
    }


def fit_addhealth() -> pd.DataFrame:
    df = pd.read_parquet(ADDHEALTH_PATH).copy()
    controls = (
        "female + age_w2 + parent_ed_max + any_parent_professional + "
        "any_parent_public_assist + resident_mother + resident_father + pvtstd1"
    )
    specs = [
        ("math_grade", "math_grade_points"),
        ("english_grade", "english_grade_points"),
    ]
    rows = []
    for label, var in specs:
        needed = ["h4ed2", var, "analysis_weight_w4", "cluster2"] + [
            "female",
            "age_w2",
            "parent_ed_max",
            "any_parent_professional",
            "any_parent_public_assist",
            "resident_mother",
            "resident_father",
            "pvtstd1",
        ]
        work = df.dropna(subset=needed).copy()
        formula = f"h4ed2 ~ {controls} + {var} + female:{var}"
        model = smf.wls(formula, data=work, weights=work["analysis_weight_w4"]).fit(
            cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
        )
        interaction = f"female:{var}"
        out = {
            "cohort": "addhealth",
            "outcome": "h4ed2",
            "predictor": var,
            "model_name": label,
            "n": int(model.nobs),
            "r_squared": float(model.rsquared),
        }
        out.update(slope_summary(model, var, interaction))
        rows.append(out)
    return pd.DataFrame(rows)


def fit_ffcws() -> pd.DataFrame:
    df = pd.read_parquet(FFCWS_PATH).copy()
    controls = (
        "female + ch5age_years + cm1inpov + C(mother_education_cat) + "
        "C(mother_race_cat) + C(family_structure)"
    )
    specs = [
        ("applied", "ch5wj10_z"),
        ("passage", "ch5wj9_z"),
        ("ppvt", "ch5ppvt_z"),
    ]
    rows = []
    for label, var in specs:
        needed = ["college_years", var, "k7natwt"] + [
            "female",
            "ch5age_years",
            "cm1inpov",
            "mother_education_cat",
            "mother_race_cat",
            "family_structure",
        ]
        work = df.dropna(subset=needed).copy()
        formula = f"college_years ~ {controls} + {var} + female:{var}"
        model = smf.wls(formula, data=work, weights=work["k7natwt"]).fit(cov_type="HC1")
        interaction = f"female:{var}"
        out = {
            "cohort": "ffcws",
            "outcome": "college_years",
            "predictor": var,
            "model_name": label,
            "n": int(model.nobs),
            "r_squared": float(model.rsquared),
        }
        out.update(slope_summary(model, var, interaction))
        rows.append(out)
    return pd.DataFrame(rows)


def build_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in frame.itertuples(index=False):
        rows.append(
            {
                "cohort": row.cohort,
                "predictor": row.predictor,
                "male_beta": row.male_beta,
                "female_beta": row.female_beta,
                "female_minus_male_slope": row.female_beta - row.male_beta,
                "interaction_beta": row.interaction_beta,
                "interaction_ci_low": row.interaction_ci_low,
                "interaction_ci_high": row.interaction_ci_high,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    addhealth = fit_addhealth()
    ffcws = fit_ffcws()
    all_rows = pd.concat([addhealth, ffcws], ignore_index=True)
    summary = build_summary(all_rows)
    addhealth.to_csv(DATA_DIR / "addhealth_outcome_interactions.tsv", sep="\t", index=False)
    ffcws.to_csv(DATA_DIR / "ffcws_outcome_interactions.tsv", sep="\t", index=False)
    summary.to_csv(DATA_DIR / "school_outcome_interactions_summary.tsv", sep="\t", index=False)
    print("wrote interaction outputs")


if __name__ == "__main__":
    main()

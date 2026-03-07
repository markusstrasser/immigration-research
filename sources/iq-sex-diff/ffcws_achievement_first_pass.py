#!/usr/bin/env python3
"""First FFCWS achievement and transition pass.

Purpose:
- test whether the math-versus-verbal geometry survives in a different cohort
- keep the first pass narrow enough to be inspectable
- separate descriptive sex-gap surfaces from a small observed-confounder
  transition model using Year 9 child scores and Year 22 college exposure
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA = ROOT / "data" / "ffcws" / "ICPSR_31622" / "DS0001"
OUTDIR = ROOT / "data" / "ffcws"

DATA_FILE = DATA / "31622-0001-Data.dta"
OUT_EXTRACT = OUTDIR / "ffcws_achievement_extract.parquet"
OUT_Y9_GAPS = OUTDIR / "ffcws_y9_surface_gaps.tsv"
OUT_Y9_REL = OUTDIR / "ffcws_y9_relative_gaps.tsv"
OUT_Y22_GAPS = OUTDIR / "ffcws_y22_transition_gaps.tsv"
OUT_MODELS = OUTDIR / "ffcws_y9_surface_models.tsv"
OUT_TRANSITION = OUTDIR / "ffcws_transition_models.tsv"
OUT_JOINT = OUTDIR / "ffcws_transition_joint_models.tsv"
OUT_WEIGHTED_JOINT = OUTDIR / "ffcws_transition_weighted_joint_models.tsv"
OUT_APPLIED_MODEL = OUTDIR / "ffcws_transition_applied_model.csv"
OUT_PPVT_MODEL = OUTDIR / "ffcws_transition_ppvt_model.csv"
OUT_PASSAGE_MODEL = OUTDIR / "ffcws_transition_passage_model.csv"
OUT_DIGIT_MODEL = OUTDIR / "ffcws_transition_digit_model.csv"


NEGATIVE_MISSING = {-9, -8, -7, -6, -5, -4, -3, -2, -1, 999, 9999, 99999}


def clean_numeric(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return values.where(~values.isin(NEGATIVE_MISSING))


def clean_binary(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where(values.isin([0, 1]))


def standardize(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    mean = values.mean()
    std = values.std(ddof=0)
    if pd.isna(std) or std == 0:
        return pd.Series(np.nan, index=series.index)
    return (values - mean) / std


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def effect_size(values: np.ndarray, female: np.ndarray, weights: np.ndarray | None = None) -> tuple[float, float, float]:
    mask_f = female == 1
    mask_m = female == 0
    if mask_f.sum() == 0 or mask_m.sum() == 0:
        return math.nan, math.nan, math.nan
    vf, vm = values[mask_f], values[mask_m]
    if weights is None:
        mean_f = float(np.mean(vf))
        mean_m = float(np.mean(vm))
        pooled = math.sqrt(max((float(np.var(vf)) + float(np.var(vm))) / 2.0, 0.0))
    else:
        wf, wm = weights[mask_f], weights[mask_m]
        mean_f = weighted_mean(vf, wf)
        mean_m = weighted_mean(vm, wm)
        pooled = math.sqrt(max((weighted_var(vf, wf) + weighted_var(vm, wm)) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def summarize(df: pd.DataFrame, outcomes: list[str], sample: str, weight_col: str | None = None) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome in outcomes:
        cols = [outcome, "female"]
        if weight_col is not None:
            cols.append(weight_col)
        work = df.dropna(subset=cols).copy()
        weights = None
        if weight_col is not None:
            work = work[work[weight_col] > 0].copy()
            weights = work[weight_col].to_numpy(dtype=float)
        if work.empty:
            continue
        mean_f, mean_m, d = effect_size(
            work[outcome].to_numpy(dtype=float),
            work["female"].to_numpy(dtype=int),
            weights,
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


def fit_surface_models(df: pd.DataFrame, outcomes: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    controls = "female + ch5age_years + C(mother_education_cat) + cm1inpov + C(mother_race_cat) + C(family_structure)"
    for outcome in outcomes:
        work = df.dropna(
            subset=[outcome, "female", "ch5age_years", "mother_education_cat", "cm1inpov", "mother_race_cat", "family_structure"]
        ).copy()
        formula = f"{outcome} ~ {controls}"
        model = smf.ols(formula, data=work).fit(cov_type="HC3")
        coef = float(model.params["female"])
        se = float(model.bse["female"])
        rows.append(
            {
                "model_group": "adjusted_surface",
                "outcome": outcome,
                "treatment": "female",
                "n": int(model.nobs),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model.rsquared),
                "formula": formula,
                "covariance": "HC3",
            }
        )
    return pd.DataFrame(rows)


def fit_transition_models(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    csv_map = {
        "ch5wj10_z": OUT_APPLIED_MODEL,
        "ch5ppvt_z": OUT_PPVT_MODEL,
        "ch5wj9_z": OUT_PASSAGE_MODEL,
        "ch5ds_z": OUT_DIGIT_MODEL,
    }
    controls = "female + ch5age_years + C(mother_education_cat) + cm1inpov + C(mother_race_cat) + C(family_structure)"
    base_cols = [
        "college_years",
        "female",
        "ch5age_years",
        "mother_education_cat",
        "cm1inpov",
        "mother_race_cat",
        "family_structure",
    ]
    for treatment, out_csv in csv_map.items():
        cols = base_cols + [treatment]
        work = df.dropna(subset=cols).copy()
        work.to_csv(out_csv, index=False)
        formula = f"college_years ~ {treatment} + {controls}"
        model = smf.ols(formula, data=work).fit(cov_type="HC3")
        coef = float(model.params[treatment])
        se = float(model.bse[treatment])
        rows.append(
            {
                "model_group": "single_score_transition",
                "outcome": "college_years",
                "treatment": treatment,
                "n": int(model.nobs),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model.rsquared),
                "formula": formula,
                "covariance": "HC3",
            }
        )

    work_joint = df.dropna(subset=base_cols + ["ch5wj10_z", "ch5ppvt_z", "ch5wj9_z", "ch5ds_z"]).copy()
    formula_joint = (
        "college_years ~ ch5wj10_z + ch5ppvt_z + ch5wj9_z + ch5ds_z + "
        f"{controls}"
    )
    model_joint = smf.ols(formula_joint, data=work_joint).fit(cov_type="HC3")
    joint_rows = []
    for treatment in ["female", "ch5wj10_z", "ch5ppvt_z", "ch5wj9_z", "ch5ds_z"]:
        coef = float(model_joint.params[treatment])
        se = float(model_joint.bse[treatment])
        joint_rows.append(
            {
                "model_group": "joint_score_transition",
                "outcome": "college_years",
                "treatment": treatment,
                "n": int(model_joint.nobs),
                "estimate": coef,
                "se": se,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
                "r_squared": float(model_joint.rsquared),
                "formula": formula_joint,
                "covariance": "HC3",
            }
        )
    work_weighted = work_joint.dropna(subset=["k7natwt"]).copy()
    work_weighted = work_weighted[work_weighted["k7natwt"] > 0].copy()
    weighted_rows = []
    if not work_weighted.empty:
        model_weighted = smf.wls(
            formula_joint,
            data=work_weighted,
            weights=work_weighted["k7natwt"],
        ).fit(cov_type="HC1")
        for treatment in ["female", "ch5wj10_z", "ch5ppvt_z", "ch5wj9_z", "ch5ds_z"]:
            coef = float(model_weighted.params[treatment])
            se = float(model_weighted.bse[treatment])
            weighted_rows.append(
                {
                    "model_group": "weighted_joint_score_transition",
                    "outcome": "college_years",
                    "treatment": treatment,
                    "n": int(model_weighted.nobs),
                    "estimate": coef,
                    "se": se,
                    "ci_low": coef - 1.96 * se,
                    "ci_high": coef + 1.96 * se,
                    "r_squared": float(model_weighted.rsquared),
                    "formula": formula_joint,
                    "weight": "k7natwt",
                    "covariance": "HC1",
                }
            )
    return pd.DataFrame(rows), pd.DataFrame(joint_rows), pd.DataFrame(weighted_rows)


def main() -> None:
    cols = [
        "CM1BSEX",
        "CM1EDU",
        "CM1INPOV",
        "CM1ETHRACE",
        "CM1MARF",
        "CM1COHF",
        "CH5AGEM",
        "CH5PPVTSS",
        "CH5WJ9SS",
        "CH5WJ10SS",
        "CH5DSSS",
        "P5NATWT",
        "K7NATWT",
        "K7B2",
        "K7B45",
        "K7B55",
        "K7B56",
        "K7B76_1",
        "K7B77_1",
    ]
    df = pd.read_stata(DATA_FILE, columns=cols, convert_categoricals=False)

    df["female"] = clean_numeric(df["CM1BSEX"]).map({1: 0.0, 2: 1.0})
    df["cm1inpov"] = clean_numeric(df["CM1INPOV"])
    df["ch5age_years"] = clean_numeric(df["CH5AGEM"]) / 12.0
    df["p5natwt"] = clean_numeric(df["P5NATWT"])
    df["k7natwt"] = clean_numeric(df["K7NATWT"])

    edu_map = {1: "lt_hs", 2: "hs", 3: "some_college", 4: "college_plus"}
    race_map = {1: "white_nonhisp", 2: "black_nonhisp", 3: "hispanic", 4: "other"}
    marf = clean_binary(df["CM1MARF"])
    cohf = clean_binary(df["CM1COHF"])

    df["mother_education_cat"] = clean_numeric(df["CM1EDU"]).map(edu_map)
    df["mother_race_cat"] = clean_numeric(df["CM1ETHRACE"]).map(race_map)
    df["family_structure"] = np.where(
        marf == 1,
        "married_to_father",
        np.where(cohf == 1, "cohab_with_father", "other"),
    )
    df["family_structure"] = pd.Series(df["family_structure"]).where(~(marf.isna() & cohf.isna()))

    # Same-wave child achievement surfaces.
    df["ch5ppvtss"] = clean_numeric(df["CH5PPVTSS"])
    df["ch5wj9ss"] = clean_numeric(df["CH5WJ9SS"])
    df["ch5wj10ss"] = clean_numeric(df["CH5WJ10SS"])
    df["ch5dsss"] = clean_numeric(df["CH5DSSS"])

    df["ch5ppvt_z"] = standardize(df["ch5ppvtss"])
    df["ch5wj9_z"] = standardize(df["ch5wj9ss"])
    df["ch5wj10_z"] = standardize(df["ch5wj10ss"])
    df["ch5ds_z"] = standardize(df["ch5dsss"])

    df["applied_minus_passage"] = df["ch5wj10_z"] - df["ch5wj9_z"]
    df["applied_minus_ppvt"] = df["ch5wj10_z"] - df["ch5ppvt_z"]
    df["applied_minus_mean_verbal"] = df["ch5wj10_z"] - df[["ch5ppvt_z", "ch5wj9_z"]].mean(axis=1)
    df["passage_minus_ppvt"] = df["ch5wj9_z"] - df["ch5ppvt_z"]

    # Transition surfaces.
    df["college_years"] = clean_numeric(df["K7B2"]).where(lambda s: s.between(0, 6))
    k7b45 = clean_numeric(df["K7B45"])
    df["ever_college"] = k7b45.map({1: 1.0, 2: 0.0})
    df["current_gpa"] = clean_numeric(df["K7B55"]).where(lambda s: s.between(0, 7))
    df["highest_gpa"] = clean_numeric(df["K7B56"]).where(lambda s: s.between(0, 7))
    first_gpa = clean_numeric(df["K7B76_1"]).where(lambda s: s.between(0, 7))
    first_scale = clean_numeric(df["K7B77_1"]).where(lambda s: s > 0)
    df["first_college_gpa_norm"] = (first_gpa / first_scale).where(first_scale.notna())

    keep = [
        "female",
        "cm1inpov",
        "ch5age_years",
        "mother_education_cat",
        "mother_race_cat",
        "family_structure",
        "p5natwt",
        "k7natwt",
        "ch5ppvtss",
        "ch5wj9ss",
        "ch5wj10ss",
        "ch5dsss",
        "ch5ppvt_z",
        "ch5wj9_z",
        "ch5wj10_z",
        "ch5ds_z",
        "applied_minus_passage",
        "applied_minus_ppvt",
        "applied_minus_mean_verbal",
        "passage_minus_ppvt",
        "college_years",
        "ever_college",
        "current_gpa",
        "highest_gpa",
        "first_college_gpa_norm",
    ]
    out = df[keep].copy()
    out.to_parquet(OUT_EXTRACT, index=False)

    y9_surfaces = ["ch5ppvtss", "ch5wj9ss", "ch5wj10ss", "ch5dsss"]
    rel_surfaces = ["applied_minus_passage", "applied_minus_ppvt", "applied_minus_mean_verbal", "passage_minus_ppvt"]
    y22_surfaces = ["college_years", "ever_college", "current_gpa", "highest_gpa", "first_college_gpa_norm"]

    pd.concat(
        [
            summarize(out, y9_surfaces, "unweighted"),
            summarize(out, y9_surfaces, "p5natwt", "p5natwt"),
        ],
        ignore_index=True,
    ).to_csv(OUT_Y9_GAPS, sep="\t", index=False)

    pd.concat(
        [
            summarize(out, rel_surfaces, "unweighted"),
            summarize(out, rel_surfaces, "p5natwt", "p5natwt"),
        ],
        ignore_index=True,
    ).to_csv(OUT_Y9_REL, sep="\t", index=False)

    pd.concat(
        [
            summarize(out, y22_surfaces, "unweighted"),
            summarize(out, y22_surfaces, "k7natwt", "k7natwt"),
        ],
        ignore_index=True,
    ).to_csv(OUT_Y22_GAPS, sep="\t", index=False)

    fit_surface_models(out, y9_surfaces + rel_surfaces).to_csv(OUT_MODELS, sep="\t", index=False)
    transition, joint, weighted_joint = fit_transition_models(out)
    transition.to_csv(OUT_TRANSITION, sep="\t", index=False)
    joint.to_csv(OUT_JOINT, sep="\t", index=False)
    weighted_joint.to_csv(OUT_WEIGHTED_JOINT, sep="\t", index=False)


if __name__ == "__main__":
    main()

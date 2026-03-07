#!/usr/bin/env python3
"""First pass on public Add Health school-grade and attainment surfaces."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA = ROOT / "data" / "addhealth"

OUT_EXTRACT = DATA / "addhealth_first_pass_extract.parquet"
OUT_GRADE_GAPS = DATA / "addhealth_subject_grade_gaps.tsv"
OUT_PROFILE_GAPS = DATA / "addhealth_relative_profile_gaps.tsv"
OUT_OUTCOME_GAPS = DATA / "addhealth_attainment_gaps.tsv"
OUT_MODELS = DATA / "addhealth_attainment_models.tsv"
OUT_MATH_MODEL = DATA / "addhealth_mathgrade_h4ed2_model_data.csv"
OUT_ENGLISH_MODEL = DATA / "addhealth_englishgrade_h4ed2_model_data.csv"


def read_tsv(path: Path, cols: list[str]) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", usecols=cols, low_memory=False)


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def clean_grade(series: pd.Series) -> pd.Series:
    """Map Add Health A/B/C/D coding to 4/3/2/1 points, drop non-graded codes."""
    values = clean_numeric(series)
    valid = values.where(values.isin([1, 2, 3, 4]))
    return 5 - valid


def clean_pvt(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where((values >= 1) & (values < 300))


def clean_h4ed2(series: pd.Series) -> pd.Series:
    values = clean_numeric(series)
    return values.where((values >= 1) & (values <= 13))


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


def fit_models(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    specs = [
        ("math_grade_points", OUT_MATH_MODEL),
        ("english_grade_points", OUT_ENGLISH_MODEL),
    ]
    for treatment, out_csv in specs:
        cols = ["h4ed2", treatment, "female", "age_w2", "pvtstd1", "cluster2", "analysis_weight_w4"]
        work = df.dropna(subset=cols).copy()
        work = work[work["analysis_weight_w4"] > 0].copy()
        # keep only clusters with at least 2 respondents for cluster-robust covariance
        counts = work.groupby("cluster2")["aid"].transform("count")
        work = work[counts >= 2].copy()
        work.to_csv(out_csv, index=False)

        formula = f"h4ed2 ~ {treatment} + female + age_w2 + pvtstd1 + C(cluster2)"
        model = smf.wls(formula, data=work, weights=work["analysis_weight_w4"]).fit(
            cov_type="cluster", cov_kwds={"groups": work["cluster2"]}
        )
        coef = float(model.params[treatment])
        se = float(model.bse[treatment])
        rows.append(
            {
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
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    w2 = read_tsv(
        DATA / "wave2" / "w2inhome_dvn.tab",
        ["aid", "bio_sex2", "calcage2", "h2ed7", "h2ed8", "h2ed9", "h2ed10"],
    ).rename(
        columns={
            "aid": "aid",
            "bio_sex2": "bio_sex",
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

    df = w2.merge(w2w, on="aid", how="left")
    df = df.merge(pvt, on="aid", how="left")
    df = df.merge(w4, on="aid", how="left")
    df = df.merge(w4w, on="aid", how="left")

    df["female"] = clean_numeric(df["bio_sex"]).map({1: 0, 2: 1})
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
    models = fit_models(df)

    df.to_parquet(OUT_EXTRACT, index=False)
    grade_gaps.to_csv(OUT_GRADE_GAPS, sep="\t", index=False)
    profile_gaps.to_csv(OUT_PROFILE_GAPS, sep="\t", index=False)
    outcome_gaps.to_csv(OUT_OUTCOME_GAPS, sep="\t", index=False)
    models.to_csv(OUT_MODELS, sep="\t", index=False)

    print(f"wrote {OUT_EXTRACT}")
    print(f"wrote {OUT_GRADE_GAPS}")
    print(f"wrote {OUT_PROFILE_GAPS}")
    print(f"wrote {OUT_OUTCOME_GAPS}")
    print(f"wrote {OUT_MODELS}")


if __name__ == "__main__":
    main()

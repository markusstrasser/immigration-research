#!/usr/bin/env python3
"""NLSY97 same-cohort PIAT Math versus CAT-ASVAB quantitative surface audit."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from nlsy97_stats_pipeline import fit_weighted_gap, pooled_weighted_sd, standardize_scores, load_frame
from stage0_config import NLSY97


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"

EXTRA_FIELDS = {
    "age_months_1997": {"code": "R1193900", "kind": "continuous"},
    "piat_percentile_1997": {"code": "R1210700", "kind": "continuous"},
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
    "transcript_gpa_hstr": {"code": "R9792900", "kind": "continuous"},
    "transcript_mathpipe_hstr": {"code": "R9860200", "kind": "continuous"},
    "transcript_total_math_hstr": {"code": "R9864300", "kind": "continuous"},
    "transcript_total_advanced_math_hstr": {"code": "R9864600", "kind": "continuous"},
    "transcript_pr_sch_ap_hstr": {"code": "R9870300", "kind": "categorical"},
    "transcript_gpa_overall_hstr": {"code": "R9871900", "kind": "continuous"},
    "transcript_gpa_math_hstr": {"code": "R9872200", "kind": "continuous"},
    "transcript_ap_calc_hstr": {"code": "R9794200", "kind": "continuous"},
    "piat_grade_gate_1997": {"code": "R0515300", "kind": "categorical"},
}

SURFACE_SPECS = {
    "piat_standard_1997": {"z_name": "piat_standard_1997_z", "scale": 1.0},
    "piat_percentile_1997": {"z_name": "piat_percentile_1997_z", "scale": 1.0},
    "transcript_gpa_hstr": {"z_name": "transcript_gpa_hstr_z", "scale": 100.0},
    "transcript_gpa_overall_hstr": {
        "z_name": "transcript_gpa_overall_hstr_z",
        "scale": 100.0,
    },
    "transcript_gpa_math_hstr": {"z_name": "transcript_gpa_math_hstr_z", "scale": 100.0},
    "transcript_mathpipe_hstr": {"z_name": "transcript_mathpipe_hstr_z", "scale": 100.0},
    "transcript_total_math_hstr": {"z_name": "transcript_total_math_hstr_z", "scale": 100.0},
    "transcript_total_advanced_math_hstr": {
        "z_name": "transcript_total_advanced_math_hstr_z",
        "scale": 100.0,
    },
}

PRIMARY_SURFACES = [
    "piat_standard_1997_z",
    "arithmetic_reasoning_z",
    "math_knowledge_z",
    "quantitative_z",
]

TRANSCRIPT_SURFACES = [
    "transcript_gpa_math_hstr_z",
    "transcript_mathpipe_hstr_z",
    "transcript_total_math_hstr_z",
    "transcript_total_advanced_math_hstr_z",
]

DESIGN_CONTINUOUS = ["age_months_1997"]
DESIGN_CATEGORICAL = ["asvab_test_year", "asvab_test_month"]


def clean_extra_fields(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()

    # Transcript and PIAT created variables use additional negative codes beyond the
    # standard interview missing values handled by the base loader.
    for column, spec in SURFACE_SPECS.items():
        frame[column] = frame[column].where(frame[column] >= 0)
        scale = float(spec["scale"])
        if scale != 1.0:
            frame[column] = frame[column] / scale

    frame["age_months_1997"] = frame["age_months_1997"].where(frame["age_months_1997"] >= 0)
    frame["asvab_test_year"] = frame["asvab_test_year"].where(frame["asvab_test_year"] >= 0)
    frame["asvab_test_month"] = frame["asvab_test_month"].where(frame["asvab_test_month"] >= 0)
    frame["avg_grade_recent"] = frame["avg_grade_recent"].where(frame["avg_grade_recent"] >= 0)
    frame["grade_fall_1997"] = frame["grade_fall_1997"].where(frame["grade_fall_1997"] >= 0)
    frame["transcript_pr_sch_ap_hstr"] = frame["transcript_pr_sch_ap_hstr"].where(
        frame["transcript_pr_sch_ap_hstr"] >= 0
    )
    frame["transcript_ap_calc_hstr"] = frame["transcript_ap_calc_hstr"].where(
        frame["transcript_ap_calc_hstr"] >= 0
    )
    frame["piat_grade_gate_1997"] = frame["piat_grade_gate_1997"].where(frame["piat_grade_gate_1997"] >= 0)

    honors_cols = [f"math_honors_{idx}" for idx in range(1, 7)]
    honors = frame[honors_cols].copy()
    for column in honors_cols:
        honors[column] = honors[column].where(honors[column] >= 0)
    honors_any = pd.Series(np.nan, index=frame.index, dtype=float)
    any_observed = honors.notna().any(axis=1)
    honors_any.loc[any_observed] = 0.0
    honors_any.loc[(honors == 1).any(axis=1)] = 1.0
    frame["math_honors_any_1997"] = honors_any

    frame["transcript_ap_calc_any_hstr"] = np.where(
        frame["transcript_ap_calc_hstr"].notna(),
        (frame["transcript_ap_calc_hstr"] > 0).astype(float),
        np.nan,
    )
    return frame


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


def prepare_design(
    sample: pd.DataFrame,
    continuous: list[str],
    categorical: list[str],
    include_female: bool = True,
) -> pd.DataFrame:
    design = pd.DataFrame(index=sample.index)
    if include_female:
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


def summarize_surface_gap(
    frame: pd.DataFrame,
    surface_name: str,
    sample_label: str,
) -> dict[str, float | int | str] | None:
    result = fit_weighted_gap(frame, surface_name)
    if result is None:
        return None
    return {
        "sample_label": sample_label,
        "surface_name": surface_name.removesuffix("_z"),
        "n_obs": int(result["n_obs"]),
        "female_beta_sd": float(result["beta_sd"]),
        "ci_low": float(result["ci_low"]),
        "ci_high": float(result["ci_high"]),
        "p_value": float(result["p_value"]),
    }


def binary_share_gap(
    frame: pd.DataFrame,
    surface_name: str,
    sample_label: str,
) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[surface_name].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", surface_name]].copy()
    if len(sample) < 100:
        return None
    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    design = sm.add_constant(sample[["female"]], has_constant="add")
    fit = sm.WLS(sample[surface_name], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "sample_label": sample_label,
        "surface_name": surface_name,
        "n_obs": int(fit.nobs),
        "female_minus_male_share": float(fit.params["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
    }


def fit_overlap_model(
    frame: pd.DataFrame,
    outcome: str,
    model_name: str,
    continuous: list[str],
    categorical: list[str],
) -> dict[str, float | int | str] | None:
    required = ["sex", "weight_1997", outcome] + continuous + categorical
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
    design = prepare_design(sample, continuous=continuous, categorical=categorical)
    fit = sm.WLS(sample[outcome], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "outcome": outcome.removesuffix("_z"),
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


def fit_cross_surface_model(
    frame: pd.DataFrame,
    outcome: str,
    reference_surface: str,
    model_name: str,
) -> dict[str, float | int | str] | None:
    required = [
        "sex",
        "weight_1997",
        outcome,
        reference_surface,
        "age_months_1997",
    ]
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
    )
    for column in required + DESIGN_CATEGORICAL:
        valid &= frame[column].notna()

    sample = frame.loc[valid, required + DESIGN_CATEGORICAL].copy()
    if len(sample) < 100:
        return None

    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    design = prepare_design(
        sample,
        continuous=[reference_surface, "age_months_1997"],
        categorical=DESIGN_CATEGORICAL,
    )
    fit = sm.WLS(sample[outcome], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    ref_low, ref_high = fit.conf_int().loc[reference_surface]
    return {
        "outcome": outcome.removesuffix("_z"),
        "model_name": model_name,
        "reference_surface": reference_surface.removesuffix("_z"),
        "n_obs": int(fit.nobs),
        "n_female": int(sample["female"].sum()),
        "n_male": int((1.0 - sample["female"]).sum()),
        "female_beta_sd": float(fit.params["female"]),
        "female_ci_low": float(low),
        "female_ci_high": float(high),
        "reference_beta_sd": float(fit.params[reference_surface]),
        "reference_ci_low": float(ref_low),
        "reference_ci_high": float(ref_high),
        "p_value_female": float(fit.pvalues["female"]),
        "n_controls": int(design.shape[1] - 2),
    }


def write_table(path: Path, fieldnames: list[str], rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print("Loading NLSY97 with PIAT and transcript extras...")
    frame, _ = load_frame(extra_fields=EXTRA_FIELDS)
    frame = clean_extra_fields(frame)
    frame, _ = standardize_scores(frame)
    for source_name, spec in SURFACE_SPECS.items():
        frame = standardize_extra_surface(frame, source_name, spec["z_name"])

    extract_path = DATA_DIR / "nlsy97_piat_cat_extract.parquet"
    frame.reset_index().to_parquet(extract_path, index=False)

    overlap_valid = (
        frame["piat_standard_1997_z"].notna()
        & frame["quantitative_z"].notna()
        & frame["age_months_1997"].notna()
        & frame["asvab_test_year"].notna()
        & frame["asvab_test_month"].notna()
        & frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
    )
    overlap = frame.loc[overlap_valid].copy()
    overlap_path = DATA_DIR / "nlsy97_piat_cat_overlap_extract.parquet"
    overlap.reset_index().to_parquet(overlap_path, index=False)

    surface_rows: list[dict[str, float | int | str]] = []
    for surface in PRIMARY_SURFACES + TRANSCRIPT_SURFACES:
        row = summarize_surface_gap(frame, surface, "full_valid")
        if row is not None:
            surface_rows.append(row)
        overlap_row = summarize_surface_gap(overlap, surface, "piat_cat_overlap")
        if overlap_row is not None:
            surface_rows.append(overlap_row)

    honors_rows = []
    for sample_label, sample_frame in [("full_valid", frame), ("piat_cat_overlap", overlap)]:
        honors = binary_share_gap(sample_frame, "math_honors_any_1997", sample_label)
        if honors is not None:
            honors_rows.append(honors)
        ap = binary_share_gap(sample_frame, "transcript_ap_calc_any_hstr", sample_label)
        if ap is not None:
            honors_rows.append(ap)

    model_rows: list[dict[str, float | int | str]] = []
    for outcome in PRIMARY_SURFACES:
        base = fit_overlap_model(overlap, outcome, "base_overlap", continuous=[], categorical=[])
        if base is not None:
            model_rows.append(base)
        design = fit_overlap_model(
            overlap,
            outcome,
            "design_overlap",
            continuous=DESIGN_CONTINUOUS,
            categorical=DESIGN_CATEGORICAL,
        )
        if design is not None:
            model_rows.append(design)

    cross_surface_rows: list[dict[str, float | int | str]] = []
    for outcome in ["quantitative_z", "arithmetic_reasoning_z", "math_knowledge_z"]:
        row = fit_cross_surface_model(
            overlap,
            outcome=outcome,
            reference_surface="piat_standard_1997_z",
            model_name="conditional_on_piat",
        )
        if row is not None:
            cross_surface_rows.append(row)

    row = fit_cross_surface_model(
        overlap,
        outcome="piat_standard_1997_z",
        reference_surface="quantitative_z",
        model_name="conditional_on_quantitative",
    )
    if row is not None:
        cross_surface_rows.append(row)

    transcript_rows: list[dict[str, float | int | str]] = []
    for outcome in TRANSCRIPT_SURFACES:
        row = fit_cross_surface_model(
            frame,
            outcome=outcome,
            reference_surface="piat_standard_1997_z",
            model_name="transcript_conditional_on_piat",
        )
        if row is not None:
            transcript_rows.append(row)
        row = fit_cross_surface_model(
            frame,
            outcome=outcome,
            reference_surface="quantitative_z",
            model_name="transcript_conditional_on_quantitative",
        )
        if row is not None:
            transcript_rows.append(row)

    write_table(
        DATA_DIR / "nlsy97_piat_cat_surface_gaps.tsv",
        ["sample_label", "surface_name", "n_obs", "female_beta_sd", "ci_low", "ci_high", "p_value"],
        surface_rows,
    )
    write_table(
        DATA_DIR / "nlsy97_piat_cat_binary_surfaces.tsv",
        [
            "sample_label",
            "surface_name",
            "n_obs",
            "female_minus_male_share",
            "ci_low",
            "ci_high",
            "p_value",
        ],
        honors_rows,
    )
    write_table(
        DATA_DIR / "nlsy97_piat_cat_models.tsv",
        [
            "outcome",
            "model_name",
            "n_obs",
            "n_female",
            "n_male",
            "female_beta_sd",
            "ci_low",
            "ci_high",
            "p_value",
            "n_controls",
        ],
        model_rows,
    )
    write_table(
        DATA_DIR / "nlsy97_piat_cat_cross_surface.tsv",
        [
            "outcome",
            "model_name",
            "reference_surface",
            "n_obs",
            "n_female",
            "n_male",
            "female_beta_sd",
            "female_ci_low",
            "female_ci_high",
            "reference_beta_sd",
            "reference_ci_low",
            "reference_ci_high",
            "p_value_female",
            "n_controls",
        ],
        cross_surface_rows,
    )
    write_table(
        DATA_DIR / "nlsy97_piat_cat_transcript_models.tsv",
        [
            "outcome",
            "model_name",
            "reference_surface",
            "n_obs",
            "n_female",
            "n_male",
            "female_beta_sd",
            "female_ci_low",
            "female_ci_high",
            "reference_beta_sd",
            "reference_ci_low",
            "reference_ci_high",
            "p_value_female",
            "n_controls",
        ],
        transcript_rows,
    )

    print(f"Wrote {extract_path}")
    print(f"Wrote {overlap_path}")
    print(f"PIAT/CAT overlap n={len(overlap):,}")
    for row in surface_rows:
        if row["sample_label"] == "piat_cat_overlap" and row["surface_name"] in {
            "piat_standard_1997",
            "quantitative",
            "arithmetic_reasoning",
            "math_knowledge",
        }:
            print(
                f"{row['surface_name']:<24} overlap beta={row['female_beta_sd']:+.3f} "
                f"ci=({row['ci_low']:+.3f},{row['ci_high']:+.3f}) n={row['n_obs']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

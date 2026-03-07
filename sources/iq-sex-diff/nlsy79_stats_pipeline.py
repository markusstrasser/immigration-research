#!/usr/bin/env python3
"""Rigorous NLSY79 descriptive and sibling-pair models with proper same-sample checks."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from build_nlsy79_sibling_pairs import load_rows, to_int
from nlsy79_first_pass import load_pairs
from stage0_config import NLSY79


MISSING_CODES = {"", ".", "-1", "-2", "-3", "-4", "-5"}
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

BASE_COVARIATES = {
    "age_diff": NLSY79["age"]["asvab_proxy"]["code"],
    "older_sibs_diff": NLSY79["birth_order_proxy"]["code"],
}

SCHOOLING_COVARIATES = {
    "hs_grade_status_diff": "R0614900",
    "mother_hgc_diff": "R0006500",
    "father_hgc_diff": "R0007900",
    "urban_rural_14_diff": "R0001800",
}


def parse_numeric(value: str) -> float | None:
    if value in MISSING_CODES:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def pooled_weighted_sd(values: pd.Series, weights: pd.Series, female_mask: pd.Series) -> float | None:
    male_mask = ~female_mask
    female_values = values[female_mask]
    female_weights = weights[female_mask]
    male_values = values[male_mask]
    male_weights = weights[male_mask]
    if female_values.empty or male_values.empty:
        return None

    female_mean = np.average(female_values, weights=female_weights)
    male_mean = np.average(male_values, weights=male_weights)
    female_var = np.average((female_values - female_mean) ** 2, weights=female_weights)
    male_var = np.average((male_values - male_mean) ** 2, weights=male_weights)
    pooled = (
        female_weights.sum() * female_var + male_weights.sum() * male_var
    ) / (female_weights.sum() + male_weights.sum())
    if pooled <= 0:
        return None
    return float(np.sqrt(pooled))


def rows_to_frame(rows: dict[int, dict[str, str]]) -> pd.DataFrame:
    records: list[dict[str, float | int | None]] = []
    for caseid, values in rows.items():
        record: dict[str, float | int | None] = {"caseid": caseid}
        record["sex"] = to_int(values[NLSY79["sex"]["code"]])
        record["weight_asvab"] = parse_numeric(values[NLSY79["weights"]["asvab_1981"]["code"]])
        record["age_1981"] = parse_numeric(values[NLSY79["age"]["asvab_proxy"]["code"]])
        record["age_1979"] = parse_numeric(values[NLSY79["age"]["baseline"]["code"]])
        record["older_sibs_1979"] = parse_numeric(values[NLSY79["birth_order_proxy"]["code"]])
        record["hs_grade_status_1981"] = parse_numeric(values["R0614900"])
        record["mother_hgc_1979"] = parse_numeric(values["R0006500"])
        record["father_hgc_1979"] = parse_numeric(values["R0007900"])
        record["urban_rural_14"] = parse_numeric(values["R0001800"])
        for name, metadata in NLSY79["primary_subtests"].items():
            record[name] = parse_numeric(values[metadata["code"]])
        records.append(record)
    return pd.DataFrame.from_records(records).set_index("caseid").sort_index()


def standardize_scores(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    frame = frame.copy()
    female_mask = frame["sex"].eq(NLSY79["sex"]["female"])
    sex_valid = frame["sex"].isin([NLSY79["sex"]["male"], NLSY79["sex"]["female"]])
    weight_valid = frame["weight_asvab"].gt(0)
    standardized_columns: list[str] = []

    for name in NLSY79["primary_subtests"]:
        valid = sex_valid & weight_valid & frame[name].notna()
        if valid.sum() < 10:
            continue
        pooled_sd = pooled_weighted_sd(frame.loc[valid, name], frame.loc[valid, "weight_asvab"], female_mask[valid])
        if pooled_sd is None:
            continue
        overall_mean = float(np.average(frame.loc[valid, name], weights=frame.loc[valid, "weight_asvab"]))
        z_name = f"{name}_z"
        frame[z_name] = (frame[name] - overall_mean) / pooled_sd
        standardized_columns.append(z_name)

    for domain, components in NLSY79["domain_composites"].items():
        component_cols = [f"{component}_z" for component in components]
        raw_name = f"{domain}_raw"
        z_name = f"{domain}_z"
        frame[raw_name] = frame[component_cols].mean(axis=1, skipna=False)
        valid = sex_valid & weight_valid & frame[raw_name].notna()
        if valid.sum() < 10:
            continue
        pooled_sd = pooled_weighted_sd(
            frame.loc[valid, raw_name],
            frame.loc[valid, "weight_asvab"],
            female_mask[valid],
        )
        if pooled_sd is None:
            continue
        overall_mean = float(np.average(frame.loc[valid, raw_name], weights=frame.loc[valid, "weight_asvab"]))
        frame[z_name] = (frame[raw_name] - overall_mean) / pooled_sd
        standardized_columns.append(z_name)

    return frame, standardized_columns


def fit_weighted_gap(frame: pd.DataFrame, outcome: str) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY79["sex"]["male"], NLSY79["sex"]["female"]])
        & frame["weight_asvab"].gt(0)
        & frame[outcome].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_asvab", outcome]].copy()
    if len(sample) < 30:
        return None
    sample["female"] = sample["sex"].eq(NLSY79["sex"]["female"]).astype(float)
    design = sm.add_constant(sample[["female"]], has_constant="add")
    fit = sm.WLS(sample[outcome], design, weights=sample["weight_asvab"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "analysis_family": "descriptive",
        "model_name": "weighted_gap",
        "score_name": outcome.replace("_z", ""),
        "n_obs": int(fit.nobs),
        "beta_sd": float(fit.params["female"]),
        "se_sd": float(fit.bse["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
    }


def build_pair_frame(frame: pd.DataFrame, pairs_path: Path) -> pd.DataFrame:
    pair_rows: list[dict[str, float | int | str | bool | None]] = []
    pairs = load_pairs(pairs_path)
    for pair in pairs:
        female_id = int(pair["female_caseid"])
        male_id = int(pair["male_caseid"])
        if female_id not in frame.index or male_id not in frame.index:
            continue
        female = frame.loc[female_id]
        male = frame.loc[male_id]
        row: dict[str, float | int | str | bool | None] = {
            "pair_id": pair["pair_id"],
            "hhid_1979": int(pair["hhid_1979"]),
            "explicit_67_only": pair["relation_low"] in {"6", "7"} and pair["relation_high"] in {"6", "7"},
            "age_diff": (
                female["age_1981"] - male["age_1981"]
                if pd.notna(female["age_1981"]) and pd.notna(male["age_1981"])
                else (
                    female["age_1979"] - male["age_1979"]
                    if pd.notna(female["age_1979"]) and pd.notna(male["age_1979"])
                    else np.nan
                )
            ),
            "older_sibs_diff": (
                female["older_sibs_1979"] - male["older_sibs_1979"]
                if pd.notna(female["older_sibs_1979"]) and pd.notna(male["older_sibs_1979"])
                else np.nan
            ),
            "hs_grade_status_diff": (
                female["hs_grade_status_1981"] - male["hs_grade_status_1981"]
                if pd.notna(female["hs_grade_status_1981"]) and pd.notna(male["hs_grade_status_1981"])
                else np.nan
            ),
            "mother_hgc_diff": (
                female["mother_hgc_1979"] - male["mother_hgc_1979"]
                if pd.notna(female["mother_hgc_1979"]) and pd.notna(male["mother_hgc_1979"])
                else np.nan
            ),
            "father_hgc_diff": (
                female["father_hgc_1979"] - male["father_hgc_1979"]
                if pd.notna(female["father_hgc_1979"]) and pd.notna(male["father_hgc_1979"])
                else np.nan
            ),
            "urban_rural_14_diff": (
                female["urban_rural_14"] - male["urban_rural_14"]
                if pd.notna(female["urban_rural_14"]) and pd.notna(male["urban_rural_14"])
                else np.nan
            ),
        }
        for column in [col for col in frame.columns if col.endswith("_z")]:
            row[f"{column}_diff"] = (
                female[column] - male[column] if pd.notna(female[column]) and pd.notna(male[column]) else np.nan
            )
        pair_rows.append(row)
    return pd.DataFrame.from_records(pair_rows)


def fit_pair_model(pair_frame: pd.DataFrame, outcome: str, covariates: list[str]) -> dict[str, float | int] | None:
    needed = [outcome] + covariates
    sample = pair_frame[needed].dropna().copy()
    if len(sample) < 20:
        return None
    design = sm.add_constant(sample[covariates], has_constant="add")
    fit = sm.OLS(sample[outcome], design).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["const"]
    return {
        "n_obs": int(fit.nobs),
        "beta_sd": float(fit.params["const"]),
        "se_sd": float(fit.bse["const"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["const"]),
    }


def run_pair_models(pair_frame: pd.DataFrame, standardized_columns: list[str]) -> list[dict[str, float | int | str]]:
    outputs: list[dict[str, float | int | str]] = []
    for z_name in standardized_columns:
        score_name = z_name.removesuffix("_z")
        outcome = f"{z_name}_diff"

        base_all = fit_pair_model(pair_frame, outcome, list(BASE_COVARIATES))
        if base_all is None:
            continue
        outputs.append(
            {
                "analysis_family": "pair_fe",
                "model_name": "base_all_pairs",
                "score_name": score_name,
                **base_all,
                "attenuation_same_sample": "",
                "selection_shift_sd": "",
            }
        )

        strict_sample = pair_frame[pair_frame["explicit_67_only"]]
        strict = fit_pair_model(strict_sample, outcome, list(BASE_COVARIATES))
        if strict is not None:
            outputs.append(
                {
                    "analysis_family": "pair_fe",
                    "model_name": "base_explicit_67",
                    "score_name": score_name,
                    **strict,
                    "attenuation_same_sample": "",
                    "selection_shift_sd": "",
                }
            )

        full_covariates = list(BASE_COVARIATES) + list(SCHOOLING_COVARIATES)
        full_sample = pair_frame[[outcome] + full_covariates].dropna().copy()
        if len(full_sample) < 20:
            continue

        base_common = fit_pair_model(full_sample, outcome, list(BASE_COVARIATES))
        full = fit_pair_model(full_sample, outcome, full_covariates)
        if base_common is None or full is None:
            continue

        attenuation = (
            np.nan
            if np.isclose(base_common["beta_sd"], 0.0)
            else 1.0 - (full["beta_sd"] / base_common["beta_sd"])
        )
        selection_shift = base_common["beta_sd"] - base_all["beta_sd"]

        outputs.append(
            {
                "analysis_family": "pair_fe",
                "model_name": "base_same_sample_as_schooling",
                "score_name": score_name,
                **base_common,
                "attenuation_same_sample": "",
                "selection_shift_sd": float(selection_shift),
            }
        )
        outputs.append(
            {
                "analysis_family": "pair_fe",
                "model_name": "schooling_block_same_sample",
                "score_name": score_name,
                **full,
                "attenuation_same_sample": float(attenuation),
                "selection_shift_sd": float(selection_shift),
            }
        )
    return outputs


def main() -> int:
    print("Loading frozen NLSY79 rows...")
    rows = load_rows()
    print(f"Loaded {len(rows):,} respondents")
    frame = rows_to_frame(rows)
    print("Standardizing subtests and composites...")
    frame, standardized_columns = standardize_scores(frame)

    print("Fitting weighted descriptive gaps...")
    descriptive_rows = [
        result
        for result in (fit_weighted_gap(frame, column) for column in standardized_columns)
        if result is not None
    ]

    print("Building sibling-pair surface...")
    pair_frame = build_pair_frame(
        frame,
        DATA_DIR / "nlsy" / "nlsy79_opposite_sex_sibling_pairs.tsv",
    )
    print(f"Built {len(pair_frame):,} pair rows")
    print("Fitting sibling-pair models...")
    pair_rows = run_pair_models(pair_frame, standardized_columns)

    outputs = descriptive_rows + pair_rows
    output_path = DATA_DIR / "nlsy" / "nlsy79_stats_pipeline.tsv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "analysis_family",
                "model_name",
                "score_name",
                "n_obs",
                "beta_sd",
                "se_sd",
                "ci_low",
                "ci_high",
                "p_value",
                "attenuation_same_sample",
                "selection_shift_sd",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(outputs)

    print("NLSY79 stats pipeline")
    print(f"Wrote {output_path}")
    key_rows = [
        row
        for row in outputs
        if row["score_name"] in {"clerical_speed", "verbal", "quantitative", "mechanical", "mechanical_plus_electronic"}
        and row["model_name"] in {"weighted_gap", "base_all_pairs", "schooling_block_same_sample"}
    ]
    for row in key_rows:
        print(
            f"{row['score_name']:<26} {row['model_name']:<28} "
            f"beta={row['beta_sd']:+.3f} ci=({row['ci_low']:+.3f},{row['ci_high']:+.3f}) "
            f"n={row['n_obs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

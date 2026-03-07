#!/usr/bin/env python3
"""Causal-oriented NLSY97 pass for current math-course exposure vs late-school test surfaces.

This pass does not claim full identification. It fits a cleaner observed-confounder
specification after a DAG audit and reserves grades / honors / transcript outputs as
downstream variables rather than nuisance controls.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"
SOURCE = DATA_DIR / "nlsy97_transcript_deep_overlap_extract.parquet"

OUT_DATA = DATA_DIR / "nlsy97_course_causal_model_data.csv"
OUT_MODELS = DATA_DIR / "nlsy97_course_causal_models.tsv"

TREATMENTS = [
    "selfreport_highest_math_1997",
    "selfreport_algebra2_plus_1997",
    "selfreport_precalc_plus_1997",
    "selfreport_calc_plus_1997",
]

OUTCOMES = [
    "math_knowledge_z",
    "arithmetic_reasoning_z",
]

BASE_CONTROLS = [
    "female",
    "piat_standard_1997_z",
    "age_months_1997",
]

OFFER_CONTROLS = [
    "transcript_pr_sch_calc_hstr",
    "transcript_pr_sch_ap_hstr",
    "transcript_pr_sch_ib_hstr",
]


def fit_model(
    frame: pd.DataFrame,
    outcome: str,
    treatment: str,
    model_name: str,
    use_weights: bool,
    include_offer_controls: bool,
) -> dict[str, float | int | str]:
    required = [outcome, treatment, *BASE_CONTROLS, "weight_1997"]
    if include_offer_controls:
        required += OFFER_CONTROLS
    sample = frame.loc[:, required].dropna().copy()
    formula = f"{outcome} ~ {treatment} + female + piat_standard_1997_z + age_months_1997"
    if include_offer_controls:
        formula += (
            " + C(transcript_pr_sch_calc_hstr)"
            " + C(transcript_pr_sch_ap_hstr)"
            " + C(transcript_pr_sch_ib_hstr)"
        )
    if use_weights:
        fit = smf.wls(formula, data=sample, weights=sample["weight_1997"]).fit(cov_type="HC1")
    else:
        fit = smf.ols(formula, data=sample).fit(cov_type="HC1")
    low, high = fit.conf_int().loc[treatment]
    return {
        "outcome": outcome.removesuffix("_z"),
        "treatment": treatment,
        "model_name": model_name,
        "weighted": int(use_weights),
        "n_obs": int(fit.nobs),
        "treatment_beta_sd": float(fit.params[treatment]),
        "treatment_ci_low": float(low),
        "treatment_ci_high": float(high),
        "treatment_p_value": float(fit.pvalues[treatment]),
        "female_beta_sd": float(fit.params["female"]),
        "female_ci_low": float(fit.conf_int().loc["female", 0]),
        "female_ci_high": float(fit.conf_int().loc["female", 1]),
        "piat_beta_sd": float(fit.params["piat_standard_1997_z"]),
        "age_beta_per_month": float(fit.params["age_months_1997"]),
        "n_controls": int(len(fit.params) - 2),
    }


def main() -> int:
    frame = pd.read_parquet(SOURCE).copy()
    frame["female"] = frame["sex"].eq(2.0).astype(float)

    export_cols = [
        "weight_1997",
        "female",
        "math_knowledge_z",
        "arithmetic_reasoning_z",
        "piat_standard_1997_z",
        "age_months_1997",
        *TREATMENTS,
        *OFFER_CONTROLS,
    ]
    frame.loc[:, export_cols].to_csv(OUT_DATA, index=False)

    rows: list[dict[str, float | int | str]] = []
    for outcome in OUTCOMES:
        for treatment in TREATMENTS:
            rows.append(
                fit_model(
                    frame,
                    outcome=outcome,
                    treatment=treatment,
                    model_name="observed_confounders_wls",
                    use_weights=True,
                    include_offer_controls=False,
                )
            )
            rows.append(
                fit_model(
                    frame,
                    outcome=outcome,
                    treatment=treatment,
                    model_name="observed_confounders_ols",
                    use_weights=False,
                    include_offer_controls=False,
                )
            )
            rows.append(
                fit_model(
                    frame,
                    outcome=outcome,
                    treatment=treatment,
                    model_name="offer_stress_wls",
                    use_weights=True,
                    include_offer_controls=True,
                )
            )
            rows.append(
                fit_model(
                    frame,
                    outcome=outcome,
                    treatment=treatment,
                    model_name="offer_stress_ols",
                    use_weights=False,
                    include_offer_controls=True,
                )
            )

    OUT_MODELS.parent.mkdir(parents=True, exist_ok=True)
    with OUT_MODELS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "outcome",
                "treatment",
                "model_name",
                "weighted",
                "n_obs",
                "treatment_beta_sd",
                "treatment_ci_low",
                "treatment_ci_high",
                "treatment_p_value",
                "female_beta_sd",
                "female_ci_low",
                "female_ci_high",
                "piat_beta_sd",
                "age_beta_per_month",
                "n_controls",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUT_DATA}")
    print(f"Wrote {OUT_MODELS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

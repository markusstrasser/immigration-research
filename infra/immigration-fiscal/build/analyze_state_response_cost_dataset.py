#!/usr/bin/env python3
"""Fit minimal OLS specifications for the state response-cost dataset."""

from __future__ import annotations

import json

import pandas as pd
import statsmodels.formula.api as smf

from paths import derived_root


ROOT = derived_root()
DATA = ROOT / "state_response_cost_dataset.csv"
OUT = ROOT / "state_response_cost_models.json"


def model_payload(formula: str, df: pd.DataFrame) -> dict:
    model = smf.ols(formula, data=df, missing="raise")
    fit = model.fit()
    hc3 = model.fit(cov_type="HC3", use_t=True)
    return {
        "formula": formula,
        "nobs": int(fit.nobs),
        "rsquared": round(float(fit.rsquared), 4),
        "adj_rsquared": round(float(fit.rsquared_adj), 4),
        "params": {k: round(float(v), 6) for k, v in fit.params.items()},
        "pvalues": {k: round(float(v), 6) for k, v in fit.pvalues.items()},
        "conf_int": {
            key: [round(float(bounds[0]), 6), round(float(bounds[1]), 6)]
            for key, bounds in fit.conf_int().to_dict("index").items()
        },
        "hc3_t_conf_int": {
            key: [float(bounds[0]), float(bounds[1])]
            for key, bounds in hc3.conf_int().to_dict("index").items()
        },
        "leave_one_state_out_params": {
            state: {key: float(value) for key, value in
                    smf.ols(formula, data=df.loc[df["state"] != state], missing="raise").fit().params.items()}
            for state in df["state"]
        },
        "residuals_by_state": {
            state: round(float(resid), 6)
            for state, resid in zip(df["state"], fit.resid, strict=True)
        },
    }


def main() -> None:
    df = pd.read_csv(DATA)

    formulas = [
        "response_spending_millions_per_100k_residents_mid ~ recent_noncit_per_100k_residents",
        "response_spending_millions_per_100k_residents_mid ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
        "response_spending_millions_per_100k_residents_low ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
        "response_spending_millions_per_100k_residents_high ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
    ]

    payload = {
        "dataset": str(DATA),
        "interpretation": "descriptive OLS in eight selected states; no causal identification or equivalence test",
        "outcome_unit": "millions of USD per 100000 residents",
        "exposure_coefficient_unit": "millions of USD per recent noncitizen in this descriptive common-slope model",
        "uncertainty": "OLS t intervals, HC3 t sensitivity and leave-one-state-out coefficients; none correct selection or omitted confounding",
        "models": [model_payload(formula, df) for formula in formulas],
    }

    with OUT.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

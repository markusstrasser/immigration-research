#!/usr/bin/env python3
"""Fit minimal OLS specifications for the state response-cost dataset."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "state_response_cost_dataset.csv"
OUT = ROOT / "state_response_cost_models.json"


def model_payload(formula: str, df: pd.DataFrame) -> dict:
    fit = smf.ols(formula, data=df).fit()
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
        "residuals_by_state": {
            state: round(float(resid), 6)
            for state, resid in zip(df["state"], fit.resid, strict=True)
        },
    }


def main() -> None:
    df = pd.read_csv(DATA)

    formulas = [
        "response_spending_per_100k_residents_mid ~ recent_noncit_per_100k_residents",
        "response_spending_per_100k_residents_mid ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
        "response_spending_per_100k_residents_low ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
        "response_spending_per_100k_residents_high ~ recent_noncit_per_100k_residents + border_state + right_to_shelter",
    ]

    payload = {
        "dataset": str(DATA),
        "models": [model_payload(formula, df) for formula in formulas],
    }

    with OUT.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""State per-pupil spend from Census F-33 county rollup (elsec23 summary)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

SUMMARY = data_root() / "external" / "census_school_finance_2023_summary.txt"
COUNTY = derived_root() / "stage2" / "school_finance_county_2023.csv"
OUT = derived_root() / "stage5"


def build_census_state_per_pupil_panel(out_dir: Path | None = None) -> pd.DataFrame:
    if COUNTY.exists():
        county = pd.read_csv(COUNTY)
        county["state_fips"] = county["county_fips"].astype(str).str[:2]
        panel = (
            county.groupby("state_fips", as_index=False)
            .agg(enrollment=("enrollment", "sum"), current_spend=("current_spend", "sum"))
            .assign(
                per_pupil_current_expenditure_usd=lambda d: (
                    d["current_spend"] * 1000 / d["enrollment"].replace(0, pd.NA)
                ),
                school_year="2022-2023",
                source="census_f33_county_rollup",
            )
        )
    elif SUMMARY.exists():
        df = pd.read_csv(SUMMARY, dtype=str, low_memory=False)
        df["state_fips"] = df["CONUM"].str.zfill(5).str[:2]
        spend_cols = ["TCURSSTA", "TCURSGEN", "TCURSSCH", "TCURSOTH", "TCURINST", "TCURSSVC", "TCURONON"]
        for c in ["ENROLL", *spend_cols]:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df["current_spend"] = df[spend_cols].sum(axis=1)
        panel = (
            df.groupby("state_fips", as_index=False)
            .agg(enrollment=("ENROLL", "sum"), current_spend=("current_spend", "sum"))
            .assign(
                per_pupil_current_expenditure_usd=lambda d: (
                    d["current_spend"] * 1000 / d["enrollment"].replace(0, pd.NA)
                ),
                school_year="2022-2023",
                source="census_f33_state_rollup",
            )
        )
    else:
        return pd.DataFrame()
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / "census_state_per_pupil_2023.csv", index=False)
    print({"census_state_per_pupil_rows": len(panel)}, flush=True)
    return panel


if __name__ == "__main__":
    build_census_state_per_pupil_panel()

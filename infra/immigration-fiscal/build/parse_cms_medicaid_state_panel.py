#!/usr/bin/env python3
"""Roll up CMS Medicaid financial management to state-year totals (KFF substitute)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

CMS = data_root() / "external" / "stage5_net_negative" / "cms" / "medicaid_financial_management.csv"
OUT = derived_root() / "stage5"

STATE_NAME_TO_FIPS = {
    "Alabama": "01", "Alaska": "02", "Arizona": "04", "Arkansas": "05", "California": "06",
    "Colorado": "08", "Connecticut": "09", "Delaware": "10", "District of Columbia": "11",
    "Florida": "12", "Georgia": "13", "Hawaii": "15", "Idaho": "16", "Illinois": "17",
    "Indiana": "18", "Iowa": "19", "Kansas": "20", "Kentucky": "21", "Louisiana": "22",
    "Maine": "23", "Maryland": "24", "Massachusetts": "25", "Michigan": "26", "Minnesota": "27",
    "Mississippi": "28", "Missouri": "29", "Montana": "30", "Nebraska": "31", "Nevada": "32",
    "New Hampshire": "33", "New Jersey": "34", "New Mexico": "35", "New York": "36",
    "North Carolina": "37", "North Dakota": "38", "Ohio": "39", "Oklahoma": "40", "Oregon": "41",
    "Pennsylvania": "42", "Rhode Island": "44", "South Carolina": "45", "South Dakota": "46",
    "Tennessee": "47", "Texas": "48", "Utah": "49", "Vermont": "50", "Virginia": "51",
    "Washington": "53", "West Virginia": "54", "Wisconsin": "55", "Wyoming": "56",
    "Puerto Rico": "72",
}


def build_cms_medicaid_state_panel(out_dir: Path | None = None) -> pd.DataFrame:
    if not CMS.exists():
        return pd.DataFrame()
    df = pd.read_csv(CMS, low_memory=False)
    df["Total Computable"] = pd.to_numeric(df["Total Computable"], errors="coerce").fillna(0)
    med = df[df["Program"].astype(str).str.contains("Medical Assistance", na=False)]
    if med.empty:
        med = df
    panel = (
        med.groupby(["State", "Year"], as_index=False)["Total Computable"]
        .sum()
        .rename(columns={"State": "state_name", "Total Computable": "medicaid_total_computable_usd", "Year": "fy"})
    )
    panel["state_fips"] = panel["state_name"].map(STATE_NAME_TO_FIPS)
    panel["source"] = "cms_medicaid_financial_management_substitute_for_kff"
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / "cms_medicaid_state_panel.csv", index=False)
    print({"cms_medicaid_state_rows": len(panel)}, flush=True)
    return panel


if __name__ == "__main__":
    build_cms_medicaid_state_panel()

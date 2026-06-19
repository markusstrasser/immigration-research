#!/usr/bin/env python3
"""OHSS state immigration flows FY2013-2023 (refugee/LPR/naturalization)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

OHSS = data_root() / "external" / "origin" / "ohss" / "state_immigration_data_2013_2023.csv"
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


def build_ohss_state_immigration_panel(
    year: int = 2023, out_dir: Path | None = None
) -> pd.DataFrame:
    if not OHSS.exists():
        return pd.DataFrame()
    df = pd.read_csv(OHSS, low_memory=False)
    df = df[df["Year"] == year].copy()
    df["state_fips"] = df["State"].map(STATE_NAME_TO_FIPS)
    panel = df.dropna(subset=["state_fips"]).rename(
        columns={
            "Refugees Total": "refugees_total",
            "Asylees Total": "asylees_total",
            "New Arrivals Total": "new_arrivals_total",
            "Lawful Permanent Residents Total": "lpr_total",
            "Naturalizations Total": "naturalizations_total",
        }
    )
    keep = [
        "state_fips",
        "State",
        "refugees_total",
        "asylees_total",
        "new_arrivals_total",
        "lpr_total",
        "naturalizations_total",
    ]
    panel = panel[[c for c in keep if c in panel.columns]].assign(
        fiscal_year=year, source="ohss_state_immigration_data"
    )
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / f"ohss_state_immigration_{year}.csv", index=False)
    print({"ohss_state_rows": len(panel), "year": year}, flush=True)
    return panel


if __name__ == "__main__":
    build_ohss_state_immigration_panel()

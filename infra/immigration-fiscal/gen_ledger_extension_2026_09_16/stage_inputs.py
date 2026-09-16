#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2", "pandas>=2", "openpyxl>=3"]
# ///
"""Stage the state-level parameter table used by extend_ledger.py.

Reads only files already downloaded into this lane directory (no network):
  taxfoundation_2024_state_sales_tax_rates.csv  - Tax Foundation, combined state+local
                                                  sales tax rate as of 1 Jan 2024
  acs2023_state_proptax_medians.json            - ACS 2023 1-year B25103_001E / B25077_001E
  acs2023_state_median_gross_rent.json          - ACS 2023 1-year B25064_001E
  census_assf_fy2024_summary_tables.xlsx        - Census ASSF FY2024 summary Table 8

Writes state_parameters.csv keyed by GESTFIPS (the CPS household state code).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def clean(name: str) -> str:
    name = re.sub(r"\s*\([a-z]\)\s*$", "", str(name).strip())
    return name.replace(".", "").strip()


def main() -> None:
    prop = json.load(open(HERE / "acs2023_state_proptax_medians.json"))
    prop = pd.DataFrame(prop[1:], columns=prop[0])
    prop["fips"] = prop.state.astype(int)
    prop["median_real_estate_tax"] = prop.B25103_001E.astype(float)
    prop["median_home_value"] = prop.B25077_001E.astype(float)
    prop["property_tax_effective_rate"] = prop.median_real_estate_tax / prop.median_home_value
    prop["name"] = prop.NAME.map(clean)

    rent = json.load(open(HERE / "acs2023_state_median_gross_rent.json"))
    rent = pd.DataFrame(rent[1:], columns=rent[0])
    rent["fips"] = rent.state.astype(int)
    rent["median_gross_rent_monthly"] = rent.B25064_001E.astype(float)

    sales = pd.read_csv(HERE / "taxfoundation_2024_state_sales_tax_rates.csv")
    sales["name"] = sales.State.map(clean)
    sales["combined_sales_tax_rate"] = sales["Combined Rate"].str.rstrip("%").astype(float) / 100.0

    school = pd.read_excel(HERE / "census_assf_fy2024_summary_tables.xlsx", "8", header=None)
    school = school[[0, 2]].rename(columns={0: "raw", 2: "per_pupil_current_spending"})
    school["name"] = school.raw.astype(str).str.replace(r"\.+\s*$", "", regex=True).str.strip()
    school = school.loc[school.per_pupil_current_spending.apply(lambda v: isinstance(v, (int, float)))]
    school = school.dropna(subset=["per_pupil_current_spending"])
    national = float(school.loc[school.name.eq("United States"), "per_pupil_current_spending"].iloc[0])
    school = school.loc[~school.name.isin(["United States"])]
    school["name"] = school.name.map(clean)

    out = (prop[["fips", "name", "median_real_estate_tax", "median_home_value",
                 "property_tax_effective_rate"]]
           .merge(rent[["fips", "median_gross_rent_monthly"]], on="fips", validate="one_to_one")
           .merge(sales[["name", "combined_sales_tax_rate"]], on="name", how="left", validate="one_to_one")
           .merge(school[["name", "per_pupil_current_spending"]], on="name", how="left", validate="one_to_one"))
    out = out.loc[out.fips <= 56]  # drop Puerto Rico if present
    missing = out.loc[out[["combined_sales_tax_rate", "per_pupil_current_spending"]].isna().any(axis=1)]
    if len(missing):
        raise ValueError(f"Unmatched states: {missing.name.tolist()}")
    if len(out) != 51:
        raise ValueError(f"Expected 51 state rows, got {len(out)}")
    out["national_per_pupil_current_spending"] = national
    out.to_csv(HERE / "state_parameters.csv", index=False)
    print(out.to_string(index=False, float_format=lambda v: f"{v:,.4f}"))
    print(f"\nNational per-pupil current spending FY2024: {national:,.0f}")
    print(f"Population-unweighted mean effective property tax rate: {out.property_tax_effective_rate.mean():.4f}")


if __name__ == "__main__":
    main()

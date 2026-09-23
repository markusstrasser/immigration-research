#!/usr/bin/env python3
"""How large could immigration detention be inside the Mexico-born institutional counts?

A bound, not a correction: the reporting rule (research/immigration-detention-crime-and-fiscal-
scope-2026-09-20.md) forbids subtracting an ICE count from an ACS estimate, because date, coverage,
age, sex and origin do not match. This script sets the largest plausible detention stock of
Mexican nationals beside the weighted institutional count of Mexico-born men 18-40 in each
years-in-US bin, to show whether detention alone could account for a cell.

Stock bound = average daily population (all nationalities) x Mexico's share of detention book-ins.
Mexicans have shorter stays than other detainees (CRS RL32369), so their share of the stock is
below their share of book-ins and the bound overstates. It covers all ages and both sexes.

Run from the repository root (after analyze_census.py and analyze_acs.py):
  uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/ice_bound.py
Out: derived/ice_bound.csv
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"

# (year, ADP, ADP source, Mexico share of book-ins or None, share source)
TMP = "Marshall Project compilation of INS/DHS appropriations records (detention.csv)"
INPUTS = [
    (1980, 1620, TMP, None, ""),
    (1990, 6571, TMP, None, ""),
    (2000, 19458, TMP, None, ""),
    (2010, 30885, TMP, 0.606, "OHSS Enforcement Actions 2012, Table 5 (219,858 of 363,064)"),
    (2011, 33330, "CRS RL32369 (matches TMP)", 0.672, "OHSS Enforcement Actions 2012, Table 5 (288,581 of 429,247)"),
    (2012, 34260, TMP, 0.644, "OHSS Enforcement Actions 2012, Table 5 (307,523 of 477,523)"),
    (2019, 50165, "ICE ERO FY2019 report (TMP gives 49,403)", 0.24, "OHSS Enforcement Actions 2019 text: 24 percent"),
    (2023, None, "", 55000 / 270000, "OHSS FY2023 flow report text: Mexico 55,000 of 'more than 270,000'"),
    (2024, 37722, "ICE FY2024 detention workbook, Detention FY24!N99 (detention_evidence lane)", 69360 / 277910,
     "ICE FY2024 annual report via cj_use_allocation lane (69,360 of 277,910)"),
]


def main() -> None:
    census = pd.read_csv(DERIVED / "census_cohort_rates.csv")
    census = census[(census.group == "mexico_born") & (census.outcome == "institutional")]
    acs = pd.read_csv(DERIVED / "acs_cohort_rates.csv")
    rows = []
    for year, adp, adp_src, share, share_src in INPUTS:
        src = census[census.year == year] if year <= 2000 else acs[acs.year == year]
        for ysm in ("0-5", "6-10", "11-15", "all"):
            cell = src[src.ysm == ysm]
            if cell.empty:
                continue
            weighted = cell.weighted.iloc[0] if year <= 2000 else cell.weighted_per_year.iloc[0]
            inst = float(cell.rate.iloc[0] * weighted)
            bound = adp * share if (adp and share) else None
            rows.append(dict(year=year, ysm=ysm, mexico_born_men_18_40_institutional=round(inst),
                             adp_all_nationalities=adp, mexico_share_of_bookins=share,
                             mexican_stock_bound=round(bound) if bound else None,
                             bound_over_cell=round(bound / inst, 2) if bound else None,
                             adp_source=adp_src, share_source=share_src))
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "ice_bound.csv", index=False)
    print(out.drop(columns=["adp_source", "share_source"]).to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Program-by-program back-cast of the 2024 net cost to other residents, 2005-2024.

Native-First: every national series is a BEA cell the complete account already cites
(`full_account_spending_2026_09_20/derived/categories.csv` source cells; Table 3.1
receipt lines). Measured by year: what the nation spent on each benefit programme and
government function, what it collected on each receipt line, prices, residents, and
the Mexican-origin count. Assumed: the group's 2024 use of each programme and its 2024
payment of each tax, per person relative to the national per-capita amount.

  programme  relative use and payment held at 2024 for every line
  income     as programme, with the four household receipt lines scaled by the
             group's measured relative per-capita income (unit elasticity)

The response cases keep their 2024 coefficients. This is a model back-cast: no year
before 2024 has the group's own benefits, services or taxes observed here.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from backcast import FISCAL, HERE, ROOT, YEARS, series, workbook

BEA = ROOT / "sources/immigration-fiscal/data/external/bea_nipa"
RECEIPT_LINES = {  # Table 3.1 line -> complete-account receipt categories counted as direct
    3: ["federal_income_tax", "state_local_income_tax", "personal_motor_vehicle", "other_personal_tax"],
    8: ["employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi", "employer_hi",
        "medicare_supplementary_premiums", "other_domestic_social_contributions"],
    4: ["general_sales_tax", "excise_selective_sales", "customs_duties"],
    17: ["personal_current_transfers"],
}
CASES = [("cbo_informed_low", "cbo_category_lag_non_school_full", "shared_9", "gdp"),
         ("cbo_informed_high", "cbo_category_lag_non_school_full", "personal_6", "cash"),
         ("full_proportional_low", "proportional_reference", "shared_0", "gdp"),
         ("full_proportional_high", "proportional_reference", "personal_0", "cash")]
EDUCATION = {"school_current": "education_services", "other_education_current": "education_services"}


class Cells:
    def __init__(self, book: pd.ExcelFile):
        self.book, self.tables = book, {}

    def get(self, reference: str) -> pd.Series:
        """`T31200-A:33;T31200-A:34` -> summed nominal $bn by year."""
        total = None
        for part in reference.split(";"):
            sheet, line = part.strip().split(":")
            if sheet not in self.tables:
                table = self.book.parse(sheet, header=None)
                header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
                years = [int(float(v)) for v in table.iloc[header, 3:]]
                body = table.iloc[header + 1:].copy()
                body.index = pd.to_numeric(body.iloc[:, 0], errors="coerce")
                values = body.iloc[:, 3:].apply(pd.to_numeric, errors="coerce")
                values.columns = years
                self.tables[sheet] = values
            row = self.tables[sheet].loc[int(line)].reindex(YEARS).fillna(0.0) / 1e3
            total = row if total is None else total + row
        return total


def main() -> None:
    cells = Cells(workbook(BEA / "Section3All_xls.xlsx"))
    annual = pd.read_csv(HERE / "derived/backcast_annual.csv").set_index("year")
    group, income = annual.group_millions, annual.relative_per_capita_income
    income = income / income[2024]
    price = series(workbook(BEA / "Section1All_xls.xlsx"), "T10109-A", "Gross domestic product")
    people = series(workbook(HERE / "_cache/Section7All_xls.xlsx"), "T70100-A", "Population (midperiod, thousands)")
    real = price[2024] / price.reindex(YEARS)
    share = group / (people.reindex(YEARS) / 1e3)
    share = share / share[2024]                                        # group population share, 2024 = 1

    categories = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    spending = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    spending = spending[spending.scenario_id == "complete_preferred_F_per_capita"]
    receipts = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    receipts = receipts[receipts.scenario_id == "cbo_collective"]
    cases = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_cases.csv")
    components = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_components.csv")

    def index(reference: str) -> pd.Series:
        nominal = cells.get(reference)
        if nominal[2024] <= 0:
            raise ValueError(f"[BLOCKED] {reference} has no positive 2024 value")
        return nominal * real / nominal[2024]                           # real national total, 2024 = 1

    rows, programme_rows = [], []
    for name, profile, case_id, normalization in CASES:
        case = cases[(cases.profile == profile) & (cases.case_id == case_id)
                     & (cases.normalization == normalization)].iloc[0]
        allocation = case.allocation
        transfers = spending[(spending.allocation == allocation) & (spending.response_class == "household_transfer")]
        transfer_t = sum(row.target_bn * index(categories.loc[row.category, "source_cells"]) * share
                         for row in transfers.itertuples())
        parts = components[(components.profile == profile) & (components.case_id == case_id)
                           & (components.allocation == allocation)].drop_duplicates("component")
        service_t = sum(row.responsive_bn * index(categories.loc[EDUCATION.get(row.component, row.component),
                                                                 "source_cells"]) * share
                        for row in parts.itertuples())
        mine = receipts[receipts.allocation == allocation].set_index("category").target_bn
        receipt_t = {line: mine[names].sum() * index(f"T30100-A:{line}") * share
                     for line, names in RECEIPT_LINES.items()}
        direct_2024 = sum(v[2024] for v in receipt_t.values())
        production = case.before_services_bn - (direct_2024 - transfer_t[2024])
        production_t = production * group / group[2024]
        for rule, scale in (("programme", 1.0), ("income", income)):
            receipts_t = sum(receipt_t.values()) * scale
            net = transfer_t + service_t - receipts_t - production_t
            if not np.isclose(net[2024], -case.welfare_bn, rtol=1e-6):
                raise ValueError(f"[BLOCKED] {name}/{rule} reconstructs {net[2024]:.4f}, account {-case.welfare_bn:.4f}")
            for year in YEARS:
                rows.append(dict(case=name, rule=rule, year=year, transfers_bn=transfer_t[year],
                                 responsive_services_bn=service_t[year], direct_receipts_bn=receipts_t[year],
                                 production_gain_bn=production_t[year], net_cost_bn=net[year]))
        if name == "cbo_informed_low":
            for row in transfers.itertuples():
                programme_rows.append((row.category, row.target_bn, categories.loc[row.category, "source_cells"]))
            for row in parts.itertuples():
                programme_rows.append((row.component, row.responsive_bn,
                                       categories.loc[EDUCATION.get(row.component, row.component), "source_cells"]))

    out = pd.DataFrame(rows)
    out.round(4).to_csv(HERE / "derived/backcast_categories_annual.csv", index=False)
    windows = {"10y_2015_2024": 2015, "15y_2010_2024": 2010, "20y_2005_2024": 2005}
    records = []
    for (case_name, rule), block in out.groupby(["case", "rule"], sort=False):
        net = block.set_index("year").net_cost_bn
        # Pandemic transfers were near-universal per head, not distributed like 2024 credits:
        # the second variant replaces 2020-2021 with the mean of 2019 and 2022.
        normal = net.copy()
        normal[[2020, 2021]] = (net[2019] + net[2022]) / 2
        for label, values in ((rule, net), (f"{rule}_ex_pandemic", normal)):
            records.append(dict(case=case_name, rule=label,
                                **{w: values[values.index >= start].sum() / 1e3 for w, start in windows.items()}))
    table = pd.DataFrame(records)
    table.round(4).to_csv(HERE / "derived/backcast_categories_windows.csv", index=False)

    residents = people.reindex(YEARS) / people[2024]
    national = pd.DataFrame({re.sub(r"_services$|_current$", "", c): index(ref) / residents
                             for c, _, ref in programme_rows}).loc[[2005, 2010, 2015, 2019, 2020, 2021, 2024]]
    weights = pd.Series({re.sub(r"_services$|_current$", "", c): bn for c, bn, _ in programme_rows})
    national = national.T.assign(group_2024_bn=weights).sort_values("group_2024_bn", ascending=False)
    national.round(3).to_csv(HERE / "derived/national_programme_index.csv", index_label="programme")
    print(table.round(2).to_string(index=False))
    print("\nreal national spending per resident, 2024 = 1 (largest lines for the group):")
    print(national.head(14).round(2).to_string())


if __name__ == "__main__":
    main()

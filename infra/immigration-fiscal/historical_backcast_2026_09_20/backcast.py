#!/usr/bin/env python3
"""Back-cast the 2024 Mexican-origin fiscal concepts to 2005-2024.

Native-First: consumes the complete account's exports, the pinned BEA workbooks
and ACS series; no new microdata estimator. Measured by year: government current
receipts and expenditures (BEA 3.1), the GDP implicit deflator (1.1.9), midperiod
population (7.1), ACS Mexican-origin counts and relative per-capita income.
Assumed: the group's 2024 per-person position relative to the nation. Three rules:

  flat    per-person cost constant in 2024 dollars
  ratio   receipts and charged spending keep their 2024 ratios to national per capita
  income  as ratio, with the receipts ratio scaled by the group's measured
          per-capita income relative to the nation (unit elasticity)

This is not a measured historical account. No year before 2024 has group taxes,
benefits or services observed here.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = ROOT / "infra/immigration-fiscal"
PINNED = {"Section1All_xls.xlsx": "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19",
          "Section3All_xls.xlsx": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
          "Section7All_xls.xlsx": "ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef"}
YEARS = list(range(2005, 2025))
PROFILES = {"net_cost_cbo_informed": "cbo_category_lag_non_school_full",
            "net_cost_full_proportional": "proportional_reference"}


def response_anchors() -> dict[str, float]:
    """2024 conditional net cost to other residents, $bn; the range spans allocation and scaling cases.

    The September 20 bands, then the main case adopted on 2026-09-23 (general government at
    0.59-0.84, justice and uncompensated care keyed by use; main_case_2026_09_23).
    """
    summary = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/service_response_summary.csv").set_index("profile")
    adopted = pd.read_csv(FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv")
    adopted = adopted[adopted.variant == "adopted"].set_index("profile")
    out = {}
    for name, profile in PROFILES.items():
        out[f"{name}_low"] = -float(summary.loc[profile, "max_welfare_bn"])
        out[f"{name}_high"] = -float(summary.loc[profile, "min_welfare_bn"])
    for name, profile in PROFILES.items():
        out[f"{name}_adopted_low"] = float(adopted.loc[profile, "cost_low_bn"])
        out[f"{name}_adopted_high"] = float(adopted.loc[profile, "cost_high_bn"])
    return out


def workbook(path: Path) -> pd.ExcelFile:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != PINNED[path.name]:
        raise ValueError(f"[BLOCKED] {path.name} is not the pinned August 2026 vintage: {digest}")
    return pd.ExcelFile(path)


def series(book: pd.ExcelFile, sheet: str, label: str) -> pd.Series:
    table = book.parse(sheet, header=None)
    header = table.index[table.iloc[:, 0].astype(str).str.strip().eq("Line")][0]
    match = table[table.iloc[:, 1].astype(str).str.strip().eq(label)]
    if match.empty:
        raise ValueError(f"[BLOCKED] {sheet} has no line labelled {label!r}")
    years = [int(float(v)) for v in table.iloc[header, 3:]]
    return pd.Series(match.iloc[0, 3:].astype(float).to_numpy(), index=years)


def anchors(allocation: str) -> dict[str, float]:
    """2024 complete-account values, $bn and millions; domestic = target plus other residents."""
    receipts = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/scenario_totals.csv")
    spending = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/scenario_totals.csv")
    accounts = pd.read_csv(FISCAL / "full_account_2026_09_20/derived/accounts.csv")
    r = receipts[(receipts.scenario_id == "cbo_collective") & (receipts.allocation == allocation)].iloc[0]
    g = spending[(spending.scenario_id == "complete_preferred_F_per_capita")
                 & (spending.allocation == allocation)].iloc[0]
    a = accounts[(accounts.receipt_scenario == "cbo_collective") & (accounts.allocation == allocation)
                 & (accounts.spending_scenario == "complete_preferred_F_per_capita")].iloc[0]
    return dict(receipts=float(r.target_bn), spending=float(g.target_bn),
                domestic_receipts=float(r.target_bn + r.other_bn), domestic_spending=float(g.target_bn + g.other_bn),
                group=float(a.target_population) / 1e6, residents=float(a.resident_population) / 1e6,
                gap=-float(a.normalized_gap_bn))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bea-dir", type=Path,
                        default=ROOT / "sources/immigration-fiscal/data/external/bea_nipa")
    args = parser.parse_args()
    section3 = workbook(args.bea_dir / "Section3All_xls.xlsx")
    receipts = series(section3, "T30100-A", "Current receipts")
    spending = series(section3, "T30100-A", "Current expenditures")
    deflator = series(workbook(args.bea_dir / "Section1All_xls.xlsx"), "T10109-A", "Gross domestic product")
    people = series(workbook(HERE / "_cache/Section7All_xls.xlsx"), "T70100-A", "Population (midperiod, thousands)")
    if abs(receipts[2024] - 8008290) > 0.5 or abs(spending[2024] - 10061458) > 0.5:
        raise ValueError("[BLOCKED] BEA 2024 totals differ from the complete account's")

    acs = pd.read_csv(HERE / "inputs/acs_mexican_origin.csv").set_index("year").reindex(YEARS)
    count = acs.acs_mexican_origin.interpolate()                      # 2020 has no standard release
    relative = (acs.per_capita_income_mexican / acs.per_capita_income_total).interpolate().bfill()
    base = anchors("shared")
    group_receipts, group_2024 = base["receipts"], base["group"]
    group = count * group_2024 / count[2024]                          # millions, account definition
    real = deflator[2024] / deflator.reindex(YEARS)
    # BEA midperiod growth, levelled to the account's 2024 resident denominator (340.111m vs 340.095m)
    residents = people.reindex(YEARS) * 1e3 * (base["residents"] * 1e6 / (people[2024] * 1e3))
    r = receipts.reindex(YEARS) * 1e6 * real / residents
    s = spending.reindex(YEARS) * 1e6 * real / residents
    rho = group_receipts * 1e9 / (group_2024 * 1e6) / r[2024]
    income = relative / relative[2024]

    annual = pd.DataFrame(dict(group_millions=group, relative_per_capita_income=relative,
                               national_receipts_per_capita=r, national_spending_per_capita=s))
    concepts = response_anchors()
    for name, value in concepts.items():
        # cost = spending charged to the group under this response case, less its receipts
        sigma = (value + group_receipts) * 1e9 / (group_2024 * 1e6) / s[2024]
        annual[f"{name}__flat"] = group / group_2024 * value
        annual[f"{name}__ratio"] = group * 1e6 * (sigma * s - rho * r) / 1e9
        annual[f"{name}__income"] = group * 1e6 * (sigma * s - rho * income * r) / 1e9
    # Gap against the average resident: a receipts shortfall less a spending shortfall, so a
    # national deficit shared by everyone cancels. Domestic shares of the BEA totals stay at 2024.
    name, value = "gap_vs_average_resident", base["gap"]
    r_dom = r * base["domestic_receipts"] * 1e3 / receipts[2024]
    s_dom = s * base["domestic_spending"] * 1e3 / spending[2024]
    rho_r = group_receipts / group_2024 / (base["domestic_receipts"] / base["residents"])
    rho_s = base["spending"] / group_2024 / (base["domestic_spending"] / base["residents"])
    annual[f"{name}__flat"] = group / group_2024 * value
    annual[f"{name}__ratio"] = group * 1e6 * ((1 - rho_r) * r_dom - (1 - rho_s) * s_dom) / 1e9
    annual[f"{name}__income"] = group * 1e6 * ((1 - rho_r * income) * r_dom - (1 - rho_s) * s_dom) / 1e9
    concepts = dict(concepts, **{name: value})
    for name, value in concepts.items():
        for rule in ("flat", "ratio", "income"):
            if not np.isclose(annual.loc[2024, f"{name}__{rule}"], value, rtol=1e-6):
                raise ValueError(f"[BLOCKED] {name}/{rule} does not reproduce its 2024 anchor: "
                                 f"{annual.loc[2024, f'{name}__{rule}']} vs {value}")
    (HERE / "derived").mkdir(exist_ok=True)
    annual.round(4).to_csv(HERE / "derived/backcast_annual.csv", index_label="year")

    windows = {"10y_2015_2024": range(2015, 2025), "15y_2010_2024": range(2010, 2025),
               "20y_2005_2024": range(2005, 2025)}
    rows = [dict(concept=name, rule=rule, **{w: annual.loc[list(ys), f"{name}__{rule}"].sum() / 1e3
                                             for w, ys in windows.items()})
            for name in concepts for rule in ("flat", "ratio", "income")]
    table = pd.DataFrame(rows)
    table.round(4).to_csv(HERE / "derived/backcast_windows.csv", index=False)
    print(f"receipts ratio {rho:.3f}; relative income {relative[2008]:.3f} (2008) -> {relative[2024]:.3f} (2024)")
    print(table.round(2).to_string(index=False))


if __name__ == "__main__":
    main()

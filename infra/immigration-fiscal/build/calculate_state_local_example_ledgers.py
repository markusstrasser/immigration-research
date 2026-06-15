#!/usr/bin/env python3
"""Calculate illustrative state/local ledgers for NY, CA, and TX.

Method:
1. Use CBO's 2023 surge-population state residence shares.
2. Use CBO's direct 2023 state/local category totals for education,
   health-income programs, shelter, and border security.
3. Allocate categories without published state tables by state share.
4. Estimate state/local tax revenue using the national CBO direct revenue
   per surge resident, adjusted by each state's ITEP tax-per-undocumented-
   resident factor relative to the national ITEP average.

This is intentionally an illustrative state ledger, not a claimed official
state estimate. CBO does not publish full state tables for all categories.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ITEP_TABLE_2 = ROOT.parent / "itep" / "itep_table_2.tsv"
ITEP_TABLE_6 = ROOT.parent / "itep" / "itep_table_6.tsv"
OUT_CSV = ROOT / "state_local_example_ledgers.csv"
OUT_JSON = ROOT / "state_local_example_ledgers.json"

# CBO 2025 state/local report.
SURGE_RESIDENTS_2023 = 4_300_000
STATE_SHARES = {
    "NY": {"name": "New York", "share": 0.07, "explicit_shelter_b": 2.6, "explicit_border_b": 0.0},
    "CA": {"name": "California", "share": 0.11, "explicit_shelter_b": 0.0, "explicit_border_b": 0.015},
    "TX": {"name": "Texas", "share": 0.15, "explicit_shelter_b": 0.0, "explicit_border_b": 2.5},
}

# CBO direct state/local 2023 totals in billions.
DIRECT_REVENUE_B = 10.1
DIRECT_SPENDING_B = 19.3
DIRECT_K12_B = 5.7
DIRECT_HEALTH_INCOME_B = 1.0
DIRECT_SHELTER_TOTAL_B = 3.3
DIRECT_BORDER_TOTAL_B = 2.7
DIRECT_OTHER_B = (
    DIRECT_SPENDING_B
    - DIRECT_K12_B
    - DIRECT_HEALTH_INCOME_B
    - DIRECT_SHELTER_TOTAL_B
    - DIRECT_BORDER_TOTAL_B
)

# Revised federal-inclusive reference from the July 2024 CBO federal report:
# +$897B included net, less $200B illustrative omitted discretionary pressure.
REVISED_FEDERAL_NET_B = 697.0
FEDERAL_YEARS = 11
FEDERAL_INCREMENT_2021_2026 = 8_700_000


def parse_money(raw: str) -> float:
    return float(raw.replace("$", "").replace(",", "").strip())


def load_itep_tax_per_person() -> dict[str, float]:
    pops: dict[str, float] = {}
    with ITEP_TABLE_6.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            pops[row["State"]] = float(row["Population"].replace(",", ""))

    taxes_per_person: dict[str, float] = {}
    with ITEP_TABLE_2.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            state = row["State"]
            if state in {"SUM ALL STATES**", "Payments to other states", "NATIONAL TOTAL***"}:
                continue
            taxes = parse_money(row["Total State and Local Taxes**"])
            taxes_per_person[state] = taxes / pops[state]
    return taxes_per_person


def build_rows() -> list[dict[str, float | str]]:
    taxes_per_person = load_itep_tax_per_person()
    national_itep_tax_per_person = 37_277_600_000 / 10_900_000
    national_cbo_revenue_per_resident = DIRECT_REVENUE_B * 1e9 / SURGE_RESIDENTS_2023
    revised_federal_net_per_person_per_year = (
        REVISED_FEDERAL_NET_B * 1e9 / FEDERAL_INCREMENT_2021_2026 / FEDERAL_YEARS
    )

    rows: list[dict[str, float | str]] = []
    for abbr, info in STATE_SHARES.items():
        residents = SURGE_RESIDENTS_2023 * info["share"]
        itep_factor = taxes_per_person[info["name"]] / national_itep_tax_per_person
        illustrative_revenue = residents * national_cbo_revenue_per_resident * itep_factor / 1e9

        education = DIRECT_K12_B * info["share"]
        health_income = DIRECT_HEALTH_INCOME_B * info["share"]
        other = DIRECT_OTHER_B * info["share"]
        explicit_floor = info["explicit_shelter_b"] + info["explicit_border_b"]
        gross = education + health_income + other + explicit_floor
        net = gross - illustrative_revenue

        row = {
            "state": abbr,
            "state_name": info["name"],
            "surge_residents_2023_est": round(residents),
            "cbo_share_of_surge_pop_pct": round(info["share"] * 100, 1),
            "explicit_response_floor_b": round(explicit_floor, 3),
            "education_allocated_b": round(education, 3),
            "health_income_allocated_b": round(health_income, 3),
            "other_general_allocated_b": round(other, 3),
            "gross_direct_local_spending_b": round(gross, 3),
            "illustrative_local_revenue_b": round(illustrative_revenue, 3),
            "illustrative_net_local_cost_b": round(net, 3),
            "explicit_response_floor_per_resident": round(explicit_floor * 1e9 / residents, 2),
            "illustrative_net_local_cost_per_resident": round(net * 1e9 / residents, 2),
            "rough_federal_net_per_incremental_surge_person_per_year": round(
                revised_federal_net_per_person_per_year, 2
            ),
            "cross_base_combined_benchmark_per_person_per_year": round(
                revised_federal_net_per_person_per_year - net * 1e9 / residents, 2
            ),
            "itep_tax_factor_vs_national": round(itep_factor, 3),
        }
        rows.append(row)
    return rows


def write_outputs(rows: list[dict[str, float | str]]) -> None:
    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "method_notes": [
            "State shares come from CBO Table A-1 for the 2023 surge population: NY 7%, CA 11%, TX 15%.",
            "Explicit shelter and border amounts use CBO's named state amounts only.",
            "Education, health-income, and other direct spending are allocated by state share because CBO does not publish full state tables.",
            "Illustrative local revenue uses national CBO direct revenue per surge resident, scaled by each state's ITEP tax-per-undocumented-resident factor.",
            "State/local spending in CBO's report is net of federal grants-in-aid.",
            "The federal comparison line uses the revised federal-inclusive net of +$697B over 2024-2034 for the 8.7M incremental surge population, annualized over 11 years.",
            "That federal benchmark and the 2023 resident-stock local figures use different denominators, so the combined benchmark is only a rough sign check.",
        ],
        "rows": rows,
    }
    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()

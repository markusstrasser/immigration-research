#!/usr/bin/env python3
"""Build a small state-level dataset for the 2021+ immigration surge analysis.

This script intentionally targets the narrow channel that is actually measurable
with local files: concentrated 2023 state/local response spending identified by
CBO, paired with ACS 2023 PUMS exposure proxies.

Outputs:
  - state_response_cost_dataset.csv
  - state_response_cost_dataset.json
"""

from __future__ import annotations

import csv
import json
import zipfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent
PERSON_ZIP = DATA_ROOT / "census" / "acs_pums_2023_person.zip"
ITEP_TAXES = DATA_ROOT / "itep" / "itep_table_2.tsv"
OUT_CSV = ROOT / "state_response_cost_dataset.csv"
OUT_JSON = ROOT / "state_response_cost_dataset.json"

STATE_INFO = {
    "04": {
        "abbr": "AZ",
        "name": "Arizona",
        "response_spending_millions_low": 174.0,
        "response_spending_millions_high": 174.0,
        "border_state": 1,
        "right_to_shelter": 0,
    },
    "06": {
        "abbr": "CA",
        "name": "California",
        "response_spending_millions_low": 15.0,
        "response_spending_millions_high": 15.0,
        "border_state": 1,
        "right_to_shelter": 0,
    },
    "08": {
        "abbr": "CO",
        "name": "Colorado",
        "response_spending_millions_low": 0.0,
        "response_spending_millions_high": 50.0,
        "border_state": 0,
        "right_to_shelter": 0,
    },
    "12": {
        "abbr": "FL",
        "name": "Florida",
        "response_spending_millions_low": 21.0,
        "response_spending_millions_high": 21.0,
        "border_state": 0,
        "right_to_shelter": 0,
    },
    "17": {
        "abbr": "IL",
        "name": "Illinois",
        "response_spending_millions_low": 400.0,
        "response_spending_millions_high": 400.0,
        "border_state": 0,
        "right_to_shelter": 0,
    },
    "25": {
        "abbr": "MA",
        "name": "Massachusetts",
        "response_spending_millions_low": 300.0,
        "response_spending_millions_high": 300.0,
        "border_state": 0,
        "right_to_shelter": 1,
    },
    "36": {
        "abbr": "NY",
        "name": "New York",
        "response_spending_millions_low": 2600.0,
        "response_spending_millions_high": 2600.0,
        "border_state": 0,
        "right_to_shelter": 1,
    },
    "48": {
        "abbr": "TX",
        "name": "Texas",
        "response_spending_millions_low": 2500.0,
        "response_spending_millions_high": 2500.0,
        "border_state": 1,
        "right_to_shelter": 0,
    },
}


def parse_currency(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    return float(cleaned) if cleaned else 0.0


def load_itep_taxes() -> dict[str, float]:
    taxes: dict[str, float] = {}
    with ITEP_TAXES.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            state_name = row["State"].strip()
            if state_name in {"SUM ALL STATES**", "Payments to other states", "NATIONAL TOTAL***"}:
                continue
            taxes[state_name] = parse_currency(row["Total State and Local Taxes**"])
    return taxes


def process_person_file(stats: dict[str, dict[str, float]], member_name: str) -> None:
    with zipfile.ZipFile(PERSON_ZIP) as archive:
        with archive.open(member_name) as raw:
            decoded = (line.decode("utf-8", "ignore") for line in raw)
            reader = csv.DictReader(decoded)
            for row in reader:
                state = row["STATE"]
                if state not in STATE_INFO:
                    continue
                weight = float(row["PWGTP"])
                stats[state]["population"] += weight

                cit = row["CIT"].strip()
                nativity = row["NATIVITY"].strip()
                yoep = row["YOEP"].strip()

                if nativity == "2":
                    stats[state]["foreign_born_total"] += weight

                    if yoep and int(yoep) <= 2020:
                        stats[state]["foreign_born_pre2021"] += weight

                if cit == "5" and nativity == "2" and yoep and int(yoep) >= 2021:
                    stats[state]["recent_noncit_2021_2023"] += weight


def build_dataset() -> list[dict[str, float | str | int]]:
    stats: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "population": 0.0,
            "foreign_born_total": 0.0,
            "foreign_born_pre2021": 0.0,
            "recent_noncit_2021_2023": 0.0,
        }
    )

    for member_name in ("psam_pusa.csv", "psam_pusb.csv"):
        process_person_file(stats, member_name)

    itep_taxes = load_itep_taxes()
    rows: list[dict[str, float | str | int]] = []
    for state_code, info in sorted(STATE_INFO.items(), key=lambda item: item[1]["abbr"]):
        state_stats = stats[state_code]
        population = state_stats["population"]
        recent_noncit = state_stats["recent_noncit_2021_2023"]
        pre2021_foreign_born = state_stats["foreign_born_pre2021"]
        taxes = itep_taxes[info["name"]]
        low = info["response_spending_millions_low"]
        high = info["response_spending_millions_high"]
        mid = (low + high) / 2.0

        row = {
            "state": info["abbr"],
            "state_name": info["name"],
            "population_weighted_acs_2023": round(population, 1),
            "recent_noncit_2021_2023_weighted": round(recent_noncit, 1),
            "recent_noncit_share_pct": round(100.0 * recent_noncit / population, 4),
            "recent_noncit_per_100k_residents": round(100000.0 * recent_noncit / population, 1),
            "pre2021_foreign_born_weighted": round(pre2021_foreign_born, 1),
            "pre2021_foreign_born_share_pct": round(100.0 * pre2021_foreign_born / population, 4),
            "response_spending_millions_low": low,
            "response_spending_millions_mid": round(mid, 3),
            "response_spending_millions_high": high,
            "response_spending_per_100k_residents_low": round(100000.0 * low / population, 4),
            "response_spending_per_100k_residents_mid": round(100000.0 * mid / population, 4),
            "response_spending_per_100k_residents_high": round(100000.0 * high / population, 4),
            "itep_total_state_local_taxes_2022": round(taxes, 1),
            "response_mid_as_share_of_itep_taxes_pct": round(100.0 * mid * 1_000_000.0 / taxes, 2),
            "border_state": info["border_state"],
            "right_to_shelter": info["right_to_shelter"],
        }
        rows.append(row)

    return rows


def write_outputs(rows: list[dict[str, float | str | int]]) -> None:
    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "notes": [
            "Response spending values are from CBO's June 2025 state/local report.",
            "Colorado is interval-censored in the source ('less than $50 million'); low=0, high=50, mid=25 is an inference for modeling convenience.",
            "ACS exposure proxy is weighted count/share of foreign-born noncitizens with year of entry 2021-2023 in ACS 2023 PUMS.",
            "ITEP taxes are descriptive context only; they are not a surge-specific offset and should not be used as a control.",
        ],
        "rows": rows,
    }
    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def main() -> None:
    rows = build_dataset()
    write_outputs(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()

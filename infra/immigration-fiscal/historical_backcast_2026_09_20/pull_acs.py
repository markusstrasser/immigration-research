#!/usr/bin/env python3
"""Pull the ACS 1-year series the back-cast needs; write `inputs/acs_mexican_origin.csv`.

B03001_004E gives the Mexican-origin count for every released year. The Selected
Population Profile (S0201) gives per-capita income and median age for the Mexican
group and the total population; its variable codes and the group code (401, later
4015) move between years, so both are resolved by label. `CENSUS_API_KEY` comes
from the environment and is never printed. 2020 has no standard 1-year release and
the profile endpoint starts in 2008.
"""
from __future__ import annotations

import csv
import json
import os
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = os.environ["CENSUS_API_KEY"]
LABELS = {"per_capita_income": r"per capita income \(dollars\)$", "median_age": r"median age \(years\)$",
          # earnings of full-time year-round workers do not move with the group's falling child share
          "median_earnings_ftyr_male": r"median earnings \(dollars\).*full-time, year-round workers.*!!male$",
          "median_earnings_ftyr_female": r"median earnings \(dollars\).*full-time, year-round workers.*!!female$",
          "median_household_income": r"median household income \(dollars\)$"}


def get(url: str):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=90) as response:
                body = response.read()
            return json.loads(body) if body else None
        except Exception as error:  # the URL carries the key: report the class only
            last = f"{type(error).__name__} {getattr(error, 'code', '')}"
            time.sleep(3)
    print(f"    ! gave up: {last}")
    return None


def profile(year: int) -> dict:
    base = f"https://api.census.gov/data/{year}/acs/acs1/spp"
    meta = get(base + "/variables.json")
    if not meta:
        return {}
    codes = {}
    for code, entry in sorted(meta["variables"].items()):
        if re.fullmatch(r"S0201_\d+E", code):
            for name, pattern in LABELS.items():
                if name not in codes and re.search(pattern, entry.get("label", ""), re.I):
                    codes[name] = code
    out = {}
    for tag, candidates in (("mexican", ("4015", "401")), ("total", ("001",))):
        for group in candidates:
            rows = get(f"{base}?get={','.join(codes.values())}&for=us:1&POPGROUP={group}&key={KEY}")
            if rows:
                for name, code in codes.items():
                    out[f"{name}_{tag}"] = rows[1][rows[0].index(code)]
                break
    return out


def main() -> None:
    rows = []
    for year in range(2005, 2025):
        if year == 2020:
            continue
        counts = get(f"https://api.census.gov/data/{year}/acs/acs1?get=B03001_001E,B03001_004E&for=us:1&key={KEY}")
        if not counts:
            raise SystemExit(f"[BLOCKED] no B03001 count for {year}")
        row = dict(year=year, acs_total=counts[1][0], acs_mexican_origin=counts[1][1])
        row.update(profile(year) if year >= 2008 else {})
        rows.append(row)
        print(f"  ✓ {year}: {row}")
    fields = ["year", "acs_total", "acs_mexican_origin"] + [f"{name}_{tag}" for name in LABELS
                                                            for tag in ("mexican", "total")]
    target = HERE / "inputs/acs_mexican_origin.csv"
    with target.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: r.get(k, "") for k in fields} for r in rows)
    print(f"[written] {target}: {len(rows)} years")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Arm 1: the published-estimate table, built from sources.json.

sources.json holds one record per published estimate, each field quoted from the
primary document.  This script only reshapes it into a table; it invents nothing.

Output: derived/published_estimates.csv
        derived/published_definitions.md
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"

COVERAGE = {
    "dhs_ohss_2022": "13% at arrival, declining 7.5% per year of presence",
    "pew_2023": "applied; rate not printed in the report",
    "cms_2024": "5% for 1982-2020 arrivals, 37% for 2021-2024 arrivals (16% overall)",
    "mpi_2024": "applied; rate not printed in the commentary",
    "mpi_2023_factsheet": "applied; rate not printed",
    "cis_jan2025": "2.25% flat",
    "cis_jul2026": "2.25% flat",
}


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    s = json.loads((HERE / "sources.json").read_text())
    rows = []
    for e in s["estimates"]:
        rows.append({
            "id": e["id"],
            "organisation": e["org"],
            "reference_date": e["reference_date"],
            "estimate": e["estimate"],
            "estimate_coverage_adjusted": e.get("estimate_coverage_adjusted"),
            "survey": e["survey"],
            "includes_parole_tps_daca_pending_asylum": e["includes_quasi_legal"],
            "quasi_legal_count": (e.get("quasi_legal") or e.get("quasi_legal_max")
                                  or e.get("some_protection")),
            "coverage_adjustment": COVERAGE.get(e["id"], ""),
            "mexico_born": e.get("mexico_born"),
            "mexico_share_pct": e.get("mexico_share_pct"),
            "share_of_foreign_born_pct": e.get("share_of_foreign_born_pct"),
            "superseded_by": e.get("superseded_by"),
            "citation": e["citation"],
            "url": e["url"],
        })
    tab = pd.DataFrame(rows).sort_values(["reference_date", "organisation"])
    tab.to_csv(DERIVED / "published_estimates.csv", index=False)
    print(tab[["organisation", "reference_date", "estimate", "survey",
               "coverage_adjustment"]].to_string(index=False))

    lines = ["# Definitions, quoted from the primary documents", ""]
    for e in s["estimates"]:
        lines += [f"## {e['org']} — reference date {e['reference_date']}", "",
                  f"**Citation.** {e['citation']}  ",
                  f"**URL.** {e['url']}", ""]
        for key, label in [("definition_quote", "Definition"),
                           ("quasi_legal_quote", "Quasi-legal categories"),
                           ("method_quote", "Method"),
                           ("coverage_quote", "Coverage adjustment"),
                           ("mexico_share_quote", "Mexico share")]:
            if e.get(key):
                lines += [f"**{label}.** “{e[key]}”", ""]
    lines += ["## CBO, other foreign nationals", "",
              f"**Citation.** {s['cbo_ofn_net_immigration']['citation']}  ",
              f"**URL.** {s['cbo_ofn_net_immigration']['url']}", "",
              f"**Definition.** “{s['cbo_ofn_net_immigration']['definition_quote']}”", "",
              f"**Flows.** “{s['cbo_ofn_net_immigration']['flow_quote']}”", "",
              f"**2025.** “{s['cbo_ofn_net_immigration']['y2025_quote']}”", "",
              f"**2025 inflow decomposition.** “{s['cbo_ofn_net_immigration']['inflow_2025_quote']}”", ""]
    (DERIVED / "published_definitions.md").write_text("\n".join(lines))
    print(f"\nwrote {DERIVED / 'published_definitions.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

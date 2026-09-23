#!/usr/bin/env python3
"""DHCS's published monthly enrollment in the status-blind full-scope Medi-Cal expansions.

Four CalHHS open-data tables (DHCS, from MEDS), fetched by fetch_sources.py:
  SB 75 children under 19 (since May 2016), Young Adult Expansion 19-25 (Jan 2020),
  Adult Expansion 26-49 (Jan 2024), Older Adult Expansion 50+ (May 2022).
Statewide rows are used where DHCS publishes them (19-25, 50+); otherwise counties are summed,
which omits suppressed small cells (the count of suppressed cells is reported). DHCS's own notes:
the 19-25, 26-49 and 50+ counts include lawfully present individuals in the same state-only aid
codes, so these tables are "UIS plus some lawfully present", not UIS alone.

Writes derived/dhcs_uis_monthly.csv and derived/dhcs_uis_windows.csv.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
TABLES = {  # file, period column, value column, age band (CPS band label)
    "0-18": ("sb75_children_under19.csv", "Eligibility Date", "Number of Beneficiaries"),
    "19-25": ("yae_19_25.csv", "Reporting Period", "Number of Eligible Individuals"),
    "26-49": ("ae_26_49.csv", "Reporting Period", "Number of Eligible Individuals"),
    "50+": ("oae_50plus.csv", "Reporting Period", "Number of Eligible Individuals"),
}
STATEWIDE = {"Statewide", "Statewide Total"}
WINDOWS = {  # label -> months (inclusive)
    "CY2024_average": ("2024-01", "2024-12"),
    "Dec2024": ("2024-12", "2024-12"),
    "Feb_Apr2025_average": ("2025-02", "2025-04"),
    "FY2024_25_average": ("2024-07", "2025-06"),
    "FY2025_26_average": ("2025-07", "2026-06"),
    "Jun2026": ("2026-06", "2026-06"),
}


def month(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s.astype(str), format="mixed").dt.strftime("%Y-%m")


def monthly() -> pd.DataFrame:
    rows = []
    for band, (f, pc, vc) in TABLES.items():
        t = pd.read_csv(CACHE / f, encoding="utf-8-sig")
        t["month"] = month(t[pc])
        t["v"] = pd.to_numeric(t[vc].astype(str).str.replace(",", ""), errors="coerce")
        sw = t[t.County.isin(STATEWIDE)].groupby("month").v.sum()
        cty = t[~t.County.isin(STATEWIDE)]
        csum = cty.groupby("month").v.sum()
        supp = cty[cty.v.isna()].groupby("month").size()
        for m in sorted(set(csum.index) | set(sw.index)):
            has_sw = m in sw.index and sw[m] > 0
            rows.append({"month": m, "age": band, "enrolled": float(sw[m] if has_sw else csum.get(m, 0.0)),
                         "source_row": "statewide" if has_sw else "county_sum",
                         "county_sum": float(csum.get(m, 0.0)), "suppressed_cells": int(supp.get(m, 0))})
    return pd.DataFrame(rows)


def main():
    m = monthly()
    wide = m.pivot(index="month", columns="age", values="enrolled").fillna(0.0)
    wide["all_ages"] = wide.sum(axis=1)
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    m.to_csv(out / "dhcs_uis_monthly_long.csv", index=False)
    wide.reset_index().to_csv(out / "dhcs_uis_monthly.csv", index=False)
    rows = []
    for label, (a, b) in WINDOWS.items():
        w = wide.loc[(wide.index >= a) & (wide.index <= b)]
        r = {"window": label, "months": len(w)}
        r.update({c: round(float(w[c].mean())) for c in wide.columns})
        rows.append(r)
    win = pd.DataFrame(rows)
    win.to_csv(out / "dhcs_uis_windows.csv", index=False)
    pd.set_option("display.width", 200)
    print(win.to_string(index=False))
    print(wide.loc["2023-12":"2026-06"].round(0).to_string())


if __name__ == "__main__":
    main()

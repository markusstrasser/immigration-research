"""Q1: BBD migration-related policy-uncertainty and migration-fear indices (US, UK, DE, FR).

Inputs (downloaded to _cache/ if absent):
- Migration_Fear_EPU_Data.xlsx, policyuncertainty.com/immigration_fear.html. Quarterly; each index is
  the count of newspaper articles with migration (M) AND economy, policy, uncertainty terms (EPU) or M AND
  fear terms, divided by all articles, normalized to mean 100 over 1995-2011 (site text).
- Categorical_EPU_Data.xlsx, policyuncertainty.com/categorical_epu.html. Monthly US overall EPU and 11
  categories; it has no immigration category ("immigration policy" is one term in the regulation list).

Outputs: derived/q1_migration_epu_annual.csv, derived/q1_migration_epu_summary.csv.
"""
import csv
import pathlib
import urllib.request

import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
URLS = {
    "migration_fear_epu.xlsx": "https://www.policyuncertainty.com/media/Migration_Fear_EPU_Data.xlsx",
    "cat_epu.xlsx": "https://www.policyuncertainty.com/media/Categorical_EPU_Data.xlsx",
}
COUNTRIES = ["usa", "uk", "germany", "france"]


def fetch(name):
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        urllib.request.urlretrieve(URLS[name], path)
    return path


def main():
    mig = pd.read_excel(fetch("migration_fear_epu.xlsx"))
    mig = mig[pd.to_numeric(mig["year"], errors="coerce").notna()].copy()
    mig["year"] = mig["year"].astype(int)
    cat = pd.read_excel(fetch("cat_epu.xlsx"))
    cat = cat[pd.to_numeric(cat["Year"], errors="coerce").notna()].copy()
    cat["year"] = cat["Year"].astype(int)
    us_epu = cat.groupby("year")["1. Economic Policy Uncertainty"].mean()

    cols = [f"{c}_{k}" for c in COUNTRIES for k in ("epu_migrant_index", "fear_index")]
    annual = mig.groupby("year")[cols].mean()
    nq = mig.groupby("year").size()
    DERIVED.mkdir(exist_ok=True)
    with open(DERIVED / "q1_migration_epu_annual.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "quarters"] + cols + ["usa_overall_epu"])
        for y, row in annual.iterrows():
            w.writerow([y, int(nq[y])] + [f"{row[c]:.1f}" if pd.notna(row[c]) else "" for c in cols]
                       + [f"{us_epu[y]:.1f}" if y in us_epu.index else ""])

    with open(DERIVED / "q1_migration_epu_summary.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["country", "index", "mean_1995_2011", "mean_2015", "mean_2016", "mean_2024", "mean_2025",
                    "max_value", "max_quarter", "last_value", "last_quarter"])
        for c in COUNTRIES:
            for k in ("epu_migrant_index", "fear_index"):
                s = mig[["year", "quarter", f"{c}_{k}"]].dropna()
                v = s[f"{c}_{k}"]
                base = v[(s.year >= 1995) & (s.year <= 2011)].mean()
                ym = lambda y: v[s.year == y].mean()  # noqa: E731
                i = v.idxmax()
                last = s.iloc[-1]
                w.writerow([c, k, f"{base:.1f}"] + [f"{ym(y):.1f}" if (s.year == y).any() else ""
                                                    for y in (2015, 2016, 2024, 2025)]
                           + [f"{v[i]:.1f}", f"{int(s.year[i])}Q{int(s.quarter[i])}",
                              f"{last[f'{c}_{k}']:.1f}", f"{int(last.year)}Q{int(last.quarter)}"])


if __name__ == "__main__":
    main()

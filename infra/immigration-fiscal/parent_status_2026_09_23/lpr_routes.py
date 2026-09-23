#!/usr/bin/env python3
"""How Mexico-born people obtain green cards: DHS OHSS counts by major class, FY2005-2022.

Question (operator, 2026-09-23): how easy is it to get legal status?

Source workbook (DHS Office of Immigration Statistics, persons obtaining lawful permanent resident
status by region and country of birth, one sheet per major class):
`sources/immigration-fiscal/data/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx`.
The workbook carries family, employment and diversity classes only; refugees, asylees and "other"
(including cancellation of removal) are not in it, so totals are totals of these classes.

Run from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/parent_status_2026_09_23/lpr_routes.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BOOK = ROOT / "sources/immigration-fiscal/data/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx"


def country_row(sheet: pd.DataFrame, name: str, first: bool = False) -> pd.Series:
    header = sheet.index[sheet[0].astype(str).str.strip().eq("Region and country of birth")][0]
    years = [int(float(y)) for y in sheet.loc[header, 1:].dropna()]
    hit = sheet.index[sheet[0].astype(str).str.strip().eq(name)]
    if len(hit) != 1 and not (first and len(hit) > 1):
        raise ValueError(f"{name!r} matched {len(hit)} rows")
    vals = pd.to_numeric(sheet.loc[hit[0], 1:len(years)], errors="coerce")
    return pd.Series(vals.to_numpy(), index=years)


def main():
    book = pd.ExcelFile(BOOK)
    rows = {}
    for sheet_name in book.sheet_names[1:]:
        sheet = pd.read_excel(BOOK, sheet_name=sheet_name, header=None)
        rows[(sheet_name, "Mexico")] = country_row(sheet, "Mexico")
        rows[(sheet_name, "Total")] = country_row(sheet, "Total", first=True)   # top-of-sheet grand total
    t = pd.DataFrame(rows).T
    t.index.names = ["class", "country"]
    mex = t.xs("Mexico", level="country")
    tot = t.xs("Total", level="country")
    summary = pd.DataFrame({
        "mexico_mean_2005_2022": mex.mean(axis=1).round(0),
        "mexico_share_of_class": (mex.sum(axis=1) / tot.sum(axis=1)).round(3),
        "share_of_mexico_listed_classes": (mex.sum(axis=1) / mex.sum().sum()).round(3),
    })
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    t.to_csv(out / "lpr_class_by_year_mexico_and_total.csv")
    summary.to_csv(out / "lpr_class_summary_mexico.csv")
    pd.set_option("display.width", 200)
    print(summary.to_string())
    print("\nMexico, listed classes, by year:")
    print(mex.sum().astype(int).to_string())


if __name__ == "__main__":
    main()

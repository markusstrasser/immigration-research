"""Parse OHSS Immigration Enforcement and Legal Processes monthly tables (Nov 2024).

Source: ohss.dhs.gov, file 2025_0116_ohss_immigration-enforcement-and-legal-processes-tables-november-2024.xlsx

Outputs (data/cbp/):
- swb_encounters_by_citizenship_monthly.parquet — SWB encounter time series by citizenship × month
- chnv_paroles_monthly.parquet — Confirmed CHNV paroles by program × month
- swb_encounters_by_sector_monthly.parquet — SWB encounter time series by sector × month
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import calendar

DATA = Path(__file__).parent.parent / "data" / "cbp"
XLSX = DATA / "ohss_enforcement_nov2024.xlsx"

MONTHS = {m: i + 1 for i, m in enumerate(["October", "November", "December", "January", "February", "March", "April", "May", "June", "July", "August", "September"])}
# US fiscal year: Oct y-1 → Sep y. So FY2023 October = Oct 2022.


def _fy_month_to_calendar(fy: int, month_name: str) -> tuple[int, int] | None:
    if month_name == "Total" or pd.isna(month_name):
        return None
    if month_name in ("October", "November", "December"):
        return (fy - 1, MONTHS[month_name])
    return (fy, MONTHS[month_name])


def parse_swb_by_citizenship() -> pd.DataFrame:
    raw = pd.read_excel(XLSX, "SWB Encounters by Citizenship", header=None)
    # Headers at row 3: Fiscal Year, Month, Total, Mexico, Venezuela, Guatemala, Cuba, Honduras, El Salvador, Colombia, Nicaragua, China, Ecuador, India, Haiti, Brazil, Peru, Russia, Turkey, Romania, Mauritania, ...
    headers = raw.iloc[3, :].tolist()
    rows = []
    current_fy = None
    for i in range(4, len(raw)):
        row = raw.iloc[i].tolist()
        if pd.notna(row[0]) and isinstance(row[0], (int, float)):
            current_fy = int(row[0])
        month = row[1]
        cal = _fy_month_to_calendar(current_fy, month) if current_fy else None
        if cal is None:
            continue
        cal_year, cal_month = cal
        d = {"fy": current_fy, "fy_month": month, "year": cal_year, "month": cal_month, "date": pd.Timestamp(cal_year, cal_month, 1)}
        for j, h in enumerate(headers):
            if pd.isna(h) or h in ("Fiscal Year", "Month"):
                continue
            v = row[j]
            d[str(h)] = pd.to_numeric(v, errors="coerce")
        rows.append(d)
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def parse_chnv() -> pd.DataFrame:
    raw = pd.read_excel(XLSX, "CHNV Paroles", header=None)
    headers = raw.iloc[2, :].tolist()  # Fiscal Year, Month, Total, Cuba, Haiti, Nicaragua, Venezuela
    rows = []
    current_fy = None
    for i in range(3, len(raw)):
        row = raw.iloc[i].tolist()
        if pd.notna(row[0]) and isinstance(row[0], (int, float)):
            current_fy = int(row[0])
        month = row[1]
        cal = _fy_month_to_calendar(current_fy, month) if current_fy else None
        if cal is None:
            continue
        cal_year, cal_month = cal
        d = {"fy": current_fy, "fy_month": month, "year": cal_year, "month": cal_month, "date": pd.Timestamp(cal_year, cal_month, 1)}
        for j, h in enumerate(headers):
            if pd.isna(h) or h in ("Fiscal Year", "Month"):
                continue
            v = row[j]
            d[str(h)] = pd.to_numeric(v, errors="coerce") if v != "X" else None
        rows.append(d)
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def parse_swb_by_sector() -> pd.DataFrame:
    raw = pd.read_excel(XLSX, "SWB Enc by Sector+Field Ofc", header=None)
    # Need to inspect; for now just save raw
    return raw


def main():
    citizenship = parse_swb_by_citizenship()
    print(f"SWB Encounters by Citizenship: {len(citizenship)} months, {len([c for c in citizenship.columns if c not in ('fy','fy_month','year','month','date')])} citizenships")
    print("Sample (last 5 months, key columns):")
    keep = ["date", "Total", "Mexico", "Venezuela", "Cuba", "Haiti", "Nicaragua", "Guatemala", "Honduras", "El Salvador"]
    keep = [c for c in keep if c in citizenship.columns]
    print(citizenship[keep].tail(5).to_string(index=False))
    citizenship.to_parquet(DATA / "swb_encounters_by_citizenship_monthly.parquet", index=False)

    chnv = parse_chnv()
    print(f"\nCHNV Paroles: {len(chnv)} months")
    print(chnv[["date", "Total", "Cuba", "Haiti", "Nicaragua", "Venezuela"]].to_string(index=False))
    chnv.to_parquet(DATA / "chnv_paroles_monthly.parquet", index=False)

    print("\nWrote: swb_encounters_by_citizenship_monthly.parquet, chnv_paroles_monthly.parquet")


if __name__ == "__main__":
    main()

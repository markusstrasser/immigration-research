#!/usr/bin/env python3
"""Parse USDA SNAP FY state participation/benefits from NDB public xlsx zip."""
from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

STAGE5_EXT = data_root() / "external" / "stage5_net_negative"
OUT = derived_root() / "stage5"
SNAP_ZIP = STAGE5_EXT / "usda" / "snap-zip-fy69tocurrent-6.zip"

SKIP_REGIONS = frozenset({"NERO", "MARO", "SERO", "MWRO", "SWRO", "MPRO", "WRO", "US Summary"})

STATE_NAME_TO_FIPS = {
    "Alabama": "01", "Alaska": "02", "Arizona": "04", "Arkansas": "05", "California": "06",
    "Colorado": "08", "Connecticut": "09", "Delaware": "10", "District of Columbia": "11",
    "Florida": "12", "Georgia": "13", "Hawaii": "15", "Idaho": "16", "Illinois": "17",
    "Indiana": "18", "Iowa": "19", "Kansas": "20", "Kentucky": "21", "Louisiana": "22",
    "Maine": "23", "Maryland": "24", "Massachusetts": "25", "Michigan": "26", "Minnesota": "27",
    "Mississippi": "28", "Missouri": "29", "Montana": "30", "Nebraska": "31", "Nevada": "32",
    "New Hampshire": "33", "New Jersey": "34", "New Mexico": "35", "New York": "36",
    "North Carolina": "37", "North Dakota": "38", "Ohio": "39", "Oklahoma": "40", "Oregon": "41",
    "Pennsylvania": "42", "Rhode Island": "44", "South Carolina": "45", "South Dakota": "46",
    "Tennessee": "47", "Texas": "48", "Utah": "49", "Vermont": "50", "Virginia": "51",
    "Washington": "53", "West Virginia": "54", "Wisconsin": "55", "Wyoming": "56",
    "Puerto Rico": "72",
}


def _parse_fy_workbook(xlsx: bytes | Path, fy: int) -> pd.DataFrame:
    raw = xlsx if isinstance(xlsx, bytes) else Path(xlsx).read_bytes()
    xl = pd.ExcelFile(BytesIO(raw))
    rows: list[dict] = []
    for sheet in xl.sheet_names:
        if sheet == "US Summary":
            continue
        df = pd.read_excel(BytesIO(raw), sheet_name=sheet, header=None)
        state: str | None = None
        for _, row in df.iterrows():
            label = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
            if not label or label == "nan":
                continue
            if pd.isna(row.iloc[1]) and pd.isna(row.iloc[2]) and pd.isna(row.iloc[3]):
                if label not in {"Fiscal Year and Month", "Participation 1/", "Household"} and label not in SKIP_REGIONS:
                    state = label
                continue
            if state and label == "Total":
                if state in SKIP_REGIONS:
                    state = None
                    continue
                rows.append(
                    {
                        "state_name": state,
                        "snap_households_avg": pd.to_numeric(row.iloc[1], errors="coerce"),
                        "snap_persons_avg": pd.to_numeric(row.iloc[2], errors="coerce"),
                        "snap_benefits_usd": pd.to_numeric(row.iloc[3], errors="coerce"),
                        "snap_benefit_per_household": pd.to_numeric(row.iloc[4], errors="coerce"),
                        "snap_benefit_per_person": pd.to_numeric(row.iloc[5], errors="coerce"),
                        "fy": fy,
                        "source": "usda_snap_ndb_public",
                    }
                )
                state = None
    out = pd.DataFrame(rows)
    out["state_fips"] = out["state_name"].map(STATE_NAME_TO_FIPS)
    out = out.dropna(subset=["state_fips"]).drop_duplicates("state_fips", keep="first")
    out["state_fips"] = out["state_fips"].astype(str).str.zfill(2)
    return out


def build_snap_state_panel(fy: int = 2023, out_dir: Path | None = None) -> pd.DataFrame:
    if not SNAP_ZIP.exists():
        return pd.DataFrame()
    member = f"FY{fy % 100:02d}.xlsx"
    with zipfile.ZipFile(SNAP_ZIP) as zf:
        if member not in zf.namelist():
            return pd.DataFrame()
        panel = _parse_fy_workbook(zf.read(member), fy)
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    if len(panel):
        panel.to_csv(out / f"snap_state_{fy}.csv", index=False)
    print({"snap_state_rows": len(panel), "fy": fy}, flush=True)
    return panel


if __name__ == "__main__":
    build_snap_state_panel()

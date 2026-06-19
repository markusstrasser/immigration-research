#!/usr/bin/env python3
"""Roll up Census SAIPE school-district poverty to state totals (2023)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

USSD = data_root() / "external" / "stage4" / "saipe" / "ussd23.txt"
OUT = derived_root() / "stage5"


def build_saipe_state_school_poverty_panel(out_dir: Path | None = None) -> pd.DataFrame:
    if not USSD.exists():
        return pd.DataFrame()
    rows: list[dict] = []
    for line in USSD.read_text(encoding="latin-1").splitlines():
        if len(line) < 108:
            continue
        st = line[0:2].strip()
        if not st.isdigit() or st == "00":
            continue
        rows.append(
            {
                "state_fips": st.zfill(2),
                "district_id": line[3:8].strip(),
                "district_name": line[9:81].strip(),
                "total_population": pd.to_numeric(line[82:90].strip(), errors="coerce"),
                "school_age_5_17": pd.to_numeric(line[91:99].strip(), errors="coerce"),
                "school_age_poverty_5_17": pd.to_numeric(line[100:108].strip(), errors="coerce"),
            }
        )
    df = pd.DataFrame(rows)
    panel = (
        df.groupby("state_fips", as_index=False)
        .agg(
            saipe_school_age_5_17=("school_age_5_17", "sum"),
            saipe_school_age_poverty_5_17=("school_age_poverty_5_17", "sum"),
            saipe_district_count=("district_id", "nunique"),
        )
        .assign(
            saipe_school_poverty_rate=lambda x: x["saipe_school_age_poverty_5_17"]
            / x["saipe_school_age_5_17"].replace(0, pd.NA),
            vintage_year=2023,
            source="census_saipe_ussd23",
        )
    )
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / "saipe_state_school_poverty_2023.csv", index=False)
    print({"saipe_state_rows": len(panel)}, flush=True)
    return panel


if __name__ == "__main__":
    build_saipe_state_school_poverty_panel()

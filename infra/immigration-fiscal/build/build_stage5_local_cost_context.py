#!/usr/bin/env python3
"""Stage-5 local-cost context: EL (2017-18), BEA RPP, CMS Medicaid, receiver cities.

Spec: research/immigration-net-negative-dataset-frontier-2026-06-15.md
"""
from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

DATA = data_root()
STAGE5 = DATA / "external" / "stage5_net_negative"
OUT = derived_root() / "stage5"

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


def build_bea_state_rpp() -> pd.DataFrame:
    path = STAGE5 / "bea" / "rpp_state_metro_2024.xlsx"
    if not path.exists():
        return pd.DataFrame(columns=["state_fips", "rpp_all_items_2023"])
    raw = pd.read_excel(path, sheet_name="Table 2", header=None)
    rows = []
    for _, row in raw.iterrows():
        name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        if name not in STATE_NAME_TO_FIPS:
            continue
        rpp = pd.to_numeric(row.iloc[1], errors="coerce")
        if pd.isna(rpp):
            continue
        rows.append({"state_name": name, "state_fips": STATE_NAME_TO_FIPS[name], "rpp_all_items_2023": rpp})
    return pd.DataFrame(rows)


def build_cms_state_medicaid() -> pd.DataFrame:
    path = STAGE5 / "cms" / "medicaid_financial_management.csv"
    if not path.exists():
        return pd.DataFrame(columns=["state_name", "medicaid_total_computable", "medicaid_year"])
    df = pd.read_csv(path, low_memory=False)
    df["Total Computable"] = pd.to_numeric(df["Total Computable"], errors="coerce").fillna(0)
    med = df[df["Program"].astype(str).str.contains("Medical Assistance", na=False)]
    if med.empty:
        med = df
    latest = int(med["Year"].max())
    agg = (
        med[med["Year"] == latest]
        .groupby("State", as_index=False)["Total Computable"]
        .sum()
        .rename(columns={"State": "state_name", "Total Computable": "medicaid_total_computable"})
        .assign(medicaid_year=latest)
    )
    agg["state_fips"] = agg["state_name"].map(STATE_NAME_TO_FIPS)
    return agg


def build_state_el_2018() -> pd.DataFrame:
    zpath = STAGE5 / "nces" / "ccd_lea_141_1718_english_learners.zip"
    if not zpath.exists():
        return pd.DataFrame(columns=["state_fips", "lep_count_reported", "districts_with_el"])
    with zipfile.ZipFile(zpath) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".csv"))
        df = pd.read_csv(BytesIO(zf.read(name)), dtype=str, low_memory=False)
    df["LEP_COUNT"] = pd.to_numeric(df["LEP_COUNT"], errors="coerce")
    reported = df[df["DMS_FLAG"].astype(str).str.lower().eq("reported")].copy()
    reported["state_fips"] = reported["FIPST"].astype(str).str.zfill(2)
    state = (
        reported.groupby("state_fips", as_index=False)
        .agg(lep_count_reported=("LEP_COUNT", "sum"), districts_with_el=("LEAID", "nunique"))
        .assign(el_school_year="2017-2018", el_source="nces_ccd_lea_141_1718")
    )
    return state


def build_receiver_costs() -> pd.DataFrame:
    path = STAGE5 / "receiver" / "receiver_city_migrant_costs.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def build_state_stage5_context() -> pd.DataFrame:
    rpp = build_bea_state_rpp()
    med = build_cms_state_medicaid()
    el = build_state_el_2018()
    state = rpp.merge(med.drop(columns=["state_name"], errors="ignore"), on="state_fips", how="outer")
    state = state.merge(el, on="state_fips", how="outer")
    return state.sort_values("state_fips")


def load_stage5_into_duckdb(con, stage5_dir: Path) -> None:
    paths = {
        "state_stage5_context_2023": stage5_dir / "state_stage5_context_2023.csv",
        "receiver_city_migrant_costs": stage5_dir / "receiver_city_migrant_costs.csv",
        "state_el_lep_2018": stage5_dir / "state_el_lep_2018.csv",
    }
    for table, path in paths.items():
        if path.exists():
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{path}', header=true)")

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_stage2_context_2023'"
    ).fetchone()[0]:
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_stage5_context_2023 AS
            SELECT
              s.*,
              st.rpp_all_items_2023,
              st.medicaid_total_computable,
              st.medicaid_year,
              st.lep_count_reported,
              st.districts_with_el,
              st.el_school_year
            FROM origin_puma_household_stage2_context_2023 s
            LEFT JOIN state_stage5_context_2023 st ON s.state_fips = st.state_fips
        """)

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_fullstock_stage2_context_2023'"
    ).fetchone()[0]:
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_fullstock_stage5_context_2023 AS
            SELECT
              s.*,
              st.rpp_all_items_2023,
              st.medicaid_total_computable,
              st.medicaid_year,
              st.lep_count_reported,
              st.districts_with_el,
              st.el_school_year
            FROM origin_puma_household_fullstock_stage2_context_2023 s
            LEFT JOIN state_stage5_context_2023 st ON s.state_fips = st.state_fips
        """)


def build_stage5(out_dir: Path | None = None) -> dict:
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)

    state = build_state_stage5_context()
    el = build_state_el_2018()
    rcv = build_receiver_costs()

    state.to_csv(out / "state_stage5_context_2023.csv", index=False)
    el.to_csv(out / "state_el_lep_2018.csv", index=False)
    if len(rcv):
        rcv.to_csv(out / "receiver_city_migrant_costs.csv", index=False)

    meta = {
        "state_rows": int(len(state)),
        "states_with_rpp": int(state["rpp_all_items_2023"].notna().sum()),
        "states_with_medicaid": int(state["medicaid_total_computable"].notna().sum()),
        "states_with_el": int(state["lep_count_reported"].notna().sum()),
        "receiver_city_rows": int(len(rcv)),
    }
    (out / "stage5_outputs.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))
    return meta


if __name__ == "__main__":
    build_stage5()

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

from parse_acs_stage5_panels import build_acs_stage5_panels
from parse_cms_medicaid_state_panel import build_cms_medicaid_state_panel
from parse_census_state_per_pupil import build_census_state_per_pupil_panel
from parse_ohss_state_immigration_panel import build_ohss_state_immigration_panel
from parse_safmr_panel import build_safmr_panels
from parse_saipe_state_school_poverty import build_saipe_state_school_poverty_panel
from parse_snap_state_panel import build_snap_state_panel
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


def _norm_fips(df: pd.DataFrame, col: str = "state_fips") -> pd.DataFrame:
    out = df.copy()
    out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=[col])
    out[col] = out[col].astype(int).astype(str).str.zfill(2)
    return out


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
    return _norm_fips(agg)


def build_state_el_panel() -> pd.DataFrame:
    for zname, year, source in (
        ("ccd_lea_141_1819_english_learners.zip", "2018-2019", "nces_ccd_lea_141_1819"),
        ("ccd_lea_141_1718_english_learners.zip", "2017-2018", "nces_ccd_lea_141_1718"),
    ):
        zpath = STAGE5 / "nces" / zname
        if not zpath.exists():
            continue
        with zipfile.ZipFile(zpath) as zf:
            name = next(n for n in zf.namelist() if n.endswith(".csv"))
            df = pd.read_csv(BytesIO(zf.read(name)), dtype=str, low_memory=False)
        df["LEP_COUNT"] = pd.to_numeric(df["LEP_COUNT"], errors="coerce")
        reported = df[df["DMS_FLAG"].astype(str).str.lower().eq("reported")].copy()
        reported["state_fips"] = reported["FIPST"].astype(str).str.zfill(2)
        state = (
            reported.groupby("state_fips", as_index=False)
            .agg(lep_count_reported=("LEP_COUNT", "sum"), districts_with_el=("LEAID", "nunique"))
            .assign(el_school_year=year, el_source=source)
        )
        return state
    return pd.DataFrame(columns=["state_fips", "lep_count_reported", "districts_with_el"])


def build_state_el_2018() -> pd.DataFrame:
    return build_state_el_panel()


def build_receiver_costs() -> pd.DataFrame:
    path = STAGE5 / "receiver" / "receiver_city_migrant_costs.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def build_state_stage5_context(
    safmr_state: pd.DataFrame | None = None,
    snap_state: pd.DataFrame | None = None,
) -> pd.DataFrame:
    rpp = _norm_fips(build_bea_state_rpp())
    med = _norm_fips(build_cms_state_medicaid())
    el = _norm_fips(build_state_el_panel())
    state = rpp.merge(med.drop(columns=["state_name"], errors="ignore"), on="state_fips", how="outer")
    state = state.merge(el, on="state_fips", how="outer")
    if safmr_state is not None and len(safmr_state):
        safmr_state = _norm_fips(safmr_state.copy())
        state = state.merge(
            safmr_state.drop(columns=["fy", "source"], errors="ignore"),
            on="state_fips",
            how="left",
        )
    if snap_state is not None and len(snap_state):
        snap_state = _norm_fips(snap_state.copy())
        state = state.merge(
            snap_state.drop(columns=["state_name", "fy", "source"], errors="ignore"),
            on="state_fips",
            how="left",
        )
    return state.drop_duplicates("state_fips", keep="first").sort_values("state_fips")


def load_stage5_into_duckdb(con, stage5_dir: Path) -> None:
    paths = {
        "state_stage5_context_2023": stage5_dir / "state_stage5_context_2023.csv",
        "receiver_city_migrant_costs": stage5_dir / "receiver_city_migrant_costs.csv",
        "state_el_lep_2018": stage5_dir / "state_el_lep_2018.csv",
        "safmr_zip_2025": stage5_dir / "safmr_zip_2025.csv",
        "safmr_county_2025": stage5_dir / "safmr_county_2025.csv",
        "safmr_puma_2025": stage5_dir / "safmr_puma_2025.csv",
        "safmr_state_2025": stage5_dir / "safmr_state_2025.csv",
        "snap_state_2023": stage5_dir / "snap_state_2023.csv",
        "acs_immigrant_health_state_summary_2023": stage5_dir / "acs_immigrant_health_state_summary_2023.csv",
        "acs_foreign_born_school_age_state_2023": stage5_dir / "acs_foreign_born_school_age_state_2023.csv",
        "saipe_state_school_poverty_2023": stage5_dir / "saipe_state_school_poverty_2023.csv",
        "census_state_per_pupil_2023": stage5_dir / "census_state_per_pupil_2023.csv",
        "ohss_state_immigration_2023": stage5_dir / "ohss_state_immigration_2023.csv",
        "cms_medicaid_state_panel": stage5_dir / "cms_medicaid_state_panel.csv",
    }
    for table, path in paths.items():
        if path.exists():
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{path}', header=true)")

    eoir_dir = stage5_dir.parent / "stage4" / "eoir"
    for table, fname in (
        ("eoir_pending_cases_fy", "eoir_pending_cases_fy.csv"),
        ("eoir_court_workload_historical_fy", "eoir_court_workload_historical_fy.csv"),
        ("eoir_amnesty_cases_by_state", "eoir_amnesty_cases_by_state.csv"),
    ):
        path = eoir_dir / fname
        if path.exists():
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{path}', header=true)")

    has_puma_safmr = bool(
        con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='safmr_puma_2025'"
        ).fetchone()[0]
    )
    puma_col = "p.safmr_2br_wtd AS safmr_2br_puma_2025," if has_puma_safmr else ""
    puma_join = (
        "LEFT JOIN safmr_puma_2025 p ON s.state_fips = p.state_fips AND s.puma_code = p.puma_code"
        if has_puma_safmr
        else ""
    )
    stage5_cols = f"""
              st.rpp_all_items_2023,
              st.medicaid_total_computable,
              st.medicaid_year,
              st.lep_count_reported,
              st.districts_with_el,
              st.el_school_year,
              st.safmr_2br_median_2025,
              st.safmr_2br_mean_2025,
              st.county_count,
              st.snap_households_avg,
              st.snap_persons_avg,
              st.snap_benefits_usd,
              st.snap_benefit_per_person,
              {puma_col.rstrip(",")}
    """.rstrip()
    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_stage2_context_2023'"
    ).fetchone()[0]:
        con.execute(f"""
            CREATE OR REPLACE TABLE origin_puma_household_stage5_context_2023 AS
            SELECT
              s.*,
              {stage5_cols}
            FROM origin_puma_household_stage2_context_2023 s
            LEFT JOIN state_stage5_context_2023 st ON s.state_fips = st.state_fips
            {puma_join}
        """)

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_fullstock_stage2_context_2023'"
    ).fetchone()[0]:
        con.execute(f"""
            CREATE OR REPLACE TABLE origin_puma_household_fullstock_stage5_context_2023 AS
            SELECT
              s.*,
              {stage5_cols}
            FROM origin_puma_household_fullstock_stage2_context_2023 s
            LEFT JOIN state_stage5_context_2023 st ON s.state_fips = st.state_fips
            {puma_join}
        """)


def build_stage5(out_dir: Path | None = None) -> dict:
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)

    safmr_meta = build_safmr_panels(out)
    cms_meta = build_cms_medicaid_state_panel(out)
    health_rows, school_age_rows = build_acs_stage5_panels(out)
    saipe_df = build_saipe_state_school_poverty_panel(out)
    nces_pp = build_census_state_per_pupil_panel(out)
    ohss_df = build_ohss_state_immigration_panel(2023, out)
    snap_df = build_snap_state_panel(2023, out)
    safmr_state_path = out / "safmr_state_2025.csv"
    safmr_state = pd.read_csv(safmr_state_path) if safmr_state_path.exists() else pd.DataFrame()

    state = build_state_stage5_context(
        safmr_state if len(safmr_state) else None,
        snap_df if len(snap_df) else None,
    )
    state["state_fips"] = state["state_fips"].astype(str).str.zfill(2)
    for extra in (saipe_df, nces_pp):
        if extra is not None and len(extra):
            extra = _norm_fips(extra.copy())
            state = state.merge(
                extra.drop(columns=["state_name", "source", "vintage_year", "school_year"], errors="ignore"),
                on="state_fips",
                how="left",
            )
    state = state.drop_duplicates("state_fips", keep="first")
    el = build_state_el_panel()
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
        "states_with_safmr": int(state.get("safmr_2br_median_2025", pd.Series(dtype=float)).notna().sum()),
        "states_with_snap": int(state.get("snap_persons_avg", pd.Series(dtype=float)).notna().sum()),
        "snap_state_rows": int(len(snap_df)),
        "receiver_city_rows": int(len(rcv)),
        **safmr_meta,
        "cms_medicaid_state_rows": int(len(cms_meta)),
        "acs_health_state_rows": int(health_rows),
        "acs_fb_school_age_state_rows": int(school_age_rows),
        "saipe_state_rows": int(len(saipe_df)),
        "census_state_per_pupil_rows": int(len(nces_pp)),
        "ohss_state_rows": int(len(ohss_df)),
    }
    (out / "stage5_outputs.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))
    return meta


if __name__ == "__main__":
    build_stage5()

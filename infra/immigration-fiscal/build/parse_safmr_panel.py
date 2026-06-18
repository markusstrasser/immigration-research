#!/usr/bin/env python3
"""Parse HUD SAFMR xlsx into zip/county/PUMA rent panels."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

STAGE5_EXT = data_root() / "external" / "stage5_net_negative"
OUT = derived_root() / "stage5"
SAFMR_XLSX = STAGE5_EXT / "hud" / "fy2025_safmrs_revised.xlsx"
ZCTA_COUNTY = data_root() / "external/stage2/census/geo/tab20_zcta520_county20_natl.txt"
PUMA_XWALK = derived_root() / "stage2/puma_county_area_xwalk_2023.csv"


def _clean_safmr_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for c in df.columns:
        key = c.replace("\n", "").replace(" ", "").lower()
        if key == "zipcode":
            rename[c] = "zip_code"
        elif key == "hudareacode":
            rename[c] = "hud_area_code"
        elif key.startswith("hudfairmarketrentareaname"):
            rename[c] = "hud_area_name"
        elif key.startswith("safmr0br") and "payment" not in key:
            rename[c] = "safmr_0br"
        elif key.startswith("safmr1br") and "payment" not in key:
            rename[c] = "safmr_1br"
        elif key.startswith("safmr2br") and "payment" not in key:
            rename[c] = "safmr_2br"
        elif key.startswith("safmr3br") and "payment" not in key:
            rename[c] = "safmr_3br"
        elif key.startswith("safmr4br") and "payment" not in key:
            rename[c] = "safmr_4br"
    out = df.rename(columns=rename)
    out["zip_code"] = out["zip_code"].astype(str).str.zfill(5)
    for col in ("safmr_0br", "safmr_1br", "safmr_2br", "safmr_3br", "safmr_4br"):
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def build_safmr_zip() -> pd.DataFrame:
    if not SAFMR_XLSX.exists():
        return pd.DataFrame()
    raw = pd.read_excel(SAFMR_XLSX, sheet_name="SAFMRs")
    out = _clean_safmr_columns(raw)
    return out.assign(fy=2025, source="hud_safmr_fy2025_revised")


def _weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    w = weights.fillna(0)
    v = values.where(w > 0)
    denom = w[v.notna()].sum()
    if denom <= 0:
        return float("nan")
    return float((v * w).sum() / denom)


def build_safmr_county(zip_df: pd.DataFrame) -> pd.DataFrame:
    if zip_df.empty or not ZCTA_COUNTY.exists():
        return pd.DataFrame()
    zc = pd.read_csv(
        ZCTA_COUNTY,
        sep="|",
        dtype=str,
        usecols=["GEOID_ZCTA5_20", "GEOID_COUNTY_20", "AREALAND_PART"],
    )
    zc = zc[zc["GEOID_ZCTA5_20"].astype(str).str.len() == 5].copy()
    zc["AREALAND_PART"] = pd.to_numeric(zc["AREALAND_PART"], errors="coerce").fillna(0)
    merged = zip_df.merge(zc, left_on="zip_code", right_on="GEOID_ZCTA5_20", how="inner")
    rows = []
    for county, g in merged.groupby("GEOID_COUNTY_20"):
        rows.append(
            {
                "county_fips": county,
                "state_fips": county[:2],
                "safmr_2br_wtd": _weighted_mean(g["safmr_2br"], g["AREALAND_PART"]),
                "zip_count": int(g["zip_code"].nunique()),
                "fy": 2025,
                "source": "hud_safmr_fy2025_revised",
            }
        )
    return pd.DataFrame(rows)


def build_safmr_puma(county_df: pd.DataFrame) -> pd.DataFrame:
    if county_df.empty or not PUMA_XWALK.exists():
        return pd.DataFrame()
    xw = pd.read_csv(PUMA_XWALK, dtype=str)
    xw["area_weight"] = pd.to_numeric(xw["area_weight"], errors="coerce").fillna(0)
    merged = county_df.merge(xw.drop(columns=["state_fips"], errors="ignore"), on="county_fips", how="inner")
    rows = []
    for (state, puma), g in merged.groupby(["state_fips", "puma_code"]):
        w = g["area_weight"]
        rows.append(
            {
                "state_fips": state,
                "puma_code": puma,
                "safmr_2br_wtd": _weighted_mean(g["safmr_2br_wtd"], w),
                "county_parts": int(len(g)),
                "fy": 2025,
                "source": "hud_safmr_fy2025_revised",
            }
        )
    return pd.DataFrame(rows)


def build_safmr_state(county_df: pd.DataFrame) -> pd.DataFrame:
    if county_df.empty:
        return pd.DataFrame()
    return (
        county_df.groupby("state_fips", as_index=False)
        .agg(
            safmr_2br_median_2025=("safmr_2br_wtd", "median"),
            safmr_2br_mean_2025=("safmr_2br_wtd", "mean"),
            county_count=("county_fips", "nunique"),
            fy=("fy", "first"),
            source=("source", "first"),
        )
        .assign(state_fips=lambda d: d["state_fips"].astype(str).str.zfill(2))
    )


def build_safmr_panels(out_dir: Path | None = None) -> dict:
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    zip_df = build_safmr_zip()
    county_df = build_safmr_county(zip_df)
    puma_df = build_safmr_puma(county_df)
    state_df = build_safmr_state(county_df)
    meta = {"zip_rows": 0, "county_rows": 0, "puma_rows": 0, "state_rows": 0}
    if not zip_df.empty:
        zip_df.to_csv(out / "safmr_zip_2025.csv", index=False)
        meta["zip_rows"] = len(zip_df)
    if not county_df.empty:
        county_df.to_csv(out / "safmr_county_2025.csv", index=False)
        meta["county_rows"] = len(county_df)
    if not puma_df.empty:
        puma_df.to_csv(out / "safmr_puma_2025.csv", index=False)
        meta["puma_rows"] = len(puma_df)
    if not state_df.empty:
        state_df.to_csv(out / "safmr_state_2025.csv", index=False)
        meta["state_rows"] = len(state_df)
    print(meta, flush=True)
    return meta


if __name__ == "__main__":
    build_safmr_panels()

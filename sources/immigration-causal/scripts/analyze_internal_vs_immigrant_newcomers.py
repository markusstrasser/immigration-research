"""Internal-native migration vs international immigration as comparable shocks.

Reframes: is the 'immigrant' or the 'newcomer in general' the right policy unit?

Approach:
1. Compute county-level inflow of native US filers (IRS SOI 2022-23, code y1=97)
2. Compute county-level recent-arrival foreign-born (ACS B05005)
3. For each county: compute "newcomer share" by type
4. Test: do counties receiving high native-migrant inflows show same school/housing/wage
   patterns as those receiving high immigrant inflows?

Output: data/analysis/county_newcomer_comparison.parquet
"""
from __future__ import annotations
from pathlib import Path
import requests
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
SOI = DATA / "internal_migration" / "county_inflow_2022_23.csv"
OUT = DATA / "analysis"


def load_soi_county_inflow() -> pd.DataFrame:
    """Aggregate IRS SOI county inflow to: county = total inflow from all-US (code 97)."""
    df = pd.read_csv(SOI, encoding="latin-1", dtype={
        "y2_statefips": str, "y2_countyfips": str,
        "y1_statefips": str, "y1_countyfips": str,
    })
    # y1 codes 96/97/98/95 are aggregate rows — keep "97" = Total Migration-US (excludes foreign)
    agg = df[df["y1_statefips"] == "97"].copy()
    agg["dest_state_fips"] = agg["y2_statefips"].str.zfill(2)
    agg["dest_county_fips"] = agg["y2_countyfips"].str.zfill(3)
    agg["dest_fips5"] = agg["dest_state_fips"] + agg["dest_county_fips"]
    agg = agg.rename(columns={"n1": "us_inflow_returns", "n2": "us_inflow_persons", "agi": "us_inflow_agi_kusd"})
    return agg[["dest_fips5", "dest_state_fips", "dest_county_fips", "us_inflow_returns", "us_inflow_persons", "us_inflow_agi_kusd"]]


def fetch_acs_county_population_and_recent_fb() -> pd.DataFrame:
    """Pull ACS 2022 5-yr county-level: total pop + foreign-born + recent-arrival FB.

    Variables:
    - B01003_001E: total population
    - B05002_013E: foreign-born population
    - B05005_002E + B05005_004E (combined ENT 2010-later approx): recent FB
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        "get": "NAME,B01003_001E,B05002_013E,B05002_001E,B25064_001E,B19013_001E",
        "for": "county:*",
    }
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns={
        "B01003_001E": "totpop",
        "B05002_013E": "fb_pop",
        "B05002_001E": "totpop_b05002",
        "B25064_001E": "median_rent",
        "B19013_001E": "median_hh_income",
    })
    for c in ("totpop", "fb_pop", "totpop_b05002", "median_rent", "median_hh_income"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    df["county_fips"] = df["county"].astype(str).str.zfill(3)
    df["fips5"] = df["state_fips"] + df["county_fips"]
    df["fb_share"] = df["fb_pop"] / df["totpop"]
    return df[["fips5", "state_fips", "county_fips", "NAME", "totpop", "fb_pop", "fb_share", "median_rent", "median_hh_income"]]


def fetch_acs_recent_fb() -> pd.DataFrame:
    """Recent-arrival foreign-born by county. B05005 is by year of entry; sum 2010-later."""
    url = "https://api.census.gov/data/2022/acs/acs5"
    # B05005_002E = entered 2010 or later (foreign-born subtotal)
    params = {
        "get": "B05005_002E",
        "for": "county:*",
    }
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["recent_fb_2010plus"] = pd.to_numeric(df["B05005_002E"], errors="coerce")
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    df["county_fips"] = df["county"].astype(str).str.zfill(3)
    df["fips5"] = df["state_fips"] + df["county_fips"]
    return df[["fips5", "recent_fb_2010plus"]]


def main():
    print("Loading IRS SOI...")
    soi = load_soi_county_inflow()
    print(f"  {len(soi)} county destinations with US-inflow data")

    print("Loading ACS county totals...")
    acs = fetch_acs_county_population_and_recent_fb()
    print(f"  {len(acs)} ACS counties")

    print("Loading ACS recent-arrival FB (B05005)...")
    try:
        rfb = fetch_acs_recent_fb()
        print(f"  {len(rfb)} county recent-FB rows")
        acs = acs.merge(rfb, on="fips5", how="left")
    except Exception as e:
        print(f"  recent-FB fetch failed: {e}")

    merged = acs.merge(soi, left_on="fips5", right_on="dest_fips5", how="left")
    merged["us_inflow_persons"] = merged["us_inflow_persons"].fillna(0)
    merged["us_inflow_share"] = merged["us_inflow_persons"] / merged["totpop"]
    if "recent_fb_2010plus" in merged.columns:
        # Recent FB stock is 12-yr accumulation; rough annual avg = total/12
        merged["recent_fb_annual_avg"] = merged["recent_fb_2010plus"] / 12
        merged["recent_fb_annual_share"] = merged["recent_fb_annual_avg"] / merged["totpop"]
    merged.to_parquet(OUT / "county_newcomer_comparison.parquet", index=False)
    print(f"\nWrote {OUT/'county_newcomer_comparison.parquet'}: {len(merged)} counties")

    # Stylized facts
    print("\n=== Stylized fact 1: native-newcomer inflow vs immigrant-newcomer inflow ===")
    sub = merged.dropna(subset=["us_inflow_persons", "totpop"])
    sub = sub[sub["totpop"] >= 10000]  # filter tiny counties
    print(f"Counties (≥10k pop): {len(sub)}")
    print(f"Median US-inflow share / yr:    {sub['us_inflow_share'].median():.4f} ({sub['us_inflow_share'].median()*100:.2f}%)")
    if "recent_fb_annual_share" in sub.columns:
        print(f"Median recent-FB annual share: {sub['recent_fb_annual_share'].median():.4f} ({sub['recent_fb_annual_share'].median()*100:.2f}%)")
        # Ratio
        ratio = sub["us_inflow_share"] / sub["recent_fb_annual_share"].replace(0, np.nan)
        print(f"Median US-inflow / FB-inflow ratio: {ratio.median():.1f}x")

    print("\n=== Stylized fact 2: counties with HIGHEST native inflow ===")
    top_us = sub.nlargest(15, "us_inflow_share")[["NAME", "totpop", "us_inflow_persons", "us_inflow_share", "median_rent"]]
    print(top_us.to_string(index=False))

    if "recent_fb_annual_share" in sub.columns:
        print("\n=== Stylized fact 3: counties with HIGHEST recent-FB inflow share ===")
        top_fb = sub.nlargest(15, "recent_fb_annual_share")[["NAME", "totpop", "recent_fb_annual_avg", "recent_fb_annual_share", "median_rent"]]
        print(top_fb.to_string(index=False))

    # Quintile comparison
    print("\n=== Stylized fact 4: rent and income by inflow type quintile ===")
    sub["us_q"] = pd.qcut(sub["us_inflow_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
    print("\nBy US-NATIVE inflow quintile:")
    print(sub.groupby("us_q", observed=True).agg(
        n=("NAME", "count"),
        median_inflow_share=("us_inflow_share", "median"),
        median_rent=("median_rent", "median"),
        median_hh_income=("median_hh_income", "median"),
        median_fb_share_overall=("fb_share", "median"),
    ).to_string())

    if "recent_fb_annual_share" in sub.columns:
        sub2 = sub.dropna(subset=["recent_fb_annual_share"]).copy()
        sub2["fb_q"] = pd.qcut(sub2["recent_fb_annual_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
        print("\nBy RECENT-FOREIGN-BORN inflow quintile:")
        print(sub2.groupby("fb_q", observed=True).agg(
            n=("NAME", "count"),
            median_inflow_share=("recent_fb_annual_share", "median"),
            median_rent=("median_rent", "median"),
            median_hh_income=("median_hh_income", "median"),
            median_us_inflow_share=("us_inflow_share", "median"),
        ).to_string())


if __name__ == "__main__":
    main()

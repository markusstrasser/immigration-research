"""Build A_assessor/prices.csv from the cached county extracts.

Rules applied identically to every county:
  * single-family-residential parcels only
  * Prop 13 base year (or transfer year) 2022-2024
  * lot area 0.03-5.0 acres, land value >= $10,000
  * base-year value = roll_land_value / 1.02**(roll_year - base_year)
  * base-year $ -> 2024 $ with S&P CoreLogic Case-Shiller metro annual averages
  * median and IQR of land $/acre
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CACHE, case_shiller_factors, iqr_stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "prices.csv"))

CS_LA, CS_SD = "LXXRSA", "SDXRSA"
YEARS = [2022, 2023, 2024]


def finalize(df, value_col, acre_col, year_col, roll_year, cs_id, label):
    cs = case_shiller_factors(cs_id, YEARS)
    df = df.copy()
    df["_acres"] = df[acre_col]
    df["_val"] = df[value_col]
    df["_by"] = df[year_col].astype(int)
    df = df[(df._acres > 0.03) & (df._acres <= 5.0) & (df._val >= 10000)]
    df["_ppa24"] = (df._val / 1.02 ** (roll_year - df._by)
                    * df._by.map(lambda y: cs[2024] / cs[y]) / df._acres)
    st = iqr_stats(df._ppa24)
    print("%s: n=%d median=%.0f p25=%.0f p75=%.0f  (cs %s: %s)"
          % (label, st["n"], st["median"], st["p25"], st["p75"], cs_id,
             {k: round(v, 2) for k, v in cs.items()}))
    return st, df


# ---------------- Los Angeles (06037) ----------------
la = pd.read_csv(os.path.join(CACHE, "la_joined.csv"),
                 dtype={"AIN": str, "UseCode": str, "Roll_LandBaseYear": str})
la = la[la.Shape__Area.notna()].copy()
la["acres"] = la.Shape__Area / 43560.0
la = la[la.UseCode.fillna("").str.startswith("01")]
la_st, la_df = finalize(la, "Roll_LandValue", "acres", "Roll_LandBaseYear", 2024, CS_LA, "LA")

# ---------------- San Diego (06073) ----------------
sd = pd.read_csv(os.path.join(CACHE, "sd_sfr_all.csv"), dtype={"docdate": str})
sd["acres"] = sd.acreage.where(sd.acreage > 0, sd.SHAPE__Area / 43560.0)
sd["by"] = 2000 + sd.docdate.astype(str).str[-2:].astype(int)
sd = sd[sd.by.isin(YEARS)]
sd_st, sd_df = finalize(sd, "asr_land", "acres", "by", 2026, CS_SD, "SD")

# ---------------- San Bernardino (06071) ----------------
sb = pd.read_csv(os.path.join(CACHE, "sb_sfr_base2022_24.csv"), dtype={"BaseYear": str})
sb["lv"] = sb.LandValue.astype(str).str.replace(",", "").astype(float)
# the county class 'SINGLE FAMILY RESIDENTIAL' also contains VACANT LAND, CONDO, MANUF HOME,
# DUPLEX rows; keep only the improved detached single-family descriptions
sb = sb[sb.AssessDescription.isin(["SFR", "PUD", "PUD, DEMINIMUS"])]
sb_st, sb_df = finalize(sb, "lv", "Acreage", "BaseYear", 2026, CS_LA, "SB")

rows = [
    {
        "county_fips": "06037", "county": "Los Angeles",
        "price_per_acre_2024": round(la_st["median"]),
        "low_per_acre_2024": round(la_st["p25"]),
        "high_per_acre_2024": round(la_st["p75"]),
        "n_obs": la_st["n"], "year_measured": 2024,
        "land_type": "single-family residential land",
        "method": "assessor land value on 2022-2024 Prop 13 base-year SFR parcels / lot acres; roll-year 2024, 2%/yr cap removed, Case-Shiller LA to 2024$",
        "source": "LA County Assessor roll (Parcel Data 2021-2025 table svc) + LA County Residential Parcels (DPH GIS) for Shape__Area",
        "source_locator": "services.arcgis.com/RmCCgQtiZLDCtblq/.../Parcel_Data_2021_Table/FeatureServer/0 where RollYear='2024' AND UseType='SFR'; area: .../ResidentialParcels_LACounty_010924.../FeatureServer/1 Shape__Area (ft2)",
        "notes": "99.5% of roll AINs matched to parcel area; IQR is 25th-75th pct of parcel $/acre; base-year medians agree within 3%",
    },
    {
        "county_fips": "06073", "county": "San Diego",
        "price_per_acre_2024": round(sd_st["median"]),
        "low_per_acre_2024": round(sd_st["p25"]),
        "high_per_acre_2024": round(sd_st["p75"]),
        "n_obs": sd_st["n"], "year_measured": 2024,
        "land_type": "single-family residential land",
        "method": "assessor land value (asr_land) on SFR parcels whose last recorded document is dated 2022-2024 / lot acres; roll-year 2026, 2%/yr cap removed, Case-Shiller San Diego to 2024$",
        "source": "SANDAG/SanGIS Parcels hosted feature service (assessor ARCC attributes)",
        "source_locator": "geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0 where asr_landuse=11 AND docdate LIKE '%22'/'%23'/'%24'; acreage field (fallback SHAPE__Area/43560)",
        "notes": "docdate = MMDDYY of last recorded document (proxy for transfer/base year); 106,217 transfers 2022-2024 before trimming; lot<=1ac variant median $2.05M",
    },
    {
        "county_fips": "06071", "county": "San Bernardino",
        "price_per_acre_2024": round(sb_st["median"]),
        "low_per_acre_2024": round(sb_st["p25"]),
        "high_per_acre_2024": round(sb_st["p75"]),
        "n_obs": sb_st["n"], "year_measured": 2024,
        "land_type": "single-family residential land",
        "method": "assessor LandValue on AssessClass='SINGLE FAMILY RESIDENTIAL' parcels with BaseYear 2022-2024 / Acreage; roll-year 2026, 2%/yr cap removed, Case-Shiller LA (proxy) to 2024$",
        "source": "County of San Bernardino 'Parcels with Redacted Owner Name' feature service (SBCountyDPW)",
        "source_locator": "services.arcgis.com/aA3snZwJfFkVyDuP/.../Parcels_for_San_Bernardino_County/FeatureServer/0 fields LandValue, Acreage, BaseYear, AssessClass",
        "notes": "kept AssessDescription SFR/PUD/PUD DEMINIMUS; the county's SINGLE FAMILY RESIDENTIAL class also holds VACANT LAND, CONDO, MANUF HOME and DUPLEX rows (class-wide median $541k, n=74,838); roll contains BaseYear=2026 parcels so roll year=2026",
    },
]

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False, lineterminator="\n")
print(df[["county_fips", "county", "price_per_acre_2024", "n_obs"]].to_string(index=False))

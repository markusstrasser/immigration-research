"""LA County (06037): median land value per acre, SFR parcels with 2022-2024 base year.

Inputs (cached by la_fetch.py):
  _cache/la_joined.csv   roll 2024 + parcel area, joined on AIN
Adjustment:
  Prop 13 cap: roll_2024 = base_value * 1.02^(2024-base_year)  -> divide back out.
  Base year -> 2024 dollars: S&P CoreLogic Case-Shiller Los Angeles metro (FRED LXXRSA),
  annual averages.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CACHE, case_shiller_factors, iqr_stats  # noqa: E402

df = pd.read_csv(os.path.join(CACHE, "la_joined.csv"),
                 dtype={"AIN": str, "UseCode": str, "Roll_LandBaseYear": str})
n_raw = len(df)
df = df[df.Shape__Area.notna()].copy()
df["acres"] = df.Shape__Area / 43560.0
df["ppa_raw"] = df.Roll_LandValue / df.acres

# --- filters: SFR use codes only, plausible urban residential lot sizes ---
f = (
    df.UseCode.fillna("").str.startswith("01")
    & df.acres.between(0.03, 5.0)
    & (df.Roll_LandValue >= 10000)
)
df = df[f].copy()
print("rows: raw %d -> filtered %d" % (n_raw, len(df)))

# --- year adjustment ---
years = [2022, 2023, 2024]
cs = case_shiller_factors("LXXRSA", years)
print("Case-Shiller LXXRSA annual averages:", {k: round(v, 2) for k, v in cs.items()})
df["base_year"] = df.Roll_LandBaseYear.astype(int)
df["cap_factor"] = 1.02 ** (2024 - df.base_year)
df["cs_factor"] = df.base_year.map(lambda y: cs[2024] / cs[y])
df["land_2024"] = df.Roll_LandValue / df.cap_factor * df.cs_factor
df["ppa_2024"] = df.land_2024 / df.acres

st = iqr_stats(df.ppa_2024)
st_raw = iqr_stats(df.ppa_raw)
print("unadjusted median $/acre: %.0f" % st_raw["median"])
print(json.dumps(st, indent=2))
print(df.groupby("base_year").ppa_2024.agg(["size", "median"]))

# sensitivity: no year adjustment, and no trim
print("no-adjust IQR:", {k: round(v) for k, v in iqr_stats(df.ppa_raw).items()})
print("no-trim (acres>0, lv>0) median:",
      round(df.ppa_raw.replace([np.inf, -np.inf], np.nan).median()))

out = {
    "county_fips": "06037", "county": "Los Angeles",
    "n": st["n"], "median": st["median"], "p25": st["p25"], "p75": st["p75"],
    "cs": cs,
}
with open(os.path.join(CACHE, "la_stats.json"), "w") as fh:
    json.dump(out, fh, indent=2)

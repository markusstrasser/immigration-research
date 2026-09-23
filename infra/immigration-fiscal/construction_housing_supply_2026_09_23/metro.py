"""The group's share of construction work by metro, on the housing lane's geography.

PUMA cells from tabulate.py are allocated to 2013 CBSAs exactly as the housing lane allocates
its rent cells: Geocorr 2022 PUMA->county population factors, then the 2013 OMB county->CBSA
delineation; counties outside a metro form one non-metro remainder per state. The allocation
preserves every national total.

Output: derived/construction_metro.csv, one row per area: construction-trades and
construction-industry employment and earnings, total and by group, and the union's shares.
Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/metro.py
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DERIVED = HERE / "derived"
XWALK = ROOT / "infra/immigration-fiscal/employment_entry_2026_09_18/_cache/xwalk_puma22.csv"
COUNTY_CBSA = ROOT / "infra/immigration-fiscal/hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv"
UNION = ["mx_born", "us_born_mx_origin", "fb_mx_origin"]
VALUES = ["trades_employed", "trades_earnings", "industry_employed", "industry_earnings",
          "all_employed", "all_earnings"]


def allocation():
    if not XWALK.exists():
        raise SystemExit(f"[BLOCKED] missing {XWALK}; run employment_entry_2026_09_18/fetch_crosswalks.py")
    xw = pd.read_csv(XWALK, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(COUNTY_CBSA, dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa", "cbsa_title"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    titles = xw.dropna(subset=["cbsa"]).drop_duplicates("cbsa").set_index("cbsa")["cbsa_title"]
    return alloc, titles


def main():
    cells = pd.read_csv(DERIVED / "construction_puma.csv", dtype={"STATE": str, "PUMA": str})
    cells["union"] = cells["group"].isin(UNION)
    wide = cells.groupby(["STATE", "PUMA", "union"])[VALUES].sum().unstack("union", fill_value=0)
    wide.columns = [f"{v}_{'union' if u else 'other'}" for v, u in wide.columns]
    wide = wide.reset_index()
    alloc, titles = allocation()
    merged = wide.merge(alloc, left_on=["STATE", "PUMA"], right_on=["state", "puma"], how="left",
                        validate="one_to_many")
    if merged["area"].isna().any():
        raise ValueError("PUMAs without crosswalk rows")
    cols = [c for c in wide.columns if c not in ("STATE", "PUMA")]
    for c in cols:
        merged[c] = merged[c] * merged["afact"]
    areas = merged.groupby("area")[cols].sum()
    for c in cols:
        if not np.isclose(areas[c].sum(), wide[c].sum(), rtol=1e-9):
            raise ValueError(f"allocation lost {c}")
    out = pd.DataFrame(index=areas.index)
    for v in VALUES:
        out[f"{v}_total"] = areas[f"{v}_union"] + areas[f"{v}_other"]
        out[f"{v}_union"] = areas[f"{v}_union"]
        out[f"{v}_union_share"] = np.divide(out[f"{v}_union"], out[f"{v}_total"],
                                            out=np.zeros(len(out)), where=out[f"{v}_total"] > 0)
    out["title"] = out.index.map(titles)
    out = out.reset_index().rename(columns={"index": "area"})
    out.to_csv(DERIVED / "construction_metro.csv", index=False)
    top = out[out["area"].str.match(r"^\d")].nlargest(25, "trades_employed_total")
    pd.set_option("display.width", 200)
    print(top[["area", "title", "trades_employed_total", "trades_employed_union_share",
               "trades_earnings_union_share", "industry_employed_union_share",
               "all_employed_union_share"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()

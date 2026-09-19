#!/usr/bin/env python3
"""Build the three geography tables the analysis needs, all on 2010 tract definitions.

  derived/geo_county_cbsa_2013.csv   county FIPS -> 2013 OMB CBSA
  derived/geo_tract2010.csv          2010 tract -> interior point, land area
  derived/geo_tract20_to_tract10.csv 2020 tract -> dominant 2010 parent

Deterministic: every output is sorted and written with fixed float formatting.
"""
import pathlib
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE, DERIVED = LANE / "_cache", LANE / "derived"
DERIVED.mkdir(exist_ok=True)


def county_cbsa():
    d = pd.read_excel(CACHE / "cbsa_list1_2013.xls", header=2, dtype=str)
    d = d.dropna(subset=["CBSA Code", "FIPS State Code", "FIPS County Code"])
    d = d[d["CBSA Code"].str.fullmatch(r"\d{5}")]
    out = pd.DataFrame({
        "county_fips": d["FIPS State Code"].str.zfill(2) + d["FIPS County Code"].str.zfill(3),
        "cbsa": d["CBSA Code"],
        "cbsa_title": d["CBSA Title"].str.strip(),
        "is_metro": (d["Metropolitan/Micropolitan Statistical Area"]
                     .str.startswith("Metropolitan")).astype(int),
    }).drop_duplicates("county_fips").sort_values("county_fips")
    out.to_csv(DERIVED / "geo_county_cbsa_2013.csv", index=False)
    print(f"[geo] counties={len(out)} cbsas={out.cbsa.nunique()} "
          f"metro={out.is_metro.sum()}", flush=True)
    return out


def tract_points():
    d = pd.read_csv(CACHE / "gaz" / "2019_Gaz_tracts_national.txt", sep="\t",
                    dtype={"GEOID": str})
    d.columns = [c.strip() for c in d.columns]
    out = pd.DataFrame({
        "tract10": d["GEOID"].str.zfill(11),
        "lat": d["INTPTLAT"].astype(float).round(6),
        "lon": d["INTPTLONG"].astype(float).round(6),
        "aland_sqmi": d["ALAND_SQMI"].astype(float).round(4),
    }).sort_values("tract10")
    out.to_csv(DERIVED / "geo_tract2010.csv", index=False)
    print(f"[geo] tracts2010={len(out)}", flush=True)
    return out


def tract20_to_10():
    d = pd.read_csv(CACHE / "tab20_tract20_tract10.txt", sep="|",
                    dtype={"GEOID_TRACT_20": str, "GEOID_TRACT_10": str},
                    encoding="utf-8-sig")
    d = d[["GEOID_TRACT_20", "GEOID_TRACT_10", "AREALAND_PART", "AREALAND_TRACT_20"]].copy()
    d["GEOID_TRACT_20"] = d["GEOID_TRACT_20"].str.zfill(11)
    d["GEOID_TRACT_10"] = d["GEOID_TRACT_10"].str.zfill(11)
    d["AREALAND_PART"] = pd.to_numeric(d["AREALAND_PART"], errors="coerce").fillna(0)
    d["AREALAND_TRACT_20"] = pd.to_numeric(d["AREALAND_TRACT_20"], errors="coerce").fillna(0)
    # Dominant parent = the 2010 tract holding most of the 2020 tract's land.
    # Ties broken by GEOID so the choice is reproducible.
    d = d.sort_values(["GEOID_TRACT_20", "AREALAND_PART", "GEOID_TRACT_10"],
                      ascending=[True, False, True])
    top = d.groupby("GEOID_TRACT_20", as_index=False).first()
    top["area_share"] = (top["AREALAND_PART"] /
                         top["AREALAND_TRACT_20"].where(top["AREALAND_TRACT_20"] > 0)).round(4)
    out = top[["GEOID_TRACT_20", "GEOID_TRACT_10", "area_share"]].rename(
        columns={"GEOID_TRACT_20": "tract20", "GEOID_TRACT_10": "tract10"}
    ).sort_values("tract20")
    out.to_csv(DERIVED / "geo_tract20_to_tract10.csv", index=False)
    clean = (out["area_share"] >= 0.99).mean()
    print(f"[geo] tracts2020={len(out)} parents={out.tract10.nunique()} "
          f"share_with_>=99pct_in_one_parent={clean:.3f}", flush=True)
    return out


if __name__ == "__main__":
    county_cbsa()
    tract_points()
    tract20_to_10()
    print("[geo] done", flush=True)

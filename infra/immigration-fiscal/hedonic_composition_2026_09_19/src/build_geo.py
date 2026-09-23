#!/usr/bin/env python3
"""Build the three geography tables the analysis needs, all on 2010 tract definitions.

  derived/geo_county_cbsa_2013.csv   county FIPS -> 2013 OMB CBSA (plus CT's 2022 planning regions)
  derived/geo_tract2010.csv          2010 tract -> interior point, land area
  derived/geo_tract20_to_tract10.csv 2020 tract -> dominant 2010 parent

Deterministic: every output is sorted and written with fixed float formatting.
"""
import json
import pathlib
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE, DERIVED = LANE / "_cache", LANE / "derived"
DERIVED.mkdir(exist_ok=True)

# Connecticut's nine planning regions (09110-09190) replaced its eight counties as county
# equivalents in 2022, so 2022 PUMA crosswalks (Geocorr 2022) key the state on them; the 2013
# delineation has only the old counties. Regions and old counties are both unions of whole towns.
#   town -> old county and planning region, Census Bureau:
#     https://www2.census.gov/geo/docs/reference/ct_change/ct_cou_to_cousub_crosswalk.txt
#   2020 Census population by town (P1_001N, old-county geography), fetched with a key:
#     https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=county%20subdivision:*&in=state:09%20county:*
CT_TOWNS = CACHE / "ct_cou_to_cousub_crosswalk.txt"
CT_TOWN_POP = CACHE / "ct_cousub_pop2020_pl.json"


def ct_planning_regions(counties):
    """Each planning region takes the 2013 CBSA row holding the majority of its 2020 population."""
    for path in (CT_TOWNS, CT_TOWN_POP):
        if not path.exists():
            raise SystemExit(f"[BLOCKED] missing {path}; fetch it from the URL in build_geo.py")
    xw = pd.read_csv(CT_TOWNS, sep="|", dtype=str, encoding="utf-8-sig")
    xw.columns = [c.split("\n")[0] for c in xw.columns]  # headers carry "\n(INCITS ...)"
    rows = json.load(open(CT_TOWN_POP))
    pop = pd.DataFrame(rows[1:], columns=rows[0])
    # Drop the legend lines and the "County subdivisions not defined" water rows (population 0).
    water = pop["county subdivision"] == "00000"
    if (pop.loc[water, "P1_001N"] != "0").any():
        raise SystemExit("[BLOCKED] populated CT water row")
    xw = xw[(xw["STATEFP"] == "09") & (xw["COUSUBFP"] != "00000")]
    towns = xw.merge(pop[~water], left_on=["OLD_COUNTYFP", "COUSUBFP"],
                     right_on=["county", "county subdivision"], how="inner", validate="one_to_one")
    if not len(towns) == len(xw) == (~water).sum() == 169:
        raise SystemExit(f"[BLOCKED] CT towns matched {len(towns)} of {len(xw)} / {(~water).sum()}")
    towns["pop"] = towns["P1_001N"].astype(int)
    towns["county_fips"] = "09" + towns["OLD_COUNTYFP"]
    towns = towns.merge(counties, on="county_fips", how="left", validate="many_to_one")
    if towns["cbsa"].isna().any():
        raise SystemExit("[BLOCKED] CT town outside the 2013 CBSA list")
    towns["region"] = "09" + towns["NEW_COUNTYFP"]
    by = towns.groupby(["region", "cbsa", "cbsa_title", "is_metro"], as_index=False)["pop"].sum()
    by["share"] = by["pop"] / by.groupby("region")["pop"].transform("sum")
    top = by.sort_values(["region", "share"], ascending=[True, False]).groupby("region").head(1)
    if len(top) != 9 or (top["share"] <= 0.5).any():
        raise SystemExit(f"[BLOCKED] CT planning region without a majority CBSA:\n{top}")
    for r in top.itertuples():
        print(f"[geo] CT {r.region} -> {r.cbsa} {r.cbsa_title} (metro={r.is_metro}), "
              f"population outside {1 - r.share:.4f}", flush=True)
    return (top.rename(columns={"region": "county_fips"})
            [["county_fips", "cbsa", "cbsa_title", "is_metro"]])


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
    }).drop_duplicates("county_fips")
    out = pd.concat([out, ct_planning_regions(out)]).sort_values("county_fips")
    if out["county_fips"].duplicated().any():
        raise SystemExit("[BLOCKED] CT planning region code already in the 2013 list")
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

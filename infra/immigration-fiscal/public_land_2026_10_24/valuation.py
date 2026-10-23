"""Reuse the school lane's FHFA price engine; locate sites on its 2010 tract vintage.

Native-First: DuckDB spatial joins and the existing school-price functions. This module
does not copy the source's discount constants or rewrite its cached inputs.
"""
import importlib.util
import math
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SCHOOL = HERE.parent / "school_land_2026_10_24"
ACRE = 4046.8564224


def school_prices():
    """The source module only defines functions on import; its main build is guarded."""
    spec = importlib.util.spec_from_file_location("public_land_school_prices", SCHOOL / "build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.prices()


def connection():
    c = duckdb.connect()
    c.execute("LOAD spatial; SET geometry_always_xy = true; SET threads=4; SET memory_limit='1500MB'")
    temp = HERE / "_cache" / "spatial_temp"
    temp.mkdir(parents=True, exist_ok=True)
    c.execute("SET temp_directory = ?", [str(temp)])
    return c


def load_tracts(c):
    files = sorted((SCHOOL / "_cache" / "tracts2010").glob("gz_2010_*_140_00_500k.zip"))
    if len(files) != 51:
        raise ValueError(f"[BLOCKED] need all 51 school-lane 2010 tract boundary files, found {len(files)}")
    queries = [f"SELECT substr(GEO_ID,10) AS tract, geom AS g FROM ST_Read('/vsizip/{p}/{p.stem}.shp')" for p in files]
    c.execute("CREATE TABLE tracts AS " + " UNION ALL ".join(queries))
    c.execute("CREATE INDEX tracts_rtree ON tracts USING RTREE(g)")


def locate_points(c, records):
    """Use containing tract; an authoritative county hint is the only geographic fallback.

    A shore or border miss has no silently invented nearest county. It remains unpriced
    without the source's county field. A synthetic tract suffix requests the source
    price engine's explicit county/state fallback; it is never reported as a tract price.
    """
    if records.empty:
        return records.assign(tract=pd.Series(dtype=str), geo_level=pd.Series(dtype=str))
    if records.record_id.duplicated().any():
        raise ValueError("[BLOCKED] duplicate valuation record IDs")
    p = records[["record_id", "lon", "lat"]].copy()
    c.register("site_points_input", p)
    found = c.execute("""SELECT p.record_id, min(t.tract) AS tract
        FROM site_points_input p JOIN tracts t ON ST_Intersects(t.g, ST_Point(p.lon,p.lat))
        GROUP BY p.record_id ORDER BY p.record_id""").df()
    out = records.merge(found, on="record_id", how="left", validate="one_to_one")
    out["geo_level"] = np.where(out.tract.notna(), "tract", "unlocated")
    if "county_fips" in out:
        good_county = out.county_fips.fillna("").astype(str).str.fullmatch(r"[0-9]{5}")
        fallback = out.tract.isna() & good_county
        out.loc[fallback, "tract"] = out.loc[fallback, "county_fips"] + "999999"
        out.loc[fallback, "geo_level"] = "source_county"
    out["county"] = out.tract.fillna("").str[:5]
    return out


def price_sites(records, engine, price_tables):
    """Price independently sized sites. Missing price/geography is retained and counted.

    `site_acres` is the entire source parcel/campus, while `acres` may be its geographic
    slice. This prevents plattage changing merely because a county/tract boundary cuts
    the site. Arm C is the source's out-of-domain reference, never a statistical bound.
    """
    out = records.copy()
    good = out.tract.notna() & out.acres.gt(0) & out.site_acres.gt(0)
    if not good.any():
        # The source's price_rows requires at least one tract. Missing geography
        # is a reportable observation, including when an entire class is absent.
        for col in ["p24", "q24", "lot_sqft", "p15", "g_land", "g_hpi", "bL", "value_A", "value_B", "value_C"]:
            out[col] = np.nan
        out["price_level"] = None
        out["priced"] = False
        return out
    pr = engine.price_rows(out.loc[good, "tract"], price_tables)
    out = out.merge(pr, on="tract", how="left", validate="many_to_one")
    good = good.to_numpy() & np.isfinite(out.p24) & out.p24.gt(0).to_numpy()
    for arm in "ABC":
        out["value_" + arm] = np.nan
    if good.any():
        arms = engine.value_arms(out.loc[good, "site_acres"], out.loc[good])
        fraction = (out.loc[good, "acres"] / out.loc[good, "site_acres"]).to_numpy()
        for arm, value in zip("ABC", arms[:3]):
            out.loc[good, "value_" + arm] = value * fraction
    out["priced"] = good
    # The cubic was estimated on vacant metropolitan lots. If it turns up at very
    # large acreage, expose that extrapolation instead of silently accepting C>A.
    invalid_c = good & (out.value_C.gt(out.value_A * (1 + 1e-12)) | ~np.isfinite(out.value_C))
    if invalid_c.any():
        ids = out.loc[invalid_c, "record_id"].head(5).tolist()
        raise ValueError(f"[BLOCKED] vacant-lot cubic exceeds residential reference: {ids}")
    return out


def county_price_sites(records):
    out = records.copy()
    out["tract"] = out.county_fips.astype(str).str.zfill(5) + "999999"
    out["county"] = out.county_fips.astype(str).str.zfill(5)
    out["geo_level"] = "source_county"
    return out


def json_finite(value):
    """Reject nonfinite JSON numbers; a missing estimate is a real null."""
    if isinstance(value, dict):
        return {str(k): json_finite(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_finite(v) for v in value]
    if isinstance(value, np.generic):
        return json_finite(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("[BLOCKED] nonfinite output; declare missing values explicitly")
    return value

"""Urban/rural status of every land record, from the Census 2020 urban areas.

- Roads: HPMS urban_id already separates urban (inside an FHWA-adjusted urban area) from rural
  (99999); `public_land_2026_10_24/roads.py` carries it as `area_type`. No geometry is needed.
- Parks: the urban fraction of each PAD-US fee polygon = area inside a 2020 urban area / polygon
  area (planar lon/lat areas; the ratio is insensitive to the projection at park scale). A polygon
  wholly inside an urban area is 1 without an intersection. Each overlap-corrected tract piece of a
  park takes its park's fraction.
- Point sites (airports, plants, facilities): reference point (airports) or the site polygon's
  point on surface, inside a 2020 urban area or not.
- Sites known only by tract (schools): the 2010 tract's internal point.

The result is cached under `_cache/` keyed by the sha256 of every input, and rebuilt on any change.
"""
import hashlib
import json
import zipfile
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PUBLIC = FISCAL / "public_land_2026_10_24"
SCHOOL = FISCAL / "school_land_2026_10_24"
UAC = HERE / "_cache" / "geo" / "tl_2020_us_uac20.zip"
PARKS = PUBLIC / "_cache" / "footprints" / "padus_parks.parquet"
FACILITIES = PUBLIC / "_cache" / "footprints" / "facility_records.parquet"
UNIVERSE = PUBLIC / "derived" / "universe_records.csv"
GAZ_TRACTS = SCHOOL / "_cache" / "gaz" / "Gaz_tracts_national_2010.zip"
OUT = HERE / "_cache" / "urban_status.parquet"
MANIFEST = HERE / "_cache" / "urban_status_manifest.json"


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def inputs():
    return {str(p.relative_to(FISCAL)): sha256(p) for p in [Path(__file__), UAC, PARKS, FACILITIES, UNIVERSE, GAZ_TRACTS]}


def connection():
    c = duckdb.connect()
    c.execute("LOAD spatial; SET geometry_always_xy=true; SET threads=8; SET memory_limit='3GB'; SET enable_progress_bar=false")
    c.execute(f"CREATE TABLE ua AS SELECT UACE20 AS uace, geom AS g FROM ST_Read('/vsizip/{UAC}/tl_2020_us_uac20.shp')")
    c.execute("CREATE INDEX ua_rtree ON ua USING RTREE(g)")
    return c


def park_fractions(c):
    c.execute(f"CREATE TABLE parks AS SELECT id, ST_MakeValid(ST_GeomFromWKB(wkb)) AS g FROM read_parquet('{PARKS}')")
    c.execute("CREATE TABLE hits AS SELECT p.id, u.uace, ST_Within(p.g, u.g) AS inside FROM parks p JOIN ua u ON ST_Intersects(p.g, u.g)")
    # A polygon wholly inside one urban area is fully urban; otherwise sum its intersections.
    # Urban areas do not overlap, so the intersections add without double counting.
    return c.execute("""
        WITH full_in AS (SELECT DISTINCT id FROM hits WHERE inside),
        partial AS (SELECT h.id, sum(ST_Area(ST_Intersection(p.g, u.g))) AS a
            FROM hits h JOIN parks p USING(id) JOIN ua u USING(uace)
            WHERE h.id NOT IN (SELECT id FROM full_in) GROUP BY h.id)
        SELECT p.id, CASE WHEN f.id IS NOT NULL THEN 1.0
                          WHEN q.a IS NULL THEN 0.0
                          ELSE least(1.0, q.a / nullif(ST_Area(p.g), 0)) END AS urban_fraction
        FROM parks p LEFT JOIN full_in f USING(id) LEFT JOIN partial q USING(id) ORDER BY p.id""").df()


def points_in_ua(c, pts, name):
    """pts: record_id, lon, lat. Returns record_id, urban (bool); a missing point is NaN."""
    c.register(name + "_in", pts[["record_id", "lon", "lat"]])
    hit = c.execute(f"""SELECT DISTINCT p.record_id FROM {name}_in p JOIN ua u
        ON ST_Intersects(u.g, ST_Point(p.lon, p.lat)) WHERE p.lon IS NOT NULL""").df()
    out = pts[["record_id"]].copy()
    out["urban_fraction"] = out.record_id.isin(set(hit.record_id)).astype(float)
    out.loc[pts.lon.isna().to_numpy(), "urban_fraction"] = float("nan")
    return out


def build():
    want = inputs()
    if OUT.exists() and MANIFEST.exists():
        m = json.loads(MANIFEST.read_text())
        if m.get("inputs") == want and m.get("output_sha256") == sha256(OUT):
            print("  ✓ urban status: hash-validated cache hit", flush=True)
            return pd.read_parquet(OUT)
    c = connection()
    parks = park_fractions(c).assign(kind="park")
    u = pd.read_csv(UNIVERSE, dtype=str, keep_default_na=False)
    air = u[u["class"].eq("airport")][["record_id", "lon", "lat"]].copy()
    air[["lon", "lat"]] = air[["lon", "lat"]].apply(pd.to_numeric, errors="coerce")
    airports = points_in_ua(c, air, "air").assign(kind="airport")
    fac = c.execute(f"""SELECT id AS record_id, ST_X(ST_PointOnSurface(ST_MakeValid(ST_GeomFromWKB(wkb)))) AS lon,
        ST_Y(ST_PointOnSurface(ST_MakeValid(ST_GeomFromWKB(wkb)))) AS lat FROM read_parquet('{FACILITIES}') ORDER BY id""").df()
    facilities = points_in_ua(c, fac, "fac").assign(kind="facility")
    with zipfile.ZipFile(GAZ_TRACTS) as z:
        g = pd.read_csv(z.open("Gaz_tracts_national.txt"), sep="\t", dtype={"GEOID": str})
    g.columns = [x.strip() for x in g.columns]
    tr = g.rename(columns={"GEOID": "record_id", "INTPTLONG": "lon", "INTPTLAT": "lat"})[["record_id", "lon", "lat"]]
    tracts = points_in_ua(c, tr, "tract").assign(kind="tract2010")
    out = pd.concat([parks.rename(columns={"id": "record_id"}), airports, facilities, tracts], ignore_index=True)
    out = out.sort_values(["kind", "record_id"]).reset_index(drop=True)
    out.to_parquet(OUT, index=False)
    MANIFEST.write_text(json.dumps(dict(inputs=want, output_sha256=sha256(OUT)), indent=2, sort_keys=True) + "\n")
    print(f"  ✓ urban status: {len(out):,} records", flush=True)
    return out


if __name__ == "__main__":
    print(build().groupby("kind").urban_fraction.describe())

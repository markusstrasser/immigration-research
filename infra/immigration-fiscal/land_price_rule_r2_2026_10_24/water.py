"""Water inside park polygons: the share of each park tract piece that is TIGER area water.

PAD-US fee polygons include bays, lakes and reservoirs (Mission Bay Park's record holds 3,876 acres in a
tract with 2,085 land acres). Each park piece is the PAD-US polygon intersected with its 2010 cartographic
tract (public_land's split); its water share is area(piece ∩ TIGER 2020 AREAWATER) / area(piece), planar
in lon/lat (a ratio, insensitive to projection at park scale). Only counties with a park piece in a 2010
tract whose Gazetteer water share exceeds WATER_MIN are fetched; the rest keep share 0, an error bounded
by WATER_MIN of their value (reported in summary.json).

Raw zips stay in the ignored `_cache/areawater/`; the result is cached in `_cache/park_water.parquet`
keyed by the sha256 of every input.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
import zipfile
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PUBLIC = FISCAL / "public_land_2026_10_24"
SCHOOL = FISCAL / "school_land_2026_10_24"
PARKS = PUBLIC / "_cache" / "footprints" / "padus_parks.parquet"
TRACTS = SCHOOL / "_cache" / "tracts2010"
GAZ = SCHOOL / "_cache" / "gaz" / "Gaz_tracts_national_2010.zip"
WATER_DIR = HERE / "_cache" / "areawater"
OUT = HERE / "_cache" / "park_water.parquet"
MANIFEST = HERE / "_cache" / "park_water_manifest.json"
URL = "https://www2.census.gov/geo/tiger/TIGER2020/AREAWATER/tl_2020_{c}_areawater.zip"
# Census's firewall rejects a few 2020 files on every request (HTML "Request Rejected", status 200); those
# counties take the 2021 vintage, listed in the manifest as `vintage_2021`.
URL_2021 = "https://www2.census.gov/geo/tiger/TIGER2021/AREAWATER/tl_2021_{c}_areawater.zip"
WATER_MIN = 0.02
SQM_PER_ACRE = 4046.8564224


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def gazetteer():
    with zipfile.ZipFile(GAZ) as z:
        g = pd.read_csv(z.open("Gaz_tracts_national.txt"), sep="\t", dtype={"GEOID": str})
    g.columns = [c.strip() for c in g.columns]
    g["aland_acres"] = g.ALAND / SQM_PER_ACRE
    g["awater_acres"] = g.AWATER / SQM_PER_ACRE
    g["water_share"] = g.awater_acres / (g.aland_acres + g.awater_acres)
    return g.set_index("GEOID")[["aland_acres", "awater_acres", "water_share"]]


def targets(park_ids):
    """park_ids: Series of park record_ids 'park:padus:<id>:<tract>'. Returns pieces in watery tracts."""
    g = gazetteer()
    p = pd.DataFrame({"record_id": park_ids.to_numpy()})
    parts = p.record_id.str.split(":")
    p["padus_id"] = parts.str[1] + ":" + parts.str[2]
    p["tract"] = parts.str[3]
    p["water_share_tract"] = p.tract.map(g.water_share).fillna(0.0)
    return p[p.water_share_tract.gt(WATER_MIN)].reset_index(drop=True)


def fetch(counties):
    """Download each county's AREAWATER zip once; a file that is not a zip is deleted and refetched."""
    WATER_DIR.mkdir(parents=True, exist_ok=True)

    def missing():
        # Census's firewall can answer a burst with an HTML "Request Rejected" page and status 200.
        for c in counties:
            z = WATER_DIR / f"tl_2020_{c}_areawater.zip"
            if z.exists() and not zipfile.is_zipfile(z):
                z.unlink()
        return [c for c in counties if water_zip(c) is None]

    if todo := missing():
        print(f"  ▸ fetching {len(todo)} TIGER 2020 AREAWATER county files", flush=True)
        lst = WATER_DIR / "fetch_list.txt"
        lst.write_text("".join(f"{URL.format(c=c)}\n" for c in todo))
        # curl writes each file under its remote name; a failed fetch leaves no file and is caught below.
        subprocess.run(f"cd '{WATER_DIR}' && xargs -P 8 -n 1 curl -sSfLO --retry 3 --max-time 300 < fetch_list.txt",
                       shell=True, check=False)
        lst.unlink()
    for attempt in range(2):
        if not (todo := missing()):
            break
        print(f"  ! refetching {len(todo)} AREAWATER files serially (attempt {attempt + 1})", flush=True)
        for c in todo:
            subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "300", "-o",
                            str(WATER_DIR / f"tl_2020_{c}_areawater.zip"), URL.format(c=c)], check=False)
            time.sleep(5)
    for c in missing():
        z = WATER_DIR / f"tl_2021_{c}_areawater.zip"
        if not (z.exists() and zipfile.is_zipfile(z)):
            print(f"  ! [DEGRADED] {c}: 2020 file rejected by Census; using TIGER 2021", flush=True)
            subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "300", "-o", str(z), URL_2021.format(c=c)], check=False)
    still = [c for c in counties if water_zip(c) is None]
    if still:
        raise RuntimeError(f"[BLOCKED] {len(still)} AREAWATER files missing or not zips, e.g. {still[:5]}")


def water_zip(c):
    """The county's AREAWATER zip: the 2020 file, else the 2021 file, else None."""
    for y in (2020, 2021):
        z = WATER_DIR / f"tl_{y}_{c}_areawater.zip"
        if z.exists() and zipfile.is_zipfile(z):
            return z
    return None


def build(park_ids):
    t = targets(park_ids)
    counties = sorted(set(t.tract.str[:5]))
    fetch(counties)
    states = sorted(set(c[:2] for c in counties))
    inputs = {"water.py": sha256(Path(__file__)), "padus_parks": sha256(PARKS), "gazetteer": sha256(GAZ),
              "targets": hashlib.sha256("\n".join(t.record_id).encode()).hexdigest(),
              "tracts": {s: sha256(TRACTS / f"gz_2010_{s}_140_00_500k.zip") for s in states},
              "areawater": {c: sha256(water_zip(c)) for c in counties},
              "vintage_2021": sorted(c for c in counties if water_zip(c).name.startswith("tl_2021"))}
    if OUT.exists() and MANIFEST.exists():
        m = json.loads(MANIFEST.read_text())
        if m.get("inputs") == inputs and m.get("output_sha256") == sha256(OUT):
            print("  ✓ park water: hash-validated cache hit", flush=True)
            return pd.read_parquet(OUT)
    c = duckdb.connect()
    c.execute("LOAD spatial; SET geometry_always_xy=true; SET threads=4; SET memory_limit='1500MB'; SET enable_progress_bar=false")
    c.register("tg", t[["record_id", "padus_id", "tract"]])
    c.execute(f"""CREATE TABLE pk AS SELECT p.id AS padus_id, ST_MakeValid(ST_GeomFromWKB(p.wkb)) AS g
                  FROM read_parquet('{PARKS}') p WHERE p.id IN (SELECT DISTINCT padus_id FROM tg)""")
    q = " UNION ALL ".join(f"SELECT substr(GEO_ID,10) AS tract, ST_MakeValid(geom) AS g FROM ST_Read('/vsizip/{TRACTS}/gz_2010_{s}_140_00_500k.zip/gz_2010_{s}_140_00_500k.shp')"
                           for s in states)
    c.execute(f"CREATE TABLE tr AS SELECT * FROM ({q}) WHERE tract IN (SELECT DISTINCT tract FROM tg)")
    c.execute("""CREATE TABLE pieces AS SELECT tg.record_id, tg.tract, substr(tg.tract,1,5) AS county,
                 ST_Intersection(pk.g, tr.g) AS g FROM tg JOIN pk USING(padus_id) JOIN tr USING(tract)""")
    rows = []
    for i, cty in enumerate(counties, 1):
        z = water_zip(cty)
        c.execute(f"""CREATE OR REPLACE TABLE w AS SELECT ST_Union_Agg(ST_MakeValid(geom)) AS g
                      FROM ST_Read('/vsizip/{z}/{z.stem}.shp')""")
        r = c.execute(f"""SELECT p.record_id, ST_Area(p.g) AS a,
                          CASE WHEN w.g IS NULL THEN 0 ELSE ST_Area(ST_Intersection(p.g, w.g)) END AS aw
                          FROM pieces p, w WHERE p.county = '{cty}'""").df()
        rows.append(r)
        if i % 200 == 0:
            print(f"  [{i}/{len(counties)}] water intersections", flush=True)
    out = pd.concat(rows, ignore_index=True)
    out["water_frac"] = (out.aw / out.a.where(out.a > 0)).fillna(0.0).clip(0.0, 1.0)
    out = t.merge(out[["record_id", "water_frac"]], on="record_id", how="left")
    if out.water_frac.isna().any():
        raise RuntimeError(f"[BLOCKED] {int(out.water_frac.isna().sum())} park pieces without a water result")
    out = out.sort_values("record_id").reset_index(drop=True)
    out.to_parquet(OUT, index=False)
    MANIFEST.write_text(json.dumps(dict(inputs=inputs, output_sha256=sha256(OUT), url_pattern=URL, water_min=WATER_MIN),
                                   indent=2, sort_keys=True) + "\n")
    print(f"  ✓ park water: {len(out):,} pieces in {len(counties)} counties", flush=True)
    return out

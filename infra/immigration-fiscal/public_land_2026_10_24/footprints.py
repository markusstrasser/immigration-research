"""Normalize acquired facility geometry without treating missing ownership as public.

Native-First: DuckDB spatial reads primary GeoJSON and Parquet and writes LF inventory CSV.
``uv run --no-project --with duckdb python3 -I {lane}/footprints.py``.
No unmatched-facility acreage is imputed. Source polygons are kept separately from modelled land values.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import inspect
import json
from pathlib import Path
import resource
import shutil
import time

import duckdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "footprints"
OUT = HERE / "derived"
ACRE = 4046.8564224
RELEASE = "2026-10-21.0"


def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1_048_576):
            h.update(chunk)
    return h.hexdigest()


def input_hashes():
    files=[Path(__file__).resolve(),CACHE/'padus'/'count.json']
    files+=sorted((CACHE/'padus').glob('page_*.geojson'))
    files+=[CACHE/'padus'/'tribal_count.json',CACHE/'padus'/'tribal.geojson']
    files+=[CACHE/'padus'/'requests.json',CACHE/'padus'/'tribal.geojson.request.json']
    files += [CACHE/f'overture_{k}_{RELEASE}.parquet' for k in ('land_use','infrastructure')]
    files += sorted((HERE.parent/'school_land_2026_10_24'/'_cache'/'tracts2010').glob('gz_2010_*_140_00_500k.zip'))
    return {str(p):sha256(p) for p in files}


def cached_outputs(inputs,out):
    manifest=CACHE/'normalized_manifest.json'
    if not manifest.exists():
        return False
    data=json.loads(manifest.read_text())
    if data.get('inputs')!=inputs:
        return False
    for name,expected in data['outputs'].items():
        p=CACHE/name
        if not p.exists() or sha256(p)!=expected:
            return False
    for name in ('footprint_coverage.csv','footprint_sources.json'):
        shutil.copyfile(CACHE/'normalization_outputs'/name,out/name)
    print('Footprint normalization: input/source/output hash-validated cache hit',flush=True)
    return True


def cache_outputs(inputs,out):
    saved=CACHE/'normalization_outputs'
    saved.mkdir(parents=True,exist_ok=True)
    for name in ('footprint_coverage.csv','footprint_sources.json'):
        shutil.copyfile(out/name,saved/name)
    names=['facility_records.parquet','padus_parks.parquet','park_tracts.parquet',
           'normalization_outputs/footprint_coverage.csv','normalization_outputs/footprint_sources.json']
    outputs={name:sha256(CACHE/name) for name in names}
    (CACHE/'normalized_manifest.json').write_text(json.dumps({'inputs':inputs,'outputs':outputs},indent=2,sort_keys=True)+'\n')


def connect():
    c = duckdb.connect()
    c.execute("LOAD spatial; SET geometry_always_xy=true; SET enable_progress_bar=false; SET threads=1")
    return c


def load_padus_raw(c,pages):
    """Avoid repeating the dominant GeoJSON parse while topology repairs are inspected."""
    dest=CACHE/'padus_raw.parquet'
    manifest=CACHE/'padus_raw_manifest.json'
    inputs={str(p):sha256(p) for p in pages}
    inputs['parser_definition']=hashlib.sha256(inspect.getsource(load_padus_raw).encode()).hexdigest()
    inputs['duckdb_version']=duckdb.__version__
    if dest.exists() and manifest.exists():
        prior=json.loads(manifest.read_text())
        if prior['inputs']==inputs and prior['output_sha256']==sha256(dest):
            c.execute(f"CREATE OR REPLACE TEMP TABLE padus_raw AS SELECT * EXCLUDE(wkb),ST_GeomFromWKB(wkb) AS g FROM read_parquet('{dest}')")
            print('PAD-US raw parse: hash-validated cache hit',flush=True)
            return
    c.execute("CREATE OR REPLACE TEMP TABLE padus_raw AS " + " UNION ALL ".join(
        f"SELECT OBJECTID,Category,Own_Type,Own_Name,Mang_Type,Mang_Name,Des_Tp,Unit_Nm,State_Nm,GIS_Acres,Pub_Access,Source_PAID,geom AS g FROM ST_Read('{p}')" for p in pages))
    c.execute(f"COPY (SELECT * EXCLUDE(g),ST_AsWKB(g) AS wkb FROM padus_raw ORDER BY OBJECTID) TO '{dest}' (FORMAT parquet,COMPRESSION zstd)")
    manifest.write_text(json.dumps({'inputs':inputs,'output_sha256':sha256(dest)},indent=2,sort_keys=True)+'\n')


def normalize_padus(c):
    pages = sorted((CACHE / "padus").glob("page_*.geojson"))
    count_path = CACHE / "padus" / "count.json"
    if not pages or not count_path.exists():
        raise RuntimeError("[BLOCKED] PAD-US pages absent; run acquire_footprints.py")
    expected = json.loads(count_path.read_text())["count"]
    load_padus_raw(c,pages)
    tribal_count_path=CACHE/'padus'/'tribal_count.json'
    if not tribal_count_path.exists():
        raise RuntimeError('[BLOCKED] tribal park ownership probe absent')
    tribal_count=json.loads(tribal_count_path.read_text())['count']
    if tribal_count:
        tribal_path=CACHE/'padus'/'tribal.geojson'
        if not tribal_path.exists():
            raise RuntimeError('[BLOCKED] tribal park source absent')
        c.execute(f"""INSERT INTO padus_raw SELECT OBJECTID,Category,Own_Type,Own_Name,Mang_Type,Mang_Name,Des_Tp,Unit_Nm,State_Nm,GIS_Acres,Pub_Access,Source_PAID,geom AS g FROM ST_Read('{tribal_path}')""")
        expected+=tribal_count
    invalid_input=c.execute('SELECT count(*) FROM padus_raw WHERE NOT ST_IsValid(g)').fetchone()[0]
    print(f'PAD-US raw invalid geometries: {invalid_input}',flush=True)
    c.execute("""CREATE OR REPLACE TEMP TABLE padus_repair AS SELECT *,
       CASE WHEN ST_IsValid(g) THEN g ELSE TRY(ST_CollectionExtract(ST_MakeValid(g,'structure',false),3)) END AS repaired
       FROM padus_raw""")
    fallback=c.execute('SELECT count(*) FROM padus_repair WHERE repaired IS NULL').fetchone()[0]
    if fallback:
        print(f'[DEGRADED] PAD-US structure repair failed for {fallback} records; explicit zero-buffer repair',flush=True)
    c.execute("""CREATE OR REPLACE TEMP TABLE padus AS SELECT * EXCLUDE(g,repaired),
       CASE WHEN repaired IS NOT NULL THEN repaired ELSE TRY(ST_Buffer(g,0)) END AS g
       FROM padus_repair""")
    unresolved=c.execute('SELECT OBJECTID FROM padus WHERE g IS NULL OR NOT ST_IsValid(g) ORDER BY OBJECTID').fetchall()
    if unresolved:
        raise RuntimeError(f'[BLOCKED] unresolved PAD-US geometry repairs: {unresolved[:20]} ({len(unresolved)} total)')
    fallback_rows=c.execute(f"""SELECT r.OBJECTID,r.Unit_Nm,r.GIS_Acres,
       ST_Area_Spheroid(r.g)/{ACRE},ST_Area_Spheroid(p.g)/{ACRE}
       FROM padus_repair r JOIN padus p USING(OBJECTID) WHERE r.repaired IS NULL ORDER BY r.OBJECTID""").fetchall()
    fallback_details=[dict(zip(['objectid','name','reported_acres','raw_geometry_acres','repaired_acres'],r)) for r in fallback_rows]
    n, distinct = c.execute("SELECT count(*),count(DISTINCT OBJECTID) FROM padus").fetchone()
    if n != expected or distinct != n:
        raise RuntimeError(f"[BLOCKED] PAD-US count/duplicate mismatch: {n}/{distinct}/{expected}")
    invalid = c.execute("SELECT count(*) FROM padus WHERE Category<>'Fee' OR Own_Type NOT IN ('STAT','DIST','LOC','TRIB') OR Des_Tp NOT IN ('SP','SREC','LP','LREC','REC')").fetchone()[0]
    if invalid:
        raise RuntimeError(f"[BLOCKED] {invalid} PAD-US records violate public park fee filter")
    dest = CACHE / "padus_parks.parquet"
    c.execute(f"""COPY (SELECT 'padus:'||OBJECTID AS id,'park' AS class,Unit_Nm AS name,
      ST_Area_Spheroid(g) AS area_m2,ST_AsWKB(g) AS wkb,
      ST_X(ST_PointOnSurface(g)) AS lon,ST_Y(ST_PointOnSurface(g)) AS lat,
      Own_Type AS own_type,Own_Name AS own_name,Mang_Type AS manager_type,Mang_Name AS manager_name,
      Des_Tp AS designation,State_Nm AS state_abbr,GIS_Acres AS reported_acres,Pub_Access AS public_access,
      Source_PAID AS source_id,'public_fee' AS ownership,'PAD-US 4.1 Fee Managers' AS source
      FROM padus ORDER BY OBJECTID) TO '{dest}' (FORMAT parquet,COMPRESSION zstd)""")
    result = c.execute(f"SELECT count(*),sum(area_m2)/{ACRE},sum(reported_acres) FROM read_parquet('{dest}')").fetchone()
    print(f"PAD-US park rows={result[0]:,}; geometry_acres={result[1]:,.0f}; reported_acres={result[2]:,.0f}", flush=True)
    return {"count": n, "geometry_acres": result[1], "reported_acres_sum": result[2],"invalid_source_geometries_repaired":invalid_input,
            "zero_buffer_fallback_records":fallback,
            "zero_buffer_fallback_details":fallback_details,
            "query_count": expected, "ownership": "public fee (STAT/DIST/LOC/TRIB)","tribal_fee_records":tribal_count,
            "designation_filter": ["SP", "SREC", "LP", "LREC", "REC"],
            "geometry_precision_degrees": 0.00001,
            "api_generalization_max_degrees": 0.00005,
            "per_page_requests": "_cache/footprints/padus/requests.json",
            "per_page_requests_sha256": sha256(CACHE/'padus'/'requests.json'),
            "tribal_request": "_cache/footprints/padus/tribal.geojson.request.json",
            "overlap_policy": "unique OBJECTID; exact duplicate geometries flagged, all positive-area tract overlaps dissolved by stable source ID",
            "scope_limit": "state/local park designation does not identify only capital-bearing or saleable acres"}


def normalize_overture(c):
    paths = [CACHE / f"overture_{k}_{RELEASE}.parquet" for k in ("land_use", "infrastructure")]
    if not all(p.exists() for p in paths):
        raise RuntimeError("[BLOCKED] Overture extracts absent; run acquire_footprints.py")
    source = " UNION ALL ".join(f"SELECT * FROM read_parquet('{p}')" for p in paths)
    c.execute("CREATE OR REPLACE TEMP TABLE ov_raw AS " + source)
    duplicate_ids = c.execute("SELECT count(*)-count(DISTINCT id) FROM ov_raw").fetchone()[0]
    if duplicate_ids:
        raise RuntimeError(f"[BLOCKED] {duplicate_ids} duplicate Overture IDs across extracts; inspect before pricing")
    # Class declarations come from OSM source tags/Overture, never from a name heuristic.
    classify = """CASE
      WHEN class IN ('university','college') THEN 'college'
      WHEN class IN ('hospital','clinic') THEN 'health'
      WHEN source_tags['amenity'] IN ('police','fire_station','prison') THEN 'public_safety'
      WHEN source_tags['amenity'] IN ('townhall','courthouse') OR source_tags['office']='government' THEN 'government'
      WHEN source_tags['man_made']='wastewater_plant' OR source_tags['industrial']='wastewater_treatment' THEN 'sewer'
      WHEN source_tags['man_made'] IN ('water_works','water_treatment_plant','pumping_station') OR source_tags['amenity']='water_works'
        OR source_tags['industrial']='water_treatment' OR class IN ('water_tower','reservoir_covered') THEN 'water'
      WHEN class IN ('substation','plant') THEN 'power'
      WHEN class IN ('airport','municipal_airport','regional_airport','international_airport','private_airport',
        'military_airport','airstrip','seaplane_airport','heliport') THEN 'airport'
      WHEN class IN ('railway_station','bus_station','subway_station','railway_halt') OR source_tags['amenity']='bus_station' THEN 'transit'
      WHEN class IN ('ferry_terminal','quay') OR source_tags['landuse'] IN ('port','harbour')
        OR source_tags['industrial']='port' OR source_tags['amenity']='ferry_terminal' THEN 'port'
      WHEN class='toll_booth' THEN 'toll'
      WHEN class='residential' OR source_tags['social_facility'] IN ('group_home','shelter','assisted_living') THEN 'housing'
      ELSE class||'_unclassified' END"""
    ownership = """CASE
      WHEN lower(coalesce(source_tags['owner:type'],source_tags['ownership'],'')) IN ('government','public','federal','state','county','municipal','local') THEN 'public_owner_tag'
      WHEN lower(coalesce(source_tags['owner:type'],source_tags['ownership'],'')) IN ('private','religious','commercial') THEN 'private_owner_tag'
      WHEN lower(coalesce(source_tags['operator:type'],'')) IN ('government','public','federal','state','county','municipal','local') THEN 'government_operator_tag'
      WHEN lower(coalesce(source_tags['operator:type'],'')) IN ('private','religious','private_non_profit','commercial') THEN 'private_operator_tag'
      ELSE 'unknown' END"""
    dest = CACHE / "facility_records.parquet"
    c.execute(f"""COPY (SELECT id,{classify} AS class,class AS overture_class,name,area_m2,wkb,
      ST_X(ST_PointOnSurface(ST_GeomFromWKB(wkb))) AS lon,
      ST_Y(ST_PointOnSurface(ST_GeomFromWKB(wkb))) AS lat,
      {ownership} AS ownership,source_tags,source_type,source_dataset,source_record,geometry_type,
      source_tags['operator'] AS operator,source_tags['owner'] AS owner,
      source_tags['operator:type'] AS operator_type,source_tags['owner:type'] AS owner_type,
      source_tags['access'] AS access
      FROM ov_raw ORDER BY id) TO '{dest}' (FORMAT parquet,COMPRESSION zstd)""")
    # Point/line records remain as coverage observations, never positive-acre land estimates.
    rows = c.execute(f"""SELECT 'Overture' AS source,class,ownership,count(*) AS features,
      count(*) FILTER (WHERE area_m2>0) AS polygons,sum(area_m2)/{ACRE} AS acres
      FROM read_parquet('{dest}') GROUP BY 1,2,3 ORDER BY 2,3""").fetchall()
    return rows


def park_tracts(c):
    """Split parks at 2010 tract boundaries, union overlaps within each tract.

    Overlaps are assigned to the lexicographically first stable source ID. Each later site loses
    the union of its overlaps with prior IDs, retaining original acreage for the B/C discount.
    It does not price whole parks at centroid tract prices.
    """
    tracts = sorted((HERE.parent / "school_land_2026_10_24" / "_cache" / "tracts2010").glob("gz_2010_*_140_00_500k.zip"))
    if len(tracts) != 51:
        raise RuntimeError(f"[BLOCKED] expected 51 2010 tract archives, found {len(tracts)}")
    dest = CACHE / "park_tracts.parquet"
    trq = " UNION ALL ".join(f"SELECT substr(GEO_ID,10) AS tract,ST_MakeValid(geom) AS g FROM ST_Read('/vsizip/{p}/{p.name.replace('.zip','.shp')}')" for p in tracts)
    c.execute("CREATE OR REPLACE TEMP TABLE park_tr AS " + trq)
    c.execute(f"CREATE OR REPLACE TEMP TABLE park_geom AS SELECT id,area_m2/{ACRE} AS site_acres,own_type,public_access,ST_GeomFromWKB(wkb) AS g FROM read_parquet('{CACHE / 'padus_parks.parquet'}')")
    print("Intersecting PAD-US parks with 2010 tracts...", flush=True)
    c.execute("""CREATE OR REPLACE TEMP TABLE park_pieces AS
       SELECT p.id,t.tract,p.site_acres,p.own_type,p.public_access,ST_Intersection(p.g,t.g) AS g
       FROM park_geom p JOIN park_tr t ON ST_Intersects(p.g,t.g)""")
    print("Assigning overlapping PAD-US pieces by stable source ID...",flush=True)
    c.execute("""CREATE OR REPLACE TEMP TABLE park_prior AS
       SELECT p.id,p.tract,ST_Union_Agg(o.g) AS g
       FROM park_pieces p JOIN park_pieces o
       ON p.tract=o.tract AND o.id<p.id
       AND ST_XMin(p.g)<=ST_XMax(o.g) AND ST_XMin(o.g)<=ST_XMax(p.g)
       AND ST_YMin(p.g)<=ST_YMax(o.g) AND ST_YMin(o.g)<=ST_YMax(p.g)
       AND ST_Intersects(p.g,o.g)
       GROUP BY p.id,p.tract""")
    c.execute("""CREATE OR REPLACE TEMP TABLE park_dissolved AS
       SELECT p.*,CASE WHEN o.g IS NULL THEN p.g ELSE ST_Difference(p.g,o.g) END AS exclusive_g
       FROM park_pieces p LEFT JOIN park_prior o USING(id,tract)""")
    c.execute(f"""COPY (SELECT p.id,p.tract,substr(p.tract,1,5) AS county,p.site_acres,p.own_type,p.public_access,
       ST_Area_Spheroid(p.g)/{ACRE} AS raw_acres,
       ST_Area_Spheroid(p.exclusive_g)/{ACRE} AS acres
       FROM park_dissolved p
       WHERE ST_Area_Spheroid(p.g)>0 ORDER BY p.id,p.tract)
       TO '{dest}' (FORMAT parquet,COMPRESSION zstd)""")
    pieces,sites,acres,raw = c.execute(f"SELECT count(*),count(DISTINCT id),sum(acres),sum(raw_acres) FROM read_parquet('{dest}')").fetchone()
    total = c.execute("SELECT sum(site_acres) FROM park_geom").fetchone()[0]
    metrics = {"pieces": pieces,"matched_sites": sites,"site_count": c.execute("SELECT count(*) FROM park_geom").fetchone()[0],
       "raw_intersected_acres": raw,"union_intersected_acres": acres,"source_geometry_acres": total,
       "raw_area_coverage": raw/total,"overlap_acres_removed": raw-acres,
       "overlap_rule": "subtract union of all earlier lexicographic source IDs within each tract; original site acreage determines B/C discounts",
       "pricing_rule": "tract prices apply to intersected pieces, with source-site acreage retained for B/C discounts"}
    print("PAD-US tract split:",metrics,flush=True)
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    start = time.perf_counter()
    args.out.mkdir(parents=True, exist_ok=True)
    inputs=input_hashes()
    if cached_outputs(inputs,args.out):
        print(f'elapsed_s={time.perf_counter()-start:.3f}; maxrss_raw={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}',flush=True)
        return
    c = connect()
    stage=time.perf_counter()
    padus = normalize_padus(c)
    print(f'PAD-US normalization elapsed_s={time.perf_counter()-stage:.3f}',flush=True)
    stage=time.perf_counter()
    park_split = park_tracts(c)
    print(f'PAD-US tract split elapsed_s={time.perf_counter()-stage:.3f}',flush=True)
    stage=time.perf_counter()
    rows = normalize_overture(c)
    print(f'Overture normalization elapsed_s={time.perf_counter()-stage:.3f}',flush=True)
    rows.append(("PAD-US 4.1", "park", "public_fee", padus["count"], padus["count"], padus["geometry_acres"]))
    with (args.out / "footprint_coverage.csv").open("w", newline="") as f:
        w = csv.writer(f,lineterminator="\n")
        w.writerow(["source", "class", "ownership", "features", "polygons", "acres"])
        w.writerows(rows)
    dup = c.execute(f"SELECT count(*)-count(DISTINCT sha256(wkb)) FROM read_parquet('{CACHE / 'padus_parks.parquet'}')").fetchone()[0]
    padus["exact_duplicate_geometries"] = dup
    (args.out / "footprint_sources.json").write_text(json.dumps({"padus": padus,"park_tract_split":park_split,
       "overture": {"release": RELEASE,"ownership_limit": "operator:type government is operating evidence, not a fee-title record; unknown is retained",
          "overlap_policy": "stable IDs retained for authoritative point matching; a facility is priced once after parent matches; unmatched acres never imputed",
          "coverage_limit": "OSM footprints are an incomplete volunteer map, not a complete facility universe"}},indent=2,sort_keys=True)+"\n")
    for row in rows:
        print(row,flush=True)
    cache_outputs(inputs,args.out)
    print(f"elapsed_s={time.perf_counter()-start:.3f}; maxrss_raw={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}",flush=True)


if __name__ == "__main__":
    main()

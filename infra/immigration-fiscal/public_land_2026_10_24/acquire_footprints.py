"""Acquire primary facility geometry by remote pushdown and USGS PAD-US Fee queries.

Native-First: DuckDB remote Parquet predicates and the existing ArcGIS query API.
Run with ``uv run --no-project --with duckdb python3 -I {lane}/acquire_footprints.py``.
The main build consumes these cached primary extracts; acquisition never imputes missing land.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import threading
import time
import urllib.parse

import duckdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "footprints"
RELEASE = "2026-10-21.0"
OVERTURE = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=base/type={{kind}}/*.parquet"
PADUS = "https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Fee_Managers_PADUS/FeatureServer/0"
PAD_WHERE = "Category = 'Fee' AND Own_Type IN ('STAT','DIST','LOC') AND Des_Tp IN ('SP','SREC','LP','LREC','REC')"
TRIBAL_WHERE = "Category = 'Fee' AND Own_Type = 'TRIB' AND Des_Tp IN ('SP','SREC','LP','LREC','REC')"
BOXES = [(-125., 24., -66.5, 49.5), (-180., 51., -129., 71.6), (-160.6, 18.8, -154.7, 22.4)]
LAND_CLASSES = ("university", "college", "hospital", "clinic", "institutional", "works", "railway", "residential")
# Keep explicit civic/utility source tags even when Overture's coarser class is commercial/industrial.
TAG_FILTER = """(source_tags['amenity'] IN ('townhall','courthouse','police','fire_station','prison','bus_station','ferry_terminal','water_works')
 OR source_tags['office'] = 'government' OR source_tags['landuse'] IN ('port','harbour','railway')
 OR source_tags['man_made'] IN ('water_works','wastewater_plant','water_treatment_plant','pumping_station')
 OR source_tags['industrial'] IN ('port','water_treatment','wastewater_treatment')
 OR source_tags['social_facility'] IN ('group_home','shelter','assisted_living'))"""
INFRA_FILTER = """(class IN ('airport','municipal_airport','regional_airport','international_airport','private_airport',
 'military_airport','airstrip','seaplane_airport','heliport','railway_station','bus_station','ferry_terminal',
 'subway_station','railway_halt','substation','plant','water_tower','reservoir_covered','toll_booth','quay'))"""
REQUEST_LOCK = threading.Lock()
NEXT_REQUEST = 0.0


def connection():
    c = duckdb.connect()
    c.execute("LOAD spatial; LOAD httpfs; SET s3_region='us-west-2'; SET geometry_always_xy=true; SET enable_progress_bar=false")
    return c


def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        subprocess.run(["curl", "--http1.1", "--fail", "--silent", "--show-error", "--location", "--retry", "3", "--retry-all-errors", "--max-time", "120", "--output", str(tmp), url], check=True)
        if tmp.stat().st_size > 1_000_000_000:
            raise RuntimeError(f"[BLOCKED] oversized source {tmp}")
        tmp.rename(dest)
        dest.with_suffix(dest.suffix+'.request.json').write_text(json.dumps({'url':url},indent=2,sort_keys=True)+'\n')
    return dest


def query_url(params):
    # RFC3986 percent-encoding also matches ArcGIS's cacheable query URLs (%20, not +).
    return PADUS + "/query?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def geometry_request_slot():
    """ESRI permits at most 60 large non-cacheable geometry queries per minute."""
    global NEXT_REQUEST
    with REQUEST_LOCK:
        delay = max(0.0, NEXT_REQUEST - time.monotonic())
        if delay:
            time.sleep(delay)
        NEXT_REQUEST = time.monotonic() + 1.25


def validate_arcgis_page(data,expected):
    """Fail on HTTP-200 ArcGIS errors and truncation, before a response becomes usable data."""
    if 'error' in data:
        raise RuntimeError(f"[BLOCKED] ArcGIS service error: {data['error']}")
    features=data.get('features')
    if not isinstance(features,list) or len(features)!=expected:
        raise RuntimeError(f"[BLOCKED] ArcGIS page has {len(features) if isinstance(features,list) else 'no'} features; expected {expected}")
    return features


def acquire_padus():
    root = CACHE / "padus"
    schema = fetch(PADUS + "?f=pjson", root / "schema.json")
    p = json.loads(schema.read_text())
    if "error" in p or not p.get("advancedQueryCapabilities", {}).get("supportsPagination"):
        raise RuntimeError("[BLOCKED] PAD-US Fee service/schema unavailable or not paginated")
    # The schema's coded-value domains are the machine-readable ownership/designation codebook.
    # USGS's prose help is read separately: its web frontend rejects curl with HTTP 403.
    fetch("https://www.arcgis.com/sharing/rest/content/items/a516f406610b42d8a755c25665324201?f=pjson", root / "source_item.json")
    count_url = query_url({"where": PAD_WHERE, "returnCountOnly": "true", "f": "json"})
    count = json.loads(fetch(count_url, root / "count.json").read_text())["count"]
    size = min(int(p["maxRecordCount"]), 2000)
    fields = "OBJECTID,Category,Own_Type,Own_Name,Mang_Type,Mang_Name,Des_Tp,Unit_Nm,State_Nm,GIS_Acres,Pub_Access,Source_PAID"

    def small_pages(params, offset, expected, destination):
        features = []
        for suboffset in range(offset, offset+expected, 500):
            part_expected = min(500,offset+expected-suboffset)
            subparams = dict(params,resultOffset=suboffset,resultRecordCount=part_expected)
            part_path = root / "subpages" / f"page_{suboffset:06d}_{part_expected}.geojson"
            for attempt in range(3):
                if not part_path.exists():
                    geometry_request_slot()
                data = json.loads(fetch(query_url(subparams),part_path).read_text())
                if len(data.get("features",[])) == part_expected:
                    validate_arcgis_page(data,part_expected)
                    break
                error = data.get("error",{})
                if error.get("code") != 429:
                    raise RuntimeError(f"[BLOCKED] PAD-US subpage {suboffset}: {error}")
                failed = root / "errors" / f"small_{suboffset:06d}_{attempt}.json"
                part_path.replace(failed)
                time.sleep(30)
            else:
                raise RuntimeError(f"[BLOCKED] PAD-US small page {suboffset} repeatedly rate-limited")
            features.extend(data["features"])
        if len(features)!=expected:
            raise RuntimeError(f"[BLOCKED] merged PAD-US page count {len(features)}/{expected}")
        merged={"type":"FeatureCollection","crs":{"type":"name","properties":{"name":"EPSG:4326"}},"features":features}
        destination.write_text(json.dumps(merged,separators=(",",":"))+"\n")
        return destination

    def page(offset):
        params = {"where": PAD_WHERE, "outFields": fields, "resultOffset": offset,
                  "resultRecordCount": size, "orderByFields": "OBJECTID", "outSR": "4326",
                  "geometryPrecision": 5, "maxAllowableOffset": 0.00005,
                  "f": "geojson", "cacheHint": "true"}
        path = root / f"page_{offset:06d}.geojson"
        expected = min(size, count - offset)
        for attempt in range(4):
            cached = path.exists()
            if not cached:
                geometry_request_slot()
            fetch(query_url(params), path)
            data = json.loads(path.read_text())
            if len(data.get("features", [])) == expected:
                validate_arcgis_page(data,expected)
                return path
            error = data.get("error", {})
            if error.get("code") == 429:
                # HTTP 200 is not proof of a successful ArcGIS response; retain the failure receipt.
                failed = root / "errors" / f"page_{offset:06d}_attempt_{attempt}.json"
                failed.parent.mkdir(parents=True, exist_ok=True)
                path.replace(failed)
                print(f"PAD-US {'cached' if cached else 'live'} large-geometry quota at page {offset}; using 500-row pages",flush=True)
                return small_pages(params,offset,expected,path)
            raise RuntimeError(f"[BLOCKED] incomplete PAD-US page {offset}: {len(data.get('features', []))}/{expected}; {error}")
        raise RuntimeError(f"[BLOCKED] PAD-US quota persists at page {offset}")

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(page, i) for i in range(0, count, size)]
        for i, future in enumerate(as_completed(futures), 1):
            future.result()
            if i % 10 == 0 or i == len(futures):
                print(f"PAD-US: {i}/{len(futures)} pages", flush=True)
    print(f"PAD-US public park fee polygons: {count:,}", flush=True)
    tribal_count=json.loads(fetch(query_url({'where':TRIBAL_WHERE,'returnCountOnly':'true','f':'json'}),root/'tribal_count.json').read_text())['count']
    if tribal_count:
        tribal_params={'where':TRIBAL_WHERE,'outFields':fields,'resultRecordCount':2000,'orderByFields':'OBJECTID',
          'outSR':'4326','geometryPrecision':5,'maxAllowableOffset':0.00005,'f':'geojson','cacheHint':'true'}
        tribal=json.loads(fetch(query_url(tribal_params),root/'tribal.geojson').read_text())
        validate_arcgis_page(tribal,tribal_count)
    print(f'PAD-US tribal park fee polygons: {tribal_count}',flush=True)


def padus_request_inventory():
    """Retain the actual scientific query parameters, including the single generalized page.

    Initial successful pages predate request sidecars. Their offsets/500-row fallback batches
    and precision are reconstructed from this acquisition run; the initial run generalized
    only page 132000. Subsequent real downloads write exact request sidecars directly.
    """
    root=CACHE/'padus'
    records=[]
    fields='OBJECTID,Category,Own_Type,Own_Name,Mang_Type,Mang_Name,Des_Tp,Unit_Nm,State_Nm,GIS_Acres,Pub_Access,Source_PAID'
    for path in sorted(root.glob('page_*.geojson')):
        offset=int(path.stem.split('_')[1])
        data=json.loads(path.read_text())
        if 'features' not in data:
            raise RuntimeError(f'[BLOCKED] error receipt still present as data: {path}')
        merged='properties' not in data
        parts=list(range(offset,offset+len(data['features']),500)) if merged else [offset]
        queries=[]
        for part in parts:
            params={'where':PAD_WHERE,'outFields':fields,'resultOffset':part,
              'resultRecordCount':min(500,offset+len(data['features'])-part) if merged else len(data['features']),
              'orderByFields':'OBJECTID','outSR':'4326','geometryPrecision':5,'f':'geojson','cacheHint':'true'}
            generalized=offset==132000
            if generalized:
                params['maxAllowableOffset']=0.00005
            sidecar=(root/'subpages'/f'page_{part:06d}_{params["resultRecordCount"]}.geojson.request.json') if merged else path.with_suffix(path.suffix+'.request.json')
            url=json.loads(sidecar.read_text())['url'] if sidecar.exists() else query_url(params)
            actual=urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
            queries.append({'url':url,'offset':part,'count':params['resultRecordCount'],
               'geometry_precision_decimal_places':int(actual.get('geometryPrecision',['5'])[0]),
               'max_allowable_offset_degrees':float(actual.get('maxAllowableOffset',['0'])[0]),
               'provenance':'request sidecar' if sidecar.exists() else 'acquisition-run parameter history; scientific query reconstructed'})
        records.append({'path':str(path.relative_to(HERE)),'merged_500_row_fallback':merged,'queries':queries})
    (root/'requests.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')


def acquire_overture(kind):
    dest = CACHE / f"overture_{kind}_{RELEASE}.parquet"
    if dest.exists():
        print(f"exists: {dest.name}", flush=True)
        return
    c = connection()
    rel = OVERTURE.format(kind=kind)
    if kind == "land_use":
        classes = ",".join("'" + x + "'" for x in LAND_CLASSES if x != "residential")
        # Housing gets only tagged public/social facilities; all residential polygons would be >1m rows.
        filt = f"(class IN ({classes}) OR (class IN ('commercial','industrial','residential') AND {TAG_FILTER}) OR (class='residential' AND (source_tags['residential']='social_housing' OR source_tags['operator:type'] IN ('government','public'))))"
    else:
        filt = INFRA_FILTER
    select = """SELECT id, '{kind}' AS source_type, class, subtype, names."primary" AS name,
      source_tags, sources[1].dataset AS source_dataset, sources[1].record_id AS source_record,
      ST_Area_Spheroid(geometry) AS area_m2, bbox.xmin AS xmin, bbox.xmax AS xmax,
      bbox.ymin AS ymin, bbox.ymax AS ymax, ST_AsWKB(geometry) AS wkb,
      ST_GeometryType(geometry)::VARCHAR AS geometry_type
      FROM read_parquet('{rel}') WHERE bbox.xmin >= {a} AND bbox.xmax <= {cx}
      AND bbox.ymin >= {b} AND bbox.ymax <= {d} AND {filt}"""
    union = " UNION ALL ".join(select.format(kind=kind, rel=rel, a=a, b=b, cx=cx, d=d, filt=filt)
                               for a, b, cx, d in BOXES)
    tmp = dest.with_suffix(".tmp.parquet")
    print(f"Overture {kind}: remote bbox/class predicate query started",flush=True)
    c.execute(f"COPY (SELECT DISTINCT ON (id) * FROM ({union}) ORDER BY id) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
    tmp.rename(dest)
    print(kind, c.execute(f"SELECT class, count(*),sum(area_m2)/4046.8564224 FROM read_parquet('{dest}') GROUP BY 1 ORDER BY 1").fetchall(), flush=True)


def manifest():
    rows = []
    for p in sorted(CACHE.rglob("*")):
        if p.is_file() and p.name != "manifest.json" and ".tmp" not in p.name:
            h = hashlib.sha256()
            with p.open("rb") as f:
                while chunk := f.read(1_048_576):
                    h.update(chunk)
            rows.append({"path": str(p.relative_to(HERE)), "bytes": p.stat().st_size, "sha256": h.hexdigest()})
    if sum(x["bytes"] for x in rows) > 2_000_000_000:
        raise RuntimeError("[BLOCKED] footprint cache exceeds assigned 2 GB budget")
    (CACHE / "manifest.json").write_text(json.dumps({"overture_release": RELEASE, "overture_sources": [OVERTURE.format(kind=k) for k in ("land_use", "infrastructure")],
          "padus_service": PADUS, "padus_where": PAD_WHERE, "files": rows}, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["padus", "land_use", "infrastructure"])
    args = parser.parse_args()
    start = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.only in (None, "padus"):
        acquire_padus()
        padus_request_inventory()
    for kind in ("land_use", "infrastructure"):
        if args.only in (None, kind):
            acquire_overture(kind)
    manifest()
    print(f"elapsed_s={time.perf_counter()-start:.3f}; maxrss_raw={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}", flush=True)


if __name__ == "__main__":
    main()

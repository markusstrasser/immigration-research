"""Fetch the lane's file inputs into _cache/ (idempotent: present files are kept) and record them.

Each source lands in its own directory under _cache/ (downloads are untrusted data). Writes
derived/acquired_sources.json: url, local path, bytes and sha256 per file. The Overture polygons
come from acquire_overture.py (a remote query, not a download).

Sources
- FHFA WP 19-01 land prices, Version 4.0 (June 2024), plus the paper and FAQ.
- FHFA annual all-transactions HPI by county (2022 -> 2024 carry-forward of land prices).
- NCES EDGE public school geocodes 2023-24; CCD 2023-24 school directory (029) and membership (052).
- Census 2010 tract gazetteer and 2010 cartographic tract boundaries (FHFA tracts are 2010 tracts).
- California School Campus Database 2025 (GreenInfo Network; parcel-aligned campus polygons), the
  validation benchmark: layer 0 (one polygon per school, CDS code) and layer 2 (one per property).

    uv run --no-project python3 infra/immigration-fiscal/school_land_2026_10_24/acquire.py
"""
import hashlib
import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived" / "acquired_sources.json"
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19", "20",
          "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
          "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]
FILES = [
    ("fhfa", "https://www.fhfa.gov/document/land-prices_2024_20_june.xlsx"),
    ("fhfa", "https://www.fhfa.gov/document/wp1901.pdf"),
    ("fhfa", "https://www.fhfa.gov/document/faqs-land-10-28-20.pdf"),
    ("hpi", "https://www.fhfa.gov/hpi/download/annual/hpi_at_county.xlsx"),
    ("nces", "https://nces.ed.gov/programs/edge/data/EDGE_GEOCODE_PUBLICSCH_2324.zip"),
    ("nces", "https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_2324_w_1a_073124.zip"),
    ("nces", "https://nces.ed.gov/ccd/Data/zip/ccd_sch_052_2324_l_1a_073124.zip"),
    ("nces", "https://nces.ed.gov/ccd/Data/zip/ccd_sch_129_2324_w_1a_073124.zip"),
    ("gaz", "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/Gaz_tracts_national.zip"),
] + [("tracts2010", f"https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_{s}_140_00_500k.zip") for s in STATES]
CSCD = "https://services1.arcgis.com/4ZKi1B1zTblbwgWB/ArcGIS/rest/services/California_School_Campus_Database_2025/FeatureServer"
CSCD_LAYERS = {0: "schools_stacked", 2: "school_property"}
LOCAL_NAME = {"Gaz_tracts_national.zip": "Gaz_tracts_national_2010.zip"}


def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    subprocess.run(["curl", "-sSL", "--fail", "--retry", "5", "-C", "-", "-A", "Mozilla/5.0", "-o", str(part), url],
                   check=True)
    part.rename(dest)


def cscd(layer, name):
    """Page a CSCD layer as GeoJSON in WGS84 (2000 records a page), into one FeatureCollection."""
    dest = CACHE / "bench_cscd" / f"{name}.geojson"
    if dest.exists():
        return dest, f"{CSCD}/{layer}/query"
    feats, offset = [], 0
    while True:
        q = urllib.parse.urlencode({"where": "1=1", "outFields": "*", "outSR": 4326, "f": "geojson",
                                    "orderByFields": "OBJECTID", "resultOffset": offset, "resultRecordCount": 2000})
        raw = subprocess.run(["curl", "-sSL", "--fail", "--retry", "5", f"{CSCD}/{layer}/query?{q}"],
                             check=True, capture_output=True).stdout
        page = json.loads(raw)
        if "features" not in page:
            raise SystemExit(f"[BLOCKED] CSCD layer {layer} offset {offset}: {raw[:300]!r}")
        feats += page["features"]
        if len(page["features"]) < 2000:
            break
        offset += 2000
        time.sleep(0.5)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    return dest, f"{CSCD}/{layer}/query"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    rows = []
    for d, url in FILES:
        base = url.rsplit("/", 1)[1]
        dest = CACHE / d / LOCAL_NAME.get(base, base)
        fetch(url, dest)
        rows.append((url, dest))
    for layer, name in CSCD_LAYERS.items():
        dest, url = cscd(layer, name)
        rows.append((url, dest))
    ov = CACHE / "overture" / "us_education_2026-10-21.0.parquet"
    if not ov.exists():
        raise SystemExit("[BLOCKED] run acquire_overture.py first (remote query of Overture 2026-10-21.0 land_use)")
    rows.append(("s3://overturemaps-us-west-2/release/2026-10-21.0/theme=base/type=land_use/ (query in acquire_overture.py)", ov))
    man = [{"url": u, "path": str(p.relative_to(HERE)), "bytes": p.stat().st_size, "sha256": sha(p)} for u, p in rows]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(man, indent=1) + "\n")
    print(f"{len(man)} files, {sum(m['bytes'] for m in man) / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())

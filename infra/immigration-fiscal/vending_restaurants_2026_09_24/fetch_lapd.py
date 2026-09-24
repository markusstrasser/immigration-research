"""Direct pre-2018 vending measure inside the City of Los Angeles: LAPD arrests under the old street
vending ban (LAMC 42.00), 2010-2019, located to 2010 ZCTAs.

Source: LA open data `yru6-6re4` (Arrest Data from 2010 to 2019, LAPD), rows whose charge contains
"42.00"; the city's filtered view `7fnr-292v` ("Street Vending Citations LAMC 42.00") holds the same
rows. Subsection 42.00(c), soliciting employment for services, is dropped as not vending. Arrests are
placed in ZCTAs by point-in-polygon against the Census TIGER 2010 California ZCTA shapefile.
Records at (0, 0) are unlocated and counted separately.

These counts mix vending with enforcement effort: they locate where police acted against vendors.

Writes _cache/lapd/*.json, derived/lapd_vending_arrests_year.csv and
derived/lapd_vending_arrests_zcta.csv (arrests 2010-2016 by ZCTA). Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with shapely --with pyshp python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/fetch_lapd.py
"""
import json
import re
import zipfile
from collections import Counter

import shapefile
from shapely.geometry import Point, shape
from shapely.strtree import STRtree

from lib import CACHE, DERIVED, curl

URL = ("https://data.lacity.org/resource/yru6-6re4.json?$select=rpt_id,arst_date,charge,chrg_desc,lat,lon,rd,area"
       "&$where=charge%20like%20'%2542.00%25'&$limit=50000")
ZCTA_URL = "https://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_06_zcta510.zip"
SERVICES = re.compile(r"42\.00\s*\(?C", re.I)


def main() -> None:
    raw = CACHE / "lapd" / "lamc4200_arrests.json"
    if not raw.exists():
        curl(URL, raw)
    rows = json.loads(raw.read_text())
    if not 5000 <= len(rows) <= 5200:
        raise SystemExit(f"[FAILED] {len(rows)} LAMC 42.00 arrest rows; expected about 5,097")
    vend = [r for r in rows if not SERVICES.search(r.get("charge", ""))]
    by_year = Counter(int(r["arst_date"][:4]) for r in vend)
    zp = CACHE / "lapd" / "tl_2010_06_zcta510.zip"
    if not zp.exists():
        curl(ZCTA_URL, zp)
    zf = zipfile.ZipFile(zp)
    base = [n for n in zf.namelist() if n.endswith(".shp")][0][:-4]
    sf = shapefile.Reader(shp=zf.open(base + ".shp"), dbf=zf.open(base + ".dbf"), shx=zf.open(base + ".shx"))
    fields = [f[0] for f in sf.fields[1:]]
    zi = fields.index("ZCTA5CE10")
    geoms, codes = [], []
    for sr in sf.iterShapeRecords():
        geoms.append(shape(sr.shape.__geo_interface__))
        codes.append(sr.record[zi])
    tree = STRtree(geoms)
    per_zcta, unlocated, outside = Counter(), 0, 0
    for r in vend:
        lat, lon = float(r.get("lat") or 0), float(r.get("lon") or 0)
        if lat == 0 or lon == 0:
            unlocated += 1
            continue
        if int(r["arst_date"][:4]) > 2016:
            continue
        p = Point(lon, lat)
        hit = [i for i in tree.query(p) if geoms[i].contains(p)]
        if hit:
            per_zcta[codes[hit[0]]] += 1
        else:
            outside += 1
    DERIVED.mkdir(exist_ok=True)
    with (DERIVED / "lapd_vending_arrests_year.csv").open("w") as fh:
        fh.write("year,arrests\n")
        for y in sorted(by_year):
            fh.write(f"{y},{by_year[y]}\n")
    with (DERIVED / "lapd_vending_arrests_zcta.csv").open("w") as fh:
        fh.write("zcta,arrests_2010_2016\n")
        for z, n in sorted(per_zcta.items()):
            fh.write(f"{z},{n}\n")
    located = sum(per_zcta.values())
    print(f"  rows {len(rows)}; vending (excl. 42.00(c)) {len(vend)}; 2010-2016 located {located} in "
          f"{len(per_zcta)} ZCTAs; unlocated {unlocated}; outside CA ZCTAs {outside}")
    print("  by year: " + ", ".join(f"{y}: {by_year[y]}" for y in sorted(by_year)))


if __name__ == "__main__":
    main()

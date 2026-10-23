"""Pull US school-ground polygons from Overture Maps base/land_use, release 2026-10-21.0, remotely.

DuckDB reads the public S3 parquet with bbox/subtype pushdown, so only the US education rows are
fetched (the theme is 18.9 GB; nothing is downloaded whole). Kept: subtype 'education', classes
school, schoolyard, kindergarten and education (university/college/driving/music schools dropped).
Area is geodesic (ST_Area_Spheroid, lon/lat axis order set explicitly). Writes
_cache/overture/us_education_2026-10-21.0.parquet, sorted by id.

    uv run --no-project --with duckdb python3 infra/immigration-fiscal/school_land_2026_10_24/acquire_overture.py
"""
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
OUT = HERE / "_cache" / "overture" / "us_education_2026-10-21.0.parquet"
RELEASE = "s3://overturemaps-us-west-2/release/2026-10-21.0/theme=base/type=land_use/*.parquet"
CLASSES = ("school", "schoolyard", "kindergarten", "education")
# Conterminous US, Alaska, Hawaii (state membership is decided later by point-in-tract joins).
BOXES = [(-125.0, 24.0, -66.5, 49.5), (-180.0, 51.0, -129.0, 71.6), (-160.6, 18.8, -154.7, 22.4)]


def main():
    if OUT.exists():
        print(f"exists: {OUT}")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = duckdb.connect()
    c.execute("LOAD spatial; LOAD httpfs; SET s3_region='us-west-2'; SET geometry_always_xy = true;")
    cls = ",".join(f"'{k}'" for k in CLASSES)
    # One SELECT per box joined by UNION ALL: an OR of boxes defeats row-group pruning (a first run read
    # 2.5 GB in 20 minutes before it was stopped); a single box scans 568 of 3,968 row groups in ~13 s.
    sel = """SELECT id, class, names."primary" AS name,
                 source_tags['amenity'] AS amenity, source_tags['landuse'] AS landuse,
                 source_tags['operator:type'] AS operator_type, source_tags['isced:level'] AS isced,
                 sources[1].dataset AS src_dataset, sources[1].record_id AS src_record,
                 ST_Area_Spheroid(geometry) AS area_m2,
                 bbox.xmin AS xmin, bbox.xmax AS xmax, bbox.ymin AS ymin, bbox.ymax AS ymax,
                 ST_AsWKB(geometry) AS wkb
          FROM read_parquet('{rel}')
          WHERE bbox.xmin >= {a} AND bbox.xmax <= {cx} AND bbox.ymin >= {b} AND bbox.ymax <= {d}
            AND subtype = 'education' AND class IN ({cls})"""
    union = "\n UNION ALL \n".join(sel.format(rel=RELEASE, a=a, b=b, cx=cx, d=d, cls=cls) for a, b, cx, d in BOXES)
    tmp = OUT.with_suffix(".tmp.parquet")
    c.execute(f"COPY (SELECT DISTINCT ON (id) * FROM ({union}) ORDER BY id) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
    tmp.rename(OUT)
    n = c.execute(f"select class, count(*), sum(area_m2)/4046.8564224 from read_parquet('{OUT}') group by 1 order by 2 desc").fetchall()
    print(n)


if __name__ == "__main__":
    sys.exit(main())

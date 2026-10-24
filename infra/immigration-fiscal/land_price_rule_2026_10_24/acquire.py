"""Acquire the rural-price and urban/rural inputs; filter bulk files to small extracts.

Sources (all primary, fetched only when missing):
- USDA NASS Quick Stats bulk files: Census of Agriculture 2022 (county value of land and
  buildings per acre, land-use acres) and the economics file (June Agricultural Land Values
  survey: state farm real estate, cropland and pasture $/acre). The economics file name carries
  NASS's release date; the extract records the exact file and its sha256.
- Census TIGER/Line 2020 urban areas (2020 criteria, tl_2020_us_uac20).
- Census 2020 Gazetteer counties (internal points), for the nearest-FHFA-county rule.
- FHWA Highway Statistics 2022 Table SF-12A (state highway capital outlay by improvement type).

Raw files stay in the ignored `_cache/`; the bulk text is read as data, never executed.

    uv run --no-project python3 infra/immigration-fiscal/land_price_rule_2026_10_24/acquire.py
"""
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
NASS = CACHE / "nass"
GEO = CACHE / "geo"
CENSUS_URL = "https://www.nass.usda.gov/datasets/qs.census2022.txt.gz"
ECON_FILE = "qs.economics_20261023.txt.gz"
ECON_URL = "https://www.nass.usda.gov/datasets/" + ECON_FILE
UAC_URL = "https://www2.census.gov/geo/tiger/TIGER2020/UAC/tl_2020_us_uac20.zip"
GAZ_URL = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip"
SF12A_URL = "https://www.fhwa.dot.gov/policyinformation/statistics/2022/xls/sf12a.xlsx"
CENSUS_ITEMS = {
    "AG LAND, INCL BUILDINGS - ASSET VALUE, MEASURED IN $ / ACRE",
    "AG LAND, INCL BUILDINGS - ASSET VALUE, MEASURED IN $",
    "FARM OPERATIONS - ACRES OPERATED",
    "AG LAND, CROPLAND - ACRES",
    "AG LAND, PASTURELAND - ACRES",
    "AG LAND, WOODLAND - ACRES",
    "AG LAND, (EXCL CROPLAND & PASTURELAND & WOODLAND) - ACRES",
}
KEEP = ["SOURCE_DESC", "SHORT_DESC", "DOMAIN_DESC", "AGG_LEVEL_DESC", "STATE_FIPS_CODE", "STATE_ALPHA",
        "COUNTY_CODE", "COUNTY_NAME", "YEAR", "REFERENCE_PERIOD_DESC", "VALUE", "CV_%"]


def fetch(url, path):
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    subprocess.run(["curl", "-sSfL", "--max-time", "1200", "-o", str(tmp), url], check=True)
    tmp.rename(path)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def extract(src, dst, keep_row):
    n = 0
    with gzip.open(src, "rt", encoding="latin-1", newline="") as f, dst.open("w", newline="") as g:
        r = csv.DictReader(f, delimiter="\t")
        w = csv.writer(g, lineterminator="\n")
        w.writerow(KEEP)
        for row in r:
            if keep_row(row):
                w.writerow([row[k].strip() for k in KEEP])
                n += 1
    return n


def census_row(row):
    return (row["SHORT_DESC"] in CENSUS_ITEMS and row["DOMAIN_DESC"] == "TOTAL"
            and row["AGG_LEVEL_DESC"] in ("COUNTY", "STATE", "NATIONAL") and row["YEAR"] == "2022")


def econ_row(row):
    return (row["SOURCE_DESC"] == "SURVEY" and row["SHORT_DESC"].startswith("AG LAND")
            and "ASSET VALUE, MEASURED IN $ / ACRE" in row["SHORT_DESC"]
            and row["AGG_LEVEL_DESC"] in ("STATE", "NATIONAL") and row["DOMAIN_DESC"] == "TOTAL"
            and row["YEAR"].isdigit() and 2015 <= int(row["YEAR"]) <= 2026)


def main():
    raw = {"census": (CENSUS_URL, NASS / "qs.census2022.txt.gz"), "economics": (ECON_URL, NASS / ECON_FILE),
           "uac": (UAC_URL, GEO / "tl_2020_us_uac20.zip"), "gazetteer": (GAZ_URL, GEO / "2020_Gaz_counties_national.zip"),
           "fhwa_sf12a": (SF12A_URL, CACHE / "fhwa" / "sf12a_2022.xlsx")}
    for url, path in raw.values():
        fetch(url, path)
    manifest = {k: dict(url=u, path=str(p.relative_to(HERE)), bytes=p.stat().st_size, sha256=sha256(p)) for k, (u, p) in raw.items()}
    for name, src, rule in [("census2022_land.csv", raw["census"][1], census_row), ("survey_land_values.csv", raw["economics"][1], econ_row)]:
        dst = NASS / name
        if not dst.exists():
            n = extract(src, dst, rule)
            print(f"  ✓ {name}: {n:,} rows", flush=True)
        manifest[name] = dict(path=str(dst.relative_to(HERE)), bytes=dst.stat().st_size, sha256=sha256(dst))
    (CACHE / "acquire_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    if not sys.flags.isolated:
        raise SystemExit("run with python3 -I (raw downloads are data)")
    main()

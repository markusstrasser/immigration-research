#!/usr/bin/env python3
"""Arm D step 2: CBSA covariates from the Census ACS API and the TIGER
cartographic-boundary CBSA polygons.

Pulls, for every metropolitan/micropolitan statistical area:
  B03001_001E total population, B03001_004E Mexican-origin population
  B19013_001E median household income
from ACS 5-year 2023 (5-year is required: 1-year omits small CBSAs).

Also downloads cb_2023_us_cbsa_500k.zip (TIGER cartographic boundaries) for the
point-in-polygon assignment of OSM restaurants to CBSAs.

Validation is by content: the API table must carry all requested columns, >=900
CBSA rows, and a national Mexican-origin total within 5% of the published ~37.4
million (ACS 2019-2023 5-year).

Output: derived/cbsa_covariates.csv, _cache/tiger/cb_2023_us_cbsa_500k.zip
"""
import io
import os
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"
TIGER = LANE / "_cache" / "tiger"
DER.mkdir(exist_ok=True)
TIGER.mkdir(parents=True, exist_ok=True)

API = "https://api.census.gov/data/2023/acs/acs5"
VARS = ["NAME", "B03001_001E", "B03001_004E", "B19013_001E", "B01003_001E"]
GEO = "metropolitan statistical area/micropolitan statistical area:*"
TIGER_URL = ("https://www2.census.gov/geo/tiger/GENZ2023/shp/"
             "cb_2023_us_cbsa_500k.zip")


def fetch_acs() -> pd.DataFrame:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("CENSUS_API_KEY not in environment; source config.local.env")
    params = {"get": ",".join(VARS), "for": GEO, "key": key}
    r = requests.get(API, params=params, timeout=180)
    r.raise_for_status()
    body = r.text
    if not body.lstrip().startswith("["):
        sys.exit(f"FAIL non-JSON body, first 200 chars: {body[:200]!r}")
    rows = r.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    missing = [v for v in VARS if v not in df.columns]
    if missing:
        sys.exit(f"FAIL missing columns {missing}")
    if len(df) < 900:
        sys.exit(f"FAIL only {len(df)} CBSA rows, expected ~939 (truncated body)")
    num = ["B03001_001E", "B03001_004E", "B19013_001E", "B01003_001E"]
    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.rename(columns={
        "metropolitan statistical area/micropolitan statistical area": "cbsa",
        "B03001_001E": "pop_b03001", "B03001_004E": "mexican_origin",
        "B19013_001E": "median_hh_income", "B01003_001E": "pop_total"})
    mex_total = df["mexican_origin"].sum()
    print(f"CBSA rows={len(df)} mexican-origin in CBSAs={mex_total:,.0f}",
          flush=True)
    # published ACS 2019-2023 5-yr national Mexican-origin ~37.2-37.6 million;
    # CBSA coverage omits non-metro/non-micro residents so allow 88-102%.
    if not (0.88 * 37.4e6 < mex_total < 1.02 * 37.4e6):
        sys.exit(f"FAIL Mexican-origin CBSA total {mex_total:,.0f} implausible")
    return df


def fetch_tiger() -> Path:
    dest = TIGER / "cb_2023_us_cbsa_500k.zip"
    if dest.exists():
        with zipfile.ZipFile(dest) as z:
            names = z.namelist()
        if any(n.endswith(".shp") for n in names):
            print(f"tiger cached ({len(names)} members)", flush=True)
            return dest
    r = requests.get(TIGER_URL, timeout=600)
    r.raise_for_status()
    buf = io.BytesIO(r.content)
    with zipfile.ZipFile(buf) as z:  # content validation: it must be a real zip
        names = z.namelist()
        if not any(n.endswith(".shp") for n in names):
            sys.exit(f"FAIL tiger zip has no .shp: {names}")
    dest.write_bytes(r.content)
    print(f"tiger downloaded {len(r.content):,} bytes, members={names}",
          flush=True)
    return dest


def main() -> None:
    df = fetch_acs()
    df = df[["cbsa", "NAME", "pop_total", "pop_b03001", "mexican_origin",
             "median_hh_income"]].sort_values("cbsa")
    df["mexican_share"] = df["mexican_origin"] / df["pop_b03001"]
    df.to_csv(DER / "cbsa_covariates.csv", index=False)
    fetch_tiger()
    print(f"wrote {DER / 'cbsa_covariates.csv'} rows={len(df)}", flush=True)


if __name__ == "__main__":
    main()

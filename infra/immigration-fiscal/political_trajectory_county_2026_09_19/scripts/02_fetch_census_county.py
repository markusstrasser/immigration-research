#!/usr/bin/env python3
"""Arm 1 step 2: county composition from the Census API.

Pulls, for every county in the 50 states + DC:
  ACS 5-year (2009, 2014, 2018, 2022, 2023)
    B03001_001E total, B03001_004E Mexican origin
    B03002_001/003/012E  total, white alone non-Hispanic, Hispanic
    B05003_008/009/011/019/020/022E   VAP and citizen VAP (all persons)
    B05003I_ same cells                VAP and citizen VAP (Hispanic)
    B19013_001E median household income
  Decennial 2000 SF1 and 2010 SF1
    P001001 total, Hispanic total, PCT011004 Mexican origin

Each ACS 5-year release is matched to the election year at its midpoint:
  2009 (2005-09) -> 2008,  2014 (2010-14) -> 2012,  2018 (2014-18) -> 2016,
  2022 (2018-22) -> 2020,  2023 (2019-23) -> 2024 (midpoint 2021: the latest
  5-year release; the lag is stated as a limit, not hidden).
2000 uses the decennial; 2004 is linearly interpolated between the two decennials.

Validation is by content: >=3,000 county rows per pull, every requested column
present, and the national Mexican-origin total inside a published band for the year.

Output (gitignored, rebuildable): _cache/census_county_<key>.csv
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"

ACS_YEARS = [2009, 2014, 2018, 2022, 2023]
ACS_VARS = (["B03001_001E", "B03001_004E",
             "B03002_001E", "B03002_003E", "B03002_012E"]
            + [f"B05003_{i:03d}E" for i in (8, 9, 11, 19, 20, 22)]
            + [f"B05003I_{i:03d}E" for i in (8, 9, 11, 19, 20, 22)]
            + ["B19013_001E"])
# national Mexican-origin population bands (millions) for the content check
# [TRAINING-DATA: Census/Pew published Mexican-origin totals; a +/-band only]
MEX_BAND = {2009: (28.0, 33.0), 2014: (32.0, 36.5), 2018: (34.0, 38.5),
            2022: (35.0, 39.5), 2023: (35.0, 40.0),
            2000: (19.5, 22.5), 2010: (30.0, 33.5)}


def key() -> str:
    k = os.environ.get("CENSUS_API_KEY")
    if not k:
        sys.exit("CENSUS_API_KEY not in environment; source config.local.env")
    return k


def available(url: str, variables: list[str], k: str) -> list[str]:
    """Census returns a bare HTTP 400 when ANY requested variable is absent from a
    vintage (B05003I is missing from ACS 5-year 2009, for one). Probe one variable
    at a time and report what is dropped rather than guessing."""
    keep, drop = [], []
    for v in variables:
        try:
            r = requests.get(url, params={"get": v, "for": "county:*", "key": k},
                             timeout=180)
            r.raise_for_status()
            keep.append(v)
        except requests.HTTPError:
            drop.append(v)
        except requests.RequestException as e:
            sys.exit(f"FAIL {type(e).__name__} probing variables")
    if drop:
        print(f"    dropped (absent from this vintage): {drop}", flush=True)
    return keep


def fetch(url: str, variables: list[str], k: str) -> pd.DataFrame:
    """One call per 45 variables, joined on the geography columns."""
    out = None
    for i in range(0, len(variables), 45):
        chunk = variables[i:i + 45]
        for attempt in (1, 2, 3):
            try:
                r = requests.get(url, params={"get": ",".join(chunk),
                                              "for": "county:*", "key": k},
                                 timeout=300)
                r.raise_for_status()
                break
            except requests.HTTPError as e:
                code = e.response.status_code if e.response is not None else "?"
                print(f"    HTTP {code} (attempt {attempt})", flush=True)
                if code == 400 and attempt == 1:
                    chunk = available(url, chunk, k)
                    if not chunk:
                        sys.exit("FAIL no requested variable exists in this vintage")
                    continue
                if attempt == 3:
                    sys.exit(f"FAIL HTTP {code} after 3 attempts")
                time.sleep(5 * attempt)
            except requests.RequestException as e:
                print(f"    {type(e).__name__} (attempt {attempt})", flush=True)
                if attempt == 3:
                    sys.exit(f"FAIL {type(e).__name__} after 3 attempts")
                time.sleep(5 * attempt)
        body = r.text
        if not body.lstrip().startswith("["):
            sys.exit(f"FAIL non-JSON body (first 120 chars) {body[:120]!r}")
        rows = r.json()
        df = pd.DataFrame(rows[1:], columns=rows[0])
        missing = [v for v in chunk if v not in df.columns]
        if missing:
            sys.exit(f"FAIL missing columns {missing}")
        print(f"    got {len(chunk)} vars x {len(df)} counties", flush=True)
        if len(df) < 3000:
            sys.exit(f"FAIL only {len(df)} county rows (truncated body?)")
        out = df if out is None else out.merge(df, on=["state", "county"],
                                               how="inner", validate="one_to_one")
    assert out is not None
    out["fips"] = out["state"].str.zfill(2) + out["county"].str.zfill(3)
    for c in out.columns:
        if c[0] == "B" or c[0] == "P":
            out[c] = pd.to_numeric(out[c], errors="coerce")
            out.loc[out[c] < -1e8, c] = pd.NA   # Census jam values
    return out


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    k = key()
    for y in ACS_YEARS:
        dest = CACHE / f"census_county_acs5_{y}.csv"
        if dest.exists():
            df = pd.read_csv(dest, dtype={"fips": str})
        else:
            print(f"ACS 5-year {y}", flush=True)
            df = fetch(f"https://api.census.gov/data/{y}/acs/acs5", ACS_VARS, k)
            df.to_csv(dest, index=False)
        mex = df["B03001_004E"].sum() / 1e6
        lo, hi = MEX_BAND[y]
        ok = lo <= mex <= hi
        print(f"  {y}: {len(df)} counties, Mexican-origin {mex:.1f}M "
              f"(band {lo}-{hi}) {'OK' if ok else 'FAIL'}", flush=True)
        if not ok:
            sys.exit(f"FAIL {y} Mexican-origin national total {mex:.2f}M off band")

    dec = {2000: ("https://api.census.gov/data/2000/dec/sf1",
                  ["P001001", "P004002", "PCT011004"]),
           2010: ("https://api.census.gov/data/2010/dec/sf1",
                  ["P001001", "P004003", "PCT011004"])}
    for y, (url, vars_) in dec.items():
        dest = CACHE / f"census_county_dec_{y}.csv"
        if dest.exists():
            df = pd.read_csv(dest, dtype={"fips": str})
        else:
            print(f"Decennial SF1 {y}", flush=True)
            df = fetch(url, vars_, k)
            df.to_csv(dest, index=False)
        mex = df["PCT011004"].sum() / 1e6
        lo, hi = MEX_BAND[y]
        ok = lo <= mex <= hi
        print(f"  {y}: {len(df)} counties, Mexican-origin {mex:.1f}M "
              f"(band {lo}-{hi}) {'OK' if ok else 'FAIL'}", flush=True)
        if not ok:
            sys.exit(f"FAIL decennial {y} Mexican-origin total {mex:.2f}M off band")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

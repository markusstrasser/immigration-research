#!/usr/bin/env python3
"""Arm B/C helper: Census 2010 surname file (surnames with >=100 bearers and
their race/ethnicity percentages). Used to impute Hispanic origin for award
winners where self-identification is not documented.

Source: https://www2.census.gov/topics/genealogy/2010surnames/names.zip
Output: _cache/surnames/Names_2010Census.csv  (raw, ~7 MB)
        derived/surname_hispanic_lookup.csv   (name, pcthispanic, count)
Validation by content: >=150,000 surnames, SMITH present with pcthispanic ~1,
GARCIA present with pcthispanic >90.
"""
import gzip
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "surnames"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)
DER.mkdir(exist_ok=True)
# www2.census.gov answers this path with an HTML "Request Rejected" page under
# HTTP 200 for scripted clients (checked 2026-09-19, browser UA and referer both
# rejected), so the Wayback capture of the same Census file is the working
# route; the body arrives gzip-wrapped. Content is validated below either way.
URL = "https://www2.census.gov/topics/genealogy/2010surnames/names.zip"
URL_WB = ("https://web.archive.org/web/2023id_/"
          "https://www2.census.gov/topics/genealogy/2010surnames/names.zip")
UA = {"User-Agent": "immigration-research-lane/1.0 (cultural-output arm B)"}
RAW = CACHE / "Names_2010Census.csv"


def main() -> None:
    if not RAW.exists():
        blob = None
        for url in (URL, URL_WB):
            try:
                r = requests.get(url, headers=UA, timeout=1800)
                r.raise_for_status()
            except Exception as exc:  # noqa: BLE001
                print(f"  {url} failed: {exc!r}", flush=True)
                continue
            body = r.content
            if body[:2] == b"\x1f\x8b":          # gzip-wrapped (Wayback)
                body = gzip.decompress(body)
            if body[:2] != b"PK":
                print(f"  {url} returned a non-zip body "
                      f"({body[:60]!r}) - rejected", flush=True)
                continue
            blob = body
            print(f"  got zip from {url}", flush=True)
            break
        if blob is None:
            sys.exit("FAIL could not obtain the Census 2010 surname zip")
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            member = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if not member:
                sys.exit(f"FAIL no csv in names.zip: {z.namelist()}")
            RAW.write_bytes(z.read(member[0]))
        print(f"downloaded {RAW.name} {RAW.stat().st_size:,} bytes", flush=True)
    df = pd.read_csv(RAW, dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    need = {"name", "count", "pcthispanic"}
    if not need <= set(df.columns):
        sys.exit(f"FAIL columns {df.columns.tolist()}")
    df = df[df["name"].str.upper() != "ALL OTHER NAMES"].copy()
    df["count"] = pd.to_numeric(df["count"], errors="coerce")
    df["pcthispanic"] = pd.to_numeric(df["pcthispanic"].replace("(S)", None),
                                      errors="coerce")
    if len(df) < 150_000:
        sys.exit(f"FAIL only {len(df):,} surnames")
    smith = df.loc[df["name"] == "SMITH", "pcthispanic"]
    garcia = df.loc[df["name"] == "GARCIA", "pcthispanic"]
    if smith.empty or garcia.empty:
        sys.exit("FAIL SMITH or GARCIA missing")
    if not (smith.iloc[0] < 5 and garcia.iloc[0] > 90):
        sys.exit(f"FAIL sanity: SMITH={smith.iloc[0]} GARCIA={garcia.iloc[0]}")
    out = df[["name", "count", "pcthispanic"]].sort_values("name")
    out.to_csv(DER / "surname_hispanic_lookup.csv", index=False)
    print(f"surnames={len(out):,} SMITH={smith.iloc[0]} "
          f"GARCIA={garcia.iloc[0]}", flush=True)


if __name__ == "__main__":
    main()

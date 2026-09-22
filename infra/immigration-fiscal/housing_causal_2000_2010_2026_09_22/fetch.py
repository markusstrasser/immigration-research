"""County housing endpoints for the 2000-2010 rent and value long difference.

2000: Census SF3 (api.census.gov/data/2000/dec/sf3), 1999 dollars
  H063001 median gross rent, H085001 median value (owner-occupied),
  H007002 owner-occupied units, H007003 renter-occupied units, H001001 housing units
2010: ACS 2006-2010 five-year (api.census.gov/data/2010/acs/acs5), 2010 dollars
  B25064_001E median gross rent, B25077_001E median value,
  B25003_002E owner-occupied, B25003_003E renter-occupied, B01003_001E population

SF3 carries no aggregate-dollar rent or value table at county level (H062/H084 are unit
counts), so both endpoints use medians and the CBSA index is a tenure-weighted mean of
county medians, built the same way in both years.

Output: _cache/{sf3,acs5}_<state>.json and derived/county_housing_2000_2010.csv.
Needs CENSUS_API_KEY in the environment (acquire/config.local.env). The key is never
printed; error text is redacted.

Run from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/fetch.py
"""
import json
import os
import pathlib
import time
import urllib.request

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
KEY = os.environ.get("CENSUS_API_KEY", "")
STATES = [f"{s:02d}" for s in
          [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
           27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48,
           49, 50, 51, 53, 54, 55, 56]]
SF3 = ("https://api.census.gov/data/2000/dec/sf3",
       ["H063001", "H085001", "H007002", "H007003", "H001001"])
ACS = ("https://api.census.gov/data/2010/acs/acs5",
       ["B25064_001E", "B25077_001E", "B25003_002E", "B25003_003E", "B01003_001E"])


def redact(text):
    return text.replace(KEY, "REDACTED") if KEY else text


def pull(tag, base, cols, state):
    p = CACHE / f"{tag}_{state}.json"
    if p.exists():
        return json.loads(p.read_text())
    url = f"{base}?get=NAME,{','.join(cols)}&for=county:*&in=state:{state}&key={KEY}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                rows = json.loads(r.read().decode())
            p.write_text(json.dumps(rows))
            return rows
        except Exception as e:  # noqa: BLE001
            print(f"  ! {tag} {state} attempt {attempt + 1}: {redact(str(e))[:120]}")
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"[BLOCKED] {tag} {state} failed after 4 attempts")


def frame(tag, base, cols):
    out = []
    for i, st in enumerate(STATES, 1):
        rows = pull(tag, base, cols, st)
        head, body = rows[0], rows[1:]
        df = pd.DataFrame(body, columns=head)
        out.append(df)
        if i % 10 == 0:
            print(f"  [{i}/{len(STATES)}] {tag}")
    df = pd.concat(out, ignore_index=True)
    df["county_fips"] = df["state"] + df["county"]
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[["county_fips", "NAME"] + cols]


def main():
    if not KEY:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    a = frame("sf3", *SF3).rename(columns={
        "H063001": "rent_med_2000", "H085001": "value_med_2000", "H007002": "owners_2000",
        "H007003": "renters_2000", "H001001": "units_2000", "NAME": "name_2000"})
    b = frame("acs5", *ACS).rename(columns={
        "B25064_001E": "rent_med_2010", "B25077_001E": "value_med_2010",
        "B25003_002E": "owners_2010", "B25003_003E": "renters_2010",
        "B01003_001E": "pop_2010", "NAME": "name_2010"})
    # ACS uses negative sentinels for suppressed medians
    for c in ("rent_med_2010", "value_med_2010"):
        b.loc[b[c] < 0, c] = float("nan")
    m = a.merge(b, on="county_fips", how="outer", indicator=True)
    print("  counties: 2000", len(a), "2010", len(b), "both", int((m._merge == "both").sum()))
    m.drop(columns="_merge").to_csv(DERIVED / "county_housing_2000_2010.csv", index=False)
    print("  ✓ wrote derived/county_housing_2000_2010.csv", m.shape)


if __name__ == "__main__":
    main()

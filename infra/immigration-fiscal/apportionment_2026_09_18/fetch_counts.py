"""Fetch state-level population counts used by the apportionment counterfactuals.

Outputs derived/state_counts.csv with one row per state (50 states, no DC).
Caches every raw API response under _cache/.
"""
import json
import os
import time
from pathlib import Path
import urllib.request
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
CACHE.mkdir(exist_ok=True)
DERIVED.mkdir(exist_ok=True)
KEY = os.environ["CENSUS_API_KEY"]

EXCLUDE_FIPS = {"11", "72"}  # DC (not apportioned) and Puerto Rico


def get(url: str, cache_name: str):
    p = CACHE / cache_name
    if not p.exists():
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=120) as r:
                    p.write_bytes(r.read())
                break
            except Exception as e:  # noqa: BLE001
                print(f"  retry {attempt}: {e}", flush=True)
                time.sleep(3 * (attempt + 1))
        else:
            raise RuntimeError(f"failed: {cache_name}")
    return json.loads(p.read_text())


def to_df(rows, value_cols):
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df[~df["state"].isin(EXCLUDE_FIPS)]
    for c in value_cols:
        df[c] = pd.to_numeric(df[c])
    return df[["NAME", "state"] + value_cols]


series = {}

print("2020 DDHC-A Mexican (POPGROUP 4015)", flush=True)
r = get(f"https://api.census.gov/data/2020/dec/ddhca?get=NAME,T01001_001N&POPGROUP=4015&for=state:*&key={KEY}",
        "ddhca_2020_mexican_states.json")
d = to_df(r, ["T01001_001N"]).rename(columns={"T01001_001N": "mex_origin_2020_dec"})
series["mex_origin_2020_dec"] = d

# NOTE: DDHC-A publishes no state-level "Total population" group (POPGROUP=001 -> HTTP 204);
# official decennial totals come from the apportionment tables instead.

print("2010 SF1 PCT11 (Mexican, total, Hispanic)", flush=True)
r = get(f"https://api.census.gov/data/2010/dec/sf1?get=NAME,PCT011001,PCT011003,PCT011004&for=state:*&key={KEY}",
        "sf1_2010_pct11_states.json")
d = to_df(r, ["PCT011001", "PCT011003", "PCT011004"]).rename(columns={
    "PCT011001": "total_2010_dec", "PCT011003": "hisp_2010_dec", "PCT011004": "mex_origin_2010_dec"})
series["sf1_2010"] = d

print("ACS 2020 5-year: B05006 Mexico-born, B03001 Mexican origin, B01003 total", flush=True)
r = get(f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B05006_150E,B03001_004E,B03001_001E,B01003_001E&for=state:*&key={KEY}",
        "acs5_2020_states.json")
d = to_df(r, ["B05006_150E", "B03001_004E", "B03001_001E", "B01003_001E"]).rename(columns={
    "B05006_150E": "mex_born_acs2020", "B03001_004E": "mex_origin_acs2020",
    "B03001_001E": "total_acs2020_b03001", "B01003_001E": "total_acs2020"})
series["acs2020"] = d

print("ACS 2010 5-year: B05006 Mexico-born, B03001 Mexican origin, B01003 total", flush=True)
r = get(f"https://api.census.gov/data/2010/acs/acs5?get=NAME,B05006_138E,B03001_004E,B01003_001E&for=state:*&key={KEY}",
        "acs5_2010_states.json")
d = to_df(r, ["B05006_138E", "B03001_004E", "B01003_001E"]).rename(columns={
    "B05006_138E": "mex_born_acs2010", "B03001_004E": "mex_origin_acs2010",
    "B01003_001E": "total_acs2010"})
series["acs2010"] = d

print("ACS 5-year: B05002_013E total foreign-born (2020 and 2010)", flush=True)
for yr, col in ((2020, "fb_acs2020"), (2010, "fb_acs2010")):
    r = get(f"https://api.census.gov/data/{yr}/acs/acs5?get=NAME,B05002_013E&for=state:*&key={KEY}",
            f"acs5_{yr}_foreignborn_states.json")
    series[col] = to_df(r, ["B05002_013E"]).rename(columns={"B05002_013E": col})

# DDHC-A publishes each population group at the most detailed table its size supports:
# large state x Mexican cells appear in T02003 (23 age categories), the smallest in T02002 (9).
print("2020 DDHC-A Mexican under 18 (T02003 with T02002 fallback, POPGROUP 4015)", flush=True)
U18_A = ["T02003_003N", "T02003_004N", "T02003_005N", "T02003_006N",
         "T02003_027N", "T02003_028N", "T02003_029N", "T02003_030N"]
U18_B = ["T02002_003N", "T02002_004N", "T02002_013N", "T02002_014N"]
r = get(f"https://api.census.gov/data/2020/dec/ddhca?get=NAME,{','.join(U18_A)}&POPGROUP=4015&for=state:*&key={KEY}",
        "ddhca_2020_mexican_age23_states.json")
a = to_df(r, U18_A)
a["mex_origin_u18_2020_dec"] = a[U18_A].sum(axis=1)
a = a.drop(columns=U18_A)
r = get(f"https://api.census.gov/data/2020/dec/ddhca?get=NAME,{','.join(U18_B)}&POPGROUP=4015&for=state:*&key={KEY}",
        "ddhca_2020_mexican_age9_states.json")
b = to_df(r, U18_B)
b["mex_origin_u18_2020_dec"] = b[U18_B].sum(axis=1)
b = b.drop(columns=U18_B)
u18 = pd.concat([a, b[~b["state"].isin(set(a["state"]))]], ignore_index=True)
print(f"  under-18 coverage: T02003 {len(a)} states + T02002 fallback {len(u18) - len(a)}", flush=True)
series["mex_u18"] = u18

out = None
for name, d in series.items():
    d = d.drop(columns=["NAME"]) if out is not None else d
    out = d if out is None else out.merge(d, on="state", how="outer")
out = out.sort_values("NAME").reset_index(drop=True)
out.to_csv(DERIVED / "state_counts.csv", index=False)
print(out.head(8).to_string())
print(f"rows={len(out)}")
print("2020 dec Mexican-origin US total:", f"{out['mex_origin_2020_dec'].sum():,}")
print("2010 dec Mexican-origin US total:", f"{out['mex_origin_2010_dec'].sum():,}")
print("ACS2020 Mexican-origin US total:", f"{out['mex_origin_acs2020'].sum():,}")
print("ACS2020 Mexico-born US total:", f"{out['mex_born_acs2020'].sum():,}")
print("ACS2020 foreign-born US total:", f"{out['fb_acs2020'].sum():,}")

"""ACS denominators for the NIBRS offending rates: population by Hispanic origin and race, all
ages and aged 12+, for every place and county in Texas, Arizona and California, plus the Mexican
share of Hispanic residents (B03001).

    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    uv run --no-project python3 acs_denominators.py

ACS 5-year 2018-2022 serves NIBRS 2022 and 2019-2023 serves NIBRS 2023 (every place and county
is published; 1-year tables stop at 65,000 residents). ACS 1-year 2022 and 2023 give the
state-level B03001 check the brief asks for.

Groups are disjoint, Hispanic of any race first:
    hisp = B01001I (Hispanic or Latino)          nhw = B01001H (White alone, not Hispanic)
    nhb  = B01001B (Black alone) x B03002_004 / (B03002_004 + B03002_014)   (non-Hispanic share)
    nho  = total - hisp - nhw - nhb               (Asian, AIAN, NHPI, other, two or more races)
Aged 12+ removes under-5, 5-9 and two fifths of 10-14 (ages 10 and 11), sex by sex; aged 18+
removes every band through 15-17 (the adult denominator for the arrest check).
The key comes from CENSUS_API_KEY and is never printed; failing URLs are redacted.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/acs"
OUT = HERE / "derived"
STATES = {"48": "TX", "04": "AZ", "06": "CA"}
# under 5, 5-9, 10-14, 15-17, male then female
AGE = {"B01001": ["003", "004", "005", "006", "027", "028", "029", "030"]}
for t in ["B01001H", "B01001I", "B01001B"]:
    AGE[t] = ["003", "004", "005", "006", "018", "019", "020", "021"]
VARS = (["B03002_001E", "B03002_003E", "B03002_004E", "B03002_012E", "B03002_014E",
         "B03001_003E", "B03001_004E"]
        + [f"{t}_{v}E" for t, vs in AGE.items() for v in ["001"] + vs])


def get(url: str, key: str, out: Path) -> list:
    if out.exists() and out.stat().st_size > 100:
        return json.loads(out.read_text())
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(f"{url}&key={key}", timeout=180).read()
            data = json.loads(body)
            out.write_bytes(body)
            return data
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            msg = re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", str(e)).replace(key, "<KEY>")
            print(f"[retry] {out.name} attempt {attempt + 1}: {msg}", flush=True)
            time.sleep(5 * (attempt + 1))
    raise SystemExit(f"[BLOCKED] ACS pull failed: {out.name}")


def groups(df: pd.DataFrame) -> pd.DataFrame:
    for c in VARS:
        df[c] = pd.to_numeric(df[c])

    def under12(t: str) -> pd.Series:
        a, b, c, _, d, e, f, _ = (df[f"{t}_{v}E"] for v in AGE[t])
        return a + b + 0.4 * c + d + e + 0.4 * f

    def under18(t: str) -> pd.Series:
        return sum(df[f"{t}_{v}E"] for v in AGE[t])

    nh_black_share = (df.B03002_004E / (df.B03002_004E + df.B03002_014E)).fillna(1.0)
    out = pd.DataFrame({
        "total": df.B01001_001E, "hisp": df.B01001I_001E, "nhw": df.B01001H_001E,
        "nhb": df.B01001B_001E * nh_black_share,
        "total_12": df.B01001_001E - under12("B01001"), "hisp_12": df.B01001I_001E - under12("B01001I"),
        "nhw_12": df.B01001H_001E - under12("B01001H"),
        "nhb_12": (df.B01001B_001E - under12("B01001B")) * nh_black_share,
        "total_18": df.B01001_001E - under18("B01001"), "hisp_18": df.B01001I_001E - under18("B01001I"),
        "nhw_18": df.B01001H_001E - under18("B01001H"),
        "nhb_18": (df.B01001B_001E - under18("B01001B")) * nh_black_share,
        "mexican": df.B03001_004E, "hisp_b03001": df.B03001_003E})
    for sfx in ["", "_12", "_18"]:
        out[f"nho{sfx}"] = out[f"total{sfx}"] - out[f"hisp{sfx}"] - out[f"nhw{sfx}"] - out[f"nhb{sfx}"]
    bad = (df.B03002_012E != df.B01001I_001E) | (df.B03002_003E != df.B01001H_001E) | (df.B03002_001E != df.B01001_001E)
    if bad.any():
        raise SystemExit(f"[BLOCKED] B03002 and B01001 totals disagree in {int(bad.sum())} rows")
    return out


def main() -> None:
    key = os.environ.get("CENSUS_API_KEY", "")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    frames = []
    for vintage in (2022, 2023):
        for fips, st in STATES.items():
            for geo in ("place", "county"):
                url = (f"https://api.census.gov/data/{vintage}/acs/acs5?get=NAME,{','.join(VARS)}"
                       f"&for={geo}:*&in=state:{fips}")
                data = get(url, key, CACHE / f"acs5_{vintage}_{st}_{geo}.json")
                df = pd.DataFrame(data[1:], columns=data[0])
                g = groups(df)
                g.insert(0, "name", df.NAME)
                g.insert(0, "geoid", df[geo])
                g.insert(0, "geo", geo)
                g.insert(0, "state", st)
                g.insert(0, "acs_year", vintage)
                frames.append(g)
    geo = pd.concat(frames, ignore_index=True)
    geo.to_csv(OUT / "acs5_place_county_groups.csv", index=False, float_format="%.1f")
    rows = []
    for vintage in (2022, 2023):
        for fips, st in STATES.items():
            url = (f"https://api.census.gov/data/{vintage}/acs/acs1?get=NAME,B03001_001E,B03001_003E,"
                   f"B03001_004E&for=state:{fips}")
            d = get(url, key, CACHE / f"acs1_{vintage}_{st}_b03001.json")
            tot, h, m = (float(x) for x in d[1][1:4])
            rows.append(dict(acs_year=vintage, state=st, total=tot, hispanic=h, mexican=m,
                             mexican_share_of_hispanic=m / h, hispanic_share=h / tot))
    b = pd.DataFrame(rows)
    b.to_csv(OUT / "acs1_state_b03001.csv", index=False, float_format="%.4f")
    print(b.to_string(index=False))
    c = geo[geo.geo.eq("county")].groupby(["acs_year", "state"])[["total", "hisp", "nhw", "nhb", "nho",
                                                                  "total_12", "hisp_12", "mexican"]].sum()
    c["mex_share_of_hisp"] = c.mexican / c.hisp
    print(c.to_string(float_format=lambda x: f"{x:,.3f}" if x < 10 else f"{x:,.0f}"))


if __name__ == "__main__":
    main()

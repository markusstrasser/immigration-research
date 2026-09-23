"""Share of Mexican-origin people among the Hispanic neighbours of Mexican-origin people.

A Mexican-origin offender's Hispanic victim is inside the target group only if that victim is
also of Mexican origin. NCVS and SHR record only Hispanic yes/no, so this lane bounds the
in-group share of Hispanic victims with a residential exposure index from ACS 2020-2024
5-year table B03001 (B03001_003E Hispanic or Latino, B03001_004E Mexican):

    m_geo = sum_g M_g * (M_g / H_g) / sum_g M_g        (g = tract or county)

m_geo is the Mexican share of the Hispanic population around the average Mexican-origin
resident. Co-ethnic sorting within tracts and within social networks makes the true in-group
share of victims higher, so 1 - m_geo is an upper-leaning estimate of the non-Mexican share.
Needs CENSUS_API_KEY (infra/immigration-fiscal/acquire/config.local.env); the key is never
printed or written.
"""
from pathlib import Path
import json
import os
import time
import urllib.error
import urllib.request

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
BASE = "https://api.census.gov/data/2024/acs/acs5"
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
          "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46",
          "47", "48", "49", "50", "51", "53", "54", "55", "56"]


def fetch(state: str, key: str) -> list:
    out = CACHE / f"acs5_2024_b03001_tract_{state}.json"
    if out.exists() and out.stat().st_size > 100:
        return json.loads(out.read_text())
    url = f"{BASE}?get=NAME,B03001_001E,B03001_003E,B03001_004E&for=tract:*&in=state:{state}&key={key}"
    for attempt in range(4):
        try:
            body = urllib.request.urlopen(url, timeout=120).read()
            data = json.loads(body)
            out.write_bytes(body)
            return data
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            msg = str(e).replace(key, "<KEY>")
            print(f"[retry] state {state} attempt {attempt + 1}: {msg}")
            time.sleep(5 * (attempt + 1))
    raise SystemExit(f"[BLOCKED] ACS B03001 tract pull failed for state {state}")


def exposure(df: pd.DataFrame, by: list[str]) -> float:
    g = df.groupby(by)[["hisp", "mex"]].sum()
    g = g[g.hisp > 0]
    return float((g.mex * g.mex / g.hisp).sum() / g.mex.sum())


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    key = os.environ.get("CENSUS_API_KEY", "")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env")
    frames = []
    for s in STATES:
        data = fetch(s, key)
        frames.append(pd.DataFrame(data[1:], columns=data[0]))
    df = pd.concat(frames, ignore_index=True)
    for c in ["B03001_001E", "B03001_003E", "B03001_004E"]:
        df[c] = pd.to_numeric(df[c])
    df = df.rename(columns={"B03001_001E": "pop", "B03001_003E": "hisp", "B03001_004E": "mex"})
    if (df.mex > df.hisp).any() or (df.hisp > df["pop"]).any():
        raise SystemExit("[BLOCKED] B03001 nesting violated")
    rows = [
        dict(level="national", m=float(df.mex.sum() / df.hisp.sum()),
             units=1, pop=df["pop"].sum(), hisp=df.hisp.sum(), mex=df.mex.sum()),
        dict(level="state", m=exposure(df, ["state"]), units=df.state.nunique(),
             pop=df["pop"].sum(), hisp=df.hisp.sum(), mex=df.mex.sum()),
        dict(level="county", m=exposure(df, ["state", "county"]),
             units=df.groupby(["state", "county"]).ngroups,
             pop=df["pop"].sum(), hisp=df.hisp.sum(), mex=df.mex.sum()),
        dict(level="tract", m=exposure(df, ["state", "county", "tract"]), units=len(df),
             pop=df["pop"].sum(), hisp=df.hisp.sum(), mex=df.mex.sum()),
    ]
    out = pd.DataFrame(rows)
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived/mexican_share_of_hispanic_exposure.csv", index=False,
               float_format="%.6f")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

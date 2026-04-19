"""Pull ACS 1-yr state-level immigrant population share, 2005-2023.

Variables:
- B05002_001E: total population
- B05002_013E: foreign-born population
- B05002_001E - B05002_013E = native-born

Output: data/lehd/acs_state_immigrant_share.parquet
"""
from __future__ import annotations
import time
from pathlib import Path
import requests
import pandas as pd

OUT = Path(__file__).parent.parent / "data" / "lehd"
OUT.mkdir(parents=True, exist_ok=True)
PARQ = OUT / "acs_state_immigrant_share.parquet"

YEARS = list(range(2005, 2024))


def fetch_year(year: int) -> pd.DataFrame:
    url = f"https://api.census.gov/data/{year}/acs/acs1"
    if year == 2020:
        # 2020 ACS 1-yr was withdrawn; use experimental estimates if needed, else skip
        url = f"https://api.census.gov/data/{year}/acs/acs1?"
    params = {
        "get": "NAME,B05002_001E,B05002_013E",
        "for": "state:*",
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code != 200:
            print(f"  {year}: HTTP {r.status_code}")
            return pd.DataFrame()
        data = r.json()
    except Exception as e:
        print(f"  {year}: {e}")
        return pd.DataFrame()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["year"] = year
    df["totpop"] = pd.to_numeric(df["B05002_001E"], errors="coerce")
    df["fb_pop"] = pd.to_numeric(df["B05002_013E"], errors="coerce")
    df["fb_share"] = df["fb_pop"] / df["totpop"]
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    return df[["year", "state_fips", "NAME", "totpop", "fb_pop", "fb_share"]]


def main() -> int:
    rows = []
    for y in YEARS:
        df = fetch_year(y)
        rows.append(df)
        print(f"  {y}: {len(df)} rows, fb_share median={df['fb_share'].median():.3f}" if len(df) else f"  {y}: empty")
        time.sleep(0.3)
    out = pd.concat(rows, ignore_index=True)
    out.to_parquet(PARQ, index=False)
    print(f"\nWrote {PARQ}: {len(out)} rows, {out['year'].nunique()} years × {out['state_fips'].nunique()} states")
    print("\nSample (CA across years):")
    print(out[out["state_fips"]=="06"].sort_values("year")[["year", "fb_share"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    main()

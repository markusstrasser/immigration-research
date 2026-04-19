"""Merge Saiz 2010 housing supply elasticity with current ACS rent + foreign-born share.

Output: data/analysis/saiz_msa_rent_immigrant_2022.parquet

Tests the hypothesis: immigrant rent burden is concentrated in inelastic MSAs.
- B25064_001E: median gross rent ($)
- B05002_001E: total population
- B05002_013E: foreign-born population
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import requests
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
OUT = DATA / "analysis"
OUT.mkdir(parents=True, exist_ok=True)

ACS_URL = "https://api.census.gov/data/2022/acs/acs5"
SAIZ = DATA / "saiz" / "saiz_2010_msa_elasticity.dta"


def pull_acs() -> pd.DataFrame:
    params = {
        "get": "NAME,B25064_001E,B05002_001E,B05002_013E,B19013_001E",  # rent, totpop, fb, medhhinc
        "for": "metropolitan statistical area/micropolitan statistical area:*",
    }
    r = requests.get(ACS_URL, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns={
        "B25064_001E": "median_rent",
        "B05002_001E": "totpop",
        "B05002_013E": "fb_pop",
        "B19013_001E": "median_hh_income",
        "metropolitan statistical area/micropolitan statistical area": "cbsa",
    })
    for c in ("median_rent", "totpop", "fb_pop", "median_hh_income"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fb_share"] = df["fb_pop"] / df["totpop"]
    df["rent_to_income"] = df["median_rent"] * 12 / df["median_hh_income"]
    df["msaname_norm"] = df["NAME"].apply(_norm_msa)
    return df


def _norm_msa(name: str) -> str:
    """Normalize MSA name to first-city/first-state form for matching with Saiz.

    Saiz format: 'Abilene, TX (MSA)'  /  'Albany-Schenectady-Troy, NY (MSA)'
    ACS format:  'Abilene, TX Metro Area'  /  'Albany-Schenectady-Troy, NY Metro Area'
    Strategy: take the first city of the hyphen list + the first state of the slash list.
    """
    s = name
    # Strip suffixes
    for suf in (" Metro Area", " Micro Area", " (MSA)", " (PMSA)", " (NECMA)"):
        s = s.replace(suf, "")
    # ACS: "City1-City2-City3, ST1-ST2 Metro Area"
    if "," in s:
        cities, states = s.rsplit(",", 1)
        first_city = cities.split("-")[0].strip()
        first_state = states.strip().split("-")[0].strip()
        s = f"{first_city}, {first_state}"
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def load_saiz() -> pd.DataFrame:
    df = pd.read_stata(SAIZ)
    df["msaname_norm"] = df["msaname"].apply(_norm_msa)
    return df[["msaname", "msaname_norm", "msanecma", "population", "WRLURI", "unaval", "elasticity"]]


def main() -> int:
    print("Loading Saiz...")
    saiz = load_saiz()
    print(f"  {len(saiz)} MSAs in Saiz dataset")
    print("Pulling ACS 2022 5-yr...")
    acs = pull_acs()
    print(f"  {len(acs)} CBSAs in ACS")

    merged = saiz.merge(acs, on="msaname_norm", how="left", suffixes=("_saiz", "_acs"))
    matched = merged["NAME"].notna().sum()
    print(f"Matched {matched}/{len(saiz)} Saiz MSAs to ACS rows")

    out = OUT / "saiz_msa_rent_immigrant_2022.parquet"
    merged.to_parquet(out, index=False)
    print(f"Wrote {out}")

    print("\n=== Summary by elasticity quartile ===")
    matched_df = merged[merged["NAME"].notna()].copy()
    matched_df["elasticity_q"] = pd.qcut(matched_df["elasticity"], 4, labels=["Q1 inelastic", "Q2", "Q3", "Q4 elastic"])
    summary = matched_df.groupby("elasticity_q", observed=True).agg(
        n_msas=("NAME", "count"),
        median_rent=("median_rent", "median"),
        median_hh_income=("median_hh_income", "median"),
        rent_to_income=("rent_to_income", "median"),
        fb_share_pct=("fb_share", lambda x: x.median() * 100),
        median_elasticity=("elasticity", "median"),
    )
    print(summary.to_string())

    print("\n=== Top 10 inelastic MSAs (most welfare-sensitive to immigrant inflows) ===")
    least_elastic = matched_df.nsmallest(10, "elasticity")[["msaname", "elasticity", "median_rent", "fb_share", "rent_to_income"]]
    print(least_elastic.to_string(index=False))

    print("\n=== Top 10 elastic MSAs (housing absorbs inflow) ===")
    most_elastic = matched_df.nlargest(10, "elasticity")[["msaname", "elasticity", "median_rent", "fb_share", "rent_to_income"]]
    print(most_elastic.to_string(index=False))

    print("\n=== Where immigrants concentrate by elasticity ===")
    # Rank MSAs by foreign-born share, see which elasticity band dominates
    matched_df["fb_share_decile"] = pd.qcut(matched_df["fb_share"], 5, labels=["D1 lowest", "D2", "D3", "D4", "D5 highest"], duplicates="drop")
    fb_by_elas = matched_df.groupby("fb_share_decile", observed=True).agg(
        median_elasticity=("elasticity", "median"),
        median_rent=("median_rent", "median"),
        n_msas=("NAME", "count"),
    )
    print(fb_by_elas.to_string())

    return 0


if __name__ == "__main__":
    main()

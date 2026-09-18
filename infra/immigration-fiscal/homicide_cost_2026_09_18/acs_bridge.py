"""The only available bridge from SHR 'Hispanic' to the ledger's Mexican-origin group.

SHR carries no national origin.  ACS 2023 1-year PUMS gives the Mexican-origin share of
Hispanics in the household population and in institutional group quarters (the prisoner
proxy the ledger's institutional line already uses).  Writes derived/acs_mexican_bridge.csv.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)
CONF = HERE.parent / "acquire/config.local.env"

HISP = {"01": "not_hispanic", "02": "Mexican", "03": "Puerto Rican", "04": "Cuban",
        "05": "Dominican", "06": "Costa Rican", "07": "Guatemalan", "08": "Honduran",
        "09": "Nicaraguan", "10": "Panamanian", "11": "Salvadoran", "12": "Other Central American",
        "13": "Argentinean", "14": "Bolivian", "15": "Chilean", "16": "Colombian",
        "17": "Ecuadorian", "18": "Paraguayan", "19": "Peruvian", "20": "Uruguayan",
        "21": "Venezuelan", "22": "Other South American", "23": "Spaniard",
        "24": "All Other Spanish/Hispanic/Latino"}


def key() -> str:
    for line in CONF.read_text().splitlines():
        if "CENSUS_API_KEY" in line:
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("CENSUS_API_KEY not found")


def fetch_raw(tag: str, ages: str) -> str:
    path = CACHE / f"acs_bridge_{tag}.json"
    if not path.exists():
        url = ("https://api.census.gov/data/2023/acs/acs1/pums?tabulate=weight(PWGTP)"
               f"&row+HISP&col+TYPEHUGQ&AGEP={ages}&key={key()}")
        path.write_bytes(urllib.request.urlopen(url, timeout=180).read())
    return path.read_text()


def parse(raw) -> pd.DataFrame:
    head = raw[0]
    names = []
    for h in head:
        names.append(f"gq{h['TYPEHUGQ']}" if isinstance(h, dict) else h)
    df = pd.DataFrame(raw[1:], columns=names)
    for c in df.columns:
        if c.startswith("gq"):
            df[c] = pd.to_numeric(df[c])
    return df


def main() -> None:
    rows = []
    for tag, ages in [("18_34", "18:34"), ("18_64", "18:64"), ("all_ages", "0:99")]:
        df = parse(json.loads(fetch_raw(tag, ages)))
        df["origin"] = df.HISP.map(HISP)
        hisp = df[df.HISP.ne("01")]
        for label, col in [("housing_unit", "gq1"), ("institutional_gq", "gq2")]:
            tot = hisp[col].sum()
            mex = hisp.loc[hisp.HISP.eq("02"), col].sum()
            generic = hisp.loc[hisp.HISP.eq("24"), col].sum()
            rows.append(dict(ages=tag, universe=label, hispanic_total=float(tot),
                             mexican=float(mex), mexican_share=float(mex / tot),
                             generic_other_hispanic=float(generic),
                             generic_share=float(generic / tot)))
        # keep the full origin breakdown for the institutional cell
        if tag == "18_64":
            hisp[["HISP", "origin", "gq1", "gq2"]].to_csv(
                OUT / "acs_hispanic_origin_18_64.csv", index=False)
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "acs_mexican_bridge.csv", index=False)
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    main()

"""Slim ACS PUMS person extracts (held 1-year files) to parquet for the integrity audit.

Keeps identity, geography, weights, the category/outcome items the repo uses, and their
allocation flags. Blank cells stay null (PUMS 'b' = not in universe); nothing is recoded.
Usage: acs_extract.py YEAR [YEAR ...]  ->  _cache/acs_person_<YEAR>.parquet
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = Path.home() / "research-data/immigration-fiscal/data"
ZIPS = {
    2019: DATA / "external/acs_pums_2019_1yr/csv_pus.zip",
    2023: DATA / "census/acs_pums_2023_person.zip",
    2024: DATA / "external/acs_pums_2024_1yr/csv_pus.zip",
}
for y in (2013, 2014, 2015, 2016, 2017, 2018, 2021, 2022):
    ZIPS[y] = DATA / f"external/acs_pums_years/csv_pus_{y}.zip"

WANT = """SERIALNO SPORDER ST STATE PUMA ADJINC PWGTP AGEP SEX HISP RAC1P RAC2P RACWHT RACSOR RACNUM
NATIVITY POBP CIT YOEP SCHL SCH SCHG RELSHIPP RELP WAGP PERNP PINCP SSIP PAP ANC1P ANC2P LANX
ENG HICOV PUBCOV ESR MIL FHISP FPOBP FCITP FYOEP FSCHLP FSCHP FSCHGP FPERNP FWAGP FPINCP FRACP
FAGEP FSEXP FANCP FLANXP FSSIP FPAP FHICOVP FESRP FRELSHIPP FRELP FENGP""".split()


def extract(year: int) -> Path:
    out = HERE / "_cache" / f"acs_person_{year}.parquet"
    if out.exists():
        return out
    out.parent.mkdir(exist_ok=True)
    frames = []
    with zipfile.ZipFile(ZIPS[year]) as z:
        for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
            header = pd.read_csv(z.open(name), nrows=0).columns
            cols = [c for c in WANT if c in header]
            for chunk in pd.read_csv(z.open(name), usecols=cols, dtype={"SERIALNO": str},
                                     chunksize=1_000_000, low_memory=False):
                frames.append(chunk)
            print(year, name, "cols", len(cols), flush=True)
    df = pd.concat(frames, ignore_index=True)
    if "STATE" in df and "ST" not in df:
        df = df.rename(columns={"STATE": "ST"})
    df["YEAR"] = year
    tmp = out.with_suffix(".tmp")
    df.to_parquet(tmp, index=False)
    tmp.rename(out)
    print(year, "rows", len(df), flush=True)
    return out


if __name__ == "__main__":
    for y in sys.argv[1:]:
        extract(int(y))

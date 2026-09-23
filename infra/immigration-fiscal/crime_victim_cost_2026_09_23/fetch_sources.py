"""Fetch and pin the two primary sources this lane adds; everything else is reused locally.

1. McCollister, French & Fang (2010), Drug Alcohol Depend 108:98-109, PMC2835847, as the
   PMC OAI-PMH JATS record (the article HTML is served behind a bot check).
2. FBI, Crime in the United States 2019, Table 43C (arrests of adults 18+ by race and
   ethnicity), the spreadsheet itself; flattened to derived/fbi_2019_table43c_adult_arrests.csv
   so the model runs without an .xls reader.
Writes derived/source_manifest.csv with byte counts and sha256 of every cached file.
Run: uv run --no-project --with xlrd python3 .../fetch_sources.py
"""
from pathlib import Path
import hashlib
import subprocess

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
SOURCES = {
    "oai_PMC2835847.xml": "https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/?verb=GetRecord"
                          "&identifier=oai:pubmedcentral.nih.gov:2835847&metadataPrefix=pmc",
    "fbi_cius2019_table43c.xls": "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/"
                                 "tables/table-43/table-43c.xls/output.xls",
}


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        path = CACHE / name
        if not path.exists() or path.stat().st_size < 10_000:
            subprocess.run(["curl", "-sS", "-L", "--fail", "-A", UA, "-o", str(path), url], check=True)
    head = (CACHE / "oai_PMC2835847.xml").read_text(errors="replace")
    if "The Cost of Crime to Society" not in head or "Table 5" not in head:
        raise SystemExit("[BLOCKED] PMC record is not the McCollister article")
    x = pd.read_excel(CACHE / "fbi_cius2019_table43c.xls", header=None, engine="xlrd")
    if "Table 43C" not in str(x.iloc[0, 0]) or "10,831 agencies" not in str(x.iloc[3, 0]):
        raise SystemExit("[BLOCKED] FBI spreadsheet is not 2019 Table 43C")
    rows = x.iloc[7:37, [0, 1, 2, 13, 14, 15]].copy()
    rows.columns = ["offense", "race_total", "race_white", "ethnicity_total", "hispanic", "not_hispanic"]
    rows = rows[pd.to_numeric(rows.race_total, errors="coerce").notna()]
    (HERE / "derived").mkdir(exist_ok=True)
    rows.to_csv(HERE / "derived/fbi_2019_table43c_adult_arrests.csv", index=False)
    man = []
    for p in sorted(CACHE.iterdir()):
        man.append(dict(file=p.name, bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    pd.DataFrame(man).to_csv(HERE / "derived/source_manifest.csv", index=False)
    print(f"[ok] {len(rows)} Table 43C rows; manifest of {len(man)} cached files")


if __name__ == "__main__":
    main()

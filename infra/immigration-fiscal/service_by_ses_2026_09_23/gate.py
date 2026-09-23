"""Gate: the staged PUMS files reproduce published ACS totals for veterans and the armed forces.

Published one-year tables (api.census.gov, national): B21001_001E civilian population 18+,
B21001_002E civilian veterans 18+, B23025_006E armed forces (population 16+). PUMS counterparts:
persons 18+ not now on active duty (`MIL` != 1), of whom `MIL` = 2, and persons 17+ with `ESR`
4-5 (the PUMS extract starts at 17; 16-year-olds cannot serve). PUMS is a subsample of the full
ACS, so totals should agree within a fraction of a percent, not exactly. Reads CENSUS_API_KEY
from the environment and never prints it. Writes `derived/gate_published_totals.txt`.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
TABLES = "B21001_001E,B21001_002E,B23025_006E"
TOLERANCE = 0.01


def published(year):
    target = CACHE / f"acs1_{year}_veterans_us.json"
    if not target.exists():
        key = os.environ.get("CENSUS_API_KEY")
        if not key:
            raise SystemExit("[BLOCKED] CENSUS_API_KEY is not set")
        url = f"https://api.census.gov/data/{year}/acs/acs1?get={TABLES}&for=us:1&key={key}"
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                target.write_text(response.read().decode())
        except Exception as error:  # the message can carry the key: report the class only
            raise SystemExit(f"[BLOCKED] {year}: {type(error).__name__}")
    header, row = json.loads(target.read_text())
    return {name: float(value) for name, value in zip(header, row) if name in TABLES}


def main():
    con = duckdb.connect()
    lines, failed = [], False
    for year in (2022, 2023, 2024):
        pums = con.execute(f"""
            SELECT SUM(CASE WHEN AGEP >= 18 AND MIL <> 1 THEN PWGTP ELSE 0 END)::DOUBLE,
                   SUM(CASE WHEN AGEP >= 18 AND MIL = 2 THEN PWGTP ELSE 0 END)::DOUBLE,
                   SUM(CASE WHEN ESR IN (4, 5) THEN PWGTP ELSE 0 END)::DOUBLE
            FROM read_parquet('{CACHE / f"acs{year}_persons.parquet"}')""").fetchone()
        table = published(year)
        for label, code, value in (("civilian population 18+", "B21001_001E", pums[0]),
                                   ("civilian veterans 18+", "B21001_002E", pums[1]),
                                   ("armed forces", "B23025_006E", pums[2])):
            gap = value / table[code] - 1
            ok = abs(gap) <= TOLERANCE
            failed |= not ok
            lines.append(f"{year}  {label:24s} PUMS {value:>13,.0f}  published {table[code]:>13,.0f} ({code})  "
                         f"{gap:+.2%}  {'PASS' if ok else 'FAIL'}")
    text = "\n".join(lines) + f"\n\nTolerance {TOLERANCE:.0%}. {'FAIL' if failed else 'PASS'}\n"
    (DERIVED / "gate_published_totals.txt").write_text(text)
    print(text)
    leaked = [p.name for p in CACHE.glob("acs1_*_veterans_us.json") if "key=" in p.read_text()]
    assert not leaked, leaked
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

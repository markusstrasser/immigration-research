"""Convert the FHFA land price workbook (WP 19-01, Version 4.0, June 2024) to plain CSVs.

Reads _cache/fhfa/land-prices_2024_20_june.xlsx (untrusted download; run with python3 -I) and
writes one CSV per needed sheet under _cache/fhfa/csv/: tract, county and state pooled
cross-sections (2015 prices), county and state annual panels (nominal, 2012-2022), and the county
standardization parameters (bL = plattage elasticity of land value on lot size). Header rows are
checked against the expected labels so a changed layout stops the run.

    uv run --no-project python3 -I infra/immigration-fiscal/school_land_2026_10_24/fhfa_extract.py
"""
import csv
import sys
from pathlib import Path

import openpyxl

HERE = Path(sys.argv[0]).resolve().parent
SRC = HERE / "_cache" / "fhfa" / "land-prices_2024_20_june.xlsx"
OUT = HERE / "_cache" / "fhfa" / "csv"
LV = ["Land Value\n(1/4 Acre Lot, Standardized)", "Land Value\n(Per Acre, As-Is)", "Land Share of Property Value"]
SHEETS = {
    "Cross-Section Census Tracts": ("xs_tract", ["State", "County", "Census Tract"] + LV + ["Lot Size"]),
    "Cross-Section Counties ": ("xs_county", ["State", "County", "FIPS"] + LV + ["Lot Size"]),
    "Cross-Section States": ("xs_state", ["State Name", "State Abbreviation", "State FIPS"] + LV + ["Lot Size"]),
    "Panel Counties": ("panel_county", ["State", "County", "FIPS", "Year"] + LV),
    "Panel States": ("panel_state", ["State Name", "State Abbreviation", "State FIPS", "Year"] + LV),
    "Cross-Section Nation": ("xs_nation", LV + ["Lot Size"]),
    "Standardization Parameters": ("std_params", ["State", "County", "FIPS", "Lot Size"]),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(SRC, read_only=True)
    readme = " ".join(str(v) for r in wb["Readme"].iter_rows(values_only=True) for v in r if v)
    if "Version 4.0 (June, 2024)" not in readme:
        raise SystemExit("[BLOCKED] FHFA workbook is not Version 4.0 (June, 2024)")
    for sheet, (name, want) in SHEETS.items():
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = [h for h in rows[1]]
        idx = []
        for w in want:
            if w not in hdr:
                raise SystemExit(f"[BLOCKED] {sheet}: header {w!r} missing; got {hdr}")
            idx.append(hdr.index(w))
        clean = [w.replace("\n", " ") for w in want]
        with open(OUT / f"{name}.csv", "w", newline="") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(clean)
            n = 0
            for r in rows[2:]:
                if all(v is None for v in r):
                    continue
                wr.writerow(["" if r[i] is None else r[i] for i in idx])
                n += 1
        print(name, n)


if __name__ == "__main__":
    main()

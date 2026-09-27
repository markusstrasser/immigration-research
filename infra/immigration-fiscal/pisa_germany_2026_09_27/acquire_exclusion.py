"""Build derived/exclusion_coverage.csv from cached OECD PISA annex A2 StatLink workbooks.

Reads only files in _cache/ (no network). Deterministic: rows sorted by country, then cycle;
LF line endings. Run from the lane directory:

    uv run --no-project --with openpyxl --with xlrd python3 acquire_exclusion.py

Sources (all "PISA target populations and samples", same 15-column layout in every cycle):
  2012  _cache/statlink_888932937092.xls   sheet 'Table A2.1'
        https://doi.org/10.1787/888932937092 -> statlinks.oecdcode.org/982013041P1T011.xls
        (PISA 2012 Vol I revised ed., Annex A2, "Version 3 - Last updated: 13-Oct-2020")
  2015  _cache/statlink_888933433129.xlsx  sheet 'Table A2.1'
        https://doi.org/10.1787/888933433129 -> statlinks.oecdcode.org/982016061P1G117.XLSX
  2018  _cache/statlink_EDU-2019-4228-EN-T010.xlsx  sheet 'Table I.A2.1'
        https://statlinks.oecdcode.org/EDU-2019-4228-EN-T010.XLSX
  2022  _cache/statlink_hpg9nd.xlsx  sheet 'Table I.A2.1'
        https://stat.link/files/53f23881-en/hpg9nd.xlsx
Revised Coverage Index 3 series: _cache/statlink_hpg9nd.xlsx sheet 'Table I.A2.2'
  (PISA 2022 Vol I; CI3 for 2003-2022 with some earlier populations revised).
"""

import csv
import re
from pathlib import Path

import openpyxl
import xlrd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived" / "exclusion_coverage.csv"

A21 = {
    2012: ("statlink_888932937092.xls", "Table A2.1"),
    2015: ("statlink_888933433129.xlsx", "Table A2.1"),
    2018: ("statlink_EDU-2019-4228-EN-T010.xlsx", "Table I.A2.1"),
    2022: ("statlink_hpg9nd.xlsx", "Table I.A2.1"),
}
REV = ("statlink_hpg9nd.xlsx", "Table I.A2.2")
# Table I.A2.2 (2022 Vol I): column index of "Coverage index 3" per cycle (verified from header row 8).
REV_CI3_COL = {2022: 4, 2018: 8, 2015: 13, 2012: 18}

# Column indices in every A2.1 table (header row "(1)".."(15)").
COLS = {
    "pop15": 1,
    "enrolled_g7plus": 2,
    "desired_target": 3,
    "school_excl_n_weighted": 4,
    "school_excl_rate_pct": 6,
    "participants_n": 7,
    "participants_weighted": 8,
    "excluded_students_n": 9,
    "excluded_students_weighted": 10,
    "within_school_excl_rate_pct": 11,
    "overall_excl_rate_pct": 12,
    "ci1": 13,
    "ci2": 14,
    "ci3": 15,
}

RENAME = {
    "Turkey": "Türkiye",
    "FYROM": "North Macedonia",
    "Former Yugoslav Republic of Macedonia": "North Macedonia",
    "Slovak Rep.": "Slovak Republic",
    "Russian Federation": "Russia",
    "Hong Kong-China": "Hong Kong (China)",
    "Macao-China": "Macao (China)",
    "Vietnam": "Viet Nam",
}

EUROPE = {
    "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Norway",
    "Poland", "Portugal", "Romania", "Serbia", "Slovak Republic", "Slovenia", "Spain", "Sweden",
    "Switzerland", "Ukraine", "United Kingdom",
}


def clean_name(raw):
    s = str(raw).replace("\n", " ").strip()
    s = re.sub(r"[\d,*\s]+$", "", s).strip()  # trailing footnote markers, e.g. "Cyprus1,2"
    return RENAME.get(s, s)


def load_rows(fname, sheet):
    path = CACHE / fname
    if path.suffix == ".xls":
        ws = xlrd.open_workbook(str(path)).sheet_by_name(sheet)
        return [[ws.cell_value(r, c) if ws.cell_value(r, c) != "" else None
                 for c in range(ws.ncols)] for r in range(ws.nrows)]
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    return rows


def num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip())
    except ValueError:
        return None  # OECD codes 'm', 'a', 'c', 'Yes'


def fmt(x, nd):
    return "" if x is None else f"{x:.{nd}f}"


def country_rows(rows):
    """Yield (name, oecd_flag, row) for data rows between 'OECD' and the table notes."""
    section = None
    for row in rows:
        if not row or row[0] is None:
            continue
        head = str(row[0]).strip()
        if head == "OECD":
            section = "OECD"
            continue
        if head == "Partners":
            section = "Partner"
            continue
        if section is None or len(row) < 16 or num(row[1]) is None:
            continue
        yield clean_name(head), section, row


def main():
    rev = {}
    for name, _, row in country_rows(load_rows(*REV)):
        for cyc, col in REV_CI3_COL.items():
            rev[(name, cyc)] = num(row[col]) if col < len(row) else None

    out = []
    for cyc, (fname, sheet) in A21.items():
        for name, section, row in country_rows(load_rows(fname, sheet)):
            v = {k: num(row[c]) for k, c in COLS.items()}
            out.append([
                name, cyc, section, "1" if name in EUROPE else "0",
                fmt(v["pop15"], 0), fmt(v["enrolled_g7plus"], 0), fmt(v["desired_target"], 0),
                fmt(v["school_excl_rate_pct"], 3), fmt(v["within_school_excl_rate_pct"], 3),
                fmt(v["overall_excl_rate_pct"], 3),
                fmt(v["excluded_students_n"], 0), fmt(v["excluded_students_weighted"], 1),
                fmt(v["participants_n"], 0), fmt(v["participants_weighted"], 1),
                fmt(v["ci1"], 4), fmt(v["ci2"], 4), fmt(v["ci3"], 4),
                fmt(rev.get((name, cyc)), 4),
                f"_cache/{fname}#{sheet}",
            ])
    out.sort(key=lambda r: (r[0], r[1]))
    header = [
        "country", "cycle", "oecd_or_partner_in_cycle", "europe",
        "pop15", "enrolled_g7plus", "desired_target_pop",
        "school_excl_rate_pct", "within_school_excl_rate_pct", "overall_excl_rate_pct",
        "excluded_students_n", "excluded_students_weighted",
        "participants_n", "participants_weighted",
        "ci1", "ci2", "ci3", "ci3_revised_2022_table_I_A2_2", "source",
    ]
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(out)
    unmatched = sorted({(r[0], r[1]) for r in out if r[17] == ""})
    print(f"wrote {len(out)} rows to {OUT.relative_to(HERE)}")
    print("no revised CI3 match:", unmatched)


if __name__ == "__main__":
    main()

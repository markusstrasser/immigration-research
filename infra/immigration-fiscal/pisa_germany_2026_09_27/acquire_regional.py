"""Build the PISA adjudicated-region panel (natives' math/reading, immigrant share) from cached OECD StatLinks.

Reads only `_cache/` (no network). Writes `derived/regional_panel.csv`, sorted, LF line endings.
Run from the lane directory:  uv run --no-project --with openpyxl --with xlrd python3 acquire_regional.py

Sources (all OECD StatLink workbooks; see reads/regional_panel.md for quoted headers):
  2022  PISA 2022 Vol I annex B2, stat.link/files/53f23881-en/ax46rt.xlsx
        I.B2.36 shares (non-imm 1-2, imm 4-5, 2nd gen 7-8, 1st gen 10-11); I.B2.39 math / I.B2.40 reading
        (all 1-2, non-immigrant 3-4)
  2018  PISA 2018 Vol II annex B2, doi 10.1787/888934038780
        II.B2.74 (imm share 1-2, average reading 4-5, non-immigrant reading 7-8). No math by immigrant background,
        no first-generation share.
  2015  PISA 2015 Vol I annex B2, doi 10.1787/888933433235
        B2.I.71 shares (non-imm 1-2, imm 3-4, 2nd 5-6, 1st 7-8). No math or reading by immigrant background
        (B2.I.72 splits science only).
  2012  PISA 2012 Vol II annex B2, doi 10.1787/888932964965
        B2.II.9 (non-imm % 1-2, imm % 3-4, non-immigrant math 9-10). No reading, no first-generation share.
"""
import csv
import os

import openpyxl
import xlrd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "derived", "regional_panel.csv")

COLUMNS = ["country", "region", "cycle", "nat_math", "nat_math_se", "nat_read", "nat_read_se",
           "imm_share", "imm_share_se", "g1_share", "source"]

# Harmonize country labels across cycles.
COUNTRY_MAP = {"Russian Federation": "Russia"}

# Harmonize region labels across cycles (applied after stripping footnote asterisks and whitespace).
REGION_MAP = {
    ("Australia", "Australian capital territory"): "Australian Capital Territory",
    ("Australia", "Northern territory"): "Northern Territory",
    ("Belgium", "Flemish Community"): "Flemish community",
    ("Belgium", "French Community"): "French community",
    ("Belgium", "German-speaking Community"): "German-speaking community",
    ("Colombia", "Bogota"): "Bogotá",
    ("Colombia", "Medellin"): "Medellín",
    ("Argentina", "Ciudad Autónoma de Buenos Aires"): "CABA",
    ("Italy", "Emilia Romagna"): "Emilia-Romagna",
    ("Spain", "Comunidad de Madrid"): "Madrid",
    ("Spain", "Castilla y León"): "Castile and Leon",
    ("Spain", "Castilla-La Mancha"): "Castile-La Mancha",
}

def num(x):
    """Return a float, or None for c/m/blank."""
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    return None


def fmt(x):
    return "" if x is None else f"{x:.4f}"


def rows_xlsx(fname, sheet):
    wb = openpyxl.load_workbook(os.path.join(CACHE, fname), read_only=True, data_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    return rows


def rows_xls(fname, sheet):
    s = xlrd.open_workbook(os.path.join(CACHE, fname)).sheet_by_name(sheet)
    return [s.row_values(i) for i in range(s.nrows)]


def regions(rows):
    """Yield (country, region, row) for data rows; a country header is a named row with no numbers or c/m codes."""
    country = None
    for r in rows:
        name = r[0]
        if name in (None, "") or not isinstance(name, str):
            continue
        vals = [x for x in r[1:12] if num(x) is not None or (isinstance(x, str) and x.strip() in ("c", "m"))]
        label = name.strip()
        if not vals:
            country = label
            continue
        if country in (None, "OECD", "Partners"):
            raise ValueError(f"data row {label!r} without a country header")
        reg = label.rstrip("*").strip()
        ctry = COUNTRY_MAP.get(country, country)
        yield ctry, REGION_MAP.get((ctry, reg), reg), r


def expect(rows, row_idx, col, text):
    got = str(rows[row_idx][col]).strip()
    if got != text:
        raise AssertionError(f"header check failed: row {row_idx} col {col} = {got!r}, expected {text!r}")


def find_row(rows, first_cell_texts):
    for i, r in enumerate(rows[:20]):
        cells = [str(x).strip() for x in r if x not in (None, "")]
        if cells[:len(first_cell_texts)] == first_cell_texts:
            return i
    raise AssertionError(f"no header row starting {first_cell_texts}")


def cycle_2022():
    f = "statlink_ax46rt.xlsx"
    sh = rows_xlsx(f, "Table I.B2.36")
    ma = rows_xlsx(f, "Table I.B2.39")
    re_ = rows_xlsx(f, "Table I.B2.40")
    h = find_row(sh, ["%", "S.E.", "%", "S.E."])
    for c, t in ((1, "%"), (2, "S.E."), (4, "%"), (5, "S.E."), (10, "%"), (11, "S.E.")):
        expect(sh, h, c, t)
    for tab in (ma, re_):
        h = find_row(tab, ["Mean score", "S.E.", "Mean score", "S.E."])
        for c, t in ((1, "Mean score"), (3, "Mean score"), (4, "S.E.")):
            expect(tab, h, c, t)
    for tab, title in ((sh, "Percentage of students with an immigrant background"),
                       (ma, "Mathematics performance of students with an immigrant background"),
                       (re_, "Reading performance of students with an immigrant background")):
        if not any(str(r[0]).strip() == title for r in tab[:6]):
            raise AssertionError(f"title {title!r} not found")
    math = {(c, r): row for c, r, row in regions(ma)}
    read = {(c, r): row for c, r, row in regions(re_)}
    out = []
    for c, r, row in regions(sh):
        m, rd = math.get((c, r)), read.get((c, r))
        if m is None or rd is None:
            raise KeyError(f"2022 region {c}/{r} missing from I.B2.39 or I.B2.40")
        out.append([c, r, 2022, num(m[3]), num(m[4]), num(rd[3]), num(rd[4]), num(row[4]), num(row[5]),
                    num(row[10]), "PISA2022 VolI annexB2 I.B2.36/39/40 (stat.link 53f23881-en/ax46rt)"])
    return out


def cycle_2018():
    rows = rows_xlsx("statlink_888934038780.xlsx", "Table II.B2.74")
    h = find_row(rows, ["%", "S.E.", "s", "Mean score"])
    for c, t in ((1, "%"), (2, "S.E."), (4, "Mean score"), (7, "Mean score"), (8, "S.E.")):
        expect(rows, h, c, t)
    h2 = h - 1
    expect(rows, h2, 7, "Non-immigrant students")
    out = []
    for c, r, row in regions(rows):
        out.append([c, r, 2018, None, None, num(row[7]), num(row[8]), num(row[1]), num(row[2]), None,
                    "PISA2018 VolII annexB2 II.B2.74 (doi 10.1787/888934038780)"])
    return out


def cycle_2015():
    rows = rows_xlsx("statlink_888933433235.xlsx", "Table B2.I.71")
    h = find_row(rows, ["%", "S.E.", "%", "S.E.", "%", "S.E.", "%", "S.E."])
    expect(rows, h - 1, 3, "Immigrant students")
    expect(rows, h - 1, 7, "First-generation immigrants")
    out = []
    for c, r, row in regions(rows):
        out.append([c, r, 2015, None, None, None, None, num(row[3]), num(row[4]), num(row[7]),
                    "PISA2015 VolI annexB2 B2.I.71 (doi 10.1787/888933433235)"])
    return out


def cycle_2012():
    rows = rows_xls("statlink_888932964965.xls", "Table B2.II.9")
    h = find_row(rows, ["%", "S.E.", "%", "S.E.", "Mean index"])
    for c, t in ((3, "%"), (4, "S.E."), (9, "Mean score"), (10, "S.E.")):
        expect(rows, h, c, t)
    expect(rows, h - 1, 9, "Non-immigrant")
    expect(rows, h - 1, 3, "Immigrant")
    out = []
    for c, r, row in regions(rows):
        out.append([c, r, 2012, num(row[9]), num(row[10]), None, None, num(row[3]), num(row[4]), None,
                    "PISA2012 VolII annexB2 B2.II.9 (doi 10.1787/888932964965)"])
    return out


def main():
    rows = cycle_2012() + cycle_2015() + cycle_2018() + cycle_2022()
    keys = [(r[0], r[1], r[2]) for r in rows]
    if len(keys) != len(set(keys)):
        dup = sorted({k for k in keys if keys.count(k) > 1})
        raise ValueError(f"duplicate region-cycle keys after harmonization: {dup}")
    cycles = {}
    for c, r, y in keys:
        cycles.setdefault((c, r), set()).add(y)
    kept = [r for r in rows if len(cycles[(r[0], r[1])]) >= 2]
    kept.sort(key=lambda r: (r[0], r[1], r[2]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(COLUMNS)
        for r in kept:
            w.writerow([r[0], r[1], r[2]] + [fmt(x) for x in r[3:10]] + [r[10]])
    dropped = sorted({(c, r) for (c, r), ys in cycles.items() if len(ys) < 2})
    print(f"rows in: {len(rows)}; kept: {len(kept)}; regions kept: {len({(r[0], r[1]) for r in kept})}; "
          f"single-cycle regions dropped: {len(dropped)}")
    for c, r in dropped:
        print(f"  dropped {c} / {r} ({sorted(cycles[(c, r)])})")


if __name__ == "__main__":
    main()

"""Pool DHS Yearbook Table 10 (LPRs by broad class of admission and country of birth), FY2004-2023.

Reads the workbooks `acquire.py` cached, writes
  derived/lpr_class_by_country_year.csv   one row per country and fiscal year, counts by class
  derived/lpr_class_mix.csv               pooled counts and route shares per country
  derived/class_mix_audit.json            per-year header map, row counts, suppressed cells, and
                                          the check that country rows sum to the published total
`--peek YEAR` prints the top of that year's sheet instead (layout inspection).
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
# FY2004 is left out: its table (Table 8, "selected class") has a multi-row header, splits
# immediate relatives three ways and interleaves regions with countries. The design named
# FY2004-2023; pooling FY2005-2023 is a recorded deviation (19 of 20 years).
YEARS = range(2005, 2024)
CLASSES = {  # output column -> keyword that identifies the header cell
    "total": "total",
    "family_sponsored": "family",
    "employment": "employment",
    "immediate_relatives": "immediate",
    "diversity": "diversity",
    "refugee_asylee": "refugee",
    "other": "other",
}
# DHS spellings that changed over the window, or differ from the ACS birthplace label, mapped to
# the ACS label. "Korea" (FY2005-2008) is pooled with "Korea, South"; North Korea is negligible.
HARMONIZE = {
    "Korea, South": "Korea", "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "China, People's Republic": "China", "Burma": "Myanmar", "Cape Verde": "Cabo Verde",
    "Czech Republic": "Czechia", "Macedonia": "North Macedonia",
    "North Macedonia (formerly Macedonia)": "North Macedonia",
}

# Table numbers moved between yearbooks (FY2004's Table 10 is adopted orphans), so the table is
# chosen by its title, never by its number.
TITLE = re.compile(r"class of admission and region and country of birth", re.I)
# FY2004 calls it "selected class of admission" (its Table 8); later years say "broad class".
NOT_TITLE = re.compile(r"new arrival|adjustment|\bage\b|\bsex\b|gender|occupation|marital", re.I)


def sheets_of(path):
    """Yield (sheet name, rows) for every sheet of an .xls or .xlsx workbook."""
    if path.suffix.lower() == ".xls":
        import xlrd
        book = xlrd.open_workbook(path)
        for sheet in book.sheets():
            yield sheet.name, [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
                               for r in range(sheet.nrows)]
    else:
        import openpyxl
        book = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for name in book.sheetnames:
            yield name, [list(row) for row in book[name].iter_rows(values_only=True)]


def table_rows(year):
    """Rows of the one sheet whose title is the class-by-country table; fail unless exactly one."""
    single = list(CACHE.glob(f"lpr_fy{year}.xls*"))
    paths = single or sorted(p for p in (CACHE / f"lpr_fy{year}").rglob("*.xls*")
                             if "sup" not in p.name.lower())
    found = []
    for path in paths:
        for name, rows in sheets_of(path):
            title = " ".join(text(c) for row in rows[:6] for c in row[:2])
            if TITLE.search(title) and not NOT_TITLE.search(title):
                found.append((f"{path.relative_to(CACHE)}::{name}", rows))
    if len(found) != 1:
        raise SystemExit(f"  ✗ FY{year}: expected one class-by-country table, found {[f for f, _ in found]}")
    return found[0]


def text(cell):
    return re.sub(r"\s+", " ", str(cell)).strip() if cell is not None else ""


def header_map(rows):
    for index, row in enumerate(rows[:15]):
        if text(row[0]).lower().startswith("region and country"):  # the title row also names it
            # FY2005-2013 stack the header over three rows ("Family-" / "sponsored" / "preferences")
            stack = rows[max(index - 2, 0):index + 1]
            labels = [" ".join(text(r[i]) for r in stack if i < len(r)).lower() for i in range(len(row))]
            columns = {}
            for name, keyword in CLASSES.items():
                hits = [i for i, label in enumerate(labels) if i >= 1 and keyword in label]
                if len(hits) != 1:
                    raise SystemExit(f"  ✗ header keyword {keyword!r} matched columns {hits}: {labels}")
                columns[name] = hits[0]
            return index, columns
    raise SystemExit("  ✗ no header row naming 'country of birth'")


def number(cell):
    """Count, or None for a suppressed (D) or not-applicable (X) cell; '-' is a published zero."""
    value = text(cell)
    if value in {"-", "–", "—"}:
        return 0.0
    if value in {"D", "X", "NA", ""}:
        return None
    return float(value.replace(",", ""))


def country_rows(rows, start):
    in_countries = False
    for row in rows[start + 1:]:
        label = re.sub(r"\s*\d+$", "", text(row[0])).strip()  # strip footnote digits
        if not label:
            continue
        if label.upper() == "COUNTRY":
            in_countries = True
            continue
        if in_countries:
            if label.lower().startswith(("d ", "- ", "x ", "note", "source", "1 ", "2 ", "3 ")) or len(label) > 60:
                break
            yield label, row


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--peek":
        source, rows = table_rows(int(sys.argv[2]))
        print(f"  {source}")
        for row in rows[:14]:
            print("   ", [text(c)[:22] for c in row[:9]])
        return
    DERIVED.mkdir(exist_ok=True)
    long_rows, audit = [], {}
    for year in YEARS:
        source, rows = table_rows(year)
        start, columns = header_map(rows)
        suppressed, country_total, published_total, count = 0, 0.0, None, 0
        for row in rows[start + 1:start + 6]:
            if text(row[0]).lower().startswith("total"):
                published_total = number(row[columns["total"]])
        for label, row in country_rows(rows, start):
            if label.lower() == "total":  # the country block repeats the grand total as its first row
                continue
            values = {name: number(row[i]) for name, i in columns.items()}
            suppressed += sum(v is None for v in values.values())
            if label.lower() in {"all other countries", "unknown"} or values["total"] is None:
                country_total += values["total"] or 0.0
                continue
            country_total += values["total"]
            count += 1
            long_rows.append({"fiscal_year": year, "country": label, **values})
        audit[str(year)] = {"countries": count, "suppressed_cells": suppressed,
                            "published_total": published_total, "sum_of_country_rows": country_total}
        gap = abs(country_total - (published_total or 0)) / (published_total or 1)
        print(f"  {'✓' if gap < 0.005 else '!'} FY{year}: {count} countries, {suppressed} suppressed cells, "
              f"rows sum to {country_total:,.0f} of {published_total or 0:,.0f}")
    with open(DERIVED / "lpr_class_by_country_year.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["fiscal_year", "country", *CLASSES])
        writer.writeheader()
        for row in long_rows:
            writer.writerow({k: ("" if v is None else (int(v) if isinstance(v, float) else v)) for k, v in row.items()})
    pooled = {}
    for row in long_rows:
        name = HARMONIZE.get(row["country"], row["country"])
        target = pooled.setdefault(name, {k: 0.0 for k in CLASSES} | {"years": 0, "suppressed_cells": 0})
        target["years"] += 1
        for key in CLASSES:
            if row[key] is None:
                target["suppressed_cells"] += 1
            else:
                target[key] += row[key]
    with open(DERIVED / "lpr_class_mix.csv", "w", newline="") as handle:
        fields = ["country", "years", "suppressed_cells", "lpr_total", "share_employment", "share_family",
                  "share_diversity", "share_refugee_asylee", "share_other", *CLASSES]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for name, t in sorted(pooled.items(), key=lambda kv: -kv[1]["total"]):
            # shares over the sum of published class cells, so a suppressed cell drops from both sides
            base = sum(t[k] for k in CLASSES if k != "total")
            if base <= 0:
                continue
            writer.writerow({
                "country": name, "years": t["years"], "suppressed_cells": t["suppressed_cells"],
                "lpr_total": int(t["total"]),
                "share_employment": f"{t['employment'] / base:.5f}",
                "share_family": f"{(t['family_sponsored'] + t['immediate_relatives']) / base:.5f}",
                "share_diversity": f"{t['diversity'] / base:.5f}",
                "share_refugee_asylee": f"{t['refugee_asylee'] / base:.5f}",
                "share_other": f"{t['other'] / base:.5f}",
                **{k: int(t[k]) for k in CLASSES}})
    audit["harmonized_names"] = HARMONIZE
    (DERIVED / "class_mix_audit.json").write_text(json.dumps(audit, indent=1))
    print(f"  ✓ pooled {len(pooled)} countries, FY{YEARS[0]}-{YEARS[-1]}")


if __name__ == "__main__":
    sys.exit(main())

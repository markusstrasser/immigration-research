#!/usr/bin/env python3
"""India's share of US admission channels, FY2020-FY2024.

Sources, cached to `_cache/` with their sha256 recorded in `derived/entry_class_sources.json`:
  * DHS/OHSS Yearbook of Immigration Statistics, Table 10 ("Persons Obtaining Lawful Permanent
    Resident Status by Broad Class of Admission and Region and Country of Birth"), one workbook
    per fiscal year — employment-based, family-sponsored, immediate relatives, diversity.
  * DHS/OHSS Yearbook nonimmigrant workbook, Table 32 (I-94 admissions by selected category of
    admission and country of citizenship) for H-1B *admissions* by citizenship.
  * USCIS H-1B petition statistics (Characteristics of H-1B Specialty Occupation Workers) for
    H-1B *approvals* by country of birth, when the report is reachable.

H-1B admissions (I-94 border events) and H-1B approvals (petitions) are different objects and
are reported separately; an admission is a border crossing, so one worker can generate several.

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" --with openpyxl --with requests \
     python3 entry_class.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
YEARS = [2020, 2021, 2022, 2023, 2024]
UA = "Mozilla/5.0 (research; immigration-fiscal lane)"
BASE = "https://ohss.dhs.gov"


def fetch(url: str, dest: Path) -> Path:
    """curl, not urllib: ohss.dhs.gov answers urllib with 403 (checked 2026-09-18)."""
    if dest.exists():
        return dest
    print(f"  fetching {url}", flush=True)
    rc = subprocess.call(["curl", "-s", "--http1.1", "-L", "--max-time", "180",
                          "-A", UA, "-o", str(dest), url])
    if rc != 0 or not dest.exists() or dest.stat().st_size == 0:
        dest.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] curl rc={rc} for {url}")
    return dest


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def discover(year: int, pattern: str) -> str | None:
    page = CACHE / f"yearbook_{year}.html"
    if not page.exists():
        fetch(f"{BASE}/topics/immigration/yearbook/{year}", page)
    html = page.read_text(errors="replace")
    hits = re.findall(r'href="([^"]*\.xlsx)"', html)
    for h in hits:
        if pattern in h.lower():
            return h if h.startswith("http") else BASE + h
    return None


def discover_lpr(year: int) -> str | None:
    """Year page first (full LPR workbook); else the table-10 subpage (tables 8-11 workbook)."""
    url = discover(year, "lawful_permanent_residents")
    if url:
        return url
    page = CACHE / f"yearbook_{year}_table10.html"
    if not page.exists():
        fetch(f"{BASE}/topics/immigration/yearbook/{year}/table10", page)
    hits = re.findall(r'href="([^"]*\.xlsx)"', page.read_text(errors="replace"))
    for h in hits:
        if "tables8-11" in h.lower() or "lawful_permanent_residents" in h.lower():
            return h if h.startswith("http") else BASE + h
    return hits[0] if hits else None


def parse_table10(path: Path) -> pd.DataFrame:
    """Return a tidy frame of the country rows of Yearbook Table 10."""
    book = pd.ExcelFile(path)
    sheet = next((n for n in book.sheet_names
                  if n.replace(" ", "").lower().startswith("table10")), None)
    if sheet is None:
        raise SystemExit(f"[BLOCKED] no 'Table 10' sheet in {path.name}: {book.sheet_names}")
    raw = book.parse(sheet, header=None)
    header_row = None
    for i in range(len(raw)):
        first = str(raw.iloc[i, 0]).strip().lower()
        if first.startswith("region and country of birth"):
            header_row = i
            break
    if header_row is None:
        raise SystemExit(f"[BLOCKED] header row not found in {path.name}")
    cols = [str(x).strip() for x in raw.iloc[header_row].tolist()]
    # FY2020/FY2021 use the "tables 8-11 new adjustment" workbook, whose Table 10 splits every
    # class of admission into "Adjustments of status" and "New arrivals" under a two-row header.
    # Those two halves are summed back into one class column so every year is comparable.
    second = [str(x).strip() for x in raw.iloc[header_row + 1].tolist()]
    two_level = second[1].lower() == "total"
    if two_level:
        classes = second[1:]
        body = raw.iloc[header_row + 2:].copy()
        body.columns = ["country"] + [f"{c}__{i}" for i, c in enumerate(classes)]
        body["country"] = body.country.astype(str).str.strip()
        for c in body.columns[1:]:
            body[c] = pd.to_numeric(body[c].astype(str).str.replace(",", ""), errors="coerce")
        out = pd.DataFrame({"country": body.country})
        for name in dict.fromkeys(classes):
            parts = [c for c in body.columns[1:] if c.rsplit("__", 1)[0] == name]
            out[name] = body[parts].sum(axis=1, min_count=1)
        return out
    body = raw.iloc[header_row + 1:].copy()
    body.columns = cols
    body = body.rename(columns={cols[0]: "country"})
    body["country"] = body.country.astype(str).str.strip()
    numeric = [c for c in body.columns if c != "country"]
    for c in numeric:
        body[c] = pd.to_numeric(body[c].astype(str).str.replace(",", "").str.replace("-", ""),
                                errors="coerce")
    return body


def series_for(body: pd.DataFrame, country: str) -> pd.Series | None:
    hit = body[body.country.str.lower() == country.lower()]
    if len(hit) == 0:
        return None
    return hit.iloc[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    sources, rows = {}, []
    print("[1/3] DHS Yearbook Table 10, FY2020-FY2024", flush=True)
    for year in YEARS:
        url = discover_lpr(year)
        if url is None:
            print(f"  ! FY{year}: no LPR workbook link found — SKIPPED", flush=True)
            continue
        dest = CACHE / f"yearbook_lpr_fy{year}.xlsx"
        fetch(url, dest)
        sources[f"yearbook_lpr_fy{year}"] = {"url": url, "sha256": sha256(dest),
                                             "bytes": dest.stat().st_size}
        body = parse_table10(dest)
        total = series_for(body, "Total")
        india = series_for(body, "India")
        china = series_for(body, "China, People's Republic")
        if china is None:
            china = series_for(body, "China")
        mexico = series_for(body, "Mexico")
        if total is None or india is None:
            print(f"  ! FY{year}: Total/India row missing — SKIPPED", flush=True)
            continue
        for label, s in (("India", india), ("China", china), ("Mexico", mexico)):
            if s is None:
                continue
            for col in body.columns:
                if col == "country" or not pd.notna(total.get(col)):
                    continue
                rows.append({"fiscal_year": year, "series": "LPR_table10", "country": label,
                             "class_of_admission": col, "persons": float(s.get(col))
                             if pd.notna(s.get(col)) else float("nan"),
                             "all_countries": float(total.get(col)),
                             "share_of_class": (float(s.get(col)) / float(total.get(col)))
                             if pd.notna(s.get(col)) and float(total.get(col)) else float("nan")})
        print(f"  FY{year}: parsed {len(body)} rows", flush=True)

    print("[2/3] DHS Yearbook nonimmigrant workbook (H-1B admissions by citizenship)", flush=True)
    ni_url = discover(2024, "nonimmigrants")
    if ni_url:
        dest = CACHE / "yearbook_nonimmigrants_fy2024.xlsx"
        fetch(ni_url, dest)
        sources["yearbook_nonimmigrants_fy2024"] = {"url": ni_url, "sha256": sha256(dest),
                                                    "bytes": dest.stat().st_size}
        book = pd.ExcelFile(dest)
        # Table 33 is the temporary-worker table: "Workers in specialty occupations" is H-1B.
        # Table 29 is the wider selected-category table. Both are keyed on country of citizenship.
        for sheet in ("Table 33", "Table 29"):
            if sheet not in book.sheet_names:
                continue
            raw = book.parse(sheet, header=None)
            # startswith, not "in": the sheet title also contains the phrase.
            hdr = next((i for i in range(len(raw))
                        if str(raw.iloc[i, 0]).strip().lower().startswith(
                            "region and country of citizenship")),
                       None)
            if hdr is None:
                continue
            seen, cols = {}, []
            for j, x in enumerate(raw.iloc[hdr].tolist()):
                name = " ".join(str(x).split())[:60] if str(x) != "nan" else f"col{j}"
                seen[name] = seen.get(name, 0) + 1
                cols.append(name if seen[name] == 1 else f"{name} ({seen[name]})")
            body = raw.iloc[hdr + 1:].copy()
            body.columns = cols
            body = body.rename(columns={cols[0]: "country"})
            body["country"] = body.country.astype(str).str.strip()
            for c in body.columns:
                if c != "country":
                    body[c] = pd.to_numeric(body[c].astype(str).str.replace(",", ""),
                                            errors="coerce")
            total = series_for(body, "Total")
            india = series_for(body, "India")
            china = series_for(body, "China, People's Republic")
            if china is None:
                china = series_for(body, "China")
            if total is None or india is None:
                continue
            for label, s in (("India", india), ("China", china)):
                if s is None:
                    continue
                for col in body.columns:
                    if col == "country" or not pd.notna(total.get(col)):
                        continue
                    rows.append({"fiscal_year": 2024, "series": f"NI_{sheet.replace(' ', '')}",
                                 "country": label, "class_of_admission": col,
                                 "persons": float(s.get(col)) if pd.notna(s.get(col)) else float("nan"),
                                 "all_countries": float(total.get(col)),
                                 "share_of_class": (float(s.get(col)) / float(total.get(col)))
                                 if pd.notna(s.get(col)) and float(total.get(col)) else float("nan")})
            print(f"  parsed {sheet}", flush=True)
    else:
        print("  ! nonimmigrant workbook link not found — SKIPPED", flush=True)

    frame = pd.DataFrame(rows).sort_values(
        ["series", "fiscal_year", "country", "class_of_admission"], kind="stable")
    frame.to_csv(args.out / "entry_class.csv", index=False, float_format="%.6f")
    (args.out / "entry_class_sources.json").write_text(
        json.dumps(sources, indent=2, sort_keys=True) + "\n")

    print("[3/3] report", flush=True)
    lines = ["India's share of US admission channels — DHS/OHSS Yearbook of Immigration Statistics",
             ""]
    lpr = frame.query("series == 'LPR_table10' and country == 'India'")
    classes = [c for c in lpr.class_of_admission.unique()]
    lines.append(f"{'class of admission':46s}" + "".join(f"{y:>12d}" for y in YEARS))
    for c in classes:
        cells = ""
        for y in YEARS:
            q = lpr.query("fiscal_year == @y and class_of_admission == @c")
            cells += (f"{q.share_of_class.iloc[0] * 100:>11.1f}%" if len(q) == 1
                      and pd.notna(q.share_of_class.iloc[0]) else "—".rjust(12))
        lines.append(f"{c[:46]:46s}{cells}")
    lines.append("")
    lines.append("India persons, same cells:")
    for c in classes:
        cells = ""
        for y in YEARS:
            q = lpr.query("fiscal_year == @y and class_of_admission == @c")
            cells += (f"{q.persons.iloc[0]:>12,.0f}" if len(q) == 1
                      and pd.notna(q.persons.iloc[0]) else "—".rjust(12))
        lines.append(f"{c[:46]:46s}{cells}")
    ni = frame[frame.series.str.startswith("NI_") & (frame.country == "India")]
    if len(ni):
        lines.append("")
        lines.append("I-94 nonimmigrant admissions, FY2024, India share of each category:")
        for _, r in ni.iterrows():
            if pd.notna(r.share_of_class):
                lines.append(f"  {r.class_of_admission[:52]:52s} {r.share_of_class * 100:6.1f}%"
                             f"  ({r.persons:,.0f} of {r.all_countries:,.0f})")
    text = "\n".join(lines) + "\n"
    (args.out / "entry_class_result.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()

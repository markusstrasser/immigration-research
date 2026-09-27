#!/usr/bin/env python3
"""Statewide grade 3-8 ELA and math scale-score means and SDs for NY, IL and CO.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/newcomer_school_shock_2026_09_28/extract_scale_sd.py

Inputs are raw files under `_cache/sd/` (this worker's pulls) and, read in place, the CDE CMAS summary
workbooks the Denver worker cached under `_cache/denver/`. Every input is pinned by sha256; a mismatch
stops the run. PDFs are read with `pdftotext -layout`; each value is anchored to its table title and
each table must yield the expected grades.

Output: `derived/scale_sd.csv` with columns
    state, year, subject, grade, n, mean, sd, source_file, source_table, page
- `year` is the spring test year.
- `state` is the population the statistic describes. Illinois figures for 2018, 2019, 2021 and 2022
  come from consortium technical reports that pool Illinois with other members; those rows carry the
  pooled population (for example `IL+BIE+NJ+NM`), never `IL`.
- `mean`, `sd` and `n` are the published values as printed (CO rounds mean and SD to integers).
- `page` is the 1-based PDF page for PDF sources and the 1-based worksheet row for spreadsheets.
See `reads/scale_sd_sources.md` for the quoted tables and the gaps.
"""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path

import openpyxl

LANE = Path(__file__).resolve().parent
OUT = LANE / "derived" / "scale_sd.csv"
GRADES = [3, 4, 5, 6, 7, 8]

PINS = {
    # New York State Education Department, grades 3-8 technical reports
    "_cache/sd/nysed_3-8_techreport_2018.pdf": "369dc705d48898dc4bbfc9597b5fa5611b4efc5fc59f9326c60c1bbc1b516c37",
    "_cache/sd/nysed_3-8_techreport_2019.pdf": "fac00bac07daebe4e54d55a17afcda6588c442061afa858e06f9f537afd7f62f",
    "_cache/sd/nysed_3-8_techreport_2021.pdf": "4874a1cd175cb87504e439f228cc6cf639d24d6fe7bb3758ae7fbca3d3f9c765",
    "_cache/sd/nysed_3-8_techreport_2022.pdf": "2bcbc4c69b8e402b8a69945bc5d112c9f4d8b48619a23d49388d4e67c3ab670d",
    "_cache/sd/nysed_3-8_techreport_2023.pdf": "91b75e98420cb6d4bc23681a8e71441c8e6556f2f6b1acc3c0f46ce922cfaecd",
    "_cache/sd/nysed_3-8_techreport_2024.pdf": "b5c089af4f5151faf5c6b35652b122b980f52d49c0581986a4647313e13c7f5e",
    "_cache/sd/nysed_3-8_techreport_2025.pdf": "ed1ac368a277600c9384adf4b27a7cefab83ae980815a117ce9197e38d753639",
    # Illinois: PARCC 2018 (Pearson), IAR 2019-2023 (New Meridian), IAR 2024-2025 (Pearson for ISBE)
    "_cache/sd/isbe_parcc_techreport_2018.pdf": "52e95b346bda1387d0da5e4a426f01cd4410dbf609b5cc235569f01a749a6d10",
    "_cache/sd/isbe_iar_techreport_2019.pdf": "6d1ef1f66fa5355f16c95175f0cdf502286dc9a185a41b8706f3a1ca0e82d144",
    "_cache/sd/isbe_iar_techreport_2021.pdf": "e627e80de7635069e4433539136cb01b228297ae317524eb7519b781de7fbf81",
    "_cache/sd/isbe_iar_techreport_2022.pdf": "103dfee0e73d69f640024229b9e6795b3f499488c2fb9ffd0c7231dde7e5d326",
    "_cache/sd/isbe_iar_techreport_2023.pdf": "bb1e90e673ee8d3b324ac9e2c4a58903b76283f886e4142da1098c1d495d0618",
    "_cache/sd/isbe_iar_techreport_2024.pdf": "de93ad2ed639535f949e785e7ac85c3640a0d809625df26f6eb92c05e736128e",
    "_cache/sd/isbe_iar_techreport_2025.pdf": "be516e0ed262f039b09b33f9c3d0c0c4d02a1cef9a91fa943fa574131186bd38",
    # Colorado Department of Education, CMAS
    "_cache/sd/cde_cmas_state_summary_2017.pdf": "8b993ed670d438f8410ece83aaa1cfb6a2c0fac2f84701ff2891f2768359a036",
    "_cache/sd/cde_cmas_state_summary_2018.pdf": "8032c82a6bcf7a5c0cdc4abff55b2c5732ed0f521f10ef69e0e2a7bab266751a",
    "_cache/denver/cde_cmas_overall_2017.xlsx": "fc1888047e435b7e545edcb05e4475a8f6d7c7d6ffe0a1ca128e894e67b0f6fa",
    "_cache/denver/cde_cmas_overall_2018.xlsx": "22e6a523d41ada5c6a9d5d958fff33a39442237d072f12b765caa04655d7e25e",
    "_cache/denver/cde_cmas_overall_2019.xlsx": "1f35cc5e4544fe9c842ddd76175f1b6cefe485a7765d5556b6c4bf4f0ef62c14",
    "_cache/denver/cde_cmas_overall_2021.xlsx": "e2b09b64335cd01d5bc30fb78833b2773320adfc644cab6a9073ce41f943abd7",
    "_cache/denver/cde_cmas_overall_2022.xlsx": "e6987f4752bb6351f931d69390508f0578b61777bc1e88c1677602a15e9c0864",
    "_cache/denver/cde_cmas_overall_2023.xlsx": "d53fe2a5037d0f3268bc8eb8f130730b065c47e8ea71f736727e6ce7717fbf43",
    "_cache/denver/cde_cmas_overall_2024.xlsx": "b7d8ab68bc9ea3ba7451f3ac8518a4c6437d92aa989a975187f60ede3ad3c590",
    "_cache/denver/cde_cmas_overall_2025.xlsx": "4b98b24812f867ab62910400e3e9a69dfb3a65aa9b7ebb900841b7362f1e69f9",
    "_cache/denver/cde_cmas_overall_2026.xlsx": "3e09dc291af72efcf5566855401fa2697bac5f1cf1fede3ac386765363236197",
}

# --- New York ---------------------------------------------------------------------------------------
NY_TABLES = {  # year -> (ELA table title, mathematics table title)
    2018: ("Table 9.1. ELA Scale Score Distribution Summary", "Table 9.9. Mathematics Scale Score Distribution Summary"),
    2019: ("Table 8.1. ELA Scale Score Distribution Summary", "Table 8.9. Mathematics Scale Score Distribution Summary"),
    2022: ("Table 8.1. ELA Scale Score Distribution Summary", "Table 8.9. Mathematics Scale Score Distribution Summary"),
    2023: ("Table 9.1. ELA Scale Score Distribution Summary", "Table 9.9. Mathematics Scale Score Distribution Summary"),
    2024: ("Table 8.1. ELA Scale Score Distribution Summary", "Table 8.9. Mathematics Scale Score Distribution Summary"),
    2025: ("Table 8.1. ELA Scale Score Distribution Summary", "Table 8.9. Mathematics Scale Score Distribution Summary"),
}
NY_POPULATION = "include examinees with valid scores from all public, non-public, and charter schools"
# Grade, N-Count, Mean, SD (2018 and 2019 add percentile columns after SD).
NY_ROW = re.compile(r"^\s*([3-8])\s+([\d,]{5,})\s+(\d{3}(?:\.\d+)?)\s+(\d{1,2}\.\d+)(?:\s|$)")

# --- Illinois ---------------------------------------------------------------------------------------
PARCC_ELA = "Table A.12.{n} Subgroup Performance for ELA/L Scale Scores: Grade {g}"
PARCC_MATH = "Table A.12.{n} Subgroup Performance for Mathematics Scale Scores: Grade {g}"
PEARSON_ELA = "Table B.{n}. Scale Score Performance by Demographic Subgroup—ELA/L Grade {g}"
PEARSON_MATH = "Table B.{n}. Scale Score Performance by Demographic Subgroup—Mathematics Grade {g}"
IL_SPECS = {
    # year: (population label, ELA title, first ELA table number, math title, first math table number,
    #        population statement that must appear in the report)
    2018: ("IL+BIE+DC+DoDEA+MD+NJ+NM", PARCC_ELA, 27, PARCC_MATH, 36,
           "Participation included students from Bureau of Indian Education, District of Columbia, "
           "Department of Defense Education Activity, Illinois, Maryland, New Jersey, and New Mexico."),
    2019: ("IL+BIE+NJ+NM", PARCC_ELA, 48, PARCC_MATH, 57,
           "Approximately two million students from the Bureau of Indian Education, Illinois, New Jersey, "
           "and New Mexico participated in the operational administration of the summative assessments "
           "during the 2018–2019 school year."),
    2021: ("IL+BIE+DoDEA", PARCC_ELA, 42, PARCC_MATH, 50,
           "Over a million forms were administered in the Bureau of Indian Education, the Department of "
           "Defense Education Activity, and Illinois during the 2020–2021 school year."),
    2022: ("IL+DC+DoDEA+NJ", PARCC_ELA, 40, PARCC_MATH, 48,
           "Over a million forms were administered in the Department of Defense Education Activity, the "
           "District of Columbia, Illinois, and New Jersey during the 2021–2022 school year."),
    2023: ("IL", PARCC_ELA, 35, PARCC_MATH, 41,
           "Almost 800,000 forms were administered in Illinois during the 2022–2023 school year."),
    2024: ("IL", PEARSON_ELA, 1, PEARSON_MATH, 7,
           "Prepared by Pearson for the Illinois State Board of Education (ISBE)"),
    2025: ("IL", PEARSON_ELA, 1, PEARSON_MATH, 7,
           "Prepared by Pearson for the Illinois State Board of Education (ISBE)"),
}
IL_FILES = {2018: "_cache/sd/isbe_parcc_techreport_2018.pdf"} | {
    y: f"_cache/sd/isbe_iar_techreport_{y}.pdf" for y in (2019, 2021, 2022, 2023, 2024, 2025)
}
# N, optional percent (2025), Mean, SD, Min, Max on the overall row.
IL_ROW = re.compile(
    r"(?:^|\s)([\d,]{5,})\s+(?:[\d.]+%\s+)?(\d{3}(?:\.\d+)?)\s+(\d{1,2}\.\d+)\s+(\d{3})\s+(\d{3})\s*$"
)
IL_OVERALL = re.compile(r"full\s+summative|overall\s+score", re.IGNORECASE)

# --- Colorado ---------------------------------------------------------------------------------------
CO_PDF = {  # year: (state summary PDF, page-1 title anchor, table name for the CSV, workbook for the cross-check)
    2017: ("_cache/sd/cde_cmas_state_summary_2017.pdf", "CMAS ELA and Math (PARCC) 2016-2017 Achievement Results",
           "CMAS ELA and Math (PARCC) 2016-2017 Achievement Results: Overall Results",
           "_cache/denver/cde_cmas_overall_2017.xlsx"),
    2018: ("_cache/sd/cde_cmas_state_summary_2018.pdf", "2018 CMAS English Language Arts/Literacy and Mathematics",
           "2018 CMAS English Language Arts/Literacy and Mathematics State Achievement Results: Overall Results",
           "_cache/denver/cde_cmas_overall_2018.xlsx"),
}
CO_PDF_ROW = re.compile(r"^\s*(ELA|Math|Mathematics) Grade 0([3-8])\s+([\d,]+)\s+(\d{3})\s+(\d{2})\s")
CO_XLSX = {y: f"_cache/denver/cde_cmas_overall_{y}.xlsx" for y in (2019, 2021, 2022, 2023, 2024, 2025, 2026)}
CO_SHEET = "CMAS ELA and Math"
CO_SUBJECT = {"English Language Arts": "ELA", "Mathematics": "math"}
# 2021 administered only the required grades (ELA 3, 5, 7; math 4, 6, 8) to all students.
CO_EXPECTED_2021 = {("ELA", 3), ("ELA", 5), ("ELA", 7), ("math", 4), ("math", 6), ("math", 8)}

EXPECTED_ROWS = 6 * 12 + 7 * 12 + (8 * 12 + 6)  # NY + IL (incl. pooled years) + CO


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_pins() -> None:
    for rel, want in PINS.items():
        got = sha256(LANE / rel)
        if got != want:
            raise SystemExit(f"[BLOCKED] sha256 mismatch for {rel}: {got} != {want}")


def pdf_pages(rel: str) -> list[str]:
    out = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(LANE / rel), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    return out.split("\f")


def flat(text: str) -> str:
    """Join hyphenated line breaks and collapse whitespace, for matching prose statements."""
    return re.sub(r"\s+", " ", re.sub(r"-\s*\n\s*", "-", text))


def lines_with_pages(pages: list[str]) -> list[tuple[int, str]]:
    return [(i + 1, line) for i, page in enumerate(pages) for line in page.splitlines()]


def find_title(lines: list[tuple[int, str]], title: str) -> int:
    hits = [k for k, (_, line) in enumerate(lines) if line.strip() == title]
    if len(hits) != 1:
        raise SystemExit(f"[BLOCKED] expected one standalone line {title!r}, found {len(hits)}")
    return hits[0]


def num(token: str) -> str:
    return token.replace(",", "")


def extract_ny() -> list[dict]:
    rows = []
    for year, titles in NY_TABLES.items():
        rel = f"_cache/sd/nysed_3-8_techreport_{year}.pdf"
        pages = pdf_pages(rel)
        if NY_POPULATION not in flat("\n".join(pages)):
            raise SystemExit(f"[BLOCKED] NY {year}: population statement not found")
        lines = lines_with_pages(pages)
        for subject, title in zip(("ELA", "math"), titles):
            start = find_title(lines, title)
            found = []
            for page, line in lines[start + 1:start + 60]:
                m = NY_ROW.match(line)
                if m:
                    found.append((page, m))
                if len(found) == len(GRADES):
                    break
            grades = [int(m.group(1)) for _, m in found]
            if grades != GRADES:
                raise SystemExit(f"[BLOCKED] NY {year} {subject}: grades {grades}")
            for page, m in found:
                rows.append(dict(state="NY", year=year, subject=subject, grade=int(m.group(1)),
                                 n=num(m.group(2)), mean=m.group(3), sd=m.group(4), source_file=rel,
                                 source_table=title, page=page))
    # The 2021 report publishes no scale-score distribution; its form statistics are raw scores from
    # the original (2018/2019) administrations. Fail loudly if a revised file changes that.
    text21 = flat("\n".join(pdf_pages("_cache/sd/nysed_3-8_techreport_2021.pdf")))
    if "Scale Score Distribution Summary" in text21 or \
            "Based on Session 1 test questions from the original administration test data" not in text21:
        raise SystemExit("[BLOCKED] NY 2021 report no longer matches the documented gap")
    return rows


def extract_il() -> list[dict]:
    rows = []
    for year, (label, ela_t, ela_n, math_t, math_n, statement) in IL_SPECS.items():
        rel = IL_FILES[year]
        pages = pdf_pages(rel)
        if statement not in flat("\n".join(pages)):
            raise SystemExit(f"[BLOCKED] IL {year}: population statement not found")
        lines = lines_with_pages(pages)
        for subject, template, first in (("ELA", ela_t, ela_n), ("math", math_t, math_n)):
            for k, grade in enumerate(GRADES):
                title = template.format(n=first + k, g=grade)
                start = find_title(lines, title)
                window = lines[start + 1:start + 8]
                hit = next(((j, page, IL_ROW.search(line)) for j, (page, line) in enumerate(window)
                            if IL_ROW.search(line)), None)
                if hit is None:
                    raise SystemExit(f"[BLOCKED] IL {year}: no overall row under {title!r}")
                j, page, m = hit
                label_text = " ".join(line for _, line in window[:j + 2])
                if not IL_OVERALL.search(label_text) or (m.group(4), m.group(5)) != ("650", "850"):
                    raise SystemExit(f"[BLOCKED] IL {year}: first row under {title!r} is not the overall row")
                rows.append(dict(state=label, year=year, subject=subject, grade=grade, n=num(m.group(1)),
                                 mean=m.group(2), sd=m.group(3), source_file=rel, source_table=title, page=page))
    return rows


def co_state_rows(rel: str, sheet: str | None) -> tuple[list[str], list[tuple[int, tuple]]]:
    """Header (whitespace-collapsed) and the Level=STATE rows, with worksheet row numbers."""
    wb = openpyxl.load_workbook(LANE / rel, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    header, state = None, []
    for row in ws.iter_rows():
        values = tuple(c.value for c in row)
        if not values:
            continue
        if values[0] == "Level":
            header = [" ".join(str(v).split()) if v is not None else "" for v in values]
        elif header and values[0] == "STATE":
            state.append((row[0].row, values))
        elif state:
            break
    wb.close()
    if header is None or not state:
        raise SystemExit(f"[BLOCKED] {rel}: no header or STATE rows")
    return header, state


def cell(values: tuple, i: int) -> str:
    return " ".join(str(values[i]).split())


def extract_co() -> list[dict]:
    rows = []
    all_cells = {(s, g) for s in ("ELA", "math") for g in GRADES}
    for year, (rel, title_anchor, table_name, xlsx) in CO_PDF.items():
        page1 = pdf_pages(rel)[0]
        if title_anchor not in page1 or "Overall Results" not in page1 or "Deviation" not in page1:
            raise SystemExit(f"[BLOCKED] CO {year}: page 1 is not the overall state results table")
        found = {}
        for line in page1.splitlines():
            m = CO_PDF_ROW.match(line)
            if m:
                key = ("ELA" if m.group(1) == "ELA" else "math", int(m.group(2)))
                if key in found:
                    raise SystemExit(f"[BLOCKED] CO {year}: {key} appears twice on page 1")
                found[key] = (num(m.group(3)), m.group(4), m.group(5))
        if set(found) != all_cells:
            raise SystemExit(f"[BLOCKED] CO {year}: grades found {sorted(found)}")
        # Cross-check valid-score counts and means against the district/school workbook's STATE rows
        # (that workbook has no SD column in 2017 and 2018).
        header, state = co_state_rows(xlsx, None)
        i_test = 6
        i_n = next(i for i, h in enumerate(header) if h.endswith("of Valid Scores"))
        i_mean = header.index("Mean Scale Score")
        checked = set()
        for _, values in state:
            m = re.fullmatch(r"(ELA|Math|Mathematics|English Language Arts) Grade 0([3-8])", cell(values, i_test))
            if not m:
                continue
            key = ("ELA" if m.group(1) in ("ELA", "English Language Arts") else "math", int(m.group(2)))
            if (num(cell(values, i_n)), cell(values, i_mean)) != found[key][:2]:
                raise SystemExit(f"[BLOCKED] CO {year} {key}: PDF and workbook disagree")
            checked.add(key)
        if checked != all_cells:
            raise SystemExit(f"[BLOCKED] CO {year}: cross-check covered {sorted(checked)}")
        for (subject, grade), (n, mean, sd) in sorted(found.items()):
            rows.append(dict(state="CO", year=year, subject=subject, grade=grade, n=n, mean=mean, sd=sd,
                             source_file=rel, source_table=table_name, page=1))
    for year, rel in CO_XLSX.items():
        header, state = co_state_rows(rel, CO_SHEET)
        i_sd = header.index("Standard Deviation")
        i_mean = i_sd - 1
        if header[i_mean] != "Mean Scale Score":
            raise SystemExit(f"[BLOCKED] CO {year}: mean column is not beside the SD column")
        i_subj = header.index("Subject") if "Subject" in header else header.index("Content")
        i_grade, i_n = header.index("Grade"), header.index("Number of Valid Scores")
        got = set()
        for row_no, values in state:
            subject = CO_SUBJECT.get(cell(values, i_subj))
            grade = cell(values, i_grade)
            if subject is None or grade not in {f"0{g}" for g in GRADES}:
                continue
            got.add((subject, int(grade)))
            rows.append(dict(state="CO", year=year, subject=subject, grade=int(grade), n=num(cell(values, i_n)),
                             mean=cell(values, i_mean), sd=cell(values, i_sd), source_file=rel,
                             source_table=f"sheet '{CO_SHEET}': Level=STATE rows (page = worksheet row)",
                             page=row_no))
        if got != (CO_EXPECTED_2021 if year == 2021 else all_cells):
            raise SystemExit(f"[BLOCKED] CO {year}: STATE rows {sorted(got)}")
    return rows


def sanity(rows: list[dict]) -> None:
    for r in rows:
        mean, sd, n = float(r["mean"]), float(r["sd"]), int(r["n"])
        if r["state"] == "NY":
            lo, hi, sd_lo, sd_hi = (430, 470, 18, 35) if r["year"] >= 2023 else (580, 620, 15, 30)
        else:
            lo, hi, sd_lo, sd_hi = 650, 850, 20, 60
        if not (lo <= mean <= hi and sd_lo <= sd <= sd_hi and n >= 30000):
            raise SystemExit(f"[BLOCKED] implausible row {r}")


def main() -> None:
    check_pins()
    rows = extract_ny() + extract_il() + extract_co()
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"[BLOCKED] expected {EXPECTED_ROWS} rows, got {len(rows)}")
    keys = [(r["state"], r["year"], r["subject"], r["grade"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise SystemExit("[BLOCKED] duplicate state-year-subject-grade rows")
    sanity(rows)
    rows.sort(key=lambda r: (r["state"], r["year"], r["subject"], r["grade"]))
    cols = ["state", "year", "subject", "grade", "n", "mean", "sd", "source_file", "source_table", "page"]
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(cols)
        for r in rows:
            writer.writerow([r[c] for c in cols])
    print(f"wrote {OUT.relative_to(LANE)}: {len(rows)} rows")


if __name__ == "__main__":
    main()

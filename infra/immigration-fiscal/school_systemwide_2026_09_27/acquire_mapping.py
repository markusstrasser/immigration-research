"""NCES "Mapping State Proficiency Standards onto the NAEP Scales": NAEP-equivalent cut scores.

Downloads the NCES state-mapping HTML data tables (2005–2022) into _cache/mapping/ and writes
derived/mapping_cut_scores.csv: one row per state × year × grade × subject with the NAEP scale
equivalent of the state's proficient standard, its standard error and relative error.

Sources: https://nces.ed.gov/nationsreportcard/studies/statemapping/data_tables.aspx
  2005, 2007, 2009 (NCES 2011-458 series): findings_table3/2/1.aspx, one table per subject.
  2009–2015: findings_table_<year>a/b.aspx (a = grade 4, b = grade 8).
  2017–2022: table_<year>a/b.aspx, with a testing-program column.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/acquire_mapping.py
"""
import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "mapping"
OUT = HERE / "derived" / "mapping_cut_scores.csv"
BASE = "https://nces.ed.gov/nationsreportcard/studies/statemapping/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"}

POSTAL = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "Puerto Rico": "PR",
}
# per-subject tables of the 2005–2009 series (NCES 2011-458)
OLD = {"findings_table3": 2005, "findings_table2": 2007, "findings_table1": 2009}
# per-grade tables: (page, year, grade)
NEW = [(f"findings_table_{y}{g}", y, 4 if g == "a" else 8) for y in (2009, 2011, 2013, 2015) for g in "ab"]
NEW += [(f"table_{y}{g}", y, 4 if g == "a" else 8) for y in (2017, 2019, 2022) for g in "ab"]
FIELDS = ["year", "grade", "subject", "state", "state_label", "naep_equiv", "se", "rel_error", "flag",
          "testing_program", "series", "source_table"]


def get(page):
    path = CACHE / f"{page}.html"
    if not path.exists():
        for attempt in range(4):
            r = requests.get(BASE + page + ".aspx", headers=UA, timeout=120)
            if r.status_code == 200 and "<table" in r.text:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(r.content)
                break
            time.sleep(5 * (attempt + 1))
        else:
            raise RuntimeError(page)
    return BeautifulSoup(path.read_bytes().decode("utf-8", "replace"), "html.parser")


def state_of(label):
    base = re.sub(r"\s*\d+$", "", label).strip()  # footnote markers such as "Connecticut 1"
    return POSTAL.get(base)


def num(x):
    x = x.strip()
    return x if re.fullmatch(r"-?\d+(\.\d+)?", x) else ""


def cells(tr):
    return [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]


def parse_old(page, year):
    soup = get(page)
    out = []
    tables = soup.find_all("table")
    subjects = []
    for tb in tables:  # the caption or preceding heading names the subject
        head = (tb.find_previous(["h2", "h3", "h4", "caption", "p"]) or tb).get_text(" ", strip=True).lower()
        cap = tb.find("caption")
        text = (cap.get_text(" ", strip=True).lower() if cap else "") + " " + head
        subjects.append("reading" if "reading" in text else "mathematics" if "math" in text else None)
    if subjects.count(None) or len(set(subjects)) != len(subjects):
        subjects = ["reading", "mathematics"][: len(tables)]  # NCES order: reading, then mathematics
    for tb, subject in zip(tables, subjects):
        for tr in tb.find_all("tr"):
            c = cells(tr)
            if not c or state_of(c[0]) is None:
                continue
            vals = [v for v in c[1:]]
            # layout: g4 equiv, g4 se, (blank), g8 equiv, g8 se, (blank)
            g4, g8 = vals[0:3], vals[3:6]
            for grade, v in ((4, g4), (8, g8)):
                out.append({"year": year, "grade": grade, "subject": subject, "state": state_of(c[0]),
                            "state_label": c[0], "naep_equiv": num(v[0]), "se": num(v[1]) if len(v) > 1 else "",
                            "rel_error": "", "flag": (v[2] if len(v) > 2 else "").strip(), "testing_program": "",
                            "series": "2005-2009 comparison", "source_table": page})
    return out


def parse_new(page, year, grade):
    soup = get(page)
    out = []
    for tb in soup.find_all("table"):
        has_program = "Testing program" in cells(tb.find("tr"))  # 2015 onward
        for tr in tb.find_all("tr"):
            c = cells(tr)
            if not c or state_of(c[0]) is None:
                continue
            rest = c[1:]
            program = ""
            if has_program:
                program, rest = rest[0], rest[1:]
            nums = rest
            # reading: equiv, se, rel [, flag]; mathematics: equiv, se, rel [, flag]
            if len(nums) >= 8:
                rd, mt = nums[0:4], nums[4:8]
            else:
                rd, mt = nums[0:3] + [""], nums[3:6] + [""]
            for subject, v in (("reading", rd), ("mathematics", mt)):
                out.append({"year": year, "grade": grade, "subject": subject, "state": state_of(c[0]),
                            "state_label": c[0], "naep_equiv": num(v[0]), "se": num(v[1]), "rel_error": num(v[2]),
                            "flag": v[3].strip(), "testing_program": "" if program == "†" else program,
                            "series": "per-year report", "source_table": page})
    return out


def main():
    rows = []
    for page, year in OLD.items():
        rows += parse_old(page, year)
    for page, year, grade in NEW:
        rows += parse_new(page, year, grade)
    rows.sort(key=lambda r: (r["year"], r["grade"], r["subject"], r["state"], r["series"]))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    n = {}
    for r in rows:
        if r["naep_equiv"]:
            k = (r["year"], r["grade"], r["subject"], r["series"])
            n[k] = n.get(k, 0) + 1
    for k in sorted(n):
        print(k, n[k])
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()

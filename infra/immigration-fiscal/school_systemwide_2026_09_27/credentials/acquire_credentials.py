"""State graduation-rate panels (ACGR, AFGR) and a sourced exit-exam panel for the credential test.

Downloads NCES Digest HTML tables into credentials/_cache/digest/ (only when absent), parses them
with code (header grid expansion with rowspan/colspan; no hand transcription of numbers), and writes:

  derived/acgr_state.csv               one row per state x cohort x subgroup (latest edition that
                                       reports the cell), with the range across editions
  derived/acgr_state_all_editions.csv  every edition's value (revision audit)
  derived/afgr_state.csv               AFGR, one row per state x school year x sex x race
  derived/afgr_state_all_editions.csv  every edition's value
  derived/digest_footnotes.csv         footnote text by edition and table
  derived/exit_exams.csv               state x graduating class 2003-2024, from the hand-built,
                                       row-cited exit_exam_spells.csv in this directory

Public NCES pages; generic User-Agent; no identifier. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/school_systemwide_2026_09_27/credentials/acquire_credentials.py
"""
import csv
import hashlib
import re
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "digest"
DERIVED = HERE / "derived"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"}
DIGEST = "https://nces.ed.gov/programs/digest/d{ed}/tables/dt{ed}_{table}.asp"

# Table 219.46 (ACGR) exists in editions 2014-2023; each edition adds one subgroup year
# (2023 adds two). Editions 2012, 2013 and 2024 return 404 (probed 2026-09-28).
ACGR_TABLES = [(ed, "219.46") for ed in range(14, 24)]
# Table 219.35 (AFGR, all students): 2013-2019 editions and 2024 (selected years through 2022-23).
# Table 219.40/219.41 (AFGR by sex and race/ethnicity): one school year per table.
AFGR_TABLES = [(ed, "219.35") for ed in (13, 14, 15, 16, 17, 18, 19, 24)] + [
    (13, "219.40"), (14, "219.40"), (15, "219.41"), (15, "219.40"), (16, "219.40"),
    (17, "219.40"), (18, "219.40"), (19, "219.40"), (24, "219.40"),
]

STATE_CODES = {
    "United States": "US", "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    # other jurisdictions, kept with non-state codes
    "Puerto Rico": "PR", "Guam": "GU", "American Samoa": "AS", "Northern Marianas": "MP",
    "U.S. Virgin Islands": "VI", "Bureau of Indian Education": "BIE",
    "Bureau of Indian Education schools": "BIE", "DoD, overseas": "DOD_OVS",
    "DoD, domestic": "DOD_DOM", "DoDEA": "DODEA", "DoDEA, domestic": "DOD_DOM",
    "DoDEA, overseas": "DOD_OVS", "DoDDs: DoDs Overseas": "DOD_OVS",
    "DoDDs: DoDs Domestic": "DOD_DOM", "Commonwealth of the Northern Marianas Islands": "MP",
}

SUBGROUPS = [  # (regex on the leaf header label with spaces and hyphens removed, code)
    (r"^total$", "all"),
    (r"^white$", "white"),
    (r"^black$", "black"),
    (r"^hispanic$", "hispanic"),
    (r"^asian/pacificislander$", "asian_pacific_islander"),
    (r"^asian$", "asian"),
    (r"^pacificislander$", "pacific_islander"),
    (r"^americanindian/alaskanative$", "american_indian_alaska_native"),
    (r"^twoormoreraces$", "two_or_more"),
    (r"^studentswithdisabil", "students_with_disabilities"),
    (r"^(limitedenglishprofi|englishlearner)", "english_learner"),
    (r"^economi", "economically_disadvantaged"),
    (r"^homeless", "homeless"),
    (r"^fostercare$", "foster_care"),
]

FLAG_SYMBOLS = {
    "---": "not_available", "—": "not_available", "--": "not_available",
    "†": "not_applicable", "‡": "reporting_standards_not_met", "#": "rounds_to_zero",
}


def fetch(ed, table):
    path = CACHE / f"dt{ed}_{table}.asp"
    url = DIGEST.format(ed=ed, table=table)
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        for attempt in range(4):
            r = requests.get(url, headers=UA, timeout=120)
            if r.status_code == 200 and b"<table" in r.content:
                path.write_bytes(r.content)
                time.sleep(0.5)
                break
            if r.status_code == 404:
                sys.exit(f"[BLOCKED] {url} returned 404")
            time.sleep(3 * (attempt + 1))
        else:
            sys.exit(f"[BLOCKED] {url} could not be fetched")
    return path, url


def clean(text):
    return " ".join(text.replace("\xa0", " ").split())


def cell_text(cell):
    """Cell text without <sup> footnote markers, and the markers separately."""
    sups = [clean(s.get_text()) for s in cell.find_all("sup")]
    parts = []
    for node in cell.descendants:
        if isinstance(node, str) and not any(p.name == "sup" for p in node.parents if p is not cell):
            parts.append(node)
    return clean(" ".join(parts)), [s for s in sups if s]  # <br> separates words


def parse_footnotes(soup):
    notes = {}
    for cell in soup.find_all(["td", "th", "p", "div"]):
        first = next((c for c in cell.children if not (isinstance(c, str) and not c.strip())), None)
        if getattr(first, "name", None) != "sup":
            continue
        key = clean(first.get_text())
        text = clean(cell.get_text())
        text = text[len(key):].strip() if text.startswith(key) else text
        if key.isdigit() and len(text) > 15 and key not in notes:
            notes[key] = text
    return notes


def is_number_row(texts):
    vals = [t for t in texts if t]
    return len(vals) >= 5 and all(t.isdigit() for t in vals) and vals[0] == "1"


def parse_digest_table(path, first_label="United States"):
    """Return (records, footnotes, title). Each record is one value cell of a data row.

    first_label is the row label that starts the data block (a state table starts with the
    United States row; Table 219.10 starts with its first school year).
    """
    soup = BeautifulSoup(path.read_bytes().decode("utf-8", errors="replace"), "html.parser")
    title = clean(soup.title.get_text()) if soup.title else ""
    tables = [t for t in soup.find_all("table") if len(t.find_all("tr")) > 40]
    if len(tables) != 1:
        sys.exit(f"[BLOCKED] {path.name}: expected one data table, found {len(tables)}")
    rows = tables[0].find_all("tr")
    first_data = next(i for i, r in enumerate(rows)
                      if cell_text(r.find_all(["th", "td"])[0])[0].startswith(first_label))
    header_rows = []
    for r in rows[:first_data]:
        cells = r.find_all(["th", "td"])
        if is_number_row([cell_text(c)[0] for c in cells]):
            continue
        header_rows.append(cells)
    grid = {}
    for ri, cells in enumerate(header_rows):
        ci = 0
        for cell in cells:
            while (ri, ci) in grid:
                ci += 1
            rs, cs = int(cell.get("rowspan", 1) or 1), int(cell.get("colspan", 1) or 1)
            for dr in range(rs):
                for dc in range(cs):
                    if ri + dr < len(header_rows):
                        grid[(ri + dr, ci + dc)] = cell
            ci += cs
    width = max(c for _, c in grid) + 1
    last = len(header_rows) - 1
    columns = []  # per physical column: (path labels, is_value_column, leaf cell)
    for c in range(width):
        col_labels, seen = [], []
        for ri in range(len(header_rows)):
            cell = grid.get((ri, c))
            if cell is not None and cell not in seen:
                seen.append(cell)
                label = cell_text(cell)[0]
                if label:
                    col_labels.append(label)
        leaf = grid.get((last, c))
        is_value = c == 0 or grid.get((last, c - 1)) is not leaf
        columns.append((col_labels, is_value, leaf))
    records = []
    for r in rows[first_data:]:
        cells = r.find_all(["th", "td"])
        spans = sum(int(c.get("colspan", 1) or 1) for c in cells)
        if spans != width or len(cells) < 3:  # separators, section labels, note rows
            continue
        name, name_fn = cell_text(cells[0])
        if not name or not any(cell_text(c)[0] for c in cells[1:]):
            continue  # blank separator or a section label such as "Other jurisdictions"
        phys = []
        for cell in cells:
            phys.extend([cell] * int(cell.get("colspan", 1) or 1))
        c = 1
        while c < width:
            labels, is_value, _ = columns[c]
            if not is_value:
                raise SystemExit(f"[BLOCKED] {path.name}: column {c} misaligned")
            raw, fns = cell_text(phys[c])
            c2 = c + 1
            while c2 < width and not columns[c2][1]:
                extra, extra_fn = cell_text(phys[c2])
                if extra and not extra.isdigit():
                    raise SystemExit(f"[BLOCKED] {path.name} {name}: footnote column {c2} "
                                     f"holds {extra!r}")
                fns += ([extra] if extra else []) + extra_fn
                c2 += 1
            if labels:
                records.append({"name": name, "name_fn": name_fn, "path": labels,
                                "raw": raw, "fns": fns})
            elif raw:
                raise SystemExit(f"[BLOCKED] {path.name} {name}: unlabeled column {c} holds {raw!r}")
            c = c2
    return records, parse_footnotes(soup), title


def parse_value(raw):
    t = raw.replace("≥", ">=").replace("≤", "<=").strip()
    if t == "":
        return "", "blank"
    if t in FLAG_SYMBOLS:
        return "", FLAG_SYMBOLS[t]
    m = re.fullmatch(r"(>=|<=|>|<)\s*(\d+(?:\.\d+)?)", t)
    if m:
        return "", f"blurred_{ {'>=': 'ge', '<=': 'le', '>': 'gt', '<': 'lt'}[m.group(1)] }{m.group(2)}"
    if re.fullmatch(r"\d+(?:\.\d+)?", t):
        return t, ""
    raise SystemExit(f"[BLOCKED] unparsed cell value {raw!r}")


def label_clean(label):
    """Header label without line-break hyphenation ("disabil- ities") or slash spacing."""
    text = re.sub(r"([a-z])- ?([a-z])", r"\1\2", clean(label))
    return re.sub(r"(\w)/ (\w)", r"\1/\2", text)


def fn_join(markers):
    return ";".join(sorted(set(markers), key=lambda m: (len(m), m)))


def subgroup_code(label):
    low = re.sub(r"\s*\d+$", "", clean(label)).lower()
    low = re.sub(r"[\s\-]", "", low)
    for pattern, code in SUBGROUPS:
        if re.search(pattern, low):
            return code
    raise SystemExit(f"[BLOCKED] unknown subgroup label {label!r}")


def year_end(text):
    m = re.search(r"(\d{4})\s*[-–—]\s*(\d{2,4})", text)
    if not m:
        return None
    start = int(m.group(1))
    return start + 1


def state_code(name):
    name = re.sub(r"\s+\d+$", "", name).strip().rstrip(".")  # 2019 table prints "Missouri."
    if name not in STATE_CODES:
        raise SystemExit(f"[BLOCKED] unknown jurisdiction {name!r}")
    return STATE_CODES[name]


def acgr_rows():
    out, notes = [], []
    for ed, table in ACGR_TABLES:
        path, url = fetch(ed, table)
        records, fnotes, title = parse_digest_table(path)
        edition = 2000 + ed
        for k, v in sorted(fnotes.items(), key=lambda kv: int(kv[0])):
            notes.append({"digest_edition": edition, "table": table, "footnote_id": k, "text": v})
        for rec in records:
            group = rec["path"][0]
            leaf = rec["path"][-1]
            if group.startswith("Total, ACGR for all students"):
                cohort, subgroup, label = year_end(leaf), "all", "Total, all students"
            elif group.startswith("ACGR for students with selected characteristics"):
                cohort = year_end(group)
                label = " / ".join(x for x in rec["path"][1:] if x != "Race/ethnicity")
                subgroup = subgroup_code(leaf if leaf != "Total" else rec["path"][-2])
            else:
                raise SystemExit(f"[BLOCKED] unexpected ACGR header {rec['path']}")
            if cohort is None:
                raise SystemExit(f"[BLOCKED] no year in {rec['path']}")
            rate, flag = parse_value(rec["raw"])
            out.append({
                "state": state_code(rec["name"]), "cohort_end_year": cohort,
                "school_year": f"{cohort - 1}-{str(cohort)[2:]}", "subgroup": subgroup,
                "subgroup_label": label_clean(label), "rate": rate, "rate_flag": flag,
                "rate_raw": rec["raw"],
                "footnotes": fn_join(rec["name_fn"] + rec["fns"]),
                "digest_edition": edition, "table": table, "source_url": url,
            })
    return out, notes


def afgr_rows():
    out, notes = [], []
    for ed, table in AFGR_TABLES:
        path, url = fetch(ed, table)
        records, fnotes, title = parse_digest_table(path)
        edition = 2000 + ed
        for k, v in sorted(fnotes.items(), key=lambda kv: int(kv[0])):
            notes.append({"digest_edition": edition, "table": table, "footnote_id": k, "text": v})
        title_year = year_end(title.split(":")[-1]) if table != "219.35" else None
        for rec in records:
            p = rec["path"]
            if table == "219.35":
                year, sex, race = year_end(p[-1]), "total", "all"
            else:
                if p[0].startswith("Number of public high school graduates"):
                    continue
                if p[0].startswith("Averaged freshman graduation rate"):
                    sex = "total"
                else:
                    sex = {"Total, male and female": "total", "Male": "male",
                           "Female": "female"}[p[0]]
                race = subgroup_code(p[-1])
                year = title_year
            if year is None:
                raise SystemExit(f"[BLOCKED] no year for {table} d{ed} {p}")
            rate, flag = parse_value(rec["raw"])
            out.append({
                "state": state_code(rec["name"]), "school_year_end": year,
                "school_year": f"{year - 1}-{str(year)[2:]}", "sex": sex, "subgroup": race,
                "subgroup_label": ("Total, all students" if table == "219.35"
                                   else label_clean(p[-1])), "rate": rate, "rate_flag": flag,
                "rate_raw": rec["raw"],
                "footnotes": fn_join(rec["name_fn"] + rec["fns"]),
                "digest_edition": edition, "table": table, "source_url": url,
            })
    out.extend(ccd_afgr_rows())
    return out, notes


CCD_AFGR_URL = "https://nces.ed.gov/ccd/tables/AFGR.asp"


def ccd_afgr_rows():
    """CCD table: AFGR by race/ethnicity, sex and state, 2002-03 through 2008-09.

    Layout differs from the Digest: a jurisdiction row with no values, then one row per year.
    """
    path = HERE / "_cache" / "ccd" / "AFGR.asp"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(CCD_AFGR_URL, headers=UA, timeout=600)
        if r.status_code != 200 or b"<table" not in r.content:
            sys.exit(f"[BLOCKED] {CCD_AFGR_URL} returned {r.status_code}")
        path.write_bytes(r.content)
    soup = BeautifulSoup(path.read_bytes().decode("utf-8", errors="replace"), "html.parser")
    table = [t for t in soup.find_all("table") if len(t.find_all("tr")) > 40]
    if len(table) != 1:
        sys.exit("[BLOCKED] CCD AFGR.asp: expected one data table")
    rows = table[0].find_all("tr")
    groups, sexes = [], []
    for cell in rows[0].find_all(["th", "td"]):
        groups.extend([cell_text(cell)[0]] * int(cell.get("colspan", 1) or 1))
    for cell in rows[1].find_all(["th", "td"]):
        sexes.extend([cell_text(cell)[0]] * int(cell.get("colspan", 1) or 1))
    if len(groups) != len(sexes):
        sys.exit("[BLOCKED] CCD AFGR.asp: header widths differ")
    race_map = {"All races/ethnicities": "all", "American Indian/Alaska Native":
                "american_indian_alaska_native", "Asian/Pacific Islander": "asian_pacific_islander",
                "Hispanic": "hispanic", "Black": "black", "White": "white"}
    out, current = [], None
    for r in rows[2:]:
        cells = r.find_all(["th", "td"])
        if len(cells) != len(groups):
            continue
        name, name_fn = cell_text(cells[0])
        values = [cell_text(c) for c in cells[1:]]
        if name and not any(v[0] for v in values):
            current = ("US_REPORTING" if name.startswith("Reporting States") else
                       state_code(name), name_fn)
            continue
        year = year_end(name)
        if current is None or year is None:
            continue
        for col, (raw, fns) in enumerate(values, start=1):
            if not groups[col] or not sexes[col]:
                if raw:
                    sys.exit(f"[BLOCKED] CCD AFGR.asp: unlabeled column {col} holds {raw!r}")
                continue
            rate, flag = parse_value(raw)
            out.append({
                "state": current[0], "school_year_end": year,
                "school_year": f"{year - 1}-{str(year)[2:]}", "sex": sexes[col].lower(),
                "subgroup": race_map[groups[col]], "subgroup_label": groups[col],
                "rate": rate, "rate_flag": flag, "rate_raw": raw,
                "footnotes": fn_join(current[1] + fns), "digest_edition": "",
                "table": "CCD AFGR.asp", "source_url": CCD_AFGR_URL,
            })
    return out


def source_rank(r):
    """Digest editions outrank the CCD web table; within an edition 219.35 outranks 219.40."""
    edition = r["digest_edition"] if r["digest_edition"] != "" else 0
    return (edition, 1 if r["table"] == "219.35" else 0)


def preferred(rows, keys):
    """Latest edition with a reported value per cell; the range across editions for audit."""
    cells = defaultdict(list)
    for r in rows:
        cells[tuple(r[k] for k in keys)].append(r)
    out = []
    for key, group in cells.items():
        group.sort(key=source_rank)
        reported = [r for r in group if r["rate"] != "" or r["rate_flag"].startswith("blurred")]
        best = dict((reported or group)[-1])
        nums = [float(r["rate"]) for r in group if r["rate"] != ""]
        best["n_editions"] = len({r["digest_edition"] for r in group})
        best["rate_min_editions"] = f"{min(nums):g}" if nums else ""
        best["rate_max_editions"] = f"{max(nums):g}" if nums else ""
        out.append(best)
    return out


def validate_national(acgr, afgr):
    """Compare the parsed national series with Digest 2024 Table 219.10, a separate table.

    219.10 prints the national ACGR to one decimal; 219.46 prints integers, so the check is
    that 219.10 rounded half-up equals the 219.46 integer. AFGR must match exactly.
    """
    path, url = fetch(24, "219.10")
    records, _, _ = parse_digest_table(path, first_label="1869-70")
    t1910 = {}
    for rec in records:
        year = year_end(rec["name"])
        label = " ".join(rec["path"])
        for measure, tag in (("acgr", "Public school ACGR"), ("afgr", "Public school AFGR")):
            if tag in label and year is not None:
                rate, _ = parse_value(rec["raw"])
                if rate:
                    t1910[(measure, year)] = rate
    ours = {("acgr", r["cohort_end_year"]): r["rate"] for r in acgr
            if r["state"] == "US" and r["subgroup"] == "all"}
    ours.update({("afgr", r["school_year_end"]): r["rate"] for r in afgr
                 if r["state"] == "US" and r["sex"] == "total" and r["subgroup"] == "all"})
    out, bad = [], []
    for (measure, year), value in sorted(t1910.items()):
        if (measure, year) not in ours or ours[(measure, year)] == "":
            continue
        mine = ours[(measure, year)]
        if measure == "acgr":
            rounded = int(float(value) + 0.5)
            ok = rounded == int(mine)
        else:
            ok = float(value) == float(mine)
        out.append({"measure": measure, "school_year_end": year, "parsed_state_table": mine,
                    "digest_2024_table_219_10": value, "match": int(ok), "source_url": url})
        if not ok:
            bad.append((measure, year, mine, value))
    if bad:
        sys.exit(f"[BLOCKED] national series disagree with Table 219.10: {bad}")
    return out


def write_csv(path, rows, fields, sort_keys):
    rows = sorted(rows, key=lambda r: tuple(str(r[k]) if not isinstance(r[k], int) else f"{r[k]:06d}"
                                            for k in sort_keys))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.relative_to(HERE)}: {len(rows)} rows")


# Digest Table 234.30: state exit-exam requirement snapshots, parsed with code. The 2013 edition
# cites the EPE Research Center (retrieved August 2013); the 2022 edition cites ECS (February 2019).
EXIT_SNAPSHOTS = [(13, "234.30"), (22, "234.30")]


def exit_exam_snapshots():
    out = []
    for ed, table in EXIT_SNAPSHOTS:
        path, url = fetch(ed, table)
        records, fnotes, title = parse_digest_table(path, first_label="Alabama")
        year = int(re.search(r"(\d{4})\s*$", title).group(1))
        cells = defaultdict(dict)
        for rec in records:
            label = " ".join(rec["path"])
            st = state_code(rec["name"])
            fns = rec["name_fn"] + rec["fns"]
            for key, tag in (("exit_exam_required", "Exit exam required for standard diploma"),
                             ("subjects_tested", "Subjects tested"),
                             ("appeals_or_alternative", "Appeals or alternative route")):
                if tag in label:
                    cells[st][key] = rec["raw"]
                    cells[st].setdefault("fns", []).extend(fns)
        for st, c in cells.items():
            if "exit_exam_required" not in c:
                continue
            markers = sorted(set(c.get("fns", [])), key=lambda m: (len(m), m))
            out.append({
                "state": st, "snapshot_year": year, "exit_exam_required": c["exit_exam_required"],
                "subjects_tested": c.get("subjects_tested", ""),
                "appeals_or_alternative": c.get("appeals_or_alternative", ""),
                "footnotes": "; ".join(f"{m}: {fnotes.get(m, '')}" for m in markers),
                "digest_edition": 2000 + ed, "source_url": url,
            })
    return out


# Exit-exam panel. exit_exam_spells.csv (this directory) is hand-built: one row per state spell of
# graduating classes, each citing a source URL and a verbatim quote (a second source where one is
# needed or where sources conflict). The script downloads every cited source into
# _cache/exit/sources/ when absent, extracts its text, and stops with [BLOCKED] if any quote is not
# found in the text of its source. Coding rule for exam_required (CEP's definition): 1 when the
# default route to a standard diploma for that class requires passing a state test, even where
# appeals, substitute tests, portfolios or other alternatives exist (requirement_type says which);
# 0 when no state test must be passed. COVID-19 waivers are recorded in covid_waiver, not in
# exam_required.
EXIT_SOURCES = HERE / "_cache" / "exit" / "sources"
EXIT_YEARS = range(2003, 2025)
SPELL_FIELDS = ["state", "first_class", "last_class", "exam_required", "requirement_type",
                "exam_name", "change_note", "retroactive", "covid_waiver", "status",
                "source_url", "source_locator", "source_quote",
                "source2_url", "source2_locator", "source2_quote"]
EXIT_FIELDS = ["state", "class_year", "exam_required", "requirement_type", "exam_name",
               "change_note", "retroactive", "covid_waiver", "status", "source_url",
               "source_locator", "source_quote", "source2_url", "source2_locator",
               "source2_quote", "digest_snapshot", "snapshot_agrees"]
CURL_UA = UA["User-Agent"]
QUOTE_MAP = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                           "–": "-", "—": "-", "­": "", " ": " "})


def curl_get(url, out):
    r = subprocess.run(["curl", "-sS", "-L", "-m", "90", "-A", CURL_UA, "-H", "Accept: */*",
                        "-o", str(out), "-w", "%{http_code}", url], capture_output=True, text=True)
    return r.stdout.strip()


def source_texts(url):
    """Download a cited source once (Wayback id_ copy if the site refuses) and return its texts."""
    h = hashlib.sha1(url.encode()).hexdigest()[:16]
    raw = next((p for p in EXIT_SOURCES.glob(h + ".*") if p.suffix in (".pdf", ".html")), None)
    if raw is None:
        EXIT_SOURCES.mkdir(parents=True, exist_ok=True)
        tmp = EXIT_SOURCES / (h + ".tmp")
        code, via = curl_get(url, tmp), "direct"
        body = tmp.read_bytes() if tmp.exists() else b""
        if code != "200" or len(body) < 2000 or b"Just a moment" in body[:5000]:
            code, via = curl_get("https://web.archive.org/web/2025id_/" + url, tmp), "wayback"
            body = tmp.read_bytes() if tmp.exists() else b""
        if code != "200" or len(body) < 2000:
            sys.exit(f"[BLOCKED] cited source unreachable ({code}): {url}")
        raw = EXIT_SOURCES / (h + (".pdf" if body[:4] == b"%PDF" else ".html"))
        tmp.rename(raw)
        (EXIT_SOURCES / (h + ".url")).write_text(f"{url}\n{via}\n")
    texts = []
    if raw.suffix == ".pdf":
        for mode, suffix in (([], ".txt"), (["-layout"], ".layout.txt")):
            txt = EXIT_SOURCES / (h + suffix)
            if not txt.exists():
                subprocess.run(["pdftotext", *mode, str(raw), str(txt)], check=True)
            texts.append(txt.read_text(errors="replace"))
    else:
        txt = EXIT_SOURCES / (h + ".txt")
        if not txt.exists():
            soup = BeautifulSoup(raw.read_bytes().decode("utf-8", "replace"), "html.parser")
            for t in soup(["script", "style"]):
                t.decompose()
            txt.write_text(soup.get_text("\n", strip=True))
        texts.append(txt.read_text(errors="replace"))
    via = (EXIT_SOURCES / (h + ".url")).read_text().split("\n")[1]
    return texts, raw.name, via


def norm_text(s):
    s = unicodedata.normalize("NFKC", s).translate(QUOTE_MAP)
    return " ".join(s.split()).lower()


def quote_found(quote, texts):
    q = norm_text(quote)
    dehyphen = lambda s: re.sub(r"(\w)- (\w)", r"\1\2", s)
    for t in texts:
        t = norm_text(t)
        if q in t or dehyphen(q) in dehyphen(t):
            return True
    return False


def load_spells():
    with (HERE / "exit_exam_spells.csv").open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != SPELL_FIELDS:
            sys.exit(f"[BLOCKED] exit_exam_spells.csv header {reader.fieldnames} != {SPELL_FIELDS}")
        spells = list(reader)
    for s in spells:
        if s["exam_required"] not in ("0", "1") or not s["source_url"] or not s["source_quote"]:
            sys.exit(f"[BLOCKED] spell lacks a 0/1 code, a source or a quote: {s['state']} "
                     f"{s['first_class']}-{s['last_class']}")
    return spells


def verify_quotes(spells):
    checks, missing = [], []
    for i, s in enumerate(spells):
        for tag in ("source", "source2"):
            url, quote = s[f"{tag}_url"], s[f"{tag}_quote"]
            if not url:
                continue
            texts, cache_name, via = source_texts(url)
            ok = quote_found(quote, texts)
            checks.append({"spell": i + 1, "state": s["state"], "first_class": s["first_class"],
                           "last_class": s["last_class"], "which": tag, "url": url,
                           "cache_file": cache_name, "fetched_via": via,
                           "quote_found": int(ok)})
            if not ok:
                missing.append(f"{s['state']} {s['first_class']}-{s['last_class']} {tag}: {quote[:80]}")
    if missing:
        sys.exit("[BLOCKED] quotes not found in their cited sources:\n  " + "\n  ".join(missing))
    return checks


def exit_exam_rows(spells, snapshots):
    """Expand the cited spells to one row per state x graduating class 2003-2024."""
    snap = {(r["state"], r["snapshot_year"]): r["exit_exam_required"] for r in snapshots}
    states = sorted(v for v in STATE_CODES.values() if len(v) == 2 and v not in
                    ("US", "PR", "GU", "AS", "MP", "VI"))
    by_state = defaultdict(list)
    for s in spells:
        if s["state"] not in states:
            sys.exit(f"[BLOCKED] unknown state in spells: {s['state']}")
        by_state[s["state"]].append(s)
    out = []
    for st in states:
        for year in EXIT_YEARS:
            hits = [s for s in by_state[st] if int(s["first_class"]) <= year <= int(s["last_class"])]
            if len(hits) > 1:
                sys.exit(f"[BLOCKED] overlapping spells for {st} {year}")
            if not hits:
                sys.exit(f"[BLOCKED] no cited spell covers {st} class of {year}")
            row = {k: hits[0][k] for k in EXIT_FIELDS if k in hits[0]}
            row.update(state=st, class_year=year, digest_snapshot="", snapshot_agrees="")
            # Digest 234.30 snapshots: EPE (Aug 2013) for the class of 2013, ECS (Feb 2019) for 2019
            if (st, year) in snap:
                row["digest_snapshot"] = snap[(st, year)]
                row["snapshot_agrees"] = int((snap[(st, year)] == "Yes") == (row["exam_required"] == "1"))
            out.append(row)
    return out


def main():
    acgr, acgr_notes = acgr_rows()
    fields = ["state", "cohort_end_year", "school_year", "subgroup", "subgroup_label", "rate",
              "rate_flag", "rate_raw", "footnotes", "digest_edition", "table", "source_url"]
    keys = ["state", "cohort_end_year", "subgroup"]
    write_csv(DERIVED / "acgr_state_all_editions.csv", acgr, fields, keys + ["digest_edition"])
    write_csv(DERIVED / "acgr_state.csv", preferred(acgr, keys),
              fields + ["n_editions", "rate_min_editions", "rate_max_editions"], keys)
    afgr, afgr_notes = afgr_rows()
    afields = ["state", "school_year_end", "school_year", "sex", "subgroup", "subgroup_label",
               "rate", "rate_flag", "rate_raw", "footnotes", "digest_edition", "table",
               "source_url"]
    akeys = ["state", "school_year_end", "sex", "subgroup"]
    write_csv(DERIVED / "afgr_state_all_editions.csv", afgr, afields,
              akeys + ["digest_edition", "table"])
    write_csv(DERIVED / "afgr_state.csv", preferred(afgr, akeys),
              afields + ["n_editions", "rate_min_editions", "rate_max_editions"], akeys)
    write_csv(DERIVED / "validation_national.csv", validate_national(acgr, afgr),
              ["measure", "school_year_end", "parsed_state_table", "digest_2024_table_219_10",
               "match", "source_url"], ["measure", "school_year_end"])
    write_csv(DERIVED / "digest_footnotes.csv", acgr_notes + afgr_notes,
              ["digest_edition", "table", "footnote_id", "text"],
              ["table", "digest_edition", "footnote_id"])
    snapshots = exit_exam_snapshots()
    write_csv(DERIVED / "exit_exam_digest_snapshots.csv", snapshots,
              ["state", "snapshot_year", "exit_exam_required", "subjects_tested",
               "appeals_or_alternative", "footnotes", "digest_edition", "source_url"],
              ["snapshot_year", "state"])
    if not (HERE / "exit_exam_spells.csv").exists():
        print("[SKIPPED] class-by-class exit-exam panel: exit_exam_spells.csv was never finished "
              "(NOTES_credentials.md), so derived/exit_exams.csv is not built", file=sys.stderr)
        return
    spells = load_spells()
    write_csv(DERIVED / "exit_exam_quote_checks.csv", verify_quotes(spells),
              ["spell", "state", "first_class", "last_class", "which", "url", "cache_file",
               "fetched_via", "quote_found"], ["spell", "which"])
    write_csv(DERIVED / "exit_exams.csv", exit_exam_rows(spells, snapshots), EXIT_FIELDS,
              ["state", "class_year"])


if __name__ == "__main__":
    main()

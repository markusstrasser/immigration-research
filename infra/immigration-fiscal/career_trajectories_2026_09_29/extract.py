"""Select the NLSY97 fields this lane needs from the full 1997–2023 public archive.

Verifies the archive hash, indexes every codebook header, selects fields by question name and
survey year (never by guessed reference number), checks that each extracted field has the
codebook's count of non-skipped values, and writes the field inventory (tracked) and the selected
microdata (ignored `_cache/`).
"""
import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

import pandas as pd

LANE = Path(__file__).resolve().parent
ARCHIVE = _data_paths.reused_surveys_root(require_exists=False) / "nlsy/nlsy97_all_1997-2023.zip"
SHA256 = "8c513e4804e5b07fce0e6b913258747dcf8707c73bb9ae54cce88dbff6d23c28"
# Reference number -> (question name, short name); asserted against the codebook below.
PERSON = {
    "R0000100": ("PUBID", "pubid"), "R0536300": ("KEY!SEX", "sex"),
    "R0536401": ("KEY!BDATE_M", "birth_month"), "R0536402": ("KEY!BDATE_Y", "birth_year"),
    "R0538600": ("KEY!ETHNICITY", "key_hispanic"), "R0538700": ("KEY!RACE", "key_race"),
    "R1482600": ("KEY!RACE_ETHNICITY", "race_ethnicity"), "R1235800": ("CV_SAMPLE_TYPE", "sample_type"),
    "R1489700": ("VSTRAT", "vstrat"), "R1489800": ("VPSU", "vpsu"),
    "R9829600": ("ASVAB_MATH_VERBAL_SCORE_PCT", "afqt_pct"),
    "R9702300": ("ASVAB_ETH_ORIGIN.01", "origin_1"), "R9702400": ("ASVAB_ETH_ORIGIN.02", "origin_2"),
    "R9702500": ("ASVAB_ETH_ORIGIN.03", "origin_3"),
    "Z9085100": ("CVC_RND", "last_round"), "Z9083900": ("CVC_HIGHEST_DEGREE_EVER", "degree_last"),
}
# Question name -> short-name stem; one field per survey round. Income questions ask about the
# calendar year before the interview round ("During 2022 ..." in round 21, 2023).
BY_ROUND = {
    "SAMPLING_WEIGHT_CC": "weight", "YINC-1400": "wage_any", "YINC-1700": "wage",
    "YINC-1800": "wage_bracket", "YINC-2000": "bus_any", "YINC-2100": "bus", "YINC-2200": "bus_bracket",
    "CV_HIGHEST_DEGREE_EVER_EDT": "degree", "CV_HGC_EVER_EDT": "hgc",
}
# Created from the weekly event history for every calendar year, interviewed that round or not.
BY_CALENDAR = {"CVC_WKSWK_YR_ALL": "weeks", "CVC_HOURS_WK_YR_ALL": "hours"}
CAL_YEARS = range(1996, 2024)

with ARCHIVE.open("rb") as fh:
    digest = hashlib.file_digest(fh, "sha256").hexdigest()
assert digest == SHA256, f"Unverified archive {digest}"

header = re.compile(r"^([A-Z]\d{5})\.(\d{2})\s+\[([^\]]+)\]\s+Survey Year:\s*(\S+)")
total = re.compile(r"TOTAL =+>\s+(\d+)")
index, cur, state = [], None, 0
with zipfile.ZipFile(ARCHIVE) as z, z.open("nlsy97_all_1997-2023.cdb") as fh:
    for raw in fh:
        line = raw.decode("utf-8", "replace").rstrip("\n")
        m = header.match(line)
        if m:
            cur = dict(ref=m[1] + m[2], qname=m[3], year=m[4], title="", total=None)
            index.append(cur); state = 1; continue
        if cur is None:
            continue
        if state == 1 and line.strip() and "VARIABLE" not in line:
            cur["title"] = line.strip(); state = 2
        elif cur["total"] is None and (t := total.search(line)):
            cur["total"] = int(t[1])
by_ref = {r["ref"]: r for r in index}

rows = []
for ref, (qname, short) in PERSON.items():
    assert by_ref[ref]["qname"] == qname, (ref, by_ref[ref]["qname"], qname)
    rows.append(dict(role="person", short=short, **by_ref[ref]))
for r in index:
    if r["qname"] in BY_ROUND and r["year"].isdigit():
        rows.append(dict(role="round", short=f"{BY_ROUND[r['qname']]}_{r['year']}", **r))
    stem, _, yy = r["qname"].partition(".")
    if stem in BY_CALENDAR and yy.isdigit():
        year = (1900 if int(yy) >= 80 else 2000) + int(yy)
        if year in CAL_YEARS:
            rows.append(dict(role="calendar", short=f"{BY_CALENDAR[stem]}_{year}", **r))
shorts = [r["short"] for r in rows]
assert len(shorts) == len(set(shorts)), "duplicate field per round"
refs = [r["ref"] for r in rows]

with zipfile.ZipFile(ARCHIVE) as z, z.open("nlsy97_all_1997-2023.csv") as fh:
    data = pd.read_csv(fh, usecols=refs, low_memory=False)
assert len(data) == 8984 and data["R0000100"].is_unique
for r in rows:
    r["extracted_not_skipped"] = int((~data[r["ref"]].isin([-4, -5])).sum())
    r["matches_codebook"] = r["extracted_not_skipped"] == r["total"]
bad = [r["short"] for r in rows if not r["matches_codebook"]]
assert not bad, f"extracted counts differ from codebook: {bad}"

data = data[refs].rename(columns=dict(zip(refs, shorts))).sort_values("pubid").reset_index(drop=True)
cache = LANE / "_cache"; cache.mkdir(exist_ok=True)
data.to_parquet(cache / "nlsy_selected.parquet", index=False)
(LANE / "derived").mkdir(exist_ok=True)
with open(LANE / "derived/field_inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["role", "field", "ref", "question_name", "survey_year", "title", "codebook_not_skipped",
                "extracted_not_skipped"])
    for r in sorted(rows, key=lambda r: (r["role"], r["short"])):
        w.writerow([r["role"], r["short"], r["ref"], r["qname"], r["year"], r["title"], r["total"],
                    r["extracted_not_skipped"]])
(LANE / "derived/extraction.json").write_text(json.dumps(dict(
    archive=str(ARCHIVE.relative_to(ARCHIVE.parents[2])), sha256=digest, bytes=ARCHIVE.stat().st_size,
    codebook_variables=len(index), selected_fields=len(rows), respondents=len(data)), indent=2) + "\n")
print(f"codebook variables {len(index)}; selected {len(rows)} fields; {len(data)} respondents")

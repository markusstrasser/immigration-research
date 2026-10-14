#!/usr/bin/env python3
"""National taxes on the business capital that serves jobs, by line and industry cell (job-capital taxes lane).

The three lines are the case's (assumption_explorer_2026_09_21/derived/model.json, 2024): business property, the
property tax line net of the CPS-modeled owner line and the BEA tenant split (273.445297bn), other production
taxes (145.258bn) and taxes on corporate income (663.685bn). Each line's national amount is spread over BEA
summary industries; the lane's industry pattern comes from primary tables parsed here, and the amounts always sum
to the model's line.

  corporate     NIPA Table 6.18D (taxes on corporate income by industry; 2026 annual update): 2024 sector totals,
                spread within a sector by its 2023 detail (2024 has no detail); retail by the 2024 supply-use
                table's gross operating surplus of its four summary industries; hospitals and nursing homes, one
                6.18D line, by the same. Management of companies (6.18D footnote: "bank and other holding companies")
                is pro rata to the other private cells (beside: kept at NAICS 55). The 6.18D total (660.908bn) is a
                later vintage than the model's NIPA 3.1 line 5 (663.685bn): the pattern is 6.18D's, the level the
                model's.
  business      The 2024 summary use table's other taxes on production (T00OTOP) by industry, housing (HS) left
  property      out: BEA's estimate of what each industry pays in property taxes, special assessments and licenses
                (NIPA's other taxes on production less housing, about three quarters of it business property on
                BEA's housing split).
                Beside: private nonresidential structures by industry (Fixed Assets Table 3.1S, 2024 yearend,
                current cost, nonprofit structures removed), with and without equipment at the tangible personal
                property share of property taxes (Tax Foundation's national estimate).
  other         NIPA Table 3.5 components: licenses and the rest (federal other, motor vehicle and other licenses,
  production    state and local "other") by the same T00OTOP pattern; severance by the mining industries' taxes on
                products (T00TOP); documentary and stamp taxes and special assessments split between residential
                and business real estate by Z.1 market value, the business part by the T00OTOP pattern and the
                residential part to a RESIDENTIAL cell outside the item (homes are items 2 and 3's).
Lessors: what real-estate (ORE) and rental-and-leasing (532RL) firms pay on capital their tenants use goes to the
using industries in proportion to their purchases of the lessor's commodity (the use table's intermediate uses,
self-use netted out by solving the two lessors' cross purchases); the part sold to final demand and to housing
stays with the lessor's own jobs.

Also measured here for the job lane: lambda_b, the land share of business real estate (Z.1 market value against
current-cost structures); tau, the tangible personal property share of the business property line; the federal
tax on foreign-source income by industry (IRS SOI Corporate Foreign Tax Credit, Tax Year 2021, Table 1 column 19,
over Publication 5655's total income tax after credits); and the normal-return share of the corporate tax (Treasury
OTA Technical Paper 5), with its later measurements by period and by industry (Power and Frerick, OTA Working Paper
111), each cell at its industry's share (pf_normal_share).

Gates (exit 1, nothing written): every pinned file's sha256; table labels where read; NIPA components add to the
model's lines (1e-6 bn); 6.18D details add to sectors (2023) and sectors to the total (2024); the use table's
industries add to its totals; Table 1 column 19's major industries add to all industries and equal column 18 less
column 2 within 0.01%; every line's cells add to its national amount (1e-6 bn); no housing tax enters a line's
industry cells; no cell is negative.

  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
      infra/immigration-fiscal/job_capital_taxes_2026_10_14/national.py [--out-dir DIR]
Outputs: derived/national_by_industry.csv, derived/national.json.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = REPO / "infra/immigration-fiscal"
CACHE = HERE / "_cache"
PINS = json.loads((HERE / "inputs/pins.json").read_text())
NIPA3 = REPO / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
NIPA3_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
TP5 = REPO / "sources/immigration-fiscal/data/external/corporate_incidence/TP-5.pdf"
TP5_SHA = "48a3a3e48f1ff50102527791c322d0e5d9c2443282c3a58ca9fd98abe0b55c4c"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
HOUSING = FISCAL / "receipt_side_long_run_2026_09_28/derived/housing.json"
YEAR = "2024"

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'✓' if ok else '✗'} {name}{f' ({detail})' if detail else ''}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pinned(name: str) -> Path:
    path = CACHE / name
    if not path.exists() or sha256(path) != PINS[name]["sha256"]:
        raise SystemExit(f"[BLOCKED] {name}: missing or changed (run acquire.py)")
    return path


def checked(path: Path, digest: str) -> Path:
    if not path.exists() or sha256(path) != digest:
        raise SystemExit(f"[BLOCKED] {path}: missing or changed")
    return path


# ---------------------------------------------------------------------------------------------------------------
# Readers. BEA NIPA and Fixed Assets workbooks share one layout: a header row whose first cell is "Line", then
# (line, label, code, values by year).
def clean(label) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\\\d+(,\d+)*\\", "", str(label))).strip()


def bea_sheet(book, sheet: str) -> dict:
    rows = list(book[sheet].values)
    head = next(i for i, r in enumerate(rows) if r and r[0] == "Line")
    years = [str(y) for y in rows[head]]
    title = " ".join(str(v) for r in rows[:head] for v in r if v is not None)
    out = {"title": title, "lines": {}}
    for r in rows[head + 1:]:
        if r is None or r[0] is None or not str(r[0]).strip().isdigit():
            continue
        vals = {y: v for y, v in zip(years, r) if y.isdigit()}
        out["lines"][int(r[0])] = (clean(r[1]), str(r[2]), vals)
    return out


def value(table: dict, line: int, label: str, year: str = YEAR) -> float:
    got, _, vals = table["lines"][line]
    if got != label:
        raise SystemExit(f"[BLOCKED] line {line} reads {got!r}, expected {label!r}")
    v = vals[year]
    if not isinstance(v, (int, float)):
        raise SystemExit(f"[BLOCKED] line {line} ({label}) {year}: {v!r}")
    return float(v)


def pdf_text(path: Path) -> str:
    r = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, check=True)
    return r.stdout.decode("utf-8", errors="replace")


def money(token: str) -> float:
    return float(token.replace("*", "").replace(",", ""))


NUM = r"\*?-?[\d,]+(?:\.\d+)?|d"
ROW = re.compile(rf"^(?P<label>.*?[A-Za-z)\]])\s+(?P<nums>(?:(?:{NUM})\s+)*(?:{NUM}))$")


def soi_rows(page: str) -> dict:
    """An SOI table page as {row label: number tokens}; a label printed over two lines (its second starting in lower
    case) is joined."""
    rows, pending = {}, None
    for ln in page.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = ROW.match(s)
        if m and re.search(r"\d", m.group("nums")):
            label = re.sub(r"\s+", " ", m.group("label")).strip()
            if pending and label[:1].islower():
                label = f"{pending} {label}"
            rows.setdefault(label, m.group("nums").split())
            pending = None
        else:
            pending = re.sub(r"\s+", " ", s) if re.match(r"^[A-Z]", s) else None
    return rows


# ---------------------------------------------------------------------------------------------------------------
# Cells: the summary use table's industries, housing out, NAICS 525 with 523 (Census codes them together), the
# federal and the state and local governments each one cell, private households (no business capital) and a
# RESIDENTIAL cell for the residential parts of two other-production components.
SUT_TO_CELL = {"525": "523", "GFGD": "GOVF", "GFGN": "GOVF", "GFE": "GOVF", "GSLG": "GOVSL", "GSLE": "GOVSL"}
LESSORS = ("ORE", "532RL")
EXTRA_CELLS = ["HH814", "RESIDENTIAL"]
# Power and Frerick (OTA Working Paper 111) Table 1: the risk-free (normal-return) share of the corporate base by
# industry, 2011-2013, and each industry's share of 2013 worldwide book income; finance, rental and real estate are
# out. The cells' industries [INFERENCE]: the table lists industries in NAICS order and its income shares add to
# 1.01, so it covers every corporate industry but those three; Fossil Fuel, between nondurable and chemical
# manufacturing, is petroleum and coal products (324), and the durable cells other than computers and electronics
# (334) are Metal and Machinery. Agriculture, finance, real estate and rental, government and the households cell
# take the paper's 2003-2013 average for all C corporations.
PF_MAJOR = ["Mining", "Utilities", "Construction", "Nondurable Manufacturing", "Fossil Fuel", "Chemical Manufacturing", "Technology",
            "Metal and Machinery Manufacturing", "Wholesale and Retail Trade", "Transportation and Warehousing", "Information", "Service"]
PF_MINOR = ["Pharmaceuticals", "Software"]
PF_INDUSTRY = {"211": "Mining", "212": "Mining", "213": "Mining", "22": "Utilities", "23": "Construction",
               **{c: "Nondurable Manufacturing" for c in ("311FT", "313TT", "315AL", "322", "323", "326")}, "324": "Fossil Fuel",
               "325": "Chemical Manufacturing", "334": "Technology",
               **{c: "Metal and Machinery Manufacturing" for c in ("321", "327", "331", "332", "333", "335", "3361MV", "3364OT", "337", "339")},
               **{c: "Wholesale and Retail Trade" for c in ("42", "441", "445", "452", "4A0")},
               **{c: "Transportation and Warehousing" for c in ("481", "482", "483", "484", "485", "486", "487OS", "493")},
               **{c: "Information" for c in ("511", "512", "513", "514")},
               **{c: "Service" for c in ("5411", "5415", "5412OP", "55", "561", "562", "61", "621", "622", "623", "624", "711AS", "713",
                                         "721", "722", "81")}}


def read_use(zpath: Path):
    with zipfile.ZipFile(zpath) as z:
        book = openpyxl.load_workbook(io.BytesIO(z.read("Use_Summary.xlsx")), read_only=True, data_only=True)
    rows = list(book[YEAR].values)
    gate("use table: the 2024 sheet's title and units", str(rows[0][0]).startswith("The Use of Commodities by Industries")
         and str(rows[1][0]) == "(Millions of dollars)" and str(rows[3][0]) == YEAR)
    codes = [str(c) if c is not None else None for c in rows[5]]
    t001 = codes.index("T001")
    industries = codes[2:t001]
    data = {str(r[0]): r for r in rows[7:] if r[0] is not None}

    def num(v, where):
        if isinstance(v, (int, float)):
            return float(v)
        if v in ("...", None):
            return 0.0
        raise SystemExit(f"[BLOCKED] use table {where}: {v!r}")

    def row(code):
        r = data[code]
        return {c: num(r[j], f"{code}/{c}") for j, c in enumerate(codes) if c is not None and j >= 2}

    return industries, row


def lessor_shares(industries, use_row):
    """For each lessor, the share of its non-self use bought by each other industry (housing and final uses stay)."""
    shares = {}
    for lessor in LESSORS:
        u = use_row(lessor)
        inter = sum(u[c] for c in industries)
        final = sum(v for c, v in u.items() if c.startswith("F"))
        tol = 0.5 * len(industries)
        gate(f"use table: {lessor}'s industry uses add to its intermediate total (rounding, {tol:.1f} $mn)",
             abs(inter - u["T001"]) <= tol, f"{inter:,.0f} vs {u['T001']:,.0f}")
        gate(f"use table: {lessor}'s intermediate and final uses add to its total use (rounding)",
             abs(inter + final - u["T019"]) <= tol, f"{inter + final:,.0f} vs {u['T019']:,.0f}")
        denom = inter + final - u[lessor]
        shares[lessor] = {c: u[c] / denom for c in industries if c not in (lessor, "HS")}
        shares[lessor]["stay"] = (final + u["HS"]) / denom
    return shares


def reallocate(amounts: dict, shares: dict) -> dict:
    """Move each lessor's amount to its users; solve the two lessors' cross purchases (x = own + share x other)."""
    a, b = LESSORS
    s_ab, s_ba = shares[a][b], shares[b][a]
    x_a = (amounts[a] + s_ba * amounts[b]) / (1 - s_ab * s_ba)
    x_b = amounts[b] + s_ab * x_a
    out = {c: v for c, v in amounts.items() if c not in LESSORS}
    for lessor, x in ((a, x_a), (b, x_b)):
        for c, s in shares[lessor].items():
            if c in LESSORS or c == "stay":
                continue
            out[c] = out.get(c, 0.0) + s * x
        out[lessor] = shares[lessor]["stay"] * x
    return out


def to_cells(amounts: dict, cells: list[str]) -> np.ndarray:
    v = np.zeros(len(cells))
    for c, x in amounts.items():
        v[cells.index(SUT_TO_CELL.get(c, c))] += x
    return v


def spread(total: float, pattern: np.ndarray) -> np.ndarray:
    return total * pattern / pattern.sum()


# ---------------------------------------------------------------------------------------------------------------
# Table 6.18D: (line, label) -> cells. Sector lines carry 2024; detail lines carry 2023 only.
CORP_SECTORS = {  # sector line: (label, [(detail line, label, cell or split key)])
    3: ("Agriculture, forestry, fishing, and hunting", [(4, "Farms", "111CA"), (5, "Forestry, fishing, and related activities", "113FF")]),
    6: ("Mining", [(7, "Oil and gas extraction", "211"), (8, "Mining, except oil and gas", "212"), (9, "Support activities for mining", "213")]),
    10: ("Utilities", [(10, "Utilities", "22")]),
    11: ("Construction", [(11, "Construction", "23")]),
    13: ("Durable goods", [(14, "Wood products", "321"), (15, "Nonmetallic mineral products", "327"), (16, "Primary metals", "331"),
                           (17, "Fabricated metal products", "332"), (18, "Machinery", "333"), (19, "Computer and electronic products", "334"),
                           (20, "Electrical equipment, appliances, and components", "335"),
                           (21, "Motor vehicles, bodies and trailers, and parts", "3361MV"), (22, "Other transportation equipment", "3364OT"),
                           (23, "Furniture and related products", "337"), (24, "Miscellaneous manufacturing", "339")]),
    25: ("Nondurable goods", [(26, "Food and beverage and tobacco products", "311FT"), (27, "Textile mills and textile product mills", "313TT"),
                              (28, "Apparel and leather and allied products", "315AL"), (29, "Paper products", "322"),
                              (30, "Printing and related support activities", "323"), (31, "Petroleum and coal products", "324"),
                              (32, "Chemical products", "325"), (33, "Plastics and rubber products", "326")]),
    34: ("Wholesale trade", [(34, "Wholesale trade", "42")]),
    37: ("Retail trade", [(37, "Retail trade", "RETAIL")]),
    38: ("Transportation and warehousing", [(39, "Air transportation", "481"), (40, "Rail transportation", "482"), (41, "Water transportation", "483"),
                                            (42, "Truck transportation", "484"), (43, "Transit and ground passenger transportation", "485"),
                                            (44, "Pipeline transportation", "486"), (45, "Other transportation and support activities", "487OS"),
                                            (46, "Warehousing and storage", "493")]),
    47: ("Information", [(48, "Publishing industries (includes software)", "511"), (49, "Motion picture and sound recording industries", "512"),
                         (50, "Broadcasting and telecommunications", "513"), (51, "Information and data processing services", "514")]),
    52: ("Finance and insurance", [(53, "Federal Reserve banks", "521CI"), (54, "Credit intermediation and related activities", "521CI"),
                                   (55, "Securities, commodity contracts, and investments", "523"), (56, "Insurance carriers and related activities", "524"),
                                   (57, "Funds, trusts, and other financial vehicles", "523")]),
    58: ("Real estate and rental and leasing", [(59, "Real estate", "ORE"),
                                                (60, "Rental and leasing services and lessors of intangible assets", "532RL")]),
    61: ("Professional, scientific, and technical services", [(62, "Legal services", "5411"), (63, "Computer systems design and related services", "5415"),
                                                              (64, "Miscellaneous professional, scientific, and technical services", "5412OP")]),
    65: ("Management of companies and enterprises", [(65, "Management of companies and enterprises", "55")]),
    66: ("Administrative and waste management services", [(67, "Administrative and support services", "561"),
                                                          (68, "Waste management and remediation services", "562")]),
    69: ("Educational services", [(69, "Educational services", "61")]),
    70: ("Health care and social assistance", [(71, "Ambulatory health care services", "621"),
                                               (72, "Hospitals and nursing and residential care facilities", "HOSPNURS"),
                                               (73, "Social assistance", "624")]),
    74: ("Arts, entertainment, and recreation", [(75, "Performing arts, spectator sports, museums, and related activities", "711AS"),
                                                 (76, "Amusements, gambling, and recreation industries", "713")]),
    77: ("Accommodation and food services", [(78, "Accommodation", "721"), (79, "Food services and drinking places", "722")]),
    80: ("Other services, except government", [(80, "Other services, except government", "81")]),
}
GOS_SPLITS = {"RETAIL": ["441", "445", "452", "4A0"], "HOSPNURS": ["622", "623"]}

# IRS SOI Table 1 column 19 rows -> cells (within a row, by the cells' corporate tax). Labels as printed.
SOI_ROWS = [
    ("Agricultural, forestry, fishing and hunting", ["111CA", "113FF"]),
    ("Oil and gas extraction", ["211"]),
    ("All Other mining", ["212", "213"]),
    ("Construction", ["23"]),
    ("Food manufacturing", ["311FT"]),
    ("Beverage and tobacco products", ["311FT"]),
    ("Paper manufacturing", ["322"]),
    ("Printing and related support activities", ["323"]),
    ("Petroleum and coal product manufacturing", ["324"]),
    ("Chemical manufacturing", ["325"]),
    ("Plastics and rubber product manufacturing", ["326"]),
    ("Nonmetallic mineral product manufacturing", ["327"]),
    ("Primary metal manufacturing", ["331"]),
    ("Fabricated metal products", ["332"]),
    ("Machinery manufacturing", ["333"]),
    ("Computer and electronic product manufacturing", ["334"]),
    ("Electrical equipment, appliance and component manufacturing", ["335"]),
    ("Motor vehicles and related manufacturing", ["3361MV"]),
    ("Other transportation equipment manufacturing", ["3364OT"]),
    ("Furniture and related product manufacturing", ["337"]),
    ("Miscellaneous manufacturing and manufacturing not allocable", ["321", "313TT", "315AL", "339"]),
    ("Wholesale trade", ["42"]),
    ("Retail trade", ["441", "445", "452", "4A0"]),
    ("Transportation and warehousing", ["481", "482", "483", "484", "485", "486", "487OS", "493"]),
    ("Publishing (except internet)", ["511"]),
    ("Motion picture and sound recording", ["512"]),
    ("Broadcasting and internet publishing", ["513"]),
    ("Telecommunications", ["513"]),
    ("Other information services", ["514"]),
    ("Depository credit intermediation", ["521CI"]),
    ("Securities, commodity contracts, and other financial investments", ["523"]),
    ("Insurance and related activities", ["524"]),
    ("All other finance industries", ["521CI", "523"]),
    ("Real estate and rental and leasing", ["ORE", "532RL"]),
    ("Professional, scientific, and technical services", ["5411", "5415", "5412OP"]),
    ("Bank holding companies", ["55"]),
    ("Other holding companies", ["55"]),
    ("Administrative and support and waste management and remediation", ["561", "562"]),
    ("Education services, health care, and social assistance", ["61", "621", "622", "623", "624"]),
    ("Arts, entertainment, and recreation", ["711AS", "713"]),
    ("Accommodation and food services", ["721", "722"]),
    ("Other services", ["81"]),
    ("All other industries", "ALL"),
]
SOI_MAJOR = ["Agricultural, forestry, fishing and hunting", "Mining", "Construction", "Manufacturing", "Wholesale and retail trade",
             "Transportation and warehousing", "Information", "Finance and insurance", "Real estate and rental and leasing",
             "Professional, scientific, and technical services", "Bank holding companies", "Other holding companies",
             "Administrative and support and waste management and remediation", "Education services, health care, and social assistance",
             "Arts, entertainment, and recreation", "Accommodation and food services", "Other services", "All other industries"]

# Fixed Assets Tables 3.1S / 3.1E: line -> (label, cell).
FA_LINES = {3: ("Farms", "111CA"), 4: ("Forestry, fishing, and related activities", "113FF"), 6: ("Oil and gas extraction", "211"),
            7: ("Mining, except oil and gas", "212"), 8: ("Support activities for mining", "213"), 9: ("Utilities", "22"),
            13: ("Construction", "23"), 16: ("Wood products", "321"), 17: ("Nonmetallic mineral products", "327"), 18: ("Primary metals", "331"),
            19: ("Fabricated metal products", "332"), 20: ("Machinery", "333"), 21: ("Computer and electronic products", "334"),
            22: ("Electrical equipment, appliances, and components", "335"), 23: ("Motor vehicles, bodies and trailers, and parts", "3361MV"),
            24: ("Other transportation equipment", "3364OT"), 25: ("Furniture and related products", "337"), 26: ("Miscellaneous manufacturing", "339"),
            30: ("Food and beverage and tobacco products", "311FT"), 33: ("Textile mills and textile product mills", "313TT"),
            34: ("Apparel and leather and allied products", "315AL"), 35: ("Paper products", "322"), 36: ("Printing and related support activities", "323"),
            37: ("Petroleum and coal products", "324"), 38: ("Chemical products", "325"), 39: ("Plastics and rubber products", "326"),
            40: ("Wholesale trade", "42"), 44: ("Motor vehicle and parts dealers", "441"), 45: ("Food and beverage stores", "445"),
            46: ("General merchandise stores", "452"), 47: ("Other retail", "4A0"), 49: ("Air transportation", "481"),
            50: ("Railroad transportation", "482"), 51: ("Water transportation", "483"), 52: ("Truck transportation", "484"),
            53: ("Transit and ground passenger transportation", "485"), 54: ("Pipeline transportation", "486"),
            55: ("Other transportation and support activities", "487OS"), 56: ("Warehousing and storage", "493"),
            58: ("Publishing industries (includes software)", "511"), 59: ("Motion picture and sound recording industries", "512"),
            60: ("Broadcasting and telecommunications", "513"), 61: ("Information and data processing services", "514"),
            63: ("Federal Reserve banks", "521CI"), 64: ("Credit intermediation and related activities", "521CI"),
            68: ("Securities, commodity contracts, and investments", "523"), 69: ("Insurance carriers and related activities", "524"),
            72: ("Funds, trusts, and other financial vehicles", "523"), 74: ("Real estate", "ORE"),
            75: ("Rental and leasing services and lessors of intangible assets", "532RL"), 77: ("Legal services", "5411"),
            78: ("Computer systems design and related services", "5415"),
            79: ("Miscellaneous professional, scientific, and technical services", "5412OP"),
            80: ("Management of companies and enterprises", "55"), 82: ("Administrative and support services", "561"),
            83: ("Waste management and remediation services", "562"), 84: ("Educational services", "61"),
            86: ("Ambulatory health care services", "621"), 87: ("Hospitals", "622"), 88: ("Nursing and residential care facilities", "623"),
            89: ("Social assistance", "624"), 91: ("Performing arts, spectator sports, museums, and related activities", "711AS"),
            92: ("Amusements, gambling, and recreation industries", "713"), 94: ("Accommodation", "721"),
            95: ("Food services and drinking places", "722"), 96: ("Other services, except government", "81")}

Z1_SERIES = {  # file, series, dictionary label, period
    "nfc_real_estate": ("S11_1_b", "LM105035005.Q", "Nonfinancial corporate business; real estate at market value", "2024:Q4"),
    "noncorp_nonres_real_estate": ("S11_2_b", "LM115035035.Q", "Nonfinancial noncorporate business; nonresidential real estate at market value", "2024:Q4"),
    "noncorp_nonres_structures": ("S11_2_b", "FL115013665.Q", "Nonfinancial noncorporate business; nonresidential structures, current cost basis", "2024:Q4"),
    "noncorp_res_real_estate": ("S11_2_b", "LM115035023.Q", "Nonfinancial noncorporate business; residential real estate at market value", "2024:Q4"),
    "household_owner_real_estate": ("S14_b", "LM155035015.A",
                                    "Households; owner-occupied real estate including vacant land and mobile homes at market value", "2024"),
}


def z1(zpath: Path) -> dict:
    out = {}
    with zipfile.ZipFile(zpath) as z:
        for key, (table, series, label, period) in Z1_SERIES.items():
            dictionary = z.read(f"data_dictionary/{table}.txt").decode("utf-8", errors="replace")
            entry = next((ln.split("\t") for ln in dictionary.splitlines() if ln.startswith(series + "\t")), None)
            gate(f"Z.1 {series} is '{label}'", entry is not None and entry[1].strip() == label)
            rows = list(csv.reader(io.StringIO(z.read(f"csv/{table}.csv").decode("utf-8"))))
            col = rows[0].index(series)
            hit = [r for r in rows[1:] if r[0] == period]
            gate(f"Z.1 {series} has one {period} value", len(hit) == 1)
            out[key] = float(hit[0][col])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = ap.parse_args()

    model = json.loads(MODEL.read_text())
    housing = json.loads(HOUSING.read_text())
    line = {x["id"]: x["national_bn"] for x in model["receipts"]["lines"]}
    tenant = housing["bea_housing"]["tenant_taxes_bn"]
    NATIONAL = {"c_and_i_property": line["remaining_production_property"] - tenant,
                "other_production_taxes": line["other_production_taxes"],
                "corporate": line["corporate_capital"] + line["corporate_labor"]}

    print("[NIPA: the model's lines from their tables]")
    nipa = openpyxl.load_workbook(checked(NIPA3, NIPA3_SHA), read_only=True, data_only=True)
    t31, t32, t33, t35 = (bea_sheet(nipa, s) for s in ("T30100-A", "T30200-A", "T30300-A", "T30500-A"))
    corp_total = value(t31, 5, "Taxes on corporate income") / 1e3
    corp_fed = value(t32, 8, "Taxes on corporate income") / 1e3
    corp_sl = value(t33, 11, "Taxes on corporate income") / 1e3
    gate("NIPA 3.1 line 5 is the model's corporate lines (1e-6 bn)", abs(corp_total - NATIONAL["corporate"]) < 1e-6, f"{corp_total:.3f}")
    gate("federal (3.2 line 8) + state and local (3.3 line 11) = 3.1 line 5 (1e-6 bn)", abs(corp_fed + corp_sl - corp_total) < 1e-6,
         f"{corp_fed:.3f} + {corp_sl:.3f}")
    otp = {"federal_other": value(t35, 17, "Other taxes on production"), "severance": value(t35, 34, "Severance taxes"),
           "documentary": value(t35, 36, "Other"), "special_assessments": value(t35, 39, "Special assessments"),
           "motor_vehicle_licenses": value(t35, 40, "Motor vehicle licenses"), "other_licenses": value(t35, 41, "Other license taxes"),
           "sl_other": value(t35, 42, "Other")}
    otp = {k: v / 1e3 for k, v in otp.items()}
    gate("Table 3.5's seven components are the model's other production taxes (1e-6 bn)",
         abs(sum(otp.values()) - NATIONAL["other_production_taxes"]) < 1e-6, f"{sum(otp.values()):.3f}")
    gate("Table 3.5 line 36's footnote: documentary and stamp taxes", "documentary and stamp taxes" in str(list(nipa["T30500-A"].values)))
    property_total = value(t35, 38, "Property taxes") / 1e3
    gate("property taxes (3.5 line 38) = the model's owner line + business property + the tenant split (1e-6 bn)",
         abs(property_total - line["modeled_owner_property"] - NATIONAL["c_and_i_property"] - tenant) < 1e-6, f"{property_total:.3f}")
    bea_housing_taxes = housing["bea_housing"]["taxes_on_production_bn"]
    gate("no housing tax inside business property: the owner and tenant lines hold more than BEA's housing taxes",
         line["modeled_owner_property"] + tenant >= bea_housing_taxes,
         f"owner {line['modeled_owner_property']:.3f} + tenant {tenant:.3f} vs BEA housing {bea_housing_taxes:.3f}")
    ci_bea_split = property_total - bea_housing_taxes

    print("\n[use table 2024: industry patterns]")
    industries, use_row = read_use(pinned("bea_SUPPLY-USE.zip"))
    cells = [c for c in dict.fromkeys(SUT_TO_CELL.get(c, c) for c in industries) if c != "HS"] + EXTRA_CELLS
    otop, gos, top = use_row("T00OTOP"), use_row("V003"), use_row("T00TOP")
    gate("use table: industries' other taxes on production add to the total (1 $mn)",
         abs(sum(otop[c] for c in industries) - otop["T001"]) <= 1.0, f"{otop['T001']:,.0f}")
    shares = lessor_shares(industries, use_row)
    for lessor in LESSORS:
        s = shares[lessor]
        gate(f"{lessor}: users' shares and what stays add to 1", abs(sum(s.values()) - 1) < 1e-12, f"stays {s['stay']:.4f}")
    otop_bus = {c: otop[c] for c in industries if c != "HS"}
    otop_pattern = to_cells(reallocate(otop_bus, shares), cells)
    otop_pattern_raw = to_cells(otop_bus, cells)
    gate("lessor reallocation keeps the pattern's total (1e-6 $mn)", abs(otop_pattern.sum() - sum(otop_bus.values())) < 1e-6)
    mining_top = {c: top[c] for c in ("211", "212", "213")}
    severance_pattern = to_cells(mining_top, cells)

    print("\n[Z.1 and Fixed Assets: land share and the residential split]")
    zv = z1(pinned("frb_z1_20260911_csv_files.zip"))
    fa4 = bea_sheet(openpyxl.load_workbook(pinned("bea_fa_Section4All_xls.xlsx"), read_only=True, data_only=True), "FAAt401-A")
    fa5 = bea_sheet(openpyxl.load_workbook(pinned("bea_fa_Section5All_xls.xlsx"), read_only=True, data_only=True), "FAAt501-A")
    fa3book = openpyxl.load_workbook(pinned("bea_fa_Section3All_xls.xlsx"), read_only=True, data_only=True)
    fa3s, fa3e = bea_sheet(fa3book, "FAAt301S-A"), bea_sheet(fa3book, "FAAt301E-A")
    nfc_structures = value(fa4, 39, "Structures")
    gate("FA 4.1 line 39 sits under 'Nonfinancial' corporate (line 37)", fa4["lines"][37][0] == "Nonfinancial"
         and fa4["lines"][33][0] == "Financial")
    corp_res_structures = value(fa5, 3, "Corporate")
    business_re = zv["nfc_real_estate"] + zv["noncorp_nonres_real_estate"]
    business_structures = nfc_structures + corp_res_structures + zv["noncorp_nonres_structures"]
    lam_b = 1 - business_structures / business_re
    gate("lambda_b in (0, 1)", 0 < lam_b < 1, f"{lam_b:.6f}")
    lam_noncorp = 1 - zv["noncorp_nonres_structures"] / zv["noncorp_nonres_real_estate"]
    lam_corp = 1 - (nfc_structures + corp_res_structures) / zv["nfc_real_estate"]
    residential_re = zv["household_owner_real_estate"] + zv["noncorp_res_real_estate"]
    res_share = residential_re / (residential_re + business_re)

    # Tangible personal property: Tax Foundation's national share of property tax collections (car taxes excluded).
    tf = pinned("taxfoundation_tpp_2023.html").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Nationally, we estimate that personal property taxes are responsible for ([\d.]+) percent of property tax "
                  r"collections, or about ([\d.]+) percent if one excludes car taxes", tf)
    gate("Tax Foundation's national TPP share sentence found", m is not None)
    tpp_all, tpp_ex_cars = float(m.group(1)) / 100, float(m.group(2)) / 100
    tau = tpp_ex_cars * property_total / NATIONAL["c_and_i_property"]
    gate("tau in (0, 1)", 0 < tau < 1, f"{tau:.6f}")

    print("\n[Fixed Assets 3.1S / 3.1E: the structures base]")
    res_structures = value(fa3s, 1, "Private fixed assets") - value(fa4, 3, "Structures")
    res_equipment = value(fa3e, 1, "Private fixed assets") - value(fa4, 2, "Equipment")
    struct, equip = {}, {}
    for ln, (label, cell) in FA_LINES.items():
        struct[cell] = struct.get(cell, 0.0) + value(fa3s, ln, label)
        equip[cell] = equip.get(cell, 0.0) + value(fa3e, ln, label)
    struct["ORE"] -= res_structures       # [ASSUMPTION] every private residential structure is in the real estate industry
    equip["ORE"] -= res_equipment
    tol = 0.5 * len(FA_LINES)
    gate(f"the structures cells add to private nonresidential structures (FA 4.1 line 3, rounding {tol:.0f} $mn)",
         abs(sum(struct.values()) - value(fa4, 3, "Structures")) <= tol, f"{sum(struct.values()):,.0f}")
    gate(f"the equipment cells add to private nonresidential equipment (FA 4.1 line 2, rounding {tol:.0f} $mn)",
         abs(sum(equip.values()) - value(fa4, 2, "Equipment")) <= tol, f"{sum(equip.values()):,.0f}")
    gate("real estate keeps positive nonresidential structures and equipment", struct["ORE"] > 0 and equip["ORE"] > 0,
         f"{struct['ORE']:,.0f} / {equip['ORE']:,.0f}")
    nonprofit_structures = value(fa4, 67, "Structures")
    nonprofit_equipment = value(fa4, 66, "Equipment")
    gate("FA 4.1 lines 66-67 sit under 'Nonprofit institutions' (line 65)", fa4["lines"][65][0] == "Nonprofit institutions")

    print("\n[Table 6.18D: corporate taxes by industry]")
    s6 = openpyxl.load_workbook(pinned("bea_Section6All_xls.xlsx"), read_only=True, data_only=True)
    t618 = bea_sheet(s6, "T61800D-A")
    gate("6.18D is 'Taxes on Corporate Income by Industry', published September 30, 2026",
         "Table 6.18D. Taxes on Corporate Income by Industry" in t618["title"] and "Data published September 30, 2026" in t618["title"])
    total618 = value(t618, 1, "Taxes on corporate income")
    gate("6.18D: domestic industries are the total (no rest-of-world line in 2024)", value(t618, 2, "Domestic industries") == total618)
    sectors24 = {ln: value(t618, ln, label) for ln, (label, _) in CORP_SECTORS.items()}
    gate("6.18D 2024: sectors add to the total (1 $mn)", abs(sum(sectors24.values()) - total618) <= 1.0, f"{sum(sectors24.values()):,.0f}")
    gate("6.18D 2024: durable + nondurable = manufacturing", abs(sectors24[13] + sectors24[25] - value(t618, 12, "Manufacturing")) <= 1.0)
    corp_raw = {}
    for ln, (label, detail) in CORP_SECTORS.items():
        d23 = {dl: value(t618, dl, dlabel, "2023") for dl, dlabel, _ in detail}
        if len(detail) > 1:
            gate(f"6.18D 2023: {label}'s detail adds to the sector (1 $mn)", abs(sum(d23.values()) - value(t618, ln, label, "2023")) <= 1.0)
        for dl, dlabel, cell in detail:
            amount = sectors24[ln] * d23[dl] / sum(d23.values())
            parts = GOS_SPLITS.get(cell, [cell])
            g = np.array([gos[p] for p in parts]) if cell in GOS_SPLITS else np.ones(1)
            for p, w in zip(parts, g / g.sum()):
                corp_raw[p] = corp_raw.get(p, 0.0) + amount * w
    scale = NATIONAL["corporate"] / (sum(corp_raw.values()) / 1e3)
    corp_raw = {c: v / 1e3 * scale for c, v in corp_raw.items()}
    gate("corporate cells add to the model's line (1e-6 bn)", abs(sum(corp_raw.values()) - NATIONAL["corporate"]) < 1e-6)

    def corp_pipeline(raw: dict, mgmt: str = "pro_rata", realloc: bool = True) -> np.ndarray:
        x = dict(raw)
        if mgmt == "pro_rata":
            m55 = x.pop("55")
            rest = sum(x.values())
            x = {c: v * (1 + m55 / rest) for c, v in x.items()}
            x["55"] = 0.0
        x = reallocate(x, shares) if realloc else x
        return to_cells(x, cells)

    print("\n[IRS SOI: federal tax on foreign-source income, Tax Year 2021]")
    soi = pdf_text(pinned("irs_soi_coftc_ty2021.pdf"))
    page19 = next(p for p in soi.split("\f") if re.search(r"\(19\)\s+\(20\)\s+\(21\)\s+\(22\)\s+\(23\)", p)
                  and "All industries" in p)
    page19b = next(p for p in soi.split("\f") if re.search(r"\(19\)\s+\(20\)\s+\(21\)\s+\(22\)\s+\(23\)", p)
                   and "Bank holding companies" in p)
    gate("SOI Table 1 column 19 is 'Difference between limitation and foreign tax credit'",
         "limitation and" in page19 and "credit [2]" in page19 and "Table 1." in page19)
    rows19 = soi_rows(page19) | soi_rows(page19b)

    def soi19(label: str) -> float:
        if label not in rows19:
            raise SystemExit(f"[BLOCKED] SOI column 19 row {label!r} not found")
        return money(rows19[label][0])

    col19_all = soi19("All industries")
    majors = {lab: soi19(lab) for lab in SOI_MAJOR}
    gate("SOI column 19: major industries add to all industries (10 $k)", abs(sum(majors.values()) - col19_all) <= 10,
         f"{sum(majors.values()):,.0f} vs {col19_all:,.0f}")
    pages = soi.split("\f")
    page18 = next(p for p in pages if re.search(r"\(13\)\s+\(14\)\s+\(15\)\s+\(16\)\s+\(17\)\s+\(18\)", p) and "All industries" in p)
    page2 = next(p for p in pages if re.search(r"\(1\)\s+\(2\)\s+\(3\)\s+\(4\)\s+\(5\)\s+\(6\)", p) and "Table 1." in p
                 and "All industries" in p)
    gate("SOI Table 1 column 2 is 'Foreign tax credit claimed'", "Foreign tax" in page2 and "credit claimed" in page2)
    col18_all = money(soi_rows(page18)["All industries"][-1])
    col2_all = money(soi_rows(page2)["All industries"][1])
    gate("SOI: column 19 is column 18 less column 2 within 0.01% (footnote 2's adjustments)",
         abs(col18_all - col2_all - col19_all) <= 1e-4 * col19_all, f"{col18_all:,.0f} - {col2_all:,.0f} vs {col19_all:,.0f}")
    gate("SOI footnote 2: the column is 'one way to measure the U.S. tax owed on foreign-source corporate income'",
         re.search(r"one way to measure the U\.S\. tax owed on foreign-source\s+corporate income", soi) is not None)
    used = [(lab, soi19(lab), cs) for lab, cs in SOI_ROWS]
    sub = sum(v for lab, v, _ in used)
    gate("SOI rows used add to all industries (10 $k)", abs(sub - col19_all) <= 10, f"{sub:,.0f}")
    p5655 = pdf_text(pinned("irs_p5655_ty2021.pdf"))
    m = re.search(r"Total income tax after credits, the amount paid to the.{0,400}?U\.S\. government, increased [\d.]+% to \$([\d.]+) billion",
                  p5655, re.S)
    gate("Publication 5655: total income tax after credits, Tax Year 2021", m is not None)
    after_credits_k = float(m.group(1)) * 1e6
    foreign_share = col19_all / after_credits_k
    foreign_bn = foreign_share * corp_fed
    fed_frac = corp_fed / corp_total  # [ASSUMPTION] the federal share is the same in every industry
    removed = {}
    for lab, v, cs in used:
        cs = [c for c in corp_raw if c != "55"] if cs == "ALL" else cs
        w = np.array([corp_raw[c] for c in cs])
        for c, x in zip(cs, w / w.sum()):
            removed[c] = removed.get(c, 0.0) + foreign_bn * v / sub * x
    worst = min(corp_raw[c] * fed_frac - removed.get(c, 0.0) for c in corp_raw)
    gate("no cell loses more than its federal corporate tax", worst >= 0, f"min federal left {worst:.3f} bn")
    corp_ex_foreign_raw = {c: v - removed.get(c, 0.0) for c, v in corp_raw.items()}

    print("\n[Treasury OTA: the normal-return share]")
    tp5 = pdf_text(checked(TP5, TP5_SHA))
    m63 = re.search(r"we find that (\d+) percent of current corporate taxable income is due to supernormal\s+returns", tp5)
    m37 = re.search(r"of the remaining (\d+)\s+percent of the corporate tax on the taxable income attributable to normal returns", tp5)
    gate("TP-5: the supernormal and normal shares are printed and add to 100", m63 is not None and m37 is not None
         and int(m63.group(1)) + int(m37.group(1)) == 100, f"{m63.group(1)} + {m37.group(1)}" if m63 and m37 else "")
    normal_share = int(m37.group(1)) / 100
    ota = pdf_text(pinned("treasury_ota_summary_2021.pdf"))
    m185 = re.search(r"split between capital income \(([\d.]+) percent\) and labor income \(([\d.]+) percent\)", ota)
    gate("OTA 2021: labor's corporate share is half the normal-return share (TP-5's rule unchanged)",
         m185 is not None and abs(2 * float(m185.group(2)) / 100 - normal_share) < 1e-12, m185.group(2) if m185 else "")
    # Power and Frerick: TP-5's method on SOI's C corporation files, 1992-2013 (abstract, p. 2), and by industry.
    wp = pdf_text(pinned("treasury_ota_wp111_2016.pdf"))
    mpf = re.search(r"averaging\s+(\d+)\s+percent\s+from\s+1992.2002\s+and\s+(\d+)\s+percent\s+from\s+2003.2013", wp)
    gate("Power and Frerick: the abstract's 1992-2002 and 2003-2013 averages are printed", mpf is not None,
         f"{mpf.group(1)} / {mpf.group(2)}" if mpf else "")
    pf_period = {"1992_2002": int(mpf.group(1)) / 100, "2003_2013": int(mpf.group(2)) / 100} if mpf else {}
    pf_table = {}
    for name in PF_MAJOR + PF_MINOR:
        mm = re.search(rf"^\s*{re.escape(name)}\s+(\d\.\d\d)(?:\s+(\d\.\d\d))?\s*$", wp, re.M)
        if mm:
            pf_table[name] = {"risk_free": float(mm.group(1)), "worldwide_income": float(mm.group(2)) if mm.group(2) else None}
    t1 = "Three Year Average Fraction of the Corporate Tax Base" in wp and "excludes finance, rental, and real estate" in wp
    gate("Power and Frerick Table 1: its title, and every industry's share (the major ones with their income shares)",
         t1 and len(pf_table) == len(PF_MAJOR) + len(PF_MINOR) and all(pf_table[n]["worldwide_income"] is not None for n in PF_MAJOR),
         f"{len(pf_table)} rows")
    inc = sum(pf_table[n]["worldwide_income"] for n in PF_MAJOR if n in pf_table)
    pf_mean = sum(pf_table[n]["risk_free"] * pf_table[n]["worldwide_income"] for n in PF_MAJOR if n in pf_table) / inc if inc else float("nan")
    gate("Power and Frerick Table 1: the income shares add to 1 (0.02) and their weighted risk-free share is the 2003-2013 "
         "average's (0.02)", abs(inc - 1) <= 0.02 and abs(pf_mean - pf_period.get("2003_2013", float("nan"))) <= 0.02,
         f"{inc:.2f}; {pf_mean:.4f}")

    print("\n[the line x cell table]")
    col = {}
    col["corporate"] = corp_pipeline(corp_raw)
    col["corporate_mgmt_own"] = corp_pipeline(corp_raw, mgmt="own")
    col["corporate_no_lessor_realloc"] = corp_pipeline(corp_raw, realloc=False)
    col["corporate_ex_foreign"] = corp_pipeline(corp_ex_foreign_raw)
    col["c_and_i_property"] = spread(NATIONAL["c_and_i_property"], otop_pattern)
    col["c_and_i_property_no_lessor_realloc"] = spread(NATIONAL["c_and_i_property"], otop_pattern_raw)
    col["c_and_i_property_bea_housing_split"] = spread(ci_bea_split, otop_pattern)

    # Structures base: nonprofit structures (exempt) leave each industry in proportion to its nonprofit wage share
    # (job_capital.py measures it; here the base is the gross stock, and the nonprofit cut is applied there).
    struct_pattern = to_cells(reallocate(struct, shares), cells)
    equip_pattern = to_cells(reallocate(equip, shares), cells)
    col["structures_stock_mn"] = struct_pattern
    col["equipment_stock_mn"] = equip_pattern

    res = {"documentary": otp["documentary"] * res_share, "special_assessments": otp["special_assessments"] * res_share}
    licenses = otp["federal_other"] + otp["motor_vehicle_licenses"] + otp["other_licenses"] + otp["sl_other"]
    col["otp_licenses_and_other"] = spread(licenses, otop_pattern)
    col["otp_severance"] = spread(otp["severance"], severance_pattern)
    col["otp_documentary"] = spread(otp["documentary"] - res["documentary"], otop_pattern)
    col["otp_special_assessments"] = spread(otp["special_assessments"] - res["special_assessments"], otop_pattern)
    col["otp_documentary"][cells.index("RESIDENTIAL")] += res["documentary"]
    col["otp_special_assessments"][cells.index("RESIDENTIAL")] += res["special_assessments"]
    col["other_production_taxes"] = (col["otp_licenses_and_other"] + col["otp_severance"] + col["otp_documentary"]
                                     + col["otp_special_assessments"])
    for name, total in (("corporate", NATIONAL["corporate"]), ("corporate_mgmt_own", NATIONAL["corporate"]),
                        ("corporate_no_lessor_realloc", NATIONAL["corporate"]), ("corporate_ex_foreign", NATIONAL["corporate"] - foreign_bn),
                        ("c_and_i_property", NATIONAL["c_and_i_property"]), ("c_and_i_property_no_lessor_realloc", NATIONAL["c_and_i_property"]),
                        ("c_and_i_property_bea_housing_split", ci_bea_split), ("other_production_taxes", NATIONAL["other_production_taxes"])):
        gate(f"{name}: cells add to the national amount (1e-6 bn)", abs(col[name].sum() - total) < 1e-6, f"{col[name].sum():.6f}")
    gate("no negative cell in any column", all((v >= -1e-12).all() for v in col.values()))
    ri = cells.index("RESIDENTIAL")
    gate("the RESIDENTIAL cell holds only the residential parts of documentary taxes and special assessments",
         all(col[k][ri] == 0 for k in col if k not in ("otp_documentary", "otp_special_assessments", "other_production_taxes")))
    gate("private households and the residential cell carry no corporate or business property tax",
         all(col[k][cells.index("HH814")] == 0 for k in col))
    pf_cell = {c: PF_INDUSTRY.get(c) for c in cells}
    gate("Power and Frerick: every industry the cells name is in Table 1, and every cell with corporate tax outside its industries is "
         "agriculture, finance, real estate and rental, or government", set(v for v in pf_cell.values() if v) <= set(PF_MAJOR)
         and {c for c, v in pf_cell.items() if not v and col["corporate"][cells.index(c)] > 0}
         <= {"111CA", "113FF", "521CI", "523", "524", "ORE", "532RL", "GOVF", "GOVSL"})

    if any(not g["passed"] for g in GATES):
        print(f"\n[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    names = list(col)
    with (args.out_dir / "national_by_industry.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["cell"] + [f"{n}_bn" if not n.endswith("_mn") else n for n in names] + ["pf_industry", "pf_normal_share"])
        for i, c in enumerate(cells):
            pf = pf_table[pf_cell[c]]["risk_free"] if pf_cell[c] else pf_period["2003_2013"]
            w.writerow([c] + [f"{col[n][i]:.9f}" for n in names] + [pf_cell[c] or "", f"{pf:.2f}"])
    r9 = lambda x: round(float(x), 9)
    out = {
        "meta": {
            "year": 2024,
            "lines": "assumption_explorer_2026_09_21/derived/model.json: remaining_production_property less the BEA tenant split "
                     "(receipt_side_long_run_2026_09_28 housing.json), other_production_taxes, corporate_capital + corporate_labor",
            "model_sha256": sha256(MODEL), "housing_sha256": sha256(HOUSING),
            "inputs": {k: v["sha256"] for k, v in PINS.items()} | {"nipa_section3": NIPA3_SHA, "treasury_tp5": TP5_SHA},
            "cells": "BEA 2024 summary use table industries; HS left out; 525 with 523; GOVF = GFGD+GFGN+GFE; GOVSL = GSLG+GSLE; "
                     "HH814 private households (zero); RESIDENTIAL holds the residential parts outside the item",
            "lessors": "ORE and 532RL amounts go to the industries buying their commodity (use table intermediate uses); the part "
                       "sold to final demand and to housing stays with the lessor; the two lessors' cross purchases solved exactly",
            "vintages": {"model_lines": "NIPA 3.1-3.3 published 2026-08-26; 3.5 published 2025-09-26",
                         "patterns": "6.18D and the supply-use tables published 2026-09-30; Fixed Assets file of 2026-09-28; Z.1 of 2026-09-11"},
        },
        "national_bn": {k: r9(v) for k, v in NATIONAL.items()} | {"tenant_split": r9(tenant), "property_total": r9(property_total),
                                                                  "c_and_i_bea_housing_split": r9(ci_bea_split)},
        "other_production_components_bn": {k: r9(v) for k, v in otp.items()},
        "corporate": {"federal_bn": r9(corp_fed), "state_local_bn": r9(corp_sl), "table_618d_2024_bn": r9(total618 / 1e3),
                      "scale_to_model": r9(scale)},
        "land": {"lambda_b": r9(lam_b), "lambda_noncorporate": r9(lam_noncorp), "lambda_corporate": r9(lam_corp),
                 "business_real_estate_mn": r9(business_re), "business_structures_mn": r9(business_structures),
                 "z1_mn": {k: r9(v) for k, v in zv.items()}, "fa_nfc_nonres_structures_mn": r9(nfc_structures),
                 "fa_corporate_residential_mn": r9(corp_res_structures),
                 "rule": "lambda_b = 1 - (FA 4.1 line 39 nonfinancial corporate structures + FA 5.1 line 3 corporate residential + Z.1 "
                         "FL115013665 noncorporate nonresidential structures) / (Z.1 LM105035005 nonfinancial corporate real estate + "
                         "LM115035035 noncorporate nonresidential real estate), 2024 yearend"},
        "residential_split": {"residential_share": r9(res_share), "residential_real_estate_mn": r9(residential_re),
                              "residential_parts_bn": {k: r9(v) for k, v in res.items()},
                              "rule": "documentary and stamp taxes and special assessments split by market value: households' owner-occupied "
                                      "real estate + noncorporate residential real estate against nonfinancial corporate + noncorporate "
                                      "nonresidential real estate (Z.1, 2024)"},
        "tpp": {"all_property_share": tpp_all, "ex_car_share": tpp_ex_cars, "tau_of_business_line": r9(tau),
                "source": "Tax Foundation, Personal Property Tax Exemptions for Small Businesses (Hulehan, 2023-12-07), tax year 2021",
                "rule": "tau = the ex-car share x NIPA property taxes / the business property line"},
        "structures_base": {"nonprofit_structures_mn": nonprofit_structures, "nonprofit_equipment_mn": nonprofit_equipment,
                            "residential_structures_removed_from_real_estate_mn": r9(res_structures),
                            "residential_equipment_removed_from_real_estate_mn": r9(res_equipment)},
        "foreign": {"soi_column19_all_k": col19_all, "soi_column18_all_k": col18_all, "soi_column2_all_k": col2_all,
                    "p5655_after_credits_bn": after_credits_k / 1e6, "share_of_federal": r9(foreign_share),
                    "removed_bn": r9(foreign_bn), "federal_fraction_used": r9(fed_frac),
                    "rows_k": {lab: v for lab, v, _ in used},
                    "rule": "federal corporate tax x (SOI TY2021 Table 1 column 19, all industries / Pub. 5655 total income tax after "
                            "credits), spread over SOI's industries by column 19 and within each over cells by their corporate tax; "
                            "state taxes kept (water's-edge apportionment taxes little foreign income) [ASSUMPTION]"},
        "normal_return": {"share": normal_share,
                          "source": "Treasury OTA Technical Paper 5 (Cronin, Lin, Power and Cooper, May 2012), p. 7: \"we find that 63 percent "
                                    "of current corporate taxable income is due to supernormal returns\" and \"the remaining 37 percent of the "
                                    "corporate tax on the taxable income attributable to normal returns\"",
                          "ota_2021_labor_share_pct": float(m185.group(2)),
                          "ota_2021_source": "Treasury OTA, Treasury's Distribution Methodology and Results (July 2021; "
                                             "Summary-of-OTA-Distribution-Methodology-05102021.pdf), p. 3 note 4: \"split between capital income "
                                             "(81.5 percent) and labor income (18.5 percent)\"",
                          "power_frerick": {"1992_2002": pf_period["1992_2002"], "2003_2013": pf_period["2003_2013"],
                                            "table1_2011_2013": pf_table, "table1_income_weighted_mean": r9(pf_mean),
                                            "cells": {c: v for c, v in pf_cell.items() if v},
                                            "source": "Power and Frerick, Have Excess Returns To Corporations Been Increasing Over Time?, "
                                                      "Treasury OTA Working Paper 111 (November 2016; National Tax Journal 69(4), 2016): abstract "
                                                      "p. 2, the risk-free share of the C corporation base \"averaging 40 percent from 1992-2002 "
                                                      "and 25 percent from 2003-2013\"; Table 1 p. 16, three-year averages 2011-2013 by industry",
                                            "rule": "cells take their Table 1 industry's share; cells outside its industries take the 2003-2013 "
                                                    "average [INFERENCE: the industry map in PF_INDUSTRY]"}},
        "lessor_shares": {k: {c: r9(v) for c, v in s.items()} for k, s in shares.items()},
        "gates": GATES,
    }
    (args.out_dir / "national.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"\nwrote {args.out_dir / 'national_by_industry.csv'} and national.json "
          f"(lambda_b {lam_b:.4f}, tau {tau:.4f}, foreign {foreign_bn:.2f} bn, residential share {res_share:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

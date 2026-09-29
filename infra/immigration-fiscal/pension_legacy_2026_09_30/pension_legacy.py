"""Unfunded public-employee pension legacy by group: stock entering 2024 and 2024 interest on it.

State-local and federal defined-benefit plans owe benefits already earned by past service that their
assets do not cover. BEA books the interest accruing on that shortfall inside government interest
payments; the main case holds that interest row (Table 3.1 line 28, $1,118.87bn) at zero response, and
the federal debt legacy lane covers Treasury debt held by the public only. This lane measures the
shortfall and its 2024 interest from pinned primary files and attributes it to three groups of the
union's size (the Mexican-origin union, third-plus-generation non-Hispanic whites, an all-residents
slice) by their use of the services the plans' employees provided.

Run from the repository root (a worktree drops --no-project):
  uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py
  uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py --fetch
`--fetch` downloads every input to `_cache/` (ignored; ASPEP needs CENSUS_API_KEY in the environment,
never written) and then runs. A default run reads `_cache/` and stops unless every file matches its pin.

Outputs (derived/, LF line endings):
  measured_2024.csv      every measured input with its source cell
  domestic_interest.csv  what the $1,118.87bn row holds: pension interest and the rest
  function_mix.csv       each plan's payroll split over the account's spending lines
  group_shares.csv       each group's share of each line and the main case's responses
  headcount_path.csv     the Mexican-origin population-share path and the service-year weights
  attribution.csv        every arm: group x plan x basis x time weighting x responses x end
  by_line.csv            the adopted arm's interest by plan and spending line
  summary.csv            the adopted arm and its companions, with the Mexican-origin minus white difference
  opeb_federal.csv       federal retiree health (beside; not in the NIPA interest row)
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import subprocess
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
UNION_ROW4 = 39_712_493.33          # dataset audit row 4: the people the account prices (per-member denominator)
RESIDENTS = 340_110_988              # the account's 2024 resident control

PINS = {
    "Section3All_xls.xlsx": "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e",
    "Section6All_xls.xlsx": None,    # filled below from the fetched file; see PINS_FILE
    "Section7All_xls.xlsx": "ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef",
}
SOURCES = {
    "Section3All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx",
    "Section6All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section6All_xls.xlsx",
    "Section7All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx",
    "z1_csv_files.zip": "https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip",
    "c2010br-04.pdf": "https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-04.pdf",
    "c2kbr01-3.pdf": "https://www2.census.gov/library/publications/decennial/2000/briefs/c2kbr01-03.pdf",
    "we-02r.pdf": "https://www2.census.gov/library/publications/decennial/1990/we-the-americans/we-02r.pdf",
    "fr2025_note13.pdf": "https://fiscal.treasury.gov/system/files/2026-04/2025-note-13-financial-statements.pdf",
}
PINS_FILE = HERE / "source_pins.json"   # tracked: sha256 and bytes of every cached input

ASPEP_URL = "https://api.census.gov/data/timeseries/govsemp"


# ----------------------------------------------------------------------------------------------- fetch
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(env_file: Path | None = None) -> None:
    CACHE.mkdir(exist_ok=True)
    agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    for name, url in SOURCES.items():
        if (CACHE / name).exists():          # keep a cached vintage; delete the file to refresh it
            continue
        body = urllib.request.urlopen(urllib.request.Request(url, headers=agent), timeout=180).read()
        if name.endswith(".pdf") and not body.startswith(b"%PDF"):
            raise ValueError(f"[BLOCKED] {url} did not return a PDF")
        (CACHE / name).write_bytes(body)
    if (CACHE / "aspep_2024.json").exists():
        write_pins()
        return
    key = os.environ.get("CENSUS_API_KEY")
    if not key and env_file:              # acquire/config.local.env, KEY=VALUE lines; the key is never printed
        found = re.search(r"^\s*(?:export\s+)?CENSUS_API_KEY=['\"]?([^'\"\s]+)", env_file.read_text(), re.M)
        key = found.group(1) if found else None
    if not key:
        raise ValueError("[BLOCKED] ASPEP needs CENSUS_API_KEY in the environment")
    q = {"get": "AGG_DESC,AGG_DESC_LABEL,GOVTYPE,GOVTYPE_LABEL,TOT_PAY,FTE", "for": "us:*", "time": "2024", "key": key}
    try:
        rows = json.load(urllib.request.urlopen(ASPEP_URL + "?" + urllib.parse.urlencode(q), timeout=120))
    except Exception as e:                                   # the URL carries the key: never print it
        raise ValueError("[BLOCKED] ASPEP request failed: " + str(e).replace(key, "<KEY>")) from None
    (CACHE / "aspep_2024.json").write_text(json.dumps(rows, indent=0) + "\n")
    write_pins()


def write_pins() -> None:
    pins = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size}
            for p in sorted(CACHE.iterdir()) if p.is_file() and p.suffix in {".xlsx", ".zip", ".pdf", ".json"}}
    PINS_FILE.write_text(json.dumps(pins, indent=1, sort_keys=True) + "\n")


def pinned(name: str) -> Path:
    path = CACHE / name
    pins = json.loads(PINS_FILE.read_text())
    if not path.exists():
        raise ValueError(f"[BLOCKED] missing {path}; run with --fetch")
    if sha(path) != pins[name]["sha256"] or (PINS.get(name) and PINS[name] != pins[name]["sha256"]):
        raise ValueError(f"[BLOCKED] {name} is not the pinned vintage")
    return path


# ----------------------------------------------------------------------------------------------- BEA
def bea_table(book, sheet: str, year: int = 2024, units: str = "[Millions of dollars]") -> tuple[dict[int, dict], list[str]]:
    rows = list(book[sheet].values)
    headers = [r for r in rows if r[0] == "Line"]
    if len(headers) != 1 or (units and rows[1][0] != units):
        raise ValueError(f"[BLOCKED] {sheet}: header or units changed")
    cols = [i for i, x in enumerate(headers[0]) if str(x) == str(year)]
    if len(cols) != 1:
        raise ValueError(f"[BLOCKED] {sheet}: no single {year} column")
    j = cols[0]
    lines = {int(r[0]): dict(label=str(r[1]).strip(), code=r[2], value=r[j]) for r in rows if str(r[0]).isdigit()}
    notes = [str(r[0]) for r in rows if r[0] and not str(r[0]).isdigit() and r[0] != "Line"]
    return lines, notes


def bea_series(book, sheet: str, number: int) -> dict[int, float]:
    rows = list(book[sheet].values)
    header = [r for r in rows if r[0] == "Line"][0]
    row = [r for r in rows if str(r[0]) == str(number)][0]
    return {int(float(y)): float(v) for y, v in zip(header[3:], row[3:]) if isinstance(v, (int, float))}


def cell(lines: dict, number: int, label: str) -> float:
    got = lines[number]
    if not got["label"].replace("\\", "").startswith(label):
        raise ValueError(f"[BLOCKED] line {number} is {got['label']!r}, expected {label!r}")
    return got["value"] / 1000.0      # $bn


def measure_bea() -> tuple[dict, dict]:
    s3 = openpyxl.load_workbook(pinned("Section3All_xls.xlsx"), read_only=True, data_only=True)
    s7 = openpyxl.load_workbook(pinned("Section7All_xls.xlsx"), read_only=True, data_only=True)
    t31, n31 = bea_table(s3, "T30100-A")
    t32, n32 = bea_table(s3, "T30200-A")
    t33, n33 = bea_table(s3, "T30300-A")
    t3105, _ = bea_table(s3, "T31005-A")
    t3115, _ = bea_table(s3, "T31105-A")
    t317, _ = bea_table(s3, "T31700-A")
    t723, n723 = bea_table(s7, "T72300-A")
    t724, n724 = bea_table(s7, "T72400-A")
    t78, _ = bea_table(s7, "T70800-A")
    m = {
        "domestic_interest_total": (cell(t31, 28, "To persons and business"), "BEA T3.1 line 28"),
        "domestic_interest_federal": (cell(t32, 34, "To persons and business"), "BEA T3.2 line 34"),
        "domestic_interest_state_local": (cell(t33, 29, "To persons and business"), "BEA T3.3 line 29"),
        "sl_actual_employer_contributions": (cell(t724, 5, "Actual employer contributions"), "BEA T7.24 line 5"),
        "sl_imputed_employer_contributions": (cell(t724, 6, "Imputed employer contributions"), "BEA T7.24 line 6"),
        "sl_plan_monetary_interest": (cell(t724, 12, "Monetary interest"), "BEA T7.24 line 12"),
        "sl_imputed_interest": (cell(t724, 13, "Imputed interest on plans' claims on employers"), "BEA T7.24 line 13"),
        "sl_plan_dividends": (cell(t724, 14, "Dividends"), "BEA T7.24 line 14"),
        "sl_interest_accrued_on_entitlements": (cell(t724, 31, "Interest accrued on benefit entitlements"), "BEA T7.24 line 31"),
        "fed_actual_employer_contributions": (cell(t723, 5, "Actual employer contributions"), "BEA T7.23 line 5"),
        "fed_imputed_employer_contributions": (cell(t723, 8, "Imputed employer contributions"), "BEA T7.23 line 8"),
        "fed_plan_interest_total": (cell(t723, 17, "Interest"), "BEA T7.23 line 17"),
        "fed_plan_monetary_interest": (cell(t723, 18, "Monetary interest"), "BEA T7.23 line 18"),
        "fed_imputed_interest": (cell(t723, 19, "Imputed interest on plans' claims on employers"), "BEA T7.23 line 19"),
        "fed_interest_accrued_on_entitlements": (cell(t723, 41, "Interest accrued on benefit entitlements"), "BEA T7.23 line 41"),
        "supp_federal_civilian_pension": (cell(t78, 6, "Federal civilian pension plans"), "BEA T7.8 line 6"),
        "supp_federal_military_pension": (cell(t78, 7, "Federal military pension plans"), "BEA T7.8 line 7"),
        "supp_state_local_retirement": (cell(t78, 10, "State and local employee retirement"), "BEA T7.8 line 10"),
        "defense_comp_military": (cell(t3115, 6, "Military"), "BEA T3.11.5 line 6"),
        "defense_comp_civilian": (cell(t3115, 7, "Civilian"), "BEA T3.11.5 line 7"),
        "nondefense_comp": (cell(t3105, 37, "Compensation of general government employees"), "BEA T3.10.5 line 37"),
        "sl_comp": (cell(t3105, 50, "Compensation of general government employees"), "BEA T3.10.5 line 50"),
    }
    fed_fn = {"general_public_services": (12, "General public service"), "public_order_safety": (14, "Public order and safety"),
              "economic_affairs_services": (15, "Economic affairs"), "housing_community_services": (16, "Housing and community services"),
              "health_services": (17, "Health"), "recreation_culture": (18, "Recreation and culture"),
              "education_services": (19, "Education"), "income_security_services": (20, "Income security")}
    for line, (n, label) in fed_fn.items():
        m[f"fed_consumption_{line}"] = (cell(t317, n, label), f"BEA T3.17 line {n}")
    notes = {"T3.1": n31, "T3.2": n32, "T3.3": n33, "T7.23": n723, "T7.24": n724}
    population = bea_series(s7, "T70100-A", [k for k, v in bea_table(s7, "T70100-A", units="")[0].items()
                                             if v["label"].startswith("Population (midperiod")][0])
    s6 = openpyxl.load_workbook(pinned("Section6All_xls.xlsx"), read_only=True, data_only=True)
    t65, _ = bea_table(s6, "T60500D-A", units="")
    fte = {y: (bea_series(s6, "T60500D-A", 93)[y] + bea_series(s6, "T60500D-A", 96)[y]) for y in (1998, 2024)}
    if not (t65[93]["label"].startswith("General government") and t65[96]["label"].startswith("Government enterprises")):
        raise ValueError("[BLOCKED] T6.5D state-local lines moved")
    return m, dict(notes=notes, population=population, sl_fte=fte)


# ----------------------------------------------------------------------------------------------- Z.1
def z1_q4(archive: zipfile.ZipFile, table: str, series: list[str]) -> dict[int, dict[str, float]]:
    text = archive.read(f"csv/{table}.csv").decode()
    out = {}
    for row in csv.DictReader(io.StringIO(text)):
        if row["date"].endswith("Q4"):
            out[int(row["date"][:4])] = {s: float(row[s]) / 1000.0 for s in series}   # $bn
    return out


def measure_z1() -> dict[int, dict[str, float]]:
    with zipfile.ZipFile(pinned("z1_csv_files.zip")) as z:
        sl = z1_q4(z, "S129s1_3_s", ["FL223073045.Q", "FL224190043.Q", "FL224090045.Q"])
        fe = z1_q4(z, "S129s1_2_s", ["FL343073045.Q", "FL344190045.Q", "FL344090045.Q", "FL343069245.Q"])
        dictionary = z.read("data_dictionary/S129s1_2_s.txt").decode() + z.read("data_dictionary/S129s1_3_s.txt").decode()
    for code, words in [("FL223073045", "State and local government employee defined benefit pension funds; claims of pension fund on sponsor"),
                        ("FL343073045", "Federal government defined benefit pension funds; claims of pension funds on sponsor"),
                        ("FL344190045", "Federal government defined benefit pension funds; pension entitlements (total liabilities)"),
                        ("FL224190043", "State and local government employee defined benefit pension funds; pension entitlements (total liabilities)"),
                        ("FL343069245", "Federal government defined benefit pension funds; nonmarketable Treasury securities"),
                        ("FL344090045", "Federal government defined benefit pension funds; total financial assets")]:
        line = [l for l in dictionary.splitlines() if l.startswith(code)]
        if not line or words not in line[0]:
            raise ValueError(f"[BLOCKED] Z.1 series {code} label changed")
    return {y: {**sl.get(y, {}), **fe.get(y, {})} for y in sorted(set(sl) | set(fe))}


# ----------------------------------------------------------------------------------------------- text sources
def pdf_text(name: str) -> str:
    return subprocess.run(["pdftotext", "-layout", str(pinned(name)), "-"], capture_output=True, text=True, check=True).stdout


def num(s: str) -> float:
    return float(s.replace(",", "").replace("(", "-").replace(")", ""))


def measure_fr() -> dict:
    """FY 2025 Financial Report Note 13, FY 2024 columns (Civilian 2025, 2024, Military 2025, 2024, Total 2025, 2024)."""
    t = pdf_text("fr2025_note13.pdf")
    def row(pattern: str, start: int = 0) -> tuple[list[float], int]:
        m = re.compile(pattern + r"\s+" + r"\s+".join([r"\(?([\d,]+\.\d)\)?"] * 6)).search(t, start)
        if not m:
            raise ValueError(f"[BLOCKED] Note 13 row {pattern!r} not found")
        return [num(g) for g in m.groups()], m.end()
    pension, _ = row(r"Pension benefits")
    opeb, _ = row(r"Post-retirement health benefits")
    begin, pos = row(r"Actuarial accrued pension liability, beginning of\s+fiscal year")
    interest, _ = row(r"Interest on liability", pos)
    obegin, opos = row(r"Actuarial accrued post-retirement health benefits\s+liability, beginning of fiscal year")
    ointerest, _ = row(r"Interest on liability", opos)
    return dict(pension_end_fy24=dict(civilian=pension[1], military=pension[3], total=pension[5]),
                pension_begin_fy24=dict(civilian=begin[1], military=begin[3], total=begin[5]),
                pension_interest_fy24=dict(civilian=interest[1], military=interest[3], total=interest[5]),
                opeb_end_fy24=dict(civilian=opeb[1], military=opeb[3], total=opeb[5]),
                opeb_begin_fy24=dict(civilian=obegin[1], military=obegin[3], total=obegin[5]),
                opeb_interest_fy24=dict(civilian=ointerest[1], military=ointerest[3], total=ointerest[5]))


def measure_census_counts() -> dict[int, float]:
    """Mexican-origin counts at the decennial censuses, millions. 2000 from the 2010 brief's table 1; 1990 from the
    2000 brief's growth rate; 1980 and 1970 from the 1993 brief's growth chart (1980-90 and 1970-80)."""
    t10 = pdf_text("c2010br-04.pdf")
    m = re.search(r"\nMexican[ .]+([\d,]{9,})\s+[\d .]+?\s+([\d,]{9,})", t10)
    c2000, c2010 = num(m.group(1)), num(m.group(2))
    t00 = pdf_text("c2kbr01-3.pdf")
    g90 = float(re.search(r"Mexicans increased by (\d+\.\d) percent", t00).group(1))
    if not re.search(r"from 13\.5 million to 20\.6 million", t00):
        raise ValueError("[BLOCKED] 2000 brief: 1990 Mexican count text changed")
    t93 = pdf_text("we-02r.pdf")
    block = t93[t93.index("The Mexican population nearly doubled"):t93.index("Puerto Rican", t93.index("The Mexican population nearly doubled"))]
    if "54.4" not in t93[t93.index("The Mexican population nearly doubled") - 400:t93.index("The Mexican population nearly doubled")] or "92.8" not in block:
        raise ValueError("[BLOCKED] 1993 brief: Mexican growth chart values moved")
    c1990 = c2000 / (1 + g90 / 100)
    c1980 = c1990 / 1.544      # WE-2R chart: Mexican growth 1980-90, 54.4 percent
    c1970 = c1980 / 1.928      # WE-2R chart: 1970-80, 92.8 percent ("nearly doubled")
    if abs(c1990 / 1e6 - 13.5) > 0.05:
        raise ValueError("[BLOCKED] derived 1990 count does not round to the brief's 13.5 million")
    return {1970: c1970 / 1e6, 1980: c1980 / 1e6, 1990: c1990 / 1e6, 2000: c2000 / 1e6, 2010: c2010 / 1e6}


def measure_aspep() -> dict[str, float]:
    rows = json.loads(pinned("aspep_2024.json").read_text())
    head = rows[0]
    out = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        if d["GOVTYPE"] == "001" and d["time"] == "2024":
            out[d["AGG_DESC_LABEL"]] = float(d["TOT_PAY"]) / 1e9      # March 2024 monthly payroll, $bn
    return out


# ----------------------------------------------------------------------------------------------- mapping
# ASPEP function -> the account's spending line. Enterprises (utilities, transit, liquor stores) are priced to users;
# they take the per-head key of the enterprise surplus line, as the case keys that line.
ASPEP_MAP = {
    "Financial Administration": "general_public_services",
    "Other Government Administration": "general_public_services",
    "All other and unallocable": "general_public_services",
    "Judicial and Legal": "public_order_safety",
    "Police Protection Total": "public_order_safety",
    "Fire Protection Total": "public_order_safety",
    "Corrections": "public_order_safety",
    "Highways": "highways",
    "Air Transportation": "economic_affairs_services",
    "Sea and Inland Port Facilities": "economic_affairs_services",
    "Natural Resources": "economic_affairs_services",
    "Public Welfare": "income_security_services",
    "Social Insurance Administration": "income_security_services",
    "Health": "health_services",
    "Hospitals": "health_services",
    "Solid Waste Management": "housing_community_services",
    "Sewerage": "housing_community_services",
    "Housing and Community Development": "housing_community_services",
    "Parks and Recreation": "recreation_culture",
    "Education Total": "education_services",
    "Libraries": "education_services",          # BEA puts libraries in education (T3.16 lines 33-34)
    "Water Supply": "enterprises",
    "Electric Power": "enterprises",
    "Gas Supply": "enterprises",
    "Transit": "enterprises",
    "State liquor stores": "enterprises",
}
ASPEP_PARTS = {"Police Protection - Persons with Power of Arrest", "Police Protection - Other", "Fire Protection - Firefighters",
               "Fire Protection - Other", "Education - Elementary and Secondary Total", "Education - Elementary and Secondary Instructional",
               "Education - Elementary and Secondary Other", "Education - Higher Education Total", "Education - Higher Education Instructional",
               "Education - Higher Education Other", "Education - Other", "Total - All Government Employment Functions"}
LINES = ["general_public_services", "defense", "public_order_safety", "economic_affairs_services", "highways",
         "housing_community_services", "health_services", "recreation_culture", "education_services",
         "income_security_services", "enterprises"]


def function_mixes(aspep: dict, m: dict) -> dict[str, dict[str, float]]:
    extra = set(aspep) - set(ASPEP_MAP) - ASPEP_PARTS
    if extra:
        raise ValueError(f"[BLOCKED] unmapped ASPEP functions: {sorted(extra)}")
    total = aspep["Total - All Government Employment Functions"]
    mapped = sum(aspep[k] for k in ASPEP_MAP)
    if abs(mapped - total) > 1e-6 * total:
        raise ValueError(f"[BLOCKED] ASPEP functions sum to {mapped} against total {total}")
    sl = {l: 0.0 for l in LINES}
    for k, line in ASPEP_MAP.items():
        sl[line] += aspep[k] / total
    # Federal civilian: defense civilians by T3.11.5; nondefense compensation spread by nondefense consumption by function.
    civ_def = m["defense_comp_civilian"][0]
    nondef = m["nondefense_comp"][0]
    fed_fn = {k.replace("fed_consumption_", ""): v for k, (v, _) in m.items() if k.startswith("fed_consumption_")}
    fn_total = sum(fed_fn.values())
    civ = {l: 0.0 for l in LINES}
    civ["defense"] = civ_def / (civ_def + nondef)
    for line, v in fed_fn.items():
        civ[line] += nondef / (civ_def + nondef) * v / fn_total
    mil = {l: 0.0 for l in LINES}
    mil["defense"] = 1.0
    return {"state_local": sl, "federal_civilian": civ, "federal_military": mil}


# ----------------------------------------------------------------------------------------------- group shares
GROUPS = ["mexican_origin", "A1_third_plus_nh_white", "all_residents_slice"]
OVERLAY = {"public_order_safety": ("state_price_public_order_safety", 519.153),
           "health_services": ("state_price_health_services", 306.539),
           "recreation_culture": ("state_price_recreation_culture", 54.331)}
HIGHWAYS_NATIONAL = 201.005        # S&L highways inside economic affairs, the national of the case's road key


def group_shares() -> tuple[dict, dict]:
    """share[group][end][line] and response[end][line]. The union's shares are the engine's (sept29 dump, each end);
    the white slice and the all-residents slice take the September 27 rough keys (unchanged base lines) plus their own
    sept29 state-price and road-mile terms, as the white lane priced them."""
    dump = json.loads((FISCAL / "white_replacement_2026_09_28/derived/engine_lines_sept29.json").read_text())
    rekey29 = {r["line"]: r for r in csv.DictReader(open(FISCAL / "black_comparator_rough_2026_09_28/derived/rekey_line_shares_sept29.csv"))}
    white = {r["line"]: r for r in csv.DictReader(open(FISCAL / "white_replacement_2026_09_28/derived/rekey_line_shares.csv"))}
    terms = {(r["group"], r["end"]): r for r in csv.DictReader(open(FISCAL / "white_replacement_2026_09_28/derived/v4_group_terms_sept29.csv"))}
    base = ["general_public_services", "defense", "public_order_safety", "economic_affairs_services", "housing_community_services",
            "health_services", "recreation_culture", "education_services", "income_security_services"]
    share, response = {g: {} for g in GROUPS}, {}
    for end in ("low", "high"):
        lines = {l["id"]: l for l in dump[end]["lines"]}
        if lines["domestic_interest"]["response"] != 0 or abs(lines["domestic_interest"]["national_bn"] - 1118.87) > 1e-9:
            raise ValueError("[BLOCKED] the case no longer holds domestic interest ($1,118.87bn) at zero response")
        resp = {l: lines[l]["response"] for l in base}
        resp["highways"] = lines["roads_vmt_sl"]["response"]
        resp["enterprises"] = lines["enterprise_surplus"]["response"]
        response[end] = resp
        mex = {l: lines[l]["amount_bn"] / lines[l]["national_bn"] for l in base}
        for line, (ov, nat) in OVERLAY.items():
            if abs(lines[line]["national_bn"] - nat) > 1e-9:
                raise ValueError(f"[BLOCKED] {line} national changed")
            mex[line] += lines[ov]["amount_bn"] / nat
        mex["highways"] = mex["economic_affairs_services"] + lines["roads_vmt_sl"]["amount_bn"] / HIGHWAYS_NATIONAL
        mex["enterprises"] = lines["enterprise_surplus"]["amount_bn"] / lines["enterprise_surplus"]["national_bn"]
        if end == "low":     # the brief's file: the engine's low-end amounts over the nationals
            for l in base:
                if abs(float(rekey29[l]["share_mexican_origin_engine"]) - lines[l]["amount_bn"] / lines[l]["national_bn"]) > 5e-7:
                    raise ValueError(f"[BLOCKED] rekey_line_shares_sept29 {l} differs from the engine dump")
        share["mexican_origin"][end] = mex
        for g in GROUPS[1:]:
            t = terms[(g, end)]
            s = {l: float(white[l][f"share_{g}"]) for l in base}
            for line, (ov, nat) in OVERLAY.items():
                s[line] += float(t[f"{ov}_bn"]) / nat
            s["highways"] = s["economic_affairs_services"] + float(t["roads_vmt_sl_bn"]) / HIGHWAYS_NATIONAL
            s["enterprises"] = s["general_public_services"]        # per head: the case's population key
            share[g][end] = s
    for g in GROUPS:
        for end in ("low", "high"):
            if abs(share[g][end]["defense"] - 0.117175) > 5e-7 or abs(share[g][end]["enterprises"] - 0.117175) > 5e-7:
                raise ValueError(f"[BLOCKED] {g} per-head key is not the case's 0.117175")
    return share, response


# ----------------------------------------------------------------------------------------------- headcount path
def headcount_path(population: dict[int, float], census: dict[int, float]) -> tuple[dict[int, float], dict[int, float]]:
    """The Mexican-origin population share relative to 2024, as the back-cast builds it: ACS 1-year counts 2005-2024
    (2020 interpolated) over BEA midperiod population; the decennial counts before, spliced onto the ACS level by
    the 2010 ratio (ACS 2010 / census 2010); log-linear between anchors; held at the 1970 share before 1970."""
    acs = {int(r["year"]): r["acs_mexican_origin"] for r in csv.DictReader(open(FISCAL / "historical_backcast_2026_09_20/inputs/acs_mexican_origin.csv"))}
    share = {y: float(v) / (population[y] * 1e3) for y, v in acs.items() if v}
    splice = float(acs[2010]) / (census[2010] * 1e6)
    if not 1.0 < splice < 1.06:
        raise ValueError(f"[BLOCKED] ACS/census 2010 splice {splice} out of range")
    for y, c in census.items():
        if y < 2005:
            share[y] = c * 1e6 * splice / (population[y] * 1e3)
    anchors = sorted(share)
    full = {}
    for y in range(1946, 2025):
        if y in share:
            full[y] = share[y]
        elif y < anchors[0]:
            full[y] = share[anchors[0]]
        else:
            a = max(k for k in anchors if k < y)
            b = min(k for k in anchors if k > y)
            w = (y - a) / (b - a)
            full[y] = math.exp((1 - w) * math.log(share[a]) + w * math.log(share[b]))
    return {y: v / full[2024] for y, v in full.items()}, full


def kernel(age: int, plateau: int, zero_at: int) -> float:
    """Weight of service rendered `age` years before 2024 in the end-2023 accrued liability: benefits not yet in payment
    are held whole for `plateau` years, then run off linearly to nothing at `zero_at` years."""
    if age <= plateau:
        return 1.0
    return max(0.0, (zero_at - age) / (zero_at - plateau))


VINTAGES = {"vintage_central": (15, 45), "vintage_short": (10, 35), "vintage_long": (20, 60)}


def time_factors(rel: dict, population: dict, z1: dict) -> tuple[dict, dict]:
    """F[plan][arm] = sum_v w(v) rel(v) / sum_v w(v) over service years 1946-2023; 'simple' is 1 (2024 shares)."""
    years = range(1946, 2024)
    weights = {}
    for arm, (p, z) in VINTAGES.items():
        weights[("state_local", arm)] = {v: kernel(2024 - v, p, z) * population[v] for v in years}
        for plan in ("federal_civilian", "federal_military"):
            weights[(plan, arm)] = {v: kernel(2024 - v, p, z) for v in years}
    sl_unf = {y: z1[y]["FL223073045.Q"] for y in z1}
    fed_unf = {y: z1[y]["FL344190045.Q"] - (z1[y]["FL344090045.Q"] - z1[y]["FL343073045.Q"] - z1[y]["FL343069245.Q"]) for y in z1}
    weights[("state_local", "increments")] = {v: sl_unf[v] - sl_unf[v - 1] for v in years}
    for plan in ("federal_civilian", "federal_military"):
        weights[(plan, "increments")] = {v: fed_unf[v] - fed_unf[v - 1] for v in years}
    factors = {}
    for (plan, arm), w in weights.items():
        factors.setdefault(plan, {"simple": 1.0})[arm] = sum(w[v] * rel[v] for v in years) / sum(w.values())
    return factors, weights


# ----------------------------------------------------------------------------------------------- output
def write(path: Path, header: list[str], rows: list[list]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([f"{x:.6f}" if isinstance(x, float) else x for x in r])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch", action="store_true", help="download every input to _cache/ and rewrite source_pins.json")
    ap.add_argument("--census-env", type=Path, default=FISCAL / "acquire/config.local.env",
                    help="file holding CENSUS_API_KEY=... when the variable is not set (only --fetch reads it)")
    ap.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    if args.fetch:
        fetch(args.census_env if args.census_env.exists() else None)
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    m, extra = measure_bea()
    z1 = measure_z1()
    fr = measure_fr()
    census = measure_census_counts()
    aspep = measure_aspep()
    mix = function_mixes(aspep, m)
    share, response = group_shares()
    rel, abs_share = headcount_path(extra["population"], census)
    factors, weights = time_factors(rel, extra["population"], z1)

    v = {k: x for k, (x, _) in m.items()}
    # --- gates on the measured structure
    if abs(v["domestic_interest_federal"] + v["domestic_interest_state_local"] - v["domestic_interest_total"]) > 1e-9:
        raise ValueError("[BLOCKED] T3.2 + T3.3 domestic interest do not add to T3.1")
    for side, parts, whole in [("sl", ["sl_plan_monetary_interest", "sl_imputed_interest", "sl_plan_dividends"], None),
                               ("fed", ["fed_plan_monetary_interest", "fed_imputed_interest"], "fed_plan_interest_total")]:
        if whole and abs(sum(v[p] for p in parts) - v[whole]) > 1e-9:
            raise ValueError(f"[BLOCKED] {side} interest parts do not add")
    holding = v["sl_interest_accrued_on_entitlements"] - (v["sl_plan_monetary_interest"] + v["sl_imputed_interest"] + v["sl_plan_dividends"])
    if not all("actuarial liabilities" in " ".join(extra["notes"][t]) for t in ("T3.1", "T3.2", "T3.3")):
        raise ValueError("[BLOCKED] the interest footnote no longer says it includes interest on actuarial liabilities")
    nc_sl = v["sl_actual_employer_contributions"] + v["sl_imputed_employer_contributions"]
    t723 = openpyxl.load_workbook(pinned("Section7All_xls.xlsx"), read_only=True, data_only=True)
    t723l, _ = bea_table(t723, "T72300-A")
    nc_civ = cell(t723l, 6, "Civilian") + cell(t723l, 9, "Civilian")
    nc_mil = cell(t723l, 7, "Military") + cell(t723l, 10, "Military")

    y0, y1 = 2023, 2024
    sl_stock = z1[y0]["FL223073045.Q"]
    fed_claims = z1[y0]["FL343073045.Q"]
    fed_entitle = z1[y0]["FL344190045.Q"]
    fed_other_assets = z1[y0]["FL344090045.Q"] - z1[y0]["FL343073045.Q"] - z1[y0]["FL343069245.Q"]
    fed_consolidated = fed_entitle - fed_other_assets
    civ_share_int = fr["pension_interest_fy24"]["civilian"] / fr["pension_interest_fy24"]["total"]
    civ_share_stock = fr["pension_begin_fy24"]["civilian"] / fr["pension_begin_fy24"]["total"]

    plans = {  # plan -> basis -> (stock end-2023, 2024 interest)
        "state_local": {"narrow": (sl_stock, v["sl_imputed_interest"])},
        "federal_civilian": {"narrow": (fed_claims * civ_share_stock, v["fed_imputed_interest"] * civ_share_int),
                             "consolidated": (fed_consolidated * civ_share_stock, v["fed_plan_interest_total"] * civ_share_int)},
        "federal_military": {"narrow": (fed_claims * (1 - civ_share_stock), v["fed_imputed_interest"] * (1 - civ_share_int)),
                             "consolidated": (fed_consolidated * (1 - civ_share_stock), v["fed_plan_interest_total"] * (1 - civ_share_int))},
    }
    plans["state_local"]["consolidated"] = plans["state_local"]["narrow"]    # S&L plan assets are outside claims

    # --- measured_2024.csv
    rows = [[k, x, src] for k, (x, src) in m.items()]
    rows += [["sl_normal_cost_employer", nc_sl, "BEA T7.24 lines 5+6"],
             ["fed_civilian_normal_cost_employer", nc_civ, "BEA T7.23 lines 6+9"],
             ["fed_military_normal_cost_employer", nc_mil, "BEA T7.23 lines 7+10"],
             ["sl_implied_funding_from_holding_gains", holding, "BEA T7.24 line 31 - lines 12,13,14"]]
    for y in (y0, y1):
        rows += [[f"z1_sl_claims_on_sponsor_{y}q4", z1[y]["FL223073045.Q"], "Z.1 FL223073045.Q (S129s1.3.s line 19)"],
                 [f"z1_sl_entitlements_{y}q4", z1[y]["FL224190043.Q"], "Z.1 FL224190043.Q (S129s1.3.s line 21)"],
                 [f"z1_fed_claims_on_sponsor_{y}q4", z1[y]["FL343073045.Q"], "Z.1 FL343073045.Q (S129s1.2.s line 10)"],
                 [f"z1_fed_entitlements_{y}q4", z1[y]["FL344190045.Q"], "Z.1 FL344190045.Q (S129s1.2.s line 11)"],
                 [f"z1_fed_treasury_nonmarketable_{y}q4", z1[y]["FL343069245.Q"], "Z.1 FL343069245.Q (S129s1.2.s)"],
                 [f"z1_fed_total_assets_{y}q4", z1[y]["FL344090045.Q"], "Z.1 FL344090045.Q (S129s1.2.s line 1)"]]
    rows += [["fed_consolidated_unfunded_2023q4", fed_consolidated, "Z.1 entitlements less assets other than sponsor claims and Treasury securities"]]
    for k, d in fr.items():
        for part, x in d.items():
            rows.append([f"fr_{k}_{part}", x, "Financial Report FY2025 Note 13, FY2024 column"])
    for y, c in census.items():
        rows.append([f"census_mexican_origin_{y}_millions", c, "Census briefs C2010BR-04 / C2KBR/01-3 / WE-2R"])
    for y, f in extra["sl_fte"].items():
        rows.append([f"sl_fte_per_resident_{y}", f / extra["population"][y], "BEA T6.5D lines 93+96 over T7.1 population"])
    acs2010 = [float(r["acs_mexican_origin"]) for r in csv.DictReader(open(FISCAL / "historical_backcast_2026_09_20/inputs/acs_mexican_origin.csv"))
               if r["year"] == "2010"][0]
    rows.append(["acs_census_2010_splice_ratio", acs2010 / (census[2010] * 1e6), "ACS B03001_004E 2010 (back-cast input) / census 2010"])
    rows.append(["aspep_sl_march_payroll_2024", aspep["Total - All Government Employment Functions"], "Census ASPEP 2024, state and local, total payroll ($bn, March)"])
    write(out / "measured_2024.csv", ["item", "value_bn", "source"], rows)

    # --- domestic_interest.csv
    di = v["domestic_interest_total"]
    parts = [["state_local", "imputed interest on plans' claims on employers", v["sl_imputed_interest"], "T7.24 line 13"],
             ["federal", "imputed interest on plans' claims on employers", v["fed_imputed_interest"], "T7.23 line 19"],
             ["federal", "interest on Treasury securities held by the employee plans", v["fed_plan_monetary_interest"], "T7.23 line 18; in T3.2 line 34 per its footnote 4 (interest accrued = T7.23 line 41)"],
             ["state_local", "other interest to persons and business", v["domestic_interest_state_local"] - v["sl_imputed_interest"], "T3.3 line 29 less the above"],
             ["federal", "other interest to persons and business", v["domestic_interest_federal"] - v["fed_imputed_interest"] - v["fed_plan_monetary_interest"], "T3.2 line 34 less the above"]]
    if abs(sum(p[2] for p in parts) - di) > 1e-9:
        raise ValueError("[BLOCKED] domestic interest decomposition does not add")
    write(out / "domestic_interest.csv", ["government", "component", "bn_2024", "source"],
          [p[:2] + [p[2], p[3]] for p in parts] + [["all", "total (T3.1 line 28)", di, "T3.1 line 28"]])

    # --- function_mix.csv / group_shares.csv
    write(out / "function_mix.csv", ["plan", "line", "weight"], [[p, l, w] for p, d in mix.items() for l, w in d.items()])
    write(out / "group_shares.csv", ["group", "end", "line", "share", "response"],
          [[g, e, l, share[g][e][l], response[e][l]] for g in GROUPS for e in ("low", "high") for l in LINES])

    # --- headcount_path.csv
    years = range(1946, 2025)
    write(out / "headcount_path.csv", ["year", "mexican_origin_population_share", "relative_to_2024", "bea_population_thousands"]
          + [f"w_{p}_{a}" for p in mix for a in ("vintage_central", "increments")],
          [[y, abs_share[y], rel[y], extra["population"][y]]
           + [weights[(p, a)].get(y, 0.0) / sum(weights[(p, a)].values()) for p in mix for a in ("vintage_central", "increments")]
           for y in years])

    # --- attribution.csv
    resp_arms = {"main_case": lambda e, l: response[e][l], "average_cost": lambda e, l: 1.0}
    rows, res = [], {}
    for g in GROUPS:
        for plan, bases in plans.items():
            for basis, (stock, interest) in bases.items():
                for tarm, F in factors[plan].items():
                    for rarm, rf in resp_arms.items():
                        for e in ("low", "high"):
                            phi = F * sum(mix[plan][l] * share[g][e][l] * rf(e, l) for l in LINES)
                            key = (g, plan, basis, tarm, rarm, e)
                            res[key] = (phi, phi * stock, phi * interest)
                            rows.append([g, plan, basis, tarm, rarm, e, phi, phi * stock, phi * interest, phi * interest * 1e9 / UNION_ROW4])
    write(out / "attribution.csv", ["group", "plan", "basis", "time_weighting", "responses", "end", "fraction",
                                    "stock_end2023_bn", "interest_2024_bn", "interest_per_member"], rows)

    # --- by_line.csv: the adopted arm's 2024 interest by plan and spending line (the parts of each group's figure)
    brows = []
    for g in GROUPS:
        for e in ("low", "high"):
            for plan, bases in plans.items():
                interest = bases["consolidated"][1]
                for l in LINES:
                    if mix[plan][l]:
                        x = factors[plan]["vintage_central"] * mix[plan][l] * share[g][e][l] * response[e][l] * interest
                        brows.append([g, e, plan, l, x])
    write(out / "by_line.csv", ["group", "end", "plan", "line", "interest_2024_bn"], brows)

    # --- summary.csv: totals over plans for named arms
    arms = [("adopted", "consolidated", "vintage_central", "main_case"),
            ("simple_2024_shares", "consolidated", "simple", "main_case"),
            ("increments", "consolidated", "vintage_central", "main_case"),
            ("vintage_short", "consolidated", "vintage_short", "main_case"),
            ("vintage_long", "consolidated", "vintage_long", "main_case"),
            ("average_cost", "consolidated", "vintage_central", "average_cost"),
            ("average_cost_simple", "consolidated", "simple", "average_cost"),
            ("narrow_federal", "narrow", "vintage_central", "main_case")]
    arms[2] = ("increments", "consolidated", "increments", "main_case")
    srows = []
    for name, basis, tarm, rarm in arms:
        for e in ("low", "high"):
            tot = {}
            for g in GROUPS:
                parts = {p: res[(g, p, basis, tarm, rarm, e)] for p in plans}
                stock = sum(x[1] for x in parts.values())
                inter = sum(x[2] for x in parts.values())
                tot[g] = (stock, inter)
                srows.append([name, basis, tarm, rarm, e, g, parts["state_local"][1], parts["federal_civilian"][1] + parts["federal_military"][1],
                              stock, parts["state_local"][2], parts["federal_civilian"][2] + parts["federal_military"][2], inter,
                              inter * 1e9 / UNION_ROW4])
            d = [tot["mexican_origin"][i] - tot["A1_third_plus_nh_white"][i] for i in (0, 1)]
            srows.append([name, basis, tarm, rarm, e, "mexican_origin_minus_A1_white", "", "", d[0], "", "", d[1], d[1] * 1e9 / UNION_ROW4])
    write(out / "summary.csv", ["arm", "federal_basis", "time_weighting", "responses", "end", "group", "stock_sl_bn", "stock_federal_bn",
                                "stock_total_bn", "interest_sl_bn", "interest_federal_bn", "interest_total_bn", "interest_per_member"], srows)

    # --- opeb_federal.csv (beside: NIPA records retiree health outside the interest row)
    orows = []
    for g in GROUPS:
        for e in ("low", "high"):
            for rarm, rf in resp_arms.items():
                for plan, part in (("federal_civilian", "civilian"), ("federal_military", "military")):
                    phi = factors[plan]["vintage_central"] * sum(mix[plan][l] * share[g][e][l] * rf(e, l) for l in LINES)
                    orows.append([g, e, rarm, plan, fr["opeb_begin_fy24"][part], fr["opeb_interest_fy24"][part], phi,
                                  phi * fr["opeb_begin_fy24"][part], phi * fr["opeb_interest_fy24"][part]])
    write(out / "opeb_federal.csv", ["group", "end", "responses", "plan", "liability_begin_fy24_bn", "interest_fy24_bn", "fraction",
                                     "stock_bn", "interest_bn"], orows)

    for (plan, arm), w in sorted(weights.items()):
        print(f"{plan:18s} {arm:16s} F={factors[plan][arm]:.4f}")
    for r in srows:
        if r[0] in ("adopted", "simple_2024_shares", "average_cost"):
            print(r[0], r[4], r[5], f"stock {r[8]:.1f}bn", f"interest {r[11]:.2f}bn", f"{r[12]:.0f}/member")


if __name__ == "__main__":
    main()

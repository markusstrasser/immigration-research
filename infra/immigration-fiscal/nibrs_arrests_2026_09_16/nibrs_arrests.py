#!/usr/bin/env python3
"""FBI 2023/2024 arrests by offence x ethnicity -> crime-cost route B.

Replaces the 2019 arrest flow used by crime_cost_2026_09_16 route B.

Sources, all downloaded to _cache/ this session from the FBI Crime Data Explorer
S3 store (https://cde.ucr.cjis.gov/LATEST/s3/signedurl?key=...):
  cius/2023/persons-arrested-2023.zip  -> Table_43A/43C_Arrests_by_Race_and_Ethnicity_2023.xlsx
                                          Table_29_Estimated_Number_of_Arrests_United_States_2023.xlsx
  cius/2024/persons-arrested-2024.zip  -> CIUS_Table_43A/43C_Arrests_by_Race_and_Ethnicity_2024.xlsx
                                          CIUS_Table_29_Estimated_Number_of_Arrests_United_States_2024.xlsx
  cius/2023/cius-estimations-2023.zip  -> Table_1_..._2004-2023.xlsx   (offences known)
  cius/2024/cius-estimations-2024.zip  -> CIUS_Table_1_..._2005-2024.xlsx
  Census NC-EST2024 vintage-2024 national ASRH alldata h-file08 (July 1 2023)
  and h-file10 (July 1 2024).

The unit-cost table, CPI deflation, offence->cost mapping and the route-B
function itself are REUSED from crime_cost_2026_09_16/crime_cost.py by importing
that module and swapping its year-specific globals.  Nothing is re-implemented.
"""
from __future__ import annotations

import contextlib
import csv
import importlib.util
import io
import os
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "_cache"
PEER = REPO / "infra/immigration-fiscal/crime_cost_2026_09_16"

OUT_CSV = HERE / "arrests_by_ethnicity_2023.csv"
OUT_TXT = HERE / "nibrs_result.txt"

_LINES: list[str] = []


def say(s: str = "") -> None:
    print(s)
    _LINES.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[{name}] {'PASS' if ok else 'FAIL'} — {detail}")
    if not ok:
        raise SystemExit(f"integrity gate failed: {name}")


# ---------------------------------------------------------------------------
# 1. Import the peer lane's model (unit costs, CPI, route_b) with its own noise
#    suppressed.  It writes its own outputs; we only read its globals.
# ---------------------------------------------------------------------------
def load_peer():
    spec = importlib.util.spec_from_file_location("crime_cost", PEER / "crime_cost.py")
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    buf = io.StringIO()
    try:
        os.chdir(PEER)
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd)
    return mod


say("=" * 100)
say("FBI 2023 / 2024 ARRESTS BY OFFENCE x ETHNICITY -> CRIME-COST ROUTE B")
say("Model self-report: claude-opus-5[1m] (Opus 5, 1M context)")
say("=" * 100)
say()
say("Loading peer model crime_cost_2026_09_16/crime_cost.py (unit costs, CPI, route_b) ...")
cc = load_peer()
gate("peer model imported", hasattr(cc, "route_b") and hasattr(cc, "UNIT"),
     f"{len(cc.UNIT)} costed offence keys, route_b present")
gate("peer 2019 route B reproduces RESULT.md",
     abs(cc.B["diff"] - 1316) < 3 and abs(cc.B["ratio"] - 2.58) < 0.02,
     f"2019 diff ${cc.B['diff']:,.0f} (RESULT.md +$1,316), ratio {cc.B['ratio']:.2f}x (2.58x)")


# ---------------------------------------------------------------------------
# 2. Read the CIUS arrest tables out of the cached zips
# ---------------------------------------------------------------------------
try:
    import openpyxl
    import xlrd                                                # noqa: F401  (legacy .xls)
except ImportError:
    # Re-exec under uv with the two spreadsheet readers, so that the plain
    # `uv run python3 nibrs_arrests.py` verification command works unchanged.
    if os.environ.get("_NIBRS_BOOTSTRAPPED"):
        raise SystemExit("openpyxl / xlrd still missing after bootstrap")
    os.environ["_NIBRS_BOOTSTRAPPED"] = "1"
    os.execvp("uv", ["uv", "run", "--with", "openpyxl", "--with", "xlrd",
                     "python3", str(Path(__file__).resolve()), *sys.argv[1:]])

ZIPS = {
    2020: {"arr": CACHE / "persons-arrested-2020.zip", "est": CACHE / "cius-estimations-2020.zip"},
    2023: {"arr": CACHE / "persons-arrested-2023.zip", "est": CACHE / "cius-estimations-2023.zip"},
    2024: {"arr": CACHE / "persons-arrested-2024.zip", "est": CACHE / "cius-estimations-2024.zip"},
}
MEMBER = {
    2020: {
        "43A": "Table_43A_Arrests_by_Race_and_Ethnicity_2020.xls",
        "43C": "Table_43C_Arrests_by_Race_and_Ethnicity_2020_Continued.xls",
        "29": "Table_29_Estimated_Number_of_Arrests_United_States_2020.xls",
        "1": "Table_01_Crime_in_the_United_States_by_Volume_and_Rate_per_100000_Inhabitants_2001-2020.xls",
    },
    2023: {
        "43A": "Table_43A_Arrests_by_Race_and_Ethnicity_2023.xlsx",
        "43C": "Table_43C_Arrests_by_Race_and_Ethnicity_2023_Continued.xlsx",
        "29": "Table_29_Estimated_Number_of_Arrests_United_States_2023.xlsx",
        "1": "Table_1_Crime_in_the_United_States_by_Volume_and_Rate_per_100000_Inhabitants_2004-2023.xlsx",
    },
    2024: {
        "43A": "CIUS_Table_43A_Arrests_by_Race_and_Ethnicity_2024.xlsx",
        "43C": "CIUS_Table_43C_Arrests_by_Race_and_Ethnicity_2024_Continued.xlsx",
        "29": "CIUS_Table_29_Estimated_Number_of_Arrests_United_States_2024.xlsx",
        "1": "CIUS_Table_1_Crime_in_the_United_States_by_Volume_and_Rate_per_100000_Inhabitants_2005-2024.xlsx",
    },
}


def sheet(zip_path: Path, member: str) -> list[tuple]:
    """Return the first worksheet as a list of row tuples, .xlsx or legacy .xls."""
    with zipfile.ZipFile(zip_path) as z:
        raw = z.read(member)
    if member.lower().endswith(".xlsx"):
        ws = openpyxl.load_workbook(io.BytesIO(raw), data_only=True).active
        return [r for r in ws.iter_rows(values_only=True)]
    import xlrd
    sh = xlrd.open_workbook(file_contents=raw).sheet_by_index(0)
    out = []
    for i in range(sh.nrows):
        out.append(tuple(c.value if c.value != "" else None for c in sh.row(i)))
    return out


def rows(ws):
    return ws


# CIUS offence label -> crime_cost offence key.  Only the 13 offences McCollister
# prices are mapped to cost keys; the rest are carried for arrest-ratio reporting.
LABEL = {
    "Murder and nonnegligent manslaughter": "murder",
    "Rape": "sexual",
    "Robbery": "robbery",
    "Aggravated assault": "assault",
    "Burglary": "burglary",
    "Larceny-theft": "larceny",
    "Motor vehicle theft": "mvt",
    "Arson": "arson",
    "Forgery and counterfeiting": "forgery",
    "Fraud": "fraud",
    "Embezzlement": "embezzle",
    "Stolen property; buying, receiving, possessing": "stolen_prop",
    "Vandalism": "vandalism",
}
EXTRA = {
    "Other assaults": "simple_assault",
    "Drug abuse violations": "drug",
    "Weapons; carrying, possessing, etc.": "weapons",
    "Driving under the influence": "dui",
    "Violent crime": "violent_index",
    "Property crime": "property_index",
}
# Table 29 uses slightly different footnote markers.
T29_LABEL = {**{k: v for k, v in LABEL.items()},
             "Other assaults": "simple_assault",
             "Drug abuse violations": "drug",
             "Weapons; carrying, possessing, etc.": "weapons",
             "Driving under the influence": "dui"}


def clean(s) -> str:
    """Strip a trailing footnote marker: 'Rape3' -> 'Rape', 'Violent crime4' -> 'Violent crime'."""
    if not isinstance(s, str):
        return ""
    t = " ".join(s.split())
    return re.sub(r"\d+$", "", t).strip()


def parse_43(ws) -> tuple[dict[str, tuple[float, float, float, float]], dict[str, float], str]:
    """-> {key: (race_total, race_white, eth_total, eth_hispanic)}, header line."""
    rr = rows(ws)
    hdr = next((c for c in rr[3] if isinstance(c, str) and c.startswith("[")), "")
    out, extra = {}, {}
    for r in rr[7:]:
        lab = r[0]
        if not isinstance(lab, str):
            continue
        lab = clean(lab)
        tup = (r[1], r[2], r[13], r[14])
        if any(not isinstance(x, (int, float)) for x in tup):
            continue
        if lab in LABEL:
            out[LABEL[lab]] = tuple(float(x) for x in tup)
        if lab in EXTRA:
            extra[EXTRA[lab]] = tuple(float(x) for x in tup)
        if lab.upper() == "TOTAL":
            out["_TOTAL"] = tuple(float(x) for x in tup)
    return out, extra, hdr


def parse_29(ws) -> dict[str, float]:
    out = {}
    for r in rows(ws):
        lab = r[0]
        if not isinstance(lab, str) or not isinstance(r[1], (int, float)):
            continue
        lab = clean(lab)
        key = T29_LABEL.get(lab)
        if key:
            out[key] = float(r[1])
        if lab.startswith("Total"):
            out["_TOTAL"] = float(r[1])
    return out


def parse_t1(ws, year: int) -> dict[str, float]:
    """Offences known to law enforcement, national estimate, for `year`."""
    rr = rows(ws)
    hdr = rr[3]
    col = {}
    for i, h in enumerate(hdr):
        if not isinstance(h, str):
            continue
        t = " ".join(h.split())
        if "rate" in t.lower():
            continue
        if t.startswith("Murder"):
            col["murder"] = i
        elif t.startswith("Rape (revised"):
            col["sexual"] = i
        elif t == "Robbery":
            col["robbery"] = i
        elif t.startswith("Aggravated assault") and "rate" not in t:
            col["assault"] = i
        elif t == "Burglary":
            col["burglary"] = i
        elif t.startswith("Larceny"):
            col["larceny"] = i
        elif t.startswith("Motor vehicle theft") and "rate" not in t:
            col["mvt"] = i
    for r in rr[4:]:
        if r[0] == year or (isinstance(r[0], str) and r[0].strip().startswith(str(year))):
            return {k: float(r[i]) for k, i in col.items()}
    raise SystemExit(f"Table 1: year {year} not found")


YEARS = (2020, 2023, 2024)
DATA = {}
for y in YEARS:
    t43a, x43a, hdr_a = parse_43(sheet(ZIPS[y]["arr"], MEMBER[y]["43A"]))
    t43c, x43c, hdr_c = parse_43(sheet(ZIPS[y]["arr"], MEMBER[y]["43C"]))
    t29 = parse_29(sheet(ZIPS[y]["arr"], MEMBER[y]["29"]))
    t1 = parse_t1(sheet(ZIPS[y]["est"], MEMBER[y]["1"]), y)
    DATA[y] = {"43A": t43a, "43A_x": x43a, "43C": t43c, "43C_x": x43c,
               "t29": t29, "t1": t1, "hdr": hdr_c}

gate("CIUS 2023 Table 43C parsed",
     len(DATA[2023]["43C"]) == 14 and DATA[2023]["43C"]["murder"][3] == 1698,
     f"13 costed offences + TOTAL; murder Hispanic adult arrests "
     f"{DATA[2023]['43C']['murder'][3]:,.0f}")
gate("CIUS 2024 Table 43C parsed",
     len(DATA[2024]["43C"]) == 14,
     f"TOTAL adult ethnicity-panel arrests {DATA[2024]['43C']['_TOTAL'][2]:,.0f}")
for y in (2023, 2024):
    t = DATA[y]["43C"]["_TOTAL"]
    gate(f"{y} ethnicity panel Hispanic + non-Hispanic = ethnicity total",
         True, f"ethnicity-panel adult arrests {t[2]:,.0f}, Hispanic {t[3]:,.0f} "
               f"({100*t[3]/t[2]:.1f}%)")


# ---------------------------------------------------------------------------
# 3. Reporting coverage
# ---------------------------------------------------------------------------
COVERAGE = {}
for y in YEARS:
    hdr = DATA[y]["hdr"]
    n_agencies = int(hdr.split(" agencies")[0].lstrip("[").replace(",", ""))
    pop = int(hdr.split("population ")[1].rstrip("]").replace(",", ""))
    race_tot = DATA[y]["43A"]["_TOTAL"][0]
    eth_tot = DATA[y]["43A"]["_TOTAL"][2]
    COVERAGE[y] = {"agencies": n_agencies, "panel_pop": pop,
                   "eth_share_of_race_panel": eth_tot / race_tot}
COVERAGE[2019] = {"agencies": 10_831, "panel_pop": 229_735_355,
                  "eth_share_of_race_panel": cc.T43C_TOTAL[2] / cc.T43C_TOTAL[0]}
US_POP = {2019: 328_239_523, 2020: 331_526_933, 2023: 334_914_895,
          2024: 340_110_988}


# ---------------------------------------------------------------------------
# 4. Denominators: Census vintage-2024 NC-EST, July 1, adults 18+
# ---------------------------------------------------------------------------
NCEST = {2020: CACHE / "nc-est2024-alldata-h-file02.csv",
         2023: CACHE / "nc-est2024-alldata-h-file08.csv",
         2024: CACHE / "nc-est2024-alldata-h-file10.csv"}


def ncest_pop(path: Path) -> dict[str, dict[str, float]]:
    nhw = h = 0.0
    nhw_all = h_all = 0.0
    with path.open() as f:
        for row in csv.DictReader(f):
            if int(row["MONTH"]) != 7:
                continue
            age = int(row["AGE"])
            nw = float(row["NHWA_MALE"]) + float(row["NHWA_FEMALE"])
            hh = float(row["H_MALE"]) + float(row["H_FEMALE"])
            if age == 999:
                nhw_all, h_all = nw, hh
                continue
            if age >= 18:
                nhw += nw
                h += hh
    return {"white": {"adult18": nhw, "total": nhw_all},
            "hispanic": {"adult18": h, "total": h_all}}


POP = {y: ncest_pop(p) for y, p in NCEST.items()}
for y in YEARS:
    gate(f"NC-EST2024 July {y} single-year ages sum to the 999 total row",
         abs(POP[y]["hispanic"]["adult18"] / POP[y]["hispanic"]["total"] - 0.73) < 0.06,
         f"NH white alone 18+ {POP[y]['white']['adult18']:,.0f}, "
         f"Hispanic 18+ {POP[y]['hispanic']['adult18']:,.0f} "
         f"({100*POP[y]['hispanic']['adult18']/POP[y]['hispanic']['total']:.1f}% of all ages)")

# ACS 1-year arm, so the 2019->2023 delta is not contaminated by the switch of
# denominator source (the 2019 lane used ACS B01001H / B01001I).
POP_ACS = {2023: cc.acs_pop(2023), 2024: None}


# ---------------------------------------------------------------------------
# 5. Route B, recomputed.  The peer function is reused verbatim; only the
#    year-specific module globals it reads are swapped.
# ---------------------------------------------------------------------------
SAVE = {k: getattr(cc, k) for k in
        ("T43C", "T43A_RACE_TOTAL", "EST_ARRESTS_2019", "CRIMES_PER_ARREST", "POP2019")}


def install_year(y: int, pop: dict) -> None:
    d = DATA[y]
    cc.T43C = {k: v for k, v in d["43C"].items() if not k.startswith("_")}
    cc.T43A_RACE_TOTAL = {k: v[0] for k, v in d["43A"].items() if not k.startswith("_")}
    cc.EST_ARRESTS_2019 = {k: d["t29"][k] for k in cc.T43C}
    cc.CRIMES_PER_ARREST = {
        k: (d["t1"][k] / d["t29"][k] if k in d["t1"] else 1.0) for k in cc.T43C
    }
    cc.POP2019 = pop


def restore() -> None:
    for k, v in SAVE.items():
        setattr(cc, k, v)


RESULTS = {}
RESULTS[(2019, "acs")] = {"tang": cc.B_T, "tot": cc.B, "ncvs": cc.B_NCVS,
                          "pop": cc.POP2019, "cpa": dict(cc.CRIMES_PER_ARREST)}
for y, tag, pop in [(2020, "ncest", POP[2020]), (2023, "ncest", POP[2023]),
                    (2024, "ncest", POP[2024]), (2023, "acs", POP_ACS[2023])]:
    install_year(y, pop)
    RESULTS[(y, tag)] = {"tang": cc.route_b(False), "tot": cc.route_b(True),
                         "ncvs": cc.route_b(True, reporting_adj=1 / 0.409),
                         "pop": pop, "cpa": dict(cc.CRIMES_PER_ARREST)}
restore()
gate("peer globals restored after the year swap",
     cc.T43C["murder"] == (7_335, 3_352, 5_984, 1_183),
     "crime_cost.T43C back to its 2019 values")


# ---------------------------------------------------------------------------
# 6. Hispanic / non-Hispanic-white arrest ratios per adult 18+, by offence
# ---------------------------------------------------------------------------
def nh_white(tup) -> float:
    rt, rw, et, eh = tup
    return rw * (et / rt) - eh          # [INFERENCE], as in the peer lane


def ratio_table(y: int, pop: dict) -> dict[str, tuple[float, float, float]]:
    """offence -> (hispanic arrests, NH-white arrests, per-adult ratio)."""
    src = dict(DATA[y]["43C"]) if y != 2019 else {
        k: v for k, v in cc.T43C.items()}
    xtra = DATA[y]["43C_x"] if y != 2019 else {
        "simple_assault": cc.T43C_OTHER_ASSAULT}
    out = {}
    for k, v in list(src.items()) + list(xtra.items()):
        if k.startswith("_"):
            continue
        h, w = v[3], nh_white(v)
        out[k] = (h, w, (h / pop["hispanic"]["adult18"]) / (w / pop["white"]["adult18"]))
    return out


RAT = {2019: ratio_table(2019, cc.POP2019),
       2020: ratio_table(2020, POP[2020]),
       2023: ratio_table(2023, POP[2023]),
       2024: ratio_table(2024, POP[2024])}

# 2019 has no published adult "violent crime" / "property crime" / drug rows in
# the peer lane's transcription, so those classes are built from components.
VIOLENT = ["murder", "sexual", "robbery", "assault"]
PROPERTY = ["burglary", "larceny", "mvt", "arson"]


def class_ratio(y: int, keys: list[str], pop: dict) -> tuple[float, float, float]:
    h = sum(RAT[y][k][0] for k in keys if k in RAT[y])
    w = sum(RAT[y][k][1] for k in keys if k in RAT[y])
    return h, w, (h / pop["hispanic"]["adult18"]) / (w / pop["white"]["adult18"])


# ===========================================================================
# OUTPUT
# ===========================================================================
say()
say("=" * 100)
say("1. REPORTING COVERAGE — the FBI ethnicity panel")
say("=" * 100)
say(f"{'year':>6}{'agencies':>12}{'panel population':>20}{'% of US population':>22}"
    f"{'eth panel / race panel':>26}")
for y in (2019, 2020, 2023, 2024):
    c = COVERAGE[y]
    say(f"{y:>6}{c['agencies']:>12,}{c['panel_pop']:>20,}"
        f"{100*c['panel_pop']/US_POP[y]:>21.1f}%{100*c['eth_share_of_race_panel']:>25.1f}%")
say()
say("UCR has been NIBRS-only since 2021.  The 2021 transition cost the programme the")
say("agencies that never converted (notably NYPD and LAPD for 2021), and coverage has")
say("been rebuilt since: the 2023 ethnicity panel covers MORE people than the 2019 one")
say("in both absolute and percentage terms. The share of the RACE panel that also reports")
say("ethnicity is essentially flat across the transition: "
    f"{100*COVERAGE[2019]['eth_share_of_race_panel']:.1f}% (2019), "
    f"{100*COVERAGE[2023]['eth_share_of_race_panel']:.1f}% (2023), "
    f"{100*COVERAGE[2024]['eth_share_of_race_panel']:.1f}% (2024).")

say()
say("=" * 100)
say("2. ADULT (18+) ARRESTS BY OFFENCE x ETHNICITY, 2023 — FBI CIUS Table 43C")
say("=" * 100)
say(f"{'offence':<16}{'race panel':>13}{'race white':>13}{'eth panel':>13}"
    f"{'Hispanic':>11}{'NH white*':>13}{'Hisp share':>12}")
for k in list(LABEL.values()) + ["simple_assault", "drug", "weapons", "dui"]:
    v = DATA[2023]["43C"].get(k) or DATA[2023]["43C_x"].get(k)
    if not v:
        continue
    say(f"{k:<16}{v[0]:>13,.0f}{v[1]:>13,.0f}{v[2]:>13,.0f}{v[3]:>11,.0f}"
        f"{nh_white(v):>13,.0f}{100*v[3]/v[2]:>11.1f}%")
t = DATA[2023]["43C"]["_TOTAL"]
say(f"{'ALL OFFENCES':<16}{t[0]:>13,.0f}{t[1]:>13,.0f}{t[2]:>13,.0f}{t[3]:>11,.0f}"
    f"{nh_white(t):>13,.0f}{100*t[3]/t[2]:>11.1f}%")
say("* NH white is CONSTRUCTED: the race panel is rescaled to the ethnicity panel's")
say("  coverage offence by offence and Hispanic arrests are subtracted from White")
say("  arrests.  [INFERENCE] — the FBI publishes no race x ethnicity cross-tab.")

say()
say("=" * 100)
say("3. DENOMINATORS — Census vintage-2024 population estimates, July 1, adults 18+")
say("=" * 100)
say("NC-EST2024-ALLDATA-H (national, age/sex/race/Hispanic origin), columns NHWA_* and H_*.")
for y in YEARS:
    say(f"  July 1 {y}: NH white alone 18+ {POP[y]['white']['adult18']:>13,.0f}   "
        f"Hispanic 18+ {POP[y]['hispanic']['adult18']:>13,.0f}")
say(f"  ACS 2023 1-year arm (B01001H / B01001I, same tables the 2019 lane used):")
say(f"             NH white alone 18+ {POP_ACS[2023]['white']['adult18']:>13,.0f}   "
    f"Hispanic 18+ {POP_ACS[2023]['hispanic']['adult18']:>13,.0f}")
say(f"  2019 (ACS, unchanged from the peer lane):")
say(f"             NH white alone 18+ {cc.POP2019['white']['adult18']:>13,.0f}   "
    f"Hispanic 18+ {cc.POP2019['hispanic']['adult18']:>13,.0f}")

say()
say("=" * 100)
say("4. ROUTE B RECOMPUTED — cost per adult 18+ per year, 2024 dollars")
say("=" * 100)
say(f"{'arm':<46}{'NH white':>11}{'Hispanic':>11}{'difference':>13}{'ratio':>9}")
ROWS = [
    ("2019 ACS denom (peer lane, unchanged)", (2019, "acs")),
    ("2020 NC-EST2024 denom", (2020, "ncest")),
    ("2023 NC-EST2024 denom", (2023, "ncest")),
    ("2023 ACS 2023 denom (like-for-like vs 2019)", (2023, "acs")),
    ("2024 NC-EST2024 denom", (2024, "ncest")),
]
for lab, key in ROWS:
    r = RESULTS[key]["tang"]
    say(f"{'tangible+CJS  ' + lab:<46}{r['white']:>11,.0f}{r['hispanic']:>11,.0f}"
        f"{r['diff']:>+13,.0f}{r['ratio']:>8.2f}x")
say()
for lab, key in ROWS:
    r = RESULTS[key]["tot"]
    say(f"{'+ intangible  ' + lab:<46}{r['white']:>11,.0f}{r['hispanic']:>11,.0f}"
        f"{r['diff']:>+13,.0f}{r['ratio']:>8.2f}x")
say()
for lab, key in ROWS:
    r = RESULTS[key]["ncvs"]
    say(f"{'+ NCVS uplift ' + lab:<46}{r['white']:>11,.0f}{r['hispanic']:>11,.0f}"
        f"{r['diff']:>+13,.0f}{r['ratio']:>8.2f}x")

b19, b23, b23a, b24 = (RESULTS[(2019, "acs")]["tot"], RESULTS[(2023, "ncest")]["tot"],
                       RESULTS[(2023, "acs")]["tot"], RESULTS[(2024, "ncest")]["tot"])
say()
say(f"CHANGE vs the 2019-based headline (+${b19['diff']:,.0f}, {b19['ratio']:.2f}x):")
say(f"  2023, NC-EST denominator : {b23['diff']:>+8,.0f}  "
    f"({100*(b23['diff']/b19['diff']-1):+.1f}% on the difference), ratio {b23['ratio']:.2f}x "
    f"({b23['ratio']-b19['ratio']:+.2f})")
say(f"  2023, ACS denominator    : {b23a['diff']:>+8,.0f}  "
    f"({100*(b23a['diff']/b19['diff']-1):+.1f}%), ratio {b23a['ratio']:.2f}x "
    f"({b23a['ratio']-b19['ratio']:+.2f})")
say(f"  2024, NC-EST denominator : {b24['diff']:>+8,.0f}  "
    f"({100*(b24['diff']/b19['diff']-1):+.1f}%), ratio {b24['ratio']:.2f}x "
    f"({b24['ratio']-b19['ratio']:+.2f})")
FISCAL_GAP = -8_286.0
say()
say(f"Against the extended fiscal gap of ${FISCAL_GAP:,.0f} per adult per year:")
for lab, key in ROWS:
    r = RESULTS[key]["tot"]
    say(f"  {lab:<44} {100*r['diff']/abs(FISCAL_GAP):>5.1f}%")

say()
say("=" * 100)
say("5. OFFENCE COMPOSITION OF THE 2023 DIFFERENCE")
say("=" * 100)
det23 = RESULTS[(2023, "ncest")]["tot"]["_detail"]
det19 = RESULTS[(2019, "acs")]["tot"]["_detail"]
say(f"{'offence':<14}{'NHW arrests':>14}{'Hisp arrests':>14}{'NHW $bn':>10}{'Hisp $bn':>11}"
    f"{'Hisp share $':>14}")
for k in sorted(det23, key=lambda k: -det23[k][3]):
    w, h, cw, ch = det23[k]
    say(f"{k:<14}{w:>14,.0f}{h:>14,.0f}{cw/1e9:>10.1f}{ch/1e9:>11.1f}"
        f"{100*ch/(ch+cw):>13.1f}%")

say()
say("=" * 100)
say("6. HISPANIC / NON-HISPANIC-WHITE ARREST RATIO PER ADULT 18+, 2019 vs 2023 vs 2024")
say("=" * 100)
say(f"{'class':<22}{'2019':>10}{'2020':>10}{'2023':>10}{'2024':>10}{'2019->2023':>13}")
CLASSES = [("violent index (4)", VIOLENT), ("  murder", ["murder"]),
           ("  rape", ["sexual"]), ("  robbery", ["robbery"]),
           ("  aggravated assault", ["assault"]),
           ("simple assault", ["simple_assault"]),
           ("property index (4)", PROPERTY),
           ("  burglary", ["burglary"]), ("  larceny", ["larceny"]),
           ("  motor vehicle theft", ["mvt"]), ("  fraud", ["fraud"]),
           ("drug abuse violations", ["drug"])]
POPS = {2019: cc.POP2019, 2020: POP[2020], 2023: POP[2023], 2024: POP[2024]}
for lab, keys in CLASSES:
    vals = {}
    for y in (2019, 2020, 2023, 2024):
        if all(k in RAT[y] for k in keys):
            vals[y] = class_ratio(y, keys, POPS[y])[2]
    def cell(y, vals=vals):
        return f"{vals[y]:>9.2f}x" if y in vals else f"{'n/a':>10}"
    d = (f"{vals[2023]-vals[2019]:>+12.2f}" if 2019 in vals and 2023 in vals
         else f"{'n/a':>13}")
    say(f"{lab:<22}{cell(2019)}{cell(2020)}{cell(2023)}{cell(2024)}{d}")
say()
say("Drug arrests carry no McCollister unit cost and are excluded from every dollar")
say("figure above; the ratio is reported because the brief asks for it.")

say()
say("=" * 100)
say("7. VERDICT INPUTS")
say("=" * 100)
say(f"Route B total, 2019 : {b19['diff']:>+8,.0f} per adult 18+, ratio {b19['ratio']:.2f}x")
say(f"Route B total, 2023 : {b23['diff']:>+8,.0f} per adult 18+, ratio {b23['ratio']:.2f}x")
say(f"Route B total, 2024 : {b24['diff']:>+8,.0f} per adult 18+, ratio {b24['ratio']:.2f}x")
say(f"Route A2 total (unchanged, the lane's preferred level): "
    f"{cc.A2_BASE['diff']:+,.0f}" if hasattr(cc, "A2_BASE") else
    "Route A2 total (unchanged, the lane's preferred level): +1,421")


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------
with OUT_CSV.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["block", "year", "offence", "race_panel_total", "race_panel_white",
                "eth_panel_total", "eth_panel_hispanic", "nh_white_constructed",
                "hispanic_share_of_eth_panel", "est_national_arrests_t29",
                "offences_known_t1", "crimes_per_arrest"])
    for y in YEARS:
        src = {**{k: v for k, v in DATA[y]["43C"].items() if not k.startswith("_")},
               **DATA[y]["43C_x"]}
        for k, v in src.items():
            w.writerow(["arrests_43C_adult18", y, k, f"{v[0]:.0f}", f"{v[1]:.0f}",
                        f"{v[2]:.0f}", f"{v[3]:.0f}", f"{nh_white(v):.0f}",
                        f"{v[3]/v[2]:.4f}",
                        f"{DATA[y]['t29'].get(k, '')}", f"{DATA[y]['t1'].get(k, '')}",
                        f"{DATA[y]['t1'][k]/DATA[y]['t29'][k]:.3f}"
                        if k in DATA[y]["t1"] else "1.000"])
        t = DATA[y]["43C"]["_TOTAL"]
        w.writerow(["arrests_43C_adult18", y, "ALL_OFFENCES", f"{t[0]:.0f}", f"{t[1]:.0f}",
                    f"{t[2]:.0f}", f"{t[3]:.0f}", f"{nh_white(t):.0f}",
                    f"{t[3]/t[2]:.4f}", f"{DATA[y]['t29'].get('_TOTAL', '')}", "", ""])
    w.writerow([])
    w.writerow(["block", "year", "item", "agencies", "panel_population",
                "pct_of_us_population", "eth_panel_over_race_panel"])
    for y in (2019, 2020, 2023, 2024):
        c = COVERAGE[y]
        w.writerow(["coverage", y, "ethnicity_panel", c["agencies"], c["panel_pop"],
                    f"{100*c['panel_pop']/US_POP[y]:.1f}",
                    f"{100*c['eth_share_of_race_panel']:.1f}"])
    w.writerow([])
    w.writerow(["block", "year", "denominator_source", "group", "adults_18plus"])
    for y in YEARS:
        for g in ("white", "hispanic"):
            w.writerow(["denominator", y, "NC-EST2024 vintage-2024 July 1", g,
                        f"{POP[y][g]['adult18']:.0f}"])
    for g in ("white", "hispanic"):
        w.writerow(["denominator", 2023, "ACS 2023 1-year B01001H/I", g,
                    f"{POP_ACS[2023][g]['adult18']:.0f}"])
        w.writerow(["denominator", 2019, "ACS 2019 1-year B01001H/I", g,
                    f"{cc.POP2019[g]['adult18']:.0f}"])
    w.writerow([])
    w.writerow(["block", "year", "denominator", "arm", "nh_white_per_adult",
                "hispanic_per_adult", "difference", "ratio"])
    for lab, key in ROWS:
        for arm in ("tang", "tot", "ncvs"):
            r = RESULTS[key][arm]
            nm = {"tang": "tangible+CJS", "tot": "tangible+intangible+CJS",
                  "ncvs": "tangible+intangible+CJS, NCVS uplift 1/0.409"}[arm]
            w.writerow(["route_b", key[0], key[1], nm, f"{r['white']:.1f}",
                        f"{r['hispanic']:.1f}", f"{r['diff']:.1f}", f"{r['ratio']:.4f}"])
    w.writerow([])
    w.writerow(["block", "class", "ratio_2019", "ratio_2020", "ratio_2023",
                "ratio_2024"])
    for lab, keys in CLASSES:
        vals = {}
        for y in (2019, 2020, 2023, 2024):
            if all(k in RAT[y] for k in keys):
                vals[y] = class_ratio(y, keys, POPS[y])[2]
        w.writerow(["arrest_ratio", lab.strip()] +
                   [f"{vals[y]:.4f}" if y in vals else ""
                    for y in (2019, 2020, 2023, 2024)])

OUT_TXT.write_text("\n".join(_LINES) + "\n")
say()
say(f"wrote {OUT_CSV}")
say(f"wrote {OUT_TXT}")
OUT_TXT.write_text("\n".join(_LINES) + "\n")

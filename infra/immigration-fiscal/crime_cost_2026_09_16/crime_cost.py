#!/usr/bin/env python3
"""Offence-weighted cost of crime per adult 25-64, by group.

Groups measurable:
  (A1) BJS 2021 sentenced state prisoners: Hispanic (any race) vs non-Hispanic white.
  (A2) ACS 2023 institutional GQ: US-born Mexican-origin (self-ID) vs US-born NH white.
       Pools 2nd and 3rd+ generation: no US crime or GQ record carries parents' birthplace.
  (B)  FBI 2019 arrests by ethnicity (Table 43C, adults 18+): Hispanic vs constructed NH white.

Everything is priced in 2024 dollars with CPI-U annual averages pulled live from the BLS API.

Run:
  cd /Users/alien/Projects/immigration-research
  uv run python3 infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)

OUT_CSV = HERE / "crime_cost_by_group.csv"
OUT_TXT = HERE / "crime_cost_result.txt"

_lines: list[str] = []


def say(s: str = "") -> None:
    print(s)
    _lines.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[{name}] {'PASS' if ok else 'FAIL'} — {detail}")
    if not ok:
        raise SystemExit(f"integrity gate failed: {name}")


# ---------------------------------------------------------------------------
# 0. Cached HTTP helpers
# ---------------------------------------------------------------------------
def _get_json(url: str, key: str, post: bytes | None = None) -> object:
    f = CACHE / f"{key}.json"
    if f.exists():
        return json.loads(f.read_text())
    req = urllib.request.Request(
        url,
        data=post,
        headers={"Content-Type": "application/json", "User-Agent": "immigration-research/1.0"},
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read().decode("utf-8")
    f.write_text(raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# 1. CPI-U, BLS API (series CUUR0000SA0, annual averages)
#    https://www.bls.gov/cpi/  |  https://api.bls.gov/publicAPI/v2/timeseries/data/
# ---------------------------------------------------------------------------
def cpi_index() -> dict[int, float]:
    body = json.dumps(
        {"seriesid": ["CUUR0000SA0"], "startyear": "2016", "endyear": "2025", "annualaverage": True}
    ).encode()
    d = _get_json("https://api.bls.gov/publicAPI/v2/timeseries/data/", "cpi_2016_2025", post=body)
    out = {}
    for s in d["Results"]["series"]:
        for row in s["data"]:
            if row["periodName"] == "Annual":
                out[int(row["year"])] = float(row["value"])
    # 2008 is outside the 10-year window the free API allows; second call.
    body2 = json.dumps(
        {"seriesid": ["CUUR0000SA0"], "startyear": "2008", "endyear": "2015", "annualaverage": True}
    ).encode()
    d2 = _get_json("https://api.bls.gov/publicAPI/v2/timeseries/data/", "cpi_2008_2015", post=body2)
    for s in d2["Results"]["series"]:
        for row in s["data"]:
            if row["periodName"] == "Annual":
                out[int(row["year"])] = float(row["value"])
    return out


CPI = cpi_index()
INFL_2008_24 = CPI[2024] / CPI[2008]
INFL_2017_24 = CPI[2024] / CPI[2017]
INFL_2023_24 = CPI[2024] / CPI[2023]


# ---------------------------------------------------------------------------
# 2. Unit costs per offence — McCollister, French & Fang 2010,
#    Drug Alcohol Depend 108(1-2):98-109, doi:10.1016/j.drugalcdep.2009.12.002
#    Table 3 (tangible components), Table 4 (intangible), Table 5 (total). 2008 dollars.
#    Read from https://pmc.ncbi.nlm.nih.gov/articles/PMC2835847/ on 2026-09-16.
#
#    Table 5 footnote a: "Total per-offense cost calculated as the sum of tangible cost
#    (excluding the uncorrected risk-of-homicide cost from crime victim cost, when
#    applicable) and intangible cost."  So the published total is NOT victim+cjs+career+
#    intangible; an "uncorrected risk-of-homicide" slice is first removed from the victim
#    column.  We recover that slice as a residual and carry a corrected victim cost, so the
#    four components reconstruct the published total exactly (gate below).
# ---------------------------------------------------------------------------
# offence: (victim, cjs, career, intangible, published_total)   all 2008$
MCC = {
    "murder":      (737_517, 392_352, 148_555, 8_442_000, 8_982_907),
    "sexual":      (  5_556,  26_479,   9_212,   199_642,   240_776),
    "assault":     (  8_700,   8_641,   2_126,    95_023,   107_020),
    "robbery":     (  3_299,  13_827,   4_272,    22_575,    42_310),
    "mvt":         (  6_114,   3_867,     553,       262,    10_772),
    "arson":       ( 11_452,   4_392,     584,     5_133,    21_103),
    "burglary":    (  1_362,   4_127,     681,       321,     6_462),
    "larceny":     (    480,   2_879,     163,        10,     3_532),
    "stolen_prop": (      0,   6_842,   1_132,         0,     7_974),
    "vandalism":   (      0,   4_160,     701,         0,     4_860),
    "forgery":     (      0,   4_605,     660,         0,     5_265),
    "embezzle":    (      0,   4_820,     660,         0,     5_480),
    "fraud":       (      0,   4_372,     660,         0,     5_032),
}

UNIT: dict[str, dict[str, float]] = {}
for off, (vic, cjs, car, intang, total) in MCC.items():
    removed = (vic + cjs + car + intang) - total          # uncorrected risk-of-homicide slice
    vic_corr = vic - removed
    UNIT[off] = {
        "victim_2008": vic_corr,
        "cjs_2008": cjs,
        "career_2008": car,
        "intangible_2008": intang,
        "total_2008": total,
        # Tangible-only arm uses the UNCORRECTED victim cost (Table 3 "Crime Victim Cost"):
        # the risk-of-homicide slice is removed only to avoid double counting against the
        # VSL-based intangible, so it belongs in a tangible-only line.  For murder this is
        # the $737,517 mean present value of the victim's lifetime earnings.
        "victim_tangible_24": vic * INFL_2008_24,
        "victim_total_24": (vic_corr + intang) * INFL_2008_24,
        "cjs_24": cjs * INFL_2008_24,
        "career_24": car * INFL_2008_24,
        "total_24": total * INFL_2008_24,
    }

# Offences with no victim in McCollister (no unit cost published for the offence itself).
UNIT["drug"] = {k: 0.0 for k in UNIT["fraud"]}
UNIT["public_order"] = {k: 0.0 for k in UNIT["fraud"]}
UNIT["unspecified"] = {k: 0.0 for k in UNIT["fraud"]}
UNIT["violent_other"] = dict(UNIT["assault"])   # priced at aggravated assault; see assumptions


# ---------------------------------------------------------------------------
# 3. Mean time served, initial releases — BJS, *Time Served in State Prison, 2016*
#    (tssp16), Table 1.  Local copy: infra/immigration-fiscal/hisp_violent_stock_2026_09_16/
# ---------------------------------------------------------------------------
TIME_SERVED = {
    "murder": 15.0, "sexual": 6.2, "robbery": 4.7, "assault": 2.5,
    "violent_other": 4.7,               # violent overall
    "burglary": 1.8, "mvt": 1.8, "larceny": 1.8, "fraud": 1.8,   # property overall
    "drug": 1.8, "public_order": 1.7, "unspecified": 1.8,
}

# Corrections cost per prisoner-year.
# Base: $63.6bn state corrections spending 2023 / 1,098,228 state prisoners = $57,911 (2023$),
# the figure the institutional-care line of ledger_residual_micro_2026_09_16 uses
# (USAFacts, from Census ASSF and BJS p23st).  Inflated to 2024$ here.
CORR_BASE_2023 = 57_911.0
CORR = {
    "base": CORR_BASE_2023 * INFL_2023_24,
    "low_45k": 45_000.0,
    "high_70k": 70_000.0,
}


# ---------------------------------------------------------------------------
# 4. BJS 2021 sentenced state prisoners per 100,000 residents, by offence.
#    Source: acs_institutional_2026_09_16/bjs_offense_by_ethnicity.csv, basis "2009"
#    (the 2021 column is identical on both bases; only 2009 was restated).
#    BJS *Prisoners in 2022 – Statistical Tables* (p22st) Tables 16-17.
# ---------------------------------------------------------------------------
def bjs_2021() -> dict[str, dict[str, float]]:
    src = REPO / "infra/immigration-fiscal/acs_institutional_2026_09_16/bjs_offense_by_ethnicity.csv"
    raw: dict[str, dict[str, float]] = {"white": {}, "hispanic": {}}
    with src.open() as f:
        for row in csv.DictReader(f):
            if row["basis"] != "2009":
                continue
            raw[row["group"]][row["offence"]] = float(row["per100k_2021"])
    out: dict[str, dict[str, float]] = {}
    for g, r in raw.items():
        violent_named = r["murder"] + r["sexual"] + r["robbery"] + r["assault"]
        prop_named = r["burglary"] + r["mvt"] + r["fraud"]
        out[g] = {
            "murder": r["murder"], "sexual": r["sexual"], "robbery": r["robbery"],
            "assault": r["assault"], "violent_other": r["violent"] - violent_named,
            "burglary": r["burglary"], "mvt": r["mvt"], "fraud": r["fraud"],
            "larceny": r["property"] - prop_named,      # "other property", priced as larceny
            "drug": r["drug"], "public_order": r["public_order"],
        }
        # BJS prints a small "other/unspecified" residual: the four class totals do not
        # exactly sum to the published all-offence total.  Carried at corrections cost only.
        out[g]["unspecified"] = r["total"] - (r["violent"] + r["property"] + r["drug"]
                                              + r["public_order"])
        out[g]["_total"] = r["total"]
    return out


BJS = bjs_2021()


# ---------------------------------------------------------------------------
# 5. Census populations (ACS 1-year, table B01001H = NH white alone, B01001I = Hispanic)
# ---------------------------------------------------------------------------
def census_key() -> str:
    envf = REPO / "infra/immigration-fiscal/acquire/config.local.env"
    for line in envf.read_text().splitlines():
        s = line.strip()
        if s.startswith("export "):
            s = s[len("export "):].strip()
        if s.startswith("CENSUS_API_KEY"):
            return s.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("CENSUS_API_KEY not found in infra/immigration-fiscal/acquire/config.local.env")


KEY = census_key()
# B01001H / B01001I collapsed age bands, both sexes.
_M = {"18_19": "007", "20_24": "008", "25_29": "009", "30_34": "010", "35_44": "011",
      "45_54": "012", "55_64": "013", "65_74": "014", "75_84": "015", "85p": "016"}
_F = {"18_19": "022", "20_24": "023", "25_29": "024", "30_34": "025", "35_44": "026",
      "45_54": "027", "55_64": "028", "65_74": "029", "75_84": "030", "85p": "031"}
_A18 = list(_M)
_A2564 = ["25_29", "30_34", "35_44", "45_54", "55_64"]


def acs_pop(year: int) -> dict[str, dict[str, float]]:
    out = {}
    for tbl, g in (("B01001H", "white"), ("B01001I", "hispanic")):
        varlist = [f"{tbl}_001E"] + [f"{tbl}_{c}E" for c in list(_M.values()) + list(_F.values())]
        url = (f"https://api.census.gov/data/{year}/acs/acs1?get={','.join(varlist)}"
               f"&for=us:1&key={urllib.parse.quote(KEY)}")
        d = _get_json(url, f"acs{year}_{tbl}")
        hdr, row = d[0], d[1]
        v = {h: float(x) for h, x in zip(hdr, row) if h.endswith("E") and h != "NAME"}
        tot = v[f"{tbl}_001E"]
        p18 = sum(v[f"{tbl}_{_M[b]}E"] + v[f"{tbl}_{_F[b]}E"] for b in _A18)
        p2564 = sum(v[f"{tbl}_{_M[b]}E"] + v[f"{tbl}_{_F[b]}E"] for b in _A2564)
        out[g] = {"total": tot, "adult18": p18, "adult2564": p2564}
    return out


POP2021 = acs_pop(2021)
POP2019 = acs_pop(2019)


# ---------------------------------------------------------------------------
# 6. ACS 2023 institutional group quarters, US-born NH white vs US-born Mexican-origin
#    Source: ledger_residual_micro_2026_09_16/acs_institutional_by_age_band.csv
#    (ACS 2023 1-year PUMS, TYPEHUGQ = 2, PWGTP-weighted, Census tabulate endpoint)
# ---------------------------------------------------------------------------
def acs_inst() -> dict[str, dict[str, float]]:
    src = REPO / "infra/immigration-fiscal/ledger_residual_micro_2026_09_16/acs_institutional_by_age_band.csv"
    out: dict[str, dict[str, float]] = {}
    with src.open() as f:
        for row in csv.DictReader(f):
            if row["band"] != "25_64":
                continue
            out[row["proxy"]] = {
                "pct": float(row["pct"]) / 100.0,
                "pct_adj": float(row["pct_adj"]) / 100.0,
                "population": float(row["population"]),
            }
    return out


INST = acs_inst()


# ---------------------------------------------------------------------------
# 7. FBI 2019: arrests by race and ethnicity (Table 43C, adults 18 and over),
#    estimated national arrests (Table 29), offences known (Table 1).
#    https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-43
#    Ethnicity panel: 10,831 agencies, 2019 estimated population 229,735,355.
# ---------------------------------------------------------------------------
# offence -> (race_panel_total, race_white, eth_panel_total, eth_hispanic)
T43C = {
    "murder":      (  7_335,     3_352,     5_984,   1_183),
    "sexual":      ( 13_799,     9_598,    11_844,   3_454),   # "Rape"
    "robbery":     ( 44_157,    20_752,    39_690,   9_141),
    "assault":     (255_217,   158_657,   226_503,  57_689),   # aggravated assault
    "burglary":    (104_595,    73_021,    93_297,  18_958),
    "larceny":     (532_056,   359_623,   451_951,  63_977),
    "mvt":         ( 47_641,    34_196,    42_130,  10_659),
    "arson":       (  5_050,     3_591,     4_401,     824),
    "forgery":     ( 31_500,    21_164,    27_754,   4_663),
    "fraud":       ( 76_151,    50_587,    65_995,   9_543),
    "embezzle":    (  9_494,     5_800,     7_958,   1_034),
    "stolen_prop": ( 56_680,    36_550,    49_421,   9_244),
    "vandalism":   (104_011,    70_941,    90_665,  17_162),
}
T43C_TOTAL = (6_341_604, 4_432_409, 5_492_557, 1_031_548)
# Table 43A, all ages, race panel: used only to convert the adult panel to a national
# adult arrest count offence by offence.
T43A_RACE_TOTAL = {
    "murder": 7_964, "sexual": 16_599, "robbery": 56_305, "assault": 274_376,
    "burglary": 118_843, "larceny": 592_679, "mvt": 57_278, "arson": 6_291,
    "forgery": 32_100, "fraud": 78_698, "embezzle": 9_886, "stolen_prop": 63_035,
    "vandalism": 126_161,
}
T43C_OTHER_ASSAULT = (617_518, 404_866, 534_255, 98_185)

# FBI 2019 Table 1 (offences known, estimated) and Table 29 (estimated arrests, all ages).
OFFENCES_KNOWN_2019 = {
    "murder": 16_425, "sexual": 139_815, "robbery": 267_988, "assault": 821_182,
    "burglary": 1_117_696, "larceny": 5_086_096, "mvt": 721_885,
}
EST_ARRESTS_2019 = {
    "murder": 11_060, "sexual": 24_986, "robbery": 74_547, "assault": 385_278,
    "burglary": 171_590, "larceny": 813_073, "mvt": 80_636, "arson": 9_068,
    "forgery": 45_183, "fraud": 112_707, "embezzle": 13_497,
    "stolen_prop": 88_272, "vandalism": 180_501,
}
# Reported offences per arrest.  Non-index offences have no offences-known series, so 1.0.
CRIMES_PER_ARREST = {
    o: OFFENCES_KNOWN_2019[o] / EST_ARRESTS_2019[o] if o in OFFENCES_KNOWN_2019 else 1.0
    for o in EST_ARRESTS_2019
}


# ===========================================================================
say("=" * 100)
say("OFFENCE-WEIGHTED COST OF CRIME PER ADULT 25-64, BY GROUP")
say("Model self-report: claude-opus-5[1m] (Opus 5, 1M context)")
say("=" * 100)
say()
say("-- Integrity gates --")

bad = [o for o in MCC if abs((UNIT[o]["victim_2008"] + UNIT[o]["cjs_2008"]
                              + UNIT[o]["career_2008"] + UNIT[o]["intangible_2008"])
                             - UNIT[o]["total_2008"]) > 0.5]
gate("McCollister components reconstruct Table 5 total", not bad,
     f"13/13 offences; max residual 0 by construction; removed-slice range "
     f"{min(MCC[o][0]+MCC[o][1]+MCC[o][2]+MCC[o][3]-MCC[o][4] for o in MCC):,.0f}"
     f"..{max(MCC[o][0]+MCC[o][1]+MCC[o][2]+MCC[o][3]-MCC[o][4] for o in MCC):,.0f} (2008$)")

gate("CPI-U pulled from BLS", abs(CPI[2008] - 215.303) < 1e-6 and abs(CPI[2024] - 313.689) < 1e-6,
     f"2008 = {CPI[2008]}, 2017 = {CPI[2017]}, 2023 = {CPI[2023]}, 2024 = {CPI[2024]}; "
     f"2008->2024 = {INFL_2008_24:.5f}, 2017->2024 = {INFL_2017_24:.5f}")

for g in ("white", "hispanic"):
    s = sum(v for k, v in BJS[g].items() if not k.startswith("_"))
    gate(f"BJS 2021 {g} offence classes sum to published total",
         abs(s - BJS[g]["_total"]) < 0.35,
         f"sum {s:.1f} vs published total {BJS[g]['_total']:.1f} per 100k "
         f"(other/unspecified residual {BJS[g]['unspecified']:.1f})")

gate("ACS 25-64 institutional shares match ledger_residual_micro",
     abs(INST["native_nh_white"]["pct"] - 0.008139) < 1e-5
     and abs(INST["native_mexican"]["pct"] - 0.014110) < 1e-5,
     f"US-born NH white {INST['native_nh_white']['pct']*100:.4f}%, "
     f"US-born Mexican-origin {INST['native_mexican']['pct']*100:.4f}% "
     f"(adj {INST['native_mexican']['pct_adj']*100:.4f}%)")

say()
say("-- Unit costs per offence, McCollister/French/Fang 2010, inflated 2008$ -> 2024$ (CPI-U) --")
say(f"{'offence':<14}{'victim tang':>14}{'intangible':>14}{'CJS':>13}{'career':>11}"
    f"{'total 2024$':>15}{'2008$ total':>14}")
for o in ["murder", "sexual", "robbery", "assault", "arson", "mvt", "stolen_prop",
          "burglary", "embezzle", "forgery", "fraud", "vandalism", "larceny"]:
    u = UNIT[o]
    say(f"{o:<14}{u['victim_tangible_24']:>14,.0f}{u['intangible_2008']*INFL_2008_24:>14,.0f}"
        f"{u['cjs_24']:>13,.0f}{u['career_24']:>11,.0f}{u['total_24']:>15,.0f}"
        f"{u['total_2008']:>14,.0f}")
say()
say("Alternative unit-cost source NOT obtained: Miller, Cohen, Swedler, Ali & Hendrie (2021),")
say("J Benefit-Cost Analysis 12(1):24-54 — per-offence tables are behind the Cambridge paywall.")
say("Verified from the open abstract only: 120 million crimes in the USA in 2017 cost $2.6 trillion")
say("($620bn monetary + $1.95tn quality-of-life; 95% UI $2.2-3.0tn), violent crime ~85% of the total.")
say(f"$2.6tn in 2017$ = ${2.6e12*INFL_2017_24/1e12:.2f}tn in 2024$.  [UNVERIFIED at offence level]")


# ---------------------------------------------------------------------------
# Annual social cost per prisoner-year, by offence class
# ---------------------------------------------------------------------------
def annual_cost(off: str, corr: float, intangibles: bool, add_cjs: bool = False) -> float:
    u = UNIT[off]
    t = TIME_SERVED[off]
    v = u["victim_total_24"] if intangibles else u["victim_tangible_24"]
    c = corr + v / t
    if add_cjs:
        c += u["cjs_24"] / t
    return c


say()
say("-- Annual social cost per prisoner-year, by offence class (2024$) --")
say(f"{'class':<15}{'time served':>12}{'victim tang/yr':>16}{'victim tot/yr':>15}"
    f"{'+corrections':>14}{'  = total/yr (tang / tot)':>28}")
for o in ["murder", "sexual", "robbery", "assault", "violent_other", "burglary", "mvt",
          "fraud", "larceny", "drug", "public_order", "unspecified"]:
    u, t = UNIT[o], TIME_SERVED[o]
    say(f"{o:<15}{t:>12.1f}{u['victim_tangible_24']/t:>16,.0f}{u['victim_total_24']/t:>15,.0f}"
        f"{CORR['base']:>14,.0f}"
        f"{annual_cost(o, CORR['base'], False):>16,.0f}"
        f"{annual_cost(o, CORR['base'], True):>12,.0f}")


# ---------------------------------------------------------------------------
# ROUTE A1 — BJS stock, Hispanic vs NH white
# ---------------------------------------------------------------------------
def route_a1(corr: float, intangibles: bool, add_cjs: bool = False) -> dict[str, float]:
    res = {}
    for g in ("white", "hispanic"):
        per_res = sum(
            (BJS[g][o] / 1e5) * annual_cost(o, corr, intangibles, add_cjs)
            for o in BJS[g] if not o.startswith("_")
        )
        scale = POP2021[g]["total"] / POP2021[g]["adult2564"]
        res[g] = per_res * scale
    res["diff"] = res["hispanic"] - res["white"]
    res["ratio"] = res["hispanic"] / res["white"]
    return res


say()
say("=" * 100)
say("ROUTE A1 (stock) — BJS 2021 sentenced STATE prisoners, Hispanic (any race) vs NH white")
say("=" * 100)
say(f"ACS 2021 populations: NH white total {POP2021['white']['total']:,.0f}, "
    f"25-64 {POP2021['white']['adult2564']:,.0f} "
    f"(ratio {POP2021['white']['total']/POP2021['white']['adult2564']:.3f})")
say(f"                     Hispanic total {POP2021['hispanic']['total']:,.0f}, "
    f"25-64 {POP2021['hispanic']['adult2564']:,.0f} "
    f"(ratio {POP2021['hispanic']['total']/POP2021['hispanic']['adult2564']:.3f})")
say()
say(f"{'arm':<46}{'NH white':>12}{'Hispanic':>12}{'diff':>12}{'ratio':>9}")
A1_ARMS = [
    ("corrections only (what the ledger already prices)", CORR["base"], None, False),
    ("+ victim tangible, amortised", CORR["base"], False, False),
    ("+ victim tangible + intangible", CORR["base"], True, False),
    ("+ victim total, corrections $45k", CORR["low_45k"], True, False),
    ("+ victim total, corrections $70k", CORR["high_70k"], True, False),
    ("+ victim total + full CJS (double counts prison)", CORR["base"], True, True),
]
a1_rows = []
for label, corr, intang, cjs in A1_ARMS:
    if intang is None:
        r = {}
        for g in ("white", "hispanic"):
            per_res = sum((BJS[g][o] / 1e5) * corr for o in BJS[g] if not o.startswith("_"))
            r[g] = per_res * POP2021[g]["total"] / POP2021[g]["adult2564"]
        r["diff"] = r["hispanic"] - r["white"]
        r["ratio"] = r["hispanic"] / r["white"]
    else:
        r = route_a1(corr, intang, cjs)
    a1_rows.append((label, r))
    say(f"{label:<46}{r['white']:>12,.0f}{r['hispanic']:>12,.0f}{r['diff']:>12,.0f}{r['ratio']:>9.2f}")

A1 = a1_rows[2][1]

say()
say("Offence composition of the Hispanic-minus-white difference (base arm, with intangibles):")
say(f"{'offence':<15}{'white $':>12}{'Hispanic $':>13}{'diff $':>12}{'% of diff':>11}")
comp = {}
for o in BJS["white"]:
    if o.startswith("_"):
        continue
    w = (BJS["white"][o] / 1e5) * annual_cost(o, CORR["base"], True) \
        * POP2021["white"]["total"] / POP2021["white"]["adult2564"]
    h = (BJS["hispanic"][o] / 1e5) * annual_cost(o, CORR["base"], True) \
        * POP2021["hispanic"]["total"] / POP2021["hispanic"]["adult2564"]
    comp[o] = (w, h, h - w)
for o, (w, h, d) in sorted(comp.items(), key=lambda kv: -kv[1][2]):
    say(f"{o:<15}{w:>12,.0f}{h:>13,.0f}{d:>12,.0f}{100*d/A1['diff']:>10.1f}%")


# ---------------------------------------------------------------------------
# ROUTE A2 — ACS institutional level x BJS offence mix,
#            US-born Mexican-origin (self-ID) vs US-born NH white
# ---------------------------------------------------------------------------
def mix(g: str) -> dict[str, float]:
    tot = BJS[g]["_total"]
    return {o: BJS[g][o] / tot for o in BJS[g] if not o.startswith("_")}


MIX = {"white": mix("white"), "hispanic": mix("hispanic")}


def route_a2(corr: float, intangibles: bool, corr_share: float, adj: bool) -> dict[str, float]:
    res = {}
    for grp, proxy, mixkey in (("white", "native_nh_white", "white"),
                               ("mexican", "native_mexican", "hispanic")):
        rate = INST[proxy]["pct_adj"] if (adj and grp == "mexican") else INST[proxy]["pct"]
        rate *= corr_share
        res[grp] = rate * sum(MIX[mixkey][o] * annual_cost(o, corr, intangibles)
                              for o in MIX[mixkey])
    res["diff"] = res["mexican"] - res["white"]
    res["ratio"] = res["mexican"] / res["white"]
    return res


say()
say("=" * 100)
say("ROUTE A2 (stock) — ACS 2023 institutional level x BJS 2021 offence mix")
say("US-born Mexican-origin (ACS self-ID, 2nd AND 3rd+ pooled) vs US-born non-Hispanic white")
say("=" * 100)
say(f"{'arm':<52}{'US-b white':>12}{'US-b Mex':>11}{'diff':>11}{'ratio':>8}")
A2_ARMS = [
    ("corrections only, all institutional GQ counted", CORR["base"], None, 1.00, False),
    ("tangible only", CORR["base"], False, 1.00, False),
    ("BASE: tangible + intangible", CORR["base"], True, 1.00, False),
    ("  + generic-Hispanic prison-coding adjustment", CORR["base"], True, 1.00, True),
    ("  correctional share of institutional GQ = 0.85", CORR["base"], True, 0.85, False),
    ("  corrections $45k/yr", CORR["low_45k"], True, 1.00, False),
    ("  corrections $70k/yr", CORR["high_70k"], True, 1.00, False),
    ("  adj coding + 0.85 correctional share", CORR["base"], True, 0.85, True),
]
a2_rows = []
for label, corr, intang, share, adj in A2_ARMS:
    if intang is None:
        r = {}
        for grp, proxy in (("white", "native_nh_white"), ("mexican", "native_mexican")):
            r[grp] = INST[proxy]["pct"] * share * corr
        r["diff"] = r["mexican"] - r["white"]
        r["ratio"] = r["mexican"] / r["white"]
    else:
        r = route_a2(corr, intang, share, adj)
    a2_rows.append((label, r))
    say(f"{label:<52}{r['white']:>12,.0f}{r['mexican']:>11,.0f}{r['diff']:>11,.0f}{r['ratio']:>8.2f}")

say()
say("Why this differs in SIGN from the institutional-care line in the ledger residual lane:")
say("that line charges the group's WHOLE adult (18+) institutional population, including 65+")
say("nursing-home residents, to its 25-64 adults.  Whites' institutional bill is 55% nursing")
say("home; the Mexican-origin group's is 11%.  A cost-of-CRIME line must drop the 65+ nursing")
say("leg, and at ages 25-64 alone the Mexican-origin institutional rate is 1.73x the white rate")
say("(1.411% vs 0.814%), so the sign reverses.  Both are right for their own question.")

A2 = a2_rows[2][1]
A2_TANG = a2_rows[1][1]
A2_CORR_ONLY = a2_rows[0][1]
A2_SPAN = (min(r["diff"] for _, r in a2_rows[1:]), max(r["diff"] for _, r in a2_rows[1:]))


# ---------------------------------------------------------------------------
# ROUTE B — FBI 2019 arrest flow
# ---------------------------------------------------------------------------
# NH-white arrests are constructed: the race panel and the ethnicity panel cover different
# agency sets, so the race panel is rescaled to the ethnicity panel per offence, then
# Hispanic arrests are subtracted from White arrests.  [INFERENCE]
def route_b(intangibles: bool, reporting_adj: float = 1.0) -> dict[str, object]:
    cost = {"white": 0.0, "hispanic": 0.0}
    detail = {}
    for o, (rt, rw, et, eh) in T43C.items():
        scaled_white = rw * (et / rt)          # race panel rescaled to ethnicity coverage
        nh_white = scaled_white - eh           # [INFERENCE]: most Hispanic arrestees code as white
        # Panel -> national ADULT arrests for this offence.  Table 29 is all ages, so it is
        # first cut to the adult share observed in the race panel (43C / 43A), then the panel
        # counts are scaled by national-adult / panel-adult.
        nat_adult = EST_ARRESTS_2019[o] * (rt / T43A_RACE_TOTAL[o])
        natscale_o = nat_adult / et
        cpa = CRIMES_PER_ARREST[o]
        u = UNIT[o]["victim_total_24"] if intangibles else UNIT[o]["victim_tangible_24"]
        u += UNIT[o]["cjs_24"]        # the flow route has no separate corrections line
        cw = nh_white * natscale_o * cpa * u * reporting_adj
        ch = eh * natscale_o * cpa * u * reporting_adj
        cost["white"] += cw
        cost["hispanic"] += ch
        detail[o] = (nh_white * natscale_o, eh * natscale_o, cw, ch)
    res = {}
    for g in ("white", "hispanic"):
        res[g] = cost[g] / POP2019[g]["adult18"]
    res["diff"] = res["hispanic"] - res["white"]
    res["ratio"] = res["hispanic"] / res["white"]
    res["_detail"] = detail
    return res


say()
say("=" * 100)
say("ROUTE B (flow) — FBI 2019 arrests by ethnicity (Table 43C, adults 18+) x offences per")
say("arrest x unit cost.  Hispanic vs constructed non-Hispanic white.")
say("=" * 100)
say(f"Ethnicity panel: 10,831 agencies, 2019 estimated population 229,735,355 "
    f"({100*229_735_355/328_239_523:.1f}% of the USA).  Agencies reporting ethnicity skew")
say("toward high-Hispanic states, so the Hispanic arrest SHARE is biased up. [FRAMING-SENSITIVE]")
say(f"Adult ethnicity coverage vs race panel: "
    f"{100*T43C_TOTAL[2]/T43C_TOTAL[0]:.1f}% of adult arrests")
say(f"ACS 2019 adults 18+: NH white {POP2019['white']['adult18']:,.0f}, "
    f"Hispanic {POP2019['hispanic']['adult18']:,.0f}")
say()
say("Reported offences per arrest (FBI 2019 Table 1 / Table 29):")
say("  " + "  ".join(f"{o}={CRIMES_PER_ARREST[o]:.2f}" for o in
                     ["murder", "sexual", "robbery", "assault", "burglary", "larceny", "mvt"]))
say("  all other offences: 1.00 (no offences-known series published)")
say()
B_T = route_b(False)
B = route_b(True)
say(f"{'arm':<52}{'NH white':>12}{'Hispanic':>12}{'diff':>12}{'ratio':>9}")
say(f"{'tangible victim + CJS, reported offences only':<52}"
    f"{B_T['white']:>12,.0f}{B_T['hispanic']:>12,.0f}{B_T['diff']:>12,.0f}{B_T['ratio']:>9.2f}")
say(f"{'+ intangible, reported offences only':<52}"
    f"{B['white']:>12,.0f}{B['hispanic']:>12,.0f}{B['diff']:>12,.0f}{B['ratio']:>9.2f}")
B_NCVS = route_b(True, reporting_adj=1 / 0.409)
say(f"{'+ intangible, NCVS reporting uplift 1/0.409':<52}"
    f"{B_NCVS['white']:>12,.0f}{B_NCVS['hispanic']:>12,.0f}"
    f"{B_NCVS['diff']:>12,.0f}{B_NCVS['ratio']:>9.2f}")
say()
say("The ratio is invariant to every multiplier applied equally to both groups")
say("(offences per arrest, reporting uplift, national scale-up), so it is the robust output.")
say()
say("Arrests below are scaled to national adult totals (Table 29 x adult share from 43C/43A).")
say(f"{'offence':<14}{'NHW arrests':>13}{'Hisp arrests':>14}{'NHW $bn':>10}{'Hisp $bn':>11}"
    f"{'Hisp share':>12}")
for o, (nw, eh, cw, ch) in sorted(B["_detail"].items(), key=lambda kv: -kv[1][3]):
    say(f"{o:<14}{nw:>13,.0f}{eh:>14,.0f}{cw/1e9:>10,.1f}{ch/1e9:>11,.1f}"
        f"{100*eh/(eh+nw):>11.1f}%")
oa_share = T43C_OTHER_ASSAULT[3] / T43C_OTHER_ASSAULT[2]
say()
say(f"Excluded from route B for want of a McCollister unit cost: 'other assaults' "
    f"({T43C_OTHER_ASSAULT[2]:,} adult arrests, Hispanic share {100*oa_share:.1f}%),")
say(f"drug ({100*180_093/898_477:.1f}%), DUI ({100*144_250/546_446:.1f}%), "
    f"weapons ({100*18_755/82_953:.1f}%), and all other public-order offences.")
say(f"Overall adult Hispanic arrest share is {100*T43C_TOTAL[3]/T43C_TOTAL[2]:.1f}%, so the")
say("excluded block is close to neutral for the RATIO but lowers both LEVELS.")


# ---------------------------------------------------------------------------
# NCVS reconciliation
# ---------------------------------------------------------------------------
say()
say("=" * 100)
say("RECONCILIATION with victim-reported offending (NCVS)")
say("=" * 100)
NCVS_HISP_WHITE = 0.92 / 0.67    # per-capita offender index, BJS 2012-15, memo §8
# violent-only ratios on each route
def violent_only_ratio_a1() -> float:
    v = ["murder", "sexual", "robbery", "assault", "violent_other"]
    w = sum((BJS["white"][o] / 1e5) * annual_cost(o, CORR["base"], True) for o in v)
    h = sum((BJS["hispanic"][o] / 1e5) * annual_cost(o, CORR["base"], True) for o in v)
    return h / w


def violent_only_ratio_b() -> float:
    v = ["murder", "sexual", "robbery", "assault"]
    w = sum(B["_detail"][o][2] for o in v)
    h = sum(B["_detail"][o][3] for o in v)
    return (h / POP2019["hispanic"]["adult18"]) / (w / POP2019["white"]["adult18"])


say(f"NCVS 2012-15 victim-reported offender index, Hispanic/white per capita   {NCVS_HISP_WHITE:>6.2f}x")
say(f"  (14.4% of violent-victimisation offenders vs 15.6% of the age-12+ population,")
say(f"   against 43.8% and 65.0% for whites; BJS, Race and Hispanic Origin of Victims")
say(f"   and Offenders 2012-15, Tables 2 and 11)")
say(f"Route B, violent offences only, cost-weighted, Hispanic/NH white            "
    f"{violent_only_ratio_b():>6.2f}x")
say(f"Route B, violent arrests unweighted by cost                                 "
    f"{(sum(B['_detail'][o][1] for o in ['murder','sexual','robbery','assault'])/POP2019['hispanic']['adult18'])/(sum(B['_detail'][o][0] for o in ['murder','sexual','robbery','assault'])/POP2019['white']['adult18']):>6.2f}x")
say(f"Route A1, violent classes only, cost-weighted, Hispanic/NH white            "
    f"{violent_only_ratio_a1():>6.2f}x")
say(f"Route A1, imprisonment rate all offences, Hispanic/NH white                 "
    f"{BJS['hispanic']['_total']/BJS['white']['_total']:>6.2f}x")
say(f"Male age-specific imprisonment 25-39, 2022 (memo §8)                        "
    f"2.15-2.84x")
say()
say("The NCVS 1.37x and the arrest 2.8x are NOT the same quantity, and the single largest")
say("reason is simple assault.  NCVS violent victimisation is dominated by simple assault,")
say("which the UCR index excludes.  Adding 'other assaults' (the UCR simple-assault line) to")
say("the route-B violent arrest count, on an unweighted per-adult basis:")
_v4 = ["murder", "sexual", "robbery", "assault"]
_h4 = sum(T43C[o][3] for o in _v4)
_w4 = sum(T43C[o][1] * (T43C[o][2] / T43C[o][0]) - T43C[o][3] for o in _v4)
_oa_t, _oa_rw, _oa_et, _oa_eh = T43C_OTHER_ASSAULT
_oa_w = _oa_rw * (_oa_et / _oa_t) - _oa_eh
_r4 = (_h4 / POP2019["hispanic"]["adult18"]) / (_w4 / POP2019["white"]["adult18"])
_r5 = ((_h4 + _oa_eh) / POP2019["hispanic"]["adult18"]) / \
      ((_w4 + _oa_w) / POP2019["white"]["adult18"])
say(f"  UCR index violent only (murder, rape, robbery, aggravated assault)         {_r4:>6.2f}x")
say(f"  + 'other assaults' (simple assault), the NCVS-comparable basis             {_r5:>6.2f}x")
say()
say("On the NCVS-comparable basis the arrest ratio falls from about 2.8x to about "
    f"{_r5:.1f}x, which")
say("brackets the 1.37x victim-report ratio far more closely.  The residual gap, and the")
say("larger gap to the 2.1-2.9x prison ratio, is the enforcement, charging and sentencing")
say("wedge PLUS the offence-severity mix.  Nothing here separates the two, and the cost")
say("weighting used in this lane deliberately AMPLIFIES severity: the Hispanic arrest share")
say("is highest for the most expensive offences (murder 43%, robbery 49%, rape 42%) and")
say("lowest for larceny (21%) and fraud (22%).  [FRAMING-SENSITIVE]")


# ---------------------------------------------------------------------------
# Offender's own lost legal earnings
# ---------------------------------------------------------------------------
say()
say("=" * 100)
say("OFFENDER'S OWN LOST LEGAL EARNINGS (separate line; NOT in the totals above)")
say("=" * 100)
# mean earnings of all adults 25-64, CPS ASEC 2025 (income year 2024), memo §2
EARN = {"white": 70_424.0, "mexican": 49_789.0}
MINWAGE_FT = 7.25 * 2080
say(f"{'arm':<48}{'US-b white':>12}{'US-b Mex':>11}{'diff':>11}")
for lab, ew, em in [
    ("group mean earnings, all adults 25-64 (upper bound)", EARN["white"], EARN["mexican"]),
    ("federal minimum wage, full time (McCollister basis)", MINWAGE_FT, MINWAGE_FT),
    ("half group mean (negative selection into prison)", EARN["white"] / 2, EARN["mexican"] / 2),
]:
    lw = INST["native_nh_white"]["pct"] * ew
    lm = INST["native_mexican"]["pct"] * em
    say(f"{lab:<48}{lw:>12,.0f}{lm:>11,.0f}{lm-lw:>11,.0f}")
say()
say("Direction on the ledger's tax gap: incarcerated adults live in institutional group")
say("quarters and are therefore OUTSIDE the CPS ASEC civilian noninstitutional universe.")
say("The -$8,286 gap never sees them at all — neither their zero taxes nor their zero")
say("transfers.  Because the Mexican-origin institutional rate (1.41%) is 1.73x the white")
say("rate (0.81%), including prisoners as zero-earning adults would WIDEN the measured tax")
say("gap, by roughly the lines above.  Adding this to the ledger and also counting the")
say("McCollister 'crime career' component would double count; the ledger line is the one to")
say("use.  [INFERENCE]")


# ---------------------------------------------------------------------------
# Lifetime cross-check and the unmeasurable residual
# ---------------------------------------------------------------------------
say()
say("=" * 100)
say("CROSS-CHECK against a lifetime career-criminal valuation")
say("=" * 100)
CP_LOW_2007, CP_HIGH_2007 = 2.6e6, 5.3e6          # Cohen & Piquero 2009, abstract
say("Cohen & Piquero (2009), J Quant Criminol 25:25-49, abstract (publisher page read this")
say("session): 'We estimate the present value of saving a 14-year-old high risk juvenile from")
say("a life of crime to range from $2.6 to $5.3 million.  Similarly, saving a high risk youth")
say("at birth would save society between $2.6 and $4.4 million.'")
say("The often-quoted $4.2-7.2m 'career criminal' figure is NOT in the abstract and was not")
say("verified here. [UNVERIFIED]")
say()
say("Implied scale check.  Route A2's difference is a FLOW per adult-year; over the 40 years")
say("from 25 to 64, undiscounted:")
say(f"  base arm        ${A2['diff']:>7,.0f}/yr x 40 = ${A2['diff']*40:>10,.0f} per adult 25-64")
say(f"  adjusted-coding arm ${a2_rows[3][1]['diff']:>4,.0f}/yr x 40 = "
    f"${a2_rows[3][1]['diff']*40:>10,.0f} per adult 25-64")
say("Against the by-generation memo's synthetic-cohort lifetime fiscal gap of about $250,000")
say("per adult (undiscounted), crime cost is a 23-32% addition on the base arm.  Cohen &")
say("Piquero's $2.6-5.3m is the lifetime cost of ONE high-risk offender, not a population")
say("average, so it is not comparable to these per-adult figures and is quoted only to show")
say("the order of magnitude that a single career offender carries. [INFERENCE]")
say()
say("=" * 100)
say("FRAGMENTATION / SOCIAL COHESION — NO DEFENSIBLE DOLLAR ESTIMATE")
say("=" * 100)
say("Asked for, and refused on the evidence.  There is no per-adult dollar figure for lost")
say("social cohesion that survives the standards this repo applies to the lines above.  What")
say("exists, and why none of it converts:")
say()
say("1. Putnam (2007), 'E Pluribus Unum', Scandinavian Political Studies 30(2):137-174.  The")
say("   canonical finding: in the short run, ethnic diversity is associated with lower trust,")
say("   less altruism and fewer friendships, including within one's own group ('hunkering")
say("   down').  It reports no dollar value and proposes none.  It is also a CROSS-SECTIONAL")
say("   association on US localities, with a long replication dispute about whether the effect")
say("   survives controls for deprivation and residential sorting. [SOURCE: doi 10.1111/")
say("   j.1467-9477.2007.00176.x] [UNVERIFIED: the replication literature was not read here]")
say()
say("2. Algan & Cahuc (2010), 'Inherited Trust and Growth', AER 100(5):2060-2092, and Algan &")
say("   Cahuc (2013, Handbook of Economic Growth ch. 2): about a fifth of the cross-country")
say("   variance in income per head 1980-2009 co-varies with generalised trust, and a one")
say("   standard deviation rise in trust is associated with income per head about 6.8% higher.")
say("   [UNVERIFIED: read from secondary summaries this session, not the papers]")
say()
say("3. Wellbeing-valuation attempts, e.g. 'Valuation of Trust in Government: The Wellbeing")
say("   Valuation Approach', Sustainability 13(19):11000 (2021), doi 10.3390/su131911000, price")
say("   trust by the income equivalent of its life-satisfaction effect. [UNVERIFIED: not read]")
say()
say("Why none of these becomes a line in this ledger, in order of severity:")
say("  (a) None is identified as a CAUSAL effect of any specific group's presence.  Putnam is")
say("      a diversity-index correlation; Algan-Cahuc is a cross-country growth regression")
say("      instrumented by ancestors' inherited trust.  Neither licenses attributing a dollar")
say("      cost to US-born Mexican-origin adults, who are the group in question.")
say("  (b) Any trust->income elasticity applied to a US subgroup would double count the wage")
say("      and tax effects the ledger already measures directly.")
say("  (c) The sign is contested even in principle: the same literature finds diversity raising")
say("      innovation and variety.  A one-sided cost line would be a framing choice, not a")
say("      measurement. [FRAMING-SENSITIVE]")
say("  (d) Any number produced would have an uncertainty band wider than the entire -$8,286")
say("      fiscal gap, so it could not change a decision.")
say("Verdict on this item: [UNVERIFIED]/speculative.  Stated as a qualitative consideration,")
say("never as a dollar figure.")


# ---------------------------------------------------------------------------
# Verdict block
# ---------------------------------------------------------------------------
FISCAL_GAP = -8_286.0
say()
say("=" * 100)
say("HEADLINE — US-born Mexican-origin minus US-born NH white, $ per adult 25-64 per year")
say("=" * 100)
say(f"{'measure':<58}{'value':>12}{'% of -$8,286':>15}")
rows_head = [
    ("Route A2 corrections only (already in the ledger)", A2_CORR_ONLY["diff"]),
    ("Route A2 tangible (corrections + victim tangible)", A2_TANG["diff"]),
    ("Route A2 total (corrections + victim + intangible)", A2["diff"]),
    ("Route A2 span across all arms", None),
    ("Route B tangible (Hispanic vs NH white, all ages 18+)", B_T["diff"]),
    ("Route B total (Hispanic vs NH white, all ages 18+)", B["diff"]),
    ("Lost legal earnings, group-mean arm", INST["native_mexican"]["pct"] * EARN["mexican"]
     - INST["native_nh_white"]["pct"] * EARN["white"]),
]
for lab, v in rows_head:
    if v is None:
        say(f"{lab:<58}{A2_SPAN[0]:>7,.0f}..{A2_SPAN[1]:>4,.0f}{'':>15}")
    else:
        say(f"{lab:<58}{v:>12,.0f}{100*abs(v)/abs(FISCAL_GAP):>14.1f}%")


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------
with OUT_CSV.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["route", "arm", "group_a", "group_b", "cost_a_per_adult2564",
                "cost_b_per_adult2564", "difference", "ratio", "unit"])
    for label, r in a1_rows:
        w.writerow(["A1_bjs_stock", label, "usborn+foreign NH white", "Hispanic any race",
                    round(r["white"], 1), round(r["hispanic"], 1), round(r["diff"], 1),
                    round(r["ratio"], 4), "2024 USD per adult 25-64 per year"])
    for label, r in a2_rows:
        w.writerow(["A2_acs_stock", label, "US-born NH white", "US-born Mexican-origin selfID",
                    round(r["white"], 1), round(r["mexican"], 1), round(r["diff"], 1),
                    round(r["ratio"], 4), "2024 USD per adult 25-64 per year"])
    for label, r in [("tangible victim + CJS", B_T), ("+ intangible", B),
                     ("+ intangible, NCVS uplift", B_NCVS)]:
        w.writerow(["B_fbi_flow", label, "NH white (constructed)", "Hispanic",
                    round(r["white"], 1), round(r["hispanic"], 1), round(r["diff"], 1),
                    round(r["ratio"], 4), "2024 USD per adult 18+ per year"])
    for o in sorted(UNIT):
        u = UNIT[o]
        w.writerow(["unit_cost", o, "", "", round(u["victim_tangible_24"], 0),
                    round(u["victim_total_24"], 0), round(u["total_24"], 0), "",
                    "2024 USD per offence (McCollister 2010, CPI-U inflated)"])

OUT_TXT.write_text("\n".join(_lines) + "\n")
say()
say(f"wrote {OUT_CSV}")
say(f"wrote {OUT_TXT}")
OUT_TXT.write_text("\n".join(_lines) + "\n")

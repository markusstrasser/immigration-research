"""Long-run responses for the account's economic-affairs and recreation lines, by NIPA subfunction.

Step 1 of this lane (BRIEF.md). The complete account's `economic_affairs_services` and
`recreation_culture` lines are consolidated government consumption expenditures, NIPA Table 3.17
lines 5 and 8 for 2024 (full_account_spending_2026_09_20/builder.py). Table 3.17 splits consumption
by level of government but not by subfunction. Table 3.16 splits current expenditures by
subfunction; current expenditures are consumption plus social benefits, grants-in-aid (federal
only), subsidies and other current transfers, and Table 3.17 gives those transfers by function and,
for grants and subsidies, by subfunction. Consumption by subfunction is therefore Table 3.16 less
the transfers, with two assignments the tables do not pin down (see ASSIGNMENTS below).

Each subfunction then gets a long-run response at the band's low and high ends (RULES below): the
state-by-year scaling estimates (scaling_test_2026_09_20/derived/state/estimates.csv) read over the
removal as the finite-removal decision reads them, r = [1 - (1 - s)^b] / s, capped at 1 as the
account caps every service line; general government's adopted responses for administration; and 0
where spending is not driven by residents.

Writes derived/subfunctions.csv, derived/response_table.csv, derived/responses.json and
derived/gates_build.json, only when every gate passes (otherwise stops with [BLOCKED] and writes
nothing). Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/build.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
PINS = FISCAL / "full_account_spending_2026_09_20" / "SOURCE_PINS.json"
MODEL = FISCAL / "assumption_explorer_2026_09_21" / "derived" / "model.json"
ESTIMATES = FISCAL / "scaling_test_2026_09_20" / "derived" / "state" / "estimates.csv"
R_VALUES = FISCAL / "finite_response_2026_09_26" / "derived" / "r_values.json"
CORRECTIONS = FISCAL / "main_case_schools_full_2026_09_26" / "derived" / "corrections.json"
SHEETS = ("T31200-A", "T31505-A", "T31600-A", "T31700-A")
ROUNDING_TOLERANCE_M = 2  # published components are rounded to $1m independently

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(label: str) -> str:
    return re.sub(r"\\\d+\\", "", str(label)).strip()


def read_tables(path: Path) -> dict:
    """{sheet: {line: (label, series, 2024 value in $m or None)}} for the four NIPA tables used."""
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables = {}
    for sheet in SHEETS:
        rows = list(book[sheet].values)
        header = [r for r in rows if r[0] == "Line"]
        if len(header) != 1 or rows[1][0] != "[Millions of dollars]":
            raise SystemExit(f"[BLOCKED] {sheet}: units or header changed")
        cols = [i for i, x in enumerate(header[0]) if str(x) == "2024"]
        if len(cols) != 1:
            raise SystemExit(f"[BLOCKED] {sheet}: no single 2024 column")
        j = cols[0]
        tables[sheet] = {int(r[0]): (clean(r[1]), r[2], r[j] if isinstance(r[j], (int, float)) else None)
                         for r in rows if str(r[0]).isdigit()}
    book.close()
    return tables


class Nipa:
    """Cell access that checks each line's label, so a renumbered table fails loudly."""

    def __init__(self, tables):
        self.t = tables
        self.used = {}

    def __call__(self, sheet: str, line: int, label: str) -> int:
        got, series, value = self.t[sheet][line]
        if got.lower() != label.lower() or value is None:
            raise SystemExit(f"[BLOCKED] {sheet} line {line}: expected '{label}', found '{got}' = {value}")
        self.used[f"{sheet}:{line}"] = {"label": got, "series": series, "million": value}
        return int(value)


def r_finite(b: float, s: float) -> float:
    return (1 - (1 - s) ** b) / s


def main() -> None:
    print("[sources]")
    pin = next(p for p in json.loads(PINS.read_text())["sources"] if p["name"] == "Section3All_xls.xlsx")
    bea = Path(pin["path"])
    gate("BEA Section 3 workbook is the account's pinned vintage", sha256(bea) == pin["sha256"], pin["sha256"][:12])
    n = Nipa(read_tables(bea))
    model = json.loads(MODEL.read_text())
    lines = {l["id"]: l for l in model["spending"]["lines"]}
    T16, T17, T155, T12 = "T31600-A", "T31700-A", "T31505-A", "T31200-A"

    # ------------------------------------------------------------------------------------------
    print("\n[the account's two lines]")
    ea_gov, rc_gov = n(T17, 5, "Economic affairs"), n(T17, 8, "Recreation and culture")
    ea_fed, rc_fed = n(T17, 15, "Economic affairs"), n(T17, 18, "Recreation and culture")
    ea_sl, rc_sl = n(T17, 24, "Economic affairs"), n(T17, 29, "Recreation and culture")
    gate("account line economic_affairs_services is Table 3.17 line 5",
         round(lines["economic_affairs_services"]["national_bn"] * 1000) == ea_gov, f"{ea_gov}")
    gate("account line recreation_culture is Table 3.17 line 8",
         round(lines["recreation_culture"]["national_bn"] * 1000) == rc_gov, f"{rc_gov}")
    gate("federal + state-local consumption = government, both lines",
         ea_fed + ea_sl == ea_gov and rc_fed + rc_sl == rc_gov, f"{ea_fed}+{ea_sl}, {rc_fed}+{rc_sl}")

    # ------------------------------------------------------------------------------------------
    print("\n[state and local economic affairs]")
    sl_cur = {"Highways": n(T16, 93, "Highways"), "Transit and railroad": n(T16, 94, "Transit and railroad"),
              "General economic and labor affairs": n(T16, 96, "General economic and labor affairs"),
              "Agriculture": n(T16, 97, "Agriculture"), "Energy": n(T16, 98, "Energy"),
              "Natural resources": n(T16, 99, "Natural resources"), "Other (commercial activities)": n(T16, 100, "Other")}
    sl_total_cur = n(T16, 91, "Economic affairs")
    sl_benefits = n(T17, 53, "Economic affairs")
    sl_subsidies = n(T17, 101, "Economic affairs")
    sl_sub_transport, sl_sub_energy = n(T17, 102, "Transportation"), n(T17, 103, "Energy")
    employment_training = n(T12, 41, "Employment and training")
    gate("3.16 S&L economic affairs = consumption + social benefits + subsidies (exact)",
         sl_total_cur == ea_sl + sl_benefits + sl_subsidies, f"{sl_total_cur} = {ea_sl} + {sl_benefits} + {sl_subsidies}")
    gate("S&L economic-affairs benefits are Table 3.12's employment and training (exact)",
         sl_benefits == employment_training, f"{sl_benefits}")
    gate("S&L economic-affairs subsidies are all transportation", sl_sub_transport == sl_subsidies and sl_sub_energy == 0,
         f"{sl_sub_transport} of {sl_subsidies}")
    gate("3.16 S&L transit and railroad equals the S&L transportation subsidy (no S&L transit consumption)",
         sl_cur["Transit and railroad"] == sl_sub_transport, f"{sl_cur['Transit and railroad']}")
    sl = {k: v for k, v in sl_cur.items()}
    sl["Transit and railroad"] -= sl_sub_transport
    sl["General economic and labor affairs"] -= sl_benefits
    sl_round = ea_sl - sum(sl.values())
    gate("S&L subfunctions miss the published level total by rounding only", abs(sl_round) <= ROUNDING_TOLERANCE_M,
         f"{sl_round:+d} ($m), put on highways")
    sl["Highways"] += sl_round

    # ------------------------------------------------------------------------------------------
    print("\n[federal economic affairs]")
    fed_cur = {"Highways": n(T16, 56, "Highways"), "Air": n(T16, 57, "Air"), "Water": n(T16, 58, "Water"),
               "Transit and railroad": n(T16, 59, "Transit and railroad"), "Space": n(T16, 60, "Space"),
               "General economic and labor affairs": n(T16, 62, "General economic and labor affairs"),
               "Agriculture": n(T16, 63, "Agriculture"), "Energy": n(T16, 64, "Energy"),
               "Natural resources": n(T16, 65, "Natural resources"), "Postal service": n(T16, 66, "Postal service")}
    fed_total_cur = n(T16, 54, "Economic affairs")
    gate("3.16 federal subfunctions add to federal economic affairs", sum(fed_cur.values()) == fed_total_cur,
         f"{sum(fed_cur.values())}")
    gov_cur = {"Highways": n(T16, 15, "Highways"), "Air": n(T16, 16, "Air"), "Water": n(T16, 17, "Water"),
               "Transit and railroad": n(T16, 18, "Transit and railroad"), "Space": n(T16, 19, "Space"),
               "General economic and labor affairs": n(T16, 21, "General economic and labor affairs"),
               "Agriculture": n(T16, 22, "Agriculture"), "Energy": n(T16, 23, "Energy"),
               "Natural resources": n(T16, 24, "Natural resources")}
    # Grants-in-aid by subfunction (Table 3.17 gives transportation only as a whole).
    grants = {"Space": n(T17, 63, "Space"), "General economic and labor affairs": n(T17, 65, "General economic and labor affairs"),
              "Agriculture": n(T17, 66, "Agriculture"), "Energy": n(T17, 67, "Energy"),
              "Natural resources": n(T17, 68, "Natural resources")}
    grants_transport, grants_total = n(T17, 62, "Transportation"), n(T17, 61, "Economic affairs")
    # Consolidation: government = federal + S&L - federal grants, so a subfunction's grant is the
    # difference. It reproduces Table 3.17's published grants where they are given.
    # 3.16 has no S&L air, water or space lines: their S&L current expenditure is zero.
    implied = {k: fed_cur[k] + sl_cur.get(k, 0) - gov_cur[k] for k in gov_cur}
    gate("consolidation reproduces Table 3.17's grants where published",
         all(abs(implied[k] - grants[k]) <= ROUNDING_TOLERANCE_M for k in grants),
         ", ".join(f"{k.split()[0]} {implied[k]}/{grants[k]}" for k in grants))
    for mode in ("Highways", "Air", "Water", "Transit and railroad"):
        grants[mode] = implied[mode]
    gate("consolidation splits the transportation grant by mode",
         abs(sum(grants[m] for m in ("Highways", "Air", "Water", "Transit and railroad")) - grants_transport) <= ROUNDING_TOLERANCE_M
         and all(grants[m] >= 0 for m in ("Highways", "Air", "Water", "Transit and railroad")),
         f"highways {grants['Highways']}, air {grants['Air']}, water {grants['Water']}, transit {grants['Transit and railroad']} vs {grants_transport}")
    gate("grants by subfunction add to the published total", sum(grants.values()) == grants_total, f"{sum(grants.values())}")
    subsidies = {"General economic and labor affairs": n(T17, 94, "General economic and labor affairs"),
                 "Agriculture": n(T17, 95, "Agriculture"), "Energy": n(T17, 96, "Energy"),
                 "Natural resources": n(T17, 97, "Natural resources")}
    sub_transport, sub_total = n(T17, 92, "Transportation"), n(T17, 91, "Economic affairs")
    # ASSIGNMENT 1: Table 3.17 does not split the federal transportation subsidy by mode. Federal
    # transit-and-railroad consumption plus investment is only $572m (3.15.5), so at least
    # (current expenditure - grant - 572) of the subsidy must be transit and railroad; the rest,
    # at most a few hundred $m, could be air or water. All of it is put on transit and railroad.
    subsidies["Transit and railroad"] = sub_transport
    gate("federal subsidies by subfunction add to the published total", sum(subsidies.values()) == sub_total, f"{sub_total}")
    fed_benefits = n(T17, 44, "Economic affairs")
    fed = {k: v - grants.get(k, 0) - subsidies.get(k, 0) for k, v in fed_cur.items()}
    # ASSIGNMENT 2: federal economic-affairs social benefits ($7.5bn) and the remaining current
    # transfers are not split by subfunction. The residual is put on general economic and labor
    # affairs, where the non-negativity of investment requires most of it (gate below).
    unallocated = sum(fed.values()) - ea_fed
    other_transfers = fed_total_cur - ea_fed - fed_benefits - grants_total - sub_total
    gate("the unallocated federal residual is the economic-affairs benefits plus other current transfers",
         abs(unallocated - (fed_benefits + other_transfers)) <= ROUNDING_TOLERANCE_M,
         f"{unallocated} = {fed_benefits} benefits + {other_transfers} other")
    gov_ea_cur, gov_benefits, gov_subsidies = n(T16, 13, "Economic affairs"), n(T17, 35, "Economic affairs"), n(T17, 80, "Economic affairs")
    gate("the other transfers are federal only (consolidated residual equals the federal one)",
         abs((gov_ea_cur - ea_gov - gov_benefits - gov_subsidies) - other_transfers) <= ROUNDING_TOLERANCE_M,
         f"consolidated {gov_ea_cur - ea_gov - gov_benefits - gov_subsidies}, federal {other_transfers}")
    fed["General economic and labor affairs"] -= unallocated
    gate("federal subfunctions add to the published level total exactly", sum(fed.values()) == ea_fed, f"{sum(fed.values())}")

    # ------------------------------------------------------------------------------------------
    print("\n[consumption plus investment bounds, Table 3.15.5]")
    cegi_fed = {"Highways": n(T155, 54, "Highways"), "Air": n(T155, 55, "Air"), "Water": n(T155, 56, "Water"),
                "Transit and railroad": n(T155, 57, "Transit and railroad"), "Space": n(T155, 58, "Space"),
                "General economic and labor affairs": n(T155, 60, "General economic and labor affairs"),
                "Agriculture": n(T155, 61, "Agriculture"), "Energy": n(T155, 62, "Energy"),
                "Natural resources": n(T155, 63, "Natural resources"), "Postal service": n(T155, 64, "Postal service")}
    cegi_sl = {"Highways": n(T155, 90, "Highways"), "Transit and railroad": n(T155, 93, "Transit and railroad"),
               "General economic and labor affairs": n(T155, 95, "General economic and labor affairs"),
               "Agriculture": n(T155, 96, "Agriculture"), "Energy": n(T155, 97, "Energy"),
               "Natural resources": n(T155, 98, "Natural resources"), "Other (commercial activities)": n(T155, 99, "Other")}
    gi = {("federal", "Economic affairs"): n(T17, 119, "Economic affairs"), ("state_local", "Economic affairs"): n(T17, 128, "Economic affairs"),
          ("federal", "Recreation and culture"): n(T17, 122, "Recreation and culture"),
          ("state_local", "Recreation and culture"): n(T17, 131, "Recreation and culture")}
    cegi_level = {("federal", "Economic affairs"): n(T155, 52, "Economic affairs"), ("state_local", "Economic affairs"): n(T155, 88, "Economic affairs"),
                  ("federal", "Recreation and culture"): n(T155, 67, "Recreation and culture"),
                  ("state_local", "Recreation and culture"): n(T155, 108, "Recreation and culture")}
    cons_level = {("federal", "Economic affairs"): ea_fed, ("state_local", "Economic affairs"): ea_sl,
                  ("federal", "Recreation and culture"): rc_fed, ("state_local", "Recreation and culture"): rc_sl}
    gate("3.15.5 = consumption + gross investment at each level (rounding)",
         all(abs(cegi_level[k] - cons_level[k] - gi[k]) <= ROUNDING_TOLERANCE_M for k in gi),
         ", ".join(f"{k[0]} {k[1].split()[0]} {cegi_level[k] - cons_level[k] - gi[k]:+d}" for k in gi))
    gel_min = fed_cur["General economic and labor affairs"] - grants["General economic and labor affairs"] \
        - subsidies["General economic and labor affairs"] - cegi_fed["General economic and labor affairs"]
    gate("assignment 2 respects investment >= 0 (general economic and labor affairs must hold at least gel_min)",
         unallocated >= gel_min > 0, f"residual {unallocated} >= minimum {gel_min} ($m)")
    transit_min = fed_cur["Transit and railroad"] - grants["Transit and railroad"] - cegi_fed["Transit and railroad"]
    gate("assignment 1 respects investment >= 0 (transit and railroad must take at least transit_min of the subsidy)",
         sub_transport >= transit_min > 0, f"subsidy {sub_transport} >= minimum {transit_min} ($m)")
    implied_gi = {("federal", k): cegi_fed[k] - fed[k] for k in fed}
    implied_gi.update({("state_local", k): cegi_sl[k] - sl[k] for k in sl})
    gate("implied gross investment is not negative in any subfunction (rounding)",
         all(v >= -ROUNDING_TOLERANCE_M for v in implied_gi.values()),
         f"min {min(implied_gi.values())} ($m)")

    # ------------------------------------------------------------------------------------------
    print("\n[recreation and culture]")
    rc_fed_cur = n(T16, 69, "Recreation and culture")
    rc_sl_cur = n(T16, 105, "Recreation and culture")
    gate("S&L recreation current expenditure is all consumption", rc_sl_cur == rc_sl, f"{rc_sl_cur}")
    rows = []

    def add(line, level, subfunction, consumption, current, benefits=0, grant=0, subsidy=0, unalloc=0, rounding=0,
            cegi=None, cells="", note=""):
        rows.append({"id": f"{'fed' if level == 'federal' else 'sl'}_{re.sub(r'[^a-z]+', '_', subfunction.lower()).strip('_')}",
                     "account_line": line, "level": level, "subfunction": subfunction,
                     "current_expenditure_m": current, "benefits_m": benefits, "grants_m": grant, "subsidies_m": subsidy,
                     "unallocated_transfers_m": unalloc, "rounding_m": rounding, "consumption_m": consumption,
                     "cegi_m": cegi, "implied_gross_investment_m": None if cegi is None else cegi - consumption,
                     "source_cells": cells, "note": note})

    ea = "economic_affairs_services"
    for k in ("Highways", "Air", "Water", "Transit and railroad", "Space", "General economic and labor affairs",
              "Agriculture", "Energy", "Natural resources", "Postal service"):
        note = {"Transit and railroad": "assignment 1: all of the federal transportation subsidy",
                "General economic and labor affairs": "assignment 2: the unallocated benefits and other current transfers",
                "Water": "grant from consolidation (3.16 federal + S&L - government)",
                }.get(k, "")
        add(ea, "federal", k, fed[k], fed_cur[k], grant=grants.get(k, 0), subsidy=subsidies.get(k, 0),
            unalloc=unallocated if k == "General economic and labor affairs" else 0, cegi=cegi_fed[k],
            cells=f"3.16 federal {k}; 3.17 grants/subsidies; 3.15.5 federal {k}", note=note)
    for k in ("Highways", "Transit and railroad", "General economic and labor affairs", "Agriculture", "Energy",
              "Natural resources", "Other (commercial activities)"):
        note = {"Highways": f"absorbs the published rounding ({sl_round:+d})",
                "Transit and railroad": "S&L transit is a government enterprise: its current expenditure is the subsidy",
                "General economic and labor affairs": "less 3.17 S&L benefits = 3.12 employment and training",
                "Other (commercial activities)": "liquor stores, lotteries and other commercial activities (3.16 note 4)"}.get(k, "")
        add(ea, "state_local", k, sl[k], sl_cur[k], benefits=sl_benefits if k == "General economic and labor affairs" else 0,
            subsidy=sl_sub_transport if k == "Transit and railroad" else 0, rounding=sl_round if k == "Highways" else 0,
            cegi=cegi_sl[k], cells=f"3.16 S&L {k}; 3.17 S&L benefits/subsidies; 3.15.5 S&L {k}", note=note)
    rc = "recreation_culture"
    add(rc, "federal", "Recreation and culture", rc_fed, rc_fed_cur, benefits=n(T17, 47, "Recreation and culture"),
        grant=n(T17, 71, "Recreation and culture"), unalloc=rc_fed_cur - rc_fed - n(T17, 47, "Recreation and culture") - n(T17, 71, "Recreation and culture"),
        cegi=cegi_level[("federal", "Recreation and culture")], cells="3.17 line 18; 3.16 line 69; 3.15.5 line 67",
        note="NIPA has no recreation subfunctions; consumption is 3.17 line 18")
    add(rc, "state_local", "Recreation and culture", rc_sl, rc_sl_cur, cegi=cegi_level[("state_local", "Recreation and culture")],
        cells="3.17 line 29; 3.16 line 105; 3.15.5 line 108", note="NIPA has no recreation subfunctions")
    for line, total in ((ea, ea_gov), (rc, rc_gov)):
        got = sum(r["consumption_m"] for r in rows if r["account_line"] == line)
        gate(f"subfunctions add to {line} exactly", got == total, f"{got} = {total} ($m)")

    # ------------------------------------------------------------------------------------------
    print("\n[responses]")
    rv = json.loads(R_VALUES.read_text())
    s = rv["s_national_memo"]
    gate("s is the brief's 0.120245 (40.896574m / 340.110988m)", abs(s - 40.896574 / 340.110988) < 1e-15, f"{s:.9f}")
    gg = json.loads(CORRECTIONS.read_text())["meta"]["responses"]["general_government"]
    b_admin = gg["elasticity"][1]
    gate("positive control: r(b) reproduces the main case's general-government high response",
         abs(r_finite(b_admin, s) - gg["high"]) < 1e-15, f"r({b_admin}) = {r_finite(b_admin, s):.10f}")
    est = {(r["function"], r["model"]): r for r in csv.DictReader(ESTIMATES.open()) if r["sample"] == "all"}

    def elasticity(function, model):
        r = est[(function, model)]
        return {"b": float(r["beta"]), "se": float(r["se_cluster_state_CR1"]), "ci": [float(r["ci_low"]), float(r["ci_high"])],
                "source": f"scaling_test_2026_09_20/derived/state/estimates.csv {function} {model} all"}
    gate("scaling estimates are the memo's table (0.727/1.464 highways, 0.948/1.412 parks, 0.824/0.471 administration)",
         all(abs(elasticity(f, m)["b"] - v) < 5e-4 for f, m, v in (("highways_nontoll", "year_fe", 0.727), ("highways_nontoll", "state_year_fe", 1.464),
                                                                     ("parks", "year_fe", 0.948), ("parks", "state_year_fe", 1.412),
                                                                     ("admin", "year_fe", 0.824), ("admin", "state_year_fe", 0.471))))
    hwy_across, hwy_within = elasticity("highways_nontoll", "year_fe"), elasticity("highways_nontoll", "state_year_fe")
    park_across, park_within = elasticity("parks", "year_fe"), elasticity("parks", "state_year_fe")

    def measured(e_low, e_high, label):
        lo, hi = r_finite(e_low["b"], s), r_finite(e_high["b"], s)
        return {"low": {"response": min(lo, 1.0), "b": e_low["b"], "source": e_low["source"], "uncapped": lo},
                "high": {"response": min(hi, 1.0), "b": e_high["b"], "source": e_high["source"], "uncapped": hi},
                "rule": label}
    highways = measured(hwy_across, hwy_within, "scaling test, nontoll highways: across states at the low end, within states at the high end, "
                                               "finite removal, capped at 1")
    parks = measured(park_across, park_within, "scaling test, parks: across states at the low end, within states at the high end, "
                                             "finite removal, capped at 1")
    admin_sl = {"low": {"response": gg["high"], "b": b_admin, "source": "main case general government, S&L part (scaling_check 0.842)", "uncapped": gg["high"]},
                "high": {"response": gg["high"], "b": b_admin, "source": "main case general government, S&L part (scaling_check 0.842)", "uncapped": gg["high"]},
                "rule": "general government's adopted response for state-local administration at both ends"}
    zero = {"low": {"response": 0.0, "b": None, "source": "held fixed", "uncapped": 0.0},
            "high": {"response": 0.0, "b": None, "source": "held fixed", "uncapped": 0.0}}

    def federal(of, label):
        return {"low": {"response": 0.0, "b": None, "source": "federal appropriation held fixed at the low end", "uncapped": 0.0},
                "high": dict(of["high"]), "rule": label}
    admin_fed = federal(admin_sl, "general government's adopted treatment of federal administration: fixed at the low end, "
                                  "the administration response at the high end")
    RULES = {
        "fed_highways": (federal(highways, "federal highway administration: fixed at the low end, the highway response at the high end"),
                         "FHWA operations and federal lands roads; network scale follows traffic"),
        "fed_air": (federal(highways, "air traffic control and screening: fixed at the low end, the nearest measured transport function (highways) at the high end"),
                    "FAA operations and TSA screening scale with flights and passengers; no air row is measured"),
        "fed_water": (dict(zero, rule="held at 0"), "Corps of Engineers navigation, Coast Guard and maritime programs follow waterways and freight, not residents"),
        "fed_transit_and_railroad": (federal(highways, "federal transit and rail administration: fixed at the low end, the highway response at the high end"),
                                     "$94m after Amtrak's subsidy; nearest measured transport function"),
        "fed_space": (dict(zero, rule="held at 0"), "NASA's budget is not driven by residents"),
        "fed_general_economic_and_labor_affairs": (admin_fed, "commerce, labor, statistical and regulatory agencies: administration"),
        "fed_agriculture": (dict(zero, rule="held at 0"), "farm programs, research and inspection follow agriculture, not residents"),
        "fed_energy": (dict(zero, rule="held at 0"), "energy programs are not driven by residents"),
        "fed_natural_resources": (dict(zero, rule="held at 0"), "land, water and conservation programs follow the resource base (brief's example)"),
        "fed_postal_service": (dict(zero, rule="held at 0"), "postal service is an enterprise; the line is a small negative net"),
        "sl_highways": (highways, "S&L highways: consumption is operations, maintenance and depreciation of the road network"),
        "sl_transit_and_railroad": (highways, "no S&L transit consumption (enterprise); rule set for completeness"),
        "sl_general_economic_and_labor_affairs": (admin_sl, "labor departments, economic development, licensing and regulation: administration"),
        "sl_agriculture": (dict(zero, rule="held at 0"), "agriculture departments and extension follow agriculture, not residents"),
        "sl_energy": (dict(zero, rule="held at 0"), "no S&L energy consumption (public power is an enterprise)"),
        "sl_natural_resources": (dict(zero, rule="held at 0"), "fish and game, forestry, water resources and conservation follow the resource base (brief's example)"),
        "sl_other_commercial_activities": (dict(zero, rule="held at 0"), "commercial activities net of their sales (3.16 note 4)"),
        "fed_recreation_and_culture": (federal(parks, "national parks and federal cultural institutions: fixed at the low end, the parks response at the high end"),
                                       "national parks, Smithsonian and federal cultural agencies"),
        "sl_recreation_and_culture": (parks, "Census parks and recreation (E61) covers parks, recreation, museums, zoos and convention centres"),
    }
    gate("every subfunction has a rule", sorted(RULES) == sorted(r["id"] for r in rows),
         f"{len(RULES)} rules, {len(rows)} rows")

    # ------------------------------------------------------------------------------------------
    key = {l: lines[l]["keys"][lines[l]["preferred_key"]]["personal"] for l in (ea, rc)}
    gate("the preferred key's share is the same for both allocations (uncorrected model)",
         all(lines[l]["keys"][lines[l]["preferred_key"]]["personal"]["share"] == lines[l]["keys"][lines[l]["preferred_key"]]["shared"]["share"]
             for l in (ea, rc)))
    table, resp_rows = [], []
    for r in rows:
        rule, reason = RULES[r["id"]]
        total = ea_gov if r["account_line"] == ea else rc_gov
        share = key[r["account_line"]]["share"]
        r["share_of_line"] = r["consumption_m"] / total
        r["group_amount_uncorrected_key_bn"] = r["consumption_m"] / 1000 * share
        r["response_low"], r["response_high"] = rule["low"]["response"], rule["high"]["response"]
        table.append(r)
        resp_rows.append({"id": r["id"], "account_line": r["account_line"], "level": r["level"], "subfunction": r["subfunction"],
                          "national_bn": r["consumption_m"] / 1000, "group_amount_uncorrected_key_bn": r["group_amount_uncorrected_key_bn"],
                          "rule": rule["rule"], "reason": reason,
                          "low_b": rule["low"]["b"], "low_response": rule["low"]["response"], "low_source": rule["low"]["source"],
                          "high_b": rule["high"]["b"], "high_response": rule["high"]["response"], "high_source": rule["high"]["source"],
                          "high_uncapped": rule["high"]["uncapped"],
                          "at_stake_bn_if_1": r["group_amount_uncorrected_key_bn"]})
    blend = {}
    for line, total in ((ea, ea_gov), (rc, rc_gov)):
        sub = [x for x in resp_rows if x["account_line"] == line]
        blend[line] = {e: sum(x["national_bn"] * x[f"{e}_response"] for x in sub) / (total / 1000) for e in ("low", "high")}
    gate("blended responses lie in [0, 1]", all(0 <= v <= 1 for b in blend.values() for v in b.values()),
         json.dumps({k: {e: round(v, 6) for e, v in b.items()} for k, b in blend.items()}))

    # ------------------------------------------------------------------------------------------
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    DERIVED.mkdir(exist_ok=True)

    def write_csv(name, records, fields):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for rec in records:
            w.writerow({k: (f"{rec[k]:.10g}" if isinstance(rec[k], float) else ("" if rec[k] is None else rec[k])) for k in fields})
        (DERIVED / name).write_text(buf.getvalue())
    write_csv("subfunctions.csv", table, ["id", "account_line", "level", "subfunction", "current_expenditure_m", "benefits_m", "grants_m",
                                          "subsidies_m", "unallocated_transfers_m", "rounding_m", "consumption_m", "share_of_line",
                                          "group_amount_uncorrected_key_bn", "cegi_m", "implied_gross_investment_m", "source_cells", "note"])
    write_csv("response_table.csv", resp_rows, ["id", "account_line", "level", "subfunction", "national_bn", "group_amount_uncorrected_key_bn",
                                                "low_b", "low_response", "high_b", "high_response", "high_uncapped", "rule", "reason",
                                                "low_source", "high_source"])
    responses = {
        "meta": {
            "lane": "service_response_long_run_2026_09_27",
            "s": s,
            "rule": "finite removal r = [1 - (1 - s)^b] / s on the scaling test's state estimates, capped at 1; "
                    "administration takes the main case's general-government responses; 0 where spending is not driven by residents",
            "band_ends": ["low", "high"],
            "note": ("A response applies to the account's keyed amount of the line (the engine's per-line response_override). "
                     "Subfunctions share their line's key, so the engine applies the amount-weighted blend (lines.*.response). "
                     "Low responses apply at the candidate band's low end, high responses at its high end; engine.cjs records the "
                     "end specifications in derived/candidate_band.json."),
            "main_case_response": 0,
        },
        "lines": {line: {"national_bn": (ea_gov if line == ea else rc_gov) / 1000, "key": lines[line]["preferred_key"],
                         "key_share_uncorrected": key[line]["share"], "main_case_response": 0,
                         "response": blend[line],
                         "subfunctions": [{"id": x["id"], "level": x["level"], "subfunction": x["subfunction"],
                                           "national_bn": x["national_bn"],
                                           "share_of_line": x["national_bn"] / ((ea_gov if line == ea else rc_gov) / 1000),
                                           "response": {"low": x["low_response"], "high": x["high_response"]},
                                           "basis": x["rule"]} for x in resp_rows if x["account_line"] == line]}
                  for line in (ea, rc)},
        "elasticities": {"highways_nontoll": {"across_states": hwy_across, "within_states": hwy_within},
                         "parks": {"across_states": park_across, "within_states": park_within},
                         "administration_general_government": {"b": b_admin, "source": "main_case_schools_full_2026_09_26 corrections.json meta.responses"}},
    }
    (DERIVED / "responses.json").write_text(json.dumps(responses, indent=1) + "\n")
    (DERIVED / "gates_build.json").write_text(json.dumps({"gates": GATES, "bea_cells": dict(sorted(n.used.items())),
                                                          "unallocated_federal_m": unallocated, "gel_minimum_m": gel_min,
                                                          "transit_subsidy_minimum_m": transit_min}, indent=1) + "\n")
    print("\n[subfunctions, $m, and responses low/high]")
    for x, r in zip(resp_rows, table):
        print(f"  {x['id']:42s} {r['consumption_m']:>9,d}  key {x['group_amount_uncorrected_key_bn']:7.3f}bn  "
              f"{x['low_response']:.4f} / {x['high_response']:.4f}" + (f"  (uncapped {x['high_uncapped']:.4f})" if x['high_uncapped'] > 1 else ""))
    print("  blended:", json.dumps({k: {e: round(v, 6) for e, v in b.items()} for k, b in blend.items()}))
    print(f"all {len(GATES)} gates passed")


if __name__ == "__main__":
    main()

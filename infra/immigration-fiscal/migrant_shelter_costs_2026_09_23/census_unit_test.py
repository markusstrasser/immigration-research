#!/usr/bin/env python3
"""Do migrant shelter outlays show up in the Census individual-unit finance files?

Reads the Annual Survey of State and Local Government Finances individual-unit files for
survey years 2021-2024 (already downloaded by two other lanes), pulls function-level direct
expenditure and intergovernmental revenue for the governments that ran the largest migrant
responses and for peer governments, and compares 2023 and 2024 with 2022.

2022 is the baseline because the 2021 file uses a finer code set than the 2022-2024 files
(all re-released 15 July 2026): 2021 carries E74/E75 vendor payments, J67/J68 cash assistance,
G capital codes, and C/L codes by function, which the later files fold into E79, F, C89 and
other codes. Function totals (all welfare codes together, total state aid) stay comparable
with 2021; sub-splits do not. 2022 is also a Census of Governments year (every unit
enumerated); 2021, 2023 and 2024 are sample years in which state governments and the large
cities and counties used here are certainty units.

Record layout (2017 and later, identical in all four files; 2024 technical documentation
pp. 1-2): ID 1-12 (FIPS state, type, FIPS county, unit), item 13-15, amount 16-27 in
thousands of dollars, year 28-31, imputation/item flag 32.

Item codes (Census Government Finance and Employment Classification Manual, ch. 5):
first character E current operations, F construction, G other capital outlay, K equipment,
J assistance and subsidies, I interest; L/M/Q/S intergovernmental expenditure;
B federal and C state intergovernmental revenue. Functions: 67/68/74/75/77/79 public
welfare, 50 housing and community development, 32 health, 36 hospitals, 89 other and
unallocable. "Temporary shelters and other services for the homeless" are coded to public
welfare *79 (manual p. 188 of the PDF); housing *50 excludes them (p. 166).

Survey year Y covers fiscal years ending 1 July Y-1 to 30 June Y, so a December fiscal
year enters survey Y as calendar Y-1, and a September fiscal year as the fiscal year ending
September Y-1.

Also aggregates the City of Chicago "Vendor Payments - New Arrivals" export (data portal
gxzc-43gg) by invoice year and funding source, and computes how the complete account's
national keys charge calendar-2024 migrant outlays (cy2024_outlays.csv) to the Mexican-origin
union against the union's share of the people served.

E23 (financial administration, current operations) jumps in the 2022 file for many governments
with no offsetting fall elsewhere (NYC $0.6bn in 2021, $10.1bn in 2022). No candidate function or
part weight uses it; the total is also given without it (total_direct_general_ex_e23), and
census_e23_by_unit.csv prints it for every unit, with Cook County added as a context unit.

Outputs (derived/): census_unit_measures.csv, census_jump_test.csv, census_target_items.csv,
census_repeated_values.csv, census_e23_by_unit.csv, census_vs_budget.csv, chicago_payments_by_year_fund.csv,
chicago_exits_by_country.csv, account_keying.csv, account_keying_parts.csv, inputs_manifest.json. Deterministic: rerunning on the same
inputs reproduces every output byte for byte.
"""
import csv
import hashlib
import io
import json
import os
import statistics
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FISCAL = os.path.dirname(HERE)
DERIVED = os.path.join(HERE, "derived")

ZIPS = {
    2021: os.path.join(FISCAL, "local_spending_composition_2026_09_18", "_cache", "indunit_2021.zip"),
    2022: os.path.join(FISCAL, "local_spending_composition_2026_09_18", "_cache", "indunit_2022.zip"),
    2023: os.path.join(FISCAL, "local_spending_composition_2026_09_18", "_cache", "indunit_2023.zip"),
    2024: os.path.join(FISCAL, "detention_reconciliation_2026_09_20", "_cache", "census_2024_units.zip"),
}
CHICAGO_PAYMENTS = os.path.join(HERE, "_cache", "src", "chi_gxzc-43gg.csv")
# "Emergency Temporary Shelters - Limited Stay Exits - By Country of Origin - Historical"
CHICAGO_EXITS = os.path.join(HERE, "_cache", "src", "chi_fk7i-xuiy.csv")
BUDGET_FIGURES = os.path.join(HERE, "budget_figures.csv")
CY2024_OUTLAYS = os.path.join(HERE, "cy2024_outlays.csv")
ALLOCATIONS = os.path.join(FISCAL, "full_account_spending_2026_09_20", "derived", "allocations.csv")
# Main-case response of general public services, adopted 2026-09-23
# (decisions/2026-09-23-main-case-general-government-and-use-keys.md); services and household
# transfers respond fully in the main case.
GG_RESPONSE = (0.59, 0.84)
YEARS = [2021, 2022, 2023, 2024]
BASE_YEAR = 2022

# id -> (label, comparison group, role). Names are asserted against every year's PID file.
UNITS = {
    "362061194805": ("NEW YORK CITY", "nyc", "target"),
    "422101133602": ("PHILADELPHIA CITY", "nyc", "peer"),
    "062075161258": ("SAN FRANCISCO CITY AND COUNTY", "nyc", "peer"),
    "061037123085": ("LOS ANGELES COUNTY", "nyc", "peer"),
    "062037161174": ("LOS ANGELES CITY", "nyc", "peer"),
    "242510208246": ("BALTIMORE CITY", "nyc", "peer"),
    "172031162236": ("CHICAGO CITY", "chicago", "target"),
    # context only (no peer statistics): printed for the E23 reporting break
    "171031102545": ("COOK COUNTY", "chicago", "context"),
    "482201176169": ("HOUSTON CITY", "chicago", "peer"),
    "042013207536": ("PHOENIX CITY", "chicago", "peer"),
    "482029175988": ("SAN ANTONIO CITY", "chicago", "peer"),
    "062073207598": ("SAN DIEGO CITY", "chicago", "peer"),
    "482113187649": ("DALLAS CITY", "chicago", "peer"),
    "532033184255": ("SEATTLE CITY", "chicago", "peer"),
    "392049209050": ("COLUMBUS CITY", "chicago", "peer"),
    "082031194647": ("DENVER CITY AND COUNTY", "denver", "target"),
    "472037175728": ("NASHVILLE-DAVIDSON COUNTY METROPOLITAN GOVERNMENT", "denver", "peer"),
    "212111165866": ("LOUISVILLE-JEFFERSON COUNTY METRO GOVERNMENT", "denver", "peer"),
    "182097207957": ("INDIANAPOLIS CITY", "denver", "peer"),
    "122031101942": ("JACKSONVILLE CITY", "denver", "peer"),
    "152003183701": ("HONOLULU CITY AND COUNTY", "denver", "peer"),
    "112001124214": ("WASHINGTON DC CITY", "dc", "target"),
    "250000227530": ("MASSACHUSETTS", "states", "target"),
    "360000227535": ("NEW YORK", "states", "target"),
    "170000227525": ("ILLINOIS", "states", "target"),
    "090000226350": ("CONNECTICUT", "states", "peer"),
    "340000226356": ("NEW JERSEY", "states", "peer"),
    "240000227750": ("MARYLAND", "states", "peer"),
    "530000227543": ("WASHINGTON", "states", "peer"),
    "270000226354": ("MINNESOTA", "states", "peer"),
    "510000227542": ("VIRGINIA", "states", "peer"),
    "420000227538": ("PENNSYLVANIA", "states", "peer"),
    "550000227544": ("WISCONSIN", "states", "peer"),
}
# DC has no same-type peer set of its own; it is compared with the NYC peer governments.
PEER_GROUP = {"nyc": "nyc", "chicago": "chicago", "denver": "denver", "dc": "nyc", "states": "states"}

DIRECT = set("EFGKJ")
INTERGOV_EXP = set("LMQS")
NON_GENERAL = {"90", "91", "92", "93", "94"}
WELFARE = {"67", "68", "74", "75", "77", "79"}
MEASURES = [
    ("total_direct_general", "direct expenditure, all general functions, incl. interest I89"),
    ("total_direct_general_ex_e23", "the same, excluding E23 (reporting break in the 2022 file)"),
    ("fin_admin_current", "financial administration, current operations (E23)"),
    ("welfare_direct", "public welfare, direct (67,68,74,75,77,79)"),
    ("welfare_cash", "public welfare cash assistance (67,68)"),
    ("welfare_vendor", "public welfare vendor payments (74,75)"),
    ("welfare_institutions", "public welfare institutions (77)"),
    ("welfare_other", "public welfare other, incl. homeless shelters (79)"),
    ("housing_commdev", "housing and community development (50)"),
    ("health", "health (32)"),
    ("hospitals", "hospitals (36)"),
    ("other_unallocable", "other and unallocable (89), excluding interest"),
    ("candidate_functions", "welfare + housing + health + hospitals + other and unallocable"),
    ("candidate_current_ops", "current operations (E) only, in the candidate functions"),
    ("ig_exp_welfare", "intergovernmental expenditure for public welfare (L/M/Q/S x welfare)"),
    ("ig_exp_total", "intergovernmental expenditure, all functions"),
    ("rev_fed_total", "federal intergovernmental revenue, all B codes"),
    ("rev_state_total", "state intergovernmental revenue, all C codes"),
]
TEST_MEASURES = ["total_direct_general", "total_direct_general_ex_e23", "fin_admin_current",
                 "candidate_functions", "candidate_current_ops", "welfare_direct",
                 "housing_commdev", "health", "hospitals", "other_unallocable", "ig_exp_welfare",
                 "rev_fed_total", "rev_state_total"]
CANDIDATE = {"welfare_direct", "housing_commdev", "health", "hospitals", "other_unallocable"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def member(zf, key):
    names = [n for n in zf.namelist() if key in n and n.endswith(".txt")]
    if len(names) != 1:
        raise RuntimeError(f"expected one {key} member, found {names}")
    return names[0]


def classify(item):
    """Return the measures one item code contributes to."""
    kind, func = item[0], item[1:3]
    out = []
    if kind in DIRECT and func not in NON_GENERAL:
        out.append("total_direct_general")
        # E23 jumps in the 2022 file for many governments (NYC $0.6bn -> $10.1bn) with no
        # offsetting fall elsewhere; totals compared across years are also given without it
        out.append("fin_admin_current" if item == "E23" else "total_direct_general_ex_e23")
        if func in WELFARE:
            out.append("welfare_direct")
            out.append({"67": "welfare_cash", "68": "welfare_cash", "74": "welfare_vendor",
                        "75": "welfare_vendor", "77": "welfare_institutions",
                        "79": "welfare_other"}[func])
        elif func == "50":
            out.append("housing_commdev")
        elif func == "32":
            out.append("health")
        elif func == "36":
            out.append("hospitals")
        elif func == "89":
            out.append("other_unallocable")
        if CANDIDATE.intersection(out):
            out.append("candidate_functions")
            if kind == "E":
                out.append("candidate_current_ops")
    elif kind == "I" and func == "89":
        out.append("total_direct_general")
        out.append("total_direct_general_ex_e23")
    elif kind in INTERGOV_EXP:
        out.append("ig_exp_total")
        if func in WELFARE:
            out.append("ig_exp_welfare")
    elif kind == "B":
        out.append("rev_fed_total")
    elif kind == "C":
        out.append("rev_state_total")
    return out


def read_year(year):
    amounts = defaultdict(float)      # (uid, measure) -> thousands
    items = defaultdict(float)        # (uid, item code) -> thousands, targets only
    imputed = defaultdict(float)      # (uid, measure) -> thousands flagged I
    n_items = defaultdict(int)
    flags = defaultdict(lambda: defaultdict(int))
    pid = {}
    with zipfile.ZipFile(ZIPS[year]) as zf:
        with zf.open(member(zf, "Fin_PID")) as fh:
            for raw in io.TextIOWrapper(fh, encoding="latin-1"):
                line = raw.rstrip("\r\n")
                uid = line[0:12]
                if uid in UNITS:
                    pid[uid] = {"name": line[12:76].strip(), "fy_end": line[140:144],
                                "population": line[116:125].strip()}
        with zf.open(member(zf, "FinEstDAT")) as fh:
            for raw in io.TextIOWrapper(fh, encoding="latin-1"):
                line = raw.rstrip("\r\n")
                uid = line[0:12]
                if uid not in UNITS:
                    continue
                if len(line) != 32:
                    raise RuntimeError(f"{year}: record length {len(line)} for {uid}: {line!r}")
                item, amt, yr, flag = line[12:15], int(line[15:27]), line[27:31], line[31]
                if yr != str(year):
                    raise RuntimeError(f"{year}: record year {yr} for {uid}")
                flags[uid][flag] += 1
                if UNITS[uid][2] == "target":
                    items[(uid, item)] += amt
                for m in classify(item):
                    amounts[(uid, m)] += amt
                    n_items[(uid, m)] += 1
                    if flag == "I":
                        imputed[(uid, m)] += amt
    for uid, (label, _, _) in UNITS.items():
        if uid not in pid:
            raise RuntimeError(f"{year}: unit {uid} {label} missing from PID file")
        if pid[uid]["name"] != label:
            raise RuntimeError(f"{year}: unit {uid} is {pid[uid]['name']!r}, expected {label!r}")
        if not flags[uid]:
            raise RuntimeError(f"{year}: unit {uid} {label} has no finance records")
    return amounts, imputed, n_items, flags, pid, items


def fmt(x):
    return "" if x is None else f"{x:.1f}"


def pct(a, b):
    return None if not b else 100.0 * (a - b) / b


def main():
    os.makedirs(DERIVED, exist_ok=True)
    data = {}
    for y in YEARS:
        data[y] = read_year(y)
        print(f"[read] {y}", flush=True)

    # 1. long table of measures
    rows = []
    for uid, (label, group, role) in sorted(UNITS.items(), key=lambda kv: (kv[1][1], kv[1][2] != "target", kv[1][0])):
        for y in YEARS:
            amounts, imputed, n_items, flags, pid, _ = data[y]
            for m, _ in MEASURES:
                rows.append({
                    "group": group, "role": role, "unit_id": uid, "unit": label, "survey_year": y,
                    "fy_end_mmdd": pid[uid]["fy_end"], "measure": m,
                    "amount_thousands": amounts.get((uid, m), 0),
                    "imputed_thousands": imputed.get((uid, m), 0),
                    "n_items": n_items.get((uid, m), 0),
                    "unit_items_reported": flags[uid].get("R", 0),
                    "unit_items_imputed": flags[uid].get("I", 0),
                    "unit_items_other_flag": sum(v for k, v in flags[uid].items() if k not in "RI"),
                })
    with open(os.path.join(DERIVED, "census_unit_measures.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (int(v) if isinstance(v, float) else v) for k, v in r.items()})

    # 2. jump test: 2023 and 2024 against 2022; a target's excess is its change minus what the
    #    peer median growth rate would have given on its own 2022 level
    val = {(r["unit_id"], r["survey_year"], r["measure"]): r["amount_thousands"] for r in rows}
    jump = []
    for uid, (label, group, role) in sorted(UNITS.items(), key=lambda kv: (kv[1][1], kv[1][2] != "target", kv[1][0])):
        for m in TEST_MEASURES:
            base = val[(uid, BASE_YEAR, m)]
            rec = {"group": group, "role": role, "unit": label, "measure": m,
                   "y2021_k": val[(uid, 2021, m)], "y2022_k": base,
                   "y2023_k": val[(uid, 2023, m)], "y2024_k": val[(uid, 2024, m)]}
            peers = [u for u, (_, g, r) in UNITS.items() if g == PEER_GROUP[group] and r == "peer"]
            for y in (2023, 2024):
                chg = val[(uid, y, m)] - base
                rec[f"chg_{y}_k"] = chg
                rec[f"chg_{y}_pct"] = pct(val[(uid, y, m)], base)
                pp = sorted(p for p in (pct(val[(u, y, m)], val[(u, BASE_YEAR, m)]) for u in peers)
                            if p is not None)
                ok = role == "target" and pp and base
                rec[f"peer_n_{y}"] = len(pp) if ok else None
                rec[f"peer_min_{y}_pct"] = pp[0] if ok else None
                rec[f"peer_median_{y}_pct"] = statistics.median(pp) if ok else None
                rec[f"peer_max_{y}_pct"] = pp[-1] if ok else None
                rec[f"excess_{y}_k"] = chg - base * statistics.median(pp) / 100.0 if ok else None
            jump.append(rec)
    with open(os.path.join(DERIVED, "census_jump_test.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(jump[0]), lineterminator="\n")
        w.writeheader()
        for r in jump:
            w.writerow({k: (fmt(v) if isinstance(v, float) or v is None else v) for k, v in r.items()})

    # 2b. every item code of every target, by year (2021 uses the finer code set)
    with open(os.path.join(DERIVED, "census_target_items.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["unit", "item", "y2021_k", "y2022_k", "y2023_k", "y2024_k", "chg_2022_2024_k"])
        for uid, (label, _, role) in sorted(UNITS.items(), key=lambda kv: kv[1][0]):
            if role != "target":
                continue
            codes = sorted({it for y in YEARS for (u, it) in data[y][5] if u == uid})
            for it in codes:
                v = [data[y][5].get((uid, it), 0.0) for y in YEARS]
                w.writerow([label, it] + [int(x) for x in v] + [int(v[3] - v[1])])

    # 2c. repeated values: a nonzero item identical to the thousand dollars in two of the
    #     2022-2024 files suggests a carried-forward figure rather than a new report
    with open(os.path.join(DERIVED, "census_repeated_values.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["unit", "item", "year_a", "year_b", "amount_k"])
        for uid, (label, _, role) in sorted(UNITS.items(), key=lambda kv: kv[1][0]):
            if role != "target":
                continue
            for ya, yb in ((2022, 2023), (2022, 2024), (2023, 2024)):
                for (u, it), amt in sorted(data[ya][5].items()):
                    if u == uid and amt >= 1000 and data[yb][5].get((uid, it)) == amt:
                        w.writerow([label, it, ya, yb, int(amt)])

    # 2d. E23 (financial administration, current operations) for every unit: the 2022 file
    #     carries a reporting break in this item, so it is shown apart and kept out of the
    #     candidate functions and the part weights
    with open(os.path.join(DERIVED, "census_e23_by_unit.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "role", "unit", "y2021_k", "y2022_k", "y2023_k", "y2024_k",
                    "chg_2021_2022_k", "chg_2022_2024_k", "e23_share_of_total_2024_pct"])
        for uid, (label, group, role) in sorted(UNITS.items(), key=lambda kv: (kv[1][1], kv[1][2] != "target", kv[1][0])):
            v = [val[(uid, y, "fin_admin_current")] for y in YEARS]
            tot = val[(uid, 2024, "total_direct_general")]
            w.writerow([group, role, label] + [int(x) for x in v]
                       + [int(v[1] - v[0]), int(v[3] - v[1]), fmt(100.0 * v[3] / tot if tot else None)])

    # 3. Chicago vendor payments by invoice year and funding source
    regroup = {
        ("City Corporate Fund", "CORPORATE FUND"): "city_corporate",
        ("ARPA", "CORONAVIRUS LOCAL FISCAL RECOVERY FUND"): "federal_arpa_slfrf",
        ("Cook County Asylum Seeker Grant", "DISASTER RESPONSE AND RECOVERY FUND"): "cook_county",
        ("Federal Health Grant", "BIOTERRORISM PREPAREDNESS RESPONSE"): "federal_health",
        ("State Asylum Seeker Grants", "STATE OF ILLINOIS ASYLUM SUPPORT GRANT"): "state_own",
        ("State Asylum Seeker Grants", "SMASS GRANT"): "state_own",
        ("State Asylum Seeker Grants", "FEMA SHELTER SERVICES PROGRAM"): "federal_fema_via_state",
        ("State Asylum Seeker Grants", "SHELTER AND SERVICES PROGRAM"): "federal_fema_via_state",
    }
    pay = defaultdict(float)
    with open(CHICAGO_PAYMENTS, newline="") as f:
        for r in csv.DictReader(f):
            date = r["DATE OF INVOICE"] or r["DATE OF GOODS RECEIVED"] or r["DATE OF CHECK"]
            year = date[:4] if date else "unknown"
            key = (r["FUND (GROUPED)"], r["FUND (DESCRIPTION)"])
            src = regroup.get(key)
            if src is None:
                if r["FUND (GROUPED)"] == "FEMA Asylum Seeker Grants":
                    src = "federal_fema_direct"
                else:
                    raise RuntimeError(f"unmapped Chicago fund {key}")
            pay[(year, src)] += float(r["AMOUNT (DOLLARS)"] or 0)
    sources = ["city_corporate", "state_own", "cook_county", "federal_fema_direct",
               "federal_fema_via_state", "federal_arpa_slfrf", "federal_health"]
    with open(os.path.join(DERIVED, "chicago_payments_by_year_fund.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["invoice_year"] + [s + "_usd" for s in sources] + ["total_usd"])
        for year in sorted({k[0] for k in pay}):
            vals = [pay.get((year, s), 0.0) for s in sources]
            w.writerow([year] + [f"{v:.2f}" for v in vals] + [f"{sum(vals):.2f}"])
        tot = [sum(v for (yy, s2), v in pay.items() if s2 == s) for s in sources]
        w.writerow(["all"] + [f"{v:.2f}" for v in tot] + [f"{sum(tot):.2f}"])

    # 3b. Chicago shelter exits at the stay limit, by country of origin (weekly counts, 2024)
    exits = defaultdict(int)
    weeks = set()
    with open(CHICAGO_EXITS, newline="") as f:
        for r in csv.DictReader(f):
            exits[r["Country of Origin"]] += int(r["Count of Exits"])
            weeks.add(r["Week End"])
    n_exits = sum(exits.values())
    with open(os.path.join(DERIVED, "chicago_exits_by_country.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["country", "exits", "share_pct", "weeks", "first_week_end", "last_week_end"])
        ends = sorted(weeks, key=lambda d: (d[6:], d[:5]))
        for c, n in sorted(exits.items(), key=lambda kv: (-kv[1], kv[0])):
            w.writerow([c, n, f"{100.0 * n / n_exits:.2f}", len(weeks), ends[0], ends[-1]])

    # 4. Census measures beside each budget figure for the same fiscal period. Chicago's rows come
    #    from its own payment file: calendar year Y-1 enters survey year Y.
    figures = []
    with open(BUDGET_FIGURES, newline="") as f:
        figures.extend(csv.DictReader(f))
    for y in (2023, 2024):
        cy = str(y - 1)
        figures.append({
            "unit_id": "172031162236", "survey_year": str(y), "fiscal_period": f"CY{cy}",
            "budget_item": "New Arrivals vendor payments by invoice year, all funding sources",
            "budget_thousands": f"{sum(v for (yy, _), v in pay.items() if yy == cy) / 1000:.0f}",
            "source": "City of Chicago data portal gxzc-43gg (derived/chicago_payments_by_year_fund.csv)"})
    compare = ["candidate_functions", "candidate_current_ops", "welfare_direct", "housing_commdev",
               "health", "hospitals", "other_unallocable", "total_direct_general",
               "total_direct_general_ex_e23", "ig_exp_welfare"]
    budget = []
    for b in figures:
        uid, y = b["unit_id"], int(b["survey_year"])
        rec = {"unit": UNITS[uid][0], "survey_year": y, "fiscal_period": b["fiscal_period"],
               "budget_item": b["budget_item"], "budget_thousands": b["budget_thousands"]}
        for m in compare:
            rec[f"{m}_k"] = int(val[(uid, y, m)])
            rec[f"{m}_chg_vs_2022_k"] = int(val[(uid, y, m)] - val[(uid, 2022, m)]) if y > 2022 else ""
        rec["budget_source"] = b["source"]
        budget.append(rec)
    with open(os.path.join(DERIVED, "census_vs_budget.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(budget[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(budget)

    # 5. How the complete account keys these outlays to the Mexican-origin union, against the
    #    union's share of the people served. [CALCULATION; assumptions in RESULT.md, part 4]
    #    Part weights: where NYC's FY2024 current-operations increase over FY2022 landed
    #    (E79 welfare, E50 housing, E89 other/unallocable, E32 health).
    nyc = "362061194805"
    parts = {"welfare": "E79", "housing": "E50", "other": "E89", "health": "E32"}
    inc = {k: data[2024][5].get((nyc, it), 0.0) - data[2022][5].get((nyc, it), 0.0)
           for k, it in parts.items()}
    weight = {k: v / sum(inc.values()) for k, v in inc.items()}
    shares = {}
    with open(ALLOCATIONS, newline="") as f:
        for r in csv.DictReader(f):
            if r["scenario_id"] == "complete_preferred_F_per_capita" and r["allocation"] == "personal":
                shares[r["category"]] = (float(r["target_share_national"]), r["response_class"])
    # each mapping sends a part to a BEA category of the account
    mappings = {
        "A_nyc_codes_consumption": {"welfare": "income_security_services", "housing": "housing_community_services",
                                    "other": "general_public_services", "health": "health_services"},
        "B_all_income_security": {k: "income_security_services" for k in parts},
        "C_nyc_codes_welfare_to_nonprofit_benefits": {"welfare": "other_state_welfare",
                                                      "housing": "housing_community_services",
                                                      "other": "general_public_services", "health": "health_services"},
        "D_all_nonprofit_benefits": {k: "other_state_welfare" for k in parts},
    }
    outlays = {"low": 0.0, "central": 0.0, "high": 0.0}
    with open(CY2024_OUTLAYS, newline="") as f:
        for r in csv.DictReader(f):
            for c in outlays:
                outlays[c] += float(r[f"{c}_musd"])
    # NYC: Mexico / guests in care, Council Terms and Conditions reports (Feb 2025 p.10, June 2025 p.11)
    served = {"nyc_feb2025": 219 / 43578, "nyc_jun2025": 231 / 36684,
              "chicago_exits_2024": exits["Mexico"] / n_exits, "allowance_2pct": 0.02}
    grid = []
    for oc, total in outlays.items():
        for mname, mp in mappings.items():
            for gg in GG_RESPONSE:
                resp = {k: (gg if shares[mp[k]][1] == "public_goods" else 1.0) for k in parts}
                key = sum(weight[k] * shares[mp[k]][0] for k in parts)
                charged = sum(total * weight[k] * shares[mp[k]][0] * resp[k] for k in parts)
                for sname, s in served.items():
                    used = sum(total * weight[k] * s * resp[k] for k in parts)
                    grid.append({"outlays_case": oc, "cy2024_outlays_musd": f"{total:.0f}",
                                 "mapping": mname, "general_govt_response": gg,
                                 "weighted_key_share": f"{key:.4f}", "served_case": sname,
                                 "served_share": f"{s:.4f}",
                                 "account_charge_musd": f"{charged:.1f}",
                                 "use_based_charge_musd": f"{used:.1f}",
                                 "overcharge_musd": f"{charged - used:.1f}",
                                 "charge_to_use_ratio": f"{charged / used:.1f}"})
    with open(os.path.join(DERIVED, "account_keying.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grid[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(grid)
    with open(os.path.join(DERIVED, "account_keying_parts.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["part", "nyc_item", "nyc_increase_fy2022_fy2024_k", "weight"]
                   + [f"{m}_category" for m in mappings])
        for k, it in parts.items():
            w.writerow([k, it, int(inc[k]), f"{weight[k]:.4f}"] + [mappings[m][k] for m in mappings])
        w.writerow([])
        w.writerow(["category", "target_share_national", "response_class"])
        for c in sorted({c for mp in mappings.values() for c in mp.values()}):
            w.writerow([c, f"{shares[c][0]:.5f}", shares[c][1]])

    manifest = {
        "script": os.path.basename(__file__),
        "script_sha256": sha256(__file__),
        "inputs": {**{str(y): {"path": os.path.relpath(p, FISCAL), "sha256": sha256(p)} for y, p in ZIPS.items()},
                   "chicago_payments": {"path": os.path.relpath(CHICAGO_PAYMENTS, FISCAL), "sha256": sha256(CHICAGO_PAYMENTS)},
                   "chicago_exits": {"path": os.path.relpath(CHICAGO_EXITS, FISCAL), "sha256": sha256(CHICAGO_EXITS)},
                   "budget_figures": {"path": os.path.relpath(BUDGET_FIGURES, FISCAL), "sha256": sha256(BUDGET_FIGURES)},
                   "cy2024_outlays": {"path": os.path.relpath(CY2024_OUTLAYS, FISCAL), "sha256": sha256(CY2024_OUTLAYS)},
                   "account_allocations": {"path": os.path.relpath(ALLOCATIONS, FISCAL), "sha256": sha256(ALLOCATIONS)}},
        "outputs": {n: sha256(os.path.join(DERIVED, n)) for n in sorted(os.listdir(DERIVED))
                    if n.endswith(".csv")},
    }
    with open(os.path.join(DERIVED, "inputs_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
        f.write("\n")
    print("[done]", ", ".join(sorted(manifest["outputs"])), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

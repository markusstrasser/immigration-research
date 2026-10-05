"""Write derived/conclusions_oct05.csv and derived/common_mode_oct05.csv: the nine conclusions on main case v5.

The v5 case is main_case_2026_10_05 (adopted 2026-10-05, key oct05): the v4 case (main_case_2026_09_29) plus the 3.04M
descendants of Mexican immigrants who no longer report Mexican origin, counted whole (a lineage of 42.75M). Each row tests
the evidence map's claim as it stands in overview_2026_09_28/groups.py (still on the September 27 case) against v5. The
text cells are this lane's reading of `engine_breaks_sept29.cjs --case oct05`'s outputs and of the cited lanes' oct05
files. Every number quoted from them is recomputed here first, so a changed input stops the build instead of leaving
stale text. tables.py's and tables_sept29.py's files are not touched. Premise P20 is new on v5: the lineage count.
Run after `node engine_breaks_sept29.cjs --case oct05`:
    uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_oct05.py
"""
import csv
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
F = HERE.parent


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def check(label, got, want, tol=0.05):
    if abs(got - want) > tol:
        sys.exit(f"[BLOCKED] {label}: computed {got:.4f}, text says {want}")


def num(r, k):
    return float(r[k])


ENDS = ["low_end_48", "high_end_11"]
LANE = F / "main_case_2026_10_05/derived"
LINEAGE = F / "main_case_lineage_2026_10_05/derived"

# ---- C1: arms and minimal cuts
arms = {r["arm"]: r for r in rows(D / "c1_arms_oct05.csv")}
cuts = {(r["direction"], r["set"]): r for r in rows(D / "c1_min_cuts_oct05.csv")}
check("case low", num(arms["adopted"], "cost_low_bn"), 390.29)
check("case high", num(arms["adopted"], "cost_high_bn"), 461.24)
mid = num(arms["adopted"], "midpoint_bn")
check("midpoint", mid, 425.77)
bands = {r["variant"]: r for r in rows(LANE / "main_case_bands.csv") if r["profile"] == "long_run_non_school_full"}
mid27 = (num(bands["sept27_case"], "cost_low_bn") + num(bands["sept27_case"], "cost_high_bn")) / 2
check("September 27 midpoint", mid27, 354.59, tol=0.005)
check("move on September 27", 100 * (mid / mid27 - 1), 20.1)
central = next(r for r in rows(LINEAGE / "v5_bands.csv") if r["set"] == "set" and r["arm"] == "b" and r["variant"] == "central")
check("per member low", num(central, "per_member_low_usd"), 9129, tol=0.5)
check("per member high", num(central, "per_member_high_usd"), 10789, tol=0.5)
check("lineage population", num(central, "population") / 1e6, 42.75, tol=0.005)
check("down cut", 0.75 * mid, 319.33, tol=0.005)
check("up cut", 1.25 * mid, 532.21, tol=0.005)
for arm, lo, hi, move in [("first_year_horizon", 289.10, 335.34, -26.7), ("first_year_horizon_cash", 206.19, 257.51, -45.5),
                          ("ancestry_share_low", 275.39, 322.13, -29.8), ("pension_cash", 307.38, 383.41, -18.9)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo, tol=0.005)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi, tol=0.005)
    check(f"{arm} move", num(arms[arm], "move_pct_of_midpoint"), move)
for arm, move in [("first_year_horizon_property_long_run", -33.7), ("capital_7pct", 20.6), ("property_none", 7.1),
                  ("school_within_district", -6.4), ("pension_scheduled", 8.5), ("lineage_arm_a", -2.8), ("lineage_arm_c", 2.8),
                  ("lineage_c3_plus_1se", -0.8), ("lineage_c3_minus_1se", 0.8), ("replacement_r1", -2.1),
                  ("ancestry_share_high", -17.5), ("ancestry_share_convention", -19.2)]:
    check(f"{arm} alone", num(arms[arm], "move_pct_of_midpoint"), move)
if max(abs(num(arms[a], "move_pct_of_midpoint")) for a in ["lineage_arm_a", "lineage_arm_c", "lineage_c3_plus_1se",
                                                             "lineage_c3_minus_1se", "replacement_r1", "replacement_r05"]) >= 3:
    sys.exit("[BLOCKED] a lineage alternative other than the ancestry-share count moves C1 by 3% or more; the text says less")
for key, lo, hi, move in [(("down", "capital_off+pension_cash"), 270.23, 321.55, -30.5),
                          (("down", "roads_parks_first_year+pension_cash"), 277.02, 333.33, -28.3),
                          (("down", "school_within_district+pension_cash"), 279.35, 356.82, -25.3)]:
    check(f"{key} low", num(cuts[key], "cost_low_bn"), lo, tol=0.005)
    check(f"{key} high", num(cuts[key], "cost_high_bn"), hi, tol=0.005)
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move)
for key, move in [(("down", "capital_off+school_within_district+roads_parks_first_year+care_low"), -26.5),
                  (("down", "capital_off+ancestry_share_convention"), -30.9), (("down", "pension_cash+ancestry_share_convention"), -34.2),
                  (("down", "roads_parks_first_year+ancestry_share_convention"), -28.7),
                  (("down", "school_within_district+ancestry_share_convention"), -25.7),
                  (("up", "capital_7pct+defense_gdp_share"), 34.7), (("up", "capital_7pct+pension_scheduled"), 29.1),
                  (("up", "capital_7pct+property_none"), 27.6), (("up", "long_run_high+pension_scheduled+defense_gdp_share"), 25.7)]:
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move)
minimal = [r for r in cuts.values() if r["minimal"] == "yes"]
size = lambda r: int(float(r["size"]))
parts = lambda r: r["set"].split("+")
ancestry = lambda r: any(p.startswith("ancestry_share") for p in parts(r))
down = [r for r in minimal if r["direction"] == "down"]
up = [r for r in minimal if r["direction"] == "up"]
if [r["set"] for r in down if size(r) == 1] != ["ancestry_share_low"]:
    sys.exit("[BLOCKED] the single downward cuts are not the ancestry-share count's low end alone")
if min(size(r) for r in down if not ancestry(r)) != 2 or any("pension_cash" not in parts(r) for r in down if not ancestry(r) and size(r) == 2):
    sys.exit("[BLOCKED] with whole people the smallest downward cuts are not pairs with cash pensions")
if min(size(r) for r in down if not ancestry(r) and "pension_cash" not in parts(r)) != 4:
    sys.exit("[BLOCKED] with whole people and without cash pensions the smallest downward cut is not 4")
if min(size(r) for r in up) != 2 or min(size(r) for r in up if "capital_7pct" not in parts(r)) != 3:
    sys.exit("[BLOCKED] the upward cuts are not 2 with 7% capital and 3 without")
stacks = {(r["direction"], size(r)): r for r in cuts.values() if r["minimal"] == "stack"}
if set(stacks) != {("down", 8), ("down", 9), ("up", 6), ("up", 7)}:
    sys.exit(f"[BLOCKED] the stacks are {sorted(stacks)}; the text says 8 / 9 downward and 6 / 7 upward")
check("down stack", num(stacks[("down", 8)], "move_pct_of_midpoint"), -50.8)
check("down stack with the ancestry share", num(stacks[("down", 9)], "move_pct_of_midpoint"), -74.7)
check("up stack", num(stacks[("up", 6)], "move_pct_of_midpoint"), 55.4)
check("up stack with arm c", num(stacks[("up", 7)], "move_pct_of_midpoint"), 58.1)
if not stacks[("down", 9)]["set"].endswith("+ancestry_share_low") or not stacks[("up", 7)]["set"].endswith("+lineage_arm_c"):
    sys.exit("[BLOCKED] the lineage stacks do not add the ancestry share's low end and arm c")
check("first-year horizon clears the cut by", -num(arms["first_year_horizon"], "move_pct_of_midpoint") - 25, 1.7)

# ---- C2: tally and break-evens
tally = {(r["model"], r["end"]): r for r in rows(D / "c2_tally_oct05.csv")}
for model, col, want in [("case_accrual", "tally_bn", (6.5, -4.4)), ("case_accrual", "direct_receipts_bn", (450.5, 424.0)),
                         ("case_accrual", "household_transfers_bn", (444.0, 428.4)), ("case_accrual", "tally_at_scheduled_bn", (-30.7, -39.3)),
                         ("union_at_case_responses", "tally_bn", (-3.4, -12.6)), ("cash_set", "tally_bn", (89.4, 73.4)),
                         ("v4_items_without_dataset_corrections", "tally_bn", (11.1, 0.4)), ("lineage_arm_a", "tally_bn", (4.6, -5.3)),
                         ("lineage_arm_c", "tally_bn", (8.4, -3.5))]:
    for end, w in zip(ENDS, want):
        check(f"C2 {model} {col} {end}", num(tally[(model, end)], col), w)
own = [num(tally[("case_accrual", e)], "tally_bn") - num(tally[("union_at_case_responses", e)], "tally_bn") for e in ENDS]
check("C2 the added people's own tally, low", own[0], 9.9)
check("C2 the added people's own tally, high", own[1], 8.2)
# Printed parts add: union -3.4 + added 9.9 = 6.5; -12.6 + 8.2 = -4.4.
if (round(-3.4 + 9.9, 1), round(-12.6 + 8.2, 1)) != (6.5, -4.4):
    sys.exit("[BLOCKED] the printed tally parts do not add")
be = {(r["case"], r["variant"], r["allocation"]): r for r in rows(D / "c2_break_even_oct05.csv")}
for key, most, least in [(("case_accrual", "enterprises_at_1", "personal"), -8.8, -0.4), (("case_accrual", "enterprises_at_1", "shared"), -6.9, 1.7),
                         (("case_accrual", "enterprises_at_s", "personal"), -3.4, 3.4), (("case_accrual", "enterprises_at_s", "shared"), -1.5, 5.5)]:
    check(f"{key} most", 100 * num(be[key], "break_even_most_adverse"), most)
    check(f"{key} least", 100 * num(be[key], "break_even_least_adverse"), least)
cash_be = [100 * num(r, k) for (c, _, _), r in be.items() if c == "cash_set" for k in r if k.startswith("break_even")]
check("cash set break-even, lowest", min(cash_be), 9.0)
check("cash set break-even, highest", max(cash_be), 24.5)
# Clause 1's distance: the tax and transfer tails of components.csv, additive.
comp = {r["component"]: r for r in rows(LANE / "components.csv")}
LO = {"low_end_48": "range_dev_low_end_lo", "high_end_11": "range_dev_high_end_lo"}
HI = {"low_end_48": "range_dev_low_end_hi", "high_end_11": "range_dev_high_end_hi"}
TAX_TRANSFER_TAILS = ["tax_block", "income_tax", "medical", "ltss", "benefits", "care"]
t0 = {e: num(tally[("case_accrual", e)], "tally_bn") for e in ENDS}
restore = [k for k in TAX_TRANSFER_TAILS if t0["high_end_11"] - num(comp[k], LO["high_end_11"]) > 0]
if restore != ["care"]:
    sys.exit(f"[BLOCKED] single tails restoring clause 1 at the high end: {restore}; the text says care alone")
check("tally, high end, care's favorable tail", t0["high_end_11"] - num(comp["care"], LO["high_end_11"]), 4.8)
check("tally, high end, the tax block's favorable tail", t0["high_end_11"] - num(comp["tax_block"], LO["high_end_11"]), -0.15, tol=0.005)
pairs = [t0["high_end_11"] - num(comp["tax_block"], LO["high_end_11"]) - num(comp[k], LO["high_end_11"]) for k in TAX_TRANSFER_TAILS[1:]]
check("tally, high end, tax block plus one more tail, smallest", min(pairs), 1.0)
breaks_low = [k for k in TAX_TRANSFER_TAILS if t0["low_end_48"] - num(comp[k], HI["low_end_48"]) < 0]
if breaks_low != ["medical"]:
    sys.exit(f"[BLOCKED] single tails breaking clause 1 at the low end: {breaks_low}; the text says medical alone")
check("tally, low end, medical's adverse tail", t0["low_end_48"] - num(comp["medical"], HI["low_end_48"]), -2.0)
check("tally, low end, the tax block's adverse tail", t0["low_end_48"] - num(comp["tax_block"], HI["low_end_48"]), 0.9)

# ---- C3: the corrections by side (the lineage's edits held in every run)
split = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_oct05.csv")}
for reading, col, want in [("pension_rebuilt", "taxes_move_by_line_type_bn", (44.43, 45.84)), ("pension_rebuilt", "spending_move_by_line_type_bn", (-55.16, -57.15)),
                           ("pension_rebuilt", "net_move_bn", (-10.73, -11.31)), ("pension_rebuilt", "accrual_follow_through_bn", (-10.66, -11.47)),
                           ("pension_rebuilt", "oasdi_receipts_move_bn", (-10.95, -11.78)), ("pension_rebuilt", "tax_side_move_bn", (33.77, 34.37)),
                           ("pension_rebuilt", "spending_side_move_bn", (-44.50, -45.68)), ("increments_held", "tax_side_move_bn", (44.43, 45.84)),
                           ("increments_held", "spending_side_move_bn", (-55.29, -56.91)), ("increments_held", "net_move_bn", (-10.86, -11.07))]:
    for end, w in zip(ENDS, want):
        check(f"C3 {reading} {col} {end}", num(split[(reading, end)], col), w, tol=0.005)
    if col == "net_move_bn" and any(abs(num(split[(reading, e)], "interaction_bn")) > 1e-6 for e in ENDS):
        sys.exit(f"[BLOCKED] C3 {reading}: the sides interact; the text says no interaction")
for end, w in zip(ENDS, (-10.79, -11.23)):
    check(f"C3 benefit corrections the accrual replaces, {end}",
          num(split[("increments_held", end)], "spending_side_move_bn") - num(split[("pension_rebuilt", end)], "spending_side_move_bn"), w, tol=0.005)
NOT_DATA = {"school_response", "long_run_response", "capital_rate", "capital_definition", "finite_removal", "property_long_run", "payroll_compliance"}
data_tails = [k for k in comp if k not in NOT_DATA]
movers = {e: [k for k in data_tails if max(abs(num(comp[k], LO[e])), abs(num(comp[k], HI[e]))) > 0.25 * abs(num(split[("pension_rebuilt", e)], "net_move_bn"))]
          for e in ENDS}
if (len(movers["low_end_48"]), len(set(movers["low_end_48"]) | set(movers["high_end_11"]))) != (5, 6):
    sys.exit(f"[BLOCKED] tails moving the net by a quarter: {movers}; the text says six (five at the low end)")
for side_cols, one, two, halves in [(("taxes_move_by_line_type_bn", "spending_move_by_line_type_bn"), [], ["care", "tax_block"], (22.2, 22.9)),
                                    (("tax_side_move_bn", "spending_side_move_bn"), ["care"], None, (16.9, 17.2))]:
    for end, half_want in zip(ENDS, halves):
        r = split[("pension_rebuilt", end)]
        net = num(r, "net_move_bn")
        half = min(abs(num(r, c)) for c in side_cols) / 2
        check(f"C3 half the smaller side {side_cols[0]} {end}", half, half_want)
        singles = [k for k in data_tails if abs(net + num(comp[k], LO[end])) > half]
        if singles != one:
            sys.exit(f"[BLOCKED] C3 {side_cols[0]} {end}: single tails ending the cancellation {singles}, the text says {one}")
        if two and abs(net + sum(num(comp[k], LO[end]) for k in two)) <= half:
            sys.exit(f"[BLOCKED] C3 {end}: care low + tax block low do not end the cancellation")
check("C3 care + tax block, low end", num(split[("pension_rebuilt", "low_end_48")], "net_move_bn") + num(comp["care"], LO["low_end_48"])
      + num(comp["tax_block"], LO["low_end_48"]), -25.4)
check("C3 care + tax block, high end", num(split[("pension_rebuilt", "high_end_11")], "net_move_bn") + num(comp["care"], LO["high_end_11"])
      + num(comp["tax_block"], LO["high_end_11"]), -24.8)
check("C3 care alone, low end", num(split[("pension_rebuilt", "low_end_48")], "net_move_bn") + num(comp["care"], LO["low_end_48"]), -19.9)
check("C3 care alone, high end", num(split[("pension_rebuilt", "high_end_11")], "net_move_bn") + num(comp["care"], LO["high_end_11"]), -20.5)
# The same split as on v4 (tables_sept29.py's figures): the lineage's edits are held, so the corrections move the union only.
split29 = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_sept29.csv")}
for k in split:
    for col in ["tax_side_move_bn", "spending_side_move_bn", "net_move_bn", "taxes_move_by_line_type_bn", "oasdi_receipts_move_bn"]:
        check(f"C3 {k} {col} within $0.01bn of v4's", num(split[k], col), num(split29[k], col), tol=0.01)

# ---- C4: the social rows and the pairing (sept24_propagation's oct05 run)
rc = {(r["column"], r["item"]): r["oct05"] for r in rows(F / "sept24_propagation_2026_09_24/derived/oct05/real_costs_totals.csv")}
pair = [float(rc[("pairing_on_priced_count", f"published pairing ({e})")]) for e in ("low", "high")]
footing = [float(rc[("hispanic", "fiscal main case (low)")]), float(rc[("custody", "fiscal main case (high)")])]
social = [p - f for p, f in zip(pair, footing)]
added = [float(rc[("pairing_on_priced_count", f"the added people's social rows ({e})")]) for e in ("low", "high")]
check("pairing low", pair[0], 490.22, tol=0.005)
check("pairing high", pair[1], 570.68, tol=0.005)
check("social rows low", social[0], 104.8)
check("social rows high", social[1], 109.4)
check("added people's social rows low", added[0], 8.6)
check("added people's social rows high", added[1], 8.8)
per = [float(rc[("pairing_on_priced_count", f"published pairing per group member ({e})")]) for e in ("low", "high")]
check("pairing per member low", 1000 * per[0], 11466, tol=0.5)
check("pairing per member high", 1000 * per[1], 13349, tol=0.5)
pmid = sum(pair) / 2
check("pairing down cut", 0.75 * pmid, 397.8)
check("pairing up cut", 1.25 * pmid, 663.1)
dev = {}
for item in ["pm25_consumption", "road_crash_externality", "scale_net_earnings"]:
    c = float(rc[(f"social_item_{item}", "central, both ends")])
    dev[item] = (float(rc[(f"social_item_{item}", "low, full span")]) - c, float(rc[(f"social_item_{item}", "high, full span")]) - c)
for item, lo, hi in [("pm25_consumption", -38.2, 52.8), ("road_crash_externality", -68.7, 63.3), ("scale_net_earnings", -70.5, 70.5)]:
    check(f"{item} low deviation", dev[item][0], lo)
    check(f"{item} high deviation", dev[item][1], hi)
    if min(abs(dev[item][0]), abs(dev[item][1])) < 0.25 * sum(social) / 2:
        sys.exit(f"[BLOCKED] {item} at a range end does not move the add by a quarter")
check("add quarter", 0.25 * sum(social) / 2, 26.8)
check("pairing: crash low + scale low", 100 * (dev["road_crash_externality"][0] + dev["scale_net_earnings"][0]) / pmid, -26.2)
check("pairing: crash high + scale high", 100 * (dev["road_crash_externality"][1] + dev["scale_net_earnings"][1]) / pmid, 25.2)
check("pairing: PM2.5 high + crash high", 100 * (dev["pm25_consumption"][1] + dev["road_crash_externality"][1]) / pmid, 21.9)
if any(abs(dev[a][k] + dev[b][k]) / pmid > 0.25 for a, b in itertools.combinations(dev, 2) for k in (0, 1)
       if {a, b} != {"road_crash_externality", "scale_net_earnings"}):
    sys.exit("[BLOCKED] another pair of items breaks the pairing")
fy = [num(arms["first_year_horizon"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]), num(arms["first_year_horizon"], "cost_high_bn")]
check("pairing at the first-year horizon, social rows held", 100 * ((fy[0] + social[0] + fy[1] + social[1]) / 2 / pmid - 1), -21.4)
cash_pair = [float(rc[("pairing_on_priced_count_cash_set", f"published pairing ({e})")]) for e in ("low", "high")]
check("cash-set pairing low", cash_pair[0], 407.30, tol=0.005)
check("cash-set pairing high", cash_pair[1], 492.85, tol=0.005)
check("cash-set pairing move", 100 * (sum(cash_pair) / 2 / pmid - 1), -15.2)
for item, want in [("social_item_pm25_consumption", -46.5), ("social_item_road_crash_externality", 0.6)]:
    check(f"{item} normalized", float(rc[(item, "normalized central, beside")]), want)

# ---- C5: the state-local share (debt_legacy's oct05 split, central convention, main profile)
split5 = {r["end"]: r for r in rows(F / "debt_legacy_2026_09_23/derived/oct05/federal_split_2024.csv")
          if r["profile"] == "long_run_non_school_full" and r["convention"] == "central"}
COLS = ["fiscal_gap_bn", "resource_cost_bn", "displaced_bn", "accrual_bn"]
FED = ["federal_bn", "resource_cost_federal_bn", "displaced_federal_bn", "accrual_federal_bn"]
with open(F / "debt_legacy_2026_09_23/derived/oct05/summary.json") as f:
    debt = json.load(f)["case"]
# debt_legacy.py keeps the run's case block under "v4" (its v4_summary(); case.v5 adds the lineage).
headline = debt["v4"]["headline_2024"]
if debt["v5"]["lineage"]["counts"]["lineage_population"] / 1e6 - 42.75 > 0.005:
    sys.exit("[BLOCKED] the debt lane's oct05 run is not on the 42.75M lineage")
LEGACY = {e: headline[e]["legacy_interest_2024_bn"] for e in ("low", "high")}
check("legacy interest low", LEGACY["low"], 30.6)
check("legacy interest high", LEGACY["high"], 42.6)
sched = {"low": num(arms["pension_scheduled"], "cost_low_bn") - num(arms["adopted"], "cost_low_bn"),
         "high": num(arms["pension_scheduled"], "cost_high_bn") - num(arms["adopted"], "cost_high_bn")}
share = {}
for e in ("low", "high"):
    r = split5[e]
    tot = sum(num(r, c) for c in COLS)
    sl = tot - sum(num(r, c) for c in FED)
    if abs(num(r, "accrual_bn") - num(r, "accrual_federal_bn")) > 1e-9:
        sys.exit("[BLOCKED] the accrual is not all federal in the debt lane's split")
    share[e] = dict(case=sl / tot, cash=sl / (tot - num(r, "accrual_bn")), scheduled=sl / (tot + sched[e]), defense=sl / (tot + 60),
                    defense_interest=sl / (tot + 60 + LEGACY[e]), defense_interest_scheduled=sl / (tot + 60 + LEGACY[e] + sched[e]),
                    average_cost=sl / (tot + 271))
    check(f"the split's total is the set's net cost plus P, {e}", tot, headline[e]["set_net_cost_bn"] + num(r, "production_P_bn"), tol=1e-6)
for key, want in [("case", (68.8, 68.2)), ("cash", (87.4, 82.1)), ("scheduled", (62.8, 63.4)), ("defense", (59.6, 60.4)),
                  ("defense_interest", (55.8, 55.8)), ("defense_interest_scheduled", (51.8, 52.5)), ("average_cost", (40.6, 43.0))]:
    for e, w in zip(("low", "high"), want):
        check(f"C5 state-local share {key} {e}", 100 * share[e][key], w)
check("accrual low", num(split5["low"], "accrual_bn"), 82.9)
check("accrual high", num(split5["high"], "accrual_bn"), 77.8)

# ---- C6: generations on the generation account's oct05 models (G3+ carries the lineage)
gen = rows(D / "c6_generation_break_even_oct05.csv")
gen29 = rows(D / "c6_generation_break_even_sept29.csv")
bmax = lambda g, case, conv=None: 100 * max(num(r, k) for r in g if r["case"] == case and (conv is None or r["convention"] == conv)
                                            for k in r if k.startswith("break_even"))
for case, conv, want in [("case_accrual", "a", 16.9), ("case_accrual", "b", 21.6), ("cash_set", "a", 38.3), ("cash_set", "b", 41.9)]:
    check(f"C6 largest break-even {case} {conv}", bmax(gen, case, conv), want)
for conv, want in [("a", 3.5), ("b", 3.2)]:
    check(f"C6 rise of the largest break-even on v4's, {conv}", bmax(gen, "case_accrual", conv) - bmax(gen29, "case_accrual", conv), want)
cmin = lambda case: min(min(num(r, "cost_low_end_bn"), num(r, "cost_high_end_bn")) for r in gen if r["case"] == case)
check("C6 smallest generation cost, case", cmin("case_accrual"), 87.0)
check("C6 smallest generation cost, cash set", cmin("cash_set"), 72.6)
g3 = next(r for r in gen if r["case"] == "case_accrual" and r["convention"] == "a" and r["generation"] == "G3plus")
g3_29 = next(r for r in gen29 if r["case"] == "case_accrual" and r["convention"] == "a" and r["generation"] == "G3plus")
for col, now, before in [("cost_low_end_bn", 141.7, 122.6), ("cost_high_end_bn", 195.0, 168.4)]:
    check(f"C6 G3+ (a) {col}", num(g3, col), now)
    check(f"C6 G3+ (a) {col} on v4", num(g3_29, col), before)
if any(num(r, k) >= 0 for r in gen if r["case"] == "case_accrual" and r["convention"] == "b" and r["generation"] == "G1"
       for k in r if k.startswith("break_even")):
    sys.exit("[BLOCKED] a G1 break-even under convention b is not negative")
if any(min(num(r, "cost_low_end_bn"), num(r, "cost_high_end_bn")) <= 0 for r in gen):
    sys.exit("[BLOCKED] a generation does not cost others at an end")

# ---- conclusions on v5
CONCLUSIONS = [
    dict(
        id="C1", claim_tested="Other US residents pay about $355bn a year for the group's presence ($322–387bn)",
        status_on_v5="holds, restated",
        deciding_premise="none at the central; P02 alone breaks it, and so does P20 counted by ancestry share at its low end "
                         "[FRAMING-SENSITIVE]",
        reading_on_v5="$390.3–461.2bn, midpoint $425.8bn (+20.1% on $354.6bn); $9,129–10,789 per member of the 42.75M lineage. "
                      "[DATA: ladder 281]",
        premises="P01 frame; P02 one-year removal; P03 long-run service and property-tax responses; P04 capital return 2–3%; P05 pensions "
                 "on accrual at payable benefits; P06 defense/old interest at 0; P07 keys; P08 corrections; P09 imputed status; P10 "
                 "production; P20 the lineage count (3.04M added, whole). Measured: line amounts, keys' shares, C3. Assumed: P02–P06, "
                 "P10, the count's arm.",
        break_condition="Down a quarter (<$319.3bn): the first-year budget horizon alone, $289.1–335.3bn (−26.7%), or the lineage "
                        "counted by ancestry share at the stated bound's low end alone, $275.4–322.1bn (−29.8%) [FRAMING-SENSITIVE]. "
                        "With whole people inside the long-run frame, cash pensions plus one of the case's own alternatives: no capital "
                        "return, $270.2–321.6bn (−30.5%); roads and parks at CBO's first-year 0, $277.0–333.3bn (−28.3%); or schools "
                        "at 0.836, $279.3–356.8bn (−25.3%). Without cash pensions it takes four (e.g. no capital return + schools "
                        "0.836 + first-year roads and parks + care low, −26.5%). Counted by ancestry share at the population lane's "
                        "convention, one alternative suffices (no capital return −30.9%, cash pensions −34.2%). Up a quarter "
                        "(>$532.2bn): 7% capital + defense by GDP share (+34.7%), + scheduled benefits (+29.1%) or + property taxes at "
                        "zero (+27.6%); without 7% it takes three (scheduled benefits + defense + the largest long-run response, "
                        "+25.7%). [CALCULATION: engine_breaks_sept29.cjs --case oct05 → c1_arms_oct05.csv, c1_min_cuts_oct05.csv]",
        break_distance_note="The first-year horizon clears the cut by 1.7 points. Cash pensions alone −18.9% and 7% capital alone "
                            "+20.6%: each one alternative short. The lineage's own count moves it by under 3%: arms a / c −2.8% / "
                            "+2.8%, C3 ± 1 SE ∓0.8%, the replacement child −2.1% [FRAMING-SENSITIVE]; the ancestry-share count by "
                            "−17.5% to −29.8%. All 8 downward alternatives stacked −50.8% (−74.7% with the ancestry share); all 6 upward "
                            "+55.4% (+58.1% with arm c).",
        rival_reading="The removal cost is mostly a horizon, pricing and pension convention: in the first year budgets respond at "
                      "CBO's rates, levies stay fixed and existing capital earns no return, $289–335bn; counted on cash as well, "
                      "$206–258bn. And the count is a convention: by ancestry share the lineage is 29.9–35.1M people and costs "
                      "$275–376bn. [FRAMING-SENSITIVE]",
        discriminating_observation="Budgets after population outflows (2008–12 Mexican net return, 2020–21 enrollment falls, "
                                   "declining-enrollment districts): spending falling ~1:1 within 3–5 years favors the long-run case. "
                                   "The count: grandparents' and great-grandparents' birthplaces for third-plus members (70% have "
                                   "no grandparent data).",
        observed_yet="partly: inflow side only (within-district 0.836, 230; 2022–24 surge money 'about half, and late', 252); "
                     "identity loss measured to the third generation (280)",
        source="ladder 229, 230, 237–239, 252, 253, 257, 275, 280, 281; main_case_2026_10_05 main_case_bands.csv, components.csv; "
               "main_case_lineage_2026_10_05 v5_bands.csv, v5_summary.json; c1_arms_oct05.csv; c1_min_cuts_oct05.csv",
    ),
    dict(
        id="C2", claim_tested="Public services decide the sign: taxes cover benefits, but not schools and services",
        status_on_v5="BREAKS at the high end; holds at the low end",
        deciding_premise="P05: Social Security and Part A on accrual at payable benefits; P20: the added people's taxes exceed "
                         "their transfers",
        reading_on_v5="Direct taxes exceed benefits counted on accrual by $6.5bn at the low end and fall $4.4bn short at the high end. "
                      "The added people's own tally, +$9.9 / 8.2bn, lifts the union's −$3.4 / −12.6bn.",
        premises="P01; P03; P04; P05 accrual at payable benefits; P07; P08; P20. The tally (direct receipts less household "
                 "transfers, the accrual among the transfers) is +$6.5 / −4.4bn at ends 48 / 11: receipts $450.5 / 424.0bn, "
                 "transfers $444.0 / 428.4bn. [CALCULATION: c2_tally_oct05.csv]",
        break_condition="Clause 1 holds at the low end and fails at the high end, under arms a and c as well (+$4.6 / −5.3bn and "
                        "+$8.4 / −3.5bn). It holds on the cash set (+$89.4 / 73.4bn) and fails at both ends at scheduled benefits "
                        "(−$30.7 / −39.3bn); without the dataset corrections it holds at both (+$11.1 / 0.4bn). Clause 2: the service "
                        "break-even is −8.8% to −0.4% (personal) and −6.9% to +1.7% (shared) with the enterprise surplus at 1, and "
                        "−3.4% to +5.5% with it at s. A negative break-even means the group costs others at every service response "
                        "from 0 to 1. On the cash set it is 9.0–24.5%. [CALCULATION: c2_tally_oct05.csv, c2_break_even_oct05.csv]",
        break_distance_note="One tail decides each end [INFERENCE: additive, components.csv]. At the high end care's favorable tail "
                            "alone restores clause 1 (+$4.8bn); the tax block's falls $0.15bn short, and with any one more tax or "
                            "transfer tail it restores it (+$1.0bn or more). At the low end the MCBS 65+ bound on medical alone breaks "
                            "it (−$2.0bn); the tax block's adverse tail leaves +$0.9bn. Clause 2 survives only at the least adverse end "
                            "(below a 1.7% response with the enterprise surplus at 1, 3.4–5.5% at s).",
        rival_reading="Counted as 2024 cash flows, the group's taxes exceed its benefits by $73–89bn and services decide the sign "
                      "(break-even 9–25%): payroll taxes are this year's receipts, and the benefits they earn are paid from later "
                      "budgets. [FRAMING-SENSITIVE]",
        discriminating_observation="Mostly values (2024 cash flows vs benefits earned). The fact inside it: the money's worth of the "
                                   "group's payroll taxes (net OASDI 0.974 and the Part A accrual are national ratios); the group's "
                                   "own earnings histories and mortality would move it.",
        observed_yet="no (national ratios only)",
        source="c2_tally_oct05.csv; c2_break_even_oct05.csv; ladder 239, 257, 275, 281; decisions/2026-09-29-main-case-v4.md, "
               "2026-10-05-main-case-v5.md; main_case_2026_10_05/derived/sign_reversal.csv; main_case_lineage_2026_10_05 "
               "lineage_lines.csv",
    ),
    dict(
        id="C3", claim_tested="Checks against records move taxes and spending by about $50bn each (44–57), and the two almost "
                              "cancel (net about $11bn)",
        status_on_v5="holds",
        deciding_premise="P08",
        reading_on_v5="As on v4: taxes +$44.43 / 45.84bn, spending −$55.16 / 57.15bn, net −$10.73 / 11.31bn; $10.66 / 11.47bn of the "
                      "spending move is the accrual following the corrected OASDI receipts. The added people's amounts are held.",
        premises="P08 (measured: T-MSIS LTSS 210, pooled MEPS 206, admin benefit keys 217, ASEC fill-in DiD 208; assumed: on-books "
                 "share 0.526 for flagged Mexico-born, 254); P09 imputed status flags; P07 CBO gradients (216); P01; P05: the accrual "
                 "is computed on the corrected OASDI receipts and replaces current Social Security and Part A benefits.",
        break_condition="On v5, with the union's pension switch rebuilt on each set of corrections and the lineage's edits held in "
                        "every run: taxes +$44.43 / 45.84bn and spending −$55.16 / 57.15bn, net −$10.73 / 11.31bn, no interaction, "
                        "within $0.01bn of v4's. The spending move is the spending checks' −$44.50 / 45.68bn plus the accrual's fall "
                        "with the corrected OASDI receipts (−$10.95 / 11.78bn), −$10.66 / 11.47bn; $10.79 / 11.23bn of Social "
                        "Security and Part A benefit corrections drop out. By the edits' side, the receipt checks move the cost +$33.77 "
                        "/ 34.37bn and the spending checks −$44.50 / 45.68bn. With every increment held instead: +$44.43 / 45.84bn and "
                        "−$55.29 / 56.91bn, net −$10.86 / 11.07bn. [CALCULATION: c3_correction_split_oct05.csv] 'Net about $11bn' "
                        "moves >25% on any one of six data-component tails (five at the low end). 'Almost cancel' (the net under half "
                        "the smaller side, $22.2 / 22.9bn) fails with two tails, care low + tax block low, −$25.4 / 24.8bn; by the "
                        "edits' side (half $16.9 / 17.2bn) care low alone does it, −$19.9 / 20.5bn [INFERENCE: additive, "
                        "components.csv].",
        break_distance_note="Net: 1 tail. Cancellation: 2 tails by the lines that move (1 by the edits' side). [GAP: the added "
                            "G3+ members are priced on the corrected G3+ model, so their amounts carry G3+'s corrections; holding "
                            "them leaves those out of the split.]",
        rival_reading="The tax side is a model, not a record: it scales imputed-unauthorized pay to an assumed on-books share "
                      "($64.8bn of $136.8bn of wages off the books, 254), so two assumed adjustments of similar size may cancel.",
        discriminating_observation="SSA Earnings Suspense File and ITIN filer counts by state, 2022–24, to measure the on-books "
                                   "share (no 2022–25 measurement exists).",
        observed_yet="spending side yes (210, 255, 256); tax side partly (249 tests IRS national bins; the group's share per bin stays the CPS's)",
        source="c3_correction_split_oct05.csv; main_case_2026_10_05 components.csv; ladder 206, 208, 210, 216, 217, 249, 254–257",
    ),
    dict(
        id="C4", claim_tested="Costs outside the public budget add about $100bn a year",
        status_on_v5="holds",
        deciding_premise="none at the central",
        reading_on_v5="The social rows rise to $104.8 / 109.4bn: the added people's own rows, $8.6 / 8.8bn, priced at their share of "
                      "each row's key. The pairing rises with the fiscal case to $490.2–570.7bn, $11,466–13,349 per member of the "
                      "42.75M; its low end is on the Hispanic footing's fiscal case. [DATA: sept24_propagation oct05]",
        premises="Inherits C1's premises. Plus P12 VSL and dose-response (PM2.5 at $13.7m VSL; Miller victim prices), P13 "
                 "crash-volume elasticity (266), P19 offender shares (202), P20 for the added people's rows. Measured: CCRS fault "
                 "odds (264), NIBRS shares.",
        break_condition="The add (a quarter ≈ $26.8bn) breaks on any one item at its published range end, as on v4: PM2.5 "
                        "−$38.2 / +52.8bn, crashes −$68.7 / +63.3bn, scale net ∓$70.5bn (each priced on the 39.71M; the added "
                        "people's rows held). The pairing (<$397.8bn or >$663.1bn) needs two: crash low + scale low (−26.2%) or "
                        "crash high + scale high (+25.2%); PM2.5 high + crash high reaches +21.9%. [INFERENCE: additive, "
                        "real_costs_totals.csv §7 item ranges on the published basis]",
        break_distance_note="Add: 1 item. Pairing: 2 items. The first-year horizon does not break the pairing: about −21.4% with the "
                            "social rows held [INFERENCE]. The cash set pairs to $407.3–492.8bn (−15.2%).",
        rival_reading="Against as many average residents the group is cleaner (PM2.5 −$46.5bn) and no worse on crashes "
                      "(+$0.6bn): most of the add is the cost of any 39.7M people. [FRAMING-SENSITIVE: absolute vs normalized]",
        discriminating_observation="Values for absolute vs normalized. Fact: the crash sign turns on the crash-volume elasticity; "
                                   "a within-network panel of volumes × crashes in the group's counties (PeMS × CCRS) would "
                                   "narrow −58 to +74.",
        observed_yet="partly: transferable elasticities (266), CCRS fault odds (264); no local volume panel",
        source="ladder 189, 195, 202, 258, 260, 264–266, 274, 281; sept24_propagation_2026_09_24/derived/oct05/real_costs_totals.csv",
    ),
    dict(
        id="C5", claim_tested="State and local taxpayers pay most of the cost (85%), and about one resident in six gains",
        status_on_v5="holds on 'most' (69%); 'one in six' not rerun here",
        deciding_premise="P05 sets the share: the accrual is federal",
        reading_on_v5="State and local taxpayers pay about 69% (68.8% / 68.2%); the accrual, $82.9 / 77.8bn, is all federal. On "
                      "the cash set 87.4% / 82.1%.",
        premises="P03 (schools at 1 are state-local); P05; P06; P10 wage nest σ=2; P11 incidence: state-local cost charged where "
                 "the group lives, tax-share financing, household pooling; P20. Measured: which budget pays each line; CPS persons.",
        break_condition="'Most' (>50%) survives defense by GDP share (59.6% / 60.4%), plus legacy interest $30.6 / 42.6bn (55.8% / "
                        "55.8%), plus scheduled benefits as well (51.8% / 52.5%); it fails with defense and old interest at average "
                        "cost (+$271bn federal: 40.6% / 43.0%). [CALCULATION: additive on debt_legacy_2026_09_23/derived/oct05/"
                        "federal_split_2024.csv, central convention; the $271bn is September 27's] 'One in six' is not rerun here: "
                        "the winners lane's oct05 run belongs to another lane [GAP]; on v4 it gave 17.9% (tax-share) and 17.1% (per "
                        "person) (858f77a).",
        break_distance_note="State-local share: 'most' needs the average-cost charge the repo rejects; with defense, legacy interest "
                            "and scheduled benefits it keeps 52%. Winners: one convention [INFERENCE: September 24 swings].",
        rival_reading="Who gains is not identified: winners are modeled channel totals assigned to survey people; halving wage "
                      "deviations moves them 23.9% → 10.3% at the same aggregate (audit §2).",
        discriminating_observation="Person-level wage effects by skill and region from linked employer–employee data (LEHD) "
                                   "against the nest's assigned gains. The defense/interest charge is a values choice.",
        observed_yet="no",
        source="ladder 194, 207, 226, 281; debt_legacy_2026_09_23/derived/oct05/federal_split_2024.csv, summary.json; "
               "research/immigration-weekly-conceptual-audit-2026-09-25.md §2",
    ),
    dict(
        id="C6", claim_tested="Each generation costs others, and progress stops after the second",
        status_on_v5="holds",
        deciding_premise="none at the central",
        reading_on_v5="Every generation costs others at both ends and under both conventions (at least $87.0bn); service "
                      "break-evens are at most 21.6%. G3+ carries the added people: $141.7 / 195.0bn under convention a (v4: $122.6 "
                      "/ 168.4bn).",
        premises="C1's premises, plus: CPS parental birthplace (self-reported for 54%), child convention (a/b), household "
                 "allocation, P15 self-ID, P16 cross-section as lineage (CPS 1994–2025; GSS), P20 (the added people on G3+).",
        break_condition="Clause 1: a generation turns into a net gain only below its service break-even: at most 16.9% under "
                        "convention a and 21.6% under b (G3+, shared), on the generation account's oct05 models [CALCULATION: "
                        "c6_generation_break_even_oct05.csv]. The added people raise G3+'s largest break-even by 3.5 / 3.2 points: "
                        "1.08M of them are priced as third-plus whites at G3+ ages. G1's are negative under b at every end and "
                        "allocation: a cost at any service response. On the cash set at most 38.3% (a) and 41.9% (b), every "
                        "generation at least $72.6bn. Clause 2: 0.86 of the BA+ gap carried G2→G3+ with C3 from the CPS basic "
                        "monthly frame (232, 280); a quarter (<0.645) needs the literature's G2→G3 transmission 0.46–0.53 (236) in "
                        "place of the CPS cross-section.",
        break_distance_note="Clause 1: far (at most 21.6% against at least 0.6 in every arm; 41.9% on cash). Clause 2: one source "
                            "swap.",
        rival_reading="Cross-sectional G3+ descends from earlier, less-selected stock, so G2 vs G3+ today is not parent→child; "
                      "matched by cohort, progress may continue. Partly answered: 0.83–0.87 in the 1979–85 cohort and at 25–44 (232).",
        discriminating_observation="Linked three-generation records tying G3 to G2 parents' schooling (restricted Census-linked "
                                   "data or PSID immigrant samples).",
        observed_yet="identity loss yes (280: 526 unique G3 non-identifiers at 25+, closing 0.57, SE 0.26); linkage no",
        source="ladder 224, 232, 236, 255, 280, 281; generation_account_2026_09_24/derived/generation_results_oct05.csv, "
               "generation_corrections_oct05.json and _cash; c6_generation_break_even_oct05.csv",
    ),
    dict(
        id="C7", claim_tested="Legal status explains little of the fiscal gap",
        status_on_v5="unchanged (no v5 input)",
        deciding_premise="",
        reading_on_v5="Carried by ladder 85 on 2024 cash flows; not recomputed with pensions on accrual [GAP]. The added people are "
                      "third-plus, with no status contrast.",
        premises="P09 imputed status (Borjas residual rules on ASEC 2025); P08 on-books share; P01. Carried by ladder 85: "
                 "unauthorized −7,806 vs legal −8,166 raw, −9,720 vs −8,234 per adult after ineligible transfers are zeroed "
                 "and taxes scaled on-books.",
        break_condition="'Little' fails if the status contrast reaches about half the gap (~$4.5k per adult) [INFERENCE: "
                        "threshold]; measured ~$1.5k (15%). Rule switches (Medicaid clause: 47% → 62% unauthorized among "
                        "low-educated parents, 185) reassign recipients but were not priced [GAP].",
        break_distance_note="Needs a ~3× larger contrast than measured; no priced arm reaches it. The weakness is identification "
                            "(status imputed from benefit receipt), not size.",
        rival_reading="Status acts through the children: minors with no legal parent are 12–14 points less often in college "
                      "at 18–24 (186), and G2 is the costliest generation, so an adult cross-section understates status's share.",
        discriminating_observation="Children's schooling around a status shock unrelated to schooling: DACA age cutoffs or IRCA "
                                   "timing, in ACS by parental arrival cohort.",
        observed_yet="no: CPS 2025 cross-section and IIMMLA only (186)",
        source="ladder 85, 185–187, 254; audit §4",
    ),
    dict(
        id="C8", claim_tested="Against as many whites, the group costs others about $320–405bn a year more, depending on which whites",
        status_on_v5="not rerun here (the comparators' oct05 run)",
        deciding_premise="P20 [INFERENCE]: the comparison's count",
        reading_on_v5="On v4 the white lane gave $351.2 / 350.5bn against US whites and $410.4 / 408.0bn against local whites "
                      "(6665297). On v5 the comparison needs the added people on both sides: either both at 42.75M, or the "
                      "identified 39.71M at v5's responses [GAP: the comparators' oct05 run belongs to another lane].",
        premises="Rough re-key of the case's rules (not an engine run); P14 third-plus non-Hispanic whites at national rates; P05 "
                 "by accrual; P07; P20: the CPS re-keys cannot see the 3.04M, who no longer report Mexican origin.",
        break_condition="On v4 inside the map's $320–405bn at its low end and $3–5bn above it at the high end (lead verification, "
                        "2026-09-29). An added person costs others $6,309–8,790, against $2,274–3,472 for a third-plus white at the "
                        "same ages, so putting both sides on 42.75M widens the gap [INFERENCE: direction only; the comparator prices "
                        "whites at national rates].",
        break_distance_note="Not measured on v5 here.",
        rival_reading="The gap is composition (schooling, age), not group-specific; against an all-residents slice the union is "
                      "$85–87bn above average (263).",
        discriminating_observation="Framing (which reference answers the question, and on which count). Fact left: the re-key on "
                                   "v5 with the added people on both sides.",
        observed_yet="partly (rough keys; v4 only)",
        source="ladder 259, 263, 274, 281; white_replacement_2026_09_28 (headline_sept29.csv)",
    ),
    dict(
        id="C9", claim_tested="Immigrants offend less, and their US-born sons are held at about twice the white rate",
        status_on_v5="unchanged (no v5 input)",
        deciding_premise="",
        reading_on_v5="No fiscal input; v5 changes nothing here.",
        premises="P18 Texas DPS felony charges 2012–18 with DHS-matched status; Pew/CMS denominators; P17 ACS institutional "
                 "counts 2010–2024 with the prison-coding fix; P15 self-ID; P19 NIBRS TX/AZ offender ethnicity.",
        break_condition="Clause 1: undocumented at 0.40–0.43 of US-born (cost-weighted per capita; 0.31–0.33 per adult) flip "
                        "only with a 2.3–3.2× undercount; the pooled foreign-born (0.63–0.79) with 1.3–2.1×; legal "
                        "non-naturalized already exceed 1 on cost weights (1.20; sexual assault 2.54) (144). Clause 2: 1.7–1.9 "
                        "raw, 2.1–2.3 coded (65); a quarter (<1.5 or >2.5) needs 2010's 2.56.",
        break_distance_note="Clause 1: undercount size unmeasured [GAP]; the DHS-match boundary is the weak point. Clause 2: "
                            "stable over 2019–2024; the coding fix alone +15–20%; the 2023 race redesign −3%.",
        rival_reading="Clause 1: removal and DHS-record matching take immigrant offenders out of the records. Clause 2: custody "
                      "carries sentencing and detention as well as offending; NCVS victims perceive Hispanic non-fatal "
                      "offending at 0.94× white (202).",
        discriminating_observation="Clause 1: arrests with birthplace recorded at booking independently of DHS records (county "
                                   "jail files). Clause 2: police-recorded offending, NIBRS TX/AZ 1.74–4.22× white by offence.",
        observed_yet="clause 2 yes (202, pooled Hispanic, all generations); clause 1 no",
        source="ladder 65, 66, 70, 82, 144, 196, 202",
    ),
]
armb = json.load(open(LINEAGE / "v5_summary.json"))["sets"]["set"]["arms"]["b"]
for k, want in [("added_per_person_usd", (6309, 8790)), ("white_person_usd", (2274, 3472))]:
    for j, w in enumerate(want):
        check(f"C8 {k} {j}", armb[k][j], w, tol=0.5)

# ---- premises on v5: kind, flags for C1..C9, and for the top five and P20 the best-supported alternative and its effect
C = [f"C{i}" for i in range(1, 10)]
PREMISES = [
    ("P01", "Survey frame: CPS ASEC / ACS Mexican-origin self-ID and parental birthplace, 39.71M identified in three generations",
     "measured (survey)", "C1 C2 C3 C4 C5 C6 C7 C8 C9"),
    ("P02", "Removal counterfactual over one income year (2024), people alive in 2024, no lifetime", "convention", "C1 C2 C3 C4 C5 C6 C7 C8"),
    ("P03", "Service budgets and property-tax levies respond at long-run rates (schools 1, general government 0.60–0.85, roads/parks "
            "long run, property taxes at the receipt-side lane's central)", "assumed (cross-section slopes)", "C1 C2 C4 C5 C6 C8"),
    ("P04", "Return on public capital at 2–3%", "convention", "C1 C2 C4 C5 C6"),
    ("P05", "Social Security and Medicare Part A on accrual at payable benefits, net of the income tax on benefits (v4's and v5's central)",
     "convention", "C1 C2 C4 C5 C6 C8"),
    ("P06", "Defense and existing interest at zero response", "assumed", "C1 C4 C5"),
    ("P07", "Allocation keys: CBO incidence, the IRS-matched income-tax key, use keys for justice and care, state price levels, "
            "roads by vehicle miles", "convention + measured shares", "C1 C2 C3 C4 C6 C8"),
    ("P08", "Dataset corrections, including an on-books share of 0.526 for flagged Mexico-born workers", "measured in part; on-books share assumed",
     "C1 C2 C3 C4 C6 C7 C8"),
    ("P09", "Legal status imputed by residual rules (benefit receipt defines some legal)", "imputed", "C1 C2 C3 C4 C7"),
    ("P10", "Production nest: two skill groups, σ 2, ε infinite, capital adjusts", "assumed (calibrated)", "C1 C4 C5 C6"),
    ("P11", "Incidence among residents: where the state-local cost falls, financing rule, household pooling", "convention", "C5"),
    ("P12", "Harm prices: VSL $13.7m, PM2.5 dose-response, Miller victim prices", "assumed (published)", "C4"),
    ("P13", "Crash-volume elasticity transferred from other networks", "assumed (published)", "C4"),
    ("P14", "Reference group: third-plus non-Hispanic whites at national rates", "convention", "C6 C8 C9"),
    ("P15", "Ethnic self-identification keeps descendants in the group", "measured in part (232, 280)", "C6 C9"),
    ("P16", "Cross-sectional generations stand in for lineages", "assumed", "C6 C9"),
    ("P17", "ACS institutional counts identify custody by nativity and ethnicity", "measured, coding errors", "C9"),
    ("P18", "Texas arrest status from DHS record matches", "administrative", "C9"),
    ("P19", "Police-recorded offender ethnicity (NIBRS TX/AZ, SHR; arrests for use keys)", "measured", "C1 C4 C9"),
    ("P20", "The lineage count: 3.04M descendants who no longer report Mexican origin (arm b, C3 0.557), counted as whole people "
            "and priced at the identified G3+'s ages", "modeled count (identity loss measured to G3) + convention (whole people)",
     "C1 C2 C4 C5 C6 C8"),
]
SWAP = {
    "P01": ("ACS level for the Mexico-born (CPS +9–13%, 209); NVSS births for the G2/G3 split (255)",
            "Not rerun on v5. On September 27: C1 −$2.2–2.5bn (−0.7%) [DATA: 209]; C2 ≈0 (removed people pay about what they "
            "cost, 209); C6 moves young children from G3+ to G2 [GAP]; C7 imputed unauthorized 4.57M → ~4.07M [GAP]; the rest "
            "< 1% [INFERENCE]. Breaks none [INFERENCE: v5's items and the lineage do not change the frame's weights]."),
    "P02": ("First-year budget horizon (ladder 229), with property levies fixed and roads keyed on resources",
            "C1 −26.7% BREAK ($289.1–335.3bn) [CALCULATION: c1_arms_oct05.csv]; C4 pairing about −21%, holds [INFERENCE: social "
            "rows held]; C2's tally has no services in it; C5, C6 and C8 not rerun on v5 [GAP]. Breaks one."),
    "P05": ("Cash, the September 27 convention (decision 2026-09-29, alternative 2)",
            "Restores C2: tally +$89.4 / 73.4bn, break-even 9.0–24.5% [CALCULATION: c2_tally_oct05.csv, c2_break_even_oct05.csv]. "
            "C1 −18.9% ($307.4–383.4bn), a break with no capital return (−30.5%), first-year roads and parks (−28.3%) or schools "
            "at 0.836 (−25.3%) [CALCULATION: c1_min_cuts_oct05.csv]; C4 pairing $407.3–492.8bn (−15.2%) [DATA: sept24_propagation "
            "oct05]; C5 state-local share 69% → 82–87% [CALCULATION: debt lane split]; C6 every generation still costs others (at "
            "least $72.6bn; break-evens at most 41.9%) [CALCULATION]; C8 not rerun [GAP]. Breaks none. Scheduled benefits "
            "instead: C1 +8.5%, C2 tally −$30.7 / −39.3bn, C5 about 63%."),
    "P08": ("No corrections (v4's items and the lineage on the uncorrected model, the union's pension switch rebuilt)",
            "C1 +2.6% ($401.0–472.6bn) [CALCULATION: c3_correction_split_oct05.csv]; C2 tally +$11.1 / 0.4bn, clause 1 holds at "
            "both ends [CALCULATION: c2_tally_oct05.csv]; C3 is this premise; C6 not split by generation [GAP]; C7 raw vs "
            "adjusted contrast changes direction (85). Breaks none."),
    "P03": ("Schools at the within-district 0.836 (the only within-unit estimate)",
            "C1 −6.4% ($362.3–434.6bn) [CALCULATION: c1_arms_oct05.csv]; property taxes at zero instead +7.1%; C2's tally has no "
            "services in it; C4 pairing about −5% [INFERENCE: social rows held]; C6 holds [INFERENCE]; C8 not rerun [GAP]. "
            "Breaks none."),
    "P20": ("The count's arms a and c (1.81M or 4.27M added); as a framing, the ancestry-share count (29.9–35.1M people)",
            "Arms a / c: C1 −2.8% / +2.8%, C2's split by end holds (+$4.6 / −5.3bn and +$8.4 / −3.5bn) [CALCULATION: "
            "c1_arms_oct05.csv, c2_tally_oct05.csv]; C3 ± 1 SE ∓0.8% and the replacement child −2.1% [FRAMING-SENSITIVE]. "
            "Breaks none. By ancestry share: C1 −17.5% to −29.8%, a break at the stated bound's low end [FRAMING-SENSITIVE]; "
            "the per-member cost barely moves ($9,211–10,774 at the low end against $9,129–10,789). Breaks one, under that "
            "count only."),
}
for arm, lo, hi in [("school_within_district", 362.27, 434.65), ("pension_cash", 307.38, 383.41)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo, tol=0.005)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi, tol=0.005)
base = [num(split[("pension_rebuilt", e)], "v4_items_only_bn") for e in ENDS]
check("P08 swap low", base[0], 401.02, tol=0.005)
check("P08 swap high", base[1], 472.55, tol=0.005)
check("P08 swap move", 100 * (sum(base) / 2 / mid - 1), 2.6)
school_pair = [num(arms["school_within_district"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]) + social[0],
               num(arms["school_within_district"], "cost_high_bn") + social[1]]
check("P03 swap pairing", 100 * (sum(school_pair) / 2 / pmid - 1), -5.0, tol=0.5)
frac = next(r for r in json.load(open(LINEAGE / "v5_summary.json"))["fractional"]["rows"]
            if r["set"] == "set" and r["arm"] == "b" and r["scenario"] == "g4_at_nothing")
check("P20 ancestry-share per member low", frac["per_member_low_usd"], 9211, tol=0.5)
check("P20 ancestry-share per member high", frac["per_member_high_usd"], 10774, tol=0.5)
fr_pop = [r["fractional_population"] / 1e6 for r in json.load(open(LINEAGE / "v5_summary.json"))["fractional"]["rows"]
          if r["set"] == "set" and r["arm"] == "b" and r["scenario"] in ("g4_at_nothing", "g4_at_bound")]
check("P20 ancestry-share population low", min(fr_pop), 29.9)
check("P20 ancestry-share population high", max(fr_pop), 35.1)
added_people = next(r for r in rows(LINEAGE / "v5_bands.csv") if r["set"] == "set" and r["arm"] == "b" and r["variant"] == "central")
check("added people", (num(added_people, "m_g3plus") + num(added_people, "m_white")) / 1e6, 3.04, tol=0.005)
check("added people priced as whites", num(added_people, "m_white") / 1e6, 1.08, tol=0.005)

by_premise = []
for pid, text, kind, flags in PREMISES:
    fl = set(flags.split())
    by_premise.append((pid, text, kind, [1 if c in fl else 0 for c in C]))
order = sorted(by_premise, key=lambda r: (-sum(r[3]), r[0]))
rank = {r[0]: i + 1 for i, r in enumerate(order)}
top = [r[0] for r in order[:5]]
if not set(top) <= set(SWAP) or set(SWAP) - set(top) != {"P20"}:
    sys.exit(f"[BLOCKED] top five premises are {top}; SWAP covers {sorted(SWAP)} (the top five and P20)")

D.mkdir(exist_ok=True)
with open(D / "conclusions_oct05.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    keys = ["id", "claim_tested", "status_on_v5", "deciding_premise", "reading_on_v5", "premises", "break_condition",
            "break_distance_note", "rival_reading", "discriminating_observation", "observed_yet", "source"]
    w.writerow(keys)
    for c in CONCLUSIONS:
        w.writerow([c[k] for k in keys])
with open(D / "common_mode_oct05.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["premise_id", "premise", "kind", *C, "n_conclusions", "rank", "best_supported_alternative", "effect_if_swapped"])
    for pid, text, kind, flags in order:
        alt, eff = SWAP.get(pid, ("", ""))
        w.writerow([pid, text, kind, *flags, sum(flags), rank[pid], alt, eff])
broken = [c["id"] for c in CONCLUSIONS if c["status_on_v5"].startswith("BREAKS")]
print(f"  ✓ conclusions_oct05.csv: {len(CONCLUSIONS)} rows, broken at the central: {', '.join(broken)}; "
      f"common_mode_oct05.csv: {len(PREMISES)} premises; top five {', '.join(top)}")

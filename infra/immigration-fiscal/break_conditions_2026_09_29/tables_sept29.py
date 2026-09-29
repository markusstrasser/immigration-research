"""Write derived/conclusions_sept29.csv and derived/common_mode_sept29.csv: the nine conclusions on the v4 case.

The v4 case is main_case_2026_09_29 (adopted 2026-09-29, key sept29). Each row tests the evidence map's claim as it
stands in overview_2026_09_28/groups.py (still on the September 27 case) against v4. The text cells are this lane's
reading of engine_breaks_sept29.cjs's outputs and of the cited lanes' sept29 files. Every number quoted from them is
recomputed here first, so a changed input stops the build instead of leaving stale text. tables.py's September 27 files
(conclusions.csv, common_mode.csv) are not touched. Run after `node engine_breaks_sept29.cjs`:
    uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_sept29.py
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

# ---- C1: arms and minimal cuts
arms = {r["arm"]: r for r in rows(D / "c1_arms_sept29.csv")}
cuts = {(r["direction"], r["set"]): r for r in rows(D / "c1_min_cuts_sept29.csv")}
check("case low", num(arms["adopted"], "cost_low_bn"), 371.41)
check("case high", num(arms["adopted"], "cost_high_bn"), 434.84)
mid = num(arms["adopted"], "midpoint_bn")
check("midpoint", mid, 403.13)
check("down cut", 0.75 * mid, 302.35)
check("up cut", 1.25 * mid, 503.91)
for arm, lo, hi, move in [("first_year_horizon", 277.31, 318.35, -26.1), ("first_year_horizon_cash", 200.59, 245.32, -44.7)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi)
    check(f"{arm} move", num(arms[arm], "move_pct_of_midpoint"), move)
for arm, move in [("pension_cash", -18.6), ("capital_7pct", 20.1), ("property_none", 6.7), ("school_within_district", -6.2),
                  ("pension_scheduled", 8.3)]:
    check(f"{arm} alone", num(arms[arm], "move_pct_of_midpoint"), move)
for key, lo, hi, move in [(("down", "capital_off+pension_cash"), 260.28, 304.65, -29.9),
                          (("down", "roads_parks_first_year+pension_cash"), 266.64, 315.49, -27.8)]:
    check(f"{key} low", num(cuts[key], "cost_low_bn"), lo)
    check(f"{key} high", num(cuts[key], "cost_high_bn"), hi)
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move)
for key, move in [(("down", "capital_off+school_within_district+roads_parks_first_year+care_low"), -26.0),
                  (("up", "capital_7pct+defense_gdp_share"), 35.0), (("up", "capital_7pct+pension_scheduled"), 28.4),
                  (("up", "capital_7pct+property_none"), 26.9), (("up", "pension_scheduled+defense_gdp_share+medical_mcbs65"), 25.2)]:
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move, tol=0.06)
minimal = [r for r in cuts.values() if r["minimal"] == "yes"]
size = lambda r: int(float(r["size"]))
if min(size(r) for r in minimal if r["direction"] == "down") != 2:
    sys.exit("[BLOCKED] the smallest downward cut is not 2; the text says 2")
if min(size(r) for r in minimal if r["direction"] == "down" and "pension_cash" not in r["set"].split("+")) != 4:
    sys.exit("[BLOCKED] without cash pensions the smallest downward cut is not 4")
if any("pension_cash" not in r["set"].split("+") for r in minimal if r["direction"] == "down" and size(r) == 2):
    sys.exit("[BLOCKED] a 2-set downward cut without cash pensions exists")
if min(size(r) for r in minimal if r["direction"] == "up") != 2:
    sys.exit("[BLOCKED] the smallest upward cut is not 2")
if min(size(r) for r in minimal if r["direction"] == "up" and "capital_7pct" not in r["set"].split("+")) != 3:
    sys.exit("[BLOCKED] without 7% capital the smallest upward cut is not 3")
stacks = {r["direction"]: r for r in cuts.values() if r["minimal"] == "stack"}
check("down stack", num(stacks["down"], "move_pct_of_midpoint"), -49.9)
check("up stack", num(stacks["up"], "move_pct_of_midpoint"), 55.2)
if (size(stacks["down"]), size(stacks["up"])) != (8, 6):
    sys.exit("[BLOCKED] the stacks are not 8 downward and 6 upward alternatives")

# ---- C2: tally and break-evens
tally = {(r["model"], r["end"]): r for r in rows(D / "c2_tally_sept29.csv")}
for model, col, want in [("case_accrual", "tally_bn", (-3.4, -12.6)), ("case_accrual", "direct_receipts_bn", (408.4, 386.7)),
                         ("case_accrual", "household_transfers_bn", (411.8, 399.3)), ("case_accrual", "tally_at_scheduled_bn", (-37.6, -45.0)),
                         ("cash_set", "tally_bn", (73.3, 60.4)), ("v4_items_without_dataset_corrections", "tally_bn", (1.2, -7.8))]:
    for end, w in zip(ENDS, want):
        # 399.35 prints as 399.3 (controlled rounding: 386.7 - 399.3 = -12.6, the printed tally)
        check(f"C2 {model} {col} {end}", num(tally[(model, end)], col), w, tol=0.06 if col == "household_transfers_bn" else 0.05)
be = {(r["case"], r["variant"], r["allocation"]): r for r in rows(D / "c2_break_even_sept29.csv")}
for key, most, least in [(("case_accrual", "enterprises_at_1", "personal"), -11.0, -2.4), (("case_accrual", "enterprises_at_1", "shared"), -9.3, -0.6)]:
    check(f"{key} most", 100 * num(be[key], "break_even_most_adverse"), most)
    check(f"{key} least", 100 * num(be[key], "break_even_least_adverse"), least)
at_s = [100 * num(r, k) for (c, v, _), r in be.items() if c == "case_accrual" and v == "enterprises_at_s" for k in r if k.startswith("break_even")]
check("case at s, lowest", min(at_s), -5.5)
check("case at s, highest", max(at_s), 3.3)
least_at_s = [100 * num(be[("case_accrual", "enterprises_at_s", a)], "break_even_least_adverse") for a in ["personal", "shared"]]
check("case at s, least adverse, personal", least_at_s[0], 1.5)
cash_be = [100 * num(r, k) for (c, _, _), r in be.items() if c == "cash_set" for k in r if k.startswith("break_even")]
check("cash set break-even, lowest", min(cash_be), 7.0)
check("cash set break-even, highest", max(cash_be), 22.2)
# Clause 1's distance: the tax and transfer tails of components.csv at their favorable (low-cost) ends, additive.
comp = {r["component"]: r for r in rows(F / "main_case_2026_09_29/derived/components.csv")}
LO = {"low_end_48": "range_dev_low_end_lo", "high_end_11": "range_dev_high_end_lo"}
HI = {"low_end_48": "range_dev_low_end_hi", "high_end_11": "range_dev_high_end_hi"}
TAX_TRANSFER_TAILS = ["tax_block", "income_tax", "medical", "ltss", "benefits", "care"]
t0 = {e: num(tally[("case_accrual", e)], "tally_bn") for e in ENDS}
check("tally, low end, tax block's favorable tail", t0["low_end_48"] - num(comp["tax_block"], LO["low_end_48"]), 2.1)
if t0["high_end_11"] - num(comp["tax_block"], LO["high_end_11"]) >= 0:
    sys.exit("[BLOCKED] the tax block alone restores clause 1 at the high end; the text says it needs all six")
check("tally, high end, all six favorable tails", t0["high_end_11"] - sum(num(comp[k], LO["high_end_11"]) for k in TAX_TRANSFER_TAILS), 6.9)

# ---- C3: the corrections by side
split = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_sept29.csv")}
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
# Tails: the data components of components.csv (not the response, capital and v4-item rows).
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

# ---- C4: the social rows and the pairing (sept24_propagation's sept29 run)
rc = {(r["column"], r["item"]): r["sept29"] for r in rows(F / "sept24_propagation_2026_09_24/derived/sept29/real_costs_totals.csv")}
pair = [float(rc[("pairing_on_priced_count", f"published pairing ({e})")]) for e in ("low", "high")]
footing = [float(rc[("hispanic", "fiscal main case (low)")]), float(rc[("custody", "fiscal main case (high)")])]
social = [p - f for p, f in zip(pair, footing)]
check("pairing low", pair[0], 462.95)
check("pairing high", pair[1], 535.52)
check("social rows low", social[0], 96.26)
check("social rows high", social[1], 100.68)
pmid = sum(pair) / 2
dev = {}
for item in ["pm25_consumption", "road_crash_externality", "scale_net_earnings"]:
    c = float(rc[(f"social_item_{item}", "central, both ends")])
    dev[item] = (float(rc[(f"social_item_{item}", "low, full span")]) - c, float(rc[(f"social_item_{item}", "high, full span")]) - c)
for item, lo, hi in [("pm25_consumption", -38.2, 52.8), ("road_crash_externality", -68.7, 63.3), ("scale_net_earnings", -70.5, 70.5)]:
    check(f"{item} low deviation", dev[item][0], lo)
    check(f"{item} high deviation", dev[item][1], hi)
    if min(abs(dev[item][0]), abs(dev[item][1])) < 0.25 * sum(social) / 2:
        sys.exit(f"[BLOCKED] {item} at a range end does not move the add by a quarter")
check("pairing: crash low + scale low", 100 * (dev["road_crash_externality"][0] + dev["scale_net_earnings"][0]) / pmid, -27.9)
check("pairing: crash high + scale high", 100 * (dev["road_crash_externality"][1] + dev["scale_net_earnings"][1]) / pmid, 26.8)
check("pairing: PM2.5 high + crash high", 100 * (dev["pm25_consumption"][1] + dev["road_crash_externality"][1]) / pmid, 23.3)
if any(abs(dev[a][k] + dev[b][k]) / pmid > 0.25 for a, b in itertools.combinations(dev, 2) for k in (0, 1)
       if {a, b} != {"road_crash_externality", "scale_net_earnings"}):
    sys.exit("[BLOCKED] another pair of items breaks the pairing")
fy = [num(arms["first_year_horizon"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]), num(arms["first_year_horizon"], "cost_high_bn")]
check("pairing at the first-year horizon, social rows held", 100 * ((fy[0] + social[0] + fy[1] + social[1]) / 2 / pmid - 1), -21.1)
cash_pair = [float(rc[("pairing_on_priced_count_cash_set", f"published pairing ({e})")]) for e in ("low", "high")]
check("cash-set pairing low", cash_pair[0], 386.23)
check("cash-set pairing high", cash_pair[1], 462.49)
check("cash-set pairing move", 100 * (sum(cash_pair) / 2 / pmid - 1), -15.0)

# ---- C5: the state-local share (debt_legacy's sept29 split, central convention, main profile)
split5 = {r["end"]: r for r in rows(F / "debt_legacy_2026_09_23/derived/sept29/federal_split_2024.csv")
          if r["profile"] == "long_run_non_school_full" and r["convention"] == "central"}
COLS = ["fiscal_gap_bn", "resource_cost_bn", "displaced_bn", "accrual_bn"]
FED = ["federal_bn", "resource_cost_federal_bn", "displaced_federal_bn", "accrual_federal_bn"]
with open(F / "debt_legacy_2026_09_23/derived/sept29/summary.json") as f:
    headline = json.load(f)["case"]["v4"]["headline_2024"]
LEGACY = {e: headline[e]["legacy_interest_2024_bn"] for e in ("low", "high")}
check("legacy interest low", LEGACY["low"], 30.8)
check("legacy interest high", LEGACY["high"], 41.5)
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
for key, want in [("case", (67.9, 67.5)), ("cash", (85.7, 81.2)), ("scheduled", (62.2, 62.8)), ("defense", (58.5, 59.3)),
                  ("defense_interest", (54.6, 54.7)), ("defense_interest_scheduled", (50.8, 51.6)), ("average_cost", (39.2, 41.6))]:
    for e, w in zip(("low", "high"), want):
        check(f"C5 state-local share {key} {e}", 100 * share[e][key], w)
check("accrual low", num(split5["low"], "accrual_bn"), 76.7)
check("accrual high", num(split5["high"], "accrual_bn"), 73.0)

# ---- C6: generations on the corrected v4 generation models
gen = rows(D / "c6_generation_break_even_sept29.csv")
bmax = lambda case, conv=None: 100 * max(num(r, k) for r in gen if r["case"] == case and (conv is None or r["convention"] == conv)
                                         for k in r if k.startswith("break_even"))
for case, conv, want in [("case_accrual", "a", 13.3), ("case_accrual", "b", 18.5), ("cash_set", "a", 35.1), ("cash_set", "b", 39.1)]:
    check(f"C6 largest break-even {case} {conv}", bmax(case, conv), want)
cmin = lambda case: min(min(num(r, "cost_low_end_bn"), num(r, "cost_high_end_bn")) for r in gen if r["case"] == case)
check("C6 smallest generation cost, case", cmin("case_accrual"), 87.1)
check("C6 smallest generation cost, cash set", cmin("cash_set"), 66.8)
if any(num(r, k) >= 0 for r in gen if r["case"] == "case_accrual" and r["convention"] == "b" and r["generation"] == "G1"
       for k in r if k.startswith("break_even")):
    sys.exit("[BLOCKED] a G1 break-even under convention b is not negative")

# ---- conclusions on v4
CONCLUSIONS = [
    dict(
        id="C1", claim_tested="Other US residents pay about $355bn a year for the group's presence ($322–387bn)",
        status_on_v4="holds, restated",
        deciding_premise="none at the central; P02 alone breaks it",
        reading_on_v4="$371.4–434.8bn, midpoint $403.1bn (+13.7% on $354.6bn). [DATA: ladder 275]",
        premises="P01 frame; P02 one-year removal; P03 long-run service and property-tax responses; P04 capital return 2–3%; P05 pensions "
                 "on accrual at payable benefits; P06 defense/old interest at 0; P07 keys; P08 corrections; P09 imputed status; P10 "
                 "production. Measured: line amounts, keys' shares. Assumed: P02–P06, P10.",
        break_condition="Down a quarter (<$302.3bn): the first-year budget horizon alone, $277.3–318.3bn (−26.1%): CBO's first-year "
                        "school response; roads, parks, property taxes, rental assistance and the enterprise surplus at zero response; "
                        "no capital return; roads keyed on resources. Inside the long-run frame, two of the case's own alternatives: "
                        "cash pensions + no capital return, $260.3–304.6bn (−29.9%), or cash pensions + roads and parks at CBO's "
                        "first-year 0, $266.6–315.5bn (−27.8%). Without cash pensions it takes four (e.g. no capital return + schools "
                        "0.836 + first-year roads and parks + care low, −26.0%). Up a quarter (>$503.9bn): 7% capital + defense by GDP "
                        "share (+35.0%), + scheduled benefits (+28.4%) or + property taxes at zero (+26.9%); without 7% it takes three "
                        "(scheduled benefits + defense + the MCBS 65+ bound, +25.2%). [CALCULATION: engine_breaks_sept29.cjs → "
                        "c1_arms_sept29.csv, c1_min_cuts_sept29.csv]",
        break_distance_note="The first-year horizon clears the cut by 1.1 points. Cash pensions alone −18.6% and 7% capital alone "
                            "+20.1%: each one alternative short. All 8 downward alternatives stacked −49.9%; all 6 upward +55.2%.",
        rival_reading="The removal cost is mostly a horizon, pricing and pension convention: in the first year budgets respond at "
                      "CBO's rates, levies stay fixed and existing capital earns no return, $277–318bn; counted on cash as well, "
                      "$201–245bn. [FRAMING-SENSITIVE]",
        discriminating_observation="Budgets after population outflows (2008–12 Mexican net return, 2020–21 enrollment falls, "
                                   "declining-enrollment districts): spending falling ~1:1 within 3–5 years favors the long-run case.",
        observed_yet="partly: inflow side only (within-district 0.836, 230; 2022–24 surge money 'about half, and late', 252)",
        source="ladder 229, 230, 237–239, 252, 253, 257, 275; main_case_2026_09_29 main_case_bands.csv, components.csv; "
               "c1_arms_sept29.csv; c1_min_cuts_sept29.csv",
    ),
    dict(
        id="C2", claim_tested="Public services decide the sign: taxes cover benefits, but not schools and services",
        status_on_v4="BREAKS at the central",
        deciding_premise="P05: Social Security and Part A on accrual at payable benefits, v4's central",
        reading_on_v4="Benefits counted on accrual exceed direct taxes by $3.4 / 12.6bn, and at the most adverse end the group costs "
                      "others before any service budget responds.",
        premises="P01; P03; P04; P05 accrual at payable benefits; P07; P08. The tally (direct receipts less household transfers, the "
                 "accrual among the transfers) is −$3.4 / −12.6bn at ends 48 / 11: receipts $408.4 / 386.7bn, transfers $411.8 / "
                 "399.3bn (controlled rounding, so the printed parts add). [CALCULATION: c2_tally_sept29.csv]",
        break_condition="Clause 1 fails on the central. It holds on the cash set (+$73.3 / 60.4bn) and fails further at scheduled "
                        "benefits (−$37.6 / −45.0bn); without the dataset corrections it splits by end (+$1.2 / −7.8bn). Clause 2: "
                        "the service break-even is −11.0% to −2.4% (personal) and −9.3% to −0.6% (shared) with the enterprise "
                        "surplus at 1, and −5.5% to +3.3% with it at s. A negative break-even means the group costs others at every "
                        "service response from 0 to 1. On the cash set it is 7.0–22.2%. [CALCULATION: c2_break_even_sept29.csv]",
        break_distance_note="Clause 1 comes back at the low end with the tax block's favorable tail alone (+$2.1bn); at the high end "
                            "it needs all six tax and transfer tails at their favorable ends (+$6.9bn) [INFERENCE: additive, "
                            "components.csv]. Clause 2 survives only at the least adverse end with the enterprise surplus at s "
                            "(below a 1.5–3.3% response).",
        rival_reading="Counted as 2024 cash flows, the group's taxes exceed its benefits by $60–73bn and services decide the sign "
                      "(break-even 7–22%): payroll taxes are this year's receipts, and the benefits they earn are paid from later "
                      "budgets. [FRAMING-SENSITIVE]",
        discriminating_observation="Mostly values (2024 cash flows vs benefits earned). The fact inside it: the money's worth of the "
                                   "group's payroll taxes (net OASDI 0.974 and the Part A accrual are national ratios); the group's "
                                   "own earnings histories and mortality would move it.",
        observed_yet="no (national ratios only)",
        source="c2_tally_sept29.csv; c2_break_even_sept29.csv; ladder 239, 257, 275; decisions/2026-09-29-main-case-v4.md; "
               "main_case_2026_09_29/derived/sign_reversal.csv",
    ),
    dict(
        id="C3", claim_tested="Checks against records move taxes and spending by about $50bn each (44–57), and the two almost "
                              "cancel (net about $11bn)",
        status_on_v4="holds",
        deciding_premise="P08",
        reading_on_v4="Taxes +$44.43 / 45.84bn, spending −$55.16 / 57.15bn, net −$10.73 / 11.31bn; $10.66 / 11.47bn of the spending move is "
                      "the accrual following the corrected OASDI receipts.",
        premises="P08 (measured: T-MSIS LTSS 210, pooled MEPS 206, admin benefit keys 217, ASEC fill-in DiD 208; assumed: on-books "
                 "share 0.526 for flagged Mexico-born, 254); P09 imputed status flags; P07 CBO gradients (216); P01. On v4 also P05: "
                 "the accrual is computed on the corrected OASDI receipts and replaces current Social Security and Part A benefits.",
        break_condition="On v4, with the pension switch rebuilt on each set of corrections: taxes +$44.43 / 45.84bn and spending −$55.16 / "
                        "57.15bn, net −$10.73 / 11.31bn, no interaction. The spending move is the spending checks' −$44.50 / 45.68bn "
                        "plus the accrual's fall with the corrected OASDI receipts (−$10.95 / 11.78bn), −$10.66 / 11.47bn; $10.79 / "
                        "11.23bn of Social Security and Part A benefit corrections drop out, since the accrual replaces current "
                        "benefits. By the edits' side, the receipt checks "
                        "move the cost +$33.77 / 34.37bn and the spending checks −$44.50 / 45.68bn. With every increment held instead: "
                        "+$44.43 / 45.84bn and −$55.29 / 56.91bn, net −$10.86 / 11.07bn. [CALCULATION: c3_correction_split_sept29.csv] "
                        "'Net about $11bn' moves >25% on any one of six data-component tails (five at the low end). 'Almost cancel' "
                        "(the net under half the smaller side, $22.2 / 22.9bn) fails with two tails, care low + tax block low, "
                        "−$25.4 / 24.8bn; by the edits' side (half $16.9 / 17.2bn) care low alone does it, −$19.9 / 20.5bn "
                        "[INFERENCE: additive, components.csv].",
        break_distance_note="Net: 1 tail. Cancellation: 2 tails by the lines that move (1 by the edits' side). The rounded '$50bn "
                            "each' sits 8–14% off both sides.",
        rival_reading="The tax side is a model, not a record: it scales imputed-unauthorized pay to an assumed on-books share "
                      "($64.8bn of $136.8bn of wages off the books, 254), so two assumed adjustments of similar size may cancel.",
        discriminating_observation="SSA Earnings Suspense File and ITIN filer counts by state, 2022–24, to measure the on-books "
                                   "share (no 2022–25 measurement exists).",
        observed_yet="spending side yes (210, 255, 256); tax side partly (249 tests IRS national bins; the group's share per bin stays the CPS's)",
        source="c3_correction_split_sept29.csv; main_case_2026_09_29 components.csv; ladder 206, 208, 210, 216, 217, 249, 254–257",
    ),
    dict(
        id="C4", claim_tested="Costs outside the public budget add about $100bn a year",
        status_on_v4="holds",
        deciding_premise="none at the central",
        reading_on_v4="The social rows do not move with v4 ($96.3 / 100.7bn on the 39.7M priced); the pairing rises with the fiscal "
                      "case to $462.9–535.5bn, its low end on the Hispanic footing's fiscal case, not the adopted one. [DATA: "
                      "sept24_propagation sept29, 911afa6]",
        premises="Inherits C1's premises. Plus P12 VSL and dose-response (PM2.5 at $13.7m VSL; Miller victim prices), P13 "
                 "crash-volume elasticity (266), P19 offender shares (202). Measured: CCRS fault odds (264), NIBRS shares.",
        break_condition="The add (a quarter ≈ $25bn) breaks on any one item at its published range end, as on September 27: PM2.5 "
                        "−$38.2 / +52.8bn, crashes −$68.7 / +63.3bn, scale net ∓$70.5bn. The pairing (<$374.4bn or >$624.0bn) "
                        "needs two: crash low + scale low (−27.9%) or crash high + scale high (+26.8%); PM2.5 high + crash high "
                        "(+23.3%) no longer suffices. [INFERENCE: additive, real_costs_totals.csv §7 item ranges on the published "
                        "basis]",
        break_distance_note="Add: 1 item. Pairing: 2 items. The first-year horizon no longer breaks the pairing: about −21% with "
                            "the social rows held [INFERENCE]. The cash set pairs to $386.2–462.5bn (−15.0%).",
        rival_reading="Against as many average residents the group is cleaner (PM2.5 −$46.5bn) and no worse on crashes "
                      "(+$0.6bn): most of the add is the cost of any 39.7M people. [FRAMING-SENSITIVE: absolute vs normalized]",
        discriminating_observation="Values for absolute vs normalized. Fact: the crash sign turns on the crash-volume elasticity; "
                                   "a within-network panel of volumes × crashes in the group's counties (PeMS × CCRS) would "
                                   "narrow −58 to +74.",
        observed_yet="partly: transferable elasticities (266), CCRS fault odds (264); no local volume panel",
        source="ladder 189, 195, 202, 258, 260, 264–266, 274; sept24_propagation_2026_09_24/derived/sept29/real_costs_totals.csv",
    ),
    dict(
        id="C5", claim_tested="State and local taxpayers pay most of the cost (85%), and about one resident in six gains",
        status_on_v4="holds on 'most' (68%); 'one in six' not rerun",
        deciding_premise="P05 sets the share: the accrual is federal",
        reading_on_v4="State and local taxpayers pay about 68% (67.9% / 67.5%); the accrual, $76.7 / 73.0bn, is all federal. On "
                      "the cash set 85.7% / 81.2%.",
        premises="P03 (schools at 1 are state-local); P05; P06; P10 wage nest σ=2; P11 incidence: state-local cost charged where "
                 "the group lives, tax-share financing, household pooling. Measured: which budget pays each line; CPS persons.",
        break_condition="'Most' (>50%) survives defense by GDP share (58.5% / 59.3%), plus legacy interest $30.8 / 41.5bn (54.6% / "
                        "54.7%), plus scheduled benefits as well (50.8% / 51.6%); it fails with defense and old interest at average "
                        "cost (+$271bn federal: 39.2% / 41.6%). [CALCULATION: additive on debt_legacy_2026_09_23/derived/sept29/"
                        "federal_split_2024.csv, central convention; the $271bn is September 27's] 'One in six' is not rerun on v4: "
                        "the winners lane has no sept29 run [GAP]. Its taxpayers' channel is $394.4bn with the $74.9bn accrual, "
                        "which that lane assigns to future taxpayers, so today's taxpayers carry about $319.5bn, 8.5% less than "
                        "September 27's $349.3bn [INFERENCE: direction only; distribution_weights_2026_09_23 RESULT bridge].",
        break_distance_note="State-local share: nearer on v4, but it still needs the average-cost charge the repo rejects; with "
                            "defense, legacy interest and scheduled benefits it keeps 51%. Winners: one convention [INFERENCE: "
                            "September 24 swings].",
        rival_reading="Who gains is not identified: winners are modeled channel totals assigned to survey people; halving wage "
                      "deviations moves them 23.9% → 10.3% at the same aggregate (audit §2).",
        discriminating_observation="Person-level wage effects by skill and region from linked employer–employee data (LEHD) "
                                   "against the nest's assigned gains. The defense/interest charge is a values choice.",
        observed_yet="no",
        source="ladder 194, 207, 226; debt_legacy_2026_09_23/derived/sept29/federal_split_2024.csv; distribution_weights_2026_09_23 "
               "RESULT (sept29 bridge); research/immigration-weekly-conceptual-audit-2026-09-25.md §2",
    ),
    dict(
        id="C6", claim_tested="Each generation costs others, and progress stops after the second",
        status_on_v4="holds",
        deciding_premise="none at the central",
        reading_on_v4="Every generation costs others at both ends and under both conventions (at least $87.1bn); service "
                      "break-evens are at most 18.5%.",
        premises="C1's premises, plus: CPS parental birthplace (self-reported for 54%), child convention (a/b), household "
                 "allocation, P15 self-ID, P16 cross-section as lineage (CPS 1994–2025; GSS).",
        break_condition="Clause 1: a generation turns into a net gain only below its service break-even: at most 13.3% under "
                        "convention a and 18.5% under b (G3+, shared), on the generation account's corrected sept29 models "
                        "[CALCULATION: c6_generation_break_even_sept29.csv]. G1's are negative under b at every end and allocation: "
                        "a cost at any service response. On the cash set at most 35.1% (a) and 39.1% (b), every generation at least "
                        "$66.8bn. Clause 2 as on September 27: 0.84 of the BA+ gap carried G2→G3+ (232); a quarter (<0.63) needs "
                        "the literature's G2→G3 transmission 0.46–0.53 (236) in place of the CPS cross-section.",
        break_distance_note="Clause 1: far (at most 18.5% against at least 0.6 in every arm; 39.1% on cash). Clause 2: one source "
                            "swap, or the identity bound plus 2 SE.",
        rival_reading="Cross-sectional G3+ descends from earlier, less-selected stock, so G2 vs G3+ today is not parent→child; "
                      "matched by cohort, progress may continue. Partly answered: 0.83–0.87 in the 1979–85 cohort and at 25–44 (232).",
        discriminating_observation="Linked three-generation records tying G3 to G2 parents' schooling (restricted Census-linked "
                                   "data or PSID immigrant samples).",
        observed_yet="attempted, no power: CPS adults with a Mexico-born grandparent, closing 0.78 (SE 0.64) (232)",
        source="ladder 224, 232, 236, 255; generation_account_2026_09_24/derived/generation_results_sept29.csv, "
               "generation_corrections_sept29.json and _cash; c6_generation_break_even_sept29.csv",
    ),
    dict(
        id="C7", claim_tested="Legal status explains little of the fiscal gap",
        status_on_v4="unchanged (no v4 input)",
        deciding_premise="",
        reading_on_v4="Carried by ladder 85 on 2024 cash flows; not recomputed with pensions on accrual [GAP].",
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
        status_on_v4="not rerun here (v4-dated-b's lane); likely breaks",
        deciding_premise="P05 [INFERENCE]",
        reading_on_v4="On September 27's rough re-key the accrual arm gave $449.8 / 447.3bn, +41% on the $320bn against US whites "
                      "[INFERENCE: v4 counts pensions on accrual; v4-dated-b reruns the comparator].",
        premises="Rough re-key of the Sept 27 rules (not an engine run; union keys 3–7% below the engine); P14 third-plus "
                 "non-Hispanic whites at national rates; P05 handled by accrual or union ages; P07.",
        break_condition="September 27: already crossed by one computed alternative, local whites state by state (+28%), now in the "
                        "claim; both convention arms on accrual $449.8 / 447.3bn (+41%). Down: cash at whites' own ages $157.2 / "
                        "154.6bn (−51%), read as the age artefact. On v4 the accrual is the central, so the US-white figure "
                        "probably moves by more than a quarter [INFERENCE].",
        break_distance_note="Zero steps on v4 if the accrual arm carries over. The ordering (the group costs more) survives every "
                            "September 27 arm (min +$155bn).",
        rival_reading="The gap is composition (schooling, age), not group-specific; against an all-residents slice the union is "
                      "$85–87bn above average (263).",
        discriminating_observation="Framing (which reference answers the question). Fact left: the same re-key through the engine "
                                   "on v4.",
        observed_yet="partly (rough keys)",
        source="ladder 259, 263, 274",
    ),
    dict(
        id="C9", claim_tested="Immigrants offend less, and their US-born sons are held at about twice the white rate",
        status_on_v4="unchanged (no v4 input)",
        deciding_premise="",
        reading_on_v4="No fiscal input; v4 changes nothing here.",
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

# ---- premises on v4: kind, flags for C1..C9, and for the top five the best-supported alternative and its effect
C = [f"C{i}" for i in range(1, 10)]
PREMISES = [
    ("P01", "Survey frame: CPS ASEC / ACS Mexican-origin self-ID and parental birthplace, 39.7M priced in three generations",
     "measured (survey)", "C1 C2 C3 C4 C5 C6 C7 C8 C9"),
    ("P02", "Removal counterfactual over one income year (2024), people alive in 2024, no lifetime", "convention", "C1 C2 C3 C4 C5 C6 C7 C8"),
    ("P03", "Service budgets and property-tax levies respond at long-run rates (schools 1, general government 0.60–0.85, roads/parks "
            "long run, property taxes at the receipt-side lane's central)", "assumed (cross-section slopes)", "C1 C2 C4 C5 C6 C8"),
    ("P04", "Return on public capital at 2–3%", "convention", "C1 C2 C4 C5 C6"),
    ("P05", "Social Security and Medicare Part A on accrual at payable benefits, net of the income tax on benefits (v4's central)",
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
    ("P15", "Ethnic self-identification keeps descendants in the group", "measured in part (232)", "C6 C9"),
    ("P16", "Cross-sectional generations stand in for lineages", "assumed", "C6 C9"),
    ("P17", "ACS institutional counts identify custody by nativity and ethnicity", "measured, coding errors", "C9"),
    ("P18", "Texas arrest status from DHS record matches", "administrative", "C9"),
    ("P19", "Police-recorded offender ethnicity (NIBRS TX/AZ, SHR; arrests for use keys)", "measured", "C1 C4 C9"),
]
SWAP = {
    "P01": ("ACS level for the Mexico-born (CPS +9–13%, 209); NVSS births for the G2/G3 split (255)",
            "Not rerun on v4. On September 27: C1 −$2.2–2.5bn (−0.7%) [DATA: 209]; C2 ≈0 (removed people pay about what they "
            "cost, 209); C6 moves young children from G3+ to G2 [GAP]; C7 imputed unauthorized 4.57M → ~4.07M [GAP]; the rest "
            "< 1% [INFERENCE]. Breaks none [INFERENCE: v4's items do not change the frame's weights]."),
    "P02": ("First-year budget horizon (ladder 229), with property levies fixed and roads keyed on resources",
            "C1 −26.1% BREAK ($277.3–318.3bn) [CALCULATION: c1_arms_sept29.csv]; C4 pairing about −21%, holds [INFERENCE: social "
            "rows held]; C2 already fails at the central; C5, C6 and C8 not rerun on v4 [GAP]. Breaks one."),
    "P05": ("Cash, the September 27 convention (decision 2026-09-29, alternative 2)",
            "Restores C2: tally +$73.3 / 60.4bn, break-even 7.0–22.2% [CALCULATION: c2_tally_sept29.csv, c2_break_even_sept29.csv]. "
            "C1 −18.6% ($294.7–361.8bn), a break with no capital return (−29.9%) or first-year roads and parks (−27.8%) "
            "[CALCULATION: c1_min_cuts_sept29.csv]; C4 pairing $386.2–462.5bn (−15.0%) [DATA: 911afa6]; C5 state-local share "
            "68% → 81–86% [CALCULATION: debt lane split]; C6 every generation still costs others (at least $66.8bn; break-evens "
            "at most 39.1%) [CALCULATION]; C8 back toward its cash figure [INFERENCE]. Breaks none. Scheduled benefits instead: "
            "C1 +8.3%, C2 tally −$37.6 / −45.0bn, C5 about 62%."),
    "P08": ("No corrections (v4's items on the uncorrected model, the pension switch rebuilt)",
            "C1 +2.7% ($382.1–446.2bn) [CALCULATION: c3_correction_split_sept29.csv]; C2 tally +$1.2 / −7.8bn, clause 1 holds at "
            "the low end only [CALCULATION: c2_tally_sept29.csv]; C3 is this premise; C6 not split by generation [GAP]; C7 raw vs "
            "adjusted contrast changes direction (85). Breaks none."),
    "P03": ("Schools at the within-district 0.836 (the only within-unit estimate)",
            "C1 −6.2% ($345.5–410.5bn) [CALCULATION: c1_arms_sept29.csv]; property taxes at zero instead +6.7%; C2's tally has no "
            "services in it; C4 pairing about −5% [INFERENCE: social rows held]; C6 holds [INFERENCE]; C8 about −3% [INFERENCE: "
            "September 27's]. Breaks none."),
}
for arm, lo, hi in [("school_within_district", 345.54, 410.46), ("pension_cash", 294.70, 361.82)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi)
base = [num(split[("pension_rebuilt", e)], "v4_items_only_bn") for e in ENDS]
check("P08 swap low", base[0], 382.14)
check("P08 swap high", base[1], 446.15)
check("P08 swap move", 100 * (sum(base) / 2 / mid - 1), 2.7)
school_pair = [num(arms["school_within_district"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]) + social[0],
               num(arms["school_within_district"], "cost_high_bn") + social[1]]
check("P03 swap pairing", 100 * (sum(school_pair) / 2 / pmid - 1), -5.0, tol=0.5)

by_premise = []
for pid, text, kind, flags in PREMISES:
    fl = set(flags.split())
    by_premise.append((pid, text, kind, [1 if c in fl else 0 for c in C]))
order = sorted(by_premise, key=lambda r: (-sum(r[3]), r[0]))
rank = {r[0]: i + 1 for i, r in enumerate(order)}
top = [r[0] for r in order[:5]]
if set(top) != set(SWAP):
    sys.exit(f"[BLOCKED] top five premises are {top}; SWAP covers {sorted(SWAP)}")

D.mkdir(exist_ok=True)
with open(D / "conclusions_sept29.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    keys = ["id", "claim_tested", "status_on_v4", "deciding_premise", "reading_on_v4", "premises", "break_condition",
            "break_distance_note", "rival_reading", "discriminating_observation", "observed_yet", "source"]
    w.writerow(keys)
    for c in CONCLUSIONS:
        w.writerow([c[k] for k in keys])
with open(D / "common_mode_sept29.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["premise_id", "premise", "kind", *C, "n_conclusions", "rank", "best_supported_alternative", "effect_if_swapped"])
    for pid, text, kind, flags in order:
        alt, eff = SWAP.get(pid, ("", ""))
        w.writerow([pid, text, kind, *flags, sum(flags), rank[pid], alt, eff])
broken = [c["id"] for c in CONCLUSIONS if c["status_on_v4"].startswith("BREAKS")]
print(f"  ✓ conclusions_sept29.csv: {len(CONCLUSIONS)} rows, broken at the central: {', '.join(broken)}; "
      f"common_mode_sept29.csv: {len(PREMISES)} premises; top five {', '.join(top)}")

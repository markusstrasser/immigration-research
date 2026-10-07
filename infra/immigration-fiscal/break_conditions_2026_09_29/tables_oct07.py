"""Write derived/conclusions_oct07.csv and derived/common_mode_oct07.csv: the nine conclusions on main case v6.

The v6 case is main_case_2026_10_07 (key oct07): main case v5 (main_case_2026_10_05) plus the items of its payload's
meta.items, the pension accrual on the 2026 Trustees' separate-funds arm (pension_tr2026), state-local retiree health on
accrual (retiree_health), the added people at their measured ages (added_age_mix) and user fees with the education keys
by use (user_fees). Each row but C8 tests the same claim as tables_oct05.py, the evidence map's claims on the September 27
case, so the three cases read side by side; the map's current wording (insight-first since 2026-10-06, on v6 since
2026-10-07) restates C2 and C6 and adds a horizon claim, which this lane does not test [GAP]. Since 2026-10-08 C8 tests the map's live sentence instead
(groups.py selection/f263, quoting whites.gap_a1 and whites.gap_local on oct07), filled by the map's own registry
(overview_2026_09_28/quantities.py, imported read-only), so the claim follows the map. The text cells are this lane's reading of
`engine_breaks_sept29.cjs --case oct07`'s outputs and of the cited lanes' oct07 files. Every number quoted from them is
recomputed here first, so a changed input stops the build instead of leaving stale text. tables.py's, tables_sept29.py's
and tables_oct05.py's files are not touched. C4 reads the pairing's oct07 run (sept24_propagation), C5 the debt lane's
oct07 split and the winners lane's oct07 run (v5's beside), C6 the generation account's oct07 models through
c6_generation_break_even_oct07.csv, and C8 the white lane's oct07 re-key, which this propagation runs.
Run after `node engine_breaks_sept29.cjs --case oct07`:
    uv run --no-project --offline python3 infra/immigration-fiscal/break_conditions_2026_09_29/tables_oct07.py
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
LANE = F / "main_case_2026_10_07/derived"
WHITE = F / "white_replacement_2026_09_28/derived"
for need in [D / "c1_arms_oct07.csv", LANE / "summary.json", WHITE / "headline_oct07.csv"]:
    if not need.exists():
        sys.exit(f"[BLOCKED] {need.relative_to(F)} does not exist: run its oct07 case first")

# ---- C1: arms and minimal cuts
arms = {r["arm"]: r for r in rows(D / "c1_arms_oct07.csv")}
cuts = {(r["direction"], r["set"]): r for r in rows(D / "c1_min_cuts_oct07.csv")}
check("case low", num(arms["adopted"], "cost_low_bn"), 389.08)
check("case high", num(arms["adopted"], "cost_high_bn"), 461.48)
mid = num(arms["adopted"], "midpoint_bn")
check("midpoint", mid, 425.28)
bands = {r["variant"]: r for r in rows(LANE / "main_case_bands.csv") if r["profile"] == "long_run_non_school_full"}
mid_of = lambda v: (num(bands[v], "cost_low_bn") + num(bands[v], "cost_high_bn")) / 2  # noqa: E731
check("September 27 midpoint", mid_of("sept27_case"), 354.59, tol=0.005)
check("move on September 27", 100 * (mid / mid_of("sept27_case") - 1), 19.9)
check("v5 midpoint", mid_of("oct05_case"), 425.77, tol=0.005)
check("move on v5", 100 * (mid / mid_of("oct05_case") - 1), -0.1)
v6 = json.load(open(LANE / "summary.json"))["v6"]
check("per member low", v6["per_member_usd"]["set"][0], 9101, tol=0.5)
check("per member high", v6["per_member_usd"]["set"][1], 10794, tol=0.5)
check("lineage population", v6["per_member_usd"]["population"] / 1e6, 42.75, tol=0.005)
check("down cut", 0.75 * mid, 318.96, tol=0.005)
check("up cut", 1.25 * mid, 531.60, tol=0.005)
for arm, lo, hi, move in [("first_year_horizon", 288.93, 336.45, -26.5), ("first_year_horizon_cash", 207.25, 260.34, -45.0),
                          ("ancestry_share_low", 274.87, 320.84, -30.0), ("pension_cash", 307.40, 385.36, -18.6)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo, tol=0.005)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi, tol=0.005)
    check(f"{arm} move", num(arms[arm], "move_pct_of_midpoint"), move)
for arm, move in [("first_year_horizon_property_long_run", -33.5), ("capital_7pct", 20.3), ("property_none", 7.0),
                  ("school_within_district", -6.4), ("pension_scheduled", 9.9), ("lineage_arm_a", -3.2), ("lineage_arm_c", 3.2),
                  ("lineage_c3_plus_1se", -0.8), ("lineage_c3_minus_1se", 0.8), ("replacement_r1", -2.1),
                  ("ancestry_share_high", -17.7), ("ancestry_share_convention", -19.4),
                  ("pension_tr2026_combined_funds", 0.3), ("retiree_health_rho_one", -0.3), ("retiree_health_rho_high", 0.5),
                  ("added_age_mix_cohort_at_birth", -1.8), ("added_age_mix_rough_keys", 0.1)]:
    check(f"{arm} alone", num(arms[arm], "move_pct_of_midpoint"), move)
ITEM_ARMS = [a for a, r in arms.items() if r["kind"] == "item"]
if len(ITEM_ARMS) != 10 or max(abs(num(arms[a], "move_pct_of_midpoint")) for a in ITEM_ARMS) >= 2:
    sys.exit("[BLOCKED] the items' arms are not ten, each under 2%; the text says so")
if max(abs(num(arms[a], "move_pct_of_midpoint")) for a in ["lineage_arm_a", "lineage_arm_c", "lineage_c3_plus_1se",
                                                             "lineage_c3_minus_1se", "replacement_r1", "replacement_r05"]) >= 3.25:
    sys.exit("[BLOCKED] a lineage alternative other than the ancestry-share count moves C1 by more than 3.2%; the text says "
             "3.2% at most")
for key, lo, hi, move in [(("down", "capital_off+pension_cash"), 270.82, 324.30, -30.0),
                          (("down", "roads_parks_first_year+pension_cash"), 277.02, 335.25, -28.0)]:
    check(f"{key} low", num(cuts[key], "cost_low_bn"), lo, tol=0.005)
    check(f"{key} high", num(cuts[key], "cost_high_bn"), hi, tol=0.005)
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move)
for key, move in [(("down", "school_within_district+pension_cash+care_low"), -27.1),
                  (("down", "school_within_district+pension_cash+added_age_mix_cohort_at_birth"), -26.3),
                  (("down", "school_within_district+pension_cash+retiree_health_rho_one"), -25.3),
                  (("down", "capital_off+school_within_district+roads_parks_first_year+care_low"), -26.3),
                  (("down", "capital_off+school_within_district+roads_parks_first_year+added_age_mix_cohort_at_birth"), -25.9),
                  (("down", "capital_off+ancestry_share_convention"), -30.9), (("down", "pension_cash+ancestry_share_convention"), -34.0),
                  (("down", "roads_parks_first_year+ancestry_share_convention"), -28.9),
                  (("down", "school_within_district+ancestry_share_convention"), -25.8),
                  (("up", "capital_7pct+defense_gdp_share"), 34.4), (("up", "capital_7pct+pension_scheduled"), 30.2),
                  (("up", "capital_7pct+property_none"), 27.4), (("up", "property_none+pension_scheduled+defense_gdp_share"), 31.0),
                  (("up", "long_run_high+pension_scheduled+defense_gdp_share"), 27.1),
                  (("up", "pension_scheduled+defense_gdp_share+medical_mcbs65"), 26.0)]:
    check(f"{key} move", num(cuts[key], "move_pct_of_midpoint"), move)
minimal = [r for r in cuts.values() if r["minimal"] == "yes"]
size = lambda r: int(float(r["size"]))  # noqa: E731
parts = lambda r: r["set"].split("+")  # noqa: E731
ancestry = lambda r: any(p.startswith("ancestry_share") for p in parts(r))  # noqa: E731
down = [r for r in minimal if r["direction"] == "down"]
up = [r for r in minimal if r["direction"] == "up"]
if [r["set"] for r in down if size(r) == 1] != ["ancestry_share_low"]:
    sys.exit("[BLOCKED] the single downward cuts are not the ancestry-share count's low end alone")
pairs_cash = sorted(r["set"] for r in down if not ancestry(r) and size(r) == 2)
if pairs_cash != ["capital_off+pension_cash", "roads_parks_first_year+pension_cash"]:
    sys.exit(f"[BLOCKED] with whole people the downward pairs are {pairs_cash}; the text says no capital return or first-year "
             "roads and parks, each with cash pensions")
if ("down", "school_within_district+pension_cash") in cuts:
    sys.exit("[BLOCKED] schools at 0.836 with cash pensions breaks C1 on v6; the text says it falls short")
if min(size(r) for r in down if not ancestry(r) and "pension_cash" not in parts(r)) != 4:
    sys.exit("[BLOCKED] with whole people and without cash pensions the smallest downward cut is not 4")
if min(size(r) for r in up) != 2 or min(size(r) for r in up if "capital_7pct" not in parts(r)) != 3:
    sys.exit("[BLOCKED] the upward cuts are not 2 with 7% capital and 3 without")
stacks = {(r["direction"], size(r)): r for r in cuts.values() if r["minimal"] == "stack"}
if set(stacks) != {("down", 10), ("down", 11), ("up", 9), ("up", 10)}:
    sys.exit(f"[BLOCKED] the stacks are {sorted(stacks)}; the text says 10 / 11 downward and 9 / 10 upward")
check("down stack", num(stacks[("down", 10)], "move_pct_of_midpoint"), -51.9)
check("down stack with the ancestry share", num(stacks[("down", 11)], "move_pct_of_midpoint"), -76.0)
check("up stack", num(stacks[("up", 9)], "move_pct_of_midpoint"), 57.4)
check("up stack with arm c", num(stacks[("up", 10)], "move_pct_of_midpoint"), 60.6)
if not stacks[("down", 11)]["set"].endswith("+ancestry_share_low") or not stacks[("up", 10)]["set"].endswith("+lineage_arm_c"):
    sys.exit("[BLOCKED] the lineage stacks do not add the ancestry share's low end and arm c")
for d_, items in [("down", ["retiree_health_rho_one", "added_age_mix_cohort_at_birth"]),
                  ("up", ["pension_tr2026_combined_funds", "retiree_health_rho_high", "added_age_mix_rough_keys"])]:
    s_ = stacks[(d_, 10 if d_ == "down" else 9)]["set"]
    if not all(i in s_.split("+") for i in items):
        sys.exit(f"[BLOCKED] the {d_} stack does not carry the items' arms {items}")
check("first-year horizon clears the cut by", -num(arms["first_year_horizon"], "move_pct_of_midpoint") - 25, 1.5)
n_item_cuts = sum(1 for r in minimal if any(p in ITEM_ARMS for p in parts(r)))
check("minimal cuts with an item arm", n_item_cuts, 81, tol=0.5)
check("minimal cuts", len(minimal), 158, tol=0.5)
if min(size(r) for r in minimal if any(p in ITEM_ARMS for p in parts(r))) < 3:
    sys.exit("[BLOCKED] an item arm enters a minimal cut of one or two; the text says always as a third or later step")
# Schools at 0.836 with cash pensions is no cut, so no file carries it: each triple with one item arm, less that arm's
# change on the cash set (summary.json v6.arms, the change the script adds), gives the pair; the three must agree.
pair = [[num(cuts[("down", f"school_within_district+pension_cash+{a}")], k) - v6["arms"][a]["cash"]["change_from_the_cash_set_bn"][j]
         for j, k in enumerate(("cost_low_bn", "cost_high_bn"))]
        for a in ("retiree_health_rho_one", "retiree_health_mu_low", "added_age_mix_cohort_at_birth")]
if max(abs(p[j] - pair[0][j]) for p in pair for j in (0, 1)) > 1e-3:
    sys.exit(f"[BLOCKED] the three triples give different schools-plus-cash pairs: {pair}")
check("schools 0.836 + cash pensions, low", pair[0][0], 279.57, tol=0.005)
check("schools 0.836 + cash pensions, high", pair[0][1], 358.79, tol=0.005)
check("schools 0.836 + cash pensions, move", 100 * (sum(pair[0]) / 2 / mid - 1), -24.95, tol=0.005)

# ---- C2: tally and break-evens
tally = {(r["model"], r["end"]): r for r in rows(D / "c2_tally_oct07.csv")}
for model, col, want in [("case_accrual", "tally_bn", (6.2, -5.3)), ("case_accrual", "direct_receipts_bn", (449.5, 421.5)),
                         ("case_accrual", "household_transfers_bn", (443.3, 426.8)), ("case_accrual", "tally_at_scheduled_bn", (-37.1, -45.8)),
                         ("case_accrual", "scheduled_move_bn", (43.3, 40.5)),
                         ("union_at_case_responses", "tally_bn", (-3.7, -13.3)), ("cash_set", "tally_bn", (87.9, 70.8)),
                         ("v4_items_without_dataset_corrections", "tally_bn", (11.0, -0.2)), ("lineage_arm_a", "tally_bn", (4.3, -6.3)),
                         ("lineage_arm_c", "tally_bn", (8.1, -4.4))]:
    for end, w in zip(ENDS, want):
        check(f"C2 {model} {col} {end}", num(tally[(model, end)], col), w)
own = [num(tally[("case_accrual", e)], "tally_bn") - num(tally[("union_at_case_responses", e)], "tally_bn") for e in ENDS]
check("C2 the added people's own tally, low", own[0], 9.9)
check("C2 the added people's own tally, high", own[1], 7.9)
# Printed parts add: union -3.7 + added 9.9 = 6.2; -13.3 + 7.9 = -5.4, printed -5.3: controlled rounding gives added 8.0.
if (round(-3.7 + 9.9, 1), round(-13.3 + 8.0, 1)) != (6.2, -5.3):
    sys.exit("[BLOCKED] the printed tally parts do not add")
check("C2 the added people's own tally, high, as printed (controlled rounding)", own[1], 8.0, tol=0.1)
be = {(r["case"], r["variant"], r["allocation"]): r for r in rows(D / "c2_break_even_oct07.csv")}
# Two decimals: the file's four (-0.0905) do not settle the first decimal of -9.05%.
for key, most, least in [(("case_accrual", "enterprises_at_1", "personal"), -9.05, -0.66), (("case_accrual", "enterprises_at_1", "shared"), -7.03, 1.58),
                         (("case_accrual", "enterprises_at_s", "personal"), -3.65, 3.16), (("case_accrual", "enterprises_at_s", "shared"), -1.63, 5.38)]:
    check(f"{key} most", 100 * num(be[key], "break_even_most_adverse"), most, tol=0.005)
    check(f"{key} least", 100 * num(be[key], "break_even_least_adverse"), least, tol=0.005)
cash_be = [100 * num(r, k) for (c, _, _), r in be.items() if c == "cash_set" for k in r if k.startswith("break_even")]
check("cash set break-even, lowest", min(cash_be), 8.3)
check("cash set break-even, highest", max(cash_be), 24.2)
# Clause 1's distance: the tax and transfer tails of components.csv, additive.
comp = {r["component"]: r for r in rows(LANE / "components.csv")}
LO = {"low_end_48": "range_dev_low_end_lo", "high_end_11": "range_dev_high_end_lo"}
HI = {"low_end_48": "range_dev_low_end_hi", "high_end_11": "range_dev_high_end_hi"}
TAX_TRANSFER_TAILS = ["tax_block", "income_tax", "medical", "ltss", "benefits", "care"]
t0 = {e: num(tally[("case_accrual", e)], "tally_bn") for e in ENDS}
restore = [k for k in TAX_TRANSFER_TAILS if t0["high_end_11"] - num(comp[k], LO["high_end_11"]) > 0]
if restore != ["care"]:
    sys.exit(f"[BLOCKED] single tails restoring clause 1 at the high end: {restore}; the text says care alone")
check("tally, high end, care's favorable tail", t0["high_end_11"] - num(comp["care"], LO["high_end_11"]), 3.9)
check("tally, high end, the tax block's favorable tail", t0["high_end_11"] - num(comp["tax_block"], LO["high_end_11"]), -1.09, tol=0.005)
pairs = {k: t0["high_end_11"] - num(comp["tax_block"], LO["high_end_11"]) - num(comp[k], LO["high_end_11"]) for k in TAX_TRANSFER_TAILS[1:]}
if min(pairs.values()) <= 0 or min(pairs, key=pairs.get) != "medical":
    sys.exit(f"[BLOCKED] the tax block plus one more tail: {pairs}; the text says every pair restores it, medical's least")
check("tally, high end, tax block plus one more tail, smallest", min(pairs.values()), 0.08, tol=0.005)
breaks_low = [k for k in TAX_TRANSFER_TAILS if t0["low_end_48"] - num(comp[k], HI["low_end_48"]) < 0]
if breaks_low != ["medical"]:
    sys.exit(f"[BLOCKED] single tails breaking clause 1 at the low end: {breaks_low}; the text says medical alone")
check("tally, low end, medical's adverse tail", t0["low_end_48"] - num(comp["medical"], HI["low_end_48"]), -2.3)
check("tally, low end, the tax block's adverse tail", t0["low_end_48"] - num(comp["tax_block"], HI["low_end_48"]), 0.6)

# ---- C3: the corrections by side (the lineage's and the items' edits held in every run)
split = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_oct07.csv")}
for reading, col, want in [("pension_rebuilt", "taxes_move_by_line_type_bn", (44.43, 45.84)), ("pension_rebuilt", "spending_move_by_line_type_bn", (-54.92, -56.89)),
                           ("pension_rebuilt", "net_move_bn", (-10.49, -11.05)), ("pension_rebuilt", "accrual_follow_through_bn", (-10.44, -11.23)),
                           ("pension_rebuilt", "oasdi_receipts_move_bn", (-10.95, -11.78)), ("pension_rebuilt", "tax_side_move_bn", (33.99, 34.61)),
                           ("pension_rebuilt", "spending_side_move_bn", (-44.48, -45.66)), ("increments_held", "tax_side_move_bn", (44.43, 45.84)),
                           ("increments_held", "spending_side_move_bn", (-55.27, -56.89)), ("increments_held", "net_move_bn", (-10.84, -11.05))]:
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
                                    (("tax_side_move_bn", "spending_side_move_bn"), ["care"], None, (17.0, 17.3))]:
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
      + num(comp["tax_block"], LO["low_end_48"]), -25.2)
check("C3 care + tax block, high end", num(split[("pension_rebuilt", "high_end_11")], "net_move_bn") + num(comp["care"], LO["high_end_11"])
      + num(comp["tax_block"], LO["high_end_11"]), -24.5)
check("C3 care alone, low end", num(split[("pension_rebuilt", "low_end_48")], "net_move_bn") + num(comp["care"], LO["low_end_48"]), -19.7)
check("C3 care alone, high end", num(split[("pension_rebuilt", "high_end_11")], "net_move_bn") + num(comp["care"], LO["high_end_11"]), -20.2)
# Against v5's split: the receipt checks' taxes are the same; the accrual follows the corrected OASDI receipts by less,
# because the pension item lowers the accrual per tax dollar (0.9535 against 0.9737).
split5 = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_oct05.csv")}
for k in split:
    check(f"C3 {k} taxes by line type as v5's", num(split[k], "taxes_move_by_line_type_bn"), num(split5[k], "taxes_move_by_line_type_bn"), tol=1e-4)
    check(f"C3 {k} OASDI receipts move as v5's", num(split[k], "oasdi_receipts_move_bn"), num(split5[k], "oasdi_receipts_move_bn"), tol=1e-4)
worst = max(abs(num(split[k], "net_move_bn") - num(split5[k], "net_move_bn")) for k in split)
check("C3 the net's largest move from v5", worst, 0.26, tol=0.005)
for end, w in zip(ENDS, (0.22, 0.24)):
    check(f"C3 the accrual's follow-through, less than v5's, {end}",
          num(split[("pension_rebuilt", end)], "accrual_follow_through_bn") - num(split5[("pension_rebuilt", end)], "accrual_follow_through_bn"), w, tol=0.005)
acc = json.load(open(LANE / "corrections.json"))["meta"]["pension_accrual"]
check("C3 the accrual per tax dollar", acc["ratio_net"], 0.9535, tol=5e-5)
check("C3 v5's accrual per tax dollar", acc["previous"]["oct05"]["ratio_net"], 0.9737, tol=5e-5)

# ---- C8: the white lane's oct07 re-key (both sides on the lineage's 42.75M)
head = {(r["figure"], r["end"]): r for r in rows(WHITE / "headline_oct07.csv")}
A1 = "age artefact removed: A1 third-plus whites, accrual (central)"
LOCAL = "local whites state by state, union ages, accrual (central)"
A3 = "age artefact removed: A3 white rates at union ages, accrual"
RAW = "raw cash at white ages: A1, cash set"
# Both sides on the IPEDS keys for Pell and public higher education, with item 4's tuition term; the comparators'
# hospital term is beside the central (the white lane's v6 section, the team lead's decision of 2026-10-07). Its
# ipeds_terms_oct07.csv holds A1 on the rough keys of September 27 and with the hospital term beside. Every group's
# income taxes are on the case's own keys (the white lane's round 2, 2026-10-07); the CPS-dollar rule is an arm.
for fig, col, want in [(A1, "oct07_bn", (431.6, 436.0)), (A1, "per_member", (10096, 10197)), (A1, "oct05_bn", (425.2, 428.1)),
                       (LOCAL, "oct07_bn", (528.6, 531.5)), (LOCAL, "per_member", (12365, 12431)), (A3, "oct07_bn", (411.4, 415.7)),
                       (RAW, "oct07_bn", (263.5, 269.8))]:
    for end, w in zip(("low", "high"), want):
        check(f"C8 {fig} {col} {end}", num(head[(fig, end)], col), w, tol=0.5 if col == "per_member" else 0.05)
terms = {(r["basis"], r["group"], r["end"]): r for r in rows(WHITE / "ipeds_terms_oct07.csv")}
for end, w, wh in zip(("low", "high"), (425.1, 429.5), (434.3, 438.6)):
    check(f"C8 A1 on the rough keys of September 27 {end}",
          num(terms[("accrual", "A1_third_plus_nh_white", end)], "delta_like_for_like_rough_keys_bn"), w)
    check(f"C8 A1 with the comparators' hospital term {end}",
          num(terms[("accrual", "A1_third_plus_nh_white", end)], "delta_with_hospital_bn"), wh)
fig_mid = lambda fig: (num(head[(fig, "low")], "oct07_bn") + num(head[(fig, "high")], "oct07_bn")) / 2  # noqa: E731
a1_mid, local_mid = fig_mid(A1), fig_mid(LOCAL)
# The claim is the map's sentence, filled by the map's own registry, whose two records are this lane's A1 and
# local-whites centrals (exact). So the central restates the claim, and each arm is read against the claim's figure for
# the same whites: about $434bn (A1's midpoint) for third-plus whites, about $530bn for local whites. A quarter breaks it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(F / "overview_2026_09_28"))
import groups as MAP  # noqa: E402  the evidence map's text, read-only
import quantities as Q  # noqa: E402  the evidence map's registry and renderer, read-only

site = Q.groups_sites(MAP.GROUPS).get("selection/f263/text", "")
if "{{q:whites.gap_a1|mid_range}}" not in site or "{{q:whites.gap_local|mid_range}}" not in site:
    sys.exit("[BLOCKED] the map's C8 sentence (groups.py selection/f263/text) no longer quotes whites.gap_a1 and whites.gap_local")
C8_CLAIM = Q.fill(site)[0]
if C8_CLAIM != ("Against as many third-generation whites, the group costs others about $434bn (432–436) a year more. "
                "Against local whites, state by state, the gap is about $530bn (529–531)."):
    sys.exit(f"[BLOCKED] the map's C8 sentence now reads {C8_CLAIM!r}: restate C8")
# The one swap that breaks C8 (P05 at whites' own ages) is the reading the map prints beside the claim.
if "{{q:whites.gap_cash|mid_range}}" not in Q.groups_sites(MAP.GROUPS).get("selection/f263/why", ""):
    sys.exit("[BLOCKED] the map's C8 why line (groups.py selection/f263/why) no longer quotes whites.gap_cash: restate C8's note")
for rid, fig in (("whites.gap_a1", A1), ("whites.gap_local", LOCAL), ("whites.gap_cash", RAW)):
    want = tuple(num(head[(fig, e)], "oct07_bn") for e in ("low", "high"))
    if Q.record_value(rid) != want:
        sys.exit(f"[BLOCKED] the map's {rid} is {Q.record_value(rid)}, not headline_oct07.csv's {fig!r} {want}")
check("C8 the claim's figure against third-plus whites", a1_mid, 433.78, tol=0.005)
check("C8 the claim's figure against local whites", local_mid, 530.05, tol=0.005)
check("C8 cash at whites' own ages on A1", 100 * (fig_mid(RAW) / a1_mid - 1), -38.5)
check("C8 A3 on A1", 100 * (fig_mid(A3) / a1_mid - 1), -4.7)
for col, w in (("delta_with_hospital_bn", 0.6), ("delta_like_for_like_rough_keys_bn", -1.5)):
    check(f"C8 A1 {col} on the claim", 100 * (sum(num(terms[("accrual", "A1_third_plus_nh_white", e)], col) for e in ("low", "high")) / 2
                                          / a1_mid - 1), w)
wsum = {(r["basis"], r["group"], r["end"]): r for r in rows(WHITE / "rekey_summary_oct07.csv")}
arm = lambda col: [num(wsum[("accrual", "mexican_origin_rough", e)], col) - num(wsum[("accrual", "A1_third_plus_nh_white", e)], col)  # noqa: E731
                   for e in ("low", "high")]
# On the case's income-tax keys the top tail is inside the central, so both arms are the capital arm; the CPS-dollar
# rule (the central before round 2) and the proportional spread are arms below it.
for col, lo, hi, move in [("cost_both_arms", 503.0, 508.5, 16.6), ("cost_capital_taxes_respond", 503.0, 508.5, 16.6),
                          ("cost_top_tail_proportional", 421.4, 425.8, -2.3), ("cost_cps", 380.3, 384.7, -11.8)]:
    v = arm(col)
    check(f"C8 {col} low", v[0], lo)
    check(f"C8 {col} high", v[1], hi)
    check(f"C8 {col} move", 100 * (sum(v) / 2 / a1_mid - 1), move)
avg = arm("cost")
check("C8 the union over A1's slice, as the headline", avg[0], num(head[(A1, "low")], "oct07_bn"), tol=1e-3)
allres = [num(wsum[("accrual", "mexican_origin_rough", e)], "cost") - num(wsum[("accrual", "all_residents_slice", e)], "cost") for e in ("low", "high")]
check("C8 against an all-residents slice, low", allres[0], 261.8)
check("C8 against an all-residents slice, high", allres[1], 267.2)
rough = [num(wsum[("accrual", "mexican_origin_rough", e)], "cost") / num(wsum[("accrual", "mexican_origin_engine", e)], "cost") - 1 for e in ("low", "high")]
check("C8 the rough union on the engine's, low", 100 * rough[0], -2.3)
check("C8 the rough union on the engine's, high", 100 * rough[1], -5.0)
allres_cash = [num(wsum[("cash", "mexican_origin_rough", e)], "cost") - num(wsum[("cash", "all_residents_slice", e)], "cost") for e in ("low", "high")]
check("C8 against an all-residents slice on cash, low", allres_cash[0], 162.2)
check("C8 against an all-residents slice on cash, high", allres_cash[1], 169.5)
# P05's swap on C8: the cash figures of the same headline.
A3_CASH = "age artefact removed: A3 white rates at union ages, cash"
LOCAL_CASH = "local whites state by state, union ages, cash"
for fig, want in [(A3_CASH, (419.6, 425.9)), (LOCAL_CASH, (554.1, 559.0))]:
    for end, w in zip(("low", "high"), want):
        check(f"C8 {fig} {end}", num(head[(fig, end)], "oct07_bn"), w)
check("C8 A3 on cash on the claim's $434bn", 100 * (fig_mid(A3_CASH) / a1_mid - 1), -2.5)
check("C8 local whites on cash on the claim's $530bn", 100 * (fig_mid(LOCAL_CASH) / local_mid - 1), 5.0)
check("C8 the smallest arm", min(num(head[(f, e)], "oct07_bn") for f in (A1, LOCAL, A3, RAW, A3_CASH, LOCAL_CASH)
                                 for e in ("low", "high")), 263.5)

# ---- C4, C5, C6: the pairing's, the debt lane's and the generation account's oct07 runs
for need in [F / "sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv",
             F / "debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv",
             D / "c6_generation_break_even_oct07.csv"]:
    if not need.exists():
        sys.exit(f"[BLOCKED] {need.relative_to(F)} does not exist: C4-C6 read the pairing's, the debt lane's and the generation "
                 "account's oct07 runs")
rc = {(r["column"], r["item"]): r["oct07"] for r in rows(F / "sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv")}
pair = [float(rc[("pairing_on_priced_count", f"published pairing ({e})")]) for e in ("low", "high")]
footing = [float(rc[("hispanic", "fiscal main case (low)")]), float(rc[("custody", "fiscal main case (high)")])]
social = [p - f for p, f in zip(pair, footing)]
added = [float(rc[("pairing_on_priced_count", f"the added people's social rows ({e})")]) for e in ("low", "high")]
check("pairing low", pair[0], 489.02, tol=0.005)
check("pairing high", pair[1], 570.68, tol=0.005)
check("social rows low", social[0], 104.7)
check("social rows high", social[1], 109.2)
check("added people's social rows low", added[0], 8.4)
check("added people's social rows high", added[1], 8.5)
per = [float(rc[("pairing_on_priced_count", f"published pairing per group member ({e})")]) for e in ("low", "high")]
check("pairing per member low", 1000 * per[0], 11438, tol=0.5)
check("pairing per member high", 1000 * per[1], 13349, tol=0.5)
pmid = sum(pair) / 2
check("pairing down cut", 0.75 * pmid, 397.4)
check("pairing up cut", 1.25 * pmid, 662.3)
dev = {}
for item in ["pm25_consumption", "road_crash_externality", "scale_net_earnings"]:
    c = float(rc[(f"social_item_{item}", "central, both ends")])
    dev[item] = (float(rc[(f"social_item_{item}", "low, full span")]) - c, float(rc[(f"social_item_{item}", "high, full span")]) - c)
for item, lo, hi in [("pm25_consumption", -38.2, 52.8), ("road_crash_externality", -68.7, 63.3), ("scale_net_earnings", -70.5, 70.5)]:
    check(f"{item} low deviation", dev[item][0], lo)
    check(f"{item} high deviation", dev[item][1], hi)
    if min(abs(dev[item][0]), abs(dev[item][1])) < 0.25 * sum(social) / 2:
        sys.exit(f"[BLOCKED] {item} at a range end does not move the add by a quarter")
check("add quarter", 0.25 * sum(social) / 2, 26.7)
check("pairing: crash low + scale low", 100 * (dev["road_crash_externality"][0] + dev["scale_net_earnings"][0]) / pmid, -26.3)
check("pairing: crash high + scale high", 100 * (dev["road_crash_externality"][1] + dev["scale_net_earnings"][1]) / pmid, 25.2)
check("pairing: PM2.5 high + crash high", 100 * (dev["pm25_consumption"][1] + dev["road_crash_externality"][1]) / pmid, 21.9)
if any(abs(dev[a][k] + dev[b][k]) / pmid > 0.25 for a, b in itertools.combinations(dev, 2) for k in (0, 1)
       if {a, b} != {"road_crash_externality", "scale_net_earnings"}):
    sys.exit("[BLOCKED] another pair of items breaks the pairing")
fy = [num(arms["first_year_horizon"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]), num(arms["first_year_horizon"], "cost_high_bn")]
check("pairing at the first-year horizon, social rows held", 100 * ((fy[0] + social[0] + fy[1] + social[1]) / 2 / pmid - 1), -21.2)
cash_pair = [float(rc[("pairing_on_priced_count_cash_set", f"published pairing ({e})")]) for e in ("low", "high")]
check("cash-set pairing low", cash_pair[0], 407.34, tol=0.005)
check("cash-set pairing high", cash_pair[1], 494.56, tol=0.005)
check("cash-set pairing move", 100 * (sum(cash_pair) / 2 / pmid - 1), -14.9)
for item, want in [("social_item_pm25_consumption", -46.5), ("social_item_road_crash_externality", 0.6)]:
    check(f"{item} normalized", float(rc[(item, "normalized central, beside")]), want)

# C5: the state-local share (debt_legacy's oct07 split, central convention, main profile)
split7 = {r["end"]: r for r in rows(F / "debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv")
          if r["profile"] == "long_run_non_school_full" and r["convention"] == "central"}
COLS = ["fiscal_gap_bn", "resource_cost_bn", "displaced_bn", "accrual_bn"]
FED = ["federal_bn", "resource_cost_federal_bn", "displaced_federal_bn", "accrual_federal_bn"]
with open(F / "debt_legacy_2026_09_23/derived/oct07/summary.json") as f:
    debt = json.load(f)["case"]
# debt_legacy.py keeps the run's case block under "v4" (its v4_summary(); case.v5 adds the lineage, case.v6 the items).
headline = debt["v4"]["headline_2024"]
if abs(debt["v5"]["lineage"]["counts"]["lineage_population"] / 1e6 - 42.75) > 0.005 or debt["v6"]["base"] != "oct05":
    sys.exit("[BLOCKED] the debt lane's oct07 run is not v6 on the 42.75M lineage")
for e in ("low", "high"):
    check(f"the debt lane's set is the case, {e}", headline[e]["set_net_cost_bn"], num(arms["adopted"], f"cost_{e}_bn"), tol=0.005)
LEGACY = {e: headline[e]["legacy_interest_2024_bn"] for e in ("low", "high")}
check("legacy interest low", LEGACY["low"], 31.8)
check("legacy interest high", LEGACY["high"], 44.2)
sched = {"low": num(arms["pension_scheduled"], "cost_low_bn") - num(arms["adopted"], "cost_low_bn"),
         "high": num(arms["pension_scheduled"], "cost_high_bn") - num(arms["adopted"], "cost_high_bn")}
share = {}
for e in ("low", "high"):
    r = split7[e]
    tot = sum(num(r, c) for c in COLS)
    sl = tot - sum(num(r, c) for c in FED)
    if abs(num(r, "accrual_bn") - num(r, "accrual_federal_bn")) > 1e-9:
        sys.exit("[BLOCKED] the accrual is not all federal in the debt lane's split")
    share[e] = dict(case=sl / tot, cash=sl / (tot - num(r, "accrual_bn")), scheduled=sl / (tot + sched[e]), defense=sl / (tot + 60),
                    defense_interest=sl / (tot + 60 + LEGACY[e]), defense_interest_scheduled=sl / (tot + 60 + LEGACY[e] + sched[e]),
                    average_cost=sl / (tot + 271))
    check(f"the split's total is the set's net cost plus P, {e}", tot, headline[e]["set_net_cost_bn"] + num(r, "production_P_bn"), tol=1e-6)
for key, want in [("case", (68.6, 68.0)), ("cash", (86.8, 81.5)), ("scheduled", (61.7, 62.6)), ("defense", (59.4, 60.2)),
                  ("defense_interest", (55.5, 55.5)), ("defense_interest_scheduled", (50.9, 51.8)), ("average_cost", (40.4, 42.9))]:
    for e, w in zip(("low", "high"), want):
        check(f"C5 state-local share {key} {e}", 100 * share[e][key], w)
check("accrual low", num(split7["low"], "accrual_bn"), 81.7)
check("accrual high", num(split7["high"], "accrual_bn"), 76.1)
# 'one in six': the winners lane's oct07 run, v5's beside
WIN = F / "winners_losers_2026_09_24/derived"
if not (WIN / "oct07/net_shares.csv").exists():
    sys.exit("[BLOCKED] winners_losers_2026_09_24/derived/oct07/net_shares.csv does not exist: C5 reads the winners lane's oct07 run")
for case, want in [("oct07", (17.5, 16.8)), ("oct05", (17.6, 16.9))]:
    shares = {(r["net"], r["stack"], r["unit"]): r for r in rows(WIN / case / "net_shares.csv")}
    for conv, w in zip(("a", "b"), want):
        check(f"C5 share ahead on {case} ({conv})", 100 * num(shares[(f"net_social_{conv}", "central", "spm_unit_pooled")], "winners_share"), w)

# C6: generations on the generation account's oct07 models (G3+ carries the lineage)
gen = rows(D / "c6_generation_break_even_oct07.csv")
gen5 = rows(D / "c6_generation_break_even_oct05.csv")
gen29 = rows(D / "c6_generation_break_even_sept29.csv")
bmax = lambda g, case, conv=None: 100 * max(num(r, k) for r in g if r["case"] == case and (conv is None or r["convention"] == conv)
                                            for k in r if k.startswith("break_even"))
for case, conv, want in [("case_accrual", "a", 16.8), ("case_accrual", "b", 21.7), ("cash_set", "a", 38.4), ("cash_set", "b", 42.2)]:
    check(f"C6 largest break-even {case} {conv}", bmax(gen, case, conv), want)
for conv, want in [("a", 3.5), ("b", 3.2)]:
    check(f"C6 rise of the largest break-even on v4's, {conv}", bmax(gen, "case_accrual", conv) - bmax(gen29, "case_accrual", conv), want)
cmin = lambda case: min(min(num(r, "cost_low_end_bn"), num(r, "cost_high_end_bn")) for r in gen if r["case"] == case)
check("C6 smallest generation cost, case", cmin("case_accrual"), 86.7)
check("C6 smallest generation cost, cash set", cmin("cash_set"), 72.7)
g3 = next(r for r in gen if r["case"] == "case_accrual" and r["convention"] == "a" and r["generation"] == "G3plus")
g3_5 = next(r for r in gen5 if r["case"] == "case_accrual" and r["convention"] == "a" and r["generation"] == "G3plus")
for col, now, before in [("cost_low_end_bn", 141.8, 141.7), ("cost_high_end_bn", 196.8, 195.0)]:
    check(f"C6 G3+ (a) {col}", num(g3, col), now)
    check(f"C6 G3+ (a) {col} on v5", num(g3_5, col), before)
if any(num(r, k) >= 0 for r in gen if r["case"] == "case_accrual" and r["convention"] == "b" and r["generation"] == "G1"
       for k in r if k.startswith("break_even")):
    sys.exit("[BLOCKED] a G1 break-even under convention b is not negative")
if any(min(num(r, "cost_low_end_bn"), num(r, "cost_high_end_bn")) <= 0 for r in gen):
    sys.exit("[BLOCKED] a generation does not cost others at an end")

# ---- conclusions on v6
CONCLUSIONS = [
    dict(
        id="C1", claim_tested="Other US residents pay about $355bn a year for the group's presence ($322–387bn)",
        status_on_v6="holds, restated",
        deciding_premise="none at the central; P02 alone breaks it, and so does P20 counted by ancestry share at its low end "
                         "[FRAMING-SENSITIVE]",
        reading_on_v6="$389.1–461.5bn, midpoint $425.3bn (+19.9% on $354.6bn; v5 $425.8bn, −0.1%); $9,101–10,794 per member of "
                      "the 42.75M lineage. [DATA: main_case_2026_10_07 summary.json v6]",
        premises="P01 frame; P02 one-year removal; P03 long-run service and property-tax responses; P04 capital return 2–3%; P05 pensions "
                 "on accrual at payable benefits (the 2026 Trustees' separate funds) and state-local retiree health on accrual; P06 "
                 "defense/old interest at 0; P07 keys, with user fees and education keyed by use; P08 corrections; P09 imputed status; "
                 "P10 production; P20 the lineage count (3.04M added, whole, at their measured ages). Measured: line amounts, keys' "
                 "shares, C3, the added people's ages. Assumed: P02–P06, P10, the count's arm.",
        break_condition="Down a quarter (<$319.0bn): the first-year budget horizon alone, $288.9–336.5bn (−26.5%), or the lineage "
                        "counted by ancestry share at the stated bound's low end alone, $274.9–320.8bn (−30.0%) [FRAMING-SENSITIVE]. "
                        "With whole people inside the long-run frame, cash pensions plus one of the case's own alternatives: no capital "
                        "return, $270.8–324.3bn (−30.0%), or roads and parks at CBO's first-year 0, $277.0–335.3bn (−28.0%). Schools at "
                        "0.836 with cash pensions, a pair on v5 (−25.3%), falls 0.05 points short on v6 ($279.6–358.8bn, −24.95%) and "
                        "takes a third: care low (−27.1%), the age mix by birth cohort (−26.3%) or retiree health at ρ = 1 (−25.3%). "
                        "Without cash pensions it takes four (e.g. no capital return + schools 0.836 + first-year roads and parks + care "
                        "low, −26.3%). Counted by ancestry share at the population lane's convention, one more alternative suffices (no "
                        "capital return −30.9%, cash pensions −34.0%, first-year roads and parks −28.9%, schools at 0.836 −25.8%). "
                        "Up a quarter (>$531.6bn): 7% capital + defense by GDP share (+34.4%), + scheduled benefits (+30.2%) or + "
                        "property taxes at zero (+27.4%); without 7% it takes three (scheduled benefits + defense + property taxes at "
                        "zero, +31.0%, or + the largest long-run response, +27.1%). [CALCULATION: engine_breaks_sept29.cjs --case oct07 "
                        "→ c1_arms_oct07.csv, c1_min_cuts_oct07.csv]",
        break_distance_note="The first-year horizon clears the cut by 1.5 points. Cash pensions alone −18.6% and 7% capital alone "
                            "+20.3%: each one alternative short. The lineage's own count moves it by 3.2% at most: arms a / c −3.2% / "
                            "+3.2%, C3 ± 1 SE ∓0.8%, the replacement child −2.1% (v5's change, not recomputed on v6) "
                            "[FRAMING-SENSITIVE]; the ancestry-share count by −17.7% to −30.0%. The items' ten arms each move it by "
                            "under 2% (the age mix by birth cohort −1.8%, retiree health −0.3% to +0.5%, the combined trust funds "
                            "+0.3%) and enter 81 of the 158 minimal cuts, always as a third or later step [APPROX: additive]. All 10 "
                            "downward alternatives stacked −51.9% (−76.0% with the ancestry share); all 9 upward +57.4% (+60.6% with "
                            "arm c).",
        rival_reading="The removal cost is mostly a horizon, pricing and pension convention: in the first year budgets respond at "
                      "CBO's rates, levies stay fixed and existing capital earns no return, $289–336bn; counted on cash as well, "
                      "$207–260bn. And the count is a convention: by ancestry share the lineage is 29.9–35.1M people and costs "
                      "$275–375bn. [FRAMING-SENSITIVE]",
        discriminating_observation="Budgets after population outflows (2008–12 Mexican net return, 2020–21 enrollment falls, "
                                   "declining-enrollment districts): spending falling ~1:1 within 3–5 years favors the long-run case. "
                                   "The count: grandparents' and great-grandparents' birthplaces for third-plus members (70% have "
                                   "no grandparent data).",
        observed_yet="partly: inflow side only (within-district 0.836, 230; 2022–24 surge money 'about half, and late', 252); "
                     "identity loss measured to the third generation (280), the added people's ages by band (added_age_mix_2026_10_07)",
        source="ladder 229, 230, 237–239, 252, 253, 257, 275, 280, 281, 286; main_case_2026_10_07 main_case_bands.csv, components.csv, "
               "summary.json v6 (v6.companions for the lineage's count and the ancestry share), ancestry_share.cjs (the convention); "
               "main_case_lineage_2026_10_05 v5_bands.csv (the replacement child); c1_arms_oct07.csv; c1_min_cuts_oct07.csv",
    ),
    dict(
        id="C2", claim_tested="Public services decide the sign: taxes cover benefits, but not schools and services",
        status_on_v6="BREAKS at the high end; holds at the low end",
        deciding_premise="P05: Social Security and Part A on accrual at payable benefits; P20: the added people's taxes exceed "
                         "their transfers",
        reading_on_v6="Direct taxes exceed benefits counted on accrual by $6.2bn at the low end and fall $5.3bn short at the high end "
                      "(v5 +$6.5 / −4.4bn). The added people's own tally, +$9.9 / 8.0bn, lifts the union's −$3.7 / −13.3bn.",
        premises="P01; P03; P04; P05 accrual at payable benefits (the 2026 Trustees' separate funds); P07; P08; P20. The tally (direct "
                 "receipts less household transfers, the accrual among the transfers) is +$6.2 / −5.3bn at ends 48 / 11: receipts "
                 "$449.5 / 421.5bn, transfers $443.3 / 426.8bn. [CALCULATION: c2_tally_oct07.csv]",
        break_condition="Clause 1 holds at the low end and fails at the high end, under arms a and c as well (+$4.3 / −6.3bn and "
                        "+$8.1 / −4.4bn). It holds on the cash set (+$87.9 / 70.8bn) and fails at both ends at scheduled benefits on "
                        "the 2026 inputs (−$37.1 / −45.8bn). Without the dataset corrections it now holds at the low end only (+$11.0 "
                        "/ −0.2bn; v5 +$11.1 / 0.4bn). Clause 2: the service break-even is −9.05% to −0.66% (personal) and −7.03% to "
                        "+1.58% (shared) with the enterprise surplus at 1, and −3.65% to +5.38% with it at s. A negative break-even "
                        "means the group costs others at every service response from 0 to 1. On the cash set it is 8.3–24.2%. "
                        "[CALCULATION: c2_tally_oct07.csv, c2_break_even_oct07.csv]",
        break_distance_note="One tail decides each end [INFERENCE: additive, components.csv]. At the high end care's favorable tail "
                            "alone restores clause 1 (+$3.9bn); the tax block's falls $1.09bn short, and with any one more tax or "
                            "transfer tail it restores it (by $0.08bn or more, medical's the least). At the low end the MCBS 65+ "
                            "bound on medical alone breaks it (−$2.3bn); the tax block's adverse tail leaves +$0.6bn. Clause 2 "
                            "survives only at the least adverse end (below a 1.58% response with the enterprise surplus at 1, "
                            "3.16–5.38% at s).",
        rival_reading="Counted as 2024 cash flows, the group's taxes exceed its benefits by $71–88bn and services decide the sign "
                      "(break-even 8–24%): payroll taxes are this year's receipts, and the benefits they earn are paid from later "
                      "budgets. [FRAMING-SENSITIVE]",
        discriminating_observation="Mostly values (2024 cash flows vs benefits earned). The fact inside it: the money's worth of the "
                                   "group's payroll taxes (net OASDI 0.954 on the 2026 Trustees' separate funds and the Part A "
                                   "accrual are national ratios); the group's own earnings histories and mortality would move it.",
        observed_yet="no (national ratios only)",
        source="c2_tally_oct07.csv; c2_break_even_oct07.csv; scheduled_tr2026.json; ladder 239, 257, 275, 281, 286; "
               "decisions/2026-09-29-main-case-v4.md, 2026-10-05-main-case-v5.md; main_case_2026_10_07/derived/sign_reversal.csv; "
               "main_case_lineage_2026_10_05 lineage_lines.csv",
    ),
    dict(
        id="C3", claim_tested="Checks against records move taxes and spending by about $50bn each (44–57), and the two almost "
                              "cancel (net about $11bn)",
        status_on_v6="holds",
        deciding_premise="P08",
        reading_on_v6="Taxes +$44.43 / 45.84bn, spending −$54.92 / 56.89bn, net −$10.49 / 11.05bn; $10.44 / 11.23bn of the "
                      "spending move is the accrual following the corrected OASDI receipts, $0.22 / 0.24bn less than on v5, because "
                      "the pension item lowers the accrual per tax dollar (0.954 against 0.974). The added people's amounts and the "
                      "items' edits are held.",
        premises="P08 (measured: T-MSIS LTSS 210, pooled MEPS 206, admin benefit keys 217, ASEC fill-in DiD 208; assumed: on-books "
                 "share 0.526 for flagged Mexico-born, 254); P09 imputed status flags; P07 CBO gradients (216); P01; P05: the accrual "
                 "is computed on the corrected OASDI receipts and replaces current Social Security and Part A benefits.",
        break_condition="On v6, with the union's pension switch rebuilt on each set of corrections and the lineage's and the items' "
                        "edits held in every run: taxes +$44.43 / 45.84bn and spending −$54.92 / 56.89bn, net −$10.49 / 11.05bn, no "
                        "interaction, the net within $0.26bn of v5's. The spending move is the spending checks' −$44.48 / 45.66bn "
                        "plus the accrual's fall with the corrected OASDI receipts (−$10.95 / 11.78bn), −$10.44 / 11.23bn; $10.79 / "
                        "11.23bn of Social Security and Part A benefit corrections drop out. By the edits' side, the receipt checks "
                        "move the cost +$33.99 / 34.61bn and the spending checks −$44.48 / 45.66bn. With every increment held instead: "
                        "+$44.43 / 45.84bn and −$55.27 / 56.89bn, net −$10.84 / 11.05bn. [CALCULATION: c3_correction_split_oct07.csv] "
                        "'Net about $11bn' moves >25% on any one of six data-component tails (five at the low end). 'Almost cancel' "
                        "(the net under half the smaller side, $22.2 / 22.9bn) fails with two tails, care low + tax block low, −$25.2 "
                        "/ 24.5bn; by the edits' side (half $17.0 / 17.3bn) care low alone does it, −$19.7 / 20.2bn [INFERENCE: "
                        "additive, components.csv].",
        break_distance_note="Net: 1 tail. Cancellation: 2 tails by the lines that move (1 by the edits' side). [GAP: the added "
                            "G3+ members are priced on the corrected G3+ model, so their amounts carry G3+'s corrections; holding "
                            "them leaves those out of the split.]",
        rival_reading="The tax side is a model, not a record: it scales imputed-unauthorized pay to an assumed on-books share "
                      "($64.8bn of $136.8bn of wages off the books, 254), so two assumed adjustments of similar size may cancel.",
        discriminating_observation="SSA Earnings Suspense File and ITIN filer counts by state, 2022–24, to measure the on-books "
                                   "share (no 2022–25 measurement exists).",
        observed_yet="spending side yes (210, 255, 256); tax side partly (249 tests IRS national bins; the group's share per bin stays the CPS's)",
        source="c3_correction_split_oct07.csv; main_case_2026_10_07 components.csv; ladder 206, 208, 210, 216, 217, 249, 254–257, 286",
    ),
    dict(
        id="C4", claim_tested="Costs outside the public budget add about $100bn a year",
        status_on_v6="holds",
        deciding_premise="none at the central",
        reading_on_v6="The social rows are $104.7 / 109.2bn (v5 $104.8 / 109.4bn): the added people's own rows, $8.4 / 8.5bn (v5 "
                      "$8.6 / 8.8bn; their key shares are read on v6's item base, at their measured ages), priced at their share "
                      "of each row's key. The pairing is $489.0–570.7bn, $11,438–13,349 per member of the 42.75M (v5 "
                      "$490.2–570.7bn); its low end is on the Hispanic footing's fiscal case. [DATA: sept24_propagation oct07, "
                      "band_variants.json lineage_social_keys]",
        premises="Inherits C1's premises. Plus P12 VSL and dose-response (PM2.5 at $13.7m VSL; Miller victim prices), P13 "
                 "crash-volume elasticity (266), P19 offender shares (202), P20 for the added people's rows. Measured: CCRS fault "
                 "odds (264), NIBRS shares.",
        break_condition="The add (a quarter ≈ $26.7bn) breaks on any one item at its published range end, as on v4 and v5: "
                        "PM2.5 −$38.2 / +52.8bn, crashes −$68.7 / +63.3bn, scale net ∓$70.5bn (each priced on the 39.71M; the "
                        "added people's rows held). The pairing (<$397.4bn or >$662.3bn) needs two: crash low + scale low "
                        "(−26.3%) or crash high + scale high (+25.2%); PM2.5 high + crash high reaches +21.9%. [INFERENCE: "
                        "additive, real_costs_totals.csv §7 item ranges on the published basis]",
        break_distance_note="Add: 1 item. Pairing: 2 items. The first-year horizon does not break the pairing: about −21.2% with the "
                            "social rows held [INFERENCE]. The cash set pairs to $407.3–494.6bn (−14.9%).",
        rival_reading="Against as many average residents the group is cleaner (PM2.5 −$46.5bn) and no worse on crashes "
                      "(+$0.6bn): most of the add is the cost of any 39.7M people. [FRAMING-SENSITIVE: absolute vs normalized]",
        discriminating_observation="Values for absolute vs normalized. Fact: the crash sign turns on the crash-volume elasticity; "
                                   "a within-network panel of volumes × crashes in the group's counties (PeMS × CCRS) would "
                                   "narrow −58 to +74.",
        observed_yet="partly: transferable elasticities (266), CCRS fault odds (264); no local volume panel",
        source="ladder 189, 195, 202, 258, 260, 264–266, 274, 281; sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv",
    ),
    dict(
        id="C5", claim_tested="State and local taxpayers pay most of the cost (85%), and about one resident in six gains",
        status_on_v6="holds on 'most' (68%) and 'one in six' (17.5% / 16.8%)",
        deciding_premise="P05 sets the share: the accrual is federal",
        reading_on_v6="State and local taxpayers pay about 68% (68.6% / 68.0%; v5 68.8% / 68.2%); the accrual, $81.7 / 76.1bn, "
                      "is all federal. On the cash set 86.8% / 81.5%. Pooled within SPM units, 17.5% of other residents come "
                      "out ahead under tax-share financing and 16.8% per person (v5 17.6% / 16.9%).",
        premises="P03 (schools at 1 are state-local); P05; P06; P10 wage nest σ=2; P11 incidence: state-local cost charged where "
                 "the group lives, tax-share financing, household pooling; P20. Measured: which budget pays each line; CPS persons.",
        break_condition="'Most' (>50%) survives defense by GDP share (59.4% / 60.2%), plus legacy interest $31.8 / 44.2bn (55.5% / "
                        "55.5%), plus scheduled benefits as well (50.9% / 51.8%); it fails with defense and old interest at average "
                        "cost (+$271bn federal: 40.4% / 42.9%). [CALCULATION: additive on debt_legacy_2026_09_23/derived/oct07/"
                        "federal_split_2024.csv, central convention; the $271bn is September 27's] 'One in six' on v6: 17.5% "
                        "(tax-share) and 16.8% (per person), pooled within SPM units, against 16.7% for one in six [DATA: "
                        "winners_losers_2026_09_24/derived/oct07/net_shares.csv].",
        break_distance_note="State-local share: 'most' needs the average-cost charge the repo rejects; with defense, legacy interest "
                            "and scheduled benefits it keeps 50.9% at the low end, under a point above half. Winners: one convention "
                            "[INFERENCE: September 24 swings].",
        rival_reading="Who gains is not identified: winners are modeled channel totals assigned to survey people; halving wage "
                      "deviations moves them 23.9% → 10.3% at the same aggregate (audit §2).",
        discriminating_observation="Person-level wage effects by skill and region from linked employer–employee data (LEHD) "
                                   "against the nest's assigned gains. The defense/interest charge is a values choice.",
        observed_yet="no",
        source="ladder 194, 207, 226, 281; debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv, summary.json; "
               "winners_losers_2026_09_24/derived/oct07/net_shares.csv; research/immigration-weekly-conceptual-audit-2026-09-25.md §2",
    ),
    dict(
        id="C6", claim_tested="Each generation costs others, and progress stops after the second",
        status_on_v6="holds",
        deciding_premise="none at the central",
        reading_on_v6="Every generation costs others at both ends and under both conventions (at least $86.7bn); service "
                      "break-evens are at most 21.7%. G3+ carries the added people: $141.8 / 196.8bn under convention a (v5: "
                      "$141.7 / 195.0bn).",
        premises="C1's premises, plus: CPS parental birthplace (self-reported for 54%), child convention (a/b), household "
                 "allocation, P15 self-ID, P16 cross-section as lineage (CPS 1994–2025; GSS), P20 (the added people on G3+, at "
                 "their measured ages).",
        break_condition="Clause 1: a generation turns into a net gain only below its service break-even: at most 16.8% under "
                        "convention a and 21.7% under b (G3+, shared), on the generation account's oct07 models [CALCULATION: "
                        "c6_generation_break_even_oct07.csv]. The added people raise G3+'s largest break-even by 3.5 / 3.2 points "
                        "over v4's: 1.08M of them are priced as third-plus whites. G1's are negative under b at every end and "
                        "allocation: a cost at any service response. On the cash set at most 38.4% (a) and 42.2% (b), every "
                        "generation at least $72.7bn. Clause 2: 0.86 of the BA+ gap carried G2→G3+ with C3 from the CPS basic "
                        "monthly frame (232, 280); a quarter (<0.645) needs the literature's G2→G3 transmission 0.46–0.53 (236) in "
                        "place of the CPS cross-section.",
        break_distance_note="Clause 1: far (at most 21.7% against at least 0.6 in every arm; 42.2% on cash). Clause 2: one source "
                            "swap.",
        rival_reading="Cross-sectional G3+ descends from earlier, less-selected stock, so G2 vs G3+ today is not parent→child; "
                      "matched by cohort, progress may continue. Partly answered: 0.83–0.87 in the 1979–85 cohort and at 25–44 (232).",
        discriminating_observation="Linked three-generation records tying G3 to G2 parents' schooling (restricted Census-linked "
                                   "data or PSID immigrant samples).",
        observed_yet="identity loss yes (280: 526 unique G3 non-identifiers at 25+, closing 0.57, SE 0.26); linkage no",
        source="ladder 224, 232, 236, 255, 280, 281; generation_account_2026_09_24/derived/generation_results_oct07.csv, "
               "generation_corrections_oct07.json and _cash; c6_generation_break_even_oct07.csv",
    ),
    dict(
        id="C7", claim_tested="Legal status explains little of the fiscal gap",
        status_on_v6="unchanged (no v6 input)",
        deciding_premise="",
        reading_on_v6="Carried by ladder 85 on 2024 cash flows; not recomputed with pensions on accrual [GAP]. The added people are "
                      "third-plus, with no status contrast, and no v6 item moves status.",
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
        id="C8", claim_tested=C8_CLAIM,
        status_on_v6="holds: the claim is the map's v6 figure",
        deciding_premise="P05 at whites' own ages [FRAMING-SENSITIVE]: on raw cash the gap falls 38.5%; inside the accrual none "
                         "(the nearest is P07's CPS-dollar rule, −11.8%)",
        reading_on_v6="The map quotes the white lane's oct07 re-key (whites.gap_a1, whites.gap_local). With both sides on the "
                      "lineage's 42.75M and every group's income taxes on the case's own keys (federal on the IRS-raked key, state "
                      "and other personal taxes on the state-liability key, the household's tax shared over its members), the "
                      "union costs others $431.6 / 436.0bn a year more than as many third-plus non-Hispanic whites at national "
                      "rates on the case's accrual basis ($10,096 / 10,197 per member; v5 on the same keys without the tuition "
                      "term $425.2 / 428.1bn), and $528.6 / 531.5bn more than local whites state by state at union ages. Both "
                      "sides take Pell by each group's IPEDS share, public higher education by its measured use, and on v6 "
                      "tuition by use [ASSUMPTION]; the comparators' hospital term stays beside. [CALCULATION: "
                      "white_replacement_2026_09_28 rekey_sept29.py --case oct07 → headline_oct07.csv, rekey_summary_oct07.csv, "
                      "ipeds_terms_oct07.csv, income_tax_keys_oct07.csv]",
        premises="Rough re-key of the case's rules (not an engine run); P14 third-plus non-Hispanic whites at national rates; P05 by "
                 "accrual, each group at its own accrual per tax dollar on the 2026 separate-funds path; P07, the case's income-tax "
                 "keys for every group; P20: the CPS re-keys cannot see the 3.04M, so the union's side carries them at the case "
                 "lane's amounts and each white slice is on 42.75M.",
        break_condition="A move of more than a quarter from the claim's figure for the same whites breaks it: $433.8bn (A1's "
                        "midpoint) against third-plus whites, $530.1bn against local whites. At the central both are the claim. "
                        "Against third-plus whites: each group charged only the income tax it reports to the CPS (the top tail the "
                        "survey misses charged to no one) $380.3 / 384.7bn (−11.8%); CPS income-tax dollars spread over the "
                        "national lines in proportion $421.4 / 425.8bn (−2.3%); white rates at the union's ages (A3) $411.4 / "
                        "415.7bn (−4.7%); capital-side taxes responding $503.0 / 508.5bn (+16.6%; with the top tail inside the "
                        "central it is also the both-arms figure); the comparators' hospital term $434.3 / 438.6bn (+0.6%); the "
                        "September 27 rough keys $425.1 / 429.5bn (−1.5%). All hold. P05 on cash: A3 $419.6 / 425.9bn (−2.5%) and "
                        "local whites $554.1 / 559.0bn (+5.0% on $530.1bn) hold; at whites' own ages $263.5 / 269.8bn (−38.5%) "
                        "breaks it downward, the age artefact the accrual removes [FRAMING-SENSITIVE]. [CALCULATION: "
                        "headline_oct07.csv, rekey_summary_oct07.csv, ipeds_terms_oct07.csv]",
        break_distance_note="One swap, and only on raw cash at whites' own ages, a reading the map prints beside the claim "
                            "($267bn, 263–270) and puts down to whites' older ages, which counting pensions when earned removes; "
                            "inside the accrual no arm reaches a quarter, the largest being capital-side taxes (+16.6%) and the "
                            "CPS-dollar rule (−11.8%). The ordering (the group costs more) holds in every arm, at least +$263.5bn.",
        rival_reading="The gap is composition (schooling, age), not group-specific; against an all-residents slice on the same "
                      "rough keys the union is $261.8 / 267.2bn above average on the case's accrual and $162.2 / 169.5bn on cash "
                      "(the September 27 cash run gave $85–87bn, 263).",
        discriminating_observation="Framing (which reference answers the question, and on which count). Fact left: the re-key "
                                   "through the engine; the rough keys put the union 2.3% below the engine's at the low end and "
                                   "5.0% below it at the high end, because on the same keys the engine's union pays less income "
                                   "tax: the case scales the union's income taxes by union-only corrections (the tax-records "
                                   "stack) that no comparator takes, and at the high end it gives each earner their own income "
                                   "tax where the comparators share it over the household.",
        observed_yet="partly (rough keys; v4, v5 and v6)",
        source="ladder 259, 263, 274, 281; the evidence map's groups.py selection/f263 (whites.gap_a1, whites.gap_local); "
               "white_replacement_2026_09_28 headline_oct07.csv, rekey_summary_oct07.csv, "
               "ipeds_terms_oct07.csv, income_tax_keys_oct07.csv",
    ),
    dict(
        id="C9", claim_tested="Immigrants offend less, and their US-born sons are held at about twice the white rate",
        status_on_v6="unchanged (no v6 input)",
        deciding_premise="",
        reading_on_v6="No fiscal input; v6 changes nothing here.",
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

# ---- premises on v6: kind, flags for C1..C9, and for the top five and P20 the best-supported alternative and its effect
LINEAGE = F / "main_case_lineage_2026_10_05/derived"
C = [f"C{i}" for i in range(1, 10)]
PREMISES = [
    ("P01", "Survey frame: CPS ASEC / ACS Mexican-origin self-ID and parental birthplace, 39.71M identified in three generations",
     "measured (survey)", "C1 C2 C3 C4 C5 C6 C7 C8 C9"),
    ("P02", "Removal counterfactual over one income year (2024), people alive in 2024, no lifetime", "convention", "C1 C2 C3 C4 C5 C6 C7 C8"),
    ("P03", "Service budgets and property-tax levies respond at long-run rates (schools 1, general government 0.60–0.85, roads/parks "
            "long run, property taxes at the receipt-side lane's central)", "assumed (cross-section slopes)", "C1 C2 C4 C5 C6 C8"),
    ("P04", "Return on public capital at 2–3%", "convention", "C1 C2 C4 C5 C6"),
    ("P05", "Social Security and Medicare Part A on accrual at payable benefits on the 2026 Trustees' separate funds, net of the "
            "income tax on benefits; public retiree health on accrual, its legacy at response 0 (v6's items 1 and 2)",
     "convention", "C1 C2 C4 C5 C6 C8"),
    ("P06", "Defense and existing interest at zero response", "assumed", "C1 C4 C5"),
    ("P07", "Allocation keys: CBO incidence, the IRS-matched income-tax key, use keys for justice and care, state price levels, "
            "roads by vehicle miles, user fees and the education keys by use (v6's item 4)", "convention + measured shares",
     "C1 C2 C3 C4 C6 C8"),
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
            "and priced at their measured ages (v6's item 3; v5 priced them at the identified G3+'s ages)",
     "modeled count (identity loss measured to G3) + convention (whole people)", "C1 C2 C4 C5 C6 C8"),
]
SWAP = {
    "P01": ("ACS level for the Mexico-born (CPS +9–13%, 209); NVSS births for the G2/G3 split (255)",
            "Not rerun on v6. On September 27: C1 −$2.2–2.5bn (−0.7%) [DATA: 209]; C2 ≈0 (removed people pay about what they "
            "cost, 209); C6 moves young children from G3+ to G2 [GAP]; C7 imputed unauthorized 4.57M → ~4.07M [GAP]; the rest "
            "< 1% [INFERENCE]. Breaks none [INFERENCE: v6's items and the lineage do not change the frame's weights]."),
    "P02": ("First-year budget horizon (ladder 229), with property levies fixed and roads keyed on resources",
            "C1 −26.5% BREAK ($288.9–336.5bn) [CALCULATION: c1_arms_oct07.csv]; C4 pairing about −21%, holds [INFERENCE: social "
            "rows held]; C2's tally has no services in it; C5, C6 and C8 not rerun on v6 [GAP]. Breaks one."),
    "P05": ("Cash, the September 27 convention (decision 2026-09-29, alternative 2)",
            "Restores C2: tally +$87.9 / 70.8bn, break-even 8.3–24.2% [CALCULATION: c2_tally_oct07.csv, c2_break_even_oct07.csv]. "
            "C1 −18.6% ($307.4–385.4bn), a break with no capital return (−30.0%) or first-year roads and parks (−28.0%); with "
            "schools at 0.836 it falls 0.05 points short (−24.95%) [CALCULATION: c1_min_cuts_oct07.csv]. C8 on cash: $419.6–425.9bn "
            "with white rates at the union's ages (−2.5% on the claim's $433.8bn) and $554.1–559.0bn against local whites (+5.0% on "
            "its $530.1bn), both inside a quarter; at whites' own ages $263.5–269.8bn (−38.5%), a break, the age artefact the "
            "accrual removes [FRAMING-SENSITIVE] [CALCULATION: white_replacement_2026_09_28 headline_oct07.csv]. C4 pairing "
            "$407.3–494.6bn (−14.9%) [DATA: sept24_propagation oct07]; C5 state-local share 68% → 82–87% [CALCULATION: debt lane "
            "split]; C6 every generation still costs others (at least $72.7bn; break-evens at most 42.2%) [CALCULATION: "
            "c6_generation_break_even_oct07.csv]. It breaks none at the union's ages; at whites' own ages it breaks C8 downward "
            "[FRAMING-SENSITIVE]. Scheduled benefits instead: C1 +9.9%, C2 tally −$37.1 / −45.8bn on the 2026 inputs, C5 about "
            "62%."),
    "P08": ("No corrections (v4's items, the lineage and v6's items on the uncorrected model, the union's pension switch rebuilt)",
            "C1 +2.5% ($399.6–472.5bn) [CALCULATION: c3_correction_split_oct07.csv]; C2 tally +$11.0 / −0.2bn: clause 1 holds at "
            "the low end and fails at the high end, as on the case, where on v5 the swap held it at both (+$11.1 / 0.4bn) "
            "[CALCULATION: c2_tally_oct07.csv]; C3 is this premise; C6 not split by generation [GAP]; C7 raw vs adjusted contrast "
            "changes direction (85). Breaks none."),
    "P03": ("Schools at the within-district 0.836 (the only within-unit estimate)",
            "C1 −6.4% ($361.3–434.9bn) [CALCULATION: c1_arms_oct07.csv]; property taxes at zero instead +7.0%; C2's tally has no "
            "services in it; C4 pairing about −5% [INFERENCE: social rows held]; C6 holds [INFERENCE]; C8 not rerun [GAP]. "
            "Breaks none."),
    "P20": ("The count's arms a and c (1.81M or 4.27M added); the added people at the identified G3+'s ages (v5's rule); as a "
            "framing, the ancestry-share count (29.9–35.1M people)",
            "Arms a / c: C1 −3.2% / +3.2%, C2's split by end holds (+$4.3 / −6.3bn and +$8.1 / −4.4bn) [CALCULATION: "
            "c1_arms_oct07.csv, c2_tally_oct07.csv]; C3 ± 1 SE ∓0.8% and the replacement child −2.1% (v5's change, not "
            "recomputed on v6) [FRAMING-SENSITIVE]; at the identified G3+'s ages C1 −0.5% (the age-mix item's +$1.35 / 2.86bn "
            "out), and at the item's cohort reading −1.8% [DATA: main_case_2026_10_07 summary.json]. Breaks none. By ancestry "
            "share: C1 −17.7% to −30.0%, a break at the stated bound's low end [FRAMING-SENSITIVE]; the per-member cost barely "
            "moves ($9,194–10,731 at the low end against $9,101–10,794) [DATA: summary.json v6.companions]. Breaks one, under that "
            "count only."),
}
for arm, lo, hi in [("school_within_district", 361.26, 434.91), ("pension_cash", 307.40, 385.36)]:
    check(f"{arm} low", num(arms[arm], "cost_low_bn"), lo, tol=0.005)
    check(f"{arm} high", num(arms[arm], "cost_high_bn"), hi, tol=0.005)
base = [num(split[("pension_rebuilt", e)], "v4_items_only_bn") for e in ENDS]
check("P08 swap low", base[0], 399.57, tol=0.005)
check("P08 swap high", base[1], 472.53, tol=0.005)
check("P08 swap move", 100 * (sum(base) / 2 / mid - 1), 2.5)
school_pair = [num(arms["school_within_district"], "cost_low_bn") - (num(arms["adopted"], "cost_low_bn") - footing[0]) + social[0],
               num(arms["school_within_district"], "cost_high_bn") + social[1]]
check("P03 swap pairing", 100 * (sum(school_pair) / 2 / pmid - 1), -5.0, tol=0.5)
summ = json.load(open(LANE / "summary.json"))
age_item = summ["change_at_fixed_specifications"]["items"]["added_age_mix"]["total"]
check("P20 the age-mix item, low", age_item[0], 1.35, tol=0.005)
check("P20 the age-mix item, high", age_item[1], 2.86, tol=0.005)
check("P20 at the identified G3+'s ages", -100 * sum(age_item) / 2 / mid, -0.5)
fr6 = summ["v6"]["companions"]["ancestry_share"]["set"]["rows"]
frac = next(r for r in fr6 if r["scenario"] == "g4_at_nothing")
for j, (k, want) in enumerate((("cost_low_bn", 9193.5), ("cost_high_bn", 10730.7))):
    got = num(arms["ancestry_share_low"], k) * 1e9 / frac["fractional_population"]
    check(f"P20 ancestry-share per member {k} (v6's row)", got, want, tol=0.5)
    check(f"P20 ancestry-share per member {k} is v6.companions'", got, frac["per_member_usd"][j], tol=0.5)
fr_pop = [r["fractional_population"] / 1e6 for r in fr6 if r["scenario"] in ("g4_at_nothing", "g4_at_bound")]
check("P20 ancestry-share population low", min(fr_pop), 29.9)
check("P20 ancestry-share population high", max(fr_pop), 35.1)
meta6 = json.load(open(LANE / "corrections.json"))["meta"]["lineage"]["counts"]
meta5 = json.load(open(F / "main_case_2026_10_05/derived/corrections.json"))["meta"]["lineage"]["counts"]
if meta6 != meta5:
    sys.exit("[BLOCKED] v6's lineage counts are not v5's; the text quotes v5's count")
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
with open(D / "conclusions_oct07.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    keys = ["id", "claim_tested", "status_on_v6", "deciding_premise", "reading_on_v6", "premises", "break_condition",
            "break_distance_note", "rival_reading", "discriminating_observation", "observed_yet", "source"]
    w.writerow(keys)
    for c in CONCLUSIONS:
        w.writerow([c[k] for k in keys])
with open(D / "common_mode_oct07.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["premise_id", "premise", "kind", *C, "n_conclusions", "rank", "best_supported_alternative", "effect_if_swapped"])
    for pid, text, kind, flags in order:
        alt, eff = SWAP.get(pid, ("", ""))
        w.writerow([pid, text, kind, *flags, sum(flags), rank[pid], alt, eff])
broken = [c["id"] for c in CONCLUSIONS if c["status_on_v6"].startswith("BREAKS")]
print(f"  ✓ conclusions_oct07.csv: {len(CONCLUSIONS)} rows, broken at the central: {', '.join(broken)}; "
      f"common_mode_oct07.csv: {len(PREMISES)} premises; top five {', '.join(top)}")

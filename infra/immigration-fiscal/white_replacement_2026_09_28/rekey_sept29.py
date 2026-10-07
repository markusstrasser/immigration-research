"""The white replacement comparison on the v4 case adopted 2026-09-29 (case key sept29), both sides on the 39,712,493
people the account prices; also the library the Black lane's rekey_sept29.py imports. Not the engine.

The September 27 outputs of this lane stay as they are. Here rekey_white.py and state_white.py are imported (their
module-level builds read files and write nothing) and their CPS frame is moved to audit row 4's weights, as
population_basis_2026_09_29/white_count.py did for ladder 274: the engine's row-4 factors on the Mexico-born outside
California and Texas, the frame totals recomputed, and every white slice scaled to 39,712,493.

Inputs: derived/engine_lines_sept29.json (the case at specs 48 / 11, methods averaged) and engine_lines_sept29_cash.json
(its cash set, the pension switch off), both from engine_lines.cjs; the case's payload meta
(main_case_2026_09_29/derived/corrections.json); derived/accrual_ratios.csv (accrual_white.py), the Black lane's
derived/accrual_ratios.csv (accrual_black.py: NH Black and all residents); derived/v4_state_relatives.csv and v4_nhts_vmt.csv (v4_inputs.py).

Rules on the sept29 case (each is stated with its alternative in RESULT.md, section "v4 case (sept29)"):
  1. Lines, responses, capital stocks and rates are the case's. Group shares are the rough keys of September 27. The
     Mexican-origin rough run keeps the engine's medical and justice shares, read from the cash set, because the
     accrual set's Medicare amount already carries the accrual.
  2. The two receipt lines v4 splits out: housing_enterprise_surplus (public housing's operating deficit) is keyed on
     housing subsidies, as the case keys it on housing support; tenant_occupied_property on renters' consumption
     (cash renters, H_TENURE 2, household income^0.7), because the CPS has no rent paid. Public housing's capital
     (ent_housing_sl) is keyed on housing subsidies, as in the case.
  3. Accrual basis (the case's central): the case's pension rule for every group at the group's own accrual per tax
     dollar. Social Security = the net OASDI ratio x the group's OASDI taxes (employee + employer + the case's SE share
     of self-employment tax); Medicare swaps the Part A share of its cash amount for the Part A ratio x the group's HI
     taxes; federal income tax loses the tax on the group's 2024 benefits (the case's receipt per benefit dollar per
     unit of relative rate x the group's relative rate x its benefits). The union takes the case's own ratios.
     Cash basis: the cash set, the rule off.
  4. State prices (item 9) and road miles (item 10) for every group from its own residence and driving:
       state_price_<line> = sum over the line's S&L functions of amount x (group index - 1) x the group's key share
       general sales tax x the group's sales index; licences = national x miles share x the group's licence index
       roads_vmt_<part> = highway national x (k_road - the earnings key the re-key gives economic affairs)
       k_road = passenger share x miles share + (1 - passenger share) x the consumption key; highway capital at k_road
       gasoline taxes move by gasoline national x (miles share - the consumption key)
     Indexes weight the state relatives by the group's CPS persons (licences: adults; corrections: persons x the
     state's imprisonment rate), as the state lane weights the union's. Miles share: the union's is the case's formula
     (p (1 - u5) rho over its denominator); another group's is p (1 - u5) rho_g over the same denominator, rho_g its
     NHTS 2017 driver miles per person aged 5+ at its own age structure over the non-Hispanic average. Union pieces
     split the union's miles share by persons aged 5+, and its per-prisoner corrections premium by where its prisoners
     are (persons x the state's imprisonment rate, the union index's weights), so that the pieces add to the union.
  5. The engine's union-only corrections stay as on September 27: school reprice, college re-key and lane constants at
     the engine's amounts for the union and none for other groups; the production gain for the union only; items 3
     (IRS key), 6a (payroll compliance) and 7 (workers' compensation key) refine the engine's union keys and have no
     counterpart in the rough CPS keys, which every group shares.

The v5 case adopted 2026-10-05 (--case oct05, main_case_2026_10_05) adds 3,039,720 descendants who no longer report
Mexican origin, so the CPS keys cannot see them. Both sides go on the lineage's 42,752,213, as the case lane's Consumers
row describes:
  - the union's side is the rough union on the identified 39,712,493 at v5's responses (engine_lines.cjs oct05_union
    dumps: the base's v4 models plus audit row 8's change, at v5's specifications), plus the added people at the case
    lane's own amounts: the case's dump less the union dump on every line, with their capital return and production
    term. The pension rule is not applied to them (their accrual is the lane's, 0.9487 per OASDI dollar);
  - every scaled slice (A1, A2, A3, A4, the all-residents slice) is on 42,752,213. A3's union ages are the lineage's: the
    union's, with the added people at the identified G3+ members' ages, as the lineage lane prices them [ASSUMPTION].
    The NH Black group keeps its own count;
  - the state arm gives each union piece the added people's cost in proportion to its share of the identified G3+
    persons, and its white pieces the piece's lineage count and ages [ASSUMPTION: they live where the identified G3+ do];
  - the attribution runs steps 1-3 on the identified union at v5's responses, every slice on 39,712,493; step 4 adds the
    lineage on both sides. headline_oct05.csv gives each figure on 42,752,213 beside the same comparison on the
    identified 39,712,493 at v5's responses and the sept29 value.
Outputs carry the case key (rekey_summary_oct05.csv, ...). The oct05 gates: the union dumps are the September 29 case
plus the union's response move, and the case less them is the lane's added people (summary.json
change_at_fixed_specifications, 1e-9); the payload's pension, state-price and road meta are the September 29 payload's;
the frame's identified G3+ is the lineage's count (1 person); step 4 moves the union by the added people, the NH Black
group not at all and every slice at fixed ages by 42,752,213 / 39,712,493 (1e-9 relative).

The v6 case adopted 2026-10-07 (--case oct07, main_case_2026_10_07) is v5 plus the items its payload's meta.items
lists. The oct05 rules carry over, with these for the items (RESULT.md, section "v6 case (oct07)"):
  - the union dumps (engine_lines.cjs oct07_union) carry every edit set's union part, so the case less them is the
    added people's on every line: their measured age mix (the lineage item) and the edit sets' lineage parts;
  - the pension accrual (item 1) is the case's rule on the 2026 Trustees' separate-funds path for every group: the
    union at the case's ratio_net and Part A accrual, the other groups at their own ratios on that path
    (accrual_ratios_oct07.csv of this lane and of the Black lane: accrual_white.py and accrual_black.py --case oct07);
  - an edit set's national-scale edits (item 2) reach every group through the national totals the rough keys share;
    its union-only cell shifts stay the union's, as rule 5's union-only corrections do;
  - A3's union ages put the added people at their measured age mix (meta.lineage.age_mix): each identified G3+
    record's weight is tilted by its band's measured over identified share, which is v5's placement at the identified
    mix. The state arm keeps each piece's added count (its share of the identified G3+) and tilts its ages the same
    way [ASSUMPTION].
The oct07 gates (items_gates), beside the oct05 ones: the payload's meta is v5's but for what its items change, the
lineage's counts and the pension rule's other inputs are v5's; on each basis and end the union dump is the oct05 union
dump plus the edit sets' union parts (summary.json change_at_fixed_specifications.items, their cash blocks) plus its
capital return's move, and the case less it is v5's added people plus the lineage item, the edit sets' lineage parts and
the lineage item's interactions (1e-9); the accrual files' union is the case's 2026 arm; the frame's identified G3+
ages are the age-mix lane's identified mix, exactly. headline_oct07.csv carries the oct05 figures beside.

The IPEDS keys (ipeds_keys.py -> derived/ipeds_keys.json; a defect fix decided in the v6 propagation, 2026-10-07).
On v5 and v6 (IPEDS_CASES), every group, the rough union too, takes Pell ($31.264bn) out of other_federal_benefits'
Social Security key at its share of Pell. It takes the higher-education part of education_services (the fee lane's
consolidated weight, 0.1916 of the line) and of the college capital stock (kappa, 0.961) at its share of public higher
education's measured use, in place of the CPS college key. A group takes its race's IPEDS share by its CPS college key
(use, tuition) or its low-income college key (Pell) over its race's [ASSUMPTION]; the union takes the fee lane's
shares. On v6 (FEE_CASES) item 4's tuition term is added on both sides, and its hospital term is priced beside:
  - tuition: the tuition each group pays short of its use, (use - tuition share) x NIPA tuition, on the education line;
  - hospital charges, beside the central (HOSPITAL_ON, the team lead's decision of 2026-10-07): for a group with MEPS
    keys, public hospitals' insured net at its MEPS shares of hospital payments by payer less its health key, on
    health_services. Its fee side would take MEPS payer shares while the group's hospital spending stays on the OTHPUB
    key, so ipeds_terms_<case>.csv prints it beside (hospital_beside_bn) and no central cost carries it. The union's
    term is in the engine's health share it takes (rule 1), as before.
sept29 keeps the September 27 keys, because lanes outside this one gate against its outputs.
ipeds_terms_<case>.csv gives each group's cost on the rough keys and each part's move, gated to add up.

The case's own income-tax keys (round 2, the team lead's instruction of 2026-10-07, approved by the operator). On v5
and v6 (TAX_CASES) every group, the rough union too, takes its income taxes on the keys the case gives the union, so
the CPS-dollar rule (a group charged the income tax it reports to the CPS, the top tail the survey misses charged to
no one) retires as the central:
  - federal_income_tax: v4 item 3's key (tax_key_heldout_2026_09_28, irs_2023_raked_with_cbo_groups): the
    federal_liability key's dollars (CPS FEDTAX_BC, tax after nonrefundable and before refundable credits) in each CBO
    income group x pooled AGI bin cell (14 cells a group), the cells raked to CBO's 2022 group shares of individual
    income tax and IRS's TY2023 shares of income tax after credits by AGI bin. A group's share is the sum over cells
    of the raked cell total x the group's part of the cell's key dollars;
  - state_local_income_tax and other_personal_tax: the state_liability key (STATETAX_A floored at 0). Other personal
    tax moves from the federal key to the state key, as the case keys it;
  - the allocation is the shared one (the SPM unit's tax split equally over its members), at both ends; the rough
    keys already split tax over the tax unit, so the personal allocation would add a second change. Each group's
    shares at both allocations are in income_tax_keys_<case>.csv;
  - the key is built on the published weights, as the case builds it, and normalized on the frame's weights as every
    rough key is. No group takes a union-only correction (rule 5): item 3 is now every group's key, not the union's.
The old rules are arms in the same files: cost_cps (the CPS-dollar rule) and cost_top_tail_proportional (CPS
income-tax dollars spread over the national line in proportion). cost_capital_taxes_respond is the central with the
capital-side lines at 1; the top tail is inside the central, so cost_both_arms is that column. The attribution's steps
1-4 keep the CPS-dollar rule and step 5 moves every group to the case's keys. cps_tax_totals_<case>.csv gives the
CPS's federal and state income-tax dollars against the national lines on the published and row-4 weights (the rough
re-key's frame), each row naming its variable, its placement (on the record or split over the tax unit) and its key.
income_tax_parts.py splits the move from the CPS-dollar rule to the case's keys into its parts.
Gates (case_tax_keys()): the benchmark lane's frame (external_benchmarks_2026_09_24, FEDTAX_BC, AGI and the CBO income
fields) is the rough frame row for row; IRS's bin shares are heldout's bins.csv (1e-12); the union's raked shares are
heldout's translation, its reweighted share plus the raked share change, at both allocations, and each vector sums
to 1 over civilians (1e-12); the union's unraked federal and state shares are model.json's cells (1e-9). The
attribution gates each group's step-5 change to minus its change in the three income-tax lines (1e-9).

Gates (exit 1, nothing written):
  - the dumps are the case: their costs are main_case_bands.csv's adopted and cash_set rows (5e-5, printed at 4
    decimals), and the lane's cost formula on the engine's amounts reproduces each dump's cost (1e-9);
  - the case's pension rule, applied to the engine's cash-set union amounts, gives the accrual set's Social Security,
    Medicare and federal income tax amounts (1e-9), and the state lane's indexes give the payload's national gaps (1e-6);
  - every line of the case is keyed: no line with a national of 0 and an amount is left at 0, no line lacks a key;
  - on the published weights and the September 27 dump, the library reproduces the lane's rekey_summary.csv costs
    (1e-9); on row-4 weights it reproduces population_basis_2026_09_29/derived/white_count.csv's row-4 costs and
    state deltas (1e-3, its printed precision); the row-4 union matches frame_counts.csv (2 persons);
  - the union's pieces sum to the rough union within $1bn (the residual is spread by persons, as state_white.py does).
Beside the rules: rule_alternatives_sept29.csv prices each designed rule's alternative (rule 2: the two receipt lines at
the keys of the lines they were split from; rule 3a: every group at the union's accrual per tax dollar; rule 3b: the
tax on benefits at the case's rule for each end; rule 4: other groups at national prices and the September 27 road
keys), and attribution_sept29.csv walks each group from the September 27 case (published, then row-4 weights) through
the sept29 cash set without and with rule 4 to the case with the accrual.
Outputs: derived/rekey_summary_sept29.csv, rekey_buckets_sept29.csv, state_summary_sept29.csv,
state_buckets_sept29.csv, headline_sept29.csv, v4_group_terms_sept29.csv, rule_alternatives_sept29.csv,
attribution_sept29.csv, attribution_buckets_sept29.csv. Run from the repository root after engine_lines.cjs sept29 / sept29_cash, accrual_white.py,
v4_inputs.py and the Black lane's accrual_black.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/rekey_sept29.py
and, after engine_lines.cjs oct05 / oct05_cash / oct05_union / oct05_union_cash, the same with --case oct05; after
engine_lines.cjs oct07 / oct07_cash / oct07_union / oct07_union_cash and accrual_white.py and accrual_black.py
--case oct07, the same with --case oct07 (after the oct05 run, whose headline it reads).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
import zipfile
from contextlib import ExitStack, contextmanager
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
sys.path.insert(0, str(LANE))
import rekey_white as R  # noqa: E402
import state_white as S  # noqa: E402
import v4_inputs as V  # noqa: E402
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import combine_onbooks_lane as L  # noqa: E402

BLACK_LANE = FISCAL / "black_comparator_rough_2026_09_28"
BASIS = FISCAL / "population_basis_2026_09_29/derived"
ENDS = ("low", "high")
BASES = ("accrual", "cash")
DUMP27 = R.case
# The cases this library re-keys, by key: the case lane. Outputs carry the key (rekey_summary_<case>.csv, ...).
# oct05 (v5) is the September 29 rules on the identified union at v5's responses, plus the lineage (see use_case()).
CASES = {"sept29": "main_case_2026_09_29", "oct05": "main_case_2026_10_05", "oct07": "main_case_2026_10_07"}
LINEAGE_CASES = ("oct05", "oct07")
# The accrual ratios each case reads (rule 3): sept29 and oct05 on the 2025 Trustees Reports, oct07 on the 2026
# separate-funds path (accrual_white.py and the Black lane's accrual_black.py, --case oct07).
ACCRUAL_FILES = {"sept29": "accrual_ratios.csv", "oct05": "accrual_ratios.csv", "oct07": "accrual_ratios_oct07.csv"}
# The IPEDS keys (module docstring): the cases that take them, and those that also take item 4's fee terms.
IPEDS_CASES = ("oct05", "oct07")
FEE_CASES = ("oct07",)
IPEDS_LINES = ("other_federal_benefits", "education_services")
# A scenario's race for the IPEDS keys, by its name (an importer adds its groups), and each race's CPS persons
IPEDS_RACE = {"mex": "union", "union_piece": "union", "w3": "white", "wus": "white", "wall": "white", "blk": "black",
              "avg": "all"}
IPEDS_MASK = {"white": "wall", "black": "blk", "all": "avg"}
V4_SPEND = ["roads_vmt_sl", "roads_vmt_fed", "state_price_public_order_safety", "state_price_health_services",
            "state_price_recreation_culture"]
SP_FUNCTIONS = V.CENTRAL                      # the state lane's central package, by parent line
SL_AMOUNT = pd.read_csv(FISCAL / "state_priced_services_2026_09_29/derived/corrections.csv").set_index("function").sl_amount_bn
NEW_RECEIPTS = {"housing_enterprise_surplus": "house", "tenant_occupied_property": "rent"}
# Rule 2's alternative: the rough keys of the lines v4 split them from (enterprise_surplus, remaining_production_property)
PARENT_KEYS = {"housing_enterprise_surplus": "pc", "tenant_occupied_property": "capinc"}
BENEFIT_TAX_RULE = "shared"   # rule 3: the shared rule at both ends; "by_end" (rule 3b's alternative): the case's per end
REL_UNION = 0.5233824966647924     # the union's measured relative benefit-tax rate (pension lane, accrual_white.py)
# Round 2 (2026-10-07): the cases whose central keys every group's income taxes on the case's own keys (module
# docstring), the allocation the comparators take, and each income-tax line's key
TAX_CASES = ("oct05", "oct07")
TAX_ALLOC = "shared"
CASE_TAX_KEY = {"federal_income_tax": "fit_case", "state_local_income_tax": "sit_case", "other_personal_tax": "sit_case"}
HELD = FISCAL / "tax_key_heldout_2026_09_28"
BENCH = FISCAL / "external_benchmarks_2026_09_24"
CBO_SPEC = "individual_inc_tax=individual_inc_tax_gross|2022"    # the CBO margin heldout.py rakes to
TAX_COLS = ["PH_SEQ", "TAX_ID", "SPM_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "PRDTHSP", "pwwgt0", "AGI", "FEDTAX_BC", "FEDTAX_AC", "STATETAX_A", "WSAL_VAL", "PTOTVAL", "SSI_VAL", "PAW_VAL",
            "CAP_VAL", "MCARE"]
TAX_K: dict = {}     # the case's key vectors on the rough frame's rows (case_tax_keys()), added to R.K on TAX_CASES


def use_case(case):
    """Point the library at a case: its dumps, payload meta and bands. sept29 at import; an importer that re-keys
    another case calls this before setup(). For oct05 DUMP holds the identified union at v5's responses (the
    engine_lines.cjs oct05_union dumps: the 39.71M the CPS keys see), FULL the case itself, and LIN the added people's
    part of every line, of the capital return and of the production term (FULL less DUMP)."""
    global CASE, CASE_LANE, DUMP, FULL, LIN, LINEAGE, META, PA, SPM, RD, BANDS, ORACLE, SP_LINES, FP, U5, RHO, GAS, LIC
    global HWY_N, SE_SHARE, PART_A_SHARE, STEPS, LINEAGE_ON, UNION_LINES, ITEM_COMPONENTS, IPEDS_ON, FEES_ON, IK
    global TAX_ON, BOTH_TOP, FINAL_STEPS
    if case not in CASES:
        raise SystemExit(f"[BLOCKED] unknown case {case!r}: one of {', '.join(CASES)}")
    CASE, CASE_LANE = case, FISCAL / CASES[case]
    stem = "engine_lines_" + case + ("_union" if case in LINEAGE_CASES else "")
    DUMP = {"accrual": json.loads((DER / f"{stem}.json").read_text()), "cash": json.loads((DER / f"{stem}_cash.json").read_text())}
    META = json.loads((CASE_LANE / "derived/corrections.json").read_text())["meta"]
    PA, SPM, RD = META["pension_accrual"], META["state_pricing"], META["roads_mileage_key"]
    BANDS = (pd.read_csv(CASE_LANE / "derived/main_case_bands.csv").query("profile == 'long_run_non_school_full'")
             .set_index("variant"))
    ORACLE = {"accrual": tuple(BANDS.loc["adopted", ["cost_low_bn", "cost_high_bn"]]),
              "cash": tuple(BANDS.loc["cash_set", ["cost_low_bn", "cost_high_bn"]])}
    SP_LINES = {x["line"]: x for x in SPM["lines"]}
    FP, U5, RHO = RD["passenger_share"], RD["under5_share"], RD["rho"]
    GAS, LIC, HWY_N = RD["gasoline_bn"], RD["licences_bn"], RD["highway_national_bn"]
    SE_SHARE, PART_A_SHARE = PA["se_oasdi_share"], PA["part_a_share"]
    # oct07: a union-only item's carrier receipt lines join rule 5's union-only lines, and its capital offset components
    # (by the component each offsets) follow rule 5 too: see run29.
    applied = [r for r in META.get("items", []) if r.get("applied") and r.get("capital")]
    UNION_LINES = R.ADJUST | {lid for r in applied for lid in r["capital"]["receipt_lines"]}
    of = {c["id"]: c.get("of_component") for c in META["capital_return"]["components"]} if applied else {}
    ITEM_COMPONENTS = {cid: of[cid] for r in applied for cid in r["capital"]["components"]}
    if any(v is None for v in ITEM_COMPONENTS.values()):
        raise SystemExit("[BLOCKED] an item's capital component does not name the component it offsets")
    STEPS = STEPS_SEPT29
    FULL = LIN = LINEAGE = None
    LINEAGE_ON = False
    if case in LINEAGE_CASES:
        FULL = {"accrual": json.loads((DER / f"engine_lines_{case}.json").read_text()),
                "cash": json.loads((DER / f"engine_lines_{case}_cash.json").read_text())}
        LINEAGE = META["lineage"]
        LIN = {b: {end: lineage_part(FULL[b][end], DUMP[b][end]) for end in ENDS} for b in BASES}
        STEPS = STEPS_SEPT29[:2] + (STEPS_IDENTIFIED_V6 + [STEP_LINEAGE_V6] if "items" in META
                                    else STEPS_IDENTIFIED + [STEP_LINEAGE])
        LINEAGE_ON = True
    IPEDS_ON, FEES_ON = case in IPEDS_CASES, case in FEE_CASES
    IK = json.loads((DER / "ipeds_keys.json").read_text()) if IPEDS_ON else None
    if IPEDS_ON:     # step 1 leaves the September 27 dump, and its keys, for the case's
        STEPS = [(s, t + (IPEDS_STEP_FEES if FEES_ON else IPEDS_STEP) if s == "1" else t, b) for s, t, b in STEPS]
    # Round 2: the case's income-tax keys are the central (top "case"); the earlier steps keep the CPS-dollar rule, and
    # the last step moves every group to the case's keys. On those keys the top tail is inside the central, so the
    # both-arms reading is the capital arm on the central.
    TAX_ON = case in TAX_CASES
    BOTH_TOP = None if TAX_ON else "prop"
    for k in ("fit_case", "sit_case", "fit_case_personal", "fit_case_shared", "sit_case_personal", "sit_case_shared"):
        R.K.pop(k, None)
    if TAX_ON:
        STEPS = STEPS + [STEP_TAX]
    FINAL_STEPS = ({"5": "accrual"} if TAX_ON else {"4": "accrual"} if LINEAGE_ON else {"2": "cash", "3": "accrual"})


def lineage_part(full, union):
    """The added people's part of a case dump at one end: every line's amount, the capital return and the production
    term, full less union. The two dumps must share every line, national and response."""
    fl = [x for x in full["lines"] if x["side"] != "scalar"]
    ul = [x for x in union["lines"] if x["side"] != "scalar"]
    if [(x["side"], x["id"]) for x in fl] != [(x["side"], x["id"]) for x in ul]:
        raise SystemExit("[BLOCKED] the case and union dumps do not have the same lines")
    for a, b in zip(fl, ul):
        if a["national_bn"] != b["national_bn"] or a["response"] != b["response"]:
            raise SystemExit(f"[BLOCKED] {a['side']}|{a['id']}: the case and union dumps differ in national or response")
    if full["spec"] != union["spec"] or full["rate"] != union["rate"]:
        raise SystemExit("[BLOCKED] the case and union dumps are not at the same specification")
    prod = lambda e: next(x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn")["effect_bn"]  # noqa: E731
    return {"lines": {a["side"] + "|" + a["id"]: a["amount_bn"] - b["amount_bn"] for a, b in zip(fl, ul)},
            "capital_bn": full["capital_bn"] - union["capital_bn"], "production_gain_bn": prod(full) - prod(union),
            "cost_bn": full["cost_bn"] - union["cost_bn"]}
CAP29 = {**R.CAP_LINES, "tenant_occupied_property": "rent"}   # the capital-side arm: every capital-side line at 1
BUCKETS = {k: list(v) for k, v in R.BUCKETS.items()}
BUCKETS["capital, property, production taxes"] += list(NEW_RECEIPTS)
BUCKETS["police, courts, prisons"].append("state_price_public_order_safety")
RACE_RATES = {"w3": "nh_white", "wus": "nh_white", "wall": "nh_white", "blk": "nh_black", "avg": "all"}
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def stop_if_failed():
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)


# ------------------------------------------------------------------ keys the rough frame lacks
with zipfile.ZipFile(R.ZIP) as _z:
    _hh = pd.read_csv(_z.open("hhpub25.csv"), usecols=["H_SEQ", "H_TENURE"]).rename(columns={"H_SEQ": "PH_SEQ"})
_ten = R.d[["PH_SEQ"]].merge(_hh, on="PH_SEQ", how="left", validate="many_to_one").H_TENURE.to_numpy()
if np.isnan(_ten.astype(float)).any():
    raise SystemExit("[BLOCKED] CPS persons without a household tenure")
R.K["rent"] = R.K["cons"] * (_ten == 2)        # cash renters' consumption: the renter-rent proxy
_keyed27 = R.keyed


def _keyed_meps(g, cw, total, ages, mwt=None):
    """rekey_white.keyed, keeping the group's MEPS weights on its scenario (the hospital term reads them)."""
    sc = _keyed27(g, cw, total, ages, mwt)
    if mwt is not None:
        sc["meps_w"] = mwt
    return sc


R.keyed = _keyed_meps       # R.scenario and state_white.white_piece look it up at call time
R.KTOT["rent"] = float((R.w * R.K["rent"]).sum())
_line_share27 = R.line_share


def _line_share_case(sc, side, lid, top="cps"):
    """rekey_white.line_share, and top 'case' (round 2): the income-tax lines at the case's own keys (CASE_TAX_KEY),
    every other line as before."""
    if top == "case":
        if side == "receipts" and lid in CASE_TAX_KEY:
            return sc["share"][CASE_TAX_KEY[lid]]
        top = "cps"
    return _line_share27(sc, side, lid, top)


R.line_share = _line_share_case     # run29 and v4_terms look it up at call time


# ------------------------------------------------------------------ round 2: the case's income-tax keys
def irs_2023():
    """IRS SOI TY2023 Table 1.2, income tax after credits by its 19 AGI bins, from the held-out lane's read of the
    table (reads/irs_table_1_2_ty2023.md; its _cache spreadsheet is not on this machine): bin labels and shares."""
    txt = (HELD / "reads/irs_table_1_2_ty2023.md").read_text()
    rows = re.findall(r"^\| ([^|]+?) \| ([\d,]+) \| ([\d,]+) \| [\d.]+% \|$", txt, re.M)
    total = float(re.search(r"All returns, total \(row 9\) \| \| ([\d,]+) \|", txt).group(1).replace(",", ""))
    amounts = np.array([float(r[2].replace(",", "")) for r in rows])
    if len(rows) != 19 or abs(amounts.sum() - total) > 1e-7 * total:
        raise SystemExit("[BLOCKED] the IRS TY2023 read does not give 19 bins adding to its total")
    return [r[0] for r in rows], amounts / amounts.sum()


def _pool14(x):
    """heldout.py's 14 raking columns from 19 bins: no AGI with $1-5k, the bins to $1M, $1M and up pooled."""
    p = np.concatenate([x[:14], x[14:].sum(axis=0, keepdims=True)])
    return np.concatenate([p[:2].sum(axis=0, keepdims=True), p[2:]])


def raked_vector(d, w, civ, g, alloc, cbo, cols, edges):
    """Each person's share of national federal income tax under v4 item 3's key (tax_key_heldout_2026_09_28,
    irs_2023_raked_with_cbo_groups) on weights w: the key's dollars (FEDTAX_BC on the record, or split equally over the
    SPM unit) in CBO income group j x AGI bin k, the cells raked to CBO's group shares and IRS's bin shares, and a
    person's share sum_k R[j, k] x its dollars in (j, k) / the cell's dollars. Sums to 1 over civilians."""
    vp = d.FEDTAX_BC.to_numpy(float)
    agi = d.AGI.to_numpy(float)
    b = np.where(agi <= 0, 0, np.searchsorted(edges, agi, side="right") + 1)
    codes, _ = pd.factorize(d.SPM_ID.to_numpy())
    size = np.bincount(codes).astype(float)
    m = np.zeros((len(d), 19))
    for k in range(19):
        x = vp * (b == k)
        m[:, k] = x if alloc == "personal" else (np.bincount(codes, weights=x) / size)[codes]
    m14 = _pool14(m.T).T
    pos = [j for j in cbo if cbo[j] > 0]
    tb = np.stack([m14[civ & (g == j)].T @ w[civ & (g == j)] for j in pos])
    rows = np.array([cbo[j] for j in pos])
    r = rows[:, None] * tb / tb.sum(axis=1, keepdims=True)
    for it in range(20000):
        r *= cols[None, :] / r.sum(axis=0)[None, :]
        r *= (rows / r.sum(axis=1))[:, None]
        if max(np.abs(r.sum(axis=0) - cols).max(), np.abs(r.sum(axis=1) - rows).max()) < 1e-12:
            break
    else:
        raise SystemExit(f"[BLOCKED] the {alloc} raking did not converge")
    ratio = np.divide(r, tb, out=np.zeros_like(r), where=tb > 0)
    v = np.zeros(len(d))
    for i, j in enumerate(pos):
        mj = civ & (g == j)
        v[mj] = m14[mj] @ ratio[i]
    return v, it + 1


def case_tax_keys():
    """Round 2: the case's income-tax keys as per-person vectors on the rough frame's rows. federal_income_tax: v4 item
    3's IRS-raked key at each allocation (raked_vector on the published weights, pwwgt0, as heldout.py rakes it);
    state_local_income_tax and other_personal_tax: the state_liability key (STATETAX_A floored at 0 on the record, or
    split equally over the SPM unit). The CPS fields the rough frame lacks come from the benchmark lane's frame
    (external_benchmarks_2026_09_24/frame.py, its cached parquet; loaded under its own name, as cbo_arm.groups builds
    the CBO groups). Gates: that frame is the rough frame row for row; IRS's bin shares are heldout's bins.csv; the
    union's raked shares are heldout's translation (reweighted share + the raked share change) at both allocations and
    the vectors sum to 1 over civilians (1e-12); the unraked federal and state shares of the union are model.json's
    cells (1e-9, printed to 9 decimals). Returns the vectors and the frame's FEDTAX_BC and STATETAX_A for the totals."""
    spec = importlib.util.spec_from_file_location("benchmark_frame", BENCH / "frame.py")
    bf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bf)
    path = bf.CACHE / "cps25_frame.parquet"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path} (external_benchmarks_2026_09_24 frame.load() builds it)")
    d = pd.read_parquet(path, columns=TAX_COLS)
    same = len(d) == len(R.d) and all(np.array_equal(d[c].to_numpy(), R.d[c].to_numpy()) for c in
                                      ("PH_SEQ", "TAX_ID", "SPM_ID", "MARSUPWT", "A_AGE", "PRCITSHP", "PENATVTY",
                                       "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "FEDTAX_AC", "STATETAX_A"))
    gate("the benchmark frame is the rough frame row for row (household, tax and SPM unit, weight, age, origin, taxes)", same)
    if not same:
        stop_if_failed()
    civ, union = bf.masks(d)
    gate("its civilian universe and union are the rough frame's", np.array_equal(civ, R.civ)
         and np.array_equal(union, R.MASK["mex"] & R.civ))
    w0 = d.pwwgt0.to_numpy(float) * civ
    labels, irs = irs_2023()
    bins = pd.read_csv(HELD / "derived/bins.csv")
    gate("IRS TY2023 bin shares are heldout's bins.csv (1e-12)", list(bins.irs_label) == labels
         and float(np.abs(bins.irs_2023_share_pct.to_numpy() / 100 - irs).max()) < 1e-12)
    lows = [int(re.match(r"\$([\d,]+) (?:under|or more)", lab).group(1).replace(",", "")) for lab in labels[1:]]
    edges = np.array(lows[1:], float)
    shares = pd.read_csv(BENCH / "derived/cbo_group_shares.csv").query("spec == @CBO_SPEC").set_index("group")
    cbo = {j: float(shares.loc[j, "cbo_share"]) for j in bf.GROUPS}
    medicare = next(x for x in bf.model()["spending"]["lines"] if x["id"] == "medicare")["national_bn"]
    per = medicare * 1e9 / d.pwwgt0.to_numpy(float)[d.MCARE.eq(1).to_numpy()].sum()
    g, _ = bf.cbo_groups(d, bf.cbo_income(d, per), d.pwwgt0.to_numpy(float))    # cbo_arm.groups(d)
    held = json.loads((HELD / "derived/translation_inputs.json").read_text())
    model = {x["id"]: x for x in bf.model()["receipts"]["lines"]}
    cell = lambda lid, a: model[lid]["cells"]["cbo_collective"][a]["share"]  # noqa: E731
    out = {}
    stl = d.STATETAX_A.clip(lower=0).to_numpy(float)
    for a in ("personal", "shared"):
        v, iters = raked_vector(d, w0, civ, g, a, cbo, _pool14(irs), edges)
        want = held["reweighted_share"][a] + held["share_change"]["irs_2023_raked_with_cbo_groups"][a]
        got = float(w0[union] @ v[union])
        gate(f"federal, {a}: the union's raked share is heldout's translation, the vector sums to 1 (1e-12; {iters} "
             "iterations)", abs(got - want) < 1e-12 and abs(float(w0 @ v) - 1) < 1e-12, f"{got:.15f} vs {want:.15f}")
        raw = d.FEDTAX_BC.to_numpy(float)
        raw = raw if a == "personal" else bf.unit_equal(raw, d.SPM_ID.to_numpy())
        st = stl if a == "personal" else bf.unit_equal(stl, d.SPM_ID.to_numpy())
        f_u, s_u = float(w0[union] @ raw[union] / (w0 @ raw)), float(w0[union] @ st[union] / (w0 @ st))
        gate(f"federal and state, {a}: the union's unraked shares are model.json's federal_liability and state_liability "
             "cells (1e-9)", abs(f_u - cell("federal_income_tax", a)) < 1e-9 and abs(s_u - cell("state_local_income_tax", a)) < 1e-9
             and cell("other_personal_tax", a) == cell("state_local_income_tax", a), f"{f_u:.9f}, {s_u:.9f}")
        out[f"fit_case_{a}"], out[f"sit_case_{a}"] = v, st
    out["fit_case"], out["sit_case"] = out[f"fit_case_{TAX_ALLOC}"], out[f"sit_case_{TAX_ALLOC}"]
    return out, d.FEDTAX_BC.to_numpy(float)


OLD_TAX_KEY = {"federal_income_tax": "fit", "state_local_income_tax": "sit", "other_personal_tax": "fit"}
CASE_KEY_LABEL = {"fit_case": "federal_liability raked to IRS 2023 and CBO 2022 (v4 item 3)", "sit_case": "state_liability"}


def tax_key_rows(groups):
    """TAX_CASES: rows of income_tax_keys_<case>.csv for the groups (label -> scenario; 'eng' skipped): each income-tax
    line's share and amount at the key (before the accrual basis takes the tax on benefits) under the central, each
    allocation of the case's key, and the rough keys' 'prop' and 'cps' rules, with the group's CPS dollars on each
    key's base: the case key's (FEDTAX_BC, or STATETAX_A floored at 0, on the record) and the rough key's (the tax-unit
    split of FEDTAX_AC or STATETAX_A, floored at 0; other personal tax was on the federal one)."""
    rows = []
    for lab, sc in groups.items():
        if sc == "eng":
            continue
        cw = sc["cps_w"]
        base = {"fit_case": float(cw @ TAX_K["_fedtax_bc"]) / 1e9, "sit_case": float(cw @ TAX_K["sit_case_personal"]) / 1e9}
        for lid, key in CASE_TAX_KEY.items():
            nat = R.NATIONAL["receipts|" + lid]
            sh = {"central": R.line_share(sc, "receipts", lid, "case"), "personal": sc["share"][key + "_personal"],
                  "shared": sc["share"][key + "_shared"], "prop": R.line_share(sc, "receipts", lid, "prop"),
                  "cps": R.line_share(sc, "receipts", lid, "cps")}
            rows.append({"case": CASE, "group": lab, "population": f"{sc['population']:.0f}", "line": lid,
                         "national_bn": f"{nat:.4f}", "case_key": f"{CASE_KEY_LABEL[key]} ({TAX_ALLOC})",
                         "rough_key": OLD_TAX_KEY[lid], **{f"share_{k}": f"{v:.9f}" for k, v in sh.items()},
                         **{f"amount_{k}_bn": f"{v * nat:.4f}" for k, v in sh.items()},
                         "cps_case_key_base_bn": f"{base[key]:.4f}",
                         "cps_rough_key_base_bn": f"{sc['cps_bn'][OLD_TAX_KEY[lid]]:.4f}"})
    return rows


def cps_tax_totals():
    """TAX_CASES: rows of cps_tax_totals_<case>.csv: the CPS's federal and state income-tax dollars against the case's
    national lines, and the gaps, on two weights: the CPS's published person weights, and audit row 4's, the frame every
    rough key and the CPS-dollar rule use. Each row names its variable, its placement and the key it is the base of:
    on the record (the tax unit's head or dependent filer carries the unit's tax, as the CPS publishes it), or split
    equally over the tax unit's members, as the rough keys split it. FEDTAX_BC on the record is the case's federal
    key's base before raking, the concept of the national line (NIPA table 3.4 line 3 is before refundable credits);
    FEDTAX_AC floored at 0 on the record is the survey's own total after refundable credits; split over the tax unit it
    is the rough federal key, whose shortfall the CPS-dollar rule charged to no one. STATETAX_A floored at 0 on the
    record is the case's state key's base; split over the tax unit, the rough state key. The split moves each unit's
    tax onto its members' person weights, which raises the weighted totals."""
    ac = np.maximum(R.d.FEDTAX_AC.to_numpy(float), 0)
    specs = (("federal_income_tax", "FEDTAX_BC", "on the record", "the case's federal key's base, before raking",
              TAX_K["_fedtax_bc"]),
             ("federal_income_tax", "FEDTAX_AC floored at 0", "on the record", "none: the survey's after-credit total", ac),
             ("federal_income_tax", "FEDTAX_AC floored at 0", "split over the tax unit",
              "fit: the rough federal key, the CPS-dollar rule's dollars", R.K["fit"]),
             ("state_local_income_tax", "STATETAX_A floored at 0", "on the record", "the case's state_liability key's base",
              TAX_K["sit_case_personal"]),
             ("state_local_income_tax", "STATETAX_A floored at 0", "split over the tax unit",
              "sit: the rough state key, the CPS-dollar rule's dollars", R.K["sit"]))
    rows = []
    for frame, use, w in (("published", "the CPS's published person weights", PUBLISHED_W),
                          ("row4", "audit row 4: the rough re-key's frame (every rough key, the CPS-dollar rule)", R.w)):
        for lid, var, place, key, v in specs:
            nat = R.NATIONAL["receipts|" + lid]
            c = float(w @ v) / 1e9
            rows.append({"case": CASE, "frame": frame, "weights": use, "line": lid, "variable": var, "placement": place,
                         "key": key, "national_bn": f"{nat:.4f}", "cps_bn": f"{c:.4f}", "gap_bn": f"{nat - c:.4f}",
                         "cps_over_national": f"{c / nat:.6f}"})
    return rows
AGE = R.d.A_AGE.to_numpy()
ADULT = (AGE >= 18).astype(float)
BAND5 = np.minimum(AGE // 5 * 5, 80)
STATE = pd.Series(S.st)
REL = pd.read_csv(DER / "v4_state_relatives.csv").set_index("fips")
NHTS = pd.read_csv(DER / "v4_nhts_vmt.csv")
V_NH = float(NHTS.query("group == 'non_hispanic' and band == 'all'").vmt_per_person.iloc[0])
VRATE = {g: NHTS[(NHTS.group == g) & (NHTS.band != "all")].assign(band=lambda x: x.band.astype(int)).set_index("band")
         .vmt_per_person for g in ("nh_white", "nh_black", "all")}
PUBLISHED_W = R.w.copy()


# ------------------------------------------------------------------ frame and case state
def set_frame(w, target, shares_dump):
    """The white lane's frame totals on person weights w (white_count.set_weights), the engine shares and nationals
    of `shares_dump` (the Mexican rough run's medical and justice shares, the top-tail nationals) and the slice size."""
    lo = {l["side"] + "|" + l["id"]: l for l in shares_dump["low"]["lines"] if l["side"] != "scalar"}
    R.NATIONAL = {k: l["national_bn"] for k, l in lo.items()}
    R.eng_share = {k: (l["amount_bn"] / l["national_bn"] if abs(l["national_bn"]) > 1e-6 else 0.0) for k, l in lo.items()}
    R.w = w
    R.KTOT = {k: float((w * v).sum()) for k, v in R.K.items()}
    R.CPS_TOTAL = float(w.sum())
    R.PI["union"] = R.structure(R.MASK["mex"], w, R.cage)
    R.pc_scale = R.eng_share["spending|general_public_services"] / (float(w[R.MASK["mex"]].sum()) / R.CPS_TOTAL)
    R.NHW_POP = float(w[R.MASK["wall"]].sum())
    R.NHW_CRIME = float((w * R.crime_c)[R.MASK["wall"]].sum())
    R.NHW_OLD = float((w * R.old_c)[R.MASK["wall"]].sum())
    R.WUS_POP = float(w[R.MASK["wus"]].sum())
    R.TARGET = target
    R.RESIDENT = shares_dump["low"]["resident_population"]


def row4_weights():
    """Audit row 4: the engine's factors on the Mexico-born outside California and Texas (white_count.py)."""
    d = F.load()
    civ, union, gens = F.masks(d)
    W = d[F.REPS[:2]].to_numpy(float)
    arms, info = L.weight_arms(d, W, L.acs_cells())
    n4_frame = float(arms["row4"][union, 0].sum())
    del arms, d, W
    counts = pd.read_csv(BASIS / "frame_counts.csv").set_index("count")
    n4 = float(counts.loc["union|all", "row4"])
    gate("the engine's row-4 union reproduces frame_counts.csv", abs(n4_frame - n4) < 1e-3, f"{n4_frame:,.2f}")
    outside = R.d.PENATVTY.eq(303).to_numpy() & ~np.isin(S.st, L.CA_TX)
    w4 = PUBLISHED_W.copy()
    w4[outside & R.d.PRCITSHP.eq(4).to_numpy()] *= info["factor_natz"]
    w4[outside & R.d.PRCITSHP.eq(5).to_numpy()] *= info["factor_noncit"]
    got = float(w4[R.MASK["mex"]].sum())
    gate("the row-4 union matches the account's count (2 persons)", abs(got - n4) < 2, f"{got:,.1f} vs {n4:,.1f}")
    return w4, n4


# ------------------------------------------------------------------ accrual ratios
def acc_entry(row, rel=None):
    """A group's accrual parameters from an accrual_ratios.csv row. rel overrides its relative benefit-tax rate, and
    the net OASDI ratio is then recomputed as gross x (1 - rel x timing), as the pension lane nets it."""
    gross, timing = float(row["oasdi_per_tax_dollar"]), float(row["benefit_tax_timing"])
    if rel is None:
        rel, net = float(row["relative_benefit_tax_rate"]), float(row["oasdi_per_tax_dollar_net"])
    else:
        net = gross * (1 - rel * timing)
    return dict(net=net, part_a=float(row["part_a_per_hi_tax_dollar"]), rel=rel, gross=gross, timing=timing)


def accrual_params():
    name = ACCRUAL_FILES[CASE]
    wr = {(r["group"], r["scenario"]): r for r in csv.DictReader(open(DER / name))}
    br = {(r["group"], r["entry_rule"], r["scenario"]): r for r in csv.DictReader(open(BLACK_LANE / "derived" / name))}
    u, wt = wr[("union", "payable")], wr[("third_plus_nh_white", "payable")]
    b = br[("nh_black", "immigrants_at_arrival", "payable")]
    a = br[("all_residents", "immigrants_at_arrival", "payable")]
    gate("the white lane's union net OASDI ratio is the case's ratio_net (1e-6)",
         abs(float(u["oasdi_per_tax_dollar_net"]) - PA["ratio_net"]) < 1e-6, f"{u['oasdi_per_tax_dollar_net']} vs {PA['ratio_net']:.6f}")
    return {"union": {**acc_entry(u), "net": PA["ratio_net"], "rel": REL_UNION},
            "white": acc_entry(wt), "black": acc_entry(b), "all": acc_entry(a)}


ACC = None
GROUP_OF = {"mex": "union", "union_piece": "union", "w3": "white", "wus": "white", "wall": "white", "blk": "black",
            "avg": "all"}


def receipt_per_rel_benefit(end):
    """The case's tax on the union's 2024 benefits per benefit dollar per unit of relative rate. Rule 3: the low end's
    rule (shared) at both ends, because the rough income-tax key splits a tax unit's tax among its members. Rule 3b's
    alternative (BENEFIT_TAX_RULE "by_end"): each end's own rule (personal at the high end) over the engine union's
    benefits at that end."""
    at = "low" if BENEFIT_TAX_RULE == "shared" else end
    ss = next(l for l in DUMP["cash"][at]["lines"] if l["side"] == "spending" and l["id"] == "social_security")["amount_bn"]
    return PA["benefit_tax_receipt_bn"]["shared" if at == "low" else "personal"] / ss / REL_UNION


def apply_accrual(amt, p, per_rel_ben):
    """The case's pension rule on a group's line amounts (dict side|id -> amount), in place."""
    se = amt["receipts|self_employment_oasdi_hi"]
    oasdi = amt["receipts|employee_oasdi"] + amt["receipts|employer_oasdi"] + SE_SHARE * se
    hi = amt["receipts|employee_hi"] + amt["receipts|employer_hi"] + (1 - SE_SHARE) * se
    ss_cash, mc_cash = amt["spending|social_security"], amt["spending|medicare"]
    amt["spending|social_security"] = p["net"] * oasdi
    amt["spending|medicare"] = (1 - PART_A_SHARE) * mc_cash + p["part_a"] * hi
    amt["receipts|federal_income_tax"] -= per_rel_ben * p["rel"] * ss_cash
    return dict(oasdi_tax=oasdi, hi_tax=hi, ss_cash=ss_cash, medicare_cash=mc_cash)


# ------------------------------------------------------------------ the IPEDS keys (IPEDS_CASES, FEE_CASES)
HOSP = HOSP_TOT = None   # MEPS hospital payments by payer per MEPS person, and their totals (hospital_inputs())
# FEE_CASES: the hospital term stays beside the central (the team lead, 2026-10-07): its fee side takes a group's MEPS
# payer shares while the comparators' hospital spending stays on the OTHPUB health key, so the term would credit a
# group for hospital use its spending side never charges. ipeds_rows() turns it on to price it beside.
HOSPITAL_ON = False


def ipeds_total(race, key):
    """A race's CPS persons on a key (college or edben) on the current frame; the union's are the rough union's (the
    39,712,493 the fee lane's shares are on)."""
    if race == "union":
        if UNION_SC is None:
            raise SystemExit("[BLOCKED] the IPEDS keys need the rough union (setup())")
        cw = UNION_SC["cps_w"]
    else:
        cw = R.w * R.MASK[IPEDS_MASK[race]]
    return float((cw * R.K[key]).sum())


def ipeds_shares(sc):
    """A group's IPEDS keys: its race's shares of public higher education's use and of the tuition paid, carried by
    the group's CPS college key over its race's, and of Pell, carried by its low-income college key [ASSUMPTION]."""
    race = IPEDS_RACE.get(sc["name"])
    if race is None:
        raise SystemExit(f"[BLOCKED] the scenario {sc['name']!r} has no IPEDS race (IPEDS_RACE)")
    x = IK["union"] if race == "union" else IK["races"][race] if race != "all" else dict(use=1.0, tuition=1.0, pell=1.0)
    f = {k: float((sc["cps_w"] * R.K[k]).sum()) / ipeds_total(race, k) for k in ("college", "edben")}
    return dict(use=x["use"] * f["college"], tuition=x["tuition"] * f["college"], pell=x["pell"] * f["edben"])


def ipeds_move(sc, lid, national, ik):
    """The IPEDS keys' move of a line's amount from its rough key: Pell carved out of other federal benefits at the
    group's Pell share, and the education line's higher-education part at its use share, with (FEE_CASES) the tuition
    it pays short of its use."""
    c = IK["constants"]
    if lid == "other_federal_benefits":
        return c["pell_bn"] * (ik["pell"] - sc["share"]["ss"])
    move = national * c["higher_weight"] * (ik["use"] - sc["share"]["college"])
    return move + c["tuition_bn"] * (ik["use"] - ik["tuition"]) if FEES_ON else move


def hospital_inputs():
    """FEE_CASES: MEPS 2024 hospital facility payments (inpatient, outpatient, emergency) by payer for every record of
    the library's MEPS frame, through the fee lane's health.py (imported read-only; it verifies the pinned file)."""
    global HOSP, HOSP_TOT
    import importlib.util
    spec = importlib.util.spec_from_file_location("fee_health", FISCAL / "user_fee_allocation_2026_10_07/health.py")
    hm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hm)
    hm.verify()
    d = hm.read_meps()
    pay = {"medicare": d.MCR, "medicaid": d.MCD, "private_other": d.EXP - d.MCR - d.MCD - d.SLF}
    gate("the hospital term's MEPS records are the library's (the same weights; the rest weigh 0)",
         bool(np.array_equal(d.PERWT24F.to_numpy(), R.md.PERWT24F.reindex(d.index).to_numpy()))
         and float(R.md.PERWT24F.drop(d.index).abs().sum()) == 0.0)
    HOSP = {q: v.reindex(R.md.index, fill_value=0.0).to_numpy(float) for q, v in pay.items()}
    HOSP_TOT = {q: float((R.mw * v).sum()) for q, v in HOSP.items()}
    gate("the hospital term's payers are ipeds_keys.json's", set(HOSP) == set(IK["hospital"]["net_bn"]))
    # Positive control: the fee lane's union (MEPS HISPNCAT 1 on its frame) at its health key gives its residual
    fee = json.loads((FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json").read_text())
    union_w = R.mw * d.HISPNCAT.eq(1).reindex(R.md.index, fill_value=False).to_numpy(float) * fee["frames"]["meps_frame"]
    for a in ("personal", "shared"):
        got, want = hospital_residual(union_w, fee["health"]["s_K"][a]), fee["health"]["central"][a]["residual_bn"]
        gate(f"positive control: the fee lane's union reproduces its hospital residual, {a} (1e-9)", abs(got - want) < 1e-9,
             f"{got:.6f} vs {want:.6f}")


def hospital_residual(meps_w, s_k):
    """sum over payers q of (cost_q - payments_q) x (s_q - s_K): s_q the MEPS weights' share of payer q's hospital
    payments, at the fee lane's central inputs (ipeds_keys.json hospital.net_bn)."""
    return sum(v * (float((meps_w * HOSP[q]).sum()) / HOSP_TOT[q] - s_k) for q, v in IK["hospital"]["net_bn"].items())


def hospital_term(sc, amt, nat):
    """FEE_CASES, a group with MEPS keys: public hospitals' insured net at the group's MEPS shares of hospital payments
    by payer less the share its health key charges (health_services and its state-price line over the national), the
    fee lane's residual (item 4's term) on the group's own keys."""
    if "meps_w" not in sc:
        raise SystemExit(f"[BLOCKED] the scenario {sc['name']!r} has no MEPS weights for the hospital term")
    k = "spending|health_services"
    return hospital_residual(sc["meps_w"], (amt[k] + amt.get("spending|state_price_health_services", 0.0)) / nat[k])


def ipeds_gates():
    """IPEDS_CASES, once the frame and the rough union are the case's: the keys file is the fee lane's current one,
    the lines and capital component the keys move are the ones the rough keys priced, and the shares reproduce their
    races' where a group is its whole race."""
    fee = json.loads((FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json").read_text())
    c = IK["constants"]
    gate("ipeds_keys.json carries the fee lane's current shares and constants",
         IK["union"]["use"] == fee["higher_ed"]["U"] and IK["union"]["tuition"] == fee["higher_ed"]["s_R"]
         and IK["union"]["pell"] == fee["pell"]["share"] and c["pell_bn"] == fee["pell"]["total_bn"]
         and c["kappa"] == fee["nipa"]["kappa"] and c["tuition_bn"] == fee["nipa"]["tuition_bn"]
         and c["higher_weight"] == fee["nipa"]["weights"]["consolidated"]["higher"])
    gate("the rough keys the IPEDS keys replace: other federal benefits by Social Security receipts, education by K-12 "
         "and college", R.SPEND_KEY["other_federal_benefits"] == "ss" and "education_services" not in R.SPEND_KEY)
    for b in BASES:
        for end in ENDS:
            for which, dd in (("union", DUMP), ("case", FULL)):
                if dd is None:
                    continue
                e = dd[b][end]
                ofb = next(x for x in e["lines"] if x["side"] == "spending" and x["id"] == "other_federal_benefits")
                cols = [x["id"] for x in e["capital"] if x["id"].split("_")[0] == "college" and x["id"] not in ITEM_COMPONENTS]
                gate(f"{b} {end} {which} dump: other federal benefits hold Pell, and one college stock is keyed",
                     ofb["national_bn"] > c["pell_bn"] and cols == ["college"], f"{ofb['national_bn']:.4f}bn; {cols}")
    edu = next(x for x in DUMP["cash"]["low"]["lines"] if x["side"] == "spending" and x["id"] == "education_services")
    print(f"  the education line: {edu['national_bn']:.4f}bn (the fee lane's {c['education_line_bn']}); its higher-education "
          f"part {c['higher_weight'] * edu['national_bn']:.4f}bn", flush=True)
    if "items" not in META:
        gate("the education line is the fee lane's, so its part is the fee lane's higher-education dollars (1e-9)",
             abs(c["higher_weight"] * edu["national_bn"] - c["higher_dollars_bn"]) < 1e-9)
    u = ipeds_shares(UNION_SC)
    gate("the rough union's IPEDS shares are the fee lane's (1e-15 relative)",
         all(abs(u[k] / IK["union"][k] - 1) < 1e-15 for k in ("use", "tuition", "pell")))
    blk = ipeds_shares(R.scenario("blk", scaled=False))
    gate("the NH Black group, its whole race, takes IPEDS's Black shares (1e-12 relative)",
         all(abs(blk[k] / IK["races"]["black"][k] - 1) < 1e-12 for k in ("use", "tuition", "pell")))
    avg = R.scenario("avg")
    a = ipeds_shares(avg)
    gate("an all-residents slice takes its CPS college and low-income college shares (1e-12)",
         abs(a["use"] - avg["share"]["college"]) < 1e-12 and abs(a["pell"] - avg["share"]["edben"]) < 1e-12)
    if FEES_ON:
        hospital_inputs()


def ipeds_rows(groups):
    """IPEDS_CASES: rows of ipeds_terms_<case>.csv for the groups (label -> scenario; the rough union among them as
    mexican_origin_rough): each group's cost on the rough keys of September 27 and on the IPEDS keys, and the move by
    part, each a line amount's move times its response (the college stock's at its rate). The hospital term is beside
    the central: hospital_beside_bn is the run with it less the central run, and cost_with_hospital_bn that run's cost.
    Gate: the parts add to the move (1e-9)."""
    c, rows = IK["constants"], []
    for b in BASES:
        for end in ENDS:
            e = DUMP[b][end]
            ln = {x["id"]: x for x in e["lines"] if x["side"] == "spending"}
            col = next(x for x in e["capital"] if x["id"] == "college")
            got = {}
            for lab, sc in groups.items():
                on = run29(sc, end, b)[0]["cost"]
                with patched(globals(), IPEDS_ON=False, FEES_ON=False):
                    off = run29(sc, end, b)[0]["cost"]
                with patched(globals(), FEES_ON=False):
                    no_fees = run29(sc, end, b)[0]["cost"]
                if sc == "eng":
                    parts = dict(pell=0.0, higher_ed_use=0.0, college_capital=0.0, tuition=0.0)
                else:
                    ik = ipeds_shares(sc)
                    d_use = ik["use"] - sc["share"]["college"]
                    parts = dict(pell=c["pell_bn"] * (ik["pell"] - sc["share"]["ss"]) * ln["other_federal_benefits"]["response"],
                                 higher_ed_use=ln["education_services"]["national_bn"] * c["higher_weight"] * d_use
                                 * ln["education_services"]["response"],
                                 college_capital=col["stock_charged_bn"] * col["response"] * e["rate"] * c["kappa"] * d_use,
                                 tuition=(c["tuition_bn"] * (ik["use"] - ik["tuition"]) * ln["education_services"]["response"]
                                          if FEES_ON else 0.0))
                with patched(globals(), HOSPITAL_ON=True):
                    with_hosp = run29(sc, end, b)[0]["cost"]
                keys_only = parts["pell"] + parts["higher_ed_use"] + parts["college_capital"]
                gate(f"{b} {end} {lab}: the keys' parts are the move on the keys alone, and with the fees the tuition part "
                     "is the rest (1e-9)",
                     abs(no_fees - off - keys_only) < 1e-9 and abs(on - off - keys_only - parts["tuition"]) < 1e-9,
                     f"{no_fees - off:+.9f} vs {keys_only:+.9f}")
                got[lab] = (off, parts, on, with_hosp)
            u_off, _, u_on, u_hosp = got["mexican_origin_rough"]
            for lab, (off, parts, on, with_hosp) in got.items():
                rows.append({"case": CASE, "basis": b, "group": lab, "end": end, "cost_rough_keys_bn": f"{off:.4f}",
                             **{f"{k}_bn": f"{v:.4f}" for k, v in parts.items()}, "cost_bn": f"{on:.4f}",
                             "move_bn": f"{on - off:.4f}", "hospital_beside_bn": f"{with_hosp - on:.4f}",
                             "cost_with_hospital_bn": f"{with_hosp:.4f}",
                             "delta_like_for_like_rough_keys_bn": f"{u_off - off:.4f}",
                             "delta_like_for_like_bn": f"{u_on - on:.4f}",
                             "delta_change_bn": f"{(u_on - on) - (u_off - off):.4f}",
                             "delta_with_hospital_bn": f"{u_hosp - with_hosp:.4f}"})
    return rows


# ------------------------------------------------------------------ v4 group terms
def state_index(cw):
    pop = pd.Series(cw).groupby(STATE).sum()
    adults = pd.Series(cw * ADULT).groupby(STATE).sum()
    return V.index_of(REL, pop, adults)


def miles_denominator(p_union):
    return p_union * (1 - U5["group"]) * RHO + (1 - p_union) * (1 - U5["others"])


def miles_share(sc, union_sc=None):
    """The group's share of driver miles (see the module docstring, rule 4)."""
    name = sc["name"]
    ph = sc["share"]["pc"] * R.pc_scale
    p_union = (union_sc or sc)["share"]["pc"] * R.pc_scale
    den = miles_denominator(p_union)
    if name == "mex":
        return p_union * (1 - U5["group"]) * RHO / den, RHO, U5["group"]
    if name == "union_piece":
        s_u = miles_share(union_sc)[0]
        n5 = lambda cw: float((cw * (AGE >= 5)).sum())  # noqa: E731
        return s_u * n5(sc["cps_w"]) / n5(union_sc["cps_w"]), RHO, float((sc["cps_w"] * (AGE < 5)).sum() / sc["cps_w"].sum())
    cw = sc["cps_w"]
    u5 = float((cw * (AGE < 5)).sum() / cw.sum())
    by = pd.Series(cw * (AGE >= 5)).groupby(BAND5).sum()
    by = by[by.index >= 5]
    rate = VRATE[RACE_RATES[name]].reindex(by.index)
    rho = float((by * rate).sum() / by.sum()) / V_NH
    return ph * (1 - u5) * rho / den, rho, u5


def v4_terms(sc, e, union_sc):
    """The v4 item-9 and item-10 amounts for a group (rule 4) at one end of the case."""
    ix = state_index(sc["cps_w"])
    s, rho, u5 = miles_share(sc, union_sc)
    k_cons, k_old = sc["share"]["cons"], sc["share"]["hi"]
    k_road = FP * s + (1 - FP) * k_cons
    lines = {"roads_vmt_sl": HWY_N["sl"] * (k_road - k_old), "roads_vmt_fed": HWY_N["fed"] * (k_road - k_old)}
    for lid, x in SP_LINES.items():
        fs = SP_FUNCTIONS[x["parent"]]
        if sc["name"] == "union_piece" and "corrections_per_inmate" in fs:
            # A piece of the union takes its part of the union's per-prisoner premium: the union's index weights states
            # by persons x imprisonment rate, the piece's persons-based justice share does not, so the piece's own index
            # on its persons-based share would not add up to the union (California's relative is 2.35).
            fs = [f for f in fs if f != "corrections_per_inmate"]
            pu = pd.Series(union_sc["cps_w"]).groupby(STATE).sum()
            pp = pd.Series(sc["cps_w"]).groupby(STATE).sum().reindex(pu.index).fillna(0.0)
            has = REL.corrections_per_inmate.reindex(pu.index).notna()
            om = pu[has] * REL.imprisonment_rate.reindex(pu.index)[has]
            prem = float((om / om.sum() * (pp[has] / pu[has]).fillna(0.0)
                          * (REL.corrections_per_inmate.reindex(pu.index)[has] - 1)).sum())
            cpi = SL_AMOUNT["corrections_per_inmate"] * prem * R.line_share(union_sc, "spending", x["parent"])
        else:
            cpi = 0.0
        gap = sum(SL_AMOUNT[f] * (ix[f] - 1) for f in fs)
        lines[lid] = gap * R.line_share(sc, "spending", x["parent"]) + cpi
    return dict(index=ix, s_vmt=s, rho=rho, u5=u5, k_road=k_road, k_cons=k_cons, k_old=k_old, lines=lines,
                gasoline_shift=GAS * (s - k_cons), licences=LIC * s * ix["licences"])


# ------------------------------------------------------------------ the re-key
def run29(sc, end, basis="accrual", top=None, cap=False, v4=True, dump=None, union_sc=None, rule4="all"):
    """rekey_white.run on a case dump, with the sept29 rules when v4 (a September 27 dump with v4=False reproduces
    run()). sc: a scenario or 'eng' (the engine's own amounts). union_sc: the whole rough union, for union pieces.
    top: the income-tax rule, by default the central ('case' on TAX_CASES, else 'cps'; a September 27 run 'cps');
    'cps' and 'prop' are rekey_white.line_share's. rule4: 'all' (rule 4 for every group); 'union' (its alternative:
    other groups at national prices and the September 27 road keys, the union keeping its state-price and road terms);
    'none' (no group, the union included: the attribution's first sept29 step)."""
    if top is None:
        top = "case" if TAX_ON and v4 else "cps"
    g = "eng" if sc == "eng" else sc["name"]
    e = (dump or DUMP[basis])[end]
    lines = [ln for ln in e["lines"] if ln["side"] != "scalar"]
    amt, resp, nat = {}, {}, {}
    terms = None
    if rule4 not in ("all", "union", "none"):
        raise ValueError(f"[BLOCKED] rule4 {rule4!r}")
    items = v4 and g != "eng" and (rule4 == "all" or (rule4 == "union" and g in ("mex", "union_piece")))
    if items:
        terms = v4_terms(sc, e, union_sc if g == "union_piece" else sc if g == "mex" else union_sc or UNION_SC)
    ik = ipeds_shares(sc) if IPEDS_ON and v4 and g != "eng" else None
    for ln in lines:
        side, lid = ln["side"], ln["id"]
        k = side + "|" + lid
        nat[k], resp[k] = ln["national_bn"], ln["response"]
        if g == "eng" or (lid in UNION_LINES and g == "mex"):
            a = ln["amount_bn"]
        elif lid in UNION_LINES:
            a = 0.0
        elif v4 and lid in V4_SPEND:
            a = terms["lines"][lid] if items else 0.0
        elif v4 and side == "receipts" and lid in NEW_RECEIPTS:
            a = ln["national_bn"] * sc["share"][NEW_RECEIPTS[lid]]
        else:
            a = ln["national_bn"] * R.line_share(sc, side, lid, top)
            if ik is not None and side == "spending" and lid in IPEDS_LINES:
                a += ipeds_move(sc, lid, ln["national_bn"], ik)
        if cap and lid in (CAP29 if v4 else R.CAP_LINES):
            a = ln["national_bn"] * (R.scenario("mex") if g == "eng" else sc)["share"][(CAP29 if v4 else R.CAP_LINES)[lid]]
            resp[k] = 1.0
        amt[k] = a
    acc = None
    if items:
        amt["receipts|general_sales_tax"] *= terms["index"]["sales"]
        amt["receipts|excise_selective_sales"] += terms["gasoline_shift"]
        amt["receipts|personal_motor_vehicle"] = terms["licences"]
    if FEES_ON and HOSPITAL_ON and v4 and g not in ("eng", "mex", "union_piece"):
        # item 4's hospital term; the union's is in the engine's health share its pieces and it take (rule 1)
        amt["spending|health_services"] += hospital_term(sc, amt, nat)
    if v4 and g != "eng" and basis == "accrual":
        acc = apply_accrual(amt, ACC[GROUP_OF[g]], receipt_per_rel_benefit(end))
    # oct05: the union's side carries the added people at the case lane's own amounts (after the pension rule, which
    # their accrual does not follow: theirs is the lane's), with their capital return and production term below.
    lin = LIN[basis][end] if (LINEAGE_ON and dump is None and g in ("eng", "mex")) else None
    if lin is not None:
        for k, v in lin["lines"].items():
            amt[k] += v
    rec_amt = rec_eff = sp_amt = sp_eff = alloc_bal = 0.0
    old = dict(bal=0.0, net=0.0, alloc=0.0)
    rows, buckets = [], {}
    for ln in lines:
        side, lid = ln["side"], ln["id"]
        k = side + "|" + lid
        eff = amt[k] * resp[k]
        if lid not in R.ZERO:
            alloc_bal += nat[k] if side == "receipts" else -nat[k]
        if lid in R.OLD_AGE:
            sgn = 1 if side == "receipts" else -1
            old["bal"] += sgn * amt[k]
            old["net"] -= sgn * eff
            old["alloc"] += sgn * nat[k]
        if side == "receipts":
            rec_amt += amt[k]
            rec_eff += eff
        else:
            sp_amt += amt[k]
            sp_eff += eff
        b = next((x for x, v in (BUCKETS if v4 else R.BUCKETS).items() if lid in v), R.PER_HEAD)
        buckets[b] = buckets.get(b, 0.0) + (eff if side == "spending" else -eff)
        rows.append((side, lid, nat[k], amt[k], ln["response"]))
    sg = R.scenario("mex")["share"] if g == "eng" else sc["share"]
    ph = sg["pc"] * R.pc_scale
    ck = {"k12": sg["k12"], "college": sg["college"], "hwy": sg["hi"], "air": sg["hi"]}
    cap_bn = 0.0
    for c in e["capital"]:
        cid = c["id"]
        if cid in ITEM_COMPONENTS:
            # oct07: an item's offset of a component's key (the fee item's K-12, college and health keys) is the
            # engine union's key refinement; the rough union takes it where it takes the engine's key for the component
            # it offsets (public order and health), and no other group or component takes it (rule 5).
            k = c["key"] if g == "mex" and ITEM_COMPONENTS[cid].startswith(("pos", "health")) else 0.0
        elif cid.startswith("pos"):
            k = sc["external"]["public_order_safety"] if g not in ("eng", "mex") else c["key"]
        elif cid.startswith("health"):
            k = sc["external"]["health_services"] if g not in ("eng", "mex") else c["key"]
        elif items and cid in ("hwy_sl", "hwy_fed"):
            k = terms["k_road"]
        elif v4 and cid == "ent_housing_sl":
            k = sg["house"]
        elif ik is not None and cid == "college":
            # the IPEDS keys: the stock's higher-education part (kappa) at the group's use share
            k = IK["constants"]["kappa"] * ik["use"] + (1 - IK["constants"]["kappa"]) * sg["college"]
        else:
            k = ck.get(cid.split("_")[0], ph)
        cap_bn += c["stock_charged_bn"] * k * c["response"] * e["rate"]
    if g == "eng":
        cap_bn = e["capital_bn"]
    prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
    prod = prod if g in ("mex", "eng") else 0.0    # no production term for a native-born group
    if lin is not None:
        cap_bn += lin["capital_bn"]
        prod += lin["production_gain_bn"]
    buckets["capital return"] = cap_bn
    buckets["production gain (subtracted)"] = -prod
    net = sp_eff - rec_eff
    popg = (R.TARGET + (LINEAGE["counts"]["added"] if lin is not None else 0.0)) if g in ("eng", "mex") else sc["population"]
    sh = popg / e["resident_population"]
    bal = rec_amt - sp_amt
    r = dict(taxes_paid=rec_amt, spending_drawn=sp_amt, taxes_lost=rec_eff, spending_saved=sp_eff, net_budget=net,
             capital=cap_bn, production_gain=prod, cost=net + cap_bn - prod, balance=bal,
             gap=bal - sh * alloc_bal, old_age_net=old["net"], cost_ex_old_age=net + cap_bn - prod - old["net"],
             gap_ex_old_age=(bal - old["bal"]) - sh * (alloc_bal - old["alloc"]), population=popg, pop_share=sh)
    return r, rows, buckets, terms, acc


UNION_SC = None


# ------------------------------------------------------------------ state arm (state_white.main on run29)
def priced29(sc, end, basis, union_sc, adjust=None, arms=False):
    r, rows, buckets, _, _ = run29(sc, end, basis, BOTH_TOP if arms else None, arms, union_sc=union_sc)
    cost = r["cost"]
    if adjust is not None:
        e = DUMP[basis][end]
        for ln in e["lines"]:
            if ln["id"] in S.ADJ_KEY and ln["side"] == "spending":
                f = adjust[S.ADJ_KEY[ln["id"]]]
                b = "schools and colleges" if ln["id"] in ("school_reprice", "college_rekey") else R.PER_HEAD
                cost += ln["amount_bn"] * ln["response"] * f
                buckets[b] = buckets.get(b, 0.0) + ln["amount_bn"] * ln["response"] * f
        prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
        cost -= prod * adjust["hi"]
        buckets["production gain (subtracted)"] = -prod * adjust["hi"]
    return cost, buckets


def lineage_by_piece(basis, end, sc_union):
    """oct05: the added people's cost on the union's side (central and both arms) and its buckets, the overlay's run
    less the identified run of the rough union."""
    out = {}
    for arms in (False, True):
        args = (BOTH_TOP, True) if arms else ()
        r1, _, b1, _, _ = run29(sc_union, end, basis, *args)
        with identified():
            r0, _, b0, _, _ = run29(sc_union, end, basis, *args)
        out[arms] = (r1["cost"] - r0["cost"], {b: b1.get(b, 0.0) - b0.get(b, 0.0) for b in set(b1) | set(b0)})
    return out


def state_rows(basis):
    """Part F on the case: rows per region and end, and the low end's buckets. oct05: each union piece carries the
    added people's cost in proportion to its share of the identified G3+ persons, and its white pieces are on the
    piece's lineage count at the piece's lineage ages [ASSUMPTION: the added people live where the identified G3+ do,
    at their ages, as PI_LINEAGE places them nationally]. oct07: the same counts, the ages at the measured mix (TILT)."""
    rough = {end: run29(UNION_SC, end, basis)[0] for end in ENDS}
    pieces = {name: S.union_piece(m) for name, m in S.REGIONS.items()}
    pieces["Los Angeles metro"] = S.union_piece(S.LA)
    region = {name: S.REGIONS.get(name, S.LA) for name in pieces}
    s3 = {name: (float(R.w[G3_CPS & m].sum()) / float(R.w[G3_CPS].sum()) if LINEAGE_ON else 0.0) for name, m in region.items()}
    added = LINEAGE["counts"]["added"] if LINEAGE_ON else 0.0
    out, bucket_rows = [], []
    for end in ENDS:
        u = {n: priced29(sc, end, basis, UNION_SC, sc["frac"]) for n, sc in pieces.items()}
        lin = lineage_by_piece(basis, end, UNION_SC) if LINEAGE_ON else {False: (0.0, {}), True: (0.0, {})}
        if LINEAGE_ON:
            u = {n: (c + lin[False][0] * s3[n], {b: bk.get(b, 0.0) + lin[False][1].get(b, 0.0) * s3[n] for b in set(bk) | set(lin[False][1])})
                 for n, (c, bk) in u.items()}
        resid = rough[end]["cost"] - sum(u[n][0] for n in S.REGIONS)
        gate(f"{basis} {end}: the union's pieces sum to the rough union within $1bn", abs(resid) < 1.0, f"{resid:+.4f}bn")
        tot = dict(union=0.0, white_union_ages=0.0, white_own_ages=0.0, arms_union=0.0, arms_white=0.0)
        for name, sc in pieces.items():
            pop, share = sc["population"] + added * s3[name], sc["frac"]["pc"]
            uc = u[name][0] + resid * share
            ua = priced29(sc, end, basis, UNION_SC, sc["frac"], arms=True)[0] + lin[True][0] * s3[name] + resid * share
            wmask = S.REGIONS.get(name, S.LA) if name != "rest of US" else np.ones(len(R.d), bool)
            if LINEAGE_ON and TILT is not None:
                # oct07: the piece's added count as on oct05 (its share of the identified G3+), at the measured ages:
                # its G3+ records tilted as nationally, then scaled to that count.
                a = R.w * (G3_CPS & region[name]) * TILT
                wl = R.w * (S.UNION & region[name]) + a * (added * s3[name] / float(a.sum()))
                pi_union = R.structure(np.ones(len(wl), bool), wl, R.cage)
            elif LINEAGE_ON:
                wl = R.w * (S.UNION & region[name]) + R.w * (G3_CPS & region[name]) * (added / float(R.w[G3_CPS].sum()))
                pi_union = R.structure(np.ones(len(wl), bool), wl, R.cage)
            else:
                pi_union = R.structure(S.UNION & S.REGIONS.get(name, S.LA), R.w, R.cage)
            wu = S.white_piece(wmask, pop, pi_union)
            wo = S.white_piece(wmask, pop, None)
            cu, bku = priced29(wu, end, basis, UNION_SC)
            co = priced29(wo, end, basis, UNION_SC)[0]
            ca = priced29(wu, end, basis, UNION_SC, arms=True)[0]
            out.append({"basis": basis, "region": name, "end": end, "spec": DUMP[basis][end]["spec"],
                        "union_persons": f"{pop:.0f}", "white_cps_sample": wu["sample"],
                        "white_rates_from": "national" if name == "rest of US" else name,
                        "cost_union_bn": f"{uc:.4f}", "cost_white_union_ages_bn": f"{cu:.4f}",
                        "cost_white_own_ages_bn": f"{co:.4f}", "delta_union_ages_bn": f"{uc - cu:.4f}",
                        "delta_own_ages_bn": f"{uc - co:.4f}", "delta_union_ages_per_person": f"{(uc - cu) * 1e9 / pop:.0f}",
                        "delta_own_ages_per_person": f"{(uc - co) * 1e9 / pop:.0f}",
                        "delta_union_ages_both_arms_per_person": f"{(ua - ca) * 1e9 / pop:.0f}"})
            if name in S.REGIONS:
                for k, v in (("union", uc), ("white_union_ages", cu), ("white_own_ages", co), ("arms_union", ua),
                             ("arms_white", ca)):
                    tot[k] += v
            if end == "low":
                for b in list(BUCKETS) + [R.PER_HEAD, "capital return", "production gain (subtracted)"]:
                    d = u[name][1].get(b, 0.0) - bku.get(b, 0.0)
                    bucket_rows.append({"basis": basis, "region": name, "bucket": b,
                                        "cost_union_bn": f"{u[name][1].get(b, 0.0):.4f}",
                                        "cost_white_union_ages_bn": f"{bku.get(b, 0.0):.4f}", "delta_cost_bn": f"{d:.4f}",
                                        "delta_cost_per_person": f"{d * 1e9 / pop:.0f}"})
        n = R.TARGET + added
        out.append({"basis": basis, "region": "sum of CA, TX and rest", "end": end, "spec": DUMP[basis][end]["spec"],
                    "union_persons": f"{sum(pieces[x]['population'] + added * s3[x] for x in S.REGIONS):.0f}", "white_cps_sample": "",
                    "white_rates_from": "state", "cost_union_bn": f"{tot['union']:.4f}",
                    "cost_white_union_ages_bn": f"{tot['white_union_ages']:.4f}",
                    "cost_white_own_ages_bn": f"{tot['white_own_ages']:.4f}",
                    "delta_union_ages_bn": f"{tot['union'] - tot['white_union_ages']:.4f}",
                    "delta_own_ages_bn": f"{tot['union'] - tot['white_own_ages']:.4f}",
                    "delta_union_ages_per_person": f"{(tot['union'] - tot['white_union_ages']) * 1e9 / n:.0f}",
                    "delta_own_ages_per_person": f"{(tot['union'] - tot['white_own_ages']) * 1e9 / n:.0f}",
                    "delta_union_ages_both_arms_per_person": f"{(tot['arms_union'] - tot['arms_white']) * 1e9 / n:.0f}"})
    return out, bucket_rows


def state_rows27():
    """state_white.main's deltas on the September 27 dump through run29 (positive control against white_count.csv)."""
    rough = {end: run29(R.scenario("mex"), end, v4=False, dump=DUMP27)[0] for end in ENDS}
    pieces = {name: S.union_piece(m) for name, m in S.REGIONS.items()}
    pieces["Los Angeles metro"] = S.union_piece(S.LA)
    out = {}
    for end in ENDS:
        def p27(sc, adjust=None):
            r, _, _, _, _ = run29(sc, end, v4=False, dump=DUMP27)
            cost = r["cost"]
            if adjust is not None:
                for ln in DUMP27[end]["lines"]:
                    if ln["id"] in S.ADJ_KEY and ln["side"] == "spending":
                        cost += ln["amount_bn"] * ln["response"] * adjust[S.ADJ_KEY[ln["id"]]]
                prod = [x for x in DUMP27[end]["lines"] if x["id"] == "production_gain_bn"][0]["effect_bn"]
                cost -= prod * adjust["hi"]
            return cost
        u = {n: p27(sc, sc["frac"]) for n, sc in pieces.items()}
        resid = rough[end]["cost"] - sum(u[n] for n in S.REGIONS)
        tot = 0.0
        for name, sc in pieces.items():
            wmask = S.REGIONS.get(name, S.LA) if name != "rest of US" else np.ones(len(R.d), bool)
            pi_union = R.structure(S.UNION & S.REGIONS.get(name, S.LA), R.w, R.cage)
            dlt = u[name] + resid * sc["frac"]["pc"] - p27(S.white_piece(wmask, sc["population"], pi_union))
            out[(name, end)] = dlt
            tot += dlt if name in S.REGIONS else 0.0
        out[("sum of CA, TX and rest", end)] = tot
    return out


def scenarios():
    """The groups; on oct05 the scaled slices are on the lineage's count and A3 at its ages (on_lineage)."""
    mex = R.scenario("mex")
    with on_lineage():
        return {"mexican_origin_engine": "eng", "mexican_origin_rough": mex,
                "nh_black_rough": R.scenario("blk", scaled=False),
                "A1_third_plus_nh_white": R.scenario("w3"), "A2_us_born_nh_white": R.scenario("wus"),
                "A3_third_plus_nh_white_at_union_ages": R.scenario("w3", "union"),
                "A4_third_plus_nh_white_stationary": R.scenario("w3", "stationary"),
                "all_residents_slice": R.scenario("avg")}


# ------------------------------------------------------------------ the designed rules' alternatives
@contextmanager
def patched(space, **values):
    """Names in a namespace (a module's globals) set for the duration of an alternative, then restored."""
    old = {k: space[k] for k in values}
    space.update(values)
    try:
        yield
    finally:
        space.update(old)


# ------------------------------------------------------------------ oct05: the lineage on both sides
G3_CPS = None        # the identified G3+ on the frame (native, both parents US-born, Mexican origin)
PI_LINEAGE = None    # the lineage's age structure: the union's, with the added people at the identified G3+'s ages
TILT = None          # oct07: each record's measured over identified age share (age_tilt); None places v5's way


def lineage_setup():
    """oct05, once the frame is the case's: the identified G3+ (gated to the lineage's count) and PI_LINEAGE
    [ASSUMPTION: the added people at the identified G3+ members' ages, as the lineage lane prices them]."""
    global G3_CPS, PI_LINEAGE, TILT
    d = R.d
    g3 = (d.PRCITSHP.isin([1, 2, 3]) & d.PEFNTVTY.isin(R.US) & d.PEMNTVTY.isin(R.US) & d.PRDTHSP.eq(1)).to_numpy()
    n3 = float(R.w[g3].sum())
    gate("the frame's identified G3+ is the lineage's identified_g3plus (1 person)",
         abs(n3 - LINEAGE["counts"]["identified_g3plus"]) <= 1.0, f"{n3:,.3f} vs {LINEAGE['counts']['identified_g3plus']:,.3f}")
    gate("the identified G3+ is inside the union", not (g3 & ~R.MASK["mex"]).any())
    if "age_mix" in LINEAGE:
        TILT = age_tilt(g3)
        wl = R.w * R.MASK["mex"] + R.w * g3 * (LINEAGE["counts"]["added"] / n3) * TILT
    else:
        TILT = None
        wl = R.w * R.MASK["mex"] + R.w * g3 * (LINEAGE["counts"]["added"] / n3)
    got = float(wl.sum())
    gate("the union with the added people at G3+ weights is the lineage population (2 persons, the frame's union gate)",
         abs(got - LINEAGE["counts"]["lineage_population"]) < 2, f"{got:,.3f} vs {LINEAGE['counts']['lineage_population']:,.3f}")
    G3_CPS, PI_LINEAGE = g3, R.structure(np.ones(len(wl), bool), wl, R.cage)


def age_tilt(g3):
    """oct07 (the lineage item's measured ages, meta.lineage.age_mix): every record's tilt, its band's share of the
    added people (the G3-rate persons and the later losses at their own mixes, by count) over its share of the
    identified G3+. The frame's G3+ structure must be the age-mix lane's identified mix exactly, so the tilted G3+
    weights carry the added people at the measured mix and the identified mix gives v5's weights."""
    am, c = LINEAGE["age_mix"], LINEAGE["counts"]
    labels = [f"{b}+" if b == 80 else f"{b}-{b + 4}" for b in R.BANDS]
    gate("the age mix is on the library's five-year bands", am["bands"] == labels)
    ident = R.structure(g3, R.w, R.cage)
    gate("the frame's identified G3+ ages are the age-mix lane's identified mix, exactly",
         [float(x) for x in ident] == am["mixes"]["identified"])
    mix = (c["at_g3_rate"] * np.asarray(am["mixes"]["g3_rate"], float)
           + c["later_losses"] * np.asarray(am["mixes"]["later"], float)) / c["added"]
    gate("the added people's mix sums to 1 and has no band without identified G3+ (1e-12)",
         abs(mix.sum() - 1) < 1e-12 and not ((ident <= 0) & (mix > 0)).any())
    t = np.divide(mix, ident, out=np.zeros(len(mix)), where=ident > 0)
    return t[np.searchsorted(R.BANDS, R.cage)]


@contextmanager
def on_lineage():
    """oct05: scaled slices built inside are on the lineage's count, and 'union' ages are PI_LINEAGE. The rough union
    itself is built outside (UNION_SC): the CPS sees the identified 39.71M, and the overlay adds the rest."""
    if not LINEAGE_ON:
        yield
        return
    with patched(vars(R), TARGET=R.TARGET + LINEAGE["counts"]["added"]), patched(R.PI, union=PI_LINEAGE):
        yield


@contextmanager
def identified():
    """oct05: the comparison on the identified union at v5's responses (the overlay off; slices built inside are on
    the union's 39,712,493 at its ages)."""
    with patched(globals(), LINEAGE_ON=False):
        yield


ALTERNATIVES = [
    ("rule 2", "housing_enterprise_surplus per head and tenant_occupied_property on capital income: the rough keys of "
               "the lines v4 split them from (enterprise_surplus, remaining_production_property)", BASES),
    # rule 3a's text takes the union's ratios of the case's accrual file (1.018378 and 1.460946 on the 2025 reports)
    ("rule 3a", "every group at the union's accrual per tax dollar (OASDI gross {gross:.6f}, Part A {part_a:.6f} per HI "
                "tax dollar), with its own benefit-tax rate and timing", ("accrual",)),
    ("rule 3b", "the tax on benefits at the case's rule for each end (shared at spec 48, personal at spec 11) over the "
                "engine union's benefits at that end", ("accrual",)),
    ("rule 4", "other groups at national prices and the September 27 road keys (the union keeps its terms)", BASES),
]


def run_alternative(rule, sc, end, basis, acc=None):
    """A group's cost under one alternative; acc (the caller's accrual parameters) replaces ACC for the run."""
    with ExitStack() as st:
        kw = {}
        if rule == "rule 2":
            st.enter_context(patched(globals(), NEW_RECEIPTS={}))
            st.enter_context(patched(vars(R), RECEIPT_KEY={**R.RECEIPT_KEY, **PARENT_KEYS}))
        elif rule == "rule 3a":
            u = ACC["union"]
            acc = {g: p if g == "union" else {**p, "net": u["gross"] * (1 - p["rel"] * p["timing"]), "part_a": u["part_a"]}
                   for g, p in ACC.items()}
        elif rule == "rule 3b":
            st.enter_context(patched(globals(), BENEFIT_TAX_RULE="by_end"))
        elif rule == "rule 4":
            kw["rule4"] = "union"
        elif acc is None:
            raise ValueError(f"[BLOCKED] unknown alternative {rule!r}")
        if acc is not None:
            st.enter_context(patched(globals(), ACC=acc))
        return run29(sc, end, basis, **kw)[0]["cost"]


def alternatives(groups, extra=()):
    """Rows of derived/rule_alternatives_sept29.csv: each alternative for the groups (label -> scenario; the rough
    union among them), the central beside it. extra: (rule, alternative, bases, acc) rows the caller adds."""
    rows = []
    for rule, text, bases, acc in [(r, t, b, None) for r, t, b in ALTERNATIVES] + list(extra):
        if rule == "rule 3a":
            text = text.format(gross=ACC["union"]["gross"], part_a=ACC["union"]["part_a"])
        for b in bases:
            for end in ENDS:
                cost = {lab: run_alternative(rule, sc, end, b, acc) for lab, sc in groups.items()}
                central = {lab: run29(sc, end, b)[0]["cost"] for lab, sc in groups.items()}
                u, uc = cost["mexican_origin_rough"], central["mexican_origin_rough"]
                for lab in groups:
                    rows.append({"rule": rule, "alternative": text, "basis": b, "end": end, "group": lab,
                                 "cost_bn": f"{cost[lab]:.4f}", "cost_central_bn": f"{central[lab]:.4f}",
                                 "change_bn": f"{cost[lab] - central[lab]:.4f}",
                                 "delta_like_for_like_bn": f"{u - cost[lab]:.4f}",
                                 "delta_like_for_like_central_bn": f"{uc - central[lab]:.4f}",
                                 "delta_change_bn": f"{(u - cost[lab]) - (uc - central[lab]):.4f}"})
    return rows


# ------------------------------------------------------------------ attribution: September 27 to sept29
ATTR_GROUPS = {"mexican_origin_rough": lambda: R.scenario("mex"),
               "A1_third_plus_nh_white": lambda: R.scenario("w3"),
               "A3_third_plus_nh_white_at_union_ages": lambda: R.scenario("w3", "union"),
               "nh_black_rough": lambda: R.scenario("blk", scaled=False),
               "all_residents_slice": lambda: R.scenario("avg")}
STEPS_SEPT29 = [("a", "September 27 case, published weights (the union at 40,896,574; ladders 259 and 263)", "cash"),
                ("0", "September 27 case, audit row-4 weights (the union at 39,712,493; ladder 274)", "cash"),
                ("1", "sept29 cash set: its lines, nationals, responses and two new receipt lines; no group state-priced "
                      "or miles-keyed", "cash"),
                ("2", "+ state prices and road miles for every group (rule 4): the sept29 cash set", "cash"),
                ("3", "+ the pension accrual (rule 3): the sept29 case", "accrual")]
# oct05: steps 1-3 run on the identified union at v5's responses (the union dumps), every slice on 39,712,493; step 4
# adds the lineage on both sides. Step 1 so also carries v5's response move (sept29's lines and nationals).
STEPS_IDENTIFIED = [("1", "oct05 cash set on the identified union (39,712,493): sept29's lines and nationals at v5's "
                          "responses, the two new receipt lines; no group state-priced or miles-keyed", "cash"),
                    ("2", "+ state prices and road miles for every group (rule 4): that cash set", "cash"),
                    ("3", "+ the pension accrual (rule 3): the oct05 case on the identified union", "accrual")]
STEP_LINEAGE =("4", "+ the lineage (oct05): the added 3,039,720 people at the case lane's amounts on the union's side, "
                     "every scaled slice on 42,752,213 and at the lineage's ages", "accrual")
# oct07: the same steps on v6; the edit sets' union parts are in the union dumps (steps 1-3: those on both sets in
# steps 1 and 2, the pension item's in step 3) and their lineage parts with the added people (step 4).
STEPS_IDENTIFIED_V6 = [("1", "oct07 cash set on the identified union (39,712,493): sept29's lines and nationals at v6's "
                             "responses with the cash set's items' union parts, the two new receipt lines; no group "
                             "state-priced or miles-keyed", "cash"),
                       ("2", "+ state prices and road miles for every group (rule 4): that cash set", "cash"),
                       ("3", "+ the pension accrual (rule 3) on the 2026 separate-funds path, the pension item's union "
                             "part with it: the oct07 case on the identified union", "accrual")]
STEP_LINEAGE_V6 = ("4", "+ the lineage (oct07): the added 3,039,720 people at the case lane's amounts (their measured "
                        "age mix, the items' lineage parts) on the union's side, every scaled slice on 42,752,213 and "
                        "at the lineage's ages", "accrual")
# IPEDS_CASES: step 1 also moves every group from the September 27 keys to the IPEDS keys (and, FEE_CASES, the fees)
IPEDS_STEP = "; every group on the IPEDS keys for Pell and public higher education"
IPEDS_STEP_FEES = "; every group on the IPEDS keys for Pell and public higher education, with item 4's tuition term"
# TAX_CASES: steps 1-4 keep the CPS-dollar rule for income taxes; step 5 moves every group to the case's own keys
STEP_TAX = ("5", "+ the case's own income-tax keys for every group (round 2): federal income tax on v4 item 3's IRS-raked "
                 "key, state and other personal taxes on the state-liability key, the shared allocation: the case", "accrual")
STEP_COST: dict = {}    # (step, label, end) -> (cost, population, buckets); steps a and 0 are filled by setup()
ALL_BUCKETS = list(BUCKETS) + [R.PER_HEAD, "capital return", "production gain (subtracted)"]
use_case("sept29")


def step27(step):
    """The September 27 case for every ATTR_GROUPS label on the current frame."""
    for lab, make in ATTR_GROUPS.items():
        sc = make()
        for end in ENDS:
            r, _, bk, _, _ = run29(sc, end, v4=False, dump=DUMP27)
            STEP_COST[(step, lab, end)] = (r["cost"], r["population"], bk)


def attribution(groups):
    """Rows of derived/attribution_<case>.csv for the groups (label -> scenario on the case's frame; labels of
    ATTR_GROUPS, the rough union among them): each step's cost, its change and the like-for-like delta's change.
    oct05: steps 1-3 rebuild the groups on the identified union (39,712,493, the overlay off); step 4 is the case.
    TAX_CASES: steps 1-4 on the CPS-dollar rule, step 5 the case on its own income-tax keys; a group's step-5 change is
    minus its change in the three income-tax lines (gate, 1e-9)."""
    lineage = LINEAGE_ON
    top = "cps" if TAX_ON else None
    with identified():
        base = {lab: ATTR_GROUPS[lab]() for lab in groups} if lineage else groups
        for lab, sc in base.items():
            for end in ENDS:
                for step, basis, rule4 in (("1", "cash", "none"), ("2", "cash", "all"), ("3", "accrual", "all")):
                    r, _, bk, _, _ = run29(sc, end, basis, top, rule4=rule4)
                    STEP_COST[(step, lab, end)] = (r["cost"], r["population"], bk)
    if TAX_ON:
        for lab, sc in groups.items():
            for end in ENDS:
                r, rows, bk, _, _ = run29(sc, end, "accrual")
                STEP_COST[("5", lab, end)] = (r["cost"], r["population"], bk)
                r0, rows0, _, _, _ = run29(sc, end, "accrual", "cps")
                tax = sum((a[3] - b[3]) * a[4] for a, b in zip(rows, rows0) if a[0] == "receipts" and a[1] in CASE_TAX_KEY)
                gate(f"attribution step 5 {lab} {end}: the change is minus the income-tax lines' change (1e-9)",
                     abs((r["cost"] - r0["cost"]) + tax) < 1e-9 and [a[:3] for a in rows] == [b[:3] for b in rows0],
                     f"{r['cost'] - r0['cost']:+.6f} vs {-tax:+.6f}")
    if lineage:
        f = (R.TARGET + LINEAGE["counts"]["added"]) / R.TARGET
        for lab, sc in groups.items():
            for end in ENDS:
                r, _, bk, _, _ = run29(sc, end, "accrual", top)
                STEP_COST[("4", lab, end)] = (r["cost"], r["population"], bk)
                # Positive controls on step 4: the union moves by the added people alone, the NH Black group (its own
                # count) not at all, and a slice at its own or fixed ages in proportion to its count (the re-key is
                # linear in a slice's weights). A3 also moves to the lineage's ages, so it has no such control.
                c3 = STEP_COST[("3", lab, end)][0]
                if lab == "mexican_origin_rough":
                    want, what = c3 + LIN["accrual"][end]["cost_bn"], "the identified union plus the added people"
                elif lab == "nh_black_rough":
                    want, what = c3, "the identified run (its own count)"
                elif lab == "A3_third_plus_nh_white_at_union_ages":
                    continue
                else:
                    want, what = c3 * f, f"the identified run x {f:.6f}"
                gate(f"attribution step 4 {lab} {end}: {what} (1e-9 relative)", abs(r["cost"] - want) <= 1e-9 * max(1.0, abs(want)),
                     f"{r['cost']:.6f} vs {want:.6f}")
    for (step, lab, end), (c, _, bk) in STEP_COST.items():
        gate(f"attribution step {step} {lab} {end}: the buckets add to the cost (1e-9)",
             abs(sum(bk.get(b, 0.0) for b in ALL_BUCKETS) - c) < 1e-9 and set(bk) <= set(ALL_BUCKETS))
    rows = []
    for end in ENDS:
        prev = None
        for step, text, basis in STEPS:
            u = STEP_COST[(step, "mexican_origin_rough", end)][0]
            now = {lab: (STEP_COST[(step, lab, end)][0], u - STEP_COST[(step, lab, end)][0]) for lab in groups}
            for lab in groups:
                c, pop, _ = STEP_COST[(step, lab, end)]
                rows.append({"step": step, "description": text, "basis": basis, "end": end, "group": lab,
                             "cost_bn": f"{c:.4f}", "population": f"{pop:.0f}", "cost_per_member": f"{c * 1e9 / pop:.0f}",
                             "change_bn": "" if prev is None else f"{c - prev[lab][0]:.4f}",
                             "delta_like_for_like_bn": f"{now[lab][1]:.4f}",
                             "delta_change_bn": "" if prev is None else f"{now[lab][1] - prev[lab][1]:.4f}"})
            prev = now
    return rows


def attribution_buckets(groups):
    """Rows of derived/attribution_buckets_sept29.csv (after attribution()): each step's cost by bucket, and the
    change from the step before."""
    rows = []
    for end in ENDS:
        for i, (step, _, basis) in enumerate(STEPS):
            ub = STEP_COST[(step, "mexican_origin_rough", end)][2]
            for lab in groups:
                bk = STEP_COST[(step, lab, end)][2]
                pb = STEP_COST[(STEPS[i - 1][0], lab, end)][2] if i else None
                for b in ALL_BUCKETS:
                    rows.append({"step": step, "basis": basis, "end": end, "group": lab, "bucket": b,
                                 "cost_bn": f"{bk.get(b, 0.0):.4f}",
                                 "change_bn": "" if pb is None else f"{bk.get(b, 0.0) - pb.get(b, 0.0):.4f}",
                                 "delta_vs_union_rough_bn": f"{ub.get(b, 0.0) - bk.get(b, 0.0):.4f}"})
    return rows


def setup():
    """Positive controls on the September 27 dump, then the sept29 frame (row-4 weights, the case's shares). Returns
    the row-4 union count."""
    global ACC, UNION_SC
    print("[the case: dumps and rules]", flush=True)
    case_dump = FULL if LINEAGE_ON else DUMP     # oct05: the case is the full dump; DUMP is its identified union
    for b in BASES:
        for i, end in enumerate(ENDS):
            gate(f"{b} dump {end}: cost is main_case_bands.csv's {'adopted' if b == 'accrual' else 'cash_set'} (5e-5)",
                 abs(case_dump[b][end]["cost_bn"] - ORACLE[b][i]) < 5e-5, f"{case_dump[b][end]['cost_bn']:.6f} vs {ORACLE[b][i]:.4f}")
            got = run29("eng", end, b)[0]["cost"]
            gate(f"{b} {end}: the lane's cost formula on the engine's amounts reproduces the dump (1e-9)"
                 + (", the added people's amounts on the union dump's" if LINEAGE_ON else ""),
                 abs(got - case_dump[b][end]["cost_bn"]) < 1e-9, f"{got:.10f}")
            if LINEAGE_ON:
                with identified():
                    got = run29("eng", end, b)[0]["cost"]
                gate(f"{b} {end}: the lane's cost formula on the union dump's amounts reproduces it (1e-9)",
                     abs(got - DUMP[b][end]["cost_bn"]) < 1e-9, f"{got:.10f}")
    if LINEAGE_ON:
        lineage_gates()
    for i, end in enumerate(ENDS):
        cash = {l["side"] + "|" + l["id"]: l["amount_bn"] for l in DUMP["cash"][end]["lines"] if l["side"] != "scalar"}
        accr = {l["side"] + "|" + l["id"]: l["amount_bn"] for l in DUMP["accrual"][end]["lines"] if l["side"] != "scalar"}
        rule = PA["benefit_tax_receipt_bn"]["shared" if end == "low" else "personal"]
        se = cash["receipts|self_employment_oasdi_hi"]
        ss = PA["ratio_net"] * (cash["receipts|employee_oasdi"] + cash["receipts|employer_oasdi"] + SE_SHARE * se)
        mc = (1 - PART_A_SHARE) * cash["spending|medicare"] + PA["part_a_accrual_bn"]
        fit = cash["receipts|federal_income_tax"] - rule
        gate(f"{end}: the case's pension rule on the engine's cash-set union amounts gives the accrual set's (1e-9)",
             max(abs(ss - accr["spending|social_security"]), abs(mc - accr["spending|medicare"]),
                 abs(fit - accr["receipts|federal_income_tax"])) < 1e-9,
             f"SS {ss:.6f}/{accr['spending|social_security']:.6f}, Medicare {mc:.6f}/{accr['spending|medicare']:.6f}, "
             f"FIT {fit:.6f}/{accr['receipts|federal_income_tax']:.6f}")
    gp = pd.read_csv(FISCAL / "state_priced_services_2026_09_29/derived/group_population_by_state.csv").set_index("fips")
    ixu = V.index_of(REL, gp.group_share, gp.group_adult_share)
    for lid, x in SP_LINES.items():
        gap = sum(SL_AMOUNT[f] * (ixu[f] - 1) for f in SP_FUNCTIONS[x["parent"]])
        gate(f"{lid}: the state lane's union indexes give the payload's national gap (1e-6)",
             abs(gap - x["national_gap_bn"]) < 1e-6, f"{gap:.6f} vs {x['national_gap_bn']:.6f}")
    for b in BASES:
        for end in ENDS:
            for ln in DUMP[b][end]["lines"]:
                if ln["side"] == "scalar" or ln["id"] in R.ZERO:
                    continue
                handled = (ln["id"] in UNION_LINES or ln["id"] in V4_SPEND or ln["id"] in NEW_RECEIPTS
                           or (R.RECEIPT_KEY if ln["side"] == "receipts" else R.SPEND_KEY).get(ln["id"])
                           or ln["id"] in ("education_services", *S.EXT))
                if not handled:
                    gate(f"{b} {end}: line {ln['side']}|{ln['id']} has a key", False)
                if abs(ln["national_bn"]) < 1e-9 and abs(ln["amount_bn"]) > 1e-9 and ln["id"] not in UNION_LINES and ln["id"] not in V4_SPEND:
                    gate(f"{b} {end}: line {ln['id']} has national 0 and an amount, and no rule", False)
    gate("every line of both dumps has a key, and every national-0 line with an amount has a rule", not FAILS)

    print("[positive controls: the September 27 dump]", flush=True)
    summary = pd.read_csv(DER / "rekey_summary.csv")
    for lab, sc in (("mexican_origin_rough", R.scenario("mex")), ("A1_third_plus_nh_white", R.scenario("w3")),
                    ("A3_third_plus_nh_white_at_union_ages", R.scenario("w3", "union")),
                    ("nh_black_rough", R.scenario("blk", scaled=False))):
        for end in ENDS:
            got = run29(sc, end, v4=False, dump=DUMP27)[0]["cost"]
            want = float(summary.query("group == @lab and end == @end").cost.iloc[0])
            gate(f"published weights: run29 reproduces rekey_summary.csv {lab} {end}", abs(got - want) < 5e-5,
                 f"{got:.4f} vs {want:.4f}")
    step27("a")
    for lab in ATTR_GROUPS:
        for end in ENDS:
            want = float(summary.query("group == @lab and end == @end").cost.iloc[0])
            gate(f"attribution step a is rekey_summary.csv {lab} {end}", abs(STEP_COST[("a", lab, end)][0] - want) < 5e-5,
                 f"{STEP_COST[('a', lab, end)][0]:.4f}")
    w4, n4 = row4_weights()
    set_frame(w4, n4, DUMP27)
    wc = pd.read_csv(BASIS / "white_count.csv")
    want = {(r.figure, r.end): r.row4_bn for r in wc.itertuples()}
    for lab, sc in (("union rough", R.scenario("mex")), ("A1", R.scenario("w3")), ("A3", R.scenario("w3", "union"))):
        for end in ENDS:
            got = run29(sc, end, v4=False, dump=DUMP27)[0]["cost"]
            gate(f"row-4 weights: run29 reproduces white_count.csv 'cost: {lab}' {end}", abs(got - want[(f"cost: {lab}", end)]) < 1e-3,
                 f"{got:.4f} vs {want[(f'cost: {lab}', end)]:.4f}")
    st27 = state_rows27()
    for (name, end), v in st27.items():
        gate(f"row-4 weights: the state arm reproduces white_count.csv 'delta: local whites, {name}' {end}",
             abs(v - want[(f"delta: local whites, {name}", end)]) < 1e-3, f"{v:.4f}")
    step27("0")
    for lab, fig in (("mexican_origin_rough", "cost: union rough"), ("A1_third_plus_nh_white", "cost: A1"),
                     ("A3_third_plus_nh_white_at_union_ages", "cost: A3")):
        for end in ENDS:
            gate(f"attribution step 0 is white_count.csv '{fig}' {end}",
                 abs(STEP_COST[("0", lab, end)][0] - want[(fig, end)]) < 1e-3, f"{STEP_COST[('0', lab, end)][0]:.4f}")
    stop_if_failed()

    if TAX_ON:
        print("[the case's income-tax keys]", flush=True)
        if not TAX_K:
            keys, TAX_K["_fedtax_bc"] = case_tax_keys()
            TAX_K.update(keys)
            stop_if_failed()
        R.K.update({k: v for k, v in TAX_K.items() if not k.startswith("_")})
    print(f"[the {CASE} frame: row-4 weights, the case's shares]", flush=True)
    set_frame(w4, n4, DUMP["cash"])
    ACC = accrual_params()
    UNION_SC = R.scenario("mex")
    if LINEAGE_ON:
        lineage_setup()
        stop_if_failed()
    if IPEDS_ON:
        print("[the IPEDS keys]", flush=True)
        ipeds_gates()
        stop_if_failed()
    return n4


def lineage_gates():
    """oct05: the union dumps are the September 29 case moved by v5's group-size responses, and the full dumps less
    the union dumps are the lane's added people (main_case_2026_10_05 summary.json change_at_fixed_specifications).
    oct07 (a payload with meta.items): items_gates()."""
    s = json.loads((CASE_LANE / "derived/summary.json").read_text())
    if "items" in META:
        items_gates(s)
        return
    ch, s29 = s["change_at_fixed_specifications"], s["adopted_2026_09_29"]
    m29 = json.loads((FISCAL / CASES["sept29"] / "derived/corrections.json").read_text())["meta"]
    for k in ("pension_accrual", "state_pricing", "roads_mileage_key"):
        gate(f"the case's meta.{k} is the September 29 payload's (the union's rules do not move)", META[k] == m29[k])
    c29 = json.loads((DER / "engine_lines_sept29_cash.json").read_text())
    for i, end in enumerate(ENDS):
        u = DUMP["accrual"][end]["cost_bn"]
        gate(f"accrual {end}: the union dump is the September 29 case plus the union's response move (1e-9)",
             abs(u - s29[i] - ch["union_response_move"][i]) < 1e-9, f"{u:.6f} = {s29[i]:.6f} {ch['union_response_move'][i]:+.6f}")
        got, want = LIN["accrual"][end]["cost_bn"], ch["g3plus_members"][i] + ch["whites"][i]
        gate(f"accrual {end}: the case less the union dump is the lane's added people, G3+ and white parts (1e-9)",
             abs(got - want) < 1e-9, f"{got:.6f} vs {want:.6f}")
        print(f"  cash {end}: union dump {DUMP['cash'][end]['cost_bn']:.4f} (the September 29 cash set "
              f"{c29[end]['cost_bn']:.4f}, move {DUMP['cash'][end]['cost_bn'] - c29[end]['cost_bn']:+.4f}); "
              f"added people {LIN['cash'][end]['cost_bn']:.4f}", flush=True)


def items_gates(s):
    """oct07: the payload's meta is v5's but for what its applied items change (meta_changed) and the stamps, the
    lineage's counts are v5's (the lineage item moves ages only), and the pension rule's inputs other than the item's
    ratio_net and Part A accrual are v5's; the dumps' capital components are v5's plus the items' offsets. Then, on each
    basis and end, against v5's dumps (engine_lines_oct05*.json) and the case lane's summary.json
    (change_at_fixed_specifications for the set, the items' cash blocks and v6.interactions for the cash set), 1e-9:
      case:      full7 - full5 = the case's change from v5;
      union:     union7 - union5 = the split edit sets' union parts + the union-only items' changes less their capital
                 parts (capital_*) + the union's capital-return move; that move less the union-only items' capital
                 parts lies within the split edit sets' capital parts (a scaled line moves the capital keys);
      lineage:   (full7 - union7) - (full5 - union5) = the split edit sets' lineage parts + the rest of their capital
                 parts + the lineage item + its interactions with the edit sets.
    A split edit set is one whose change splits into union, lineage and capital_return parts; a union-only item (its
    record's union_only) is the union's whole. An interaction between two edit sets has no side here, so it must be
    zero (1e-9: the case lane prints differences of order 1e-13)."""
    ch, v6 = s["change_at_fixed_specifications"], s["v6"]
    m5 = json.loads((FISCAL / CASES["oct05"] / "derived/corrections.json").read_text())["meta"]
    applied = [r for r in META["items"] if r.get("applied")]
    changed = {k for r in applied for k in r.get("meta_changed", [])}
    keep = sorted(set(m5) - changed - set(v6["payload"]["stamped"]))
    gate(f"the payload's meta is v5's but for the items' meta_changed ({', '.join(sorted(changed))}) and the stamps",
         set(META) - changed - set(v6["payload"]["stamped"]) - {"capital_return"} == set(keep) - {"capital_return"}
         and all(META[k] == m5[k] for k in keep if k != "capital_return"),
         ", ".join(k for k in keep if k != "capital_return" and META.get(k) != m5[k]))
    cr7, cr5 = META["capital_return"], m5["capital_return"]
    gate("the payload's capital_return is v5's plus the items' offset components, appended",
         {k: v for k, v in cr7.items() if k != "components"} == {k: v for k, v in cr5.items() if k != "components"}
         and cr7["components"][:len(cr5["components"])] == cr5["components"]
         and [c["id"] for c in cr7["components"][len(cr5["components"]):]] == list(ITEM_COMPONENTS))
    gate("the lineage's counts are v5's (the lineage item moves ages only)", LINEAGE["counts"] == m5["lineage"]["counts"])
    pa5 = m5["pension_accrual"]
    for k in ("se_oasdi_share", "part_a_share", "benefit_tax_receipt_bn"):
        gate(f"the pension rule's {k} is v5's", PA[k] == pa5[k])
    prev = PA.get("previous", {}).get("oct05", {})
    gate("the pension block's previous.oct05 holds v5's ratio_net and Part A accrual",
         all(prev.get(k) == pa5[k] for k in ("ratio_net", "part_a_accrual_bn")))
    edit_sets = [r["id"] for r in applied if r["kind"] == "edit_set"]
    union_only = {r["id"] for r in applied if r["kind"] == "edit_set" and r.get("union_only")}
    lineage_items = [r["id"] for r in applied if r["kind"] == "lineage"]
    gate("the payload's items are edit sets and one lineage item",
         len(lineage_items) <= 1 and len(edit_sets) + len(lineage_items) == len(applied))
    cash_meta = json.loads((CASE_LANE / "derived/corrections_cash.json").read_text())["meta"]
    cash_applied = {r["id"] for r in cash_meta["items"] if r.get("applied")}
    for b in BASES:
        base5 = {"union": json.loads((DER / f"engine_lines_oct05_union{'_cash' if b == 'cash' else ''}.json").read_text()),
                 "full": json.loads((DER / f"engine_lines_oct05{'_cash' if b == 'cash' else ''}.json").read_text())}
        sets = [i for i in edit_sets if b == "accrual" or i in cash_applied]

        def block(i):
            return ch["items"][i] if b == "accrual" else ch["items"][i]["cash"]

        def split(i, part):
            if i in union_only:
                raise SystemExit(f"[BLOCKED] item {i} is union-only: it has no split")
            return (block(i) if b == "accrual" else block(i)["split"]).get(part, [0.0, 0.0])

        def capital_parts(i):
            # the record's capital_components name their parts (the case lane of 15:03 JST); else the capital_* parts
            rec = next(r for r in applied if r["id"] == i)
            names = ({c["part"] for c in rec["capital_components"].values()} if "capital_components" in rec
                     else {k for k in block(i)["parts"] if k.startswith("capital_")})
            if bool(names) != bool(rec.get("capital")) or not names <= set(block(i)["parts"]):
                raise SystemExit(f"[BLOCKED] item {i}: capital parts without a capital block, or the reverse, or not in its parts")
            return [sum(block(i)["parts"][k][e] for k in names) for e in range(2)]

        def interaction(a, c):
            k = next((x for x in (f"{a}_x_{c}", f"{c}_x_{a}") if x in v6["interactions"]), None)
            if k is None:
                raise SystemExit(f"[BLOCKED] no interaction of {a} and {c} in summary.json v6.interactions")
            return v6["interactions"][k]["at_end_specifications_bn" if b == "accrual" else "cash_at_end_specifications_bn"]
        total = ch["total"] if b == "accrual" else v6["change_from_the_october_5_cash_set_bn"]
        for x in range(len(sets)):
            for y in range(x + 1, len(sets)):
                gate(f"{b}: the edit sets {sets[x]} and {sets[y]} do not interact (1e-9)",
                     max(abs(v) for v in interaction(sets[x], sets[y])) < 1e-9)
        for i, end in enumerate(ENDS):
            u5, f5 = base5["union"][end], base5["full"][end]
            u7, f7 = DUMP[b][end], FULL[b][end]
            gate(f"{b} {end}: the dumps' capital components are v5's plus the items' offsets",
                 [c["id"] for c in u7["capital"]] == [c["id"] for c in f7["capital"]]
                 == [c["id"] for c in u5["capital"]] + list(ITEM_COMPONENTS))
            gate(f"{b} {end}: the case less v5 is the case lane's change from v5 (1e-9)",
                 abs((f7["cost_bn"] - f5["cost_bn"]) - total[i]) < 1e-9, f"{f7['cost_bn'] - f5['cost_bn']:+.9f} vs {total[i]:+.9f}")
            dcap = u7["capital_bn"] - u5["capital_bn"]
            split_sets = [j for j in sets if j not in union_only]
            cap = sum(split(j, "capital_return")[i] for j in split_sets)
            uo_cap = sum(capital_parts(j)[i] for j in sets if j in union_only)
            union = (sum(split(j, "union")[i] for j in split_sets)
                     + sum(block(j)["total"][i] - capital_parts(j)[i] for j in sets if j in union_only))
            gate(f"{b} {end}: the union dump less v5's is the edit sets' union parts plus its capital-return move (1e-9)",
                 abs(u7["cost_bn"] - u5["cost_bn"] - union - dcap) < 1e-9,
                 f"{u7['cost_bn'] - u5['cost_bn']:+.9f} = {union:+.9f} {dcap:+.9f}")
            gate(f"{b} {end}: the union's capital-return move, less the union-only items' capital, lies within the split "
                 "edit sets' capital parts", (dcap - uo_cap) * cap >= 0 and abs(dcap - uo_cap) <= abs(cap) + 1e-12,
                 f"{dcap - uo_cap:+.9f} of {cap:+.9f} (union-only capital {uo_cap:+.9f})")
            want = (sum(split(j, "lineage")[i] for j in split_sets) + cap - (dcap - uo_cap)
                    + sum(block(j)["total"][i] + sum(interaction(j, k)[i] for k in sets) for j in lineage_items))
            got = (f7["cost_bn"] - u7["cost_bn"]) - (f5["cost_bn"] - u5["cost_bn"])
            gate(f"{b} {end}: the added people less v5's are the items' lineage parts, the lineage item and its "
                 "interactions (1e-9)", abs(got - want) < 1e-9, f"{got:+.9f} vs {want:+.9f}")
            print(f"  {b} {end}: union dump {u7['cost_bn']:.4f} (v5 {u5['cost_bn']:.4f}, {u7['cost_bn'] - u5['cost_bn']:+.4f}); "
                  f"added people {LIN[b][end]['cost_bn']:.4f} (v5 {f5['cost_bn'] - u5['cost_bn']:.4f}, {got:+.4f})", flush=True)


def main(case="sept29"):
    use_case(case)
    n4 = setup()
    scen = scenarios()
    res = {}
    for b in BASES:
        for end in ENDS:
            for lab, sc in scen.items():
                r, rows, bk, terms, acc = run29(sc, end, b)
                if TAX_ON:     # the CPS-dollar rule, the central before round 2
                    r["cost_cps"] = r["cost"] if sc == "eng" else run29(sc, end, b, "cps")[0]["cost"]
                r["cost_top_tail_proportional"] = r["cost"] if sc == "eng" else run29(sc, end, b, "prop")[0]["cost"]
                r["cost_capital_taxes_respond"] = run29(sc, end, b, cap=True)[0]["cost"]
                # on the case's keys the top tail is inside the central, so both arms are the capital arm
                r["cost_both_arms"] = (r["cost_capital_taxes_respond"] if TAX_ON else r["cost"] if sc == "eng"
                                       else run29(sc, end, b, "prop", True)[0]["cost"])
                r["cost_others_at_national_prices"] = r["cost"] if sc == "eng" else run29(sc, end, b, rule4="union")[0]["cost"]
                res[(b, lab, end)] = (r, rows, bk, terms, acc)
    stop_if_failed()
    summary, bucket_rows, term_rows = [], [], []
    for (b, lab, end), (r, rows, bk, terms, acc) in res.items():
        u = res[(b, "mexican_origin_rough", end)][0]
        eg = res[(b, "mexican_origin_engine", end)][0]
        summary.append({"basis": b, "group": lab, "end": end, "spec": DUMP[b][end]["spec"],
                        **{k: f"{v:.4f}" for k, v in r.items() if k not in ("population", "pop_share")},
                        "population": f"{r['population']:.0f}", "pop_share": f"{r['pop_share']:.6f}",
                        "cost_per_member": f"{r['cost'] * 1e9 / r['population']:.0f}",
                        "delta_like_for_like_bn": f"{u['cost'] - r['cost']:.4f}",
                        "delta_vs_engine_union_bn": f"{eg['cost'] - r['cost']:.4f}",
                        **({"delta_like_for_like_cps_bn": f"{u['cost_cps'] - r['cost_cps']:.4f}"} if TAX_ON else {}),
                        "delta_like_for_like_top_tail_proportional_bn": f"{u['cost_top_tail_proportional'] - r['cost_top_tail_proportional']:.4f}",
                        "delta_like_for_like_capital_taxes_respond_bn": f"{u['cost_capital_taxes_respond'] - r['cost_capital_taxes_respond']:.4f}",
                        "delta_like_for_like_both_arms_bn": f"{u['cost_both_arms'] - r['cost_both_arms']:.4f}",
                        "delta_like_for_like_others_at_national_prices_bn":
                            f"{u['cost_others_at_national_prices'] - r['cost_others_at_national_prices']:.4f}"})
        ub = res[(b, "mexican_origin_rough", end)][2]
        for bucket in list(BUCKETS) + [R.PER_HEAD, "capital return", "production gain (subtracted)"]:
            v = bk.get(bucket, 0.0)
            bucket_rows.append({"basis": b, "group": lab, "end": end, "bucket": bucket, "cost_bn": f"{v:.4f}",
                                "per_member": f"{v * 1e9 / r['population']:.0f}",
                                "delta_vs_union_rough_bn": f"{ub.get(bucket, 0.0) - v:.4f}"})
        if terms is not None and b == "accrual":
            term_rows.append({"group": lab, "end": end, **{f"index_{k}": f"{v:.6f}" for k, v in terms["index"].items()},
                              "rho_miles": f"{terms['rho']:.6f}", "under5_share": f"{terms['u5']:.6f}",
                              "miles_share": f"{terms['s_vmt']:.6f}", "k_road": f"{terms['k_road']:.6f}",
                              "k_consumption": f"{terms['k_cons']:.6f}", "k_earnings": f"{terms['k_old']:.6f}",
                              **{f"{k}_bn": f"{v:.4f}" for k, v in terms["lines"].items()},
                              "gasoline_shift_bn": f"{terms['gasoline_shift']:.4f}", "licences_bn": f"{terms['licences']:.4f}",
                              **({f"accrual_{k}_bn": f"{v:.4f}" for k, v in acc.items()} if acc else {})})
    st, st_buckets = [], []
    for b in BASES:
        rows_b, bk_b = state_rows(b)
        st += rows_b
        st_buckets += bk_b
    groups = {lab: scen[lab] for lab in ATTR_GROUPS}
    alt_rows = alternatives(groups)
    attr_rows = attribution(groups)
    for r in attr_rows:     # FINAL_STEPS: the steps that are the case's runs
        if r["step"] in FINAL_STEPS:
            want = res[(FINAL_STEPS[r["step"]], r["group"], r["end"])][0]["cost"]
            gate(f"attribution step {r['step']} is the {CASE} run {r['group']} {r['end']}", abs(float(r["cost_bn"]) - want) < 5e-5)
        if TAX_ON and r["step"] == "4":
            want = res[("accrual", r["group"], r["end"])][0]["cost_cps"]
            gate(f"attribution step 4 is the {CASE} run on the CPS-dollar rule {r['group']} {r['end']}",
                 abs(float(r["cost_bn"]) - want) < 5e-5)
    for r in alt_rows:
        if r["rule"] == "rule 4":
            want = res[(r["basis"], r["group"], r["end"])][0]["cost_others_at_national_prices"]
            gate(f"rule 4's alternative is the summary's others-at-national-prices cost {r['group']} {r['basis']} {r['end']}",
                 abs(float(r["cost_bn"]) - want) < 5e-5)
    ipeds = ipeds_rows(scen) if IPEDS_ON else None
    if ipeds:
        for r in ipeds:
            want = res[(r["basis"], r["group"], r["end"])][0]["cost"]
            gate(f"the IPEDS terms' cost is the summary's {r['group']} {r['basis']} {r['end']}", abs(float(r["cost_bn"]) - want) < 5e-5)
    stop_if_failed()
    if LINEAGE_ON:
        hl = headline_lineage(summary, st, n4)     # its identified pass runs gates of its own; nothing is written yet
        stop_if_failed()
    write(f"rekey_summary_{CASE}.csv", summary)
    write(f"rekey_buckets_{CASE}.csv", bucket_rows)
    write(f"state_buckets_{CASE}.csv", st_buckets)
    write(f"state_summary_{CASE}.csv", st)
    write(f"v4_group_terms_{CASE}.csv", term_rows)
    write(f"rule_alternatives_{CASE}.csv", alt_rows)
    write(f"attribution_{CASE}.csv", attr_rows)
    write(f"attribution_buckets_{CASE}.csv", attribution_buckets(groups))
    if ipeds:
        write(f"ipeds_terms_{CASE}.csv", ipeds)
    if TAX_ON:
        write(f"income_tax_keys_{CASE}.csv", tax_key_rows(scen))
        write(f"cps_tax_totals_{CASE}.csv", cps_tax_totals())
    if LINEAGE_ON:
        write(f"headline_{CASE}.csv", hl)
        print(pd.DataFrame(hl).to_string(index=False))
    else:
        headline(summary, st, n4)
    a = pd.DataFrame(alt_rows)
    print(a.query("group == 'A1_third_plus_nh_white'")[["rule", "basis", "end", "cost_bn", "change_bn", "delta_like_for_like_bn",
                                                         "delta_change_bn"]].to_string(index=False))
    t = pd.DataFrame(attr_rows)
    print(t.query("group == 'A1_third_plus_nh_white'")[["step", "basis", "end", "cost_bn", "delta_like_for_like_bn",
                                                        "delta_change_bn"]].to_string(index=False))


def write(name, rows):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def headline(summary, st, n4):
    """The four figures ladder 263 / 274 quote, on the sept29 case, beside their September 27 row-4 values."""
    s = pd.DataFrame(summary)
    t = pd.DataFrame(st)
    wc = pd.read_csv(BASIS / "white_count.csv").set_index(["figure", "end"])

    def d(b, lab, end):
        return float(s.query("basis == @b and group == @lab and end == @end").delta_like_for_like_bn.iloc[0])

    def sd(b, region, end, col="delta_union_ages_bn"):
        return float(t.query("basis == @b and region == @region and end == @end")[col].iloc[0])

    rows = []
    for end in ENDS:
        figs = [("age artefact removed: A1 third-plus whites, accrual (central)", d("accrual", "A1_third_plus_nh_white", end),
                 wc.loc[("delta: A1, accrual (payable)", end), "row4_bn"]),
                ("age artefact removed: A3 white rates at union ages, accrual", d("accrual", "A3_third_plus_nh_white_at_union_ages", end), ""),
                ("age artefact removed: A3 white rates at union ages, cash", d("cash", "A3_third_plus_nh_white_at_union_ages", end),
                 wc.loc[("delta: A3, cash, union ages", end), "row4_bn"]),
                ("raw cash at white ages: A1, cash set", d("cash", "A1_third_plus_nh_white", end),
                 wc.loc[("delta: A1, cash, white ages", end), "row4_bn"]),
                ("local whites state by state, union ages, accrual (central)", sd("accrual", "sum of CA, TX and rest", end), ""),
                ("local whites state by state, union ages, cash", sd("cash", "sum of CA, TX and rest", end),
                 wc.loc[("delta: local whites, sum of CA, TX and rest", end), "row4_bn"])]
        for name, v, v27 in figs:
            rows.append({"figure": name, "end": end, "sept29_bn": f"{v:.4f}", "per_member": f"{v * 1e9 / n4:.0f}",
                         "sept27_row4_bn": "" if v27 == "" else f"{float(v27):.4f}"})
        for b in BASES:
            ca = t.query("basis == @b and region == 'California' and end == @end").iloc[0]
            v27 = wc.loc[("delta: local whites, California", end)]
            rows.append({"figure": f"California per union member, union ages, {b}", "end": end,
                         "sept29_bn": ca.delta_union_ages_bn, "per_member": ca.delta_union_ages_per_person,
                         "sept27_row4_bn": f"{v27.row4_bn:.4f}" if b == "cash" else ""})
    write("headline_sept29.csv", rows)
    print(pd.DataFrame(rows).to_string(index=False))


HEADLINE_FIGURES = [("age artefact removed: A1 third-plus whites, accrual (central)", "accrual", "A1_third_plus_nh_white"),
                    ("age artefact removed: A3 white rates at union ages, accrual", "accrual", "A3_third_plus_nh_white_at_union_ages"),
                    ("age artefact removed: A3 white rates at union ages, cash", "cash", "A3_third_plus_nh_white_at_union_ages"),
                    ("raw cash at white ages: A1, cash set", "cash", "A1_third_plus_nh_white"),
                    ("local whites state by state, union ages, accrual (central)", "accrual", None),
                    ("local whites state by state, union ages, cash", "cash", None)]


def headline_lineage(summary, st, n4):
    """oct05: the headline's figures with both sides on the lineage's 42,752,213, beside the same comparison on the
    identified union at v5's responses (both sides on 39,712,493, the overlay off) and the sept29 file's values."""
    s, t = pd.DataFrame(summary), pd.DataFrame(st)
    n_case = n4 + LINEAGE["counts"]["added"]
    with identified():
        g = {lab: ATTR_GROUPS[lab]() for lab in ("mexican_origin_rough", "A1_third_plus_nh_white",
                                                 "A3_third_plus_nh_white_at_union_ages")}
        d_id = {(b, lab, end): run29(g["mexican_origin_rough"], end, b)[0]["cost"] - run29(g[lab], end, b)[0]["cost"]
                for b in BASES for lab in g for end in ENDS}
        t_id = pd.DataFrame([row for b in BASES for row in state_rows(b)[0]])
    h29 = pd.read_csv(DER / "headline_sept29.csv").set_index(["figure", "end"])
    # oct07: also each earlier lineage case's figure (headline_oct05.csv), beside the sept29 one
    earlier = {c: pd.read_csv(DER / f"headline_{c}.csv", dtype=str).set_index(["figure", "end"])
               for c in LINEAGE_CASES[:LINEAGE_CASES.index(CASE)]}

    def state(frame, b, region, end):
        return frame.query("basis == @b and region == @region and end == @end").iloc[0]

    def beside(name, end):
        return {k: v for c, h in earlier.items()
                for k, v in ((f"{c}_bn", h.loc[(name, end), f"{c}_bn"]), (f"{c}_per_member", h.loc[(name, end), "per_member"]))}

    rows = []
    for end in ENDS:
        for name, b, lab in HEADLINE_FIGURES:
            if lab is None:
                v = float(state(t, b, "sum of CA, TX and rest", end).delta_union_ages_bn)
                v_id = float(state(t_id, b, "sum of CA, TX and rest", end).delta_union_ages_bn)
            else:
                v = float(s.query("basis == @b and group == @lab and end == @end").delta_like_for_like_bn.iloc[0])
                v_id = d_id[(b, lab, end)]
            p = h29.loc[(name, end)]
            rows.append({"figure": name, "end": end, f"{CASE}_bn": f"{v:.4f}", "per_member": f"{v * 1e9 / n_case:.0f}",
                         "identified_bn": f"{v_id:.4f}", "identified_per_member": f"{v_id * 1e9 / n4:.0f}",
                         **beside(name, end), "sept29_bn": f"{p.sept29_bn:.4f}", "sept29_per_member": f"{p.per_member:.0f}"})
        for b in BASES:
            name = f"California per union member, union ages, {b}"
            ca, ca_id, p = state(t, b, "California", end), state(t_id, b, "California", end), h29.loc[(name, end)]
            rows.append({"figure": name, "end": end, f"{CASE}_bn": ca.delta_union_ages_bn,
                         "per_member": ca.delta_union_ages_per_person, "identified_bn": ca_id.delta_union_ages_bn,
                         "identified_per_member": ca_id.delta_union_ages_per_person, **beside(name, end),
                         "sept29_bn": f"{p.sept29_bn:.4f}", "sept29_per_member": f"{p.per_member:.0f}"})
    return rows


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=list(CASES),
                    help="sept29 (default), oct05 (v5, the lineage on both sides) or oct07 (v6, v5 plus its items)")
    main(ap.parse_args().case)

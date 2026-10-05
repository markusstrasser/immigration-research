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
and, after engine_lines.cjs oct05 / oct05_cash / oct05_union / oct05_union_cash, the same with --case oct05.
"""
from __future__ import annotations

import csv
import json
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
CASES = {"sept29": "main_case_2026_09_29", "oct05": "main_case_2026_10_05"}
LINEAGE_CASES = ("oct05",)
V4_SPEND = ["roads_vmt_sl", "roads_vmt_fed", "state_price_public_order_safety", "state_price_health_services",
            "state_price_recreation_culture"]
SP_FUNCTIONS = V.CENTRAL                      # the state lane's central package, by parent line
SL_AMOUNT = pd.read_csv(FISCAL / "state_priced_services_2026_09_29/derived/corrections.csv").set_index("function").sl_amount_bn
NEW_RECEIPTS = {"housing_enterprise_surplus": "house", "tenant_occupied_property": "rent"}
# Rule 2's alternative: the rough keys of the lines v4 split them from (enterprise_surplus, remaining_production_property)
PARENT_KEYS = {"housing_enterprise_surplus": "pc", "tenant_occupied_property": "capinc"}
BENEFIT_TAX_RULE = "shared"   # rule 3: the shared rule at both ends; "by_end" (rule 3b's alternative): the case's per end
REL_UNION = 0.5233824966647924     # the union's measured relative benefit-tax rate (pension lane, accrual_white.py)


def use_case(case):
    """Point the library at a case: its dumps, payload meta and bands. sept29 at import; an importer that re-keys
    another case calls this before setup(). For oct05 DUMP holds the identified union at v5's responses (the
    engine_lines.cjs oct05_union dumps: the 39.71M the CPS keys see), FULL the case itself, and LIN the added people's
    part of every line, of the capital return and of the production term (FULL less DUMP)."""
    global CASE, CASE_LANE, DUMP, FULL, LIN, LINEAGE, META, PA, SPM, RD, BANDS, ORACLE, SP_LINES, FP, U5, RHO, GAS, LIC
    global HWY_N, SE_SHARE, PART_A_SHARE, STEPS, LINEAGE_ON
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
    STEPS = STEPS_SEPT29
    FULL = LIN = LINEAGE = None
    LINEAGE_ON = False
    if case in LINEAGE_CASES:
        FULL = {"accrual": json.loads((DER / f"engine_lines_{case}.json").read_text()),
                "cash": json.loads((DER / f"engine_lines_{case}_cash.json").read_text())}
        LINEAGE = META["lineage"]
        LIN = {b: {end: lineage_part(FULL[b][end], DUMP[b][end]) for end in ENDS} for b in BASES}
        STEPS = STEPS_SEPT29[:2] + STEPS_IDENTIFIED + [STEP_LINEAGE]
        LINEAGE_ON = True


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
R.KTOT["rent"] = float((R.w * R.K["rent"]).sum())
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
    wr = {(r["group"], r["scenario"]): r for r in csv.DictReader(open(DER / "accrual_ratios.csv"))}
    br = {(r["group"], r["entry_rule"], r["scenario"]): r for r in csv.DictReader(open(BLACK_LANE / "derived/accrual_ratios.csv"))}
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
def run29(sc, end, basis="accrual", top="cps", cap=False, v4=True, dump=None, union_sc=None, rule4="all"):
    """rekey_white.run on a case dump, with the sept29 rules when v4 (a September 27 dump with v4=False reproduces
    run()). sc: a scenario or 'eng' (the engine's own amounts). union_sc: the whole rough union, for union pieces.
    rule4: 'all' (rule 4 for every group); 'union' (its alternative: other groups at national prices and the
    September 27 road keys, the union keeping its state-price and road terms); 'none' (no group, the union included:
    the attribution's first sept29 step)."""
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
    for ln in lines:
        side, lid = ln["side"], ln["id"]
        k = side + "|" + lid
        nat[k], resp[k] = ln["national_bn"], ln["response"]
        if g == "eng" or (lid in R.ADJUST and g == "mex"):
            a = ln["amount_bn"]
        elif lid in R.ADJUST:
            a = 0.0
        elif v4 and lid in V4_SPEND:
            a = terms["lines"][lid] if items else 0.0
        elif v4 and side == "receipts" and lid in NEW_RECEIPTS:
            a = ln["national_bn"] * sc["share"][NEW_RECEIPTS[lid]]
        else:
            a = ln["national_bn"] * R.line_share(sc, side, lid, top)
        if cap and lid in (CAP29 if v4 else R.CAP_LINES):
            a = ln["national_bn"] * (R.scenario("mex") if g == "eng" else sc)["share"][(CAP29 if v4 else R.CAP_LINES)[lid]]
            resp[k] = 1.0
        amt[k] = a
    acc = None
    if items:
        amt["receipts|general_sales_tax"] *= terms["index"]["sales"]
        amt["receipts|excise_selective_sales"] += terms["gasoline_shift"]
        amt["receipts|personal_motor_vehicle"] = terms["licences"]
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
        if cid.startswith("pos"):
            k = sc["external"]["public_order_safety"] if g not in ("eng", "mex") else c["key"]
        elif cid.startswith("health"):
            k = sc["external"]["health_services"] if g not in ("eng", "mex") else c["key"]
        elif items and cid in ("hwy_sl", "hwy_fed"):
            k = terms["k_road"]
        elif v4 and cid == "ent_housing_sl":
            k = sg["house"]
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
    r, rows, buckets, _, _ = run29(sc, end, basis, "prop" if arms else "cps", arms, union_sc=union_sc)
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
        args = ("prop", True) if arms else ()
        r1, _, b1, _, _ = run29(sc_union, end, basis, *args)
        with identified():
            r0, _, b0, _, _ = run29(sc_union, end, basis, *args)
        out[arms] = (r1["cost"] - r0["cost"], {b: b1.get(b, 0.0) - b0.get(b, 0.0) for b in set(b1) | set(b0)})
    return out


def state_rows(basis):
    """Part F on the case: rows per region and end, and the low end's buckets. oct05: each union piece carries the
    added people's cost in proportion to its share of the identified G3+ persons, and its white pieces are on the
    piece's lineage count at the piece's lineage ages [ASSUMPTION: the added people live where the identified G3+ do,
    at their ages, as PI_LINEAGE places them nationally]."""
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
            if LINEAGE_ON:
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


def lineage_setup():
    """oct05, once the frame is the case's: the identified G3+ (gated to the lineage's count) and PI_LINEAGE
    [ASSUMPTION: the added people at the identified G3+ members' ages, as the lineage lane prices them]."""
    global G3_CPS, PI_LINEAGE
    d = R.d
    g3 = (d.PRCITSHP.isin([1, 2, 3]) & d.PEFNTVTY.isin(R.US) & d.PEMNTVTY.isin(R.US) & d.PRDTHSP.eq(1)).to_numpy()
    n3 = float(R.w[g3].sum())
    gate("the frame's identified G3+ is the lineage's identified_g3plus (1 person)",
         abs(n3 - LINEAGE["counts"]["identified_g3plus"]) <= 1.0, f"{n3:,.3f} vs {LINEAGE['counts']['identified_g3plus']:,.3f}")
    gate("the identified G3+ is inside the union", not (g3 & ~R.MASK["mex"]).any())
    wl = R.w * R.MASK["mex"] + R.w * g3 * (LINEAGE["counts"]["added"] / n3)
    got = float(wl.sum())
    gate("the union with the added people at G3+ weights is the lineage population (2 persons, the frame's union gate)",
         abs(got - LINEAGE["counts"]["lineage_population"]) < 2, f"{got:,.3f} vs {LINEAGE['counts']['lineage_population']:,.3f}")
    G3_CPS, PI_LINEAGE = g3, R.structure(np.ones(len(wl), bool), wl, R.cage)


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
    ("rule 3a", "every group at the union's accrual per tax dollar (OASDI gross 1.018378, Part A 1.460946 per HI tax "
                "dollar), with its own benefit-tax rate and timing", ("accrual",)),
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
    oct05: steps 1-3 rebuild the groups on the identified union (39,712,493, the overlay off); step 4 is the case."""
    lineage = LINEAGE_ON
    with identified():
        base = {lab: ATTR_GROUPS[lab]() for lab in groups} if lineage else groups
        for lab, sc in base.items():
            for end in ENDS:
                for step, basis, rule4 in (("1", "cash", "none"), ("2", "cash", "all"), ("3", "accrual", "all")):
                    r, _, bk, _, _ = run29(sc, end, basis, rule4=rule4)
                    STEP_COST[(step, lab, end)] = (r["cost"], r["population"], bk)
    if lineage:
        f = (R.TARGET + LINEAGE["counts"]["added"]) / R.TARGET
        for lab, sc in groups.items():
            for end in ENDS:
                r, _, bk, _, _ = run29(sc, end, "accrual")
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
                handled = (ln["id"] in R.ADJUST or ln["id"] in V4_SPEND or ln["id"] in NEW_RECEIPTS
                           or (R.RECEIPT_KEY if ln["side"] == "receipts" else R.SPEND_KEY).get(ln["id"])
                           or ln["id"] in ("education_services", *S.EXT))
                if not handled:
                    gate(f"{b} {end}: line {ln['side']}|{ln['id']} has a key", False)
                if abs(ln["national_bn"]) < 1e-9 and abs(ln["amount_bn"]) > 1e-9 and ln["id"] not in R.ADJUST and ln["id"] not in V4_SPEND:
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

    print(f"[the {CASE} frame: row-4 weights, the case's shares]", flush=True)
    set_frame(w4, n4, DUMP["cash"])
    ACC = accrual_params()
    UNION_SC = R.scenario("mex")
    if LINEAGE_ON:
        lineage_setup()
        stop_if_failed()
    return n4


def lineage_gates():
    """oct05: the union dumps are the September 29 case moved by v5's group-size responses, and the full dumps less
    the union dumps are the lane's added people (main_case_2026_10_05 summary.json change_at_fixed_specifications)."""
    s = json.loads((CASE_LANE / "derived/summary.json").read_text())
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


def main(case="sept29"):
    use_case(case)
    n4 = setup()
    scen = scenarios()
    res = {}
    for b in BASES:
        for end in ENDS:
            for lab, sc in scen.items():
                r, rows, bk, terms, acc = run29(sc, end, b)
                r["cost_top_tail_proportional"] = r["cost"] if sc == "eng" else run29(sc, end, b, "prop")[0]["cost"]
                r["cost_capital_taxes_respond"] = run29(sc, end, b, cap=True)[0]["cost"]
                r["cost_both_arms"] = r["cost"] if sc == "eng" else run29(sc, end, b, "prop", True)[0]["cost"]
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
    final = {"4": "accrual"} if LINEAGE_ON else {"2": "cash", "3": "accrual"}    # the steps that are the case's runs
    for r in attr_rows:
        if r["step"] in final:
            want = res[(final[r["step"]], r["group"], r["end"])][0]["cost"]
            gate(f"attribution step {r['step']} is the {CASE} run {r['group']} {r['end']}", abs(float(r["cost_bn"]) - want) < 5e-5)
    for r in alt_rows:
        if r["rule"] == "rule 4":
            want = res[(r["basis"], r["group"], r["end"])][0]["cost_others_at_national_prices"]
            gate(f"rule 4's alternative is the summary's others-at-national-prices cost {r['group']} {r['basis']} {r['end']}",
                 abs(float(r["cost_bn"]) - want) < 5e-5)
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

    def state(frame, b, region, end):
        return frame.query("basis == @b and region == @region and end == @end").iloc[0]

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
                         "sept29_bn": f"{p.sept29_bn:.4f}", "sept29_per_member": f"{p.per_member:.0f}"})
        for b in BASES:
            name = f"California per union member, union ages, {b}"
            ca, ca_id, p = state(t, b, "California", end), state(t_id, b, "California", end), h29.loc[(name, end)]
            rows.append({"figure": name, "end": end, f"{CASE}_bn": ca.delta_union_ages_bn,
                         "per_member": ca.delta_union_ages_per_person, "identified_bn": ca_id.delta_union_ages_bn,
                         "identified_per_member": ca_id.delta_union_ages_per_person, "sept29_bn": f"{p.sept29_bn:.4f}",
                         "sept29_per_member": f"{p.per_member:.0f}"})
    return rows


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=list(CASES), help="sept29 (default) or oct05 (v5, the lineage on both sides)")
    main(ap.parse_args().case)

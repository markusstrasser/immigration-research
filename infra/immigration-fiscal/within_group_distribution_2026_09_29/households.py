"""Step 2: the September 27 case distributed over the union's households, conventions A and B.

Input: _cache/lines.json from export_lines.cjs (each generation's corrected lines at the case's two band ends:
specification 48, shared allocation, the low end; specification 11, personal allocation, the high end).
Rule: within each generation, each line's corrected amount is spread over that generation's persons in
proportion to the line's own key vector at the end's allocation (the account's definitions: the CPS, MEPS and
school keys that generation_account_2026_09_24/keys.py rebuilds and gates, imported read-only). This keeps each
generation's total, and so the union's, exactly; within a generation it is first order: a correction that in
truth falls on a subset (the SSN rule on credits, status-based compliance) is spread over the whole key.
  - public order by use: the generation's amount splits into its per-head part and its custody, arrest and ICE
    part in the proportions of the use key's components (generation_key_shares.json meta.use_parts, convention
    a); per head over all members, the rest over members aged 18-64 (the key's own base; the incarcerated are
    outside the household frame, so within a generation "use" cannot follow individuals);
  - Medicaid with uninsured use: the Medicaid-key part and the uninsured part in the proportions of the
    generation's uncorrected cells (model_G*.json), the first by the MEPS Medicaid key, the second by uninsured
    person-years (NOCOV_CYR 3 = 1, 2 = 0.5, keys.py's exposure);
  - the capital return: each component by its own key rule, i.e. by the persons' amounts of its numerator lines
    (the enterprise components by the enterprise_surplus receipt, per head);
  - the production term (P + F): by positive earnings (the specification's proxy) within the skill cells, the
    generation lane's Aumann-Shapley attribution (production.py) carried down to the worker; the cell parts are
    solved from the three generations' terms and gated;
  - the lane constants (care work, shelter, audit rows 8-10; no person-level rule): not assigned, reported as
    the residual.
Convention A: everything assigned. Convention B: taxes (every receipt but the enterprise surplus) against
transfers keyed to the household's own benefit receipt (CPS benefit amounts and SPM unit benefits, including the
income-security services line keyed to cash assistance and housing subsidies), health (MEPS use cells, Medicaid
with uninsured use, Medicare), K-12 schools
(the school part of education plus the school reprice) and justice by use (the non-per-head part); general
government, public order per head, roads and parks, other per-head services and transfers keyed per head or by
age, college and other education, the capital return, the enterprise surplus and the production term are left out.
Standard errors: the 160 ASEC replicate weights (successive difference, 4/160), re-running the within-generation
spread and every statistic per replicate with the engine's line totals held fixed.
Weights (--weights): `published`, the default, spreads over the ASEC person weights (union 40,896,574). `row4`
spreads over audit row 4's weights, the count the case prices (union 39,712,493): the Mexico-born naturalized
and noncitizen persons outside CA+TX scaled to their ACS 2024 cells by cps_imputation_keys_2026_09_23/
combine_onbooks_lane.py weight_arms, arm "row4", called as population_basis_2026_09_29/frame_counts.py calls it
but on all 161 columns (every step acts column by column, so the replicates come from the same call). Beyond the
weights, two generation-level inputs follow the count: the per-head part of public order moves with each
generation's share of the civilian frame, as the engine's row-4 correction moves it; the production term keeps
the generation lane's attribution on the published weights, as the case keeps the term at its published value.
Gates (exit 1, nothing written): the union count reproduces main_case_decomposition_2026_09_29/derived/
headcount.csv (1 person); key totals reproduce generation_keys.csv by generation (1e-9 relative; on row 4, G2
and G3+ there, whose weights row 4 leaves, and the union the decomposition lane's row-4 age_bins.csv);
production cell parts close (1e-6 bn); every generation's assigned amounts plus its residual equal its cost
(1e-6 bn); households plus the residual reproduce the case at both ends (1e-6 bn); on row 4, the per-head
part's change reproduces the engine's (stack_by_generation.json, 1e-6 bn) and every per-head line charges each
generation the same per member (1e-9 relative); one reference person per household; the status imputation
reproduces its published Mexico-born 25-64 counts (on the published weights: the flag does not use weights).
Sensitivity A_schools_per_head: convention A with the school dollars spread per head over the union instead of
charged to the pupils' households.
--case sept29 (the main case adopted on 2026-09-29, main_case_2026_09_29; with --weights row4 only, the count the case
prices) reads _cache/sept29/lines.json (export_lines.cjs --case sept29) and writes derived/sept29/ and _cache/sept29/;
the September 27 files do not move. Its new lines take these person rules, each carried down from the generation
account's own v4 split (run_generations_v4.cjs, v4_split.cjs):
  - the pension switch (a new category, pension_accrual, in B: the members' own contributions earn it): social_security
    is the accrual, spread by the persons' OASDI receipts (employee and employer OASDI on their key plus
    se_oasdi_share of self-employment tax on its key), since each generation's accrual is its accrual per tax dollar
    times its OASDI receipts; medicare's Part A accrual likewise by HI receipts, its benefits (the cash set's less the
    Part A share) by the Medicare key; the federal income tax falls by the tax on benefits, spread by the Social
    Security benefit key, and the rest stays on its own key;
  - roads keyed by miles (roads_vmt_*): the driver-mile piece over persons aged 5 and over (each at the union's miles),
    the freight piece on the excise line's consumption key and the old-key piece on economic affairs' key (candidate
    v4's withRoads formula, split and gated in the export);
  - state pricing (state_price_*): the parent line's split (public order: per head and by use), since each
    generation's gap is the union's price index on its own parent amount;
  - public housing's deficit (receipt housing_enterprise_surplus): the housing-assistance key, as a transfer;
  - the tax on tenant-occupied housing (receipt tenant_occupied_property): persons in homes rented for cash, weighted
    by their state's group rent per such union member (the generation account's rule, v4_inputs.py tenant_share;
    gated to its generation shares);
  - part-rekeyed capital (the highway components): the parent line's part by the parent's split and the correction
    line's part by the road line's pieces;
  - production: the cell parts are solved on the row-4 labor shares, where the generation account attributes the
    case's row-4 grid (v4_inputs.py).
--accrual person (with --case sept29; the lead's arm of 2026-09-30) spreads each generation's two pension pieces, its
Social Security accrual and its Part A accrual, over its members by the pension lane's person model instead
(person_accrual.py: _cache/sept29/person_accrual.parquet), and beside it by three steps between the rules
(PERSON_ARMS: the on-books tax base, the unauthorized's 10% claim share, the benefit formula for Social Security).
Two arms also key the payroll taxes on on-books wages, where the account keys them on all wages: ONBOOKS_CENTRAL, the
person arm so keyed (the lane's central since 2026-09-30), and FULL_CLAIM, the same with the unauthorized credited in
full, which asks whether the status rows turn on the 10% claim share or on on-books pay. Each generation keeps its
accrual and its payroll taxes, so the union keeps the case's: Social Security ratio_net x the account's OASDI
receipts, Part A the payload's part_a_accrual_bn. The run computes the flat arm too, stops unless it reproduces the
files the flat run wrote in derived/sept29/ byte for byte, and writes only new files there: net_positive_shares,
concentration, household_balance_quantiles, category_means and control with the suffix _person_accrual, and
person_accrual_arms.csv (every arm's shares, each against the flat arm with its replicate standard error). Its status
rows add the case's own flag (head_status_case_flag: the state-aware status the case's on-books share and the
accrual's 10% claim share read, cps_ca_status via the pension lane's frame).
--accrual person --payroll onbooks writes the central's five files instead, with the suffix _person_onbooks, and
_cache/sept29/households_person_onbooks.parquet. It stops unless its flat arm, its person arm and its arms comparison
reproduce, byte for byte, the files the two runs before it wrote.
--case oct05 (the main case adopted on 2026-10-05, main_case_2026_10_05: v4 plus the lineage, 3.04M descendants who no
longer report Mexican origin, priced on G3+) runs as sept29 on _cache/oct05/lines.json (export_lines.cjs --case oct05)
and writes derived/oct05/ and _cache/oct05/; every --accrual and --payroll arm runs on it too. The added people are not
in the CPS as Mexican-origin, so they are placed [ASSUMPTION] at the identified G3+ members' composition: every G3+
record's weight, in every replicate, is scaled by f = 1 + added / identified G3+ (1.2119), so they sit in the same
households, ages, keys and statuses. G3+'s lines, which carry the lineage, are spread over the scaled records, so each
G3+ record carries the blend of the identified and the added people's per-member amounts. The gates on the key vectors,
the tenant key, public order's per-head part and the production solve run on the identified weights, as on sept29. The
lineage's production term (lines.json meta.lineage) is set apart before the cell parts are solved and goes to G3+'s
two cells in proportion to its own parts. The pension gates add the lineage's own accrual, Part A and OASDI receipts
(meta.lineage.pension_bn), whose accrual per OASDI dollar is not ratio_net. The person-accrual arms reuse
_cache/sept29/person_accrual.parquet: the persons are the same.
--case oct07 (main case v6, main_case_2026_10_07: v5 plus the edit sets in its meta.items) runs as oct05 on
_cache/oct07/lines.json (export_lines.cjs --case oct07) and writes derived/oct07/ and _cache/oct07/, with three changes:
  - the added people are placed [ASSUMPTION] at the case's measured age mix (meta.lineage.age_mix, the case's item
    added_age_mix): every G3+ record's weight, in every replicate, is scaled by its five-year band's
    f_b = 1 + added_b / identified G3+_b, where added_b is the G3-rate persons and the later losses at their own mixes. The
    case prices them so (the engine's G3+ keys reweighted by band), so a G3+ record carries its own keys' amounts.
    Gated: the frame's identified G3+ mix is the case's, and the placed G3+ adults are the generation account's.
    --placement uniform (flat arm only) puts them at v5's one factor beside it, written to derived/oct07/uniform_placement/
    and _cache/oct07/uniform_placement/, so the switch's effect shows;
  - the items' capital offsets (components keyed by an item's carrier receipt lines, lines.json meta.carriers) are
    spread as their parent lines (the item's splits.split_basis, its household rule);
  - the items' cell shifts are folded into their lines' cells. A part whose split basis is the line it edits follows
    that line's rule. A part whose basis is another line (lines.json meta.routes: the K-12 weight's two parts on
    school_reprice and college_rekey, each by education_services) takes its share of its line's amount, and so of its
    cost, since a spending line costs its response x its amount, out of the line's split and spreads it as the basis
    line [ASSUMPTION, the case's splits.household_person]. The capital keyed by the line's amount spreads the same
    way. A part routed off a state-priced line's parent stops the run. derived/oct07/split_basis_moves.csv gives each
    such part's cost by category, on its own line's split and on the basis line's.
The pension gates take v6's ratio_net and Part A accrual, with the items' parts on the added people (pension_tr2026's
lineage parts) in the lineage's own. The person-accrual arms' vectors stay the September 29 parquet's (the 2025
Trustees path) [APPROX]: they only spread each generation's accrual, which is v6's.
Writes derived/net_positive_shares.csv, concentration.csv, household_balance_quantiles.csv, control.csv,
category_means.csv, line_scaling.csv and _cache/households.parquet; the row-4 run writes the same files to
derived/row4/ and _cache/row4/. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --weights row4
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --case sept29 --weights row4
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/person_accrual.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --case sept29 --weights row4 --accrual person
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --case sept29 --weights row4 --accrual person --payroll onbooks
  (the same three households.py commands with --case oct05 or --case oct07, after export_lines.cjs with that case)
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import argparse
import csv
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
GENLANE = FISCAL / "generation_account_2026_09_24"
sys.path.insert(0, str(GENLANE))
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import keys as K  # noqa: E402
from impute_status import impute  # noqa: E402
import combine_onbooks_lane as L  # noqa: E402  last: it puts two more lanes at the front of sys.path

C = F.C
OUT = HERE / "derived"
CACHE = HERE / "_cache"
DECOMP = FISCAL / "main_case_decomposition_2026_09_29/derived"
GENS = F.GENS
ENDS = ["low", "high"]
PUBLISHED_MEX_25_64 = {"borjas_paper_rules": 3.9170610819750302, "no_medicaid_rule": 4.778136460024849}
PER_HEAD_KEYS = {"population", "resident_population"}
FAILS = []
# The September 29 case (export_lines.cjs --case sept29): its lines, its tenant key's inputs and its new category.
# oct05 (v5) runs on the same rules, with the lineage placed on G3+ (LINEAGE_CASES); oct07 (v6) places it by age band
# (AGE_MIX_CASES).
CASE_DIRS = {"sept27": None, "sept29": "sept29", "oct05": "oct05", "oct07": "oct07"}
CASE_LANES = {"sept29": "main_case_2026_09_29", "oct05": "main_case_2026_10_05", "oct07": "main_case_2026_10_07"}
LINEAGE_CASES = ("oct05", "oct07")
AGE_MIX_CASES = ("oct07",)
STATES_CSV = FISCAL / "receipt_side_long_run_2026_09_28/derived/states.csv"
V4_INPUTS = GENLANE / "derived/v4_inputs.json"
CASH_RENT = 2  # H_TENURE: rented for cash
PENSION = "pension_accrual"
# --accrual person: the arms beside the flat rule, each a person vector for the two pension pieces (person_vectors).
# Two arms also key the payroll taxes on on-books wages, each with its pension vectors: ONBOOKS_CENTRAL (the person
# arm; the lane's central since 2026-09-30, written by --payroll onbooks) and FULL_CLAIM (the unauthorized credited in
# full).
PERSON_ARMS = ["tax_base", "claim_share", "oasdi_formula", "person"]
PENSION_VECTORS = PERSON_ARMS + ["person_full_claim"]
ONBOOKS_CENTRAL = "person_payroll_onbooks"
FULL_CLAIM = "person_payroll_onbooks_full_claim"
ONBOOKS_ARMS = {ONBOOKS_CENTRAL: "person", FULL_CLAIM: "person_full_claim"}
ARM_ORDER = ["flat"] + PERSON_ARMS + list(ONBOOKS_ARMS)
PERSON_SUFFIX = "_person_accrual"
ONBOOKS_SUFFIX = "_person_onbooks"
FLAT_FILES = ["net_positive_shares.csv", "concentration.csv", "household_balance_quantiles.csv", "control.csv",
              "category_means.csv", "line_scaling.csv"]
CASE_FLAG = "head_status_case_flag"
# Keys the decomposition lane's row-4 age bins do not carry: on row 4 they are pinned for G2 and G3+ only.
NO_UNION_ROW4_PIN = {("receipt", "modeled_owner_property")}
STATE_PRICE_PARENT = {"state_price_public_order_safety": "public_order_safety",
                      "state_price_health_services": "health_services",
                      "state_price_recreation_culture": "recreation_culture"}
FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA", 15: "HI",
        16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD", 25: "MA", 26: "MI",
        27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC",
        38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT",
        50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}  # GESTFIPS; v4_inputs.py STATES


def tenant_key(d, union, gens, w0):
    """The tax on tenant-occupied housing by person: union members in homes rented for cash, each weighted by the
    group's rent in their state (states.csv group_rent) over the union's members in such homes there (row-4 weights).
    A state without such members would spread its rent nationally, as the generation account's rule does. Gated to
    that rule's generation shares (v4_inputs.json tenant_share, convention a)."""
    with STATES_CSV.open() as f:
        group = {r["state"]: float(r["group_rent"]) for r in csv.DictReader(f)}
    gate("states.csv covers the 50 states and DC, as the FIPS map", sorted(group) == sorted(FIPS.values()), f"{len(group)} rows")
    rent = (d.H_TENURE.eq(CASH_RENT).to_numpy() & union).astype(float)
    st = d.GESTFIPS.to_numpy()
    x, spread = np.zeros(len(d)), 0.0
    n_nat = float(rent @ w0)
    for fips, abbr in FIPS.items():
        here = rent * (st == fips)
        n = float(here @ w0)
        if n > 0:
            x += group[abbr] * here / n
        else:
            spread += group[abbr] / n_nat
    x += spread * rent
    ref = json.loads(V4_INPUTS.read_text())["tenant_share"]
    total = float(x @ w0)
    worst = max(abs(float(x[gens[g]] @ w0[gens[g]]) / total - ref["rule"]["a"][g] / ref["rent_share"]) for g in GENS)
    gate("the tenant key's generation shares are the generation account's (v4_inputs.json tenant_share, 1e-12)",
         worst < 1e-12, f"max |diff| {worst:.1e}")
    return x


def person_vectors(d, union, gens, index):
    """The two pension pieces' person vectors under each set of PENSION_VECTORS, by piece (oasdi, part_a) and
    allocation. Within a generation each vector spreads the generation's accrual, as the flat rule's receipts do:
      tax_base           the pension lane's on-books OASDI (HI) tax: one accrual per tax dollar, as the flat rule, but
                         the unauthorized pay on the on-books share of their wages (the case's status stack), not on all
                         of them;
      claim_share        the same, with the unauthorized's at Note 151's long-run 10%;
      oasdi_formula      Social Security by the person model (the benefit formula: progressivity, family type, career
                         start, benefit-tax timing), Part A still as claim_share;
      person             the person model's net Social Security and its Part A accrual (person_accrual.py), Part A per
                         covered worker rather than per tax dollar;
      person_full_claim  the person model with the unauthorized credited in full (FULL_CLAIM's accrual).
    Every person of the frame carries a value, members or not: the shared allocation splits each SPM unit's total
    equally, as the account's shared receipt keys do, so a member's share includes the unit's non-members. Returns
    the vectors, the persons' on-books factor and state-aware unauthorized flag (the case's), and the model's record."""
    pa = pd.read_parquet(CACHE / "sept29/person_accrual.parquet")
    stale = {"oasdi_net_full_claim", "part_a_full_claim"} - set(pa.columns)
    if stale:
        raise SystemExit(f"[BLOCKED] _cache/sept29/person_accrual.parquet has no {sorted(stale)}: run person_accrual.py")
    model = json.loads((OUT / "sept29/person_accrual_model.json").read_text())
    m = d[["PH_SEQ", "A_LINENO"]].merge(pa, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one",
                                        indicator=True)
    found = (m.pop("_merge") == "both").to_numpy()
    gate("the person model covers every person of the frame", bool(found.all()) and len(pa) == len(d),
         f"{int(found.sum()):,} of {len(d):,}")
    lab = F.label(gens, len(d))
    same = (np.array_equal(m.union.to_numpy(bool), union)
            and np.array_equal(m.gen.to_numpy()[union].astype(str), np.array(GENS)[lab[union]]))
    gate("its union and generations are the account's", same)
    u = float(model["unauthorized_credit"])
    unauth = m.unauth.fillna(False).to_numpy(bool)
    num = {c: m[c].fillna(0.0).to_numpy(float)
           for c in ("tax_oasdi", "tax_hi", "oasdi_net", "part_a", "oasdi_net_full_claim", "part_a_full_claim")}
    claim = np.where(unauth, u, 1.0)
    personal = {"tax_base": {"oasdi": num["tax_oasdi"], "part_a": num["tax_hi"]},
                "claim_share": {"oasdi": num["tax_oasdi"] * claim, "part_a": num["tax_hi"] * claim},
                "oasdi_formula": {"oasdi": num["oasdi_net"], "part_a": num["tax_hi"] * claim},
                "person": {"oasdi": num["oasdi_net"], "part_a": num["part_a"]},
                "person_full_claim": {"oasdi": num["oasdi_net_full_claim"], "part_a": num["part_a_full_claim"]}}
    out = {arm: {piece: {"personal": v, "shared": C.unit_equal(v, index)} for piece, v in parts.items()}
           for arm, parts in personal.items()}
    return out, m.onbooks.fillna(1.0).to_numpy(float), unauth, model


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def sdr(values):
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


# Category of every assigned piece; B keeps the first five.
B_CATS = ["taxes", "transfers", "health", "schools", "justice_use"]
A_ONLY = ["enterprise", "transfers_per_head", "education_other", "justice_per_head", "general_government",
          "roads_parks", "other_shared", "capital", "production"]
# Spending lines are classed by their key: keyed to the household's own benefit receipt (CPS amounts, SPM unit
# benefits) = transfers; MEPS use cells = health; keyed per head or by age = per-head transfers or other shared.
HEALTH_KEYS = {"medicare", "medicaid", "health_other", "tricare", "va_medical"}
OWN_RECEIPT_KEYS = {"cash_assistance", "social_security", "ssi", "unemployment", "veterans", "workers_comp", "snap",
                    "energy", "wic", "housing_support", "refundable_credits", "all_cash"}
ROADS_PARKS = {"economic_affairs_services", "recreation_culture"}


def spending_category(row):
    i, k = row["id"], row["key"]
    if i == "general_public_services":
        return "general_government"
    if i in ROADS_PARKS:
        return "roads_parks"
    if k in HEALTH_KEYS:
        return "health"
    if k in OWN_RECEIPT_KEYS:
        return "transfers"
    if row["response_class"] == "household_transfer":
        return "transfers_per_head"
    return "other_shared"


def age_band_factors(age, g3, w_id, lineage):
    """Each record's placement factor at the case's measured age mix (lines.json meta.lineage.age_mix): its five-year
    band's f_b = 1 + added_b / identified G3+_b, added_b = the G3-rate persons x their mix_b + the later losses x
    their mix_b (meta.lineage.counts). Returns the factors by record and the bands' inputs."""
    mix_meta, counts = lineage["age_mix"], lineage["counts"]
    starts = [int(b.split("-")[0].rstrip("+")) for b in mix_meta["bands"]]
    if starts != list(range(0, 5 * len(starts), 5)) or not mix_meta["bands"][-1].endswith("+"):
        raise SystemExit("[BLOCKED] meta.lineage.age_mix: the bands are not five-year bands from 0 with an open top")
    band = np.minimum(age // 5, len(starts) - 1)
    n_id = np.array([float(w_id[g3 & (band == b)].sum()) for b in range(len(starts))])
    mix = {k: np.asarray(mix_meta["mixes"][k], float) for k in ("identified", "g3_rate", "later")}
    added_b = counts["at_g3_rate"] * mix["g3_rate"] + counts["later_losses"] * mix["later"]
    f_b = 1.0 + added_b / n_id
    return f_b[band], dict(n_id=n_id, added_b=added_b, f_b=f_b, mix_gap=float(np.abs(n_id / n_id.sum() - mix["identified"]).max()))


def main(arm, case="sept27", accrual="flat", payroll_base="all", placement="band"):
    sub = CASE_DIRS[case]
    if placement != "band" and (case not in AGE_MIX_CASES or accrual != "flat"):
        raise SystemExit("[BLOCKED] --placement uniform is the beside arm of a case placed by age band (oct07), flat arm only")
    if sub and arm != "row4":
        raise SystemExit(f"[BLOCKED] --case {case} runs on the row-4 weights only, the count the case prices")
    if accrual != "flat" and case not in CASE_LANES:
        raise SystemExit("[BLOCKED] --accrual person needs --case sept29, oct05 or oct07, the cases that carry the pension accrual")
    if payroll_base != "all" and accrual != "person":
        raise SystemExit("[BLOCKED] --payroll onbooks needs --accrual person: the central pairs the two")
    print(f"[frame] weights: {arm}" + (f"; case {case}" if sub else "") + (f"; accrual {accrual}" if accrual != "flat" else "")
          + (f"; payroll {payroll_base}" if payroll_base != "all" else ""), flush=True)
    lines = json.loads(((CACHE / sub if sub else CACHE) / "lines.json").read_text())
    v4 = case in CASE_LANES
    if v4 and lines["meta"]["case"] != CASE_LANES[case]:
        raise SystemExit(f"[BLOCKED] _cache/{sub}/lines.json is {lines['meta']['case']}'s; run export_lines.cjs --case {case}")
    lineage = lines["meta"]["lineage"] if case in LINEAGE_CASES else None
    carriers = lines["meta"].get("carriers", {})   # oct07: the items' carriers and their parent lines (export_lines.cjs)
    routes = {}   # oct07: (side, line) -> the items' parts on it whose split basis is another line (meta.routes)
    for r in lines["meta"].get("routes", []):
        if r["line"] in STATE_PRICE_PARENT.values():
            # A state-priced line spreads as its parent's own split, which a part routed off the parent would leave.
            raise SystemExit(f"[BLOCKED] {r['part']}: routed off {r['line']}, a state-priced line's parent")
        routes.setdefault((r["side"], r["line"]), []).append(r)
    PA = lines["meta"]["pension_accrual"] if v4 else None
    b_cats = B_CATS + ([PENSION] if v4 else [])   # the pension accrual is the members' own claim, so in B
    d = F.load()
    civ, union, gens = F.masks(d)
    W_pub = d[F.REPS].to_numpy(float)
    W = W_pub
    if arm == "row4":
        print("[row 4 weights]", flush=True)
        arms, info = L.weight_arms(d, W_pub, L.acs_cells())
        W = arms["row4"]
        del arms
        print(f"  row-4 factors: naturalized {info['factor_natz']:.6f}, noncitizen {info['factor_noncit']:.6f}", flush=True)
    w0 = W[:, 0]
    w_pub = W_pub[:, 0]
    out_dir, cache_dir = (OUT, CACHE) if arm == "published" else (OUT / arm, CACHE / arm)
    if sub:     # a later case writes its own directory, on the row-4 weights
        out_dir, cache_dir = OUT / sub, CACHE / sub
    if placement == "uniform":   # beside the case: v5's one factor, in a directory of its own
        out_dir, cache_dir = out_dir / "uniform_placement", cache_dir / "uniform_placement"
    index = C.spm_index(d)
    age = d.A_AGE.to_numpy()
    lab = F.label(gens, len(d))
    heads = pd.read_csv(DECOMP / "headcount.csv").query("cut == 'all' and group == 'union'")
    n_union, want = float(w0[union].sum()), float(heads[arm].iloc[0])
    gate(f"union count reproduces headcount.csv, column {arm} (1 person)", abs(n_union - want) <= 1.0,
         f"{n_union:,.3f} vs {want:,.3f}")
    # w_id: the identified union's weights. With the lineage (oct05) W and w0 place the added people on G3+'s records;
    # the gates on the key vectors, the tenant key, public order's per-head part and the production solve keep w_id.
    w_id = w0
    if lineage:
        g3 = gens["G3plus"]
        n_g3, counts = float(w0[g3].sum()), lineage["counts"]
        gate("the identified G3+ count is the lineage's identified_g3plus (1 person)", abs(n_g3 - counts["identified_g3plus"]) <= 1.0,
             f"{n_g3:,.3f} vs {counts['identified_g3plus']:,.3f}")
        w_id = w0.copy()
        if W is W_pub:
            W = W.copy()
        if case in AGE_MIX_CASES and placement == "band":
            f_rec, bands = age_band_factors(age, g3, w_id, lineage)
            # The case's mix agrees to about 1e-8 (single-precision weights there); another frame or weight would miss by ~1e-3.
            gate("the frame's identified G3+ age mix is the case's (meta.lineage.age_mix identified, 1e-7 per band)",
                 bands["mix_gap"] < 1e-7, f"max |diff| {bands['mix_gap']:.1e} over {len(bands['f_b'])} bands")
            gap = abs(float(bands["added_b"].sum()) - counts["added"])
            gate("the bands' added people add to meta.lineage.counts added (1e-6 persons)", gap < 1e-6, f"|diff| {gap:.1e}")
            W[g3, :] *= f_rec[g3][:, None]   # [ASSUMPTION] the added people at the case's measured age mix, by band, every replicate
            placed = f"G3+ records x f_b {bands['f_b'].min():.4f} to {bands['f_b'].max():.4f} by band"
        else:
            lineage_f = 1.0 + counts["added"] / n_g3
            W[g3, :] *= lineage_f   # [ASSUMPTION] the added people at the identified G3+ members' composition, every replicate
            placed = f"G3+ records x {lineage_f:.6f}"
        w0 = W[:, 0]
        n_scaled = float(w0[union].sum())
        gate("the placed union is the lineage population (1 person)", abs(n_scaled - counts["lineage_population"]) <= 1.0,
             f"{n_scaled:,.3f} = {n_union:,.3f} + {counts['added']:,.3f}; {placed}")
        if case in AGE_MIX_CASES and placement == "uniform":
            adults, want = float(w0[g3 & (age >= 18)].sum()), lineage["generation_g3plus"]["adults"]
            print(f"  beside the case: the placed G3+ adults (18 and over) are {adults:,.1f}, the generation account's {want:,.1f}", flush=True)
        elif case in AGE_MIX_CASES:
            adults, want = float(w0[g3 & (age >= 18)].sum()), lineage["generation_g3plus"]["adults"]
            gate("the placed G3+ adults (18 and over) are the generation account's, its added people's at their age mix (1 person)",
                 abs(adults - want) <= 1.0, f"{adults:,.1f} vs {want:,.1f} ({lineage['generation_g3plus']['source']})")

    print("[key vectors]", flush=True)
    rk = C.receipt_keys(d, index)
    sk = C.spending_vectors(d, index)
    owner, params = K.owner_property(d)
    medical, _, _, _ = K.meps_keys(d)
    edu = K.school_keys(d, civ, params)
    exposure_py = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    vec = {}
    for a in ("personal", "shared"):
        v = {("receipt", k): x for k, x in rk[a].items()}
        v[("receipt", "resident_population")] = np.ones(len(d))
        v.update({("spending", k): x for k, x in sk[a].items()})
        v.update({("spending", k): x for k, x in medical.items()})
        v[("spending", "school_part")] = edu[a]["school"]
        v[("spending", "P_part")] = edu[a]["P"]
        v[("spending", "postsecondary")] = edu[a]["P"]
        v[("spending", "school_operating")] = edu[a]["school"]
        vec[a] = v
    if v4:
        # The case's receipt keys that respond from September 29: public housing's deficit on the housing-assistance
        # key, the tax on tenant-occupied housing on the tenant key, and owner-occupied property tax on the generation
        # account's owner key (keys.py owner_property, SPM-shared; at response 0 until then, so never spread).
        tenant = tenant_key(d, union, gens, w_id)
        for a in vec:
            vec[a][("receipt", "housing_support")] = vec[a][("spending", "housing_support")]
            vec[a][("receipt", "renter_contract_rent")] = tenant
            vec[a][("receipt", "modeled_owner_property")] = owner
    alt = unauth_case = person_model = None
    payroll = set()
    if accrual == "person":
        print("[person accrual]", flush=True)
        alt, onbooks, unauth_case, person_model = person_vectors(d, union, gens, index)
        # ONBOOKS_ARMS: each payroll line on its own key times the person's on-books share (the status stack's 0.53
        # for the unauthorized), shared as the account shares its keys.
        payroll = set(PA["oasdi_lines"] + PA["hi_lines"] + [PA["se_line"]])
        onbooks_key = {}
        for k in {"wage_oasdi", "wage", "self_payroll"}:
            v = vec["personal"][("receipt", k)] * onbooks
            onbooks_key[k] = {"personal": v, "shared": C.unit_equal(v, index)}
    pub = pd.read_csv(GENLANE / "derived/generation_keys.csv").query("convention == 'a'")
    # Row 4 moves no weight in G2 or G3+, so their rows keep generation_keys.csv; the union's row-4 totals are the
    # decomposition lane's age bins (the same key vectors under the same weight_arms call), which pins G1 as well.
    by_gen, union_ref = GENS, None
    if arm != "published":
        by_gen = GENS[1:]
        union_ref = pd.read_csv(DECOMP / "age_bins.csv").query("weights == @arm").groupby(["allocation", "key"])["union"].sum()
    worst, checked = 0.0, 0

    def pin(r, x):
        nonlocal worst, checked
        for g in by_gen:
            want = getattr(r, g)
            worst = max(worst, abs(float(x[gens[g]] @ w_id[gens[g]]) - want) / max(abs(want), 1.0))
        if union_ref is not None and (r.side, r.key) not in NO_UNION_ROW4_PIN:
            want = float(union_ref[("both", "extra|pop") if r.key == "resident_population"
                                   else (r.allocation, f"{r.side}|{r.key}")])
            worst = max(worst, abs(float(x[union] @ w_id[union]) - want) / max(abs(want), 1.0))
        checked += 1

    for r in pub.itertuples():
        key = (r.side, r.key)
        if r.allocation not in vec or key not in vec[r.allocation]:
            continue
        pin(r, vec[r.allocation][key])
    mix = {a: vec[a][("spending", "school_part")] + vec[a][("spending", "P_part")] for a in vec}
    for r in pub.query("key == 'education_mix'").itertuples():
        pin(r, mix[r.allocation])
    ref = ("generation_keys.csv by generation" if union_ref is None
           else "G2 and G3+ generation_keys.csv, the union age_bins.csv")
    gate(f"{checked} key rows reproduce their {arm} totals: {ref} (1e-9 relative)", worst < 1e-9, f"worst {worst:.1e}")
    gaps = {"key totals (relative)": worst}

    shares = json.loads((GENLANE / "derived/generation_key_shares.json").read_text())
    use_parts = shares["meta"]["use_parts"]["a"]
    models = {g: json.loads((GENLANE / f"derived/model_{g}.json").read_text()) for g in GENS}

    # The use key's per-head part is a per-head rate times each generation's population (keys.py); the engine's row-4
    # correction moves it with the generation's share of the civilian frame. The factor is 1 on the published weights.
    pop = np.array([w0[gens[g]].sum() for g in GENS])
    pop_id = np.array([w_id[gens[g]].sum() for g in GENS])
    pop_pub = np.array([w_pub[gens[g]].sum() for g in GENS])
    per_head_factor = pop_id / pop_pub * (w_pub[civ].sum() / w_id[civ].sum())
    if arm != "published":
        comp = json.loads((GENLANE / "derived/stack_by_generation.json").read_text())["components"]["C_row4_weights"]["a"]
        engine = np.array([comp[g]["spending"]["public_order_safety"]["population"]["personal"] for g in GENS])
        moved = np.array(use_parts["per_head"]) * (per_head_factor - 1)
        gap = float(np.abs(moved - engine).max())
        gate("row 4 moves public order's per-head part as the engine does (C_row4_weights, 1e-6 bn)", gap < 1e-6,
             f"{', '.join(f'{g} {x:+.6f}' for g, x in zip(GENS, moved))} bn; max |diff| {gap:.1e}")
    # Per-head lines: the case prices them for the row-4 count, so on its weights every generation pays the same per
    # member; on the published weights the first generation pays less.
    spread = 0.0
    for end in ENDS:
        rows_g = {g: {r["id"]: r for r in lines["generations"][g][end]["rows"]} for g in GENS}
        for i, r in rows_g["G1"].items():
            per_member = np.array([rows_g[g][i]["cost_bn"] for g in GENS]) * 1e9 / pop
            if r["key"] in PER_HEAD_KEYS and np.any(per_member != 0):
                spread = max(spread, float(np.ptp(per_member) / np.abs(per_member).max()))
    if arm == "published":
        print(f"  · per-head lines per member across generations: widest relative spread {spread:.2%}", flush=True)
    else:
        # With the lineage, G3+'s per-head lines carry the added people's per-head amounts, which the lineage lane priced
        # for about 0.03 fewer people than meta.lineage counts.added: G3+ pays 1.9e-9 less per member on every per-head
        # line. The tolerance is 1e-8 there.
        tol = 1e-8 if lineage else 1e-9
        gate(f"every per-head line charges each generation the same per member ({tol:.0e} relative)", spread < tol,
             f"widest spread {spread:.1e}")
    gaps["per-head lines' spread (relative)"] = spread

    # Production: cell parts AS_s solved from the three generations' terms and their cell labor shares. The case keeps
    # the term at its published value and the generation lane attributes it on the published weights, so the parts are
    # solved there on both arms; each part is then spread over its cell's workers at the arm's weights. The
    # September 29 case puts the grid on the row-4 weights and the generation lane attributes it there (v4_inputs.py),
    # so its parts are solved on the row-4 labor shares.
    print("[production cells]", flush=True)
    prod_parts = {}
    w_labor = w_id if v4 else w_pub
    for end in ENDS:
        dims = lines["union"][end]["production"]["dims"]
        cut = 39 if dims["split"] == "hs_or_less" else 42
        earn = np.maximum(d[dims["proxy"]].to_numpy(float), 0)
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        labor = np.array([[float((earn * w_labor)[gens[g] & c].sum()) for c in cells] for g in GENS])
        A = labor / labor.sum(axis=0)
        y = np.array([lines["generations"][g][end]["production"]["cost_bn"] for g in GENS])
        y_all = y.copy()
        if lineage:     # the lineage's production term is set apart: the identified union's terms are September 29's
            y[GENS.index("G3plus")] -= lineage["production_bn"][end]
        AS, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = float(np.abs(A @ AS - y).max())
        gate(f"production {end}: cell parts reproduce the three generations' terms", resid < 1e-6,
             f"AS = {AS.round(4).tolist()} bn, max residual {resid:.1e}")
        part = A * AS  # generation x cell, $bn
        if lineage:
            # [ASSUMPTION] the added people's production term splits over G3+'s two cells as G3+'s own parts do.
            j3 = GENS.index("G3plus")
            part[j3] += lineage["production_bn"][end] * part[j3] / part[j3].sum()
            gap = float(np.abs(part.sum(axis=1) - y_all).max())
            gate(f"production {end}: with the lineage's term on G3+ the cell parts add to the generations' terms (1e-9 bn)",
                 gap < 1e-9, f"lineage {lineage['production_bn'][end]:.6f} bn; max |diff| {gap:.1e}")
        prod_parts[end] = dict(earn=earn, cells=cells, part=part)

    # Pieces: (generation, category, amount_bn, vector restricted to the generation).
    print("[pieces]", flush=True)
    pieces, residual, scaling = {e: [] for e in ENDS}, {e: {} for e in ENDS}, []
    moves = []   # oct07: each part split by another line, its cost by category on its own line's split and on the basis line's
    for end in ENDS:
        for g in GENS:
            G = lines["generations"][g][end]
            a = G["allocation"]
            m = gens[g]
            amount = {}

            def add(cat, bn, x, pid):
                x = np.where(m, x, 0.0)
                piece = dict(g=g, cat=cat, bn=bn, x=x, id=pid)
                if alt is not None and cat == PENSION:
                    # The pension pieces: Social Security (the social_security line) and Part A (part of medicare).
                    part = {"social_security": "oasdi", "medicare": "part_a"}[pid]
                    piece["alt"] = {k: np.where(m, alt[k][part][a], 0.0) for k in PENSION_VECTORS}
                    piece["part"] = part
                if pid in payroll:
                    key = row_of("receipt", pid)["key"]
                    if cat != "taxes" or key not in onbooks_key:
                        raise SystemExit(f"[BLOCKED] payroll line {pid}: category {cat}, key {key}")
                    piece["alt_tax"] = np.where(m, onbooks_key[key][a], 0.0)
                pieces[end].append(piece)

            def line_parts(row):
                """[(category, vector)] whose sum is the line's key vector."""
                k, i = row["key"], row["id"]
                if row["side"] == "receipt":
                    return [("enterprise" if i == "enterprise_surplus" else "taxes", vec[a][("receipt", k)])]
                if i == "education_services":
                    return [("schools", vec[a][("spending", "school_part")]),
                            ("education_other", vec[a][("spending", "P_part")])]
                if i == "school_reprice":
                    return [("schools", vec[a][("spending", "school_part")])]
                if i == "college_rekey":
                    return [("education_other", vec[a][("spending", "P_part")])]
                return [(spending_category(row), vec[a][("spending", k)])]

            def row_of(side, i):
                return next(r for r in G["rows"] if r["side"] == side and r["id"] == i)

            def receipts_of(parts):
                """Persons' amounts of receipt lines within the generation: each (line, weight)'s generation amount
                spread on its key vector."""
                x = np.zeros(len(d))
                for lid, wt in parts:
                    r = row_of("receipt", lid)
                    v = np.where(m, vec[a][("receipt", r["key"])], 0.0)
                    x += wt * r["amount_bn"] * v / float(v @ w0)
                return x

            def v4_split(row):
                """[(category, share of the line, vector)] for a line the September 29 case adds or changes, else None."""
                i, side = row["id"], row["side"]
                if side == "spending" and i in STATE_PRICE_PARENT:
                    return line_split(row_of("spending", STATE_PRICE_PARENT[i]))
                if side == "spending" and i in G["roads"]:
                    rp = G["roads"][i]
                    got = rp["driver_miles_bn"] + rp["freight_bn"] + rp["old_key_bn"]
                    if abs(got - row["amount_bn"]) > 1e-9:
                        raise SystemExit(f"[BLOCKED] {g} {end} {i}: its pieces do not add to its amount")
                    return [("roads_parks", rp["driver_miles_bn"] / row["amount_bn"], (age >= 5).astype(float)),
                            ("roads_parks", rp["freight_bn"] / row["amount_bn"], vec[a][("receipt", rp["freight_key"])]),
                            ("roads_parks", rp["old_key_bn"] / row["amount_bn"], vec[a][("spending", rp["old_key"])])]
                pen = G["pension"]
                if side == "spending" and i == "social_security":
                    return [(PENSION, 1.0, receipts_of([(x, 1.0) for x in PA["oasdi_lines"]]
                                                       + [(PA["se_line"], PA["se_oasdi_share"])]))]
                if side == "spending" and i == "medicare":
                    if abs(pen["medicare_benefits_bn"] + pen["part_a_accrual_bn"] - row["amount_bn"]) > 1e-9:
                        raise SystemExit(f"[BLOCKED] {g} {end} medicare: benefits and the Part A accrual do not add to it")
                    hi = receipts_of([(x, 1.0) for x in PA["hi_lines"]] + [(PA["se_line"], 1 - PA["se_oasdi_share"])])
                    return [("health", pen["medicare_benefits_bn"] / row["amount_bn"], vec[a][("spending", row["key"])]),
                            (PENSION, pen["part_a_accrual_bn"] / row["amount_bn"], hi)]
                if side == "receipt" and i == "federal_income_tax":
                    if abs(pen["fit_cash_bn"] - pen["benefit_tax_bn"] - row["amount_bn"]) > 1e-9:
                        raise SystemExit(f"[BLOCKED] {g} {end} federal_income_tax: the cash set's less the tax on benefits is not it")
                    return [("taxes", pen["fit_cash_bn"] / row["amount_bn"], vec[a][("receipt", row["key"])]),
                            ("taxes", -pen["benefit_tax_bn"] / row["amount_bn"], vec[a][("spending", "social_security")])]
                if side == "receipt" and i == "housing_enterprise_surplus":
                    return [("transfers", 1.0, vec[a][("receipt", row["key"])])]
                return None

            def line_split(row):
                """[(category, share of the line, vector)] for one line of this generation."""
                i = row["id"]
                if i == "public_order_safety":
                    j = GENS.index(g)
                    ph = use_parts["per_head"][j] * per_head_factor[j]
                    rest = use_parts["custody"][j] + use_parts["arrest_like_custody"][j] + use_parts["ice_interior"][j]
                    f = ph / (ph + rest)
                    return [("justice_per_head", f, np.ones(len(d))),
                            ("justice_use", 1 - f, ((age >= 18) & (age <= 64)).astype(float))]
                if row["key"].startswith("uninsured_use"):
                    line = next(x for x in models[g]["spending"]["lines"] if x["id"] == i)
                    med = line["keys"]["medicaid"][a]["target_bn"] / line["keys"][row["key"]][a]["target_bn"]
                    return [("health", med, vec[a][("spending", "medicaid")]), ("health", 1 - med, exposure_py)]
                if v4:
                    split = v4_split(row)
                    if split is not None:
                        return split
                parts = line_parts(row)
                # One coefficient per line: split the line by the parts' shares of its key total.
                total = sum(float(np.where(m, x, 0) @ w0) for _, x in parts)
                return [(cat, float(np.where(m, x, 0) @ w0) / total if total else 0.0, x) for cat, x in parts]

            def routed_split(row):
                """line_split(row), with the items' parts on the row whose split basis is another line (meta.routes)
                spread as that line: each part's share of the row's amount is its share of the row's cost."""
                rs = routes.get((row["side"], row["id"]))
                if not rs:
                    return line_split(row)
                moved = [(r, r["bn"][g][a] / row["amount_bn"]) for r in rs]
                split = [(cat, (1.0 - sum(s for _, s in moved)) * share, x) for cat, share, x in line_split(row)]
                for r, s in moved:
                    split += [(cat, s * share, x) for cat, share, x in line_split(row_of("spending", r["basis"]))]
                return split

            for (side, lid), rs in routes.items():
                row = row_of(side, lid)
                for r in rs:
                    cost = r["bn"][g][a] * row["response"]
                    print(f"  {g} {end}: {r['part']} {r['bn'][g][a]:+.6f} bn of {lid} ({cost:+.6f} bn at its response) "
                          f"spread as {r['basis']}", flush=True)
                    own, basis = {}, {}
                    for into, split in ((own, line_split(row)), (basis, line_split(row_of("spending", r["basis"])))):
                        for cat, share, _ in split:
                            into[cat] = into.get(cat, 0.0) + cost * share
                    moves += [dict(end=end, generation=g, part=r["part"], line=lid, basis=r["basis"], amount_bn=r["bn"][g][a],
                                   cost_bn=cost, category=cat, own_line_bn=own.get(cat, 0.0), basis_line_bn=basis.get(cat, 0.0))
                              for cat in sorted(set(own) | set(basis))]
            for row in G["rows"]:
                i, bn = row["id"], row["cost_bn"]
                amount[i] = row["amount_bn"]
                if bn == 0:
                    continue
                if i == "lane_constants":
                    residual[end][g] = residual[end].get(g, 0.0) + bn
                    continue
                for cat, share, x in routed_split(row):
                    add(cat, bn * share, x, i)
                # Scaling diagnostic: corrected amount over the uncorrected generation cell.
                ml = models[g]["receipts" if row["side"] == "receipt" else "spending"]["lines"]
                line0 = next((x for x in ml if x["id"] == i), None)
                if line0 is not None:
                    cell0 = (line0["cells"][row["scenario"]][a] if row["side"] == "receipt"
                             else line0["keys"][row["key"]][a])["target_bn"]
                    scaling.append(dict(end=end, generation=g, side=row["side"], line=i, key=row["key"], allocation=a,
                                        uncorrected_bn=cell0, corrected_bn=row["amount_bn"],
                                        ratio=(row["amount_bn"] / cell0 if cell0 else float("nan"))))
            for c in G["capital"]:
                rule = c["rule"]
                if rule["kind"] == "receipt_amount_over_national":
                    if rule["line"] in carriers:
                        # An item's offset, keyed by its carrier: spread as the parent line its item names (split_basis).
                        for _, share, x in routed_split(row_of("spending", carriers[rule["line"]]["parent_line"])):
                            add("capital", c["cost_bn"] * share, x, c["id"])
                        continue
                    if rule["line"] != "enterprise_surplus":
                        raise SystemExit(f"[BLOCKED] {c['id']}: a receipt key other than the per-head enterprise surplus")
                    add("capital", c["cost_bn"], np.ones(len(d)), c["id"])
                    continue
                if rule["kind"] == "part_rekeyed":
                    # The parent line's share and the road line's share of the key (the export's split of keyOf).
                    sh = c["shares"]
                    for lid, s_ in ((rule["parent_line"], sh["parent"]), (rule["correction_line"], sh["part"])):
                        for _, share, x in routed_split(row_of("spending", lid)):
                            add("capital", c["cost_bn"] * s_ / (sh["parent"] + sh["part"]) * share, x, c["id"])
                    continue
                nums = rule["numerator_lines"]
                den = sum(amount[n] for n in nums)
                for n in nums:
                    row = next(r for r in G["rows"] if r["id"] == n)
                    for _, share, x in routed_split(row):
                        add("capital", c["cost_bn"] * amount[n] / den * share, x, c["id"])
            pp = prod_parts[end]
            for s, cell in enumerate(pp["cells"]):
                add("production", pp["part"][GENS.index(g), s], pp["earn"] * cell, "production")
            # Gate: the generation's pieces plus its residual equal its cost.
            got = sum(p["bn"] for p in pieces[end] if p["g"] == g) + residual[end].get(g, 0.0)
            gaps["generation pieces vs cost (bn)"] = max(gaps.get("generation pieces vs cost (bn)", 0.0),
                                                         abs(got - G["cost_bn"]))
            gate(f"{g} {end}: pieces plus residual equal the generation's cost", abs(got - G["cost_bn"]) < 1e-6,
                 f"{got:.6f} vs {G['cost_bn']:.6f}")

    # Person amounts per replicate, by category: coefficient = bn * 1e9 / (x . w_r) within the generation.
    print("[person amounts]", flush=True)
    rows_u = np.flatnonzero(union)
    Wu = W[rows_u]
    cats = b_cats + A_ONLY
    amt = {e: {c: np.zeros((len(rows_u), W.shape[1])) for c in cats} for e in ENDS}
    unassigned = {e: np.zeros(W.shape[1]) for e in ENDS}
    for end in ENDS:
        for p in pieces[end]:
            x = p["x"][rows_u]
            k = x @ Wu  # 161
            if not np.any(x) or np.any(k == 0):
                unassigned[end] += p["bn"]
                if p["bn"] != 0:
                    print(f"  · unassignable piece {p['g']} {p['id']} {p['bn']:.6f} bn")
                continue
            amt[end][p["cat"]] += np.outer(x, p["bn"] * 1e9 / k)
    for end in ENDS:
        tot = sum((amt[end][c] * Wu).sum(axis=0) for c in cats) / 1e9
        res = sum(residual[end].values()) + unassigned[end][0]
        case = lines["union"][end]["cost_bn"]
        gap_case, gap_reps = abs(tot[0] + res - case), float(np.abs(tot - tot[0]).max())
        gaps["households + residual vs the case (bn)"] = max(gaps.get("households + residual vs the case (bn)", 0.0), gap_case)
        gaps["replicates vs full sample (bn)"] = max(gaps.get("replicates vs full sample (bn)", 0.0), gap_reps)
        gate(f"{end}: persons' assigned amounts plus the residual reproduce the case (full sample)",
             gap_case < 1e-6, f"{tot[0]:.6f} + {res:.6f} = {tot[0] + res:.6f} vs {case:.6f}, gap {gap_case:.1e}")
        gate(f"{end}: every replicate's assigned total equals the full sample's (line totals held)",
             gap_reps < 1e-6, f"max |diff| {gap_reps:.1e} bn")
        # Sensitivity: the same school dollars spread per head over the union instead of charged to the pupils.
        school_total = (amt[end]["schools"] * Wu).sum(axis=0)
        amt[end]["schools_per_head"] = np.tile(school_total / Wu.sum(axis=0), (len(rows_u), 1))

    # --accrual person: the pension pieces again under each arm; every other category is the flat arm's.
    arms = {"flat": amt}
    if alt is not None:
        print("[person accrual arms]", flush=True)
        for end in ENDS:
            oasdi = sum(r["amount_bn"] * (1.0 if r["id"] in PA["oasdi_lines"] else PA["se_oasdi_share"])
                        for g in GENS for r in lines["generations"][g][end]["rows"]
                        if r["side"] == "receipt" and (r["id"] in PA["oasdi_lines"] or r["id"] == PA["se_line"]))
            part_bn = {k: sum(p["bn"] for p in pieces[end] if p.get("part") == k) for k in ("oasdi", "part_a")}
            # oct05: the lineage's own accrual and Part A sit beside the September 29 union's (export_lines.cjs gates them).
            own = lineage["pension_bn"][end] if lineage else dict(oasdi_receipts_bn=0.0, accrual=0.0, part_a=0.0)
            want = PA["ratio_net"] * (oasdi - own["oasdi_receipts_bn"]) + own["accrual"]
            gap = abs(part_bn["oasdi"] - want) / want
            gate(f"{end}: the union's Social Security accrual is ratio_net x its OASDI receipts in the account (1e-9 relative)"
                 + (", plus the lineage's own on its receipts" if lineage else ""),
                 gap < 1e-9, f"{part_bn['oasdi']:.6f} = {PA['ratio_net']:.6f} x {oasdi - own['oasdi_receipts_bn']:.6f}"
                 + (f" + {own['accrual']:.6f}" if lineage else "") + " bn")
            gate(f"{end}: the union's Part A accrual is the payload's part_a_accrual_bn (1e-9 bn)" + (", plus the lineage's" if lineage else ""),
                 abs(part_bn["part_a"] - PA["part_a_accrual_bn"] - own["part_a"]) < 1e-9, f"{part_bn['part_a']:.9f} bn")
        pen_by = {}
        for k_vec in PENSION_VECTORS:
            pen = {e: np.zeros((len(rows_u), W.shape[1])) for e in ENDS}
            worst = 0.0
            for end in ENDS:
                for p in pieces[end]:
                    if "alt" not in p:
                        continue
                    x = p["alt"][k_vec][rows_u]
                    k = x @ Wu
                    if not np.any(x) or np.any(k <= 0):
                        raise SystemExit(f"[BLOCKED] {k_vec}: {p['g']} {end} {p['id']}: no member carries the piece")
                    part = np.outer(x, p["bn"] * 1e9 / k)
                    worst = max(worst, float(np.abs((part * Wu).sum(axis=0) / 1e9 - p["bn"]).max()))
                    pen[end] += part
            gate(f"{k_vec}: every pension piece keeps its generation's accrual in every replicate (1e-9 bn)",
                 worst < 1e-9, f"max |diff| {worst:.1e}")
            pen_by[k_vec] = pen
            if k_vec in PERSON_ARMS:
                arms[k_vec] = {e: {**amt[e], PENSION: pen[e]} for e in ENDS}
        # ONBOOKS_ARMS: each payroll piece moved from its key to its on-books key, beside their pension vectors.
        taxes = {e: amt[e]["taxes"].copy() for e in ENDS}
        worst = 0.0
        for end in ENDS:
            for p in pieces[end]:
                if "alt_tax" not in p:
                    continue
                x0, x1 = p["x"][rows_u], p["alt_tax"][rows_u]
                k0, k1 = x0 @ Wu, x1 @ Wu
                if not (np.any(x0) and np.all(k0 != 0) and np.any(x1) and np.all(k1 > 0)):
                    raise SystemExit(f"[BLOCKED] on-books payroll: {p['g']} {end} {p['id']} cannot be re-keyed")
                moved = np.outer(x1, p["bn"] * 1e9 / k1)
                worst = max(worst, float(np.abs((moved * Wu).sum(axis=0) / 1e9 - p["bn"]).max()))
                taxes[end] += moved - np.outer(x0, p["bn"] * 1e9 / k0)
        gate("on-books payroll: every payroll piece keeps its generation's total in every replicate (1e-9 bn)",
             worst < 1e-9, f"max |diff| {worst:.1e}")
        own = lab[rows_u]
        for k_arm, k_vec in ONBOOKS_ARMS.items():
            arms[k_arm] = {e: {**amt[e], PENSION: pen_by[k_vec][e], "taxes": taxes[e]} for e in ENDS}
            worst = 0.0
            for end in ENDS:
                for gi in range(len(GENS)):
                    m = own == gi
                    for c in ("taxes", PENSION):
                        got = (arms[k_arm][end][c][m] * Wu[m]).sum(axis=0)
                        want = (amt[end][c][m] * Wu[m]).sum(axis=0)
                        worst = max(worst, float(np.abs(got - want).max()) / 1e9)
            gate(f"{k_arm}: each generation keeps its taxes and its pension accrual in every replicate (1e-9 bn)",
                 worst < 1e-9, f"max |diff| {worst:.1e} bn")
        for k_arm in ARM_ORDER[1:]:
            for end in ENDS:
                tot = sum((arms[k_arm][end][c] * Wu).sum(axis=0) for c in cats) / 1e9
                res = sum(residual[end].values()) + unassigned[end][0]
                gap_case = float(np.abs(tot + res - lines["union"][end]["cost_bn"]).max())
                gate(f"{k_arm} {end}: convention A reproduces the case in every replicate (1e-9 bn)", gap_case < 1e-9,
                     f"max |gap| {gap_case:.1e}")

    print("[households]", flush=True)
    du = d.iloc[rows_u].reset_index(drop=True)
    hh_code, hh_ids = pd.factorize(du.PH_SEQ, sort=True)
    H = len(hh_ids)
    members = np.bincount(hh_code).astype(float)
    Wh = np.stack([np.bincount(hh_code, weights=Wu[:, r]) for r in range(Wu.shape[1])], axis=1) / members[:, None]
    ref = d.A_EXPRRP.isin([1, 2]).to_numpy()
    nref = pd.Series(ref.astype(int)).groupby(d.PH_SEQ.to_numpy()).sum()
    gate("one reference person per household (A_EXPRRP 1, 2)", bool((nref == 1).all()), f"{int((nref != 1).sum())} exceptions")
    # Head: the reference person when a union member, else the oldest union adult, else the oldest union member.
    ua = du.assign(row=rows_u, code=hh_code, ref=ref[rows_u], adult=du.A_AGE.ge(18))
    ua = ua.sort_values(["code", "ref", "adult", "A_AGE", "PPPOS"], ascending=[True, False, False, False, True])
    head_rows = ua.drop_duplicates("code").sort_values("code").row.to_numpy()
    refrow = pd.Series(np.flatnonzero(ref), index=d.PH_SEQ.to_numpy()[ref])
    ref_rows = refrow.reindex(hh_ids).to_numpy()
    ref_in_union = union[ref_rows]
    # A household whose union members are all minors takes its head's attributes from the reference person, who is
    # then outside the union (generation and status "outside_union").
    minor_only = age[head_rows] < 18
    head_rows = np.where(minor_only, ref_rows, head_rows)
    head_is_ref = ref[head_rows]
    head_lab = lab[head_rows]

    s_status = {}
    dd = d.assign(state=d.GESTFIPS)
    hh = d[["H_SEQ", "HPUBLIC", "HLORENT"]].drop_duplicates("H_SEQ")
    mex = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.isin([4, 5]).to_numpy()
    for name, use_med in (("borjas_paper_rules", True), ("no_medicaid_rule", False)):
        s = impute(dd, hh, use_medicaid_rule=use_med)
        un = np.asarray(s["unauthorized"], bool)
        sel = mex & un & (age >= 25) & (age <= 64)
        got = w_pub[sel].sum() / 1e6
        gate(f"status ({name}) reproduces the published Mexico-born 25-64 count", abs(got - PUBLISHED_MEX_25_64[name]) < 1e-9,
             f"{got:.6f}M" + ("" if arm == "published" else f"; {w0[sel].sum() / 1e6:.6f}M on the {arm} weights"))
        s_status[name] = un

    hga = d.A_HGA.to_numpy()[head_rows]
    edu_lab = np.select([hga <= 38, hga == 39, hga <= 42], ["below_high_school", "high_school", "some_college"],
                        "bachelor_plus")
    hage = age[head_rows]
    age_lab = np.select([hage < 30, hage < 45, hage < 65], ["under_30", "30_44", "45_64"], "65_plus")
    st = d.GESTFIPS.to_numpy()[head_rows]
    state_lab = np.select([st == 6, st == 48], ["CA", "TX"], "other")
    gen_lab = np.where(head_lab >= 0, np.array(GENS)[np.maximum(head_lab, 0)], "outside_union")
    kids = np.bincount(hh_code, weights=(du.A_AGE.lt(18)).to_numpy(float))
    kid_lab = np.select([kids == 0, kids <= 2], ["none", "1_2"], "3_plus")
    status_lab = {}
    for name, un in s_status.items():
        lab_s = np.where(head_lab == 0, np.where(un[head_rows], "unauthorized", "legal_immigrant"),
                         np.where(head_lab > 0, "us_born", "outside_union"))
        status_lab[name] = lab_s
    head_breaks = {"all": np.full(H, "all"), "head_education": edu_lab, "head_generation": gen_lab, "head_age": age_lab,
                   "state_group": state_lab, "children_in_household": kid_lab,
                   "head_status_borjas_rules": status_lab["borjas_paper_rules"],
                   "head_status_no_medicaid_rule": status_lab["no_medicaid_rule"]}
    own_gen = np.array(GENS)[lab[rows_u]]

    conv_cats = {"A": cats, "B": b_cats, "A_schools_per_head": [c for c in cats if c != "schools"] + ["schools_per_head"]}

    def household_stats(amt, breaks):
        """One arm's statistics from its person amounts: the rows of the files and, for the arms' comparison, the
        replicate vectors of each cell's net-positive share and pension accrual per member."""
        reps = {"share": {}, "pension": {}}
        mean_rows = []
        for end in ENDS:
            for name, labels in list(breaks.items()) + [("own_generation", None)]:
                lab_p = own_gen if labels is None else labels[hh_code]
                for cell in sorted(set(lab_p)):
                    sel = lab_p == cell
                    wsel = Wu[sel]
                    for c in cats + ["schools_per_head"]:
                        mean = (amt[end][c][sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                        mean_rows.append(dict(end=end, breakdown=name, cell=cell, category=c, in_B=c in b_cats,
                                              net_cost_per_member_usd=mean[0], se=sdr(mean)))
                        if c == PENSION:
                            reps["pension"][(end, name, cell)] = mean
        npos_rows, conc_rows, q_rows, ctrl_rows = [], [], [], []
        hh_out = pd.DataFrame({"PH_SEQ": hh_ids, "union_members": members, "weight": Wh[:, 0], **{k: v for k, v in breaks.items() if k != "all"},
                               "head_is_reference_person": head_is_ref, "reference_person_in_union": ref_in_union})
        for conv, cs in conv_cats.items():
            for end in ENDS:
                person = sum(amt[end][c] for c in cs)  # n_u x 161, $ per person
                hcost = np.stack([np.bincount(hh_code, weights=person[:, r], minlength=H) for r in range(person.shape[1])], axis=1)
                hweighted = np.stack([np.bincount(hh_code, weights=person[:, r] * Wu[:, r], minlength=H) for r in range(person.shape[1])], axis=1)
                per_member = hcost / members[:, None]
                hh_out[f"{conv}_{end}_household_cost_usd"] = hcost[:, 0]
                hh_out[f"{conv}_{end}_per_member_usd"] = per_member[:, 0]
                for c in cs:
                    hh_out[f"{conv}_{end}_{c}_usd"] = np.bincount(hh_code, weights=amt[end][c][:, 0], minlength=H)
                npos_p = hcost[hh_code] < 0  # members in net-contributor households, per replicate
                total = hweighted.sum(axis=0) / 1e9
                # Net-positive shares by breakdown (members weighted by their person weights).
                for name, labels in list(breaks.items()) + [("own_generation", None)]:
                    lab_p = own_gen if labels is None else labels[hh_code]
                    for cell in sorted(set(lab_p)):
                        sel = lab_p == cell
                        wsel = Wu[sel]
                        share = (npos_p[sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                        mean_pm = (person[sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                        hsel = np.zeros(H, bool)
                        hsel[np.unique(hh_code[sel])] = True
                        hshare = ((hcost[hsel] < 0) * Wh[hsel]).sum(axis=0) / Wh[hsel].sum(axis=0)
                        cell_bn = (person[sel] * wsel).sum(axis=0) / 1e9
                        npos_rows.append(dict(convention=conv, end=end, breakdown=name, cell=cell, records=int(sel.sum()),
                                              households=int(hsel.sum()), members_m=wsel[:, 0].sum() / 1e6,
                                              share_members_net_positive=share[0], se=sdr(share),
                                              share_households_net_positive=hshare[0], se_households=sdr(hshare),
                                              net_cost_per_member_usd=mean_pm[0], se_per_member=sdr(mean_pm),
                                              cell_net_cost_bn=cell_bn[0], se_cell_bn=sdr(cell_bn),
                                              small_cell=bool(sel.sum() < 200)))
                        reps["share"][(conv, end, name, cell)] = share
                # Concentration: households ranked by household net cost, counted by household weight.
                stats = {k: np.zeros(W.shape[1]) for k in ("top10_share_of_total", "top20_share_of_total",
                                                            "top10_members_share", "top20_members_share",
                                                            "net_cost_households_bn", "net_contributor_households_bn",
                                                            "share_households_net_positive")}
                for r in range(W.shape[1]):
                    order = np.argsort(-hcost[:, r], kind="stable")
                    cw = np.cumsum(Wh[order, r]) / Wh[:, r].sum()
                    contrib = hweighted[order, r]
                    mem = (members * Wh[:, r])[order]
                    for p, key in ((0.1, "10"), (0.2, "20")):
                        full = cw <= p
                        j = int(full.sum())
                        prev = cw[j - 1] if j else 0.0
                        frac = (p - prev) / (cw[j] - prev) if j < H else 0.0
                        stats[f"top{key}_share_of_total"][r] = (contrib[full].sum() + frac * contrib[j]) / contrib.sum()
                        stats[f"top{key}_members_share"][r] = (mem[full].sum() + frac * mem[j]) / mem.sum()
                    stats["net_cost_households_bn"][r] = hweighted[hcost[:, r] > 0, r].sum() / 1e9
                    stats["net_contributor_households_bn"][r] = hweighted[hcost[:, r] < 0, r].sum() / 1e9
                    stats["share_households_net_positive"][r] = Wh[hcost[:, r] < 0, r].sum() / Wh[:, r].sum()
                stats["total_bn"] = total
                for k, v in stats.items():
                    conc_rows.append(dict(convention=conv, end=end, statistic=k, value=v[0], se=sdr(v)))
                # Quantiles: per member (members weighted by person weights) and per household (household weights).
                for unit, vals, wts in (("per_member", per_member[hh_code], Wu), ("household", hcost, Wh)):
                    for q in (0.1, 0.25, 0.5, 0.75, 0.9):
                        qs = np.zeros(W.shape[1])
                        for r in range(W.shape[1]):
                            o = np.argsort(vals[:, r], kind="stable")
                            cwq = np.cumsum(wts[o, r]) / wts[:, r].sum()
                            qs[r] = vals[o, r][min(int(np.searchsorted(cwq, q)), len(o) - 1)]
                        q_rows.append(dict(convention=conv, end=end, unit=unit, quantile=q, net_cost_usd=qs[0], se=sdr(qs)))
                if conv == "A":
                    case = lines["union"][end]["cost_bn"]
                    for c in cs:
                        ctrl_rows.append(dict(end=end, item=c, bn=float((amt[end][c][:, 0] * Wu[:, 0]).sum() / 1e9),
                                              assigned=True))
                    for g in GENS:
                        ctrl_rows.append(dict(end=end, item=f"lane_constants_{g}", bn=residual[end].get(g, 0.0), assigned=False))
                    ctrl_rows.append(dict(end=end, item="unassignable_pieces", bn=float(unassigned[end][0]), assigned=False))
                    ctrl_rows.append(dict(end=end, item="households_sum", bn=float(total[0]), assigned=True))
                    ctrl_rows.append(dict(end=end, item="case", bn=case, assigned=None))
                    ctrl_rows.append(dict(end=end, item="households_sum_plus_residual_minus_case",
                                          bn=float(total[0]) + sum(residual[end].values()) + float(unassigned[end][0]) - case,
                                          assigned=None))
        return dict(npos=npos_rows, conc=conc_rows, q=q_rows, ctrl=ctrl_rows, means=mean_rows, hh=hh_out, reps=reps)

    breaks = dict(head_breaks)
    if alt is not None:
        # The case's own status flag (state-aware, the one its on-books share and the accrual's claim share read).
        breaks[CASE_FLAG] = np.where(head_lab == 0, np.where(unauth_case[head_rows], "unauthorized", "legal_immigrant"),
                                     np.where(head_lab > 0, "us_born", "outside_union"))
    results = {name: household_stats(a_, breaks) for name, a_ in arms.items()}

    print(f"  households: {H:,} with {len(rows_u):,} union person records; reference person outside the union: "
          f"{int((~ref_in_union).sum())} households; union members all minors (head = reference person): {int(minor_only.sum())}")
    gate("every head is an adult", bool((age[head_rows] >= 15).all()), f"youngest head {int(age[head_rows].min())}")
    print(f"  worst gaps ({arm}): " + "; ".join(f"{k} {v:.1e}" for k, v in gaps.items()), flush=True)

    def frame_of(rows):
        df = pd.DataFrame(rows)
        for c in df.columns:
            if df[c].dtype == float:
                df[c] = df[c].round(6)
        return df

    def write(name, rows):
        frame_of(rows).to_csv(out_dir / name, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)

    def same_as_written(label, named_rows):
        differ = []
        for name, rows in named_rows.items():
            text = frame_of(rows).to_csv(index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL).encode()
            if not (out_dir / name).exists() or (out_dir / name).read_bytes() != text:
                differ.append(name)
        gate(f"{label} {len(named_rows)} file(s) in {out_dir.relative_to(HERE)}/ byte for byte", not differ,
             ", ".join(differ) or "identical")

    def five(res, suffix):
        return {name.replace(".csv", f"{suffix}.csv"): rows
                for name, rows in zip(FLAT_FILES[:5], [res["npos"], res["conc"], res["q"], res["ctrl"], res["means"]])}

    flat = results["flat"]
    files = dict(zip(FLAT_FILES, [flat["npos"], flat["conc"], flat["q"], flat["ctrl"], flat["means"], scaling]))
    if moves:
        files["split_basis_moves.csv"] = moves
    if alt is not None:
        # The flat arm without the case-flag rows is the flat run's output, byte for byte.
        same_as_written("the flat arm reproduces the flat run's",
                        {name: [r for r in rows if r.get("breakdown") != CASE_FLAG] for name, rows in files.items()})
        # Every arm's net-positive shares against the flat arm's, conventions A and B; the difference's standard
        # error from the same replicates.
        base = flat["reps"]
        info = {(r["convention"], r["end"], r["breakdown"], r["cell"]): r for r in flat["npos"]}
        arm_rows = []
        for name in ARM_ORDER:
            reps = results[name]["reps"]
            for (conv, end, bname, cell), share in reps["share"].items():
                if conv not in ("A", "B"):
                    continue
                diff = share - base["share"][(conv, end, bname, cell)]
                pen = reps["pension"][(end, bname, cell)]
                r0 = info[(conv, end, bname, cell)]
                arm_rows.append(dict(arm=name, convention=conv, end=end, breakdown=bname, cell=cell, records=r0["records"],
                                     members_m=r0["members_m"], share_members_net_positive=share[0], se=sdr(share),
                                     diff_vs_flat=diff[0], se_diff=sdr(diff), pension_accrual_per_member_usd=pen[0],
                                     se_pension_accrual=sdr(pen), small_cell=r0["small_cell"]))
        person_files = five(results["person"], PERSON_SUFFIX)
        if payroll_base == "onbooks":
            same_as_written("the person arm reproduces the --accrual person run's", person_files)
            same_as_written("the arms comparison reproduces the --accrual person run's",
                            {"person_accrual_arms.csv": arm_rows})
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed, nothing written: {FAILS}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    if alt is None:
        for name, rows in files.items():
            write(name, rows)
        flat["hh"].to_parquet(cache_dir / "households.parquet", index=False)
        print(f"  ✓ all household gates passed; wrote {out_dir.relative_to(HERE)}/ and {cache_dir.relative_to(HERE)}/households.parquet")
        return

    if payroll_base not in ("all", "onbooks"):   # fail loud: an earlier draft shadowed it with the payroll line set
        raise SystemExit(f"[BLOCKED] payroll_base is {payroll_base!r}, not 'all' or 'onbooks'")
    name, suffix = ("person", PERSON_SUFFIX) if payroll_base == "all" else (ONBOOKS_CENTRAL, ONBOOKS_SUFFIX)
    for fname, rows in five(results[name], suffix).items():
        write(fname, rows)
    if payroll_base == "all":
        write("person_accrual_arms.csv", arm_rows)
    results[name]["hh"].to_parquet(cache_dir / f"households{suffix}.parquet", index=False)
    print(f"  ✓ all household gates passed; wrote the {name} arm's files in {out_dir.relative_to(HERE)}/ "
          f"(*{suffix}.csv{', person_accrual_arms.csv' if payroll_base == 'all' else ''}) and "
          f"{cache_dir.relative_to(HERE)}/households{suffix}.parquet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An adopted main case spread over the union's households.")
    parser.add_argument("--weights", choices=["published", "row4"], default="published",
                        help="published: ASEC person weights (derived/); row4: audit row 4's weights (derived/row4/)")
    parser.add_argument("--case", choices=list(CASE_DIRS), default="sept27",
                        help="sept27 (default): the September 27 case; sept29: the main case adopted on 2026-09-29; oct05: on 2026-10-05; "
                             "oct07: main case v6; the later cases on the row-4 weights only, written to derived/<case>/")
    parser.add_argument("--accrual", choices=["flat", "person"], default="flat",
                        help="flat (default): the pension accrual by OASDI and HI receipts; person: by the pension "
                             "lane's person model (person_accrual.py), new *_person_accrual files beside the flat ones "
                             "(--case sept29, oct05 or oct07)")
    parser.add_argument("--payroll", choices=["all", "onbooks"], default="all",
                        help="all (default): the payroll taxes on all wages, as the account keys them; onbooks (with "
                             "--accrual person): on on-books wages, the lane's central, written to *_person_onbooks")
    parser.add_argument("--placement", choices=["band", "uniform"], default="band",
                        help="band (default): a case's added people by five-year band at its measured age mix (oct07); "
                             "uniform: beside it, v5's one factor on every G3+ record, flat arm only, written to "
                             "derived/oct07/uniform_placement/")
    args = parser.parse_args()
    main(args.weights, args.case, args.accrual, args.payroll, args.placement)

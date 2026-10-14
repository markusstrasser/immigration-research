"""Write the nine conclusions and premise matrix on live main case v8 only.

The oct07 CSVs supply the historical claims and qualitative questions, never live values.
C8 tests the map's still-oct07 sentence against explicitly labelled live comparator
readings at personal ends, preserving gaps in the local-white symmetric route.
Every input file and its numeric CSV cells is pinned in tables_oct15_pins.json, rederived
after CASE_FINAL; drift stops before writing. No script repins itself. Historical scripts
and outputs are preserved. Run after engine_breaks_sept29.cjs --case oct15 and all of
the generation, white, pairing, debt and winners lanes' oct15 runs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/tables_oct15.py
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
F = HERE.parent
D = HERE / "derived"
CASE = F / "main_case_2026_10_15/derived"
PINS = HERE / "tables_oct15_pins.json"
INPUTS = [
    *[D / f"{name}_oct15.csv" for name in (
        "c1_arms", "c1_min_cuts", "c2_tally", "c2_break_even", "c3_correction_split",
        "c6_generation_break_even", "c6_inputs")],
    D / "first_year_item6_oct15.json", D / "first_year_calibration.json", D / "c1_search_oct15.json",
    CASE / "summary.json", CASE / "main_case_bands.csv", CASE / "corrections.json", CASE / "corrections_cash.json",
    F / "white_replacement_2026_09_28/derived/headline_oct15.csv",
    F / "white_replacement_2026_09_28/derived/rekey_summary_oct15.csv",
    F / "white_replacement_2026_09_28/derived/ipeds_terms_oct15.csv",
    F / "white_replacement_2026_09_28/derived/symmetric_results_oct15.csv",
    F / "white_replacement_2026_09_28/derived/symmetric_audit_oct15.json",
    F / "white_replacement_2026_09_28/derived/lineage_engine_bridge_oct15.csv",
    F / "white_replacement_2026_09_28/mortality_conventions.py",
    F / "white_replacement_2026_09_28/comparison_contract.py",
    *[F / "lineage_mortality_2026_10_14/derived" / name for name in (
        "case_changes.csv", "comparisons.csv", "accrual_ratios.csv", "reproduced_ratios.csv", "added_profiles.csv")],
    F / "sept24_propagation_2026_09_24/derived/oct15/real_costs_totals.csv",
    F / "debt_legacy_2026_09_23/derived/oct15/federal_split_2024.csv",
    F / "debt_legacy_2026_09_23/derived/oct15/summary.json",
    F / "winners_losers_2026_09_24/derived/oct15/net_shares.csv",
    D / "conclusions_oct07.csv", D / "common_mode_oct07.csv",
    F / "white_replacement_2026_09_28/derived/headline_oct07.csv",
    F / "overview_2026_09_28/groups.py", F / "overview_2026_09_28/quantity_registry.csv",
    F / "overview_2026_09_28/quantities.py",
    F / "main_case_lineage_2026_10_05/derived/white_lines.json",
    F / "main_case_lineage_2026_10_05/derived/v5_summary.json",
]


def blocked(message):
    raise SystemExit(f"[BLOCKED] {message}")


def rows(file):
    with file.open(newline="") as stream:
        return list(csv.DictReader(stream))


def num(row, field):
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError):
        blocked(f"missing or non-numeric {field}: {row}")
    if not math.isfinite(value):
        blocked(f"non-finite {field}: {row}")
    return value


def check(label, got, want, tol):
    if not all(math.isfinite(value) for value in (got, want, tol)) or tol < 0:
        blocked(f"{label}: non-finite value or invalid tolerance")
    if abs(got - want) > tol:
        blocked(f"{label}: {got} != {want} (tolerance {tol})")


def snapshot():
    """Evidence pins: every input's bytes and every numeric CSV cell, with its row and column."""
    result = {}
    for file in INPUTS:
        if not file.exists():
            blocked(f"{file.relative_to(F)} absent: run its live oct15 producer first")
        cells = []
        if file.suffix == ".csv":
            for index, row in enumerate(rows(file)):
                for key, text in row.items():
                    try:
                        value = float(text)
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(value):
                        cells.append([index, key, value])
        result[str(file.relative_to(F))] = {"sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "numeric_cells": cells}
    return result


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def band(row):
    return [num(row, "cost_low_bn"), num(row, "cost_high_bn")]


def pair_text(values, digits=1):
    return " / ".join(f"{v:,.{digits}f}" for v in values)


MORTALITY = load_module("mortality_conventions_c8", F / "white_replacement_2026_09_28/mortality_conventions.py")
COMPARISON = load_module("comparison_contract_c8", F / "white_replacement_2026_09_28/comparison_contract.py")
MIXED_MORTALITY = MORTALITY.MIXED
OWN_MORTALITY = MORTALITY.OWN
MORTALITY_READINGS = ((MIXED_MORTALITY, "none"), (OWN_MORTALITY, "low"), (OWN_MORTALITY, "high"))
ROUGH_LINEAGE = "mexican_origin_rough"


def comparator_values(records, arm="combined_rules_only"):
    """No implicit whole-population/own-group pairing; row provenance is mandatory."""
    selected, declared = {}, {}
    for row in records:
        if row.get("arm") != arm:
            continue
        if row.get("case") != "oct15":
            blocked("C8 comparator case must be oct15")
        reading = row.get("mortality_convention"), row.get("mortality_bound")
        if reading not in MORTALITY_READINGS:
            blocked(f"C8 explicit mortality convention/bound required: {reading}")
        if row.get("allocation") != "personal":
            blocked("C8 comparator allocation must be personal")
        if row.get("group_mortality") not in ("whole-population", "own-group"):
            blocked("C8 actual group mortality declaration required")
        key = (*reading, row["basis"], row["group"], row["end"])
        if key in selected:
            blocked(f"C8 duplicate comparator row: {key}")
        selected[key] = num(row, "cost_bn")
        declared[key] = row
    for reading in MORTALITY_READINGS:
        for basis in ("accrual", "cash"):
            for group in ("mexican_origin_engine", ROUGH_LINEAGE, "A1_third_plus_nh_white", "A3_third_plus_nh_white_at_union_ages"):
                for end in ("low", "high"):
                    if (*reading, basis, group, end) not in selected:
                        blocked(f"C8 missing comparator row: {(*reading, basis, group, end)}")
            for group in ("A1_third_plus_nh_white", "A3_third_plus_nh_white_at_union_ages"):
                for end in ("low", "high"):
                    try:
                        lineage = declared[*reading, basis, ROUGH_LINEAGE, end]
                        comparator = declared[*reading, basis, group, end]
                        COMPARISON.require_same_engine(lineage, comparator)
                        if lineage.get("engine") != "rough" or comparator.get("engine") != "rough":
                            blocked("C8 gap requires both sides on engine rough")
                        for row in (lineage, comparator):
                            removal = num(row, "mixed_unit_removal_bn")
                            check("C8 item11 exclusion closes", num(row, "cost_without_item11_bn"),
                                  num(row, "cost_bn") - removal, 1e-9)
                            if not row.get("mixed_unit_asymmetry"):
                                blocked("C8 explicit mixed-unit asymmetry required")
                        if group == 'A1_third_plus_nh_white':
                            check('C8 measured comparator item11 declaration',
                                  num(comparator, 'mixed_unit_removal_bn'), num(comparator, 'comparator_item11_bn'), 1e-9)
                            if num(comparator, 'item11_paired_se_bn') < 0:
                                blocked('C8 paired item11 SE must be nonnegative')
                        elif num(comparator, 'mixed_unit_removal_bn') != 0:
                            blocked('C8 age-standardized comparator item11 remains unmeasured')
                        MORTALITY.validate_pair(lineage,
                                                declared[*reading, basis, group, end], reading[0])
                    except ValueError as error:
                        raise SystemExit(str(error)) from error
    return selected


def comparator_gap(values, mortality, bound, basis, group):
    return [values[mortality, bound, basis, ROUGH_LINEAGE, end]
            - values[mortality, bound, basis, group, end] for end in ("low", "high")]


def bridge_values(records, values):
    """Require the delivered itemization for every mortality reading."""
    parts = {}
    for row in records:
        if row.get("arm") != "combined_rules_only":
            continue
        reading = row.get("mortality_convention"), row.get("mortality_bound")
        if (row.get("case"), row.get("case_engine"), row.get("rough_engine")) != ("oct15", "case", "rough") or reading not in MORTALITY_READINGS:
            blocked("C8 bridge provenance must declare case-to-rough oct15 and a source mortality reading")
        key = (*reading, row["basis"], row["end"])
        identity = (*key, row["side"], row["line"])
        if identity in parts:
            blocked("C8 duplicate bridge component")
        value = num(row, "case_minus_rough_bn")
        check("C8 bridge component difference", value, num(row, "case_bn") - num(row, "rough_bn"), 1e-9)
        parts[identity] = value
    totals = {}
    for mortality, bound in MORTALITY_READINGS:
        for basis in ("accrual", "cash"):
            for end in ("low", "high"):
                key = mortality, bound, basis, end
                selected = [amount for identity, amount in parts.items() if identity[:4] == key]
                if not selected:
                    blocked(f"C8 missing itemized bridge {mortality}/{bound}/{basis}/{end}")
                total = sum(selected)
                check(f"C8 {mortality}/{bound}/{basis}/{end} itemized bridge closure",
                      total, values[mortality, bound, basis, "mexican_origin_engine", end]
                      - values[mortality, bound, basis, ROUGH_LINEAGE, end], 1e-9)
                totals[key] = total
    return totals


def live_pairing_values(records):
    """Section 7 is the current pairing; dated revision rows have no live oct15 amount."""
    return {(row["column"], row["item"]): num(row, "oct15") for row in records if row["section"] == "7"}


def debt_split_values(case, end, printed):
    """Use the debt producer's unrounded principal columns; gate its six-decimal CSV separately."""
    financing = case["financing_columns_2024"]["main_profile"][f"{end}|central"]
    headline = case["v4"]["headline_2024"][end]
    values = {"fiscal_gap_bn": num(financing, "cash_fiscal_gap_bn"),
              "federal_bn": num(financing, "cash_federal_bn"),
              **{key: num(financing, key) for key in ("resource_cost_bn", "resource_cost_federal_bn",
                                                     "displaced_bn", "displaced_federal_bn")},
              "accrual_bn": num(headline, "accrual_2024_bn"),
              "accrual_federal_bn": num(headline, "accrual_federal_2024_bn")}
    for key, value in values.items():
        check(f"C5 {end} printed {key}", num(printed, key), value, 5e-7 + 1e-12)
    return {**printed, **values}


def write(file, data):
    with file.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def main():
    current = snapshot()
    if not PINS.exists():
        blocked("tables_oct15_pins.json absent: derive pins from the final adopted run before tables")
    pinned = json.loads(PINS.read_text())
    if pinned["inputs"] != current:
        changed = [name for name in current if current[name] != pinned["inputs"].get(name)]
        blocked(f"final evidence drift: {changed}")
    summary = json.loads((CASE / "summary.json").read_text())["v8"]
    payload = json.loads((CASE / "corrections.json").read_text())
    if payload["meta"]["adopted"] != "2026-10-15" or payload["meta"]["allocation"]["group_total"] != "personal":
        blocked("the live payload is not adopted v8 at the personal allocation")
    ends = summary["end_specifications"]["set"][0]
    if any(ends != row for basis in ("set", "cash") for row in summary["end_specifications"][basis]):
        blocked("set and cash ends differ: the tally rule needs revision")
    end_labels = [f"low_end_{ends[0]}", f"high_end_{ends[1]}"]
    arms = {r["arm"]: r for r in rows(D / "c1_arms_oct15.csv")}
    bands = {r["variant"]: r for r in rows(CASE / "main_case_bands.csv") if r["profile"] == "long_run_non_school_full"}
    for variant, arm, key in [("adopted", "adopted", "band_bn"), ("cash_set", "pension_cash", "cash_set_bn")]:
        for i, value in enumerate(band(arms[arm])):
            check(f"{variant} published band", value, band(bands[variant])[i], 1e-4)
            check(f"{variant} summary", value, summary[key][i], 1e-4)
    midpoint = sum(band(arms["adopted"])) / 2
    horizon = json.loads((D / "first_year_item6_oct15.json").read_text())
    for basis, arm in (("set", "first_year_horizon"), ("cash", "first_year_horizon_cash")):
        for i, value in enumerate(horizon["variants"]["fixed_capital"][basis]):
            check(f"first-year {basis} engine report", band(arms[arm])[i], value, 1e-4)
    check("first-year lower threshold", horizon["thresholds"]["low_bn"], 0.75 * sum(summary["band_bn"]) / 2, 1e-9)
    horizon_breaks = sum(horizon["variants"]["fixed_capital"]["set"])/2 < horizon["thresholds"]["low_bn"]
    if horizon_breaks != horizon["first_year_breaks_alone"]:
        blocked("first-year C1 verdict disagrees with the unrounded engine report")
    horizon_clause = "First-year horizon " + ("breaks C1 alone" if horizon_breaks else "does not break C1 alone")
    cuts = [r for r in rows(D / "c1_min_cuts_oct15.csv") if r["minimal"] == "yes"]
    tally = {(r["model"], r["end"]): r for r in rows(D / "c2_tally_oct15.csv")}
    tally_of = lambda model: [num(tally[model, e], "tally_bn") for e in end_labels]
    be = rows(D / "c2_break_even_oct15.csv")
    split = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_oct15.csv")}
    for row in split.values():
        check("C3 side closure", num(row, "net_move_bn"), num(row, "tax_side_move_bn") + num(row, "spending_side_move_bn") + num(row, "interaction_bn"), 2e-4)
        check("C3 full case", num(row, "all_edits_bn"), band(arms["adopted"])[end_labels.index(row["end"])], 1e-4)
    gen = rows(D / "c6_generation_break_even_oct15.csv")
    for case, oracle in [("case_accrual", "adopted"), ("cash_set", "pension_cash")]:
        for conv in ("a", "b"):
            rr = [r for r in gen if r["case"] == case and r["convention"] == conv]
            if {r["generation"] for r in rr} != {"G1", "G2", "G3plus"}:
                blocked(f"C6 incomplete generations for {case} {conv}")
            for i, key in enumerate(("cost_low_end_bn", "cost_high_end_bn")):
                check(f"C6 {case} {conv} sum", sum(num(r, key) for r in rr), band(arms[oracle])[i], 2e-4)
    white = F / "white_replacement_2026_09_28/derived"
    comparator_records = rows(white / "symmetric_results_oct15.csv")
    comparator = comparator_values(comparator_records)
    bridges = bridge_values(rows(white / "lineage_engine_bridge_oct15.csv"), comparator)
    comparator_rows = {(r["mortality_convention"], r["mortality_bound"], r["basis"], r["group"], r["end"]): r
                       for r in comparator_records if r["arm"] == "combined_rules_only"}
    for basis, key in (("accrual", "band_bn"), ("cash", "cash_set_bn")):
        for i, end in enumerate(("low", "high")):
            check(f"C8 labelled mixed mortality headline {basis}/{end}",
                  comparator[MIXED_MORTALITY, "none", basis, "mexican_origin_engine", end], summary[key][i], 1e-9)
    head = {(r["figure"], r["end"]): r for r in rows(white / "headline_oct15.csv")}
    white_summary = {(r["basis"], r["group"], r["end"]): r for r in rows(white / "rekey_summary_oct15.csv")}
    for basis, key in (("accrual", "band_bn"), ("cash", "cash_set_bn")):
        for i, end in enumerate(("low", "high")):
            row = white_summary[basis, "mexican_origin_engine", end]
            check(f"C8 {basis} engine union on final adopted case {end}", num(row, "cost"), summary[key][i], 1e-4)
            check(f"C8 {basis} personal end {end}", num(row, "spec"), ends[i], 0)
    A1 = "age artefact removed: A1 third-plus whites, accrual (central)"
    LOCAL = "local whites state by state, union ages, accrual (central)"
    RAW = "raw cash at white ages: A1, cash set"
    def white_band(figure):
        return [num(head[figure, end], "oct15_bn") for end in ("low", "high")]
    sys.path.insert(0, str(F / "overview_2026_09_28"))
    MAP = load_module("groups", F / "overview_2026_09_28/groups.py")
    Q = load_module("quantities", F / "overview_2026_09_28/quantities.py")
    site = Q.groups_sites(MAP.GROUPS).get("selection/f263/text", "")
    if not all(f"{{{{q:{rid}|mid_range}}}}" in site for rid in ("whites.gap_a1", "whites.gap_local")):
        blocked("C8 map sentence no longer quotes the two historical white comparisons")
    if "{{q:whites.gap_cash|mid_range}}" not in Q.groups_sites(MAP.GROUPS).get("selection/f263/why", ""):
        blocked("C8 map why line no longer quotes its historical raw-cash comparator")
    historical = {(r["figure"], r["end"]): r for r in rows(white / "headline_oct07.csv")}
    references = {}
    for rid, fig in (("whites.gap_a1", A1), ("whites.gap_local", LOCAL), ("whites.gap_cash", RAW)):
        expected = tuple(num(historical[fig, e], "oct07_bn") for e in ("low", "high"))
        if Q.record_value(rid) != expected:
            blocked(f"C8 {rid}: map changed from the explicit historical oct07 baseline")
        references[fig] = sum(expected) / 2
    claim = Q.fill(site)[0]
    historical_claim = next(r["claim_tested"] for r in rows(D / "conclusions_oct07.csv") if r["id"] == "C8")
    if claim != historical_claim:
        blocked("C8 map's claim text changed from oct07: restate its frame before grading oct15")
    real = live_pairing_values(rows(F / "sept24_propagation_2026_09_24/derived/oct15/real_costs_totals.csv"))
    pairing = [real["pairing_on_priced_count", f"published pairing ({e})"] for e in ("low", "high")]
    footing = [real["hispanic", "fiscal main case (low)"], real["custody", "fiscal main case (high)"]]
    social = [p - f for p, f in zip(pairing, footing)]
    debt_dir = F / "debt_legacy_2026_09_23/derived/oct15"
    debt_case = json.loads((debt_dir / "summary.json").read_text())["case"]
    debt = debt_case["v4"]["headline_2024"]
    federal = {r["end"]: r for r in rows(debt_dir / "federal_split_2024.csv") if r["profile"] == "long_run_non_school_full" and r["convention"] == "central"}
    shares, cash_shares, share_alternatives = [], [], []
    for i, end in enumerate(("low", "high")):
        row = debt_split_values(debt_case, end, federal[end])
        total = sum(num(row, k) for k in ("fiscal_gap_bn", "resource_cost_bn", "displaced_bn", "accrual_bn"))
        fed = sum(num(row, k) for k in ("federal_bn", "resource_cost_federal_bn", "displaced_federal_bn", "accrual_federal_bn"))
        check(f"C5 debt set {end}", debt[end]["set_net_cost_bn"], summary["band_bn"][i], 1e-6)
        check(f"C5 split sum {end}", total, debt[end]["set_net_cost_bn"] + num(row, "production_P_bn"), 1e-6)
        shares.append(100 * (total - fed) / total)
        cash_shares.append(100 * (total - fed) / (total - num(row, "accrual_bn")))
        scheduled = band(arms["pension_scheduled"])[i] - band(arms["adopted"])[i]
        legacy = debt[end]["legacy_interest_2024_bn"]
        share_alternatives.append({
            "scheduled": 100 * (total - fed) / (total + scheduled),
            "defense_GDP": 100 * (total - fed) / (total + 60),
            "defense_GDP_and_legacy_interest": 100 * (total - fed) / (total + 60 + legacy),
            "defense_interest_scheduled": 100 * (total - fed) / (total + 60 + legacy + scheduled),
            "defense_interest_average_cost": 100 * (total - fed) / (total + 271),
        })
    winners = {(r["net"], r["stack"], r["unit"]): r for r in rows(F / "winners_losers_2026_09_24/derived/oct15/net_shares.csv")}
    wins = [100 * num(winners[f"net_social_{c}", "central", "spm_unit_pooled"], "winners_share") for c in ("a", "b")]
    conclusions = rows(D / "conclusions_oct07.csv")
    for row in conclusions:
        row["status_on_v8"] = row.pop("status_on_v6")
        row["reading_on_v8"] = row.pop("reading_on_v6")
    C = {r["id"]: r for r in conclusions}
    def update(cid, status, reading, condition, note, premise):
        C[cid].update(status_on_v8=status, reading_on_v8=reading, break_condition=condition, break_distance_note=note,
                      deciding_premise=premise, source=f"[CALCULATION: live oct15 files pinned in {PINS.name}]",
                      premises=C[cid]["premises"] + "; v8 personal allocation; domestic-source job-capital tax; completed membership; bounded mixed-unit removal and coverage, post-engine",
                      rival_reading="[FRAMING-SENSITIVE] Alternative conventions and comparison populations answer different questions; live alternatives are reported in the break-condition and premise cells.")
    def arm_text(arm):
        return f"{arm}: ${pair_text(band(arms[arm]))}bn ({num(arms[arm], 'move_pct_of_midpoint'):+.1f}%)"
    cut_text = "; ".join(f"{r['set']} ({num(r, 'move_pct_of_midpoint'):+.1f}%)" for r in cuts if int(float(r["size"])) <= 2)
    update("C1", "holds, restated", f"${pair_text(summary['band_bn'])}bn; midpoint ${midpoint:.1f}bn; ${pair_text(summary['per_member_usd']['set'], 0)} per member. Personal specifications {ends}.",
           f"Midpoint cuts: below ${0.75 * midpoint:.1f}bn or above ${1.25 * midpoint:.1f}bn. Minimal cuts of one or two: {cut_text}. {arm_text('first_year_horizon')}. {horizon_clause}; items6/9 business property at 0, corporate and production at 1-alpha; completion in full with first-year parent responses and source endpoint prices; items11/12 full post-engine [ASSUMPTION; APPROX]. [APPROX: additive item/lineage arms in combinations]",
           f"{len(cuts)} minimal cuts. All arms and stacks remain in c1_arms_oct15.csv and c1_min_cuts_oct15.csv.", "P02/P03/P04/P05/P20, and v8 receipt rules")
    t = tally_of("case_accrual")
    status2 = "direct-receipt clause holds at both ends" if min(t) >= 0 else "direct-receipt clause BREAKS at both ends" if max(t) < 0 else "direct-receipt clause splits by end"
    be_text = "; ".join(f"{r['case']} {r['variant']} {r['allocation']}: {100*num(r,'break_even_most_adverse'):.2f}% / {100*num(r,'break_even_least_adverse'):.2f}%" for r in be)
    update("C2", status2, f"Direct receipts less household transfers: ${pair_text(t)}bn. Union at case responses ${pair_text(tally_of('union_at_case_responses'))}bn; cash ${pair_text(tally_of('cash_set'))}bn.",
           f"{be_text}. At scheduled benefits ${pair_text([num(tally['case_accrual', e], 'tally_at_scheduled_bn') for e in end_labels])}bn; lineage arm a ${pair_text(tally_of('lineage_arm_a'))}bn, arm c ${pair_text(tally_of('lineage_arm_c'))}bn.",
           "Direct receipts exclude job-capital indirect receipts; completion real-line carriers take their parent's class. [GAP] Post-engine mixed-unit and coverage costs have no receipt/transfer-class split in the payload, so this tally excludes them; the service break-even includes their full amounts. A negative break-even means a cost even at zero service response.", "P05 and v8 receipt/credit rules")
    C["C2"]["premises"] = "P01/P03/P04/P05/P07/P08/P20; payable-benefit accrual on 2026 separate funds; personal allocation; keyed completion and credit parts held. Class-defined tally including completion parent classes; post-engine costs excluded from this clause because their class split is undeclared."
    C["C2"]["claim_tested"] = "Historical September-27 claim: " + C["C2"]["claim_tested"]
    split_pair = lambda key: [num(split['pension_rebuilt', e], key) for e in end_labels]
    cancellation = all(abs(net) < min(abs(tax), abs(spending))/2 for net, tax, spending in zip(
        split_pair("net_move_bn"), split_pair("taxes_move_by_line_type_bn"), split_pair("spending_move_by_line_type_bn")))
    net_claim = all(8.25 <= abs(v) <= 13.75 for v in split_pair("net_move_bn"))
    # The historical range is printed in whole $bn: compare at that precision, so 57.0088 is still 57.
    side_claim = all(43.5 <= abs(v) < 57.5 for key in ("taxes_move_by_line_type_bn", "spending_move_by_line_type_bn") for v in split_pair(key))
    status3 = f"{'holds' if side_claim else 'BREAKS'} side magnitudes; {'holds' if net_claim else 'BREAKS'} net-about-11; {'holds' if cancellation else 'BREAKS'} cancellation"
    update("C3", status3,
           f"Taxes ${pair_text(split_pair('taxes_move_by_line_type_bn'), 2)}bn; spending ${pair_text(split_pair('spending_move_by_line_type_bn'), 2)}bn; net ${pair_text(split_pair('net_move_bn'), 2)}bn.",
           "The historical claim tests side magnitudes $44–57bn at its printed whole-bn precision, net-about-$11bn at a quarter ($8.25–13.75bn), and cancellation as a net below half the smaller side. Rebuilt union pension switch; lineage and every meta.items edit are held in all four runs. Their changes are not counted as dataset corrections.",
           "See both pension_rebuilt and increments_held rows. [GAP: holding lineage/items excludes their correction-dependent re-keying.]", "P08")
    deviations = {}
    for item in ("pm25_consumption", "road_crash_externality", "scale_net_earnings"):
        center = real[f"social_item_{item}", "central, both ends"]
        deviations[item] = [real[f"social_item_{item}", f"{e}, full span"] - center for e in ("low", "high")]
    ranges_text = "; ".join(f"{item}: ${pair_text(values)}bn" for item, values in deviations.items())
    update("C4", "holds, restated" if all(75 <= v <= 125 for v in social) else "BREAKS about-$100bn add", f"Social rows ${pair_text(social)}bn; published pairing ${pair_text(pairing)}bn.",
           f"A quarter of the add is ${sum(social)/8:.1f}bn; of the pairing ${sum(pairing)/8:.1f}bn. Item deviations {ranges_text}. [INFERENCE: additive published social tails; added people's rows held.]",
           "The pairing uses its own Hispanic/custody footings, rather than substituting the fiscal headline.", "C1 plus social prices and elasticities")
    share_text = "; ".join(f"{key}: {pair_text([x[key] for x in share_alternatives])}%" for key in share_alternatives[0])
    status5 = f"{'holds' if min(shares) > 50 else 'BREAKS'} most; {'holds' if all(12.5 <= value <= 100*1.25/6 for value in wins) else 'BREAKS'} about-one-in-six (quarter threshold)"
    update("C5", status5, f"State-local share {pair_text(shares)}%; cash {pair_text(cash_shares)}%; winners pooled in SPM units {pair_text(wins)}% (a / b).",
           f"Most means above 50%. Additive federal charges on the debt split: {share_text}. [ASSUMPTION: GDP-share defense $60bn; historical average-cost defense/interest charge $271bn.] Financing and pooling determine the winner shares.",
           "The winner shares are modeled incidence, not observed individual effects.", "P05/P06/P11 and v8 taxes")
    cost_min = min(num(r,k) for r in gen if r['case']=='case_accrual' for k in ('cost_low_end_bn','cost_high_end_bn'))
    bmax = max(100*num(r,k) for r in gen if r['case']=='case_accrual' for k in r if k.startswith('break_even'))
    cash_min = min(num(r,k) for r in gen if r['case']=='cash_set' for k in ('cost_low_end_bn','cost_high_end_bn'))
    cash_bmax = max(100*num(r,k) for r in gen if r['case']=='cash_set' for k in r if k.startswith('break_even'))
    update("C6", "holds" if cost_min > 0 else "BREAKS at a generation end", f"Each generation costs others at both ends under both conventions; minimum ${cost_min:.1f}bn. Largest service break-even {bmax:.1f}%.",
           f"A generation becomes a gain below its own service break-even. On cash, minimum generation cost ${cash_min:.1f}bn at the case's personal ends; largest service break-even {cash_bmax:.1f}% over both allocations and conventions. All values are in c6_generation_break_even_oct15.csv. The progress clause retains its historical cohort evidence.",
           "G3+ carries the added people and the case's lineage item parts.", "C1 and lineage/generation allocation")
    mixed_a1 = comparator_gap(comparator, MIXED_MORTALITY, "none", "accrual", "A1_third_plus_nh_white")
    moves = [100*(sum(mixed_a1)/2/references[A1]-1)]
    C["C8"]["claim_tested"] = claim
    comparison_figures = [A1, LOCAL, RAW, "age artefact removed: A3 white rates at union ages, accrual",
                          "age artefact removed: A3 white rates at union ages, cash", "local whites state by state, union ages, cash"]
    historical_midpoints = {fig: sum(num(historical[fig, e], "oct07_bn") for e in ("low", "high"))/2
                            for fig in comparison_figures}
    white_readings = "Live legacy headline gaps are withheld: they mix the case lineage and rough comparator engines. Historical oct07 figures remain historical."
    comparison_rows, matched_readings = [], []
    matched_figures = ((A1, "accrual", "A1_third_plus_nh_white"),
                       (RAW, "cash", "A1_third_plus_nh_white"),
                       (comparison_figures[3], "accrual", "A3_third_plus_nh_white_at_union_ages"),
                       (comparison_figures[4], "cash", "A3_third_plus_nh_white_at_union_ages"))
    for mortality, bound in MORTALITY_READINGS:
        for figure, basis, group in matched_figures:
            values = comparator_gap(comparator, mortality, bound, basis, group)
            matched_readings.append(f"oct15 {mortality}, mortality bound {bound}, {figure}: ${pair_text(values)}bn")
            for i, end in enumerate(("low", "high")):
                lineage_row = comparator_rows[mortality, bound, basis, ROUGH_LINEAGE, end]
                comparison_row = comparator_rows[mortality, bound, basis, group, end]
                case_value = comparator[mortality, bound, basis, "mexican_origin_engine", end]
                comparison_rows.append({"case": "oct15", "mortality_convention": mortality,
                    "mortality_bound": bound, "arm": "combined_rules_only", "allocation": "personal",
                    "basis": basis, "figure": figure, "group": group, "end": end,
                    "lineage_engine": "rough", "comparator_engine": "rough",
                    "lineage_cost_bn": comparator[mortality, bound, basis, ROUGH_LINEAGE, end],
                    "comparator_cost_bn": comparator[mortality, bound, basis, group, end],
                    "lineage_minus_comparator_bn": values[i],
                    "lineage_minus_comparator_without_item11_bn": num(lineage_row, "cost_without_item11_bn") - num(comparison_row, "cost_without_item11_bn"),
                    "mixed_unit_removal_bn": num(lineage_row, "mixed_unit_removal_bn") - num(comparison_row, 'mixed_unit_removal_bn'),
                    "comparator_item11_bn": num(comparison_row, 'mixed_unit_removal_bn'),
                    "item11_paired_se_bn": comparison_row.get('item11_paired_se_bn', ''),
                    "lineage_minus_comparator_one_sided_bn": values[i] + num(comparison_row, 'mixed_unit_removal_bn'),
                    "mixed_unit_asymmetry": comparison_row["mixed_unit_asymmetry"],
                    "framing": COMPARISON.MIXED_FRAME,
                    "case_lineage_cost_bn": case_value,
                    "case_minus_rough_lineage_bridge_bn": bridges[mortality, bound, basis, end],
                    "bridge_itemization": "white_replacement_2026_09_28/derived/lineage_engine_bridge_oct15.csv"})
    update("C8", ("A1 holds against historical map claim" if abs(moves[0])<=25 else "A1 BREAKS historical map claim")
           + "; matched local-white reading GAP",
           f"Live v8 A1 ${pair_text(mixed_a1)}bn on rough engine for both sides, mixed mortality conventions. Move on map's historical oct07 A1 midpoint: {pair_text(moves)}%. " + "; ".join(matched_readings),
           f"A quarter from the historical map midpoints ${references[A1]:.2f}bn (A1), ${references[LOCAL]:.2f}bn (local). {white_readings} The explicitly tagged A1/A3 matched readings use symmetric_results_oct15.csv; all bounds are preserved in c8_comparisons_oct15.csv. [GAP] No local-state own-production/own-mortality row is delivered; the live legacy source mixes engines and cannot clear that gap.",
           "The map remains oct07 by operator rule; the consumer is oct15. The live full lineage and A1/A3 use personal ends on the rough engine, own comparator production/status/eligibility/frame rules. The mixed mortality conventions retain whole-population lineage mortality and each comparator's own mortality. Own-group mortality replaces the lineage's mortality using both source bounds. Case-versus-rough lineage bridge and itemization are beside each gap. Item11 is measured only for the lineage; every row declares the asymmetry and reports its exclusion. Completion remains lineage-only; comparator coverage follows its lane's rule. [FRAMING-SENSITIVE]", "P05/P07/P14")
    C["C8"]["discriminating_observation"] = "[GAP] The tagged rules-only comparisons do not identify causal replacement or transport lineage-only membership/mixed-unit estimates to comparators; local-state matched mortality/production remains uncomputed."
    rivals = {
        "C1": f"[FRAMING-SENSITIVE] First-year budgets: {arm_text('first_year_horizon')}; first-year cash: {arm_text('first_year_horizon_cash')}; counted by ancestry share: ${pair_text([band(arms['ancestry_share_low'])[0], band(arms['ancestry_share_high'])[1]])}bn.",
        "C2": f"[FRAMING-SENSITIVE] Counting benefits when paid gives direct receipts less household transfers of ${pair_text(tally_of('cash_set'))}bn; payroll receipts and future earned benefits belong to different annual budgets.",
        "C3": "[ASSUMPTION] The tax side scales imputed-unauthorized wages to an assumed on-books share; correction cancellation does not validate either side's key. Spending checks and tax adjustments have different evidence.",
        "C4": f"[FRAMING-SENSITIVE] Against as many average residents, normalized PM2.5 ${real['social_item_pm25_consumption', 'normalized central, beside']:.1f}bn and crashes ${real['social_item_road_crash_externality', 'normalized central, beside']:.1f}bn. Absolute and normalized costs have different counterfactuals.",
        "C5": "[INFERENCE] Wage-channel totals assigned to survey people do not identify who gains. Household pooling and financing can change the winner share at the same aggregate cost.",
        "C6": "[INFERENCE] Today's G3+ descends from earlier stock than today's G2; the cross-section does not identify parent-to-child progress. Linked cohorts could show a different trajectory.",
        "C8": "[FRAMING-SENSITIVE] An all-residents slice answers a composition question. The white headline, own-age cash, union-age cash and local-white gaps are distinct comparisons.",
    }
    for cid, text in rivals.items():
        C[cid]["rival_reading"] = text
    for cid in ("C7", "C9"):
        C[cid]["status_on_v8"] = "unchanged historical evidence; not rerun"
        C[cid]["reading_on_v8"] = "[GAP] No v8 computation for this claim. Historical record: " + C[cid]["reading_on_v8"]
    premises = rows(D / "common_mode_oct07.csv")
    for row in premises:
        row["best_supported_alternative"] = row["best_supported_alternative"].replace("v6", "v8")
        row["effect_if_swapped"] = ""
        if row["premise_id"] == "P02":
            row["best_supported_alternative"] += "; item 6 business property at 0, corporate and production at 1-alpha [ASSUMPTION; APPROX]"
            row["effect_if_swapped"] = arm_text("first_year_horizon") + f"; {horizon_clause}; C4 horizon not re-priced here [GAP]."
        elif row["premise_id"] == "P05":
            row["effect_if_swapped"] = arm_text("pension_cash") + f"; C2 cash tally ${pair_text(tally_of('cash_set'))}bn; C5 cash share {pair_text(cash_shares)}%."
        elif row["premise_id"] == "P08":
            row["effect_if_swapped"] = f"C2 without dataset corrections ${pair_text(tally_of('v4_items_without_dataset_corrections'))}bn; C3 split in c3_correction_split_oct15.csv."
        elif row["premise_id"] == "P03":
            row["effect_if_swapped"] = arm_text("school_within_district") + "; " + arm_text("property_none")
        elif row["premise_id"] == "P20":
            row["effect_if_swapped"] = "; ".join(arm_text(a) for a in ("lineage_arm_a", "lineage_arm_c", "ancestry_share_low", "ancestry_share_high"))
        elif row["premise_id"] == "P01":
            row["effect_if_swapped"] = "[GAP] Alternative survey frame not rerun on v8. Historical experiments remain in oct07/sept29 files."
    write(D / "conclusions_oct15.csv", conclusions)
    write(D / "common_mode_oct15.csv", premises)
    write(D / "c8_comparisons_oct15.csv", comparison_rows)
    print(f"[written] conclusions_oct15.csv (9), common_mode_oct15.csv ({len(premises)}), c8_comparisons_oct15.csv ({len(comparison_rows)}); {len(current)} pinned files")


if __name__ == "__main__":
    main()
    sys.path.insert(0, str(F / "scripts"))
    from memory_budget import require_within_budget
    print(f"[memory] break-condition tables peak physical footprint {require_within_budget('break-condition tables') / 1e9:.3f} GB")

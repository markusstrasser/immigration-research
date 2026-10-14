"""Write the nine conclusions and premise matrix on live main case v7 only.

The oct07 CSVs supply the historical claims and qualitative questions, never live values.
C8 tests the map's still-oct07 sentence against the live white comparator at personal ends.
Every input file and its numeric CSV cells is pinned in tables_oct14_pins.json, rederived
after CASE_FINAL; drift stops before writing. No script repins itself. Historical scripts
and outputs are preserved. Run after engine_breaks_sept29.cjs --case oct14 and all of
the generation, white, pairing, debt and winners lanes' oct14 runs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/tables_oct14.py
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
CASE = F / "main_case_2026_10_14/derived"
PINS = HERE / "tables_oct14_pins.json"
INPUTS = [
    *[D / f"{name}_oct14.csv" for name in (
        "c1_arms", "c1_min_cuts", "c2_tally", "c2_break_even", "c3_correction_split",
        "c6_generation_break_even", "c6_inputs")],
    D / "first_year_item6_oct14.json", D / "first_year_calibration.json",
    CASE / "summary.json", CASE / "main_case_bands.csv", CASE / "corrections.json", CASE / "corrections_cash.json",
    F / "white_replacement_2026_09_28/derived/headline_oct14.csv",
    F / "white_replacement_2026_09_28/derived/rekey_summary_oct14.csv",
    F / "white_replacement_2026_09_28/derived/ipeds_terms_oct14.csv",
    F / "sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.csv",
    F / "debt_legacy_2026_09_23/derived/oct14/federal_split_2024.csv",
    F / "debt_legacy_2026_09_23/derived/oct14/summary.json",
    F / "winners_losers_2026_09_24/derived/oct14/net_shares.csv",
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
    if abs(got - want) > tol:
        blocked(f"{label}: {got} != {want} (tolerance {tol})")


def snapshot():
    """Evidence pins: every input's bytes and every numeric CSV cell, with its row and column."""
    result = {}
    for file in INPUTS:
        if not file.exists():
            blocked(f"{file.relative_to(F)} absent: run its live oct14 producer first")
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


def live_pairing_values(records):
    """Section 7 is the current pairing; dated revision rows have no live oct14 amount."""
    return {(row["column"], row["item"]): num(row, "oct14") for row in records if row["section"] == "7"}


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
        blocked("tables_oct14_pins.json absent: derive pins from the final adopted run before tables")
    pinned = json.loads(PINS.read_text())
    if pinned["inputs"] != current:
        changed = [name for name in current if current[name] != pinned["inputs"].get(name)]
        blocked(f"final evidence drift: {changed}")
    summary = json.loads((CASE / "summary.json").read_text())["v7"]
    payload = json.loads((CASE / "corrections.json").read_text())
    if payload["meta"]["adopted"] != "2026-10-14" or payload["meta"]["allocation"]["group_total"] != "personal":
        blocked("the live payload is not adopted v7 at the personal allocation")
    ends = summary["end_specifications"]["set"]
    if ends != summary["end_specifications"]["cash"]:
        blocked("set and cash ends differ: the tally rule needs revision")
    end_labels = [f"low_end_{ends[0]}", f"high_end_{ends[1]}"]
    arms = {r["arm"]: r for r in rows(D / "c1_arms_oct14.csv")}
    bands = {r["variant"]: r for r in rows(CASE / "main_case_bands.csv") if r["profile"] == "long_run_non_school_full"}
    for variant, arm, key in [("adopted", "adopted", "band_bn"), ("cash_set", "pension_cash", "cash_set_bn")]:
        for i, value in enumerate(band(arms[arm])):
            check(f"{variant} published band", value, band(bands[variant])[i], 1e-4)
            check(f"{variant} summary", value, summary[key][i], 1e-4)
    midpoint = sum(band(arms["adopted"])) / 2
    horizon = json.loads((D / "first_year_item6_oct14.json").read_text())
    for basis, arm in (("set", "first_year_horizon"), ("cash", "first_year_horizon_cash")):
        for i, value in enumerate(horizon["variants"]["fixed_capital"][basis]):
            check(f"first-year {basis} engine report", band(arms[arm])[i], value, 1e-4)
    check("first-year lower threshold", horizon["thresholds"]["low_bn"], 0.75 * sum(summary["band_bn"]) / 2, 1e-9)
    horizon_breaks = sum(horizon["variants"]["fixed_capital"]["set"])/2 < horizon["thresholds"]["low_bn"]
    if horizon_breaks != horizon["first_year_breaks_alone"]:
        blocked("first-year C1 verdict disagrees with the unrounded engine report")
    horizon_clause = "First-year horizon " + ("breaks C1 alone" if horizon_breaks else "does not break C1 alone")
    cuts = [r for r in rows(D / "c1_min_cuts_oct14.csv") if r["minimal"] == "yes"]
    tally = {(r["model"], r["end"]): r for r in rows(D / "c2_tally_oct14.csv")}
    tally_of = lambda model: [num(tally[model, e], "tally_bn") for e in end_labels]
    be = rows(D / "c2_break_even_oct14.csv")
    split = {(r["reading"], r["end"]): r for r in rows(D / "c3_correction_split_oct14.csv")}
    for row in split.values():
        check("C3 side closure", num(row, "net_move_bn"), num(row, "tax_side_move_bn") + num(row, "spending_side_move_bn") + num(row, "interaction_bn"), 2e-4)
        check("C3 full case", num(row, "all_edits_bn"), band(arms["adopted"])[end_labels.index(row["end"])], 1e-4)
    gen = rows(D / "c6_generation_break_even_oct14.csv")
    for case, oracle in [("case_accrual", "adopted"), ("cash_set", "pension_cash")]:
        for conv in ("a", "b"):
            rr = [r for r in gen if r["case"] == case and r["convention"] == conv]
            if {r["generation"] for r in rr} != {"G1", "G2", "G3plus"}:
                blocked(f"C6 incomplete generations for {case} {conv}")
            for i, key in enumerate(("cost_low_end_bn", "cost_high_end_bn")):
                check(f"C6 {case} {conv} sum", sum(num(r, key) for r in rr), band(arms[oracle])[i], 2e-4)
    white = F / "white_replacement_2026_09_28/derived"
    head = {(r["figure"], r["end"]): r for r in rows(white / "headline_oct14.csv")}
    white_summary = {(r["basis"], r["group"], r["end"]): r for r in rows(white / "rekey_summary_oct14.csv")}
    for basis, key in (("accrual", "band_bn"), ("cash", "cash_set_bn")):
        for i, end in enumerate(("low", "high")):
            row = white_summary[basis, "mexican_origin_engine", end]
            check(f"C8 {basis} engine union on final adopted case {end}", num(row, "cost"), summary[key][i], 1e-4)
            check(f"C8 {basis} personal end {end}", num(row, "spec"), ends[i], 0)
    A1 = "age artefact removed: A1 third-plus whites, accrual (central)"
    LOCAL = "local whites state by state, union ages, accrual (central)"
    RAW = "raw cash at white ages: A1, cash set"
    def white_band(figure):
        return [num(head[figure, end], "oct14_bn") for end in ("low", "high")]
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
        blocked("C8 map's claim text changed from oct07: restate its frame before grading oct14")
    real = live_pairing_values(rows(F / "sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.csv"))
    pairing = [real["pairing_on_priced_count", f"published pairing ({e})"] for e in ("low", "high")]
    footing = [real["hispanic", "fiscal main case (low)"], real["custody", "fiscal main case (high)"]]
    social = [p - f for p, f in zip(pairing, footing)]
    debt_dir = F / "debt_legacy_2026_09_23/derived/oct14"
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
    winners = {(r["net"], r["stack"], r["unit"]): r for r in rows(F / "winners_losers_2026_09_24/derived/oct14/net_shares.csv")}
    wins = [100 * num(winners[f"net_social_{c}", "central", "spm_unit_pooled"], "winners_share") for c in ("a", "b")]
    conclusions = rows(D / "conclusions_oct07.csv")
    for row in conclusions:
        row["status_on_v7"] = row.pop("status_on_v6")
        row["reading_on_v7"] = row.pop("reading_on_v6")
    C = {r["id"]: r for r in conclusions}
    def update(cid, status, reading, condition, note, premise):
        C[cid].update(status_on_v7=status, reading_on_v7=reading, break_condition=condition, break_distance_note=note,
                      deciding_premise=premise, source=f"[CALCULATION: live oct14 files pinned in {PINS.name}]",
                      premises=C[cid]["premises"] + "; v7 personal allocation, mixed-unit child credits, job-capital taxes and items 7/8 through meta.items",
                      rival_reading="[FRAMING-SENSITIVE] Alternative conventions and comparison populations answer different questions; live alternatives are reported in the break-condition and premise cells.")
    def arm_text(arm):
        return f"{arm}: ${pair_text(band(arms[arm]))}bn ({num(arms[arm], 'move_pct_of_midpoint'):+.1f}%)"
    cut_text = "; ".join(f"{r['set']} ({num(r, 'move_pct_of_midpoint'):+.1f}%)" for r in cuts if int(float(r["size"])) <= 2)
    update("C1", "holds, restated", f"${pair_text(summary['band_bn'])}bn; midpoint ${midpoint:.1f}bn; ${pair_text(summary['per_member_usd']['set'], 0)} per member. Personal specifications {ends}.",
           f"Midpoint cuts: below ${0.75 * midpoint:.1f}bn or above ${1.25 * midpoint:.1f}bn. Minimal cuts of one or two: {cut_text}. {arm_text('first_year_horizon')}. {horizon_clause}; item 6 business property at 0, corporate and production at 1-alpha [ASSUMPTION; APPROX]. [APPROX: additive item/lineage arms in combinations]",
           f"{len(cuts)} minimal cuts. All arms and stacks remain in c1_arms_oct14.csv and c1_min_cuts_oct14.csv.", "P02/P03/P04/P05/P20, and v7 receipt rules")
    t = tally_of("case_accrual")
    status2 = "direct-receipt clause holds at both ends" if min(t) >= 0 else "direct-receipt clause BREAKS at both ends" if max(t) < 0 else "direct-receipt clause splits by end"
    be_text = "; ".join(f"{r['case']} {r['variant']} {r['allocation']}: {100*num(r,'break_even_most_adverse'):.2f}% / {100*num(r,'break_even_least_adverse'):.2f}%" for r in be)
    update("C2", status2, f"Direct receipts less household transfers: ${pair_text(t)}bn. Union at case responses ${pair_text(tally_of('union_at_case_responses'))}bn; cash ${pair_text(tally_of('cash_set'))}bn.",
           f"{be_text}. At scheduled benefits ${pair_text([num(tally['case_accrual', e], 'tally_at_scheduled_bn') for e in end_labels])}bn; lineage arm a ${pair_text(tally_of('lineage_arm_a'))}bn, arm c ${pair_text(tally_of('lineage_arm_c'))}bn.",
           "Direct receipts exclude job-capital indirect receipts; the service break-even includes their responses. A negative break-even means a cost even at zero service response.", "P05 and v7 receipt/credit rules")
    C["C2"]["premises"] = "P01/P03/P04/P05/P07/P08/P20; pensions at payable-benefit accrual on the 2026 separate funds; personal allocation; credits and all meta.items parts held. Direct receipts and household transfers are the engine's distinct responsive classes at the live ends."
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
           "The winner shares are modeled incidence, not observed individual effects.", "P05/P06/P11 and v7 taxes")
    cost_min = min(num(r,k) for r in gen if r['case']=='case_accrual' for k in ('cost_low_end_bn','cost_high_end_bn'))
    bmax = max(100*num(r,k) for r in gen if r['case']=='case_accrual' for k in r if k.startswith('break_even'))
    cash_min = min(num(r,k) for r in gen if r['case']=='cash_set' for k in ('cost_low_end_bn','cost_high_end_bn'))
    cash_bmax = max(100*num(r,k) for r in gen if r['case']=='cash_set' for k in r if k.startswith('break_even'))
    update("C6", "holds" if cost_min > 0 else "BREAKS at a generation end", f"Each generation costs others at both ends under both conventions; minimum ${cost_min:.1f}bn. Largest service break-even {bmax:.1f}%.",
           f"A generation becomes a gain below its own service break-even. On cash, minimum generation cost ${cash_min:.1f}bn at the case's personal ends; largest service break-even {cash_bmax:.1f}% over both allocations and conventions. All values are in c6_generation_break_even_oct14.csv. The progress clause retains its historical cohort evidence.",
           "G3+ carries the added people and the case's lineage item parts.", "C1 and lineage/generation allocation")
    moves = [100*(sum(white_band(fig))/2/references[fig]-1) for fig in (A1, LOCAL)]
    C["C8"]["claim_tested"] = claim
    comparison_figures = [A1, LOCAL, RAW, "age artefact removed: A3 white rates at union ages, accrual",
                          "age artefact removed: A3 white rates at union ages, cash", "local whites state by state, union ages, cash"]
    historical_midpoints = {fig: sum(num(historical[fig, e], "oct07_bn") for e in ("low", "high"))/2
                            for fig in comparison_figures}
    white_readings = "; ".join(f"{fig}: ${pair_text(white_band(fig))}bn ({100*(sum(white_band(fig))/2/historical_midpoints[fig]-1):+.1f}% on the same historical figure)"
                               for fig in comparison_figures)
    update("C8", "holds against historical map claim" if max(abs(v) for v in moves)<=25 else "BREAKS historical map claim", f"Live v7 A1 ${pair_text(white_band(A1))}bn; local whites ${pair_text(white_band(LOCAL))}bn. Moves on map's oct07 midpoints: {pair_text(moves)}%.",
           f"A quarter from the historical map midpoints ${references[A1]:.2f}bn (A1), ${references[LOCAL]:.2f}bn (local). {white_readings}. Every live comparator arm is pinned from headline/rekey_summary/ipeds_terms_oct14.csv.",
           "The map remains oct07 by operator rule; the consumer is oct14. Both comparison sides use v7 personal ends and R7. Union credits are measured; no comparator mixed-unit credit is invented. [FRAMING-SENSITIVE]", "P05/P07/P14")
    C["C8"]["discriminating_observation"] = "[GAP] The re-key remains a rough comparison rather than an engine run on each comparison population. Frame, age and reference-group choices remain consequential."
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
        C[cid]["status_on_v7"] = "unchanged historical evidence; not rerun"
        C[cid]["reading_on_v7"] = "[GAP] No v7 computation for this claim. Historical record: " + C[cid]["reading_on_v7"]
    premises = rows(D / "common_mode_oct07.csv")
    for row in premises:
        row["best_supported_alternative"] = row["best_supported_alternative"].replace("v6", "v7")
        row["effect_if_swapped"] = ""
        if row["premise_id"] == "P02":
            row["best_supported_alternative"] += "; item 6 business property at 0, corporate and production at 1-alpha [ASSUMPTION; APPROX]"
            row["effect_if_swapped"] = arm_text("first_year_horizon") + f"; {horizon_clause}; C4 horizon not re-priced here [GAP]."
        elif row["premise_id"] == "P05":
            row["effect_if_swapped"] = arm_text("pension_cash") + f"; C2 cash tally ${pair_text(tally_of('cash_set'))}bn; C5 cash share {pair_text(cash_shares)}%."
        elif row["premise_id"] == "P08":
            row["effect_if_swapped"] = f"C2 without dataset corrections ${pair_text(tally_of('v4_items_without_dataset_corrections'))}bn; C3 split in c3_correction_split_oct14.csv."
        elif row["premise_id"] == "P03":
            row["effect_if_swapped"] = arm_text("school_within_district") + "; " + arm_text("property_none")
        elif row["premise_id"] == "P20":
            row["effect_if_swapped"] = "; ".join(arm_text(a) for a in ("lineage_arm_a", "lineage_arm_c", "ancestry_share_low", "ancestry_share_high"))
        elif row["premise_id"] == "P01":
            row["effect_if_swapped"] = "[GAP] Alternative survey frame not rerun on v7. Historical experiments remain in oct07/sept29 files."
    write(D / "conclusions_oct14.csv", conclusions)
    write(D / "common_mode_oct14.csv", premises)
    print(f"[written] conclusions_oct14.csv (9), common_mode_oct14.csv ({len(premises)}); {len(current)} pinned files")


if __name__ == "__main__":
    main()

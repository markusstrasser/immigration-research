"""Direct age >=18 allocation from the gated convention-a person kernel.

The source kernel has the household consumer's driver/credit rules, constants
per member and fixed national totals. These are modeled allocations. Its 161
replicates give conditional sampling uncertainty, not account-wide uncertainty.
Historical files are read-only; outputs compute only oct15.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
COVERAGE = HERE.parent / "coverage_bound_2026_10_14"
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget


def require(ok, message):
    if not ok:
        raise SystemExit("[BLOCKED] direct adults: " + message)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def sdr(values):
    return float(np.sqrt(4 / 160 * np.sum((values[1:] - values[0]) ** 2)))


def credit_age_correction(summary, snapshot, audit, piece_prices, weights, selected, adult, end):
    """Replace first-order generic credit spreading with actual source owner ages."""
    source = HERE / "derived/credit_replicates_oct15.json"
    credits = json.loads(source.read_text())
    require(bool(credits["gates"]) and all(g["passed"] for g in credits["gates"]), "credit source gates")
    group = snapshot["generations"]["G2"][end]
    fit = [r for r in group["rows"] if r["id"] == "federal_income_tax" and r["side"] == "receipt"]
    require(len(fit) == 1 and fit[0]["response"] == 1, "FIT selected key/response")
    refund = [r for r in group["rows"] if r["id"] == "refundable_tax_credits" and r["side"] == "spending"]
    require(len(refund) == 1 and refund[0]["response"] == 1, "refund response")
    scenario = fit[0]["scenario"]
    fractions = {}
    for side, line, key in (("receipt", "federal_income_tax", fit[0]["key"]),
                            ("spending", "refundable_tax_credits", "refundable_credits")):
        indexes = [i for i, row in enumerate(audit["denominator_pieces"])
                   if row["end"] == end and row["generation"] == "G2" and row["line"] == line
                   and f"canonical {side}:{key}" in row["key"]]
        require(len(indexes) == 1, "no unique generic credit source piece " + line)
        vector = piece_prices[indexes[0]]
        denominator = vector[selected] @ weights[selected]
        require(np.all(np.abs(denominator) > 1e-15), "zero generic credit source mass")
        fractions[side] = (vector[adult] @ weights[adult]) / denominator
    generic_spend = np.asarray(credits["mean_base_credit_spending_bn"]["a"]["G2"])
    generic_receipt = np.asarray(credits["base_credit_receipt_edit_bn"]["a"]["G2"][scenario])
    owner_spend = np.asarray(credits["mean_base_credit_spending_bn"]["a_age"]["G2_adult"])
    owner_receipt = np.asarray(credits["base_credit_receipt_edit_bn"]["a_age"]["G2_adult"][scenario])
    correction = owner_spend - owner_receipt - generic_spend[0] * fractions["spending"] + generic_receipt[0] * fractions["receipt"]
    total_credit_replicates = generic_spend - generic_receipt
    r6 = next(it for it in summary["items"]["split"]["a"] if it["id"] == "child_credits")
    part_checks = []
    for edit in r6["edits"]:
        if edit["side"] == "receipt" and edit.get("scenario") != scenario:
            continue
        for part in edit["parts"]:
            route = part.get("route", {})
            if route.get("kind") != "union" or route.get("generation") != "G2":
                continue
            component = route["component"]
            own = credits["r6_age_parts_edit_bn"]["a_age"][component]
            adult_values = np.asarray(own["G2_adult"])
            minor_values = np.asarray(own["G2_minor"])
            selected_amount = part["bn"]["G2"]["personal"]
            scale = 1.0
            measured = adult_values[0] + minor_values[0]
            if edit["side"] == "receipt" and measured:
                scale = selected_amount / measured  # source scenario's declared scaling
            require(abs(scale * measured - selected_amount) < 1e-9,
                    "R6 age component differs from selected case " + component)
            sign = -1 if edit["side"] == "receipt" else 1
            correction += sign * (scale * adult_values - selected_amount * fractions[edit["side"]])
            total_credit_replicates += sign * scale * (adult_values + minor_values)
            part_checks.append({"component": component, "selected_amount_bn": selected_amount,
                                "adult_owner_edit_bn": float(scale * adult_values[0]),
                                "scenario_scale": scale})
    interaction_source = HERE / "derived/union_credit_age_oct15.json"
    interaction = json.loads(interaction_source.read_text())["expanded_minus_canonical"]
    completion = next(it for it in summary["items"]["split"]["a"] if it["id"] == "union_completion")
    interaction_checks = []
    for edit in completion["edits"]:
        if edit["side"] == "receipt" and edit.get("scenario") != scenario:
            continue
        for part in edit["parts"]:
            route = part["route"]
            if route["component"] != "credit_interaction" or route["generation"] != "G2":
                continue
            field = "receipts" if edit["side"] == "receipt" else "spending"
            owner_adult = np.asarray(interaction[field]["G2_adult"])
            owner_minor = np.asarray(interaction[field]["G2_minor"])
            total = owner_adult[0] + owner_minor[0]
            amount = part["bn"]["G2"]["personal"]
            require(bool(total) or abs(amount) < 1e-12, "zero item10 credit-owner source")
            scale = amount / total if total else 0.0
            require(abs(total * scale - amount) < 1e-9, "item10 credit age does not collapse")
            sign = -1 if edit["side"] == "receipt" else 1
            correction += sign * (scale * owner_adult - amount * fractions[edit["side"]])
            total_credit_replicates += sign * scale * (owner_adult + owner_minor)
            interaction_checks.append({"side": edit["side"], "selected_amount_bn": amount,
                                       "adult_owner_edit_bn": float(scale * owner_adult[0]), "scenario_scale": scale})
    return correction, total_credit_replicates - total_credit_replicates[0], {
        "source_sha256": sha(source), "generic_adult_share": {k: float(v[0]) for k, v in fractions.items()},
        "adult_correction_bn": float(correction[0]), "conditional_sdr_se_bn": sdr(correction),
        "r6_parts": part_checks, "item10_parts": interaction_checks,
        "item10_source_sha256": sha(interaction_source),
        "rule": "undo generic cash-FIT/refund key allocation of P7 base/R6 and item10 credit changes; add source claimant/dependent age allocation; benefit-tax component untouched"}


def calculate(basis):
    case = "oct15" + ("_cash" if basis == "cash" else "")
    summary = json.loads((HERE / f"derived/generation_summary_{case}.json").read_text())
    final = bool(summary.get("post_engine", {}).get("coverage"))
    vintage = "oct15_final_routing" if final else "oct15"
    cache = COVERAGE / "_cache" / vintage / basis
    audit = json.loads((COVERAGE / f"derived/pricing_audit_{vintage}_{basis}.json").read_text())
    source = cache / "pricing.npz"
    require(audit.get("pricing_cache_sha256") == sha(source), "pricing cache changed")
    require(audit.get("case") == "oct15" and audit.get("basis") == basis,
            "case or basis mismatch")
    require(audit.get("gates", {}).get("physical_footprint_within_2_5GB") is True,
            "source has no successful physical-footprint receipt")
    with np.load(source, allow_pickle=False) as prices:
        weights = prices["weights"]
        age, generation = prices["age"], prices["generation"]
        net = prices["net_id"]
        piece_prices = prices["base_piece_prices"]
    require(weights.shape[1] == 161 and net.shape == (2, len(age), 161), "kernel dimensions")
    selected = generation == 1
    adult, minor = selected & (age >= 18), selected & (age < 18)
    snapshot_path = COVERAGE / "inputs" / (vintage if final else "oct15_base") / ("lines_cash.json" if basis == "cash" else "lines.json")
    snapshot = json.loads(snapshot_path.read_text())
    coverage_path = COVERAGE / "derived/coverage_bound_oct15.json"
    coverage = None
    if final:
        require(coverage_path.exists(), "final coverage missing")
        coverage = json.loads(coverage_path.read_text())["sets"][basis]["scenarios"]["central"]
    records, checks, corrections = [], [], []
    for end_i, end in enumerate(("low", "high")):
        totals = {}
        for label, mask in (("adult", adult), ("minor", minor)):
            totals[label] = (net[end_i, mask] * weights[mask]).sum(axis=0)
        whole = (net[end_i, selected] * weights[selected]).sum(axis=0)
        gap = float(np.max(np.abs(totals["adult"] + totals["minor"] - whole)))
        require(gap < 1e-9, "adult/minor partition does not close")
        corrected, whole_credit_delta, credit_receipt = credit_age_correction(
            summary, snapshot, audit, piece_prices, weights, selected, adult, end)
        generic_adult = float(totals["adult"][0])
        totals["adult"] += corrected
        totals["minor"] += whole_credit_delta - corrected
        require(np.max(np.abs(totals["adult"] + totals["minor"] - whole - whole_credit_delta)) < 1e-9,
                "credit-owner adult/minor partition does not close")
        corrections.append({"end": end, **credit_receipt})
        coverage_adult = coverage_minor = 0.0
        if coverage:
            c = coverage["ends"][end]
            require("adult_cost_by_generation_bn" in c and "minor_cost_by_generation_bn" in c,
                    "coverage has no exact adult/minor decomposition")
            coverage_adult = c["adult_cost_by_generation_bn"]["G2"]
            coverage_minor = c["minor_cost_by_generation_bn"]["G2"]
            require(abs(coverage_adult + coverage_minor - c["by_generation"]["G2"]) < 1e-9,
                    "coverage adult/minor parts do not close")
        target = summary["conventions"]["a"]["G2"]["cost_bn"][end_i]
        gap_final = abs(float(whole[0]) + coverage_adult + coverage_minor - target)
        require(gap_final < 1e-9, "direct allocation differs from final G2(a): " + str(gap_final))
        population_reps = weights[adult].sum(axis=0)
        if coverage:
            population_reps += coverage["adults_by_generation"]["G2"]
        values = totals["adult"] + coverage_adult
        per_adult = values * 1e9 / population_reps
        old = summary["g2_adults_alone"]["cost_bn"][end_i]
        records.append({"case": case, "end": end, "convention": "a",
                        "rule": "A_AGE>=18; source credit owner ages; remaining person keys; coverage own age block",
                        "fixes": "|".join(summary["policy"]["fixes"]),
                        "minor_scale": summary["policy"]["minor_scale"],
                        "production_rule": summary["policy"]["production_rule"],
                        "g2_adults_direct_bn": float(values[0]),
                        "first_order_generic_adult_bn": generic_adult,
                        "credit_owner_age_correction_bn": float(corrected[0]),
                        "g2_minors_direct_bn": float(totals["minor"][0]) + coverage_minor,
                        "g2_total_a_bn": target, "g2_adults_residual_bn": old,
                        "direct_minus_residual_bn": float(values[0]) - old,
                        "adults": float(population_reps[0]), "per_adult_usd": float(per_adult[0]),
                        "conditional_sdr_se_bn": sdr(values),
                        "conditional_per_adult_sdr_se_usd": sdr(per_adult),
                        "coverage_adult_cost_bn": coverage_adult,
                        "coverage_minor_cost_bn": coverage_minor})
        checks.append({"end": end, "all_replicate_partition_gap_bn": gap,
                       "final_G2_a_gap_bn": gap_final, "pass": True})
    receipt = {"case": case, "basis": basis, "source": str(source.relative_to(HERE.parent)),
               "source_sha256": sha(source), "policy": summary["policy"], "rows": records,
               "gates": checks, "credit_owner_age_corrections": corrections,
               "uncertainty": "conditional person allocation plus actual credit-owner age replicates; remaining national/generation totals fixed; excludes full fiscal-model uncertainty, parent misreporting and modeled coverage uncertainty"}
    require_within_budget()
    return records, receipt


def main():
    rows, receipts = [], {}
    for basis in ("set", "cash"):
        records, receipts[basis] = calculate(basis)
        rows.extend(records)
    out = HERE / "derived"
    with (out / "g2_adults_direct_oct15.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (out / "g2_adults_direct_oct15.json").write_text(json.dumps(receipts, indent=1) + "\n")
    print("direct G2 adults: accrual/cash, both ends, partitions PASS")


if __name__ == "__main__":
    main()

"""Joint SDR uncertainty and explicit contents of convention-b numerators.

This propagates measured routing inputs jointly, not a full fiscal-model SE.
Unknown coverage, misreporting, national-price and latent-demography uncertainty
remain unidentified. Never infer an observed generation ranking from this file.
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
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget

GENS = ("G1", "G2", "G3plus")


def read(path):
    return json.loads(path.read_text())


def require(ok, message):
    if not ok:
        raise SystemExit("[BLOCKED] allocation uncertainty: " + message)


def sdr(array):
    return float(np.sqrt(4 / 160 * np.square(array[1:] - array[0]).sum()))


def write_csv(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    measurement = read(HERE / "inputs/minor_parent_measurement_oct15.json")
    credit = read(HERE / "derived/credit_replicates_oct15.json")
    gradients = read(HERE / "derived/native_parent_gradients_oct15.json")
    interaction = read(HERE / "derived/union_credit_age_oct15.json")["expanded_minus_canonical"]
    share = np.asarray(measurement["replicate_shares"])
    rows, contents, receipts = [], [], {}
    for case, basis in (("oct15", "set"), ("oct15_cash", "cash")):
        central = read(HERE / f"derived/generation_summary_{case}.json")
        zero = read(HERE / f"_cache/routing_audit/{case}/no_added_G2/generation_summary_{case}.json")
        one = read(HERE / f"_cache/routing_audit/{case}/wholly_G2/generation_summary_{case}.json")
        payload = read(HERE / f"derived/generation_corrections_{case}.json")["payloads"]["b"]
        snapshot = read(HERE.parent / f"coverage_bound_2026_10_14/inputs/oct15_final_routing/lines{'_cash' if basis == 'cash' else ''}.json")
        coverage = read(HERE.parent / "coverage_bound_2026_10_14/derived/coverage_bound_oct15.json")["sets"][basis]["scenarios"]["central"]
        raw_adults = measurement["adult_population_replicates"]
        cost_replicates = {g: [] for g in GENS}
        for end_i, end in enumerate(("low", "high")):
            scenario = snapshot["generations"]["G2"][end]["receipt_scenario"]
            r6 = next(it for it in central["items"]["split"]["b"] if it["id"] == "child_credits")
            r6_delta = {g: np.zeros(161) for g in GENS}
            interaction_delta = {g: np.zeros(161) for g in GENS}
            for edit in r6["edits"]:
                if edit["side"] == "receipt" and edit.get("scenario") != scenario:
                    continue
                for part in edit["parts"]:
                    route = part.get("route", {})
                    if route.get("kind") != "union":
                        continue
                    component = route["component"]
                    source = credit["r6_b_parts_edit_bn"][component]
                    total = sum(source[g][0] for g in GENS)
                    selected_total = part["union_bn"]["personal"]
                    scale = selected_total / total if total else 0.0
                    require(bool(total) or abs(selected_total) < 1e-12, "zero R6 component denominator")
                    for g in GENS:
                        values = np.asarray(source[g]) * scale
                        require(abs(values[0] - part["bn"][g]["personal"]) < 1e-9,
                                "R6 source ownership differs from selected case component " + component)
                        r6_delta[g] += (1 if edit["side"] == "spending" else -1) * (values - values[0])
            completion = next(it for it in central["items"]["split"]["b"] if it["id"] == "union_completion")
            for edit in completion["edits"]:
                if edit["side"] == "receipt" and edit.get("scenario") != scenario:
                    continue
                for part in edit["parts"]:
                    route = part["route"]
                    if route["component"] != "credit_interaction":
                        continue
                    g = route["generation"]
                    field = "receipts" if edit["side"] == "receipt" else "spending"
                    source = np.asarray(interaction[field][g + "_adult"]) + np.asarray(interaction[field][g + "_minor"])
                    amount = part["bn"][g]["personal"]
                    require(bool(source[0]) or abs(amount) < 1e-12, "zero item10 credit covariance source")
                    scale = amount / source[0] if source[0] else 0.0
                    interaction_delta[g] += (1 if edit["side"] == "spending" else -1) * scale * (source - source[0])
            for g in GENS:
                value = central["conventions"]["b"][g]["cost_bn"][end_i]
                slope = one["conventions"]["b"][g]["cost_bn"][end_i] - zero["conventions"]["b"][g]["cost_bn"][end_i]
                require(abs(zero["conventions"]["b"][g]["cost_bn"][end_i] + slope * share[0] - value) < 1e-9,
                        "historical routing share is not affine")
                values = np.full(161, value) + slope * (share - share[0])
                base_credit = np.asarray(credit["mean_base_credit_net_cost_bn"]["b"][g][scenario])
                values += base_credit - base_credit[0] + r6_delta[g]
                values += interaction_delta[g]
                values += np.asarray(central["state_price_replicate_delta_bn"]["b"][g][end_i])
                values += np.asarray(central["reporter_parent_replicate_delta_bn"]["b"][g][end_i])
                mixed = np.asarray(payload[g]["meta"]["mixed_unit_removal"]["by_end"][end]["replicates_bn"])
                values += mixed - mixed[0]
                # Native parents are directly linked; hold each source band count
                # fixed and propagate its measured G2 fraction through exact b slopes.
                for kind in ("g3_rate", "later"):
                    for band in measurement["native_observed_children"]["by_rate_class"][kind]["by_age_band"]:
                        persons = np.asarray(band["persons"]["replicates"])
                        equivalent = np.asarray(band["g2_equivalents"]["replicates"])
                        if not persons[0]:
                            require(np.all(equivalent == 0), "nonempty parent numerator in empty band")
                            continue
                        require(np.all(persons > 0), "native band missing from a replicate")
                        allocated = persons[0] * equivalent / persons
                        gradient = gradients["sets"][basis]["by_rate_class"][kind][str(band["band"])][end][g]
                        values += gradient * (allocated - allocated[0])
                cost_replicates[g].append(values)
            adults = {g: np.asarray(raw_adults[g]) + central["conventions"]["b"][g]["adults"] - raw_adults[g][0] for g in GENS}
            require(all(np.all(v > 0) for v in adults.values()), "nonpositive adult denominator")
            per = {g: cost_replicates[g][end_i] * 1e9 / adults[g] for g in GENS}
            difference = per["G2"] - per["G3plus"] if basis == "set" else per["G3plus"] - per["G2"]
            rows.append({"case": case, "end": end, "convention": "b", "fixes": "|".join(central["policy"]["fixes"]),
                         "minor_scale": central["policy"]["minor_scale"], "production_rule": central["policy"]["production_rule"],
                         "difference": "G2 minus G3plus" if basis == "set" else "G3plus minus G2",
                         "per_adult_difference_usd": float(difference[0]), "conditional_joint_sdr_se_usd": sdr(difference),
                         "full_fiscal_model_se": "unidentified", "measured_generation_ranking": False})
        receipts[case] = {"policy": central["policy"], "cost_replicates_bn": {g: [v.tolist() for v in q] for g, q in cost_replicates.items()}}
        for g in GENS:
            source = measurement["propagated_observed_rule_breakdown"][g]
            original = measurement["canonical_rule_breakdown"][g]
            for end_i, end in enumerate(("low", "high")):
                contents.append({"case": case, "end": end, "convention": "b", "generation": g,
                                 "numerator_cost_bn": central["conventions"]["b"][g]["cost_bn"][end_i],
                                 "adult_denominator": central["conventions"]["b"][g]["adults"],
                                 "observed_adults": source["adults_own_generation"]["estimate"],
                                 "observed_minors_with_union_parent": source["minors_with_union_parent"]["estimate"],
                                 "observed_minors_without_union_parent_including_relative_fallback": source["minors_without_union_parent"]["estimate"],
                                 "original_canonical_minors_without_union_parent": original["minors_without_union_parent"]["estimate"],
                                 "modeled_added_minor_G2_equivalents": central["routing"]["age"]["minor_count"] * share[0] if g == "G2" else 0.0,
                                 "modeled_added_minors_assigned": central["routing"]["age"]["minor_count"] * share[0] if g == "G2" else
                                     central["lineage"]["counts"]["added"] - central["added_adults"]["adults"] - central["routing"]["age"]["minor_count"] * share[0] if g == "G3plus" else 0.0,
                                 "modeled_added_adults": central["added_adults"]["adults"] if g == "G3plus" else 0.0,
                                 "coverage_adults": coverage["adults_by_generation"][g],
                                 "coverage_minors": coverage["implied_net_missing_people"][g] - coverage["adults_by_generation"][g],
                                 "contents_rule": "adults plus minors assigned under named frame rules; absent-parent relative fallback retained; added/coverage people modeled; not a measured ranking"})
    require_within_budget()
    write_csv(HERE / "derived/per_adult_differences_oct15.csv", rows)
    write_csv(HERE / "derived/generation_numerator_contents_oct15.csv", contents)
    receipts["uncertainty"] = "joint same161 survey replicates for historical parent fractions, observed reporter parent-driver shares, credit ownership, state indexes, mixed-unit changes and observed adult denominators; conditional on national fiscal totals, other generation key costs, fixed latent demography and source coverage prices; misreporting/coverage/model uncertainty unidentified"
    receipts["existing_union_parent_vintage"] = "P7_frozen; six preexisting minors whose parents enter through union completion retain their pinned original parent assignment; exact fully-completed-frame difference is preserved in measurement input, not silently represented as priced"
    receipts["source_hashes"] = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                                 for name in ("inputs/minor_parent_measurement_oct15.json", "derived/credit_replicates_oct15.json", "derived/native_parent_gradients_oct15.json", "derived/union_credit_age_oct15.json")}
    (HERE / "derived/allocation_uncertainty_oct15.json").write_text(json.dumps(receipts, indent=1) + "\n")
    print("per-adult named allocations: joint161 routing covariance PASS; full model uncertainty unidentified")


if __name__ == "__main__":
    main()

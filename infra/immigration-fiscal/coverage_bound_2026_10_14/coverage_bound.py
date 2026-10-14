"""Cohort coverage sensitivity beside v7, with fixed case prices and national masses.
Native-First: pinned Census tables and the existing case consumer's person pricing.
Historical filenames stay; public output fields use coverage, never bound.
"""
import csv
from datetime import date
import hashlib
import json
import math
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from export_pricing import validate_metadata, verify_local_pins
from source_tables import load
from dependency_manifest import MANIFEST, validate_manifest

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
# Preserve the original v7 generation/household pricing epoch while P7 peers revise their lane.
GEN = LANE / "inputs/generation_results_original.csv"
SUMMARY = ROOT / "infra/immigration-fiscal/main_case_2026_10_14/derived/summary.json"
ENDS = ("low", "high")
GENS = ("G1", "G2", "G3plus")
TOL = 1e-6
# Calendar-based uniform-birthday approximation at the case's March 15 survey date.
BIRTH_OLDER_SHARE = (date(2020, 4, 1) - date(2020, 3, 15)).days / (date(2021, 3, 15) - date(2020, 3, 15)).days


def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] " + why)


def validate_generation_rows(rows, summary):
    require(summary["v7"]["end_specifications"]["set"] == [16, 11], "mismatched case specifications")
    chosen = [r for r in rows if r["convention"] == "a"]
    keys = [(r["band_end"], r["generation"]) for r in chosen]
    require(len(keys) == len(set(keys)), "duplicate generation row")
    require(set(keys) == {(e, g) for e in ENDS for g in GENS}, "missing or extra generation/end row")
    for r in chosen:
        require(r["allocation"] == "personal", "mismatched generation allocation")
        for field in ("cost_bn", "population"):
            try:
                value = float(r[field])
            except (ValueError, TypeError):
                require(False, "invalid generation value " + field)
            require(math.isfinite(value), "non-finite generation value " + field)
        require(float(r["population"]) > 0, "non-positive generation population")
    for i, end in enumerate(ENDS):
        require(math.isfinite(float(summary["main_case"][i])), "non-finite case value")
        require(abs(sum(float(x["cost_bn"]) for x in chosen if x["band_end"] == end)
                    - summary["main_case"][i]) < TOL, "generation costs do not close to case")
    return {(r["band_end"], r["generation"]): r for r in chosen}


def pes_label(age, sex):
    if age <= 4:
        return "0 to 4", (0, 4)
    if age <= 9:
        return "5 to 9", (5, 9)
    if age <= 17:
        return "10 to 17", (10, 17)
    if age <= 29:
        return "18 to 29 " + ("males" if sex == 1 else "females"), (18, 29)
    if age <= 49:
        return "30 to 49 " + ("males" if sex == 1 else "females"), (30, 49)
    return "50 and over " + ("males" if sex == 1 else "females"), (50, 100)


def rate_at(age2020, sex, rates, base, mode="central", se_shift=0.0):
    label, band = pes_label(age2020, sex)
    cell = base[(*band, sex)]
    q = cell["base_over_census"]
    if (age2020 <= 4 and mode != "pes_only") or (mode.startswith("da_") and age2020 <= 29):
        series = mode.split("_")[1] if mode.startswith("da_") else "middle"
        return cell["da_residual_factor_" + series]
    estimate = rates["hispanic"][label]
    nce = (estimate["nce_pct"] + se_shift * estimate["se_pct"]) / 100
    require(1 + nce > 0 and q > 0, "invalid coverage denominator")
    return 1 / ((1 + nce) * q) - 1


def factors(data, rates, base, mode="central", se_shift=0.0, birth_arm="mixture", arrival_arm="central"):
    n = len(data["age"])
    f, added_f = np.zeros(n), np.zeros(n)
    for i, (age, sex, gen, arrival, hispanic) in enumerate(zip(data["age"], data["sex"], data["generation"],
                                                            data["arrival"], data["hispanic"], strict=True)):
        # Public-use ages lack birthdays. Use March15 (the case's frame date) and uniform birthdays.
        # Negative ages mean later births, whose Census omission correction is zero.
        options = [(age - 5, 1 - BIRTH_OLDER_SHARE), (age - 4, BIRTH_OLDER_SHARE)]
        if birth_arm == "all_younger":
            options = [(age - 5, 1.0)]
        elif birth_arm == "all_older":
            options = [(age - 4, 1.0)]
        prearrival = 1.0
        if gen == 0:
            # Code27 combines 2020-21; Jan-Mar2020 is 3/24 under uniform arrival months.
            prearrival = 1.0 if arrival <= 26 else 1 / 8 if arrival == 27 else 0.0
            if arrival_arm == "none_27" and arrival == 27:
                prearrival = 0.0
            elif arrival_arm == "all_27" and arrival == 27:
                prearrival = 1.0
            elif arrival_arm == "post_rate":
                prearrival = 1.0
        for old_age, fraction in options:
            if old_age < 0:
                continue
            if hispanic:
                if mode == "proportional":
                    nce = rates["hispanic"]["all"]["nce_pct"] / 100
                    r = 1 / ((1 + nce) * base[(0, 100)]["base_over_census"]) - 1
                else:
                    r = rate_at(int(old_age), int(sex), rates, base, mode, se_shift)
                f[i] += fraction * prearrival * r
            if mode == "added_white":
                r = 1 / (1 + rates["nonhispanic_white"]["all"]["nce_pct"] / 100) - 1
                added_f[i] += fraction * r
    require(np.isfinite(f).all() and np.isfinite(added_f).all(), "non-finite coverage factors")
    return f, added_f


def sdr(estimates):
    require(estimates.shape == (161,), "replicate estimate shape")
    return float(np.sqrt((4 / 160) * np.square(estimates[1:] - estimates[0]).sum()))


def evaluate(data, f, af, proportional=False):
    out, parts, people = [], {}, {}
    weights, added = data["weights"], data["added_weights"]
    for g_i, gen in enumerate(GENS):
        m = data["generation"] == g_i
        people[gen] = float((weights[m, 0] * f[m]).sum())
    people["added"] = float((added[:, 0] * af).sum())
    for end_i, end in enumerate(ENDS):
        row, total = {}, np.zeros(161)
        for g_i, gen in enumerate(GENS):
            m = data["generation"] == g_i
            prices = data["net_id"][end_i, m]
            if proportional:
                average = (prices * weights[m]).sum(axis=0) / weights[m].sum(axis=0)
                est = average * (weights[m] * f[m, None]).sum(axis=0)
            else:
                est = (prices * weights[m] * f[m, None]).sum(axis=0)
            total += est
            row[gen] = {"coverage_bn": float(est[0]), "cps_replicate_se_bn": sdr(est)}
        ad = (data["net_added"][end_i] * added * af[:, None]).sum(axis=0)
        total += ad
        row["added"] = {"coverage_bn": float(ad[0]), "cps_replicate_se_bn": sdr(ad)}
        require(abs(sum(x["coverage_bn"] for x in row.values()) - total[0]) < TOL, "coverage generation closure")
        out.append(total)
        parts[end] = row
    return out, parts, people


def denominator_arm(data, f, central):
    """Add positive omissions to the consumer's actual national driver masses."""
    audit = json.loads((LANE / "derived/pricing_audit.json").read_text())
    shifts = {e: 0.0 for e in ENDS}
    covered, held = {e: 0.0 for e in ENDS}, {e: 0.0 for e in ENDS}
    diagnostics = []
    # The arm adds omissions to denominators while retaining overcounts, as requested.
    # Central numerators still contain the signed net correction, including negative cells.
    delta_weight = data["weights"][:, 0] * np.maximum(f, 0)
    numerator_delta_weight = data["weights"][:, 0] * f
    current_weight = data["weights"][:, 0] + data["added_weights"][:, 0]
    for i, piece in enumerate(audit["denominator_pieces"]):
        amount = float(data["base_piece_prices"][i] @ current_weight)
        addition = float(data["base_piece_prices"][i] @ numerator_delta_weight)
        end = piece["end"]
        require(piece["denominator_scope"] == "actual_declared_driver", "unpriced national denominator piece")
        dilution = float(data["national_vectors"][i] @ delta_weight) / data["national_masses"][i]
        require(math.isfinite(dilution) and 1 + dilution > 0, "invalid added national denominator")
        require(dilution >= 0, "denominator arm removes overcounts")
        shifts[end] += (amount + addition) / (1 + dilution) - (amount + addition)
        covered[end] += abs(amount)
        diagnostics.append({"piece": i, "end": end, "generation": piece["generation"], "line": piece["line"],
                            "category": piece["category"], "national_mass": float(data["national_masses"][i]),
                            "positive_omission_mass": float(data["national_vectors"][i] @ delta_weight),
                            "national_dilution": float(dilution), "base_piece_bn": amount,
                            "signed_numerator_addition_bn": addition,
                            "change_from_fixed_mass_bn": float((amount + addition) / (1 + dilution) - (amount + addition))})
    with (LANE / "derived/denominators.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=diagnostics[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(diagnostics)
    return {e: {"coverage_bn": float(central[i][0]) + float(shifts[e]), "change_from_central_bn": float(shifts[e]),
                "scope": "actual declared consumer driver masses, with coefficients/responses fixed; not an engine rerun",
                "gross_piece_bn_with_parent": covered[e], "gross_piece_bn_held": held[e]} for i, e in enumerate(ENDS)}


def validate_cache_receipt(audit):
    for field, filename in (("adapter_sha256", "export_pricing.py"), ("national_keys_sha256", "national_keys.py")):
        require(audit.get(field) == hashlib.sha256((LANE / filename).read_bytes()).hexdigest(),
                "stale pricing adapter " + filename + "; rerun export_pricing.py")
    require(audit.get("dependency_manifest_sha256") == hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
            "stale pricing input manifest; rerun export_pricing.py")
    with (LANE / "_cache/pricing.npz").open("rb") as stream:
        cache_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    require(audit.get("pricing_cache_sha256") == cache_hash, "stale or corrupt pricing cache")


def main():
    start = time.perf_counter()
    verify_local_pins()
    summary = json.loads(SUMMARY.read_text())
    with GEN.open() as stream:
        generations = validate_generation_rows(list(csv.DictReader(stream)), summary)
    meta = json.loads((ROOT / "infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct14/lines.json").read_text())["meta"]
    validate_metadata(meta)
    rates, base = load()
    validate_manifest()
    audit = json.loads((LANE / "derived/pricing_audit.json").read_text())
    validate_cache_receipt(audit)
    with np.load(LANE / "_cache/pricing.npz") as cache:
        data = {k: cache[k] for k in cache.files}
    require(np.isfinite(data["net_id"]).all() and np.isfinite(data["net_added"]).all(), "non-finite person prices")
    require(np.isfinite(data["weights"]).all() and (data["weights"][:, 0] > 0).all(), "non-positive person populations")
    require(np.isfinite(data["added_weights"]).all() and (data["added_weights"] >= -1e-8).all(), "invalid added populations")
    for i, end in enumerate(ENDS):
        total = (data["net_id"][i] * data["weights"] + data["net_added"][i] * data["added_weights"]).sum(axis=0)
        require(np.max(np.abs(total - summary["main_case"][i])) < TOL, "cached pricing case/replicate closure")
    legacy = json.loads((LANE / "inputs/legacy.json").read_text())
    factor = 1 / (1 + rates["hispanic"]["all"]["nce_pct"] / 100) - 1
    old = {}
    for i, end in enumerate(ENDS):
        got = factor * sum(float(generations[(end, g)]["cost_bn"]) for g in ("G2", "G3plus"))
        require(abs(got - legacy["ends"][end]["bound_bn"]) < TOL, "legacy positive control failed")
        old[end] = {"coverage_bn": got, "case_with_coverage_bn": summary["main_case"][i] + got}
    definitions = {
        "central": {}, "pes_only": {"mode": "pes_only"},
        "da_low": {"mode": "da_low"}, "da_middle": {"mode": "da_middle"}, "da_high": {"mode": "da_high"},
        "pes_nce_minus_1se": {"se_shift": -1}, "pes_nce_plus_1se": {"se_shift": 1},
        "proportional_pricing": {},
        "age_priced_all_age_rate": {"mode": "proportional"}, "proportional": {"mode": "proportional"},
        "post_arrival_rate": {"arrival_arm": "post_rate"}, "arrival27_none_pre2020": {"arrival_arm": "none_27"},
        "arrival27_all_pre2020": {"arrival_arm": "all_27"}, "added_white": {"mode": "added_white"},
        "birthday_younger": {"birth_arm": "all_younger"}, "birthday_older": {"birth_arm": "all_older"}}
    scenarios, rows = {}, []
    for name, options in definitions.items():
        f, af = factors(data, rates, base, **options)
        estimates, parts, people = evaluate(data, f, af, proportional=name in ("proportional", "proportional_pricing"))
        scenarios[name] = {"ends": {}, "parts": parts, "implied_net_missing_people": people}
        for i, end in enumerate(ENDS):
            value = float(estimates[i][0])
            scenarios[name]["ends"][end] = {"coverage_bn": value,
                "case_with_coverage_bn": summary["main_case"][i] + value, "cps_replicate_se_bn": sdr(estimates[i])}
            for g, part in parts[end].items():
                rows.append({"scenario": name, "end": end, "allocation": "personal", "specification": [16, 11][i],
                             "generation": g, **part, "implied_net_missing_people": people[g]})
        if name == "central":
            central_estimates, central_f = estimates, f
    central_ends = scenarios["central"]["ends"]
    for scenario in scenarios.values():
        for end, entry in scenario["ends"].items():
            change = entry["coverage_bn"] - central_ends[end]["coverage_bn"]
            entry["change_from_central_bn"] = change
            entry["over_5bn_from_central"] = abs(change) >= 5
    denom = denominator_arm(data, central_f, central_estimates)
    for i, e in enumerate(ENDS):
        denom[e]["case_with_coverage_bn"] = summary["main_case"][i] + denom[e]["coverage_bn"]
        denom[e]["over_5bn_from_central"] = abs(denom[e]["change_from_central_bn"]) >= 5
    envelope = ("da_low", "da_high", "pes_nce_minus_1se", "pes_nce_plus_1se", "proportional",
                "proportional_pricing", "age_priced_all_age_rate", "pes_only")
    output = {"key": "oct14", "case": "main_case_2026_10_14", "allocation": "personal", "specifications": [16, 11],
        "ends": central_ends, "legacy_positive_control": old, "scenarios": scenarios, "denominator_arm": denom,
        "range_bn": {e: [min(scenarios[n]["ends"][e]["coverage_bn"] for n in envelope),
                         max(scenarios[n]["ends"][e]["coverage_bn"] for n in envelope)] for e in ENDS},
        "range_label": "construction sensitivity envelope, not confidence interval or bound",
        "gates": {"legacy_reproduction_1e_6bn": True, "pricing_every_replicate_1e_6bn": True,
                  "coverage_generation_closure_1e_6bn": True, "finite_positive_inputs": True, "metadata": True},
        "fixed": ["national budgets and key masses in central", "case per-member prices and responses"],
        "limitations": ["PES household-to-resident and Hispanic-to-Mexican-origin transfer assumptions",
            "birth/arrival dates inside public-use bands modelled; missed-member survival/emigration unobserved",
            "within-G3+ pricing proxy and per-head calibration separate exact net totals",
            "denominator arm holds composite receipt coefficients and case responses fixed; not an engine rerun",
            "CPS replicate SE excludes PES covariance, DA series range and transfer uncertainty"]}
    output["population_basis"] = {"identified_union": float(data["weights"][:, 0].sum()),
                                  "added_nonhispanic": float(data["added_weights"][:, 0].sum()),
                                  "lineage": float(data["weights"][:, 0].sum() + data["added_weights"][:, 0].sum())}
    output["hispanic_reporting_population"] = {g: float(data["weights"][data["generation"] == i, 0]
        @ data["hispanic"][data["generation"] == i]) for i, g in enumerate(GENS)}
    encoded = json.dumps(output, indent=2, allow_nan=False) + "\n"
    with (LANE / "derived/coverage_bound.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (LANE / "derived/coverage_bound.json").write_text(encoded)
    for e in ENDS:
        p = central_ends[e]
        print(f"{e}: coverage {p['coverage_bn']:+.3f}bn; case {p['case_with_coverage_bn']:.3f}bn; CPS SE {p['cps_replicate_se_bn']:.3f}bn; range {output['range_bn'][e]}")
    print(f"PASS; elapsed {time.perf_counter()-start:.3f}s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f}MB")


if __name__ == "__main__":
    main()

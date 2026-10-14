"""Price all preserved coverage constructions on explicit, frozen oct15 BASE inputs.

The live case later consumes this result. Reproduction never feeds coverage-on
generation costs back into coverage prices. --freeze-base is explicit discovery.
"""
import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import coverage_bound as C
from dependency_manifest import validate_manifest
from export_pricing import validate_metadata
from source_tables import load

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from memory_budget import require_within_budget

LANE, ROOT, ENDS, GENS = C.LANE, C.ROOT, C.ENDS, C.GENS
BASE = LANE / "inputs/oct15_base"
CASE = ROOT / "infra/immigration-fiscal/main_case_2026_10_15/derived"
GEN = ROOT / "infra/immigration-fiscal/generation_account_2026_09_24/derived"
HOUSE = ROOT / "infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct15"
DEFINITIONS, ENVELOPE = C.DEFINITIONS, C.ENVELOPE


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def validate_generations(rows, full, summary, basis):
    C.require(full["case"] == {"set": "oct15", "cash": "oct15_cash"}[basis]
              and full["set"] == basis, "generation base case/set identity")
    targets = summary["v8"]["band_bn" if basis == "set" else "cash_set_bn"]
    specs = summary["v8"]["end_specifications"][basis]
    C.require(specs == [[16, 11], [16, 11]], "oct15 base specifications")
    C.require(abs(sum(full["conventions"]["a"][g]["population"] for g in GENS)
                  - summary["v8"]["population"]["without_coverage"]) < 1e-6,
              "full precision generation base population closure")
    # Retain the CSV shape/finite/allocation guard at its existing rounding tolerance.
    chosen = C.validate_generation_rows(rows, {"v7": {"end_specifications": {"set": [16, 11]}},
                                              "main_case": targets})
    for i, end in enumerate(ENDS):
        C.require(abs(sum(full["conventions"]["a"][g]["cost_bn"][i] for g in GENS) - targets[i]) < 1e-9,
                  "full precision generation base closure")
        for g in GENS:
            exact = full["conventions"]["a"][g]
            C.require(abs(float(chosen[end, g]["cost_bn"]) - exact["cost_bn"][i]) < 1e-6,
                      "generation CSV/full precision cost mismatch")
            C.require(abs(float(chosen[end, g]["population"]) - exact["population"]) < 1e-6,
                      "generation CSV/full precision population mismatch")
    return targets


def same_numeric(old, new):
    """Structured identity with a 1e-12 roundoff ceiling on floating dollar fields."""
    if type(old) is not type(new):
        return False
    if isinstance(old, dict):
        return old.keys() == new.keys() and all(same_numeric(v, new[k]) for k, v in old.items())
    if isinstance(old, list):
        return len(old) == len(new) and all(same_numeric(a, b) for a, b in zip(old, new, strict=True))
    if isinstance(old, float):
        return np.isfinite(old) and np.isfinite(new) and abs(old-new) <= 1e-12
    return old == new


def validate_base_revision(snapshots):
    """Accept provenance/category additions only after exact principal numeric identity."""
    for basis in ("set", "cash"):
        suffix = "" if basis == "set" else "_cash"
        old_payload = json.loads((BASE / f"corrections{suffix}.json").read_text())
        new_payload = json.loads(snapshots[f"corrections{suffix}.json"])
        C.require(same_numeric({k: v for k, v in old_payload.items() if k != "meta"},
                  {k: v for k, v in new_payload.items() if k != "meta"}),
                  "BASE revision changes engine edits or pricing declarations")
        for key in ("responses", "capital_return", "production", "pension_accrual", "state_pricing",
                    "roads_mileage_key", "retiree_health", "user_fees", "allocation"):
            C.require(same_numeric(old_payload["meta"].get(key), new_payload["meta"].get(key)),
                      "BASE revision changes pricing metadata " + key)
        old_gen = json.loads((BASE / f"generation_summary{suffix}.json").read_text())
        new_gen = json.loads(snapshots[f"generation_summary{suffix}.json"])
        for generation in GENS:
            for key, value in old_gen["conventions"]["a"][generation].items():
                C.require(same_numeric(new_gen["conventions"]["a"][generation].get(key), value),
                          "BASE revision changes convention-a generation " + generation + ":" + key)
        with (BASE / f"generation_results{suffix}.csv").open() as stream:
            old_rows = [r for r in csv.DictReader(stream) if r["convention"] == "a"]
        new_rows = [r for r in csv.DictReader(snapshots[f"generation_results{suffix}.csv"].decode().splitlines())
                    if r["convention"] == "a"]
        C.require(len(old_rows) == len(new_rows), "BASE revision changes generation CSV shape")
        for old, new in zip(old_rows, new_rows, strict=True):
            C.require(all(new.get(k) == v for k, v in old.items()), "BASE revision changes convention-a CSV values")
        old_lines = json.loads((BASE / f"lines{suffix}.json").read_text())
        new_lines = json.loads(snapshots[f"lines{suffix}.json"])
        C.require(same_numeric({k: v for k, v in old_lines.items() if k != "meta"},
                  {k: v for k, v in new_lines.items() if k != "meta"}),
                  "BASE revision changes household numeric price declarations")
        old_records = old_lines["meta"]["child_pricing"]["records"]
        new_records = new_lines["meta"]["child_pricing"]["records"]
        C.require(len(old_records) == len(new_records), "BASE revision changes native child frame")
        def original_record(record):
            copy = json.loads(json.dumps(record))
            for block in copy["ends"].values():
                for row in block["rows"]:
                    row.pop("category_cost_bn", None)
            return copy
        C.require(same_numeric([original_record(r) for r in old_records], [original_record(r) for r in new_records]),
                  "BASE revision changes principal own-age child prices")
    old_summary, new_summary = json.loads((BASE / "summary.json").read_text()), json.loads(snapshots["summary.json"])
    for key in ("band_bn", "cash_set_bn", "population", "end_specifications"):
        C.require(same_numeric(old_summary["v8"][key], new_summary["v8"][key]), "BASE revision changes case " + key)
    old_added, new_added = json.loads((BASE / "lineage_addition.json").read_text()), json.loads(snapshots["lineage_addition.json"])
    for basis in ("set", "cash"):
        C.require(same_numeric(old_added["v8"][basis]["all_nonreporting_descendants"]["cost_bn"],
                  new_added["v8"][basis]["all_nonreporting_descendants"]["cost_bn"]),
                  "BASE revision changes exact added price targets")


def freeze_base(refresh_lines=False, refresh_provenance=False):
    refresh = refresh_lines or refresh_provenance
    prior = validate_frozen() if refresh else None
    C.require(refresh or not (BASE / "manifest.json").exists(), "base already frozen; do not overwrite evidence")
    sources = {"summary.json": CASE / "summary.json", "lineage_addition.json": CASE / "lineage_addition.json"}
    for basis in ("set", "cash"):
        suffix = "" if basis == "set" else "_cash"
        sources[f"corrections{suffix}.json"] = CASE / f"corrections{suffix}.json"
        sources[f"generation_results{suffix}.csv"] = GEN / f"generation_results_oct15{suffix}.csv"
        sources[f"generation_summary{suffix}.json"] = GEN / f"generation_summary_oct15{suffix}.json"
        sources[f"lines{suffix}.json"] = HOUSE / f"lines{suffix}.json"
    for name, path in sources.items():
        C.require(path.is_file(), "missing oct15 BASE input " + str(path.relative_to(ROOT)))
    snapshots = {name: path.read_bytes() for name, path in sources.items()}
    if refresh_provenance:
        validate_base_revision(snapshots)
    if refresh_lines:
        prior_files = {r["name"]: r for r in prior["files"]}
        for name, data in snapshots.items():
            if name not in ("lines.json", "lines_cash.json"):
                C.require(hashlib.sha256(data).hexdigest() == prior_files[name]["sha256"],
                          "base changed during line refresh: " + name)
    summary = json.loads(snapshots["summary.json"])
    C.require(summary["v8"]["population"]["coverage"] == 0, "coverage-on case cannot become base")
    for basis in ("set", "cash"):
        suffix = "" if basis == "set" else "_cash"
        payload = json.loads(snapshots[f"corrections{suffix}.json"])
        C.require(payload["meta"].get("coverage") is None, "coverage payload is not a BASE")
        rows = list(csv.DictReader(snapshots[f"generation_results{suffix}.csv"].decode().splitlines()))
        targets = validate_generations(rows, json.loads(snapshots[f"generation_summary{suffix}.json"]), summary, basis)
        lines = json.loads(snapshots[f"lines{suffix}.json"])
        validate_metadata(lines["meta"], "oct15")
        C.require(lines["meta"]["basis"] == basis, "household pricing set identity")
        gen_summary = json.loads(snapshots[f"generation_summary{suffix}.json"])
        C.require(lines["meta"].get("population_rounding") == gen_summary.get("population_rounding")
                  and lines["meta"].get("population_rounding", {}).get("generation") == "G1",
                  "household/base principal population rounding identity")
        exact_added = json.loads(snapshots["lineage_addition.json"])["v8"][basis]["all_nonreporting_descendants"]["cost_bn"]
        for i, end in enumerate(ENDS):
            C.require(abs(lines["meta"]["coverage_added_cost_bn"][end] - exact_added[i]) < 1e-9,
                      "household/base exact added cost identity")
            C.require(abs(lines["union"][end]["cost_bn"] - targets[i]) < 1e-9, "household/base case closure")
            C.require(abs(sum(lines["generations"][g][end]["cost_bn"] for g in GENS) - targets[i]) < 1e-9,
                      "household/base generation closure")
    BASE.mkdir(parents=True, exist_ok=True)
    if refresh:
        archive = BASE / ("superseded_" + digest(BASE / "manifest.json")[:16])
        C.require(not archive.exists(), "this base line revision already preserved; do not overwrite evidence")
        archive.mkdir()
        for name in (("manifest.json", *sources) if refresh_provenance else ("manifest.json", "lines.json", "lines_cash.json")):
            (archive / name).write_bytes((BASE / name).read_bytes())
    files = []
    for name, source in sources.items():
        data = snapshots[name]
        (BASE / name).write_bytes(data)
        files.append({"name": name, "source": str(source.relative_to(ROOT)), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()})
    (BASE / "manifest.json").write_text(json.dumps({"key": "oct15", "coverage": "off", "files": files}, indent=2) + "\n")
    print("oct15 BASE frozen; case/generation/household set and cash gates PASS")


def validate_frozen():
    C.require((BASE / "manifest.json").exists(), "missing frozen oct15 BASE; run --freeze-base")
    receipt = json.loads((BASE / "manifest.json").read_text())
    C.require(receipt.get("key") == "oct15" and receipt.get("coverage") == "off", "frozen base identity")
    names = [x["name"] for x in receipt["files"]]
    expected = {"summary.json", "lineage_addition.json"} | {f"{name}{s}.{ext}" for s in ("", "_cash")
                                 for name, ext in (("corrections", "json"), ("generation_results", "csv"),
                                                   ("generation_summary", "json"), ("lines", "json"))}
    C.require(set(names) == expected and len(names) == len(expected), "frozen base receipt file coverage")
    for entry in receipt["files"]:
        path = BASE / entry["name"]
        C.require(path.is_file() and path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"],
                  "stale frozen oct15 BASE " + entry["name"])
    return receipt


def missing_age_bands(data, f, af):
    result = {}
    for label, weights, factors in [(g, data["weights"][:, 0] * (data["generation"] == i), f)
                                    for i, g in enumerate(GENS)] + [("added", data["added_weights"][:, 0], af)]:
        result[label] = {f"{lo}-{lo+4}" if lo < 80 else "80+": float((weights * factors)[
            (data["age"] >= lo) & ((data["age"] < lo+5) if lo < 80 else True)].sum()) for lo in range(0, 81, 5)}
    return result


def missing_age_prices(data, f, af, parts, proportional=False):
    result = {}
    for label, weights, factors, prices in [(g, data["weights"][:, 0] * (data["generation"] == i), f, data["net_id"])
                                            for i, g in enumerate(GENS)] + [("added", data["added_weights"][:, 0], af, data["net_added"])]:
        result[label] = {}
        for lo in range(0, 81, 5):
            band = f"{lo}-{lo+4}" if lo < 80 else "80+"
            m = (data["age"] >= lo) & ((data["age"] < lo+5) if lo < 80 else True)
            masses = weights[m] * factors[m]
            count = float(masses.sum())
            entry = {"net_missing_people": count, "by_end": {}}
            for i, end in enumerate(ENDS):
                if proportional and label != "added":
                    average = float(prices[i, :, 0] @ weights / weights.sum())
                    cost = average * count
                else:
                    cost = float((prices[i, m, 0] * masses).sum())
                entry["by_end"][end] = {"coverage_bn": cost, "per_member_usd": cost*1e9/count if count else None}
            result[label][band] = entry
        for end in ENDS:
            C.require(abs(sum(v["by_end"][end]["coverage_bn"] for v in result[label].values())
                          - parts[end][label]["coverage_bn"]) < 1e-9, "missing-person age-price closure")
    return result


def decompose(data, f, af, audit, end, target, basis, production_split):
    identified, added = data["weights"][:, 0] * f, data["added_weights"][:, 0] * af
    mass = identified + added
    capital = {"federal": 0.0, "state_local": 0.0}
    P, F, fiscal, unclassified = 0.0, 0.0, 0.0, 0.0
    rows = []
    for i, piece in enumerate(audit["denominator_pieces"]):
        if piece["end"] != end:
            continue
        cost = float(data["base_piece_prices"][i] @ mass)
        kind = piece["economic_class"]
        row = {k: piece[k] for k in ("generation", "line", "source_line", "source_side", "category", "level", "economic_class")}
        row["coverage_bn"] = cost
        if kind == "capital_return":
            C.require(piece["level"] in capital, "unknown coverage public-capital level")
            capital[piece["level"]] += cost
        elif kind == "production":
            if production_split == "generation_ratio":
                p = piece["source_production"]
                denominator = p["cost_bn"]
                C.require(abs(denominator) > 1e-12 or cost == 0, "production generation ratio undefined")
                private = cost*p["private_wtp_bn"]/denominator if denominator else 0.0
                induced = cost*p["fiscal_weight"]*p["induced_receipts_bn"]/denominator if denominator else 0.0
                C.require(abs(cost+private+induced) < 1e-9, "signed production P/F closure")
                P += private
                F += induced
                row.update(P_bn=private, F_bn=induced)
            else:
                unclassified += cost
        elif kind == "fiscal_line":
            fiscal += cost
        else:
            C.require(kind == "unclassified_post_engine", "unknown coverage component class")
            unclassified += cost
        rows.append(row)
    for i, piece in enumerate(audit["other_pieces"]):
        if piece["end"] != end:
            continue
        m = {"both": mass, "identified": identified, "added": added}[piece["population"]]
        cost = float(data["other_piece_prices"][i] @ m)
        unclassified += cost
        rows.append({**piece, "economic_class": "unclassified_residual", "level": "unclassified", "coverage_bn": cost})
    closed = sum(capital.values()) + fiscal + unclassified - P - F
    C.require(abs(closed-target) < 1e-9, "coverage economic decomposition closure")
    result = {"capital_by_level_bn": capital,
              "production": {"P_bn": P, "F_bn": F, "allocation_rule": production_split,
                 "approximation": production_split == "generation_ratio",
                 "scope": "generation-end P/F ratio on that generation's existing earnings-key price pieces"},
              "unclassified_bn": unclassified, "classified_fiscal_line_bn": fiscal,
              "classified_fiscal_with_production_F_bn": fiscal-F, "total_cost_bn": closed,
              "line_parts": rows,
              "sign_convention": "capital, fiscal lines and unclassified are net costs; P and F are signed welfare/receipt gains; total = capital + fiscal lines + unclassified - P - F",
              "borrowing_rule": "capital return and private P are not borrowing; unclassified residual/calibration/post-engine amounts require the consumer's declared financing rule"}
    if basis == "cash":
        result["classified_cash_fiscal_bn"] = fiscal-F
    return result


def calculate(basis, summary, rates, base, production_split="generation_ratio"):
    suffix = "" if basis == "set" else "_cash"
    with (BASE / f"generation_results{suffix}.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    targets = validate_generations(rows, json.loads((BASE / f"generation_summary{suffix}.json").read_text()), summary, basis)
    lines = json.loads((BASE / f"lines{suffix}.json").read_text())
    validate_metadata(lines["meta"], "oct15")
    manifest = LANE / f"inputs/pricing_dependencies_oct15_{basis}.json"
    validate_manifest(manifest, f"coverage oct15 personal flat pricing {basis}")
    audit_path = LANE / f"derived/pricing_audit_oct15_{basis}.json"
    audit = json.loads(audit_path.read_text())
    C.require(audit["case"] == "oct15" and audit["basis"] == basis, "pricing audit case/set identity")
    C.require(audit["gates"].get("physical_footprint_within_2_5GB") is True, "pricing process did not pass physical-footprint gate")
    cache_path = LANE / f"_cache/oct15/{basis}/pricing.npz"
    C.validate_cache_receipt(audit, manifest, cache_path)
    with np.load(cache_path) as cache:
        data = {k: cache[k] for k in cache.files}
    C.require(np.isfinite(data["net_id"]).all() and np.isfinite(data["net_added"]).all(), "nonfinite oct15 person prices")
    C.require(np.isfinite(data["weights"]).all() and np.all(data["weights"] >= -1e-8), "invalid identified populations")
    C.require(np.isfinite(data["added_weights"]).all() and np.all(data["added_weights"] >= -1e-8), "invalid added populations")
    for i, end in enumerate(ENDS):
        total = (data["net_id"][i] * data["weights"] + data["net_added"][i] * data["added_weights"]).sum(axis=0)
        C.require(np.max(np.abs(total - targets[i])) < 1e-6, "cached oct15 every-replicate closure")
        for j, g in enumerate(GENS):
            mask = data["generation"] == j
            got = (data["net_id"][i, mask] * data["weights"][mask] + data["net_added"][i, mask] * data["added_weights"][mask]).sum(axis=0)
            C.require(np.max(np.abs(got - lines["generations"][g][end]["cost_bn"])) < 1e-6,
                      "cached oct15 generation every-replicate closure")
    scenarios = {}
    for name, options in DEFINITIONS.items():
        f, af = C.factors(data, rates, base, **options)
        estimates, parts, people = C.evaluate(data, f, af, proportional=name in ("proportional", "proportional_pricing"))
        age_bands = missing_age_bands(data, f, af)
        adults = {g: float((data["weights"][:, 0] * f)[(data["generation"] == j) & (data["age"] >= 18)].sum())
                  for j, g in enumerate(GENS)}
        adults["G3plus"] += float((data["added_weights"][:, 0] * af)[data["age"] >= 18].sum())
        for g, count in people.items():
            C.require(abs(sum(age_bands[g].values()) - count) < 1e-6, "coverage missing age/generation population closure")
        scenarios[name] = {"ends": {}, "parts": parts, "implied_net_missing_people": people,
                           "implied_net_missing_people_by_age_band": age_bands, "adults_by_generation": adults,
                           "by_generation_age_band": missing_age_prices(data, f, af, parts,
                               proportional=name in ("proportional", "proportional_pricing"))}
        for i, end in enumerate(ENDS):
            by_gen = {g: parts[end][g]["coverage_bn"] + (parts[end]["added"]["coverage_bn"] if g == "G3plus" else 0) for g in GENS}
            value = float(estimates[i][0])
            C.require(abs(sum(by_gen.values()) - value) < 1e-9, "coverage generation closure 1e-9")
            scenarios[name]["ends"][end] = {"coverage_bn": value, "total_bn": value, "by_generation": by_gen,
                "case_with_coverage_bn": targets[i] + value, "cps_replicate_se_bn": C.sdr(estimates[i])}
        if name == "central":
            C.require(people["added"] == 0 and all(parts[e]["added"]["coverage_bn"] == 0 for e in ENDS),
                      "added descendants must have zero central coverage")
            central_estimates, central_f = estimates, f
            for i, end in enumerate(ENDS):
                adult_cost, minor_cost = {}, {}
                for j, generation in enumerate(GENS):
                    for is_adult, destination in ((True, adult_cost), (False, minor_cost)):
                        mask = (data["generation"] == j) & ((data["age"] >= 18) == is_adult)
                        cost = float(data["net_id"][i, mask, 0] @ (data["weights"][mask, 0] * f[mask]))
                        if generation == "G3plus":
                            added_mask = (data["age"] >= 18) == is_adult
                            cost += float(data["net_added"][i, added_mask, 0] @ (data["added_weights"][added_mask, 0] * af[added_mask]))
                        destination[generation] = cost
                    C.require(abs(adult_cost[generation] + minor_cost[generation]
                                  - scenarios[name]["ends"][end]["by_generation"][generation]) < 1e-9,
                              "exact-age adult/minor coverage cost closure")
                scenarios[name]["ends"][end].update(adult_cost_by_generation_bn=adult_cost,
                    minor_cost_by_generation_bn=minor_cost,
                    adult_minor_uncertainty_rule="conditional CPS price/weight replication; missing-count assumptions are construction sensitivities, not observed counts or an estimated missing-count SE")
                scenarios[name]["ends"][end]["decomposition"] = decompose(data, f, af, audit, end,
                    float(estimates[i][0]), basis, production_split)
    central = scenarios["central"]
    for scenario in scenarios.values():
        for end, entry in scenario["ends"].items():
            change = entry["coverage_bn"] - central["ends"][end]["coverage_bn"]
            entry.update(change_from_central_bn=change, over_5bn_from_central=abs(change) >= 5)
    denom = C.denominator_arm(data, central_f, central_estimates, audit_path,
                             LANE / f"derived/denominators_oct15_{basis}.csv")
    for i, end in enumerate(ENDS):
        denom[end].update(case_with_coverage_bn=targets[i] + denom[end]["coverage_bn"],
                          over_5bn_from_central=abs(denom[end]["change_from_central_bn"]) >= 5)
    # Retain the original frozen-era positive control; the oct15 prices have no legacy target.
    pins = json.loads((LANE / "inputs/pins.json").read_text())
    C.require(digest(C.GEN) == pins["generation_results_original.csv"]["sha256"], "stale frozen legacy generation input")
    with C.GEN.open() as stream:
        old_rows = C.validate_generation_rows(list(csv.DictReader(stream)), json.loads(C.SUMMARY.read_text()))
    factor = 1/(1+rates["hispanic"]["all"]["nce_pct"]/100)-1
    legacy = json.loads((LANE / "inputs/legacy.json").read_text())
    old = {}
    for end in ENDS:
        got = factor * sum(float(old_rows[end, g]["cost_bn"]) for g in ("G2", "G3plus"))
        C.require(abs(got-legacy["ends"][end]["bound_bn"]) < 1e-6, "legacy positive control failed")
        old[end] = {"coverage_bn": got, "pricing_epoch": "original oct14"}
    return {"ends": central["ends"], "parts": central["parts"], "scenarios": scenarios,
            "implied_net_missing_people": central["implied_net_missing_people"],
            "implied_net_missing_people_by_age_band": central["implied_net_missing_people_by_age_band"],
            "adults_by_generation": central["adults_by_generation"],
            "by_generation_age_band": central["by_generation_age_band"],
            "denominator_arm": denom, "legacy_positive_control": old,
            "range_bn": {e: [min(scenarios[n]["ends"][e]["coverage_bn"] for n in ENVELOPE),
                               max(scenarios[n]["ends"][e]["coverage_bn"] for n in ENVELOPE)] for e in ENDS},
            "range_label": "construction sensitivity envelope, not confidence interval or bound",
            "population_basis": {"identified_union": float(data["weights"][:, 0].sum()) + audit["population_rounding"]["people"],
                "identified_union_observed_weights": float(data["weights"][:, 0].sum()),
                "added_nonhispanic": float(data["added_weights"][:, 0].sum()),
                "lineage": float(data["weights"][:, 0].sum()+data["added_weights"][:, 0].sum()) + audit["population_rounding"]["people"],
                "zero_cost_population_rounding": audit["population_rounding"],
                "rounding_rule": "principal source count reconciliation; zero dollars, no assigned age or coverage exposure"},
            "hispanic_reporting_population": {g: float(data["weights"][data["generation"] == i, 0]
                    @ data["hispanic"][data["generation"] == i]) for i,g in enumerate(GENS)},
            "gates": {"full_precision_base_1e_9bn": True, "pricing_every_replicate_1e_6bn": True,
                "coverage_generation_closure_1e_9bn": True, "added_central_zero": True,
                "source_pins": True, "actual_dependency_manifest": True, "cache_digest": True},
            "cash_rule": "own cash-set person prices" if basis == "cash" else "own accrual-set person prices"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-base", action="store_true")
    parser.add_argument("--refresh-base-lines", action="store_true")
    parser.add_argument("--refresh-base-provenance", action="store_true")
    parser.add_argument("--production-split", choices=["generation_ratio", "unclassified"], default="generation_ratio")
    args = parser.parse_args()
    C.require(sum((args.freeze_base, args.refresh_base_lines, args.refresh_base_provenance)) <= 1,
              "choose one explicit base operation")
    if args.freeze_base or args.refresh_base_lines or args.refresh_base_provenance:
        freeze_base(args.refresh_base_lines, args.refresh_base_provenance)
        return
    start = time.perf_counter()
    validate_frozen()
    summary = json.loads((BASE / "summary.json").read_text())
    rates, base = load()
    sets = {basis: calculate(basis, summary, rates, base, args.production_split) for basis in ("set", "cash")}
    hashes = {basis: digest(BASE / ("corrections.json" if basis == "set" else "corrections_cash.json"))
              for basis in ("set", "cash")}
    output = {"key": "oct15", "case": "main_case_2026_10_15", "allocation": "personal",
              "specifications": [16, 11], "base_payload_sha256": hashes["set"],
              "base_payload_sha256_by_set": hashes, "sets": sets,
              "production_split": args.production_split,
              "fixed": ["national budgets and key masses in central", "base case per-member prices and responses"],
              "limitations": json.loads((LANE / "derived/coverage_bound.json").read_text())["limitations"]}
    footprint = require_within_budget("oct15 coverage constructions")
    encoded = json.dumps(output, indent=2, allow_nan=False) + "\n"
    destination = LANE / "derived/coverage_bound_oct15.json"
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(encoded)
    temporary.replace(destination)  # publish only after both sets and every guard pass
    for basis, result in sets.items():
        print(basis, {end: result["ends"][end]["coverage_bn"] for end in ENDS})
    print(f"COVERAGE OCT15 WRITTEN; elapsed {time.perf_counter()-start:.3f}s; peak physical footprint {footprint/1e6:.1f}MB")


if __name__ == "__main__":
    main()

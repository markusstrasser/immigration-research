"""Separate final-routing price replay and the required <=0.5bn coverage check."""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import coverage_bound as C
from coverage_oct15 import BASE, digest, validate_frozen
from dependency_manifest import validate_manifest
from source_tables import load

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from memory_budget import require_within_budget

LANE, ROOT = C.LANE, C.ROOT
FINAL = LANE / "inputs/oct15_final_routing"
HOUSE = ROOT / "infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct15"


def adoption_receipt(marker):
    C.require(marker is not None and marker.is_file(), "phase2 requires actual CASE_FINAL adoption marker")
    text = marker.read_text()
    match = re.match(r"CASE_FINAL: main case v8 \(key oct15\) adopted at commit ([0-9a-f]{7,40})\b", text)
    C.require(match is not None, "CASE_FINAL is absent, a template, or not an oct15 adoption")
    resolved = subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), "rev-parse", "--verify",
                               match.group(1)+"^{commit}"], capture_output=True, text=True, check=False)
    C.require(resolved.returncode == 0, "CASE_FINAL adoption commit does not resolve")
    return {"source": str(marker.resolve()), "commit": resolved.stdout.strip(),
            "bytes": marker.stat().st_size, "sha256": digest(marker)}


def validate_observed_target_revision(previous, current, basis, coverage):
    """Allow only the principal coverage exclusion from the observed G3 target."""
    old = previous["meta"]["lineage"]["generation_g3plus"]
    lineage = current["meta"]["lineage"]
    revised = lineage["generation_g3plus"]
    excluded = revised.get("coverage_excluded", {})
    central = coverage["sets"][basis]["scenarios"]["central"]
    C.require(lineage.get("complete_generation_g3plus") == old,
              "final refresh changed the complete generation target")
    for field, expected in (("population", central["implied_net_missing_people"]["G3plus"]),
                            ("adults", central["adults_by_generation"]["G3plus"])):
        C.require(abs(excluded.get(field, float("inf"))-expected) < 1e-6
                  and abs(revised[field]+expected-old[field]) < 1e-6,
                  "final observed target exclusion differs from principal coverage " + field)
    declared = current["meta"]["coverage"]
    C.require(excluded.get("file") == declared["file"] and excluded.get("sha256") == declared["sha256"],
              "final observed target has stale coverage receipt")
    normalized = copy.deepcopy(current)
    normalized["meta"]["lineage"]["generation_g3plus"] = old
    del normalized["meta"]["lineage"]["complete_generation_g3plus"]
    C.require(normalized == previous, "final refresh changed amounts or unrelated declarations")


def freeze_final_inputs(marker, refresh=False):
    adoption = adoption_receipt(marker)
    receipt_path = FINAL / "manifest.json"
    if refresh:
        validate_final_inputs()
    else:
        C.require(not receipt_path.exists(), "final-routing source already frozen")
    validate_frozen()
    files = {}
    blocks = {}
    for basis in ("set", "cash"):
        name = "lines_cash.json" if basis == "cash" else "lines.json"
        source = HOUSE / name
        block = json.loads(source.read_text())
        meta = block["meta"]
        coverage = meta.get("coverage")
        C.require(meta["case"] == "main_case_2026_10_15" and meta["basis"] == basis,
                  "final-routing household case/set identity")
        C.require(coverage and not coverage.get("stub"), "final routing requires actual coverage, never STUB")
        coverage_file = ROOT / "infra/immigration-fiscal" / coverage["file"]
        C.require(coverage_file.is_file() and digest(coverage_file) == coverage["sha256"], "stale final coverage source")
        if refresh:
            validate_observed_target_revision(json.loads((FINAL / name).read_text()), block, basis,
                                              json.loads(coverage_file.read_text()))
        blocks[name] = source.read_bytes()
        files[name] = {"bytes": source.stat().st_size, "sha256": digest(source),
                       "source": str(source.relative_to(ROOT))}
    if refresh:
        archived = FINAL / ("superseded_" + digest(receipt_path)[:16])
        C.require(not archived.exists(), "final-routing superseded receipt already archived")
        archived.mkdir()
        for name in ("manifest.json", "CASE_FINAL", "lines.json", "lines_cash.json"):
            (archived / name).write_bytes((FINAL / name).read_bytes())
    FINAL.mkdir(parents=True, exist_ok=True)
    for name in files:
        (FINAL / name).write_bytes(blocks[name])
    (FINAL / "CASE_FINAL").write_bytes(marker.read_bytes())
    (FINAL / "manifest.json").write_text(json.dumps({"vintage": "oct15_final_routing", "files": files,
                                                    "adoption": adoption}, indent=2)+"\n")
    print("final routing household snapshots frozen; actual coverage receipt PASS")


def validate_final_inputs():
    path = FINAL / "manifest.json"
    C.require(path.exists(), "missing final routing inputs; explicit --freeze-final required")
    receipt = json.loads(path.read_text())
    C.require(receipt.get("vintage") == "oct15_final_routing"
              and set(receipt["files"]) == {"lines.json", "lines_cash.json"}, "final routing receipt shape")
    marker = FINAL / "CASE_FINAL"
    C.require(marker.is_file() and marker.stat().st_size == receipt["adoption"]["bytes"]
              and digest(marker) == receipt["adoption"]["sha256"], "frozen final adoption marker changed")
    for name, row in receipt["files"].items():
        file = FINAL / name
        C.require(file.is_file() and file.stat().st_size == row["bytes"] and digest(file) == row["sha256"],
                  "stale frozen final routing source " + name)


def observed_snapshot(snapshot):
    """Remove only declared coverage residual after the original household gates run."""
    lines = snapshot["lines"]
    coverage = lines["meta"].get("coverage")
    C.require(coverage and not coverage.get("stub"), "final observed kernel requires real coverage metadata")
    state_reallocation = lines["meta"].get("coverage_added_state_reallocation_bn")
    source_cost = lines["meta"].get("coverage_added_source_cost_bn")
    C.require(isinstance(state_reallocation, dict) and isinstance(source_cost, dict),
              "final added-price calibration needs explicit principal source and state reallocation")
    original = json.loads((BASE / ("lines_cash.json" if lines["meta"]["basis"] == "cash" else "lines.json")).read_text())
    for end in C.ENDS:
        C.require(abs(source_cost[end]-original["meta"]["coverage_added_cost_bn"][end]) < 1e-9,
                  "final added-price source differs from frozen principal BASE")
        state_added = sum(part["cost_by_population"]["latent"] + part["cost_by_population"]["native"]
            for generation in C.GENS for part in lines["generations"][generation][end].get("added_state_prices", []))
        C.require(abs(state_added-state_reallocation[end]) < 1e-9,
                  "final added-state calibration declaration does not match active principal parts")
        C.require(abs(lines["meta"]["coverage_added_cost_bn"][end]-source_cost[end]-state_added) < 1e-9,
                  "final added calibration erases declared state allocation")
        declared = coverage["by_end"][end]
        removed = 0.0
        for generation in C.GENS:
            group = lines["generations"][generation][end]
            missing = group["post_engine"].get("coverage", 0.0)
            expected = declared.get("by_generation", declared.get("by_generation_bn"))[generation]
            C.require(abs(missing-expected) < 1e-9, "final generation coverage declaration mismatch")
            snapshot["residual"][end][generation] -= missing
            group["cost_bn"] -= missing
            group["sum_bn"] -= missing
            group["post_engine"]["coverage"] = 0.0
            removed += missing
        C.require(abs(removed-declared["total_bn"]) < 1e-9, "final observed coverage subtraction closure")
        lines["union"][end]["cost_bn"] -= removed
        lines["union"][end]["sum_bn"] -= removed
        lines["union"][end]["post_engine"]["coverage"] = 0.0


def compare_final_prices():
    start = time.perf_counter()
    validate_final_inputs()
    adopted = json.loads((LANE / "derived/coverage_bound_oct15.json").read_text())
    rates, base = load()
    result = {"vintage": "oct15_final_routing", "coverage_base_preserved": True,
              "threshold_bn": .5, "sets": {}, "minor_scale_rule": "convention-b minor-parent scaling has no convention-a coverage channel; final state/credit routing is measured separately"}
    for basis in ("set", "cash"):
        manifest = LANE / f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json"
        validate_manifest(manifest, f"coverage oct15_final_routing personal flat pricing {basis}")
        audit = json.loads((LANE / f"derived/pricing_audit_oct15_final_routing_{basis}.json").read_text())
        C.require(audit["case"] == "oct15" and audit["basis"] == basis
                  and audit.get("routing_vintage") == "oct15_final_routing"
                  and audit.get("coverage_on_observed_people") is False,
                  "final observed pricing provenance mismatch")
        C.require(audit["gates"].get("physical_footprint_within_2_5GB") is True, "final pricing physical gate failed")
        cache = LANE / f"_cache/oct15_final_routing/{basis}/pricing.npz"
        C.validate_cache_receipt(audit, manifest, cache)
        with np.load(cache, allow_pickle=False) as stored:
            data = {key: stored[key] for key in stored.files}
        original = LANE / f"_cache/oct15/{basis}/pricing.npz"
        old_audit = json.loads((LANE / f"derived/pricing_audit_oct15_{basis}.json").read_text())
        C.require(digest(original) == old_audit["pricing_cache_sha256"], "BASE pricing record changed")
        with np.load(original, allow_pickle=False) as stored:
            for key in ("weights", "added_weights", "generation", "age", "sex", "arrival", "hispanic",
                        "person_rows", "person_ph_seq", "person_pppos"):
                C.require(np.array_equal(data[key], stored[key]), "final routing changed BASE frame " + key)
        f, af = C.factors(data, rates, base)
        estimates, parts, people = C.evaluate(data, f, af)
        ends = {}
        for i, end in enumerate(C.ENDS):
            before = adopted["sets"][basis]["ends"][end]["coverage_bn"]
            after = float(estimates[i][0])
            ends[end] = {"base_coverage_bn": before, "final_routing_coverage_bn": after,
                         "repricing_delta_bn": after-before, "within_0_5bn": abs(after-before) <= .5}
        result["sets"][basis] = {"ends": ends, "parts": parts, "implied_net_missing_people": people}
        del data
    result["pass"] = all(e["within_0_5bn"] for s in result["sets"].values() for e in s["ends"].values())
    footprint = require_within_budget("final-routing coverage consistency")
    (LANE / "derived/coverage_final_routing_check.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({b: s["ends"] for b, s in result["sets"].items()}))
    C.require(result["pass"], "final routing changes coverage by more than 0.5bn; parent must stop")
    print(f"final routing coverage consistency PASS; elapsed {time.perf_counter()-start:.3f}s; physical {footprint/1e6:.1f}MB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-final", action="store_true")
    parser.add_argument("--refresh-final-observed-target", action="store_true")
    parser.add_argument("--case-final", type=Path)
    args = parser.parse_args()
    C.require(not (args.freeze_final and args.refresh_final_observed_target), "choose one final source operation")
    if args.freeze_final or args.refresh_final_observed_target:
        freeze_final_inputs(args.case_final, refresh=args.refresh_final_observed_target)
    else:
        C.require(args.case_final is None, "--case-final is the explicit freeze-only input")
        compare_final_prices()

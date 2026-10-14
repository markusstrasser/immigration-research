"""Reuse the case consumer's gated person-price construction without upstream writes.

Native-First: reuse households.py's AST through its piece-construction boundary.
This is a read-only adapter, not a second implementation of its fiscal keys.
The pinned upstream source and uniquely matched AST boundary both fail closed.
"""
import ast
import argparse
import cProfile
import csv
import gc
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pyarrow as pa
from national_keys import full_key
from dependency_manifest import guard
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from memory_budget import require_within_budget, peak_bytes

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
SOURCE = ROOT / "infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py"
PINS = LANE / "inputs/pins.json"


def require(ok, message):
    if not ok:
        raise SystemExit("[BLOCKED] " + message)


def verify_local_pins():
    pins = json.loads(PINS.read_text())
    for name, pin in pins.items():
        if name == "generation_results_original.csv":
            path = LANE / "inputs" / name
            require(path.exists(), "missing frozen generation input " + name)
            require(hashlib.sha256(path.read_bytes()).hexdigest() == pin["sha256"],
                    "stale frozen generation input " + name)
            continue
        if "repo_path" not in pin:
            continue
        path = ROOT / pin["repo_path"]
        require(path.exists(), "missing principal input " + pin["repo_path"])
        with path.open("rb") as stream:
            sha = hashlib.file_digest(stream, "sha256").hexdigest()
        require(sha == pin["sha256"], "stale principal input " + pin["repo_path"])


def construction(source=SOURCE, case="oct14", basis="set", lines_path=None):
    """Keep the original function prefix and return its locals before any writes."""
    spec = importlib.util.spec_from_file_location("coverage_households", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = ast.parse(source.read_text(), filename=str(source))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    require(len(functions) == 1, "household pricing has no unique main")
    fn = functions[0]
    expected = {"prod_parts", "vec", "rk", "sk", "medical", "edu", "v"}
    boundaries = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Delete)
                  and {x.id for x in n.targets if isinstance(x, ast.Name)} == expected]
    require(len(boundaries) == 1, "household piece boundary changed")
    fields = ["pieces", "residual", "d", "W", "w_id", "rows_u", "gens", "lines", "vec", "f_rec", "age", "lineage",
              "PA", "prod_parts", "pop", "pop_id", "civ"]
    if case == "oct15":
        fields += ["coverage_identified_weights", "coverage_added_weights", "original_gens", "reporter", "nonreporter",
                   "completion_jobs", "completion_pension", "completion_national_mass", "identities", "use_parts", "per_head_factor"]
    result = ast.Dict(keys=[ast.Constant(k) for k in fields], values=[ast.Name(k, ast.Load()) for k in fields])
    fn.body = fn.body[:boundaries[0]] + [ast.Return(result)]
    if "--profile" in sys.argv:
        body = []
        last_peak = [0]
        def checkpoint(line):
            peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
            if peak - last_peak[0] > 100:
                print(f"[memory] upstream line {line}: peak {peak:.1f}MB", flush=True)
                last_peak[0] = peak
        module._coverage_checkpoint = checkpoint
        for statement in fn.body:
            body.append(statement)
            body.append(ast.Expr(ast.Call(ast.Name("_coverage_checkpoint", ast.Load()), [ast.Constant(getattr(statement, "lineno", 0))], [])))
        fn.body = body
    adapted = ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[]))
    exec(compile(adapted, str(source), "exec"), module.__dict__)
    # The normal builder accumulates gate failures until the end; the adapter must do that check now.
    module.FAILS.clear()
    frame_cache = module.F.CACHE / "asec25_generation.parquet"
    require(frame_cache.exists(), "read-only pricing requires existing canonical CPS frame cache")
    kwargs = dict(case=case, allocation="personal")
    if case == "oct15":
        kwargs["basis"] = basis
        kwargs["lines_path"] = lines_path or LANE / f"inputs/oct15_base/lines{'_cash' if basis == 'cash' else ''}.json"
    got = module.main("row4", **kwargs)
    require(not module.FAILS, "upstream pricing gates failed: " + repr(module.FAILS))
    require({"pieces", "residual", "d", "W", "w_id", "rows_u", "gens", "lines", "vec"} <= got.keys(),
            "pricing return schema changed")
    return module, got


def validate_metadata(meta, case="oct14"):
    require(meta.get("case") == {"oct14": "main_case_2026_10_14", "oct15": "main_case_2026_10_15"}[case], "mismatched case metadata")
    require(meta.get("allocation") == "personal", "mismatched allocation metadata")
    require(meta.get("convention") == "a", "mismatched generation convention")
    require(meta.get("spec_index") == {"low": 16, "high": 11}, "mismatched specification metadata")
    require(all(meta["specs"][e]["allocation"] == "personal" for e in ("low", "high")),
            "mismatched end allocation metadata")


def component_metadata(snapshot, piece, end):
    """Economic decomposition follows declarations, independently of synthetic storage side."""
    full = snapshot["lines"]["generations"][piece["g"]][end]
    group = full.get("before_native_children") or full
    native, carrier, state = piece.get("native_child_source"), piece.get("completion_source"), piece.get("state_price_source")
    parent = state["edit"]["line"] if state else native["parent"] if native else carrier.get("parent_line", piece["id"]) if carrier else piece["id"]
    result = {"generation": piece["g"], "line": piece["id"], "source_line": parent,
              "category": piece["cat"], "level": "unclassified", "economic_class": "fiscal_line"}
    if piece["cat"] == "capital":
        declarations = [x for x in group["capital"] if x["id"] == parent]
        require(len(declarations) == 1, "no declared public-capital level " + parent)
        result.update(economic_class="capital_return", source_side="capital", level=declarations[0]["level"])
    elif piece["cat"] == "production":
        result.update(economic_class="production", source_side="production", source_production=group["production"])
    elif piece["id"] == "mixed_unit_removal":
        result.update(economic_class="unclassified_post_engine", source_side="post_engine")
    elif carrier and parent == "lane_constants":
        result.update(economic_class="unclassified_post_engine", source_side="spending")
    else:
        side = state["edit"]["side"] if state else native.get("side") if native else carrier.get("side") if carrier else None
        declarations = [x for x in group["rows"] if x["id"] == parent and (side is None or x["side"] == side)]
        require(len(declarations) == 1, "no unique source-side fiscal line " + parent)
        result["source_side"] = declarations[0]["side"]
    return result


def main(tracker, case="oct14", basis="set", final_routing=False):
    start = time.perf_counter()
    def stage(name):
        if "--cpu-profile" in sys.argv:
            print(f"[profile] {name}: elapsed {time.perf_counter()-start:.3f}s; peak physical {peak_bytes()/1e6:.1f}MB", flush=True)
    if case == "oct14":
        verify_local_pins()
    else:
        from source_tables import load
        load()  # all source/control pins still gate the live route
        from coverage_oct15 import validate_frozen
        validate_frozen()
    if final_routing:
        from coverage_final_routing import FINAL, validate_final_inputs, observed_snapshot
        validate_final_inputs()
        module, s = construction(case=case, basis=basis,
            lines_path=FINAL / f"lines{'_cash' if basis == 'cash' else ''}.json")
        observed_snapshot(s)
    else:
        module, s = construction(case=case, basis=basis)
    stage("construction")
    ends, gen_names = tuple(module.ENDS), tuple(module.GENS)
    print(f"[memory] construction peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f}MB", flush=True)
    validate_metadata(s["lines"]["meta"], case)
    rows = s["rows_u"]
    w = s["W"][rows].copy()
    # The original constructor has already gated all 161 full-frame weights.
    # Pricing keeps those 161 columns on union rows; driver recovery needs only
    # full-frame central weights for fixed pension composite coefficients.
    s["W"] = s["W"][:, :1].copy()
    gc.collect()
    pa.default_memory_pool().release_unused()
    g = module.F.label(s["gens"], len(s["d"]))[rows]
    age = s["age"][rows]
    sex = s["d"].A_SEX.to_numpy()[rows]
    arrival = s["d"].PEINUSYR.to_numpy()[rows]
    hispanic = s["d"].PRDTHSP.to_numpy()[rows] > 0
    person_rows = rows.copy()
    person_ph_seq = s["d"].PH_SEQ.to_numpy()[rows].copy()
    person_pppos = s["d"].PPPOS.to_numpy()[rows].copy()
    require(np.isfinite(w).all() and (w >= 0).all() and (w[:, 0] > 0).all(), "invalid person weights")
    require(w.shape[1] == 161, "expected full weight plus 160 replicates")
    require(np.isin(sex, [1, 2]).all(), "invalid sex code")
    require(np.isin(arrival[g == 0], np.arange(1, 29)).all(), "unrecognized G1 arrival code")
    if case == "oct15":
        identified = s["coverage_identified_weights"]
        added = s["coverage_added_weights"]
        require(identified.shape == w.shape and added.shape == w.shape,
                "coverage identified/added weight shape")
        require(np.max(np.abs(identified + added - w)) < 1e-8, "coverage weight decomposition")
    else:
        identified = w.copy()
        identified[g == 2] /= s["f_rec"][rows][g == 2, None]
        added = w - identified
    counts = dict(s["lineage"]["counts"])
    if case == "oct15":
        completion = s["lines"]["meta"]["union_completion"]["counts"]
        counts["account_union"] += completion["reporters"]
        counts["added"] += completion["nonreporters"]
    if case == "oct15":
        rounding = s["lines"]["meta"]["population_rounding"]
        require(rounding["generation"] == "G1" and np.isfinite(rounding["people"]), "invalid population rounding declaration")
        require(abs(identified[:, 0].sum() + rounding["people"] - counts["account_union"]) < 1e-6,
                "identified-weight plus principal zero-dollar rounding conservation")
    else:
        require(abs(identified[:, 0].sum() - counts["account_union"]) < 1e-3, "identified-weight conservation")
    require(abs(added[:, 0].sum() - counts["added"]) < 1e-6, "added-weight conservation")
    require(np.all(added >= -1e-8), "negative added weights")
    if case == "oct15":
        exact_added = [s["lines"]["meta"]["coverage_added_cost_bn"][end] for end in module.ENDS]
    else:
        exact_added = json.loads((ROOT / "infra/immigration-fiscal/main_case_2026_10_14/derived/lineage_addition.json").read_text())["set"]["parts"]["added"]["cost_bn"]
    net = np.zeros((2, len(rows), 161))
    line_rows = []
    line_vectors = []
    line_national = []
    line_base = []
    other_prices, other_rows = [], []
    case_bn = []
    # Save actual canonical key vectors for the denominator sensitivity. Secondary keys (pensions, roads,
    # capital) use their declared parent key; the approximation and its scope are explicit in RESULT.
    for end_i, end in enumerate(module.ENDS):
        for p in s["pieces"][end]:
            x, bn = p["x"], float(p["bn"])
            denom = x @ w
            if bn == 0:
                continue
            require(np.isfinite(x).all() and np.isfinite(denom).all() and (denom > 0).all(),
                    "invalid or unassignable pricing piece " + p["id"])
            person = bn * x[:, None] / denom
            net[end_i] += person
            # Trace the actual driver (including pensions, routes, roads and capital), then verify that
            # its generation restriction is exactly the vector which priced this piece.
            full, source, override = full_key(s, p, end)
            mass = float(full @ (s["w_id"] * s["civ"])) if override is None else override
            require(np.isfinite(mass) and mass > 0, "invalid national key mass " + source)
            vector = full[rows].copy()
            scope = "actual_declared_driver"
            detail = component_metadata(s, p, end) if case == "oct15" else {}
            line_rows.append({"end": end, "generation": p["g"], "line": p["id"], "category": p["cat"],
                              "key": source, "denominator_scope": scope, **detail})
            line_vectors.append(vector)
            line_national.append(mass)
            # Copy this tiny column: a view would retain every 161-column temporary price matrix.
            line_base.append(person[:, 0].copy())
        for g_i, gen in enumerate(module.GENS):
            m = g == g_i
            residual = float(s["residual"][end].get(gen, 0.0))
            # [ASSUMPTION] constants have no person key; place them per head inside their generation.
            net[end_i, m] += residual / w[m].sum(axis=0)
            if case == "oct15":
                other_prices.append(np.where(m, residual / w[m, 0].sum(), 0.0))
                other_rows.append(dict(end=end, generation=gen, line="lane_residual", population="both"))
            got = (net[end_i, m] * w[m]).sum(axis=0)
            want = s["lines"]["generations"][gen][end]["cost_bn"]
            require(np.max(np.abs(got - want)) < 1e-6, "generation price closure " + gen + " " + end)
        total = (net[end_i] * w).sum(axis=0)
        want = s["lines"]["union"][end]["cost_bn"]
        require(np.max(np.abs(total - want)) < 1e-6, "case price closure " + end)
        case_bn.append(float(total[0]))
    stage("price pieces")
    combined_g3 = [s["lines"]["generations"]["G3plus"][end]["cost_bn"] for end in ends]
    population_rounding = s["lines"]["meta"].get("population_rounding")
    # Release the raw construction BEFORE allocating the separate net profile.
    # The phase probe located the budget crossing at those profile copies.
    del s, module, w
    gc.collect()
    pa.default_memory_pool().release_unused()
    stage("source buffers released")
    # Separate the added people's exact net total from the household route's blended G3+ placement.
    # Keep the existing individual profile and add a per-head calibration within the two G3+ parts.
    # This is a transparent distribution assumption; both populations and combined totals stay exact.
    net_id, net_add = net, net.copy()
    del net
    calibration = {}
    for end_i, end in enumerate(ends):
        m = g == 2
        want_added = exact_added[end_i]
        combined = combined_g3[end_i]
        for label, prices, weights, want in (("identified", net_id, identified, combined - want_added),
                                             ("added", net_add, added, want_added)):
            before = (prices[end_i, m] * weights[m]).sum(axis=0)
            adjustment = want - before
            prices[end_i, m] += adjustment / weights[m].sum(axis=0)
            require(np.max(np.abs((prices[end_i, m] * weights[m]).sum(axis=0) - want)) < 1e-6,
                    "separate G3+ price closure")
            calibration[end + "_" + label + "_bn"] = float(adjustment[0])
            if case == "oct15":
                other_prices.append(np.where(m, adjustment[0] / weights[m, 0].sum(), 0.0))
                other_rows.append(dict(end=end, generation="G3plus", line="net_profile_calibration", population=label))
    gc.collect()
    pa.default_memory_pool().release_unused()
    stage("calibration and release")
    age_rows = []
    for end_i, end in enumerate(ends):
        for label, weights, prices in [(gname, identified * (g == g_i)[:, None], net_id)
                                       for g_i, gname in enumerate(gen_names)] + [("added", added, net_add)]:
            all_cost, all_pop = 0.0, 0.0
            for lo in range(0, 81, 5):
                m = (age >= lo) & ((age < lo + 5) if lo < 80 else True)
                pop = float(weights[m, 0].sum())
                if pop == 0:
                    continue
                dollars = (prices[end_i, m] * weights[m]).sum(axis=0)
                age_rows.append({"end": end, "specification": [16, 11][end_i], "allocation": "personal",
                                 "generation": label, "age_band_march2025": f"{lo}-{lo+4}" if lo < 80 else "80+",
                                 "population": pop, "cost_bn": float(dollars[0]),
                                 "per_member_usd": float(dollars[0]) * 1e9 / pop,
                                 "cps_replicate_se_bn": float(np.sqrt(4 / 160 * np.square(dollars[1:] - dollars[0]).sum()))})
                all_cost += float(dollars[0])
                all_pop += pop
            require(abs(all_cost - float((prices[end_i] * weights).sum(axis=0)[0])) < 1e-6, "age-price cost closure")
            require(abs(all_pop - float(weights[:, 0].sum())) < 1e-6, "age-price population closure")
    vintage = "oct15_final_routing" if final_routing else case
    suffix = "" if case == "oct14" else f"_{vintage}_{basis}"
    with (LANE / f"derived/age_prices{suffix}.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=age_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(age_rows)
    dependency_hash = tracker.finish()
    cache = LANE / "_cache" / ("" if case == "oct14" else f"{vintage}/{basis}")
    cache.mkdir(exist_ok=True, parents=True)
    extra = {"other_piece_prices": np.asarray(other_prices)} if case == "oct15" else {}
    other_prices.clear()
    national_vectors = np.asarray(line_vectors)
    line_vectors.clear()
    base_piece_prices = np.asarray(line_base)
    line_base.clear()
    stage("packed cache")
    np.savez_compressed(cache / "pricing.npz", weights=identified, added_weights=added, generation=g,
                        age=age, sex=sex, arrival=arrival, hispanic=hispanic,
                        person_rows=person_rows, person_ph_seq=person_ph_seq, person_pppos=person_pppos,
                        net_id=net_id, net_added=net_add, national_vectors=national_vectors,
                        national_masses=np.asarray(line_national), base_piece_prices=base_piece_prices, **extra)
    stage("compressed cache")
    audit = {"case": case, "basis": basis, "allocation": "personal", "specifications": [16, 11],
             "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "national_keys_sha256": hashlib.sha256((LANE / "national_keys.py").read_bytes()).hexdigest(),
             "dependency_manifest_sha256": dependency_hash,
             "pricing_cache_sha256": hashlib.file_digest((cache / "pricing.npz").open("rb"), "sha256").hexdigest(),
             "price_rule": "case consumer piece vectors, flat accrual as in case; constants per head; G3+ per-head net calibration separates exact added total",
             "identified_population": float(identified[:, 0].sum()), "added_population": float(added[:, 0].sum()),
             "population_rounding": population_rounding,
             "case_bn": case_bn,
             "g3_net_calibration": calibration, "denominator_pieces": line_rows,
             "other_pieces": other_rows,
             "gates": {"metadata": True, "161_weights": True, "population_conservation": True,
                       "every_generation_and_replicate_closes_1e_6bn": True, "separate_added_total_closes_1e_6bn": True}}
    if final_routing:
        audit.update(routing_vintage="oct15_final_routing", coverage_on_observed_people=False,
                     source_lines_sha256=hashlib.file_digest((FINAL / f"lines{'_cash' if basis == 'cash' else ''}.json").open("rb"), "sha256").hexdigest())
    elapsed = time.perf_counter() - start
    memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6  # bytes on macOS
    footprint = require_within_budget("coverage person pricing")
    audit["gates"]["physical_footprint_within_2_5GB"] = True
    (LANE / f"derived/pricing_audit{suffix}.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(f"pricing {case}/{basis} PASS; elapsed {elapsed:.3f}s; peak physical footprint {footprint/1e6:.1f}MB; RSS {memory:.1f}MB")


def profile_call(call, destination):
    """Save CPU evidence while propagating failures (stdlib cProfile CLI hides SystemExit)."""
    profile = cProfile.Profile()
    profile.enable()
    try:
        return call()
    finally:
        profile.disable()
        profile.dump_stats(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["oct14", "oct15"], default="oct15")
    parser.add_argument("--basis", choices=["set", "cash"], default="set")
    parser.add_argument("--capture-dependencies", action="store_true")
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--cpu-profile", action="store_true")
    parser.add_argument("--final-routing", action="store_true")
    args = parser.parse_args()
    require(args.case != "oct14" or args.basis == "set", "historical oct14 cash route was not defined")
    require(not args.final_routing or args.case == "oct15", "final routing needs oct15")
    vintage = "oct15_final_routing" if args.final_routing else args.case
    manifest = LANE / ("inputs/pricing_dependencies.json" if args.case == "oct14"
                       else f"inputs/pricing_dependencies_{vintage}_{args.basis}.json")
    with guard(capture=args.capture_dependencies, manifest=manifest,
               route=f"coverage {vintage} personal flat pricing" + ("" if args.case == "oct14" else f" {args.basis}")) as tracker:
        if args.cpu_profile:
            profile_call(lambda: main(tracker, args.case, args.basis, args.final_routing),
                         LANE / f"_cache/export_{vintage}_{args.basis}.prof")
        else:
            main(tracker, args.case, args.basis, args.final_routing)

"""Reuse the case consumer's gated person-price construction without upstream writes.

Native-First: reuse households.py's AST through its piece-construction boundary.
This is a read-only adapter, not a second implementation of its fiscal keys.
The pinned upstream source and uniquely matched AST boundary both fail closed.
"""
import ast
import csv
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from national_keys import full_key
from dependency_manifest import guard

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


def construction(source=SOURCE):
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
    got = module.main("row4", case="oct14", allocation="personal")
    require(not module.FAILS, "upstream pricing gates failed: " + repr(module.FAILS))
    require({"pieces", "residual", "d", "W", "w_id", "rows_u", "gens", "lines", "vec"} <= got.keys(),
            "pricing return schema changed")
    return module, got


def validate_metadata(meta):
    require(meta.get("case") == "main_case_2026_10_14", "mismatched case metadata")
    require(meta.get("allocation") == "personal", "mismatched allocation metadata")
    require(meta.get("convention") == "a", "mismatched generation convention")
    require(meta.get("spec_index") == {"low": 16, "high": 11}, "mismatched specification metadata")
    require(all(meta["specs"][e]["allocation"] == "personal" for e in ("low", "high")),
            "mismatched end allocation metadata")


def main(tracker):
    start = time.perf_counter()
    verify_local_pins()
    module, s = construction()
    print(f"[memory] construction peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f}MB", flush=True)
    validate_metadata(s["lines"]["meta"])
    rows = s["rows_u"]
    w = s["W"][rows].copy()
    g = module.F.label(s["gens"], len(s["d"]))[rows]
    age = s["age"][rows]
    sex = s["d"].A_SEX.to_numpy()[rows]
    arrival = s["d"].PEINUSYR.to_numpy()[rows]
    hispanic = s["d"].PRDTHSP.to_numpy()[rows] > 0
    require(np.isfinite(w).all() and (w >= 0).all() and (w[:, 0] > 0).all(), "invalid person weights")
    require(w.shape[1] == 161, "expected full weight plus 160 replicates")
    require(np.isin(sex, [1, 2]).all(), "invalid sex code")
    require(np.isin(arrival[g == 0], np.arange(1, 29)).all(), "unrecognized G1 arrival code")
    identified = w.copy()
    identified[g == 2] /= s["f_rec"][rows][g == 2, None]
    added = w - identified
    counts = s["lineage"]["counts"]
    require(abs(identified[:, 0].sum() - counts["account_union"]) < 1e-3, "identified-weight conservation")
    require(abs(added[:, 0].sum() - counts["added"]) < 1e-6, "added-weight conservation")
    require(np.all(added >= -1e-8), "negative added weights")
    exact_added = json.loads((ROOT / "infra/immigration-fiscal/main_case_2026_10_14/derived/lineage_addition.json").read_text())["set"]["parts"]["added"]["cost_bn"]
    net = np.zeros((2, len(rows), 161))
    line_rows = []
    line_vectors = []
    line_national = []
    line_base = []
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
            line_rows.append({"end": end, "generation": p["g"], "line": p["id"], "category": p["cat"],
                              "key": source, "denominator_scope": scope})
            line_vectors.append(vector)
            line_national.append(mass)
            # Copy this tiny column: a view would retain every 161-column temporary price matrix.
            line_base.append(person[:, 0].copy())
        for g_i, gen in enumerate(module.GENS):
            m = g == g_i
            residual = float(s["residual"][end].get(gen, 0.0))
            # [ASSUMPTION] constants have no person key; place them per head inside their generation.
            net[end_i, m] += residual / w[m].sum(axis=0)
            got = (net[end_i, m] * w[m]).sum(axis=0)
            want = s["lines"]["generations"][gen][end]["cost_bn"]
            require(np.max(np.abs(got - want)) < 1e-6, "generation price closure " + gen + " " + end)
        total = (net[end_i] * w).sum(axis=0)
        want = s["lines"]["union"][end]["cost_bn"]
        require(np.max(np.abs(total - want)) < 1e-6, "case price closure " + end)
    # Separate the added people's exact net total from the household route's blended G3+ placement.
    # Keep the existing individual profile and add a per-head calibration within the two G3+ parts.
    # This is a transparent distribution assumption; both populations and combined totals stay exact.
    net_id, net_add = net.copy(), net.copy()
    calibration = {}
    for end_i, end in enumerate(module.ENDS):
        m = g == 2
        want_added = exact_added[end_i]
        combined = s["lines"]["generations"]["G3plus"][end]["cost_bn"]
        for label, prices, weights, want in (("identified", net_id, identified, combined - want_added),
                                             ("added", net_add, added, want_added)):
            before = (prices[end_i, m] * weights[m]).sum(axis=0)
            adjustment = want - before
            prices[end_i, m] += adjustment / weights[m].sum(axis=0)
            require(np.max(np.abs((prices[end_i, m] * weights[m]).sum(axis=0) - want)) < 1e-6,
                    "separate G3+ price closure")
            calibration[end + "_" + label + "_bn"] = float(adjustment[0])
    age_rows = []
    for end_i, end in enumerate(module.ENDS):
        for label, weights, prices in [(gname, identified * (g == g_i)[:, None], net_id)
                                       for g_i, gname in enumerate(module.GENS)] + [("added", added, net_add)]:
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
    with (LANE / "derived/age_prices.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=age_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(age_rows)
    dependency_hash = tracker.finish()
    cache = LANE / "_cache"
    cache.mkdir(exist_ok=True)
    np.savez_compressed(cache / "pricing.npz", weights=identified, added_weights=added, generation=g,
                        age=age, sex=sex, arrival=arrival, hispanic=hispanic,
                        net_id=net_id, net_added=net_add, national_vectors=np.asarray(line_vectors),
                        national_masses=np.asarray(line_national), base_piece_prices=np.asarray(line_base))
    audit = {"case": "oct14", "allocation": "personal", "specifications": [16, 11],
             "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "national_keys_sha256": hashlib.sha256((LANE / "national_keys.py").read_bytes()).hexdigest(),
             "dependency_manifest_sha256": dependency_hash,
             "pricing_cache_sha256": hashlib.file_digest((cache / "pricing.npz").open("rb"), "sha256").hexdigest(),
             "price_rule": "case consumer piece vectors, flat accrual as in case; constants per head; G3+ per-head net calibration separates exact added total",
             "identified_population": float(identified[:, 0].sum()), "added_population": float(added[:, 0].sum()),
             "case_bn": [float((net[i] * w).sum(axis=0)[0]) for i in range(2)],
             "g3_net_calibration": calibration, "denominator_pieces": line_rows,
             "gates": {"metadata": True, "161_weights": True, "population_conservation": True,
                       "every_generation_and_replicate_closes_1e_6bn": True, "separate_added_total_closes_1e_6bn": True}}
    (LANE / "derived/pricing_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    elapsed = time.perf_counter() - start
    memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6  # bytes on macOS
    require(memory < 2500, f"pricing peak memory {memory:.1f}MB exceeded 2.5 GB")
    print(f"pricing PASS; elapsed {elapsed:.3f}s; peak RSS {memory:.1f}MB")


if __name__ == "__main__":
    with guard(capture="--capture-dependencies" in sys.argv) as tracker:
        main(tracker)

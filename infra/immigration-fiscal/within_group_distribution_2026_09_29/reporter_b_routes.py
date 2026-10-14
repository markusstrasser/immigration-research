"""Exact NAS(b) ownership of every declared reporter carrier's raw driver.

The AST adapter reuses household driver primitives before endpoint price skips.
It does not write household outputs or change convention(a). Existing members
retain the P7 parent vintage; only the 204 new reporters use completed parents.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
BASE = FISCAL / "coverage_bound_2026_10_14/inputs/oct15_base"
MEASUREMENT = FISCAL / "generation_account_2026_09_24/inputs/minor_parent_measurement_oct15.json"
SOURCE = HERE / "households.py"
GENS = ("G1", "G2", "G3plus")


def require(ok, message):
    if not ok:
        raise SystemExit("[BLOCKED] reporter raw routes: " + message)


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def atomic_json_write(target, result, budget_check=None):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=target.parent, prefix=target.name+".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(result, stream, separators=(",", ":"), allow_nan=False)
            stream.write("\n")
        peak = budget_check() if budget_check is not None else None
        temporary.replace(target)
        return peak
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def component_shares(components, weights, omega, by):
    """Signed composites preserve each raw component; zero quantities are explicit."""
    require(weights.ndim == 2 and weights.shape[1] == 161 and omega.shape == (len(weights), 3), "weight/omega shape")
    require(np.max(np.abs(omega.sum(axis=1)-1)) < 1e-12, "reporter omega does not partition records")
    shares = np.zeros((3, 161))
    require(abs(sum(c[0] for c in components)-1) < 1e-12, "raw component coefficients do not sum to one")
    for coefficient, values in components:
        require(values.shape == (len(weights),) and np.isfinite(values).all(), "invalid raw driver")
        if coefficient == 0:
            continue
        den = values @ weights
        if np.any(den == 0):
            require(by == 0, "nonzero raw part has a zero driver mass")
            return np.tile(np.array([[0.0], [0.0], [1.0]]), (1, 161)), True
        numerators = np.einsum("i,ir,ig->gr", values, weights, omega)
        shares += coefficient * numerators / den
    require(np.isfinite(shares).all() and np.max(np.abs(shares.sum(axis=0)-1)) < 1e-12, "generation shares do not close")
    require(np.max(np.abs((shares*by).sum(axis=0)-by)) < 1e-9, "raw generation amounts do not close")
    return shares, False


class RawCollector:
    def __init__(self, module, inventory, basis, measurement, carrier_code, zero_raw_driver_policy="stop"):
        self.module, self.inventory, self.basis = module, inventory, basis
        self.measurement, self.carrier_code = measurement, carrier_code
        self.routes, self.pool, self.reporters = {}, {}, None
        self.pins = {}
        self.calls = 0
        self.errors = []
        self.zero_raw_driver_policy = zero_raw_driver_policy

    def read(self, path):
        path = Path(path)
        self.pins[str(path.relative_to(FISCAL))] = sha(path)
        return json.loads(path.read_text())

    def add_gap_key(self, ctx):
        # Principal recipe: generation_account/keys.py lines300-318.
        cats_path = FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv"
        tax_path = FISCAL / "admin_tax_checks_2026_09_19/derived/group_components.csv"
        for path in (cats_path, tax_path):
            self.pins[str(path.relative_to(FISCAL))] = sha(path)
        cats, tax = pd.read_csv(cats_path), pd.read_csv(tax_path)
        for allocation in ("personal", "shared"):
            fb = ctx["vec"][allocation][("receipt", "federal_liability")]
            hi = ctx["vec"][allocation][("receipt", "federal_high_agi")]
            national = tax.query("allocation == @allocation and group == 'national_civilian' and metric == 'federal_before_refundable'").value
            gap = cats.query("scenario_id == 'federal_gap_high_agi' and category == 'federal_income_tax' and allocation == @allocation").national_bn
            require(len(national) == len(gap) == 1, "high-AGI composite has no unique national declaration")
            den = float(hi[ctx["civ"]] @ ctx["w_pub"][ctx["civ"]])
            require(den > 0, "high-AGI composite national driver has no mass")
            vector = fb + (float(gap.iloc[0])-float(national.iloc[0])/1e9)*1e9*hi/den
            ctx["vec"][allocation][("receipt", "observed_liability_plus_positive_gap_high_agi")] = vector
            original = ctx["original_gens"]
            totals = np.array([float(vector[m] @ ctx["w_pub"][m]) for m in original.values()])
            expected = self.read(FISCAL / "generation_account_2026_09_24/derived/generation_key_shares.json")["shares"]["receipt"][allocation]["observed_liability_plus_positive_gap_high_agi"]["a"]
            require(np.max(np.abs(totals/totals.sum()-expected)) < 1e-9, "high-AGI primitive differs from principal generation recipe")

    def initialize(self, ctx):
        d = ctx["d"]
        identities = {(int(h), int(p)): i for i, (h, p) in enumerate(zip(d.PH_SEQ, d.PPPOS, strict=True))}
        records = self.measurement["reporter_assignment_b"]
        require(len(records) == 204 and len({(r["PH_SEQ"], r["PPPOS"]) for r in records}) == 204, "principal reporter identities")
        self.rows = np.array([identities[(r["PH_SEQ"], r["PPPOS"])] for r in records])
        require(set(self.rows) == set(np.flatnonzero(ctx["reporter"])), "reporter identity set differs from household kernel")
        self.weights = ctx["W"][self.rows].copy()
        expected = np.array([r["replicate_weights"] for r in records])
        require(np.array_equal(self.weights, expected), "principal reporter replicate weights differ")
        self.omega = np.array([r["omega"] for r in records])
        self.reporters = [{**r, "omega_b": r["omega"]} for r in records]
        self.add_gap_key(ctx)

    def view(self, ctx):
        """All raw selector amounts, with the source's existing split functions."""
        basis, allocation = self.basis, ctx["a"]
        model = self.inventory["sets"][basis]
        old = ctx["G"]
        rows = []
        for row in old["rows"]:
            r = dict(row)
            parent = model["receipt" if r["side"] == "receipt" else "spending"].get(r["id"])
            require(parent is not None, "raw model lacks row " + r["id"])
            cell = parent["cells"][r["scenario"]][allocation] if r["side"] == "receipt" else parent["keys"][r["key"]][allocation]
            r["amount_bn"] = cell["target_bn"]
            if r["side"] == "receipt":
                r["key"] = cell["key"]
            rows.append(r)
        pension = dict(old["pension"])
        result = {**old, "rows": rows, "pension": pension, "allocation": allocation}
        if allocation == "shared":
            shared = self.read(HERE / "_cache/oct14/shared_allocation/lines.json")
            result["roads"] = shared["generations"]["G3plus"][ctx["end"]]["roads"]
        capital = [dict(c) for c in old["capital"]]
        for c in capital:
            if c["rule"]["kind"] == "part_rekeyed":
                rule = c["rule"]
                parent = model["spending"][rule["parent_line"]]
                correction = model["spending"][rule["correction_line"]]
                parent_row = next(r for r in rows if r["side"] == "spending" and r["id"] == rule["parent_line"])
                correction_row = next(r for r in rows if r["side"] == "spending" and r["id"] == rule["correction_line"])
                c["shares"] = dict(parent=parent["keys"][parent_row["key"]][allocation]["target_bn"]/parent["national_bn"],
                                   part=correction["keys"][correction_row["key"]][allocation]["target_bn"]/rule["part_national_bn"])
        result["capital"] = capital
        return result

    def selector(self, view, ctx, source):
        if source["kind"] != "line":
            return
        side, lid, key = source["side"], source["parent_line"], source["parent_key"]
        allocation, basis = ctx["a"], self.basis
        row = next(r for r in view["rows"] if r["side"] == side and r["id"] == lid)
        model = self.inventory["sets"][basis]
        parent = model["receipt" if side == "receipt" else "spending"][lid]
        cell = parent["cells"][key][allocation] if side == "receipt" else parent["keys"][key][allocation]
        row["amount_bn"] = cell["target_bn"]
        if side == "receipt":
            view["receipt_scenario"] = key
            row["scenario"], row["key"] = key, cell["key"]
        else:
            row["key"] = key
        if basis == "set" and lid in ("medicare", "federal_income_tax"):
            cash = self.inventory["sets"]["cash"]
            if lid == "medicare":
                amount = cash["spending"][lid]["keys"][key][allocation]["target_bn"]
                view["pension"]["medicare_benefits_bn"] = (1-ctx["PA"]["part_a_share"])*amount
                view["pension"]["part_a_accrual_bn"] = row["amount_bn"]-view["pension"]["medicare_benefits_bn"]
            else:
                amount = cash["receipt"][lid]["cells"][key][allocation]["target_bn"]
                view["pension"]["fit_cash_bn"] = amount
                view["pension"]["benefit_tax_bn"] = amount-row["amount_bn"]

    def __call__(self, ctx):
        if self.reporters is None:
            self.initialize(ctx)
        self.calls += 1
        allocation, end = ctx["a"], ctx["end"]
        original_view = ctx["G"]
        view = self.view(ctx)
        saved = dict(original_view)
        try:
            for name, part in self.inventory["sets"][self.basis]["parts"].items():
                source = part["selector"]
                if source["kind"] != "line" and source["end"] != end:
                    continue
                by = part["by"][allocation]
                ownership = dict(kind="actual_selected_raw_driver")
                if by == 0:
                    shares, zero = np.tile(np.array([[0.0], [0.0], [1.0]]), (1, 161)), True
                    components = []
                else:
                    chosen = {**view, "rows": [dict(r) for r in view["rows"]], "pension": dict(view["pension"])}
                    self.selector(chosen, ctx, source)
                    original_view.clear(); original_view.update(chosen)
                    row = next(r for r in chosen["rows"] if r["id"] == part["carrier"])
                    if source["kind"] == "line":
                        parent = next(r for r in chosen["rows"] if r["side"] == source["side"] and r["id"] == source["parent_line"])
                        row["response"] = parent["response"]
                    namespace = {**self.module.__dict__, **ctx, "i": part["carrier"], "row": row}
                    exec(self.carrier_code, namespace)
                    split = namespace["split"]
                    components = [(float(coefficient), np.asarray(values)[self.rows].copy()) for _, coefficient, values in split]
                    undefined = any(coefficient != 0 and np.any(values @ self.weights == 0) for coefficient, values in components)
                    if undefined and self.zero_raw_driver_policy == "source_anchor" and source.get("extrapolated_key"):
                        anchor = part.get("source_anchor")
                        require(anchor is not None, "source anchor declaration missing for " + name)
                        anchor_source = {**source, "parent_key": anchor["source_key"]}
                        anchored = {**view, "rows": [dict(r) for r in view["rows"]], "pension": dict(view["pension"])}
                        self.selector(anchored, ctx, anchor_source)
                        original_view.clear(); original_view.update(anchored)
                        row = next(r for r in anchored["rows"] if r["id"] == part["carrier"])
                        parent = next(r for r in anchored["rows"] if r["side"] == source["side"] and r["id"] == source["parent_line"])
                        row["response"] = parent["response"]
                        completion = {**ctx["completion"], "carriers": {**ctx["completion"]["carriers"], part["carrier"]: anchor_source}}
                        namespace = {**self.module.__dict__, **ctx, "completion": completion, "i": part["carrier"], "row": row}
                        exec(self.carrier_code, namespace)
                        components = [(float(c), np.asarray(x)[self.rows].copy()) for _, c, x in namespace["split"]]
                        ownership = dict(kind="modeled_source_anchor", zero_raw_driver_policy="source_anchor", declaration=anchor,
                            rule="exact unused-key reporter mass is zero; use item_union263–277 authoritative fallback anchor ownership; retain alternative carrier key/response/by",
                            limitation="Modeled record ownership, not observed alternative-key measurement")
                    try:
                        shares, zero = component_shares(components, self.weights, self.omega, by)
                    except SystemExit as exc:
                        self.errors.append(f"{exc}; {name}/{allocation}/{end}; components " +
                            repr([(c, float(x @ self.weights[:, 0]), int(np.count_nonzero(x))) for c, x in components]))
                        continue
                encoded = []
                for coefficient, values in components:
                    driver_id = hashlib.sha256(values.tobytes()).hexdigest()
                    self.pool.setdefault(driver_id, dict(values=values.tolist(), primitive="actual household raw parent split: " + part["carrier"]))
                    encoded.append(dict(driver_id=driver_id, raw_share=coefficient))
                allocation_result = dict(components=encoded, zero_quantity_ownership=zero, ownership=ownership,
                    generation_shares={g: shares[i].tolist() for i, g in enumerate(GENS)},
                    by_generation_bn={g: (shares[i]*by).tolist() for i, g in enumerate(GENS)})
                route = self.routes.setdefault(name, {**part, "allocations": {}})
                previous = route["allocations"].get(allocation)
                if previous is not None:
                    require(np.max(np.abs(np.array(list(previous["generation_shares"].values()))-shares)) < 1e-12,
                            f"raw line driver depends on endpoint: {name}/{allocation}")
                else:
                    route["allocations"][allocation] = allocation_result
        finally:
            original_view.clear(); original_view.update(saved)


def adapted(module, collector):
    tree = ast.parse(SOURCE.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    row_loops = [n for n in ast.walk(fn) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == "row"
                 and ast.unparse(n.iter) == "G['rows']"]
    require(len(row_loops) == 1, "raw parent construction boundary changed")
    carrier = [n for n in row_loops[0].body if isinstance(n, ast.If) and isinstance(n.body[0], ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "src" for t in n.body[0].targets)]
    require(len(carrier) == 1, "reporter raw split branch changed")
    split_at = [i for i, n in enumerate(carrier[0].body) if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple)]
    require(len(split_at) == 1, "reporter raw component boundary changed")
    carrier_code = compile(ast.fix_missing_locations(ast.Module(body=carrier[0].body[:split_at[0]], type_ignores=[])), str(SOURCE), "exec")
    collector.carrier_code = carrier_code
    gen_loops = [n for n in ast.walk(fn) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == "g"
                 and row_loops[0] in n.body]
    require(len(gen_loops) == 1, "raw generation boundary changed")
    loop = gen_loops[0]
    cut = loop.body.index(row_loops[0])
    loop.body = loop.body[:cut] + ast.parse("""
if g == 'G3plus':
    source_allocation = a
    for a in ('personal', 'shared'):
        _raw_collector(locals())
    a = source_allocation
""").body
    boundary = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Delete)
                and {t.id for t in n.targets if isinstance(t, ast.Name)} == {"prod_parts", "vec", "rk", "sk", "medical", "edu", "v"}]
    require(len(boundary) == 1, "raw main boundary changed")
    fn.body = fn.body[:boundary[0]] + ast.parse("return None").body
    module._raw_collector = collector
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(SOURCE), "exec"), module.__dict__)


def main(basis, zero_raw_driver_policy):
    started = time.perf_counter()
    read_pins, auditing = {}, False

    def record_read(event, args):
        nonlocal auditing
        if auditing or event != "open" or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(args[0])).resolve()
        if path.suffix == ".pyc":
            # Import caches are disposable; provenance pins their canonical source.
            try:
                path = Path(importlib.util.source_from_cache(str(path)))
            except ValueError:
                require(False, "noncanonical bytecode dependency " + str(path))
        if not path.is_relative_to(FISCAL) or not path.is_file() or (args[2] & (os.O_WRONLY | os.O_RDWR)):
            return
        rel = str(path.relative_to(FISCAL))
        if rel not in read_pins:
            auditing = True
            try:
                read_pins[rel] = sha(path)
            finally:
                auditing = False

    sys.addaudithook(record_read)
    inventory = json.loads((HERE / "derived/reporter_b_inputs.json").read_text())
    for rel, expected in inventory["source_sha256"].items():
        require(sha(FISCAL / rel) == expected, "stale raw inventory source " + rel)
    measurement = json.loads(MEASUREMENT.read_text())
    for rel, expected in measurement["source_sha256"].items():
        require(sha(FISCAL / rel) == expected, "stale measured parent source " + rel)
    spec = importlib.util.spec_from_file_location("reporter_raw_households", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    collector = RawCollector(module, inventory, basis, measurement, None, zero_raw_driver_policy)
    adapted(module, collector)
    module.FAILS.clear()
    module.main("row4", case="oct15", basis=basis, lines_path=BASE / f"lines{'_cash' if basis == 'cash' else ''}.json")
    require(not module.FAILS, "upstream primitive gates failed: " + repr(module.FAILS))
    require(not collector.errors, "undefined raw ownership:\n" + "\n".join(collector.errors))
    expected = inventory["sets"][basis]["parts"]
    require(set(collector.routes) == set(expected) and collector.calls == 4, "all339 raw parts and both allocations/end selectors were not covered")
    require(all(set(r["allocations"]) == {"personal", "shared"} for r in collector.routes.values()), "raw allocation coverage")
    sources = {**measurement["source_sha256"], **inventory["source_sha256"], **read_pins, **collector.pins,
               "within_group_distribution_2026_09_29/reporter_b_inputs.cjs": sha(HERE / "reporter_b_inputs.cjs"),
               "within_group_distribution_2026_09_29/reporter_b_routes.py": sha(Path(__file__)),
               "within_group_distribution_2026_09_29/households.py": sha(SOURCE),
               "generation_account_2026_09_24/inputs/minor_parent_measurement_oct15.json": sha(MEASUREMENT),
               "within_group_distribution_2026_09_29/_cache/sept29/person_accrual.parquet": sha(HERE / "_cache/sept29/person_accrual.parquet"),
               "within_group_distribution_2026_09_29/derived/sept29/person_accrual_model.json": sha(HERE / "derived/sept29/person_accrual_model.json")}
    for rel, expected_sha in sources.items():
        require(sha(FISCAL / rel) == expected_sha, "source changed during reporter routes: " + rel)
    peak = module.require_within_budget("all raw reporter parent routes")
    result = dict(contract="oct15 reporter NAS(b) all raw carrier ownership", basis=basis, source_sha256=sources,
        reporters=collector.reporters, driver_pool=collector.pool, sets={basis: dict(routes=collector.routes)},
        existing_union_parent_vintage="P7_frozen", convention="b", replicate_order=module.F.REPS,
        zero_raw_driver_policy=zero_raw_driver_policy,
        composition_rule="record contribution = sum component raw_share * driver_value * reporter_weight / sum reporter driver_weight; destination uses measured omega_b",
        gates=dict(all339_declared_raw_parts=True, all161_replicates=True, exact_reporter_weights=True,
                   shares_closure_1e_12=True, by_amount_closure_1e_9=True, physical_footprint_within_2_5GB=True),
        resources=dict(physical_footprint_limit_bytes=2_500_000_000))
    target = HERE / f"derived/reporter_b_routes_{basis}.json"
    peak = atomic_json_write(target, result, lambda: module.require_within_budget("serialized all raw reporter parent routes"))
    print(json.dumps(dict(basis=basis, routes=len(collector.routes), driver_count=len(collector.pool), elapsed_seconds=time.perf_counter()-started,
                          physical_footprint_bytes=peak)), flush=True)


def merge():
    results = [json.loads((HERE / f"derived/reporter_b_routes_{basis}.json").read_text()) for basis in ("set", "cash")]
    left, right = results
    require(left["reporters"] == right["reporters"], "set/cash reporter frames differ")
    sources, pool, sets = {}, {}, {}
    for result in results:
        for rel, expected in result["source_sha256"].items():
            require(sha(FISCAL / rel) == expected, "stale publication source " + rel)
            require(rel not in sources or sources[rel] == expected, "set/cash source pin conflict " + rel)
            sources[rel] = expected
        for key, driver in result["driver_pool"].items():
            require(key not in pool or pool[key]["values"] == driver["values"], "driver pool collision")
            pool.setdefault(key, driver)
        sets.update(result["sets"])
    result = {k: v for k, v in left.items() if k not in ("basis", "source_sha256", "driver_pool", "sets")}
    result.update(source_sha256=sources, driver_pool=pool, sets=sets)
    target = HERE / "derived/reporter_b_routes.json"
    atomic_json_write(target, result)
    print("✓ published exact reporter raw routes: 339 set / 339 cash, both allocations, all161 replicates", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--basis", choices=("set", "cash"))
    group.add_argument("--merge", action="store_true")
    parser.add_argument("--zero-raw-driver-policy", choices=("stop", "source_anchor"), default="stop")
    args = parser.parse_args()
    merge() if args.merge else main(args.basis, args.zero_raw_driver_policy)

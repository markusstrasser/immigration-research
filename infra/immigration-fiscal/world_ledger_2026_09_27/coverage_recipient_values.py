"""Recipient-only transport where zero fiscal response erased a public-good price.

The canonical household constructor supplies its exact native routed_split
vectors before its zero-cost skip. No coverage factor or fiscal allocation is
reimplemented. Its original fiscal calculations and guards are unchanged.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import coverage_transport as CT
import valuation as V

HERE = Path(__file__).resolve().parent
COVERAGE = CT.COVERAGE


def transport_price(vector, weights, coverage_weights, amount):
    """The constructor's counted price, transported on its exported donor mass."""
    require(np.isfinite(vector).all() and np.isfinite(weights).all()
            and np.isfinite(coverage_weights).all(), "nonfinite canonical key")
    denominator = float(vector @ weights)
    require(denominator > 0 or amount == 0, "zero canonical key mass")
    price = amount * vector / denominator if denominator else np.zeros(len(vector))
    require(abs(float(price @ weights) - amount) < 1e-9, "counted recipient amount does not close")
    return float(price @ coverage_weights)


def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] coverage recipient values: " + why)


def instrument(tree):
    """Capture a canonical row immediately before its unchanged zero-cost skip."""
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    require(len(functions) == 1, "unique canonical main absent")
    fn = functions[0]
    row_loops = [n for n in ast.walk(fn) if isinstance(n, ast.For) and ast.unparse(n.target) == "row"
                 and ast.unparse(n.iter) == "G['rows']"]
    require(len(row_loops) == 1, "unique native row loop absent")
    loop = row_loops[0]
    skips = [i for i, n in enumerate(loop.body) if isinstance(n, ast.If)
             and ast.unparse(n.test) == "bn == 0" and len(n.body) == 1 and isinstance(n.body[0], ast.Continue)]
    require(len(skips) == 1, "canonical zero-cost skip changed")
    # Permit zero-response recipient rows through their original native routing,
    # keeping fiscal bn=0. Capture only the original routed share/vector passed
    # to add; all original fiscal guards still see exactly zero added cost.
    skip = loop.body[skips[0]]
    skip.test = ast.BoolOp(ast.And(), [skip.test, ast.UnaryOp(ast.Not(),
        ast.Call(ast.Name("_zero_recipient_row", ast.Load()), [ast.Name("row", ast.Load()),
            ast.Call(ast.Name("locals", ast.Load()), [], [])], []))])
    additions = 0
    for node in ast.walk(loop):
        if isinstance(node, ast.For):
            body = []
            for statement in node.body:
                body.append(statement)
                if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
                        and isinstance(statement.value.func, ast.Name) and statement.value.func.id == "add"
                        and len(statement.value.args) == 4 and isinstance(statement.value.args[3], ast.Name)
                        and statement.value.args[3].id == "i"):
                    body.append(ast.parse("_capture_zero_recipient(locals(), x, share)").body[0])
                    additions += 1
            node.body = body
    require(additions == 2, "canonical direct/carrier routing call sites changed")
    expected = {"prod_parts", "vec", "rk", "sk", "medical", "edu", "v"}
    boundaries = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Delete)
                  and {x.id for x in n.targets if isinstance(x, ast.Name)} == expected]
    require(len(boundaries) == 1, "canonical construction boundary changed")
    fn.body = fn.body[:boundaries[0]] + [ast.Return(ast.Constant(None))]
    pattern = ast.parse("source = FISCAL / coverage['file']").body[0]
    assignments = [n for n in ast.walk(fn) if isinstance(n, ast.Assign) and ast.dump(n) == ast.dump(pattern)]
    require(len(assignments) == 1, "frozen canonical coverage boundary changed")
    assignments[0].value = ast.Call(ast.Name("_coverage_frozen_source", ast.Load()), [ast.Name("coverage", ast.Load())], [])
    return ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[]))


def routing_paths(case, basis):
    """Use the selected native routing receipt; never relabel an older case."""
    require(basis in ("cash", "set"), "explicit cash/set routing basis required")
    pin = V.PINS[case]
    directory = CT.ROOT / pin.get("coverage_routing_dir", str((COVERAGE / f"inputs/{case}_final_routing").relative_to(CT.ROOT)))
    manifest = directory / "manifest.json"
    require(manifest.is_file(), f"selected {case} native routing receipt absent")
    receipt = json.loads(manifest.read_text())
    require(receipt.get("vintage") == f"{case}_final_routing"
            and set(receipt["files"]) == {"lines.json", "lines_cash.json"}, "selected routing receipt shape/case")
    for name, row in {**receipt["files"], "CASE_FINAL": receipt["adoption"]}.items():
        path = directory / name
        require(path.is_file() and path.stat().st_size == row["bytes"]
                and CT.digest(path) == row["sha256"], "stale selected routing source " + name)
    default_receipt = "final_routing_coverage_source.json" if case == "oct15" else f"{case}_final_routing_coverage_source.json"
    frozen = CT.ROOT / pin.get("coverage_source_receipt", str((COVERAGE / "inputs" / default_receipt).relative_to(CT.ROOT)))
    require(frozen.is_file(), f"selected {case} frozen coverage source receipt absent")
    return directory / ("lines_cash.json" if basis == "cash" else "lines.json"), frozen


def export(case="oct15", basis="cash"):
    start = time.perf_counter()
    donors, donor_receipt = CT.load_donors(case, basis)
    sys.path.insert(0, str(COVERAGE))
    import export_pricing as EP
    lines_path, frozen_source = routing_paths(case, basis)
    source = EP.SOURCE
    spec = importlib.util.spec_from_file_location("coverage_recipient_households", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # The source loader's guards and frozen-source receipt are the same as the
    # coverage constructor; only the return boundary and observation callback differ.
    module._coverage_frozen_source = lambda record: EP.frozen_coverage_source(
        frozen_source, record)
    V.ITEM_CLASS.update(V.offset_classes(case))
    V.receipt_contract(case)
    rows = []
    positions = None
    coverage_mass = None

    def eligible(row, s):
        if not (row["side"] == "spending" and row["response"] == 0 and row["amount_bn"] != 0
                and V.LINE_CLASS.get(row["id"], V.ITEM_CLASS.get(row["id"])) == "public_good"):
            return False
        carrier = s.get("completion", {}).get("carriers", {}).get(row["id"]) if s.get("completion") else None
        if carrier:
            # Inactive alternative carriers carry raw amounts but no service at
            # this specification. Native routing admits a line carrier only at
            # its declared active parent key and response; capital responds at 1.
            if carrier["kind"] != "line" or carrier["side"] != "spending":
                return False
            parent = s["row_of"]("spending", carrier["parent_line"])
            return parent["key"] == carrier["parent_key"] and parent["response"] == row["response"]
        return True

    def capture(s, driver, share):
        nonlocal positions, coverage_mass
        row = s["row"]
        if not eligible(row, s):
            return
        line = row["id"]
        cls = V.LINE_CLASS.get(line, V.ITEM_CLASS.get(line))
        if cls != "public_good":
            return
        if positions is None:
            frame_ids = pd.MultiIndex.from_frame(s["d"][["PH_SEQ", "PPPOS"]])
            positions = frame_ids.get_indexer(pd.MultiIndex.from_frame(donors[["PH_SEQ", "PPPOS"]]))
            require((positions >= 0).all(), "donor absent from canonical native frame")
            coverage_mass = np.zeros(len(s["d"]))
            coverage_mass[positions] = donors.coverage_weight.to_numpy()
            require(np.array_equal(s["age"][positions], donors.age.to_numpy()), "native donor ages differ")
        mask = s["m"]
        source_line = line
        carrier = s.get("completion", {}).get("carriers", {}).get(line) if s.get("completion") else None
        if carrier:
            require(carrier["kind"] in ("line", "capital"), "unknown public-good carrier kind")
            source_line = ("capital_" if carrier["kind"] == "capital" else "") + carrier["parent_line"]
        vector = np.where(mask, driver, 0.0)
        value = transport_price(vector, s["w0"], coverage_mass, row["amount_bn"] * share)
        rows.append(dict(case=case, basis=basis, end=s["end"], generation=s["g"].replace("G3plus", "G3+"),
                         line=source_line, source_line=line, cls=cls, recipient_value_bn=value,
                         fiscal_cost_bn=0.0, native_splits=1,
                         provenance="canonical routed_split before zero-response fiscal skip; exact exported central donor weights"))

    module._capture_zero_recipient = capture
    module._zero_recipient_row = eligible
    exec(compile(instrument(ast.parse(source.read_text())), str(source), "exec"), module.__dict__)
    module.FAILS.clear()
    module.main("row4", case=case, basis=basis, allocation="personal",
                lines_path=lines_path)
    require(not module.FAILS, "canonical construction guards failed " + repr(module.FAILS))
    frame = pd.DataFrame(rows)
    require(not frame.empty and "defense" in set(frame.line), "nonresponsive defense recipient cells absent")
    target = HERE / f"derived/coverage_recipient_supplement_{case}_{basis}.csv"
    frame.to_csv(target, index=False, float_format="%.17g", lineterminator="\n")
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    peak = require_within_budget("zero-response coverage recipient native construction")
    receipt = dict(case=case, basis=basis, donor_csv_sha256=donor_receipt["donor_csv_sha256"],
                   source_sha256=CT.digest(source), adapter_sha256=CT.digest(Path(__file__)),
                   csv_sha256=CT.digest(target), rows=len(frame),
                   native_lines_sha256=CT.digest(lines_path), frozen_source_receipt_sha256=CT.digest(frozen_source))
    target.with_suffix(".json").write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    print(json.dumps(dict(receipt, peak_physical_bytes=peak, elapsed_seconds=time.perf_counter() - start), indent=1))
    return frame


def supplement(I, case=None, basis="cash"):
    case = I["case"] if case is None else case
    target = HERE / f"derived/coverage_recipient_supplement_{case}_{basis}.csv"
    require(target.exists() and target.with_suffix(".json").exists(), "recipient export absent")
    record = json.loads(target.with_suffix(".json").read_text())
    lines_path, frozen_source = routing_paths(case, basis)
    require(record.get("native_lines_sha256") == CT.digest(lines_path)
            and record.get("frozen_source_receipt_sha256") == CT.digest(frozen_source), "native routing receipt changed")
    _, donor_record = CT.load_donors(case, basis)
    require(record["case"] == case and record["basis"] == basis, "case/basis mismatch")
    require(record["csv_sha256"] == CT.digest(target) and record["adapter_sha256"] == CT.digest(Path(__file__)),
            "stale recipient export")
    require(record["donor_csv_sha256"] == donor_record["donor_csv_sha256"], "donor receipt changed")
    require(record["source_sha256"] == CT.digest(COVERAGE.parent / "within_group_distribution_2026_09_29/households.py"),
            "canonical constructor changed")
    data = pd.read_csv(target, float_precision="round_trip")
    v = I["vgen"]
    extra = []
    for r in data.itertuples():
        row = dict(case=case, end=r.end, generation=r.generation, side="spending", line=r.line,
                   origin_line=f"coverage_recipient_only_{r.source_line}", cls=r.cls,
                   economic_payer="government_budget", receipt_incidence_class="not_receipt", amount_bn=0.0,
                   response=0.0, G_bn=0.0, net_cost_bn=0.0, third_party_bn=0.0,
                   source_tax_credit_bn=0.0, child_credit_other_residents_bn=0.0, group_credit_adjustment_bn=0.0)
        row.update({col: r.recipient_value_bn for col in ("V_low_bn", "V_central_bn", "V_high_bn")})
        extra.append(row)
    out = dict(I, vgen=pd.concat([v, pd.DataFrame(extra)], ignore_index=True))
    require(abs(out["vgen"].net_cost_bn.sum() - v.net_cost_bn.sum()) < 1e-10, "recipient supplement changed fiscal cost")
    out["coverage_recipient_supplement"] = record
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="oct15")
    parser.add_argument("--basis", default="cash", choices=("cash", "set"))
    args = parser.parse_args()
    export(args.case, args.basis)

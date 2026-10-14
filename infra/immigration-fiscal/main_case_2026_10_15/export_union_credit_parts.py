"""Retain exact side/generation terms from the unchanged joint-credit source.

The source publishes net generation deltas. Payload edits need their receipt
and spending pieces separately; capture those same account/owner arrays before
the source drops its per-arm state. No source writer is called or changed.
"""
from __future__ import annotations

import ast
import argparse
import contextlib
import gc
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SOURCE = FISCAL/"union_completion_2026_10_14/credits_interaction.py"
sys.path.insert(0, str(SOURCE.parent))
sys.path.insert(0, str(FISCAL/"scripts"))
from memory_budget import require_within_budget


class Capture(ast.NodeTransformer):
    def __init__(self):
        self.matches = 0

    def visit_Assign(self, node):
        if not (len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript)
                and isinstance(node.targets[0].value, ast.Name)
                and node.targets[0].value.id == "results"):
            return node
        self.matches += 1
        retain = ast.parse("""
r['by_generation_by_side'] = {
    name: {side_name: float(sum(
        s['account'](s['comp_ruled'][k] * s['owner'][k][g] * s['keep_of']('R3', k), k)[0]
        for k in keys if s['side'][k] == side_name))
        for side_name in ('receipts', 'spending')}
    for g, name in enumerate(credits.GENS)}
""").body
        # AST-executed functions use s as their __globals__, so every completed
        # arm otherwise retains its full account arrays in a dictionary/function
        # cycle until an unpredictable automatic collection. The result holds
        # only scalar/list exports; drop and collect that finished arm now.
        release = ast.parse("del s\ngc.collect()\n").body
        return retain+[node]+release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-existing", action="store_true",
                        help="require byte parity with the existing output before writing; regression gate for representation-only fixes")
    args = parser.parse_args()
    started = time.perf_counter()
    target = HERE/"derived/union_credit_parts.json"
    if args.check_existing and not target.is_file():
        raise SystemExit("[BLOCKED] byte-parity regression requires existing union_credit_parts.json")
    baseline = target.read_bytes() if args.check_existing else None
    spec = importlib.util.spec_from_file_location("union_credit_capture", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.gc = gc
    fn = next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute")
    adapter = Capture()
    fn = adapter.visit(fn)
    assert adapter.matches == 1, "[BLOCKED] joint-credit source capture boundary changed"
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(SOURCE), "exec"), module.__dict__)
    with contextlib.redirect_stdout(io.StringIO()):
        source = module.compute(include_siblings=True)
    out = {}
    canonical = source["results"]["canonical"]["by_generation_by_side"]
    for arm, r in source["results"].items():
        if arm == "canonical":
            continue
        sides = r["by_generation_by_side"]
        delta = {g: dict(receipt_edit_bn=-(sides[g]["receipts"]-canonical[g]["receipts"]),
                         spending_edit_bn=sides[g]["spending"]-canonical[g]["spending"])
                 for g in sides}
        assert abs(sum(v["receipt_edit_bn"] for v in delta.values())-r["delta_receipt_edit_bn"]) < 1e-12
        assert abs(sum(v["spending_edit_bn"] for v in delta.values())-r["delta_spending_edit_bn"]) < 1e-12
        for g, v in delta.items():
            assert abs(v["spending_edit_bn"]-v["receipt_edit_bn"]-(r["by_generation"][g]-source["results"]["canonical"]["by_generation"][g])) < 1e-12
        out[arm] = delta
    encoded = (json.dumps(dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                              units="bn; receipt_edit is signed raw target shift, spending_edit likewise",
                              results=out), indent=2)+"\n").encode("utf-8")
    gc.collect()
    # Gate before any output mutation: a failed build cannot replace its last
    # valid artifact, even when the computation itself completed successfully.
    peak = require_within_budget("union-completion credit generation parts")
    if baseline is not None and encoded != baseline:
        raise SystemExit("[BLOCKED] byte-parity regression: union_credit_parts.json would change "
                         f"({hashlib.sha256(baseline).hexdigest()} -> {hashlib.sha256(encoded).hexdigest()})")
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(encoded)
    print(json.dumps(dict(arms=len(out), elapsed_seconds=time.perf_counter()-started, peak_bytes=peak,
                          byte_parity="IDENTICAL" if baseline is not None else "not requested",
                          output_sha256=hashlib.sha256(encoded).hexdigest())))


if __name__ == "__main__":
    main()

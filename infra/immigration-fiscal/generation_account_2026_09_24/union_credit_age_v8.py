"""Actual owner-age capture of item10's joint-credit membership interaction.

Replays the principal computation without invoking its writer. Original P7
credit vintage stays frozen; only the expanded-minus-canonical term is exported.
"""
from __future__ import annotations

import ast
import contextlib
import gc
import hashlib
import importlib.util
import io
import json
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SOURCE = FISCAL / "union_completion_2026_10_14/credits_interaction.py"
PARTS = FISCAL / "main_case_2026_10_15/derived/union_credit_parts.json"
ARM = "one_us_parent_plus_observed"
GENS = ["G1", "G2", "G3plus"]
CELLS = [f"{g}_{age}" for g in GENS for age in ("adult", "minor")]
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def finite161(values):
    result = np.asarray(values, dtype=float)
    if result.shape != (161,) or not np.isfinite(result).all():
        raise ValueError("[BLOCKED] missing or nonfinite actual credit161 array")
    return result


def capture_age(s, keys):
    """Same source owner fractions with actual ages added to their dimensions."""
    age = s["d"].A_AGE.to_numpy()
    dependents, return_index, member = s["drows"], s["ri"], s["dmem"]
    dependent_gen = s["dgen"]
    head_gen = s["R"].gen_h.to_numpy()
    head_age = age[s["h"]]
    n = len(s["h"])
    fraction = np.stack([np.bincount(return_index, weights=member & (dependent_gen == g) &
                            ((age[dependents] >= 18) if adult else (age[dependents] < 18)), minlength=n)
                         for g in range(3) for adult in (True, False)]) / np.maximum(s["n_mem"], 1)
    head = np.stack([(head_gen == g) & ((head_age >= 18) if adult else (head_age < 18))
                     for g in range(3) for adult in (True, False)]).astype(float)
    totals = {side: np.zeros((6, 161)) for side in ("receipts", "spending")}
    for key in keys:
        owner = fraction if key.startswith(("A_", "C_")) else head
        for g in range(3):
            if not np.allclose(owner[2*g] + owner[2*g+1], s["owner"][key][g], atol=1e-12, rtol=0):
                raise ValueError(f"[BLOCKED] actual age owner does not preserve source generation {key}/{g}")
        for j in range(6):
            totals[s["side"][key]][j] += finite161(s["account"](
                s["comp_ruled"][key] * owner[j] * s["keep_of"]("R3", key), key))
    # Account's receipt side is a cost. Export its signed raw receipt edit.
    return {side: {cell: ((-1 if side == "receipts" else 1) * totals[side][j]).tolist()
                   for j, cell in enumerate(CELLS)} for side in totals}


class Capture(ast.NodeTransformer):
    def __init__(self):
        self.matches = self.loops = 0

    def visit_For(self, node):
        node = self.generic_visit(node)
        if isinstance(node.target, ast.Tuple) and [getattr(x, "id", None) for x in node.target.elts] == ["label", "extra"]:
            self.loops += 1
            node.iter = ast.parse("[('canonical', canonical & False), ('one_us_parent_plus_observed', extras['one_us_parent_plus_observed'])]", mode="eval").body
        return node

    def visit_Assign(self, node):
        if not (len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript)
                and isinstance(node.targets[0].value, ast.Name) and node.targets[0].value.id == "results"):
            return node
        self.matches += 1
        return ast.parse("r['actual_owner_age'] = capture_age(s, keys)").body + [node] + ast.parse("del s\ngc.collect()").body


def check_sources(hashes):
    if any(sha(p) != expected for p, expected in hashes.items()):
        raise ValueError("[BLOCKED] stale or changed actual-credit source")


def compute():
    paths = [Path(__file__), SOURCE, PARTS, FISCAL / "mixed_unit_credits_2026_10_14/credits.py",
             FISCAL / "mixed_unit_credits_2026_10_14/derived/item.json",
             FISCAL / "union_completion_2026_10_14/completion.py",
             HERE / "frame.py", FISCAL / "main_case_2026_10_15/derived/corrections.json"]
    # Admit the already pinned raw/weight/status/tax source graph. The credit
    # routing producer itself is not imported by this independent computation.
    pin_path = HERE / "inputs/credit_pins.json"
    pinned = json.loads(pin_path.read_text())
    for relative, expected in pinned.items():
        if relative == "generation_account_2026_09_24/credit_routing.py":
            continue
        path = FISCAL / relative
        if sha(path) != expected:
            raise ValueError(f"[BLOCKED] stale pinned actual-credit source {relative}")
        paths.append(path)
    paths.append(pin_path)
    hashes = {str(p): sha(p) for p in paths}
    principal = json.loads(PARTS.read_text())["results"][ARM]
    spec = importlib.util.spec_from_file_location("actual_union_credit_age", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.capture_age, module.gc = capture_age, gc
    fn = next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute")
    adapter = Capture()
    fn = adapter.visit(fn)
    if adapter.matches != 1 or adapter.loops != 1:
        raise ValueError("[BLOCKED] principal credit capture anchors changed")
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(SOURCE), "exec"), module.__dict__)
    with contextlib.redirect_stdout(io.StringIO()):
        result = module.compute(include_siblings=True)
    canonical = result["results"]["canonical"]["actual_owner_age"]
    expanded = result["results"][ARM]["actual_owner_age"]
    delta = {side: {cell: (finite161(expanded[side][cell])-finite161(canonical[side][cell])).tolist()
                    for cell in CELLS} for side in canonical}
    gaps = []
    for g in GENS:
        source = principal["G3+" if g == "G3plus" else g]
        for side, field in (("receipts", "receipt_edit_bn"), ("spending", "spending_edit_bn")):
            value = delta[side][f"{g}_adult"][0] + delta[side][f"{g}_minor"][0]
            gap = abs(value-source[field])
            if gap >= 1e-9:
                raise ValueError(f"[BLOCKED] actual age delta disagrees with principal {g}/{side}: {gap}")
            gaps.append(dict(generation=g, side=side, gap_bn=gap, tolerance_bn=1e-9))
    for r in range(161):
        net = sum(delta["spending"][cell][r]-delta["receipts"][cell][r] for cell in CELLS)
        if abs(net-result["results"][ARM]["replicate_delta_bn"][r]) >= 1e-9:
            raise ValueError("[BLOCKED] actual age source joint161 closure")
    check_sources(hashes)
    return dict(version=1, units="bn signed raw receipt/spending edit; central plus160 genuine SDR replicates",
                arm=ARM, source_sha256=hashes, canonical=canonical, expanded=expanded,
                expanded_minus_canonical=delta, gates=gaps,
                vintage="Original P7 credit vintage; actual-age source owner split of item10 interaction only",
                rule="R3: A/C equal member-dependent owners; B/Cr actual head; six ages collapse exact source generations",
                uncertainty="Source sampling conditional on frozen original credit model; no baseline/coverage/loss uncertainty added")


def publish(result, target, budget_check=require_within_budget):
    check_sources(result["source_sha256"])
    for side in ("receipts", "spending"):
        for cell in CELLS:
            finite161(result["expanded_minus_canonical"][side][cell])
    budget_check("actual union-credit interaction owner age")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main():
    start = time.perf_counter()
    result = compute()
    target = HERE / "derived/union_credit_age_oct15.json"
    publish(result, target)
    print(json.dumps(dict(output_sha256=sha(target), elapsed_seconds=time.perf_counter()-start,
                          peak_rss_diagnostic=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          physical_peak_bytes=require_within_budget("actual union credit timing"))))


if __name__ == "__main__":
    main()

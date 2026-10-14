#!/usr/bin/env python3
"""Recompute frozen item 5b at changed membership, without modifying its lane.

AST selection reuses the main's computation, ending before writes. Baseline
identities run first. Expansion repeats the live rules and cell coverage gates;
the old union's published-share identity is baseline-only. The national keys,
weights, status rules and original 3.04M lineage item remain fixed.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import resource
import sys
import time
from pathlib import Path

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parent / "mixed_unit_credits_2026_10_14/credits.py"
ITEM = SOURCE.parent / "derived/item.json"
SOURCE_SHA = "d41e16a5fdce5dfcc141aa8c6c11dde9842c614ee185f70b84ecfa2b89782481"
ITEM_SHA = "2773e34d4cb02a70dd21544f915b2b83bbdc00855d24d468ed67e81e0310b5ac"
sys.dont_write_bytecode = True


def _block(nodes, state):
    module = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    exec(compile(module, str(SOURCE), "exec"), state)


def _is_call_assignment(node, name):
    return (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name) and node.value.func.id == name)


def _is_named_gate(node, name):
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name) and node.value.func.id == "gate"
            and node.value.args and isinstance(node.value.args[0], ast.Constant)
            and node.value.args[0].value == name)


def _observed_sibling_masks(d, canonical, civ, one_us_parent, all_outsiders, credits):
    """Use the lane's exact biological sibling universe and existing parent linker."""
    sys.path.insert(0, str(LANE))
    from completion import siblings
    frame = credits.by_path(LANE.parent / "generation_account_2026_09_24/frame.py", "union_credit_frame")
    arms, mexican_origin, _parents = siblings(d, frame, civ, canonical)
    observed = arms["biological"] & ~mexican_origin
    return {"observed_biological_siblings": observed,
            "one_us_parent_plus_observed": one_us_parent | observed,
            "all_outsiders_plus_observed": all_outsiders | observed}


def compute(extra_masks=None, include_siblings=False):
    """Return exact baseline/expansion interactions and all 161 replicate totals.

    Optional extra_masks(d, canonical_union, civilian) returns a mapping of arm
    names to additional-person boolean arrays on sorted CPS PH_SEQ/PPPOS. This
    permits directly observed nonreporting sibling masks without reraking weights.
    """
    start = time.perf_counter()
    spec = importlib.util.spec_from_file_location("union_credit_source", SOURCE)
    credits = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(credits)
    credits.gate("union_interaction_credits_source_hash_is_pinned",
                 hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA)
    credits.gate("union_interaction_frozen_item_hash_is_pinned",
                 hashlib.sha256(ITEM.read_bytes()).hexdigest() == ITEM_SHA)
    if include_siblings:
        credits.PERSON = [*credits.PERSON, "PEPAR1TYP", "PEPAR2TYP"]
    main = next(n for n in ast.parse(SOURCE.read_text()).body
                if isinstance(n, ast.FunctionDef) and n.name == "main")
    first = next(i for i, n in enumerate(main.body) if _is_call_assignment(n, "returns"))
    last = next(i for i, n in enumerate(main.body)
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "terms" for t in n.targets))
    assert first < last, "[BLOCKED] frozen main computation anchors changed"
    body = main.body[first:last + 1]
    state = dict(vars(credits))
    _block(main.body[:first], state)
    canonical, civ, d = state["union"].copy(), state["civ"], state["d"]
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    outside = civ & native & d.PRDTHSP.eq(1).to_numpy() & ~canonical
    us = [57, 60, 66, 69, 73, 78]
    one = d.PEFNTVTY.isin(us).to_numpy() | d.PEMNTVTY.isin(us).to_numpy()
    extras = {"one_us_parent": outside & one, "all_outsiders": outside}
    if include_siblings:
        extras.update(_observed_sibling_masks(d, canonical, civ, extras["one_us_parent"],
                                             extras["all_outsiders"], credits))
    if extra_masks is not None:
        supplied = extra_masks(d, canonical.copy(), civ.copy())
        assert not set(supplied) & set(extras), "[BLOCKED] extra mask replaces a specified arm"
        extras.update(supplied)
    for name, extra in extras.items():
        assert extra.shape == canonical.shape and extra.dtype == bool, f"[BLOCKED] mask shape/type: {name}"
        assert not (extra & canonical).any(), f"[BLOCKED] duplicate canonical member: {name}"
        assert not (extra & ~civ).any(), f"[BLOCKED] noncivilian addition: {name}"
    frozen = json.loads(ITEM.read_text())
    results, vectors = {}, {}
    for label, extra in [("canonical", canonical & False), *extras.items()]:
        s = dict(state)
        s["union"] = canonical | extra
        s["gen"] = state["gen"].copy()
        s["gen"][extra] = 2
        nodes = body if label == "canonical" else [n for n in body if not _is_named_gate(
            n, "published_refundable_key_share_is_model_jsons")]
        gate_start = len(credits.GATES)
        with contextlib.redirect_stdout(io.StringIO()):
            _block(nodes, s)
        keys = [k for k in s["comp"] if k.startswith(("A_", "B_", "C_", "Cr_"))]
        by_side = {side: sum(s["account"](s["comp_ruled"][k] * s["keep_of"]("R3", k), k)
                           for k in keys if s["side"][k] == side)
                   for side in ("receipts", "spending")}
        total = by_side["receipts"] + by_side["spending"]
        by_gen = {name: float(sum(s["account"](s["comp_ruled"][k] * s["owner"][k][g]
                              * s["keep_of"]("R3", k), k)[0] for k in keys))
                  for g, name in enumerate(credits.GENS)}
        by_component = {k: float(s["account"](s["comp_ruled"][k] * s["keep_of"]("R3", k), k)[0])
                        for k in keys}
        assert abs(sum(by_gen.values()) - total[0]) < 1e-12
        assert abs(sum(by_component.values()) - total[0]) < 1e-12
        vectors[label] = total
        r = dict(net_bn=float(total[0]), se_bn=credits.sdr(total),
                 receipt_edit_bn=-float(by_side["receipts"][0]),
                 spending_edit_bn=float(by_side["spending"][0]),
                 by_generation=by_gen, by_component=by_component,
                 union_count=float(s["W"][s["union"], 0].sum()),
                 added_count=float(s["W"][extra, 0].sum()), added_records=int(extra.sum()),
                 households_with_added_people=int(d.loc[extra, "PH_SEQ"].nunique()),
                 replicate_net_bn=total.tolist(),
                 gates=credits.GATES[gate_start:])
        if label == "canonical":
            assert abs(total[0] - frozen["net_bn"]["personal"]) < 1e-9
            for name, got in by_gen.items():
                key = "G3plus" if name == "G3+" else name
                assert abs(got - frozen["by_generation"][key]["personal"]) < 1e-9
            receipt = next(e for e in frozen["edits"] if e["side"] == "receipt")["by"]["personal"]
            spending = next(e for e in frozen["edits"] if e["side"] == "spending")["by"]["personal"]
            assert abs(r["receipt_edit_bn"] - receipt) < 1e-9
            assert abs(r["spending_edit_bn"] - spending) < 1e-9
            for part in frozen["parts"].values():
                generation = "G3+" if part["generation"] == "G3plus" else part["generation"]
                g = credits.GENS.index(generation)
                side = "receipts" if part["side"] == "receipt" else "spending"
                term_keys = [k for k in keys if k.startswith(part["term"] + "_") and s["side"][k] == side]
                got = sum(s["account"](s["comp_ruled"][k] * s["owner"][k][g]
                                      * s["keep_of"]("R3", k), k)[0] for k in term_keys)
                assert abs(got - part["cost_bn"]) < 1e-9, "[BLOCKED] canonical part control failed"
            r["positive_control_tolerance_bn"] = 1e-9
            r["positive_control_parts"] = len(frozen["parts"])
            baseline_per_return = {k: s["comp_ruled"][k] * s["keep_of"]("R3", k) for k in keys}
            baseline_return_rows = s["h"].copy()
        else:
            delta = total - vectors["canonical"]
            assert (s["h"] == baseline_return_rows).all(), "[BLOCKED] return-order drift"
            changed = s["h"] < 0
            for k in keys:
                changed |= abs(s["comp_ruled"][k] * s["keep_of"]("R3", k) - baseline_per_return[k]) > 1e-9
            r.update(delta_bn=float(delta[0]), delta_se_bn=credits.sdr(delta),
                     replicate_delta_bn=delta.tolist(),
                     delta_receipt_edit_bn=r["receipt_edit_bn"] - results["canonical"]["receipt_edit_bn"],
                     delta_spending_edit_bn=r["spending_edit_bn"] - results["canonical"]["spending_edit_bn"],
                     returns_with_changed_interaction=int(changed.sum()),
                     households_with_changed_interaction=int(d.iloc[s["h"][changed]].PH_SEQ.nunique()))
            assert abs(r["delta_spending_edit_bn"] - r["delta_receipt_edit_bn"] - r["delta_bn"]) < 1e-12
        results[label] = r
        print(label, "net", round(r["net_bn"], 9), "delta", round(r.get("delta_bn", 0), 9), flush=True)
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak_rss if sys.platform == "darwin" else peak_rss * 1024
    credits.gate("union_interaction_peak_rss_below_2p5_gib", peak_bytes < 2.5 * 1024 ** 3)
    return dict(reading="R3_with_status", scope="identified union interaction; original lineage item held fixed",
                sets="same current-year edits in set and cash, both ends at personal allocation",
                delta_se_rule="4/160 times squared replicate differences; paired expanded minus canonical",
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                item_sha256=hashlib.sha256(ITEM.read_bytes()).hexdigest(), results=results,
                baseline_gates=credits.GATES[:len(credits.GATES) - 1 - sum(len(v["gates"]) for v in results.values())],
                memory_limit_gate=credits.GATES[-1],
                timing=dict(seconds=time.perf_counter() - start,
                            peak_rss_bytes=peak_bytes))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=LANE / "derived")
    parser.add_argument("--include-siblings", action="store_true",
                        help="include directly observed biological nonreporters alone and with each outsider arm")
    args = parser.parse_args()
    output = compute(include_siblings=args.include_siblings)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    # Runtime and peak RSS are execution evidence, not deterministic derived bytes.
    timing = output.pop("timing")
    (args.out_dir / "credits_interaction.json").write_text(json.dumps(output, indent=2) + "\n")
    print("timing", timing, flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Measure item-11's original-unit dollar footprint containing item-10 people.

Reuse the pinned source kernels without changing their populations, denominators,
policy parameters, or source files. AST hooks observe full-sample unit flows before
aggregation. Independent child processes keep each physical footprint below 2.5GB.
The household footprint is a conservative superset of tax/SPM-unit intersections.
It is an interaction exposure bound, not a joint membership counterfactual solve.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import zipfile

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
MIXED = FISCAL / "mixed_unit_removal_2026_10_14"
CONTROL = FISCAL / "mixed_unit_credits_2026_10_14"
COMPLETION = FISCAL / "union_completion_2026_10_14"
START = time.perf_counter()
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget


def require(ok, name):
    if not ok:
        raise RuntimeError("[BLOCKED] mixed overlap: " + name)


def guard(event, args):
    if event == "open":
        target, mode, flags = args
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing and isinstance(target, (str, bytes, os.PathLike)):
            require(Path(target).resolve().is_relative_to(HERE), "write outside v8: " + str(target))
    if event == "socket.connect":
        raise RuntimeError("[BLOCKED] source acquisition forbidden in overlap probe")


sys.addaudithook(guard)


def module(file, name):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def adapted(mod, function, hook, match, before=False):
    """Install exactly one AST observation hook in the named source function."""
    tree = ast.parse(Path(mod.__file__).read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function)
    hits = []

    class Observe(ast.NodeTransformer):
        def visit_Assign(self, node):
            node = self.generic_visit(node)
            if match(node):
                hits.append(node.lineno)
                call = ast.parse("_overlap_hook(locals())").body[0]
                return [call, node] if before else [node, call]
            return node

    fn = Observe().visit(fn)
    require(len(hits) == 1, f"AST anchor {function}: {hits}")
    mod._overlap_hook = hook
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(mod.__file__), "exec"), mod.__dict__)
    return hits[0]


def is_target(node, name):
    return any(isinstance(t, ast.Name) and t.id == name for t in node.targets)


def load_frame():
    c = module(CONTROL / "credits.py", "overlap_credits")
    d = c.load()
    civ, union, gen = c.groups(d)
    W, _, _ = c.row4_weights(d, civ, union)
    d = d.drop(columns=c.REPS[1:])
    return c, d, civ, union, gen, W


def augment(d, c, extras):
    missing = [k for k in extras if k not in d]
    if not missing:
        return d
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        available = pd.read_csv(z.open("pppub25.csv"), nrows=0).columns
        fields = [k for k in missing if k in available]
        extra = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS"] + fields)
    result = d.merge(extra, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    require(len(result) == len(d) and result[fields].notna().all().all(), "source-key join incomplete")
    return result


def completion_mask(d, c, civ, union, W):
    # Call the exact masks/siblings source functions; supply its canonical frame API.
    sys.path.insert(0, str(COMPLETION))
    co = module(COMPLETION / "completion.py", "overlap_completion")
    h = module(FISCAL / "within_group_distribution_2026_09_29/households.py", "overlap_households")
    d = augment(d, c, ["PEPAR1TYP", "PEPAR2TYP"])
    cv, un, _, _, central, _, _ = co.masks(d, h.F)
    require(np.array_equal(cv, civ) and np.array_equal(un, union), "completion/mixed canonical membership differs")
    arms, mex, _ = co.siblings(d, h.F, civ, union)
    children = arms["biological"] & ~mex
    mask = central | children
    counts = {name: {"records": int(m.sum()), "people": float(W[m, 0].sum())} for name, m in [("reporters", central), ("children", children), ("all", mask)]}
    require(counts["reporters"]["records"] == 204, "central reporter record count differs")
    require(abs(counts["reporters"]["people"] - 456936) < 1, "central reporter people count differs")
    hh, labels = pd.factorize(d.PH_SEQ, sort=False)
    affected = np.bincount(hh, weights=mask, minlength=len(labels)) > 0
    spm, spmlabels = pd.factorize(d.SPM_ID, sort=False)
    affected_spm = np.bincount(spm, weights=mask, minlength=len(spmlabels)) > 0
    counts.update(households=int(affected.sum()), spm_units=int(affected_spm.sum()),
                  original_union_people_in_affected_households=float(W[union & affected[hh], 0].sum()))
    return d, mask, hh, affected, counts


class Collect:
    def __init__(self, d, hh, affected):
        self.d, self.hh, self.affected = d, hh, affected
        self.events = {}

    def add(self, name, values, rows=None):
        codes = self.hh if rows is None else self.hh[np.asarray(rows, int)]
        self.events[name] = np.bincount(codes, weights=np.asarray(values), minlength=len(self.affected))

    def record(self, name):
        values = self.events[name]
        return {"global_bn": float(values.sum()), "overlap_bn": float(values[self.affected].sum()),
                "overlap_absolute_household_bn": float(np.abs(values[self.affected]).sum())}


@contextlib.contextmanager
def trace_return(fn, callback):
    def profile(frame, event, arg):
        if event == "return" and frame.f_code is fn.__code__ and arg is not None:
            callback(frame.f_locals)
    sys.setprofile(profile)
    try:
        yield
    finally:
        sys.setprofile(None)


def context():
    c = module(CONTROL / "credits.py", "overlap_tax_credits")
    tree = ast.parse((CONTROL / "credits.py").read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    cut = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
           and isinstance(n.value.func, ast.Attribute) and isinstance(n.value.func.value, ast.Name)
           and n.value.func.value.id == "OUT" and n.value.func.attr == "mkdir"]
    require(len(cut) == 1, "credits output boundary changed")
    fn.body = fn.body[:cut[0]] + ast.parse("return locals()").body
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(CONTROL / "credits.py"), "exec"), c.__dict__)
    x = c.main()
    m = module(MIXED / "removal.py", "overlap_removal")
    d = m.add_fields(x["d"], c)
    d = augment(d, c, ["PEPAR1TYP", "PEPAR2TYP"])
    x["d"] = d
    return c, m, x, d


def tax_part():
    c, m, x, d = context()
    print("[tax] source context ready", time.perf_counter() - START, file=sys.stderr, flush=True)
    d, mask, hh, affected, counts = completion_mask(d, c, x["civ"], x["union"], x["W"])
    x["d"] = d
    col = Collect(d, hh, affected)
    case = json.loads((MIXED / "derived/case_inputs.json").read_text())
    membership = module(MIXED / "membership.py", "overlap_membership")
    current = ["union"]
    tax_cache = {}
    original_loader = m.load_module

    def cached_kernel(mod):
        original = mod.run_taxsim

        def run(frame):
            key = hashlib.sha256(frame.to_numpy().tobytes() + repr(tuple(frame.columns)).encode()).hexdigest()
            if key not in tax_cache:
                tax_cache[key] = original(frame)
            return tax_cache[key].copy(deep=True)
        mod.run_taxsim = run
        return mod

    def loader(file, name):
        mod = original_loader(file, name)
        return cached_kernel(mod) if Path(file).name == "state_tax.py" else mod
    m.load_module = loader

    def federal(v):
        # Exact net flow before generation aggregation; aggregate to original household.
        h, own = v["h"], v["own_safe"]
        af = v["after_f"] * v["ownW"][:, 0] * v["fit_line"] / v["mass"][0]
        bf = v["before_f"] * v["oldW"][:, 0] * v["fit_line"] / v["mass"][0]
        cr_after = v["after_cr"] * v["ownW"][:, 0] * x["per_ref"][0]
        cr_before = v["before_cr"] * v["oldW"][:, 0] * x["per_ref"][0]
        f = np.bincount(hh[own], weights=af, minlength=len(affected)) - np.bincount(hh[h], weights=bf, minlength=len(affected))
        r = np.bincount(hh[h], weights=cr_before, minlength=len(affected)) - np.bincount(hh[own], weights=cr_after, minlength=len(affected))
        item = {"receipts": np.zeros(len(affected)), "spending": np.zeros(len(affected))}
        for k, value in x["comp_ruled"].items():
            if k.startswith("D_"):
                continue
            flow = value * x["owner"][k].sum(axis=0) * x["keep_of"]("R3", k)
            calibrated = flow * (x["per_fit"] if x["side"][k] == "receipts" else x["per_ref"][0]) * x["wr"][:, 0]
            item[x["side"][k]] += np.bincount(hh[x["h"]], weights=calibrated, minlength=len(affected))
        col.events[current[0] + "_federal"] = f - item["receipts"]
        col.events[current[0] + "_refunds"] = r - item["spending"]

    with trace_return(m.federal_removal, federal):
        fed = m.federal_removal(c, x, d)
    print("[tax] union federal ready", time.perf_counter() - START, file=sys.stderr, flush=True)
    st = cached_kernel(module(MIXED / "state_tax.py", "overlap_state"))

    def state(v):
        vals = v["difference"][:, 0] * v["conversion"][0]
        col.add(current[0] + "_state", vals, v["h"][v["scope"]])

    def run_state(y, f):
        with trace_return(st.compute, state):
            return st.compute(y["d"], y["R"], y["P"], y["base"], y["W"], y["union"], y["gen"], y["flag"], y["onbooks"], y["model"], civ=y["civ"],
                              refiling={"own": f["own"], "dep_counts": f["counts"], "R": f["afterR"], "owner": f["owner"], "before_input": f["before_input"], "after_input": f["after_input"]})
    run_state(x, fed)
    print("[tax] union state ready", time.perf_counter() - START, file=sys.stderr, flush=True)
    y, _ = membership.expanded_context(c, x, d, case, latent_only=True)
    current[0] = "expanded"
    with trace_return(m.federal_removal, federal):
        ef = m.federal_removal(c, y, y["d"])
    print("[tax] expanded federal ready", time.perf_counter() - START, file=sys.stderr, flush=True)
    run_state(y, ef)
    print("[tax] expanded state ready", time.perf_counter() - START, file=sys.stderr, flush=True)
    latent = membership.latent_mask(d, x["union"], x["civ"])
    _, _, links = membership.biological_children(d, x["union"], x["civ"])
    parentgen = np.stack([np.where(rows >= 0, x["gen"][np.maximum(rows, 0)], -1) for rows in links])
    third = latent & (parentgen == 1).any(axis=0)
    roster_g3 = latent.astype(float) - case["lineage"]["c3"]["value"] * third
    old_g3 = sum(float((val * x["owner"][k][2] * x["keep_of"]("R3", k)
                       * (x["per_fit"] if x["side"][k] == "receipts" else x["per_ref"][0])) @ x["wr"][:, 0])
                 for k, val in x["comp_ruled"].items() if not k.startswith("D_"))
    projection = -old_g3 * roster_g3 * x["W"][:, 0] / case["lineage"]["counts"]["identified_g3plus"]
    col.add("projection", projection)
    col.events["M6_biological_children"] = sum(col.events["expanded_" + k] - col.events["union_" + k] for k in ["federal", "refunds", "state"]) + col.events["projection"]
    for src, dest in [("union_federal", "M1_federal"), ("union_refunds", "M3_refunds"), ("union_state", "M2_state")]:
        col.events[dest] = col.events[src]
    keys = ["M1_federal", "M2_state", "M3_refunds", "M6_biological_children"]
    return {"counts": counts, "components": {k: col.record(k) for k in keys}}


def resource_part():
    c, m, x, d = context()
    d, _, hh, affected, counts = completion_mask(d, c, x["civ"], x["union"], x["W"])
    x["d"] = d
    col = Collect(d, hh, affected)
    resource_mod = module(MIXED / "resource_keys.py", "overlap_resources")
    case = json.loads((MIXED / "derived/case_inputs.json").read_text())
    own, *_ = m.disposable_income(d, x["R"], x["P"])

    def hook(v):
        if v["r"] != 0:
            return
        line = v["line"]
        event = (v["new"] - v["value"]) * v["w"] * v["civ"] * (v["gen"] >= 0) / v["group"] * line["union_target_bn"] * (-1 if line["side"] == "receipt" else 1)
        col.add(v["name"], event)
    adapted(resource_mod, "compute", hook, lambda n: is_target(n, "move"))
    result = resource_mod.compute(d, x, case, own)
    mapping = {"modeled_owner_property": "M5_owner_property", "housing_subsidies": "M5_housing_key"}
    comps = {}
    for key, name in mapping.items():
        if key == "modeled_owner_property":
            responses = [next(v["response"] for v in e["receipts"] if v["id"] == key) for e in case["evaluated"]["set"]]
            require(responses[0] == responses[1], "owner property source endpoints differ")
            col.events[key] *= responses[0]
        comps[name] = col.record(key)
        expected = result["terms"][key][:, 0].sum() * (responses[0] if key == "modeled_owner_property" else 1)
        require(abs(comps[name]["global_bn"] - expected) < 1e-9, "resource global parity")
    return {"counts": counts, "components": comps}


def consumption_part():
    c, m, x, d = context()
    d, _, hh, affected, counts = completion_mask(d, c, x["civ"], x["union"], x["W"])
    x["d"] = d
    col = Collect(d, hh, affected)
    case = json.loads((MIXED / "derived/case_inputs.json").read_text())

    # completion's households import legitimately loads the generation frame as
    # plain `frame`; consumption's outside checker requires its own module.
    # Bind the principal explicitly, then check its authoritative cache path.
    bench = FISCAL / "external_benchmarks_2026_09_24"
    module(bench / "frame.py", "frame")
    require(Path(sys.modules["frame"].__file__).resolve() == (bench / "frame.py").resolve(), "outside-check frame binding")

    def hook(v):
        if v["r"] != 0 or v["name"] != "own_disposable":
            return
        pos = v["pos"]
        event_raw = (v["new"] - v["old"]) * v["wr"] * v["civ"] * (v["gen"] >= 0)
        nat = v["old"][v["civ"]] @ v["wr"][v["civ"]]
        masses = np.bincount(v["cbo_code"], weights=v["old"] * v["wr"] * v["civ"], minlength=len(v["cbo_targets"]))
        per = np.divide(v["cbo_targets"], masses, out=np.zeros_like(masses), where=masses != 0)
        total = np.zeros(len(d))
        for lid, line in case["lines"].items():
            if lid == "excise_selective_sales":
                raw = (line["national_bn"] - v["F"]) * v["base_group"] + v["F"] * v["base_cbo"]
                move = (line["national_bn"] - v["F"]) * event_raw / nat + v["F"] * event_raw * per[v["cbo_code"]]
            else:
                raw = line["national_bn"] * v["base_group"]
                move = line["national_bn"] * event_raw / nat
            total += -move * line["union_target_bn"] / raw
        col.add("M5_consumption", total, pos)
    adapted(m, "consumption_removal", hook, lambda n: isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == "consumption_exposure")
    result = m.consumption_removal(c, x, d, case)
    require(abs(col.record("M5_consumption")["global_bn"] - result["M5"][:, 0].sum()) < 1e-9, "consumption global parity")
    return {"counts": counts, "components": {"M5_consumption": col.record("M5_consumption")}}


def benefit_part(kind):
    c, d, civ, union, gen, W = load_frame()
    m = module(MIXED / "removal.py", "overlap_benefit_removal")
    mod = module(MIXED / ("health.py" if kind == "health" else "snap_arm.py"), "overlap_benefit")
    extras = mod.EXTRA if kind == "health" else []
    d = m.add_fields(d, c)
    d = augment(d, c, extras + ["PEPAR1TYP", "PEPAR2TYP"])
    d, _, hh, affected, counts = completion_mask(d, c, civ, union, W)
    membership = module(MIXED / "membership.py", "overlap_benefit_membership")
    departure = union | membership.latent_mask(d, union, civ)
    col = Collect(d, hh, affected)
    captured = []
    if kind == "health":
        original = mod.attribute

        def attribute(person_change, data, weights, member, generation):
            event = person_change[:, 0] * weights[:, 0] / 1e9
            name = f"event_{len(captured)}"
            col.add(name, event)
            captured.append(name)
            return original(person_change, data, weights, member, generation)
        mod.attribute = attribute
        result = mod.compute(d, W, union, gen, {"civ": civ, "removal_mask": departure})
        require(len(captured) == 6, "health attribution hook count changed")
        names = {"Medicaid_low": 0, "Medicaid_high": 1, "ACA_low": 4, "ACA_high": 5}
        out = {name: col.record(captured[i]) for name, i in names.items()}
        for name in out:
            require(abs(out[name]["global_bn"] - result[name][:, 0].sum()) < 1e-9, "health global parity " + name)
    else:
        original_loader = mod.load

        def loader(file, name):
            b = original_loader(file, name)
            original = b.attribute

            def attribute(change, unit, weights, member, generation, mixed):
                event = change[:, 0] * mixed
                # Every SPM belongs to one household; use its first person row.
                first = np.unique(unit, return_index=True)[1]
                name = f"event_{len(captured)}"
                col.add(name, event, first)
                captured.append(name)
                return original(change, unit, weights, member, generation, mixed)
            b.attribute = attribute
            return b
        mod.load = loader
        # The source SNAP main reads the same stored engine model as credits.
        model = json.loads(c.MODEL.read_text())
        result = mod.compute(d, W, departure, np.where(departure & ~union, 2, gen), civ, model, baseline_union=union)
        require(len(captured) == 10, "SNAP attribution hook count changed")
        names = {"SNAP_zero_observed_high_takeup": 1, "SNAP_cap_observed_low_takeup": 5}
        out = {name: col.record(captured[i]) for name, i in names.items()}
        for name in out:
            require(abs(out[name]["global_bn"] - result["terms"][name][:, 0].sum()) < 1e-9, "SNAP global parity " + name)
    return {"counts": counts, "components": out}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=["tax", "resources", "consumption", "health", "snap"])
    parser.add_argument("--jobs", type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    if args.part:
        with contextlib.redirect_stdout(sys.stderr):
            result = {"tax": tax_part, "resources": resource_part, "consumption": consumption_part,
                      "health": lambda: benefit_part("health"), "snap": lambda: benefit_part("snap")}[args.part]()
        peak = require_within_budget("mixed overlap " + args.part)
        print(json.dumps({"part": args.part, "seconds": time.perf_counter() - START, "peak_footprint_bytes": peak,
                          "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), file=sys.stderr)
        print(json.dumps(result, allow_nan=False))
        return
    components, parts = {}, {}
    reference_counts = None
    def run_part(part):
        print("[overlap] " + part, file=sys.stderr, flush=True)
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--part", part], capture_output=True, text=True, check=False)
        require(run.returncode == 0, f"{part} exited {run.returncode}: {run.stderr[-4000:]}")
        for line in run.stderr.splitlines():
            if line.startswith('{"part":'):
                print(line, file=sys.stderr, flush=True)
        return part, json.loads(run.stdout)
    # These processes read immutable source caches; their independent kernels
    # each enforce the canonical footprint budget. Preserve input ordering in
    # the resulting artifact even when completion order differs.
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for part, value in pool.map(run_part, ["tax", "resources", "consumption", "health", "snap"]):
            if reference_counts is None:
                reference_counts = value["counts"]
            require(value["counts"] == reference_counts, "component frames disagree on intersection records/counts")
            components.update(value["components"])
            parts[part] = {k: v for k, v in value.items() if k != "components"}
    source = json.loads((MIXED / "derived/round2_summary.json").read_text())
    for name, v in components.items():
        expected = next(r for r in source["results"] if r["method"] == "set" and r["end"] == "low" and r["component"] == name)
        if name.startswith(("Medicaid", "ACA", "SNAP")):
            # Those saved one-change rows use union departures; this footprint uses
            # latent departures, as selected in the bounded stack.
            continue
        require(abs(v["global_bn"] - expected["bn"]) < 1e-8, "source component global mismatch " + name)
    fixed = ["M1_federal", "M2_state", "M3_refunds", "M6_biological_children", "M5_consumption", "M5_owner_property", "M5_housing_key"]
    readings = {}
    for reading, health, snap in [("low", "low", "SNAP_zero_observed_high_takeup"), ("high", "high", "SNAP_cap_observed_low_takeup")]:
        names = fixed + ["Medicaid_" + health, "ACA_" + health, snap]
        rows = [components[n] for n in names]
        total = next(r["bn"] for r in source["results"] if r["method"] == "set" and r["end"] == reading and r["component"] == "bounded_" + reading)
        d = next(r["bn"] for r in source["results"] if r["method"] == "set" and r["end"] == reading and r["component"] == "D_added_residual")
        require(abs(sum(v["global_bn"] for v in rows) + d - total) < 1e-8, "bounded stack global parity " + reading)
        signed = sum(v["overlap_bn"] for v in rows)
        absolute = sum(v["overlap_absolute_household_bn"] for v in rows)
        readings[reading] = {"signed_observed_overlap_bn": signed, "observed_absolute_component_household_bound_bn": absolute,
                             "share_of_item11_absolute_bound": absolute / total,
                             "unlocated_D_residual_bn": d, "including_all_unlocated_D_conservative_bn": absolute + abs(d),
                             "components": names, "item11_total_bn": total}
    pins = {}
    for p in [Path(__file__), MIXED / "round2.py", MIXED / "removal.py", MIXED / "membership.py", MIXED / "resource_keys.py", MIXED / "state_tax.py", MIXED / "health.py", MIXED / "snap_arm.py", MIXED / "benefits.py", CONTROL / "credits.py", COMPLETION / "completion.py", MIXED / "derived/round2_summary.json"]:
        pins[str(p.relative_to(FISCAL.parent.parent))] = hashlib.sha256(p.read_bytes()).hexdigest()
    result = {"status": "computed", "quantity": "Original-unit item-11 dollar footprint containing central item-10 people; conservative household superset of tax/SPM units",
              "interpretation": "Interaction exposure bound, not a joint-counterfactual estimate; full populations, calibrations, donor cells and policy assumptions fixed",
              "counts_by_part": parts, "by_reading": readings, "components": components, "source_sha256": pins,
              "limitations": ["absolute bound sums absolute component-by-household contributions; cancellations retained only in signed footprint", "unlocated residual D has no observed person/unit crosswalk; include all its magnitude for the conservative bound", "SNAP allocation key and its matching baseline interaction cancel exactly; neither is separately added"]}
    out = HERE / "derived/mixed_overlap.json"
    require_within_budget("mixed overlap coordinator")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"seconds": time.perf_counter() - START, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), file=sys.stderr)
    print(json.dumps(readings, indent=2))


if __name__ == "__main__":
    main()

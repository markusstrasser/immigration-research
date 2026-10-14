#!/usr/bin/env python3
"""Replay the frozen source to scratch and export its exact CPS sufficient statistics.

The return-event observer reads locals; it does not alter the imported source or
its calculations. All frozen outputs are checked against the replay before export.
The ignored NPZ is a rebuildable cache; deterministic gates live in derived/core.json.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np

# Imported frozen modules are read-only, including incidental interpreter caches.
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SOURCE = FISCAL / "job_capital_taxes_2026_10_14"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
GROUPS = ["G1", "G2", "G3plus", "white", "union"]


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load():
    spec = importlib.util.spec_from_file_location("frozen_job_capital", SOURCE / "job_capital.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started = time.perf_counter()
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    replay = CACHE / "positive_control"
    source = load()
    captured = {}
    frozen_interpreter_files = {str(p): digest(p) for p in (SOURCE / "__pycache__").glob("*") if p.is_file()}

    def observe(frame, event, arg):
        if event == "return" and frame.f_code is source.main.__code__:
            captured.update(frame.f_locals)

    before = {p.name: digest(p) for p in (SOURCE / "derived").iterdir() if p.is_file()}
    argv = sys.argv
    try:
        sys.argv = [str(SOURCE / "job_capital.py"), "--out-dir", str(replay)]
        with (CACHE / "positive_control.log").open("w") as log, contextlib.redirect_stdout(log):
            sys.setprofile(observe)
            rc = source.main()
    finally:
        sys.setprofile(None)
        sys.argv = argv
    assert rc == 0, "[BLOCKED] frozen replay failed"
    gates = []

    def gate(name, ok, detail=None):
        gates.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            raise RuntimeError(f"[BLOCKED] {name}: {detail}")

    for p in replay.iterdir():
        if p.is_file():
            gate(f"frozen positive control byte-identical: {p.name}", digest(p) == before[p.name])
    gate("source outputs untouched", before == {p.name: digest(p) for p in (SOURCE / "derived").iterdir() if p.is_file()})
    gate("frozen interpreter caches unchanged", frozen_interpreter_files ==
         {str(p): digest(p) for p in (SOURCE / "__pycache__").glob("*") if p.is_file()})
    gate("all frozen replay gates passed", all(g["passed"] for g in source.GATES))
    loc = captured
    arrays = {"cells": np.array(loc["all_cells"])}
    for g in GROUPS:
        arrays[f"shares_{g}"] = loc["shares"]("personal", g)
    arrays["cell_pool"] = np.array([",".join(map(str, idx)) for idx in loc["pooled_index"](source.N_MIN)])
    for name, vector in loc["nat_lines"].items():
        arrays[f"tax_{name}"] = vector
    for name, vector in loc["full"].items():
        arrays[f"full_{name}"] = vector
    arrays["tax_corporate_ex_foreign"] = loc["vec"]["corporate_ex_foreign_bn"]
    d, weights, wage, masks = loc["d"], loc["w4"], loc["wage"], loc["m"]
    cells, cellidx = loc["all_cells"], loc["cellidx"]
    codes, codeidx = np.unique(d.INDUSTRY.to_numpy(int), return_inverse=True)
    arrays["industry_codes"] = codes
    arrays["code_cells"] = np.array([cells[cellidx[np.flatnonzero(codeidx == i)[0]]] for i in range(len(codes))])
    # Some public-administration/class-worker records override their industry's
    # summary cell. Each industry's national wages exported below are civilian
    # private jobs only where it belongs to a tax-bearing private cell.
    arrays["code_records"] = np.bincount(codeidx[masks["civilian"] & (wage > 0)], minlength=len(codes))
    pairs, pairidx = np.unique(np.stack([cellidx, codeidx], axis=1), axis=0, return_inverse=True)
    arrays["pair_cell_index"], arrays["pair_code_index"] = pairs[:, 0], pairs[:, 1]
    arrays["pair_records"] = np.bincount(pairidx[masks["civilian"] & (wage > 0)], minlength=len(pairs))
    sizes = d.NOEMP.to_numpy(int)
    gate("NOEMP lies in the source's seven bins", np.isin(sizes, np.arange(7)).all())

    def accumulate(index, n, group, vector):
        out = np.zeros((n, 161))
        k = masks[group] & (vector > 0)
        # Replicate-column loop avoids a large temporary record ×161 matrix.
        for r in range(161):
            out[:, r] = np.bincount(index[k], weights=vector[k] * weights[k, r], minlength=n)
        return out

    for label, index, n in (("size", cellidx * 7 + sizes, len(cells) * 7), ("code", codeidx, len(codes)), ("pair", pairidx, len(pairs))):
        national = accumulate(index, n, "civilian", wage)
        national_top = accumulate(index, n, "civilian", np.where(wage >= source.TOP, wage, 0))
        spread = national_top / national_top.sum(axis=0)
        grouped = {}
        for g in ["G1", "G2", "G3plus", "white"]:
            low = accumulate(index, n, g, np.where(wage < source.TOP, wage, 0))
            high = accumulate(index, n, g, np.where(wage >= source.TOP, wage, 0)).sum(axis=0)
            grouped[g] = (low + spread * high) * loc["corr"]["personal"][g]
        grouped["union"] = sum(grouped[g] for g in source.GENS)
        for g, arr in {"national": national, **grouped}.items():
            arrays[f"{label}_wages_{g}"] = arr.reshape(len(cells), 7, 161) if label == "size" else arr
            if label == "size":
                ref = loc["wages"]["personal"][g]
                gap = float(np.max(np.abs(arr.reshape(len(cells), 7, 161).sum(axis=1) - ref)) / np.max(ref))
                gate(f"{g} size split conserves frozen cell wages in all replicates", gap < 1e-12, gap)
            else:
                ref = loc["wages"]["personal"][g].sum(axis=0)
                gap = float(np.max(np.abs(arr.sum(axis=0) - ref)) / np.max(ref))
                gate(f"{g} code split conserves frozen total wages in all replicates", gap < 1e-12, gap)
    item = json.loads((SOURCE / "derived/item.json").read_text())
    payload = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())
    jc = payload["meta"]["job_capital_taxes"]
    rates = {
        "G3plus": jc["lineage"]["wage_share"]["g3plus"]["personal"] / loc["denom"]["G3plus"]["personal"],
        "white": jc["lineage"]["wage_share"]["whites"]["personal"] / loc["denom"]["white_nh"]["personal"],
    }
    responses = {rd: loc["LINE_RESP"][rd] for rd in source.READINGS}
    control = {}
    for rd in source.READINGS:
        union = sum(arrays["shares_union"].T @ loc["nat_lines"][ln] * responses[rd][ln] for ln in source.LINES)
        lineage = union + sum(rates[g] * sum(arrays[f"shares_{g}"].T @ loc["nat_lines"][ln] * responses[rd][ln]
                                             for ln in source.LINES) for g in rates)
        gate(f"{rd} union control reproduces frozen central", abs(union[0] - item["central_bn"][rd]["personal"]) < 1e-9)
        gate(f"{rd} lineage control reproduces adopted v7", abs(lineage[0] - jc["effect_at_reference_bn"][rd]["personal"]) < 1e-9)
        control[rd] = {"union_bn": float(union[0]), "lineage_bn": float(lineage[0]), "union_se_bn": source.se(union), "lineage_conditional_se_bn": source.se(lineage)}
    np.savez(CACHE / "core.npz", **arrays)
    pin_paths = [SOURCE / "job_capital.py", SOURCE / "derived/item.json", SOURCE / "derived/national.json", SOURCE / "derived/national_by_industry.csv",
                 SOURCE / "derived/case_keys.json", SOURCE / "inputs/census_industry_crosswalk.csv", FISCAL / "main_case_2026_10_14/derived/corrections.json"]
    pin_paths += [getattr(source, n) for n in ("CPS", "KEYS", "ROW4", "FILLIN", "COUNTIES", "V6", "STACK")]
    pins = {str(p): {"sha256": digest(p), "reuse": "read-only local authoritative source"} for p in pin_paths}
    pin_file = HERE / "inputs/pins.json"
    if pin_file.exists():
        gate("previously pinned upstream bytes unchanged", json.loads(pin_file.read_text()) == pins)
    else:
        pin_file.write_text(json.dumps(pins, indent=2) + "\n")
    result = {"control": control, "responses": responses, "lineage_rates": rates, "corr": loc["corr"]["personal"], "gates": gates,
              "uncertainty": "160 CPS SDR replicates. Lineage wage shares and denominator calibration held fixed; excludes added-ancestry count/C3 and source-table uncertainty."}
    (DERIVED / "core.json").write_text(json.dumps(result, indent=2) + "\n")
    metric = {"elapsed_s": time.perf_counter() - started, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (CACHE / "core_runtime.json").write_text(json.dumps(metric) + "\n")
    gate("peak RSS below 2.5 GB", metric["peak_rss_bytes"] < 2.5e9, metric)
    print(json.dumps({"control": control, "gates": len(gates), "runtime": metric}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

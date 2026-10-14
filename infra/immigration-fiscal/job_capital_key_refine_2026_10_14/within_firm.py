#!/usr/bin/env python3
"""Firm-size gaps standardized to the union's BEA-cell wage distribution.

Read the common exact row-4/fill-in sufficient statistics; never replay or alter
the frozen item lane. All ratios and cell weights are recalculated in each of
the 160 SDR replicates, conditional on the core's calibration and top-wage rule.
"""
from __future__ import annotations

import csv
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
GATES = []
CATEGORIES = {
    "under100": [1, 2, 3],
    "1000plus": [6],
    "100to999": [4, 5],
    "unknown": [0],
}
EXCLUDED = ["GOVF", "GOVSL", "HH814", "RESIDENTIAL", "NOIND"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gate(name, passed, detail=None):
    GATES.append({"name": name, "passed": bool(passed), "detail": detail})
    if not passed:
        raise RuntimeError(f"[BLOCKED] {name}: {detail}")


def se(vector):
    return float(np.sqrt(4 / 160 * np.square(vector[1:] - vector[0]).sum()))


def summarize(vector, scale=1):
    return {"estimate": float(vector[0] * scale),
            "conditional_se": se(vector) * scale,
            "all161_columns": [float(x * scale) for x in vector]}


def main():
    start = time.perf_counter()
    GATES.clear()
    cache = HERE / "_cache/core.npz"
    core_file = DERIVED / "core.json"
    pins_file = HERE / "inputs/pins.json"
    pins = json.loads(pins_file.read_text())
    # These pins are core.py's authoritative upstream declarations, not a new
    # fallback source. Fail closed if the common cache's inputs have changed.
    for name, metadata in pins.items():
        path = Path(name)
        gate(f"common core upstream pin: {name}", path.exists() and digest(path) == metadata["sha256"])
    core = json.loads(core_file.read_text())
    gate("common core deterministic gates all passed", all(g["passed"] for g in core["gates"]))
    z = np.load(cache)
    cells = z["cells"].astype(str)
    national_all = z["size_wages_national"]
    union_all = z["size_wages_union"]
    gate("exact 69-cell seven-bin all161 core shape", national_all.shape == union_all.shape == (69, 7, 161))
    gate("union equals corrected generations all cells/bins/replicates",
         np.allclose(union_all, sum(z[f"size_wages_{g}"] for g in ["G1", "G2", "G3plus"]), rtol=1e-12, atol=1e-3))
    private = ~np.isin(cells, EXCLUDED)
    n, u = national_all[private], union_all[private]
    labels = cells[private]
    ncell, ucell = n.sum(axis=1), u.sum(axis=1)
    ntotal, utotal = ncell.sum(axis=0), ucell.sum(axis=0)
    gate("all included cells have positive national wages in all161 columns", np.all(ncell > 0))
    gate("private nation and union total positive in all161 columns", np.all(ntotal > 0) and np.all(utotal > 0))
    gate("NOEMP0 has no private wage dollars all161 columns", np.max(n[:, 0]) == 0 and np.max(u[:, 0]) == 0)
    gate("private wage conservation after exclusion all161 columns",
         np.allclose(utotal + union_all[~private].sum(axis=(0, 1)), union_all.sum(axis=(0, 1)), rtol=1e-12, atol=1e-3)
         and np.allclose(ntotal + national_all[~private].sum(axis=(0, 1)), national_all.sum(axis=(0, 1)), rtol=1e-12, atol=1e-3))
    uw, nw = ucell / utotal, ncell / ntotal
    gate("union and national BEA-cell weights sum to one all161 columns",
         np.max(np.abs(uw.sum(axis=0) - 1)) < 1e-12 and np.max(np.abs(nw.sum(axis=0) - 1)) < 1e-12)
    results, rows, standardized = {}, [], []
    for category, bins in CATEGORIES.items():
        ns, us = n[:, bins].sum(axis=1), u[:, bins].sum(axis=1)
        npart = ns / ncell
        upart = np.divide(us, ucell, out=np.zeros_like(us), where=ucell > 0)
        nat = ns.sum(axis=0) / ntotal
        union = us.sum(axis=0) / utotal
        reweighted = (uw * npart).sum(axis=0)
        raw = union - nat
        within = (uw * (upart - npart)).sum(axis=0)
        composition = ((uw - nw) * npart).sum(axis=0)
        standardized.append(reweighted)
        error = float(np.max(np.abs(raw - within - composition)))
        gate(f"{category} raw = within + composition all161 columns at1e-12", error < 1e-12, error)
        gate(f"{category} standardized subtraction = weighted within all161 columns at1e-12",
             np.max(np.abs(within - (union - reweighted))) < 1e-12)
        results[category] = {
            "national_share_pct": summarize(nat, 100),
            "union_share_pct": summarize(union, 100),
            "national_reweighted_to_union_cells_share_pct": summarize(reweighted, 100),
            "raw_gap_pp": summarize(raw, 100),
            "within_cell_gap_pp": summarize(within, 100),
            "cell_composition_gap_pp": summarize(composition, 100),
        }
        for i, cell in enumerate(labels):
            cgap = upart[i] - npart[i]
            cw = uw[i] * cgap
            cmix = (uw[i] - nw[i]) * npart[i]
            rows.append({"cell": cell, "firm_size": category,
                         "national_cell_wages_bn": float(ncell[i, 0] / 1e9),
                         "union_cell_wages_bn": float(ucell[i, 0] / 1e9),
                         "national_cell_weight_pct": float(nw[i, 0] * 100),
                         "union_cell_weight_pct": float(uw[i, 0] * 100),
                         "national_size_share_pct": float(npart[i, 0] * 100),
                         "union_size_share_pct": float(upart[i, 0] * 100),
                         "within_cell_gap_pp": float(cgap[0] * 100),
                         "within_cell_gap_conditional_se_pp": se(cgap) * 100,
                         "weighted_within_contribution_pp": float(cw[0] * 100),
                         "weighted_within_contribution_conditional_se_pp": se(cw) * 100,
                         "cell_composition_contribution_pp": float(cmix[0] * 100),
                         "cell_composition_contribution_conditional_se_pp": se(cmix) * 100})
    gate("four size categories partition every private wage dollar",
         sorted(sum(CATEGORIES.values(), [])) == list(range(7)))
    gate("standardized four-category proportions conserve one all161 columns",
         np.max(np.abs(sum(standardized) - 1)) < 1e-12)
    with (DERIVED / "within_firm.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "status": "measured CPS wage composition conditional on the case frame and wage treatment",
        "frame": "2024 wages, CPS ASEC2025, core's personal row-4 weights, fill-in correction by generation and national cell-size spread of group wages at or above $1M",
        "scope": "private BEA cells; exclude government, households and none exactly as frozen source private_cells",
        "excluded_cells": EXCLUDED,
        "included_cell_count": len(labels),
        "private_wages_bn": {"national": summarize(ntotal, 1e-9), "union": summarize(utotal, 1e-9)},
        "results": results,
        "standardization": "Sum union private wage cell weights times national within-cell firm-size wage proportions. Raw gap = standardized within-cell gap + BEA-cell composition gap; all weights recomputed in each replicate.",
        "uncertainty": "160 CPS SDR replicates with variance factor4/160. Conditional on fixed source fill-in factors and top-wage rule; excludes source-rule and calibration uncertainty. Finite-cell sampling reflected without thin-cell tax-key pooling.",
        "published_weight_comparison": "Not reproduced: core.npz only exports the exact adjusted row-4/fill-in frame. Frozen summary firm_size_wage_shares is direct row-4 civilian wages before fill-in/top-wage spread, pools all cells and has a different scope.",
        "frozen_source_trace": {"job_capital.py": "663-669 pools all civilian/union wage records by NOEMP, without any industry conditioning", "RESULT.md": "490-493 calls the pooled result within industries; replace with explicitly standardized results here"},
        "source_hashes": {str(p.relative_to(HERE)): digest(p) for p in [cache, core_file, pins_file]},
        "gates": GATES,
    }
    (DERIVED / "within_firm.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"gates": len(GATES), "private_cells": len(labels),
                      "results": {k: {label: {q: v for q, v in x.items() if q != "all161_columns"} for label, x in r.items()} for k, r in results.items()},
                      "elapsed_seconds": time.perf_counter() - start,
                      "peak_rss_native_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

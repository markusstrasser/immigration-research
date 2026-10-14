"""Exact personal job-capital taxes for omitted people, on source-lane keys.

Reuse the source's gated setup by AST, stopping before any output is built.
Linearize its TOP-wage redistribution and thin-cell pooling into per-record
rates. Original identified G3+ records supply the age rates and positive
control; lineage-inflated weights never enter those denominators.
"""
from __future__ import annotations

import ast
import gc
import importlib.util
import json
import resource
import sys
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "job_capital_taxes_2026_10_14/job_capital.py"


def _require(ok, name, **detail):
    if not ok:
        raise RuntimeError(f"[BLOCKED] job-capital {name}: {detail}")


def _source_setup(d):
    spec = importlib.util.spec_from_file_location("union_job_source", SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # The canonical frame has every source field except some employment fields.
    # Join by person identity, never assume the raw CSV's order is canonical.
    missing = [c for c in mod.PERSON if c not in d]
    frame = pd.DataFrame({c: d[c].to_numpy() for c in mod.PERSON + mod.REPS + ["GESTFIPS"]
                          if c in d}, copy=False)
    mod.checked(mod.CPS, mod.CPS_SHA)
    if missing:
        with zipfile.ZipFile(mod.CPS) as z:
            raw = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", *missing])
        frame = frame.merge(raw, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one", sort=False)
        _require(not frame[missing].isna().any().any(), "every job field joined")
    _require(np.array_equal(frame[["PH_SEQ", "PPPOS"]].to_numpy(), d[["PH_SEQ", "PPPOS"]].to_numpy()),
             "source frame preserves canonical person order")
    _require(not frame[mod.REPS].isna().any().any(), "every person has all replicate weights")
    _require(float((frame.MARSUPWT / 100 - frame.pwwgt0).abs().max()) < .01,
             "published main weight matches MARSUPWT")
    mod.load_frame = lambda: frame
    tree = ast.parse(SOURCE.read_text())
    # pandas' copy-on-write can expose the compact frame's weights read-only.
    # The source rakes them in place, so give that exact function a writable
    # copy; no values, masks or gates change.
    raker = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "row4_weights")
    weight_assign = [n for n in raker.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "w" for t in n.targets)]
    _require(len(weight_assign) == 1 and isinstance(weight_assign[0].value, ast.Call)
             and isinstance(weight_assign[0].value.func, ast.Attribute)
             and weight_assign[0].value.func.attr == "to_numpy", "source row4 buffer boundary unchanged")
    weight_assign[0].value.keywords.append(ast.keyword(arg="copy", value=ast.Constant(value=True)))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    boundaries = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "rows" for t in n.targets)
                  and isinstance(n.value, ast.List) and not n.value.elts]
    _require(len(boundaries) == 1, "source setup boundary unchanged")
    # CLI parsing is irrelevant to a callable; no source computation changes.
    fn.body = fn.body[:boundaries[0]] + ast.parse("return locals()").body
    row4_at = [i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "row4" for t in n.targets)]
    _require(len(row4_at) == 1, "source published-weight buffer boundary unchanged")
    # All published-weight gates and cell totals have finished; this full
    # 161-column buffer is never read again in the captured setup.
    fn.body[row4_at[0]:row4_at[0]] = ast.parse("del w_pub").body
    parses = [n for n in fn.body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "args" for t in n.targets)]
    _require(len(parses) == 1, "source CLI boundary unchanged")
    parses[0].value = ast.parse("argparse.Namespace(out_dir=DERIVED)", mode="eval").body
    exec(compile(ast.fix_missing_locations(ast.Module(body=[raker, fn], type_ignores=[])), str(SOURCE), "exec"),
         mod.__dict__)
    state = mod.main()
    _require(all(g["passed"] for g in mod.GATES), "all original source setup gates passed",
             failed=[g for g in mod.GATES if not g["passed"]])
    return mod, state


def job_record_taxes(d, W, extra_rows, gens):
    """Return exact job-tax receipts, before responses, in billions.

    outside_bn[line]: (len(extra_rows), 161), weighted own-record receipts.
    g3_age_rates_bn[line]: (17, 161), original G3+ receipts per person by
    five-year age band (80+ open); caller applies line responses and signs.
    baseline_bn[line]: original G3+ aggregate, checked against item.json.
    responses[line]: {low, high}, the source item's responses.
    The omitted native records take G3+'s wage fill-in correction [ASSUMPTION].
    All source keys, row4 and denominators remain on the canonical union.
    """
    start = time.perf_counter()
    extra_rows = np.asarray(extra_rows, dtype=int)
    _require(len(np.unique(extra_rows)) == len(extra_rows), "outside rows unique")
    mod, S = _source_setup(d)
    item = json.loads((mod.DERIVED / "item.json").read_text())
    _require(all(g["passed"] for g in item["gates"]), "item gates passed")
    _require(all(np.array_equal(gens[g], S["m"][g]) for g in mod.GENS),
             "caller generations equal source generations")
    _require(not S["m"]["union"][extra_rows].any(), "outside rows disjoint from original union")
    _require(S["m"]["civilian"][extra_rows].all(), "outside persons civilian")
    _require(d.PRCITSHP.iloc[extra_rows].isin([1, 2, 3]).all(), "outside persons native")
    _require(np.array_equal(W[extra_rows], S["w4"][extra_rows]), "outside weights equal original row4")
    pools, n_cells = S["pooled_index"](mod.N_MIN), S["n_cells"]
    natw = S["wages"]["personal"]["national"]
    hi = S["wage"] >= mod.TOP
    high = mod.cell_wages(np.where(hi, S["wage"], 0.), S["cellidx"], n_cells,
                          S["m"]["civilian"], S["w4"], S["unit"], S["n_unit"], "personal")
    high_total = high.sum(axis=0)
    _require((high_total > 0).all(), "national TOP wages positive in every replicate")
    spread = high / high_total
    g3_rows = np.flatnonzero(S["m"]["G3plus"])
    age = np.minimum(d.A_AGE.to_numpy()[g3_rows] // 5, 16)
    g3w = S["w4"][g3_rows]
    band_n = np.zeros((17, 161))
    np.add.at(band_n, age, g3w)
    _require((band_n > 0).all(), "all original G3+ age bands positive")
    factor = S["corr"]["personal"]["G3plus"]
    outside, age_rates, baseline, responses, closures, baseline_gaps = {}, {}, {}, {}, {}, {}
    for name, line in mod.ITEM_LINES.items():
        # A person's low wage contributes to every tax cell whose pooled
        # denominator includes that person's cell. Sum the linear coefficients.
        coefficients = np.zeros((n_cells, 161))
        tax = S["nat_lines"][line]
        for i, idx in enumerate(pools):
            den = natw[idx].sum(axis=0)
            rates = np.divide(tax[i], den, out=np.zeros_like(den), where=den > 0)
            coefficients[idx] += rates
        top_rate = (spread * coefficients).sum(axis=0)
        # National closure is uncorrected: fill-in moves group wages only.
        closed = ((natw - high) * coefficients).sum(axis=0) + high_total * top_rate
        gap = float(np.abs(closed - tax.sum()).max())
        _require(gap < 1e-6, f"{name} national closure every replicate", max_gap_bn=gap)
        closures[name] = gap

        def receipts(rows):
            wage = S["wage"][rows]
            rate = coefficients[S["cellidx"][rows]].copy()
            rate[hi[rows]] = top_rate
            return wage[:, None] * factor * rate

        g3_tax = receipts(g3_rows) * g3w
        target = S["shares"]("personal", "G3plus").T @ tax
        actual = g3_tax.sum(axis=0)
        gap_reps = float(np.abs(actual - target).max())
        expected = item["by_generation"]["G3plus"][name]["personal"]
        gap_main = float(abs(actual[0] - expected))
        _require(max(gap_reps, gap_main) < 1e-6, f"{name} original G3+ positive control",
                 max_gap_replicates_bn=gap_reps, item_gap_bn=gap_main)
        baseline_gaps[name] = max(gap_reps, gap_main)
        baseline[name] = actual
        band_tax = np.zeros((17, 161))
        np.add.at(band_tax, age, g3_tax)
        age_rates[name] = band_tax / band_n
        outside[name] = receipts(extra_rows) * W[extra_rows]
        _require(np.isfinite(outside[name]).all() and (outside[name] >= 0).all()
                 and np.isfinite(age_rates[name]).all() and (age_rates[name] >= 0).all(),
                 f"{name} finite nonnegative own and age rates")
        responses[name] = item["lines"][name]["response"]
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on this macOS host
    _require(peak < 2_500_000_000, "peak memory below 2.5GB", maxrss_bytes=peak)
    result = dict(outside_bn=outside, g3_age_rates_bn=age_rates, baseline_bn=baseline,
                responses=responses, national_closure_gap_bn=closures,
                baseline_gap_bn=baseline_gaps, source_gates=mod.GATES,
                g3_fillin_factor=factor, elapsed_seconds=time.perf_counter() - start,
                maxrss_bytes=peak)
    # The AST module's functions reference their globals; collect that cycle
    # before the caller loads another large person-pricing kernel.
    del receipts, S, mod
    gc.collect()
    return result

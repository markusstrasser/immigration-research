"""Paired, read-only hot-deck operator probe. Run from the repository root.

Only this lane receives outputs. The imported run is cloned through AST, replacing
exactly its two earned-income assignments; its donor procedure and AGI stay fixed.
The corrected compute reuses mixed_unit_credits.eitc and half_se_tax. No income,
return-mapping, status, national-budget, or AGI correction is bundled into this probe.
"""
from __future__ import annotations

import ast
import cProfile
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import resource
import pstats
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
UP = FISCAL / "cps_imputation_keys_2026_09_23"
OUT = LANE / "derived"
sys.path.insert(0, str(UP))
import common as c
import hotdeck as hd
import run_hotdeck as driver
import taxcalc as tc
import translate as tr
import combine_onbooks_lane as cb
import combine_status as cs

spec = importlib.util.spec_from_file_location("correct_credit_rules", FISCAL / "mixed_unit_credits_2026_10_14/credits.py")
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)
OLD_COMPUTE = tc.compute
GATES = []


def gate(name, ok):
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}")
    GATES.append(name)


def corrected_compute(agi, earned, investment, status, kids17, kids19, other_dep, aged, head_age):
    fed, _, actc = OLD_COMPUTE(agi, earned, investment, status, kids17, kids19, other_dep, aged, head_age)
    eitc = rules.eitc(kids19, earned, agi, status == "joint", investment, (head_age >= 25) & (head_age <= 64))
    return fed, eitc, actc


def corrected_earned(frame):
    wages = frame.WSAL_VAL.to_numpy(float)
    se = (frame.SEMP_VAL + frame.FRSE_VAL).to_numpy(float)
    return wages + se - rules.half_se_tax(se, wages)


def corrected_run():
    tree = ast.parse(inspect.getsource(hd.run))
    changed = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("earned_old", "earned_new"):
                frame = "d" if name == "earned_old" else "new"
                node.value = ast.Call(ast.Name("corrected_earned", ast.Load()), [ast.Name(frame, ast.Load())], [])
                changed.append(name)
    gate("AST changes exactly earned_old and earned_new", sorted(changed) == ["earned_new", "earned_old"])
    namespace = {**hd.__dict__, "corrected_earned": corrected_earned}
    exec(compile(ast.fix_missing_locations(tree), str(UP / "hotdeck.py"), "exec"), namespace)
    return namespace["run"]


def write_csv(name, rows):
    pd.DataFrame(rows).to_csv(OUT / name, index=False, lineterminator="\n", float_format="%.15g")


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def validation(d, operator, earned, label):
    r, member = tc.returns(d)
    tc.compute = operator
    inv = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL.clip(lower=0) + d.CAP_VAL).to_numpy(float)
    fields = tc.model_fields(d, r, member, earned, inv)
    w = d.pwwgt0.to_numpy(float)[r.row]
    out = []
    for field, values, col in zip(("fedtax_bc", "eitc", "actc"), fields, ("FEDTAX_BC", "EIT_CRED", "ACTC_CRD")):
        observed = d[col].to_numpy(float)[r.row]
        err = values - observed
        cov = np.cov(values, observed, aweights=w)
        out.append(dict(operator=label, field=field, returns=len(r), census_total_bn=float(observed @ w / 1e9),
                        model_total_bn=float(values @ w / 1e9), weighted_corr=float(cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])),
                        mean_abs_error=float(np.abs(err) @ w / w.sum()),
                        share_within_100=float((np.abs(err) <= 100) @ w / w.sum())))
    tc.compute = OLD_COMPUTE
    return out


def vectors(frame, index, flag=None, books=None):
    if flag is None:
        receipt = c.receipt_keys(frame, index)
        spending = c.spending_vectors(frame, index)
        return {a: {**receipt[a], **spending[a]} for a in ("personal", "shared")}
    return cb.frame_vectors(frame, flag, books, index)


def shares(vec, w, civ, union):
    return {(a, k): np.array([float(v[union] @ w[union] / (v[civ] @ w[civ]))])
            for a, keys in vec.items() for k, v in keys.items()}


def method_pair(base, m, p):
    return {"b_hotdeck_union_matched": m, "b_matched_over_pooled": {k: base[k] * m[k] / p[k] for k in base}}


def mean_maps(maps):
    return {k: np.mean([x[k] for x in maps], axis=0) for k in maps[0]}


def main():
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    cache = UP / "_cache/asec25_lane.parquet"
    gate("required cached frame exists; no upstream cache write", cache.is_file())
    names = pq.read_schema(cache).names
    d = pd.read_parquet(cache, columns=[n for n in names if n not in c.REPS[1:]])
    if "--profile-one" in sys.argv:
        profiler = cProfile.Profile()
        profiler.runcall(hd.run, d, seed=driver.SPECS["main"][1][0], verbose=False)
        pstats.Stats(profiler).strip_dirs().sort_stats("cumulative").print_stats(12)
        return
    civ, union = c.masks(d)
    index = c.spm_index(d)
    w0 = d.pwwgt0.to_numpy(float)
    hf = float(w0[civ].sum() / c.RESIDENT)
    row4 = json.loads((FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json").read_text())
    w4 = w0.copy()
    for label, code in (("naturalized", 4), ("noncitizen", 5)):
        mask = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(code).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
        ref = row4["row4_factors"][label]
        gate(f"row4 {label} exact records and published weight", int(mask.sum()) == ref["records"] and abs(w0[mask].sum() - ref["cps_population"]) < 1e-3)
        w4[mask] *= ref["factor"]
    gate("row4 union is account population", abs(w4[union].sum() - row4["populations"]["row4"]) < 1e-3)
    si, hh = cs.status_inputs()
    flag = cb.state_aware_flag(si, hh, d, cb.STATUS_BLIND_2024)
    configs, _ = cb.share_configs(d)
    del si, hh
    stored_frame = json.loads((FISCAL / "backtest_admin_totals_2026_09_28/derived/prediction_audit.json").read_text())["asec2025_adopted"]
    for name, value in (("union_m", w4[union].sum() / 1e6), ("flagged_union_m", w4[union & flag].sum() / 1e6),
                        ("flagged_m", w4[civ & flag].sum() / 1e6)):
        gate(f"case status population {name}", abs(float(value) - stored_frame[name]) < 1e-9)
    model = json.loads(tr.MODEL.read_text())
    stored = np.load(UP / "_cache/hotdeck_key_shares.npz")
    weights = {"published": w0, "row4": w4}
    # Plain published and row4; plus the adopted row4/state-aware status at each on-books arm.
    frames = {"published": (w0, None, None), "row4": (w4, None, None),
              **{f"case_{arm}": (w4, flag, configs[("origin", arm)]) for arm in cb.CASES}}
    base, denominators = {}, {}
    for label, (w, f, ob) in frames.items():
        vec = vectors(d, index, f, ob)
        base[label] = shares(vec, w, civ, union)
        denominators[label] = {a: float(vec[a]["refundable_credits"][civ] @ w[civ]) for a in ("personal", "shared")}
    gate("base published shares reproduce stored keys", max(abs(v[0] - stored[f"base|{a}|{k}"][0]) for (a, k), v in base["published"].items()) < 1e-12)
    gross = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    val = validation(d, OLD_COMPUTE, gross, "published")
    val += validation(d, corrected_compute, corrected_earned(d), "corrected")
    val_ref = pd.read_csv(UP / "derived/taxcalc_validation.csv").set_index("field")
    gate("baseline validation reproduces stored table", all(abs(x[k] - val_ref.loc[x["field"], k]) < 1e-8
         for x in val[:3] for k in ("census_total_bn", "model_total_bn", "weighted_corr", "mean_abs_error", "share_within_100")))
    # Direct arithmetic probes cover the regime where subtraction gives the wrong result.
    earned = np.array([5000., 20000., 0.])
    agi = np.array([30000., 30000., 40000.])
    e = rules.eitc(np.ones(3), earned, agi, np.zeros(3, bool), np.zeros(3), np.ones(3, bool))
    gate("low earnings high AGI min-of-two arithmetic", np.allclose(e, [1700., 3049.656, 0.]))
    gate("SE deduction wage-base and floor arithmetic", np.allclose(rules.half_se_tax(np.array([10000., 10000., 100.]), np.array([0., 168600., 0.])), [706.4775, 133.9075, 0.]))
    run_correct = corrected_run()
    totals, keyrows, lines, translated, donor_checks = [], [], [], [], []
    payload = {}
    original_draw = hd.draw_donors
    for spec_name, (all_items, seeds) in driver.SPECS.items():
        runs = {op: {variant: {f: [] for f in frames} for variant in ("matched", "pooled")} for op in ("published", "corrected")}
        for seed in seeds:
            for variant, cells in (("matched", hd.BASE), ("pooled", [])):
                print(f"[paired] {spec_name} {seed} {variant}", flush=True)
                draws = []
                def record(*args, **kwargs):
                    result = original_draw(*args, **kwargs)
                    draws.append(tuple(x.copy() for x in result))
                    return result
                hd.draw_donors = record
                tc.compute = OLD_COMPUTE
                old, diag_old = hd.run(d, seed=seed, verbose=False, base=cells, item_property=all_items)
                pos = 0
                def replay(*args, **kwargs):
                    nonlocal pos
                    result = draws[pos]
                    gate(f"replay recipient count {spec_name} {seed} {variant} {pos}", len(result[0]) == len(args[2]))
                    pos += 1
                    return result
                hd.draw_donors = replay
                run_correct.__globals__["draw_donors"] = replay
                tc.compute = corrected_compute
                new, diag_new = run_correct(d, seed=seed, verbose=False, base=cells, item_property=all_items)
                hd.draw_donors = original_draw
                tc.compute = OLD_COMPUTE
                gate(f"all draws consumed {spec_name} {seed} {variant}", pos == len(draws))
                gate(f"same donor diagnostics {spec_name} {seed} {variant}", diag_old.equals(diag_new))
                allowed = {"EIT_CRED", "ACTC_CRD", "SPM_RESOURCES"}
                gate(f"only credits/resources change {spec_name} {seed} {variant}", old.drop(columns=list(allowed)).equals(new.drop(columns=list(allowed))))
                draw_sha = hashlib.sha256(b"".join(x.tobytes() for pair in draws for x in pair)).hexdigest()
                donor_checks.append(dict(spec=spec_name, seed=seed, variant=variant, calls=len(draws), donor_sha256=draw_sha))
                for basis, w in weights.items():
                    for group, mask in (("union", union), ("everyone_else", civ & ~union)):
                        for col in ("EIT_CRED", "FEDTAX_BC", "ACTC_CRD"):
                            before = float(old[col].to_numpy(float)[mask] @ w[mask] / 1e9)
                            after = float(new[col].to_numpy(float)[mask] @ w[mask] / 1e9)
                            totals.append(dict(spec=spec_name, seed=seed, variant=variant, basis=basis, group=group, field=col,
                                               published_bn=before, corrected_bn=after, change_bn=after-before))
                for op, frame in (("published", old), ("corrected", new)):
                    for label, (w, f, ob) in frames.items():
                        got = shares(vectors(frame, index, f, ob), w, civ, union)
                        runs[op][variant][label].append(got)
                        if op == "published" and label == "published":
                            gap = max(abs(v[0] - stored[f"{spec_name}|{variant}@{seed}|{a}|{k}"][0]) for (a, k), v in got.items())
                            gate(f"stored full-weight seed {spec_name} {seed} {variant}", gap < 1e-12)
                del old, new, draws
        # The driver takes ratios AFTER averaging shares. Seed means of ratios are different.
        for seed_label, i in [(s, j) for j, s in enumerate(seeds)] + [("mean", None)]:
            for label in frames:
                methods = {}
                for op in runs:
                    m = runs[op]["matched"][label][i] if i is not None else mean_maps(runs[op]["matched"][label])
                    p = runs[op]["pooled"][label][i] if i is not None else mean_maps(runs[op]["pooled"][label])
                    methods[op] = method_pair(base[label], m, p)
                for method in methods["published"]:
                    before, after = methods["published"][method], methods["corrected"][method]
                    changed = {k: after[k]-before[k] for k in before if abs(float(after[k][0]-before[k][0])) > 1e-15}
                    for (a, k), diff in changed.items():
                        keyrows.append(dict(spec=spec_name, seed=seed_label, basis=label, method=method, allocation=a, key=k,
                                            published_share=float(before[(a,k)][0]), corrected_share=float(after[(a,k)][0]), change_share=float(diff[0])))
                    changed_rows = tr.line_deltas(model, before, after, np.array([hf]))
                    for row in changed_rows:
                        delta = float(row["reps"][0])
                        if abs(delta) <= 1e-12:
                            continue
                        lines.append(dict(spec=spec_name, seed=seed_label, basis=label, method=method, side=row["side"],
                                          line=row["line"], key=row["key"], allocation=row["allocation"], change_bn=delta))
                    if label.startswith("case_"):
                        for a in ("shared", "personal"):
                            delta_share = float(after[(a,"refundable_credits")][0]-before[(a,"refundable_credits")][0])
                            cps_equiv_bn = denominators[label][a] * delta_share / 1e9
                            translated.append(dict(spec=spec_name, seed=seed_label, case=label, method=method, allocation=a,
                                                   cps_group_equivalent_change_bn=cps_equiv_bn, refundable_change_bn=1.90*cps_equiv_bn,
                                                   federal_income_tax_change_bn=0.0, cost_change_bn=1.90*cps_equiv_bn))
                    if seed_label == "mean":
                        key = f"{spec_name}|{label}|{method}"
                        payload[key] = {"receipts": {}, "spending": {}}
                        for row in changed_rows:
                            point = float(row["reps"][0])
                            if abs(point) <= 1e-12:
                                continue
                            if row["side"] == "receipts":
                                payload[key]["receipts"].setdefault(row["line"], {})[row["allocation"]] = point
                            else:
                                payload[key]["spending"].setdefault(row["line"], {}).setdefault(row["key"], {})[row["allocation"]] = point
        # Raw group-flow means, unlike matched-over-pooled, are ordinary arithmetic means.
        t = pd.DataFrame([r for r in totals if r["spec"] == spec_name and r["seed"] != "mean"])
        for group, frame in t.groupby(["variant", "basis", "group", "field"], sort=True):
            totals.append(dict(spec=spec_name, seed="mean", **dict(zip(("variant", "basis", "group", "field"), group)),
                               **{k: float(frame[k].mean()) for k in ("published_bn", "corrected_bn", "change_bn")}))
    trans = pd.DataFrame(translated)
    means = trans[(trans.spec == "main") & (trans.seed == "mean")]
    band = {arm: {a: float(means[(means.case == f"case_{arm}") & (means.allocation == a)].cost_change_bn.mean())
                  for a in ("shared", "personal")} for arm in cb.CASES}
    inputs = [UP / n for n in ("taxcalc.py", "hotdeck.py", "run_hotdeck.py", "common.py", "translate.py", "combine_onbooks_lane.py", "combine_status.py")]
    inputs += [rules.LANE / "credits.py", cache, UP / "_cache/hotdeck_key_shares.npz", tr.MODEL,
               FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json"]
    summary = dict(scope="EITC formula and net earned income for EITC/ACTC; AGI held; donor draws paired",
                   populations=dict(published_union=float(w0[union].sum()), row4_union=float(w4[union].sum())),
                   first_order_band_change_bn=band, clears_half_bn=any(abs(v) > .5 for z in band.values() for v in z.values()),
                   conversions=dict(refundable_account_per_cps_dollar=1.90, federal_change="zero; operator never changes FEDTAX_BC"),
                   translation=translated, validation=val, donor_checks=donor_checks, gates=GATES,
                   sources_sha256={str(p.relative_to(FISCAL)): c.sha(p) for p in inputs})
    write_csv("totals.csv", totals)
    write_csv("keys.csv", keyrows)
    write_csv("line_deltas.csv", lines)
    write_csv("validation.csv", val)
    write_json("line_deltas.json", payload)
    write_json("summary.json", summary)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes, Linux KiB. Timing/peak go to stdout, never into reproducible artifacts.
    peak_gb = peak / (1e9 if sys.platform == "darwin" else 1e6)
    print(json.dumps({"band_change_bn": band, "gates": len(GATES), "seconds": time.perf_counter()-started, "peak_gb": peak_gb}), flush=True)
    gate("process peak under 2.5 GB", peak_gb < 2.5)


if __name__ == "__main__":
    main()

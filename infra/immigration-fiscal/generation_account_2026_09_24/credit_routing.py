"""Replay child-credit ownership without changing the national or identified-union account.

The claimant's survey/replicate weight travels with the dollars. Only linked union
dependents of union claimants are transferred here: item 5b separately covers the
boundary. Eligible dependents share a return's credit equally; the model observes
credit amounts by return, not individual children. Childless EITC remains with its
claimant. Convention b uses frame.assignments, including its parent fallback.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/credit_routing.py
The full hotdeck RNG sequence is replayed, and checked against stored source keys.
Only sufficient statistics are cached in this lane; source imports never write
bytecode. --refresh ignores that provenance-keyed cache.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
import gc
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from memory_budget import peak_bytes, require_within_budget

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
CACHE = HERE / "_cache" / "credit_routing"
GENS = ("G1", "G2", "G3plus")
METHODS = ("b_hotdeck_union_matched", "b_matched_over_pooled")
GATES = []


def checkpoint(label):
    print(f"[footprint] {label}: peak_bytes={peak_bytes()}", flush=True)


def release_frames():
    """Return freed Arrow decoding arenas before the next stage allocates."""
    gc.collect()
    pa.default_memory_pool().release_unused()


def frame_without_replicates(path, reps):
    """Preserve source column order/dtypes, omitting only unused replicate columns."""
    columns = [c for c in pq.read_schema(path).names if c not in reps[1:]]
    d = pd.read_parquet(path, columns=columns, use_threads=False)
    checkpoint(f"projected frame {path.name}")
    return d


def replicate_weights(path, reps, block_size=16):
    """Bound Arrow's decoding buffers; retain the original float64/F-order matrix.

    Matrix products still use all 161 columns at once, preserving their original
    BLAS arithmetic and output bytes. Only the parquet decoding is blocked.
    """
    n = pq.read_metadata(path).num_rows
    weights = np.empty((n, len(reps)), dtype=np.float64, order="F")
    for start in range(0, len(reps), block_size):
        columns = reps[start:start + block_size]
        block = pd.read_parquet(path, columns=columns, use_threads=False)
        weights[:, start:start + len(columns)] = block.to_numpy(float)
        del block
        release_frames()
        checkpoint(f"replicate block {path.name} {start}:{start + len(columns)}")
    return weights


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def gate(name, ok, value=True):
    if not ok:
        raise RuntimeError(f"[BLOCKED] {name}: {value}")
    GATES.append({"name": name, "passed": True, "value": value})
    print(f"  ✓ {name}", flush=True)


def sdr(a):
    a = np.asarray(a)
    return float(np.sqrt(4 / 160 * np.square(a[1:] - a[0]).sum()))


def aligned_omega(F, d):
    fields = ["PH_SEQ", "PPPOS", "PRPERTYP", "A_AGE", "PRCITSHP", "PENATVTY", "PEMNTVTY", "PEFNTVTY",
              "PRDTHSP", "A_LINENO", "PEPAR1", "PEPAR2", "PF_SEQ"]
    gd = pd.read_parquet(F.CACHE / "asec25_generation.parquet", columns=fields)
    civ, union, gens = F.masks(gd)
    om, _, _ = F.assignments(gd, civ, union, gens)
    key = pd.MultiIndex.from_frame(gd[["PH_SEQ", "PPPOS"]])
    ix = key.get_indexer(pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]]))
    gate("every_person_has_generation_frame_row", bool((ix >= 0).all()))
    return {k: v[ix] for k, v in om.items()}


def transfer_owner(omega, heads, drows, ri, eligible, union):
    """Return-level child-minus-filer ownership; never cross the identified union.

    Eligible dependents outside the union retain their portion with the union
    claimant: moving it out would change the fixed removal total. Eligible union
    dependents receive their equal portion. No eligible dependent means no move.
    """
    n = len(heads)
    denom = np.bincount(ri, weights=eligible.astype(float), minlength=n)
    moved = eligible & union[drows] & union[heads][ri]
    frac = np.bincount(ri, weights=moved.astype(float), minlength=n) / np.maximum(denom, 1)
    child = np.stack([np.bincount(ri, weights=moved * omega[drows, j], minlength=n)
                      / np.maximum(denom, 1) for j in range(3)])
    result = child - omega[heads].T * frac
    gate("transfer_owner_preserves_union", float(np.abs(result.sum(axis=0)).max()) < 1e-12)
    return result


def weighted_delta(amount, delta, W):
    return np.stack([(amount * v) @ W for v in delta])


def capture_credit_replay(C):
    C.OUT = CACHE / "source_replay"
    C.OUT.mkdir(parents=True, exist_ok=True)
    captured = {}
    wanted = {"item", "d", "civ", "union", "W", "h", "drows", "ri", "base", "mts", "model", "hf", "ref_line",
              "flag", "onbooks", "f_other", "per_fit", "wr", "R", "dmem", "dgen", "owner", "comp_ruled",
              "side", "account", "keep_of"}
    def profile(frame, event, arg):
        if event == "return" and frame.f_code.co_name in (
                "read_csv", "read_parquet", "load", "row4_weights", "person_keys", "status_flag"):
            checkpoint(f"source {frame.f_code.co_name} {frame.f_code.co_filename}")
        if event == "return" and frame.f_code is C.main.__code__:
            captured.update({k:v for k,v in frame.f_locals.items() if k in wanted})
    before = sys.getprofile()
    sys.setprofile(profile)
    try:
        C.main()
    finally:
        sys.setprofile(before)
    gate("source_replay_completed", "item" in captured)
    source = json.loads((FISCAL / "mixed_unit_credits_2026_10_14/derived/item.json").read_text())
    got = captured["item"]
    gap = max(abs(got["parts"][k]["bn"] - v["bn"]) for k, v in source["parts"].items())
    gate("item5b_replay_reproduces_frozen_parts", gap < 1e-9, gap)
    return captured, source


def refundable_stats(d, W, civ, union, heads, delta, flag=None, onbooks=None):
    eit = d.EIT_CRED.to_numpy(float)
    act = d.ACTC_CRD.to_numpy(float)
    if flag is not None:
        eit = np.where(flag, 0.0, eit)
        act = np.where(flag, act * onbooks, act)
    total = (eit + act)[civ] @ W[civ]
    gate("refundable_national_key_positive", bool((total > 0).all()))
    sh = (eit + act)[union] @ W[union] / total
    return {"union": sh, "delta": {conv: (weighted_delta(eit[heads], v["eitc"], W[heads])
                                          + weighted_delta(act[heads], v["actc"], W[heads])) / total
                                    for conv, v in delta.items()}}


def route_r6(L, om, source):
    R, dr, ri, dm = (L[k] for k in ("R", "drows", "ri", "dmem"))
    n = len(R)
    owner_b = np.stack([np.bincount(ri, weights=dm * om["b"][dr, j], minlength=n)
                        / np.maximum(R.n_mem.to_numpy(), 1) for j in range(3)])
    out = []
    net_shift = np.zeros((3,161))
    for key, part in source["parts"].items():
        term, side, source_gen = part["term"], part["side"], part["generation"]
        ix = GENS.index(source_gen)
        values = np.zeros((3, 161))
        for component, amount in L["comp_ruled"].items():
            if component.split("_")[0] != term or L["side"][component] != ("receipts" if side == "receipt" else "spending"):
                continue
            new_owner = owner_b if term in ("A", "C") else L["owner"][component]
            live = np.abs(amount) > 0
            gate(f"r6_{component}_b_owner_exhaustive", bool(np.allclose(new_owner[:, live].sum(axis=0), 1)))
            for j in range(3):
                if term in ("A", "C"):
                    # Joint old/new ownership by dependent, not a product of
                    # return-level marginal shares (which loses the lineage).
                    joint = np.bincount(ri, weights=dm * (L["dgen"] == ix) * om["b"][dr, j], minlength=n)
                    joint /= np.maximum(R.n_mem.to_numpy(), 1)
                else:
                    joint = L["owner"][component][ix] * new_owner[j]
                x = amount * L["keep_of"]("R3", component) * joint
                values[j] += L["account"](x, component) * (-1 if side == "receipt" else 1)
        gate(f"r6_{key}_preserves_frozen_part", abs(values[:, 0].sum() - part["bn"]) < 1e-9)
        out.append({"part": key, "side": side, "line": part["line"], "source_generation": source_gen,
                    "per_generation_bn": {g: float(values[j, 0]) for j, g in enumerate(GENS)},
                    "se_bn": {g: sdr(values[j]) for j, g in enumerate(GENS)}})
        signed = values * (-1 if side == "receipt" else 1)
        net_shift += signed
        net_shift[ix] -= signed.sum(axis=0)
    return out, {g:{"bn":float(net_shift[j,0]),"se_bn":sdr(net_shift[j])} for j,g in enumerate(GENS)}


def pins():
    paths = [Path(__file__), HERE / "frame.py", HERE / "stack_split.py", HERE / "external_split.py",
             HERE / "derived/stack_by_generation.json", HERE / "derived/external_by_generation.json",
             FISCAL / "mixed_unit_credits_2026_10_14/credits.py",
             FISCAL / "mixed_unit_credits_2026_10_14/derived/item.json",
             FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json",
             FISCAL / "external_benchmarks_2026_09_24/derived/ota_shares.csv",
             FISCAL / "tax_key_heldout_2026_09_28/keys.py",
             FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"]
    paths += [FISCAL / "cps_imputation_keys_2026_09_23" / p for p in
              ["hotdeck.py", "taxcalc.py", "common.py", "run_hotdeck.py", "combine_onbooks_lane.py",
               "combine_status.py", "_cache/hotdeck_key_shares.npz", "_cache/onbooks_lane_line_deltas.json"]]
    paths += [FISCAL / p for p in ["external_benchmarks_2026_09_24/frame.py",
                                   "external_benchmarks_2026_09_24/ota_arm.py",
                                   "world_ledger_2026_09_27/population_basis.py",
                                   "assumption_explorer_2026_09_21/derived/model.json",
                                   "generation_account_2026_09_24/_cache/asec25_generation.parquet",
                                   "external_benchmarks_2026_09_24/_cache/cps25_frame.parquet",
                                   "cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet",
                                   "tax_key_heldout_2026_09_28/reads/irs_table_1_2_ty2023.md",
                                   "tax_key_heldout_2026_09_28/derived/bins.csv",
                                   "tax_key_heldout_2026_09_28/derived/translation_inputs.json",
                                   "external_benchmarks_2026_09_24/derived/cbo_group_shares.csv"]]
    return {str(p.relative_to(FISCAL)): sha(p) for p in paths}


def replay_source():
    """Compute replay statistics in a process that exits before hotdeck starts."""
    start = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    source_pins = pins()
    C = load_module(FISCAL / "mixed_unit_credits_2026_10_14/credits.py", "routing_credits")
    F = load_module(HERE / "frame.py", "routing_generation_frame")
    L, source_item = capture_credit_replay(C)
    checkpoint("source replay captured")
    d, civ, union, W, heads, dr, ri, base = (L[k] for k in ("d", "civ", "union", "W", "h", "drows", "ri", "base"))
    row4_union = float(W[union, 0].sum())  # source replay already gates this on the authoritative row-4 count
    omega = aligned_omega(F, d)
    age = d.A_AGE.to_numpy()[dr]
    student = d.A_ENRLW.eq(1).to_numpy()[dr]
    kinds = {"actc": age < 17, "eitc": (age < 19) | ((age < 24) & student),
             "nonref": np.ones(len(dr), bool), "care": age < 13}
    delta = {conv: {k: transfer_owner(om, heads, dr, ri, m, union) for k, m in kinds.items()}
             for conv, om in omega.items()}
    # The full published weights remain available from the source frame loaded by row4_weights.
    # Only Mexico-born outside CA/TX changed under row 4. Restore their raw
    # weights directly; reading a second full 161-column frame caused >2.5 GB.
    WP = W.copy()
    changed = union & d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.isin([4, 5]).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
    gd = pd.read_parquet(F.CACHE / "asec25_generation.parquet", columns=["PH_SEQ", "PPPOS", *C.REPS],
                         filters=[("PENATVTY", "=", 303), ("PRCITSHP", "in", [4, 5]), ("GESTFIPS", "not in", [6, 48])])
    ix = pd.MultiIndex.from_frame(gd[["PH_SEQ", "PPPOS"]]).get_indexer(pd.MultiIndex.from_frame(d.loc[changed, ["PH_SEQ", "PPPOS"]]))
    gate("every_row4_changed_person_has_raw_published_weights", bool((ix >= 0).all()))
    WP[changed] = gd[C.REPS].to_numpy(float)[ix]
    checkpoint("published weights restored")
    raw = refundable_stats(d, WP, civ, union, heads, delta)
    # Release the C-order published matrix immediately; its layout and the
    # full-width dot products are retained to keep floating-point bytes exact.
    del WP, gd
    release_frames()
    refundable_stats(d, W, civ, union, heads, delta, L["flag"], L["onbooks"]["central"])
    mts, model, hf = L["mts"], L["model"], L["hf"]
    ref_line = L["ref_line"]
    gate("raw_refund_share_matches_model", abs(raw["union"][0] - ref_line["keys"]["refundable_credits"]["personal"]["share"]) < 1e-9)
    r6, r6_net = route_r6(L, omega, source_item)
    # Capture only small statistics before discarding the source replay's large locals.
    receipt = {}
    for conv, v in delta.items():
        x = weighted_delta((base.ctc * L["f_other"]) * L["per_fit"], v["nonref"], L["wr"])
        x += weighted_delta((base.cdcc0 * L["f_other"]) * L["per_fit"], v["care"], L["wr"])
        receipt[conv] = -x  # positive credit lowers receipts where the child is assigned
    arrays = {"head_ph": d.PH_SEQ.to_numpy()[heads], "head_pp": d.PPPOS.to_numpy()[heads],
              "raw_union": raw["union"]}
    for conv in omega:
        arrays[f"raw_{conv}"] = raw["delta"][conv]
        arrays[f"receipt_{conv}"] = receipt[conv]
        for kind, values in delta[conv].items():
            arrays[f"delta_{conv}_{kind}"] = values
    directory = CACHE / "source_replay"
    data = directory / "statistics.npz"
    pending = directory / "statistics.pending.npz"
    require_within_budget("source replay, statistics not written")
    np.savez(pending, **arrays)
    metadata = {"pins": source_pins, "data_sha256": sha(pending), "row4_union": row4_union,
                "mts": mts, "model": model, "hf": hf, "ref_line": ref_line,
                "r6": r6, "r6_net": r6_net, "gates": GATES}
    text = json.dumps(metadata, sort_keys=True, indent=1) + "\n"
    if pins() != source_pins:
        raise RuntimeError("[BLOCKED] source replay provenance changed during replay")
    peak = require_within_budget("source replay, statistics not published")
    pending.replace(data)
    (directory / "statistics.json").write_text(text)
    print(f"[timing] source replay {time.perf_counter()-start:.3f}s; peak_footprint_bytes {peak}", flush=True)


def read_source_statistics(source_pins):
    """Fail closed on stale or incomplete subprocess output; never replay here."""
    directory = CACHE / "source_replay"
    metadata = json.loads((directory / "statistics.json").read_text())
    if metadata.get("pins") != source_pins or sha(directory / "statistics.npz") != metadata.get("data_sha256"):
        raise RuntimeError("[BLOCKED] source replay cache provenance mismatch")
    with np.load(directory / "statistics.npz", allow_pickle=False) as stored:
        arrays = {key: stored[key] for key in stored.files}
    return metadata, arrays


def main():
    start = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    source_pins = pins()
    cache = CACHE / "sufficient_statistics.json"
    if "--refresh" not in sys.argv and cache.exists():
        saved = json.loads(cache.read_text())
        if saved.get("pins") == source_pins:
            gate("cached_statistics_sources_match", True)
            peak = require_within_budget("credit cache, nothing written")
            OUT.mkdir(exist_ok=True)
            (OUT / "credit_routing.json").write_text(json.dumps(saved["output"], sort_keys=True, indent=1) + "\n")
            print(f"[timing] cache {time.perf_counter()-start:.3f}s; peak_footprint_bytes {peak}")
            return
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--source-replay"], check=True)
    metadata, arrays = read_source_statistics(source_pins)
    GATES.extend(metadata["gates"])
    row4_union, mts, model, hf, ref_line, r6, r6_net = (
        metadata[k] for k in ("row4_union", "mts", "model", "hf", "ref_line", "r6", "r6_net"))
    delta = {conv: {kind: arrays[f"delta_{conv}_{kind}"] for kind in ("actc", "eitc", "nonref", "care")}
             for conv in "ab"}
    raw = {"union": arrays["raw_union"], "delta": {conv: arrays[f"raw_{conv}"] for conv in "ab"}}
    receipt = {conv: arrays[f"receipt_{conv}"] for conv in "ab"}
    head_keys = pd.MultiIndex.from_arrays([arrays["head_ph"], arrays["head_pp"]])
    F = load_module(HERE / "frame.py", "routing_generation_frame")
    omega = delta  # Only convention keys are needed after the replay.
    checkpoint("source statistics read after child exit")
    # stack_split imports exactly the same hotdeck/status helpers as the published generation stack.
    S = load_module(HERE / "stack_split.py", "routing_stack")
    hotdeck_path = S.c.CACHE / "asec25_lane.parquet"
    d = frame_without_replicates(hotdeck_path, S.c.REPS)
    checkpoint("hotdeck frame read")
    civ, union = S.c.masks(d)
    aligned_omega(F, d)
    # Link heads by person identity, without loading the full source a second time.
    key = pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]])
    hdheads = key.get_indexer(head_keys)
    gate("every_credit_return_head_is_in_hotdeck_frame", bool((hdheads >= 0).all()))
    Wpub = replicate_weights(hotdeck_path, S.c.REPS)
    cells = S.L.acs_cells()
    # Only the adopted arm is needed. weight_arms also constructs three large
    # sensitivity matrices, pushing this consumer above the lane's memory cap.
    W4 = Wpub.copy()
    checkpoint("hotdeck replicate matrices")
    outside = ~d.GESTFIPS.isin(S.L.CA_TX).to_numpy()
    for label, code in (("natz", 4), ("noncit", 5)):
        mask = outside & d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(code).to_numpy()
        W4[mask] *= cells[label] / Wpub[mask].sum(axis=0)
    # Hotdeck reads only pwwgt0; cloning 160 unused replicate columns on every
    # seed dominates peak RSS. The unchanged Wpub/W4 matrices retain every SDR
    # weight for attribution. All ten source controls verify unchanged draws.
    release_frames()
    gate("hotdeck_row4_weights_match_credit_replay_union", abs(W4[union,0].sum()-row4_union)<1e-3)
    status, hh = S.cs.status_inputs()
    checkpoint("hotdeck status read")
    aware = S.L.state_aware_flag(status, hh, d, S.L.STATUS_BLIND_2024)
    configs, _ = S.L.share_configs(d)
    share = configs[("origin", "central")]
    flag_credit = np.asarray(aware, bool)
    # Return-level deltas are in credits.py's head order, not hotdeck person order.
    ref_stats = refundable_stats(d, W4, civ, union, hdheads, delta, flag_credit, share)
    hd = np.load(S.c.CACHE / "hotdeck_key_shares.npz")
    runs = {"matched": [], "pooled": []}
    for seed in S.run_hotdeck.SPECS["main"][1]:
        for variant, cells in [("matched", S.hotdeck.BASE), ("pooled", [])]:
            tick = time.perf_counter()
            print(f"[hotdeck] {seed} {variant}", flush=True)
            new, _ = S.hotdeck.run(d, seed=seed, verbose=False, base=cells, item_property=False)
            checkpoint(f"hotdeck {seed} {variant} draw")
            v = (new.EIT_CRED + new.ACTC_CRD).to_numpy(float)
            share0 = v[union] @ Wpub[union, 0] / (v[civ] @ Wpub[civ, 0])
            want = hd[f"main|{variant}@{seed}|personal|refundable_credits"][0]
            gate(f"hotdeck_{seed}_{variant}_source_positive_control", abs(share0 - want) < 1e-12, float(share0-want))
            runs[variant].append(refundable_stats(new, W4, civ, union, hdheads, delta, flag_credit, share))
            del new
            release_frames()
            checkpoint(f"hotdeck {seed} {variant} freed")
            print(f"[timing] hotdeck {seed} {variant} {time.perf_counter()-tick:.3f}s; peak_footprint_bytes {peak_bytes()}", flush=True)
    mean = {kind: {"union": np.mean([r["union"] for r in seq], axis=0),
                   "delta": {conv: np.mean([r["delta"][conv] for r in seq], axis=0) for conv in omega}}
            for kind, seq in runs.items()}
    meth = {METHODS[0]: mean["matched"]["delta"], METHODS[1]: {}}
    for conv in omega:
        meth[METHODS[1]][conv] = ref_stats["delta"][conv] + ref_stats["union"] * (
            mean["matched"]["delta"][conv] - mean["pooled"]["delta"][conv]) / mean["pooled"]["union"]
    union_shares = {METHODS[0]: mean["matched"]["union"], METHODS[1]: ref_stats["union"]
                    *mean["matched"]["union"]/mean["pooled"]["union"]}
    old_stack = json.loads((HERE / "derived/stack_by_generation.json").read_text())["payloads"]
    for method, sh in union_shares.items():
        got = mts["non_ptc_remainder_bn"]*hf*(sh[0]-raw["union"][0])
        want = old_stack[method]["union"]["spending"]["refundable_tax_credits"]["refundable_credits"]["personal"]
        gate(f"{method}_row4_ssn_stack_source_positive_control", abs(got-want)<1e-9, float(got-want))
    del d, Wpub, W4, status, hh, configs, key
    release_frames()
    checkpoint("hotdeck frames and weights freed before OTA")
    # OTA uses its own published frame's SSN rule, not the stack's state-aware flag.
    E = load_module(HERE / "external_split.py", "routing_external")
    # The historical lanes share the generic module name `frame`; a direct
    # path load makes this consumer immune to earlier generation-frame imports.
    E.xf = load_module(FISCAL / "external_benchmarks_2026_09_24/frame.py", "routing_external_frame")
    external_path = E.xf.CACHE / "cps25_frame.parquet"
    ed = frame_without_replicates(external_path, E.xf.REPS)
    checkpoint("OTA frame read")
    eciv, eu = E.xf.masks(ed)
    ew = replicate_weights(external_path, E.xf.REPS)
    ekeys = pd.MultiIndex.from_frame(ed[["PH_SEQ", "PPPOS"]])
    eheads = ekeys.get_indexer(head_keys)
    gate("every_credit_head_is_in_ota_frame", bool((eheads >= 0).all()))
    un, latin = E.xf.status(ed)
    flag = un & latin
    eit = np.where(flag, 0.0, ed.EIT_CRED.to_numpy(float))
    act = np.where(flag, ed.ACTC_CRD.to_numpy(float)*E.ota_arm.ON_BOOKS["central"], ed.ACTC_CRD.to_numpy(float))
    etotal = (eit+act)[eciv] @ ew[eciv]
    ratios = pd.read_csv(E.EXT / "derived/ota_shares.csv").set_index("item").ratio_ota_to_cps
    ota = {}
    ehf = E.xf.household_fraction(ed, eciv)
    for conv in omega:
        de = weighted_delta(eit[eheads], delta[conv]["eitc"], ew[eheads])
        da = weighted_delta(act[eheads], delta[conv]["actc"], ew[eheads])
        ota[conv] = E.ota_arm.NON_PTC_BN*ehf*((ratios["eitc_ssn_rule"]-1)*de
                                          +(ratios["ctc_on_books_central"]-1)*da)/etotal
    ext = json.loads((HERE / "derived/external_by_generation.json").read_text())
    want = ext["ota"]["union"]["personal"]
    got = E.ota_arm.NON_PTC_BN*ehf*((ratios["eitc_ssn_rule"]-1)*(eit[eu]@ew[eu,0])
                                  +(ratios["ctc_on_books_central"]-1)*(act[eu]@ew[eu,0]))/etotal[0]
    gate("ota_source_positive_control", abs(got-want)<1e-9, float(got-want))
    mrks = ed.MRKS.eq(1).to_numpy(float)
    # The rounded row-1 booking is preserved; only its allocation among generations moves.
    e_raw = refundable_stats(ed, ew, eciv, eu, eheads, delta)
    gap_u = mrks[eu]@ew[eu]/(mrks[eciv]@ew[eciv]) - e_raw["union"]
    gate("row1_all_replicate_share_gaps_nonzero", bool((np.abs(gap_u)>1e-12).all()))
    row1 = {conv: -mts["ptc_effect_on_main_case_bn"] * e_raw["delta"][conv]/gap_u for conv in omega}
    baseline_bn = ref_line["national_bn"]
    nonptc_bn = mts["non_ptc_remainder_bn"]
    base_out, se_out, components, net_se, spending_reps = {}, {}, {}, {}, {}
    fit_line = next(x for x in model["receipts"]["lines"] if x["id"] == "federal_income_tax")
    reference = model["receipts"]["reference"]
    for method in METHODS:
        base_out[method], se_out[method], components[method] = {}, {}, {}
        net_se[method], spending_reps[method] = {}, {}
        for conv in omega:
            parts = {"base": baseline_bn*hf*raw["delta"][conv],
                     "status_row4_hotdeck": nonptc_bn*hf*(meth[method][conv]-raw["delta"][conv]),
                     "ota": ota[conv], "row1_ptc_removal": row1[conv]}
            spending = sum(parts.values())
            spending_reps[method][conv] = spending
            net_se[method][conv] = {}
            base_out[method][conv], se_out[method][conv] = {}, {}
            for j,g in enumerate(GENS):
                receipts = {sc: float(receipt[conv][j,0]*fit_line["cells"][sc]["personal"]["target_bn"]
                                      /fit_line["cells"][reference]["personal"]["target_bn"])
                            for sc in model["receipts"]["scenarios"]}
                base_out[method][conv][g] = {"spending": {"refundable_tax_credits": {"personal": float(spending[j,0])}},
                                            "receipt": {"federal_income_tax": {"personal": receipts}}}
                se_out[method][conv][g] = {"spending": {"refundable_tax_credits": {"personal": sdr(spending[j])}},
                                          "receipt": {"federal_income_tax": {"personal": {sc: sdr(receipt[conv][j])
                                              *fit_line["cells"][sc]["personal"]["target_bn"]
                                              /fit_line["cells"][reference]["personal"]["target_bn"] for sc in receipts}}}}
                net_se[method][conv][g] = {sc:sdr(spending[j]-receipt[conv][j]
                                                *fit_line["cells"][sc]["personal"]["target_bn"]
                                                /fit_line["cells"][reference]["personal"]["target_bn"])
                                          for sc in receipts}
            for label, values in {**parts,"receipt":receipt[conv]}.items():
                gap = float(np.abs(values.sum(axis=0)).max())
                gate(f"{method}_{conv}_{label}_all_replicates_preserve_union", gap<1e-9, gap)
            components[method][conv] = {label:{g:float(v[j,0]) for j,g in enumerate(GENS)} for label,v in parts.items()}
    mean_net_se = {conv:{g:{sc:sdr(np.mean([spending_reps[m][conv][j] for m in METHODS],axis=0)
                                  -receipt[conv][j]*fit_line["cells"][sc]["personal"]["target_bn"]
                                  /fit_line["cells"][reference]["personal"]["target_bn"])
                            for sc in model["receipts"]["scenarios"]} for j,g in enumerate(GENS)} for conv in omega}
    output = {"base":base_out,"se":se_out,"net_cost_se":net_se,"average_net_cost_se":mean_net_se,
              "components":components,"r6_b_parts":r6,"r6_b_net_shift":r6_net,"gates":GATES,
              "meta":{"sign":"spending positive raises spending; receipt positive raises receipts",
                      "scope":"identified union only; no transfer changes the case or added lineage total",
                      "owner_rule":"equal qualifying dependents; union claimant weights follow dollars; outside-union portions retain claimant",
                      "childless_eitc":"no eligible dependent means zero transfer","ptc":"MRKS person component unchanged",
                      "receipt_rule":"Census CTC/ODC and modeled care credit, state-aware onbooks and IRS raked personal key; high-AGI scenario scaled like item5b",
                      "limitations":["equal allocation within a return is an attribution assumption, not child-specific observed tax dollars",
                                      "care credit uses the source lane's model anchored on Census tax; disability exceptions are not observed",
                                      "receipt credits use the base return credits; hotdeck does not persist or recompute CTC_CRD/care components"],
                      "se_rule":"160 SDR survey replicates, conditional on fixed five hotdeck seeds; no imputation SE added",
                      "source_pins":"inputs/credit_pins.json"}}
    peak = require_within_budget("credit replay, nothing written")
    OUT.mkdir(exist_ok=True)
    (OUT / "credit_routing.json").write_text(json.dumps(output, sort_keys=True, indent=1)+"\n")
    (HERE / "inputs").mkdir(exist_ok=True)
    (HERE / "inputs/credit_pins.json").write_text(json.dumps(source_pins,sort_keys=True,indent=1)+"\n")
    cache.write_text(json.dumps({"pins":source_pins,"output":output},sort_keys=True,indent=1)+"\n")
    print(f"[timing] total {time.perf_counter()-start:.3f}s; peak_footprint_bytes {peak}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--source-replay"]:
        replay_source()
    else:
        main()

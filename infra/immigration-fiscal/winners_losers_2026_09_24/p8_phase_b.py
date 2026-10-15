"""Execute the corrected live v8 incidence account and its declared beside arms.

Native-First: reuse the case exporter, CPS frame, source kernels and allocators.
Pin acquisition is explicit; the pricing command never enrolls current bytes.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import itertools
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

import winners_losers as wl
import p7_frames as p7
from p8_incidence import ALL_FIXES, Incidence
from p8_phase_a import load_extra

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived/oct15"
MANIFEST = HERE / "inputs/p8_pins_oct15.json"
COMMIT = "7342b331"


def write(table, name, out=OUT):
    path = out / name
    if name.endswith(".gz"):
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as handle:
                    table.to_csv(handle, index=False, lineterminator="\n", float_format="%.15g")
    else:
        table.to_csv(path, index=False, lineterminator="\n", float_format="%.15g")


def write_json_gzip(data, path):
    with Path(path).open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as stream:
                json.dump(data, stream, indent=1, default=float)
                stream.write("\n")


def source_paths():
    paths = set(json.loads((HERE / "inputs/p8_pins_oct14.json").read_text())["sha256"])
    principals = {
        "main_case_2026_10_15": ["package.cjs", "derived/corrections.json", "derived/corrections_cash.json", "derived/summary.json", "derived/main_case_bands.csv"],
        "generation_account_2026_09_24": ["derived/generation_results_oct15.csv", "derived/generation_summary_oct15.json"],
        "distribution_weights_2026_09_23": ["distribute.py", "derived/case_ends_oct15.json"],
        "debt_legacy_2026_09_23": ["derived/oct15/current_flow_contract.json", "derived/oct15/current_flow_source_parts_2024.csv"],
        "late_arrival_account_line_2026_09_27": ["derived/late_arrival_line_oct15.csv"],
        "sept24_propagation_2026_09_24": ["derived/oct15/real_costs_totals.json", "derived/oct15/real_costs_totals.csv", "derived/oct15/band_variants.json"],
    }
    for lane, names in principals.items():
        paths.update(str((wl.FISCAL / lane / n).relative_to(ROOT)) for n in names)
    for directory in ("within_group_distribution_2026_09_29/derived/oct15", "distribution_weights_2026_09_23/derived/oct15"):
        paths.update(str(p.relative_to(ROOT)) for p in (wl.FISCAL / directory).glob("*") if p.is_file())
    for lane in ("union_completion_2026_10_14", "mixed_unit_removal_2026_10_14", "main_case_2026_10_15"):
        paths.update(str(p.relative_to(ROOT)) for p in (wl.FISCAL / lane).glob("*.py"))
        paths.update(str(p.relative_to(ROOT)) for p in (wl.FISCAL / lane).glob("*.cjs"))
        paths.update(str(p.relative_to(ROOT)) for p in (wl.FISCAL / lane / "derived").glob("*.json"))
        paths.update(str(p.relative_to(ROOT)) for p in (wl.FISCAL / lane / "derived").glob("*.csv"))
    paths.update(str((wl.FISCAL / "generation_account_2026_09_24" / p).relative_to(ROOT)) for p in ("frame.py", "keys.py"))
    from p8_stayers import source_paths as stayer_sources
    paths.update(str(p.relative_to(ROOT)) for p in stayer_sources())
    paths.update(str(OUT.joinpath(name).relative_to(ROOT)) for name in ("p7_trust_inputs.json", "p8_programmes.json", "p8_item_effects.json"))
    paths.update(str(p.relative_to(ROOT)) for p in HERE.glob("*.py"))
    paths.update(str(p.relative_to(ROOT)) for p in HERE.glob("*.cjs"))
    paths.update(str((HERE / "inputs" / p).relative_to(ROOT)) for p in ("phase_a_joint_oct14.csv", "phase_a_joint_channels_oct14.csv"))
    for metadata in (HERE / "_cache").rglob("*metadata*.json"):
        try:
            body = json.loads(metadata.read_text())
            paths.update(str(Path(p).relative_to(ROOT)) for p in body.get("source_paths", []) if Path(p).is_relative_to(ROOT) and ".venv" not in Path(p).parts)
        except (ValueError, TypeError):
            pass
    return sorted(p for p in paths if (ROOT / p).is_file())


def prepare_pins(revise=False):
    if MANIFEST.exists():
        if not revise:
            raise SystemExit("[BLOCKED] oct15 pin manifest exists; explicitly review a revision before replacing it")
        archive = HERE / "_cache/pin_history"
        archive.mkdir(exist_ok=True)
        (archive / (wl.file_sha(MANIFEST) + ".json")).write_bytes(MANIFEST.read_bytes())
    hashes, commits = {}, {}
    for rel in source_paths():
        path = ROOT / rel
        hashes[rel] = wl.file_sha(path)
        result = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "HEAD", "--", rel], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            commit = result.stdout.strip()
            body = wl.git_show(rel, commit)
            if hashlib.sha256(body).hexdigest() == hashes[rel]:
                commits[rel] = commit
    MANIFEST.write_text(json.dumps(dict(case="oct15", source_head=subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(), sha256=hashes, commits=commits,
        rule="explicit reviewed source acquisition; code pins and hashes verified before and after pricing"), indent=1) + "\n")
    print(f"[pins] prepared {len(hashes)} hashes, {len(commits)} immutable source commits")


class SourcePins:
    def __init__(self):
        p7.require("oct15_manifest_exists", MANIFEST.is_file())
        self.manifest = json.loads(MANIFEST.read_text())
        self.used = {}

    def pin(self, path, namespace=wl):
        path = Path(path).resolve()
        rel = str(path.relative_to(ROOT))
        actual = wl.file_sha(path)
        expected = self.manifest["sha256"].get(rel)
        p7.require("source_hash_" + rel, actual == expected, expected=expected, actual=actual)
        commit = self.manifest["commits"].get(rel)
        if commit:
            p7.require("source_commit_" + rel, hashlib.sha256(wl.git_show(rel, commit)).hexdigest() == actual, commit=commit)
        self.used[rel] = actual
        return path

    def finish(self):
        for rel, digest in self.used.items():
            p7.require("final_source_" + rel, wl.file_sha(ROOT / rel) == digest)


def initialize(out):
    wl.configure("oct15", out)
    pins = SourcePins()
    p7.pin = pins.pin
    for path in sorted(HERE.glob("*.py")) + sorted(HERE.glob("*.cjs")):
        pins.pin(path)
    for rel in pins.manifest["commits"]:
        if "/oct15/" in rel or "main_case_2026_10_15" in rel or "generation_results_oct15" in rel:
            pins.pin(ROOT / rel)
    B, _ = wl.load_base()
    d, _ = wl.load_frame(B)
    I = wl.base_inputs(B, d)
    fin = wl.fiscal_inputs()
    fiscal_A = wl.fiscal_one_definition(B, fin)
    fedsplit, fs_info = wl.federal_split(fin)
    deficit = wl.deficit_share_fy2024()
    notes = {}
    ch, totals, meta, ctx = wl.build_frame(B, d, I, fin, fedsplit, deficit, notes)
    print("[Phase B] core account initialized", flush=True)
    meta.update(deficit=deficit, fiscal_A=fiscal_A, federal_split_info=fs_info)
    load_extra(d, B)
    payload = json.loads(pins.pin(wl.FISCAL / wl.CASE["lane"] / "derived/corrections.json").read_text())
    rates = payload["meta"]["capital_return"]["rates"]
    p7.require("real_resource_rate", rates["low"] == .02 and rates["high"] == .03, rates=rates)
    trust = json.loads(pins.pin(out / "p7_trust_inputs.json").read_text())["rows"]
    trust["central"] = {k: (trust["low"][k] + trust["high"][k]) / 2 for k in trust["low"]}
    programmes = json.loads(pins.pin(out / "p8_programmes.json").read_text())["programmes"]
    from p7_nest import build
    nest, nest_table, nest_meta = build(wl, B, d, I, pins.pin, p7.require, p7.check_total)
    print("[Phase B] finite-epsilon controls built", flush=True)
    write(nest_table, "p7_nest_wages.csv", out)
    (out / "p7_nest_inputs.json").write_text(json.dumps(nest_meta, indent=1, default=float) + "\n")
    from p7_credits import crossing_credit_arrays
    legacy = crossing_credit_arrays(d)
    from p8_membership import apply_membership, payer_weights
    d, membership = apply_membership(d, wl.FISCAL, B)
    for path in membership["source_paths"]:
        pins.pin(path)
    weights, payer_cells, payer_audit = payer_weights(d, d.pw.to_numpy(), payload["meta"]["lineage"], wl)
    factor = payload["meta"]["lineage"]["members"]["g3plus"] / payload["meta"]["lineage"]["counts"]["identified_g3plus"]
    legacy_vector = legacy["forward"] + factor * legacy["forward_g3plus"]
    from p8_membership import replacement_credit
    legacy_vector, legacy_audit = replacement_credit(d, weights, legacy_vector, legacy["source_weight"])
    from p8_stayers import load_stayers
    credits = load_stayers(d, weights, wl.FISCAL, HERE / "_cache/oct15/stayers", payload, legacy_credit=legacy_vector)
    credits["metadata"]["replacement_credit_routing"] = legacy_audit
    print("[Phase B] observed membership and source stayer arrays joined", flush=True)
    for path in credits["source_paths"]:
        pins.pin(path)
    from p7_cohorts import cohort_keys
    mw, _ = wl.lineage_group_weights(B, d)
    cohort = cohort_keys(p7.weighted_frame(d, weights), wl, trust["central"], group_weights=mw)
    print("[Phase B] cohort keys built", flush=True)
    for rel in cohort["pins"]:
        pins.pin(ROOT / rel)
    cohorts = {True: cohort, False: cohort}
    model = Incidence(wl, B, d, I, ch, meta, fin, ctx, payload, trust,
        programmes, credits, cohorts, cohorts, nest, nest)
    model.initial_notes = notes
    model.membership = dict(membership, **payer_audit)
    model.configure(ALL_FIXES)
    wl.add_cut_columns(d, I["R_spm"])
    return model, pins, totals


def measure(out):
    start = time.perf_counter()
    p7.GATES.clear()
    p7.GATE_COUNTS.clear()
    wl.GATES.clear()
    model, pins, base_totals = initialize(out)
    rows, channels, cuts, recon, grid = [], [], [], [], []
    for rule, frame, level, arm, epsilon in itertools.product(("a", "b", "c"),
            ("stationary", "cohort30", "cohort10"), wl.LEVELS,
            ("recommended", "stack", "coverage", "item11_attribution"), (None, "eps8.7", "eps17.9")):
        if arm in ("coverage", "item11_attribution") and epsilon:
            continue
        tags = dict(case="oct15", financing=rule, frame=frame, level=level, arm=arm, epsilon=epsilon or "infinite", population="lineage")
        p7.GATE_SCOPE = "/".join(str(v) for v in tags.values())
        sharing, pieces, future, boundary = model.evaluate(rule, frame, level, arm, level, epsilon)
        for mode, vector in sharing.items():
            rows.append(p7.summary_row(model.d, model.weights, vector, sharing=mode, future_bn=-future, **tags))
            cuts.extend(p7.cut_rows(model.d, model.weights, vector, dict(sharing=mode, **tags), wl.CUT_COLUMNS))
        for channel, vector in pieces.items():
            channels.append(dict(channel=channel, total_bn=p7.total(vector, model.weights), **tags))
        channels.append(dict(channel="future_cohorts", total_bn=-future, **tags))
        if boundary:
            recon.append(dict(**tags, **boundary))
    for rule, frame, level, arm, setting in itertools.product(("a", "b", "c"),
            ("stationary", "cohort30", "cohort10"), ("low", "high"), ("recommended", "stack"), wl.LEVELS):
        tags = dict(case="oct15", financing=rule, frame=frame, level=level, arm=arm, social_setting=setting)
        p7.GATE_SCOPE = "uncertainty/" + "/".join(str(v) for v in tags.values())
        sharing, _, future, _ = model.evaluate(rule, frame, level, arm, setting)
        for mode, vector in sharing.items():
            grid.append(p7.summary_row(model.d, model.weights, vector, sharing=mode, future_bn=-future, **tags))
    shares = pd.DataFrame(rows)
    channel_table = pd.DataFrame(channels)
    write(shares, "p7_net_shares.csv", out)
    write(channel_table, "p7_channel_table.csv", out)
    write(pd.DataFrame(cuts), "p7_cuts.csv.gz", out)
    write(pd.DataFrame(recon), "p7_mixed_reconciliation.csv", out)
    gt = pd.DataFrame(grid)
    write(gt, "p7_social_grid.csv", out)
    extremes = []
    for _, group in gt.groupby(["financing", "frame", "sharing"]):
        for label, column, fn in (("share_min", "winners_share", "idxmin"), ("share_max", "winners_share", "idxmax"), ("dollar_min", "total_bn", "idxmin"), ("dollar_max", "total_bn", "idxmax")):
            extremes.append(dict(extreme=label, **group.loc[getattr(group[column], fn)()].to_dict()))
    write(pd.DataFrame(extremes), "p7_grid_extrema.csv", out)
    write(model.payer_cells, "p7_payer_cells.csv", out)
    social_values = model.context("a")["social_values"]
    wl.core_registry(base_totals, model.meta, model.fin, social=social_values).to_csv(
        out / "channels.csv", index=False, lineterminator="\n", float_format="%.15g")
    write(pd.DataFrame([dict(item=k, **{f"{L}_bn": v[L] for L in wl.LEVELS})
        for k,v in social_values.items()]), "p7_channel_coverage.csv", out)
    from p8_ablations import measure as measure_ablations, ledger
    measure_ablations(model, out, write)
    ledger(model, out, write)
    from p8_group_frame import produce_group_frame
    produce_group_frame(model, out)
    mappings = [("shares", "p7_net_shares.csv", "select financing, frame, level, arm, epsilon, population, sharing explicitly"),
                ("cuts", "p7_cuts.csv.gz", "gzip; same explicit scenario tags, plus cut and group"),
                ("channels", "p7_channel_table.csv", "select financing, frame, level, arm, epsilon explicitly; mixed_boundary only with mixed_unit"),
                ("uncertainty extrema", "p7_grid_extrema.csv", "social low/central/high from live producer; labelled dollar/share extrema"),
                ("isolated source items", "p8_isolated_channels.csv", "source-isolated fiscal changes at actual endpoints; fixed current incidence keys"),
                ("controlled beside arms", "p8_ablations.csv", "leave one source item/social correction out, named budget variants; explicit frames"),
                ("both pension sets", "p8_channel_ledger.csv", "basis=set/cash; end=low/high; current debt-class rows plus social; no historical debt stock")]
    write(pd.DataFrame(mappings, columns=["memo_table","file","selection"]), "p7_table_map.csv", out)
    pins.finish()
    from p7_cohorts import FISCAL
    sys.path.insert(0, str(FISCAL / "scripts"))
    from memory_budget import require_within_budget
    memory = require_within_budget()
    audit = dict(case="oct15", stationary_verdict=True, membership=model.membership,
        population=model.payload["meta"]["population_v8"],
        credits=model.credits["metadata"], notes=dict(initial=model.initial_notes, incidence=model.notes),
        details=model.details, source_pins=pins.used, memory_limit_bytes=2_500_000_000,
        social_uncertainty_rule="live current row levels; declared producer ratios on those rows; budget PM counterflows have point values rather than historical consumer-PM ranges",
        pooling_item11_rule="budget includes every item11 part; person resources use raw tax/benefit before-after flows; fixed-pool movements are attribution beside; pooling adds only its boundary residual")
    (out / "p7_inputs.json").write_text(json.dumps(audit, indent=1, default=float) + "\n")
    combined_gates = {**{"core/"+k:v for k,v in wl.GATES.items()}, **p7.GATES}
    write_json_gzip(combined_gates, out / "p7_gates.json.gz")
    oversized = {p.name:p.stat().st_size for p in out.iterdir() if p.is_file() and p.stat().st_size >= 10_000_000}
    if oversized:
        raise RuntimeError("[BLOCKED] derived artifacts exceed file-size contract: " + str(oversized))
    receipt = dict(wall_seconds=time.perf_counter()-start, user_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                   system_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime, memory=memory)
    with (HERE / "_cache/oct15_timings.jsonl").open("a") as handle:
        handle.write(json.dumps(receipt) + "\n")
    print("[Phase B] " + json.dumps(dict(rows=len(shares), gates=len(p7.GATES), **receipt)), flush=True)


def run(out_dir=None):
    out = Path(out_dir) if out_dir is not None else OUT
    out.mkdir(parents=True, exist_ok=True)
    measure(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-pins", action="store_true")
    parser.add_argument("--revise-pins", action="store_true", help="explicit source revision, retaining previous manifest by hash")
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.prepare_pins or args.revise_pins:
        prepare_pins(revise=args.revise_pins)
    else:
        measure(args.out_dir)


if __name__ == "__main__":
    main()

"""Measure twelve isolated round-two fixes and their joint v7 effect in scratch.

Native-First: frozen lane inputs plus existing allocation APIs; no Git writes.
Pin preparation is an explicit command. A missing manifest always stops pricing.
"""
from __future__ import annotations

import argparse
import cProfile
import hashlib
import io
import itertools
import json
import resource
import sys
import tempfile
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

import winners_losers as wl
import p7_frames as p7
from p8_incidence import ALL_FIXES, EXTRA_FIELDS, Incidence, frozen_module

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "inputs/p8_pins_oct14.json"
BASE = HERE / "derived/oct14"
ROOT = HERE.parents[2]


def added_sources():
    fiscal = HERE.parent
    return [
        HERE / "inputs/p8_epsilon_sources.json", HERE / "inputs/p8_programmes_oct14.json",
        fiscal / "air_pollution_2026_09_28/derived/mortality_rates.csv",
        fiscal / "air_pollution_2026_09_28/derived/mortality_age_contexts.csv",
        fiscal / "air_pollution_2026_09_28/_cache/lt2024_Table01.xlsx",
        fiscal / "road_crash_externality_2026_09_28/_cache/fars2023/FARS2023NationalCSV/person.csv",
        fiscal / "housing_transfer_2026_09_23/derived/inputs_land_foreign.csv",
        fiscal / "state_priced_services_2026_09_29/derived/state_per_capita.csv",
        fiscal / "state_priced_services_2026_09_29/derived/corrections.csv",
        fiscal / "state_priced_services_2026_09_29/derived/prison_cost_by_state.csv",
        fiscal / "school_cost_where_enrolled_2026_09_24/derived/state_breakdown.csv",
        fiscal / "school_cost_where_enrolled_2026_09_24/derived/within_district.json",
        fiscal / "debt_legacy_2026_09_23/derived/oct14/federal_shares_by_year.csv",
        fiscal / "debt_legacy_2026_09_23/derived/oct14/federal_split_2024_lines.csv",
        fiscal / "gen_ledger_extension_2026_09_16/extend_ledger.py",
        fiscal / "scripts/memory_budget.py",
        ROOT / "sources/immigration-fiscal/data/external/cps_asec_doc/ddl25.txt",
        BASE / "fiscal_specs.csv", BASE / "fiscal_lines_band_ends.csv",
        BASE / "p7_trust_inputs.json", BASE / "p7_net_shares.csv",
        BASE / "p7_cuts.csv", BASE / "p7_channel_table.csv",
    ]


def prepare_pins(out):
    """Explicit source-acquisition operation; never called by the pricing route."""
    if MANIFEST.exists():
        raise SystemExit("[BLOCKED] manifest already exists; review any revision explicitly")
    original = json.loads((HERE / "inputs/pins.json").read_text())
    export = out / "p8_programmes.json"
    if not export.is_file():
        raise SystemExit("[BLOCKED] run p7_inputs.cjs --jurisdiction --out-dir SCRATCH first")
    (HERE / "inputs/p8_programmes_oct14.json").write_bytes(export.read_bytes())
    expected = dict(original["sha256"])
    for path in added_sources():
        expected[str(path.relative_to(ROOT))] = wl.file_sha(path)
    MANIFEST.write_text(json.dumps(dict(sha256=expected,
        rule="explicit Phase-A acquisition; existing p7 pins retained; added health/geography/CPS fields declared here",
        source_vintage="frozen oct14 fiscal and social input; live producer recipient vectors pinned separately"), indent=1) + "\n")
    print(f"[pins] explicitly prepared {MANIFEST}; {len(expected)} inputs")


class SourcePins:
    def __init__(self, B):
        p7.require("p8_manifest_exists", MANIFEST.is_file(), manifest=str(MANIFEST))
        self.expected = json.loads(MANIFEST.read_text())["sha256"]
        self.used = {}
        self.B = B

    def pin(self, path, namespace=wl):
        path = Path(path).resolve()
        key = str(path.relative_to(ROOT))
        if key == f"{wl.BASE_REL}/distribute.py":
            # The actual executable source is the pinned git blob loaded by
            # load_base, not a peer's concurrent oct15 working-tree edit.
            body = wl.git_show(key, wl.CASE["base"])
            digest = hashlib.sha256(body).hexdigest()
            p7.require("frozen_distribution_module_hash", digest == self.expected[key], sha256=digest)
            self.used[f"git:{wl.CASE['base']}:{key}"] = digest
            return path
        digest = wl.file_sha(path)
        p7.require(f"input_pin_{key}", self.expected.get(key) == digest, sha256=digest)
        p7.require(f"within_run_input_{key}", key not in self.used or self.used[key] == digest)
        self.used[key] = digest
        return path

    def final_check(self):
        for key, digest in self.used.items():
            actual = hashlib.sha256(wl.git_show(key.split(":", 2)[2], key.split(":", 2)[1])).hexdigest() if key.startswith("git:") else wl.file_sha(ROOT / key)
            p7.require(f"final_pin_{key}", actual == digest)


def load_extra(d, B):
    p7.extra_fields(d, B)
    with zipfile.ZipFile(B.PATHS["cps"]) as archive:
        source = pd.read_csv(archive.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", *EXTRA_FIELDS])
    p7.require("p8_extra_person_join", np.array_equal(d[["PH_SEQ", "PPPOS"]], source[["PH_SEQ", "PPPOS"]]))
    for name in EXTRA_FIELDS:
        d[name] = source[name].to_numpy()


def initialize(out):
    wl.configure("oct14", out)
    for name in ("fiscal_specs.csv", "fiscal_lines_band_ends.csv"):
        (out / name).write_bytes((BASE / name).read_bytes())
    B, _ = wl.load_base()
    pins = SourcePins(B)
    for path in added_sources():
        pins.pin(path)
    # Keep p7's historical expected hashes and use the explicit extension for
    # newly declared sources; no normal path acquires pins.
    d, _ = wl.load_frame(B)
    I = wl.base_inputs(B, d)
    for case in ("oct07", "oct14"):
        wl.regression(B, d, I, case)
    fin = wl.fiscal_inputs()
    fiscal_A = wl.fiscal_one_definition(B, fin)
    fedsplit, _ = wl.federal_split(fin)
    deficit = wl.deficit_share_fy2024()
    notes = {}
    ch, _, meta, ctx = wl.build_frame(B, d, I, fin, fedsplit, deficit, notes)
    meta.update(deficit=deficit, fiscal_A=fiscal_A)
    load_extra(d, B)
    payload = json.loads(pins.pin(wl.FISCAL / wl.CASE["lane"] / "derived/corrections.json").read_text())
    rates = payload["meta"]["capital_return"]["rates"]
    p7.require("adopted_capital_real_resource_rate", rates["low"] == .02 and rates["high"] == .03,
               low=rates["low"], high=rates["high"], concept="imputed real resource cost; never borrowing")
    exported = json.loads((BASE / "p7_trust_inputs.json").read_text())
    trust = exported["rows"]
    trust["central"] = {k: (trust["low"][k] + trust["high"][k]) / 2 for k in trust["low"]}
    programmes = json.loads((HERE / "inputs/p8_programmes_oct14.json").read_text())["programmes"]
    from p7_credits import crossing_credit_arrays
    credits = crossing_credit_arrays(d)
    for path in credits["metadata"]["source_paths"]:
        p = Path(path)
        if p.is_relative_to(ROOT) and ".venv" not in p.parts and "__pycache__" not in p.parts:
            pins.pin(p)
    old_nest_module = frozen_module(wl, "p7_nest")
    nest_old, _, _ = old_nest_module.build(wl, B, d, I, pins.pin, p7.require, p7.check_total)
    from p7_nest import build
    nest_new, nest_table, nest_meta = build(wl, B, d, I, pins.pin, p7.require, p7.check_total)
    write(nest_table, out / "phase_a_epsilon_wages.csv")
    (out / "phase_a_epsilon_inputs.json").write_text(json.dumps(nest_meta, indent=1, default=float) + "\n")
    from p7_cohorts import cohort_keys
    old_cohort_module = frozen_module(wl, "p7_cohorts")
    from p8_recipient_keys import lineage_payers_state_age
    mw, _ = wl.lineage_group_weights(B, d)
    old_weights, _ = p7.lineage_payers(d, d.pw.to_numpy(), payload["meta"]["lineage"], wl)
    new_weights, _ = lineage_payers_state_age(d, d.pw.to_numpy(), payload["meta"]["lineage"], wl)
    old_cohort, new_cohort = {}, {}
    for geographic, weights in ((False, old_weights), (True, new_weights)):
        dd = p7.weighted_frame(d, weights)
        old_cohort[geographic] = old_cohort_module.cohort_keys(dd, wl, trust["central"], group_weights=mw)
        new_cohort[geographic] = cohort_keys(dd, wl, trust["central"], group_weights=mw)
        for path in new_cohort[geographic]["pins"]:
            pins.pin(ROOT / path)
    model = Incidence(wl, B, d, I, ch, meta, fin, ctx, payload, trust,
                      programmes, credits, old_cohort, new_cohort, nest_old, nest_new)
    model.initial_notes = notes
    return model, pins


def write(table, path):
    table.to_csv(path, index=False, lineterminator="\n", float_format="%.15g")


def measure(out, only_baseline=False):
    started = time.perf_counter()
    p7.GATES.clear()
    p7.GATE_COUNTS.clear()
    model, pins = initialize(out)
    rows, channels, cuts, recon, grid, audits = [], [], [], [], [], []
    scenarios = [("baseline", frozenset())]
    if not only_baseline:
        scenarios += [(f"fix_{i}", {i}) for i in range(1, 13)] + [("joint", ALL_FIXES)]
    for name, fixes in scenarios:
        p7.GATE_SCOPE = name
        model.configure(fixes)
        for rule, frame, level, arm, epsilon in itertools.product(
                ("a", "b", "c"), ("stationary", "cohort30", "cohort10"),
                wl.LEVELS, ("recommended", "stack", "coverage"), (None, "eps8.7", "eps17.9")):
            # Coverage is its own matched comparator, ε arms are beside the
            # central infinity. Keep arms out of combinations without meaning.
            if arm == "coverage" and epsilon is not None:
                continue
            tags = dict(fix=name, financing=rule, frame=frame, level=level, arm=arm, epsilon=epsilon or "infinite")
            p7.GATE_SCOPE = "/".join(str(v) for v in tags.values())
            settings = ["central"]
            if 5 in fixes and level != "central":
                settings = [level]
            share, pieces, future, boundary = model.evaluate(rule, frame, level, arm, settings[0], epsilon)
            for sharing, vector in share.items():
                rows.append(p7.summary_row(model.d, model.weights, vector, sharing=sharing, future_bn=-future, **tags))
                cuts.extend(p7.cut_rows(model.d, model.weights, vector, dict(sharing=sharing, **tags), ["state3", "tenure"]))
            for channel, vector in pieces.items():
                channels.append(dict(channel=channel, total_bn=p7.total(vector, model.weights), **tags))
            channels.append(dict(channel="future_cohorts", total_bn=-future, **tags))
            if boundary:
                diagnostic = {k: boundary.pop(k) for k in ("other_before_level_bn", "other_after_level_bn", "removal_level_change_diagnostic_bn")}
                print("[removal-level diagnostic only] " + json.dumps(dict(**tags, **diagnostic)), flush=True)
                recon.append(dict(**tags, **boundary))
        if name in ("baseline", "fix_5", "joint"):
            for rule, frame, level, arm, setting in itertools.product(("a", "b", "c"), ("stationary", "cohort30"),
                    ("low", "high"), ("recommended", "stack"), ("low", "central", "high")):
                tags = dict(fix=name, financing=rule, frame=frame, level=level, arm=arm, social_setting=setting)
                p7.GATE_SCOPE = "grid/" + "/".join(str(v) for v in tags.values())
                share, _, future, _ = model.evaluate(rule, frame, level, arm, setting)
                for sharing in ("person", "pooled", "mixed_unit"):
                    grid.append(p7.summary_row(model.d, model.weights, share[sharing], sharing=sharing, future_bn=-future, **tags))
        audits.append(dict(fix=name, notes=model.notes, payer_cells=model.payer_cells.to_dict("records"), details=model.details))
        model.details = []
        print(f"[Phase A] {name}: measurements complete", flush=True)
    results, channel_table = pd.DataFrame(rows), pd.DataFrame(channels)
    reference_keys = ["financing", "frame", "level", "arm", "epsilon", "sharing"]
    baseline = results[results.fix.eq("baseline")][reference_keys + ["total_bn", "winners_share"]].rename(
        columns={"total_bn": "baseline_total_bn", "winners_share": "baseline_winners_share"})
    results = results.merge(baseline, on=reference_keys, validate="many_to_one")
    results["delta_total_bn"] = results.total_bn - results.baseline_total_bn
    results["delta_ahead_pp"] = 100 * (results.winners_share - results.baseline_winners_share)
    ck = ["financing", "frame", "level", "arm", "epsilon", "channel"]
    base_ch = channel_table[channel_table.fix.eq("baseline")][ck + ["total_bn"]].rename(columns={"total_bn": "baseline_total_bn"})
    channel_table = channel_table.merge(base_ch, on=ck, how="left", validate="many_to_one")
    channel_table["delta_bn"] = channel_table.total_bn - channel_table.baseline_total_bn.fillna(0)
    # Frozen oracle, measured before any correction. It is not loosened by the
    # fact that the corrected scenario intentionally changes incidence.
    prior = pd.read_csv(BASE / "p7_net_shares.csv")
    control = results[results.fix.eq("baseline") & results.arm.isin(["recommended", "stack"]) & results.epsilon.eq("infinite")]
    old = prior[prior.population.eq("lineage") & prior.arm.isin(["recommended", "stack"])]
    matched = control.merge(old, on=["financing", "frame", "level", "arm", "sharing"], suffixes=("_new", "_old"), validate="one_to_one")
    p7.GATE_SCOPE = "final"
    write(matched, out / "phase_a_positive_control.csv")
    p7.require("frozen_v7_positive_control", len(matched) == 108 and
               abs(matched.total_bn_new - matched.total_bn_old).max() < 5e-7 and
               abs(matched.winners_share_new - matched.winners_share_old).max() < 5e-11,
               rows=len(matched), max_total_gap_bn=float(abs(matched.total_bn_new-matched.total_bn_old).max()),
               max_share_gap=float(abs(matched.winners_share_new-matched.winners_share_old).max()))
    gt = pd.DataFrame(grid)
    extrema = []
    for _, frame in gt.groupby(["fix", "financing", "frame", "sharing"]):
        for label, column, function in (("share_min", "winners_share", "idxmin"), ("share_max", "winners_share", "idxmax"),
                                        ("dollar_min", "total_bn", "idxmin"), ("dollar_max", "total_bn", "idxmax")):
            extrema.append(dict(extreme=label, **frame.loc[getattr(frame[column], function)()].to_dict()))
    for table, filename in ((results, "phase_a_shares.csv"), (channel_table, "phase_a_channels.csv"),
                            (pd.DataFrame(cuts), "phase_a_cuts.csv"), (pd.DataFrame(recon), "phase_a_mixed_levels.csv"),
                            (gt, "phase_a_social_grid.csv"), (pd.DataFrame(extrema), "phase_a_grid_extrema.csv")):
        write(table, out / filename)
    pins.final_check()
    (out / "phase_a_gates.json").write_text(json.dumps(p7.GATES, indent=1, default=float) + "\n")
    (out / "phase_a_audit.json").write_text(json.dumps(dict(scenarios=audits, base_notes=model.initial_notes,
        source_sha256=pins.used, source_vintage="frozen oct14 fiscal/social; pinned recipient age and state-price producer vectors",
        grid_rule="finite coherent producer low/central/high vectors × fiscal ends × recommended/stack; not all independent combinations or universal bounds",
        mixed_rule="presence effect = before pooled levels minus after removal; removal-level changes are labelled diagnostics in the run log only",
        state_rule="state-priced spending shares applied to net state-local financing cost; receipt geography not independently identified",
        trust_cash_surplus_bn=model.trust["central"]["payroll_bn"]-model.trust["central"]["cash_benefits_bn"]), indent=1, default=float) + "\n")
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    footprint = require_within_budget("winners Phase A")
    usage = resource.getrusage(resource.RUSAGE_SELF)
    (out / "phase_a_timing.json").write_text(json.dumps(dict(seconds=time.perf_counter()-started,
        physical_footprint_bytes=footprint, descriptive_ru_maxrss=usage.ru_maxrss,
        user_seconds=usage.ru_utime, system_seconds=usage.ru_stime), indent=1) + "\n")
    print(f"[Phase A] {len(results)} rows; {len(p7.GATES)} gates; peak footprint {footprint/1e9:.3f} GB", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--prepare-pins", action="store_true")
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--only-baseline", action="store_true", help="probe frozen control before the full ablation grid")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    temp_roots = {Path(tempfile.gettempdir()).resolve(), Path("/tmp").resolve()}
    if out.is_relative_to(HERE / "derived") or not any(out.is_relative_to(root) for root in temp_roots):
        raise SystemExit("[BLOCKED] Phase A writes only to an explicit system temporary directory")
    out.mkdir(parents=True, exist_ok=True)
    if args.prepare_pins:
        prepare_pins(out)
    elif args.profile:
        profile = cProfile.Profile()
        try:
            profile.runcall(measure, out, args.only_baseline)
        finally:
            profile.dump_stats(str(out / "phase_a_profile.pstat"))
    else:
        measure(out, args.only_baseline)


if __name__ == "__main__":
    main()

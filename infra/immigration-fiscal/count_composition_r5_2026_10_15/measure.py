"""Items 16/17: survey calibration and conditional tenure price transfer.

Native-First: integrate the adopted consumer's own signed fiscal piece vectors.
The roster, budgets, responses, production coefficients and latent stock stay
fixed. This is a survey-weight calibration, not a new household removal model.
"""
import csv
from datetime import datetime, timezone
import gc
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

from tenure import C, FISCAL, LANE, fixed_count_tenure, load, require, tenure_rates, transfer_count_tenure
from mixed_interaction import item10_flags

COVER = FISCAL / "coverage_bound_2026_10_14"
CASE = FISCAL / "main_case_2026_10_15/derived"
OUT = LANE / "derived"
GENS = ("G1", "G2", "G3plus")
ENDS = ("low", "high")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def write_csv(path, rows):
    require(bool(rows), "no CSV rows")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_kernel(basis):
    audit_path = COVER / f"derived/pricing_audit_oct15_final_routing_{basis}.json"
    audit = json.loads(audit_path.read_text())
    manifest = COVER / f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json"
    cache = COVER / f"_cache/oct15_final_routing/{basis}/pricing.npz"
    C.validate_cache_receipt(audit, manifest, cache)
    require(audit["case"] == "oct15" and audit["basis"] == basis, "pricing case/set identity")
    with np.load(cache) as archive:
        # Full replicate net prices are not retained alongside the piece matrix.
        data = {key: archive[key] for key in ("weights", "added_weights", "generation", "age", "sex",
                "arrival", "hispanic", "person_ph_seq", "person_pppos", "base_piece_prices",
                "constructed_piece_prices", "other_piece_prices")}
        data["net_id0"] = archive["net_id"][:, :, 0].copy()
        data["net_added0"] = archive["net_added"][:, :, 0].copy()
        data["excluded0"] = archive["excluded_use_prices"][:, :, 0].copy()
    require(np.isfinite(data["base_piece_prices"]).all(), "nonfinite fiscal price")
    return data, audit, [audit_path, manifest, cache]


def person_inputs(data):
    fields = ["PH_SEQ", "PPPOS", "H_TENURE", "A_AGE", "A_SEX", "PRDTHSP", "PRCITSHP"]
    frame = pd.read_parquet(FISCAL / "generation_account_2026_09_24/_cache/asec25_generation.parquet", columns=fields)
    factors = pd.read_parquet(OUT / "native_person_factors.parquet")
    keys = pd.MultiIndex.from_arrays([data["person_ph_seq"], data["person_pppos"]])
    require(keys.is_unique, "duplicate kernel identities")
    matched = frame.set_index(["PH_SEQ", "PPPOS"]).reindex(keys)
    calibrated = factors.set_index(["PH_SEQ", "PPPOS"]).reindex(keys)
    require(not matched.isna().any().any() and not calibrated.isna().any().any(), "incomplete person/factor join")
    require(np.array_equal(matched.A_AGE, data["age"]) and np.array_equal(matched.A_SEX, data["sex"]), "person demographics alignment")
    return matched.H_TENURE.to_numpy(int), calibrated.central_member_factor.to_numpy(float)


def summarize_pieces(data, audit, observed_delta, missing_delta, observed_added_delta=None):
    """Keep observed use prices; missing people exclude complete justice use."""
    rows = []
    if observed_added_delta is None:
        observed_added_delta = np.zeros_like(observed_delta)
    for i, piece in enumerate(audit["denominator_pieces"]):
        a = float(data["base_piece_prices"][i] @ (observed_delta+observed_added_delta))
        b = float(data["constructed_piece_prices"][i] @ missing_delta)
        rows.append(dict(end=piece["end"], generation=piece["generation"],
            line=piece["line"], source_line=piece["source_line"], source_side=piece["source_side"],
            category=piece["category"], economic_class=piece["economic_class"],
            level=piece["level"], observed_change_bn=a, coverage_change_bn=b, change_bn=a+b,
            complete_use_excluded=piece["administratively_complete_use"]))
    for i, piece in enumerate(audit["other_pieces"]):
        # Original nonreporting descendants' counts/prices stay fixed.
        eligible = piece["population"] != "added"
        mass = {"both": observed_delta+observed_added_delta,
                "identified": observed_delta, "added": observed_added_delta}[piece["population"]]
        a = float(data["other_piece_prices"][i] @ mass)
        b = float(data["other_piece_prices"][i] @ missing_delta) if eligible else 0.0
        rows.append(dict(end=piece["end"], generation=piece["generation"], line=piece["line"],
            source_line=piece["line"], source_side="post_engine", category="residual",
            economic_class="unclassified_residual", level="unclassified",
            observed_change_bn=a, coverage_change_bn=b, change_bn=a+b, complete_use_excluded=False))
    ends = {}
    for i, end in enumerate(ENDS):
        selected = [p for p in rows if p["end"] == end]
        by_gen = {g: sum(p["change_bn"] for p in selected if p["generation"] == g) for g in GENS}
        total = sum(by_gen.values())
        principal = float(data["net_id0"][i] @ observed_delta + data["net_added0"][i] @ observed_added_delta
                          + (data["net_id0"][i]-data["excluded0"][i]) @ missing_delta)
        require(abs(total-principal) < 1e-9, "fiscal piece/net profile closure")
        ends[end] = dict(total_bn=total, by_generation_bn=by_gen,
                         observed_bn=sum(p["observed_change_bn"] for p in selected),
                         coverage_bn=sum(p["coverage_change_bn"] for p in selected))
    return ends, rows


def compute(basis, coverage, population):
    data, audit, dependencies = load_kernel(basis)
    tenure, factor = person_inputs(data)
    payload = json.loads((CASE / f"corrections{'_cash' if basis == 'cash' else ''}.json").read_text())
    flags = item10_flags(data, payload)
    w = data["weights"][:, 0]
    # Cache separates item10 reporters from nonreporting children (in added_weights).
    row4 = float(w.sum()-w[flags["reporter"]].sum())
    require(abs(row4-39_712_493.331187896) < 1, "original-union row4 population gate")
    require(np.all(factor[data["age"] >= 18] == 1), "native recalibration alters adults")
    rates, base = load()
    cross = tenure_rates()
    f, _ = C.factors(data, rates, base)
    native_w = w*factor
    # These are actual item10 nonreporting children, not synthetic descendants.
    completion_delta = data["added_weights"][:, 0]*(factor-1)*flags["nonreporter"]
    fixed, cells = fixed_count_tenure(data, tenure, w, rates, base, cross)
    joint_fixed, joint_cells = fixed_count_tenure(data, tenure, native_w, rates, base, cross)
    transfer = transfer_count_tenure(data, tenure, rates, base, cross)
    zero = np.zeros_like(w)
    scenarios = {
        "unchanged": (zero, zero, w, f),
        "item16": (native_w-w, native_w*f-w*f, native_w, f),
        "item17": (zero, w*(fixed-f), w, fixed),
        "joint": (native_w-w, native_w*joint_fixed-w*f, native_w, joint_fixed),
        "item17_count_transfer": (zero, w*(transfer-f), w, transfer),
        "joint_count_transfer": (native_w-w, native_w*transfer-w*f, native_w, transfer),
    }
    result, all_parts, count_rows = {}, [], []
    old_counts = coverage["sets"][basis]["implied_net_missing_people"]
    for name, (observed, missing, neww, newf) in scenarios.items():
        changed_completion = completion_delta if name.startswith("joint") or name == "item16" else zero
        ends, parts = summarize_pieces(data, audit, observed, missing, changed_completion)
        observed_by_gen = {g: float((observed+changed_completion)[data["generation"] == i].sum()) for i, g in enumerate(GENS)}
        missing_by_gen = {g: float(missing[data["generation"] == i].sum()) for i, g in enumerate(GENS)}
        population_delta = sum(observed_by_gen.values()) + sum(missing_by_gen.values())
        for end in ENDS:
            ends[end]["per_v8_member_usd"] = ends[end]["total_bn"]*1e9/population
        result[name] = dict(by_end=ends, observed_people_change_by_generation=observed_by_gen,
            coverage_people_change_by_generation=missing_by_gen, population_change=population_delta,
            coverage_counts_by_generation={g: old_counts[g]+missing_by_gen[g] for g in GENS},
            scope="fixed-roster survey calibration at v8 signed piece prices; national key masses, coefficients and production attribution fixed")
        all_parts.extend(dict(scenario=name, **part) for part in parts)
        for generation in range(3):
            for age in np.unique(data["age"]):
                for sex in (1, 2):
                    m = (data["generation"] == generation) & (data["age"] == age) & (data["sex"] == sex)
                    if not m.any():
                        continue
                    count_rows.append(dict(scenario=name, generation=GENS[generation], age=int(age), sex=sex,
                        old_coverage_people=float((w[m]*f[m]).sum()), new_coverage_people=float((neww[m]*newf[m]).sum()),
                        new_owner_people=float((neww[m & (tenure == 1)]*newf[m & (tenure == 1)]).sum()),
                        new_renter_people=float((neww[m & (tenure != 1)]*newf[m & (tenure != 1)]).sum())))
    # Cache's final-routing refresh is held constant and is not smuggled into either item.
    routing_gap = {}
    for i, end in enumerate(ENDS):
        got = float((data["net_id0"][i]-data["excluded0"][i]) @ (w*f))
        expected = coverage["sets"][basis]["ends"][end]["total_bn"]
        routing_gap[end] = got-expected
        require(abs(routing_gap[end]) < .5, "final routing exceeds adopted tolerance")
    # Central fixed counts are checked in exact current age x sex x generation cells.
    require(abs(result["item17"]["population_change"]) < 1e-6, "tenure-only fixed counts")
    require(abs(result["joint"]["population_change"]-result["item16"]["population_change"]) < 1e-6,
            "joint tenure preserves revised native coverage counts")
    write_csv(OUT / f"line_parts_{basis}.csv", all_parts)
    if basis == "set":
        write_csv(OUT / "coverage_cells.csv", count_rows)
        write_csv(OUT / "tenure_preservation.csv", [dict(base="v8", **r) for r in cells]
                  + [dict(base="item16", **r) for r in joint_cells])
    meta = dict(row4_original_union=row4, final_routing_gap_held_fixed_bn=routing_gap,
        reporter_records=int(flags["reporter"].sum()), nonreporter_records=int(flags["nonreporter"].sum()),
        native_weight_change_reporters=float((w*(factor-1))[flags["reporter"]].sum()),
        native_weight_change_observed_nonreporters=float(completion_delta.sum()),
        central_tenure_rule="Table D all-age net-omission odds, normalized within exact current age x sex x generation PES cells; DA under-five part unchanged",
        transfer_arm="actual Table D tenure x Census-age x sex cells, with V2024 absorption; counts may change",
        no_cash_rent_rule="H_TENURE 3 included in renter; same occupied nonowner definition as Census tenure",
        fixed=["national budgets/key masses", "response settings including item9", "latent nonreporting stock/age mix",
               "household rosters/keys and filing units", "item11 generation allocation rule", "production coefficients"])
    del data
    gc.collect()
    return result, meta, dependencies


def main():
    start = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    (LANE / "_cache").mkdir(exist_ok=True)
    summary = json.loads((CASE / "summary.json").read_text())
    coverage = json.loads((COVER / "derived/coverage_bound_oct15.json").read_text())
    population = summary["v8"]["population"]["with_coverage"]
    sets, metadata, sources = {}, {}, set()
    for basis in ("set", "cash"):
        sets[basis], metadata[basis], dependencies = compute(basis, coverage, population)
        sources.update(dependencies)
    for basis in sets:
        for name, entry in sets[basis].items():
            for i, end in enumerate(ENDS):
                base = summary["v8"]["band_bn" if basis == "set" else "cash_set_bn"][i]
                entry["by_end"][end]["v8_plus_change_bn"] = base+entry["by_end"][end]["total_bn"]
    output = dict(case="oct15", accounting_year=2024, population_v8=population, sets=sets, metadata=metadata,
        sign="positive raises annual net cost to other residents; $bn",
        v8_unchanged=dict(set=summary["v8"]["band_bn"], cash=summary["v8"]["cash_set_bn"]),
        item_ids={"16": "native_minor_calibration", "17": "coverage_tenure"},
        interaction="item17 after item16 = joint minus item16; do not stack the standalone item17 on item16",
        measured_vs_model="survey counts and replicate sampling variance measured; reassignment, missing people and prices modeled/conditional",
        limitations=["Survey-weight calibration keeps actual household identities and generation masks. Identity reassignment would require a new joint household assignment model and survivor solve.",
            "Household/spending/receipt pieces retain v8 calibration coefficients and keys; no new nonlinear behavioral or production solve.",
            "All-age tenure contrast transferred conditionally to exact age-sex-generation cell totals; not an identified distribution of omitted residents.",
            "No new benefit take-up, legal-status, income or eligibility assumption; tenure only selects observed case price cells.",
            "Original nonreporting descendants remain at fixed counts and price profile; linked-child origin diagnostic is separate, not an extra adopted correction."])
    write_json(OUT / "items.json", output)
    table = []
    for basis, scenarios in sets.items():
        for scenario, item in scenarios.items():
            for end, row in item["by_end"].items():
                table.append(dict(basis=basis, scenario=scenario, end=end, change_bn=row["total_bn"],
                    observed_bn=row["observed_bn"], coverage_bn=row["coverage_bn"],
                    per_v8_member_usd=row["per_v8_member_usd"], v8_plus_change_bn=row["v8_plus_change_bn"],
                    population_change=item["population_change"]))
    write_csv(OUT / "effects.csv", table)
    sources.update([CASE/"summary.json", CASE/"corrections.json", CASE/"corrections_cash.json",
                    COVER/"derived/coverage_bound_oct15.json", OUT/"native_person_factors.parquet"])
    write_json(OUT / "sources.json", {str(p.relative_to(LANE.parents[2])): digest(p) for p in sorted(sources)})
    elapsed = time.perf_counter()-start
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    require(peak < 2_500_000_000, "process peak RSS exceeds 2.5GB")
    stamp = datetime.now(timezone.utc).isoformat()
    with (LANE / "_cache/run.log").open("a") as stream:
        stream.write(f"{stamp} measure PASS elapsed={elapsed:.3f}s peakRSS={peak} bytes\n")
    print(f"PASS {elapsed:.3f}s peakRSS {peak/1e6:.1f}MB")
    for row in table:
        print(f"{row['basis']} {row['scenario']} {row['end']}: {row['change_bn']:+.9f}bn")


if __name__ == "__main__":
    main()

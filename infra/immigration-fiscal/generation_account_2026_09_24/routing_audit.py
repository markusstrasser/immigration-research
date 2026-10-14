"""One-change attribution audit at the frozen personal ends, set and cash.

Native-First: the lane's existing runner and CSV/JSON artifacts. No new engine.
Runs each independent fix from the same no-fix central, then their combination,
the direct-G3-share parent assignment and the labour-income production arm.
All child exit codes, existing tolerances and every runner gate are enforced.
"""
from __future__ import annotations

import csv
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget

GENS = ["G1", "G2", "G3plus"]


def read(path):
    return json.loads(path.read_text())


def main():
    start = time.perf_counter()
    # P7 baseline remains a pinned historical control. Oct15's no-fix control
    # carries all newly admitted v8 items and cannot equal the older case.
    credit = read(HERE / "derived/credit_routing.json")
    receipt_scenario = read(HERE / "derived/model_G1.json")["receipts"]["reference"]
    lin = read(HERE.parent / "main_case_2026_10_15/derived/corrections.json")["meta"]["lineage"]
    direct_share = read(HERE.parent / "main_case_lineage_2026_10_05/derived/population.json")["arms"]["floor"]["added"] / lin["counts"]["at_g3_rate"]
    measurement = read(HERE / "inputs/minor_parent_measurement_oct15.json")
    runs = {
        "baseline": ["--fixes", "none"], "minors": ["--fixes", "minors"], "credits": ["--fixes", "credits"],
        "tags": ["--fixes", "tags"], "tags_union": ["--fixes", "tags", "--minor-scale", "0"],
        "state_prices": ["--fixes", "state_prices"], "all": [],
        "direct_g3_minors": ["--fixes", "minors", "--minor-scale", str(direct_share)],
        "direct_g3": ["--minor-scale", str(direct_share)],
        "exogamous_half": ["--minor-scale", str(direct_share / 2)],
        "wholly_G2": ["--minor-scale", "1"],
        "no_added_G2": ["--minor-scale", "0"],
        "child_report": ["--minor-scale", str(measurement["source_definition_sensitivities"]["child_report"]["share"])],
        "strict_intersection": ["--minor-scale", str(measurement["source_definition_sensitivities"]["strict_intersection"]["share"])],
        "labour_income": ["--production-rule", "labour_income"],
    }
    summaries = {}
    rows, residuals, controls = [], [], []
    plan = [["--case", case, "--out-dir", str(HERE / "_cache/routing_audit" / case / name), *options]
            for case in ("oct15", "oct15_cash") for name, options in runs.items()]
    plan_path = HERE / "_cache/routing_audit/oct15_plan.json"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, indent=1) + "\n")
    p = subprocess.run(["node", str(HERE / "routing_variants.cjs"), str(plan_path)],
                       capture_output=True, text=True, check=False)
    (plan_path.parent / "oct15_runs.log").write_text(p.stdout + p.stderr)
    if p.returncode:
        print(p.stdout[-4000:] + p.stderr[-4000:], file=sys.stderr)
        raise SystemExit(p.returncode)
    for case in ["oct15", "oct15_cash"]:
        summaries[case] = {}
        for name in runs:
            out = HERE / "_cache/routing_audit" / case / name
            s = read(out / f"generation_summary_{case}.json")
            if s["gates"]["failed"] or not all(g["pass"] for g in s["gates"]["checks"]):
                raise SystemExit(f"[BLOCKED] {case} {name}: runner gates")
            summaries[case][name] = s
            print(f"{case}/{name}: {len(s['gates']['checks'])} gates PASS", flush=True)
        baseline = summaries[case]["baseline"]
        central = read(HERE / "derived" / f"generation_summary_{case}.json")
        gap = max(abs(v - w) for v, w in zip(baseline["union"]["cost_bn"], central["union"]["cost_bn"]))
        if gap >= 1e-9:
            raise SystemExit(f"[BLOCKED] original split positive control {gap}")
        controls.append({"case": case, "no_fix_union_gap": gap, "inherited_control": "P7 G4 source split checked by runner; inputs/baseline.json remains pinned", "pass": True})
        for name, s in summaries[case].items():
            for conv in "ab":
                for gen in GENS:
                    for end, k in [("low", 0), ("high", 1)]:
                        v = s["conventions"][conv][gen]
                        delta = v["cost_bn"][k] - baseline["conventions"][conv][gen]["cost_bn"][k]
                        se = credit["average_net_cost_se"][conv][gen][receipt_scenario] if name == "credits" else ""
                        if name == "state_prices":
                            se = s["state_price_conditional_se"][conv][gen][k]
                        union_delta = 0 if name in ["minors", "direct_g3_minors"] else delta
                        if name == "tags":
                            union_delta = summaries[case]["tags_union"]["conventions"][conv][gen]["cost_bn"][k] - baseline["conventions"][conv][gen]["cost_bn"][k]
                        if name in ["all", "direct_g3", "exogamous_half", "wholly_G2", "no_added_G2", "child_report", "strict_intersection", "labour_income"]:
                            union_delta = ""  # combined readings have cross-fix interactions; independent rows give the scope
                        rows.append({"case": case, "variant": name, "convention": conv, "generation": gen, "end": end,
                                     "fixes": "|".join(s["policy"]["fixes"]), "minor_scale": s["policy"]["minor_scale"],
                                     "production_rule": s["policy"]["production_rule"],
                                     "cost_bn": v["cost_bn"][k], "change_from_central_bn": delta,
                                     "identified_union_routing_change_bn": union_delta,
                                     "lineage_routing_change_bn": delta, "conditional_sdr_se_bn": se,
                                     "per_member_usd": v["per_member_usd"][k], "per_adult_usd": v["per_adult_usd"][k],
                                     "delta_per_lineage_member_usd": delta * 1e9 / s["union"]["population"],
                                     "clears_5bn_redistribution_bar": abs(delta) >= 5,
                                     "headline_change_bn": s["union"]["cost_bn"][k] - baseline["union"]["cost_bn"][k]})
            for end, k in [("low", 0), ("high", 1)]:
                n = s["g2_adults_alone"]["population"]
                value = s["g2_adults_alone"]["cost_bn"][k]
                residuals.append({"case": case, "variant": name, "end": end, "g2_adults_residual_bn": value,
                                  "per_g2_adult_usd": value * 1e9 / n,
                                  "change_from_original_residual_bn": value - baseline["g2_adults_alone"]["cost_bn"][k]})
    footprint = require_within_budget()
    for file, records in [("routing_changes_oct15.csv", rows), ("g2_adults_alone_oct15.csv", residuals)]:
        with (HERE / "derived" / file).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(records)
    synopsis = {"source": "routing_audit.py", "positive_controls": controls, "direct_g3_scale": direct_share,
                "parent_measurement": measurement,
                "headline": {c: s["all"]["union"]["cost_bn"] for c, s in summaries.items()},
                "all": {c: {"conventions": s["all"]["conventions"], "g2_adults_alone": s["all"]["g2_adults_alone"]} for c, s in summaries.items()},
                "ordering_b": {c: {name: [s["conventions"]["b"]["G2"]["per_adult_usd"][k] < s["conventions"]["b"]["G3plus"]["per_adult_usd"][k] for k in [0, 1]]
                                   for name, s in cases.items()} for c, cases in summaries.items()},
                "uncertainty": "credit net SE keeps covariance and fixed imputation seeds; state-price index SE conditional on finance/row4 factors; no invented account-wide or added-parent SE"}
    (HERE / "derived/routing_audit_oct15.json").write_text(json.dumps(synopsis, indent=1) + "\n")
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    print(f"routing audit: seconds={time.perf_counter()-start:.3f} physical_peak_bytes={footprint} diagnostic_peak_child_bytes={peak}")
    # Child RSS is informational. Producers enforce physical footprint inside
    # each Python process; post-exit RSS is not a physical-footprint gate.


if __name__ == "__main__":
    main()

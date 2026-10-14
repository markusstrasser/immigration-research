"""One-change attribution audit at the frozen personal ends, set and cash.

Native-First: the lane's existing runner and CSV/JSON artifacts. No new engine.
Runs each independent fix from the same no-fix central, then their combination,
the floor-scaled parent assignment and the labour-income production arm.
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
GENS = ["G1", "G2", "G3plus"]


def read(path):
    return json.loads(path.read_text())


def main():
    start = time.perf_counter()
    original = read(HERE / "inputs/baseline.json")
    credit = read(HERE / "derived/credit_routing.json")
    receipt_scenario = read(HERE / "derived/model_G1.json")["receipts"]["reference"]
    lin = read(HERE.parent / "main_case_2026_10_14/derived/corrections.json")["meta"]["lineage"]
    floor = read(HERE.parent / "main_case_lineage_2026_10_05/derived/population.json")["arms"]["floor"]["added"] / lin["counts"]["at_g3_rate"]
    runs = {
        "baseline": ["--fixes", "none"], "minors": ["--fixes", "minors"], "credits": ["--fixes", "credits"],
        "tags": ["--fixes", "tags"], "tags_union": ["--fixes", "tags", "--minor-scale", "0"],
        "state_prices": ["--fixes", "state_prices"], "all": [],
        "floor_minors": ["--fixes", "minors", "--minor-scale", str(floor)],
        "floor": ["--minor-scale", str(floor)], "labour_income": ["--production-rule", "labour_income"],
    }
    summaries = {}
    rows, residuals, controls = [], [], []
    for case in ["oct14", "oct14_cash"]:
        summaries[case] = {}
        for name, options in runs.items():
            out = HERE / "_cache/routing_audit" / case / name
            p = subprocess.run(["node", str(HERE / "run_generations_v7.cjs"), "--case", case,
                                "--out-dir", str(out), *options], capture_output=True, text=True, check=False)
            if p.returncode:
                print(p.stdout[-4000:] + p.stderr[-4000:], file=sys.stderr)
                raise SystemExit(p.returncode)
            s = read(out / f"generation_summary_{case}.json")
            if s["gates"]["failed"] or not all(g["pass"] for g in s["gates"]["checks"]):
                raise SystemExit(f"[BLOCKED] {case} {name}: runner gates")
            summaries[case][name] = s
            print(f"{case}/{name}: {len(s['gates']['checks'])} gates PASS", flush=True)
        baseline = summaries[case]["baseline"]
        old = original["cases"][case]
        gap = max(abs(v - w) for c in "ab" for g in GENS for k in ["cost_bn", "per_member_usd", "per_adult_usd"]
                  for v, w in zip(baseline["conventions"][c][g][k], old["conventions"][c][g][k]))
        if gap >= 1e-9:
            raise SystemExit(f"[BLOCKED] original split positive control {gap}")
        controls.append({"case": case, "original_split_gap": gap, "pass": True})
        for name, s in summaries[case].items():
            for conv in "ab":
                for gen in GENS:
                    for end, k in [("low", 0), ("high", 1)]:
                        v = s["conventions"][conv][gen]
                        delta = v["cost_bn"][k] - baseline["conventions"][conv][gen]["cost_bn"][k]
                        se = credit["average_net_cost_se"][conv][gen][receipt_scenario] if name == "credits" else ""
                        if name == "state_prices":
                            se = s["state_price_conditional_se"][conv][gen][k]
                        union_delta = 0 if name in ["minors", "floor_minors"] else delta
                        if name == "tags":
                            union_delta = summaries[case]["tags_union"]["conventions"][conv][gen]["cost_bn"][k] - baseline["conventions"][conv][gen]["cost_bn"][k]
                        if name in ["all", "floor", "labour_income"]:
                            union_delta = ""  # combined readings have cross-fix interactions; independent rows give the scope
                        rows.append({"case": case, "variant": name, "convention": conv, "generation": gen, "end": end,
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
    for file, records in [("routing_changes_oct14.csv", rows), ("g2_adults_alone_oct14.csv", residuals)]:
        with (HERE / "derived" / file).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(records)
    synopsis = {"source": "routing_audit.py", "positive_controls": controls, "minor_floor_scale": floor,
                "headline": {c: s["all"]["union"]["cost_bn"] for c, s in summaries.items()},
                "all": {c: {"conventions": s["all"]["conventions"], "g2_adults_alone": s["all"]["g2_adults_alone"]} for c, s in summaries.items()},
                "ordering_b": {c: {name: [s["conventions"]["b"]["G2"]["per_adult_usd"][k] < s["conventions"]["b"]["G3plus"]["per_adult_usd"][k] for k in [0, 1]]
                                   for name, s in cases.items()} for c, cases in summaries.items()},
                "uncertainty": "credit net SE keeps covariance and fixed imputation seeds; state-price index SE conditional on finance/row4 factors; no invented account-wide or added-parent SE"}
    (HERE / "derived/routing_audit_oct14.json").write_text(json.dumps(synopsis, indent=1) + "\n")
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    print(f"routing audit: seconds={time.perf_counter()-start:.3f} peak_child_bytes={peak}")
    if peak > 2_500_000_000:
        raise SystemExit("[BLOCKED] routing-audit child exceeded 2.5 GB")


if __name__ == "__main__":
    main()

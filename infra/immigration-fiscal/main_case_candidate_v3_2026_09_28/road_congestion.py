"""The congestion item beside the account at every lane cut the v3 lane prices (BRIEF.md, 0a83245).

Congestion is priced as the September 27 case and candidate v2 price it (service_response_long_run_2026_09_27/congestion.py):
lanes shrink by c = kappa * h * k, with h the highway response the lanes follow, k the group's key share of the
economic-affairs line (the two fill-in methods averaged, as the bridge averages them) and kappa 1, or 0 where lanes stay
(the B1). The cuts come from the v3 package through node (package.cjs congestionCuts(): the road arm at the fixed end
specifications on the candidate, v2 and the September 27 case, and every outer-range variant's band ends on the candidate
with each switch off and on, v2 and the September 27 case), so the Python step and main_case.cjs read one
definition. The congestion functions are the response lane's own, imported read-only (its main() is not run; nothing of
it is written; no bytecode is written).

Gates reproduce the bridge's B1 and its four uniform rows (central and factorial range) before anything new is priced,
and every cut this lane shares with candidate v2's committed road_congestion.json must price as v2 priced it. Factorial
ranges are priced for the road arm's cuts only. Writes derived/road_congestion.json; exit 1 and nothing written on a
failed gate. Run from the repository root, after transit_key.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_candidate_v3_2026_09_28/road_congestion.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
BRIDGE_DIR = FISCAL / "service_response_long_run_2026_09_27"
V2_CONGESTION = "main_case_candidate_v2_2026_09_28/derived/road_congestion.json"
SOURCES = [
    "service_response_long_run_2026_09_27/congestion.py",
    "congestion_2026_09_23/arms.py",
    "service_response_long_run_2026_09_27/derived/congestion_bridge.csv",
    "service_response_long_run_2026_09_27/derived/net_change.json",
    "main_case_candidate_v3_2026_09_28/package.cjs",
    "main_case_candidate_v3_2026_09_28/derived/transit_key.json",
    "main_case_candidate_v2_2026_09_28/package.cjs",
    "main_case_candidate_v2_2026_09_28/derived/road_stock.json",
    V2_CONGESTION,
    "main_case_candidate_2026_09_28/package.cjs",
    "main_case_long_run_2026_09_27/package.cjs",
    "receipt_side_long_run_2026_09_28/items.cjs",
    "receipt_side_long_run_2026_09_28/derived/housing.json",
    "payroll_compliance_2026_09_28/derived/items.json",
    "backcast_pandemic_measured_2026_09_28/derived/ratio_vs_2024.csv",
    "uncompensated_care_2026_09_23/derived/summary.json",
]
GATES: list[dict] = []
NODE = r"""
const C = require(process.argv[1]);
process.stdout.write(JSON.stringify({ cuts: C.congestionCuts(), pension: { commit: C.PENSION_COMMIT, sha256: C.pension().sha256 } }));
"""


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def sha256(rel):
    return hashlib.sha256((FISCAL / rel).read_bytes()).hexdigest()


def main():
    before = {rel: sha256(rel) for rel in SOURCES}
    res = subprocess.run(["node", "-e", NODE, str(HERE / "package.cjs")], capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise SystemExit(f"[BLOCKED] node could not read package.cjs: {res.stderr.strip()[-600:]}")
    got = json.loads(res.stdout)
    cuts = got["cuts"]
    spec = importlib.util.spec_from_file_location("congestion_bridge", BRIDGE_DIR / "congestion.py")
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    A = M.A
    control, nhts, tau, vots, exposures, pop_share = M.setup()
    e = exposures["2017 southwest"]
    scope = e["in_scope"].to_numpy()
    r_h = nhts["2017 southwest"]["r_hours"]
    eps_c = A.POP_FIXED_LANES["central"]
    factorial = {"elasticity": A.POP_FIXED_LANES, "share": {"population": "s", "traffic": "phi"}, "vot": vots, "tau": tau,
                 "nhts": nhts, "hours": {"2022": 2022, "2017": 2017}}

    def central(cut):
        return M.arm(e, scope, e.s, eps_c, A.LANES_COEF_T10, cut, tau["central"], vots["central"], 2022, r_h)

    def factorial_range(cut):
        # congestion.py main()'s b_grid with a uniform cut and its three lane coefficients.
        out = []
        for lab, val in A.grid(dict(factorial, lanes=M.LANES)):
            ex = exposures[lab["nhts"]]
            sc = ex["in_scope"].to_numpy()
            share = ex.s if val["share"] == "s" else ex.phi_commute_route
            out.append(M.arm(ex, sc, share, val["elasticity"], val["lanes"], cut, val["tau"], val["vot"], val["hours"],
                             val["nhts"]["r_hours"]))
        return [min(out), max(out)]

    net = json.loads((BRIDGE_DIR / "derived" / "net_change.json").read_text())
    with open(BRIDGE_DIR / "derived" / "congestion_bridge.csv", newline="") as fh:
        bridge = [r for r in csv.DictReader(fh) if r["geography"] == "uniform (account key)"]
    rel = lambda a, b: abs(a - b) <= 1e-9 * max(1.0, abs(b))  # the bridge csv carries 10 significant digits

    rows = []
    for x in cuts:
        c = x["cut"]
        row = {"lane_cut": c, "congestion_central_bn": central(c)}
        if x["factorial"]:
            lo, hi = factorial_range(c)
            row.update({"factorial_min_bn": lo, "factorial_max_bn": hi})
        rows.append(row)
    by_cut = {r["lane_cut"]: r for r in rows}

    print("[gates: the congestion bridge reproduced]")
    gate("UMR positive control passes", control["passed"])
    b1 = by_cut.get(0.0)
    gate("the lanes-fixed cut (0) is priced and is net_change.json's B1 (1e-9)",
         b1 is not None and abs(b1["congestion_central_bn"] - net["b1_lanes_fixed_bn"]) < 1e-9, f"{b1['congestion_central_bn']:.6f}" if b1 else "missing")
    for r in bridge:
        want = float(r["lane_cut"])
        hit = [x for x in rows if "factorial_min_bn" in x and rel(x["lane_cut"], want)]
        ok = len(hit) == 1 and rel(hit[0]["congestion_central_bn"], float(r["congestion_central_bn"])) \
            and rel(hit[0]["factorial_min_bn"], float(r["factorial_min_bn"])) and rel(hit[0]["factorial_max_bn"], float(r["factorial_max_bn"]))
        gate(f"bridge {r['band_end']} / {r['variant']}: the lane's cut is priced and reproduces central and factorial range", ok,
             f"cut {want} -> {hit[0]['congestion_central_bn']:.6f} ({hit[0]['factorial_min_bn']:.4f}–{hit[0]['factorial_max_bn']:.4f})" if hit else "cut missing")
    v2 = json.loads((FISCAL / V2_CONGESTION).read_text())
    v2_by_cut = {r["lane_cut"]: r for r in v2["rows"]}
    shared = [r for r in rows if r["lane_cut"] in v2_by_cut]
    worst = max((abs(r["congestion_central_bn"] - v2_by_cut[r["lane_cut"]]["congestion_central_bn"]) for r in shared), default=0.0)
    worst_f = max((abs(r[k] - v2_by_cut[r["lane_cut"]][k]) for r in shared if "factorial_min_bn" in r and "factorial_min_bn" in v2_by_cut[r["lane_cut"]]
                   for k in ("factorial_min_bn", "factorial_max_bn")), default=0.0)
    gate("every cut shared with candidate v2's road_congestion.json prices as v2 priced it (central and factorial, 1e-12)",
         len(shared) > 0 and worst < 1e-12 and worst_f < 1e-12,
         f"{len(shared)} of {len(rows)} cuts shared; max |diff| {worst:.1e} / {worst_f:.1e}")
    gate("congestion falls as the lane cut grows (monotone)",
         all(a["congestion_central_bn"] >= b["congestion_central_bn"] - 1e-12 for a, b in zip(rows, rows[1:])), f"{len(rows)} cuts")
    gate("the sources did not change during the run", before == {rel_: sha256(rel_) for rel_ in SOURCES})

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "road_congestion.json").write_text(json.dumps({
        "meta": {"lane": "main_case_candidate_v3_2026_09_28", "case": "sept28_candidate_v3",
                 "definition": ("congestion beside the account (service_response_long_run_2026_09_27/congestion.py arm(), central inputs; "
                                "factorial range over its grid with three lane coefficients, road-arm cuts only) with lanes cut uniformly "
                                "by the lane cut package.cjs congestionCuts() lists"),
                 "sources": before, "pension_summary": got["pension"],
                 "cuts_shared_with_v2": len(shared), "cuts_new": len(rows) - len(shared)},
        "b1_lanes_fixed_bn": b1["congestion_central_bn"], "rows": rows, "gates": GATES}, indent=1) + "\n")
    print(f"\nall {len(GATES)} gates passed; {len(rows)} cuts priced ({len(shared)} shared with v2); wrote derived/road_congestion.json")


if __name__ == "__main__":
    main()

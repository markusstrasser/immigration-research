"""Item 3 of BRIEF.md, the road arm: the congestion item at every long-run road response.

The September 27 case prices congestion beside the account at the adopted highway response only
(service_response_long_run_2026_09_27/congestion.py, derived/congestion_bridge.csv): lanes shrink by
c = kappa * h * k, with h the highway response at the band end (S&L and federal highways, weighted by
national amount), k the group's key share of the economic-affairs line and kappa 1 (the network follows
spending) or 0 (lanes fixed, the B1 $19.16bn). Its range component "long_run_response" varies h without
the congestion item. This script prices congestion at every long-run variant's h, so main_case.cjs can
report each variant's account move and congestion move together.

The long-run variants, the highway subfunctions and the key come from the candidate package (package.cjs,
through node), one definition; the congestion functions are the response lane's own (imported read-only;
its main() is not run and nothing of it is written). Gates reproduce the bridge's B1, its adopted rows
(central and factorial range, both band ends, both kappas) and its h and k before anything new is priced.
Writes derived/road_congestion.json; exit 1 and nothing written on a failed gate.
Run from the repository root (production_row4.py first; package.cjs needs its output):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_candidate_2026_09_28/road_congestion.py
"""
from __future__ import annotations

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
SOURCES = [
    "service_response_long_run_2026_09_27/congestion.py",
    "congestion_2026_09_23/arms.py",
    "service_response_long_run_2026_09_27/derived/congestion_bridge.csv",
    "service_response_long_run_2026_09_27/derived/net_change.json",
    "service_response_long_run_2026_09_27/derived/responses.json",
    "main_case_candidate_2026_09_28/package.cjs",
    "main_case_long_run_2026_09_27/package.cjs",
]
READINGS = ("low", "high")
# The fixed end specifications of the brief: 48 at the low end, 11 at the high end.
END_SPEC = {"low": 48, "high": 11}
GATES: list[dict] = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def sha256(rel):
    return hashlib.sha256((FISCAL / rel).read_bytes()).hexdigest()


# The package's highway responses by variant and reading, and the road key at the fixed end specifications
# (each method's key averaged).
NODE = r"""
const C = require(process.argv[1]);
const ends = JSON.parse(process.argv[2]);
const sfs = C.LR.lines[C.ROAD_LINE].subfunctions.filter((s) => C.ROAD_SUBFUNCTIONS.includes(s.id));
const w = sfs.reduce((a, s) => a + s.national_bn, 0);
const out = { road_subfunctions: sfs.map((s) => ({ id: s.id, national_bn: s.national_bn })), highway_response: {}, key: {} };
for (const v of Object.keys(C.LONG_RUN_VARIANTS)) {
  out.highway_response[v] = {};
  for (const rd of ["low", "high"]) {
    const r = C.subfunctionResponses(v, rd);
    out.highway_response[v][rd] = sfs.reduce((a, s) => a + s.national_bn * r[s.id], 0) / w;
  }
}
const oo = C.withCentral({});
const specs = C.specsFor(oo);
for (const rd of ["low", "high"]) {
  const ks = C.METHODS.map((meth) => {
    const l = C.evaluateFull(C.modelFor("central", meth, oo), specs[ends[rd]]).evaluation.spending.find((x) => x.id === C.ROAD_LINE);
    return l.amount_bn / l.national_bn;
  });
  out.key[rd] = ks.reduce((a, b) => a + b, 0) / ks.length;
}
process.stdout.write(JSON.stringify(out));
"""


def package_inputs():
    res = subprocess.run(["node", "-e", NODE, str(HERE / "package.cjs"), json.dumps(END_SPEC)],
                         capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise SystemExit(f"[BLOCKED] node could not read package.cjs: {res.stderr.strip()[-400:]}")
    return json.loads(res.stdout)


def main():
    before = {rel: sha256(rel) for rel in SOURCES}
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

    inp = package_inputs()
    net = json.loads((BRIDGE_DIR / "derived" / "net_change.json").read_text())
    with open(BRIDGE_DIR / "derived" / "congestion_bridge.csv", newline="") as fh:
        bridge = [r for r in csv.DictReader(fh) if r["geography"] == "uniform (account key)"]

    print("[gates: the congestion bridge reproduced]")
    gate("UMR positive control passes", control["passed"])
    b1 = central(0.0)
    gate("B1 (lanes fixed) is net_change.json's b1_lanes_fixed_bn (1e-9)", abs(b1 - net["b1_lanes_fixed_bn"]) < 1e-9, f"{b1:.6f}")
    cache: dict[float, dict] = {}

    def priced(cut):
        if cut not in cache:
            cache[cut] = {"congestion_central_bn": central(cut), "factorial_bn": factorial_range(cut)}
        return cache[cut]

    rel = lambda a, b: abs(a - b) <= 1e-9 * max(1.0, abs(b))  # the bridge csv carries 10 significant digits
    kappa = {"network follows spending": 1.0, "network fixed (bound)": 0.0}
    for r in bridge:
        rd, kp = r["band_end"], kappa[r["variant"]]
        h, k = inp["highway_response"]["adopted"][rd], inp["key"][rd]
        x = priced(kp * h * k)
        gate(f"bridge {rd} / {r['variant']}: h, k, the lane cut, the central and the factorial range reproduce",
             rel(h, float(r["highway_response"])) and rel(k, float(r["key_share"])) and rel(kp * h * k, float(r["lane_cut"]))
             and rel(x["congestion_central_bn"], float(r["congestion_central_bn"]))
             and rel(x["factorial_bn"][0], float(r["factorial_min_bn"])) and rel(x["factorial_bn"][1], float(r["factorial_max_bn"])),
             f"h {h:.10f} k {k:.10f} congestion {x['congestion_central_bn']:.6f} ({x['factorial_bn'][0]:.4f}–{x['factorial_bn'][1]:.4f})")
    gate("every bridge row is reproduced (2 band ends x 2 kappas)", len(bridge) == 4)
    gate("the package's highway responses are finite and non-negative, and its keys in (0, 1)",
         all(0 <= v[rd] < 2 for v in inp["highway_response"].values() for rd in READINGS)
         and all(0 < inp["key"][rd] < 1 for rd in READINGS), json.dumps(inp["key"]))

    print("\n[the long-run variants, the network following spending]")
    rows = []
    for v, hs in inp["highway_response"].items():
        for rd in READINGS:
            cut = hs[rd] * inp["key"][rd]
            x = priced(cut)
            rows.append({"variant": v, "reading": rd, "end_specification": END_SPEC[rd], "kappa": 1.0, "highway_response": hs[rd],
                         "key_share": inp["key"][rd], "lane_cut": cut, "congestion_central_bn": x["congestion_central_bn"],
                         "factorial_min_bn": x["factorial_bn"][0], "factorial_max_bn": x["factorial_bn"][1],
                         "change_vs_b1_central_bn": x["congestion_central_bn"] - b1})
            print(f"  {v:26s} {rd:4s} h {hs[rd]:.6f} cut {cut:.6f} congestion {x['congestion_central_bn']:.4f} "
                  f"({x['factorial_bn'][0]:.2f}–{x['factorial_bn'][1]:.2f})")
    fixed = priced(0.0)
    gate("congestion falls as the lane cut grows (monotone in the cut)",
         all(a["congestion_central_bn"] >= b["congestion_central_bn"] - 1e-12
             for a in rows for b in rows if a["lane_cut"] < b["lane_cut"]))
    gate("the sources did not change during the run", before == {rel_: sha256(rel_) for rel_ in SOURCES})

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "road_congestion.json").write_text(json.dumps({
        "meta": {"lane": "main_case_candidate_2026_09_28", "case": "sept28_candidate",
                 "definition": ("congestion beside the account (service_response_long_run_2026_09_27/congestion.py arm(), "
                                "central inputs; factorial range over its grid with three lane coefficients) with lanes cut "
                                "uniformly by kappa * h * k: h the variant's highway response at the band end (S&L and federal "
                                "highways weighted by national amount), k the group's key share of economic_affairs_services "
                                "at the fixed end specification (48 low, 11 high; the two fill-in methods averaged)"),
                 "sources": before},
        "b1_lanes_fixed_bn": b1, "b1_factorial_bn": fixed["factorial_bn"],
        "road_subfunctions": inp["road_subfunctions"], "key": inp["key"], "highway_response": inp["highway_response"],
        "rows": rows, "gates": GATES}, indent=1) + "\n")
    print(f"\nall {len(GATES)} gates passed; wrote derived/road_congestion.json")


if __name__ == "__main__":
    main()

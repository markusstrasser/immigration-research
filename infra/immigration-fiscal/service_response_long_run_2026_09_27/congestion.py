"""Step 3 of this lane (BRIEF.md): the congestion item when road capacity follows the highway response.

congestion_2026_09_23 prices other residents' extra delay from the group's traffic beside the
account: $19.2bn (B1) with lanes fixed, because the main case holds economic affairs at zero response.
If highway spending responds, the road network without the group is smaller, and the account must not
charge both the spending the group's roads cost and the full fixed-lane congestion.

B1 is Couture, Duranton and Turner's regression of log speed on log population and log lanes across
100 MSAs (table 10 column 6): population -0.12 (SE 0.035), lanes 0.066 (SE 0.038). With lanes fixed the
time cost moves by ln C0 = eps ln(1 - s_i); with lanes shrinking by c it moves by
  ln C0 = eps ln(1 - s_i) - lam ln(1 - c).
The lane's own keyed variant is this with c = the account's resources key share 0.0810 ($12.0bn, the
proportional reference). Here c = kappa * h * k: h is the highway spending response at the band end
(S&L and federal highways, amount-weighted, from derived/responses.json), k the group's key share of
the economic-affairs line at that end's specification (derived/candidate_band.json), and kappa the
elasticity of lane capacity with respect to highway spending (1 central: the network is what the
spending maintains and depreciates; 0 bounds it: the saving comes from maintenance on an unchanged
network). The cut is spread uniformly over urban areas as in the lane's keyed variant; a variant cuts
lanes where the group lives.

Functions and inputs are the congestion lane's own (imported read-only from its arms.py; its _cache/
and derived/ files are read, never written). Gates reproduce its B1 central, its B1 factorial range and
its keyed proportional variant before anything new is computed. Writes derived/congestion_bridge.csv,
derived/net_change.json, derived/gates_congestion.json and derived/gates.json (every step; run build.py,
engine.cjs and land_check.py first).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/congestion.py
"""
from __future__ import annotations

import csv
import importlib.util
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
spec = importlib.util.spec_from_file_location("arms", FISCAL / "congestion_2026_09_23" / "arms.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

LANES_SE = 0.038  # CDT working paper table 10 column 6, log lane (total) 0.066 (0.038); lane _cache cdt_speed_2016_hal.firecrawl.md
LANES = {"low": A.LANES_COEF_T10 - LANES_SE, "central": A.LANES_COEF_T10, "high": A.LANES_COEF_T10 + LANES_SE}
KAPPA = {"network follows spending": 1.0, "network fixed (bound)": 0.0}
GATES: list[dict] = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def setup():
    """The congestion lane's main() inputs, in its order, without its writes."""
    u, summary = A.load_umr()
    control = A.positive_control(u, summary)
    checks_pums = json.loads((A.DERIVED / "pums_commute_checks.json").read_text())
    scale = A.TARGET / checks_pums["group_persons_acs"]
    wide = A.load_cells()
    ua, xw = A.ua_areas(wide)
    u = A.match_umr(u, xw)
    rat = pd.read_csv(A.DERIVED / "nhts_ratios.csv").set_index(["survey", "cut"])
    hours = pd.read_csv(A.DERIVED / "nhts_hours_by_urbansize.csv")
    vot, _ = A.vot_2024()

    def nhts_set(r):
        return dict(rho=r.rho_all_over_commute_H_vs_N, r_all=r.r_all_driver_vmt_per_person_H_vs_N,
                    occ=r.occupancy_ratio_H_vs_N, pi=r.peak_share_H / r.peak_share_N,
                    r_hours=r.r_pov_hours_per_person_H_vs_N)
    nhts = {"2017 southwest": nhts_set(rat.loc[(2017, "southwest")]),
            "2022 national": nhts_set(rat.loc[(2022, "national")]),
            "2017 national": nhts_set(rat.loc[(2017, "national")])}
    nat = pd.read_csv(A.DERIVED / "pums_commute_national.csv").set_index(["group", "item"])["estimate"]
    income_share = float(scale * nat[("group_share", "personal_income")])
    pop_share = A.TARGET / A.RESIDENTS
    tau = {"low": income_share, "central": (income_share + pop_share) / 2, "high": pop_share}
    vots = {lv: vot.loc[lv] for lv in ("low", "central", "high")}
    exposures = {k: A.build_exposure(u, ua, hours, inp, scale) for k, inp in nhts.items()}
    return control, nhts, tau, vots, exposures, pop_share


def arm(ex, scope, share, eps, lam, cut, tau, vot, year, r_hours):
    """B-arm time cost with lanes shrinking by `cut` (a scalar or a per-area series); $bn over the lane's scope."""
    log_c0 = eps * np.log1p(-share) - lam * np.log1p(-cut)
    res = A.time_cost_arm(ex, log_c0, 0.0, tau, ex.phi_commute_route, vot, year, r_hours)
    return A.summarise(res, ex, scope)["total_bn"]


def main():
    control, nhts, tau, vots, exposures, pop_share = setup()
    e = exposures["2017 southwest"]
    scope = e["in_scope"].to_numpy()
    r_h = nhts["2017 southwest"]["r_hours"]
    eps_c = A.POP_FIXED_LANES["central"]
    summ = pd.read_csv(A.DERIVED / "arms_summary.csv").set_index("approach")
    grid = pd.read_csv(A.DERIVED / "arms_grid.csv")

    print("[gates: the congestion lane reproduced]")
    gate("UMR positive control passes", control["passed"])
    b1 = arm(e, scope, e.s, eps_c, 0.0, 0.0, tau["central"], vots["central"], 2022, r_h)
    b1_pub = summ.loc["B1 population elasticity, lanes fixed"]
    gate("B1 central (lanes fixed) reproduces arms_summary.csv", abs(b1 - b1_pub.central_bn) < 1e-9, f"{b1:.6f}")
    factorial = {"elasticity": A.POP_FIXED_LANES, "share": {"population": "s", "traffic": "phi"}, "vot": vots, "tau": tau,
                 "nhts": nhts, "hours": {"2022": 2022, "2017": 2017}}

    def b_grid(cut_of, lanes):
        out = []
        for lab, val in A.grid(dict(factorial, lanes=lanes)):
            ex = exposures[lab["nhts"]]
            sc = ex["in_scope"].to_numpy()
            share = ex.s if val["share"] == "s" else ex.phi_commute_route
            out.append(arm(ex, sc, share, val["elasticity"], val["lanes"], cut_of(ex), val["tau"], val["vot"], val["hours"],
                           val["nhts"]["r_hours"]))
        return out
    fixed = b_grid(lambda ex: 0.0, {"central": A.LANES_COEF_T10})
    gate("B1 factorial range reproduces arms_summary.csv", abs(min(fixed) - b1_pub.factorial_min_bn) < 1e-9
         and abs(max(fixed) - b1_pub.factorial_max_bn) < 1e-9, f"{min(fixed):.4f}–{max(fixed):.4f}")
    model = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    line = next(x for x in model["spending"]["lines"] if x["id"] == "economic_affairs_services")
    k0 = line["keys"][line["preferred_key"]]["personal"]["share"]
    keyed = arm(e, scope, e.s, eps_c, A.LANES_COEF_T10, k0, tau["central"], vots["central"], 2022, r_h)
    row = grid[grid.note.fillna("").str.contains("lanes shrink by the account's resources key")]
    gate("keyed proportional variant (lanes shrink by the 0.0810 key) reproduces arms_grid.csv",
         len(row) == 1 and abs(keyed - float(row.total_bn.iloc[0])) < 1e-9, f"{keyed:.6f}")

    # ------------------------------------------------------------------------------------------
    print("\n[bridge]")
    resp = json.loads((DERIVED / "responses.json").read_text())
    cand = json.loads((DERIVED / "candidate_band.json").read_text())
    ea = resp["lines"]["economic_affairs_services"]
    hw = [s for s in ea["subfunctions"] if s["subfunction"] == "Highways"]
    gate("highway subfunctions are S&L and federal", sorted(s["level"] for s in hw) == ["federal", "state_local"])
    h = {end: sum(s["national_bn"] * s["response"][end] for s in hw) / sum(s["national_bn"] for s in hw) for end in ("low", "high")}
    k = {end: cand["group_amounts_at_end_specifications_bn"][end]["economic_affairs_services"] / ea["national_bn"] for end in ("low", "high")}
    move = {"low": cand["move_at_fixed_specifications_bn"]["low_end_spec_low_responses"],
            "high": cand["move_at_fixed_specifications_bn"]["high_end_spec_high_responses"]}
    rows, net = [], {}
    for end in ("low", "high"):
        for kname, kappa in KAPPA.items():
            cut = kappa * h[end] * k[end]
            central = arm(e, scope, e.s, eps_c, A.LANES_COEF_T10, cut, tau["central"], vots["central"], 2022, r_h)
            g = b_grid(lambda ex, c=cut: c, LANES)
            rows.append({"band_end": end, "variant": kname, "geography": "uniform (account key)", "kappa": kappa,
                         "highway_response": h[end], "key_share": k[end], "lane_cut": cut, "congestion_central_bn": central,
                         "factorial_min_bn": min(g), "factorial_max_bn": max(g), "change_vs_b1_central_bn": central - b1})
        # Lanes cut where the group lives: the same national dollar cut, spread by the group's local
        # population share (lanes in proportion, as the lane's B3; scaled to h * k nationally).
        local = lambda ex, end=end: h[end] * k[end] / pop_share * ex.s
        central = arm(e, scope, e.s, eps_c, A.LANES_COEF_T10, local(e), tau["central"], vots["central"], 2022, r_h)
        g = b_grid(local, LANES)
        rows.append({"band_end": end, "variant": "network follows spending", "geography": "local (group's population share)",
                     "kappa": 1.0, "highway_response": h[end], "key_share": k[end], "lane_cut": h[end] * k[end],
                     "congestion_central_bn": central, "factorial_min_bn": min(g), "factorial_max_bn": max(g),
                     "change_vs_b1_central_bn": central - b1})
        main = next(r for r in rows if r["band_end"] == end and r["variant"] == "network follows spending"
                    and r["geography"].startswith("uniform"))
        net[end] = {"account_move_bn": move[end], "congestion_change_bn": main["change_vs_b1_central_bn"],
                    "net_change_bn": move[end] + main["change_vs_b1_central_bn"],
                    "congestion_bn": main["congestion_central_bn"], "congestion_range_bn": [main["factorial_min_bn"], main["factorial_max_bn"]],
                    "lane_cut": main["lane_cut"], "highway_response": h[end], "key_share": k[end]}
    gate("congestion with shrinking lanes is at most the fixed-lane B1", all(r["congestion_central_bn"] <= b1 + 1e-9 for r in rows))

    # ------------------------------------------------------------------------------------------
    if not all(g_["passed"] for g_ in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g_['passed'] for g_ in GATES)} gate(s) failed; nothing written")
    fields = ["band_end", "variant", "geography", "kappa", "highway_response", "key_share", "lane_cut",
              "congestion_central_bn", "factorial_min_bn", "factorial_max_bn", "change_vs_b1_central_bn"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({f: (f"{r[f]:.10g}" if isinstance(r[f], float) else r[f]) for f in fields})
    (DERIVED / "congestion_bridge.csv").write_text(buf.getvalue())
    (DERIVED / "net_change.json").write_text(json.dumps({
        "b1_lanes_fixed_bn": b1, "b1_factorial_bn": [min(fixed), max(fixed)], "keyed_proportional_bn": keyed,
        "lanes_coefficient": LANES, "note": ("net_change = the account's move at the band end's fixed specification + the change in "
                                             "the congestion item beside it (central inputs, network follows spending, uniform cut)"),
        "by_band_end": net}, indent=1) + "\n")
    (DERIVED / "gates_congestion.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    all_gates = {step: json.loads((DERIVED / f"gates_{step}.json").read_text())["gates"] for step in ("build", "engine", "land", "congestion")}
    (DERIVED / "gates.json").write_text(json.dumps({"all_passed": all(g_["passed"] for gs in all_gates.values() for g_ in gs),
                                                    "counts": {s: len(g_) for s, g_ in all_gates.items()}, "gates": all_gates}, indent=1) + "\n")
    print(f"\n  B1 lanes fixed {b1:.4f}; keyed proportional {keyed:.4f}")
    for r in rows:
        print(f"  {r['band_end']:4s} {r['variant']:26s} {r['geography']:32s} cut {r['lane_cut']:.5f}  "
              f"{r['congestion_central_bn']:.4f} ({r['factorial_min_bn']:.2f}–{r['factorial_max_bn']:.2f})  change {r['change_vs_b1_central_bn']:+.4f}")
    for end, v in net.items():
        print(f"  net {end}: account {v['account_move_bn']:+.4f} + congestion {v['congestion_change_bn']:+.4f} = {v['net_change_bn']:+.4f}")
    print(f"all {len(GATES)} gates passed")


if __name__ == "__main__":
    main()

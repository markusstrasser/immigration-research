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
import ctypes
import ctypes.util
import hashlib
import os
import subprocess
import sys
import tempfile
import time
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
sys.path.insert(0, str(FISCAL / "scripts"))
import memory_budget as MB
ARM_WEIGHTS = {}


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}: {detail}; no new outputs written")


def live_roads():
    """Use the adopted native road key/responses; no physicalization of fixed post amounts."""
    source = r'''
const P=require('./infra/immigration-fiscal/main_case_2026_10_15/package.cjs');
const S=P.readJson('main_case_2026_10_15/derived/summary.json'), Q=P.correctionsPayload();
if(S.v8.status!=='adopted'||Q.meta.coverage.stub||JSON.stringify(Q)!==JSON.stringify(P.readJson('main_case_2026_10_15/derived/corrections.json')))throw Error('[BLOCKED] roads require matching adopted payload');
const rows={};for(const [j,end]of ['low','high'].entries()){const i=S.v8.end_specifications.set[0][j],sp=P.MAIN_SPECS[i],x=P.evaluateFull(P.payloadModel(),sp);if(Math.abs(x.cost_bn-S.main_case[j])>1e-9)throw Error('[BLOCKED] road case does not close');rows[end]={specification:i,allocation:sp.allocation,roads:x.capital.components.filter(c=>['hwy_sl','hwy_fed'].includes(c.id))};}
console.log(JSON.stringify({case:'oct15',population:Q.meta.population_v8,ends:rows}));
'''
    proc = subprocess.Popen(["node", "-e", source], cwd=HERE.parents[2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    peak = 0
    if sys.platform == "darwin":
        lib = ctypes.CDLL(ctypes.util.find_library("proc"), use_errno=True)
        while proc.poll() is None:
            info = MB._RUsageInfoV4()
            rc = lib.proc_pid_rusage(proc.pid, MB._RUSAGE_INFO_V4, ctypes.byref(info))
            if rc == 0:
                peak = max(peak, info.ri_lifetime_max_phys_footprint)
                if peak > MB.LIMIT_BYTES:
                    proc.terminate()
                    proc.wait()
                    raise SystemExit("[BLOCKED] road probe exceeds physical-footprint budget")
            elif ctypes.get_errno() != 3:
                proc.terminate()
                proc.wait()
                raise OSError(ctypes.get_errno(), "road-probe footprint measurement failed")
            time.sleep(0.01)
    stdout, stderr = proc.communicate()
    if proc.returncode or not stdout.strip():
        raise RuntimeError(f"[BLOCKED] adopted road probe failed: {stderr}")
    print(f"road probe physical footprint {peak / 1e9:.3f} GB")
    return json.loads(stdout)


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
    log_c0 = eps * np.log1p(-np.asarray(share)) - lam * np.log1p(-np.asarray(cut))
    # A.time_cost_arm is linear in g once its free-flow cap is applied. Cache
    # unchanged exposure/price weights instead of rebuilding pandas Series for
    # thousands of factorial cells; the original helper remains the parity oracle.
    cache_key = (id(ex), year, r_hours, tau, float(vot["all_purposes_local"]), float(vot["truck_driver"]))
    if cache_key not in ARM_WEIGHTS:
        delay = np.asarray(A.delay_share(ex, year, r_hours))
        passenger = np.asarray(A.others_hours(ex, year)) * float(vot["all_purposes_local"])
        truck = np.asarray(ex.truck_delay_ph) * (1 - tau) * float(vot["truck_driver"])
        fuel = (np.asarray(ex.passenger_fuel_gal) * (1 - np.asarray(ex.phi_commute_route)) * np.asarray(ex.gas_price)
                + np.asarray(ex.truck_fuel_gal) * (1 - tau) * np.asarray(ex.diesel_price))
        ARM_WEIGHTS[cache_key] = delay, passenger + (truck + fuel) / delay
    delay, weights = ARM_WEIGHTS[cache_key]
    g = np.minimum(np.asarray(A.surplus_fraction(log_c0, 0.0)), delay)
    return float(np.nansum((weights * g)[scope]) / 1e9)


def pairing_values(baseline, replacement):
    """Apply the unchanged printed row4/5+ and recipient contract to new dollars."""
    out = {}
    row = baseline["row"]
    for end in ("low", "high"):
        before = baseline["source_published_before"][f"{end}_end"]
        factor = row[f"union_before_boundary_{end}_bn"] / before
        lineage_factor = (1 + row[f"share_{end}"]) * (1 - row[f"recipient_share_{end}"])
        base = before * factor * lineage_factor
        principal = row[f"union_{end}_bn"] + row[f"added_{end}_bn"]
        gate(f"{end}: parent pre-R2b lineage congestion baseline closes (1e-9)", abs(base - principal) < 1e-9)
        value = replacement[end]["congestion_bn"] * factor * lineage_factor
        out[end] = {"baseline_lineage_congestion_bn": principal, "replacement_lineage_congestion_bn": value,
                    "lineage_congestion_delta_bn": value - principal,
                    "source_published_before_bn": before, "source_published_after_bn": replacement[end]["congestion_bn"],
                    "row4_nhts5plus_factor": factor, "original_lineage_road_factor": row[f"share_{end}"],
                    "outside_lineage_recipient_share": row[f"recipient_share_{end}"],
                    "rule": baseline["rule"]}
    return out


def main():
    started = time.perf_counter()
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
    live = live_roads()
    ea = resp["lines"]["economic_affairs_services"]
    hw = [s for s in ea["subfunctions"] if s["subfunction"] == "Highways"]
    gate("highway subfunctions are S&L and federal", sorted(s["level"] for s in hw) == ["federal", "state_local"])
    h, k = {}, {}
    for end in ("low", "high"):
        roads = {r["level"]: r for r in live["ends"][end]["roads"]}
        gate(f"{end}: live highways have both government levels", sorted(roads) == ["federal", "state_local"])
        gate(f"{end}: road keys agree across levels", abs(roads["federal"]["key"] - roads["state_local"]["key"]) < 1e-12)
        gate(f"{end}: personal adopted specification", live["ends"][end]["allocation"] == "personal" and live["ends"][end]["specification"] == {"low": 16, "high": 11}[end])
        h[end] = sum(s["national_bn"] * roads[s["level"]]["response"] for s in hw) / sum(s["national_bn"] for s in hw)
        k[end] = roads["state_local"]["key"]
        gate(f"{end}: live capacity fraction valid", 0 <= h[end] * k[end] < 1)
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
        net[end] = {"congestion_change_bn": main["change_vs_b1_central_bn"],
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
    baseline_path = DERIVED / "congestion_pairing_baseline_oct15.json"
    pairing = pairing_values(json.loads(baseline_path.read_text()), net)
    source_paths = [Path(__file__), Path(A.__file__), baseline_path, DERIVED / "responses.json", FISCAL / "main_case_2026_10_15/derived/corrections.json", FISCAL / "main_case_2026_10_15/derived/summary.json"]
    source_hashes = {str(p.relative_to(HERE.parents[2])): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    document = {
        "case": "oct15", "live_roads": live, "source_hashes": source_hashes,
        "b1_lanes_fixed_bn": b1, "b1_factorial_bn": [min(fixed), max(fixed)], "keyed_proportional_bn": keyed,
        "lanes_coefficient": LANES,
        "note": "Live native road key and actual case responses; capacity follows spending [ASSUMPTION]. Original congestion urban exposures/traffic quantities transported, not observed oct15 geography. Coverage/mixed post-engine resource amounts have no separately measured physical capacity response and are not silently converted to roads. This is congestion only, not the historical service-response account-move total.",
        "by_band_end": net, "pairing_by_end": pairing}
    print(f"physical footprint {MB.require_within_budget('live congestion') / 1e9:.3f} GB; elapsed_s={time.perf_counter()-started:.3f}")
    outputs = {"congestion_bridge_oct15.csv": buf.getvalue(), "net_change_oct15.json": json.dumps(document, indent=1) + "\n",
               "gates_congestion_oct15.json": json.dumps({"gates": GATES}, indent=1) + "\n"}
    with tempfile.TemporaryDirectory(dir=DERIVED) as stage:
        for name, text in outputs.items():
            (Path(stage) / name).write_text(text)
        for name in outputs:
            os.replace(Path(stage) / name, DERIVED / name)
    print(f"\n  B1 lanes fixed {b1:.4f}; keyed proportional {keyed:.4f}")
    for r in rows:
        print(f"  {r['band_end']:4s} {r['variant']:26s} {r['geography']:32s} cut {r['lane_cut']:.5f}  "
              f"{r['congestion_central_bn']:.4f} ({r['factorial_min_bn']:.2f}–{r['factorial_max_bn']:.2f})  change {r['change_vs_b1_central_bn']:+.4f}")
    print(f"all {len(GATES)} gates passed")


if __name__ == "__main__":
    main()

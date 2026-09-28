"""Re-evaluate, on audit row 4's CPS counts, the pairing's social rows whose value is not a plain multiple of
the group's count.

Each lane's own functions are imported read-only (nothing is written beside them) and evaluated twice at the
pairing's central inputs: first with the lane's constants, which must reproduce the lane's published figure
(positive control), then with every CPS count the function reads replaced by its row-4 value from
derived/frame_counts.csv. Inputs from outside the CPS (ACS areas, UMR, NHTS, prices, elasticities, the adopted
case's key shares) are left as the lane has them.

  pm25_consumption        air_pollution_2026_09_28/air_items.py pm_grid: union n and the CPS civilian frame
  road_crash_externality  road_crash_externality_2026_09_28/crash_model.py evaluate_split: union and civilian
                          counts, the union's share of Hispanic residents, and the traffic self-exposure q
                          re-derived from the congestion exposures at the row-4 scale
  congestion (both ends)  service_response_long_run_2026_09_27/congestion.py: the congestion lane's TARGET,
                          which scales the ACS group to the CPS union; the lane cut stays the adopted case's
  housing (both ends)     housing_transfer_2026_09_23/arms.py evaluate, long run, central, form A: TARGET
  fear, security, school  social_costs_unpriced_2026_09_28/items.py: victim cost by offence and the group's
                          offending shares scale with the victim lane's population share s = union 12+ / CPS
                          Hispanic 12+; the population share is the row-4 union over the row-4 frame; the
                          group's pupils move with the union aged 5-17 (the lane's 8.487m is a CPS count)
  scale_net_earnings      scale_spillovers_2026_09_23/arms.py: SCALE (ACS group to the CPS union), the joint
                          central on 1990 CZs; the context main() builds is rebuilt for the pieces it reads
  total_consumer_scale    consumer_scale_2026_09_28/price_items.py main(), run twice with its OUT redirected
                          here: on the lane's own inputs (must reproduce its items.csv byte for byte), then on
                          the row-4 union and the scale lane's CBSA areas at the row-4 scale

A second arm for the two traffic rows puts the NHTS per-person ratios on persons aged 5+ (the roads lane's
cross-lane flag, roads_mileage_key_2026_09_29), with the under-5 shares of the union (u_g) and of other residents
(u_o) on row-4 weights from main_case_decomposition_2026_09_29/derived/age_bins.csv:
  road_crash_externality  the lane's population share P becomes the union's share of persons aged 5+,
                          p(1-u_g) / [p(1-u_g) + (1-p)(1-u_o)], so its traffic share s = P r / (P r + 1 - P)
                          is p(1-u_g)r / [p(1-u_g)r + (1-p)(1-u_o)]; q is commute-based and stays
  congestion              the central row's share is the group's population share (a city-size population
                          elasticity), not a VMT share; the NHTS per-person-5+ ratios enter its vehicle-hour
                          terms (arms.py others_hours, delay_share), where the lane applies one national under-5
                          share to both groups; the arm gives each group its own
Gates for the arm: at u_g = u_o = 0 the crash arm reproduces the row-4 figure; at u_g = u_o = the lane's own
UNDER5_SHARE the congestion arm reproduces the row-4 figures; u_g and u_o equal the roads lane's keys.csv; at the
roads lane's p and 2017 southwest ratio the arm's share formula reproduces its keys.csv vmt_share_group. These
records (suffix _5plus) hold row 4 plus the 5+ basis in the row4_bn column. The crash arm keeps its lane's p, the
union over the CPS civilian frame; road_crash_externality_5plus_account_p is a sensitivity outside the pairing,
with the roads lane's p (the account's per-head cell, a share of all residents).

Gates (exit 1, nothing written to reeval.csv): every positive control; the lanes' union counts equal the frame's
published count. Writes derived/reeval.csv, derived/area_measures_cbsa_row4.csv and
derived/consumer_scale_rerun/. Run from the repository root after frame_counts.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline --with statsmodels python3 \\
      infra/immigration-fiscal/population_basis_2026_09_29/reeval.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived" / "reeval.csv"
AGE_BINS = FISCAL / "main_case_decomposition_2026_09_29" / "derived" / "age_bins.csv"
ROADS_KEYS = FISCAL / "roads_mileage_key_2026_09_29" / "derived" / "keys.csv"
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load(name, path):
    """A lane's script as a module; its main() is guarded, so nothing runs or writes."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def counts():
    with (HERE / "derived" / "frame_counts.csv").open() as handle:
        return {r["count"]: (float(r["published"]), float(r["row4"])) for r in csv.DictReader(handle)}


def under5_shares():
    """The union's and other residents' under-5 shares on row-4 weights, and the two totals they divide by."""
    pop = [r for r in csv.DictReader(AGE_BINS.open()) if r["weights"] == "row4" and r["key"] == "extra|pop"]
    union, national = (sum(float(r[c]) for r in pop) for c in ("union", "national"))
    union5, national5 = (sum(float(r[c]) for r in pop if int(r["bin"]) < 5) for c in ("union", "national"))
    return union5 / union, (national5 - union5) / (national - union), union, national


def hours_5plus(u_g, u_o):
    """congestion_2026_09_23/arms.py others_hours and delay_share with each group's own under-5 share (the lane
    applies UNDER5_SHARE to both). NHTS hours per person are per person aged 5+."""
    def others_hours(e, year):
        return e.other_persons * (1 - u_o) * e[f"h_other_{year}"]

    def delay_share(e, year, r_hours):
        total = (e.other_persons * (1 - u_o) + e.group_persons * (1 - u_g) * r_hours) * e[f"h_other_{year}"]
        return (e.passenger_delay_ph / total).clip(upper=0.6)
    return others_hours, delay_share


def item_central(path, item, group="mexican_origin", measure="absolute"):
    rows = [r for r in csv.DictReader(path.open()) if r["item"] == item and r["group"] == group
            and r.get("measure", "absolute") == measure]
    if len(rows) != 1:
        raise SystemExit(f"[BLOCKED] {path}: {len(rows)} rows for {item}")
    return float(rows[0]["central_bn"])


def main():
    k = counts()
    n0, n4 = k["union|all"]
    civ0, civ4 = k["cps_all_civilian|all"]
    s12 = {w: k["union|12_plus"][i] / k["cps_hispanic_civilian|12_plus"][i] for i, w in enumerate(("published", "row4"))}
    f_s = s12["row4"] / s12["published"]
    u_g, u_o, u_union, u_national = under5_shares()
    roads = next(csv.DictReader(ROADS_KEYS.open()))
    gate("age bins are on the row-4 union and frame", abs(u_union - n4) < 1e-3 and abs(u_national - civ4) < 1e-3,
         f"{u_union:,.2f}, {u_national:,.2f}")
    gate("under-5 shares equal the roads lane's", abs(u_g - float(roads["under5_group"])) < 1e-6
         and abs(u_o - float(roads["under5_others"])) < 1e-6, f"u_g {u_g:.6f}, u_o {u_o:.6f}")
    rows = []

    def record(row, published, row4, control, method):
        rows.append(dict(row=row, published_bn=published, row4_bn=row4, factor=row4 / published,
                         control_published_bn=control, method=method))

    print("[pm25_consumption]", flush=True)
    air = load("air_items", FISCAL / "air_pollution_2026_09_28" / "air_items.py")

    def pm_central():
        grid, s = air.pm_grid("mexican_origin")
        cen = grid[(grid[[c for c in grid.columns if c.startswith("i_")]] == 1).all(axis=1)].iloc[0]
        return float(cen.others * cen.morb * air.VSL_DOT_2024 / 1e9), s

    want = item_central(FISCAL / "air_pollution_2026_09_28" / "derived" / "items.csv", "pm25_consumption")
    gate("air lane's union and frame are the published CPS counts",
         abs(air.GROUPS["mexican_origin"]["n"] - n0) < 0.5 and abs(air.POP_ALL - civ0) < 0.5)
    pub, s_pub = pm_central()
    gate("pm25 central reproduces items.csv", abs(pub - want) < 5e-5, f"{pub:.6f} vs {want}")
    air.GROUPS["mexican_origin"]["n"], air.POP_ALL = n4, civ4
    new, s_new = pm_central()
    record("pm25_consumption", pub, new, want, f"pm_grid central; s {s_pub:.6f} -> {s_new:.6f} (union / CPS civilian frame)")

    print("[congestion: long-run response lane, band ends]", flush=True)
    cong = load("long_run_congestion", FISCAL / "service_response_long_run_2026_09_27" / "congestion.py")
    A = cong.A
    net = json.loads((cong.DERIVED / "net_change.json").read_text())
    resp = json.loads((cong.DERIVED / "responses.json").read_text())
    cand = json.loads((cong.DERIVED / "candidate_band.json").read_text())
    ea = resp["lines"]["economic_affairs_services"]
    hw = [s for s in ea["subfunctions"] if s["subfunction"] == "Highways"]
    h = {end: sum(s["national_bn"] * s["response"][end] for s in hw) / sum(s["national_bn"] for s in hw) for end in ("low", "high")}
    key = {end: cand["group_amounts_at_end_specifications_bn"][end]["economic_affairs_services"] / ea["national_bn"]
           for end in ("low", "high")}

    def congestion(target):
        A.TARGET = target
        _, nhts, tau, vots, exposures, _ = cong.setup()
        e = exposures["2017 southwest"]
        scope = e["in_scope"].to_numpy()
        r_h = nhts["2017 southwest"]["r_hours"]
        eps = A.POP_FIXED_LANES["central"]
        ends = {end: cong.arm(e, scope, e.s, eps, A.LANES_COEF_T10, h[end] * key[end], tau["central"], vots["central"],
                              2022, r_h) for end in ("low", "high")}
        b1 = cong.arm(e, scope, e.s, eps, 0.0, 0.0, tau["central"], vots["central"], 2022, r_h)
        ok = e.phi_commute_route.notna() & e.acs_group_vehicle_minutes.notna()
        q = float((e.acs_group_vehicle_minutes * e.phi_commute_route)[ok].sum() / e.acs_group_vehicle_minutes[ok].sum())
        return ends, b1, q, target / json.loads((A.DERIVED / "pums_commute_checks.json").read_text())["group_persons_acs"]

    gate("congestion lane's TARGET is the published CPS union", abs(A.TARGET - n0) < 0.5, f"{A.TARGET:,.1f}")
    target_lane = A.TARGET
    ends0, b10, q0, scale0 = congestion(target_lane)
    for end in ("low", "high"):
        want = net["by_band_end"][end]["congestion_bn"]
        gate(f"congestion at the {end} band end reproduces net_change.json", abs(ends0[end] - want) < 1e-9,
             f"{ends0[end]:.9f} vs {want:.9f}")
    gate("B1 with lanes fixed reproduces net_change.json", abs(b10 - net["b1_lanes_fixed_bn"]) < 1e-9, f"{b10:.6f}")
    ends4, b14, q4, scale4 = congestion(n4)
    lane_hours = (A.others_hours, A.delay_share)
    A.others_hours, A.delay_share = hours_5plus(A.UNDER5_SHARE, A.UNDER5_SHARE)
    same = congestion(n4)[0]
    A.others_hours, A.delay_share = hours_5plus(u_g, u_o)
    ends5 = congestion(n4)[0]
    A.others_hours, A.delay_share = lane_hours
    for end in ("low", "high"):
        gate(f"congestion 5+ arm at the lane's one under-5 share ({A.UNDER5_SHARE:.6f}) reproduces the row-4 {end} end",
             abs(same[end] - ends4[end]) < 1e-9, f"{same[end]:.9f} vs {ends4[end]:.9f}")
    A.TARGET = target_lane
    for end in ("low", "high"):
        record(f"congestion_{end}_end", ends0[end], ends4[end], net["by_band_end"][end]["congestion_bn"],
               f"network follows spending, uniform cut {h[end] * key[end]:.6f} held; CPS scale {scale0:.6f} -> {scale4:.6f}")
    record("congestion_b1_lanes_fixed", b10, b14, net["b1_lanes_fixed_bn"], "reference: B1 with lanes fixed (not in the pairing)")

    print("[road_crash_externality]", flush=True)
    crash = load("crash_model", FISCAL / "road_crash_externality_2026_09_28" / "crash_model.py")
    levels = {**crash.FACTORS, **crash.x_levels_evidence()}
    nf_or = crash.ccrs_nonfatal_or()

    def crash_central():
        return crash.evaluate_split(*[levels[x][1] for x in crash.FACTORS], r_nf=nf_or[1], composition=True)["total"]

    model = json.loads((FISCAL / "road_crash_externality_2026_09_28" / "derived" / "model.json").read_text())
    gate("crash lane's union and frame are the published CPS counts", abs(crash.N_GROUP - n0) < 0.5 and abs(crash.N_ALL - civ0) < 0.5)
    gate("congestion exposures at the lane's scale reproduce the crash lane's q", abs(q0 - crash.Q_METRO) < 1e-12, f"{q0:.9f}")
    pub = crash_central()
    gate("crash central reproduces model.json", abs(pub - model["central"]["total"]) < 1e-12, f"{pub:.9f}")
    mex_of_hisp4 = k["union_hispanic|all"][1] / k["cps_hispanic_civilian|all"][1]
    crash.N_GROUP, crash.N_ALL, crash.P_SHARE = n4, civ4, n4 / civ4
    crash.MEX_OF_HISP, crash.Q_METRO = mex_of_hisp4, q4
    new = crash_central()
    p4, r_c = n4 / civ4, crash.VMT_RATIO_OTHERS["central"]

    def share5(p, ug, uo):
        """The union's share of persons aged 5+; the lane's s = P r / (P r + 1 - P) then applies the NHTS ratio."""
        return p * (1 - ug) / (p * (1 - ug) + (1 - p) * (1 - uo))

    def vmt_share(P, r):
        return P * r / (P * r + 1 - P)

    P5 = share5(p4, u_g, u_o)
    crash.P_SHARE = share5(p4, 0.0, 0.0)
    zero = crash_central()
    crash.P_SHARE = P5
    crash5 = crash_central()
    p_acct, rho_acct = float(roads["per_head_share"]), float(roads["ratio_per_person_5plus"])
    P5_acct = share5(p_acct, u_g, u_o)
    gate("the 5+ share at the roads lane's p and 2017 southwest ratio reproduces its keys.csv",
         roads["nhts_ratio"] == "2017_southwest"
         and abs(vmt_share(P5_acct, rho_acct) - float(roads["vmt_share_group"])) < 1e-6,
         f"{vmt_share(P5_acct, rho_acct):.7f} vs {roads['vmt_share_group']}")
    crash.P_SHARE = P5_acct
    crash5_acct = crash_central()
    crash.P_SHARE = p4
    gate("crash 5+ arm at u_g = u_o = 0 reproduces the row-4 figure", abs(zero - new) < 1e-12, f"{zero:.9f} vs {new:.9f}")
    crash_pub, crash_s = pub, [vmt_share(P, r_c) for P in (p4, P5)]
    record("road_crash_externality", pub, new, model["central"]["total"],
           f"evaluate_split central with the composition term; population share {n0 / civ0:.6f} -> {n4 / civ4:.6f}, "
           f"q {q0:.6f} -> {q4:.6f}, union share of Hispanic residents {crash.cps()[2]:.6f} -> {mex_of_hisp4:.6f}")

    print("[housing: long run, central, form A]", flush=True)
    hou = load("housing_arms", FISCAL / "housing_transfer_2026_09_23" / "arms.py")
    summ = pd.read_csv(hou.DERIVED / "arms_summary.csv")
    summ = summ[(summ.arm == "long_run") & (summ.metric == "net_other_residents_welfare_bn")].iloc[0]

    def housing(target):
        hou.TARGET = target
        areas, _ = hou.load_areas()
        return {geo: hou.evaluate(areas, "long_run", "central", "A", geo, "central")["net_other_residents_welfare_bn"]
                for geo in ("metro_local", "national_uniform")}

    gate("housing lane's TARGET is the published CPS union", abs(hou.TARGET - n0) < 0.5)
    target_lane = hou.TARGET
    h0, h4 = housing(target_lane), housing(n4)
    hou.TARGET = target_lane
    for geo, end in (("metro_local", "low"), ("national_uniform", "high")):
        gate(f"housing {geo} reproduces arms_summary.csv", abs(h0[geo] - float(summ[f"central_{geo}"])) < 1e-9, f"{h0[geo]:.9f}")
        record(f"housing_gain_{end}_end", h0[geo], h4[geo], float(summ[f"central_{geo}"]),
               f"long run, central, form A, {geo}; TARGET {target_lane:,.0f} -> {n4:,.1f}")

    print("[fear, private security, school disruption]", flush=True)
    sc = load("social_items", FISCAL / "social_costs_unpriced_2026_09_28" / "items.py")
    items = FISCAL / "social_costs_unpriced_2026_09_28" / "derived" / "items.csv"
    g = "mexican_origin"
    gate("social-costs lane's union and frame are the published CPS counts", abs(sc.N[g] - n0) < 0.5 and abs(sc.POP_ALL - civ0) < 0.5)
    fear0, sec0, school0 = sc.fear(g, "central"), sc.security(g)[1], sc.school_range(g)[1]
    for name, v in (("fear_avoidance", fear0), ("private_security", sec0), ("school_disruption", school0)):
        want = item_central(items, name)
        gate(f"{name} central reproduces items.csv", abs(round(v, 2) - want) < 1e-9, f"{v:.6f} vs {want}")
    saved = dict(sc.V[g])
    sc.V[g] = {o: v * f_s for o, v in saved.items()}
    fear4 = sc.fear(g, "central")
    sc.V[g] = saved
    exc0 = sc.W_PROP * sc.mex_prop_cost + (1 - sc.W_PROP) * sc.mex_viol_ncvs - sc.SHARE[g]
    gate("security's central excess share rebuilds from its parts", abs(exc0 - sc.EXC[g]["central"]) < 1e-15, f"{exc0:.6f}")
    exc4 = (sc.W_PROP * sc.mex_prop_cost + (1 - sc.W_PROP) * sc.mex_viol_ncvs) * f_s - n4 / civ4
    sec4 = sc.s_total(1)[0] * exc4
    pupils = k["union|5_17"][1] / k["union|5_17"][0]
    share0, share4 = sc.PUPIL_SHARE[g], 8.487 * pupils / (8.487 * pupils + 39.45)
    gate("school's pupil share is 8.487m over 8.487m + 39.45m", abs(share0 - 8.487 / (8.487 + 39.45)) < 1e-15)
    sc.PUPIL_SHARE[g] = share4
    school4 = sc.school_range(g)[1]
    sc.PUPIL_SHARE[g] = share0
    record("fear_avoidance", fear0, fear4, item_central(items, "fear_avoidance"),
           f"victim cost by offence x s ratio {f_s:.6f} (union 12+ / CPS Hispanic 12+)")
    record("private_security", sec0, sec4, item_central(items, "private_security"),
           f"crime-driven spend x (offending share x {f_s:.6f} - population share {n4 / civ4:.6f}); excess {exc0:.6f} -> {exc4:.6f}")
    record("school_disruption", school0, school4, item_central(items, "school_disruption"),
           f"group pupils 8.487m x {pupils:.6f} (union aged 5-17); pupil share {share0:.6f} -> {share4:.6f}")

    print("[scale_net_earnings: CZ 1990 joint, central]", flush=True)
    sca = load("scale_arms", FISCAL / "scale_spillovers_2026_09_23" / "arms.py")
    _, cry_joint, _ = sca.cry_regressions()
    # The context main() builds, for the pieces the joint specifications read (arms.py main()).
    nat_table = pd.read_csv(sca.DERIVED / "pums_national.csv")
    sw = pd.read_csv(sca.DERIVED / "sample_weights.csv").set_index(["year", "cell"])
    all_w = nat_table[nat_table.label == "all"].set_index("item")["estimate"]
    w_more = all_w["workers_sc"] + all_w["workers_ba"] + all_w["workers_grad"]
    e_more = all_w["earnings_sc"] + all_w["earnings_ba"] + all_w["earnings_grad"]
    rel = (e_more / w_more) / ((all_w["earnings"] - e_more) / (all_w["workers"] - w_more))
    s_cry = cry_joint["s_sc_cry_sample"]
    ba2000 = {"s": float(np.mean([sw.loc[(2000, "ba"), "worker_share"]])),
              "theta": float(np.mean([sw.loc[(2000, "ba"), "income_share"]]))}
    ctx = {"cry_joint": cry_joint, "shares": {"sc_cry": {"s": s_cry, "theta": float(s_cry * rel / (s_cry * rel + 1 - s_cry))},
                                              "ba_2000": ba2000}}
    _, params, _, fn, _ = next(s for s in sca.joint_specs(ctx) if s[0].endswith("[central]"))
    values = np.array([p[0] for p in params], float)

    def scale_eval(scale):
        sca.SCALE = scale
        wide = sca.load_cells()
        cz = sca.measures(sca.cz_areas(wide))
        gain = sca.gain_parts(cz, fn(cz, values))[0] / 1e9
        cb_raw, names, land = sca.cbsa_areas(wide)
        cb = sca.measures(cb_raw, land)
        cb["E_all"] = cb["other_earnings"]
        return gain, cb.assign(name=cb.index.map(lambda a: names.get(a, a)))

    summ = pd.read_csv(sca.DERIVED / "summary.csv")
    want = float(summ[(summ.table == "joint_grid") & (summ.geography == "CZ 1990")].gain_bn.iloc[0])
    gate("scale lane's CPS_UNION is the published union", abs(sca.CPS_UNION - n0) < 0.5, f"{sca.CPS_UNION:,}")
    scale_lane = sca.SCALE
    gain0, cb0 = scale_eval(scale_lane)
    gate("scale joint central reproduces summary.csv", abs(gain0 - want) < 1e-9, f"{gain0:.9f} vs {want:.9f}")
    lane_cb = pd.read_csv(sca.DERIVED / "area_measures_cbsa.csv", dtype={"area": str}).set_index("area")
    numeric = [c for c in lane_cb.columns if c != "name"]
    mine = cb0.reindex(lane_cb.index)[numeric].to_numpy(float)
    theirs = lane_cb[numeric].to_numpy(float)
    both = ~(np.isnan(mine) & np.isnan(theirs))
    worst = float(np.nanmax(np.abs(mine - theirs)[both] / np.maximum(np.abs(theirs[both]), 1e-300)))
    gate("CBSA measures at the lane's scale reproduce area_measures_cbsa.csv", len(cb0) == len(lane_cb) and worst < 1e-12,
         f"{len(cb0)} areas, worst relative difference {worst:.1e}")
    scale4 = n4 / sca.ACS_GROUP
    gain4, cb4 = scale_eval(scale4)
    sca.SCALE = scale_lane
    record("scale_net_earnings", -gain0, -gain4, -want,
           f"CRY joint central on 1990 CZs; ACS group scaled to the CPS union x {scale_lane:.6f} -> {scale4:.6f}")
    area4 = HERE / "derived" / "area_measures_cbsa_row4.csv"
    cb4.index.name = "area"
    cb4.to_csv(area4, lineterminator="\n")

    print("[total_consumer_scale: the lane's main() with its inputs and outputs in this lane]", flush=True)
    cs = load("consumer_scale", FISCAL / "consumer_scale_2026_09_28" / "price_items.py")
    lane_items = cs.OUT / "items.csv"
    runs = HERE / "derived" / "consumer_scale_rerun"
    gate("consumer-scale lane reads the published union", abs(float(pd.read_csv(cs.POP).set_index("group").loc["union", "all_ages"]) - n0) < 0.5)
    cs.OUT = runs / "published"
    cs.OUT.mkdir(parents=True, exist_ok=True)
    cs.main()
    gate("consumer-scale rerun on the lane's inputs reproduces its items.csv byte for byte",
         (cs.OUT / "items.csv").read_bytes() == lane_items.read_bytes())
    pop4 = runs / "target_population_row4.csv"
    with pop4.open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["group", "all_ages"])
        out.writerow(["union", repr(n4)])
    cs.OUT, cs.AREAS, cs.POP = runs / "row4", area4, pop4
    cs.OUT.mkdir(parents=True, exist_ok=True)
    cs.main()
    pub = item_central(lane_items, "total_consumer_scale")
    record("total_consumer_scale", pub, item_central(cs.OUT / "items.csv", "total_consumer_scale"), pub,
           "the lane's main() on the row-4 union and CBSA areas (area_measures_cbsa_row4.csv); items.csv rounds to 4 dp")

    for end in ("low", "high"):
        record(f"congestion_{end}_end_5plus", ends0[end], ends5[end], net["by_band_end"][end]["congestion_bn"],
               f"row 4 plus the 5+ basis: others' vehicle-occupant hours on (1 - u_o) = {1 - u_o:.6f} and the group's on "
               f"(1 - u_g) = {1 - u_g:.6f}, against the lane's one (1 - {A.UNDER5_SHARE:.6f}); share, cut and q unchanged")
    record("road_crash_externality_5plus", crash_pub, crash5, model["central"]["total"],
           f"row 4 plus the 5+ basis: P = the union's share of persons aged 5+, {p4:.6f} -> {P5:.6f}; "
           f"traffic share s at r = {r_c} {crash_s[0]:.6f} -> {crash_s[1]:.6f}; q {q4:.6f} (commute-based) unchanged")
    record("road_crash_externality_5plus_account_p", crash_pub, crash5_acct, model["central"]["total"],
           f"sensitivity, not in the pairing: the 5+ arm on the roads lane's p, the account's per-head cell {p_acct} "
           f"(a share of all residents, not of the CPS frame); P {P5_acct:.6f}, s at r = {r_c} {vmt_share(P5_acct, r_c):.6f}")
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({c: (f"{v:.9f}" if isinstance(v, float) else v) for c, v in r.items()})
    for r in rows:
        print(f"  {r['row']:28s} {r['published_bn']:>11.6f} -> {r['row4_bn']:>11.6f}  x{r['factor']:.6f}")
    print(f"  wrote {len(rows)} rows -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()

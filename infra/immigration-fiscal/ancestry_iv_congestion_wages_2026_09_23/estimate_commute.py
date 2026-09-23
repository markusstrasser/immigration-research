"""Commute time against the 2000-2010 inflow, instrumented by the ancestry prediction.

Outcomes (derived/commute_metro.csv, from build_commute.py)
  commute              mean one-way minutes, workers not at home (all workers, summary tables)
  commute_nontransit   the same without public transport
  sh_transit, sh_home, sh_alone, sh_carpool   commute-mode shares, points of workers
  PUMS natives (derived/pums_metro.csv): natives' mean minutes, natives' car-commute minutes
Treatments
  dX      change in the foreign-born share of population, points
  dlnpop  change in log population (SF1 2000 and 2010 counts on 2013 CBSAs)
Samples: FG (fixed 2013 geography; primary) and PC (the ancestry lane's 334, 2010 on the published
2009 delineation).

The speed conversion: commute minutes = distance / speed, so with distance fixed the elasticity of
speed to population is minus the elasticity of minutes to population. Set against Couture,
Duranton and Turner's -0.12 (SE 0.035) at fixed lanes, the congestion lane's B1 input.

Writes derived/estimates_commute.csv and derived/commute_implications.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
    python3 infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/estimate_commute.py
"""
import importlib.util
import json
import sys

import numpy as np
import pandas as pd

from common import DERIVED, HERE, gates, menu, sample_fg, sample_pc, wls

CONG = HERE.parent / "congestion_2026_09_23"
B1_GRID = {"low": 0.085, "central": 0.12, "high": 0.155}  # the congestion lane's POP_FIXED_LANES
CDT = (0.12, 0.035)


def b1_model():
    """The congestion lane's own arm B1 as a function of the elasticity: arms.arm_pop (ln C0 =
    eps ln(1 - s) in each urban area, capped at free flow, valued on others' hours) on its saved
    central exposure (derived/ua_exposure.csv, 2017-southwest NHTS inputs) with its central tau,
    value of time, hours ratio and 2022 hours. Imported without writing bytecode into that lane.
    Positive control: its three B1 grid points (other factors central) to 1e-6bn, or [BLOCKED]."""
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("congestion_arms", CONG / "arms.py")
    arms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arms)
    e = pd.read_csv(CONG / "derived" / "ua_exposure.csv")
    scope = e["in_scope"].astype(bool).to_numpy()
    par = pd.read_csv(CONG / "derived" / "parameters.csv").set_index("parameter")["value"]
    vot = pd.read_csv(CONG / "derived" / "vot_2024.csv").set_index("level").loc["central"]
    tau, r_hours = float(par["tau_central"]), float(par["r_hours_central"])

    def b1(eps):
        res = arms.arm_pop(e, e.s, float(eps), 0.0, tau, e.phi_commute_route, vot, 2022, r_hours)
        return arms.summarise(res, e, scope)["total_bn"]

    g = pd.read_csv(CONG / "derived" / "arms_grid.csv")
    g = g[g.approach.eq("B1 population elasticity, lanes fixed") & g.f_vot.eq("central") & g.f_tau.eq("central")
          & g.f_nhts.eq("2017 southwest") & g.f_share.eq("population") & g.f_hours.eq(2022)]
    control = {}
    for lab, eps in B1_GRID.items():
        ref = float(g.loc[g.f_elasticity.eq(lab), "total_bn"].iloc[0])
        control[str(eps)] = {"lane_grid_bn": ref, "model_bn": b1(eps)}
        if abs(control[str(eps)]["model_bn"] - ref) > 1e-6:
            raise SystemExit(f"[BLOCKED] congestion-model reproduction failed at {eps}: {control}")
    return b1, control


def pums_commute():
    p = pd.read_csv(DERIVED / "pums_metro.csv", dtype={"cbsa": str})
    out = {}
    for samp, tag in ((200001, "0"), (201001, "1"), (201103, "3")):
        s = p[p["sample"] == samp].set_index("cbsa")
        out[f"pcommute_nat_{tag}"] = s.commute_min_nat / s.commuters_nat
        out[f"pcar_nat_{tag}"] = s.car_min_nat / s.car_nat
        out[f"pcommute_all_{tag}"] = s.commute_min / s.commuters
    return pd.DataFrame(out).reset_index()


def main():
    g = gates()
    print("gates passed:", g)
    cm = pd.read_csv(DERIVED / "commute_metro.csv", dtype={"cbsa": str})
    try:
        pc_ = pums_commute()
        cm = cm.merge(pc_, on="cbsa", how="left")
    except FileNotFoundError:
        print("[note] derived/pums_metro.csv absent; PUMS commute outcomes skipped")
    rows = []
    fg = sample_fg()
    for design, frame, suffix in (("FG", fg, "1f"), ("FG_noLA", fg[fg.cbsa != "31080"], "1f"),
                                  ("PC", sample_pc(), "1p")):
        m = frame.merge(cm, on="cbsa", how="left")
        if design.startswith("FG"):
            m["dX"] = m.fb_share_1f - m.fb_share
        m["dlnpop"] = m.dlnpop_sf1
        for base in ("commute", "commute_nontransit", "sh_transit", "sh_home", "sh_alone", "sh_carpool"):
            m[f"d_{base}"] = m[f"{base}_{suffix}"] - m[f"{base}_0"]
            if base.startswith("commute"):
                m[f"dln_{base}"] = np.log(m[f"{base}_{suffix}"] / m[f"{base}_0"])
                m[f"ln_{base}_0"] = np.log(m[f"{base}_0"])
        m["lnpop0"] = np.log(m["pop"])
        if "pcommute_nat_0" in m:
            for v in ("pcommute_nat", "pcar_nat", "pcommute_all"):
                for tag in ("1", "3"):
                    m[f"dln_{v}_{tag}"] = np.log(m[f"{v}_{tag}"] / m[f"{v}_0"])
                    m[f"d_{v}_{tag}"] = m[f"{v}_{tag}"] - m[f"{v}_0"]
                m[f"ln_{v}_0"] = np.log(m[f"{v}_0"])
        b = {"design": design}
        # minutes and log minutes on the foreign-born share change
        for oc in ("commute", "commute_nontransit"):
            menu(rows, m, f"d_{oc}", "dX", {**b, "outcome": f"{oc} (minutes)"}, y0=f"{oc}_0",
                 placebo_extra=["lnpop0"])
            menu(rows, m, f"dln_{oc}", "dX", {**b, "outcome": f"log {oc}"}, y0=f"ln_{oc}_0",
                 placebo_extra=["lnpop0"])
            menu(rows, m, f"dln_{oc}", "dX", {**b, "outcome": f"log {oc}, mode-share controls"},
                 controls=["d_sh_transit", "d_sh_home"])
            # the elasticity: log minutes on log population
            menu(rows, m, f"dln_{oc}", "dlnpop", {**b, "outcome": f"log {oc}"}, y0=f"ln_{oc}_0",
                 placebo_extra=["lnpop0"])
            menu(rows, m, f"dln_{oc}", "dlnpop", {**b, "outcome": f"log {oc}, mode-share controls"},
                 controls=["d_sh_transit", "d_sh_home"])
        for oc in ("sh_transit", "sh_home", "sh_alone", "sh_carpool"):
            menu(rows, m, f"d_{oc}", "dX", {**b, "outcome": f"{oc} (points)"}, y0=f"{oc}_0")
        menu(rows, m, "dlnpop", "dX", {**b, "outcome": "log population (SF1)"})
        if design.startswith("FG") and "pcommute_nat_0" in m:
            for v, lab in (("pcommute_nat", "PUMS natives' commute"), ("pcar_nat", "PUMS natives' car commute"),
                           ("pcommute_all", "PUMS all workers' commute")):
                for tag, s in (("1", "2010 ACS"), ("3", "2009-11 ACS")):
                    menu(rows, m, f"dln_{v}_{tag}", "dlnpop", {**b, "outcome": f"log {lab}, {s}"},
                         y0=f"ln_{v}_0", placebo_extra=["lnpop0"])
                    menu(rows, m, f"dln_{v}_{tag}", "dX", {**b, "outcome": f"log {lab}, {s}"},
                         y0=f"ln_{v}_0")
        # diagnostics: population growth and the foreign-born change per unit of Z2
        d = m.dropna(subset=["dlnpop", "Z2", "w"])
        r = wls(d.dlnpop, d[["Z2"]], d.w)
        print(f"{design}: n {len(d)}; dlnpop on Z2 {r.params['Z2']:.4f} ({r.bse['Z2']:.4f})")
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "estimates_commute.csv", index=False)

    # ---- implications for the congestion lane's B1
    def pick(design, outcome, x, estimator):
        r = est[(est.design == design) & (est.outcome == outcome) & (est.x == x) & (est.estimator == estimator)]
        return (float(r.coef.iloc[0]), float(r.se.iloc[0])) if len(r) else (np.nan, np.nan)

    b1_of, control = b1_model()
    imp = {"b1_model_positive_control": control, "cdt": CDT, "rows": []}
    fs_dlnpop = {d_: float(est[(est.design == d_) & (est.outcome == "log commute") & (est.x == "dlnpop")
                               & (est.estimator == "first stage on Z2")].F.iloc[0]) for d_ in ("FG", "FG_noLA", "PC")}
    for design in ("FG", "FG_noLA", "PC"):
        for outcome in ("log commute", "log commute_nontransit", "log commute, mode-share controls",
                        "log commute_nontransit, mode-share controls",
                        "log PUMS natives' car commute, 2010 ACS", "log PUMS natives' car commute, 2009-11 ACS",
                        "log PUMS natives' commute, 2010 ACS", "log PUMS natives' commute, 2009-11 ACS"):
            for estimator in ("OLS", "IV with Z2", "IV with Z2_exmex", "IV with Z"):
                beta, se = pick(design, outcome, "dlnpop", estimator)
                if not np.isfinite(beta):
                    continue
                eps = beta  # speed elasticity is -beta; B1 uses its magnitude
                z = (beta - CDT[0]) / np.sqrt(se ** 2 + CDT[1] ** 2)
                # Z2 barely moves log population (first-stage F below 2 for log commute), so the IV
                # rows' Wald bounds are not valid intervals; the AR sets in estimates_commute.csv are
                bound = ("Wald" if estimator == "OLS" else
                         f"Wald, invalid: first-stage F {fs_dlnpop[design]:.2f} (log-commute sample)")
                imp["rows"].append(dict(design=design, outcome=outcome, estimator=estimator,
                                        time_elasticity=beta, se=se, speed_elasticity=-beta, bound=bound,
                                        z_vs_cdt=z, b1_central_bn=float(b1_of(max(eps, 0.0))),
                                        b1_lo_bn=float(b1_of(max(eps - 1.96 * se, 0.0))),
                                        b1_hi_bn=float(b1_of(max(eps + 1.96 * se, 0.0)))))
    # the foreign-born-share design, converted with the no-displacement population change per point
    # (d ln P = d s / (1 - s), s the 2000 population-weighted foreign-born share of the sample)
    fg_all = sample_fg().set_index("cbsa")
    for design in ("FG", "FG_noLA", "PC"):
        fr = sample_fg() if design.startswith("FG") else sample_pc()
        if design == "FG_noLA":
            fr = fr[fr.cbsa != "31080"]
        s0 = float(np.average(fg_all.loc[fr.cbsa, "fb_share"], weights=fr.w)) / 100
        per_pt = 1.0 / (1.0 - s0)  # percent population per point of foreign-born share
        for outcome in ("log commute", "log commute, mode-share controls",
                        "log PUMS natives' car commute, 2009-11 ACS", "log PUMS natives' commute, 2009-11 ACS",
                        "log PUMS natives' car commute, 2010 ACS"):
            # the baseline-level arm answers the failed level placebo; menu() computes no AR set for it,
            # so its bound is the Wald interval
            for estimator in ("IV with Z2", "IV with Z2 + baseline level"):
                r = est[(est.design == design) & (est.outcome == outcome) & (est.x == "dX")
                        & (est.estimator == estimator)]
                if not len(r):
                    continue
                r = r.iloc[0]
                conv = 100.0 / per_pt  # log minutes per point -> elasticity of minutes to population
                if estimator == "IV with Z2":
                    bound = "AR" if r.ar_kind == "bounded" else f"AR {r.ar_kind}"
                    lo_, hi_ = (r.ar_lo * conv, r.ar_hi * conv) if r.ar_kind == "bounded" else (-np.inf, np.inf)
                else:
                    bound = "Wald"
                    lo_, hi_ = (r.coef - 1.96 * r.se) * conv, (r.coef + 1.96 * r.se) * conv
                imp["rows"].append(dict(design=design, outcome=outcome + " [via dX]", estimator=estimator,
                                        time_elasticity=r.coef * conv, se=r.se * conv,
                                        speed_elasticity=-r.coef * conv,
                                        ar_lo=lo_, ar_hi=hi_, bound=bound, fb_share_2000=s0,
                                        pop_pct_per_point=per_pt,
                                        z_vs_cdt=(r.coef * conv - CDT[0]) / np.sqrt((r.se * conv) ** 2 + CDT[1] ** 2),
                                        b1_central_bn=float(b1_of(max(r.coef * conv, 0.0))),
                                        b1_hi_bn=float(b1_of(max(hi_, 0.0))) if np.isfinite(hi_) else np.inf))
    (DERIVED / "commute_implications.json").write_text(json.dumps(imp, indent=1, default=float))
    with pd.option_context("display.width", 250, "display.max_rows", 400):
        show = est[est.estimator.isin(["first stage on Z2", "first stage on Z2_exmex", "OLS", "reduced form on Z2",
                                       "IV with Z2", "IV with Z2_exmex", "IV with Z", "IV with Z+Z2",
                                       "level placebo: Z2 on 2000 level",
                                       "level placebo: Z2 on 2000 level given lnpop0"])]
        print(show[["design", "outcome", "x", "controls", "estimator", "n", "coef", "se", "F", "hansen_p"]]
              .round(4).to_string(index=False))
        print(pd.DataFrame(imp["rows"]).round(3).to_string(index=False))


if __name__ == "__main__":
    main()

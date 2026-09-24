"""Collect every specification of the five arms into derived/ratio_adjustments.csv, with the net
bands for murder and robbery.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/ratio_adjustments.py

Run after nibrs_impute.py, nibrs_checks.py, shr_impute.py, ncvs_select.py, ncvs_units.py,
arm5_white_subtraction.py and dollar_effects.py. Reads their derived CSVs only.

Columns: offence, method, hispanic_div_nh_white, hispanic_div_all, change_vs_central (Hispanic ÷
NH white, relative), plus arm, frame, the central each row is compared with, and a note. Rows in
another frame than the NIBRS offender central say so in `frame`; `change_vs_central` compares
each row with the central of its own frame unless `central_frame` says otherwise.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import ncvs_select as ns

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
NIBRS_FRAME = "NIBRS offenders, TX+AZ 2022-23, agencies recording >= 50% (lane central)"
# 2020 Post-Enumeration Survey: Hispanic net undercount 4.99%, non-Hispanic white alone net
# overcount 1.64%, nation -0.24% (overcount, not significant) [_cache/pes/census_pes_2022_03_10.html]
PES_H, PES_NHW, PES_ALL = 0.0499, -0.0164, -0.0024
F_NHW = (1 - PES_H) / (1 - PES_NHW)          # census-based rate ratio -> true-population rate ratio
F_ALL = (1 - PES_H) / (1 - PES_ALL)
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def row(offence, method, arm, frame, h_nhw, h_all, c_nhw, c_all, note="", central_frame=None):
    return dict(offence=offence, method=method, hispanic_div_nh_white=h_nhw, hispanic_div_all=h_all,
                change_vs_central=(h_nhw / c_nhw - 1) if c_nhw and not pd.isna(h_nhw) else np.nan,
                change_all_vs_central=(h_all / c_all - 1) if c_all and not pd.isna(h_all) else np.nan,
                arm=arm, frame=frame, central_frame=central_frame or frame, central_h_nhw=c_nhw, central_h_all=c_all,
                note=note)


def main() -> None:
    rows = []
    # ---- Arm 1, NIBRS offenders: imputation methods and the arrestee validation
    imp = pd.read_csv(OUT / "nibrs_imputation_specs.csv")
    cen = imp[imp.method.str.startswith("central")].set_index("offence")
    gate("NIBRS central replicates the lane (murder 2.303, robbery 4.219)",
         abs(cen.loc["Murder", "RR_H_NHW"] - 2.3034) < 1e-3 and abs(cen.loc["Robbery", "RR_H_NHW"] - 4.2193) < 1e-3,
         f"{cen.loc['Murder', 'RR_H_NHW']:.4f}, {cen.loc['Robbery', 'RR_H_NHW']:.4f}")
    C = lambda o: (cen.loc[o, "RR_H_NHW"], cen.loc[o, "RR_H_all"])  # noqa: E731
    for x in imp.itertuples():
        rows.append(row(x.offence, x.method, "1 imputation of unknown offenders", NIBRS_FRAME, x.RR_H_NHW, x.RR_H_all,
                        *C(x.offence)))
    val = pd.read_csv(OUT / "nibrs_validation_adjusted.csv")
    for x in val[~val.method.eq("central")].itertuples():
        rows.append(row(x.offence, x.method, "1 arrestee validation of the imputation", NIBRS_FRAME, x.RR_H_NHW,
                        x.RR_H_all, *C(x.offence), "offenders recorded without ethnicity get the Hispanic share their "
                        "booked arrestees show (small sample; booking under-records Hispanic)"))
    # ---- Arm 1, SHR national homicide
    shr = pd.read_csv(OUT / "shr_imputation_specs.csv")
    for w, g in shr.groupby(shr.window.astype(str), sort=False):
        lane = g[g.method.str.startswith("victim lane")].iloc[0]
        for x in g.itertuples():
            rows.append(row("Murder", f"{w}: {x.method}", "1 imputation of unknown offenders (SHR national)",
                            f"SHR national {w}, WONDER deaths (victim-cost lane design)", x.RR_H_NHW, x.RR_H_all,
                            lane.RR_H_NHW, lane.RR_H_all))
    # ---- Arm 2, NCVS perceived offender (cross-frame: compared with the NIBRS central)
    nc = pd.read_csv(OUT / "ncvs_offender_ratios.csv")
    for x in nc.itertuples():
        c = C(x.offence) if x.offence in cen.index else (np.nan, np.nan)
        rows.append(row(x.offence, f"NCVS {x.years} {x.region}, allocation {x.allocation}", "2 NCVS perceived offender",
                        "NCVS Select victimizations, perceived offender; groups with any Hispanic offender coded Hispanic",
                        x.RR_H_NHW, x.RR_H_all, *c, f"SE H/NHW {x.se_RR_H_NHW:.3f}; different construct and geography",
                        central_frame=NIBRS_FRAME))
    # ---- Arm 2, the multiple-offender rule (all violent, 2022-2024, known offenders only)
    u = pd.read_csv(OUT / "ncvs_victimizations_per_incident.csv")
    u = u[u.year.astype(str).eq("2022-2024") & u.victim.isin(["White", "Black", "Hispanic", "Other"])]
    lane_r = u[u.offender.eq("all (row)")].set_index("victim").victimizations_per_incident
    cells = u[~u.offender.eq("all (row)")].pivot_table(index="victim", columns="offender",
                                                        values=["published_incidents", "select_victimizations"])
    pop = ns.fetch_population()
    pop = pop[pop.year.between(2022, 2024)].groupby("g").w.sum()
    theta_n = float(pd.read_csv(OUT / "nibrs_mixed_group_hispanic_fraction.csv").query("offence == 'All five'")
                    .mean_hispanic_fraction.iloc[0])
    known = ["White", "Black", "Hispanic", "Other"]
    lane_v = cells["published_incidents"][known].mul(lane_r, axis=0)            # the victim lane's victimizations
    sel_v = cells["select_victimizations"][known]
    rule = {}
    excess = sel_v["Hispanic"] - lane_v["Hispanic"]
    matched = pd.concat([excess, lane_v["Other"] - sel_v["Other"]], axis=1).min(axis=1).clip(lower=0)
    for lab, th, mv in [("NCVS table 13 rule: Hispanic only if every offender Hispanic (victim-cost lane)", 0.0, excess),
                        (f"mixed groups attributed Hispanic at the NIBRS mean fraction {theta_n:.3f}", theta_n, excess),
                        (f"NIBRS mean fraction {theta_n:.3f}, only the excess matched by the Other deficit", theta_n,
                         matched),
                        ("Select coding: groups with any Hispanic offender counted Hispanic", 1.0, excess)]:
        v = lane_v.copy()
        extra = th * mv
        v["Hispanic"] += extra
        v["Other"] -= extra
        tot = v.to_numpy().sum()
        h_nhw = (v["Hispanic"].sum() / pop["H"]) / (v["White"].sum() / pop["NHW"])
        h_all = (v["Hispanic"].sum() / pop["H"]) / (tot / pop.sum())
        rule[lab] = (h_nhw, h_all)
    c0 = list(rule.values())[0]
    for lab, (a, b) in rule.items():
        rows.append(row("All violent", lab, "2 multiple-offender rule", "NCVS 2022-24 national, known offenders, "
                        "victimizations", a, b, *c0, "the victim-cost lane's non-fatal count sits on the first row"))
    # ---- Arm 3, reporting to police: police-recorded -> all crimes (NCVS 2012-2024 and 2022-2024)
    rep = pd.read_csv(OUT / "ncvs_reporting.csv")
    pv = pd.read_csv(OUT / "ncvs_police_visible_factors.csv")
    for yrs in ["2012-2024", "2022-2024"]:
        r = rep[rep.years.eq(yrs) & rep.dimension.eq("offender")].set_index(["offence", "group"]).pct_reported
        f = pv[pv.years.eq(yrs) & pv.victim.eq("all") & pv.stat.eq("factor")].set_index("offence").estimate
        for o in ["Robbery", "Aggravated assault", "Rape/sexual assault", "Simple assault"]:
            adj_nhw = r[(o, "NHW")] / r[(o, "H")]
            rows.append(row(o, f"reporting-weighted to all crimes, NCVS {yrs} (x {adj_nhw:.3f} H/NHW, / {f[o]:.3f} H/all)",
                            "3 reporting to police", NIBRS_FRAME, C(o)[0] * adj_nhw, C(o)[1] / f[o], *C(o),
                            f"reported: Hispanic-offender {r[(o, 'H')]:.1f}%, NH-white-offender {r[(o, 'NHW')]:.1f}%"))
    rows.append(row("Murder", "reporting to police: not applicable", "3 reporting to police", NIBRS_FRAME, *C("Murder"),
                    *C("Murder"), "[INFERENCE] homicides reach police records without victim reporting"))
    # ---- Arm 5, White subtraction: absent in the NIBRS offender frame; measured on arrestees
    for o in cen.index:
        rows.append(row(o, "White-subtraction: not present (disjoint race-ethnicity classes)", "5 White subtraction",
                        NIBRS_FRAME, *C(o), *C(o)))
    a5 = pd.read_csv(OUT / "arm5_white_subtraction.csv")
    for x in a5.itertuples():
        central = x.universe.startswith("central")
        c_nhw = x.RR_H_NHW_lane_central if central else x.RR_H_NHW_known_true
        rows.append(row(x.offence, f"White-subtraction construction (route B), {x.universe}, {x.arrestees}",
                        "5 White subtraction", "NIBRS arrestees" + (" (lane arrestee central)" if central else
                                                                     " (known ethnicity, no allocation)"),
                        c_nhw * (1 + x.over_route_b), np.nan, c_nhw, np.nan,
                        f"{x.hispanic_not_white:.1%} of Hispanic arrestees not coded White"))
    # ---- booking discordance (arrestee frame; bears on arrest-keyed shares, not the offender ratios)
    bk = pd.read_csv(OUT / "nibrs_arrestee_ratios_booking.csv")
    for (age, o), g in bk.groupby(["arrestees", "offence"], sort=False):
        base = g[g.universe.str.startswith("all central")].iloc[0]
        for x in g.itertuples():
            rows.append(row(o, f"arrestees {age}: {x.universe}", "booking discordance", "NIBRS arrestees, TX+AZ",
                            x.RR_H_NHW, np.nan, base.RR_H_NHW, np.nan,
                            "dropping agencies changes composition too; see booking_factors.csv for the within-incident factor"))
    bf = pd.read_csv(OUT / "booking_factors.csv").set_index("universe").factor
    for (age, o), g in bk[bk.universe.str.startswith("all central")].groupby(["arrestees", "offence"], sort=False):
        k = {"Murder": "all ages, murder", "Robbery": "all ages, robbery",
             "Aggravated assault": "all ages, aggravated assault"}.get(o, "all ages, all five offences")
        b = g.iloc[0]
        rows.append(row(o, f"arrestees {age} x within-incident booking factor ({k}) {bf[k]:.4f}", "booking discordance",
                        "NIBRS arrestees, TX+AZ", b.RR_H_NHW * bf[k], np.nan, b.RR_H_NHW, np.nan,
                        "offender-segment / arrestee-segment Hispanic share in single pairs"))
    # ---- census undercount (PES) on per-capita ratios
    for o in cen.index:
        rows.append(row(o, "census 2020 PES coverage (Hispanic -4.99%, NH white +1.64%) if carried into denominators",
                        "counter-item: census coverage", NIBRS_FRAME, C(o)[0] * F_NHW, C(o)[1] * F_ALL, *C(o),
                        "[UNVERIFIED] carry-through into the ACS denominators; cancels in the account's dollars"))
    # ---- net bands, murder and robbery, NIBRS offender frame
    R = pd.DataFrame(rows)
    for o in ["Murder", "Robbery"]:
        band = R[R.frame.eq(NIBRS_FRAME) & R.offence.eq(o) & R.arm.str.startswith("1 ")]
        lo, hi = band.hispanic_div_nh_white.min(), band.hispanic_div_nh_white.max()
        lo_a, hi_a = band.hispanic_div_all.min(), band.hispanic_div_all.max()
        rp = R[R.offence.eq(o) & R.arm.eq("3 reporting to police") & R.method.str.contains("2012-2024|not applicable")]
        m_rep = float(rp.hispanic_div_nh_white.iloc[0] / C(o)[0])
        m_rep_a = float(rp.hispanic_div_all.iloc[0] / C(o)[1])
        c_nhw, c_all = C(o)
        net = [("NET allocation band, low (Arm 1 methods and validation)", lo, lo_a),
               ("NET allocation band, high", hi, hi_a),
               ("NET central: lane allocation x reporting (Arms 1, 3, 5)", c_nhw * m_rep, c_all * m_rep_a),
               ("NET low x reporting", lo * m_rep, lo_a * m_rep_a), ("NET high x reporting", hi * m_rep, hi_a * m_rep_a),
               ("NET central x reporting x census PES", c_nhw * m_rep * F_NHW, c_all * m_rep_a * F_ALL),
               ("NET low x reporting x census PES", lo * m_rep * F_NHW, lo_a * m_rep_a * F_ALL),
               ("NET high x reporting x census PES", hi * m_rep * F_NHW, hi_a * m_rep_a * F_ALL)]
        for lab, a, b in net:
            rows.append(row(o, lab, "net", NIBRS_FRAME, a, b, c_nhw, c_all,
                            "White subtraction contributes 0 in this frame; census factor [UNVERIFIED carry-through]"))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "ratio_adjustments.csv", index=False, float_format="%.6f", lineterminator="\n")
    say(f"wrote derived/ratio_adjustments.csv: {len(R)} rows, arms {R.arm.unique().tolist()}")
    say(R[R.arm.eq("net") | R.arm.eq("2 multiple-offender rule")][
        ["offence", "method", "hispanic_div_nh_white", "hispanic_div_all", "change_vs_central", "change_all_vs_central"]]
        .to_string(index=False, float_format=lambda z: f"{z:+.3f}" if abs(z) < 1 and z != 0 else f"{z:.3f}"))
    (OUT / "ratio_adjustments_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

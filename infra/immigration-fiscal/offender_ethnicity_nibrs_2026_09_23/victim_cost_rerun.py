"""Re-run the crime-victim cost (crime_victim_cost_2026_09_23) with police-recorded NIBRS inputs.

    uv run --no-project python3 victim_cost_rerun.py        (after nibrs_rates.py)

The victim lane's model is imported, not copied: its prices, incidence builder and run() are
used unchanged, and nothing is written into that lane. Its setup (main() without the file
writes) is replicated here, and the gate reproduces its published central ($28.92bn full,
$4.50bn tangible) and its arrest-share arm ($43.12bn) before any NIBRS input is used.

Arms, each for every NIBRS specification in derived/rates_by_spec.csv:
  offender   non-fatal Hispanic-offender victimisations = 2024 NCVS national victimisations of
             the offence x the NIBRS national Hispanic share; NCVS victim distribution kept. This
             is the victim lane's own code path for its arrest-share arm (like for like).
  offender+victims  the same, with the share of the group's victims who are other residents
             taken from NIBRS: TX/AZ victim ethnicity carried to the nation through tract
             exposure (derived/victim_exposure_transfer.csv; validated on SHR homicide), then
             (1 - P) + P (1 - m), m = 0.786 as in the victim lane.
  offender+victims(TX/AZ as observed)  the untransferred TX/AZ victim shares (most in-group).
  victim-conditional  the victim lane's homicide design for non-fatal violence: NCVS national
             victimisations split by self-reported victim ethnicity (pooled 2022-2024 N-DASH) x the
             NIBRS P(offender Hispanic | victim group) carried to the nation
             (derived/offender_given_victim_transfer.csv), raw and with the logit shift that makes
             its murder row match national SHR 2024 (the SHR-calibrated arm).
Homicide stays on the victim lane's WONDER x SHR inputs throughout (the brief: NIBRS homicide
is a check, not a replacement).
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
VL = HERE.parent / "crime_victim_cost_2026_09_23"
NONFATAL = ["Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} — {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def load_victim_lane():
    spec = importlib.util.spec_from_file_location("victim_cost", VL / "victim_cost.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)
    vc.say = lambda s="": LOG.append(f"  [victim lane] {s}")      # keep its console quiet
    return vc


def setup(vc):
    """victim_cost.main() up to the arms, without writing any file."""
    c = vc.cpi()
    mcc = vc.mccollister_tables()
    txt = vc.NCVS / "_cache/miller2021_jbca.txt"
    if not txt.exists():
        raise SystemExit(f"[BLOCKED] {txt} missing; this lane does not write into other lanes")
    m21, m21n = vc.miller_2021(txt.read_text(errors="replace"))
    ps = pd.read_csv(vc.NCVS / "derived/miller2021_price_set.csv").set_index("ncvs_offence")
    f17 = c[2024] / c[2017]
    k_central = (m21["assault"]["total"] * f17 / ps.loc["Simple assault", "total_2024"]
                 - m21n["simple"] / m21n["assault"]) / (m21n["aggravated"] / m21n["assault"])
    P = {lab: vc.price_sets(c, mcc, m21, m21n, k)[0] for lab, k in [("k_central", k_central), ("k_floor", 1.93)]}
    nc = vc.ncvs_inputs()
    nc["arrest_based"] = vc.arrest_share_incidence()
    tp = pd.read_csv(vc.HERE / "derived/target_population_cps2025.csv").set_index("group")
    s_pop = {"cps_share": tp.loc["union", "age_12_plus"] / tp.loc["cps_hispanic_civilian", "age_12_plus"],
             "rate_x_target": tp.loc["union", "age_12_plus"] / nc["pop_h_2024"]}
    ex = pd.read_csv(vc.HERE / "derived/mexican_share_of_hispanic_exposure.csv").set_index("level").m
    m_geo = {"tract": ex["tract"], "county": ex["county"], "national": ex["national"], "none": 1.0}
    p = pd.read_csv(vc.HERE / "derived/shr_p_offender_given_victim.csv").set_index(["window", "victim"])
    w = pd.read_csv(vc.HERE / "derived/wonder_2024_homicide_victims.csv").set_index("group")
    joint = pd.read_csv(vc.HOM / "derived/c1b_matrix_joint_impute.csv").set_index("off_eth").loc["hispanic"].to_dict()
    hom = dict(p=p, wonder=w.deaths_not_stated_allocated.to_dict(), joint=joint)
    base = dict(price="miller2021", unknown="proportional", victimisations=True, ratio=1.0,
                pop_basis="cps_share", m="tract", ncvs_year="pooled", mix="victim_group",
                hom_window="2024", hom_scope="all", hom_dist="victim_conditional", k="k_central",
                nonfatal_source="ncvs")
    return dict(P=P, nc=nc, s_pop=s_pop, m_geo=m_geo, hom=hom, base=base)


def run(vc, S, nonfatal_totals=None, outside_share=None, **kw):
    o = {**S["base"], **kw}
    nc = dict(S["nc"])
    if nonfatal_totals is not None:
        nc["arrest_based"] = nonfatal_totals
        o["nonfatal_source"] = "arrests_2019"            # the lane's generic rescale-by-offence path
    r = vc.run(o, S["P"][o["k"]], nc, S["hom"], S["s_pop"], S["m_geo"])
    d = r["detail"]
    if outside_share is not None:
        nf = d.block.eq("nonfatal_violence")
        g = d[nf].groupby("offence")[["group_victimisations"]].sum()
        g["outside_victims"] = [g.loc[x, "group_victimisations"] * outside_share[x] for x in g.index]
        unit = d[nf].groupby("offence")[["unit_tangible", "unit_full"]].first()
        g = g.join(unit)
        h = d[~nf]
        tang = float((g.outside_victims * g.unit_tangible).sum() + h.cost_tangible.sum())
        full = float((g.outside_victims * g.unit_full).sum() + h.cost_full.sum())
        return dict(tangible=tang, full=full, murder_full=float(h.cost_full.sum()),
                    outside_nonfatal=float(g.outside_victims.sum()), group_nonfatal=float(g.group_victimisations.sum()),
                    detail_nf=g.assign(cost_tangible=g.outside_victims * g.unit_tangible,
                                       cost_full=g.outside_victims * g.unit_full))
    nf = d.block.eq("nonfatal_violence")
    g = d[nf].groupby("offence")[["hispanic_victimisations", "group_victimisations", "outside_victims",
                                  "cost_tangible", "cost_full"]].sum()
    return dict(tangible=r["tangible"], full=r["full"], murder_full=float(d.loc[~nf, "cost_full"].sum()),
                outside_nonfatal=r["outside_nonfatal"], group_nonfatal=r["group_nonfatal"], detail_nf=g)


def main() -> None:
    vc = load_victim_lane()
    S = setup(vc)
    held = pd.read_csv(VL / "derived/arms.csv").set_index("arm")
    cen = run(vc, S)
    arr = run(vc, S, nonfatal_source="arrests_2019")
    gate("victim lane central reproduced ($28.92bn full, $4.50bn tangible)",
         abs(cen["full"] / 1e9 - held.loc["central", "full_bn"]) < 1e-3
         and abs(cen["tangible"] / 1e9 - held.loc["central", "tangible_bn"]) < 1e-3,
         f"full ${cen['full'] / 1e9:.4f}bn (held {held.loc['central', 'full_bn']:.4f}), "
         f"tangible ${cen['tangible'] / 1e9:.4f}bn (held {held.loc['central', 'tangible_bn']:.4f})")
    arm = "non-fatal offender ethnicity from 2019 adult arrest shares, not NCVS perception"
    gate("victim lane arrest-share arm reproduced ($43.12bn)",
         abs(arr["full"] / 1e9 - held.loc[arm, "full_bn"]) < 1e-3, f"${arr['full'] / 1e9:.4f}bn")
    N = S["nc"]["arrest_based"]
    n2024 = {o: vc.cv2024_number("cv24t01.csv", lab) for o, lab in
             [("Rape/sexual assault", "Rape/sexual assault/c"), ("Robbery", "Robbery"),
              ("Aggravated assault", "Aggravated assault"), ("Simple assault", "Simple assault")]}
    ncvs_share = (cen["detail_nf"].hispanic_victimisations / pd.Series(n2024)).to_dict()
    arrest_share = {o: N[o] / n2024[o] for o in NONFATAL}
    say("Hispanic share of 2024 national victimisations implied by each source:")
    for o in NONFATAL:
        say(f"  {o:<22} NCVS perception {ncvs_share[o]:.3f}   2019 arrests {arrest_share[o]:.3f}")

    R = pd.read_csv(OUT / "rates_by_spec.csv")
    ex = pd.read_csv(OUT / "victim_exposure_transfer.csv")
    ex = ex[ex.offenders.eq("H")].set_index("offence")
    m = S["m_geo"]["tract"]
    out_nat = {o: (1 - ex.loc[o, "p_victim_hispanic_national"]) + ex.loc[o, "p_victim_hispanic_national"] * (1 - m)
               for o in NONFATAL}
    out_obs = {o: (1 - ex.loc[o, "p_victim_hispanic_txaz"]) + ex.loc[o, "p_victim_hispanic_txaz"] * (1 - m)
               for o in NONFATAL}
    ncvs_out = (cen["detail_nf"].outside_victims / cen["detail_nf"].group_victimisations).to_dict()
    say("Share of the group's non-fatal victims who are other residents: " + ", ".join(
        f"{o} NCVS {ncvs_out[o]:.3f} / NIBRS national {out_nat[o]:.3f} / TX-AZ {out_obs[o]:.3f}" for o in NONFATAL))
    pd.DataFrame({"ncvs_victim_lane": ncvs_out, "nibrs_transferred_national": out_nat, "nibrs_txaz_observed": out_obs}) \
        .to_csv(OUT / "outside_share_by_offence.csv", float_format="%.4f")

    # arrest-calibrated translation (upper arm): scale S by FBI 2023 national arrest share over the
    # TX/AZ arrestee translation (derived/translation_check_arrests_vs_table43c.csv)
    tc = pd.read_csv(OUT / "translation_check_arrests_vs_table43c.csv").set_index("offence")
    calib = (tc.fbi_2023_table43c_share / tc.national_share_H).to_dict()

    rows, byoff = [], []
    specs = list(dict.fromkeys(R.spec))
    for sp in specs:
        r = R[R.spec.eq(sp)].set_index("offence")
        share = {o: float(r.loc[o, "national_share_H"]) for o in NONFATAL}
        variants = [("offender", share, None), ("offender+victims", share, out_nat)]
        if sp == "central":
            variants += [("offender+victims (TX/AZ as observed)", share, out_obs),
                         ("offender, arrest-calibrated translation", {o: share[o] * calib[o] for o in NONFATAL}, None),
                         ("offender+victims, arrest-calibrated translation",
                          {o: share[o] * calib[o] for o in NONFATAL}, out_nat)]
        for lab, sh, osh in variants:
            res = run(vc, S, nonfatal_totals={o: n2024[o] * sh[o] for o in NONFATAL}, outside_share=osh)
            rows.append(dict(spec=sp, arm=lab, tangible_bn=res["tangible"] / 1e9, full_bn=res["full"] / 1e9,
                             murder_full_bn=res["murder_full"] / 1e9, outside_nonfatal_victims=res["outside_nonfatal"],
                             group_nonfatal_victimisations=res["group_nonfatal"],
                             **{f"share_{o}": sh[o] for o in NONFATAL}))
            if sp == "central":
                byoff.append(res["detail_nf"].assign(arm=lab).reset_index())
    # Victim-conditional arms (the victim lane's homicide design applied to non-fatal violence):
    # NCVS 2024 victimisations by victim group (self-reported ethnicity; pooled 2022-2024 N-DASH
    # shares x CV2024 table 1 totals) x NIBRS P(offender Hispanic | victim group) carried to the
    # nation (derived/offender_given_victim_transfer.csv), uncalibrated and SHR-calibrated.
    nd = pd.read_csv(vc.NCVS / "derived/ndash_rate_by_victim_race.csv")
    nd = nd[nd.year.between(2022, 2024) & nd.crimeType.isin(NONFATAL)]
    vg = nd.pivot_table(index="crimeType", columns="victim_race", values="count", aggfunc="sum")
    vshare_h = (vg["Hispanic"] / vg.sum(axis=1)).to_dict()
    ogv = pd.read_csv(OUT / "offender_given_victim_transfer.csv")

    def vc_inputs(g: pd.DataFrame, col: str, m_: float) -> tuple[dict, dict]:
        """Group victimisations V_H P_H + V_NH P_NH, and the share V_NH P_NH + V_H P_H (1 - m)
        of them whose victims are other residents."""
        tot, osh = {}, {}
        for o in NONFATAL:
            vh, vnh = n2024[o] * vshare_h[o], n2024[o] * (1 - vshare_h[o])
            ph, pnh = float(g.loc[(o, "H"), col]), float(g.loc[(o, "NH"), col])
            tot[o] = vh * ph + vnh * pnh
            osh[o] = (vnh * pnh + vh * ph * (1 - m_)) / tot[o]
        return tot, osh

    vc_central = {}
    for sp in list(dict.fromkeys(ogv.spec)):
        g = ogv[ogv.spec.eq(sp)].set_index(["offence", "victims"])
        variants = [("victim-conditional", "p_off_hispanic_national"),
                    ("victim-conditional, SHR-calibrated", "p_off_hispanic_national_shr_calibrated")]
        if sp == "central":
            variants.append(("victim-conditional, SHR 2022-2024-calibrated", "p_off_hispanic_national_shr2224_calibrated"))
        for lab, col in variants:
            tot, osh = vc_inputs(g, col, m)
            sh = {o: tot[o] / n2024[o] for o in NONFATAL}
            res = run(vc, S, nonfatal_totals=tot, outside_share=osh)
            rows.append(dict(spec=sp, arm=lab, tangible_bn=res["tangible"] / 1e9, full_bn=res["full"] / 1e9,
                             murder_full_bn=res["murder_full"] / 1e9, outside_nonfatal_victims=res["outside_nonfatal"],
                             group_nonfatal_victimisations=res["group_nonfatal"],
                             **{f"share_{o}": sh[o] for o in NONFATAL}))
            if sp == "central":
                byoff.append(res["detail_nf"].assign(arm=lab).reset_index())
                vc_central[f"{lab} (central)"] = ({o: float(g.loc[(o, "H"), col]) for o in NONFATAL},
                                                  {o: float(g.loc[(o, "NH"), col]) for o in NONFATAL})
    # price and structure sensitivities on the three central NIBRS arms
    ir = vc.institutional_ratio()
    gc = ogv[ogv.spec.eq("central")].set_index(["offence", "victims"])
    r = R[R.spec.eq("central")].set_index("offence")
    share = {o: float(r.loc[o, "national_share_H"]) for o in NONFATAL}
    p_vh = ex.p_victim_hispanic_national
    for kw_lab, kw in [("prices: McCollister 2010, risk of homicide removed", dict(price="mccollister2010")),
                       ("prices: Miller + DOT 2024 VSL for murder", dict(price="miller2021_dot_vsl")),
                       ("Hispanic victims all in-group (non-Hispanic victims only)", dict(m="none")),
                       (f"scaling: ACS institutional ratio {ir['ratio_generic_reallocated']:.3f}",
                        dict(ratio=ir["ratio_generic_reallocated"])),
                       (f"scaling: ACS institutional ratio {ir['ratio_generic_kept']:.3f}",
                        dict(ratio=ir["ratio_generic_kept"]))]:
        m_kw = S["m_geo"][kw.get("m", S["base"]["m"])]
        nibrs_tot = {o: n2024[o] * share[o] for o in NONFATAL}
        for lab, tot, osh in [("offender", nibrs_tot, None),
                              ("offender+victims", nibrs_tot, {o: (1 - p_vh[o]) + p_vh[o] * (1 - m_kw) for o in NONFATAL}),
                              ("victim-conditional, SHR-calibrated",
                               *vc_inputs(gc, "p_off_hispanic_national_shr_calibrated", m_kw))]:
            res = run(vc, S, nonfatal_totals=tot, outside_share=osh, **kw)
            rows.append(dict(spec=f"central; {kw_lab}", arm=lab, tangible_bn=res["tangible"] / 1e9,
                             full_bn=res["full"] / 1e9, murder_full_bn=res["murder_full"] / 1e9,
                             outside_nonfatal_victims=res["outside_nonfatal"],
                             group_nonfatal_victimisations=res["group_nonfatal"],
                             **{f"share_{o}": tot[o] / n2024[o] for o in NONFATAL}))
    # Consistency with NCVS's self-reported victim ethnicity: what each arm implies nationally for
    # P(offender Hispanic | victim group), against SHR 2024 homicide (0.719 / 0.069). The
    # victim-conditional arms hold these at their NIBRS inputs and imply the offending share instead.
    dd = vc.run(S["base"], S["P"]["k_central"], S["nc"], S["hom"], S["s_pop"], S["m_geo"])["detail"]
    dd = dd[dd.block.eq("nonfatal_violence")]
    cen_share = {o: float(R[R.spec.eq("central")].set_index("offence").loc[o, "national_share_H"]) for o in NONFATAL}
    diag = []
    for o in NONFATAL:
        vh, vnh = n2024[o] * vshare_h[o], n2024[o] * (1 - vshare_h[o])
        do = dd[dd.offence.eq(o)]
        p_ncvs = float(do.loc[do.victim.eq("Hispanic"), "hispanic_victimisations"].sum() / do.hispanic_victimisations.sum())
        for lab, S_o, pvh in [("NCVS perception (victim lane)", ncvs_share[o], p_ncvs),
                              ("offender (NIBRS share, NCVS victim pattern)", cen_share[o], p_ncvs),
                              ("offender+victims (NIBRS share and victim pattern)", cen_share[o],
                               float(ex.loc[o, "p_victim_hispanic_national"])),
                              ("2019 arrests (victim lane arm, NCVS victim pattern)", arrest_share[o], p_ncvs)]:
            diag.append(dict(offence=o, arm=lab, hispanic_offender_share=S_o, p_victim_hispanic_given_offender_h=pvh,
                             implied_p_off_h_given_victim_h=S_o * pvh * n2024[o] / vh,
                             implied_p_off_h_given_victim_nh=S_o * (1 - pvh) * n2024[o] / vnh,
                             ncvs_hispanic_victim_share=vshare_h[o]))
        for lab, (ph, pnh) in vc_central.items():
            S_o = vshare_h[o] * ph[o] + (1 - vshare_h[o]) * pnh[o]
            diag.append(dict(offence=o, arm=lab, hispanic_offender_share=S_o,
                             p_victim_hispanic_given_offender_h=vshare_h[o] * ph[o] / S_o,
                             implied_p_off_h_given_victim_h=ph[o], implied_p_off_h_given_victim_nh=pnh[o],
                             ncvs_hispanic_victim_share=vshare_h[o]))
    pd.DataFrame(diag).to_csv(OUT / "consistency_with_ncvs_victims.csv", index=False, float_format="%.4f")
    say("\n-- Implied P(offender Hispanic | victim group) under each arm (SHR national homicide: H 0.719, NH 0.069) --")
    say(pd.DataFrame(diag).to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    for lab, res in [("victim lane central (NCVS perception)", cen), ("victim lane arrest-share arm (2019 arrests)", arr)]:
        rows.insert(0, dict(spec="reference", arm=lab, tangible_bn=res["tangible"] / 1e9, full_bn=res["full"] / 1e9,
                            murder_full_bn=res["murder_full"] / 1e9, outside_nonfatal_victims=res["outside_nonfatal"],
                            group_nonfatal_victimisations=res["group_nonfatal"],
                            **{f"share_{o}": (ncvs_share if "NCVS" in lab else arrest_share)[o] for o in NONFATAL}))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / "cost_arms.csv", index=False, float_format="%.4f")
    pd.concat(byoff).to_csv(OUT / "cost_by_offence_nibrs_central.csv", index=False, float_format="%.4f")
    say("\n-- Victim cost to other residents, 2024 $bn (homicide on WONDER x SHR throughout) --")
    say(A[["spec", "arm", "tangible_bn", "full_bn", "murder_full_bn", "outside_nonfatal_victims"]]
        .to_string(index=False, float_format=lambda v: f"{v:,.2f}" if abs(v) < 1000 else f"{v:,.0f}"))
    (OUT / "cost_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

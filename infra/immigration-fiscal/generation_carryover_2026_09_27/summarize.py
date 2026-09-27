"""Assemble the four deliverable tables from the per-source outputs.

gaps_by_generation.csv  every source's gap to whites, one row per source x frame x measure x generation
carryover.csv           rho(n -> n+1) = gap(n+1) / gap(n) with SEs, plus the adopted account's $-per-adult
                        ratios read from generation_account_2026_09_24/derived/generation_results.csv
attrition_bounds.csv    G3/G4+ gaps under three attriter scenarios and a range of attrition rates
projection.csv          [MODEL] G4/G5 gaps from the G3+ gap under stated rho paths

Published NLSY97 numbers are from Duncan, Grogger, Leon & Trejo, IZA DP 12704 (Oct 2019), read in
_cache/dp12704.pdf (sha256 5e65103e...); PDF page numbers below.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
ACCOUNT = HERE.parent / "generation_account_2026_09_24/derived/generation_results.csv"
COLS = ["source", "frame", "measure", "unit", "generation", "n", "mean_age", "value", "ref_value", "gap", "se", "citation"]
CCOLS = ["source", "frame", "measure", "generation", "n", "gap_from", "gap_to", "rho", "se", "rho_p05", "rho_p95",
         "change_in_gap", "se_change", "denominator_stable", "note"]

# ---- NLSY97 published tables (value, se); white 4th+ is the reference -------------------------
T2 = "IZA DP12704 Table 2, PDF p.45"
NLSY_T2 = {  # measure: {generation: (value, se, n)}
    "educ_years": {"G1.5": (11.94, .18, 189), "G2": (13.01, .13, 378), "G3": (13.54, .23, 151), "G4plus": (12.78, .19, 274),
                   "G3plus_all": (13.02, .15, 425), "white4plus": (14.47, .06, 2436)},
    "hs_diploma": {"G1.5": (61.87, 3.52, 189), "G2": (76.95, 2.16, 378), "G3": (84.34, 2.93, 151), "G4plus": (68.14, 2.80, 274),
                   "G3plus_all": (73.42, 2.13, 425), "white4plus": (86.12, .70, 2436)},
    "some_college": {"G1.5": (28.30, 3.27, 189), "G2": (47.82, 2.57, 378), "G3": (53.46, 4.02, 151), "G4plus": (42.12, 2.97, 274),
                     "G3plus_all": (45.81, 2.40, 425), "white4plus": (65.08, .96, 2436)},
    "ba_plus": {"G1.5": (9.02, 2.08, 189), "G2": (14.16, 1.79, 378), "G3": (20.22, 3.24, 151), "G4plus": (20.81, 2.44, 274),
                "G3plus_all": (20.62, 1.95, 425), "white4plus": (39.58, .99, 2436)},
}
# Regression gaps to white 4th+ (col 1, no controls), coefficient and SE.
NLSY_REG = {
    ("log_annual_earnings", "IZA DP12704 Table 11 col (1), PDF p.55; ages 30+, not enrolled"):
        {"G1.5": (-.479, .105), "G2": (-.225, .070), "G3": (-.078, .074), "G4plus": (-.197, .084)},
    ("log_hourly_wage", "IZA DP12704 Table 10 col (1), PDF p.54; ages 30+, not enrolled"):
        {"G1.5": (-.314, .060), "G2": (-.164, .038), "G3": (-.121, .055), "G4plus": (-.156, .050)},
    ("annual_weeks_worked", "IZA DP12704 Table 9 col (1), PDF p.53; ages 30+, not enrolled"):
        {"G1.5": (-2.758, 1.716), "G2": (.067, 1.029), "G3": (-.430, 1.828), "G4plus": (-5.703, 1.548)},
    ("afqt_percentile", "IZA DP12704 Table 8 col (1), PDF p.52; sex and age at testing"):
        {"G1.5": (-31.75, 2.54), "G2": (-24.98, 1.76), "G3": (-17.72, 2.53), "G4plus": (-25.63, 1.91)},
}
# Table 5 PDF p.48: parents' mean years of schooling (mother, father) by the CHILD's generation.
NLSY_T5 = {"G1.5": ((7.02, .25), (6.89, .27)), "G2": ((8.79, .20), (8.17, .25)), "G3": ((12.56, .21), (12.34, .25)),
           "G4plus": ((12.15, .15), (12.17, .19)), "white4plus": ((13.44, .05), (13.51, .06))}
# Table 6 col (2) PDF p.49: child years on parents' years (each .28, SE .02), conditional group gaps.
NLSY_T6_BETA = (.28 + .28, math.sqrt(.02 ** 2 + .02 ** 2))
NLSY_T6_DELTA = {"G2": (1.08, .20), "G3": (-.31, .28), "G4plus": (-.87, .19)}
# Table 12 PDF p.56 (cross-sectional sample): share identified as Hispanic in 1997.
NLSY_T12 = {"G2": (94.63, 1.82, 155), "G3": (79.38, 4.58, 79)}
# Table 13 PDF p.57: 3rd generation, cross-sectional sample, by Hispanic identification.
NLSY_T13 = {"identified": {"educ_years": 13.58, "ba_plus": 23.01, "n": 65},
            "not_identified": {"educ_years": 14.22, "ba_plus": 29.17, "n": 11}}


def ratio_se(a, sa, b, sb):
    r = b / a
    return r, abs(r) * math.sqrt((sa / a) ** 2 + (sb / b) ** 2)


def gaps_table():
    rows = []
    for f, src in [("cps_gaps_CPS_ASEC_2022_2025.csv", "CPS_ASEC_2022_2025"),
                   ("cps_gaps_CPS_ASEC_2022_2026.csv", "CPS_ASEC_2022_2026_sensitivity")]:
        t = pd.read_csv(D / f)
        for r in t.itertuples():
            rows.append(dict(source=src, frame=f"{r.frame}: {r.frame_desc}", measure=r.measure, unit=r.unit, generation=r.generation,
                             n=r.n, mean_age=r.mean_age, value=r.value, ref_value=r.ref_value_age_matched, gap=r.gap, se=r.se,
                             citation=f"[CALCULATION: analyze_cps.py -> derived/{f}]"))
    t = pd.read_csv(D / "gss_gaps.csv")
    for r in t.itertuples():
        rows.append(dict(source=r.source, frame=r.frame, measure=r.measure, unit="pct" if r.measure in ("ba_plus", "less_than_hs", "employed") else "level",
                         generation=r.generation, n=r.n, mean_age=r.mean_age, value=r.value, ref_value=r.ref_value_age_matched,
                         gap=r.gap, se=r.se, citation="[CALCULATION: analyze_gss.py -> derived/gss_gaps.csv]"))
    t = pd.read_csv(D / "masp_gaps.csv")
    for r in t.itertuples():
        rows.append(dict(source=r.source, frame=r.frame, measure=r.measure, unit="pct", generation=r.generation, n=r.n,
                         mean_age=r.mean_age, value=r.value, ref_value=r.ref_value_age_matched, gap=r.gap, se=r.se,
                         citation="[CALCULATION: analyze_masp.py -> derived/masp_gaps.csv]"))
    for m, gens in NLSY_T2.items():
        w, sw, _ = gens["white4plus"]
        for g, (v, s, n) in gens.items():
            if g == "white4plus":
                continue
            rows.append(dict(source="NLSY97_published", frame="1980-84 birth cohort, age 25+ at last round (to 2015-16); ref white 4th+",
                             measure=m, unit="pct" if m != "educ_years" else "years", generation=g, n=n, mean_age=np.nan, value=v,
                             ref_value=w, gap=v - w, se=math.hypot(s, sw), citation=f"[SOURCE: {T2}]"))
    for (m, cite), gens in NLSY_REG.items():
        for g, (b, s) in gens.items():
            rows.append(dict(source="NLSY97_published", frame="regression gap to white 4th+", measure=m, unit="coef",
                             generation=g, n=np.nan, mean_age=np.nan, value=np.nan, ref_value=0.0, gap=b, se=s,
                             citation=f"[SOURCE: {cite}]"))
    (wm, swm), (wf, swf) = NLSY_T5["white4plus"]
    for g, ((m_, sm), (f_, sf)) in NLSY_T5.items():
        if g == "white4plus":
            continue
        v = (m_ + f_) / 2
        rows.append(dict(source="NLSY97_published", frame="parents of respondents (mean of mother, father)", measure="parental_educ_years",
                         unit="years", generation=f"parents_of_{g}", n=np.nan, mean_age=np.nan, value=v, ref_value=(wm + wf) / 2,
                         gap=v - (wm + wf) / 2, se=0.5 * math.sqrt(sm ** 2 + sf ** 2 + swm ** 2 + swf ** 2),
                         citation="[SOURCE: IZA DP12704 Table 5, PDF p.48]"))
    return rows


def carry_table(gaps):
    rows = []
    for f, src in [("cps_carryover_CPS_ASEC_2022_2025.csv", None), ("cps_carryover_CPS_ASEC_2022_2026.csv", "CPS_ASEC_2022_2026_sensitivity"),
                   ("gss_carryover.csv", None), ("masp_carryover.csv", None)]:
        t = pd.read_csv(D / f)
        for r in t.to_dict("records"):
            if src:
                r["source"] = src
            r.setdefault("rho_p05", np.nan)
            r.setdefault("rho_p95", np.nan)
            r["note"] = "replicate/bootstrap SE; ratio unstable when denominator_stable is False"
            rows.append({k: r.get(k) for k in CCOLS})
    g = pd.DataFrame(gaps)
    nl = g[g.source.eq("NLSY97_published")]
    for (frame, m), s in nl.groupby(["frame", "measure"]):
        by = s.set_index("generation")
        for a, b in [("G1.5", "G2"), ("G2", "G3"), ("G3", "G4plus"), ("G2", "G3plus_all"),
                     ("parents_of_G1.5", "G1.5"), ("parents_of_G2", "G2"), ("parents_of_G3", "G3"), ("parents_of_G4plus", "G4plus")]:
            if a not in by.index or b not in by.index:
                continue
            ga, sa, gb, sb = by.gap[a], by.se[a], by.gap[b], by.se[b]
            rho, se = ratio_se(ga, sa, gb, sb)
            rows.append(dict(source="NLSY97_published", frame=frame, measure=m, generation=f"{a}->{b}", n=by.n.get(b),
                             gap_from=ga, gap_to=gb, rho=rho, se=se, rho_p05=np.nan, rho_p95=np.nan, change_in_gap=gb - ga,
                             se_change=math.hypot(sa, sb), denominator_stable=abs(ga) > 2 * sa,
                             note="delta method, gaps treated as independent (shared white reference ignored)"))
    # The parental-schooling pairs live in different measure rows; build them explicitly.
    par = nl[nl.measure.eq("parental_educ_years")].set_index("generation")
    kid = nl[nl.measure.eq("educ_years")].set_index("generation")
    for g in ["G1.5", "G2", "G3", "G4plus"]:
        ga, sa = par.gap[f"parents_of_{g}"], par.se[f"parents_of_{g}"]
        gb, sb = kid.gap[g], kid.se[g]
        rho, se = ratio_se(ga, sa, gb, sb)
        rows.append(dict(source="NLSY97_published", frame="lineage: parents' schooling gap -> own schooling gap (Tables 5, 2)",
                         measure="educ_years", generation=f"parents->{g}", n=kid.n[g], gap_from=ga, gap_to=gb, rho=rho, se=se,
                         rho_p05=np.nan, rho_p95=np.nan, change_in_gap=gb - ga, se_change=math.hypot(sa, sb),
                         denominator_stable=abs(ga) > 2 * sa,
                         note="parent generation of G3 children is G2 (born ~1950-65); of G4+ children is G3+"))
    acc = pd.read_csv(ACCOUNT)
    for (conv, band), s in acc.groupby(["convention", "band_end"]):
        v = s.set_index("generation").per_adult_usd
        for a, b in [("G1", "G2"), ("G2", "G3plus")]:
            rows.append(dict(source="adopted_account_2026_09_26", frame=f"convention {conv} ({'own generation' if conv == 'a' else 'minors with parents'}), {band} end",
                             measure="net_cost_to_other_residents_per_adult_usd", generation=f"{a}->{b}", n=np.nan,
                             gap_from=-v[a], gap_to=-v[b], rho=v[b] / v[a], se=np.nan, rho_p05=np.nan, rho_p95=np.nan,
                             change_in_gap=-(v[b] - v[a]), se_change=np.nan, denominator_stable=True,
                             note="absolute net cost vs zero, no white reference; read from generation_results.csv"))
    return rows


# ---- attrition ----------------------------------------------------------------------------------
RATES = {  # share of the Mexican-descent lineage that does not identify, by generation
    "G3": [("CPS2025 children, 88.81% identify [DATA: mexican_origin_population_total_2026_09_19 arm3_dt_table8_replication.csv]", .1119),
           ("NLSY97 cross-section 79.38% [SOURCE: DP12704 Table 12 p.56]", .2062),
           ("Duncan-Trejo 1994-2006 CPS 71.8% [SOURCE: DT 2011 Table 8 via population-total lane]", .282)],
    "G4plus": [("at the measured G3 rate (CPS2025)", .1119),
               ("Duncan-Trejo 1994-2006 fourth-plus 70.8%", .292),
               ("1970 Census reinterview fourth generation 44.4% (n=27) [SOURCE: US Census 1974 Table C via DT 2011 Table 2]", .556)],
}
DELTA = {  # nonidentifier minus identifier, same measure units
    "ba_plus": [("MASP only-Anglo vs Latino mention +0.63 [DATA: masp_2026_09_20 RESULT.md]", .63),
                ("Pew US-born US-parents 25+ +2.54 [DATA: pew_outcomes_2026_09_20 outcomes.csv]", 2.54),
                ("NLSY97 G3 cross-section +6.16 (n=11) [SOURCE: DP12704 Table 13 p.57]", 6.16)],
    "educ_years": [("NLSY97 G3 cross-section +0.64 (n=11) [SOURCE: DP12704 Table 13 p.57]", .64),
                   ("Duncan-Trejo 2017 G2 adults +0.76 [SOURCE: ILR Review 71(5) Table 8 via population-total lane]", .76)],
}
# Dollar gaps: the population-total lane's convention, attriters close 72.4% (adult) or 54.3% (child) of the gap.
CLOSE = [("attriters close 54.3% of the gap (DT 2017 child +0.57y / CPS 1.049y gap) [DATA: arm5_education_selectivity.csv]", .5433),
         ("attriters close 72.4% of the gap (DT 2017 adult +0.76y / CPS 1.049y gap)", .7244)]


def attrition_table(gaps):
    g = pd.DataFrame(gaps)
    targets = [
        ("CPS_ASEC_2022_2025", "pop", "ba_plus", "G3plus_all"), ("CPS_ASEC_2022_2025", "pop", "ledger_partial_per_adult", "G3plus_all"),
        ("CPS_ASEC_2022_2025", "cores_both", "ba_plus", "G3_obs"), ("CPS_ASEC_2022_2025", "cores_both", "ba_plus", "G4plus_obs"),
        ("CPS_ASEC_2022_2025", "cores_both", "ledger_partial_per_adult", "G3_obs"),
        ("CPS_ASEC_2022_2025", "cores_both", "ledger_partial_per_adult", "G4plus_obs"),
        ("GSS_2000_2024", "white_USparents", "ba_plus", "G3_generic"), ("GSS_2000_2024", "white_USparents", "ba_plus", "G4plus_generic"),
        ("GSS_2000_2024", "white_USparents", "educ_years", "G3_generic"), ("GSS_2000_2024", "white_USparents", "educ_years", "G4plus_generic"),
        ("NLSY97_published", "white 4th+", "ba_plus", "G3"), ("NLSY97_published", "white 4th+", "ba_plus", "G4plus"),
        ("NLSY97_published", "white 4th+", "educ_years", "G3"), ("NLSY97_published", "white 4th+", "educ_years", "G4plus"),
    ]
    rows = []
    for src, frame, m, gen in targets:
        r = g[g.source.eq(src) & g.frame.str.contains(frame, regex=False) & g.measure.eq(m) & g.generation.eq(gen)]
        assert len(r) == 1, (src, frame, m, gen, len(r))
        r = r.iloc[0]
        genkey = "G3" if gen.startswith("G3") and "plus_all" not in gen else "G4plus"
        rate_sets = RATES["G3"] + RATES["G4plus"] if gen == "G3plus_all" else RATES[genkey]
        if src == "NLSY97_published" and genkey == "G3":
            # NLSY97 assigns G3 from grandparents' birthplaces, identifiers or not (Table 12): no identity loss.
            rate_sets = [("NLSY97 G3 is defined by grandparents' birthplace; nonidentifiers included", 0.0)]
        base = dict(source=src, frame=r.frame, measure=m, generation=gen, n=r.n, observed_gap=r.gap, se=r.se)
        for rname, a in rate_sets:
            rows.append({**base, "attrition_rate": a, "rate_source": rname, "scenario": "attriters_like_identifiers",
                         "delta_source": "", "lineage_gap": r.gap})
            rows.append({**base, "attrition_rate": a, "rate_source": rname, "scenario": "attriters_like_whites",
                         "delta_source": "", "lineage_gap": (1 - a) * r.gap})
            if m in DELTA:
                for dname, dv in DELTA[m]:
                    rows.append({**base, "attrition_rate": a, "rate_source": rname, "scenario": "attriters_at_measured_nonidentifier_values",
                                 "delta_source": dname, "lineage_gap": r.gap + a * dv * (1 if r.gap < 0 else -1)})
            else:
                for dname, c in CLOSE:
                    rows.append({**base, "attrition_rate": a, "rate_source": rname, "scenario": "attriters_at_measured_nonidentifier_values",
                                 "delta_source": dname, "lineage_gap": r.gap * (1 - a * c)})
    return rows


def corrected_rho(att):
    """G3 -> G4+ ratio after attrition correction, pairing G3 and G4+ rate assumptions."""
    t = pd.DataFrame(att)
    out = []
    pairs = [(0, 0), (0, 1), (1, 2)]  # (G3 rate idx, G4 rate idx): equal-low, CPS/DT, NLSY/1970
    for (src, m), s in t.groupby(["source", "measure"]):
        g3 = s[s.generation.isin(["G3_obs", "G3_generic", "G3"])]
        g4 = s[s.generation.isin(["G4plus_obs", "G4plus_generic", "G4plus"])]
        if g3.empty or g4.empty:
            continue
        for scen in g3.scenario.unique():
            for i3, i4 in pairs:
                a3, a4 = RATES["G3"][i3][1], RATES["G4plus"][i4][1]
                if src == "NLSY97_published":
                    a3 = 0.0
                for dsrc in g3[g3.scenario.eq(scen)].delta_source.unique():
                    x3 = g3[g3.scenario.eq(scen) & g3.attrition_rate.eq(a3) & g3.delta_source.eq(dsrc)]
                    x4 = g4[g4.scenario.eq(scen) & g4.attrition_rate.eq(a4) & g4.delta_source.eq(dsrc)]
                    if len(x3) != 1 or len(x4) != 1:
                        continue
                    out.append(dict(source=src, measure=m, scenario=scen, delta_source=dsrc, attrition_G3=a3, attrition_G4plus=a4,
                                    gap_G3=x3.lineage_gap.iloc[0], gap_G4plus=x4.lineage_gap.iloc[0],
                                    rho_G3_G4plus=x4.lineage_gap.iloc[0] / x3.lineage_gap.iloc[0]))
    return out


def projection(gaps, crho):
    g = pd.DataFrame(gaps)
    c = pd.DataFrame(crho)

    def pick(src, frame, m, gen):
        r = g[g.source.eq(src) & g.frame.str.startswith(frame) & g.measure.eq(m) & g.generation.eq(gen)].iloc[0]
        return r.gap, r.se

    base = {"ba_plus": pick("CPS_ASEC_2022_2025", "pop", "ba_plus", "G3plus_all"),
            "ledger_partial_per_adult": pick("CPS_ASEC_2022_2025", "pop", "ledger_partial_per_adult", "G3plus_all"),
            "educ_years": pick("NLSY97_published", "1980-84", "educ_years", "G3")}
    corr = c[c.measure.eq("ba_plus") & c.source.isin(["CPS_ASEC_2022_2025", "GSS_2000_2024", "NLSY97_published"])]
    paths = [
        ("stall: observed identifiers (G4+ = G3), rho 1.00", "measured G3->G4+ ratios in carryover.csv (CPS both-parents, GSS, NLSY, MASP)", None),
        ("attrition-corrected, central: CPS G3 rate 11.2%, DT G4+ rate 29.2%, attriters at measured nonidentifier values",
         "mean of CPS/GSS/NLSY BA rho in attrition_corrected_rho.csv (NLSY +6.16 delta); assumed constant per generation", None),
        ("intergenerational recursion, residual of the 4th+ (-0.87y)", "NLSY Table 6 col 2: beta 0.56, delta -0.87; [MODEL]", None),
        ("intergenerational recursion, residual of the 3rd (-0.31y)", "NLSY Table 6 col 2: beta 0.56, delta -0.31; [MODEL]", None),
        ("intergenerational recursion, no group residual", "beta 0.56, delta 0 (pure regression to the white mean); [MODEL]", None),
        ("resume the G2 -> G3 cross-section step, rho 0.76", "NLSY BA 19.36/25.42 = 0.76; assumed constant; [MODEL]", None),
        ("attrition worst case: identifiers stall, attriters like whites, 1970 reinterview rates (G4 55.6%, G5+ 94.4%)",
         "lineage gap = (1 - attrition) x identifier gap; steps (1-.556)/(1-.112) then (1-.944)/(1-.556); [MODEL]", None),
    ]
    rows = []
    beta = NLSY_T6_BETA[0]
    g3y = base["educ_years"][0]
    # attrition-corrected central rho: average of GSS BA and NLSY BA under (0.112, 0.292, NLSY delta)
    sel = corr[corr.scenario.eq("attriters_at_measured_nonidentifier_values") & corr.attrition_G3.eq(.1119)
               & corr.attrition_G4plus.eq(.292) & corr.delta_source.str.startswith("NLSY97 G3 cross-section +6.16")]
    rho_att = float(sel.rho_G3_G4plus.mean()) if len(sel) else np.nan
    worst = ((1 - .556) / (1 - .1119), (1 - .944) / (1 - .556))
    resume = NLSY_T2["ba_plus"]["G3"][0] - NLSY_T2["ba_plus"]["white4plus"][0]
    resume /= NLSY_T2["ba_plus"]["G2"][0] - NLSY_T2["ba_plus"]["white4plus"][0]
    for name, basis, _ in paths:
        # sequence of years gaps G3, G4, G5 and the implied per-step rhos
        if name.startswith("intergenerational"):
            delta = -.87 if "4th+" in name else (-.31 if "3rd" in name else 0.0)
            y4 = beta * g3y + delta
            y5 = beta * y4 + delta
            r4, r5 = y4 / g3y, y5 / y4
            fixed = delta / (1 - beta)
        elif name.startswith("stall"):
            r4 = r5 = 1.0
            fixed = np.nan
        elif name.startswith("attrition-corrected"):
            r4 = r5 = rho_att
            fixed = np.nan
        elif name.startswith("resume"):
            r4 = r5 = resume
            fixed = 0.0
        else:
            r4, r5 = worst
            fixed = 0.0
        for m, (gap, se) in base.items():
            rows.append(dict(source="[MODEL] projection", measure=m, generation="G3+ (measured base)", path=name, basis=basis,
                             n=np.nan, gap=gap, se=se, rho_step=np.nan, steady_state_years=fixed))
            rows.append(dict(source="[MODEL] projection", measure=m, generation="G4", path=name, basis=basis, n=np.nan,
                             gap=gap * r4, se=se * abs(r4), rho_step=r4, steady_state_years=fixed))
            rows.append(dict(source="[MODEL] projection", measure=m, generation="G5", path=name, basis=basis, n=np.nan,
                             gap=gap * r4 * r5, se=se * abs(r4 * r5), rho_step=r5, steady_state_years=fixed))
    return rows


def write(rows, name, cols=None):
    cols = cols or list(rows[0])
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    gaps = gaps_table()
    write(gaps, "gaps_by_generation.csv", COLS)
    carry = carry_table(gaps)
    write(carry, "carryover.csv", CCOLS)
    att = attrition_table(gaps)
    write(att, "attrition_bounds.csv")
    crho = corrected_rho(att)
    write(crho, "attrition_corrected_rho.csv")
    proj = projection(gaps, crho)
    write(proj, "projection.csv")
    pd.set_option("display.width", 250)
    print(pd.DataFrame(crho).round(3).to_string(index=False))
    print(pd.DataFrame(proj).round(3).to_string(index=False))


if __name__ == "__main__":
    main()

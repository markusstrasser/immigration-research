#!/usr/bin/env python3
"""Arms 3c, 4 and 5.

Arm 3c -- bound the attrition correction to the self-identified third-plus count.
  The third-plus cell is the only part of the 40.97M union that depends on
  self-identification; G1 is birthplace and G2 is parental birthplace, both
  objective.  The observed third-plus splits into third-generation identifiers and
  fourth-plus identifiers; the CPS measures the first group's attrition directly and
  cannot see the second group's at all, because a fourth-generation person of Mexican
  descent whose parents both stopped identifying leaves no trace in the file.
  Three assumptions on the fourth-plus identification rate are carried.

Arm 4 -- coverage.  The CPS ASEC is post-stratified to independent population
  controls, so the 17-19% Hispanic survey undercoverage is already removed by the
  weighting; what remains is error in the controls themselves.
  [SOURCE: CPS March 2025 technical documentation, "Estimation Procedure" p. 4 and
   "Undercoverage" p. 7, Table 3 Hispanic coverage ratios 0.81 male / 0.83 female]

Arm 5 -- fiscal implication, using the all-age ledger's per-person and aggregate
  gaps against third-plus non-Hispanic whites (read-only).

Inputs : _cache/cps_asec2025_person_subset.parquet
         ../all_age_ledger_2026_09_17/derived/estimates.csv   (read-only)
         derived/arm1_counts_cps.csv, derived/arm3_multiplier.csv
Outputs: derived/arm3_correction_bounds.csv
         derived/arm3_fractional_counting.csv
         derived/arm4_coverage_grid.csv
         derived/arm5_fiscal_implication.csv
         derived/arm5_education_selectivity.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
LEDGER = HERE.parent / "all_age_ledger_2026_09_17" / "derived" / "estimates.csv"

MEXICO = 303
US_AREA = (57, 60, 66, 69, 73, 78)
REP_N = 160
W0 = "pwwgt0"
REPS = [f"pwwgt{i}" for i in range(1, REP_N + 1)]

# A_HGA -> completed years of schooling, the usual CPS crosswalk.
HGA_YEARS = {0: 0, 31: 0, 32: 2.5, 33: 5.5, 34: 7.5, 35: 9, 36: 10, 37: 11,
             38: 12, 39: 12, 40: 13, 41: 14, 42: 14, 43: 16, 44: 18, 45: 19, 46: 21}

# PEINUSYR band -> midpoint year of entry.  [SOURCE: 2025 ASEC data dictionary p. 6C-5]
PEINUSYR_MID = {1: 1945, 2: 1955, 3: 1962, 4: 1967, 5: 1972, 6: 1977, 7: 1980.5,
                8: 1982.5, 9: 1984.5, 10: 1986.5, 11: 1988.5, 12: 1990.5, 13: 1992.5,
                14: 1994.5, 15: 1996.5, 16: 1998.5, 17: 2000.5, 18: 2002.5, 19: 2004.5,
                20: 2006.5, 21: 2008.5, 22: 2010.5, 23: 2012.5, 24: 2014.5, 25: 2016.5,
                26: 2018.5, 27: 2020.5, 28: 2023}

# Duncan & Trejo 2011 Table 8 identification rates, and the 1970 Census Content
# Reinterview Study rates they reproduce as their Table 2 (US Bureau of the Census
# 1974, Table C, p. 8; n = 27 for the fourth generation, n = 18 for the fifth-plus).
DT_4TH_PLUS_ID = 0.708          # Duncan & Trejo 2011 Table 8, all 4th+ children
REINTERVIEW_4TH_ID = 0.444      # 1970 reinterview, 4th generation


def sdr_se(full: float, reps: np.ndarray) -> float:
    return float(np.sqrt(4.0 / REP_N * np.sum((reps - full) ** 2)))


def wtot(d: pd.DataFrame, mask: np.ndarray) -> tuple[float, float]:
    sub = d.loc[mask]
    full = float(sub[W0].sum())
    return full, sdr_se(full, sub[REPS].sum().to_numpy(dtype=float))


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    d = pd.read_parquet(CACHE / "cps_asec2025_person_subset.parquet")
    n = len(d)

    native = d["PRCITSHP"].isin([1, 2, 3]).to_numpy()
    fb = d["PRCITSHP"].isin([4, 5]).to_numpy()
    mex_born = (d["PENATVTY"] == MEXICO).to_numpy()
    mom_mex = (d["PEMNTVTY"] == MEXICO).to_numpy()
    dad_mex = (d["PEFNTVTY"] == MEXICO).to_numpy()
    mom_us = d["PEMNTVTY"].isin(US_AREA).to_numpy()
    dad_us = d["PEFNTVTY"].isin(US_AREA).to_numpy()
    hisp = (d["PEHSPNON"] == 1).to_numpy()
    mex_id = hisp & (d["PRDTHSP"] == 1).to_numpy()
    g1 = mex_born & fb
    g2 = native & (mom_mex | dad_mex)
    g3 = native & mom_us & dad_us & mex_id

    g1_t, g1_se = wtot(d, g1)
    g2_t, g2_se = wtot(d, g2)
    g3_t, g3_se = wtot(d, g3)
    union_t, union_se = wtot(d, g1 | g2 | g3)
    print(f"G1 {g1_t/1e6:.3f}M  G2 {g2_t/1e6:.3f}M  G3+ {g3_t/1e6:.3f}M  "
          f"union {union_t/1e6:.3f}M", flush=True)

    # ---------------- Arm 3c: bounds on the third-plus correction ----------------
    mult = pd.read_csv(DERIVED / "arm3_multiplier.csv")
    q = dict(zip(mult["quantity"], mult["children"]))
    A = q["A: self-identified Mexican, two US-area-born parents"]
    B_not_A = q["B not A: 3rd-generation attriters (recoverable)"]
    A_and_B = q["A and B: 3rd-generation identifiers"]
    A_not_B = q["A not B: 4th-plus identifiers (no Mexico-born grandparent)"]
    share_3rd = A_and_B / A          # of the self-ID third-plus, the exact 3rd generation
    share_4th = A_not_B / A
    p3 = A_and_B / (A_and_B + B_not_A)   # third-generation identification rate

    rows = []
    for label, p4, note in (
        ("floor: 3rd-generation attriters only, no 4th-plus correction",
         1.0, "the only piece CPS measures; a strict lower bound"),
        ("4th-plus identifies at the measured 3rd-generation rate",
         p3, "assumes identification stops decaying after the third generation"),
        ("4th-plus identifies at Duncan-Trejo 1994-2006 rate (70.8%)",
         DT_4TH_PLUS_ID, "their Table 8 4th+ row, itself censored upward"),
        ("4th-plus identifies at the 1970 reinterview 4th-generation rate (44.4%)",
         REINTERVIEW_4TH_ID, "n=27, 1970 population; an upper bound, not an estimate"),
    ):
        s3 = g3_t * share_3rd
        s4 = g3_t * share_4th
        t3 = s3 / p3
        t4 = s4 / p4
        corrected = t3 + t4
        rows.append({
            "assumption": label,
            "fourth_plus_identification_rate": round(p4, 4),
            "third_gen_identification_rate": round(p3, 4),
            "self_id_third_plus": round(g3_t, 1),
            "corrected_third_plus": round(corrected, 1),
            "added": round(corrected - g3_t, 1),
            "corrected_union": round(g1_t + g2_t + corrected, 1),
            "union_added": round(corrected - g3_t, 1),
            "note": note,
        })
        print(f"  {label:<62} third-plus {corrected/1e6:6.3f}M  "
              f"union {(g1_t+g2_t+corrected)/1e6:6.3f}M", flush=True)
    pd.DataFrame(rows).to_csv(DERIVED / "arm3_correction_bounds.csv", index=False)

    # ---- fractional (quarter-per-grandparent) counting of the third generation ----
    gp = pd.read_csv(DERIVED / "arm3_grandparent_counts.csv")
    whole = float(gp["children"].sum())
    frac = float(gp["fractional_children"].sum())
    frows = [
        {"convention": "whole persons", "third_generation_children": round(whole, 1),
         "ratio_to_whole": 1.0},
        {"convention": "fractional, one quarter per Mexico-born grandparent",
         "third_generation_children": round(frac, 1),
         "ratio_to_whole": round(frac / whole, 4)},
    ]
    # apply the same fractional ratio to the corrected third-plus counts
    ratio = frac / whole
    for r in rows:
        frows.append({
            "convention": f"fractional applied to: {r['assumption'][:48]}",
            "third_generation_children": round(r["corrected_third_plus"] * ratio, 1),
            "ratio_to_whole": round(ratio, 4)})
    pd.DataFrame(frows).to_csv(DERIVED / "arm3_fractional_counting.csv", index=False)
    print(f"\n  fractional counting ratio (quarter per Mexico-born grandparent): "
          f"{ratio:.4f}", flush=True)

    # ---------------------------- Arm 4: coverage --------------------------------
    print("\nArm 4 -- coverage", flush=True)
    # unauthorized share of the Mexico-born, from the parallel lane's CPS residual
    # [SOURCE: infra/immigration-fiscal/unauthorized_population_size_2026_09_19/
    #          derived/cps2025_residual_by_region.csv, Mexico row]
    unauth_mex = 4_567_144.0
    unauth_share = unauth_mex / g1_t

    yr = d["PEINUSYR"].map(PEINUSYR_MID).to_numpy(dtype=float)
    years_present = np.clip(2025.0 - yr, 0, None)
    ohss_rate = 0.13 * np.power(1 - 0.075, years_present)
    w = d[W0].to_numpy(dtype=float)
    ohss_mex = float(np.nansum(np.where(g1, w * ohss_rate, 0.0))) / g1_t
    cms_rate = np.where(yr >= 2021, 0.37, 0.05)
    cms_mex = float(np.nansum(np.where(g1, w * cms_rate, 0.0))) / g1_t
    print(f"  Mexico-born weighted-average coverage rates: "
          f"OHSS {ohss_mex*100:.2f}%  CMS 5/37 {cms_mex*100:.2f}%  "
          f"unauthorized share {unauth_share*100:.1f}%", flush=True)

    PES = 0.0499   # 2020 PES Hispanic net undercount [SOURCE: PES Table B, se 0.53]
    crows = []
    for label, r_native, r_legal_mex, r_unauth_mex, note in (
        ("A: controls are right (Bureau's own blended base)", 0.0, 0.0, 0.0,
         "CPS weights already remove survey undercoverage"),
        ("B: PES Hispanic 4.99% on everyone", PES, PES, PES,
         "2020 census-base error; partly absorbed by the Blended Base"),
        ("C: PES on US-born, OHSS decay on the unauthorized Mexico-born",
         PES, PES, ohss_mex / unauth_share, "OHSS rate concentrated on the unauthorized"),
        ("D: PES on US-born, CMS 5/37 on the unauthorized Mexico-born",
         PES, PES, min(cms_mex / unauth_share, 0.9), "CMS Warren et al. 2026"),
        ("E: no adjustment for natives, CMS 5/37 on the unauthorized only",
         0.0, 0.0, min(cms_mex / unauth_share, 0.9), "narrowest defensible arm"),
    ):
        legal_mex = g1_t * (1 - unauth_share)
        adj = ((g2_t + g3_t) / (1 - r_native)
               + legal_mex / (1 - r_legal_mex)
               + unauth_mex / (1 - r_unauth_mex))
        crows.append({
            "scheme": label, "rate_us_born": round(r_native, 4),
            "rate_legal_mexico_born": round(r_legal_mex, 4),
            "rate_unauthorized_mexico_born": round(r_unauth_mex, 4),
            "counted_union": round(union_t, 1),
            "coverage_adjusted_union": round(adj, 1),
            "multiplier": round(adj / union_t, 4),
            "note": note,
        })
        print(f"  {label:<58} {adj/1e6:6.3f}M  x{adj/union_t:.4f}", flush=True)
    pd.DataFrame(crows).to_csv(DERIVED / "arm4_coverage_grid.csv", index=False)

    # ------------------------- Arm 5: fiscal implication -------------------------
    print("\nArm 5 -- fiscal implication", flush=True)
    yrs = d["A_HGA"].map(HGA_YEARS).to_numpy(dtype=float)
    adult = (d["A_AGE"] >= 25).to_numpy()
    white_ref = (native & mom_us & dad_us & ~hisp
                 & (d["PRDTRACE"] == 1).to_numpy())

    def mean_years(mask: np.ndarray) -> float:
        m = mask & adult & np.isfinite(yrs)
        return float((w[m] * yrs[m]).sum() / w[m].sum())

    ed_g3 = mean_years(g3)
    ed_white = mean_years(white_ref)
    ed_gap = ed_white - ed_g3
    # Duncan & Trejo 2017 Table 8 p. 23, Mexico row: non-identifiers have +0.76 years
    # (second-generation adults) and +0.57 years of parental schooling (third-generation
    # children), conditional on controls.
    DT_EDU_ADULT, DT_EDU_CHILD = 0.76, 0.57
    erows = [
        {"quantity": "mean years of schooling, adults 25+, Mexican third-plus self-ID",
         "value": round(ed_g3, 3)},
        {"quantity": "mean years of schooling, adults 25+, third-plus NH white",
         "value": round(ed_white, 3)},
        {"quantity": "education gap to be closed", "value": round(ed_gap, 3)},
        {"quantity": "Duncan-Trejo 2017 attriter advantage, 2nd-gen adults (years)",
         "value": DT_EDU_ADULT},
        {"quantity": "Duncan-Trejo 2017 attriter advantage, 3rd-gen children (years)",
         "value": DT_EDU_CHILD},
        {"quantity": "share of the education gap closed by the adult advantage",
         "value": round(DT_EDU_ADULT / ed_gap, 4)},
        {"quantity": "share of the education gap closed by the child advantage",
         "value": round(DT_EDU_CHILD / ed_gap, 4)},
    ]
    pd.DataFrame(erows).to_csv(DERIVED / "arm5_education_selectivity.csv", index=False)
    for r in erows:
        print(f"  {r['quantity']:<62} {r['value']}", flush=True)

    led = pd.read_csv(LEDGER)
    sel = led[(led.scenario == "all_age_shared")
              & (led.reference.astype(str) == "third_plus_nh_white")
              & (led.matching == "age_band")]
    gp_pp = {t: float(sel[(sel.target == t) & (sel.metric == "gap_per_person")]
                      ["estimate"].iloc[0])
             for t in ("mexico_born", "mexican_second_gen",
                       "mexican_third_plus_selfid", "mexican_observed_total")}
    gp_tot = {t: float(sel[(sel.target == t) & (sel.metric == "gap_total")]
                       ["estimate"].iloc[0])
              for t in gp_pp}
    pop = {t: float(sel[(sel.target == t) & (sel.metric == "gap_total")]
                    ["population"].iloc[0]) for t in gp_pp}
    print(f"  ledger union population {pop['mexican_observed_total']/1e6:.3f}M, "
          f"gap per person ${gp_pp['mexican_observed_total']:,.0f}, "
          f"aggregate ${gp_tot['mexican_observed_total']/1e9:,.1f}bn", flush=True)

    g3_gap = gp_pp["mexican_third_plus_selfid"]
    frows5 = []
    for bound in rows:
        added = bound["added"]
        for aname, attr_gap in (
            ("fully converged (white balance, gap $0)", 0.0),
            (f"Duncan-Trejo selectivity ({DT_EDU_ADULT}/{round(ed_gap,2)} of the "
             f"education gap closed)", g3_gap * (1 - DT_EDU_ADULT / ed_gap)),
            ("halfway to white", g3_gap * 0.5),
        ):
            new_pop = pop["mexican_observed_total"] + added
            new_total = gp_tot["mexican_observed_total"] + added * attr_gap
            frows5.append({
                "population_assumption": bound["assumption"],
                "attriter_characteristics": aname,
                "attriters_added": round(added, 1),
                "attriter_gap_per_person": round(attr_gap, 1),
                "population_before": round(pop["mexican_observed_total"], 1),
                "population_after": round(new_pop, 1),
                "gap_per_person_before": round(gp_pp["mexican_observed_total"], 1),
                "gap_per_person_after": round(new_total / new_pop, 1),
                "aggregate_gap_bn_before": round(gp_tot["mexican_observed_total"] / 1e9, 2),
                "aggregate_gap_bn_after": round(new_total / 1e9, 2),
            })
    f5 = pd.DataFrame(frows5)
    f5.to_csv(DERIVED / "arm5_fiscal_implication.csv", index=False)
    print("\n  per-person gap and aggregate after adding attriters:", flush=True)
    for _, r in f5.iterrows():
        print(f"    {r.population_assumption[:34]:<34} | "
              f"{r.attriter_characteristics[:32]:<32} | "
              f"+{r.attriters_added/1e6:5.2f}M | "
              f"${r.gap_per_person_after:8,.0f} | "
              f"${r.aggregate_gap_bn_after:8,.1f}bn", flush=True)

    print("\nwrote derived/arm3_correction_bounds.csv, arm3_fractional_counting.csv, "
          "arm4_coverage_grid.csv, arm5_*.csv", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

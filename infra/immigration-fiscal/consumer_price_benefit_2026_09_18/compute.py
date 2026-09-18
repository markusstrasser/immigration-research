#!/usr/bin/env python3
"""Counterfactual consumer-price and native-hours benefits of Mexico-born low-skill labor.

Part A: apply the Cortes (2008) price elasticity to the removal of the Mexico-born
high-school-dropout share of the labor force, and value the resulting price rise
against native consumer-unit expenditure on the mapped immigrant-intensive services.

Part B: apply the Cortes-Tessada (2011) hours elasticity to the same removal, for
native college-educated employed women in the top quartile of the female hourly-wage
distribution.

Everything is first-order: no substitution, no re-optimization, no general equilibrium.
A total removal is FAR outside the identifying variation of either paper.
"""
from __future__ import annotations
import json, re
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"

QCOLS = ["q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest"]

# ------------------------------------------------------------------ elasticities
# Cortes 2008 states effects as "a 10 percent increase in the share ... decreases the
# price by X percent".  Her own conversion in the working paper (coef -0.043 -> 0.4%)
# shows the mapping is beta * ln(1.1), so beta = ln(1-X/100) / ln(1.1).
def beta_from_pct(pct_fall: float) -> float:
    return float(np.log(1.0 - pct_fall / 100.0) / np.log(1.1))

PRICE_ARMS = {
    # name: (beta on immigrant-intensive services, beta on the average non-traded good)
    "published_jpe_2008":   (beta_from_pct(2.0), beta_from_pct(0.2)),
    "working_paper_2005":   (beta_from_pct(1.3), beta_from_pct(0.2)),
    "half_published":       (beta_from_pct(2.0) / 2.0, beta_from_pct(0.2) / 2.0),
}

# Cortes-Tessada 2011, AEA-hosted Online Appendix Table 1, IV, Panel A "Top 25%"
# (occupations ranked by male median wage), coefficient on the log low-skilled
# immigrant share.  Units: usual hours per week.
HOURS_ARMS = {
    "hours_given_working_addl_controls": (0.980, 0.497),
    "usual_hours_addl_controls":         (0.451, 0.563),
    "half_hours_given_working":          (0.490, None),
}

# Marginal tax rate on the extra labor income.  See memo Sources.
TAX_ARMS = {
    "cbo_economywide_federal_2018": 0.27,   # 18% individual income + 9% payroll
    "high_earner_buildup":          0.35,   # ~22-24% federal + 7.65% employee FICA + ~4-5% state
    "incl_employer_payroll":        0.43,
}

# --------------------------------------------- CEX detail -> immigrant-intensive map
# (CEX Table 2500 detail line, CEX Table 1101 parent line, tier)
# tier "intensive" gets the immigrant-intensive elasticity; "nontraded" gets the
# average-non-traded-good elasticity.
MAP = [
    ("Babysitting, childcare, daycare, preschool [I]", "Personal services", "intensive"),
    ("Housekeeping services [I]", "Other household expenses", "intensive"),
    ("Gardening and lawn care service [I]", "Other household expenses", "intensive"),
    ("Household laundry and dry cleaning, sent out (nonclothing) not coin-operated [D]",
     "Other household expenses", "intensive"),
    ("Shoe repair and other shoe services [I]", "Other apparel products and services", "intensive"),
    ("Apparel laundry and dry cleaning not coin-operated [I]",
     "Other apparel products and services", "intensive"),
    ("Coin-operated apparel laundry and dry cleaning [I]",
     "Other apparel products and services", "intensive"),
    ("Alteration, repair, and tailoring of apparel and accessories [I]",
     "Other apparel products and services", "intensive"),
    ("Personal care services", "Personal care products and services", "intensive"),
    # broader non-traded services: average-non-traded elasticity
    ("Care for elderly, invalids, handicapped, etc. [I]", "Personal services", "nontraded"),
    ("Adult day care centers [I]", "Personal services", "nontraded"),
    ("Services for termite/pest control [I]", "Other household expenses", "nontraded"),
    ("Moving, storage, and freight [I]", "Other household expenses", "nontraded"),
]
# whole Table 1101 parents priced at the average-non-traded elasticity
WHOLE_PARENT_NONTRADED = ["Food away from home"]


def _norm(x: str) -> str:
    return re.sub(r"\s*\[[ID]\]\s*$", "", str(x)).strip().lower()


def first(df: pd.DataFrame, item: str) -> pd.Series:
    s = df[df.item == item]
    if s.empty:
        s = df[df.item.map(_norm) == _norm(item)]
    if s.empty:
        raise SystemExit(f"[BLOCKED] CEX line not found: {item!r}")
    return s.iloc[0]


def main() -> None:
    det = pd.read_csv(D / "cex_detail_all.csv")
    q = pd.read_csv(D / "cex_quintile_parents.csv")
    ls = pd.read_csv(D / "lowskill_share.csv")
    nat = pd.read_csv(D / "native_hh_by_quintile.csv")
    women = pd.read_csv(D / "women_top_quartile.csv")
    cexaud = json.loads((D / "cex_audit.json").read_text())

    # ---------------- treatment variable and its counterfactual change ----------------
    us = ls[ls.geo == "US"].set_index("numerator")
    LF = float(us.loc["fb_dropout", "labor_force"])
    fb_drop = float(us.loc["fb_dropout", "count"])
    mex_drop = float(us.loc["mexborn_dropout", "count"])
    s0 = fb_drop / LF
    s1_lfadj = (fb_drop - mex_drop) / (LF - mex_drop)   # removed workers leave the LF too
    s1_lffix = (fb_drop - mex_drop) / LF
    dln_lfadj = float(np.log(s1_lfadj / s0))
    dln_lffix = float(np.log(s1_lffix / s0))

    # ---------------- Part A: expenditure base ----------------
    rows, dropped = [], []
    for line, parent, tier in MAP:
        raw = first(det, line).mean_all_cu
        try:
            dv = float(raw)
        except (TypeError, ValueError):
            dropped.append(dict(line=line, published_value=str(raw)))
            continue
        pv = float(first(det, parent).mean_all_cu)
        frac = dv / pv if pv > 0 else 0.0
        pq = first(q, parent)
        rec = dict(detail_line=line, parent=parent, tier=tier,
                   detail_mean_all_cu=dv, parent_mean_all_cu=pv, within_parent_fraction=frac)
        for c in QCOLS:
            rec[c] = float(pq[c]) * frac
        rows.append(rec)
    for parent in WHOLE_PARENT_NONTRADED:
        pq = first(q, parent)
        rec = dict(detail_line=parent, parent=parent, tier="nontraded",
                   detail_mean_all_cu=float(first(det, parent).mean_all_cu),
                   parent_mean_all_cu=float(first(det, parent).mean_all_cu),
                   within_parent_fraction=1.0)
        for c in QCOLS:
            rec[c] = float(pq[c])
        rows.append(rec)
    exp = pd.DataFrame(rows)
    exp.to_csv(D / "expenditure_map.csv", index=False)

    # native consumer units per quintile
    cu = cexaud["consumer_units_thousands"]
    natshare = nat.set_index("quintile")["native_head_share"]
    ncu = {c: cu[c] * 1000.0 * float(natshare[c]) for c in QCOLS}

    # ---------------- Part A results ----------------
    outA = []
    for arm, (b_int, b_nt) in PRICE_ARMS.items():
        for shock_name, dln in (("lf_adjusted", dln_lfadj), ("lf_fixed", dln_lffix)):
            dlnP_int = b_int * dln
            dlnP_nt = b_nt * dln
            pr_int = float(np.exp(dlnP_int) - 1.0)
            pr_nt = float(np.exp(dlnP_nt) - 1.0)
            for scope, tiers in (("narrow_immigrant_intensive", ["intensive"]),
                                 ("broad_incl_other_nontraded", ["intensive", "nontraded"])):
                tot = 0.0
                byq = {}
                for c in QCOLS:
                    e_int = exp.loc[exp.tier == "intensive", c].sum()
                    e_nt = exp.loc[exp.tier == "nontraded", c].sum()
                    loss = e_int * pr_int
                    if "nontraded" in tiers:
                        loss += e_nt * pr_nt
                    v = loss * ncu[c]
                    byq[c] = v / 1e9
                    tot += v
                outA.append(dict(arm=arm, shock=shock_name, scope=scope,
                                 beta_intensive=b_int, beta_nontraded=b_nt,
                                 dln_share=dln,
                                 price_rise_intensive=pr_int, price_rise_nontraded=pr_nt,
                                 annual_loss_bn=tot / 1e9,
                                 per_mexborn_dropout_worker=tot / mex_drop,
                                 **{f"loss_bn_{c}": byq[c] for c in QCOLS}))
    A = pd.DataFrame(outA)
    A.to_csv(D / "partA_price_results.csv", index=False)

    # -------- offsetting native low-skilled wage channel (same paper) --------
    # Cortes (2008/2005 WP): a 10% increase in the low-skilled immigrant share reduces
    # the wages of low-skilled NATIVES by 0.6% (and of low-skilled immigrants by 8.0%).
    # Removing the Mexico-born low-skilled share therefore RAISES native low-skilled
    # wages by the same log-linear extrapolation.  This is a native gain that partly
    # offsets the native consumer loss above.
    base = pd.read_csv(D / "native_lowskill_base.csv").set_index("group")
    b_wage_nat = beta_from_pct(0.6)
    b_wage_imm = beta_from_pct(8.0)
    outW = []
    for shock_name, dln in (("lf_adjusted", dln_lfadj), ("lf_fixed", dln_lffix)):
        for half, tag in ((1.0, "full"), (0.5, "half")):
            dlnw = b_wage_nat * half * dln
            gain = float(base.loc["native_dropout_employed", "aggregate_earnings_bn"]) * (np.exp(dlnw) - 1.0)
            outW.append(dict(shock=shock_name, arm=tag, beta_native_wage=b_wage_nat * half,
                             wage_rise_pct=100.0 * (np.exp(dlnw) - 1.0),
                             native_dropout_workers=float(base.loc["native_dropout_employed", "workers"]),
                             native_dropout_earnings_bn=float(base.loc["native_dropout_employed", "aggregate_earnings_bn"]),
                             annual_gain_bn=gain,
                             implied_immigrant_wage_rise_pct=100.0 * (np.exp(b_wage_imm * half * dln) - 1.0)))
    W = pd.DataFrame(outW)
    W.to_csv(D / "native_lowskill_wage_offset.csv", index=False)

    # ---------------- Part B results ----------------
    w = women.set_index("group")
    outB = []
    for pop in ["topq_native_college_women", "topq_native_women"]:
        n = float(w.loc[pop, "count"])
        weeks = float(w.loc[pop, "mean_weeks"])
        wage = float(w.loc[pop, "aggregate_hourly_wage"])
        hrs_wk = float(w.loc[pop, "mean_usual_hours_week"])
        for arm, (beta, se) in HOURS_ARMS.items():
            for shock_name, dln in (("lf_adjusted", dln_lfadj), ("lf_fixed", dln_lffix)):
                d_hours_wk = beta * dln              # negative: hours fall on removal
                d_hours_yr = d_hours_wk * weeks
                agg_hours = d_hours_yr * n
                earnings = agg_hours * wage
                rec = dict(population=pop, arm=arm, beta_hours_per_logpoint=beta,
                           beta_se=se, shock=shock_name, dln_share=dln,
                           women=n, mean_weeks=weeks, mean_hours_week=hrs_wk,
                           hourly_wage=wage,
                           d_hours_week=d_hours_wk, d_hours_year=d_hours_yr,
                           pct_of_mean_hours=d_hours_wk / hrs_wk,
                           aggregate_hours_mn=agg_hours / 1e6,
                           earnings_change_bn=earnings / 1e9)
                for tname, rate in TAX_ARMS.items():
                    rec[f"tax_bn_{tname}"] = earnings * rate / 1e9
                rec["per_mexborn_dropout_worker_earnings"] = earnings / mex_drop
                rec["per_mexborn_dropout_worker_tax_35"] = earnings * 0.35 / mex_drop
                outB.append(rec)
    B = pd.DataFrame(outB)
    B.to_csv(D / "partB_hours_results.csv", index=False)

    aud = dict(
        labor_force_16plus=LF, fb_dropout=fb_drop, mexborn_dropout=mex_drop,
        share_before=s0, share_after_lf_adjusted=s1_lfadj, share_after_lf_fixed=s1_lffix,
        dln_share_lf_adjusted=dln_lfadj, dln_share_lf_fixed=dln_lffix,
        share_reduction_pct=100.0 * (1 - s1_lfadj / s0),
        native_consumer_units=ncu,
        cex_consumer_units_thousands=cu,
        narrow_expenditure_per_cu={c: float(exp.loc[exp.tier == "intensive", c].sum()) for c in QCOLS},
        nontraded_expenditure_per_cu={c: float(exp.loc[exp.tier == "nontraded", c].sum()) for c in QCOLS},
        dropped_cex_lines=dropped,
        price_arms={k: dict(beta_intensive=v[0], beta_nontraded=v[1]) for k, v in PRICE_ARMS.items()},
        hours_arms={k: dict(beta=v[0], se=v[1]) for k, v in HOURS_ARMS.items()},
        tax_arms=TAX_ARMS,
        beta_native_lowskill_wage=b_wage_nat,
        beta_immigrant_lowskill_wage=b_wage_imm,
    )
    (D / "compute_audit.json").write_text(json.dumps(aud, indent=2))
    pd.set_option("display.width", 220)
    print(json.dumps(aud, indent=2)[:1600])
    print("\n=== PART A ===")
    print(A[["arm", "shock", "scope", "price_rise_intensive", "annual_loss_bn",
             "per_mexborn_dropout_worker"]].to_string(index=False))
    print("\n=== NATIVE LOW-SKILL WAGE OFFSET ===")
    print(W.to_string(index=False))
    print("\n=== PART B ===")
    print(B[["population", "arm", "shock", "d_hours_week", "earnings_change_bn",
             "tax_bn_high_earner_buildup", "per_mexborn_dropout_worker_earnings"]].to_string(index=False))


if __name__ == "__main__":
    main()

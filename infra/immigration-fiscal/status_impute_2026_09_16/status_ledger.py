#!/usr/bin/env python3
"""Split the generation ledger's Mexico-born cell by imputed legal status.

Reuses, without copying:
  * infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py  (prepare, allocate,
    estimate, summarize, the SPM conservation checks, the 160-replicate SDR)
  * infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py
    (build(): employer payroll, sales/excise, property tax, K-12, group masks)
  * status_impute_2026_09_16/impute_status.py (Borjas 2017 residual imputation)

Outputs status_imputed_ledger.csv and status_result.txt beside this file.
"""
from __future__ import annotations

import argparse
import json
import sys
import types
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(HERE))

import analyze_cps_fiscal_2025 as base           # noqa: E402
import extend_ledger as ext                      # noqa: E402
from impute_status import impute                 # noqa: E402

EXTRA = ["A_LINENO", "A_SPOUSE", "A_CLSWKR", "PEIOOCC", "PEAFEVER", "WSAL_VAL"]
for f in EXTRA:
    if f not in base.PERSON:
        base.PERSON.append(f)

# SSA OCACT Actuarial Note 151 (Goss et al., April 2013): of 7.0M unauthorized
# workers in 2010, 3.9M were in the underground economy with no payroll record.
# 3.9/7.0 = 55.7%, rounded to 56% by the informal-channel lane
# (infra/immigration-fiscal/informal_channel_2026_09_16/RESULT.md).
OFF_BOOKS_SHARE = 3.9 / 7.0
ON_BOOKS = 1.0 - OFF_BOOKS_SHARE

NEW_GROUPS = ["mexico_born_imputed_unauthorized", "mexico_born_imputed_legal",
              "all_imputed_unauthorized"]


def sdr(v):
    v = np.asarray(v, dtype=float)
    return float(v[0]), float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def unit_totals(d, index, n_units, heads, corrected: bool, unauth: np.ndarray,
                sales_rate_unit, unit_resources, prop_rate, rent_month,
                per_pupil, q_codes):
    """Rebuild every ledger component at the person level so the corrected arm
    can zero status-ineligible items before the unit sums."""
    f = np.where(unauth, ON_BOOKS, 1.0) if corrected else np.ones(len(d))
    zero = (~unauth).astype(float) if corrected else np.ones(len(d))

    fica = d.FICA.to_numpy(float) * f
    bc = d.FEDTAX_BC.to_numpy(float) * f
    actc = d.ACTC_CRD.to_numpy(float) * f
    eitc = d.EIT_CRED.to_numpy(float) * (zero if corrected else 1.0)
    state = d.STATETAX_A.to_numpy(float) * f
    ac = bc - actc - eitc

    t = {}
    S = lambda x: np.bincount(index, weights=x, minlength=n_units)   # noqa: E731
    t["payroll"] = S(fica)
    t["federal_after_refundable"] = S(ac)
    t["federal_eitc"] = S(eitc)
    t["federal_actc"] = S(actc)
    t["state_after_credits"] = S(state)
    t["modeled_tax_total"] = t["payroll"] + t["federal_after_refundable"] + t["state_after_credits"]

    # Cash transfers: SS/SSI/veterans already route the recipient to LEGAL under
    # rule (c)/(d), so zeroing them is a no-op by construction. TANF (PAW) and
    # unemployment insurance are the live corrections: both require work
    # authorization or qualified-alien status for the ADULT.
    for k, col in base.CASH.items():
        t[k] = S(d[col].to_numpy(float) * (zero if corrected else 1.0))
    t["selected_cash_total"] = sum(t[k] for k in base.CASH)

    # Non-cash transfers are SPM-unit totals. SNAP and LIHEAP are prorated to the
    # share of unit members who are NOT imputed unauthorized (citizen children
    # and legal spouses stay eligible). WIC, school lunch and the broadband
    # subsidy are child/household programmes with no status test, kept whole.
    members = np.bincount(index, minlength=n_units).astype(float)
    eligible_members = np.bincount(index, weights=(~unauth).astype(float), minlength=n_units)
    share = np.divide(eligible_members, members, out=np.ones(n_units), where=members > 0)
    prorate = {"snap", "energy"}
    for k, col in base.NONCASH.items():
        v = heads[col].to_numpy(float)
        t[k] = v * share if (corrected and k in prorate) else v
    t["selected_noncash_total"] = sum(t[k] for k in base.NONCASH)
    t["cash_noncash_tax_balance"] = (t["modeled_tax_total"] - t["selected_cash_total"]
                                     - t["selected_noncash_total"])

    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float) * f
    t["employer_payroll"] = S(ext.OASDI_RATE * np.minimum(wage, ext.OASDI_CAP_2024)
                              + ext.HI_RATE * wage)

    for name, sh in ext.TAXABLE_SHARES.items():
        t[f"sales_tax_{name}"] = (sales_rate_unit * ext.CONSUMPTION_OF_INCOME
                                  * unit_resources * sh)
    t["sales_tax_itep"] = ext.ITEP_QUINTILE_RATES[q_codes] * unit_resources

    hhm = d.groupby("PH_SEQ").PPPOS.transform("size").to_numpy(float)
    owner = d.H_TENURE.eq(1).to_numpy()
    renter = d.H_TENURE.eq(2).to_numpy()
    t["property_tax_owner"] = S(np.where(owner, prop_rate * d.HPROP_VAL.to_numpy(float), 0.0) / hhm)
    t["property_tax_renter_proxy"] = S(np.where(renter, ext.RENTER_PASSTHROUGH * 12.0 * rent_month, 0.0) / hhm)
    t["property_tax_owner_plus_renter"] = t["property_tax_owner"] + t["property_tax_renter_proxy"]

    kids = d.A_AGE.between(5, 17).to_numpy(float)
    t["children_5_17"] = S(kids)
    t["k12_cost_at_full_attendance"] = S(kids * per_pupil)
    return t


REPORTED = ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
            "cash_noncash_tax_balance", "employer_payroll", "sales_tax_share35",
            "sales_tax_itep", "property_tax_owner", "property_tax_owner_plus_renter",
            "children_5_17", "k12_cost_at_full_attendance"]


def run():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cps-zip", type=Path, default=None)
    args = ap.parse_args()

    state = ext.build(args)
    d, index, n_units = state["d"], state["index"], state["n_units"]
    heads = d.loc[d.SPM_HEAD.eq(1)].set_index("SPM_ID").sort_index()
    params = state["params"]
    cps = state["cps"]

    with zipfile.ZipFile(cps) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"),
                         usecols=["H_SEQ", "HPUBLIC", "HLORENT"])

    prop_rate = d.GESTFIPS.map(params.property_tax_effective_rate).to_numpy(float)
    rent_month = d.GESTFIPS.map(params.median_gross_rent_monthly).to_numpy(float)
    per_pupil = d.GESTFIPS.map(params.per_pupil_current_spending).to_numpy(float)
    sales_rate = d.GESTFIPS.map(params.combined_sales_tax_rate).to_numpy(float)
    head_order = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID").index.to_numpy()
    sales_rate_unit = sales_rate[head_order]
    unit_resources = heads.SPM_RESOURCES.to_numpy(float).clip(min=0)
    unit_weight = heads.pwwgt0.to_numpy(float) * heads.SPM_NUMPER.to_numpy(float)
    q_codes = ext.weighted_quintile_codes(unit_resources, unit_weight)

    lines = []

    def out(t=""):
        print(t, flush=True)
        lines.append(t)

    # ---------------- Step 1: imputation and counts ------------------------
    arms = {
        "borjas_paper_rules": dict(use_occupation_rule=True, refugee="cuba", use_medicaid_rule=True),
        "no_occupation_rule": dict(use_occupation_rule=False, refugee="cuba", use_medicaid_rule=True),
        "wide_refugee_list": dict(use_occupation_rule=True, refugee="wide", use_medicaid_rule=True),
        "no_medicaid_rule": dict(use_occupation_rule=True, refugee="cuba", use_medicaid_rule=False),
    }
    w = d.pwwgt0.to_numpy(float)
    mex = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy()
    a18 = d.A_AGE.ge(18).to_numpy()
    a2564 = state["adults_25_64"]

    out("=" * 110)
    out("STEP 1 — Borjas (2017, NBER w22102 / Labour Economics 46) residual imputation, CPS ASEC 2025")
    out("=" * 110)
    count_rows = []
    imps = {}
    for arm, kw in arms.items():
        imp = impute(d, hh, **kw)
        imps[arm] = imp
        u = imp["unauthorized"]
        row = {"arm": arm,
               "unauth_all_ages_millions": w[u].sum() / 1e6,
               "unauth_18plus_millions": w[u & a18].sum() / 1e6,
               "unauth_25_64_millions": w[u & a2564].sum() / 1e6,
               "unauth_mexico_all_ages_millions": w[u & mex].sum() / 1e6,
               "unauth_mexico_18plus_millions": w[u & mex & a18].sum() / 1e6,
               "unauth_mexico_25_64_millions": w[u & mex & a2564].sum() / 1e6,
               "n_unweighted": int(u.sum()),
               "n_unweighted_mexico": int((u & mex).sum())}
        count_rows.append(row)
    counts = pd.DataFrame(count_rows)
    out(counts.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))

    imp = imps["borjas_paper_rules"]
    unauth = imp["unauthorized"]
    out("")
    out("-- rule hit rates among foreign-born NONCITIZENS (headline arm; rules overlap) --")
    nc = d.PRCITSHP.eq(5).to_numpy()
    for k, v in imp["rule"].items():
        if k == "b_citizen":
            continue
        out(f"   {k:32s} n={int((v & nc).sum()):6,d}  weighted={w[v & nc].sum()/1e6:7.3f}M")
    out(f"   {'-> imputed UNAUTHORIZED':32s} n={int(unauth.sum()):6,d}  weighted={w[unauth].sum()/1e6:7.3f}M")
    out(f"   {'-> imputed LEGAL noncitizen':32s} "
        f"n={int((nc & ~unauth).sum()):6,d}  weighted={w[nc & ~unauth].sum()/1e6:7.3f}M")
    out(f"   all foreign-born noncitizens      n={int(nc.sum()):6,d}  weighted={w[nc].sum()/1e6:7.3f}M")
    out(f"   all foreign-born                  n={int(imp['foreign_born'].sum()):6,d}  "
        f"weighted={w[imp['foreign_born']].sum()/1e6:7.3f}M")

    # ---------------- Step 2/3: the ledger ---------------------------------
    group = dict(state["group"])
    group["mexico_born_imputed_unauthorized"] = mex & unauth
    group["mexico_born_imputed_legal"] = mex & ~unauth
    group["all_imputed_unauthorized"] = unauth
    groups = list(ext.GROUPS) + NEW_GROUPS
    pupil = dict(ext.PUPIL_RATIO_DIFFERENTIAL)
    for g in NEW_GROUPS:
        pupil[g] = ext.PUPIL_RATIO_MEXICO_BORN_ACS

    weights = state["person_weights"]
    rows = []
    store = {}
    for arm_name, corrected in (("raw", False), ("corrected_eligibility_and_off_books", True)):
        tot = unit_totals(d, index, n_units, heads, corrected, unauth,
                          sales_rate_unit, unit_resources, prop_rate, rent_month,
                          per_pupil, q_codes)
        for allocation, eligible in state["allocations"].items():
            per = {k: base.allocate(v, index, eligible, n_units) for k, v in tot.items()}
            ext_bal = (per["cash_noncash_tax_balance"] + per["employer_payroll"]
                       + per["sales_tax_share35"] + per["property_tax_owner"])
            rep = {}
            for g in groups:
                use = a2564 & group[g]
                if use.sum() == 0:
                    continue
                ww = weights[use]
                vals = np.stack([per[m][use] for m in REPORTED] + [ext_bal[use]])
                for metric, est in zip(REPORTED + ["_extbal_pre_k12"], base.estimate(vals, ww)):
                    rep[g, metric] = est
                rep[g, "k12_charged_acs_native"] = (rep[g, "k12_cost_at_full_attendance"]
                                                    * ext.PUPIL_RATIO_NATIVE_ACS)
                rep[g, "k12_charged_differential"] = (rep[g, "k12_cost_at_full_attendance"]
                                                      * pupil[g])
                rep[g, "extended_balance_base"] = (rep[g, "_extbal_pre_k12"]
                                                   - rep[g, "k12_charged_acs_native"])
                rep[g, "extended_balance_pupil_differential"] = (rep[g, "_extbal_pre_k12"]
                                                                 - rep[g, "k12_charged_differential"])
            store[arm_name, allocation] = rep
            metrics = REPORTED + ["k12_charged_acs_native", "k12_charged_differential",
                                  "extended_balance_base", "extended_balance_pupil_differential"]
            for g in groups:
                if (g, "cash_noncash_tax_balance") not in rep:
                    continue
                use = a2564 & group[g]
                for m in metrics:
                    est, se = sdr(rep[g, m])
                    dest, dse = sdr(rep[g, m] - rep["third_plus_nh_white", m])
                    rows.append({"arm": arm_name, "allocation": allocation, "weighting": "person",
                                 "group": g, "metric": m, "n_adults_unweighted": int(use.sum()),
                                 "weighted_adults": float(weights[use, 0].sum()),
                                 "estimate": est, "se_sdr": se,
                                 "difference_from_third_plus_nh_white": dest,
                                 "se_sdr_difference": dse})

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "status_imputed_ledger.csv", index=False)

    # ---------------- Step A reproduction -----------------------------------
    r = store["raw", "equal_all_members"]
    g1, s1 = sdr(r["mexican_second_gen", "cash_noncash_tax_balance"]
                 - r["third_plus_nh_white", "cash_noncash_tax_balance"])
    g2, s2 = sdr(r["mexican_second_gen", "extended_balance_base"]
                 - r["third_plus_nh_white", "extended_balance_base"])
    out("")
    out("=" * 110)
    out("STEP A — reproduction of the published gen-ledger numbers")
    out("=" * 110)
    out(f"   Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers: "
        f"{g1:,.0f} (se {s1:,.0f})   published -6,066 (se 353)   deviation {g1 + 6066:+.2f}")
    out(f"   same, EXTENDED balance:                                             "
        f"{g2:,.0f} (se {s2:,.0f})   published -8,286 (se 443)   deviation {g2 + 8286:+.2f}")
    if abs(g1 + 6066) > 50 or abs(g2 + 8286) > 50:
        raise SystemExit(f"[BLOCKED] reproduction failed: {g1:,.0f} / {g2:,.0f}")
    out("   [reproduction check] PASS (both within $50)")

    display = [("Modeled taxes (payroll+fed+state)", "modeled_tax_total"),
               ("Selected cash transfers", "selected_cash_total"),
               ("Selected non-cash transfers", "selected_noncash_total"),
               ("= Taxes minus selected transfers", "cash_noncash_tax_balance"),
               ("+ Employer payroll tax", "employer_payroll"),
               ("+ Sales/excise tax (0.35 share)", "sales_tax_share35"),
               ("+ Property tax (owner-occupied)", "property_tax_owner"),
               ("- K-12 (ACS native pupil ratio)", "k12_charged_acs_native"),
               ("= EXTENDED BALANCE", "extended_balance_base"),
               ("= EXTENDED BAL (diff pupil ratio)", "extended_balance_pupil_differential")]
    show = ["third_plus_nh_white", "mexico_born", "mexico_born_imputed_unauthorized",
            "mexico_born_imputed_legal", "all_imputed_unauthorized", "mexican_second_gen"]

    for arm_name in ("raw", "corrected_eligibility_and_off_books"):
        for allocation in state["allocations"]:
            rep = store[arm_name, allocation]
            out("")
            out("=" * 170)
            out(f"== arm={arm_name}  allocation={allocation}  weighting=person  "
                f"adults 25-64, annual $ per adult, income year 2024 (SDR se) ==")
            out("=" * 170)
            out(f"{'row':38s}" + "".join(f"{g[:24]:>22s}" for g in show))
            for label, m in display:
                cells = "".join(f"{sdr(rep[g, m])[0]:>13,.0f} ({sdr(rep[g, m])[1]:,.0f})".rjust(22)
                                for g in show)
                out(f"{label:38s}{cells}")
            out("")
            out(f"{'difference from 3rd+ NH white':38s}" + "".join(f"{g[:24]:>22s}" for g in show))
            for label, m in display:
                cells = ""
                for g in show:
                    if g == "third_plus_nh_white":
                        cells += "—".rjust(22)
                        continue
                    e, s = sdr(rep[g, m] - rep["third_plus_nh_white", m])
                    cells += f"{e:>13,.0f} ({s:,.0f})".rjust(22)
                out(f"{label:38s}{cells}")
            out("")
            out(f"{'adults 25-64 (unweighted n / weighted M)':46s}"
                + "".join(f"{int((a2564 & group[g]).sum()):,d}/"
                          f"{weights[a2564 & group[g], 0].sum()/1e6:.2f}M".rjust(22) for g in show))

    # ---------------- decomposition of the Mexico-born gap ------------------
    out("")
    out("=" * 110)
    out("STEP 4 — how much of the Mexico-born gap the imputed-unauthorized carry")
    out("=" * 110)
    for arm_name in ("raw", "corrected_eligibility_and_off_books"):
        rep = store[arm_name, "equal_all_members"]
        for m in ("cash_noncash_tax_balance", "extended_balance_base"):
            gap_all = sdr(rep["mexico_born", m] - rep["third_plus_nh_white", m])
            gap_u = sdr(rep["mexico_born_imputed_unauthorized", m] - rep["third_plus_nh_white", m])
            gap_l = sdr(rep["mexico_born_imputed_legal", m] - rep["third_plus_nh_white", m])
            nu = weights[a2564 & group["mexico_born_imputed_unauthorized"], 0].sum()
            nl = weights[a2564 & group["mexico_born_imputed_legal"], 0].sum()
            sh = nu / (nu + nl)
            out(f"   {arm_name:36s} {m:28s} all Mexico-born {gap_all[0]:>8,.0f} ({gap_all[1]:,.0f})"
                f"   unauth {gap_u[0]:>8,.0f} ({gap_u[1]:,.0f})   legal {gap_l[0]:>8,.0f} ({gap_l[1]:,.0f})"
                f"   unauth share of adults {sh:5.1%}   unauth contribution {sh*gap_u[0]/gap_all[0]:5.1%}")

    (HERE / "status_result.txt").write_text("\n".join(lines) + "\n")
    counts.to_csv(HERE / "status_counts.csv", index=False)
    meta = {"cps_source": str(cps), "imputation": "Borjas 2017 NBER w22102 residual rules a-i",
            "off_books_share": OFF_BOOKS_SHARE,
            "corrected_arm": "EITC zeroed for imputed-unauthorized persons; federal/state/payroll "
                             "tax and ACTC scaled by the 44% on-books share; TANF, UI, SSI, SS and "
                             "veterans' receipts of the imputed-unauthorized zeroed; SNAP and LIHEAP "
                             "prorated to the non-unauthorized member share of the SPM unit; WIC, "
                             "school lunch, broadband, sales and property tax left whole"}
    (HERE / "status_manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"\nWrote {HERE/'status_imputed_ledger.csv'}")
    print(f"Wrote {HERE/'status_result.txt'}")
    print(f"Wrote {HERE/'status_counts.csv'}")


if __name__ == "__main__":
    run()

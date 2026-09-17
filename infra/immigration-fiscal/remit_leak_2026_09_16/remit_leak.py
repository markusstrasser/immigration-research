"""Remittance leakage applied to the generation ledger's sales/excise line.

Imports the gen-ledger-extension lane (which itself imports the repo's
analyze_cps_fiscal_2025 generator), rebuilds the sales/excise tax with the
domestic consumption base cut by each person's remittance outflow, and
reports the change in the extended balance by group.

No network except the CPS ASEC resolution already implemented upstream.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(HERE.parent / "build"))

import extend_ledger as ext  # noqa: E402

# --- remittance rates, share of WAGE AND SALARY income --------------------
# Mexico-born: CEMLA, Notas de Remesas 2025-3 (Feb 2025): remittances from the
# US in 2024 were 16.7% of the $373,726m US wage bill of Mexican immigrant
# workers ($62,529m). CEMLA states the residual explicitly: "los trabajadores
# mexicanos inmigrantes dedicaron el 83.3% de su ingreso laboral a erogaciones
# locales".
R_MEXICO_BORN = 0.167

# Correction 2026-09-17: the quotient above does not identify the first-gen
# sender share. Keeping it fixed is a scenario, not a measured propensity.
# It cannot establish the former $3.7bn US-born / 0.9% G2 ceiling.
# US-born second generation: this lane has not established a measured
# Mexican-origin second-generation remittance rate. Scenario assumptions:
#   participation ratio 2nd/1st ~0.31 (Hispanic, derived from Pew 51% FB vs
#   35% all-Latino 2006) to 0.47 (Asian, Pew 2024 published 15% vs 32%);
#   amount-per-sender ratio unmeasured, assumed 0.3-1.0.
R_SECOND_GEN_ARMS = {"r2_zero": 0.000, "r2_low": 0.016, "r2_central": 0.025,
                     "r2_high": 0.052}
# Third-plus self-ID Mexican: Pew 2024 Asian third+ 4% vs second-gen 15%
# => 0.27x the second-generation rate.
# That cross-origin participation transport is also an assumption, not a bound.
R_THIRD_SCALE = 0.267

TAXABLE_SHARES = ext.TAXABLE_SHARES
CONSUMPTION_OF_INCOME = ext.CONSUMPTION_OF_INCOME


def person_remit_rate(d, r2: float) -> np.ndarray:
    """Person-level remittance rate applied to wage and salary income."""
    native = d.PRCITSHP.isin([1, 2, 3])
    us_area = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    mexico_born = d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)
    mex_2g = native & parent_mexico
    mex_3p = native & parents_us & d.PRDTHSP.eq(1)
    rate = np.zeros(len(d), dtype=float)
    rate[mex_3p.to_numpy()] = r2 * R_THIRD_SCALE
    rate[mex_2g.to_numpy()] = r2
    rate[mexico_born.to_numpy()] = R_MEXICO_BORN
    return rate


def main():
    args = ext.main.__wrapped__ if False else None
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--cps-zip", type=Path, default=None)
    a = p.parse_args()

    state = ext.build(a)
    d, index, n_units = state["d"], state["index"], state["n_units"]
    totals, group = state["totals"], state["group"]
    adults, weights = state["adults_25_64"], state["person_weights"]
    heads_res = totals  # totals already carries baseline lines

    # unit-level consumption base, exactly as extend_ledger builds it
    dd = d
    head_mask = dd.SPM_HEAD.eq(1)
    heads = dd.loc[head_mask].sort_values("SPM_ID")
    unit_resources = heads.SPM_RESOURCES.to_numpy(dtype=float).clip(min=0)
    base_consumption = CONSUMPTION_OF_INCOME * unit_resources

    params = state["params"]
    sales_rate_person = dd.GESTFIPS.map(params.combined_sales_tax_rate).to_numpy(dtype=float)
    head_order = dd.loc[head_mask].sort_values("SPM_ID").index.to_numpy()
    unit_sales_rate = sales_rate_person[head_order]

    wage = dd.WSAL_VAL.clip(lower=0).to_numpy(dtype=float)

    lines = []

    def out(t=""):
        print(t)
        lines.append(t)

    # ---------- validation (a): baseline sales lines reproduce ----------
    def per_adult(vec_unit, g):
        """Unit-level dollar vector -> per-adult-25-64 estimate + SDR se,
        headline equal_all_members allocation, person weights."""
        alloc = state["allocations"]["equal_all_members"]
        share = np.bincount(index, weights=alloc.astype(float), minlength=n_units)
        share = np.where(share > 0, share, np.nan)
        per_person = np.where(alloc, vec_unit[index] / share[index], 0.0)
        mask = group[g] & adults
        num = weights[mask].T @ per_person[mask]
        den = weights[mask].sum(axis=0)
        vals = num / den
        return ext.sdr(vals)

    base_sales35 = totals["sales_tax_share35"]
    base_itep = totals["sales_tax_itep"]
    v35, s35 = per_adult(base_sales35, "third_plus_nh_white")
    vit, sit = per_adult(base_itep, "third_plus_nh_white")
    out("-- VALIDATION (a): baseline sales/excise line, third_plus_nh_white --")
    out(f"0.35 taxable-share arm: {v35:,.1f}  (gen-ledger lane published 1,050)  "
        f"deviation {v35-1050:+.1f}")
    out(f"ITEP arm:               {vit:,.1f}  (gen-ledger lane published 1,812)  "
        f"deviation {vit-1812:+.1f}")
    ok_a = abs(v35 - 1050) <= 5 and abs(vit - 1812) <= 5
    out(f"[validation a] {'PASS' if ok_a else 'FAIL'} (both within $5)")
    out()

    # ---------- the leakage model ----------
    groups = ["third_plus_nh_white", "all_native", "all_second_gen",
              "mexican_second_gen", "mexican_third_plus_selfid", "mexico_born"]
    rows = []
    for arm_name, r2 in R_SECOND_GEN_ARMS.items():
        rate_p = person_remit_rate(dd, r2)
        remit_person = rate_p * wage
        remit_unit = np.bincount(index, weights=remit_person, minlength=n_units)
        new_base = np.clip(base_consumption - remit_unit, 0.0, None)
        ratio = np.where(base_consumption > 0, new_base / np.maximum(base_consumption, 1e-9), 1.0)

        arm_sales = {}
        for nm, sh in TAXABLE_SHARES.items():
            arm_sales[nm] = unit_sales_rate * new_base * sh
        arm_sales["itep"] = base_itep * ratio

        for g in groups:
            rem_pa, rem_se = per_adult(remit_unit, g)
            row = {"arm": arm_name, "r2": r2, "group": g,
                   "remit_per_adult": rem_pa, "remit_se": rem_se}
            for nm in ["share25", "share35", "share45", "itep"]:
                bkey = f"sales_tax_{nm}" if nm != "itep" else "sales_tax_itep"
                b, _ = per_adult(totals[bkey], g)
                n, _ = per_adult(arm_sales[nm if nm != "itep" else "itep"], g)
                row[f"sales_{nm}_base"] = b
                row[f"sales_{nm}_remit"] = n
                row[f"d_sales_{nm}"] = n - b
            rows.append(row)

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "remit_leak_by_group.csv", index=False)

    out("-- Remittance outflow modelled, $ per adult 25-64 per year (2024$) --")
    sub = frame[frame.arm == "r2_central"]
    out(f"{'group':<30}{'remittance/adult':>18}{'se':>10}")
    for _, r in sub.iterrows():
        out(f"{r.group:<30}{r.remit_per_adult:>18,.0f}{r.remit_se:>10,.0f}")
    out()

    out("-- Change in the sales/excise line from the remittance haircut, $/adult --")
    hdr = f"{'arm':<12}{'group':<30}" + "".join(f"{k:>14}" for k in
                                                ["d 0.25", "d 0.35", "d 0.45", "d ITEP"])
    out(hdr)
    for _, r in frame.iterrows():
        out(f"{r.arm:<12}{r.group:<30}"
            f"{r.d_sales_share25:>14,.1f}{r.d_sales_share35:>14,.1f}"
            f"{r.d_sales_share45:>14,.1f}{r.d_sales_itep:>14,.1f}")
    out()

    # ---------- extended balance change ----------
    out("-- Extended balance with the remittance haircut, 0.35 arm and ITEP arm --")
    out("(extended balance = taxes - selected transfers + employer payroll")
    out(" + sales/excise + owner property - K-12; only the sales line moves)")
    ext_base_components = (totals["cash_noncash_tax_balance"]
                           + totals["employer_payroll"]
                           + totals["property_tax_owner"]
                           - ext.PUPIL_RATIO_NATIVE_ACS * totals["k12_cost_at_full_attendance"])
    ref = "third_plus_nh_white"
    out(f"{'arm':<12}{'group':<30}{'ext base':>12}{'ext remit':>12}{'delta':>10}"
        f"{'gap base':>12}{'gap remit':>12}{'d gap':>10}")
    bal_rows = []
    for arm_name, r2 in R_SECOND_GEN_ARMS.items():
        rate_p = person_remit_rate(dd, r2)
        remit_unit = np.bincount(index, weights=rate_p * wage, minlength=n_units)
        new_base = np.clip(base_consumption - remit_unit, 0.0, None)
        ratio = np.where(base_consumption > 0, new_base / np.maximum(base_consumption, 1e-9), 1.0)
        for salesnm, base_vec, new_vec in (
                ("0.35", totals["sales_tax_share35"],
                 unit_sales_rate * new_base * TAXABLE_SHARES["share35"]),
                ("ITEP", totals["sales_tax_itep"], totals["sales_tax_itep"] * ratio)):
            balb = ext_base_components + base_vec
            baln = ext_base_components + new_vec
            refb, _ = per_adult(balb, ref)
            refn, _ = per_adult(baln, ref)
            for g in groups:
                b, bse = per_adult(balb, g)
                n, nse = per_adult(baln, g)
                bal_rows.append(dict(arm=arm_name, sales_arm=salesnm, group=g,
                                     ext_base=b, ext_remit=n, delta=n - b,
                                     gap_base=b - refb, gap_remit=n - refn,
                                     d_gap=(n - refn) - (b - refb)))
                out(f"{arm_name+'/'+salesnm:<12}{g:<30}{b:>12,.0f}{n:>12,.0f}"
                    f"{n-b:>10,.1f}{b-refb:>12,.0f}{n-refn:>12,.0f}"
                    f"{(n-refn)-(b-refb):>10,.1f}")
    pd.DataFrame(bal_rows).to_csv(HERE / "remit_extended_balance.csv", index=False)
    out()

    # ---------- national forgone sales tax ----------
    out("-- National forgone state+local sales tax on remitted dollars --")
    REMIT_US_TO_MEX_2024_MN = 62_529.0
    pw = dd[ext.base.REPS[0]].to_numpy(dtype=float)
    nat_rate = np.average(sales_rate_person, weights=pw)
    mb = group["mexico_born"]
    mb_rate = np.average(sales_rate_person[mb], weights=pw[mb])
    out(f"population-weighted combined state+local sales rate (all persons): {nat_rate:.4%}")
    out(f"same, weighted by the Mexico-born population:                     {mb_rate:.4%}")
    for nm, sh in list(TAXABLE_SHARES.items()):
        out(f"  taxable share {sh:.2f}: national-weighted ${REMIT_US_TO_MEX_2024_MN*nat_rate*sh:,.0f}mn"
            f"   Mexico-born-weighted ${REMIT_US_TO_MEX_2024_MN*mb_rate*sh:,.0f}mn")
    out()

    (HERE / "remit_result.txt").write_text("\n".join(lines) + "\n")
    print(f"\nWrote {HERE/'remit_leak_by_group.csv'}")
    print(f"Wrote {HERE/'remit_extended_balance.csv'}")
    print(f"Wrote {HERE/'remit_result.txt'}")


if __name__ == "__main__":
    main()

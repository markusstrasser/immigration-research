"""Age profile and synthetic-cohort lifetime sum of the annual partial fiscal ledger by origin-generation.

Reuses analyze_cps_fiscal_2025.py (same CPS ASEC 2025 inputs, equal-shares-among-all-members allocation
of SPM-unit taxes and transfers) and meps_health_transport_2024.py (MEPS 2024 public-paid medical spending
by age band x US-born, and x insurance). Person-weighted means by age band and group, then a synthetic
lifetime: the band mean applied at each single age, weighted by survival from the CDC 2021 period life
table of the group's population (Hispanic tables for Mexican-origin groups, non-Hispanic white for whites,
total for all natives), undiscounted and at 3%. A mortality swap isolates the longevity effect.

Inputs: CPS zip, MEPS zip + SAS layout (as the generator), CDC life-table CSV from the derived root.
Run: uv run --with numpy --with pandas python3 lifecycle_ledger_by_generation.py --cps-zip ... --meps-zip ... --meps-sas ... --life-table ... > lifecycle_ledger_result.txt
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "build"))
from analyze_cps_fiscal_2025 import CASH, NONCASH, TAX, allocate, prepare  # noqa: E402
from meps_health_transport_2024 import donor_model, read_meps  # noqa: E402

US_AREA = [57, 60, 66, 69, 73, 78]
BANDS = [(0, 17), (18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 120)]
LIFE = {"third_plus_nh_white": "the White, non-Hispanic population", "all_native": "the total population",
        "all_second_gen": "the total population", "mexican_second_gen": "the Hispanic population",
        "mexican_third_plus_selfid": "the Hispanic population", "mexico_born": "the Hispanic population"}


def band_of(age):
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= age <= hi:
            return i
    raise ValueError(age)


def survival(lt: pd.DataFrame, group: str) -> np.ndarray:
    x = lt[lt.population_group == group].copy()
    x["age"] = pd.to_numeric(x.age_interval.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    x = x.dropna(subset=["age"]).astype({"age": int}).sort_values("age")
    lx = np.zeros(101)
    for a, l in zip(x.age, x.lx):
        if a <= 100:
            lx[a] = l
    return lx / 100000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cps-zip", type=Path, required=True)
    ap.add_argument("--meps-zip", type=Path, required=True)
    ap.add_argument("--meps-sas", type=Path, required=True)
    ap.add_argument("--life-table", type=Path, required=True)
    a = ap.parse_args()
    d, heads, index, _ = prepare(a.cps_zip)
    n_units = len(heads)
    units = d.groupby("SPM_ID", sort=True)
    totals = {k: units[v].sum().to_numpy(dtype=float) for k, v in (TAX | CASH).items()}
    totals.update({k: heads[v].to_numpy(dtype=float) for k, v in NONCASH.items()})
    eligible = np.ones(len(d), dtype=bool)  # equal shares among all members
    per = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}
    tax = per["payroll"] + per["federal_after_refundable"] + per["state_after_credits"]
    cash = sum(per[k] for k in CASH)
    noncash = sum(per[k] for k in NONCASH)
    medical, _ = read_meps(a.meps_zip, a.meps_sas)
    alive = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    health = {}
    for insured, label in ((False, "age_birth"), (True, "age_birth_insurance")):
        cells, codes, _ = donor_model(medical, d, insured)
        health[label] = cells.mean_public_paid.to_numpy()[codes] * alive
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    groups = {
        "third_plus_nh_white": native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1),
        "all_native": native,
        "all_second_gen": native & ~parents_us,
        "mexican_second_gen": native & parent_mex,
        "mexican_third_plus_selfid": native & parents_us & d.PRDTHSP.eq(1),
        "mexico_born": d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303),
    }
    w = d.MARSUPWT.to_numpy(dtype=float)
    band = d.A_AGE.map(band_of).to_numpy()
    civ = d.PRPERTYP.eq(2).to_numpy() | d.A_AGE.lt(15).to_numpy()  # civilian adults plus children
    comp = {"taxes": tax, "cash_transfers": cash, "social_security": per["social_security"], "noncash": noncash,
            "health_age_birth": health["age_birth"], "health_age_birth_ins": health["age_birth_insurance"]}
    comp["balance_after_health"] = tax - cash - noncash - health["age_birth"]
    comp["balance_after_health_ins"] = tax - cash - noncash - health["age_birth_insurance"]
    prof = {}
    print("== Annual partial ledger by age band and origin-generation, $ per person per year (person-weighted), CPS ASEC 2025 / MEPS 2024 ==")
    for g, mask in groups.items():
        m = mask.to_numpy() & civ
        print(f"\n-- {g} --")
        print(f"{'band':8s}{'n':>7s}" + "".join(f"{c[:20]:>22s}" for c in comp))
        prof[g] = np.zeros((len(BANDS), len(comp)))
        for i, (lo, hi) in enumerate(BANDS):
            sel = m & (band == i)
            ws = w[sel].sum()
            vals = [float((v[sel] * w[sel]).sum() / ws) for v in comp.values()]
            prof[g][i] = vals
            print(f"{lo:>3d}-{hi:<4d}{int(sel.sum()):>7d}" + "".join(f"{v:>22,.0f}" for v in vals))
    lt = pd.read_csv(a.life_table)
    S = {name: survival(lt, name) for name in set(LIFE.values())}
    ages = np.arange(0, 101)
    band_idx = np.array([band_of(x) for x in ages])
    ci = list(comp).index
    print("\n== Synthetic lifetime from birth: sum over ages of the band mean x survival probability (CDC 2021 period life tables) ==")
    print("   group                        mortality table              undiscounted$   PV3%$   | after-health(ins) undiscounted   PV3%  | expected years lived")
    for g in groups:
        for tab in sorted({LIFE[g], "the White, non-Hispanic population", "the Hispanic population"}):
            s = S[tab]
            bal = prof[g][band_idx, ci("balance_after_health")]
            bal_ins = prof[g][band_idx, ci("balance_after_health_ins")]
            disc = 1.03 ** (-ages)
            mark = "*" if tab == LIFE[g] else " "
            print(f" {mark} {g:26s} {tab:34s} {np.sum(bal * s):>12,.0f} {np.sum(bal * s * disc):>9,.0f}   | {np.sum(bal_ins * s):>12,.0f} {np.sum(bal_ins * s * disc):>9,.0f}  | {s.sum():5.1f}")
    print("\n   (* = the group's own table. Working-age-only and retirement-only splits:)")
    for g in groups:
        s = S[LIFE[g]]
        bal = prof[g][band_idx, ci("balance_after_health")]
        work = np.sum((bal * s)[18:65]); ret = np.sum((bal * s)[65:]); kid = np.sum((bal * s)[:18])
        print(f"   {g:26s} ages 0-17 {kid:>10,.0f}   ages 18-64 {work:>11,.0f}   ages 65+ {ret:>11,.0f}   total {kid + work + ret:>11,.0f}")


if __name__ == "__main__":
    main()

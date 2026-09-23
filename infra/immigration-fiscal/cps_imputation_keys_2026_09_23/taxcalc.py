"""Simplified 2024 federal income tax, EITC and ACTC, used only as a difference operator.

The account's tax keys are the Census tax model's FEDTAX_BC, EIT_CRED and ACTC_CRD. When the hot
deck (step 4b) changes a return's incomes, the change in each field is taken as
model(new incomes) - model(published incomes), added to the published Census value. The model is
validated against the Census fields on the published incomes (derived/taxcalc_validation.csv).

Parameters for tax year 2024 [TRAINING-DATA; IRS Rev. Proc. 2023-34, sections 3.01 (rate tables),
3.07 (EITC), 3.15 (standard deduction); CTC and ACTC amounts from 26 U.S.C. 24(h)]. Qualified
dividends and capital gains are taxed at ordinary rates here, and itemized deductions are
ignored; both errors largely cancel in the difference.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

BRACKETS = {  # upper bounds for 10, 12, 22, 24, 32, 35%; 37% above
    "single": [11600, 47150, 100525, 191950, 243725, 609350],
    "joint": [23200, 94300, 201050, 383900, 487450, 731200],
    "hoh": [16550, 63100, 100500, 191950, 243700, 609350],
}
RATES = [.10, .12, .22, .24, .32, .35, .37]
STD = {"single": 14600, "joint": 29200, "hoh": 21900}
AGED_EXTRA = {"single": 1950, "joint": 1550, "hoh": 1950}
EITC = {  # kids: (phase-in rate, earned income amount, max credit, phase-out rate, threshold single, threshold joint)
    0: (.0765, 8260, 632, .0765, 10330, 17250),
    1: (.34, 12390, 4213, .1598, 22720, 29640),
    2: (.40, 17400, 6960, .2106, 22720, 29640),
    3: (.45, 17400, 7830, .2106, 22720, 29640),
}
EITC_INVESTMENT_LIMIT = 11600
CTC, ACTC_MAX, ACTC_RATE, ACTC_FLOOR, ODC = 2000, 1700, .15, 2500, 500


def regular_tax(taxable, status):
    tax = np.zeros_like(taxable)
    lower = np.zeros_like(taxable)
    for s in ("single", "joint", "hoh"):
        m = status == s
        bounds = BRACKETS[s] + [np.inf]
        prev = 0.
        for rate, upper in zip(RATES, bounds):
            tax[m] += rate * np.clip(taxable[m] - prev, 0, upper - prev)
            prev = upper
    return tax


def compute(agi, earned, investment, status, kids17, kids19, other_dep, aged, head_age):
    """Vectorized over returns. Returns (fedtax_bc, eitc, actc)."""
    agi = np.asarray(agi, float)
    std = np.select([status == "single", status == "joint"], [STD["single"], STD["joint"]], STD["hoh"])
    extra = np.select([status == "single", status == "joint"], [AGED_EXTRA["single"], AGED_EXTRA["joint"]],
                      AGED_EXTRA["hoh"]) * aged
    taxable = np.maximum(agi - std - extra, 0)
    tax = regular_tax(taxable, status)
    threshold = np.where(status == "joint", 400000, 200000)
    reduction = 50 * np.ceil(np.maximum(agi - threshold, 0) / 1000)
    ctc_total = np.maximum(CTC * kids17 + ODC * other_dep - reduction, 0)
    ctc_child = np.minimum(ctc_total, CTC * kids17)
    nonref = np.minimum(ctc_total, tax)
    fedtax_bc = tax - nonref
    unused_child = np.maximum(ctc_child - np.minimum(ctc_child, tax), 0)
    actc = np.minimum(np.minimum(unused_child, ACTC_MAX * kids17),
                      ACTC_RATE * np.maximum(earned - ACTC_FLOOR, 0))
    k = np.minimum(kids19, 3)
    eitc = np.zeros_like(agi)
    for n, (pin, amount, mx, pout, th_s, th_j) in EITC.items():
        m = k == n
        th = np.where(status == "joint", th_j, th_s)
        phase_in = np.minimum(pin * np.maximum(earned, 0), mx)
        income = np.maximum(agi, earned)
        credit = np.maximum(phase_in - pout * np.maximum(income - th, 0), 0)
        if n == 0:
            credit = np.where((head_age >= 25) & (head_age <= 64), credit, 0)
        eitc[m] = credit[m]
    eitc = np.where(investment > EITC_INVESTMENT_LIMIT, 0, eitc)
    return fedtax_bc, eitc, np.maximum(actc, 0)


def returns(d):
    """One row per filed return (holder record: AGI != 0), with members and dependents.

    Joint returns hold two FILESTAT 1-3 members; FILESTAT 4/5 returns hold one. Dependents of the
    primary (oldest) return in a tax unit are the unit's other members.
    """
    tid = d.TAX_ID.to_numpy()
    holder = d.AGI.ne(0).to_numpy() & d.FILESTAT.isin([1, 2, 3, 4, 5]).to_numpy()
    rows = np.flatnonzero(holder)
    status = np.select([d.FILESTAT.isin([1, 2, 3]).to_numpy(), d.FILESTAT.eq(4).to_numpy()], ["joint", "hoh"], "single")
    member_of = np.full(len(d), -1)
    member_of[rows] = rows
    joint = d.FILESTAT.isin([1, 2, 3]).to_numpy()
    frame = pd.DataFrame(dict(tid=tid, pos=np.arange(len(d)), joint=joint, holder=holder, age=d.A_AGE.to_numpy()))
    spouse = frame[joint & ~holder]
    holders = frame[holder & joint].set_index("tid").pos
    member_of[spouse.pos.to_numpy()] = holders.reindex(spouse.tid).to_numpy()
    if (member_of[spouse.pos.to_numpy()] < 0).any():
        raise ValueError("Joint spouse without a holder")
    # primary return per tax unit = the oldest holder
    fr = frame[holder].sort_values(["tid", "age"], ascending=[True, False])
    primary = fr.drop_duplicates("tid").set_index("tid").pos
    is_primary = np.zeros(len(d), bool)
    is_primary[primary.to_numpy()] = True
    age = d.A_AGE.to_numpy()
    dependent = member_of < 0  # nonmembers of any return in the unit, plus dependent filers below
    dep_filer = holder & ~is_primary
    kid_pool = (dependent | dep_filer)
    prim_of_tid = primary.reindex(tid).to_numpy()
    k17 = np.bincount(np.where(kid_pool & (age < 17) & ~np.isnan(prim_of_tid), prim_of_tid, 0).astype(int),
                      weights=(kid_pool & (age < 17) & ~np.isnan(prim_of_tid)).astype(float), minlength=len(d))
    k19 = np.bincount(np.where(kid_pool & (age < 19) & ~np.isnan(prim_of_tid), prim_of_tid, 0).astype(int),
                      weights=(kid_pool & (age < 19) & ~np.isnan(prim_of_tid)).astype(float), minlength=len(d))
    other = np.bincount(np.where(kid_pool & (age >= 17) & ~np.isnan(prim_of_tid), prim_of_tid, 0).astype(int),
                        weights=(kid_pool & (age >= 17) & ~np.isnan(prim_of_tid)).astype(float), minlength=len(d))
    aged = np.bincount(np.where(member_of >= 0, member_of, 0), weights=((member_of >= 0) & (age >= 65)).astype(float),
                       minlength=len(d))
    out = pd.DataFrame(dict(row=rows, status=status[rows], kids17=k17[rows] * is_primary[rows],
                            kids19=k19[rows] * is_primary[rows], other_dep=other[rows] * is_primary[rows],
                            aged=aged[rows], head_age=age[rows]))
    return out, member_of


def member_sums(values, member_of, n):
    m = member_of >= 0
    return np.bincount(member_of[m], weights=np.asarray(values, float)[m], minlength=n)


def model_fields(d, r, member_of, earned_person, invest_person, agi=None):
    n = len(d)
    earned = member_sums(earned_person, member_of, n)[r.row]
    invest = member_sums(invest_person, member_of, n)[r.row]
    agi = d.AGI.to_numpy(float)[r.row] if agi is None else agi
    return compute(agi, earned, invest, r.status.to_numpy(), r.kids17.to_numpy(), r.kids19.to_numpy(),
                   r.other_dep.to_numpy(), r.aged.to_numpy(), r.head_age.to_numpy())


def validate(d, out_csv):
    r, member_of = returns(d)
    earned = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    invest = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL.clip(lower=0) + d.CAP_VAL).to_numpy(float)
    fed, eitc, actc = model_fields(d, r, member_of, earned, invest)
    w = d.pwwgt0.to_numpy()[r.row]
    rows = []
    for name, model, census in [("fedtax_bc", fed, d.FEDTAX_BC.to_numpy(float)[r.row]),
                                ("eitc", eitc, d.EIT_CRED.to_numpy(float)[r.row]),
                                ("actc", actc, d.ACTC_CRD.to_numpy(float)[r.row])]:
        err = model - census
        rows.append(dict(field=name, returns=len(r), census_total_bn=float(census @ w / 1e9),
                         model_total_bn=float(model @ w / 1e9), weighted_corr=float(
                             np.cov(model, census, aweights=w)[0, 1] / np.sqrt(
                                 np.cov(model, aweights=w) * np.cov(census, aweights=w))),
                         mean_abs_error=float(np.abs(err) @ w / w.sum()),
                         share_within_100=float(((np.abs(err) <= 100) * w).sum() / w.sum())))
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import common as c
    print(validate(c.load_frame(), c.OUT / "taxcalc_validation.csv").to_string(index=False))

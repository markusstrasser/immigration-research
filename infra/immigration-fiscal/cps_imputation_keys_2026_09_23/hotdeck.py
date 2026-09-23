"""Step 4b: re-impute the imputed items from donors of the same union status and nativity.

Sequential cell hot deck with a fixed seed. Every imputed item is replaced by the value of a
reported donor drawn (with probability proportional to the ASEC weight) from the recipient's
cell. Cells always hold union membership and nativity (foreign-born or not) fixed; the other
match variables are basic-CPS items, which are observed even for whole-supplement
nonrespondents, and are dropped in the order of LEVELS until a cell holds MIN_DONORS donors.

- Whole-supplement nonrespondents (FL_665 != 1): one donor supplies all income blocks, as in the
  Census full-record imputation ("all income items are imputed together by matching to another
  individual", Rothbaum 2019, p. 6).
- Item nonrespondents: each block separately. A recipient who reported receipt draws only from
  reported recipients; a longest-job earnings value imputed from a range answer (I_ERNVAL 1-3)
  draws only from donors in the same range bin and earnings source.
- Coverage (Medicare, Medicaid; flags 1 and 3) is re-imputed from reported persons.
- Household noncash benefits (SNAP, housing, energy, school lunch, WIC) are re-imputed per SPM
  unit from units of the same head union status and nativity, size, children and earners.
- Census tax-model fields change by the difference of taxcalc.py evaluated on new and published
  incomes; state tax by the state's marginal rate on AGI; payroll tax by statute; SPM resources
  by the change in cash, noncash and taxes.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import common as c
import taxcalc

MIN_DONORS = 5
BLOCKS = {
    "earnings": ["WSAL_VAL", "SEMP_VAL", "FRSE_VAL"],
    "interest": ["INT_VAL"], "dividends": ["DIV_VAL"], "rent": ["RNT_VAL"],
    "social_security": ["SS_VAL"], "ssi": ["SSI_VAL"], "public_assistance": ["PAW_VAL"],
    "unemployment": ["UC_VAL"], "veterans": ["VET_VAL"], "workers_comp": ["WC_VAL"],
    "pensions_retirement": ["PEN_VAL1", "PEN_VAL2", "DST_VAL1", "DST_VAL2", "ANN_VAL"],
    "survivor_disability": ["SUR_VAL1", "SUR_VAL2", "DIS_VAL1", "DIS_VAL2"],
    "other_income": ["CSP_VAL", "ED_VAL", "FIN_VAL", "OI_VAL", "CAP_VAL"],
}
STATUS_OF = {"earnings": "earnings"}  # other blocks share their name with common.ITEMS
RECEIPT_YN = {"social_security": "SS_YN", "ssi": "SSI_YN", "public_assistance": "PAW_YN",
              "unemployment": "UC_YN", "veterans": "VET_YN", "workers_comp": "WC_YN",
              "interest": "INT_YN", "dividends": "DIV_YN", "rent": "RNT_YN"}
YN_FLAG = {"social_security": "I_SSYN", "ssi": "I_SSIYN", "public_assistance": "I_PAWYN",
           "unemployment": "I_UCYN", "veterans": "I_VETYN", "workers_comp": "I_WCYN",
           "interest": "I_INTYN", "dividends": "I_DIVYN", "rent": "I_RNTYN"}
BASE = ["union", "foreign_born"]
LEVELS = [
    ["age9", "sex", "edu5", "race3", "lf5", "class4", "occ", "married", "rel5", "region"],
    ["age9", "sex", "edu5", "race3", "lf5", "class4", "married"],
    ["age6", "sex", "edu4", "race3", "lf5", "class4"],
    ["age6", "sex", "edu4", "lf5"],
    ["age3", "sex", "lf5"],
    ["age3", "sex"],
    [],
]
# Item-level re-imputation of non-earnings income also matches on income to this point.
ITEM_LEVELS = [
    ["age9", "sex", "edu5", "race3", "lf5", "married", "rel5", "region", "hinc5", "earn7"],
    ["age9", "sex", "edu5", "lf5", "married", "hinc5", "earn7"],
    ["age6", "sex", "edu4", "lf5", "hinc5", "earn7"],
    ["age6", "sex", "lf5", "hinc5"],
    ["age3", "sex", "hinc5"],
    ["age3", "sex"],
    [],
]
UNIT_LEVELS = [
    ["size", "kids", "earners", "hage", "hedu", "region", "tenure"],
    ["size", "kids", "earners", "hage", "hedu"],
    ["size", "kids", "earners"],
    ["size", "kids"],
    ["size"],
    [],
]
EARN_BINS = [-np.inf, 15000, 30000.5, 44999.5, 60000.5, np.inf]  # dictionary's five range bins


def draw_donors(rng, cells, recipients, donors, weight, levels, extra_r=None, extra_d=None, base=BASE):
    """Return donor row for each recipient row (sequential collapse over levels)."""
    out = np.full(len(recipients), -1)
    level_used = np.full(len(recipients), -1)
    todo = np.arange(len(recipients))
    # After the listed levels: the base cell with any donor, then union alone, then all donors.
    steps = [(base + cols, MIN_DONORS) for cols in levels] + [(base, 1), (base[:1], 1), ([], 1)]
    for li, (keycols, minimum) in enumerate(steps):
        if len(todo) == 0:
            break
        if not keycols:
            keycols = ["_all"]
            cells = cells.assign(_all=0)
        rkey = pd.MultiIndex.from_frame(cells.iloc[recipients[todo]][keycols].reset_index(drop=True))
        dkey = pd.MultiIndex.from_frame(cells.iloc[donors][keycols].reset_index(drop=True))
        if extra_r is not None:
            rkey = pd.MultiIndex.from_arrays([*[rkey.get_level_values(i) for i in range(rkey.nlevels)], extra_r[todo]])
            dkey = pd.MultiIndex.from_arrays([*[dkey.get_level_values(i) for i in range(dkey.nlevels)], extra_d])
        codes, uniq = pd.factorize(pd.Index(dkey.append(rkey)))
        dcode, rcode = codes[:len(donors)], codes[len(donors):]
        count = np.bincount(dcode, minlength=len(uniq))
        ok = count[rcode] >= minimum
        if not ok.any():
            continue
        order = np.lexsort((np.arange(len(donors)), dcode))
        sw = weight[donors][order]
        cum = np.cumsum(sw)
        wsum = np.bincount(dcode, weights=weight[donors], minlength=len(uniq))
        start_cum = np.concatenate([[0], np.cumsum(wsum)[:-1]])
        idx = todo[ok]
        rc = rcode[ok]
        target = start_cum[rc] + rng.random(len(idx)) * wsum[rc]
        pos = np.searchsorted(cum, target, side="right")
        pos = np.minimum(pos, len(order) - 1)
        out[idx] = donors[order][pos]
        level_used[idx] = li
        todo = todo[~ok]
    if len(todo):
        raise ValueError(f"{len(todo)} recipients without donors")
    return out, level_used


def unit_frame(d, union, cv):
    """One row per SPM unit, keyed by the unit's head."""
    idx = c.spm_index(d)
    n = idx.max() + 1
    head = np.zeros(n, int)
    head_rows = np.flatnonzero(d.SPM_HEAD.eq(1).to_numpy())
    head[idx[head_rows]] = head_rows
    size = np.bincount(idx, minlength=n)
    kids = np.bincount(idx, weights=d.A_AGE.lt(18).to_numpy(float), minlength=n)
    earners = np.bincount(idx, weights=(cv.lf5.eq(1) & d.A_AGE.ge(15)).to_numpy(float), minlength=n)
    u = pd.DataFrame(dict(union=union[head].astype(int), foreign_born=cv.foreign_born.to_numpy()[head],
                          size=np.minimum(size, 5), kids=np.minimum(kids, 3).astype(int),
                          earners=np.minimum(earners, 2).astype(int), hage=cv.age3.to_numpy()[head],
                          hedu=cv.edu4.to_numpy()[head], region=cv.region.to_numpy()[head],
                          tenure=d.H_TENURE.to_numpy()[head]))
    return u, idx, head, size


def payroll(wage, se_net):
    wage = np.maximum(wage, 0)
    se = .9235 * np.maximum(se_net, 0)
    se = np.where(se >= 400, se, 0)
    cap = 168600
    return .062 * np.minimum(wage, cap) + .0145 * wage + .124 * np.minimum(se, np.maximum(cap - np.minimum(wage, cap), 0)) + .029 * se


def state_rates(d, r):
    """Average marginal state income-tax rate per state: weighted slope of STATETAX_A on AGI."""
    rows = r.row.to_numpy()
    agi = d.AGI.to_numpy(float)[rows]
    st = d.STATETAX_A.to_numpy(float)[rows]
    fips = d.GESTFIPS.to_numpy()[rows]
    w = d.pwwgt0.to_numpy()[rows]
    keep = (agi > 10000) & (agi < 250000)
    rate = {}
    for f in np.unique(fips):
        m = keep & (fips == f)
        x, y, ww = agi[m], st[m], w[m]
        xm, ym = np.average(x, weights=ww), np.average(y, weights=ww)
        rate[f] = max(float(np.sum(ww * (x - xm) * (y - ym)) / np.sum(ww * (x - xm) ** 2)), 0.)
    return rate


def taxable_ss_share(agi, status):
    lo = np.where(status == "joint", 32000, 25000)
    hi = np.where(status == "joint", 44000, 34000)
    return np.select([agi < lo, agi < hi], [0., .5], .85)


# Item-level property, retirement and other income stay at the Census values in the main
# specification: the redesigned Census models for them use asset-type detail (checking, savings,
# money-market and retirement interest) that a public-file cell hot deck cannot reproduce, and
# re-imputing them from coarser cells lowers their totals for everyone (see RESULT.md, step 4b).
PROPERTY_BLOCKS = ("interest", "dividends", "rent", "pensions_retirement", "survivor_disability", "other_income")


def run(d, seed=20260923, verbose=True, base=BASE, item_property=False):
    """base=BASE matches donors on union membership and nativity; base=[] pools all donors (control).
    item_property=True also re-imputes item-level property, retirement and other income."""
    rng = np.random.default_rng(seed)
    def draw(*args, **kwargs):  # bind the donor-pool rule for this run
        return draw_donors(*args, base=base, **kwargs)
    civ, union = c.masks(d)
    cv = c.cell_vars(d)
    cv["union"] = union.astype(int)
    cv = cv.reset_index(drop=True)
    s = c.person_status(d)
    w = d.pwwgt0.to_numpy(float)
    adult = d.A_AGE.ge(15).to_numpy()
    full = d.FL_665.ne(1).to_numpy() & adult
    new = d.copy()
    diag = []
    # ---- whole-supplement records: one donor for every income block --------------------------
    clean = adult & civ & ~full & ~np.logical_or.reduce([s[b] for b in BLOCKS if b not in
                                                         ("interest", "dividends", "rent", "other_income")])
    recipients = np.flatnonzero(full)
    donors = np.flatnonzero(clean)
    donor, level = draw(rng, cv, recipients, donors, w, LEVELS)
    cols = [col for b in BLOCKS.values() for col in b]
    new.loc[recipients, cols] = d.loc[donor, cols].to_numpy()
    new.loc[recipients, "ERN_VAL"] = d.loc[donor, "ERN_VAL"].to_numpy()
    diag.append(dict(block="whole_supplement", recipients=len(recipients), donors=len(donors),
                     level_mean=level.mean(), level_max=level.max()))
    # ---- item nonrespondents: block by block -----------------------------------------------
    for block, columns in BLOCKS.items():
        if block in PROPERTY_BLOCKS and not item_property:
            continue
        status = s[STATUS_OF.get(block, block)]
        rec = adult & status & ~full
        rep = adult & civ & ~status & ~full
        if block == "earnings":
            lvl = d.I_ERNVAL.to_numpy()
            ranged = rec & np.isin(lvl, [1, 2, 3]) & d.ERN_YN.eq(1).to_numpy()
            said_yes = rec & ~ranged & d.ERN_YN.eq(1).to_numpy() & (d.I_ERNYN.to_numpy() == 0) & \
                (d.I_WORKYN.to_numpy() == 0)
            other = rec & ~ranged & ~said_yes
            ern_bin = np.digitize(d.ERN_VAL.to_numpy(float), EARN_BINS)
            src = d.ERN_SRCE.to_numpy()
            groups = [("range", ranged, rep & d.ERN_YN.eq(1).to_numpy() & (d.ERN_VAL.to_numpy() != 0), True),
                      ("recipient", said_yes, rep & d.ERN_YN.eq(1).to_numpy(), False),
                      ("any", other, rep, False)]
            for gname, rmask, dmask, use_bin in groups:
                r_rows, d_rows = np.flatnonzero(rmask), np.flatnonzero(dmask)
                if len(r_rows) == 0:
                    continue
                if use_bin:
                    extra_r = ern_bin[r_rows] * 10 + src[r_rows]
                    extra_d = ern_bin[d_rows] * 10 + src[d_rows]
                    donor, level = draw(rng, cv, r_rows, d_rows, w, LEVELS, extra_r, extra_d)
                else:
                    donor, level = draw(rng, cv, r_rows, d_rows, w, LEVELS)
                new.loc[r_rows, columns] = d.loc[donor, columns].to_numpy()
                diag.append(dict(block=f"earnings_{gname}", recipients=len(r_rows), donors=len(d_rows),
                                 level_mean=level.mean(), level_max=level.max()))
            continue
        yn = RECEIPT_YN.get(block)
        if yn is not None:
            said_yes = rec & d[yn].eq(1).to_numpy() & (d[YN_FLAG[block]].to_numpy() == 0)
            parts = [("recipient", said_yes, rep & (d[columns].sum(axis=1).to_numpy() != 0)),
                     ("any", rec & ~said_yes, rep)]
        else:
            parts = [("any", rec, rep)]
        for gname, rmask, dmask in parts:
            r_rows, d_rows = np.flatnonzero(rmask), np.flatnonzero(dmask)
            if len(r_rows) == 0:
                continue
            donor, level = draw(rng, cv, r_rows, d_rows, w, ITEM_LEVELS)
            new.loc[r_rows, columns] = d.loc[donor, columns].to_numpy()
            diag.append(dict(block=f"{block}_{gname}", recipients=len(r_rows), donors=len(d_rows),
                             level_mean=level.mean(), level_max=level.max()))
    # ---- coverage ------------------------------------------------------------------------
    for col, flag in [("MCARE", "I_MCARE"), ("MCAID", "I_MCAID")]:
        f = d[flag].to_numpy()
        r_rows, d_rows = np.flatnonzero(np.isin(f, [1, 3])), np.flatnonzero((f == 0) & civ)
        donor, level = draw(rng, cv, r_rows, d_rows, w, LEVELS)
        new.loc[r_rows, col] = d.loc[donor, col].to_numpy()
        diag.append(dict(block=col, recipients=len(r_rows), donors=len(d_rows), level_mean=level.mean(),
                         level_max=level.max()))
    # ---- household noncash benefits per SPM unit ----------------------------------------
    units, idx, head, size = unit_frame(d, union, cv)
    unit_flag = {"SPM_SNAPSUB": s["snap"], "SPM_CAPHOUSESUB": s["housing"], "SPM_ENGVAL": s["energy"],
                 "SPM_SCHLUNCH": s["school_lunch"], "SPM_WICVAL": c.unit_any(s["wic_person"], d.SPM_ID.to_numpy())}
    head_full = d.FL_665.ne(1).to_numpy()[head]
    per_capita = {}
    noncash_change = np.zeros(len(units))
    for col, flag in unit_flag.items():
        uflag = flag[head]
        r_units = np.flatnonzero(uflag)
        d_units = np.flatnonzero(~uflag & ~head_full)
        donor, level = draw(rng, units, r_units, d_units, np.ones(len(units)) * w[head], UNIT_LEVELS)
        value = d[col].to_numpy(float)[head]
        newval = value.copy()
        newval[r_units] = value[donor] / size[donor] * size[r_units]
        noncash_change += newval - value
        per_capita[col] = newval
        diag.append(dict(block=col, recipients=len(r_units), donors=len(d_units), level_mean=level.mean(),
                         level_max=level.max()))
    for col, val in per_capita.items():
        new[col] = val[idx]
    # ---- derived: federal and state income tax, payroll tax, SPM resources -------------------
    r, member_of = taxcalc.returns(d)
    status_arr = r.status.to_numpy()
    rows = r.row.to_numpy()
    n = len(d)
    def agi_part(frame):
        return (frame.WSAL_VAL + frame.SEMP_VAL + frame.FRSE_VAL + frame.INT_VAL + frame.DIV_VAL + frame.RNT_VAL
                + frame.UC_VAL + frame.PEN_VAL1 + frame.PEN_VAL2 + frame.DST_VAL1 + frame.DST_VAL2 + frame.ANN_VAL
                + frame.SUR_VAL1 + frame.SUR_VAL2 + frame.DIS_VAL1 + frame.DIS_VAL2 + frame.OI_VAL
                + frame.CAP_VAL).to_numpy(float)
    d_agi_person = agi_part(new) - agi_part(d)
    d_ss_person = (new.SS_VAL - d.SS_VAL).to_numpy(float)
    agi_old = d.AGI.to_numpy(float)[rows]
    ss_share = taxable_ss_share(agi_old, status_arr)
    d_agi = taxcalc.member_sums(d_agi_person, member_of, n)[rows] + ss_share * taxcalc.member_sums(d_ss_person, member_of, n)[rows]
    agi_new = agi_old + d_agi
    earned_old = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    earned_new = (new.WSAL_VAL + new.SEMP_VAL + new.FRSE_VAL).to_numpy(float)
    inv_old = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL.clip(lower=0) + d.CAP_VAL).to_numpy(float)
    inv_new = (new.INT_VAL + new.DIV_VAL + new.RNT_VAL.clip(lower=0) + new.CAP_VAL).to_numpy(float)
    f0, e0, a0 = taxcalc.model_fields(d, r, member_of, earned_old, inv_old, agi_old)
    f1, e1, a1 = taxcalc.model_fields(d, r, member_of, earned_new, inv_new, agi_new)
    fed = d.FEDTAX_BC.to_numpy(float).copy()
    eit = d.EIT_CRED.to_numpy(float).copy()
    act = d.ACTC_CRD.to_numpy(float).copy()
    fed[rows] = np.maximum(fed[rows] + f1 - f0, 0)
    eit[rows] = np.maximum(eit[rows] + e1 - e0, 0)
    act[rows] = np.maximum(act[rows] + a1 - a0, 0)
    # Adults outside any published return whose re-imputed income is positive file as single.
    loose = (member_of < 0) & d.A_AGE.ge(18).to_numpy() & (np.abs(d_agi_person) + np.abs(d_ss_person) > 0)
    lrows = np.flatnonzero(loose)
    if len(lrows):
        lagi = np.maximum(agi_part(new)[lrows] + .85 * np.maximum(new.SS_VAL.to_numpy(float)[lrows] - 25000, 0), 0)
        zeros = np.zeros(len(lrows))
        lf, le, la = taxcalc.compute(lagi, earned_new[lrows], inv_new[lrows], np.full(len(lrows), "single"),
                                     zeros, zeros, zeros, (d.A_AGE.to_numpy()[lrows] >= 65).astype(float),
                                     d.A_AGE.to_numpy()[lrows])
        of, oe, oa = taxcalc.compute(np.maximum(agi_part(d)[lrows], 0), earned_old[lrows], inv_old[lrows],
                                     np.full(len(lrows), "single"), zeros, zeros, zeros,
                                     (d.A_AGE.to_numpy()[lrows] >= 65).astype(float), d.A_AGE.to_numpy()[lrows])
        fed[lrows] = np.maximum(fed[lrows] + lf - of, 0)
        eit[lrows] = np.maximum(eit[lrows] + le - oe, 0)
    rates = state_rates(d, r)
    state = d.STATETAX_A.to_numpy(float).copy()
    fips = d.GESTFIPS.to_numpy()
    state[rows] = state[rows] + np.array([rates[f] for f in fips[rows]]) * d_agi
    fica_change = payroll(new.WSAL_VAL.to_numpy(float), (new.SEMP_VAL + new.FRSE_VAL).to_numpy(float)) - \
        payroll(d.WSAL_VAL.to_numpy(float), (d.SEMP_VAL + d.FRSE_VAL).to_numpy(float))
    fica = np.maximum(d.FICA.to_numpy(float) + fica_change, 0)
    changed = (new.WSAL_VAL.to_numpy() != d.WSAL_VAL.to_numpy()) | \
        ((new.SEMP_VAL + new.FRSE_VAL).to_numpy() != (d.SEMP_VAL + d.FRSE_VAL).to_numpy())
    covered = (new.WSAL_VAL.to_numpy() > 0) | (.9235 * (new.SEMP_VAL + new.FRSE_VAL).to_numpy() >= 400)
    fica = np.where(changed, np.where(covered, np.maximum(fica, 1), 0), d.FICA.to_numpy(float))
    new["FEDTAX_BC"], new["EIT_CRED"], new["ACTC_CRD"] = fed, eit, act
    new["STATETAX_A"], new["FICA"] = state, fica
    new["AGI"] = d.AGI.to_numpy(float)
    new.loc[rows, "AGI"] = agi_new
    cash_cols = [col for b in BLOCKS.values() for col in b] + ["SS_VAL"]
    cash_cols = list(dict.fromkeys(cash_cols))
    d_cash = (new[cash_cols].sum(axis=1) - d[cash_cols].sum(axis=1)).to_numpy(float)
    d_fedac = (fed - eit - act) - (d.FEDTAX_BC - d.EIT_CRED - d.ACTC_CRD).to_numpy(float)
    d_person = d_cash - d_fedac - (state - d.STATETAX_A.to_numpy(float)) - (fica - d.FICA.to_numpy(float))
    d_unit = np.bincount(idx, weights=d_person, minlength=len(units)) + noncash_change
    new["SPM_RESOURCES"] = d.SPM_RESOURCES.to_numpy(float) + d_unit[idx]
    diag = pd.DataFrame(diag)
    if verbose:
        print(diag.to_string(index=False), flush=True)
    return new, diag


if __name__ == "__main__":
    d = c.load_frame()
    new, diag = run(d)
    civ, union = c.masks(d)
    w = d.pwwgt0.to_numpy()
    for col in ["WSAL_VAL", "SS_VAL", "FEDTAX_BC", "STATETAX_A", "EIT_CRED", "SPM_RESOURCES", "SPM_SNAPSUB"]:
        before = (d[col].to_numpy(float) * w)[union].sum() / 1e9
        after = (new[col].to_numpy(float) * w)[union].sum() / 1e9
        ob = (d[col].to_numpy(float) * w)[civ & ~union].sum() / 1e9
        oa = (new[col].to_numpy(float) * w)[civ & ~union].sum() / 1e9
        print(f"{col:14s} union {before:9.2f} -> {after:9.2f} ({after / before - 1:+.2%}); "
              f"other {ob:9.2f} -> {oa:9.2f} ({oa / ob - 1:+.2%})", flush=True)

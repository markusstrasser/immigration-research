"""Survey-independent assembly of person records into taxcalc tax units.

Both surveys hand this module the same person-level schema, so the CPS and the
ACS arm differ only in how that schema is filled in, never in how returns are
formed, counted or allocated.

Required person columns
-----------------------
ret_unit    integer code of the return holding this person's income
ret_role    0 head, 1 spouse, 2 dependent without a return of his own
claim_unit  integer code of the return that claims this person
claim_role  0 head, 1 spouse, 2 dependent
age         integer age
mars        filing status of `ret_unit` (constant inside a return)
dsi         1 when `ret_unit` is a dependent's own return

A dependent who files his own return therefore has ret_role 0 on his own
return and claim_role 2 on the return that claims him: his income is taxed
separately while he still counts as a dependent for the claiming return's
exemptions and credits.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SPLIT = {"e00200": ("e00200p", "e00200s"),
         "e00900": ("e00900p", "e00900s"),
         "e02100": ("e02100p", "e02100s")}


def build_frame(p: pd.DataFrame, income: dict[str, np.ndarray],
                n_returns: int, eic_child: np.ndarray | None = None) -> pd.DataFrame:
    """One taxcalc input row per return.

    `eic_child` is a person-level mask of EITC-qualifying children. When it is
    omitted the test falls back to age under 19; the statutory test also
    accepts a child under 24 who is a student, which each survey supplies from
    its own enrolment variable.
    """
    ret = p.ret_unit.to_numpy()
    claim = p.claim_unit.to_numpy()
    age = p.age.to_numpy()
    head = (p.ret_role == 0).to_numpy()
    spouse = (p.ret_role == 1).to_numpy()
    filer = head | spouse
    claimed_dep = (p.claim_role == 2).to_numpy()
    n = n_returns

    def on_ret(mask, vals=None):
        w = np.where(mask, 1.0 if vals is None else vals, 0.0)
        return np.bincount(ret, weights=w, minlength=n)

    def on_claim(mask, vals=None):
        w = np.where(mask, 1.0 if vals is None else vals, 0.0)
        return np.bincount(claim, weights=w, minlength=n)

    # A code can exist purely as a claim unit: every one of its members filed
    # a separate dependent return, so nothing is left to tax on it. Such rows
    # stay in the frame (the code space is shared with `claim`) as empty
    # single returns and contribute nothing.
    occupied = np.bincount(ret, minlength=n) > 0
    nhead = np.bincount(ret[head], minlength=n)
    nspouse = np.bincount(ret[spouse], minlength=n)
    if nhead.max() > 1 or nspouse.max() > 1:
        raise SystemExit("[BLOCKED] return with more than one head or spouse")
    if (occupied & (nhead == 0)).any():
        raise SystemExit("[BLOCKED] occupied return without a head")
    joint = np.zeros(n, dtype=bool)
    joint[ret[head]] = p.mars.to_numpy()[head] == 2
    if ((nspouse == 1) & ~joint).any():
        raise SystemExit("[BLOCKED] spouse on a return that is not filing jointly")

    out = pd.DataFrame(index=range(n))
    out["RECID"] = np.arange(1, n + 1)

    mars = np.ones(n)
    mars[ret[head]] = p.mars.to_numpy()[head]
    out["MARS"] = mars.astype(int)

    dsi = np.zeros(n)
    dsi[ret[head]] = p.dsi.to_numpy()[head]
    out["DSI"] = dsi.astype(int)

    ah = np.zeros(n)
    ah[ret[head]] = age[head]
    asp = np.zeros(n)
    asp[ret[spouse]] = age[spouse]
    out["age_head"] = ah.astype(int)
    out["age_spouse"] = asp.astype(int)

    # membership for counts: own head/spouse plus the dependents claimed here
    def members(mask_on_person):
        return on_ret(filer & mask_on_person) + on_claim(claimed_dep & mask_on_person)

    everyone = np.ones(len(p), dtype=bool)
    out["XTOT"] = members(everyone).astype(int)
    out["nu18"] = members(age < 18).astype(int)
    out["n1820"] = members((age >= 18) & (age <= 20)).astype(int)
    out["n21"] = members(age >= 21).astype(int)
    out["nu13"] = members(age < 13).astype(int)
    out["nu06"] = members(age < 6).astype(int)
    out["n24"] = on_claim(claimed_dep & (age < 17)).astype(int)
    eic_mask = (age < 19) if eic_child is None else np.asarray(eic_child, dtype=bool)
    out["EIC"] = np.minimum(on_claim(claimed_dep & eic_mask), 3).astype(int)
    out["elderly_dependents"] = on_claim(claimed_dep & (age >= 65)).astype(int)

    for key, vals in income.items():
        if key in SPLIT:
            ph, ps = SPLIT[key]
            out[ph] = on_ret(head, vals)
            out[ps] = on_ret(spouse, vals)
            out[key] = out[ph] + out[ps]
        else:
            out[key] = on_ret(filer, vals)
    return out


def allocate(ret: np.ndarray, earnings: np.ndarray, unit_value: np.ndarray) -> np.ndarray:
    """Split each return's dollars over its members, by own earnings.

    Proportional to the person's own positive earnings; equal shares when the
    return has no positive earnings. Conservation is asserted.
    """
    n = unit_value.shape[0]
    pos = np.clip(earnings, 0.0, None)
    tot = np.bincount(ret, weights=pos, minlength=n)
    size = np.bincount(ret, minlength=n).astype(float)
    denom = np.where(tot[ret] > 0, tot[ret], 1.0)
    share = np.where(tot[ret] > 0, pos / denom, 1.0 / size[ret])
    person = unit_value[ret] * share
    back = np.bincount(ret, weights=person, minlength=n)
    scale = max(1.0, float(np.abs(unit_value).max()))
    if not np.allclose(back, unit_value, rtol=1e-9, atol=1e-6 * scale):
        raise SystemExit("[BLOCKED] allocation does not conserve unit dollars")
    return person


def promote_headless(p: pd.DataFrame) -> pd.DataFrame:
    """Give any return whose members are all dependents an oldest-member head.

    Such returns exist in the CPS file (126 of them) and can appear in the ACS
    construction; they carry no taxable income but must still be well formed.
    """
    has_head = p.groupby("ret_unit").ret_role.min().eq(0)
    bad = has_head[~has_head].index
    if len(bad) == 0:
        return p
    p = p.copy()
    sub = p[p.ret_unit.isin(bad)]
    pick = sub.sort_values(["ret_unit", "age"], ascending=[True, False]) \
              .groupby("ret_unit").head(1).index
    p.loc[pick, ["ret_role", "claim_role", "mars", "dsi"]] = [0, 0, 1, 1]
    return p

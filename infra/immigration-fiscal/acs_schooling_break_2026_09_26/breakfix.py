"""Break corrections for the ACS 2020 "no schooling completed" step, shared by this lane's re-runs.

Method A (the brief's): a share phi of a group's 2020+ no-schooling reports is excess; it is returned
to grades 1-8 in proportion to the same group's 2019 distribution over grades 1-8.

Method B (flow rates, preferred): in a fixed population whose attainment cannot change
(break_anatomy.py, universe "fixed"), every category below a diploma that loses mass at the 2020
step is a source. For source category c: loss_c = -step_c, counterfactual post share
cf_c = observed post mean - step_c, loss rate lambda_c = loss_c / cf_c. Only part of the gross
losses went to "none" (kappa = none step / sum of losses); the rest went to grade 5, preschool or
12th grade without a diploma, which the brief does not ask to undo. The flow rate into "none" is
pi_c = kappa * lambda_c. Applied to any group with observed 2020+ shares obs_c:
  flow_c = pi_c * obs_c / (1 - lambda_c)     (obs_c / (1 - lambda_c) is the group's counterfactual)
  excess = sum_c flow_c,  phi = excess / obs_none,  destination_c = flow_c / excess.
Unlike A, B lets a group with few primary-only members get a small correction, and it returns
reports to grade 9 as well as to grades 1-8, which the anatomy shows is where they came from.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STEPS = HERE / "derived" / "break_steps.csv"
SHARES = HERE / "derived" / "break_anatomy_shares.csv"
POST_YEARS = (2021, 2022, 2023, 2024)

# categories below a diploma, as ACS SCHL codes and as IPUMS EDUCD codes (ACS 2008+ detail)
SCHL_CODES = {"none": [1], "prek": [2, 3], "g1_4": [4, 5, 6, 7], "g5": [8], "g6": [9], "g7": [10], "g8": [11],
              "g9": [12], "g10": [13], "g11": [14], "g12_nodip": [15]}
EDUCD_CODES = {"none": [2], "prek": [11, 12], "g1_4": [14, 15, 16, 17], "g5": [22], "g6": [23], "g7": [25],
               "g8": [26], "g9": [30], "g10": [40], "g11": [50], "g12_nodip": [61]}
SOURCES = [c for c in SCHL_CODES if c != "none"]
GRADES_1_8 = {"schl": [4, 5, 6, 7, 8, 9, 10, 11], "educd": [14, 15, 16, 17, 22, 23, 25, 26]}
YEARS_OF_GRADE = {"schl": {s: s - 3 for s in range(4, 16)}, "educd": {14: 1, 15: 2, 16: 3, 17: 4, 22: 5, 23: 6,
                                                                       25: 7, 26: 8, 30: 9, 40: 10, 50: 11}}


def gate(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit(msg)


def flow_rates(group: str, universe: str = "fixed") -> dict:
    """Method B parameters for one origin group, from the anatomy's trend steps."""
    T = pd.read_csv(STEPS)
    S = pd.read_csv(SHARES)
    t = T[(T.universe == universe) & (T.group == group)].set_index("category")
    s = S[(S.universe == universe) & (S.group == group) & S.year.isin(POST_YEARS)]
    gate(len(t) > 0 and len(s) > 0, f"[BLOCKED] no anatomy rows for {group}/{universe}")
    post = s.groupby("category").share_pct.mean()
    none_step = float(t.loc["none", "trend_step"])
    gate(none_step > 0, f"[BLOCKED] {group}: no upward step in no-schooling reports")
    lam, loss = {}, {}
    for c in SOURCES:
        st = float(t.loc[c, "trend_step"])
        if st < 0:
            loss[c] = -st
            lam[c] = -st / (float(post[c]) - st)
    kappa = none_step / sum(loss.values())
    gate(0 < kappa <= 1, f"[BLOCKED] {group}: none step {none_step:.3f} exceeds below-diploma losses")
    return {"group": group, "universe": universe, "none_step_pp": none_step, "kappa": kappa, "lam": lam,
            "pi": {c: kappa * lam[c] for c in lam}, "loss_pp": loss}


def split_b(weights: dict, rates: dict, coding: str) -> tuple[float, dict]:
    """phi and destination (code -> share of the excess) for a group whose weights by code are given."""
    codes = SCHL_CODES if coding == "schl" else EDUCD_CODES
    w_none = sum(weights.get(k, 0.0) for k in codes["none"])
    gate(w_none > 0, "[BLOCKED] group has no no-schooling reports to correct")
    flows = {}
    for c, pi in rates["pi"].items():
        wc = {k: weights.get(k, 0.0) for k in codes[c]}
        tot = sum(wc.values())
        if tot <= 0:
            continue
        f = pi * tot / (1 - rates["lam"][c])
        for k, v in wc.items():
            if v > 0:
                flows[k] = flows.get(k, 0.0) + f * v / tot
    excess = sum(flows.values())
    phi = excess / w_none
    gate(0 < phi < 1, f"[BLOCKED] excess share phi={phi:.3f} outside (0, 1)")
    return phi, {k: v / excess for k, v in flows.items()}


def split_a(weights_2019: dict, coding: str) -> dict:
    """Destination for method A: the group's 2019 distribution over grades 1-8."""
    codes = GRADES_1_8[coding]
    w = {k: weights_2019.get(k, 0.0) for k in codes}
    tot = sum(w.values())
    gate(tot > 0, "[BLOCKED] no 2019 grades 1-8 reports for the method-A destination")
    return {k: v / tot for k, v in w.items() if v > 0}


def mean_years(dest: dict, coding: str) -> float:
    y = YEARS_OF_GRADE[coding]
    return float(sum(y[k] * v for k, v in dest.items()))


def weights_by_code(codes: np.ndarray, w: np.ndarray) -> dict:
    s = pd.Series(w).groupby(codes).sum()
    return {int(k): float(v) for k, v in s.items()}

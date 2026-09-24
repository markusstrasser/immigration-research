"""Remittance outflows for every CPS SPM unit, calibrated to a national flow.

A unit's expected outflow is M = theta * P * rho * E: P is the measured household sender rate for
its type (FDIC supplement to the June CPS, 2015 and 2017 pooled; derived/sender_rates_pooled.csv),
E the unit's positive earnings, rho the amount of a US-born-only sending unit relative to one with a
foreign-born member (no source measures it), and theta a share of earnings solved so that a named
set of units sends a named national flow. The first generation's share of the group's outflow is
therefore an output of measured sender counts and rho, never an input: remit_leak's correction
(2026-09-17) rules out treating CEMLA's 16.7% quotient, all US-to-Mexico remittances over
first-generation earnings, as a first-generation sending rate.

Types follow the unit head (SPM_HEAD), as FDIC classifies households by the householder:
  Mexico-born head                      37.3%  (all households)
  other foreign-born head               28.7%
  US-born head, G2 / G3+ / other native with a foreign-born member: 26.3% / 11.2% / 18.8%
  US-born head, no foreign-born member: 6.5% / 1.45% / 1.28%
The FDIC unit is the household; applying its rates to SPM units treats a roommate unit as its own
household [INFERENCE]. Calibrated flows fix the level, so this mainly moves outflow between types.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
MEXICO = 303
US_BIRTH = [57, 60, 66, 69, 73, 78]  # United States and outlying areas (spending builder's union mask)

# National flows, 2024, $bn.
BANXICO_US = 62.794313       # Banxico SIE CE167 series SE43738, sum of four quarters
BANXICO_TOTAL = 65.016836    # CE167 SE43675 (revised from the Feb-2025 release's 64.745)
BEA_PERSONAL_TRANSFERS = 72.407  # BEA ITA Table 5 line 18, June-2025 annual update (trans125)
# Temporary workers are non-residents in both accounts (BEA C&M 6.13, 13.57), but money they wire
# home is inside Banxico's receipts. Mexican H-2B visas FY2024: 90,457 (USCIS Table 1); Mexican
# H-2A: about 250-300 thousand [INFERENCE: 315,328 worldwide, State Dept Table XV(B); Mexico's row
# not read]. At roughly six months of work at the H-2A wage floor (about $17.6 an hour) and half
# to two-thirds of pay sent home, that is $2.5-5.5bn [INFERENCE]; central $4.0bn.
H2_ALLOWANCE = {"low": 2.5, "central": 4.0, "high": 5.5}
# Signos Vitales via Reuters (secondary): "at least $4.4 billion, or 7.5%" of 2022 receipts.
ILLICIT_SHARE = 0.075
# Survey amounts per sender (person): CEMLA-Banxico questionnaire of 6,803 Mexican emigrants visiting
# Mexico over the December 2015 holidays (report March 2018, section 5.4 and Cuadro 6): "la remesa
# mensual promedio es de 380 dolares"; a convenience sample of travellers. NIS-2003 Mexico-born
# givers: $3,192 a year (derived/nis_transfers.csv).
CEMLA_MONTHLY_2015 = 380.0
NIS_MEAN_2003 = 3192.0

RATE_ROWS = {  # (type, scope in sender_rates_pooled.csv)
    "mexico_born_head": ("mexico_born", "all_households"),
    "other_foreign_born_head": ("other_foreign_born", "all_households"),
    "g2_head_fb": ("us_born_mex_parent_G2", "with_foreign_born_member"),
    "g3_head_fb": ("us_born_mex_origin_G3plus", "with_foreign_born_member"),
    "native_head_fb": ("other_native", "with_foreign_born_member"),
    "g2_head_usonly": ("us_born_mex_parent_G2", "no_foreign_born_member"),
    "g3_head_usonly": ("us_born_mex_origin_G3plus", "no_foreign_born_member"),
    "native_head_usonly": ("other_native", "no_foreign_born_member"),
}
TYPES = list(RATE_ROWS)


CORRIDOR = HERE / "_cache" / "sources" / "corridor"


def primary_flows() -> dict:
    """The 2024 flows read back from the primary files: Banxico SIE CE167 (quarterly, $mn) and BEA's
    June-2025 ITA release text (Table 5 line 18)."""
    import openpyxl
    import warnings
    warnings.filterwarnings("ignore")
    ws = openpyxl.load_workbook(CORRIDOR / "banxico_CE167_2022_2025.xlsx", data_only=True).worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True)]
    head = next(r for r in rows if r and "Ene-Mar 2022" in r)
    cols = [i for i, c in enumerate(head) if isinstance(c, str) and c.endswith("2024")]
    def label(r):
        first = next((c for c in r if isinstance(c, str) and c.strip()), "") if r else ""
        return first.replace(" ", "").replace(" ", "").replace("●", "").strip()
    total = next(r for r in rows if label(r) == "Total")
    us = next(r for r in rows if label(r) == "Estados Unidos")
    text = (CORRIDOR / "bea_2025-06_trans125.txt").read_text().splitlines()
    line = next(l for l in text if l.strip().startswith("18") and "Personal transfers" in l)
    bea = [float(x.replace(",", "")) for x in line.split("Personal transfers")[1].split()[1:3]]
    return {"banxico_total_2024": sum(total[i] for i in cols) / 1e3, "banxico_us_2024": sum(us[i] for i in cols) / 1e3,
            "quarters": len(cols), "bea_2023": bea[0] / 1e3, "bea_2024": bea[1] / 1e3}


def sender_rates() -> dict:
    t = pd.read_csv(DERIVED / "sender_rates_pooled.csv")
    out = {}
    for typ, (g, scope) in RATE_ROWS.items():
        row = t[(t.group == g) & (t.scope == scope)]
        if len(row) != 1:
            raise ValueError(f"[BLOCKED] no pooled sender rate for {g}/{scope}; run sender_rates.py")
        out[typ] = float(row.rate_pct.iloc[0]) / 100
    return out


def units(a: dict) -> dict:
    """Unit types, earnings and membership; per-unit arrays indexed by the unit code."""
    n = int(a["n_units"])
    u = a["unit"]
    cit = a["citizen"]
    fb = np.isin(cit, [4, 5])
    usb = np.isin(cit, [1, 2, 3])
    mexborn = fb & (a["penatvty"] == MEXICO)
    g2 = usb & ((a["pefntvty"] == MEXICO) | (a["pemntvty"] == MEXICO))
    g3 = usb & np.isin(a["pefntvty"], US_BIRTH) & np.isin(a["pemntvty"], US_BIRTH) & (a["prdthsp"] == 1)
    any_fb = np.bincount(u, weights=fb.astype(float), minlength=n) > 0
    any_target = np.bincount(u, weights=a["target"].astype(float), minlength=n) > 0
    head = a["head"]
    typ = np.empty(n, dtype=object)
    hu = u[head]
    kind = np.where(mexborn[head], "mexico_born_head",
           np.where(fb[head], "other_foreign_born_head",
           np.where(g2[head], "g2_head", np.where(g3[head], "g3_head", "native_head"))))
    typ[hu] = kind
    us_headed = ~np.isin(typ, ["mexico_born_head", "other_foreign_born_head"])
    typ[us_headed] = np.where(any_fb[us_headed], typ[us_headed] + "_fb", typ[us_headed] + "_usonly")
    earnings = np.bincount(u, weights=np.clip(a["earnings"], 0, None), minlength=n)
    resources = np.zeros(n)
    resources[hu] = np.clip(a["spm_resources"][head], 0, None)
    return {"type": typ, "any_fb": any_fb, "any_target": any_target, "earnings": earnings,
            "resources": resources, "mexborn_person": mexborn, "n": n}


def per_theta(a: dict, un: dict, rates: dict, rho: float) -> np.ndarray:
    """Outflow per unit of theta: P * rho * E (rho applies to units with no foreign-born member)."""
    p = np.array([rates[t] for t in un["type"]])
    r = np.where(un["any_fb"], 1.0, rho)
    return p * r * un["earnings"]


def person_sum(a: dict, per_unit: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Weighted total over persons of a unit quantity split per capita (161 replicate columns)."""
    v = per_unit[a["unit"]] / a["size"]
    if mask is not None:
        v = np.where(mask, v, 0.0)
    return v @ a["weights"]


def solve_theta(a: dict, un: dict, per: np.ndarray, flow_bn: float, scope: np.ndarray) -> np.ndarray:
    """theta (161 replicates) such that units in scope send flow_bn in total."""
    base = person_sum(a, np.where(scope, per, 0.0))
    return flow_bn * 1e9 / base


def survey_theta(a: dict, un: dict, per: np.ndarray, rates: dict, amount: float) -> np.ndarray:
    """theta such that Mexico-born-headed sending units send `amount` dollars a year on average."""
    mx = un["type"] == "mexico_born_head"
    p = np.array([rates[t] for t in un["type"]])
    senders = person_sum(a, np.where(mx, p, 0.0))
    dollars = person_sum(a, np.where(mx, per, 0.0))
    return amount * senders / dollars


def outflow_split(a: dict, un: dict, per: np.ndarray, theta0: float, rates: dict) -> dict:
    """Point outflow ($bn) by sending unit type, and by who bears it in the key.

    The key splits a unit's resources per capita, so a Mexico-born parent's remittance also lowers
    the key of the US-born children in the unit: 'bearer' columns follow the key, 'sent_by' columns
    follow the unit head, which is FDIC's classification of the sender household.
    """
    w = a["weights"][:, 0]
    unit_m = theta0 * per
    m = unit_m[a["unit"]] / a["size"]
    civ, tgt = a["civilian"], a["target"]
    first = tgt & a["mexico_born"]
    usborn = tgt & ~a["mexico_born"]
    out = {"all_civilians_bn": (m[civ] @ w[civ]) / 1e9, "bearer_union_bn": (m[tgt] @ w[tgt]) / 1e9,
           "bearer_union_first_generation_bn": (m[first] @ w[first]) / 1e9,
           "bearer_union_us_born_bn": (m[usborn] @ w[usborn]) / 1e9}
    union_units = un["any_target"]
    for t in TYPES:
        in_t = (un["type"] == t) & union_units
        out[f"sent_by_union_{t}_units_bn"] = float(person_sum(a, np.where(in_t, unit_m, 0.0))[0]) / 1e9
    p = np.array([rates[t] for t in un["type"]])
    senders = float(person_sum(a, np.where(union_units, p, 0.0))[0])
    sent = float(person_sum(a, np.where(union_units, unit_m, 0.0))[0])
    mx = un["type"] == "mexico_born_head"
    out.update(union_units_m=float(person_sum(a, union_units.astype(float))[0]) / 1e6,
               union_expected_sending_units_m=senders / 1e6,
               sent_per_expected_sending_union_unit=sent / senders,
               mexico_born_headed_units_m=float(person_sum(a, mx.astype(float))[0]) / 1e6)
    return out


def spec_flows(a: dict, un: dict, rates: dict, cpi: dict) -> dict:
    """Every remittance specification: per-unit outflow for each replicate's theta.

    Returns {spec: dict(per=per_theta array, theta=161 vector, absolute=bool, note=str, others=...)}.
    'absolute' marks flows fixed in dollars (the Banxico corridor), which do not scale with the
    adopted count corrections.
    """
    cemla = CEMLA_MONTHLY_2015 * 12 * cpi[2024] / cpi[2015]
    nis = NIS_MEAN_2003 * cpi[2024] / cpi[2003]
    corridor_units = un["any_target"]
    fb_units = un["any_fb"]
    specs = {}

    def add(name, rho, theta_fn, absolute, note, others="same_theta"):
        per = per_theta(a, un, rates, rho)
        theta = theta_fn(per)
        specs[name] = dict(per=per, theta=theta, absolute=absolute, note=note, rho=rho, others=others)

    for rho in (0.5, 0.25, 1.0):
        tag = "" if rho == 0.5 else f"_rho{rho:g}"
        add("survey_cemla" + tag, rho, lambda per: survey_theta(a, un, per, rates, cemla), False,
            f"FDIC sender rates x CEMLA (Dec-2015 survey) ${cemla:,.0f} a year per Mexico-born-headed sending unit")
        add("bea" + tag, rho, lambda per: solve_theta(a, un, per, BEA_PERSONAL_TRANSFERS, fb_units), False,
            f"units with a foreign-born member send BEA's ${BEA_PERSONAL_TRANSFERS}bn")
        for h, allowance in H2_ALLOWANCE.items():
            if h != "central" and rho != 0.5:
                continue
            name = "corridor_net_h2" + ("" if h == "central" else f"_{h}") + tag
            flow = BANXICO_US - allowance
            add(name, rho, lambda per, f=flow: solve_theta(a, un, per, f, corridor_units), True,
                f"units with a group member send Banxico's US corridor less ${allowance}bn of H-2 pay: ${flow:.3f}bn")
    add("survey_nis", 0.5, lambda per: survey_theta(a, un, per, rates, nis), False,
        f"FDIC sender rates x NIS-2003 ${nis:,.0f} a year per Mexico-born-headed sending unit")
    add("corridor_full", 0.5, lambda per: solve_theta(a, un, per, BANXICO_US, corridor_units), True,
        f"units with a group member send the whole US corridor: ${BANXICO_US:.3f}bn")
    illicit = BANXICO_US - H2_ALLOWANCE["central"] - ILLICIT_SHARE * BANXICO_US
    add("corridor_net_h2_illicit", 0.5, lambda per: solve_theta(a, un, per, illicit, corridor_units), True,
        f"corridor less H-2 pay and 7.5% illicit: ${illicit:.3f}bn")
    # Others' outflows in the central corridor case: at BEA's theta instead of the corridor's, or none.
    per = per_theta(a, un, rates, 0.5)
    specs["corridor_net_h2_others_bea"] = dict(
        per=per, theta=specs["corridor_net_h2"]["theta"], absolute=True, rho=0.5, others="bea_theta",
        theta_others=specs["bea"]["theta"], note="central corridor; units without a group member at BEA's theta")
    specs["corridor_net_h2_others_zero"] = dict(
        per=per, theta=specs["corridor_net_h2"]["theta"], absolute=True, rho=0.5, others="zero",
        note="central corridor; no outflow from units without a group member")
    return specs, {"cemla_2024_dollars": cemla, "nis_2024_dollars": nis}


def outflow_matrix(spec: dict, un: dict, rep: int) -> np.ndarray:
    """Per-unit outflow for one replicate column, honoring the others' treatment."""
    per = spec["per"]
    m = spec["theta"][rep] * per
    if spec["others"] == "bea_theta":
        m = np.where(un["any_target"], m, spec["theta_others"][rep] * per)
    elif spec["others"] == "zero":
        m = np.where(un["any_target"], m, 0.0)
    return m

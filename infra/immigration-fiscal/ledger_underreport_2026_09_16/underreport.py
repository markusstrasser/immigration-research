#!/usr/bin/env python3
"""Transfer under-reporting sensitivity for the Mexican-origin generation ledger.

Threat: Meyer, Mittag, Wu, Tatarka & Langetieg, "The Anatomy and Evolution of
Survey Error", NBER w35680 (Aug 2026), report CPS ASEC net bias exceeding 40%
for nearly half of eighteen income/transfer variables, dominated by false
negatives among respondents who report no receipt.  The generation ledger
(taxes minus reported transfers) is built on CPS ASEC 2025 reported receipt.
Does the Mexican-second-generation versus third-plus-non-Hispanic-white gap
survive scaling reported receipt to administrative totals?

Three arms, all on the same ledger and the same 160-replicate SDR variance:
  (a) proportional      -- every unit's program dollars multiplied by 1/ratio.
  (b) false-negative    -- the shortfall is assigned only to income-eligible
                           units that report NO receipt, Monte Carlo, 50 draws.
  (c) differential      -- ratios vary by the recipient's race/ethnicity, from
                           Meyer, Mittag & Wu, NBER w32860, renormalised so the
                           national aggregate still hits the same admin target.

The tax side is untouched: CPS ASEC federal, state and payroll tax are Census
MODEL output computed from reported income, not reported tax payments, and the
survey-error literature measures reported transfer receipt.  See the caveats
block in the output for what that leaves on the table.
"""
from __future__ import annotations

import os
import subprocess
import sys

if os.environ.get("_UNDERREPORT_BOOTSTRAPPED") != "1":
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        env = dict(os.environ, _UNDERREPORT_BOOTSTRAPPED="1",
                   _EXTEND_LEDGER_BOOTSTRAPPED="1")
        cmd = ["uv", "run", "--with", "numpy>=2", "--with", "pandas>=2",
               "python3", os.path.abspath(__file__), *sys.argv[1:]]
        sys.exit(subprocess.call(cmd, env=env))
os.environ["_EXTEND_LEDGER_BOOTSTRAPPED"] = "1"

import argparse  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(HERE.parent / "build"))

import analyze_cps_fiscal_2025 as base  # noqa: E402

# Fields the peer generators do not read but the eligibility screens need.
for _f in ["SPM_POVTHRESHOLD", "PRDISFLG", "WKSWORK", "PEAFEVER"]:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

import extend_ledger as ext  # noqa: E402
from analyze_cps_fiscal_2025 import CASH, NONCASH, allocate, estimate  # noqa: E402

GROUPS = ext.GROUPS
REFERENCE = ext.REFERENCE
PUPIL = ext.PUPIL_RATIO_NATIVE_ACS

# ---------------------------------------------------------------------------
# Published under-reporting ratios.  RATIO = reported survey dollars divided by
# the coverage-adjusted administrative aggregate.  A ratio below 1 means the
# survey understates.  Every number here is a published figure, not a fit.
# ---------------------------------------------------------------------------
# w35680 Table 4, "Total Net Survey Error for Dollar Amounts ... (as a % of
# Survey Targets), 2017", printed page 48 of the PDF.  Total Net Error row:
#   Pensions -44.0 | OASDI -8.1 | OASI -4.9 | DI -25.7 | SSI +1.9 | UI -42.3
#   VA Disability -38.0 | SNAP -46.9.   RATIO = 1 + TSE/100.
# w21399 Table 1 Panel A (dollars) and Panel B (months), "Proportional Bias in
# Survey Estimates of Mean Program Dollars and Months Received, by Program and
# Survey, 2000-2012", printed page 34, CPS row:
#   AFDC/TANF -0.500 | FSP/SNAP -0.417 | OASI -0.086 | SSDI -0.187 | SSI -0.162
#   UI -0.325 | WC -0.541  (Panel A, dollars)
#   NSLP -0.503 | WIC -0.341                              (Panel B, months)
RATIO_BASE = {
    "social_security": 0.919,   # w35680 T4 col (2) OASDI, -8.1%
    "ssi": 1.019,               # w35680 T4 col (5) SSI, +1.9%  (survey OVERstates)
    "cash_assistance": 0.500,   # w21399 T1 Panel A CPS AFDC/TANF, -0.500
    "unemployment": 0.577,      # w35680 T4 col (6) UI, -42.3%
    "veterans": 0.620,          # w35680 T4 col (7) VA Disability, -38.0%
    "snap": 0.531,              # w35680 T4 col (8) SNAP, -46.9%
    "energy": 1.0,              # no linked-administrative estimate exists
    "wic": 1.0,
    "school_lunch": 1.0,
    "broadband": 1.0,
}
# Aggressive variant: the four in-kind programs with no linked-admin dollar
# estimate get the best available proxy instead of being left uncorrected.
RATIO_NONCASH_EXTENDED = dict(RATIO_BASE)
RATIO_NONCASH_EXTENDED.update({
    "wic": 1.0 - 0.341,          # w21399 T1 Panel B CPS WIC months, -0.341
    "school_lunch": 1.0 - 0.503,  # w21399 T1 Panel B CPS NSLP months, -0.503
    "energy": 0.531,             # no estimate; SNAP's dollar ratio as a proxy
    "broadband": 0.531,          # no estimate; SNAP's dollar ratio as a proxy
})
# Older-vintage variant: everything from w21399 (2000-2012) instead of w35680
# (2017), to show the answer does not hinge on which vintage is believed.
RATIO_W21399 = dict(RATIO_BASE)
RATIO_W21399.update({
    "social_security": 1.0 - 0.086,   # OASI dollars
    "ssi": 1.0 - 0.162,
    "unemployment": 1.0 - 0.325,
    "snap": 1.0 - 0.417,
})
# Deliberately OUTSIDE the literature: a uniform ratio of 0.5 on every transfer
# programme, i.e. assume the CPS captures only half of every dollar of every
# transfer including Social Security, whose measured bias is 8%. This exists
# only to bound how much headroom the proportional family has at all.
RATIO_UNIFORM_HALF = {k: 0.5 for k in RATIO_BASE}

# ---------------------------------------------------------------------------
# Race/ethnicity differentials, Meyer, Mittag & Wu, "Race, Ethnicity, and
# Measurement Error", NBER w32860 (Aug 2024).
#
# Table 4, printed page 34, "Bias in Estimates of Program Receipt and Average
# Amounts for True Reporting Recipients".  Survey and admin receipt rates:
#   Shantz & Fox (2018), 2010-16 CPS
#     SNAP  receipt  white 8.5/14.6  black 21.8/38.8  hispanic 22.9/37.7
#     SNAP  amount   white 3409/3607 black 3825/4172  hispanic 3528/3638
#     TANF  receipt  white 0.9/1.2   black  4.6/7.1   hispanic  2.0/3.0
#     TANF  amount   white 2567/2196 black 3420/2640  hispanic 3006/1455
#   Meyer et al. (2023), 2011 CPS
#     UI    receipt  white 4.2/5.9   black  4.8/8.3   hispanic  3.4/6.2
#     UI    amount   white 8065/8808 black 6917/7990  hispanic 7556/8803
#
# Table 2, printed page 32, "False Negative and False Positive Rates by Race and
# Ethnicity".  Bee & Mitchell (2017), 2013 CPS, OASDI false negative rates:
#     white 6.4%  black 13.6%  hispanic 14.3%.  Used as s = 1 - false negative.
# ---------------------------------------------------------------------------
DIFF_RECEIPT = {   # extensive margin only -- the margin w35680 finds dominant
    "snap": {"white": 8.5 / 14.6, "black": 21.8 / 38.8, "hispanic": 22.9 / 37.7},
    "cash_assistance": {"white": 0.9 / 1.2, "black": 4.6 / 7.1, "hispanic": 2.0 / 3.0},
    "unemployment": {"white": 4.2 / 5.9, "black": 4.8 / 8.3, "hispanic": 3.4 / 6.2},
    "social_security": {"white": 1 - 0.064, "black": 1 - 0.136, "hispanic": 1 - 0.143},
}
DIFF_DOLLARS = {   # receipt rate times conditional amount -- an approximation
    "snap": {"white": 0.085 * 3409 / (0.146 * 3607),
             "black": 0.218 * 3825 / (0.388 * 4172),
             "hispanic": 0.229 * 3528 / (0.377 * 3638)},
    "cash_assistance": {"white": 0.009 * 2567 / (0.012 * 2196),
                        "black": 0.046 * 3420 / (0.071 * 2640),
                        "hispanic": 0.020 * 3006 / (0.030 * 1455)},
    "unemployment": {"white": 0.042 * 8065 / (0.059 * 8808),
                     "black": 0.048 * 6917 / (0.083 * 7990),
                     "hispanic": 0.034 * 7556 / (0.062 * 8803)},
    "social_security": DIFF_RECEIPT["social_security"],
}

TRANSFERS = list(CASH) + list(NONCASH)
CASH_KEYS = list(CASH)
NONCASH_KEYS = list(NONCASH)

# Income-eligibility screens for the false-negative arm.  Key -> (resource-to-
# SPM-threshold ceiling or None, categorical screen name or None).
ELIGIBILITY = {
    "snap": (2.0, None),             # gross-income tests up to 200% under BBCE
    "cash_assistance": (1.0, None),  # TANF/GA, state limits cluster near the line
    "unemployment": (None, "part_year_worker"),
    "social_security": (None, "aged62_or_disabled"),
    "veterans": (None, "veteran"),
    "ssi": (1.5, "aged65_or_disabled"),
}

N_DRAWS = 50
SEED = 20260916


def sdr(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    return float(values[0]), float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def person_ethnicity(d: pd.DataFrame) -> np.ndarray:
    """hispanic / black / white, with every other race folded into white."""
    eth = np.full(len(d), "white", dtype=object)
    eth[d.PRDTRACE.eq(2).to_numpy()] = "black"
    eth[d.PEHSPNON.eq(1).to_numpy()] = "hispanic"
    return eth


def build_state(cps_zip):
    args = argparse.Namespace(cps_zip=cps_zip)
    state = ext.build(args)
    d, index, n_units = state["d"], state["index"], state["n_units"]

    head_rows = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    state["head_rows"] = head_rows
    state["unit_weight"] = head_rows.pwwgt0.to_numpy(dtype=float)
    thresh = head_rows.SPM_POVTHRESHOLD.to_numpy(dtype=float)
    res = head_rows.SPM_RESOURCES.to_numpy(dtype=float)
    if (thresh <= 0).any():
        raise ValueError("Nonpositive SPM poverty threshold")
    state["res_ratio"] = res / thresh

    age = d.A_AGE.to_numpy()
    disabled = d.PRDISFLG.eq(1).to_numpy()
    wks = d.WKSWORK.to_numpy()
    def any_in_unit(flag):
        return np.bincount(index, weights=flag.astype(float), minlength=n_units) > 0
    state["screen"] = {
        "part_year_worker": any_in_unit((age >= 18) & (age <= 64) & (wks >= 1) & (wks <= 51)),
        "aged62_or_disabled": any_in_unit((age >= 62) | disabled),
        "aged65_or_disabled": any_in_unit((age >= 65) | disabled),
        # PEAFEVER is "ever served on active duty"; VET_YN is veterans-payment
        # RECIPIENCY, so screening on VET_YN would leave no non-reporters at all.
        "veteran": any_in_unit(d.PEAFEVER.eq(1).to_numpy()),
    }

    state["person_eth"] = person_ethnicity(d)
    state["unit_eth"] = person_ethnicity(head_rows)
    # Person-level cash dollars, so a differential ratio can follow the actual
    # recipient rather than the resource unit's head.
    state["cash_person"] = {k: d[v].to_numpy(dtype=float) for k, v in CASH.items()}
    return state


def transfer_totals_baseline(state) -> dict[str, np.ndarray]:
    return {k: state["totals"][k].copy() for k in TRANSFERS}


def proportional_arm(state, ratios) -> dict[str, np.ndarray]:
    return {k: state["totals"][k] / ratios[k] for k in TRANSFERS}


def differential_ratios(state, ratios, diff_table):
    """Per-record ratios that reproduce the national ratio in aggregate.

    r_g = r_national * s_g / c, with c = A / sum_g (A_g / s_g), so that
    sum_g A_g / r_g = A / r_national exactly.  s_g is the published
    group pattern; c only renormalises it.
    """
    index, n_units = state["index"], state["n_units"]
    w_person = state["d"].pwwgt0.to_numpy(dtype=float)
    w_unit = state["unit_weight"]
    out_person, out_unit, report = {}, {}, {}
    for key in TRANSFERS:
        s = diff_table.get(key)
        if s is None:
            continue
        if key in CASH_KEYS:
            vals, w, eth = state["cash_person"][key], w_person, state["person_eth"]
        else:
            vals, w, eth = state["totals"][key], w_unit, state["unit_eth"]
        agg = float((vals * w).sum())
        denom = 0.0
        for g, s_g in s.items():
            m = eth == g
            denom += float((vals[m] * w[m]).sum()) / s_g
        c = agg / denom
        r_rec = np.array([ratios[key] * s[g] / c for g in eth], dtype=float)
        if key in CASH_KEYS:
            out_person[key] = r_rec
        else:
            out_unit[key] = r_rec
        report[key] = {g: ratios[key] * s[g] / c for g in s}
    totals = {}
    for key in TRANSFERS:
        if key in out_person:
            scaled = state["cash_person"][key] / out_person[key]
            totals[key] = np.bincount(index, weights=scaled, minlength=n_units)
        elif key in out_unit:
            totals[key] = state["totals"][key] / out_unit[key]
        else:
            totals[key] = state["totals"][key] / ratios[key]
    return totals, report


def false_negative_plan(state, ratios):
    """Per-program: eligible non-reporting units, selection probability, amount."""
    w = state["unit_weight"]
    plan, notes = {}, []
    for key in TRANSFERS:
        r = ratios[key]
        total = state["totals"][key]
        reporting = total > 0
        agg = float((total * w).sum())
        if r >= 1.0 or agg <= 0:
            notes.append(f"{key:18s} ratio {r:5.3f}  no false-negative assignment "
                         f"({'survey overstates' if r >= 1 else 'no reported dollars'})")
            continue
        shortfall = agg * (1.0 / r - 1.0)
        mean_amount = agg / float(w[reporting].sum())
        ceiling, screen = ELIGIBILITY.get(key, (None, None))
        eligible = ~reporting
        if ceiling is not None:
            eligible &= state["res_ratio"] <= ceiling
        if screen is not None:
            eligible &= state["screen"][screen]
        pool = float(w[eligible].sum())
        if pool <= 0:
            notes.append(f"{key:18s} [DEGRADED] no eligible non-reporting units")
            continue
        needed = shortfall / mean_amount
        prob = needed / pool
        capped = min(prob, 1.0)
        residual = 0.0 if prob <= 1.0 else (prob - 1.0) * pool * mean_amount
        plan[key] = {"eligible": eligible, "prob": capped, "amount": mean_amount,
                     "shortfall": shortfall, "pool": pool, "needed": needed,
                     "residual": residual}
        tag = "" if prob <= 1.0 else f"  [DEGRADED] probability {prob:.2f} capped at 1.0, " \
                                     f"${residual / 1e9:,.1f}B of the shortfall unassignable"
        notes.append(f"{key:18s} ratio {r:5.3f}  shortfall ${shortfall / 1e9:8,.1f}B  "
                     f"mean unit benefit ${mean_amount:8,.0f}  eligible non-reporting units "
                     f"{pool / 1e6:6,.1f}M  p={capped:.4f}{tag}")
    return plan, notes


def draw_false_negative(state, plan, rng) -> dict[str, np.ndarray]:
    totals = transfer_totals_baseline(state)
    for key, p in plan.items():
        hit = p["eligible"] & (rng.random(state["n_units"]) < p["prob"])
        totals[key] = totals[key] + hit * p["amount"]
    return totals


class Ledger:
    """Everything that does not move across arms, allocated once."""

    def __init__(self, state, allocation):
        index, n_units = state["index"], state["n_units"]
        eligible = state["allocations"][allocation]
        t = state["totals"]
        a = lambda k: allocate(t[k], index, eligible, n_units)  # noqa: E731
        self.state, self.allocation = state, allocation
        self.index, self.n_units, self.eligible = index, n_units, eligible
        self.tax = a("modeled_tax_total")
        self.extra = (a("employer_payroll") + a("sales_tax_share35")
                      + a("property_tax_owner") - PUPIL * a("k12_cost_at_full_attendance"))

    def metrics(self, transfer_totals):
        total = sum(transfer_totals[k] for k in TRANSFERS)
        t = allocate(total, self.index, self.eligible, self.n_units)
        return {"taxes_minus_transfers": self.tax - t,
                "extended_balance": self.tax + self.extra - t}


def evaluate(ledger, state, transfer_totals):
    adults, weights = state["adults_25_64"], state["person_weights"]
    per = ledger.metrics(transfer_totals)
    rep = {}
    for g, mask in state["group"].items():
        use = adults & mask
        w = weights[use]
        for metric, arr in per.items():
            rep[g, metric] = estimate(arr[use][None, :], w)[0]
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cps-zip", type=Path, default=None)
    ap.add_argument("--draws", type=int, default=N_DRAWS)
    args = ap.parse_args()

    cps = ext.resolve_cps_zip(args.cps_zip)
    print(f"[stage] CPS ASEC 2025 source: {cps}", flush=True)
    state = build_state(cps)

    lines: list[str] = []

    def out(text=""):
        print(text)
        lines.append(text)

    out("Transfer under-reporting sensitivity of the origin-generation fiscal ledger")
    out("CPS ASEC 2025 (income year 2024), SPM resource units, person weights,")
    out("160-replicate SDR standard errors, adults 25-64, civilian household members.")
    out(f"CPS source: {cps}")
    out("")
    out("[DATA] CPS ASEC 2025 public-use microdata.")
    out("[SOURCE: https://www.nber.org/papers/w35680] Meyer, Mittag, Wu, Tatarka & Langetieg,")
    out("        The Anatomy and Evolution of Survey Error, NBER w35680, August 2026.")
    out("[SOURCE: https://www.nber.org/papers/w32860] Meyer, Mittag & Wu, Race, Ethnicity, and")
    out("        Measurement Error, NBER w32860, August 2024.")
    out("[SOURCE: https://www.nber.org/papers/w21399] Meyer, Mok & Sullivan, Household Surveys")
    out("        in Crisis, NBER w21399, 2015 (JEP 29(4):199-226).")
    out("[INFERENCE] every arm below is an accounting scenario, not a measurement.")

    # ---- baseline / gate A ------------------------------------------------
    ledgers = {alloc: Ledger(state, alloc) for alloc in state["allocations"]}
    baseline_totals = transfer_totals_baseline(state)
    baseline = {alloc: evaluate(ledgers[alloc], state, baseline_totals) for alloc in ledgers}

    gate = sdr(baseline["equal_all_members"]["mexican_second_gen", "extended_balance"]
               - baseline["equal_all_members"][REFERENCE, "extended_balance"])
    gate_b = sdr(baseline["equal_all_members"]["mexican_second_gen", "taxes_minus_transfers"]
                 - baseline["equal_all_members"][REFERENCE, "taxes_minus_transfers"])
    out("")
    out("-- GATE A: reproduce the peer lane's extended ledger before touching anything --")
    out(f"   extended balance gap, equal_all_members : {gate[0]:,.0f} (se {gate[1]:,.0f})"
        f"   expected -8,286 (se 443)   deviation {gate[0] - (-8286):+,.2f}")
    out(f"   taxes-minus-transfers gap, same          : {gate_b[0]:,.0f} (se {gate_b[1]:,.0f})"
        f"   expected -6,066 (se 353)   deviation {gate_b[0] - (-6066):+,.2f}")
    gate_ok = abs(gate[0] - (-8286)) <= 50
    out(f"   [gate A] {'PASS' if gate_ok else 'FAIL'} (within $50 of -8,286)")
    if not gate_ok:
        raise SystemExit("[BLOCKED] gate A failed; refusing to report sensitivity arms")

    # ---- ratios in force --------------------------------------------------
    out("")
    out("-- under-reporting ratios applied (reported survey dollars / administrative target) --")
    out(f"{'ledger program':20s}{'CPS field':18s}{'base':>8s}{'noncash-ext':>13s}"
        f"{'w21399':>9s}   source of the base ratio")
    src = {
        "social_security": "w35680 Table 4 col (2) OASDI, p.48: -8.1%",
        "ssi": "w35680 Table 4 col (5) SSI, p.48: +1.9%",
        "cash_assistance": "w21399 Table 1 Panel A CPS AFDC/TANF, p.34: -0.500",
        "unemployment": "w35680 Table 4 col (6) UI, p.48: -42.3%",
        "veterans": "w35680 Table 4 col (7) VA Disability, p.48: -38.0%",
        "snap": "w35680 Table 4 col (8) SNAP, p.48: -46.9%",
        "energy": "no linked-administrative estimate published",
        "wic": "no dollar estimate; months only (w21399 T1 Panel B)",
        "school_lunch": "no dollar estimate; months only (w21399 T1 Panel B)",
        "broadband": "program began 2021; no estimate published",
    }
    fields = dict(CASH) | dict(NONCASH)
    for k in TRANSFERS:
        out(f"{k:20s}{fields[k]:18s}{RATIO_BASE[k]:8.3f}{RATIO_NONCASH_EXTENDED[k]:13.3f}"
            f"{RATIO_W21399[k]:9.3f}   {src[k]}")

    rows = []

    def record(arm, allocation, rep, sd_map=None, extra=None):
        for g in GROUPS:
            for metric in ("taxes_minus_transfers", "extended_balance"):
                est, se = sdr(rep[g, metric])
                diff = rep[g, metric] - rep[REFERENCE, metric]
                dest, dse = sdr(diff)
                rows.append({"arm": arm, "allocation": allocation, "group": g,
                             "metric": metric, "estimate": est, "se_sdr": se,
                             "difference_from_third_plus_nh_white": dest,
                             "se_sdr_difference": dse,
                             "mc_sd_of_difference": (sd_map or {}).get((g, metric), ""),
                             "note": (extra or "")})

    record("baseline_reported", "equal_all_members", baseline["equal_all_members"])
    record("baseline_reported", "equal_adults_18plus", baseline["equal_adults_18plus"])

    # ---- arm (a) proportional --------------------------------------------
    prop_sets = {
        "a_proportional_base": RATIO_BASE,
        "a_proportional_noncash_extended": RATIO_NONCASH_EXTENDED,
        "a_proportional_w21399_vintage": RATIO_W21399,
        "a_bound_uniform_half_NOT_A_LITERATURE_VALUE": RATIO_UNIFORM_HALF,
    }
    results = {}
    for name, ratios in prop_sets.items():
        tot = proportional_arm(state, ratios)
        for alloc, ld in ledgers.items():
            rep = evaluate(ld, state, tot)
            results[name, alloc] = rep
            record(name, alloc, rep)

    # ---- arm (c) differential --------------------------------------------
    diff_sets = {
        "c_differential_receipt_rates": (RATIO_BASE, DIFF_RECEIPT),
        "c_differential_dollar_ratios": (RATIO_BASE, DIFF_DOLLARS),
    }
    diff_reports = {}
    for name, (ratios, table) in diff_sets.items():
        tot, rep_ratios = differential_ratios(state, ratios, table)
        diff_reports[name] = rep_ratios
        for alloc, ld in ledgers.items():
            rep = evaluate(ld, state, tot)
            results[name, alloc] = rep
            record(name, alloc, rep)

    # ---- arm (b) false-negative Monte Carlo -------------------------------
    plan, notes = false_negative_plan(state, RATIO_BASE)
    out("")
    out("-- arm (b) false-negative allocation plan (eligible non-reporting units only) --")
    for n in notes:
        out("   " + n)

    rng = np.random.default_rng(SEED)
    draws: dict[tuple[str, str, str], list[np.ndarray]] = {}
    for _ in range(args.draws):
        tot = draw_false_negative(state, plan, rng)
        for alloc, ld in ledgers.items():
            rep = evaluate(ld, state, tot)
            for key, val in rep.items():
                draws.setdefault((alloc, *key), []).append(val)
    mc = {}
    mc_sd = {}
    for (alloc, g, metric), vals in draws.items():
        stack = np.stack(vals)
        mc[alloc] = mc.get(alloc, {})
        mc[alloc][g, metric] = stack.mean(axis=0)
        mc_sd[alloc] = mc_sd.get(alloc, {})
        mc_sd[alloc][g, metric] = float(stack[:, 0].std(ddof=1))
    mc_gap_sd = {}
    for alloc in ledgers:
        gap_sd = {}
        for g in GROUPS:
            for metric in ("taxes_minus_transfers", "extended_balance"):
                per_draw = np.array([draws[alloc, g, metric][i][0]
                                     - draws[alloc, REFERENCE, metric][i][0]
                                     for i in range(args.draws)])
                gap_sd[g, metric] = float(per_draw.std(ddof=1))
        mc_gap_sd[alloc] = gap_sd
        results["b_false_negative_mc", alloc] = mc[alloc]
        record("b_false_negative_mc", alloc, mc[alloc], sd_map=gap_sd,
               extra=f"mean of {args.draws} Monte Carlo draws, seed {SEED}")

    # ---- headline table ---------------------------------------------------
    order = ["baseline_reported", "a_proportional_base", "a_proportional_noncash_extended",
             "a_proportional_w21399_vintage", "b_false_negative_mc",
             "c_differential_receipt_rates", "c_differential_dollar_ratios",
             "a_bound_uniform_half_NOT_A_LITERATURE_VALUE"]
    all_results = {("baseline_reported", a): baseline[a] for a in ledgers}
    all_results.update(results)

    for metric, label in (("taxes_minus_transfers", "TAXES MINUS SELECTED TRANSFERS"),
                          ("extended_balance", "EXTENDED BALANCE")):
        out("")
        out("=" * 118)
        out(f"== {label}: Mexican 2nd gen minus 3rd+ NH white, annual $ per adult 25-64 ==")
        out("=" * 118)
        out(f"{'arm':44s}{'equal_all_members':>26s}{'move':>10s}"
            f"{'equal_adults_18plus':>26s}{'move':>10s}")
        for arm in order:
            cells = ""
            for alloc in ("equal_all_members", "equal_adults_18plus"):
                rep = all_results[arm, alloc]
                d = rep["mexican_second_gen", metric] - rep[REFERENCE, metric]
                est, se = sdr(d)
                b = baseline[alloc]
                bd = sdr(b["mexican_second_gen", metric] - b[REFERENCE, metric])[0]
                cells += f"{f'{est:,.0f} ({se:,.0f})':>26s}"
                cells += ("—".rjust(10) if arm == "baseline_reported"
                          else f"{est - bd:>+10,.0f}")
            out(f"{arm:44s}{cells}")
            if arm == "b_false_negative_mc":
                sds = "  ".join(
                    f"{a} {mc_gap_sd[a]['mexican_second_gen', metric]:,.0f}"
                    for a in ("equal_all_members", "equal_adults_18plus"))
                out(f"{'':44s}(Monte Carlo sd of the gap across "
                    f"{args.draws} draws: {sds})")

    out("")
    out("-- group levels under the base proportional arm, equal_all_members --")
    out(f"{'group':30s}{'transfers, reported':>22s}{'transfers, scaled':>20s}"
        f"{'extended balance':>20s}{'vs reported':>14s}")
    base_tot = transfer_totals_baseline(state)
    scaled_tot = proportional_arm(state, RATIO_BASE)
    ld = ledgers["equal_all_members"]
    tr_rep = allocate(sum(base_tot[k] for k in TRANSFERS), ld.index, ld.eligible, ld.n_units)
    tr_sca = allocate(sum(scaled_tot[k] for k in TRANSFERS), ld.index, ld.eligible, ld.n_units)
    for g in GROUPS:
        use = state["adults_25_64"] & state["group"][g]
        w = state["person_weights"][use]
        a = sdr(estimate(tr_rep[use][None, :], w)[0])[0]
        b = sdr(estimate(tr_sca[use][None, :], w)[0])[0]
        eb = sdr(results["a_proportional_base", "equal_all_members"][g, "extended_balance"])[0]
        eb0 = sdr(baseline["equal_all_members"][g, "extended_balance"])[0]
        out(f"{g:30s}{a:>22,.0f}{b:>20,.0f}{eb:>20,.0f}{eb - eb0:>+14,.0f}")

    out("")
    out("-- arm (c) renormalised per-group ratios actually applied --")
    for name, rep_ratios in diff_reports.items():
        out(f"   {name}")
        for key, gr in rep_ratios.items():
            out("      " + f"{key:18s}" + "  ".join(f"{g}={v:.3f}" for g, v in gr.items()))

    out("")
    out("-- what is NOT corrected, and which way each omission cuts --")
    out("   1. The tax side is untouched. CPS ASEC FEDTAX_AC, STATETAX_A and FICA are Census")
    out("      MODEL output computed from reported income, not reported tax payments, so the")
    out("      survey-error literature on reported receipt does not apply to them. EITC and")
    out("      ACTC sit inside FEDTAX_AC and are likewise modeled, not reported.")
    out("   2. Because the arms add transfer dollars without re-running the tax model, they")
    out("      omit the tax that the added receipt would generate. UI is fully taxable and up")
    out("      to 85% of Social Security is taxable. Adding those dollars back would raise")
    out("      modeled tax more for the group receiving more of them, which is the white")
    out("      reference group. Correcting this would push the gap further NEGATIVE, i.e. the")
    out("      arms as run are biased toward the gap-narrowing direction.")
    out("   3. Earnings under-reporting is not addressed. w35680 covers transfer and pension")
    out("      receipt, not wage and salary income.")
    out("   4. Medicaid and housing assistance carry no dollar value in this ledger at all,")
    out("      so their (large) under-reporting cannot move it.")
    out("   5. Sampling error only. The SDR standard errors cover CPS sampling. They do not")
    out("      cover error in the published ratios, nor the transport of national ratios onto")
    out("      individual resource units.")

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "underreport_arms.csv", index=False)
    (HERE / "underreport_result.txt").write_text("\n".join(lines) + "\n")
    print(f"\nWrote {HERE / 'underreport_arms.csv'}")
    print(f"Wrote {HERE / 'underreport_result.txt'}")


if __name__ == "__main__":
    main()

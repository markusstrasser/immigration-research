#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2", "pandas>=2"]
# ///
"""Separate fiscal missingness, collection/credit assumptions and crime ascertainment.

Native-First: CSV/JSON inputs from verified analyses; algebraic grids and tipping
points. Scenario grids are stress assumptions, never fitted probabilities or CIs.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


def corrected_mean(observed: float, missing_share_true: float, missing_mean: float) -> float:
    if not 0 <= missing_share_true <= 1:
        raise ValueError("Missing fraction must be a share of the true population in [0,1]")
    return (1 - missing_share_true) * observed + missing_share_true * missing_mean


def required_missing_mean(observed: float, target: float, missing_share_true: float) -> float:
    if not 0 < missing_share_true <= 1:
        raise ValueError("A tipping mean needs a nonzero missing share")
    return (target - (1 - missing_share_true) * observed) / missing_share_true


def true_rate_ratio(observed_ratio: float, relative_denominator_factor: float,
                    relative_ascertainment: float) -> float:
    """D_published/D_true for U relative to N; recorded events/true events U/N."""
    if min(relative_denominator_factor, relative_ascertainment) <= 0 or observed_ratio < 0:
        raise ValueError("Positive ascertainment/denominator factors and nonnegative rate required")
    return observed_ratio * relative_denominator_factor / relative_ascertainment


def run(args):
    args.output.mkdir(parents=True, exist_ok=True)
    accounts = pd.read_csv(args.fiscal / "accounts.csv")
    gaps = pd.read_csv(args.fiscal / "contrasts.csv")
    schools = pd.read_csv(args.schools / "school_exposure.csv")
    school_gaps = pd.read_csv(args.schools / "school_exposure_contrasts.csv")
    # School transport uses the explicitly person-weighted allocation on both sides.
    a = accounts.loc[accounts.weighting.eq("person")].set_index(["allocation", "group", "metric"])
    s = schools.set_index(["allocation", "group", "metric"])
    rows, missing, collection, two_sided = [], [], [], []
    for allocation, health, school_case in itertools.product(
        ["equal_all_members", "equal_adults_18plus"], ["age_birth", "age_birth_insurance"],
        [("not_added", 0)] + [("includes_food", c) for c in [0, 5000, 10000, 17619, 25000]],
    ):
        school_accounting, cost = school_case
        metric = ("balance_after_health_" if school_accounting == "not_added"
                  else "balance_excluding_school_lunch_after_health_") + health
        net = {}
        for group in ["all_native", "mexico_born"]:
            before = float(a.loc[(allocation, group, metric), "estimate"])
            exposure = float(s.loc[(allocation, group, "pupil"), "estimate"])
            net[group] = before - cost * exposure
            rows.append({"allocation": allocation, "health_transport": health,
                         "school_accounting": school_accounting, "base_metric": metric,
                         "school_cost_assumption_per_pupil": cost, "group": group,
                         "balance_before_school": before, "allocated_public_pupils": exposure,
                         "school_scenario_cost": cost * exposure, "conditional_balance": net[group],
                         "net_sign_school_cost_threshold": before / exposure if school_accounting == "includes_food" else np.nan})
        # Point ranges across constructions are distinct from conditional sampling intervals.
        gap = gaps.loc[gaps.allocation.eq(allocation) & gaps.weighting.eq("person") &
                       gaps.metric.eq(metric)].iloc[0]
        sg = school_gaps.loc[school_gaps.allocation.eq(allocation) & school_gaps.metric.eq("pupil")].iloc[0]
        gap_value = net["all_native"] - net["mexico_born"]
        se = float(np.sqrt(gap.se_sampling_cps_and_meps ** 2 + cost ** 2 * sg.se_sampling ** 2))
        rows.append({"allocation": allocation, "health_transport": health,
                     "school_accounting": school_accounting, "base_metric": metric,
                     "school_cost_assumption_per_pupil": cost, "group": "native_minus_mexico",
                     "conditional_balance": gap_value, "se_sampling_three_surveys": se,
                     "ci95_sampling_low": gap_value - 1.96 * se, "ci95_sampling_high": gap_value + 1.96 * se})
        if school_accounting == "not_added" or cost == 17619:
            for q in [.05, .10, .20]:
                threshold = required_missing_mean(net["mexico_born"], net["all_native"], q)
                missing.append({"allocation": allocation, "health_transport": health,
                    "school_accounting": school_accounting,
                    "school_cost_assumption_per_pupil": cost, "missing_share_true_mexico_population": q,
                    "observed_mexico_balance": net["mexico_born"], "native_balance_held_fixed": net["all_native"],
                    "missing_mexico_mean_needed_to_equal_native": threshold,
                    "if_missing_mean_minus10000": corrected_mean(net["mexico_born"], q, -10000),
                    "if_missing_mean_zero": corrected_mean(net["mexico_born"], q, 0),
                    "scope": "Incremental residual missingness after survey weights; not an estimate of undocumented share"})
        # Broad group-wide stress; never label these fractions as estimates for unauthorized people.
        if allocation == "equal_adults_18plus" and health == "age_birth_insurance" and (school_accounting == "not_added" or cost == 17619):
            for qn, qm, mn, mm in itertools.product([0, .05, .10], [0, .05, .10, .20],
                                                   [-10000, 0, 20000], [-10000, 0, 20000]):
                ntrue = corrected_mean(net["all_native"], qn, mn)
                mtrue = corrected_mean(net["mexico_born"], qm, mm)
                two_sided.append({"school_accounting": school_accounting,
                    "school_cost_assumption_per_pupil": cost,
                    "missing_share_true_native": qn, "missing_share_true_mexico": qm,
                    "missing_native_mean_assumption": mn, "missing_mexico_mean_assumption": mm,
                    "corrected_native_balance": ntrue, "corrected_mexico_balance": mtrue,
                    "native_minus_mexico": ntrue - mtrue,
                    "scope": "Two-sided residual coverage/selection stress; parameters are assumptions, not fitted bounds"})
            for native_c, mexico_c, refund_receipt in itertools.product([.9, 1], [.5, .75, 1], [0, .5, 1]):
                adjusted = {}
                for group, c in [("all_native", native_c), ("mexico_born", mexico_c)]:
                    positive = float(a.loc[(allocation, group, "modeled_positive_liability"), "estimate"])
                    refund = float(a.loc[(allocation, group, "modeled_refund_amount"), "estimate"])
                    adjusted[group] = net[group] - (1-c)*positive + (1-refund_receipt)*refund
                collection.append({"school_cost_assumption_per_pupil": cost,
                    "school_accounting": school_accounting,
                    "native_liability_collection_factor": native_c, "mexico_liability_collection_factor": mexico_c,
                    "refund_receipt_factor_both_groups": refund_receipt,
                    "native_balance": adjusted["all_native"], "mexico_balance": adjusted["mexico_born"],
                    "native_minus_mexico": adjusted["all_native"] - adjusted["mexico_born"]})
    tx = pd.read_csv(args.tx_comparisons)
    chosen = tx.loc[tx.year.eq(2018) & tx.crime_category.eq("violent") & tx.denom_source.eq("CMS") & tx.status_class.eq("unauthorized")]
    if len(chosen) != 1:
        raise ValueError("Need exactly one source-defined Texas2018 CMS unauthorized violent comparison")
    obs = float(chosen.iloc[0].ratio_to_native_born)
    crime = [{"source_observed_ratio": obs, "relative_denominator_factor": d,
              "relative_ascertainment_U_over_N": p, "conditional_true_ratio": true_rate_ratio(obs, d, p),
              "ascertainment_ratio_at_equality": obs*d}
             for d, p in itertools.product([.8, 1, 1.2], [.25, .4, .5, .75, 1])]
    for name, data in [("fiscal_school_scenarios", rows), ("missing_population_tipping_points", missing),
                       ("two_sided_population_stress", two_sided),
                       ("collection_credit_stress", collection), ("crime_ascertainment_stress", crime)]:
        pd.DataFrame(data).to_csv(args.output / f"{name}.csv", index=False)
    sources = [args.fiscal / "accounts.csv", args.fiscal / "contrasts.csv",
               args.schools / "school_exposure.csv", args.schools / "school_exposure_contrasts.csv", args.tx_comparisons]
    meta = {"sources": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
        "stress_not_probability": True, "school_average_anchor": {"amount": 17619, "year": "FY2024",
            "source": "https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html"},
        "school_food_overlap": "not_added retains SPM lunch in the original transfer ledger. includes_food removes SPM lunch before subtracting total school spending, which includes food services. Private-school and out-of-age-domain lunch is therefore omitted in the combined construction, not claimed to be an exact matched offset. A zero school cost under includes_food is a distinct scenario from not_added.",
        "fiscal_limits": "Calendar2024 CPS/MEPS plus ACS2024 household school exposure; survey populations/weights and clocks differ. Transport is an accounting assumption; no full fiscal or causal sign. Partial collection and refunds varied separately, with cash/service use held fixed.",
        "sampling": "Three-survey first-order variances treated independent conditional on cost/allocation/transport; systematic errors excluded.",
        "crime_limits": "Texas2018 recorded violent arrest-charge ratio, not2022–26 or conviction rate. Denominator factor means published/true U relative to native; ascertainment is effective recorded-event intensity U/native. Prosecutor declination is downstream of the arrest measure. No empirical detection probabilities estimated.",
        "unknown_unknowns": "No invented probability distribution. Use explicit unidentified-loss tipping points, external reconciliation and dated falsifiers; stress ranges do not exhaust possibilities."}
    (args.output / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(pd.DataFrame(rows).query("school_cost_assumption_per_pupil==17619")[["allocation", "health_transport", "group", "conditional_balance"]].to_string(index=False))
    print(json.dumps({"tx_observed_ratio": obs, "equal_denominator_ascertainment_tipping_ratio": obs}))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fiscal", type=Path, required=True)
    p.add_argument("--schools", type=Path, required=True)
    p.add_argument("--tx-comparisons", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    run(p.parse_args())

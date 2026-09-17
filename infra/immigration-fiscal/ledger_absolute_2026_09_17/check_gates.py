#!/usr/bin/env python3
"""Re-read `derived/` and re-test every gate the builder claims to have passed.

Reads only the written artefacts, never the CPS microdata, so a stale or
hand-edited output cannot pass. Exits non-zero on any failed gate.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ledger_absolute_2026_09_17/check_gates.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DER = HERE / "derived"
ALL_AGE = HERE.parent / "all_age_ledger_2026_09_17"
UNION = "mexican_observed_total"
TARGETS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]

results: list[tuple[str, bool, str]] = []


def gate(name: str, passed: bool, detail: str = "") -> None:
    results.append((name, bool(passed), detail))


def main() -> int:
    for required in ["items_by_group.csv", "waterfall.csv", "arms_matrix.csv",
                     "marginality_curve.csv", "complete_gaps.csv",
                     "complete_gaps_by_item.csv", "national_reconciliation.csv", "audit.json"]:
        if not (DER / required).exists():
            gate(f"artefact_present:{required}", False, "missing")
            report()
            return 1
        gate(f"artefact_present:{required}", True)

    audit = json.loads((DER / "audit.json").read_text())
    items = pd.read_csv(DER / "items_by_group.csv")
    water = pd.read_csv(DER / "waterfall.csv")
    arms = pd.read_csv(DER / "arms_matrix.csv")
    curve = pd.read_csv(DER / "marginality_curve.csv")
    gaps = pd.read_csv(DER / "complete_gaps.csv")
    gap_items = pd.read_csv(DER / "complete_gaps_by_item.csv")
    nat = pd.read_csv(DER / "national_reconciliation.csv")

    # --- gate 0: the upstream union absolute -------------------------------
    g0 = audit["gate0"]
    stored = pd.read_csv(ALL_AGE / "derived/estimates.csv")
    row = stored[(stored.scenario == "all_age_shared") & (stored.target == UNION)
                 & (stored.metric == "absolute_total")]
    live_stored = float(row.estimate.iloc[0])
    gate("gate0_passed", bool(g0["passed"]) and abs(float(g0["residual"])) <= 1.0,
         f"residual ${float(g0['residual']):,.2f}")
    gate("gate0_matches_live_upstream_estimate",
         abs(float(g0["stored"]) - live_stored) <= 1.0,
         f"audit {float(g0['stored']):,.0f} vs upstream {live_stored:,.0f}")
    base = water[(water.group == UNION) & (water.item == "base")]
    gate("waterfall_starts_at_the_gated_absolute",
         abs(float(base.cumulative_bn.iloc[0]) * 1e9 - live_stored) <= 1.0,
         f"{float(base.cumulative_bn.iloc[0]):+.5f}bn")

    # --- parameter discipline ---------------------------------------------
    used = audit.get("params_used", {})
    not_verified = {k: v.get("status") for k, v in used.items()
                    if str(v.get("status", "")).lower() != "verified"}
    if audit.get("params_allow_placeholder"):
        gate("parameters_all_verified", False,
             f"run used --allow-placeholder; {len(used)} parameters consumed without verification")
    else:
        gate("parameters_all_verified", not not_verified,
             "all consumed parameters are verified" if not not_verified else str(not_verified))

    # --- reconciliation and cancellation -----------------------------------
    recon = audit["national_reconciliation"]
    gate("national_total_reconciliation", all(r["ok"] for r in recon),
         "; ".join(f"{r['charge']}={r['ratio']:.4f}" for r in recon))
    ratio = float(audit["population_ratio"])
    flat = [r for r in recon if r["kind"] == "flat_per_capita"]
    gate("flat_items_reconcile_to_the_population_ratio",
         all(abs(float(r["ratio"]) - ratio) < 1e-9 for r in flat),
         f"population ratio {ratio:.5f} over {len(flat)} flat items")
    cancel = audit["common_charge_cancellation"]
    gate("common_charge_cancellation", all(v["passed"] for v in cancel.values()),
         "; ".join(f"{k}={v['relative']:.2e}" for k, v in cancel.items()) or "no flat item")
    gate("replicate_se_finite", bool(audit["replicate_se_finite"]))
    sibling = audit.get("sibling_lane_crosschecks", [])
    gate("reused_constructions_match_their_source_lane",
         bool(sibling) and all(c["passed"] for c in sibling),
         "; ".join(f"{c['check'].split('_vs_')[0]}={c['value']:,.0f}" for c in sibling)
         or "no cross-check recorded")
    inv = audit.get("admin_over_survey_inversion_check", [])
    gate("admin_survey_ratios_are_the_reciprocal_of_the_published_coverage_ratios",
         bool(inv) and all(r["agree"] for r in inv),
         "; ".join(f"{r['program']} 1/{r['published_coverage_ratio']}="
                   f"{r['parameter_admin_over_survey']}" for r in inv) or "none checked")
    omb_cc = audit.get("omb_cache_vs_params", [])
    gate("omb_cache_agrees_with_the_fetched_parameters",
         all(r["agree"] for r in omb_cc),
         f"{len(omb_cc)} functions compared")

    # --- internal consistency of the written tables ------------------------
    numeric = items.select_dtypes(include=[np.number])
    gate("items_table_finite", bool(np.isfinite(numeric.to_numpy()).all()),
         f"{len(items)} rows")
    union_rows = items[items.group == UNION].set_index(["item", "arm"])
    parts = items[items.group.isin(TARGETS)].groupby(["item", "arm"]).total_bn.sum()
    diffs = (union_rows.total_bn - parts).abs()
    gate("union_equals_the_sum_of_the_three_targets", bool((diffs < 1e-6).all()),
         f"max |union - sum of parts| = {float(diffs.max()):.3e} bn")

    steps_ok, step_detail = True, []
    for group, block in water.groupby("group"):
        block = block.sort_values("step")
        cum = block.cumulative_bn.to_numpy()
        delta = np.diff(cum)
        declared = block.item_bn.to_numpy()[1:]
        if not np.allclose(delta, declared, atol=1e-6):
            steps_ok = False
            step_detail.append(f"{group}: max {np.abs(delta - declared).max():.3e}")
    gate("waterfall_steps_add_up", steps_ok, "; ".join(step_detail) or "every step matches")

    ends = water.sort_values("step").groupby("group").tail(1).set_index("group")
    union_end = float(ends.loc[UNION, "cumulative_bn"])
    parts_end = sum(float(ends.loc[g, "cumulative_bn"]) for g in TARGETS)
    gate("waterfall_endpoint_is_additive", abs(union_end - parts_end) < 1e-6,
         f"union {union_end:+.4f}bn vs parts {parts_end:+.4f}bn")

    centrals = audit["central_arms"]
    want = {"F_arm": centrals.get("F"), "E_arm": centrals.get("E"),
            "C_arm": centrals.get("C"), "R_arm": centrals.get("R")}
    mask = np.ones(len(arms), bool)
    for col, value in want.items():
        mask &= (arms[col].isna() if value is None else arms[col].eq(value)).to_numpy()
    if mask.sum() == 1:
        gate("arms_matrix_contains_the_waterfall_endpoint",
             abs(float(arms.loc[mask, "union_absolute_bn"].iloc[0]) - union_end) < 1e-6,
             f"{float(arms.loc[mask, 'union_absolute_bn'].iloc[0]):+.4f}bn vs {union_end:+.4f}bn")
    else:
        gate("arms_matrix_contains_the_waterfall_endpoint", False,
             f"{int(mask.sum())} rows match the central combination {want}")
    expected = 1
    for col in ["F_arm", "E_arm", "C_arm", "R_arm"]:
        expected *= max(arms[col].nunique(dropna=False), 1)
    gate("arms_matrix_is_the_full_grid", len(arms) == expected,
         f"{len(arms)} rows, grid {expected}")

    # --- complete-account gaps ----------------------------------------------
    anchor = audit.get("upstream_partial_gap_anchor", [])
    gate("partial_gaps_reproduce_the_upstream_estimates",
         bool(anchor) and all(a["agree"] for a in anchor),
         f"{len(anchor)} common-age gaps checked against estimates.csv")
    add_ok, add_detail = True, []
    for _, row in gaps.iterrows():
        block = gap_items[(gap_items.group == row.group) & (gap_items.reference == row.reference)]
        for base_col, complete_col, item_col in [
                ("base_common_age_gap_per_person", "complete_common_age_gap_per_person",
                 "common_age_gap_per_person"),
                ("base_age_matched_gap_bn", "complete_age_matched_gap_bn", "age_matched_gap_bn")]:
            rebuilt = row[base_col] + block[item_col].sum()
            if abs(rebuilt - row[complete_col]) > 1e-6 * max(abs(row[complete_col]), 1.0):
                add_ok = False
                add_detail.append(f"{row.group}/{row.reference}/{item_col}")
    gate("complete_gaps_are_the_base_plus_the_item_contributions", add_ok,
         "; ".join(add_detail) or f"{len(gaps)} group-reference pairs add up")
    gate("complete_gaps_cover_both_references",
         set(gaps.reference) == {"third_plus_nh_white", "all_native"} and len(gaps) == 8,
         f"{len(gaps)} rows over {sorted(set(gaps.reference))}")

    # --- national reconciliation ---------------------------------------------
    nr = audit.get("national_reconciliation_vs_consolidated_budget", {})
    account_lines = nat[nat.block == "account"].amount_bn.sum()
    gate("national_account_lines_sum_to_the_reported_position",
         abs(account_lines * 1e9 - float(nr.get("account_position", 0))) < 1e3,
         f"lines {account_lines:+,.1f}bn vs reported {float(nr.get('account_position', 0))/1e9:+,.1f}bn")
    reported_residual = float(nr.get("residual_unpriced_or_coverage", float("nan")))
    gate("national_residual_is_reported_and_finite", np.isfinite(reported_residual),
         f"residual {reported_residual/1e9:+,.1f}bn, outlay coverage "
         f"{float(nr.get('outlay_coverage', 0)):.3f}, receipt coverage "
         f"{float(nr.get('receipt_coverage', 0)):.3f}")
    gate("national_residual_is_a_real_unforced_quantity", abs(reported_residual) > 1e9,
         "the residual is reported, never solved for; a residual near zero would mean it "
         "had been forced")

    # --- the brief's step-12 endpoint stays visible --------------------------
    brief_step = int(audit.get("brief_final_step", 12))
    step12 = water[(water.group == UNION) & (water.step == brief_step)]
    gate("brief_final_step_endpoint_still_reported", len(step12) == 1,
         f"step {brief_step} cumulative {float(step12.cumulative_bn.iloc[0]):+,.2f}bn"
         if len(step12) == 1 else "missing")

    # --- marginality curve --------------------------------------------------
    m = curve.m.to_numpy()
    y = curve.union_absolute_bn.to_numpy()
    gate("marginality_grid", len(curve) == 21 and abs(m[0]) < 1e-12 and abs(m[-1] - 1) < 1e-12,
         f"{len(curve)} points from {m[0]} to {m[-1]}")
    slope = (y[-1] - y[0])
    linear = np.allclose(y, y[0] + m * slope, atol=1e-6)
    gate("marginality_curve_is_linear_in_m", bool(linear))
    m_star = curve.break_even_m_star.iloc[0]
    if pd.isna(m_star):
        gate("break_even_m_star_consistent", slope == 0, "no finite m*")
    else:
        value_at = y[0] + float(m_star) * slope
        gate("break_even_m_star_consistent", abs(value_at) < 1e-6,
             f"m* = {float(m_star):.6f}, union absolute there = {value_at:+.2e} bn")
    at_one = float(y[-1])
    gate("marginality_endpoint_matches_the_waterfall", abs(at_one - union_end) < 1e-6,
         f"m=1 gives {at_one:+.4f}bn, waterfall ends at {union_end:+.4f}bn")

    return report()


def report() -> int:
    width = max(len(n) for n, _, _ in results)
    failed = 0
    for name, passed, detail in results:
        mark = "PASS" if passed else "FAIL"
        failed += 0 if passed else 1
        print(f"  {mark}  {name:<{width}}  {detail}")
    print(f"\n{len(results) - failed}/{len(results)} gates passed")
    if failed:
        print(f"[BLOCKED] {failed} gate(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

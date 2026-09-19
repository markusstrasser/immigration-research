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
    expected = sum(1 for f in arms.F_arm.unique() for e in arms.E_arm.unique()
                   for c in arms.C_arm.unique() for r in arms.R_arm.unique()
                   if e == "zero" or r == "all_zero")
    gate("arms_matrix_covers_nonoverlapping_combinations", len(arms) == expected
         and not ((arms.E_arm != "zero") & (arms.R_arm != "all_zero")).any(),
         f"{len(arms)} rows; additive E/R enforcement combinations excluded")

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
    # Zero is valid. A large residual is not evidence of reconciliation.
    comparator = nat[(nat.block == "consolidated") & (nat.line != "consolidated position")].amount_bn.sum() * 1e9
    gate("national_comparator_rows_sum", abs(comparator - nr["consolidated_position"]) < 1e3)
    gate("national_bridge_arithmetic", abs(comparator - account_lines * 1e9 - reported_residual) < 1e3)
    gate("unresolved_coverage_is_not_certified_complete", audit.get("account_status") == "expanded_partial",
         "arithmetic gates do not certify program completeness")
    from consolidation import require_conservation
    detail = audit["item_metadata"]["R|central"]["detail"]
    va = detail["700_veterans_net_of_medical"]
    require_conservation(va["gross"], va["va_medical_already_priced"] + va["cash_already_priced"], 0,
                         va["dollars"], "VA base cash plus residual")
    for name in ["400_transportation", "600_income_security_net"]:
        row = detail[name]
        gross = row["gross"] if name.startswith("400") else row["general_retirement_601"] + row["housing_assistance_604"]
        require_conservation(gross, 0, row["federal_grants_netted"], row["dollars"], name)
    gate("known_program_ownership_identities", True, "VA cash and matched grants count once")
    from lifetime import load_age_profiles
    profiles, _ = load_age_profiles(HERE.parents[2])
    exported = profiles[(profiles.allocation == "shared") & (profiles.account == "expanded")].groupby("group").net_total.sum()
    gate("age_profiles_reproduce_each_annual_total", all(abs(exported[g] - r.cumulative_bn * 1e9) < 1.0
                                                       for g, r in ends.iterrows()))

    # --- item D: the district cost-to-serve differential ---------------------
    dg = audit.get("district_coverage_gate", {})
    gate("item_D_district_differential_was_built", bool(dg.get("built")),
         f"{dg.get('states', 0)} jurisdictions, coverage ratios "
         f"{dg.get('min_ratio', float('nan')):.4f} to {dg.get('max_ratio', float('nan')):.4f}"
         if dg.get("built") else "item D is not in this run")
    if dg.get("built"):
        gate("item_D_every_state_clears_the_coverage_gate_or_carries_a_zero_differential",
             bool(dg["every_state_clears_or_is_zeroed"]),
             f"{len(dg['states_failing_the_coverage_gate'])} failed the "
             f"{float(dg['tolerance']):.0%} gate and are zeroed: "
             f"{dg['states_failing_the_coverage_gate'] or 'none'}")
        gate("item_D_covers_all_51_jurisdictions", bool(dg["all_51_jurisdictions"]),
             f"{dg['states']} jurisdictions")
        csv_path = DER / "district_differential_by_state.csv"
        if not csv_path.exists():
            gate("item_D_parameters_match_the_written_district_table", False,
                 "district_differential_by_state.csv is missing")
        else:
            dd = pd.read_csv(csv_path)
            per_state = dg["per_state"]
            bad = []
            for _, r in dd.iterrows():
                got = per_state.get(r.state)
                if got is None:
                    bad.append(f"{r.state}: absent from the parameters")
                    continue
                for col, key in [("hispanic_minus_all_charged", "hispanic_minus_all"),
                                 ("white_minus_all_charged", "white_minus_all"),
                                 ("coverage_ratio", "coverage_ratio")]:
                    if abs(float(r[col]) - float(got[key])) > 1e-3:
                        bad.append(f"{r.state}/{key}")
            gate("item_D_parameters_match_the_written_district_table", not bad,
                 "; ".join(bad) or f"{len(dd)} states agree to a tenth of a cent")
            gate("item_D_differential_signs_are_reported",
                 bool(np.isfinite(dd.hispanic_minus_all.to_numpy()).all()
                      and np.isfinite(dd.white_minus_all.to_numpy()).all()),
                 f"Hispanic-minus-all positive in {int((dd.hispanic_minus_all > 0).sum())} of "
                 f"{len(dd)} states, white-minus-all positive in "
                 f"{int((dd.white_minus_all > 0).sum())}")
        d_rows = items[(items.item == "D") & (items.group == UNION)]
        gate("item_D_is_in_the_items_table", len(d_rows) == 1,
             f"union {float(d_rows.total_bn.iloc[0]):+.3f}bn" if len(d_rows) == 1
             else f"{len(d_rows)} rows")

    # --- item P: non-school state and local capital --------------------------
    cg = audit.get("capital_reconciliation_gate", {})
    gate("item_P_capital_charge_was_built", bool(cg.get("built")),
         f"arm {cg.get('arm')}" if cg.get("built") else "item P is not in this run")
    if cg.get("built"):
        gate("item_P_reconciles_to_the_national_non_school_capital_total",
             bool(cg["within_population_ratio"]),
             f"charged {float(cg['charged_dollars'])/1e9:,.2f}bn of "
             f"{float(cg['national_target_2024'])/1e9:,.2f}bn, ratio {float(cg['ratio']):.5f} "
             f"vs population ratio {float(cg['population_ratio']):.5f}")
        gate("item_P_shares_item_G_per_capita_convention", bool(cg["matches_item_G"]),
             f"P {float(cg['ratio']):.5f} vs G {float(cg['item_G_ratio']):.5f}, "
             f"difference {float(cg['item_G_ratio_difference']):+.5f}")
        comp = cg["components"]
        split = (float(comp["elsec_capital"]) + float(comp["capital_inside_item_G"])
                 + float(cg["national_target_2022"]))
        gate("item_P_capital_split_is_exhaustive",
             abs(split - float(comp["capital_total"])) < 1.0,
             f"elementary and secondary {float(comp['elsec_capital'])/1e9:,.1f}bn + inside "
             f"item G {float(comp['capital_inside_item_G'])/1e9:,.1f}bn + item P "
             f"{float(cg['national_target_2022'])/1e9:,.1f}bn = "
             f"{split/1e9:,.1f}bn vs Census line 67 "
             f"{float(comp['capital_total'])/1e9:,.1f}bn")
        gate("item_P_parsed_capital_total_matches_census_line_67",
             bool(cg["cog_line_67_matches_the_parsed_total"]))
        order = water[water.group == UNION].sort_values("step").item.tolist()
        gate("item_P_follows_item_K_in_the_waterfall",
             "K" in order and "P" in order and order.index("P") == order.index("K") + 1,
             " ".join(order))
        dial = {r["item"]: r for r in audit.get("marginality_dial", [])}
        gate("items_D_and_P_are_on_the_marginality_dial",
             bool(dial.get("P", {}).get("dialled")) and bool(dial.get("D", {}).get("dialled")),
             f"P {dial.get('P', {}).get('dialled')}, D {dial.get('D', {}).get('dialled')}")

    gate("no_item_was_switched_off_at_the_command_line",
         not audit.get("items_switched_off"),
         str(audit.get("items_switched_off") or "none"))

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

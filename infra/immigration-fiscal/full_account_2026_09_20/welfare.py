"""Explicit fiscal-response sensitivities for the reconciled annual accounts.

No incidence column is treated as an estimated counterfactual response. The
declared arms retain direct taxes, remove capital-incidence pools, and expose
unresolved double counting as a nonnegative subtraction, O.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from builder import HERE, read_allocations, sha, verify_export


def response_pools(receipts, spending):
    receipts = receipts.loc[~receipts.scenario_id.eq("evidence_only")].copy()
    r_classes = {"personal_income", "household_direct", "corporate_capital",
                 "business_property", "other_business", "public_asset", "foreign", "rounding"}
    s_classes = {"service", "household_transfer", "interest", "foreign",
                 "subsidy", "rounding", "public_goods"}
    if set(receipts.response_class)-r_classes or set(spending.response_class)-s_classes:
        raise ValueError("Unreviewed response class; explicit mapping required")
    # Incidence assigned to labor is not an independently remitted payroll tax.
    capital_category = receipts.category.isin([
        "corporate_capital", "corporate_labor", "modeled_owner_property",
        "remaining_production_property", "personal_property_tax"])
    direct = receipts.response_class.isin(["personal_income", "household_direct"]) & ~capital_category
    receipts = receipts.assign(direct_bn=np.where(direct, receipts.target_bn, 0.0))
    rows = []
    for (r_case, allocation), r in receipts.groupby(["scenario_id", "allocation"]):
        if r.unallocated_bn.abs().sum() > 1e-8 or "external" in r_case:
            continue
        for (s_case, _), s in spending.loc[spending.allocation.eq(allocation)].groupby(["scenario_id", "allocation"]):
            # F-fixed is a different allocation of the same expense, not a
            # second physical-cost estimate; use the average assignment as base.
            if not s_case.endswith("F_per_capita") or s.unallocated_bn.abs().sum() > 1e-8:
                continue
            by_class = s.groupby("response_class").target_bn.sum()
            rows.append(dict(
                receipt_scenario=r_case, spending_scenario=s_case, allocation=allocation,
                direct_receipts_bn=r.direct_bn.sum(),
                excluded_incidence_receipts_bn=r.target_bn.sum()-r.direct_bn.sum(),
                transfers_bn=float(by_class.get("household_transfer", 0)),
                fixed_business_subsidies_bn=float(by_class.get("subsidy", 0)),
                services_bn=float(by_class.get("service", 0)),
                public_goods_bn=float(by_class.get("public_goods", 0)),
                legacy_interest_bn=float(by_class.get("interest", 0)),
                personal_income_overlap_ceiling_bn=r.loc[r.response_class.eq("personal_income"), "target_bn"].sum(),
            ))
    return pd.DataFrame(rows)


def combine(pools, benefits):
    required = ["scenario_id", "capital_adjustment", "excluded_capital_owner_share",
                "normalization", "private_after_tax_wtp_bn", "induced_current_receipts_bn",
                "source_transfer_saving_bn", "private_plus_receipts_bn"]
    if set(required)-set(benefits) or benefits[required].isna().any().any():
        raise ValueError("Missing benefit-contract field")
    if benefits.scenario_id.duplicated().any():
        raise ValueError("Duplicate benefit scenario")
    if not np.allclose(benefits.private_plus_receipts_bn,
                       benefits.private_after_tax_wtp_bn+benefits.induced_current_receipts_bn):
        raise ValueError("Benefit private/tax identity broken")
    frames = []
    for pool in pools.itertuples():
        for public_response in (0., 1.):
            # Capacity alignment is a declared three-point assumption. It is
            # not an estimated time path or a mathematical requirement.
            b = benefits.copy()
            service_response = b.capital_adjustment.to_numpy()
            if not np.isin(service_response, [0., .5, 1.]).all():
                raise ValueError("Unreviewed capacity response")
            direct = (pool.direct_receipts_bn-pool.transfers_bn
                      -service_response*pool.services_bn-public_response*pool.public_goods_bn)
            for beta in (0., 1.):
                # M=0 in this export. The source phaseout can be applied with
                # its private loss and cancels identically at primary beta=1.
                budget = direct+b.induced_current_receipts_bn
                welfare = b.private_after_tax_wtp_bn+beta*budget
                out = b.copy()
                out["receipt_scenario"] = pool.receipt_scenario
                out["spending_scenario"] = pool.spending_scenario
                out["allocation"] = pool.allocation
                out["public_goods_response"] = public_response
                out["service_response"] = service_response
                out["fiscal_weight"] = beta
                out["direct_fiscal_response_bn"] = direct
                out["budget_effect_bn"] = budget
                out["welfare_bn"] = welfare
                out["break_even_omitted_bn"] = -welfare
                out["overlap_assumed_bn"] = 0.
                # At beta=1 this is the extra overlapping receipt that
                # consumes a positive result; negative values already fail.
                out["overlap_to_zero_bn"] = welfare if beta else np.nan
                out["break_even_service_response_beta1"] = (
                    pool.direct_receipts_bn-pool.transfers_bn
                    -public_response*pool.public_goods_bn+b.private_plus_receipts_bn
                    )/pool.services_bn if pool.services_bn else np.nan
                out["welfare_after_all_personal_income_removed_bn"] = (
                    welfare-beta*pool.personal_income_overlap_ceiling_bn)
                out["break_even_fiscal_weight"] = np.divide(
                    -b.private_after_tax_wtp_bn.to_numpy(), budget.to_numpy(),
                    out=np.full(len(b), np.nan), where=budget.to_numpy()!=0)
                out["fiscal_weight_root_in_0_1"] = out.break_even_fiscal_weight.between(0, 1)
                out["interpretation"] = "CONDITIONAL_MODEL_NOT_IDENTIFIED_POLICY_EFFECT"
                frames.append(out)
    return pd.concat(frames, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--out", type=Path, default=HERE/"derived")
    args = parser.parse_args()
    fiscal = args.source_root.resolve()/"infra/immigration-fiscal"
    receipt_path = fiscal/"full_account_receipts_2026_09_20/derived/category_allocations.csv"
    spending_path = fiscal/"full_account_spending_2026_09_20/derived/allocations.csv"
    benefit_path = fiscal/"full_account_benefits_2026_09_20/derived/benefit_scenarios.csv"
    upstream_audits = [verify_export(p) for p in [receipt_path, spending_path, benefit_path]]
    receipts, _ = read_allocations(receipt_path, 8008.290)
    spending, _ = read_allocations(spending_path, 10061.458)
    benefits = pd.read_csv(benefit_path)
    pools = response_pools(receipts, spending)
    combined = combine(pools, benefits)
    group = ["allocation", "normalization", "excluded_capital_owner_share",
             "service_response", "public_goods_response", "fiscal_weight"]
    summary = combined.groupby(group).agg(
        cases=("welfare_bn", "size"), min_bn=("welfare_bn", "min"),
        max_bn=("welfare_bn", "max"),
        break_even_service_min=("break_even_service_response_beta1", "min"),
        break_even_service_max=("break_even_service_response_beta1", "max"),
        ).reset_index()
    args.out.mkdir(parents=True, exist_ok=True)
    frames = {"response_pools": pools, "welfare_scenarios": combined, "welfare_summary": summary}
    for name, frame in frames.items():
        frame.to_csv(args.out/f"{name}.csv", index=False)
    audit = dict(source_hashes={str(p): sha(p) for p in [receipt_path, spending_path, benefit_path,
                    *upstream_audits, Path(__file__), HERE/"builder.py", HERE/"model.py", HERE/"DESIGN.md"]},
                 outputs={name: sha(args.out/f"{name}.csv") for name in frames},
                 overlap="O=0 upper welfare case; unmeasured O>=0 lowers results at beta>0",
                 service_capital_alignment="0/.5/1 service response paired to capital adjustment0/.5/1; unestimated",
                 owner_endpoints="Ownership0/.5/1 are unmeasured scenarios, not confidence bounds",
                 omitted_effects="Z=0; required incremental Z for zero is exported, not estimated",
                 population="Observed CPS Mexican-origin union; all ages and education",
                 fiscal_recycling="beta1 transfers all marginal fiscal dollars to other US residents; beta0 separate endpoint")
    audit["business_subsidy_response"] = (
        "Zero in these conditional response arms. Incidence on target does not identify "
        "disappearing subsidies; payments to included owners need a matching private offset.")
    (args.out/"welfare_audit.json").write_text(json.dumps(audit, indent=2)+"\n")
    print(summary.query("excluded_capital_owner_share == 0 and service_response == 1 and public_goods_response == 0 and fiscal_weight == 1").to_string(index=False))


if __name__ == "__main__":
    main()

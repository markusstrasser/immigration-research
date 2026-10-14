"""Isolated corrections from the committed oct14 central at the two personal endpoints.

The legacy price mixture is reproduced only as a labelled positive-control comparator.
No legacy nominal Mexican row is passed to the live totals or log-weight code.
"""
import copy
import json
from pathlib import Path

import numpy as np
import pandas as pd

import world_ledger as W
from population_basis import suffixed

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
BASE = HERE / "_cache/p7_baseline/derived"


def linear_totals(rows, I, weighting):
    """Equal/λ sums for labelled historical comparisons; reject any nonfinite input."""
    W.gate("isolated_rows_finite", np.isfinite(rows.central).all())
    fac = W.channel_factors(I, "money")
    fac["_lambda"] = {f"equal_lambda_{k}": v for k, v in W.LAMBDAS.items()}
    amounts = dict.fromkeys(W.PARTIES, 0.0)
    for r in rows.itertuples():
        weight = W.row_weight(r, weighting, fac, I["pos"], I, {}, "a")
        W.gate("isolated_weight_finite", np.isfinite(weight))
        amounts[r.party] += r.central * weight
    group = sum(amounts[g] for g in W.GROUP)
    other = amounts["others_today"] + amounts["future_taxpayers"]
    mexico = amounts["mexico_residents"]
    return dict(world_total_bn=group + other + mexico, group_total_bn=group,
                other_us_residents_bn=other, us_residents_incl_group_bn=other + group,
                mexico_residents_bn=mexico, breakeven_w=-(other + mexico) / group)


def main():
    result = []
    incidence = json.loads((D / "valuation_meta_oct14.json").read_text())["incidence"]["oct14"]
    for basis in ("lineage", "row4"):
        I = W.load("oct14", basis)
        old = dict(I, cash_positive_control=True)
        old["g2"] = pd.read_csv(suffixed(BASE / "g2_premium.csv", basis))
        old["vgen"] = pd.read_csv(BASE / "valuation_by_generation_oct14.csv")
        old["val"] = pd.read_csv(BASE / "valuation_oct14.csv")
        for bound in ("zero", "upper"):
            pn = W.premium_rows(I, g3_central=bound)
            po = W.premium_rows(old, g3_central=bound)
            for end in ("low", "high"):
                J = dict(old, account_end=end)
                original, _, _ = W.build_rows(J, g3_central=bound)
                rem = original.row.eq("remit_mexico")
                nominal = original.loc[rem, "nominal_usd_bn"].item()
                original.loc[rem, ["low", "central", "high"]] = nominal
                original["price_basis"] = "LEGACY_MIXED_DO_NOT_LOG_WEIGHT"
                arms = {"original_oct14": original}
                comp = original.copy()
                for gen in W.GROUP:
                    m = comp.row.eq(f"premium_{gen}")
                    comp.loc[m, "central"] += pn[gen]["gain"]["central"] - po[gen]["gain"]["central"]
                    tax = (pn[gen]["tax"]["central"] + pn[gen]["ctax"]["central"]
                           - po[gen]["tax"]["central"] - po[gen]["ctax"]["central"])
                    comp.loc[comp.row.eq(f"mexico_taxes_avoided_{gen}"), "central"] += tax
                    comp.loc[comp.row.eq(f"mexico_taxes_lost_{gen}"), "central"] -= tax
                arms["fix1_compensation"] = comp
                source, payer = original.copy(), original.copy()
                v = I["vgen"][I["vgen"].end.eq(end)]
                for gen in W.GROUP:
                    s = v[v.generation.eq(gen)]
                    source_move = s.source_tax_credit_bn.sum()
                    payer_move = s.group_credit_adjustment_bn.sum()
                    if basis == "row4" and gen == "G3+":
                        source_move -= (incidence[end]["source_tax_credit_bn"]
                                        - incidence[end]["identified_union_source_tax_credit_bn"])
                        payer_move += incidence[end]["added_people_child_credit_other_residents_bn"]
                    source.loc[source.row.eq(f"us_budget_value_{gen}"), "central"] += source_move
                    payer.loc[payer.row.eq(f"us_budget_value_{gen}"), "central"] += payer_move
                amount = v.child_credit_other_residents_bn.sum()
                if basis == "row4":
                    amount -= incidence[end]["added_people_child_credit_other_residents_bn"]
                extra = original.iloc[0:1].copy()
                extra.loc[:, "row"] = "fiscal_nonmember_credits"
                extra.loc[:, "party"] = "others_today"
                extra.loc[:, "weight"] = "others:mean"
                extra.loc[:, "central"] = amount
                payer = pd.concat([payer, extra], ignore_index=True)
                arms["fix2_source_incidence"] = source
                arms["fix12_child_credit_payer"] = payer
                for prices in ("gdp", "consumption"):
                    price = original.copy()
                    price.loc[rem, "central"] = nominal * W.remittance_price_factor(prices)
                    arms[f"fix7_recipient_principal_{prices}"] = price
                for weighting in ("equal", "equal_lambda_1.16", "equal_lambda_1.5"):
                    before = linear_totals(original, I, weighting)
                    for name, frame in arms.items():
                        after = linear_totals(frame, I, weighting)
                        row = dict(fix=name, population_basis=basis, population_rule=(
                            "42.75M lineage, fiscal and person rows" if basis == "lineage" else
                            "39.71M identified-union correction only; frozen lineage fiscal baseline retained"),
                            account_end=end, allocation="personal", g3_bound=bound, weighting=weighting,
                            headline_change_bn=0.0, **after)
                        for key in before:
                            row[f"delta_{key}"] = after[key] - before[key]
                        row["world_delta_over_5bn"] = abs(row["delta_world_total_bn"]) >= 5
                        result.append(row)
    pd.DataFrame(result).to_csv(D / "p7_fix_deltas_oct14.csv", index=False, lineterminator="\n", float_format="%.9f")
    # Source-tax counterpart is excluded centrally; the range is a declared parity stress, not an empirical bound.
    rows = []
    for end, s in incidence.items():
        upper = s["capital_source_tax_credit_bn"]
        rows.append(dict(account_end=end, corporate_labor_already_in_wages_bn=s["corporate_labor_credit_bn"],
                         us_capital_source_tax_bn=upper, foreign_counterpart_central_bn=0,
                         foreign_counterpart_stress_low_bn=0, foreign_counterpart_stress_high_bn=upper,
                         identified_union_capital_source_bn=s["identified_union_capital_source_tax_credit_bn"],
                         rule="Mexico plus rest of world excluded; [ASSUMPTION] 0..US capital-source parity stress; no empirical finite bound"))
    pd.DataFrame(rows).to_csv(D / "p7_foreign_counterparts_oct14.csv", index=False, lineterminator="\n", float_format="%.9f")
    # Isolate the service-asymmetry part of fix 5 on the originally reported zero-bound private comparison.
    # Its old all-tax scope is held fixed; the final wage-tax scope is reported separately by beside_extra.
    private_old = pd.read_csv(BASE / "beside_extra_private_gain_oct14.csv")
    original_v = pd.read_csv(BASE / "valuation_by_generation_oct14.csv")
    taxes = original_v[original_v.cls.eq("tax")].groupby(["end", "generation"]).V_central_bn.sum()
    private_rows = []
    for end in ("low", "high"):
        shift = {g: taxes.loc[(end, g)] - np.mean([taxes.loc[(e, g)] for e in ("low", "high")]) for g in W.GROUP}
        shift["group"] = sum(shift.values())
        for r in private_old.itertuples():
            before = r.wages_only_bn + shift[r.generation]
            change = -r.mexico_services_forgone_bn
            private_rows.append(dict(scenario=r.scenario, generation=r.generation, account_end=end,
                allocation="personal", population_basis="lineage", g3_bound="zero",
                tax_scope="original all-tax scope held fixed to isolate service symmetry only",
                original_asymmetric_private_bn=before, symmetric_no_services_private_bn=before + change,
                delta_private_bn=change, world_ledger_change_bn=0.0))
    pd.DataFrame(private_rows).to_csv(D / "p7_private_symmetry_delta_oct14.csv", index=False,
                                     lineterminator="\n", float_format="%.9f")
    print(f"P7 isolated corrections: {len(result)} rows; frozen headline unchanged")


if __name__ == "__main__":
    main()

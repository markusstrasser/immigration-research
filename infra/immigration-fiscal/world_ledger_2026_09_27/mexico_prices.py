"""Numeric peso/PPP contracts and separate Mexican fiscal cost/recipient value.

Native-First: the existing pandas lane owns the calculation; this module supplies
one shared representation for its world and beside-arm callers.
"""
import numpy as np

ENDS = ("low", "central", "high")
BUDGET_CLASSES = {"education", "health", "cash", "public_good"}


def require(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def budget_from_gdp(mxb, gdp_divisor):
    """Migrate the existing producer's GDP-PPP budget, preserving original bn.

    Its source is valuation.mexico_budget: ENIGH/WDI quantities are emitted at
    GDP PPP. The explicit source contract is distinct from a label assigned to
    an already mixed world row.
    """
    require("budget_source_gdp_ppp_positive", np.isfinite(gdp_divisor) and gdp_divisor > 0)
    out = mxb.copy()
    require("budget_classes_known", set(out.cls) <= BUDGET_CLASSES | {"tax"})
    used = out.cls.isin(BUDGET_CLASSES)
    require("budget_source_amounts_finite", np.isfinite(out.loc[used, "bn"]).all())
    for side in ("fiscal_cost", "recipient_value"):
        input_column = "fiscal_bn" if side == "fiscal_cost" else "recipient_bn"
        source = out[input_column] if input_column in out else out.bn
        require("budget_side_source_finite", np.isfinite(source[used]).all(), side=side)
        out[f"{side}_pesos_bn"] = source.astype(float) * float(gdp_divisor)
        out[f"{side}_ppp_divisor"] = float(gdp_divisor)
        out[f"{side}_bn"] = source.astype(float)
    out["source_ppp_divisor"] = float(gdp_divisor)
    out["source_pesos_bn"] = out.fiscal_cost_pesos_bn
    out["price_rule"] = "GDP money"
    return out


def validate_budget(mxb):
    used = mxb[mxb.cls.isin(BUDGET_CLASSES)]
    required = {"source_pesos_bn", *(f"{side}_{field}" for side in ("fiscal_cost", "recipient_value")
                                    for field in ("pesos_bn", "ppp_divisor", "bn"))}
    require("budget_numeric_contract_present", required <= set(mxb.columns), missing=sorted(required - set(mxb.columns)))
    difference = (used.fiscal_cost_pesos_bn - used.source_pesos_bn).abs().max()
    require("fiscal_cost_is_full_source_cost", difference <= 1e-9, error=float(difference))
    for side in ("fiscal_cost", "recipient_value"):
        columns = [f"{side}_pesos_bn", f"{side}_ppp_divisor", f"{side}_bn"]
        require("budget_numeric_contract_present", set(columns) <= set(mxb.columns), side=side)
        require("budget_numeric_contract_finite", np.isfinite(used[columns]).all().all())
        divisor = used[f"{side}_ppp_divisor"]
        require("budget_ppp_positive", (divisor > 0).all())
        error = (used[f"{side}_pesos_bn"] / divisor - used[f"{side}_bn"]).abs().max()
        require("budget_actual_numeric_conversion", error <= 1e-9, error=float(error))


def price_budget(mxb, divisors, *, recipient_only=False):
    """Change price, never source pesos. An explicit recipient arm cannot move cost."""
    validate_budget(mxb)
    out = mxb.copy()
    require("budget_category_divisors_complete", BUDGET_CLASSES <= set(divisors))
    sides = ("recipient_value",) if recipient_only else ("fiscal_cost", "recipient_value")
    for cls, divisor in divisors.items():
        require("budget_category_divisor_positive", np.isfinite(divisor) and divisor > 0, cls=cls)
        mask = out.cls.eq(cls)
        for side in sides:
            out.loc[mask, f"{side}_ppp_divisor"] = divisor
            out.loc[mask, f"{side}_bn"] = out.loc[mask, f"{side}_pesos_bn"] / divisor
    out["price_rule"] = "category services"
    validate_budget(out)
    if recipient_only:
        require("valuation_cannot_change_fiscal_cost", out.fiscal_cost_bn.equals(mxb.fiscal_cost_bn))
    return out


def budget_values(mxb, generation, health_vg, response, convention="average_cost"):
    """Saved fiscal cost and forgone value from disjoint fields, by endpoint."""
    validate_budget(mxb)
    require("public_response_floor", min(response) >= 0.60 and max(response) <= 0.85, response=response)
    require("public_response_ordered", list(response) == sorted(response))
    require("public_value_convention", convention in ("average_cost", "response_only"))
    s = mxb[mxb.generation.eq(generation) & mxb.cls.isin(BUDGET_CLASSES)]
    cost = s.groupby("cls").fiscal_cost_bn.sum()
    value = s.groupby("cls").recipient_value_bn.sum()
    peso = s.groupby("cls").fiscal_cost_pesos_bn.sum()
    require("budget_generation_classes_complete", BUDGET_CLASSES <= set(cost.index), generation=generation)
    pg_value = value.public_good * (1 if convention == "average_cost" else response[1])
    saved = {end: float(cost.education + cost.health + cost.cash + cost.public_good * r)
             for end, r in zip(ENDS, response)}
    saved_pesos = {end: float(peso.education + peso.health + peso.cash + peso.public_good * r)
                   for end, r in zip(ENDS, response)}
    lost = {end: -float(value.health * h + value.cash + pg_value)
            for end, h in zip(ENDS, reversed(health_vg))}
    for r in response:
        pg = cost.public_good
        require("effective_public_response_above_floor", pg == 0 or pg * r / pg >= response[0] - 1e-12)
    return saved, saved_pesos, lost


def mixture_divisor(pesos_by_class, divisors):
    """Peso expenditure shares imply a harmonic PPP divisor, not a label."""
    require("fiscal_mix_nonnegative", all(np.isfinite(v) and v >= 0 for v in pesos_by_class.values()))
    require("fiscal_mix_divisors_complete", set(pesos_by_class) <= set(divisors))
    total = sum(pesos_by_class.values())
    international = sum(v / divisors[c] for c, v in pesos_by_class.items())
    require("fiscal_mix_positive", total > 0 and international > 0)
    return total / international


def numeric_row_metadata(pesos, divisors, basis):
    if not isinstance(divisors, dict):
        divisors = dict.fromkeys(ENDS, divisors)
    return dict(mexico_price_basis=basis,
                **{f"mexico_pesos_bn_{e}": pesos[e] for e in ENDS},
                **{f"mexico_ppp_divisor_{e}": divisors[e] for e in ENDS})


def validate_numeric_rows(rows):
    """Reconstruct Mexico-side dollars from explicit source pesos and divisors."""
    columns = [f"mexico_{k}_{e}" for e in ENDS for k in ("pesos_bn", "ppp_divisor")]
    require("mexico_numeric_price_contract_present", set(columns) <= set(rows.columns))
    mexico = rows[rows.party.eq("mexico_residents")]
    require("mexico_numeric_price_contract_finite", np.isfinite(mexico[columns]).all().all())
    for end in ENDS:
        div = mexico[f"mexico_ppp_divisor_{end}"]
        require("mexico_numeric_divisor_positive", (div > 0).all())
        error = (mexico[f"mexico_pesos_bn_{end}"] / div - mexico[end]).abs().max()
        require("mexico_actual_numeric_conversion", error <= 1e-9, end=end, error=float(error))
    require("mexico_numeric_basis_present", mexico.mexico_price_basis.notna().all())


def scale_peso_rows(rows, factor):
    """A dimensional-invariance probe, preserving the independent PPP divisors."""
    require("peso_scaling_positive", np.isfinite(factor) and factor > 0)
    validate_numeric_rows(rows)
    out = rows.copy()
    m = out.party.eq("mexico_residents")
    for end in ENDS:
        out.loc[m, f"mexico_pesos_bn_{end}"] *= factor
        out.loc[m, end] = out.loc[m, f"mexico_pesos_bn_{end}"] / out.loc[m, f"mexico_ppp_divisor_{end}"]
    validate_numeric_rows(out)
    return out

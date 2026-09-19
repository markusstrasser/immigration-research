"""Normalized competitive CES counterfactual; assumptions, not policy estimates."""
from __future__ import annotations

import numpy as np


def equilibrium(shares, target, sigma=2., labor_share=.65, adjustment=1., elasticity=0.):
    """Remove target efficiency labor; outside workers may adjust hours.

    Both arrays have skill on axis 0; remaining axes may be replicate weights.
    Current skill quantities, wages and capital are normalized to one. Capital
    without target is q**adjustment; released capital earns the initial rental
    rate elsewhere. Its opportunity return is deducted from outside income.
    """
    shares, target = np.asarray(shares, float), np.asarray(target, float)
    if shares.shape != target.shape or shares.shape[0] != 2:
        raise ValueError("Require matching two-skill share arrays")
    if not np.isfinite(shares).all() or not np.isfinite(target).all():
        raise ValueError("Nonfinite calibration")
    if np.any(shares <= 0) or not np.allclose(shares.sum(axis=0), 1):
        raise ValueError("Skill compensation shares must sum to one")
    if np.any((target < 0) | (target >= 1)):
        raise ValueError("Target share outside [0,1)")
    if not (sigma > 0 and 0 < labor_share < 1 and 0 <= adjustment <= 1
            and 0 <= elasticity <= 1):
        raise ValueError("Invalid model parameter")
    rho = 1. if np.isinf(sigma) else 1 - 1 / sigma
    power = labor_share + adjustment * (1 - labor_share)

    def evaluate(log_hours):
        x = (1 - target) * np.exp(log_hours)
        log_q = ((shares * np.log(x)).sum(axis=0) if abs(rho) < 1e-12
                 else np.log((shares * x**rho).sum(axis=0)) / rho)
        log_wage = (power - rho) * log_q + (rho - 1) * np.log(x)
        return log_q, log_wage

    log_hours = np.zeros_like(shares)
    for iteration in range(5000):
        log_q, log_wage = evaluate(log_hours)
        desired = elasticity * log_wage
        error = float(np.max(np.abs(desired - log_hours)))
        if error < 1e-12:
            break
        log_hours = .75 * log_hours + .25 * desired
    else:
        raise ValueError("Labor-supply fixed point did not converge")
    hours, wage = np.exp(log_hours), np.exp(log_wage)
    q = np.exp(log_q)
    output = q**power
    capital = q**adjustment
    current_pay = labor_share * shares * (1 - target)
    counterfactual_pay = current_pay * hours * wage
    labor_gain = current_pay - counterfactual_pay
    domestic_capital_gain = (1 - labor_share) * (1 - output)
    opportunity_income = (1 - labor_share) * (1 - capital)
    capital_gain = domestic_capital_gain - opportunity_income
    gross_income_gain = labor_gain.sum(axis=0) + capital_gain
    # Euler exhaustion applies to domestic output only; opportunity income is
    # outside the modeled production sector and is accounted for separately.
    if not np.allclose(counterfactual_pay.sum(axis=0), labor_share * output,
                       rtol=1e-10, atol=1e-12):
        raise ValueError("Counterfactual Euler conservation failed")
    # Quasilinear isoelastic labor disutility at constant marginal tax rates.
    # The caller multiplies by (1-tax) to express this in after-tax dollars.
    disutility_difference = np.zeros_like(shares)
    if elasticity:
        disutility_difference = current_pay * elasticity / (1 + elasticity) * (
            1 - hours**(1 + 1 / elasticity))
    return dict(labor_gain=labor_gain, capital_gain=capital_gain,
                domestic_capital_gain=domestic_capital_gain,
                opportunity_income=opportunity_income,
                gross_income_gain=gross_income_gain,
                disutility_difference=disutility_difference,
                wage_without_over_with=wage, hours_without_over_with=hours,
                output_without_over_with=output, capital_without_over_with=capital,
                iterations=iteration, fixed_point_error=error)


def fiscal_and_private(result, tax_rates, capital_tax=.246, tax_retention=1., excluded_owner_share=0.):
    """Partition income into private money-metric WTP and current tax receipts.

    Retention=1 taxes the alternative capital return identically in the US;
    retention=0 assumes that alternative return produces no US revenue.
    Excluded owners are foreign or target-group owners whose private welfare is
    omitted; this is a scenario share, not an observed ownership estimate. The
    fiscal dollar receives full weight, equivalent to recycling it to included
    residents. Neither retention nor ownership is measured. No phaseouts enter.
    """
    if not (0 <= capital_tax <= 1 and 0 <= tax_retention <= 1 and 0 <= excluded_owner_share <= 1):
        raise ValueError("Invalid capital tax/retention")
    tau = np.asarray(tax_rates, float).reshape((2,) + (1,) * (result["labor_gain"].ndim - 1))
    labor_tax = (tau * result["labor_gain"]).sum(axis=0)
    capital_tax_gain = capital_tax * (result["domestic_capital_gain"]
                                     - tax_retention * result["opportunity_income"])
    taxes = labor_tax + capital_tax_gain
    private_wtp = ((1 - tau) * (result["labor_gain"]
                   - result["disutility_difference"])).sum(axis=0)
    private_wtp += (1 - excluded_owner_share) * (result["capital_gain"] - capital_tax_gain)
    resource_cost = ((1 - tau) * result["disutility_difference"]).sum(axis=0)
    included_gross = result["labor_gain"].sum(axis=0) + (1-excluded_owner_share) * result["capital_gain"]
    target_identity = included_gross - resource_cost + excluded_owner_share * capital_tax_gain
    if not np.allclose(private_wtp + taxes, target_identity,
                       rtol=1e-10, atol=1e-12):
        raise ValueError("Tax/private partition double counts income")
    return dict(labor_tax_gain=labor_tax, capital_tax_gain=capital_tax_gain,
                current_receipts_gain=taxes, private_wtp=private_wtp,
                private_plus_receipts=private_wtp + taxes)

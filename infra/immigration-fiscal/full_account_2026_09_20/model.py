"""Accounting identities and a beneficiary-matched annual welfare bridge."""
from __future__ import annotations

import math


def finite(*values):
    if not all(math.isfinite(float(value)) for value in values):
        raise ValueError("Nonfinite accounting input")


def reconcile(national, target, other, external, unallocated, tolerance=1e-6):
    """Signed revenues, including enterprise losses, must also conserve."""
    finite(national, target, other, external, unallocated)
    residual = national - target - other - external - unallocated
    if abs(residual) > tolerance:
        raise ValueError(f"Accounting conservation failed: {residual}")
    return residual


def normalized_gap(target_balance, other_balance, target_population, population):
    finite(target_balance, other_balance, target_population, population)
    if not 0 < target_population < population:
        raise ValueError("Population universe or target invalid")
    share = target_population / population
    return target_balance - share * (target_balance + other_balance)


def bridge(direct, private, induced, overlap=0, transfer_saving=0,
           fiscal_weight=1, omitted=0):
    """With-target minus without-target welfare, in billions per year.

    'direct' already applies explicit response assumptions to assigned flows.
    A positive 'overlap' removes revenue counted in direct and induced.
    Omitted is a signed threshold variable, never an estimated residual benefit.
    """
    finite(direct, private, induced, overlap, transfer_saving, fiscal_weight, omitted)
    if not 0 <= fiscal_weight <= 1:
        raise ValueError("Fiscal recycling weight must lie in [0, 1]")
    if overlap < 0:
        raise ValueError("Duplicated receipts must be nonnegative")
    budget = direct + induced + transfer_saving - overlap
    private_net = private - transfer_saving
    welfare = private_net + fiscal_weight * budget + omitted
    return {
        "budget_effect_bn": budget,
        "outside_private_bn": private_net,
        "welfare_bn": welfare,
        "break_even_omitted_bn": -welfare,
        "break_even_fiscal_weight":
            -(private_net + omitted) / budget if budget else None,
    }

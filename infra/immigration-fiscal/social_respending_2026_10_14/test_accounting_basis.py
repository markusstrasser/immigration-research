"""Regress the cross-basis multiplication; CE requires an explicit sensitivity."""
import pytest

from respending import spending_basis_gate


def test_national_accounts_basis_matches_pce():
    spending_basis_gate("national_accounts", "national_accounts")


def test_cross_basis_spending_requires_labelled_sensitivity():
    with pytest.raises(ValueError, match="accounting basis differs"):
        spending_basis_gate("national_accounts", "CE_survey")
    spending_basis_gate("national_accounts", "CE_survey", units_sensitivity=True)

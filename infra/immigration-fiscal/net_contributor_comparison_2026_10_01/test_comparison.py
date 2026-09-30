"""Behavioral checks for weighting, zero classification and allocation conservation."""
import numpy as np
import pytest

from compare import household_table, normalized


def test_households_classified_before_person_weighting():
    # One mixed-balance two-member household is net positive even though one
    # member costs money. Its residents carry unequal survey weights.
    h = household_table([1, 1, 2, 3], np.ones(4, bool), np.array([-10., 6., 1., 0.]),
                        np.array([2., 5., 3., 7.]))
    positive = h.net_per_member > 0
    assert h.loc[positive, "resident_weight"].sum() == 7
    assert h.resident_weight.sum() == 17
    assert h.loc[h.household == 1, "net_per_member"].item() == 2
    assert h.loc[h.household == 3, "net_per_member"].item() == 0
    assert positive.sum() == 1


def test_outside_group_member_does_not_change_group_household_balance():
    h = household_table([1, 1], np.array([True, False]), np.array([5., -100.]), np.ones(2))
    assert h.members.item() == 1
    assert h.net_per_member.item() == -5


def test_allocation_conserves_under_population_rescaling():
    v, w = np.array([0., 2., 6.]), np.array([1., 3., 9.])
    assert np.isclose(normalized(v, w) @ w, 1)
    assert np.allclose(normalized(v, w * 4) * 4, normalized(v, w))


@pytest.mark.parametrize("v", [[0., 0.], [1., -1.], [1., np.nan]])
def test_unallocatable_nonzero_line_fails(v):
    with pytest.raises(ValueError, match="BLOCKED"):
        normalized(v, np.ones(2))

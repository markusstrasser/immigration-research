import numpy as np
import pytest

from tenure import C, fixed_count_tenure, load, tenure_rates, transfer_count_tenure


def fixture_data():
    return dict(age=np.array([7, 7, 25, 25, 55, 55, 2, 2]),
        sex=np.ones(8, int), generation=np.ones(8, int), arrival=np.zeros(8, int),
        hispanic=np.ones(8, bool))


def test_primary_table_and_conditional_cells():
    x = tenure_rates()
    assert x["owner"]["all"]["nce_pct"] == -2.18
    assert x["renter"]["all"]["nce_pct"] == -7.83
    assert x["owner"]["30 to 49 males"]["nce_pct"] == -6.57
    assert x["renter"]["50 and over males"]["nce_pct"] == 2.43


def test_tenure_preserves_counts_and_da_and_changes_composition():
    data = fixture_data()
    rates, base = load()
    old, _ = C.factors(data, rates, base)
    weights = np.array([3., 1., 1., 3., 2., 2., 1., 2.])
    new, cells = fixed_count_tenure(data, np.tile([1, 2], 4), weights, rates, base)
    for age in np.unique(data["age"]):
        m = data["age"] == age
        assert weights[m] @ new[m] == pytest.approx(weights[m] @ old[m], abs=1e-12)
    assert np.array_equal(new[:2], old[:2])  # Census under-five → DA only.
    assert new[3] > old[3] and new[2] < old[2]
    assert new[-2:].tolist() == [0., 0.]  # Born after the Census.
    assert len(cells) == 4


def test_count_transfer_retains_da_but_changes_total():
    data = fixture_data()
    rates, base = load()
    old, _ = C.factors(data, rates, base)
    transfer = transfer_count_tenure(data, np.tile([1, 2], 4), rates, base)
    assert np.array_equal(transfer[:2], old[:2])
    assert transfer.sum() != pytest.approx(old.sum())


def test_unknown_tenure_fails():
    data = fixture_data()
    rates, base = load()
    with pytest.raises(ValueError, match="unmapped CPS tenure"):
        fixed_count_tenure(data, np.zeros(8, int), np.ones(8), rates, base)

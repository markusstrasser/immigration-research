"""Legal dual-entitlement gate: the greater benefit, with incremental topups."""
import numpy as np
from pensions import topups


def test_spousal_and_survivor_never_add_full_own_benefit_twice():
    spouse,survivor=topups(np.array([2000.,2000.]),np.array([1200.,600.]),
                          np.array([2000.,2000.]),np.array([2200.,600.]))
    np.testing.assert_array_equal(spouse,[0.,400.])
    np.testing.assert_array_equal(survivor,[0.,1400.])

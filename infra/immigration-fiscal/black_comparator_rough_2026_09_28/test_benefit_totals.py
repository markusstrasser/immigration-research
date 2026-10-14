"""Positive benefits must not be netted against negative survey values in a unit."""
import numpy as np
import pandas as pd

from accrual_black import benefit_totals


def test_negative_values_and_multiple_units_preserve_positive_total():
    d = pd.DataFrame({'PH_SEQ': [1, 1, 1, 1, 2, 2], 'TAX_ID': [1, 1, 2, 2, 1, 1],
                      'SS_VAL': [1200, -700, -900, 0, 300, 550]})
    assert np.array_equal(benefit_totals(d), [1200, 1200, 0, 0, 850, 850])


def test_vectorized_totals_match_previous_rule_on_adversarial_units():
    rng = np.random.default_rng(14015)
    d = pd.DataFrame({'PH_SEQ': rng.integers(0, 30, 500), 'TAX_ID': rng.integers(0, 3, 500),
                      'SS_VAL': rng.integers(-10000, 10000, 500)})
    previous = d.groupby(['PH_SEQ', 'TAX_ID']).SS_VAL.transform(lambda values: values.clip(lower=0).sum()).to_numpy(float)
    assert np.array_equal(benefit_totals(d), previous)

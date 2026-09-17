"""Regression: partial/fully unknown parent birthplaces cannot establish generation 2."""
import numpy as np
import pandas as pd
from generation import gss_generation


def test_gss_all_parent_combinations():
    parents = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, np.nan])
    result = gss_generation(pd.Series([1] * len(parents)), parents)
    expected = pd.Series([3, 2, 2, np.nan, 2, np.nan, 2, np.nan, 2, np.nan])
    pd.testing.assert_series_equal(result, expected)


def test_own_birthplace_precedes_parent_information():
    born = pd.Series([2, 2, np.nan, np.nan])
    parents = pd.Series([0, np.nan, 0, 8])
    result = gss_generation(born, parents)
    pd.testing.assert_series_equal(result, pd.Series([1, 1, np.nan, np.nan]))

"""Adversarial arithmetic checks for resource allocation and missing-data bounds."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from analyze_cps_fiscal_2025 import allocate, estimate, summarize, health_model_for_metric
from analyze_immigration_uncertainty import corrected_mean, required_missing_mean, true_rate_ratio
from meps_health_transport_2024 import cps_insurance_category


class FiscalUncertaintyTests(unittest.TestCase):
    def test_military_insurance_matches_meps_private_equivalent(self):
        d = pd.DataFrame({"A_AGE": [40, 40, 40, 40, 40, 70],
                          "PRIV": [1, 2, 2, 2, 2, 2], "PUB": [1, 1, 1, 1, 2, 1],
                          "MIL": [2, 1, 2, 2, 2, 1], "CHAMPVA": [2, 2, 1, 2, 2, 2]})
        np.testing.assert_array_equal(cps_insurance_category(d), [1, 1, 1, 2, 3, 0])

    def test_school_combination_retains_health_uncertainty(self):
        self.assertEqual(health_model_for_metric("balance_excluding_school_lunch_after_health_age_birth"), "age_birth")
        self.assertEqual(health_model_for_metric("health_age_birth_insurance"), "age_birth_insurance")
        self.assertEqual(health_model_for_metric("school_lunch"), "")

    def test_mixed_family_totals_conserved_before_selection(self):
        # Four-member family, two adults; child is native and parent foreign-born.
        # Recipient selection must not assign the whole family's costs to that parent.
        unit = np.array([0, 0, 0, 0, 1])
        totals = np.array([1200., 60.])
        adults = np.array([True, True, False, False, True])
        np.testing.assert_allclose(allocate(totals, unit, adults, 2), [600, 600, 0, 0, 60])
        np.testing.assert_allclose(allocate(totals, unit, np.ones(5, bool), 2), [300, 300, 300, 300, 60])
        with self.assertRaises(ValueError):
            allocate(totals, unit, np.zeros(5, bool), 2)

    def test_sdr_keeps_negative_weights_and_whole_ratio(self):
        weights = np.ones((2, 161))
        weights[:, 1] = [-1, 3]
        values = np.array([0., 10.])
        est = estimate(values, weights)
        self.assertEqual(est[0], 5)
        self.assertEqual(est[1], 15)
        self.assertAlmostEqual(summarize(est)["se_sampling"], np.sqrt(2.5))

    def test_missing_population_tipping_point_and_share_definition(self):
        # Observed90 of true100, not10 missing for each100 observed.
        self.assertEqual(corrected_mean(2000, .1, -10000), 800)
        needed = required_missing_mean(2000, 8000, .1)
        self.assertAlmostEqual(needed, 62000)
        self.assertAlmostEqual(corrected_mean(2000, .1, needed), 8000)
        with self.assertRaises(ValueError):
            required_missing_mean(2000, 8000, 0)

    def test_crime_numerator_and_denominator_errors_have_opposite_effects(self):
        self.assertAlmostEqual(true_rate_ratio(.46, 1, .46), 1)
        self.assertAlmostEqual(true_rate_ratio(.46, .8, 1), .368)
        self.assertAlmostEqual(true_rate_ratio(.46, 1, .5), .92)
        self.assertAlmostEqual(true_rate_ratio(.46, 1.2, .5), 1.104)
        with self.assertRaises(ValueError):
            true_rate_ratio(.46, 1, 0)


if __name__ == "__main__":
    unittest.main()

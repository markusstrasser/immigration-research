"""Statistical invariants, not assertions about a desired empirical conclusion."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from analyze_arrival_cohorts import cohort_masks, ratios, sdr_estimate


class ArrivalCohortTests(unittest.TestCase):
    def test_negative_weight_changes_ratio_and_variance(self):
        # Full weights (1,1), replicate weights (-1,3): same denominator,
        # but for outcomes (0,2), full mean1 and every replicate mean3.
        weights = np.column_stack(([1, 1], np.tile([[-1], [3]], (1, 80))))
        estimates = ratios(np.array([0, 2]) @ weights, weights.sum(axis=0))
        result = sdr_estimate(estimates)
        self.assertEqual(result["estimate"], 1)
        self.assertEqual(result["acs_sdr_se"], 4)

    def test_within_survey_difference_preserves_covariance(self):
        first = np.r_[1., np.linspace(.5, 1.5, 80)]
        second = first + 2
        self.assertGreater(sdr_estimate(first)["acs_sdr_se"], 0)
        self.assertAlmostEqual(sdr_estimate(second - first)["acs_sdr_se"], 0, places=12)

    def test_recent_resident_cohort_uses_nativity_and_exact_window(self):
        frame = pd.DataFrame({"NATIVITY": [2, 2, 2, 2, 1], "POBP": [303] * 5,
                              "YOEP": [2020, 2021, 2023, 2024, 2024],
                              "HISP": [1] * 5, "RAC1P": [1] * 5})
        groups = cohort_masks(frame, 2024)
        self.assertEqual(groups["foreign_born/entry_0_3"].tolist(), [False, True, True, True, False])
        self.assertEqual(groups["foreign_born/entry_1_3"].tolist(), [False, True, True, False, False])
        self.assertEqual(groups["mexico_born/entry_d0"].tolist(), [False, False, False, True, False])

    def test_invalid_replicate_denominator_fails(self):
        with self.assertRaises(ValueError):
            ratios(np.ones(81), np.r_[1., 0., np.ones(79)])


if __name__ == "__main__":
    unittest.main()

"""Mask and variance checks independent of the full administrative-value gates."""
import unittest
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location("institutional_counts", Path(__file__).with_name("institutional_counts.py"))
lane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lane)


def fixture() -> pd.DataFrame:
    rows = [
        (24, 15, 303, 2, 2, 1, 1, 37, "GQ"),
        (25, 15, 303, 2, 2, 1, 1, 37, "GQ"),
        (34, 16, 310, 2, 2, 1, 2, 38, "GQ"),
        (35, 17, 327, 2, 2, 1, 1, 20, "HU"),
        (45, 18, 360, 2, 2, 1, 2, 37, "GQ"),
        (55, 20, 233, 2, 1, 6, 1, 20, "HU"),
        (65, 21, 1, 1, 1, 1, 1, 37, "GQ"),
        (75, 24, 1, 1, 1, 1, 2, 37, "GQ"),
        (80, 15, 303, 1, 2, 1, 1, 20, "HU"),
    ]
    data = pd.DataFrame(rows, columns=["AGEP", "SCHL", "POBP", "NATIVITY", "HISP", "RAC1P", "SEX", "RELSHIPP", "residence"])
    data["SERIALNO"] = "2024" + data.pop("residence") + "0000001"
    weights = pd.DataFrame({name: np.arange(1, len(data) + 1) for name in lane.WEIGHTS})
    return pd.concat([data, weights], axis=1)


class InstitutionalCountsTests(unittest.TestCase):
    def test_education_partition_and_boundaries(self):
        d = fixture()
        masks = lane.education_masks(d)
        self.assertTrue(np.array_equal(sum(masks[e] for e in lane.EDUCATIONS[1:]), masks["all"]))
        self.assertFalse(masks["all"][0])
        self.assertEqual(np.flatnonzero(masks["lt_hs"]).tolist(), [1, 8])
        self.assertEqual(np.flatnonzero(masks["hs_only"]).tolist(), [2, 3])
        self.assertEqual(np.flatnonzero(masks["some_college"]).tolist(), [4, 5])
        self.assertEqual(np.flatnonzero(masks["ba_plus"]).tolist(), [6, 7])

    def test_invalid_adult_education_fails(self):
        d = fixture()
        d.loc[1, "SCHL"] = 0
        with self.assertRaisesRegex(ValueError, "SCHL"):
            lane.education_masks(d)

    def test_origin_native_proxy_and_foreign_requirement(self):
        masks = lane.origin_masks(fixture())
        self.assertEqual(np.flatnonzero(masks["mexico_born"]).tolist(), [0, 1])
        self.assertEqual(np.flatnonzero(masks["all_native"]).tolist(), [6, 7, 8])
        self.assertEqual(np.flatnonzero(masks["native_nh_white"]).tolist(), [6, 7])
        self.assertTrue(np.all(sum(masks[o] for o in lane.ORIGINS[:5]) <= 1))

    def test_residence_disagreement_fails(self):
        d = fixture()
        d.loc[1, "SERIALNO"] = "2024HU0000001"
        with self.assertRaisesRegex(ValueError, "RELSHIPP"):
            lane.residence_masks(d)

    def test_accumulation_preserves_age_and_institution_types(self):
        weighted, raw = lane.empty_arrays()
        meta = {"records": 0, "national_population_all_ages": 0,
                "usborn_mexican_male_18_39_institutional": 0,
                "all_age_raw_records": {q: 0 for q in lane.QUANTITIES}}
        lane.accumulate(fixture(), weighted, raw, meta)
        mexico_all = lane.DOMAINS.index(("mexico_born", "all"))
        central_hs = lane.DOMAINS.index(("other_central_america", "hs_only"))
        native_ba = lane.DOMAINS.index(("all_native", "ba_plus"))
        self.assertEqual(int(weighted["institutional_population"][mexico_all, 0, 0]), 2)
        self.assertEqual(int(raw["population_all"][mexico_all].sum()), 1)
        self.assertEqual(int(weighted["population_all"][central_hs, 0, 0]), 3)
        self.assertEqual(int(weighted["institutional_population"][central_hs, 0, 0]), 0)
        self.assertEqual(int(weighted["household_population"][central_hs, 0, 0]), 0)
        self.assertEqual(int(weighted["institutional_population"][native_ba, 5, 0]), 8)
        self.assertEqual(int(weighted["institutional_male_population"][native_ba, 5, 0]), 0)

    def test_sdr_variance_hand_calculation(self):
        x = np.full(81, 10.0)
        x[1], x[2] = 12, 8
        self.assertAlmostEqual(float(lane.sdr_variance(x)), 0.4)

    def test_paired_contrast_preserves_shared_error(self):
        x = np.arange(81, dtype=float)
        estimate, variance = lane.contrast(x, x + 3)
        self.assertEqual(float(estimate), -3.0)
        self.assertEqual(float(variance), 0.0)

    def test_bad_replicates_fail(self):
        with self.assertRaises(ValueError):
            lane.sdr_variance(np.ones(80))
        x = np.ones(81)
        x[4] = np.nan
        with self.assertRaises(ValueError):
            lane.sdr_variance(x)


if __name__ == "__main__":
    unittest.main()

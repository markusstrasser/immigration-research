"""Domain, conservation and uncertainty tests independent of held data."""
import unittest
import json
import importlib.util
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location("education_builder", Path(__file__).with_name("builder.py"))
lane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lane)
aggregate, domain_masks, education_masks, safe_means = lane.aggregate, lane.domain_masks, lane.education_masks, lane.safe_means
sha, standardized_contrast, summarize, support = lane.sha, lane.standardized_contrast, lane.summarize, lane.support
verified_upstream_inputs = lane.verified_upstream_inputs


class DomainTests(unittest.TestCase):
    def test_completed_education_partition_and_missing_guard(self):
        d = pd.DataFrame({"A_AGE": [14, 25, 35, 45, 55, 65],
                          "A_HGA": [0, 31, 38, 39, 42, 46]})
        masks = education_masks(d)
        self.assertTrue(np.array_equal(sum(m.astype(int) for k, m in masks.items() if k != "all"), masks["all"]))
        self.assertEqual(masks["lt_hs"].sum(), 2)
        self.assertEqual(masks["hs_only"].sum(), 1)
        d.loc[1, "A_HGA"] = 0
        with self.assertRaisesRegex(ValueError, "missing/reserved"):
            education_masks(d)

    def test_foreign_origin_recent_window_and_native_separation(self):
        d = pd.DataFrame({"A_AGE": [30] * 5, "A_HGA": [39] * 5, "PRPERTYP": [2] * 5,
                          "PRCITSHP": [4, 5, 3, 5, 5], "PENATVTY": [303, 303, 303, 313, 233],
                          "PEINUSYR": [24, 25, 0, 28, 23]})
        native = d.PRCITSHP.eq(3).to_numpy()
        masks = domain_masks(d, {"all_native": native, "third_plus_nh_white": native})
        self.assertEqual(masks[("mexico_born", "all", "stock")].sum(), 2)
        self.assertEqual(masks[("mexico_born", "all", "recent_2016_2025")].sum(), 1)
        self.assertEqual(masks[("other_central_america", "hs_only", "recent_2016_2025")].sum(), 1)
        self.assertEqual(masks[("southeast_asia", "all", "stock")].sum(), 1)
        d.loc[0, "PEINUSYR"] = 0
        with self.assertRaisesRegex(ValueError, "entry code"):
            domain_masks(d, {"all_native": native, "third_plus_nh_white": native})

    def test_empty_and_dominant_weight_support(self):
        weights = np.ones((40, 161))
        bands = np.zeros(40, int)
        rows = support(np.ones(40, bool), weights, bands)
        self.assertTrue(rows[0]["support"])
        self.assertEqual(rows[1]["support_reason"], "empty")
        weights[0] = 1000
        self.assertFalse(support(np.ones(40, bool), weights, bands)[0]["support"])


class EstimatorTests(unittest.TestCase):
    def test_stale_upstream_input_and_anchor_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "infra/immigration-fiscal/ledger_absolute_2026_09_17/derived"
            output.mkdir(parents=True)
            source = root / "source.csv"
            source.write_text("source-v1")
            anchor = output / "age_profiles.csv"
            anchor.write_text("anchor-v1")
            audit = dict(inputs=[dict(path="source.csv", sha256=sha(source))],
                         age_profile_export=dict(files={anchor.name: sha(anchor)}))
            (output / "audit.json").write_text(json.dumps(audit))
            self.assertEqual(len(verified_upstream_inputs(root)), 3)
            source.write_text("source-v2")
            with self.assertRaisesRegex(ValueError, "Stale canonical repaired input"):
                verified_upstream_inputs(root)
            source.write_text("source-v1")
            anchor.write_text("anchor-v2")
            with self.assertRaisesRegex(ValueError, "Stale canonical age-profile"):
                verified_upstream_inputs(root)

    def test_signed_totals_conserve_partition_in_every_replicate(self):
        rng = np.random.default_rng(31)
        values = rng.normal(size=(36, 5))
        health = np.eye(3)[np.arange(36) % 3]
        weights = rng.uniform(1, 10, (36, 161))
        bands = np.arange(36) % 6
        full = aggregate(values, health, weights, np.ones(36, bool), bands)
        a = aggregate(values, health, weights, np.arange(36) < 18, bands)
        b = aggregate(values, health, weights, np.arange(36) >= 18, bands)
        for total, part_a, part_b in zip(full, a, b):
            np.testing.assert_allclose(total, part_a + part_b)

    def test_joint_covariance_is_not_independent_payer_errors(self):
        values = np.full(161, 50.0)
        covariance = np.array([[4.0, 3.0], [3.0, 9.0]])
        result = summarize(values, np.array([1.0, -1.0]), covariance)
        self.assertAlmostEqual(result["se_joint"], np.sqrt(7))
        values[1:] += 1
        self.assertAlmostEqual(summarize(values, np.zeros(2), covariance)["se_cps"], 2.0)

    def test_shared_reference_covariance_cancels_and_empty_support_fails(self):
        pop = np.ones((6, 161)) * 10
        total = np.tile(np.arange(6)[:, None], (1, 161)) * 100
        gradients = np.ones((6, 3)) * -5
        selected = np.array([1, 1, 1, 1, 0, 0], dtype=bool)
        shares = selected.astype(float) / 4
        values, gradient = standardized_contrast(total, pop, gradients, total, pop, gradients, shares, selected)
        np.testing.assert_array_equal(values, 0)
        np.testing.assert_array_equal(gradient, 0)
        with self.assertRaisesRegex(ValueError, "Empty"):
            standardized_contrast(total, pop, gradients, total, pop, gradients, shares, np.zeros(6, bool))
        pop[0, 1] = 0
        with self.assertRaisesRegex(ValueError, "Nonpositive"):
            standardized_contrast(total, pop, gradients, total, pop, gradients, shares, selected)

    def test_empty_age_means_stay_missing(self):
        result = safe_means(np.array([0., 20.]), np.array([0., 10.]))
        self.assertTrue(np.isnan(result[0]))
        self.assertEqual(result[1], 2)


if __name__ == "__main__":
    unittest.main()

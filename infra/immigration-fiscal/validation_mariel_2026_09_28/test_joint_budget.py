"""Guards against leakage, invalid fits and incoherent fiscal predictions."""
import unittest

import numpy as np

import joint_budget as j


class JointBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = j.ROOT / "infra/immigration-fiscal/causal_execution_2026_09_20/mariel/work/scm-june-only-panel.csv"
        cls.panels, _ = j.load_panel(source)
        cls.donors = sorted(set(cls.panels)-{j.TREATED})
        cls.train = list(range(1970, 1977))

    def test_known_convex_mixture(self):
        x = np.array([[1., 0.], [0., 1.], [1., 1.]])
        np.testing.assert_allclose(j.solve(x @ [.25, .75], x), [.25, .75], atol=1e-6)

    def test_nonfinite_fit_rejected(self):
        with self.assertRaises(ValueError):
            j.solve(np.array([1., np.nan]), np.eye(2))

    def test_future_treated_outcome_cannot_change_fit(self):
        original = j.fit_weights(self.panels, j.TREATED, self.donors, self.train, "component_relative")
        changed = {k: v.copy() for k, v in self.panels.items()}
        changed[j.TREATED].loc[1977:] *= 3
        mutated = j.fit_weights(changed, j.TREATED, self.donors, self.train, "component_relative")
        np.testing.assert_array_equal(original, mutated)

    def test_shared_weights_preserve_balance_and_components(self):
        prediction, _ = j.predict(self.panels, j.TREATED, self.donors, self.train, "component_relative")
        j.verify_identities(prediction)
        prediction.loc[1978, "balance"] += 1
        with self.assertRaises(ValueError):
            j.verify_identities(prediction)

    def test_score_discriminates_exact_and_wrong_predictions(self):
        actual = self.panels[j.TREATED]
        exact, _ = j.score(actual, actual, self.train, [1977, 1978, 1979])
        wrong, _ = j.score(actual, actual*1.2, self.train, [1977, 1978, 1979])
        self.assertEqual(exact, 0)
        self.assertGreater(wrong, 0)

    def test_invalid_scoring_normalizer_rejected(self):
        actual = self.panels[j.TREATED].copy()
        actual.loc[self.train, "Total_Revenue"] = 0
        with self.assertRaises(ValueError):
            j.score(actual, actual, self.train, [1977, 1978, 1979])


if __name__ == "__main__":
    unittest.main()

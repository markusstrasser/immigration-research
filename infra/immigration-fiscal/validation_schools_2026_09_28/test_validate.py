"""Meaningful guards against leakage, invalid identity joins and scoring errors."""
import unittest

import numpy as np
import pandas as pd

from validate import fit, pair, predict, score, supported_test, unique


class TemporalValidationTests(unittest.TestCase):
    def fixture(self):
        x = np.array([-.2, -.1, .1, .2, -.3, -.1, .15, .3])
        return pd.DataFrame(dict(leaid=[str(i) for i in range(8)], fips=[1]*4+[2]*4,
            dx=x, pupils0=np.arange(8)*100+200, current0=np.full(8, 1000.),
            current1=1000*np.exp(x), year0=2000, year1=2010))

    def test_training_year_guard(self):
        train = self.fixture()
        train.loc[0, "year1"] = 2019
        with self.assertRaisesRegex(ValueError, "Training years"):
            fit(train, "current", "free_trend", False, (2000, 2010))

    def test_training_is_invariant_to_test_outcomes(self):
        rows = []
        for leaid in range(8):
            for year, factor in ((2000, 1), (2010, 1.1), (2019, 1.2)):
                rows.append(dict(leaid=str(leaid), fips=1+leaid//4, year=year,
                    pupils=(200+leaid*20)*factor, current=(1000+leaid*100)*factor))
        data = pd.DataFrame(rows)
        before = pair(data, 2000, 2010, ["current"], "test")
        data.loc[data.year.eq(2019), "current"] = -999
        after = pair(data, 2000, 2010, ["current"], "test")
        pd.testing.assert_frame_equal(before, after)

    def test_proportional_and_frozen_have_reachable_wins(self):
        sample = self.fixture()
        proportional = fit(sample, "current", "proportional", False, (2000, 2010))
        frozen = fit(sample, "current", "frozen", False, (2000, 2010))
        np.testing.assert_allclose(predict(proportional, sample, .9), sample.dx)
        np.testing.assert_allclose(predict(frozen, sample, .9), 0)
        # A frozen endpoint favors frozen; a proportional endpoint favors proportional.
        for truth, winner in ((sample.dx.to_numpy(), proportional), (np.zeros(8), frozen)):
            self.assertAlmostEqual(float(np.square(predict(winner, sample, .9)-truth).mean()), 0)

    def test_training_trend_scaled_by_horizon(self):
        sample = self.fixture()
        sample["current1"] *= np.exp(.2)
        rule = fit(sample, "current", "free_trend", False, (2000, 2010))
        np.testing.assert_allclose(rule["beta"], [1])
        np.testing.assert_allclose(predict(rule, sample, .9), sample.dx+.18)

    def test_duplicate_and_unknown_state_fail(self):
        sample = self.fixture()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            unique(pd.concat([sample, sample.iloc[:1]]), ["leaid"], "test")
        rule = fit(sample, "current", "free_trend", False, (2000, 2010))
        sample.loc[0, "fips"] = 99
        with self.assertRaisesRegex(ValueError, "Test-state"):
            predict(rule, sample, .9)

    def test_score_known_level_and_growth_errors(self):
        rows = pd.DataFrame(dict(fips=[1, 2], actual=[100., 200.], predicted=[110., 160.],
            initial=[100., 100.], pred_log_change=np.log([1.1, 1.6]), actual_log_change=np.log([1., 2.])))
        result = score(rows, np.ones(2))
        self.assertEqual(result["level_mae"], 25.)
        self.assertEqual(result["growth_mae_pp"], 25.)
        self.assertEqual(result["aggregate_bias_percent"], -10.)

    def test_missing_training_state_only_restricts_prediction_support(self):
        train = self.fixture()
        test = train.copy()
        test.loc[0, "fips"] = 99
        supported = supported_test(train, test, "fixture")
        self.assertEqual(len(supported), 7)
        self.assertNotIn(99, supported.fips.unique())
        self.assertEqual(len(test), 8)


if __name__ == "__main__":
    unittest.main()

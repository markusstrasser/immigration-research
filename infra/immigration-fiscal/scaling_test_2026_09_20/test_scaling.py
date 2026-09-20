import unittest

import numpy as np
import pandas as pd

from analyze import absorb, finite_response, fit, predict_cv
from verification_guards import exact_models, finite_values


class ScalingTests(unittest.TestCase):
    def test_verification_rejects_corrupt_and_incomplete_exports(self):
        valid = pd.DataFrame({"model": ["a", "b"], "beta": [.75, 1.]})
        expected = [("a",), ("b",)]
        exact_models(valid, ["model"], expected, ["beta"])
        for bad in [valid.iloc[:1], pd.concat([valid, valid.iloc[:1]]),
                    valid.assign(model=["a", "c"]), valid.assign(beta=[np.nan, 1.]),
                    valid.assign(beta=[np.inf, 1.])]:
            with self.subTest(values=bad.to_dict()), self.assertRaises(ValueError):
                exact_models(bad, ["model"], expected, ["beta"])
        for bad in [np.nan, np.inf, -np.inf]:
            with self.assertRaises(ValueError):
                finite_values(bad)

    def test_finite_removal_is_not_local_derivative(self):
        self.assertAlmostEqual(finite_response(1, .12), 1.)
        self.assertAlmostEqual(finite_response(0, .12), 0.)
        self.assertAlmostEqual(finite_response(5/6, 1e-8), 5/6, places=8)
        self.assertGreater(finite_response(5/6, .12), 5/6)
        self.assertAlmostEqual(finite_response(.75, .12), (1-.88**.75)/.12)
        with self.assertRaises(ValueError):
            finite_response(.75, 1.)

    def test_absorbed_weighted_slope_matches_explicit_dummy_ols(self):
        rng = np.random.default_rng(73)
        d = pd.DataFrame([(s, f"{s}-{j}", y) for s in range(4) for j in range(5) for y in range(3)],
                         columns=["fips", "leaid", "year"])
        d["state_year"] = d.fips.astype(str)+"_"+d.year.astype(str)
        d["x"] = rng.normal(size=len(d))
        d["w"] = d.leaid.map({g: i+1 for i, g in enumerate(d.leaid.unique())})
        d["y"] = .8*d.x + d.leaid.factorize()[0] + 2*d.year + rng.normal(size=len(d))*.1
        root = np.sqrt(d.w.to_numpy())
        design = np.column_stack([d.x, pd.get_dummies(d.leaid), pd.get_dummies(d.state_year)])
        beta = np.linalg.lstsq(design*root[:, None], d.y*root, rcond=None)[0][0]
        result = fit(d, "y", ["x"], ["leaid", "state_year"], 28, "w")[0]
        self.assertAlmostEqual(beta, result["beta"], places=10)
        residual = absorb(d[["x", "y"]], [d.leaid, d.state_year], d.w.to_numpy())
        self.assertLess(np.max(np.abs(pd.DataFrame(residual*d.w.to_numpy()[:, None]).groupby(d.leaid).sum())), 1e-7)

    def test_cv_excludes_unsupported_state_and_predicts_exact_power(self):
        rows = [dict(fips=s, leaid=f"{s:02d}{j:05d}", year=2019, log_pupils=float(j),
                     log_current=float(s)+.85*j) for s in range(3) for j in range(10)]
        rows.append(dict(fips=15, leaid="1500001", year=2019, log_pupils=1., log_current=1.))
        scored = predict_cv(pd.DataFrame(rows)).set_index("model")
        self.assertLess(scored.loc["point85", "log_rmse"], 1e-12)
        self.assertLess(scored.loc["free", "log_rmse"], 1e-12)
        self.assertGreater(scored.loc["linear", "log_rmse"], .1)
        self.assertEqual(scored.loc["free", "n"], 30)
        self.assertEqual(scored.loc["free", "excluded_rows"], 1)


if __name__ == "__main__":
    unittest.main()

"""Independent numerical and limiting-case oracles for the CES scenarios."""
import unittest

import numpy as np

from model import equilibrium, fiscal_and_private


class ModelTests(unittest.TestCase):
    def test_zero_and_homogeneous_limits(self):
        shares = np.array([.3, .7])
        for adjustment in (0., .5, 1.):
            for elasticity in (0., .33):
                zero = equilibrium(shares, np.zeros(2), 2., .65, adjustment, elasticity)
                self.assertAlmostEqual(float(zero["gross_income_gain"]), 0., places=13)
                np.testing.assert_allclose(zero["wage_without_over_with"], 1.)
        m, s = .1, .65
        for sigma in (1., 1.5, 2.5, np.inf):
            fixed = equilibrium(shares, np.full(2, m), sigma, s, 0., 0.)
            self.assertAlmostEqual(float(fixed["gross_income_gain"]), 1 - s*m - (1-m)**s, places=13)
            adjusted = equilibrium(shares, np.full(2, m), sigma, s, 1., 0.)
            self.assertAlmostEqual(float(adjusted["gross_income_gain"]), 0., places=13)

    def test_independent_finite_difference_factor_prices(self):
        # Different implementation: level production, numerical derivatives;
        # no CES wage-ratio formula or Euler share formula from the model.
        shares, target, s, sigma = np.array([.31, .69]), np.array([.19, .04]), .65, 2.
        rho = 1 - 1/sigma
        def output(k, labor):
            return k**(1-s) * np.sum(shares * labor**rho)**(s/rho)
        for adjustment in (0., .5, 1.):
            result = equilibrium(shares, target, sigma, s, adjustment, 0.)
            labor, k, step = 1-target, result["capital_without_over_with"], 1e-5
            wages = []
            for j in range(2):
                delta = np.eye(2)[j] * step
                wages.append((output(k, labor+delta)-output(k, labor-delta))/(2*step))
            rent = (output(k+step, labor)-output(k-step, labor))/(2*step)
            current_outside = s*np.dot(shares, 1-target) + (1-s)
            without = np.dot(wages, labor) + rent*k + (1-s)*(1-k)
            self.assertAlmostEqual(float(result["gross_income_gain"]), current_outside-without, places=9)
            np.testing.assert_allclose(wages/(s*shares), result["wage_without_over_with"], rtol=1e-9)

    def test_small_shock_and_complete_substitution(self):
        s, shares = .65, np.array([.3, .7])
        m = 1e-5
        result = equilibrium(shares, np.full(2, m), 2., s, 0., 0.)
        np.testing.assert_allclose(result["gross_income_gain"], .5*s*(1-s)*m*m, rtol=1e-4, atol=0)
        adjusted = equilibrium(shares, np.array([.2, .03]), np.inf, s, 1., 0.)
        self.assertAlmostEqual(float(adjusted["gross_income_gain"]), 0., places=13)

    def test_endogenous_labor_and_tax_opportunity_cost(self):
        result = equilibrium([.3, .7], [.2, .04], 2., .65, 1., .33)
        np.testing.assert_allclose(result["hours_without_over_with"], result["wage_without_over_with"]**.33, rtol=2e-12)
        # Alternative equilibrium solved through undamped numerical Newton,
        # with explicit factor-price finite differences, independent of solver.
        shares, remaining, s, rho, e = np.array([.3, .7]), np.array([.8, .96]), .65, .5, .33
        def residual(log_h):
            labor = remaining * np.exp(log_h)
            q = np.sum(shares * labor**rho)**(1/rho)
            def y(l):
                return q**(1-s) * np.sum(shares*l**rho)**(s/rho)
            wages = np.array([(y(labor+np.eye(2)[j]*1e-5)-y(labor-np.eye(2)[j]*1e-5))/2e-5 for j in range(2)])
            return log_h-e*np.log(wages/(s*shares))
        point = np.zeros(2)
        for _ in range(10):
            value = residual(point)
            jac = np.column_stack([(residual(point+np.eye(2)[j]*1e-4)-residual(point-np.eye(2)[j]*1e-4))/2e-4 for j in range(2)])
            point -= np.linalg.solve(jac, value)
        np.testing.assert_allclose(np.exp(point), result["hours_without_over_with"], rtol=1e-8)
        retained = fiscal_and_private(result, [.384, .426], .246, 1.)
        lost = fiscal_and_private(result, [.384, .426], .246, 0.)
        self.assertAlmostEqual(float(retained["capital_tax_gain"]), 0., places=13)
        self.assertGreater(float(lost["current_receipts_gain"]), float(retained["current_receipts_gain"]))
        self.assertAlmostEqual(float(retained["private_plus_receipts"]), float(lost["private_plus_receipts"]), places=13)
        external = fiscal_and_private(result, [.384, .426], .246, 0., 1.)
        self.assertAlmostEqual(float(external["private_plus_receipts"]-lost["private_plus_receipts"]),
                               float(lost["capital_tax_gain"]-result["capital_gain"]), places=13)

    def test_invalid_calibration_fails_loudly(self):
        for shares, target in [([.2, .7], [.1, .2]), ([.3, .7], [1., .2]), ([.3, .7], [np.nan, .2])]:
            with self.assertRaises(ValueError):
                equilibrium(shares, target)

    def test_colas_sachs_marginal_tax_formula(self):
        # Source's fixed-labor marginal redistribution formula, with capital
        # fully adjusted and alternative capital taxes retained domestically.
        shares, s, sigma, shock = np.array([.21, .79]), .65, 2., 1e-5
        result = equilibrium(shares, [shock, 0.], sigma, s, 1., 0.)
        taxes = fiscal_and_private(result, [.303, .366], .246, 1.)
        expected = s*shares[0]*shock * shares[1]/sigma * (.366-.303)
        np.testing.assert_allclose(taxes["labor_tax_gain"], expected, rtol=5e-5, atol=0)


if __name__ == "__main__":
    unittest.main()

"""Limiting-case and independent-oracle tests for the branch nest.

Synthetic shares only: these run without the CPS extract. The unnested model of
`matched_benefits_2026_09_19/model.py` is the oracle for every collapse test; the
flat single-level CES written here is an independent oracle for the case the
collapses cannot reach.
"""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / "matched_benefits_2026_09_19"))

import nest_model as nest  # noqa: E402
from model import equilibrium, fiscal_and_private  # noqa: E402

SHARES = np.array([.215366, .784634])
# Four-branch calibration in the shape of the CPS probe: native non-union,
# union US-born, other foreign-born, union Mexico-born; dollars per skill cell.
DOLLARS = np.array([[1828.61, 7607.74], [228.80, 442.39],
                    [395.06, 1684.58], [253.72, 124.67]])
FOUR = DOLLARS / DOLLARS.sum(axis=0)
NATIVE, FOREIGN = FOUR[0] + FOUR[1], FOUR[2] + FOUR[3]
BRANCHES = np.stack([NATIVE, FOREIGN])
REMOVED = np.stack([FOUR[1] / NATIVE, FOUR[3] / FOREIGN])
UNION = (BRANCHES * REMOVED).sum(axis=0)
GRID = (1.3, 3., 4.6, 5., 7., 20., np.inf)
COMPARED = ("labor_gain", "capital_gain", "domestic_capital_gain", "opportunity_income",
            "gross_income_gain", "disutility_difference", "output_without_over_with",
            "capital_without_over_with")


def flat_ces(shares, branch_shares, removed, sigma, labor_share, adjustment):
    """One-level CES over every branch-cell pair; no nest code is reused."""
    rho, power = 1 - 1 / sigma, labor_share + adjustment * (1 - labor_share)
    weights, quantity = (shares * branch_shares).ravel(), (1 - removed).ravel()
    aggregate = (weights * quantity**rho).sum()**(1 / rho)
    output, capital = aggregate**power, aggregate**adjustment
    wage = aggregate**(power - rho) * quantity**(rho - 1)
    current = labor_share * weights * quantity
    return float((current - current * wage).sum()
                 + (1 - labor_share) * (capital - output))


def same(actual, expected, message):
    np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-15, err_msg=message)


class NestTests(unittest.TestCase):
    def test_zero_shock_leaves_the_economy_unchanged(self):
        """G5: with nothing removed every gain is zero at every elasticity."""
        for epsilon in GRID:
            for adjustment in (0., .5, 1.):
                for elasticity in (0., .33):
                    result = nest.nested_equilibrium(
                        SHARES, BRANCHES, np.zeros((2, 2)), 2., epsilon, .65,
                        adjustment, elasticity)
                    self.assertAlmostEqual(float(result["gross_income_gain"]), 0., places=14)
                    same(result["wage_without_over_with"], 1., f"wage at {epsilon}")
                    same(result["cell_quantity_without_over_with"], 1., f"cell at {epsilon}")
                    same(result["labor_gain"], 0., f"gain at {epsilon}")

    def test_single_branch_reproduces_the_unnested_model(self):
        """A one-branch nest is the existing model at any nest elasticity."""
        for epsilon in GRID:
            for sigma in (1.5, 2., 2.5):
                for adjustment in (0., .5, 1.):
                    for elasticity in (0., .33):
                        base = equilibrium(SHARES, UNION, sigma, .65, adjustment, elasticity)
                        got = nest.nested_equilibrium(
                            SHARES, np.ones((1, 2)), UNION[None, :], sigma, epsilon,
                            .65, adjustment, elasticity)
                        for key in COMPARED:
                            same(got[key], base[key], f"{key} at eps={epsilon} sigma={sigma}")

    def test_proportional_removal_collapses_at_every_epsilon(self):
        """G3: a removal proportional across branches is the unnested model exactly.

        This is the satisfiable form of "the nest is a strict generalization": it
        holds at every epsilon, not only at epsilon = sigma. See
        test_literal_spec_g3_is_not_an_identity for why the SPEC wording cannot hold.
        """
        proportional = np.stack([UNION, UNION])
        for epsilon in GRID:
            for sigma in (1.5, 2., 2.5):
                for adjustment in (0., .5, 1.):
                    for elasticity in (0., .33):
                        base = equilibrium(SHARES, UNION, sigma, .65, adjustment, elasticity)
                        got = nest.nested_equilibrium(
                            SHARES, BRANCHES, proportional, sigma, epsilon, .65,
                            adjustment, elasticity)
                        for key in COMPARED:
                            same(got[key], base[key], f"{key} at eps={epsilon} sigma={sigma}")
                        for retention in (0., .5, 1.):
                            expected = fiscal_and_private(base, [.384, .426], .246, retention)
                            actual = fiscal_and_private(got, [.384, .426], .246, retention)
                            for key, value in expected.items():
                                same(actual[key], value, f"{key} at eps={epsilon}")

    def test_perfect_substitution_limit_reproduces_the_account(self):
        """G4: epsilon = infinity with the real uneven removal is the existing model."""
        for sigma in (1.5, 2., 2.5):
            for adjustment in (0., .5, 1.):
                for elasticity in (0., .33):
                    base = equilibrium(SHARES, UNION, sigma, .65, adjustment, elasticity)
                    got = nest.nested_equilibrium(SHARES, BRANCHES, REMOVED, sigma,
                                                  np.inf, .65, adjustment, elasticity)
                    for key in COMPARED:
                        same(got[key], base[key], f"{key} at sigma={sigma}")
                    # Every branch faces one cell wage when substitution is perfect.
                    same(got["wage_without_over_with"][0],
                         got["wage_without_over_with"][1], "branch wages differ at infinity")
                    for retention in (0., .5, 1.):
                        for owner in (0., .5, 1.):
                            expected = fiscal_and_private(base, [.384, .426], .246, retention, owner)
                            actual = fiscal_and_private(got, [.384, .426], .246, retention, owner)
                            for key, value in expected.items():
                                same(actual[key], value, f"partition {key}")

    def test_epsilon_equals_sigma_matches_an_independent_flat_ces(self):
        """At kappa = rho the nest is a single-level CES over branch-cell pairs."""
        for sigma in (1.5, 2., 2.5):
            for adjustment in (0., .5, 1.):
                got = nest.nested_equilibrium(SHARES, BRANCHES, REMOVED, sigma,
                                              sigma, .65, adjustment, 0.)
                want = flat_ces(SHARES, BRANCHES, REMOVED, sigma, .65, adjustment)
                np.testing.assert_allclose(float(got["gross_income_gain"]), want,
                                           rtol=1e-12, atol=1e-16)

    def test_literal_spec_g3_is_not_an_identity(self):
        """SPEC section 5 G3 as worded is unsatisfiable; record the size of the gap.

        At kappa = rho the cell aggregate is a power mean of branch quantities,
        while the unnested model uses their arithmetic mean. Jensen separates the
        two whenever the removal is uneven across branches, so demanding 1e-12
        agreement at epsilon = sigma with the real shock asks for a false identity.
        """
        base = equilibrium(SHARES, UNION, 2., .65, 1., 0.)
        got = nest.nested_equilibrium(SHARES, BRANCHES, REMOVED, 2., 2., .65, 1., 0.)
        arithmetic = 1 - UNION
        power_mean = got["cell_quantity_without_over_with"]
        self.assertTrue(np.all(power_mean < arithmetic))
        gap = abs(float(got["gross_income_gain"]) / float(base["gross_income_gain"]) - 1)
        self.assertGreater(gap, .5)

    def test_small_shock_matches_the_linearization(self):
        """G8: the exact solver meets the section 3.2 formulas to first order."""
        for epsilon in (1.3, 3., 20., np.inf):
            previous = None
            for shock in (1e-2, 1e-4, 1e-6):
                removed = np.zeros((2, 2))
                removed[1, 0] = shock
                exact = np.log(nest.nested_equilibrium(
                    SHARES, BRANCHES, removed, 2., epsilon, .65, 1., 0.
                )["wage_without_over_with"])
                linear = nest.linearized_wage_response(SHARES, BRANCHES, 0, 2., epsilon,
                                                       np.log(1 - shock), 1)
                self.assertEqual(np.sign(exact).tolist(), np.sign(linear).tolist())
                deviation = float(np.max(np.abs(exact - linear) / np.abs(linear)))
                self.assertLess(deviation, 5 * shock, f"eps={epsilon} shock={shock}")
                if previous is not None:
                    # First-order error falls with the shock, not slower.
                    self.assertLess(deviation, previous / 50)
                previous = deviation

    def test_euler_and_partition_hold_across_replicates(self):
        """G6: cell-level and total Euler plus the tax identity on a replicate axis."""
        generator = np.random.default_rng(20260922)
        jitter = 1 + .05 * generator.standard_normal((2, 17))
        shares = SHARES[:, None] * jitter
        shares /= shares.sum(axis=0)
        branches = np.repeat(BRANCHES[:, :, None], 17, axis=2)
        removed = np.repeat(REMOVED[:, :, None], 17, axis=2)
        for epsilon in GRID:
            for elasticity in (0., .33):
                got = nest.nested_equilibrium(shares, branches, removed, 2., epsilon,
                                              .65, .5, elasticity)
                pay = got["counterfactual_pay_by_branch"].sum(axis=0)
                cell = got["cell_quantity_without_over_with"]
                q = got["output_without_over_with"]**(1 / (.65 + .5 * .35))
                expected = .65 * shares * q**(.65 + .5 * .35 - .5) * cell**.5
                same(pay, expected, f"cell Euler at {epsilon}")
                same(pay.sum(axis=0), .65 * got["output_without_over_with"],
                     f"total Euler at {epsilon}")
                self.assertEqual(got["labor_gain"].shape, (2, 17))
                partition = fiscal_and_private(got, [.384, .426], .246, .5, .5)
                self.assertTrue(np.isfinite(partition["private_plus_receipts"]).all())

    def test_exact_drop_is_the_limit_of_the_delta_floor(self):
        """Option B removal: dropping the term is the delta to zero limit."""
        three = np.stack([FOUR[0], FOUR[2], FOUR[1] + FOUR[3]])
        removed = np.stack([np.zeros(2), np.zeros(2), np.ones(2)])
        for epsilon in (1.3, 3., 20., np.inf):
            exact = float(nest.nested_equilibrium(SHARES, three, removed, 2., epsilon,
                                                  .65, 1., 0., dropped=(2,))["gross_income_gain"])
            previous = None
            for delta in (1e-6, 1e-9, 1e-12):
                floored = removed.copy()
                floored[2] = 1 - delta
                approximate = float(nest.nested_equilibrium(
                    SHARES, three, floored, 2., epsilon, .65, 1., 0.)["gross_income_gain"])
                deviation = abs(approximate / exact - 1)
                if previous is not None:
                    self.assertLess(deviation, previous)
                previous = deviation
            self.assertLess(previous, 1e-2)

    def test_three_level_nest_absorbs_into_two_when_elasticities_match(self):
        """B_deep with sigma_FT = epsilon is the flat three-branch nest."""
        inner = np.stack([FOUR[2], FOUR[3]]) / FOREIGN
        flat = np.stack([NATIVE, FOREIGN * inner[0], FOREIGN * inner[1]])
        removed = np.stack([FOUR[1] / NATIVE, np.zeros(2), np.ones(2)])
        for epsilon in (3., 20.):
            tree = nest.three_level(BRANCHES, epsilon, 1, inner, epsilon)
            deep = nest.solve(SHARES, tree, removed, 2., .65, 1., 0., dropped=(2,))
            shallow = nest.nested_equilibrium(SHARES, flat, removed, 2., epsilon,
                                              .65, 1., 0., dropped=(2,))
            for key in COMPARED:
                same(deep[key], shallow[key], f"{key} at eps={epsilon}")

    def test_invalid_inputs_fail_loudly(self):
        cases = [
            (np.array([.2, .7]), BRANCHES, REMOVED, {}),
            (SHARES, BRANCHES, np.stack([[1., .1], [.2, .3]]), {}),
            (SHARES, BRANCHES, -REMOVED, {}),
            (SHARES, BRANCHES, np.stack([[np.nan, .1], [.2, .3]]), {}),
            (SHARES, np.stack([[.5, .5], [.4, .4]]), REMOVED, {}),
            (SHARES, np.stack([[.7, .8], [-.3, .2]]), REMOVED, {}),
            (SHARES, BRANCHES, REMOVED, dict(sigma=0.)),
            (SHARES, BRANCHES, REMOVED, dict(labor_share=1.)),
            (SHARES, BRANCHES, REMOVED, dict(adjustment=1.5)),
            (SHARES, BRANCHES, REMOVED, dict(elasticity=-.1)),
            (SHARES, BRANCHES, REMOVED, dict(sigma_ni=0.)),
            (SHARES, BRANCHES, REMOVED, dict(sigma_ni=np.nan)),
            (SHARES, BRANCHES, np.zeros((3, 2)), {}),
            (np.array([.3, .3, .4]), np.ones((1, 3)), np.zeros((1, 3)), {}),
        ]
        for shares, branches, removed, extra in cases:
            with self.assertRaises(ValueError):
                nest.nested_equilibrium(shares, branches, removed, **extra)
        # A branch at full removal must be declared dropped, and vice versa.
        with self.assertRaises(ValueError):
            nest.nested_equilibrium(SHARES, BRANCHES, np.stack([np.zeros(2), np.ones(2)]),
                                    2., 3.)
        with self.assertRaises(ValueError):
            nest.nested_equilibrium(SHARES, BRANCHES, REMOVED, 2., 3., dropped=(1,))
        with self.assertRaises(ValueError):
            nest.nested_equilibrium(SHARES, np.ones((1, 2)), np.ones((1, 2)),
                                    2., 3., dropped=(0,))


if __name__ == "__main__":
    unittest.main()

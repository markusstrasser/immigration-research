"""Scoped epsilon controls against analytic CES and finite descendant additions."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p8 = load("p8_nest", HERE / "p7_nest.py")
model = load("p8_producer_nest", HERE.parent / "production_nativity_nest_2026_09_22/nest_model.py")


@pytest.mark.parametrize("epsilon", [8.7, 17.9, np.inf])
def test_scoped_nest_matches_independent_ces_equations(epsilon):
    shares = np.array([[.35], [.65]])
    branches = np.array([[[.8], [.75]], [[.2], [.25]]])
    removed = np.array([[[.08], [.03]], [[.4], [.12]]])
    tree = model.two_level(branches, epsilon)
    result = p8.low_skill_solve(model, shares, tree, removed, 2., .65, 1.)
    quantities = 1 - removed
    kappa = 1 if np.isinf(epsilon) else 1 - 1 / epsilon
    cell = np.array([((branches[:, 0] * quantities[:, 0] ** kappa).sum(axis=0)) ** (1 / kappa),
                     (branches[:, 1] * quantities[:, 1]).sum(axis=0)])
    q = ((shares * np.sqrt(cell)).sum(axis=0)) ** 2
    expected = np.sqrt(q / cell)[None, :, :] * np.ones_like(removed)
    expected[:, 0] *= quantities[:, 0] ** (kappa - 1) * cell[0] ** (1 - kappa)
    np.testing.assert_allclose(result["wage_without_over_with"], expected, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(result["wage_without_over_with"][0, 1], result["wage_without_over_with"][1, 1], atol=1e-12)
    assert result["wage_without_over_with"][0, 1, 0] != pytest.approx(1.)
    # This fails if a global adapter accidentally changes the producer model.
    original = model.solve(shares, tree, removed, 2., .65, 1.)
    if np.isinf(epsilon):
        np.testing.assert_allclose(result["wage_without_over_with"], original["wage_without_over_with"], atol=1e-12)
    else:
        assert original["wage_without_over_with"][0, 1, 0] != pytest.approx(original["wage_without_over_with"][1, 1, 0])


def synthetic_row(epsilon, low_scale=1., capital=0.):
    bases = {("native", 0): 400., ("other_fb", 0): 100., ("native", 1): 800., ("other_fb", 1): 200.}
    tau = np.array([.384, .426])
    row = pd.Series(dict(sigma_NI=epsilon, wage_pct_native_cell0=-2. * low_scale,
                         wage_pct_other_fb_cell0=3. * low_scale,
                         wage_pct_native_cell1=.5, wage_pct_other_fb_cell1=.5,
                         capital_gain_bn=capital, capital_tax_gain_bn=capital * .246,
                         capital_private_residual_bn=capital * (1 - .246)))
    wages = np.array([5. * low_scale, -5.])
    row["native_production_gain_bn"] = (1 - tau[0]) * 8. * low_scale - (1 - tau[1]) * 4.
    row["other_immigrant_production_gain_bn"] = -(1 - tau[0]) * 3. * low_scale - (1 - tau[1])
    row["induced_current_receipts_bn"] = tau @ wages + row.capital_tax_gain_bn
    row["private_plus_receipts_bn"] = row.native_production_gain_bn + row.other_immigrant_production_gain_bn + row.capital_private_residual_bn + row.induced_current_receipts_bn
    return row, bases, tau


@pytest.mark.parametrize("capital", [0., 3.])
def test_finite_descendants_recompute_multipliers_and_keep_both_added_totals(capital):
    infinite, bases, tau = synthetic_row(np.inf, capital=capital)
    finite, _, _ = synthetic_row(8.7, low_scale=2., capital=capital)
    infinity_added, infinity_meta = p8.recompute_lineage_row(infinite, bases, tau, .15, .08)
    finite_added, finite_meta = p8.recompute_lineage_row(finite, bases, tau, .15, .08)
    assert finite_meta["lambda_cell0"] != pytest.approx(infinity_meta["lambda_cell0"])
    for before, after, metadata in ((infinite, infinity_added, infinity_meta), (finite, finite_added, finite_meta)):
        private = lambda r: r.native_production_gain_bn + r.other_immigrant_production_gain_bn + r.capital_private_residual_bn
        assert private(after) - private(before) == pytest.approx(.15)
        assert after.induced_current_receipts_bn - before.induced_current_receipts_bn == pytest.approx(.08)
        assert metadata["max_abs_closure_bn"] < 1e-12
        # Reusing the sibling lambda gives twice the descendant increment in the
        # changed low-skill wage bill and therefore fails one or both totals.
    assert finite_added.wage_pct_native_cell0 != pytest.approx(finite.wage_pct_native_cell0 * infinity_meta["lambda_cell0"])


def test_low_skill_solve_rejects_a_nested_or_target_branch_tree():
    tree = model.two_level(np.full((3, 2, 1), 1 / 3), 8.7)
    with pytest.raises(ValueError, match="two-branch"):
        p8.low_skill_solve(model, np.full((2, 1), .5), tree, np.zeros((3, 2, 1)), 2., .65, 1.)

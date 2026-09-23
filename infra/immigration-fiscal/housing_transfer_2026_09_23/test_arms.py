"""Checks for the rent-path arithmetic in arms.py.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/housing_transfer_2026_09_23/ -q
"""
import importlib.util
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("arms", HERE / "arms.py")
arms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arms)


def test_unit_elasticity_attributes_the_population_share():
    f, _ = arms.effect("A", 1.0, np.array([0.12, 0.35]))
    assert np.allclose(f, [0.12, 0.35])


def test_kappa_is_one_half_for_a_small_linear_shock():
    _, kappa = arms.effect("B", 1.5, np.array([1e-4]))
    assert abs(kappa[0] - 0.5) < 1e-6


def test_fixed_stock_welfare_equals_the_integral():
    # Fixed stock S; the group's H_g units come out of other renters' consumption along the
    # rent path. Other residents own the stock. Net for others = S dP - integral of their own
    # consumption over the path, which must equal kappa * H_g * dP.
    s, e, stock, h_g = 0.3, 1.5, 100.0, 30.0
    lam = np.linspace(0, 1, 200001)
    p = (1 + lam * s / (1 - s)) ** e
    others = stock - lam * h_g
    loss = np.sum(0.5 * (others[1:] + others[:-1]) * np.diff(p))
    direct = stock * (p[-1] - p[0]) - loss
    _, kappa = arms.effect("A", e, np.array([s]))
    # arms.LAMBDA has 401 points; the trapezoid error is of order 1e-7 relative.
    assert abs(direct / (kappa[0] * h_g * (p[-1] - p[0])) - 1) < 1e-5


def test_support_limited_form_matches_short_run_inside_support():
    small = np.array([0.02])
    fa, _ = arms.effect("A", 1.5, small)
    fd, _ = arms.effect("D", 1.5, small, arms.ARMS["long_run"]["central"])
    assert np.allclose(fa, fd)
    big = np.array([0.12])
    fa, _ = arms.effect("A", 1.5, big)
    fd, _ = arms.effect("D", 1.5, big, arms.ARMS["long_run"]["central"])
    assert fd < fa


def test_long_run_land_elasticity():
    # a / (1 - a (1 - eD)) at a = 0.35, eD = 0.7.
    assert abs(arms.ARMS["long_run"]["central"] - 0.35 / 0.895) < 1e-12

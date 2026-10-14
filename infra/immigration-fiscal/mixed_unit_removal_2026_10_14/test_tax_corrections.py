"""Primary-table and accounting regressions for lane-local tax corrections."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tested_tax_corrections", LANE / "tax_corrections.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_pinned_primary_IRS_table_roundtrip_and_schedule():
    pins = M.verify_sources()
    table = pd.read_csv(M.TABLE)
    assert len(table) == pins["parsed_rows"]
    assert len(table) > 10600
    parsed = M.parse_irs_table(M.TEXT.read_text())
    pd.testing.assert_frame_equal(table, parsed.reset_index(drop=True))
    midpoint = (table.income_at_least + table.income_less_than) / 2
    actual = M.corrected_eitc(table.kids, midpoint, midpoint, table.joint,
                              np.zeros(len(table)), np.ones(len(table), bool))
    # Four IRS intervals straddle a statutory kink; table's interval convention
    # takes the plateau there. They are explicitly verified separately below.
    crossing = np.zeros(len(table), bool)
    for kids, (pin, maximum, _, single_start, joint_start) in M.EITC.items():
        for threshold in (maximum / pin, single_start, joint_start):
            crossing |= ((table.kids == kids) & (table.income_at_least < threshold)
                          & (table.income_less_than > threshold))
    assert np.max(np.abs(actual[~crossing] - table.credit.to_numpy()[~crossing])) <= .51
    assert np.max(np.abs(actual[crossing] - table.credit.to_numpy()[crossing])) <= 5.5
    selected = table.query("income_at_least == 22700 and joint == 0 and kids >= 2")
    assert selected.credit.tolist() == [6960, 7830]


def test_low_earnings_high_AGI_takes_smaller_of_table_credits():
    table = pd.read_csv(M.TABLE)
    earned, agi = 5025., 25025.
    first = table.query("income_at_least == 5000 and joint == 0 and kids == 1").credit.item()
    second = table.query("income_at_least == 25000 and joint == 0 and kids == 1").credit.item()
    actual = M.corrected_eitc([1], [earned], [agi], [False], [0], [True]).item()
    assert actual == pytest.approx(min(first, second), abs=.51)
    broken = min(.34 * earned, 4213) - .1598 * (agi - 22720)
    assert actual - broken > 300


def test_lane_local_taxcalc_fix_changes_EITC_only():
    path = LANE.parent / "cps_imputation_keys_2026_09_23/taxcalc.py"
    module = M.load(path, "tested_frozen_taxcalc")
    args = (np.array([25025.]), np.array([5025.]), np.array([0.]),
            np.array(["hoh"]), np.array([1]), np.array([1]),
            np.array([0]), np.array([0]), np.array([40]))
    old = module.compute(*args)
    digest = M.sha(path)
    M.install_eitc_fix(module)
    M.install_eitc_fix(module)  # Idempotent; no wrapper recursion.
    new = module.compute(*args)
    np.testing.assert_array_equal(new[0], old[0])
    np.testing.assert_array_equal(new[2], old[2])
    assert new[1][0] == pytest.approx(.34 * 5025)
    assert new[1][0] - old[1][0] > 300
    assert M.sha(path) == digest


def test_EITC_age_and_investment_are_separate_eligibility_gates():
    actual = M.corrected_eitc([0, 0, 1, 1], [10000]*4, [10000]*4,
                              [False]*4, [0, 0, 11600, 11601], [False, True, False, True])
    np.testing.assert_allclose(actual, [0, 632, 3400, 0], atol=1e-9)


def test_high_AGI_crossing_recomputes_residual_not_scalar():
    weights = np.ones((1, 161))
    owner = np.array([[1.], [0.], [0.]])
    zero = np.zeros((3, 161))
    result, audit = M.high_agi_delta(
        np.array([80.]), np.array([400000.]), np.array([1.]), np.array([True]), weights,
        np.array([100.]), np.array([600000.]), np.array([1.]), np.array([True]), weights,
        owner, 1000., np.full(161, 10000.), np.full(161, 1000.), 2000., zero)
    # Liability change -2; loss of high-AGI residual allocation -100.
    np.testing.assert_allclose(result[0], np.full(161, -102.))
    assert audit["high_AGI_residual_delta_bn"] == -100
    assert audit["generation_closure_bn"] < 1e-9


def test_high_AGI_uses_survivor_factor_and_weights_but_unruled_high_key():
    after_weights = np.full((1, 161), 3.)
    before_weights = np.full((1, 161), 2.)
    owner = np.array([[0.], [1.], [0.]])
    booked = np.zeros((3, 161))
    booked[1] = -7.
    result, _ = M.high_agi_delta(
        np.array([80.]), np.array([600000.]), np.array([1.]), np.array([True]), after_weights,
        np.array([100.]), np.array([600000.]), np.array([.5]), np.array([True]), before_weights,
        owner, 1000., np.full(161, 10000.), np.full(161, 1000.), 2000., booked)
    # liability +14; high key +40; remove old booked edit -7 once.
    np.testing.assert_allclose(result[1], np.full(161, 61.))


def test_high_AGI_missing_denominator_blocks():
    w = np.ones((1, 161))
    a = np.ones(1)
    with pytest.raises(ValueError, match="nonpositive national key"):
        M.high_agi_delta(a, a, a, a, w, a, a, a, a, w,
                         np.array([[1.], [0.], [0.]]), 1., np.zeros(161),
                         np.ones(161), 2., np.zeros((3, 161)))


def test_pinned_TAXSIM_survivor_EITC_passes_defect_regression():
    tax = M.load(LANE / "state_tax.py", "tax_corrections_test_taxsim")
    result = M.assert_eitc_used(tax)
    assert result["passed"]
    assert result["kernel_credit_usd"] == pytest.approx(.34 * 5025)


def test_wrong_survivor_EITC_kernel_blocks():
    class Broken:
        @staticmethod
        def run_taxsim(_frame):
            return pd.DataFrame({"v25": [1340.16], "v10": [25025.]})
    with pytest.raises(ValueError, match="actual survivor kernel EITC fails IRS table"):
        M.assert_eitc_used(Broken)

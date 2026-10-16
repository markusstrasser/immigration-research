"""Independent statutory examples and counterfactual-isolation regressions."""
import numpy as np
import pandas as pd
import bound


def test_payroll_cap_and_self_employment():
    # SSA 2024: combined 12.4% up to168600, 2.9% uncapped;
    # SE uses92.35% net earnings with the residual individual OASDI cap.
    np.testing.assert_allclose(bound.payroll([10000, 200000, 0, 168600],
                                             [0, 0, 10000, 10000]),
                               [1530, 26706.4, 1412.955, 25795.8 + 267.815])
    assert bound.payroll(0, 400) == 0  # net SE base is below400
    assert bound.payroll(0, -10000) == 0


def test_additional_medicare_joint_threshold_and_wage_se_order():
    f = pd.DataFrame({'mstat': [1, 1, 2, 2], 'pwages': [210000, 225000, 200000, 200000],
                      'swages': [0, 0, 60000, 0], 'psemp': [0, 10000, 0, 100000], 'ssemp': 0})
    np.testing.assert_allclose(bound.additional_medicare(f), [90, 308.115, 90, 381.15])


def test_shock_preserves_losses_other_people_and_frozen_baseline():
    d = pd.DataFrame({'WSAL_VAL': [100, 0, 0, 80], 'SEMP_VAL': [-20, 20, -10, 0],
                      'FRSE_VAL': [0, -5, 0, 0]})
    original = d.copy()
    changed, delta = bound.change_earnings(d, np.array([True, True, True, False]), -1)
    np.testing.assert_array_equal(delta, [-100, -15, 0, 0])
    np.testing.assert_array_equal(changed.SEMP_VAL + changed.FRSE_VAL, [-20, 0, -10, 0])
    pd.testing.assert_frame_equal(d, original)
    _, fractional = bound.change_earnings(d, np.array([True, True, True, False]), -.1)
    np.testing.assert_allclose(fractional, [-10, -1.5, 0, 0])
    _, entry = bound.change_earnings(d, np.ones(4, bool), entry=True)
    np.testing.assert_array_equal(entry, [0, 0, 10000, 0])


def test_pinned_kernel_components_and_credit_response():
    tax = bound.module(bound.REMOVAL / 'state_tax.py', 'bound_test_taxsim')
    d = pd.DataFrame({key: np.zeros(4) for key in ['SEMP_VAL', 'FRSE_VAL', 'DIV_VAL',
        'INT_VAL', 'CAP_VAL', 'RNT_VAL', 'PNSN_VAL', 'ANN_VAL', 'SS_VAL', 'UC_VAL']})
    d['WSAL_VAL'], d['A_AGE'], d['GESTFIPS'] = [200000, 210000, 300000, 10000], 40, 0
    r = pd.DataFrame({'row': range(4), 'spouse': -1, 'status': 'single', 'depfiler': False,
                      'n_all': 0, 'k13_all': 0, 'k17_all': 0, 'keitc_all': 0})
    f = tax.taxsim_frame(d, r)
    result = tax.run_taxsim(f)
    # Current pinned binary includes addmed in fiitax. Its aggregate fica and
    # addmed fields fail independent wage-only formulas; never use them as totals.
    np.testing.assert_allclose(result.fiitax[:3], result.v28[:3] + result.addmed[:3])
    assert result.fica.iloc[0] != bound.payroll(200000, 0)
    assert result.addmed.iloc[1] != 90
    assert result.v25.iloc[3] > 0 and result.fiitax.iloc[3] < 0
    corrected = result.fiitax - result.addmed + bound.additional_medicare(f)
    np.testing.assert_allclose(corrected[:3], result.v28[:3] + [0, 90, 900])


def test_snap_income_moves_with_earned_income():
    b = bound.module(bound.REMOVAL / 'benefits.py', 'bound_test_snap')
    rules = b.rules()
    def amount(income):
        return b.snap_rule(rules, 24, np.array([1]), np.array([income]),
            np.array([income]), np.array([0]), np.array([0]), np.array([0]),
            np.array([False]), np.array([6]), 'zero')[0]
    # One person, no income: maximum; 100k annual earnings: financially ineligible.
    assert amount(0) == 12 * rules[24]['max'][0, 0]
    assert amount(100000) == 0


def test_snap_new_eligibility_and_loss_preserve_frozen_original():
    arm = bound.module(bound.REMOVAL / 'snap_arm.py', 'bound_test_snap_arm')
    observed, original = np.array([500., 0., 0.]), np.array([600., 0., 600.])
    changed = np.array([0., 600., 700.])
    low, high, _, _ = arm.after_benefit(observed, original, changed, np.full(3, 1000.), 0, 1)
    np.testing.assert_array_equal(low, [0, 0, 0])
    np.testing.assert_array_equal(high, [0, 600, 0])


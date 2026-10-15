"""Operator price ruling: recipient value, cost conservation and reading scope."""
import numpy as np
import pandas as pd
import pytest

import beside_arms as B
import beside_extra as X
import world_ledger as W
from mexico_prices import budget_from_gdp
from service_prices import money_price_inputs, price_levels, price_us_services, prepare_us_service_values


def valuation():
    items = [('medicare', 'medicare', 100, 100),
             ('medicaid_and_chip_other_medical', 'medicaid', 100, 92),
             ('income_security_services', 'services', 100, 100),
             ('general_public_services', 'public_good', 100, 140),
             ('public_order_safety', 'justice', 100, 30),
             ('housing_subsidies', 'housing_voucher', 100, 83),
             ('recreation_culture', 'public_good', 100, 100),
             ('education_services', 'education', 100, 0),
             ('capital_ent_water_sl', 'services', 10, 10),
             ('capital_ent_transit_sl', 'services', 10, 10),
             ('federal_income_tax', 'tax', -100, -100)]
    return pd.DataFrame([dict(end=e, generation=g, line=line, cls=cls,
                              G_bn=cost, net_cost_bn=cost,
                              V_low_bn=float(value), V_central_bn=float(value), V_high_bn=float(value))
                         for e in ('low', 'high') for g in W.GENS
                         for line, cls, cost, value in items])


def test_primary_price_dimensions_and_exact_ratio_no_cap():
    v = valuation()
    priced = price_us_services(v)
    levels = price_levels()
    health = v.line.eq('medicare')
    assert np.allclose(priced.loc[health, 'V_central_bn'], 100 * levels['1000000'] / levels['9080000'])
    recreation = priced.line.eq('recreation_culture')
    assert priced.loc[recreation, 'us_price_factor'].gt(1).all()
    assert priced.G_bn.equals(v.G_bn) and priced.net_cost_bn.equals(v.net_cost_bn)
    exempt = v.cls.isin(['tax', 'medicaid', 'housing_voucher'])
    assert priced.loc[exempt, 'V_central_bn'].equals(v.loc[exempt, 'V_central_bn'])
    assert priced.loc[v.cls.eq('education'), 'V_central_bn'].eq(0).all()
    with pytest.raises(SystemExit, match='not_already_general_priced'):
        price_us_services(priced)


def test_wtp_arm_and_reading2_3a_are_exempt_from_second_discount():
    v = valuation()
    three_a = B.services_at_prices(v, 0.81, 0.40)
    priced = price_us_services(three_a)
    mask = v.cls.isin(B.HEALTH_CLASSES) | v.line.isin(B.SOCIAL_LINES)
    pd.testing.assert_frame_equal(priced.loc[mask, ['V_low_bn', 'V_central_bn', 'V_high_bn']],
                                  three_a.loc[mask, ['V_low_bn', 'V_central_bn', 'V_high_bn']])
    pos = pd.DataFrame([dict(measure='money', party=g, mean_y_pc=50 if g in W.GENS else 100)
                        for g in (*W.GENS, 'other_residents')])
    wtp, _ = X.public_goods_wtp(v, pos, 1.0)
    got = price_us_services(wtp)
    mask = v.cls.eq('public_good')
    assert got.loc[mask, 'V_central_bn'].equals(wtp.loc[mask, 'V_central_bn'])


def test_mexico_full_budget_has_one_gdp_divisor_and_recipient_remits_consumption():
    raw = pd.DataFrame([dict(generation=g, cls=cls, bn=1.0)
                        for g in W.GENS for cls in ('education', 'health', 'cash', 'public_good')])
    base = dict(mxb=budget_from_gdp(raw, 10), household_price_basis='consumption')
    ruled = money_price_inputs(base, {'PA.NUS.PPP': 10, 'PA.NUS.PRVT.PP': 11})
    for side in ('recipient_value', 'fiscal_cost'):
        assert ruled['mxb'][f'{side}_ppp_divisor'].eq(10).all()
        assert ruled['mxb'][f'{side}_bn'].eq(1).all()
    assert ruled['mexico_tax_ppp_divisor'] == 10
    assert ruled['remittance_price_basis'] == 'consumption'
    assert ruled['household_price_basis'] == 'consumption'
    assert money_price_inputs(base, {}, enabled=False) is base


def test_operator_side_only_readings_keep_3a_and_expand_both_bounds():
    v = valuation()
    inputs = dict(vgen=B.services_at_prices(v, 0.81, 0.40), mxb='source')
    scenarios = [('reading2', 'reading_2', 'Reading 2', inputs, {'pgc': 'response_only'})]
    got = X.operator_reading_scenarios(scenarios, inputs, 'published budget', {'mxb': 'brief budget'})
    assert len(got) == 5
    for _, _, _, obj, kw in got:
        pd.testing.assert_frame_equal(obj['vgen'], inputs['vgen'])
        assert kw['pgc'] == 'response_only'
    variants = {name: obj for name, _, _, obj, _ in got}
    assert variants['reading2']['operator_us_general'] and variants['reading2']['operator_mexico_money']
    assert not variants['reading2__price_mexico_only']['operator_us_general']
    assert not variants['reading2__price_us_only']['operator_mexico_money']
    assert {x[4]['g3_bound'] for x in B.bound_scenarios(got)} >= {'zero', 'upper'}


def test_operator_variants_hold_mexico_log_income_basis_fixed(monkeypatch):
    obj = dict(mxb='source', household_price_basis='consumption',
               wmeta={'mexico': {'median_y': 100}, 'us_reference': {'per_capita': {'y_ref_other_mean': 100}}})
    variants = X.operator_reading_scenarios([('reading1', 'reading_1', 'R1', obj, {})],
                                           obj, 'published budget', {'mxb': 'brief budget'})
    rates = {'ppp_2024': {'PA.NUS.PPP': 10, 'PA.NUS.PRVT.PP': 11}}
    monkeypatch.setattr(W.json, 'load', lambda _: rates)
    row = pd.Series(dict(weight='mexico_budget', row='mexico_taxes_lost_G1', price_basis='PPP-GDP'))
    weights = {}
    for name, _, _, inputs, _ in variants:
        assert inputs['household_price_basis'] == 'consumption'
        weights[name] = W.row_weight(row, 'log_a', {}, None, inputs, {}, 'a')
    assert weights['reading1'] == weights['reading1__price_mexico_only'] == weights['reading1__price_us_only']


def test_response_only_value_receipt_uses_responsive_cost_before_pricing():
    source = valuation()
    before = prepare_us_service_values(source, 'response_only', enabled=False)
    after = prepare_us_service_values(source, 'response_only')
    selected = source.cls.eq('public_good')
    assert before.loc[selected, 'V_central_bn'].equals(source.loc[selected, 'G_bn'].astype(float))
    assert np.allclose(after.loc[selected, 'V_central_bn'],
                       source.loc[selected, 'G_bn'] * after.loc[selected, 'us_price_factor'])

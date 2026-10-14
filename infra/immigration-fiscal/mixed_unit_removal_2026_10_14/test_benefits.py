"""Independent boundary/weight/conservation tests for the conditional M4 lane."""
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location('benefit_test_module', Path(__file__).with_name('benefits.py'))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


@pytest.fixture(scope='module')
def rules():
    return b.rules()


def run_snap(rules, size=1, gross=0, earned=0, elderly=False, year=24, shelter='zero'):
    a = lambda x: np.array([x])
    return b.snap_rule(rules, year, a(size), a(gross), a(earned), a(0), a(0),
                       a(0), a(elderly), a(6), shelter)[0]


def test_primary_source_hashes_guard_against_html_error_pages(tmp_path, monkeypatch):
    path = tmp_path / 'primary.pdf'
    path.write_text('<html>Missing Key</html>')
    (tmp_path / 'benefit_pins.json').write_text(json.dumps({'files': {'primary.pdf': {'sha256': '0' * 64}}}))
    monkeypatch.setattr(b, 'INPUTS', tmp_path)
    with pytest.raises(ValueError, match='BLOCKED.*stale input'):
        b.verify_sources()


def test_usda_dimensions_and_regions(rules):
    for year in (24, 25):
        r = rules[year]
        assert r['max'].shape == (8, 7)
        assert r['net'].shape == (8, 3)
        assert (r['max'][:, 3] > r['max'][:, 1]).all()  # rural Alaska > urban
        assert (r['gross'] > r['net']).all()


def test_cms_statewide_infant_notes_are_parsed(rules):
    for name, note in rules['statewide_infant_notes'].items():
        assert note['age_limit'] > 0
        assert note['threshold'] >= rules['medicaid'][note['state']][1]
    assert rules['snap_elderly_age'] < rules['magi_senior_age']


def test_zero_income_gets_full_allotment(rules):
    for n in (1, 2, 4, 8):
        assert run_snap(rules, size=n) == 12 * rules[24]['max'][n - 1, 0]


def test_additional_member_schedule_is_linear(rules):
    n = np.array([8, 9, 10])
    values = b.sized(rules[24]['max'], rules[24]['increment'], n, np.zeros(3, int))
    assert np.array_equal(np.diff(values), np.repeat(rules[24]['increment'][0], 2))


def test_gross_test_is_not_net_deduction_test(rules):
    # Exceed federal gross limit by one cent, regardless of high earned deduction.
    annual_limit = 12 * rules[24]['gross'][0, 0]
    assert run_snap(rules, gross=annual_limit + .01, earned=annual_limit + .01) == 0
    assert run_snap(rules, gross=annual_limit, earned=annual_limit) > 0


def test_elderly_exemption_does_not_exempt_net_income(rules):
    annual_limit = 12 * rules[24]['gross'][0, 0]
    assert run_snap(rules, gross=annual_limit + 1, earned=annual_limit + 1,
                    elderly=True, shelter='cap') > 0
    assert run_snap(rules, gross=10 * annual_limit, elderly=True, shelter='zero') == 0


def test_shelter_sensitivity_is_monotonic(rules):
    income = 12 * rules[24]['net'][3, 0]
    assert run_snap(rules, size=4, gross=income, shelter='cap') >= run_snap(rules, size=4, gross=income)


def test_minimum_for_small_eligible_units(rules):
    annual_limit = 12 * rules[24]['net'][0, 0]
    # Net after standard deduction equals the limit, so benefit may reach minimum.
    gross = annual_limit + 12 * rules[24]['standard'][0, 0]
    assert run_snap(rules, gross=gross, elderly=True) == 12 * rules[24]['minimum'][0]


def test_160_replicates_and_identical_weights_zero_se():
    assert b.sdr(np.repeat(12., 161)) == 0
    with pytest.raises(ValueError, match='160 replicate'):
        b.sdr(np.repeat(12., 160))


def test_weighted_generation_attribution_and_no_head_dependence():
    # Three people, member generations 0/1, weights 1/3, survivor weight 7.
    unit = np.array([0, 0, 0])
    W = np.repeat(np.array([1., 3., 7.])[:, None], 161, axis=1)
    union = np.array([True, True, False])
    gen = np.array([0, 1, -1])
    change = np.repeat(np.array([[8.]]), 161, axis=1)
    out = b.attribute(change, unit, W, union, gen, np.array([True]))
    assert np.array_equal(out[:, 0], [2., 6., 0.])
    order = [2, 1, 0]
    assert np.array_equal(out, b.attribute(change, unit[order], W[order], union[order], gen[order], np.array([True])))


def test_unit_fields_fail_loud_on_inconsistent_repeats():
    with pytest.raises(ValueError, match='nonconstant unit field'):
        b.unit_values(pd.DataFrame({'SPM_ID': [1, 1], 'B': [3, 4]}), ['B'])


def test_signed_census_replicates_are_preserved():
    args = list(toy_frame())
    args[1][0, 1] = -1.
    result = b.compute(*args)
    assert result['details']['frame']['signed_replicate_weights'] == 1
    assert result['M4'][0, 1] != result['M4'][0, 0]
    assert result['details']['national_closure_max_bn'] <= 1e-6


def toy_frame():
    n = 3
    d = pd.DataFrame({k: np.zeros(n) for k in b.PERSON_COLUMNS})
    d['SPM_ID'] = 1
    d['SPM_NUMPER'] = n
    d['SPM_SNAPSUB'] = 6000.
    d['SPM_TOTVAL'] = 0.
    d['GESTFIPS'] = 6
    d['pwwgt0'] = [1., 3., 7.]
    d['A_AGE'] = [30, 8, 35]
    for k in ('WSAL_VAL', 'SEMP_VAL', 'FRSE_VAL'):
        d[k] = 0.
    W = np.repeat(d.pwwgt0.to_numpy()[:, None], 161, axis=1)
    gen = np.array([0, 1, -1])
    union = gen >= 0
    civ = np.ones(n, bool)
    model = {'spending': {'lines': [{'id': 'snap', 'national_bn': 11.,
             'keys': {'snap': {'personal': {'share': 4 / 11}}}}]}}
    return d, W, union, gen, civ, model


def test_partial_stack_discloses_unidentified_health_and_preserves_envelope():
    result = b.compute(*toy_frame())
    assert result['M4'].shape == (3, 161)
    assert not result['details']['adoptable']
    assert '[DEGRADED]' in result['details']['status']
    assert 'unidentifiable' in result['details']['ACA']['status']
    lo, hi = result['terms']['SNAP_envelope_low'], result['terms']['SNAP_envelope_high']
    assert (lo.sum(axis=0) <= result['M4'].sum(axis=0)).all()
    assert (result['M4'].sum(axis=0) <= hi.sum(axis=0)).all()
    assert result['details']['national_closure_max_bn'] <= 1e-6
    assert np.array_equal(result['M4'][:, 0], result['M4'][:, 1])


def test_actual_baseline_positive_control_is_required():
    args = list(toy_frame())
    args[-1]['spending']['lines'][0]['keys']['snap']['personal']['share'] = .99
    with pytest.raises(ValueError, match='positive control'):
        b.compute(*args)

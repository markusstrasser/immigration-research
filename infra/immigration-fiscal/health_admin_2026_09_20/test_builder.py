"""Semantic regressions for administrative-denominator and scope failures."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('health_admin_builder', HERE / 'builder.py')
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


def test_member_year_is_not_ever_enrolled():
    values = np.array([[1] * 12, [1] * 3 + [2] * 9, [-1] * 12])
    low, high, ever, unknown = b.monthly_bounds(values)
    assert low.sum() == high.sum() == 1.25
    assert ever.sum() == 2
    assert unknown.sum() == 0


def test_unknown_months_are_bounded_not_silently_zeroed():
    low, high, ever, unknown = b.monthly_bounds([[1] + [-9] * 2 + [2] * 9])
    assert low[0] == 1 / 12
    assert high[0] == 3 / 12
    assert unknown[0] == 2
    with pytest.raises(ValueError, match='coverage code'):
        b.monthly_bounds([[7] * 12])


def test_cps_some_year_is_bounded_not_assigned_twelve_months():
    lower, upper = b.cps_coverage_bounds([0, 1, 2, 3])
    np.testing.assert_allclose(lower, [0, 0, 1 / 12, 1])
    np.testing.assert_allclose(upper, [0, 0, 11 / 12, 1])


def test_canonical_exposure_and_origin_not_broad_or():
    data = pd.DataFrame(dict(PRPERTYP=[1, 2, 3, 2], A_AGE=[0, 30, 30, 30],
        PUB=[0, 1, 1, 1], PRIV=[0, 2, 2, 2], PENATVTY=[57, 303, 303, 310],
        PRCITSHP=[1, 4, 4, 4], PEFNTVTY=[303, 303, 303, 310],
        PEMNTVTY=[57, 303, 303, 310], PRDTHSP=[1, 1, 1, 1]))
    civilian, exposure, mexican = b.canonical_cps_domains(data)
    np.testing.assert_array_equal(civilian, [True, True, False, True])
    np.testing.assert_array_equal(exposure, [False, True, True, True])
    np.testing.assert_array_equal(mexican, [True, True, True, False])
    data.loc[0, 'A_AGE'] = 1
    with pytest.raises(ValueError, match='noninfant'):
        b.canonical_cps_domains(data)


def test_domain_variance_retains_other_psu():
    data = pd.DataFrame({'PERWT23F': [1, 1, 1, 1], 'VARSTR': [1, 1, 2, 2],
                         'VARPSU': [1, 2, 1, 2]})
    assert b.wr_variance(data, [3, 0, 0, 0]) == 9
    with pytest.raises(ValueError, match='Lonely PSU'):
        b.wr_variance(data.iloc[[0]], [3])


def test_unknown_end_year_age_is_explicit_and_reconciles():
    data = pd.DataFrame(dict(AGE23X=[-1, 10, 40, 70], PERWT23F=[1., 1., 1., 1.],
        VARSTR=[1, 1, 2, 2], VARPSU=[1, 2, 1, 2], TOTMCD23=[4., 1., 2., 3.],
        member_years_low=[1., 1., 1., 1.], member_years_high=[1., 1., 1., 1.],
        ever_covered=[1., 1., 1., 1.], unknown_months=[0., 0., 0., 0.]))
    result = b.national_meps(data, 2).set_index('domain')
    assert result.loc['age_unknown_or_out_of_scope', 'raw_spending'] == 4
    assert result.loc['age_unknown_or_out_of_scope', 'records'] == 1
    assert result.loc['all', 'raw_spending'] == result.iloc[1:].raw_spending.sum() == 10


def test_scorecard_missing_expansion_is_not_zero(tmp_path):
    rows = [dict(measure_id='EX.5', state_abbreviation='TX', data_period=y,
                 strat_tier1_value='Adults: ACA Medicaid Expansion', measure_value='null')
            for y in ['2022', '2023']]
    path = tmp_path / 'data.json'
    path.write_text(json.dumps(dict(count=2, results=rows)))
    assert b.load_scorecard(path).per_member_year.isna().all()
    rows.append(rows[0])
    path.write_text(json.dumps(dict(count=3, results=rows)))
    with pytest.raises(ValueError, match='Duplicate'):
        b.load_scorecard(path)


def test_release_does_not_promote_scope_gap_to_correction():
    path = HERE / 'derived/audit.json'
    if not path.exists():
        pytest.skip('Run builder to enable full-release semantic checks')
    audit = json.loads(path.read_text())
    assert b.sha(HERE / 'builder.py') == audit['builder_sha256']
    assert audit['canonical_correction_applied'] is False
    assert audit['institutions_added'] is False
    assert audit['year'] == 2023
    assert 'DEGRADED' in audit['scope_status']
    for item in audit['outputs']:
        assert b.sha(path.parent / item['name']) == item['sha256']
    rows = pd.read_csv(path.parent / 'ca_tx_observed_rates_2023.csv')
    assert rows.loc[rows.state_abbreviation.eq('CA') & rows.strat_tier1_value.eq('Children'),
                    'per_member_year'].iloc[0] == 3574
    assert rows.loc[rows.state_abbreviation.eq('TX') & rows.strat_tier1_value.eq('Children'),
                    'per_member_year'].iloc[0] == 5276
    scale = pd.read_csv(path.parent / 'scope_stresses_2023.csv')
    assert scale.status.str.contains('NOT_MATCHED_CORRECTION_OR_HARD_BOUND').all()
    assert scale.residual_scale.iloc[2] > 200e9
    assert scale.subtraction.iloc[2] > scale.subtraction.iloc[1]

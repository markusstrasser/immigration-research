"""Accounting boundaries for the separate current-law companion."""
import json

import pytest

import companion as C


def test_fiscal_calendar_bridge_and_printed_receipt():
    b = C.customs_bridge()
    y24, y25 = b['bridge']
    assert y25['fy_cash_bn'] == pytest.approx(194.86573987282, abs=1e-11)
    assert y24['fy_cash_bn'] == pytest.approx(77.03690994489, abs=1e-11)
    for row in b['bridge']:
        assert row['fy_cash_bn'] - row['subtract_prior_oct_dec_bn'] + row['add_current_oct_dec_bn'] == pytest.approx(row['calendar_cash_bn'], abs=1e-9)
        assert row['current_nipa_bn'] == pytest.approx(row['calendar_cash_bn'] + row['current_nipa_less_calendar_cash_bn'], abs=1e-9)
    assert y25['calendar_cash_bn'] == pytest.approx(264.04406843111)
    assert y25['current_nipa_bn'] == pytest.approx(268.663)
    assert b['fy2028_customs_bn'] is None


def test_business_score_uses_fy2028_and_marks_baseline():
    score = C.business_scores()
    assert score['70301']['fy2028_revenue_change_nominal_bn'] == -57.507
    assert score['70302']['fy2028_revenue_change_nominal_bn'] == -13.794
    assert all('NOT frozen2024' in row['comparison'] for row in score.values())
    assert all(row['corporate_pass_through_split'] is None for row in score.values())


@pytest.mark.parametrize('summary', [
    {'gaps': ['tariff schedule missing'], 'coherent_full_law_net_taken_bn': 7},
    {'gaps': [], 'coherent_full_law_net_taken_bn': None},
])
def test_incomplete_total_cannot_be_certified(summary):
    with pytest.raises(ValueError, match=r'\[BLOCKED\].*full current-law total unavailable'):
        C.full_total(summary)


def test_derived_population_response_and_signs():
    s = json.loads((C.OUT / 'companion_summary.json').read_text())
    assert s['population_v8']['with_coverage'] == pytest.approx(45230062.30075857)
    assert s['coherent_full_law_net_taken_bn'] is None
    assert s['headline_2024_law_change_bn'] == {'set': [0, 0], 'cash': [0, 0]}
    low, high = s['case_keys']['rows'][:2]
    assert high['corporate_share_after_response'] / low['corporate_share_after_response'] == pytest.approx(0.37)
    for row in s['rows']:
        assert row['delta_net_cost_bn'] == -row['delta_net_taken_bn']
        assert row['per_member_usd'] == pytest.approx(row['delta_net_cost_bn'] * 1e9 / s['population_v8']['with_coverage'])
        assert (row['delta_net_cost_bn'] > 0) == row['part'].startswith('business_')
    for section in ('70301', '70302'):
        rows = [r for r in s['rows'] if r['section'] == section]
        assert [r['delta_net_cost_bn'] for r in rows if r['which'] == 'set'] == [r['delta_net_cost_bn'] for r in rows if r['which'] == 'cash']


def test_sources_are_pinned_and_legal_certification_is_withheld():
    C.verify_sources()
    legal = json.loads((C.INPUTS / 'companion_legal.json').read_text())
    assert not legal['complete_legal_certification']
    assert len(legal['authorities']) == 6
    assert not any(row['fy2028_carry_fy2025_allowed'] for row in legal['authorities'])
    assert legal['remaining_legal_gaps']


def test_changed_raw_source_fails_before_calculation(tmp_path, monkeypatch):
    inputs = tmp_path / 'inputs'
    inputs.mkdir()
    raw = tmp_path / 'source.json'
    raw.write_text('{"verified": true}\n')
    (inputs / 'companion_sources.json').write_text(json.dumps({'sources': [{'path': 'source.json', 'sha256': C.sha(raw)}]}))
    raw.write_text('{"verified": false}\n')
    monkeypatch.setattr(C, 'INPUTS', inputs)
    monkeypatch.setattr(C, 'LANE', tmp_path)
    with pytest.raises(ValueError, match='stale source'):
        C.verify_sources()

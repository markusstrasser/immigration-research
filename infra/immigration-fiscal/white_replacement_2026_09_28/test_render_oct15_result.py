"""Reporting regressions independent of the costly comparator production route."""
import json

import pandas as pd
import pytest

import render_oct15_result as R


DIAGNOSTICS = ['combined_rules_members_round3', 'combined_rules_members_no_district',
               'combined_rules_members_round3_no_district', 'combined_rules_members_no_row8',
               'combined_rules_members_half_white', 'combined_rules_members_half_black',
               'combined_rules_members_da_middle', 'combined_rules_members_da_all_black',
               'combined_rules_members_partial_lineage']


@pytest.fixture
def reporting_files(tmp_path, monkeypatch):
    white, black, mixed = [tmp_path / name for name in ('white', 'black', 'mixed')]
    for lane in (white, black, mixed):
        (lane / 'derived').mkdir(parents=True)
    readings = {(a, m, b) for a, m, b, _ in R.READINGS}
    readings |= {(a, R.MC.OWN, b) for a in DIAGNOSTICS + ['combined_rules_members', 'combined_rules_coverage']
                 for b in ('low', 'high')}
    comparisons, black_rows, white_rows, results = [], [], [], []
    for arm, mortality, bound in sorted(readings):
        for basis in ('accrual', 'cash'):
            for i, end in enumerate(('low', 'high')):
                common = dict(arm=arm, mortality_convention=mortality, mortality_bound=bound, basis=basis, end=end)
                decomposition = dict(comparison_lineage_cost_bn=110. + i, case_headline_cost_bn=100. + i,
                                     lineage_children_block_bn=2., lineage_children_item11_bn=3.,
                                     mortality_delta_bn=4., case_minus_rough_bridge_bn=-1.)
                offset = {name: j + 1. for j, name in enumerate(DIAGNOSTICS)}.get(arm, 0.)
                comparisons.append(dict(common, **decomposition, white_gap_rough_lineage_bn=200. + i + offset,
                                        central=arm == R.CENTRAL['arm'] and mortality == R.CENTRAL['mortality_convention']))
                for count in ('own_count', 'scaled_to_lineage'):
                    black_rows.append(dict(common, **decomposition, population_basis=count, population=40e6,
                                           black_minus_rough_lineage_bn=70. + i + offset,
                                           comparator_item11_bn=5. + i, item11_comparator_se_bn=2.,
                                           item11_paired_se_bn=float('nan'), lineage_item11_se_bn=3.))
                for count in ('own_count', 'lineage_count'):
                    white_rows.append(dict(common, **decomposition, population_basis=count, population=45e6,
                                           lineage_minus_comparator_bn=200. + i + offset, comparator_item11_bn=6. + i,
                                           item11_comparator_se_bn=4., item11_paired_se_bn=5., lineage_item11_se_bn=3.))
                for group in ('A3_third_plus_nh_white_at_union_ages', 'A4_third_plus_nh_white_stationary'):
                    results.append(dict(common, group=group, cost_bn=-20., comparator_item11_bn=3.,
                                        item11_comparator_se_bn=2., item11_paired_se_bn=float('nan'),
                                        population=45e6, true_own_count=175e6, lineage_item11_se_bn=3.,
                                        own_count_item11_bn=11., own_count_item11_comparator_se_bn=7.,
                                        own_count_item11_paired_se_bn=8.))
    for lane, name, rows in [(white, 'symmetric_comparisons_oct15.csv', comparisons),
                             (white, 'symmetric_white_population_oct15.csv', white_rows),
                             (white, 'symmetric_results_oct15.csv', results),
                             (black, 'symmetric_population_oct15.csv', black_rows)]:
        pd.DataFrame(rows).to_csv(lane / 'derived' / name, index=False, lineterminator='\n')
    precedence = dict(round3=179e6, lineage_precedence=177e6, half_overlap=178e6, overlap=2e6,
                      lineage_observed=43e6, lineage_half_overlap=42e6)
    (white / 'derived/members_coverage_oct15.json').write_text(json.dumps({'counts': {'precedence': {
        'A1_third_plus_nh_white': precedence, 'nh_black_rough': precedence}},
        'controls': {'alternative_white_black_overlap_people': 12345.6,
                     'overlap_gate_scope': 'each lineage/comparator pair; alternatives not simultaneous partition'}}))
    source = {'gaps': []}
    targets = {}
    for group in ('white', 'black'):
        targets[group] = {}
        for method in ('set', 'cash'):
            targets[group][method] = {}
            for i, end in enumerate(('low', 'high')):
                targets[group][method][end] = dict(rough_lineage_cost_bn=90. + i, case_lineage_cost_bn=100. + i)
                for count in ('own_count', 'lineage_count'):
                    source['gaps'].append(dict(group=group, method=method, end=end, population_basis=count,
                                               both_sided_rough_gap_bn=290. + i, one_sided_rough_gap_bn=300. + i))
    (mixed / 'derived/comparator_targets.json').write_text(json.dumps(targets))
    originals = {lane: f'Original {lane.name} evidence.\n \n' for lane in (white, black)}
    for lane, old in originals.items():
        (lane / 'RESULT.md').write_text(old)
    monkeypatch.setattr(R, 'HERE', white)
    monkeypatch.setattr(R, 'BLACK', black)
    monkeypatch.setattr(R.CC, 'MIXED_SOURCE', mixed / 'derived')
    monkeypatch.setattr(R.CC, 'load_mixed_unit', lambda: source)
    return white, black, originals


def test_round4_render_preserves_prefix_and_se_distinctions(reporting_files):
    white, black, originals = reporting_files
    R.render()
    first = {lane: (lane / 'RESULT.md').read_bytes() for lane in originals}
    text = (white / 'RESULT.md').read_text()
    assert 'DA envelope, bound high' in text
    assert '179,000,000 | 177,000,000 | 178,000,000 | 2,000,000' in text
    assert 'current-rule readings' in text and 'contract refuses both as centrals' in text
    assert 'comparison: 110.000 / 111.000' in text and 'headline: 100.000 / 101.000' in text
    assert 'children item 11: 3.000 / 3.000' in text
    assert 'Comparator SE' in text and 'Lineage SE' in text and 'Paired SE' in text
    assert 'not computed' in text and '| nan' not in text
    assert '0.56797%' in text and '−$2.036694bn' in text and 'IPEDS' in text
    assert 'not a paired SE for the whole modeled fiscal cost' in text
    assert 'Full lineage survivor solve, bound high' in text
    assert 'A1 white, old partial lineage survivor patch, bound low' in text
    assert 'central preserves it in the bridge' in text and 'incidence difference' in text
    assert 'not a simultaneous partition' in text
    assert 'themselves share 12,345.60' in text
    assert '| A3 reweighted, children, PES central, bound low | accrual | own_count | 175,000,000 | 11.000 / 11.000 | 7.000 / 7.000 | 3.000 / 3.000 | 8.000 / 8.000 |' in text
    assert '| A4 reweighted, children, PES central, bound high | cash | lineage_count | 45,000,000 | 3.000 / 3.000 |' in text
    R.render()
    for lane, old in originals.items():
        assert (lane / 'RESULT.md').read_bytes() == first[lane]
        assert (lane / 'RESULT.md').read_text().startswith(old)


def test_report_refuses_missing_decomposition_or_one_endpoint():
    with pytest.raises(SystemExit, match='decomposition is incomplete'):
        R.lineage_decomposition(pd.DataFrame({'end': ['low', 'high']}))
    with pytest.raises(SystemExit, match='endpoint pair is not unique'):
        R.pair(pd.DataFrame({'end': ['low'], 'se': [1.]}), 'se')
    with pytest.raises(SystemExit, match='missing or nonfinite'):
        R.pair(pd.DataFrame({'end': ['low', 'high'], 'se': [1., None]}), 'se')
    with pytest.raises(SystemExit, match='missing or nonfinite'):
        R.pair(pd.DataFrame({'end': ['low', 'high'], 'cost_bn': [None, None]}), 'cost_bn')


def test_lineage_mortality_decomposition_does_not_take_comparator_mortality():
    frame = pd.DataFrame({'end': ['low', 'high'], **{name: [1., 2.] for name, _ in R.DECOMPOSITION},
                          'mortality_delta_bn': [999., 999.]})
    assert 'own mortality: 1.000 / 2.000' in R.lineage_decomposition(frame)
    assert '999' not in R.lineage_decomposition(frame)


def test_optional_policy_delta_is_printed_only_for_changed_policy():
    frame = pd.DataFrame({'end': ['low', 'high'], **{name: [1., 2.] for name, _ in R.DECOMPOSITION},
                          'lineage_policy_delta_bn': [3., 4.]})
    assert 'policy change: 3.000 / 4.000' in R.lineage_decomposition(frame)
    frame['lineage_policy_delta_bn'] = 0.
    assert 'policy change' not in R.lineage_decomposition(frame)


def test_change_table_uses_endpoint_matched_differences(reporting_files):
    white, black, _ = reporting_files
    comparisons = pd.read_csv(white / 'derived/symmetric_comparisons_oct15.csv')
    population = pd.read_csv(black / 'derived/symmetric_population_oct15.csv')
    lines = []
    R.change_table(lines, comparisons, population)
    text = '\n'.join(lines)
    assert '| Lineage precedence, bound low | accrual | -1.000 / -1.000 | -1.000 / -1.000 | -1.000 / -1.000 |' in text
    assert '| Precedence + own district prices, joint, bound high | cash | -3.000 / -3.000 |' in text

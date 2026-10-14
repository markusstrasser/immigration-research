"""Regression checks for engine mixing, frame mismatch and item11 asymmetry."""
import pytest
import comparison_contract as C


def test_case_rough_gap_rejected():
    with pytest.raises(SystemExit, match='different engine tags'):
        C.require_same_engine({'engine': 'case'}, {'engine': 'rough'})
    with pytest.raises(SystemExit, match='missing'):
        C.require_same_engine({}, {})


def test_equal_population_and_item11_signs():
    lineage = dict(engine='rough', population=44., cost_bn=100.)
    white = dict(engine='rough', population=44., cost_bn=-50.)
    black = dict(engine='rough', population=40., cost_bn=120.)
    d = C.gap_fields(lineage, white, black, 10.)
    assert d['white_gap_rough_lineage_bn'] == 150.
    assert d['white_gap_without_item11_bn'] == 140.
    assert d['black_minus_rough_lineage_bn'] == 20.
    assert d['black_minus_rough_lineage_equal_population_bn'] == 32.
    assert d['black_minus_lineage_equal_population_without_item11_bn'] == 42.
    with pytest.raises(SystemExit, match='match lineage population'):
        C.gap_fields(lineage, dict(white, population=40.), black, 10.)


def test_measured_counterparts_negative_signs_and_both_side_exclusion():
    lineage = dict(engine='rough', population=44., cost_bn=100.)
    white = dict(engine='rough', population=44., cost_bn=-55., comparator_item11_bn=-5., item11_paired_se_bn=3.)
    black = dict(engine='rough', population=40., cost_bn=122., comparator_item11_bn=2., item11_paired_se_bn=4.)
    d = C.gap_fields(lineage, white, black, 10.)
    assert d['white_gap_rough_lineage_bn'] == 155.
    assert d['white_gap_one_sided_bn'] == 150.
    assert d['white_gap_without_item11_bn'] == 140.
    assert d['black_minus_lineage_one_sided_bn'] == 20.
    assert d['black_minus_lineage_without_item11_bn'] == 30.
    assert d['black_minus_lineage_equal_population_without_item11_bn'] == pytest.approx(42.)
    assert d['white_item11_paired_se_bn'] == 3.


def test_source_drift_blocks_and_live_scaling_uses_paired_vectors(tmp_path):
    import shutil
    source = C.load_mixed_unit()
    population = float(source['gaps'][0]['lineage_count'])
    low = C.comparator_removal(source, 'A1_third_plus_nh_white', 'accrual', 'low', population)
    high = C.comparator_removal(source, 'A1_third_plus_nh_white', 'cash', 'high', population)
    assert low['bn'] == pytest.approx(-9.250755056064, abs=1e-9)
    assert high['bn'] == pytest.approx(-4.653441516614, abs=1e-9)
    assert low['paired_se_bn'] == pytest.approx(5.883572282839, abs=1e-9)
    for name in C.MIXED_PINS:
        shutil.copyfile(C.MIXED_SOURCE / name, tmp_path / name)
    with (tmp_path / 'white_summary.json').open('a') as stream:
        stream.write(' ')
    with pytest.raises(SystemExit, match=r'\[BLOCKED\].*sha256 mismatch'):
        C.load_mixed_unit(tmp_path)
    with pytest.raises(SystemExit, match='population differs'):
        C.comparator_removal(source, 'A1_third_plus_nh_white', 'cash', 'low', population + 1.)


def test_base_publication_keeps_dimensionless_ratio_and_budget_identity():
    source = C.load_mixed_unit()
    lineage_population = float(source['gaps'][0]['lineage_count'])
    black_population = float(next(r['comparator_own_count'] for r in source['gaps'] if r['group'] == 'black'))
    rows = [dict(basis='cash', end='low', group='mexican_origin_rough', population=str(round(lineage_population)),
                 cost='300.0000', net_budget='300.0000', spending_saved='400.0000', balance='-200.0000',
                 cost_per_member='6633', mixed_unit_removal_bn=10.74001627270179),
            dict(basis='cash', end='low', group='nh_black_rough', population=str(round(black_population)),
                 cost='400.0000', net_budget='400.0000', spending_saved='500.0000', balance='-250.0000',
                 cost_per_member='9534', per_member_over_rough_union='1.4374', mixed_unit_removal_bn=10.74001627270179)]
    C.publish_base_summary(rows, lineage_population)
    black = rows[1]
    expected_ratio = float(black['cost']) / black_population / (300. / lineage_population)
    assert float(black['per_member_over_rough_union']) == pytest.approx(expected_ratio, abs=5e-5)
    assert float(black['cost']) == float(black['net_budget'])
    assert float(black['spending_saved']) - 100. == pytest.approx(float(black['net_budget']), abs=1e-9)
    assert black['balance'] == '-250.0000'
    assert black['cost_evaluator_bn'] == '400.0000'
    assert black['comparator_item11_bn'] == pytest.approx(-2.333671, abs=1e-6)
    with pytest.raises(SystemExit, match='already published'):
        C.publish_base_summary(rows, lineage_population)


def test_bridge_includes_response_resource_and_post_and_fails_on_missing_component():
    case = ({'cost': 15., 'capital': 4., 'production_gain': 2.},
            [('spending', 'x', 10., 10., 1.)], {'lineage post-engine mixed_unit_removal_bn': 3.})
    rough = ({'cost': 9., 'capital': 3., 'production_gain': 2.},
             [('spending', 'x', 10., 5., 1.)], {'lineage post-engine mixed_unit_removal_bn': 3.})
    parts = C.bridge_parts(case, rough)
    assert sum(r['case_minus_rough_bn'] for r in parts) == 6.
    broken = (case[0], case[1], {})
    with pytest.raises(SystemExit, match='does not close'):
        C.bridge_parts(broken, rough)


def test_bridge_does_not_double_count_resource_carriers():
    case = ({'cost': 14., 'capital': 4., 'production_gain': 0.},
            [('spending', 'x', 10., 10., 1.), ('spending', 'capital_carrier', 0., 4., 1.)], {})
    rough = ({'cost': 8., 'capital': 3., 'production_gain': 0.},
             [('spending', 'x', 10., 5., 1.), ('spending', 'capital_carrier', 0., 3., 1.)], {})
    parts = C.bridge_parts(case, rough, {'capital_carrier': {'kind': 'capital'}})
    assert sum(r['case_minus_rough_bn'] for r in parts) == 6.

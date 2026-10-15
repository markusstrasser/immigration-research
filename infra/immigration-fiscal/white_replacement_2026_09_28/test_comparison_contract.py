"""Regression checks for engine mixing, frame mismatch, item11 asymmetry and round 3's contract (C3 fixes 3b, 5, 6)."""
import numpy as np
import pandas as pd
import pytest
import comparison_contract as C
import mortality_conventions as MC


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


def paired(source, group, method, end, frame):
    rows = [r for r in source['gaps'] if (r['group'], r['method'], r['end'], r['population_basis']) ==
            (group, method, end, frame)]
    assert len(rows) == 1
    return rows[0]


def test_source_drift_blocks_and_live_scaling_uses_paired_vectors(tmp_path):
    import shutil
    source = C.load_mixed_unit()
    population = float(paired(source, 'white', 'set', 'low', 'lineage_count')['lineage_count'])
    low = C.comparator_removal(source, 'A1_third_plus_nh_white', 'accrual', 'low', population)
    high = C.comparator_removal(source, 'A1_third_plus_nh_white', 'cash', 'high', population)
    assert low['bn'] == pytest.approx(float(paired(source, 'white', 'set', 'low', 'lineage_count')['comparator_adjustment_bn']), abs=1e-12)
    assert high['bn'] == pytest.approx(float(paired(source, 'white', 'cash', 'high', 'lineage_count')['comparator_adjustment_bn']), abs=1e-12)
    assert low['paired_se_bn'] == float(paired(source, 'white', 'set', 'low', 'lineage_count')['item11_paired_se_bn'])
    assert low['spending_bn'] + low['receipt_bn'] == pytest.approx(low['bn'], abs=1e-9)
    for name in C.MIXED_PINS:
        shutil.copyfile(C.MIXED_SOURCE / name, tmp_path / name)
    with (tmp_path / 'white_summary.json').open('a') as stream:
        stream.write(' ')
    with pytest.raises(SystemExit, match=r'\[BLOCKED\].*sha256 mismatch'):
        C.load_mixed_unit(tmp_path)
    with pytest.raises(SystemExit, match='population differs'):
        C.comparator_removal(source, 'A1_third_plus_nh_white', 'cash', 'low', population + 1.)


def test_registry_blocks_unknown_groups_and_labels_unmeasured():
    source = C.load_mixed_unit()
    with pytest.raises(SystemExit, match='not registered'):
        C.comparator_removal(source, 'A1_third_plus_nh_whites', 'accrual', 'low', 1e6)
    for group in ('A2_us_born_nh_white', 'all_residents_slice', 'india_born_white_ages', 'indian_origin'):
        term = C.comparator_removal(source, group, 'accrual', 'low', 1e6)
        assert term['status'] == 'unmeasured' and term['bn'] == 0. and term['scope'].startswith('unmeasured')
    assert C.comparator_removal(source, 'mexican_origin_rough_white_ages', 'cash', 'high', 1e6)['status'] == 'lineage'
    with pytest.raises(SystemExit, match='reweighting factors'):
        C.comparator_removal(source, 'A3_third_plus_nh_white_at_union_ages', 'accrual', 'low', 1e6)


def test_parts_have_sides_and_add():
    with pytest.raises(SystemExit, match='without a side'):
        C.split({'M1_federal': {'bn': 1.}, 'new_part': {'bn': 2.}})
    out = C.split({'M1_federal': {'bn': 1.}, 'Medicaid': {'bn': -3.}, 'M5_owner_property': {'bn': 2.}}, 2.,
                  {'tax': 1., 'spm': 0.5, 'household': 3.})
    assert out == {'receipts': 2. + 12., 'spending': -3.}
    with pytest.raises(SystemExit, match='do not add'):
        C.checked(dict(bn=1., spending_bn=0.5, receipt_bn=0.4, own_count=10.))


def test_reweighting_is_identity_for_a1_and_moves_with_mixed_weight():
    # household 1: member 0 with non-member 1 in one tax and SPM unit; household 2: member 2 files apart from
    # non-member 3 but shares their SPM unit; household 3: members only
    d = pd.DataFrame({'PH_SEQ': [1, 1, 2, 2, 3, 3], 'TAX_ID': [1, 1, 1, 2, 1, 1], 'SPM_ID': [10, 10, 20, 20, 30, 30]})
    civ = np.ones(6, bool)
    a1 = np.array([1., 0., 1., 0., 1., 1.])
    ratios = C.reweight_ratios(d, civ, {'A1': a1, 'same': a1 * 2., 'tilt': np.array([3., 0., 1., 0., 1., 1.])})
    assert ratios['same'] == {'tax': 1., 'spm': 1., 'household': 1.}
    assert ratios['tilt']['tax'] == pytest.approx((3 / 6) / (1 / 4))
    assert ratios['tilt']['spm'] == pytest.approx((4 / 6) / (2 / 4))
    assert ratios['tilt']['household'] == pytest.approx((4 / 6) / (2 / 4))
    with pytest.raises(SystemExit, match='A1 members only'):
        C.reweight_ratios(d, civ, {'A1': a1, 'leak': np.ones(6)})
    with pytest.raises(SystemExit, match='no weight in mixed'):
        C.reweight_ratios(d, civ, {'A1': np.array([0., 0., 0., 0., 1., 1.])})


def test_true_count_removal_scales_the_measured_term_by_the_true_count():
    source = C.load_mixed_unit()
    for group, mask in (('A1_third_plus_nh_white', 'white'), ('nh_black_rough', 'black')):
        for rule, suffix in (('current', ''), ('children', '_children')):
            measured = next(r for r in source['summaries'][mask + suffix]['results']
                            if (r['method'], r['end'], r['reading']) == ('set', 'low', 'bounded_low'))
            at_true = C.true_count_removal(source, group, 'accrual', 'low', 1.2e8, 1.2e8, rule)
            assert at_true['bn'] == pytest.approx(measured['bn'], abs=1e-12)
            half = C.true_count_removal(source, group, 'accrual', 'low', 0.6e8, 1.2e8, rule)
            assert half['bn'] == pytest.approx(measured['bn'] / 2, abs=1e-12)
            assert half['comparator_se_bn'] == pytest.approx(measured['se_bn'] / 2, abs=1e-10)
            if rule == 'children':
                assert half['paired_se_bn'] is None
                assert 'comparator-only' in half['se_scope']
    with pytest.raises(SystemExit, match='A1 and Black only'):
        C.true_count_removal(source, 'A2_us_born_nh_white', 'accrual', 'low', 1., 1., 'children')


def test_children_reweighting_uses_expanded_departure_mask_and_lineage_precedence():
    d = pd.DataFrame({'PH_SEQ': [1, 1, 2, 2, 3, 3], 'TAX_ID': [1, 1, 1, 1, 1, 1],
                      'SPM_ID': [10, 10, 20, 20, 30, 30]})
    civ = np.ones(6, bool)
    # Household 1 child departs despite zero survey weight; it cannot turn its parent's unit into a mixed unit.
    expanded = np.array([True, True, True, False, True, False])
    base = np.array([1., 0., 1., 0., 1., 0.])
    tilt = np.array([2., 0., 1., 0., 1., 0.])
    ratios = C.reweight_ratios(d, civ, {'A1': base, 'tilt': tilt}, membership_rule='children',
                               membership_mask=expanded, lineage_mask=np.array([0, 0, 0, 1, 0, 0], bool))
    assert ratios['tilt'] == {'tax': 0.75, 'spm': 0.75, 'household': 0.75}
    with pytest.raises(SystemExit, match='overlaps the precedence lineage'):
        C.reweight_ratios(d, civ, {'A1': base}, membership_rule='children', membership_mask=expanded,
                          lineage_mask=np.array([1, 0, 0, 0, 0, 0], bool))
    with pytest.raises(SystemExit, match='unknown.*membership rule'):
        C.reweight_ratios(d, civ, {'A1': base}, membership_rule='invented')


def test_reweighted_true_count_uses_its_observed_count_and_signed_paired_parts():
    source = C.load_mixed_unit()
    group = 'A3_third_plus_nh_white_at_union_ages'
    factors = {'tax': 1.2, 'spm': 0.8, 'household': 0.9}
    row, gaps = C.entry(source, 'white_children', 'set', 'low')
    source_own = float(gaps[0]['comparator_own_count'])
    observed = source_own / 4
    true = observed * 1.1
    population = true / 2
    lineage = np.linspace(10., 12., 161)
    term = C.true_count_removal(source, group, 'accrual', 'low', population, true, 'children',
                                reweight={group: factors}, observed_own=observed, lineage_replicates=lineage)
    expected_parts = C.split(row['parts'], 1 / 8, factors)
    assert term['bn'] == pytest.approx(sum(expected_parts.values()), abs=1e-12)
    assert term['own_count'] == observed
    comparator = C.item11_replicates(source, 'white_children', 'set', 'low', factors) / 8
    assert term['comparator_se_bn'] == pytest.approx(C.sdr(comparator), abs=1e-12)
    assert term['paired_se_bn'] == pytest.approx(C.sdr(lineage - comparator), abs=1e-12)
    assert term['paired_se_bn'] != pytest.approx(np.hypot(C.sdr(lineage), C.sdr(comparator)), abs=1e-6)
    with pytest.raises(SystemExit, match='observed own count'):
        C.true_count_removal(source, group, 'accrual', 'low', population, true, 'children', reweight={group: factors})


def test_a2_and_population_slice_cannot_be_published_as_central():
    for group in ('A2_us_born_nh_white', 'all_residents_slice'):
        reading = C.reading_scope(group)
        assert reading['comparison_reading'] == 'current-rule reading'
        assert not reading['central_eligible'] and reading['current_rule_reason']
        with pytest.raises(SystemExit, match='current-rule reading, not a central'):
            C.require_central_reading(group)
    assert C.require_central_reading('A3_third_plus_nh_white_at_union_ages')['central_eligible']


def test_uncertainty_without_expanded_lineage_vector_never_claims_pairing():
    source = C.load_mixed_unit()
    term = C.true_count_removal(source, 'A1_third_plus_nh_white', 'accrual', 'low', 1., 1., 'children')
    assert term['paired_se_bn'] is None and term['comparator_se_bn'] > 0
    with pytest.raises(SystemExit, match='160 finite signed replicates'):
        C.sdr(np.ones(160))


def test_mixed_mortality_pair_is_never_a_stated_claim():
    with pytest.raises(SystemExit, match='mixed mortality pair'):
        C.require_stated(MC.MIXED)
    assert C.require_stated(MC.OWN) == MC.OWN and MC.stated(MC.GENERAL) and not MC.stated(MC.MIXED)
    with pytest.raises(ValueError, match='unknown mortality convention'):
        MC.stated('own mortality')
    assert MC.CENTRAL['arm'] in MC.DERIVED and MC.CENTRAL['arm'] in MC.OWN_ARMS
    assert 'combined_rules_members_general' not in MC.OWN_ARMS


def test_base_publication_keeps_dimensionless_ratio_and_budget_identity():
    source = C.load_mixed_unit()
    lineage_population = float(source['gaps'][0]['lineage_count'])
    black_population = float(next(r['comparator_own_count'] for r in source['gaps'] if r['group'] == 'black'))
    rows = [dict(basis='cash', end='low', group='mexican_origin_rough', population=str(round(lineage_population)),
                 cost='300.0000', net_budget='300.0000', spending_saved='400.0000', balance='-200.0000',
                 cost_per_member='6633', mixed_unit_removal_bn=10.74001627270179),
            dict(basis='cash', end='low', group='nh_black_rough', population=str(round(black_population)),
                 cost='400.0000', net_budget='400.0000', spending_saved='500.0000', taxes_lost='100.0000', balance='-250.0000',
                 cost_per_member='9534', per_member_over_rough_union='1.4374', mixed_unit_removal_bn=10.74001627270179)]
    C.publish_base_summary(rows, lineage_population)
    black = rows[1]
    expected_ratio = float(black['cost']) / black_population / (300. / lineage_population)
    assert float(black['per_member_over_rough_union']) == pytest.approx(expected_ratio, abs=5e-5)
    assert float(black['cost']) == float(black['net_budget'])
    assert float(black['spending_saved']) == pytest.approx(500. + black['item11_spending_bn'], abs=1e-4)
    assert float(black['taxes_lost']) == pytest.approx(100. - black['item11_receipt_bn'], abs=1e-4)
    assert float(black['net_budget']) == pytest.approx(float(black['spending_saved']) - float(black['taxes_lost']), abs=2e-4)
    assert black['item11_spending_bn'] + black['item11_receipt_bn'] == pytest.approx(black['comparator_item11_bn'], abs=1e-9)
    assert black['balance'] == '-250.0000'
    assert black['cost_evaluator_bn'] == '400.0000'
    measured = next(r for r in source['summaries']['black']['results']
                    if (r['method'], r['end'], r['reading']) == ('cash', 'low', 'bounded_low'))
    assert black['comparator_item11_bn'] == pytest.approx(measured['bn'], abs=1e-9)
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

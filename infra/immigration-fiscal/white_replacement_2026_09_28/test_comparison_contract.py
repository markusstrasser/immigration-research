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

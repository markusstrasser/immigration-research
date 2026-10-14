"""Round-2 negative controls and independent source substitution reproduction."""
import json
from pathlib import Path
import pytest
import mortality_conventions as M

HERE = Path(__file__).resolve().parent


def test_own_black_and_whole_headline_require_mixed_label():
    lineage = dict(case='oct15', group_mortality='whole-population')
    black = dict(case='oct15', group_mortality='own-group')
    for label in ('', None, M.OWN, M.GENERAL):
        with pytest.raises(ValueError, match='requires explicit label'):
            M.validate_pair(lineage, black, label)
    M.validate_pair(lineage, black, M.MIXED)


def test_stale_case_pairing_rejected():
    with pytest.raises(ValueError, match='crosses case keys'):
        M.validate_pair(dict(case='oct14', group_mortality='own-group'),
                        dict(case='oct15', group_mortality='own-group'), M.OWN)


def test_source_method_reproduces_frozen_central_change():
    """Read-only v7 positive control; no production run or historical output write."""
    full, union = {}, {}
    for basis, suffix in (('accrual', ''), ('cash', '_cash')):
        full[basis] = json.loads((HERE / f'derived/engine_lines_oct14{suffix}.json').read_text())
        union[basis] = json.loads((HERE / f'derived/engine_lines_oct14_union{suffix}.json').read_text())
    meta = json.loads((HERE.parent / 'main_case_2026_10_14/derived/corrections.json').read_text())['meta']
    source = M.read_rows(M.SOURCE / 'derived/case_changes.csv')
    for end in ('low', 'high'):
        expected = M.one(source, arm='central', basis='accrual', end=end)
        actual = M.source_change(full, union, meta, end)
        for bound in ('low', 'high'):
            assert actual[bound] == pytest.approx(float(expected[f'lineage_delta_{bound}_bn']), abs=1e-9)


def test_live_delivered_comparisons_trace_tagged_cost_rows():
    path = HERE / 'derived/symmetric_results_oct15.csv'
    if not path.exists():
        pytest.skip('final oct15 outputs await CASE_FINAL')
    rows = M.read_rows(path)
    comparisons = M.read_rows(HERE / 'derived/symmetric_comparisons_oct15.csv')
    for c in comparisons:
        selected = [r for r in rows if all(r[k] == c[k] for k in
                    ('case', 'arm', 'basis', 'end', 'mortality_convention', 'mortality_bound'))]
        e = M.one(selected, group='mexican_origin_rough')
        b = M.one(selected, group='nh_black_rough')
        w = M.one(selected, group='A1_third_plus_nh_white')
        M.validate_pair(e, b, c['mortality_convention'])
        M.validate_pair(e, w, c['mortality_convention'])
        assert c['lineage_engine'] == c['comparator_engine'] == e['engine'] == b['engine'] == w['engine'] == 'rough'
        assert float(c['black_minus_rough_lineage_bn']) == pytest.approx(float(b['cost_bn'])-float(e['cost_bn']), abs=1e-9)
        assert float(c['white_gap_rough_lineage_bn']) == pytest.approx(float(e['cost_bn'])-float(w['cost_bn']), abs=1e-9)

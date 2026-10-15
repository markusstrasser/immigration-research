"""Independent mask boundaries, source immutability and stored stack checks."""
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import adapter
import finalize


def test_masks_keep_distinct_race_origin_generation_boundaries():
    d = pd.DataFrame({'PRCITSHP': [1, 1, 4, 1, 1, 1], 'PEFNTVTY': [57, 303, 57, 57, 57, 57],
        'PEMNTVTY': [57] * 6, 'PEHSPNON': [2, 2, 2, 1, 2, 2], 'PRDTRACE': [1, 1, 2, 2, 2, 1]})
    civ = np.array([True, True, True, True, True, False])
    white, _ = adapter.membership(d, civ, 'white')
    black, _ = adapter.membership(d, civ, 'black')
    assert white.tolist() == [True, False, False, False, False, False]
    assert black.tolist() == [False, False, True, False, True, False]


def test_children_rule_adds_only_members_biological_minor_children():
    # One household: a white member parent (line 1), her non-member Hispanic child (line 2, biological), a step child
    # (line 3), an adult non-member (line 4) and a white member's own white child (line 5, already a member).
    d = pd.DataFrame({'PH_SEQ': [7] * 5, 'A_LINENO': [1, 2, 3, 4, 5], 'PEPAR1': [-1, 1, 1, -1, 1], 'PEPAR2': [-1] * 5,
                      'PEPAR1TYP': [-1, 1, 2, -1, 1], 'PEPAR2TYP': [-1] * 5, 'A_AGE': [40, 10, 9, 45, 8],
                      'PRCITSHP': [1] * 5, 'PEFNTVTY': [57] * 5, 'PEMNTVTY': [57] * 5,
                      'PEHSPNON': [2, 1, 1, 1, 2], 'PRDTRACE': [1, 1, 1, 1, 1]})
    civ = np.ones(5, bool)
    white, _ = adapter.membership(d, civ, 'white')
    children, gen = adapter.membership(d, civ, 'white_children_round3')
    assert white.tolist() == [True, False, False, False, True]
    assert children.tolist() == [True, True, False, False, True]
    assert (gen[children] == 2).all() and (gen[~children] == -1).all()


def test_precedence_excludes_lineage_from_base_and_added_children(monkeypatch):
    d = pd.DataFrame({'PH_SEQ': [7] * 3, 'A_LINENO': [1, 2, 3], 'PEPAR1': [-1, 1, -1],
        'PEPAR2': [-1] * 3, 'PEPAR1TYP': [-1, 1, -1], 'PEPAR2TYP': [-1] * 3,
        'A_AGE': [40, 10, 9], 'PRCITSHP': [1] * 3, 'PEFNTVTY': [57] * 3,
        'PEMNTVTY': [57] * 3, 'PEHSPNON': [2, 1, 2], 'PRDTRACE': [1] * 3})
    monkeypatch.setattr(adapter, 'lineage_membership_masks', lambda d, civ: {'all': np.array([False, True, True])})
    mask, _ = adapter.membership(d, np.ones(3, bool), 'white_children')
    assert mask.tolist() == [True, False, False]


def test_completed_parent_children_enter_lineage_precedence():
    d = pd.DataFrame({'PH_SEQ': [7] * 4, 'PPPOS': [1, 2, 3, 4], 'A_LINENO': [1, 2, 3, 4],
        'PEPAR1': [-1, 1, -1, 3], 'PEPAR2': [-1] * 4, 'PEPAR1TYP': [-1, 1, -1, 1],
        'PEPAR2TYP': [-1] * 4, 'A_AGE': [40, 10, 40, 9], 'PRCITSHP': [1] * 4,
        'PEFNTVTY': [57] * 4, 'PEMNTVTY': [57] * 4, 'PENATVTY': [57] * 4,
        'PRDTHSP': [0] * 4})
    completion = [{'PH_SEQ': 7, 'PPPOS': 1, 'central_reporter': True}]
    masks = adapter.lineage_membership_masks(d, np.ones(4, bool), completion=completion)
    assert masks['union'].tolist() == [True, False, False, False]
    assert masks['all'].tolist() == [True, True, False, False]
    with pytest.raises(SystemExit, match='completion record missing'):
        adapter.lineage_membership_masks(d.iloc[1:], np.ones(3, bool), completion=completion)


def test_shared_original_union_rule_matches_frozen_principal():
    d = pd.DataFrame({'PH_SEQ': range(6), 'PPPOS': [1] * 6, 'A_LINENO': [1] * 6,
        'PEPAR1': [-1] * 6, 'PEPAR2': [-1] * 6, 'PEPAR1TYP': [-1] * 6, 'PEPAR2TYP': [-1] * 6,
        'A_AGE': [40] * 6, 'PRPERTYP': [2, 2, 2, 2, 2, 1],
        'PRCITSHP': [4, 1, 1, 1, 4, 1], 'PENATVTY': [303, 57, 57, 57, 57, 57],
        'PEFNTVTY': [57, 303, 57, 57, 57, 57], 'PEMNTVTY': [57, 57, 57, 999, 57, 57],
        'PRDTHSP': [0, 0, 1, 1, 0, 1]})
    principal = adapter.load(adapter.FISCAL / 'mixed_unit_credits_2026_10_14/credits.py', 'fixture_principal_groups')
    civ, union, _ = principal.groups(d)
    masks = adapter.lineage_membership_masks(d, civ, completion=[])
    assert union.tolist() == [True, True, True, False, False, False]
    assert np.array_equal(masks['original'], union)


def test_frozen_sibling_loader_imports_pension_membership():
    pension = adapter.source_module('pensions', 'fixture')
    import membership
    assert Path(membership.__file__).resolve().parent == adapter.SOURCE
    assert pension.OUT.is_relative_to(adapter.LANE)


def test_source_snapshot_still_matches_and_poison_fails(monkeypatch):
    adapter.verify_source()
    monkeypatch.setattr(adapter, 'digest', lambda path: 'poison')
    with pytest.raises(SystemExit, match='source bytes unchanged'):
        adapter.verify_source()


def test_new_survivor_filer_keeps_income_only_on_after_return():
    original = pd.DataFrame({'row': [0], 'spouse': [-1], 'status': ['single']})
    after = pd.concat([original, pd.DataFrame({'row': [1], 'spouse': [-1], 'status': ['hoh']})], ignore_index=True)
    fields = pd.DataFrame({'year': [2024, 2024], 'statefip': [6, 6], 'page': [40, 25], 'mstat': [1, 1],
                           'pwages': [50000, 12000], 'depx': [0, 1], 'pensions': [0, 500]})
    d = pd.DataFrame({'STATETAX_A': [2000, 0]})
    reg, before = adapter.state_registry(d, original, {'afterR': after, 'after_input': fields, 'before_input': fields.iloc[:1]})
    assert reg.row.tolist() == [0, 1]
    assert before.iloc[1].pwages == before.iloc[1].depx == before.iloc[1].pensions == 0
    assert fields.iloc[1].pwages == 12000
    d.loc[1, 'STATETAX_A'] = 1
    with pytest.raises(SystemExit, match='no booked original state liability'):
        adapter.state_registry(d, original, {'afterR': after, 'after_input': fields, 'before_input': fields.iloc[:1]})


def test_kernel_reuse_is_exact_input_and_does_not_alias_results():
    events = []
    kernel = SimpleNamespace(verify_sources=lambda: events.append('verify'))
    def native(frame):
        events.append('run')
        return pd.DataFrame({'liability': frame.income * .1})
    cache = adapter.TaxsimCache()
    frame = pd.DataFrame({'income': [100, 200]})
    first = cache.run(kernel, native, frame)
    first.iloc[0, 0] = -999
    assert cache.run(kernel, native, frame).liability.tolist() == [10, 20]
    assert cache.run(kernel, native, frame.iloc[::-1]).liability.tolist() == [20, 10]
    assert events.count('verify') == 3
    assert events.count('run') == 2
    assert cache.bytes <= 64_000_000


def test_half_overlap_uncertainty_keeps_signed_covariance(tmp_path, monkeypatch):
    monkeypatch.setattr(finalize, 'OUT', tmp_path)
    for base in ('white', 'black'):
        for suffix, direction, population in (('children', 1., 100.), ('children_round3', -1., 120.)):
            v = np.full(161, 4.)
            v[1:] += direction
            pd.DataFrame([{'method': 'set', 'end': 'low', 'component': component,
                **{f'r{i}': x for i, x in enumerate(v)}} for component in ('bounded_low', 'M1_federal')]).to_csv(
                    tmp_path / f'{base}_{suffix}_replicates.csv', index=False)
            (tmp_path / f'{base}_{suffix}_summary.json').write_text(json.dumps({'counts': {'members': {
                'records': 10, 'weighted_persons': population, 'replicate_counts': [population] * 161}},
                'results': [{'method': 'set', 'end': 'low', 'reading': 'bounded_low', 'arm': '',
                             'parts': {'M1_federal': {'bn': 4., 'se_bn': 2.}}}]}))
    finalize.interpolate_comparator_halves()
    got = json.loads((tmp_path / 'white_children_half_summary.json').read_text())
    assert got['results'][0]['bn'] == 4.
    assert got['results'][0]['se_bn'] == 0.   # Opposing signed errors cancel; averaging SEs would not.
    assert got['counts']['members']['weighted_persons'] == 110.


def test_completion_credit_is_subtracted_once_from_each_paired_stack(monkeypatch):
    credit, receipt = finalize.completion_credit_already_booked()
    assert credit.shape == (161,) and abs(receipt['already_booked_bn'] - .3254843214294949) < 1e-12
    rows = [{'method': method, 'end': end, 'component': reading,
             **{f'r{i}': float(credit[i] + 1.) for i in range(161)}}
            for method in ('set', 'cash') for end in ('low', 'high') for reading in ('bounded_low', 'bounded_high')]
    corrected, _ = finalize.subtract_completion_credit(pd.DataFrame(rows).set_index(['method', 'end', 'component']))
    for method in ('set', 'cash'):
        for end in ('low', 'high'):
            assert np.max(abs(corrected.loc[(method, end, 'bounded_low')].to_numpy(float) - 1.)) < 1e-12
            assert np.array_equal(corrected.loc[(method, end, 'completion_credit_already_booked')].to_numpy(float), -credit)
    monkeypatch.setattr(finalize, 'digest', lambda path: 'poison')
    with pytest.raises(SystemExit, match='case source pin'):
        finalize.completion_credit_already_booked()


def test_missing_source_generation_cannot_silently_sum_to_zero():
    missing = pd.DataFrame(columns=['method', 'end', 'component', 'generation'] + [f'r{i}' for i in range(161)])
    with pytest.raises(SystemExit, match='exactly its three generation vectors'):
        finalize.source_vector(missing, 'set', 'low', 'bounded_low')


@pytest.mark.parametrize('group', adapter.GROUPS)
def test_actual_stacks_close_and_se_uses_signed_paired_replicates(group):
    summary = json.loads((adapter.OUT / f'{group}_summary.json').read_text())
    reps = pd.read_csv(adapter.OUT / f'{group}_replicates.csv')
    for row in summary['results']:
        selected = reps[(reps.method == row['method']) & (reps.end == row['end']) & (reps.component == row['reading'])]
        v = selected.iloc[0, 3:].to_numpy(float)
        assert abs(v[0] - row['bn']) < 1e-9
        assert abs(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()) - row['se_bn']) < 1e-9
        assert abs(sum(p['bn'] for p in row['parts'].values()) - row['bn']) < 1e-9
        assert row['parts']['M6_biological_children']['bn'] == 0
        assert row['parts']['D_added_residual']['bn'] == 0
        assert row['parts']['membership_benefit_interaction']['bn'] == 0
        assert row['parts']['M5_SNAP_key']['bn'] == -row['parts']['M4_SNAP_baseline_interaction']['bn']

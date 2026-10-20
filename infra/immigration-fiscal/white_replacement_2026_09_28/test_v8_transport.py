"""Independent checks that v8 additions neither vanish nor leak to comparators."""
import json
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
CASE = HERE.parent / 'main_case_2026_10_16'


def load(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize('suffix,payload_name', [('', 'corrections.json'), ('_cash', 'corrections_cash.json')])
def test_post_engine_carried_once_and_base_unchanged(suffix, payload_name):
    payload = load(CASE / 'derived' / payload_name)['meta']
    full = load(HERE / f'derived/engine_lines_oct16{suffix}.json')
    union = load(HERE / f'derived/engine_lines_oct16_union{suffix}.json')
    for end in ('low', 'high'):
        post=full[end]['post_engine']
        expected=post['mixed_unit_removal_bn']+post['coverage_bn']+sum(full[end]['v9_parts'].values())
        assert expected==pytest.approx(post['total_bn'],abs=1e-9)
        # The inherited terms come from the payload, not the dump: v9's coverage repricing is a separate post term.
        assert post['mixed_unit_removal_bn']==pytest.approx(payload['mixed_unit_removal']['by_end'][end]['total_bn'],abs=1e-9)
        assert post['coverage_bn']+full[end]['v9_parts']['coverage_repricing']==pytest.approx(
            payload['coverage']['by_end'][end]['total_bn'],abs=1e-9)
        assert full[end]['cost_bn'] == pytest.approx(-full[end]['welfare_bn'] + full[end]['capital_bn'] + expected, abs=1e-9)
        assert union[end]['post_engine']['total_bn'] == 0
        carriers = [x for x in union[end]['lines'] if x['id'].startswith('union_completion_')]
        assert carriers and all(x['amount_bn'] == 0 for x in carriers)


def test_completed_population_and_comparator_asymmetry():
    payload = load(CASE / 'derived/corrections.json')['meta']
    results = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    current = results[results.membership_rule.eq('current')]
    lineage = current[current.group.eq('mexican_origin_engine')]
    assert (lineage.population - payload['population_v9']['with_coverage']).abs().max() < 1e-6
    white = current[current.group.eq('A1_third_plus_nh_white')]
    assert (white.population - payload['population_v9']['with_coverage']).abs().max() < 1e-6
    # The paired half-overlap arms may remove more lineage children than the
    # outside block adds; each reading still uses its own exact common count.
    children = results[results.membership_rule.eq('children')]
    keys = ['arm', 'basis', 'end', 'mortality_convention', 'mortality_bound']
    for key, reading in children.groupby(keys):
        line = reading[reading.group.eq('mexican_origin_engine')].iloc[0]
        block = line.lineage_children_block_population
        if '_half_' not in key[0]:
            assert block > 0
        for group in ('mexican_origin_engine', 'mexican_origin_rough', 'A1_third_plus_nh_white'):
            sub = reading[reading.group.eq(group)]
            assert len(sub) == 1
            assert (sub.population - payload['population_v9']['with_coverage'] - block).abs().max() < 1e-6
    audit = load(HERE / 'derived/symmetric_audit_oct16.json')['v8_asymmetry']
    assert audit['union_completion']['total'] > 0
    assert audit['comparator_completion'].startswith('unmeasured')
    assert audit['comparator_mixed_unit_removal'].startswith('measured for A1')
    assert audit['comparator_coverage'].startswith('round 3')


def test_full_union_split_closes_after_synthetic_and_post_engine():
    for suffix in ('', '_cash'):
        full = load(HERE / f'derived/engine_lines_oct16{suffix}.json')
        union = load(HERE / f'derived/engine_lines_oct16_union{suffix}.json')
        for end in ('low', 'high'):
            a, b = full[end], union[end]
            before = {(x['side'], x['id']): x for x in b['lines'] if x['side'] != 'scalar'}
            delta = sum((1 if x['side'] == 'spending' else -1) * x['response'] *
                        (x['amount_bn'] - before[x['side'], x['id']]['amount_bn'])
                        for x in a['lines'] if x['side'] != 'scalar')
            production = lambda d: next(x['effect_bn'] for x in d['lines'] if x['side'] == 'scalar' and x['id'] == 'production_gain_bn')
            delta += a['capital_bn'] - b['capital_bn'] - production(a) + production(b) + a['post_engine']['total_bn']
            assert delta == pytest.approx(a['cost_bn'] - b['cost_bn'], abs=1e-9)


def test_reporter_receipts_and_resource_terms_use_economic_side():
    carriers = load(CASE / 'derived/corrections.json')['meta']['union_completion']['carriers']
    summary = pd.read_csv(HERE / 'derived/rekey_summary_oct16.csv').query("group == 'mexican_origin_engine'")
    for basis, suffix in (('accrual', ''), ('cash', '_cash')):
        dumps = load(HERE / f'derived/engine_lines_oct16{suffix}.json')
        for end in ('low', 'high'):
            rows = dumps[end]['lines']
            receipts = sum(x['amount_bn'] for x in rows if x['side'] == 'receipts')
            spending = 0.0
            for row in rows:
                if row['side'] != 'spending':
                    continue
                source = carriers.get(row['id'])
                if source and source['kind'] in ('capital', 'production'):
                    continue
                if source and source.get('side') == 'receipt':
                    receipts -= row['amount_bn']
                else:
                    spending += row['amount_bn']
            actual = summary[(summary.basis == basis) & (summary.end == end)].iloc[0]
            assert actual.taxes_paid == pytest.approx(receipts, abs=5e-5)
            assert actual.spending_drawn == pytest.approx(spending, abs=5e-5)


def test_attribution_exports_both_post_engine_components():
    meta = load(CASE / 'derived/corrections.json')['meta']
    d = pd.read_csv(HERE / 'derived/attribution_buckets_oct16.csv')
    for step in ('4', '5'):
        for end in ('low', 'high'):
            rows = d[(d.step.astype(str) == step) & (d.end == end)
                     & (d.group == 'mexican_origin_rough')].set_index('bucket')
            full=load(HERE/'derived/engine_lines_oct16.json')[end]
            declared = {'mixed_unit_removal_bn': meta['mixed_unit_removal']['by_end'][end]['total_bn'],
                        'coverage_bn': meta['coverage']['by_end'][end]['total_bn'] - full['v9_parts']['coverage_repricing']}
            for name, field in (('mixed_unit_removal', 'mixed_unit_removal_bn'), ('coverage', 'coverage_bn')):
                actual = rows.loc['lineage post-engine ' + field, 'cost_bn']
                assert actual == pytest.approx(full['post_engine'][field], abs=5e-5)
                assert actual == pytest.approx(declared[field], abs=5e-5)
            fiscal=sum(rows.loc['lineage post-engine '+field,'cost_bn'] for field in
                       ('mixed_unit_removal_bn','coverage_bn','v9_additions_bn'))
            classified=full['v9_classified']
            assert fiscal==pytest.approx(full['post_engine']['total_bn']-classified['capital_bn']+classified['production_gain_bn'],abs=1.5e-4)

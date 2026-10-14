"""Check the engine-dump leaf independently of rough comparator pricing."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

FISCAL = Path(__file__).resolve().parent.parent
CASE = FISCAL / 'main_case_2026_10_15'
LANES = ('white_replacement_2026_09_28', 'black_comparator_rough_2026_09_28')


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label, actual, expected, tolerance):
    if abs(actual - expected) >= tolerance:
        raise SystemExit(f'[BLOCKED] {label}: {actual!r} vs {expected!r} (tolerance {tolerance})')
    return {'gate': label, 'actual': actual, 'expected': expected, 'tolerance': tolerance}


def main():
    summary = load(CASE / 'derived/summary.json')
    lineage = load(CASE / 'derived/lineage_addition.json')
    payload = load(CASE / 'derived/corrections.json')
    if payload['meta'].get('adopted') != '2026-10-15':
        raise SystemExit('[BLOCKED] the dump leaf requires the adopted October 15 case')
    bands = {r['variant']: r for r in csv.DictReader((CASE / 'derived/main_case_bands.csv').open())
             if r['profile'] == 'long_run_non_school_full'}
    inputs = [CASE / 'derived' / n for n in ('corrections.json', 'corrections_cash.json', 'summary.json',
               'lineage_addition.json', 'main_case_bands.csv')]
    inputs += [CASE / 'package.cjs', FISCAL / 'job_capital_taxes_2026_10_14/derived/item.json']
    jobs = load(inputs[-1])
    job_lines = {'corporate_capital': 'corporate', 'corporate_labor': 'corporate',
                 'remaining_production_property': 'business_property', 'other_production_taxes': 'other_production_taxes'}
    rows, outputs = [], {}
    for lane_name in LANES:
        lane = FISCAL / lane_name
        inputs.append(lane / 'engine_lines.cjs')
        for basis, suffix, block, band in (('accrual', '', 'set', 'adopted'), ('cash', '_cash', 'cash', 'cash_set')):
            full_path = lane / f'derived/engine_lines_oct15{suffix}.json'
            union_path = lane / f'derived/engine_lines_oct15_union{suffix}.json'
            full, union = load(full_path), load(union_path)
            for p in (full_path, union_path):
                outputs[str(p.relative_to(FISCAL))] = digest(p)
            for i, end in enumerate(('low', 'high')):
                label = f'{lane_name} {basis} {end}'
                for name, dump in (('full', full), ('union', union)):
                    declared = summary['v8']['end_specifications'][block]
                    if declared[0] != declared[1] or dump[end]['spec'] != declared[0][i] or dump[end]['allocation'] != 'personal':
                        raise SystemExit(f'[BLOCKED] {label} {name}: incorrect end specification/allocation')
                    rows.append(check(f'{label} {name} cost accounting', dump[end]['cost_bn'],
                                      -dump[end]['welfare_bn'] + dump[end]['capital_bn'] + dump[end]['post_engine']['total_bn'], 1e-9))
                rows.append(check(f'{label} authoritative band', full[end]['cost_bn'], float(bands[band][f'cost_{end}_bn']), 5e-5))
                fl = {(x['side'], x['id']): x for x in full[end]['lines'] if x['side'] != 'scalar'}
                ul = {(x['side'], x['id']): x for x in union[end]['lines'] if x['side'] != 'scalar'}
                delta = sum((1 if side == 'spending' else -1) * (line['amount_bn'] - ul[side, lid]['amount_bn']) * line['response']
                            for (side, lid), line in fl.items())
                prod = lambda d: next(x['effect_bn'] for x in d['lines'] if x['side'] == 'scalar' and x['id'] == 'production_gain_bn')
                delta += full[end]['capital_bn'] - union[end]['capital_bn'] - prod(full[end]) + prod(union[end])
                delta += full[end]['post_engine']['total_bn'] - union[end]['post_engine']['total_bn']
                rows.append(check(f'{label} full less base union line/post-engine split', full[end]['cost_bn'] - union[end]['cost_bn'], delta, 1e-9))
                for line in union[end]['lines']:
                    category = job_lines.get(line['id'])
                    if line['side'] == 'receipts' and category:
                        rows.append(check(f'{label} {line["id"]} R7 response', line['response'],
                                          payload['meta']['responses'][line['id']][end], 1e-12))
    metadata = {'case': 'oct15', 'scope': 'engine dump leaf only; rough comparator pricing has separate gates',
                'gates': rows, 'inputs_sha256': {str(p.relative_to(FISCAL)): digest(p) for p in inputs},
                'outputs_sha256': outputs}
    for name in LANES:
        (FISCAL / name / 'derived/engine_lines_oct15_meta.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'[PASS] {len(rows)} engine-dump leaf gates')


if __name__ == '__main__':
    main()

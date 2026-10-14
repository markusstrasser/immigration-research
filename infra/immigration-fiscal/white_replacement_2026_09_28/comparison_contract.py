"""One-engine contrasts and the separately itemized case-to-rough bridge."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

MIXED_SOURCE = Path(__file__).resolve().parent.parent / 'mixed_unit_comparators_2026_10_15/derived'
MIXED_PINS = {
    'white_summary.json': '121b787f04637b43d698555fade2b115686f15fa7f30d4d5167ac5c3d4477081',
    'black_summary.json': '2cf7a859a12a3775a385440347ebf7851630302b56b95dbbd00847b26d7c2409',
    'gaps.csv': 'b28eced6679186982310efef4192e718a6f58a74cfbbb3e35e8d02566babb794',
}
MIXED_GROUPS = {'A1_third_plus_nh_white': 'white', 'nh_black_rough': 'black'}
MIXED_FRAME = '[FRAMING-SENSITIVE] whole-person static removal; conditional survivor solve'


def load_mixed_unit(source=MIXED_SOURCE):
    """Frozen own-mask terms. Never called from the comparator evaluator/setup."""
    contents = {}
    for name, expected in MIXED_PINS.items():
        path = source / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'[BLOCKED] comparator item11 sha256 mismatch: {path}')
        contents[name] = path.read_text()
    gaps = list(csv.DictReader(contents['gaps.csv'].splitlines()))
    return {'summaries': {group: json.loads(contents[f'{group}_summary.json']) for group in ('white', 'black')},
            'gaps': gaps, 'sha256': dict(MIXED_PINS)}


def comparator_removal(source, group, basis, end, population):
    if group not in MIXED_GROUPS:
        return dict(bn=0., paired_se_bn=None, scope='unmeasured for this membership/age definition')
    mask = MIXED_GROUPS[group]
    method = 'set' if basis == 'accrual' else basis
    reading = f'bounded_{end}'
    entries = [r for r in source['summaries'][mask]['results']
               if (r['method'], r['end'], r['reading']) == (method, end, reading)]
    gaps = [r for r in source['gaps'] if (r['group'], r['method'], r['end'], r['reading']) ==
            (mask, method, end, reading)]
    if len(entries) != 1 or len(gaps) != 2:
        raise SystemExit('[BLOCKED] comparator item11 endpoint/reading not unique')
    own = float(gaps[0]['comparator_own_count'])
    frame = 'own_count' if abs(population - own) < 1e-6 else 'lineage_count'
    paired = next(r for r in gaps if r['population_basis'] == frame)
    expected_population = own if frame == 'own_count' else float(paired['lineage_count'])
    if abs(population - expected_population) > 1e-6:
        raise SystemExit('[BLOCKED] comparator item11 population differs from paired source')
    amount = entries[0]['bn'] * population / own
    if not math.isfinite(amount) or abs(amount - float(paired['comparator_adjustment_bn'])) > 1e-9:
        raise SystemExit('[BLOCKED] comparator item11 own-count standardization mismatch')
    return dict(bn=amount, paired_se_bn=float(paired['item11_paired_se_bn']),
                own_count=own, scope='measured own membership; linear population standardization; ' + MIXED_FRAME)


def engine_for(group):
    return 'case' if group == 'mexican_origin_engine' else 'rough'


def publish_base_summary(summary, lineage_population):
    """Add own-mask survivor terms to published costs, retaining evaluator controls.

    Rounded baseline amounts retain their original precision. This runs only in
    producer main(), after all evaluator/decomposition gates, never in run29.
    """
    source = load_mixed_unit()
    lineage_rows = {(row['basis'], row['end']): row for row in summary if row['group'] == 'mexican_origin_rough'}
    for row in summary:
        if 'cost_evaluator_bn' in row:
            raise SystemExit('[BLOCKED] comparator item11 already published; refusing double application')
        group, basis, end = row['group'], row['basis'], row['end']
        population = (lineage_population if group == 'A1_third_plus_nh_white' else
                      float(next(r['comparator_own_count'] for r in source['gaps'] if r['group'] == 'black'))
                      if group == 'nh_black_rough' else float(row['population']))
        term = comparator_removal(source, group, basis, end, population)
        amount = term['bn']
        row['cost_evaluator_bn'] = row['cost']
        row['comparator_item11_bn'] = amount
        row['lineage_item11_bn'] = row.get('mixed_unit_removal_bn', '')
        if not group.startswith('mexican_'):
            row['mixed_unit_removal_bn'] = amount
        row['item11_paired_se_bn'] = term['paired_se_bn']
        row['mixed_unit_asymmetry'] = term['scope'] if not group.startswith('mexican_') else 'lineage measured; A1/Black counterparts measured'
        row['framing'] = MIXED_FRAME
        row['cost_one_sided_bn'] = row['cost']
        row['cost'] = f"{float(row['cost']) + amount:.4f}"
        row['cost_per_member'] = f"{float(row['cost']) * 1e9 / population:.0f}"
        for key in ('net_budget', 'spending_saved'):
            if key in row:
                row[key + '_evaluator_bn'] = row[key]
                row[key] = f"{float(row[key]) + amount:.4f}"
        row['balance_scope'] = 'allocated member lines; survivor post-engine term excluded, as on lineage side'
        for key in ('cost_cps', 'cost_top_tail_proportional', 'cost_capital_taxes_respond',
                    'cost_both_arms', 'cost_others_at_national_prices', 'cost_ex_old_age'):
            if key in row and row[key] != '':
                row[key + '_evaluator_bn'] = row[key]
                row[key] = f"{float(row[key]) + amount:.4f}"
        gap_keys = [key for key in row if key.startswith('delta_like_for_like')]
        gap_keys += ['black_minus_lineage_own_count_bn', 'black_minus_lineage_equal_population_bn']
        for key in gap_keys:
            if key not in row or row[key] == '':
                continue
            row[key + '_one_sided'] = row[key]
            direction = 1 if key.startswith('black_') else -1
            scale = lineage_population / population if key == 'black_minus_lineage_equal_population_bn' else 1.
            precision = 4 if isinstance(row[key], str) else 12
            row[key] = f"{float(row[key]) + direction * amount * scale:.{precision}f}"
        for key in ('per_member_over_rough_union', 'per_member_over_engine_union'):
            if key in row and row[key] != '':
                row[key + '_one_sided'] = row[key]
                lineage = lineage_rows[basis, end]
                denominator = float(lineage['cost']) / lineage_population
                row[key] = f"{float(row['cost']) / population / denominator:.4f}"
        if group in MIXED_GROUPS:
            if 'delta_without_item11_bn' in row and row['delta_without_item11_bn'] != '':
                # The comparator term cancels when excluding item11 on both sides.
                row['delta_one_sided_bn'] = row.get('delta_like_for_like_bn_one_sided', '')
            if 'black_minus_lineage_without_item11_bn' in row:
                row['black_minus_lineage_one_sided_bn'] = row.get('black_minus_lineage_own_count_bn_one_sided', '')
    # All CSV rows need the same schema, including baseline-only noncomparators.
    fields = dict.fromkeys(key for row in summary for key in row)
    for row in summary:
        for key in fields:
            row.setdefault(key, '')


def require_same_engine(left, right):
    if not left.get('engine') or left.get('engine') != right.get('engine'):
        raise SystemExit('[BLOCKED] comparison sides have missing or different engine tags')


def gap_fields(lineage, white, black, item11):
    require_same_engine(lineage, white)
    require_same_engine(lineage, black)
    if abs(lineage['population'] - white['population']) > 1e-6:
        raise SystemExit('[BLOCKED] white comparison does not match lineage population (1e-6 persons)')
    white_gap = lineage['cost_bn'] - white['cost_bn']
    black_gap = black['cost_bn'] - lineage['cost_bn']
    factor = lineage['population'] / black['population']
    equal = black['cost_bn'] * factor - lineage['cost_bn']
    return dict(lineage_engine=lineage['engine'], comparator_engine=white['engine'],
                white_gap_rough_lineage_bn=white_gap,
                black_minus_rough_lineage_bn=black_gap,
                black_minus_rough_lineage_equal_population_bn=equal,
                white_gap_one_sided_bn=white_gap + white.get('comparator_item11_bn', 0.),
                black_minus_lineage_one_sided_bn=black_gap - black.get('comparator_item11_bn', 0.),
                white_gap_without_item11_bn=white_gap - item11 + white.get('comparator_item11_bn', 0.),
                black_minus_lineage_without_item11_bn=black_gap + item11 - black.get('comparator_item11_bn', 0.),
                black_minus_lineage_equal_population_without_item11_bn=equal + item11 - black.get('comparator_item11_bn', 0.) * factor,
                white_comparator_item11_bn=white.get('comparator_item11_bn', 0.),
                black_comparator_item11_bn=black.get('comparator_item11_bn', 0.),
                white_item11_paired_se_bn=white.get('item11_paired_se_bn'),
                black_item11_paired_se_bn=black.get('item11_paired_se_bn'),
                lineage_population=lineage['population'], black_own_population=black['population'],
                mixed_unit_removal_bn=item11,
                mixed_unit_asymmetry='item11 measured for lineage, A1 whites and Black; other age/membership definitions unmeasured',
                framing=MIXED_FRAME)


def bridge_parts(case_run, rough_run, carriers=None):
    """All evaluated line responses plus resource and post-engine components."""
    carriers = carriers or {}
    case, case_lines = case_run[:2]
    rough, rough_lines = rough_run[:2]
    def components(result, lines, buckets):
        out = {(side, lid): (1 if side == 'spending' else -1) * amount * response
               for side, lid, _, amount, response in lines
               if carriers.get(lid, {}).get('kind') not in ('capital', 'production')}
        out[('resource', 'capital_return')] = result['capital']
        out[('resource', 'production_gain')] = -result['production_gain']
        for key, value in buckets.items():
            if key.startswith('lineage post-engine '):
                out[('post_engine', key.removeprefix('lineage post-engine '))] = value
        if abs(sum(out.values()) - result['cost']) > 1e-9:
            raise SystemExit('[BLOCKED] bridge side decomposition does not close (1e-9bn)')
        return out
    a, b = components(case, case_lines, case_run[2]), components(rough, rough_lines, rough_run[2])
    parts = [dict(side=side, line=lid, case_bn=a.get((side, lid), 0.),
                  rough_bn=b.get((side, lid), 0.),
                  case_minus_rough_bn=a.get((side, lid), 0.) - b.get((side, lid), 0.))
             for side, lid in sorted(a.keys() | b.keys())]
    target = case['cost'] - rough['cost']
    if abs(sum(x['case_minus_rough_bn'] for x in parts) - target) > 1e-9:
        raise SystemExit('[BLOCKED] itemized case-to-rough bridge does not close (1e-9bn)')
    return parts

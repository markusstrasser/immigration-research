"""One-engine contrasts and the separately itemized case-to-rough bridge.

Round 3 (C3 fixes 5 and 6, 2026-10-15): every group passed to comparator_removal() must be registered (REGISTRY) as
measured, reweighted from a measured group, intentionally unmeasured, or the lineage; anything else stops [BLOCKED].
A measured or reweighted term carries its spending and receipt parts (PART_SIDE), so a published spending_saved column
holds spending only. The children rule's terms (members' biological minor children depart and count as members, with
each group's own Census coverage) are members_removal()'s.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

MIXED_SOURCE = Path(__file__).resolve().parent.parent / 'mixed_unit_comparators_2026_10_15/derived'
MIXED_PINS = {
    'white_summary.json': '121b787f04637b43d698555fade2b115686f15fa7f30d4d5167ac5c3d4477081',
    'black_summary.json': '2cf7a859a12a3775a385440347ebf7851630302b56b95dbbd00847b26d7c2409',
    'white_children_summary.json': '647223a2ca64fdc17688ffda01d1614c7f533e3650fc02ac56682f58daaf99d3',
    'black_children_summary.json': 'b2ac50210518879a49c6f7fa085117c0606a6e0c4fbd501be6ac3bb65951c9b9',
    'gaps.csv': '18112e8cf04bb4afe6a5db603b70e1761ca024f787fcf02f05b6da9e0d4831ef',
}
MIXED_GROUPS = {'A1_third_plus_nh_white': 'white', 'nh_black_rough': 'black'}
MIXED_FRAME = '[FRAMING-SENSITIVE] whole-person static removal; conditional survivor solve'
# Every group a caller may pass: measured on its own mask, reweighted from a measured group's record-level parts,
# intentionally unmeasured (stated in the row), or the lineage (its item 11 is the case's). Prefix rules cover the
# Indian lane's and the lineage's families; a name no rule covers is invalid.
REGISTRY = {
    'A1_third_plus_nh_white': ('measured', 'white'),
    'nh_black_rough': ('measured', 'black'),
    'A3_third_plus_nh_white_at_union_ages': ('reweighted', 'white'),
    'A4_third_plus_nh_white_stationary': ('reweighted', 'white'),
    'A2_us_born_nh_white': ('unmeasured', 'its own mask (US-born NH whites) was not solved'),
    'all_residents_slice': ('unmeasured', 'a population slice, not a membership definition'),
}
PREFIXES = (('mexican_origin_', ('lineage', 'the case measures the lineage\'s item 11')),
            ('india_born', ('unmeasured', 'the Indian-origin masks were not solved')),
            ('indian_origin', ('unmeasured', 'the Indian-origin masks were not solved')))
# Item 11's parts: receipts are survivors' taxes; spending is their benefits and refundable credits.
PART_SIDE = {'M1_federal': 'receipts', 'M2_state': 'receipts', 'M5_consumption': 'receipts',
             'M5_owner_property': 'receipts', 'M6_biological_children': 'receipts',
             'M3_refunds': 'spending', 'D_added_residual': 'spending', 'M5_SNAP_key': 'spending',
             'M5_housing_key': 'spending', 'M4_SNAP_baseline_interaction': 'spending',
             'membership_benefit_interaction': 'spending', 'Medicaid': 'spending', 'ACA': 'spending', 'SNAP': 'spending'}
# The unit each part is solved on, for the record-level reweighting of A3 and A4 (reweight_ratios()).
PART_UNIT = {'M1_federal': 'tax', 'M2_state': 'tax', 'M3_refunds': 'tax', 'M6_biological_children': 'tax',
             'D_added_residual': 'tax', 'ACA': 'tax', 'M5_owner_property': 'household'}
REWEIGHT_RULE = ('A1\'s item 11 by part, each part scaled by the scenario\'s share of weight on A1 members in mixed '
                 'units of the part\'s kind (tax unit, SPM unit, household) over A1\'s share [ASSUMPTION: survivor terms '
                 'uniform per departing member within a mixed unit of that kind]')
RULES = {'current': '', 'children': '_children'}


def registered(group):
    if group in REGISTRY:
        return REGISTRY[group]
    for prefix, entry in PREFIXES:
        if group.startswith(prefix):
            return entry
    raise SystemExit(f'[BLOCKED] comparator group {group!r} is not registered for item 11 (comparison_contract.REGISTRY)')


def load_mixed_unit(source=MIXED_SOURCE):
    """Frozen own-mask terms. Never called from the comparator evaluator/setup."""
    contents = {}
    for name, expected in MIXED_PINS.items():
        path = source / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'[BLOCKED] comparator item11 sha256 mismatch: {path}')
        contents[name] = path.read_text()
    gaps = list(csv.DictReader(contents['gaps.csv'].splitlines()))
    return {'summaries': {group: json.loads(contents[f'{group}_summary.json'])
                          for group in ('white', 'black', 'white_children', 'black_children')},
            'gaps': gaps, 'sha256': dict(MIXED_PINS)}


def entry(source, mask, method, end):
    reading = f'bounded_{end}'
    entries = [r for r in source['summaries'][mask]['results']
               if (r['method'], r['end'], r['reading']) == (method, end, reading)]
    gaps = [r for r in source['gaps'] if (r['group'], r['method'], r['end'], r['reading']) ==
            (mask, method, end, reading)]
    if len(entries) != 1 or len(gaps) != 2:
        raise SystemExit('[BLOCKED] comparator item11 endpoint/reading not unique')
    return entries[0], gaps


def split(parts, scale=1., factors=None):
    """Spending and receipt parts of a scaled item 11; every part must have a side."""
    if set(parts) - set(PART_SIDE):
        raise SystemExit(f'[BLOCKED] item 11 part without a side: {sorted(set(parts) - set(PART_SIDE))}')
    out = {'spending': 0., 'receipts': 0.}
    for name, part in parts.items():
        out[PART_SIDE[name]] += part['bn'] * scale * (1. if factors is None else factors[PART_UNIT.get(name, 'spm')])
    return out


def checked(term):
    """A measured or reweighted row carries every field; its parts add to its amount."""
    for key in ('bn', 'spending_bn', 'receipt_bn', 'own_count'):
        if not isinstance(term.get(key), float) or not math.isfinite(term[key]):
            raise SystemExit(f'[BLOCKED] measured comparator item11 lacks a finite {key}')
    if abs(term['spending_bn'] + term['receipt_bn'] - term['bn']) > 1e-9:
        raise SystemExit('[BLOCKED] item11 spending and receipt parts do not add to the term (1e-9bn)')
    return term


def comparator_removal(source, group, basis, end, population, reweight=None):
    """The current rule's item 11 for a registered group at `population` (its own count or the lineage's)."""
    status, mask = registered(group)
    if status in ('unmeasured', 'lineage'):
        scope = 'lineage measured in the case' if status == 'lineage' else f'unmeasured: {mask}'
        return dict(bn=0., paired_se_bn=None, scope=scope, status=status, spending_bn=0., receipt_bn=0.)
    method = 'set' if basis == 'accrual' else basis
    row, gaps = entry(source, mask, method, end)
    own = float(gaps[0]['comparator_own_count'])
    if status == 'reweighted':
        if reweight is None or group not in reweight:
            raise SystemExit(f'[BLOCKED] {group} item 11 needs its record-level reweighting factors')
        factors = reweight[group]
        parts = split(row['parts'], population / own, factors)
        amount = parts['spending'] + parts['receipts']
        return checked(dict(bn=amount, paired_se_bn=None, own_count=own, status=status,
                            spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                            scope=f'reweighted from A1: {REWEIGHT_RULE}; paired SE not computed; ' + MIXED_FRAME))
    frame = 'own_count' if abs(population - own) < 1e-6 else 'lineage_count'
    paired = next(r for r in gaps if r['population_basis'] == frame)
    expected_population = own if frame == 'own_count' else float(paired['lineage_count'])
    if abs(population - expected_population) > 1e-6:
        raise SystemExit('[BLOCKED] comparator item11 population differs from paired source')
    amount = row['bn'] * population / own
    if not math.isfinite(amount) or abs(amount - float(paired['comparator_adjustment_bn'])) > 1e-9:
        raise SystemExit('[BLOCKED] comparator item11 own-count standardization mismatch')
    parts = split(row['parts'], population / own)
    return checked(dict(bn=amount, paired_se_bn=float(paired['item11_paired_se_bn']),
                        own_count=own, status=status, spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                        scope='measured own membership; linear population standardization; ' + MIXED_FRAME))


def true_count_removal(source, group, basis, end, population, true_own, rule):
    """Item 11 under a membership rule ('current', or 'children': members' biological minor children depart and count
    as members) for `population` people, from the term measured on the group's observed mask.

    Coverage's missed people add no mixed-unit term [ASSUMPTION, as their custody and arrests are held]: the per-person
    amount is the measured term over the group's true count. The SE is the comparator side's, scaled the same way; a
    paired SE was not computed for these readings."""
    status, mask = registered(group)
    if status != 'measured':
        raise SystemExit(f'[BLOCKED] true-count item 11 is measured for A1 and Black only, not {group}')
    method = 'set' if basis == 'accrual' else basis
    row, gaps = entry(source, mask + RULES[rule], method, end)
    own = float(gaps[0]['comparator_own_count'])
    if not (math.isfinite(true_own) and true_own > 0):
        raise SystemExit('[BLOCKED] true-count item 11 needs a positive true own count')
    scale = population / true_own
    parts = split(row['parts'], scale)
    return checked(dict(bn=row['bn'] * scale, own_count=own, true_own_count=true_own, status='measured', rule=rule,
                        paired_se_bn=float(gaps[0]['comparator_adjustment_se_bn']) * scale,
                        spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                        scope=f'{rule} rule, own mask; measured term over the true count; comparator-side SE; ' + MIXED_FRAME))


def reweight_ratios(d, civ, weights):
    """Per part kind, a reweighted scenario's share of weight on A1 members in mixed units over A1's share.

    d: the rough frame (PH_SEQ, TAX_ID, SPM_ID); civ: civilians; weights: {'A1': cw, name: cw}, each named scenario a
    reweighting of A1's members (no weight outside them). A unit is mixed when it holds a civilian who is not a member."""
    base = np.asarray(weights['A1'], float)
    member = base > 0
    other = np.asarray(civ, bool) & ~member
    units = {'tax': d.groupby(['PH_SEQ', 'TAX_ID'], sort=False).ngroup().to_numpy(),
             'spm': pd.factorize(d.SPM_ID, sort=False)[0], 'household': pd.factorize(d.PH_SEQ, sort=False)[0]}
    mixed = {}
    for kind, unit in units.items():
        has_other = np.bincount(unit, weights=other.astype(float), minlength=int(unit.max()) + 1) > 0
        mixed[kind] = member & has_other[unit]
    for kind, m in mixed.items():
        if not float(base[m].sum()) > 0:
            raise SystemExit(f'[BLOCKED] A1 has no weight in mixed {kind} units; the reweighting is undefined')
    out = {}
    for name, cw in weights.items():
        if name == 'A1':
            continue
        cw = np.asarray(cw, float)
        if bool((cw[~member] != 0).any()) or not float(cw.sum()) > 0:
            raise SystemExit(f'[BLOCKED] {name} reweighting needs weight on A1 members only')
        out[name] = {kind: (float(cw[m].sum()) / float(cw.sum())) / (float(base[m].sum()) / float(base.sum()))
                     for kind, m in mixed.items()}
    return out


def scenario_reweight(R, scenarios):
    """reweight_ratios() for every registered reweighted scenario in `scenarios`, on the rough frame R."""
    names = [n for n in scenarios if registered(n)[0] == 'reweighted']
    return reweight_ratios(R.d, R.civ, {'A1': scenarios['A1_third_plus_nh_white']['cps_w'],
                                        **{n: scenarios[n]['cps_w'] for n in names}})


def engine_for(group):
    return 'case' if group == 'mexican_origin_engine' else 'rough'


def publish_base_summary(summary, lineage_population, reweight=None):
    """Add own-mask survivor terms to published costs, retaining evaluator controls.

    Rounded baseline amounts retain their original precision. This runs only in
    producer main(), after all evaluator/decomposition gates, never in run29.
    spending_saved takes item 11's spending part; its receipt part (a cost contribution: survivors' extra taxes) lowers
    taxes_lost, so net_budget = spending_saved - taxes_lost still holds. A3 and A4 take A1's term reweighted
    (reweight: scenario_reweight()); without it they stop.
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
        term = comparator_removal(source, group, basis, end, population, reweight=reweight)
        amount = term['bn']
        row['cost_evaluator_bn'] = row['cost']
        row['comparator_item11_bn'] = amount
        row['item11_spending_bn'] = term['spending_bn']
        row['item11_receipt_bn'] = term['receipt_bn']
        row['lineage_item11_bn'] = row.get('mixed_unit_removal_bn', '')
        if not group.startswith('mexican_'):
            row['mixed_unit_removal_bn'] = amount
        row['item11_paired_se_bn'] = term['paired_se_bn']
        row['mixed_unit_asymmetry'] = term['scope'] if not group.startswith('mexican_') else 'lineage measured; A1/Black counterparts measured'
        row['framing'] = MIXED_FRAME
        row['cost_one_sided_bn'] = row['cost']
        row['cost'] = f"{float(row['cost']) + amount:.4f}"
        row['cost_per_member'] = f"{float(row['cost']) * 1e9 / population:.0f}"
        for key, value in (('net_budget', amount), ('spending_saved', term['spending_bn']),
                           ('taxes_lost', -term['receipt_bn'])):
            if key in row:
                row[key + '_evaluator_bn'] = row[key]
                row[key] = f"{float(row[key]) + value:.4f}"
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


def require_stated(mortality_convention):
    """A stated comparison claim pairs every group on one mortality convention; a mixed pair is labelled beside."""
    if mortality_convention == 'mixed mortality conventions':
        raise SystemExit('[BLOCKED] a stated comparison claim cannot rest on a mixed mortality pair')
    return mortality_convention


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

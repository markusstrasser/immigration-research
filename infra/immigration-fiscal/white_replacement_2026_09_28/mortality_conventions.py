"""Explicit round-2 mortality pairing and live pension-dollar substitution.

Imported by symmetric_comparators_oct14.py; no standalone producer. Source
methods are lineage_mortality_2026_10_14/mortality.py case_inputs/profile_deltas.
Native-First: extend the existing comparator CSV producer and source ratios.
"""
from pathlib import Path
import csv
import json
import math

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'lineage_mortality_2026_10_14'
# Round 3 (C3 fix 3a): the source's central rows repriced with the whole-population factor on the left-out share.
MIX = HERE / 'derived/lineage_mortality_mix_oct15.csv'
MIXED = 'mixed mortality conventions'
OWN = 'own-group mortality'
GENERAL = 'whole-population mortality'
OWN_ARMS = {'combined_before_round2', 'combined_bracket_only', 'combined_payroll_only',
            'combined_bracket_payroll_joint', 'mortality_group', 'mortality_symmetric_frame_status',
            'combined_rules_only', 'combined_zero_production',
            # round 3's derived arms on combined_rules_only (DERIVED below) and its school-key diagnostic
            'combined_rules_coverage', 'combined_rules_members', 'combined_rules_rough_school',
            'combined_rules_members_round3', 'combined_rules_members_no_district',
            'combined_rules_members_round3_no_district', 'combined_rules_members_no_row8',
            'combined_rules_members_partial_lineage',
            'combined_rules_members_da_middle', 'combined_rules_members_da_all_black',
            'combined_rules_members_half_white', 'combined_rules_members_half_black'}
# Round 3 (C3 fixes 1, 2, 3b): arms symmetric_comparators_oct14.py derives after the evaluator from
# members_coverage_oct15.py's runs, which rebuild A1 and Black on combined_rules_only's settings (own-group mortality)
# or combined_rules_general's (whole-population): rule 'current' or 'children' (members' biological minor children
# depart and count as members), every comparator at its own Census coverage (central arm). The lineage's coverage is
# the case's; under the children rule it adds its outside-definition children block and their item 11 shift.
DERIVED = {'combined_rules_coverage': dict(base='combined_rules_only', rule='current', mortality='specific'),
           'combined_rules_members': dict(base='combined_rules_only', rule='children', mortality='specific'),
           'combined_rules_members_general': dict(base='combined_rules_general', rule='children', mortality='general')}
for _arm, _options in {
        'round3': dict(rule='children_round3'),
        'no_district': dict(district=False),
        'round3_no_district': dict(rule='children_round3', district=False),
        'no_row8': dict(row8=False),
        'partial_lineage': dict(partial_lineage=True),
        'da_middle': dict(coverage='da_middle'),
        'da_all_black': dict(coverage='da_all_black'),
        'half_white': dict(half='white'),
        'half_black': dict(half='black')}.items():
    DERIVED['combined_rules_members_' + _arm] = dict(base='combined_rules_only', rule='children',
                                                   mortality='specific', **_options) if 'rule' not in _options else {
        'base': 'combined_rules_only', 'mortality': 'specific', **_options}
CENTRAL = dict(arm='combined_rules_members', mortality_convention=OWN)


def read_rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def one(rows, **keys):
    selected = [r for r in rows if all(r.get(k) == v for k, v in keys.items())]
    if len(selected) != 1:
        raise ValueError(f'[BLOCKED] ambiguous mortality source row {keys}')
    return selected[0]


def coefficients(mix=True):
    """Own-group rows from lineage_mortality_mix_oct15.py (mix left_out_share), or with mix=False the source's own
    central rows (its frozen positive control); general rows from the source."""
    rows = read_rows(SOURCE / 'derived/accrual_ratios.csv')
    if mix:
        mixed = [r for r in read_rows(MIX) if r['mix'] == 'left_out_share' and r['arm'] == 'central']
    else:
        mixed = [r for r in rows if r['arm'] == 'central']
    controls = read_rows(SOURCE / 'derived/reproduced_ratios.csv')
    union = one(controls, group='union', basis='row4', mortality='general')
    generations = {}
    for g in ('G1', 'G2', 'G3plus'):
        ref = one(rows, group=g, basis='row4', arm='general')
        own = one(mixed, group=g, basis='row4')
        generations[g] = {}
        for metric, tax, key in (('oasdi_per_tax_dollar_net', 'cps_oasdi_tax_bn', 'ss'),
                                 ('part_a_per_hi_tax_dollar', 'cps_hi_tax_bn', 'pa')):
            generations[g][key + '_per_tax'] = ((float(own[metric]) - float(ref[metric]))
                                               * float(ref[tax]) / float(union[tax]))
            generations[g][key + '_factor'] = float(own[metric]) / float(ref[metric]) - 1
    profiles = []
    for own in mixed:
        if own['basis'] != 'added_profile':
            continue
        ref = one(controls, group=own['group'], basis='added_profile',
                  age_mix=own['age_mix'], mortality='general')
        profiles.append({key: float(own[metric]) / float(ref[metric]) - 1
                         for key, metric in (('ss', 'oasdi_per_tax_dollar_net'),
                                             ('pa', 'part_a_per_hi_tax_dollar'))})
    if len(profiles) != 3:
        raise ValueError('[BLOCKED] mortality needs all three source added profiles')
    return generations, profiles


def amounts(dump, carriers=None):
    """Economic parent amounts, including signed completion accounting carriers."""
    result = {}
    for row in dump['lines']:
        if row['side'] == 'scalar':
            continue
        source = (carriers or {}).get(row['id'], {})
        if source and source.get('kind') != 'line':
            continue
        side = source.get('side', row['side'])
        side = 'receipts' if side in ('receipt', 'receipts') else 'spending'
        value = row['amount_bn'] * (1 if side == row['side'] else -1)
        key = side + '|' + source.get('parent_line', row['id'])
        result[key] = result.get(key, 0.) + value
    return result


def source_change(full, union, meta, end, include_coverage=False, mix=True):
    """Source nativity coefficients on current taxes and current overlay stocks.

    Source generation payer proportions are held fixed, exactly as the producer
    does. Missing overlay pension-dollar profile splits are bounded using the
    source's three measured profiles, also for completed reporters/children.
    Coverage uses its exported generation pension parts rather than headcount.
    """
    gen, profiles = coefficients(mix)
    carriers = meta.get('union_completion', {}).get('carriers', {})
    cash = amounts(union['cash'][end])
    se = cash['receipts|self_employment_oasdi_hi']
    share = meta['pension_accrual']['se_oasdi_share']
    part_a = meta['pension_accrual']['part_a_share']
    otax = cash['receipts|employee_oasdi'] + cash['receipts|employer_oasdi'] + share * se
    hitax = cash['receipts|employee_hi'] + cash['receipts|employer_hi'] + (1-share) * se
    identified = sum(c['ss_per_tax'] * otax + c['pa_per_tax'] * hitax for c in gen.values())
    extra = {}
    for basis in ('accrual', 'cash'):
        fm = amounts(full[basis][end], carriers)
        um = amounts(union[basis][end], carriers)
        extra[basis] = {k: fm.get(k, 0.) - um.get(k, 0.) for k in fm.keys() | um.keys()}
    ss = extra['accrual']['spending|social_security']
    pa = extra['accrual']['spending|medicare'] - (1-part_a) * extra['cash']['spending|medicare']
    if min(ss, pa) < -1e-9:
        raise ValueError('[BLOCKED] negative overlay accrued pension stocks')
    coverage = 0.
    if include_coverage and meta.get('coverage'):
        path = HERE.parent / meta['coverage']['file']
        raw = json.loads(path.read_text())
        if raw.get('key') != 'oct15':
            raise ValueError('[BLOCKED] live mortality needs oct15 coverage decomposition')
        pensions = {}
        for basis in ('set', 'cash'):
            rows = raw['sets'][basis]['ends'][end]['decomposition']['line_parts']
            pensions[basis] = {}
            for r in rows:
                if r.get('economic_class') != 'fiscal_line' or r.get('source_side') != 'spending':
                    continue
                key = r['generation'], r['source_line']
                pensions[basis][key] = pensions[basis].get(key, 0.) + r['coverage_bn']
            expected = {(g, line) for g in gen for line in ('social_security', 'medicare')}
            if not expected <= pensions[basis].keys():
                raise ValueError('[BLOCKED] coverage lacks generation pension-stock decomposition')
        for g, c in gen.items():
            css = pensions['set'].get((g, 'social_security'), 0.)
            cpa = pensions['set'].get((g, 'medicare'), 0.) - (1-part_a) * pensions['cash'].get((g, 'medicare'), 0.)
            coverage += css * c['ss_factor'] + cpa * c['pa_factor']
    bounds = {bound: identified + ss * choose(p['ss'] for p in profiles)
              + pa * choose(p['pa'] for p in profiles) + coverage
              for bound, choose in (('low', min), ('high', max))}
    if not all(math.isfinite(v) for v in bounds.values()):
        raise ValueError('[BLOCKED] nonfinite lineage mortality substitution')
    return bounds


def convention(arm):
    return MIXED if arm in OWN_ARMS else GENERAL


def stated(label):
    """Round 3 (C3 fix 3b): a stated comparison claim pairs both sides on one mortality convention."""
    if label not in (MIXED, OWN, GENERAL):
        raise ValueError(f'[BLOCKED] unknown mortality convention {label!r}')
    return label != MIXED


def validate_pair(lineage, comparator, label):
    """The actual producer calls this before emitting any comparison."""
    if lineage['case'] != comparator['case']:
        raise ValueError('[BLOCKED] comparison crosses case keys')
    lm, cm = lineage['group_mortality'], comparator['group_mortality']
    required = MIXED if lm == 'whole-population' and cm == 'own-group' else OWN if lm == cm == 'own-group' else GENERAL
    if label != required:
        raise ValueError(f'[BLOCKED] mortality pairing requires explicit label {required!r}')


def tag(row):
    arm, group = row['arm'], row.get('group', '')
    return dict(row, case='oct15', mortality_convention=convention(arm), mortality_bound='none',
                mortality_delta_bn=0.,
                group_mortality='own-group' if arm in OWN_ARMS and group and not group.startswith('mexican_')
                else 'whole-population')

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
MIXED = 'mixed mortality conventions'
OWN = 'own-group mortality'
GENERAL = 'whole-population mortality'
OWN_ARMS = {'combined_before_round2', 'combined_bracket_only', 'combined_payroll_only',
            'combined_bracket_payroll_joint', 'mortality_group', 'mortality_symmetric_frame_status',
            'combined_rules_only', 'combined_zero_production'}


def read_rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def one(rows, **keys):
    selected = [r for r in rows if all(r.get(k) == v for k, v in keys.items())]
    if len(selected) != 1:
        raise ValueError(f'[BLOCKED] ambiguous mortality source row {keys}')
    return selected[0]


def coefficients():
    rows = read_rows(SOURCE / 'derived/accrual_ratios.csv')
    controls = read_rows(SOURCE / 'derived/reproduced_ratios.csv')
    union = one(controls, group='union', basis='row4', mortality='general')
    generations = {}
    for g in ('G1', 'G2', 'G3plus'):
        ref = one(rows, group=g, basis='row4', arm='general')
        own = one(rows, group=g, basis='row4', arm='central')
        generations[g] = {}
        for metric, tax, key in (('oasdi_per_tax_dollar_net', 'cps_oasdi_tax_bn', 'ss'),
                                 ('part_a_per_hi_tax_dollar', 'cps_hi_tax_bn', 'pa')):
            generations[g][key + '_per_tax'] = ((float(own[metric]) - float(ref[metric]))
                                               * float(ref[tax]) / float(union[tax]))
            generations[g][key + '_factor'] = float(own[metric]) / float(ref[metric]) - 1
    profiles = []
    for own in rows:
        if own['basis'] != 'added_profile' or own['arm'] != 'central':
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


def source_change(full, union, meta, end, include_coverage=False):
    """Source nativity coefficients on current taxes and current overlay stocks.

    Source generation payer proportions are held fixed, exactly as the producer
    does. Missing overlay pension-dollar profile splits are bounded using the
    source's three measured profiles, also for completed reporters/children.
    Coverage uses its exported generation pension parts rather than headcount.
    """
    gen, profiles = coefficients()
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

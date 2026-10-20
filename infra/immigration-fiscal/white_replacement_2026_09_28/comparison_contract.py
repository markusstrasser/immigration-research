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
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

MIXED_SOURCE = Path(__file__).resolve().parent.parent / 'mixed_unit_comparators_2026_10_15/derived'
MIXED_PINS = {
    'white_summary.json': '121b787f04637b43d698555fade2b115686f15fa7f30d4d5167ac5c3d4477081',
    'white_replicates.csv': '3da68f4be49514508c0a601cff1eadb31a0e405c72b940c83c6bd2e4062720b0',
    'black_summary.json': '2cf7a859a12a3775a385440347ebf7851630302b56b95dbbd00847b26d7c2409',
    'black_replicates.csv': 'b78f9a6e60e5bf9bb72842c58e8385b415db5c27c0006a1ef932a81c7723c03d',
    'white_children_summary.json': '9b06285b012453a8c7dd8720f4f67cde990795fce2de5c65c67481635eb228eb',
    'white_children_replicates.csv': '852aaec100e3c589057b3de955f00641dc82f7cc3fbe014497d798f6005fcfd4',
    'black_children_summary.json': 'faedcc82ff1aaed64adac97783a6d4479b8ab339b1a5658e259e57c16ad5ff29',
    'black_children_replicates.csv': '71c6a4e7c71f930126a339fc438c960362a996415309374b28f3a0b60c9bd8ad',
    'white_children_round3_summary.json': 'ded538a18d275a25a9beec85b2387f916346bddb2deb47c83e85c0e59abb141c',
    'white_children_round3_replicates.csv': 'e9d91836cb5be7201fa4a330d00d6947847f4e2cbf154e67d0e7d29fe820b1c7',
    'black_children_round3_summary.json': '14f94cef3bbe8a2e7ee838220da68ca8487cf148a656c58043531f582be5519a',
    'black_children_round3_replicates.csv': '0a8e64a32bb788ea8dd351450c4c6514ac4187618d21460ba6304670e1aadf30',
    'white_children_half_summary.json': 'c4aa4175ef98f1bb8a6a3806f5e8330bf00e558600e25bd39b85e2f1feaf9a42',
    'white_children_half_replicates.csv': 'ee12537d17ae6ee404fdfecd4e3bd038d2dda000a7f3794e6b3cc0cba94f6de9',
    'black_children_half_summary.json': '046c6dddd22559588754931a8495296ccf8f38db56366609c2b6eccc79df0ae5',
    'black_children_half_replicates.csv': '663875d6161b31f07e964832c885873d61feda927075922bc0ecec946153de8d',
    'gaps.csv': '7ab68989d5b9e0f30e276c86fb2f83dc1f95c5703908deb8868822abd820c9d9',
}
LINEAGE_REPLICATES = MIXED_SOURCE.parent.parent / 'mixed_unit_removal_2026_10_14/derived/round2_replicates.csv'
LINEAGE_REPLICATES_PIN = '008472495fd84072c67b9cd5091001b5533aa7c5d0769b51f324b3603c1d0e40'
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
RULES = {'current': '', 'children': '_children', 'children_round3': '_children_round3', 'children_half': '_children_half'}
CURRENT_RULE_ONLY = {'A2_us_born_nh_white': REGISTRY['A2_us_born_nh_white'][1],
                     'all_residents_slice': REGISTRY['all_residents_slice'][1]}


def reading_scope(group):
    """Publication eligibility is independent of the presence of a numeric cost."""
    registered(group)
    reason = CURRENT_RULE_ONLY.get(group, '')
    return dict(comparison_reading='current-rule reading' if reason else 'registered comparison reading',
                central_eligible=not bool(reason), current_rule_reason=reason)


def require_central_reading(group):
    scope = reading_scope(group)
    if not scope['central_eligible']:
        raise SystemExit(f'[BLOCKED] {group} is a current-rule reading, not a central: {scope["current_rule_reason"]}')
    return scope


def registered(group):
    if group in REGISTRY:
        return REGISTRY[group]
    for prefix, entry in PREFIXES:
        if group.startswith(prefix):
            return entry
    raise SystemExit(f'[BLOCKED] comparator group {group!r} is not registered for item 11 (comparison_contract.REGISTRY)')


def load_mixed_unit(source=MIXED_SOURCE, case='oct15'):
    """Frozen own-mask terms. Never called from the comparator evaluator/setup."""
    contents = {}
    for name, expected in MIXED_PINS.items():
        path = source / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'[BLOCKED] comparator item11 sha256 mismatch: {path}')
        contents[name] = path.read_text()
    gaps = list(csv.DictReader(contents['gaps.csv'].splitlines()))
    if hashlib.sha256(LINEAGE_REPLICATES.read_bytes()).hexdigest() != LINEAGE_REPLICATES_PIN:
        raise SystemExit('[BLOCKED] lineage item11 replicate sha256 mismatch')
    groups = [name.removesuffix('_summary.json') for name in contents if name.endswith('_summary.json')]
    return {'comparison_case': case, 'summaries': {group: json.loads(contents[f'{group}_summary.json']) for group in groups},
            'gaps': gaps, 'sha256': dict(MIXED_PINS),
            'replicates': {group: pd.read_csv(StringIO(contents[f'{group}_replicates.csv']))
                           for group in groups if f'{group}_replicates.csv' in contents},
            'lineage_replicates': pd.read_csv(LINEAGE_REPLICATES)}


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
    if factors is not None and any(kind not in factors or not math.isfinite(factors[kind]) or factors[kind] < 0
                                   for kind in ('tax', 'spm', 'household')):
        raise SystemExit('[BLOCKED] item11 reweighting factors must be finite nonnegative tax, spm and household ratios')
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


def sdr(vector):
    vector = np.asarray(vector, float)
    if vector.shape != (161,) or not np.isfinite(vector).all():
        raise SystemExit('[BLOCKED] item11 SDR needs the full estimate and 160 finite signed replicates')
    return float(np.sqrt(4 / 160 * np.square(vector[1:] - vector[0]).sum()))


def item11_replicates(source, mask, method, end, factors=None):
    """Use the selected endpoint's parts, preserving signs and cross-part covariance."""
    row, _ = entry(source, mask, method, end)
    table = source.get('replicates', {}).get(mask)
    if table is None:
        return None
    cells = table[(table.method == method) & (table.end == end)]
    def vector(component):
        found = cells[cells.component == component]
        if len(found) != 1:
            raise SystemExit(f'[BLOCKED] item11 replicate component not unique: {mask}/{component}')
        values = found[[f'r{i}' for i in range(161)]].iloc[0].to_numpy(float)
        sdr(values)
        return values
    if factors is None:
        result = vector(f'bounded_{end}')
    else:
        selected = dict(zip(('Medicaid', 'ACA', 'SNAP'), row['arm'].split('|')))
        result = sum((vector(selected.get(part, part)) * factors[PART_UNIT.get(part, 'spm')]
                      for part in row['parts']), np.zeros(161))
    expected = sum(split(row['parts'], factors=factors).values())
    if abs(result[0] - expected) > 1e-9:
        raise SystemExit('[BLOCKED] item11 replicate full estimate does not match reweighted parts (1e-9bn)')
    return result


def lineage_item11_replicates(source, basis, end):
    """Current-rule source vector; children-rule additions require an explicit expanded vector."""
    table = source.get('lineage_replicates')
    if table is None:
        return None
    method = 'set' if basis == 'accrual' else basis
    rows = table[(table.method == method) & (table.end == end) & (table.component == f'bounded_{end}')]
    if rows.empty:
        raise SystemExit('[BLOCKED] lineage item11 replicate endpoint missing')
    vector = rows[[f'r{i}' for i in range(161)]].sum().to_numpy(float)
    sdr(vector)
    return vector


def uncertainty(source, mask, basis, end, scale, factors=None, lineage_replicates=None, rule='current'):
    vector = item11_replicates(source, mask, 'set' if basis == 'accrual' else basis, end, factors)
    if vector is None:
        return dict(comparator_se_bn=None, paired_se_bn=None,
                    se_scope='not computed: authenticated comparator replicate parts unavailable')
    vector = vector * scale
    if source.get('comparison_case') == 'oct16':
        return dict(comparator_se_bn=sdr(vector), paired_se_bn=None,
                    se_scope='own-mask comparator SDR at v9 counts; calibrated v9 lineage paired replicate vector unmeasured')
    if lineage_replicates is None and rule == 'current':
        lineage_replicates = lineage_item11_replicates(source, basis, end)
    paired = None if lineage_replicates is None else sdr(np.asarray(lineage_replicates, float) - vector)
    return dict(comparator_se_bn=sdr(vector), paired_se_bn=paired,
                se_scope=('signed paired item11 SDR; fixed counts and reweighting factors'
                          if paired is not None else
                          'comparator-only signed item11 SDR; expanded lineage replicate vector unavailable'))


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
        se = uncertainty(source, mask, basis, end, population / own, factors)
        return checked(dict(bn=amount, **se, own_count=own, status=status,
                            spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                            scope=f'reweighted from A1: {REWEIGHT_RULE}; ' + se['se_scope'] + '; ' + MIXED_FRAME))
    frame = 'own_count' if abs(population - own) < 1e-6 else 'lineage_count'
    paired = next(r for r in gaps if r['population_basis'] == frame)
    expected_population = own if frame == 'own_count' else float(paired['lineage_count'])
    if source.get('comparison_case') == 'oct16':
        # v9 prices several lineage readings (44.19-45.08M people) against a source paired at v8's one lineage
        # count, so the v8 population-equality stop cannot hold. Keep everything else at full strength: the
        # frozen source's own standardization at its paired count (1e-9), the linear amount at this count, and
        # its spending/receipt parts against that independently computed amount (checked(), 1e-9).
        if not math.isfinite(population) or population <= 0:
            raise SystemExit('[BLOCKED] comparator item11 population must be a positive finite count')
        source_count = own if frame == 'own_count' else float(paired['lineage_count'])
        if (not math.isfinite(row['bn'] * source_count / own)
                or abs(row['bn'] * source_count / own - float(paired['comparator_adjustment_bn'])) > 1e-9):
            raise SystemExit('[BLOCKED] comparator item11 own-count standardization mismatch')
        amount = row['bn'] * population / own
        parts = split(row['parts'], population / own)
        if not math.isfinite(amount) or abs(parts['spending'] + parts['receipts'] - amount) > 1e-9:
            raise SystemExit('[BLOCKED] comparator item11 parts do not add to the standardized term (1e-9bn)')
        se = uncertainty(source, mask, basis, end, population / own)
        # The published amount stays the parts' sum (its bytes since the oct16 migration); the gate above ties it
        # to the independently standardized term.
        return checked(dict(bn=parts['spending']+parts['receipts'], **se,
                            own_count=own,status=status,spending_bn=parts['spending'],receipt_bn=parts['receipts'],
                            scope='measured own membership; explicit v9 linear count standardization; paired SE unavailable; '+MIXED_FRAME))
    if abs(population - expected_population) > 1e-6:
        raise SystemExit('[BLOCKED] comparator item11 population differs from paired source')
    amount = row['bn'] * population / own
    if not math.isfinite(amount) or abs(amount - float(paired['comparator_adjustment_bn'])) > 1e-9:
        raise SystemExit('[BLOCKED] comparator item11 own-count standardization mismatch')
    parts = split(row['parts'], population / own)
    return checked(dict(bn=amount, paired_se_bn=float(paired['item11_paired_se_bn']),
                        comparator_se_bn=float(paired['comparator_adjustment_se_bn']),
                        se_scope='signed paired item11 SDR; fixed population standardization',
                        own_count=own, status=status, spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                        scope='measured own membership; linear population standardization; ' + MIXED_FRAME))


def true_count_removal(source, group, basis, end, population, true_own, rule, reweight=None,
                       observed_own=None, lineage_replicates=None):
    """Item 11 under a membership rule ('current', or 'children': members' biological minor children depart and count
    as members) for `population` people, from the term measured on the group's observed mask.

    Coverage's missed people add no mixed-unit term [ASSUMPTION, as their custody and arrests are held]: the per-person
    amount is the measured term over the group's true count. Reweighted scenarios must supply their observed own
    count and factors computed on the same expanded mask. Counts and factors are conditioned in SDR uncertainty.
    Children-rule pairing requires the expanded lineage's signed replicate vector; comparator-only SE is separate."""
    status, mask = registered(group)
    if status not in ('measured', 'reweighted'):
        raise SystemExit(f'[BLOCKED] true-count item 11 is measured for A1 and Black only, not {group}')
    if rule not in RULES or not math.isfinite(population) or population <= 0:
        raise SystemExit('[BLOCKED] true-count item11 needs a known membership rule and positive finite population')
    method = 'set' if basis == 'accrual' else basis
    row, gaps = entry(source, mask + RULES[rule], method, end)
    own = float(gaps[0]['comparator_own_count'])
    if not (math.isfinite(true_own) and true_own > 0):
        raise SystemExit('[BLOCKED] true-count item 11 needs a positive true own count')
    scale = population / true_own
    factors = None
    if status == 'reweighted':
        if reweight is None or group not in reweight:
            raise SystemExit(f'[BLOCKED] {group} item 11 needs its record-level reweighting factors')
        if observed_own is None or not math.isfinite(observed_own) or observed_own <= 0:
            raise SystemExit('[BLOCKED] reweighted true-count item11 needs its positive observed own count')
        factors = reweight[group]
        scale *= observed_own / own
    parts = split(row['parts'], scale, factors)
    se = uncertainty(source, mask + RULES[rule], basis, end, scale, factors,
                     lineage_replicates=lineage_replicates, rule=rule)
    return checked(dict(bn=parts['spending'] + parts['receipts'], own_count=float(observed_own or own),
                        true_own_count=true_own, status=status, rule=rule, **se,
                        spending_bn=parts['spending'], receipt_bn=parts['receipts'],
                        scope=f'{rule} rule; {status} term over the true count; ' + se['se_scope'] + '; ' + MIXED_FRAME))


def reweight_ratios(d, civ, weights, membership_rule='current', membership_mask=None, lineage_mask=None):
    """Per part kind, a reweighted scenario's share of weight on A1 members in mixed units over A1's share.

    d: the rough frame (PH_SEQ, TAX_ID, SPM_ID); civ: civilians; weights: {'A1': cw, name: cw}, each named scenario a
    reweighting of A1's members (no weight outside them). Under children, A1 weights already include the authoritative
    expanded mask, after lineage precedence. membership_mask preserves departing zero-weight records; lineage_mask
    gates disjointness with the completed lineage including added children. No raw A1 mask is substituted here.
    A unit is mixed when it holds a civilian who is not a member."""
    if membership_rule not in RULES:
        raise SystemExit('[BLOCKED] unknown item11 reweighting membership rule')
    base = np.asarray(weights['A1'], float)
    member = base > 0 if membership_mask is None else np.asarray(membership_mask, bool)
    if base.shape != (len(d),) or member.shape != base.shape or not np.isfinite(base).all() or (base < 0).any():
        raise SystemExit('[BLOCKED] A1 reweighting weights/membership are invalid')
    if (base[~member] != 0).any() or not base.sum() > 0:
        raise SystemExit('[BLOCKED] A1 reweighting weights extend outside its membership or have no mass')
    if lineage_mask is not None and (member & np.asarray(lineage_mask, bool)).any():
        raise SystemExit('[BLOCKED] item11 comparator membership overlaps the precedence lineage')
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
        if cw.shape != base.shape or not np.isfinite(cw).all() or (cw < 0).any():
            raise SystemExit(f'[BLOCKED] {name} reweighting weights are invalid')
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
    source = load_mixed_unit(case='oct16')
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

"""P7 one-change-at-a-time comparator audit; frozen case and archive outputs read-only.

Run production_state_oct14.cjs, accrual_white.py --mortality and the Black lane's
accrual_black.py --mortality first. This route writes new symmetric_* tables in
the two comparator lanes. Legacy rough tables remain positive-control evidence.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import csv
from functools import lru_cache
import gzip
import hashlib
import io
import json
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import numpy as np
import pandas as pd
import rekey_sept29 as W
from memory_budget import require_within_budget
from production_comparators_oct14 import Production, sampling_se
from status_keys_oct14 import build as status_build, engine_accrual_rates
from status_keys_oct14 import LINE_KEYS
import mortality_conventions as MC
import comparison_contract as CC
from mortality_comparators import read_verified_ratio_table, select_verified_ratio, require_ratio_snapshot_fresh

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BLACK = W.BLACK_LANE
MEMBERS = HERE / 'derived/members_coverage_oct16.json'
LINEAGE_ROUND2 = W.FISCAL / 'mixed_unit_removal_2026_10_14/derived/round2_summary.json'
DERIVED, CENTRAL = MC.DERIVED, MC.CENTRAL       # round 3's derived arms and the central reading
DERIVED_GROUPS = ('mexican_origin_engine', 'mexican_origin_rough', 'A1_third_plus_nh_white', 'nh_black_rough',
                  'A3_third_plus_nh_white_at_union_ages', 'A4_third_plus_nh_white_stationary')
_SCHOOL_TRANSFER_OPTION = os.environ.get('R4_LINEAGE_SCHOOL_BRIDGE', '0')
if _SCHOOL_TRANSFER_OPTION not in ('0', '1'):
    raise SystemExit('[BLOCKED] R4_LINEAGE_SCHOOL_BRIDGE must be 0 or 1')
SCHOOL_BRIDGE_TRANSFER = _SCHOOL_TRANSFER_OPTION == '1'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check_pins(pin=False):
    paths = [W.R.ZIP, HERE / 'inputs/comparator_baseline_oct14.json',
             HERE / 'derived/rekey_summary_oct14.csv',
             HERE / 'derived/production_state_oct16.json',
             W.FISCAL / 'main_case_candidate_2026_09_28/derived/production_row4.json',
             W.FISCAL / 'matched_benefits_2026_09_19/model.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/common.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_status.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_onbooks_lane.py']
    paths += [W.FISCAL / 'main_case_2026_10_16/derived' / n for n in ('corrections.json', 'corrections_cash.json', 'summary.json')]
    paths += [lane / 'derived/accrual_ratios_mortality_oct16.csv' for lane in (HERE, BLACK)]
    paths += [MC.SOURCE / 'derived' / n for n in ('accrual_ratios.csv', 'reproduced_ratios.csv', 'case_changes.csv', 'comparisons.csv')]
    paths += [HERE / 'mortality_conventions.py',
              W.FISCAL / 'coverage_bound_2026_10_14/derived/coverage_bound_oct16.json',
              W.FISCAL / 'job_capital_taxes_2026_10_14/derived/item.json']
    # Round 3 (C3): the mortality mix, the school key, the coverage and children terms, the lineage's children shift.
    paths += [MC.MIX, HERE / 'derived/school_key_oct16.json', MEMBERS, LINEAGE_ROUND2,
              HERE / 'derived/district_prices_oct16.json', HERE / 'r4_adjustments.py']
    paths += [CC.MIXED_SOURCE / n for n in ('lineage_children_delta_summary.json',
        'lineage_children_total_replicates.csv', 'lineage_half_white_total_replicates.csv',
        'lineage_half_black_total_replicates.csv')]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    target = HERE / 'inputs/pins.json'
    data = json.loads(target.read_text())
    if pin:
        data['symmetric_inputs_oct16'] = hashes
        target.write_text(json.dumps(data, indent=2) + '\n')
    if data.get('symmetric_inputs_oct16') != hashes:
        raise SystemExit('[BLOCKED] comparator input pin mismatch; inspect changed source before repinning')
    return hashes


def write(lane, name, rows):
    # Rows of the round-3 derived arms carry a few extra columns; every row takes the union schema.
    fields = list(dict.fromkeys(key for row in rows for key in row))
    if name.endswith('.gz'):
        # Deterministic gzip (no file name, mtime 0) so a rerun rewrites the same bytes. Used for the
        # program-level table: 243,105 rows, 51.5 MB as plain CSV on oct15 and oct16, over the 50 MB
        # limit for tracked files (rerun_lane.py LARGE).
        text = io.StringIO()
        writer = csv.DictWriter(text, fieldnames=fields, restval='', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        with (lane / 'derived' / name).open('wb') as raw, \
                gzip.GzipFile(filename='', mode='wb', fileobj=raw, compresslevel=9, mtime=0) as stream:
            stream.write(text.getvalue().encode('utf-8'))
        return
    with (lane / 'derived' / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, restval='', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


@contextlib.contextmanager
def school_key(rough, groups):
    """Yield the arm's scenarios: round 3's school key (the default), or the rough key on persons aged 5-17 for the
    diagnostic arm that isolates C3 fix 4; the frame's key totals and the union scenario follow, then are restored."""
    if not rough:
        yield groups
        return
    saved, union = W.R.K['k12'], W.UNION_SC
    W.R.K['k12'] = W.K12_ROUGH
    W.R.KTOT['k12'] = float((W.R.w * W.R.K['k12']).sum())
    W.UNION_SC = W.R.scenario('mex')
    try:
        yield W.scenarios()
    finally:
        W.R.K['k12'] = saved
        W.R.KTOT['k12'] = float((W.R.w * saved).sum())
        W.UNION_SC = union


def coverage_label(name, spec):
    if name.startswith('mexican_'):
        return "lineage: the case's coverage (item 12)"
    return 'none' if spec is None else 'own group, 2020 PES central (members_coverage_oct15.py)'


def members_terms():
    """members_coverage_oct15.py's runs by (scenario, rule, coverage, mortality, basis, end), and its counts."""
    data = json.loads(MEMBERS.read_text())
    if data.get('case') != 'oct16' or data.get('arm') != 'combined_rules_only':
        raise SystemExit('[BLOCKED] members and coverage terms are not on oct16 combined rules')
    runs = {}
    for r in data['runs']:
        key = r['scenario'], r['rule'], r['coverage'], r['mortality'], r['basis'], r['end']
        if key in runs:
            raise SystemExit(f'[BLOCKED] duplicate members/coverage run {key}')
        runs[key] = r
    return runs, data['counts']


def lineage_children_shift():
    """Expanded-minus-current full survivor solve, retaining source D/credit closure once.

    Federal, state, refunds, health, SNAP and M5 are solved on the same departure
    roster. The signed 161-vector delta retains covariance; no zero state fallback.
    """
    data = json.loads((CC.MIXED_SOURCE / 'lineage_children_delta_summary.json').read_text())
    out = {}
    for method in ('set', 'cash'):
        for end in W.ENDS:
            rows = [r for r in data['results'] if (r['method'], r['end'], r['reading']) == (method, end, f'bounded_{end}')]
            if len(rows) != 1:
                raise SystemExit('[BLOCKED] expanded lineage survivor endpoint not unique')
            row = rows[0]
            out[method, end] = dict(row, total_bn=row['delta_bn'])
    W.stop_if_failed()
    return out


@lru_cache(maxsize=32)
def lineage_vector(basis, end, half=None, partial=False):
    if partial:
        table = pd.read_csv(CC.LINEAGE_REPLICATES)
        method = 'set' if basis == 'accrual' else basis
        cells = table[(table.method == method) & (table.end == end)]
        def vec(component):
            return cells[cells.component == component][[f'r{i}' for i in range(161)]].sum().to_numpy(float)
        m = json.loads(LINEAGE_ROUND2.read_text())['membership']
        ratio = m['outside_existing_addition_definition'] / m['latent_children_with_two_US_parents']
        return (vec(f'bounded_{end}') + vec('M6_all_biological_federal_tax_arm')
                - vec('M6_biological_children') + ratio * vec(f'bounded_{end}_membership_benefit_interaction'))
    filename = 'lineage_children_total_replicates.csv' if half is None else f'lineage_half_{half}_total_replicates.csv'
    table = pd.read_csv(CC.MIXED_SOURCE / filename)
    method = 'set' if basis == 'accrual' else 'cash'
    row = table[(table.method == method) & (table.end == end) & (table.component == f'bounded_{end}')]
    if len(row) != 1:
        raise SystemExit('[BLOCKED] expanded lineage replicate endpoint not unique')
    return row[[f'r{i}' for i in range(161)]].iloc[0].to_numpy(float)


def derived_rows(arm, spec, lookup, legacy, mixed, members, shift):
    """Rebuilt membership/coverage scenarios, with separately switched district and row8 terms.

    Half-overlap arms average whole-departure endpoints, including signed survivor
    vectors; their counts and direct costs carry the same half weight on both sides.
    """
    runs, counts = members
    out = []
    for basis in W.BASES:
        for end in W.ENDS:
            method = 'set' if basis == 'accrual' else 'cash'
            block = (runs['lineage_block', 'children', 'central', spec['mortality'], basis, end]
                     if spec['rule'] != 'current' else None)
            lv = lineage_vector(basis, end, spec.get('half'), spec.get('partial_lineage', False)) if block is not None else CC.lineage_item11_replicates(mixed, basis, end)
            delta = lv[0] - W.META['mixed_unit_removal']['by_end'][end]['total_bn'] if block is not None else 0.
            half = spec.get('half')
            overlap = runs[f'overlap_{half}', 'children', 'central', spec['mortality'], basis, end] if half else None
            block_adjustment = lambda r: ((r['district_bn'] if spec.get('district', True) else 0.)
                                         + (r['row8_bn'] if spec.get('row8', True) else 0.))
            lineage_population = lookup[spec['base'], basis, end, 'mexican_origin_rough']['population']
            if block is not None:
                lineage_population += block['population']
            if overlap is not None:
                lineage_population -= .5 * overlap['population']
            for name in DERIVED_GROUPS:
                if half and name.startswith(('A3_', 'A4_')):
                    continue
                base = lookup[spec['base'], basis, end, name]
                common = dict(membership_rule=spec['rule'], comparator_coverage=coverage_label(name, spec),
                              production_sampling_se_bn=None, se_scope='not estimated (round-3 derived arm)')
                if name.startswith('mexican_'):
                    row = dict(base, arm=arm, **common)
                    # The case's school_reprice is already carried by both engines.
                    # An education_services incidence residual is not an identified
                    # district price. Retain its whole transfer only as an explicit
                    # assumed-calibration branch, never the default measurement.
                    school_transfer = 0.
                    if SCHOOL_BRIDGE_TRANSFER and name == 'mexican_origin_rough' and spec.get('district', True):
                        school_transfer = sum(part['case_minus_rough_bn'] for part in
                            CC.bridge_parts(W.run29('eng', end, basis), W.run29(W.UNION_SC, end, basis),
                                            W.META['union_completion']['carriers'])
                            if part['side'] == 'spending' and part['line'] == 'education_services')
                    direct = 0. if block is None else block['cost_bn'] + block_adjustment(block)
                    if overlap is not None:
                        direct -= .5 * (overlap['cost_bn'] + block_adjustment(overlap))
                    add = direct + delta + school_transfer
                    if block is not None:
                        population = lineage_population
                        cost = base['cost_bn'] + add
                        def increment(field):
                            return block[field] - (0. if overlap is None else .5 * overlap[field])
                        spending_extra = block_adjustment(block) - (0. if overlap is None else .5 * block_adjustment(overlap))
                        row.update(population=population, cost_bn=cost, cost_one_sided_bn=base['cost_one_sided_bn'] + add,
                                   cost_without_item11_bn=base['cost_without_item11_bn'] + direct + school_transfer,
                                   mixed_unit_removal_bn=base['mixed_unit_removal_bn'] + delta,
                                   change_from_raw_bn=base['change_from_raw_bn'] + add,
                                   exceeds_5bn=abs(base['change_from_raw_bn'] + add) >= 5,
                                   cost_per_person=cost * 1e9 / population,
                                   allocated_balance_bn=base['allocated_balance_bn'] + increment('balance_bn') - spending_extra - school_transfer,
                                   responsive_budget_cost_bn=base['responsive_budget_cost_bn'] + increment('net_budget_bn') + spending_extra + delta + school_transfer,
                                   capital_resource_cost_bn=base['capital_resource_cost_bn'] + increment('capital_bn'),
                                   production_gain_bn=base['production_gain_bn'] + increment('production_gain_bn'),
                                   contribution_to_others_bn=-cost,
                                   lineage_children_block_bn=direct, lineage_children_block_population=population - base['population'],
                                   lineage_children_item11_bn=delta,
                                   lineage_children_item11_rule=lineage_children_shift.__doc__.replace('\n', ' '))
                    elif school_transfer:
                        for field in ('cost_bn', 'cost_one_sided_bn', 'cost_without_item11_bn', 'responsive_budget_cost_bn'):
                            row[field] += school_transfer
                        row['allocated_balance_bn'] -= school_transfer
                        row['cost_per_person'] = row['cost_bn'] * 1e9 / row['population']
                        row['contribution_to_others_bn'] = -row['cost_bn']
                    row['lineage_school_price_transfer_bn'] = school_transfer
                    row['lineage_item11_se_bn'] = None
                    row['change_from_base_arm_bn'] = add
                else:
                    CC.require_central_reading(name)
                    coverage = spec.get('coverage', 'central') if name == 'nh_black_rough' else 'central'
                    rule = spec['rule']
                    r = dict(runs[name, rule, coverage, spec['mortality'], basis, end])
                    count = counts[f'{name}/{rule}/{coverage}']
                    true_own, observed_own = count['true_own_scale'], count['observed_own_scale']
                    reweight = {name: count['item11_reweight']} if 'item11_reweight' in count else None
                    if half and name == ('A1_third_plus_nh_white' if half == 'white' else 'nh_black_rough'):
                        other = runs[name, 'children_round3', coverage, spec['mortality'], basis, end]
                        other_count = counts[f'{name}/children_round3/{coverage}']
                        half_own = .5 * (true_own + other_count['true_own_scale'])
                        for field in list(r):
                            if field.endswith('_bn') or field in ('pupil_count', 'school_level_unmeasured_bn'):
                                r[field] = .5 * (r[field] * true_own / r['population']
                                                   + other[field] * other_count['true_own_scale'] / other['population'])
                        r['population'] = half_own
                        observed_own = .5 * (observed_own + other_count['observed_own_scale'])
                        true_own, rule = half_own, 'children_half'
                    requested_population = lineage_population if name != 'nh_black_rough' else true_own
                    scale = requested_population / r['population']
                    for field in list(r):
                        if field.endswith('_bn') or field == 'pupil_count':
                            r[field] *= scale
                    r['population'] = requested_population
                    term = CC.true_count_removal(mixed, name, basis, end, r['population'], true_own, rule,
                        reweight=reweight, observed_own=observed_own, lineage_replicates=lv)
                    own_term = CC.true_count_removal(mixed, name, basis, end, true_own, true_own, rule,
                        reweight=reweight, observed_own=observed_own, lineage_replicates=lv)
                    extra = block_adjustment(r)
                    cost = r['cost_bn'] + extra + term['bn']
                    W.gate(f'{arm}/{basis}/{end}/{name}: rebuilt run cost identity (1e-9bn)',
                           abs(r['cost_bn'] - (r['spending_saved_bn'] - r['taxes_lost_bn'] + r['capital_bn']
                                               - r['production_gain_bn'])) < 1e-9)
                    change = r['cost_bn'] + extra - legacy[basis, end, name]['cost']
                    row = dict(arm=arm, basis=basis, end=end, group=name, allocation='personal', population=r['population'],
                               engine=CC.engine_for(name), mixed_unit_removal_bn=term['bn'], comparator_item11_bn=term['bn'],
                               item11_spending_bn=term['spending_bn'], item11_receipt_bn=term['receipt_bn'],
                               item11_paired_se_bn=term['paired_se_bn'], item11_comparator_se_bn=term['comparator_se_bn'],
                               own_count_item11_bn=own_term['bn'],
                               own_count_item11_comparator_se_bn=own_term['comparator_se_bn'],
                               own_count_item11_paired_se_bn=own_term['paired_se_bn'],
                                item11_se_scope=term['se_scope'], lineage_item11_se_bn=None, **common,
                               mixed_unit_asymmetry=term['scope'], framing=CC.MIXED_FRAME,
                               balance_scope='allocated member lines; survivor post-engine term excluded, as on lineage side',
                               cost_one_sided_bn=r['cost_bn'] + extra, cost_without_item11_bn=r['cost_bn'] + extra, cost_bn=cost,
                               change_from_raw_bn=change, exceeds_5bn=abs(change) >= 5,
                               cost_per_person=cost * 1e9 / r['population'], allocated_balance_bn=r['balance_bn'] - extra,
                               responsive_budget_cost_bn=r['net_budget_bn'] + extra + term['bn'], capital_resource_cost_bn=r['capital_bn'],
                               production_gain_bn=r['production_gain_bn'], contribution_to_others_bn=-cost,
                               true_own_count=true_own, observed_own_count=observed_own,
                               district_adjustment_bn=r['district_bn'] if spec.get('district', True) else 0.,
                               row8_adjustment_bn=r['row8_bn'] if spec.get('row8', True) else 0.,
                               school_level_unmeasured_bn=r['school_level_unmeasured_bn'],
                               item11_effective_rule=rule, item11_reweight_factors=json.dumps(reweight),
                               change_from_base_arm_bn=cost - base['cost_bn'])
                out.append(MC.tag(row))
    W.stop_if_failed()
    return out


def mortality_params(mortality='specific', basis='row4', payroll_basis='legacy', scenario_ages=True, ratio_tables=None):
    """Only comparator ratios change; union's recorded accrual stays the principal.

    Ratios are applied to account-frame payroll amounts. Pension helper frame
    counts never replace the comparator's own population denominator.
    """
    params = copy.deepcopy(W.ACC)
    if ratio_tables is None:
        ratio_tables = {lane: read_verified_ratio_table(lane) for lane in (HERE, BLACK)}
    for lane, group, key, specific in ((HERE, 'third_plus_nh_white', 'white', 'nh_white'),
                                        (BLACK, 'nh_black', 'black', 'nh_black')):
        mt = specific if mortality == 'specific' else 'general'
        def entry(scenario_name):
            by_end = {end: W.acc_entry(select_verified_ratio(ratio_tables[lane], group, mt, basis,
                        scenario_name=scenario_name, end=end if payroll_basis != 'legacy' else '',
                        payroll_basis=payroll_basis)) for end in W.ENDS}
            return {**by_end['low'], 'by_end': by_end}
        params[key] = entry('observed')
        if key == 'white' and scenario_ages:
            params[key]['by_scenario'] = {name: entry(name) for name in
                ('A1_third_plus_nh_white', 'A2_us_born_nh_white',
                 'A3_third_plus_nh_white_at_union_ages', 'A4_third_plus_nh_white_stationary')}
    return params


def status_params(status, coupled):
    """Keep the union's pension target fixed, or transport principal per-tax rates.

    Never apply the old R9 effective ratio to a newly corrected tax denominator.
    Comparator ratios stay their own study ratios, on their new tax amounts.
    """
    params = copy.deepcopy(W.ACC)
    for end in W.ENDS:
        p = dict(params['union']['by_end'][end])
        e = W.DUMP['cash'][end]
        amounts = {ln['id']: status.receipt_amount(W.UNION_SC, ln['id'], ln['national_bn'])
                   for ln in e['lines'] if ln['side'] == 'receipts'}
        se = amounts['self_employment_oasdi_hi']
        oasdi = amounts['employee_oasdi'] + amounts['employer_oasdi'] + W.SE_SHARE * se
        hi = amounts['employee_hi'] + amounts['employer_hi'] + (1 - W.SE_SHARE) * se
        if coupled:
            p.update(engine_accrual_rates(W, end))
        else:
            r = W.run29(W.UNION_SC, end, 'accrual')
            r_cash = W.run29(W.UNION_SC, end, 'cash')
            def amount(rows, lid):
                return next(x[3] for x in rows if x[0] == 'spending' and x[1] == lid)
            # Exclude the added people: their authoritative amounts travel in LIN.
            ss = amount(r[1], 'social_security') - W.LIN['accrual'][end]['lines']['spending|social_security']
            mc = amount(r[1], 'medicare') - W.LIN['accrual'][end]['lines']['spending|medicare']
            mc_cash = amount(r_cash[1], 'medicare') - W.LIN['cash'][end]['lines']['spending|medicare']
            p.update(net=ss / oasdi, part_a=(mc - (1 - W.PART_A_SHARE) * mc_cash) / hi)
        params['union']['by_end'][end] = p
    return params


def status_sampling(status, production, sc, end):
    """Receipt-shift SDR only, conditional on point flags, carriers and count.

    Does not claim full fiscal uncertainty or rerun IRS raking/status imputation.
    The principal fiscal point uses rounded MARSUPWT; official SDR columns are
    used for sampling with the same row-4 cell targets.
    """
    estimates = np.zeros(161)
    for start in range(0, 161, 16):
        cols = slice(start, min(start + 16, 161))
        wt = production.scenario_weights(sc, columns=cols)
        if start == 0:
            wt[:, 0] = sc['cps_w']
        for ln in W.DUMP['cash'][end]['lines']:
            if ln['side'] != 'receipts' or ln['id'] not in LINE_KEYS:
                continue
            key = LINE_KEYS[ln['id']]
            shares = {}
            for rule in ('raw', 'rules_only'):
                v = status.vectors[rule][key]
                den = v @ production.weights[:, cols]
                if start == 0:
                    den[0] = v @ W.R.w
                shares[rule] = (v @ wt) / den
            estimates[cols] += ln['national_bn'] * (shares['rules_only'] - shares['raw'])
    expected = sum(status.receipt_amount(sc, ln['id'], ln['national_bn'], 'rules_only')
                   - status.receipt_amount(sc, ln['id'], ln['national_bn'], 'raw')
                   for ln in W.DUMP['cash'][end]['lines'] if ln['side'] == 'receipts' and ln['id'] in LINE_KEYS)
    W.gate(f'{sc["name"]}/{end}: receipt SDR point reproduces status-only point (1e-9bn)', abs(estimates[0] - expected) < 1e-9)
    return dict(group=sc['name'], end=end, population=sc['population'], receipt_change_bn=estimates[0],
                receipt_sampling_se_bn=sampling_se(estimates),
                uncertainty_scope='receipt shift only; conditional fixed count, status flags, IRS/CBO carrier and age mix; no reimputation/reraking uncertainty')


def hispanic_arm(ratio_table=None):
    """Exact identified-union ratio swap plus a bounded added-profile extension.

    Added pension dollar splits by measured age profile are not exported by the
    frozen case. Do not invent them: bound the added accrued dollars by the min
    and max full-precision factors for its three profiles, stated as a proxy.
    """
    rows = (read_verified_ratio_table(HERE) if ratio_table is None else ratio_table).rows
    selected = rows[(rows.group == 'union') & (rows.basis == 'row4') & (rows.scenario == 'payable')]
    gen = selected[selected.mortality == 'general'].iloc[0]
    hisp = selected[selected.mortality == 'hispanic'].iloc[0]
    profiles = rows[rows.basis == 'added_profile']
    ratios = {}
    for metric in ('oasdi_per_tax_dollar_net', 'part_a_per_hi_tax_dollar'):
        by = profiles.pivot(index=['group', 'age_mix'], columns='mortality', values=metric)
        if len(by) != 3 or by[['general', 'hispanic']].isna().any().any():
            raise SystemExit('[BLOCKED] incomplete added mortality profiles')
        ratios[metric] = (by.hispanic / by.general - 1).to_numpy()
    out = []
    for end in W.ENDS:
        cash = {x['side'] + '|' + x['id']: x['amount_bn'] for x in W.DUMP['cash'][end]['lines'] if x['side'] != 'scalar'}
        se = cash['receipts|self_employment_oasdi_hi']
        oasdi = cash['receipts|employee_oasdi'] + cash['receipts|employer_oasdi'] + W.SE_SHARE * se
        hi = cash['receipts|employee_hi'] + cash['receipts|employer_hi'] + (1 - W.SE_SHARE) * se
        ss_delta = (hisp.oasdi_per_tax_dollar_net - gen.oasdi_per_tax_dollar_net) * oasdi
        pa_delta = (hisp.part_a_per_hi_tax_dollar - gen.part_a_per_hi_tax_dollar) * hi
        a, c = W.LIN['accrual'][end]['lines'], W.LIN['cash'][end]['lines']
        added_ss = a['spending|social_security']
        added_pa = a['spending|medicare'] - (1 - W.PART_A_SHARE) * c['spending|medicare']
        if min(added_ss, added_pa) < 0:
            raise SystemExit('[BLOCKED] added pension profile bound requires nonnegative liabilities')
        low = added_ss * ratios['oasdi_per_tax_dollar_net'].min() + added_pa * ratios['part_a_per_hi_tax_dollar'].min()
        high = added_ss * ratios['oasdi_per_tax_dollar_net'].max() + added_pa * ratios['part_a_per_hi_tax_dollar'].max()
        principal = W.FULL['accrual'][end]['cost_bn']
        out.append(dict(end=end, allocation='personal', identified_union_population=W.R.TARGET,
                        lineage_population=W.LINEAGE['counts']['lineage_population'],
                        identified_ss_delta_bn=ss_delta, identified_part_a_delta_bn=pa_delta,
                        identified_delta_bn=ss_delta + pa_delta, added_profile_delta_low_bn=low,
                        added_profile_delta_high_bn=high, lineage_delta_low_bn=ss_delta + pa_delta + low,
                        lineage_delta_high_bn=ss_delta + pa_delta + high,
                        lineage_cost_low_bn=principal + ss_delta + pa_delta + low,
                        lineage_cost_high_bn=principal + ss_delta + pa_delta + high,
                        rule='2026 payable Hispanic pooled proxy; current benefit-tax receipt fixed; original added dollar split bounded over measured profiles; completion/coverage not independently repriced for mortality'))
    return out


def main(pin=False):
    started = time.perf_counter()
    W.use_case('oct16')
    hashes = check_pins(pin)
    mixed = CC.load_mixed_unit(case=W.CASE)
    baseline = json.loads((HERE / 'inputs/comparator_baseline_oct14.json').read_text())
    archive = pd.read_csv(HERE / 'derived/rekey_summary_oct14.csv').set_index(['basis', 'end', 'group'])
    for row in baseline:
        index = row['basis'], row['end'], row['group']
        for metric in ('cost', 'taxes_paid', 'spending_drawn', 'production_gain', 'capital'):
            W.gate(f'preserved v7 positive control {index}/{metric} (1e-12bn)', abs(archive.loc[index, metric] - row[metric]) < 1e-12)
    W.stop_if_failed()
    # The archived rows are read-only controls. Compute only the live case.
    W.setup()
    groups = W.scenarios()
    legacy = {(basis, end, name): W.run29(sc, end, basis)[0]
              for basis in W.BASES for end in W.ENDS for name, sc in groups.items()}
    production = Production(W)
    status = status_build(W)
    global_status = status_build(W, income_rake='global')
    closure = status.closure({ln['id']: ln['national_bn'] for ln in W.DUMP['cash']['low']['lines']
                             if ln['side'] == 'receipts' and ln['id'] in LINE_KEYS})
    W.gate('24 status line/rule national closures (1e-6bn)', len(closure) == 24 and all(abs(r['error_bn']) <= 1e-6 for r in closure))
    sampling = [status_sampling(status, production, groups[name], end)
                for name in ('mexican_origin_rough', 'nh_black_rough', 'A1_third_plus_nh_white') for end in W.ENDS]
    ratio_tables = {lane: read_verified_ratio_table(lane) for lane in (HERE, BLACK)}
    hispanic = hispanic_arm(ratio_tables[HERE])
    specific = mortality_params(ratio_tables=ratio_tables)
    general_row4 = mortality_params('general', ratio_tables=ratio_tables)
    symmetric_general = mortality_params('general', 'symmetric', ratio_tables=ratio_tables)
    symmetric_specific = mortality_params('specific', 'symmetric', ratio_tables=ratio_tables)
    fixed_benefits = status_params(status, coupled=False)
    coupled = status_params(status, coupled=True)
    combined = copy.deepcopy(symmetric_specific)
    combined['union'] = coupled['union']
    normalized_specific = mortality_params('specific', 'symmetric', payroll_basis='renormalized_status', ratio_tables=ratio_tables)
    normalized_specific['union'] = coupled['union']
    before_round2 = mortality_params('specific', 'symmetric', scenario_ages=False, ratio_tables=ratio_tables)
    before_round2['union'] = coupled['union']
    payroll_only = mortality_params('specific', 'symmetric', payroll_basis='renormalized_status', scenario_ages=False, ratio_tables=ratio_tables)
    payroll_only['union'] = coupled['union']
    # Round 3 (C3 fix 3b): the same combined rules with every group at whole-population mortality.
    normalized_general = mortality_params('general', 'symmetric', payroll_basis='renormalized_status', ratio_tables=ratio_tables)
    normalized_general['union'] = coupled['union']
    reweight = CC.scenario_reweight(W.R, groups)     # round 3 (C3 fix 5): A3 and A4 take A1's item 11, reweighted
    members = members_terms()
    shift = lineage_children_shift()
    # Four cells isolate post-status bracket conservation and pension denominators.
    # The final cell also preserves A3/A4's actual scenario age weights.
    arms = {
        'legacy_raw': ('legacy', None, W.ACC, 'rules_only'),
        'production_own': ('own', None, W.ACC, 'rules_only'),
        'production_zero': ('zero', None, W.ACC, 'rules_only'),
        'source_payroll_proxy': ('legacy', status, W.ACC, 'source_proxy'),
        'status_rules_fixed_union_benefits': ('legacy', status, fixed_benefits, 'rules_only'),
        'status_rules_coupled_accrual': ('legacy', status, coupled, 'rules_only'),
        'mortality_group': ('legacy', None, specific, 'rules_only'),
        'accrual_row4': ('legacy', None, general_row4, 'rules_only'),
        'pension_symmetric_frame_status': ('legacy', None, symmetric_general, 'rules_only'),
        'mortality_symmetric_frame_status': ('legacy', None, symmetric_specific, 'rules_only'),
        'combined_before_round2': ('own', global_status, before_round2, 'rules_only'),
        'combined_bracket_only': ('own', status, before_round2, 'rules_only'),
        'combined_payroll_only': ('own', global_status, payroll_only, 'rules_only'),
        'combined_bracket_payroll_joint': ('own', status, payroll_only, 'rules_only'),
        'combined_rules_only': ('own', status, normalized_specific, 'rules_only'),
        'combined_zero_production': ('zero', status, normalized_specific, 'rules_only'),
        'combined_rules_general': ('own', status, normalized_general, 'rules_only'),
        # round 3 (C3 fix 4) diagnostic: combined_rules_only on the rough school key (persons aged 5-17) for every group
        'combined_rules_rough_school': ('own', status, normalized_specific, 'rules_only'),
    }
    results, program_rows, bridges = [], [], []
    lookup = {}
    for arm, (policy, sk, accrual, rule) in arms.items():
        with W.patched(vars(W), ACC=accrual), school_key(arm == 'combined_rules_rough_school', groups) as arm_groups:
            for basis in W.BASES:
                for end in W.ENDS:
                    runs = {}
                    for name, sc in arm_groups.items():
                        run = W.run29(sc, end, basis, production=policy, production_model=production,
                                      status_keys=sk, status_rule=rule)
                        runs[name] = run
                        r, lines = run[:2]
                        W.gate(f'{arm}/{basis}/{end}/{name}: cost identity (1e-9bn)',
                               abs(r['cost'] - (r['spending_saved'] - r['taxes_lost'] + r['capital'] - r['production_gain'])) < 1e-9)
                        before = legacy[basis, end, name]
                        correction = CC.comparator_removal(mixed, name, basis, end, r['population'], reweight=reweight)
                        comparator_item11 = correction['bn']
                        # Publication only: run29 remains the unadjusted M5 calibration input.
                        r = dict(r, cost=r['cost'] + comparator_item11,
                                 net_budget=r['net_budget'] + comparator_item11,
                                 spending_saved=r['spending_saved'] + correction['spending_bn'],
                                 taxes_lost=r['taxes_lost'] - correction['receipt_bn'])
                        se = sampling_se(production.evaluate(sc, end)) if policy == 'own' and sc != 'eng' and sc['name'] != 'mex' else None
                        item11 = W.META['mixed_unit_removal']['by_end'][end]['total_bn'] if name.startswith('mexican_') else comparator_item11
                        row = dict(arm=arm, basis=basis, end=end, group=name, allocation='personal', population=r['population'],
                                   engine=CC.engine_for(name), mixed_unit_removal_bn=item11,
                                   comparator_item11_bn=comparator_item11,
                                   item11_spending_bn=correction['spending_bn'], item11_receipt_bn=correction['receipt_bn'],
                                   item11_paired_se_bn=correction['paired_se_bn'],
                                   item11_comparator_se_bn=correction.get('comparator_se_bn'),
                                   item11_se_scope=correction.get('se_scope'),
                                   membership_rule='current', comparator_coverage=coverage_label(name, None),
                                   mixed_unit_asymmetry=correction['scope'] if not name.startswith('mexican_') else 'lineage measured; A1/Black counterparts measured',
                                   framing=CC.MIXED_FRAME,
                                   balance_scope='allocated member lines; survivor post-engine term excluded, as on lineage side',
                                   cost_one_sided_bn=r['cost'] - comparator_item11,
                                   cost_without_item11_bn=r['cost'] - item11,
                                   cost_bn=r['cost'], change_from_raw_bn=r['cost'] - before['cost'] - comparator_item11,
                                   exceeds_5bn=abs(r['cost'] - before['cost'] - comparator_item11) >= 5,
                                   cost_per_person=r['cost'] * 1e9 / r['population'],
                                   allocated_balance_bn=r['balance'], responsive_budget_cost_bn=r['net_budget'],
                                   capital_resource_cost_bn=r['capital'], production_gain_bn=r['production_gain'],
                                   contribution_to_others_bn=-r['cost'], production_sampling_se_bn=se,
                                   se_scope='production only, conditional on fixed count and requested ages' if se is not None else 'not estimated')
                        row = MC.tag(row)
                        row.update(CC.reading_scope(name))
                        results.append(row)
                        lookup[arm, basis, end, name] = row
                        if name in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough', 'A1_third_plus_nh_white'):
                            if name in CC.MIXED_GROUPS:
                                program_rows.append(MC.tag(dict(arm=arm, basis=basis, end=end, group=name,
                                    side='post_engine', line='comparator_mixed_unit_removal',
                                    source_side='post_engine', source_line='mixed_unit_removal', carrier_kind='survivor_net',
                                    national_bn=0., amount_bn=comparator_item11, response=1.)))
                            for side, lid, national, amount, response in lines:
                                source = W.META.get('union_completion', {}).get('carriers', {}).get(lid, {})
                                program_rows.append(MC.tag(dict(arm=arm, basis=basis, end=end, group=name, side=side, line=lid,
                                                         source_side=source.get('side', side), source_line=source.get('parent_line', lid),
                                                         carrier_kind=source.get('kind', ''),
                                                         national_bn=national, amount_bn=amount, response=response)))
                    bridges.extend(dict(case='oct16', arm=arm, basis=basis, end=end,
                                        mortality_convention=MC.convention(arm), mortality_bound='none',
                                        case_engine='case', rough_engine='rough', **part)
                                   for part in CC.bridge_parts(runs['mexican_origin_engine'], runs['mexican_origin_rough'],
                                                              W.META['union_completion']['carriers']))
    # Round 3 (C3): the derived arms, after the evaluator. Their bridges are their base arms': the lineage's children
    # block and item 11 shift enter its case and rough rows alike.
    arm_names = list(arms) + list(DERIVED)
    for arm, spec in DERIVED.items():
        for row in derived_rows(arm, spec, lookup, legacy, mixed, members, shift):
            results.append(row)
            lookup[arm, row['basis'], row['end'], row['group']] = row
        for b in list(bridges):
            if b['arm'] != spec['base']:
                continue
            changed = dict(b, arm=arm, mortality_convention=MC.convention(arm))
            if SCHOOL_BRIDGE_TRANSFER and spec.get('district', True) and b['side'] == 'spending' and b['line'] == 'education_services':
                changed.update(rough_bn=b['case_bn'], case_minus_rough_bn=0.)
            bridges.append(changed)

    def item11_at(arm, name, basis, end, population):
        """Item 11 for `population` people under the arm's rule: observed own count, or the true own count."""
        spec = DERIVED.get(arm)
        if spec is None:
            term = CC.comparator_removal(mixed, name, basis, end, population, reweight=reweight)
            return dict(term, frame_own_count=term['own_count'])
        coverage = spec.get('coverage', 'central') if name == 'nh_black_rough' else 'central'
        count = members[1][f'{name}/{spec["rule"]}/{coverage}']
        true_own = count['true_own_scale']
        effective_rule = spec['rule']
        if spec.get('half') == ('white' if name.startswith('A1_') else 'black'):
            raw = members[1][f'{name}/children_round3/{coverage}']
            true_own = .5 * (true_own + raw['true_own_scale'])
            effective_rule = 'children_half'
        lv = lineage_vector(basis, end, spec.get('half'), spec.get('partial_lineage', False)) if spec['rule'] != 'current' else CC.lineage_item11_replicates(mixed, basis, end)
        term = CC.true_count_removal(mixed, name, basis, end, population, true_own, effective_rule,
                                     lineage_replicates=lv)
        return dict(term, frame_own_count=true_own)
    mortality_changes = {end: MC.source_change(W.FULL, W.DUMP, W.META, end, include_coverage=True)
                         for end in W.ENDS}
    for original in list(bridges):
        if original['arm'] in MC.OWN_ARMS:
            for bound in ('low', 'high'):
                bridges.append(dict(original, mortality_convention=MC.OWN, mortality_bound=bound))
    for arm in arm_names:
        if arm in MC.OWN_ARMS:
            for basis in W.BASES:
                for end in W.ENDS:
                    for bound in ('low', 'high'):
                        delta = mortality_changes[end][bound] if basis == 'accrual' else 0.
                        bridges.append(dict(case='oct16', arm=arm, basis=basis, end=end,
                            mortality_convention=MC.OWN, mortality_bound=bound, case_engine='case', rough_engine='rough',
                            side='mortality', line='lineage_mortality_substitution', case_bn=delta, rough_bn=delta,
                            case_minus_rough_bn=0.))
    # Keep the whole-population headline intact. Own-group readings are beside it,
    # with both missing-profile bounds rather than an invented midpoint.
    for original in list(results):
        if original['arm'] not in MC.OWN_ARMS:
            continue
        for bound in ('low', 'high'):
            row = dict(original, mortality_convention=MC.OWN, mortality_bound=bound,
                       group_mortality='own-group')
            delta = (mortality_changes[row['end']][bound]
                     if row['basis'] == 'accrual' and row['group'].startswith('mexican_') else 0.)
            row.update(cost_bn=row['cost_bn'] + delta,
                       cost_one_sided_bn=row['cost_one_sided_bn'] + delta,
                       mortality_delta_bn=delta,
                       change_from_raw_bn=row['change_from_raw_bn'] + delta,
                       cost_per_person=(row['cost_bn'] + delta) * 1e9 / row['population'],
                        cost_without_item11_bn=row['cost_without_item11_bn'] + delta,
                       allocated_balance_bn=row['allocated_balance_bn'] - delta,
                       responsive_budget_cost_bn=row['responsive_budget_cost_bn'] + delta,
                       contribution_to_others_bn=-(row['cost_bn'] + delta),
                       exceeds_5bn=abs(row['change_from_raw_bn'] + delta) >= 5)
            results.append(row)
            lookup[row['arm'], row['basis'], row['end'], row['group'], MC.OWN, bound] = row
    for original in list(program_rows):
        if original['arm'] in MC.OWN_ARMS:
            for bound in ('low', 'high'):
                program_rows.append(dict(original, mortality_convention=MC.OWN,
                                         mortality_bound=bound, group_mortality='own-group'))
    for r in results:
        if r['mortality_convention'] == MC.OWN and r['group'].startswith('mexican_'):
            program_rows.append(dict(case='oct16', mortality_convention=MC.OWN,
                mortality_bound=r['mortality_bound'], mortality_delta_bn=r['mortality_delta_bn'],
                group_mortality='own-group', arm=r['arm'], basis=r['basis'], end=r['end'], group=r['group'],
                side='spending', line='lineage_mortality_substitution', source_side='spending',
                source_line='social_security_and_medicare_part_a', carrier_kind='mortality_sensitivity',
                national_bn=0., amount_bn=r['mortality_delta_bn'], response=1.))
    comparisons, scaled, white_scaled = [], [], []
    readings = [(arm, MC.convention(arm), 'none') for arm in arm_names]
    readings += [(arm, MC.OWN, bound) for arm in arm_names if arm in MC.OWN_ARMS for bound in ('low', 'high')]
    for arm, mortality_convention, mortality_bound in readings:
        for basis in W.BASES:
            for end in W.ENDS:
                def get(name):
                    key = (arm, basis, end, name)
                    return lookup[key + (MC.OWN, mortality_bound)] if mortality_convention == MC.OWN else lookup[key]
                u, e, w, b = map(get, ('mexican_origin_rough', 'mexican_origin_engine', 'A1_third_plus_nh_white', 'nh_black_rough'))
                lineage_fields = dict(comparison_lineage_cost_bn=u['cost_bn'],
                    case_headline_cost_bn=legacy[basis, end, 'mexican_origin_engine']['cost'],
                    lineage_policy_delta_bn=(e['cost_bn'] - legacy[basis, end, 'mexican_origin_engine']['cost']
                        - e.get('lineage_children_block_bn', 0.) - e.get('lineage_children_item11_bn', 0.)
                        - e.get('mortality_delta_bn', 0.)),
                    lineage_children_block_bn=u.get('lineage_children_block_bn', 0.),
                    lineage_children_item11_bn=u.get('lineage_children_item11_bn', 0.),
                    lineage_school_price_transfer_bn=u.get('lineage_school_price_transfer_bn', 0.),
                    lineage_mortality_delta_bn=u.get('mortality_delta_bn', 0.),
                    case_minus_rough_bridge_bn=e['cost_bn'] - u['cost_bn'],
                    lineage_item11_se_bn=u.get('lineage_item11_se_bn'))
                W.gate(f'{arm}/{basis}/{end}: headline-to-comparison lineage decomposition (1e-9bn)',
                    abs(lineage_fields['case_headline_cost_bn'] - lineage_fields['case_minus_rough_bridge_bn']
                        + lineage_fields['lineage_children_block_bn'] + lineage_fields['lineage_children_item11_bn']
                        + lineage_fields['lineage_mortality_delta_bn'] + lineage_fields['lineage_policy_delta_bn'] - u['cost_bn']) < 1e-9)
                for row in results:
                    if all(row[k] == v for k, v in dict(arm=arm, basis=basis, end=end,
                            mortality_convention=mortality_convention, mortality_bound=mortality_bound).items()):
                        row.update(lineage_fields)
                for comparator in (w, b):
                    MC.validate_pair(u, comparator, mortality_convention)
                item11 = u['mixed_unit_removal_bn']
                white_own = item11_at(arm, 'A1_third_plus_nh_white', basis, end, w['population'])['frame_own_count']
                for frame, population in (('own_count', white_own), ('lineage_count', e['population'])):
                    f = population / w['population']
                    correction = item11_at(arm, 'A1_third_plus_nh_white', basis, end, population)
                    white_scaled.append(dict(case='oct16', arm=arm, basis=basis, end=end,
                        mortality_convention=mortality_convention, mortality_bound=mortality_bound,
                        population_basis=frame, population=population,
                        lineage_engine=u['engine'], comparator_engine=w['engine'], **lineage_fields,
                        comparator_cost_bn=w['cost_bn'] * f, lineage_cost_bn=u['cost_bn'],
                        lineage_population=u['population'],
                        lineage_minus_comparator_bn=u['cost_bn'] - w['cost_bn'] * f,
                        one_sided_gap_bn=u['cost_bn'] - (w['cost_bn'] - w['comparator_item11_bn']) * f,
                        comparator_item11_bn=correction['bn'], item11_paired_se_bn=correction['paired_se_bn'],
                        item11_comparator_se_bn=correction.get('comparator_se_bn'),
                        item11_se_scope=correction['se_scope'], membership_rule=w['membership_rule'],
                        framing=CC.MIXED_FRAME,
                        population_warning=('own count differs from the lineage count: not an as-many comparison'
                                            if frame == 'own_count' else ''),
                        rule='linear standardization of comparator per-person price; lineage held at live count; no new removal solve'))
                comparisons.append(dict(case='oct16', mortality_convention=mortality_convention, mortality_bound=mortality_bound,
                    arm=arm, basis=basis, end=end,
                    **CC.gap_fields(u, w, b, item11),
                    **lineage_fields,
                    membership_rule=w['membership_rule'], comparator_coverage=w['comparator_coverage'],
                    item11_se_scope=item11_at(arm, 'A1_third_plus_nh_white', basis, end, w['population'])['se_scope'],
                    stated_claim=MC.stated(mortality_convention),
                    central=arm == CENTRAL['arm'] and mortality_convention == CENTRAL['mortality_convention'],
                    full_row13_symmetric=False))
                factor = e['population'] / b['population']
                for frame, f in (('own_count', 1.), ('scaled_to_lineage', factor)):
                    correction = item11_at(arm, 'nh_black_rough', basis, end, b['population'] * f)
                    scaled.append(dict(case='oct16', mortality_convention=mortality_convention, mortality_bound=mortality_bound,
                        arm=arm, basis=basis, end=end, population_basis=frame,
                        population=b['population'] * f, cost_bn=b['cost_bn'] * f,
                        lineage_engine=u['engine'], comparator_engine=b['engine'], **lineage_fields,
                        mixed_unit_removal_bn=item11, mixed_unit_asymmetry=u['mixed_unit_asymmetry'],
                        comparator_item11_bn=correction['bn'], item11_paired_se_bn=correction['paired_se_bn'],
                        item11_comparator_se_bn=correction.get('comparator_se_bn'),
                        item11_se_scope=correction['se_scope'], membership_rule=b['membership_rule'],
                        comparator_coverage=b['comparator_coverage'], stated_claim=MC.stated(mortality_convention),
                        central=arm == CENTRAL['arm'] and mortality_convention == CENTRAL['mortality_convention'],
                        framing=CC.MIXED_FRAME,
                        cost_per_person=b['cost_per_person'], scaling_delta_bn=b['cost_bn'] * (f - 1),
                        black_minus_rough_lineage_bn=b['cost_bn'] * f - u['cost_bn'],
                        black_minus_lineage_one_sided_bn=(b['cost_bn'] - b['comparator_item11_bn']) * f - u['cost_bn'],
                        black_minus_lineage_without_item11_bn=b['cost_bn'] * f - u['cost_bn'] + item11 - correction['bn'],
                        rule='linear accounting standardization; fixed per-person amount, no new CES removal solve'))
                W.gate(f'{arm}/{basis}/{end}: population standardization conserves per-person amount (1e-9)',
                       abs(b['cost_bn'] * factor * 1e9 / (b['population'] * factor) - b['cost_per_person']) < 1e-9)
    W.stop_if_failed()
    changes = []
    for basis in W.BASES:
        for end in W.ENDS:
            for name in ('mexican_origin_rough', 'A1_third_plus_nh_white',
                         'A3_third_plus_nh_white_at_union_ages', 'A4_third_plus_nh_white_stationary', 'nh_black_rough'):
                values = {arm: lookup[arm, basis, end, name]['cost_bn'] for arm in
                    ('combined_before_round2', 'combined_bracket_only', 'combined_payroll_only',
                     'combined_bracket_payroll_joint', 'combined_rules_only')}
                before = values['combined_before_round2']
                bracket = values['combined_bracket_only'] - before
                payroll = values['combined_payroll_only'] - before
                joint = values['combined_bracket_payroll_joint'] - before
                ages = values['combined_rules_only'] - values['combined_bracket_payroll_joint']
                changes.append(dict(case='oct16', mortality_convention=MC.MIXED, mortality_bound='none',
                    basis=basis, end=end, group=name, engine=CC.engine_for(name),
                    before_cost_bn=before, bracket_rerake_change_bn=bracket, payroll_denominator_change_bn=payroll,
                    joint_bracket_payroll_change_bn=joint, interaction_bn=joint - bracket - payroll,
                    scenario_pension_selection_change_bn=ages, after_cost_bn=values['combined_rules_only'],
                    total_change_bn=values['combined_rules_only']-before))
    # Measure item 9 on each comparator's actual job-capital lines. Only the
    # domestic-source factor changes; counts, keys, mortality and responses stay.
    domestic = []
    old_job = json.loads((W.FISCAL / 'job_capital_taxes_2026_10_14/derived/item.json').read_text())
    for basis in W.BASES:
        for end in W.ENDS:
            for name, sc in groups.items():
                if name.startswith('mexican_'):
                    continue
                with W.patched(vars(W), ACC=combined):
                    new = W.run29(sc, end, basis, production='own', production_model=production,
                                  status_keys=status, status_rule='rules_only')
                    with W.patched(vars(W), JOB_CAPITAL=old_job):
                        old = W.run29(sc, end, basis, production='own', production_model=production,
                                      status_keys=status, status_rule='rules_only')
                parts = []
                for lid in ('corporate_capital', 'corporate_labor'):
                    a = next(r for r in old[1] if r[0] == 'receipts' and r[1] == lid)
                    b = next(r for r in new[1] if r[0] == 'receipts' and r[1] == lid)
                    parts.append((a[3] - b[3]) * b[4])
                    domestic.append(dict(case='oct16', mortality_convention=MC.MIXED, mortality_bound='none',
                        basis=basis, end=end, group=name, line=lid, old_amount_bn=a[3], domestic_amount_bn=b[3],
                        response=b[4], cost_change_bn=parts[-1], group_total_change_bn=new[0]['cost']-old[0]['cost'],
                        rule='own scenario job wage share times source K2 personal factor; no lineage scaling'))
                W.gate(f'item9/{basis}/{end}/{name}: own-line changes close (1e-9bn)',
                       abs(sum(parts) - (new[0]['cost']-old[0]['cost'])) < 1e-9)
    W.stop_if_failed()
    require_within_budget('symmetric comparators, before writing outputs')
    for table in ratio_tables.values():
        require_ratio_snapshot_fresh(table)
    write(HERE, 'symmetric_results_oct16.csv', results)
    write(HERE, 'symmetric_comparisons_oct16.csv', comparisons)
    write(HERE, 'symmetric_white_population_oct16.csv', white_scaled)
    write(HERE, 'lineage_engine_bridge_oct16.csv', bridges)
    write(HERE, 'round2_changes_oct16.csv', changes)
    write(HERE, 'symmetric_programs_oct16.csv.gz', program_rows)
    write(HERE, 'symmetric_status_sampling_oct16.csv', [dict(r, case='oct16', mortality_convention=MC.GENERAL, mortality_bound='none') for r in sampling])
    write(HERE, 'symmetric_hispanic_arm_oct16.csv', [dict(r, case='oct16', mortality_convention='pooled Hispanic mortality proxy', mortality_bound='low/high') for r in hispanic])
    write(HERE, 'domestic_source_changes_oct16.csv', domestic)
    write(BLACK, 'domestic_source_changes_oct16.csv', [r for r in domestic if r['group'] == 'nh_black_rough'])
    write(HERE, 'symmetric_white_measures_oct16.csv', [dict(case=r['case'], mortality_convention=r['mortality_convention'], mortality_bound=r['mortality_bound'],
        arm=r['arm'], basis=r['basis'], end=r['end'], group=r['group'],
        population=r['population'], allocated_balance_bn=r['allocated_balance_bn'],
        responsive_budget_cost_bn=r['responsive_budget_cost_bn'], capital_resource_cost_bn=r['capital_resource_cost_bn'],
        responsive_resource_cost_bn=r['cost_bn'], contribution_to_others_bn=r['contribution_to_others_bn'])
        for r in results if r['group'].startswith('A')])
    write(BLACK, 'symmetric_results_oct16.csv', [r for r in results if r['group'] in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough')])
    write(BLACK, 'symmetric_population_oct16.csv', scaled)
    write(BLACK, 'round2_changes_oct16.csv', [r for r in changes if r['group'] == 'nh_black_rough'])
    metadata = dict(case='oct16', allocation='personal', source_hashes=hashes,
                    assumed_whole_education_bridge_transfer=SCHOOL_BRIDGE_TRANSFER,
                    scalar_policies=W.SCALAR_POLICIES, status_method=status.source_info,
                    full_row13_symmetric=False,
                    row13_limit='matched and matched/pooled composite has no declared conserved comparator record vector; rules_only is a named sensitivity, never exact full-case symmetry',
                    credit_crossing='own-mask comparator survivor solve measured; applied after evaluator only',
                    comparator_item11_source_sha256=mixed['sha256'],
                    production_point_weight_rounding_max=production.point_weight_rounding_max,
                    source_proxy_limit='diagnostic only: old R9 union ratio held on changed denominator; do not interpret as status correction',
                    preserved_case_lineage=True, comparison_engine='rough on both sides',
                    bridge='lineage_engine_bridge_oct16.csv: evaluated lines, capital, production and post amounts; case minus rough; 1e-9bn closure',
                    mortality_substitution_bn=mortality_changes,
                    mortality_substitution_rule='central Fenelon Models 1/3 source coefficients on live pension amounts; source payer-generation shares held; completion/child overlay pension profiles bounded over source profiles; coverage on exported generation pension stocks; cash unchanged',
                    rough_mortality_limit='rough lineage takes the same authoritative lineage mortality change as the case; its alternative status/pension numerator is not an independent mortality remeasurement',
                    v8_asymmetry={'union_completion': W.META['union_completion']['counts'],
                                  'mixed_unit_removal': W.META['mixed_unit_removal']['by_end'],
                                  'coverage': W.META.get('coverage', {}),
                                  'comparator_completion': 'unmeasured; no counterpart invented',
                                  'comparator_mixed_unit_removal': ('measured for A1 whites and Black on own masks under the current '
                                      'and children rules; A3/A4 take A1\'s term reweighted (' + CC.REWEIGHT_RULE + '); A2 unmeasured'),
                                  'comparator_coverage': ('round 3: every comparator at its own 2020 PES coverage by age and sex '
                                      '(NH white alone; Black alone or in combination, Table C\'s universe; non-Hispanic q), '
                                      'priced on its own rough-engine records: members_coverage_oct15.py, derived arms ' + ', '.join(DERIVED)),
                                  'coverage_age_mix': 'coverage people take completed observed overlay age shares; generation-only source supplies no own-age people',
                                  'lineage_mortality': ('central: every group at its own mortality (combined_rules_members, own-group); '
                                      'whole-population pair beside (combined_rules_members_general); the mixed pair labelled, '
                                      'never a stated claim (stated_claim false)')},
                    round4=dict(membership='completed-lineage precedence; zero overlap for each comparison pair',
                        alternatives='White and Black are separate counterfactual removals, not a three-way partition',
                        school_prices='own race/state F-33 FY2024 x CCD SY2023-24 differential, mapped to live evaluator school dollars',
                        school_bridge='incidence residual preserved; school_reprice already present in both engines; optional R4_LINEAGE_SCHOOL_BRIDGE=1 assumed transfer',
                        row8='2 * current row8_factor / identified base-union persons, on each comparator; inherited lineage part retained once',
                        lineage_survivors='full expanded-minus-current adapter delta; already-booked completion credit subtracted once',
                        half_overlap='conditional endpoint interpolation, including half count/cost and signed survivor vectors on both sides',
                        limitations='unmeasured school-level district premium for comparators; item-P versus CPS/IPEDS college incidence; A2/all-residents current-rule readings only'),
                    round3=dict(central=CENTRAL, derived_arms=DERIVED,
                                membership_rule="children: members' biological minor children outside the group's definition depart with them and count as members, at their own costs",
                                school_key='every group keys K-12 on its own cell\'s October public K-12 rates at state spending per pupil (school_key_oct15.py)',
                                mortality_mix='group survival factors move only the retirement share the formula route models; disability, children\'s and young survivors\' shares keep the whole-population factor (mortality_comparators.left_out_share; lineage_mortality_mix_oct15.py)',
                                lineage_children_shift={f'{m}/{e}': v for (m, e), v in shift.items()},
                                members_source_sha256=digest(MEMBERS)))
    for lane in (HERE, BLACK):
        (lane / 'derived/symmetric_audit_oct16.json').write_text(json.dumps(metadata, indent=2) + '\n')
    elapsed = time.perf_counter() - started
    peak = require_within_budget('symmetric comparators')
    print(f'[PASS] P7 symmetric rules-only tables; elapsed_seconds={elapsed:.3f} peak_footprint_gb={peak / 1e9:.3f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', action='store_true', help='record explicitly inspected inputs, then run')
    main(parser.parse_args().pin)

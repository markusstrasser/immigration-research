"""P7 one-change-at-a-time comparator audit; frozen case and archive outputs read-only.

Run production_state_oct14.cjs, accrual_white.py --mortality and the Black lane's
accrual_black.py --mortality first. This route writes new symmetric_* tables in
the two comparator lanes. Legacy rough tables remain positive-control evidence.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
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


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check_pins(pin=False):
    paths = [W.R.ZIP, HERE / 'inputs/comparator_baseline_oct14.json',
             HERE / 'derived/rekey_summary_oct14.csv',
             HERE / 'derived/production_state_oct15.json',
             W.FISCAL / 'main_case_candidate_2026_09_28/derived/production_row4.json',
             W.FISCAL / 'matched_benefits_2026_09_19/model.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/common.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_status.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_onbooks_lane.py']
    paths += [W.FISCAL / 'main_case_2026_10_15/derived' / n for n in ('corrections.json', 'corrections_cash.json', 'summary.json')]
    paths += [lane / 'derived/accrual_ratios_mortality_oct15.csv' for lane in (HERE, BLACK)]
    paths += [MC.SOURCE / 'derived' / n for n in ('accrual_ratios.csv', 'reproduced_ratios.csv', 'case_changes.csv', 'comparisons.csv')]
    paths += [HERE / 'mortality_conventions.py',
              W.FISCAL / 'coverage_bound_2026_10_14/derived/coverage_bound_oct15.json',
              W.FISCAL / 'job_capital_taxes_2026_10_14/derived/item.json']
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    target = HERE / 'inputs/pins.json'
    data = json.loads(target.read_text())
    if pin:
        data['symmetric_inputs_oct15'] = hashes
        target.write_text(json.dumps(data, indent=2) + '\n')
    if data.get('symmetric_inputs_oct15') != hashes:
        raise SystemExit('[BLOCKED] comparator input pin mismatch; inspect changed source before repinning')
    return hashes


def write(lane, name, rows):
    with (lane / 'derived' / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


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
    hashes = check_pins(pin)
    baseline = json.loads((HERE / 'inputs/comparator_baseline_oct14.json').read_text())
    archive = pd.read_csv(HERE / 'derived/rekey_summary_oct14.csv').set_index(['basis', 'end', 'group'])
    for row in baseline:
        index = row['basis'], row['end'], row['group']
        for metric in ('cost', 'taxes_paid', 'spending_drawn', 'production_gain', 'capital'):
            W.gate(f'preserved v7 positive control {index}/{metric} (1e-12bn)', abs(archive.loc[index, metric] - row[metric]) < 1e-12)
    W.stop_if_failed()
    # The archived rows are read-only controls. Compute only the live case.
    W.use_case('oct15')
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
    }
    results, program_rows, bridges = [], [], []
    lookup = {}
    for arm, (policy, sk, accrual, rule) in arms.items():
        with W.patched(vars(W), ACC=accrual):
            for basis in W.BASES:
                for end in W.ENDS:
                    runs = {}
                    for name, sc in groups.items():
                        run = W.run29(sc, end, basis, production=policy, production_model=production,
                                      status_keys=sk, status_rule=rule)
                        runs[name] = run
                        r, lines = run[:2]
                        W.gate(f'{arm}/{basis}/{end}/{name}: cost identity (1e-9bn)',
                               abs(r['cost'] - (r['spending_saved'] - r['taxes_lost'] + r['capital'] - r['production_gain'])) < 1e-9)
                        before = legacy[basis, end, name]
                        se = sampling_se(production.evaluate(sc, end)) if policy == 'own' and sc != 'eng' and sc['name'] != 'mex' else None
                        item11 = W.META['mixed_unit_removal']['by_end'][end]['total_bn'] if name.startswith('mexican_') else 0.
                        row = dict(arm=arm, basis=basis, end=end, group=name, allocation='personal', population=r['population'],
                                   engine=CC.engine_for(name), mixed_unit_removal_bn=item11,
                                   mixed_unit_asymmetry='item11 measured for lineage only; comparator counterpart unmeasured',
                                   cost_without_item11_bn=r['cost'] - item11,
                                   cost_bn=r['cost'], change_from_raw_bn=r['cost'] - before['cost'],
                                   exceeds_5bn=abs(r['cost'] - before['cost']) >= 5,
                                   cost_per_person=r['cost'] * 1e9 / r['population'],
                                   allocated_balance_bn=r['balance'], responsive_budget_cost_bn=r['net_budget'],
                                   capital_resource_cost_bn=r['capital'], production_gain_bn=r['production_gain'],
                                   contribution_to_others_bn=-r['cost'], production_sampling_se_bn=se,
                                   se_scope='production only, conditional on fixed count and requested ages' if se is not None else 'not estimated')
                        row = MC.tag(row)
                        results.append(row)
                        lookup[arm, basis, end, name] = row
                        if name in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough', 'A1_third_plus_nh_white'):
                            for side, lid, national, amount, response in lines:
                                source = W.META.get('union_completion', {}).get('carriers', {}).get(lid, {})
                                program_rows.append(MC.tag(dict(arm=arm, basis=basis, end=end, group=name, side=side, line=lid,
                                                         source_side=source.get('side', side), source_line=source.get('parent_line', lid),
                                                         carrier_kind=source.get('kind', ''),
                                                         national_bn=national, amount_bn=amount, response=response)))
                    bridges.extend(dict(case='oct15', arm=arm, basis=basis, end=end,
                                        mortality_convention=MC.convention(arm), mortality_bound='none',
                                        case_engine='case', rough_engine='rough', **part)
                                   for part in CC.bridge_parts(runs['mexican_origin_engine'], runs['mexican_origin_rough'],
                                                              W.META['union_completion']['carriers']))
    mortality_changes = {end: MC.source_change(W.FULL, W.DUMP, W.META, end, include_coverage=True)
                         for end in W.ENDS}
    for original in list(bridges):
        if original['arm'] in MC.OWN_ARMS:
            for bound in ('low', 'high'):
                bridges.append(dict(original, mortality_convention=MC.OWN, mortality_bound=bound))
    for arm in arms:
        if arm in MC.OWN_ARMS:
            for basis in W.BASES:
                for end in W.ENDS:
                    for bound in ('low', 'high'):
                        delta = mortality_changes[end][bound] if basis == 'accrual' else 0.
                        bridges.append(dict(case='oct15', arm=arm, basis=basis, end=end,
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
            program_rows.append(dict(case='oct15', mortality_convention=MC.OWN,
                mortality_bound=r['mortality_bound'], mortality_delta_bn=r['mortality_delta_bn'],
                group_mortality='own-group', arm=r['arm'], basis=r['basis'], end=r['end'], group=r['group'],
                side='spending', line='lineage_mortality_substitution', source_side='spending',
                source_line='social_security_and_medicare_part_a', carrier_kind='mortality_sensitivity',
                national_bn=0., amount_bn=r['mortality_delta_bn'], response=1.))
    comparisons, scaled = [], []
    readings = [(arm, MC.convention(arm), 'none') for arm in arms]
    readings += [(arm, MC.OWN, bound) for arm in arms if arm in MC.OWN_ARMS for bound in ('low', 'high')]
    for arm, mortality_convention, mortality_bound in readings:
        for basis in W.BASES:
            for end in W.ENDS:
                def get(name):
                    key = (arm, basis, end, name)
                    return lookup[key + (MC.OWN, mortality_bound)] if mortality_convention == MC.OWN else lookup[key]
                u, e, w, b = map(get, ('mexican_origin_rough', 'mexican_origin_engine', 'A1_third_plus_nh_white', 'nh_black_rough'))
                for comparator in (w, b):
                    MC.validate_pair(u, comparator, mortality_convention)
                item11 = u['mixed_unit_removal_bn']
                comparisons.append(dict(case='oct15', mortality_convention=mortality_convention, mortality_bound=mortality_bound,
                    arm=arm, basis=basis, end=end,
                    **CC.gap_fields(u, w, b, item11),
                    case_minus_rough_bridge_bn=e['cost_bn'] - u['cost_bn'],
                    full_row13_symmetric=False))
                factor = e['population'] / b['population']
                for frame, f in (('own_count', 1.), ('scaled_to_lineage', factor)):
                    scaled.append(dict(case='oct15', mortality_convention=mortality_convention, mortality_bound=mortality_bound,
                        arm=arm, basis=basis, end=end, population_basis=frame,
                        population=b['population'] * f, cost_bn=b['cost_bn'] * f,
                        lineage_engine=u['engine'], comparator_engine=b['engine'],
                        mixed_unit_removal_bn=item11, mixed_unit_asymmetry=u['mixed_unit_asymmetry'],
                        cost_per_person=b['cost_per_person'], scaling_delta_bn=b['cost_bn'] * (f - 1),
                        black_minus_rough_lineage_bn=b['cost_bn'] * f - u['cost_bn'],
                        black_minus_lineage_without_item11_bn=b['cost_bn'] * f - u['cost_bn'] + item11,
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
                changes.append(dict(case='oct15', mortality_convention=MC.MIXED, mortality_bound='none',
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
                    domestic.append(dict(case='oct15', mortality_convention=MC.MIXED, mortality_bound='none',
                        basis=basis, end=end, group=name, line=lid, old_amount_bn=a[3], domestic_amount_bn=b[3],
                        response=b[4], cost_change_bn=parts[-1], group_total_change_bn=new[0]['cost']-old[0]['cost'],
                        rule='own scenario job wage share times source K2 personal factor; no lineage scaling'))
                W.gate(f'item9/{basis}/{end}/{name}: own-line changes close (1e-9bn)',
                       abs(sum(parts) - (new[0]['cost']-old[0]['cost'])) < 1e-9)
    W.stop_if_failed()
    require_within_budget('symmetric comparators, before writing outputs')
    for table in ratio_tables.values():
        require_ratio_snapshot_fresh(table)
    write(HERE, 'symmetric_results_oct15.csv', results)
    write(HERE, 'symmetric_comparisons_oct15.csv', comparisons)
    write(HERE, 'lineage_engine_bridge_oct15.csv', bridges)
    write(HERE, 'round2_changes_oct15.csv', changes)
    write(HERE, 'symmetric_programs_oct15.csv', program_rows)
    write(HERE, 'symmetric_status_sampling_oct15.csv', [dict(r, case='oct15', mortality_convention=MC.GENERAL, mortality_bound='none') for r in sampling])
    write(HERE, 'symmetric_hispanic_arm_oct15.csv', [dict(r, case='oct15', mortality_convention='pooled Hispanic mortality proxy', mortality_bound='low/high') for r in hispanic])
    write(HERE, 'domestic_source_changes_oct15.csv', domestic)
    write(BLACK, 'domestic_source_changes_oct15.csv', [r for r in domestic if r['group'] == 'nh_black_rough'])
    write(HERE, 'symmetric_white_measures_oct15.csv', [dict(case=r['case'], mortality_convention=r['mortality_convention'], mortality_bound=r['mortality_bound'],
        arm=r['arm'], basis=r['basis'], end=r['end'], group=r['group'],
        population=r['population'], allocated_balance_bn=r['allocated_balance_bn'],
        responsive_budget_cost_bn=r['responsive_budget_cost_bn'], capital_resource_cost_bn=r['capital_resource_cost_bn'],
        responsive_resource_cost_bn=r['cost_bn'], contribution_to_others_bn=r['contribution_to_others_bn'])
        for r in results if r['group'].startswith('A')])
    write(BLACK, 'symmetric_results_oct15.csv', [r for r in results if r['group'] in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough')])
    write(BLACK, 'symmetric_population_oct15.csv', scaled)
    write(BLACK, 'round2_changes_oct15.csv', [r for r in changes if r['group'] == 'nh_black_rough'])
    metadata = dict(case='oct15', allocation='personal', source_hashes=hashes,
                    scalar_policies=W.SCALAR_POLICIES, status_method=status.source_info,
                    full_row13_symmetric=False,
                    row13_limit='matched and matched/pooled composite has no declared conserved comparator record vector; rules_only is a named sensitivity, never exact full-case symmetry',
                    credit_crossing='comparator crossings not measured; union case crossings preserved',
                    production_point_weight_rounding_max=production.point_weight_rounding_max,
                    source_proxy_limit='diagnostic only: old R9 union ratio held on changed denominator; do not interpret as status correction',
                    preserved_case_lineage=True, comparison_engine='rough on both sides',
                    bridge='lineage_engine_bridge_oct15.csv: evaluated lines, capital, production and post amounts; case minus rough; 1e-9bn closure',
                    mortality_substitution_bn=mortality_changes,
                    mortality_substitution_rule='central Fenelon Models 1/3 source coefficients on live pension amounts; source payer-generation shares held; completion/child overlay pension profiles bounded over source profiles; coverage on exported generation pension stocks; cash unchanged',
                    rough_mortality_limit='rough lineage takes the same authoritative lineage mortality change as the case; its alternative status/pension numerator is not an independent mortality remeasurement',
                    v8_asymmetry={'union_completion': W.META['union_completion']['counts'],
                                  'mixed_unit_removal': W.META['mixed_unit_removal']['by_end'],
                                  'coverage': W.META.get('coverage', {}),
                                  'comparator_completion_and_mixed_unit_removal': 'unmeasured; no counterpart invented',
                                  'comparator_coverage': 'none; NH-white PES rates exist but no own-price cohort/base-adjusted term; Black rates absent from source export',
                                  'coverage_age_mix': 'coverage people take completed observed overlay age shares; generation-only source supplies no own-age people',
                                  'lineage_mortality': 'whole-population headline; explicit mixed and own-group comparisons beside'})
    for lane in (HERE, BLACK):
        (lane / 'derived/symmetric_audit_oct15.json').write_text(json.dumps(metadata, indent=2) + '\n')
    elapsed = time.perf_counter() - started
    peak = require_within_budget('symmetric comparators')
    print(f'[PASS] P7 symmetric rules-only tables; elapsed_seconds={elapsed:.3f} peak_footprint_gb={peak / 1e9:.3f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', action='store_true', help='record explicitly inspected inputs, then run')
    main(parser.parse_args().pin)

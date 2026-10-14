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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BLACK = W.BLACK_LANE


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check_pins(pin=False):
    paths = [W.R.ZIP, HERE / 'inputs/comparator_baseline_oct14.json',
             HERE / 'derived/production_state_oct14.json',
             W.FISCAL / 'main_case_candidate_2026_09_28/derived/production_row4.json',
             W.FISCAL / 'matched_benefits_2026_09_19/model.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/common.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_status.py',
             W.FISCAL / 'cps_imputation_keys_2026_09_23/combine_onbooks_lane.py']
    paths += [W.FISCAL / 'main_case_2026_10_14/derived' / n for n in ('corrections.json', 'corrections_cash.json', 'summary.json')]
    paths += [lane / 'derived/accrual_ratios_mortality_oct14.csv' for lane in (HERE, BLACK)]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    target = HERE / 'inputs/pins.json'
    data = json.loads(target.read_text())
    if pin:
        data['symmetric_inputs'] = hashes
        target.write_text(json.dumps(data, indent=2) + '\n')
    if data.get('symmetric_inputs') != hashes:
        raise SystemExit('[BLOCKED] comparator input pin mismatch; inspect changed source before repinning')
    return hashes


def write(lane, name, rows):
    with (lane / 'derived' / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def mortality_params(mortality='specific', basis='row4'):
    """Only comparator ratios change; union's recorded accrual stays the principal.

    Ratios are applied to account-frame payroll amounts. Pension helper frame
    counts never replace the comparator's own population denominator.
    """
    params = copy.deepcopy(W.ACC)
    for lane, group, key, specific in ((HERE, 'third_plus_nh_white', 'white', 'nh_white'),
                                        (BLACK, 'nh_black', 'black', 'nh_black')):
        rows = pd.read_csv(lane / 'derived/accrual_ratios_mortality_oct14.csv')
        mt = specific if mortality == 'specific' else 'general'
        selected = rows[(rows.group == group) & (rows.basis == basis) & (rows.mortality == mt)
                        & (rows.scenario == 'payable') & (rows.entry_rule == 'immigrants_at_arrival')]
        if len(selected) != 1:
            raise SystemExit(f'[BLOCKED] ambiguous mortality ratio {group}/{mt}')
        params[key] = W.acc_entry(selected.iloc[0].to_dict())
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


def hispanic_arm():
    """Exact identified-union ratio swap plus a bounded added-profile extension.

    Added pension dollar splits by measured age profile are not exported by the
    frozen case. Do not invent them: bound the added accrued dollars by the min
    and max full-precision factors for its three profiles, stated as a proxy.
    """
    rows = pd.read_csv(HERE / 'derived/accrual_ratios_mortality_oct14.csv')
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
                        rule='2026 payable Hispanic pooled proxy; current benefit-tax receipt fixed; added dollar split bounded over measured profiles, no invented exact split'))
    return out


def main(pin=False):
    started = time.perf_counter()
    hashes = check_pins(pin)
    W.use_case('oct14')
    W.setup()
    groups = W.scenarios()
    baseline = json.loads((HERE / 'inputs/comparator_baseline_oct14.json').read_text())
    legacy = {}
    for basis in W.BASES:
        for end in W.ENDS:
            for name, sc in groups.items():
                result = W.run29(sc, end, basis)[0]
                old = next(r for r in baseline if (r['basis'], r['end'], r['group']) == (basis, end, name))
                for metric in ('cost', 'taxes_paid', 'spending_drawn', 'production_gain', 'capital'):
                    W.gate(f'P7 raw positive control {basis}/{end}/{name}/{metric} (5e-5bn)', abs(result[metric] - old[metric]) < 5e-5)
                legacy[basis, end, name] = result
    W.stop_if_failed()
    production = Production(W)
    status = status_build(W)
    closure = status.closure({ln['id']: ln['national_bn'] for ln in W.DUMP['cash']['low']['lines']
                             if ln['side'] == 'receipts' and ln['id'] in LINE_KEYS})
    W.gate('24 status line/rule national closures (1e-6bn)', len(closure) == 24 and all(abs(r['error_bn']) <= 1e-6 for r in closure))
    sampling = [status_sampling(status, production, groups[name], end)
                for name in ('mexican_origin_rough', 'nh_black_rough', 'A1_third_plus_nh_white') for end in W.ENDS]
    hispanic = hispanic_arm()
    specific = mortality_params()
    general_row4 = mortality_params('general')
    symmetric_general = mortality_params('general', 'symmetric')
    symmetric_specific = mortality_params('specific', 'symmetric')
    fixed_benefits = status_params(status, coupled=False)
    coupled = status_params(status, coupled=True)
    combined = copy.deepcopy(symmetric_specific)
    combined['union'] = coupled['union']
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
        'combined_rules_only': ('own', status, combined, 'rules_only'),
        'combined_zero_production': ('zero', status, combined, 'rules_only'),
    }
    results, program_rows = [], []
    lookup = {}
    for arm, (policy, sk, accrual, rule) in arms.items():
        with W.patched(vars(W), ACC=accrual):
            for basis in W.BASES:
                for end in W.ENDS:
                    for name, sc in groups.items():
                        r, lines = W.run29(sc, end, basis, production=policy, production_model=production,
                                          status_keys=sk, status_rule=rule)[:2]
                        W.gate(f'{arm}/{basis}/{end}/{name}: cost identity (1e-9bn)',
                               abs(r['cost'] - (r['spending_saved'] - r['taxes_lost'] + r['capital'] - r['production_gain'])) < 1e-9)
                        before = legacy[basis, end, name]
                        se = sampling_se(production.evaluate(sc, end)) if policy == 'own' and sc != 'eng' and sc['name'] != 'mex' else None
                        row = dict(arm=arm, basis=basis, end=end, group=name, allocation='personal', population=r['population'],
                                   cost_bn=r['cost'], change_from_raw_bn=r['cost'] - before['cost'],
                                   exceeds_5bn=abs(r['cost'] - before['cost']) >= 5,
                                   cost_per_person=r['cost'] * 1e9 / r['population'],
                                   allocated_balance_bn=r['balance'], responsive_budget_cost_bn=r['net_budget'],
                                   capital_resource_cost_bn=r['capital'], production_gain_bn=r['production_gain'],
                                   contribution_to_others_bn=-r['cost'], production_sampling_se_bn=se,
                                   se_scope='production only, conditional on fixed count and requested ages' if se is not None else 'not estimated')
                        results.append(row)
                        lookup[arm, basis, end, name] = row
                        if name in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough', 'A1_third_plus_nh_white'):
                            for side, lid, national, amount, response in lines:
                                program_rows.append(dict(arm=arm, basis=basis, end=end, group=name, side=side, line=lid,
                                                         national_bn=national, amount_bn=amount, response=response))
    comparisons, scaled = [], []
    for arm in arms:
        for basis in W.BASES:
            for end in W.ENDS:
                u = lookup[arm, basis, end, 'mexican_origin_rough']
                e = lookup[arm, basis, end, 'mexican_origin_engine']
                w = lookup[arm, basis, end, 'A1_third_plus_nh_white']
                b = lookup[arm, basis, end, 'nh_black_rough']
                comparisons.append(dict(arm=arm, basis=basis, end=end,
                    white_gap_rough_union_bn=u['cost_bn'] - w['cost_bn'],
                    white_gap_case_lineage_bn=e['cost_bn'] - w['cost_bn'],
                    black_minus_rough_union_bn=b['cost_bn'] - u['cost_bn'],
                    black_minus_case_lineage_bn=b['cost_bn'] - e['cost_bn'],
                    rough_union_residual_to_case_bn=u['cost_bn'] - e['cost_bn'],
                    full_row13_symmetric=False))
                factor = e['population'] / b['population']
                for frame, f in (('own_count', 1.), ('scaled_to_lineage', factor)):
                    scaled.append(dict(arm=arm, basis=basis, end=end, population_basis=frame,
                        population=b['population'] * f, cost_bn=b['cost_bn'] * f,
                        cost_per_person=b['cost_per_person'], scaling_delta_bn=b['cost_bn'] * (f - 1),
                        black_minus_case_lineage_bn=b['cost_bn'] * f - e['cost_bn'],
                        black_minus_rough_union_bn=b['cost_bn'] * f - u['cost_bn'],
                        rule='linear accounting standardization; fixed per-person amount, no new CES removal solve'))
                W.gate(f'{arm}/{basis}/{end}: population standardization conserves per-person amount (1e-9)',
                       abs(b['cost_bn'] * factor * 1e9 / (b['population'] * factor) - b['cost_per_person']) < 1e-9)
    W.stop_if_failed()
    require_within_budget('symmetric comparators, before writing outputs')
    write(HERE, 'symmetric_results_oct14.csv', results)
    write(HERE, 'symmetric_comparisons_oct14.csv', comparisons)
    write(HERE, 'symmetric_programs_oct14.csv', program_rows)
    write(HERE, 'symmetric_status_sampling_oct14.csv', sampling)
    write(HERE, 'symmetric_hispanic_arm_oct14.csv', hispanic)
    write(HERE, 'symmetric_white_measures_oct14.csv', [dict(arm=r['arm'], basis=r['basis'], end=r['end'], group=r['group'],
        population=r['population'], allocated_balance_bn=r['allocated_balance_bn'],
        responsive_budget_cost_bn=r['responsive_budget_cost_bn'], capital_resource_cost_bn=r['capital_resource_cost_bn'],
        responsive_resource_cost_bn=r['cost_bn'], contribution_to_others_bn=r['contribution_to_others_bn'])
        for r in results if r['group'].startswith('A')])
    write(BLACK, 'symmetric_results_oct14.csv', [r for r in results if r['group'] in ('mexican_origin_engine', 'mexican_origin_rough', 'nh_black_rough')])
    write(BLACK, 'symmetric_population_oct14.csv', scaled)
    metadata = dict(case='oct14', allocation='personal', source_hashes=hashes,
                    scalar_policies=W.SCALAR_POLICIES, status_method=status.source_info,
                    full_row13_symmetric=False,
                    row13_limit='matched and matched/pooled composite has no declared conserved comparator record vector; rules_only is a named sensitivity, never exact full-case symmetry',
                    credit_crossing='comparator crossings not measured; union case crossings preserved',
                    production_point_weight_rounding_max=production.point_weight_rounding_max,
                    source_proxy_limit='diagnostic only: old R9 union ratio held on changed denominator; do not interpret as status correction',
                    preserved_case_lineage=True)
    for lane in (HERE, BLACK):
        (lane / 'derived/symmetric_audit_oct14.json').write_text(json.dumps(metadata, indent=2) + '\n')
    elapsed = time.perf_counter() - started
    peak = require_within_budget('symmetric comparators')
    print(f'[PASS] P7 symmetric rules-only tables; elapsed_seconds={elapsed:.3f} peak_footprint_gb={peak / 1e9:.3f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', action='store_true', help='record explicitly inspected inputs, then run')
    main(parser.parse_args().pin)

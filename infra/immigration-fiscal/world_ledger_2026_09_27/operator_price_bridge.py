"""Price-only bridge on captured v7 inputs; never regenerate historical outputs.

Run with --captured <scratch>/prop8/world --out <scratch>/prop8/world/operator-price.
The published recipe is loaded from the capture's exact historical source pin;
upstream ownership, pension and capital fixes are held out of this price-only
comparison. Live evaluators independently apply service_prices.py by default.
"""
import argparse
import copy
import hashlib
import json
import pickle
import resource
import subprocess
import sys
import time
import types
from pathlib import Path

import numpy as np
import pandas as pd

from mexico_prices import budget_from_gdp, budget_values, numeric_row_metadata, validate_numeric_rows
from service_prices import prepare_us_service_values
import beside_extra as LIVE_X

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
WEIGHTS = ('equal', 'equal_lambda_1.16', 'equal_lambda_1.5',
           'equal_lambda_hendren_a', 'hendren_a', 'hendren_b', 'log_a', 'log_b')
PARTS = dict(world_total_bn='world_total', group_total_bn='group_total',
             mexico_residents_bn='mexico_residents', other_us_residents_bn='other_us_residents_total')


def historical(name, ref):
    rel = f'infra/immigration-fiscal/world_ledger_2026_09_27/{name}.py'
    source = subprocess.run(['git', '-C', str(REPO), 'show', f'{ref}:{rel}'],
                            check=True, capture_output=True).stdout
    module = types.ModuleType('price_bridge_' + name)
    module.__file__ = str(HERE / (name + '.py'))
    exec(compile(source, module.__file__, 'exec'), vars(module))
    return module, hashlib.sha256(source).hexdigest()


def exemptions(vgen, name, B):
    v = vgen.copy()
    v['us_service_price_exemption'] = None
    if name.startswith(('reading2', 'combined_low')) or name in ('arm3a', 'arm3_mexican_numeraire'):
        mask = v.cls.isin(B.HEALTH_CLASSES) | v.line.isin(B.SOCIAL_LINES)
        v.loc[mask, 'us_service_price_exemption'] = 'Mexican prices'
    if name == 'arm3_mexican_numeraire':
        v.loc[v.cls.isin(['public_good', 'justice', 'cash', 'snap']), 'us_service_price_exemption'] = 'Mexican prices'
    if name.startswith('p7_goods_wtp_'):
        v.loc[v.cls.eq('public_good'), 'us_service_price_exemption'] = 'WTP'
    return v


def money_rows(rows, prem, I, base_budget, rates, kw, W, tax_divisor=None):
    """Price Mexico from actual source pesos; leave private compensation fixed.

    Captured published G3+ definitions stay fixed in this isolated bridge. The
    live producer's common-generation PPP and compensation gates are separate.
    """
    out = rows.copy().set_index('row')
    response = W.MEXICO_PUBLIC_RESPONSE
    hv = kw.get('mexico_health_vg') or I['health_vg']
    for gen in W.GENS:
        saved, _, lost = budget_values(base_budget, gen, hv, response, kw.get('pgc', 'average_cost'))
        out.loc[f'mexico_budget_saved_{gen}', ['low', 'central', 'high']] = [saved[e] for e in ('low', 'central', 'high')]
        out.loc[f'mexico_budget_lost_{gen}', ['low', 'central', 'high']] = [lost[e] for e in ('low', 'central', 'high')]
        # The published table copies household-PPP G1/G2 cells into GDP slots.
        # Identify their actual divisor from the reading's specified pay basis.
        is_consumption = gen != 'G3+' and (I['g2'].attrs.get('central_ppp') == 'consumption'
                                         or kw.get('_household_consumption', False))
        divisor = rates['PA.NUS.PRVT.PP'] if is_consumption else rates['PA.NUS.PPP']
        tax = {e: prem[gen]['tax'][e] + prem[gen]['ctax'][e] for e in ('low', 'central', 'high')}
        out.loc[f'mexico_taxes_lost_{gen}', ['low', 'central', 'high']] = [
            -tax[e] * divisor / (tax_divisor or rates['PA.NUS.PPP']) for e in ('low', 'central', 'high')]
    remit = -sum(float(out.loc[f'remit_{g}', 'central']) for g in ('G1', 'G2'))
    recipient = remit * rates['PA.NUS.FCRF'] / rates['PA.NUS.PRVT.PP']
    out.loc['remit_mexico', ['low', 'central', 'high']] = recipient
    out.loc['remit_mexico', 'price_basis'] = 'PPP-consumption'
    fiscal = out.index.str.startswith(('mexico_budget_saved_', 'mexico_taxes_lost_'))
    out.loc[fiscal, 'price_basis'] = 'PPP-GDP' if tax_divisor is None else 'PPP-category-services'
    return out.reset_index()


def numeric_contract(rows, prem, budget, rates, kw, W):
    """Source-peso receipts for the archived mixed-price companions too."""
    out = rows.copy()
    for index, row in out[out.party.eq('mexico_residents')].iterrows():
        if row.row == 'remit_mexico':
            nominal = -rows[rows.row.isin(['remit_G1', 'remit_G2'])].central.sum()
            pesos = dict.fromkeys(('low', 'central', 'high'), nominal * rates['PA.NUS.FCRF'])
            basis = 'household-consumption-or-published-GDP'
        elif row.row.startswith('mexico_budget_saved_'):
            gen = row.row.removeprefix('mexico_budget_saved_')
            pesos = budget_values(budget, gen, I_health(kw), W.MEXICO_PUBLIC_RESPONSE,
                                  kw.get('pgc', 'average_cost'))[1]
            basis = 'declared-budget-price-rule'
        elif row.row.startswith('mexico_taxes_lost_'):
            gen = row.row.removeprefix('mexico_taxes_lost_')
            consumption = gen != 'G3+' and kw.get('_household_consumption', False)
            divisor = rates['PA.NUS.PRVT.PP'] if consumption else rates['PA.NUS.PPP']
            pesos = {e: -(prem[gen]['tax'][e] + prem[gen]['ctax'][e]) * divisor
                     for e in ('low', 'central', 'high')}
            basis = 'declared-fiscal-money-or-published-household-rule'
        else:
            raise SystemExit(f'[BLOCKED] unknown Mexico price-bridge row {row.row}')
        div = {e: pesos[e] / row[e] for e in pesos}
        meta = numeric_row_metadata(pesos, div, basis)
        for column, value in meta.items():
            out.loc[index, column] = value
    validate_numeric_rows(out)
    return out


def I_health(kw):
    return kw.get('mexico_health_vg') or (1.0, 1.0, 1.0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--captured', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--ref', default='f3148023')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    W, wh = historical('world_ledger', args.ref)
    B, bh = historical('beside_arms', args.ref)
    X, xh = historical('beside_extra', args.ref)
    B.W, X.W, X.B = W, W, B
    capture_receipt = json.loads((args.captured / 'baseline_receipt.json').read_text())
    W.gate('price_bridge_exact_published_source', xh == capture_receipt['source_sha256'])
    with (args.captured / 'prepared_v7.pkl').open('rb') as stream:
        prepared = pickle.load(stream)
    rates = prepared['rates']
    original_fiscal = W.fiscal_group_rows

    def fiscal(I, convention):
        v = prepare_us_service_values(I['vgen'], convention, I.get('operator_us_general', False))
        return original_fiscal(dict(I, vgen=v), 'average_cost')

    W.fiscal_group_rows = fiscal
    budget = budget_from_gdp(prepared['I']['mxb'], rates['PA.NUS.PPP'])
    legacy_validate = W.validate_rows

    def validate(rows, logarithmic=False):
        # Published companions intentionally retain their mixed price rules;
        # their numeric conversions still have to reconstruct each source peso.
        legacy_validate(rows[~rows.party.eq('mexico_residents')], logarithmic=False)
        validate_numeric_rows(rows)

    W.validate_rows = validate
    brief = LIVE_X.fiscal_price_inputs(dict(prepared['I'], mxb=budget), prepared['ratio'], rates)
    summaries, details, line_receipts = [], [], []
    oracle = pd.read_csv(HERE / 'derived/p7_named_readings_oct14.csv')
    stored_extra = pd.read_csv(HERE / 'derived/beside_extra_summary_oct14.csv')
    published_max_error = 0.0
    us_cost_max_error = 0.0
    fiscal_columns = ['amount_bn', 'response', 'G_bn', 'net_cost_bn']
    scenarios = [s for s in prepared['S'] if B.scenario_bound(s[0]) == 'zero'
                 and (s[0] == 'baseline' or s[1] in ('reading_1', 'reading_2', 'same_person', 'p7_6a', 'p7_11'))]
    for name, arm, label, inputs, original_kw in scenarios:
        household_consumption = name.startswith(('reading1', 'reading3', 'p7_')) or name.endswith('_consumption')
        tagged = exemptions(inputs['vgen'], name, B)
        source = prepare_us_service_values(tagged, original_kw.get('pgc', 'average_cost'), enabled=False)
        priced = prepare_us_service_values(tagged, original_kw.get('pgc', 'average_cost'))
        W.gate('price_bridge_us_fiscal_columns_exact', priced[fiscal_columns].equals(tagged[fiscal_columns]))
        audit = priced[['end', 'generation', 'side', 'line', 'cls', 'us_price_category',
                        'us_price_factor', 'us_price_reason', *fiscal_columns]].copy()
        audit['original_recipient_value_bn'] = source.V_central_bn
        audit['ruled_recipient_value_bn'] = priced.V_central_bn
        audit['recipient_value_lost_bn'] = source.V_central_bn - priced.V_central_bn
        line_receipts.append(audit.assign(reading=name))
        for bound in ('zero', 'upper'):
            for end in ('low', 'high'):
                kw = dict(original_kw, g3_bound=bound, end=end)
                base_I = copy.deepcopy(inputs)
                # The archived evaluator calls its row gate while evaluating.
                # Baselines are first computed with their original checker.
                W.validate_rows = legacy_validate
                before_rows, before_prem, _ = X.evaluate(base_I, prepared['fac'], **kw)
                endpoint_I = dict(base_I, account_end=end)
                before = W.totals(before_rows, before_prem, endpoint_I, 'central', prepared['fac'],
                                  base_I['pos'], requested_weightings=WEIGHTS)
                ref = oracle[oracle.scenario.eq(B.bound_name(name, bound)) & oracle.end.eq(end)
                             & oracle.weighting.isin(WEIGHTS)]
                if name == 'reading1':
                    for r in ref.itertuples():
                        value = before[before.weighting.eq(r.weighting) & before.party.eq('world_total')].bn.item()
                        published_max_error = max(published_max_error, abs(value - r.world_total_bn))
                # The centre of every published reading is also a second oracle.
                if bound == 'zero' and end == 'low':
                    _, _, centre = X.evaluate(base_I, prepared['fac'], **dict(original_kw, g3_bound='zero'))
                    expected = stored_extra[stored_extra.scenario.eq(name) & stored_extra.weighting.isin(centre.weighting)]
                    for r in expected.itertuples():
                        value = centre[centre.weighting.eq(r.weighting) & centre.party.eq('world_total')].bn.item()
                        published_max_error = max(published_max_error, abs(value - r.world_total_bn))
                for variant, mx, us in (('published', False, False), ('mexico_only', True, False),
                                        ('us_only', False, True), ('both', True, True), ('brief_category', True, False)):
                    W.validate_rows = legacy_validate
                    obj = dict(base_I, vgen=tagged, operator_us_general=us)
                    rows, prem, _ = X.evaluate(obj, prepared['fac'], **kw)
                    if mx:
                        target = brief['mxb'] if variant == 'brief_category' else budget
                        tax_divisor = brief['mexico_tax_ppp_divisor'] if variant == 'brief_category' else None
                        rows = money_rows(rows, prem, obj, target, rates,
                                          dict(kw, _household_consumption=household_consumption), W, tax_divisor)
                    rows = numeric_contract(rows, prem, budget, rates,
                                            dict(kw, _household_consumption=household_consumption), W)
                    W.validate_rows = validate
                    totals = W.totals(rows, prem, dict(obj, account_end=end), 'central', prepared['fac'],
                                      obj['pos'], requested_weightings=WEIGHTS)
                    mask = rows.party.isin(['others_today', 'future_taxpayers'])
                    fiscal_diff = np.max(np.abs(rows.loc[mask, ['low', 'central', 'high']].to_numpy()
                                                - before_rows.loc[mask, ['low', 'central', 'high']].to_numpy()))
                    us_cost_max_error = max(us_cost_max_error, float(fiscal_diff))
                    for weighting in WEIGHTS:
                        a = totals[totals.weighting.eq(weighting)].set_index('party').bn
                        b = before[before.weighting.eq(weighting)].set_index('party').bn
                        summaries.append(dict(reading=name, variant=variant, account_end=end,
                                              g3_bound=bound, weighting=weighting,
                                              **{key: a[party] for key, party in PARTS.items()},
                                              **{f'delta_{key}': a[party] - b[party] for key, party in PARTS.items()}))
                    details.append(rows.assign(reading=name, variant=variant, account_end=end, g3_bound=bound))
                print(f'PRICE_BRIDGE {name} {bound} {end}', flush=True)
    W.gate('price_bridge_published_oracles', published_max_error <= 5.01e-7,
           max_abs_error=published_max_error)
    W.gate('price_bridge_actual_us_cost_unchanged', us_cost_max_error == 0.0)
    table = pd.DataFrame(summaries)
    audit = pd.concat(line_receipts, ignore_index=True)
    # The dollar loss receipt must reconstruct the actual group's US-only
    # endpoint change, including response-only quantities and WTP exemptions.
    for row in table[table.variant.eq('us_only') & table.weighting.eq('equal')].itertuples():
        cells = audit[audit.reading.eq(row.reading) & audit.end.eq(row.account_end)]
        implied = (cells.ruled_recipient_value_bn - cells.original_recipient_value_bn).sum()
        W.gate('price_bridge_line_values_close_us_only_change',
               abs(implied - row.delta_group_total_bn) <= 1e-9,
               reading=row.reading, end=row.account_end, bound=row.g3_bound,
               error=float(implied - row.delta_group_total_bn))
    key = ['reading', 'account_end', 'g3_bound', 'weighting']
    by = {v: f.set_index(key) for v, f in table.groupby('variant')}
    for part in PARTS:
        error = (by['both'][f'delta_{part}'] - by['mexico_only'][f'delta_{part}']
                 - by['us_only'][f'delta_{part}']).abs().max()
        # Log utility can have a cross-term; equal and lambda/Hendren row sums are linear.
        linear = ~by['both'].index.get_level_values('weighting').str.startswith('log')
        W.gate('price_bridge_side_deltas_add_at_linear_weights',
               (by['both'][f'delta_{part}'] - by['mexico_only'][f'delta_{part}']
                - by['us_only'][f'delta_{part}'])[linear].abs().max() < 1e-9,
               part=part, all_weight_max_error=float(error))
    for name, frame in (('operator_price_changes_v7.csv', table),
                        ('operator_price_rows_v7.csv', pd.concat(details, ignore_index=True)),
                        ('operator_us_service_factors_v7.csv', audit)):
        frame.to_csv(args.out / name, index=False, float_format='%.12f', lineterminator='\n')
    receipt = dict(reference=args.ref, captured_sha256=hashlib.sha256(
        (args.captured / 'prepared_v7.pkl').read_bytes()).hexdigest(),
        source_sha256=dict(world_ledger=wh, beside_arms=bh, beside_extra=xh),
        readings=[s[0] for s in scenarios], rows=len(table),
        published_max_abs_error_bn=published_max_error, us_cost_max_abs_error_bn=us_cost_max_error,
        seconds=time.perf_counter() - started,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
        limitations='Price-only bridge holds published upstream compensation/G3/pension/capital definitions; not oct15 adoption')
    (args.out / 'operator_price_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()

"""Conditional benefit/fiscal bridge, using the existing stationary CES model.

Native-First: replay the existing generator, verify point estimates independently
through its public model functions, then use pandas for explicit accounting.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TARGET = 'mexican_observed_total'
KEYS = ['proxy', 'split', 'normalization', 'labor_share', 'sigma',
        'capital_adjustment', 'labor_supply_elasticity', 'capital_tax_retention']
RESPONSE_COLUMNS = ['fiscal_case', 'component', 'receipt_change_bn', 'spending_change_bn',
                    'tax_overlap_bn', 'fiscal_recycling_weight', 'transfer_phaseout', 'source_rule']


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def close(actual, expected, label, atol=1e-4):
    if not np.isfinite(actual).all() or not np.allclose(actual, expected, atol=atol, rtol=1e-10):
        raise ValueError(f'Accounting/source reconciliation failed: {label}')


def accounting(private, induced_tax, transfer_saving, direct_receipts, direct_spending,
               overlap, beta):
    """With target minus without; transfers between included parties cancel at beta=1."""
    if beta not in (0, 1):
        raise ValueError('Fiscal recycling weight must be the declared 0/1 endpoint')
    values = np.asarray([private, induced_tax, transfer_saving, direct_receipts,
                         direct_spending, overlap], float)
    if not np.isfinite(values).all():
        raise ValueError('Nonfinite bridge input')
    if overlap < 0:
        raise ValueError('Duplicated receipts must be nonnegative')
    budget = direct_receipts - direct_spending + induced_tax + transfer_saving - overlap
    private_after_transfers = private - transfer_saving
    welfare = private_after_transfers + beta * budget
    return dict(budget_change_bn=budget, private_after_transfers_bn=private_after_transfers,
                conditional_net_benefit_bn=welfare,
                unmodeled_benefit_for_zero_bn=-welfare,
                maximum_additional_overlap_before_zero_bn=welfare if beta else None)


def expand_ownership(source, model, composition, gdp_bn):
    if len(source) != 1296 or source.duplicated(KEYS).any():
        raise ValueError('Expected all 1296 unique upstream scenarios')
    rows = []
    for index, row in source.iterrows():
        cells = composition.loc[composition.proxy.eq(row.proxy) & composition.split.eq(row.split)]
        incomes = cells.pivot(index='skill', columns='group', values='estimate').sort_index()
        shares = incomes.national.to_numpy() / incomes.national.sum()
        fractions = incomes.target.to_numpy() / incomes.national.to_numpy()
        scale = gdp_bn * 1e9 if row.normalization == 'gdp' else incomes.national.sum() / row.labor_share
        result = model.equilibrium(shares, fractions, row.sigma, row.labor_share,
                                   row.capital_adjustment, row.labor_supply_elasticity)
        original = model.fiscal_and_private(result, [.384, .426], .246, row.capital_tax_retention)
        for name, value in original.items():
            # Scalar and161-column solves stop at different iterations under the
            # upstream1e-12 normalized fixed-point tolerance; bound rounding in dollars.
            close(scale * value, row[f'{name}_estimate'], f'upstream replay point {index}/{name}',
                  atol=scale * 1e-11)
        transfer = scale * np.dot([.038, .010], result['labor_gain']) / 1e9
        close(transfer, row.current_transfer_saving_estimate / 1e9, 'phaseout units', 1e-8)
        for excluded in (0., .5, 1.):
            part = model.fiscal_and_private(result, [.384, .426], .246, row.capital_tax_retention, excluded)
            private, tax = float(part['private_wtp'] * scale / 1e9), float(part['current_receipts_gain'] * scale / 1e9)
            capital_gain = float(result['capital_gain'] * scale / 1e9)
            capital_tax = float(part['capital_tax_gain'] * scale / 1e9)
            expected = row.private_wtp_estimate / 1e9 - excluded * (capital_gain - capital_tax)
            close(private, expected, 'ownership partition', 1e-8)
            item = {key: row[key] for key in KEYS}
            item.update(scenario_id=f'ces_{index:04d}_owner{int(excluded*100):03d}',
                        excluded_capital_owner_share=excluded,
                        ownership_class='core_all_outside_resident_owners' if excluded == 0 else 'unestimated_ownership_endpoint',
                        tax_classification_transport=row.tax_classification_transport,
                        private_after_tax_wtp_bn=private, induced_current_receipts_bn=tax,
                        labor_tax_gain_bn=float(part['labor_tax_gain'] * scale / 1e9),
                        capital_tax_gain_bn=capital_tax, source_transfer_saving_bn=transfer,
                        gross_income_gain_all_owners_bn=row.gross_income_gain_estimate / 1e9,
                        net_capital_income_all_owners_bn=capital_gain,
                        private_plus_receipts_bn=private + tax,
                        beta0_no_phaseout_private_bn=private,
                        beta0_with_phaseout_private_bn=private-transfer,
                        beta1_production_plus_budget_bn=private+tax,
                        net_direct_fiscal_response_for_zero_beta1_bn=-(private+tax),
                        private_plus_receipts_se_sampling_bn=(row.private_plus_receipts_se_sampling / 1e9 if excluded == 0 else np.nan),
                        sampling_status=('original_joint_161_weight_SE' if excluded == 0 else 'point_only_no_covariance_inference'),
                        complete_welfare_bound=False, direct_ledger_addition_permitted=False)
            rows.append(item)
    return pd.DataFrame(rows)


def validate_ownership_baselines(expanded, original):
    merged = original.merge(expanded, on=KEYS + ['excluded_capital_owner_share'], validate='one_to_one')
    if len(merged) != 18:
        raise ValueError('Expected all 18 pre-existing ownership scenarios')
    for old, new in [('private_wtp_estimate', 'private_after_tax_wtp_bn'),
                     ('current_receipts_gain_estimate', 'induced_current_receipts_bn'),
                     ('private_plus_receipts_estimate', 'private_plus_receipts_bn')]:
        close(merged[old].to_numpy() / 1e9, merged[new].to_numpy(), old, 1e-8)


def integrate(benefits, response):
    if set(RESPONSE_COLUMNS) - set(response):
        raise ValueError(f'Response CSV requires {RESPONSE_COLUMNS}')
    if response.empty or response[RESPONSE_COLUMNS].isna().any().any():
        raise ValueError('Missing fiscal response or explanation; no inferred defaults')
    if response.duplicated(['fiscal_case', 'component']).any():
        raise ValueError('Duplicate fiscal component within case')
    rows = []
    for case, inputs in response.groupby('fiscal_case', sort=True):
        if inputs.fiscal_recycling_weight.nunique() != 1 or inputs.transfer_phaseout.nunique() != 1:
            raise ValueError('A case must have one recycling/phaseout convention')
        beta = float(inputs.fiscal_recycling_weight.iloc[0])
        transfer_rule = inputs.transfer_phaseout.iloc[0]
        if transfer_rule not in ('none', 'source_2017'):
            raise ValueError('Unknown transfer phaseout rule')
        amounts = inputs[['receipt_change_bn', 'spending_change_bn', 'tax_overlap_bn']].to_numpy(float)
        if not np.isfinite(amounts).all():
            raise ValueError('Nonfinite component response')
        receipt, spending, overlap = amounts.sum(axis=0)
        for _, benefit in benefits.iterrows():
            transfer = benefit.source_transfer_saving_bn if transfer_rule == 'source_2017' else 0.
            calculated = accounting(benefit.private_after_tax_wtp_bn, benefit.induced_current_receipts_bn,
                                    transfer, receipt, spending, overlap, beta)
            rows.append(dict(fiscal_case=case, scenario_id=benefit.scenario_id,
                fiscal_recycling_weight=beta, transfer_phaseout=transfer_rule,
                direct_receipt_response_bn=receipt, direct_spending_response_bn=spending,
                already_counted_tax_overlap_bn=overlap, **calculated,
                status='CONDITIONAL_RESPONSE_CASE_NOT_IDENTIFIED_POLICY_EFFECT'))
    return pd.DataFrame(rows)


def read_verified(folder, name, fingerprints):
    audit = json.loads((folder / 'audit.json').read_text())
    path = folder / f'{name}.csv'
    if audit['outputs'][name] != sha(path):
        raise ValueError(f'Changed component output: {path}')
    for source, expected in audit['source_hashes'].items():
        if sha(source) != expected:
            raise ValueError(f'Changed source: {source}')
    fingerprints[str(folder / 'audit.json')] = sha(folder / 'audit.json')
    fingerprints[str(path)] = sha(path)
    return pd.read_csv(path)


def component_contract(root, fingerprints):
    fiscal = root / 'infra/immigration-fiscal'
    # School release uses a path-keyed manifest rather than macro's named-output audit.
    path = fiscal / 'school_enrollment_2026_09_20/derived/updated_account_components.csv'
    audit_path = path.parent / 'manifest.json'
    audit = json.loads(audit_path.read_text())
    for item in audit['inputs']:
        if sha(item['path']) != item['sha256']:
            raise ValueError(f'Changed school input: {item["path"]}')
        fingerprints[item['path']] = item['sha256']
    fingerprints[str(path)] = sha(path)
    fingerprints[str(audit_path)] = sha(audit_path)
    data = pd.read_csv(path)
    baseline = read_verified(fiscal / 'macro_closure_2026_09_19/derived', 'updated_account_components', fingerprints)
    effects_path = path.parent / 'correction_effects.csv'
    fingerprints[str(effects_path)] = sha(effects_path)
    effects = pd.read_csv(effects_path)
    keys = ['allocation', 'group', 'component']
    merged = data.merge(baseline, on=keys, suffixes=('_current', '_before'), validate='one_to_one')
    if len(merged) != len(data) or len(data) != len(baseline):
        raise ValueError('Current fiscal components changed ownership')
    merged = merged.merge(effects[keys + ['balance_change_bn']], on=keys, how='left', validate='one_to_one')
    delta = merged.balance_change_bn.fillna(0).to_numpy()
    close(merged.signed_bn_current.to_numpy(), merged.signed_bn_before.to_numpy() + delta,
          'current school revision exact component replacement', 1e-7)
    close(merged.receipts_bn_current.to_numpy(), merged.receipts_bn_before.to_numpy(), 'school leaves receipts unchanged', 1e-7)
    close(merged.spending_bn_current.to_numpy(), merged.spending_bn_before.to_numpy() - delta,
          'school signed spending change', 1e-7)
    target = data.loc[data.group.eq(TARGET), ['allocation', 'component', 'population', 'receipts_bn', 'spending_bn']].copy()
    if len(target) != 48 or target.duplicated(['allocation', 'component']).any():
        raise ValueError('Expected 24 disjoint target components per fiscal allocation')
    classifications = {
        'C': ('exclude_from_direct_response_when_CES_capital_tax_used', 'Incidence-allocated corporate pool can overlap modeled capital taxes.'),
        'owner_property': ('exclude_or_explicit_tax_base_overlap', 'CES has no separate housing sector; source capital-tax adjustment and GDP scope differ.'),
        'tax': ('split_payroll_from_income_tax', 'Personal capital-income tax is inseparable inside income-tax total; expose O.'),
        'employer': ('conditional_target_labor_tax_response', 'Wage payroll proxy; no inference that incidence assignment proves disappearance.'),
        'sales': ('conditional_target_consumption_response', 'Selected capital tax rate excludes sales; consumption response remains assumed.'),
        'X': ('conditional_excise_response', 'Mixed excise base; no automatic direct-revenue response.'),
        'F': ('fixed_public_goods_response_separate', 'Attribution is not avoidable defense/debt/general-government spending.'),
        'G_fee_grossup': ('couple_receipt_and_service_responses', 'Symmetric fee grossup must not generate a fictitious saving.'),
        'lunch': ('negative_spending_offset', 'Keep lunch reversal with its owning transfer line; do not count twice.'),
    }
    target['recommended_contract'] = [classifications.get(c, ('declare_service_response', 'Assigned spending is not measured avoidable cost.'))[0] for c in target.component]
    target['limitation'] = [classifications.get(c, ('declare_service_response', 'Assigned spending is not measured avoidable cost.'))[1] for c in target.component]
    target['disappearing_share'] = np.nan
    target['avoidable_share'] = np.nan
    target['receipt_tax_overlap_bn'] = np.nan
    tax = read_verified(fiscal / 'admin_tax_checks_2026_09_19/derived', 'group_components', fingerprints)
    tax = tax.loc[tax.group.eq(TARGET)].copy()
    return target, tax, audit


def build(root, out, response_path=None):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'audit.json').unlink(missing_ok=True)
    upstream = root / 'infra/immigration-fiscal/matched_benefits_2026_09_19'
    replay = out / 'upstream_replay'
    command = [sys.executable, str(upstream / 'builder.py'), '--source-root', str(root), '--out', str(replay)]
    completed = subprocess.run(command, text=True, capture_output=True)
    (out / 'upstream_replay.log').write_text(completed.stdout + completed.stderr)
    if completed.returncode:
        raise RuntimeError(f'Upstream replay failed ({completed.returncode}); see upstream_replay.log')
    manifest = json.loads((replay / 'audit.json').read_text())
    fingerprints = manifest['source_hashes'].copy()
    for source, expected in fingerprints.items():
        if sha(source) != expected:
            raise ValueError(f'Upstream input drift: {source}')
    spec = importlib.util.spec_from_file_location('matched_stationary_model', upstream / 'model.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    source = pd.read_csv(replay / 'scenarios.csv')
    composition = pd.read_csv(replay / 'skill_composition.csv')
    benefits = expand_ownership(source, model, composition, manifest['gdp_billions'])
    validate_ownership_baselines(benefits, pd.read_csv(replay / 'ownership_sensitivity.csv'))
    components, taxes, school_audit = component_contract(root, fingerprints)
    close(components.population.to_numpy(), manifest['population'], 'current fiscal target population', .001)
    frames = {'benefit_scenarios': benefits, 'current_component_contract': components,
              'current_tax_details': taxes,
              'benefit_grid_summary': benefits.groupby(['normalization', 'ownership_class', 'excluded_capital_owner_share',
                    'capital_adjustment', 'labor_supply_elasticity']).agg(
                    cases=('scenario_id', 'size'), benefit_min_bn=('private_plus_receipts_bn', 'min'),
                    benefit_max_bn=('private_plus_receipts_bn', 'max'),
                    private_min_bn=('private_after_tax_wtp_bn', 'min'), private_max_bn=('private_after_tax_wtp_bn', 'max')).reset_index()}
    if response_path is not None:
        frames['conditional_combination'] = integrate(benefits, pd.read_csv(response_path))
        fingerprints[str(response_path)] = sha(response_path)
    for name, frame in frames.items():
        frame.to_csv(out / f'{name}.csv', index=False)
    pd.DataFrame(columns=RESPONSE_COLUMNS).to_csv(out / 'fiscal_response_template.csv', index=False)
    for path in [Path(__file__), HERE / 'test_builder.py', HERE / 'README.md', HERE / 'mechanism_contracts.json',
                 *replay.glob('*.csv'), replay / 'audit.json']:
        fingerprints[str(path)] = sha(path)
    for name in ['immigration-matched-benefits-2026-09-19.md',
                 'immigration-consumer-price-and-native-hours-2026-09-18.md',
                 'immigration-hedonic-composition-amenity-2026-09-19.md',
                 'immigration-cultural-output-and-variety-saturation-2026-09-19.md',
                 'immigration-ncvs-victim-offender-off-the-murder-margin-2026-09-18.md',
                 'immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md']:
        path = root / 'research' / name
        fingerprints[str(path)] = sha(path)
    audit = dict(source_hashes=fingerprints, outputs={p.name: sha(p) for p in sorted(out.glob('*.csv'))},
                 population=manifest['population'], dollar_year=2024, upstream_scenarios=1296,
                 expanded_ownership_scenarios=len(benefits), beneficiaries='Other US residents outside canonical target',
                 counterfactual='Stationary economy with versus without target labor; fiscal response separately declared',
                 fiscal_combination_executed=response_path is not None,
                 baseline_full_ledger_automatically_netted=False, crime_or_amenity_values_added=False,
                 formulas={'budget': 'A + F + M - O', 'private': 'P - M', 'net': 'P - M + beta*(A + F + M - O)',
                           'beta1_breakeven': 'A - O + Z = -(P + F)'},
                 limitations=['Ownership0/.5/1 and fiscal recycling0/1 are unestimated scenario endpoints, not bounds',
                              'Original161-weight sampling SE retained only for core ownership; no invented covariance for new ownership rows',
                              '2017 tax/phaseout and2011-2013 capital tax parameters are transported assumptions',
                              'No historical/no-immigration, admission, deportation or lifetime effect identified',
                              'A complete incidence allocation does not establish disappearing taxes or avoidable costs',
                              'Budget-normalized relative contributions are never inputs to the welfare formula'])
    (out / 'audit.json').write_text(json.dumps(audit, indent=2, allow_nan=False) + '\n')
    print(frames['benefit_grid_summary'].to_string(index=False))
    return audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=HERE / 'derived')
    parser.add_argument('--fiscal-response', type=Path)
    args = parser.parse_args()
    build(args.source_root.resolve(), args.out.resolve(), args.fiscal_response)

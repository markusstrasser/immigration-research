"""Point-estimate audit; writes only this audit's ignored _cache directory.

Recalibrate the adopted two-skill CES under the adopted row-4 weights and
existing hot-deck seeds. These are diagnostic scenarios, not new identified
effects. The matched-over-pooled analogue is explicitly a ratio adjustment of
each national/target skill total, since no such production estimator is adopted.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
F = ROOT / 'infra/immigration-fiscal'
LANE = F / 'cps_imputation_keys_2026_09_23'
sys.path.insert(0, str(LANE))
sys.path.insert(0, str(F / 'matched_benefits_2026_09_19'))
import common as c
import hotdeck
from model import equilibrium, fiscal_and_private

source_paths = [LANE / 'common.py', LANE / 'hotdeck.py', LANE / 'taxcalc.py',
                LANE / '_cache/asec25_lane.parquet', F / 'matched_benefits_2026_09_19/model.py',
                F / 'dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet',
                F / 'matched_benefits_2026_09_19/derived/scenarios.csv',
                F / 'assumption_explorer_2026_09_21/derived/model.json',
                F / 'main_case_long_run_2026_09_27/derived/corrections.json']
pins = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
d = pd.read_parquet(LANE / '_cache/asec25_lane.parquet')
civ, target = c.masks(d)
weights = d.pwwgt0.to_numpy(float)
earn0 = d.PEARNVAL.to_numpy(float)
earn_sum = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
assert np.array_equal(earn0, earn_sum), 'PEARNVAL not equal to component sum'
assert abs(weights[target].sum() - c.TARGET_POP) < .01
skill = [d.A_HGA.between(31, 39).to_numpy(), d.A_HGA.between(40, 46).to_numpy()]

acs = pd.read_parquet(source_paths[5], columns=['ST', 'RELSHIPP', 'POBP', 'CIT', 'PWGTP'])
acs = acs[acs.RELSHIPP.ne(37) & acs.POBP.eq(303) & acs.CIT.isin([4, 5]) & ~acs.ST.isin([6, 48])]
w4 = weights.copy()
factors = {}
for status, label in [(4, 'naturalized'), (5, 'noncitizen')]:
    mask = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
    desired = float(acs.loc[acs.CIT.eq(status), 'PWGTP'].sum())
    factor = desired / weights[mask].sum()
    w4[mask] *= factor
    factors[label] = dict(records=int(mask.sum()), cps_population=float(weights[mask].sum()),
                          acs_population=desired, factor=factor)

def totals(frame, w):
    # Hotdeck deliberately does not update PEARNVAL: reconstruct its verified identity.
    earnings = np.maximum((frame.WSAL_VAL + frame.SEMP_VAL + frame.FRSE_VAL).to_numpy(float), 0)
    assert not np.any((earnings > 0) & civ & ~(skill[0] | skill[1]))
    return np.array([[float((earnings * w)[mask & cell].sum()) for cell in skill]
                     for mask in [civ, target]])

def calculate(t):
    national, union = t
    a = national / national.sum()
    m = union / national
    result = equilibrium(a, m, sigma=2, labor_share=.65, adjustment=1, elasticity=0)
    part = fiscal_and_private(result, [.384, .426], .246, 1, 0)
    out = {'national_skill_earnings_bn': (national / 1e9).tolist(),
           'target_skill_earnings_bn': (union / 1e9).tolist(),
           'national_skill_shares': a.tolist(), 'target_efficiency_shares': m.tolist()}
    for normalization, scale in [('cash', national.sum() / .65 / 1e9), ('gdp', 29298.)]:
        out[normalization] = {k: float(v * scale) for k, v in part.items()}
    return out

base = totals(d, weights)
row4 = totals(d, w4)
results = {'published': calculate(base), 'row4_only': calculate(row4)}
stored = pd.read_csv(F / 'matched_benefits_2026_09_19/derived/scenarios.csv')
baseline = stored[(stored.proxy == 'PEARNVAL') & (stored.split == 'hs_or_less')
                  & np.isclose(stored.labor_share, .65) & np.isclose(stored.sigma, 2)
                  & np.isclose(stored.capital_adjustment, 1)
                  & np.isclose(stored.labor_supply_elasticity, 0)
                  & np.isclose(stored.capital_tax_retention, 1)
                  & (stored.tax_classification_transport == 'source_split')]
for normalization in ('cash', 'gdp'):
    check = baseline[baseline.normalization == normalization]
    assert len(check) == 1, 'Published production baseline is not unique'
    for key, value in results['published'][normalization].items():
        assert abs(value - float(check.iloc[0][key + '_estimate']) / 1e9) < 1e-7, key
seeds = list(range(20260923, 20260928))
per_seed = []
for seed in seeds:
    matched, _ = hotdeck.run(d, seed=seed, verbose=False, base=hotdeck.BASE, item_property=False)
    pooled, _ = hotdeck.run(d, seed=seed, verbose=False, base=[], item_property=False)
    m, p = totals(matched, w4), totals(pooled, w4)
    per_seed.append({'seed': seed, 'matched': calculate(m), 'pooled': calculate(p),
                     'ratio_adjusted_diagnostic': calculate(row4 * m / p)})
    print('finished seed', seed, flush=True)
for method in ['matched', 'pooled', 'ratio_adjusted_diagnostic']:
    results[method] = {normalization: {
        k: float(np.mean([r[method][normalization][k] for r in per_seed]))
        for k in per_seed[0][method][normalization]}
        for normalization in ['cash', 'gdp']}

# Reproduce the service-price side view with the caller's actual beneficiary bases.
old = F / 'consumer_price_benefit_2026_09_18/derived'
new = F / 'care_household_services_2026_09_23/derived'
side_paths = [old / 'expenditure_map.csv', old / 'compute_audit.json',
              old / 'native_lowskill_base.csv', new / 'partA_side_view_union_frame.csv',
              new.parent / 'hours_tax.py']
expenditures = pd.read_csv(side_paths[0])
consumer_units = json.loads(side_paths[1].read_text())['native_consumer_units']
native_wage_base = pd.read_csv(side_paths[2]).set_index('group').loc[
    'native_dropout_employed', 'aggregate_earnings_bn']
side = pd.read_csv(side_paths[3]).query(
    "price_arm == 'jpe_2008_2pct' and shock == 'union_national'").iloc[0]
price = np.exp(np.log(.98) / np.log(1.1) * side.dln_share) - 1
consumer = sum(expenditures.loc[expenditures.tier.eq('intensive'), q].sum() * count
               for q, count in consumer_units.items()) * price / 1e9
wage = native_wage_base * (np.exp(np.log(.994) / np.log(1.1) * side.dln_share) - 1)
assert max(abs(consumer - side.consumer_loss_narrow_bn),
           abs(wage - side.native_dropout_wage_gain_bn)) < 1e-10
sideview = {'native_head_scaled_consumer_units': consumer_units,
            'native_dropout_earnings_bn': float(native_wage_base),
            'consumer_gain_bn': consumer, 'native_wage_loss_bn': wage,
            'net_bn': consumer - wage,
            'interpretation': 'Native-headed consumer units and all native dropout wages '
                              'are retained while the shock changes to the target union.',
            'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in side_paths}}
payload = {'source_hashes': pins, 'definitions': {'population': 'CPS ASEC 2025 civilian Mexican-origin observable union',
           'year': 'income 2024; fixed full-adjustment two-skill CES',
           'national_denominator': 'positive person earnings within civilian skill groups; no national re-raking after row4',
           'sampling': 'point estimates only; seed spread is not a survey-design interval',
           'hotdeck_PEARNVAL_identity': 'original PEARNVAL exactly WSAL_VAL + SEMP_VAL + FRSE_VAL; reconstructed after re-imputation',
           'ratio_adjustment': 'diagnostic skill-total ratio analogue only, not an adopted production estimator'},
           'records': len(d), 'target_records': int(target.sum()),
           'populations': {'published': float(weights[target].sum()), 'row4': float(w4[target].sum())},
           'row4_factors': factors, 'results': results, 'seeds': per_seed,
           'service_sideview': sideview}
assert all(pins[str(p.relative_to(ROOT))] == hashlib.sha256(p.read_bytes()).hexdigest()
           for p in source_paths), 'Source changed during the diagnostic'
dest = Path(__file__).resolve().parent / '_cache/production.json'
dest.parent.mkdir(exist_ok=True, parents=True)
dest.write_text(json.dumps(payload, indent=2) + '\n')
print(json.dumps({'populations': payload['populations'], 'row4_factors': factors, 'results': results}, indent=2))

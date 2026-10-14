#!/usr/bin/env python3
"""Pair the source SDR stacks, and price gap changes at fixed per-person amounts."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
OUT = LANE / 'derived'
SOURCE = LANE.parent / 'mixed_unit_removal_2026_10_14'


def sdr(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def main():
    targets = json.loads((OUT / 'comparator_targets.json').read_text())
    live = json.loads((LANE.parent / 'main_case_2026_10_15/derived/summary.json').read_text())['v8']
    bands = pd.read_csv(LANE.parent / 'main_case_2026_10_15/derived/main_case_bands.csv').set_index(['profile', 'variant'])
    for group in targets.values():
        for method, field, variant in [('set', 'band_bn', 'adopted'), ('cash', 'cash_set_bn', 'cash_set')]:
            for i, end in enumerate(('low', 'high')):
                if abs(group[method][end]['case_lineage_cost_bn'] - live[field][i]) > 1e-9:
                    raise SystemExit('[BLOCKED] comparator case-side total differs from live exact case')
                if abs(group[method][end]['case_lineage_cost_bn'] - bands.loc[('long_run_non_school_full', variant), f'cost_{end}_bn']) > 5.01e-5:
                    raise SystemExit('[BLOCKED] comparator case-side total differs from rounded live bands')
                if abs(group[method][end]['lineage_population'] - live['population']['with_coverage']) > 1e-9:
                    raise SystemExit('[BLOCKED] comparator complete denominator differs from live case')
    source = pd.read_csv(SOURCE / 'derived/round2_replicates.csv')
    gaps, components = [], []
    for group in ('white', 'black'):
        result = json.loads((OUT / f'{group}_summary.json').read_text())
        reps = pd.read_csv(OUT / f'{group}_replicates.csv')
        for row in result['results']:
            for component, values in row['parts'].items():
                components.append({'group': group, 'method': row['method'], 'end': row['end'], 'reading': row['reading'],
                                   'component': component, **values})
        for method in ('set', 'cash'):
            for end, reading in [('low', 'bounded_low'), ('high', 'bounded_high')]:
                own = targets[group][method][end]
                row = next(r for r in result['results'] if (r['method'], r['end'], r['reading']) == (method, end, reading))
                comparator = reps.query('method == @method and end == @end and component == @reading').iloc[0, 3:].to_numpy(float)
                lineage = source.query('method == @method and end == @end and component == @reading').iloc[:, 4:].sum().to_numpy(float)
                for basis, scale in [('own_count', 1.), ('lineage_count', own['lineage_population'] / own['population'])]:
                    correction = row['bn'] * scale
                    paired = lineage - scale * comparator
                    oldgap = own['rough_lineage_cost_bn'] - own['cost_bn'] * scale
                    exactgap = own['case_lineage_cost_bn'] - own['cost_bn'] * scale
                    gaps.append({'group': group, 'method': method, 'end': end, 'reading': reading, 'population_basis': basis,
                        'specification': own['specification'], 'comparator_own_count': own['population'],
                        'lineage_count': own['lineage_population'], 'standardization_factor': scale,
                        'comparator_adjustment_bn': correction, 'comparator_adjustment_se_bn': row['se_bn'] * scale,
                        'one_sided_rough_gap_bn': oldgap, 'both_sided_rough_gap_bn': oldgap - correction,
                        'one_sided_case_gap_bn': exactgap, 'both_sided_case_gap_bn': exactgap - correction,
                        'change_from_current_one_sided_gap_bn': -correction,
                        'item11_net_change_from_neither_side_bn': float(paired[0]), 'item11_paired_se_bn': sdr(paired)})
    pd.DataFrame(components).to_csv(OUT / 'components.csv', index=False, lineterminator='\n', float_format='%.12f')
    pd.DataFrame(gaps).to_csv(OUT / 'gaps.csv', index=False, lineterminator='\n', float_format='%.12f')
    (OUT / 'gaps.json').write_text(json.dumps(gaps, indent=2, allow_nan=False) + '\n')
    lines = ['**Verdict:** The comparator mixed-unit adjustments are computed with the frozen source survivor kernels and exact comparator masks. The lineage control reproduces every part, paired SE and replicate before admitting comparators. [CALCULATION: `adapter.py`; `derived/positive_control.json`]', '',
        'Income-year 2024, current oct15 comparator ends, personal allocation. Positive adjustments raise the comparator\'s modeled net cost to other residents and reduce the lineage-minus-comparator gap. These are conditional simulations, not observed removals. [FRAMING-SENSITIVE] [ASSUMPTION]', '',
        '| Comparator, own count | Bounded low, $bn | Bounded high, $bn | SE low / high, $bn |', '|---|---:|---:|---:|']
    for group in ('white', 'black'):
        result = json.loads((OUT / f'{group}_summary.json').read_text())
        low, high = [next(r for r in result['results'] if r['method'] == 'set' and r['end'] == e and r['reading'] == a) for e, a in [('low', 'bounded_low'), ('high', 'bounded_high')]]
        lines.append(f"| {group} | {low['bn']:+.6f} | {high['bn']:+.6f} | {low['se_bn']:.6f} / {high['se_bn']:.6f} |")
    lines += ['', 'All table numbers: [CALCULATION: `derived/{white,black}_summary.json` `results`]. Set and cash use the same current-year survivor terms; no spousal-pension model is added. Both readings at each endpoint and all component/diagnostic stacks appear in the JSON/CSV outputs. [ASSUMPTION]', '', '## Definitions and populations', '',
        'A1 whites: civilian (`PRPERTYP==2` or age under 15), non-Hispanic (`PEHSPNON==2`), white alone (`PRDTRACE==1`), native (`PRCITSHP` 1/2/3), with both parents born in US areas (57/60/66/69/73/78). All ages, third-plus definition, own age mix. [DATA: `../white_replacement_2026_09_28/rekey_white.py:68-79`; `rekey_sept29.py:1299`]', '',
        'Black: civilian, non-Hispanic (`PEHSPNON==2`), Black alone (`PRDTRACE==2`); all ages, generations and birthplaces, own count. [DATA: `../black_comparator_rough_2026_09_28/rekey.py:41-48`; `../white_replacement_2026_09_28/rekey_white.py:76`]', '',
        'The original union is used to construct row-4 national weights before swapping the group mask. Comparators never inherit the Mexican union\'s completion, added residual or Hispanic coverage construction. Paired uncertainty retains all signed SDR columns. Ownership is stored in the third source row as a computational slot; no Black generation classification is inferred. [CALCULATION: `adapter.py` `frame`, `membership`]', '',
        '| Comparator | Own members, records / weighted | Mixed members, records / weighted | Staying civilian nonmembers, records / weighted | Outside biological children, records / weighted |', '|---|---:|---:|---:|---:|']
    for group in ('white', 'black'):
        counts = json.loads((OUT / f'{group}_summary.json').read_text())['counts']
        cells = [counts[k] for k in ('members', 'members_in_mixed_units', 'nonmembers_staying_in_mixed_units', 'all_biological_children_outside_group_stay')]
        lines.append('| ' + group + ' | ' + ' | '.join(f"{r['records']:,} / {r['weighted_persons']:,.6f}" for r in cells) + ' |')
    lines += ['', 'Counts: [DATA / CALCULATION: `derived/{white,black}_summary.json` `counts`]. Weighted counts and record counts refer to these civilian masks; noncivilian co-residents are disclosed separately in the JSON.', '',
        'M6: a biological child outside the comparator definition stays. Biological links (`PEPAR1TYP`/`PEPAR2TYP==1`, under-18 native civilian child outside the mask) are counted with the source\'s keyed roster function, but do not expand departures. Their taxes/benefits therefore already enter the ordinary survivor solve. The incremental M6 membership change and membership-benefit interaction are exactly zero because both masks are identical. D is zero by the requested no-added-residual rule. [DATA: `../mixed_unit_removal_2026_10_14/membership.py:43-62`] [CALCULATION: `adapter.py` `counts`, `tax`] [ASSUMPTION]', '',
        '## Gap changes', '', '| Group / set / population | Current one-sided rough gap, low / high $bn | Both-sided rough gap, low / high $bn | Change, low / high $bn |', '|---|---:|---:|---:|']
    for group in ('white', 'black'):
        for method in ('set', 'cash'):
            for basis in ('own_count', 'lineage_count'):
                pair = [next(r for r in gaps if (r['group'], r['method'], r['population_basis'], r['end']) == (group, method, basis, end)) for end in ('low', 'high')]
                formatted = [' / '.join(f"{r[k]:+.6f}" for r in pair) for k in ('one_sided_rough_gap_bn', 'both_sided_rough_gap_bn', 'change_from_current_one_sided_gap_bn')]
                lines.append('| ' + ' / '.join([group, method, basis]) + ' | ' + ' | '.join(formatted) + ' |')
    lines += ['', 'Gap table: [CALCULATION: `derived/gaps.csv`]. The published comparator central is rough lineage against rough comparator, not the exact case lineage against rough comparator. Both comparisons are supplied in the CSV with explicit names. Population standardization is linear at fixed per-person amounts; it is not a fresh removal of a smaller universe. `item11_paired_se_bn` uses lineage-minus-comparator signed replicate vectors, not SE quadrature. The SE for changing the already one-sided gap is the comparator correction\'s SE. [CALCULATION: `finalize.py`] [ASSUMPTION]', '',
        '## Calibration and limitations', '',
        'Source federal/state/refund kernels retain their national calibration, own-survivor filing status, own IRS cell, actual person flags, residual rules and paired weights. The comparator has no previously booked item 5b, so its subtraction vector is zero. The national source IRS/refund calibration remains conditioned. Unobserved deductions, QBI and care attribution remain source assumptions. [CALCULATION: `adapter.py` `tax`; source `removal.py:273-393`; source `state_tax.py:166-354`] [ASSUMPTION]', '',
        'M5 uses each comparator\'s own-count amount from the live comparator evaluator, including state sales/excise pricing and the actual owner-property response. Its relative change uses the source\'s saving/remittance-adjusted SPM consumption and state-rate/owner-tenure property allocator. The rough comparator baseline uses an income-power household consumption proxy and a property-value proxy; transporting source allocator relative movements to those amounts is an explicit calibration bridge, not equality of raw keys. SNAP/housing retain their reported unit pools. Source model-share declarations are rederived for each mask without changing national totals. [DATA: `../white_replacement_2026_09_28/rekey_white.py:97-119,266-284`; `rekey_sept29.py:973-1068`] [CALCULATION: `derived/comparator_targets.json`; `adapter.py` `declaration_model`] [ASSUMPTION]', '',
        'Health/takeup/shelter models and prices are the frozen source\'s. Membership-benefit terms are solved on the comparator departure mask, while M5 SNAP and its baseline interaction cancel exactly. Conditional SDR SEs omit policy, takeup, cost-vintage and calibration uncertainty; the bounded-low/high readings are model scenarios, not confidence limits. Current consumption resources are held rather than responding behaviorally to new taxes or benefits. Source spousal-pension alternatives stay beside the unified reading. [ASSUMPTION]', '',
        'The LLM-assisted analysis can inherit political framing bias. Executable controls verify implementation and accounting, not the removal counterfactual\'s causal premises. [INFERENCE]', '',
        '## Reproduce', '', 'From the repository root:', '```sh', 'sh infra/immigration-fiscal/mixed_unit_comparators_2026_10_15/run_all.sh', 'uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/mixed_unit_comparators_2026_10_15 "sh {lane}/run_all.sh"', '```', '',
        'Every process gates its own peak physical footprint through the existing memory-budget helper. Python perf_counter/getrusage receipts append only in ignored `_cache/timing.jsonl`. Source bytes are checked before and after execution; no source/comparator producer lane or Git metadata is edited. [CALCULATION: `adapter.py`; `derived/source_fingerprints.json`]', '']
    lines += ['## Adapter conventions', '',
        'The child-count table includes every under-18 civilian outside the group with a type-1 biological member parent, regardless of citizenship. The source-native subset is also reported separately in the JSON. Both subsets stay; neither changes departure membership. [CALCULATION: `adapter.py` `counts`] [DATA: `derived/{white,black}_summary.json`]', '',
        'The comparator full weight is MARSUPWT/100 with its exact live row-4 factors; national federal/refund denominators are recomputed on that column. Source signed SDR columns are unchanged. The source control retains its own pwwgt0 full weight. These conventions keep the comparator own-count gate exact rather than loosening it. [DATA: `derived/comparator_weight_rule.json`] [CALCULATION: `adapter.py` `comparator_weights`, `tax`]', '',
        'For a new nonfiler claimant, the state adapter aligns a zero-income/dependent before-return, gated to zero booked CPS state tax, with the actual after-return. The added row creates no original income or tax calibration mass; income, dependents, weights and ownership enter only after removal. [CALCULATION: `adapter.py` `state_registry`; `test_adapter.py`]', '',
        'The white own-count baseline is a linear standardization of the published A1 per-person prices. A fresh natural unscaled MEPS universe uses different prices, recorded separately as `natural_unscaled_universe_cost_bn`; it does not replace that baseline. The comparator M5 amounts are CPS-keyed and are computed at own count before standardizing the adjustment. [DATA: `derived/comparator_targets.json`] [CALCULATION: `adapter.py` `prepare`] [ASSUMPTION]', '',
        'The exact case-side totals and complete denominator gate against the live JSON at 1e-9; the adopted/cash_set CSV rows gate at their four-decimal rounding tolerance. [CALCULATION: `finalize.py`]', '']
    (LANE / 'RESULT.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()

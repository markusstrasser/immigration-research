#!/usr/bin/env python3
"""Pair the source SDR stacks, and price gap changes at fixed per-person amounts."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
OUT = LANE / 'derived'
SOURCE = LANE.parent / 'mixed_unit_removal_2026_10_14'
from adapter import GROUPS as SOLVED_GROUPS, digest

GROUPS = tuple(g for g in SOLVED_GROUPS if not g.startswith('lineage_'))


def sdr(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def source_vector(source, method, end, reading):
    rows = source.query('method == @method and end == @end and component == @reading')
    if len(rows) != 3 or set(rows.generation) != {'G1', 'G2', 'G3+'}:
        raise SystemExit('[BLOCKED] source item11 needs exactly its three generation vectors')
    values = rows[[f'r{i}' for i in range(161)]].to_numpy(float)
    if not np.isfinite(values).all():
        raise SystemExit('[BLOCKED] source item11 replicate vector is nonfinite')
    return values.sum(axis=0)


def completion_credit_already_booked():
    """The completed reporter crossing-credit change already sits in item 10."""
    path = LANE.parent / 'union_completion_2026_10_14/derived/credits_interaction.json'
    case = LANE.parent / 'main_case_2026_10_15/derived/corrections.json'
    record = json.loads(path.read_text())['results']['one_us_parent_plus_observed']
    v = np.asarray(record['replicate_delta_bn'], float)
    meta = json.loads(case.read_text())['meta']['union_completion']
    target = meta['credit_interaction_bn']
    source_hash = digest(path)
    if source_hash != meta['source_hashes'][str(path.relative_to(LANE.parent))]:
        raise SystemExit('[BLOCKED] completion crossing-credit source differs from case source pin')
    if len(v) != 161 or not np.isfinite(v).all() or abs(v[0] - target) > 1e-12 or abs(record['delta_bn'] - target) > 1e-12:
        raise SystemExit('[BLOCKED] completion crossing-credit vector differs from live item10')
    receipt = {'path': str(path.relative_to(LANE.parent.parent.parent)), 'sha256': source_hash,
               'case_path': str(case.relative_to(LANE.parent.parent.parent)), 'case_sha256': digest(case),
               'already_booked_bn': float(v[0]), 'subtraction_bn': float(-v[0]), 'replicates': len(v)}
    return v, receipt


def subtract_completion_credit(delta):
    v, receipt = completion_credit_already_booked()
    delta = delta.copy()
    for method in ('set', 'cash'):
        for end in ('low', 'high'):
            for reading in ('bounded_low', 'bounded_high'):
                delta.loc[(method, end, reading)] -= v
            delta.loc[(method, end, 'completion_credit_already_booked'), :] = -v
    return delta, receipt


def lineage_delta():
    """Increment the frozen bounded source term with a fully paired mask change.

    D and the old credit subtraction stay in the frozen source term once. The
    adapter's two solves share weights, tax calibration, state and resource keys.
    """
    source = pd.read_csv(SOURCE / 'derived/round2_replicates.csv')
    current = pd.read_csv(OUT / 'lineage_current_replicates.csv').set_index(['method', 'end', 'component'])
    expanded = pd.read_csv(OUT / 'lineage_children_replicates.csv').set_index(['method', 'end', 'component'])
    if not current.index.equals(expanded.index):
        raise SystemExit('[BLOCKED] lineage paired solve component keys differ')
    delta, credit_receipt = subtract_completion_credit(expanded - current)
    delta.reset_index().to_csv(OUT / 'lineage_children_delta_replicates.csv', index=False,
        lineterminator='\n', float_format='%.15g')
    rows = []
    total_vectors = []
    for method in ('set', 'cash'):
        for end in ('low', 'high'):
            for reading in ('bounded_low', 'bounded_high'):
                move = delta.loc[(method, end, reading)].to_numpy(float)
                original = source_vector(source, method, end, reading)
                combined = original + move
                rows.append({'method': method, 'end': end, 'reading': reading,
                    'delta_bn': float(move[0]), 'delta_se_bn': sdr(move),
                    'source_item11_bn': float(original[0]), 'bn': float(combined[0]), 'se_bn': sdr(combined),
                    'diagnostic_component_deltas': {k[2]: {'bn': float(delta.loc[k].iloc[0]),
                                    'se_bn': sdr(delta.loc[k].to_numpy(float))}
                              for k in delta.index if k[:2] == (method, end) and k[2] not in ('bounded_low', 'bounded_high')}})
                total_vectors.append({'method': method, 'end': end, 'component': reading,
                                      **{f'r{i}': float(v) for i, v in enumerate(combined)}})
    pd.DataFrame(total_vectors).to_csv(OUT / 'lineage_children_total_replicates.csv', index=False,
        lineterminator='\n', float_format='%.15g')
    (OUT / 'lineage_children_delta_summary.json').write_text(json.dumps({
        'interpretation': 'source item11 plus expanded-minus-current full adapter solve, less already-booked item10 crossing credit; D and original credit subtraction retained once',
        'completion_credit_already_booked': credit_receipt,
        'results': rows}, indent=2, allow_nan=False) + '\n')
    return rows


def interpolate_comparator_halves():
    """Half of the overlapping record's weight and computed endpoint cost.

    This is explicitly an interpolation of discrete endpoint simulations;
    half-person tax filing statuses are not observed or simulated.
    """
    for base in ('white', 'black'):
        central = pd.read_csv(OUT / f'{base}_children_replicates.csv').set_index(['method', 'end', 'component'])
        raw = pd.read_csv(OUT / f'{base}_children_round3_replicates.csv').set_index(['method', 'end', 'component'])
        if not central.index.equals(raw.index):
            raise SystemExit('[BLOCKED] half-rule comparator endpoint component keys differ')
        half = ((central + raw) / 2).copy()
        central_json = json.loads((OUT / f'{base}_children_summary.json').read_text())
        raw_json = json.loads((OUT / f'{base}_children_round3_summary.json').read_text())
        rows = []
        for method, end, reading in half.index:
            if reading not in ('bounded_low', 'bounded_high'):
                continue
            v = half.loc[(method, end, reading)].to_numpy(float)
            ca, ra = [next(r for r in source['results'] if (r['method'], r['end'], r['reading']) == (method, end, reading))
                      for source in (central_json, raw_json)]
            csel = dict(zip(('Medicaid', 'ACA', 'SNAP'), ca['arm'].split('|')))
            rsel = dict(zip(('Medicaid', 'ACA', 'SNAP'), ra['arm'].split('|')))
            parts = {}
            for part in ca['parts']:
                pv = (central.loc[(method, end, csel.get(part, part))].to_numpy(float)
                      + raw.loc[(method, end, rsel.get(part, part))].to_numpy(float)) / 2
                parts[part] = {'bn': float(pv[0]), 'se_bn': sdr(pv)}
                if part in csel:
                    half.loc[(method, end, f'half_{part}_{reading}'), :] = pv
            if abs(sum(p['bn'] for p in parts.values()) - v[0]) > 1e-9:
                raise SystemExit('[BLOCKED] half-rule selected components do not close')
            rows.append({'method': method, 'end': end, 'reading': reading, 'bn': float(v[0]), 'se_bn': sdr(v),
                'arm': '|'.join(f'half_{part}_{reading}' for part in ('Medicaid', 'ACA', 'SNAP')), 'parts': parts})
        half.reset_index().to_csv(OUT / f'{base}_children_half_replicates.csv', index=False,
            lineterminator='\n', float_format='%.15g')
        counts = {}
        for k, a in central_json['counts'].items():
            b = raw_json['counts'].get(k)
            if isinstance(a, dict) and isinstance(b, dict) and 'replicate_counts' in a:
                v = (np.asarray(a['replicate_counts']) + np.asarray(b['replicate_counts'])) / 2
                counts[k] = {'weighted_persons': float(v[0]), 'replicate_counts': v.tolist(),
                    'records': (a['records'] + b['records']) / 2,
                    'central_records': a['records'], 'round3_records': b['records']}
        (OUT / f'{base}_children_half_summary.json').write_text(json.dumps({
            'group': base + '_children_half', 'interpretation': 'half of central precedence and round3 endpoint costs and weights; conditional interpolation',
            'counts': counts, 'results': rows}, indent=2, allow_nan=False) + '\n')


def interpolate_lineage_halves():
    """The lineage side of each half-overlap comparison has its own endpoint."""
    current = pd.read_csv(OUT / 'lineage_current_replicates.csv').set_index(['method', 'end', 'component'])
    full = pd.read_csv(OUT / 'lineage_children_replicates.csv').set_index(['method', 'end', 'component'])
    source = pd.read_csv(SOURCE / 'derived/round2_replicates.csv')
    for base in ('white', 'black'):
        without = pd.read_csv(OUT / f'lineage_without_{base}_overlap_replicates.csv').set_index(['method', 'end', 'component'])
        if not full.index.equals(without.index) or not full.index.equals(current.index):
            raise SystemExit('[BLOCKED] half-rule lineage endpoint component keys differ')
        delta, credit_receipt = subtract_completion_credit((full + without) / 2 - current)
        delta.reset_index().to_csv(OUT / f'lineage_half_{base}_delta_replicates.csv', index=False,
            lineterminator='\n', float_format='%.15g')
        rows, vectors = [], []
        for method, end, reading in delta.index:
            if reading not in ('bounded_low', 'bounded_high'):
                continue
            move = delta.loc[(method, end, reading)].to_numpy(float)
            original = source_vector(source, method, end, reading)
            v = original + move
            rows.append({'method': method, 'end': end, 'reading': reading,
                'delta_bn': float(move[0]), 'delta_se_bn': sdr(move), 'source_item11_bn': float(original[0]),
                'bn': float(v[0]), 'se_bn': sdr(v)})
            vectors.append({'method': method, 'end': end, 'component': reading,
                            **{f'r{i}': float(x) for i, x in enumerate(v)}})
        pd.DataFrame(vectors).to_csv(OUT / f'lineage_half_{base}_total_replicates.csv', index=False,
            lineterminator='\n', float_format='%.15g')
        (OUT / f'lineage_half_{base}_summary.json').write_text(json.dumps({
            'interpretation': 'source item11 plus half full-expanded and half without-comparator-overlap, less current adapter baseline and already-booked item10 crossing credit',
            'completion_credit_already_booked': credit_receipt,
            'results': rows}, indent=2, allow_nan=False) + '\n')


def main():
    targets = json.loads((OUT / 'comparator_targets.json').read_text())
    member_file = LANE.parent / 'white_replacement_2026_09_28/derived/members_coverage_oct15.json'
    member_runs = json.loads(member_file.read_text())['runs']
    for base in ('white', 'black'):
        entries = {}
        for method in ('set', 'cash'):
            entries[method] = {}
            for end in ('low', 'high'):
                a, b = (targets[base + suffix][method][end] for suffix in ('_children', '_children_round3'))
                overlap = [r for r in member_runs if (r['scenario'], r['coverage'], r['mortality'], r['basis'], r['end'])
                    == ('overlap_' + base, 'none', 'general', 'accrual' if method == 'set' else 'cash', end)]
                if len(overlap) != 1:
                    raise SystemExit('[BLOCKED] half lineage overlap count does not have a unique source row')
                lines = {}
                for lid, line in a['lines'].items():
                    lines[lid] = {k: ((v + b['lines'][lid][k]) / 2 if isinstance(v, (int, float)) else v)
                                  for k, v in line.items()}
                entries[method][end] = {'population': (a['population'] + b['population']) / 2,
                    'cost_bn': (a['cost_bn'] + b['cost_bn']) / 2, 'specification': a['specification'],
                    'lineage_population': a['lineage_population'] - .5 * overlap[0]['population'],
                    'lines': lines, 'interpretation': 'half central and half round3 own-count targets; lineage half cost/count supplied by producer'}
        targets[base + '_children_half'] = entries
    (OUT / 'comparator_targets.json').write_text(json.dumps(targets, indent=2, allow_nan=False) + '\n')
    (OUT / 'half_count_source.json').write_text(json.dumps({'path': str(member_file.relative_to(LANE.parent.parent.parent)),
        'sha256': digest(member_file), 'reading': 'overlap_{white,black}, none coverage, general mortality; half subtracted from full lineage count'},
        indent=2) + '\n')
    live = json.loads((LANE.parent / 'main_case_2026_10_15/derived/summary.json').read_text())['v8']
    bands = pd.read_csv(LANE.parent / 'main_case_2026_10_15/derived/main_case_bands.csv').set_index(['profile', 'variant'])
    for name, group in targets.items():
        if name.startswith('lineage_') or name.endswith('_half'):
            continue   # Fixed-calibration delta targets are not independent whole-case oracles.
        for method, field, variant in [('set', 'band_bn', 'adopted'), ('cash', 'cash_set_bn', 'cash_set')]:
            for i, end in enumerate(('low', 'high')):
                # Children-rule groups carry the lineage's own outside children as a block on the lineage side.
                block = group[method][end].get('lineage_children_block', {'cost_bn': 0., 'population': 0.})
                case = group[method][end]['case_lineage_cost_bn'] - block['cost_bn']
                if abs(case - live[field][i]) > 1e-9:
                    raise SystemExit('[BLOCKED] comparator case-side total differs from live exact case')
                if abs(case - bands.loc[('long_run_non_school_full', variant), f'cost_{end}_bn']) > 5.01e-5:
                    raise SystemExit('[BLOCKED] comparator case-side total differs from rounded live bands')
                if abs(group[method][end]['lineage_population'] - block['population'] - live['population']['with_coverage']) > 1e-6:
                    raise SystemExit('[BLOCKED] comparator complete denominator differs from live case')
    lineage_changes = lineage_delta()
    interpolate_comparator_halves()
    interpolate_lineage_halves()
    source = pd.read_csv(SOURCE / 'derived/round2_replicates.csv')
    expanded_source = pd.read_csv(OUT / 'lineage_children_total_replicates.csv')
    gaps, components = [], []
    for group in GROUPS:
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
                change = next(r for r in lineage_changes if (r['method'], r['end'], r['reading']) == (method, end, reading))
                expanded_rule = '_children' in group
                lineage = (expanded_source.query('method == @method and end == @end and component == @reading').iloc[0, 3:].to_numpy(float)
                           if expanded_rule else source_vector(source, method, end, reading))
                for basis, scale in [('own_count', 1.), ('lineage_count', own['lineage_population'] / own['population'])]:
                    correction = row['bn'] * scale
                    paired = lineage - scale * comparator
                    oldgap = own['rough_lineage_cost_bn'] - own['cost_bn'] * scale
                    exactgap = own['case_lineage_cost_bn'] - own['cost_bn'] * scale
                    lineage_move = change['delta_bn'] if expanded_rule else 0.
                    gaps.append({'group': group, 'method': method, 'end': end, 'reading': reading, 'population_basis': basis,
                        'specification': own['specification'], 'comparator_own_count': own['population'],
                        'lineage_count': own['lineage_population'], 'standardization_factor': scale,
                        'comparator_adjustment_bn': correction, 'comparator_adjustment_se_bn': row['se_bn'] * scale,
                        'lineage_expanded_item11_delta_bn': lineage_move,
                        'lineage_item11_bn': float(lineage[0]), 'lineage_item11_se_bn': sdr(lineage),
                        'comparison_lineage_cost_bn': own['case_lineage_cost_bn'] + lineage_move,
                        'one_sided_rough_gap_bn': oldgap, 'both_sided_rough_gap_bn': oldgap + lineage_move - correction,
                        'one_sided_case_gap_bn': exactgap, 'both_sided_case_gap_bn': exactgap + lineage_move - correction,
                        'change_from_current_one_sided_gap_bn': lineage_move - correction,
                        'item11_net_change_from_neither_side_bn': float(paired[0]), 'item11_paired_se_bn': sdr(paired)})
    for group in ('white_children_half', 'black_children_half'):
        base = group.split('_')[0]
        result = json.loads((OUT / f'{group}_summary.json').read_text())
        reps = pd.read_csv(OUT / f'{group}_replicates.csv')
        lineage_reps = pd.read_csv(OUT / f'lineage_half_{base}_total_replicates.csv')
        for row in result['results']:
            for component, values in row['parts'].items():
                components.append({'group': group, 'method': row['method'], 'end': row['end'], 'reading': row['reading'],
                                   'component': component, **values})
        for method in ('set', 'cash'):
            for end, reading in [('low', 'bounded_low'), ('high', 'bounded_high')]:
                own = targets[group][method][end]
                row = next(r for r in result['results'] if (r['method'], r['end'], r['reading']) == (method, end, reading))
                cv = reps.query('method == @method and end == @end and component == @reading').iloc[0, 3:].to_numpy(float)
                lv = lineage_reps.query('method == @method and end == @end and component == @reading').iloc[0, 3:].to_numpy(float)
                for basis, scale in [('own_count', 1.), ('lineage_count', own['lineage_population'] / own['population'])]:
                    gaps.append({'group': group, 'method': method, 'end': end, 'reading': reading, 'population_basis': basis,
                        'specification': own['specification'], 'comparator_own_count': own['population'],
                        'lineage_count': own['lineage_population'], 'standardization_factor': scale,
                        'comparator_adjustment_bn': row['bn'] * scale, 'comparator_adjustment_se_bn': row['se_bn'] * scale,
                        'lineage_item11_bn': float(lv[0]), 'lineage_item11_se_bn': sdr(lv),
                        'item11_net_change_from_neither_side_bn': float((lv - cv * scale)[0]),
                        'item11_paired_se_bn': sdr(lv - cv * scale),
                        'whole_gap_status': 'not computed here: producer owns direct half-lineage costs'})
    pd.DataFrame(components).to_csv(OUT / 'components.csv', index=False, lineterminator='\n', float_format='%.12f')
    pd.DataFrame(gaps).to_csv(OUT / 'gaps.csv', index=False, lineterminator='\n', float_format='%.12f')
    (OUT / 'gaps.json').write_text(json.dumps(gaps, indent=2, allow_nan=False) + '\n')
    lines = ['**Verdict:** The comparator mixed-unit adjustments are computed with the frozen source survivor kernels and exact comparator masks. The lineage control reproduces every part, paired SE and replicate before admitting comparators. [CALCULATION: `adapter.py`; `derived/positive_control.json`]', '',
        'Income-year 2024, current oct15 comparator ends, personal allocation. Positive adjustments raise the comparator\'s modeled net cost to other residents and reduce the lineage-minus-comparator gap. These are conditional simulations, not observed removals. [FRAMING-SENSITIVE] [ASSUMPTION]', '',
        '| Comparator, own count | Bounded low, $bn | Bounded high, $bn | SE low / high, $bn |', '|---|---:|---:|---:|']
    for group in GROUPS:
        result = json.loads((OUT / f'{group}_summary.json').read_text())
        low, high = [next(r for r in result['results'] if r['method'] == 'set' and r['end'] == e and r['reading'] == a) for e, a in [('low', 'bounded_low'), ('high', 'bounded_high')]]
        lines.append(f"| {group} | {low['bn']:+.6f} | {high['bn']:+.6f} | {low['se_bn']:.6f} / {high['se_bn']:.6f} |")
    lines += ['', '2026-10-15, round 4: central `white_children` / `black_children` exclude every observed member of the completed lineage and its biological-child universe, including lineage children who already satisfy the comparator base definition. The same keyed rule is shared with the white producer in `membership_rules.py`. `*_children_round3` retain the previous overlap rule beside. The original lineage source control remains byte-identical across all 122 exported rows. [CALCULATION: `adapter.py`; `derived/positive_control.json`]', '',
        '| Expanded lineage, source item 11 plus full solve delta | Item 11 low / high, $bn | Delta low / high, $bn | Item 11 SE low / high, $bn |',
        '|---|---:|---:|---:|']
    for method in ('set', 'cash'):
        pair = [next(r for r in lineage_changes if (r['method'], r['end'], r['reading']) == (method, e, a))
                for e, a in [('low', 'bounded_low'), ('high', 'bounded_high')]]
        lines.append('| ' + method + ' | ' + ' | '.join(' / '.join(f"{r[k]:+.6f}" for r in pair)
                     for k in ('bn', 'delta_bn', 'se_bn')) + ' |')
    lines += ['', 'The lineage delta jointly solves federal/state taxes, refunds, health, SNAP, consumption, owner property and housing on the completed expanded mask with the same adapter as comparators. The current baseline matches the source latent tax/benefit departure and original-union M5 resource departure. Its fixed calibration and weights are held between the two solves. The source residual and old credit subtraction remain once in source item 11; only the measured paired delta is added. [CALCULATION: `derived/lineage_children_delta_summary.json`; `derived/lineage_children_delta_replicates.csv`; `derived/lineage_children_total_replicates.csv`]', '',
        'The `*_children_half` files take half of central-precedence and half of overlapping round-3 endpoint weights and survivor costs; paired SEs are recomputed from the averaged signed replicate vectors. Each lineage half file similarly averages its full expanded endpoint and the endpoint retaining that comparator overlap, then differences the source-current baseline. This is a conditional endpoint interpolation. Both full and half lineage changes subtract item 10\'s already-booked crossing-credit vector once, gated at 0.3254843214294949bn and all 161 source columns. [ASSUMPTION] [CALCULATION: `finalize.py` `interpolate_comparator_halves`, `interpolate_lineage_halves`, `completion_credit_already_booked`]']
    lines += ['', 'All table numbers: [CALCULATION: `derived/{white,black}_summary.json` `results`]. Set and cash use the same current-year survivor terms; no spousal-pension model is added. Both readings at each endpoint and all component/diagnostic stacks appear in the JSON/CSV outputs. [ASSUMPTION]', '', '## Definitions and populations', '',
        'A1 whites: civilian (`PRPERTYP==2` or age under 15), non-Hispanic (`PEHSPNON==2`), white alone (`PRDTRACE==1`), native (`PRCITSHP` 1/2/3), with both parents born in US areas (57/60/66/69/73/78). All ages, third-plus definition, own age mix. [DATA: `../white_replacement_2026_09_28/rekey_white.py:68-79`; `rekey_sept29.py:1299`]', '',
        'Black: civilian, non-Hispanic (`PEHSPNON==2`), Black alone (`PRDTRACE==2`); all ages, generations and birthplaces, own count. [DATA: `../black_comparator_rough_2026_09_28/rekey.py:41-48`; `../white_replacement_2026_09_28/rekey_white.py:76`]', '',
        'The original union is used to construct row-4 national weights before swapping the group mask. Comparators never inherit the Mexican union\'s completion, added residual or Hispanic coverage construction. Paired uncertainty retains all signed SDR columns. Ownership is stored in the third source row as a computational slot; no Black generation classification is inferred. [CALCULATION: `adapter.py` `frame`, `membership`]', '',
        '| Comparator | Own members, records / weighted | Mixed members, records / weighted | Staying civilian nonmembers, records / weighted | Outside biological children, records / weighted |', '|---|---:|---:|---:|---:|']
    for group in GROUPS:
        counts = json.loads((OUT / f'{group}_summary.json').read_text())['counts']
        cells = [counts[k] for k in ('members', 'members_in_mixed_units', 'nonmembers_staying_in_mixed_units', 'all_biological_children_outside_group_stay')]
        lines.append('| ' + group + ' | ' + ' | '.join(f"{r['records']:,} / {r['weighted_persons']:,.6f}" for r in cells) + ' |')
    lines += ['', 'Counts: [DATA / CALCULATION: `derived/{white,black}_summary.json` `counts`]. Weighted counts and record counts refer to these civilian masks; noncivilian co-residents are disclosed separately in the JSON.', '',
        'M6: a biological child outside the comparator definition stays. Biological links (`PEPAR1TYP`/`PEPAR2TYP==1`, under-18 native civilian child outside the mask) are counted with the source\'s keyed roster function, but do not expand departures. Their taxes/benefits therefore already enter the ordinary survivor solve. The incremental M6 membership change and membership-benefit interaction are exactly zero because both masks are identical. D is zero by the requested no-added-residual rule. [DATA: `../mixed_unit_removal_2026_10_14/membership.py:43-62`] [CALCULATION: `adapter.py` `counts`, `tax`] [ASSUMPTION]', '',
        '2026-10-15, round 3 (C3 fix 2): `white_children` and `black_children` take one membership rule for all three groups. Members\' biological minor children outside the group depart with them and count as members at their own costs: the same source roster rule, now expanding the departure and the own-count population. The survivor solve, health, SNAP and resource kernels run unchanged on the expanded mask. The groups\' own-count line targets come from the white lane\'s rough engine on the same expanded masks (`../white_replacement_2026_09_28/derived/children_targets_oct15.json`, sha256 in `derived/children_targets_source.json`); their lineage side adds the lineage\'s own 0.336M outside children, outside its latent subset, as a block at their own costs. The rule\'s change in item 11 is the children group\'s amount less the current group\'s. The lineage\'s item 11 stays the source\'s; its all-biological federal-tax arm is the source\'s `M6_all_biological_federal_tax_arm`. Splitting the change by household type would need three more solves per group, because the national pools are not separable by unit; it is not computed. [CALCULATION: `adapter.py` `membership`, `prepare`] [ASSUMPTION]', '',
        '## Gap changes', '', '| Group / set / population | Current one-sided rough gap, low / high $bn | Both-sided rough gap, low / high $bn | Change, low / high $bn |', '|---|---:|---:|---:|']
    for group in GROUPS:
        for method in ('set', 'cash'):
            for basis in ('own_count', 'lineage_count'):
                pair = [next(r for r in gaps if (r['group'], r['method'], r['population_basis'], r['end']) == (group, method, basis, end)) for end in ('low', 'high')]
                formatted = [' / '.join(f"{r[k]:+.6f}" for r in pair) for k in ('one_sided_rough_gap_bn', 'both_sided_rough_gap_bn', 'change_from_current_one_sided_gap_bn')]
                lines.append('| ' + ' / '.join([group, method, basis]) + ' | ' + ' | '.join(formatted) + ' |')
    lines += ['', 'Gap table: [CALCULATION: `derived/gaps.csv`]. These are the base route\'s gaps: the evaluator\'s default settings (whole-population mortality, the original status and production rules, no comparator coverage). They are this lane\'s record of the survivor term, not the comparison central, which is round 3\'s table in the white lane (`../white_replacement_2026_09_28/RESULT.md`, R3C3: children rule, own coverage, own mortality). Each gap is rough lineage against rough comparator, not the exact case lineage against rough comparator. Both comparisons are supplied in the CSV with explicit names. Population standardization is linear at fixed per-person amounts; it is not a fresh removal of a smaller universe. `item11_paired_se_bn` uses lineage-minus-comparator signed replicate vectors, not SE quadrature. The SE for changing the already one-sided gap is the comparator correction\'s SE. [CALCULATION: `finalize.py`] [ASSUMPTION]', '',
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

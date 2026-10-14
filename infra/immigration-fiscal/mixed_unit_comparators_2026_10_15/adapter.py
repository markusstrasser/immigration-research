#!/usr/bin/env python3
"""Frozen survivor kernels on comparator masks; all writes stay in this lane.

Run separate policy children to bound peak memory. No microdata are serialized.
The source's lineage round2.extend is executed as the positive control.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import contextlib
import copy
import cProfile
import hashlib
import importlib.util
import io
import json
import resource
import pstats
import sys
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
SOURCE = FISCAL / 'mixed_unit_removal_2026_10_14'
sys.path.insert(0, str(SOURCE))
OUT = LANE / 'derived'
CACHE = LANE / '_cache'
sys.path.insert(0, str(FISCAL / 'scripts'))
from memory_budget import require_within_budget


def require(ok, name):
    if not ok:
        raise SystemExit('[BLOCKED] ' + name)


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def source_module(name, group):
    module = load(SOURCE / (name + '.py'), 'mixedcomp_' + group + '_' + name)
    # Keep LANE/INPUTS pointing to frozen read-only inputs. Redirect only outputs.
    if hasattr(module, 'OUT'):
        module.OUT = CACHE / group
    if hasattr(module, 'CACHE'):
        module.CACHE = CACHE / group
    return module


def membership(d, civ, group):
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    parents = d.PEFNTVTY.isin([57, 60, 66, 69, 73, 78]).to_numpy() & d.PEMNTVTY.isin([57, 60, 66, 69, 73, 78]).to_numpy()
    if group == 'white':
        mask = civ & native & parents & d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy()
    elif group == 'black':
        mask = civ & d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(2).to_numpy()
    else:
        raise ValueError(group)
    # Source's three-row ownership contract; no comparator generation claim.
    return mask, np.where(mask, 2, -1)


def comparator_weights(d, W):
    """Use comparator MARSUPWT full weights and the source's signed SDR columns."""
    convention = json.loads((OUT / 'comparator_weight_rule.json').read_text())
    full = d.MARSUPWT.to_numpy(float) / 100
    outside = d.PENATVTY.eq(303).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
    for code in (4, 5):
        full[outside & d.PRCITSHP.eq(code).to_numpy()] *= convention['factors'][str(code)]
    W[:, 0] = full
    return W


def join_extra(d, c, fields):
    fields = [f for f in fields if f not in d]
    if fields:
        with zipfile.ZipFile(c.CPS_ZIP) as z:
            extra = pd.read_csv(z.open('pppub25.csv'), usecols=['PH_SEQ', 'PPPOS'] + fields)
        d = d.merge(extra, on=['PH_SEQ', 'PPPOS'], validate='one_to_one', how='left')
        require(not d[fields].isna().any().any(), 'complete extra-column key join')
    return d


def frame(group):
    c = load(FISCAL / 'mixed_unit_credits_2026_10_14/credits.py', 'mixedcomp_frame')
    d = c.load()
    civ, union, gen = c.groups(d)
    # Weight raking is ALWAYS against the original Mexican union; never comparator.
    W, _, _ = c.row4_weights(d, civ, union)
    d = d.drop(columns=c.REPS[1:])
    m = source_module('removal', group)
    d = m.add_fields(d, c)
    h = source_module('health', group)
    d = join_extra(d, c, list(dict.fromkeys(h.EXTRA + ['PEHSPNON', 'PRDTRACE'])))
    if group != 'lineage':
        union, gen = membership(d, civ, group)
        W = comparator_weights(d, W)
    return c, d, W, civ, union, gen


def policy(group, kind, subset):
    c, d, W, civ, union, gen = frame(group)
    if subset == 'latent':
        require(group == 'lineage', 'latent membership only applies to source lineage')
        mem = source_module('membership', group)
        departure = union | mem.latent_mask(d, union, civ)
    else:
        departure = union
    if kind == 'health':
        h = source_module('health', group)
        result = h.compute(d, W, union, gen, {'civ': civ, 'removal_mask': departure})
        terms = dict(result['terms'], Medicaid_low=result['Medicaid_low'], Medicaid_high=result['Medicaid_high'])
    else:
        h = source_module('snap_arm', group)
        model = json.loads(c.MODEL.read_text())
        model = declaration_model(d, civ, union, model)
        dgen = gen.copy()
        dgen[departure & ~union] = 2
        result = h.compute(d, W, departure, dgen, civ, model, baseline_union=union)
        terms = result['terms']
    target = CACHE / group
    target.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(target / f'{kind}_{subset}.npz', **terms)
    write_json(target / f'{kind}_{subset}.json', result['details'])
    if group == 'lineage':
        expected = SOURCE / '_cache' / ({('health', 'union'): 'health_arrays.npz',
            ('health', 'latent'): 'health_latent_arrays.npz', ('snap', 'union'): 'snap_arm_arrays.npz',
            ('snap', 'latent'): 'snap_arm_latent_arrays.npz'}[(kind, subset)])
        with np.load(expected) as old:
            require(set(old.files) == set(terms), 'policy positive control exported terms')
            require(all(np.max(abs(old[k] - terms[k])) < 1e-9 for k in terms), 'policy positive control all columns')


def declaration_model(d, civ, union, model):
    """Declare the new mask's source-key share for kernel retrodiction checks.

    This changes no national amount. It is not a claim that rough comparator
    keys equal the source allocator: amount calibration is separately exported.
    """
    model = copy.deepcopy(model)
    w = d.pwwgt0.to_numpy(float)
    spm = pd.factorize(d.SPM_ID, sort=False)[0]
    hh = pd.factorize(d.PH_SEQ, sort=False)[0]
    parameters = pd.read_csv(FISCAL / 'gen_ledger_extension_2026_09_16/state_parameters.csv').set_index('fips')
    owner = np.where(d.H_TENURE.eq(1), d.GESTFIPS.map(parameters.property_tax_effective_rate).to_numpy() * d.HPROP_VAL.to_numpy(), 0) / np.bincount(hh)[hh]
    keys = {'modeled_owner_property': owner, 'snap': d.SPM_SNAPSUB.to_numpy() / np.bincount(spm)[spm],
            'housing_subsidies': d.SPM_CAPHOUSESUB.to_numpy() / np.bincount(spm)[spm]}
    for side in ('receipts', 'spending'):
        for line in model[side]['lines']:
            if line['id'] in keys:
                values = keys[line['id']]
                share = float(values[union] @ w[union] / (values[civ] @ w[civ]))
                cell = line['cells'][model['receipts']['reference']]['personal'] if side == 'receipts' else line['keys'][line['preferred_key']]['personal']
                cell['share'] = share
    return model


def prepare():
    # Freeze and verify all source-lane bytes, including the immutable pin registry.
    files = sorted(p for p in SOURCE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '_cache' not in p.parts)
    snapshot = {str(p.relative_to(FISCAL)): digest(p) for p in files}
    pin = OUT / 'source_fingerprints.json'
    if pin.exists():
        require(json.loads(pin.read_text()) == snapshot, 'source lane has changed since adapter registration')
    else:
        write_json(pin, snapshot)
    m = source_module('removal', 'lineage')
    registered = m.input_pins()
    write_json(OUT / 'source_pin_check.json', {'passed': True, 'registered_inputs': len(registered), 'source_files': len(files)})
    # Read-only comparator evaluator; no producer main() and no writes to its lane.
    with contextlib.redirect_stdout(io.StringIO()) as log:
        w = load(FISCAL / 'white_replacement_2026_09_28/rekey_sept29.py', 'mixedcomp_comparator')
        w.use_case('oct15')
        w.setup()
        w.stop_if_failed()
        outside = w.R.d.PENATVTY.eq(303).to_numpy() & ~np.isin(w.S.st, [6, 48])
        factors = {}
        for code in (4, 5):
            rows = outside & w.R.d.PRCITSHP.eq(code).to_numpy() & w.R.civ
            ratios = w.R.w[rows] / w.PUBLISHED_W[rows]
            require(np.max(abs(ratios - ratios[0])) < 1e-12, 'single comparator row4 factor per citizenship')
            factors[str(code)] = float(ratios[0])
        write_json(OUT / 'comparator_weight_rule.json', {'full': 'MARSUPWT/100', 'factors': factors,
            'replicates': 'original source row4 signed SDR columns, unchanged', 'full_factor_source': 'rekey_sept29.row4_weights'})
        groups = {}
        for group, code, name in [('white', 'w3', 'A1_third_plus_nh_white'), ('black', 'blk', 'nh_black_rough')]:
            sc = w.R.scenario(code, scaled=False)
            sc['scenario_name'] = name
            published = w.scenarios()[name]
            entries = {}
            for method, basis in [('set', 'accrual'), ('cash', 'cash')]:
                entries[method] = {}
                for end in ('low', 'high'):
                    amount, rows, *_ = w.run29(sc, end, basis)
                    published_amount = w.run29(published, end, basis)[0]
                    # Preserve the comparator lane's fixed per-person prices:
                    # a fresh unscaled MEPS universe has different raw prices.
                    cost = published_amount['cost'] * sc['population'] / published_amount['population']
                    entries[method][end] = {'population': sc['population'], 'cost_bn': cost,
                        'natural_unscaled_universe_cost_bn': amount['cost'],
                        'published_comparator_cost_bn': published_amount['cost'],
                        'published_comparator_population': published_amount['population'],
                        'rough_lineage_cost_bn': w.run29(w.UNION_SC, end, basis)[0]['cost'],
                        'case_lineage_cost_bn': w.run29('eng', end, basis)[0]['cost'],
                        'lineage_population': w.R.TARGET + w.LINEAGE['counts']['added'],
                        'specification': w.DUMP[basis][end]['spec'],
                        'lines': {lid: {'side': side, 'national_bn': national, 'union_target_bn': target, 'response': response}
                                  for side, lid, national, target, response in rows}}
            groups[group] = entries
    (CACHE / 'comparator_targets.log').write_text(log.getvalue())
    write_json(OUT / 'comparator_targets.json', groups)


def archive(path):
    with np.load(path) as data:
        return {k: data[k].copy() for k in data.files}


def counts(d, W, civ, union):
    unit = pd.factorize(d.SPM_ID, sort=False)[0]
    mixed = (np.bincount(unit, weights=union) > 0) & (np.bincount(unit, weights=civ & ~union) > 0)
    mem = source_module('membership', 'counts')
    bio, step, links = mem.biological_children(d, union, civ)
    all_bio = civ & ~union & d.A_AGE.lt(18).to_numpy() & (links >= 0).any(axis=0)
    def count(mask):
        return {'records': int(mask.sum()), 'weighted_persons': float(W[mask, 0].sum()),
                'replicate_counts': W[mask].sum(axis=0).tolist()}
    return {'members': count(union), 'mixed_units': int(mixed.sum()), 'members_in_mixed_units': count(union & mixed[unit]),
            'nonmembers_staying_in_mixed_units': count(civ & ~union & mixed[unit]),
            'noncivilian_nonmembers_in_mixed_units': count(~civ & ~union & mixed[unit]),
            'biological_children_outside_group_stay': count(bio),
            'all_biological_children_outside_group_stay': count(all_bio), 'step_only_children_stay': count(step)}


def state_registry(d, original, federal):
    """Represent new survivor filers by absent, zero-income before returns.

    The source state kernel requires aligned before/after rows. Zero before
    rows create no original tax or calibration mass; the actual after-return
    retains the new claimant's own record, inputs, weight and source ownership.
    """
    n = len(original)
    extra = federal['afterR'].iloc[n:].copy()
    if extra.empty:
        return original, federal['before_input']
    rows = extra.row.to_numpy(int)
    require((d.STATETAX_A.to_numpy()[rows] == 0).all(), 'new filer has no booked original state liability')
    extra['spouse'] = -1
    extra['status'] = 'single'
    before = federal['after_input'].iloc[n:].copy()
    identity = {'year', 'statefip', 'page', 'mstat'}
    before.loc[:, [k for k in before if k not in identity]] = 0
    before['mstat'] = 1
    return pd.concat([original, extra], ignore_index=True), pd.concat([federal['before_input'], before], ignore_index=True)


class TaxsimCache:
    """Exact-input in-run kernel reuse, capped at 64MB and four outputs."""
    def __init__(self):
        self.outputs = OrderedDict()
        self.bytes = self.hits = self.misses = 0

    def run(self, kernel, native, frame):
        kernel.verify_sources()
        key = hashlib.sha256(frame.to_csv(index=False, lineterminator='\n').encode()).hexdigest()
        if key in self.outputs:
            self.hits += 1
            value, _ = self.outputs.pop(key)
            self.outputs[key] = value, int(value.memory_usage(deep=True).sum())
            return value.copy(deep=True)
        self.misses += 1
        value = native(frame)
        size = int(value.memory_usage(deep=True).sum())
        if size <= 64_000_000:
            while self.outputs and (self.bytes + size > 64_000_000 or len(self.outputs) >= 4):
                _, (_, oldsize) = self.outputs.popitem(last=False)
                self.bytes -= oldsize
            self.outputs[key] = value, size
            self.bytes += size
            return value.copy(deep=True)
        return value


def tax(group, profile=False):
    require(group == 'lineage' or (OUT / 'positive_control.json').exists(), 'lineage positive control before comparators')
    target = CACHE / group
    target.mkdir(parents=True, exist_ok=True)
    m = source_module('removal', group)
    original_loader = m.load_module
    kernel_cache = TaxsimCache()
    def redirected(path, name):
        module = original_loader(path, name)
        if Path(path).parent == SOURCE:
            if hasattr(module, 'OUT'):
                module.OUT = target
            if hasattr(module, 'CACHE'):
                module.CACHE = target
            if Path(path).stem == 'state_tax':
                native = module.run_taxsim
                module.run_taxsim = lambda frame: kernel_cache.run(module, native, frame)
            if Path(path).stem == 'tax_corrections':
                module.load = redirected
        return module
    m.load_module = redirected
    c, x = m.positive_control()
    d = m.add_fields(x['d'], c)
    d = join_extra(d, c, ['PEHSPNON', 'PRDTRACE', 'PEPAR1TYP', 'PEPAR2TYP'])
    x['d'] = d
    case = json.loads((SOURCE / 'derived/case_inputs.json').read_text())
    if group != 'lineage':
        union, gen = membership(d, x['civ'], group)
        x.update(union=union, gen=gen)
        x['W'] = comparator_weights(d, x['W'])
        x['wr'] = x['W'][x['R'].row.to_numpy(int)]
        x['mass_r4'] = float(x['vkey'][x['civ']] @ x['W'][x['civ'], 0])
        refkey = x['eitc_case'] + x['actc_case']
        x['per_ref'] = x['mts']['non_ptc_remainder_bn'] * x['hf'] / (refkey[x['civ']] @ x['W'][x['civ']])
        R, drows, ri, dgen, dmem = c.returns(d, union, gen, x['civ'])
        require(np.array_equal(R.row, x['R'].row) and np.array_equal(R.spouse, x['R'].spouse), 'comparator registry keeps actual tax carriers')
        x.update(R=R, drows=drows, ri=ri, dgen=dgen, dmem=dmem, comp_ruled={})
        x['model'] = declaration_model(d, x['civ'], union, x['model'])
    federal = m.federal_removal(c, x, d)
    state_kernel = redirected(SOURCE / 'state_tax.py', 'mixedcomp_state')
    before_registry, before_inputs = state_registry(d, x['R'], federal)
    state = state_kernel.compute(d, before_registry, x['P'], x['base'], x['W'], x['union'], x['gen'], x['flag'], x['onbooks'], x['model'], civ=x['civ'],
        refiling={'own': federal['own'], 'dep_counts': federal['counts'], 'R': federal['afterR'], 'owner': federal['owner'],
                  'before_input': before_inputs, 'after_input': federal['after_input']})
    if group == 'lineage':
        consumption = m.consumption_removal(c, x, d, case)
        r = redirected(SOURCE / 'round2.py', 'mixedcomp_round2')
        def terms(command, path):
            kind = 'health' if Path(command[4]).name == 'health.py' else 'snap'
            subset = 'latent' if '--membership' in command else 'union'
            result = archive(target / f'{kind}_{subset}.npz')
            if subset == 'union':
                write_json(target / ('health_results.json' if kind == 'health' else 'snap_arm_results.json'), json.loads((target / f'{kind}_{subset}.json').read_text()))
            return result
        r.load_terms = terms
        if profile:
            profiler = cProfile.Profile()
            details = profiler.runcall(r.extend, m.runtime_api(), c, x, d, case, federal, state, None, consumption)
            profiler.dump_stats(CACHE / 'source_integration.prof')
            with (CACHE / 'source_integration_profile.txt').open('w') as stream:
                pstats.Stats(profiler, stream=stream).sort_stats('cumulative').print_stats(30)
        else:
            details = r.extend(m.runtime_api(), c, x, d, case, federal, state, None, consumption)
        positive_control(details, target)
        write_json(target / 'kernel_cache.json', {'hits': kernel_cache.hits, 'misses': kernel_cache.misses, 'retained_bytes': kernel_cache.bytes})
        return
    all_targets = json.loads((OUT / 'comparator_targets.json').read_text())[group]
    count = counts(d, x['W'], x['civ'], x['union'])
    require(abs(count['members']['weighted_persons'] - all_targets['set']['low']['population']) < 1e-3,
            f"comparator count equals authoritative lane: {count['members']['weighted_persons']} vs {all_targets['set']['low']['population']}")
    vectors, summaries, allocations = {}, [], {}
    for method in ('set', 'cash'):
        for end in ('low', 'high'):
            own = all_targets[method][end]
            for lid in ('general_sales_tax', 'excise_selective_sales', 'customs_duties', 'personal_current_transfers',
                        'federal_income_tax', 'state_local_income_tax', 'refundable_tax_credits', 'snap', 'housing_subsidies'):
                require(own['lines'][lid]['response'] == 1, 'source unified kernel requires unit current response: ' + lid)
            context = copy.deepcopy(case)
            context['lines'] = {lid: own['lines'][lid] for lid in case['lines']}
            context['resourceLines'] = {lid: dict(own['lines'][lid], side=('receipt' if own['lines'][lid]['side'] == 'receipts' else 'spending')) for lid in case['resourceLines']}
            allocation_key = json.dumps([context['lines'], {lid: context['resourceLines'][lid]
                for lid in ('modeled_owner_property', 'snap', 'housing_subsidies')}], sort_keys=True)
            if allocation_key not in allocations:
                consumption = m.consumption_removal(c, x, d, context)
                res = redirected(SOURCE / 'resource_keys.py', 'mixedcomp_resource')
                resources = res.compute(d, x, context, m.disposable_income(d, x['R'], x['P'])[0])
                allocations[allocation_key] = consumption, resources
            consumption, resources = allocations[allocation_key]
            health = archive(target / 'health_union.npz')
            snap = archive(target / 'snap_union.npz')
            z = np.zeros((3, 161))
            fixed = {'M1_federal': federal['M1'], 'M2_state': state['M2'], 'M3_refunds': federal['M3'],
                'M6_biological_children': z, 'D_added_residual': z, 'M5_consumption': consumption['M5'],
                'M5_owner_property': resources['terms']['modeled_owner_property'] * own['lines']['modeled_owner_property']['response'],
                'M5_SNAP_key': resources['terms']['snap'], 'M5_housing_key': resources['terms']['housing_subsidies'],
                'M4_SNAP_baseline_interaction': -resources['terms']['snap'], 'membership_benefit_interaction': z}
            candidates = {h + '|' + a + '|' + s: sum(fixed.values()) + health[h] + health[a] + snap[s]
                for h in ('Medicaid_low', 'Medicaid_high') for a in ('ACA_low', 'ACA_high') for s in ('SNAP_zero_observed_low_takeup', 'SNAP_zero_observed_high_takeup', 'SNAP_cap_observed_low_takeup', 'SNAP_cap_observed_high_takeup')}
            for label, chooser in [('bounded_low', min), ('bounded_high', max)]:
                arm = chooser(candidates, key=lambda k: float(candidates[k][:, 0].sum()))
                vector = candidates[arm]
                h, a, s = arm.split('|')
                parts = dict(fixed, Medicaid=health[h], ACA=health[a], SNAP=snap[s])
                require(np.max(abs(sum(parts.values()) - vector)) < 1e-9, 'comparator all-replicate component closure')
                summaries.append({'method': method, 'end': end, 'reading': label, 'arm': arm, 'bn': float(vector[:, 0].sum()),
                    'se_bn': c.sdr(vector.sum(axis=0)), 'parts': {k: {'bn': float(v[:, 0].sum()), 'se_bn': c.sdr(v.sum(axis=0))} for k, v in parts.items()}})
                vectors[(method, end, label)] = vector.sum(axis=0)
            vectors.update({(method, end, k): v.sum(axis=0) for k, v in fixed.items()})
            vectors.update({(method, end, k): health[k].sum(axis=0) for k in ('Medicaid_low', 'Medicaid_high', 'ACA_low', 'ACA_high')})
            vectors.update({(method, end, k): v.sum(axis=0) for k, v in snap.items()})
    write_json(OUT / f'{group}_summary.json', {'group': group, 'counts': count, 'results': summaries, 'federal': federal['details'], 'state': state['details'], 'source_gates': m.GATES})
    pd.DataFrame([{'method': method, 'end': end, 'component': component, **{f'r{i}': float(v[i]) for i in range(161)}}
                  for (method, end, component), v in vectors.items()]).to_csv(OUT / f'{group}_replicates.csv', index=False, lineterminator='\n', float_format='%.15g')
    write_json(target / 'kernel_cache.json', {'hits': kernel_cache.hits, 'misses': kernel_cache.misses, 'retained_bytes': kernel_cache.bytes})


def positive_control(details, target):
    reference = json.loads((SOURCE / 'derived/round2_summary.json').read_text())
    keys = lambda row: (row['method'], row['end'], row['component'])
    old = {keys(r): r for r in reference['results']}
    maximum = 0.
    for row in details['results']:
        ref = old[keys(row)]
        for field in ('bn', 'se_bn', 'by_generation_bn', 'by_generation_se_bn'):
            maximum = max(maximum, float(np.max(abs(np.asarray(row[field]) - np.asarray(ref[field])))))
    require(maximum <= 1e-6, 'lineage all parts and paired SE reproduce within 1e-6bn')
    generated = pd.read_csv(target / 'round2_replicates.csv')
    original = pd.read_csv(SOURCE / 'derived/round2_replicates.csv')
    require(generated.iloc[:, :4].equals(original.iloc[:, :4]), 'lineage replicate component keys')
    stack_gap = float(np.max(abs(generated.iloc[:, 4:].to_numpy() - original.iloc[:, 4:].to_numpy())))
    require(stack_gap <= 1e-6, 'lineage every component replicate reproduces')
    headline = [r for r in details['results'] if r['component'] in ('bounded_low', 'bounded_high')]
    write_json(OUT / 'positive_control.json', {'passed': True, 'tolerance_bn': 1e-6, 'maximum_part_or_se_gap_bn': maximum,
        'maximum_replicate_gap_bn': stack_gap, 'rows_checked': len(details['results']), 'headline': headline})
    print('[positive control] PASS', maximum, stack_gap, flush=True)


def verify_source():
    pins = json.loads((OUT / 'source_fingerprints.json').read_text())
    require(all(digest(FISCAL / path) == value for path, value in pins.items()), 'all source bytes unchanged')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--profile', action='store_true')
    parser.add_argument('--tax', choices=('lineage', 'white', 'black'))
    parser.add_argument('--policy', choices=('health', 'snap'))
    parser.add_argument('--group', choices=('lineage', 'white', 'black'))
    parser.add_argument('--subset', choices=('union', 'latent'), default='union')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    if args.prepare:
        prepare()
    elif args.tax:
        tax(args.tax, profile=args.profile)
    elif args.policy and args.group:
        policy(args.group, args.policy, args.subset)
    else:
        parser.error('specify --prepare, --tax, or --policy and --group')
    verify_source()
    peak = require_within_budget('mixed-unit comparator adapter')
    receipt = {'seconds': time.perf_counter() - start, 'peak_physical_footprint_bytes': peak,
               'maxrss_raw': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'argv': sys.argv[1:]}
    with (CACHE / 'timing.jsonl').open('a') as stream:
        stream.write(json.dumps(receipt) + '\n')
    print('[receipt]', json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()

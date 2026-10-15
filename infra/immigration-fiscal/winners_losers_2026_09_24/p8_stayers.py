"""Trace item 11's fixed-membership producer flows before generation aggregation.

The source overlap probe already observes every native kernel. This adapter loads
only its function definitions as a library, substitutes record IDs for household
bins, and publishes the observed dollar vectors in isolated bounded processes.
No source entry point, acquisition, output writer or source-lane guard is run.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PARTS = ('tax', 'resources', 'consumption', 'health', 'snap')
FIXED = ('M1_federal', 'M2_state', 'M3_refunds', 'M6_biological_children',
         'M5_consumption', 'M5_owner_property', 'M5_housing_key')
POLICY_TAX = ('M1_federal', 'M2_state', 'M3_refunds', 'M6_biological_children')


def require(ok, message):
    if not bool(ok):
        raise ValueError('[BLOCKED] v8 stayers: ' + message)


def source_paths(fiscal=FISCAL):
    fiscal = Path(fiscal)
    mixed = fiscal / 'mixed_unit_removal_2026_10_14'
    files = [Path(__file__), fiscal / 'main_case_2026_10_15/mixed_overlap.py',
             fiscal / 'union_completion_2026_10_14/completion.py',
             fiscal / 'mixed_unit_credits_2026_10_14/credits.py',
             mixed / 'derived/round2_summary.json', mixed / 'derived/case_inputs.json']
    files += [mixed / (name + '.py') for name in
              ('removal', 'membership', 'resource_keys', 'state_tax', 'health', 'snap_arm', 'benefits')]
    return files


def _signature(fiscal=FISCAL):
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths(fiscal)}


def _capture_policy(kind, population, producer, observer, collector, receipts):
    """Observe own-resource tax changes before source attribution subtractions.

    Liability after-minus-before and refunds before-minus-after are signed
    presence gains. The producer's item5b subtraction belongs only to its fiscal
    delta. Native before/after flows provide an independent conservation check.
    """
    n = collector.n
    if kind == 'federal':
        h, own = observer['h'], observer['own']
        flows = {
            'federal': (observer['af'], observer['bf'], own, h, 1.,
                        float(producer['M1'][:, 0].sum()), float(producer['item']['receipts'][:, 0].sum())),
            'refunds': (observer['cr_after'], observer['cr_before'], own, h, -1.,
                       float(producer['M3'][:, 0].sum()), float(producer['item']['spending'][:, 0].sum())),
        }
    else:
        scope = producer['scope']
        conversion = producer['conversion'][0]
        flows = {'state': (producer['surviving_weighted'][:, 0] * conversion,
                           producer['original_weighted'][:, 0] * conversion,
                           producer['own'][scope], producer['h'][scope], 1.,
                           float(producer['direct'][0]), 0.)}
    for name, (after, before, after_rows, before_rows, sign, fiscal, subtraction) in flows.items():
        require(np.all(np.asarray(after_rows) >= 0) and np.all(np.asarray(before_rows) >= 0),
                'native tax event has no record owner')
        after_vector = np.bincount(after_rows, weights=after, minlength=n)
        before_vector = np.bincount(before_rows, weights=before, minlength=n)
        policy = sign * (after_vector - before_vector)
        native = sign * (float(np.sum(after)) - float(np.sum(before)))
        require(abs(float(policy.sum()) - native) < 1e-9, 'raw before/after tax closure ' + name)
        require(abs(float(policy.sum()) - fiscal - subtraction) < 1e-9,
                'raw tax is not source fiscal plus its complete old5b subtraction ' + name)
        collector.events[population + '_policy_' + name] = policy
        receipts[population + '_' + name] = dict(before_bn=float(before_vector.sum()),
            after_bn=float(after_vector.sum()), signed_presence_bn=float(policy.sum()),
            source_fiscal_delta_bn=fiscal, source_old5b_subtraction_bn=subtraction,
            signed_presence_rule='after-minus-before liability' if sign == 1 else 'before-minus-after refunds')


def _policy_observers(fn):
    """Insert two observations into the source's nested tax callbacks only."""
    counts = dict(federal=0, state=0)

    class AddPolicy(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name == 'federal':
                anchors = [i for i, child in enumerate(node.body) if isinstance(child, ast.Assign)
                           and any(isinstance(t, ast.Name) and t.id == 'r' for t in child.targets)]
                require(len(anchors) == 1, 'raw federal observer anchor changed')
                call = ast.parse("_capture_policy('federal', current[0], v, locals(), col, _policy_receipts)").body
                node.body[anchors[0] + 1:anchors[0] + 1] = call
                counts['federal'] += 1
                return node
            if node.name == 'state':
                node.body += ast.parse("_capture_policy('state', current[0], v, locals(), col, _policy_receipts)").body
                counts['state'] += 1
                return node
            return self.generic_visit(node)
    transformed = AddPolicy().visit(fn)
    require(counts == dict(federal=1, state=1), 'raw-policy observer callback API changed')
    return ast.fix_missing_locations(transformed)


def _run_source_part(part, output):
    """Observe the exact full-sample monetary flows, never rerun producer writers."""
    start = time.perf_counter()
    source = FISCAL / 'main_case_2026_10_15/mixed_overlap.py'
    selected = {'require', 'module', 'adapted', 'is_target', 'augment', 'load_frame',
                'completion_mask', 'trace_return', 'context', 'tax_part',
                'resource_part', 'consumption_part', 'benefit_part'}
    tree = ast.parse(source.read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in selected]
    require({n.name for n in functions} == selected, 'overlap observer API changed')
    functions = [_policy_observers(fn) if fn.name == 'tax_part' else fn for fn in functions]
    ns = dict(ast=ast, contextlib=contextlib, hashlib=hashlib, importlib=importlib,
              json=json, np=np, pd=pd, Path=Path, sys=sys, time=time,
              zipfile=zipfile, FISCAL=FISCAL, START=start,
              MIXED=FISCAL / 'mixed_unit_removal_2026_10_14',
              CONTROL=FISCAL / 'mixed_unit_credits_2026_10_14',
              COMPLETION=FISCAL / 'union_completion_2026_10_14',
              _capture_policy=_capture_policy, _policy_receipts={})
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), ns)
    original_mask = ns['completion_mask']
    state = {}

    def mask(d, c, civ, union, W):
        d, completed, _, _, counts = original_mask(d, c, civ, union, W)
        state.update(d=d, completed=completed, civ=civ, union=union,
                     weights=W[:, 0].copy())
        return d, completed, np.arange(len(d)), np.zeros(len(d), bool), counts
    ns['completion_mask'] = mask

    class Records:
        def __init__(self, d, hh, affected):
            self.events = {}
            self.n = len(d)
            state['collector'] = self

        def add(self, name, values, rows=None):
            rows = np.arange(self.n) if rows is None else np.asarray(rows, int)
            self.events[name] = np.bincount(rows, weights=values, minlength=self.n)

        def record(self, name):
            values = self.events[name]
            state.setdefault('published', {})[name] = values.copy()
            return dict(global_bn=float(values.sum()), overlap_bn=0.,
                        overlap_absolute_household_bn=0.)
    ns['Collect'] = Records
    with contextlib.redirect_stdout(sys.stderr):
        fn = ns[part + '_part'] if part in ('tax', 'consumption') else ns['resource_part'] if part == 'resources' else lambda: ns['benefit_part'](part)
        result = fn()
    d = state['d']
    # Record aliases used by resource/health/SNAP observers are mapped in their
    # result object; recover the matching native vector by exact monetary total.
    aliases = {'M5_owner_property': 'modeled_owner_property', 'M5_housing_key': 'housing_subsidies',
               'Medicaid_low': 'event_0', 'Medicaid_high': 'event_1',
               'ACA_low': 'event_4', 'ACA_high': 'event_5',
               'SNAP_zero_observed_high_takeup': 'event_1',
               'SNAP_cap_observed_low_takeup': 'event_5'}
    arrays = {}
    for name, receipt in result['components'].items():
        key = name if name in state['published'] else aliases[name]
        v = state['published'][key]
        require(abs(v.sum() - receipt['global_bn']) < 1e-9, 'native component parity ' + name)
        arrays[name] = v
    if part == 'tax':
        events = state['collector'].events
        aliases = dict(M1_federal='federal', M2_state='state', M3_refunds='refunds')
        for component, event in aliases.items():
            arrays['policy_' + component] = events['union_policy_' + event]
        arrays['policy_M6_biological_children'] = sum(
            events['expanded_policy_' + event] - events['union_policy_' + event]
            for event in aliases.values())
        expected = sum(v['signed_presence_bn'] for k, v in ns['_policy_receipts'].items() if k.startswith('expanded_'))
        require(abs(sum(arrays['policy_' + k].sum() for k in POLICY_TAX) - expected) < 1e-9,
                'policy tax and raw M6 do not telescope to expanded native before/after')
        result['policy_tax_bn'] = {k: float(arrays['policy_' + k].sum()) for k in POLICY_TAX}
        result['policy_before_after'] = ns['_policy_receipts']
    sys.path.insert(0, str(FISCAL / 'scripts'))
    from memory_budget import require_within_budget
    peak = require_within_budget('winners item11 ' + part)
    with Path(output).open('wb') as stream:
        np.savez_compressed(stream, PH_SEQ=d.PH_SEQ.to_numpy(), PPPOS=d.PPPOS.to_numpy(),
                            SPM_ID=d.SPM_ID.to_numpy(), state=d.GESTFIPS.to_numpy(),
                            stayer=state['civ'] & ~state['union'] & ~state['completed'],
                            weight=state['weights'], **arrays)
    Path(str(output) + '.json').write_text(json.dumps(dict(
        part=part, seconds=time.perf_counter() - start, peak_footprint_bytes=peak,
        diagnostic_peak_rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        source_sha256=_signature(), components=result['components'],
        policy_tax_bn=result.get('policy_tax_bn'), policy_before_after=result.get('policy_before_after')), indent=2) + '\n')


def _remap(values, stayer, units, states, weights):
    """Conserve each native flow, reassign departing carriers to surviving units."""
    values = np.asarray(values, float)
    out = np.where(stayer, values, 0.)
    displaced = np.where(~stayer, values, 0.)
    # Transfer within actual SPM first. The source component may be a carrier
    # on a departing member, which is attribution rather than that person's gain.
    uc, _ = pd.factorize(units, sort=False)
    pool = np.bincount(uc, weights=displaced)
    mass = np.bincount(uc, weights=weights * stayer)
    located = np.divide(pool, mass, out=np.zeros_like(pool), where=mass > 0)
    out += weights * stayer * located[uc]
    unlocated = (mass[uc] == 0) & ~stayer
    degraded = []
    for state in np.unique(states[unlocated]):
        m = unlocated & (states == state)
        amount = float(displaced[m].sum())
        if amount == 0:
            continue
        eligible = stayer & (states == state)
        den = float(weights[eligible].sum())
        require(den > 0, 'state has unlocated dollars and no stayer')
        out[eligible] += amount * weights[eligible] / den
        degraded.append(dict(state=int(state), signed_bn=amount,
                             absolute_bn=float(np.abs(displaced[m]).sum()),
                             status='[DEGRADED]', rule='same-state stayer head weight'))
    require(abs(out.sum() - values.sum()) < 1e-8, 'stayer reassignment changed total')
    require(not np.any(out[~stayer]), 'departing person retains stayer flow')
    return out, dict(reassigned_within_spm_bn=float(displaced[~unlocated].sum()),
                     unlocated_stayer_buckets=degraded)


def load_stayers(d, weights, fiscal, cache, payload, legacy_credit=None):
    """Return policy resource changes and a separate full fiscal-attribution arm.

    Direct policy tax uses native before/after flows before every old5b
    subtraction; M6 is the raw membership difference, without the projection.
    Fixed-pool M5 changes and unlocated D are fiscal attribution only. Passing
    legacy_credit restores the prior attribution arm beside; it never changes
    policy incidence. Suppress the old separate direct credit channel.
    """
    require(Path(fiscal).resolve() == FISCAL.resolve(), 'unexpected fiscal root')
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    signature = _signature()
    collected, audits, raw, policy_receipts = {}, {}, None, None
    for part in PARTS:
        path = cache / ('item11_' + part + '.npz')
        receipt = Path(str(path) + '.json')
        fresh = path.exists() and receipt.exists() and json.loads(receipt.read_text()).get('source_sha256') == signature
        if not fresh:
            command = [sys.executable, str(Path(__file__)), '--part', part, '--out', str(path)]
            run = subprocess.run(command, text=True, capture_output=True, env=dict(os.environ, OPENBLAS_NUM_THREADS='1'))
            (cache / ('item11_' + part + '.log')).write_text(run.stdout + run.stderr)
            require(run.returncode == 0, part + ' kernel exited ' + str(run.returncode) + ': ' + run.stderr[-2500:])
        if part == 'tax':
            policy_receipts = json.loads(receipt.read_text())
            require(policy_receipts.get('policy_tax_bn') is not None, 'raw policy-tax receipt missing')
        with np.load(path, allow_pickle=False) as store:
            frame = {k: store[k].copy() for k in ('PH_SEQ', 'PPPOS', 'SPM_ID', 'state', 'stayer', 'weight')}
            if raw is None:
                raw = frame
            else:
                require(all(np.array_equal(raw[k], frame[k]) for k in raw), 'component source frames disagree')
            for name in store.files:
                if name in frame:
                    continue
                collected[name], audits[name] = _remap(store[name], raw['stayer'], raw['SPM_ID'], raw['state'], raw['weight'])
    source = json.loads((FISCAL / 'mixed_unit_removal_2026_10_14/derived/round2_summary.json').read_text())
    source_index = pd.MultiIndex.from_arrays([raw['PH_SEQ'], raw['PPPOS']])
    target_index = pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']])
    pos = source_index.get_indexer(target_index)
    require(len(pos) == len(source_index) and np.all(pos >= 0) and len(np.unique(pos)) == len(pos), 'caller person join not bijective')
    by_end, by_end_attribution, totals = {}, {}, {}
    weights = np.asarray(weights, float)
    caller_stayer = d.other.to_numpy(bool)
    for end in ('low', 'high'):
        selected = next(r for r in source['results'] if r['method'] == 'set' and r['end'] == end and r['component'] == 'bounded_' + end)
        health, aca, snap = selected['arm'].split('|')
        names = list(FIXED) + [health, aca, snap]
        dollars = {k: collected[k][pos] for k in names}
        residual = payload['meta']['mixed_unit_removal']['by_end'][end]['D_added_residual_bn']
        dollars['D_added_residual'] = np.where(caller_stayer, weights, 0.) * residual / weights[caller_stayer].sum()
        target = payload['meta']['mixed_unit_removal']['by_end'][end]['total_bn']
        got = sum(float(v.sum()) for v in dollars.values())
        require(abs(got - target) < 1e-6, 'oct15 source item11 parts fail closure at ' + end)
        # Native vectors contain billions of dollars per record, already weighted.
        require(not any(np.any((v != 0) & ~caller_stayer) for v in dollars.values()), 'nonstayer carries a direct gain')
        stable = {health: 'Medicaid', aca: 'ACA', snap: 'SNAP'}
        arrays = {stable.get(k, k): np.divide(v * 1e9, weights, out=np.zeros(len(d)), where=weights > 0)
                  for k, v in dollars.items()}
        if legacy_credit is not None:
            arrays['item5b_replaced_once'] = np.asarray(legacy_credit, float).copy()
        by_end_attribution[end] = arrays
        policy_dollars = {k: collected['policy_' + k][pos] for k in POLICY_TAX}
        policy_dollars.update({stable[k]: dollars[k] for k in (health, aca, snap)})
        direct = {k: np.divide(v * 1e9, weights, out=np.zeros(len(d)), where=weights > 0)
                  for k, v in policy_dollars.items()}
        expected_policy = sum(policy_receipts['policy_tax_bn'].values()) + sum(float(dollars[k].sum()) for k in (health, aca, snap))
        policy_total = sum(float(v @ weights / 1e9) for v in direct.values())
        require(abs(policy_total - expected_policy) < 1e-9, 'direct policy native closure ' + end)
        require(not any(np.any(v[~caller_stayer]) for v in direct.values()), 'nonstayer retains policy resource change')
        by_end[end] = direct
        attribution_total = sum(float(v @ weights / 1e9) for v in arrays.values())
        legacy_bn = float(np.asarray(legacy_credit) @ weights / 1e9) if legacy_credit is not None else 0.
        require(abs(attribution_total - target - legacy_bn) < 1e-6, 'beside attribution closure ' + end)
        component_source = {stable.get(k, k): float(v.sum()) for k, v in dollars.items()}
        component_policy = {k: float(v.sum()) for k, v in policy_dollars.items()}
        discrepancy = {k: component_source.get(k, 0.) - component_policy.get(k, 0.)
                       for k in sorted(set(component_source) | set(component_policy))}
        require(abs(sum(discrepancy.values()) - (got - policy_total)) < 1e-9,
                'fiscal versus policy discrepancy ledger closure ' + end)
        totals[end] = dict(item11_delta_bn=got, replacement_bn=attribution_total,
                           direct_policy_bn=policy_total, attribution_bn=attribution_total,
                           source_fiscal_minus_policy_bn=got-policy_total,
                           source_fiscal_by_component_bn=component_source,
                           direct_policy_by_component_bn=component_policy,
                           source_fiscal_minus_policy_by_component_bn=discrepancy,
                           attribution_legacy_restoration_bn=legacy_bn,
                           unlocated_D_bn=residual, source_envelope=selected['arm'])
    metadata = dict(by_end=totals, components=audits,
                    credit_rule='direct: raw liability/refund before-after; no item5b restoration. Beside attribution: source delta plus legacy forward once',
                    legacy_credit_merged=legacy_credit is not None, legacy_credit_route='attribution_only',
                    direct_exclusions=['M5_consumption', 'M5_owner_property', 'M5_housing_key', 'D_added_residual', 'old5b_forward_restoration', 'M6_old_projection'],
                    D_assignment='beside attribution only: [DEGRADED] unlocated D assigned by surviving payer weight',
                    policy_before_after=policy_receipts['policy_before_after'],
                    fiscal_attribution_rule='fixed-pool allocation changes are retained in the case budget and beside incidence only; no own-resource dollar is created',
                    membership_interaction='source fixed-membership item11; item10 × item11 joint counterfactual uncomputed',
                    source_sha256=signature)
    return dict(by_end=by_end, by_end_attribution=by_end_attribution,
                metadata=metadata, source_paths=[str(p) for p in source_paths()])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', choices=PARTS, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    _run_source_part(args.part, args.out)

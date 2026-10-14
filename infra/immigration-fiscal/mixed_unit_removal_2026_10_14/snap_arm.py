#!/usr/bin/env python3
"""Conditional SNAP survivor arm with observed, explicitly pooled CPS take-up."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import time
import zipfile

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent


def load(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observed_takeup(state, size, eligible, observed, unit_weights, targets, minimum=20,
                    reference_size=None):
    """Rates +/- one SDR SE fixed across replicate outcome calculations.

    Pooling is explicit, with every selected tier and eligible sample count
    recorded. State/size -> state -> region/size -> national/size -> national.
    Signed replicate weights are retained; nonpositive pooled denominators block.
    """
    sizebin = np.minimum(size, 4)
    reference_bin = sizebin if reference_size is None else np.minimum(reference_size, 4)
    region = np.where(state == 2, 1, np.where(state == 15, 2, 0))
    low, high, rows = np.zeros(len(state)), np.zeros(len(state)), []
    for st, sz in sorted(set(zip(state[targets], sizebin[targets]))):
        dest = targets & (state == st) & (sizebin == sz)
        reg = 1 if st == 2 else 2 if st == 15 else 0
        tiers = (("state_size", (state == st) & (reference_bin == sz)),
                 ("state", state == st),
                 ("region_size", (region == reg) & (reference_bin == sz)),
                 ("national_size", reference_bin == sz),
                 ("national", np.ones(len(state), bool)))
        for tier, candidates in tiers:
            pool = candidates & eligible
            if pool.sum() >= minimum:
                break
        else:
            raise ValueError("[BLOCKED] no supported SNAP take-up population")
        den = unit_weights[pool].sum(axis=0)
        num = unit_weights[pool & observed].sum(axis=0)
        if np.any(den <= 0):
            raise ValueError(f"[BLOCKED] SNAP take-up {st}/{sz} nonpositive replicate denominator")
        rates = num / den
        if not 0 <= rates[0] <= 1:
            raise ValueError("[BLOCKED] SNAP full-sample take-up outside [0,1]")
        se = float(np.sqrt(4 / 160 * np.square(rates[1:] - rates[0]).sum()))
        lo, hi = max(0., float(rates[0]) - se), min(1., float(rates[0]) + se)
        low[dest], high[dest] = lo, hi
        rows.append({"state": int(st), "size_bin": int(sz), "tier": tier,
                     "eligible_sample_units": int(pool.sum()), "takeup": float(rates[0]),
                     "takeup_se": se, "takeup_low": lo, "takeup_high": hi})
    return low, high, rows


def after_benefit(observed, before_rule, after_rule, maximum, low, high):
    """Observed-level residual for participants; new eligibility gets take-up.

    Losing financial eligibility stops the benefit. Nonparticipants already
    financially eligible stay unobserved nonparticipants; no-event identity
    therefore holds. Observed participants failing both income proxies keep
    their reported residual rather than being relabeled as newly ineligible.
    """
    newly = (before_rule <= 0) & (after_rule > 0) & (observed <= 0)
    lost = (before_rule > 0) & (after_rule <= 0)
    anchored = np.minimum(np.maximum(observed + after_rule - before_rule, 0), maximum)
    existing = np.where(observed > 0, anchored, 0)
    existing = np.where(lost, 0, existing)
    return (existing + np.where(newly, after_rule * low, 0),
            existing + np.where(newly, after_rule * high, 0), newly, lost)


def compute(d, W, union, gen, civ, model, *, baseline_union=None):
    b = load(LANE / "benefits.py", "snap_reused_benefits")
    rule = b.rules()
    b.unit_values(d, ['SPM_SNAPSUB', 'SPM_TOTVAL', 'SPM_CHILDCAREXPNS',
                      'SPM_CHILDSUPPD', 'SPM_MEDXPNS', 'SPM_NUMPER', 'GESTFIPS'])
    unit, labels = pd.factorize(d.SPM_ID, sort=False)
    nu = len(labels)
    first = np.unique(unit, return_index=True)[1]
    size = np.bincount(unit, minlength=nu)
    b.require(np.array_equal(size, d.SPM_NUMPER.to_numpy()[first]), 'SNAP unit size drift')
    sums = lambda v: np.bincount(unit, weights=v, minlength=nu)
    nm = sums(union).astype(int)
    remaining = size - nm
    state = d.GESTFIPS.to_numpy(int)[first]
    allciv = sums(~civ) == 0
    mixed = (nm > 0) & (remaining > 0) & allciv & (state != 2)
    B = d.SPM_SNAPSUB.to_numpy(float)[first]
    income0 = d.SPM_TOTVAL.to_numpy(float)[first]
    income1 = income0 - sums(d.PTOTVAL.to_numpy(float) * union)
    earned = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    earn0, earn1 = sums(earned), sums(earned * ~union)
    care, medical, support = (d[col].to_numpy(float)[first] for col in
                              ('SPM_CHILDCAREXPNS', 'SPM_MEDXPNS', 'SPM_CHILDSUPPD'))
    special = (d.A_AGE.ge(rule['snap_elderly_age']) | d.SSI_VAL.gt(0) | d.PRDISFLG.eq(1)).to_numpy()
    sp0, sp1 = sums(special) > 0, sums(special & ~union) > 0
    fraction, safe_n = remaining / size, np.maximum(remaining, 1)
    allw = np.stack([sums(W[:, r]) for r in range(161)], axis=1)
    nonw = np.stack([sums(W[:, r] * ~union) for r in range(161)], axis=1)
    unitw = allw / size[:, None]
    key = B[unit] / size[unit]
    nat = key[civ] @ W[civ]
    line = next(x for x in model['spending']['lines'] if x['id'] == 'snap')
    audit = json.loads((LANE.parent / 'backtest_admin_totals_2026_09_28/derived/prediction_audit.json').read_text())
    conversion = line['national_bn'] * audit['household_fraction'] / nat
    base_union = union if baseline_union is None else baseline_union
    published = float(key[base_union] @ d.pwwgt0.to_numpy()[base_union] / (key[civ] @ d.pwwgt0.to_numpy()[civ]))
    b.require(abs(published - line['keys']['snap']['personal']['share']) < 5e-9,
              'SNAP positive control allocation changed')
    old_other = B[:, None] / size[:, None] * nonw
    terms, diagnostics = {}, {}
    for shelter in ('zero', 'cap'):
        r0, r1, maximum = np.zeros(nu), np.zeros(nu), np.zeros(nu)
        for year, months in ((24, 9), (25, 3)):
            r0 += months / 12 * b.snap_rule(rule, year, size, income0, earn0, care,
                                           medical, support, sp0, state, shelter)
            r1 += months / 12 * b.snap_rule(rule, year, safe_n, income1, earn1,
                                           care * fraction, medical * fraction,
                                           support * fraction, sp1, state, shelter)
            region = np.where(state == 2, 1, np.where(state == 15, 5, 0))
            maximum += months * b.sized(rule[year]['max'], rule[year]['increment'], safe_n, region)
        eligible_reference = (r0 > 0) & allciv & (state != 2)
        lo, hi, cells = observed_takeup(state, safe_n, eligible_reference, B > 0, unitw, mixed,
                                       reference_size=size)
        after_lo, after_hi, newly, lost = after_benefit(B, r0, r1, maximum, lo, hi)
        for name, amount in (('low_takeup', after_lo), ('high_takeup', after_hi)):
            change = (old_other - amount[:, None] * unitw) * conversion
            terms[f'SNAP_{shelter}_observed_{name}'] = b.attribute(change, unit, W, union, gen, mixed)
        # Counts describe financial-rule crossings independent of observed take-up.
        newly_financial = (r0 <= 0) & (r1 > 0) & mixed
        loss_financial = lost & mixed
        diagnostics[shelter] = {
            'newly_eligible_units': float(unitw[newly_financial, 0].sum()),
            'newly_eligible_surviving_people': float(nonw[newly_financial, 0].sum()),
            'newly_ineligible_units': float(unitw[loss_financial, 0].sum()),
            'newly_ineligible_surviving_people': float(nonw[loss_financial, 0].sum()),
            'new_nonparticipant_eligible_units': float(unitw[newly & mixed, 0].sum()),
            'new_nonparticipant_enrollments_low': float((unitw[:, 0] * lo)[newly & mixed].sum()),
            'new_nonparticipant_enrollments_high': float((unitw[:, 0] * hi)[newly & mixed].sum()),
            'takeup_cells': cells,
            'reported_participants_failing_proxy_test': int(((B > 0) & (r0 == 0) & mixed).sum()),
        }
        # Newly eligible spending and observed-recipient losses separately.
        for name, amount in (('newly_eligible_low', np.where(newly, r1 * lo, 0)),
                             ('newly_eligible_high', np.where(newly, r1 * hi, 0)),
                             ('newly_ineligible', np.where(lost, B, 0))):
            sign = 1 if name == 'newly_ineligible' else -1
            v = sign * amount[:, None] * unitw * conversion
            terms[f'SNAP_{shelter}_observed_{name}'] = b.attribute(v, unit, W, union, gen, mixed)
    details = {'recommendation': 'arm', 'identified_union_only': True,
               'source_pins': b.verify_sources(), 'positive_control_share': published,
               'exclusions': {'mixed_Alaska': int(((nm > 0) & (remaining > 0) & (state == 2)).sum()),
                              'mixed_noncivilian': int(((nm > 0) & (remaining > 0) & ~allciv).sum())},
               'diagnostics': diagnostics,
               'assumptions': ['SPM proxy assistance unit; steady annualized monthly income',
                               'federal financial income rules; assets/BBCE/ABAWD/student/status unresolved',
                               'income residual held; deductions proportional to survivors',
                               'shelter zero/cap; fixed observed take-up +/- one replicate SE',
                               'only newly eligible nonparticipants start; observed recipients retain level residual',
                               'loss of proxy financial eligibility stops prior participant benefits',
                               'original mean person weight unit-event basis; person weights unchanged'],
               'summaries': {k: {'bn': float(v[:, 0].sum()), 'se_bn': b.sdr(v.sum(axis=0))}
                             for k, v in terms.items()}}
    return {'terms': terms, 'details': details}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arrays-out', type=Path)
    parser.add_argument('--out', type=Path, default=LANE / 'derived/snap_arm_results.json')
    parser.add_argument('--membership', choices=('union', 'latent'), default='union')
    args = parser.parse_args()
    started = time.perf_counter()
    b = load(LANE / 'benefits.py', 'snap_standalone_benefits')
    c = load(LANE.parent / 'mixed_unit_credits_2026_10_14/credits.py', 'snap_standalone_credits')
    d = c.load()
    civ, union, gen = c.groups(d)
    W, _, _ = c.row4_weights(d, civ, union)
    d = d.drop(columns=c.REPS[1:])
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        extra = pd.read_csv(z.open('pppub25.csv'), usecols=['PH_SEQ', 'PPPOS'] + b.PERSON_COLUMNS)
        hh = pd.read_csv(z.open('hhpub25.csv'), usecols=['H_SEQ'] + b.HOUSEHOLD_COLUMNS)
    d = d.merge(extra, on=['PH_SEQ', 'PPPOS'], validate='one_to_one').merge(hh, on='H_SEQ', validate='many_to_one')
    base_union = union.copy()
    if args.membership == 'latent':
        membership = load(LANE / 'membership.py', 'snap_membership')
        d = membership.add_parent_types(d, c)
        latent = membership.latent_mask(d, union, civ)
        union = union | latent
        gen = gen.copy()
        gen[latent] = 2
    result = compute(d, W, union, gen, civ, json.loads(c.MODEL.read_text()), baseline_union=base_union)
    result['details']['membership'] = args.membership
    if args.membership == 'latent':
        result['details']['located_latent_people'] = float(W[latent, 0].sum())
    args.out.write_text(json.dumps(result['details'], indent=2, allow_nan=False) + '\n')
    csv_path = args.out.with_name(args.out.stem.replace('_results', '') + '_replicates.csv')
    pd.DataFrame([{'component': name, 'generation': g,
                   **{f'r{k}': float(v[i, k]) for k in range(161)}}
                  for name, v in result['terms'].items()
                  for i, g in enumerate(('G1', 'G2', 'G3+'))]).to_csv(
                      csv_path, index=False, lineterminator='\n')
    if args.arrays_out:
        np.savez_compressed(args.arrays_out, **result['terms'])
    print(json.dumps({'seconds': time.perf_counter() - started,
                      'self_maxrss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'summaries': result['details']['summaries']}, indent=2))


if __name__ == '__main__':
    main()

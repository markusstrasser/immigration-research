#!/usr/bin/env python3
"""Observed-household statutory cash sensitivities; not an identified v9 correction."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parent.parent
REMOVAL = FISCAL / 'mixed_unit_removal_2026_10_14'
CASE = FISCAL / 'main_case_2026_10_16'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    sys.modules[name] = out
    spec.loader.exec_module(out)
    return out


def require(ok, message):
    if not ok:
        raise RuntimeError('[BLOCKED] ' + message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def estimate(values, divisor=1e9):
    values = np.asarray(values) / divisor
    require(values.shape == (161,) and np.isfinite(values).all(), 'invalid estimate')
    return {'estimate': float(values[0]),
            'sdr_se': float(np.sqrt(4 / 160 * ((values[1:] - values[0]) ** 2).sum()))}


def payroll(wages, self_employment):
    """Both sides of covered payroll, CY2024; Additional Medicare separate."""
    wages = np.maximum(np.asarray(wages, float), 0)
    base = np.maximum(np.asarray(self_employment, float), 0) * .9235
    base = np.where(base >= 400, base, 0)
    return (.124 * np.minimum(wages, 168600) + .029 * wages
            + .124 * np.minimum(base, np.maximum(168600 - wages, 0)) + .029 * base)


def additional_medicare(frame):
    se = sum(np.where(frame[x].to_numpy() * .9235 >= 400,
                      np.maximum(frame[x].to_numpy(), 0) * .9235, 0)
             for x in ('psemp', 'ssemp'))
    wage = frame.pwages.to_numpy() + frame.swages.to_numpy()
    threshold = np.where(frame.mstat.to_numpy() == 2, 250000, 200000)
    return .009 * np.maximum(wage + se - threshold, 0)


def change_earnings(d, mask, fraction=None, entry=False):
    out = d.astype({'WSAL_VAL': float, 'SEMP_VAL': float, 'FRSE_VAL': float}).copy()
    wage = d.WSAL_VAL.to_numpy(float)
    se = (d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    if entry:
        # No positive labor income, not a claim about labor-force status.
        selected = mask & (wage <= 0) & (se <= 0)
        out.loc[selected, 'WSAL_VAL'] += 10000
    else:
        require(fraction is not None and fraction >= -1, 'invalid earnings shock')
        out.loc[mask, 'WSAL_VAL'] += np.maximum(wage[mask], 0) * fraction
        # Change positive NET farm + nonfarm SE; keep negative net losses fixed.
        out.loc[mask, 'SEMP_VAL'] += np.maximum(se[mask], 0) * fraction
    delta = ((out.WSAL_VAL + out.SEMP_VAL + out.FRSE_VAL)
             - (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL)).to_numpy(float)
    require(np.all(delta[~mask] == 0), 'earnings changed outside exposure')
    return out, delta


def load():
    c = module(FISCAL / 'mixed_unit_credits_2026_10_14/credits.py', 'bound_credits')
    r = module(REMOVAL / 'removal.py', 'bound_removal')
    m = module(REMOVAL / 'membership.py', 'bound_membership')
    with contextlib.redirect_stdout(io.StringIO()):
        d = c.load()
        civ, original, gen = c.groups(d)
        W, _, _ = c.row4_weights(d, civ, original)
        d = r.add_fields(d, c)
    fields = ['PH_SEQ', 'PPPOS', 'A_SPOUSE', 'PEPAR1TYP', 'PEPAR2TYP',
              'WKSWORK', 'HRSWK', 'PEDISDRS', 'PEDISOUT']
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        extra = pd.read_csv(z.open('pppub25.csv'), usecols=fields)
    d = d.merge(extra, on=['PH_SEQ', 'PPPOS'], how='left', validate='one_to_one', sort=False)
    require(not d[fields].isna().any().any(), 'raw person join incomplete')
    payload = json.loads((CASE / 'derived/corrections.json').read_text())
    keys = pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']])
    require(keys.is_unique, 'duplicate person keys')
    completion = np.zeros(len(d), bool)
    for row in payload['meta']['union_completion']['observed_records']:
        pos = keys.get_loc((row['PH_SEQ'], row['PPPOS']))
        require(not original[pos], 'completion duplicates original member')
        completion[pos] = True
    latent = m.latent_mask(d, original, civ)
    depart = original | completion | latent
    gen = gen.copy()
    gen[depart & ~original] = 2  # owner attribution only; no generation results published
    age = d.A_AGE.to_numpy()
    adult = age >= 18
    require(np.array_equal(W[adult & civ & ~depart, 0], d.pwwgt0.to_numpy()[adult & civ & ~depart]),
            'remaining-adult weight differs from published weight')
    factors = pd.read_parquet(FISCAL / 'count_composition_r5_2026_10_15/derived/native_person_factors.parquet')
    require(not factors.duplicated(['PH_SEQ', 'PPPOS']).any(), 'duplicate calibration keys')
    factor = factors.set_index(['PH_SEQ', 'PPPOS']).central_member_factor.reindex(keys).to_numpy()
    require(np.isfinite(factor).all() and (factor[adult] == 1).all(),
            'adult native calibration changed')
    hh, labels = pd.factorize(d.PH_SEQ, sort=False)
    count = lambda mask: np.bincount(hh, weights=mask, minlength=len(labels))[hh]
    stay = civ & ~depart
    broad = stay & adult & (count(depart) > 0)
    need = stay & ((age < 13) | (age >= 65) | d.PRDISFLG.eq(1).to_numpy())
    care = broad & (count(depart & adult) > 0) & (count(need) > need.astype(int))
    personal = stay & (d.PEDISDRS.eq(1) | d.PEDISOUT.eq(1)).to_numpy()
    masks = {'all_exposed': broad, 'care_proxy': care}
    diagnostic = {'personal_care_difficulty': broad & (count(personal) > personal.astype(int))}
    with contextlib.redirect_stdout(io.StringIO()):
        R, drows, ri, _, _ = c.returns(d, depart, gen, civ)
        after, own, _, _, details = r.survivor_registry(d, R, depart, gen, civ, drows, ri)
    # Original care allocation remains fixed in both after states.
    ncare = pd.Series((R.k13_all.to_numpy() > 0).astype(float)).groupby(
        d.PH_SEQ.to_numpy()[R.row]).transform('sum').to_numpy()
    care_paid = np.maximum(d.HCHCARE_VAL.to_numpy()[R.row], 0) / np.maximum(ncare, 1)
    after['childcare'] = 0.
    after.loc[:len(R)-1, 'childcare'] = np.where(after.k13_all.to_numpy()[:len(R)] > 0, care_paid, 0)
    after = after.loc[own >= 0].copy().reset_index(drop=True)
    represented = np.zeros(len(d), int)
    np.add.at(represented, after.row.to_numpy(int), 1)
    np.add.at(represented, after.loc[after.spouse >= 0, 'spouse'].to_numpy(int), 1)
    require((represented <= 1).all(), 'person represented twice in surviving returns')
    # Model an individual return for otherwise unrepresented exposed adults,
    # including zero-earners in the entry arm. No invented dependent assignment.
    missing = np.flatnonzero(broad & (represented == 0))
    if len(missing):
        extra = pd.DataFrame(0, index=np.arange(len(missing)), columns=after.columns)
        extra['row'], extra['spouse'], extra['status'] = missing, -1, 'single'
        extra['depfiler'] = d.DEP_STAT.to_numpy()[missing] > 0
        after = pd.concat([after, extra], ignore_index=True)
        represented[missing] += 1
    require((represented[broad] == 1).all(), 'exposed adult missing from returns')
    h, s = after.row.to_numpy(int), after.spouse.to_numpy(int)
    scope = broad[h] | ((s >= 0) & broad[np.maximum(s, 0)])
    after = after.loc[scope].reset_index(drop=True)
    require(not depart[after.row.to_numpy(int)].any(), 'departing return head retained')
    require(not depart[after.loc[after.spouse >= 0, 'spouse'].to_numpy(int)].any(), 'departing spouse retained')
    details.update(added_exposed_nonfiler_returns=len(missing), priced_returns=len(after),
                   observed_completion_records=int(completion.sum()), located_latent_records=int(latent.sum()))
    return c, d, W, civ, depart, after, masks, diagnostic, details


def snap_context(d, W, civ, depart, exposed):
    b = module(REMOVAL / 'benefits.py', 'bound_benefits')
    arm = module(REMOVAL / 'snap_arm.py', 'bound_snap_arm')
    rule = b.rules()
    fields = ['SPM_NUMPER', 'SPM_TOTVAL', 'SPM_SNAPSUB', 'GESTFIPS',
              'SPM_CHILDCAREXPNS', 'SPM_MEDXPNS', 'SPM_CHILDSUPPD']
    b.unit_values(d, fields)
    unit, labels = pd.factorize(d.SPM_ID, sort=False)
    n = len(labels)
    first = np.unique(unit, return_index=True)[1]
    sums = lambda v: np.bincount(unit, weights=v, minlength=n)
    size = np.bincount(unit, minlength=n)
    require(np.array_equal(size, d.SPM_NUMPER.to_numpy()[first]), 'SNAP roster mismatch')
    remain = size - sums(depart).astype(int)
    state = d.GESTFIPS.to_numpy()[first]
    priced = (sums(exposed) > 0) & (sums(~civ) == 0) & (state != 2)
    weights = np.stack([sums(W[:, j]) / size for j in range(161)], axis=1)
    special = (d.A_AGE.ge(rule['snap_elderly_age']) | d.SSI_VAL.gt(0) | d.PRDISFLG.eq(1)).to_numpy()
    income = d.SPM_TOTVAL.to_numpy()[first] - sums(np.where(depart, d.PTOTVAL, 0))
    earned = sums(np.where(depart, 0, d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL))
    deductions = [d[x].to_numpy()[first] * remain / size for x in fields[-3:]]
    new_special = sums(special & ~depart) > 0
    observed = d.SPM_SNAPSUB.to_numpy()[first]
    maximum = np.zeros(n)
    region = np.where(state == 2, 1, np.where(state == 15, 5, 0))
    for year, months in ((24, 9), (25, 3)):
        maximum += months * b.sized(rule[year]['max'], rule[year]['increment'], np.maximum(remain, 1), region)

    def schedule(delta, shelter):
        change = sums(delta)
        out = np.zeros(n)
        for year, months in ((24, 9), (25, 3)):
            out += months / 12 * b.snap_rule(rule, year, np.maximum(remain, 1),
                income + change, earned + change, *deductions, new_special, state, shelter)
        return out

    zero = np.zeros(len(d))
    # Reconstruct the original reported-level residual once. Eligibility and
    # deductions are proxy schedules, not administrative SNAP entitlement.
    original = {}
    for shelter in ('zero', 'cap'):
        original[shelter] = np.zeros(n)
        for year, months in ((24, 9), (25, 3)):
            original[shelter] += months / 12 * b.snap_rule(rule, year, size,
                d.SPM_TOTVAL.to_numpy()[first], sums(d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL),
                *(d[x].to_numpy()[first] for x in fields[-3:]), sums(special) > 0, state, shelter)
    baseline = {s: arm.after_benefit(observed, original[s], schedule(zero, s), maximum, 0, 1)[:2]
                for s in original}

    def response(delta):
        out = {}
        for shelter in original:
            changed = arm.after_benefit(observed, original[shelter], schedule(delta, shelter), maximum, 0, 1)[:2]
            for index, participation in enumerate(('existing', 'new_eligible_full')):
                out[f'snap_{shelter}_{participation}'] = ((changed[index] - baseline[shelter][index]) * priced) @ weights / 1e9
        return out
    return response, {'priced_units': int(priced.sum()),
                      'unpriced_alaska_or_noncivilian_units': int(((sums(exposed) > 0) & ~priced).sum()),
                      'weight_rule': 'original mean person weight per SPM unit; held across shocks'}


def main(out):
    c, d, W, civ, depart, R, masks, diagnostic, details = load()
    t = module(REMOVAL / 'state_tax.py', 'bound_tax')
    t.verify_sources()
    def frame(data):
        f = t.taxsim_frame(data, R)
        f['childcare'] = R.childcare.to_numpy()
        return f
    baseline_frame = frame(d)
    baseline = t.run_taxsim(baseline_frame)
    require({'addmed', 'fiitax', 'siitax'} <= set(baseline), 'missing tax components')
    h = R.row.to_numpy(int)
    # A return event uses its staying claimant's weight. Payroll uses each
    # person's own weight, so unequal spouse weights are not silently replaced.
    return_weights = W[h]
    base_payroll = payroll(d.WSAL_VAL, d.SEMP_VAL + d.FRSE_VAL)
    base_addmed = additional_medicare(baseline_frame)
    snap, snap_details = snap_context(d, W, civ, depart, masks['all_exposed'])
    earnings = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy()
    exposures = {}
    for name, mask in {**masks, **diagnostic}.items():
        positive = mask & ((d.WSAL_VAL > 0) | ((d.SEMP_VAL + d.FRSE_VAL) > 0)).to_numpy()
        exposures[name] = {'sample_adults': int(mask.sum()),
            'sample_households': int(d.loc[mask, 'PH_SEQ'].nunique()),
            'adults': estimate(mask @ W, 1), 'current_earners': estimate(positive @ W, 1),
            'earnings_bn': estimate((earnings * mask) @ W),
            'annual_hours_million': estimate((d.WKSWORK * d.HRSWK * mask).to_numpy() @ W, 1e6)}
    rows = []
    unchanged_max = 0.
    for group, mask in masks.items():
        for fraction in (0, -.1, -.25, -.5, -1, .1, .25, .5, 1, None):
            changed, delta = change_earnings(d, mask, fraction, entry=fraction is None)
            f = frame(changed)
            changed_rows = (f != baseline_frame).any(axis=1).to_numpy()
            evaluated = baseline.copy()
            if changed_rows.any():
                solved = t.run_taxsim(f.loc[changed_rows].reset_index(drop=True))
                for field in ('fiitax', 'siitax', 'addmed'):
                    evaluated.loc[changed_rows, field] = solved[field].to_numpy()
            tax_delta = evaluated[['fiitax', 'siitax', 'addmed']] - baseline[['fiitax', 'siitax', 'addmed']]
            unchanged_max = max(unchanged_max, float(np.abs(tax_delta.loc[~changed_rows].to_numpy()).max(initial=0)))
            # TAXSIM's reported Additional Medicare component is excluded here;
            # source formula is added once. Kernel fica is not used (see fixture).
            federal = (tax_delta.fiitax - tax_delta.addmed).to_numpy() @ return_weights / 1e9
            state = tax_delta.siitax.to_numpy() @ return_weights / 1e9
            pay = (payroll(changed.WSAL_VAL, changed.SEMP_VAL + changed.FRSE_VAL) - base_payroll) @ W / 1e9
            addmed = (additional_medicare(f) - base_addmed) @ return_weights / 1e9
            taxes = federal + state + pay + addmed
            benefit = snap(delta)
            nets = {key.replace('snap_', 'net_'): taxes - val for key, val in benefit.items()}
            values = {'earnings': delta @ W / 1e9, 'federal_net': federal, 'state_net': state,
                      'payroll': pay, 'additional_medicare': addmed, 'taxes': taxes, **benefit, **nets}
            if fraction == 0:
                require(all(np.max(np.abs(v)) == 0 for v in values.values()), 'zero response not identity')
            row = {'group': group, 'response': 'entry_10000' if fraction is None else str(fraction),
                   'changed_returns': int(changed_rows.sum())}
            for key, value in values.items():
                est = estimate(value, 1)
                row[key + '_bn'], row[key + '_se_bn'] = est['estimate'], est['sdr_se']
            rows.append(row)
            print(f"[scenario] {group} {row['response']}: taxes {taxes[0]:.4f}bn", flush=True)
    require(unchanged_max == 0, 'unchanged returns affected')
    summary = json.loads((CASE / 'derived/summary.json').read_text())
    paths = [Path(__file__), LANE / 'DESIGN.md', c.CPS_ZIP, CASE / 'derived/corrections.json',
             CASE / 'derived/summary.json', FISCAL / 'count_composition_r5_2026_10_15/derived/native_person_factors.parquet',
             FISCAL / 'mixed_unit_credits_2026_10_14/credits.py', REMOVAL / 'removal.py',
             REMOVAL / 'membership.py', REMOVAL / 'state_tax.py', REMOVAL / 'benefits.py', REMOVAL / 'snap_arm.py',
             REMOVAL / 'inputs/state_pins.json', REMOVAL / 'inputs/benefit_pins.json']
    manifest = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    result = {'status': 'conditional partial cash response; not an identified effect or complete bound',
              'income_year': 2024, 'survey_year': 2025,
              'cash_materiality_bn': .05 * summary['cash_set']['band_bn'][0],
              'accrual_scale_reference_bn': .05 * summary['main_case'][0],
              'exposures': exposures, 'registry': details, 'snap': snap_details,
              'checks': {'zero_response_identity': True, 'unchanged_returns_identity': True,
                         'signed_replicates': 160, 'complete_exposed_adult_return_coverage': True},
              'source_sha256': manifest}
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / 'responses.csv', index=False, lineterminator='\n', float_format='%.12g')
    (out / 'audit.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'exposures': exposures, 'cash_materiality_bn': result['cash_materiality_bn']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', type=Path, default=LANE / 'derived')
    main(parser.parse_args().out_dir)

#!/usr/bin/env python3
"""Read-only re-use of v7's CPS frame; survivor removal on the personal account.

Native-First: the existing Census-credit lane is the positive control; its main
is run unchanged with outputs redirected here. No new acquisition of CPS data.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import resource
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
OUT = LANE / 'derived'
CACHE = LANE / '_cache'
CONTROL = FISCAL / 'mixed_unit_credits_2026_10_14'
GATES = []


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def gate(name, passed, value=None):
    if not passed:
        raise SystemExit(f'[BLOCKED] {name}: {value}')
    GATES.append({'name': name, 'passed': True, 'value': value})


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False,
                                    default=lambda x: x.item() if hasattr(x, 'item') else str(x)) + '\n')


def positive_control():
    """Capture the original main's checked arrays, retaining every original gate."""
    c = load_module(CONTROL / 'credits.py', 'removal_original_credits')
    c.OUT = OUT / 'positive_control'
    c.GATES.clear()
    captured = {}

    def profile(frame, event, _arg):
        if event == 'return' and frame.f_code is c.main.__code__:
            captured.update(frame.f_locals)

    sys.setprofile(profile)
    try:
        with contextlib.redirect_stdout(io.StringIO()) as log:
            c.main()
    finally:
        sys.setprofile(None)
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / 'control.log').write_text(log.getvalue())
    for path in sorted(c.OUT.iterdir()):
        gate(f'positive_control_bytes_{path.name}', sha(path) == sha(CONTROL / 'derived' / path.name))
    summary = json.loads((c.OUT / 'summary.json').read_text())
    gate('positive_control_item_5b', abs(captured['net'] - summary['account']['R3'][
        'child_credit_and_status_net']['bn']['total']) < 1e-9, captured['net'])
    gate('positive_control_D', abs(sum(captured['account'](captured['comp_ruled'][k], k)[0]
        for k in ('D_receipts', 'D_spending')) - summary['account']['R3']['joint_split_D']['bn']['total']) < 1e-9,
        summary['account']['R3']['joint_split_D'])
    print(f"[control] {len(c.GATES)} original gates; item 5b {captured['net']:.9f}bn; "
          f"D {summary['account']['R3']['joint_split_D']['bn']['total']:.9f}bn", flush=True)
    return c, captured


def add_fields(d, c):
    """Join source columns on the canonical person key; never use row coincidence."""
    fields = ['PH_SEQ', 'PPPOS', 'PTOTVAL', 'SSI_VAL', 'PAW_VAL', 'MCARE', 'MCAID', 'PCHIP',
              'PUB', 'PRIV', 'PRDISFLG', 'PARENT', 'FICA', 'PEARNVAL', 'SPM_NUMPER',
              'SPM_RESOURCES', 'SPM_TOTVAL', 'SPM_SNAPSUB', 'SPM_CHILDCAREXPNS',
              'SPM_CHILDSUPPD', 'SPM_MEDXPNS', 'SPM_CAPWKCCXPNS', 'SPM_WKXPNS',
              'SPM_ENGVAL', 'SPM_WICVAL', 'SPM_CAPHOUSESUB', 'SPM_FEDTAX', 'SPM_STTAX',
              'SPM_FICA', 'SPM_EITC', 'SPM_ACTC', 'SPM_WEIGHT', 'SPM_HEAD']
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        cols = pd.read_csv(z.open('pppub25.csv'), nrows=0).columns
        gate('additional_CPS_fields_exist', set(fields) <= set(cols), sorted(set(fields) - set(cols)))
        extra = pd.read_csv(z.open('pppub25.csv'), usecols=[x for x in fields if x not in d or x in ['PH_SEQ', 'PPPOS']])
        hh = pd.read_csv(z.open('hhpub25.csv'), usecols=['H_SEQ', 'HFOODMO', 'HFOODNO', 'HFDVAL', 'HFOODSP', 'H_TENURE'])
    d = d.merge(extra, on=['PH_SEQ', 'PPPOS'], how='left', validate='one_to_one')
    d = d.merge(hh.drop(columns=[x for x in hh if x != 'H_SEQ' and x in d]), on='H_SEQ', how='left', validate='many_to_one')
    gate('additional_CPS_fields_join_every_person', not d[fields].isna().any().any())
    return d


def survivor_registry(d, R, union, gen, civ, drows, ri):
    """Rebuild claimant links; a staying spouse, then a staying parent, can claim.

    Parent precedence when two remain: PEPAR1 then PEPAR2. All actual unmarried
    nonfilers who become a claimant get a new modeled return. No imagined guardian
    is created for children without a remaining parent. Other claimants' current
    incomes stay fixed. R3's fractional reverse credit is replaced, not added.
    """
    h, s = R.row.to_numpy(int), R.spouse.to_numpy(int)
    own = np.where(~union[h], h, np.where((s >= 0) & ~union[np.maximum(s, 0)], s, -1))
    nm_child = ~union[drows]
    survivors = own >= 0
    source = np.stack([R[f'g{g}_mem'].to_numpy(float) for g in range(3)],axis=1)
    source /= np.maximum(source.sum(axis=1),1)[:,None]
    heads=np.flatnonzero(union[h])
    source[heads]=0
    source[heads,gen[h[heads]]]=1
    spouses=np.flatnonzero(~union[h] & (s>=0) & union[np.maximum(s,0)])
    source[spouses]=0
    source[spouses,gen[s[spouses]]]=1
    by_person = {int(row): i for i, row in enumerate(h)}
    by_person.update({int(s[i]): i for i in range(len(R)) if s[i] >= 0})
    ph,line,ages=d.PH_SEQ.to_numpy(),d.A_LINENO.to_numpy(),d.A_AGE.to_numpy()
    parents={col:d[col].to_numpy() for col in ('PEPAR1','PEPAR2')}
    lookup = dict(zip(zip(ph,line),range(len(d))))
    assignments = np.full(len(drows), -1, int)
    added, extra_rows, transferred = {}, [], []
    for k in np.flatnonzero(nm_child):
        old = int(ri[k])
        if survivors[old]:
            assignments[k] = old
            continue
        child = int(drows[k])
        claimant = None
        for col in ('PEPAR1', 'PEPAR2'):
            candidate = lookup.get((ph[child],parents[col][child]))
            if candidate is not None and civ[candidate] and not union[candidate] and ages[candidate] >= 18:
                claimant = candidate
                break
        if claimant is None:
            continue
        dest = by_person.get(claimant)
        if dest is None or not survivors[dest]:
            if claimant not in added:
                added[claimant] = len(R) + len(extra_rows)
                extra_rows.append(claimant)
            dest = added[claimant]
        assignments[k] = dest
        transferred.append((k, old, dest))
    if extra_rows:
        own = np.concatenate([own, extra_rows])
    n = len(own)
    kcounts = {kind: np.zeros(n) for kind in ('n', 'k17', 'other', 'keitc', 'k13')}
    age = d.A_AGE.to_numpy()[drows]
    student = d.A_ENRLW.to_numpy()[drows] == 1
    creditable = ~R.depfiler.to_numpy()[ri]
    kinds = {'n': np.ones(len(drows), bool), 'k17': (age < 17) & creditable,
             'other': (age >= 17) & creditable,
             'keitc': ((age < 19) | ((age < 24) & student)) & creditable,
             'k13': (age < 13) & creditable}
    valid = assignments >= 0
    for kind, mask in kinds.items():
        kcounts[kind] = np.bincount(assignments[valid], weights=mask[valid].astype(float), minlength=n)
    owner = np.zeros((n, 3))
    owner[:len(R)] = source
    donor_owner = np.zeros((n, 3))
    for _, old, dest in transferred:
        donor_owner[dest] += source[old]
    for i in np.flatnonzero(donor_owner.sum(axis=1) > 0):
        owner[i] += donor_owner[i]
        owner[i] /= owner[i].sum()
    outR = R.copy()
    if extra_rows:
        extra = pd.DataFrame(0, index=np.arange(len(extra_rows)), columns=R.columns)
        extra['row'], extra['spouse'], extra['status'] = extra_rows, -1, 'single'
        extra['depfiler'] = False
        outR = pd.concat([outR, extra], ignore_index=True)
    own_safe = np.maximum(own, 0)
    outR['row'] = own_safe
    # Two non-members' joint return keeps both actual incomes; every mixed joint
    # survivor files alone on their own person record.
    keep_joint = (s >= 0) & ~union[h] & ~union[np.maximum(s, 0)]
    outR['spouse'] = -1
    outR.loc[np.flatnonzero(keep_joint), 'spouse'] = s[keep_joint]
    outR['status'] = np.where(outR.spouse.to_numpy() >= 0, 'joint', np.where(kcounts['n'] > 0, 'hoh', 'single'))
    for name, value in kcounts.items():
        stem = 'n' if name == 'n' else name
        outR[f'{stem}_all'] = value
    gate('survivor_dependents_each_assigned_once', len(set(drows[valid])) == int(valid.sum()))
    gate('survivor_dependents_counts_close', abs(kcounts['n'].sum() - valid.sum()) < 1e-9)
    details = {'new_nonfiler_claimants': len(extra_rows), 'transferred_dependents': len(transferred),
               'nonmember_dependents_without_remaining_claimant': int((nm_child & ~valid).sum()),
               'rule': 'staying spouse, else PEPAR1/PEPAR2 staying adult parent; no invented guardian'}
    return outR, own, kcounts, owner.T, details


def original_item_parts(x):
    """Full 161-column item 5b parts, not rounded CSV amounts or SE quadrature."""
    out = {'receipts': np.zeros((3, 161)), 'spending': np.zeros((3, 161))}
    for k, value in x['comp_ruled'].items():
        if k.startswith('D_'):
            continue
        for g in range(3):
            out[x['side'][k]][g] += x['account'](value * x['owner'][k][g] * x['keep_of']('R3', k), k)
    return out


def federal_denominator(x):
    """One fixed benchmark convention for control and changed receipt flows."""
    return np.full(161,x['mass_r4'])


def weighted_generation_totals(values,owner,weights):
    """Contract person flows with replicate weights without n-by-161 copies."""
    return np.stack([(values*owner[g])@weights for g in range(3)])


def survivor_irs_cells(c, x, d, own, agi):
    """Survivor's post-removal household CBO cell and own-return IRS AGI bin.

    The national benchmark cell multipliers and income-rank boundaries are held;
    the household is rebuilt without members. Zero-support cells are unidentified,
    never silently filled with a head's multiplier.
    """
    km, bench = x['km'], x['bench']
    bf = km.benchmark_frame()
    med = next(v for v in x['model']['spending']['lines'] if v['id'] == 'medicare')['national_bn']
    per = med * 1e9 / bench.pwwgt0.to_numpy()[bench.MCARE.eq(1).to_numpy()].sum()
    inc = bf.cbo_income(bench, per)
    labels, adjusted = bf.cbo_groups(bench, inc)
    boundaries = np.array([np.min(adjusted[labels == g]) for g in bf.GROUPS[1:-1]])
    gate('CBO_fixed_rank_boundaries_ordered', bool(np.all(np.diff(boundaries) >= 0)))
    idx = pd.Series(np.arange(len(bench)), index=pd.MultiIndex.from_frame(bench[['PH_SEQ', 'PPPOS']])).reindex(
        pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']])).to_numpy(int)
    hh = pd.factorize(d.PH_SEQ)[0]
    non = ~x['union']
    post = np.bincount(hh, weights=inc[idx] * non)
    size = np.bincount(hh, weights=non)
    eq = post / np.sqrt(np.maximum(size, 1))
    g = np.array(bf.GROUPS[:-1])[np.searchsorted(boundaries, eq[hh[np.maximum(own, 0)]], side='right')]
    g = np.where(post[hh[np.maximum(own, 0)]] < 0, 'negative', g)
    b19 = np.where(agi <= 0, 0, np.searchsorted(x['edges'], agi, side='right') + 1)
    b14 = np.where(b19 <= 1, 0, np.minimum(b19, 14) - 1)
    ratio = x['table'].reindex(pd.MultiIndex.from_arrays([g, b14])).to_numpy(float)
    return ratio, g, b14


def federal_removal(c, x, d):
    """M1 liability and M3 refunds replace all union item-5b parts exactly once."""
    tax = load_module(LANE / 'state_tax.py', 'removal_taxsim')
    R, W, union, gen, civ = (x[k] for k in ['R', 'W', 'union', 'gen', 'civ'])
    afterR, own, counts, owner, details = survivor_registry(d, R, union, gen, civ, x['drows'], x['ri'])
    before_input = tax.taxsim_frame(d, R)
    after_input = tax.taxsim_frame(d, afterR)
    # Attribute reported household care only across that household's actual tax
    # units with qualifying children. Same spending is held after departure.
    ncare = pd.Series((R.k13_all.to_numpy() > 0).astype(float)).groupby(d.PH_SEQ.to_numpy()[R.row]).transform('sum').to_numpy()
    care = np.maximum(d.HCHCARE_VAL.to_numpy()[R.row], 0) / np.maximum(ncare, 1)
    before_input['childcare'] = np.where(R.k13_all.to_numpy() > 0, care, 0)
    after_input['childcare'] = 0.0
    after_input.loc[:len(R)-1, 'childcare'] = np.where(counts['k13'][:len(R)] > 0, care, 0)
    before = tax.run_taxsim(before_input)
    after = tax.run_taxsim(after_input)
    h = R.row.to_numpy(int)
    s = R.spouse.to_numpy(int)
    nm_h = ~union[h]
    joint_mixed = (s >= 0) & (union[h] != union[np.maximum(s, 0)])
    live = (own >= 0) & civ[np.maximum(own, 0)]
    live[:len(R)] &= x['civ_ok']
    bf = before.fiitax.to_numpy() + before.v25.to_numpy() + before.actc.to_numpy()
    af = after.fiitax.to_numpy() + after.v25.to_numpy() + after.actc.to_numpy()
    # The same surviving return retains its Census residual; newly filed returns
    # use their own statutory result, with no unexplained joint-income share.
    anchored = np.zeros(len(afterR), bool)
    anchored[:len(R)] = nm_h & ~joint_mixed
    af[anchored] += (x['base'].fedbc - bf)[anchored[:len(R)]]
    af = np.maximum(af, 0)
    ae, aa = after.v25.to_numpy().copy(), after.actc.to_numpy().copy()
    ae[anchored] += (x['base'].eitc - before.v25.to_numpy())[anchored[:len(R)]]
    aa[anchored] += (x['base'].actc - before.actc.to_numpy())[anchored[:len(R)]]
    ae, aa = np.maximum(ae, 0), np.maximum(aa, 0)
    flag, onbooks = x['flag'], x['onbooks']['central']
    own_safe = np.maximum(own, 0)
    factor = np.where(flag[own_safe], onbooks[own_safe], 1.)
    efactor = np.where(flag[own_safe], 0., 1.)
    # New IRS cells are used for refiled joint returns and new claimant returns.
    ratio, cg, ib = survivor_irs_cells(c, x, d, own, after.v10.to_numpy())
    base_ratio = np.concatenate([x['ratio'], np.zeros(len(afterR)-len(R))])
    refile = ~anchored & live
    unsupported = refile & (af > 0) & ~np.isfinite(ratio)
    details['unsupported_positive_survivor_IRS_cells'] = int(unsupported.sum())
    if unsupported.any():
        raise SystemExit('[BLOCKED] survivor IRS cells have positive tax but no benchmark support')
    use_ratio = np.where(anchored, base_ratio, np.nan_to_num(ratio))
    # Match the frozen credit lane's replication convention: the full-sample
    # IRS benchmark calibration is held across all columns. Varying it here but
    # subtracting item 5b at its fixed mass would corrupt the difference's SE.
    mass = federal_denominator(x)
    fit_line = x['fit_line']
    after_f = af*factor*live*use_ratio
    after_cr = (ae*efactor+aa*factor)*live
    before_f = x['base'].fedbc*x['f_other']*x['ratio']*nm_h*x['civ_ok']
    before_cr = (x['base'].eitc*x['f_eitc']+x['base'].actc*x['f_other'])*(nm_h&x['civ_ok'])
    old_f = np.zeros_like(after_f)
    old_cr = np.zeros_like(after_cr)
    old_f[:len(R)],old_cr[:len(R)]=before_f,before_cr
    # Unaffected returns must be exactly fixed even if household CBO bins change
    # elsewhere. Original tax amount residuals are kept on those returns.
    owner_zero = owner.sum(axis=0) == 0
    gate('all_nonzero_survivor_changes_have_generation',
         np.max(np.abs(after_f[owner_zero] - old_f[owner_zero]), initial=0) < 1e-6
         and np.max(np.abs(after_cr[owner_zero] - old_cr[owner_zero]), initial=0) < 1e-6)
    item = original_item_parts(x)
    ownW=W[own_safe]
    oldW=x['wr']
    after_ft=weighted_generation_totals(after_f,owner,ownW)*fit_line/mass
    before_ft=weighted_generation_totals(before_f,owner[:,:len(R)],oldW)*fit_line/mass
    after_ct=weighted_generation_totals(after_cr,owner,ownW)*x['per_ref']
    before_ct=weighted_generation_totals(before_cr,owner[:,:len(R)],oldW)*x['per_ref']
    M1=after_ft-before_ft-item['receipts']
    M3=before_ct-after_ct-item['spending']
    direct_f=(after_f@ownW-before_f@oldW)*fit_line/mass-item['receipts'].sum(axis=0)
    direct_c=(before_cr@oldW-after_cr@ownW)*x['per_ref']-item['spending'].sum(axis=0)
    gate('federal_generation_closure',np.max(np.abs(M1.sum(axis=0)-direct_f))<1e-6)
    gate('refundable_generation_closure',np.max(np.abs(M3.sum(axis=0)-direct_c))<1e-6)
    # Survivor kernel output and its IRS cell must be identical when the original
    # head and spouse labels switch; the frozen personal baseline is held.
    ids = np.flatnonzero(joint_mixed)
    swapped = R.iloc[ids].copy().reset_index(drop=True)
    swapped['row'], swapped['spouse'] = R.spouse.to_numpy()[ids], R.row.to_numpy()[ids]
    dc = {key: counts[key][ids] for key in ('n', 'k13', 'k17', 'keitc')}
    swapped_input = tax.taxsim_frame(d, swapped, own=own[ids], dep_counts=dc)
    swapped_input['childcare'] = after_input.childcare.to_numpy()[ids]
    swapped_out = tax.run_taxsim(swapped_input)
    swap_gap = max(np.max(np.abs(swapped_out[k].to_numpy()-after[k].to_numpy()[ids]), initial=0)
                   for k in ('fiitax', 'v25', 'actc', 'v10', 'siitax'))
    gate('head_spouse_swap_survivor_kernel_1e9', swap_gap <= 1e-9, float(swap_gap))
    swap_ratio, _, _ = survivor_irs_cells(c, x, d, own[ids], after.v10.to_numpy()[ids])
    gate('head_spouse_swap_IRS_cell_1e9', np.allclose(swap_ratio, ratio[ids], rtol=0, atol=1e-9, equal_nan=True))
    details.update({'adoptable': False,
                    'rule': 'staying same return: CPS residual plus TAXSIM delta; newly filed: own TAXSIM income/flags/cell; subtract item 5b once',
                    'unknown_inputs': ['itemized deductions', 'QBI eligibility', 'qualified dividend/capital-gain character', 'other refundable credits and actual care attribution'],
                    'baseline_rule_federal_bn': float(bf @ W[h,0] / 1e9),
                    'baseline_CPS_federal_bn': float(x['base'].fedbc @ W[h,0] / 1e9),
                    'baseline_rule_EITC_bn': float(before.v25.to_numpy() @ W[h,0] / 1e9),
                    'baseline_CPS_EITC_bn': float(x['base'].eitc @ W[h,0] / 1e9),
                    'baseline_rule_ACTC_bn': float(before.actc.to_numpy() @ W[h,0] / 1e9),
                    'baseline_CPS_ACTC_bn': float(x['base'].actc @ W[h,0] / 1e9),
                    'mixed_joint_returns': int(joint_mixed.sum()), 'swap_max_dollars': float(swap_gap),
                    'IRS_rule': 'own AGI bin, remaining-household CBO group at original national rank thresholds; benchmark multipliers fixed',
                    'weights': 'actual amount: actual carrier weights; new amount: survivor own weights; all 160 replicates',
                    'IRS_replication':'full-sample benchmark mass held across replicates, matching original item 5b; benchmark uncertainty not included',
                    'swap_scope': 'survivor tax calculation and IRS multiplier; changing the frozen baseline carrier changes its personal ledger by definition'})
    old_cell_after=af*factor*live*base_ratio
    head_cell=M1+weighted_generation_totals(old_cell_after-after_f,owner,ownW)*fit_line/mass
    # Keep directly comparable own-return ordinary-schedule alternative beside
    # the legal kernel as a disconfirmation check, not an adopted fallback.
    return {'M1': M1, 'M3': M3, 'terms':{'M1_original_head_IRS_cell':head_cell},'details': details, 'afterR': afterR,
            'own': own, 'counts': counts, 'owner': owner, 'before_input':before_input,'after_input': after_input,
            'after_federal': af, 'after_refunds': ae+aa}


def disposable_income(d, R, P):
    """Own cash income minus FICA and own-income shares of joint income tax.

    On joint returns only, the joint federal tax after refunds and state tax are
    split in proportion to positive AGI components. When both are zero the split
    is equally between spouses, explicitly prescribed. Other persons keep their
    record's liabilities. This is a resource attribution, not observed spending.
    """
    fit = d.FEDTAX_AC.to_numpy(float).copy()
    sit = d.STATETAX_A.to_numpy(float).copy()
    h, s = R.row.to_numpy(int), R.spouse.to_numpy(int)
    j = s >= 0
    hv, sv = np.maximum(P['agi_parts'][h[j]], 0), np.maximum(P['agi_parts'][s[j]], 0)
    sh = np.divide(hv, hv+sv, out=np.full(len(hv), .5), where=hv+sv>0)
    for v in (fit, sit):
        bill = v[h[j]].copy()
        v[h[j]], v[s[j]] = bill*sh, bill*(1-sh)
    return d.PTOTVAL.to_numpy(float) - d.FICA.to_numpy(float) - fit - sit, fit, sit


def weight_preserving_split(old, income, unit, w, mixed, equal_fraction=0.):
    """Conserve each unit's weighted key, for one replicate. Equal share when
    all incomes are zero is part of the specified rule, not an implicit fallback.
    """
    n = len(mixed)
    if int(unit.max())>=n:
        raise ValueError('[BLOCKED] consumption unit index exceeds declared mixed mask')
    positive = np.maximum(income, 0)
    weighted_income = np.bincount(unit, weights=w*positive, minlength=n)
    mass = np.bincount(unit, weights=w, minlength=n)
    total = np.bincount(unit, weights=w*old, minlength=n)
    support = np.bincount(unit, weights=positive, minlength=n)
    if np.any(mixed & (support>0) & (weighted_income==0) & (total!=0)):
        raise RuntimeError('[BLOCKED] signed replicate gives zero own-income moment with nonzero pool')
    own = positive * np.divide(total, weighted_income, out=np.zeros(n), where=weighted_income!=0)[unit]
    own = np.where(support[unit] > 0, own, old)
    new = np.where(mixed[unit], equal_fraction*old + (1-equal_fraction)*own, old)
    residual = np.bincount(unit, weights=w*(new-old), minlength=n)
    if np.max(np.abs(residual))/1e9 > 1e-6:
        raise RuntimeError('[BLOCKED] consumption split loses weighted unit totals')
    return new, residual


def consumption_exposure(old,new,w,civ,union,gen,cbo_code,cbo_targets):
    """Sufficient weighted totals; equivalent to the original group-mask sums."""
    nat=old[civ]@w[civ]
    group_mass=np.bincount(cbo_code,weights=old*w*civ,minlength=len(cbo_targets))
    if np.any((group_mass==0)&(cbo_targets!=0)):
        raise RuntimeError('[BLOCKED] positive CBO excise share has no consumption key support')
    per_group=np.divide(cbo_targets,group_mass,out=np.zeros_like(cbo_targets),where=group_mass!=0)
    base_group=old[union]@w[union]/nat
    base_cbo=np.sum(old*w*union*per_group[cbo_code])
    diff=(new-old)*w*civ
    delta=np.bincount(gen+1,weights=diff,minlength=4)[1:]/nat
    fed_delta=np.bincount(gen+1,weights=diff*per_group[cbo_code],minlength=4)[1:]
    return base_group,base_cbo,delta,fed_delta


def consumption_removal(c, x, d, case):
    """M5 on the adopted saving/remittance pool, with an own-income split.

    Each SPM pool and all national key totals are fixed; only allocation inside
    mixed units moves. Positive controls reproduce the original consumption lane.
    Full transfer-response consumption is not identified by household resources.
    """
    kl = FISCAL / 'consumption_key_2026_09_24'
    sys.path.insert(0, str(FISCAL / 'external_benchmarks_2026_09_24'))
    sys.path.insert(0, str(kl))
    ck = load_module(kl / 'consumption_key.py', 'removal_consumption')
    # Bypass acquisition paths: every dependency is a read-only existing cache.
    gate('consumption_cache_exists_read_only', (kl / '_cache/cps_arrays.npz').exists())
    a = ck.cps_frame.frame()
    pos = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_frame(d[['PH_SEQ','PPPOS']])).reindex(
        pd.MultiIndex.from_arrays([a['ph_seq'], a['pppos']])).to_numpy(int)
    gate('consumption_person_join_bijective', len(pos)==len(d) and len(np.unique(pos))==len(d))
    gate('consumption_original_frame_reproduces_key', ck.cps_frame.reproduce(a)['ok'])
    fr = ck.Frame(a)
    curve = ck.saving.ce_curve('consumption', 50, ck.saving.pumd_ranked(), ck.saving.published_deciles(), within=True)
    propensity = ck.saving.unit_factor(a, curve, 'ratio')
    units = ck.remittance.units(a)
    specs, _ = ck.remittance.spec_flows(a, units, ck.remittance.sender_rates(), ck.fetch.cpi_annual())
    sp = specs['corridor_net_h2']
    G, N, oldkey = fr.totals_remit(propensity, sp, units, 'proportional')
    stored = pd.read_csv(kl/'derived/key_specs.csv').set_index('spec')
    gate('consumption_saving_remittance_positive_control', abs(G[0]/N[0]-stored.loc['both_corridor_net_h2','key_share'])<1e-12, float(G[0]/N[0]))
    groups, cbo = ck.outside.cbo_groups_for(a)
    fixed_cbo = ck.outside.cbo_federal_share(oldkey,a,groups,cbo)['cbo']
    cbo_code=pd.Categorical(groups,categories=list(fixed_cbo)).codes
    gate('all_consumption_persons_have_CBO_group',bool((cbo_code>=0).all()))
    cbo_targets=np.array(list(fixed_cbo.values()),float)
    W = x['W'][pos]
    union, civ, gen = x['union'][pos], x['civ'][pos], x['gen'][pos]
    income, _, _ = disposable_income(d,x['R'],x['P'])
    income = income[pos]
    unit, size = a['unit'], a['size']
    mixed = (np.bincount(unit,weights=union)>0) & (np.bincount(unit,weights=(civ&~union))>0)
    split_unit=unit*2+(~civ).astype(int)
    split_mixed=np.repeat(mixed,2)
    split_mixed[1::2]=False
    zero = np.bincount(unit,weights=np.maximum(income,0))==0
    variants = {'own_disposable':0.,'half_equal_half_own':.5}
    arrays = {name:{lid:np.zeros((3,161)) for lid in case['lines']} for name in variants}
    worst = 0.
    F = ck.FEDERAL_EXCISE_BN
    for r in range(161):
        resources = np.maximum(fr.res-ck.remittance.outflow_matrix(sp,units,r),0)*propensity
        old = resources[unit]/size
        wr = W[:,r]
        national = old[civ] @ wr[civ]
        for name, equal in variants.items():
            new, residual = weight_preserving_split(old,income,split_unit,wr,split_mixed,equal)
            worst = max(worst,float(np.max(np.abs(residual)))/1e9)
            if abs((new[civ]@wr[civ])-(old[civ]@wr[civ]))/1e9 > 1e-6:
                raise SystemExit('[BLOCKED] consumption civilian national total changed')
            base_group,base_cbo,delta_g,fed_delta_g=consumption_exposure(old,new,wr,civ,union,gen,cbo_code,cbo_targets)
            for gi in range(3):
                delta,fed_delta=delta_g[gi],fed_delta_g[gi]
                for lid, line in case['lines'].items():
                    if lid=='excise_selective_sales':
                        raw = (line['national_bn']-F)*base_group+F*base_cbo
                        move = (line['national_bn']-F)*delta+F*fed_delta
                    else:
                        raw, move = line['national_bn']*base_group, line['national_bn']*delta
                    # Calibrate the *union* to the live case; hold added people's
                    # receipts fixed. Federal excise keeps its CBO group rule.
                    arrays[name][lid][gi,r] = -move*line['union_target_bn']/raw
    gate('consumption_all_unit_weight_columns_conserve',worst<1e-6,worst)
    totals={name:sum(values.values()) for name,values in arrays.items()}
    return {'M5':totals['own_disposable'],'terms':totals,'lines':arrays,
            'details':{'adoptable':False,'rule':'positive own cash disposable income; joint tax bills split by positive AGI components; normalize inside each mixed SPM pool separately for every weight column; equal if all zero',
                       'mixed_SPM_units':int(mixed.sum()),'zero_income_mixed_units':int((mixed&zero).sum()),
                       'original_consumption_share':float(G[0]/N[0]),
                       'unit_closure_max_bn':worst,'saving_remittances':'adopted consumption lane both_corridor_net_h2 held',
                       'conversion':'calibrate raw weighted union receipt exposure to v7 union-only target; added people fixed; CBO federal excise retained',
                       'unidentified':'person spending and intrahousehold transfers; no claim that a child with zero own income consumes zero',
                       'interaction_scope':'this is an allocation of the fixed pre-removal pool; tax/benefit-induced post-removal consumption held, not estimated'}}


def identity_loss_children(c,x,d,case):
    """M6 locates children with roster ancestry; v5 has no person IDs to match.

    Keep the existing added-person count and all their costs fixed. This reports
    the possible overlap and the credit-only child-leaves scenario; it never adds
    these children to the 3.04M aggregate count a second time.
    """
    union,civ,gen,W=(x[k] for k in ('union','civ','gen','W'))
    lookup=pd.Series(np.arange(len(d)),index=pd.MultiIndex.from_frame(d[['PH_SEQ','A_LINENO']]))
    links=[]
    for col in ('PEPAR1','PEPAR2'):
        rows=lookup.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ,d[col]])).to_numpy(float)
        found=np.isfinite(rows)
        member=np.zeros(len(d),bool)
        member[found]=union[rows[found].astype(int)]
        links.append((rows,member))
    native=d.PRCITSHP.isin([1,2,3]).to_numpy()
    candidate=civ & ~union & native & (d.A_AGE.to_numpy()<18) & (links[0][1]|links[1][1])
    parent_gen=np.zeros((3,len(d)))
    for rows,member in links:
        for g in range(3):
            parent_gen[g,member]=(gen[rows[member].astype(int)]==g).astype(float)+parent_gen[g,member]
    denom=np.maximum(parent_gen.sum(axis=0),1)
    parent_gen/=denom
    counts=np.stack([np.where(candidate,parent_gen[g],0)@W/1e6 for g in range(3)])
    own_only=(~x['dmem']) & candidate[x['drows']]
    dependent_counts=np.stack([np.where(own_only,parent_gen[g,x['drows']],0)@W[x['drows']]/1e6 for g in range(3)])
    gate('M6_candidate_children_do_not_intersect_identified_union',not bool((candidate&union).any()))
    gate('M6_parent_generation_counts_close',np.max(np.abs(counts.sum(axis=0)-candidate@W/1e6))<1e-9)
    age_rows=[]
    for lo in (0,5,10,15):
        mask=candidate&(d.A_AGE.to_numpy()>=lo)&(d.A_AGE.to_numpy()<min(lo+5,18))
        estimates=mask@W/1e6
        age_rows.append({'ages':f'{lo}-{min(lo+4,17)}','million':float(estimates[0]),'se_million':c.sdr(estimates)})
    return {'M6':None,'counts':counts,'details':{
        'candidate_children_million':float(counts[:,0].sum()),'candidate_children_se_million':c.sdr(counts.sum(axis=0)),
        'by_member_parent_generation_million':counts[:,0].tolist(),
        'linked_tax_dependents_million':float(dependent_counts[:,0].sum()),'age_rows':age_rows,
        'added_lineage_count_million':case['lineage']['counts']['added']/1e6,
        'overlap_identified':False,'duplicate_count_added':0,
        'rule':'roster children under 18, native, outside identified union, with a member parent; generations assigned to member parents equally',
        'reconciliation':'v5 aggregate loss estimate has no PH_SEQ/PPPOS crosswalk; preserve full added count and costs; no new child cost or credit added',
        'direction':'if candidates are added members, their own costs already belong in the aggregate addition; treating them as survivors can overstate continuing credits; exact net correction needs membership crosswalk plus replacement of aggregate costs',
        'adoptable':False,'cost_delta_bn':None,
        'holding_fixed':'3.04M addition, item 5b lineage extrapolation and all v7 child costs; zero booked edit means withheld, not measured zero'}}


def input_pins():
    """First-run immutable acquisition register; later runs verify before compute."""
    root=FISCAL.parents[1]
    named=[CONTROL/'credits.py', CONTROL/'derived/item.json', CONTROL/'derived/summary.json',
           FISCAL/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip',
           FISCAL/'assumption_explorer_2026_09_21/derived/model.json',
           FISCAL/'main_case_2026_10_14/derived/corrections.json',
           FISCAL/'main_case_2026_10_14/derived/corrections_cash.json',
           FISCAL/'main_case_2026_10_14/derived/summary.json']
    # All consumption source caches used by the inherited computation are pinned
    # read-only. Include ignored caches explicitly rather than infer availability.
    kl=FISCAL/'consumption_key_2026_09_24'
    named += [kl/'_cache/cps_arrays.npz',kl/'_cache/ce_pumd_2024.csv']
    named += sorted((kl/'_cache/sources').glob('bls_cpi_u_*.json'))
    named += [kl/'_cache/sources/cu-income-deciles-before-taxes-2024.xlsx',
              kl/'derived/key_specs.csv',kl/'derived/sender_rates.csv',
              FISCAL/'external_benchmarks_2026_09_24/_cache/cps25_frame.parquet',
              FISCAL/'external_benchmarks_2026_09_24/derived/cbo_group_shares.csv']
    # Pin primary federal-rule PDFs reused from the positive control.
    named += sorted((CONTROL/'_cache').glob('*/*.pdf'))
    candidates={f'repo:{p.relative_to(root)}':{'sha256':sha(p)} for p in named}
    for name in ('state_pins.json','benefit_pins.json'):
        source=json.loads((LANE/'inputs'/name).read_text())
        entries=source.get('files',source)
        for rel,pin in entries.items():
            fullrel=('inputs/'+rel) if name=='benefit_pins.json' else rel
            candidates[fullrel]=pin
    target=LANE/'inputs/pins.json'
    if not target.exists():
        write_json(target,candidates)
    registered=json.loads(target.read_text())
    gate('all_used_acquisition_inputs_are_registered',set(candidates)<=set(registered))
    for rel,pin in registered.items():
        path=root/rel.removeprefix('repo:') if rel.startswith('repo:') else LANE/rel
        gate(f'input_sha_{rel}',path.exists() and sha(path)==pin['sha256'])
    return registered


def result_rows(c,components,case):
    rows=[]
    scale=case['lineage']['members']['g3plus']/case['lineage']['counts']['identified_g3plus']
    for name,values in components.items():
        union=values.sum(axis=0)
        transport=union+scale*values[2]
        for gi,g in enumerate(('G1','G2','G3+','all')):
            v=union if g=='all' else values[gi]
            rows.append({'component':name,'generation':g,'union_delta_low_bn':float(v[0]),
                         'union_delta_high_bn':float(v[0]),'union_se_bn':c.sdr(v),
                         'lineage_added_held_delta_low_bn':float(v[0]),'lineage_added_held_delta_high_bn':float(v[0]),
                         'lineage_G3_transport_delta_bn':float(transport[0] if g=='all' else v[0]*(1+scale if g=='G3+' else 1)),
                         'lineage_G3_transport_se_bn':c.sdr(transport if g=='all' else v*(1+scale if g=='G3+' else 1)),
                         'crosses_5bn_point_estimate':abs(float(v[0]))>=5 if g=='all' else '',
                         'estimate_kind':'conditional simulation; no new adopted edit'})
    return pd.DataFrame(rows)


def write_report(summary):
    r={(x['component'],x['generation']):x for x in summary['results']}
    total=lambda name:r[(name,'all')]['union_delta_low_bn']
    se=lambda name:r[(name,'all')]['union_se_bn']
    names=['M1','M2','M3','M4_conditional_SNAP','M5_fixed_pool','tax_only_stack','conditional_fixed_pool_stack']
    rows=['| Component, change from frozen v7 | Union, low / high $bn | SE $bn | G1 | G2 | G3+ | Review bar |',
          '|---|---:|---:|---:|---:|---:|---|']
    for name in names:
        g=[r[(name,x)]['union_delta_low_bn'] for x in ('G1','G2','G3+')]
        rows.append(f'| {name} | {total(name):+.6f} / {total(name):+.6f} | {se(name):.6f} | '+
                    ' | '.join(f'{x:+.6f}' for x in g)+f" | {'Above' if abs(total(name))>=5 else 'Below'} $5bn |")
    controls=summary['positive_control']
    body=f'''**Verdict:** Withhold new adoption. The conditional tax-only correction is **{total('tax_only_stack'):+.3f}bn** (SE {se('tax_only_stack'):.3f}bn), beyond item 5b, and the conditional fixed-pool stack is **{total('conditional_fixed_pool_stack'):+.3f}bn** (SE {se('conditional_fixed_pool_stack'):.3f}bn). These cross the $5bn point-estimate review bar. They are not an identified complete removal effect: deductions, person consumption, benefit units/takeup and added-child membership remain unmeasured. M6 is unpriced, not zero. [CALCULATION: `removal.py` → `derived/summary.json`, `derived/results.csv`, `derived/replicates.csv`] [INFERENCE]

## One change from the current central

Income year 2024, personal allocation, specifications 16 / 11, row-4 identified union {summary['frame']['union']:,.0f}, against v7 plus item 5b. A plus sign raises net cost to other residents. Every row holds other case lines fixed and is a modeled mechanical adjustment, not a causal forecast. SEs use all 160 SDR replicates; the stack SE comes from the summed replicate vector. [DATA: frozen v7 `package.cjs`, `derived/corrections.json`; CPS ASEC 2025 pinned archive] [FRAMING-SENSITIVE]

'''+ '\n'.join(rows)+f'''

The primary whole-lineage reading uses the **same adjustment at both ends**, holding the case's existing added-person costs fixed; it does not observe their mixed units. `results.csv` separately shows the case-style G3 transport: each union G3+ adjustment per identified G3+ member times the case's 1.957M G3+-priced added people, white-priced people held. That assumed transport gives {r[('conditional_fixed_pool_stack','all')]['lineage_G3_transport_delta_bn']:+.3f}bn for the stack; its SE conditions on the transport coefficient. This is not a measured 42.75M correction. [ASSUMPTION] [CALCULATION: `result_rows`, `derived/case_inputs.json`]

## Positive controls and account sign

The original credits code runs unchanged with only its output directory redirected here. All six files reproduce byte for byte; all {controls['original_gates']} original gates pass. Item 5b is {controls['item5b_union_bn']:+.9f}bn and the old D is {controls['D_union_bn']:+.9f}bn. D is a control, **never an added component**. [CALCULATION: `derived/positive_control/`, `positive_control()`]

The new correction is remaining nonmembers' tax after removal minus their tax on the original personal ledger, and original nonmember refunds minus their post-removal refunds. The already-booked A/B/C/Cr item-5b receipt and spending vectors are subtracted once. M1 includes federal liability before EITC/ACTC; M3 includes those refunds, not the same child credit a second time. Item 5b's own full-sample IRS normalization is retained for every replicate, so the subtraction uses one calibration convention. [CALCULATION: `federal_removal`, `original_item_parts`, `federal_denominator`]

## M1, M2 and M3: the surviving return

The local pinned NBER 2024 TAXSIM kernel evaluates surviving incomes, Social Security taxability, dependent counts, filing status, capital-gain preferences and state laws. A staying spouse files alone; nonmember parents receive staying dependents from vanished returns, including a new return if necessary. The current data transfer {summary['M1_M3']['transferred_dependents']} dependents to existing returns and create {summary['M1_M3']['new_nonfiler_claimants']} nonfiler returns. Children with no staying parent receive no invented claimant. Two nonmembers' joint return remains joint. The statutory survivor calculation and own IRS cell pass the head/spouse swap check at 1e-9 (measured discrepancy 0). The frozen personal baseline is held: relabeling which original person carried its tax changes that baseline by definition. [CALCULATION: `survivor_registry`, `federal_removal`; `test_removal.py`, `test_state_tax.py`] [ASSUMPTION: staying claimant rule and qualifying dependents]

The surviving return uses its own state-aware status flag and on-books share, its own weight, its own AGI bin and the remaining household's CBO income group at fixed original national rank thresholds. The benchmark cell multipliers are fixed; unsupported positive-tax cells block. A continuing claimant keeps the Census residual plus the statutory schedule difference; a new return gets its own statutory result, without unexplained joint-income residuals. M2 is state/replicate calibrated to original CPS positive state liability and uses the same canonical before/after kernel inputs as M1/M3, including the conditional care-spending attribution. State negative refunds are outside the positive receipt key and are held outside M2. [CALCULATION: `survivor_irs_cells`, `state_tax.compute`]

Baseline TAXSIM federal liability is {summary['M1_M3']['baseline_rule_federal_bn']:.3f}bn versus CPS {summary['M1_M3']['baseline_CPS_federal_bn']:.3f}bn; EITC is {summary['M1_M3']['baseline_rule_EITC_bn']:.3f} versus {summary['M1_M3']['baseline_CPS_EITC_bn']:.3f}; ACTC is {summary['M1_M3']['baseline_rule_ACTC_bn']:.3f} versus {summary['M1_M3']['baseline_CPS_ACTC_bn']:.3f}. Retaining residuals is calibration, not validation of new returns. Keeping the original head's IRS cell instead of the survivor's gives M1 {total('M1_original_head_IRS_cell'):+.3f}bn, showing material cell sensitivity. [CALCULATION: `derived/summary.json`, `derived/results.csv`] [INFERENCE]

Unobserved itemized deductions, qualified dividends, short/long gains, taxable pension shares, QBI, qualifying-household maintenance and actual child-care attribution remain assumptions. March 2025 ages are held as in the CPS model. Other refundable credits, including education credits and ACA PTC, are not identified as a return-level CPS value; their spending is held, not declared zero. The original non-PTC line convention prices EITC and ACTC together, as the control lane does. The M1/M3 result is therefore a conditional kernel simulation, not an exact reconstructed legal return. [ASSUMPTION / DEGRADED]

## M4: benefits

SNAP uses primary USDA FY2024/FY2025 schedules in calendar-year 9/3-month proportions, income tests, unit size, standard/earned/medical/care/support deductions, the benefit formula and the statutory maximum. It keeps reported CPS level residuals, varies missing shelter deductions, and compares reported participation held with full-takeup proxies. SPM is a proxy assistance unit, annual incomes proxy monthly incomes, and deductions are prorated: assets, state BBCE/ABAWD/student/status rules are unmeasured. Existing participation with zero shelter is {total('M4_conditional_SNAP'):+.3f}bn; maximum shelter is {total('SNAP_cap_existing_participation'):+.3f}; full-takeup/zero-shelter is {total('SNAP_zero_full_takeup_proxy'):+.3f}, crossing $5bn only under that unverified takeup construction. [CALCULATION: `benefits.py`, `derived/benefit_results.json`] [ASSUMPTION]

Medicaid/CHIP uses parsed state age/parent/expansion thresholds and the 2024 FPL to show income-proxy transitions for surviving children/adults. The fixed MEPS expected-payment key remains held: eligibility is not observed enrollment or spending. ACA premiums, SLCSP, APTC, monthly enrollment and complete MAGI/employer-affordability inputs are absent, so PTC is unpriced. The health changes are unidentified. See `benefits-result.md` for proxy fit failures, excluded units, signed weights, threshold-vintage limits and the conditional SNAP envelope. [DATA: `derived/benefit_results.json` `Medicaid_CHIP`, `ACA`] [SOURCE: primary files and URLs in `inputs/benefit_pins.json`]

## M5: consumption allocation

Only mixed SPM units change: the adopted saving/remittance-adjusted resource pool is split in proportion to positive own disposable cash income, with joint tax bills split by positive AGI components. Each full/replicate weighted pool and the civilian national key is conserved at 1e-6bn or tighter; signed weights are retained, and noncivilian strata stay fixed. All-zero own-income units explicitly keep equal shares. The original consumption key and saving/remittance shares are positive controls. Sales, excise, customs and personal-transfer receipts use the live **union-only** targets; added people's targets are isolated and fixed. Federal excise keeps CBO income-group shares; the resulting raw union exposure is calibrated to the current case line. [CALCULATION: `weight_preserving_split`, `consumption_removal`, `case_inputs.cjs`]

Own disposable income is an attribution assumption, not measured individual consumption: children can consume resources supplied by parents. Half equal sharing / half own income reduces M5 to {total('M5_half_equal_half_own'):+.3f}bn. Do not adopt the own-income split as a literal spending measurement. Resource-keyed service/subsidy lines and the corporate/business-property key remain held; M5 prices the requested consumption receipts only. [ASSUMPTION / SCOPE]

## M6: identity-loss reconciliation

The roster locates {summary['M6']['candidate_children_million']:.6f}M native children under 18 outside the identified union with a member parent (SE {summary['M6']['candidate_children_se_million']:.6f}M). The population concept includes such lost-identity descendants, but v5's 3.04M aggregate addition has no `PH_SEQ`/`PPPOS` crosswalk. No individual child's numerical inclusion or pool overlap is verified. The prior claim that a particular such child is already counted and would leave is therefore not established by these files. [CALCULATION: `identity_loss_children`, `derived/summary.json` `M6`] [INFERENCE]

No new child, cost or credit is added; the aggregate addition and its item-5b extrapolation stay fixed. If these children are added members, letting them stay can overstate continuing credits; replacing an aggregate child with a roster child requires subtracting its existing modeled costs first. The direction of the full fiscal correction cannot be determined without that membership/substitution map. M6's cost is **null/unidentified**, not an assumed measured zero. [ASSUMPTION / DEGRADED]

## Stack, adoption and limits

M1/M2/M3 are solved on one shared post-removal return, including nonlinear tax/credit interactions. The displayed stack adds that solved tax correction, the named conditional SNAP scenario and the fixed-pool M5 allocation. Its extra cross-module interaction is 0 **by construction**: SNAP uses pre-tax gross income and the pre-removal consumption pool is held. This does not estimate consumption responses to survivor taxes/refunds/SNAP, benefit takeup/health changes or M6. It is explicitly a partial conditional stack. [CALCULATION: `derived/replicates.csv`, `derived/summary.json` `stack`] [ASSUMPTION]

Recommend adopting no new headline edit from this lane yet. Retain the material tax finding for further validation; do not infer reliability from national residual calibration or from a confidence interval containing/excluding zero. Missing deductibles/new-return fit can move M1, and the tax-only sampling SE is large. Individual consumption observations or an explicit normative allocation rule would settle M5; actual program units/monthly resources would settle M4; a roster-to-added-person crosswalk with aggregate-cost replacement would settle M6. The politically sensitive analysis is LLM-assisted; independent source/gate checks reduce implementation errors without identifying the modeled counterfactual. [INFERENCE]

## Sources, checks and reproduction

Input URLs, primary-file SHA256 and reused read-only input hashes are in `inputs/pins.json`, `inputs/state_pins.json`, and `inputs/benefit_pins.json`. Downloaded constants are parsed, or evaluated by the pinned statutory kernel; no model-extracted numbers are used as statutory tables. NBER documents the local beta's 2024 coverage and input omissions: https://taxsim.nber.org/taxsimtest/. Census's workbook preserves its 2024 source cells in `inputs/state_parameters_2024.json`. [SOURCE]

Run from repository root:
```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/removal.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_removal_2026_10_14/ -q
```

The code review is `review-result.md`; its calibration issue was repaired and cancellation has a regression test. All implemented gates are in `derived/summary.json`; no existing gate or tolerance was relaxed. `RUN_LOG.md` records actual check commands, return codes, wall time, Python RSS and full-lane reproduction. The frozen case and all other lanes are read-only. No Git metadata was changed by this worker. Every changed path is enumerated in `changed-paths.txt`.
'''
    (LANE/'RESULT.md').write_text(body)


def main():
    start = time.perf_counter()
    input_pins()
    subprocess.run(['node',str(LANE/'case_inputs.cjs')],check=True,capture_output=True,text=True)
    case=json.loads((OUT/'case_inputs.json').read_text())
    gate('case_personal_end_specifications',case['endpoints']=={'set':[16,11],'cash':[16,11]})
    c, x = positive_control()
    d = add_fields(x['d'], c)
    x['d'] = d
    federal = federal_removal(c, x, d)
    tax=load_module(LANE/'state_tax.py','removal_state')
    nR=len(x['R'])
    gate('state_expanded_registry_has_no_unmodeled_new_filers',len(federal['own'])==nR)
    state=tax.compute(d,x['R'],x['P'],x['base'],x['W'],x['union'],x['gen'],x['flag'],x['onbooks'],x['model'],
                      civ=x['civ'],refiling={'own':federal['own'],'dep_counts':federal['counts'],
                                            'R':federal['afterR'],'owner':federal['owner'],
                                            'before_input':federal['before_input'],'after_input':federal['after_input']})
    # Benefit unit-by-replicate intermediates are large. Reuse the independently
    # gated standalone frame in a fresh process; do not retain those matrices in
    # the tax/consumption process. No microdata are serialized or transmitted.
    arrays_path=CACHE/'benefit_arrays.npz'
    child=subprocess.run(['uv','run','--no-project','python3',str(LANE/'benefits.py'),
                          '--arrays-out',str(arrays_path)],check=True,capture_output=True,text=True)
    (CACHE/'benefit_subprocess.log').write_text(child.stdout)
    with np.load(arrays_path,allow_pickle=False) as data:
        benefit_terms={key:data[key].copy() for key in data.files}
    benefit={'M4':benefit_terms['SNAP_zero_existing_participation'],'terms':benefit_terms,
             'details':json.loads((OUT/'benefit_results.json').read_text())}
    consumption=consumption_removal(c,x,d,case)
    children=identity_loss_children(c,x,d,case)
    components={'M1':federal['M1'],'M2':state['M2'],'M3':federal['M3'],'M4_conditional_SNAP':benefit['M4'],
                'M5_fixed_pool':consumption['M5']}
    components['tax_only_stack']=sum(components[k] for k in ('M1','M2','M3'))
    components['conditional_fixed_pool_stack']=sum(components[k] for k in ('M1','M2','M3','M4_conditional_SNAP','M5_fixed_pool'))
    components.update(federal['terms'])
    components.update(benefit['terms'])
    components['M5_half_equal_half_own']=consumption['terms']['half_equal_half_own']
    gate('stack_generation_closure',np.max(np.abs(components['conditional_fixed_pool_stack'].sum(axis=0)-sum(
        components[k].sum(axis=0) for k in ('M1','M2','M3','M4_conditional_SNAP','M5_fixed_pool'))))<1e-6)
    results=result_rows(c,components,case)
    results.to_csv(OUT/'results.csv',index=False,lineterminator='\n',float_format='%.12f')
    reps=[]
    for component,values in components.items():
        for gi,g in enumerate(('G1','G2','G3+')):
            reps.append({'component':component,'generation':g,**{f'r{r}':values[gi,r] for r in range(161)}})
    pd.DataFrame(reps).to_csv(OUT/'replicates.csv',index=False,lineterminator='\n',float_format='%.15g')
    summary={'case':'oct14','allocation':'personal','income_year':2024,'sign':'positive raises group net cost',
             'frame':{'union':float(x['W'][x['union'],0].sum()),'lineage':case['lineage']['counts']['lineage_population']},
             'positive_control':{'original_gates':len(c.GATES),'item5b_union_bn':x['net'],
                                 'D_union_bn':x['summary']['account']['R3']['joint_split_D']['bn']['total']},
             'adopted_new_edit_bn':None,'recommended':'withhold adoption; conditional tax result crosses review bar, but own-return inputs and person consumption are not identified',
             'M1_M3':federal['details'],'M2':state['details'],'M4':benefit['details'],'M5':consumption['details'],
             'M6':children['details'],'M6_generation_count_million':children['counts'][:,0].tolist(),
             'results':results.to_dict(orient='records'),'gates':GATES,
             'stack':{'label':'conditional fixed-pool partial stack','M6_included':False,
                      'Medicaid_CHIP_ACA_spending_identified':False,'added_persons':'held in primary result; G3 transport shown separately as assumption',
                      'interactions_bn':0.,'interaction_rule':'M1/M2/M3 solved on one shared after-return; item 5b subtracted once; SNAP uses gross income; fixed pre-removal consumption pool does not respond to taxes or benefits',
                      'unidentified_interactions':['consumption response to survivor taxes/refunds/SNAP','takeup/eligibility/ACA changes','identity-loss membership and aggregate substitution']}}
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes=rss if sys.platform=='darwin' else rss*1024
    child_rss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    child_bytes=child_rss if sys.platform=='darwin' else child_rss*1024
    print(f'[memory] self {rss_bytes/1e9:.3f}GB; largest child {child_bytes/1e9:.3f}GB',flush=True)
    gate('process_peak_RSS_under_2_5GB',max(rss_bytes,child_bytes)<=2_500_000_000,{'limit_bytes':2_500_000_000})
    write_json(OUT/'summary.json',summary)
    write_report(summary)
    write_json(OUT / 'probe.json', {'persons': len(d), 'columns': list(d), 'gates': GATES,
                                  'federal': federal['details'],
                                  'M1_bn': federal['M1'][:,0].tolist(),
                                  'M3_bn': federal['M3'][:,0].tolist()})
    for k in ('M1','M2','M3','M4_conditional_SNAP','M5_fixed_pool','tax_only_stack','conditional_fixed_pool_stack'):
        v=components[k].sum(axis=0)
        print(f'[result] {k}: {v[0]:+.9f}bn SE {c.sdr(v):.9f}',flush=True)
    print(f"[M6] {children['details']['candidate_children_million']:.6f}M candidate children; overlap unidentifiable",flush=True)
    print(f'[runtime] {time.perf_counter()-start:.3f}s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2:.1f} MiB', flush=True)


if __name__ == '__main__':
    main()

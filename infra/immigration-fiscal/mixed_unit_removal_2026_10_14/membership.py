"""Biological-child R3-prime removal mask and inspectable credit partitions.

This changes the departure universe, not the priced population: children drawn
from the existing latent addition are not added to its population or own costs.
Use expanded_context in the jointly solved survivor tax/benefit calculation;
diagnostic reverse-credit terms below must NOT also be added to that solution.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
LANE = Path(__file__).resolve().parent
OUT = LANE / 'derived'


def gate(name, condition, value=None):
    if not condition:
        raise SystemExit(f'[BLOCKED] membership {name}: {value}')
    return {'name': name, 'passed': True, 'value': value}


def add_parent_types(d, c):
    fields = ['PH_SEQ', 'PPPOS', 'PEPAR1TYP', 'PEPAR2TYP']
    if all(k in d for k in fields):
        return d
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        extra = pd.read_csv(z.open('pppub25.csv'), usecols=fields)
    result = d.merge(extra, on=['PH_SEQ', 'PPPOS'], validate='one_to_one', how='left')
    gate('parent_type_join_complete', not result[['PEPAR1TYP', 'PEPAR2TYP']].isna().any().any())
    return result


def biological_children(d, union, civ):
    """Under-18 native civilians with a co-resident type-1 member parent.

    A biological link confers ancestry even where the child's tax claimant is
    somebody else. Type 2 (step) and type 3 (adoptive) alone do not confer it.
    """
    lookup = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_frame(d[['PH_SEQ', 'A_LINENO']]))
    bio, step = np.zeros(len(d), bool), np.zeros(len(d), bool)
    links = np.full((2, len(d)), -1, int)
    for i in (1, 2):
        raw = lookup.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ, d[f'PEPAR{i}']])).to_numpy(float)
        found = np.isfinite(raw)
        rows = np.where(found, np.nan_to_num(raw), -1).astype(int)
        members = found & union[np.maximum(rows, 0)]
        typ = d[f'PEPAR{i}TYP'].to_numpy()
        bio |= members & (typ == 1)
        step |= members & (typ == 2)
        links[i-1] = np.where(members & (typ == 1), rows, -1)
    eligible = civ & ~union & d.PRCITSHP.isin([1, 2, 3]).to_numpy() & (d.A_AGE.to_numpy() < 18)
    return eligible & bio, eligible & step & ~bio, links


def latent_mask(d, union, civ):
    """Single shared departure subset for health/SNAP/tax standalone frames.

    Both child parent-birthplace fields must be US areas and the child must not
    report Mexican origin. At least one actual biological member-parent record
    must itself be native: a conflicting Mexico-born linked parent is excluded
    from the latent pool and retained only in the broad biological-child arm.
    """
    extra,_,links=biological_children(d,union,civ)
    us=[57,60,66,69,73,78]
    native=d.PRCITSHP.isin([1,2,3]).to_numpy()
    actual_native_parent=np.zeros(len(d),bool)
    for rows in links:
        actual_native_parent |= (rows>=0)&native[np.maximum(rows,0)]
    return extra & d.PEFNTVTY.isin(us).to_numpy() & d.PEMNTVTY.isin(us).to_numpy() & ~d.PRDTHSP.eq(1).to_numpy() & actual_native_parent


def expanded_context(c, x, d, case, *, latent_only=False):
    """Copy x, rebuild its registry; hold old item5b account closure/calibration.

    All new removal children are assigned G3+ for fiscal-generation ownership,
    as the existing latent addition is. Parent generations remain diagnostics.
    National weights, original baseline tax amounts and old item vectors stay.
    """
    d = add_parent_types(d, c)
    extra, step, links = biological_children(d, x['union'], x['civ'])
    if latent_only:
        extra=latent_mask(d,x['union'],x['civ'])
    y = dict(x)
    y['union'] = x['union'] | extra
    y['gen'] = x['gen'].copy()
    y['gen'][extra] = 2
    start=len(c.GATES)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            R, drows, ri, dgen, dmem = c.returns(d, y['union'], y['gen'], x['civ'])
        rebuild_gates=c.GATES[start:].copy()
    finally:
        del c.GATES[start:]
    gate('return_rows_unchanged', np.array_equal(R.row, x['R'].row))
    gate('return_spouses_unchanged', np.array_equal(R.spouse, x['R'].spouse))
    gate('dependent_link_order_unchanged', np.array_equal(drows, x['drows']) and np.array_equal(ri, x['ri']))
    y.update(d=d, R=R, drows=drows, ri=ri, dgen=dgen, dmem=dmem)
    y['membership_registry_gates']=rebuild_gates
    return y, {'extra': extra, 'step_stays': step, 'links': links}


def transport_added(case, values, residual_g3=None):
    """Existing case G3-rate transport; white-priced amount held at zero.

    This is not a measured added-person return: all replicate uncertainty is
    conditional on fixed counts and the existing case transport assumption.
    """
    number=case['lineage']['members']['g3plus'] if residual_g3 is None else residual_g3
    scale = number / case['lineage']['counts']['identified_g3plus']
    result = np.zeros((3, 161))
    result[2] = values[2] * scale
    return result


def compute(c, x, d, case):
    verify_pins(c)
    y, masks = expanded_context(c, x, d, case)
    extra, step, W, R = masks['extra'], masks['step_stays'], x['W'], x['R']
    d = y['d']
    counts = extra @ W
    stepcounts = step @ W
    gates = [gate('extra_and_original_union_disjoint', not (extra & x['union']).any()),
             gate('extra_all_civilian_native_children', bool((~extra | (x['civ'] & (d.A_AGE.to_numpy()<18)
                  & d.PRCITSHP.isin([1,2,3]).to_numpy())).all())),
             gate('step_only_children_stay', not (step & y['union']).any()),
             gate('expanded_count_exactly_union_plus_extra_all_columns',
                  np.max(abs(y['union'] @ W - x['union'] @ W - counts)) < 1e-6)]
    # Existing latent addition requires two US-area-born parents. The observed
    # outside-this-universe children cannot silently be assigned to that pool.
    us = [57,60,66,69,73,78]
    raw_latent = extra & d.PEFNTVTY.isin(us).to_numpy() & d.PEMNTVTY.isin(us).to_numpy() & ~d.PRDTHSP.eq(1).to_numpy()
    parent_gen = np.full((2,len(d)),-1,int)
    for i in range(2):
        valid=masks['links'][i]>=0
        parent_gen[i,valid]=x['gen'][masks['links'][i,valid]]
    inconsistent=raw_latent & ~(parent_gen>=1).any(axis=0)
    latent=raw_latent & ~inconsistent
    gates.append(gate('shared_latent_mask_agrees_with_generation_definition',np.array_equal(latent,latent_mask(d,x['union'],x['civ']))))
    outside=extra & ~latent
    latent_counts=latent@W
    added=case['lineage']['counts']['added']
    # A second-generation member parent gives G3-rate attrition; a G3+ parent
    # gives later loss. With both, use the earliest measured generation.
    third = latent & (parent_gen==1).any(axis=0)
    later = latent & ~third
    malformed = latent & ~(parent_gen>=1).any(axis=0)
    gates.append(gate('latent_has_native_G2_or_G3_member_parent',not malformed.any(),int(malformed.sum())))
    third_count=third@W
    later_count=later@W
    c3=case['lineage']['c3']['value']
    roster_g3=later_count+(1-c3)*third_count
    roster_white=c3*third_count
    remaining_g3=case['lineage']['members']['g3plus']-roster_g3
    remaining_white=case['lineage']['members']['white']-roster_white
    gates.append(gate('latent_pricing_classes_have_nonnegative_residual_all_columns',
                      bool((remaining_g3>=0).all() and (remaining_white>=0).all())))
    gates.append(gate('roster_plus_unlocated_latent_closes_fixed_addition_all_columns',
                      np.max(abs(roster_g3+roster_white+remaining_g3+remaining_white-added))<1e-6))
    own_ref=(d.EIT_CRED.to_numpy()+d.ACTC_CRD.to_numpy())*latent
    own_nonref=d.CTC_CRD.to_numpy()*latent
    own_ref_bn=own_ref@W/1e9
    own_nonref_bn=own_nonref@W/1e9
    # This gate addresses the claimed duplicate: qualifying children and the
    # tax claimant carrying the credit are different actual person records.
    gates.append(gate('located_latent_children_own_credit_records_zero',
                      bool((own_ref==0).all() and (own_nonref==0).all())))
    gates.append(gate('latent_roster_subset_fits_existing_added_count_all_columns',
                      bool((latent_counts >= 0).all() and (latent_counts <= added).all())))
    gates.append(gate('observed_latent_and_other_children_partition_exactly_all_columns',
                      np.max(abs((latent@W)+(outside@W)-counts)) < 1e-6))
    # Diagnostic R3 -> R3-prime reverse effects, same within-return equal credit
    # convention as the frozen lane. Joint surviving spouse no longer overrides
    # child's own biological lineage membership.
    remain = ~y['union'][x['drows']]
    kept_old = ~x['dmem']
    nonmem_parent = np.zeros(len(d), bool)
    lookup = dict(zip(zip(d.PH_SEQ, d.A_LINENO), range(len(d))))
    for p in ('PEPAR1','PEPAR2'):
        rows = np.array([lookup.get((ph,ln),-1) for ph,ln in zip(d.PH_SEQ,d[p])])
        nonmem_parent |= (rows>=0) & ~y['union'][np.maximum(rows,0)]
    new_child_can_continue = remain & nonmem_parent[x['drows']]
    new_keep = np.bincount(x['ri'], weights=new_child_can_continue.astype(float), minlength=len(R)) / np.maximum(R.n_non.to_numpy(),1)
    mixed_surviving_spouse = x['dm2']
    new_keep = np.where(mixed_surviving_spouse,
                        np.bincount(x['ri'],weights=remain.astype(float),minlength=len(R))/np.maximum(R.n_non.to_numpy(),1),new_keep)
    terms = {}
    for k, value in x['comp_ruled'].items():
        if not k.startswith(('B_', 'Cr_')):
            continue
        terms[k] = np.stack([x['account'](value * x['owner'][k][g] * (new_keep-x['keep_of']('R3',k)), k)
                             for g in range(3)])
    terms['reverse_credit_reclassification'] = sum(terms.values())
    terms['D_added_original_control'] = transport_added(case, np.stack([
        sum(x['account'](x['comp_ruled'][k]*x['owner'][k][g],k) for k in ('D_receipts','D_spending'))
        for g in range(3)]))
    terms['D_added_original_residual_control']=transport_added(case,np.stack([
        sum(x['account'](x['comp_ruled'][k]*x['owner'][k][g],k) for k in ('D_receipts','D_spending'))
        for g in range(3)]),remaining_g3)
    old_g3=sum(x['account'](value*x['owner'][k][2]*x['keep_of']('R3',k),k)
               for k,value in x['comp_ruled'].items() if not k.startswith('D_'))
    # Frozen item5b holds its full-sample per-member calibration across columns.
    # Roster count uncertainty is sampled; transport calibration is conditioned.
    projected=np.zeros((3,161))
    projected[2]=-old_g3[0]*roster_g3/case['lineage']['counts']['identified_g3plus']
    terms['M6_remove_roster_lineage_credit_projection']=projected
    projections={}
    for side in ('receipts','spending'):
        side_g3=sum(x['account'](value*x['owner'][k][2]*x['keep_of']('R3',k),k)
                    for k,value in x['comp_ruled'].items() if not k.startswith('D_') and x['side'][k]==side)
        v=np.zeros((3,161))
        v[2]=-side_g3[0]*roster_g3/case['lineage']['counts']['identified_g3plus']
        projections[side]=v
    gates.append(gate('projection_side_vectors_close_all_columns',np.max(abs(sum(projections.values())-projected))<1e-9))
    # Credits on a member claimant remain in the union's priced head record.
    # Added children have no extra own-record credit to insert here. Their case
    # crossing-credit projection is a separate global G3-per-person transport.
    # Quantify the reported $1.033bn exposure under the original per-child split.
    identity_claim = np.zeros((3,161))
    latent_dep = latent[x['drows']]
    fractions = np.bincount(x['ri'],weights=latent_dep.astype(float),minlength=len(R))/np.maximum(R.n_all.to_numpy(),1)
    for g in range(3):
        member_h = R.mem_h.to_numpy() & (R.gen_h.to_numpy()==g)
        identity_claim[g] = x['account'](x['base'].ctc * x['f_other'] * fractions * member_h,'B_nonref')
        identity_claim[g] += x['account']((x['base'].eitc*x['f_eitc']+x['base'].actc*x['f_other'])*fractions*member_h,'B_actc')
    terms['identity_child_credit_on_union_heads_diagnostic'] = identity_claim
    details = {'extra_children':float(counts[0]),'extra_children_se':c.sdr(counts),
               'nonmember_claimant_extra_dependents':float((extra[x['drows']] & ~R.mem_h.to_numpy()[x['ri']]) @ W[x['drows'],0]),
               'nonmember_claimant_latent_dependents':float((latent[x['drows']] & ~R.mem_h.to_numpy()[x['ri']]) @ W[x['drows'],0]),
               'latent_children_with_two_US_parents':float(latent_counts[0]),
               'outside_existing_addition_definition':float((outside@W)[0]),
               'two_US_parent_fields_conflict_with_linked_Mexico_born_parent_records':int(inconsistent.sum()),
               'conflicting_parent_fields_child_count':float((inconsistent@W)[0]),
               'step_only_children_stay':float(stepcounts[0]), 'step_only_se':c.sdr(stepcounts),
               'union_count_unchanged':float(x['union']@W[:,0]),'existing_addition_count_unchanged':added,
               'latent_residual':float(added-latent_counts[0]),
               'latent_third_rate_roster':float(third_count[0]),'latent_later_loss_roster':float(later_count[0]),
               'roster_g3_priced_count':float(roster_g3[0]),'roster_white_priced_count':float(roster_white[0]),
               'latent_child_own_refundable_credit_key_bn':float(own_ref_bn[0]),
               'latent_child_own_nonrefundable_credit_key_bn':float(own_nonref_bn[0]),
               'remaining_added_g3_priced_count':float(remaining_g3[0]),'remaining_added_white_priced_count':float(remaining_white[0]),
               'class_assignment':'earliest biological member-parent generation: G2 -> third-generation loss blend; G3+ -> later loss at G3+; C3 fixed case value',
               'counterfactual_departure_count':float(y['union']@W[:,0]),
               'original_personal_costs_held':True,'no_new_population_or_own_cost':True,
               'adoption':'biological-link correction is observed; full departure mask is an arm until outside-latent children have an adopted own-cost rebase',
               'overlap_rule':'union; disjoint roster latent subset; residual of fixed latent count; outside-definition departures separately identified, no second own cost',
               'duplicate_1_033_claim':'head-record credit exposure is not evidence of a duplicate: added-age personal refundable key is carried by adult claimant ages, not by qualifying-child ages',
               'white_rule':'crossing credits and D zero under existing case rule, assumed; a <=0.25bn white-credit sensitivity is not a verified bound on D',
               'diagnostics_not_additive':['reverse_credit_reclassification','identity_child_credit_on_union_heads_diagnostic'],
               'D_added_control_rule':'original D G3+ per identified member x existing added G3+-priced count; corrected D should use solved corrected mixed-couple vector',
               'projection_replication':'frozen original full-sample per-member projection; roster counts vary through all160 replicates; C3 fixed',
               'gates':gates}
    return {'context':y,'removal_union':y['union'],'masks':masks,'terms':terms,'details':details,
            'projection_sides':projections,'remaining_added_g3':remaining_g3,'remaining_added_white':remaining_white}


def write(c, result):
    OUT.mkdir(exist_ok=True)
    rows=[]
    for name, v in result['terms'].items():
        for g,label in enumerate(('G1','G2','G3+')):
            rows.append({'component':name,'generation':label,**{f'r{i}':v[g,i] for i in range(161)}})
    pd.DataFrame(rows).to_csv(OUT/'membership_replicates.csv',index=False,lineterminator='\n',float_format='%.15g')
    details=dict(result['details'])
    details['terms']={name:{'bn':float(v[:,0].sum()),'se_bn':c.sdr(v.sum(axis=0)),
                            'by_generation_bn':v[:,0].tolist()} for name,v in result['terms'].items()}
    (OUT/'membership.json').write_text(json.dumps(details,indent=2)+'\n')
    verify_pins(c)
    return details


def verify_pins(c):
    """Register immutable inputs once; every later call rejects byte drift."""
    sources=[Path(c.__file__),c.CPS_ZIP,
             LANE.parent/'main_case_2026_10_14/derived/corrections.json',
             LANE.parent/'main_case_2026_10_14/derived/corrections_cash.json',
             LANE.parent/'added_age_mix_2026_10_07/derived/g3_age_keys.json',
             LANE.parent/'within_group_distribution_2026_09_29/_cache/sept29/pension_grid_7660d97f808b5c75.npz',
             LANE.parent/'within_group_distribution_2026_09_29/_cache/sept29/person_accrual.parquet',
             LANE.parent/'within_group_distribution_2026_09_29/derived/sept29/person_accrual_model.json']
    sources += [LANE.parent/'pension_accrual_2026_09_28'/name
                for name in ['pension_accrual.py','lifetime_model.py','sources.py']]
    pins={'files':[{ 'path':str(path.relative_to(LANE.parent)),
                     'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest()} for path in sources],
          'primary_rules':[{'url':'https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf',
                            'checked':'PEPAR1TYP/PEPAR2TYP 1 Biological; 2 Step; 3 Adopted'},
                           {'url':'https://www.ssa.gov/faqs/en/questions/KA-02011.html','checked':'own/spouse total equals higher amount'},
                           {'url':'https://www.ssa.gov/survivor/amount','checked':'survivor up to100% at survivor FRA'}]}
    register=LANE/'inputs/membership_pension_pins.json'
    if register.exists():
        prior=json.loads(register.read_text())
        if prior!=pins:
            before={p['path']:p['sha256'] for p in prior['files']}
            now={p['path']:p['sha256'] for p in pins['files']}
            changed=sorted(k for k in before.keys()|now.keys() if before.get(k)!=now.get(k))
            raise SystemExit(f'[BLOCKED] membership/pension immutable input drift: {changed or "register metadata"}')
    else:
        register.write_text(json.dumps(pins,indent=2)+'\n')
    return pins

"""Transport measured October2024 public-K12 exposure into the refreshed account.

This is a synthetic exposure correction, not a record linkage or causal effect.
Cost schedules and all non-school components remain the canonical account's.
"""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from measurement import AGE_BANDS, cells, fit_rates, load_october, origin_masks, public_k12, sdr, sha

HERE=Path(__file__).resolve().parent
GROUPS={'target':'mexican_observed_total','rest':'other_residents','all':'national_civilian'}

def describe(d,w):
    pupil=public_k12(d)
    origins=origin_masks(d)
    rows=[]
    ages=[('all_ages',0,99),('5_17',5,17),*AGE_BANDS]
    for state in [0,6,48]:
        geo=np.ones(len(d),bool) if state==0 else d.GESTFIPS.eq(state).to_numpy()
        for origin,mask in origins.items():
            for age,lo,hi in ages:
                use=geo&mask&d.PRTAGE.between(lo,hi).to_numpy()
                pop=w[use].sum(axis=0)
                count=w[use&pupil].sum(axis=0)
                rows.append(dict(state=state,origin=origin,age=age,n=int(use.sum()),
                    n_public=int((use&pupil).sum()),population=pop[0],population_se=float(sdr(pop)),
                    pupils=count[0],pupil_se=float(sdr(count))))
    return pd.DataFrame(rows)

def heldout_states(d,w):
    fit=~d.GESTFIPS.isin([6,48]).to_numpy()
    rates,_=fit_rates(d,w,fit_mask=fit)
    code=cells(d)
    predicted=np.array([rates[c] for c in code])
    actual=public_k12(d)
    rows=[]
    for state in [6,48]:
        for origin in ['all','target','rest','hispanic']:
            use=d.GESTFIPS.eq(state).to_numpy()&origin_masks(d)[origin]
            obs=w[use&actual].sum(axis=0)
            pred=(predicted[use]*w[use]).sum(axis=0)
            delta=pred-obs
            rows.append(dict(state=state,origin=origin,predicted=pred[0],observed=obs[0],
                residual=delta[0],residual_se=float(sdr(delta)),
                fit_population='October respondents outside CA and TX',
                timing='Same October; each replicate refits rates and heldout counts'))
    return pd.DataFrame(rows)

def canonical(root):
    fiscal=root/'infra/immigration-fiscal'
    sys.path.insert(0,str(fiscal/'ledger_absolute_2026_09_17'))
    import absolute_ledger as al
    ext=al.ext
    cps=fiscal/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    if sha(cps)!=ext.CPS_SHA:
        raise ValueError('March CPS release checksum differs')
    state=ext.build(argparse.Namespace(cps_zip=cps))
    d=state['d'].copy()
    d['PRTAGE']=d.A_AGE
    civil=(d.PRPERTYP.eq(2)|d.A_AGE.lt(15)).to_numpy()
    actual=np.logical_or.reduce([state['group'][g] for g in al.TARGETS])
    if not np.array_equal(actual,origin_masks(d)['target']):
        raise ValueError('Canonical fiscal target drift')
    masks={GROUPS[k]:m&civil for k,m in origin_masks(d).items() if k in GROUPS}
    path=fiscal/'ledger_absolute_2026_09_17/params/params.json'
    p=al.Params(path,False)
    cap=p.pick('k12',['capital_outlay','by_state'],'state_money',preferred='f33_capital_outlay_by_state')
    interest=p.pick('k12',['interest','by_state'],'state_money',preferred='f33_interest_on_school_debt_by_state')
    membership=p.pick('k12',['membership','by_state'],'state_count',preferred='f33_fall_membership_by_state')
    h=p.pick('district',['hispanic','minus_all'],'state_money',preferred='hispanic_minus_all_by_state')
    white=p.pick('district',['white','minus_all'],'state_money',preferred='white_minus_all_by_state')
    if not all([cap,interest,membership,h,white]):
        raise ValueError('Verified cost schedules unavailable; no fallback')
    caprate={f:(cap[f]+interest[f])/membership[f] for f in membership if membership[f]>0}
    costs=dict(school=d.GESTFIPS.map(state['params'].per_pupil_current_spending).to_numpy(float),
               K=d.GESTFIPS.map(caprate).to_numpy(float),
               D=np.where(state['group'][al.WHITE]&civil,d.GESTFIPS.map(white),
                          np.where(actual&civil,d.GESTFIPS.map(h),0)).astype(float))
    if not np.isfinite(np.column_stack(list(costs.values()))).all():
        raise ValueError('Unmapped pupil cost schedule')
    inputs=[cps,path,Path(ext.__file__),Path(ext.base.__file__),Path(al.__file__),
            ext.HERE/'state_parameters.csv']
    return state,d,civil,masks,costs,ext.PUPIL_RATIO_NATIVE_ACS,inputs

def coefficients(d,weights,index,n_units,mask,cost,codes,allocation):
    """Collapse fiscal receiver weights to exposure donors; preserve sharing.

    Shared exposure is assigned once to its resource unit then equally to all
    members, exactly as canonical. Person weights need not match inside units.
    """
    effective=weights*mask[:,None]
    if allocation=='shared':
        unit=np.zeros((n_units,weights.shape[1]))
        np.add.at(unit,index,effective)
        effective=unit[index]/np.bincount(index,minlength=n_units)[index,None]
    return {code:(-cost[codes==code])@effective[codes==code]/1e9 for code in set(codes)}

def apply_rates(basis,rates,old):
    order=sorted(basis)
    b=np.array([basis[c] for c in order])
    r=np.array([rates[c] for c in order])
    point=float(b[:,0]@r[:,0])
    oct_reps=b[:,0]@r
    march_reps=b.T@r[:,0]
    change_oct=oct_reps-old[0]
    change_march=march_reps-old
    se_o=float(sdr(change_oct))
    se_m=float(sdr(change_march))
    return dict(updated_signed_bn=point,balance_change_bn=point-old[0],
                se_october_bn=se_o,se_march_bn=se_m,
                se_zero_covariance_bn=float(np.hypot(se_o,se_m)),
                se_unknown_correlation_lower_bn=abs(se_o-se_m),
                se_unknown_correlation_upper_bn=se_o+se_m)

def fiscal_effects(state,d,civil,masks,costs,r0,octd,octw,account):
    weights=state['person_weights']
    old_exposure=d.PRTAGE.between(5,17).to_numpy()*r0
    rows=[]
    for scenario,pooled,expand in [('ages5_17',False,False),('all_ages',False,True),('ages3_24',False,True),('pooled_origin',True,True)]:
        rates,_=fit_rates(octd,octw,pooled)
        code=cells(d,pooled)
        code[~civil]='out'
        if not expand:
            code[~d.PRTAGE.between(5,17).to_numpy()]='out'
        if scenario=='ages3_24':
            code[d.PRTAGE.ge(25).to_numpy()]='out'
        for allocation in ['personal','shared']:
            for group,mask in masks.items():
                old_total=np.zeros(161)
                sum_basis={}
                for component,cost in costs.items():
                    basis=coefficients(d,weights,state['index'],state['n_units'],mask,cost,code,allocation)
                    old_basis=coefficients(d,weights,state['index'],state['n_units'],mask,cost*old_exposure,np.repeat('all',len(d)),allocation)
                    old=old_basis['all']
                    prior=account.loc[account.allocation.eq(allocation)&account.group.eq(group)&account.component.eq(component),'signed_bn']
                    if len(prior)!=1 or abs(old[0]-prior.iloc[0])>1e-6:
                        raise ValueError(f'Baseline school reconciliation failed: {allocation}/{group}/{component}: {old[0]}, {prior.tolist()}')
                    result=apply_rates(basis,rates,old)
                    rows.append(dict(scenario=scenario,allocation=allocation,group=group,component=component,
                                     original_signed_bn=old[0],**result))
                    old_total+=old
                    for c,v in basis.items():
                        sum_basis[c]=sum_basis.get(c,np.zeros(161))+v
                rows.append(dict(scenario=scenario,allocation=allocation,group=group,component='school_K_D',
                                 original_signed_bn=old_total[0],**apply_rates(sum_basis,rates,old_total)))
    result=pd.DataFrame(rows)
    for (scenario,allocation,component),block in result.groupby(['scenario','allocation','component']):
        by=block.set_index('group')
        for field in ['original_signed_bn','updated_signed_bn','balance_change_bn']:
            if abs(by.loc['mexican_observed_total',field]+by.loc['other_residents',field]-by.loc['national_civilian',field])>1e-7:
                raise ValueError('Target/rest conservation failure')
    baseline=account.groupby(['allocation','group']).signed_bn.sum()
    result['baseline_balance_bn']=[baseline.loc[a,g] for a,g in zip(result.allocation,result.group)]
    result['updated_balance_bn']=result.baseline_balance_bn+result.balance_change_bn
    return result

def comparisons(root,counts):
    prior=root/'infra/immigration-fiscal/admin_school_checks_2026_09_19'
    acs=pd.read_csv(prior/'derived/pupil_counts.csv')
    rows=[]
    for r in acs[acs.source.eq('ACS2024') & acs.metric.ne('children_5_17')].itertuples():
        state={'US':0,'California':6,'Texas':48}[r.area]
        age='5_17' if r.metric=='public_k12_5_17' else 'all_ages'
        c=counts[counts.state.eq(state)&counts.origin.eq(r.origin)&counts.age.eq(age)].iloc[0]
        rows.append(dict(comparator='ACS2024',state=state,origin=r.origin,age=age,october=c.pupils,
                         control=r.estimate,difference=c.pupils-r.estimate,october_se=c.pupil_se,
                         control_se=r.se,source='Unused matched child/grade cells; ACS source reused earlier'))
    meta=json.loads((prior/'sources.json').read_text())
    for r in meta['administrative_controls']:
        c=counts[counts.state.eq(r['fips'])&counts.origin.eq(r['origin'])&counts.age.eq('all_ages')].iloc[0]
        control=r['total']-r['excluded_early_education']
        rows.append(dict(comparator=r['school_year']+' administrative',state=r['fips'],origin=r['origin'],
            age='all_ages',october=c.pupils,control=control,difference=c.pupils-control,
            october_se=c.pupil_se,control_se=np.nan,source=r['url']))
    return pd.DataFrame(rows),[prior/'derived/pupil_counts.csv',prior/'sources.json',prior/'derived/audit.json']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--cache',type=Path,default=HERE/'_cache')
    parser.add_argument('--out',type=Path,default=HERE/'derived')
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    d,w,audit=load_october(args.cache,HERE/'sources.json')
    counts=describe(d,w)
    counts.to_csv(args.out/'october_counts.csv',index=False)
    rates,rate_rows=fit_rates(d,w)
    pd.DataFrame(rate_rows).to_csv(args.out/'national_rates.csv',index=False)
    heldout_states(d,w).to_csv(args.out/'heldout_CA_TX.csv',index=False)
    comp,comp_inputs=comparisons(args.source_root,counts)
    comp.to_csv(args.out/'comparators.csv',index=False)
    state,march,civil,masks,costs,r0,inputs=canonical(args.source_root)
    code=cells(march)
    prediction=np.array([rates[c][0] for c in code])*civil
    old=march.PRTAGE.between(5,17).to_numpy()*r0*civil
    exposure_rows=[]
    for geo in [0,6,48]:
        where=np.ones(len(march),bool) if geo==0 else march.GESTFIPS.eq(geo).to_numpy()
        for group,mask in masks.items():
            for age,lo,hi in [('all_ages',0,99),('5_17',5,17),*AGE_BANDS]:
                use=where&mask&march.PRTAGE.between(lo,hi).to_numpy()
                weight=state['person_weights'][use,0]
                exposure_rows.append(dict(state=geo,group=group,age=age,
                    original_pupils=float(old[use]@weight),updated_pupils=float(prediction[use]@weight)))
    pd.DataFrame(exposure_rows).to_csv(args.out/'transported_pupils.csv',index=False)
    account_path=args.source_root/'infra/immigration-fiscal/macro_closure_2026_09_19/derived/updated_account_components.csv'
    account=pd.read_csv(account_path)
    effects=fiscal_effects(state,march,civil,masks,costs,r0,d,w,account)
    effects.to_csv(args.out/'fiscal_effects.csv',index=False)
    effects[effects.scenario.eq('all_ages')&effects.component.ne('school_K_D')].to_csv(args.out/'correction_effects.csv',index=False)
    summary=effects[effects.component.eq('school_K_D')]
    summary.to_csv(args.out/'annual_balance.csv',index=False)
    corrected=account.copy()
    for r in effects[effects.scenario.eq('all_ages')&effects.component.ne('school_K_D')].itertuples():
        use=corrected.allocation.eq(r.allocation)&corrected.group.eq(r.group)&corrected.component.eq(r.component)
        corrected.loc[use,'signed_bn']=r.updated_signed_bn
        corrected.loc[use,'spending_bn']=-r.updated_signed_bn
    corrected.to_csv(args.out/'updated_account_components.csv',index=False)
    inputs += comp_inputs+[account_path,HERE/'sources.json',Path(__file__),HERE/'measurement.py',HERE/'acquire.py']
    audit.update(fixed_old_rate=r0,inputs=[dict(path=str(p),sha256=sha(p)) for p in inputs],
       identification='National age/origin enrollment transported to March population; no person linkage',
       uncertainty='160-replicate sampling SEs separately for October rates and March exposures; their covariance unidentified. Sum-of-SE bound, not a bound on systematic error.',
       scope='Only school/K/D replaced. SPM school-lunch reversal and every other component unchanged.',
       checks='All18 baseline component/group/allocation totals reconcile; every point target+rest=national; all161 official October weight sums match.')
    (args.out/'manifest.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(pd.DataFrame(rate_rows).to_string(index=False),flush=True)
    print(summary[['scenario','allocation','group','balance_change_bn','updated_balance_bn','se_unknown_correlation_upper_bn']].to_string(index=False),flush=True)

if __name__=='__main__':
    main()

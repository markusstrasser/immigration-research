#!/usr/bin/env python3
"""M5 siblings and the within-member weight-artifact gate.

Native-First: reuse the source CSV, canonical CPS frame and frozen case evaluator.
Own disposable resources are an allocation arm, not observed person consumption.
Each weighted source pool stays fixed separately in every SDR column.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

LANE=Path(__file__).resolve().parent
GENS=('G1','G2','G3+')


def require(ok,name):
    if not ok:
        raise ValueError('[BLOCKED] resource keys '+name)


def weighted_split(old,income,unit,w,change):
    """Split the original weighted pool, never an unweighted sum times new weights."""
    n=len(change)
    positive=np.maximum(income,0)
    total=np.bincount(unit,weights=old*w,minlength=n)
    moment=np.bincount(unit,weights=positive*w,minlength=n)
    support=np.bincount(unit,weights=positive,minlength=n)
    require(not np.any(change&(support>0)&(moment==0)&(total!=0)),'zero signed own-income moment')
    scale=np.divide(total,moment,out=np.zeros(n),where=moment!=0)
    new=np.where(change[unit]&(support[unit]>0),positive*scale[unit],old)
    error=np.bincount(unit,weights=w*(new-old),minlength=n)
    require(np.max(np.abs(error),initial=0)/1e9<1e-6,'weighted unit conservation')
    return new,float(np.max(np.abs(error),initial=0)/1e9)


def compute(d,x,case,disposable):
    """Returns fixed-pool owner/SNAP/housing movements and diagnostic four-line artifact."""
    W,union,gen,civ=(x[k] for k in ('W','union','gen','civ'))
    spm,_=pd.factorize(d.SPM_ID,sort=False)
    hh,_=pd.factorize(d.PH_SEQ,sort=False)
    sizes=np.bincount(hh)
    parameter=LANE.parent/'gen_ledger_extension_2026_09_16/state_parameters.csv'
    digest=hashlib.sha256(parameter.read_bytes()).hexdigest()
    pinpath=LANE/'inputs/resource_pins.json'
    if not pinpath.exists():
        pinpath.write_text(json.dumps({'state_parameters.csv':{'path':str(parameter),'sha256':digest}},indent=2)+'\n')
    pins=json.loads(pinpath.read_text())
    require(pins['state_parameters.csv']['sha256']==digest,'source parameters hash')
    params=pd.read_csv(parameter).set_index('fips')
    rates=d.GESTFIPS.map(params.property_tax_effective_rate).to_numpy(float)
    require(np.isfinite(rates).all(),'property state support')
    owner=np.where(d.H_TENURE.eq(1),rates*d.HPROP_VAL.to_numpy(float),0)/sizes[hh]
    spmsize=np.bincount(spm)
    old={
        'modeled_owner_property':(owner,hh),
        'snap':(d.SPM_SNAPSUB.to_numpy(float)/spmsize[spm],spm),
        'housing_subsidies':(d.SPM_CAPHOUSESUB.to_numpy(float)/spmsize[spm],spm)}
    terms={name:np.zeros((3,161)) for name in old}
    controls={}
    for name,(value,_unit) in old.items():
        published=d.pwwgt0.to_numpy(float)
        measured=float(value[union]@published[union]/(value[civ]@published[civ]))
        side=case['resourceLines'][name]['side']
        if side=='receipt':
            line=next(v for v in x['model']['receipts']['lines'] if v['id']==name)
            declared=line['cells'][x['model']['receipts']['reference']]['personal']['share']
        else:
            line=next(v for v in x['model']['spending']['lines'] if v['id']==name)
            declared=line['keys'][line['preferred_key']]['personal']['share']
        require(abs(measured-declared)<5e-9,'positive control original model share '+name)
        controls[name]={'measured_published_share':measured,'declared_source_share':declared,'tolerance':5e-9}
    maxerr=0.
    for name,(value,unit) in old.items():
        n=int(unit.max())+1
        mixed=(np.bincount(unit,weights=union,minlength=n)>0)&(np.bincount(unit,weights=civ&~union,minlength=n)>0)
        # Retain the non-civilian pool rather than transferring it into the account.
        subunit=2*unit+(~civ).astype(int)
        change=np.repeat(mixed,2);change[1::2]=False
        line=case['resourceLines'][name]
        for r in range(161):
            w=W[:,r]
            new,error=weighted_split(value,disposable,subunit,w,change)
            maxerr=max(maxerr,error)
            nat=value[civ]@w[civ]
            group=value[union]@w[union]
            require(nat>0 and group>0,'nonpositive original key')
            require(abs((new[civ]@w[civ])-nat)/1e9<1e-6,'national key closure')
            move=np.bincount(gen+1,weights=(new-value)*w*civ,minlength=4)[1:]
            terms[name][:,r]=move/group*line['union_target_bn']*(-1 if line['side']=='receipt' else 1)
    # Retrodiction of the reported +$1.44bn: within-member sharing cannot change
    # the personal group total. Equal unweighted shares fail this identity.
    four={'refundable_credits':d.EIT_CRED.to_numpy(float)+d.ACTC_CRD.to_numpy(float),
          'social_security':d.SS_VAL.to_numpy(float),
          'federal_liability':d.FEDTAX_BC.to_numpy(float),
          'wage_oasdi':np.minimum(np.maximum(d.WSAL_VAL.to_numpy(float),0),168600.)}
    klass=np.where(~civ,2,np.where(union,0,1))
    within=spm*3+klass
    mask=np.ones(int(within.max())+1,bool)
    conservation={}
    for name,value in four.items():
        worst=0.
        for r in range(161):
            new,error=weighted_split(value,np.ones(len(d)),within,W[:,r],mask)
            maxerr=max(maxerr,error)
            gap=abs((new[union]-value[union])@W[union,r])/1e9
            require(gap<1e-6,'within-member personal identity '+name)
            worst=max(worst,gap)
        conservation[name]={'max_group_gap_bn':worst,'columns':161}
    control=pd.read_csv(LANE/'derived/positive_control/allocation_check.csv')
    sign=np.where(control.side.eq('receipts'),-1,1)
    artifact=float((control.members_only_minus_personal_bn*sign).sum())
    unequal=d.groupby('SPM_ID').pwwgt0.nunique().gt(1).mean()
    details={'rule':'positive own after-tax cash resources; joint taxes attributed by own positive AGI; original weighted unit pool held in each of 161 columns; all-zero own resources keep old equal shares',
             'owner_unit':'household PH_SEQ; state effective property rate times HPROP_VAL / actual household size',
             'SNAP_housing_unit':'SPM_ID; reported benefit pool held before removal',
             'zero_income_rule':'retain equal share; not zero consumption',
             'national_totals':'all keys preserve their old civilian weighted totals; calibrate movement to current union-only case target, added people fixed',
             'four_person_line_artifact_bn':artifact,
             'unweighted_units_unequal_person_weights_fraction':float(unequal),
             'artifact_admitted_bn':0.,'artifact_reason':'v7 uses personal allocation; all new splits conserve the original weighted pool. Adding the old within-member sharing artifact would count a nonexistent v7 error.',
             'conservation':conservation,'positive_controls':controls,'unit_closure_max_bn':maxerr,
             'recommendation':'own-resource keys are arms; weight conservation is a measurement correction already required by these operators',
             'SNAP_interaction':'M5 SNAP reallocation and M4 baseline reallocation cancel exactly in a solved removal: replace M4 with M4 minus M5 SNAP when stacking',
             'covered':['owner property','SNAP','housing subsidies','four original shared-person metrics all 161 weights'],
             'held':['energy and WIC resource sharing','added-person own resource keys','housing eligibility and rent response']}
    return {'terms':terms,'details':details}

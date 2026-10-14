"""Model envelope for reverse mixed-couple spousal/survivor accrual.

Member workers' family ratios already include the hypothetical spouse/survivor
benefit earned on their own records. Do not add that benefit again. The reverse
exposure is on nonmember workers' records whose spouse is removed. CPS current
earnings do not identify both spouses' lifetime insured benefit entitlements.
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode=True
LANE=Path(__file__).resolve().parent
FISCAL=LANE.parent
OUT=LANE/'derived'


def topups(worker_pia, spouse_own, survivor_worker, survivor_own):
    """Incremental entitlement, not the sum of the two earnings records."""
    return np.maximum(.5*np.asarray(worker_pia)-spouse_own,0), np.maximum(np.asarray(survivor_worker)-survivor_own,0)


def compute(c,x,d,case):
    from membership import verify_pins
    verify_pins(c)
    folder=FISCAL/'within_group_distribution_2026_09_29'
    path=folder/'person_accrual.py'
    spec=importlib.util.spec_from_file_location('mixed_pension_model',path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    PA=module.PA
    grid_path=module.CACHE/f'pension_grid_{module.grid_key()}.npz'
    if not grid_path.exists():
        raise SystemExit('[BLOCKED] missing precomputed pension grid; no remote or source-lane rebuild allowed')
    grids={PA.CENTRAL['scenario']:module.model_grid()}
    p=PA.frame()
    reference=pd.read_parquet(module.CACHE/'person_accrual.parquet')
    q=p[p.tax_oasdi.gt(0)].copy().reset_index(drop=True)
    keys=pd.MultiIndex.from_frame(q[['PH_SEQ','A_LINENO']])
    data_index=pd.Series(np.arange(len(d)),index=pd.MultiIndex.from_frame(d[['PH_SEQ','A_LINENO']]))
    idx=data_index.reindex(keys).to_numpy()
    if pd.isna(idx).any():
        raise SystemExit('[BLOCKED] pension frame lacks canonical person match')
    idx=idx.astype(int)
    ref=reference.set_index(['PH_SEQ','A_LINENO']).reindex(keys)
    if ref.oasdi_gross.isna().any():
        raise SystemExit('[BLOCKED] pension cached reference missing tax-paying record')
    level=PA.career_levels(q,PA.CENTRAL['mapping'])
    lvl=np.clip(level,PA.MODEL_LEVELS[0],PA.MODEL_LEVELS[-1])
    birth=np.clip(PA.ss.INCOME_YEAR-q.age.to_numpy(),PA.BIRTHS[0],PA.BIRTHS[-1]).astype(float)
    entry=np.where(q.mexico_born & q.arrival_age.notna(),q.arrival_age.fillna(21),21.)
    run=(PA.CENTRAL['rate'],PA.CENTRAL['mortality'])
    note=PA.S.mwr_table(PA.MWR_TABLE[PA.CENTRAL['scenario']])
    summary=json.loads((PA.OUT/'summary.json').read_text())
    cached_meta=json.loads((folder/'derived/sept29/person_accrual_model.json').read_text())
    for name,expected in cached_meta['pension_files_sha256'].items():
        got=hashlib.file_digest((PA.OUT/name).open('rb'),'sha256').hexdigest()
        if got!=expected:
            raise SystemExit(f'[BLOCKED] cached pension provenance stale: {name}')
    u=float(cached_meta['unauthorized_credit'])
    def accrual(fam):
        fac=PA.model_factor(grids[PA.CENTRAL['scenario']],PA.CENTRAL['method'],run,fam,entry,birth,lvl,q.age.to_numpy())
        return q.tax_oasdi.to_numpy()*PA.note_mwr(q,note,level,fam)*fac*np.where(q.unauth,u,1.)
    fam=PA.ss.family_vector(q,'observed_family')
    before=accrual(fam)
    gap=float(np.max(abs(before-ref.oasdi_gross.to_numpy())/np.maximum(abs(before),1)))
    if gap>1e-12:
        raise SystemExit(f'[BLOCKED] pension cached baseline failed {gap}')
    one=accrual(np.full(len(q),'one_earner_couple',object))
    male=accrual(np.full(len(q),'single_man',object))
    female=accrual(np.full(len(q),'single_woman',object))
    own=np.where(q.sex.to_numpy()==1,male,female)
    # Model's one-earner family is male-worker/female-spouse. Transfer its
    # spouse-only premium to a female worker's own term, explicitly a proxy.
    premium=np.maximum(one/np.maximum(male,1e-20)-1,0)*own
    net_fraction=np.divide(ref.oasdi_net.to_numpy(),ref.oasdi_gross.to_numpy(),out=np.ones(len(q)),where=ref.oasdi_gross.to_numpy()>0)
    premium*=net_fraction
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        spouse=pd.read_csv(z.open('pppub25.csv'),usecols=['PH_SEQ','PPPOS','A_SPOUSE'])
    joined=d[['PH_SEQ','PPPOS']].merge(spouse,on=['PH_SEQ','PPPOS'],how='left',validate='one_to_one')
    lookup=dict(zip(zip(d.PH_SEQ,d.A_LINENO),range(len(d))))
    partner=np.array([lookup.get((ph,ln),-1) for ph,ln in zip(d.PH_SEQ,joined.A_SPOUSE)])
    qp=partner[idx]
    mixed=(qp>=0)&~x['union'][idx]&x['union'][np.maximum(qp,0)]&x['civ'][idx]
    partner_zero=(d.WSAL_VAL.to_numpy()[np.maximum(qp,0)]+d.SEMP_VAL.to_numpy()[np.maximum(qp,0)]+d.FRSE_VAL.to_numpy()[np.maximum(qp,0)])<=0
    generation=x['gen'][np.maximum(qp,0)]
    W=x['W'][idx]
    terms={}
    for label,mask in [('pension_reverse_max_model',mixed),('pension_reverse_zero_current_earnings_proxy',mixed&partner_zero)]:
        terms[label]=np.stack([(premium*mask*(generation==g))@W/1e9 for g in range(3)])
    terms['pension_reverse_lower']=np.zeros((3,161))
    # Survey-level cash ceiling on co-resident nonmember recipients. There is
    # no benefit-type or earnings-record identifier: this includes own benefits
    # and is a diagnostic ceiling, not an adoptable price at case SS calibration.
    all_mixed=(partner>=0)&~x['union']&x['union'][np.maximum(partner,0)]&x['civ']
    all_gen=x['gen'][np.maximum(partner,0)]
    cash=np.maximum(d.SS_VAL.to_numpy(),0)
    terms['pension_cash_upper_raw_CPS']=np.stack([(cash*all_mixed*(all_gen==g))@x['W']/1e9 for g in range(3)])
    count=mixed@W/1e6
    details={'basis':'payable 2025 pension model, EAN new_issue central; hypothetical lifetime-family envelope, not measured 2026 case correction',
             'mixed_surviving_workers_million':float(count[0]),'mixed_surviving_workers_se_million':c.sdr(count),
             'baseline_relative_error':gap,'already_booked':'member workers observed-family ratios already include spouse and survivor contingent benefits; add zero again',
             'bounds_rule':'zero to one-earner spouse-only premium on all nonmember mixed-couple workers; removed spouse own entitlement fixed at zero at upper model endpoint',
             'zero_current_earnings_proxy_is_not_lower_bound':True,
             'missing_inputs':['both spouses lifetime covered earnings','insured-status histories','prior marriages and duration','own/spouse benefit netting','actual claim ages','benefit-type flags for current SS_VAL','non-co-resident former spouses'],
             'female_worker_rule':'male-worker/female-spouse one-earner premium ratio times female own accrual; mortality/age orientation proxy',
             'cash_increment':None,'cash_reason':'CPS SS_VAL has no retired/spousal/survivor component or linked earnings record. Paid member benefits already on members own record; raw-CPS all surviving-spouse SS is a diagnostic ceiling, includes own benefits, not an additive correction.',
             'recommendation':'arm only; reject universal +1–5bn measurement correction; no claim of hard bound beyond this hypothetical family model',
             'white_and_added_rule':'no pension transport: lineage aggregate has no mixed spouse links; priced own pension costs held',
             'source_rules':['https://www.ssa.gov/faqs/en/questions/KA-02011.html','https://www.ssa.gov/survivor/amount'],
             'gates':[{'name':'cached_gross_baseline_1e12_relative','passed':True,'value':gap},
                      {'name':'generation_owner_on_every_mixed_worker','passed':bool(((generation>=0)|~mixed).all())},
                      {'name':'lower_zero_and_upper_nonnegative','passed':bool((premium>=0).all())}]}
    return {'terms':terms,'details':details}


def write(c,result):
    rows=[]
    for name,v in result['terms'].items():
        for g,label in enumerate(('G1','G2','G3+')):
            rows.append({'component':name,'generation':label,**{f'r{i}':v[g,i] for i in range(161)}})
    pd.DataFrame(rows).to_csv(OUT/'pensions_replicates.csv',index=False,lineterminator='\n',float_format='%.15g')
    details=dict(result['details'])
    details['terms']={name:{'bn':float(v[:,0].sum()),'se_bn':c.sdr(v.sum(axis=0)),
                            'by_generation_bn':v[:,0].tolist()} for name,v in result['terms'].items()}
    (OUT/'pensions.json').write_text(json.dumps(details,indent=2)+'\n')
    return details

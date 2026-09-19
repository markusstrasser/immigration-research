from pathlib import Path
import hashlib, zipfile
import numpy as np
import pandas as pd

CW=['pwwgt0']+[f'pwwgt{i}' for i in range(1,161)]
AW=['PWGTP']+[f'PWGTP{i}' for i in range(1,81)]
PAYLOAD=['AGI','FEDTAX_BC','FEDTAX_AC','ACTC_CRD','EIT_CRED','TAX_INC']

def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def check_sources(raw,lock):
    for name,item in lock.items():
        if sha(Path(raw)/name)!=item['sha256']: raise ValueError(f'Source fingerprint changed: {name}')

def summary(values):
    v=np.asarray(values,float)
    se=float(np.sqrt(4/(len(v)-1)*np.square(v[1:]-v[0]).sum()))
    return {'estimate':float(v[0]),'se_sampling':se,'ci95_low':float(v[0]-1.96*se),'ci95_high':float(v[0]+1.96*se)}

def quantile(x,w,q):
    x,w=np.asarray(x),np.asarray(w)
    if np.any(w<0) or w.sum()<=0: raise ValueError('Invalid quantile weights')
    order=np.argsort(x,kind='stable'); x,w=x[order],w[order]
    return float(x[np.searchsorted(np.cumsum(w),q*w.sum(),side='left')])

def cps(path,year):
    fields=['PH_SEQ','PPPOS','A_LINENO','A_AGE','PRPERTYP','PRDTHSP','PENATVTY','PRCITSHP',
            'PEFNTVTY','PEMNTVTY','WSAL_VAL','SEMP_VAL','FRSE_VAL','FICA','STATETAX_A',
            'TAX_ID','DEP_STAT','FILESTAT','MARSUPWT','WECLW','WKSWORK',*PAYLOAD]
    with zipfile.ZipFile(path) as z:
        d=pd.read_csv(z.open(f'pppub{year%100}.csv'),usecols=fields)
        r=pd.read_csv(z.open(f'asec_csv_repwgt_{year}.csv'),usecols=['h_seq','PPPOS',*CW]).rename(columns={'h_seq':'PH_SEQ'})
        h=pd.read_csv(z.open(f'hhpub{year%100}.csv'),usecols=['H_SEQ','GESTFIPS','HHSTATUS'])
    d=d.merge(r,on=['PH_SEQ','PPPOS'],validate='one_to_one',how='left')
    d=d.merge(h,left_on='PH_SEQ',right_on='H_SEQ',validate='many_to_one',how='left')
    d=d.copy()
    if d.isna().any().any(): raise ValueError('Missing selected CPS fields or incomplete joins')
    np.testing.assert_allclose(d.MARSUPWT/100,d.pwwgt0,atol=.01,rtol=0)
    np.testing.assert_array_equal(d.FEDTAX_AC.to_numpy(),(d.FEDTAX_BC-d.ACTC_CRD-d.EIT_CRED).to_numpy())
    d['civilian']=d.PRPERTYP.isin([1,2])
    d['household']=d.HHSTATUS.isin([1,2,3])
    return d

def payroll(d,cap):
    wage=np.maximum(np.asarray(d.WSAL_VAL,float),0)
    se=.9235*np.maximum(np.asarray(d.SEMP_VAL+d.FRSE_VAL,float),0)
    se=np.where(se>=400,se,0)
    wb=np.minimum(wage,cap); sb=np.minimum(se,np.maximum(cap-wb,0))
    return {'wage_workers':(wage>0).astype(float),'se_workers':(se>0).astype(float),
            'oasdi_wage_base':wb,'oasdi_se_base':sb,'oasdi_total_base':wb+sb,
            'hi_wage_base':wage,'hi_se_base':se,'hi_total_base':wage+se,
            'employer_payroll':.062*wb+.0145*wage,
            'employee_self_payroll':.062*wb+.0145*wage+.124*sb+.029*se}

def returns(d):
    """Native claiming TAX_ID plus observed dependent-filer records; no assumed filer."""
    core=d.loc[d.DEP_STAT.eq(0)].copy()
    cg=core.groupby('TAX_ID')
    if cg.FILESTAT.nunique().max()!=1: raise ValueError('Mixed core filing statuses')
    n=cg.size(); joint=cg.FILESTAT.first().isin([1,2,3])
    if not n.eq(np.where(joint,2,1)).all(): raise ValueError('Unexpected native tax unit composition')
    core['has_payload']=core[PAYLOAD].ne(0).any(axis=1)
    carriers=core.loc[core.has_payload]
    counts=carriers.groupby('TAX_ID').size().reindex(n.index,fill_value=0)
    filing=cg.FILESTAT.first().ne(6)
    if counts.gt(1).any() or counts.loc[~filing].ne(0).any():
        raise ValueError('Multiple tax payload carriers or nonfiler payload')
    zero=core.loc[core.TAX_ID.isin(counts.index[filing&counts.eq(0)])].copy()
    if not zero.WSAL_VAL.eq(0).all(): raise ValueError('Zero tax-payload filer with unresolved wage assignment')
    # Zero-income units have no payload identifying the head. One observed member is
    # a count convention only; export the full possible head-weight range separately.
    zero_selected=zero.sort_values('A_LINENO').drop_duplicates('TAX_ID')
    zero_weights=zero.groupby('TAX_ID').pwwgt0
    count_range={'minimum':float(zero_weights.min().sum()),
                 'selected':float(zero_selected.pwwgt0.sum()),
                 'maximum':float(zero_weights.max().sum())}
    scope_bounds={}
    for scope,mask in [('all_survey_persons',np.ones(len(zero),bool)),('civilian',zero.civilian),('civilian_household',zero.civilian&zero.household)]:
        eligible=zero.pwwgt0*mask
        zgroup=eligible.groupby(zero.TAX_ID)
        scope_bounds[scope]={'minimum':float(zgroup.min().sum()),'maximum':float(zgroup.max().sum())}
    dep=d.loc[d.DEP_STAT.gt(0)&d.FILESTAT.ne(6)].copy()
    if not dep.FILESTAT.eq(5).all():
        raise ValueError('Unexpected dependent-filer structure')
    result=pd.concat([carriers,zero_selected,dep]).copy()
    wages=core.groupby('TAX_ID').WSAL_VAL.sum()
    result['return_wages']=np.where(result.DEP_STAT.eq(0),result.TAX_ID.map(wages),result.WSAL_VAL)
    # Every nonzero tax dollar must be on exactly one selected filer record.
    if d.loc[~d.index.isin(result.index),PAYLOAD].ne(0).any().any():
        raise ValueError('Tax or AGI payload omitted from filer extraction')
    np.testing.assert_allclose(result[PAYLOAD].sum(),d[PAYLOAD].sum(),rtol=1e-13,atol=.001)
    if not result.index.is_unique: raise ValueError('Duplicate filer carriers')
    return result,{'core_filer_returns':len(carriers),'dependent_filer_returns':len(dep),
                   'zero_payload_filing_units':len(zero_selected),
                   'zero_payload_count_weight_range':count_range,
                   'zero_payload_scoped_count_bounds':scope_bounds,
                   'zero_payload_ambiguous_scope_units':int(zero.groupby('TAX_ID')[['civilian','household']].nunique().gt(1).any(axis=1).sum()),
                   'zero_payload_ambiguous_head_weights':int(zero.groupby('TAX_ID')[CW].nunique().gt(1).any(axis=1).sum()),
                   'zero_payload_nonfiling_core_units':int(cg.FILESTAT.first().eq(6).sum()),
                   'method':'Observed nonzero tax/AGI carrier per filing native TAX_ID plus each DEP_STAT>0 FILESTAT=5 dependent filer; all tax dollars conserved. Zero-payload filing units use first observed member only as a count convention, with head-weight bounds exported. Census modeled returns, not observed IRS filing.'}

"""Independent arithmetic checks on saved products, not implementation snapshots."""
from pathlib import Path
import argparse, json, math
import numpy as np
import pandas as pd
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/social')
O=parser.parse_args().output_dir
a=pd.read_csv(O/'cps_annual.csv');c=pd.read_csv(O/'cps_direct_contrasts.csv');p=pd.read_csv(O/'cps_equal_year_pool.csv')
for row in c.itertuples():
    left,right=row.group.split(' minus ')
    base=a[(a.year==row.year)&(a.subgroup==row.subgroup)&(a.metric==row.metric)&(a.standard==row.standard)].set_index('group')
    assert abs(base.loc[left,'estimate']-base.loc[right,'estimate']-row.estimate)<1e-10
    sl,sr=base.loc[left,'se'],base.loc[right,'se']
    assert abs(sl-sr)-1e-10<=row.se<=sl+sr+1e-10
for row in p.itertuples():
    source=a if row.kind=='level' else c
    ss=source[(source.subgroup==row.subgroup)&(source.group==row.group)&(source.metric==row.metric)&(source.standard==row.standard)]
    assert len(ss)==3 and abs(row.estimate-ss.estimate.sum()/3)<1e-10
    assert abs(row.se_unknown_cov_upper-ss.se.sum()/3)<1e-10
    assert row.se_unknown_cov_upper+1e-10>=row.se_independence_diagnostic
    assert abs(row.ci95_conservative_hi-row.estimate-1.96*row.se_unknown_cov_upper)<1e-10
# Exact two-PSU-strata formula: n/(n-1)*sum((Uj-mean)^2)=(U1-U2)^2.
for pair in [[.1,-.2],[0,0],[12,9]]:
    q=np.asarray(pair);assert abs(2*((q-q.mean())**2).sum()-(q[0]-q[1])**2)<1e-10
dist=pd.read_csv(O/'gss_trust_distribution.csv')
for (weight,group),rows in dist.groupby(['weight','group']):
    t=rows[rows.denominator=='three_responses'].set_index('code').estimate
    b=rows[(rows.denominator=='definite')&(rows.code==1)].iloc[0].estimate
    assert abs(b-t.loc[1]/(t.loc[1]+t.loc[2]))<1e-12
res=pd.read_csv(O/'gss_trust_residuals.csv')
assert np.allclose(res.groupby(['weight','group']).weighted_share_all.sum(),1)
(O/'validation.json').write_text(json.dumps({'status':'PASS','direct_CPS_contrasts':len(c),'pooled_CPS_rows':len(p),'GSS_response_partition_and_denominator_identity':'PASS','two_PSU_variance_identity':'PASS'},indent=2))
print('PASS: contrast, covariance, pool, partition and survey-variance arithmetic')
print('CPS annual disability:')
print(a[(a.subgroup=='all')&(a.metric=='disability')&(a.standard=='age_std_fixed2025white')][['year','group','n','events','estimate','se']].to_string(index=False))
print('Birth-cohort contrasts (crude within reported survey-year minus age bins, not panel trajectories):')
print(p[(p.kind=='contrast')&(p.subgroup.str.startswith('birth'))&(p.group.isin(['mex_g2 minus mex_born','mex_g3_selfid minus mex_g2']))][['subgroup','group','estimate','ci95_conservative_lo','ci95_conservative_hi']].to_string(index=False))
print('Source coverage',json.loads((O/'cps_audit.json').read_text())['join_gates'])

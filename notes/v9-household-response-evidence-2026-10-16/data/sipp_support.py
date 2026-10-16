"""Refine Type-2 candidate support from the already-read SIPP extract."""
import json
from pathlib import Path
import pandas as pd
out = Path(__file__).parent
d = pd.read_parquet(out/'sipp2025_selected.parquet').sort_values(['SSUID','PNUM','MONTHCODE'])
earnings_missing = d.assign(earn_missing=d.TPEARN.isna()).groupby('RMESR',dropna=False).earn_missing.agg(['size','sum'])
earnings_missing.to_csv(out/'sipp_earnings_missing.csv',lineterminator='\n')
d = d[d.TAGE_EHC.between(18,64) & d.THHLDSTATUS.isin([1,2,3,4])].copy()
prev = d.groupby(['SSUID','PNUM']).shift()
adj = d.MONTHCODE.eq(prev.MONTHCODE+1) & d.ERESIDENCEID.eq(prev.ERESIDENCEID)
exit_mask = pd.Series(False,index=d.index)
for i in range(1,11):
    exit_mask |= prev[f'ET2_LNO{i}'].ge(60) & prev[f'TT2_AGE{i}'].ge(18) & d[f'ET2_LNO{i}'].isna() & adj
events = d[exit_mask]
result = {}
for label, sub in [('all',events),('mexican_identifier_focal',events[events.EHISPAN.eq(1)]),('US_born_focal',events[events.EBORNUS.eq(1)])]:
    result[label] = {'candidate_person_event_months':len(sub),'unique_focal_people':len(sub[['SSUID','PNUM']].drop_duplicates()),
                     'events_month4to10':int(sub.MONTHCODE.between(4,10).sum()),
                     'no_job_prior_month':int(prev.loc[sub.index,'RMESR'].isin([6,7,8]).sum())}
result['three_months_each_side']={}
good=[]
groups={k:g.set_index('MONTHCODE') for k,g in d.groupby(['SSUID','PNUM'])}
for idx, row in events.iterrows():
    month=int(row.MONTHCODE)
    months=list(range(month-3,month+3))
    g=groups[(row.SSUID,row.PNUM)]
    if all(m in g.index for m in months) and g.loc[months,'RMESR'].between(1,8).all():
        good.append(idx)
g=events.loc[good]
assert len(g) <= result['all']['events_month4to10']
result['three_months_each_side']={'all_event_months':len(g),'mexican_identifier_focal_event_months':int(g.EHISPAN.eq(1).sum()),
                                  'note':'Three observed employment months before and three including/after first absent month. Not a causal or imputation-valid sample.'}
(out/'sipp_support.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

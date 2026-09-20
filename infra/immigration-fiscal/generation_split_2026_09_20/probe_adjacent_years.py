"""Adjacent ASEC feasibility candidates, never applied to the canonical split."""
import runpy
from pathlib import Path
import zipfile
import json
import hashlib
import numpy as np
import pandas as pd

state=runpy.run_path(str(Path(__file__).resolve().with_name('audit_unresolved.py')))
d=state['d']; m=state['m']; unresolved=state['unresolved']; weights=state['weights']
inconsistent=state['inconsistent']; root=state['root']
outdir=state['outdir']
paths={2024:root/'infra/immigration-fiscal/same_year_tax_2026_09_20/_cache/asecpub24csv.zip',
       2026:root/'infra/immigration-fiscal/ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip'}
hashes={2024:'cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09',
        2026:'fe819d0d2fc4470c282e76c247b8aa8b6054811619730307e9f2fe6186707d93'}
rows=[]; candidates={}; strict_candidates={}; audit=[]
def parent_histories(frame):
    lk=pd.Series(np.arange(len(frame)),index=pd.MultiIndex.from_frame(frame[['PH_SEQ','A_LINENO']]))
    result=[{} for _ in range(len(frame))]
    for slot in (1,2):
        line=frame[f'PEPAR{slot}'].to_numpy()
        par=lk.reindex(pd.MultiIndex.from_arrays([frame.PH_SEQ.to_numpy(),line])).fillna(-1).to_numpy(int)
        bio=(line>0)&(par>=0)&frame[f'PEPAR{slot}TYP'].eq(1).to_numpy()
        for i in np.flatnonzero(bio):
            p=par[i]
            result[i][frame.PERIDNUM.iloc[p]]=(int(frame.PENATVTY.iloc[p]),int(frame.PEMNTVTY.iloc[p]),int(frame.PEFNTVTY.iloc[p]))
    return result
current_histories=parent_histories(d)
def add(year,label,mask):
    for age,am in [('all',np.ones(len(d),bool)),('under18',d.A_AGE.lt(18).to_numpy()),('18plus',d.A_AGE.ge(18).to_numpy())]:
        use=unresolved&mask&am
        v=weights[use].sum(axis=0)
        rows.append(dict(year=year,criterion=label,age=age,n=int(use.sum()),people=v[0],se=np.sqrt(4/160*((v[1:]-v[0])**2).sum())))
for year,path in paths.items():
    if hashlib.sha256(path.read_bytes()).hexdigest() != hashes[year]:
        raise ValueError(f'CPS{year} source hash changed')
    with zipfile.ZipFile(path) as z:
        with z.open(f'pppub{str(year)[-2:]}.csv') as f:
            o=pd.read_csv(f,usecols=m.COLS+['PERIDNUM','A_SEX','PRDTRACE'],dtype={'PERIDNUM':str})
    assert o.PERIDNUM.notna().all() and o.PERIDNUM.is_unique
    labels=m.classify(o)
    o['g3']=labels['G3_Mexico_GP_observed']
    o['g4']=labels['G4plus_all_US_GP_observed']
    fields=['PERIDNUM','A_SEX','A_AGE','PENATVTY','PEMNTVTY','PEFNTVTY','PRCITSHP','PRDTHSP','g3','g4']
    q=d[fields[:-2]].merge(o[fields],on='PERIDNUM',how='left',validate='one_to_one',suffixes=('','_other'),indicator=True)
    matched=q._merge.eq('both').to_numpy()
    demo=matched&q.A_SEX.eq(q.A_SEX_other).to_numpy()
    delta=(q.A_AGE_other-q.A_AGE)*(1 if year==2026 else -1)
    demo &= delta.between(0,2).to_numpy()
    histories=demo.copy()
    for f in ['PENATVTY','PEMNTVTY','PEFNTVTY','PRCITSHP','PRDTHSP']:
        histories &= q[f].eq(q[f+'_other']).to_numpy()
    old_histories=parent_histories(o)
    old_lookup=pd.Series(np.arange(len(o)),index=o.PERIDNUM)
    old_i=old_lookup.reindex(d.PERIDNUM).fillna(-1).to_numpy(int)
    gp_consistent=np.ones(len(d),bool)
    no_shared_parent=np.zeros(len(d),bool)
    for i in np.flatnonzero(histories):
        a=current_histories[i]; b=old_histories[old_i[i]]
        shared=set(a)&set(b)
        # Every currently observed parent branch must be comparable; sharing
        # only one of two parents does not verify the other branch.
        no_shared_parent[i]=bool(set(a)-set(b))
        gp_consistent[i]=all(a[x]==b[x] for x in shared)
    g3=q.g3.eq(True).to_numpy()
    g4=q.g4.eq(True).to_numpy()
    add(year,'person_ID_match',matched)
    add(year,'age_sex_consistent_ID_match',demo)
    add(year,'own_parent_birth_identity_stable_match',histories)
    add(year,'classified_elsewhere_any_ID_match',matched&(g3|g4))
    add(year,'G3_candidate_stable_history_no_current_contradiction',histories&g3&~inconsistent)
    add(year,'G4_candidate_stable_history_no_current_contradiction',histories&g4&~inconsistent)
    add(year,'candidate_shared_parent_grandparent_history_conflict',histories&(g3|g4)&~inconsistent&~gp_consistent)
    add(year,'candidate_current_parent_present_but_unshared_ID',histories&(g3|g4)&~inconsistent&no_shared_parent)
    add(year,'G3_candidate_after_GP_consistency',histories&g3&~inconsistent&gp_consistent)
    add(year,'G4_candidate_after_GP_consistency',histories&g4&~inconsistent&gp_consistent)
    add(year,'G3_strict_candidate_GP_consistent_no_unshared_current_parent',histories&g3&~inconsistent&gp_consistent&~no_shared_parent)
    add(year,'G4_strict_candidate_GP_consistent_no_unshared_current_parent',histories&g4&~inconsistent&gp_consistent&~no_shared_parent)
    candidates[year]=(histories&g3&~inconsistent&gp_consistent,histories&g4&~inconsistent&gp_consistent)
    strict_candidates[year]=tuple(mask&~no_shared_parent for mask in candidates[year])
    audit.append({'year':year,'path':str(path),'sha256':hashes[year],'rows':len(o)})
g3=candidates[2024][0]|candidates[2026][0]
g4=candidates[2024][1]|candidates[2026][1]
conflict=g3&g4
add('union','cross_wave_G3_G4_conflict',conflict)
add('union','G3_candidate',g3&~conflict)
add('union','G4_candidate',g4&~conflict)
add('union','G3_strict_candidate',(strict_candidates[2024][0]|strict_candidates[2026][0])&~conflict)
add('union','G4_strict_candidate',(strict_candidates[2024][1]|strict_candidates[2026][1])&~conflict)
out=pd.DataFrame(rows)
out.to_csv(outdir/'cps_adjacent_generation_candidates_20260920.csv',index=False)
manifest=dict(current_source=state['audit'],adjacent_sources=audit,
              status='Unapplied feasibility candidates; all numbers use 2025 target weights',
              limitations=['Edited-field flags not fully adjudicated',
              'No complementary partial-branch union or monthly interview search',
              'Sampling SE excludes linkage and classification errors'])
(outdir/'cps_adjacent_generation_audit_20260920.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('\nADJACENT WAVE CANDIDATES (not final validated classifications):\n'+out.query('age=="all"').to_string(index=False))
print('\nUNION BY AGE:\n'+out.query('year=="union"').to_string(index=False))
gp=state['gp']
finite=gp[unresolved][np.isfinite(gp[unresolved])]
print('Other nonMexico GP codes in unresolved:',sorted(set(finite)-set(m.US)-{303}))

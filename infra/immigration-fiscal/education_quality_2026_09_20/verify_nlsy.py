"""Independent scalar verifier; does not import the analyzer."""
import csv
import json
import math
from pathlib import Path
from collections import Counter
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'education_quality_2026_09_20/derived/nlsy'
def read(p):
    with p.open() as f:
        return list(csv.DictReader(f))
def num(x):
    return float(x) if x not in ('',None) else math.nan
base = {r['R0000100']:r for r in read(ROOT/'new_datasets_2026_09_17/derived/nlsy/full_selected_data.csv')}
score = {r['R0000100']:r for r in read(ROOT/'frontier_execution_2026_09_17/derived/nlsy/selected.csv')}
family = {r['R0000100']:r for r in read(ROOT/'new_datasets_2026_09_17/derived/nlsy_family/family_analysis_rows.csv')}
saved = {r['R0000100']:r for r in read(OUT/'analysis_rows.csv')}
assert set(base)==set(score)==set(family)==set(saved) and len(base)==8984
def coalesce(row, fields):
    valid = {num(row[k]) for k in fields if num(row[k]) in (0,1)}
    return next(iter(valid)) if len(valid)==1 else None
rows=[]
for key,b in base.items():
    s,f = score[key],family[key]
    y=num(s['R9829600'])/1000 if num(s['R9829600'])>=0 else None
    deg=num(b['T8129600']) if num(b['T8129600']) in range(8) else None
    mex=any(num(b[k]) in (21,22,23) for k in ('R9702300','R9702400','R9702500'))
    white=not mex and num(b['R0538600'])==0 and num(b['R0538700'])==1
    ident='Mexican_Chicano_self_ID' if mex else 'Baseline_NH_White_not_Mexican_self_ID' if white else 'Other_or_unresolved'
    assert ident==f['comparison']==saved[key]['comparison']
    own=coalesce(b,['R5821400','S0191300','S2175900','S3952000','S7642200','T0135800'])
    mom,dad=num(f['mother_us']),num(f['father_us'])
    gps=[coalesce(b,z) for z in [['S7639500','T0133500'],['S7639800','T0133800'],['S7640100','T0134100'],['S7640400','T0134400']]]
    if own==0: gen='G1_foreign_born_childhood_resident'
    elif own==1 and (mom==0 or dad==0): gen='G2_USborn_at_least_one_foreign_biological_parent'
    elif own==mom==dad==1 and 0 in gps: gen='G3_USborn_USparents_foreign_grandparent'
    elif own==mom==dad==1 and all(z==1 for z in gps): gen='G4plus_USborn_USparents_all_four_USgrandparents'
    elif own==mom==dad==1: gen='USborn_USparents_grandparents_unresolved'
    else: gen='Generation_unresolved'
    assert gen==f['linked_exact']==saved[key]['linked_exact']
    r={'y':y,'degree':deg,'mex':mex,'white':white,'generation':gen,
       'base':num(s['R1236101'])/100,'wave':num(b['T8135900'])/100,
       'stratum':int(s['R1489700']),'psu':int(s['R1489800'])}
    for field,val in [('afqt_percentile',y),('degree_2013',deg),('BAplus_2013',None if deg is None else int(deg>=4)),('wbase',r['base']),('w2013',r['wave']),('stratum',r['stratum']),('psu',r['psu'])]:
        actual=num(saved[key][field])
        assert (val is None and math.isnan(actual)) or (val is not None and math.isclose(val,actual,rel_tol=1e-12,abs_tol=1e-12)), (key,field)
    rows.append(r)
grid=sorted({(r['stratum'],r['psu']) for r in rows})
strata=sorted({s for s,p in grid})
assert len(strata)==117 and all([(s,1),(s,2)]==[q for q in grid if q[0]==s] for s in strata)
df=len(grid)-len(strata)
crit=t.ppf(.975,df)
def group(r,name):
    gen=r['generation']
    definitions={'Mexican_self_ID_all_family_histories':r['mex'],
      'Mexican_self_ID_G2':r['mex'] and gen.startswith('G2_'),
      'Mexican_self_ID_G3':r['mex'] and gen.startswith('G3_'),
      'Mexican_self_ID_G4plus':r['mex'] and gen.startswith('G4plus_'),
      'Mexican_self_ID_G3_G4plus_pooled':r['mex'] and gen.startswith(('G3_','G4plus_')),
      'Mexican_self_ID_USparents_GP_unresolved':r['mex'] and gen=='USborn_USparents_grandparents_unresolved',
      'NH_white_all_family_histories':r['white'],'NH_white_G4plus':r['white'] and gen.startswith('G4plus_')}
    return name=='all' or definitions[name]
def credential(r,name):
    return name=='benchmark' or r['degree'] is not None and (name=='all_known_degree' or name=='BAplus' and r['degree']>=4 or name=='BA_only' and r['degree']==4)
def weight(r,name):
    return r['base'] if name=='baseline' else r['wave'] if name=='2013_interview' else r['base'] if r['wave']>0 else 0
def estimate(name,cred,wname):
    subset=[r for r in rows if group(r,name) and credential(r,cred) and r['y'] is not None and weight(r,wname)>0]
    den=math.fsum(weight(r,wname) for r in subset)
    mean=math.fsum(weight(r,wname)*r['y'] for r in subset)/den
    parts={q:[] for q in grid}
    for r in subset: parts[r['stratum'],r['psu']].append(weight(r,wname)*(r['y']-mean)/den)
    totals={q:math.fsum(v) for q,v in parts.items()}
    diffs={s:totals[s,1]-totals[s,2] for s in strata}
    variance=math.fsum(v*v for v in diffs.values())
    se=math.sqrt(variance)
    return dict(n=len(subset),mean_percentile=mean,design_se=se,low95=mean-crit*se,high95=mean+crit*se,
                kish_n=den*den/math.fsum(weight(r,wname)**2 for r in subset),
                domain_psus=len({(r['stratum'],r['psu']) for r in subset})),diffs
checks=[]
def check(label, expected, actual):
    err=abs(float(expected)-float(actual))
    checks.append({'key':label,'abs_error':err})
    assert math.isclose(float(expected),float(actual),rel_tol=1e-9,abs_tol=1e-9),(label,expected,actual)
bench,_=estimate('all','benchmark','baseline')
check('benchmark.n',7093,bench['n']);check('benchmark.mean',50.4099446909,bench['mean_percentile']);check('benchmark.se',.6376813718,bench['design_se'])
means={}
for out in read(OUT/'means.csv'):
    key=(out['weight'],out['credential'],out['group'])
    calc,diff=estimate(key[2],key[1],key[0]);means[key]=(calc,diff)
    for field,val in calc.items():check(str(key)+'.'+field,val,out[field])
max_se_independence_difference=0
for out in read(OUT/'contrasts.csv'):
    ka=(out['weight'],out['credential'],out['group']);kb=(out['weight'],out['credential'],out['reference'])
    a,da=means[ka];b,db=means[kb]
    diff=a['mean_percentile']-b['mean_percentile']
    se=math.sqrt(math.fsum((da[s]-db[s])**2 for s in strata))
    naive=math.hypot(a['design_se'],b['design_se'])
    max_se_independence_difference=max(max_se_independence_difference,abs(naive-se))
    for field,val in [('group_n',a['n']),('reference_n',b['n']),('difference_percentile_points',diff),('design_se',se),('low95',diff-crit*se),('high95',diff+crit*se)]:check(str(ka)+'.'+out['reference']+'.'+field,val,out[field])
for out in read(OUT/'coverage.csv'):
    sub=[r for r in rows if group(r,out['group'])]
    known=[r for r in sub if r['wave']>0 and r['degree'] is not None]
    ba=[r for r in known if r['degree']>=4];sc=[r for r in ba if r['y'] is not None]
    for field,val in [('baseline_n',len(sub)),('degree_2013_observed_n',len(known)),('BAplus_2013_n',len(ba)),('BAplus_and_score_n',len(sc)),('BAplus_score_missing_n',len(ba)-len(sc))]:check(out['group']+'.'+field,val,out[field])
bounds=[]
for out in read(OUT/'missing_score_bounds.csv'):
    sub=[r for r in rows if group(r,out['group']) and r['wave']>0 and r['degree'] is not None and r['degree']>=4]
    total=math.fsum(r['wave'] for r in sub)
    missing=math.fsum(r['wave'] for r in sub if r['y'] is None)
    lower=math.fsum(r['wave']*(r['y'] if r['y'] is not None else 0) for r in sub)/total
    upper=math.fsum(r['wave']*(r['y'] if r['y'] is not None else 100) for r in sub)/total
    vals={'BAplus_2013_n':len(sub),'missing_score_weight_fraction':missing/total,'mean_if_missing_scores_0':lower,'mean_if_missing_scores_100':upper}
    for field,val in vals.items():check(out['group']+'.bounds.'+field,val,out[field])
    bounds.append({'group':out['group'],'score_missing_n':sum(r['y'] is None for r in sub),**vals})
result={'verdict':'PASS','bench':bench,'strata':len(strata),'psus':len(grid),'df':df,'means_checked':len(means),'contrasts_checked':len(read(OUT/'contrasts.csv')),'numeric_checks':len(checks),'max_abs_error':max(x['abs_error'] for x in checks),'max_contrast_se_difference_from_wrong_independence_assumption':max_se_independence_difference,'missing_score_bounds':bounds,
 'score_missing':sum(r['y'] is None for r in rows),'wave_zero_weight':sum(r['wave']==0 for r in rows),'wave_negative_or_missing_weight':sum(not math.isfinite(r['wave']) or r['wave']<0 for r in rows),
 'degree_missing_by_retention':dict(Counter('retained' if r['wave']>0 else 'not_retained' for r in rows if r['degree'] is None)),
 'all_Mexican_identifiers_have_scores':all(r['y'] is not None for r in rows if r['mex']),
 'limits':['Conditional adolescent preparation among observed later degree holders; not college learning or institutional causal quality.','Mexican self-ID is collected during ASVAB, creating joint identity/test observation selection.','Generic ancestral birthplace, with audited parent linkage inputs; not exact Mexican ancestry.','Small Mexican G3/G4 BA samples; intervals omit selection and classification uncertainty.']}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

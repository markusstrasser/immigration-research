"""Independent scalar-loop arithmetic check; does not import analysis functions."""
import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy');a=p.parse_args();o=a.output_dir
def read(name):
    with (o/name).open() as f:return list(csv.DictReader(f))
rows=read('analysis_rows.csv');means=read('means.csv');contrasts=read('contrasts.csv')
assert len(rows)==8984 and len({r['R0000100'] for r in rows})==8984
def val(x):return float(x) if x else math.nan
for r in rows:
    if val(r['E8043000'])==-3:
        assert val(r['incarc_age12_before30'])!=0, 'Invalid first date must not establish no event'
assert any(val(r['E8043000'])==-4 and val(r['incarc_age12_before30'])==0 for r in rows), 'Valid no-event skip was lost'
def close(x,y):assert math.isclose(x,y,rel_tol=2e-10,abs_tol=1e-9),(x,y)
def domain(r,sex,group,comparison='Mexican_Chicano_self_ID',variant='linked_exact'):
    return (sex=='All' or r['sex']==sex) and r['comparison']==comparison and r[variant].startswith(group)
def scalar_est(metric,weight,pred):
    valid=[r for r in rows if pred(r) and not math.isnan(val(r[metric])) and val(r[weight])>0]
    den=math.fsum(val(r[weight]) for r in valid)
    mean=math.fsum(val(r[weight])*val(r[metric]) for r in valid)/den
    clusters=defaultdict(float)
    for r in valid:clusters[(int(r['stratum']),int(r['psu']))]+=val(r[weight])*(val(r[metric])-mean)/den
    return len(valid),mean,clusters
def variance(clusters):
    return math.fsum((clusters.get((s,1),0)-clusters.get((s,2),0))**2 for s in range(1,118))
metric_weights={r['metric']:r['weight'] for r in means}
checks=0
for out in means:
    if out['variant']!='linked_exact' or out['comparison']!='Mexican_Chicano_self_ID' or int(out['n'])==0:continue
    n,mean,clusters=scalar_est(out['metric'],out['weight'],lambda r:domain(r,out['sex'],out['group']))
    assert n==int(out['n']);close(mean,float(out['mean']));close(variance(clusters)**.5,float(out['se']));checks+=1
for out in contrasts:
    def pred(tag):
        if tag=='whiteG4':return lambda r:domain(r,out['sex'],'G4plus','Baseline_NH_White_not_Mexican_self_ID')
        return lambda r:domain(r,out['sex'],tag,variant='detail' if tag.startswith('G2_') else 'linked_exact')
    nh,mh,ch=scalar_est(out['metric'],metric_weights[out['metric']],pred(out['high']))
    nl,ml,cl=scalar_est(out['metric'],metric_weights[out['metric']],pred(out['low']))
    combined={k:ch.get(k,0)-cl.get(k,0) for k in set(ch)|set(cl)}
    assert nh==int(out['n_high']) and nl==int(out['n_low']);close(mh-ml,float(out['difference']));close(variance(combined)**.5,float(out['design_se']));checks+=1
for out in read('completion_bounds.csv'):
    pred=lambda r:domain(r,out['sex'],out['group'])
    selected=[r for r in rows if pred(r)]
    observed=[r for r in selected if val(r[metric_weights[out['metric']]])>0 and not math.isnan(val(r[out['metric']]))]
    total=math.fsum(val(r['wbase']) for r in selected)
    ev=math.fsum(val(r['wbase'])*val(r[out['metric']]) for r in observed)
    missing=total-math.fsum(val(r['wbase']) for r in observed)
    close(ev/total,float(out['lower']));close((ev+missing)/total,float(out['upper']));checks+=1
for out in read('classification_tipping_points.csv'):
    q=float(out['GP_unknown_fraction_assigned_G3_for_equal_means'])
    if not 0<=q<=1:continue
    totals=[]
    for group in ['G3_','G4plus','USborn_USparents_grandparents_unresolved']:
        selected=[r for r in rows if domain(r,out['sex'],group) and val(r[metric_weights[out['metric']]])>0 and not math.isnan(val(r[out['metric']]))]
        totals.append((math.fsum(val(r[metric_weights[out['metric']]])*val(r[out['metric']]) for r in selected),math.fsum(val(r[metric_weights[out['metric']]]) for r in selected)))
    (a3,b3),(a4,b4),(a,b)=totals
    close((a3+q*a)/(b3+q*b),(a4+(1-q)*a)/(b4+(1-q)*b));checks+=1
result={'verdict':'PASS','independent_cells_checked':checks,'method':'CSV-only scalar weighted sums; variance separately computed as sum of squared within-stratum PSU influence differences; all Mexican means, all contrasts, all completion bounds','rows':len(rows)}
(o/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

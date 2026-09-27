"""Joint-CPS diagnostic; writes only this audit's ignored _cache directory.

Uses producer functions and captures their in-memory inputs before any producer writes.
Re-runs baseline propagation into scratch, then varies only the central administrative
benefit factors jointly with its existing CPS deviations. Other omissions stay fixed.
"""
import contextlib
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[3]
F = ROOT / 'infra/immigration-fiscal'
OUT = pathlib.Path(__file__).resolve().parent / '_cache/uncertainty'
OUT.mkdir(exist_ok=True, parents=True)

def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, F / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

paths = ['uncertainty_propagation_2026_09_22/propagate.py',
         'admin_benefit_keys_2026_09_24/compare.py',
         'main_case_2026_09_24/package.cjs']
hashes = {p: hashlib.sha256((F/p).read_bytes()).hexdigest() for p in paths}
up = load(paths[0], 'audit_propagate')
ad = load(paths[1], 'audit_admin')
ctx = {}
up.OUT = OUT / 'baseline'
up.adopted_cases = lambda c, name: ctx.update(c)
sys.argv = ['probe', '--case', 'sept26_schools']
with (OUT/'baseline.log').open('w') as log, contextlib.redirect_stdout(log):
    up.main()

# Capture the producer's centrally defined programme tuples, before its record loop.
captured = {}
class Captured(Exception):
    pass
def trace(frame, event, arg):
    if frame.f_code == ad.main.__code__ and event == 'line' and 'progs' in frame.f_locals:
        captured.update(frame.f_locals)
        raise Captured()
    return trace
ad.share_comparisons = lambda: None
sys.settrace(trace)
try:
    ad.main()
except Captured:
    pass
finally:
    sys.settrace(None)

# Use the same averaged stack factors the central correction payload uses.
js = """const p=require('./infra/immigration-fiscal/main_case_2026_09_24/package.cjs');
const lines=['snap','other_state_welfare','family_and_general_assistance','unemployment','housing_subsidies'];
const out={};for(const line of lines){out[line]={};for(const a of ['personal','shared'])
out[line][a]=p.METHODS.reduce((s,m)=>s+p.stackFactor(p.STACKS[`row4+status_state_aware|central|${m}`],'spending',line,null)[a],0)/p.METHODS.length;}console.log(JSON.stringify(out));"""
factors = json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,text=True))
ben = {a: np.zeros(161) for a in ['personal','shared']}
pubcheck, factor_reps = [], {}
for prog, admin, comp, base, keys, line, share, acs, acs_screen, note in captured['progs']:
    invalid, _ = ad.validity(prog, admin, acs_screen)
    astates = [s for s in ad.ROUTE_A if not invalid[ad.STATES.index(s)]]
    spec = ad.specs_for(prog, admin, comp, ad.acs_m(acs), astates, base=base, invalid=invalid)['BV']
    for a, km in keys.items():
        kp = ad.key_parts(*km)
        f = ad.rekey(spec,kp)/kp['U']
        now = float(captured['alloc'].loc[(line,a),'target_bn'])*share
        delta = now*(f-1)
        factor_reps[(a,line)] = (f,now,share)
        if line != 'housing_subsidies':
            ben[a] += delta*factors[line][a]
        pubcheck.append(dict(programme=prog,allocation=a,line=line,delta=delta[0],se=ad.rep_se(delta),
                             stack_factor=factors[line][a]))
pc = pd.DataFrame(pubcheck)
pub = pd.read_csv(ad.D/'program_keys.csv').query("spec == 'BV'")
for r in pc.itertuples():
    p = pub[(pub.programme==r.programme)&(pub.allocation==r.allocation)].iloc[0]
    assert abs(r.delta-p.change_bn)<1e-8 and abs(r.se-p.change_se_bn)<1e-8

dest = F/'uncertainty_propagation_2026_09_22/derived/sept26_schools'
specs = pd.read_csv(dest/'spec_costs.csv')
lt = pd.read_csv(dest/'line_targets.csv').set_index(['side','line','key','allocation'])
published = pd.read_csv(dest/'case_uncertainty.csv').query("case == 'sept26_schools'").reset_index(drop=True)
def target(tag,side,line,key,a):
    v=lt.loc[(side,line,key,a),'target_'+tag+'_bn']
    return 0 if pd.isna(v) else float(v)
def ratio(kind,line,a):
    side,key=('receipt','cbo_collective') if kind=='receipt' else ('spending',ctx['lane_keys'][(a,line)])
    t0=target('uncorrected',side,line,key,a)
    return target('sept26_schools',side,line,key,a)/t0 if t0 else 1

rows=[]
for i,s in enumerate(specs.itertuples()):
    a=s.allocation
    cases=ctx['cases']
    c=cases[(cases.profile==up.MAIN_PROFILE)&(cases.allocation==a)&(cases.normalization==s.normalization)
            &np.isclose(cases.school_share,s.share,atol=1e-6)&np.isclose(cases.school_response,s.school_sept24)].iloc[0]
    cc=ctx['comps'].query('case_id == @c.case_id')
    resp={r.component:r.response for r in cc.itertuples() if r.component in up.SERVICE_CATEGORIES}
    resp['education_services']=s.share*s.school+1-s.share
    dev=np.zeros(161)
    for (al,kind,line),rep in ctx['line_reps'].items():
        if al!=a: continue
        sign,weight=(1,1) if kind=='receipt' else (-1,1 if kind=='transfer' else resp[line])
        dev+=sign*weight*ratio(kind,line,a)*(rep-rep[0])
    g=ctx['spending'].query("allocation == @a and category == 'general_public_services'").iloc[0]
    gps=g.national_bn*ctx['hf']*ctx['skeys'][a][g.allocation_key]
    ctx['lane_keys'][(a,'general_public_services')]=g.allocation_key
    dev-=s.gg*ratio('service','general_public_services',a)*(gps-gps[0])
    old=up.sdr(dev)
    assert abs(old-published.iloc[i].se_cps_fiscal_keys_bn)<1e-8
    b=-(ben[a]-ben[a][0])
    b_exact=np.zeros(161)
    for (al,line),(f,now,share) in factor_reps.items():
        if al!=a or line=='housing_subsidies': continue
        rep=ctx['line_reps'][(a,'transfer',line)]
        b_exact-=factors[line][a]*share*rep*(f-f[0])
    # Correct the uncertainty of the factors that were fixed in the old gradient.
    joint=up.sdr(dev+b)
    naive=float(np.hypot(old,up.sdr(b)))
    cov=float(4/160*np.dot(dev[1:]-dev[0],b[1:]-b[0]))
    rows.append(dict(allocation=a,normalization=s.normalization,cost=published.iloc[i].net_cost_bn,
                     original_cps_se=old,benefit_factor_se=up.sdr(b),cov_bn2=cov,
                     corr=cov/(old*up.sdr(b)),independent_append_cps_se=naive,joint_firstorder_cps_se=joint,
                     joint_factor_product_cps_se=up.sdr(dev+b_exact),
                     published_combined_with_benefits=published.iloc[i].se_with_benefit_keys_bn,
                     joint_combined_se=float(np.sqrt(published.iloc[i].se_combined_independent_bn**2-old**2+joint**2))))
pd.DataFrame(rows).to_csv(OUT/'joint_benefits.csv',index=False,lineterminator='\n')
pc.to_csv(OUT/'producer_reproduction.csv',index=False,lineterminator='\n')
result={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'hashes':hashes,'hashes_unchanged':all(hashes[p]==hashlib.sha256((F/p).read_bytes()).hexdigest() for p in paths),
        'results_by_allocation':pd.DataFrame(rows).groupby('allocation').agg(['min','max']).to_dict(),
        'check':'All central BV point corrections and delta SEs reproduced to 1e-8; all 64 published CPS SEs reproduced to 1e-8.'}
# Flatten tuple column keys for a portable summary.
assert result['hashes_unchanged'], 'Source changed during the diagnostic'
result['results_by_allocation']={str(k):v for k,v in result['results_by_allocation'].items()}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(pd.DataFrame(rows).groupby('allocation').agg(['min','max']).to_string())
print(result['check'])

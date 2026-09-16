"""Log-log regression: suspects per 100k vs origin GDP pc, majority-Muslim dummy, age-sex control."""
import csv, math, os, json
import numpy as np
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=list(csv.DictReader(open(os.path.join(D,'de_nationality_rates.csv'))))

def ols(y,X,names):
    XtX=X.T@X; b=np.linalg.solve(XtX,X.T@y); e=y-X@b
    n,k=X.shape
    XtXi=np.linalg.inv(XtX)
    # HC1 robust
    S=(X*e[:,None]).T@(X*e[:,None])
    V=XtXi@S@XtXi*(n/(n-k))
    se=np.sqrt(np.diag(V))
    r2=1-e@e/((y-y.mean())@(y-y.mean()))
    return b,se,r2,n,names

def run(sample,ycol,extra=None,label=''):
    d=[]
    for r in sample:
        if not r['gdp_pc_2023'] or not r[ycol] or float(r[ycol])<=0: continue
        rec=[math.log(float(r['gdp_pc_2023'])), 1.0 if r['muslim_majority']=='1' else 0.0]
        if extra:
            ok=True
            for c in extra:
                if not r[c]: ok=False; break
                rec.append(float(r[c]))
            if not ok: continue
        d.append(([1.0]+rec, math.log(float(r[ycol]))))
    X=np.array([x for x,_ in d]); y=np.array([v for _,v in d])
    names=['const','log_gdp_pc','muslim_majority']+(extra or [])
    b,se,r2,n,_=ols(y,X,names)
    print(f"--- {label}  y=log({ycol})  n={n}  R2={r2:.3f}")
    for nm,bb,ss in zip(names,b,se):
        t=bb/ss
        print(f"    {nm:22s} {bb:8.4f}  (se {ss:.4f}, t {t:6.2f})"+(f"   => {100*(math.exp(bb)-1):+.1f}%" if nm=='muslim_majority' else ""))
    return b,se,n

big=[r for r in rows if int(r['pop_2025'])>=10000]
allc=rows
print("=== Pueyo replication: rate EXCLUDING immigration-law offences ===")
run(big,'rate_total_excl_imm',None,'>=10k residents')
run(allc,'rate_total_excl_imm',None,'all nationalities')
print()
print("=== Same but INCLUDING immigration-law offences (his chart axis) ===")
run(big,'rate_total_all',None,'>=10k residents')
run(allc,'rate_total_all',None,'all nationalities')
print()
print("=== Add age-sex control: share of residents who are men 18-39 ===")
run(big,'rate_total_excl_imm',['share_m1839'],'>=10k residents')
run(allc,'rate_total_excl_imm',['share_m1839'],'all nationalities')
run(big,'rate_total_all',['share_m1839'],'>=10k, incl. imm. offences')
print()
print("=== Violent crime ===")
run(big,'rate_violent',None,'>=10k residents')
run(big,'rate_violent',['share_m1839'],'>=10k + age-sex')

print()
print("=== Population-weighted (WLS, weight = residents) and correlation diagnostics ===")
def wls(sample,ycol,extra=None,label=''):
    d=[]
    for r in sample:
        if not r['gdp_pc_2023'] or not r[ycol] or float(r[ycol])<=0: continue
        rec=[math.log(float(r['gdp_pc_2023'])), 1.0 if r['muslim_majority']=='1' else 0.0]
        if extra: rec+= [float(r[c]) for c in extra]
        d.append(([1.0]+rec, math.log(float(r[ycol])), int(r['pop_2025'])))
    X=np.array([x for x,_,_ in d]); y=np.array([v for _,v,_ in d]); w=np.array([float(p) for _,_,p in d])
    sw=np.sqrt(w); Xw=X*sw[:,None]; yw=y*sw
    b=np.linalg.solve(Xw.T@Xw,Xw.T@yw); e=yw-Xw@b
    n,k=Xw.shape; XtXi=np.linalg.inv(Xw.T@Xw)
    S=(Xw*e[:,None]).T@(Xw*e[:,None]); V=XtXi@S@XtXi*(n/(n-k)); se=np.sqrt(np.diag(V))
    names=['const','log_gdp_pc','muslim_majority']+(extra or [])
    print(f"--- WLS {label} y=log({ycol}) n={n}")
    for nm,bb,ss in zip(names,b,se):
        print(f"    {nm:22s} {bb:8.4f} (se {ss:.4f}, t {bb/ss:6.2f})"+(f"  => {100*(math.exp(bb)-1):+.1f}%" if nm=='muslim_majority' else ""))
wls(big,'rate_total_excl_imm',None,'>=10k')
wls(allc,'rate_total_excl_imm',None,'all')
wls(big,'rate_total_excl_imm',['share_m1839'],'>=10k + age-sex')

m=np.array([1.0 if r['muslim_majority']=='1' else 0.0 for r in big])
s=np.array([float(r['share_m1839']) for r in big])
g=np.array([math.log(float(r['gdp_pc_2023'])) for r in big if r['gdp_pc_2023']])
print(f"corr(muslim, share_m1839) = {np.corrcoef(m,s)[0,1]:.3f}")
print(f"mean share_m1839: muslim={s[m==1].mean():.3f} non-muslim={s[m==0].mean():.3f} German baseline=0.121")

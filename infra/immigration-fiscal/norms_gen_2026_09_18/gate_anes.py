"""Gate: reproduce the attitudes_gen_2026_09_16 ANES pooled means with this lane's
loader, weights and generation coding."""
import numpy as np, pandas as pd, math
S={2020:dict(f="raw/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_csv_20220210.csv",
     w="V200010b",psu="V200010c",st="V200010d",hisp="V201558x",race="V201549x",par="V201553",
     born="V201554",th_h="V202479",th_w="V202482",imm="V202232"),
   2024:dict(f="raw/anes_timeseries_2024_csv_20260519/anes_timeseries_2024_csv_20260519.csv",
     w="V240107b",psu="V240107c",st="V240107d",hisp="V241512x",race="V241501x",par="V241506",
     born="V241507",th_h="V242515",th_w="V242518",imm="V242227")}
F=[]
for y,s in S.items():
    d=pd.read_csv(s["f"],usecols=[v for k,v in s.items() if k!="f"],low_memory=False)
    d=d.rename(columns={v:k for k,v in s.items() if k!="f"})
    for c in d.columns: d[c]=pd.to_numeric(d[c],errors="coerce")
    d["year"]=y
    for t in ("th_h","th_w"): d[t]=d[t].where(d[t].between(0,100))
    d["net"]=d.th_h-d.th_w
    g=pd.Series(np.nan,index=d.index)
    g[d.born.eq(4)]=1; g[d.born.isin([1,2,3])&d.par.isin([2,3])]=2; g[d.born.isin([1,2,3])&d.par.eq(1)]=3
    d["gen"]=g; d["hispanic"]=d.hisp.isin([1,2,3,4]); d["nhwhite"]=d.race.eq(1)
    d["immig_reduce"]=(d.imm.isin([4,5])).where(d.imm.between(1,5))
    F.append(d)
D=pd.concat(F,ignore_index=True)
def grp(r):
    if r.hispanic and r.gen==1: return "Hisp G1"
    if r.hispanic and r.gen==2: return "Hisp G2"
    if r.hispanic and r.gen==3: return "Hisp G3+"
    if r.nhwhite and r.gen==3: return "NHWhite G3+"
    return None
D["grp"]=D.apply(grp,axis=1)
def wstat(s,col):
    s=s[s[col].notna()&s.w.notna()&(s.w>0)]
    x=s[col].astype(float).values; w=s.w.values; m=np.average(x,weights=w)
    cl=s.assign(_r=w*(x-m)).groupby([s.year,s.st,s.psu])["_r"].sum(); nc=len(cl)
    return len(s), m, float(np.sqrt((cl**2).sum())/w.sum()*np.sqrt(nc/max(nc-1,1)))
T={("net","Hisp G1"):(11.7,2.2),("net","Hisp G2"):(15.3,1.7),("net","Hisp G3+"):(12.3,1.5),
   ("net","NHWhite G3+"):(-1.2,0.4),("th_h","Hisp G1"):(80.0,1.7),("th_w","NHWhite G3+"):(70.6,0.3),
   ("immig_reduce","Hisp G1"):(.219,.030),("immig_reduce","Hisp G3+"):(.350,.033),
   ("immig_reduce","NHWhite G3+"):(.380,.009)}
ok=True
print("gate vs attitudes_gen_2026_09_16/anes_gen_results.csv:")
for (col,g),(te,ts) in T.items():
    n,m,se=wstat(D[D.grp==g],col); tol=0.06 if abs(te)>1 else 0.0015
    good=abs(m-te)<tol and abs(se-ts)<tol; ok&=good
    print(f"  {col:13s} {g:12s} mine {m:8.3f} ({se:.3f}) n={n:5d}  theirs {te:8.3f} ({ts:.3f})  {'ok' if good else 'MISMATCH'}")
print("GATE:", "PASS" if ok else "FAIL"); assert ok

import pandas as pd, numpy as np
SPEC={
 2020: dict(f="raw/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_csv_20220210.csv",
   w="V200010b",psu="V200010c",st="V200010d",hisp="V201558x",race="V201549x",
   par="V201553",born="V201554",th_h="V202479",th_w="V202482",imm="V202232",job="V201255"),
 2024: dict(f="raw/anes_timeseries_2024_csv_20260519/anes_timeseries_2024_csv_20260519.csv",
   w="V240107b",psu="V240107c",st="V240107d",hisp="V241512x",race="V241501x",
   par="V241506",born="V241507",th_h="V242515",th_w="V242518",imm="V242227",job="V241252"),
}
def load(y):
    s=SPEC[y]; cols=[v for k,v in s.items() if k!="f"]
    d=pd.read_csv(s["f"],usecols=cols,low_memory=False).rename(columns={v:k for k,v in s.items() if k!="f"})
    for c in d.columns: d[c]=pd.to_numeric(d[c],errors="coerce")
    d["year"]=y
    # thermometers: valid 0-100
    for t in ["th_h","th_w"]: d[t]=d[t].where(d[t].between(0,100))
    d["net"]=d.th_h-d.th_w
    d["hispanic"]=d.hisp.isin([1,2,3,4])
    d["nhwhite"]=(d.race==1)
    g=pd.Series(np.nan,index=d.index)
    g[d.born==4]=1                                   # born another country
    g[(d.born.isin([1,2,3]))&(d.par.isin([2,3]))]=2  # US-born, >=1 foreign parent
    g[(d.born.isin([1,2,3]))&(d.par==1)]=3           # US-born, both parents US-born
    d["gen"]=g
    d["immig_reduce"]=(d.imm.isin([4,5])).where(d.imm.between(1,5))
    d["guarjob"]=(8-d.job).where(d.job.between(1,7))  # higher = govt should guarantee
    return d
D=pd.concat([load(2020),load(2024)],ignore_index=True)
def grp(r):
    if r.hispanic and r.gen==1: return "Hisp G1"
    if r.hispanic and r.gen==2: return "Hisp G2"
    if r.hispanic and r.gen==3: return "Hisp G3+"
    if r.nhwhite and r.gen==3: return "NHWhite G3+"
    if r.nhwhite: return "NHWhite G1-2"
    return None
D["grp"]=D.apply(grp,axis=1)
def wstat(s,col):
    s=s[s[col].notna()&s.w.notna()&(s.w>0)]
    if len(s)==0: return None
    x=s[col].astype(float).values; ww=s.w.values; m=np.average(x,weights=ww)
    cl=s.assign(_r=ww*(x-m)).groupby([s.year,s.st,s.psu])["_r"].sum(); nc=len(cl)
    se=np.sqrt((cl**2).sum())/ww.sum()*np.sqrt(nc/max(nc-1,1))
    return len(s),m,se,nc
rows=[]
for col in ["th_h","th_w","net","immig_reduce","guarjob"]:
    for lab,sub in [("pooled",D)]+[(str(y),D[D.year==y]) for y in (2020,2024)]:
        for g in ["Hisp G1","Hisp G2","Hisp G3+","NHWhite G3+","NHWhite G1-2"]:
            r=wstat(sub[sub.grp==g],col)
            if r: rows.append(dict(item=col,sample=lab,group=g,n=r[0],mean=round(r[1],3),se=round(r[2],3),clusters=r[3]))
res=pd.DataFrame(rows); res.to_csv("anes_gen_results.csv",index=False)
print(res[res["sample"]=="pooled"].to_string(index=False))
print("\nGATE white->white thermometer (NH white respondents, all gens), weighted:")
for y in (2020,2024):
    s=D[(D.year==y)&D.nhwhite]; r=wstat(s,"th_w"); print(f"  {y}: mean={r[1]:.1f} se={r[2]:.2f} n={r[0]}")
    ra=wstat(D[D.year==y],"th_w"); print(f"  {y} ALL respondents toward whites: mean={ra[1]:.1f} n={ra[0]}")
print("\nweighted generation shares among Hispanic respondents:")
for y in (2020,2024):
    h=D[(D.year==y)&D.hispanic&D.grp.notna()&D.w.notna()]
    print(" ",y,(h.groupby("grp").w.sum()/h.w.sum()).round(3).to_dict())
print("\nunweighted n by group/year:"); print(D.groupby(["year","grp"]).size().to_string())

import pandas as pd, numpy as np, math
S={2020:dict(f="raw/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_csv_20220210.csv",
   lang="V201001",wpre="V200010a",wpost="V200010b",psu="V200010c",st="V200010d",hisp="V201558x",
   race="V201549x",born="V201554",par="V201553",strpres="V201372x",viol="V201602",
   obed="V202268",resp="V202266",lead="V202413",adapt="V202416",prefdem=None),
   2024:dict(f="raw/anes_timeseries_2024_csv_20260519/anes_timeseries_2024_csv_20260519.csv",
   lang="V241001",wpre="V240107a",wpost="V240107b",psu="V240107c",st="V240107d",hisp="V241512x",
   race="V241501x",born="V241507",par="V241506",strpres="V241330x",viol="V241579",
   obed="V242262",resp="V242260",lead="V242411",adapt=None,prefdem="V242409")}
F=[]
for y,s in S.items():
    cols=[v for k,v in s.items() if k!="f" and v]
    d=pd.read_csv(s["f"],usecols=cols,low_memory=False).rename(columns={v:k for k,v in s.items() if k!="f" and v})
    for c in d.columns: d[c]=pd.to_numeric(d[c],errors="coerce")
    d["year"]=y
    for k in ["strpres","viol","obed","resp","lead","adapt","prefdem"]:
        if k not in d: d[k]=np.nan
    F.append(d)
D=pd.concat(F,ignore_index=True)
g=pd.Series(np.nan,index=D.index); g[D.born.eq(4)]=1
g[D.born.isin([1,2,3])&D.par.isin([2,3])]=2; g[D.born.isin([1,2,3])&D.par.eq(1)]=3
D["gen"]=g; D["hispanic"]=D.hisp.isin([1,2,3,4])
O={"strpres_helpful":(D.strpres.where(D.strpres>=0).le(3),"pre"),
   "violence_justified":(D.viol.where(D.viol>=0).isin([2,3,4,5]),"pre"),
   "auth_obedience":(D.obed.where(D.obed>=0).eq(1),"post"),
   "auth_respect":(D.resp.where(D.resp>=0).eq(2),"post"),
   "strleader_agree":(D.lead.where(D.lead>=0).le(2),"post"),
   "minorities_adapt":(D.adapt.where(D.adapt>=0).le(2),"post"),
   "prefer_democracy":(D.prefdem.where(D.prefdem>=0).le(2),"post")}
SRC={"strpres_helpful":D.strpres,"violence_justified":D.viol,"auth_obedience":D.obed,
     "auth_respect":D.resp,"strleader_agree":D.lead,"minorities_adapt":D.adapt,"prefer_democracy":D.prefdem}
rows=[]
for name,(y01,stage) in O.items():
    src=SRC[name]; valid=src.notna()&src.ge(0)
    yy=y01.where(valid).astype(float)
    w=(D.wpost if stage=="post" else D.wpre)
    for gname,mask in [("Hisp G1 Spanish",D.hispanic&D.gen.eq(1)&D.lang.eq(2)),
                       ("Hisp G1 English",D.hispanic&D.gen.eq(1)&D.lang.eq(1)),
                       ("Hisp G3+",D.hispanic&D.gen.eq(3)),
                       ("NHWhite G3+",D.race.eq(1)&D.gen.eq(3))]:
        m=(mask&yy.notna()&w.notna()&w.gt(0)).to_numpy()
        if m.sum()<15: continue
        x=yy.to_numpy()[m]; ww=w.to_numpy()[m]; est=float(ww@x/ww.sum())
        cl=pd.DataFrame({"r":ww*(x-est)}).groupby([D.year.to_numpy()[m],D.st.to_numpy()[m],D.psu.to_numpy()[m]]).r.sum()
        se=float(np.sqrt((cl**2).sum())/ww.sum()*np.sqrt(len(cl)/max(len(cl)-1,1)))
        rows.append(dict(item=name,group=gname,n=int(m.sum()),mean=est,se=se))
R=pd.DataFrame(rows); R.to_csv("derived/anes_language_check.csv",index=False)
R["cell"]=R.apply(lambda r:f"{r['mean']*100:.1f} ({r.se*100:.1f}) n={r.n}",axis=1)
pd.set_option("display.width",200)
print(R.pivot(index="item",columns="group",values="cell").to_string())

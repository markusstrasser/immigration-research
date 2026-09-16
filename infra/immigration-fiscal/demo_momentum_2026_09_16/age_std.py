import zipfile, pandas as pd, numpy as np
Z="/Users/alien/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
COLS=["PH_SEQ","PPPOS","A_AGE","A_SEX","PRCITSHP","PENATVTY","PEFNTVTY","PEMNTVTY","PEHSPNON","PRDTRACE","PRDTHSP","MARSUPWT","PEPAR1","PEPAR2"]
US=[57,60,66,69,73,78]
d=pd.read_csv(zipfile.ZipFile(Z).open("pppub25.csv"),usecols=COLS); d["w"]=d.MARSUPWT/100
kids=d[d.A_AGE<5]; L=[]
for c in("PEPAR1","PEPAR2"):
    k=kids[kids[c]>0][["PH_SEQ",c]].copy(); k["PPPOS"]=k[c]+40; L.append(k[["PH_SEQ","PPPOS"]])
nk=pd.concat(L).groupby(["PH_SEQ","PPPOS"]).size().rename("nk")
d=d.merge(nk,on=["PH_SEQ","PPPOS"],how="left"); d["nk"]=d.nk.fillna(0)
w=d[(d.A_SEX==2)&d.A_AGE.between(15,44)].copy()
ub=w.PENATVTY.isin(US); pu=w.PEFNTVTY.isin(US)&w.PEMNTVTY.isin(US); pm=w.PEFNTVTY.eq(303)|w.PEMNTVTY.eq(303)
G={"Mexico-born":w.PRCITSHP.isin([4,5])&w.PENATVTY.eq(303),
   "Mexican 2nd gen":ub&pm,
   "Mexican 3rd+ gen":ub&pu&w.PRDTHSP.eq(1),
   "NH white 3rd+ gen":ub&pu&w.PEHSPNON.eq(2)&w.PRDTRACE.eq(1)}
w["ag"]=pd.cut(w.A_AGE,[14,19,24,29,34,39,44],labels=["15-19","20-24","25-29","30-34","35-39","40-44"])
std=w[G["NH white 3rd+ gen"]].groupby("ag",observed=True).w.sum(); std=std/std.sum()
rows=[]
for n,m in G.items():
    s=w[m]; asr=s.groupby("ag",observed=True).apply(lambda x:np.average(x.nk,weights=x.w))
    cnt=s.groupby("ag",observed=True).size()
    crude=np.average(s.nk,weights=s.w); adj=float((asr.reindex(std.index).fillna(0)*std).sum())
    rows.append([n,len(s),round(crude,4),round(adj,4),round(adj*6,2)]+[round(float(asr.get(a,np.nan)),3) for a in std.index]+[int(cnt.get(a,0)) for a in std.index])
cols=["group","n","crude","age_std","implied_TFR_x6"]+[f"r_{a}" for a in std.index]+[f"n_{a}" for a in std.index]
t=pd.DataFrame(rows,columns=cols); print(t.to_string(index=False)); t.to_csv("cps_fertility_agestd.csv",index=False)
print("\nNH white 15-44 age weights:", dict(std.round(3)))

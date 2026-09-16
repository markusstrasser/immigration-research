import pyreadstat, numpy as np, pandas as pd
P="raw/GSS_stata/gss7224_r3a.dta"
cols=["year","wtssps","wtssall","vpsu","vstrat","born","parborn","hispanic","race",
 "trust","eqwlth","helppoor","natfare","letin1","partyid","immcrime","age","educ"]
df,meta=pyreadstat.read_dta(P, usecols=cols, encoding="latin1")
def num(s): return pd.to_numeric(s, errors="coerce")
for c in cols: df[c]=num(df[c])
df=df[df.year>=2000].copy()
w = df.wtssps.fillna(df.wtssall)
df["w"]=w
print("weight coverage 2000+:", df.w.notna().mean().round(3), "| years:", int(df.year.min()), int(df.year.max()))

# generation
gen=pd.Series(np.nan,index=df.index)
gen[df.born==2]=1
gen[(df.born==1)&(df.parborn.isin([1,2,3,4,5,6,7,8]))]=2
gen[(df.born==1)&(df.parborn==0)]=3
df["gen"]=gen
df["hisp"]=df.hispanic>=2
df["nhwhite"]=(df.race==1)&(df.hispanic==1)

def grp(r):
    if r.hisp and r.gen==1: return "Hisp G1"
    if r.hisp and r.gen==2: return "Hisp G2"
    if r.hisp and r.gen==3: return "Hisp G3+"
    if r.nhwhite and r.gen==3: return "NHWhite G3+"
    if r.nhwhite: return "NHWhite G1-2"
    return None
df["grp"]=df.apply(grp,axis=1)
d=df[df.grp.notna()&df.w.notna()].copy()

# outcomes (higher = more left / more of the named thing)
d["redist"]=8-d.eqwlth            # 1-7, higher=govt should reduce income diffs
d["helppoor_r"]=6-d.helppoor      # 1-5, higher=govt should help
d["welfare_toolittle"]=(d.natfare==1).where(d.natfare.isin([1,2,3]))
d["immig_reduce"]=(d.letin1.isin([4,5])).where(d.letin1.isin([1,2,3,4,5]))
d["pid_dem"]=(d.partyid.isin([0,1,2])).where(d.partyid<=6)
d["pid_strong"]=(d.partyid.isin([0,6])).where(d.partyid<=6)
d["trust_yes"]=(d.trust==1).where(d.trust.isin([1,2]))
d["immcrime_agree"]=(d.immcrime.isin([1,2])).where(d.immcrime.isin([1,2,3,4,5]))

OUT=["redist","helppoor_r","welfare_toolittle","immig_reduce","pid_dem","pid_strong","trust_yes","immcrime_agree"]
rows=[]
for o in OUT:
    for g,sub in d.groupby("grp"):
        s=sub[sub[o].notna()]
        if len(s)==0: continue
        x=s[o].astype(float).values; ww=s.w.values
        m=np.average(x,weights=ww)
        # cluster-robust SE on (year,vstrat,vpsu)
        cl=s.assign(_r=ww*(x-m)).groupby([s.year,s.vstrat,s.vpsu])["_r"].sum()
        nc=len(cl); W=ww.sum()
        se=np.sqrt((cl**2).sum())/W * np.sqrt(nc/max(nc-1,1))
        rows.append(dict(item=o,group=g,n=len(s),mean=round(m,4),se=round(se,4),clusters=nc))
r=pd.DataFrame(rows).sort_values(["item","group"])
r.to_csv("gss_gen_results.csv",index=False)
print(r.to_string(index=False))
# generation shares among Hispanics
h=d[d.hisp]
print("\nWeighted generation shares among Hispanic respondents (GSS 2000-2024):")
print((h.groupby("grp").w.sum()/h.w.sum()).round(3).to_string())
print("unweighted n:", h.grp.value_counts().to_dict())

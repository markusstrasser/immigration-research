import pyreadstat, numpy as np, pandas as pd, statsmodels.formula.api as smf
exec(open("gss_gen.py").read().split("OUT=")[0])
OUT=["redist","helppoor_r","welfare_toolittle","immig_reduce","pid_dem","pid_strong","trust_yes","immcrime_agree"]
d["grp"]=pd.Categorical(d.grp,categories=["NHWhite G3+","Hisp G1","Hisp G2","Hisp G3+","NHWhite G1-2"])
d["cl"]=d.year.astype(str)+"_"+d.vstrat.astype(str)+"_"+d.vpsu.astype(str)
rows=[]
for o in OUT:
    s=d[d[o].notna()&d.age.notna()&d.educ.notna()].copy(); s["y"]=s[o].astype(float)
    m=smf.wls("y ~ C(grp) + age + I(age**2) + educ + C(year)", data=s, weights=s.w).fit(cov_type="cluster",cov_kwds={"groups":s.cl})
    for k in ["C(grp)[T.Hisp G1]","C(grp)[T.Hisp G2]","C(grp)[T.Hisp G3+]"]:
        rows.append(dict(item=o,contrast=k.split("T.")[1][:-1],coef=round(m.params[k],4),se=round(m.bse[k],4),n=int(m.nobs)))
r=pd.DataFrame(rows); r.to_csv("gss_gen_adjusted.csv",index=False)
print("Adjusted gap vs NH white G3+ (age, age^2, educ, year FE; weighted; cluster SE)")
print(r.to_string(index=False))

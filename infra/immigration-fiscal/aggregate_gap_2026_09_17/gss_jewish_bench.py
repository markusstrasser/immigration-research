import pandas as pd, numpy as np, sys
sys.path.insert(0, ".")
from generation import gss_generation
cols=["year","wtssps","wtssall","born","parborn","hispanic","race","age","relig","coninc","realinc","degree","sex"]
df=pd.read_stata("raw/GSS_stata/gss7224_r3a.dta",columns=cols,convert_categoricals=False)
df=df[(df.year>=2000)&(df.age.between(25,64))]
w=df.wtssps.fillna(df.wtssall)
gen=gss_generation(df.born, df.parborn)
white3=(df.race==1)&(df.hispanic==1)&(gen==3)
d=df[white3].assign(w=w[white3])
d=d[d.coninc.notna()&d.w.notna()]
jew=d.relig==3
def wm(s,ww): return np.average(s,weights=ww)
sh=d.w[jew].sum()/d.w.sum()
mj=wm(d.coninc[jew],d.w[jew]); mo=wm(d.coninc[~jew],d.w[~jew]); ma=wm(d.coninc,d.w)
print(f"white NH 3rd+ 25-64, GSS 2000-2024: n={len(d)}, Jewish n={jew.sum()}, weighted Jewish share={sh:.3%}")
print(f"mean family income (2000$ coninc): Jewish {mj:,.0f}  other {mo:,.0f}  all {ma:,.0f}; ratio J/other {mj/mo:.2f}; all/other {ma/mo:.4f}")
print(f"BA+ share: Jewish {wm((d.degree[jew]>=3).astype(float),d.w[jew]):.2f} other {wm((d.degree[~jew]>=3).astype(float),d.w[~jew]):.2f}")
for k in [1.0,1.3,1.6]:
    # tax ~ income^k: benchmark change from dropping Jewish respondents
    tj=(mj/mo)**k; frac=sh*tj/(sh*tj+(1-sh)); print(f"tax elasticity {k}: Jewish share of white-3rd+ tax ≈ {frac:.1%}; benchmark falls by {(1-(1-frac)/(1-sh))*100:.1f}%")

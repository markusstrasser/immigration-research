"""Cross-sectional state regressions: guard labor / police spending on diversity measures."""
import json, pathlib, numpy as np, pandas as pd, statsmodels.api as sm
H = pathlib.Path(__file__).resolve().parent
p = pd.read_csv(H/"state_pums.csv", dtype={"state":str})
f = pd.read_csv(H/"state_finance.csv", dtype={"state":str})
c = pd.read_csv(H/"state_crime_2019.csv"); c["state_name"]=c["state_name"].str.replace(" Of "," of ")
def tab(fn, cols):
    d = json.loads((H/"_cache"/fn).read_text()); return pd.DataFrame(d[1:], columns=d[0])[cols]
a = tab("acs_controls.json", ["NAME","B19013_001E","B17001_002E","B17001_001E","state"])
u = tab("urban_2020.json", ["NAME","P2_001N","P2_002N","state"])
for col in ["B19013_001E","B17001_002E","B17001_001E"]: a[col]=a[col].astype(float)
for col in ["P2_001N","P2_002N"]: u[col]=u[col].astype(float)
a["log_medinc"]=np.log(a["B19013_001E"]); a["poverty"]=a["B17001_002E"]/a["B17001_001E"]*100
u["urban"]=u["P2_002N"]/u["P2_001N"]*100
d = (p.merge(f,on="state").merge(a[["state","NAME","log_medinc","poverty"]],on="state")
       .merge(u[["state","urban"]],on="state")
       .merge(c,left_on="NAME",right_on="state_name",how="left"))
d["police_pc"]=d["police_exp_k"]*1000/d["pop"]; d["corr_pc"]=d["corrections_exp_k"]*1000/d["pop"]
d["polcorr_pc"]=d["police_pc"]+d["corr_pc"]; d["crime"]=d["violent_crime_rate_2019"]
d["frac"]=d["frac"]*100
assert d["crime"].notna().all(), d.loc[d["crime"].isna(),"NAME"].tolist()
d.to_csv(H/"panel.csv", index=False)
print(f"n = {len(d)} states (incl. DC)\n")
CTRL = ["log_medinc","poverty","urban","black_share","crime"]
def run(y, x, ctrl):
    X = sm.add_constant(d[[x]+ctrl]); m = sm.OLS(d[y], X).fit()
    b, se, p_ = m.params[x], m.bse[x], m.pvalues[x]
    return f"{y:12} ~ {x:12} {'+ctrl' if ctrl else '     '}  b={b:9.4f}  se={se:8.4f}  t={b/se:6.2f}  p={p_:6.3f}  R2={m.rsquared:.3f}  n={int(m.nobs)}"
print("=== Guard-labor share of employment (%) and public spending ($/capita) ===")
print("ctrl set = log median HH income, poverty rate, urban share, Black share, 2019 violent crime rate\n")
for y in ["guard_share","police_share","police_pc","corr_pc","polcorr_pc"]:
    for x in ["fb_share","hisp_share","frac"]:
        print(run(y,x,[])); print(run(y,x,CTRL))
        print(run(y,x,[k for k in CTRL if k!="black_share"])+"   [no Black-share ctrl]")
    print()
print("=== descriptives ===")
print(d[["guard_share","police_share","police_pc","corr_pc","fb_share","hisp_share","black_share","frac","crime"]].describe().round(3).to_string())
print("\n=== simple correlations ===")
print(d[["guard_share","police_share","polcorr_pc","fb_share","hisp_share","frac","black_share","crime","urban","poverty"]].corr().round(3).to_string())

print("\n=== ROBUSTNESS: drop DC (guard_share and police_pc outlier) ===")
d = d[d["NAME"]!="District of Columbia"].reset_index(drop=True)
for y in ["guard_share","police_share","polcorr_pc"]:
    for x in ["fb_share","hisp_share","frac"]:
        print(run(y,x,[])); print(run(y,x,CTRL))

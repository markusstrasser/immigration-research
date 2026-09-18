import pandas as pd, numpy as np, sys
M=pd.read_csv("derived/gss_mode_check.csv"); D=pd.read_csv("derived/gss_mode_difference.csv")
def v(it,arm,g): 
    s=M[(M.item==it)&(M.arm==arm)&(M.group==g)]; return round(s.estimate.iloc[0]*100,1)
def d(it,g):
    s=D[(D.item==it)&(D.group==g)]; return round(s["diff"].iloc[0]*100,1), round(s.se_approx.iloc[0]*100,1)
bad=0
for it,g,wweb,wint,wd,wse in [("obey_top2","Hisp G1",8.2,27.7,-19.5,7.2),
                              ("cappun_favor","Hisp G1",-13.8,-34.8,21.0,8.6)]:
    for got,want,lbl in [(v(it,"web",g),wweb,"web"),(v(it,"interviewer",g),wint,"interviewer")]:
        if abs(got-want)>0.06: print(f"FAIL {it} {lbl}: {got} vs {want}"); bad+=1
    dd,ds=d(it,g)
    if abs(abs(dd)-abs(wd))>0.15 or abs(ds-wse)>0.15: print(f"FAIL {it} diff: {dd} ({ds}) vs {wd} ({wse})"); bad+=1
agree=sum(1 for _,r in D.iterrows() if abs(r.z)<2)
print(f"outcomes where the two mode arms agree within 2 approximate SE: {agree}/{len(D)}")
byitem=D.groupby("item").z.apply(lambda s: (s.abs()<2).all())
print(f"outcomes with NO arm disagreement at |z|>=2: {int(byitem.sum())}/{len(byitem)}")
print("n per arm:", M.groupby("arm").n.max().to_dict())
print("PASS" if bad==0 else f"{bad} FAILURES"); sys.exit(1 if bad else 0)

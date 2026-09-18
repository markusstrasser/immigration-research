import pandas as pd
pd.set_option("display.width",300); pd.set_option("display.max_rows",300)
R=pd.read_csv("derived/gss_raw_means.csv"); A=pd.read_csv("derived/gss_adjusted.csv")
G=["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+","NHWhite G3+","White G3+ liberal","White G3+ conservative","White G3+ no BA","White G3+ BA+"]
s=R[R.item.isin(["police_spread","con_within_sd"])&R.group.isin(G)].copy()
s["cell"]=s.apply(lambda r:f"{r['mean']:.3f} ({r.se:.3f}) n={r.n}",axis=1)
print("="*18,"INSTRUMENT CHECKS, raw"); print(s.pivot(index="item",columns="group",values="cell")[G].to_string())
ID=["amcit_very","ambornin_very","amenglsh_very","amgovt_very","amancstr_very","amchrstn_very","amfeel_very","amlived_very"]
ID2=["amcitizn_agree","amcult_agree","amshamed_agree","amownway_agree","ethnofit_agree","ethadapt_agree","immlimit_agree","immcult_agree","immassim_giveup","immassim_retain_only"]
def tab(items,model,cs,sc=1.,dc=2):
    t=A[(A.model==model)&A.item.isin(items)&A.contrast.isin(cs)].copy()
    t["cell"]=t.apply(lambda r:f"{r.estimate*sc:+.{dc}f} ({r.se*sc:.{dc}f})",axis=1)
    p=t.pivot(index="item",columns="contrast",values="cell")
    return p.reindex([i for i in items if i in p.index])[[c for c in cs if c in p.columns]]
H=["Hisp G1 vs white G3+","Hisp G2 vs white G3+","Hisp G3+ vs white G3+"]
C=["Hisp G1 vs white conservative","Hisp G3+ vs white conservative","white conservative vs white liberal"]
print("\n"+"="*18,"ADJUSTED — national identity, 'very important' shares (pp)")
print(pd.concat([tab(ID,"adj_hisp",H,100,1),tab(ID,"ideo_hisp",C,100,1)],axis=1).to_string())
print("\n"+"="*18,"ADJUSTED — pluralism / agreement items")
print(pd.concat([tab(ID2[:8],"adj_hisp",H,1,3),tab(ID2[:8],"ideo_hisp",C,1,3)],axis=1).to_string())
print(pd.concat([tab(ID2[8:],"adj_hisp",H,100,1),tab(ID2[8:],"ideo_hisp",C,100,1)],axis=1).to_string())
print("\n"+"="*18,"ADJUSTED — instrument checks")
print(pd.concat([tab(["police_spread","con_within_sd"],"adj_hisp",H,1,3),tab(["police_spread","con_within_sd"],"ideo_hisp",C,1,3)],axis=1).to_string())

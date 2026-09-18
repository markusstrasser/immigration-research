import pandas as pd, numpy as np
pd.set_option("display.width", 300); pd.set_option("display.max_rows", 500)
A = pd.read_csv("derived/gss_adjusted.csv")

def tab(items, model, contrasts, scale=1.0, dec=2):
    s = A[(A.model == model) & A.item.isin(items) & A.contrast.isin(contrasts)].copy()
    s["cell"] = s.apply(lambda r: f"{r.estimate*scale:+.{dec}f} ({r.se*scale:.{dec}f})", axis=1)
    p = s.pivot(index="item", columns="contrast", values="cell")
    return p.reindex([i for i in items if i in p.index])[[c for c in contrasts if c in p.columns]]

HG = ["Hisp G1 vs white G3+","Hisp G2 vs white G3+","Hisp G3+ vs white G3+"]
MG = ["Mex G1 vs white G3+","Mex G2 vs white G3+","Mex G3+ vs white G3+"]
CON=["confed","conlegis","conjudge","conarmy","conpress","consci","coneduc","conbus",
     "confinan","conclerg","conmedic","conlabor","contv"]
KEY = [f"{c}_great" for c in CON]+["con_index_gov3","con_index_all13"]
print("="*20,"ADJUSTED gap vs NH white G3+ — institutional confidence, 'great deal' (pp)")
print(pd.concat([tab(KEY[:-2],"adj_hisp",HG,100,1), tab(KEY[:-2],"adj_mex",MG,100,1)],axis=1).to_string())
print("\n index means (1-3 scale, not pp):")
print(pd.concat([tab(KEY[-2:],"adj_hisp",HG,1,3), tab(KEY[-2:],"adj_mex",MG,1,3)],axis=1).to_string())

TOL=["tolscale_classic15","tolscale_core9","tolscale_mslm3"]
TOLI=[f"tol_{v}" for v in ["spkath","spkrac","spkcom","spkmil","spkhomo","spkmslm",
      "colath","colrac","colcom","colmil","colhomo","colmslm",
      "libath","librac","libcom","libmil","libhomo","libmslm"]]
print("\n"+"="*20,"ADJUSTED — tolerance scales (scale points)")
print(pd.concat([tab(TOL,"adj_hisp",HG,1,3), tab(TOL,"adj_mex",MG,1,3)],axis=1).to_string())
print("\n tolerance items (pp):")
print(pd.concat([tab(TOLI,"adj_hisp",HG,100,1), tab(TOLI,"adj_mex",MG,100,1)],axis=1).to_string())

LAW=["obey_top2","obey_rank","courts_too_harsh","courts_not_harsh_enough","cappun_favor",
     "gunlaw_favor","grass_favor","polhitok_yes","polabuse_yes","polmurdr_yes",
     "polescap_yes","polattak_yes","police_force_index","welfare_toolittle"]
print("\n"+"="*20,"ADJUSTED — rule of law / policing (pp; obey_rank in scale points)")
print(pd.concat([tab(LAW,"adj_hisp",HG,100,1), tab(LAW,"adj_mex",MG,100,1)],axis=1).to_string())
GOV=["redist","helppoor_r","helpnot_r"]
print("\n role of government (scale points):")
print(pd.concat([tab(GOV,"adj_hisp",HG,1,3), tab(GOV,"adj_mex",MG,1,3)],axis=1).to_string())

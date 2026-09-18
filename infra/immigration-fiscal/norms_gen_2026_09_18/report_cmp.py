import pandas as pd, numpy as np
pd.set_option("display.width", 320); pd.set_option("display.max_rows", 500)
A = pd.read_csv("derived/gss_adjusted.csv")
def tab(items, model, contrasts, scale=1.0, dec=2, rename=None):
    s = A[(A.model==model) & A.item.isin(items) & A.contrast.isin(contrasts)].copy()
    s["cell"] = s.apply(lambda r: f"{r.estimate*scale:+.{dec}f} ({r.se*scale:.{dec}f})", axis=1)
    p = s.pivot(index="item", columns="contrast", values="cell")
    p = p.reindex([i for i in items if i in p.index])[[c for c in contrasts if c in p.columns]]
    if rename: p.columns = [rename.get(c,c) for c in p.columns]
    return p
HEAD=["con_index_gov3","con_index_all13","tolscale_classic15","tolscale_core9","tolscale_mslm3"]
SH=["confed_great","conlegis_great","conjudge_great","conarmy_great","tol_spkmslm","tol_colmslm","tol_libmslm",
    "obey_top2","cappun_favor","polhitok_yes","police_force_index","courts_too_harsh","welfare_toolittle"]
GOV=["redist","helppoor_r","helpnot_r"]
C1=["Hisp G1 vs white conservative","Hisp G2 vs white conservative","Hisp G3+ vs white conservative"]
C2=["Hisp G1 vs white liberal","Hisp G2 vs white liberal","Hisp G3+ vs white liberal"]
CW=["white conservative vs white moderate","white liberal vs white moderate","white conservative vs white liberal"]
E1=["Hisp G1 vs white no BA","Hisp G2 vs white no BA","Hisp G3+ vs white no BA","white BA+ vs white no BA"]
rn={c:c.replace("Hisp ","").replace(" vs white conservative"," v wCons").replace(" vs white liberal"," v wLib").replace(" vs white no BA"," v w-noBA") for c in C1+C2+E1}
rn.update({"white conservative vs white moderate":"wCons v wMod","white liberal vs white moderate":"wLib v wMod","white conservative vs white liberal":"wCons v wLib","white BA+ vs white no BA":"wBA v w-noBA"})
for title, items, sc, dc in [("scales/indices (scale points)", HEAD, 1, 3),
                             ("shares (pp)", SH, 100, 1),
                             ("role of government (scale points)", GOV, 1, 3)]:
    print("="*18, "ADJUSTED — Hispanic generations vs WHITE IDEOLOGY subgroups —", title)
    print(pd.concat([tab(items,"ideo_hisp",C1,sc,dc,rn), tab(items,"ideo_hisp",C2,sc,dc,rn),
                     tab(items,"ideo_hisp",CW,sc,dc,rn)], axis=1).to_string()); print()
for title, items, sc, dc in [("scales/indices", HEAD, 1, 3), ("shares (pp)", SH, 100, 1),
                             ("role of government", GOV, 1, 3)]:
    print("="*18, "ADJUSTED — Hispanic generations vs WHITE EDUCATION subgroups —", title)
    print(tab(items,"educ_hisp",E1,sc,dc,rn).to_string()); print()

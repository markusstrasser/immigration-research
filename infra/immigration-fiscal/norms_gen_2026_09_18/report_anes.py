import pandas as pd
pd.set_option("display.width",320); pd.set_option("display.max_rows",300); pd.set_option("display.max_colwidth",60)
R=pd.read_csv("derived/anes_raw_means.csv"); A=pd.read_csv("derived/anes_adjusted.csv")
G=["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+","NHWhite G3+","White G3+ liberal","White G3+ conservative","White G3+ no BA","White G3+ BA+"]
IT=["strpres_helpful","strleader_agree","prefer_democracy","courts_authority","people_decide",
    "votes_counted_fairly","violence_justified","satisfied_democracy","trust_govt",
    "trust_election_officials","minorities_adapt","born_here_important",
    "auth_obedience","auth_respect","auth_manners","auth_behaved","auth_scale4"]
s=R[R.group.isin(G)].copy(); s["cell"]=s.apply(lambda r:f"{r['mean']*100:.1f} ({r.se*100:.1f}) n={r.n}" if r.item!="auth_scale4" else f"{r['mean']:.2f} ({r.se:.2f}) n={r.n}",axis=1)
print("="*18,"ANES RAW (shares x100; auth_scale4 in 0-4 points)")
print(s.pivot(index="item",columns="group",values="cell").reindex([i for i in IT if i in set(s.item)])[G].to_string())
print("\nyears per item:"); print(R.drop_duplicates("item")[["item","years","label"]].to_string(index=False))
def tab(model,cs,sc=100,dc=1):
    t=A[(A.model==model)&A.contrast.isin(cs)].copy()
    t["cell"]=t.apply(lambda r:f"{r.estimate*sc:+.{dc}f} ({r.se*sc:.{dc}f})",axis=1)
    p=t.pivot(index="item",columns="contrast",values="cell")
    return p.reindex([i for i in IT if i in p.index])[[c for c in cs if c in p.columns]]
print("\n"+"="*18,"ANES ADJUSTED vs NH white G3+ (pp; age, educ, income, year)")
print(pd.concat([tab("adj_hisp",["Hisp G1 vs white G3+","Hisp G2 vs white G3+","Hisp G3+ vs white G3+"]),
                 tab("adj_mex",["Mex G1 vs white G3+","Mex G2 vs white G3+","Mex G3+ vs white G3+"])],axis=1).to_string())
print("\n"+"="*18,"ANES ADJUSTED vs white ideology / education subgroups (pp)")
print(pd.concat([tab("ideo_hisp",["Hisp G1 vs white conservative","Hisp G3+ vs white conservative","Hisp G1 vs white liberal","Hisp G3+ vs white liberal","white conservative vs white liberal"]),
                 tab("educ_hisp",["Hisp G3+ vs white no BA","white BA+ vs white no BA"])],axis=1).to_string())

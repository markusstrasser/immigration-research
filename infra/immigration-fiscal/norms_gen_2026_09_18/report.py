import pandas as pd, numpy as np
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 400)
R = pd.read_csv("derived/gss_raw_means.csv"); A = pd.read_csv("derived/gss_adjusted.csv")

def piv(items, groups, scale=1.0, dec=3):
    s = R[R.item.isin(items) & R.group.isin(groups)].copy()
    s["cell"] = s.apply(lambda r: f"{r['mean']*scale:.{dec}f} ({r.se*scale:.{dec}f}) n={r.n}", axis=1)
    return s.pivot(index="item", columns="group", values="cell").reindex(items)[groups]

G = ["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+","NHWhite G3+",
     "White G3+ liberal","White G3+ conservative","White G3+ no BA","White G3+ BA+"]
CON = ["confed","conlegis","conjudge","conarmy","conpress","consci","coneduc","conbus",
       "confinan","conclerg","conmedic","conlabor","contv"]
print("="*30, "RAW: share 'a great deal' of confidence (x100)")
print(piv([f"{c}_great" for c in CON]+["con_index_gov3","con_index_all13"], G, 100, 1).to_string())
print()
print("="*30, "RAW: tolerance scales and key items")
print(piv(["tolscale_classic15","tolscale_core9","tolscale_mslm3"], G, 1, 2).to_string())
print(piv([f"tol_{v}" for v in ["spkath","spkrac","spkcom","spkmil","spkhomo","spkmslm",
       "colath","colrac","colhomo","colmslm","libath","librac","libhomo","libmslm"]], G, 100, 1).to_string())

print()
print("="*30, "RAW: rule of law, policing, role of government (x100 for shares)")
print(piv(["obey_top2","courts_too_harsh","courts_not_harsh_enough","cappun_favor",
           "gunlaw_favor","grass_favor","polhitok_yes","polabuse_yes","polmurdr_yes",
           "polescap_yes","polattak_yes","police_force_index","welfare_toolittle"], G, 100, 1).to_string())
print(piv(["obey_rank","redist","helppoor_r","helpnot_r"], G, 1, 2).to_string())
print()
print("="*30, "RAW: national identity / pluralism (ISSP modules; thin cells)")
print(piv(["amcit_very","ambornin_very","amenglsh_very","amgovt_very","amancstr_very",
           "amchrstn_very","amfeel_very","amlived_very"], G, 100, 1).to_string())
print(piv(["amcitizn_agree","amcult_agree","amshamed_agree","amownway_agree",
           "ethnofit_agree","ethadapt_agree","immlimit_agree","immcult_agree"], G, 1, 2).to_string())
print(piv(["immassim_giveup","immassim_retain_only"], G, 100, 1).to_string())

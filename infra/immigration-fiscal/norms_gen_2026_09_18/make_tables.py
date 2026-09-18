"""Emit the memo's markdown tables straight from the derived CSVs."""
import pandas as pd, numpy as np, io
R=pd.read_csv("derived/gss_raw_means.csv"); A=pd.read_csv("derived/gss_adjusted.csv")
AR=pd.read_csv("derived/anes_raw_means.csv"); AA=pd.read_csv("derived/anes_adjusted.csv")
out=io.StringIO()
def w(s=""): out.write(s+"\n")

def raw_table(df, items, groups, names, scale, dec, label_col=None):
    w("| Item | " + " | ".join(names) + " |")
    w("|---|" + "---:|"*len(groups))
    for it in items:
        row=[]
        for g in groups:
            s=df[(df.item==it)&(df.group==g)]
            row.append(f"{s['mean'].iloc[0]*scale:.{dec}f} ({s.se.iloc[0]*scale:.{dec}f}) {int(s.n.iloc[0])}" if len(s) else "—")
        w(f"| {LAB.get(it,it)} | " + " | ".join(row) + " |")

def adj_table(df, items, pairs, scale, dec):
    w("| Item | " + " | ".join(n for _,_,n in pairs) + " |")
    w("|---|" + "---:|"*len(pairs))
    for it in items:
        row=[]
        for m,c,_ in pairs:
            s=df[(df.item==it)&(df.model==m)&(df.contrast==c)]
            row.append(f"{s.estimate.iloc[0]*scale:+.{dec}f} ({s.se.iloc[0]*scale:.{dec}f})" if len(s) else "—")
        w(f"| {LAB.get(it,it)} | " + " | ".join(row) + " |")

LAB = {
 "confed_great":"Executive branch of the federal government","conlegis_great":"Congress",
 "conjudge_great":"US Supreme Court","conarmy_great":"The military","conpress_great":"The press",
 "consci_great":"The scientific community","coneduc_great":"Education","conbus_great":"Major companies",
 "confinan_great":"Banks and financial institutions","conclerg_great":"Organised religion",
 "conmedic_great":"Medicine","conlabor_great":"Organised labour","contv_great":"Television",
 "confed_mean":"Executive branch of the federal government", "conlegis_mean":"Congress", "conjudge_mean":"US Supreme Court", "conarmy_mean":"The military", "conpress_mean":"The press", "consci_mean":"The scientific community", "coneduc_mean":"Education", "conbus_mean":"Major companies", "confinan_mean":"Banks and financial institutions", "conclerg_mean":"Organised religion", "conmedic_mean":"Medicine", "conlabor_mean":"Organised labour", "contv_mean":"Television",
 "con_index_gov3":"Index: executive + Congress + Supreme Court (1-3)",
 "con_index_all13":"Index: all 13 institutions (1-3)",
 "tolscale_classic15":"Stouffer 15-item tolerance scale (0-15)",
 "tolscale_core9":"9-item core scale, atheist/racist/communist (0-9)",
 "tolscale_mslm3":"3-item scale, anti-American Muslim clergyman (0-3)",
 "tol_spkath":"Let an anti-religionist speak","tol_spkrac":"Let a racist speak",
 "tol_spkcom":"Let a communist speak","tol_spkmil":"Let a militarist speak",
 "tol_spkhomo":"Let a homosexual speak","tol_spkmslm":"Let an anti-American Muslim clergyman speak",
 "tol_colath":"Let an anti-religionist teach","tol_colrac":"Let a racist teach",
 "tol_colmslm":"Let an anti-American Muslim clergyman teach",
 "tol_libath":"Keep an anti-religious book","tol_librac":"Keep a racist book",
 "tol_libmslm":"Keep an anti-American Muslim clergyman's book",
 "obey_top2":"Obedience ranked 1st or 2nd child quality","obey_rank":"Obedience rank, reversed (1-5)",
 "courts_too_harsh":"Courts deal with criminals too harshly",
 "courts_not_harsh_enough":"Courts not harsh enough","cappun_favor":"Favours the death penalty",
 "gunlaw_favor":"Favours police permits to buy a gun","grass_favor":"Marijuana should be legal",
 "polhitok_yes":"Ever approves police striking a citizen","polabuse_yes":"…after vulgar language",
 "polmurdr_yes":"…questioning a murder suspect","polescap_yes":"…a citizen escaping custody",
 "polattak_yes":"…a citizen attacking the officer",
 "police_force_index":"Share of 4 police-force scenarios approved",
 "police_spread":"INSTRUMENT: attacker minus vulgar-language approval",
 "con_within_sd":"INSTRUMENT: within-person SD over 13 confidence items",
 "redist":"Government should reduce income differences (1-7)",
 "helppoor_r":"Government should improve living standards (1-5)",
 "helpnot_r":"Government should do more (1-5)","welfare_toolittle":"Welfare spending too little",
 "amcit_very":"Having American citizenship","ambornin_very":"Having been born in America",
 "amenglsh_very":"Being able to speak English","amgovt_very":"Respecting America's laws and institutions",
 "amancstr_very":"Having American ancestry","amchrstn_very":"Being a Christian",
 "amfeel_very":"Feeling American","amlived_very":"Having lived in America most of one's life",
 "amcitizn_agree":"Would rather be a citizen of America than anywhere else (1-5)",
 "amcult_agree":"Impossible for those not sharing customs to become fully American (1-5)",
 "amshamed_agree":"There are things about America that make me ashamed (1-5)",
 "amownway_agree":"America should follow its own interests (1-5)",
 "ethnofit_agree":"Ethnic minorities never fit into the American mainstream (1-5)",
 "ethadapt_agree":"Minorities must adapt to American culture (1-5)",
 "immlimit_agree":"America should limit immigration to protect its way of life (1-5)",
 "immcult_agree":"Immigrants undermine American culture (1-4)",
 "immassim_giveup":"Immigrants should give up their culture of origin",
 "immassim_retain_only":"Immigrants should retain it and not adopt American culture",
 "strpres_helpful":"President acting without Congress and the courts would be helpful",
 "strleader_agree":"A strong leader is good even if the leader bends the rules",
 "prefer_democracy":"Democracy is preferable to any other kind of government (2024)",
 "courts_authority":"Courts should stop the government exceeding its authority (2024)",
 "people_decide":"The people, not politicians, should make policy (2020)",
 "votes_counted_fairly":"Votes are counted fairly all or most of the time",
 "violence_justified":"Political violence at least a little justified",
 "satisfied_democracy":"Satisfied with the way democracy works in the US",
 "trust_govt":"Trusts the federal government always or most of the time",
 "trust_election_officials":"Trusts election officials a great deal or a lot",
 "auth_obedience":"Obedience over self-reliance","auth_respect":"Respect for elders over independence",
 "auth_manners":"Good manners over curiosity","auth_behaved":"Well behaved over being considerate",
 "auth_scale4":"Authoritarian child-rearing scale (0-4)",
 "minorities_adapt":"Minorities should adapt to US customs (2020)",
 "born_here_important":"Being born in the US matters for being American",
}
GR=["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+","NHWhite G3+",
    "White G3+ liberal","White G3+ conservative","White G3+ no BA","White G3+ BA+"]
GN=["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+","White G3+","W lib","W cons","W no BA","W BA+"]
HG=[("adj_hisp","Hisp G1 vs white G3+","H G1"),("adj_hisp","Hisp G2 vs white G3+","H G2"),
    ("adj_hisp","Hisp G3+ vs white G3+","H G3+"),("adj_hisp","Hisp G3+ minus Hisp G1","H G3+ − G1"),
    ("adj_mex","Mex G1 vs white G3+","M G1"),("adj_mex","Mex G2 vs white G3+","M G2"),
    ("adj_mex","Mex G3+ vs white G3+","M G3+")]
CMP=[("ideo_hisp","Hisp G1 vs white conservative","H G1 vs W cons"),
     ("ideo_hisp","Hisp G3+ vs white conservative","H G3+ vs W cons"),
     ("ideo_hisp","Hisp G3+ vs white liberal","H G3+ vs W lib"),
     ("educ_hisp","Hisp G3+ vs white no BA","H G3+ vs W no BA"),
     ("ideo_hisp","white conservative vs white liberal","W cons − W lib"),
     ("educ_hisp","white BA+ vs white no BA","W BA+ − W no BA")]

CON=["confed_great","conlegis_great","conjudge_great","conarmy_great","conpress_great","consci_great",
     "coneduc_great","conbus_great","confinan_great","conclerg_great","conmedic_great","conlabor_great","contv_great"]
S=[("### A1 raw. Share saying 'a great deal' of confidence, percent (design SE, unweighted n)",
    lambda: raw_table(R,CON,GR,GN,100,1)),
   ("### A1 raw. Confidence indices, 1-3 scale where 3 is a great deal",
    lambda: raw_table(R,["con_index_gov3","con_index_all13"],GR,GN,1,3)),
   ("### A1 raw. Three-point confidence means, 3 = a great deal and 1 = hardly any",
    lambda: raw_table(R,[c.replace("_great","_mean") for c in CON],GR,GN,1,2)),
   ("### A1 adjusted. Three-point confidence means, scale points",
    lambda: adj_table(A,[c.replace("_great","_mean") for c in CON],HG,1,3)),
   ("### A1 adjusted. Gap in the 'great deal' share, percentage points",
    lambda: adj_table(A,CON,HG,100,1)),
   ("### A1 adjusted. Confidence indices, scale points",
    lambda: adj_table(A,["con_index_gov3","con_index_all13"],HG,1,3)),
   ("### A1 adjusted. Where the Hispanic generations sit against white subgroups",
    lambda: adj_table(A,["con_index_gov3","con_index_all13","confed_great","conlegis_great","conjudge_great","conarmy_great"],CMP,100,1)),
   ("### A2 raw. Tolerance scales",
    lambda: raw_table(R,["tolscale_classic15","tolscale_core9","tolscale_mslm3"],GR,GN,1,2)),
   ("### A2 raw. Tolerant-answer share, percent",
    lambda: raw_table(R,["tol_spkath","tol_spkrac","tol_spkcom","tol_spkmil","tol_spkhomo","tol_spkmslm","tol_colath","tol_colrac","tol_colmslm","tol_libath","tol_librac","tol_libmslm"],GR,GN,100,1)),
   ("### A2 adjusted. Tolerance scales, scale points",
    lambda: adj_table(A,["tolscale_classic15","tolscale_core9","tolscale_mslm3"],HG,1,3)),
   ("### A2 adjusted. Tolerance against white subgroups, scale points",
    lambda: adj_table(A,["tolscale_classic15","tolscale_core9","tolscale_mslm3"],CMP,1,3)),
   ("### A3 raw. Rule of law, policing and civic values",
    lambda: raw_table(R,["obey_top2","courts_too_harsh","courts_not_harsh_enough","cappun_favor","gunlaw_favor","grass_favor","polhitok_yes","polabuse_yes","polmurdr_yes","polescap_yes","polattak_yes","police_force_index"],GR,GN,100,1)),
   ("### A3 adjusted. Rule of law and policing, percentage points",
    lambda: adj_table(A,["obey_top2","courts_too_harsh","courts_not_harsh_enough","cappun_favor","gunlaw_favor","grass_favor","polhitok_yes","polescap_yes","polattak_yes","police_force_index"],HG,100,1)),
   ("### A3 adjusted. Against white subgroups, percentage points",
    lambda: adj_table(A,["obey_top2","cappun_favor","gunlaw_favor","polhitok_yes","police_force_index","courts_too_harsh"],CMP,100,1)),
   ("### A4 raw and adjusted. Role of government",
    lambda: (raw_table(R,["redist","helppoor_r","helpnot_r"],GR,GN,1,2), w(),
             adj_table(A,["redist","helppoor_r","helpnot_r","welfare_toolittle"],HG,1,3), w(),
             adj_table(A,["redist","helppoor_r","helpnot_r"],CMP,1,3))),
   ("### A5 raw. National identity, share saying 'very important' to being truly American, percent",
    lambda: raw_table(R,["amcit_very","ambornin_very","amenglsh_very","amgovt_very","amancstr_very","amchrstn_very","amfeel_very","amlived_very"],GR,GN,100,1)),
   ("### A5 raw. Pluralism items, agreement means",
    lambda: raw_table(R,["amcitizn_agree","amcult_agree","amshamed_agree","amownway_agree","ethnofit_agree","ethadapt_agree","immlimit_agree","immcult_agree"],GR,GN,1,2)),
   ("### A5 adjusted. National identity and pluralism",
    lambda: (adj_table(A,["amcit_very","ambornin_very","amenglsh_very","amgovt_very","amancstr_very","amchrstn_very","amfeel_very","amlived_very"],HG,100,1), w(),
             adj_table(A,["amcitizn_agree","amcult_agree","amshamed_agree","amownway_agree","ethnofit_agree","ethadapt_agree","immlimit_agree","immcult_agree"],HG,1,3))),
   ("### A6. Instrument checks, raw then adjusted",
    lambda: (raw_table(R,["police_spread","con_within_sd"],GR,GN,1,3), w(),
             adj_table(A,["police_spread","con_within_sd"],HG,1,3))),
]
ANI=["strpres_helpful","strleader_agree","prefer_democracy","courts_authority","people_decide",
     "votes_counted_fairly","violence_justified","satisfied_democracy","trust_govt",
     "trust_election_officials","minorities_adapt","born_here_important",
     "auth_obedience","auth_respect","auth_manners","auth_behaved"]
HGA=[(m,c.replace("g_","g"),n) for m,c,n in HG]
S += [("### B raw. ANES 2020 + 2024 pooled, percent",
       lambda: (raw_table(AR,ANI,GR,GN,100,1), w(), raw_table(AR,["auth_scale4"],GR,GN,1,2))),
      ("### B adjusted. Gap versus non-Hispanic white third-plus generation, percentage points",
       lambda: (adj_table(AA,ANI,HGA,100,1), w(), adj_table(AA,["auth_scale4"],HGA,1,3))),
      ("### B adjusted. Against white subgroups",
       lambda: (adj_table(AA,ANI,CMP,100,1), w(), adj_table(AA,["auth_scale4"],CMP,1,3)))]
for title, fn in S:
    w(title); w(); fn(); w()
open("derived/tables.md","w").write(out.getvalue())
print(out.getvalue()[:1500]); print("... wrote derived/tables.md", len(out.getvalue()), "chars")

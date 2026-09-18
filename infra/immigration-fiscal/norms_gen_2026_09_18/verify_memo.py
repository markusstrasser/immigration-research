"""Check every number asserted in memo_prose.md against the derived CSVs."""
import pandas as pd, numpy as np, sys
R=pd.read_csv("derived/gss_raw_means.csv"); A=pd.read_csv("derived/gss_adjusted.csv")
AR=pd.read_csv("derived/anes_raw_means.csv"); AA=pd.read_csv("derived/anes_adjusted.csv")
def raw(df,it,g,f=1): 
    s=df[(df.item==it)&(df.group==g)]; return (s['mean'].iloc[0]*f, s.se.iloc[0]*f, int(s.n.iloc[0])) if len(s) else None
def adj(df,it,m,c,f=1):
    s=df[(df.item==it)&(df.model==m)&(df.contrast==c)]; return (s.estimate.iloc[0]*f, s.se.iloc[0]*f) if len(s) else None
CH=[]
def chk(label, got, want, tol=0.06):
    ok = got is not None and abs(got-want)<=tol
    CH.append((ok,label,got,want))
C=[("con_index_all13 G3+ est",adj(A,"con_index_all13","adj_hisp","Hisp G3+ vs white G3+")[0],0.001,0.0006),
   ("con_index_all13 G3+ se",adj(A,"con_index_all13","adj_hisp","Hisp G3+ vs white G3+")[1],0.018,0.0006),
   ("con_index_gov3 G1",adj(A,"con_index_gov3","adj_hisp","Hisp G1 vs white G3+")[0],0.287,0.0006),
   ("con_index_gov3 G3+",adj(A,"con_index_gov3","adj_hisp","Hisp G3+ vs white G3+")[0],0.040,0.0006),
   ("con13 G3+-G1",adj(A,"con_index_all13","adj_hisp","Hisp G3+ minus Hisp G1")[0],-0.119,0.0006),
   ("gov3 G3+-G1",adj(A,"con_index_gov3","adj_hisp","Hisp G3+ minus Hisp G1")[0],-0.248,0.0006),
   ("conarmy G3+ pp",adj(A,"conarmy_great","adj_hisp","Hisp G3+ vs white G3+",100)[0],-8.6),
   ("con13 wcons-wlib",adj(A,"con_index_all13","ideo_hisp","white conservative vs white liberal")[0],-0.038,0.0006),
   ("con13 G1 vs wlib",adj(A,"con_index_all13","ideo_hisp","Hisp G1 vs white liberal")[0],0.109,0.0006),
   ("conarmy wcons-wlib pp",adj(A,"conarmy_great","ideo_hisp","white conservative vs white liberal",100)[0],19.2),
   ("conarmy G3+ vs wlib pp",adj(A,"conarmy_great","ideo_hisp","Hisp G3+ vs white liberal",100)[0],3.2),
   ("tol15 G1",adj(A,"tolscale_classic15","adj_hisp","Hisp G1 vs white G3+")[0],-1.583,0.001),
   ("tol15 G3+",adj(A,"tolscale_classic15","adj_hisp","Hisp G3+ vs white G3+")[0],-0.424,0.001),
   ("tol15 G3+-G1",adj(A,"tolscale_classic15","adj_hisp","Hisp G3+ minus Hisp G1")[0],1.159,0.001),
   ("tol15 vs wcons",adj(A,"tolscale_classic15","ideo_hisp","Hisp G3+ vs white conservative")[0],-0.034,0.001),
   ("tol15 vs wnoBA",adj(A,"tolscale_classic15","educ_hisp","Hisp G3+ vs white no BA")[0],-0.281,0.001),
   ("tol15 wBA-wnoBA",adj(A,"tolscale_classic15","educ_hisp","white BA+ vs white no BA")[0],1.634,0.001),
   ("tol15 wcons-wlib",adj(A,"tolscale_classic15","ideo_hisp","white conservative vs white liberal")[0],-0.984,0.001),
   ("spkrac raw HG1",raw(R,"tol_spkrac","Hisp G1",100)[0],34.4),("spkrac raw white",raw(R,"tol_spkrac","NHWhite G3+",100)[0],63.1),
   ("spkmslm raw HG1",raw(R,"tol_spkmslm","Hisp G1",100)[0],16.1),("spkmslm raw white",raw(R,"tol_spkmslm","NHWhite G3+",100)[0],48.9),
   ("mslm3 vs wcons",adj(A,"tolscale_mslm3","ideo_hisp","Hisp G3+ vs white conservative")[0],-0.042,0.001),
   ("mslm3 vs wlib",adj(A,"tolscale_mslm3","ideo_hisp","Hisp G3+ vs white liberal")[0],-0.507,0.001),
   ("obey Mex G1 raw",raw(R,"obey_top2","Mex G1",100)[0],42.9),("obey white raw",raw(R,"obey_top2","NHWhite G3+",100)[0],18.8),
   ("obey wcons raw",raw(R,"obey_top2","White G3+ conservative",100)[0],23.4),
   ("obey adj G1 pp",adj(A,"obey_top2","adj_hisp","Hisp G1 vs white G3+",100)[0],16.1),
   ("obey adj G3+ vs wcons",adj(A,"obey_top2","ideo_hisp","Hisp G3+ vs white conservative",100)[0],-1.6),
   ("obey G3+-G1 pp",adj(A,"obey_top2","adj_hisp","Hisp G3+ minus Hisp G1",100)[0],-12.9),
   ("polhitok G3+ pp",adj(A,"polhitok_yes","adj_hisp","Hisp G3+ vs white G3+",100)[0],-11.4),
   ("polhitok G3+ vs wlib",adj(A,"polhitok_yes","ideo_hisp","Hisp G3+ vs white liberal",100)[0],-7.2),
   ("cappun raw HG1",raw(R,"cappun_favor","Hisp G1",100)[0],46.2),("cappun raw white",raw(R,"cappun_favor","NHWhite G3+",100)[0],71.8),
   ("cappun G3+ vs wlib",adj(A,"cappun_favor","ideo_hisp","Hisp G3+ vs white liberal",100)[0],18.1),
   ("redist G3+",adj(A,"redist","adj_hisp","Hisp G3+ vs white G3+")[0],0.459,0.001),
   ("redist G3+-G1",adj(A,"redist","adj_hisp","Hisp G3+ minus Hisp G1")[0],-0.144,0.001),
   ("redist wcons-wlib",adj(A,"redist","ideo_hisp","white conservative vs white liberal")[0],-2.179,0.001),
   ("redist G3+ vs wlib",adj(A,"redist","ideo_hisp","Hisp G3+ vs white liberal")[0],-0.682,0.001),
   ("spread white raw",raw(R,"police_spread","NHWhite G3+",100)[0],83.7),
   ("spread HG1 raw",raw(R,"police_spread","Hisp G1",100)[0],57.3),
   ("spread HG3 raw",raw(R,"police_spread","Hisp G3+",100)[0],77.6),
   ("withinSD HG1",raw(R,"con_within_sd","Hisp G1")[0],0.534,0.001),
   ("withinSD white",raw(R,"con_within_sd","NHWhite G3+")[0],0.596,0.001),
   ("withinSD G3+-G1 adj",adj(A,"con_within_sd","adj_hisp","Hisp G3+ minus Hisp G1")[0],0.038,0.001),
   ("amgovt raw HG1",raw(R,"amgovt_very","Hisp G1",100)[0],79.5),("amgovt raw white",raw(R,"amgovt_very","NHWhite G3+",100)[0],64.5),
   ("amgovt adj G1",adj(A,"amgovt_very","adj_hisp","Hisp G1 vs white G3+",100)[0],19.1),
   ("amenglsh raw HG1",raw(R,"amenglsh_very","Hisp G1",100)[0],86.4),
   ("ambornin raw HG2",raw(R,"ambornin_very","Hisp G2",100)[0],56.9),("ambornin raw white",raw(R,"ambornin_very","NHWhite G3+",100)[0],40.5),
   ("amcult adj G3+",adj(A,"amcult_agree","adj_hisp","Hisp G3+ vs white G3+")[0],-0.032,0.001),
   ("ethnofit adj G3+",adj(A,"ethnofit_agree","adj_hisp","Hisp G3+ vs white G3+")[0],-0.325,0.001),
   ("immassim white raw",raw(R,"immassim_giveup","NHWhite G3+",100)[0],5.6),
   ("ANES strpres G3+",adj(AA,"strpres_helpful","adj_hisp","Hisp G3+ vs white G3+",100)[0],4.0),
   ("ANES strpres vs wcons",adj(AA,"strpres_helpful","ideo_hisp","Hisp G3+ vs white conservative",100)[0],2.0),
   ("ANES strpres wcons-wlib",adj(AA,"strpres_helpful","ideo_hisp","white conservative vs white liberal",100)[0],7.5),
   ("ANES strleader vs wlib",adj(AA,"strleader_agree","ideo_hisp","Hisp G3+ vs white liberal",100)[0],20.7),
   ("ANES strleader wcons-wlib",adj(AA,"strleader_agree","ideo_hisp","white conservative vs white liberal",100)[0],29.0),
   ("ANES prefdem G3+",adj(AA,"prefer_democracy","adj_hisp","Hisp G3+ vs white G3+",100)[0],-3.0),
   ("ANES courts G3+",adj(AA,"courts_authority","adj_hisp","Hisp G3+ vs white G3+",100)[0],8.1),
   ("ANES trustgov G3+",adj(AA,"trust_govt","adj_hisp","Hisp G3+ vs white G3+",100)[0],6.5),
   ("ANES viol raw HG1",raw(AR,"violence_justified","Hisp G1",100)[0],30.3),
   ("ANES viol raw white",raw(AR,"violence_justified","NHWhite G3+",100)[0],12.0),
   ("ANES viol adj G3+",adj(AA,"violence_justified","adj_hisp","Hisp G3+ vs white G3+",100)[0],10.1),
   ("ANES viol vs wcons",adj(AA,"violence_justified","ideo_hisp","Hisp G3+ vs white conservative",100)[0],14.1),
   ("ANES viol wcons-wlib",adj(AA,"violence_justified","ideo_hisp","white conservative vs white liberal",100)[0],-8.3),
   ("ANES auth4 G3+",adj(AA,"auth_scale4","adj_hisp","Hisp G3+ vs white G3+")[0],0.160,0.001),
   ("ANES auth4 wcons-wlib",adj(AA,"auth_scale4","ideo_hisp","white conservative vs white liberal")[0],1.254,0.001),
   ("ANES viol G3+-G1 pp",adj(AA,"violence_justified","adj_hisp","Hisp G3+ minus Hisp G1",100)[0],-6.0),
  ]
for c in C: chk(c[0],c[1],c[2],c[3] if len(c)>3 else 0.06)
bad=[c for c in CH if not c[0]]
for ok,l,g,wv in CH:
    if not ok: print(f"  FAIL {l}: got {g} want {wv}")
print(f"{len(CH)-len(bad)}/{len(CH)} numeric claims verified")
# cell-size ranges quoted in the prose
for it_set,name in [(["amcit_very","ambornin_very","amenglsh_very","amgovt_very","amancstr_very","amchrstn_very","amfeel_very","amlived_very","amcitizn_agree","amcult_agree","amshamed_agree","amownway_agree","ethnofit_agree","ethadapt_agree","immlimit_agree","immcult_agree","immassim_giveup"],"ISSP identity")]:
    for g in ["Mex G1","Mex G2","Mex G3+"]:
        s=R[R.item.isin(it_set)&(R.group==g)].n
        print(f"  {name} {g}: n range {s.min()}-{s.max()}")
    for g in ["Hisp G1","Hisp G2","Hisp G3+"]:
        s=R[R.item.isin(it_set)&(R.group==g)].n
        print(f"  {name} {g}: n range {s.min()}-{s.max()}")
print("  tol/con Mexican cell range:",
      R[R.item.str.startswith(("con","tol"))&R.group.str.startswith("Mex")].n.min(),
      R[R.item.str.startswith(("con","tol"))&R.group.str.startswith("Mex")].n.max())
print("  educ spread / G3+ gap on tol15:",
      round(abs(adj(A,"tolscale_classic15","educ_hisp","white BA+ vs white no BA")[0])/abs(adj(A,"tolscale_classic15","adj_hisp","Hisp G3+ vs white G3+")[0]),2))
sys.exit(1 if bad else 0)

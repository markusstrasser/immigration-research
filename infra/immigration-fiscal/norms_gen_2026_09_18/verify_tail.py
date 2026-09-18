"""Second pass: the synthesis table and the language-check numbers in the memo tail."""
import pandas as pd, numpy as np, sys
A=pd.read_csv("derived/gss_adjusted.csv"); AA=pd.read_csv("derived/anes_adjusted.csv")
GL=pd.read_csv("derived/gss_language_check.csv"); AL=pd.read_csv("derived/anes_language_check.csv")
def a(df,it,m,c,f=1):
    s=df[(df.item==it)&(df.model==m)&(df.contrast==c)]
    return (round(s.estimate.iloc[0]*f,4), round(s.se.iloc[0]*f,4)) if len(s) else (None,None)
ROWS=[("tolscale_classic15",A,1,2,(-0.42,0.18),(-0.03,0.19),(-0.28,0.20),(-0.98,0.10)),
      ("tolscale_mslm3",A,1,2,(-0.17,0.07),(-0.04,0.07),(-0.07,0.07),(-0.46,0.04)),
      ("obey_top2",A,100,1,(3.2,1.8),(-1.6,1.9),(2.1,1.9),(11.5,1.0)),
      ("con_index_all13",A,1,2,(0.00,0.02),(0.03,0.02),(0.01,0.02),(-0.04,0.01)),
      ("cappun_favor",A,100,1,(-4.2,1.9),(-15.7,1.9),(-7.7,1.9),(33.7,1.1)),
      ("strpres_helpful",AA,100,1,(4.0,2.8),(2.0,3.0),(1.1,2.9),(7.5,1.3)),
      ("strleader_agree",AA,100,1,(3.6,3.2),(-8.3,3.4),(-0.9,3.2),(29.0,1.7)),
      ("prefer_democracy",AA,100,1,(-3.0,4.9),(-7.7,5.0),(-0.4,5.2),(-2.7,2.2)),
      ("auth_scale4",AA,1,2,(0.16,0.08),(-0.24,0.09),(-0.07,0.09),(1.25,0.05)),
      ("redist",A,1,2,(0.46,0.09),(1.50,0.09),(0.47,0.09),(-2.18,0.05)),
      ("violence_justified",AA,100,1,(10.1,2.6),(14.1,2.8),(9.6,2.7),(-8.3,1.4))]
CON=[("adj_hisp","Hisp G3+ vs white G3+"),("ideo_hisp","Hisp G3+ vs white conservative"),
     ("educ_hisp","Hisp G3+ vs white no BA"),("ideo_hisp","white conservative vs white liberal")]
bad=0
for it,df,f,dec,*want in ROWS:
    for (m,c),(we,ws) in zip(CON,want):
        e,s=a(df,it,m,c,f)
        ge,gs=(round(e,dec),round(s,dec)) if e is not None else (None,None)
        if ge!=round(we,dec) or gs!=round(ws,dec):
            print(f"  FAIL {it:22s} {c:36s} memo {we} ({ws})  csv {ge} ({gs})"); bad+=1
def lang(df,it,g,f=1):
    s=df[(df.item==it)&(df.group==g)]; return round(s['mean'].iloc[0]*f,3) if len(s) else None
L=[("gss tol15 Spanish",lang(GL,"tolscale_classic15","Hisp G1, Spanish interview"),9.318),
   ("gss tol15 English",lang(GL,"tolscale_classic15","Hisp G1, English interview"),7.570),
   ("gss obey Spanish",lang(GL,"obey_top2","Hisp G1, Spanish interview",100),33.5),
   ("gss obey English",lang(GL,"obey_top2","Hisp G1, English interview",100),52.3),
   ("gss redist Spanish",lang(GL,"redist","Hisp G1, Spanish interview"),4.691),
   ("gss redist English",lang(GL,"redist","Hisp G1, English interview"),5.296),
   ("anes obed Spanish",lang(AL,"auth_obedience","Hisp G1 Spanish",100),70.3),
   ("anes obed English",lang(AL,"auth_obedience","Hisp G1 English",100),48.2),
   ("anes prefdem Spanish",lang(AL,"prefer_democracy","Hisp G1 Spanish",100),51.3),
   ("anes prefdem English",lang(AL,"prefer_democracy","Hisp G1 English",100),76.6)]
for n,g,w in L:
    if g is None or abs(g-w)>0.06: print(f"  FAIL {n}: csv {g} memo {w}"); bad+=1
print("anes language cell n range:", AL.n.min(), "-", AL.n.max())
# "more confident in eleven of thirteen institutions"
CONS=["confed","conlegis","conjudge","conarmy","conpress","consci","coneduc","conbus",
      "confinan","conclerg","conmedic","conlabor","contv"]
pos=sum(1 for c in CONS if a(A,f"{c}_great","adj_hisp","Hisp G1 vs white G3+")[0]>0)
print(f"institutions where Hispanic G1 is adjusted-higher: {pos} of 13")
if pos!=11: print("  FAIL: memo says eleven of thirteen"); bad+=1
print("PASS" if bad==0 else f"{bad} FAILURES")
sys.exit(1 if bad else 0)

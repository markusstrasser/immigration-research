"""Mexican-origin version of the synthesis table: does the all-Hispanic verdict hold
for the Mexican-origin subgroup on its own?"""
import pandas as pd, numpy as np
A=pd.read_csv("derived/gss_adjusted.csv"); AA=pd.read_csv("derived/anes_adjusted.csv")
def g(df,it,m,c,f=1,dec=2):
    s=df[(df.item==it)&(df.model==m)&(df.contrast==c)]
    return f"{s.estimate.iloc[0]*f:+.{dec}f} ({s.se.iloc[0]*f:.{dec}f})" if len(s) else "—"
ROWS=[("Stouffer 15-item tolerance (scale pts)","tolscale_classic15",A,1,2),
      ("Anti-American Muslim clergyman, 3 items","tolscale_mslm3",A,1,2),
      ("Obedience as a top child quality (pp)","obey_top2",A,100,1),
      ("All-13 confidence index (scale pts)","con_index_all13",A,1,2),
      ("Death penalty (pp)","cappun_favor",A,100,1),
      ("Ever approves police striking a citizen (pp)","polhitok_yes",A,100,1),
      ("Government should reduce income differences (1-7)","redist",A,1,2),
      ("President without Congress or courts (pp)","strpres_helpful",AA,100,1),
      ("Strong leader who bends the rules (pp)","strleader_agree",AA,100,1),
      ("Democracy is preferable (2024, pp)","prefer_democracy",AA,100,1),
      ("Authoritarian child-rearing (0-4)","auth_scale4",AA,1,2),
      ("Political violence at least a little justified (pp)","violence_justified",AA,100,1)]
print("| Item | Mex G1 vs whites | Mex G2 | Mex G3+ | Mex G3+ vs white cons | vs white no BA | Mex G3+ − G1 |")
print("|---|---:|---:|---:|---:|---:|---:|")
for lab,it,df,f,dec in ROWS:
    cells=[g(df,it,"adj_mex",f"Mex {t} vs white G3+",f,dec) for t in ("G1","G2","G3+")]
    cells.append(g(df,it,"ideo_mex","Mex G3+ vs white conservative",f,dec))
    cells.append(g(df,it,"educ_mex","Mex G3+ vs white no BA",f,dec))
    cells.append(g(df,it,"adj_mex","Mex G3+ minus Mex G1",f,dec))
    print(f"| {lab} | " + " | ".join(cells) + " |")

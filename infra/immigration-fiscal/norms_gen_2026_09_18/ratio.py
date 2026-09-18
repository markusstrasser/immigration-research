"""How large is each Hispanic third-generation gap relative to the internal white
ideological spread on the same item? Ratio of |G3+ minus white G3+| (adjusted) to
|white conservative minus white liberal| (adjusted, same model family)."""
import pandas as pd, numpy as np
def build(adj, src):
    a = pd.read_csv(adj)
    g = a[(a.model.isin(["adj_hisp"])) & (a.contrast == "Hisp G3+ vs white G3+")].set_index("item")
    g1 = a[(a.model.isin(["adj_hisp"])) & (a.contrast == "Hisp G1 vs white G3+")].set_index("item")
    w = a[(a.model.isin(["ideo_hisp"])) & (a.contrast == "white conservative vs white liberal")].set_index("item")
    e = a[(a.model.isin(["educ_hisp"])) & (a.contrast == "white BA+ vs white no BA")].set_index("item")
    ix = g.index.intersection(w.index)
    out = pd.DataFrame(dict(source=src,
        g1_gap=g1.reindex(ix).estimate, g3_gap=g.reindex(ix).estimate, g3_se=g.reindex(ix).se,
        white_ideo_spread=w.reindex(ix).estimate.abs(), white_educ_spread=e.reindex(ix).estimate.abs()))
    out["g3_over_ideo"] = out.g3_gap.abs() / out.white_ideo_spread
    out["g3_over_educ"] = out.g3_gap.abs() / out.white_educ_spread
    out["converged"] = out.g3_gap.abs() / out.g1_gap.abs()
    return out
KEY = ["con_index_gov3","con_index_all13","confed_great","conlegis_great","conjudge_great",
       "conarmy_great","tolscale_classic15","tolscale_core9","tolscale_mslm3","obey_top2",
       "cappun_favor","polhitok_yes","police_force_index","courts_too_harsh","gunlaw_favor",
       "redist","helppoor_r","welfare_toolittle","amcit_very","amgovt_very","ambornin_very"]
A = build("derived/gss_adjusted.csv", "GSS")
B = build("derived/anes_adjusted.csv", "ANES")
T = pd.concat([A.reindex([k for k in KEY if k in A.index]), B])
T.to_csv("derived/gap_vs_white_spread.csv")
pd.set_option("display.width", 200)
print(T.round(3).to_string())

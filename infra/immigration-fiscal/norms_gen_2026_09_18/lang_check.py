"""Disconfirmation: does interview language move the first-generation results?
GSS SPANENG and ANES V201001/V241001 (language of interview)."""
import numpy as np, pandas as pd, pyreadstat, math
from norms_lib import *
from outcomes import build
from estimate import covariates, wls, contrast

extra = ["spaneng", "spanint", "spanself"]
d, meta = pyreadstat.read_dta(GSS, usecols=COLS + extra, encoding="latin1")
k = meta.variable_to_label.get("spaneng")
print("spaneng:", meta.column_names_to_labels.get("spaneng"),
      {kk: vv for kk, vv in (meta.value_labels[k].items() if k else [])
       if str(kk) not in set("dijmnprsuxyz")})
for c in d.columns: d[c] = pd.to_numeric(d[c], errors="coerce")
d = d[d.year >= 2006].reset_index(drop=True)  # GSS began Spanish interviewing in 2006
d["w"] = d.wtssnrps.fillna(d.wtssps)
d, lab = assign_groups(d); des = Design(d)
Y, L = build(d)
sp = d.spaneng.to_numpy()
print("\nspaneng distribution among Hispanic G1:", pd.Series(sp[lab["Hisp G1"]]).value_counts(dropna=False).to_dict())
KEY = ["tolscale_classic15","tolscale_core9","con_index_gov3","con_index_all13",
       "obey_top2","polhitok_yes","police_spread","con_within_sd","redist","cappun_favor"]
rows = []
for item in KEY:
    y = Y[item].to_numpy(float)
    for gname, mask in [("Hisp G1, Spanish interview", lab["Hisp G1"] & (sp == 1)),
                        ("Hisp G1, English interview", lab["Hisp G1"] & (sp == 2)),
                        ("Hisp G2 (all)", lab["Hisp G2"]),
                        ("NHWhite G3+", lab["NHWhite G3+"])]:
        m = mask & np.isfinite(y); w = d.w.to_numpy()
        if m.sum() < 15: continue
        est = float(w[m] @ y[m] / w[m].sum())
        infl = np.where(m, w * (np.nan_to_num(y) - est) / w[m].sum(), 0.0)
        se = math.sqrt(max(0, des.cov(infl[:, None])[0, 0]))
        rows.append(dict(item=item, group=gname, n=int(m.sum()), mean=est, se=se))
R = pd.DataFrame(rows); R.to_csv("derived/gss_language_check.csv", index=False)
R["cell"] = R.apply(lambda r: f"{r['mean']:.3f} ({r.se:.3f}) n={r.n}", axis=1)
pd.set_option("display.width", 200)
print("\nGSS, raw weighted means by interview language:")
print(R.pivot(index="item", columns="group", values="cell").reindex(KEY).to_string())

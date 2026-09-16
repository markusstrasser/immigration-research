"""Own-children-under-5 per woman 15-44, by Hispanic generation, CPS ASEC 2025."""
import zipfile, pandas as pd, numpy as np
Z = "/Users/alien/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip"
COLS = ["PH_SEQ","PPPOS","A_AGE","A_SEX","PRCITSHP","PENATVTY","PEFNTVTY","PEMNTVTY",
        "PEHSPNON","PRDTRACE","PRDTHSP","MARSUPWT","PEPAR1","PEPAR2","PEPAR1TYP","PEPAR2TYP"]
US = [57,60,66,69,73,78]
with zipfile.ZipFile(Z) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS)
d["w"] = d.MARSUPWT/100.0
# --- own children under 5 linked to mother ---
kids = d[d.A_AGE < 5]
links = []
for pcol, tcol in (("PEPAR1","PEPAR1TYP"),("PEPAR2","PEPAR2TYP")):
    k = kids[kids[pcol] > 0][["PH_SEQ",pcol]].copy()
    k["PPPOS"] = k[pcol] + 40  # PPPOS is line number + 40 in ASEC CSV
    k = k[["PH_SEQ","PPPOS"]]
    links.append(k)
link = pd.concat(links)
nkids = link.groupby(["PH_SEQ","PPPOS"]).size().rename("nkids_u5")
d = d.merge(nkids, on=["PH_SEQ","PPPOS"], how="left")
d["nkids_u5"] = d.nkids_u5.fillna(0)
# validate: kids' parents are mostly female-or-male adults
w = d[(d.A_SEX == 2) & d.A_AGE.between(15,44)].copy()
us_born = w.PENATVTY.isin(US)
par_us = w.PEFNTVTY.isin(US) & w.PEMNTVTY.isin(US)
par_mx = w.PEFNTVTY.eq(303) | w.PEMNTVTY.eq(303)
groups = {
 "Mexico-born women": w.PRCITSHP.isin([4,5]) & w.PENATVTY.eq(303),
 "Mexican 2nd gen (US-born, >=1 MX parent)": us_born & par_mx,
 "Mexican 3rd+ gen (US-born, US-born parents, Mexican self-ID)": us_born & par_us & w.PRDTHSP.eq(1),
 "All Hispanic (any gen)": w.PEHSPNON.eq(1),
 "NH white 3rd+ gen": us_born & par_us & w.PEHSPNON.eq(2) & w.PRDTRACE.eq(1),
}
rows=[]
for name, m in groups.items():
    s = w[m]
    mean = np.average(s.nkids_u5, weights=s.w)
    # jackknife-free SE via weighted variance
    var = np.average((s.nkids_u5-mean)**2, weights=s.w)
    se = np.sqrt(var/len(s))
    rows.append((name, len(s), round(float(s.w.sum())/1e6,2), round(float(mean),4), round(float(se),4)))
out = pd.DataFrame(rows, columns=["group","n_unweighted","pop_millions","own_kids_u5_per_woman_15_44","approx_se"])
print(out.to_string(index=False))
# TFR-ish scaling: children under 5 per woman 15-44 * (30/5) = implied births per woman over 30 repro years
out["implied_TFR_crude"] = (out.own_kids_u5_per_woman_15_44*6).round(2)
out.to_csv("/Users/alien/Projects/immigration-research/infra/immigration-fiscal/demo_momentum_2026_09_16/cps_fertility_proxy.csv", index=False)
print("\nlink diagnostics: kids u5 =", len(kids), " linked to >=1 parent =", link.PH_SEQ.nunique())
print("share of u5 kids with a parent pointer:", round((kids.PEPAR1>0).mean(),3))

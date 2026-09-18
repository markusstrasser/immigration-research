"""SF neighborhood maintenance quality: inspector-observed street/sidewalk audit
(DataSF qya8-uhsz, 7,318 randomly-sampled blockface evaluations Jan2022-Jun2025)
joined to ACS 2019-23 neighborhood composition, plus 311 complaint rates.

Tests: does Hispanic / Mexican population share predict worse observed
maintenance conditioning on income, tenure, density and land use?
"""
import json, pathlib, collections, re
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
pd.set_option("display.width", 260, "display.max_columns", 60)

# ---------- ACS by analysis neighborhood ----------
acs = pd.DataFrame(json.load(open(CD/"sf_nbhd_acs.json")))
acs = acs[acs["pop"] > 1000].copy()

# ---------- eval-group -> analysis neighborhoods ----------
ev = pd.DataFrame(json.load(open(CD/"sf_street_eval_2022_2025.json")))
groups = sorted(ev["analysis_neighborhoods"].dropna().unique())
def split_group(g):
    body = g.split(" - ", 1)[1]
    return [s.strip() for s in body.split(",")]
g2n = {g: split_group(g) for g in groups}
known = set(acs["nbhd"])
for g, ns in g2n.items():
    miss = [n for n in ns if n not in known]
    if miss: print("UNMATCHED neighborhood names:", g, miss)

# aggregate ACS to eval groups (population-weighted / sum where additive)
raw = {r["nbhd"]: r for r in json.load(open(CD/"sf_nbhd_acs.json"))}
grows = []
for g, ns in g2n.items():
    sub = [raw[n] for n in ns if n in raw]
    pop = sum(s["pop"] for s in sub); hh = sum(s["hh"] for s in sub)
    w = lambda k: sum((s[k] or 0)*s["pop"] for s in sub)/pop
    wh = lambda k: sum((s[k] or 0)*s["hh"] for s in sub)/hh
    grows.append(dict(group=g, pop=pop, hh=hh,
        mean_hh_inc=sum((s["mean_hh_inc"] or 0)*s["hh"] for s in sub)/hh,
        hisp_pct=w("hisp_pct"), mex_pct=w("mex_pct"), fb_pct=w("fb_pct"),
        nhwhite_pct=w("nhwhite_pct"), nhasian_pct=w("nhasian_pct"),
        nhblack_pct=w("nhblack_pct"), owner_pct=wh("owner_pct"),
        crowded_pct=wh("crowded_pct"), severe_crowded_pct=wh("severe_crowded_pct"),
        pov_pct=w("pov_pct"), hu=sum(s["hu"] for s in sub)))
G = pd.DataFrame(grows).set_index("group")

# ---------- outcomes ----------
num = lambda s: pd.to_numeric(ev[s], errors="coerce")
ev["street_litter"]   = num("select_the_statement_that")
ev["sidewalk_litter"] = num("select_the_statement_that_1")
ev["broken_glass"]    = num("select_the_statement_that_2")
ev["dumping_items"]   = num("how_many_large_abandoned").fillna(0)
ev["graffiti_priv"]   = num("how_many_instances_of_graffiti").fillna(0)
ev["graffiti_gov"]    = num("how_many_instances_of_graffiti_1").fillna(0)
ev["graffiti_other"]  = num("how_many_instances_of_graffiti_2").fillna(0)
ev["graffiti_tot"]    = ev.graffiti_priv + ev.graffiti_gov + ev.graffiti_other
ev["feces"]           = num("how_many_instances_of_feces").fillna(0)
ev["syringes"]        = num("how_many_abandoned_syringes").fillna(0)
ev["sw_defect_unmarked"] = num("does_the_sidewalk_have_any").fillna(0)
ev["pavement_sev"]    = num("how_severe_are_the_pavement").fillna(0)
ev["commercial"]      = (num("is_this_route_predominantly") == 1).astype(int)
ev["dumping_any"]     = (ev.dumping_items > 0).astype(int)
ev["litter_bad"]      = (ev.sidewalk_litter >= 4).astype(int)
ev["period"] = ev["evaluation_period"]

OUT = ["street_litter","sidewalk_litter","litter_bad","broken_glass","dumping_items",
       "dumping_any","graffiti_tot","graffiti_priv","feces","syringes",
       "sw_defect_unmarked","pavement_sev"]

d = ev.dropna(subset=["analysis_neighborhoods"]).join(G, on="analysis_neighborhoods")
d = d.dropna(subset=["mean_hh_inc"])
d["log_inc"]  = np.log(d.mean_hh_inc)
d["dens"]     = d["pop"]
print(f"routes analysed: {len(d)}  groups: {d.analysis_neighborhoods.nunique()}")

# ---------- Table 1: group means ----------
t1 = d.groupby("analysis_neighborhoods").agg(
    n=("street_litter","size"), commercial=("commercial","mean"),
    **{o:(o,"mean") for o in OUT})
t1 = t1.join(G[["mean_hh_inc","hisp_pct","mex_pct","nhwhite_pct","nhasian_pct",
                "fb_pct","crowded_pct","pov_pct","owner_pct"]])
t1 = t1.sort_values("sidewalk_litter", ascending=False)
print("\n=== TABLE 1. Inspector-observed conditions by SF evaluation group "
      "(Jan 2022 - Jun 2025 means) ===")
print(t1.round(2).to_string())
t1.round(3).to_csv(HERE/"table1_sf_street_eval_by_group.csv")

# ---------- Table 2: regressions ----------
print("\n=== TABLE 2. Route-level regressions, cluster-robust by evaluation group ===")
specs = {
 "raw":        "{y} ~ hisp_pct",
 "+income":    "{y} ~ hisp_pct + log_inc",
 "+landuse":   "{y} ~ hisp_pct + log_inc + commercial + C(period)",
 "full":       "{y} ~ hisp_pct + log_inc + commercial + C(period) + owner_pct + crowded_pct + nhblack_pct",
}
res = []
for y in OUT:
    for name, f in specs.items():
        m = smf.ols(f.format(y=y), data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d.analysis_neighborhoods})
        b = m.params.get("hisp_pct", np.nan); se = m.bse.get("hisp_pct", np.nan)
        res.append(dict(outcome=y, spec=name, beta_hisp_pct=b, se=se,
                        t=b/se if se else np.nan, p=m.pvalues.get("hisp_pct", np.nan),
                        sd_y=d[y].std(), n=int(m.nobs)))
R = pd.DataFrame(res)
R["beta_per_10pp_in_sd"] = 10*R.beta_hisp_pct/R.sd_y
print(R.round(4).to_string(index=False))
R.round(5).to_csv(HERE/"table2_sf_hisp_share_regressions.csv", index=False)

# same with Mexican share
res2 = []
for y in OUT:
    for name, f in specs.items():
        f2 = f.replace("hisp_pct", "mex_pct")
        m = smf.ols(f2.format(y=y), data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d.analysis_neighborhoods})
        b = m.params.get("mex_pct", np.nan); se = m.bse.get("mex_pct", np.nan)
        res2.append(dict(outcome=y, spec=name, beta_mex_pct=b, se=se,
                         t=b/se if se else np.nan, p=m.pvalues.get("mex_pct", np.nan),
                         sd_y=d[y].std()))
R2 = pd.DataFrame(res2); R2["beta_per_10pp_in_sd"] = 10*R2.beta_mex_pct/R2.sd_y
print("\n--- Mexican-origin share instead of all-Hispanic ---")
print(R2.round(4).to_string(index=False))
R2.round(5).to_csv(HERE/"table2b_sf_mex_share_regressions.csv", index=False)

# ---------- horse race: income vs each group share ----------
print("\n=== TABLE 3. Horse race, full spec, all composition shares together ===")
hr = []
for y in ["sidewalk_litter","street_litter","graffiti_tot","dumping_any","feces","broken_glass"]:
    m = smf.ols(f"{y} ~ hisp_pct + nhasian_pct + nhblack_pct + log_inc + commercial "
                f"+ C(period) + owner_pct + crowded_pct", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.analysis_neighborhoods})
    row = {"outcome": y, "n": int(m.nobs), "R2": m.rsquared}
    for k in ["hisp_pct","nhasian_pct","nhblack_pct","log_inc","commercial",
              "owner_pct","crowded_pct"]:
        row[k] = m.params[k]; row[k+"_t"] = m.params[k]/m.bse[k]
    hr.append(row)
H = pd.DataFrame(hr)
print(H.round(3).to_string(index=False))
H.round(5).to_csv(HERE/"table3_sf_horserace.csv", index=False)

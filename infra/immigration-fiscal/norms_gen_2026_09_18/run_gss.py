"""Part A. GSS 2000-2024 institutional confidence, civil liberties, rule of law,
role of government and national identity, by Hispanic / Mexican-origin generation
against non-Hispanic whites overall and white ideology / education subgroups."""
import numpy as np, pandas as pd, math, json, time
from norms_lib import *
from outcomes import build, FAMILY
from estimate import covariates, wls, contrast

t0 = time.time()
d = load(); d, lab = assign_groups(d); des = Design(d)
Y, LABELS = build(d)
print(f"rows {len(d)} | outcomes {Y.shape[1]} | strata {des.n_strata} psus {des.n_psu}", flush=True)

WHITE = lab["NHWhite G3+"]
HISP = lab["Hisp G1"] | lab["Hisp G2"] | lab["Hisp G3+"]
MEX = lab["Mex G1"] | lab["Mex G2"] | lab["Mex G3+"]
ideo_na = WHITE & ~(lab["White G3+ liberal"] | lab["White G3+ moderate"] | lab["White G3+ conservative"])
deg_na = WHITE & ~(lab["White G3+ no BA"] | lab["White G3+ BA+"])

Zf, Znf = covariates(d, use_educ=True, use_income=True)     # full controls
Zn_, Znn = covariates(d, use_educ=False, use_income=True)    # education is the splitter

SPECS = {}
for tag, gens, pool in [("hisp", ["Hisp G1", "Hisp G2", "Hisp G3+"], HISP),
                        ("mex", ["Mex G1", "Mex G2", "Mex G3+"], MEX)]:
    SPECS[f"adj_{tag}"] = dict(
        sample=WHITE | pool, Z=(Zf, Znf),
        dummies=[(g, lab[g]) for g in gens],
        contrasts={**{f"{g} vs white G3+": {g: 1.0} for g in gens},
                   **{f"{gens[b]} minus {gens[a]}": {gens[b]: 1.0, gens[a]: -1.0}
                      for a, b in [(0, 1), (0, 2), (1, 2)]}})
    SPECS[f"ideo_{tag}"] = dict(
        sample=WHITE | pool, Z=(Zf, Znf),
        dummies=[(g, lab[g]) for g in gens] +
                [("white liberal", lab["White G3+ liberal"]),
                 ("white conservative", lab["White G3+ conservative"]),
                 ("white ideology missing", ideo_na)],
        contrasts={**{f"{g} vs white moderate": {g: 1.0} for g in gens},
                   **{f"{g} vs white conservative": {g: 1.0, "white conservative": -1.0} for g in gens},
                   **{f"{g} vs white liberal": {g: 1.0, "white liberal": -1.0} for g in gens},
                   "white liberal vs white moderate": {"white liberal": 1.0},
                   "white conservative vs white moderate": {"white conservative": 1.0},
                   "white conservative vs white liberal": {"white conservative": 1.0, "white liberal": -1.0}})
    SPECS[f"educ_{tag}"] = dict(
        sample=WHITE | pool, Z=(Zn_, Znn),
        dummies=[(g, lab[g]) for g in gens] +
                [("white BA+", lab["White G3+ BA+"]), ("white degree missing", deg_na)],
        contrasts={**{f"{g} vs white no BA": {g: 1.0} for g in gens},
                   **{f"{g} vs white BA+": {g: 1.0, "white BA+": -1.0} for g in gens},
                   "white BA+ vs white no BA": {"white BA+": 1.0}})

raw_rows, adj_rows = [], []
for k, item in enumerate(Y.columns):
    y = Y[item].to_numpy(dtype=float)
    fam, labtxt = FAMILY.get(item, "other"), LABELS[item]
    # ---- raw weighted means, all groups, joint design covariance -----------
    infl, meta = [], []
    for g in GROUP_ORDER:
        m = lab[g] & np.isfinite(y)
        w = d.w.to_numpy()
        den = w[m].sum()
        if m.sum() < 5 or den <= 0:
            continue
        est = float(w[m] @ y[m] / den)
        infl.append(np.where(m, w * (np.nan_to_num(y) - est) / den, 0.0))
        meta.append((g, int(m.sum()), est))
    if not meta:
        continue
    C = des.cov(np.column_stack(infl))
    for j, (g, n, est) in enumerate(meta):
        raw_rows.append(dict(item=item, family=fam, label=labtxt, group=g, n=n,
                             mean=est, se=math.sqrt(max(0, C[j, j]))))
    # a few raw contrasts that the memo leans on
    pos = {g: j for j, (g, _, _) in enumerate(meta)}
    for a, b in [("Hisp G3+", "NHWhite G3+"), ("Mex G3+", "NHWhite G3+"),
                 ("Hisp G1", "NHWhite G3+"), ("Mex G1", "NHWhite G3+"),
                 ("Hisp G3+", "White G3+ conservative"), ("Hisp G3+", "White G3+ no BA"),
                 ("White G3+ conservative", "White G3+ liberal")]:
        if a in pos and b in pos:
            i, j = pos[a], pos[b]
            e = meta[i][2] - meta[j][2]
            v = C[i, i] + C[j, j] - 2 * C[i, j]
            adj_rows.append(dict(item=item, family=fam, label=labtxt, model="raw",
                                 contrast=f"{a} vs {b}", estimate=e,
                                 se=math.sqrt(max(0, v)), n=meta[i][1] + meta[j][1]))
    # ---- adjusted models --------------------------------------------------
    for mname, sp in SPECS.items():
        Z, Zn = sp["Z"]
        fit = wls(d, des, y, sp["sample"], sp["dummies"], Z, Zn)
        if fit is None:
            continue
        for cname, cspec in sp["contrasts"].items():
            r = contrast(fit, cspec)
            if r is None:
                continue
            adj_rows.append(dict(item=item, family=fam, label=labtxt, model=mname,
                                 contrast=cname, estimate=r[0], se=r[1], n=fit["n"]))
    if k % 20 == 0:
        print(f"  {k:3d}/{Y.shape[1]} {item} ({time.time()-t0:.0f}s)", flush=True)

R = pd.DataFrame(raw_rows); A = pd.DataFrame(adj_rows)
R.to_csv("derived/gss_raw_means.csv", index=False)
A.to_csv("derived/gss_adjusted.csv", index=False)
print(f"\nwrote derived/gss_raw_means.csv ({len(R)} rows), derived/gss_adjusted.csv ({len(A)} rows)")
print(f"elapsed {time.time()-t0:.0f}s")
json.dump(dict(rows=int(len(d)), strata=des.n_strata, psus=des.n_psu,
               years=[int(v) for v in sorted(d.year.unique())],
               weight="wtssnrps with wtssps fallback (2000, 2002)",
               variance="stratified with-replacement PSU linearisation, n_h/(n_h-1)",
               controls="age, age^2, education years, log constant-dollar family income "
                        "with a missing flag, survey-year fixed effects",
               generation="BORN x PARBORN, PARBORN 3/5/7 left unknown (ladder 110)",
               outcomes=int(Y.shape[1]), labels=LABELS),
          open("derived/gss_audit.json", "w"), indent=2)

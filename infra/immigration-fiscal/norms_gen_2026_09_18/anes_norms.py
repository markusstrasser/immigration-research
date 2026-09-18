"""Part B. ANES 2020 and 2024 democratic-norms items by Hispanic / Mexican-origin
generation, against non-Hispanic whites overall and white ideology / education
subgroups. Design-based variance on the ANES variance stratum and PSU."""
import numpy as np, pandas as pd, math, json, sys
sys.path.insert(0, ".")
from anes_spec import FILES, DESIGN, ITEMS, AUTH4
from norms_lib import Design
from estimate import covariates, wls, contrast

def load(year):
    s = DESIGN[year]
    need = sorted(set(s.values()) | {v[0] for it in ITEMS.values()
                                     for y, v in it["v"].items() if y == year})
    head = pd.read_csv(FILES[year], nrows=0).columns
    missing = [c for c in need if c not in head]
    use = [c for c in need if c in head]
    d = pd.read_csv(FILES[year], usecols=use, low_memory=False)
    for c in d.columns:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.rename(columns={v: k for k, v in s.items() if v in d.columns})
    d["year"] = year
    return d, missing

frames, miss = [], {}
for y in (2020, 2024):
    f, m = load(y); frames.append(f); miss[y] = m
    print(f"{y}: {len(f)} rows, missing columns {m}", flush=True)
D = pd.concat(frames, ignore_index=True)

# --- generation, prior-lane coding, plus a grandparent split of the third-plus ---
g = pd.Series(np.nan, index=D.index)
g[D.born.eq(4)] = 1                                     # born in another country
g[D.born.isin([1, 2, 3]) & D.par.isin([2, 3])] = 2      # US-born, >=1 foreign parent
g[D.born.isin([1, 2, 3]) & D.par.eq(1)] = 3             # US-born, both parents US-born
D["gen"] = g
D["hispanic"] = D.hisp.isin([1, 2, 3, 4])
D["mexican"] = D.hisp.eq(1)
D["nhwhite"] = D.race.eq(1)
lab = {}
for v, t in [(1, "G1"), (2, "G2"), (3, "G3+")]:
    lab[f"Hisp {t}"] = (D.hispanic & D.gen.eq(v)).to_numpy()
    lab[f"Mex {t}"] = (D.mexican & D.gen.eq(v)).to_numpy()
W3 = (D.nhwhite & D.gen.eq(3)).to_numpy()
lab["NHWhite G3+"] = W3
lab["White G3+ liberal"] = W3 & D.ideo.isin([1, 2, 3]).to_numpy()
lab["White G3+ moderate"] = W3 & D.ideo.eq(4).to_numpy()
lab["White G3+ conservative"] = W3 & D.ideo.isin([5, 6, 7]).to_numpy()
lab["White G3+ no BA"] = W3 & D.educ5.isin([1, 2, 3]).to_numpy()
lab["White G3+ BA+"] = W3 & D.educ5.isin([4, 5]).to_numpy()
# third generation proper (>=1 foreign-born grandparent) vs fourth-plus
lab["Hisp G3 (gp foreign)"] = lab["Hisp G3+"] & D.gpar.between(1, 4).to_numpy()
lab["Hisp G4+ (no gp foreign)"] = lab["Hisp G3+"] & D.gpar.eq(0).to_numpy()
ORDER = ["Mex G1","Mex G2","Mex G3+","Hisp G1","Hisp G2","Hisp G3+",
         "Hisp G3 (gp foreign)","Hisp G4+ (no gp foreign)","NHWhite G3+",
         "White G3+ liberal","White G3+ moderate","White G3+ conservative",
         "White G3+ no BA","White G3+ BA+"]
print("\ngroup n:", {k: int(lab[k].sum()) for k in ORDER})
print("weighted Hispanic generation shares by year:")
for y in (2020, 2024):
    sel = (D.year == y).to_numpy() & D.hispanic.to_numpy() & D.gen.notna().to_numpy()
    w = D.wpost.to_numpy()
    tot = np.nansum(np.where(sel & (w > 0), w, 0))
    print("  ", y, {f"G{int(v)}": round(float(np.nansum(np.where(sel & D.gen.eq(v).to_numpy() & (w > 0), w, 0)) / tot), 3) for v in (1, 2, 3)})

def recode(x, rule):
    kind, arg = rule
    v = x.where(x >= 0)
    if kind == "le":   return v.le(arg).where(v.notna()).astype(float)
    if kind == "eq":   return v.eq(arg).where(v.notna()).astype(float)
    if kind == "ge_in": return v.isin(arg).where(v.notna()).astype(float)
    raise ValueError(kind)

# ---- build outcomes, tracking which weight each one needs --------------------
Y, STAGE, LBL, YRS = {}, {}, {}, {}
for name, spec in ITEMS.items():
    col = pd.Series(np.nan, index=D.index)
    stages, years = set(), []
    for y, (var, stage) in spec["v"].items():
        if var not in D.columns:
            continue
        sel = (D.year == y).to_numpy()
        col[sel] = recode(D.loc[sel, var], spec["rule"]).to_numpy()
        stages.add(stage); years.append(y)
    if not years:
        print("SKIP (variable absent):", name); continue
    Y[name] = col; STAGE[name] = "post" if "post" in stages else "pre"
    LBL[name] = spec["label"]; YRS[name] = sorted(years)
am = pd.concat([Y[k] for k in AUTH4 if k in Y], axis=1)
Y["auth_scale4"] = am.sum(axis=1).where(am.notna().all(axis=1))
STAGE["auth_scale4"] = "post"; YRS["auth_scale4"] = [2020, 2024]
LBL["auth_scale4"] = "authoritarian child-rearing scale, 0-4 authoritarian choices"

# ---- design, one per weight stage -------------------------------------------
def build_design(stage):
    w = D.wpost if stage == "post" else D.wpre
    f = D.assign(w=w, vstrat=D.strat, vpsu=D.psu)
    keep = f.w.notna() & f.w.gt(0) & f.vstrat.notna() & f.vpsu.notna()
    f = f[keep].reset_index(drop=True)
    # ANES strata are year-unique once year is folded in
    f["vstrat"] = f.year.astype(int) * 10000 + f.vstrat.astype(int)
    npsu = f.groupby(["vstrat", "vpsu"]).size().groupby(level=0).size()
    assert npsu.ge(2).all(), f"{stage}: stratum with one PSU"
    return f, keep.to_numpy(), npsu

RES_raw, RES_adj = [], []
for stage in ("pre", "post"):
    f, keep, npsu = build_design(stage)
    class Dg: pass
    dg = Dg(); dg.strat = f.vstrat.to_numpy(); dg.psu = f.vpsu.to_numpy()
    dg.n_strata = len(npsu); dg.n_psu = int(npsu.sum())
    dg.cov = Design.cov.__get__(dg)
    print(f"\n{stage} design: n={len(f)} strata={dg.n_strata} psus={dg.n_psu}")
    sub = {k: v[keep] for k, v in lab.items()}
    fW = f.copy()
    Zf, Znf = covariates(fW.assign(educ=fW.educ5, coninc=fW.inc), True, True)
    Zn_, Znn = covariates(fW.assign(educ=fW.educ5, coninc=fW.inc), False, True)
    WH = sub["NHWhite G3+"]; HP = sub["Hisp G1"] | sub["Hisp G2"] | sub["Hisp G3+"]
    MX = sub["Mex G1"] | sub["Mex G2"] | sub["Mex G3+"]
    ideo_na = WH & ~(sub["White G3+ liberal"] | sub["White G3+ moderate"] | sub["White G3+ conservative"])
    deg_na = WH & ~(sub["White G3+ no BA"] | sub["White G3+ BA+"])
    SPECS = {}
    for tag, gens, pool in [("hisp", ["Hisp G1","Hisp G2","Hisp G3+"], HP),
                            ("mex", ["Mex G1","Mex G2","Mex G3+"], MX)]:
        SPECS[f"adj_{tag}"] = dict(sample=WH | pool, Z=(Zf, Znf),
            dummies=[(g_, sub[g_]) for g_ in gens],
            contrasts={**{f"{g_} vs white G3+": {g_: 1.0} for g_ in gens},
                       **{f"{gens[b]} minus {gens[a]}": {gens[b]: 1.0, gens[a]: -1.0}
                          for a, b in [(0, 1), (0, 2), (1, 2)]}})
        SPECS[f"ideo_{tag}"] = dict(sample=WH | pool, Z=(Zf, Znf),
            dummies=[(g_, sub[g_]) for g_ in gens] +
                    [("white liberal", sub["White G3+ liberal"]),
                     ("white conservative", sub["White G3+ conservative"]),
                     ("white ideology missing", ideo_na)],
            contrasts={**{f"{g_} vs white moderate": {g_: 1.0} for g_ in gens},
                       **{f"{g_} vs white conservative": {g_: 1.0, "white conservative": -1.0} for g_ in gens},
                       **{f"{g_} vs white liberal": {g_: 1.0, "white liberal": -1.0} for g_ in gens},
                       "white conservative vs white liberal": {"white conservative": 1.0, "white liberal": -1.0}})
        SPECS[f"educ_{tag}"] = dict(sample=WH | pool, Z=(Zn_, Znn),
            dummies=[(g_, sub[g_]) for g_ in gens] +
                    [("white BA+", sub["White G3+ BA+"]), ("white degree missing", deg_na)],
            contrasts={**{f"{g_} vs white no BA": {g_: 1.0} for g_ in gens},
                       "white BA+ vs white no BA": {"white BA+": 1.0}})
    for name in Y:
        if STAGE[name] != stage: continue
        y = Y[name].to_numpy(float)[keep]
        infl, meta = [], []
        w = fW.w.to_numpy()
        for gname in ORDER:
            m = sub[gname] & np.isfinite(y)
            if m.sum() < 5 or w[m].sum() <= 0: continue
            est = float(w[m] @ y[m] / w[m].sum())
            infl.append(np.where(m, w * (np.nan_to_num(y) - est) / w[m].sum(), 0.0))
            meta.append((gname, int(m.sum()), est))
        if not meta: continue
        C = dg.cov(np.column_stack(infl))
        for j, (gname, n, est) in enumerate(meta):
            RES_raw.append(dict(item=name, label=LBL[name], years=str(YRS[name]),
                                group=gname, n=n, mean=est, se=math.sqrt(max(0, C[j, j]))))
        for mn, sp in SPECS.items():
            fit = wls(fW, dg, y, sp["sample"], sp["dummies"], *sp["Z"])
            if fit is None: continue
            for cn, cs in sp["contrasts"].items():
                r = contrast(fit, cs)
                if r: RES_adj.append(dict(item=name, label=LBL[name], model=mn,
                                          contrast=cn, estimate=r[0], se=r[1], n=fit["n"]))
R = pd.DataFrame(RES_raw); A = pd.DataFrame(RES_adj)
R.to_csv("derived/anes_raw_means.csv", index=False); A.to_csv("derived/anes_adjusted.csv", index=False)
print(f"\nwrote derived/anes_raw_means.csv ({len(R)}) and derived/anes_adjusted.csv ({len(A)})")
json.dump(dict(missing_columns={str(k): v for k, v in miss.items()},
               items={k: dict(label=LBL[k], years=YRS[k], stage=STAGE[k]) for k in Y}),
          open("derived/anes_audit.json", "w"), indent=2)

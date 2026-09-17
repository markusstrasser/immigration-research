"""Descriptive within-CBSA panel. Fixed effects remove fixed area differences and common
year shocks, but do not identify causality; changing boundaries remain unharmonized."""
import json, pathlib, warnings
import numpy as np, pandas as pd, statsmodels.api as sm
import fetch_acs as F
from build_panel import women_age_windows
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2022, 2023]  # Standard 2020 ACS1 unavailable; published 2021 omitted here.
G = ["B13008", "B05012", "B25064", "B19013", "B01001"]
OUT = []
def say(s=""):
    print(s); OUT.append(s)

def load(year, group):
    d = json.loads((CACHE / f"acs_acs1_{year}_{group}_cbsa.json").read_text())
    hdr = list(d[0]); seen = set()
    for i, c in enumerate(hdr):
        if c in seen: hdr[i] = f"{c}__d{i}"
        seen.add(c)
    df = pd.DataFrame(d[1:], columns=hdr).rename(
        columns={"metropolitan statistical area/micropolitan statistical area": "cbsa"})
    keep = [c for c in df.columns if c.startswith(group) and c.endswith("E")]
    for c in keep: df[c] = pd.to_numeric(df[c], errors="coerce")
    df.loc[:, keep] = df[keep].mask(df[keep] < -1e8)
    return df[["cbsa"] + keep]

for y in YEARS:
    for g in G:
        F.fetch(str(y), "acs/acs1", g)
rows = []
for y in YEARS:
    d = load(y, G[0])
    for g in G[1:]:
        d = d.merge(load(y, g), on="cbsa", how="outer")
    nb = d.B13008_004E + d.B13008_007E
    nw = nb + d.B13008_011E + d.B13008_014E
    w2034, w1550 = women_age_windows(d)
    rows.append(pd.DataFrame({
        "cbsa": d.cbsa, "year": y, "native_birth_rate": nb / nw * 1000, "native_women": nw,
        "fb_share": d.B05012_003E / d.B05012_001E * 100,
        "log_rent": np.log(d.B25064_001E), "log_income": np.log(d.B19013_001E),
        "share_w2034": w2034 / w1550 * 100, "pop": d.B05012_001E}))
p = pd.concat(rows).dropna()
p["cbsa"] = p.cbsa.replace({"31100": "31080", "42060": "42200"})
n_y = p.groupby("cbsa").year.nunique()
bal = n_y[n_y >= 10].index                      # metros observed in >=10 of the 12 years
p = p[p.cbsa.isin(bal)].copy()
say("=" * 100)
say("7. DESCRIPTIVE CBSA FE, 2010-2023 (standard 2020 ACS1 unavailable; published 2021 omitted)")
say("  [DEGRADED] CBSA boundaries are not harmonized; fixed effects do not identify causality.")
say("=" * 100)
say(f"  metros with >=10 years: {p.cbsa.nunique()}   metro-year observations: {len(p)}")

def fe(df, y, x, ctrl, w=None, label="", cluster=True):
    X = pd.concat([df[[x] + list(ctrl)],
                   pd.get_dummies(df.cbsa, prefix="m", drop_first=True, dtype=float),
                   pd.get_dummies(df.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X)
    mod = sm.WLS(df[y], X, weights=df[w]) if w else sm.OLS(df[y], X)
    m = mod.fit(cov_type="cluster", cov_kwds={"groups": df.cbsa}) if cluster else mod.fit(cov_type="HC1")
    say(f"  {label:<46} b={m.params[x]:+8.4f}  se={m.bse[x]:6.4f}  t={m.tvalues[x]:+6.2f}"
        f"  p={m.pvalues[x]:.4f}  n={int(m.nobs):5d}")
    return m

say("  [metro FE + year FE, SEs clustered by metro]")
m_fe = fe(p, "native_birth_rate", "fb_share", [], label="no time-varying controls")
fe(p, "native_birth_rate", "fb_share", ["share_w2034"], label="+ age structure")
m_fe2 = fe(p, "native_birth_rate", "fb_share", ["log_rent", "log_income", "share_w2034"],
           label="+ rent, income, age structure")
fe(p, "native_birth_rate", "fb_share", ["log_rent", "log_income", "share_w2034"],
   w="native_women", label="+ controls, weighted by native women")
top50 = p[p.cbsa.isin(p.groupby("cbsa")["pop"].max().nlargest(50).index)]
fe(top50, "native_birth_rate", "fb_share", ["log_rent", "log_income", "share_w2034"],
   label="50 largest metros only")
say("  channel check inside the FE panel:")
fe(p, "log_rent", "fb_share", ["log_income"], label="log rent on fb_share (metro+year FE)")
say("")
say("  POOLED CROSS-SECTION for contrast (no metro FE, year FE only):")
Xp = pd.concat([p[["fb_share", "log_rent", "log_income", "share_w2034"]],
                pd.get_dummies(p.year, prefix="y", drop_first=True, dtype=float)], axis=1)
mp = sm.OLS(p.native_birth_rate, sm.add_constant(Xp)).fit(
    cov_type="cluster", cov_kwds={"groups": p.cbsa})
say(f"  {'pooled, year FE only':<46} b={mp.params['fb_share']:+8.4f}  "
    f"se={mp.bse['fb_share']:6.4f}  t={mp.tvalues['fb_share']:+6.2f}  p={mp.pvalues['fb_share']:.4f}")
say("")
say(f"  HYPOTHETICAL LINEAR EXTRAPOLATION, NOT A NATIONAL EFFECT ESTIMATE: b={m_fe2.params['fb_share']:+.4f}, "
    f"95% CI [{m_fe2.params['fb_share']-1.96*m_fe2.bse['fb_share']:+.3f}, "
    f"{m_fe2.params['fb_share']+1.96*m_fe2.bse['fb_share']:+.3f}]")
for b, nm in ((m_fe2.params["fb_share"], "point"),
              (m_fe2.params["fb_share"] - 1.96 * m_fe2.bse["fb_share"], "CI lower (most negative)")):
    say(f"    {nm:<26}: fewer native women reporting a birth at fb_share=15.6% = {-b*15.6/1000*65192113:+,.0f} "
        f"({-b*15.6/1000*65192113/792725*100:+.1f}% of 792,725 foreign-born women reporting a birth)")
p.to_csv(HERE / "fe_panel.csv", index=False)
(HERE / "fe_output.txt").write_text("\n".join(OUT) + "\n")

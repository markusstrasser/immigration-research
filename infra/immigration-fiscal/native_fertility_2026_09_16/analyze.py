"""Native birth rate vs foreign-born share: cross-sections, long differences, shift-share IV."""
import json, pathlib, re, warnings
import numpy as np, pandas as pd, statsmodels.api as sm
from build_panel import build
warnings.filterwarnings("ignore")

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ZORI = pathlib.Path("/Users/alien/research-data/immigration-fiscal/data/external/"
                    "urban_housing/zillow/metro_zori_sfrcondomfr_sm_month.csv")
CTRL = ["log_rent", "log_income", "ba_plus_share", "black_share", "hisp_share",
        "ownership_rate", "median_age_native_female", "share_women_20_34"]
OUT = []


def say(s=""):
    print(s); OUT.append(s)


def prep(tag):
    # Rebuild from source: tracked panel CSVs are pre-audit historical snapshots.
    d = build(tag)
    d = d[d.native_women_15_50 > 0].copy()
    d["log_rent"] = np.log(d.median_rent)
    d["log_income"] = np.log(d.median_hh_income)
    d["log_pop"] = np.log(d["pop"])
    return d.dropna(subset=["native_birth_rate", "fb_share"] + CTRL)


def reg(d, y, x, ctrl, w=None, label=""):
    X = sm.add_constant(d[[x] + list(ctrl)])
    m = (sm.WLS(d[y], X, weights=d[w]) if w else sm.OLS(d[y], X)).fit(cov_type="HC1")
    say(f"  {label:<44} b={m.params[x]:+8.4f}  se={m.bse[x]:6.4f}  "
        f"t={m.tvalues[x]:+6.2f}  p={m.pvalues[x]:.4f}  n={int(m.nobs):4d}  R2={m.rsquared:.3f}")
    return m


def top(d, n):
    return d.nlargest(n, "pop")


# ---------------------------------------------------------------- CIS reproduction
say("=" * 100)
say("1. CIS COMPARISON (different controls; not a specification replication), ACS 2015-2019")
say("   women reporting a birth per 1,000 native women 15-50 on immigrant share.")
say("   Their reported coefficient, 50 largest metros with controls: -0.269")
say("=" * 100)
d19 = prep("acs5_2019")
t50 = top(d19, 50)
say(f"[2015-19 5-year, 50 largest metros, n={len(t50)}]")
reg(t50, "native_birth_rate", "fb_share", [], label="bivariate")
m_cis = reg(t50, "native_birth_rate", "fb_share", CTRL, label="+ full controls")
reg(t50, "native_birth_rate", "fb_share", CTRL, w="native_women_15_50",
    label="+ controls, native-women-weighted")
say(f"[2015-19 5-year, all published CBSAs, n={len(d19)}]")
reg(d19, "native_birth_rate", "fb_share", [], label="bivariate")
reg(d19, "native_birth_rate", "fb_share", CTRL, label="+ full controls")
for n in (100, 250):
    reg(top(d19, n), "native_birth_rate", "fb_share", CTRL, label=f"+ controls, top {n}")
say("  smaller-metro split (rank 51+):")
reg(d19[~d19.cbsa.isin(t50.cbsa)], "native_birth_rate", "fb_share", CTRL, label="  rank 51+")

# ---------------------------------------------------------------- 2023 cross-section
say(""); say("=" * 100)
say("2. OWN SPEC -- ACS 2023 1-year cross-section")
say("=" * 100)
d23 = prep("acs1_2023")
say(f"[2023, 50 largest, n={len(top(d23,50))}]")
reg(top(d23, 50), "native_birth_rate", "fb_share", [], label="bivariate")
reg(top(d23, 50), "native_birth_rate", "fb_share", CTRL, label="+ full controls")
say(f"[2023, all published CBSAs, n={len(d23)}]")
reg(d23, "native_birth_rate", "fb_share", [], label="bivariate")
m23 = reg(d23, "native_birth_rate", "fb_share", CTRL, label="+ full controls")
reg(d23, "native_birth_rate", "fb_share", CTRL, w="native_women_15_50",
    label="+ controls, native-women-weighted")
say("  descriptive association (not a placebo): foreign-born birth reporting on fb_share")
reg(d23, "fb_birth_rate", "fb_share", CTRL, label="  FB birth rate")
say("  rent as the claimed channel: log_rent on fb_share (first stage of the story)")
reg(d23, "log_rent", "fb_share", [c for c in CTRL if c != "log_rent"], label="  log rent")
say("  omit rent from controls (descriptive specification sensitivity):")
reg(d23, "native_birth_rate", "fb_share", [c for c in CTRL if c != "log_rent"],
    label="  no-rent controls")

# ---------------------------------------------------------------- long difference
say(""); say("=" * 100)
say("3. LONG DIFFERENCE 2010 -> 2023 (CBSA codes harmonized; 2009 vintage vs 2023 vintage)")
say("=" * 100)
d10 = prep("acs1_2010")
XW = {"31100": "31080", "42060": "42200", "14460": "14460", "19380": "19380"}
d10["cbsa"] = d10.cbsa.replace(XW)
common = sorted(set(d10.cbsa) & set(d23.cbsa))
say(f"  2010 n={len(d10)}  2023 n={len(d23)}  harmonized common n={len(common)}")
miss = d10[~d10.cbsa.isin(d23.cbsa)].nlargest(5, "pop")[["cbsa", "name", "pop"]]
say("  largest 2010 CBSAs with no 2023 match (delineation changes / non-publication):")
for _, r in miss.iterrows():
    say(f"    {r.cbsa} {r['name'][:58]:<58} pop={r['pop']:,.0f}")
a = d10[d10.cbsa.isin(common)].set_index("cbsa").sort_index()
b = d23[d23.cbsa.isin(common)].set_index("cbsa").sort_index()
dd = pd.DataFrame({
    "d_native_birth_rate": b.native_birth_rate - a.native_birth_rate,
    "d_fb_share": b.fb_share - a.fb_share,
    "d_log_rent": b.log_rent - a.log_rent,
    "d_log_income": b.log_income - a.log_income,
    "d_ba": b.ba_plus_share - a.ba_plus_share,
    "d_black": b.black_share - a.black_share,
    "d_hisp": b.hisp_share - a.hisp_share,
    "d_own": b.ownership_rate - a.ownership_rate,
    "d_age": b.median_age_native_female - a.median_age_native_female,
    "d_w2034": b.share_women_20_34 - a.share_women_20_34,
    "fb_share_2010": a.fb_share, "pop": b["pop"], "name": b.name,
    "native_women_15_50": b.native_women_15_50,
}).dropna()
DCTRL = ["d_log_rent", "d_log_income", "d_ba", "d_black", "d_hisp", "d_own", "d_age", "d_w2034"]
say(f"[long difference, n={len(dd)}]")
reg(dd, "d_native_birth_rate", "d_fb_share", [], label="bivariate")
m_ld = reg(dd, "d_native_birth_rate", "d_fb_share", DCTRL, label="+ full delta controls")
reg(dd, "d_native_birth_rate", "d_fb_share", DCTRL, w="native_women_15_50",
    label="+ controls, native-women-weighted")
reg(dd.nlargest(50, "pop"), "d_native_birth_rate", "d_fb_share", DCTRL, label="top 50 only")
say(f"  mean change in native birth rate: {dd.d_native_birth_rate.mean():+.2f} per 1,000")
say(f"  mean change in fb share:          {dd.d_fb_share.mean():+.2f} pts")

# ---------------------------------------------------------------- shift-share IV
say(""); say("=" * 100)
say("4. SHIFT-SHARE DIAGNOSTIC -- matched origin labels and published-CBSA stock changes")
say("   [INVALID FOR IV] National coverage/geography not harmonized. Base year is 2010; the")
say("   1990/2000 base is not reachable at 2023-vintage CBSA geography here. [CAVEAT]")
say("=" * 100)


def b05006(year, ds):
    d = json.loads((CACHE / f"{ds}_{year}_B05006_cbsa.json").read_text())
    hdr = list(d[0])
    seen = set()
    for i, c in enumerate(hdr):
        if c in seen:
            hdr[i] = f"{c}__dup{i}"
        seen.add(c)
    df = pd.DataFrame(d[1:], columns=hdr)
    df = df.rename(columns={"metropolitan statistical area/micropolitan statistical area": "cbsa"})
    vs = [c for c in df.columns if re.fullmatch(r"B05006_\d+E", c)]
    for c in vs:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df[vs] = df[vs].mask(df[vs] < -1e8)
    return df.set_index("cbsa")[vs]


lab10 = json.loads((CACHE / "acs_acs1_2010_B05006_cbsa.json").read_text())
v10 = b05006("2010", "acs_acs1")
v23 = b05006("2023", "acs_acs1")
lbl = {k: v["label"] for k, v in
       json.loads(pathlib.Path(CACHE / "b05006_labels.json").read_text())["variables"].items()} \
    if (CACHE / "b05006_labels.json").exists() else None
# leaf countries only: a variable is a leaf if no other label extends it. Use the 2023 metadata.
import urllib.request
meta_p = CACHE / "b05006_2023_meta.json"
if not meta_p.exists():
    meta_p.write_bytes(urllib.request.urlopen(
        "https://api.census.gov/data/2023/acs/acs1/groups/B05006.json", timeout=120).read())
meta = json.loads(meta_p.read_text())["variables"]
meta10_p = CACHE / "b05006_2010_meta.json"
if not meta10_p.exists():
    meta10_p.write_bytes(urllib.request.urlopen(
        "https://api.census.gov/data/2010/acs/acs1/groups/B05006.json", timeout=120).read())

def origin_leaves(metadata):
    labels = {k: re.sub(r"[^a-z0-9!]", "", v["label"].lower()) for k, v in metadata.items()
              if k.startswith("B05006") and k.endswith("E")}
    return {label: k for k, label in labels.items()
            if not any(other.startswith(label + "!!") for other in labels.values())}

old_labels = origin_leaves(json.loads(meta10_p.read_text())["variables"])
new_labels = origin_leaves(meta)
leaves = sorted(old_labels.keys() & new_labels.keys())
if not leaves:
    raise ValueError("No common origin labels across source vintages; no exposure can be constructed.")
v10.index = v10.index.to_series().replace(XW)
S10 = v10[[old_labels[label] for label in leaves]].copy()
S23 = v23[[new_labels[label] for label in leaves]].copy()
S10.columns = S23.columns = leaves
shares = S10.div(S10.sum(axis=0, min_count=1).replace(0, np.nan), axis=1)
cbsa_growth = S23.sum(min_count=1) - S10.sum(min_count=1)  # Not national totals.
bartik = (shares * cbsa_growth).sum(axis=1, min_count=len(leaves))
dd["bartik_raw"] = bartik.reindex(dd.index)
dd["bartik"] = dd.bartik_raw / a["pop"].reindex(dd.index) * 100   # predicted pp change in fb share
iv = dd.dropna(subset=["bartik"]).copy()
say(f"  matched leaf origins: {len(leaves)}   complete origin exposure: {len(iv)}/{len(dd)} metros")
say(f"  corr(bartik, actual d_fb_share) = {iv.bartik.corr(iv.d_fb_share):.3f}")
fs = reg(iv, "d_fb_share", "bartik", DCTRL, label="FIRST STAGE: d_fb_share on bartik")
say(f"  first-stage F (robust) = {fs.tvalues['bartik']**2:.1f} "
    f"({'strong' if fs.tvalues['bartik']**2 > 10 else 'WEAK -- IV unreliable'})")
say("  [INVALID] 2SLS DISABLED: harmonize geography and coverage, obtain national origin stocks,")
say("  and establish a valid strong first stage before estimating a causal effect.")
iv_b = iv_se = float("nan")

# ---------------------------------------------------------------- ZORI
say(""); say("=" * 100)
say("5. ZILLOW ZORI RENT GROWTH 2015->2023 AS AN ALTERNATIVE RENT MEASURE")
say("=" * 100)
z = pd.read_csv(ZORI)
z = z[z.RegionType == "msa"].copy()
c15 = [c for c in z.columns if c.startswith("2015-")]
c23 = [c for c in z.columns if c.startswith("2023-")]
z["zori_growth"] = np.log(z[c23].mean(axis=1) / z[c15].mean(axis=1))


def keyname(s):
    s = str(s).split(" Metro Area")[0].split(" Micro Area")[0]
    city, st = s.rsplit(",", 1)
    return (city.split("-")[0].strip().lower(), st.strip().split("-")[0].strip().lower())


z["k"] = z.RegionName.map(keyname)
zz = z.dropna(subset=["zori_growth"]).drop_duplicates("k").set_index("k").zori_growth
dd["k"] = dd.name.map(keyname)
dd["zori_growth"] = dd.k.map(zz)
say(f"  ZORI matched to {dd.zori_growth.notna().sum()} of {len(dd)} long-difference metros")
zd = dd.dropna(subset=["zori_growth"])
say(f"  corr(zori_growth, d_log_rent ACS) = {zd.zori_growth.corr(zd.d_log_rent):.3f}")
say(f"  corr(zori_growth, d_fb_share)     = {zd.zori_growth.corr(zd.d_fb_share):.3f}")
reg(zd, "d_native_birth_rate", "d_fb_share",
    [c for c in DCTRL if c != "d_log_rent"] + ["zori_growth"], label="ZORI in place of ACS rent")
reg(zd, "d_native_birth_rate", "d_fb_share", DCTRL + ["zori_growth"], label="both rent measures")
reg(zd, "zori_growth", "d_fb_share", [c for c in DCTRL if c != "d_log_rent"],
    label="ZORI growth on d_fb_share")

# ---------------------------------------------------------------- arithmetic
say(""); say("=" * 100)
say("6. ARITHMETIC AT THE ESTIMATED COEFFICIENTS  [INFERENCE]")
say("=" * 100)
nat_fb = 15.6
b_cis, b_own, b_ld = m_cis.params["fb_share"], m23.params["fb_share"], m_ld.params["d_fb_share"]
nw = d23.native_women_15_50.sum()
say(f"  native women 15-50 in published CBSAs, 2023 (ACS B13008): {nw:,.0f}")
nat_us = json.loads((CACHE / "acs_acs1_2023_B13008_us.json").read_text())
h = nat_us[0]; r = nat_us[1]
gi = {c: i for i, c in enumerate(h)}
nb_us = int(r[gi["B13008_004E"]]) + int(r[gi["B13008_007E"]])
nw_us = nb_us + int(r[gi["B13008_011E"]]) + int(r[gi["B13008_014E"]])
say(f"  national native women 15-50: {nw_us:,}   native births past 12 mo: {nb_us:,}")
for nm, b in (("CIS comparison (2015-19, top 50)", b_cis), ("own 2023 cross-section", b_own),
              ("long difference 2010-23", b_ld)):
    lost = -b * nat_fb / 1000 * nw_us
    say(f"  {nm:<32} b={b:+.4f} -> counterfactual native births forgone at "
        f"fb_share={nat_fb}%: {lost:+,.0f}/yr ({lost/nb_us*100:+.1f}% of native births)")
say("  Against: immigrant TFR 2.02 vs native 1.69 (2019, CIS); ~945,000 Hispanic births/yr.")
fb_us_b = int(r[gi["B13008_005E"]]) + int(r[gi["B13008_008E"]])
say(f"  ACS 2023 direct count of births to foreign-born women past 12 mo: {fb_us_b:,}")
say(f"  ratio of the largest estimated native loss to foreign-born births: "
    f"{-b_cis*nat_fb/1000*nw_us/fb_us_b*100:+.1f}%")

(HERE / "analysis_output.txt").write_text("\n".join(OUT) + "\n")
dd.to_csv(HERE / "long_difference.csv")

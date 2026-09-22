"""AHS 2023 national household-level test of H1.

Does householder Hispanic origin predict worse unit adequacy and worse
neighborhood conditions once household income, tenure, metro, structure age and
crowding are held fixed?

Variables verified against the AHS 2023 National PUF flat-CSV header:
  HHSPAN     householder Hispanic origin
  HHRACE     householder race
  HHNATVTY   householder nativity (country of birth code)
  HINCP      household income
  TENURE     owner / renter / no cash rent
  ADEQUACY   unit adequacy (1 adequate, 2 moderately, 3 severely inadequate)
  RATINGNH   respondent's 1-10 rating of the neighborhood
  RATINGHS   respondent's 1-10 rating of the unit
  NEARTRASH  trash, litter or junk in streets/properties nearby
  NEARABAND  abandoned or vandalized buildings nearby
  NEARBARCL  bars on windows of buildings nearby
  NHQPCRIME  neighborhood petty crime
  NHQSCRIME  neighborhood serious crime
  NHQSCHOOL  neighborhood schools
  NHQPUBTRN  neighborhood public transport
  NHQRISK    neighborhood natural-disaster risk
  WEIGHT     final household weight; REPWEIGHT1-160 replicate weights
  OMB13CBSA  metro area; DIVISION census division
  BLD YRBUILT UNITSIZE NUMPEOPLE TOTROOMS PERPOVLVL HUDSUB

Standard errors: AHS is a complex sample. The main specification is re-fit on all
160 replicate weights and the variance is the successive-difference replication
estimate, Var = (4/160) * sum_r (b_r - b)^2.
"""
import io, json, pathlib, re, sys, zipfile
import numpy as np, pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

HERE = pathlib.Path(__file__).parent; CD = HERE/"_cache"
ZIP = _data_paths.data_root(require_exists=False) / "external/ahs_2023/ahs2023_flat_v1_0.zip"
pd.set_option("display.width", 250, "display.max_columns", 60)

EXPECTED = 141729433
sz = ZIP.stat().st_size if ZIP.exists() else 0
if sz != EXPECTED:
    print(f"[GAP] {ZIP} is {sz} bytes, expected {EXPECTED}. Not a complete zip.")
    sys.exit(2)

z = zipfile.ZipFile(ZIP)
csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
target = max(csvs, key=lambda n: z.getinfo(n).file_size)
print("zip contents:", z.namelist())
print("using:", target, z.getinfo(target).file_size, "bytes uncompressed")

CORE = ["CONTROL","WEIGHT","HHSPAN","HHRACE","HHNATVTY","HINCP","TENURE",
        "ADEQUACY","RATINGNH","RATINGHS","NEARTRASH","NEARABAND","NEARBARCL",
        "NHQPCRIME","NHQSCRIME","NHQSCHOOL","NHQPUBTRN","NHQRISK",
        "OMB13CBSA","DIVISION","BLD","YRBUILT","UNITSIZE","NUMPEOPLE",
        "TOTROOMS","PERPOVLVL","HUDSUB"]
REPS = [f"REPWEIGHT{i}" for i in range(1, 161)]

hdr = pd.read_csv(z.open(target), nrows=0, dtype=str)
have = [c for c in CORE + REPS if c in hdr.columns]
missing = [c for c in CORE if c not in hdr.columns]
print("missing core variables:", missing)

df = pd.read_csv(z.open(target), usecols=have, dtype=str, low_memory=False)
print("households:", len(df))


def clean(s):
    return (s.astype(str).str.strip().str.strip("'").str.strip('"')
             .replace({"": np.nan, "-6": np.nan, "-9": np.nan, "M": np.nan,
                       "N": np.nan, "B": np.nan, ".": np.nan, "nan": np.nan}))


for c in df.columns:
    df[c] = clean(df[c])
for c in ["WEIGHT","HINCP","RATINGNH","RATINGHS","NUMPEOPLE","TOTROOMS",
          "PERPOVLVL"] + REPS:
    if c in df:
        df[c] = pd.to_numeric(df[c], errors="coerce")

print("\n=== value distributions of the classification and outcome variables ===")
for c in ["HHSPAN","HHRACE","TENURE","ADEQUACY","NEARTRASH","NEARABAND",
          "NEARBARCL","NHQPCRIME","NHQSCRIME","NHQSCHOOL","NHQPUBTRN","NHQRISK",
          "BLD","UNITSIZE","HUDSUB"]:
    if c in df:
        print(f"--- {c} ---")
        print(df[c].value_counts(dropna=False).head(12).to_string())
print("--- HHNATVTY top 15 ---")
print(df["HHNATVTY"].value_counts(dropna=False).head(15).to_string())
print("--- RATINGNH ---")
print(df["RATINGNH"].value_counts(dropna=False).sort_index().to_string())
print("--- HINCP summary ---")
print(df["HINCP"].describe().to_string())

# ---------------- recodes ----------------
# HHSPAN: 1 = Hispanic, 2 = not Hispanic (verify from the printout above)
df["hisp"] = (df.HHSPAN == "1").astype(float)
df.loc[df.HHSPAN.isna(), "hisp"] = np.nan

# nativity: the modal HHNATVTY code is the United States
us_code = df["HHNATVTY"].value_counts().idxmax()
print("\nmodal HHNATVTY code treated as United States:", us_code)
df["foreign_born"] = (df.HHNATVTY.notna() & (df.HHNATVTY != us_code)).astype(float)
df.loc[df.HHNATVTY.isna(), "foreign_born"] = np.nan
MEX = {"210", "303", "2000"}          # candidate Mexico codes; resolved below
mex_code = None
for cand in df["HHNATVTY"].value_counts().index[:12]:
    if cand in MEX:
        mex_code = cand; break
df["mex_born"] = (df.HHNATVTY == mex_code).astype(float) if mex_code else np.nan
print("HHNATVTY code treated as Mexico:", mex_code,
      "(n =", int(df['mex_born'].sum()) if mex_code else 0, ")")

df["inadequate"] = df.ADEQUACY.isin(["2", "3"]).astype(float)
df.loc[df.ADEQUACY.isna(), "inadequate"] = np.nan
df["sev_inadequate"] = (df.ADEQUACY == "3").astype(float)
df.loc[df.ADEQUACY.isna(), "sev_inadequate"] = np.nan

# the NEAR*/NHQ* battery: 1 = yes/present, 2 = no
for c, name in [("NEARTRASH","trash_nearby"), ("NEARABAND","abandoned_nearby"),
                ("NEARBARCL","bars_on_windows"), ("NHQPCRIME","petty_crime"),
                ("NHQSCRIME","serious_crime"), ("NHQSCHOOL","school_problem"),
                ("NHQPUBTRN","transit_problem"), ("NHQRISK","disaster_risk")]:
    if c in df:
        df[name] = (df[c] == "1").astype(float)
        df.loc[df[c].isna(), name] = np.nan

df["nh_rating"] = df.RATINGNH
df["unit_rating"] = df.RATINGHS
df["owner"] = (df.TENURE == "1").astype(float)
df["ppr"] = df.NUMPEOPLE/df.TOTROOMS.replace(0, np.nan)
df["crowded"] = (df.ppr > 1).astype(float)
df.loc[df.ppr.isna(), "crowded"] = np.nan
df["log_inc"] = np.log(df.HINCP.clip(lower=1000))
df["yrb"] = pd.to_numeric(df.YRBUILT, errors="coerce")

OUT = ["inadequate","sev_inadequate","trash_nearby","abandoned_nearby",
       "bars_on_windows","petty_crime","serious_crime","nh_rating","unit_rating"]
OUT = [o for o in OUT if o in df and df[o].notna().sum() > 1000]
print("\noutcomes analysed:", OUT)


def design(d, spec, key="hisp"):
    X = pd.DataFrame({key: d[key]})
    if spec >= 1:
        X["log_inc"] = d.log_inc
    if spec >= 2:
        X["owner"] = d.owner
        X = X.join(pd.get_dummies(d.TENURE.fillna("Z"), prefix="ten",
                                  drop_first=True).astype(float))
        X = X.join(pd.get_dummies(d.DIVISION.fillna("Z"), prefix="div",
                                  drop_first=True).astype(float))
        X["yrb"] = d.yrb
        X = X.join(pd.get_dummies(d.BLD.fillna("Z"), prefix="bld",
                                  drop_first=True).astype(float))
    if spec >= 3:
        X["ppr"] = d.ppr
        X["hh_size"] = d.NUMPEOPLE
    return sm.add_constant(X.astype(float))


SPECS = {0: "raw", 1: "+income", 2: "+income, tenure, division, structure age/type",
         3: "+ persons per room, household size"}

rows = []
for y in OUT:
    for spec, label in SPECS.items():
        d = df.dropna(subset=[y, "hisp", "log_inc", "WEIGHT"]).copy()
        X = design(d, spec)
        d = d.loc[X.dropna().index]; X = X.dropna()
        m = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit(cov_type="HC1")
        rows.append(dict(outcome=y, spec=label, beta=m.params["hisp"],
                         se_hc1=m.bse["hisp"], t=m.tvalues["hisp"],
                         p=m.pvalues["hisp"], n=int(m.nobs),
                         mean_y=np.average(d[y].astype(float), weights=d.WEIGHT)))
R = pd.DataFrame(rows)
print("\n=== TABLE 18. AHS 2023: Hispanic householder coefficient, weighted "
      "(HC1 standard errors) ===")
print(R.round(4).to_string(index=False))
R.round(5).to_csv(HERE/"table18_ahs_hispanic.csv", index=False)

# nativity cut: foreign-born householder, and Mexico-born where identifiable
rows2 = []
for key in ["foreign_born"] + (["mex_born"] if df["mex_born"].notna().any() else []):
    for y in OUT:
        for spec, label in SPECS.items():
            d = df.dropna(subset=[y, key, "log_inc", "WEIGHT"]).copy()
            X = design(d, spec, key=key)
            d = d.loc[X.dropna().index]; X = X.dropna()
            m = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit(cov_type="HC1")
            rows2.append(dict(regressor=key, outcome=y, spec=label,
                              beta=m.params[key], t=m.tvalues[key],
                              p=m.pvalues[key], n=int(m.nobs)))
R2 = pd.DataFrame(rows2)
print("\n=== TABLE 19. AHS 2023: nativity of householder ===")
print(R2.round(4).to_string(index=False))
R2.round(5).to_csv(HERE/"table19_ahs_nativity.csv", index=False)

# ---------- replicate-weight SEs for the fullest spec ----------
have_reps = [c for c in REPS if c in df]
if have_reps:
    print(f"\n=== TABLE 20. Successive-difference replication standard errors "
          f"({len(have_reps)} replicate weights), fullest specification ===")
    rows3 = []
    for y in OUT:
        d = df.dropna(subset=[y, "hisp", "log_inc", "WEIGHT"]).copy()
        X = design(d, 3)
        d = d.loc[X.dropna().index]; X = X.dropna()
        b0 = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit().params["hisp"]
        bs = []
        for rw in have_reps:
            w = d[rw]
            ok = w.notna() & (w > 0)
            if ok.sum() < 1000: continue
            bs.append(sm.WLS(d.loc[ok, y].astype(float), X.loc[ok],
                             weights=w[ok]).fit().params["hisp"])
        bs = np.array(bs)
        se = np.sqrt(4.0/len(bs)*np.sum((bs - b0)**2)) if len(bs) else np.nan
        rows3.append(dict(outcome=y, beta=b0, se_sdr=se,
                          t_sdr=b0/se if se else np.nan, n_reps=len(bs),
                          n=int(len(d))))
        print(f"  {y}: beta={b0:.4f} se_sdr={se:.4f} t={b0/se:.2f}", flush=True)
    R3 = pd.DataFrame(rows3)
    R3.round(5).to_csv(HERE/"table20_ahs_sdr_se.csv", index=False)

# ---------- income-stratified means, the plain "equal income" comparison ----------
d = df.dropna(subset=["hisp","HINCP","WEIGHT"]).copy()
d["inc_band"] = pd.cut(d.HINCP, [-1e9, 25000, 50000, 75000, 100000, 150000, 1e9],
    labels=["<25k","25-50k","50-75k","75-100k","100-150k","150k+"])
print("\n=== TABLE 21. Weighted means by income band and Hispanic origin ===")
g = (d.groupby(["inc_band","hisp"], observed=True)
      .apply(lambda s: pd.Series({o: np.average(s[o].astype(float),
                weights=s.WEIGHT) if s[o].notna().sum() > 30 else np.nan
                for o in OUT} | {"n": len(s)}), include_groups=False))
print(g.round(3).to_string())
g.round(4).to_csv(HERE/"table21_ahs_income_bands.csv")

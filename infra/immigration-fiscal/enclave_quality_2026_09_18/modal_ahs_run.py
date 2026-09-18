"""AHS 2023 national household-level test of H1, executed in a Modal container.

The local link is saturated, so the 141,729,433-byte PUF is downloaded in the
cloud and only the result tables come back. Returns a dict of CSV strings that
the local entrypoint writes into the lane directory.

Design (as briefed): unit adequacy, the 1-10 neighborhood rating and each item of
the NEAR*/NHQ* neighborhood-problem battery regressed on a Hispanic-householder
indicator, and separately on foreign-born and Mexico-born householder indicators,
in nested specifications - raw, plus log household income, plus tenure, metro,
census division, structure age and structure type, plus persons per room and
household size. Weighted by WEIGHT. Successive-difference replication standard
errors from the 160 replicate weights for the headline outcomes.

Run:  modal run infra/immigration-fiscal/enclave_quality_2026_09_18/modal_ahs_run.py
"""
import modal

app = modal.App("ahs-enclave-quality-run")
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("pandas>=2", "numpy>=2", "statsmodels", "requests"))

URL = ("https://www2.census.gov/programs-surveys/ahs/2023/"
       "AHS%202023%20National%20PUF%20v1.0%20Flat%20CSV.zip")
EXPECTED = 141729433


@app.function(image=image, timeout=3600, memory=32768, cpu=8)
def run():
    import io, zipfile, requests
    import numpy as np, pandas as pd, statsmodels.api as sm

    out = {}
    log = []
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True); log.append(s)

    r = requests.get(URL, timeout=2400)
    r.raise_for_status()
    P("downloaded bytes:", len(r.content), "expected:", EXPECTED,
      "MATCH" if len(r.content) == EXPECTED else "MISMATCH")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    P("zip opens OK; contents:", z.namelist())
    csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
    target = max(csvs, key=lambda n: z.getinfo(n).file_size)
    P("using:", target, z.getinfo(target).file_size, "bytes uncompressed")

    hdr = pd.read_csv(z.open(target), nrows=0, dtype=str)
    P("header column count:", len(hdr.columns),
      "(expected 3208)" if len(hdr.columns) == 3208 else "(UNEXPECTED)")

    CORE = ["CONTROL","WEIGHT","HHSPAN","HHRACE","HHNATVTY","HINCP","TENURE",
            "ADEQUACY","RATINGNH","RATINGHS","NEARTRASH","NEARABAND","NEARBARCL",
            "NHQPCRIME","NHQSCRIME","NHQSCHOOL","NHQPUBTRN","NHQRISK",
            "OMB13CBSA","DIVISION","BLD","YRBUILT","UNITSIZE","NUMPEOPLE",
            "TOTROOMS","PERPOVLVL","HUDSUB"]
    REPS = [f"REPWEIGHT{i}" for i in range(1, 161)]
    have = [c for c in CORE + REPS if c in hdr.columns]
    P("missing core:", [c for c in CORE if c not in hdr.columns])

    df = pd.read_csv(z.open(target), usecols=have, dtype=str, low_memory=False)
    P("households:", len(df))

    def clean(s):
        return (s.astype(str).str.strip().str.strip("'").str.strip('"')
                 .replace({"": np.nan, "-6": np.nan, "-9": np.nan, "M": np.nan,
                           "N": np.nan, "B": np.nan, ".": np.nan, "nan": np.nan}))
    for c in df.columns:
        df[c] = clean(df[c])
    for c in ["WEIGHT","HINCP","RATINGNH","RATINGHS","NUMPEOPLE","TOTROOMS",
              "PERPOVLVL"] + [c for c in REPS if c in df]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- distributions, so the coding can be verified rather than assumed ----
    vc_rows = []
    for c in ["HHSPAN","HHRACE","TENURE","ADEQUACY","NEARTRASH","NEARABAND",
              "NEARBARCL","NHQPCRIME","NHQSCRIME","NHQSCHOOL","NHQPUBTRN",
              "NHQRISK","BLD","UNITSIZE","HUDSUB","RATINGNH"]:
        if c not in df: continue
        vc = df[c].value_counts(dropna=False)
        P(f"--- {c} (nuniq={df[c].nunique()}) ---")
        P(vc.head(14).to_string())
        for k, v in vc.head(14).items():
            vc_rows.append(dict(variable=c, value=str(k), n=int(v),
                                pct=round(100*v/len(df), 2)))
    out["table18a_ahs_value_distributions.csv"] = pd.DataFrame(vc_rows).to_csv(index=False)

    # ---- recodes ----
    df["hisp"] = np.where(df.HHSPAN.isna(), np.nan, (df.HHSPAN == "1").astype(float))
    wsum = df.WEIGHT.sum()
    P("weighted Hispanic householder share: "
      f"{100*np.nansum(df.hisp*df.WEIGHT)/wsum:.2f}%  (ACS benchmark ~14%)")

    nat = df.HHNATVTY.value_counts()
    us_code = nat.idxmax()
    P("HHNATVTY top 15:"); P(nat.head(15).to_string())
    P("modal HHNATVTY code taken as United States:", us_code,
      f"({100*nat.max()/nat.sum():.1f}% of non-missing)")
    df["foreign_born"] = np.where(df.HHNATVTY.isna(), np.nan,
                                  (df.HHNATVTY != us_code).astype(float))
    # Mexico = the non-US birthplace most common among Hispanic householders
    hisp_nat = df.loc[df.hisp == 1, "HHNATVTY"].value_counts()
    hisp_nat = hisp_nat[hisp_nat.index != us_code]
    mex_code = hisp_nat.idxmax() if len(hisp_nat) else None
    P("HHNATVTY among Hispanic householders, top 10:")
    P(hisp_nat.head(10).to_string())
    P("code taken as Mexico:", mex_code, "n =",
      int((df.HHNATVTY == mex_code).sum()) if mex_code else 0)
    df["mex_born"] = (np.where(df.HHNATVTY.isna(), np.nan,
                               (df.HHNATVTY == mex_code).astype(float))
                      if mex_code else np.nan)

    df["inadequate"] = np.where(df.ADEQUACY.isna(), np.nan,
                                df.ADEQUACY.isin(["2","3"]).astype(float))
    df["sev_inadequate"] = np.where(df.ADEQUACY.isna(), np.nan,
                                    (df.ADEQUACY == "3").astype(float))
    BATTERY = [("NEARTRASH","trash_nearby"), ("NEARABAND","abandoned_nearby"),
               ("NEARBARCL","bars_on_windows"), ("NHQPCRIME","petty_crime"),
               ("NHQSCRIME","serious_crime"), ("NHQSCHOOL","school_problem"),
               ("NHQPUBTRN","transit_problem"), ("NHQRISK","disaster_risk")]
    for c, name in BATTERY:
        if c in df:
            df[name] = np.where(df[c].isna(), np.nan, (df[c] == "1").astype(float))
    df["nh_rating"] = df.RATINGNH
    df["unit_rating"] = df.RATINGHS
    df["owner"] = np.where(df.TENURE.isna(), np.nan, (df.TENURE == "1").astype(float))
    df["ppr"] = df.NUMPEOPLE/df.TOTROOMS.replace(0, np.nan)
    df["log_inc"] = np.log(df.HINCP.clip(lower=1000))
    df["yrb"] = pd.to_numeric(df.YRBUILT, errors="coerce")

    OUT = (["inadequate","sev_inadequate","nh_rating","unit_rating"]
           + [n for _, n in BATTERY if n in df])
    OUT = [o for o in OUT if df[o].notna().sum() > 1000]
    P("outcomes analysed:", OUT)

    def design(d, spec, key):
        X = pd.DataFrame({key: d[key].astype(float)})
        if spec >= 1:
            X["log_inc"] = d.log_inc
        if spec >= 2:
            for col, pre in [("TENURE","ten"), ("DIVISION","div"),
                             ("BLD","bld"), ("OMB13CBSA","cbsa")]:
                if col in d:
                    X = X.join(pd.get_dummies(d[col].fillna("Z"), prefix=pre,
                                              drop_first=True).astype(float))
            X["yrb"] = d.yrb
        if spec >= 3:
            X["ppr"] = d.ppr
            X["hh_size"] = d.NUMPEOPLE
        return sm.add_constant(X.astype(float))

    SPECS = {0: "raw",
             1: "+income",
             2: "+income, tenure, metro, division, structure age/type",
             3: "+persons per room, household size"}

    rows = []
    for key in ["hisp","foreign_born"] + (["mex_born"] if mex_code else []):
        for y in OUT:
            for spec, label in SPECS.items():
                d = df.dropna(subset=[y, key, "log_inc", "WEIGHT"]).copy()
                X = design(d, spec, key)
                keep = X.dropna().index
                d = d.loc[keep]; X = X.loc[keep]
                m = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit(cov_type="HC1")
                rows.append(dict(regressor=key, outcome=y, spec=label,
                                 beta=m.params[key], se_hc1=m.bse[key],
                                 t=m.tvalues[key], p=m.pvalues[key], n=int(m.nobs),
                                 mean_y=float(np.average(d[y].astype(float),
                                                         weights=d.WEIGHT))))
                P(f"  {key:13s} {y:18s} {label[:22]:24s} beta={m.params[key]:+.4f} "
                  f"t={m.tvalues[key]:6.2f} n={int(m.nobs)}")
    R = pd.DataFrame(rows)
    out["table18_ahs_regressions.csv"] = R.to_csv(index=False)

    # ---- SDR standard errors for the headline outcomes, fullest spec ----
    reps = [c for c in REPS if c in df]
    HEAD = [o for o in ["inadequate","trash_nearby","abandoned_nearby",
                        "bars_on_windows","nh_rating"] if o in OUT]
    rows3 = []
    for key in ["hisp"] + (["mex_born"] if mex_code else []):
        for y in HEAD:
            d = df.dropna(subset=[y, key, "log_inc", "WEIGHT"]).copy()
            X = design(d, 3, key)
            keep = X.dropna().index
            d = d.loc[keep]; X = X.loc[keep]
            b0 = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit().params[key]
            bs = []
            for rw in reps:
                w = d[rw]; ok = w.notna() & (w > 0)
                if ok.sum() < 1000: continue
                bs.append(sm.WLS(d.loc[ok, y].astype(float), X.loc[ok],
                                 weights=w[ok]).fit().params[key])
            bs = np.array(bs)
            se = float(np.sqrt(4.0/len(bs)*np.sum((bs - b0)**2))) if len(bs) else np.nan
            rows3.append(dict(regressor=key, outcome=y, beta=b0, se_sdr=se,
                              t_sdr=b0/se if se else np.nan, n_reps=len(bs),
                              n=int(len(d))))
            P(f"  SDR {key} {y}: beta={b0:+.4f} se={se:.4f} t={b0/se:.2f} "
              f"({len(bs)} reps)")
    out["table20_ahs_sdr_se.csv"] = pd.DataFrame(rows3).to_csv(index=False)

    # ---- the plain "equal income" comparison ----
    d = df.dropna(subset=["hisp","HINCP","WEIGHT"]).copy()
    d["inc_band"] = pd.cut(d.HINCP,
        [-1e9, 25000, 50000, 75000, 100000, 150000, 1e9],
        labels=["<25k","25-50k","50-75k","75-100k","100-150k","150k+"])
    recs = []
    for (band, h), s in d.groupby(["inc_band","hisp"], observed=True):
        row = {"inc_band": str(band), "hispanic": int(h), "n": len(s),
               "wgt_households": float(s.WEIGHT.sum()),
               "mean_income": float(np.average(s.HINCP, weights=s.WEIGHT))}
        for o in OUT:
            ok = s[o].notna()
            row[o] = (float(np.average(s.loc[ok, o].astype(float),
                                       weights=s.loc[ok, "WEIGHT"]))
                      if ok.sum() > 30 else np.nan)
        recs.append(row)
    B = pd.DataFrame(recs).sort_values(["inc_band","hispanic"])
    P("\n=== weighted means by income band and Hispanic origin ===")
    P(B.round(3).to_string(index=False))
    out["table21_ahs_income_bands.csv"] = B.to_csv(index=False)

    out["ahs_run_log.txt"] = "\n".join(log)
    return out


@app.local_entrypoint()
def main():
    import pathlib
    res = run.remote()
    d = pathlib.Path(__file__).parent
    for name, body in res.items():
        (d/name).write_text(body)
        print("wrote", d/name, len(body), "bytes")

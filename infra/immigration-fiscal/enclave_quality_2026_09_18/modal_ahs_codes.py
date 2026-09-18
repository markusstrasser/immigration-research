"""Establish the code order of the AHS NEAR* neighborhood items empirically, then
re-run the H1 regressions with correctly-signed outcomes.

Why this run exists. The 2023 AHS mini codebook describes NEARTRASH as the
"frequency of trash, litter, or junk ... within 1/2 block", NEARABAND as the
"number of buildings that are abandoned or vandalized", and NEARBARCL as the
"number of buildings with bars on windows". None is a yes/no item, so an `== 1`
indicator cannot be assumed to mean "problem present". Category order is
therefore determined from the data: for each category, the weighted mean of
RATINGNH (the respondent's own 1-10 rating of the neighborhood, where 10 is
best) and the weighted poverty share. The worst-rated category is the severe one.

The NHQ* items are agree/disagree, and their polarity differs by item:
NHQPCRIME "this neighborhood has a lot of petty crime" and NHQRISK "at high risk
for floods" are negative, while NHQSCHOOL "has good schools" and NHQPUBTRN "has
good bus, subway, or commuter train service" are positive. Outcomes below are
named accordingly.

Run:  modal run infra/immigration-fiscal/enclave_quality_2026_09_18/modal_ahs_codes.py
"""
import modal

app = modal.App("ahs-enclave-codes")
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("pandas>=2", "numpy>=2", "statsmodels", "requests"))

BASE = "https://www2.census.gov/programs-surveys/ahs/2023/"
V10 = BASE + "AHS%202023%20National%20PUF%20v1.0%20Flat%20CSV.zip"
V11 = BASE + "AHS%202023%20National%20PUF%20v1.1%20Flat%20CSV.zip"


@app.function(image=image, timeout=3600, memory=32768, cpu=8)
def run():
    import io, zipfile, requests
    import numpy as np, pandas as pd, statsmodels.api as sm

    out, log = {}, []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); log.append(s)

    CORE = ["WEIGHT","HHSPAN","HHNATVTY","HINCP","TENURE","ADEQUACY","RATINGNH",
            "RATINGHS","NEARTRASH","NEARABAND","NEARBARCL","NHQPCRIME",
            "NHQSCRIME","NHQSCHOOL","NHQPUBTRN","NHQRISK","OMB13CBSA","DIVISION",
            "BLD","YRBUILT","NUMPEOPLE","TOTROOMS","PERPOVLVL"]

    def load(url, tag):
        r = requests.get(url, timeout=2400); r.raise_for_status()
        P(f"{tag}: downloaded {len(r.content)} bytes")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        t = max((n for n in z.namelist() if n.lower().endswith(".csv")),
                key=lambda n: z.getinfo(n).file_size)
        h = pd.read_csv(z.open(t), nrows=0, dtype=str)
        P(f"{tag}: {t}, {len(h.columns)} columns")
        d = pd.read_csv(z.open(t), usecols=[c for c in CORE if c in h.columns],
                        dtype=str, low_memory=False)
        P(f"{tag}: {len(d)} households")
        for c in d.columns:
            d[c] = (d[c].astype(str).str.strip().str.strip("'").str.strip('"')
                     .replace({"": np.nan, "-6": np.nan, "-9": np.nan,
                               "M": np.nan, "N": np.nan, "B": np.nan,
                               ".": np.nan, "nan": np.nan}))
        for c in ["WEIGHT","HINCP","RATINGNH","RATINGHS","NUMPEOPLE","TOTROOMS",
                  "PERPOVLVL"]:
            if c in d: d[c] = pd.to_numeric(d[c], errors="coerce")
        return d

    df = load(V10, "v1.0")
    try:
        d11 = load(V11, "v1.1")
        comp = []
        for c in ["NEARTRASH","NEARABAND","NEARBARCL","ADEQUACY","HHSPAN",
                  "RATINGNH","NHQPCRIME"]:
            if c in df and c in d11:
                a = df[c].value_counts(dropna=False).sort_index()
                b = d11[c].value_counts(dropna=False).sort_index()
                same = a.equals(b)
                comp.append(dict(variable=c, v10_rows=len(df), v11_rows=len(d11),
                                 distributions_identical=bool(same)))
                P(f"v1.0 vs v1.1 {c}: identical={same}")
        out["table18b_ahs_version_check.csv"] = pd.DataFrame(comp).to_csv(index=False)
    except Exception as e:
        P("v1.1 comparison failed:", repr(e))

    # ---- category ordering, from the respondent's own neighborhood rating ----
    rows = []
    for c in ["NEARTRASH","NEARABAND","NEARBARCL","ADEQUACY","NHQPCRIME",
              "NHQSCRIME","NHQSCHOOL","NHQPUBTRN","NHQRISK"]:
        if c not in df: continue
        for val, s in df.dropna(subset=["WEIGHT"]).groupby(df[c], dropna=False):
            ok = s.RATINGNH.notna()
            pv = s.PERPOVLVL.notna()
            rows.append(dict(
                variable=c, code=str(val), n=len(s),
                wgt_share_pct=round(100*s.WEIGHT.sum()/df.WEIGHT.sum(), 2),
                mean_nh_rating=(round(float(np.average(s.loc[ok, "RATINGNH"],
                    weights=s.loc[ok, "WEIGHT"])), 3) if ok.sum() > 30 else None),
                mean_pct_of_poverty=(round(float(np.average(s.loc[pv, "PERPOVLVL"],
                    weights=s.loc[pv, "WEIGHT"])), 1) if pv.sum() > 30 else None)))
    C = pd.DataFrame(rows)
    P("\n=== category ordering diagnostics "
      "(lower mean_nh_rating = worse neighborhood) ===")
    P(C.to_string(index=False))
    out["table18c_ahs_category_ordering.csv"] = C.to_csv(index=False)

    # severe category = the one with the lowest weighted mean neighborhood rating
    severe = {}
    for c in ["NEARTRASH","NEARABAND","NEARBARCL"]:
        sub = C[(C.variable == c) & C.mean_nh_rating.notna() & (C.n > 100)]
        if len(sub):
            severe[c] = sub.loc[sub.mean_nh_rating.idxmin(), "code"]
    P("\nsevere category by lowest neighborhood rating:", severe)

    # ---- recodes with verified polarity ----
    df["hisp"] = np.where(df.HHSPAN.isna(), np.nan, (df.HHSPAN == "1").astype(float))
    nat = df.HHNATVTY.value_counts(); us = nat.idxmax()
    df["foreign_born"] = np.where(df.HHNATVTY.isna(), np.nan,
                                  (df.HHNATVTY != us).astype(float))
    hn = df.loc[df.hisp == 1, "HHNATVTY"].value_counts()
    hn = hn[hn.index != us]; mex = hn.idxmax()
    df["mex_born"] = np.where(df.HHNATVTY.isna(), np.nan,
                              (df.HHNATVTY == mex).astype(float))
    P("US code:", us, " Mexico code:", mex, " n Mexico-born:",
      int((df.HHNATVTY == mex).sum()))

    df["inadequate"] = np.where(df.ADEQUACY.isna(), np.nan,
                                df.ADEQUACY.isin(["2","3"]).astype(float))
    for c, name in [("NEARTRASH","trash_severe"), ("NEARABAND","abandoned_severe"),
                    ("NEARBARCL","bars_severe")]:
        if c in severe:
            df[name] = np.where(df[c].isna(), np.nan,
                                (df[c] == severe[c]).astype(float))
    # any non-modal (i.e. any presence) as a second, looser coding
    for c, name in [("NEARTRASH","trash_any"), ("NEARABAND","abandoned_any"),
                    ("NEARBARCL","bars_any")]:
        if c in df:
            modal_code = df[c].value_counts().idxmax()
            df[name] = np.where(df[c].isna(), np.nan,
                                (df[c] != modal_code).astype(float))
    df["agrees_lot_petty_crime"] = np.where(df.NHQPCRIME.isna(), np.nan,
                                            (df.NHQPCRIME == "1").astype(float))
    df["agrees_lot_serious_crime"] = np.where(df.NHQSCRIME.isna(), np.nan,
                                              (df.NHQSCRIME == "1").astype(float))
    df["agrees_good_schools"] = np.where(df.NHQSCHOOL.isna(), np.nan,
                                         (df.NHQSCHOOL == "1").astype(float))
    df["agrees_good_transit"] = np.where(df.NHQPUBTRN.isna(), np.nan,
                                         (df.NHQPUBTRN == "1").astype(float))
    df["agrees_high_disaster_risk"] = np.where(df.NHQRISK.isna(), np.nan,
                                               (df.NHQRISK == "1").astype(float))
    df["nh_rating"] = df.RATINGNH
    df["ppr"] = df.NUMPEOPLE/df.TOTROOMS.replace(0, np.nan)
    df["log_inc"] = np.log(df.HINCP.clip(lower=1000))
    df["yrb"] = pd.to_numeric(df.YRBUILT, errors="coerce")

    OUT = [o for o in ["inadequate","nh_rating","trash_severe","trash_any",
                       "abandoned_severe","abandoned_any","bars_severe","bars_any",
                       "agrees_lot_petty_crime","agrees_lot_serious_crime",
                       "agrees_good_schools","agrees_good_transit",
                       "agrees_high_disaster_risk"]
           if o in df and df[o].notna().sum() > 1000]
    P("outcomes:", OUT)

    def design(d, spec, key):
        X = pd.DataFrame({key: d[key].astype(float)})
        if spec >= 1: X["log_inc"] = d.log_inc
        if spec >= 2:
            for col, pre in [("TENURE","ten"), ("DIVISION","div"),
                             ("BLD","bld"), ("OMB13CBSA","cbsa")]:
                X = X.join(pd.get_dummies(d[col].fillna("Z"), prefix=pre,
                                          drop_first=True).astype(float))
            X["yrb"] = d.yrb
        if spec >= 3:
            X["ppr"] = d.ppr; X["hh_size"] = d.NUMPEOPLE
        return sm.add_constant(X.astype(float))

    SPECS = {0: "raw", 1: "+income",
             2: "+income, tenure, metro, division, structure age/type",
             3: "+persons per room, household size"}
    res = []
    for key in ["hisp","foreign_born","mex_born"]:
        for y in OUT:
            for spec, label in SPECS.items():
                d = df.dropna(subset=[y, key, "log_inc", "WEIGHT"]).copy()
                X = design(d, spec, key); keep = X.dropna().index
                d = d.loc[keep]; X = X.loc[keep]
                m = sm.WLS(d[y].astype(float), X, weights=d.WEIGHT).fit(cov_type="HC1")
                res.append(dict(regressor=key, outcome=y, spec=label,
                                beta=m.params[key], se_hc1=m.bse[key],
                                t=m.tvalues[key], p=m.pvalues[key], n=int(m.nobs),
                                mean_y=float(np.average(d[y].astype(float),
                                                        weights=d.WEIGHT))))
                if spec in (1, 3):
                    P(f"  {key:13s} {y:26s} {label[:20]:22s} "
                      f"beta={m.params[key]:+.4f} t={m.tvalues[key]:6.2f}")
    R = pd.DataFrame(res)
    out["table19_ahs_regressions_signed.csv"] = R.to_csv(index=False)
    out["ahs_codes_log.txt"] = "\n".join(log)
    return out


@app.local_entrypoint()
def main():
    import pathlib
    res = run.remote()
    d = pathlib.Path(__file__).parent
    for name, body in res.items():
        (d/name).write_text(body); print("wrote", d/name, len(body), "bytes")

"""ECLS-K:2011 kindergarten classroom ELL association. Not a 1998 replication.

Child birthplace (P2BTHPLC/P2CNTRYB) is blank and teacher IDs are all -2, matching
the dataset card. Internal school IDs, Hispanic identity, home language and
teacher-reported ELL counts are populated. Target is English-home non-Hispanic
white children (X12LANGST=2, X_HISP_R=2, X_RACETHP_R=1). That is not the 1998
US-born filter.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "_cache" / "ecls_k2011"
OUT = ROOT / "derived"
OUT.mkdir(parents=True, exist_ok=True)

probe = json.loads((CACHE / "probe.json").read_text())
df = pd.read_parquet(CACHE / "selected.parquet")
if len(df) != probe["rows"] or df.CHILDID.duplicated().any():
    raise ValueError("Extracted file does not match probe.json")


def session_col(am, pm, full):
    out = pd.Series(np.nan, index=df.index, dtype=float)
    use_d = df["A1FULDAY"] == 1
    use_a = (~use_d) & (df["A1HALFAM"] == 1)
    use_p = (~use_d) & (~use_a) & (df["A1HALFPM"] == 1)
    out = out.mask(use_a, pd.to_numeric(df[am], errors="coerce"))
    out = out.mask(use_p, pd.to_numeric(df[pm], errors="coerce"))
    out = out.mask(use_d, pd.to_numeric(df[full], errors="coerce"))
    return out.where(out >= 0)


df["ell"] = session_col("A1ANMELL", "A1PNMELL", "A1DNMELL")
df["size"] = session_col("A1ATOTRA", "A1PTOTRA", "A1DTOTRA")
df["ell"] = df["ell"].where(df["ell"] <= df["size"])
df["ell10pp"] = df["ell"] / df["size"] * 10
df["read1"] = df["X1RTHETK5"].where(df["X1RTHETK5"] > -8)
df["read2"] = df["X2RTHETK5"].where(df["X2RTHETK5"] > -8)
df["math1"] = df["X1MTHETK5"].where(df["X1MTHETK5"] > -8)
df["math2"] = df["X2MTHETK5"].where(df["X2MTHETK5"] > -8)
df["weight"] = df["W1C0"].where(df["W1C0"] > 0)
df["school"] = df["S1_ID"].astype(str).where(
    df["S1_ID"].astype(str).str.fullmatch(r"\d+")
    & ~df["S1_ID"].astype(str).str.startswith("999")
)
# X12LANGST: 2 is the modal code (12,926 of 16,045). Parallel to 1998 WKLANGST=2 English.
df["english_home"] = (df["X12LANGST"] == 2).where(df["X12LANGST"] >= 0)
df["nh_white"] = ((df["X_HISP_R"] == 2) & (df["X_RACETHP_R"] == 1)).where(
    (df["X_HISP_R"] >= 0) & (df["X_RACETHP_R"] >= 0)
)

coverage_rows = [{"field": name, **spec} for name, spec in probe["coverage"].items()]
pd.DataFrame(coverage_rows).to_csv(OUT / "ecls_k2011_coverage.csv", index=False)

n_birth = int((df["P2BTHPLC"] >= 0).sum())
n_country = int((df["P2CNTRYB"] >= 0).sum())
n_teacher = int((df["T1_ID"].astype(str) != "-2").sum())
target = df["english_home"].eq(True) & df["nh_white"].eq(True)
work = df.loc[target].copy()
summary = {
    "rows": int(len(df)),
    "p2bthplc_nonneg": n_birth,
    "p2cntryb_nonneg": n_country,
    "t1_id_not_suppressed": n_teacher,
    "s1_id_usable": int(df["school"].notna().sum()),
    "ell_nonneg": int(df["ell"].notna().sum()),
    "target": "english-home non-Hispanic white; birthplace suppressed so not the 1998 US-born cut",
    "target_n": int(len(work)),
    "target_with_ell_scores": int(
        work[["ell10pp", "read2", "read1", "weight", "school"]].notna().all(axis=1).sum()
    ),
}


def fit(outcome, baseline, label):
    cols = ["ell10pp", baseline, "X1KAGE_R", "X12SESL", "X_CHSEX_R"]
    use = work.dropna(subset=cols + [outcome, "weight", "school"]).copy()
    use = use[use["weight"] > 0]
    use = use[use.groupby("school")["school"].transform("size") > 1]
    if len(use) < 200:
        return {"label": label, "n": int(len(use)), "status": "too_few"}
    w = use["weight"].to_numpy(float)
    w = w / w.mean()
    matrix = use[[outcome, "ell10pp", baseline, "X1KAGE_R", "X12SESL", "X_CHSEX_R"]].astype(float)
    weighted = matrix.mul(w, axis=0)
    sums = weighted.groupby(use["school"]).transform("sum")
    den = pd.Series(w, index=use.index).groupby(use["school"]).transform("sum")
    matrix = matrix - sums.div(den, axis=0)
    y = matrix.iloc[:, 0].to_numpy()
    x = matrix.iloc[:, 1:].to_numpy()
    root = np.sqrt(w)
    xw, yw = x * root[:, None], y * root
    bread = np.linalg.inv(xw.T @ xw)
    beta = np.linalg.lstsq(xw, yw, rcond=None)[0]
    residual = y - x @ beta
    scores = x * (w * residual)[:, None]
    clusters = pd.DataFrame(scores).groupby(use["school"].to_numpy()).sum().to_numpy()
    groups = len(clusters)
    rank = xw.shape[1] + groups
    correction = groups / (groups - 1) * (len(use) - 1) / (len(use) - rank)
    covariance = bread @ (clusters.T @ clusters) @ bread * correction
    se = float(np.sqrt(covariance[0, 0]))
    coef = float(beta[0])
    return {
        "label": label,
        "n": int(len(use)),
        "schools": int(groups),
        "ell10pp": coef,
        "se": se,
        "lo": coef - 1.96 * se,
        "hi": coef + 1.96 * se,
        "units": "IRT theta points per 10pp classroom ELL",
    }


models = [
    fit("read2", "read1", "read_spring_given_fall"),
    fit("math2", "math1", "math_spring_given_fall"),
]
pd.DataFrame(models).to_csv(OUT / "ecls_k2011_models.csv", index=False)
summary["models"] = models
(OUT / "ecls_k2011_summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))

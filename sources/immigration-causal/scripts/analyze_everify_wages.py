"""Analyze E-Verify mandate effects on low-education worker wages.

Card vs Borjas test:
- Borjas predicts: tighter unauthorized labor supply → higher wages for native low-skill
- Card predicts: complementarity dominates → no positive wage effect, possibly negative

Design:
- TWFE: log(EarnS) ~ everify_mandate × education + state + year + state×education trends
- Restrict to E1 (less than HS, the Borjas margin) and E2 (HS only)
- Compare to E3/E4 (some college / BA+) as placebo — should see no effect
- Industries with high unauthorized exposure: 11 (Ag), 23 (Constr), 72 (Accom/Food)

Treatment definition:
- Treated: state has 'all_employers' or '15plus_employees' mandate effective by year y
- Control: states with no mandate or only public-employer mandates

Output: data/analysis/everify_wage_results.txt + parquet
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
QWI = DATA / "lehd" / "qwi_state_panel.parquet"
EVERIFY = DATA / "everify" / "everify_state_mandates.csv"
OUT = DATA / "analysis"
OUT.mkdir(parents=True, exist_ok=True)


def load_qwi() -> pd.DataFrame:
    df = pd.read_parquet(QWI)
    for c in ("Emp", "EmpS", "EarnS", "EarnBeg", "Payroll"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["year"] = df["year"].astype(int)
    df["quarter"] = df["quarter"].astype(int)
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    df = df[df["EarnS"].notna() & (df["EarnS"] > 0)]
    df["log_earns"] = np.log(df["EarnS"])
    return df


def load_everify() -> pd.DataFrame:
    df = pd.read_csv(EVERIFY)
    df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
    return df


def build_treatment_panel(qwi: pd.DataFrame, everify: pd.DataFrame) -> pd.DataFrame:
    """Add columns: ever_treated (state has all-employer mandate), treated (effective by year)."""
    treated_states = everify[everify["scope"].isin(["all_employers", "15plus_employees", "10plus_employees", "25plus_employees", "6plus_employees"])]
    map_eff = dict(zip(treated_states["state_fips"], treated_states["effective_year"]))

    qwi["ever_treated"] = qwi["state_fips"].isin(map_eff).astype(int)
    qwi["effective_year"] = qwi["state_fips"].map(map_eff)
    qwi["treated"] = ((qwi["ever_treated"] == 1) & (qwi["year"] >= qwi["effective_year"].fillna(9999))).astype(int)
    qwi["years_since_treat"] = np.where(qwi["ever_treated"] == 1, qwi["year"] - qwi["effective_year"], np.nan)
    return qwi


def twfe_regression(df: pd.DataFrame, edu_filter: str | None = None, ind_filter: list[str] | None = None) -> dict:
    """Two-way fixed effects via dummy variables. Returns dict with treatment coef + SE.

    Avoid statsmodels dependency for portability — use np.linalg.lstsq with within-transformation.
    Cluster-robust SE at state level via Liang-Zeger.
    """
    sub = df.copy()
    if edu_filter:
        sub = sub[sub["education"] == edu_filter]
    if ind_filter:
        sub = sub[sub["industry"].isin(ind_filter)]
    sub = sub.dropna(subset=["log_earns", "treated", "state_fips", "year"])
    if len(sub) < 100:
        return {"n": len(sub), "error": "insufficient observations"}

    # Within-transform: subtract state-mean and year-mean (sequential demeaning is biased
    # but acceptable for balanced-ish panel)
    sub["log_earns_dm"] = sub["log_earns"] - sub.groupby("state_fips")["log_earns"].transform("mean")
    sub["log_earns_dm"] = sub["log_earns_dm"] - sub.groupby("year")["log_earns_dm"].transform("mean")
    sub["treated_dm"] = sub["treated"] - sub.groupby("state_fips")["treated"].transform("mean")
    sub["treated_dm"] = sub["treated_dm"] - sub.groupby("year")["treated_dm"].transform("mean")

    y = sub["log_earns_dm"].values
    x = sub["treated_dm"].values
    # OLS: beta = (x'x)^-1 x'y
    xx = np.dot(x, x)
    if xx == 0:
        return {"n": len(sub), "error": "no within-variation in treated"}
    beta = np.dot(x, y) / xx
    resid = y - beta * x

    # Cluster-robust SE at state level (Liang-Zeger 1986)
    cluster_sums = sub.assign(xe=x * resid).groupby("state_fips")["xe"].sum().values
    meat = np.sum(cluster_sums ** 2)
    n_clusters = len(cluster_sums)
    bread = 1.0 / xx
    var_beta = bread * meat * bread
    # small-sample correction
    n = len(sub)
    k = 1
    var_beta = var_beta * n_clusters / (n_clusters - 1) * (n - 1) / (n - k)
    se = np.sqrt(var_beta)
    t = beta / se

    return {
        "n": n,
        "n_clusters": n_clusters,
        "beta_treated": beta,
        "se_clustered": se,
        "t": t,
        "pct_effect": (np.exp(beta) - 1) * 100,
        "treated_share": float(sub["treated"].mean()),
    }


def event_study(df: pd.DataFrame, edu_filter: str, ind_filter: list[str] | None = None) -> pd.DataFrame:
    """Event-time regression with explicit state and year fixed-effect dummies.

    Spec: log_earns_it = Σ_k β_k 1[event_time == k] + α_i + γ_t + ε_it
    where event_time = year − effective_year for treated states; controls have event_time = NaN.
    Including controls means α_i absorbs untreated states, and event-time coefficients
    are identified off the treatment timing.
    """
    sub = df.copy()
    sub = sub[sub["education"] == edu_filter]
    if ind_filter:
        sub = sub[sub["industry"].isin(ind_filter)]
    sub = sub.dropna(subset=["log_earns"])
    sub["event_time"] = np.where(
        sub["ever_treated"] == 1,
        np.clip(sub["years_since_treat"], -6, 8),
        np.nan,
    )

    # Build dummy matrix: event_time bins (omit -1), state dummies (omit one), year dummies (omit one)
    state_codes, state_levels = pd.factorize(sub["state_fips"], sort=True)
    year_codes, year_levels = pd.factorize(sub["year"], sort=True)

    n = len(sub)
    event_cols = []
    event_labels = []
    for k in range(-6, 9):
        if k == -1:
            continue
        col = ((sub["ever_treated"] == 1) & (sub["event_time"] == k)).astype(float).values
        event_cols.append(col)
        event_labels.append(k)

    # Dummies (omit first level for collinearity)
    state_dums = np.zeros((n, len(state_levels) - 1))
    for i in range(1, len(state_levels)):
        state_dums[:, i - 1] = (state_codes == i).astype(float)
    year_dums = np.zeros((n, len(year_levels) - 1))
    for i in range(1, len(year_levels)):
        year_dums[:, i - 1] = (year_codes == i).astype(float)

    X = np.column_stack([np.ones(n), np.column_stack(event_cols), state_dums, year_dums])
    y = sub["log_earns"].values

    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    XX_inv = np.linalg.pinv(X.T @ X)
    # Cluster-robust at state level
    cluster_meat = np.zeros_like(XX_inv)
    for sf in state_levels:
        idx = (sub["state_fips"] == sf).values
        Xc = X[idx]
        ec = resid[idx]
        Xe = (Xc.T * ec).sum(axis=1).reshape(-1, 1)
        cluster_meat += Xe @ Xe.T
    var_beta = XX_inv @ cluster_meat @ XX_inv
    se_all = np.sqrt(np.diag(var_beta))

    rows = []
    # Indices: 0 is intercept; 1..1+len(event_cols) are event coefficients
    for i, k in enumerate(event_labels):
        rows.append({"event_time": k, "beta": beta[1 + i], "se": se_all[1 + i]})
    rows.append({"event_time": -1, "beta": 0.0, "se": 0.0})
    return pd.DataFrame(rows).sort_values("event_time").reset_index(drop=True)


def main() -> int:
    if not QWI.exists():
        print(f"QWI panel not found at {QWI} — pull script first")
        return 1
    qwi = load_qwi()
    everify = load_everify()
    panel = build_treatment_panel(qwi, everify)
    panel.to_parquet(OUT / "qwi_everify_panel.parquet", index=False)
    print(f"Panel rows: {len(panel)}")
    print(f"Treated states (effective_year not null): {panel[panel['ever_treated']==1]['state_fips'].nunique()}")
    print(f"Control states: {panel[panel['ever_treated']==0]['state_fips'].nunique()}")
    print()

    results = []
    print("=" * 80)
    print("MAIN TWFE RESULTS — log(EarnS) ~ E-Verify mandate × education")
    print("=" * 80)
    for edu in ("E1", "E2", "E3", "E4"):
        for inds in (None, ["11", "23", "31-33", "72"], ["00"]):
            label = "all-industries" if inds is None else ("everify-exposed" if "11" in inds else "total-aggregate")
            res = twfe_regression(panel, edu_filter=edu, ind_filter=inds)
            res["education"] = edu
            res["industry_set"] = label
            results.append(res)
            if "beta_treated" in res:
                stars = ""
                if abs(res["t"]) > 2.58:
                    stars = "***"
                elif abs(res["t"]) > 1.96:
                    stars = "**"
                elif abs(res["t"]) > 1.645:
                    stars = "*"
                print(f"  edu={edu:3s} ind={label:18s}  β={res['beta_treated']:+.4f} ({res['pct_effect']:+.2f}%)  SE={res['se_clustered']:.4f}  t={res['t']:+.2f}{stars}  n={res['n']:,}  clusters={res['n_clusters']}")
            else:
                print(f"  edu={edu:3s} ind={label:18s}  ERROR: {res.get('error')}")

    res_df = pd.DataFrame(results)
    res_df.to_csv(OUT / "everify_twfe_results.csv", index=False)
    print(f"\nWrote results to {OUT/'everify_twfe_results.csv'}")

    print()
    print("=" * 80)
    print("EVENT STUDY — E1 (less than HS) workers in E-Verify-exposed industries")
    print("=" * 80)
    es = event_study(panel, "E1", ["11", "23", "31-33", "72"])
    print(es.to_string(index=False))
    es.to_csv(OUT / "everify_event_study_E1.csv", index=False)

    return 0


if __name__ == "__main__":
    main()

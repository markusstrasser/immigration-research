"""Sanctuary state policies as DiD on QWI wages.

Two-sided design: pro-sanctuary states (CA, IL, OR, etc) vs anti-sanctuary states
(TX SB 4, FL SB 168, AL HB 56, AZ SB 1070, etc.). E-Verify states already in
prior analysis — sanctuary axis is partially correlated but distinct.

Hypothesis: If anti-sanctuary policies operate by reducing unauthorized labor
supply via fear of LE-ICE cooperation, they should produce wage effects
similar to E-Verify (Borjas) — or null (Card). Sanctuary policies should do
the opposite or null.

Three contrasts:
1. Sanctuary onset DiD: pro-sanctuary states vs all others, post-2017 vs pre
2. Anti-sanctuary onset DiD: anti-sanctuary states vs all others, post-policy
3. Pro vs Anti contrast: drop neutral states, compare sanctuary vs anti-sanctuary
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
QWI = DATA / "lehd" / "qwi_state_panel.parquet"
SANCTUARY = DATA / "sanctuary" / "sanctuary_state_panel.csv"
OUT = DATA / "analysis"
OUT.mkdir(parents=True, exist_ok=True)


def load() -> pd.DataFrame:
    qwi = pd.read_parquet(QWI)
    qwi["state_fips"] = qwi["state"].astype(str).str.zfill(2)
    qwi["year"] = qwi["year"].astype(int)
    qwi["EarnS"] = pd.to_numeric(qwi["EarnS"], errors="coerce")
    qwi["EmpS"] = pd.to_numeric(qwi["EmpS"], errors="coerce")
    qwi = qwi[qwi["EarnS"].notna() & (qwi["EarnS"] > 0)]
    qwi["log_earns"] = np.log(qwi["EarnS"])

    sanc = pd.read_csv(SANCTUARY)
    sanc["state_fips"] = sanc["state_fips"].astype(str).str.zfill(2)
    sanc["effective_year"] = pd.to_datetime(sanc["effective_date"]).dt.year

    sanctuary_states = sanc[sanc["policy_type"] == "sanctuary"].set_index("state_fips")["effective_year"]
    anti_states = sanc[sanc["policy_type"] == "anti_sanctuary"].set_index("state_fips")["effective_year"]

    qwi["sanctuary_year"] = qwi["state_fips"].map(sanctuary_states)
    qwi["anti_year"] = qwi["state_fips"].map(anti_states)
    qwi["is_sanctuary"] = qwi["sanctuary_year"].notna().astype(int)
    qwi["is_anti"] = qwi["anti_year"].notna().astype(int)
    qwi["sanctuary_treated"] = ((qwi["sanctuary_year"].notna()) & (qwi["year"] >= qwi["sanctuary_year"].fillna(9999))).astype(int)
    qwi["anti_treated"] = ((qwi["anti_year"].notna()) & (qwi["year"] >= qwi["anti_year"].fillna(9999))).astype(int)
    return qwi


def twfe(df: pd.DataFrame, treat_col: str, edu: str, ind_subset: list[str] | None) -> dict:
    sub = df[df["education"] == edu].copy()
    if ind_subset:
        sub = sub[sub["industry"].isin(ind_subset)]
    sub = sub.dropna(subset=["log_earns", treat_col, "state_fips", "year"])
    if len(sub) < 100:
        return {"error": "n<100"}
    sub["y_dm"] = sub["log_earns"] - sub.groupby("state_fips")["log_earns"].transform("mean")
    sub["y_dm"] = sub["y_dm"] - sub.groupby("year")["y_dm"].transform("mean")
    sub["x_dm"] = sub[treat_col] - sub.groupby("state_fips")[treat_col].transform("mean")
    sub["x_dm"] = sub["x_dm"] - sub.groupby("year")["x_dm"].transform("mean")
    y = sub["y_dm"].values
    x = sub["x_dm"].values
    xx = (x * x).sum()
    if xx == 0:
        return {"error": "no within-variation"}
    beta = (x * y).sum() / xx
    resid = y - beta * x
    cluster_sums = sub.assign(xe=x * resid).groupby("state_fips")["xe"].sum().values
    meat = (cluster_sums ** 2).sum()
    n_c = len(cluster_sums)
    var_beta = (1 / xx) * meat * (1 / xx) * n_c / max(n_c - 1, 1)
    se = np.sqrt(var_beta)
    return {"beta": beta, "se": se, "t": beta / se, "pct": (np.exp(beta) - 1) * 100, "n": len(sub), "n_clusters": n_c}


def main():
    df = load()
    print(f"Loaded {len(df):,} QWI rows")
    print(f"Sanctuary states: {df[df['is_sanctuary']==1]['state_fips'].nunique()}")
    print(f"Anti-sanctuary states: {df[df['is_anti']==1]['state_fips'].nunique()}")
    print()

    print("=" * 80)
    print("SANCTUARY DiD: log(EarnS) ~ sanctuary_treated × education")
    print("=" * 80)
    rows = []
    for treat_col in ["sanctuary_treated", "anti_treated"]:
        for edu in ("E1", "E2", "E3", "E4"):
            for inds_label, inds in [("everify-exposed", ["11", "23", "31-33", "72"]), ("all-non-agg", ["11", "23", "31-33", "44-45", "56", "62", "72", "81"])]:
                res = twfe(df, treat_col, edu, inds)
                if "error" in res:
                    continue
                stars = "***" if abs(res["t"]) > 2.58 else ("**" if abs(res["t"]) > 1.96 else ("*" if abs(res["t"]) > 1.645 else ""))
                print(f"  {treat_col:<18s} edu={edu} ind={inds_label:18s}  β={res['beta']:+.4f} ({res['pct']:+.2f}%)  SE={res['se']:.4f}  t={res['t']:+.2f}{stars}  n={res['n']:,}")
                res.update({"treat": treat_col, "edu": edu, "ind": inds_label})
                rows.append(res)
            print()

    pd.DataFrame(rows).to_csv(OUT / "sanctuary_twfe_results.csv", index=False)


if __name__ == "__main__":
    main()

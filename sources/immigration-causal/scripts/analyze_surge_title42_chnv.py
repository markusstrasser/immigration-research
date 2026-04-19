"""Title 42 lift event study + CHNV nationality-DiD on OHSS monthly encounters.

Title 42 lift: 2023-05-11. Treatment is post-May-2023 dummy.
CHNV parole start: 2023-01-05 (full 4-nationality program). Treatment is post-Jan-2023
dummy applied to Cuba+Haiti+Nicaragua+Venezuela; control is Mexico+Guatemala+
Honduras+El Salvador.

Outputs:
- data/analysis/title42_event_study.csv
- data/analysis/chnv_nationality_did.csv
- data/analysis/surge_summary.json
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
ENC = DATA / "cbp" / "swb_encounters_by_citizenship_monthly.parquet"
CHNV = DATA / "cbp" / "chnv_paroles_monthly.parquet"
OUT = DATA / "analysis"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    enc = pd.read_parquet(ENC)
    enc = enc.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    print(f"Encounter panel: {len(enc)} months, {enc['date'].min().date()} to {enc['date'].max().date()}")

    # === 1. TITLE 42 LIFT EVENT STUDY ===
    print("\n" + "=" * 70)
    print("TITLE 42 LIFT EVENT STUDY (2023-05-11)")
    print("=" * 70)
    enc["since_lift"] = (enc["date"] - pd.Timestamp("2023-05-01")).dt.days // 30
    enc["post_lift"] = (enc["date"] >= pd.Timestamp("2023-06-01")).astype(int)

    # Print monthly Total around lift
    window = enc[(enc["date"] >= "2022-11-01") & (enc["date"] <= "2024-06-01")].copy()
    print("\n  Monthly SWB total encounters around Title 42 lift (May 11 2023):")
    for _, r in window.iterrows():
        marker = " <-- TITLE 42 LIFT" if r["date"].strftime("%Y-%m") == "2023-05" else ""
        print(f"    {r['date'].strftime('%Y-%m')}: {int(r['Total']):>7,d} total, MEX {int(r['Mexico']):>6,d}, VEN {int(r['Venezuela']):>6,d}, CUB {int(r['Cuba']):>5,d}, HTI {int(r['Haiti']):>5,d}{marker}")

    # Pre/post 6-month means
    pre = enc[(enc["date"] >= "2022-11-01") & (enc["date"] <= "2023-04-01")]
    post = enc[(enc["date"] >= "2023-06-01") & (enc["date"] <= "2023-11-01")]
    print(f"\n  Pre-lift 6mo mean (Nov22-Apr23): {pre['Total'].mean():>8,.0f} total/month")
    print(f"  Post-lift 6mo mean (Jun23-Nov23): {post['Total'].mean():>8,.0f} total/month")
    print(f"  Change: {post['Total'].mean() - pre['Total'].mean():+,.0f} ({100*(post['Total'].mean()/pre['Total'].mean() - 1):+.1f}%)")

    # 12mo each side
    pre12 = enc[(enc["date"] >= "2022-05-01") & (enc["date"] <= "2023-04-01")]
    post12 = enc[(enc["date"] >= "2023-06-01") & (enc["date"] <= "2024-05-01")]
    print(f"\n  Pre-lift 12mo mean: {pre12['Total'].mean():>8,.0f} total/month")
    print(f"  Post-lift 12mo mean: {post12['Total'].mean():>8,.0f} total/month")
    print(f"  Change: {post12['Total'].mean() - pre12['Total'].mean():+,.0f} ({100*(post12['Total'].mean()/pre12['Total'].mean() - 1):+.1f}%)")

    # The May 2023 spike pattern (anticipation + crash)
    print(f"\n  Anticipation: April 2023 = {int(enc[enc['date']=='2023-04-01']['Total'].iloc[0]):,}")
    print(f"                May 2023 = {int(enc[enc['date']=='2023-05-01']['Total'].iloc[0]):,}  <-- pre-lift surge anticipation")
    print(f"                June 2023 = {int(enc[enc['date']=='2023-06-01']['Total'].iloc[0]):,}  <-- post-lift crash")

    # Save event study summary
    es = enc[(enc["date"] >= "2022-05-01") & (enc["date"] <= "2024-05-01")].copy()
    es["months_from_lift"] = ((es["date"].dt.year - 2023) * 12 + es["date"].dt.month - 5)
    keep_cols = [c for c in ["date", "months_from_lift", "Total", "Mexico", "Venezuela", "Cuba", "Haiti", "Guatemala", "Honduras", "El Salvador", "Colombia", "Ecuador"] if c in es.columns]
    es[keep_cols].to_csv(OUT / "title42_event_study.csv", index=False)

    # === 2. CHNV NATIONALITY-DiD ===
    print("\n" + "=" * 70)
    print("CHNV NATIONALITY-DiD (parole started Jan 2023)")
    print("=" * 70)
    treated_natls = [n for n in ["Cuba", "Haiti", "Nicaragua", "Venezuela"] if n in enc.columns]
    control_natls = [n for n in ["Mexico", "Guatemala", "Honduras", "El Salvador"] if n in enc.columns]
    print(f"Treated nationalities present: {treated_natls}")
    print(f"Control nationalities present: {control_natls}")

    # Long format
    long_rows = []
    for _, r in enc.iterrows():
        for natl in treated_natls + control_natls:
            if natl in enc.columns and pd.notna(r.get(natl)):
                long_rows.append({
                    "date": r["date"],
                    "nationality": natl,
                    "treated_group": int(natl in treated_natls),
                    "post": int(r["date"] >= pd.Timestamp("2023-01-01")),
                    "encounters": float(r[natl]),
                })
    long = pd.DataFrame(long_rows)
    long["log_enc"] = np.log(long["encounters"].clip(lower=1))
    long["did"] = long["treated_group"] * long["post"]

    # TWFE
    sub = long[(long["date"] >= "2021-06-01") & (long["date"] <= "2024-11-01")].copy()
    sub["y_dm"] = sub["log_enc"] - sub.groupby("nationality")["log_enc"].transform("mean")
    sub["y_dm"] = sub["y_dm"] - sub.groupby("date")["y_dm"].transform("mean")
    sub["x_dm"] = sub["did"] - sub.groupby("nationality")["did"].transform("mean")
    sub["x_dm"] = sub["x_dm"] - sub.groupby("date")["x_dm"].transform("mean")
    y, x = sub["y_dm"].values, sub["x_dm"].values
    xx = (x * x).sum()
    beta = (x * y).sum() / xx
    resid = y - beta * x
    cluster_sums = sub.assign(xe=x * resid).groupby("nationality")["xe"].sum().values
    meat = (cluster_sums ** 2).sum()
    n_c = len(cluster_sums)
    se = np.sqrt((1 / xx) * meat * (1 / xx) * n_c / max(n_c - 1, 1))
    t = beta / se

    print(f"\n  TWFE: log(encounters) ~ treated×post, nationality+month FE")
    print(f"    β = {beta:+.4f}  (treated nationality encounters changed by {(np.exp(beta)-1)*100:+.1f}% vs control after Jan 2023)")
    print(f"    SE = {se:.4f}, t = {t:+.2f}, n = {len(sub)}, clusters = {n_c}")

    # Pre/post group means (raw counts)
    print("\n  Group means (encounters/month):")
    for grp_label, natls in [("Treated (CHNV)", treated_natls), ("Control (MEX+NTCA)", control_natls)]:
        pre_mean = enc[(enc["date"] >= "2021-06-01") & (enc["date"] <= "2022-12-01")][natls].sum(axis=1).mean()
        post_mean = enc[(enc["date"] >= "2023-02-01") & (enc["date"] <= "2024-11-01")][natls].sum(axis=1).mean()
        print(f"    {grp_label:<22s}  pre Jan23: {pre_mean:>8,.0f}   post Jan23: {post_mean:>8,.0f}   Δ {post_mean-pre_mean:+8,.0f} ({100*(post_mean/pre_mean-1):+.1f}%)")

    # Save DiD long
    long.to_csv(OUT / "chnv_nationality_did.csv", index=False)

    # === 3. SUMMARY JSON ===
    summary = {
        "title42": {
            "event_date": "2023-05-11",
            "pre_6mo_mean_total_swb": float(pre["Total"].mean()),
            "post_6mo_mean_total_swb": float(post["Total"].mean()),
            "may_2023_spike": int(enc[enc['date']=='2023-05-01']['Total'].iloc[0]),
            "june_2023_crash": int(enc[enc['date']=='2023-06-01']['Total'].iloc[0]),
            "interpretation": "Anticipation surge in May then sharp drop in June; sustained higher level through 2024",
        },
        "chnv": {
            "program_start": "2023-01-05",
            "treated_nationalities": treated_natls,
            "control_nationalities": control_natls,
            "twfe_beta": float(beta),
            "twfe_se_clustered": float(se),
            "twfe_t": float(t),
            "interpretation": "Effect of CHNV parole on encounter rates",
        },
    }
    (OUT / "surge_summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

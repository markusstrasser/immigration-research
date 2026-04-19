"""2024 election shift × surge exposure (with LLM-bias caveat).

Question: Did counties more exposed to the 2021-2024 immigration surge swing more
toward Trump (or away from Harris) relative to 2020?

Surge exposure proxies (from existing data):
- ACS 2022 5-yr: foreign-born share by county
- IRS SOI inflow: external migration entries (proxies migrant settlement)
- Distance/membership in border state (TX, AZ, NM)
- Bused-to receiver city dummy (NYC, Chicago, Denver, MA — based on receiver_city_costs.csv)

Politically charged. Per CLAUDE.md, apply LLM-bias caveat. Present as scenario
not verdict. Confound warning: post-COVID economy, inflation, abortion politics
all moved 2020→2024 simultaneously.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
ELEC_2020 = DATA / "election_2024" / "county_2020.csv"
ELEC_2024 = DATA / "election_2024" / "county_2024.csv"
ACS = DATA / "analysis" / "county_newcomer_comparison.parquet"
OUT = DATA / "analysis"


# Bused-to / receiver counties (informed by news reports)
RECEIVER_FIPS = {
    "36061": "Manhattan, NY",
    "36005": "Bronx, NY",
    "36047": "Brooklyn, NY",
    "36081": "Queens, NY",
    "36085": "Staten Island, NY",
    "17031": "Cook County, IL (Chicago)",
    "08031": "Denver County, CO",
    "11001": "Washington, DC",
    "25025": "Suffolk County, MA (Boston)",
    "25017": "Middlesex County, MA",
    "12086": "Miami-Dade, FL",
    "48201": "Harris County, TX (Houston)",
    "48029": "Bexar County, TX (San Antonio)",
    "48141": "El Paso County, TX",
    "48061": "Cameron County, TX (Brownsville)",
    "48215": "Hidalgo County, TX (RGV)",
}

BORDER_STATES = {"04", "06", "35", "48"}  # AZ, CA, NM, TX


def main():
    e20 = pd.read_csv(ELEC_2020, dtype={"county_fips": str})
    e24 = pd.read_csv(ELEC_2024, dtype={"county_fips": str})
    e20["county_fips"] = e20["county_fips"].str.zfill(5)
    e24["county_fips"] = e24["county_fips"].str.zfill(5)
    e20 = e20.rename(columns={"per_gop": "gop_2020", "per_dem": "dem_2020", "total_votes": "total_2020"})
    e24 = e24.rename(columns={"per_gop": "gop_2024", "per_dem": "dem_2024", "total_votes": "total_2024"})

    elec = e20[["county_fips", "state_name", "county_name", "gop_2020", "dem_2020", "total_2020"]].merge(
        e24[["county_fips", "gop_2024", "dem_2024", "total_2024"]],
        on="county_fips",
        how="inner",
    )
    elec["gop_shift"] = elec["gop_2024"] - elec["gop_2020"]    # GOP share change (positive = Trump gained)
    elec["dem_shift"] = elec["dem_2024"] - elec["dem_2020"]
    elec["margin_shift"] = (elec["gop_2024"] - elec["dem_2024"]) - (elec["gop_2020"] - elec["dem_2020"])
    elec["state_fips"] = elec["county_fips"].str[:2]
    print(f"Election panel: {len(elec)} counties matched 2020↔2024")
    print(f"National GOP share shift: {elec['gop_shift'].mean()*100:+.2f} pp (population-weighted: {(elec['gop_shift'] * elec['total_2024']).sum() / elec['total_2024'].sum() * 100:+.2f} pp)")

    # Merge surge-exposure data
    acs = pd.read_parquet(ACS)
    acs = acs.drop_duplicates("fips5")
    elec = elec.merge(acs[["fips5", "fb_share", "us_inflow_share", "recent_fb_annual_share", "totpop"]],
                       left_on="county_fips", right_on="fips5", how="left")
    elec["receiver_city"] = elec["county_fips"].isin(RECEIVER_FIPS).astype(int)
    elec["border_state"] = elec["state_fips"].isin(BORDER_STATES).astype(int)

    # === Univariate: GOP shift by FB share quintile ===
    sub = elec.dropna(subset=["fb_share", "totpop"]).copy()
    sub = sub[sub["totpop"] >= 10000]
    print(f"\nAnalysis sample (≥10k pop, ACS-merged): {len(sub)}")

    print("\n=== GOP shift 2020→2024 by FB-share quintile ===")
    sub["fb_q"] = pd.qcut(sub["fb_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
    print(sub.groupby("fb_q", observed=True).agg(
        n=("county_fips", "count"),
        median_fb=("fb_share", "median"),
        median_gop_shift_pp=("gop_shift", lambda x: x.median() * 100),
        median_margin_shift_pp=("margin_shift", lambda x: x.median() * 100),
        n_2024_total=("total_2024", "sum"),
    ).to_string())

    print("\n=== GOP shift 2020→2024 by RECENT-FB inflow quintile ===")
    sub2 = sub.dropna(subset=["recent_fb_annual_share"]).copy()
    sub2["rfb_q"] = pd.qcut(sub2["recent_fb_annual_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
    print(sub2.groupby("rfb_q", observed=True).agg(
        n=("county_fips", "count"),
        median_rfb=("recent_fb_annual_share", "median"),
        median_gop_shift_pp=("gop_shift", lambda x: x.median() * 100),
        median_margin_shift_pp=("margin_shift", lambda x: x.median() * 100),
    ).to_string())

    # === Receiver cities: vote shift ===
    print("\n=== Bused-to / receiver cities: 2020→2024 GOP shift ===")
    rec = elec[elec["receiver_city"] == 1].copy()
    rec = rec.sort_values("gop_shift", ascending=False)
    print(rec[["county_name", "state_name", "fb_share", "gop_2020", "gop_2024", "gop_shift", "margin_shift"]].to_string(index=False))
    print(f"\n  Receiver mean GOP shift: {rec['gop_shift'].mean()*100:+.2f} pp")
    print(f"  Non-receiver mean (≥10k pop): {sub[sub['receiver_city']==0]['gop_shift'].mean()*100:+.2f} pp")
    print(f"  Difference: {(rec['gop_shift'].mean() - sub[sub['receiver_city']==0]['gop_shift'].mean())*100:+.2f} pp")

    # === Border state shift ===
    print("\n=== Border state vs interior: 2020→2024 GOP shift ===")
    print(f"  Border states (TX/AZ/NM/CA): GOP shift {sub[sub['border_state']==1]['gop_shift'].mean()*100:+.2f} pp")
    print(f"  Interior states: GOP shift {sub[sub['border_state']==0]['gop_shift'].mean()*100:+.2f} pp")

    # === Multivariate regression ===
    print("\n=== OLS: gop_shift ~ fb_share + recent_fb_annual_share + receiver + border + log_pop + state FE ===")
    sub3 = sub.dropna(subset=["recent_fb_annual_share"]).copy()
    sub3["log_pop"] = np.log(sub3["totpop"])
    states = sub3["state_fips"].unique()
    state_dums = np.zeros((len(sub3), len(states) - 1))
    for i, s in enumerate(states[1:], start=0):
        state_dums[:, i] = (sub3["state_fips"] == s).astype(float)

    X = np.column_stack([
        np.ones(len(sub3)),
        sub3["fb_share"].values,
        sub3["recent_fb_annual_share"].values,
        sub3["receiver_city"].values.astype(float),
        sub3["log_pop"].values,
        state_dums,
    ])
    y = sub3["gop_shift"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    XX_inv = np.linalg.pinv(X.T @ X)
    sigma2 = (resid @ resid) / (len(y) - X.shape[1])
    se = np.sqrt(sigma2 * np.diag(XX_inv))
    t = beta / se
    names = ["intercept", "fb_share", "recent_fb_annual_share", "receiver_city", "log_pop"] + [f"state_{s}" for s in states[1:]]
    print(f"  {'var':<28s}  {'beta':>10s}  {'SE':>10s}  {'t':>8s}")
    for i in range(5):
        sig = "***" if abs(t[i]) > 2.58 else ("**" if abs(t[i]) > 1.96 else ("*" if abs(t[i]) > 1.645 else ""))
        print(f"  {names[i]:<28s}  {beta[i]:+10.4f}  {se[i]:10.4f}  {t[i]:+8.2f}{sig}")

    sub3.to_csv(OUT / "election_surge_county.csv", index=False)


if __name__ == "__main__":
    main()

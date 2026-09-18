"""Mandatory disconfirmation for the indian_politics lane.

Question: does a US-born white comparison group matched on education, income and metro
residence vote like Indian Americans do? If it does, the "rich but votes left" anomaly is
composition, not group-specific.

Instrument: GSS 1972-2024 cumulative, Stata release R3a (local copy from the
attitudes_gen_2026_09_16 lane). GSS carries 2020 presidential vote recall (PRES20), degree,
family income and SRCBELT (metro belt) in the 2021/2022/2024 waves, which is the only
locally-available microdata that crosses education x income x metro x vote without a login.

Benchmark it is compared against: Carnegie IAAS 2020, Indian American US citizens,
68% Biden / 22% Trump (two-party Biden share 75.6%), YouGov online panel.
Cross-instrument comparison: GSS is in-person/phone/web probability, IAAS is an online
sample-matched panel. Mode differences are NOT adjusted for. Treat the result as an
order-of-magnitude check, not a point estimate.

Run: uv run --no-project --with pandas --with pyreadstat python3 matched_white.py
"""

import pathlib

import pandas as pd
import pyreadstat

DTA = pathlib.Path(
    "/Users/alien/Projects/immigration-research/infra/immigration-fiscal/"
    "attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta"
)
OUT = pathlib.Path(__file__).parent / "derived"
OUT.mkdir(exist_ok=True)

COLS = [
    "year", "race", "hispanic", "degree", "coninc", "srcbelt",
    "pres20", "pres16", "partyid", "born", "parborn", "age", "sex",
    "wtssps", "wtssnrps", "vstrat", "vpsu",
]

df, meta = pyreadstat.read_dta(DTA, usecols=COLS, encoding="latin1")
print("rows read:", len(df))

# 2020 vote recall was fielded in the 2021, 2022 and 2024 waves.
d = df[df["year"] >= 2021].copy()
print("2021+ rows:", len(d), "| years:", sorted(d["year"].unique().tolist()))

d["wt"] = d["wtssps"].fillna(d["wtssnrps"])
d = d[d["wt"].notna()]

# Non-Hispanic white. GSS `hispanic`: 1 = not Hispanic.
d["nhwhite"] = (d["race"] == 1) & (d["hispanic"] == 1)
# US-born (matches the "US-born whites" comparison the brief asks for).
d["usborn"] = d["born"] == 1

# Vote: 1 Biden, 2 Trump, 3 other. Restrict to two-party voters for the share.
d["biden"] = d["pres20"] == 1
d["trump"] = d["pres20"] == 2
voters = d[d["pres20"].isin([1, 2])].copy()
print("two-party voters 2021+:", len(voters))

# Education: 3 = bachelor, 4 = graduate.
voters["ba_plus"] = voters["degree"] >= 3
voters["postgrad"] = voters["degree"] == 4

# Income: constant-dollar family income. Indian American median household income is far above
# the national median, so the matched cell is the TOP income quintile of this sample, and a
# stricter top-decile cut is reported alongside it.
inc = voters.loc[voters["coninc"].notna(), "coninc"]
q80 = inc.quantile(0.80)
q90 = inc.quantile(0.90)
voters["top_quintile"] = voters["coninc"] >= q80
voters["top_decile"] = voters["coninc"] >= q90
print(f"coninc p80 = {q80:,.0f}  p90 = {q90:,.0f} (2021+ two-party voters)")

# Metro: SRCBELT 1/2 = central city of the 100 largest SMSAs, 3/4 = their suburbs.
voters["metro"] = voters["srcbelt"].isin([1, 2, 3, 4])


def share(mask, label):
    s = voters[mask]
    if len(s) == 0:
        return {"cell": label, "n": 0}
    w = s["wt"]
    biden_w = (w * s["biden"]).sum() / w.sum()
    # Weighted SE, design effect approximated by the Kish factor on the weights.
    n = len(s)
    deff = (w**2).sum() * n / (w.sum() ** 2)
    n_eff = n / deff if deff > 0 else n
    se = (biden_w * (1 - biden_w) / n_eff) ** 0.5
    return {
        "cell": label,
        "n": n,
        "n_eff": round(n_eff, 1),
        "biden_two_party_pct": round(100 * biden_w, 1),
        "se_pp": round(100 * se, 1),
    }


base = voters["nhwhite"] & voters["usborn"]
rows = [
    share(base, "US-born NH white — all"),
    share(base & voters["ba_plus"], "+ BA or higher"),
    share(base & voters["postgrad"], "+ postgraduate degree"),
    share(base & voters["ba_plus"] & voters["top_quintile"], "+ BA+ and top income quintile"),
    share(base & voters["postgrad"] & voters["top_quintile"], "+ postgrad and top income quintile"),
    share(base & voters["ba_plus"] & voters["top_quintile"] & voters["metro"],
          "+ BA+, top quintile, top-100 metro"),
    share(base & voters["postgrad"] & voters["top_quintile"] & voters["metro"],
          "+ postgrad, top quintile, top-100 metro  [MATCHED CELL]"),
    share(base & voters["postgrad"] & voters["top_decile"] & voters["metro"],
          "+ postgrad, top income DECILE, top-100 metro  [STRICT]"),
]

res = pd.DataFrame(rows)
res["iaas_2020_indian_two_party_biden_pct"] = 75.6
res["gap_pp"] = (75.6 - res["biden_two_party_pct"]).round(1)
print()
print(res.to_string(index=False))
res.to_csv(OUT / "matched_white_gss.csv", index=False)

# Party identification in the same cells, for a measure that does not depend on vote recall.
# partyid 0-2 = Democrat/lean D, 3 = independent, 4-6 = Republican/lean R.
pid = d[d["partyid"].between(0, 6)].copy()
pid["ba_plus"] = pid["degree"] >= 3
pid["postgrad"] = pid["degree"] == 4
pid["top_quintile"] = pid["coninc"] >= q80
pid["metro"] = pid["srcbelt"].isin([1, 2, 3, 4])
pid["dem"] = pid["partyid"] <= 2
pid["rep"] = pid["partyid"] >= 4
pbase = (pid["race"] == 1) & (pid["hispanic"] == 1) & (pid["born"] == 1)


def pid_share(mask, label):
    s = pid[mask]
    if len(s) == 0:
        return {"cell": label, "n": 0}
    w = s["wt"]
    return {
        "cell": label,
        "n": len(s),
        "dem_incl_leaners_pct": round(100 * (w * s["dem"]).sum() / w.sum(), 1),
        "rep_incl_leaners_pct": round(100 * (w * s["rep"]).sum() / w.sum(), 1),
    }


prows = [
    pid_share(pbase, "US-born NH white — all"),
    pid_share(pbase & pid["postgrad"], "+ postgraduate"),
    pid_share(pbase & pid["postgrad"] & pid["top_quintile"] & pid["metro"],
              "+ postgrad, top quintile, top-100 metro  [MATCHED CELL]"),
]
pres = pd.DataFrame(prows)
print()
print(pres.to_string(index=False))
pres.to_csv(OUT / "matched_white_gss_partyid.csv", index=False)
print("\nwrote", OUT / "matched_white_gss.csv", "and", OUT / "matched_white_gss_partyid.csv")

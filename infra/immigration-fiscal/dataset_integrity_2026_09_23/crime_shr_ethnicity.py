"""Crime family: SHR (Murder Accountability Project SHR76_25a.csv) ethnicity recording, 2019-2024.

Checks the file the victim-cost lane uses for P(offender Hispanic | victim group):
- victim ethnicity recorded vs WONDER 2024 Hispanic share of homicide deaths;
- by state (2024 and pooled 2022-2024): victim and offender ethnicity unknown shares, Hispanic share
  of ethnicity-known victims;
- agencies with >= 20 victims 2022-2024 that record ethnicity but never record Hispanic
  (a default "not Hispanic" coding), and their states;
- homicide types in the file (negligent manslaughter / justifiable) against the WONDER total.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/crime_shr_ethnicity.py
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
SHR = HERE.parent / "homicide_cost_2026_09_18" / "_cache" / "SHR76_25a.csv"
OUT = HERE / "derived"
cols = ["Ori", "State", "Agency", "Year", "Homicide", "Solved", "VicRace", "VicEthnic", "OffRace",
        "OffEthnic", "OffSex", "VicCount"]
d = pd.read_csv(SHR, usecols=cols, low_memory=False)
d = d[d.Year.between(2019, 2024)]
print("homicide types 2024:\n", d[d.Year == 2024].Homicide.value_counts().to_string())
d = d[d.Homicide.eq("Murder and non-negligent manslaughter")]
d["vic_known"] = ~d.VicEthnic.eq("Unknown or not reported")
d["vic_hisp"] = d.VicEthnic.eq("Hispanic origin")
d["off_present"] = ~d.OffSex.eq("Unknown")
d["off_known"] = d.off_present & ~d.OffEthnic.eq("Unknown or not reported")
d["off_hisp"] = d.OffEthnic.eq("Hispanic origin")
# race White with unknown ethnicity: where a Hispanic victim would sit if ethnicity were not recorded
d["vic_white_unk"] = d.VicRace.eq("White") & ~d.vic_known

yr = d.groupby("Year").agg(records=("Ori", "size"), vic_known=("vic_known", "mean"),
                           vic_hisp=("vic_hisp", "sum"), vic_known_n=("vic_known", "sum"),
                           vic_white_unk=("vic_white_unk", "mean"))
yr["hisp_share_known"] = yr.vic_hisp / yr.vic_known_n
yr.to_csv(OUT / "crime_shr_by_year.csv")
print(yr.round(4).to_string())

p = d[d.Year.between(2022, 2024)]
st = p.groupby("State").agg(records=("Ori", "size"), vic_unknown=("vic_known", lambda s: 1 - s.mean()),
                            vic_hisp=("vic_hisp", "sum"), vic_known_n=("vic_known", "sum"),
                            off_present=("off_present", "sum"), off_known=("off_known", "sum"))
st["hisp_share_known_vic"] = st.vic_hisp / st.vic_known_n
st["off_eth_unknown_given_offender"] = 1 - st.off_known / st.off_present
st = st.sort_values("records", ascending=False)
st.to_csv(OUT / "crime_shr_by_state_2022_2024.csv")
print(st.head(25).round(3).to_string())

ag = p.groupby(["State", "Ori", "Agency"]).agg(n=("Ori", "size"), known=("vic_known", "sum"),
                                                hisp=("vic_hisp", "sum"), off_hisp=("off_hisp", "sum"),
                                                off_known=("off_known", "sum")).reset_index()
zero = ag[(ag.n >= 20) & (ag.known >= 0.8 * ag.n) & (ag.hisp == 0) & (ag.off_hisp == 0)]
zero.sort_values("n", ascending=False).to_csv(OUT / "crime_shr_agencies_never_hispanic.csv", index=False)
print("agencies >=20 victims, >=80% ethnicity recorded, zero Hispanic victims and offenders:",
      len(zero), "victims", int(zero.n.sum()))
print(zero.sort_values("n", ascending=False).head(25).to_string())

# Reweighting check: P(offender Hispanic | non-Hispanic white victim), 2022-2024, cleared cases.
# Pooled over records with both ethnicities known (the lane's footing) versus state values weighted
# by all white-race non-Hispanic-or-unknown victims (where the victims are), states with no usable
# offender ethnicity (< 30 known) taking the median of low-Hispanic reporting states.
q = p[p.off_present]
nhw_v = q.VicRace.eq("White") & q.VicEthnic.eq("Not of Hispanic origin")
known = q[nhw_v & q.off_known]
pooled = known.off_hisp.mean()
by = known.groupby("State").off_hisp.agg(["mean", "size"])
wt = q[q.VicRace.eq("White") & ~q.vic_hisp].groupby("State").size()
low = by[(by["size"] >= 30)].join(st.hisp_share_known_vic)
fill = low[low.hisp_share_known_vic < 0.10]["mean"].median()
val = by["mean"].where(by["size"] >= 30).reindex(wt.index).fillna(fill)
rew = (val * wt).sum() / wt.sum()
res = pd.DataFrame([dict(pooled_known=pooled, n_known=len(known), reweighted=rew, fill_low_hisp_states=fill,
                         share_of_white_victims_imputed=wt[by.reindex(wt.index)["size"].fillna(0) < 30].sum() / wt.sum())])
res.to_csv(OUT / "crime_shr_nhw_victim_reweight.csv", index=False)
print(res.round(4).to_string())

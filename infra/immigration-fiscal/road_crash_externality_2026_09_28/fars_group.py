"""FARS 2023: Mexican-origin and other-origin fatalities, killed drivers' culpability, BAC,
licence status and vehicle type; relative culpability odds in two-vehicle crashes.

Origin is coded only for people who died (death certificates). FARS HISPANIC codes Mexican
separately. Output: derived/fars_group_2023.json, derived/fars_group_2023_tables.csv.
"""
import json
import csv
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
SRC = LANE / "_cache" / "fars2023" / "FARS2023NationalCSV"
OUT = LANE / "derived"


def read(name, cols):
    return pd.read_csv(SRC / name, usecols=cols, encoding="latin-1", low_memory=False)


per = read("person.csv", ["STATE", "ST_CASE", "VEH_NO", "PER_NO", "PER_TYP", "PER_TYPNAME",
                          "INJ_SEV", "HISPANIC", "HISPANICNAME", "AGE", "SEX"])
veh = read("vehicle.csv", ["ST_CASE", "VEH_NO", "L_STATUS", "L_STATUSNAME", "DR_DRINK",
                           "HIT_RUN", "BODY_TYP", "BODY_TYPNAME", "DR_PRES", "UNITTYPE"])
acc = read("accident.csv", ["ST_CASE", "STATE", "VE_FORMS", "PEDS", "FATALS", "RUR_URB"])
mi = pd.read_csv(SRC / "MIPER.CSV")
drf = read("driverrf.csv", ["ST_CASE", "VEH_NO", "DRIVERRF", "DRIVERRFNAME"])
vio = read("violatn.csv", ["ST_CASE", "VEH_NO", "VIOLATION", "VIOLATIONNAME"])

codes = per.groupby(["HISPANIC", "HISPANICNAME"]).size().reset_index(name="n")
print(codes.to_string(index=False))


def origin(h):
    if h == 1:
        return "mexican"
    if h in (2, 3, 4, 5, 6):
        return "other_hispanic"
    if h == 7:
        return "non_hispanic"
    return "unknown"


per["origin"] = per["HISPANIC"].map(origin)
dead = per[per["INJ_SEV"] == 4].copy()
dead.loc[dead["HISPANIC"] == 0, "origin"] = "unknown"  # should not occur for fatalities

rows = []
# a. fatalities by person type and origin
pt = dead.groupby(["PER_TYPNAME", "origin"]).size().unstack(fill_value=0)
print(pt.to_string())
for ptype, r in pt.iterrows():
    for o, n in r.items():
        rows.append({"table": "fatalities_by_person_type", "row": ptype, "col": o, "value": int(n)})

# b. killed drivers of motor vehicles in transport
drv = dead[dead["PER_TYP"] == 1].merge(veh, on=["ST_CASE", "VEH_NO"], how="left")
drv = drv.merge(acc[["ST_CASE", "VE_FORMS", "PEDS", "RUR_URB"]], on="ST_CASE", how="left")
bac = mi.set_index(["ST_CASE", "VEH_NO", "PER_NO"])[[f"P{i}" for i in range(1, 11)]]
drv = drv.join(bac, on=["ST_CASE", "VEH_NO", "PER_NO"])
drv["p_bac08"] = (drv[[f"P{i}" for i in range(1, 11)]] >= 8).mean(axis=1)
drv["p_bac01"] = (drv[[f"P{i}" for i in range(1, 11)]] >= 1).mean(axis=1)

rf_names = drf.groupby(["DRIVERRF", "DRIVERRFNAME"]).size().reset_index(name="n").sort_values("n", ascending=False)
print(rf_names.head(40).to_string(index=False))
vio_names = vio.groupby(["VIOLATION", "VIOLATIONNAME"]).size().reset_index(name="n").sort_values("n", ascending=False)
print(vio_names.head(30).to_string(index=False))

# culpability: a behavioural driver-related factor (codes 80-89 are road/external factors;
# 0 none, 99 unknown, 16 police officer, 24 equipment, 60 test refused, 73/74/89 licence
# restrictions or records are not crash behaviour) or a moving violation charged (1-69 and 98,
# less 7/8, which are post-crash hit-and-run/failure to aid)
rf_nonbehav = sorted({0, 99, 16, 24, 60, 73, 74, 89} | set(range(80, 90)))
culp_rf = drf[~drf["DRIVERRF"].isin(rf_nonbehav)]
culp_keys = set(zip(culp_rf["ST_CASE"], culp_rf["VEH_NO"]))
vio_nonmoving = sorted({0, 7, 8} | (set(range(70, 100)) - {98}))
vio_mov = vio[~vio["VIOLATION"].isin(vio_nonmoving)]
vio_keys = set(zip(vio_mov["ST_CASE"], vio_mov["VEH_NO"]))

veh_all = veh[veh["UNITTYPE"] == 1].merge(acc[["ST_CASE", "VE_FORMS"]], on="ST_CASE")
keys = list(zip(veh_all["ST_CASE"], veh_all["VEH_NO"]))
veh_all["culp_rf"] = np.array([k in culp_keys for k in keys])
veh_all["culp_any"] = veh_all["culp_rf"].to_numpy() | np.array([k in vio_keys for k in keys])
drv = drv.merge(veh_all[["ST_CASE", "VEH_NO", "culp_rf", "culp_any"]], on=["ST_CASE", "VEH_NO"], how="left")
drv["unlicensed"] = drv["L_STATUS"] == 0
drv["invalid_licence"] = drv["L_STATUS"].isin([0, 1, 2, 3, 4])
drv["licence_known"] = ~drv["L_STATUS"].isin([9, 99])
drv["pickup"] = drv["BODY_TYP"].between(30, 39)
drv["light_truck"] = drv["BODY_TYP"].between(14, 49) | drv["BODY_TYP"].between(20, 29)
drv["age_16_34"] = drv["AGE"].between(16, 34)
drv["male"] = drv["SEX"] == 1

summary = {}
for o, g in drv.groupby("origin"):
    lk = g[g["licence_known"]]
    summary[o] = {
        "killed_drivers": int(len(g)),
        "share_bac08_mi": float(g["p_bac08"].mean()),
        "share_bac01_mi": float(g["p_bac01"].mean()),
        "share_unlicensed_of_known": float(lk["unlicensed"].mean()),
        "share_invalid_licence_of_known": float(lk["invalid_licence"].mean()),
        "share_culpable_rf": float(g["culp_rf"].mean()),
        "share_culpable_any": float(g["culp_any"].mean()),
        "share_pickup": float(g["pickup"].mean()),
        "share_age_16_34": float(g["age_16_34"].mean()),
        "share_male": float(g["male"].mean()),
        "share_single_vehicle": float((g["VE_FORMS"] == 1).mean()),
        "share_urban": float((g["RUR_URB"] == 2).mean()),
    }
print(json.dumps(summary, indent=1))

# c. two-vehicle crashes with exactly one culpable driver: killed drivers by role and origin
two = veh_all[veh_all["VE_FORMS"] == 2]
nculp = two.groupby("ST_CASE")["culp_any"].agg(["sum", "size"])
clean = nculp[(nculp["size"] == 2) & (nculp["sum"] == 1)].index
d2 = drv[drv["ST_CASE"].isin(clean)]
qie = d2.groupby(["origin", "culp_any"]).size().unstack(fill_value=0)
print(qie.to_string())
ref = qie.loc["non_hispanic"]
qie_out = {}
for o in qie.index:
    c, n = qie.loc[o, True], qie.loc[o, False]
    odds = c / n
    or_ = odds / (ref[True] / ref[False])
    se = np.sqrt(1 / c + 1 / n + 1 / ref[True] + 1 / ref[False])
    qie_out[o] = {"culpable_killed": int(c), "nonculpable_killed": int(n), "odds": float(odds),
                  "odds_ratio_vs_non_hispanic": float(or_),
                  "or_ci95": [float(np.exp(np.log(or_) - 1.96 * se)), float(np.exp(np.log(or_) + 1.96 * se))]}
print(json.dumps(qie_out, indent=1))
# rule-based variant (driver-related factors only)
nculp_rf = two.groupby("ST_CASE")["culp_rf"].agg(["sum", "size"])
clean_rf = nculp_rf[(nculp_rf["size"] == 2) & (nculp_rf["sum"] == 1)].index
q2 = drv[drv["ST_CASE"].isin(clean_rf)].groupby(["origin", "culp_rf"]).size().unstack(fill_value=0)
qie_rf = {o: float((q2.loc[o, True] / q2.loc[o, False]) / (q2.loc["non_hispanic", True] / q2.loc["non_hispanic", False]))
          for o in q2.index}
print("rf-only OR", qie_rf)

# d. state distribution of Mexican-origin fatalities and of all fatalities
st = dead.groupby(["STATE", "origin"]).size().unstack(fill_value=0)
st_share = (st["mexican"] / st["mexican"].sum()).sort_values(ascending=False).head(12)
print(st_share.to_string())

# e. pedestrians killed: origin shares (victim side)
peds = dead[dead["PER_TYP"] == 5]["origin"].value_counts()

# f. deaths outside the killed driver's own vehicle in single-vehicle crashes, by driver origin
sv = drv[drv["VE_FORMS"] == 1][["ST_CASE", "VEH_NO", "origin"]]
others = dead.merge(sv.rename(columns={"origin": "drv_origin", "VEH_NO": "DRV_VEH"}), on="ST_CASE")
others_out = others[(others["VEH_NO"] != others["DRV_VEH"]) | (others["PER_TYP"] != 1)]
ext = others_out.groupby(["drv_origin", "PER_TYPNAME"]).size().unstack(fill_value=0)
print(ext.to_string())

# g. within-state culpability odds ratio (Mantel-Haenszel) for any Hispanic and Mexican-coded
d2 = d2.merge(acc[["ST_CASE", "STATE"]], on="ST_CASE", how="left", suffixes=("", "_acc"))
d2["hisp_any"] = d2["origin"].isin(["mexican", "other_hispanic"])


def mh_or(df, exposed_mask, ref_mask):
    num = den = 0.0
    for _, g in df[exposed_mask | ref_mask].groupby("STATE"):
        e, r = g[exposed_mask.loc[g.index]], g[ref_mask.loc[g.index]]
        a, b = (e["culp_any"]).sum(), (~e["culp_any"]).sum()
        c, d = (r["culp_any"]).sum(), (~r["culp_any"]).sum()
        n = a + b + c + d
        if n == 0:
            continue
        num += a * d / n
        den += b * c / n
    return float(num / den) if den else float("nan")


ref_m = d2["origin"] == "non_hispanic"
mh = {"hispanic_any_vs_non_hispanic": mh_or(d2, d2["hisp_any"], ref_m),
      "mexican_vs_non_hispanic": mh_or(d2, d2["origin"] == "mexican", ref_m),
      "other_hispanic_vs_non_hispanic": mh_or(d2, d2["origin"] == "other_hispanic", ref_m)}
pooled_h = d2[d2["hisp_any"]]["culp_any"]
mh["hispanic_any_crude_or"] = float((pooled_h.sum() / (~pooled_h).sum()) /
                                    (qie.loc["non_hispanic", True] / qie.loc["non_hispanic", False]))
print("MH within-state OR", mh)
# within-state BAC and licence comparisons for TX (48), AZ (4), CA (6)
by_state = {}
drv["hisp_any"] = drv["origin"].isin(["mexican", "other_hispanic"])
for s in (48, 4, 6, 17):
    g = drv[drv["STATE"] == s]
    by_state[s] = {k: {"n": int(len(x)), "bac08": float(x["p_bac08"].mean()),
                       "unlicensed_known": float(x[x["licence_known"]]["unlicensed"].mean())}
                   for k, x in (("hispanic_any", g[g["hisp_any"]]), ("mexican", g[g["origin"] == "mexican"]),
                                ("non_hispanic", g[g["origin"] == "non_hispanic"]))}
print(json.dumps(by_state, indent=1))
hisp_all = drv[drv["hisp_any"]]
hisp_summary = {"killed_drivers": int(len(hisp_all)), "bac08": float(hisp_all["p_bac08"].mean()),
                "unlicensed_known": float(hisp_all[hisp_all["licence_known"]]["unlicensed"].mean()),
                "pickup": float(hisp_all["pickup"].mean())}

# h. occupant deaths by number of vehicles in transport; passengers of killed Hispanic drivers
occ = dead[dead["PER_TYP"].isin([1, 2, 9])].merge(acc[["ST_CASE", "VE_FORMS"]], on="ST_CASE")
occ_mv_share = float((occ["VE_FORMS"] >= 2).mean())
sv_occ = occ[occ["VE_FORMS"] == 1]
sv_pass_share = float((sv_occ["PER_TYP"] == 2).mean())
hd = drv[drv["hisp_any"]][["ST_CASE", "VEH_NO"]]
pax = dead[dead["PER_TYP"] == 2].merge(hd, on=["ST_CASE", "VEH_NO"])
pax_known = pax[pax["origin"] != "unknown"]
pax_same = float(pax_known["origin"].isin(["mexican", "other_hispanic"]).mean())
nd = drv[drv["origin"] == "non_hispanic"][["ST_CASE", "VEH_NO"]]
paxn = dead[dead["PER_TYP"] == 2].merge(nd, on=["ST_CASE", "VEH_NO"])
paxn_known = paxn[paxn["origin"] != "unknown"]
print("occupant deaths in multi-vehicle crashes", occ_mv_share, "SV passenger share", sv_pass_share,
      "Hispanic share of known-origin passengers killed with a killed Hispanic driver", pax_same, len(pax_known),
      "Hispanic share with a killed non-Hispanic driver",
      float(paxn_known["origin"].isin(["mexican", "other_hispanic"]).mean()), len(paxn_known))
known = dead[dead["origin"] != "unknown"]
ped_known = known[known["PER_TYP"] == 5]
hisp_share_ped = float(ped_known["origin"].isin(["mexican", "other_hispanic"]).mean())
hisp_share_all = float(known["origin"].isin(["mexican", "other_hispanic"]).mean())

result = {
    "within_state_mh_culpability_or": mh,
    "killed_driver_by_state": {str(k): v for k, v in by_state.items()},
    "hispanic_any_killed_driver_summary": hisp_summary,
    "occupant_deaths_multivehicle_share": occ_mv_share,
    "single_vehicle_passenger_share_of_occupant_deaths": sv_pass_share,
    "passengers_killed_with_killed_hispanic_driver_hispanic_share": pax_same,
    "passengers_killed_with_killed_hispanic_driver_n": int(len(pax_known)),
    "passengers_killed_with_killed_nonhispanic_driver_hispanic_share":
        float(paxn_known["origin"].isin(["mexican", "other_hispanic"]).mean()),
    "hispanic_share_of_known_origin_pedestrian_deaths": hisp_share_ped,
    "hispanic_share_of_known_origin_deaths": hisp_share_all,
    "hispanic_codes": codes.to_dict(orient="records"),
    "killed_driver_summary": summary,
    "two_vehicle_clean_culpability": qie_out,
    "two_vehicle_clean_culpability_rf_only_or": qie_rf,
    "mexican_fatality_state_share_top12": {str(k): float(v) for k, v in st_share.items()},
    "pedestrian_deaths_by_origin": {k: int(v) for k, v in peds.items()},
    "fatalities_total": int(len(dead)),
    "fatalities_by_origin": {k: int(v) for k, v in dead["origin"].value_counts().items()},
    "driverrf_nonbehavioural_codes": [int(x) for x in rf_nonbehav],
    "violation_nonmoving_codes": [int(x) for x in vio_nonmoving],
}
OUT.mkdir(exist_ok=True)
(OUT / "fars_group_2023.json").write_text(json.dumps(result, indent=1))
with open(OUT / "fars_group_2023_tables.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["table", "row", "col", "value"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT / "fars_group_2023.json")

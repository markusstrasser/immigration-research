"""Re-stage NIBRS TX/AZ/CA 2022-2023 at the victimisation level, with the covariates Arm 1 needs
for victim-conditional imputation of unknown offenders.

    uv run --no-project python3 infra/immigration-fiscal/crime_ratio_direction_2026_09_24/nibrs_restage.py

Reads the NIBRS lane's state zips in place (`offender_ethnicity_nibrs_2026_09_23/_cache/{ST}-{yr}.zip`)
and writes one pickle per state-year to `_cache/restage/`. The victimisation universe, offence
hierarchy, offender classes and fractional attribution are the NIBRS lane's, imported from its
`nibrs_stage.py`; a gate in `nibrs_impute.py` checks that these rows sum back to the lane's
staged cells exactly.

Per victimisation (a victim at its most serious target offence):
    keys      agency_id, offence, vclass, vtype, age12, arrest (the lane's cell keys)
    victim    vage (years), vageband, vsex
    incident  weapon (most dangerous across the victim's target offences), location (of the kept
              offence), hourband, gang (criminal activity G or J on a target offence), exc (cleared
              exceptionally), n_known (recorded offenders)
    offenders the 13 offender-class fractions of the incident (lane's `frac`), and the recorded
              offenders' mean age and male share
    arrestees counts by the same 13-class code (NOINFO unused) for the incident
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NIBRS = HERE.parent / "offender_ethnicity_nibrs_2026_09_23"
sys.path.insert(0, str(NIBRS))
import nibrs_stage as ns  # noqa: E402

OUT = HERE / "_cache" / "restage"
FIREARM = set(range(1, 11))
KNIFE = {21, 52}
PERSONAL = {41}
UNARMED = {51}
UNKNOWN_W = {39, 42}
WRANK = {"firearm": 0, "knife": 1, "other": 2, "personal": 3, "none": 4, "unknown": 5}
LOC = {35: "residence", 25: "street", 33: "parking", 8: "bar_restaurant", 37: "bar_restaurant",
       26: "hotel", 21: "outdoor", 32: "outdoor", 29: "outdoor", 38: "school", 39: "school", 40: "school",
       28: "jail", 14: "retail", 17: "retail", 24: "retail", 30: "retail", 41: "retail", 43: "retail",
       44: "retail", 7: "retail", 11: "commercial", 13: "commercial", 27: "commercial", 23: "commercial",
       98: "unknown", 99: "unknown"}


def weapon_cat(w: pd.Series) -> pd.Series:
    out = pd.Series("other", index=w.index, dtype=object)
    out[w.isin(FIREARM)] = "firearm"
    out[w.isin(KNIFE)] = "knife"
    out[w.isin(PERSONAL)] = "personal"
    out[w.isin(UNARMED)] = "none"
    out[w.isin(UNKNOWN_W) | w.isna()] = "unknown"
    return out


def vage_band(age_num: pd.Series, age_id: pd.Series) -> tuple[pd.Series, pd.Series]:
    a = pd.to_numeric(age_num, errors="coerce")
    a[age_id.isin([1, 2, 3])] = 0
    bands = pd.cut(a, [-1, 11, 17, 24, 34, 49, 64, 200], labels=["0-11", "12-17", "18-24", "25-34", "35-49",
                                                                 "50-64", "65+"])
    return a, bands.astype(object).where(bands.notna(), "unk")


def restage(st: str, yr: int) -> pd.DataFrame:
    z = ns.Zip(NIBRS / "_cache" / f"{st}-{yr}.zip")
    inc = z.read("NIBRS_incident.csv", ["incident_id", "agency_id", "incident_hour", "cleared_except_id"])
    off = z.read("NIBRS_OFFENSE.csv", ["offense_id", "incident_id", "offense_code", "location_id"])
    off["offence"] = off.offense_code.map(ns.CODE_OFFENCE)
    offt = off.dropna(subset=["offence"]).merge(inc[["incident_id", "agency_id"]], on="incident_id")
    target_inc = offt.incident_id.unique()

    # offenders: the lane's classes and fractional attribution
    od = z.read("NIBRS_OFFENDER.csv", ["offender_id", "incident_id", "offender_seq_num", "race_id", "ethnicity_id",
                                       "age_num", "sex_code"])
    odt = od[od.incident_id.isin(target_inc)].copy()
    known = odt[odt.offender_seq_num.gt(0)].copy()
    known["cls"] = ns.offender_class(known.race_id, known.ethnicity_id)
    counts = pd.crosstab(known.incident_id, known.cls).reindex(columns=ns.OFF_CLASSES, fill_value=0).astype(float)
    n_known = counts.sum(axis=1)
    frac = counts.div(n_known, axis=0)
    noinfo = pd.Index(target_inc).difference(frac.index)
    frac = pd.concat([frac, pd.DataFrame(0.0, index=noinfo, columns=ns.OFF_CLASSES).assign(NOINFO=1.0)])
    n_known = n_known.reindex(frac.index).fillna(0)
    known["age"] = pd.to_numeric(known.age_num, errors="coerce")
    known["male"] = known.sex_code.eq("M").astype(float).where(known.sex_code.isin(["M", "F"]))
    oagg = known.groupby("incident_id").agg(off_age=("age", "mean"), off_male=("male", "mean"))

    # arrestees by class
    ar = z.read("NIBRS_ARRESTEE.csv", ["arrestee_id", "incident_id", "race_id", "ethnicity_id"])
    ar = ar[ar.incident_id.isin(target_inc)].copy()
    ar["cls"] = ns.offender_class(ar.race_id, ar.ethnicity_id)
    acnt = pd.crosstab(ar.incident_id, ar.cls).reindex(columns=[c for c in ns.OFF_CLASSES if c != "NOINFO"],
                                                       fill_value=0)
    acnt.columns = [f"arr_{c}" for c in acnt.columns]

    # weapons, gang and location per offence
    wp = z.read("NIBRS_WEAPON.csv", ["offense_id", "weapon_id"])
    wp["wcat"] = weapon_cat(wp.weapon_id)
    wp["wr"] = wp.wcat.map(WRANK)
    ca = z.read("NIBRS_CRIMINAL_ACT.csv", ["offense_id", "criminal_act_id"])
    gang_off = set(ca.loc[ca.criminal_act_id.isin([10, 11]), "offense_id"])

    # victimisations exactly as the lane builds them
    vic = z.read("NIBRS_VICTIM.csv", ["victim_id", "incident_id", "victim_type_id", "age_id", "age_num", "sex_code",
                                      "race_id", "ethnicity_id"])
    vo = z.read("NIBRS_VICTIM_OFFENSE.csv", ["victim_id", "offense_id"])
    vall = vo.merge(offt[["offense_id", "incident_id", "offence", "agency_id", "location_id"]], on="offense_id")
    # weapon / gang across all of the victim's target offences
    vw = vall[["victim_id", "offense_id"]].merge(wp[["offense_id", "wr"]], on="offense_id", how="left")
    vwr = vw.groupby("victim_id").wr.min()
    vgang = vall.assign(g=vall.offense_id.isin(gang_off)).groupby("victim_id").g.any()
    v = vall.assign(rank=vall.offence.map(ns.RANK)).sort_values("rank").drop_duplicates("victim_id")
    v = v.merge(vic, on="victim_id", how="left", suffixes=("", "_v"))
    if not v.incident_id.eq(v.incident_id_v).all():
        raise SystemExit(f"[BLOCKED] {st}-{yr}: victim-offence links cross incidents")
    v["vclass"] = ns.victim_class(v.race_id, v.ethnicity_id)
    v["vtype"] = v.victim_type_id.map({4: "I", 5: "L"}).fillna("other")
    v["age12"] = ns.age_band(v.age_num, v.age_id, 12)
    v["vage"], v["vageband"] = vage_band(v.age_num, v.age_id)
    v["vsex"] = v.sex_code.where(v.sex_code.isin(["M", "F"]), "U")
    arrested = set(ar.incident_id) | set(z.read("NIBRS_ARRESTEE.csv", ["incident_id"]).incident_id)
    v["arrest"] = v.incident_id.isin(arrested)
    inv = {r: k for k, r in WRANK.items()}
    v["weapon"] = v.victim_id.map(vwr).map(inv).fillna("unknown")
    v["gang"] = v.victim_id.map(vgang).fillna(False)
    v["location"] = v.location_id.map(LOC).fillna("other")
    ih = inc.set_index("incident_id")
    hr = pd.to_numeric(v.incident_id.map(ih.incident_hour), errors="coerce")
    v["hourband"] = pd.cut(hr, [-1, 5, 11, 17, 23], labels=["00-05", "06-11", "12-17", "18-23"]).astype(object)
    v["hourband"] = v.hourband.where(v.hourband.notna(), "unk")
    ce = v.incident_id.map(ih.cleared_except_id)
    v["exc"] = ce.isin([1, 2, 3, 4, 5])
    keep = ["victim_id", "incident_id", "agency_id", "offence", "vclass", "vtype", "age12", "arrest", "vage",
            "vageband", "vsex", "weapon", "gang", "location", "hourband", "exc"]
    v = v[keep].copy()
    x = frac.reindex(v.incident_id.to_numpy())
    x.index = v.index
    v = pd.concat([v, x], axis=1)
    v["n_known"] = v.incident_id.map(n_known).fillna(0).to_numpy()
    v = v.join(oagg, on="incident_id")
    v = v.join(acnt, on="incident_id")
    acols = [c for c in v.columns if c.startswith("arr_")]
    v[acols] = v[acols].fillna(0).astype(np.int32)
    v["state"], v["year"] = st, yr
    return v


def main(args: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for a in args or ["TX-2022", "TX-2023", "AZ-2022", "AZ-2023", "CA-2022", "CA-2023"]:
        st, yr = a.split("-")
        v = restage(st, int(yr))
        v.to_pickle(OUT / f"{a}.pkl")
        print(f"[restage] {a}: {len(v):,} victimisations; offender-unknown share "
              f"{v.NOINFO.mean():.3f}; weapons {v.weapon.value_counts(normalize=True).round(3).to_dict()}",
              flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])

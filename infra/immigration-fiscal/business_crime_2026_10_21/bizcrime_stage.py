"""Stage one NIBRS state-year for the business-crime lane into small aggregate cells, cached as
_cache/stage/{ST}-{year}.pkl. Reads the zips the offender-ethnicity lane fetched and validated
(../offender_ethnicity_nibrs_2026_09_23/_cache/{ST}-{year}.zip, sha256 pinned in inputs/pins.json)
and reuses that lane's reader and offender/victim coding (nibrs_stage.py), so groups are the same
disjoint classes: Hispanic of any race, then non-Hispanic white, Black and other.

Cells written (every count is a victimisation: one victim of one incident, at its most serious
offence in the group hierarchy below; offenders carry 1/n of it, the sibling lane's "frac" rule):
    pcells  property and fraud offences, by agency x offence group x victim type x retail location
            x cargo flag x arrest flag: n, losses (stolen, damaged/burned, recovered, net), and the
            offender-class weights of n and of net loss
    acells  arrestees by agency x arrest-offence group x class x adult, and whether the incident
            has a business-type victim
    kcells  violent victimisations of individuals under 12, by offence x victim class x
            family/household relationship to an offender
    jcells  violent victimisations of individuals 12+ at a jail/prison location (code 15)
Property value: sum of NIBRS_PROPERTY_DESC.property_value by loss type, each item capped at
CAP_ITEM; an incident's loss is split evenly over its victims of the staged offences.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SIB = FISCAL / "offender_ethnicity_nibrs_2026_09_23"
sys.path.insert(0, str(SIB))
from nibrs_stage import (CODE_OFFENCE, H_CLASSES, OFF_CLASSES, RANK, Zip,  # noqa: E402
                         age_band, offender_class, victim_class)

STAGE = HERE / "_cache" / "stage"
CAP_ITEM = 1_000_000          # $ per property item; NIBRS carries keying errors up to 999,999,999
# Business-property groups, most serious first (one victimisation counts once, at the first).
GROUP_OF = {"120": "robbery", "220": "burglary", "240": "motor_vehicle_theft", "200": "arson",
            "270": "embezzlement", "210": "extortion",
            **{c: "fraud" for c in ["26A", "26B", "26C", "26D", "26E", "26F", "26G", "26H", "250"]},
            "23C": "shoplifting", "23D": "theft_from_building", "23E": "theft_coin_machine",
            **{c: "other_larceny" for c in ["23A", "23B", "23F", "23G", "23H"]},
            "290": "vandalism"}
PGROUPS = ["robbery", "burglary", "motor_vehicle_theft", "arson", "embezzlement", "extortion", "fraud",
           "shoplifting", "theft_from_building", "theft_coin_machine", "other_larceny", "vandalism"]
PRANK = {g: i for i, g in enumerate(PGROUPS)}
VTYPE = {1: "B", 2: "F", 3: "G", 4: "I", 5: "L", 6: "O", 7: "R", 8: "S", 9: "U"}
# NIBRS location codes treated as retail (NRSS sectors): convenience, department/discount, drug
# store/doctor's office/hospital (pooled code), grocery, liquor, service/gas station, specialty, mall.
RETAIL_LOC_IDS = {14, 17, 19, 24, 30, 41, 43, 44}
JAIL_LOC_ID = 28
FAMILY_REL = {"CH", "CF", "CS", "FC", "FP", "GC", "GP", "IL", "OF", "PA", "SB", "SC", "SE", "SP", "SS"}


def frac_weights(od: pd.DataFrame, incidents: np.ndarray) -> pd.DataFrame:
    """Per incident, each recorded offender's class carries 1/n; no recorded offender: NOINFO."""
    od = od[od.incident_id.isin(incidents)]
    known = od[od.offender_seq_num > 0].copy()
    known["cls"] = offender_class(known.race_id, known.ethnicity_id)
    counts = pd.crosstab(known.incident_id, known.cls).reindex(columns=OFF_CLASSES, fill_value=0).astype(float)
    frac = counts.div(counts.sum(axis=1), axis=0)
    noinfo = pd.Index(incidents).difference(frac.index)
    frac = pd.concat([frac, pd.DataFrame(0.0, index=noinfo, columns=OFF_CLASSES).assign(NOINFO=1.0)])
    if not np.allclose(frac.sum(axis=1), 1.0):
        raise SystemExit("[BLOCKED] offender weights do not sum to one")
    return frac


def stage(zpath: Path, st: str, yr: int) -> dict:
    z = Zip(zpath)
    inc = z.read("NIBRS_incident.csv", ["incident_id", "agency_id", "cargo_theft_flag"])
    inc["cargo"] = inc.cargo_theft_flag.astype(str).str.lower().isin(["t", "true", "y", "1"])
    off = z.read("NIBRS_OFFENSE.csv", ["offense_id", "incident_id", "offense_code", "location_id"])
    od = z.read("NIBRS_OFFENDER.csv", ["offender_id", "incident_id", "offender_seq_num", "race_id", "ethnicity_id"])
    vic = z.read("NIBRS_VICTIM.csv", ["victim_id", "incident_id", "victim_type_id", "age_id", "age_num",
                                      "race_id", "ethnicity_id"])
    vo = z.read("NIBRS_VICTIM_OFFENSE.csv", ["victim_id", "offense_id"])
    arrested = set(z.read("NIBRS_ARRESTEE.csv", ["incident_id"]).incident_id)
    vic["vtype"] = vic.victim_type_id.map(VTYPE).fillna("U")

    # ---- property and fraud victimisations ----
    off["group"] = off.offense_code.map(GROUP_OF)
    po = off.dropna(subset=["group"])
    v = vo.merge(po[["offense_id", "incident_id", "group", "location_id"]], on="offense_id")
    v = v.assign(rank=v.group.map(PRANK)).sort_values(["rank", "offense_id"]).drop_duplicates("victim_id")
    v = v.merge(vic[["victim_id", "vtype"]], on="victim_id", how="left")
    v = v.merge(inc[["incident_id", "agency_id", "cargo"]], on="incident_id", how="left")
    v["retail"] = v.location_id.isin(RETAIL_LOC_IDS)
    v["arrest"] = v.incident_id.isin(arrested)
    v["vtype"] = v.vtype.fillna("U")

    prop = z.read("NIBRS_PROPERTY.csv", ["property_id", "incident_id", "prop_loss_id"])
    pdsc = z.read("NIBRS_PROPERTY_DESC.csv", ["property_id", "property_value"])
    pdsc["value"] = pd.to_numeric(pdsc.property_value, errors="coerce").fillna(0).clip(lower=0, upper=CAP_ITEM)
    pv = pdsc.groupby("property_id").value.sum()
    prop["value"] = prop.property_id.map(pv).fillna(0.0)
    kind = prop.prop_loss_id.map({7: "stolen", 4: "damaged", 2: "damaged", 5: "recovered"})
    pl = prop.assign(kind=kind).dropna(subset=["kind"]).pivot_table(index="incident_id", columns="kind",
                                                                       values="value", aggfunc="sum", fill_value=0.0)
    pl = pl.reindex(columns=["stolen", "damaged", "recovered"], fill_value=0.0)
    pl["recovered"] = np.minimum(pl.recovered, pl.stolen)
    pl["net"] = pl.stolen + pl.damaged - pl.recovered
    nvic = v.groupby("incident_id").size()
    for c in ["stolen", "damaged", "recovered", "net"]:
        v[f"loss_{c}"] = v.incident_id.map(pl[c] / nvic.reindex(pl.index)).fillna(0.0)
    fw = frac_weights(od, v.incident_id.unique())
    W = fw.reindex(v.incident_id.to_numpy()).to_numpy()
    for i, k in enumerate(OFF_CLASSES):
        v[f"n_{k}"] = W[:, i]
        v[f"l_{k}"] = W[:, i] * v.loss_net.to_numpy()
    keys = ["agency_id", "group", "vtype", "retail", "cargo", "arrest"]
    vals = ["loss_stolen", "loss_damaged", "loss_recovered", "loss_net"] + [f"n_{k}" for k in OFF_CLASSES] + \
           [f"l_{k}" for k in OFF_CLASSES]
    pcells = v.assign(n=1.0).groupby(keys, observed=True)[["n"] + vals].sum().reset_index()

    # ---- arrestees ----
    ar = z.read("NIBRS_ARRESTEE.csv", ["arrestee_id", "incident_id", "offense_code", "age_id", "age_num",
                                       "race_id", "ethnicity_id"])
    ar["group"] = ar.offense_code.map(GROUP_OF)
    ar = ar.dropna(subset=["group"]).merge(inc[["incident_id", "agency_id"]], on="incident_id")
    biz_inc = set(v.loc[v.vtype.isin(["B", "F", "R", "O"]), "incident_id"])
    ar["biz_incident"] = ar.incident_id.isin(biz_inc)
    ar["cls"] = offender_class(ar.race_id, ar.ethnicity_id)
    ar["age18"] = age_band(ar.age_num, ar.age_id, 18)
    acells = ar.groupby(["agency_id", "group", "biz_incident", "cls", "age18"]).size().rename("arrestees").reset_index()

    # ---- violent: children under 12 and jail/prison locations ----
    off["offence"] = off.offense_code.map(CODE_OFFENCE)
    vio = off.dropna(subset=["offence"])
    w = vo.merge(vio[["offense_id", "incident_id", "offence", "location_id"]], on="offense_id")
    w = w.assign(rank=w.offence.map(RANK)).sort_values(["rank", "offense_id"]).drop_duplicates("victim_id")
    w = w.merge(vic, on="victim_id", how="left", suffixes=("", "_v"))
    w = w[w.vtype.eq("I") & w.offence.ne("Intimidation")].copy()
    w["age12"] = age_band(w.age_num, w.age_id, 12)
    w["vclass"] = victim_class(w.race_id, w.ethnicity_id)
    w = w.merge(inc[["incident_id", "agency_id"]], on="incident_id", how="left")
    rel = z.read("NIBRS_VICTIM_OFFENDER_REL.csv", ["victim_id", "relationship_id"])
    relc = z.read("NIBRS_RELATIONSHIP.csv", ["relationship_id", "relationship_code"])
    rel = rel.merge(relc, on="relationship_id", how="left")
    fam = set(rel.loc[rel.relationship_code.isin(FAMILY_REL), "victim_id"])
    w["family"] = w.victim_id.isin(fam)
    fwv = frac_weights(od, w.incident_id.unique())
    Wv = fwv.reindex(w.incident_id.to_numpy()).to_numpy()
    for i, k in enumerate(OFF_CLASSES):
        w[k] = Wv[:, i]
    kids = w[w.age12.eq("lt12")]
    kcells = kids.groupby(["agency_id", "offence", "vclass", "family"], observed=True)[OFF_CLASSES].sum().reset_index()
    jail = w[w.location_id.eq(JAIL_LOC_ID) & w.age12.ne("lt12")]
    jcells = jail.groupby(["agency_id", "offence", "vclass"], observed=True)[OFF_CLASSES].sum().reset_index()

    info = dict(state=st, year=yr, incidents=len(inc), property_victimisations=len(v),
                property_value_items_capped=int((pd.to_numeric(pdsc.property_value, errors="coerce") > CAP_ITEM).sum()),
                child_victimisations=len(kids), jail_victimisations=len(jail), arrestees=len(ar),
                cargo_incidents=int(inc.cargo.sum()))
    return dict(info=info, pcells=pcells, acells=acells, kcells=kcells, jcells=jcells)


def load(zpath: Path, st: str, yr: int) -> dict:
    """The staged cells, built once; the cache is keyed by this module's own logic, so delete
    _cache/stage after editing it."""
    STAGE.mkdir(parents=True, exist_ok=True)
    out = STAGE / f"{st}-{yr}.pkl"
    if not out.exists():
        pd.to_pickle(stage(zpath, st, yr), out)
    return pd.read_pickle(out)

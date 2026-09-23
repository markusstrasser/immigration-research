"""Stage one NIBRS state-year into small aggregate tables (victimisation, offender and arrestee
cells by agency), cached as _cache/stage/{ST}-{year}.pkl for nibrs_rates.py.

    uv run --no-project python3 nibrs_stage.py TX-2022 TX-2023 AZ-2022 AZ-2023 CA-2022 CA-2023

Offences follow the NCVS violent categories: murder 09A; rape/sexual assault 11A-11D (rape,
sodomy, sexual assault with an object, fondling); robbery 120; aggravated assault 13A; simple
assault 13B; intimidation 13C is staged for a sensitivity only. A victim hit by several of these
offences in one incident is counted once, at the most serious (the NCVS hierarchy).

Offender classes (police-recorded race and ethnicity, disjoint, Hispanic of any race):
    HW HB HO HU     ethnicity Hispanic, recorded race White / Black / other known / unknown
    NHW NHB NHO NHU ethnicity not Hispanic, same race split
    UW UB UO UU     ethnicity unknown, not specified, 'multiple' or blank, same race split
    NOINFO          the incident has only the unknown-offender record (sequence number 0)
All offenders in an incident act in concert on every offence (NIBRS rule), so every victim of the
incident carries the incident's offender set. Attribution methods, per victimisation:
    frac   each recorded offender carries 1/n of the victimisation (central)
    first  the offender with the lowest sequence number carries all of it
    anyH   all of it goes to a Hispanic offender when any recorded offender is Hispanic
    allH   Hispanic only when every recorded offender is Hispanic (the NCVS rule since 2021);
           in mixed groups the Hispanic share moves to the other recorded offenders
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
STAGE = CACHE / "stage"
CODE_OFFENCE = {"09A": "Murder", "11A": "Rape/sexual assault", "11B": "Rape/sexual assault",
                "11C": "Rape/sexual assault", "11D": "Rape/sexual assault", "120": "Robbery",
                "13A": "Aggravated assault", "13B": "Simple assault", "13C": "Intimidation"}
HIER = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault", "Intimidation"]
RANK = {o: i for i, o in enumerate(HIER)}
OFF_CLASSES = ["HW", "HB", "HO", "HU", "NHW", "NHB", "NHO", "NHU", "UW", "UB", "UO", "UU", "NOINFO"]
H_CLASSES = ["HW", "HB", "HO", "HU"]
RACE_OTHER_KNOWN = {30, 40, 41, 42, 43, 50, 60, 70}          # AIAN, Asian, NHPI, legacy codes, multiple
ETH_H, ETH_NH = 10, 20                                        # 30 multiple, 40 unknown, 50 not specified


class Zip:
    """Read members by basename, case-insensitively (2023 files sit in {ST}-{year}/{ST}/)."""

    def __init__(self, path: Path):
        self.z = zipfile.ZipFile(path)
        self.names = {n.split("/")[-1].lower(): n for n in self.z.namelist() if not n.endswith("/")}

    def read(self, table: str, cols: list[str]) -> pd.DataFrame:
        name = self.names[table.lower()]
        with self.z.open(name) as f:
            header = f.readline().decode("utf-8-sig").strip().split(",")
        lower = {h.lower(): h for h in header}
        missing = [c for c in cols if c not in lower]
        if missing:
            raise SystemExit(f"[BLOCKED] {table}: columns {missing} not in header {header}")
        try:
            with self.z.open(name) as f:
                df = pd.read_csv(f, usecols=[lower[c] for c in cols], low_memory=False)
        except UnicodeDecodeError:                            # CA-2023 agencies.csv carries cp1252 bytes
            with self.z.open(name) as f:
                df = pd.read_csv(f, usecols=[lower[c] for c in cols], low_memory=False, encoding="cp1252")
        return df.rename(columns={lower[c]: c for c in cols})


def race_letter(race: pd.Series) -> pd.Series:
    r = pd.Series("U", index=race.index, dtype=object)
    r[race.eq(10)] = "W"
    r[race.eq(20)] = "B"
    r[race.isin(RACE_OTHER_KNOWN)] = "O"
    return r


def offender_class(race: pd.Series, eth: pd.Series) -> pd.Series:
    rl = race_letter(race)
    cls = "U" + rl
    cls[eth.eq(ETH_H)] = "H" + rl[eth.eq(ETH_H)]
    cls[eth.eq(ETH_NH)] = "NH" + rl[eth.eq(ETH_NH)]
    return cls


def victim_class(race: pd.Series, eth: pd.Series) -> pd.Series:
    rl = race_letter(race)
    v = pd.Series("vU", index=race.index, dtype=object)
    v[eth.eq(ETH_H)] = "vH"
    nh = eth.eq(ETH_NH)
    for letter, lab in [("W", "vNHW"), ("B", "vNHB"), ("O", "vNHO"), ("U", "vNHU")]:
        v[nh & rl.eq(letter)] = lab
    return v


def age_band(age_num: pd.Series, age_id: pd.Series, cut: int) -> pd.Series:
    a = pd.to_numeric(age_num, errors="coerce")
    a[age_id.isin([1, 2, 3])] = 0                            # under 24 hours, 1-6 days, 7-364 days
    return pd.Series(np.where(a.isna(), "unk", np.where(a >= cut, f"{cut}p", f"lt{cut}")), index=a.index)


def stage(st: str, yr: int) -> dict:
    z = Zip(CACHE / f"{st}-{yr}.zip")
    ag = z.read("agencies.csv", ["agency_id", "ori", "pub_agency_name", "agency_type_name", "population",
                                 "county_name", "nibrs_off_eth_start_date", "data_year", "state_abbr"])
    if not (ag.data_year.eq(yr).all() and ag.state_abbr.eq(st).all() and ag.agency_id.is_unique):
        raise SystemExit(f"[BLOCKED] {st}-{yr} agencies.csv year/state/unique-id check failed")
    mon = z.read("NIBRS_month.csv", ["agency_id", "month_num", "reported_status"])
    statuses = sorted(mon.reported_status.dropna().unique())
    months = (mon[mon.reported_status.isin(["I", "Z", "R"])].drop_duplicates(["agency_id", "month_num"])
              .groupby("agency_id").size().rename("months"))
    inc = z.read("NIBRS_incident.csv", ["incident_id", "agency_id"])
    off = z.read("NIBRS_OFFENSE.csv", ["offense_id", "incident_id", "offense_code"])
    od = z.read("NIBRS_OFFENDER.csv", ["offender_id", "incident_id", "offender_seq_num", "race_id",
                                       "ethnicity_id", "age_num"])
    if od.incident_id.isin(inc.incident_id).mean() < 0.999 or off.incident_id.isin(inc.incident_id).mean() < 0.999:
        raise SystemExit(f"[BLOCKED] {st}-{yr}: offender/offence rows without an incident")
    # Agency ethnicity recording: share of recorded offenders (all Group A incidents) with
    # ethnicity Hispanic or not Hispanic.
    kn = od[od.offender_seq_num > 0].merge(inc, on="incident_id")
    rec = kn.groupby("agency_id").ethnicity_id.agg(n_known_all="size",
                                                   rec_rate=lambda s: float(s.isin([ETH_H, ETH_NH]).mean()))
    ag = ag.merge(months, left_on="agency_id", right_index=True, how="left").merge(
        rec, left_on="agency_id", right_index=True, how="left")
    ag["months"] = ag.months.fillna(0).astype(int)
    ag["incidents_all"] = ag.agency_id.map(inc.agency_id.value_counts()).fillna(0).astype(int)

    off["offence"] = off.offense_code.map(CODE_OFFENCE)
    offt = off.dropna(subset=["offence"]).merge(inc, on="incident_id")
    target_inc = offt.incident_id.unique()
    inc_off = (offt.assign(rank=offt.offence.map(RANK)).sort_values("rank")
               .drop_duplicates("incident_id").set_index("incident_id")[["offence", "agency_id"]])

    # Offender composition per target incident
    odt = od[od.incident_id.isin(target_inc)].copy()
    unknown_rows = odt.offender_seq_num.eq(0)
    mixed = set(odt.loc[unknown_rows, "incident_id"]) & set(odt.loc[~unknown_rows, "incident_id"])
    known = odt[~unknown_rows].copy()
    known["cls"] = offender_class(known.race_id, known.ethnicity_id)
    counts = pd.crosstab(known.incident_id, known.cls).reindex(columns=OFF_CLASSES, fill_value=0).astype(float)
    n_known = counts.sum(axis=1)
    frac = counts.div(n_known, axis=0)
    noinfo = pd.Index(target_inc).difference(frac.index)
    frac = pd.concat([frac, pd.DataFrame(0.0, index=noinfo, columns=OFF_CLASSES).assign(NOINFO=1.0)])
    first_cls = known.sort_values(["incident_id", "offender_seq_num"]).drop_duplicates("incident_id") \
        .set_index("incident_id").cls
    first = pd.get_dummies(first_cls).reindex(columns=OFF_CLASSES, fill_value=0).astype(float)
    first = pd.concat([first, frac.loc[noinfo]])
    hsum = frac[H_CLASSES].sum(axis=1)
    any_h = hsum > 0
    first_h = known[known.cls.isin(H_CLASSES)].sort_values(["incident_id", "offender_seq_num"]) \
        .drop_duplicates("incident_id").set_index("incident_id").cls
    anyh = frac.copy()
    anyh.loc[any_h[any_h].index] = 0.0
    fh = pd.get_dummies(first_h).reindex(columns=OFF_CLASSES, fill_value=0).astype(float)
    anyh.loc[fh.index] = fh
    allh = frac.copy()
    part = any_h & (hsum < 1 - 1e-9)                          # mixed groups with a Hispanic member
    rest = allh.loc[part].drop(columns=H_CLASSES)
    allh.loc[part, [c for c in OFF_CLASSES if c not in H_CLASSES]] = rest.div(rest.sum(axis=1), axis=0).values
    allh.loc[part, H_CLASSES] = 0.0
    methods = {"frac": frac, "first": first, "anyH": anyh, "allH": allh}
    for m, w in methods.items():
        if not np.allclose(w.sum(axis=1), 1.0):
            raise SystemExit(f"[BLOCKED] {st}-{yr}: {m} weights do not sum to one")

    # Victimisations: each victim once, at the most serious target offence
    vic = z.read("NIBRS_VICTIM.csv", ["victim_id", "incident_id", "victim_type_id", "age_id", "age_num",
                                      "race_id", "ethnicity_id"])
    vo = z.read("NIBRS_VICTIM_OFFENSE.csv", ["victim_id", "offense_id"])
    v = vo.merge(offt[["offense_id", "incident_id", "offence", "agency_id"]], on="offense_id")
    v = v.assign(rank=v.offence.map(RANK)).sort_values("rank").drop_duplicates("victim_id")
    v = v.merge(vic, on="victim_id", how="left", suffixes=("", "_v"))
    if not v.incident_id.eq(v.incident_id_v).all():
        raise SystemExit(f"[BLOCKED] {st}-{yr}: victim-offence links cross incidents")
    v["vclass"] = victim_class(v.race_id, v.ethnicity_id)
    v["vtype"] = v.victim_type_id.map({4: "I", 5: "L"}).fillna("other")
    v["age12"] = age_band(v.age_num, v.age_id, 12)
    arrested = set(z.read("NIBRS_ARRESTEE.csv", ["incident_id"]).incident_id)
    v["arrest"] = v.incident_id.isin(arrested)                # an arrestee is on the incident
    keys = ["agency_id", "offence", "vclass", "vtype", "age12", "arrest"]
    vcells = {}
    for m, w in methods.items():
        x = w.reindex(v.incident_id.to_numpy())
        x.index = v.index
        vcells[m] = pd.concat([v[keys], x], axis=1).groupby(keys, observed=True)[OFF_CLASSES].sum().reset_index()
    nv = len(v)

    # Offender records per incident (the incident's most serious offence), unknown offender = 1
    ok = known[["incident_id", "cls"]].copy()
    ok = pd.concat([ok, pd.DataFrame({"incident_id": noinfo, "cls": "NOINFO"})], ignore_index=True)
    ok = ok.join(inc_off, on="incident_id")
    ocells = ok.groupby(["agency_id", "offence", "cls"]).size().rename("offenders").reset_index()

    # Arrestees: arrest offence as recorded, adult flag for the Table 43C check
    ar = z.read("NIBRS_ARRESTEE.csv", ["arrestee_id", "incident_id", "offense_code", "age_id", "age_num",
                                       "race_id", "ethnicity_id"])
    ar["offence"] = ar.offense_code.map(CODE_OFFENCE)
    ar = ar.dropna(subset=["offence"]).merge(inc, on="incident_id")
    ar["cls"] = offender_class(ar.race_id, ar.ethnicity_id)
    ar["age18"] = age_band(ar.age_num, ar.age_id, 18)
    acells = ar.groupby(["agency_id", "offence", "cls", "age18"]).size().rename("arrestees").reset_index()

    info = dict(state=st, year=yr, month_statuses=statuses, incidents=len(inc), target_incidents=len(target_inc),
                victimisations=nv, known_offenders_target=len(known), unknown_offender_incidents=len(noinfo),
                incidents_with_both_unknown_and_known_offender_records=len(mixed),
                known_offenders_ethnicity_codes=known.ethnicity_id.value_counts(dropna=False).to_dict(),
                arrestees_target=len(ar))
    return dict(info=info, agencies=ag, vcells=vcells, ocells=ocells, acells=acells)


def main(args: list[str]) -> None:
    STAGE.mkdir(parents=True, exist_ok=True)
    for a in args:
        st, yr = a.split("-")
        out = STAGE / f"{st}-{yr}.pkl"
        d = stage(st, int(yr))
        pd.to_pickle(d, out)
        print(f"[stage] {a}: {d['info']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])

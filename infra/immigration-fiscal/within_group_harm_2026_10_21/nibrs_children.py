"""Police-recorded victims of Hispanic offenders by victim age and relationship (NIBRS, read-only).

Reads the FBI CDE state files cached by `offender_ethnicity_nibrs_2026_09_23/_cache/` (never copied or
written there) and returns small cells: state, year, offence, victim class, victim age band, relationship
of the victim to the incident's first recorded Hispanic offender, and the Hispanic share of the incident's
ethnicity-known offenders (each recorded offender carries 1/n; the NIBRS lane's central `frac` rule).

Universe, as in the NIBRS lane: individual victims (type I) of murder 09A, rape and sexual assault
11A-11D, robbery 120, aggravated assault 13A and simple assault 13B, each victim once at the most serious
of these offences; agencies whose recorded offenders carry Hispanic or non-Hispanic ethnicity at least
half the time. Unlike that lane, victims of every age are kept and split at 12 (the NCVS universe starts
at 12). The cells are aggregated per state-year and cached in this lane's `_cache/nibrs_cells/`, keyed by
the source zip's sha256, so a rerun reuses them; a changed zip is re-staged.
"""
from __future__ import annotations

import hashlib

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "offender_ethnicity_nibrs_2026_09_23/_cache"
CELLS = HERE / "_cache/nibrs_cells"
CODE_OFFENCE = {"09A": "Murder", "11A": "Rape/sexual assault", "11B": "Rape/sexual assault",
                "11C": "Rape/sexual assault", "11D": "Rape/sexual assault", "120": "Robbery",
                "13A": "Aggravated assault", "13B": "Simple assault"}
RANK = {o: i for i, o in enumerate(["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault",
                                    "Simple assault"])}
ETH_H, ETH_NH = 10, 20
# Relationship of the victim to the offender, by NIBRS relationship_code (stable across years; the
# numeric ids are not). Family includes the household's children of a partner and foster relations.
REL_CLASS = {
    "CH": "family", "PA": "family", "SB": "family", "GC": "family", "GP": "family", "IL": "family",
    "OF": "family", "SC": "family", "SP": "family", "SS": "family", "CF": "family", "FC": "family",
    "FP": "family",
    "SE": "intimate", "CS": "intimate", "BG": "intimate", "XS": "intimate", "XR": "intimate", "HR": "intimate",
    "AQ": "known", "FR": "known", "NE": "known", "OK": "known", "EE": "known", "ER": "known", "BE": "known",
    "CO": "known",
    "ST": "stranger",
    "RU": "unknown", "VO": "unknown",
}
# Bump when stage() changes: cached cells are keyed by the zip's sha256 and this version (v1 read the
# unknown-age code '00' as age 0).
STAGE_VERSION = "2"
STATE_YEARS = ("TX-2022", "TX-2023", "AZ-2022", "AZ-2023", "CA-2022", "CA-2023")
COLUMNS = ["state", "year", "offence", "vclass", "age", "rel", "victims", "hisp_weight", "known_eth_weight"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Zip:
    """Members by basename, case-insensitively (2023 files sit in {ST}-{year}/{ST}/)."""

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
        dtype = {lower[c]: str for c in cols if c in ("offense_code", "relationship_code")}
        for encoding in ("utf-8", "cp1252"):                # CA-2023 agencies carry cp1252 bytes
            try:
                with self.z.open(name) as f:
                    df = pd.read_csv(f, usecols=[lower[c] for c in cols], dtype=dtype, encoding=encoding,
                                     low_memory=False)
                break
            except UnicodeDecodeError:
                continue
        return df.rename(columns={lower[c]: c for c in cols})


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def victim_class(race: pd.Series, eth: pd.Series) -> pd.Series:
    v = pd.Series("vU", index=eth.index, dtype=object)
    v[eth.eq(ETH_H)] = "vH"
    v[eth.eq(ETH_NH)] = "vNH"
    return v


def age_band(age_num: pd.Series, age_id: pd.Series) -> pd.Series:
    """NIBRS_AGE: ids 1-3 are under a year (codes NN, NB, BB); 103 is code '00', Unknown, and 104 'NS', Not
    specified. age_num carries the code, so '00' must not be read as age 0."""
    a, ids = num(age_num), num(age_id)
    a[ids.isin([1, 2, 3])] = 0
    a[ids.isin([103, 104]) | ids.isna()] = np.nan
    return pd.Series(np.where(a.isna(), "unk", np.where(a >= 12, "12p", "lt12")), index=a.index)


def stage(state_year: str) -> pd.DataFrame:
    st, yr = state_year.split("-")
    z = Zip(SOURCE / f"{state_year}.zip")
    inc = z.read("NIBRS_incident.csv", ["incident_id", "agency_id"])
    od = z.read("NIBRS_OFFENDER.csv", ["offender_id", "incident_id", "offender_seq_num", "ethnicity_id"])
    od["seq"], od["eth"] = num(od.offender_seq_num), num(od.ethnicity_id)
    known = od[od.seq > 0].merge(inc, on="incident_id")
    rec = known.groupby("agency_id").eth.apply(lambda s: float(s.isin([ETH_H, ETH_NH]).mean()))
    keep_agencies = set(rec[rec >= 0.5].index)
    del known
    off = z.read("NIBRS_OFFENSE.csv", ["offense_id", "incident_id", "offense_code"])
    off["offence"] = off.offense_code.map(CODE_OFFENCE)
    off = off.dropna(subset=["offence"]).merge(inc, on="incident_id")
    off = off[off.agency_id.isin(keep_agencies)]
    target = set(off.incident_id)
    odt = od[od.incident_id.isin(target) & (od.seq > 0)].copy()
    odt["h"] = odt.eth.eq(ETH_H).astype(float)
    odt["k"] = odt.eth.isin([ETH_H, ETH_NH]).astype(float)
    per_inc = odt.groupby("incident_id").agg(n=("h", "size"), nh=("h", "sum"), nk=("k", "sum"))
    # First recorded Hispanic offender of the incident, for the relationship.
    first_h = (odt[odt.h.eq(1)].sort_values(["incident_id", "seq"]).drop_duplicates("incident_id")
               .set_index("incident_id").offender_id)
    vic = z.read("NIBRS_VICTIM.csv", ["victim_id", "incident_id", "victim_type_id", "age_id", "age_num",
                                      "race_id", "ethnicity_id"])
    vo = z.read("NIBRS_VICTIM_OFFENSE.csv", ["victim_id", "offense_id"])
    v = vo.merge(off[["offense_id", "incident_id", "offence"]], on="offense_id")
    v = v.assign(rank=v.offence.map(RANK)).sort_values(["rank", "victim_id"]).drop_duplicates("victim_id")
    v = v.merge(vic, on="victim_id", how="left", suffixes=("", "_v"))
    if not v.incident_id.eq(v.incident_id_v).all():
        raise SystemExit(f"[BLOCKED] {state_year}: victim-offence links cross incidents")
    v = v[num(v.victim_type_id).eq(4)].copy()
    v["vclass"] = victim_class(v.race_id, num(v.ethnicity_id))
    v["age"] = age_band(v.age_num, v.age_id)
    v = v.join(per_inc, on="incident_id")
    v[["n", "nh", "nk"]] = v[["n", "nh", "nk"]].fillna(0.0)
    # Hispanic weight: each recorded offender carries 1/n; known-ethnicity weight is the same over H+NH.
    v["hisp_weight"] = np.where(v.n > 0, v.nh / v.n.where(v.n > 0, 1), 0.0)
    v["known_eth_weight"] = np.where(v.n > 0, v.nk / v.n.where(v.n > 0, 1), 0.0)
    v = v[v.nh > 0].copy()
    rel = z.read("NIBRS_VICTIM_OFFENDER_REL.csv", ["victim_id", "offender_id", "relationship_id"])
    codes = z.read("NIBRS_RELATIONSHIP.csv", ["relationship_id", "relationship_code"])
    rel = rel.merge(codes, on="relationship_id", how="left")
    unmapped = set(rel.relationship_code.dropna()) - set(REL_CLASS)
    if unmapped:
        raise SystemExit(f"[BLOCKED] {state_year}: unmapped relationship codes {sorted(unmapped)}")
    v["first_h"] = v.incident_id.map(first_h)
    v = v.merge(rel[["victim_id", "offender_id", "relationship_code"]],
                left_on=["victim_id", "first_h"], right_on=["victim_id", "offender_id"], how="left")
    v["rel"] = v.relationship_code.map(REL_CLASS).fillna("unknown")
    v = v.drop_duplicates("victim_id")
    cells = (v.groupby(["offence", "vclass", "age", "rel"])
             .agg(victims=("victim_id", "size"), hisp_weight=("hisp_weight", "sum"),
                  known_eth_weight=("known_eth_weight", "sum")).reset_index())
    cells.insert(0, "year", int(yr))
    cells.insert(0, "state", st)
    return cells[COLUMNS]


def cells() -> tuple[pd.DataFrame, list[dict]]:
    """All state-years' cells and a manifest of the zips they came from (path, sha256, bytes)."""
    CELLS.mkdir(parents=True, exist_ok=True)
    out, manifest = [], []
    for sy in STATE_YEARS:
        src = SOURCE / f"{sy}.zip"
        if not src.exists():
            raise SystemExit(f"[BLOCKED] missing NIBRS source {src}")
        digest = sha256(src)
        cached = CELLS / f"{sy}.{digest[:16]}.v{STAGE_VERSION}.csv"
        if cached.exists():
            df = pd.read_csv(cached)
        else:
            df = stage(sy)
            df.to_csv(cached, index=False, lineterminator="\n")
            df = pd.read_csv(cached)
        out.append(df)
        manifest.append(dict(path=str(src.relative_to(HERE.parent.parent.parent)), sha256=digest,
                             bytes=src.stat().st_size))
    return pd.concat(out, ignore_index=True), manifest


if __name__ == "__main__":
    df, _ = cells()
    print(df.groupby(["state", "year"]).victims.sum())

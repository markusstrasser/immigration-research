"""Hispanic offending rates per resident from police-recorded NIBRS incidents, Texas and Arizona
2022-2023 (California as a sensitivity), and their national translation for the victim-cost lane.

    uv run --no-project python3 nibrs_rates.py        (after fetch_nibrs.py, acs_denominators.py
                                                       and nibrs_stage.py)

Rates. For offence o and offender group g (Hispanic of any race; non-Hispanic White, Black and
other), V[g,o] = victimisations of residents' victims (individuals aged 12+, the NCVS universe)
attributed to offenders of group g; rate = V / covered residents of g aged 12+. Covered residents
are summed agency by agency: the FBI jurisdiction population x months reported / 12 x the ACS
5-year composition of the agency's place (city police) or of its county net of every city with
its own police (sheriffs). Tribal agencies are left out on both sides.

Unknown offenders. Victimisations whose offender is unknown (no offender record) or whose
recorded offender has no ethnicity are allocated three ways, as the brief asks:
    a   proportional to recorded offenders in the same state-year x offence x victim-ethnicity
        cell, and for an offender whose race is recorded, within that race (central)
    a0  proportional to recorded offenders at state-year x offence level only
    b   all non-Hispanic (by recorded race where known)
    c   all Hispanic
    k   dropped (recorded offenders only; ratios equal a0)

National translation. Relative rates against non-Hispanic whites are carried to the national
population aged 12+ (NCVS 2024 household population, as the victim lane uses):
    S[o] = RR_H P_H / (P_NHW + RR_NHB P_NHB + RR_H P_H + RR_NHO P_NHO)
the share of 2024 national victimisations of offence o committed by Hispanic offenders.
Assumption [INFERENCE]: within-state relative rates in TX/AZ equal national relative rates.
Checks: the same translation applied to NIBRS arrestees is compared with FBI 2023 Table 43C
national arrest shares, and NIBRS homicide with the SHR.

Writes derived/*.csv and derived/rates_log.txt. Every gate stops the run with [BLOCKED].
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from nibrs_stage import H_CLASSES, OFF_CLASSES

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
STAGE = CACHE / "stage"
OUT = HERE / "derived"
FISCAL = HERE.parent
VL = FISCAL / "crime_victim_cost_2026_09_23"
NCVS = FISCAL / "ncvs_victim_offender_2026_09_18"
ARR = FISCAL / "nibrs_arrests_2026_09_16"
HOM = FISCAL / "homicide_cost_2026_09_18"
SHR_SHA256 = "eeedbf5e58a4a2e91d88e8078341210bd2034b57e6d42d0e2de2667020b88a12"
LOG: list[str] = []
STATE_YEARS = [(s, y) for s in ["TX", "AZ", "CA"] for y in [2022, 2023]]
NONFATAL = ["Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]
OFFENCES = ["Murder"] + NONFATAL
GROUPS = ["H", "NHW", "NHB", "NHO"]
POPCOL = {"H": "hisp", "NHW": "nhw", "NHB": "nhb", "NHO": "nho"}
VCLASSES = ["vH", "vNHW", "vNHB", "vNHO", "vNHU", "vU"]


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} — {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


# ---------------------------------------------------------------------------------------
# 1. Agency jurisdictions -> ACS composition
# ---------------------------------------------------------------------------------------
def norm(s: str) -> str:
    s = str(s).lower().replace("&", " and ")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"\bsaint\b", "st", s)
    s = re.sub(r"\bmount\b", "mt", s)
    s = re.sub(r"\bfort\b", "ft", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


KIND = re.compile(r"^(.*?)\s+(city|town|village|CDP|borough|municipality)$")
SUFFIX = re.compile(r"\s+(police department|police dept\.?|police|department of public safety|"
                    r"public safety department|public safety|marshal'?s office|city marshal|marshal)$", re.I)
COUNT_COLS = [f"{g}{s}" for g in ["total", "hisp", "nhw", "nhb", "nho"] for s in ["", "_12", "_18"]] + ["mexican"]


def place_index(places: pd.DataFrame) -> dict[str, list[int]]:
    idx: dict[str, list[int]] = {}
    for i, name in places.name.items():
        base = name.rsplit(",", 1)[0].strip()
        m = KIND.match(base)
        stem = m.group(1) if m else base
        keys = {norm(stem)} | {norm(x) for x in re.findall(r"\((.*?)\)", stem)}
        for k in keys:
            idx.setdefault(k, []).append(i)
    return idx


def match_place(name: str, pop: float, places: pd.DataFrame, idx: dict) -> int | None:
    cands = idx.get(norm(name), [])
    best, err = None, None
    for i in cands:
        kind = KIND.match(places.at[i, "name"].rsplit(",", 1)[0].strip())
        incorporated = kind is not None and kind.group(2) != "CDP"
        tot = places.at[i, "total"]
        if tot <= 0:
            continue
        e = abs(np.log(pop / tot)) if pop > 0 else 0.0
        e += 0 if incorporated else 0.5
        if err is None or e < err:
            best, err = i, e
    if best is None:
        return None
    tot = places.at[best, "total"]
    if pop > 0 and not (0.5 <= pop / tot <= 2.0):
        return None
    return best


def compositions(st: str, yr: int, ag: pd.DataFrame, acs: pd.DataFrame) -> pd.DataFrame:
    """Per-agency covered residents by group (FBI population x months/12 x ACS shares)."""
    a = acs[(acs.acs_year == yr) & (acs.state == st)]
    places = a[a.geo.eq("place")].reset_index(drop=True)
    counties = a[a.geo.eq("county")].reset_index(drop=True)
    counties["key"] = counties.name.map(lambda n: norm(re.sub(r"\s+County$", "", n.rsplit(",", 1)[0].strip())))
    ckey = dict(zip(counties.key, counties.index))
    idx = place_index(places)
    # Every city police agency in the state, reporting or not, comes out of its county's
    # sheriff residual.  NIBRS pub_agency_name where the ORI is known, else the CDE name stripped.
    cde = json.loads((CACHE / f"cde_agencies_{st}.json").read_text())
    cde = pd.DataFrame([x for v in cde.values() for x in v])
    names = {}
    for s2, y2 in STATE_YEARS:
        if s2 == st and (STAGE / f"{s2}-{y2}.pkl").exists():
            g = pd.read_pickle(STAGE / f"{s2}-{y2}.pkl")["agencies"]
            names.update(dict(zip(g.ori, g.pub_agency_name)))
    city = cde[cde.agency_type_name.eq("City")].copy()
    city["name"] = [names.get(o, SUFFIX.sub("", n)) for o, n in zip(city.ori, city.agency_name)]
    city["place"] = [match_place(n, 0, places, idx) for n in city.name]
    city["county_key"] = city.counties.fillna("").map(lambda c: norm(c.split(",")[0]))
    sub = city.dropna(subset=["place"]).drop_duplicates("place")
    resid = counties.copy()
    for ck, grp in sub.groupby("county_key"):
        if ck in ckey:
            resid.loc[ckey[ck], COUNT_COLS] -= places.loc[grp.place.astype(int), COUNT_COLS].sum().values
    resid[COUNT_COLS] = resid[COUNT_COLS].clip(lower=0)
    rows = []
    for r in ag.itertuples():
        typ, pop = r.agency_type_name, float(r.population or 0)
        ck = norm(str(r.county_name).split(",")[0]) if isinstance(r.county_name, str) else ""
        src, geo = "none", None
        if typ == "Tribal":
            src = "tribal_excluded"
        elif typ == "City":
            p = match_place(r.pub_agency_name, pop, places, idx)
            if p is not None:
                src, geo = "place", places.loc[p]
            elif ck in ckey:
                src, geo = "county_fallback", counties.loc[ckey[ck]]
        elif typ == "County" and ck in ckey:
            geo = resid.loc[ckey[ck]]
            src = "county_residual"
            if geo.total < 0.2 * pop:
                src, geo = "county_fallback", counties.loc[ckey[ck]]
        elif pop > 0 and ck in ckey:
            src, geo = "county_fallback", counties.loc[ckey[ck]]
        w = pop * r.months / 12.0
        row = dict(agency_id=r.agency_id, comp_source=src, covered_pop=w if src != "tribal_excluded" else 0.0)
        for c in COUNT_COLS:
            row[f"c_{c}"] = (w * geo[c] / geo["total"]) if (geo is not None and geo["total"] > 0 and pop > 0) else 0.0
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------
# 2. Allocation of unknown offenders
# ---------------------------------------------------------------------------------------
def _split(num: np.ndarray, fb: np.ndarray) -> np.ndarray:
    """Row shares of num (n x k), falling back to fb (n x k) rows, then to equal shares."""
    s = num.sum(axis=1, keepdims=True)
    f = fb.sum(axis=1, keepdims=True)
    k = num.shape[1]
    return np.where(s > 0, num / np.where(s > 0, s, 1), np.where(f > 0, fb / np.where(f > 0, f, 1), 1.0 / k))


def allocate(c: pd.DataFrame, method: str) -> pd.DataFrame:
    """c: rows = cells (state, year, offence, vclass), columns OFF_CLASSES. Returns H/NHW/NHB/NHO."""
    lvl = [n for n in c.index.names if n != "vclass"]
    fb = c.groupby(level=lvl).sum().reindex(c.index.droplevel("vclass")).to_numpy()
    X = c[OFF_CLASSES].to_numpy()
    col = {k: i for i, k in enumerate(OFF_CLASSES)}

    def v(M, *ks):
        return sum(M[:, col[k]] for k in ks)

    def nh3(M):
        return np.column_stack([v(M, "NHW"), v(M, "NHB"), v(M, "NHO")])

    # shares come from the cell (a, b) or from the offence level pooled over victims (a0)
    cell = fb if method == "a0" else X
    nh_share = _split(nh3(cell), nh3(fb))                  # splits non-Hispanic, race unknown
    known = np.column_stack([v(X, *H_CLASSES), nh3(X) + v(X, "NHU")[:, None] * nh_share])
    unknown = v(X, "UW", "UB", "UO", "UU", "NOINFO")
    out = known.copy()
    if method == "c":
        out[:, 0] += unknown
    elif method == "b":
        out[:, 1] += v(X, "UW")
        out[:, 2] += v(X, "UB")
        out[:, 3] += v(X, "UO")
        out[:, 1:] += v(X, "UU", "NOINFO")[:, None] * nh_share
    elif method in ("a", "a0"):
        overall = _split(np.column_stack([v(cell, *H_CLASSES), nh3(cell) + v(cell, "NHU")[:, None] * nh_share]),
                         np.column_stack([v(fb, *H_CLASSES), nh3(fb) + v(fb, "NHU")[:, None] * nh_share]))
        if method == "a0":
            out += unknown[:, None] * overall
        else:
            # recorded race, unknown ethnicity: Hispanic vs non-Hispanic within that race
            for u, hk, nk, j in [("UW", "HW", "NHW", 1), ("UB", "HB", "NHB", 2), ("UO", "HO", "NHO", 3)]:
                pair_cell = np.column_stack([v(cell, hk), v(cell, nk)])
                pair_fb = np.column_stack([v(fb, hk), v(fb, nk)])
                none = (pair_cell.sum(axis=1) + pair_fb.sum(axis=1)) == 0
                q = _split(pair_cell, pair_fb)
                q[none] = _split(overall[:, [0, j]], overall[:, [0, j]])[none]
                out[:, 0] += v(X, u) * q[:, 0]
                out[:, j] += v(X, u) * q[:, 1]
            out += v(X, "UU", "NOINFO")[:, None] * overall
    elif method != "k":
        raise ValueError(method)
    tot_in = X.sum(axis=1) if method != "k" else (X.sum(axis=1) - v(X, "UW", "UB", "UO", "UU", "NOINFO"))
    if not np.allclose(out.sum(axis=1), tot_in):
        raise SystemExit(f"[BLOCKED] allocation {method} does not conserve victimisations")
    return pd.DataFrame(out, index=c.index, columns=GROUPS)


# ---------------------------------------------------------------------------------------
# 3. Specifications
# ---------------------------------------------------------------------------------------
CENTRAL = dict(states=("TX", "AZ"), years=(2022, 2023), attrib="frac", alloc="a", thresh=0.5,
               eth_start=False, months12=False, vtypes=("I",), ages=("12p", "unk"), denom="_12",
               simple="13B", transfer="vector")


def spec_cells(stages: dict, sp: dict) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    cells, pops, kept = [], [], []
    for (st, yr), d in stages.items():
        if st not in sp["states"] or yr not in sp["years"]:
            continue
        ag = d["agencies"]
        keep = ag[ag.comp_source.ne("tribal_excluded") & ag.rec_rate.fillna(0).ge(sp["thresh"])]
        if sp["eth_start"]:
            start = pd.to_datetime(keep.nibrs_off_eth_start_date, errors="coerce")
            keep = keep[start.le(pd.Timestamp(f"{yr}-01-01"))]
        if sp["months12"]:
            keep = keep[keep.months.eq(12)]
        vc = d["vcells"][sp["attrib"]]
        vc = vc[vc.agency_id.isin(keep.agency_id) & vc.vtype.isin(sp["vtypes"]) & vc.age12.isin(sp["ages"])].copy()
        if sp.get("arrest_only"):
            vc = vc[vc.arrest]
        if sp["simple"] == "13B+13C":
            vc.loc[vc.offence.eq("Intimidation"), "offence"] = "Simple assault"
        vc = vc[vc.offence.isin(OFFENCES)]
        c = vc.groupby(["offence", "vclass"])[OFF_CLASSES].sum()
        c = pd.concat({(st, yr): c}, names=["state", "year"])
        cells.append(c)
        pops.append(keep[[f"c_{g}{sp['denom']}" for g in ["total", "hisp", "nhw", "nhb", "nho"]]
                         + ["c_mexican", "covered_pop"]].sum().rename((st, yr)))
        kept.append(keep.assign(state=st, year=yr))
    return pd.concat(cells), pd.DataFrame(pops), pd.concat(kept)


def national_pops() -> dict[str, dict[str, float]]:
    """NCVS 2024 household population 12+ (the victim lane's denominators) and Census NC-EST2024
    July 2023/2024 resident population by age, for all-ages and adult translations."""
    p = pd.read_csv(NCVS / "derived/cv_population_12plus.csv")
    p = p[p.year.eq(2024)].set_index("group").population
    out = {"ncvs2024_12": {"H": p["Hispanic"], "NHW": p["White"], "NHB": p["Black"], "NHO": p["Asian"] + p["Other"]}}
    for yr, f in [(2023, "nc-est2024-alldata-h-file08.csv"), (2024, "nc-est2024-alldata-h-file10.csv")]:
        acc = {k: {"all": 0.0, "12": 0.0, "18": 0.0} for k in ["TOT", "H", "NHWA", "NHBA"]}
        with (ARR / "_cache" / f).open() as fh:
            for row in csv.DictReader(fh):
                if int(row["MONTH"]) != 7 or int(row["AGE"]) == 999:
                    continue
                age = int(row["AGE"])
                for k in acc:
                    x = float(row[f"{k}_MALE"]) + float(row[f"{k}_FEMALE"])
                    acc[k]["all"] += x
                    acc[k]["12"] += x if age >= 12 else 0.0
                    acc[k]["18"] += x if age >= 18 else 0.0
        for a in ["all", "12", "18"]:
            out[f"ncest{yr}_{a}"] = {"H": acc["H"][a], "NHW": acc["NHWA"][a], "NHB": acc["NHBA"][a],
                                    "NHO": acc["TOT"][a] - acc["H"][a] - acc["NHWA"][a] - acc["NHBA"][a]}
    return out


def results(stages: dict, sp: dict, natpop: dict, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    cells, pops, _ = spec_cells(stages, sp)
    al = allocate(cells, sp["alloc"])
    V = al.groupby(level="offence").sum().reindex(OFFENCES)
    P = pops.sum()
    d = sp["denom"]
    Pg = {g: P[f"c_{POPCOL[g]}{d}"] for g in GROUPS}
    Ptot = P[f"c_total{d}"]
    nat = natpop["ncvs2024_12"] if d == "_12" else natpop["ncest2024_all"]
    rows = []
    for o in OFFENCES:
        r = {g: V.loc[o, g] / Pg[g] * 1000 for g in GROUPS}
        rall = V.loc[o].sum() / Ptot * 1000
        RR = {g: r[g] / r["NHW"] for g in GROUPS}
        S_vec = RR["H"] * nat["H"] / sum(RR[g] * nat[g] for g in GROUPS)
        S_all = r["H"] / rall * nat["H"] / sum(nat.values())
        tot_w = cells.xs(o, level="offence")[OFF_CLASSES].sum()
        rows.append(dict(spec=name, offence=o, victimisations=float(tot_w.sum()),
                         **{f"V_{g}": V.loc[o, g] for g in GROUPS},
                         **{f"pop_{g}": Pg[g] for g in GROUPS}, pop_total=Ptot,
                         **{f"rate_{g}": r[g] for g in GROUPS}, rate_all=rall,
                         RR_H_NHW=RR["H"], RR_NHB_NHW=RR["NHB"], RR_NHO_NHW=RR["NHO"], RR_H_all=r["H"] / rall,
                         local_share_H=V.loc[o, "H"] / V.loc[o].sum(),
                         local_pop_share_H=Pg["H"] / Ptot,
                         national_share_H=S_vec if sp["transfer"] == "vector" else S_all,
                         national_share_H_vector=S_vec, national_share_H_vs_all=S_all,
                         share_noinfo=tot_w["NOINFO"] / tot_w.sum(),
                         share_eth_unknown=tot_w[["UW", "UB", "UO", "UU"]].sum() / tot_w.sum(),
                         share_nh_race_unknown=tot_w["NHU"] / tot_w.sum()))
    vd = al["H"].groupby(level=["offence", "vclass"]).sum().unstack("vclass").reindex(columns=VCLASSES, fill_value=0)
    vd.insert(0, "spec", name)
    return pd.DataFrame(rows), vd.reset_index()


def specs() -> list[tuple[str, dict]]:
    c = CENTRAL
    out = [("central", c)]
    for a in ["a0", "b", "c", "k"]:
        out.append((f"alloc={a}", {**c, "alloc": a}))
    for t in [0.0, 0.8, 0.95]:
        out.append((f"agencies: ethnicity recorded >= {t:.0%}", {**c, "thresh": t}))
    out.append(("agencies: offender-ethnicity start date by Jan 1", {**c, "eth_start": True}))
    out.append(("agencies: 12 months reported", {**c, "months12": True}))
    for s in [("TX",), ("AZ",), ("CA",), ("TX", "AZ", "CA")]:
        out.append((f"states={'+'.join(s)}", {**c, "states": s}))
    for y in [(2022,), (2023,)]:
        out.append((f"year={y[0]}", {**c, "years": y}))
    for m in ["first", "anyH", "allH"]:
        out.append((f"attribution={m}", {**c, "attrib": m}))
    out.append(("victims: all ages", {**c, "ages": ("lt12", "12p", "unk")}))
    out.append(("victims: individuals + officers", {**c, "vtypes": ("I", "L")}))
    out.append(("denominator: all ages", {**c, "denom": ""}))
    out.append(("simple assault incl. intimidation 13C", {**c, "simple": "13B+13C"}))
    out.append(("translation: rate vs all residents", {**c, "transfer": "all"}))
    out.append(("incidents with an arrest only", {**c, "arrest_only": True}))
    for a in ["b", "c"]:
        out.append((f"states=TX+AZ+CA, alloc={a}", {**c, "states": ("TX", "AZ", "CA"), "alloc": a}))
    return out


# ---------------------------------------------------------------------------------------
# 4. Checks: arrestees, homicide against SHR, victim ethnicity transfer
# ---------------------------------------------------------------------------------------
def arrestee_results(stages: dict, sp: dict, natpop: dict) -> pd.DataFrame:
    rows = []
    for adult in [False, True]:
        cells, pops = [], []
        for (st, yr), d in stages.items():
            if st not in sp["states"] or yr not in sp["years"]:
                continue
            ag = d["agencies"]
            keep = ag[ag.comp_source.ne("tribal_excluded") & ag.rec_rate.fillna(0).ge(sp["thresh"])]
            a = d["acells"]
            a = a[a.agency_id.isin(keep.agency_id) & a.offence.isin(OFFENCES)]
            if adult:
                a = a[a.age18.eq("18p")]
            c = a.groupby(["offence", "cls"]).arrestees.sum().unstack("cls", fill_value=0).reindex(columns=OFF_CLASSES,
                                                                                                    fill_value=0)
            c["vclass"] = "all"
            c = c.set_index("vclass", append=True)
            cells.append(pd.concat({(st, yr): c}, names=["state", "year"]))
            sfx = "_18" if adult else "_12"
            pops.append(keep[[f"c_{g}{sfx}" for g in ["total", "hisp", "nhw", "nhb", "nho"]]].sum())
        cells = pd.concat(cells).astype(float)
        P = pd.concat(pops, axis=1).sum(axis=1)
        sfx = "_18" if adult else "_12"
        nat = natpop["ncest2023_18"] if adult else natpop["ncvs2024_12"]
        for alloc in ["a", "k", "b", "c"]:
            al = allocate(cells, alloc).groupby(level="offence").sum()
            for o in al.index:
                r = {g: al.loc[o, g] / P[f"c_{POPCOL[g]}{sfx}"] for g in GROUPS}
                RR = {g: r[g] / r["NHW"] for g in GROUPS}
                rows.append(dict(arrestees="adults 18+" if adult else "all ages", alloc=alloc, offence=o,
                                 arrestees_n=float(cells.xs(o, level="offence").to_numpy().sum()),
                                 eth_unknown_share=float(cells.xs(o, level="offence")[["UW", "UB", "UO", "UU"]].to_numpy().sum()
                                                         / cells.xs(o, level="offence").to_numpy().sum()),
                                 RR_H_NHW=RR["H"], RR_NHB_NHW=RR["NHB"],
                                 local_share_H=al.loc[o, "H"] / al.loc[o].sum(),
                                 national_share_H=RR["H"] * nat["H"] / sum(RR[g] * nat[g] for g in GROUPS)))
    return pd.DataFrame(rows)


def shr_state_check(stages: dict) -> pd.DataFrame:
    """Hispanic share of recorded homicide offenders, TX and AZ 2022-2023: NIBRS 09A victims (first
    offender, recorded ethnicity) against the SHR (MAP compilation, cleared, first offender)."""
    raw = HOM / "_cache/SHR76_25a.csv"
    h = hashlib.sha256()
    with open(raw, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    gate("SHR76_25a.csv sha256 equals the homicide lane's pin", h.hexdigest() == SHR_SHA256, h.hexdigest()[:12])
    df = pd.read_csv(raw, usecols=["Year", "State", "Solved", "Homicide", "Circumstance", "VicRace", "VicEthnic",
                                   "OffRace", "OffEthnic"], low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")
            & ~df.Circumstance.isin({"Felon killed by police", "Felon killed by private citizen"})
            & df.Year.between(2022, 2023) & df.State.isin(["Texas", "Arizona"])]

    def eth(race, ethnic):                                 # the homicide lane's coding, replicated
        out = pd.Series("unknown", index=race.index, dtype=object)
        nonh = ethnic.eq("Not of Hispanic origin")
        out[nonh & race.eq("White")] = "NHW"
        out[nonh & race.eq("Black")] = "NHB"
        out[nonh & race.isin(["Asian", "American Indian or Alaskan Native", "Native Hawaiian or Pacific Islander"])] = "NHO"
        out[ethnic.eq("Hispanic origin")] = "H"
        return out

    df["off"] = eth(df.OffRace, df.OffEthnic)
    df["vic"] = eth(df.VicRace, df.VicEthnic)
    rows = []
    for st in ["Texas", "Arizona"]:
        d = df[df.State.eq(st)]
        k = d[d.Solved.eq("Yes") & d.off.isin(GROUPS)]
        rows.append(dict(source="SHR (MAP)", state=st, victims=len(d), cleared_known_offender=len(k),
                         share_offender_H=k.off.eq("H").mean(),
                         p_off_H_given_vic_H=k[k.vic.eq("H")].off.eq("H").mean(),
                         p_off_H_given_vic_NHW=k[k.vic.eq("NHW")].off.eq("H").mean(),
                         share_H_victims_of_H_offenders=k[k.off.eq("H")].vic.eq("H").mean()))
    for st, nm in [("TX", "Texas"), ("AZ", "Arizona")]:
        tot = None
        for yr in [2022, 2023]:
            vc = stages[(st, yr)]["vcells"]["first"]
            vc = vc[vc.offence.eq("Murder") & vc.vtype.eq("I")]
            c = vc.groupby("vclass")[OFF_CLASSES].sum()
            tot = c if tot is None else tot.add(c, fill_value=0)
        kn = tot[H_CLASSES + ["NHW", "NHB", "NHO"]]
        hh = kn[H_CLASSES].sum(axis=1)
        allk = kn.sum(axis=1)
        rows.append(dict(source="NIBRS 09A (first offender, recorded ethnicity)", state=nm,
                         victims=float(tot.to_numpy().sum()), cleared_known_offender=float(allk.sum()),
                         share_offender_H=float(hh.sum() / allk.sum()),
                         p_off_H_given_vic_H=float(hh.get("vH", 0) / allk.get("vH", np.nan)),
                         p_off_H_given_vic_NHW=float(hh.get("vNHW", 0) / allk.get("vNHW", np.nan)),
                         share_H_victims_of_H_offenders=float(hh.get("vH", 0) / hh[[c for c in hh.index if c != "vU"]].sum())))
    return pd.DataFrame(rows)


def exposure_transfer(vd_central: pd.DataFrame, cen_rows: pd.DataFrame, stages: dict) -> pd.DataFrame:
    """Share of Hispanic-offender victims who are Hispanic, TX/AZ observed -> national, through the
    tract Hispanic share of the offender's neighbourhood: P = mean_w logistic(logit(e_t) + delta).
    delta is solved on TX+AZ tracts weighted by each state's Hispanic-offender victimisations and
    applied to all US tracts weighted by Mexican-origin residents. Validation: the same model for
    non-Hispanic offenders against NCVS's national 0.140."""
    t = load_tracts()
    gate("victim lane tract B03001 cache: 51 state files, national Mexican share of Hispanics 0.586",
         t.state.nunique() == 51 and round(t.B03001_004E.sum() / t.B03001_003E.sum(), 3) == 0.586,
         f"{len(t):,} tracts, {t.B03001_004E.sum() / t.B03001_003E.sum():.4f}")
    e = (t.B03001_003E / t.B03001_001E).clip(0.001, 0.999).to_numpy()
    le = np.log(e / (1 - e))

    def model(delta, w):
        return float((w / (1 + np.exp(-(le + delta)))).sum() / w.sum())

    def solve(target, w):
        lo, hi = -10.0, 10.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if model(mid, w) < target else (lo, mid)
        return (lo + hi) / 2

    st_fips = {"TX": "48", "AZ": "04"}
    # observed shares by state from the central victimisation cells (H offenders, allocated)
    obs = {}
    for st in ["TX", "AZ"]:
        sp = {**CENTRAL, "states": (st,)}
        cells, _, _ = spec_cells(stages, sp)
        al = allocate(cells, "a")
        obs[st] = al.groupby(level=["offence", "vclass"]).sum()
    rows = []
    for o in OFFENCES:
        for who in ["H", "NH"]:
            w = np.zeros(len(t))
            num = den = 0.0
            for st, fips in st_fips.items():
                x = obs[st].xs(o, level="offence")
                x = x[x.index != "vU"]
                grp = x["H"] if who == "H" else x[["NHW", "NHB", "NHO"]].sum(axis=1)
                num += float(grp.get("vH", 0.0))
                den += float(grp.sum())
                m = (t.state == fips).to_numpy()
                base = (t.B03001_003E if who == "H" else t.B03001_001E - t.B03001_003E).to_numpy()
                w[m] = base[m] / base[m].sum() * float(grp.sum())
            p_obs = num / den
            delta = solve(p_obs, w)
            wn = (t.B03001_004E if who == "H" else t.B03001_001E - t.B03001_003E).to_numpy().astype(float)
            rows.append(dict(offence=o, offenders=who, p_victim_hispanic_txaz=p_obs, delta=delta,
                             txaz_exposure_mean=model(0.0, w), national_exposure_mean=model(0.0, wn),
                             p_victim_hispanic_national=model(delta, wn)))
    out = pd.DataFrame(rows)
    # National benchmarks: SHR homicide (police-recorded, cleared, first offender; the victim
    # lane's matrix) and NCVS non-fatal violence (victim-perceived offender; NCVS lane matrix).
    m = pd.read_csv(VL / "derived/shr_victim_by_first_offender.csv")
    g4 = ["hispanic", "nh_white", "nh_black", "nh_other"]
    bench = {}
    for w in ["2024", "2022_2024"]:
        k = m[m.window.astype(str).eq(w)].pivot_table(index="vic_eth", columns="off_eth", values="victims",
                                                      aggfunc="sum").loc[g4, g4]
        nh = k[["nh_white", "nh_black", "nh_other"]].sum(axis=1)
        bench[f"shr_{w}"] = (k.loc["hispanic", "hispanic"] / k["hispanic"].sum(), nh["hispanic"] / nh.sum())
    x = pd.read_csv(NCVS / "derived/matrix_pooled_2022_2024.csv").pivot_table(index="victim", columns="offender",
                                                                               values="count", aggfunc="sum")
    known = ["White", "Black", "Hispanic", "Other"]
    nh = x.loc[known, ["White", "Black", "Other"]].sum(axis=1)
    bench["ncvs_2022_2024"] = (x.loc["Hispanic", "Hispanic"] / x.loc[known, "Hispanic"].sum(), nh["Hispanic"] / nh.sum())
    for b, (ph, pnh) in bench.items():
        out[f"benchmark_{b}"] = np.where(out.offenders.eq("H"), ph, pnh)
    return out


def load_tracts() -> pd.DataFrame:
    frames = []
    for f in sorted((VL / "_cache").glob("acs5_2024_b03001_tract_*.json")):
        d = json.loads(f.read_text())
        frames.append(pd.DataFrame(d[1:], columns=d[0]))
    t = pd.concat(frames, ignore_index=True)
    for c in ["B03001_001E", "B03001_003E", "B03001_004E"]:
        t[c] = pd.to_numeric(t[c])
    return t[t.B03001_001E > 0].reset_index(drop=True)


def offender_given_victim(stages: dict, specs_: list[tuple[str, dict]]) -> pd.DataFrame:
    """P(offender Hispanic | victim group), the victim-conditional input the victim lane uses for
    homicide, from NIBRS and carried to the nation through the victims' tract exposure:
        P = mean_w logistic(logit(e_t) + delta_g),  e_t = tract Hispanic share,
    w = victim group's residents (Hispanic or non-Hispanic) in the spec's states, each state
    weighted by its victimisations of that group; national w = the group's residents in every
    tract. Benchmarks: SHR national homicide by victim group and NCVS perceived offenders."""
    t = load_tracts()
    e = (t.B03001_003E / t.B03001_001E).clip(0.001, 0.999).to_numpy()
    le = np.log(e / (1 - e))
    res = {"H": t.B03001_003E.to_numpy().astype(float), "NH": (t.B03001_001E - t.B03001_003E).to_numpy().astype(float)}
    fips = {"TX": "48", "AZ": "04", "CA": "06"}

    def model(delta, w):
        return float((w / (1 + np.exp(-(le + delta)))).sum() / w.sum())

    def solve(target, w):
        lo, hi = -12.0, 12.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if model(mid, w) < target else (lo, mid)
        return (lo + hi) / 2

    shr = pd.read_csv(VL / "derived/shr_p_offender_given_victim.csv")
    won = pd.read_csv(VL / "derived/wonder_2024_homicide_victims.csv").set_index("group").deaths
    bench = {}
    for w_ in ["2024", "2022_2024"]:
        s = shr[shr.window.astype(str).eq(w_)].set_index("victim")
        nh = ["nh_white", "nh_black", "nh_other"]
        bench[w_] = {"H": float(s.loc["hispanic", "p_off_hispanic"]),
                     "NH": float((s.loc[nh, "p_off_hispanic"] * won[nh]).sum() / won[nh].sum())}
    rows = []
    for name, sp in specs_:
        per_state = {}
        for st in sp["states"]:
            cells, _, _ = spec_cells(stages, {**sp, "states": (st,)})
            per_state[st] = allocate(cells, sp["alloc"]).groupby(level=["offence", "vclass"]).sum()
        for o in OFFENCES:
            for g, vcls in [("H", ["vH"]), ("NH", ["vNHW", "vNHB", "vNHO", "vNHU"])]:
                w = np.zeros(len(t))
                num = den = 0.0
                for st, al in per_state.items():
                    x = al.xs(o, level="offence").reindex(vcls).fillna(0.0)
                    h, tot = float(x["H"].sum()), float(x.sum(axis=1).sum())
                    num, den = num + h, den + tot
                    m = (t.state == fips[st]).to_numpy()
                    w[m] = res[g][m] / res[g][m].sum() * tot
                p_obs = num / den
                delta = solve(p_obs, w)
                rows.append(dict(spec=name, offence=o, victims=g, victimisations_local=den,
                                 p_off_hispanic_local=p_obs, delta=delta,
                                 local_exposure=model(0.0, w), national_exposure=model(0.0, res[g]),
                                 p_off_hispanic_national=model(delta, res[g])))
        # SHR calibration: shift delta (logit scale) so that the model reproduces national SHR
        # homicide for this spec's murder row, and apply the same shift to non-fatal offences
        # (2024 target central; the 2022-2024 target as a sensitivity)
        for g in ["H", "NH"]:
            mrow = next(r for r in rows if r["spec"] == name and r["offence"] == "Murder" and r["victims"] == g)
            for w_, col in [("2024", "p_off_hispanic_national_shr_calibrated"),
                            ("2022_2024", "p_off_hispanic_national_shr2224_calibrated")]:
                shift = solve(bench[w_][g], res[g]) - mrow["delta"]
                for r in rows:
                    if r["spec"] == name and r["victims"] == g:
                        if w_ == "2024":
                            r["shr_logit_shift"] = shift
                        r[col] = model(r["delta"] + shift, res[g])
    out = pd.DataFrame(rows)
    for w_ in ["2024", "2022_2024"]:
        out[f"benchmark_shr_{w_}"] = np.where(out.victims.eq("H"), bench[w_]["H"], bench[w_]["NH"])
    x = pd.read_csv(NCVS / "derived/matrix_pooled_2022_2024.csv").pivot_table(index="victim", columns="offender",
                                                                               values="count", aggfunc="sum")
    known = ["White", "Black", "Hispanic", "Other"]
    kh = x.loc["Hispanic", known]
    knh = x.loc[["White", "Black", "Other"], known].sum()
    out["benchmark_ncvs_2022_2024"] = np.where(out.victims.eq("H"), kh["Hispanic"] / kh.sum(), knh["Hispanic"] / knh.sum())
    return out


# ---------------------------------------------------------------------------------------
def main() -> None:
    OUT.mkdir(exist_ok=True)
    acs = pd.read_csv(OUT / "acs5_place_county_groups.csv")
    stages = {}
    cov = []
    for st, yr in STATE_YEARS:
        d = pd.read_pickle(STAGE / f"{st}-{yr}.pkl")
        comp = compositions(st, yr, d["agencies"], acs)
        d["agencies"] = d["agencies"].merge(comp, on="agency_id", how="left")
        stages[(st, yr)] = d
        ag = d["agencies"]
        v = d["vcells"]["frac"]
        v = v[v.offence.isin(OFFENCES) & v.vtype.eq("I")]
        vv = v.groupby("agency_id")[OFF_CLASSES].sum().sum(axis=1)
        ag["victimisations_violent"] = ag.agency_id.map(vv).fillna(0)
        st_acs = acs[(acs.acs_year == yr) & (acs.state == st) & acs.geo.eq("county")][["total", "hisp", "mexican"]].sum()
        nontribal = ag[ag.comp_source.ne("tribal_excluded")]
        rec50 = nontribal[nontribal.rec_rate.fillna(0).ge(0.5)]
        cov.append(dict(state=st, year=yr, agencies=len(ag), agencies_tribal=int(ag.comp_source.eq("tribal_excluded").sum()),
                        fbi_population_nibrs_agencies=float(ag.population.sum()),
                        covered_pop_months_weighted=float(nontribal.covered_pop.sum()),
                        acs_state_population=float(st_acs.total),
                        coverage_share=float(nontribal.covered_pop.sum() / st_acs.total),
                        coverage_share_recording50=float(rec50.covered_pop.sum() / st_acs.total),
                        hispanic_covered_share=float(nontribal.c_hisp.sum() / st_acs.hisp),
                        hispanic_covered_share_recording50=float(rec50.c_hisp.sum() / st_acs.hisp),
                        mexican_share_of_hispanic_covered=float(rec50.c_mexican.sum() / rec50.c_hisp.sum()),
                        pop_share_place=float(nontribal.loc[nontribal.comp_source.eq("place"), "covered_pop"].sum() / nontribal.covered_pop.sum()),
                        pop_share_county_residual=float(nontribal.loc[nontribal.comp_source.eq("county_residual"), "covered_pop"].sum() / nontribal.covered_pop.sum()),
                        pop_share_county_fallback=float(nontribal.loc[nontribal.comp_source.eq("county_fallback"), "covered_pop"].sum() / nontribal.covered_pop.sum()),
                        victimisations_violent=float(vv.sum()),
                        victimisations_share_recording50=float(ag.loc[ag.agency_id.isin(rec50.agency_id), "victimisations_violent"].sum() / vv.sum()),
                        victimisations_share_zero_population_agencies=float(ag.loc[ag.population.fillna(0).eq(0), "victimisations_violent"].sum() / vv.sum()),
                        **{k: d["info"][k] for k in ["incidents", "target_incidents", "victimisations", "known_offenders_target",
                                                       "unknown_offender_incidents"]}))
    cov = pd.DataFrame(cov)
    cov.to_csv(OUT / "coverage_by_state_year.csv", index=False, float_format="%.4f")
    say("-- Coverage by state-year --")
    say(cov[["state", "year", "agencies", "coverage_share", "coverage_share_recording50", "hispanic_covered_share_recording50",
             "mexican_share_of_hispanic_covered", "pop_share_place", "pop_share_county_residual", "pop_share_county_fallback",
             "victimisations_share_recording50", "victimisations_share_zero_population_agencies"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    gate("TX covered population within 5% of the FBI participation file (98.6%, 99.2%)",
         all(abs(r.coverage_share - t) < 0.05 for r, t in zip(cov[cov.state.eq("TX")].itertuples(), [0.986, 0.992])),
         ", ".join(f"{r.year} {r.coverage_share:.3f}" for r in cov[cov.state.eq("TX")].itertuples()))

    agcols = ["state", "year", "agency_id", "ori", "pub_agency_name", "agency_type_name", "population", "months",
              "n_known_all", "rec_rate", "nibrs_off_eth_start_date", "comp_source", "covered_pop", "victimisations_violent"]
    pd.concat([d["agencies"].assign(state=st, year=yr) for (st, yr), d in stages.items()])[agcols] \
        .to_csv(OUT / "agency_recording_rates.csv", index=False, float_format="%.4f")
    # recording-rate distribution, weighted by violent victimisations
    dist = []
    for (st, yr), d in stages.items():
        ag = d["agencies"]
        b = pd.cut(ag.rec_rate.fillna(0), [-0.001, 0.0001, 0.25, 0.5, 0.8, 0.95, 1.0])
        g = ag.groupby(b, observed=False).agg(agencies=("agency_id", "size"), victimisations=("victimisations_violent", "sum"),
                                              covered_pop=("covered_pop", "sum"))
        g["state"], g["year"] = st, yr
        dist.append(g.reset_index().rename(columns={"rec_rate": "recording_rate_bin"}))
    dist = pd.concat(dist)
    dist["recording_rate_bin"] = dist.recording_rate_bin.astype(str)
    dist.to_csv(OUT / "recording_rate_distribution.csv", index=False, float_format="%.1f")

    natpop = national_pops()
    gate("NCVS 2024 Hispanic 12+ equals the victim lane's 53,539,670",
         abs(natpop["ncvs2024_12"]["H"] - 53_539_670) < 1, f"{natpop['ncvs2024_12']['H']:,.0f}")
    pd.DataFrame(natpop).T.to_csv(OUT / "national_populations.csv", float_format="%.0f")

    allrows, vds = [], []
    for name, sp in specs():
        r, vd = results(stages, sp, natpop, name)
        allrows.append(r)
        vds.append(vd)
    R = pd.concat(allrows, ignore_index=True)
    R.to_csv(OUT / "rates_by_spec.csv", index=False, float_format="%.6f")
    VD = pd.concat(vds, ignore_index=True)
    VD.to_csv(OUT / "victim_ethnicity_of_hispanic_offenders_by_spec.csv", index=False, float_format="%.3f")
    cen = R[R.spec.eq("central")].set_index("offence")
    say("\n-- Central: TX+AZ 2022-2023, individuals 12+, agencies recording ethnicity >= 50%, allocation a --")
    say(cen[["victimisations", "rate_H", "rate_NHW", "rate_NHB", "rate_all", "RR_H_NHW", "RR_H_all", "RR_NHB_NHW",
             "local_share_H", "local_pop_share_H", "national_share_H", "share_noinfo", "share_eth_unknown"]]
        .to_string(float_format=lambda x: f"{x:,.3f}" if abs(x) < 100 else f"{x:,.0f}"))
    say("\n-- Hispanic/NH-white rate ratio and national Hispanic share, every specification --")
    piv = R.pivot_table(index="spec", columns="offence", values="RR_H_NHW", sort=False)[OFFENCES]
    say(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    piv2 = R.pivot_table(index="spec", columns="offence", values="national_share_H", sort=False)[OFFENCES]
    say(piv2.to_string(float_format=lambda x: f"{x:.3f}"))

    # unknown shares by offence, all agencies vs central agencies
    unk = []
    for lab, sp in [("all agencies", {**CENTRAL, "thresh": 0.0}), ("central agencies", CENTRAL),
                    ("all agencies, CA", {**CENTRAL, "thresh": 0.0, "states": ("CA",)})]:
        cells, _, _ = spec_cells(stages, sp)
        for (st,), g in cells.groupby(level=["state"]):
            t = g.groupby(level="offence").sum()
            for o in t.index:
                x = t.loc[o]
                unk.append(dict(agencies=lab, state=st, offence=o, victimisations=float(x.sum()),
                                offender_unknown=float(x["NOINFO"] / x.sum()),
                                ethnicity_unknown=float(x[["UW", "UB", "UO", "UU"]].sum() / x.sum()),
                                ethnicity_unknown_race_white=float(x["UW"] / x.sum()),
                                nh_race_unknown=float(x["NHU"] / x.sum()),
                                recorded=float(x[H_CLASSES + ["NHW", "NHB", "NHO", "NHU"]].sum() / x.sum())))
    unk = pd.DataFrame(unk)
    unk.to_csv(OUT / "unknown_offender_shares.csv", index=False, float_format="%.4f")
    say("\n-- Unknown offender and unknown ethnicity shares of victimisations --")
    say(unk.to_string(index=False, float_format=lambda x: f"{x:.3f}" if x < 10 else f"{x:,.0f}"))

    # victims of Hispanic offenders
    vd = VD[VD.spec.eq("central")].set_index("offence")[VCLASSES]
    vk = vd.drop(columns="vU")
    vtab = pd.DataFrame({"victims_H_offenders": vd.sum(axis=1), "victim_ethnicity_unknown": vd.vU / vd.sum(axis=1),
                         "victim_hispanic": vk.vH / vk.sum(axis=1),
                         "victim_non_hispanic": 1 - vk.vH / vk.sum(axis=1),
                         "victim_nh_white": vk.vNHW / vk.sum(axis=1), "victim_nh_black": vk.vNHB / vk.sum(axis=1)})
    say("\n-- Victims of Hispanic offenders (central, TX+AZ) --")
    say(vtab.to_string(float_format=lambda x: f"{x:.3f}" if x < 10 else f"{x:,.0f}"))
    vtab.to_csv(OUT / "victims_of_hispanic_offenders_central.csv", float_format="%.4f")

    ex = exposure_transfer(VD, cen, stages)
    ex.to_csv(OUT / "victim_exposure_transfer.csv", index=False, float_format="%.4f")
    say("\n-- Victim ethnicity: TX/AZ observed -> national via tract exposure (NCVS national: H offenders 0.404, NH 0.140) --")
    say(ex.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    vc_specs = [(n, sp) for n, sp in specs() if n in {
        "central", "alloc=b", "alloc=c", "alloc=a0", "agencies: ethnicity recorded >= 0%",
        "agencies: ethnicity recorded >= 80%", "agencies: ethnicity recorded >= 95%", "states=TX", "states=AZ",
        "states=CA", "states=TX+AZ+CA", "year=2022", "year=2023", "attribution=first", "attribution=anyH",
        "attribution=allH", "victims: all ages", "states=TX+AZ+CA, alloc=b", "states=TX+AZ+CA, alloc=c",
        "incidents with an arrest only"}]
    ogv = offender_given_victim(stages, vc_specs)
    ogv.to_csv(OUT / "offender_given_victim_transfer.csv", index=False, float_format="%.4f")
    say("\n-- P(offender Hispanic | victim group): NIBRS local -> national (central spec rows) --")
    say(ogv[ogv.spec.eq("central")].drop(columns="spec").to_string(index=False, float_format=lambda x: f"{x:.3f}" if abs(x) < 100 else f"{x:,.0f}"))

    arr = arrestee_results(stages, CENTRAL, natpop)
    arr.to_csv(OUT / "arrestee_rates.csv", index=False, float_format="%.4f")
    t43 = pd.read_csv(ARR / "arrests_by_ethnicity_2023.csv", dtype=str)      # sections repeat their header
    t43 = t43[t43.block.eq("arrests_43C_adult18") & t43.year.eq("2023")].set_index("offence").hispanic_share_of_eth_panel
    gate("FBI 2023 Table 43C shares held by the arrests lane (aggravated assault 26.6%, murder 21.7%)",
         abs(float(t43["assault"]) - 0.2662) < 1e-4 and abs(float(t43["murder"]) - 0.2169) < 1e-4,
         f"assault {t43['assault']}, murder {t43['murder']}, simple assault {t43['simple_assault']}")
    fbi = {"Murder": "murder", "Rape/sexual assault": "sexual", "Robbery": "robbery", "Aggravated assault": "assault",
           "Simple assault": "simple_assault"}
    chk = arr[arr.arrestees.eq("adults 18+") & arr.alloc.eq("a")].set_index("offence")
    chk = chk.assign(fbi_2023_table43c_share=[float(t43[fbi[o]]) for o in chk.index])
    chk["predicted_minus_fbi"] = chk.national_share_H - chk.fbi_2023_table43c_share
    say("\n-- Translation check: NIBRS TX/AZ adult arrestees carried to the nation vs FBI 2023 Table 43C --")
    say(chk[["arrestees_n", "eth_unknown_share", "RR_H_NHW", "local_share_H", "national_share_H",
             "fbi_2023_table43c_share", "predicted_minus_fbi"]].to_string(float_format=lambda x: f"{x:.3f}" if abs(x) < 100 else f"{x:,.0f}"))
    chk.to_csv(OUT / "translation_check_arrests_vs_table43c.csv", float_format="%.4f")
    comp = arr[arr.arrestees.eq("all ages") & arr.alloc.eq("a")].set_index("offence")[["RR_H_NHW", "local_share_H"]]
    comp.columns = ["arrestee_RR_H_NHW", "arrestee_local_share_H"]
    comp = comp.join(cen[["RR_H_NHW", "local_share_H"]].rename(columns={"RR_H_NHW": "offender_RR_H_NHW",
                                                                          "local_share_H": "offender_local_share_H"}))
    say("\n-- Incident offenders vs arrestees, same agencies (central) --")
    say(comp.to_string(float_format=lambda x: f"{x:.3f}"))
    comp.to_csv(OUT / "offenders_vs_arrestees.csv", float_format="%.4f")

    shr = shr_state_check(stages)
    shr.to_csv(OUT / "homicide_check_nibrs_vs_shr.csv", index=False, float_format="%.4f")
    say("\n-- Homicide check, TX and AZ 2022-2023: NIBRS vs SHR --")
    say(shr.to_string(index=False, float_format=lambda x: f"{x:.3f}" if x < 10 else f"{x:,.0f}"))
    (OUT / "rates_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

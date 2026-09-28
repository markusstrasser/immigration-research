"""Culpability of Hispanic drivers in California's crash records by quasi-induced exposure.

CHP California Crash Reporting System (CCRS), crashes of 2022-2024, from data.ca.gov through
acquire_ccrs_modal.py into _cache/ccrs/. In two-vehicle crashes with exactly one at-fault driver
the not-at-fault drivers stand in for exposure. For group g against reference set R:

    QIE odds ratio   (at-fault g / not-at-fault g) / (at-fault R / not-at-fault R),
                     crude and Mantel-Haenszel within county x year
    mixed-pair ratio (g at fault against an R driver) / (R at fault against a g driver)

Race is the officer-recorded party race (A/B/H/O/W, blank = not stated). "At fault" is the
officer's primary-collision-factor party. Confidence intervals come from a stratified
multinomial bootstrap over crashes (each crash is one draw of an at-fault x not-at-fault pair).

Outputs in derived/ (see RESULT.md for the reading of each file).
"""
import csv
import importlib.util
import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
SRC = LANE / "_cache" / "ccrs"
OUT = LANE / "derived"
CRASH_LANE = ROOT / "infra/immigration-fiscal/road_crash_externality_2026_09_28"
YEARS = (2022, 2023, 2024)
RACES = ["H", "W", "B", "A", "O", "U"]  # U = not stated
RI = {r: i for i, r in enumerate(RACES)}
NH = ["W", "B", "A", "O"]
SEV_ORDER = ["fatal", "severe", "other_visible", "complaint_of_pain", "injury_unclassified", "pdo"]
INJ = ["severe", "other_visible", "complaint_of_pain", "injury_unclassified"]
KNOWN_INJ_CODES = {"Fatal": 4, "SuspectSerious": 3, "SevereInactive": 3, "SuspectMinor": 2,
                   "OtherVisibleInactive": 2, "PossibleInjury": 1, "ComplaintOfPainInactive": 1}
N_BOOT = 400
rng = np.random.default_rng(20260928)


def write_csv(name, rows):
    OUT.mkdir(exist_ok=True)
    rows = list(rows)
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})


# --------------------------------------------------------------------------- load
con = duckdb.connect()


def load(kind, cols):
    sel = " UNION ALL ".join(
        f"SELECT {y} AS yr, {cols} FROM read_csv('{SRC}/{kind}_{y}.csv.gz', all_varchar=true, "
        f"header=true, normalize_names=true)" for y in YEARS)
    con.execute(f"CREATE TABLE {kind} AS {sel}")


load("crashes", "collision_id, report_number, report_version, ncic_code, county_code, numberkilled, "
     "numberinjured, hitrun, special_condition, collision_type_code, primarycollisionfactoriscited, isdeleted")
load("parties", "collisionid, partynumber, partytype, isatfault, isondutyemergencyvehicle, ishitandrun, "
     "sobrietydrugphysicalcode1, sobrietydrugphysicalcode2, gendercode, statedage, driverlicenseclass, "
     "driverlicensestatecode, racecode, vehicle1typeid")
load("injuredwitnesspassengers", "collisionid, partynumber, extentofinjurycode, injuredpersontype")

codes = con.execute("SELECT DISTINCT extentofinjurycode FROM injuredwitnesspassengers "
                    "WHERE extentofinjurycode IS NOT NULL").fetchall()
unknown_codes = {c[0] for c in codes} - set(KNOWN_INJ_CODES)
print("injury codes not mapped:", unknown_codes)
assert not unknown_codes, unknown_codes

inj_case = " ".join(f"WHEN '{k}' THEN {v}" for k, v in KNOWN_INJ_CODES.items())
con.execute(f"""
CREATE TABLE cr AS
WITH dedup AS (
  SELECT *, row_number() OVER (PARTITION BY yr, ncic_code, report_number
      ORDER BY TRY_CAST(report_version AS INT) DESC, TRY_CAST(collision_id AS BIGINT) DESC) AS rn
  FROM crashes WHERE coalesce(isdeleted, 'False') <> 'True'),
inj AS (
  SELECT yr, collisionid, max(CASE extentofinjurycode {inj_case} ELSE 0 END) AS maxinj,
         max(CASE WHEN extentofinjurycode = 'Fatal' AND injuredpersontype = 'Driver' THEN 1 ELSE 0 END) AS any_driver_killed
  FROM injuredwitnesspassengers GROUP BY 1, 2)
SELECT d.yr, d.collision_id, d.ncic_code, TRY_CAST(d.county_code AS INT) AS county,
       coalesce(TRY_CAST(d.numberkilled AS INT), 0) AS killed, coalesce(TRY_CAST(d.numberinjured AS INT), 0) AS injured,
       coalesce(d.hitrun IN ('F', 'M'), false) AS crash_hr,
       coalesce(d.special_condition, '') LIKE '%Private Property%' AS private_prop,
       d.collision_type_code AS ctype, coalesce(d.primarycollisionfactoriscited = 'True', false) AS pcf_cited,
       coalesce(d.ncic_code LIKE '9%', false) AS chp,
       CASE WHEN coalesce(TRY_CAST(d.numberkilled AS INT), 0) > 0 OR i.maxinj = 4 THEN 'fatal'
            WHEN i.maxinj = 3 THEN 'severe' WHEN i.maxinj = 2 THEN 'other_visible'
            WHEN i.maxinj = 1 THEN 'complaint_of_pain'
            WHEN coalesce(TRY_CAST(d.numberinjured AS INT), 0) > 0 THEN 'injury_unclassified'
            ELSE 'pdo' END AS sev
FROM dedup d LEFT JOIN inj i ON i.yr = d.yr AND i.collisionid = d.collision_id
WHERE d.rn = 1
""")
con.execute("""
CREATE TABLE pa AS
SELECT p.yr, p.collisionid, TRY_CAST(p.partynumber AS INT) AS pno, p.partytype,
       coalesce(p.isatfault = 'True', false) AS at_fault, coalesce(p.isondutyemergencyvehicle = 'True', false) AS emerg,
       coalesce(p.ishitandrun = 'True', false) AS party_hr,
       CASE WHEN p.racecode IN ('H', 'W', 'B', 'A', 'O') THEN p.racecode ELSE 'U' END AS race,
       coalesce(p.sobrietydrugphysicalcode1 IN ('B', 'C', 'D'), false)
         OR coalesce(p.sobrietydrugphysicalcode2 IN ('B', 'C', 'D'), false) AS hbd,
       coalesce(p.sobrietydrugphysicalcode1 = 'B', false) OR coalesce(p.sobrietydrugphysicalcode2 = 'B', false) AS hbd_under_influence,
       coalesce(p.sobrietydrugphysicalcode1 = 'E', false) OR coalesce(p.sobrietydrugphysicalcode2 = 'E', false) AS drug,
       coalesce(p.sobrietydrugphysicalcode1 IN ('A', 'B', 'C', 'D', 'E', 'F', 'I'), false) AS sobriety_stated,
       p.gendercode AS sex, TRY_CAST(p.statedage AS INT) AS age,
       coalesce(p.driverlicenseclass, '') AS lic_class, coalesce(p.driverlicensestatecode, '') AS lic_state
FROM parties p
""")

flow = []


def count(label, sql):
    n = con.execute(sql).fetchone()[0]
    flow.append({"step": label, "crashes": int(n)})
    print(f"  ▸ {label}: {n:,}")


count("crash rows, 2022-2024", "SELECT count(*) FROM crashes")
count("after dropping deleted and duplicate report versions", "SELECT count(*) FROM cr")

# one row per crash with party composition
con.execute("""
CREATE TABLE kc AS
SELECT c.*, count(p.collisionid) AS np,
       sum(CASE WHEN p.partytype = 'Driver' THEN 1 ELSE 0 END) AS nd,
       sum(CASE WHEN p.at_fault THEN 1 ELSE 0 END) AS naf,
       coalesce(bool_or(p.party_hr), false) AS party_hr, coalesce(bool_or(p.emerg), false) AS emerg
FROM cr c LEFT JOIN pa p ON p.yr = c.yr AND p.collisionid = c.collision_id
GROUP BY ALL
""")
count("exactly two parties, both drivers", "SELECT count(*) FROM kc WHERE np = 2 AND nd = 2")
count("... exactly one at fault", "SELECT count(*) FROM kc WHERE np = 2 AND nd = 2 AND naf = 1")
count("... no on-duty emergency vehicle", "SELECT count(*) FROM kc WHERE np = 2 AND nd = 2 AND naf = 1 AND NOT emerg")
count("... not on private property", "SELECT count(*) FROM kc WHERE np = 2 AND nd = 2 AND naf = 1 AND NOT emerg AND NOT private_prop")
count("... no hit-and-run flag", "SELECT count(*) FROM kc WHERE np = 2 AND nd = 2 AND naf = 1 AND NOT emerg AND NOT private_prop AND NOT crash_hr AND NOT party_hr")

pairs = con.execute("""
SELECT k.yr, k.collision_id, k.county, k.sev, k.ctype, k.chp, k.pcf_cited, k.private_prop,
       (k.crash_hr OR k.party_hr) AS hr, k.emerg,
       a.race AS af_race, n.race AS nf_race, a.party_hr AS af_fled,
       a.hbd AS af_hbd, n.hbd AS nf_hbd, a.hbd_under_influence AS af_hbd_ui, n.hbd_under_influence AS nf_hbd_ui,
       a.drug AS af_drug, n.drug AS nf_drug, a.sobriety_stated AS af_sob_known, n.sobriety_stated AS nf_sob_known,
       a.sex AS af_sex, n.sex AS nf_sex, a.age AS af_age, n.age AS nf_age,
       a.lic_class AS af_lic, n.lic_class AS nf_lic, a.lic_state AS af_lic_state, n.lic_state AS nf_lic_state,
       coalesce(ka.killed_driver, 0) AS af_killed, coalesce(kn.killed_driver, 0) AS nf_killed
FROM kc k
JOIN pa a ON a.yr = k.yr AND a.collisionid = k.collision_id AND a.at_fault
JOIN pa n ON n.yr = k.yr AND n.collisionid = k.collision_id AND NOT n.at_fault
LEFT JOIN (SELECT yr, collisionid, TRY_CAST(partynumber AS INT) AS pno, 1 AS killed_driver
           FROM injuredwitnesspassengers WHERE extentofinjurycode = 'Fatal' AND injuredpersontype = 'Driver'
           GROUP BY ALL) ka ON ka.yr = k.yr AND ka.collisionid = k.collision_id AND ka.pno = a.pno
LEFT JOIN (SELECT yr, collisionid, TRY_CAST(partynumber AS INT) AS pno, 1 AS killed_driver
           FROM injuredwitnesspassengers WHERE extentofinjurycode = 'Fatal' AND injuredpersontype = 'Driver'
           GROUP BY ALL) kn ON kn.yr = k.yr AND kn.collisionid = k.collision_id AND kn.pno = n.pno
WHERE k.np = 2 AND k.nd = 2 AND k.naf = 1 AND NOT k.emerg
""").fetchdf()
pairs["stratum"] = pairs["county"].fillna(-1).astype(int).astype(str) + "_" + pairs["yr"].astype(str)
primary_mask = ~pairs["private_prop"] & ~pairs["hr"]
both_known = (pairs["af_race"] != "U") & (pairs["nf_race"] != "U")
flow.append({"step": "... both drivers' race recorded (primary sample)",
             "crashes": int((primary_mask & both_known).sum())})
print(f"  ▸ primary sample: {(primary_mask & both_known).sum():,}")
write_csv("sample_flow.csv", flow)


# --------------------------------------------------------------------------- estimators
def cube_of(df):
    """(strata, 6, 6) counts: at-fault race x not-at-fault race."""
    strata = sorted(df["stratum"].unique())
    si = {s: i for i, s in enumerate(strata)}
    cube = np.zeros((len(strata), 6, 6))
    g = df.groupby(["stratum", "af_race", "nf_race"]).size()
    for (s, a, n), v in g.items():
        cube[si[s], RI[a], RI[n]] += v
    return cube


def estimates(cube, g, ref):
    gi, ri = RI[g], [RI[r] for r in ref]
    A_g = cube[:, gi, :].sum(axis=1)
    N_g = cube[:, :, gi].sum(axis=1)
    A_r = cube[:, ri, :].sum(axis=(1, 2))
    N_r = cube[:, :, ri].sum(axis=(1, 2))
    crude = (A_g.sum() / N_g.sum()) / (A_r.sum() / N_r.sum())
    n = A_g + N_g + A_r + N_r
    ok = n > 0
    mh = (A_g * N_r / np.where(ok, n, 1))[ok].sum() / (N_g * A_r / np.where(ok, n, 1))[ok].sum()
    n_gr = cube[:, gi, :][:, ri].sum()
    n_rg = cube[:, ri, gi].sum()
    return {"qie_crude": crude, "qie_mh": mh, "mixed_pair": n_gr / n_rg,
            "A_g": A_g.sum(), "N_g": N_g.sum(), "A_r": A_r.sum(), "N_r": N_r.sum(), "n_gr": n_gr, "n_rg": n_rg}


def boot(cube, g, ref, n_boot=N_BOOT):
    ns = cube.reshape(len(cube), -1).sum(axis=1).astype(np.int64)
    p = cube.reshape(len(cube), -1) / np.maximum(ns, 1)[:, None]
    out = {"qie_crude": [], "qie_mh": [], "mixed_pair": []}
    for _ in range(n_boot):
        c = rng.multinomial(ns, p).reshape(cube.shape).astype(float)
        e = estimates(c, g, ref)
        for k in out:
            out[k].append(e[k])
    return {k: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for k, v in out.items()}


def sev_mask(df, sev):
    if sev == "injury_all":
        return df["sev"].isin(INJ)
    if sev == "nonfatal_all":
        return df["sev"] != "fatal"
    return df["sev"] == sev


SEV_ROWS = ["fatal", "severe", "other_visible", "complaint_of_pain", "injury_all", "pdo", "nonfatal_all"]
COMPARISONS = {"vs_nh_white": ["W"], "vs_all_non_hispanic": NH}
prim = pairs[primary_mask & both_known]
rows = []
cubes = {}
for sev in SEV_ROWS:
    sub = prim[sev_mask(prim, sev)]
    cube = cube_of(sub)
    cubes[sev] = cube
    for cname, ref in COMPARISONS.items():
        e = estimates(cube, "H", ref)
        ci = boot(cube, "H", ref, n_boot=N_BOOT if sev in ("injury_all", "pdo", "fatal", "nonfatal_all") else 200)
        rows.append({"severity": sev, "comparison": cname, "crashes": int(cube.sum()),
                     "at_fault_hispanic": int(e["A_g"]), "not_at_fault_hispanic": int(e["N_g"]),
                     "at_fault_ref": int(e["A_r"]), "not_at_fault_ref": int(e["N_r"]),
                     "hispanic_at_fault_vs_ref": int(e["n_gr"]), "ref_at_fault_vs_hispanic": int(e["n_rg"]),
                     "or_qie_crude": e["qie_crude"], "or_qie_crude_lo": ci["qie_crude"][0], "or_qie_crude_hi": ci["qie_crude"][1],
                     "or_qie_mh_county_year": e["qie_mh"], "or_qie_mh_lo": ci["qie_mh"][0], "or_qie_mh_hi": ci["qie_mh"][1],
                     "or_mixed_pair": e["mixed_pair"], "or_mixed_pair_lo": ci["mixed_pair"][0], "or_mixed_pair_hi": ci["mixed_pair"][1],
                     "m_qie_mh": (1 + e["qie_mh"]) / 2, "m_mixed_pair": (1 + e["mixed_pair"]) / 2})
write_csv("qie_or_table.csv", rows)
ORT = pd.DataFrame(rows)
print(ORT[["severity", "comparison", "crashes", "or_qie_crude", "or_qie_mh_county_year", "or_mixed_pair"]].to_string(index=False))

# pair backbone: at-fault race x not-at-fault race by severity (primary sample, both races known)
pb = prim.groupby(["sev", "af_race", "nf_race"]).size().reset_index(name="crashes")
write_csv("pair_counts.csv", pb.to_dict(orient="records"))

# by year, and other groups against white, for stability and context
by_year, other = [], []
for y in YEARS:
    for sev in ("fatal", "injury_all", "pdo"):
        sub = prim[(prim["yr"] == y) & sev_mask(prim, sev)]
        c = cube_of(sub)
        for cname, ref in COMPARISONS.items():
            e = estimates(c, "H", ref)
            by_year.append({"year": y, "severity": sev, "comparison": cname, "crashes": int(c.sum()),
                            "or_qie_crude": e["qie_crude"], "or_qie_mh_county_year": e["qie_mh"],
                            "or_mixed_pair": e["mixed_pair"]})
write_csv("qie_or_by_year.csv", by_year)
for sev in ("fatal", "injury_all", "pdo"):
    for g in ("H", "B", "A", "O"):
        e = estimates(cubes[sev], g, ["W"])
        other.append({"severity": sev, "group": g, "reference": "W", "or_qie_crude": e["qie_crude"],
                      "or_qie_mh_county_year": e["qie_mh"], "or_mixed_pair": e["mixed_pair"],
                      "at_fault": int(e["A_g"]), "not_at_fault": int(e["N_g"])})
write_csv("qie_or_other_groups_vs_white.csv", other)

# --------------------------------------------------------------------------- sensitivity
sens = []


def add_sens(label, df, sev_list=("injury_all", "pdo", "fatal")):
    for sev in sev_list:
        sub = df[sev_mask(df, sev)]
        if len(sub) == 0:
            continue
        c = cube_of(sub)
        for cname, ref in COMPARISONS.items():
            e = estimates(c, "H", ref)
            sens.append({"variant": label, "severity": sev, "comparison": cname, "crashes": int(c.sum()),
                         "or_qie_crude": e["qie_crude"], "or_qie_mh_county_year": e["qie_mh"],
                         "or_mixed_pair": e["mixed_pair"]})


add_sens("primary", prim)
add_sens("with private-property crashes", pairs[~pairs["hr"] & both_known])
add_sens("CHP reports only", prim[prim["chp"]])
add_sens("local-agency reports only", prim[~prim["chp"]])
for ct, name in (("C", "rear-end"), ("D", "broadside"), ("B", "sideswipe"), ("A", "head-on")):
    add_sens(f"collision type {name}", prim[prim["ctype"] == ct])
add_sens("at-fault party cited", prim[prim["pcf_cited"]])
add_sens("at-fault party not cited", prim[~prim["pcf_cited"].astype(bool)])
add_sens("neither driver had been drinking or drugged",
         prim[~prim["af_hbd"].astype(bool) & ~prim["nf_hbd"].astype(bool) & ~prim["af_drug"].astype(bool) & ~prim["nf_drug"].astype(bool)])
write_csv("qie_or_sensitivity.csv", sens)

# age-sex adjusted: each driver in the stratum of their own age band and sex
drivers = pd.concat([
    prim.assign(role="at_fault", race=prim["af_race"], age=prim["af_age"], sex=prim["af_sex"]),
    prim.assign(role="not_at_fault", race=prim["nf_race"], age=prim["nf_age"], sex=prim["nf_sex"])])[
    ["sev", "role", "race", "age", "sex", "county", "yr"]]
bands = [(14, 20), (21, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 120)]
drivers["band"] = None
for lo, hi in bands:
    drivers.loc[drivers["age"].between(lo, hi), "band"] = f"{lo}-{hi}"
adj = []
for sev in ("fatal", "injury_all", "pdo"):
    d = drivers[sev_mask(drivers, sev) & drivers["band"].notna() & drivers["sex"].isin(["M", "F"])]
    for cname, ref in COMPARISONS.items():
        num = den = 0.0
        tot = {"A_g": 0, "N_g": 0, "A_r": 0, "N_r": 0}
        for _, s in d.groupby(["band", "sex"]):
            a = ((s["race"] == "H") & (s["role"] == "at_fault")).sum()
            b = ((s["race"] == "H") & (s["role"] == "not_at_fault")).sum()
            c = ((s["race"].isin(ref)) & (s["role"] == "at_fault")).sum()
            dd = ((s["race"].isin(ref)) & (s["role"] == "not_at_fault")).sum()
            n = a + b + c + dd
            if n:
                num += a * dd / n
                den += b * c / n
            tot["A_g"] += a; tot["N_g"] += b; tot["A_r"] += c; tot["N_r"] += dd
        crude_known_age = (tot["A_g"] / tot["N_g"]) / (tot["A_r"] / tot["N_r"])
        adj.append({"severity": sev, "comparison": cname, "drivers_with_age_sex": int(sum(tot.values())),
                    "or_crude_same_drivers": crude_known_age, "or_mh_age_band_sex": num / den})
write_csv("qie_or_age_sex_adjusted.csv", adj)

# --------------------------------------------------------------------------- hit-and-run bounds
hr_rows = []
hr_parts = {}  # severity -> (base, identified fled, P(at-fault race | victim race, stratum), unidentified)
hr_pairs = pairs[~pairs["private_prop"] & pairs["hr"] & (pairs["nf_race"] != "U")]
for sev in ("injury_all", "pdo", "nonfatal_all", "fatal"):
    base = cube_of(prim[sev_mask(prim, sev)])
    strata = sorted(prim[sev_mask(prim, sev)]["stratum"].unique())
    si = {s: i for i, s in enumerate(strata)}
    hp = hr_pairs[sev_mask(hr_pairs, sev)]
    known = hp[hp["af_race"] != "U"]
    unk = hp[hp["af_race"] == "U"]
    add_known = np.zeros_like(base)
    add_unk = np.zeros((len(strata), 6))  # stratum x not-at-fault race, fled driver race unknown
    for (s, a, n), v in known.groupby(["stratum", "af_race", "nf_race"]).size().items():
        if s in si:
            add_known[si[s], RI[a], RI[n]] += v
    dropped = 0
    for (s, n), v in unk.groupby(["stratum", "nf_race"]).size().items():
        if s in si:
            add_unk[si[s], RI[n]] += v
        else:
            dropped += v
    # conditional at-fault race given victim race and stratum, from non-hit-and-run crashes
    cond = base / np.maximum(base.sum(axis=1, keepdims=True), 1)
    state_cond = base.sum(axis=0) / np.maximum(base.sum(axis=0).sum(axis=0, keepdims=True), 1)
    empty = base.sum(axis=1) == 0
    for s_i in range(len(strata)):
        for n_i in range(6):
            if empty[s_i, n_i]:
                cond[s_i, :, n_i] = state_cond[:, n_i]
    imputed = cond * add_unk[:, None, :]
    hr_parts[sev] = (base, add_known, cond, add_unk)
    all_h = np.zeros_like(base)
    all_h[:, RI["H"], :] = add_unk
    for cname, ref in COMPARISONS.items():
        none_h = np.zeros_like(base)
        if cname == "vs_nh_white":
            none_h[:, RI["W"], :] = add_unk
        else:  # spread over non-Hispanic groups by their at-fault mix among fled-victim strata
            mix = base[:, [RI[r] for r in NH], :].sum(axis=(0, 2))
            mix = mix / mix.sum()
            for j, r in enumerate(NH):
                none_h[:, RI[r], :] = add_unk * mix[j]
        for label, cube in (("exclude hit-and-run crashes (primary)", base),
                            ("add identified fled drivers only", base + add_known),
                            ("impute fled drivers from victim race and county", base + add_known + imputed),
                            ("all unidentified fled drivers Hispanic", base + add_known + all_h),
                            ("no unidentified fled driver Hispanic", base + add_known + none_h)):
            e = estimates(cube, "H", ref)
            hr_rows.append({"severity": sev, "comparison": cname, "scenario": label,
                            "crashes": round(float(cube.sum()), 1), "or_qie_crude": e["qie_crude"],
                            "or_qie_mh_county_year": e["qie_mh"], "or_mixed_pair": e["mixed_pair"],
                            "unidentified_fled": int(add_unk.sum()), "identified_fled": int(add_known.sum()),
                            "unidentified_outside_strata": int(dropped)})
write_csv("hit_and_run_bounds.csv", hr_rows)


def mnar_cube(sev, k):
    """Unidentified fled drivers imputed from victim race and stratum, with the Hispanic odds
    multiplied by k (k = 1 is the missing-at-random imputation)."""
    base, add_known, cond, add_unk = hr_parts[sev]
    h = cond[:, RI["H"], :]
    c = cond / (k * h + (1 - h))[:, None, :]
    c[:, RI["H"], :] *= k
    share_h = float((c[:, RI["H"], :] * add_unk).sum() / add_unk.sum())
    return base + add_known + c * add_unk[:, None, :], share_h


mnar_rows = []
for k in (1.0, 1.5, 2.0, 3.0, 5.0, 10.0):
    row = {"hispanic_odds_multiplier_k": k}
    for sev in ("injury_all", "pdo", "fatal"):
        cube, share_h = mnar_cube(sev, k)
        e = estimates(cube, "H", NH)
        row[f"{sev}_fled_hispanic_share"] = share_h
        row[f"{sev}_or_qie_mh_vs_all_nh"] = e["qie_mh"]
    mnar_rows.append(row)
write_csv("hit_and_run_mnar_sensitivity.csv", mnar_rows)

# --------------------------------------------------------------------------- driver traits
traits = []
two = pairs[~pairs["private_prop"]]  # all clean two-driver crashes incl. hit-and-run
for sev in ("fatal", "injury_all", "pdo"):
    t = two[sev_mask(two, sev)]
    for role, pre in (("at_fault", "af_"), ("not_at_fault", "nf_")):
        for race in RACES + ["NH"]:  # NH = all non-Hispanic with race recorded
            d = t[t[pre + "race"].isin(NH)] if race == "NH" else t[t[pre + "race"] == race]
            if len(d) == 0:
                continue
            sob = d[d[pre + "sob_known"].astype(bool)]
            age = d[pre + "age"]
            traits.append({
                "severity": sev, "role": role, "race": race, "drivers": int(len(d)),
                "share_had_been_drinking": float(d[pre + "hbd"].astype(bool).mean()),
                "share_had_been_drinking_of_sobriety_stated": float(sob[pre + "hbd"].astype(bool).mean()) if len(sob) else None,
                "share_hbd_under_influence": float(d[pre + "hbd_ui"].astype(bool).mean()),
                "share_drug": float(d[pre + "drug"].astype(bool).mean()),
                "share_fled_hit_and_run": float(d["af_fled"].astype(bool).mean()) if role == "at_fault" else None,
                "share_crash_hit_and_run": float(d["hr"].astype(bool).mean()),
                "share_licence_class_U": float((d[pre + "lic"] == "U").mean()),
                "share_licence_class_blank": float((d[pre + "lic"] == "").mean()),
                "share_licence_state_MX": float((d[pre + "lic_state"] == "MX").mean()),
                "share_licence_state_CA": float((d[pre + "lic_state"] == "CA").mean()),
                "share_age_14_24": float(age.between(14, 24).sum() / max(age.between(14, 120).sum(), 1)),
                "share_age_stated": float(age.between(14, 120).mean()),
                "share_male": float((d[pre + "sex"] == "M").mean()),
                "share_killed": float(d[pre + "killed"].astype(bool).mean()),
            })
write_csv("driver_traits_by_race.csv", traits)

# licence-state codes by race among all drivers of all crashes (to check the MX code spelling)
lic = con.execute("""SELECT race, lic_state, count(*) AS drivers FROM pa WHERE partytype = 'Driver'
                     GROUP BY 1, 2 QUALIFY row_number() OVER (PARTITION BY race ORDER BY count(*) DESC) <= 6
                     ORDER BY 1, 3 DESC""").fetchdf()
write_csv("licence_state_top_codes_by_race.csv", lic.to_dict(orient="records"))

# hit-and-run by race among all at-fault drivers (any crash type, not only two-vehicle)
hr_all = con.execute("""
SELECT p.race, count(*) AS at_fault_drivers, sum(CASE WHEN p.party_hr THEN 1 ELSE 0 END) AS flagged_fled,
       sum(CASE WHEN c.crash_hr THEN 1 ELSE 0 END) AS in_hit_and_run_crash
FROM pa p JOIN cr c ON c.yr = p.yr AND c.collision_id = p.collisionid
WHERE p.partytype = 'Driver' AND p.at_fault AND NOT c.private_prop GROUP BY 1 ORDER BY 1""").fetchdf()
write_csv("at_fault_drivers_hit_and_run_by_race.csv", hr_all.to_dict(orient="records"))

# victims of hit-and-run: race mix of not-at-fault drivers in hit-and-run vs other two-driver crashes
vict = (two[two["nf_race"] != "U"].groupby(["hr", "nf_race"]).size().unstack(fill_value=0))
vict = vict.div(vict.sum(axis=1), axis=0)
write_csv("not_at_fault_race_mix_by_hit_and_run.csv",
          [{"hit_and_run_crash": bool(k), **{r: float(v[r]) for r in vict.columns}} for k, v in vict.iterrows()])

# --------------------------------------------------------------------------- killed-driver subset, coverage
kd = pairs[~pairs["private_prop"] & ~pairs["hr"] & (pairs["sev"] == "fatal")]
kd_rows = []
for cname, ref in COMPARISONS.items():
    a = ((kd["af_race"] == "H") & kd["af_killed"].astype(bool)).sum()
    b = ((kd["nf_race"] == "H") & kd["nf_killed"].astype(bool)).sum()
    c = ((kd["af_race"].isin(ref)) & kd["af_killed"].astype(bool)).sum()
    d = ((kd["nf_race"].isin(ref)) & kd["nf_killed"].astype(bool)).sum()
    kd_rows.append({"sample": "CCRS killed drivers, two-driver fatal crashes 2022-2024", "comparison": cname,
                    "at_fault_hispanic_killed": int(a), "not_at_fault_hispanic_killed": int(b),
                    "at_fault_ref_killed": int(c), "not_at_fault_ref_killed": int(d),
                    "or": float((a / b) / (c / d)) if b and c and d else None})

# FARS 2023, California only, same culpability rule as road_crash_externality_2026_09_28/fars_group.py
F = CRASH_LANE / "_cache" / "fars2023" / "FARS2023NationalCSV"
per = pd.read_csv(F / "person.csv", usecols=["STATE", "ST_CASE", "VEH_NO", "PER_TYP", "INJ_SEV", "HISPANIC"],
                  encoding="latin-1", low_memory=False)
veh = pd.read_csv(F / "vehicle.csv", usecols=["ST_CASE", "VEH_NO", "UNITTYPE"], encoding="latin-1", low_memory=False)
acc = pd.read_csv(F / "accident.csv", usecols=["ST_CASE", "STATE", "VE_FORMS", "FATALS"], encoding="latin-1", low_memory=False)
drf = pd.read_csv(F / "driverrf.csv", usecols=["ST_CASE", "VEH_NO", "DRIVERRF"], encoding="latin-1", low_memory=False)
vio = pd.read_csv(F / "violatn.csv", usecols=["ST_CASE", "VEH_NO", "VIOLATION"], encoding="latin-1", low_memory=False)
rf_nonbehav = {0, 99, 16, 24, 60, 73, 74, 89} | set(range(80, 90))
vio_nonmoving = {0, 7, 8} | (set(range(70, 100)) - {98})
culp = set(map(tuple, drf[~drf["DRIVERRF"].isin(rf_nonbehav)][["ST_CASE", "VEH_NO"]].values)) | \
    set(map(tuple, vio[~vio["VIOLATION"].isin(vio_nonmoving)][["ST_CASE", "VEH_NO"]].values))
va = veh[veh["UNITTYPE"] == 1].merge(acc[["ST_CASE", "VE_FORMS", "STATE"]], on="ST_CASE")
va["culp"] = [k in culp for k in zip(va["ST_CASE"], va["VEH_NO"])]
two_f = va[va["VE_FORMS"] == 2]
nc = two_f.groupby("ST_CASE")["culp"].agg(["sum", "size"])
clean = set(nc[(nc["size"] == 2) & (nc["sum"] == 1)].index)
kdr = per[(per["INJ_SEV"] == 4) & (per["PER_TYP"] == 1) & per["ST_CASE"].isin(clean)].merge(
    va[["ST_CASE", "VEH_NO", "culp", "STATE"]], on=["ST_CASE", "VEH_NO"], suffixes=("", "_v"))
kdr["hisp"] = kdr["HISPANIC"].between(1, 6)
kdr["nonhisp"] = kdr["HISPANIC"] == 7
for scope, d in (("FARS 2023 killed drivers, California", kdr[kdr["STATE"] == 6]),
                 ("FARS 2023 killed drivers, national", kdr)):
    a, b = int((d["hisp"] & d["culp"]).sum()), int((d["hisp"] & ~d["culp"]).sum())
    c, dd = int((d["nonhisp"] & d["culp"]).sum()), int((d["nonhisp"] & ~d["culp"]).sum())
    kd_rows.append({"sample": scope, "comparison": "vs_all_non_hispanic", "at_fault_hispanic_killed": a,
                    "not_at_fault_hispanic_killed": b, "at_fault_ref_killed": c, "not_at_fault_ref_killed": dd,
                    "or": (a / b) / (c / dd)})
write_csv("killed_driver_check.csv", kd_rows)

cov = con.execute("""SELECT yr, count(*) AS crashes, sum(CASE WHEN sev = 'fatal' THEN 1 ELSE 0 END) AS fatal_crashes,
       sum(killed) AS killed, sum(CASE WHEN sev IN ('severe','other_visible','complaint_of_pain','injury_unclassified') THEN 1 ELSE 0 END) AS injury_crashes,
       sum(injured) AS injured, sum(CASE WHEN sev = 'pdo' THEN 1 ELSE 0 END) AS pdo_crashes,
       sum(CASE WHEN chp THEN 1 ELSE 0 END) AS chp_crashes, sum(CASE WHEN private_prop THEN 1 ELSE 0 END) AS private_property
FROM cr GROUP BY 1 ORDER BY 1""").fetchdf()
fars_ca = acc[acc["STATE"] == 6]
cov_rows = cov.to_dict(orient="records")
cov_rows.append({"yr": "FARS 2023 CA", "crashes": None, "fatal_crashes": int(len(fars_ca)),
                 "killed": int(fars_ca["FATALS"].sum()), "injury_crashes": None, "injured": None,
                 "pdo_crashes": None, "chp_crashes": None, "private_property": None})
write_csv("coverage_by_year.csv", cov_rows)
sevmix = con.execute("SELECT yr, sev, count(*) AS crashes FROM cr GROUP BY 1, 2 ORDER BY 1, 2").fetchdf()
write_csv("crashes_by_severity.csv", sevmix.to_dict(orient="records"))
agency = con.execute("""SELECT ncic_code, count(*) AS crashes_2022_2024 FROM cr GROUP BY 1
                        ORDER BY 2 DESC LIMIT 25""").fetchdf()
write_csv("top_reporting_agencies.csv", agency.to_dict(orient="records"))

# ACS 2024 1-year, California (api.census.gov, saved in _cache/): Mexican share of Hispanics and the
# Hispanic share of car commuters, against the not-at-fault (exposure) shares of the primary sample
def acs(name):
    head, row = json.loads((LANE / "_cache" / name).read_text())
    return {h: row[i] for i, h in enumerate(head)}


b03, b08 = acs("acs1_2024_B03001_ca.json"), acs("acs1_2024_B08105_ca.json")
drivers_acs = lambda alone, pool: float(alone) + float(pool) / 2  # noqa: E731
acs_rows = [
    {"measure": "Mexican-origin share of Hispanic residents (B03001_004/_003)",
     "value": float(b03["B03001_004E"]) / float(b03["B03001_003E"])},
    {"measure": "Hispanic share of residents (B03001_003/_001)", "value": float(b03["B03001_003E"]) / float(b03["B03001_001E"])},
    {"measure": "Hispanic share of workers driving to work, alone + carpool/2 (B08105I/B08301)",
     "value": drivers_acs(b08["B08105I_002E"], b08["B08105I_003E"]) / drivers_acs(b08["B08301_003E"], b08["B08301_004E"])},
    {"measure": "white non-Hispanic share of workers driving to work, alone + carpool/2 (B08105H/B08301)",
     "value": drivers_acs(b08["B08105H_002E"], b08["B08105H_003E"]) / drivers_acs(b08["B08301_003E"], b08["B08301_004E"])},
]
for sev in ("injury_all", "pdo"):
    nf = prim[sev_mask(prim, sev)]["nf_race"].value_counts(normalize=True)
    acs_rows.append({"measure": f"Hispanic share of not-at-fault drivers, {sev} (primary sample)", "value": float(nf["H"])})
    acs_rows.append({"measure": f"white share of not-at-fault drivers, {sev} (primary sample)", "value": float(nf["W"])})
write_csv("acs_ca_checks.csv", acs_rows)

# race-missing pattern among drivers of clean two-driver crashes
miss = []
for sev in ("fatal", "injury_all", "pdo"):
    t = two[sev_mask(two, sev)]
    for hr in (False, True):
        u = t[t["hr"] == hr]
        miss.append({"severity": sev, "hit_and_run_crash": hr, "crashes": int(len(u)),
                     "at_fault_race_missing": float((u["af_race"] == "U").mean()) if len(u) else None,
                     "not_at_fault_race_missing": float((u["nf_race"] == "U").mean()) if len(u) else None})
write_csv("race_missing.csv", miss)
print("✓ CCRS tables written")


# --------------------------------------------------------------------------- apply to the crash lane
def load_crash_model():
    sys.dont_write_bytecode = True  # read the other lane; never write into its directory
    spec = importlib.util.spec_from_file_location("crash_model", CRASH_LANE / "crash_model.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # top level only reads inputs; main() is not called
    return mod


cm = load_crash_model()
keys = list(cm.FACTORS)
central_args = [cm.FACTORS[k][1] for k in keys]
cen = cm.evaluate(*central_args)


def pdo_share_of_mv_nonfatal():
    """PDO row's part of the lane's non-fatal multi-vehicle base, from the lane's own constants."""
    parts = {}
    for k in cm.SEV:
        if k == "Fatal":
            continue
        econ_keep = cm.ECON[k] - cm.CONG[k] - cm.EMS[k]
        comp = econ_keep + cm.QALY[k]
        price = (econ_keep * cm.CPI_2024 / cm.CPI_2019 + cm.QALY[k] * cm.VSL_2024 / cm.VSL_2019) / comp
        count = cm.PDO_CRASHES[2023] / cm.PDO_CRASHES[2019] if k == "PDO" else cm.INJURED[2023] / cm.INJURED[2019]
        keep_frac = comp / (cm.ECON[k] + cm.QALY[k])
        occ = comp - (cm.PED[k] + cm.BIKE[k]) * keep_frac
        mv = cm.MV_SHARE_PDO if k == "PDO" else cm.MV_SHARE_INJ
        parts[k] = occ * mv * price * count / 1000.0
    assert abs(sum(parts.values()) - cm.BASE["mv_nonfatal"]) < 1e-6
    return parts["PDO"] / sum(parts.values()), parts


def split_eval(args, r_mv_nf, r_nm_nf):
    """crash_model.evaluate with separate culpability odds ratios for the non-fatal
    multi-vehicle and non-fatal non-motorist parts; fatal and single-vehicle parts keep args' r_c."""
    vmt, r_c, q_mult, x_nf, x_f, beta, liab, e_sv = args
    base = cm.evaluate(*args)
    s, q, v = base["s"], base["q"], base["vmt_vs_avg"]
    h = cm.HISP_PED * cm.MEX_OF_HISP
    kappa, ins_g = liab
    b_nf, b_f = beta
    B = cm.BASE

    def liab_term(r):
        f = r / (1 + r)
        return kappa * ((1 - f) * cm.INS_OTHER - f * ins_g)

    m_f, m_mv, m_nm = (1 + r_c) / 2, (1 + r_mv_nf) / 2, (1 + r_nm_nf) / 2
    comp = {
        "mv_nonfatal": m_mv * s * (1 - q) * B["mv_nonfatal"] * (x_nf + liab_term(r_mv_nf)),
        "mv_fatal": m_f * s * (1 - q) * B["mv_fatal"] * (x_f + liab_term(r_c)),
        "nm_nonfatal": m_nm * s * (1 - q) / (1 - s) * (1 - h) * b_nf * B["nm_nonfatal"],
        "nm_fatal": m_f * s * (1 - q) / (1 - s) * (1 - h) * b_f * B["nm_fatal"],
        "single_vehicle": m_f * s * B["sv"] * e_sv,
    }
    m_of = {"mv_nonfatal": m_mv, "mv_fatal": m_f, "nm_nonfatal": m_nm, "nm_fatal": m_f, "single_vehicle": m_f}
    total = sum(comp.values())
    normalized = sum(e * (1 - 1 / (v * m_of[c])) for c, e in comp.items())
    fk = lambda r: r / (1 + r)  # noqa: E731
    fault_parts = {
        "mv_nonfatal": m_mv * s * (1 - q) * B["mv_nonfatal"] * fk(r_mv_nf) * (1 - kappa * ins_g),
        "mv_fatal": m_f * s * (1 - q) * B["mv_fatal"] * fk(r_c) * (1 - kappa * ins_g),
        "nm_nonfatal": m_nm * s * (1 - q) / (1 - s) * (1 - h) * B["nm_nonfatal"] * cm.F_DRIVER_PED
        * (r_nm_nf / m_nm) * (1 - kappa * ins_g),
        "nm_fatal": m_f * s * (1 - q) / (1 - s) * (1 - h) * B["nm_fatal"] * cm.F_DRIVER_PED
        * (r_c / m_f) * (1 - kappa * ins_g),
        "single_vehicle": comp["single_vehicle"],
    }
    r_of = {"mv_nonfatal": r_mv_nf, "mv_fatal": r_c, "nm_nonfatal": r_nm_nf, "nm_fatal": r_c, "single_vehicle": r_c}
    fault_total = sum(fault_parts.values())
    fault_norm = sum(e * (1 - 1 / (v * r_of[c])) for c, e in fault_parts.items())
    return {**comp, "nonmotorist": comp["nm_nonfatal"] + comp["nm_fatal"], "total": total,
            "normalized": normalized, "fault_total": fault_total, "fault_normalized": fault_norm,
            "m_mv_nonfatal": m_mv, "m_nm_nonfatal": m_nm, "m_fatal_sv": m_f}


# positive control: equal odds ratios reproduce the lane's central
pc = split_eval(central_args, central_args[1], central_args[1])
for k in ("total", "normalized", "fault_total", "fault_normalized", "mv_nonfatal", "nonmotorist"):
    assert abs(pc[k] - cen[k]) < 1e-9, (k, pc[k], cen[k])
print(f"  ✓ positive control: total {pc['total']:.3f}, normalized {pc['normalized']:.3f}, "
      f"fault {pc['fault_total']:.3f}")

w_pdo, parts = pdo_share_of_mv_nonfatal()
lookup = {(r["severity"], r["comparison"]): r for r in rows}
apply_rows = []
lane_or = central_args[1]
lane_m = (1 + lane_or) / 2


def scenario(label, or_inj, or_pdo, note):
    m_inj, m_pdo = (1 + or_inj) / 2, (1 + or_pdo) / 2
    scenario_m(label, w_pdo * m_pdo + (1 - w_pdo) * m_inj, m_inj, note, or_inj, or_pdo)


def scenario_m(label, m_mv, m_inj, note, or_inj=None, or_pdo=None):
    """m_mv: involvement multiplier for the non-fatal multi-vehicle part (cost-weighted over
    severities); m_inj: for the non-fatal non-motorist part."""
    m_pdo = (1 + or_pdo) / 2 if or_pdo is not None else None
    or_inj = 2 * m_inj - 1 if or_inj is None else or_inj
    r_mv = 2 * m_mv - 1  # odds ratio equivalent of the cost-weighted m
    # (1) the requested scaling: non-fatal components times m_measured / m_lane
    nm_nf_part = pc["nm_nonfatal"]
    mv_s = cen["mv_nonfatal"] * m_mv / lane_m
    nm_s = nm_nf_part * m_inj / lane_m
    total_s = cen["total"] - cen["mv_nonfatal"] - nm_nf_part + mv_s + nm_s
    v = cen["vmt_vs_avg"]
    norm_s = (mv_s * (1 - 1 / (v * m_mv)) + nm_s * (1 - 1 / (v * m_inj))
              + (cen["total"] - cen["mv_nonfatal"] - nm_nf_part) * (1 - 1 / (v * lane_m)))
    # (2) full re-evaluation: the odds ratio also moves the fault share in the liability term
    full = split_eval(central_args, r_mv, or_inj)
    apply_rows.append({
        "scenario": label, "note": note, "or_injury": or_inj, "or_pdo": or_pdo,
        "m_injury": m_inj, "m_pdo": m_pdo, "pdo_weight_in_mv_nonfatal": w_pdo, "m_mv_nonfatal": m_mv,
        "lane_m": lane_m,
        "mv_nonfatal_lane_bn": cen["mv_nonfatal"], "mv_nonfatal_scaled_bn": mv_s,
        "nm_nonfatal_lane_bn": nm_nf_part, "nm_nonfatal_scaled_bn": nm_s,
        "total_lane_bn": cen["total"], "total_scaled_bn": total_s,
        "normalized_lane_bn": cen["normalized"], "normalized_scaled_bn": norm_s,
        "total_full_reeval_bn": full["total"], "normalized_full_reeval_bn": full["normalized"],
        "fault_total_lane_bn": cen["fault_total"], "fault_total_full_reeval_bn": full["fault_total"],
        "fault_normalized_lane_bn": cen["fault_normalized"], "fault_normalized_full_reeval_bn": full["fault_normalized"],
        "per_member_usd_scaled": total_s * 1e9 / cm.N_GROUP,
    })


for cname in COMPARISONS:
    inj, pdo = lookup[("injury_all", cname)], lookup[("pdo", cname)]
    scenario(f"QIE within county x year, {cname}", inj["or_qie_mh_county_year"], pdo["or_qie_mh_county_year"],
             "central" if cname == "vs_all_non_hispanic" else "alternative reference")
    scenario(f"QIE crude, {cname}", inj["or_qie_crude"], pdo["or_qie_crude"], "check")
    scenario(f"mixed pairs, {cname}", inj["or_mixed_pair"], pdo["or_mixed_pair"], "check: mixing-robust")
    scenario(f"QIE within county x year, CI low, {cname}", inj["or_qie_mh_lo"], pdo["or_qie_mh_lo"], "sampling")
    scenario(f"QIE within county x year, CI high, {cname}", inj["or_qie_mh_hi"], pdo["or_qie_mh_hi"], "sampling")
hrb = {(r["severity"], r["comparison"], r["scenario"]): r for r in hr_rows}
for lab in ("impute fled drivers from victim race and county", "all unidentified fled drivers Hispanic",
            "no unidentified fled driver Hispanic"):
    scenario(f"hit-and-run: {lab}, vs_all_non_hispanic",
             hrb[("injury_all", "vs_all_non_hispanic", lab)]["or_qie_mh_county_year"],
             hrb[("pdo", "vs_all_non_hispanic", lab)]["or_qie_mh_county_year"], "hit-and-run bound")

# severity-weighted: police KABCO classes mapped onto the lane's MAIS cost rows (severe -> MAIS3-5,
# other visible -> MAIS2, complaint of pain -> MAIS0-1, PDO -> PDO); the mapping is approximate
m_by = {s: lookup[(s, "vs_all_non_hispanic")]["m_qie_mh"] for s in ("severe", "other_visible", "complaint_of_pain", "pdo")}
kab = {"PDO": "pdo", "MAIS0": "complaint_of_pain", "MAIS1": "complaint_of_pain", "MAIS2": "other_visible",
       "MAIS3": "severe", "MAIS4": "severe", "MAIS5": "severe"}
m_sevw = sum(parts[k] * m_by[kab[k]] for k in parts) / sum(parts.values())
m_inj_c = lookup[("injury_all", "vs_all_non_hispanic")]["m_qie_mh"]
scenario_m("severity-weighted (KABCO to MAIS), vs_all_non_hispanic", m_sevw, m_inj_c, "check: cost weights by severity")


def m_nf_at(k):
    ors = {sev: estimates(mnar_cube(sev, k)[0], "H", NH)["qie_mh"] for sev in ("injury_all", "pdo")}
    return w_pdo * (1 + ors["pdo"]) / 2 + (1 - w_pdo) * (1 + ors["injury_all"]) / 2, ors


for k in (2.0, 3.0):
    mk, ors = m_nf_at(k)
    scenario(f"hit-and-run MNAR: fled drivers' Hispanic odds x{k:g}, vs_all_non_hispanic",
             ors["injury_all"], ors["pdo"], "hit-and-run sensitivity")
lo_k, hi_k = 1.0, 200.0
if m_nf_at(hi_k)[0] > lane_m:
    for _ in range(60):
        mid = (lo_k * hi_k) ** 0.5
        lo_k, hi_k = (mid, hi_k) if m_nf_at(mid)[0] < lane_m else (lo_k, mid)
    k_star = hi_k
    share_star = {sev: mnar_cube(sev, k_star)[1] for sev in ("injury_all", "pdo")}
    share_mar = {sev: mnar_cube(sev, 1.0)[1] for sev in ("injury_all", "pdo")}
    mk, ors = m_nf_at(k_star)
    scenario(f"hit-and-run MNAR break-even k={k_star:.2f} (m back to the lane's), vs_all_non_hispanic",
             ors["injury_all"], ors["pdo"], "break-even")
    (OUT / "hit_and_run_break_even.json").write_text(json.dumps({
        "k_star": k_star, "fled_hispanic_share_at_k_star": share_star,
        "fled_hispanic_share_missing_at_random": share_mar, "lane_m": lane_m}, indent=1))

# licence-mediated flight: if drivers with licence class U (read here as unlicensed, an inference)
# flee F times as often as others, the fled pool's Hispanic odds rise by k(F) over missing-at-random
nf_all = prim[prim["sev"] != "fatal"]
u = {r: float((nf_all[nf_all["af_race"] == r]["af_lic"] == "U").mean()) for r in ("H", "W", "B", "A", "O")}
mix_nh = nf_all[nf_all["af_race"].isin(NH)]["af_race"].value_counts(normalize=True)
fled_known = two[two["af_fled"].astype(bool) & (two["af_race"] != "U") & (two["sev"] != "fatal")]
nonfled = two[~two["hr"] & (two["af_race"] != "U") & (two["sev"] != "fatal")]
p_u_fled = float((fled_known["af_lic"] == "U").mean())
p_u_nonfled = float((nonfled["af_lic"] == "U").mean())
F_hat = (p_u_fled / (1 - p_u_fled)) / (p_u_nonfled / (1 - p_u_nonfled))
flight_rows = []
# F is a free parameter: identified fled drivers almost never carry class U (their licence data come
# from later tracing), so F_hat below says nothing about flight and is kept only as that record
for F in (1.0, 2.0, 5.0, 10.0, 20.0, 50.0):
    k = (1 + (F - 1) * u["H"]) / sum(mix_nh[r] * (1 + (F - 1) * u[r]) for r in NH)
    mk, ors = m_nf_at(k)
    flight_rows.append({"flee_ratio_unlicensed_F": F, "hispanic_odds_multiplier_k": k,
                        "fled_hispanic_share_injury": mnar_cube("injury_all", k)[1],
                        "or_injury": ors["injury_all"], "or_pdo": ors["pdo"], "m_mv_nonfatal": mk})
write_csv("hit_and_run_licence_flight_model.csv", flight_rows)
(OUT / "licence_class_u_shares.json").write_text(json.dumps({
    "at_fault_share_class_U_nonfatal_primary": u, "identified_fled_at_fault_share_U": p_u_fled,
    "non_fled_at_fault_share_U": p_u_nonfled, "F_hat_odds_ratio_uninformative": F_hat,
    "identified_fled_at_fault_drivers_nonfatal": int(len(fled_known))}, indent=1))
write_csv("crash_component_revision.csv", apply_rows)
(OUT / "apply_meta.json").write_text(json.dumps({
    "lane_central": {k: cen[k] for k in ("total", "normalized", "fault_total", "fault_normalized", "mv_nonfatal",
                                          "mv_fatal", "nonmotorist", "single_vehicle", "m", "vmt_vs_avg", "R")},
    "lane_nm_nonfatal_part_bn": pc["nm_nonfatal"], "lane_nm_fatal_part_bn": pc["nm_fatal"],
    "pdo_share_of_mv_nonfatal_base": w_pdo, "mv_nonfatal_base_by_severity_bn": parts,
    "lane_or_central": lane_or, "n_group": cm.N_GROUP}, indent=1))
print(pd.DataFrame(apply_rows)[["scenario", "m_mv_nonfatal", "m_injury", "total_scaled_bn", "normalized_scaled_bn",
                                 "total_full_reeval_bn", "normalized_full_reeval_bn"]].to_string(index=False))

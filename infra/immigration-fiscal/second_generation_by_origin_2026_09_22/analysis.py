#!/usr/bin/env python3
"""Cluster-V V02 — second-generation adult outcomes by parental origin, IPUMS-CPS ASEC 1994-2025.

Descriptive only. Cross-sectional origin-group means by generation do not identify transmitted
culture, individual assimilation, or any causal effect of ancestry: family selection into
migration, destination, cohort, period and institutions all differ across the groups compared
here. Synthetic-cohort comparisons of a first generation observed today with a second generation
observed today are NOT the same people's children.

Run:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 analysis.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import warnings
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[2]
CPS_DIR = REPO / "sources" / "immigration-fiscal" / "data" / "external" / "cps"
SRC = CPS_DIR / "cps_2ndgen.csv.gz"
DDI = CPS_DIR / "cps_2ndgen.xml"
MANIFEST = CPS_DIR / "cps_2ndgen.manifest.json"
LOADER_CSV = REPO / "sources" / "immigration-fiscal" / "derived" / "lifetime" / "cps_second_gen_by_origin.csv"
LEDGER_CSV = (REPO / "infra" / "immigration-fiscal" / "gen_ledger_extension_2026_09_16"
              / "extended_ledger_by_generation.csv")
DERIVED = LANE / "derived"

BOOT_DRAWS = 200
BOOT_SEED = 20260922
MIN_N_REPORT = 100   # G5: no reported cell below this unweighted count
MIN_N_DESIGN = 20    # groups below this are dropped from the regression design (documented)

YEARS = list(range(1994, 2026))
NY = len(YEARS)
AGE_BAND_EDGES = [25, 30, 35, 40, 45, 50, 55, 60, 65]
NBAND = len(AGE_BAND_EDGES) - 1
NFE = NBAND * 2 * NY

PERIODS = [("1994-2004", 1994, 2004), ("2005-2014", 2005, 2014), ("2015-2025", 2015, 2025)]

# --- code sets, every one of them read back against the DDI in ddi_code_report() -------------
EMPSTAT_EMPLOYED = (10, 12)
EMPSTAT_ARMED_FORCES = 1
LABFORCE_IN = 2
LABFORCE_OUT = 1
EDUC_NIU = (0, 1, 999)
EDUC_COLLEGE_PLUS_MIN = 111        # 111 Bachelor's degree; 120-125 are above it
EDUC_LT_HS_MAX = 71                # 71 = 12th grade no diploma; 73 = HS diploma or equivalent
HISPAN_NOT = 0
HISPAN_MEXICAN = (100, 102, 103, 104, 108, 109)
RACE_WHITE = 100
CITIZEN_NATIVE = (1, 2, 3)         # born in US / US outlying / abroad of American parents
CITIZEN_FOREIGN = (4, 5)           # naturalized / not a citizen
CITIZEN_IS_CITIZEN = (1, 2, 3, 4)
NATIVITY_G1 = 5
NATIVITY_G2 = (2, 3, 4)
NATIVITY_G3 = 1
INC_MAX_REAL = 99999998            # 999999999 is the IPUMS NIU sentinel
BPL_MEXICO = 20000
BPL_US_MAX_GENERAL = 149           # general codes 99-120 are US and US outlying areas

# loader region map (infra/immigration-fiscal/build/load_cps_second_gen.py), applied to the
# GENERAL code = 5-digit code // 100.  'US outlying' is this lane's tenth category and holds the
# US-territory birthplaces (general 100-120) that the loader map leaves unassigned.
REGIONS = ["Mexico", "Central America", "Caribbean", "South America", "Europe", "Asia",
           "Africa", "Canada", "Other", "US outlying"]


def region_of(general: int) -> str:
    if 100 <= general <= 120:
        return "US outlying"
    if general == 200:
        return "Mexico"
    if general == 210:
        return "Central America"
    if general in (250, 260):
        return "Caribbean"
    if general == 300:
        return "South America"
    if 400 <= general <= 499:
        return "Europe"
    if 500 <= general <= 599:
        return "Asia"
    if 600 <= general <= 699:
        return "Africa"
    if general == 150:
        return "Canada"
    return "Other"


# ---------------------------------------------------------------------------------------------
# gates and provenance
# ---------------------------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ddi(path: Path) -> dict[str, dict[int, str]]:
    """variable -> {integer code: label} straight out of the IPUMS DDI."""
    root = ET.parse(path).getroot()
    out: dict[str, dict[int, str]] = {}
    for var in root.iter():
        if not var.tag.endswith("}var"):
            continue
        vid = var.attrib.get("ID")
        codes: dict[int, str] = {}
        for cat in var:
            if not cat.tag.endswith("catgry"):
                continue
            value = label = None
            for child in cat:
                if child.tag.endswith("catValu"):
                    value = child.text
                elif child.tag.endswith("labl"):
                    label = child.text
            if value is not None and label is not None:
                try:
                    codes[int(value)] = label
                except ValueError:
                    continue
        if codes:
            out[vid] = codes
    return out


def ddi_code_report(ddi: dict[str, dict[int, str]]) -> dict:
    """G4 — print every decision code with the label the DDI gives it, and assert the label."""
    def label(var: str, code: int) -> str:
        lab = ddi[var].get(code)
        if lab is None:
            raise AssertionError(f"G4: {var}={code} is not in the DDI code list")
        return lab

    report = {
        "EMPSTAT.employed": {str(c): label("EMPSTAT", c) for c in EMPSTAT_EMPLOYED},
        "EMPSTAT.armed_forces_dropped": {str(EMPSTAT_ARMED_FORCES): label("EMPSTAT", EMPSTAT_ARMED_FORCES)},
        "LABFORCE.in_labor_force": {str(LABFORCE_IN): label("LABFORCE", LABFORCE_IN)},
        "LABFORCE.out_of_labor_force": {str(LABFORCE_OUT): label("LABFORCE", LABFORCE_OUT)},
        "EDUC.college_plus_min": {str(EDUC_COLLEGE_PLUS_MIN): label("EDUC", EDUC_COLLEGE_PLUS_MIN)},
        "EDUC.lt_hs_max": {str(EDUC_LT_HS_MAX): label("EDUC", EDUC_LT_HS_MAX)},
        "EDUC.first_hs_completion": {"73": label("EDUC", 73)},
        "EDUC.niu": {str(c): label("EDUC", c) for c in EDUC_NIU},
        "HISPAN.not_hispanic": {str(HISPAN_NOT): label("HISPAN", HISPAN_NOT)},
        "HISPAN.mexican": {str(c): label("HISPAN", c) for c in HISPAN_MEXICAN},
        "RACE.white": {str(RACE_WHITE): label("RACE", RACE_WHITE)},
        "CITIZEN.native": {str(c): label("CITIZEN", c) for c in CITIZEN_NATIVE},
        "CITIZEN.foreign": {str(c): label("CITIZEN", c) for c in CITIZEN_FOREIGN},
        "NATIVITY.first_generation": {str(NATIVITY_G1): label("NATIVITY", NATIVITY_G1)},
        "NATIVITY.second_generation": {str(c): label("NATIVITY", c) for c in NATIVITY_G2},
        "NATIVITY.third_plus": {str(NATIVITY_G3): label("NATIVITY", NATIVITY_G3)},
        "BPL.mexico": {str(BPL_MEXICO): label("BPL", BPL_MEXICO)},
    }
    # the EDUC bracket has to be exactly "no HS credential" vs "BA or more"
    assert ddi["EDUC"][73].startswith("High school diploma"), ddi["EDUC"][73]
    assert ddi["EDUC"][111].startswith("Bachelor"), ddi["EDUC"][111]
    assert ddi["EMPSTAT"][EMPSTAT_ARMED_FORCES] == "Armed Forces"
    assert ddi["NATIVITY"][5] == "Foreign born"
    assert ddi["BPL"][BPL_MEXICO] == "Mexico"
    return report


# ---------------------------------------------------------------------------------------------
# G2 — reproduce the committed loader table from this lane's code
# ---------------------------------------------------------------------------------------------

LOADER_SQL = """
CREATE OR REPLACE TABLE repro AS
WITH base AS (
    SELECT
        CAST(NATIVITY AS INT) AS NATIVITY,
        CAST(ASECWT AS DOUBLE) AS w,
        CASE WHEN CAST(FBPL AS INT) // 100 >= 150 THEN CAST(FBPL AS INT) // 100
             WHEN CAST(MBPL AS INT) // 100 >= 150 THEN CAST(MBPL AS INT) // 100
             ELSE NULL END AS bpl_origin,
        CASE WHEN CAST(EMPSTAT AS INT) IN (10,12) THEN 1.0 ELSE 0.0 END AS employed,
        CASE WHEN CAST(INCTOT AS BIGINT) BETWEEN 1 AND 99999998 THEN ln(CAST(INCTOT AS DOUBLE)) END AS log_inc,
        CAST(EDUC AS INT) AS educ,
        CASE WHEN CAST(SEX AS INT)=2 AND CAST(LABFORCE AS INT)=2 THEN 1.0
             WHEN CAST(SEX AS INT)=2 THEN 0.0 END AS female_in_lf
    FROM _cps
    WHERE CAST(AGE AS INT) BETWEEN 25 AND 64
      AND NOT (CAST(YEAR AS INT) = 2014 AND COALESCE(CAST(HFLAG AS VARCHAR), '') = '1')
)
SELECT
    CASE NATIVITY
        WHEN 1 THEN '3rd+_native_parentage'
        WHEN 2 THEN '2nd_father_foreign'
        WHEN 3 THEN '2nd_mother_foreign'
        WHEN 4 THEN '2nd_both_foreign'
        WHEN 5 THEN '1st_foreign_born'
        ELSE 'unknown' END AS generation,
    CASE WHEN NATIVITY=1 THEN 'native_baseline' ELSE
      CASE
        WHEN bpl_origin=200 THEN 'Mexico'
        WHEN bpl_origin=210 THEN 'Central America'
        WHEN bpl_origin IN (250,260) THEN 'Caribbean'
        WHEN bpl_origin=300 THEN 'South America'
        WHEN bpl_origin BETWEEN 400 AND 499 THEN 'Europe'
        WHEN bpl_origin BETWEEN 500 AND 599 THEN 'Asia'
        WHEN bpl_origin BETWEEN 600 AND 699 THEN 'Africa'
        WHEN bpl_origin=150 THEN 'Canada'
        ELSE 'Other'
      END END AS parental_origin,
    round(sum(w*employed)/sum(w),4) AS emp_rate,
    round(sum(w*log_inc) FILTER (WHERE log_inc IS NOT NULL)
          /sum(w) FILTER (WHERE log_inc IS NOT NULL),4) AS mean_log_inc,
    round(sum(w*educ)/sum(w),2) AS mean_educ,
    round(sum(w*female_in_lf) FILTER (WHERE female_in_lf IS NOT NULL)
          /sum(w) FILTER (WHERE female_in_lf IS NOT NULL),4) AS female_lfp,
    round(sum(w)) AS weighted_n,
    count(*) AS n_obs
FROM base
WHERE NATIVITY IN (1,2,3,4,5)
GROUP BY 1,2
HAVING count(*) >= 100
ORDER BY generation, parental_origin
"""


def gate_g2(con) -> dict:
    con.execute(LOADER_SQL)
    got = con.execute("SELECT * FROM repro").df()
    want = pd.read_csv(LOADER_CSV)
    detail = {"rows_expected": int(len(want)), "rows_reproduced": int(len(got))}
    if len(got) != len(want):
        raise AssertionError(f"G2: row count {len(got)} != committed {len(want)}")
    if list(got.columns) != list(want.columns):
        raise AssertionError(f"G2: columns {list(got.columns)} != {list(want.columns)}")
    key = ["generation", "parental_origin"]
    got = got.sort_values(key).reset_index(drop=True)
    want = want.sort_values(key).reset_index(drop=True)
    for col in key:
        if not (got[col] == want[col]).all():
            raise AssertionError(f"G2: key column {col} differs")
    worst = 0.0
    for col in [c for c in want.columns if c not in key]:
        diff = np.abs(got[col].to_numpy(dtype=float) - want[col].to_numpy(dtype=float))
        worst = max(worst, float(np.nanmax(diff)))
        if not np.all(diff <= 1e-9):
            raise AssertionError(f"G2: column {col} max abs diff {np.nanmax(diff)} > 1e-9")
    detail["max_abs_diff"] = worst
    detail["tolerance"] = 1e-9
    detail["status"] = "PASS"
    return detail


# ---------------------------------------------------------------------------------------------
# G3 — population anchor against gen_ledger_extension_2026_09_16 (ASEC 2025)
# ---------------------------------------------------------------------------------------------

G3_TOLERANCE = 0.005

G3_SQL = {
    # ledger: PRCITSHP in (4,5) & PENATVTY == 303
    "mexico_born": ("CITIZEN IN (4,5) AND BPL = 20000"),
    # ledger: PRCITSHP in (1,2,3) & (PEFNTVTY == 303 | PEMNTVTY == 303)
    "mexican_second_gen": ("CITIZEN IN (1,2,3) AND (FBPL = 20000 OR MBPL = 20000)"),
    # ledger: PRCITSHP in (1,2,3) & parents in US areas & PEHSPNON == 2 & PRDTRACE == 1
    "third_plus_nh_white": ("CITIZEN IN (1,2,3) AND FBPL//100 < 150 AND MBPL//100 < 150 "
                            "AND HISPAN = 0 AND RACE = 100"),
    # ledger: PRCITSHP in (1,2,3) & parents in US areas & PRDTHSP == 1
    "mexican_third_plus_selfid": ("CITIZEN IN (1,2,3) AND FBPL//100 < 150 AND MBPL//100 < 150 "
                                  "AND HISPAN IN (100,102,103,104,108,109)"),
}


def gate_g3(con) -> dict:
    ledger = pd.read_csv(LEDGER_CSV)
    anchor = (ledger[ledger.weighting == "person"]
              .drop_duplicates("group").set_index("group")[["n_adults_unweighted", "weighted_adults"]])
    rows = []
    worst = 0.0
    for name, where in G3_SQL.items():
        n_obs, wsum = con.execute(
            f"SELECT count(*), sum(ASECWT) FROM _cps "
            f"WHERE YEAR = 2025 AND AGE BETWEEN 25 AND 64 AND EMPSTAT <> 1 AND ({where})"
        ).fetchone()
        want_n = int(anchor.loc[name, "n_adults_unweighted"])
        want_w = float(anchor.loc[name, "weighted_adults"])
        rel = abs(float(wsum) - want_w) / want_w
        worst = max(worst, rel)
        rows.append({"group": name, "ipums_n_obs": int(n_obs), "ledger_n_obs": want_n,
                     "ipums_weighted": float(wsum), "ledger_weighted": want_w,
                     "rel_diff": rel})
        if rel > G3_TOLERANCE:
            raise AssertionError(f"G3: {name} weighted {wsum} vs ledger {want_w} — rel {rel:.5f}")
        if int(n_obs) != want_n:
            raise AssertionError(f"G3: {name} unweighted {n_obs} vs ledger {want_n}")
    return {"status": "PASS", "tolerance_rel": G3_TOLERANCE, "worst_rel_diff": worst,
            "universe": "ASEC 2025, civilian (EMPSTAT<>1) adults 25-64, ASECWT — the ledger's own "
                        "adults_25_64 & PRPERTYP==2 universe, person weighting",
            "rows": rows}


# ---------------------------------------------------------------------------------------------
# analysis frame
# ---------------------------------------------------------------------------------------------

FRAME_SQL = """
SELECT CAST(YEAR AS INT) AS year, CAST(SERIAL AS BIGINT) AS serial,
       CAST(ASECWT AS DOUBLE) AS w, CAST(AGE AS INT) AS age, CAST(SEX AS INT) AS sex,
       CAST(RACE AS INT) AS race, CAST(HISPAN AS INT) AS hispan, CAST(NCHILD AS INT) AS nchild,
       CAST(BPL AS INT) AS bpl, CAST(FBPL AS INT) AS fbpl, CAST(MBPL AS INT) AS mbpl,
       CAST(CITIZEN AS INT) AS citizen, CAST(NATIVITY AS INT) AS nativity,
       CAST(EMPSTAT AS INT) AS empstat, CAST(LABFORCE AS INT) AS labforce,
       CAST(EDUC AS INT) AS educ, CAST(INCTOT AS BIGINT) AS inctot,
       CAST(INCWAGE AS BIGINT) AS incwage
FROM _cps
WHERE CAST(AGE AS INT) BETWEEN 25 AND 64
  AND CAST(EMPSTAT AS INT) <> 1
  AND CAST(NATIVITY AS INT) IN (1,2,3,4,5)
  AND NOT (CAST(YEAR AS INT) = 2014 AND HFLAG = '1')
ORDER BY year, serial
"""


def top_countries(df: pd.DataFrame, k: int = 10) -> list[int]:
    """The k largest single PARENTAL birthplaces by weighted second-generation count."""
    g2 = df[df.nativity.isin(NATIVITY_G2)]
    code = np.where(g2.fbpl.to_numpy() // 100 >= 150, g2.fbpl.to_numpy(), g2.mbpl.to_numpy())
    ok = code // 100 >= 150
    tab = pd.DataFrame({"code": code[ok], "w": g2.w.to_numpy()[ok]}).groupby("code").w.sum()
    return [int(c) for c in tab.sort_values(ascending=False).head(k).index]


def build_groups(df: pd.DataFrame, countries: list[int]) -> dict:
    """Fine partition of the sample: (origin x generation) for G1/G2, three cells for G3+."""
    nat = df.nativity.to_numpy()
    fbpl, mbpl, bpl = df.fbpl.to_numpy(), df.mbpl.to_numpy(), df.bpl.to_numpy()

    # G1 origin = own birthplace; G2 origin = father's when foreign, else mother's
    parent = np.where(fbpl // 100 >= 150, fbpl, np.where(mbpl // 100 >= 150, mbpl, -1))
    parent_out = np.where((parent < 0) & ((fbpl // 100 >= 100) | (mbpl // 100 >= 100)),
                          np.where(fbpl // 100 >= 100, fbpl, mbpl), parent)
    origin_code = np.where(nat == NATIVITY_G1, bpl, parent_out)

    general = origin_code // 100
    # vectorised region lookup over the handful of general codes that actually occur
    uniq, inv = np.unique(general, return_inverse=True)
    region_lut = np.array([region_of(int(g)) for g in uniq], dtype=object)
    region = region_lut[inv]
    # codes that are neither a foreign country nor a US area (origin_code == -1) cannot happen
    # once the US-outlying fallback is applied; assert it rather than silently bucket them.
    origin_bearing = np.isin(nat, list(NATIVITY_G2) + [NATIVITY_G1])
    if (origin_code[origin_bearing] < 0).any():
        n_bad = int((origin_code[origin_bearing] < 0).sum())
        raise AssertionError(f"{n_bad} G1/G2 persons have no assignable birthplace code")
    niu = origin_bearing & np.isin(origin_code, (99999, 96000))
    if niu.any():
        raise AssertionError(f"{int(niu.sum())} G1/G2 persons carry an unknown/NIU birthplace code; "
                             "the region map would silently file them under 'Other'")

    # fine origin: 0..9 = the ten countries, 10..19 = each region's residual
    fine_origin = np.full(len(df), -1, dtype=np.int64)
    for i, code in enumerate(countries):
        fine_origin[origin_bearing & (origin_code == code)] = i
    resid = origin_bearing & (fine_origin < 0)
    for j, r in enumerate(REGIONS):
        fine_origin[resid & (region == r)] = 10 + j
    if (fine_origin[origin_bearing] < 0).any():
        raise AssertionError("unmapped fine origin")

    gen_idx = np.full(len(df), -1, dtype=np.int64)   # 0 father-foreign, 1 mother-foreign, 2 both, 3 G1
    gen_idx[nat == 2] = 0
    gen_idx[nat == 3] = 1
    gen_idx[nat == 4] = 2
    gen_idx[nat == NATIVITY_G1] = 3

    n_fine_origin = 10 + len(REGIONS)
    fine = np.full(len(df), -1, dtype=np.int64)
    fine[origin_bearing] = fine_origin[origin_bearing] * 4 + gen_idx[origin_bearing]
    base = n_fine_origin * 4
    third = nat == NATIVITY_G3
    nhw = third & (df.hispan.to_numpy() == HISPAN_NOT) & (df.race.to_numpy() == RACE_WHITE)
    mex3 = third & np.isin(df.hispan.to_numpy(), HISPAN_MEXICAN)
    fine[third] = base + 2
    fine[nhw] = base + 0
    fine[mex3] = base + 1
    if (fine < 0).any():
        raise AssertionError("unmapped fine group")

    labels = {}
    country_name = {}
    for i, code in enumerate(countries):
        country_name[i] = code
    gen_name = ["2nd_father_foreign", "2nd_mother_foreign", "2nd_both_foreign", "1st_foreign_born"]
    for i in range(n_fine_origin):
        oname = f"country:{countries[i]}" if i < 10 else f"region_residual:{REGIONS[i - 10]}"
        for g in range(4):
            labels[i * 4 + g] = (oname, gen_name[g])
    labels[base + 0] = ("3rd+_NH_white", "3rd+")
    labels[base + 1] = ("3rd+_Mexican_selfid", "3rd+")
    labels[base + 2] = ("3rd+_other", "3rd+")
    return {"fine": fine, "n_fine": base + 3, "base": base, "labels": labels,
            "n_fine_origin": n_fine_origin, "countries": countries}


def build_taxonomies(G: dict, ddi: dict) -> dict:
    """Each taxonomy is a list of (name, [fine ids]) partitioning the sample."""
    n_fo, base, countries = G["n_fine_origin"], G["base"], G["countries"]
    bpl_lab = ddi["BPL"]
    cname = {i: bpl_lab[c] for i, c in enumerate(countries)}
    region_members = {r: [] for r in REGIONS}
    for i, c in enumerate(countries):
        region_members[region_of(c // 100)].append(i)
    for j, r in enumerate(REGIONS):
        region_members[r].append(10 + j)

    third = [("3rd+_NH_white", [base + 0]), ("3rd+_Mexican_selfid", [base + 1]),
             ("3rd+_other", [base + 2])]
    G1, G2ALL = [3], [0, 1, 2]

    tax = {}
    groups = []
    for r in REGIONS:
        for gname, gs in (("1st_foreign_born", G1), ("2nd_gen_all", G2ALL)):
            groups.append((f"{r}|{gname}", [o * 4 + g for o in region_members[r] for g in gs]))
    tax["region_gen_union"] = groups + third

    groups = []
    for r in REGIONS:
        for gname, gs in (("1st_foreign_born", [3]), ("2nd_father_foreign", [0]),
                          ("2nd_mother_foreign", [1]), ("2nd_both_foreign", [2])):
            groups.append((f"{r}|{gname}", [o * 4 + g for o in region_members[r] for g in gs]))
    tax["region_gen_detail"] = groups + third

    groups = []
    for i in range(10):
        for gname, gs in (("1st_foreign_born", G1), ("2nd_gen_all", G2ALL)):
            groups.append((f"{cname[i]}|{gname}", [i * 4 + g for g in gs]))
    for gname, gs in (("1st_foreign_born", G1), ("2nd_gen_all", G2ALL)):
        groups.append((f"Other origin|{gname}", [o * 4 + g for o in range(10, n_fo) for g in gs]))
    tax["country_gen_union"] = groups + third
    return tax


def taxonomy_matrix(groups: list, n_fine: int) -> np.ndarray:
    M = np.zeros((len(groups), n_fine))
    for i, (_, members) in enumerate(groups):
        M[i, members] = 1.0
    if not np.all(M.sum(0) <= 1.0 + 1e-12):
        raise AssertionError("taxonomy groups overlap")
    return M


# ---------------------------------------------------------------------------------------------
# estimators
# ---------------------------------------------------------------------------------------------

def raw_gaps(W: np.ndarray, Y: np.ndarray, ref: int) -> np.ndarray:
    """Unadjusted difference in weighted means against the reference group."""
    n = W.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = np.where(n > 0, Y.sum(1) / np.where(n > 0, n, 1.0), np.nan)
    return mean - mean[ref]


def wls_gaps(W: np.ndarray, Y: np.ndarray, ref: int, keep: np.ndarray | None = None):
    """Weighted least squares of y on group dummies with a full set of FE-cell dummies.

    W[g, f] = weighted count, Y[g, f] = weighted sum of y, for group g and fixed-effect cell f.
    The FE block is diagonal, so the coefficients on the group dummies come out of the Schur
    complement of the normal equations; that is algebraically the same number the dense dummy
    regression gives, at a fraction of the cost. Returns gaps against `ref` (gaps[ref] = 0).
    """
    n_groups = W.shape[0]
    gaps = np.full(n_groups, np.nan)
    n_g = W.sum(1)
    if keep is None:
        keep = n_g > 0
    keep = keep & (n_g > 0)
    if not keep[ref]:
        return gaps, "reference-empty"
    Wk, Yk = W[keep], Y[keep]
    n_f = Wk.sum(0)
    fkeep = n_f > 0
    if not fkeep.any():
        return gaps, "no-fe-cells"
    idx_local = np.where(keep)[0]
    ref_local = int(np.where(idx_local == ref)[0][0])
    other = np.array([i for i in range(len(idx_local)) if i != ref_local])
    if other.size == 0:
        return gaps, "only-reference"
    T = Wk[np.ix_(other, np.where(fkeep)[0])]
    nf = n_f[fkeep]
    Sf = Yk[:, fkeep].sum(0)
    Tn = T / nf
    M = np.diag(Wk[other].sum(1)) - Tn @ T.T
    rhs = Yk[other].sum(1) - Tn @ Sf
    status = "ok"
    try:
        beta = np.linalg.solve(M, rhs)
        if not np.all(np.isfinite(beta)):
            raise np.linalg.LinAlgError("non-finite")
    except np.linalg.LinAlgError:
        beta, *_ = np.linalg.lstsq(M, rhs, rcond=None)
        status = "lstsq-fallback"
    gaps[idx_local[other]] = beta
    gaps[ref] = 0.0
    return gaps, status


def closing_ratio(gap_g1: float, gap_g2: float) -> float:
    """Share of the first-generation gap that the second generation has closed."""
    if not np.isfinite(gap_g1) or not np.isfinite(gap_g2) or gap_g1 == 0.0:
        return np.nan
    return 1.0 - gap_g2 / gap_g1


# ---------------------------------------------------------------------------------------------
# outcomes
# ---------------------------------------------------------------------------------------------

def build_outcomes(df: pd.DataFrame) -> list[dict]:
    empstat = df.empstat.to_numpy()
    labforce = df.labforce.to_numpy()
    educ = df.educ.to_numpy()
    inctot = df.inctot.to_numpy()
    incwage = df.incwage.to_numpy()
    sex = df.sex.to_numpy()
    age = df.age.to_numpy()
    nat = df.nativity.to_numpy()
    citizen = df.citizen.to_numpy()
    nchild = df.nchild.to_numpy()

    lf_universe = np.isin(labforce, (LABFORCE_OUT, LABFORCE_IN))
    educ_universe = ~np.isin(educ, EDUC_NIU)
    inc_pos = (inctot >= 1) & (inctot <= INC_MAX_REAL)
    wage_pos = (incwage >= 1) & (incwage <= INC_MAX_REAL)
    wage_universe = incwage <= INC_MAX_REAL

    out = [
        dict(name="employed", label="employed (EMPSTAT 10 or 12)", gaps=True,
             mask=np.ones(len(df), bool), y=np.isin(empstat, EMPSTAT_EMPLOYED).astype(float)),
        dict(name="in_labor_force", label="in the labor force (LABFORCE 2)", gaps=True,
             mask=lf_universe, y=(labforce == LABFORCE_IN).astype(float)),
        dict(name="female_lfp", label="women in the labor force (LABFORCE 2 | SEX 2)", gaps=True,
             mask=lf_universe & (sex == 2), y=(labforce == LABFORCE_IN).astype(float)),
        dict(name="college_plus", label="bachelor's degree or more (EDUC >= 111)", gaps=True,
             mask=educ_universe, y=(educ >= EDUC_COLLEGE_PLUS_MIN).astype(float)),
        dict(name="less_than_hs", label="no high-school credential (EDUC <= 71)", gaps=True,
             mask=educ_universe, y=((educ <= EDUC_LT_HS_MAX) & (educ >= 2)).astype(float)),
        dict(name="log_inctot", label="log total personal income | positive", gaps=True,
             mask=inc_pos, y=np.log(np.where(inc_pos, inctot, 1).astype(float))),
        dict(name="positive_wage", label="any wage and salary income (INCWAGE > 0)", gaps=True,
             mask=wage_universe, y=wage_pos.astype(float)),
        dict(name="log_incwage", label="log wage and salary income | positive", gaps=True,
             mask=wage_pos, y=np.log(np.where(wage_pos, incwage, 1).astype(float))),
        dict(name="children_women_40_49", label="coresident own children, women 40-49 (NCHILD)",
             gaps=True, mask=(sex == 2) & (age >= 40) & (age <= 49), y=nchild.astype(float)),
        dict(name="us_citizen_g1", label="US citizen, first generation only (CITIZEN 1-4)",
             gaps=False, mask=(nat == NATIVITY_G1), y=np.isin(citizen, CITIZEN_IS_CITIZEN).astype(float)),
    ]
    return out


# ---------------------------------------------------------------------------------------------
# tabulation engine
# ---------------------------------------------------------------------------------------------

class Engine:
    """Bins the sample once, then re-tabulates cheaply for every bootstrap draw."""

    def __init__(self, df: pd.DataFrame, fine: np.ndarray, n_fine: int):
        age = df.age.to_numpy()
        band = np.clip((age - 25) // 5, 0, NBAND - 1)
        sex0 = df.sex.to_numpy() - 1
        yidx = df.year.to_numpy() - YEARS[0]
        self.fe = (band * 2 + sex0) * NY + yidx
        self.fine = fine
        self.n_fine = n_fine
        self.bin = fine * NFE + self.fe
        self.nbins = n_fine * NFE
        self.w = df.w.to_numpy(dtype=float)
        serial = df.serial.to_numpy().astype(np.int64)
        if serial.max() >= 10_000_000:
            raise AssertionError("SERIAL overflows the year*1e7 household key")
        key = df.year.to_numpy().astype(np.int64) * 10_000_000 + serial
        _, self.hh = np.unique(key, return_inverse=True)
        self.n_hh = int(self.hh.max()) + 1
        # household -> year block, for a within-year cluster resample
        first = np.zeros(self.n_hh, dtype=np.int64)
        first[self.hh[::-1]] = np.arange(len(self.hh))[::-1]
        self.hh_year = df.year.to_numpy()[first]
        self.year_blocks = []
        for y in YEARS:
            ids = np.where(self.hh_year == y)[0]
            if ids.size:
                if ids[-1] - ids[0] + 1 != ids.size:
                    raise AssertionError(f"household ids for {y} are not contiguous")
                self.year_blocks.append((int(ids[0]), int(ids[-1]) + 1))
        if sum(hi - lo for lo, hi in self.year_blocks) != self.n_hh:
            raise AssertionError("year blocks do not cover every household")
        self.period_cols = {}
        year_of_fe = np.tile(np.arange(NY), NBAND * 2)
        for pname, lo, hi in PERIODS:
            self.period_cols[pname] = ((year_of_fe + YEARS[0]) >= lo) & ((year_of_fe + YEARS[0]) <= hi)
        self.period_cols["all"] = np.ones(NFE, bool)

    def prepare(self, outcomes: list[dict]):
        for o in outcomes:
            m = o["mask"]
            o["idx"] = self.bin[m]
            o["hh_m"] = self.hh[m]
            o["w_m"] = self.w[m]
            o["y_m"] = o["y"][m]
            o["wy_m"] = o["w_m"] * o["y_m"]
            o["n_obs_fine"] = np.bincount(o["idx"], minlength=self.nbins).reshape(self.n_fine, NFE)

    def tables(self, o: dict, mult: np.ndarray | None):
        if mult is None:
            w, wy = o["w_m"], o["wy_m"]
        else:
            m = mult[o["hh_m"]]
            w = o["w_m"] * m
            wy = o["wy_m"] * m
        W = np.bincount(o["idx"], weights=w, minlength=self.nbins).reshape(self.n_fine, NFE)
        Y = np.bincount(o["idx"], weights=wy, minlength=self.nbins).reshape(self.n_fine, NFE)
        return W, Y

    def draw_multipliers(self, rng) -> np.ndarray:
        mult = np.empty(self.n_hh, dtype=float)
        for lo, hi in self.year_blocks:
            n = hi - lo
            mult[lo:hi] = np.bincount(rng.integers(0, n, size=n), minlength=n)
        return mult


# ---------------------------------------------------------------------------------------------
# one full pass over every reported statistic
# ---------------------------------------------------------------------------------------------

REF_GROUP = "3rd+_NH_white"


def reference_index(tax: dict) -> dict:
    out = {}
    for tname, groups in tax.items():
        hits = [i for i, (n, _) in enumerate(groups) if n == REF_GROUP]
        if len(hits) != 1:
            raise AssertionError(f"{tname}: {len(hits)} reference groups named {REF_GROUP}")
        out[tname] = hits[0]
    return out


def collect(engine: Engine, outcomes: list[dict], tax: dict, mats: dict, design_keep: dict,
            refs: dict, mult: np.ndarray | None):
    """Returns flat float vectors: cell means, adjusted gaps, raw gaps — one pass per outcome."""
    cells, adj, raw, status = [], [], [], []
    for o in outcomes:
        W, Y = engine.tables(o, mult)
        for tname, groups in tax.items():
            M = mats[tname]
            Wc, Yc = M @ W, M @ Y
            ref = refs[tname]
            for pname, cols in engine.period_cols.items():
                Wp, Yp = Wc[:, cols], Yc[:, cols]
                n = Wp.sum(1)
                with np.errstate(invalid="ignore", divide="ignore"):
                    cells.append(np.where(n > 0, Yp.sum(1) / np.where(n > 0, n, 1.0), np.nan))
                if o["gaps"]:
                    g, st = wls_gaps(Wp, Yp, ref, design_keep[(o["name"], tname, pname)])
                    adj.append(g)
                    raw.append(raw_gaps(Wp, Yp, ref))
                    status.append(st)
                else:
                    adj.append(np.full(len(groups), np.nan))
                    raw.append(np.full(len(groups), np.nan))
                    status.append("no-gaps")
    return np.concatenate(cells), np.concatenate(adj), np.concatenate(raw), status


def main() -> int:
    t0 = time.time()
    DERIVED.mkdir(exist_ok=True)
    audit: dict = {"lane": LANE.name, "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "gates": {}}

    print("[G1] manifest sha256")
    manifest = json.loads(MANIFEST.read_text())
    got = sha256_file(SRC)
    if got != manifest["sha256"]:
        raise AssertionError(f"G1: sha256 {got} != manifest {manifest['sha256']}")
    audit["gates"]["G1_manifest_sha256"] = {"status": "PASS", "sha256": got,
                                            "file": str(SRC.relative_to(REPO)),
                                            "bytes": int(manifest["bytes"])}
    audit["ddi_sha256"] = sha256_file(DDI)
    audit["analysis_py_sha256"] = sha256_file(Path(__file__).resolve())
    print(f"       PASS {got}")

    import duckdb
    con = duckdb.connect()
    con.execute(f"CREATE VIEW _cps AS SELECT * FROM read_csv_auto('{SRC}', header=true)")

    print("[G4] DDI code list")
    ddi = parse_ddi(DDI)
    audit["gates"]["G4_ddi_codes"] = {"status": "PASS", "codes": ddi_code_report(ddi)}
    for key, labels in audit["gates"]["G4_ddi_codes"]["codes"].items():
        print(f"       {key}: " + "; ".join(f"{k}={v}" for k, v in labels.items()))

    print("[G2] reproduce cps_second_gen_by_origin")
    audit["gates"]["G2_loader_reproduction"] = gate_g2(con)
    print(f"       PASS {audit['gates']['G2_loader_reproduction']['rows_reproduced']} rows, "
          f"max abs diff {audit['gates']['G2_loader_reproduction']['max_abs_diff']:.2e}")

    print("[G3] ASEC 2025 population anchor vs gen_ledger_extension_2026_09_16")
    audit["gates"]["G3_population_anchor"] = gate_g3(con)
    for r in audit["gates"]["G3_population_anchor"]["rows"]:
        print(f"       {r['group']:<26} ipums {r['ipums_weighted']:>14,.0f} "
              f"ledger {r['ledger_weighted']:>14,.0f}  rel {r['rel_diff']:.2e}")

    # ---- the 2014 double count -------------------------------------------------------------
    by_flag = con.execute("SELECT HFLAG, sum(ASECWT) FROM _cps WHERE YEAR=2014 GROUP BY 1 "
                          "ORDER BY 1").fetchall()
    neigh = con.execute("SELECT YEAR, sum(ASECWT) FROM _cps WHERE YEAR IN (2013,2015) "
                        "GROUP BY 1 ORDER BY 1").fetchall()
    audit["sample_decisions"] = {
        "asecflag": "the extract is ASEC only (ASECFLAG = 1 for all 5,721,633 records); no March "
                    "Basic records to drop",
        "hflag_2014": {
            "finding": "both 2014 parts carry full-population weights, so keeping both double "
                       "counts 2014",
            "weighted_by_hflag": {str(f): float(s) for f, s in by_flag},
            "weighted_2013_2015": {str(y): float(s) for y, s in neigh},
            "choice": "drop HFLAG = 1 (the 3/8 redesign sample); keep HFLAG = 0 (5/8 traditional) "
                      "so the income questions are comparable with 1994-2013",
        },
        "civilian": "EMPSTAT = 1 (Armed Forces) dropped, matching the ledger's PRPERTYP = 2 "
                    "civilian-adult universe",
        "nativity_unknown": "NATIVITY = 0 (Unknown) dropped, as the loader does",
        "g1_origin": "first generation takes its origin from its own BPL (the brief), not from "
                     "parental birthplace as the committed loader does",
        "us_outlying": "birthplaces in general codes 100-120 (Puerto Rico, Guam, USVI, American "
                       "Samoa, outlying n.s.) are a tenth origin category, 'US outlying'; the "
                       "loader's nine-region map leaves them unassigned",
    }
    print(f"[sample] 2014 by HFLAG: " + ", ".join(f"{f}={s:,.0f}" for f, s in by_flag)
          + "; 2013/2015 " + ", ".join(f"{y}={s:,.0f}" for y, s in neigh)
          + " -> dropping HFLAG=1")

    print("[load] analysis frame")
    df = con.execute(FRAME_SQL).df()
    con.close()
    print(f"       {len(df):,} civilian adults 25-64, {df.year.nunique()} ASEC years")

    countries = top_countries(df)
    print("[origins] top ten parental birthplaces: "
          + ", ".join(f"{ddi['BPL'][c]}" for c in countries))
    Gf = build_groups(df, countries)

    # what actually sits in the tenth, lane-added origin category
    us_out = df[(df.nativity == NATIVITY_G1) & (df.bpl // 100 >= 100)
                & (df.bpl // 100 <= 120)]
    comp = (us_out.groupby("bpl").w.agg(["size", "sum"])
            .sort_values("sum", ascending=False))
    audit["us_outlying_composition"] = {
        "universe": "first generation (NATIVITY 5) whose own birthplace is a US area, general "
                    "codes 100-120; the second-generation side of the category is built the same "
                    "way from parental birthplace",
        "n_obs_total": int(len(us_out)), "weighted_total": float(us_out.w.sum()),
        "by_birthplace": [{"bpl": int(c), "label": ddi["BPL"][int(c)], "n_obs": int(row["size"]),
                           "weighted": float(row["sum"]),
                           "weighted_share": float(row["sum"] / us_out.w.sum())}
                          for c, row in comp.iterrows()],
    }
    top = audit["us_outlying_composition"]["by_birthplace"][0]
    print(f"[origins] 'US outlying' first generation: {len(us_out):,} obs, largest is "
          f"{top['label']} at {top['weighted_share']:.1%} of weight")
    tax = build_taxonomies(Gf, ddi)
    mats = {k: taxonomy_matrix(v, Gf["n_fine"]) for k, v in tax.items()}
    outcomes = build_outcomes(df)

    engine = Engine(df, Gf["fine"], Gf["n_fine"])
    engine.prepare(outcomes)
    print(f"       {engine.n_hh:,} households, {NFE} age-band x sex x year cells, "
          f"{Gf['n_fine']} fine groups")

    # design-inclusion masks, fixed at the point estimate so every draw fits the same model
    design_keep, n_obs_report = {}, {}
    for o in outcomes:
        for tname, groups in tax.items():
            Nc = mats[tname] @ o["n_obs_fine"]
            for pname, cols in engine.period_cols.items():
                n = Nc[:, cols].sum(1)
                design_keep[(o["name"], tname, pname)] = n >= MIN_N_DESIGN
                n_obs_report[(o["name"], tname, pname)] = n

    # ---- point estimates --------------------------------------------------------------------
    print("[estimate] point estimates")
    refs = reference_index(tax)
    cells0, adj0, raw0, status = collect(engine, outcomes, tax, mats, design_keep, refs, None)
    bad = sorted({s for s in status if s not in ("ok", "no-gaps")})
    audit["wls_status"] = {"unique_statuses": sorted(set(status)),
                           "n_lstsq_fallback": int(sum(s == "lstsq-fallback" for s in status))}
    if bad:
        print(f"       WLS fallbacks: {bad} on {audit['wls_status']['n_lstsq_fallback']} fits")

    # index map, identical ordering to collect()
    index = []
    for o in outcomes:
        for tname, groups in tax.items():
            for pname in engine.period_cols:
                for gi, (gname, _) in enumerate(groups):
                    index.append((o["name"], o["label"], tname, pname, gname,
                                  float(n_obs_report[(o["name"], tname, pname)][gi])))
    idx = pd.DataFrame(index, columns=["outcome", "outcome_label", "taxonomy", "period",
                                       "group", "n_obs"])
    assert len(idx) == len(cells0) == len(adj0) == len(raw0), (len(idx), len(cells0))

    # ---- bootstrap ---------------------------------------------------------------------------
    print(f"[bootstrap] {BOOT_DRAWS} household-cluster draws, seed {BOOT_SEED}")
    rng = np.random.default_rng(BOOT_SEED)
    B_cells = np.empty((BOOT_DRAWS, len(cells0)))
    B_adj = np.empty((BOOT_DRAWS, len(adj0)))
    B_raw = np.empty((BOOT_DRAWS, len(raw0)))
    for b in range(BOOT_DRAWS):
        mult = engine.draw_multipliers(rng)
        B_cells[b], B_adj[b], B_raw[b], _ = collect(engine, outcomes, tax, mats, design_keep,
                                                    refs, mult)
        if (b + 1) % 25 == 0:
            print(f"       draw {b + 1}/{BOOT_DRAWS}  {time.time() - t0:6.1f}s")

    def se(mat, point):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            s = np.nanstd(mat, axis=0, ddof=1)
        s[~np.isfinite(point)] = np.nan
        return s

    idx["mean"] = cells0
    idx["se_mean"] = se(B_cells, cells0)
    idx["adjusted_gap"] = adj0
    idx["se_adjusted_gap"] = se(B_adj, adj0)
    idx["raw_gap"] = raw0
    idx["se_raw_gap"] = se(B_raw, raw0)
    idx["reported"] = idx.n_obs >= MIN_N_REPORT

    # ---- outputs ------------------------------------------------------------------------------
    rep = idx[idx.reported].copy()

    cells_out = rep[["outcome", "outcome_label", "taxonomy", "period", "group", "n_obs",
                     "mean", "se_mean"]].copy()
    cells_out.to_csv(DERIVED / "cells.csv", index=False)

    gaps_out = rep[rep.adjusted_gap.notna()][
        ["outcome", "outcome_label", "taxonomy", "period", "group", "n_obs",
         "adjusted_gap", "se_adjusted_gap", "raw_gap", "se_raw_gap"]].copy()
    gaps_out.to_csv(DERIVED / "adjusted_gaps.csv", index=False)

    # ---- closing ratios, recomputed inside every draw so the ratio carries a cluster SE ------
    pos = {(r.outcome, r.taxonomy, r.period, r.group): i for i, r in enumerate(idx.itertuples())}
    warnings.simplefilter("ignore", RuntimeWarning)
    ratio_rows = []
    for o in outcomes:
        if not o["gaps"]:
            continue
        for tname, groups in tax.items():
            names = [g for g, _ in groups]
            origins = sorted({n.split("|")[0] for n in names if "|" in n})
            for origin in origins:
                g1n, g2n = f"{origin}|1st_foreign_born", f"{origin}|2nd_gen_all"
                if g1n not in names or g2n not in names:
                    continue
                for pname in engine.period_cols:
                    i1 = pos.get((o["name"], tname, pname, g1n))
                    i2 = pos.get((o["name"], tname, pname, g2n))
                    if i1 is None or i2 is None:
                        continue
                    if not (idx.reported.iloc[i1] and idx.reported.iloc[i2]):
                        continue
                    adj_r = closing_ratio(adj0[i1], adj0[i2])
                    raw_r = closing_ratio(raw0[i1], raw0[i2])
                    bs_adj = np.array([closing_ratio(B_adj[b, i1], B_adj[b, i2])
                                       for b in range(BOOT_DRAWS)])
                    bs_raw = np.array([closing_ratio(B_raw[b, i1], B_raw[b, i2])
                                       for b in range(BOOT_DRAWS)])
                    ratio_rows.append(dict(
                        outcome=o["name"], outcome_label=o["label"], taxonomy=tname,
                        period=pname, origin=origin,
                        g1_adjusted_gap=adj0[i1], se_g1_adjusted_gap=idx.se_adjusted_gap.iloc[i1],
                        g2_adjusted_gap=adj0[i2], se_g2_adjusted_gap=idx.se_adjusted_gap.iloc[i2],
                        closing_ratio_adjusted=adj_r,
                        se_closing_ratio_adjusted=float(np.nanstd(bs_adj, ddof=1)),
                        p025_closing_ratio_adjusted=float(np.nanpercentile(bs_adj, 2.5)),
                        p975_closing_ratio_adjusted=float(np.nanpercentile(bs_adj, 97.5)),
                        g1_raw_gap=raw0[i1], g2_raw_gap=raw0[i2],
                        closing_ratio_raw=raw_r,
                        se_closing_ratio_raw=float(np.nanstd(bs_raw, ddof=1)),
                        n_obs_g1=idx.n_obs.iloc[i1], n_obs_g2=idx.n_obs.iloc[i2]))
    ratios = pd.DataFrame(ratio_rows)
    ratios.to_csv(DERIVED / "closing_ratios.csv", index=False)

    # ---- period trends -------------------------------------------------------------------------
    trend = rep[rep.period != "all"].copy()
    trend = trend[["outcome", "outcome_label", "taxonomy", "period", "group", "n_obs", "mean",
                   "se_mean", "adjusted_gap", "se_adjusted_gap"]]
    wide = []
    for (out_, tax_, grp), sub in trend.groupby(["outcome", "taxonomy", "group"], sort=False):
        row = {"outcome": out_, "taxonomy": tax_, "group": grp}
        s = sub.set_index("period")
        for pname, _, _ in PERIODS:
            if pname in s.index:
                row[f"mean_{pname}"] = float(s.loc[pname, "mean"])
                row[f"se_mean_{pname}"] = float(s.loc[pname, "se_mean"])
                row[f"gap_{pname}"] = float(s.loc[pname, "adjusted_gap"])
                row[f"se_gap_{pname}"] = float(s.loc[pname, "se_adjusted_gap"])
        first, last = PERIODS[0][0], PERIODS[-1][0]
        if f"mean_{first}" in row and f"mean_{last}" in row:
            row["change_mean_first_to_last"] = row[f"mean_{last}"] - row[f"mean_{first}"]
        if f"gap_{first}" in row and f"gap_{last}" in row:
            row["change_gap_first_to_last"] = row[f"gap_{last}"] - row[f"gap_{first}"]
        wide.append(row)
    trends = pd.DataFrame(wide)
    # bootstrap SE of the first->last change, recomputed inside the draw
    ch_mean_se, ch_gap_se = [], []
    for r in trends.itertuples():
        kf = (r.outcome, r.taxonomy, PERIODS[0][0], r.group)
        kl = (r.outcome, r.taxonomy, PERIODS[-1][0], r.group)
        if kf in pos and kl in pos:
            ch_mean_se.append(float(np.nanstd(B_cells[:, pos[kl]] - B_cells[:, pos[kf]], ddof=1)))
            ch_gap_se.append(float(np.nanstd(B_adj[:, pos[kl]] - B_adj[:, pos[kf]], ddof=1)))
        else:
            ch_mean_se.append(np.nan)
            ch_gap_se.append(np.nan)
    trends["se_change_mean"] = ch_mean_se
    trends["se_change_gap"] = ch_gap_se
    trends.to_csv(DERIVED / "period_trends.csv", index=False)

    # ---- G5 ------------------------------------------------------------------------------------
    print("[G5] reporting floor and finite standard errors")
    if (cells_out.n_obs < MIN_N_REPORT).any():
        raise AssertionError("G5: a reported cell is below the unweighted floor")
    if not np.isfinite(cells_out.se_mean.to_numpy()).all():
        raise AssertionError("G5: a reported cell mean has a non-finite standard error")
    if not np.isfinite(gaps_out.se_adjusted_gap.to_numpy()).all():
        raise AssertionError("G5: a reported adjusted gap has a non-finite standard error")
    nonfinite_ratio = int((~np.isfinite(ratios.se_closing_ratio_adjusted.to_numpy())).sum())
    audit["gates"]["G5_cell_floor_and_finite_se"] = {
        "status": "PASS", "min_n_report": MIN_N_REPORT,
        "cells_reported": int(len(cells_out)),
        "cells_suppressed_below_floor": int((~idx.reported).sum()),
        "gaps_reported": int(len(gaps_out)),
        "closing_ratios": int(len(ratios)),
        "closing_ratios_with_nonfinite_se": nonfinite_ratio,
        "note": "a closing ratio is a ratio of two estimated gaps; where the first-generation gap "
                "is near zero the ratio is unstable and its bootstrap spread is reported as it "
                "comes out, not trimmed",
    }
    print(f"       PASS {len(cells_out)} cells, {len(gaps_out)} gaps, {len(ratios)} ratios; "
          f"{int((~idx.reported).sum())} cells suppressed below n={MIN_N_REPORT}")

    audit["universe"] = {
        "rows": int(len(df)), "households": int(engine.n_hh),
        "years": [int(df.year.min()), int(df.year.max())], "n_years": int(df.year.nunique()),
        "definition": "civilian adults 25-64, ASECWT, NATIVITY 1-5, 2014 3/8 redesign dropped",
        "weighted_total": float(df.w.sum()),
    }
    audit["design"] = {
        "fixed_effects": f"{NBAND} five-year age bands x sex x {NY} survey years = {NFE} cells",
        "reference_group": "third-plus generation, non-Hispanic white (NATIVITY 1, HISPAN 0, RACE 100)",
        "also_reported": "3rd+_other is the all-native-parentage residual; the loader's "
                         "native_baseline is the union of 3rd+_NH_white, 3rd+_Mexican_selfid and "
                         "3rd+_other and is reproduced exactly in G2",
        "taxonomies": {k: [n for n, _ in v] for k, v in tax.items()},
        "top_ten_parental_birthplaces": {str(c): ddi["BPL"][c] for c in countries},
        "min_n_design": MIN_N_DESIGN, "min_n_report": MIN_N_REPORT,
        "estimator": "weighted least squares of the outcome on group dummies plus a full set of "
                     "age-band x sex x survey-year dummies; the group coefficients are the "
                     "reported adjusted gaps and no coefficient on a control is reported",
    }
    audit["bootstrap"] = {
        "draws": BOOT_DRAWS, "seed": BOOT_SEED,
        "cluster": "household (YEAR, SERIAL), resampled with replacement within each survey year",
        "applies_to": "every reported mean, adjusted gap, raw gap, closing ratio and period change",
        "limitation": "this extract carries no replicate weights, so the resample ignores the CPS "
                      "stratified PSU design; the CPS design effect is above one, so every "
                      "standard error here is a LOWER BOUND on the true sampling error",
        "second_limitation": "the CPS rotation panel returns about half of each March sample the "
                             "following March, and resampling SERIAL within YEAR treats the same "
                             "household in two adjacent ASECs as two independent clusters; that "
                             "makes the pooled multi-year standard errors a lower bound for a "
                             "second, separate reason",
    }
    audit["limitations"] = [
        "Descriptive. Cross-sectional generation contrasts are not the same families followed over "
        "time; the first generation observed in a period is not the parent generation of the "
        "second generation observed in the same period.",
        "Origin-group differences confound selection into migration, cohort of arrival, "
        "destination, legal status and period with anything transmitted within families.",
        "Age and sex adjustment plus survey-year fixed effects remove composition on those margins "
        "only. Education, state of residence and legal status are NOT controlled, by design: they "
        "are outcomes or endogenous to the comparison.",
        "NCHILD counts coresident own children, not completed fertility (see "
        "research/immigration-gated-data-specs-2026-06-25.md section 1).",
        "EDUC is a categorical attainment code; college_plus and less_than_hs are shares built from "
        "the DDI code list, and no years-of-schooling scale is imputed.",
        "INCTOT and INCWAGE are nominal as reported, not deflated; survey-year fixed effects absorb "
        "the common price level within a year but period means in levels are not comparable across "
        "periods and only the gaps to the same-year reference are.",
        "Income means are conditional on positive income, so they mix a participation margin into "
        "the level; positive_wage is reported alongside for that reason.",
        "Standard errors ignore the CPS PSU design AND the CPS rotation panel (about half of each "
        "March sample returns the following March), so they are lower bounds twice over.",
        "IPUMS NATIVITY treats people born in US outlying areas and people born abroad to American "
        "parents as foreign-born, so a small number of US citizens by birth sit in the first "
        "generation here. The ledger's PRCITSHP rule treats them as native; that difference is "
        "why the G3 anchor uses CITIZEN rather than NATIVITY.",
        "The loader table reproduced in G2 (build/load_cps_second_gen.py; a local derived file "
        "under sources/, not tracked) kept both 2014 ASEC files until 2026-09-22 and now drops "
        "the 3/8 redesign file as this lane does; its cells still differ from this lane's in "
        "universe (armed forces kept), origin rule (parental birthplace for the first "
        "generation too) and the missing US-outlying category.",
    ]
    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")

    print(f"[done] {time.time() - t0:.1f}s -> {DERIVED}")
    for f in sorted(DERIVED.iterdir()):
        print(f"       {f.name}  {f.stat().st_size:,} bytes")

    # ---- console headline, Mexico first ---------------------------------------------------------
    print()
    print("MEXICO — adjusted gap to third-plus non-Hispanic white, all years, region taxonomy")
    sel = gaps_out[(gaps_out.taxonomy == "region_gen_union") & (gaps_out.period == "all")
                   & (gaps_out.group.str.startswith("Mexico|"))]
    for r in sel.itertuples():
        print(f"   {r.outcome:<22} {r.group:<28} {r.adjusted_gap:+8.4f} ({r.se_adjusted_gap:.4f})")
    print()
    print("MEXICO — closing ratios, all years, region taxonomy")
    rsel = ratios[(ratios.taxonomy == "region_gen_union") & (ratios.period == "all")
                  & (ratios.origin == "Mexico")]
    for r in rsel.itertuples():
        print(f"   {r.outcome:<22} ratio {r.closing_ratio_adjusted:+.4f} "
              f"({r.se_closing_ratio_adjusted:.4f})  raw {r.closing_ratio_raw:+.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

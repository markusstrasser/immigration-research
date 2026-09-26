#!/usr/bin/env python3
"""Mexico-born returnees from the US (ENADID) against Mexico-born people still in the US (ACS PUMS).

Returnees: Mexico-born adults 20-64 resident in Mexico at an ENADID survey (2018, 2023) who lived
in the United States five years before it. Read from enadid_return_selectivity_2026_09_22/derived/,
never recomputed, and gated against that lane's RESULT.md tables.
Stayers: ACS one-year person PUMS of the same survey year, POBP 303 (Mexico), AGEP 20-64,
YOEP <= year - 5 (in the US at the start of the window; year - 6 as a sensitivity), group quarters
kept. Weights PWGTP; standard errors from the 80 successive-difference replicate weights,
SE^2 = 4/80 * sum_r (theta_r - theta)^2, negative and zero replicate values kept.
Schooling: ACS SCHL -> the shared attainment scale of schooling_selection_position_2026_09_23
(SCHL map and years imported from that lane) -> the four INEGI niv_esc bands the ENADID lane uses.
Differences are returnee minus stayer; the samples are independent, so SE = sqrt(se_ret^2 + se_stay^2).
Standardized stayer figures reweight stayer cells to the returnees' weighted_pop by cell, which
is treated as fixed.

Specs (SPECS): the brief's main case, YOEP <= year - 6, (a) SCHL 18 as tertiary, (b) half of US
diplomas and GEDs read as secundaria, (c) allocated schooling dropped, the non-citizen undercount
at k = 1.10/1.25/1.75, and three added here: (d) households only, as ENADID samples; (e) 2023 mean
years with the excess of the ACS 2020 no-schooling step returned to grades 1-9; (f) stayers who
arrived aged 18 or older. Short-stay returnees are set beside ACS arrivals inside the window.

Outputs in derived/: stayers_by_schooling.csv, comparison.csv, anchor.csv,
acs_no_schooling_break.csv, audit.json.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/compare.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pcsv

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
DERIVED = LANE / "derived"
ENADID_LANE = LANE.parent / "enadid_return_selectivity_2026_09_22"
SCHOOLING_LANE = LANE.parent / "schooling_selection_position_2026_09_23"

sys.path.insert(0, str(SCHOOLING_LANE))
from acs_pums_check import SCHL as SCHL_LEVEL  # noqa: E402  ACS SCHL (2008+) -> shared-scale index
from levels import YEARS as LEVEL_YEARS  # noqa: E402  approximate completed years per scale index

WAVES = (2018, 2023)
PUMS = {
    2018: {"zip": ROOT / "sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_2018.zip",
           # acs_pums_years/download.log, [ok] 2018 line
           "sha256": "73fba8988d84f6425966fa14ab26af6ab40ebc0f0e16156b0dada39322349243",
           "rel": "RELP", "gq_rel": (16, 17), "records": None},
    2023: {"zip": ROOT / "sources/immigration-fiscal/data/census/acs_pums_2023_person.zip",
           # service_by_ses_2026_09_23/derived/acs_inputs.json; verify_acs_2023.sh checks it against Census
           "sha256": "98b6ecb14b4830d1f2b54c265a5bd997828415c2dab14e17369c40e98b78d9d4",
           "rel": "RELSHIPP", "gq_rel": (37, 38), "records": 3405809},
}
PUMS_MEMBERS = ["psam_pusa.csv", "psam_pusb.csv"]
REP = [f"PWGTP{i}" for i in range(1, 81)]

# ACS published Mexico-born population, table B05006 (place of birth for the foreign-born
# population), United States, one-year. The keyless api.census.gov table endpoint redirected to
# missing_key.html on 2026-09-26, so the values come from data.census.gov's table API (responses
# kept in _cache/b05006_<year>_us.json, not tracked).
ANCHOR = {
    2018: {"variable": "B05006_139E", "estimate": 11171893, "moe90": 79577,
           "label": "Estimate!!Total!!Americas!!Latin America!!Central America!!Mexico",
           "url": "https://data.census.gov/api/access/data/table?id=ACSDT1Y2018.B05006&g=010XX00US"},
    2023: {"variable": "B05006_160E", "estimate": 10918205, "moe90": 87367,
           "label": "Estimate!!Total:!!Americas:!!Latin America:!!Central America:!!Mexico",
           "url": "https://data.census.gov/api/access/data/table?id=ACSDT1Y2023.B05006&g=010XX00US"},
}
ANCHOR_RETRIEVED = "2026-09-26"
ANCHOR_TOL = 0.005      # build gate
ANCHOR_EXPLAIN = 0.002  # gaps above this get a stated explanation

ENADID_RESULT = ENADID_LANE / "RESULT.md"
ENADID_RETURNEES = ENADID_LANE / "derived/return_migrants_by_schooling.csv"
ENADID_DEPARTURES = ENADID_LANE / "derived/departures_by_schooling.csv"

# IPUMS USA extract 3 (Mexico-born, ACS 2005-2024), used only for the 2019/2020 no-schooling break.
IPUMS_MEXBORN = ROOT / "sources/immigration-fiscal/derived/ipums_usa/usa_00003_census1980-2000+acs2005-2024_mexborn.parquet"
IPUMS_MEXBORN_SHA = "4779fe688d764cb41751afde1ac44f5b2a80d5c19f622b2f34b0ab638f6dfa37"

BAND_ORDER = ["lt_lower_secondary", "lower_secondary", "upper_secondary", "tertiary"]
MEASURES = BAND_ORDER + ["mean_years_schooling"]
YEARS_COL = MEASURES.index("mean_years_schooling")
AGE_BANDS = [(20, 29), (30, 39), (40, 49), (50, 59), (60, 64)]
AGE_LABELS = [f"{lo}-{hi}" for lo, hi in AGE_BANDS]
SEX_LABELS = {1: "men", 2: "women"}  # ACS SEX and ENADID sexo share the coding
CELLS = [f"sex:{s}|age:{a}" for s in SEX_LABELS.values() for a in AGE_LABELS]
SLICES = (["all"] + [f"sex:{s}" for s in SEX_LABELS.values()] + [f"age:{a}" for a in AGE_LABELS] + CELLS)
# Standardized stayer figures: slice -> (label, returnee cells whose weighted_pop sets the weights)
STANDARDIZED = {
    "sex:men": ("age_within_sex", [c for c in CELLS if c.startswith("sex:men|")]),
    "sex:women": ("age_within_sex", [c for c in CELLS if c.startswith("sex:women|")]),
    "all": ("sex_age", CELLS),
}

# The brief's main SCHL -> ENADID band mapping, checked against the shared scale at start-up.
BRIEF_MAIN_BANDS = {**{s: "lt_lower_secondary" for s in range(1, 12)}, 12: "lower_secondary",
                    **{s: "upper_secondary" for s in range(13, 19)},
                    **{s: "tertiary" for s in range(19, 25)}}
SCHL18_TERTIARY_YEARS = 13.0  # sensitivity (a): one approved tertiary year, the least that reading implies
UNDERCOUNT_K = (1.10, 1.25, 1.75)

ADULT_ARRIVAL_AGE = 18  # sensitivity f: stayers who arrived as adults, schooling mostly from Mexico


def spec(name: str, lag: int = 5, coding: str = "main", drop_allocated: bool = False, drop_gq: bool = False,
         k: float = 1.0, min_arrival_age: int | None = None) -> dict:
    return {"name": name, "lag": lag, "coding": coding, "drop_allocated": drop_allocated, "drop_gq": drop_gq,
            "k": k, "min_arrival_age": min_arrival_age}


SPECS = [
    spec("main"),
    spec("yoep_le_year_minus_6", lag=6),
    spec("a_schl18_as_tertiary", coding="a"),
    spec("b_half_diploma_as_secundaria", coding="b"),
    spec("c_drop_allocated_schooling", drop_allocated=True),
    spec("d_households_only", drop_gq=True),           # added: ENADID samples households only
    spec("e_no_schooling_break", coding="e"),           # added: 2023 only, mean years only
    spec("f_stayers_arrived_as_adults", min_arrival_age=ADULT_ARRIVAL_AGE),  # added
] + [spec(f"undercount_k{k:.2f}", k=k) for k in UNDERCOUNT_K]
SHORT_STAY_SPECS = [("short_stay_recent_arrivals", "main"), ("short_stay_recent_arrivals_a", "a")]


class GateFailure(RuntimeError):
    """A hard gate failed. Never downgraded to a warning."""


def gate(condition: bool, message: str) -> None:
    if not condition:
        raise GateFailure(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- schooling
def level_band(level: int) -> str:
    """INEGI niv_esc band on the shared scale (levels.py): L9 is secundaria completa; L10-L13 any
    approved grade of media superior (US grades 10-12, diploma, GED, under a year of college);
    L14 and above any approved tertiary year."""
    if level <= 8:
        return "lt_lower_secondary"
    if level == 9:
        return "lower_secondary"
    if level <= 13:
        return "upper_secondary"
    return "tertiary"


SCHL_BAND = {s: level_band(lv) for s, lv in SCHL_LEVEL.items()}
SCHL_YEARS = {s: float(LEVEL_YEARS[lv]) for s, lv in SCHL_LEVEL.items()}


def check_schooling_maps() -> None:
    gate(sorted(SCHL_LEVEL) == list(range(1, 25)), "[BLOCKED] imported SCHL map does not cover codes 1-24")
    gate(SCHL_BAND == BRIEF_MAIN_BANDS, "[BLOCKED] shared-scale bands differ from the brief's SCHL mapping")


def outcomes(schl: np.ndarray, coding: str, break_years: float | None = None) -> np.ndarray:
    """Outcome matrix (n x 5): four band indicators (fractional under coding b) and years.

    main  the brief's mapping; years from the shared scale
    a     SCHL 18 (some college, under one year) read as tertiary, years 13
    b     half of SCHL 16-17 (US diploma or GED) re-read as Mexican secundaria, years 9 for that half
    e     SCHL 1 (no schooling) scored at `break_years`, the expected years of a no-schooling
          report once the 2020 break's excess is returned to grades 1-9; bands as main
    """
    gate(coding in ("main", "a", "b", "e"), f"[BLOCKED] unknown coding {coding}")
    n = len(schl)
    Y = np.zeros((n, len(MEASURES)))
    band_idx = np.array([BAND_ORDER.index(SCHL_BAND[s]) for s in schl], dtype=int)
    Y[np.arange(n), band_idx] = 1.0
    Y[:, YEARS_COL] = [SCHL_YEARS[s] for s in schl]
    if coding == "a":
        m = schl == 18
        Y[m, :4] = 0.0
        Y[m, BAND_ORDER.index("tertiary")] = 1.0
        Y[m, YEARS_COL] = SCHL18_TERTIARY_YEARS
    elif coding == "b":
        m = np.isin(schl, (16, 17))
        Y[m, :4] = 0.0
        Y[m, BAND_ORDER.index("lower_secondary")] = 0.5
        Y[m, BAND_ORDER.index("upper_secondary")] = 0.5
        Y[m, YEARS_COL] = 0.5 * 9.0 + 0.5 * SCHL_YEARS[16]
    elif coding == "e":
        gate(break_years is not None, "[BLOCKED] coding e needs break_years")
        Y[schl == 1, YEARS_COL] = break_years
    return Y


def undercount_multiplier(cit: np.ndarray, schl: np.ndarray, k: float) -> np.ndarray:
    """k for non-citizens (CIT 5) in the two lowest bands, 1 elsewhere (main band mapping)."""
    low = np.isin([SCHL_BAND[s] for s in schl], ("lt_lower_secondary", "lower_secondary"))
    return np.where((cit == 5) & low, k, 1.0)


# ---------------------------------------------------------------- estimation
def estimate(Y: np.ndarray, W: np.ndarray) -> np.ndarray:
    """Weighted means of each column of Y under the full weight (column 0 of W) and the 80
    replicates (columns 1-80). Returns shape (n_measures, 81)."""
    den = W.sum(axis=0)
    gate(bool((den > 0).all()), "[BLOCKED] empty or non-positive weight total in a domain")
    return (Y.T @ W) / den


def sdr_se(theta: np.ndarray) -> np.ndarray:
    """ACS successive-difference replicate SE: sqrt(4/80 * sum_r (theta_r - theta_0)^2)."""
    theta = np.asarray(theta, dtype=float)
    gate(theta.shape[-1] == 81, "[BLOCKED] replicate SE needs the full estimate plus 80 replicates")
    d = theta[..., 1:] - theta[..., :1]
    return np.sqrt(4.0 / 80.0 * (d ** 2).sum(axis=-1))


def standardization_weights(ret: dict, wave: int, cells: list[str]) -> np.ndarray:
    """Per-measure returnee weights over `cells`, normalized to sum to one: shape (n_cells, 5).
    Band measures use the known-band weighted_pop, mean years the known-years one."""
    w = np.array([[ret[(wave, c, m)]["w"] for m in MEASURES] for c in cells], dtype=float)
    gate(bool((w >= 0).all()) and bool((w.sum(axis=0) > 0).all()), "[BLOCKED] bad returnee cell weights")
    p = w / w.sum(axis=0)
    gate(bool(np.allclose(p.sum(axis=0), 1.0, atol=1e-12)), "[BLOCKED] standardization weights do not sum to one")
    return p


def standardize(cell_theta: list[np.ndarray], p: np.ndarray) -> np.ndarray:
    """Sum over cells of p[cell, measure] * theta[cell][measure, replicate] -> shape (5, 81)."""
    stack = np.stack(cell_theta)  # (n_cells, 5, 81)
    return (p[:, :, None] * stack).sum(axis=0)


# ---------------------------------------------------------------- ENADID side
LABEL_TO_MEASURE = {"Less than lower secondary": "lt_lower_secondary", "Lower secondary": "lower_secondary",
                    "Upper secondary": "upper_secondary", "Tertiary": "tertiary",
                    "Mean years of schooling": "mean_years_schooling"}


def _table_after(lines: list[str], start: int) -> list[list[str]]:
    j = start + 1
    while j < len(lines) and not lines[j].startswith("|"):
        j += 1
    rows = []
    while j < len(lines) and lines[j].startswith("|"):
        rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
        j += 1
    return rows


def parse_enadid_result(text: str) -> dict:
    """Numbers the ENADID lane printed in RESULT.md that this lane reads from its CSVs."""
    lines = text.splitlines()
    exp = {"level": {}, "n_all": {}, "w_all": {}, "n_sex": {}, "n_age": {}, "linked": {}, "women_share": {},
           "departures": {}}
    for i, line in enumerate(lines):
        m = re.match(r"^\| (2018|2023) \| (Returned|Still abroad) \| ([\d,]+) \| ([\d,]+) \| ([\d.]+) \| ([\d.]+) \|",
                     line)
        if m:
            group = "returned" if m[2] == "Returned" else "still_abroad"
            exp["departures"][(int(m[1]), group)] = {"n": int(m[3].replace(",", "")),
                                                     "weighted": int(m[4].replace(",", "")),
                                                     "men": (float(m[5]), float(m[6]))}
        m = re.match(r"^\*\*(2018|2023)\*\* — returnees n = ([\d,]+) \(weighted ([\d,]+)\)", line)
        if m:
            wave = int(m[1])
            exp["n_all"][wave] = int(m[2].replace(",", ""))
            exp["w_all"][wave] = int(m[3].replace(",", ""))
            for cells in _table_after(lines, i):
                if cells[0] in LABEL_TO_MEASURE:
                    exp["level"][(wave, LABEL_TO_MEASURE[cells[0]])] = (float(cells[1]), float(cells[2]))
        m = re.match(r"^\| (2018|2023) \| (Men|Women) \| ([\d,]+) \|", line)
        if m:
            exp["n_sex"][(int(m[1]), m[2].lower())] = int(m[3].replace(",", ""))
        m = re.match(r"^\| (2018|2023) \| (\d\d)–(\d\d) \| ([\d,]+) \|", line)
        if m:
            exp["n_age"][(int(m[1]), f"{m[2]}-{m[3]}")] = int(m[4].replace(",", ""))
        if line.startswith("Restricted to the same universe as the resident table"):
            for cells in _table_after(lines, i):
                if cells[0] in LABEL_TO_MEASURE:
                    band = LABEL_TO_MEASURE[cells[0]]
                    exp["linked"][(2018, band)] = (float(cells[1]), float(cells[2]))
                    exp["linked"][(2023, band)] = (float(cells[3]), float(cells[4]))
    m = re.search(r"Women are ([\d.]+) percent of the weighted\s+2018 returnee population and ([\d.]+) "
                  r"percent of the 2023 one", text)
    if m:
        exp["women_share"] = {2018: float(m[1]), 2023: float(m[2])}
    expected_sizes = {"level": 10, "n_all": 2, "w_all": 2, "n_sex": 4, "n_age": 10, "linked": 8, "women_share": 2,
                      "departures": 4}
    for key, size in expected_sizes.items():
        gate(len(exp[key]) == size, f"[BLOCKED] ENADID RESULT.md parse: {key} has {len(exp[key])} entries, "
                                    f"expected {size}; the table layout changed")
    return exp


def load_returnees() -> tuple[dict, dict, dict]:
    df = pd.read_csv(ENADID_RETURNEES)
    df = df[(df["group"] == "returnee_from_us") & df["wave"].isin(WAVES)]
    ret = {}
    for r in df.itertuples(index=False):
        ret[(int(r.wave), r.slice, r.measure)] = {"estimate": float(r.estimate), "se": float(r.se),
                                                  "n": int(r.n_unweighted), "w": float(r.weighted_pop)}
    for wave in WAVES:
        for s in SLICES:
            for m in MEASURES:
                gate((wave, s, m) in ret, f"[BLOCKED] ENADID returnee row missing: {wave} {s} {m}")
    dep = pd.read_csv(ENADID_DEPARTURES)
    linked, coverage = {}, {}
    for r in dep[dep["group"] == "returned"].itertuples(index=False):
        if r.measure == "linked_schooling_share_20_64":
            linked[(int(r.wave), r.category)] = {"estimate": float(r.estimate), "se": float(r.se),
                                                 "n_band": int(r.n_unweighted)}
        elif r.measure in ("linked_20_64_coverage", "weighted_count"):
            coverage[(int(r.wave), r.measure)] = {"n": int(r.n_unweighted), "estimate": float(r.estimate)}
        elif r.measure == "share_sex" and r.category == "men":
            coverage[(int(r.wave), "returned_share_men")] = {"n": int(r.n_unweighted), "estimate": float(r.estimate),
                                                             "se": float(r.se)}
    for r in dep[dep["group"] == "still_abroad"].itertuples(index=False):
        if r.measure == "weighted_count":
            coverage[(int(r.wave), "still_abroad_weighted_count")] = {"n": int(r.n_unweighted),
                                                                      "estimate": float(r.estimate)}
    for wave in WAVES:
        for band in BAND_ORDER:
            gate((wave, band) in linked, f"[BLOCKED] ENADID linked share missing: {wave} {band}")
        for key in ("linked_20_64_coverage", "weighted_count", "returned_share_men", "still_abroad_weighted_count"):
            gate((wave, key) in coverage, f"[BLOCKED] ENADID departure row missing: {wave} {key}")
    return ret, linked, coverage


def gate_returnees(ret: dict, linked: dict, coverage: dict, exp: dict) -> list[str]:
    """Every returnee number used here must match the ENADID lane's printed tables, and the
    cell rows must aggregate exactly to the gated slices."""
    passed = []
    for (wave, measure), (val, se) in exp["level"].items():
        row = ret[(wave, "all", measure)]
        scale = 1.0 if measure == "mean_years_schooling" else 100.0
        gate(abs(scale * row["estimate"] - val) <= 0.005 + 1e-9,
             f"[BLOCKED] ENADID {wave} {measure}: CSV {scale * row['estimate']:.4f} != RESULT.md {val}")
        gate(abs(scale * row["se"] - se) <= 0.005 + 1e-9,
             f"[BLOCKED] ENADID {wave} {measure} SE: CSV {scale * row['se']:.4f} != RESULT.md {se}")
        passed.append(f"{wave} all {measure} estimate and SE")
    for wave in WAVES:
        row = ret[(wave, "all", "tertiary")]
        gate(row["n"] == exp["n_all"][wave], f"[BLOCKED] ENADID {wave} returnee n {row['n']} != {exp['n_all'][wave]}")
        gate(abs(row["w"] - exp["w_all"][wave]) <= 0.5, f"[BLOCKED] ENADID {wave} weighted returnees differ")
        women = ret[(wave, "sex:women", "tertiary")]["w"] / row["w"]
        gate(abs(100 * women - exp["women_share"][wave]) <= 0.05 + 1e-9,
             f"[BLOCKED] ENADID {wave} women share {100 * women:.3f} != {exp['women_share'][wave]}")
        passed += [f"{wave} returnee n and weighted total", f"{wave} women share"]
    for (wave, sex), n in exp["n_sex"].items():
        gate(ret[(wave, f"sex:{sex}", "tertiary")]["n"] == n, f"[BLOCKED] ENADID {wave} {sex} n differs")
        passed.append(f"{wave} {sex} n")
    for (wave, age), n in exp["n_age"].items():
        gate(ret[(wave, f"age:{age}", "tertiary")]["n"] == n, f"[BLOCKED] ENADID {wave} age {age} n differs")
        passed.append(f"{wave} age {age} n")
    for (wave, band), (val, se) in exp["linked"].items():
        row = linked[(wave, band)]
        gate(abs(100 * row["estimate"] - val) <= 0.005 + 1e-9 and abs(100 * row["se"] - se) <= 0.005 + 1e-9,
             f"[BLOCKED] ENADID linked {wave} {band}: CSV {100 * row['estimate']:.4f} != RESULT.md {val}")
        passed.append(f"{wave} linked {band} estimate and SE")
    for (wave, group), d in exp["departures"].items():
        count = coverage[(wave, "weighted_count" if group == "returned" else "still_abroad_weighted_count")]
        gate(count["n"] == d["n"] and abs(count["estimate"] - d["weighted"]) <= 0.5,
             f"[BLOCKED] ENADID {wave} {group} departures: CSV n {count['n']}, weighted {count['estimate']:.0f} "
             f"!= RESULT.md {d['n']}, {d['weighted']}")
        passed.append(f"{wave} {group} departures n and weighted count")
        if group == "returned":
            men = coverage[(wave, "returned_share_men")]
            gate(abs(100 * men["estimate"] - d["men"][0]) <= 0.005 + 1e-9
                 and abs(100 * men["se"] - d["men"][1]) <= 0.005 + 1e-9,
                 f"[BLOCKED] ENADID {wave} returned men share {100 * men['estimate']:.4f} != {d['men'][0]}")
            passed.append(f"{wave} returned departures men share and SE")
    # Cells aggregate to sex and age slices, and those to the pooled slice (exact for ratio estimators).
    for wave in WAVES:
        for m in MEASURES:
            groups = {f"sex:{s}": [c for c in CELLS if c.startswith(f"sex:{s}|")] for s in SEX_LABELS.values()}
            groups.update({f"age:{a}": [c for c in CELLS if c.endswith(f"|age:{a}")] for a in AGE_LABELS})
            groups["all"] = CELLS
            for parent, cells in groups.items():
                w = np.array([ret[(wave, c, m)]["w"] for c in cells])
                est = np.array([ret[(wave, c, m)]["estimate"] for c in cells])
                top = ret[(wave, parent, m)]
                gate(abs(w.sum() - top["w"]) <= 0.5, f"[BLOCKED] ENADID {wave} {parent} {m}: cell weights "
                                                     f"{w.sum():.1f} != slice {top['w']:.1f}")
                gate(abs((w * est).sum() / w.sum() - top["estimate"]) <= 1e-9,
                     f"[BLOCKED] ENADID {wave} {parent} {m}: cells do not aggregate to the slice")
        for s in SLICES:
            tot = sum(ret[(wave, s, b)]["estimate"] for b in BAND_ORDER)
            gate(abs(tot - 1.0) <= 1e-9, f"[BLOCKED] ENADID {wave} {s} band shares sum to {tot}")
        passed.append(f"{wave} cells aggregate to every sex, age and pooled slice; band shares sum to one")
    return passed


# ---------------------------------------------------------------- ACS side
def read_mexico_born(year: int, audit: dict) -> dict:
    cfg = PUMS[year]
    zp = cfg["zip"]
    gate(zp.exists(), f"[BLOCKED] missing {zp}")
    sha = sha256_file(zp)
    gate(sha == cfg["sha256"], f"[BLOCKED] {zp.name} sha256 {sha} != pinned {cfg['sha256']}")
    cols = ["SERIALNO", "SPORDER", "POBP", "AGEP", "SEX", "SCHL", "FSCHLP", "YOEP", "CIT", cfg["rel"], "PWGTP"] + REP
    types = {c: pa.int64() for c in cols}
    types["SERIALNO"] = pa.string()
    parts, n_all = [], 0
    with zipfile.ZipFile(zp) as zf:
        members = sorted(n for n in zf.namelist() if n.lower().endswith(".csv"))
        gate(members == PUMS_MEMBERS, f"[BLOCKED] {zp.name} CSV members {members} != {PUMS_MEMBERS}")
        for member in members:
            with zf.open(member) as fh:
                reader = pcsv.open_csv(fh, read_options=pcsv.ReadOptions(block_size=1 << 26),
                                       convert_options=pcsv.ConvertOptions(include_columns=cols, column_types=types))
                for batch in reader:
                    n_all += batch.num_rows
                    parts.append(batch.filter(pc.equal(batch.column("POBP"), 303)))
    if cfg["records"] is not None:
        gate(n_all == cfg["records"], f"[BLOCKED] {year} person records {n_all} != recorded {cfg['records']}")
    d = pa.Table.from_batches(parts).to_pandas()
    gate(len(d) > 50_000, f"[BLOCKED] {year} only {len(d)} Mexico-born records")
    gate(not d.duplicated(["SERIALNO", "SPORDER"]).any(), f"[BLOCKED] {year} duplicate person keys")
    for c in ["AGEP", "SEX", "YOEP", "CIT", "PWGTP"] + REP:
        gate(bool(d[c].notna().all()), f"[BLOCKED] {year} Mexico-born records with missing {c}")
    gq = d["SERIALNO"].str.contains("GQ", regex=False).to_numpy()
    gq_rel = d[cfg["rel"]].isin(cfg["gq_rel"]).to_numpy()
    gate(bool((gq == gq_rel).all()), f"[BLOCKED] {year} GQ serial numbers disagree with {cfg['rel']} GQ codes")
    gate(bool(d["CIT"].isin([3, 4, 5]).all()), f"[BLOCKED] {year} Mexico-born record with CIT outside 3-5")
    audit["pums"][str(year)] = {"zip": str(zp.relative_to(ROOT)), "sha256": sha, "person_records": n_all,
                                "mexico_born_records": len(d), "members": members}
    schl = d["SCHL"].fillna(-1).astype(int).to_numpy()
    fschlp = d["FSCHLP"].fillna(-1).astype(int).to_numpy()
    W = d[["PWGTP"] + REP].to_numpy(dtype=float)
    return {"age": d["AGEP"].astype(int).to_numpy(), "sex": d["SEX"].astype(int).to_numpy(), "schl": schl,
            "fschlp": fschlp, "yoep": d["YOEP"].astype(int).to_numpy(), "cit": d["CIT"].astype(int).to_numpy(),
            "gq": gq, "W": W}


def slice_masks(age: np.ndarray, sex: np.ndarray) -> dict[str, np.ndarray]:
    masks = {"all": np.ones(len(age), dtype=bool)}
    for code, lab in SEX_LABELS.items():
        masks[f"sex:{lab}"] = sex == code
    for (lo, hi), a in zip(AGE_BANDS, AGE_LABELS):
        masks[f"age:{a}"] = (age >= lo) & (age <= hi)
    for code, lab in SEX_LABELS.items():
        for (lo, hi), a in zip(AGE_BANDS, AGE_LABELS):
            masks[f"sex:{lab}|age:{a}"] = (sex == code) & (age >= lo) & (age <= hi)
    return masks


def universe(mx: dict, year: int, lag: int | None = 5, recent: bool = False) -> np.ndarray:
    adult = (mx["age"] >= 20) & (mx["age"] <= 64)
    if recent:  # arrived inside the five-year window
        return adult & (mx["yoep"] >= year - 5) & (mx["yoep"] <= year)
    return adult & (mx["yoep"] <= year - lag)


def arrival_age(mx: dict, year: int) -> np.ndarray:
    """Age at the most recent arrival, from AGEP and YOEP (within about a year)."""
    return mx["age"] - (year - mx["yoep"])


def spec_arrays(mx: dict, year: int, sp: dict, break_years: float | None) -> tuple:
    m = universe(mx, year, sp["lag"])
    if sp["drop_allocated"]:
        m &= mx["fschlp"] == 0
    if sp["drop_gq"]:
        m &= ~mx["gq"]
    if sp["min_arrival_age"] is not None:
        m &= arrival_age(mx, year) >= sp["min_arrival_age"]
    schl = mx["schl"][m]
    gate(bool((schl >= 1).all()), f"[BLOCKED] {year} {sp['name']}: adult record without SCHL")
    Y = outcomes(schl, sp["coding"], break_years)
    W = mx["W"][m]
    if sp["k"] != 1.0:
        W = W * undercount_multiplier(mx["cit"][m], schl, sp["k"])[:, None]
    return m, Y, W


def stayer_estimates(mx: dict, m: np.ndarray, Y: np.ndarray, W: np.ndarray) -> dict:
    masks = slice_masks(mx["age"][m], mx["sex"][m])
    out = {}
    for s in SLICES:
        sm = masks[s]
        gate(bool(sm.any()), f"[BLOCKED] empty stayer slice {s}")
        out[s] = {"theta": estimate(Y[sm], W[sm]), "n": int(sm.sum()), "w": float(W[sm, 0].sum())}
    return out


def break_parameters(mexborn: dict) -> dict:
    """Sensitivity e for 2023: the share of no-schooling reports above the 2018 level (same universe),
    re-scored at the mean years of grades 1-9 reports (SCHL 4-12) in the 2023 universe."""
    share = {}
    for year in WAVES:
        mx = mexborn[year]
        m = universe(mx, year, 5)
        w = mx["W"][m, 0]
        share[year] = float(w[mx["schl"][m] == 1].sum() / w.sum())
    mx = mexborn[2023]
    m = universe(mx, 2023, 5)
    schl, w = mx["schl"][m], mx["W"][m, 0]
    g19 = (schl >= 4) & (schl <= 12)
    ybar = float((w[g19] * np.array([SCHL_YEARS[s] for s in schl[g19]])).sum() / w[g19].sum())
    excess = 1.0 - share[2018] / share[2023]
    gate(0.0 < excess < 1.0, f"[BLOCKED] no-schooling excess {excess} outside (0, 1)")
    return {"no_schooling_share_2018": share[2018], "no_schooling_share_2023": share[2023],
            "excess_fraction_2023": excess, "mean_years_grades_1_9_2023": ybar,
            "no_schooling_years_2023": excess * ybar}


def no_schooling_break_series() -> pd.DataFrame:
    """ACS reports of no schooling among Mexico-born 20-64 by survey year (IPUMS EDUCD), with the
    grade-8-or-less total, grade 9, and one fixed arrival cohort (entered 1990-1999)."""
    gate(IPUMS_MEXBORN.exists(), f"[BLOCKED] missing {IPUMS_MEXBORN}")
    sha = sha256_file(IPUMS_MEXBORN)
    gate(sha == IPUMS_MEXBORN_SHA, f"[BLOCKED] IPUMS extract sha256 {sha} != pinned")
    d = pd.read_parquet(IPUMS_MEXBORN, columns=["YEAR", "PERWT", "AGE", "YRIMMIG", "EDUCD"])
    d = d[(d["YEAR"] >= 2008) & d["AGE"].between(20, 64) & (d["EDUCD"] != 999)]
    rows = []
    for year, g in d.groupby("YEAR", sort=True):
        w = g["PERWT"].to_numpy(float)
        e = g["EDUCD"].to_numpy()
        c = g["YRIMMIG"].between(1990, 1999).to_numpy()
        rows.append({"acs_year": int(year), "n": len(g),
                     "no_schooling_share": w[e == 2].sum() / w.sum(),
                     "grade_8_or_less_share_incl_none": w[(e >= 2) & (e <= 26)].sum() / w.sum(),
                     "grade_9_share": w[e == 30].sum() / w.sum(),
                     "cohort_1990s_n": int(c.sum()),
                     "cohort_1990s_no_schooling_share": w[c & (e == 2)].sum() / w[c].sum()})
    return pd.DataFrame(rows)


def anchor_row(year: int, mx: dict) -> dict:
    fb = np.isin(mx["cit"], (4, 5))  # B05006 counts the foreign born; CIT 3 (born abroad of US parents) is native
    tot = mx["W"][fb].sum(axis=0)
    se = float(sdr_se(tot))
    gate(se > 0, f"[BLOCKED] {year} anchor total has a zero replicate SE")
    a = ANCHOR[year]
    gap = float(tot[0] - a["estimate"])
    rel = gap / a["estimate"]
    gate(abs(rel) <= ANCHOR_TOL, f"[BLOCKED] {year} PUMS Mexico-born {tot[0]:,.0f} vs B05006 {a['estimate']:,} "
                                 f"({rel:+.3%}) outside {ANCHOR_TOL:.1%}")
    note = ("within 0.2%" if abs(rel) <= ANCHOR_EXPLAIN else
            f"over 0.2%: the PUMS subsample's own replicate SE is {se:,.0f} ({se / tot[0]:.2%}), so the gap is "
            f"{gap / se:+.2f} PUMS SEs; PUMS weights are not controlled to place of birth")
    return {"year": year, "table": "B05006", "variable": a["variable"], "label": a["label"],
            "published_estimate": a["estimate"], "published_moe90": a["moe90"], "url": a["url"],
            "retrieved": ANCHOR_RETRIEVED, "pums_universe": "POBP 303 and CIT 4-5, all ages, PWGTP",
            "pums_estimate": int(round(tot[0])), "pums_se_replicate": round(se, 1), "gap": int(round(gap)),
            "gap_share": round(rel, 6), "gap_in_pums_se": round(gap / se, 4), "within_tolerance": True,
            "note": note}


def universe_profile(mx: dict, year: int) -> dict:
    m = universe(mx, year, 5)
    w = mx["W"][m, 0]
    schl, cit = mx["schl"][m], mx["cit"][m]

    def share(mask: np.ndarray) -> float:
        return round(float(w[mask].sum() / w.sum()), 6)

    arr = arrival_age(mx, year)[m]
    child, adult = arr < 15, arr >= ADULT_ARRIVAL_AGE
    tertiary = np.array([SCHL_BAND[s] == "tertiary" for s in schl])

    def tertiary_share(mask: np.ndarray) -> float:
        return round(float(w[mask & tertiary].sum() / w[mask].sum()), 6)

    return {"n": int(m.sum()), "weighted": int(round(w.sum())),
            "arrived_before_age_15_share": share(child), "tertiary_share_arrived_before_15": tertiary_share(child),
            "arrived_age_18_plus_share": share(adult), "tertiary_share_arrived_18_plus": tertiary_share(adult),
            "tertiary_share_schooling_allocated": tertiary_share(mx["fschlp"][m] == 1),
            "tertiary_share_schooling_reported": tertiary_share(mx["fschlp"][m] == 0),
            "gq_share_weighted": share(mx["gq"][m]), "gq_n": int(mx["gq"][m].sum()),
            "allocated_schooling_share_weighted": share(mx["fschlp"][m] == 1),
            "allocated_schooling_n": int((mx["fschlp"][m] == 1).sum()),
            "noncitizen_share": share(cit == 5), "born_abroad_us_parent_share": share(cit == 3),
            "men_share": share(mx["sex"][m] == 1),
            "schl_1_no_schooling_share": share(schl == 1), "schl_16_17_share": share(np.isin(schl, (16, 17))),
            "schl_17_ged_share": share(schl == 17), "schl_18_share": share(schl == 18),
            "schl_22_24_graduate_share": share(schl >= 22),
            "replicate_weights_negative": int((mx["W"][m, 1:] < 0).sum()),
            "replicate_weights_zero": int((mx["W"][m, 1:] == 0).sum())}


# ---------------------------------------------------------------- assembly
def stayer_row(year: int, spec_name: str, s: str, std: str, meas: str, n: int, w: float, est: float,
               se: float) -> dict:
    return {"wave": year, "spec": spec_name, "slice": s, "standardization": std, "measure": meas,
            "n_unweighted": n, "weighted_pop": int(round(w)), "estimate": est, "se": se}


def stayer_spec(year: int, mx: dict, sp: dict, break_years: float | None, ret: dict,
                stayer_rows: list, comp_rows: list, audit: dict) -> None:
    """Raw stayer figures for every returnee slice, the three standardized figures, and their
    comparisons with the returnees."""
    name = sp["name"]
    m, Y, W = spec_arrays(mx, year, sp, break_years)
    audit["spec_n"][f"{year} {name}"] = int(m.sum())
    est = stayer_estimates(mx, m, Y, W)
    measures = ["mean_years_schooling"] if name == "e_no_schooling_break" else MEASURES
    for s in SLICES:
        se = sdr_se(est[s]["theta"])
        for j, meas in enumerate(MEASURES):
            if meas in measures:
                stay = est[s]["theta"][j, 0]
                stayer_rows.append(stayer_row(year, name, s, "raw", meas, est[s]["n"], est[s]["w"], stay, se[j]))
                comp_rows.append(comparison(year, s, name, "raw", meas, ret[(year, s, meas)], stay, se[j],
                                            est[s]["n"]))
    for s, (label, cells) in STANDARDIZED.items():
        theta = standardize([est[c]["theta"] for c in cells], standardization_weights(ret, year, cells))
        se = sdr_se(theta)
        for j, meas in enumerate(MEASURES):
            if meas in measures:
                stayer_rows.append(stayer_row(year, name, s, label, meas, est[s]["n"], est[s]["w"], theta[j, 0], se[j]))
                comp_rows.append(comparison(year, s, name, label, meas, ret[(year, s, meas)], theta[j, 0], se[j],
                                            est[s]["n"]))


def short_stay(year: int, mx: dict, name: str, coding: str, linked: dict, coverage: dict,
               stayer_rows: list, comp_rows: list, audit: dict) -> None:
    """Returnees who left and came back inside the window (ENADID departure records linked to a
    household member, Mexico-born 20-64) against ACS Mexico-born 20-64 who arrived inside it.
    Raw, and with the ACS side reweighted to the men's share of all returned departures (all ages,
    the only sex split the ENADID file carries for this group)."""
    m = universe(mx, year, recent=True)
    audit["spec_n"][f"{year} {name}"] = int(m.sum())
    est = stayer_estimates(mx, m, outcomes(mx["schl"][m], coding), mx["W"][m])
    for s in ("all", "sex:men", "sex:women"):
        se = sdr_se(est[s]["theta"])
        for j, band in enumerate(BAND_ORDER):
            stayer_rows.append(stayer_row(year, name, s, "raw", band, est[s]["n"], est[s]["w"],
                                          est[s]["theta"][j, 0], se[j]))
    men = coverage[(year, "returned_share_men")]["estimate"]
    p = np.array([[men] * len(MEASURES), [1.0 - men] * len(MEASURES)])
    by_sex = standardize([est["sex:men"]["theta"], est["sex:women"]["theta"]], p)
    se_sex = sdr_se(by_sex)
    for j, band in enumerate(BAND_ORDER):
        stayer_rows.append(stayer_row(year, name, "all", "sex_returned_departures", band, est["all"]["n"],
                                      est["all"]["w"], by_sex[j, 0], se_sex[j]))
    se = sdr_se(est["all"]["theta"])
    n_linked = coverage[(year, "linked_20_64_coverage")]["n"]
    for j, band in enumerate(BAND_ORDER):
        r = {"estimate": linked[(year, band)]["estimate"], "se": linked[(year, band)]["se"], "n": n_linked}
        comp_rows.append(comparison(year, "all", name, "raw", band, r, est["all"]["theta"][j, 0], se[j],
                                    est["all"]["n"]))
        comp_rows.append(comparison(year, "all", name, "sex_returned_departures", band, r, by_sex[j, 0], se_sex[j],
                                    est["all"]["n"]))
    if name == SHORT_STAY_SPECS[0][0]:
        # Weighted recent arrivals of all ages, beside ENADID's household-reported departures.
        all_ages = (mx["yoep"] >= year - 5) & (mx["yoep"] <= year)
        audit["short_stay_context"][str(year)] = {
            "acs_recent_arrivals_all_ages_weighted": int(round(mx["W"][all_ages, 0].sum())),
            "acs_recent_arrivals_20_64_weighted": int(round(mx["W"][m, 0].sum())),
            "enadid_returned_departures_weighted": coverage[(year, "weighted_count")]["estimate"],
            "enadid_still_abroad_departures_weighted": coverage[(year, "still_abroad_weighted_count")]["estimate"],
            "enadid_returned_men_share_all_ages": men,
            "enadid_linked_20_64_n": n_linked,
            "enadid_linked_20_64_share_of_returned_rows": coverage[(year, "linked_20_64_coverage")]["estimate"]}


def stock_shift(comp: pd.DataFrame, audit: dict) -> dict:
    """What the window's returnees, had they stayed, would do to the stayer stock: with N_r
    returnees and N_s stayers, the stock's figure is higher after their exit by
    -gap * N_r / (N_s + N_r), where gap is the raw returnee-minus-stayer difference (main spec)."""
    out = {}
    for wave in WAVES:
        raw = comp[(comp["wave"] == wave) & (comp["spec"] == "main") & (comp["slice"] == "all")
                   & (comp["standardization"] == "raw")].set_index("measure")
        n_r = float(audit["enadid_returnees_weighted"][str(wave)])
        n_s = float(audit["universe_main"][str(wave)]["weighted"])
        out[str(wave)] = {"returnees_weighted": n_r, "stayers_weighted": n_s,
                          "returnees_per_stayer": round(n_r / n_s, 6),
                          **{f"shift_{meas}": round(float(-raw.loc[meas, "difference"] * n_r / (n_s + n_r)), 6)
                             for meas in ("tertiary", "mean_years_schooling")}}
    return out


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    check_schooling_maps()
    audit: dict = {"pums": {}, "inputs": {}, "universe_main": {}, "spec_n": {}, "enadid_gates": [],
                   "anchor": {}, "break_2023": {}}
    for p in (ENADID_RESULT, ENADID_RETURNEES, ENADID_DEPARTURES):
        gate(p.exists(), f"[BLOCKED] missing {p}")
        audit["inputs"][str(p.relative_to(ROOT))] = sha256_file(p)

    # Returnee side first: nothing on the ACS side is computed until these gates pass.
    ret, linked, coverage = load_returnees()
    exp = parse_enadid_result(ENADID_RESULT.read_text(encoding="utf-8"))
    audit["enadid_gates"] = gate_returnees(ret, linked, coverage, exp)
    audit["enadid_returnees_weighted"] = {str(w): ret[(w, "all", "tertiary")]["w"] for w in WAVES}

    mexborn = {year: read_mexico_born(year, audit) for year in WAVES}
    anchors = [anchor_row(year, mexborn[year]) for year in WAVES]  # build gate before any result
    for a in anchors:
        audit["anchor"][str(a["year"])] = {k: a[k] for k in ("pums_estimate", "published_estimate", "gap_share",
                                                             "gap_in_pums_se")}
    brk = break_parameters(mexborn)
    audit["break_2023"] = {k: round(v, 6) for k, v in brk.items()}
    series = no_schooling_break_series()
    audit["inputs"][str(IPUMS_MEXBORN.relative_to(ROOT))] = IPUMS_MEXBORN_SHA

    stayer_rows, comp_rows = [], []
    audit["short_stay_context"] = {}
    for year in WAVES:
        mx = mexborn[year]
        audit["universe_main"][str(year)] = universe_profile(mx, year)
        for sp in SPECS:
            if sp["name"] == "e_no_schooling_break" and year != 2023:
                continue
            break_years = brk["no_schooling_years_2023"] if year == 2023 else None
            stayer_spec(year, mx, sp, break_years, ret, stayer_rows, comp_rows, audit)
        for name, coding in SHORT_STAY_SPECS:
            short_stay(year, mx, name, coding, linked, coverage, stayer_rows, comp_rows, audit)

    stayers = pd.DataFrame(stayer_rows)
    comp = pd.DataFrame(comp_rows)
    audit["stock_shift"] = stock_shift(comp, audit)
    write_csv(stayers, DERIVED / "stayers_by_schooling.csv")
    write_csv(comp, DERIVED / "comparison.csv")
    write_csv(pd.DataFrame(anchors), DERIVED / "anchor.csv")
    write_csv(series, DERIVED / "acs_no_schooling_break.csv")
    with open(DERIVED / "audit.json", "w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print_summary(comp, anchors, brk)


def comparison(wave: int, s: str, spec: str, std: str, meas: str, r: dict, stay: float, se_stay: float,
               n_stay: int) -> dict:
    return {"wave": wave, "slice": s, "spec": spec, "standardization": std, "measure": meas,
            "returnee": r["estimate"], "se_returnee": r["se"], "stayer": stay, "se_stayer": se_stay,
            "difference": r["estimate"] - stay, "se": float(np.hypot(r["se"], se_stay)),
            "n_returnee": r["n"], "n_stayer": n_stay}


def write_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, float_format="%.6f", lineterminator="\n")


def print_summary(comp: pd.DataFrame, anchors: list[dict], brk: dict) -> None:
    for a in anchors:
        print(f"anchor {a['year']}: PUMS {a['pums_estimate']:,} vs B05006 {a['published_estimate']:,} "
              f"({a['gap_share']:+.3%}, {a['gap_in_pums_se']:+.2f} PUMS SE)")
    print(f"2023 no-schooling break: share {brk['no_schooling_share_2018']:.4f} -> {brk['no_schooling_share_2023']:.4f}, "
          f"excess {brk['excess_fraction_2023']:.3f}, re-scored at {brk['no_schooling_years_2023']:.3f} years")
    key = comp[(comp["measure"].isin(["tertiary", "mean_years_schooling"]))
               & (((comp["slice"].isin(["sex:men", "sex:women"])) & (comp["standardization"] == "age_within_sex"))
                  | ((comp["slice"] == "all") & (comp["standardization"] == "sex_age")))]
    for (wave, s, meas), g in key.groupby(["wave", "slice", "measure"], sort=True):
        main = g[g["spec"] == "main"].iloc[0]
        signs = {np.sign(v) for v in g["difference"]}
        print(f"{wave} {s:9s} {meas:21s} main {main['difference']:+.4f} ({main['se']:.4f}); "
              f"range {g['difference'].min():+.4f}..{g['difference'].max():+.4f}; "
              f"sign {'holds' if len(signs) == 1 else 'FLIPS'} across {len(g)} specs")


if __name__ == "__main__":
    main()

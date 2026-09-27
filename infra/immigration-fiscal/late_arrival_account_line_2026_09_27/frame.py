"""The account's CPS ASEC 2025 frame, the three generation masks and the two assignment conventions.

Frame: the pinned public-use zip the complete account reads (sha256 318845a2...), person records with
household fields and all 161 weights, sorted by SPM unit as analyze_cps_fiscal_2025.prepare sorts them.
The key vectors are the complete account's own definitions as the CPS imputation lane copied and gated
them (cps_imputation_keys_2026_09_23/common.py; its gate.py matches 70 key shares to 1e-14), imported
read-only.

Generations inside the canonical union (full_account_spending_2026_09_20/builder.py canonical_target,
generation_split_2026_09_20/analyze_cps.py population_masks):
  G1      foreign-born (PRCITSHP 4, 5) and born in Mexico (PENATVTY 303);
  G2      native (PRCITSHP 1-3) with a Mexico-born mother or father (PEMNTVTY or PEFNTVTY 303);
  G3plus  native, both parents born in US areas, Mexican origin (PRDTHSP 1).
All three are restricted to the civilian household universe (PRPERTYP 2 or age under 15).

Conventions for whose account a person sits in:
  (a) everyone in their own generation;
  (b) minors (under 18) in their parents' generation, the National Academies' 2017 grouping (pp. 387-388):
      a co-resident parent's generation; parents in two generations split half and half (the expectation
      of the report's random halves, footnote 13); no co-resident parent: the oldest co-resident adult
      relative in the union; a minor whose co-resident parents are all outside the union, or who has no
      union relative in the household, stays in their own generation, so the union's total is unchanged.

Late-arrival lane (late_arrival_account_line_2026_09_27): a copy of generation_account_2026_09_24/frame.py
at 0f22f0c with the mask changed. G1 is split into seven cells by approximate age at arrival and current age
(CPS PEINUSYR, grouped year of entry, and A_AGE); G2 and G3plus are unchanged. The G1 cells add to the
generation lane's G1 person for person. LATE_DEF (environment: central | lower | upper) picks the
age-at-arrival reading: central, the interval midpoint; lower, the earliest arrival and latest birth
(arrived-at-50+ only if certain); upper, the latest arrival and earliest birth (possible). Outputs of the
copied steps go to _cache/split_<LATE_DEF>/.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import hashlib
import os
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
CACHE = HERE / "_cache"
LATE_DEF = os.environ.get("LATE_DEF", "central")
if LATE_DEF not in ("central", "lower", "upper"):
    raise SystemExit(f"[BLOCKED] LATE_DEF must be central, lower or upper, not {LATE_DEF}")
OUT = CACHE / f"split_{LATE_DEF}"
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
REPS = [f"pwwgt{i}" for i in range(161)]
TARGET_POP = 40896574.15235156
RESIDENT = 340_110_988.0
# G1 cells: Y = arrived before 50, L50 = arrived at 50-54, L55 = arrived at 55+; then current age.
G1_CELLS = ["G1_Y_u50", "G1_Y_50_64", "G1_Y_65p", "G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"]
GENS = G1_CELLS + ["G2", "G3plus"]
TOP = {**{g: "G1" for g in G1_CELLS}, "G2": "G2", "G3plus": "G3plus"}
IS_G1 = [TOP[g] == "G1" for g in GENS]
# PEINUSYR (ASEC 2025 dictionary; indian_civic_cps_2026_09_18/_cache/asec_2025_PEINUSYR.json): code -> first
# and last calendar year of entry. Code 1 is "Before 1950"; code 28 is "2022-2025" and ends at the survey.
ENTRY = {1: (1900, 1949), 2: (1950, 1959), 3: (1960, 1964), 4: (1965, 1969), 5: (1970, 1974), 6: (1975, 1979),
         **{7 + k: (1980 + 2 * k, 1981 + 2 * k) for k in range(21)}, 28: (2022, 2025)}
SURVEY = 2025.2  # ASEC interviews, February-April 2025
# A_AGE top codes (ASEC public use): 80 = 80-84, 85 = 85+. (central, lowest, highest) true age.
TOP_AGE = {80: (82.0, 80.0, 84.99), 85: (88.0, 85.0, 99.0)}
US_AREAS = [57, 60, 66, 69, 73, 78]
MEXICO = 303

sys.path.insert(0, str(FISCAL / "cps_imputation_keys_2026_09_23"))
import common as C  # noqa: E402  read-only: the account's key vectors, gated by that lane's gate.py

EXTRA = ["PEINUSYR", "A_LINENO", "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP", "PXPAR1", "PXPAR2", "PXPAR1TYP",
         "PXPAR2TYP", "A_SPOUSE", "A_FAMREL", "A_FAMTYP", "A_PFREL", "NOCOV_CYR", "COV", "MRKS", "MRK",
         "I_MRKS", "CTC_CRD", "A_ENRLW", "A_FTPT", "A_HSCOL", "PEIOOCC", "PEIOIND", "A_DTOCC", "A_DTIND",
         "PEAFEVER", "VET_YN", "PERLIS", "PECOHAB", "MIL", "CHAMPVA"]
HH_EXTRA = ["HPUBLIC", "HLORENT", "GTCBSA"]


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def load(refresh=False):
    """Person frame, household fields and 161 weights; cached in this lane's ignored _cache."""
    cache = CACHE / "asec25_generation.parquet"
    if cache.exists() and not refresh:
        return pd.read_parquet(cache)
    if sha(CPS_ZIP) != CPS_SHA:
        raise ValueError("[BLOCKED] unreviewed CPS source")
    person = list(dict.fromkeys(C.ID + C.DEMO + C.VALUES + C.INCOME_FLAGS + C.OTHER_FLAGS + EXTRA))
    household = list(dict.fromkeys(C.HOUSEHOLD + HH_EXTRA))
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=person)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=household)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", *REPS])
    w = w.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if d[REPS].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    if (d.MARSUPWT / 100 - d.pwwgt0).abs().max() >= .01:
        raise ValueError("Full-weight merge validation failed")
    d = d.merge(hh, left_on="PH_SEQ", right_on="H_SEQ", how="left", validate="many_to_one")
    if d.H_SEQ.isna().any():
        raise ValueError("Person without household record")
    d = d.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    d.to_parquet(cache, index=False)
    return d


def arrival_age(d, reading=None):
    """Approximate age at arrival for every row (NaN where PEINUSYR is NIU): age now less the years since
    arrival. central: arrival at the interval's midpoint (entry year e_lo..e_hi, uniform over the calendar
    years, the last interval ending at the survey), birth half a year before the age's anniversary. lower:
    earliest arrival and latest birth. upper: latest arrival and earliest birth. Top-coded ages take the
    reading's end of the top-code interval."""
    reading = reading or LATE_DEF
    code = d.PEINUSYR.to_numpy()
    age = d.A_AGE.to_numpy().astype(float)
    k = {"central": 0, "lower": 1, "upper": 2}[reading]
    for coded, triple in TOP_AGE.items():
        age = np.where(d.A_AGE.to_numpy() == coded, triple[k], age)
    lo = np.array([ENTRY.get(int(c), (np.nan, np.nan))[0] for c in code], float)
    hi = np.array([min(ENTRY.get(int(c), (np.nan, np.nan))[1] + 1.0, SURVEY) for c in code], float)
    if reading == "central":
        out = age - (SURVEY - 0.5 - (lo + hi) / 2)
    elif reading == "lower":
        out = age - (SURVEY - lo)
    else:
        out = age - (SURVEY - 1.0 - hi)
    return np.clip(out, 0.0, age)


def g1_cells(d, g1, reading=None):
    """The seven G1 cells (disjoint, exhaustive inside g1)."""
    alpha = arrival_age(d, reading)
    age = d.A_AGE.to_numpy()
    if np.isnan(alpha[g1]).any():
        raise ValueError("Mexico-born person without a year of entry")
    y, l50, l55 = alpha < 50, (alpha >= 50) & (alpha < 55), alpha >= 55
    cells = {"G1_Y_u50": y & (age < 50), "G1_Y_50_64": y & (age >= 50) & (age < 65), "G1_Y_65p": y & (age >= 65),
             "G1_L50_50_64": l50 & (age < 65), "G1_L50_65p": l50 & (age >= 65),
             "G1_L55_55_64": l55 & (age < 65), "G1_L55_65p": l55 & (age >= 65)}
    return {k: v & g1 for k, v in cells.items()}


def g1_class(d, reading=None):
    """Arrival class per row under the reading: "Y" (< 50), "L50" (50-54), "L55" (55+); "" where no entry year."""
    alpha = arrival_age(d, reading)
    return np.where(np.isnan(alpha), "", np.where(alpha < 50, "Y", np.where(alpha < 55, "L50", "L55")))


def g1(gens):
    """The generation lane's G1 mask: the union of the G1 cells."""
    return np.logical_or.reduce([gens[g] for g in G1_CELLS])


def g1_vector(weights):
    """A G1 amount split over GENS by non-negative per-cell weights (dict over G1_CELLS); zero elsewhere."""
    total = sum(weights[g] for g in G1_CELLS)
    if total <= 0:
        raise ValueError("no weight inside G1")
    return np.array([weights[g] / total if g in G1_CELLS else 0.0 for g in GENS])


def masks(d):
    """Civilian universe, union and the generation cells (disjoint, exhaustive inside the union)."""
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    g1 = d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(MEXICO).to_numpy()
    g2 = native & (d.PEMNTVTY.eq(MEXICO) | d.PEFNTVTY.eq(MEXICO)).to_numpy()
    g3 = native & (d.PEMNTVTY.isin(US_AREAS) & d.PEFNTVTY.isin(US_AREAS) & d.PRDTHSP.eq(1)).to_numpy()
    gens = {**g1_cells(d, g1 & civilian), "G2": g2 & civilian, "G3plus": g3 & civilian}
    if not np.array_equal(np.logical_or.reduce([gens[g] for g in G1_CELLS]), g1 & civilian):
        raise ValueError("G1 cells do not partition G1")
    union = np.logical_or.reduce([gens[g] for g in GENS])
    if (sum(m.astype(int) for m in gens.values()) > 1).any():
        raise ValueError("Generations overlap")
    _, canonical = C.masks(d)
    if not np.array_equal(union, canonical):
        raise ValueError("Generation union differs from the account's canonical target")
    return civilian, union, gens


def label(gens, n):
    out = np.full(n, -1, dtype=int)
    for j, g in enumerate(GENS):
        out[gens[g]] = j
    return out


def parent_rows(d):
    """Row index of each co-resident parent slot (-1 if none), linked by household and line number."""
    keys = pd.MultiIndex.from_frame(d[["PH_SEQ", "A_LINENO"]])
    if not keys.is_unique:
        raise ValueError("Duplicate person linkage key")
    lookup = pd.Series(np.arange(len(d)), index=keys)
    rows = []
    for slot in (1, 2):
        line = d[f"PEPAR{slot}"].to_numpy()
        query = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), line])
        row = lookup.reindex(query).fillna(-1).to_numpy(dtype=int)
        if np.any((line > 0) & (row < 0)):
            raise ValueError("Parent line number without a person record")
        rows.append(np.where(line > 0, row, -1))
    return np.column_stack(rows)


def assignments(d, civilian, union, gens):
    """Generation weights per person, n x len(GENS), for conventions (a) and (b); rows sum to 1 on the union."""
    n = len(d)
    lab = label(gens, n)
    own = np.zeros((n, len(GENS)))
    own[union, lab[union]] = 1.0
    parents = parent_rows(d)
    age = d.A_AGE.to_numpy()
    b = own.copy()
    rule = np.full(n, "adult_or_outside", dtype=object)
    minors = np.flatnonzero(union & (age < 18))
    family = pd.MultiIndex.from_frame(d[["PH_SEQ", "PF_SEQ"]]).factorize()[0]
    # Oldest union adult in each family, the NAS fallback when no parent is in the household.
    adult_union = union & (age >= 18)
    oldest = pd.DataFrame({"family": family[adult_union], "age": age[adult_union],
                           "row": np.flatnonzero(adult_union)}).sort_values(["family", "age", "row"],
                                                                            ascending=[True, False, True])
    oldest = oldest.drop_duplicates("family").set_index("family").row
    for i in minors:
        slots = [p for p in parents[i] if p >= 0]
        in_union = [p for p in slots if union[p]]
        if in_union:
            b[i] = 0
            for p in in_union:
                b[i, lab[p]] += 1 / len(in_union)
            rule[i] = "parents_two_generations" if len({lab[p] for p in in_union}) > 1 else "parent_in_union"
        elif slots:
            rule[i] = "parents_outside_union_own"
        elif family[i] in oldest.index and oldest[family[i]] != i:
            b[i] = 0
            b[i, lab[oldest[family[i]]]] = 1.0
            rule[i] = "oldest_union_relative"
        else:
            rule[i] = "no_union_relative_own"
    for name, omega in [("a", own), ("b", b)]:
        if not np.allclose(omega[union].sum(axis=1), 1) or omega[~union].any():
            raise ValueError(f"Convention {name} does not partition the union")
    return {"a": own, "b": b}, rule, parents


def totals(vector, weights, omega):
    """Generation totals of a per-person vector: sum_i v_i w_i omega_ig (weights n or n x 161)."""
    v = np.asarray(vector, float)
    if weights.ndim == 1:
        return (v * weights) @ omega
    return np.einsum("i,ir,ig->gr", v, weights, omega)

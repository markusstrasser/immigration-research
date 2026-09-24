"""CPS ASEC 2025 frame, the complete account's allocation keys, and CBO-style income groups.

Read-only consumer of the pinned CPS ASEC 2025 public-use zip the complete account uses. Key
vectors copy full_account_receipts_2026_09_20/builder.py::derive_keys and
full_account_spending_2026_09_20/builder.py::build_keys. The MEPS payer means come from the
account's own build/meps_health_transport_2024.py, imported read-only. test_benchmarks.py
reproduces the published target shares from these vectors before any new computation uses them.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
CACHE = HERE / "_cache"
OUT = HERE / "derived"
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
MEPS_ZIP = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
REPS = [f"pwwgt{i}" for i in range(161)]
TARGET_POP = 40896574.15235156
RESIDENT = 340_110_988.0
OASDI_MAX = 168600  # 2024 taxable maximum, as in the receipts builder

PERSON = ["PH_SEQ", "PPPOS", "P_SEQ", "SPM_ID", "TAX_ID", "PERRP", "MARSUPWT", "A_AGE", "A_SEX",
          "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTHSP", "PRDTRACE",
          "PEINUSYR", "A_HGA", "A_MARITL", "FILESTAT", "DEP_STAT", "PEMLR", "A_CLSWKR",
          "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "INT_VAL", "DIV_VAL", "RNT_VAL", "CAP_VAL", "SS_VAL",
          "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL", "WC_VAL", "PTOTVAL", "FEDTAX_BC", "FEDTAX_AC",
          "STATETAX_A", "STATETAX_B", "FICA", "AGI", "EIT_CRED", "ACTC_CRD", "CTC_CRD", "MCARE", "MCAID",
          "PUB", "PRIV", "MIL", "CHAMPVA", "MRKS", "MRK", "SPM_RESOURCES", "SPM_SNAPSUB", "SPM_ENGVAL",
          "SPM_WICVAL", "SPM_CAPHOUSESUB", "SPM_SCHLUNCH", "SPM_NUMPER",
          # status_impute_2026_09_16/impute_status.py::impute fields
          "A_LINENO", "A_SPOUSE", "VET_YN", "PEAFEVER", "PEIOOCC", "SE_VAL",
          # uncompensated_care_2026_09_23 exposure (hospital arm)
          "NOCOV_CYR"]
HOUSEHOLD = ["H_SEQ", "GESTFIPS", "H_NUMPER", "HPUBLIC", "HLORENT"]


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def sdr(values):
    """160-replicate successive-difference SE, as the account's generator."""
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def load(refresh=False):
    """Person frame with household fields and all 161 weights, in file order."""
    cache = CACHE / "cps25_frame.parquet"
    if cache.exists() and not refresh:
        d = pd.read_parquet(cache)
        if set(PERSON + HOUSEHOLD + REPS) <= set(d.columns):
            return d
    if sha(CPS_ZIP) != CPS_SHA:
        raise ValueError("Unreviewed CPS source")
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=HOUSEHOLD)
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
    if len(d) < 140000 or d.pwwgt0.sum() < 3.3e8:
        raise ValueError("Truncated CPS person file")
    CACHE.mkdir(parents=True, exist_ok=True)
    d.to_parquet(cache, index=False)
    return d


def weights(d):
    return d[REPS].to_numpy(float)


def masks(d):
    """Canonical civilian universe and the 40.9m union (spending builder::canonical_target)."""
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3])
    us = [57, 60, 66, 69, 73, 78]
    union = ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) |
             (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303))) |
             (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)))
    return civilian, (union & civilian).to_numpy()


def unit_equal(values, ids):
    """Equal split of each SPM unit's total across all members (the shared convention)."""
    codes = pd.factorize(ids)[0]
    values = np.asarray(values, float)
    total = np.bincount(codes, weights=values)
    size = np.bincount(codes).astype(float)
    return (total / size)[codes]


def receipt_vectors(d):
    """full_account_receipts_2026_09_20/builder.py::derive_keys, personal convention."""
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    se = .9235 * np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    se = np.where(se >= 400, se, 0)
    se_capped = np.minimum(se, np.maximum(OASDI_MAX - np.minimum(wage, OASDI_MAX), 0))
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    medicare = d.MCARE.eq(1).to_numpy(float)
    return dict(
        population=np.ones(len(d)), adults=d.A_AGE.ge(18).to_numpy(float), wage=wage,
        wage_oasdi=np.minimum(wage, OASDI_MAX), self_payroll=.124 * se_capped + .029 * se,
        positive_fica_worker=d.FICA.gt(0).to_numpy(float),
        capital=(d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(float),
        interest_dividend=(d.INT_VAL + d.DIV_VAL).clip(lower=0).to_numpy(float),
        federal_liability=d.FEDTAX_BC.to_numpy(float),
        federal_high_agi=(d.FEDTAX_BC * d.AGI.ge(500000)).to_numpy(float),
        state_liability=d.STATETAX_A.clip(lower=0).to_numpy(float),
        consumption=d.SPM_RESOURCES.clip(lower=0).to_numpy(float) / size,
        medicare=medicare, medicare_income=medicare * (d.AGI.clip(lower=0).to_numpy(float) + 1))


def receipt_keys(d):
    personal = receipt_vectors(d)
    ids = d.SPM_ID.to_numpy()
    return {"personal": personal, "shared": {k: unit_equal(v, ids) for k, v in personal.items()}}


def meps_means(d):
    """Account's MEPS payer means by age band x US/not-US birth, applied to the whole cell."""
    sys.path.insert(0, str(FISCAL / "build"))
    from meps_health_transport_2024 import read_meps, donor_model
    md, _ = read_meps(MEPS_ZIP, MEPS_ZIP.with_name("h256su.txt"))
    cells, codes, _ = donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid]
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    out = {}
    for name, cols in [("medicare", ["TOTMCR24"]), ("medicaid", ["TOTMCD24"]), ("va_medical", ["TOTVA24"]),
                       ("tricare", ["TOTTRI24"]), ("health_other", ["TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"])]:
        sums = sample.assign(wx=sample[cols].sum(axis=1) * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        mean = (sums / pop).reindex(index)
        if mean.isna().any():
            raise ValueError("Unmatched payer cell")
        out[name] = mean.to_numpy()[codes] * exposure
    return out


def spending_keys(d, meps=None):
    """full_account_spending_2026_09_20/builder.py::build_keys, per allocation convention."""
    ids = d.SPM_ID.to_numpy()
    counts = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    dollars = {k: d[v].to_numpy(float) for k, v in [("social_security", "SS_VAL"), ("ssi", "SSI_VAL"),
               ("cash_assistance", "PAW_VAL"), ("unemployment", "UC_VAL"), ("veterans", "VET_VAL"),
               ("workers_comp", "WC_VAL"), ("wages", "WSAL_VAL")]}
    dollars["refundable_credits"] = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
    dollars["all_cash"] = sum(dollars[k] for k in ["social_security", "ssi", "cash_assistance",
                                                   "unemployment", "veterans"])
    units = {k: d[v].to_numpy(float) / counts for k, v in [("snap", "SPM_SNAPSUB"), ("energy", "SPM_ENGVAL"),
                                                           ("wic", "SPM_WICVAL"), ("housing_support", "SPM_CAPHOUSESUB")]}
    units["resources"] = np.maximum(d.SPM_RESOURCES.to_numpy(float) / counts, 0)
    ages = {"population": np.ones(len(d)), "age65plus": d.A_AGE.ge(65).to_numpy(float),
            "working_age": d.A_AGE.between(18, 64).to_numpy(float), "adults": d.A_AGE.ge(18).to_numpy(float),
            "age5_24": d.A_AGE.between(5, 24).to_numpy(float), "age18_24": d.A_AGE.between(18, 24).to_numpy(float),
            "medicaid_covered": d.MCAID.eq(1).to_numpy(float)}
    meps = meps_means(d) if meps is None else meps
    out = {}
    for allocation in ["personal", "shared"]:
        vec = {k: (v if allocation == "personal" else unit_equal(v, ids)) for k, v in dollars.items()}
        vec.update(units)
        vec.update(ages)
        vec.update(meps)
        out[allocation] = vec
    return out


def model():
    return json.loads(MODEL.read_text())


def status(d):
    """Imputed legal status from the repo's Borjas-residual rules (status_impute_2026_09_16,
    imported read-only; the same call dataset_integrity_2026_09_23/cps_status_keys.py makes).
    Returns the imputed unauthorized and the Latin-American-born mask the audit's rules use."""
    sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
    from impute_status import impute
    hh = d[["H_SEQ", "HPUBLIC", "HLORENT"]].drop_duplicates("H_SEQ")
    st = impute(d, hh)
    latin = d.PENATVTY.between(302, 399).to_numpy() & ~d.PENATVTY.eq(327).to_numpy()
    return np.asarray(st["unauthorized"], bool), latin


def household_fraction(d, civ):
    """Spending builder's pool fraction: CPS civilians over the July 2024 resident count."""
    return float(d.pwwgt0.to_numpy()[civ].sum() / RESIDENT)


# --------------------------------------------------------------------------------------------
# CBO-style income groups. CBO ranks households by income before transfers and taxes (market
# income plus Social Security, Medicare, UI and workers' compensation) divided by the square root
# of household size; quintiles hold equal numbers of people; households with negative income are
# excluded from the lowest group and kept in totals (CBO 61911 researcher README).
# --------------------------------------------------------------------------------------------
GROUPS = ["q1", "q2", "q3", "q4", "p81_90", "p91_95", "p96_99", "top1", "negative"]
EDGES = [0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99]


def cbo_income(d, medicare_per_enrollee, employer_payroll=True, capital_gains=True):
    """Person-level contribution to household income before transfers and taxes (CPS proxy).

    Money income (PTOTVAL) less SSI and public assistance, which CBO counts as means-tested
    transfers, plus the employer's OASDI and HI tax, CPS capital gains (CAP_VAL) and Medicare at an
    average cost per enrollee. Employer health-insurance contributions are not on the public file.
    """
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    x = d.PTOTVAL.to_numpy(float) - d.SSI_VAL.to_numpy(float) - d.PAW_VAL.to_numpy(float)
    if employer_payroll:
        x = x + .062 * np.minimum(wage, OASDI_MAX) + .0145 * wage
    if capital_gains:
        x = x + d.CAP_VAL.to_numpy(float)
    return x + medicare_per_enrollee * d.MCARE.eq(1).to_numpy(float)


def cbo_groups(d, person_income, weight=None):
    """Assign every person the group of their household, ranked by size-adjusted income."""
    weight = d.pwwgt0.to_numpy(float) if weight is None else weight
    hh = pd.factorize(d.PH_SEQ)[0]
    income = np.bincount(hh, weights=person_income)
    size = np.bincount(hh).astype(float)
    adjusted = (income / np.sqrt(size))[hh]
    order = np.argsort(adjusted, kind="mergesort")
    cum = np.empty(len(d))
    cum[order] = np.cumsum(weight[order]) / weight.sum()
    # A person's position is the population share at or below their household's income; ties
    # share a household, so every member lands in one group.
    position = pd.Series(cum).groupby(hh).transform("min").to_numpy()
    labels = np.array(GROUPS[:-1])[np.searchsorted(EDGES, position, side="left")]
    negative = income[hh] < 0
    return np.where(negative, "negative", labels), adjusted


def group_totals(vector, weight, mask, groups):
    """Weighted totals of a key by group over a person mask (weight may be n x 161)."""
    out = {}
    for g in GROUPS:
        m = mask & (groups == g)
        out[g] = vector[m] @ weight[m]
    return out

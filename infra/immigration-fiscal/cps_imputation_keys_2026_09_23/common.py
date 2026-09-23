"""Shared loaders and definitions for the CPS ASEC imputation-keys lane.

Read-only consumer of the pinned CPS ASEC 2025 public-use zip that the complete
account uses. Key vectors copy the definitions in
full_account_receipts_2026_09_20/builder.py::derive_keys and
full_account_spending_2026_09_20/builder.py::build_keys (not imported, so no
upstream code is executed or edited). Microdata stay in _cache/.
"""
from __future__ import annotations

import hashlib
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
REPS = [f"pwwgt{i}" for i in range(161)]
TARGET_POP = 40896574.15235156
RESIDENT = 340_110_988.0

ID = ["PH_SEQ", "PPPOS", "P_SEQ", "PF_SEQ", "SPM_ID", "SPM_HEAD", "SPM_NUMPER", "TAX_ID", "PERRP",
      "A_EXPRRP", "MARSUPWT", "FL_665"]
DEMO = ["A_AGE", "A_SEX", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON",
        "PRDTRACE", "PRDTHSP", "PEINUSYR", "A_HGA", "A_MARITL", "PEMLR", "A_CLSWKR", "A_MJOCC",
        "LJCW", "WKSWORK", "HRSWK", "PXNATVTY", "PXMNTVTY", "PXFNTVTY", "PXHSPNON", "PRCITFLG",
        "PXINUSYR", "PXRACE1"]
VALUES = ["WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "ERN_VAL", "ERN_SRCE", "ERN_YN", "WS_VAL", "SE_VAL",
          "FRM_VAL", "INT_VAL", "DIV_VAL", "RNT_VAL", "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL",
          "VET_VAL", "WC_VAL", "PTOTVAL", "PEARNVAL", "FEDTAX_BC", "FEDTAX_AC", "STATETAX_A",
          "FICA", "AGI", "EIT_CRED", "ACTC_CRD", "FILESTAT", "MCARE", "MCAID", "PUB", "PRIV", "MIL",
          "CHAMPVA", "WICYN", "SPM_RESOURCES", "SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL",
          "SPM_CAPHOUSESUB", "SPM_SCHLUNCH", "MARG_TAX", "ANN_VAL", "CAP_VAL", "CSP_VAL", "DIS_VAL1",
          "DIS_VAL2", "DST_VAL1", "DST_VAL2", "ED_VAL", "FIN_VAL", "OI_VAL", "PEN_VAL1", "PEN_VAL2",
          "SUR_VAL1", "SUR_VAL2", "SPM_FEDTAX", "SPM_STTAX", "SPM_FICA", "SPM_EITC", "SPM_ACTC",
          "SPM_TOTVAL", "WORKYN", "SS_YN", "SSI_YN", "PAW_YN", "UC_YN", "VET_YN", "WC_YN", "INT_YN",
          "DIV_YN", "RNT_YN"]
# Person income allocation flags (data dictionary, Person record, SubTopic Allocation Flags).
INCOME_FLAGS = ["I_WORKYN", "I_WTEMP", "I_ERNYN", "I_ERNSRC", "I_ERNVAL", "I_WSYN", "I_WSVAL",
                "I_SEYN", "I_SEVAL", "I_FRMYN", "I_FRMVAL", "I_INTYN", "I_INTVAL", "I_DIVYN",
                "I_DIVVAL", "I_RNTYN", "I_RNTVAL", "I_SSYN", "I_SSVAL", "I_SSIYN", "I_SSIVAL",
                "I_PAWYN", "I_PAWVAL", "I_PAWTYP", "I_PAWMO", "I_UCYN", "I_UCVAL", "I_VETYN",
                "I_VETVAL", "I_VETTYP", "I_VETQVA", "I_WCYN", "I_WCVAL", "I_WCTYP", "I_ANNYN",
                "I_ANNVAL", "I_CAPYN", "I_CAPVAL", "I_CHSPYN", "I_CHSPVAL", "I_CSPYN", "I_CSPVAL",
                "I_DISYN", "I_DISVL1", "I_DISVL2", "I_DISCS", "I_DISHP", "I_DISSC1", "I_DISSC2",
                "I_DSTYNCOMP", "I_DSTVAL1COMP", "I_DSTVAL2COMP", "I_DSTSC", "I_DSTSCCOMP", "I_EDYN",
                "I_EDTYP", "I_OEDVAL", "I_FINYN", "I_FINVAL", "I_OIVAL", "I_PENYN", "I_PENVAL1",
                "I_PENVAL2", "I_PENINC", "I_PENPLA", "I_PENSC1", "I_PENSC2", "I_RETCBYN",
                "I_RETCBVAL", "I_RINTYN", "I_RINTVAL1", "I_RINTVAL2", "I_RINTSC", "I_SURYN",
                "I_SURVL1", "I_SURVL2", "I_SURSC1", "I_SURSC2"]
OTHER_FLAGS = ["I_MCARE", "I_MCAID", "WICYNA", "I_MOOP", "I_MOOP2", "I_WKSWK", "I_HRSWK", "I_LJCW"]
HOUSEHOLD = ["H_SEQ", "GESTFIPS", "GEREG", "H_TENURE", "HPROP_VAL", "I_PROPVAL", "HFOODSP", "HFDVAL",
             "I_HFOODS", "I_HFDVAL", "I_HFOODM", "I_HFOODN", "HPUBLIC", "HLORENT", "I_HPUBLI",
             "I_HLOREN", "HFLUNCH", "I_HFLUNC", "I_HFLUNN", "HENGAST", "HENGVAL", "I_HENGAS",
             "I_HENGVA", "I_CHCAREVAL"]


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def sdr(values):
    """160-replicate successive-difference SE, as the account's generator."""
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def load_frame(refresh=False):
    """Person frame with household fields and all 161 weights, sorted as base.prepare."""
    cache = CACHE / "asec25_lane.parquet"
    if cache.exists() and not refresh:
        return pd.read_parquet(cache)
    if sha(CPS_ZIP) != CPS_SHA:
        raise ValueError("Unreviewed CPS source")
    print("[load] reading pppub25.csv, hhpub25.csv and the replicate file", flush=True)
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=ID + DEMO + VALUES + INCOME_FLAGS + OTHER_FLAGS)
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
    d = d.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    d.to_parquet(cache, index=False)
    print(f"[load] cached {len(d)} persons to {cache.name}", flush=True)
    return d


def masks(d):
    """Canonical civilian universe and the 40.9m union (spending builder::canonical_target)."""
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3])
    us = [57, 60, 66, 69, 73, 78]
    union = ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) |
             (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303))) |
             (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)))
    return civilian, (union & civilian).to_numpy()


def spm_index(d):
    return pd.factorize(d.SPM_ID, sort=True)[0]


def unit_equal(values, index):
    """Equal split of each SPM unit's total across all members (receipts shared rule)."""
    values = np.asarray(values, float)
    n = index.max() + 1
    total = np.bincount(index, weights=values, minlength=n)
    size = np.bincount(index, minlength=n).astype(float)
    return (total / size)[index]


def receipt_vectors(d):
    """full_account_receipts_2026_09_20/builder.py::derive_keys, personal convention."""
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    se = .9235 * np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    se = np.where(se >= 400, se, 0)
    se_capped = np.minimum(se, np.maximum(168600 - np.minimum(wage, 168600), 0))
    size = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy(float)
    medicare = d.MCARE.eq(1).to_numpy(float)
    return dict(
        population=np.ones(len(d)), adults=d.A_AGE.ge(18).to_numpy(float), wage=wage,
        wage_oasdi=np.minimum(wage, 168600), self_payroll=.124 * se_capped + .029 * se,
        positive_fica_worker=d.FICA.gt(0).to_numpy(float),
        capital=(d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0).to_numpy(float),
        interest_dividend=(d.INT_VAL + d.DIV_VAL).clip(lower=0).to_numpy(float),
        federal_liability=d.FEDTAX_BC.to_numpy(float),
        federal_high_agi=(d.FEDTAX_BC * d.AGI.ge(500000)).to_numpy(float),
        state_liability=d.STATETAX_A.clip(lower=0).to_numpy(float),
        consumption=d.SPM_RESOURCES.clip(lower=0).to_numpy(float) / size,
        medicare=medicare, medicare_income=medicare * (d.AGI.clip(lower=0).to_numpy(float) + 1))


# Receipt keys already expressed per member of the SPM unit, or person counts: the shared rule
# re-splits unit totals equally, which leaves consumption unchanged.
def receipt_keys(d, index, vectors=None):
    vectors = receipt_vectors(d) if vectors is None else vectors
    return {"personal": vectors,
            "shared": {k: unit_equal(v, index) for k, v in vectors.items()}}


SPENDING_DOLLARS = [("social_security", "SS_VAL"), ("ssi", "SSI_VAL"), ("cash_assistance", "PAW_VAL"),
                    ("unemployment", "UC_VAL"), ("veterans", "VET_VAL"), ("workers_comp", "WC_VAL"),
                    ("wages", "WSAL_VAL")]
SPENDING_UNITS = [("snap", "SPM_SNAPSUB"), ("energy", "SPM_ENGVAL"), ("wic", "SPM_WICVAL"),
                  ("housing_support", "SPM_CAPHOUSESUB")]


def spending_vectors(d, index):
    """full_account_spending_2026_09_20/builder.py::build_keys, CPS-based keys only."""
    counts = np.bincount(index).astype(float)[index]
    dollars = {k: d[v].to_numpy(float) for k, v in SPENDING_DOLLARS}
    dollars["refundable_credits"] = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
    dollars["all_cash"] = sum(dollars[k] for k in ["social_security", "ssi", "cash_assistance",
                                                   "unemployment", "veterans"])
    units = {k: d[v].to_numpy(float) / counts for k, v in SPENDING_UNITS}
    units["resources"] = np.maximum(d.SPM_RESOURCES.to_numpy(float) / counts, 0)
    ages = {"population": np.ones(len(d)), "age65plus": d.A_AGE.ge(65).to_numpy(float),
            "working_age": d.A_AGE.between(18, 64).to_numpy(float), "adults": d.A_AGE.ge(18).to_numpy(float),
            "age5_24": d.A_AGE.between(5, 24).to_numpy(float), "age18_24": d.A_AGE.between(18, 24).to_numpy(float),
            "medicaid_covered": d.MCAID.eq(1).to_numpy(float)}
    out = {}
    for allocation in ["personal", "shared"]:
        vec = {k: (v if allocation == "personal" else unit_equal(v, index)) for k, v in dollars.items()}
        vec.update(units)
        vec.update(ages)
        out[allocation] = vec
    return out


def shares(vectors, W, civ, target):
    """Target share of each key under all 161 weights."""
    out = {}
    for name, v in vectors.items():
        if np.any(v < 0):
            raise ValueError(f"Negative proxy {name}")
        out[name] = (v[target] @ W[target]) / (v[civ] @ W[civ])
    return out


# --------------------------------------------------------------------------
# Imputation status. A value counts as imputed when any allocation flag in the chain
# that produces it is nonzero, or when the whole supplement was imputed: the data
# dictionary codes flag value 9 as "Full record imputation (FL_665 ≠ 1)".
# --------------------------------------------------------------------------
def _any(d, flags):
    return np.logical_or.reduce([d[f].to_numpy() > 0 for f in flags])


# item: (allocation flags, value columns, account keys fed). Earnings flags follow the chain
# WORKYN -> ERN_YN -> ERN_SRCE/ERN_VAL (longest job) and ERN_OTR (I_WSYN) -> WS_VAL/SE_VAL/FRM_VAL.
ITEMS = {
    "wage": (["I_WORKYN", "I_ERNYN", "I_WSYN", "I_WSVAL"], ["WSAL_VAL"], "wage, wage_oasdi, wages"),
    "self_employment": (["I_WORKYN", "I_ERNYN", "I_WSYN", "I_SEYN", "I_SEVAL", "I_FRMYN", "I_FRMVAL"],
                        ["SEMP_VAL", "FRSE_VAL"], "self_payroll"),
    "interest": (["I_INTYN", "I_INTVAL"], ["INT_VAL"], "capital, interest_dividend"),
    "dividends": (["I_DIVYN", "I_DIVVAL"], ["DIV_VAL"], "capital, interest_dividend"),
    "rent": (["I_RNTYN", "I_RNTVAL"], ["RNT_VAL"], "capital"),
    "social_security": (["I_SSYN", "I_SSVAL"], ["SS_VAL"], "social_security, all_cash"),
    "ssi": (["I_SSIYN", "I_SSIVAL"], ["SSI_VAL"], "ssi, all_cash"),
    "public_assistance": (["I_PAWYN", "I_PAWVAL", "I_PAWTYP", "I_PAWMO"], ["PAW_VAL"],
                          "cash_assistance, all_cash"),
    "unemployment": (["I_UCYN", "I_UCVAL"], ["UC_VAL"], "unemployment, all_cash"),
    "veterans": (["I_VETYN", "I_VETVAL", "I_VETTYP", "I_VETQVA"], ["VET_VAL"], "veterans, all_cash"),
    "workers_comp": (["I_WCYN", "I_WCVAL", "I_WCTYP"], ["WC_VAL"], "workers_comp"),
    "pensions_retirement": (["I_PENYN", "I_PENVAL1", "I_PENVAL2", "I_PENSC1", "I_PENSC2", "I_DSTYNCOMP",
                             "I_DSTVAL1COMP", "I_DSTVAL2COMP", "I_DSTSC", "I_DSTSCCOMP", "I_ANNYN", "I_ANNVAL"],
                            ["PEN_VAL1", "PEN_VAL2", "DST_VAL1", "DST_VAL2", "ANN_VAL"], "tax and SPM inputs"),
    "survivor_disability": (["I_SURYN", "I_SURVL1", "I_SURVL2", "I_SURSC1", "I_SURSC2", "I_DISYN", "I_DISVL1",
                             "I_DISVL2", "I_DISCS", "I_DISHP", "I_DISSC1", "I_DISSC2"],
                            ["SUR_VAL1", "SUR_VAL2", "DIS_VAL1", "DIS_VAL2"], "tax and SPM inputs"),
    "other_income": (["I_CSPYN", "I_CSPVAL", "I_EDYN", "I_EDTYP", "I_OEDVAL", "I_FINYN", "I_FINVAL", "I_OIVAL",
                      "I_CAPYN", "I_CAPVAL"], ["CSP_VAL", "ED_VAL", "FIN_VAL", "OI_VAL", "CAP_VAL"],
                     "tax and SPM inputs"),
}
EARN_LEVEL = {0: "reported", 1: "range_1", 2: "range_2", 3: "range_3", 4: "no_range_101", 5: "no_range_102",
              6: "no_range_103", 7: "age_sex_104", 8: "pooled_105", 9: "whole_supplement"}


def item_amount(d, item):
    return d[ITEMS[item][1]].sum(axis=1).to_numpy(float)


def person_status(d):
    """Person-level imputed indicators; income items exist only for persons 15+."""
    full = d.FL_665.ne(1).to_numpy()
    adult15 = d.A_AGE.ge(15).to_numpy()
    s = {"whole_supplement": full & adult15}
    for item, (flags, _, _) in ITEMS.items():
        imp = _any(d, flags) | full
        if item == "wage":
            imp |= d.ERN_SRCE.eq(1).to_numpy() & (d.I_ERNVAL.to_numpy() > 0)
        if item == "self_employment":
            imp |= d.ERN_SRCE.isin([2, 3]).to_numpy() & (d.I_ERNVAL.to_numpy() > 0)
        s[item] = imp & adult15
    s["earnings"] = s["wage"] | s["self_employment"]
    s["capital"] = s["interest"] | s["dividends"] | s["rent"]
    s["all_cash"] = s["social_security"] | s["ssi"] | s["public_assistance"] | s["unemployment"] | s["veterans"]
    # Coverage flags: 1 = hot deck, 3 = whole unit; 2 = logical imputation (an edit rule, not a donor).
    s["medicare"] = d.I_MCARE.isin([1, 3]).to_numpy()
    s["medicare_logical"] = d.I_MCARE.eq(2).to_numpy()
    s["medicaid"] = d.I_MCAID.isin([1, 3]).to_numpy()
    s["medicaid_logical"] = d.I_MCAID.eq(2).to_numpy()
    s["wic_person"] = (d.WICYNA.to_numpy() > 0) | full
    s["moop"] = d.I_MOOP.isin([1, 3]).to_numpy()
    # Household noncash items: household-record flags, repeated on every member.
    s["snap"] = _any(d, ["I_HFOODS", "I_HFDVAL", "I_HFOODM", "I_HFOODN"])
    s["housing"] = _any(d, ["I_HPUBLI", "I_HLOREN"])
    s["school_lunch"] = _any(d, ["I_HFLUNC", "I_HFLUNN"])
    s["energy"] = _any(d, ["I_HENGAS", "I_HENGVA"])
    s["property_value"] = d.I_PROPVAL.to_numpy() > 0
    s["childcare"] = d.I_CHCAREVAL.to_numpy() > 0
    return s


def unit_sum(values, ids):
    codes = pd.factorize(ids)[0]
    return np.bincount(codes, weights=np.asarray(values, float))[codes]


def unit_any(flag, ids):
    """True for every member of a unit in which any member is flagged."""
    return unit_sum(flag.astype(float), ids) > 0


def material_status(d, s, threshold=0.05):
    """A unit's tax-model or SPM quantity counts as imputed when an adult's whole supplement was
    imputed, an adult's work or earnings recipiency was imputed, or imputed dollars reach
    `threshold` of the unit's gross income dollars. threshold=None gives the strict rule: any flag."""
    adult15 = d.A_AGE.ge(15).to_numpy()
    imputed, total = np.zeros(len(d)), np.zeros(len(d))
    for item in ITEMS:
        amount = np.abs(item_amount(d, item))
        total += amount
        imputed += amount * s[item]
    work = (_any(d, ["I_WORKYN", "I_ERNYN"]) | s["whole_supplement"]) & adult15
    out = {}
    for name, ids in [("tax_unit", d.TAX_ID.to_numpy()), ("spm_unit", d.SPM_ID.to_numpy())]:
        if threshold is None:
            any_flag = np.logical_or.reduce([s[i] for i in ITEMS])
            out[name] = unit_any(any_flag, ids)
            continue
        imp, tot = unit_sum(imputed, ids), unit_sum(total, ids)
        share = np.divide(imp, tot, out=np.zeros_like(imp), where=tot > 0)
        out[name] = unit_any(work, ids) | (share >= threshold)
    return out


# Status governing each account key. Keys built from person items use the person's own status in
# the personal convention; once split equally over the SPM unit they carry the unit's status.
PERSON_KEYS = {"wage": "wage", "wage_oasdi": "wage", "self_payroll": "earnings", "positive_fica_worker": "earnings",
               "capital": "capital", "interest_dividend": "capital", "medicare": "medicare",
               "medicare_income": "medicare", "social_security": "social_security", "ssi": "ssi",
               "cash_assistance": "public_assistance", "unemployment": "unemployment", "veterans": "veterans",
               "workers_comp": "workers_comp", "wages": "wage", "all_cash": "all_cash",
               "medicaid_covered": "medicaid"}
TAX_KEYS = {"federal_liability", "federal_high_agi", "state_liability", "refundable_credits"}
SPM_KEYS = {"consumption": "spm_resources", "resources": "spm_resources", "snap": "snap", "energy": "energy",
            "wic": "spm_wic", "housing_support": "housing"}
UNAFFECTED = {"population", "adults", "age65plus", "working_age", "age5_24", "age18_24"}


def key_status(d, threshold=0.05):
    """Imputed indicator for every CPS account key, per allocation convention."""
    s = person_status(d)
    mat = material_status(d, s, threshold)
    spm = d.SPM_ID.to_numpy()
    s["spm_wic"] = unit_any(s["wic_person"], spm)
    s["spm_resources"] = mat["spm_unit"] | s["spm_wic"] | unit_any(s["moop"], spm) | s["snap"] | \
        s["housing"] | s["school_lunch"] | s["energy"] | s["childcare"]
    out = {"personal": {}, "shared": {}}
    for key, name in PERSON_KEYS.items():
        out["personal"][key] = s[name]
        out["shared"][key] = unit_any(s[name], spm)
    for key in TAX_KEYS:
        out["personal"][key] = mat["tax_unit"]
        out["shared"][key] = mat["spm_unit"]
    for key, name in SPM_KEYS.items():
        out["personal"][key] = s[name]
        out["shared"][key] = s[name]
    return out, s, mat


# --------------------------------------------------------------------------
# Cell variables from the basic monthly CPS (observed for whole-supplement imputes too).
# --------------------------------------------------------------------------
def cell_vars(d):
    age = d.A_AGE.to_numpy()
    hga = d.A_HGA.to_numpy()
    lf = d.PEMLR.to_numpy()
    out = pd.DataFrame(index=d.index)
    out["age9"] = np.digitize(age, [15, 18, 25, 35, 45, 55, 65, 75])
    out["age6"] = np.digitize(age, [15, 25, 35, 45, 55, 65])
    out["age3"] = np.digitize(age, [15, 35, 55])
    out["sex"] = d.A_SEX.to_numpy()
    out["edu5"] = np.select([hga == 0, hga <= 38, hga == 39, hga <= 42, hga == 43], [0, 1, 2, 3, 4], 5)
    out["edu4"] = np.select([hga == 0, hga <= 38, hga == 39, hga <= 42], [0, 1, 2, 3], 4)
    out["race3"] = np.select([d.PRDTRACE.eq(1), d.PRDTRACE.eq(2)], [1, 2], 3)
    out["black"] = d.PRDTRACE.eq(2).astype(int).to_numpy()
    out["lf3"] = np.select([np.isin(lf, [1, 2]), np.isin(lf, [3, 4])], [1, 2], 3)  # employed, unemployed, other
    cls = d.A_CLSWKR.to_numpy()
    out["class4"] = np.select([cls == 0, np.isin(cls, [1]), np.isin(cls, [2, 3, 4]), np.isin(cls, [5, 6])],
                              [0, 1, 2, 3], 4)  # none, private, government, self-employed, other
    out["occ"] = d.A_MJOCC.to_numpy()
    out["married"] = d.A_MARITL.isin([1, 2, 3]).astype(int).to_numpy()
    rel = d.PERRP.to_numpy()
    out["rel5"] = np.select([np.isin(rel, [40, 41]), np.isin(rel, range(42, 48)), np.isin(rel, [48, 53]),
                             np.isin(rel, range(49, 53))], [1, 2, 3, 4], 5)
    out["lf5"] = np.select([np.isin(lf, [1, 2]), np.isin(lf, [3, 4]), lf == 5, lf == 6], [1, 2, 3, 4], 5)
    out["region"] = d.GEREG.to_numpy()
    out["foreign_born"] = d.PRCITSHP.isin([4, 5]).astype(int).to_numpy()
    # Income "to this point" (Rothbaum 2019 slides list household income and earnings among the
    # redesigned model variables): own earnings band and household income quintile.
    earn = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    out["earn7"] = np.digitize(earn, [1, 15000, 30000, 45000, 60000, 100000])
    hinc = d.groupby("PH_SEQ").PTOTVAL.transform("sum").to_numpy(float)
    out["hinc5"] = np.digitize(hinc, np.quantile(hinc, [.2, .4, .6, .8]))
    return out


def cell_codes(frame, columns):
    return pd.MultiIndex.from_frame(frame[columns]).factorize()[0] if columns else np.zeros(len(frame), int)

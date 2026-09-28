"""Rough re-key of the adopted September 27 case to 40.9M non-Hispanic white residents. Not the engine.

A modified copy of black_comparator_rough_2026_09_28/rekey.py (the original is not edited). Every group runs through
one code path: a scenario is a person-weight vector on CPS ASEC 2025 and on MEPS 2024, plus the external keys
(Medicaid LTSS, justice). The Mexican-origin union (rough) and the NH Black group reproduce the Black lane's
rekey_summary.csv exactly (gate); the white slices are then scaled to the engine's union population (40,896,574):

  A1  third-plus NH white (native, both parents US-born, NH, white alone), own age structure
  A2  all US-born NH white, own age structure
  A3  third-plus NH white per-age rates at the union's age structure (CPS five-year bands, 80+)
  A4  third-plus NH white per-age rates at the stationary NH white life course (NVSS 2024 Table 16 Lx)

National lines, responses and capital stocks: derived/engine_lines.json (engine_lines.cjs, byte-identical to the
Black lane's). Replacement delta = cost of the union minus cost of the white slice; a negative cost means the slice
leaves other residents better off. Outputs: derived/rekey_summary.csv, rekey_buckets.csv, rekey_line_shares.csv,
keys.csv, age_structures.csv.
"""
import csv
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parent.parent
DER = LANE / "derived"
BLACK = FISCAL / "black_comparator_rough_2026_09_28/derived/rekey_summary.csv"
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
MEPS = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
LIFE = FISCAL / "lifetime_longevity_sstiming_2026_09_18/_cache/lt2024_Table16.xlsx"   # NVSS 2024, NH white
TAF = FISCAL / "ltss_share_2026_09_23/derived/taf_race_ethn.csv"
ARRESTS = FISCAL / "crime_victim_cost_2026_09_23/derived/fbi_2019_table43c_adult_arrests.csv"
US = [57, 60, 66, 69, 73, 78]
OASDI_CAP = 168_600       # 2024 taxable maximum [SOURCE: SSA]
BETA = 0.7                # consumption ~ household income^0.7 [INFERENCE]
K12_PART = 0.74           # K-12 part of education_services; the rest higher education [INFERENCE]
LTSS_PART = 228.65 / 870.0   # T-MSIS 2023 LTSS spending over total Medicaid spending [DATA; total TRAINING-DATA]
BLK_LTSS = 0.20865        # T-MSIS 2023 LTSS spending, black_nh [DATA: ltss_share_2026_09_23/derived/taf_race_ethn.csv]
BLK_CUSTODY = 0.331       # SPI 2016 NH Black share of prisoners [SOURCE: research/immigration-crime-race-ethnicity-2026-09-05.md]
BLK_ARREST = 0.266        # FBI UCR 2019 Table 43A, Black share of all arrests [TRAINING-DATA]
REF_EITC_PART = 0.45      # EITC and ACTC in the refundable-credit line; the rest mostly premium credits [INFERENCE]
# SPI 2016: NH white 30.08% of prisoners; 417,141 of their 427,675 weighted prisoners report a US birthplace
# [DATA: research/immigration-crime-race-ethnicity-2026-09-05.md, analysis/spi_race_composition.csv]
WHT_CUSTODY_USBORN = 0.3008 * 417_141 / 427_675
# Offending-age proxy: NCVS 2024 violent victimisation rate by age (CV2024 Table 3), as the NCVS lane's variant B
# uses it; under 12 zero [SOURCE: ncvs_victim_offender_2026_09_18/age_standardise.py; INFERENCE: victim ages as a
# proxy for offender ages, flatter than arrest curves]
CRIME_AGE = [(12, 17, 29.3), (18, 24, 34.8), (25, 34, 31.7), (35, 49, 27.1), (50, 64, 20.4), (65, 200, 7.5)]
BANDS = list(range(0, 80, 5)) + [80]           # five-year bands, 80 and over


def band(age):
    return np.minimum(np.asarray(age) // 5 * 5, 80).astype(int)


PC = ["PH_SEQ", "TAX_ID", "SPM_ID", "SPM_NUMPER", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
      "PEMNTVTY", "PRDTHSP", "PEHSPNON", "PRDTRACE", "PEARNVAL", "PTOTVAL", "FEDTAX_AC", "STATETAX_A", "EIT_CRED",
      "ACTC_CRD", "SS_VAL", "SSI_VAL", "UC_VAL", "VET_VAL", "WC_VAL", "PAW_VAL", "SPM_SNAPSUB", "SPM_CAPHOUSESUB",
      "SPM_ENGVAL", "NOW_MCARE", "A_HSCOL", "INT_VAL", "DIV_VAL", "RNT_VAL"]
with zipfile.ZipFile(ZIP) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=PC)
    h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPROP_VAL"]).rename(columns={"H_SEQ": "PH_SEQ"})
d = d.merge(h, on="PH_SEQ", how="left", validate="many_to_one")
civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
w = d.MARSUPWT.to_numpy(float) / 100 * civ
native = d.PRCITSHP.isin([1, 2, 3])
parents_us = d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US)
nhw = d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)
MASK = {
    "mex": ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
            | (native & parents_us & d.PRDTHSP.eq(1))).to_numpy(),
    "blk": (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(2)).to_numpy(),
    "w3": (native & parents_us & nhw).to_numpy(),
    "wus": (native & nhw).to_numpy(),
    "wall": nhw.to_numpy(),
    "avg": np.ones(len(d), bool),
}
cage = band(d.A_AGE.to_numpy())


def split(values, keys):
    """Sum a unit-level field over the unit's records, then give each member an equal part."""
    f = pd.DataFrame({k: d[k] for k in keys}).assign(v=np.asarray(values, float))
    g = f.groupby(keys).v
    return (g.transform("sum") / g.transform("size")).to_numpy()


def per_member(field):
    """SPM-unit field repeated on each member: the member's equal part."""
    return d[field].to_numpy(float) / d.SPM_NUMPER.to_numpy(float)


earn = d.PEARNVAL.clip(lower=0).to_numpy(float)
hh_n = d.groupby("PH_SEQ").PH_SEQ.transform("size").to_numpy(float)
hh_inc = split(d.PTOTVAL.clip(lower=0), ["PH_SEQ"]) * hh_n
college = d.A_HSCOL.eq(2).to_numpy(float)
inc_pp = hh_inc / hh_n
K = {
    "pc": np.ones(len(d)),
    "fit": np.maximum(split(d.FEDTAX_AC, ["PH_SEQ", "TAX_ID"]), 0),
    "sit": np.maximum(split(d.STATETAX_A, ["PH_SEQ", "TAX_ID"]), 0),
    "ref": split(d.EIT_CRED + d.ACTC_CRD, ["PH_SEQ", "TAX_ID"]),
    "oasdi": np.minimum(earn, OASDI_CAP),
    "hi": earn,
    "workers": (earn > 0).astype(float),
    "cons": np.maximum(hh_inc, 5_000) ** BETA / hh_n,
    "capinc": split((d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0), ["PH_SEQ"]),
    "prop": d.HPROP_VAL.clip(lower=0).to_numpy(float) / hh_n,
    "mcare": d.NOW_MCARE.eq(1).to_numpy(float),
    "ss": d.SS_VAL.to_numpy(float), "ssi": d.SSI_VAL.to_numpy(float), "uc": d.UC_VAL.to_numpy(float),
    "vet": d.VET_VAL.to_numpy(float), "wc": d.WC_VAL.to_numpy(float), "paw": d.PAW_VAL.to_numpy(float),
    "snap": per_member("SPM_SNAPSUB"), "house": per_member("SPM_CAPHOUSESUB"), "eng": per_member("SPM_ENGVAL"),
    "k12": d.A_AGE.between(5, 17).to_numpy(float),
    "college": college,
    "edben": college * (inc_pp < np.median(inc_pp[civ])),
}
KTOT = {k: float((w * v).sum()) for k, v in K.items()}
CPS_TOTAL = float(w.sum())

# MEPS 2024: persons, age, race/ethnicity, US birth and public payers' spending.
sys.path.insert(0, str(FISCAL / "build"))
from public_mvp_io import parse_meps_sas_fields  # noqa: E402

lay = parse_meps_sas_fields(MEPS.with_name("h256su.txt"))
MF = ["PERWT24F", "RACETHX", "AGELAST", "BORNUSA", "TOTMCD24", "TOTMCR24", "TOTOFD24", "TOTSTL24", "TOTVA24",
      "TOTTRI24"]
with zipfile.ZipFile(MEPS) as z:
    name = [n for n in z.namelist() if n.lower().endswith(".dat")][0]
    rows = [{k: float(t[lay[k][0]:sum(lay[k])]) for k in MF} for t in (ln.decode("ascii") for ln in z.open(name))]
md = pd.DataFrame(rows)
md["OTHPUB"] = md.TOTOFD24 + md.TOTSTL24
mw = md.PERWT24F.to_numpy()
mage = band(np.maximum(md.AGELAST.to_numpy(), 0))
MMASK = {"blk": md.RACETHX.eq(3).to_numpy(), "wall": md.RACETHX.eq(2).to_numpy(),
         "wus": (md.RACETHX.eq(2) & md.BORNUSA.ne(2)).to_numpy()}   # BORNUSA 2 = born abroad; the rest US or n/a
MMASK["w3"] = MMASK["wus"]
MMASK["avg"] = np.ones(len(md), bool)      # MEPS has no parent birthplace: third-plus take the US-born rates [INFERENCE]
MEPS_COLS = ["TOTMCD24", "TOTMCR24", "TOTVA24", "TOTTRI24", "OTHPUB"]
MTOT = {c: float((mw * md[c]).sum()) for c in MEPS_COLS}

# External shares: LTSS spending (T-MSIS 2023) and adult arrests (FBI 2019 Table 43C).
taf = pd.read_csv(TAF)
taf = taf[(taf.year == 2023) & (taf.category == "LTSS") & (taf.measure == "expenditures") & (taf.state == "National")]
WHT_LTSS = float(taf.set_index("group").loc["white_nh", "value"] / taf.total.iloc[0])
arr = pd.read_csv(ARRESTS).set_index("offense").loc["TOTAL"]
# NH white share of adult arrests: white share of race-reported arrests less the Hispanic share of ethnicity-reported
# arrests [INFERENCE: nearly all Hispanic arrestees are recorded as white in UCR race coding]
WHT_ARREST = float(arr.race_white / arr.race_total - arr.hispanic / arr.ethnicity_total)

cj = pd.read_csv(FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv").set_index("component")
case = json.loads((DER / "engine_lines.json").read_text())
lo_lines = {l["side"] + "|" + l["id"]: l for l in case["low"]["lines"] if l["side"] != "scalar"}
NATIONAL = {k: l["national_bn"] for k, l in lo_lines.items()}
eng_share = {k: (l["amount_bn"] / l["national_bn"] if abs(l["national_bn"]) > 1e-6 else 0.0) for k, l in lo_lines.items()}
TARGET = case["low"]["target_population"]
RESIDENT = case["low"]["resident_population"]


def crime_rate(age):
    out = np.zeros(len(age))
    for lo, hi, r in CRIME_AGE:
        out[(age >= lo) & (age <= hi)] = r
    return out


def life_structure():
    """Stationary NH white age structure: NVSS 2024 Table 16 person-years Lx by band."""
    raw = pd.read_excel(LIFE, header=None)
    lx = {}
    for _, row in raw.iterrows():
        lab = str(row[0]).strip().replace("–", "-")
        if lab.startswith("100 and"):
            lx[100] = float(row[4])
        elif "-" in lab and lab[0].isdigit():
            lx[int(lab.split("-")[0])] = float(row[4])
    if sorted(lx) != list(range(101)):
        raise SystemExit(f"[BLOCKED] life table ages incomplete: {LIFE}")
    s = pd.Series(lx)
    by = s.groupby(band(s.index.to_numpy())).sum()
    return (by / by.sum()).reindex(BANDS).to_numpy()


def structure(mask, wt, ages):
    s = pd.Series(wt * mask).groupby(ages).sum().reindex(BANDS, fill_value=0.0)
    return (s / s.sum()).to_numpy()


def reweight(mask, wt, ages, target_pi, total):
    """Person weights for `mask` rescaled so the group has age structure target_pi and `total` persons."""
    own = pd.Series(wt * mask).groupby(ages).sum().reindex(BANDS, fill_value=0.0).to_numpy()
    if (own[target_pi > 0] <= 0).any():
        raise SystemExit("[BLOCKED] a target age band has no group observations")
    f = np.where(own > 0, total * target_pi / np.where(own > 0, own, 1.0), 0.0)
    return wt * mask * f[np.searchsorted(BANDS, ages)]


PI = {"union": structure(MASK["mex"], w, cage), "stationary": life_structure()}
pc_scale = eng_share["spending|general_public_services"] / (float(w[MASK["mex"]].sum()) / CPS_TOTAL)
crime_c = crime_rate(d.A_AGE.to_numpy())
old_c = (d.A_AGE.to_numpy() >= 65).astype(float)
NHW_POP = float(w[MASK["wall"]].sum())
NHW_CRIME = float((w * crime_c)[MASK["wall"]].sum())
NHW_OLD = float((w * old_c)[MASK["wall"]].sum())
WUS_POP = float(w[MASK["wus"]].sum())


def scenario(g, ages="own", scaled=True):
    """Person weights and external keys for one scenario. g: mex, blk, w3 or wus."""
    popg = float(w[MASK[g]].sum())
    total = TARGET if scaled else popg
    if ages == "own":
        cw = w * MASK[g] * (total / popg)
    else:
        cw = reweight(MASK[g], w, cage, PI[ages], total)
    if g == "mex":
        return keyed(g, cw, total, ages)
    mmask = MMASK[g]
    mpop = float(mw[mmask].sum())
    mfrac = (total / CPS_TOTAL) * float(mw.sum())    # the group's MEPS persons, set to its CPS population share
    if ages == "own":
        mwt = mw * mmask * (mfrac / mpop if scaled else 1.0)
    else:
        mwt = reweight(mmask, mw, mage, PI[ages], mfrac)
    return keyed(g, cw, total, ages, mwt)


def keyed(g, cw, total, ages, mwt=None):
    """CPS key shares for person weights cw (total persons), and for g other than mex the external keys from MEPS
    weights mwt (blk: the Black lane's constants; avg: population shares; else the white rules)."""
    sc = {"name": g, "ages": ages, "population": total, "cps_w": cw,
          "share": {k: float((cw * v).sum() / KTOT[k]) for k, v in K.items()},
          "cps_bn": {k: float((cw * K[k]).sum() / 1e9) for k in ("fit", "sit")}}
    if g == "mex":
        return sc
    meps = {c: float((mwt * md[c]).sum() / MTOT[c]) for c in MEPS_COLS}
    ph = sc["share"]["pc"] * pc_scale
    if g == "blk":
        ltss, custody, arrest = BLK_LTSS, BLK_CUSTODY, BLK_ARREST
    elif g == "avg":
        ltss = custody = arrest = total / CPS_TOTAL
    else:
        frac = total / CPS_TOTAL
        crime_f = float((cw * crime_c).sum() / total) / (NHW_CRIME / NHW_POP)   # age factor vs all NH whites
        old_f = float((cw * old_c).sum() / total) / (NHW_OLD / NHW_POP)
        ltss = WHT_LTSS / (NHW_POP / CPS_TOTAL) * frac * old_f        # LTSS scaled by the 65+ share [INFERENCE]
        custody = WHT_CUSTODY_USBORN / (WUS_POP / CPS_TOTAL) * frac * crime_f
        arrest = WHT_ARREST / (NHW_POP / CPS_TOTAL) * frac * crime_f
        sc.update(crime_factor=crime_f, old_factor=old_f)
    key = {"fire": ph, "prisons": custody, "law_courts": 0.6 * arrest + 0.4 * ph, "police_cbp": ph,
           "police_ice_border": ph, "police_ice_interior": ph, "police_non_border": 0.5 * arrest + 0.5 * ph}
    justice = float(sum(cj.loc[c, "national_bn"] * k for c, k in key.items()) / cj.national_bn.sum())
    medicaid = LTSS_PART * ltss + (1 - LTSS_PART) * meps["TOTMCD24"]
    sc["external"] = {"public_order_safety": justice, "health_services": meps["OTHPUB"], "medicare": meps["TOTMCR24"],
                      "veterans_other": meps["TOTVA24"], "military_medical": meps["TOTTRI24"],
                      "medicaid_and_chip_other_medical": medicaid}
    sc["keys"] = {"meps_medicare": meps["TOTMCR24"], "meps_medicaid": meps["TOTMCD24"], "meps_other_public": meps["OTHPUB"],
                  "meps_va": meps["TOTVA24"], "meps_tricare": meps["TOTTRI24"], "ltss": ltss, "custody": custody,
                  "arrests": arrest, "justice": justice, "medicaid_blended": medicaid}
    return sc


RECEIPT_KEY = {"federal_income_tax": "fit", "state_local_income_tax": "sit", "personal_motor_vehicle": "cons",
               "personal_property_tax": "prop", "other_personal_tax": "fit", "employee_oasdi": "oasdi",
               "employer_oasdi": "oasdi", "employee_hi": "hi", "employer_hi": "hi", "self_employment_oasdi_hi": "oasdi",
               "medicare_supplementary_premiums": "mcare", "other_domestic_social_contributions": "workers",
               "corporate_capital": "capinc", "corporate_labor": "hi", "general_sales_tax": "cons",
               "modeled_owner_property": "prop", "remaining_production_property": "capinc",
               "excise_selective_sales": "cons", "customs_duties": "cons", "other_production_taxes": "capinc",
               "government_asset_income": "pc", "business_current_transfers": "capinc",
               "personal_current_transfers": "cons", "enterprise_surplus": "pc"}
SPEND_KEY = {"general_public_services": "pc", "defense": "pc", "economic_affairs_services": "hi",
             "housing_community_services": "pc", "recreation_culture": "pc", "income_security_services": "snap",
             "social_security": "ss", "unemployment": "uc", "railroad_retirement": "ss", "pension_guaranty": "ss",
             "veterans_life_insurance": "vet", "workers_compensation": "wc", "veterans_pension_disability": "vet",
             "veterans_readjustment": "vet", "snap": "snap", "black_lung": "wc", "ssi": "ssi",
             "refundable_tax_credits": "ref", "other_federal_benefits": "ss", "temporary_disability": "wc",
             "family_and_general_assistance": "paw", "energy_assistance": "eng", "other_state_welfare": "paw",
             "education_benefits": "edben", "employment_training": "pc", "other_state_benefits": "pc",
             "domestic_interest": "pc", "agricultural_subsidies": "hi", "housing_subsidies": "house",
             "transport_subsidies": "hi", "other_subsidies": "hi"}
ADJUST = {"school_reprice", "college_rekey", "lane_constants", "source_rounding"}   # Mexican-origin-specific lines
ZERO = {"rest_world_tax_contributions", "rest_world_current_transfers", "foreign_territory_social_benefits",
        "other_foreign_current_transfers", "foreign_interest"}
TOP_TAIL = {"federal_income_tax": ("fit", "receipts|federal_income_tax"),
            "other_personal_tax": ("fit", "receipts|federal_income_tax"),
            "state_local_income_tax": ("sit", "receipts|state_local_income_tax")}
OLD_AGE = {"employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi", "self_employment_oasdi_hi",
           "medicare_supplementary_premiums", "social_security", "medicare", "railroad_retirement", "pension_guaranty"}
# Cost buckets for the replacement table (line effects: spending saved less receipts lost).
BUCKETS = {
    "income taxes": ["federal_income_tax", "state_local_income_tax", "other_personal_tax"],
    "payroll taxes and Medicare premiums": ["employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi",
                                            "self_employment_oasdi_hi", "medicare_supplementary_premiums",
                                            "other_domestic_social_contributions"],
    "sales, excise, customs, fees": ["general_sales_tax", "excise_selective_sales", "customs_duties",
                                     "personal_current_transfers", "personal_motor_vehicle"],
    "capital, property, production taxes": ["corporate_capital", "corporate_labor", "modeled_owner_property",
                                            "remaining_production_property", "other_production_taxes",
                                            "business_current_transfers", "personal_property_tax",
                                            "government_asset_income", "enterprise_surplus"],
    "Social Security": ["social_security", "railroad_retirement", "pension_guaranty"],
    "Medicare": ["medicare"],
    "Medicaid": ["medicaid_and_chip_other_medical"],
    "schools and colleges": ["education_services", "education_benefits", "school_reprice", "college_rekey"],
    "police, courts, prisons": ["public_order_safety"],
    "SNAP, SSI, housing, cash aid, credits, other welfare": [
        "snap", "ssi", "housing_subsidies", "family_and_general_assistance", "other_state_welfare", "energy_assistance",
        "refundable_tax_credits", "income_security_services", "unemployment", "workers_compensation",
        "temporary_disability", "black_lung"],
    "veterans and military medical": ["veterans_pension_disability", "veterans_readjustment", "veterans_other",
                                      "veterans_life_insurance", "military_medical"],
}
PER_HEAD = "per-head lines: government, defense, interest, roads, other"
# Arm: capital-side receipts the case holds at zero response (capital stays when people leave). In a long-run steady
# state the business capital stock follows effective labour and the housing stock follows residents, so these lines
# respond at 1: business lines keyed on earnings, property lines on the group's property value [INFERENCE].
CAP_LINES = {"corporate_capital": "hi", "corporate_labor": "hi", "remaining_production_property": "hi",
             "other_production_taxes": "hi", "business_current_transfers": "hi", "modeled_owner_property": "prop",
             "personal_property_tax": "prop"}


def line_share(sc, side, lid, top="cps"):
    """top: 'cps' charges a group its CPS income-tax dollars (the Black lane's rule: the top tail CPS misses is charged
    to nobody); 'prop' charges the national line by the group's share of CPS income-tax dollars (the missing top tail
    spread in proportion)."""
    g = sc["name"]
    if lid in ZERO:
        return 0.0
    key = RECEIPT_KEY.get(lid) if side == "receipts" else SPEND_KEY.get(lid)
    if side == "spending" and lid == "education_services":
        return K12_PART * sc["share"]["k12"] + (1 - K12_PART) * sc["share"]["college"]
    if key == "pc":
        return sc["share"]["pc"] * pc_scale
    if lid in TOP_TAIL:
        k, nat = TOP_TAIL[lid]
        return sc["share"][k] if top == "prop" else sc["cps_bn"][k] / NATIONAL[nat]
    if lid == "refundable_tax_credits":
        return REF_EITC_PART * sc["share"]["ref"] + (1 - REF_EITC_PART) * sc["share"]["pc"] * pc_scale
    if key:
        return sc["share"][key]
    if g != "mex":
        return sc["external"][lid]
    return eng_share[side + "|" + lid]     # the Mexican rough run keeps the engine's medical and justice shares


def run(sc, end, top="cps", cap=False):
    """sc: a scenario, or 'eng' for the engine's own amounts. top: see line_share. cap: the CAP_LINES arm."""
    g = "eng" if sc == "eng" else sc["name"]
    e = case[end]
    rec_amt = rec_eff = sp_amt = sp_eff = alloc_bal = 0.0
    old = dict(bal=0.0, net=0.0, alloc=0.0)
    rows, buckets = [], {}
    for ln in e["lines"]:
        if ln["side"] == "scalar":
            continue
        side, lid = ln["side"], ln["id"]
        if g == "eng" or (lid in ADJUST and g == "mex"):
            amt = ln["amount_bn"]
        elif lid in ADJUST:
            amt = 0.0
        else:
            amt = ln["national_bn"] * line_share(sc, side, lid, top)
        resp = ln["response"]
        if cap and lid in CAP_LINES:
            amt = ln["national_bn"] * (scenario("mex") if g == "eng" else sc)["share"][CAP_LINES[lid]]
            resp = 1.0
        eff = amt * resp
        if lid not in ZERO:
            alloc_bal += ln["national_bn"] if side == "receipts" else -ln["national_bn"]
        if lid in OLD_AGE:
            sgn = 1 if side == "receipts" else -1
            old["bal"] += sgn * amt
            old["net"] -= sgn * eff
            old["alloc"] += sgn * ln["national_bn"]
        if side == "receipts":
            rec_amt += amt
            rec_eff += eff
        else:
            sp_amt += amt
            sp_eff += eff
        b = next((k for k, v in BUCKETS.items() if lid in v), PER_HEAD)
        buckets[b] = buckets.get(b, 0.0) + (eff if side == "spending" else -eff)
        rows.append((side, lid, ln["national_bn"], amt, ln["response"]))
    sg = scenario("mex")["share"] if g == "eng" else sc["share"]
    ph = sg["pc"] * pc_scale
    ck = {"k12": sg["k12"], "college": sg["college"], "hwy": sg["hi"], "air": sg["hi"]}
    cap_bn = 0.0
    for c in e["capital"]:
        cid = c["id"]
        if cid.startswith("pos"):
            k = sc["external"]["public_order_safety"] if g not in ("eng", "mex") else c["key"]
        elif cid.startswith("health"):
            k = sc["external"]["health_services"] if g not in ("eng", "mex") else c["key"]
        else:
            k = ck.get(cid.split("_")[0], ph)
        cap_bn += c["stock_charged_bn"] * k * c["response"] * e["rate"]
    if g == "eng":
        cap_bn = e["capital_bn"]
    prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
    prod = prod if g in ("mex", "eng") else 0.0    # no production term for a native-born group
    buckets["capital return"] = cap_bn
    buckets["production gain (subtracted)"] = -prod
    net = sp_eff - rec_eff
    popg = e["target_population"] if g in ("eng", "mex") else sc["population"]
    sh = popg / e["resident_population"]
    bal = rec_amt - sp_amt
    return dict(taxes_paid=rec_amt, spending_drawn=sp_amt, taxes_lost=rec_eff, spending_saved=sp_eff, net_budget=net,
                capital=cap_bn, production_gain=prod, cost=net + cap_bn - prod, balance=bal,
                gap=bal - sh * alloc_bal, old_age_net=old["net"], cost_ex_old_age=net + cap_bn - prod - old["net"],
                gap_ex_old_age=(bal - old["bal"]) - sh * (alloc_bal - old["alloc"]), population=popg,
                pop_share=sh), rows, buckets


def write(name, rows, fields):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    scen = {"mexican_origin_engine": "eng", "mexican_origin_rough": scenario("mex"),
            "nh_black_rough": scenario("blk", scaled=False),
            "A1_third_plus_nh_white": scenario("w3"), "A2_us_born_nh_white": scenario("wus"),
            "A3_third_plus_nh_white_at_union_ages": scenario("w3", "union"),
            "A4_third_plus_nh_white_stationary": scenario("w3", "stationary"),
            "all_residents_slice": scenario("avg")}
    summary, bucket_rows, line_rows = [], [], {}
    res = {}
    for end in ("low", "high"):
        for lab, sc in scen.items():
            r, rows, buckets = run(sc, end)
            res[(lab, end)] = (r, buckets)
            r["cost_top_tail_proportional"] = r["cost"] if sc == "eng" else run(sc, end, "prop")[0]["cost"]
            r["cost_capital_taxes_respond"] = run(sc, end, cap=True)[0]["cost"]
            r["cost_both_arms"] = r["cost"] if sc == "eng" else run(sc, end, "prop", cap=True)[0]["cost"]
            summary.append({"group": lab, "end": end, "spec": case[end]["spec"],
                            **{k: f"{v:.4f}" for k, v in r.items() if k not in ("population", "pop_share")},
                            "population": f"{r['population']:.0f}", "pop_share": f"{r['pop_share']:.6f}",
                            "cost_per_member": f"{r['cost'] * 1e9 / r['population']:.0f}",
                            "gap_per_member": f"{r['gap'] * 1e9 / r['population']:.0f}"})
            if end == "low":
                line_rows[lab] = rows
    # Gate: the generalized code reproduces the Black lane's union (rough, engine) and Black rows exactly.
    ref = pd.read_csv(BLACK)
    for lab in ("mexican_origin_engine", "mexican_origin_rough", "nh_black_rough"):
        for end in ("low", "high"):
            mine = next(s for s in summary if s["group"] == lab and s["end"] == end)
            theirs = ref[(ref.group == lab) & (ref.end == end)].iloc[0]
            for col in ("cost", "gap", "net_budget", "capital", "cost_ex_old_age", "gap_ex_old_age", "population"):
                if abs(float(mine[col]) - float(theirs[col])) > 1e-3:
                    raise SystemExit(f"[BLOCKED] {lab} {end} {col}: {mine[col]} vs Black lane {theirs[col]}")
    print("[gate] union (engine, rough) and NH Black rows reproduce the Black lane's rekey_summary.csv")
    for end in ("low", "high"):
        base = {k: res[(k, end)] for k in ("mexican_origin_engine", "mexican_origin_rough")}
        for lab in scen:
            r, bk = res[(lab, end)]
            for b in list(BUCKETS) + [PER_HEAD, "capital return", "production gain (subtracted)"]:
                v = bk.get(b, 0.0)
                bucket_rows.append({"group": lab, "end": end, "bucket": b, "cost_bn": f"{v:.4f}",
                                    "per_member": f"{v * 1e9 / r['population']:.0f}",
                                    "delta_vs_union_rough_bn": f"{base['mexican_origin_rough'][1].get(b, 0.0) - v:.4f}",
                                    "delta_vs_union_engine_bn": f"{base['mexican_origin_engine'][1].get(b, 0.0) - v:.4f}"})
    for s in summary:
        u_r = float(next(x for x in summary if x["group"] == "mexican_origin_rough" and x["end"] == s["end"])["cost"])
        u_e = float(next(x for x in summary if x["group"] == "mexican_origin_engine" and x["end"] == s["end"])["cost"])
        s["delta_like_for_like_bn"] = f"{u_r - float(s['cost']):.4f}"
        s["delta_vs_engine_union_bn"] = f"{u_e - float(s['cost']):.4f}"
        u_p = float(next(x for x in summary if x["group"] == "mexican_origin_rough" and x["end"] == s["end"])[
            "cost_top_tail_proportional"])
        s["delta_like_for_like_top_tail_proportional_bn"] = f"{u_p - float(s['cost_top_tail_proportional']):.4f}"
        for arm in ("cost_capital_taxes_respond", "cost_both_arms"):
            u_a = float(next(x for x in summary if x["group"] == "mexican_origin_rough" and x["end"] == s["end"])[arm])
            s[arm.replace("cost_", "delta_like_for_like_") + "_bn"] = f"{u_a - float(s[arm]):.4f}"
    write("rekey_summary.csv", summary, list(summary[0]))
    write("rekey_buckets.csv", bucket_rows, list(bucket_rows[0]))
    shares = []
    labs = list(scen)
    for i, (side, lid, nat, _, resp) in enumerate(line_rows["mexican_origin_rough"]):
        row = {"side": side, "line": lid, "national_bn": f"{nat:.4f}", "response_low": f"{resp:.4f}"}
        for lab in labs:
            amt = line_rows[lab][i][3]
            row[f"share_{lab}"] = f"{amt / nat:.6f}" if abs(nat) > 1e-6 else ""
        shares.append(row)
    write("rekey_line_shares.csv", shares, list(shares[0]))
    keys = [{"scenario": "all", "key": "cps_total_population", "value": f"{CPS_TOTAL:.0f}"},
            {"scenario": "all", "key": "cps_population_nh_white_all", "value": f"{NHW_POP:.0f}"},
            {"scenario": "all", "key": "cps_population_us_born_nh_white", "value": f"{WUS_POP:.0f}"},
            {"scenario": "all", "key": "cps_population_third_plus_nh_white", "value": f"{w[MASK['w3']].sum():.0f}"},
            {"scenario": "all", "key": "cps_population_union", "value": f"{w[MASK['mex']].sum():.0f}"},
            {"scenario": "all", "key": "tmsis_ltss_share_white_nh", "value": f"{WHT_LTSS:.6f}"},
            {"scenario": "all", "key": "spi_custody_share_us_born_nh_white", "value": f"{WHT_CUSTODY_USBORN:.6f}"},
            {"scenario": "all", "key": "fbi2019_adult_arrest_share_nh_white", "value": f"{WHT_ARREST:.6f}"},
            {"scenario": "all", "key": "per_head_scale", "value": f"{pc_scale:.6f}"}]
    for lab, sc in scen.items():
        if sc == "eng":
            continue
        for k, v in {**sc.get("keys", {}), **{f"cps_{k}": sc["share"][k] for k in ("pc", "fit", "oasdi", "ss", "mcare", "k12")},
                     **{k: sc[k] for k in ("crime_factor", "old_factor") if k in sc}}.items():
            keys.append({"scenario": lab, "key": k, "value": f"{v:.6f}"})
    write("keys.csv", keys, ["scenario", "key", "value"])
    ages = []
    own = {"union": PI["union"], "third_plus_nh_white": structure(MASK["w3"], w, cage),
           "us_born_nh_white": structure(MASK["wus"], w, cage), "stationary_nh_white_lx": PI["stationary"]}
    for i, b in enumerate(BANDS):
        ages.append({"band": f"{b}+" if b == 80 else f"{b}-{b + 4}", **{k: f"{v[i]:.6f}" for k, v in own.items()}})
    write("age_structures.csv", ages, list(ages[0]))
    for s in summary:
        print(f"{s['group']:40s} {s['end']:4s} cost {float(s['cost']):8.1f} per member {int(s['cost_per_member']):7d} "
              f"old-age net {float(s['old_age_net']):7.1f} ex-old-age {float(s['cost_ex_old_age']):7.1f} "
              f"delta like-for-like {float(s['delta_like_for_like_bn']):7.1f} vs engine {float(s['delta_vs_engine_union_bn']):7.1f}"
              f" top-tail prop {float(s['delta_like_for_like_top_tail_proportional_bn']):7.1f} capital {float(s['delta_like_for_like_capital_taxes_respond_bn']):7.1f}"
              f" both {float(s['delta_like_for_like_both_arms_bn']):7.1f}")
    print(f"CPS income tax: federal ${(w * K['fit']).sum() / 1e9:.1f}bn against the national line "
          f"${NATIONAL['receipts|federal_income_tax']:.1f}bn; state ${(w * K['sit']).sum() / 1e9:.1f}bn against "
          f"${NATIONAL['receipts|state_local_income_tax']:.1f}bn")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Borjas (2017) residual imputation of unauthorized status on CPS ASEC 2025.

Rule list, quoted verbatim from George J. Borjas, "The Labor Supply of
Undocumented Immigrants", NBER Working Paper 22102 (March 2016), published as
Labour Economics 46 (2017) 1-13, pp. 10-11:

    "The algorithm I use to create a comparable undocumented status identifier
    in all the relevant ASEC files is as follows. A foreign-born person will be
    classified as a legal immigrant if:

    a. that person arrived before 1980;
    b. that person is a citizen;
    c. that person receives Social Security benefits, SSI, Medicaid, Medicare,
       or Military Insurance;
    d. that person is a veteran, is currently in the Armed Forces;
    e. that person works in the government sector;
    f. that person resides in public housing or receives rental subsidies, or
       that person is a spouse of someone who resides in public housing or
       receives rental subsidies;
    g. that person was born in Cuba (as practically all Cuban immigrants are
       granted refugee status);
    h. that person's occupation requires some form of licensing (such as
       physicians, registered nurses, air traffic controllers, and lawyers;
    i. that person's spouse is a legal immigrant or citizen.

    The residual group of all other foreign-born persons is then classified as
    undocumented."

[SOURCE: https://www.nber.org/system/files/working_papers/w22102/w22102.pdf pp. 10-11]

Two rules need a concrete list the paper does not print:

* (h) the paper names four example occupations only. LICENSED_OCC below is this
  lane's list of 2018-vintage Census occupation codes, flagged [INFERENCE].
  `--no-occupation-rule` drops rule (h) entirely as a sensitivity.
* (g) the paper's refugee rule is Cuba ALONE. Pew/CMS implementations use a
  wider refugee-origin list; `--wide-refugee` adds Vietnam, Laos, Cambodia,
  Thailand, the former USSR/Ukraine, Iraq, Iran, Afghanistan, Somalia, Syria,
  Eritrea, Ethiopia, Sudan, Bosnia, Burma, Bhutan and the DRC as a sensitivity,
  flagged [INFERENCE] against the paper's own rule.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

# CPS ASEC PEINUSYR bands. 1 = before 1950 ... 6 = 1975-1979, 7 = 1980-1981.
# Rule (a) "arrived before 1980" is therefore codes 1-6.
PEINUSYR_PRE_1980 = [1, 2, 3, 4, 5, 6]

# PENATVTY country codes (CPS ASEC country-of-birth recode). Verified against
# this repo's own crosswalk, infra/immigration-fiscal/secgen_selectivity_2026_09_16/
# country_crosswalk.csv (cps_code -> cps_name): 327 = Cuba, 303 = Mexico.
CUBA = 327
# Wider Pew/CMS-style refugee-origin list, used only by --wide-refugee. Taken from
# the refugee_origin=1 rows of that same crosswalk. [INFERENCE] against the paper,
# whose rule (g) is Cuba alone.
WIDE_REFUGEE = {147, 150, 151, 152, 154, 158, 159, 160, 161, 162, 163, 164, 165,
                168, 200, 205, 206, 212, 213, 218, 223, 246, 247, 327, 416, 417,
                448, 451}

# Rule (h). 2018 Census occupation codes (PEIOOCC on ASEC 2020+). [INFERENCE]
LICENSED_OCC = {
    2100,  # Lawyers
    2110,  # Judges, magistrates, and other judicial workers
    3000,  # Chiropractors
    3010,  # Dentists
    3030,  # Dietitians and nutritionists
    3040,  # Optometrists
    3050,  # Pharmacists
    3090,  # Physicians
    3100,  # Surgeons
    3110,  # Physician assistants
    3120,  # Podiatrists
    3140,  # Audiologists
    3150,  # Occupational therapists
    3160,  # Physical therapists
    3200,  # Radiation therapists
    3210,  # Recreational therapists
    3220,  # Respiratory therapists
    3230,  # Speech-language pathologists
    3245,  # Other therapists
    3250,  # Veterinarians
    3255,  # Registered nurses
    3256,  # Nurse anesthetists
    3258,  # Nurse practitioners and nurse midwives
    3300,  # Licensed practical and licensed vocational nurses
    3600,  # Dental hygienists
    3700,  # Emergency medical technicians and paramedics
    3740,  # Firefighters
    3800,  # Bailiffs and correctional officers
    3820,  # Detectives and criminal investigators
    3850,  # Police officers
    3870,  # Transit and railroad police
    9030,  # Aircraft pilots and flight engineers
    9040,  # Air traffic controllers and airfield operations specialists
}

GOVERNMENT_CLSWKR = [2, 3, 4]   # federal, state, local government


def impute(d: pd.DataFrame, hh: pd.DataFrame, *, use_occupation_rule: bool = True,
           refugee: str = "cuba", use_medicaid_rule: bool = True) -> dict:
    """Return per-person boolean arrays: foreign_born, legal, unauthorized, plus rule hits.

    `d` must carry PH_SEQ, A_LINENO, A_SPOUSE and the fields named in the rules.
    `hh` must carry H_SEQ, HPUBLIC, HLORENT.
    """
    need = ["PH_SEQ", "A_LINENO", "A_SPOUSE", "PRCITSHP", "PENATVTY", "PEINUSYR",
            "SS_VAL", "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN",
            "PEAFEVER", "PRPERTYP", "A_CLSWKR", "PEIOOCC"]
    missing = [c for c in need if c not in d.columns]
    if missing:
        raise ValueError(f"impute() missing required CPS fields: {missing}")

    hsub = hh[["H_SEQ", "HPUBLIC", "HLORENT"]]
    m = d[["PH_SEQ"]].merge(hsub, left_on="PH_SEQ", right_on="H_SEQ",
                            how="left", validate="many_to_one")
    if m.H_SEQ.isna().any():
        raise ValueError("Person record without a household record in impute()")
    subsidised_housing = (m.HPUBLIC.eq(1) | m.HLORENT.eq(1)).to_numpy()

    foreign_born = d.PRCITSHP.isin([4, 5]).to_numpy()
    citizen = d.PRCITSHP.isin([1, 2, 3, 4]).to_numpy()   # rule (b): includes naturalized

    rule = {}
    rule["a_arrived_pre_1980"] = d.PEINUSYR.isin(PEINUSYR_PRE_1980).to_numpy()
    rule["b_citizen"] = citizen
    benefit = (d.SS_VAL.gt(0) | d.SSI_VAL.gt(0) | d.MCARE.eq(1)
               | d.MIL.eq(1) | d.CHAMPVA.eq(1))
    if use_medicaid_rule:
        # The paper's clause assumes Medicaid implies legal status. States that cover people
        # regardless of status break it (California: children from 2016, all ages from 2024).
        # `california_medical_status_2026_09_23` measures the damage: 0.47-0.66M Mexico-born moved
        # into the legal column; its STATUS_BLIND_2024 rule set is the state-aware alternative.
        print("[DEGRADED] impute_status: Medicaid clause treats every Medicaid reporter as legal; "
              "wrong in status-blind states (CA 2016+/2024+). State-aware variant: "
              "california_medical_status_2026_09_23/cps_ca_status.py STATUS_BLIND_2024",
              file=sys.stderr)
        benefit = benefit | d.MCAID.eq(1)
    rule["c_benefits"] = benefit.to_numpy()
    rule["d_veteran_or_armed_forces"] = (d.VET_YN.eq(1) | d.PEAFEVER.eq(1)
                                         | d.PRPERTYP.eq(3)).to_numpy()
    rule["e_government_sector"] = d.A_CLSWKR.isin(GOVERNMENT_CLSWKR).to_numpy()
    rule["f_subsidised_housing"] = subsidised_housing
    if refugee == "cuba":
        rule["g_refugee_origin"] = d.PENATVTY.eq(CUBA).to_numpy()
    elif refugee == "wide":
        rule["g_refugee_origin"] = d.PENATVTY.isin(sorted(WIDE_REFUGEE)).to_numpy()
    else:
        raise ValueError(f"unknown refugee option {refugee!r}")
    rule["h_licensed_occupation"] = (d.PEIOOCC.isin(sorted(LICENSED_OCC)).to_numpy()
                                     if use_occupation_rule
                                     else np.zeros(len(d), dtype=bool))

    own_legal = np.zeros(len(d), dtype=bool)
    for v in rule.values():
        own_legal |= v

    # --- spouse linkage: A_SPOUSE is the spouse's A_LINENO inside PH_SEQ -----
    key = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.A_LINENO.to_numpy()])
    lookup = pd.Series(np.arange(len(d)), index=key)
    if lookup.index.duplicated().any():
        raise ValueError("PH_SEQ + A_LINENO is not unique")
    want = pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.A_SPOUSE.to_numpy()])
    spouse_row = lookup.reindex(want).to_numpy()
    has_spouse = d.A_SPOUSE.gt(0).to_numpy() & ~np.isnan(spouse_row)
    spouse_idx = np.where(has_spouse, np.nan_to_num(spouse_row, nan=0.0), 0).astype(int)

    # Rule (f) second clause: spouse of someone in subsidised housing. Same
    # household by construction, so this adds nothing; kept explicit anyway.
    own_legal = own_legal | (has_spouse & subsidised_housing[spouse_idx])

    # Rule (i) is recursive (spouse legal -> person legal). Iterate to a fixpoint.
    legal = own_legal.copy()
    for _ in range(10):
        nxt = legal | (has_spouse & legal[spouse_idx])
        if np.array_equal(nxt, legal):
            break
        legal = nxt
    else:
        raise ValueError("spouse legality did not reach a fixpoint")

    rule["i_spouse_legal_or_citizen"] = legal & ~own_legal
    unauthorized = foreign_born & ~legal
    return {"foreign_born": foreign_born, "legal": legal,
            "unauthorized": unauthorized, "rule": rule,
            "own_legal": own_legal, "has_spouse": has_spouse}

"""Assemble the state × year × grade × subject analysis panel from the lane's derived inputs.

Inputs (all built in this lane):
  derived/naep_state_long.csv        acquire_naep.py      NAEP Data Service API
  derived/state_shares.csv           acquire_shares.py    CCD (Urban Institute API) and ACS 1-year
  inclusion/derived/naep_inclusion.csv inclusion/acquire_inclusion.py  NAEP technical appendices
  derived/mapping_cut_scores.csv     acquire_mapping.py   NCES state mapping tables
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STATES = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH "
          "NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split()
REGION = {  # Census regions
    **{s: "Northeast" for s in "CT ME MA NH RI VT NJ NY PA".split()},
    **{s: "Midwest" for s in "IL IN MI OH WI IA KS MN MO NE ND SD".split()},
    **{s: "South" for s in "DE DC FL GA MD NC SC VA WV AL KY MS TN AR LA OK TX".split()},
    **{s: "West" for s in "AZ CO ID MT NV NM UT WY AK CA HI OR WA".split()},
}
CELLS = [("mathematics", 4), ("mathematics", 8), ("reading", 4), ("reading", 8)]
MAIN_YEARS = [2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019]
ALL_YEARS = MAIN_YEARS + [2022, 2024]


def _pick(d, variable, stattype, value, name, se=True):
    x = d[(d.variable == variable) & (d.stattype == stattype) & (d.var_value == value)]
    cols = {"value": name}
    if se:
        cols["std_error"] = name + "_se"
    return x.rename(columns=cols)[["subject", "grade", "year", "jurisdiction"] + list(cols.values())]


def naep_panel():
    d = pd.read_csv(HERE / "derived" / "naep_state_long.csv", dtype={"var_value": str})
    parts = [
        _pick(d, "SDRACE", "MN:MN", "1", "white"),
        _pick(d, "LEP", "MN:MN", "2", "nonel"),
        _pick(d, "SDRACE+LEP", "MN:MN", "1+2", "white_nonel"),
        _pick(d, "SDRACE+LEP", "MN:MN", "3+2", "hisp_nonel"),
        _pick(d, "SDRACE", "MN:MN", "3", "hisp"),
        _pick(d, "SDRACE", "MN:MN", "2", "black"),
        _pick(d, "TOTAL", "MN:MN", "1", "all"),
        _pick(d, "SDRACE", "RP:RP", "3", "rp_hisp"),
        _pick(d, "SDRACE", "RP:RP", "1", "rp_white"),
        _pick(d, "LEP", "RP:RP", "1", "rp_el"),
        _pick(d, "SDRACE", "PC:P1", "1", "white_p10"),
        _pick(d, "SDRACE", "PC:P9", "1", "white_p90"),
        _pick(d, "SLUNCH3+SDRACE", "RP:RP", "1+1", "white_nslp"),
        _pick(d, "PARED+SDRACE", "RP:RP", "4+1", "white_parcol"),
    ]
    p = parts[0]
    for q in parts[1:]:
        p = p.merge(q, on=["subject", "grade", "year", "jurisdiction"], how="outer")
    sd = d[(d.stattype == "SD:SD") & (d.jurisdiction == "NP")]
    sd_all = sd[sd.variable == "TOTAL"].rename(columns={"value": "sd_np_all"})[["subject", "grade", "year", "sd_np_all"]]
    sd_w = sd[(sd.variable == "SDRACE") & (sd.var_value == "1")].rename(columns={"value": "sd_np_white"})[
        ["subject", "grade", "year", "sd_np_white"]]
    p = p.merge(sd_all, on=["subject", "grade", "year"], how="left").merge(sd_w, on=["subject", "grade", "year"], how="left")
    # fixed SD per cell: national public all-student SD in 2019
    base = sd_all[sd_all.year == 2019].set_index(["subject", "grade"]).sd_np_all
    p["sd2019"] = [base[(s, g)] for s, g in zip(p.subject, p.grade)]
    p = p.rename(columns={"jurisdiction": "state"})
    return p


def shares():
    s = pd.read_csv(HERE / "derived" / "state_shares.csv")
    ccd = s[["state", "fall_year", "hisp_share", "white_share", "el_share_ccd", "ccd_total"]].copy()
    ccd["year"] = ccd.fall_year + 1  # fall of the school year whose spring NAEP tests
    acs = s[["state", "fall_year", "fb_share_u18", "fb_share_617", "imm_origin_share_617"]].rename(
        columns={"fall_year": "year"})  # ACS calendar year = NAEP calendar year
    return ccd.drop(columns="fall_year"), acs


def inclusion():
    i = pd.read_csv(HERE / "inclusion" / "derived" / "naep_inclusion.csv", low_memory=False)
    i = i[(i.jurisdiction_type == "state") | (i.jurisdiction_abbr == "DC") | (i.jurisdiction_abbr == "NP")]
    keep = ["el_identified_pct_all", "el_excluded_pct_all", "el_excluded_pct_identified", "sd_identified_pct_all",
            "sd_excluded_pct_all", "sd_excluded_pct_identified", "sdel_excluded_pct_all", "sdel_identified_pct_all"]
    out = i[["subject", "grade", "year", "jurisdiction_abbr"] + keep + [k + "_flag" for k in keep]].rename(
        columns={"jurisdiction_abbr": "state"})
    for k in keep:  # "#" rounds to zero: kept as 0; "‡" and other flags are blank already
        out[k] = pd.to_numeric(out[k], errors="coerce")
    return out


def build():
    p = naep_panel()
    ccd, acs = shares()
    p = p.merge(ccd, on=["state", "year"], how="left").merge(acs, on=["state", "year"], how="left")
    p = p.merge(inclusion(), on=["subject", "grade", "year", "state"], how="left")
    p = p[p.state.isin(STATES)].copy()
    p["region"] = p.state.map(REGION)
    p["cell"] = p.subject.str[:4] + p.grade.astype(str)
    p = p.sort_values(["subject", "grade", "state", "year"]).reset_index(drop=True)
    return p


if __name__ == "__main__":
    p = build()
    print(p.shape)
    print(p[p.year.isin(MAIN_YEARS)].groupby("cell")[["white", "hisp_share", "el_identified_pct_all",
                                                         "imm_origin_share_617"]].count())

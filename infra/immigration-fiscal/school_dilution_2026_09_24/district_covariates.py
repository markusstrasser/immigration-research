"""District covariates by fall: CCD membership (all, Hispanic), English learners, SAIPE child poverty.

Shared by compensatory.py and price.py. F-33 fiscal year t pairs with CCD fall t-1 (fall 2019 =
SY2019-20 = FY2020). New York City's CCD geographic districts are merged into F-33's single unit.

Sources, in order of preference:
  CCD falls 2000/2005/2010/2019 membership by race and directory: this lane's pull_ccd.py cache if a
    year is complete, else the school-flight lane's pull of the same Urban endpoints (2026-09-18).
  CCD fall 2023: NCES LEA membership 2023-24 as aggregated by the school-cost lane (ccd.py, K-12 and
    total counts, all and Hispanic).
  English learners 2018-19: NCES CCD LEA file 141 (LEP_COUNT), staged in sources/.
  SAIPE school-district estimates 2005, 2010, 2019, 2023: relevant children 5-17 and those in poverty.
"""
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CCD = HERE / "_cache" / "ccd"
FLIGHT = FISCAL / "school_flight_2026_09_18" / "_cache" / "dist"
LEA_2324 = FISCAL / "school_cost_where_enrolled_2026_09_24" / "_cache" / "ccd_lea_2324_counts.csv"
DIR_2324 = Path("/Users/alien/research-data/immigration-fiscal/data/external/nces_ccd/ccd_lea_029_2324_w_1a_073124.zip")
EL_1819 = FISCAL.parents[1] / "sources/immigration-fiscal/data/external/stage5_net_negative/nces/ccd_lea_141_1819_english_learners.zip"
SAIPE = HERE / "_cache" / "saipe"
NYC_F33 = "3620580"


def _files(kind, fall):
    for folder in (CCD, FLIGHT):
        files = sorted(folder.glob(f"{kind}_{fall}_*.csv"))
        if len(files) == 51:
            return files
    raise SystemExit(f"[BLOCKED] no complete set of 51 CCD {kind} files for fall {fall}")


def directory(fall):
    d = pd.concat([pd.read_csv(p, dtype={"leaid": str}) for p in _files("dir", fall)], ignore_index=True)
    d["leaid"] = d.leaid.str.zfill(7)
    return d


def _nyc(frame, names):
    nyc = frame.leaid.map(names).fillna("").str.upper().str.startswith("NEW YORK CITY GEOGRAPHIC DISTRICT")
    frame.loc[nyc, "leaid"] = NYC_F33
    return frame


def membership(fall):
    """leaid -> pupils (all) and Hispanic pupils, fall `fall`."""
    if fall == 2023:
        m = pd.read_csv(LEA_2324, dtype={"LEAID": str})
        with zipfile.ZipFile(DIR_2324) as f:
            dr = pd.read_csv(f.open("ccd_lea_029_2324_w_1a_073124.csv"), dtype=str, usecols=["LEAID", "LEA_NAME"])
        m = m.rename(columns={"LEAID": "leaid", "tot_all": "pupils", "tot_hisp": "hisp"})[["leaid", "pupils", "hisp"]]
        m = _nyc(m, dr.set_index("LEAID").LEA_NAME)
    else:
        e = pd.concat([pd.read_csv(p, dtype={"leaid": str}) for p in _files("enr", fall)], ignore_index=True)
        e["leaid"] = e.leaid.str.zfill(7)
        names = directory(fall).set_index("leaid").lea_name
        m = e.rename(columns={"enr_total": "pupils", "enr_hisp": "hisp"})[["leaid", "pupils", "hisp"]]
        m = _nyc(m, names[~names.index.duplicated()])
    m = m.groupby("leaid", as_index=False)[["pupils", "hisp"]].sum(min_count=1)
    m = m[m.pupils.gt(0)]
    m["hisp_share"] = (m.hisp / m.pupils).clip(0, 1)
    return m.set_index("leaid")


def english_learners(fall):
    """leaid -> EL count; CCD directory for 2000/2005/2010/2019, NCES file 141 for fall 2018."""
    if fall == 2018:
        with zipfile.ZipFile(EL_1819) as f:
            d = pd.read_csv(f.open("ccd_lea_141_1819_l_1a_091019.csv"), dtype={"LEAID": str})
        d["el"] = pd.to_numeric(d.LEP_COUNT, errors="coerce")
        d = d.rename(columns={"LEAID": "leaid"})[["leaid", "el"]]
    else:
        d = directory(fall)
        d["el"] = pd.to_numeric(d.english_language_learners, errors="coerce")
        d = _nyc(d, d.set_index("leaid").lea_name[~d.set_index("leaid").index.duplicated()])
        d = d[["leaid", "el"]]
    d = d[d.el.ge(0)]
    return d.groupby("leaid").el.sum()


def saipe(year):
    """leaid -> (children 5-17, children 5-17 in poverty in families), SAIPE `year`."""
    rows = []
    for line in (SAIPE / f"ussd{year % 100:02d}.txt").read_text(encoding="latin-1").splitlines():
        tok = line.split()
        rows.append({"leaid": line[0:2] + line[3:8], "kids": float(tok[-4]), "kids_pov": float(tok[-3])})
    s = pd.DataFrame(rows).groupby("leaid").sum()
    s["pov_rate"] = np.where(s.kids > 0, s.kids_pov / s.kids, np.nan)
    return s

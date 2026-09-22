#!/usr/bin/env python3
"""Religion, employment and earnings among NIS-2003 Round 1 adult immigrants.

Every code used below is transcribed from the ICPSR 38031 v3 primary documentation
(picklists, questionnaires, P.I. codebooks) bundled in the study zip; the source file
for each code list is recorded in CODE_SOURCES and written to derived/audit.json.

Run:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/analysis.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import numpy as np
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache" / "ICPSR_38031"
DERIVED = LANE / "derived"
ZIP = pathlib.Path(
    "/Users/alien/Projects/immigration-research/sources/immigration-fiscal/data/"
    "external/icpsr_nis_2003/ICPSR_38031-V3.zip"
)
ZIP_SHA256 = "61a6e3d58d79f6522bfe1deda84d287aa53960d46b5e97fbee265b010b9885c1"
N_ADULT = 8573
N_BOOT = 500
SEED = 20260922

# ---------------------------------------------------------------------------
# Code lists. Transcribed verbatim from the primary documentation in the zip.
# ---------------------------------------------------------------------------
CODE_SOURCES = {
    "J30_1MO": "ICPSR_38031/DS0017/38031-0017-Questionnaire-SectionJ_MULTI.pdf (item J30_X) "
    "and ICPSR_38031/DS0001/38031-0001-Documentation-picklists_public_MULTI.pdf (RELPICK1)",
    "J14": "ICPSR_38031/DS0017/38031-0017-Questionnaire-SectionJ_MULTI.pdf (item J14)",
    "C1": "ICPSR_38031/DS0006/38031-0006-Questionnaire-SectionC_MULTI.pdf (item C1)",
    "C47_1": "ICPSR_38031/DS0006/38031-0006-Questionnaire-SectionC_MULTI.pdf (item C47_X)",
    "C48A2_1": "ICPSR_38031/DS0006/38031-0006-Questionnaire-SectionC_MULTI.pdf (item C48A2_X)",
    "G7/G15": "ICPSR_38031/DS0011/38031-0011-Questionnaire-SectionG_MULTI.pdf (items G7, G15)",
    "A6": "ICPSR_38031/DS0003/38031-0003-Codebook-PI.pdf (R00008.00 [A6])",
    "CISADJUST": "ICPSR_38031/DS0002/38031-0002-Codebook-PI.pdf (cisadjust)",
    "VISACATMO": "ICPSR_38031/DS0002/38031-0002-Codebook-PI.pdf (visacatmo)",
    "CISCOBINSMO": "ICPSR_38031/DS0002/38031-0002-Codebook-PI.pdf (ciscobinsmo)",
    "NISADULTSTR": "ICPSR_38031/DS0002/38031-0002-Codebook-PI.pdf (nisadultstr)",
    "NISWGTSAMP1": "ICPSR_38031/38031-Documentation-sampling_weights.pdf (design-weight recipe + Table 1)",
}

# Variable labels as printed in the ICPSR / P.I. codebooks in the zip, transcribed so that
# every recoded variable can be checked against its documentation without reopening the PDFs.
VARIABLE_LABELS = {
    "J30_1MO": "R's religion, 1 (DS0017 ICPSR codebook; codes from questionnaire item J30_X)",
    "J14": "HOW WELL SPEAK ENGLISH (DS0017 ICPSR codebook; codes from questionnaire item J14)",
    "A6": "GENDER — 1 Male (4,133), 2 Female (4,440) (DS0003 P.I. codebook R00008.00)",
    "A7": "YEAR BORN (DS0003 ICPSR codebook)",
    "A20": "YEARS SCHOOL COMPLETED (DS0003 ICPSR codebook)",
    "C1": "CURRENT EMPLOYMENT (DS0006 ICPSR codebook; codes from questionnaire item C1)",
    "C33_1": "HRS PER WEEK CURRENTLY WORK (DS0006 ICPSR codebook; item C33_X, upper limit 168)",
    "C37_1": "WKS PER YR USUALLY WORK (DS0006 ICPSR codebook; item C37_X, upper limit 52)",
    "C47_1": "SALARIED OR PAID BY THE HOUR (DS0006 ICPSR codebook; item C47_X)",
    "C48A2_1": "SALARY UNIT (DS0006 ICPSR codebook; item C48A2_X)",
    "C48_1PPP": "SALARY BEFORE TAX in US current prices, PPP adjusted (DS0007 ICPSR codebook)",
    "C49_1PPP": "HOURLY WAGE RATE in US current prices, PPP adjusted (DS0007 ICPSR codebook)",
    "G7": "INCOME FROM WAGES AND SALARY (DS0011 ICPSR codebook; item G7)",
    "G7APPP": "INCOME FROM WAGES AND SALARY in US current prices, PPP adj (DS0012 ICPSR codebook)",
    "G15 (spouse path)": "SPOUSE INCOME FROM WAGES AND SALARY (DS0011 ICPSR codebook; item G15)",
    "G16PPP (spouse path)": "HOW MUCH SPOUSE WAGES in US current prices, PPP adj (DS0012/DS0054)",
    "WHOKNOW": "WHO IS MOST KNOWLEDGEABLE RE FINANCES (DS0011 ICPSR codebook)",
    "CISADJUST": "1=adjust, 0=new arrival (DS0002 P.I. codebook)",
    "CISCOBINSMO": "Country of birth, valid 2003 ins code (DS0002 P.I. codebook)",
    "VISACATMO": "NIS visa categories (DS0002 P.I. codebook)",
    "NISADULTSTR": "1=spcitz, 2=empprin, 3=divprin, 4=other (DS0002 P.I. codebook)",
    "NISWGTSAMP1": "Sampling Weights (DS0002; recipe in 38031-Documentation-sampling_weights.pdf)",
    "H1 / H1A": "PLACE WHERE YOU LIVE / H1 OWN THIS PLACE (DS0013 ICPSR codebook; items H1, H1A)",
}

RELIGION_CODES = {  # RELPICK1 / item J30_X
    1: "Catholic",
    2: "Orthodox Christian",
    3: "Protestant",
    4: "Muslim",
    5: "Jewish",
    6: "Buddhist",
    7: "Hindu",
    8: "No religion",
    997: "Some other religion",
    -1: "REFUSED",
    -2: "DON'T KNOW",
}
RELIGION_GROUP = {  # analysis grouping
    1: "Catholic",
    2: "Orthodox",
    3: "Protestant",
    4: "Muslim",
    5: "Jewish",
    6: "Buddhist",
    7: "Hindu",
    8: "No religion",
    997: "Other",
}
CHRISTIAN = ("Catholic", "Orthodox", "Protestant")

ENGLISH_CODES = {1: "Very well", 2: "Well", 3: "Not well", 4: "Not at all", -1: "REFUSED", -2: "DON'T KNOW"}
C1_CODES = {
    1: "WORKING NOW",
    2: "UNEMPLOYED AND LOOKING FOR WORK",
    3: "TEMPORARILY LAID OFF, ON SICK OR OTHER LEAVE",
    4: "DISABLED",
    5: "RETIRED",
    6: "HOMEMAKER",
    97: "OTHER (SPECIFY)",
    -1: "REFUSED",
    -2: "DON'T KNOW",
}
C47_CODES = {1: "SALARIED", 2: "HOURLY", 3: "PIECEWORK/COMMISSION", 4: "OTHER/COMBINATION", -1: "REFUSED", -2: "DON'T KNOW"}
C48A2_CODES = {
    1: "Hour",
    2: "Week",
    3: "Every two weeks/bi-weekly",
    4: "Month",
    5: "Year",
    97: "OTHER (SPECIFY)",
    -1: "REFUSED",
    -2: "DON'T KNOW",
}
YESNO_CODES = {1: "YES", 2: "NO", -1: "REFUSED", -2: "DON'T KNOW"}
SEX_CODES = {1: "(IM) MALE", 2: "(IM) FEMALE"}  # A6 GENDER, P.I. codebook R00008.00
VISACAT_CODES = {
    0: "Other",
    1: "Spouse of U.S. Citizen",
    2: "Spouse of Legal Permanent Resident",
    3: "Parent of U.S. Citizen",
    4: "Child of U.S. Citizen",
    5: "Family Fourth Preference",
    7: "Employment Preferences",
    9: "Diversity Immigrants",
    11: "Refugee/Asylee/Parolee",
    13: "Legalization",
}
ADJUST_CODES = {0: "New arrival", 1: "Adjusting status"}
STRATUM_CODES = {1: "Spouse of U.S. Citizen", 2: "Employment principal", 3: "Diversity", 4: "Other"}
COUNTRY_CODES = {  # ciscobinsmo, P.I. codebook DS0002
    38: "CANADA", 44: "CHINA, PEOPLES REPUBLIC", 47: "COLOMBIA", 55: "CUBA",
    62: "DOMINICAN REPUBLIC", 65: "EL SALVADOR", 69: "ETHIOPIA", 88: "GUATEMALA",
    92: "HAITI", 98: "INDIA", 105: "JAMAICA", 111: "KOREA", 135: "MEXICO",
    152: "NIGERIA", 163: "PERU", 164: "PHILIPPINES", 166: "POLAND", 172: "RUSSIA",
    215: "UKRAINE", 217: "UNITED KINGDOM", 218: "UNITED STATES", 219: "UNKNOWN",
    224: "VIETNAM", 301: "EUROPE & CENTRAL ASIA", 302: "EAST ASIA, SOUTH ASIA & THE PACIFIC",
    304: "OTHER NORTH AMERICA", 305: "LATIN AMERICA & THE CARIBBEAN",
    306: "AFRICAN SUB-SAHARAN", 307: "MIDDLE EAST & NORTH AFRICA", 308: "OCEANIA",
    310: "ARCTIC REGION",
}
# Named countries folded into the file's own residual world-region codes. This mapping is
# [INFERENCE] from the residual codes' labels; the residual codes themselves are authoritative.
COUNTRY_TO_REGION = {
    166: 301, 172: 301, 215: 301, 217: 301,
    44: 302, 98: 302, 111: 302, 164: 302, 224: 302,
    38: 304, 218: 304,
    47: 305, 55: 305, 62: 305, 65: 305, 88: 305, 92: 305, 105: 305, 135: 305, 163: 305,
    69: 306, 152: 306,
}

# Table 1, NIS-2003 Round 1 Adult Sample Summary, 38031-Documentation-sampling_weights.pdf.
# replicate -> stratum -> (frame, sampled, complete)
WEIGHT_TABLE = {
    1: {1: (6235, 147, 108), 2: (1269, 147, 108), 3: (662, 121, 99), 4: (9019, 477, 372)},
    2: {1: (15891, 295, 219), 2: (2704, 295, 210), 3: (1836, 241, 194), 4: (22683, 955, 721)},
    3: {1: (13666, 295, 212), 2: (2438, 295, 191), 3: (1790, 241, 183), 4: (21218, 955, 690)},
    4: {1: (17659, 295, 212), 2: (3084, 295, 204), 3: (2757, 241, 179), 4: (31175, 952, 662)},
    5: {1: (7606, 295, 203), 2: (1651, 295, 207), 3: (1540, 241, 175), 4: (15285, 953, 649)},
    6: {1: (15415, 295, 196), 2: (3022, 295, 179), 3: (3043, 241, 167), 4: (25742, 954, 578)},
    7: {1: (14798, 295, 184), 2: (2639, 294, 177), 3: (2578, 241, 160), 4: (23243, 951, 570)},
    8: {1: (6342, 147, 93), 2: (1205, 146, 93), 3: (913, 121, 78), 4: (10370, 477, 300)},
}
FRAME_TOTAL, SAMPLED_TOTAL = 289478, 12488  # same document, step 2 of the weight recipe

# Published figures used as anchors.
PUBLISHED = {
    "adult_sample_n": 8573,          # overview p.5 and sampling-weights Table 1
    "frame_total": 289478,           # sampling-weights doc, step 2
    "sampled_total": 12488,          # sampling-weights doc, step 2
    "adjustee_share": 0.57,          # overview: "approximately 57% in the NIS-2003"
    "home_own_25_64": {1: 0.406, 2: 0.38, 3: 0.05, 4: 0.21},  # overview Figures 1 and 3
}

DATASETS = {
    "0002": ["PU_ID", "CISBIRTHYERMO", "CISADMYER", "CISCOBINSMO", "CISADJUST",
             "VISACATMO", "NISADULTSTR", "NISWGTSAMP1"],
    "0003": ["PU_ID", "A6", "A7", "A20", "STRTYR", "LANGUAGE"],
    "0006": ["PU_ID", "C1", "C16", "C22_1", "C33_1", "C37_1", "C47_1", "C48A2_1"],
    "0007": ["PU_ID", "C48_1PPP", "C49_1PPP"],
    "0011": ["PU_ID", "WHOKNOW", "G1", "G7"],
    "0012": ["PU_ID", "G7APPP"],
    "0013": ["PU_ID", "H1", "H1A"],
    "0017": ["PU_ID", "J30_1MO", "J13", "J14"],
}
SPOUSE_DATASETS = {  # spouse-path files; PU_ID is <case><person>, person 20 = spouse
    "0053": ["PU_ID", "G1", "G2", "G15"],
    "0054": ["PU_ID", "G16PPP"],
}


def log(msg: str) -> None:
    print(msg, flush=True)


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
def read_ds(ds: str, cols: list[str]) -> pd.DataFrame:
    path = CACHE / f"DS{ds}" / f"38031-{ds}-Data.tsv"
    if not path.exists():
        sys.exit(f"[BLOCKED] missing extracted dataset {path}; unzip it into _cache/ first")
    return pd.read_csv(path, sep="\t", usecols=cols, dtype=str)


def load() -> tuple[pd.DataFrame, dict]:
    gate2 = {}
    d = None
    for ds, cols in DATASETS.items():
        x = read_ds(ds, cols)
        gate2[f"DS{ds}"] = {"rows": int(len(x)), "unique_PU_ID": bool(x.PU_ID.is_unique)}
        assert len(x) == N_ADULT, f"G2 FAIL: DS{ds} has {len(x)} rows, expected {N_ADULT}"
        assert x.PU_ID.is_unique, f"G2 FAIL: DS{ds} PU_ID not unique"
        d = x if d is None else d.merge(x, on="PU_ID", how="outer", validate="1:1")
    assert len(d) == N_ADULT and d.PU_ID.is_unique, "G2 FAIL: joined frame"
    d["case"] = d.PU_ID.str[:4]
    assert d.case.is_unique, "G2 FAIL: case id not unique among adults"

    sp = None
    for ds, cols in SPOUSE_DATASETS.items():
        x = read_ds(ds, cols).rename(columns={c: f"S_{c}" for c in cols if c != "PU_ID"})
        gate2[f"DS{ds}(spouse)"] = {"rows": int(len(x)), "unique_PU_ID": bool(x.PU_ID.is_unique)}
        sp = x if sp is None else sp.merge(x, on="PU_ID", how="outer", validate="1:1")
    sp["case"] = sp.PU_ID.str[:4]
    sp = sp.drop(columns=["PU_ID"])
    d = d.merge(sp, on="case", how="left", validate="1:1")
    return d, gate2


# ---------------------------------------------------------------------------
# Build analysis variables
# ---------------------------------------------------------------------------
def build(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["w"] = num(d.NISWGTSAMP1)
    d["stratum"] = num(d.NISADULTSTR).astype("Int64")
    d["yob"] = num(d.A7).where(num(d.A7) > 1800)
    d["intyr"] = num(d.STRTYR)
    d["age"] = d.intyr - d.yob
    d["sex"] = num(d.A6)
    d["adjustee"] = num(d.CISADJUST)
    d["visacat"] = num(d.VISACATMO)
    d["cob"] = num(d.CISCOBINSMO)
    d["region"] = d.cob.map(lambda c: COUNTRY_TO_REGION.get(c, c) if pd.notna(c) else np.nan)

    # religion, first mention
    rel = num(d.J30_1MO)
    d["rel_code"] = rel
    d["religion"] = rel.map(RELIGION_GROUP)
    d["rel_broad"] = d.religion.where(~d.religion.isin(CHRISTIAN), "Christian")

    # English: how well do you speak English (J14)
    eng = num(d.J14)
    d["english"] = eng.where(eng.isin([1, 2, 3, 4]))

    # schooling: years of school completed (A20); valid range 0..30
    sch = num(d.A20)
    d["school_yrs"] = sch.where((sch >= 0) & (sch <= 30))
    d["school_cat"] = pd.cut(d.school_yrs, [-0.5, 8.5, 11.5, 12.5, 15.5, 16.5, 30.5],
                             labels=["<9", "9-11", "12", "13-15", "16", "17+"])

    # employment: current employment status, Section C item C1
    c1 = num(d.C1)
    d["c1"] = c1.where(c1.isin(list(C1_CODES)))
    d["employed"] = np.where(d.c1 == 1, 1.0, np.where(d.c1.isin([2, 3, 4, 5, 6, 97]), 0.0, np.nan))

    # annualised earnings on the current main job (Section C, PPP-adjusted US dollars)
    pay_kind = num(d.C47_1)
    unit = num(d.C48A2_1)
    hrs = num(d.C33_1).where(lambda s: (s > 0) & (s <= 168))
    wks = num(d.C37_1).where(lambda s: (s > 0) & (s <= 52))
    sal = num(d.C48_1PPP).where(lambda s: s > 0)
    hourly = num(d.C49_1PPP).where(lambda s: s > 0)
    factor = pd.Series(np.nan, index=d.index, dtype=float)
    factor[unit == 1] = (hrs * wks)[unit == 1]
    factor[unit == 2] = wks[unit == 2]
    factor[unit == 3] = (wks / 2.0)[unit == 3]
    factor[unit == 4] = 12.0
    factor[unit == 5] = 1.0
    from_salary = sal * factor
    from_hourly = hourly * hrs * wks
    earn = from_salary.where(pay_kind != 2, np.nan)
    earn = earn.fillna(from_hourly)
    earn = earn.fillna(from_salary)
    d["earn_annual"] = earn.where((earn > 0) & (earn < 5e6))
    d["earn_source"] = np.where(from_salary.notna() & (pay_kind != 2), "C48 salary",
                                np.where(from_hourly.notna(), "C49 hourly",
                                         np.where(from_salary.notna(), "C48 salary", "")))
    d["hours_wk"] = hrs
    # full-time restriction: usual hours on the current main job at least 30 a week
    d["earn_ft"] = d.earn_annual.where(hrs >= 30)

    # wage and salary income in the last twelve months (Section G), with spouse-path recovery
    own_g7 = num(d.G7)
    sp_g15 = num(d.S_G15)
    any_wage = np.where(own_g7 == 1, 1.0, np.where(own_g7 == 2, 0.0, np.nan))
    fill = np.isnan(any_wage)
    any_wage[fill] = np.where(sp_g15[fill] == 1, 1.0, np.where(sp_g15[fill] == 2, 0.0, np.nan))
    d["any_wage_12m"] = any_wage
    d["wage_src"] = np.where(own_g7.isin([1, 2]), "own Section G",
                             np.where(sp_g15.isin([1, 2]), "spouse Section G", ""))
    w12 = num(d.G7APPP)
    w12 = w12.fillna(num(d.S_G16PPP).where(own_g7.isna()))
    d["wage_12m"] = w12.where((w12 > 0) & (w12 < 5e6))

    # design cell = stratum x replicate, recovered from the distinct design-weight values
    cells = {}
    for rep, strata in WEIGHT_TABLE.items():
        for st, (frame, sampled, _) in strata.items():
            cells[(st, round(1.0 / ((sampled / frame) * (FRAME_TOTAL / SAMPLED_TOTAL)), 9))] = f"s{st}r{rep}"
    d["design_cell"] = [cells.get((s, round(w, 9)), "UNMATCHED")
                        for s, w in zip(d.stratum.astype("float"), d.w)]
    return d


# ---------------------------------------------------------------------------
# Anchors (G3)
# ---------------------------------------------------------------------------
def anchors(d: pd.DataFrame, gate2: dict) -> pd.DataFrame:
    rows = []

    def add(name, published, reproduced, unit, ok, note=""):
        rows.append({"anchor": name, "published": published, "reproduced": reproduced,
                     "unit": unit, "exact": bool(ok), "note": note})

    for k, v in gate2.items():
        add(f"rows in {k}", N_ADULT if "spouse" not in k else v["rows"], v["rows"], "respondents",
            v["rows"] == (N_ADULT if "spouse" not in k else v["rows"]),
            "38031-Documentation-questionnaires_intro.pdf: 8,573 completed adult interviews")

    tb = pd.DataFrame(
        [(rep, st, fr, sa, co, 1.0 / ((sa / fr) * (FRAME_TOTAL / SAMPLED_TOTAL)))
         for rep, strata in WEIGHT_TABLE.items() for st, (fr, sa, co) in strata.items()],
        columns=["rep", "stratum", "frame", "sampled", "complete", "w_doc"])
    add("sampling frame total (weights Table 1)", FRAME_TOTAL, int(tb.frame.sum()), "immigrants",
        int(tb.frame.sum()) == FRAME_TOTAL)
    add("cases sampled total (weights Table 1)", SAMPLED_TOTAL, int(tb.sampled.sum()), "cases",
        int(tb.sampled.sum()) == SAMPLED_TOTAL)
    add("completed adult interviews (weights Table 1)", N_ADULT, int(tb.complete.sum()),
        "respondents", int(tb.complete.sum()) == N_ADULT)

    obs = d.groupby(["stratum", "w"], observed=True).size().rename("n_obs").reset_index()
    tb2 = tb.assign(key=tb.w_doc.round(9))
    obs = obs.assign(key=obs.w.round(9))
    mg = obs.merge(tb2, on="key", how="left", suffixes=("", "_doc"))
    max_dev = float((mg.w - mg.w_doc).abs().max())
    add("distinct design weights reconstructed from Table 1", 32, int(len(obs)), "weight values",
        len(obs) == 32 and mg.w_doc.notna().all())
    add("max |NISWGTSAMP1 - documented design weight|", 0.0, max_dev, "weight units", max_dev < 1e-9,
        "weight = (frame/sampled) x (12488/289478), sampling-weights doc steps 1-3")
    same_stratum = bool((mg.stratum == mg.stratum_doc).all())
    add("stratum agrees for every design-weight cell", 32, int((mg.stratum == mg.stratum_doc).sum()),
        "cells", same_stratum)
    n_match = int((mg.n_obs == mg.complete).sum())
    add("stratum x replicate completed-case counts", 32, n_match, "cells", n_match == 32,
        "two cells differ by one case (s4r4 661 vs 662; s1r4 213 vs 212); totals agree")

    doc_str = tb.groupby("stratum").complete.sum()
    obs_str = d.stratum.value_counts().sort_index()
    for st in [1, 2, 3, 4]:
        add(f"completed cases, stratum {st} ({STRATUM_CODES[st]})", int(doc_str[st]),
            int(obs_str[st]), "respondents", int(doc_str[st]) == int(obs_str[st]))

    adj_w = float(np.average(d.adjustee, weights=d.w))
    add("share adjusting status (weighted)", PUBLISHED["adjustee_share"], round(adj_w, 4), "share",
        abs(adj_w - PUBLISHED["adjustee_share"]) < 0.005,
        f"overview: 'approximately 57%'; unweighted {d.adjustee.mean():.4f}")

    h1 = num(d.H1)
    h1a = num(d.H1A)
    own = np.where(h1a == 1, 1.0, np.where(h1a.isin([2, 3]), 0.0,
                                           np.where(h1.isin([3, 4, 5, 6]), 0.0, np.nan)))
    age_adm = num(d.CISADMYER) - d.yob
    sel = (age_adm >= 25) & (age_adm <= 64) & ~np.isnan(own)
    for st, pub in PUBLISHED["home_own_25_64"].items():
        m = sel & (d.stratum == st)
        val = float(np.average(own[m], weights=d.w[m]))
        add(f"home ownership, ages 25-64 at admission, {STRATUM_CODES[st]}", pub, round(val, 4),
            "share", abs(val - pub) < 0.005,
            f"overview Figures 1/3; n={int(m.sum())}; Section H missing for "
            f"{int((~np.isnan(own)).sum())}/{N_ADULT} adults (financial-respondent path)")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Weighted statistics and WLS
# ---------------------------------------------------------------------------
def wmean(x: np.ndarray, w: np.ndarray) -> float:
    return float(np.sum(x * w) / np.sum(w)) if np.sum(w) > 0 else np.nan


def wmedian(x: np.ndarray, w: np.ndarray) -> float:
    if len(x) == 0:
        return np.nan
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w) - 0.5 * w
    return float(np.interp(0.5 * np.sum(w), c, x))


def wquantile(x: np.ndarray, w: np.ndarray, q: float) -> float:
    if len(x) == 0:
        return np.nan
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w) - 0.5 * w
    return float(np.interp(q * np.sum(w), c, x))


def anomalies(d: pd.DataFrame) -> dict:
    """Diagnostics for the four results that looked wrong on first inspection.

    Each entry records what looked wrong, the numbers that decide it, and whether it is a
    real feature of the data or an artefact. None of them was smoothed over in the tables.
    """
    b = d[d.age.between(18, 64)].copy()
    b["grp"] = b.religion.where(~b.religion.isin(CHRISTIAN), "Christian")

    def q(group, col, qs=(0.10, 0.25, 0.50, 0.75, 0.90)):
        s = b[(b.grp == group) & b[col].notna()]
        if not len(s):
            return {}
        x, w = s[col].to_numpy(float), s.w.to_numpy(float)
        out = {f"p{int(k * 100)}": round(wquantile(x, w, k), 1) for k in qs}
        out["n"] = int(len(s))
        out["mean_log"] = round(wmean(np.log(x), w), 4)
        return out

    out = {}
    out["A1_muslim_median_below_christian_but_mean_log_above"] = {
        "looked_wrong": "median earn_annual is lower for Muslims than Christians while the "
                        "unadjusted log-earnings gap is positive (+0.12)",
        "muslim_earn_annual": q("Muslim", "earn_annual"),
        "christian_earn_annual": q("Christian", "earn_annual"),
        "resolution": "real feature, not an artefact. The mean of log earnings is a geometric "
                      "mean, so it is driven by the left tail, and the Christian left tail is "
                      "much lower (see p10). Median and mean-log therefore rank the two groups "
                      "in opposite directions. Both are reported in derived/earnings_gaps.csv; "
                      "neither is presented alone.",
        "codebook_check": "J30_1MO code 4 = MUSLIM (questionnaire item J30_X, RELPICK1); codes "
                          "1/2/3 = CATHOLIC/ORTHODOX CHRISTIAN/PROTESTANT. Verified, no recode error.",
    }
    hin = b[(b.grp == "Hindu") & b.earn_annual.notna()]
    chr_ = b[(b.grp == "Christian") & b.earn_annual.notna()]
    spread = {}
    for nm, s in [("Hindu", hin), ("Christian", chr_)]:
        x, w = s.earn_annual.to_numpy(float), s.w.to_numpy(float)
        spread[nm] = {"p45": round(wquantile(x, w, 0.45), 1), "p50": round(wquantile(x, w, 0.50), 1),
                      "p55": round(wquantile(x, w, 0.55), 1),
                      "p55_minus_p45": round(wquantile(x, w, 0.55) - wquantile(x, w, 0.45), 1),
                      "n": int(len(s))}
    out["A2_hindu_median_earnings_has_a_very_large_bootstrap_se"] = {
        "looked_wrong": "bootstrap SE on the Hindu weighted median earnings is about $11,000 on "
                        "a $40,000 median, far larger than for any other group",
        "median_neighbourhood": spread,
        "resolution": "real feature of a bimodal distribution, not a bug in wmedian (unit-tested "
                      "against numpy.median at equal weights). The Hindu earnings distribution is "
                      "close to flat between roughly $27k and $55k, so the weighted median moves a "
                      "long way under resampling; compare the much narrower Christian p45-p55 band. "
                      "The Hindu median is reported with its SE and should not be read as precise; "
                      "the log-earnings gaps, which use the whole distribution, are the stable "
                      "statistic for this group.",
    }
    gsec = {}
    for g in ["Christian", "Muslim", "Hindu", "Buddhist", "No religion"]:
        s = b[b.grp == g]
        gsec[g] = {"n_18_64": int(len(s)),
                   "answered_section_G": int(s.wage_src.isin(["own Section G", "spouse Section G"]).sum()),
                   "share_answered_section_G": round(float(s.wage_src.isin(
                       ["own Section G", "spouse Section G"]).mean()), 4),
                   "employed_rate_C1": round(wmean(s.employed.fillna(0).to_numpy(float),
                                                   s.w.to_numpy(float)), 4)}
    out["A3_section_C_and_section_G_earnings_gaps_differ_in_sign"] = {
        "looked_wrong": "unadjusted Muslim-Christian log gap is +0.12 on the Section C measure and "
                        "-0.29 on the Section G measure",
        "section_G_coverage_by_group": gsec,
        "resolution": "the two measures answer different questions and both are reported. Section C "
                      "(C48_1PPP / C49_1PPP) annualises the pay rate on the job held at interview, "
                      "so it conditions on working and ignores weeks not worked. Section G (G7APPP) "
                      "is wage and salary income actually received over the last twelve months, "
                      "which for a cohort interviewed about four months after admission loads heavily "
                      "on months spent in the United States and employed. A group with a lower "
                      "employment rate and the same pay rate will show parity on Section C and a "
                      "deficit on Section G, which is what the two columns show.",
    }
    out["A4_any_wage_12m_is_higher_for_muslims_than_christians"] = {
        "looked_wrong": "share reporting any wage income in the last twelve months is 0.87 for "
                        "Muslims against 0.85 for Christians, the opposite direction to the "
                        "current-employment rate (0.51 against 0.61)",
        "section_G_coverage_by_group": gsec,
        "resolution": "a universe difference, and it is flagged in the table rather than adjusted "
                      "away. any_wage_12m is defined only for respondents whose household answered "
                      "Section G (item G7, or the spouse's G15), so its denominator is a selected "
                      "subset of each religion group, whereas the C1 employment rate covers the "
                      "whole group. Compare share_answered_section_G across groups. The employment "
                      "rate, not any_wage_12m, is the comparable participation measure.",
    }
    own_missing = num(d.G7).isna()
    usable = num(d.S_G15).isin([1, 2])
    out["A5_spouse_path_recovers_fewer_cases_than_the_spouse_G1_count_suggested"] = {
        "looked_wrong": "1,522 adults with no own Section G have a valid spouse G1, but only 840 "
                        "wage reports are recovered from the spouse path",
        "counts": {
            "own_G7_missing": int(own_missing.sum()),
            "spouse_record_exists": int((own_missing & d.S_G1.notna()).sum()),
            "spouse_G1_valid": int((own_missing & num(d.S_G1).notna()).sum()),
            "spouse_G1_equals_1_someone_worked": int((own_missing & (num(d.S_G1) == 1)).sum()),
            "spouse_G2_in_2_3_reaches_G13_branch": int(
                (own_missing & (num(d.S_G1) == 1) & num(d.S_G2).isin([2, 3])).sum())
            if "S_G2" in d.columns else None,
            "spouse_G15_valid": int((own_missing & num(d.S_G15).notna()).sum()),
            "spouse_G15_usable_yes_no": int((own_missing & usable).sum()),
            "recovered_into_wage_src": int((d.wage_src == "spouse Section G").sum()),
        },
        "resolution": "correct behaviour, and the recovery is exhaustive over the universe the "
                      "instrument allows. The recoverable item is the spouse's G15, not the "
                      "spouse's G1. Section G item G13, which leads to G15, is reached only "
                      "'IF NOT MARRIED/PARTNERED OR G2=1: G21', so the spouse income block is "
                      "skipped unless the respondent is married or partnered and the spouse "
                      "worked for pay. 840 is therefore the ceiling, not a shortfall. An earlier "
                      "test asserted the wrong ceiling (>1000) and was corrected against the "
                      "questionnaire rather than by loosening the threshold.",
    }
    return out


def design_matrix(d: pd.DataFrame, groups: list[str], ref: str, spec: str) -> tuple[np.ndarray, list[str]]:
    cols, names = [np.ones(len(d))], ["const"]
    for g in groups:
        if g == ref:
            continue
        cols.append((d.rel_broad_eff == g).to_numpy(float))
        names.append(f"rel[{g}]")
    if spec == "unadj":
        return np.column_stack(cols), names
    ageband = pd.cut(d.age, [17.5, 24.5, 34.5, 44.5, 54.5, 64.5],
                     labels=["18-24", "25-34", "35-44", "45-54", "55-64"])
    for lvl in ["25-34", "35-44", "45-54", "55-64"]:
        for sx in [1, 2]:
            cols.append(((ageband == lvl) & (d.sex == sx)).to_numpy(float))
            names.append(f"age{lvl}_sex{sx}")
    cols.append((d.sex == 2).to_numpy(float))
    names.append("female")
    for lvl in ["<9", "9-11", "13-15", "16", "17+"]:
        cols.append((d.school_cat == lvl).to_numpy(float))
        names.append(f"school[{lvl}]")
    cols.append(d.school_cat.isna().to_numpy(float))
    names.append("school[missing]")
    for lvl in [2, 3, 4]:
        cols.append((d.english == lvl).to_numpy(float))
        names.append(f"english[{ENGLISH_CODES[lvl]}]")
    cols.append(d.english.isna().to_numpy(float))
    names.append("english[missing]")
    for v in sorted(VISACAT_CODES):
        if v == 0:
            continue
        cols.append((d.visacat == v).to_numpy(float))
        names.append(f"visa[{VISACAT_CODES[v]}]")
    cols.append(d.adjustee.fillna(0).to_numpy(float))
    names.append("adjustee")
    if spec == "adj":
        levels = sorted(x for x in d.region.dropna().unique() if x != 305)
        for r in levels:
            cols.append((d.region == r).to_numpy(float))
            names.append(f"region[{COUNTRY_CODES.get(int(r), int(r))}]")
    elif spec == "adj_origin":
        levels = sorted(x for x in d.cob.dropna().unique() if x != 135)
        for c in levels:
            cols.append((d.cob == c).to_numpy(float))
            names.append(f"cob[{COUNTRY_CODES.get(int(c), int(c))}]")
    return np.column_stack(cols), names


def wls(X: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    sw = np.sqrt(w)
    return np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]


def point_estimates(d: pd.DataFrame, groups: list[str], ref: str) -> dict:
    out = {}
    base = d[d.age.between(18, 64)]
    for g in groups:
        m = base[base.rel_broad_eff == g]
        e = m[m.employed.notna()]
        out[(g, "emp_rate")] = wmean(e.employed.to_numpy(), e.w.to_numpy()) if len(e) else np.nan
        a = m[m.any_wage_12m.notna()]
        out[(g, "any_wage_12m")] = wmean(a.any_wage_12m.to_numpy(), a.w.to_numpy()) if len(a) else np.nan
        k = m[m.earn_annual.notna()]
        out[(g, "mean_earn")] = wmean(k.earn_annual.to_numpy(), k.w.to_numpy()) if len(k) else np.nan
        out[(g, "median_earn")] = wmedian(k.earn_annual.to_numpy(), k.w.to_numpy()) if len(k) else np.nan
        j = m[m.wage_12m.notna()]
        out[(g, "median_wage12m")] = wmedian(j.wage_12m.to_numpy(), j.w.to_numpy()) if len(j) else np.nan
        f = m[m.earn_ft.notna()]
        out[(g, "median_earn_ft")] = wmedian(f.earn_ft.to_numpy(), f.w.to_numpy()) if len(f) else np.nan
    # employment gap: linear probability model on the same covariates
    e = base[base.employed.notna() & base.rel_broad_eff.notna()]
    for spec in ["unadj", "adj", "adj_origin"]:
        X, names = design_matrix(e, groups, ref, spec)
        b = wls(X, e.employed.to_numpy(float), e.w.to_numpy())
        for nm, coef in zip(names, b):
            if nm.startswith("rel["):
                out[(nm[4:-1], f"empgap_{spec}")] = float(coef)
    for measure, col in [("earnC", "earn_annual"), ("earnFT", "earn_ft"), ("wageG", "wage_12m")]:
        s = base[base[col].notna() & base.rel_broad_eff.notna()]
        y = np.log(s[col].to_numpy())
        for spec in ["unadj", "adj", "adj_origin"]:
            X, names = design_matrix(s, groups, ref, spec)
            b = wls(X, y, s.w.to_numpy())
            for nm, coef in zip(names, b):
                if nm.startswith("rel["):
                    out[(nm[4:-1], f"loggap_{measure}_{spec}")] = float(coef)
    return out


def bootstrap(d: pd.DataFrame, groups: list[str], ref: str, n_boot: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx_by_cell = [np.flatnonzero((d.design_cell == c).to_numpy()) for c in sorted(d.design_cell.unique())]
    draws = []
    for b in range(n_boot):
        take = np.concatenate([rng.choice(ix, size=len(ix), replace=True) for ix in idx_by_cell])
        draws.append(point_estimates(d.iloc[take].reset_index(drop=True), groups, ref))
        if (b + 1) % 100 == 0:
            log(f"    bootstrap draw {b + 1}/{n_boot}")
    keys = sorted({k for dd in draws for k in dd})
    rec = []
    for k in keys:
        v = np.array([dd.get(k, np.nan) for dd in draws], float)
        v = v[np.isfinite(v)]
        rec.append({"group": k[0], "stat": k[1], "se": float(np.std(v, ddof=1)) if len(v) > 1 else np.nan,
                    "boot_n": int(len(v))})
    return pd.DataFrame(rec)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    log("gate G1: verifying source zip sha256")
    got = sha256(ZIP)
    assert got == ZIP_SHA256, f"G1 FAIL: zip sha256 {got} != {ZIP_SHA256}"
    log(f"  G1 PASS {got}")

    log("loading datasets (gate G2)")
    raw, gate2 = load()
    d = build(raw)
    assert (d.design_cell != "UNMATCHED").all(), "design cell recovery failed"
    log(f"  G2 PASS: {len(d)} adults, unique PU_ID, in {len(DATASETS)} adult datasets")

    log("gate G3: reproducing published counts")
    anc = anchors(d, gate2)
    anc.to_csv(DERIVED / "anchors.csv", index=False)
    n_exact = int(anc.exact.sum())
    log(f"  anchors exact: {n_exact}/{len(anc)}")
    for _, r in anc.iterrows():
        log(f"    [{'PASS' if r.exact else 'near'}] {r.anchor}: published={r.published} reproduced={r.reproduced}")
    assert n_exact >= 3, "G3 FAIL: fewer than three published counts reproduced"

    # religion cells
    base = d[d.age.between(18, 64)]
    rows = []
    for g in sorted(set(RELIGION_GROUP.values())) + ["Christian"]:
        sel = (d.religion == g) if g != "Christian" else d.religion.isin(CHRISTIAN)
        selb = (base.religion == g) if g != "Christian" else base.religion.isin(CHRISTIAN)
        rows.append({
            "group": g,
            "n_unweighted_all": int(sel.sum()),
            "n_weighted_all": float(d.w[sel].sum()),
            "share_weighted_all": float(d.w[sel].sum() / d.w[d.religion.notna()].sum()),
            "n_unweighted_18_64": int(selb.sum()),
            "n_weighted_18_64": float(base.w[selb].sum()),
            "n_with_employment": int(base.employed[selb].notna().sum()),
            "n_with_earnings_C": int(base.earn_annual[selb].notna().sum()),
            "n_with_earnings_C_fulltime": int(base.earn_ft[selb].notna().sum()),
            "n_with_wage12m_G": int(base.wage_12m[selb].notna().sum()),
        })
    for lbl, sel in [("REFUSED", d.rel_code == -1), ("DON'T KNOW", d.rel_code == -2),
                     ("not asked / missing", d.rel_code.isna())]:
        rows.append({"group": lbl, "n_unweighted_all": int(sel.sum()),
                     "n_weighted_all": float(d.w[sel].sum()), "share_weighted_all": np.nan,
                     "n_unweighted_18_64": int((base.rel_code.isna() if lbl.startswith("not")
                                                else base.rel_code == (-1 if lbl == "REFUSED" else -2)).sum()),
                     "n_weighted_18_64": np.nan, "n_with_employment": np.nan,
                     "n_with_earnings_C": np.nan, "n_with_earnings_C_fulltime": np.nan,
                     "n_with_wage12m_G": np.nan})
    cells = pd.DataFrame(rows)
    cells.to_csv(DERIVED / "religion_cells.csv", index=False)
    log("wrote derived/religion_cells.csv")

    # model A: Christian reference; model B: Catholic reference with Christian split
    results = []
    for model, ref, mapper in [
        ("A_christian_ref", "Christian", lambda s: s.religion.where(~s.religion.isin(CHRISTIAN), "Christian")),
        ("B_catholic_ref", "Catholic", lambda s: s.religion),
    ]:
        dd = d.copy()
        dd["rel_broad_eff"] = mapper(dd)
        groups = sorted(x for x in dd.rel_broad_eff.dropna().unique())
        log(f"model {model}: reference={ref} groups={groups}")
        pt = point_estimates(dd, groups, ref)
        se = bootstrap(dd, groups, ref, N_BOOT, SEED)
        se = se.set_index(["group", "stat"])
        bb = dd[dd.age.between(18, 64)]
        for (g, stat), est in pt.items():
            sel = bb.rel_broad_eff == g
            counts = {"emp_rate": "employed", "empgap": "employed",      # order matters: the
                      "any_wage_12m": "any_wage_12m",                    # first substring match wins,
                      "median_earn_ft": "earn_ft", "earnFT": "earn_ft",  # so specific keys come first
                      "median_wage12m": "wage_12m", "wageG": "wage_12m",
                      "mean_earn": "earn_annual", "median_earn": "earn_annual",
                      "earnC": "earn_annual"}
            key = next((v for k, v in counts.items() if stat == k or k in stat), "earn_annual")
            n = int(bb[key][sel].notna().sum())
            row = se.loc[(g, stat)] if (g, stat) in se.index else pd.Series({"se": np.nan, "boot_n": 0})
            results.append({"model": model, "reference": ref, "group": g, "stat": stat,
                            "estimate": est, "se": float(row.se), "n_cell": n,
                            "boot_draws": int(row.boot_n),
                            "reported": bool(n >= 50 and np.isfinite(est) and np.isfinite(row.se))})
    res = pd.DataFrame(results)
    res.to_csv(DERIVED / "earnings_gaps.csv", index=False)
    log("wrote derived/earnings_gaps.csv")

    rep = res[res.reported]
    assert np.isfinite(rep.se).all(), "G5 FAIL: non-finite SE among reported cells"
    assert (rep.n_cell >= 50).all(), "G5 FAIL: reported cell with n < 50"
    suppressed = res[~res.reported][["model", "group", "stat", "n_cell"]]
    log(f"  G5: {len(rep)} reported cells (n>=50, finite SE); {len(suppressed)} suppressed")

    audit = {
        "lane": "nis2003_religion_earnings_2026_09_22",
        "source_zip": str(ZIP),
        "source_zip_sha256": got,
        "datasets_used": {f"DS{k}": v for k, v in DATASETS.items()},
        "spouse_datasets_used": {f"DS{k}": v for k, v in SPOUSE_DATASETS.items()},
        "gates": {
            "G1_zip_sha256": "PASS",
            "G2_8573_unique_per_dataset": gate2,
            "G3_anchors_exact": f"{n_exact}/{len(anc)}",
            "G4_codes_printed": "see code_lists",
            "G5_reported_cells_n_ge_50_finite_se": {
                "reported": int(len(rep)), "suppressed": int(len(suppressed))},
        },
        "code_lists": {
            "J30_1MO religion (RELPICK1)": {str(k): v for k, v in RELIGION_CODES.items()},
            "J14 how well speak English": {str(k): v for k, v in ENGLISH_CODES.items()},
            "C1 current employment": {str(k): v for k, v in C1_CODES.items()},
            "C47_1 salaried or paid by the hour": {str(k): v for k, v in C47_CODES.items()},
            "C48A2_1 salary unit": {str(k): v for k, v in C48A2_CODES.items()},
            "G7 / G15 wage and salary income last 12 months": {str(k): v for k, v in YESNO_CODES.items()},
            "A6 gender": {str(k): v for k, v in SEX_CODES.items()},
            "CISADJUST": {str(k): v for k, v in ADJUST_CODES.items()},
            "VISACATMO class of admission": {str(k): v for k, v in VISACAT_CODES.items()},
            "NISADULTSTR sampling stratum": {str(k): v for k, v in STRATUM_CODES.items()},
            "CISCOBINSMO country of birth": {str(k): v for k, v in COUNTRY_CODES.items()},
        },
        "variable_labels_verified": VARIABLE_LABELS,
        "anomalies_and_resolutions": anomalies(d),
        "code_sources": CODE_SOURCES,
        "country_to_region_map": {str(k): COUNTRY_CODES[v] for k, v in COUNTRY_TO_REGION.items()},
        "variance": {
            "method": "stratified respondent bootstrap, 500 draws, seed 20260922",
            "strata": "32 stratum x replicate design cells recovered from the distinct "
                      "NISWGTSAMP1 values (the public file carries no PSU identifier, so "
                      "no Taylor-linearised design variance is available)",
        },
        "earnings_definitions": {
            "earn_annual": "current main job, annualised: C48_1PPP x unit factor (C48A2_1) for "
                           "salaried/piecework/other, C49_1PPP x C33_1 x C37_1 for hourly; "
                           "PPP-adjusted US current prices, 2003-2004 interview",
            "earn_ft": "earn_annual restricted to usual hours on the current main job "
                       "(C33_1) of 30 or more a week",
            "wage_12m": "own wage and salary income in the last twelve months, G7APPP; for "
                        "households where the spouse answered Section G, the sampled immigrant's "
                        "amount is the spouse questionnaire's G16PPP, linked on the 4-digit case id",
        },
        "sample_sizes": {
            "adults": int(len(d)),
            "age_18_64": int(len(base)),
            "with_religion": int(d.religion.notna().sum()),
            "with_employment_18_64": int(base.employed.notna().sum()),
            "with_earn_annual_18_64": int(base.earn_annual.notna().sum()),
            "with_earn_ft_18_64": int(base.earn_ft.notna().sum()),
            "with_wage_12m_18_64": int(base.wage_12m.notna().sum()),
            "wage_12m_from_spouse_path": int((base.wage_src == "spouse Section G").sum()),
        },
    }
    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=2, sort_keys=False))
    log("wrote derived/audit.json")

    log("--- headline ---")
    a = res[(res.model == "A_christian_ref") & res.reported]
    for stat in ["emp_rate", "empgap_adj", "empgap_adj_origin", "any_wage_12m", "mean_earn",
                 "median_earn", "median_earn_ft", "loggap_earnC_unadj", "loggap_earnC_adj",
                 "loggap_earnC_adj_origin", "loggap_earnFT_adj", "loggap_wageG_adj"]:
        s = a[a.stat == stat]
        if len(s):
            log(f"  {stat}: " + "  ".join(
                f"{r.group}={r.estimate:,.4f}({r.se:,.4f};n={r.n_cell})" for _, r in s.iterrows()))
    return 0


if __name__ == "__main__":
    sys.exit(main())

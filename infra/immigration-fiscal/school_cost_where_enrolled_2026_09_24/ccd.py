"""NCES Common Core of Data membership counts by LEA (2023-24) and by school (2021-22), cached.

The long membership files carry several overlapping totals; each count here comes from exactly one
TOTAL_INDICATOR so no pupil is counted twice. K-12 means kindergarten, grades 1-12 and ungraded;
pre-kindergarten, grade 13 and adult education are excluded (the account's pupils are public K-12).
A blank STUDENT_COUNT is missing, never zero (DMS_FLAG says so).
"""
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
LEA_2324 = Path("/Users/alien/research-data/immigration-fiscal/data/external/nces_ccd/ccd_lea_052_2324_l_1a_073124.csv")
SCH_2122 = CACHE / "ccd_sch_052_2122_l_1a_071722.zip"
K12 = {"Kindergarten", "Ungraded"} | {f"Grade {g}" for g in range(1, 13)}
SET_A = "Category Set A - By Race/Ethnicity; Sex; Grade"
BY_GRADE = "Subtotal 4 - By Grade"
UNIT_TOTAL_NO_AE = "Derived - Education Unit Total minus Adult Education Count"
RACE_SEX_NO_AE = "Derived - Subtotal by Race/Ethnicity and Sex minus Adult Education Count"
UNIT_TOTAL = "Education Unit Total"
HISPANIC = "Hispanic/Latino"


def _aggregate(chunks, key):
    parts = {"k12_all": [], "k12_hisp": [], "tot_all": [], "tot_hisp": [], "pk_all": [], "pk_hisp": [], "unit_total": []}
    for c in chunks:
        c = c[c.STUDENT_COUNT.notna()]
        ti, grade = c.TOTAL_INDICATOR, c.GRADE
        g = c[(ti == BY_GRADE)]
        parts["k12_all"].append(g[g.GRADE.isin(K12)].groupby(key).STUDENT_COUNT.sum())
        parts["pk_all"].append(g[g.GRADE.eq("Pre-Kindergarten")].groupby(key).STUDENT_COUNT.sum())
        a = c[(ti == SET_A) & c.RACE_ETHNICITY.eq(HISPANIC)]
        parts["k12_hisp"].append(a[a.GRADE.isin(K12)].groupby(key).STUDENT_COUNT.sum())
        parts["pk_hisp"].append(a[a.GRADE.eq("Pre-Kindergarten")].groupby(key).STUDENT_COUNT.sum())
        parts["tot_all"].append(c[ti == UNIT_TOTAL_NO_AE].groupby(key).STUDENT_COUNT.sum())
        parts["tot_hisp"].append(c[(ti == RACE_SEX_NO_AE) & c.RACE_ETHNICITY.eq(HISPANIC)].groupby(key).STUDENT_COUNT.sum())
        parts["unit_total"].append(c[ti == UNIT_TOTAL].groupby(key).STUDENT_COUNT.sum())
        del grade
    out = pd.concat({k: pd.concat(v).groupby(level=0).sum() for k, v in parts.items()}, axis=1)
    return out


def lea_2324():
    """Per LEAID: K-12 and total membership, all pupils and Hispanic, SY 2023-24 (fall 2023)."""
    cache = CACHE / "ccd_lea_2324_counts.csv"
    if cache.exists():
        return pd.read_csv(cache, dtype={"LEAID": str, "FIPST": str})
    cols = ["FIPST", "LEAID", "GRADE", "RACE_ETHNICITY", "STUDENT_COUNT", "TOTAL_INDICATOR"]
    reader = pd.read_csv(LEA_2324, usecols=cols, chunksize=1_000_000, dtype={"LEAID": str, "FIPST": str})
    fips = {}

    def chunks():
        for c in reader:
            fips.update(dict(zip(c.LEAID, c.FIPST)))
            yield c
    out = _aggregate(chunks(), "LEAID").reset_index().rename(columns={"index": "LEAID"})
    out["FIPST"] = out.LEAID.map(fips)
    out.to_csv(cache, index=False, lineterminator="\n")
    return pd.read_csv(cache, dtype={"LEAID": str, "FIPST": str})


def school_2122():
    """Per NCESSCH: membership, all pupils and Hispanic, SY 2021-22 (matches SLFS FY 2022)."""
    cache = CACHE / "ccd_sch_2122_counts.csv"
    if cache.exists():
        return pd.read_csv(cache, dtype={"NCESSCH": str, "LEAID": str, "FIPST": str})
    if not SCH_2122.exists():
        raise FileNotFoundError(SCH_2122)
    # The inner CSV zip uses Deflate64, which Python's zipfile cannot read: stream it through unzip.
    inner = CACHE / "ccd_SCH_052_2122_l_1a_071722_CSV.zip"
    if not inner.exists():
        subprocess.run(["unzip", "-o", "-q", str(SCH_2122), inner.name, "-d", str(CACHE)], check=True)
    listing = subprocess.run(["unzip", "-Z1", str(inner)], capture_output=True, text=True, check=True).stdout.split()
    if listing != ["ccd_SCH_052_2122_l_1a_071722.csv"]:
        raise SystemExit(f"[BLOCKED] unexpected members in {inner.name}: {listing}")
    cols = ["FIPST", "LEAID", "NCESSCH", "GRADE", "RACE_ETHNICITY", "STUDENT_COUNT", "TOTAL_INDICATOR"]
    lea = {}
    proc = subprocess.Popen(["unzip", "-p", str(inner), listing[0]], stdout=subprocess.PIPE)
    reader = pd.read_csv(proc.stdout, usecols=cols, chunksize=2_000_000,
                         dtype={"LEAID": str, "FIPST": str, "NCESSCH": str})

    def chunks():
        for c in reader:
            lea.update(dict(zip(c.NCESSCH, zip(c.LEAID, c.FIPST))))
            yield c
    out = _aggregate(chunks(), "NCESSCH").reset_index().rename(columns={"index": "NCESSCH"})
    if proc.wait() != 0:
        raise SystemExit("[BLOCKED] unzip failed while streaming the CCD school file")
    out["LEAID"] = out.NCESSCH.map(lambda s: lea[s][0])
    out["FIPST"] = out.NCESSCH.map(lambda s: lea[s][1])
    out.to_csv(cache, index=False, lineterminator="\n")
    return pd.read_csv(cache, dtype={"NCESSCH": str, "LEAID": str, "FIPST": str})


def lea_directory_2324():
    z = Path("/Users/alien/research-data/immigration-fiscal/data/external/nces_ccd/ccd_lea_029_2324_w_1a_073124.zip")
    with zipfile.ZipFile(z) as f:
        d = pd.read_csv(f.open("ccd_lea_029_2324_w_1a_073124.csv"), dtype=str,
                        usecols=["LEAID", "LEA_NAME", "LEA_TYPE", "LEA_TYPE_TEXT", "CHARTER_LEA", "SY_STATUS"])
    return d


def el_1819():
    z = HERE.parents[2] / "sources/immigration-fiscal/data/external/stage5_net_negative/nces/ccd_lea_141_1819_english_learners.zip"
    with zipfile.ZipFile(z) as f:
        d = pd.read_csv(f.open("ccd_lea_141_1819_l_1a_091019.csv"), dtype={"LEAID": str, "FIPST": str})
    d["LEP_COUNT"] = pd.to_numeric(d.LEP_COUNT, errors="coerce")
    return d[["LEAID", "FIPST", "LEP_COUNT", "DMS_FLAG"]]


if __name__ == "__main__":
    lea = lea_2324()
    print(lea[["k12_all", "k12_hisp", "tot_all", "tot_hisp", "pk_all", "pk_hisp", "unit_total"]].sum().to_string())

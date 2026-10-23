"""The public K-12 school universe, 2023-24: NCES EDGE points joined to CCD directory, virtual flag
and membership.

Universe: 50 states and DC; operating schools (CCD SY_STATUS open, new, added, changed boundary or
reopened); all four school types; membership from CCD 052 (K-12 = kindergarten, grades 1-12 and
ungraded, all pupils and Hispanic), aggregated with the same TOTAL_INDICATOR rules as the where-
enrolled lane (`school_cost_where_enrolled_2026_09_24/ccd.py::_aggregate`, imported, one
definition). The 2.35 GB membership CSV is streamed from its zip in chunks and the per-school
counts cached in _cache/nces/sch_2324_counts.csv.

Exclusively virtual schools (CCD 129 VIRTUAL = FULLVIRTUAL) and schools with no K-12 pupils are
flagged, not dropped; build.py decides what counts.
"""
import importlib.util
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
NCES = HERE / "_cache" / "nces"
EDGE_ZIP = NCES / "EDGE_GEOCODE_PUBLICSCH_2324.zip"
EDGE_TXT = "EDGE_GEOCODE_PUBLICSCH_2324/EDGE_GEOCODE_PUBLICSCH_2324.TXT"
EDGE_COLS = ["NCESSCH", "LEAID", "NAME", "OPSTFIPS", "STREET", "CITY", "STATE", "ZIP", "STFIP", "CNTY", "NMCNTY",
             "LOCALE", "LAT", "LON", "CBSA", "NMCBSA", "CBSATYPE", "CSA", "NMCSA", "CD", "SLDL", "SLDU", "SCHOOLYEAR"]
DIR_ZIP, DIR_CSV = NCES / "ccd_sch_029_2324_w_1a_073124.zip", "ccd_sch_029_2324_w_1a_073124.csv"
CHR_ZIP, CHR_CSV = NCES / "ccd_sch_129_2324_w_1a_073124.zip", "ccd_sch_129_2324_w_1a_073124.csv"
MEM_ZIP, MEM_CSV = NCES / "ccd_sch_052_2324_l_1a_073124.zip", "ccd_sch_052_2324_l_1a_073124.csv"
COUNTS = NCES / "sch_2324_counts.csv"
OPERATING = {"1", "3", "4", "5", "8"}     # open, new, added, changed boundary/agency, reopened
SIBLING = HERE.parent / "school_cost_where_enrolled_2026_09_24" / "ccd.py"


def _unzip(zpath, member):
    return subprocess.Popen(["unzip", "-p", str(zpath), member], stdout=subprocess.PIPE).stdout


def _sibling_aggregate():
    spec = importlib.util.spec_from_file_location("where_enrolled_ccd", SIBLING)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._aggregate


def membership():
    if COUNTS.exists():
        return pd.read_csv(COUNTS, dtype={"NCESSCH": str})
    cols = ["NCESSCH", "GRADE", "RACE_ETHNICITY", "STUDENT_COUNT", "TOTAL_INDICATOR"]
    dt = {"NCESSCH": str, "GRADE": str, "RACE_ETHNICITY": str, "TOTAL_INDICATOR": str, "STUDENT_COUNT": float}
    reader = pd.read_csv(_unzip(MEM_ZIP, MEM_CSV), usecols=cols, dtype=dt, chunksize=2_000_000)
    out = _sibling_aggregate()(reader, "NCESSCH").reset_index().rename(columns={"index": "NCESSCH"})
    out = out.sort_values("NCESSCH")
    tmp = COUNTS.with_suffix(".tmp")
    out.to_csv(tmp, index=False, lineterminator="\n")
    tmp.rename(COUNTS)
    return pd.read_csv(COUNTS, dtype={"NCESSCH": str})


def universe():
    e = pd.read_csv(_unzip(EDGE_ZIP, EDGE_TXT), sep="|", header=None, names=EDGE_COLS, dtype=str,
                    encoding="latin-1")
    if len(e) < 95_000 or e.NCESSCH.duplicated().any():
        raise SystemExit(f"[BLOCKED] EDGE geocode file: {len(e)} rows or duplicate NCESSCH")
    e["LAT"], e["LON"] = pd.to_numeric(e.LAT), pd.to_numeric(e.LON)
    d = pd.read_csv(_unzip(DIR_ZIP, DIR_CSV), dtype=str, encoding="latin-1",
                    usecols=["NCESSCH", "FIPST", "ST", "SCH_NAME", "LEAID", "LEA_NAME", "ST_SCHID", "SY_STATUS",
                             "SCH_TYPE", "SCH_TYPE_TEXT", "CHARTER_TEXT", "LEVEL", "GSLO", "GSHI"])
    v = pd.read_csv(_unzip(CHR_ZIP, CHR_CSV), dtype=str, encoding="latin-1", usecols=["NCESSCH", "VIRTUAL"])
    m = membership()
    u = d.merge(e[["NCESSCH", "LAT", "LON", "LOCALE", "CNTY", "STFIP"]], on="NCESSCH", how="left", validate="1:1")
    u = u.merge(v, on="NCESSCH", how="left", validate="1:1").merge(m, on="NCESSCH", how="left", validate="1:1")
    u = u[u.FIPST.astype(int).le(56) & u.SY_STATUS.isin(OPERATING)].copy()
    for c in ["k12_all", "k12_hisp", "tot_all", "tot_hisp", "pk_all", "pk_hisp"]:
        u[c] = pd.to_numeric(u[c])
    # Hispanic K-12 missing but a Hispanic total present: scale by the K-12 share (as weighting.py does).
    fill = u.k12_hisp.isna() & u.tot_hisp.notna() & u.tot_all.gt(0)
    u.loc[fill, "k12_hisp"] = u.tot_hisp * u.k12_all.fillna(u.tot_all) / u.tot_all
    u["k12_all"] = u.k12_all.fillna(u.tot_all - u.pk_all.fillna(0)).fillna(0)
    u["k12_hisp"] = u.k12_hisp.fillna(0)
    u["virtual"] = u.VIRTUAL.eq("FULLVIRTUAL")
    u["charter"] = u.CHARTER_TEXT.eq("Yes")
    u["has_point"] = u.LAT.notna() & u.LON.notna()
    return u.sort_values("NCESSCH").reset_index(drop=True)


if __name__ == "__main__":
    u = universe()
    print(len(u), int(u.k12_all.sum()), int(u.k12_hisp.sum()), u.virtual.sum(), u.charter.sum(), (~u.has_point).sum())

"""Shared loader for the selection-curve lane.

Reads the gated IPUMS-CPS ASEC 1994-2025 extract with the universe rules of
`second_generation_by_origin_2026_09_22` (civilian adults 25-64, NATIVITY 1-5, the 2014 HFLAG=1
redesign sample dropped) and caches the analysis columns as `_cache/frame.parquet`. The sha256 of
the extract is checked against its manifest before the first read.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[2]
CPS_DIR = REPO / "sources" / "immigration-fiscal" / "data" / "external" / "cps"
SRC = CPS_DIR / "cps_2ndgen.csv.gz"
MANIFEST = CPS_DIR / "cps_2ndgen.manifest.json"
DDI = CPS_DIR / "cps_2ndgen.xml"
CACHE = LANE / "_cache"
FRAME = CACHE / "frame.parquet"
G2_LANE = REPO / "infra" / "immigration-fiscal" / "second_generation_by_origin_2026_09_22"

FRAME_SQL = """
SELECT CAST(YEAR AS INT) AS year, CAST(SERIAL AS BIGINT) AS serial,
       CAST(ASECWT AS DOUBLE) AS w, CAST(AGE AS INT) AS age, CAST(SEX AS INT) AS sex,
       CAST(RACE AS INT) AS race, CAST(HISPAN AS INT) AS hispan, CAST(NCHILD AS INT) AS nchild,
       CAST(BPL AS INT) AS bpl, CAST(FBPL AS INT) AS fbpl, CAST(MBPL AS INT) AS mbpl,
       CAST(CITIZEN AS INT) AS citizen, CAST(NATIVITY AS INT) AS nativity,
       CAST(YRIMMIG AS INT) AS yrimmig,
       CAST(EMPSTAT AS INT) AS empstat, CAST(LABFORCE AS INT) AS labforce,
       CAST(EDUC AS INT) AS educ, CAST(INCTOT AS BIGINT) AS inctot,
       CAST(INCWAGE AS BIGINT) AS incwage
FROM read_csv_auto('{src}', header=true)
WHERE CAST(AGE AS INT) BETWEEN 25 AND 64
  AND CAST(EMPSTAT AS INT) <> 1
  AND CAST(NATIVITY AS INT) IN (1,2,3,4,5)
  AND NOT (CAST(YEAR AS INT) = 2014 AND HFLAG = '1')
ORDER BY year, serial
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest() -> str:
    want = json.loads(MANIFEST.read_text())["sha256"]
    got = sha256_file(SRC)
    if got != want:
        raise SystemExit(f"[BLOCKED] cps_2ndgen sha256 {got} != manifest {want}")
    return got


def load_frame() -> pd.DataFrame:
    if not FRAME.exists():
        check_manifest()
        import duckdb
        con = duckdb.connect()
        df = con.execute(FRAME_SQL.format(src=SRC)).df()
        con.close()
        CACHE.mkdir(exist_ok=True)
        df.to_parquet(FRAME, index=False)
    return pd.read_parquet(FRAME)


def parent_origin(df: pd.DataFrame) -> np.ndarray:
    """G2 origin rule of the V02 lane: father's birthplace when foreign-born, else mother's."""
    fbpl, mbpl = df.fbpl.to_numpy(), df.mbpl.to_numpy()
    return np.where(fbpl // 100 >= 150, fbpl, np.where(mbpl // 100 >= 150, mbpl, -1))


def ddi_labels(var: str) -> dict[int, str]:
    import xml.etree.ElementTree as ET
    root = ET.parse(DDI).getroot()
    for v in root.iter():
        if v.tag.endswith("}var") and v.attrib.get("ID") == var:
            out = {}
            for cat in v:
                if not cat.tag.endswith("catgry"):
                    continue
                val = lab = None
                for ch in cat:
                    if ch.tag.endswith("catValu"):
                        val = ch.text
                    elif ch.tag.endswith("labl"):
                        lab = ch.text
                if val is not None and lab is not None:
                    try:
                        out[int(val)] = lab
                    except ValueError:
                        pass
            return out
    raise KeyError(var)

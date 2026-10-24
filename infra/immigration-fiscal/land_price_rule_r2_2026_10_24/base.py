"""The r1 lane's records and prices, rebuilt through r1's own functions (read only).

`land_price_rule_2026_10_24/build.py` is imported as a library: its acquisition check, urban/rural
classifier (hash-validated cache), FHFA engine, farmland prices and record valuation run unchanged,
so every r2 correction starts from exactly the r1 frame. Nothing in the r1 or public_land lanes is
written. The r1 frame is checked against r1's cached `valued_records.parquet` before use.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
R1_DIR = FISCAL / "land_price_rule_2026_10_24"
PUBLIC = FISCAL / "public_land_2026_10_24"
SCHOOL = FISCAL / "school_land_2026_10_24"


def load_r1():
    """Import r1's build.py under a private name (r1 re-execs itself with -I; callers must run -I)."""
    if not sys.flags.isolated:
        raise RuntimeError("[BLOCKED] run under python -I (r1's build.py re-execs otherwise)")
    spec = importlib.util.spec_from_file_location("land_rule_r1_build", R1_DIR / "build.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def r1_frame():
    """Return (r1 module, valued frame d, helpers) exactly as r1's main() builds them, before charges."""
    r1 = load_r1()
    r1.acquire.main()
    status = r1.classify.build()
    engine, P = r1.school_engine()
    r1.ENGINE, r1.PRICES = engine, P
    r1.FARM = r1.farm_prices()
    rest, hw = r1.load_records()
    rest = r1.attach_urban_status(rest, status)
    counties = sorted(set(hw.county) | set(rest.county.dropna()) - {""})
    near = r1.nearest_fhfa(P)
    urban_tracts = set(status[status.kind.eq("tract2010") & status.urban_fraction.eq(1.0)].record_id)
    upt = r1.urban_price_table(engine, P, counties, near, r1.county_urban_prices(engine, P, urban_tracts))
    farm_rows = r1.farm_price_rows([c for c in counties if c[2:] != "000"], r1.FARM)
    d = r1.value_records(rest, hw, upt, farm_rows, P, engine)
    cached = pd.read_parquet(R1_DIR / "_cache" / "valued_records.parquet", columns=["record_id", "value_central"])
    if len(cached) != len(d) or not (cached.record_id.to_numpy() == d.record_id.to_numpy()).all() \
            or not np.allclose(cached.value_central.to_numpy(), d.value_central.to_numpy(), rtol=1e-12, atol=1e-6):
        raise ValueError("[BLOCKED] r1 frame no longer matches r1's valued_records.parquet; rerun r1 first")
    roads = pd.read_csv(PUBLIC / "derived" / "roads_county_acres.csv", dtype={"county_fips": str, "toll_id": str})
    roads = roads[roads.case_line.notna() & roads.case_line.ne("")].reset_index(drop=True)
    return r1, d, dict(engine=engine, P=P, upt=upt, farm_rows=farm_rows, near=near, status=status, roads=roads)

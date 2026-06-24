#!/usr/bin/env python3
"""INT-06 — canonical citizenship/legal-status harmonization spine (the join keystone).

The recurring blocker for every crime<->fiscal join is that legal status is coded ~5
different ways (ACS CIT/NATIVITY, IPUMS CITIZEN, USSC, BJS SPI, Light TX-DPS). This is a
SHARED INVARIANT: define the canonical enum ONCE here, every node loads it (never re-maps).

Builds two tables into the context warehouse (flow into the unified release):
  status_class_def        — the 5 canonical classes + nativity rollup + is_citizen
  status_class_crosswalk  — each source's native codes -> canonical class, with lossy_flag
                            (source can't resolve finer) and verified (codebook-confirmed).

Honest discipline: ACS/IPUMS cannot split LPR from unauthorized -> fold to other_noncitizen,
lossy_flag=True. USSC/SPI category specifics are UNVERIFIED (verified=False) pending codebook.

Run: uv run --with duckdb,pandas python build_status_crosswalk.py
"""
from __future__ import annotations

import sys

from paths import derived_root, duckdb_path

# canonical enum: (status_class, rank, nativity_rollup, is_citizen, label)
CLASSES = [
    ("native_born",          1, "native",  True,  "US-born citizen (incl. born abroad to US parents, PR/territories)"),
    ("naturalized",          2, "foreign", True,  "Foreign-born, naturalized US citizen"),
    ("lpr_legal_noncitizen", 3, "foreign", False, "Lawful permanent resident / other lawfully-present noncitizen"),
    ("unauthorized",         4, "foreign", False, "Unauthorized / undocumented noncitizen"),
    ("other_noncitizen",     5, "foreign", False, "Noncitizen, legal status unresolved (catch-all for lossy sources)"),
]

# (source, native_code, native_label, status_class, lossy_flag, verified, note)
CROSSWALK = [
    # --- ACS CIT (5-level; ACSPUMS2019_2023CodeLists.xlsx, local) ---
    ("ACS_CIT", "1", "Born in the United States",            "native_born",      False, True,  ""),
    ("ACS_CIT", "2", "Born in PR/US Island Areas",           "native_born",      False, True,  ""),
    ("ACS_CIT", "3", "Born abroad of American parent(s)",    "native_born",      False, True,  ""),
    ("ACS_CIT", "4", "US citizen by naturalization",         "naturalized",      False, True,  ""),
    ("ACS_CIT", "5", "Not a US citizen",                     "other_noncitizen", True,  True,  "ACS cannot split LPR/unauthorized/other; folds to other_noncitizen"),
    # --- ACS NATIVITY (2-level; rollup axis only) ---
    ("ACS_NATIVITY", "1", "Native",       "native_born",      False, True, ""),
    ("ACS_NATIVITY", "2", "Foreign born", "other_noncitizen", True,  True, "ROLLUP ONLY: foreign-born spans naturalized+LPR+unauthorized; do NOT use for fine status (use CIT). Joins at nativity_rollup='foreign'"),
    # --- IPUMS CITIZEN (the local 44M-row panel) ---
    ("IPUMS_CITIZEN", "0", "N/A (born in US)",                "native_born",      False, True, ""),
    ("IPUMS_CITIZEN", "1", "Born abroad of American parents", "native_born",      False, True, ""),
    ("IPUMS_CITIZEN", "2", "Naturalized citizen",             "naturalized",      False, True, ""),
    ("IPUMS_CITIZEN", "3", "Not a citizen",                   "other_noncitizen", True,  True, "IPUMS cannot split LPR/unauthorized; folds to other_noncitizen"),
    # --- Light/He/Robey TX-DPS (the unit-level crime source) ---
    ("LIGHT_TXDPS", "USB",   "US-born",         "native_born",          False, True, ""),
    ("LIGHT_TXDPS", "LEGAL", "Legal immigrant", "lpr_legal_noncitizen", True,  True, "Paper's 'legal immigrant' = LPR + other lawful; carry denom_source (CMS/Pew) separately, never collapse"),
    ("LIGHT_TXDPS", "UNDOC", "Undocumented",    "unauthorized",         False, True, "DPS immigration-status flag at arrest"),
    # --- USSC individual offender citizenship field (categories UNVERIFIED) ---
    ("USSC_NEWCIT", "0", "US Citizen",            "native_born",          True,  False, "[UNVERIFIED] US-citizen offenders not split native/naturalized; confirm USSC codebook"),
    ("USSC_NEWCIT", "1", "Resident/Legal Alien",  "lpr_legal_noncitizen", False, False, "[UNVERIFIED] confirm USSC codebook"),
    ("USSC_NEWCIT", "2", "Illegal Alien",         "unauthorized",         False, False, "[UNVERIFIED] confirm USSC codebook"),
    ("USSC_NEWCIT", "3", "Non-US Citizen/Unknown","other_noncitizen",     True,  False, "[UNVERIFIED] confirm USSC codebook"),
    # --- BJS Survey of Prison Inmates citizenship item (UNVERIFIED) ---
    ("BJS_SPI", "CIT",    "US citizen",  "native_born",      True,  False, "[UNVERIFIED] SPI citizen item not split native/naturalized; confirm DS1 codebook"),
    ("BJS_SPI", "NONCIT", "Non-citizen", "other_noncitizen", True,  False, "[UNVERIFIED] SPI cannot split LPR/unauthorized; confirm DS1 codebook"),
]


def build() -> None:
    try:
        import duckdb
        import pandas as pd
    except ImportError:
        sys.exit("need duckdb+pandas — run via: uv run --with duckdb,pandas python build_status_crosswalk.py")

    cls = pd.DataFrame(CLASSES, columns=["status_class", "rank", "nativity_rollup", "is_citizen", "label"])
    xw = pd.DataFrame(CROSSWALK, columns=["source", "native_code", "native_label",
                                          "status_class", "lossy_flag", "verified", "note"])
    # integrity: every crosswalk target must be a defined canonical class
    bad = set(xw["status_class"]) - set(cls["status_class"])
    if bad:
        sys.exit(f"crosswalk maps to undefined status_class(es): {bad}")

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build context first")
    con = duckdb.connect(str(db))
    con.register("_cls", cls)
    con.register("_xw", xw)
    con.execute("CREATE OR REPLACE TABLE status_class_def AS SELECT * FROM _cls")
    con.execute("CREATE OR REPLACE TABLE status_class_crosswalk AS SELECT * FROM _xw")

    out = derived_root() / "context"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY status_class_def TO '{out / 'status_class_def.csv'}' (HEADER)")
    con.execute(f"COPY status_class_crosswalk TO '{out / 'status_class_crosswalk.csv'}' (HEADER)")

    n_src = con.execute("SELECT count(DISTINCT source) FROM status_class_crosswalk").fetchone()[0]
    n_lossy = con.execute("SELECT count(*) FROM status_class_crosswalk WHERE lossy_flag").fetchone()[0]
    n_unver = con.execute("SELECT count(*) FROM status_class_crosswalk WHERE NOT verified").fetchone()[0]
    con.close()

    print(f"  ✓ status_class_def: {len(cls)} canonical classes")
    print(f"  ✓ status_class_crosswalk: {len(xw)} rows across {n_src} sources "
          f"({n_lossy} lossy folds, {n_unver} UNVERIFIED pending codebook)")
    print(f"  → {out}/status_class_*.csv")
    print("  sources harmonized: " + ", ".join(sorted(set(xw['source']))))


if __name__ == "__main__":
    build()

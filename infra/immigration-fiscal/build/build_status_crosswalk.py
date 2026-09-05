#!/usr/bin/env python3
"""INT-06 — canonical citizenship/legal-status harmonization spine (the join keystone).

The recurring blocker for every crime<->fiscal join is that legal status is coded ~5
different ways (ACS CIT/NATIVITY, IPUMS CITIZEN, USSC, BJS SPI, Light TX-DPS). This is a
SHARED INVARIANT: define the canonical enum ONCE here, every node loads it (never re-maps).

Builds two tables into the context warehouse (flow into the unified release):
  status_class_def        — source-resolvable classes + nativity rollup + is_citizen
  status_class_crosswalk  — each source's native codes -> canonical class, with lossy_flag
                            (source can't resolve finer) and verified (codebook-confirmed).

Unresolved citizenship or nativity stays unresolved. Broad source categories must not
be mapped to a narrower class even when lossy_flag is set. USSC codes remain unverified.

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
    ("other_noncitizen",     5, "unknown", False, "Noncitizen; birthplace and legal status unresolved"),
    ("citizen_unknown_nativity", 6, "unknown", True, "US citizen; native/naturalized split unresolved"),
    ("foreign_born_unknown_citizenship", 7, "foreign", None, "Foreign-born; citizenship and legal status unresolved"),
    ("legal_immigrant_mixed_citizenship", 8, "foreign", None, "Study-classified legal immigrants, including naturalized citizens"),
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
    ("ACS_NATIVITY", "2", "Foreign born", "foreign_born_unknown_citizenship", True, True, "Nativity alone does not establish citizenship; use CIT for finer status"),
    # --- IPUMS CITIZEN (the local 44M-row panel) ---
    ("IPUMS_CITIZEN", "0", "N/A (born in US)",                "native_born",      False, True, ""),
    ("IPUMS_CITIZEN", "1", "Born abroad of American parents", "native_born",      False, True, ""),
    ("IPUMS_CITIZEN", "2", "Naturalized citizen",             "naturalized",      False, True, ""),
    ("IPUMS_CITIZEN", "3", "Not a citizen",                   "other_noncitizen", True,  True, "IPUMS cannot split LPR/unauthorized; folds to other_noncitizen"),
    # --- Light/He/Robey TX-DPS (the unit-level crime source) ---
    ("LIGHT_TXDPS", "USB",   "US-born",         "native_born",          False, True, ""),
    ("LIGHT_TXDPS", "LEGAL", "Legal immigrant including naturalized", "legal_immigrant_mixed_citizenship", True, True, "PNAS methods and replication.do: baseline legal group includes naturalized citizens; CMS/Pew are denominator variants"),
    ("LIGHT_TXDPS", "LEGAL_NONCIT", "Legal immigrant excluding naturalized", "lpr_legal_noncitizen", True, True, "CMS_nat splits naturalized from the legal-immigrant group, not from the native-born group; study classification, not an LPR-only measure"),
    ("LIGHT_TXDPS", "NATURALIZED", "Naturalized citizen", "naturalized", False, True, "Separate group in big_category_nat.dta"),
    ("LIGHT_TXDPS", "UNDOC", "Undocumented",    "unauthorized",         False, True, "DPS immigration-status flag at arrest"),
    # --- USSC individual offender citizenship field (categories UNVERIFIED) ---
    ("USSC_NEWCIT", "0", "US Citizen",            "citizen_unknown_nativity", True, False, "[UNVERIFIED] US-citizen offenders not split native/naturalized; confirm USSC codebook"),
    ("USSC_NEWCIT", "1", "Resident/Legal Alien",  "lpr_legal_noncitizen", False, False, "[UNVERIFIED] confirm USSC codebook"),
    ("USSC_NEWCIT", "2", "Illegal Alien",         "unauthorized",         False, False, "[UNVERIFIED] confirm USSC codebook"),
    ("USSC_NEWCIT", "3", "Non-US Citizen/Unknown","other_noncitizen",     True,  False, "[UNVERIFIED] confirm USSC codebook"),
    # Official analysis recode; V0950 skip logic is not an equivalent classifier.
    ("BJS_SPI", "RV0004_1", "US citizen", "citizen_unknown_nativity", True, True, "ICPSR37692 codebook RV0004=1; V0945 separately records birthplace"),
    ("BJS_SPI", "RV0004_2", "Noncitizen", "other_noncitizen", True, True, "ICPSR37692 codebook RV0004=2; no exact LPR/unauthorized split"),
]


def status_class_for(source: str, native_code: str) -> str:
    """Use the canonical crosswalk without inferring finer information."""
    matches = [r[3] for r in CROSSWALK if r[0] == source and r[1] == native_code]
    if len(matches) != 1:
        raise ValueError(f"Expected one status mapping for {source}/{native_code}: {matches}")
    return matches[0]


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

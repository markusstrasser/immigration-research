#!/usr/bin/env python3
"""INT-03 — represent DOJ SCAAP awards as the crime↔fiscal $ bridge.

Parses the auto-fetched SCAAP FY23 award PDF (crime_frontier/scaap/) into two tables in
the context warehouse (flow into the unified release):
  crime_scaap_awards      — per-jurisdiction: criminal-alien inmate-days + reimbursement $
  crime_scaap_state_2023  — state rollup keyed by state_fips (joins the fiscal state-local ledger)

This is the ONLY admin series tying criminal-alien incarceration burden to dollars — the
single line connecting the crime and fiscal halves of the project.

Run: uv run --with duckdb,pandas,pdfplumber python parse_scaap_awards.py
Skips gracefully if the PDF isn't present (run setup-crime-frontier.sh first).
"""
from __future__ import annotations

import re
import sys

from paths import data_root, derived_root, duckdb_path

# USPS state/territory abbrev -> FIPS (2-digit string)
ST_FIPS = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06", "CO": "08", "CT": "09",
    "DE": "10", "DC": "11", "FL": "12", "GA": "13", "HI": "15", "ID": "16", "IL": "17",
    "IN": "18", "IA": "19", "KS": "20", "KY": "21", "LA": "22", "ME": "23", "MD": "24",
    "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29", "MT": "30", "NE": "31",
    "NV": "32", "NH": "33", "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38",
    "OH": "39", "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46",
    "TN": "47", "TX": "48", "UT": "49", "VT": "50", "VA": "51", "WA": "53", "WV": "54",
    "WI": "55", "WY": "56", "PR": "72", "GU": "66", "VI": "78",
}


def _num(s: str) -> float | None:
    if s is None:
        return None
    s = re.sub(r"[\$,]", "", str(s)).strip()
    if not s or s in {"-", "N/A"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def build() -> None:
    try:
        import duckdb
        import pandas as pd
        import pdfplumber
    except ImportError:
        sys.exit("need duckdb+pandas+pdfplumber — uv run --with duckdb,pandas,pdfplumber python parse_scaap_awards.py")

    pdf_path = data_root() / "external" / "crime_frontier" / "scaap" / "scaap_fy23_awards.pdf"
    if not pdf_path.exists():
        print(f"  ! SCAAP PDF not found at {pdf_path} — run setup-crime-frontier.sh; skipping")
        return

    rows = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            tbl = page.extract_table()
            if not tbl:
                continue
            for r in tbl:
                if not r or r[0] is None or not str(r[0]).strip().isdigit():
                    continue  # skip header / non-data rows
                if len(r) < 8:
                    continue
                fy, st, name, salary, total_days, dhs_days, unk_days, award = r[:8]
                rows.append({
                    "fiscal_year": int(str(fy).strip()),
                    "state_abbr": str(st).strip(),
                    "state_fips": ST_FIPS.get(str(st).strip()),
                    "jurisdiction": str(name).strip(),
                    "correctional_salary": _num(salary),
                    "total_inmate_days": _num(total_days),
                    "dhs_confirmed_criminal_alien_days": _num(dhs_days),
                    "unknown_status_days": _num(unk_days),
                    "scaap_award_usd": _num(award),
                })
    if not rows:
        sys.exit("parsed 0 rows from SCAAP PDF — table extraction failed; inspect the PDF")

    df = pd.DataFrame(rows)
    unmapped = sorted(df.loc[df["state_fips"].isna(), "state_abbr"].unique())
    if unmapped:
        print(f"  ! unmapped state abbrevs (no FIPS): {unmapped}")

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build context first")
    con = duckdb.connect(str(db))
    con.register("_s", df)
    con.execute("CREATE OR REPLACE TABLE crime_scaap_awards AS SELECT * FROM _s")
    con.execute("""
        CREATE OR REPLACE TABLE crime_scaap_state_2023 AS
        SELECT fiscal_year, state_fips, any_value(state_abbr) AS state_abbr,
               count(*)                                  AS n_jurisdictions,
               sum(dhs_confirmed_criminal_alien_days)    AS criminal_alien_inmate_days,
               sum(unknown_status_days)                  AS unknown_status_days,
               sum(total_inmate_days)                    AS total_inmate_days,
               sum(scaap_award_usd)                      AS scaap_award_usd
        FROM crime_scaap_awards
        WHERE state_fips IS NOT NULL
        GROUP BY fiscal_year, state_fips
        ORDER BY criminal_alien_inmate_days DESC NULLS LAST
    """)

    out = derived_root() / "crime"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY crime_scaap_awards TO '{out / 'scaap_awards_fy23.csv'}' (HEADER)")
    con.execute(f"COPY crime_scaap_state_2023 TO '{out / 'scaap_state_fy23.csv'}' (HEADER)")

    n = con.execute("SELECT count(*) FROM crime_scaap_awards").fetchone()[0]
    n_st = con.execute("SELECT count(*) FROM crime_scaap_state_2023").fetchone()[0]
    tot_days, tot_award = con.execute(
        "SELECT sum(criminal_alien_inmate_days), sum(scaap_award_usd) FROM crime_scaap_state_2023").fetchone()
    top = con.execute(
        "SELECT state_abbr, criminal_alien_inmate_days, scaap_award_usd FROM crime_scaap_state_2023 LIMIT 5").fetchall()
    con.close()

    print(f"  ✓ crime_scaap_awards: {n} jurisdictions; crime_scaap_state_2023: {n_st} states")
    print(f"  ✓ national FY23: {tot_days:,.0f} DHS-confirmed criminal-alien inmate-days, "
          f"${tot_award:,.0f} reimbursed")
    print("  top states by criminal-alien inmate-days: " +
          ", ".join(f"{s}({d:,.0f}d/${a:,.0f})" for s, d, a in top))


if __name__ == "__main__":
    build()

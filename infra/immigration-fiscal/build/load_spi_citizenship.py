#!/usr/bin/env python3
"""INT-02 — represent BJS Survey of Prison Inmates 2016 incarceration by citizenship.

The standard incarceration-rate-by-citizenship surface (the Butcher-Piehl method). Reads the
ICPSR 37692 DS0001 public-use file (staged at crime_frontier/spi/, login/DUA-gated — see
MANUAL_ACQUIRE) and produces the weighted prison population by citizenship, harmonized to the
INT-06 spine.

Citizenship logic (per the SPI codebook): country-of-citizenship (SES5, V0946-49) is SUPPRESSED
in the public file. V0950 (SES5A "Also a US citizen?") is asked only of respondents who reported
a FOREIGN citizenship — so V0950=No (2) = noncitizen; V0950=Yes (1) = dual (US citizen); a
US-only citizen said "United States" to SES5 and skipped V0950 (missing). Refusal/Don't-know are
flagged ambiguous, not assigned.

  crime_spi_inmates_by_citizenship — weighted prison pop by {us_citizen, noncitizen} (2016),
                                     status_class via the spine (noncitizen -> other_noncitizen,
                                     us_citizen -> native_born; both lossy — can't split finer).

Run: uv run --with duckdb,pandas,pyreadstat python load_spi_citizenship.py  (skips if not staged)
"""
from __future__ import annotations

import sys

from paths import data_root, derived_root, duckdb_path, microdata_duckdb_path


def build() -> None:
    try:
        import duckdb
        import pyreadstat
    except ImportError:
        sys.exit("need duckdb+pyreadstat+pandas — uv run --with duckdb,pandas,pyreadstat python load_spi_citizenship.py")

    base = data_root() / "external" / "crime_frontier" / "spi"
    dta = base / "ICPSR_37692" / "DS0001" / "37692-0001-Data.dta"
    if not dta.exists():
        # try a flatter staging
        hits = list(base.rglob("37692-0001-Data.dta")) if base.exists() else []
        if not hits:
            print(f"  ! SPI data not staged at {dta} (ICPSR 37692, gated — see MANUAL_ACQUIRE); skipping")
            return
        dta = hits[0]

    df, _ = pyreadstat.read_dta(str(dta), usecols=["V0950", "V1585"])
    w = "V1585"
    total = df[w].sum()

    noncit = df.loc[df["V0950"] == 2, w].sum()
    ambiguous = df.loc[df["V0950"].isin([-1, -2]), w].sum()
    uscit = total - noncit - ambiguous  # dual (V0950=1) + US-only (skipped/missing)

    rows = [
        {"citizenship_status": "noncitizen", "status_class": "other_noncitizen",
         "weighted_inmates": float(noncit), "share_of_prison_pop": float(noncit / total),
         "note": "V0950=2 (foreign citizen, not also US); SPI can't split LPR/unauthorized"},
        {"citizenship_status": "us_citizen", "status_class": "native_born",
         "weighted_inmates": float(uscit), "share_of_prison_pop": float(uscit / total),
         "note": "US-only (skipped V0950) + dual citizens (V0950=1); can't split native/naturalized"},
        {"citizenship_status": "ambiguous", "status_class": None,
         "weighted_inmates": float(ambiguous), "share_of_prison_pop": float(ambiguous / total),
         "note": "V0950 refusal/don't-know — unassigned"},
    ]

    import pandas as pd
    out_df = pd.DataFrame(rows)
    out_df.insert(0, "survey_year", 2016)
    out_df.insert(1, "prison_population_total", float(total))

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build context first")
    con = duckdb.connect(str(db))
    con.register("_s", out_df)
    con.execute("CREATE OR REPLACE TABLE crime_spi_inmates_by_citizenship AS SELECT * FROM _s")
    out = derived_root() / "crime"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY crime_spi_inmates_by_citizenship TO '{out / 'spi_inmates_by_citizenship_2016.csv'}' (HEADER)")

    print(f"  ✓ crime_spi_inmates_by_citizenship: weighted 2016 US prison pop = {total:,.0f}")
    print(f"    noncitizen: {noncit:,.0f} ({noncit/total:.1%})  |  us_citizen: {uscit:,.0f} ({uscit/total:.1%})")

    # INT-02 incarceration RATE: SPI numerator / ACS noncitizen-adult denominator (from the licensed
    # microdata panel — AGGREGATE output only, no microdata redistributed). Skips if panel absent.
    md = microdata_duckdb_path()
    if md.exists():
        mcon = duckdb.connect(str(md), read_only=True)
        yr, noncit_adults, all_adults = mcon.execute(
            "SELECT YEAR, sum(CASE WHEN CITIZEN=3 THEN PERWT ELSE 0 END), sum(PERWT) "
            "FROM ipums_usa_borjas_panel WHERE AGE>=18 GROUP BY YEAR ORDER BY YEAR DESC LIMIT 1").fetchone()
        mcon.close()
        cit_adults = all_adults - noncit_adults
        nr = noncit / noncit_adults * 1e5
        cr = uscit / cit_adults * 1e5
        rate_df = pd.DataFrame([
            {"citizenship_status": "noncitizen", "prison_year": 2016, "acs_adult_year": int(yr),
             "prisoners": float(noncit), "adults_18plus": float(noncit_adults), "per_100k_adults": round(nr, 1)},
            {"citizenship_status": "us_citizen", "prison_year": 2016, "acs_adult_year": int(yr),
             "prisoners": float(uscit), "adults_18plus": float(cit_adults), "per_100k_adults": round(cr, 1)},
        ])
        con.register("_r", rate_df)
        con.execute("CREATE OR REPLACE TABLE crime_spi_incarceration_rate AS SELECT * FROM _r")
        con.execute(f"COPY crime_spi_incarceration_rate TO '{out / 'spi_incarceration_rate.csv'}' (HEADER)")
        print(f"    INT-02 RATE (ACS {yr} adult denom, prison 2016): noncitizen {nr:.0f}/100k vs citizen {cr:.0f}/100k "
              f"→ ratio {nr/cr:.2f} (noncitizens {'UNDER' if nr < cr else 'OVER'}-represented). "
              f"Caveat: prison year 2016 vs adult-denominator {yr}.")
    else:
        print("    ! incarceration RATE skipped (licensed microdata panel absent) — SPI share only")
    con.close()


if __name__ == "__main__":
    build()

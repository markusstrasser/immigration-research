#!/usr/bin/env python3
"""MSA foreign-born stock share × rent × supply elasticity: descriptive context.

Metro foreign-born share comes from ACS 2023 B05002, joined through a CBSA
gazetteer and approximate name key. A stock share is not an exogenous demand shock;
these cross-sectional correlations do not test the Wilson-Zhou causal mechanism.

Cross-section caveat: only ACS 2023 is staged, so fb-share is a 2023 LEVEL (not a Δ); rent is both
the ACS 2023 level (B25064) and Zillow 2016-25 growth. A second ACS year permits
changes; causal identification additionally requires a credible counterfactual.

Inputs (staged in <data_root>/external/urban_housing/):
  acs/acsdt1y2023-b05002.dat  acs/acsdt1y2023-b25064.dat  geo/2023_Gaz_cbsa_national.txt
  + the msa_rent_elasticity_panel table (Zillow growth × Saiz elasticity).
Run: uv run --with duckdb python build_msa_fb_rent_panel.py  → table msa_fb_rent_panel (context warehouse).
"""
from __future__ import annotations

import sys

from paths import data_root, duckdb_path
from build_msa_rent_elasticity_panel import _keysql


def _ok(m): print(f"  ✓ {m}")
def _warn(m): print(f"  ! {m}")


def build() -> int:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python build_msa_fb_rent_panel.py")

    uh = data_root() / "external" / "urban_housing"
    b05002 = uh / "acs" / "acsdt1y2023-b05002.dat"
    b25064 = uh / "acs" / "acsdt1y2023-b25064.dat"
    gaz = uh / "geo" / "2023_Gaz_cbsa_national.txt"
    for f in (b05002, b25064, gaz):
        if not f.exists():
            _warn(f"missing {f} — stage ACS summary-file tables + gazetteer (see setup-urban-housing MANUAL); skipping")
            return 1

    con = duckdb.connect(str(duckdb_path()))
    if "msa_rent_elasticity_panel" not in {r[0] for r in con.execute("SELECT table_name FROM duckdb_tables()").fetchall()}:
        _warn("msa_rent_elasticity_panel absent — run build_msa_rent_elasticity_panel.py first; skipping")
        con.close(); return 1

    # gazetteer NAME has a " Metro Area"/" Micro Area" suffix that must be stripped BEFORE the key
    gaz_name_clean = "regexp_replace(NAME, '\\s+(Metro|Micro) Area$', '')"
    con.execute(f"""
        CREATE OR REPLACE TABLE msa_fb_rent_panel AS
        WITH fb AS (   -- ACS B05002: foreign-born share by CBSA (sumlevel 310 = MSA)
            SELECT regexp_extract(GEO_ID, 'US([0-9]+)', 1) AS cbsa_code,
                   "B05002_E001" AS total_pop, "B05002_E013" AS foreign_born,
                   round("B05002_E013" / nullif("B05002_E001", 0), 4) AS fb_share
            FROM read_csv_auto('{b05002}', delim='|', header=true)
            WHERE GEO_ID LIKE '310%US%' AND "B05002_E001" > 0
        ), rent AS (   -- ACS B25064: median gross rent by CBSA
            SELECT regexp_extract(GEO_ID, 'US([0-9]+)', 1) AS cbsa_code, "B25064_E001" AS acs_median_rent
            FROM read_csv_auto('{b25064}', delim='|', header=true)
            WHERE GEO_ID LIKE '310%US%' AND "B25064_E001" > 0
        ), gz AS (     -- gazetteer: CBSA code → (first-city, state) key
            SELECT CAST(GEOID AS VARCHAR) AS cbsa_code, {_keysql(gaz_name_clean)} AS k
            FROM read_csv_auto('{gaz}', delim='\t', header=true) WHERE CBSA_TYPE = 1
        ), acs AS (
            SELECT g.k, f.fb_share, f.foreign_born, f.total_pop, r.acs_median_rent
            FROM fb f JOIN rent r USING (cbsa_code) JOIN gz g USING (cbsa_code)
            QUALIFY row_number() OVER (PARTITION BY g.k ORDER BY f.total_pop DESC) = 1
        )
        SELECT p.saiz_metro, p.zillow_metro, p.st, p.elasticity, p.population,
               a.fb_share, a.acs_median_rent, p.zori_annual_pct, p.zori_log_growth,
               p.elasticity_quartile,
               ntile(3) OVER (ORDER BY p.elasticity) AS elasticity_tercile
        FROM msa_rent_elasticity_panel p
        JOIN acs a ON a.k = {_keysql('p.zillow_metro')}
        WHERE a.fb_share IS NOT NULL
        ORDER BY a.fb_share DESC
    """)

    n = con.execute("SELECT count(*) FROM msa_fb_rent_panel").fetchone()[0]
    _ok(f"joined {n} metros with fb-share + rent + elasticity (ACS 2023 × Zillow × Saiz, no API key)")
    if n < 20:
        _warn("too few matched — inspect the name join"); con.close(); return 1

    # Descriptive correlation: stock composition, not a demand treatment.
    cr_lvl, cr_grw = con.execute(
        "SELECT round(corr(fb_share, acs_median_rent),3), round(corr(fb_share, zori_log_growth),3) "
        "FROM msa_fb_rent_panel").fetchone()
    print(f"\n  corr(fb_share, rent LEVEL) = {cr_lvl}   corr(fb_share, rent GROWTH 2016-25) = {cr_grw}")
    print("\n  Stock-share/rent associations by elasticity; no causal effect identified:")
    print(f"    {'tercile':<10}{'n':>4}{'elast':>8}{'fb_share':>10}{'rent$':>8}{'corr(fb,rent_lvl)':>20}")
    for t, n_, el, fb, rt, cc in con.execute("""
        SELECT elasticity_tercile, count(*), round(avg(elasticity),2), round(avg(fb_share),3),
               round(avg(acs_median_rent),0), round(corr(fb_share, acs_median_rent),3)
        FROM msa_fb_rent_panel GROUP BY 1 ORDER BY 1""").fetchall():
        lab = {1: 'inelastic', 2: 'mid', 3: 'elastic'}[t]
        print(f"    {lab:<10}{n_:>4}{el:>8}{fb:>10}{rt:>8}{str(cc) if cc is not None else 'NA':>20}")
    # top + bottom fb-share metros (sanity)
    print("\n  highest-immigrant metros (fb_share, rent, elasticity):")
    for m, fb, rt, el in con.execute(
        "SELECT zillow_metro, fb_share, acs_median_rent, elasticity FROM msa_fb_rent_panel LIMIT 5").fetchall():
        print(f"    {m:<28} fb={fb:.0%}  rent=${rt:.0f}  elasticity={el:.2f}")
    print("\n  NOTE: cross-sectional stock share only. A second year permits changes, not causal identification by itself.")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(build())

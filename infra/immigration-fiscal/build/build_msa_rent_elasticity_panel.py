#!/usr/bin/env python3
"""MSA rent-trajectory × housing-supply-elasticity panel — the supply-side half of the
Wilson-Zhou (2026) mechanism, built from acquired data only.

Wilson & Zhou (2026, Dallas Fed WP2607) find immigrant inflow raises rents with a ~null
housing-supply (permit) response — the price/rent response concentrates where supply is inelastic.
This panel joins the acquired Zillow ZORI/ZHVI panels to the in-warehouse Saiz (2010) elasticity by a
(first-city, state) key (the vintage-mismatch crosswalk: Zillow's modern multi-city CBSA names
"Miami-Fort Lauderdale, FL" ↔ Saiz's 1999 "Miami, FL (PMSA)" → both "miami|fl").

SCOPE: descriptive associations in a subset linked by an approximate name key.
The join does not validate geographic equivalence across metro vintages. Neither
a weak nor a strong bivariate correlation identifies the supply mechanism or the
immigration effect. A second exposure year enables changes, not causal inference
without a credible counterfactual and assumptions about confounding.

Run: uv run --with duckdb python build_msa_rent_elasticity_panel.py
Writes table `msa_rent_elasticity_panel`; missing required inputs fail explicitly.
"""
from __future__ import annotations

import sys

from paths import data_root, duckdb_path, lifetime_duckdb_path


def _ok(m): print(f"  ✓ {m}")
def _warn(m): print(f"  ! {m}")


def _keysql(col: str) -> str:
    """Approximate city/state locator; does not establish identical metro boundaries."""
    stripped = f"regexp_replace({col}, '\\s*\\([^)]*\\)\\s*$', '')"          # drop "(PMSA)/(MSA)"
    cities = f"regexp_replace({stripped}, ',\\s*[^,]*$', '')"                # before last comma
    state = f"regexp_extract({stripped}, ',\\s*([^,]*)$', 1)"                # after last comma
    fcity = f"lower(trim(regexp_extract({cities}, '^([^-/]*)', 1)))"          # before first - or /
    fstate = f"lower(trim(regexp_extract({state}, '^([^-/]*)', 1)))"
    return f"({fcity} || '|' || {fstate})"


def build() -> int:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python build_msa_rent_elasticity_panel.py")

    zdir = data_root() / "external" / "urban_housing" / "zillow"
    zori = zdir / "metro_zori_sfrcondomfr_sm_month.csv"
    zhvi = zdir / "metro_zhvi_sfrcondo_tier_sm_sa_month.csv"
    life = lifetime_duckdb_path()
    if not zori.exists() or not zhvi.exists():
        _warn(f"missing required Zillow input: {zori} / {zhvi}"); return 1
    if not life.exists():
        _warn(f"missing {life} — build lifetime warehouse first"); return 1

    con = duckdb.connect(str(duckdb_path()))
    con.execute(f"ATTACH '{life}' AS life (READ_ONLY)")

    have = {r[0] for r in con.execute(
        "SELECT table_name FROM duckdb_tables() WHERE database_name='life'").fetchall()}
    if "saiz_msa_elasticity" not in have:
        _warn("life.saiz_msa_elasticity absent"); con.close(); return 1

    zcols = {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{zori}')").fetchall()}
    c0, c1 = "2016-01-31", "2025-12-31"
    hcols = {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{zhvi}')").fetchall()}
    if not {c0, c1}.issubset(zcols & hcols):
        raise ValueError(f"Both Zillow inputs must contain the specified window {c0} to {c1}")
    years = (int(c1[:4]) + int(c1[5:7]) / 12) - (int(c0[:4]) + int(c0[5:7]) / 12)
    _ok(f"rent window {c0} → {c1} ({years:.1f} yr)")

    kr, km = _keysql("RegionName"), _keysql("msaname")
    con.execute(f"""
        CREATE OR REPLACE TABLE msa_rent_elasticity_panel AS
        WITH zori AS (
            SELECT {kr} AS k, RegionName AS zillow_metro, StateName AS st,
                   "{c0}" AS zori_start, "{c1}" AS zori_end,
                   ln("{c1}" / nullif("{c0}", 0)) AS zori_log_growth,
                   row_number() OVER (PARTITION BY {kr} ORDER BY SizeRank) AS rn
            FROM read_csv_auto('{zori}')
            WHERE RegionType = 'msa' AND "{c0}" IS NOT NULL AND "{c1}" IS NOT NULL
        ), zhvi AS (
            SELECT {kr} AS k, ln("{c1}" / nullif("{c0}", 0)) AS zhvi_log_growth,
                   row_number() OVER (PARTITION BY {kr} ORDER BY SizeRank) AS rn
            FROM read_csv_auto('{zhvi}')
            WHERE RegionType = 'msa' AND "{c0}" IS NOT NULL AND "{c1}" IS NOT NULL
        ), saiz AS (
            SELECT {km} AS k, msaname AS saiz_metro, elasticity, WRLURI, unaval, population,
                   row_number() OVER (PARTITION BY {km} ORDER BY population DESC) AS rn
            FROM life.saiz_msa_elasticity WHERE elasticity IS NOT NULL
        )
        SELECT s.saiz_metro, z.zillow_metro, z.st, s.elasticity, s.WRLURI, s.population,
               round(z.zori_start, 0) AS zori_start, round(z.zori_end, 0) AS zori_end,
               round(z.zori_log_growth, 4) AS zori_log_growth,
               round(100 * (exp(z.zori_log_growth / {years}) - 1), 2) AS zori_annual_pct,
               round(h.zhvi_log_growth, 4) AS zhvi_log_growth,
               ntile(4) OVER (ORDER BY s.elasticity) AS elasticity_quartile
        FROM (SELECT * FROM saiz WHERE rn = 1) s
        JOIN (SELECT * FROM zori WHERE rn = 1) z USING (k)
        LEFT JOIN (SELECT * FROM zhvi WHERE rn = 1) h USING (k)
        ORDER BY s.elasticity
    """)

    n_saiz = con.execute(
        f"SELECT count(DISTINCT {km}) FROM life.saiz_msa_elasticity WHERE elasticity IS NOT NULL").fetchone()[0]
    n_match = con.execute("SELECT count(*) FROM msa_rent_elasticity_panel").fetchone()[0]
    if not n_saiz or not n_match:
        raise ValueError("No usable Saiz/Zillow matches; cannot summarize an empty panel")
    _ok(f"matched {n_match}/{n_saiz} Saiz metros to Zillow on (first-city, state) ({100*n_match//n_saiz}%)")

    print("\n  rent growth (ZORI) by supply-elasticity quartile (Q1 = most inelastic):")
    rows = con.execute("""
        SELECT elasticity_quartile, count(*) n, round(avg(elasticity), 2) avg_elasticity,
               round(avg(zori_annual_pct), 2) avg_annual_rent_pct, round(avg(zhvi_log_growth), 3) avg_zhvi_log_growth
        FROM msa_rent_elasticity_panel GROUP BY 1 ORDER BY 1
    """).fetchall()
    print(f"    {'Q':<3}{'n':>5}{'elasticity':>12}{'rent %/yr':>12}{'zhvi Δlog':>12}")
    for q, n, el, rp, zh in rows:
        print(f"    {q:<3}{n:>5}{el:>12}{rp:>12}{str(zh) if zh is not None else 'NA':>12}")

    corr_r, corr_h = con.execute(
        "SELECT round(corr(zori_log_growth, elasticity), 3), round(corr(zhvi_log_growth, elasticity), 3) "
        "FROM msa_rent_elasticity_panel").fetchone()
    q1, q4 = rows[0][3], rows[-1][3]
    print(f"\n  corr(rent growth, elasticity) = {corr_r}  | corr(home-value growth, elasticity) = {corr_h}")
    print(f"  most-inelastic Q1 rent {q1}%/yr vs most-elastic Q4 {q4}%/yr  →  spread {round(q1 - q4, 2)} pp/yr")

    if corr_r is None:
        _warn("corr undefined")
    print("\n  Descriptive correlations only: no coefficient threshold here tests a causal mechanism.\n"
          "  Changes in foreign-born share would add an exposure measure, not identification by themselves.")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(build())

#!/usr/bin/env python3
"""MSA rent-trajectory × housing-supply-elasticity panel — the supply-side half of the
Wilson-Zhou (2026) mechanism, built from acquired data only.

Wilson & Zhou (2026, Dallas Fed WP2607) find immigrant inflow raises rents with a ~null
housing-supply (permit) response — the price/rent response concentrates where supply is inelastic.
This panel joins the acquired Zillow ZORI/ZHVI panels to the in-warehouse Saiz (2010) elasticity by a
(first-city, state) key (the vintage-mismatch crosswalk: Zillow's modern multi-city CBSA names
"Miami-Fort Lauderdale, FL" ↔ Saiz's 1999 "Miami, FL (PMSA)" → both "miami|fl").

HONEST SCOPE: this is a SUPPLY-MODERATOR validation + crosswalk proof, NOT the causal result.
The bivariate elasticity↔rent-growth relationship is expected to be weak precisely because elasticity
MODERATES a demand shock rather than driving rent growth on its own — which is the empirical reason the
immigrant TREATMENT (Δ foreign-born share by CBSA) is the load-bearing input. That treatment is GATED:
Census API (key-gated; keyless route closed 2026) or the Geocorr PUMA↔CBSA crosswalk. The
Δrent~Δfb-share×elasticity regression is staged for when that input lands (HUMAN.md).

Run: uv run --with duckdb python build_msa_rent_elasticity_panel.py
Writes table `msa_rent_elasticity_panel` to the context warehouse; skips if Zillow/Saiz absent.
"""
from __future__ import annotations

import re
import sys

from paths import data_root, duckdb_path, lifetime_duckdb_path


def _ok(m): print(f"  ✓ {m}")
def _warn(m): print(f"  ! {m}")


def _keysql(col: str) -> str:
    """SQL expression → (first principal city, first state) join key. Robust across Zillow
    multi-city CBSA names and Saiz 1999 single-city PMSA names. Pure SQL (no UDF)."""
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
    if not zori.exists():
        _warn(f"missing {zori} — run acquire/setup-urban-housing.sh first; skipping"); return 0
    if not life.exists():
        _warn(f"missing {life} — build lifetime warehouse first; skipping"); return 0

    con = duckdb.connect(str(duckdb_path()))
    con.execute(f"ATTACH '{life}' AS life (READ_ONLY)")

    have = {r[0] for r in con.execute(
        "SELECT table_name FROM duckdb_tables() WHERE database_name='life'").fetchall()}
    if "saiz_msa_elasticity" not in have:
        _warn("life.saiz_msa_elasticity absent; skipping"); con.close(); return 0

    zcols = {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{zori}')").fetchall()}
    c0, c1 = "2016-01-31", "2025-12-31"
    if c0 not in zcols or c1 not in zcols:
        date_cols = sorted(c for c in zcols if re.fullmatch(r"\d{4}-\d{2}-\d{2}", c))
        c0, c1 = date_cols[0], date_cols[-1]
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
    _ok(f"matched {n_match}/{n_saiz} Saiz metros to Zillow on (first-city, state) ({100*n_match//n_saiz}%)")

    print("\n  rent growth (ZORI) by supply-elasticity quartile (Q1 = most inelastic):")
    rows = con.execute("""
        SELECT elasticity_quartile, count(*) n, round(avg(elasticity), 2) avg_elasticity,
               round(avg(zori_annual_pct), 2) avg_annual_rent_pct, round(avg(zhvi_log_growth), 3) avg_zhvi_log_growth
        FROM msa_rent_elasticity_panel GROUP BY 1 ORDER BY 1
    """).fetchall()
    print(f"    {'Q':<3}{'n':>5}{'elasticity':>12}{'rent %/yr':>12}{'zhvi Δlog':>12}")
    for q, n, el, rp, zh in rows:
        print(f"    {q:<3}{n:>5}{el:>12}{rp:>12}{(zh if zh is not None else 0):>12}")

    corr_r, corr_h = con.execute(
        "SELECT round(corr(zori_log_growth, elasticity), 3), round(corr(zhvi_log_growth, elasticity), 3) "
        "FROM msa_rent_elasticity_panel").fetchone()
    q1, q4 = rows[0][3], rows[-1][3]
    print(f"\n  corr(rent growth, elasticity) = {corr_r}  | corr(home-value growth, elasticity) = {corr_h}")
    print(f"  most-inelastic Q1 rent {q1}%/yr vs most-elastic Q4 {q4}%/yr  →  spread {round(q1 - q4, 2)} pp/yr")

    if corr_r is None:
        _warn("corr undefined")
    elif corr_r <= -0.20:
        _ok(f"corr {corr_r}: supports the Wilson-Zhou supply leg (rents grew faster where supply is inelastic)")
    elif abs(corr_r) < 0.20:
        _warn(f"corr {corr_r}: ~NULL bivariate — elasticity ALONE does not predict 2016-25 rent growth. "
              "Expected: elasticity MODERATES a demand shock; the 2021-22 run-up was a broad rate/COVID shock, "
              "not metro-differentiated by supply. This is WHY the Δfb-share demand treatment is load-bearing.")
    else:
        _warn(f"corr {corr_r}: POSITIVE — opposite of the supply mechanism; inspect (name-match noise / composition)")
    print("\n  [GATED] the causal result (Δrent ~ Δfb-share × elasticity) needs metro foreign-born share over\n"
          "          time — Census API key OR Geocorr PUMA↔CBSA crosswalk. Staged; see HUMAN.md.")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(build())

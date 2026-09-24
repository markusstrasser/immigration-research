#!/usr/bin/env python3
"""QCEW private employment by state x industry cell x year, plus the national gates.

Input: _cache/qcew/qcew_state_<year>.csv.gz (fetch_qcew.py), 2005-2024, private ownership
(own_code 5). A cell is a signed sum of NAICS codes (cells.py). A cell with any suppressed
component (disclosure code N) is missing for that state and year; a suppressed subtrahend would
otherwise leak into the difference.

Outputs:
  _cache/panel/qcew_cells.parquet      year, st, cell, estabs, emp, wages, suppressed
  derived/qcew_national_sectors.csv    national private totals by NAICS sector, 2005-2024
  derived/gates_qcew.csv               the national gates (below)

Gates:
  1. National private sector totals from the singlefiles equal, sector by sector, the rows of the
     BLS open-data slice for US000 that feeds the published Table 2 of "Employment and Wages,
     Annual Averages" (https://data.bls.gov/cew/data/api/<year>/a/area/US000.csv), 2019 and 2023.
  2. The national private total equals the publication's text, "an average of 126.4 million wage
     and salary employees in approximately 9.9 million business establishments" (2019) and
     "131.3 million ... 11.6 million" (2023), to the printed rounding.
  3. The state cells of each year sum to at least 99% of the state private totals, less
     unclassified establishments (NAICS 99), where nothing is suppressed.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/qcew_cells.py
"""
from __future__ import annotations

import csv
import io
import subprocess
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import CELLS, OUTCOMES  # noqa: E402

SRC = HERE / "_cache" / "qcew"
OUT = HERE / "_cache" / "panel" / "qcew_cells.parquet"
NAT = HERE / "derived" / "qcew_national_sectors.csv"
GATES = HERE / "derived" / "gates_qcew.csv"
SECTORS = ["11", "21", "22", "23", "31-33", "42", "44-45", "48-49", "51", "52", "53", "54", "55",
           "56", "61", "62", "71", "72", "81", "99"]
PUBLISHED = {  # year: (employment millions, establishments millions) as printed
    2019: (126.4, 9.9),
    2023: (131.3, 11.6),
}
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")


def api_slice(year: int) -> dict[str, tuple[int, int, int]]:
    cache = HERE / "_cache" / "qcew" / f"api_US000_{year}.csv"
    if not cache.exists():
        r = subprocess.run(["curl", "-sS", "--fail", "-A", UA, "-H", 'sec-ch-ua: "Chromium";v="128"',
                            "-o", str(cache), f"https://data.bls.gov/cew/data/api/{year}/a/area/US000.csv"])
        if r.returncode != 0:
            raise SystemExit(f"[FAILED] API slice {year}: curl exit {r.returncode}")
    rows = list(csv.DictReader(io.StringIO(cache.read_text())))
    if not rows or "annual_avg_emplvl" not in rows[0]:
        raise SystemExit(f"[FAILED] API slice {year}: unexpected content")
    return {r["industry_code"]: (int(r["annual_avg_estabs"]), int(r["annual_avg_emplvl"]),
                                 int(r["total_annual_wages"]))
            for r in rows if r["own_code"] == "5" and r["industry_code"] in SECTORS}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='2GB'; SET threads=4")
    con.execute(f"""CREATE TEMP TABLE q AS SELECT CAST(year AS INTEGER) AS year,
        TRY_CAST(substr(area_fips, 1, 2) AS INTEGER) AS st, area_fips, industry_code AS naics,
        coalesce(disclosure_code, '') = 'N' AS supp, CAST(annual_avg_estabs AS BIGINT) AS estabs,
        CAST(annual_avg_emplvl AS BIGINT) AS emp, CAST(total_annual_wages AS DOUBLE) AS wages
        FROM read_csv('{SRC}/qcew_state_*.csv.gz', header=true, all_varchar=true)
        WHERE own_code = '5' AND size_code = '0'""")
    terms = []
    for cell, spec in {**{c: s["qcew"] for c, s in CELLS.items()}, **OUTCOMES}.items():
        for sign, code in spec:
            terms.append((cell, sign, code))
    con.execute("CREATE TEMP TABLE t (cell VARCHAR, sign INTEGER, naics VARCHAR)")
    con.executemany("INSERT INTO t VALUES (?, ?, ?)", terms)
    # st 0 is the nation (area US000)
    con.execute(f"""COPY (
        SELECT q.year, coalesce(q.st, 0) AS st, t.cell,
          sum(t.sign * q.estabs) AS estabs, sum(t.sign * q.emp) AS emp, sum(t.sign * q.wages) AS wages,
          bool_or(q.supp) AS suppressed, count(*) AS n_terms,
          (SELECT count(*) FROM t t2 WHERE t2.cell = t.cell) AS n_terms_expected
        FROM q JOIN t USING (naics)
        GROUP BY q.year, coalesce(q.st, 0), t.cell) TO '{OUT}' (FORMAT parquet)""")
    # national sector totals
    nat = con.execute(f"""SELECT year, naics, estabs, emp, wages, supp FROM q
        WHERE area_fips = 'US000' AND naics IN ({','.join("'" + s + "'" for s in SECTORS)})
        ORDER BY year, naics""").fetchall()
    NAT.parent.mkdir(parents=True, exist_ok=True)
    with open(NAT, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "naics_sector", "estabs", "emp", "wages", "suppressed"])
        w.writerows(nat)
    gates = []
    by = {(y, n): (e, m, wg) for y, n, e, m, wg, s in nat}
    for year, (emp_pub, est_pub) in PUBLISHED.items():
        api = api_slice(year)
        diffs = [n for n in SECTORS if n in api and by.get((year, n)) != (api[n][0], api[n][1], int(api[n][2]))]
        gates.append(("sector_totals_equal_published_table2_source", year, len(api), len(diffs) == 0,
                      f"{len(api)} sectors compared; differing: {diffs}"))
        tot = con.execute(f"""SELECT emp, estabs FROM q WHERE area_fips = 'US000' AND naics = '10'
            AND year = {year}""").fetchone()
        ok = abs(tot[0] / 1e6 - emp_pub) <= 0.05 and abs(tot[1] / 1e6 - est_pub) <= 0.05
        gates.append(("private_total_equals_publication_text", year, 1, ok,
                      f"file {tot[0] / 1e6:.3f}m employees, {tot[1] / 1e6:.3f}m establishments; "
                      f"printed {emp_pub}m and {est_pub}m"))
    # the partition, applied to the national rows (no suppression there), covers private employment
    # outside unclassified establishments exactly once
    cover = con.execute("""WITH c AS (SELECT q.year, sum(t.sign * q.emp) emp, bool_or(q.supp) sup
              FROM q JOIN t USING (naics) WHERE q.area_fips = 'US000' AND t.cell LIKE 'c%' GROUP BY 1),
        tot AS (SELECT year, emp FROM q WHERE area_fips = 'US000' AND naics = '10'),
        unc AS (SELECT year, emp FROM q WHERE area_fips = 'US000' AND naics = '99')
        SELECT count(*), count(*) FILTER (WHERE NOT c.sup AND abs(c.emp / (tot.emp - coalesce(unc.emp, 0)) - 1) < 0.001),
          min(c.emp / (tot.emp - coalesce(unc.emp, 0))), max(c.emp / (tot.emp - coalesce(unc.emp, 0)))
        FROM c JOIN tot USING (year) LEFT JOIN unc USING (year)""").fetchone()
    gates.append(("cells_partition_national_private_total", "2005-2024", cover[0], cover[0] == cover[1] == 20,
                  f"{cover[1]} of {cover[0]} years within 0.1%; ratio {cover[2]:.5f}-{cover[3]:.5f}"))
    share = con.execute(f"""WITH c AS (SELECT year, st, sum(emp) FILTER (WHERE NOT suppressed) ok_emp
              FROM '{OUT}' WHERE cell LIKE 'c%' AND st > 0 GROUP BY 1, 2),
        tot AS (SELECT year, st, emp FROM q WHERE naics = '10' AND area_fips <> 'US000')
        SELECT quantile_cont(1 - ok_emp / tot.emp, [0.5, 0.9]), max(1 - ok_emp / tot.emp)
        FROM c JOIN tot USING (year, st)""").fetchone()
    gates.append(("state_employment_in_suppressed_cells", "2005-2024", 1020, True,
                  f"share of state private employment in a cell with a suppressed component: median "
                  f"{share[0][0]:.4f}, p90 {share[0][1]:.4f}, max {share[1]:.4f} (informational)"))
    with open(GATES, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["gate", "year", "n", "pass", "detail"])
        w.writerows(gates)
    for g in gates:
        print(("✓" if g[3] else "✗"), g[0], g[1], g[4])
    n, sup = con.execute(f"SELECT count(*), count(*) FILTER (WHERE suppressed) FROM '{OUT}'").fetchone()
    print(f"  {OUT.name}: {n:,} state x series x year rows, {sup:,} with a suppressed component")
    if not all(g[3] for g in gates):
        raise SystemExit("[FAILED] a QCEW gate failed")


if __name__ == "__main__":
    main()

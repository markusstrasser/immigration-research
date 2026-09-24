#!/usr/bin/env python3
"""Check the IPUMS extracts against their codebooks and IPUMS's published counts, then write the
analysis files: movers with weights, interstate movers with replicate weights, and state-year
population cells.

Reads (all under _cache/, git-ignored):
  ipums/cps_main.csv.gz + cps_main.xml     ASEC 1999-2025, every person (extract 2)
  ipums/cps_repwt.csv.gz + cps_repwt.xml   ASEC 2005-2025, interstate movers, REPWTP1-160 (extract 3)
  ipums_doc/*_frequencies.json, *.html     IPUMS's published per-sample case counts
Writes:
  _cache/build/movers.parquet        persons 1+ who moved inside the US (MIGRATE1 3, 4, 5)
  _cache/build/repwt.parquet         interstate movers 2005-2025, 160 replicate weights
  _cache/build/state_cells.parquet   weighted state-year cells for composition and rates
  derived/gate_extract.csv           gate G1 rows (codebook vs header, rows vs IPUMS counts)
  derived/whymove_counts_by_year.csv unweighted WHYMOVE counts by year, all movers (data quality)

The 2014 ASEC holds two files (HFLAG 0 = 5/8 file, 1 = 3/8 file), each weighted to the full
population (313.4M each), so pooling both double-counts 2014. Weights in 2014 are multiplied by
the file's share of 2014 person records; replicate weights get the same factor.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/build_cps.py
"""
import csv
import json
import re
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
IPUMS = CACHE / "ipums"
DOC = CACHE / "ipums_doc"
BUILD = CACHE / "build"
DERIVED = HERE / "derived"
MAIN = IPUMS / "cps_main.csv.gz"
REPWT = IPUMS / "cps_repwt.csv.gz"


def ddi_vars(xml: Path) -> list[str]:
    return re.findall(r'<var ID="([A-Z0-9_]+)"', xml.read_text(encoding="latin-1"))


def csv_header(gz: Path, con) -> list[str]:
    return [r[0] for r in con.execute(f"describe select * from read_csv('{gz}', header=true, sample_size=1000)").fetchall()]


def ipums_published(var: str) -> dict[tuple[str, str], int]:
    """(year, code) -> unweighted case count as IPUMS publishes it on the variable page."""
    raw = (DOC / f"{var}.html").read_text(errors="replace")
    cats = json.loads(re.search(r"categories: (\[.*?\]),\n", raw).group(1))
    samples = json.loads(re.search(r"samples: (\[.*?\]),\n", raw).group(1))
    sid = {str(s["id"]): s["name"][3:7] for s in samples}
    cid = {str(c["id"]): c["code"] for c in cats if c["code"] is not None}
    freq = json.loads((DOC / f"{var}_frequencies.json").read_text())
    out = {}
    for s, row in freq.items():
        for c, v in row.items():
            if c in cid and v.get("availability") == "X":
                out[(sid[s], cid[c])] = int(v["count"])
    return out


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='1500MB'; SET threads=2; SET preserve_insertion_order=false")
    gates = []

    # G1a: codebook variables equal the CSV header, in order
    for gz, xml in ((MAIN, IPUMS / "cps_main.xml"), (REPWT, IPUMS / "cps_repwt.xml")):
        d, h = ddi_vars(xml), csv_header(gz, con)
        ok = d == h
        gates.append({"gate": "G1a codebook = header", "file": gz.name, "detail": f"{len(d)} codebook vars, {len(h)} header columns",
                      "value": "identical" if ok else f"diff {sorted(set(d) ^ set(h))[:10]}", "pass": ok})

    main_types = {"HFLAG": "INTEGER", "QWHYMOVE": "INTEGER", "COUNTYERR": "INTEGER", "HHINCOME": "BIGINT",
                  "INCTOT": "BIGINT", "CPSID": "BIGINT", "CPSIDP": "BIGINT", "CPSIDV": "BIGINT"}
    tj = ", ".join(f"'{k}': '{v}'" for k, v in main_types.items())
    con.execute(f"create or replace view raw as select * from read_csv('{MAIN}', header=true, types={{{tj}}})")

    # G1b: per-year row counts and MIGRATE1 / WHYMOVE code counts against IPUMS's published counts
    rows = {str(y): n for y, n in con.execute("select YEAR, count(*) from raw group by 1").fetchall()}
    for var in ("MIGRATE1", "WHYMOVE"):
        pub = ipums_published(var)
        mine = {(str(y), f"{c:02d}" if var == "WHYMOVE" else str(c)): n
                for y, c, n in con.execute(f"select YEAR, {var}, count(*) from raw group by 1, 2").fetchall()}
        years = sorted({y for y, _ in pub})
        bad = [(k, pub[k], mine.get(k, 0)) for k in pub if pub[k] != mine.get(k, 0)]
        gates.append({"gate": f"G1b {var} counts = IPUMS published", "file": MAIN.name,
                      "detail": f"{len(pub)} year-code cells over {len(years)} samples published by IPUMS ({years[0]}-{years[-1]}, no 2021 on the page)",
                      "value": "all equal" if not bad else f"{len(bad)} differ, e.g. {bad[:3]}", "pass": not bad})
        if var == "MIGRATE1":
            tot = {y: sum(v for (yy, _), v in pub.items() if yy == y) for y in years}
            badr = [(y, tot[y], rows.get(y)) for y in years if tot[y] != rows.get(y)]
            gates.append({"gate": "G1b rows per sample = IPUMS published", "file": MAIN.name,
                          "detail": f"{len(years)} samples; total rows {sum(rows.values()):,} over 27 samples",
                          "value": "all equal" if not badr else f"differ {badr[:3]}", "pass": not badr})

    # 2014 split-file weight factor
    f = dict(con.execute("""select HFLAG, count(*) * 1.0 / sum(count(*)) over () from raw where YEAR = 2014
                           group by 1""").fetchall())
    if set(f) != {0, 1}:
        sys.exit(f"[FAILED] unexpected 2014 HFLAG values {f}")
    fexpr = f"case when YEAR = 2014 and HFLAG = 0 then {f[0]!r} when YEAR = 2014 and HFLAG = 1 then {f[1]!r} else 1.0 end"
    gates.append({"gate": "2014 split files", "file": MAIN.name, "detail": "weight factors by HFLAG (share of 2014 records)",
                  "value": f"HFLAG0 {f[0]:.4f}, HFLAG1 {f[1]:.4f}", "pass": True})

    con.execute(f"""
      create or replace table movers as
      select YEAR, SERIAL, PERNUM, coalesce(HFLAG, -1) as HFLAG, ASECWT * ({fexpr}) as wt,
             ASECWTH * ({fexpr}) as wth, STATEFIP, COUNTY, coalesce(COUNTYERR, 0) as COUNTYERR, METFIPS,
             MIGRATE1, MIGSTA1, WHYMOVE, QMIGRAT1, QMIGST1B, coalesce(QWHYMOVE, -1) as QWHYMOVE, QMIGRAT1G,
             NATIVITY, BPL, CITIZEN, HISPAN, RACE, AGE, SEX, EDUC, INCTOT, HHINCOME, CPI99, OWNERSHP, RELATE
      from raw where MIGRATE1 in (3, 4, 5)""")
    con.execute(f"copy movers to '{BUILD / 'movers.parquet'}' (format parquet)")
    n_movers = con.execute("select count(*) from movers").fetchone()[0]

    # state-year cells: residents now, and US-born adults by state of residence one year earlier
    con.execute(f"""
      create or replace table cells as
      select YEAR, STATEFIP as state, 'now' as basis,
             sum(ASECWT * ({fexpr})) as pop,
             sum(case when HISPAN between 1 and 612 then ASECWT * ({fexpr}) else 0 end) as hisp,
             sum(case when HISPAN between 100 and 109 then ASECWT * ({fexpr}) else 0 end) as mex,
             sum(case when BPL = 9900 and AGE >= 18 then ASECWT * ({fexpr}) else 0 end) as usborn_adult,
             count(*) as n
      from raw group by 1, 2
      union all
      select YEAR, case when MIGRATE1 = 5 then MIGSTA1 else STATEFIP end as state, 'year_ago' as basis,
             sum(ASECWT * ({fexpr})), null, null,
             sum(case when BPL = 9900 and AGE >= 18 then ASECWT * ({fexpr}) else 0 end), count(*)
      from raw where MIGRATE1 in (1, 3, 4, 5) group by 1, 2""")
    con.execute(f"copy cells to '{BUILD / 'state_cells.parquet'}' (format parquet)")

    # WHYMOVE counts by year for the data-quality record
    wm = con.execute("select YEAR, WHYMOVE, count(*) from raw where MIGRATE1 in (3, 4, 5) group by 1, 2 order by 1, 2").fetchall()
    with open(DERIVED / "whymove_counts_by_year.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["year", "whymove", "n_movers_unweighted"])
        w.writerows(wm)

    # replicate weights: join to the main extract and check the universe
    rtypes = {"HFLAG": "INTEGER", "CPSID": "BIGINT", "CPSIDP": "BIGINT", "CPSIDV": "BIGINT"}
    rj = ", ".join(f"'{k}': '{v}'" for k, v in rtypes.items())
    reps = ", ".join(f"REPWTP{i} * ({fexpr}) as r{i}" for i in range(1, 161))
    con.execute(f"""create or replace table repwt as
                    select YEAR, SERIAL, PERNUM, ASECWT as asecwt_rep, {reps}
                    from read_csv('{REPWT}', header=true, types={{{rj}}})""")
    chk = con.execute("""
      select count(*) as n_rep,
             (select count(*) from movers where MIGRATE1 = 5 and YEAR >= 2005) as n_main,
             count(m.YEAR) as n_joined
      from repwt r left join movers m using (YEAR, SERIAL, PERNUM)""").fetchone()
    dup = con.execute("select count(*) from (select YEAR, SERIAL, PERNUM from repwt group by all having count(*) > 1)").fetchone()[0]
    wdiff = con.execute("""select max(abs(r.asecwt_rep - m.wt / (case when m.YEAR = 2014 and m.HFLAG = 0 then ? when m.YEAR = 2014 then ? else 1 end)))
                           from repwt r join movers m using (YEAR, SERIAL, PERNUM)""", [f[0], f[1]]).fetchone()[0]
    ok = chk[0] == chk[1] == chk[2] and dup == 0 and wdiff < 0.01
    gates.append({"gate": "G1c replicate extract = interstate movers of main extract", "file": REPWT.name,
                  "detail": f"rows {chk[0]:,}; main MIGRATE1=5 2005+ {chk[1]:,}; joined {chk[2]:,}; duplicate keys {dup}; max ASECWT diff {wdiff:.4f}",
                  "value": "consistent" if ok else "INCONSISTENT", "pass": ok})
    con.execute(f"copy repwt to '{BUILD / 'repwt.parquet'}' (format parquet)")

    with open(DERIVED / "gate_extract.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["gate", "file", "detail", "value", "pass"], lineterminator="\n")
        w.writeheader()
        w.writerows(gates)
    for g in gates:
        print(("PASS " if g["pass"] else "FAIL ") + f"{g['gate']}: {g['detail']} -> {g['value']}")
    print(f"movers written: {n_movers:,}")
    if not all(g["pass"] for g in gates):
        sys.exit(1)


if __name__ == "__main__":
    main()

# IPUMS USA extract store

**Verdict:** all 14 IPUMS USA extracts we hold (numbers 2–15; 1 was superseded) now sit in one store:
97.5 million person records, 1.64 GB compressed, cataloged, converted to typed Parquet (1.13 GB)
and joinable in one DuckDB file. Extracts 7 and 8 were downloaded today and match IPUMS's
sha256. The 55 pairs of extracts that share a sample were joined on YEAR, SAMPLE, SERIAL and
PERNUM. In the 46 whose universes overlap, every record found its counterpart. The 788 shared
columns compared show no disagreement, so allocation flags and SEX carry across extracts person
by person. The other 9 pairs have disjoint universes (US-born against Mexico-born). All 103
gates pass [DATA: `derived/joins.csv`, `derived/gates.csv`].

Catalog: [`CATALOG.md`](../../../sources/immigration-fiscal/data/external/ipums/usa_extract/CATALOG.md)
(ignored store; tracked copy in [`derived/CATALOG.md`](derived/CATALOG.md)). It has one row per
extract with samples, universe, variables, rows, bytes, sha256 and the lanes that used it, plus
one line per extract on what else it can answer.

## What is held

| # | Store name (`usa_extract/`) | Rows | From lane |
|---|---|---|---|
| 2 | `usa_00002_census1980-2000+acs2010+acs2023_all` | 44,393,133 | June browser extract (Borjas panel) |
| 3 | `usa_00003_census1980-2000+acs2005-2024_mexborn` | 2,575,058 | schooling_selection_position |
| 4 | `usa_00004_census1980-2000_men18-40` | 6,558,144 | crime_selection_cohorts |
| 5 | `usa_00005_acs2006-2024-no2020_mexborn-men18-40_repwt` | 361,850 | crime_selection_cohorts |
| 6 | `usa_00006_census1980-2000_men18-40_qflags` | 6,558,144 | crime_selection_cohorts |
| 7 | `usa_00007_acs2019+2023+2024_usborn-men18-40_repwt` | 1,207,425 | crime (submitted), this lane (downloaded) |
| 8 | `usa_00008_acs2006-2024-no2020_usborn-men18-40` | 6,684,204 | crime (submitted), this lane (downloaded) |
| 9 | `usa_00009_acs2019+2023+2024_usborn-men18-40` | 1,207,425 | crime_selection_cohorts |
| 10 | `usa_00010_census2000+acs2010+acs2009-2011_age16-64` | 16,851,363 | ancestry_iv_congestion_wages |
| 11 | `usa_00011_census1990_age16-64` | 7,937,859 | ancestry_iv_congestion_wages |
| 12 | `usa_00012_acs2000-2004_mexborn` | 109,834 | schooling_selection_position |
| 13 | `usa_00013_census1980-2000+acs2000-2024_mexborn_qeduc` | 2,684,892 | schooling_selection_position |
| 14 | `usa_00014_census1980-2000_inst-men18-40_qflags` | 121,364 | crime_selection_cohorts |
| 15 | `usa_00015_census2000_inst-allages_qflags` | 200,397 | crime_selection_cohorts |

Slugs read `<samples>_<universe>[_<content>]`. Every name is a hard link to the lane's own cache
file (`catalog.json` → `same_file_as`), so no lane path changed and no bytes were copied. Extract 1
(same samples as 2, fewer variables) was never downloaded. The files of extracts 1 and 2 have
expired at IPUMS, so `usa_extract/usa_00002.csv.gz` is the only copy of 2 and no DDI exists for it.

## What was added

- **Extracts 7 and 8**, downloaded through the API: 152,975,361 and 127,611,443 bytes, sha256
  equal to IPUMS's published values, DDIs too. They are hard-linked into the crime lane as
  `_cache/ipums/acs_movers.{csv.gz,xml}` and `acs_us.{csv.gz,xml}`; that lane's own
  `ipums_extract.py download` will find them and skip the fetch.
- **DDI codebooks for 3, 12 and 13**, whose lane kept only the basic `.cbk`, fetched from the API
  (sha256 match).
- **Typed Parquet**, one file per extract in `sources/immigration-fiscal/derived/ipums_usa/`, with
  types from the DDI widths (TINYINT to BIGINT, DOUBLE for the weights) and a `manifest.json` of
  source hashes and column types.
- **`sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb`**:
  - views `usa_00002` … `usa_00015`;
  - `qflags`: one row per person record covered by the flag extracts 6, 13, 14 and 15, carrying
    QBPL, QYRIMM, QEDUC and QCITIZEN. NULL means the flag was not extracted for that record, 0
    means reported as written. `q_extracts` lists the sources;
  - `usa_000NN_q` for the seven extracts whose people the flag extracts cover (2, 3, 4, 5, 10, 11
    and 12): the extract plus its flags;
  - `usa_00002_sex`: extract 2 plus SEX (below);
  - tables `catalog`, `variables` (486 columns with label, DDI width and type source),
    `value_labels` (21,504 codes from the DDIs), `joins` and `gates`.
- **Registration**: 27 sha256 lines in the raw-file `MANIFEST.md`, a section in
  `external/ipums/README.md`, and the register card `IPUMS_USA_EXTRACTS_2026_09_23`.

## Join match rates

Every pair that shares a sample, restricted to the records inside both universes. In 10 pairs
only one direction can be tested, because one extract lacks the other's selection variable
(extract 2 has no SEX; extract 13 has no SEX or AGE). Matched means found on all four keys.

| Pair | What it attaches | Records tested | Matched |
|---|---|---|---|
| 6 → 4 | QBPL, QYRIMM, QEDUC to census men 18–40 | 6,558,144 both ways | 100% |
| 13 → 3 | QEDUC to the Mexico-born, 1980–2024 | 2,575,058 both ways | 100% |
| 13 → 12 | QEDUC to the Mexico-born, ACS 2000–2004 | 109,834 both ways | 100% |
| 14 ↔ 15, 2000 | QBPL, QCITIZEN agree for institutional men 18–40 | 62,336 both ways | 100% |
| 14 → 4 | QCITIZEN to institutional men, 1980–2000 | 121,364 both ways | 100% |
| 13 → 5 | QEDUC to Mexico-born men 18–40 with replicate weights | 361,850 | 100% |
| 6 → 10, 6 → 11 | flags to the 2000 and 1990 wage files | 2,262,402 and 2,236,671 | 100% |
| 4, 6, 14 → 2 | the Borjas panel's young men | 6,558,144; 6,558,144; 121,364 | 100% |
| 10 ↔ 2, 11 ↔ 2 | the Borjas panel's ages 16–64, 1990–2010 | 10,948,875 and 7,937,859 both ways | 100% |
| 3 ↔ 2, 13 ↔ 2 | the Borjas panel's Mexico-born | 967,300 both ways | 100% |
| 7 ↔ 9, 7 ↔ 8, 8 ↔ 9 | US-born men 18–40, 2019/2023/2024 | 1,207,425 both ways | 100% |
| 8 ↔ 10 | US-born men 18–40, ACS 2010 | 349,809 both ways | 100% |

The other 27 overlapping pairs also match at 100%; `derived/joins.csv` lists all 55 with the
columns compared. Record by record, the shared variables are identical across extracts (AGE, BPLD,
EDUCD, PERWT, CLUSTER, STRATA and the rest). That holds for June's extract 2 as well, so the June
and September files come from the same IPUMS data release. Negative control: comparing AGE with
AGE + 1 over the 10,948,875 matched records of 2 and 10 flags every one of them.

## Gates

103 gates, all pass [DATA: `derived/gates.csv`]:
- per extract: data sha256 and bytes equal to IPUMS's published values (13; extract 2 has none
  and its hash is now recorded for the first time), DDI sha256 (13), Parquet rows equal to the
  CSV line count (14), unique person key (14), no record outside the extract's own case selection
  (14), and every requested sample present (14);
- `qflags`: no record has different QBPL, QYRIMM, QEDUC or QCITIZEN values in two extracts;
- `usa_00002_sex`: SEX never conflicts across extracts, and both absence rules hold where SEX is
  observed directly.

Neither the API nor the DDI publishes a record count, so the row gate counts the CSV lines
independently of DuckDB. One external count agrees exactly: extract 3 holds 967,300 Mexico-born
records in extract 2's five samples, the schooling lane's figure for the held panel.

## What the store answers that it could not before

- **Imputation checks outside the lanes that requested them.** Any analysis of men 18–40 in
  1980–2000, of the Mexico-born in any year from 1980 to 2024, or of the institutionalized can now
  drop or reweight records with allocated birthplace, arrival year, education or citizenship
  (`usa_000NN_q`). Example: the weighted share of Mexico-born people whose education was edited
  or allocated (QEDUC > 0) rose from about 7% in the ACS 2001–2005 to 16–18% in 2020–2024
  [CALCULATION: `SELECT YEAR, sum(PERWT * (QEDUC > 0)::INT) / sum(PERWT) FROM usa_00013 GROUP BY 1`].
- **The Borjas panel by sex, with no new extract.** Extract 2 never had SEX. `usa_00002_sex` takes
  it from extracts 3, 4, 8, 10 and 11 for the same people. Two groups get it by absence, because
  the source extract holds every man in them: 1980 ages 18–40 missing from extract 4, and 2023
  US-born ages 18–40 missing from extract 8, are women. The absence rule was tested where SEX is
  observed directly: 1990 and 2000 against extract 4 (0 men among 4,541,087 records) and 2010
  against extract 8 (0 men among 351,997). Weighted coverage: 37% (1980), 65% (1990), 65% (2000),
  66% (2010), 29% (2023). Known-sex ratios are 0.98–1.03 men per woman
  [DATA: `derived/sex_coverage.csv`]. The same join gives the 1990–2010 working-age panel
  INCWAGE, hours, weeks and commute from extracts 10 and 11.
- **Replicate-weight standard errors for US-born young men** (extract 7). The crime lane's mover
  comparison used a household jackknife that may understate SEs by up to 30% (its RESULT.md,
  section 3b). It can now use the 80 replicate weights.
- **Native reference rates by single year of age, 2006–2024** (extract 8). The Census API
  tabulate endpoint could not provide these by age in the early years.

## Layout

- `organize.py`: every step, idempotent, one line per item, deletes nothing.
- `derived/` (tracked): `catalog.json` and `CATALOG.md` (copies of the store's), `joins.csv`,
  `gates.csv`, `sex_coverage.csv`.
- `_cache/` (ignored): API definitions (`api/extract_NN.json`, the operator's email stripped),
  `api/published.json` (IPUMS's hashes, kept after files expire), the downloads of 7 and 8 and
  the fetched DDIs (`downloads/`, same inodes as the store names), and hash and row-count caches.
- Store: `sources/immigration-fiscal/data/external/ipums/usa_extract/` holds `catalog.json`,
  `CATALOG.md`, the original `usa_00002.csv.gz` and the 14 named data files with 13 DDIs.

## Reproduce

```sh
# from the repository root; about 2 minutes once 7 and 8 are downloaded (their download took 9)
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
  infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py            # all steps
# or any of: api download ddi link verify count parquet duckdb joins catalog register
```

The api, download and ddi steps read `IPUMS_API_KEY` from `acquire/config.local.env` and never
print it. A name that already exists is skipped if it is the same inode (or, for a separate copy,
the same sha256); otherwise the run stops. An existing Parquet file whose source hash differs
also stops the run instead of being overwritten.

## Limits and traps

- **The Borjas loader is pinned.** `build/load_ipums_borjas_panel.py` resolves `usa_00002.csv.gz`
  by exact name since 4767db7. Before that it loaded the last-sorting `usa_*.csv.gz` in
  `usa_extract/`, and the slugged names would have made it load extract 15.
- **Views hold absolute Parquet paths.** After moving the repository, re-run
  `organize.py duckdb joins catalog`.
- **Extract 2 has no DDI.** Its column types come from the DDIs of other extracts. WKSWORK1 and
  INCTOT appear in none, so they use the IPUMS widths (2 and 7 digits). A value that did not fit
  would have stopped the typed read.
- **Institution type exists only in 1980.** In the 1990 and 2000 files, GQTYPE/GQTYPED say
  "institution" for every institutional record, so extract 15 cannot separate prisons from
  nursing homes; age has to stand in.
- **Universes:** "US-born" in 7–9 means the 50 states and DC (Puerto Rico and other territories
  excluded). Extracts 5 and 8 skip 2020. Extract 12's ACS 2000–2004 samples cover households only.
  Extract 10's `us2011c` is the 2009–2011 three-year ACS (YEAR 2011; MULTYEAR gives the survey
  year).
- The first `duckdb` run built `_q` views for 7, 8 and 9, whose flags could only ever be NULL:
  those extracts share samples with 13 but no people. The step now requires overlapping
  universes, and those three views were dropped by hand once.

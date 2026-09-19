# Lane: the real size of the Mexican-origin population (2026-09-19)

How many people of Mexican origin live in the United States, by generation, under
each defensible definition; how much of the standing 40.9M figure is missing because
of ethnic attrition and survey coverage; and what the larger population does to the
fiscal gap. Findings: [RESULT.md](RESULT.md).

## Reproduce

From this directory. Every script takes the same interpreter line; none of them
downloads anything except the paper PDFs, and none writes outside this lane.

```sh
R='uv run --no-project --with pandas>=2 --with numpy>=2 --with duckdb --with requests --with pyarrow python3'

PYTHONUNBUFFERED=1 $R extract_cps.py          # -> _cache/cps_asec2025_person_subset.parquet
PYTHONUNBUFFERED=1 $R extract_acs.py          # -> _cache/acs2024_ancestry_subset.parquet
PYTHONUNBUFFERED=1 $R cps_counts.py           # arm 1 + arm 3 attrition rates
PYTHONUNBUFFERED=1 $R acs_ancestry.py         # arm 2 ancestry
PYTHONUNBUFFERED=1 $R dt_replication.py       # arm 3b strict Duncan-Trejo replication
PYTHONUNBUFFERED=1 $R bounds_coverage_fiscal.py   # arm 3c bounds, arm 4, arm 5
PYTHONUNBUFFERED=1 $R allocation_check.py     # imputation disconfirmation arm
```

`bounds_coverage_fiscal.py` reads `derived/arm3_multiplier.csv` and
`derived/arm3_grandparent_counts.csv`, so run `cps_counts.py` and `dt_replication.py`
before it. The two extractors skip their work when the cache file already exists;
delete `_cache/*.parquet` to force a cold rebuild.

Verified 2026-09-19, twice: re-running all seven scripts over the existing `_cache/`
leaves every file in `derived/` byte-identical (`shasum -a 256 derived/* | sort`
before and after, no difference). The extractors are the only step not re-executed on
those runs, and they are pure column selection plus a deterministic sort, so the cache
is a function of the read-only raw files alone. `derived/` is 84 KB across 20 files;
nothing approaches the 5 MB cap.

## Inputs (all read-only)

| Input | Path |
|---|---|
| CPS ASEC 2025 person file + 160 replicate weights | `~/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip` |
| ACS 2024 1-year PUMS person files + 80 replicate weights | `~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip` |
| ACS 2024 PUMS data dictionary | `~/research-data/immigration-fiscal/data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.csv` |
| CPS ASEC 2025 data dictionary and technical documentation | `~/research-data/immigration-fiscal/data/external/cps_asec_doc/{ddl25.txt,cpsmar25.pdf}` |
| All-age fiscal ledger, per-person and aggregate gaps | `../all_age_ledger_2026_09_17/derived/estimates.csv` |
| Unauthorized share of the Mexico-born (CPS residual) | `../unauthorized_population_size_2026_09_19/derived/cps2025_residual_by_region.csv` |
| Census Bureau 2024 ASEC generation table | `../acs_institutional_2026_09_16/cps_2024_asec_generation_table4.xlsx` |

Papers, downloaded to `_cache/papers/` (gitignored) and read as PDFs:

| Paper | File | Route |
|---|---|---|
| Duncan & Trejo 2011, JOLE 29(2):195–227 | `dt2011_jole_cream.pdf` | research MCP `fetch_paper` DOI 10.1086/658088 (CReAM DP 02/09 copy) |
| Duncan & Trejo 2017, ILR Review 71(5) | `dt2017_ilr.pdf` | research MCP `fetch_paper` DOI 10.1177/0019793916679613 |
| Duncan & Trejo 2025, AEA P&P 115:451–56 / IZA DP 17579 | `dp17579.pdf` | `https://docs.iza.org/dp17579.pdf` |
| 2020 PES net coverage by race and Hispanic origin | `_cache/sources/pes_net_coverage_race_hispanic.pdf` | census.gov |

Emeka & Vallejo 2011 (Social Science Research 40(6)) has no open PDF and was **not**
obtained; its headline 6% is marked `[UNVERIFIED]` in RESULT.md and the same statistic
is rebuilt directly on ACS 2024 instead.

## Key variable codes

`PENATVTY` / `PEMNTVTY` / `PEFNTVTY` country codes: 057 United States, 060 American
Samoa, 066 Guam, 069 Northern Marianas, 073 Puerto Rico, 078 U.S. Virgin Islands,
303 Mexico. [SOURCE: CPS March 2025 technical documentation, Appendix J, p. J-1]
`PRDTHSP` = 1 is Mexican, universe `PEHSPNON` = 1. `PEPAR1` / `PEPAR2` are the line
numbers of the child's parents within the household, so a child's grandparents'
birthplaces are read off the linked parent's own `PEMNTVTY` / `PEFNTVTY`.
`PEPAR1TYP` / `PEPAR2TYP` distinguish biological (1) from step (2) and adopted (3)
parents, which the strict replication arm uses.

ACS: `HISP` = 02 Mexican; `POBP` = 303 Mexico; Mexican ancestry is `ANC1P` or `ANC2P`
in {210 Mexican, 211 Mexican American, 212 Mexicano, 213 Chicano, 215 Mexican American
Indian, 218 Mexican State, 219 Mexican Indian}.

Standard errors are successive-difference replication throughout: variance factor
4/160 on the CPS ASEC and 4/80 on the ACS PUMS.

## Outputs

| File | Contents |
|---|---|
| `arm1_counts_cps.csv` | twelve definitions of the Mexican-origin population with SDR standard errors |
| `arm1_definition_notes.json` | codes, weights, record counts, headline totals |
| `arm2_ancestry_crosstab.csv` | ancestry against Hispanic origin, ACS 2024 |
| `arm2_ancestry_by_nativity.csv` | the same split foreign-born / US-born |
| `arm2_ancestry_totals.csv` | what the ancestry question adds over self-identification |
| `arm2_emeka_vallejo.csv` | share of Latin American ancestry answering "not Hispanic", 2024 |
| `arm3_attrition_children.csv` | attrition by generation, parentage, age band, grandparent count |
| `arm3_grandparent_counts.csv` | third-generation children by number of Mexico-born grandparents |
| `arm3_dt_table8_replication.csv` | Duncan & Trejo 2011 Table 8, replicated cell by cell |
| `arm3_dt_table8_replication_biological.csv` | the same, biological parents only |
| `arm3_dt_hispanic_definition.csv` | the Hispanic-identification outcome against Duncan & Trejo 2017 Table 1 |
| `arm3_dt_decomposition.csv` | composition versus rate decomposition of the 1994–2006 to 2025 change |
| `arm3_multiplier.csv` | the directly measured third-plus correction multiplier |
| `arm3_applied_correction.csv` | the floor correction applied to the standing counts |
| `arm3_correction_bounds.csv` | four assumptions on fourth-plus identification |
| `arm3_fractional_counting.csv` | quarter-per-grandparent convention against whole persons |
| `arm3_allocation_check.csv` | attrition on non-imputed records only |
| `arm4_coverage_grid.csv` | five coverage schemes applied to the union |
| `arm5_education_selectivity.csv` | the education gap the attriter advantage closes |
| `arm5_fiscal_implication.csv` | per-person and aggregate gap under 4 population × 3 characteristics arms |

## Scope

Resident stock, not admission. Every gap is a benchmark contrast against third-plus
non-Hispanic whites inside the all-age ledger's partial annual account, not a net
fiscal cost and not a policy counterfactual. No policy advice is given or implied.

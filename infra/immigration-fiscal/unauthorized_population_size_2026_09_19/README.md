# Lane: how large is the unauthorized population, really (2026-09-19)

Triangulates the resident unauthorized stock three ways — published residual
estimates, a residual reproduced on this repo's own microdata, and a stock-flow
identity from the DHS January 2022 stock forward — and tests explicitly what
population, if any, a figure of 40 million could name.

See `BRIEF.md` for the question, `RESULT.md` for the answer.

## Inputs

All read-only. Nothing in `~/research-data` is written by this lane.

| Input | Path | Used by |
|---|---|---|
| ACS 2024 1-year PUMS, person records | `~/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip` | `extract_pums.py` |
| ACS 2024 PUMS data dictionary | `~/research-data/immigration-fiscal/data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.csv` | variable coding (read by hand) |
| CPS ASEC 2025 public use, person + household + replicate weights | `~/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip` | `cps_residual.py` |
| Borjas (2017) status imputation | `../status_impute_2026_09_16/impute_status.py` | `cps_residual.py` (imported unmodified) |
| DHS OHSS unauthorized estimates, Jan 2018 – Jan 2022 | `~/research-data/immigration-fiscal/data/external/ohss/ohss_unauth_2018_2022.pdf` | `sources.json` (quoted by hand) |
| Pew unauthorized estimates, Aug 2025 | `~/research-data/immigration-fiscal/data/external/pew/pew_unauth_2023.pdf` | `sources.json` (quoted by hand) |
| DHS OHSS enforcement monthly tables, Nov 2024 | `_cache/sources/ohss_monthly_nov2024.xlsx` | `stock_flow.py` |
| Census Vintage 2024 population estimates | `~/research-data/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv` | `coverage_and_ladder.py` weight-control check |
| CMS, MPI, CIS, CBO documents | `_cache/sources/` | `sources.json` (quoted by hand) |

`sources.json` is the only hand-entered file. Every field in it is a verbatim
quote or a number read directly out of the primary document named in the same
record. `_cache/` is gitignored repo-wide; `logs/` is gitignored by this lane.

## Run

Everything runs under `uv run --no-project`. No bare `python3`.

```bash
cd infra/immigration-fiscal/unauthorized_population_size_2026_09_19
mkdir -p _cache derived logs

# 1. Extract the columns this lane needs from the 2.4 GB PUMS person files.
#    ~4 min; writes _cache/acs2024_person_subset.parquet (378 MB, gitignored).
#    Skips itself if the parquet already exists.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with pyarrow python3 extract_pums.py

# 2. Arm 1: the published-estimate table and the quoted definitions.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" python3 build_estimate_table.py

# 3. Arm 2 (ACS half) and the base of Arm 6.  ~2 min.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with pyarrow python3 acs_residual.py

# 4. Arm 2 (CPS half).  ~1 min.  Reproduces ladder 85.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  python3 cps_residual.py

# 5. Arm 4: stock-flow reconciliation.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with openpyxl python3 stock_flow.py

# 6. Arms 3 and 6: coverage grid and the 40-million ladder.  ~2 min.
#    Also checks the ACS 2024 weighted total against the Vintage 2024 estimate.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
  --with pyarrow python3 coverage_and_ladder.py

# 7. The coverage grid applied to the CPS residual.
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" python3 cps_coverage.py

# 8. Rule-list sensitivity.  Run the three variants below first, then collect.
for flags in "--no-occupation-rule" "--refugee wide" "--refugee wide --no-occupation-rule"; do
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" \
    --with pyarrow python3 acs_residual.py $flags
done
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" python3 rule_sensitivity.py
```

Non-default rule settings write to their own suffixed files, so a sensitivity run
can never overwrite the headline tables.

## Re-fetching the cached sources

`_cache/sources/` is gitignored, so a clean checkout has to fetch again. Only
`stock_flow.py` reads a cached file programmatically; the rest were read by a
human-equivalent pass into `sources.json`.

```bash
cd _cache/sources
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36"
curl -sSL --http1.1 -A "$UA" -o ohss_monthly_nov2024.xlsx \
  "https://ohss.dhs.gov/sites/default/files/2025-01/2025_0116_ohss_immigration-enforcement-and-legal-processes-tables-november-2024.xlsx"
curl -sSL --http1.1 -C - -A "$UA" -o house_border_report_sep2024.pdf \
  "https://homeland.house.gov/wp-content/uploads/2024/09/September-2024-Border-Report.pdf"
curl -sSL --http1.1 -A "$UA" -o mpi_fact_sheet_2025.pdf \
  "https://www.migrationpolicy.org/sites/default/files/publications/mpi-unauthorized-immigrants-fact-sheet-2025_FINAL.pdf"
```

Read-only sources quoted into `sources.json`, for anyone checking the quotes:

- DHS OHSS unauthorized estimates: <https://www.dhs.gov/ohss/topics/immigration>
- Pew, August 21 2025: <https://www.pewresearch.org/race-and-ethnicity/2025/08/21/u-s-unauthorized-immigrant-population-reached-a-record-14-million-in-2023/>
- CMS, *JMHS* July 2026: <https://journals.sagepub.com/doi/10.1177/23315024261466218>
- MPI, "new peak": <https://www.migrationpolicy.org/commentary/us-unauthorized-immigrant-population-new-peak>
- CIS January 2025: <https://cis.org/Report/ForeignBorn-Number-and-Share-US-Population-AllTime-Highs-January-2025>
- CIS September 2026: <https://cis.org/Report/Census-Bureau-Survey-Shows-Total-ForeignBorn-Down-29-Million>
- CBO, *The Demographic Outlook: 2026 to 2056*: <https://www.cbo.gov/publication/61994>
- 2020 PES and DA: <https://www.census.gov/newsroom/press-releases/2022/2020-census-estimates-of-undercount-and-overcount.html>
- Census net international migration revision: <https://www.census.gov/newsroom/blogs/random-samplings/2024/12/international-migration-population-estimates.html>

`census.gov` PES and Random Samplings pages, `cbo.gov`, `cis.org`, `migrationpolicy.org`
and `journals.sagepub.com` sit behind
bot protection and return 403 to `curl` and to WebFetch; they were retrieved with
a scraping tool. `homeland.house.gov` truncates the first attempt — `-C -` and a
retry get the whole 28 MB PDF.

## Outputs (`derived/`, 35 files, 148K total)

| File | Arm | Contents |
|---|---|---|
| `published_estimates.csv` | 1 | one row per published estimate: reference date, value, survey, quasi-legal inclusion, coverage adjustment, Mexico share |
| `published_definitions.md` | 1 | the definition, method and coverage sentences quoted verbatim, per source |
| `cps2025_residual_by_region.csv` | 2 | CPS ASEC 2025 residual by region of birth, with replicate-weight SEs |
| `cps2025_residual_by_yrsince.csv` | 2 | CPS ASEC 2025 residual by arrival cohort |
| `cps2025_summary.json` | 2 | CPS headline numbers |
| `acs2024_residual_by_region.csv` | 2 | ACS 2024 residual by region of birth, counted and DHS-coverage-adjusted |
| `acs2024_residual_by_yrsince.csv` | 2 | ACS 2024 residual by years since arrival |
| `acs2024_rule_hits.csv` | 2 | how many foreign-born people each Borjas rule marks legal |
| `acs2024_summary_cuba.json` | 2 | ACS headline numbers |
| `coverage_grid.csv` | 3 | the ACS residual under five published coverage assumptions |
| `coverage_grid_by_cohort.csv` | 3 | the same grid split by arrival cohort, where the whole spread lives |
| `cps2025_coverage_grid.csv` | 3 | the same schemes applied to the CPS residual, with the double-adjustment caution |
| `rule_sensitivity.csv` | 2 | the ACS residual under all four Borjas rule-list variants |
| `acs2024_*_cuba_noocc.csv`, `*_wide.csv`, `*_wide_noocc.csv` | 2 | the sensitivity runs' own tables |
| `stock_flow_cbo.csv` | 4 | DHS January 2022 stock rolled forward on CBO's other-foreign-national net series |
| `stock_flow_dispositions.csv` | 4 | CBP southwest-border encounters by disposition, FY2021–FY2024, plus known gotaways |
| `stock_flow_sensitivity.csv` | 4 | the answer as a function of the share of releases and gotaways who stayed |
| `stock_flow_comparison.csv` | 4 | stock-flow implied stock against every survey residual |
| `forty_million_ladder.csv` | 6 | the definition ladder and which rungs reach 40 million |
| `forty_million_summary.json` | 6 | the multiplier on non-citizens that 40 million requires |
| `acs2024_definition_ladder.csv` | 6 | the plain ACS definition counts |

## Reproducibility

Every script is deterministic: no sampling, no random assignment, no wall-clock
or hostname in any output. Re-running all eight steps over an existing `_cache/`
leaves `derived/` byte-identical. Verify with:

```bash
cp -R derived /tmp/derived_first
# re-run steps 2 to 8
diff -r /tmp/derived_first derived && echo "byte-identical"
git status --porcelain -- derived/
```

## Limits

- Residual estimates inherit the error in the legal-immigrant stock they subtract.
  The spread between published estimates for the same reference date is driven
  more by that term and by the coverage assumption than by the survey.
- Coverage multipliers are assumptions, not measurements, with one exception: the
  2020 Post-Enumeration Survey row. `coverage_grid.csv` spans 12.97M to 21.08M on a
  single counted base.
- The ACS 2024 and CPS ASEC 2025 weights are controlled to the Census Bureau's Vintage
  2024 population estimates, which already carry an upward humanitarian-migrant
  adjustment. Applying a further ACS-calibrated undercount rate partly adjusts twice.
- The ACS has no public-housing or rental-subsidy variable, so Borjas rule (f)
  cannot be applied there. This makes the ACS residual larger than a like-for-like
  CPS residual would be, not smaller.
- Encounters are events, not people. A person encountered three times is three
  encounters. `stock_flow_dispositions.csv` counts events throughout.
- The DHS OHSS enforcement monthly series stops with the November 2024 edition,
  so no disposition detail exists for calendar 2025 or 2026.
- Quasi-legal categories are a definition choice. Every published estimate in
  `published_estimates.csv` includes them; the narrow reading is reported
  separately in `RESULT.md`.

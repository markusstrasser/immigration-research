# Reader inputs, joins and normalization

Updated 2026-09-19. This guide connects source acquisition to the existing analysis recipes. It covers the core fiscal warehouse and the named September survey/ledger lanes below; it is not a claim that every research memo is included in one build. No AWS mirror URL is registered here yet.

## Get the exact inputs

Use these routes in order, for each input file:

1. **Official download:** use the recorded official URL or API and verify the release, format and checksum. A working URL is an access route, not redistribution permission. A site's usage terms still apply to automated downloading.
2. **AWS mirror:** use a versioned copy only where redistribution is cleared, with its original license, attribution and checksum. A failed official URL does not itself authorize mirroring. Keep the original source URL alongside the mirror URL.
3. **Reader acquisition:** where login, terms acceptance or an application is required, the reader or their browser agent obtains the file from the provider, then resumes the same local recipe. A missing or unresolved license also stays on this route until clarified.

For each release, record the source identifier/version, source and reference years, URL, retrieval date, expected archive members, SHA-256, local destination, applicable terms, and consuming recipe. Include the Git commit and dependency lockfile. Existing manifests linked below hold much of this information; they are the source records rather than a new copy of every hash in this guide.

**Exact reproduction versus a refresh:** if a provider replaces the file, a checksum mismatch means the input changed. Preserve the old file and report the mismatch. Do not relabel the newest file as the frozen vintage. For dynamically generated ZIPs, compare the recorded member hashes as well: ZIP timestamps can change without the underlying CSV changing. Where no cleared copy of the historical bytes is available, report that exact reproduction is unavailable; a new-vintage run is a separate result.

### Source routes and existing records

Paths in this table are relative to this directory unless specified otherwise. “Mirror candidate” means evidence supports preparing a mirror; it does not mean one is already hosted. Licenses were inspected on 2026-09-19 in the associated task; the LNS declarations below are from primary metadata saved on September 17.

| Source | Preferred acquisition / fallback | Exact-file record and recipe |
|---|---|---|
| Census ACS PUMS, CPS ASEC, SIPP | Official Census bulk files; public-use originals are mirror candidates. Prefer bulk archives when a query API would add unnecessary key/setup work. | [Core manifest](DOWNLOAD_MANIFEST.tsv), [2024 fiscal input URLs/hashes](acquire/fiscal_2024_sources.tsv), [dataset register](../../research/immigration-dataset-register.md). The fiscal catalog's absolute `local_path` values describe the acquisition machine; relocate under the reader's configured data root. |
| AHRQ MEPS HC-256 (2024) / HC-251 (2023) | Official AHRQ public-use download; obtain the fixed-width data ZIP and matching SAS layout, codebook and documentation. | [HC-256 URLs and hashes](acquire/fiscal_2024_sources.tsv), [older MVP acquisition](acquire/setup.sh). Do not mix the 2023 and 2024 layouts/data. |
| CPS ASEC 2022–2026 comparison | Official annual archives. The comparison acquisition script only fetches its missing 2022/23 inputs; it reuses the other years. | [LATAM recipe](latam_comparison_2026_09_17/README.md); `_cache/acquisition.json` and `derived/audit.json` are generated/local evidence, not guaranteed to exist in a fresh clone. |
| Census/IRS/BEA/BLS/HUD/NCES/USDA/DOJ public tables | Official links in the acquisition scripts; ordinary browser download where the official site requires it. Assess third-party attachments separately. | [Core setup](acquire/setup.sh), [crime source setup and generated manual instructions](acquire/setup-crime-frontier.sh), [download manifest](DOWNLOAD_MANIFEST.tsv). |
| NLSY97 public-use extracts | BLS/NLS Investigator, with the saved variable basket; public-use files are mirror candidates under [BLS policy](https://www.bls.gov/opub/copyright-information.htm). | [Survey intake recipe](new_datasets_2026_09_17/README.md), [original-name map](new_datasets_2026_09_17/library/README.md), [98-field basket](new_datasets_2026_09_17/nlsy/required_analyzed_fields.NLSY97), [additional parent-linkage basket](new_datasets_2026_09_17/nlsy/parent_linkage_fields.NLSY97). Core and extra parent fields are separate inputs. |
| Pew NSL 2011/12/14/15/16/18, 2013 religion, 2015–16 nonidentifiers | Reader downloads the exact survey ZIP from [Pew's dataset library](https://www.pewresearch.org/tools-and-resources/). Full-file mirror needs permission under [survey terms §13](https://www.pewresearch.org/about/terms-and-conditions/). | [Eight-survey original-name map](new_datasets_2026_09_17/library/README.md), [manifest](new_datasets_2026_09_17/manifest.json), [Pew recipes](new_datasets_2026_09_17/README.md). |
| IPUMS USA historical sample extract | Reader requests CSV at [IPUMS USA](https://usa.ipums.org/usa/); general mirror needs permission, subject to the specific journal-subset exception in [terms](https://usa.ipums.org/usa/terms.shtml). | Exact sample/variable specification in [loader](build/load_ipums_borjas_panel.py); instructions below. |
| SPI 2016, ICPSR 37692 v5 | Reader obtains DS1/DS2 public-use files from [study 37692](https://www.icpsr.umich.edu/web/NACJD/studies/37692). Packaged terms require permission for general redistribution. | `external/crime_frontier/spi/ICPSR_37692-V5.zip` under the data root; [loader](build/load_spi_citizenship.py). Do not substitute restricted DS3. |
| ICPSR LNS 20862 v6 / NYC second generation 30302 v1 | Reader obtains access from [20862](https://www.icpsr.umich.edu/web/ICPSR/studies/20862) / [30302](https://www.icpsr.umich.edu/web/ICPSR/studies/30302); [redistribution policy](https://www.icpsr.umich.edu/sites/icpsr/about/policies/redistribution) also covers documentation. | [Access status](new_datasets_2026_09_17/access-status.md). Held packages are documentation only. Existing codebook analyses reproduce marginal tables, not respondent-level analyses. |
| Branton/Wallace/Perez LNS author replications | Official Dataverse file URLs first; deposited data/code are mirror candidates under their CC0 declarations. Separately copyrighted article PDFs are excluded from that conclusion. | [Pinned versions, file URLs, licenses and hashes](new_datasets_2026_09_17/lns_replications/source_manifest.json); [staging/analysis recipe](new_datasets_2026_09_17/README.md). These are not substitutes for all variables in the original LNS release. |
| Saiz–Wachter housing replication 114757 v1 | [Official archive](https://www.openicpsr.org/openicpsr/project/114757/version/V1/view), or a mirror retaining CC-BY4.0 data/BSD code licenses. | [Archive hash/license record](hedonic_replay_2026_09_19/ACQUIRED.md), [stage and replay recipe](hedonic_replay_2026_09_19/README.md). |
| Light–He–Robey Texas replication 124923 v1 | Reader downloads from [official archive](https://www.openicpsr.org/openicpsr/project/124923/version/V1/view). Exact redistribution license remains unresolved; login alone proves neither permission nor prohibition. | `external/crime_frontier/light_texas/124923-V1.zip`; [loader](build/load_light_tx_crime.py). |
| Vera processed ICE series | Reader/source download at the pinned revision; no general mirror under [Vera's license](https://github.com/vera-institute/ice-fytd-stats/blob/main/License.md). Separately assess original ICE workbooks. | [Pinned acquisition code](acquire/refresh-frontier-20260905.py) and its generated `.scratch/frontier-20260905/datasets/manifest.json` at repo root. |
| GSS, Zillow ZORI/ZHVI, Opportunity Insights | Official sources/readers fetch directly. Complete raw-file mirror permission remains unresolved; do not infer it from availability. | [GSS terms](https://gss.norc.org/terms-and-conditions.html), [Zillow data](https://www.zillow.com/research/data/), [OI data](https://opportunityinsights.org/data/); [dataset register](../../research/immigration-dataset-register.md) and [OI acquisition recipe](latam_comparison_2026_09_17/README.md). |
| FRED Case–Shiller | Reader obtains the series under its terms; a full mirror requires clearance. Federal CPI/unemployment series have different rights from S&P's series. | [CSUSHPINSA source/rights](https://fred.stlouisfed.org/series/CSUSHPINSA); [setup](acquire/setup.sh). |
| LAPOP | Reader obtains data and accepts [provider terms](https://www.vanderbilt.edu/center-for-global-democracy/data/); no general data-file mirror. | Only a codebook was acquired in the named LATAM lane; there is no respondent dataset to rebuild there. |

### Reader or browser-agent handoff

Give the reader/agent this task together with the selected row's source record:

> Open the official study page. Obtain the specified release using the reader's account and authorized access. Select the data file format required by the recipe and its codebook; retain the license. Save the untouched download to the stated input directory. Record the final filename, URL, study/version, file size and SHA-256; inspect archive members and confirm that respondent data are present if required. Compare to the frozen input record. If the account cannot access that release, report the exact access message and missing file instead of repeatedly downloading documentation. Do not substitute a newer release or different study. Once verified, run the named local analysis and validation commands.

For Pew, use the original download filenames in the named library map. `stage.py --source /path/to/downloads` stages the supplied survey batch; it is not an independent web downloader. For NLSY97, import the saved basket into [Investigator](https://www.nlsinfo.org/investigator/), export CSV with codebook and setup files, and check the source-reference coverage. A `.NLSY97` basket alone contains no respondent data.

For the historical IPUMS recipe, request 1980/1990/2000 5% Census samples plus 2010 and 2023 ACS. Required fields are listed in the [loader header](build/load_ipums_borjas_panel.py), including `YEAR SAMPLE SERIAL PERWT GQ STATEFIP AGE BPL BPLD CITIZEN YRIMMIG EDUC EDUCD RACE RACED EMPSTAT EMPSTATD WKSWORK1 INCTOT`. Stage the matching CSV/GZIP and documentation under `$PNY_DATA_ROOT/external/ipums/usa_extract/`. The current loader chooses a filename by sorting rather than a pinned hash: use a dedicated input directory containing only the verified intended extract. Its person records go to the local `immigration_microdata.duckdb`, not the aggregate release.

### A concrete direct-download check

This reproduces one frozen input in [the fiscal catalog](acquire/fiscal_2024_sources.tsv); it does not run the whole analysis. From the repository root after `init`, choose the same data root as in `config.local.env`:

```bash
export IMMIGRATION_DATA_ROOT="$HOME/research-data/immigration-fiscal/data"
mkdir -p "$IMMIGRATION_DATA_ROOT/external/stage3/census/cps_asec_2025"
cd "$IMMIGRATION_DATA_ROOT/external/stage3/census/cps_asec_2025"
# Use an empty staging directory or a new filename; preserve existing raw inputs.
curl --fail --location --retry 3 \
  'https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip' \
  --output asecpub25csv.zip.part
printf '%s\n' '318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b  asecpub25csv.zip.part' \
  | shasum -a 256 -c -
unzip -tq asecpub25csv.zip.part
# Only after both checks pass, move it to the recipe's asecpub25csv.zip input.
```

For a cleared AWS fallback, replace only the URL with the recorded mirror URL: the expected original-file hash stays the same. Never put a reader's session cookies, signed access URLs or API credentials in the published manifest.

## Join and normalize

There is no person identifier shared across ACS, CPS, SIPP, MEPS, Pew and NLSY97. Three operations must stay distinct:

- **Record linkage:** attach records for the same surveyed person or household using documented IDs within the appropriate study/release.
- **Context join:** attach a state/county/PUMA/year attribute to records. This does not make the area attribute an observed individual outcome.
- **Statistical matching:** attach an estimated mean from a different survey's age/education/insurance group. This is a modeled projection, not a same-person join.

### Core contracts

| Operation | Keys, normalization and limits | Implementation |
|---|---|---|
| ACS person + household | Append every national person-file part, and every household-file part, before joining. Household attachment is many people to one `SERIALNO` within a release. Retain release/year when combining years. Person estimates use `PWGTP`; household estimates use `WGTP`. Do not count the full household amount once for every person. | [Core warehouse builder](build/build_immigration_warehouse.py); [school exposure](build/measure_acs_school_exposure_2024.py). |
| Geographic context | Keep FIPS/PUMA/ZIP identifiers as strings with leading zeros. A PUMA needs its state and boundary vintage. Crosswalk allocations are weighted mappings, not unique-person links. Report uncovered geography and the chosen mapping convention. | [Stage2 builder](build/build_stage2_incidence_context.py), [origin/geography register](../../research/immigration-dataset-register.md). |
| Separate surveys | Preserve each source's original codes and an explicit recode. Unknown/refused/not-in-universe codes are not zeros. Detailed origin, citizenship, nativity, parental birthplace and self-identified ethnicity are different variables; no harmonized label manufactures missing ancestry or legal status. | Source-specific scripts and dictionaries in the recipes below. |
| Dollar/year comparison | Record interview year, income/reference year and price year separately. CPS ASEC 2025 and SIPP 2025 describe 2024 income; a file named 2024 need not contain 2024 income. Apply source-prescribed adjustment factors and the recipe's deflator once; do not mix nominal and real dollars. | [Fiscal input catalog](acquire/fiscal_2024_sources.tsv), source dictionaries and individual builders. |
| Weighted estimates | Use the outcome's eligible denominator, retain missingness counts, and use the matching person/household weights. Follow the survey's replicate-weight method; do not treat annual cross-sections or all rows as independent observations. | Lane validators linked below. |
| Warehouse assembly | `context`, `lifetime`, and `fiscal` preserve separate source warehouses; materialized views are frozen snapshots. This step copies tables and evaluates views, not a new respondent linkage. Prefer schema-qualified table names where names collide. | [Unified builder](build/build_unified_warehouse.py). |

### Recipes and result checks

Start with the lane that produced the figure being reproduced. The core `build all` command does not execute every September lane. The source recipe, its input records and its validator together define reproduction; the detailed lane rules below are not a new harmonization algorithm.

Commands run from the repository root; replace `/path/to/` placeholders with verified inputs. `uv` resolves script-declared dependencies; explicit `--with` options supply additional dependencies.

#### CPS fiscal accounts: ASEC 2025, calendar year 2024

```bash
uv run python3 infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py \
  --cps-zip /path/to/asecpub25csv.zip --output /path/to/results/cps-2024 \
  --meps-zip /path/to/h256dat.zip --meps-sas /path/to/h256su.txt
```

Omitting the optional MEPS arguments reproduces tax/benefit-only results, not health-inclusive accounts. Outputs include `accounts.csv`, `contrasts.csv`, `replicate_estimates.json` and `manifest.json`.

- Join `pppub25.csv` to `asec_csv_repwgt_2025.csv` one-to-one on `(PH_SEQ, PPPOS)`, renaming replicate `h_seq` to `PH_SEQ`. Require complete matches. `MARSUPWT / 100` must match `pwwgt0` within 0.01; do not rescale replicate weights again.
- `SPM_ID` identifies a resource unit, not necessarily a household. Require one `SPM_HEAD` and membership equal to `SPM_NUMPER`. Take repeated unit benefit amounts once, then allocate across members while conserving dollars.
- The [expanded extension](gen_ledger_extension_2026_09_16/extend_ledger.py) attaches households with `PH_SEQ=H_SEQ`, many-to-one, rejecting unmatched people; state parameters use `fips`.
- Recompute estimates with the full weight and 160 replicates; SDR variance uses `4/160`. Unknown parent birthplace does not establish native parentage. Third-plus Mexican self-identification does not measure all third-plus Mexican ancestry.

For expanded results, follow the [all-age recipe and guards](all_age_ledger_2026_09_17/README.md) and [current yearly/lifetime repair](../../research/immigration-yearly-lifetime-cost-repair-2026-09-19.md). **Portability gap:** this lane also needs held state parameters, an extended ledger, MEPS at its expected path and the independent aggregate audit. A fresh clone plus CPS ZIP is insufficient; those prerequisites must be rebuilt or supplied as cleared, hash-pinned intermediates.

#### MEPS health costs: transport between surveys

The [2024 transport](build/meps_health_transport_2024.py) uses HC-256 `AGE24X`, `BORNUSA`, `INSURC24`, `PERWT24F`, `VARSTR` and `VARPSU`. Donor cells use age bands bounded at 18/35/50/65 and birthplace, optionally insurance. Calculate positive-weight cost means from valid records, attach the matching mean to CPS recipients, and reject unsupported cells.

This is statistical matching, not respondent linkage. The transport's CPS birthplace rule (`PENATVTY==57`) differs from broader nativity definitions. MEPS age at December 31, 2024 differs from CPS interview age in 2025; do not subtract one from every CPS age. Survey variance propagation does not remove the transport assumptions or prove independence between surveys.

#### SIPP annual benefits: 2025 release, calendar year 2024

```bash
uv run --with numpy python3 infra/immigration-fiscal/build/analyze_sipp_2025.py \
  --schema /path/to/pu2025_schema.json --zip /path/to/pu2025_csv.zip \
  --replicate-schema /path/to/rw2025_schema.json --replicate-zip /path/to/rw2025_csv.zip \
  --out-dir /path/to/results/sipp-2024
uv run --with duckdb --with pandas --with numpy python3 -m unittest discover \
  -s infra/immigration-fiscal/tests -p 'test_sipp*.py'
```

- Person-month keys are `(SSUID, PNUM, MONTHCODE)` within this release. Select positive-weight, in-frame December people aged 25–64; preserve observed annual sums without annualizing short histories.
- Select December replicate rows, join one-to-one on `(SSUID, PNUM)`, and reject duplicate/missing/invalid weights. `REPWGT0` must equal December `WPFINWGT`. Combining panels/waves requires extending these keys; this code handles one release.
- Use December person weight once, plus 240 Fay-BRR replicates with Fay factor 0.5. Summed monthly weights are not annual person weights.
- Allocate SNAP/TANF owner amounts equally among covered people by `(program, SSUID, owner-PNUM, month)` **before** demographic/weight filters. The owner need not be covered; SSI remains individual. Excluded children's shares do not move to adults.
- Native is `EBORNUS=1 OR ENATCIT in (4,5)`; otherwise `EBORNUS=2` is foreign-born, with missing preserved. Keep negative/zero earnings. Income and benefit fields can overlap; do not sum them as disjoint components.

Outputs include `benefit_profiles_2024.csv`, `benefit_contrasts_2024.csv`, person allocations, `replicate_estimates_2024.json` and a manifest. The [result memo](../../research/immigration-sipp-2024-benefits-2026-09-05.md) records source hashes. Its older verifier in ignored `.scratch/` is not a tracked reader entrypoint; the tests above check the implementation and do not replace input/output checks.

#### Older SIPP–MEPS MVP: separate monthly calculation

```bash
uv run python3 infra/immigration-fiscal/build/build_public_mvp_sipp_module_2024.py
uv run python3 infra/immigration-fiscal/build/build_public_mvp_meps_module.py
uv run python3 infra/immigration-fiscal/build/build_public_mvp_sipp_meps_bridge_2024.py
```

Inputs are SIPP `pu2024_csv.zip`/schema and MEPS `h251dat.zip`/`h251su.txt` under the configured data root. This SIPP release covers 2023; pooled monthly `WPFINWGT` counts person-months. The [bridge](build/build_public_mvp_sipp_meps_bridge_2024.py) matches SIPP `(age, nativity, education)` to MEPS `(broader age, birthplace)`, then splits by MEPS insurance shares. Branch weight equals SIPP person-month weight times the donor insurance share. Education remains in output labels but does not condition health means. Unknown/unmatched cells fail; mapping conventions are recorded. Inspect the `stage3_proto/sipp_meps_bridge_cells_2024.csv`, expected-health-cost cells and metadata.

#### NLSY97: respondent and family linkage

Use the [intake and NLSY recipe](new_datasets_2026_09_17/README.md), including `nlsy/verify.py` and `nlsy/verify_family.py`. Pass the historical full archive as `--baseline-archive` to `nlsy/extract.py` and `--archive` to `nlsy/extract_family.py`; pass the legacy validation directory as `--profile-source-dir` to `nlsy/analyze.py`.

**Portability gap:** the family extractor pins the historical archive hash. Baseline validation also needs `hu2025_nlsy97_mgcfa_input.csv` and `profile_outcomes/source_extract.parquet`. The 98-field basket and fresh export do not replace all these dependencies. Investigate a different archive hash; document a changed-input refresh separately.

Join baseline and parent supplements one-to-one on `R0000100`, checking exact equality for overlapping fields; historical extraction expects 8,984 unique respondents. A parent interview respondent/spouse is not automatically biological parent: use relationship/roster evidence and preserve conflicts and unresolved links. Use positive `U6365400/100` and outcome-valid denominators. Generation here is generic US/foreign parentage, not Mexican ancestry; the current family analysis supplies no survey-design standard errors. Inspect parent-nativity sources, linkage issues and generation/outcome outputs.

#### Pew: harmonize cross-sections

After staging the original survey batch using the intake recipe:

```bash
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/analyze.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/harmonize.py \
  --lane-dir infra/immigration-fiscal/new_datasets_2026_09_17 \
  --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/verify_harmonized.py \
  --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
```

Retain SPSS labels/user-missing codes. The [harmonizer](new_datasets_2026_09_17/pew/harmonize.py) selects wave-specific variables and `weight`/`weights`, validates meanings/sample sizes, and reports outcome-specific missingness/denominators. Preserve unknown parents and the two stated Puerto Rico conventions.

Append comparable cross-sections; never person-join waves. Descriptive pooled WLS normalizes each survey to equal total weight before outcome conditioning. The non-Hispanic ancestry supplement represents a different population and stays outside the seven-wave series; its complementary population calculation uses the recipe's explicit calibration. Inspect `generation_outcomes.csv`, `classification_missingness.csv`, `denominator_audit.csv`, model outputs and source/field hashes. These comparisons establish neither causal assimilation nor survey-design standard errors.

## Verify what was actually reproduced

The existing `reproduce.sh verify` checks presence and minimum sizes from `DOWNLOAD_MANIFEST.tsv`; it does not verify source SHA-256 hashes. `verify derived` checks `build`/`compose` entries under the configured derived root and fails if no entries are selected. It does not cover every standalone lane or validate calculations. Also run lane-specific validators and hash checks. Optional acquisitions/builders may skip inputs without making the overall command fail; a successful exit alone does not establish complete coverage.

For a reader release, preserve an input/output receipt for each requested result: source versions/hashes; code commit; environment; commands; expected table/column keys; duplicate and unmatched-key counts; row counts and weighted totals; normalization conventions; validator results; and any missing modules. Source hash equality proves byte identity, while an analytical validator checks the resulting calculations. Neither proves the scientific interpretation.

**Current publication limit:** `package_data_release.py` copies the entire unified DuckDB and exports every cataloged table. It has no source-license filter; its generated README now states that limit. Inspect the actual tables and their upstream rights before preparing an AWS release; an aggregate database can still contain a substantially complete third-party series. This guide adds instructions, not an automated acquisition router or a publication checker.

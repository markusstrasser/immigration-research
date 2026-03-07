This overview focuses on the codebase's infrastructure for data processing, analysis pipelines, and statistical computation, rather than the specific domain analysis.

### INDEX
- **DATA_EXTRACTION_PREPARATION**: Scripts for parsing and extracting data from raw, complex formats.
- **DATA_INGESTION_CACHING**: Scripts for downloading data via HTTP and managing local caches.
- **ANALYSIS_PIPELINES_STATISTICAL_PATTERNS**: Core scripts implementing load-process-model-save workflows and shared statistical utilities.
- **SYNTHESIS_META_ANALYSIS**: Scripts that consume results from other pipelines or use hardcoded data for meta-analysis.

### DATA_EXTRACTION_PREPARATION
This section covers scripts that transform raw data files (e.g., fixed-width `.dat`, large `.csv` in `.zip`, SAS syntax) into analysis-ready tabular formats like `.tsv` or `.parquet`.

`sources/iq-sex-diff/extract_nlsy_asvab_vars.py`
- Parses SAS syntax files from NLSY ZIP archives to extract variable metadata.
- **Key Functions**: `extract_rows`, `parse_sas`
- **Dependencies**: `zipfile`, `re`, `csv`

`sources/iq-sex-diff/map_nlscya_early_school.py`
- Parses a SAS file to generate a variable map for targeted data extraction.
- **Key Functions**: `parse_sas`, `build_rows`, `classify_label`
- **Dependencies**: `zipfile`, `re`, `csv`

`sources/iq-sex-diff/extract_eclsk_early_school.py`
- Extracts data from a multi-line fixed-width `.dat` file using a `.dct` layout file.
- **Key Functions**: `parse_layout`, `main`
- **Dependencies**: `re`, `csv`, `gzip`

`sources/iq-sex-diff/extract_eclsk2011_early_school.py`
- Extracts data from a single-line fixed-width `.dat` file based on a `.dct` layout file.
- **Key Functions**: `parse_layout`, `main`
- **Dependencies**: `zipfile`, `re`, `csv`, `gzip`

`sources/iq-sex-diff/build_nlscya_early_school_extract.py`
- Creates a compact TSV extract from a large CSV within a ZIP archive based on a variable map.
- **Key Functions**: `load_variable_map`, `main`
- **Dependencies**: `zipfile`, `csv`, `gzip`, `io`

`sources/iq-sex-diff/build_nlsy79_sibling_pairs.py`
- Implements logic to identify and extract sibling pairs from the main NLSY79 CSV file.
- **Key Functions**: `load_rows`, `candidate_edges`, `build_pairs`
- **Dependencies**: `zipfile`, `csv`, `collections.defaultdict`

`sources/iq-sex-diff/build_public_archive_catalog.py`
- Catalogs the contents of multiple ZIP archives in the data directory into TSV manifests.
- **Key Functions**: `iter_archives`, `build_catalog`
- **Dependencies**: `zipfile`, `csv`

### DATA_INGESTION_CACHING
These scripts handle fetching data from external sources and managing local caches for performance.

`sources/iq-sex-diff/download_nces_onlinecodebook_assets.py`
- Fetches JSON file manifests from the NCES DataLab API and downloads associated data files.
- **Key Functions**: `fetch_json`, `stream_download`, `resolve_manifest`
- **Dependencies**: `urllib.request`, `json`

`sources/iq-sex-diff/psid_access_probe.py`
- Probes web server availability for PSID data using a browser-impersonating HTTP client.
- **Key Functions**: `main`
- **Dependencies**: `curl_cffi.requests`

`sources/iq-sex-diff/cache_nlsy_extracts.py`
- Caching pipeline that processes raw NLSY data and saves it as Parquet for faster analysis runs.
- **Key Functions**: `main`
- **Dependencies**: `pandas` (for `to_parquet`), `build_nlsy79_sibling_pairs`, `nlsy79_stats_pipeline`

### ANALYSIS_PIPELINES_STATISTICAL_PATTERNS
This section details the common analysis pipeline pattern: load data, perform weighted statistical calculations, fit regression models, and save results. Many scripts define their own local statistical utilities (`weighted_mean`, `weighted_d`).

`sources/iq-sex-diff/timss_common.py`
- Provides shared statistical utilities for TIMSS data, handling plausible values and Jackknife variance estimation.
- **Key Functions**: `plausible_value_summary`, `jackknife_effect`, `weighted_effect`
- **Dependencies**: `pandas`, `numpy`, `pyreadstat`

`sources/iq-sex-diff/nlsy79_stats_pipeline.py`
- A robust pipeline for NLSY79 data using `pandas` and `statsmodels` for analysis.
- **Key Functions**: `rows_to_frame`, `standardize_scores`, `fit_weighted_gap`, `run_pair_models`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`, `build_nlsy79_sibling_pairs`

`sources/iq-sex-diff/nlsy97_stats_pipeline.py`
- A reusable pipeline for NLSY97 data, loading from a ZIP, standardizing scores, and fitting weighted models.
- **Key Functions**: `load_frame`, `standardize_scores`, `fit_weighted_gap`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`, `zipfile`

`sources/iq-sex-diff/nlsy79_first_pass.py`
- An early version of the NLSY79 pipeline featuring a manual OLS matrix implementation.
- **Key Functions**: `raw_subtest_surface`, `standardized_person_scores`, `fit_ols`, `inverse_matrix`
- **Dependencies**: `csv`, `math`, `build_nlsy79_sibling_pairs`

`sources/iq-sex-diff/nlsy97_stage_a_pass.py`
- An incremental analysis pipeline that adds process and school exposure variables to the NLSY97 models.
- **Key Functions**: `same_sample_model`, `prepare_design`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`, `nlsy97_stats_pipeline`

`sources/iq-sex-diff/hsls_wedge_first_pass.py`
- Pipeline for HSLS data, loading from a `.sav` file and executing a standard analysis workflow.
- **Key Functions**: `load_hsls`, `build_extract`, `build_model_table`, `fit_wls`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`, `pyreadstat`, `zipfile`

`sources/iq-sex-diff/piaac_p1_stratified.py`
- A pipeline for PIAAC data designed to handle its complex survey structure (plausible values, replicate weights).
- **Key Functions**: `load_file`, `estimate_cell`, `weighted_effect`, `replicate_factor`
- **Dependencies**: `pandas`, `numpy`

`sources/iq-sex-diff/early_school_age_matched_alignment.py`
- A cross-dataset alignment pipeline that loads multiple datasets, performs age-based matching, and standardizes results.
- **Key Functions**: `load_pairs`, `add_age_bins`, `enrich_group`, `run_models`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`

`sources/iq-sex-diff/pisa2018_dif_leaveout_pass.py`
- Advanced Differential Item Functioning (DIF) pipeline for PISA data, implementing leave-one-out matching scores.
- **Key Functions**: `fit_item_model`, `weighted_demean`
- **Dependencies**: `pandas`, `numpy`, `statsmodels`

*Other analysis pipelines not listed for brevity follow similar patterns:*
- **NLSY**: `nlsy79_schooling_pass.py`, `nlsy97_piat_cat_pass.py`, `nlsy97_transcript_deep_pass.py`, `nlsy97_course_causal_pass.py`, `nlsy97_behavior_evaluation_pass.py`
- **Early School**: `nlscya_early_school_first_pass.py`, `eclsk_early_school_first_pass.py`, `eclsk2011_early_school_first_pass.py`, `early_school_score_alignment.py`
- **Late School Wedge**: `els_wedge_first_pass.py`, `nels_wedge_first_pass.py`, `hsls_wedge_refinement.py`
- **PIAAC/PISA/TIMSS**: `piaac_p1_age_stratified.py`, `piaac_p1_occupation_proxy.py`, `pisa2018_item_split.py`, `pisa2018_dif_proxy_pass.py`, `timss_advanced_first_pass.py`, `timss_grade_decomposition.py`
- **Other**: `icar_decomposition.py`

### SYNTHESIS_META_ANALYSIS
These scripts operate on the *results* of other analysis pipelines or on hardcoded data to synthesize findings.

`sources/iq-sex-diff/school_wedge_synthesis.py`
- Synthesizes findings across multiple late-school cohort datasets by loading and summarizing their TSV results.
- **Key Functions**: `pick_hsls`, `pick_els`, `pick_nels`, `pick_nlsy97`
- **Dependencies**: `pandas`

`sources/iq-sex-diff/school_wedge_mechanism_triage.py`
- Loads TSV results from multiple mechanism-analysis pipelines and creates summary tables.
- **Key Functions**: `build_shift_rows`, `build_family_summary`
- **Dependencies**: `pandas`

`sources/iq-sex-diff/pisa2018_framework_proxy_split.py`
- Summarizes PISA item-level results from other pipeline outputs into framework-level aggregates.
- **Key Functions**: `summarize`
- **Dependencies**: `pandas`, `numpy`

`sources/iq-sex-diff/timss_cognitive_split.py`
- Summarizes and contrasts TIMSS results from different pipeline runs.
- **Key Functions**: `build_domain_contrasts`, `build_advanced_contrasts`
- **Dependencies**: `pandas`

`sources/iq-sex-diff/meta_analysis.py`
- Performs a random-effects meta-analysis on hardcoded effect sizes from scientific literature.
- **Key Functions**: `meta_analyze_re`, `variance_d`
- **Dependencies**: `math`

`sources/iq-sex-diff/german_wais4_effects.py`
- Calculates Cohen's d effect sizes from hardcoded summary statistics from a research paper.
- **Key Functions**: `cohens_d`
- **Dependencies**: `math`

`sources/iq-sex-diff/timing_channel_analysis.py`
- A descriptive script that analyzes hardcoded effect sizes to compare timed vs. untimed tests.
- **Key Functions**: `main`
- **Dependencies**: `statistics.mean`

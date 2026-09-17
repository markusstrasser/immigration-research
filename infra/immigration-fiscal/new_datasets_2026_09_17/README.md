# September 17 survey intake and conclusion audit

**Start with the [named dataset library](library/README.md).** It groups NLSY97, Pew and ICPSR files under descriptive names, maps original filenames and equivalent downloads, and marks documentation-only packages. Rebuild it with `uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/organize.py`. Copies and catalog are ignored; the generator and source records are tracked. The library stays inside this project because the repository's `sources/` path is a symlink to a separate data directory.

**Current access:** the complete NLS core export is verified; ICPSR20862 respondent data are blocked by the account's non-member status according to the operator's browser report. Stop repeated documentation downloads. [Access evidence and remaining options](access-status.md). Historical intake notes below retain the earlier state.

Thirteen supplied files are recorded in `manifest.json` and `ACQUIRED.md`. Originals are preserved; duplicate NLS ZIPs share one canonical staged copy. `raw/` and `derived/` stay local and are ignored. Research synthesis and source definitions: [audit](../../../research/immigration-new-datasets-and-conclusions-2026-09-17.md), [dataset cards](../../../research/immigration-dataset-register.md).

Run commands from the repository root. Python dependencies already declared in this project cover these acquisition/analysis scripts; PDF text extraction also uses `pdftotext`. Set `UV_CACHE_DIR` to a writable temporary directory if the normal cache is sandboxed.

```bash
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/stage.py --source /Users/alien/Downloads
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/analyze.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/icpsr/inspect_archives.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/icpsr/analyze_codebooks.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/audit_other.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/extract.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/analyze.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/verify.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/verify.py
```

The NLS extractor streams an 8GB uncompressed CSV from the already-held sibling archive, selecting only the frozen 98 requested references. Override `--baseline-archive` if needed. The analysis also validates links against the existing ability table and outcome cache; use `--profile-source-dir` to relocate those inputs. The minimal request at `nlsy/required_analyzed_fields.NLSY97` can be imported into Investigator for a fresh CSV/codebook export, but current-public country specificity remains limited. An actual fresh export is needed to check drift in cumulative histories missing from the supplied ZIP.

**Later September 17 follow-up:** the three supplied `nlsy97_gen_crime_2` ZIPs are identical, now staged separately from the original 13-file intake. Their cumulative histories and four other examined non-ID fields match the audited baseline across all 8,984 respondents, closing the history-drift check for this export. The two exports combined still omit 47 of the frozen 98 fields. Reproduce with `uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/check_followup_export.py`; source hashes, archive members and coverage are in `nlsy/followup_export_check.json`. The original manifest remains the record of the first intake. Browser follow-up: import the exact 98-field basket for complete export coverage, and obtain actual public ICPSR20862 DS0003 data (DS0001 acceptable); the earlier ICPSR downloads contain only documentation.

**Final September 17 request check:** `default.zip` completes the frozen NLS request: 8,984 unique matching IDs, all 98 requested references plus `R1235800`, complete requested codebook coverage, and zero value differences in the 97 requested non-ID fields against the audited baseline. No more NLS exports are needed for this request. The second ICPSR ZIP, `ICPSR_20862-V6 (1).zip`, still contains only documentation: seven files identical to the prior package. Reproduce with `uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/check_completion.py`; hashes, member inventories and checks are in `completion_check.json`. The remaining browser task is actual DS0003 respondent data (Stata, SPSS or TSV; DS0001 acceptable). If unavailable, capture the exact access message and selected options instead of downloading documentation again.

Outputs:

- `derived/pew_harmonized/`: seven-survey language, perceived-American-similarity and party comparisons, both Puerto Rico conventions, explicit outcome denominators and descriptive composition sensitivities. [Findings](../../../research/immigration-pew-generation-denominators-2026-09-17.md).
- `derived/nlsy_family/`: 104 additional selected fields from the already-held full archive, corrected biological-parent links, source/conflict rows, generation assignments and descriptive outcome tables. [Findings and exact source rules](../../../research/immigration-nlsy97-parent-linkage-2026-09-17.md).
- `raw/lns_replications/` and `derived/lns_replications/`: three freely posted author derivatives, their documentation, exact source manifest and limited weighted policy analysis. These are additional data sources, not the full ICPSR release. [Source limits](../../../research/immigration-lns-public-replications-2026-09-17.md).
- `derived/pew/`: survey metadata/weights, direct-item generation diagnostics, weighted tables and missingness. Independent cross-sections are appended only for the documented 2015/2015–16 complementary population calculation. Both rounded 89/11 and published-count 37.8m/4.9m calibrations are retained.
- `derived/icpsr/`: extracted documentation, parsed marginal tables and arithmetic bounds. No synthetic respondent data are created. Missing actual LNS data are DS0001 or DS0003; NYC's catalog requires a restricted-use agreement.
- `derived/nlsy/`: selected columns, codebooks, tagset coverage, baseline archive hash, same-person join diagnostics, six descriptive tables. All participant-level derivatives remain ignored.
- `derived/other_audit/`: independent CILS contrasts/missing-record completion bounds and IIMMLA sex-by-parental-education contrasts. Illustrative independent-binomial intervals are not survey-design population intervals.

Completed substantive analysis: [collection synthesis](../../../research/immigration-organized-surveys-analysis-2026-09-17.md). Reproduce after the initial extraction above:

```bash
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/harmonize.py --lane-dir infra/immigration-fiscal/new_datasets_2026_09_17 --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/verify_harmonized.py --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/extract_family.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/analyze_family.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/verify_family.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/lns_replications/analyze_replications.py --input-dir infra/immigration-fiscal/new_datasets_2026_09_17/raw/lns_replications --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/lns_replications
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/organize.py
```

The LNS [source manifest](lns_replications/source_manifest.json) records all15 acquisition artifacts with public URLs, original filenames, descriptive destinations, versions, license metadata and SHA-256. To rebuild from verified downloads, use `lns_replications/stage_lns_replications.py --source-dir DOWNLOAD_ROOT --destination infra/immigration-fiscal/new_datasets_2026_09_17/raw/lns_replications`. The stager is copy-only; the manifest describes the source tree. Current staged files are already present. No NLS re-download or ICPSR account retry is needed for the completed analyses.

The existing GSS/ANES lane was also repaired: GSS parental-birthplace codes 3/5/7 do not establish second generation, and unknown-generation whites must not enter either auxiliary G1–2 group. Reproduction from that lane's directory:

```bash
uv run python3 gss_gen.py
uv run --with statsmodels python3 gss_adj.py
uv run python3 anes_gen.py
uv run --with statsmodels python3 anes_adj.py
uv run python3 -m pytest -q test_generation.py
```

Execution note: the new dependency download stalled; the adjusted reruns completed with an already-installed local Python3.13 environment containing statsmodels and pyreadstat. The unused download process was stopped. This affected dependency transport, not analysis completion. No data file was silently substituted.

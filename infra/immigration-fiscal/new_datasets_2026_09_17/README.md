# September 17 survey intake and conclusion audit

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

Outputs:

- `derived/pew/`: survey metadata/weights, direct-item generation diagnostics, weighted tables and missingness. Independent cross-sections are appended only for the documented 2015/2015–16 complementary population calculation. Both rounded 89/11 and published-count 37.8m/4.9m calibrations are retained.
- `derived/icpsr/`: extracted documentation, parsed marginal tables and arithmetic bounds. No synthetic respondent data are created. Missing actual LNS data are DS0001 or DS0003; NYC's catalog requires a restricted-use agreement.
- `derived/nlsy/`: selected columns, codebooks, tagset coverage, baseline archive hash, same-person join diagnostics, six descriptive tables. All participant-level derivatives remain ignored.
- `derived/other_audit/`: independent CILS contrasts/missing-record completion bounds and IIMMLA sex-by-parental-education contrasts. Illustrative independent-binomial intervals are not survey-design population intervals.

The existing GSS/ANES lane was also repaired: GSS parental-birthplace codes 3/5/7 do not establish second generation, and unknown-generation whites must not enter either auxiliary G1–2 group. Reproduction from that lane's directory:

```bash
uv run python3 gss_gen.py
uv run --with statsmodels python3 gss_adj.py
uv run python3 anes_gen.py
uv run --with statsmodels python3 anes_adj.py
uv run python3 -m pytest -q test_generation.py
```

Execution note: the new dependency download stalled; the adjusted reruns completed with an already-installed local Python3.13 environment containing statsmodels and pyreadstat. The unused download process was stopped. This affected dependency transport, not analysis completion. No data file was silently substituted.

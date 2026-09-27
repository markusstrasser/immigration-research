**Verdict:** The 2023 cross-survey discrepancy remains, principally in Medicare.
New MCBS2022 data yield a smaller and imprecise discrepancy; retrospective 2024
prediction is mixed. See [RESULT.md](RESULT.md) and the pre-scoring [Design.md](Design.md).

From the main repository root:

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/validation_medical_2026_09_28/acquire.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/validation_medical_2026_09_28/analysis.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 -m pytest -q -p no:cacheprovider infra/immigration-fiscal/validation_medical_2026_09_28/test_analysis.py
```

In a managed worktree, run the main checkout's environment and pass the worktree
script's absolute path. `--source-root` points to the checkout holding existing ignored
inputs; `--out-dir` changes only this lane's output destination. Raw inputs are read-only.

Inputs reused: pooled MEPS2016–2024 and HC-036 design from
`medical_ethnicity_pooled_2026_09_23`, raw MEPS2023 SAS layout/data, MCBS2023 from
`fiscal_access_2026_09_20`. The new CMS2022 ZIP/codebook are in `_cache/`; restore
with `acquire.py`, which checks hashes and archive/content validity before writing.
An input/source hash manifest is generated in `derived/audit.json`. All outputs and
downloaded inputs are ignored; source scripts, design, report and tests are tracked.

Guards reproduce the existing 2023 headline ratios, check 2022 codebook counts,
preserve complete age-sex support, reject empty replicate domains, and enforce payer
decomposition closure. Six deterministic tests exercise tail treatment, replicate
variance identities and drift of the authoritative acquisition pins. These verify
implementation; they are not external validation.

Review fix, 2026-09-28: analysis now loads both CMS2022 source pins directly from
`acquire.py` through a path-based module loader, including when tests import analysis
by specification. The source manifest also fingerprints `acquire.py`. Six tests pass;
the generator exits successfully; all five numerical CSV outputs are byte-identical
to the pre-fix outputs. Only provenance metadata changes.

Covered: public payer components, four-cell age/sex composition, CMS-style disclosure
tail treatment, capped sensitivities, income and MA proxies, a new 2022 external check,
and 2024 retrospective prediction using the common survey design. Skipped with reasons: exact MA/FFS
enrollment and monthly exposure, Mexican-origin and country-of-birth splits in MCBS,
facility/hospice exclusions and detailed health matching (fields unavailable); restricted
claims acquisition (outside this public-data exercise).

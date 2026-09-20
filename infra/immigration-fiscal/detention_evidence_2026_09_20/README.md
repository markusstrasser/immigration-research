# Detention evidence, September20,2026

This acquisition bundle separates custody legal basis, criminal history, federal primary sentencing offence and fiscal payer. Read RESULT.md for source-specific limitations. It supplies verified cells and records, not a national crime correction or new fiscal total.

`manifest.json`: fourteen hashed inputs, source URLs and documentation. `_cache/`: original bytes, codebooks, extracted text and cell dumps. `probe.py`: portable local verification using openpyxl. `derived/probes.json`: verified ICE FY2024 detainee-days, SCAAP FY2024 reported award aggregates and BJS midyear2023 local custody for ICE. Raw files are read-only evidence; outputs rederive.

Reproduce: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with openpyxl python3 probe.py`.

Acquire or rebuild: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with pdfplumber python3 acquire_sources.py`. Existing pinned bytes are verified; missing inputs use manifest URLs. To reuse held originals explicitly pass `--source-repo /path/to/immigration-research`; add `--offline` to forbid downloads. Network errors and hash drift fail rather than substitute newer content. SCAAP CSV is regenerated from the official PDF through `parse_scaap.py` and checked against its retained exact hash; it belongs in `derived/`, not among original agency data. Source parser lineage is recorded in the manifest.

Validation: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with openpyxl python3 -O test_contract.py`; also run `python3 -O probe.py` in that environment. Empty manifests, missing principal sources/cache and changed bytes fail under optimized Python. BJS standard error is read from the second matching ICE column, validated against the table's standard-error header.

The lane tracks acquisition, parsing and validation scripts plus the manifest and documentation. The 13 original source files in `_cache/` and generated SCAAP CSV/probe receipt in `derived/` are ignored. The manifest distinguishes agency originals from project-derived data.

Vera's raw files are unmodified official ICE publications with archive attribution; the dictionary/license are bundled. Government PDFs are public official publications. The SCAAP parsed CSV is pre-existing project-derived data; retain the paired official PDF and do not imply it came from BJA as a CSV.

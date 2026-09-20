# Fiscal source acquisition and access routes

Read `RESULT.md` for acquired versus restricted status and the concrete access route.

- `manifest.json`, `extra_manifest.json`, `fee_manifest.json`: frozen successful sources and failed attempts; the fee manifest pins the repaired URL.
- `restore.py`: restores missing successful sources from the frozen inventory; checks existing bytes without overwriting, verifies downloads before atomic installation, never refreshes a vintage or rewrites manifests, and separately reports failed attempts.
- `validate_mcbs.py`: all three manifest inventories and hashes, pinned MCBS archive/member/codebook, exact 134-column schema, row/year/ID/weight/frequency gates; outputs `derived/mcbs_validation.json` and reports failed acquisitions explicitly.
- `check_validation.py`: failure regressions for empty or unsuccessful inventories, corrupt bytes, wrong ZIP member metadata and forbidden directory fallback; safe under `python -O`.
- `check_restore.py`: offline fixtures verify missing-file restoration, invalid-download rejection, preservation of corrupt existing bytes and immutable manifests.
- `_cache/`: acquired public source bytes. `derived/`: regenerated inspection results.
- `REGISTER_SNIPPET.md`: minimal dataset-register addition.

For a fresh checkout, run `uv run --with pandas --with requests python3 restore.py`, then `uv run --with pandas python3 validate_mcbs.py`. Restoration requires network access and fails if a publisher has replaced pinned source bytes. Existing mismatched files are never overwritten. Run `uv run --with pandas python3 -O check_validation.py` to exercise failure gates.

No restricted microdata were downloaded, and no paid or contractual action occurred. Keep `_cache/`, `derived/`, extracted docs and `__pycache__/` out of version control.

**Verdict:** Complete. Final rerun `IDENTICAL: 18/18 files unchanged`, exit0, at 2026-10-14 23:09:51+09:00 (`date -Iseconds`). No `--allow-unrun`.

- 36 input pins verified; 24 frozen-v7 controls; 390 source/extraction/accounting gates; 340 conditional arm rows and 66 threshold rows.
- Fourteen tests passed; all lane Python sources compile without bytecode writes. Frozen and peer files were not edited. Git operations were read-only.
- Last measured build: exit0, 11.452s, peak child RSS 228.66MiB, using `perf_counter` and `getrusage`; no ps/sysctl/time-l calls. Metrics are not part of deterministic derived outputs.
- Initial tests appended this lane's node IDs to the ignored repo cache `.pytest_cache/v/cache/nodeids`; later tests isolate `_cache/pytest`. The incidental root cache edit is listed in `changed-paths.txt` for the parent.
- Exact extraction is from primary PDFs/CSVs, not a model transcription. Ownership source PDF page71 was visually verified against the OCR labels and amounts. Qualified-retirement rates and φ remain unmeasured, not gate failures.
- Citation checker: 4/4 published-paper DOIs resolved, 0 hallucinated, 0 unreachable, exit0. Title, journal and year match each claimed paper; full-text claim support was checked separately.

Reproduction command:

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/corporate_rents_2026_10_14 "uv run --no-project python3 {lane}/measured_run.py sh {lane}/run_all.sh"
```

No `--allow-unrun`: every live lane script is covered by the wrapper or its command. Research retrieval/extraction scratch scripts live in ignored `_cache/` and are not live lane commands.

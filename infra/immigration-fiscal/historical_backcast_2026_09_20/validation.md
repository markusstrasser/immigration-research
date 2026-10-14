**Verdict:** Deterministic checks passed before final reproduction; the final reproduction receipt will be appended below.

- Full suite after the production-path fix: 29 passed in 28.55 seconds.
- New pandemic uncertainty test plus all P7 tests: 9 passed in 1.88 seconds.
- `git diff --no-ext-diff --check -- <lane>`: exit 0.
- Review: `code-review.md`; both recorded findings resolved with source and regression checks. No frozen case files or research docs changed.
- Positive control: all four `derived/oct14/` outputs reproduce byte for byte. Programme 2024 anchors close to the live engine at 1e-6bn; national charged-base closure at 1e-9bn.
- Source lineage: primary files in `inputs/pins.json`; raw CPS sources in `derived/p7/use_source_manifest.json`; remaining consumed dependencies in `derived/p7/audit.json`.

## Final reproducibility command

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/historical_backcast_2026_09_20 \
  "uv run --no-project python3 {lane}/acquire_p7.py" \
  "uv run --no-project python3 {lane}/historical_use.py" \
  "node {lane}/programme_inputs.cjs" \
  "uv run --no-project python3 {lane}/backcast.py --case oct14" \
  "uv run --no-project python3 {lane}/backcast_categories.py" \
  "uv run --no-project python3 {lane}/p7_backcast.py" \
  "uv run --no-project python3 {lane}/write_p7_result.py" \
  "uv run --no-project python3 -m pytest {lane}/test_backcast.py {lane}/test_historical_use.py {lane}/test_p7_backcast.py -q --import-mode=importlib"
```

No `--allow-unrun`: every changed/new script is named. `programme_inputs.cjs` also runs through `p7_backcast.py`; the explicit command lets the reproduction coverage gate verify that dependency. Superseded case outputs are regression-checked in scratch directories, not overwritten.

## Timings and memory

Measured with Python `time.perf_counter` and `resource.getrusage`, never `/usr/bin/time -l`, `ps` or `sysctl`. P7 numerical builds took about 4–9 seconds with peak RSS about 0.20GB. The complete historical-use build took 24.13 seconds with peak RSS 1.90GB, below the 2.5GB limit. Cached parsing of a verified BEA workbook sheet avoids hundreds of repeated Excel parses; no hash or numerical gate was loosened.

## Final receipt — 2026-10-14

**PASS:** All eight commands above returned 0, including the complete regression suite. `rerun_lane.py` ended **`IDENTICAL: 65/65 files unchanged`**, exit 0, with no `--allow-unrun`. Python measured 55.830 seconds and maximum child peak RSS 1,909,719,040 bytes (1.91GB). The backup receipt is `/var/folders/td/k9yd1c8n5478my_42k9tb89h0000gn/T/rerun_nssegbbq/lane`.

This receipt covers the final numerical artifacts and generated docs. This dated validation paragraph was appended afterward. All edits are within the assigned lane plus the explicitly assigned scratch result; git metadata remained read-only.

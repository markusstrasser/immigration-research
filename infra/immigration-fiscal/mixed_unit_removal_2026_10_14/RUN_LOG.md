**Verdict:** Validated conditional results; no new adoption recommended. Forty tests pass, all original controls and the memory gate pass, and the final inventory-inclusive full-lane rerun is IDENTICAL 60/60, exit 0.

- 2026-10-14 20:47 JST: first integrated run, 177.604s, peak RSS 2,321.7 MiB; original 83 gates and six byte controls passed. M1 +6.723962369, M2 +0.850817060, M3 −0.800464477, conditional SNAP −1.069500698, fixed-pool M5 +4.372536264bn. The review later identified a federal replicate-denominator mismatch; the central estimates were unaffected and all SE outputs were rebuilt.
- 2026-10-14 20:52:47 JST: Python cProfile run, 203.087s, peak RSS 2,165.1 MiB. Of this, 108.290s was repeated CBO group-mask summation. Replaced masks with sufficient weighted totals and vectorized roster indexing. Profile retained at `_cache/runtime.prof`.
- 2026-10-14 20:56 JST: optimized run, 54.451s; every reported numeric cell matched the profiled run exactly. Peak RSS 2,621.3 MiB exceeded the brief's memory limit. Added a fail-loud 2.5GB gate; a subsequent integrated run was correctly blocked before publishing outputs.
- 2026-10-14 21:05:16 JST: replaced federal per-return replicate matrices with direct weighted contractions and ran the existing benefits CLI in a fresh process, exchanging only exact 3×161 component arrays. Successful full run: **62.468s; self peak 1.467GB; largest child 1.672GB**, both under 2.5GB. Original credit controls, symmetry, national/generation/weight gates and the new memory gate pass. Tax-only +6.774314951bn (SE 4.075206683); conditional fixed-pool stack +10.077350517bn (SE 4.163753225). The modeled M6 roster count is 0.970877M; fiscal correction remains unidentified.
- Runtime uses `time.perf_counter` and `resource.getrusage`; no `ps`, `sysctl` or `/usr/bin/time -l` call.
- 2026-10-14 21:09:12 JST: full-lane `rerun_lane.py`, five live commands, all return codes 0; **IDENTICAL: 59/59**, exit 0, no `--allow-unrun`. All 40 tests pass, including independent statutory probes, survey controls, claimant reassignment, the replicate calibration cancellation, signed-weight conservation, and sufficient-total/matrix equivalence.
- Profiling and memory optimizations preserve every reported numeric cell within **1.0001e−12bn**, checked against `_cache/pre_optimization_results.csv` at a fixed 1e−9bn limit. No scientific tolerance was relaxed.
- Early pytest commands updated the shared derived cache files `.pytest_cache/v/cache/nodeids` and `.pytest_cache/v/cache/lastfailed`. Later test commands disable pytest caching. Those shared caches are preserved because other workers use them; no source outside the assigned lane was edited. Both cache paths are disclosed in `changed-paths.txt`.
- Final inventory-inclusive full-lane rerun: **IDENTICAL: 60/60**, exit 0; all five live commands return 0, no allowed-unrun exclusions. This receipt was appended after the successful check; executable source and generated numeric outputs were unchanged.

Reproduction commands (read-only Git access inside `rerun_lane.py`; no allowed-unrun exclusions):
```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/mixed_unit_removal_2026_10_14 \
  "node {lane}/case_inputs.cjs" \
  "uv run --no-project python3 {lane}/state_tax.py --run" \
  "uv run --no-project python3 {lane}/benefits.py" \
  "uv run --no-project python3 {lane}/removal.py" \
  "uv run --no-project python3 -m pytest -p no:cacheprovider {lane}/test_removal.py {lane}/test_state_tax.py {lane}/test_benefits.py -q"
```

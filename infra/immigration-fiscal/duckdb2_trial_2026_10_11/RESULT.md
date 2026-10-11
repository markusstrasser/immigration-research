# DuckDB 2 trial result — 2026-10-11

**Keep the current DuckDB dependency.** This pinned alpha preserved the tested
results, but delivered no repeatable material speedup on the substantial local
queries. The ACS calculation slowed down with both the bounded and normal memory
budgets. VARIANT passed a real-data fidelity probe, without a scale-based reason
to migrate the catalog.

These are measured SQL execution times on this desktop, not estimated savings or
pipeline-wide timings. Baseline Python package/engine: `1.5.5` / `v1.5.5`.
Candidate: `2.0.0.dev2610011535` / `v2.0.0-alpha43763`. Both used Python 3.13.6,
macOS 27.2 ARM64, six threads and UTC. Canonical data stayed read-only, and
before/after hashes matched. Project dependencies were not changed.

## Normal memory budget: the actual ACS caller setting

Six rounds, every permutation of three arm orders, fresh processes and full
result fetches. All arms reported the same default memory limit: **14.3 GiB**.
Both query outputs matched exactly in every arm and execution.

| Query | 1.5.5 first / warm | v2 first / warm | v2 warm change |
|---|---:|---:|---:|
| IPUMS weighted scan, 44.4M input records | 182 / 190 ms | 167 / 183 ms | 4% faster |
| ACS cells, 3.42M input records and 81 weights | 1.21 / 1.49 s | 2.40 / 2.02 s | 35% slower |

Medians above include full execution/materialization but exclude connection
setup, imports, output sorting/serialization and input hashing. First execution
does not mean OS-cold: the machine cache was not purged. The first-execution ACS
median was 98% slower. Variability was substantial: first ACS ranges were
1.07–4.40 s on stable and 1.73–3.26 s on v2; warm ranges were 1.04–2.21 s and
1.67–2.56 s. These small samples support a local adoption decision, not a precise
general performance forecast.

Disabling v2 read-ahead did not consistently rescue the regression: ACS medians
were 2.11 s first and 2.55 s warm. The earlier diagnostic's timed samples also
showed slower ACS medians; its subsequent profile collection failed on a
profiling-setting order error, so it did not produce a success summary. That
error was fixed, tested and the complete diagnostic rerun successfully. The
verified diagnostic is `_cache/diagnostic-validated/`.

Separate untimed ACS profiles reported no temporary-directory spilling in any
arm. This narrows one explanation; the engine-change mechanism is unresolved.
v2 changed the JSON profile layout to `query` / `system` / `operator` sections.
Cross-version scan counters were not treated as equivalent without verifying
their definitions. The read-ahead control follows the documented setting; it
does not revert the other v2 engine changes.
[DuckDB async-I/O design](https://duckdb.org/2026/07/31/asynchronous-io).

## Bounded 2 GB screen and repeatability

Three separate six-pair runs alternated engine order. Each contained four
microdata cases plus all **17 warehouse SQL files / 19 statements**, for 23
statements in total. Every full result/schema comparison was exact in all three
runs. The final validated run gave:

| Query | 1.5.5 first / warm | v2 first / warm |
|---|---:|---:|
| IPUMS weighted scan | 174 / 164 ms | 184 / 178 ms |
| IPUMS person-key join, two 6.56M-record extracts | 138 / 129 ms | 148 / 133 ms |
| IPUMS filtered education-quality query | 8.45 / 7.82 ms | 5.18 / 4.88 ms |
| ACS 81-weight cells | 1.12 / 1.27 s | 1.50 / 1.66 s |

The first screen suggested a 2× first-execution IPUMS scan gain. It did not
replicate: the next two first-execution speed ratios were 1.01× and 0.94×.
ACS warm medians were 32%, 37% and 30% slower across the three screens. The
filtered-quality improvement repeated, but saves about 3 ms; the protocol treats
sub-10-ms differences as immaterial. Most warehouse queries were also below
10 ms. One exception was the first metadata-listing query: 2.55 ms on stable
versus 97.5 ms on v2, then below 1 ms on the warm connection.

The final process-wide median peak RSS was 1,966 MB on stable versus 1,837 MB
on v2. This includes all queries and Python result handling; it does not measure
ACS-only memory or establish pipeline memory savings.

The initial adoption screen required exact/tolerant correctness, a repeatable
≥1.5× useful-query gain and no ≥20% meaningful regression. Correctness passed;
the performance requirements failed. No default upgrade is supported.

## New features: what earned a use here

**VARIANT fidelity works on the existing IPUMS catalog.** All fifteen records
survived JSON → VARIANT, checkpoint and read-only reopen. Both scalar and nested
array projections matched equivalent JSON queries. The live minimum row-group
size for shredding was 30,000 records; this fixture supports no shredding speed/storage
claim. VARIANT existed in v1.5; v2's important addition is its storage/execution
pipeline. [Official preview](https://duckdb.org/2026/08/17/duckdb-20-highlights).

There is a query compatibility detail: `payload.status::VARCHAR` on JSON yields
`"held"`, including quotes; the VARIANT cast yields `held`. The JSON equivalent
is `json_extract_string(payload, '$.status')`. The initial identical-SQL
projection check therefore failed despite a correct full-record round-trip;
equivalent extraction queries passed. The probe records both representations.
Its v2 scratch database could not be reopened by 1.5.5 (unsupported file version
999). Keep these preview files isolated from canonical warehouses.

Possible future use: retain nested source/catalog/mining payloads for inspection
when flattening discards useful structure. Current catalog/mining volumes are
small, typed tables already work, and no measured benefit justifies a migration.
Mined claims must retain their unverified evidence status.

The repo's SQL runner uses Python; the new CLI agent mode would require a
separate caller and was not tested. Its output caps can stop a query early, so a
previewed result cannot replace these full-result comparisons.
[CLI agent mode](https://duckdb.org/2026/10/09/agent-mode).
No traced current requirement justified adding Quack, triggers, nested schemas
or a recursive-CTE workflow. Remote-storage gains were not tested on these local
files. The JavaScript main-case fiscal engine and full CPS carryover pipeline
were outside this screening; no speed or scientific-validation claim covers them.

## Receipts and validation

- Protocol commits: initial `7e4e3e25`; caller-memory follow-up `5503c460`.
- First two bounded screens: `_cache/run/`, `_cache/confirmation/`;
  manifest SHA-256 `adb0fe966257a458b6c2276b90b1597b425ff8f94f03c01cc7dd66567d866360`.
- Final bounded screen: `_cache/validated/`; 41 source/input hashes unchanged;
  manifest SHA-256 `15561d03bc5fd8cb75692390f2ed93079633e63e3e539d9433fd17b76325fcf0`.
- Final default-memory diagnostic: `_cache/diagnostic-validated/`;
  manifest SHA-256 `293a83919f43be1da7c76968f48b43f6429220206da61cefc6efaaf8a5433d9e`.
- Final catalog probe: `_cache/features-verified/results.json`; full round-trip
  and both projection checks passed, source hash unchanged.
- Code-review scout covered `trial.py`, `features.py`, `diagnose.py`. All three
  medium findings were checked and fixed: failed-connection cleanup, timeout
  evidence/worker cleanup and relative parent/worker path handling.
- Four failure-path tests passed under unittest and pytest; Python compile check
  passed. Tests reject missing rows/type changes, preserve SQL failure receipts,
  retain timeout/nonzero-exit output and verify baseline JSON profiling.
- Repo reproduction runner: all four commands exited zero; **IDENTICAL: 7/7**
  source/doc files unchanged. Timings/full results are ignored artifacts, not
  byte-identical timing forecasts. See [README.md](README.md) for rerun commands.

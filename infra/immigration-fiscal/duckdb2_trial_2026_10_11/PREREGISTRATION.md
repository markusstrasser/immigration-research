# DuckDB 2 preview on immigration research

Registered before workload timings, 2026-10-11. Screening, on this machine and
these existing local inputs; no claim about all queries or pipeline-wide speed.

- Baseline: installed/locked DuckDB 1.5.5. Candidate Python package:
  `2.0.0.dev2610011535`, probed engine `v2.0.0-alpha43763`.
- Same Python interpreter, six threads, 2 GB DuckDB memory limit, UTC, read-only
  input connections. Output/scratch files confined to this lane's ignored `_cache`.
- Workloads: existing ACS creative-labour cell query (81 weights, unmodified SQL
  captured from its builder); IPUMS population/earnings scan; IPUMS person-key
  join with allocation flags; year-filtered IPUMS education-quality scan; all
  checked-in warehouse SQL files, including every returned row and statement.
- Six paired rounds, alternate baseline/candidate order. Each engine gets a
  fresh process; each query runs once then again on the same connection. Neither
  run is called an OS-cold read: no machine-wide cache purge. Separately report
  first execution and connection-warm execution. Imports/setup/serialization and
  input hashing excluded from query timers. Resource peak is process-wide RSS.
- Record all SQL, input/source SHA-256, versions, full result schemas/rows, errors,
  per-execution times and process RSS. No silent optional-query skips. A failed
  workload remains a failure, and partial runs cannot produce a success verdict.
- Correctness: names/types, cardinality, strings, integers, decimals and NULLs
  must match; floating aggregates use relative tolerance 1e-12, absolute 1e-8.
  Exact equality is reported separately. Deliberate count, schema and NULL
  perturbations must fail the comparison before timing begins.
- A candidate for adoption needs all comparisons to pass, a repeatable >=1.5x
  median gain on a useful workload, and no >=20% regression on another meaningful
  workload. This screening does not alone change the repo's default runtime.
  Sub-10-ms query differences are treated as immaterial.
- Feature probes use the actual small IPUMS catalog: JSON -> VARIANT persistence
  and round-trip of all records. Availability is not a performance or usefulness
  finding. Remote I/O, server topology and synthetic deep graphs are outside the
  timed comparison because no current caller requires them.

Consumer: this lane's result guides whether to introduce a pinned optional v2
analysis command, expand validation, or retain the current dependency. The fiscal
headline is computed by the JavaScript main-case engine and is outside this test.

Method controls follow DuckDB's own async-I/O experiment: identical query and
inputs, controlled threads/memory, distinguish cached from uncached execution,
and verify results. Our cache regime is explicitly weaker than its purged-cache
or cache-disabled remote measurements:
https://duckdb.org/2026/07/31/asynchronous-io

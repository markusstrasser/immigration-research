# Follow-up: match the caller's memory budget and vary read-ahead

Registered after two six-pair screenings, before diagnostic timings. Those runs
showed no repeatable material large-IPUMS speedup and a repeatable ACS slowdown
at 2 GB. The ACS caller sets six threads and leaves DuckDB's memory limit at its
default. Thus the 2 GB screening does not establish its normal execution speed.

Use the exact captured SQL and inputs from `_cache/run/manifest.json` for the
large IPUMS weighted scan and ACS 81-weight cells. Recheck input hashes. Compare
three arms in fresh processes: 1.5.5 default memory; pinned v2 default memory and
read-ahead; pinned v2 default memory with `read_ahead_depth=0`. Verify that actual
memory limits agree. Six rounds use every permutation of the three arm orders;
each query executes first and connection-warm. Same six threads, UTC, full fetch,
schema/result comparison and no OS-cache purge as the original screening.

Do not combine these timings with the 2 GB results. The default-memory arms
address the actual ACS caller configuration; the read-ahead arm is a mechanism
probe within v2. Disabling read-ahead is not a full reversion to the v1 engine.
Record a separate untimed JSON profile for each query after its timed executions.
Profiles can locate scans/materialization/spill but do not alone identify a
causal explanation for a version change. This diagnostic cannot authorize a
default dependency upgrade or establish pipeline-wide speed.

Read-ahead setting semantics:
https://duckdb.org/2026/07/31/asynchronous-io

# DuckDB 2 trial on immigration research

This lane tests real local SQL without rebuilding source data or changing the
project dependency. The pinned candidate is Python package
`2.0.0.dev2610011535`, engine `v2.0.0-alpha43763`; baseline is the installed and
locked `1.5.5`. See [RESULT.md](RESULT.md) for the measured decision.

From the repository root, with the existing local data and project environment:

```bash
uv run --no-sync python3 infra/immigration-fiscal/duckdb2_trial_2026_10_11/trial.py
uv run --no-sync python3 infra/immigration-fiscal/duckdb2_trial_2026_10_11/trial.py \
  --out infra/immigration-fiscal/duckdb2_trial_2026_10_11/_cache/confirmation
uv run --no-sync python3 infra/immigration-fiscal/duckdb2_trial_2026_10_11/diagnose.py
uv run --isolated --no-project --python .venv/bin/python \
  --with duckdb==2.0.0.dev2610011535 python3 \
  infra/immigration-fiscal/duckdb2_trial_2026_10_11/features.py \
  --out infra/immigration-fiscal/duckdb2_trial_2026_10_11/_cache/features-fixed
```

Every output directory must be new; use `--out` to retain earlier receipts.
`diagnose.py --input <manifest.json>` consumes a completed screening manifest and
refuses changed source/input hashes. The scripts deliberately require these local
datasets instead of downloading replacements or silently skipping missing cases.
The isolated workers use the invoking Python interpreter and pinned DuckDB wheels.

`trial.py` measures four microdata queries plus every checked-in warehouse SQL
file. It captures the ACS SQL from the existing builder, including all 81 weight
aggregates and integer-cent earnings expressions. The three IPUMS queries test
the store's weighted scan, person keys and education-quality fields; they are
bounded analytical probes rather than full store-rebuild validation. It executes
every SQL statement and fetches every result row. Schema, counts, NULLs, integers
and decimals must agree; floating values have a tight declared tolerance, and
exact equality is reported separately. Negative controls run before measurement.

The screening has a shared 2 GB limit. `diagnose.py` separately uses DuckDB's
actual default memory limit to match the ACS caller, and compares v2 read-ahead
enabled versus disabled. Untimed JSON profiles are collected after all timed
rounds. Neither experiment purges the OS cache, so first execution means a fresh
connection/process, not a cold disk. These are same-machine screenings, with
ordinary desktop noise, not pipeline-wide or remote-storage benchmarks.

`features.py` persists all fifteen real IPUMS catalog records as VARIANT, reopens
the scratch database and checks full round-trip plus scalar/array projections.
It records the JSON/VARIANT string-cast difference. It does not manufacture enough
records to claim shredding performance or migrate the canonical catalog.

Canonical databases and attached warehouses are opened read-only. Source/input
SHA-256 hashes are checked before and after the run. Scratch databases, full
results, captured SQL, timings, profiles and errors live under ignored `_cache/`.
The feature probe writes only its scratch database. These tests cover SQL
execution; the main-case fiscal engine is JavaScript and has its own contracts.

The protocols were committed before their respective measurements:
[initial screening](PREREGISTRATION.md), [memory/read-ahead follow-up](DIAGNOSTIC_PROTOCOL.md).

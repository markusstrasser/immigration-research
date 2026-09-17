# Ledger stress tests — September 17, 2026

Two stress tests on the all-age partial fiscal account built by
[`all_age_ledger_2026_09_17`](../all_age_ledger_2026_09_17/): within-state matched
gaps (state group × age cells) and earnings/tax measurement sensitivity. Results
and interpretation: [RESULT.md](RESULT.md).

Nothing outside this directory is written. The upstream lane's `analyze` module is
imported for its objects only; `analyze.generate()` is never called.

## Reproduce

From the repository root, using the held inputs:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ledger_stress_2026_09_17/test1_state_matched.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ledger_stress_2026_09_17/test1b_generation_contrasts.py
curl -s 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=A576RC1' -o infra/immigration-fiscal/ledger_stress_2026_09_17/derived/fred_A576RC1.csv
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ledger_stress_2026_09_17/test2_earnings_scaling.py
```

Requires NumPy and pandas. The FRED fetch is a context value only; if it is absent
`test2` records the failure rather than substituting a remembered number. Outputs
land in `derived/`, which is ignored.

## Inputs

Held CPS ASEC 2025 ZIP (income year 2024), MEPS 2024 full-year file and SAS
positions, the extension lane's state parameters, and the source lane's stored
`derived/estimates.csv` used as the collapse anchor. SHA-256 hashes of all of them
are recorded in `derived/audit.json` and `derived/audit_test2.json`.

# Audit the all-age benchmark sum

`audit.py` independently reconstructs the CPS/MEPS baseline in commit
`24e75ae` using group transforms and raw donor-cell means. It reuses the
validated raw parsers, but neither the ledger allocator nor aggregate-gap
generator. It reports absolute balances, benchmark gaps, child components,
senior offsets and health sensitivity. The adult extensions and lunch
overlap sensitivity are checked against the held component CSV, not freshly
regenerated from their external source files.

Baseline reference gaps match eight age bands. The extension CSV instead
contains crude 25–64 means; its increments are kept in a separate JSON field.
Their sum is a hybrid comparison, not a consistently age-adjusted total.

```sh
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 infra/immigration-fiscal/aggregate_audit_2026_09_17/audit.py
```

Requires the held CPS2025 and MEPS2024 inputs, pandas and NumPy. Sources are
read-only; `derived/audit.json` records hashes, full-weight results and parser
checks. Missing inputs/cells, failed conservation or target overlap stop the
run. No sampling intervals, complete all-age extension or policy
counterfactual are estimated. Interpretation and source corrections are in
[the audit memo](../../../research/immigration-aggregate-and-generation-audit-2026-09-17.md).

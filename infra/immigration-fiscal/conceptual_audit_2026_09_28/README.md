# September 28 adversarial audit diagnostics

Supports [the memo](../../../research/immigration-adversarial-audit-2026-09-28.md).
Both probes read existing inputs and print JSON. They do not change audited models.

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_28/probe_population.py
node infra/immigration-fiscal/conceptual_audit_2026_09_28/probe_fiscal.cjs
```

The population probe imports the canonical target definition and requires the
September 28 input hashes. It verifies the target population, within-unit benefit
consistency, and closure of the existing generation production attribution. It
reports baseline CPS weights, before the row-4 population correction. Resource
units are not necessarily families; raw allocated benefit dollars are not calibrated
account dollars or predicted savings. It recomputes descriptive counts and reads
the existing production diagnostic; it does not rerun the production solver.

The fiscal probe changes the substitution elasticity in one named package
specification and checks that production changes while fiscal spending and public
capital do not. Success reproduces the interface finding, not a validation of the
economic model. Input hashes identify the checked source. Public workers' wage
response, their public employer's budget, employment and output need reconciliation
before calculating a correction. The script makes no dollar adjustment.

Generated captures belong in ignored `_cache/` or temporary storage. The memo
records the checked figures; raw data remain unchanged. No new regression or
causal-effect estimate is produced by either diagnostic.

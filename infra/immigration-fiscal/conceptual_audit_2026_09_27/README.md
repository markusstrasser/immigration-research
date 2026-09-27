# September 27 conceptual audit: reproducible diagnostics

These probes support [the audit memo](../../../research/immigration-conceptual-audit-2026-09-27.md).
They read model/data inputs and print JSON; they do not rewrite audited lanes.
The fiscal integration was committed as `f3031ab` during this audit. The world-ledger
and propagation briefs are specifications, not completed world or debt estimates.

From the repository root:

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_accounting.py
node infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_fiscal.cjs
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_generations.py
```

- `probe_accounting.py` reconciles 2024 federal NIPA current saving to net lending
  using the actual capital-account rows, then verifies the main-case capital split.
  The national $231.766bn difference is **not** an estimated Mexican-origin correction.
- `probe_fiscal.cjs` adds a synthetic $1bn transfer to both public-sector legs on a
  cloned model, with capital disabled. `invariant: false` is the diagnosed result;
  successful execution means the mechanism reproduced, not that the model passed
  the economic conservation requirement. The highway alternatives are different
  assumed workload laws, not causal re-estimates.
- `probe_generations.py` pins the cached CPS frame, origin table and DDI. It uses
  exactly 78 origins, 10,000 paired origin resamples and seed 20260927. Its intervals
  are sensitivity to origin resampling, not survey-design or causal confidence
  intervals. Arrival-age bounds propagate grouped arrival and birth-year uncertainty;
  unknown arrival code 0 contributes to the upper bound only. The equal-fertility
  identity example is algebra, not an empirical attrition estimate.

All three probes exited 0 after validation. The original exploratory generation
probe silently classified unknown arrival dates as outside its upper bound; the
saved probe exposes them and includes them. This moves the all-origin upper bound
from 33.51% to 33.54%, without changing the lower bound or conclusion.

Inputs are local existing data. The cached selection frame is not independently
rebuilt; its exact bytes are pinned. Fiscal probe output includes source hashes;
the imported packages also carry their own provenance checks. Generated captures
belong in ignored `_cache/`, not in a duplicate research-data archive.

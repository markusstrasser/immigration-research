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

## Expanded audit, later September 27

The four additional probes read the existing corrected models and write only
ignored diagnostics in this directory's `_cache/` (sponsorship prints JSON).
They do not implement their counterfactuals in any production model.
The original generation probe pins the first-pass inputs; subsequent upstream
repairs may intentionally invalidate those pins. Its earlier successful execution
is historical evidence, not a claim that the repaired sources reproduce old findings.

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_uncertainty.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_production.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_medical_composition.py
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_sponsorship.py
```

- `probe_uncertainty.py` reproduces all 64 September 26 schools-case CPS SEs and
  ten central benefit corrections/SEs, then combines the correction-factor
  deviations with matching CPS replicates. It retains the other published
  variances and does not produce a complete revised interval. The in-memory
  producer interception stops before its writes; baseline replay is redirected
  into `_cache/uncertainty/`. Nonlinear factor-product and first-order results
  agree closely. This is a September 26 diagnostic for the pending September 27
  extension, not a September 27 uncertainty result.
- `probe_production.py` reproduces the published fixed-hours, fully adjusted CES
  baseline before applying adopted row-4 population weights. Five existing
  matched and pooled hot-deck seeds are also run. The matched/pooled ratio arm is
  a diagnostic analogue, not an adopted estimator. No national re-raking is
  imposed beyond the existing row-4 rule. It also reconstructs the service-price
  side view from its actual native-headed consumer-unit and native wage bases.
  Outputs: `_cache/production.json`. The existing `probe_fiscal.cjs` now checks
  that the live September 27 fiscal payload leaves production unchanged and
  reports private welfare and induced receipts separately.
- `probe_medical_composition.py` reproduces the five published pooled medical
  factors, then changes the weighted cell mix. The net $0.062bn interaction is
  before LTSS and later adjustments, not a correction to the final headline.
  Output: `_cache/medical_composition.json`.
- `probe_sponsorship.py` reproduces the sponsorship and central lineage baselines,
  verifies cancellation of the admissions numerator in the estimator ratio,
  and probes timing and parent survival. Its birth-count adjustment is valid
  within the existing all-births-at-29 convention, not a full fertility projection.
  Timing holds the naturalization and petition probabilities fixed. No new
  empirical hazard is estimated.

Inputs and producer hashes are reported. Assertions check baseline reproduction;
diagnostic differences are findings rather than assertions that a model passed.

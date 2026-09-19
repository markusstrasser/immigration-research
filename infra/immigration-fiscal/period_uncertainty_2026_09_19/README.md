# Adult fiscal period profiles with conditional uncertainty

Consumes the education/origin annual account, matching ACS institutional counts, MEPS healthcare sensitivity and the existing NVSS life-table reader. The default inputs are canonical lanes under `infra/immigration-fiscal/`. Raw data are read-only. All generated artifacts are ignored by Git.

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache OPENBLAS_NUM_THREADS=1 \
  uv run --no-project python3 \
  infra/immigration-fiscal/period_uncertainty_2026_09_19/period_uncertainty.py

UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 -m pytest \
  infra/immigration-fiscal/period_uncertainty_2026_09_19/test_period_uncertainty.py -q
```

Run the [health](../health_transport_sensitivity_2026_09_19/README.md), [annual](../education_origin_fiscal_2026_09_19/README.md) and [institutional](../institutional_education_2026_09_19/README.md) producers first. Optional `--root`, `--annual-dir`, `--health-dir`, `--institutions-dir`, `--out-dir` select locations. The consumer verifies producer input/output fingerprints and row alignment before calculation. A changed helper requires an annual rebuild, not a manual hash edit.

## Quantities and uncertainty

For age band b, `T_br/N_br` is the net per-person balance for CPS replicate r. NVSS exposure weights are `Lx(a)/lx(25)/(1+r)^(a-25)`, summed within each band. The last age100 cell includes the life table's remaining100+ exposure at age100 discounting. An alternative ends after85. Six fiscal bands span25–34 through75+; the75+ balance is held constant. Common US-total survival isolates fiscal-profile differences; origin/education-specific mortality is not estimated here.

Sum the entire lifetime under each of160 CPS replicates, retaining each replicate's denominator. Variance is `4/160 Σ(L_r−L_0)^2`. Medical dollar gradients are divided by the corresponding point-estimate population, aggregated across ages, and multiplied by the full donor covariance: `g'Σg`. Shared donor cells therefore stay correlated across ages. Fixed medical calibration/coverage ratios and other fitted fiscal allocation coefficients are assumptions of this conditional inference.

The optional institutional cost is an ACS stock count multiplied by a hypothetical public cost and allocated over CPS household residents in the matching education/origin/age cell. CPS denominator uncertainty and80 ACS replicate numerator uncertainty are propagated separately; ACS variance is `4/80 Σ(L_r−L_0)^2`. Independent-survey sampling errors and first-order propagation are assumed. The price grid0/$50k/$100k/$150k is deliberately **uncalibrated**, not an empirical bound or preferred unit cost. It represents extra cost not otherwise priced; it does not identify prison costs, transitions into institutions, or a marginal admission cost. The underlying medical calibration is to institution-excluded adjusted NHEA, documented in the health lane.

The F scenario adds the existing average per-capita defense, interest and general-government allocation, with transported TRICARE subtracted once. Its CPS and correlated MEPS uncertainty are carried through. Other government totals remain fixed. F is an attribution scenario, not estimated marginal public-goods cost.

The health-model file replaces the **entire** calibrated medical term with the alternate fit. It removes the old medical covariance and inserts the new donor covariance; simply adding the variance of their difference would double count. Replicate replacements use exactly the same CPS population. Only all-target supported alternatives are emitted. F and N are zero in this file: the alternate-medical export does not include the separate TRICARE cross-covariance needed for the F scenario. This is an explicit coverage boundary.

## Output contracts

| File | Meaning |
|---|---|
| `period_profiles.csv` | Same annual profile IDs, rates0/2/3/5%, endpoints85/100, F0/1 and institutional-price scenarios; estimate, three sampling variance components, conditional95% intervals, break-even receipts and discount derivatives |
| `health_period_profiles.csv` | Adult-age/birth, education and insurance medical alternatives, F0/N0; fully recomputed conditional intervals and change versus the canonical donor model |
| `withheld_profiles.csv` | Stock profiles failing required-age support; no synthetic fill |
| `withheld_health_profiles.csv` | Alternate donor models lacking full target age support |
| `audit.json` | Input/code/output hashes, interpretation and uncertainty contracts |

All emitted primary profiles must have n≥30, Kish weight ESS≥20 and positive population in every CPS replicate in every required age band. This is a declared reporting rule, not a calibrated precision guarantee. Every recent-arrival profile is excluded from lifetime projection regardless of sample size. Institutional raw-n and sparse/zero-cell flags are retained separately: CPS support does not certify ACS support. Sparse ACS normal intervals can be unreliable; zero observed records and zero design SE do not establish zero institutional risk. Group-quarter records can include whole-person imputation.

The signed break-even amount is `−NPV`; a positive number is missing net receipts needed to reach zero, while a negative number is fiscal room before reaching zero. The nonnegative version truncates this at zero. Dividing by the survival annuity gives a constant annual equivalent. None measures omitted private benefits or total US welfare. Analytic `dNPV/dr` is tested against finite differences; the per-percentage-point column is a local derivative, not an exact finite-rate change.

## Scope and regression checks

These are current-resident period profiles conditional on common survival and fixed2024 real flows. No future policy, real earnings growth, education transitions, selective emigration or descendants are estimated. They are neither admission cohorts nor completed lifetimes. The year25 entry interpretation remains invalid.

Tests cover shared age-error covariance, shared-donor cancellation, independent ACS/CPS perturbations with uncertain denominators, mixed-sign discount derivatives, withholding missing ages and stale/tampered release rejection. Integration initially exposed colliding `builder` imports in sibling tests; tests now load their own files by unique module name and the combined suite runs with `--import-mode=importlib`. Producer path/hash freshness prevents stale worktree outputs from being treated as canonical.

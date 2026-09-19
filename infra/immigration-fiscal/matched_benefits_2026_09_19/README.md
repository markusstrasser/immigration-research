# Matched production and fiscal benefit scenarios

**Verdict:** Skill complementarity adds a measurable modeled channel, but the
capital-tax counterfactual matters much more for fiscal receipts. Neither a
gross revenue gain nor a private production surplus is a complete welfare effect.
See the [calculation memo](../../../research/immigration-matched-benefits-2026-09-19.md).

## Reproduce

Run from the repository root. `--source-root` may point at the canonical checkout
when an isolated worktree lacks ignored raw inputs. The builder reads those
inputs without modifying them; output paths and source hashes enter `audit.json`.

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy python3 -m unittest discover -s infra/immigration-fiscal/matched_benefits_2026_09_19 -v
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy python3 infra/immigration-fiscal/matched_benefits_2026_09_19/builder.py --source-root /Users/alien/Projects/immigration-research
```

`--offline` uses the existing dependency cache and fails if dependencies are not
available; omit only when network access is available. No silent download or
substitute data source is used. `--out` changes the ignored derived directory.

## Model

Current normalized capital and both skill quantities equal1. National labor
compensation shares are `a[j]`; within-skill target earnings shares are `m[j]`.
Current output is `Y`; labor's share is `s`. The absent-target skill quantities
are `x[j]=(1-m[j])*h[j]`, with outside-worker hours ratio `h[j]`.

```
rho = 1 - 1/sigma
q = sum(a[j]*x[j]**rho)**(1/rho)       # geometric limit at sigma=1
K_without = q**adjustment
Y_without/Y = q**(s + adjustment*(1-s))
w_without[j]/w_current[j] = q**(s + adjustment*(1-s)-rho)*x[j]**(rho-1)
h[j] = (w_without[j]/w_current[j])**labor_supply_elasticity
```

`adjustment=0/.5/1` means fixed/intermediate/fully adjusted capital, not an
estimated number of years. Released capital earns the initial rental rate
elsewhere. Its opportunity income `(1-s)*Y*(1-K_without)` is subtracted from
the domestic capital-income gain. Under full adjustment net capital-income
gain is zero; skill-composition gains can remain.

Tax-retention0/.5/1 says how much of the alternative capital return would still
generate US taxes. The selected capital rate .246 is a transported2011–2013
macroeconomic rate excluding sales taxes, not a current2024 marginal rate.
Current federal/state/payroll marginal rates .384/.426 come from the2017
components of Colas–Sachs Table1; .303/.366 instead subtract discounted future
Social Security accrual and are exported as a different fiscal object.

The main model assigns all capital to outside-union residents. Optional
excluded-owner shares0/.5/1 remove capital owners' private welfare from the
beneficiary account; all fiscal dollars still receive full weight. This is
an explicit ownership/recycling sensitivity, not an empirical estimate.

## Artifacts and checks

- `skill_composition.csv`: both education splits, earnings proxies, populations,
  positive earners and161-weight sampling uncertainty. Children with zero
  earnings stay in the target population; education cells cover valid codes.
- `scenarios.csv`:1,296 model/tax cases with joint sampling uncertainty,
  separate skill wages, hours, gross/net capital income, private WTP and taxes.
- `ownership_sensitivity.csv`:18 baseline ownership/tax-retention cases.
- `magnitude_thresholds.csv`: elasticity needed for gross income gain to match
  the assigned fiscal deficit in magnitude; explicitly not welfare break-even.
- `existing_tax_credits.csv`, `replacement_arithmetic.csv`: identified credited
  pools and replacement arithmetic. Personal capital-income-tax overlap remains
  unresolved; every candidate is marked `direct_addition_permitted=False`.
- `audit.json`: exact inputs/generator hashes, sources, scope and assumptions.

Six tests cover zero shock, homogeneous-labor and infinite-substitution limits,
small-shock curvature, independent finite-difference factor prices and capital
returns, an independent Newton solution with numerical wages for endogenous
hours, the Colas–Sachs marginal tax formula, ownership/tax conservation, and
fail-loud invalid inputs. The full build
checks the canonical fiscal population under both allocations, all161 earnings
partitions, Euler exhaustion, equilibrium residuals and the private/tax identity.

No receipt scenario is added to the fiscal ledger. No services-price estimate is
added to production income. The income model omits housing, innovation, trade,
technology choice, endogenous education, transition costs and policy selection.

# Fiscal scale and a conditional production benefit

**Verdict:** The fiscal difference remains large after population normalization.
The same observed Mexican-origin population supplies about 8.35% of surveyed
annual earnings. A standard homogeneous-labor, fixed-capital model yields roughly
$13–26bn/year of gross-income gains to other residents under the calibrations
below. This is one modeled benefit, not an estimate or bound on total welfare.

The evidence and macro reconciliation are indexed in
[the calculation memo](../../../research/immigration-benefits-and-macro-scale-2026-09-19.md).

## Reproduce

Run from the repository root with the existing CPS cache and repaired annual release:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with pandas --with numpy python3 infra/immigration-fiscal/benefit_scale_2026_09_19/builder.py --gdp-billions 29298 --gdp-source https://www.whitehouse.gov/wp-content/uploads/2026/04/2026-Economic-Report-of-the-President.pdf
```

GDP is CY2024 nominal GDP, $29,298bn, from the 2026 Economic Report of the
President, Table B-3, printed p374. Ignored/regenerated outputs are `income.csv`,
`fiscal_scale.csv`, `surplus_scenarios.csv`, and `audit.json` (hashes and assumptions).

## Scope and formula

Population: the canonical civilian-household observed union of Mexico-born,
Mexican second-generation and self-identifying Mexican third-plus residents,
all ages and education. This is not complete genealogical ancestry.
Beneficiaries: everyone outside that union, including other immigrants.
This chosen perspective differs from all citizens or all native-born residents.

Let `m` be the target share of positive national cash earnings, used as a proxy
for its share of homogeneous labor efficiency. Let `s` be labor's output share.
Competitive Cobb-Douglas production, fixed technology and capital, and ownership
of all capital by other residents give:

```
surplus = Y * [1 - s*m - (1-m)**s]
```

Current output less target labor compensation is `Y*(1-s*m)`. Output with that
labor absent is `Y*(1-m)**s`. Their difference is the gross-income benefit to the
complement. It includes incumbent-factor gains and losses within this model;
it is not an additional wage bill or an identified immigration-policy effect.

[National Academies chapter4, pp169–174](https://www.nationalacademies.org/read/23550/chapter/8)
develops this framework and warns against treating a decades-old stock as a
temporary labor shock with fixed capital. With homogeneous labor, constant
returns and complete capital adjustment, this particular surplus is zero.
That says nothing about omitted channels.

Two calibrations remain separate:

- **GDP:** official GDP, assuming the cash-earnings share also describes total
  labor compensation. This scales up the compensation base by assumption.
- **Cash earnings:** implied output `Y = national positive cash earnings / s`,
  not measured GDP. Cash earnings omit noncash compensation and differ from
  national-accounts income definitions.

`s=0.60/0.65/0.70` are illustrative scenarios, not estimated parameters or
confidence bounds. Both wage-only `WSAL_VAL` and total earnings `PEARNVAL` are
reported. Negative self-employment earnings are retained in descriptive totals
but clipped to zero for the efficiency proxy; both totals are exported.

Sampling uncertainty uses all 161 CPS weights jointly, including the share
denominator and, in the cash calibration, the output base. It excludes model
uncertainty. Taxes, sector price surplus and other channels are not added.
Adding taxes to gross income gains can double count already valued income;
combining channels needs a consistent after-tax welfare account.

Checks: canonical input fingerprints; five group population anchors under both
allocations; disjoint generations; earnings conservation in every replicate;
exact production identity; zero-target and small-shock limits. Independent
in-task code review verified the formula by integrating marginal product and
subtracting target pay. Its finding, a loose small-shock test tolerance, was
fixed by setting the absolute tolerance to zero.

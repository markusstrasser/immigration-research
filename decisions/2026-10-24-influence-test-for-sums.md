---
date: 2026-10-24
concepts: [estimate-screen, influence-test, public-land]
status: reopened
supersedes: []
relations:
  - refines: decisions/2026-10-23-routing-layer-range-and-estimate-screen.md
evidence: infra/immigration-fiscal/land_price_rule_2026_10_24/RESULT.md
---

# 2026-10-24: For a sum of measured values, the influence test reprices the five largest units instead of dropping them

## Context

The estimate screen's influence test drops the five most influential observations and fails an estimate that moves
more than 25%. It was written for scaling elasticities, where one unit can carry a fitted slope. The land price rule
lane (`land_price_rule_2026_10_24`) applied it to a sum: the group's annual charge for land under public capital,
$19.74 / 23.68bn at the case rate. Dropping Los Angeles, New York, Orange, San Diego and Santa Clara moves that sum
33%, because the group lives where urban land is dearest. Dropping them deletes measured cost; it tests nothing about
a fit. Under the screen as written the estimate is "not identified" while precision (0.42), stability and data
quality (0.39% fallback share) pass.

Operator, 2026-10-24, after the recommendation to adopt the repricing test: "go on" (earlier the same day: "put it in
then").

## Alternatives considered

1. **Keep drop-five for every estimate.** Uniform, but it fails any sum whose cost is concentrated where the group
   lives, however well each unit is measured. Rejected.
2. **Reprice the five largest units at a coarser price** (county-average urban price for land). Tests whether the
   sum leans on the fine-grained prices of a few units, which is the influence question a sum can fail. Chosen.
3. **No influence test for sums.** Leaves concentration in a few units' prices unchecked. Rejected.

## Decision

For an estimate that is a sum of measured unit values (no fitted parameter), the influence test reprices the five
units with the largest contributions at the next coarser price level the lane already uses and fails the estimate if
the sum moves more than 25%. Drop-five stays the test for fitted parameters. The land price rule passes: repricing
the five counties moves the sum 2.9% / 2.8%, so its $19.7–23.7bn (case rate) is identified and enters candidate
main case v10. The drop-five result stays reported beside it.

## Evidence

- `infra/immigration-fiscal/land_price_rule_2026_10_24/derived/summary.json`; RESULT "Screen" table.
- `scripts/estimate_screen.py` docstring, test 3.

## Revisit if

- A sum's coarser price level is itself built from the five units (then the reprice is circular).
- A whole-case review finds the reprice test lets through a sum that a unit-level audit contradicts.

## Supersedes

None; refines test 3 of decisions/2026-10-23-routing-layer-range-and-estimate-screen.md for sums.

## Revisions

- 2026-10-24 15:0x JST: **reopened.** A blind review found the repricing test duplicates the stability screen's
  county-average variant and does not test concentration; the land estimate is again "not identified" and the
  drop-five rule stands until a concentration test for sums is designed (for example, an independent price source for
  the top units, or the share of the sum in the top five against a pre-set limit). Source:
  `infra/immigration-fiscal/land_price_rule_2026_10_24/RESULT.md` "Screen revision withdrawn".

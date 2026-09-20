# 2026-09-20: Integrate category-specific service responses

## Context

The annual account's prominent $270–289bn conditional loss assumes that every
assigned ordinary-service dollar is incremental. Earlier follow-up notes explained
break-even thresholds without running the evidence-informed alternative through
the principal report. The operator requested actual integration and reasoning.

## Alternatives considered

1. Retain proportional spending alone: coherent equal-service benchmark, weak as
   a description of immediate budget behavior.
2. Use the roughly20% break-even point as a cost estimate: rejected; a solved
   threshold supplies no evidence about actual response.
3. Apply CBO's63–66% to every service: rejected; the evidence concerns K–12.
4. Apply it to our whole education row: rejected; that row includes non-school
   education, and its school/college proxy mix is not an official spending split.
5. Integrate category responses, preserve uncertain composition and separate
   delayed budgets from service quality: selected.

## Decision

The main report now regenerates category-specific scenarios with production,
receipts and household transfers held fixed. CBO's school association gives
63%/66% directional sensitivity values; neither is an identified coefficient for
our population or a confidence endpoint. Economic-affairs and recreation budgets
receive zero response in the CBO-informed lag cases; other noneducation services
retain proportional response. Keep non-school education fully responsive in the
main comparison and expose zero response as a separate favorable sensitivity.

For the school fraction, use the pinned BEA national gross-function amounts and
aggregate education investment to bound the consumption-only school share at
71.5–86.5%, assuming nonnegative component investment. Transporting that range to
the target is a declared common-composition assumption. It replaces neither the
original incidence allocation nor an unobserved subgroup spending decomposition.
Diagnostics with education entirely fixed/full expose dependence on that bridge.

## Evidence

- [CBO June2025 report](https://www.cbo.gov/publication/61464), checked September20:
  school spending/enrollment associations and category-specific adjustment rules.
- Pinned BEA workbook, T31505-A lines29–32; T31700-A lines9/113. Gross-investment
  figures are excluded from the current-service bill, not charged a second time.
- [Executed annual account](../research/immigration-complete-annual-account-2026-09-20.md),
  new category-response section; `service_response_audit.json` records cells and hashes.

## Interpretation and decision impact

The narrower CBO-informed comparison gives $165–197bn/year conditional net cost;
fixing non-school education budgets lowers that to $121–160bn. Proportional
services remain the $270–289bn benchmark, not an empirically established magnitude.
The sign survives these service-response alternatives under unchanged receipt,
benefit and production assumptions. It is not a measured marginal admission,
removal saving, long-run CBO forecast, or complete welfare estimate. Production is
held fully adjusted to isolate the service channel; mixed adjustment assumptions
do not describe a coherent estimated time path. Unpriced congestion and the
property-receipt bridge remain separate uncertainties.

## Revisit if

Matched national category response estimates, subgroup-specific current education
composition, a corrected receipt bridge, or measured service-quality effects
change the comparison. Lower noneducation response can still change the sign;
CBO's proportional category choices are assumptions too.

## Supersedes

Updates the interpretation in [the complete-account decision](2026-09-20-complete-account-and-fiscal-response.md).
Preserves the original calculations and the earlier sensitivity notes. The report
producer, main memo and index must present the new comparison together.

---
date: 2026-09-22
concepts: [fiscal-attribution, convention-range, arms-grid, instrument-bias]
supersedes: []
evidence: research/immigration-ledger-practitioner-range-2026-09-22.md
---

# 2026-09-22: Report the ledger's range as a practitioner hull, with the design hull and the public-goods object disclosed beside it

## Context

The September 17 ledger lane reported its convention sensitivity as the hull of every
switch combination (144 cells, −$548bn to −$87bn). The September 19 repair changed the
grid to 63 admissible cells (−$496bn to −$76bn, central −$217bn) but no memo restated the
range, and RESULT.md still prints the old one. A recut proposal on September 22 asked
which cells a budget modeler would run, and how best to give a min–max over all
assumptions of the object.

## Alternatives considered

1. **Keep the full hull as "the range".** Coherent as a design statement, but it grows
   with every arm added, including arms nobody runs (R all zero, C per capita), and it
   reads as a confidence interval it is not.
2. **Probability weights over the switches.** Rejected: priors over conventions are
   opinions dressed as probabilities, and the result would be quoted as a posterior.
3. **Practitioner hull, design hull and second object, each named** (selected): each arm
   tagged with the class of modeler that runs it; cells nobody runs disclosed and
   dropped; F per capita reported as a separate object; the arm list audited from both
   sides for missing arms, which is where instrument bias can enter.

## Decision

The reported range for this ledger is the practitioner hull, −$290bn to −$190bn around
−$217bn, built from the live grid plus five switches the grid does not hold (enforcement
netted, general government at the administration elasticity, G at cross-state function
elasticities, interest treated alike at both levels, K and D at the within-district
school elasticity). The design hull (−$496bn to −$76bn; +$41bn with the dial at zero) and
the public-goods object (−$502bn to −$402bn around −$429bn) are printed beside it, never
inside it. Standard errors are shown so that convention spread is seen to dominate
sampling. No published ledger value changes; the stale RESULT.md lines are stamped, not
edited.

Applying the recut to the complete account (a different object with its own service
response grid) is not decided here.

## Evidence

`infra/immigration-fiscal/ledger_recut_2026_09_22/` reproduces all 63 grid cells and the
marginality curve from the ledger's replicate vectors to 1e-6 $bn before adding anything.
Elasticities are the September 20 scaling test's year-effects column and within-district
school rows; G's composition is the 2022 Census of Governments functional lines. The
[scaling decision](2026-09-20-service-scaling-calibration.md) holds those elasticities as
sensitivities, which is how the lenient bound uses them.

## Revisit if

A measured response for base school current spending or public medical transfers to this
population (then the dial needs those items); the builder gains a netted enforcement arm
or a function split of G (then the added switches should move inside `arms_matrix.csv`);
or a named modeler's convention is shown to sit outside the practitioner hull.

## Supersedes

Nothing. Qualifies the "What this does not settle" section of the ledger README and the
"63 admissible arm combinations" sentence of the repaired calculation index.

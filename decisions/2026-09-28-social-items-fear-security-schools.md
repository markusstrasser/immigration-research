---
date: 2026-09-28
concepts: [social-costs, crime-costs, school-quality-spillovers]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-09-25-school-dilution-priced-beside.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md
---

# 2026-09-28: Add fear, private security and school disruption to the social total; keep property values out (adopted)

## Context

The operator listed four costs the real-costs memo left unpriced: fear and avoidance by people who
are not victims, private security, property values and school disruption. The
[social-costs lane](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md)
(ladder 258) priced them with one method per item, applied to the Mexican-origin union and, for
comparison, to non-Hispanic Black residents. Central values for the union: fear $10.49bn, security
−$0.60bn, school disruption −$1.95bn, property values 0; together $7.94bn (stacked envelope −$9.40bn
to $30.16bn). Each central rests on one assumed parameter: the fear share φ of the willingness-to-pay
excess, the crime share of security spending, or the behaviour share κ of the suspension gap.

## Alternatives considered

1. **Keep all four beside the account and out of every total.** This follows the school-dilution
   precedent. It leaves the total without costs the operator asked to have counted, even though
   the lane built the three items to be added without double counting.
2. **Add fear, security and schools to the social rows; keep property values out (recommended).**
   The three items are net of victims' own losses (fear), of government guards (security) and of
   resource dilution (schools).
3. **Also add a property-value arm.** A composition price discount is either a transfer between
   owners and buyers or a capitalisation of crime and schools, which are already priced. The only
   part that is neither is a taste for neighbours' race or ethnicity. For the union no clean price
   exists: the ACS gradient gives an over-bound of $18.5bn, while Zillow values on the same rows
   carry the opposite sign.

## Decision

Option 2, adopted by the operator on 2026-09-28 ("ok do ..."). He added that "5B seems low if
you're asking me but ok", doubting the level rather than the method; the Consequences section
records what follows from that doubt.

- The union's three items join the social rows of the fiscal-plus-social total from the
  September 27 case on. Their central sum, $7.94bn, applies at both ends of the central values;
  their stacked low (−$9.40bn) and high (+$30.16bn) apply at the ends of the full span.
- Property values stay out. The taste arms are shown in the lane and never added.
- Earlier cases keep their totals.

School disruption enters through a behaviour channel: Carrell, Hoekstra & Kuka's US estimate times
the CRDC suspension gap. That refines the September 25 rule that peer effects stay unpriced in
both directions. The composition channel it addressed remains unpriced. For the union the item is
a small gain, because Hispanic pupils are 29% of enrollment and 24% of out-of-school suspensions.

## Consequences

The published pairing moves from $363.4–438.0bn to **$371.3–445.9bn** a year at central values,
$9.1–10.9k per member. The full span moves from $325.0–473.6bn to $315.6–503.8bn. The fiscal rows
and every earlier case are unchanged.

- Totals: `sept24_propagation_2026_09_24/real_costs_totals.py --case sept27`. The Sept 24 and
  schools-case outputs rerun byte-identical.
- Winners and losers: the rerun changes only the published totals it quotes. The three items are
  not allocated among other residents, and they are not in the income split (§4).
- The operator's doubt about the level points to channels the lane did not price:
  - physical disorder, which the September 18 enclave lane measured (no group effect at equal
    income except slight litter);
  - gang violence, which is already inside victims' harm;
  - the crash and emission costs of the group's driving, which the memo lists as unpriced.

## Evidence

- [Social-costs lane](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md),
  `derived/items.csv` (fa791b1), rerun byte-identical.
- [Black comparator](../infra/immigration-fiscal/black_comparator_rough_2026_09_28/RESULT.md)
  (dd375b8), which supplies the Black victim inputs.
- CRDC 2021-22 First Look, p. 22, Figure 12, read from the primary PDF.

## Revisit if

- A measured fear or avoidance valuation replaces the assumed φ, for example a life-satisfaction
  or time-use estimate on US data.
- A US estimate of disruption by origin replaces the suspension proxy, or Mexican-origin
  suspension rates are published apart from all Hispanic pupils.
- A clean price for a taste for neighbours' ethnicity appears for the union.

## Supersedes

None. It refines the peer-effect clause of
[2026-09-25-school-dilution-priced-beside](2026-09-25-school-dilution-priced-beside.md).

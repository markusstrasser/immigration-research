---
date: 2026-10-21
concepts: [social-pairing, business-crime, private-security, crime-senders, within-group-harm, world-ledger]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-10-16-main-case-v9.md
evidence: infra/immigration-fiscal/business_crime_2026_10_21/RESULT.md
---

# 2026-10-21: The pairing counts business crime at its net, prices commercial security against member victims, and sends crime from the completion and item 16 people: $483.1–557.3bn

## Context

The business-crime lane (`business_crime_2026_10_21`) priced the crime the victim row cannot see: retail
external and employee theft, non-retail business losses, violence against children under 12 outside the family,
violence at jails, and fraud against individuals. Gross, the lineage's offending costs residents outside it
$5.24 / 5.22bn a year at the case's two ends, about a third of murder on v9. Because the group's own purchases
also carry part of other offenders' theft, the with/without net is $1.40 / 1.38bn. The lane left the choice
between the two readings to the operator.

The within-group lane (`within_group_harm_2026_10_21`) raised three suspected holes in the pairing: the added
people carry no crime share, about $1.9bn of commercial security falls in no row, and the world ledger's in-group
victims use the September price and frame.

Operator, 2026-10-21 11:54 JST: "ok net then ..."

## Alternatives considered

1. **Net (with/without, pass-through).** What other residents lose when the group is removed: the losses its
   offending causes them, less the group's own payment, through prices, toward other offenders' losses. This is
   the rule the private-security row already uses. Chosen.
2. **Gross.** Harm the group's offending causes others, ignoring that removing the group also removes its share of
   paying for everyone else's offending. It answers "how much harm does the group cause", not "what does its
   presence cost others", and would mix the two questions inside one pairing. Kept beside.

## Decision

- **Business crime** enters the v9 pairing as the row `business_crime`, at the lane's net with the same v9 sender,
  payer and receiver terms as the other crime rows: **$1.377 / 1.355bn**. The gross, $5.24 / 5.22bn, is printed
  beside and never added.
- **Commercial security against member victims** enters as the row `commercial_security_member_victims`,
  **$1.904 / 1.955bn**. P7 scaled businesses' crime-driven security by the outside-victim share; a business guards
  against all offending and passes the cost to its customers, the same rule as the business row. The business
  lane counts losses only, so the row does not count anything twice.
- **Crime senders.** The coverage people (1.95M) are already inside the national incident counts. The completion
  reporters and item 16's minors are CPS Hispanics outside the union mask, so their offending was missing. Their
  located change aged 12+ (δ = 0.006973) now sends crime in every crime row: **+$0.266 / +0.302bn**.
- **World ledger.** Its live case replaces the in-group victimization rows ($20.11bn) with the within-group lane's
  row A victims ($28.91 / 32.20bn), never adding both. R1 moves from +$327.7 / 273.0bn to +$318.9 / 260.9bn.
- The within-group harm ($93.6 / 96.3bn) stays beside the pairing and is never added to it.

The pairing becomes **$483.1–557.3bn** (was $479.6–553.7bn), $10.8–12.4k per member of the 44.90M-person lineage;
counting benefits when paid, $399.5–473.7bn. The fiscal case does not change.

## Evidence

- `infra/immigration-fiscal/business_crime_2026_10_21/derived/summary.json` (`pairing`, overlap table in its RESULT);
  `sept24_propagation_2026_09_24/v9_totals.py` `crime_rows`; `derived/oct16/real_costs_totals.json`
  `v9_social_environment.current_social_rows`, `joint_social_stack`.
- P7: `social_costs_unpriced_2026_09_28/p7_crime.py` `response()` and `population_factor`; crime_victim_cost RESULT
  on how Hispanic-offender incidents are attributed by the CPS union share.
- `within_group_harm_2026_10_21/derived/rows.csv`; `world_ledger_2026_09_27/derived/readings_cash_oct16.csv`.
- Overlap: the victim row covers NCVS victims 12+ and WONDER homicides; business lines D and E cover victims under
  12 and at jails. Property crime covers NCVS household property; lines A–C cover business victims and F covers
  fraud, which the NCVS does not measure. Security rows are spending, not losses.

## Revisit if

- The 35% of shoplifting victimisations with no recorded offender can be attributed (line A's hard bounds run from
  $1.42bn to $4.65bn gross at the low end).
- A measured business security response to crime replaces P7's proportional rule.
- Fear is shown to fall with the commercial-security response (φ × Δ would leave about +$0.95bn of hole 2).

## Supersedes

None. Refines the v9 pairing's social rows; the fiscal case (v9) is unchanged.

## Addendum, 2026-10-21 (later)

The world ledger's others-side crime, property-crime, unreimbursed-care and congestion rows also moved from the winners
lane's September channels to the pairing's v9 rows at each end. Other US residents' line becomes −$340.6 / 401.1bn, and
R1 becomes +$285.0 / 284.3bn (after the in-group replacement above it was +$318.9 / 260.9bn).
[CALCULATION: `world_ledger_2026_09_27/derived/readings_cash_oct16.csv`]

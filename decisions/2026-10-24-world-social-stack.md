---
date: 2026-10-24
concepts: [world-ledger, social-pairing, pm25, world-gain]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-10-21-business-crime-in-pairing.md
evidence: infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md
---

# 2026-10-24: The world ledger's other US residents carry the whole paired social stack, PM2.5 included: R1 +$222.1 / 222.8bn

## Context

The world ledger sets the main case against the group living in Mexico. Its line for other US residents carried
the fiscal account plus only four of the pairing's social rows (crime victims, property crime, unreimbursed care,
congestion), the housing arrays and mobility. The rest of the stack, which the winners count includes, stayed
beside under the Phase B scope held fixed since October 15: PM2.5 (−$80.7bn on health and mortality alone), road
crashes, fear and security, business crime, school disruption, and the scale and variety gains. Other US residents
lost −$340.6 / 401.1bn in the world ledger against −$509.2bn in the winners count, and the world gain of
+$285.0 / 284.3bn omitted the largest priced harm outside the budget.

Operator, 2026-10-24: "ok add that".

## Alternatives considered

1. **Add the whole remaining stack, costs and gains.** The world line then carries the same social channels as the
   winners count. Chosen: the operator wants the full cost, and taking PM2.5 without the scale and variety gains
   would break the symmetry rule.
2. **Add PM2.5 only.** Lowers the world gain by about $77bn instead of $62bn, but counts one side of the stack.
   Rejected.
3. **Keep the Phase B scope.** Leaves the world line incomplete by the pairing's own rows. Rejected.

## Decision

For the live case `oct16`, `world_ledger.py` adds the stack's fourteen other `p7_social_*` rows from the pinned
winners `channels.csv` to other US residents (`SOCIAL_STACK_ROWS`), at the case's ends: −$62.86 / −61.51bn. Rows the
line already stands for are not repeated. Other US residents' line becomes −$403.5 / 462.6bn. At equal weights,
scope A, G3+ zero: R1 +$222.1 / 222.8bn (was +$285.0 / 284.3bn), R2 +$35.8 / 62.7bn, R3 +$108.1 / 116.6bn. R2 turns
negative at λ 1.16. The defensible R1 range becomes about $160–230bn; the output fall that would offset R1 is about
0.76% of GDP [THRESHOLD].

The remaining gap to the winners count's −$509.2bn central is the $83.6bn pension accrual, which a cash world sum
leaves out because the group receives what future payers pay, less item 11's stayers (+$11.0bn, a winners row) and
about $3.5bn of housing and mobility construction.

## Evidence

- `infra/immigration-fiscal/world_ledger_2026_09_27/derived/reading_rows_cash_oct16.csv` rows `social_*`;
  `derived/readings_cash_oct16.csv`, scope A_completed, public_pension_share 1, g3_bound zero.
- 243 lane tests pass; `rerun_lane.py … "sh {lane}/run_all.sh"`: IDENTICAL 294/294, exit 0.

## Revisit if

- The group's own air-quality change (Mexico's PM2.5 is higher than its US metros') is priced; it would raise the
  group's gain.
- Item 11's stayers are given a row in the world ledger.

## Supersedes

None; refines the world-ledger scope of decisions/2026-10-21-business-crime-in-pairing.md.

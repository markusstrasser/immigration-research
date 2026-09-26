---
date: 2026-09-26
concepts: [headline, service-response, finite-removal, consumption-taxes, cost-allocation]
status: adopted
supersedes: []
relations:
  - refines: decisions/2026-09-24-main-case-audit-and-outside-checks.md
  - applies: decisions/2026-09-25-weekly-audit-corrections.md
evidence: infra/immigration-fiscal/main_case_2026_09_26/RESULT.md
---

# 2026-09-26: The main case takes finite-removal responses and the corrected consumption key

## Context

Two proposals were pending against the adopted $200.9–246.3bn main case.

- **Finite removal** (ladder 227, `finite_response_2026_09_26`). The weekly conceptual audit asked
  whether a marginal elasticity can stand for the saving from removing a whole group. The main case
  used elasticities as responses: general government at 0.59–0.84, from cross-state scale
  elasticities, and schools at 0.63–0.66, from CBO's growth-rate coefficients. For a power-law cost,
  removing a share s saves r = [1 − (1 − s)^b] / s of average cost, which exceeds b. The group is
  12% of residents and 17.5% of pupils. The correction adds $4.1 / $3.4bn.
- **Consumption key** (ladder 225, `consumption_key_2026_09_24`). The key spent every dollar of
  resources, so it gave richer residents, who save more, too large a share of consumption taxes.
  Remittances pull the other way, by less. The correction subtracts $4.1bn.

The operator was asked: "Adopt the two pending main-case corrections (ladders 225 and 227)
together. Combined they leave the headline at $201–246bn." He answered "kk".

## Alternatives considered

1. **Adopt both in one engine run.** Chosen. Each lane's central specification goes in unchanged,
   and the gates reproduce both lanes' own runs.
2. **Adopt one.** Either alone moves the headline by about $4bn, up for finite removal and down for
   the key. The two are independent corrections of different lines, so adopting one would have to
   rest on a judgment that the other is wrong. Neither lane found that.
3. **Keep both beside the account.** The key's saving correction is backed by three outside checks
   (CBO's excise distribution, ITEP's gradient, CE's Mexican-origin units). Finite removal follows
   from the functional form the elasticities were estimated under. Leaving known biases outside
   the account would have mixed a better and a worse measurement.

## Decision

- **The main case is $200.9–245.7bn** (`main_case_2026_09_26`): +$0.04bn at the low end and −$0.62bn
  at the high end. It still rounds to $201–246bn.
- **The responses become data.** General government responds at 0.6000/0.8504 and schools at
  0.6522/0.6813; audit row 8's increment is scaled by 0.949. These are engine state, so
  `corrections.json` carries them in `meta.responses`, and every consumer sets them from there.
- **The consumption key's edits** are that lane's cells for `both_corridor_net_h2`, composed after
  the September 24 corrections.
- **The outer range is $164–277bn** (was $172–276bn). It adds the two corrections' own uncertainty:
  the removal's functional form (r = b under a fixed cost plus a constant marginal cost, −$4.1 /
  −3.4bn) and the consumption key's twelve specifications (−$4.4bn to +$1.5bn).
- **The sign break-even rises to 5.8–17.0%** (was 4.8–16.0%), because the key raises the group's
  taxes by $4.05bn.
- Every consumer of the September 24 case moves to this case in the same session: the explorer,
  the figures page, the back-cast, the debt legacy, the distribution, the uncertainty propagation,
  the real-costs totals, the generation account and the winners-and-losers ledger.

## Evidence

- `infra/immigration-fiscal/main_case_2026_09_26/RESULT.md`. The gates reproduce the September 24
  case and payload, each finite-removal run of that lane (I, F, G, H, J), the consumption key's
  twelve "both" specifications, and the two combined (run K).
- `infra/immigration-fiscal/finite_response_2026_09_26/RESULT.md` and
  `infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md`.

## Revisit if

- A measurement of cost over a large removal distinguishes a power law from a fixed cost plus a
  constant marginal cost.
- Banxico splits the US corridor by the sender's residence or nativity, or the Latino National
  Survey respondent file gives US-born sending amounts.
- A CE-to-PCE reconciliation by income sizes CE's shortfall at the top.

## Supersedes

None. It refines the September 24 decision: its package stands, and its responses and consumption
key change.

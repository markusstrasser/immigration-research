---
date: 2026-09-28
concepts: [social-benefits, evidence-symmetry, trade, volunteering, consumer-scale]
status: adopted
supersedes: []
relations:
  - extends: decisions/2026-09-28-social-items-scale-benefits.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/benefits_inventory_2026_09_28/RESULT.md
---

# 2026-09-28: Count volunteering, consumer-side scale and trade ties as benefits in the social total (adopted)

## Context

The operator asked for benefits to be counted and for more of them to be found: "count benefits ... if you can
think of more benefits it would be good ... looks a bit one sided now". Three lanes searched and priced what the
account did not yet carry. All figures are the absolute (with against without) central, as gains to other
residents.

| Lane | Item | Gain, $bn a year | Normalized (cost vs average residents) |
|---|---|---:|---:|
| [Benefits inventory](../infra/immigration-fiscal/benefits_inventory_2026_09_28/RESULT.md) | formal volunteering for people outside the group | 6.2 (4.5–7.9) | +4.2 |
| [Consumer scale](../infra/immigration-fiscal/consumer_scale_2026_09_28/RESULT.md) | network fixed costs, grocery variety and mix, cross-group media | 2.2 (−6.1 to 11.9) | +2.5 |
| [Trade networks](../infra/immigration-fiscal/trade_networks_2026_09_28/RESULT.md) | trade, visits and FDI created by ties with Mexico | 6.8 (1.1–23.7) | +0.8 |

The inventory found that the account already carries the large benefit channels: every tax, the long-run
production term, care, housing, and an implicit credit of about $271bn a year, because defense and existing
interest are never charged to the group. Capital owners' gain from more workers is zero in the adopted long run.

## Alternatives considered

1. **Keep all three beside the total**, as the inventory and trade lanes proposed. That would hold benefits to a
   stricter standard than costs. Fear entered the total on an assumed share φ; volunteering rests on an assumed
   outsider share, measured hours and a standard hourly value.
2. **Add all three at their absolute centrals and show the normalized figures beside them (adopted).**
3. **Also add the arms.** These are:
   - capital owners' gain with capital fixed (a $20.4bn gain, but a $50.9bn loss net of about 40% foreign
     ownership);
   - the corporate tax on foreign-owned capital serving the group's jobs ($0–21bn, retention unmeasured);
   - short-run electricity with the grid held fixed ($8.3bn).

   Each contradicts the account's long-run frame or rests on an unmeasured share, so all stay beside.

## Decision

Option 2, under the operator's instruction of 2026-09-28 to count benefits and find more.

- The three items join the social rows as negative costs from the September 27 case on. At the central values
  each enters at its central; in the full span, at its ends.
- Their normalized figures sit beside and are never added.
- `real_costs_totals.py` now orders each item's range by cost before stacking, and gates that the central lies
  inside it. The trade lane labels its arms by evidence: its "low" is the small gain.

## Consequences

**Totals.** The fiscal account is unchanged at $321.8–387.4bn.

| Measure | Before | After |
|---|---|---|
| Published pairing, central values | $462.6–537.2bn | **$447.5–522.0bn** ($10.9–12.8k per member) |
| Full span | $267.2–755.0bn | $223.7–755.4bn |

[2026-09-29: with road crashes charged with against without the group's traffic, the pairing is $416.2–490.7bn and
the full span $142.2–756.5bn ([decision](2026-09-29-crash-item-with-against-without.md)).]

The added social items net to $84.1bn at central values. The Sept 24 and schools-case outputs rerun
byte-identical. The winners lane changes only the totals it quotes.

## Evidence

- Lanes: e887023 (inventory), 8e15969 (consumer scale), 0d895f8 (trade); each reruns byte-identical.
- Totals: `sept24_propagation_2026_09_24/real_costs_totals.py --case sept27` →
  `sept27_propagation_2026_09_27/derived/real_costs_totals.csv`, `.json`.

## Revisit if

- The foreign share of US capital income, or the retention of corporate tax on relocated capital, is measured.
  Both decide whether the capital and corporate-tax arms can enter the total.
- A Mexico-specific estimate of trade created, rather than moved between states, replaces the stretched Gove (2017)
  elasticity.
- A measured outsider share of the group's volunteering replaces the assumed 0.4–0.7.

## Supersedes

None.

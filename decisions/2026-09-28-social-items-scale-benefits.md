---
date: 2026-09-28
concepts: [social-benefits, scale-spillovers, evidence-symmetry, quality-of-life]
status: adopted
supersedes: []
relations:
  - extends: decisions/2026-09-28-social-items-pollution-crashes.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md
---

# 2026-09-28: Count the benefits of scale in the social total beside its costs (adopted)

## Context

The total now counts PM2.5 and road crashes ([decision](2026-09-28-social-items-pollution-crashes.md)). With
them, it carries $128.5bn a year of costs that come mostly from population size: congestion ($13.0bn), PM2.5
($69.7bn) and crashes ($45.8bn). None of the matching benefits was in it, although the repo had priced two:

- **Scale lane (ladder 201).** Bigger cities raise other residents' earnings by $38.6bn ($32.3–45.0bn). The
  group's lower schooling takes back $24.9bn. Card, Rothstein and Yi's joint regression measures both on the same
  data and nets them to **+$13.9bn** (95% −$56.6bn to +$84.4bn), of which $6.0bn is induced tax receipts. It has
  been "proposed, not adopted" since September 23.
- **Restaurant market size (ladder 261).** A $6.8bn benefit ($1.1–19.2bn), which "belongs with the scale items".

Evidence-symmetry rule 5 asks that benefits be priced to the same standard as costs. The operator agreed:
"yes sure ... count benefits ... if you can think of more benefits it would be good ... looks a bit one sided now".

## Alternatives considered

1. **Keep the scale benefits beside the total.** The total would count what population size costs other
   residents and none of what it gives them.
2. **Add the scale lane's joint net and restaurant market size to the social rows (adopted).**
3. **Add only the pure size gain, +$38.6bn.** The removal frame must also count the schooling-mix part, which
   goes with the same people.
4. **Wait for the benefit lanes now running, and add everything at once.** The lanes are trade networks,
   consumer-side scale and a benefits inventory that includes capital owners' gains. Waiting would leave a
   known one-sidedness in the published total for no gain; each lane can join when it lands.

## Decision

Option 2, adopted by the operator on 2026-09-28.

- **The two items join the social rows as negative costs**, from the September 27 case on.
  - At the central values each item enters at its central, at both ends.
  - In the full span each enters at its lane's ends: the scale net's 95% interval and restaurants' grid.
- **Normalized figures, beside and never added:**
  - Scale: against as many average residents, the size part cancels and the schooling-mix part remains: a
    $24.9bn cost (−$43.1bn to +$93.0bn). This is read from the lane's composition row [INFERENCE].
  - Restaurants: a $1.2bn cost ($0.2–3.4bn).
- **The scale net enters the social rows whole, induced receipts included.** The fiscal main case is unchanged.
  Moving the $6.0bn of receipts into the fiscal account would take an engine run; that was ladder 201's
  original proposal.
- **Section 7b is unchanged.** Its social rows keep the cost items only, because its last column adds the scale
  net itself.

## Consequences

**Totals.** The fiscal account is unchanged at $321.8–387.4bn.

| Measure | Before | After |
|---|---|---|
| Published pairing, central values | $486.8–561.4bn | **$466.1–540.6bn** ($11.4–13.2k per member) |
| Full span | $373.3–707.2bn | $269.7–762.7bn |

The full span widens because the scale net's interval crosses zero widely.

**Added social items.** They net to $102.7bn at central values: $123.4bn of costs and $20.7bn of benefits
[CALCULATION: `sept24_propagation_2026_09_24/real_costs_totals.py --case sept27` →
`sept27_propagation_2026_09_27/derived/real_costs_totals.csv`, `.json`]. The Sept 24 and schools-case outputs
rerun byte-identical. The winners lane changes only the totals it quotes; neither item is allocated among other
residents.

**Against average residents**, the social items now read:
- PM2.5 −$46.5bn;
- crashes $0.0bn;
- the schooling-mix part of scale +$24.9bn;
- restaurants +$1.2bn.

**More benefits are being priced.** Three lanes are running:
- trade, investment and travel created by the group's networks (`trade_networks_2026_09_28`);
- consumer-side scale: variety-adjusted prices, network utilities and media variety (`consumer_scale_2026_09_28`);
- an inventory of every benefit channel against the account, led by capital owners' gain from more labour
  (`benefits_inventory_2026_09_28`).

## Evidence

- [Scale lane](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md), `derived/summary.csv`
  (joint grid and composition grid, CZ 1990).
  - Ladder 201 documents the design and the netting weight: m 0.609, whose SE of 0.156 would widen the net to
    −$212bn to +$240bn.
- [Disease and food lane](../infra/immigration-fiscal/disease_food_2026_09_28/RESULT.md), `derived/items.csv`
  (267b8e1), ladder 261.

## Revisit if

- The benefit lanes land. Each priced benefit joins or stays beside by the same rules as the costs.
- The scale net's netting weight or its design is re-estimated. Moretti and Iranzo–Peri's college-share
  estimates would make it a cost of $109–677bn; Ciccone–Peri's joint estimate a gain of $116–169bn.
- The account moves the scale net's induced receipts into the fiscal main case.

## Supersedes

None. It changes the scale net's status from "proposed, not adopted" (ladder 201; real-costs memo §7b) to
counted in the fiscal-plus-social total. It still sits outside the fiscal main case.

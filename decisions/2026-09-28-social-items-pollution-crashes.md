---
date: 2026-09-28
concepts: [social-costs, quality-of-life, air-pollution, road-crashes]
status: adopted
supersedes: []
relations:
  - extends: decisions/2026-09-28-social-items-fear-security-schools.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/air_pollution_2026_09_28/RESULT.md
---

# 2026-09-28: Add fine-particle pollution and road crashes to the social total, with per-head figures beside (adopted)

## Context

The operator asked for quality-of-life costs to be priced: "congestion and pollution in general ... QoL ... and
sickness ... and food quality". Three lanes did so, each reporting two figures: an absolute figure (the group
against its absence, the account's frame) and a normalized figure (the group against as many average
residents).

| Lane | Absolute, central (range), $bn | Normalized, $bn |
|---|---|---|
| [PM2.5 from the group's consumption](../infra/immigration-fiscal/air_pollution_2026_09_28/RESULT.md) (ladder 260) | 69.7 (31.5–122.5) | −46.5 |
| [Road crashes, charged by fault](../infra/immigration-fiscal/road_crash_externality_2026_09_28/RESULT.md) | 45.8 (26.3–80.9) | 0.0 |
| Road crashes, but-for (extra crashes the group's traffic adds) | 44.5 (5.7–145.1) | −2.6 |
| [Disease and food safety](../infra/immigration-fiscal/disease_food_2026_09_28/RESULT.md) (ladder 261) | 0.30 (0.01–1.8) | 0.22 |
| CO2, the share borne by US residents [FRAMING-SENSITIVE] | 12.0 (1.7–48.2) | −4.3 |

Ozone ($2.5bn) and the emissions of government services ($6.2bn) are speculative. Road congestion has been in
the social rows since September 23, on the same with-against-without frame.

## Alternatives considered

1. **Keep every quality-of-life item beside the account.** This leaves out harms the operator asked to have
   counted. It would also be inconsistent: congestion, a scale externality of the same kind, is already in
   the social rows.
2. **Add PM2.5 and crashes at their absolute figures and show the normalized figures beside them
   (recommended).** The account is built on removal throughout: its fiscal lines are with against without,
   not against average residents.
3. **Add the normalized figures instead.** The total would then carry only what is specific to the group and
   would fall by about $46.5bn. That mixes two frames in one total.
4. **Also add CO2, ozone, government-services emissions and disease/food.**
   - CO2 depends on an origin counterfactual and on the US share of global damage.
   - Ozone and government-services emissions are speculative.
   - Disease and food come to $0.3bn, most of it a food-safety arm that inspection data do not tie to
     outbreaks.

**Which crash row.** The crash lane gives two figures that are alternatives, never added together:
- the but-for row: outsiders' losses in the extra crashes the group's traffic causes;
- the fault-based row: outsiders' losses in crashes the group's drivers cause, net of their liability
  insurance.

The fault-based row is taken, for three reasons:
- the centrals agree ($45.8bn against $44.5bn);
- the fault-based row does not depend on the traffic-volume elasticity, the contested input that spreads the
  but-for from $5.7bn to $145.1bn;
- it matches how the account charges crime, where victims' harm follows offences the group's members commit.

The but-for row stays beside as the alternative.
[2026-09-29: reversed once the traffic elasticity was graded. The but-for is now the row in the total, and the
fault-based row sits beside ([decision](2026-09-29-crash-item-with-against-without.md)).]

## Decision

Option 2, adopted by the operator on 2026-09-28 ("ok add em"), on the recommendation to "add pollution ($70bn)
and crashes ($45bn) to the social rows, with the average-resident figures shown beside them". The crash band
shown to him was the fault-based $26–81bn.

- **PM2.5** (`pm25_consumption`, absolute) and **road crashes** (`road_crash_externality_fault_based`, absolute)
  join the social rows of the fiscal-plus-social total from the September 27 case on.
  - As with fear, security and schools, the central values carry each item's central at both ends.
  - The full span carries each item's low and high at its ends.
- **Beside, never added** (rows `social_item_*`, "normalized …, beside"):
  - the normalized figures: PM2.5 −$46.5bn (−$81.8 to −$17.9bn), crashes $0.0bn (−$18.6 to +$20.0bn);
  - the crash but-for row.
- **Out:** CO2, ozone, government-services emissions, EPA's value of a statistical life (an alternative
  valuation), and disease and food.
- Earlier cases keep their totals.

## Consequences

**Totals.** The fiscal account is unchanged at $321.8–387.4bn.

| Measure | Before | After |
|---|---|---|
| Published pairing, central values | $371.3–445.9bn | **$486.8–561.4bn** ($11.9–13.7k per member) |
| Full span | $315.6–503.8bn | $373.3–707.2bn |

The added social items now come to $123.4bn at central values ($48.4–233.6bn stacked); PM2.5 and crashes are
$115.5bn of that. The `sept27` totals were rerun, and the Sept 24 and schools-case outputs rerun byte-identical
[CALCULATION: `sept24_propagation_2026_09_24/real_costs_totals.py` →
`sept27_propagation_2026_09_27/derived/real_costs_totals.csv`, `.json`].

**Most of the two items is population scale.** Any 40.9m residents would impose a similar amount. Per head the
group is at or below average on both:
- pollution: −$46.5bn normalized, because the group consumes less;
- crashes: about zero normalized. The group drives 11% fewer miles per head. Its drivers' at-fault odds are 1.13
  times other drivers', and the two cancel.

A reader who wants only the group-specific part should read the normalized figures [FRAMING-SENSITIVE].

**The scale benefits are still out.** The total now carries $128.5bn of costs that come mostly from population
scale: congestion ($13.0bn), PM2.5 and crashes. None of the matching scale benefits is in the total:
- The scale lane (ladder 201) finds bigger cities raise other residents' earnings by $38.6bn ($32.3–45.0bn).
- Net of the group's lower schooling, that is +$13.9bn (95% interval −$56.6bn to +$84.4bn). It is proposed and
  not adopted.
- Restaurant market size is a benefit of $6.8bn ($1.1–19.2bn, ladder 261).

Evidence-symmetry rule 5 asks that benefits be priced to the same standard as costs. Adding both benefits would
lower the pairing by $20.7bn. That step is the operator's to take (see Revisit if).

[Later on 2026-09-28 the operator added both, and the pairing is $466.1–540.6bn
([decision](2026-09-28-social-items-scale-benefits.md)).]

**Winners and losers.** The rerun changes only the published totals the lane quotes. The two items are not
allocated among other residents. Their harm averages about $390 per other resident a year, spread across the
295.8m others by exposure. So the lane's 17.8% of other residents who come out ahead is somewhat overstated
[INFERENCE].

**The crash item's weakest input is under test.** The culpability odds ratio of 1.13 comes from drivers killed
in crashes (FARS). No non-fatal evidence on the group's involvement was used.
- The fault-based figure moves about $4bn per 0.1 of the odds ratio: $40.7bn at 1.00, $52.7bn at 1.30,
  $59.4bn at 1.47.
- Non-fatal crashes carry $29.7bn of the $45.8bn; fatal crashes $14.0bn; single-vehicle crashes $2.0bn.

[CALCULATION: the lane's `evaluate` at central inputs.] A lane measuring at-fault odds in California's crash
records (CCRS, 2022–24) is running.

## Evidence

- [Air-pollution lane](../infra/immigration-fiscal/air_pollution_2026_09_28/RESULT.md), `derived/items.csv`
  (b1f9ad5), rerun identical 8/8.
  - Primary checks by the lead: Bekbulat et al.'s 96,000 deaths in 2019; Tessum et al. 2019's
    inequity ratios; DOT's $13.7m VSL.
- [Road-crash lane](../infra/immigration-fiscal/road_crash_externality_2026_09_28/RESULT.md), `derived/items.csv`
  (5b6d859), rerun identical 9/9.
  - Primary checks by the lead: the lead reread the FARS 2023 killed-driver shares from the lane's
    derived JSON.
- [Disease and food lane](../infra/immigration-fiscal/disease_food_2026_09_28/RESULT.md) (267b8e1).
- Ladder 260–261 (7916392).

## Revisit if

- The operator adds the scale benefits, the scale lane's joint net and restaurant market size, as the
  counterpart of the scale costs now in the total.
- California's crash records give a non-fatal at-fault odds ratio for Hispanic drivers different from 1.13. The
  crash lane would then carry that ratio for non-fatal crashes.
  [2026-09-28 23:14: they did. CCRS 2022–24 gives 0.98 in injury and 1.15 in PDO crashes (m 1.00), and the crash lane
  now carries them for its non-fatal parts. The fault-based row is $42.3bn ($23.8–73.3bn; normalized −$3.4bn), and the
  pairing is $462.6–537.2bn with the scale benefits (`ccrs_nonfatal_involvement_2026_09_28`, 20755cb).]
- A measured traffic-volume elasticity narrows the but-for range enough to replace the fault-based row.
  [2026-09-28 23:51: graded evidence (`crash_volume_elasticity_2026_09_28`, f9fecd6) puts x near 0 for non-fatal and
  −0.21 for fatal crashes. The but-for is $11.1bn (−$57.7bn to +$74.3bn; cc2b092). Its range did not narrow, but its
  central no longer agrees with the fault-based row's, which was the first of the three reasons above. Switching the row is
  proposed to the operator (ladder 266). 2026-09-29: adopted ([decision](2026-09-29-crash-item-with-against-without.md)).]
- The account values deaths by life-years rather than one VSL at every age. PM2.5 would fall to about $26bn.
- The concentration–response evidence moves. Wu 2020 sets the low end and Di 2017 the high end.

## Supersedes

None. It extends [2026-09-28-social-items-fear-security-schools](2026-09-28-social-items-fear-security-schools.md).

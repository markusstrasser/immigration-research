---
date: 2026-09-29
concepts: [social-costs, road-crashes, counterfactual-frame]
status: adopted
supersedes: []
relations:
  - revises: decisions/2026-09-28-social-items-pollution-crashes.md
  - applies: decisions/2026-09-23-evidence-symmetry-rules.md
evidence: infra/immigration-fiscal/crash_volume_elasticity_2026_09_28/RESULT.md
---

# 2026-09-29: Charge road crashes with against without the group's traffic, not by fault (adopted)

## Context

On September 28 the social total took road crashes charged by fault: $42.3bn, the damage in crashes the group's
drivers cause, net of their liability insurance
([decision](2026-09-28-social-items-pollution-crashes.md)). That decision gave three reasons:
1. the lane's two rows agreed ($45.8bn by fault, $44.5bn but-for);
2. the fault-based row does not depend on the traffic elasticity x, which spread the but-for from $5.7bn to $145.1bn;
3. it matches how the account charges crime.

It named the event that would reopen it: a measured traffic elasticity.

The operator then asked how much a marginal driver adds to crashes, and whether the US is different. The traffic
elasticity lane graded the transferable evidence (`crash_volume_elasticity_2026_09_28`, f9fecd6; ladder 266). The
cost-weighted elasticity of the non-fatal crash rate to traffic is about +0.07 (bootstrap p10–p90 −0.23 to +0.52),
and of the fatal rate −0.21 (−1.55 to −0.16). The lane had taken 0.6 and 0. With these levels, and a composition
term for the group's higher fatal culpability, the but-for, other residents with against without the group's
traffic, is **$11.1bn** (−$57.7bn to +$74.3bn; cc2b092). The first reason no longer holds.

## Alternatives considered

1. **Keep the fault-based row.** It is robust to x. It answers a different question, though: who caused which
   crash, not how much better off other residents would be without the group. With crash risk per mile roughly
   flat in traffic, the crashes other residents have with the group's drivers would largely happen anyway without
   the group, as crashes among themselves on emptier, faster roads. The crime analogy fails at exactly this point:
   removing offenders does not make other people offend, but removing drivers leaves others' risk per mile about
   where it was.
2. **Take the but-for row, with the fault-based row beside (adopted).** It is the with-against-without comparison
   that every other fiscal and social line uses.
3. **Wait for a multi-vehicle elasticity.** The studies count all crashes, and car-to-car crashes may respond to
   traffic more than single-vehicle ones (CRSS by number of vehicles is untested). Each 0.1 of non-fatal x adds
   $5.4bn. No single study, dropped from the evidence, moves the but-for outside $0–22bn (before the $1.8bn
   composition term), far below $42.3bn. Waiting would leave a known overstatement in the published total.

## Decision

Option 2. The operator adopted it on 2026-09-29 ("ok do all you think are good") on the recommendation to "switch
the crash row in the total".
- `road_crash_externality` joins the social rows in place of `road_crash_externality_fault_based`, from the
  September 27 case on. At the central values it enters at its central, $11.05bn, at both ends. In the full span it
  enters at its grid ends, −$57.68bn and +$74.34bn.
- **Beside, never added:**
  - its normalized figure, +$0.62bn (−$24.1bn to +$31.5bn);
  - the fault-based row, $42.34bn ($23.80–73.25bn; normalized −$3.43bn).
- Earlier cases keep their totals. The Sept 24 and schools-case outputs rerun byte-identical.

## Consequences

The fiscal account is unchanged at $321.8–387.4bn.

| Measure | Before | After |
|---|---|---|
| Published pairing, central values | $447.5–522.0bn ($10.9–12.8k per member) | **$416.2–490.7bn** ($10.2–12.0k) |
| Full span | $223.7–755.4bn | $142.2–756.5bn |

The full span's low end falls most, because the but-for's evidence range crosses zero: in dense traffic, studies
disagree on whether extra traffic raises or lowers others' injury risk. The winners lane changes only the totals it
quotes. [CALCULATION: `sept24_propagation_2026_09_24/real_costs_totals.py --case sept27` →
`sept27_propagation_2026_09_27/derived/real_costs_totals.csv`, `.json`]

## Evidence

- Traffic elasticity lane (f9fecd6). The lead verified its key sources: Green, Heywood and Navarro; Edlin and
  Karaca-Mandic; Bauernschuster, Hener and Rainer; Tang and van Ommeren's abstract; ITF 2021; CE Delft; and the NYC
  AJE table. Reruns are identical 9/9.
- Crash lane revision (cc2b092). The composition term is derived in its RESULT; controls pass; reruns are identical 9/9.
- Ladder 266.

## Revisit if

- A multi-vehicle elasticity (CRSS 2019–2020 by number of vehicles, or a study of car-to-car crashes) comes in above
  the all-crash evidence. Each 0.1 of non-fatal x moves the item by $5.4bn.
- The account stops letting roads respond in the long run. With roads that respond, traffic density with and
  without the group is about the same, which keeps the but-for small whatever x is; on a fixed network x decides
  it. [INFERENCE]

## Supersedes

None. It revises the crash-row choice in
[2026-09-28-social-items-pollution-crashes](2026-09-28-social-items-pollution-crashes.md). PM2.5 and the rest of that
decision stand.

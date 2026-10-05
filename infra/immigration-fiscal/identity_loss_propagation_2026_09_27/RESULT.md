claude-opus-5-5

**Verdict:** [2026-09-28: two upstream corrections change the dollar figures below; the population counts do not move (§5). The lineage central is now −$1,288,162 (−$513,398 at 3%), because births need a living parent (audit §E). Row 2a now uses the measured generation split, under which losses after G3 keep the whole gap, so no schedule moves it: −$1,283,352 in every arm, +$4,810 (0.37%) on the central. The years convention, with its divisor corrected to the self-ID gap, is the sensitivity; there (b) raises the attrition effect from +$4,491 (0.35%) to +$8,784 (0.68%). In the population total under the split, the aggregate widens as the hidden share grows: −$292.7bn on (a), −$298.5bn on (b) and −$304.3bn on (c, ρ 0.5), at −$6,853, −$6,792 and −$6,735 per person. Entry 241 moves only by §E.] [2026-10-05: at C3 0.557 from the IPUMS-CPS basic monthly frame, row 2a is −$1,284,710, +$3,452 (0.27%) on the central, and still no schedule moves it. The population aggregate under the split is −$294.7bn on (a), −$300.7bn on (b) and −$306.6bn on (c, ρ 0.5), at −$6,901, −$6,842 and −$6,787 per person. (g3_identity_pooled_2026_10_05, monthly frame)] Identification that keeps falling after G3 moves the size of the Mexican-origin lineage. It barely moves its cost. The population total's arm 3 central rises from 42.78M to 44.02M if G4+ takes one more step (b), and to 45.25M if the loss compounds (c, with an assumed generation mix). The published "42–45M" becomes about 44–46M on (b) and 45–48M on (c). The hidden share of the third-plus rises from 11.2% to 17.5% (b) or 23.0% (c). The lineage cost's central (−$1,297,150; −$514,635 at 3%) and all its legalisation arms are unchanged to the cent, because they use the self-ID profile and never read the identification rate. Only arm 2a, the attrition-corrected mix, moves: its effect roughly doubles, from +$5,178 (0.40%) to +$10,126 (0.78%) on (b). Entry 241 does not move. [CALCULATION] Rates after G4 in (b)–(d) are [MODEL] extrapolations of a birth-stage loss (see Limits).

# Per-generation identity loss applied to lineage size and cost (2026-09-27)

Brief: [`BRIEF.md`](BRIEF.md). Source finding: `civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv`
(d75963b). Consumers: `mexican_origin_population_total_2026_09_19` (arm 3, `bounds_coverage_fiscal.py`)
and `lineage_cost_2026_09_19` (`inputs.attrition()` → `lineage.g3plus_profile`), both read-only.

## 1. Identification by generation

`r_g` is the cumulative share of generation g reported Mexican. The measured G3 rate is
p3 = 0.888111 (the lineage lane reads the rounded 0.8881). Per-step losses for children of
self-identified G3+ parents come from the three-couple-type rows: not reported Mexican 12.04%
(SE 0.86) and not reported Hispanic 9.01% (SE 0.82).

| Arm | Rule | G4 | G5 | G6 | G7 |
|---|---|---:|---:|---:|---:|
| (a) current | G4+ at the G3 rate | 0.888 | 0.888 | 0.888 | 0.888 |
| (b) one step | G4 = p3 × (1 − 0.1204), held for G5+ | 0.781 | 0.781 | 0.781 | 0.781 |
| (c) compound | × (1 − 0.1204) each generation | 0.781 | 0.687 | 0.604 | 0.532 |
| (d) compound, Hispanic | × (1 − 0.0901) each generation | 0.808 | 0.735 | 0.669 | 0.609 |
| (e) compound, calibrated | step × 0.740 = 8.90% | 0.809 | 0.737 | 0.671 | 0.612 |

Arm (e) is a disconfirmation arm not in the brief. The civic lane's equal-fertility synthetic puts the
G2-parent step at 15.13%, but the population lane directly measures the G3 loss at 11.19%. Arm (e) scales
the G3+ step by that ratio (0.740), reading the synthetic as overstated in the way the civic lane
suspects. It lands on (d). [CALCULATION, INFERENCE] `derived/schedules.csv`

## 2. Population total, arm 3

The population lane's `main()` runs unmodified, writing to `_cache/`. Its five outputs [2026-09-28: six,
with `arm5_generation_split.csv`] are byte-identical
to the lane's `derived/`. For each arm, the third bound row carries the arm's effective fourth-plus rate,
and the other bound rows are checked unchanged. The 4th-plus pool mixes G4, G5 and later generations
in unobserved proportions. Arms (c)–(e) therefore need a mix: true persons fall across G4, G5, … in
shares (1 − ρ)ρ^k. Central ρ = 0.5 means each later generation is half the size of the one before.
[ASSUMPTION] The case for ρ well below 1 is that Mexican immigration before 1910 was small next to
the 1910–1930 wave. [TRAINING-DATA] Flat arms (a) and (b) do not depend on ρ.

| Arm | ρ | 4th+ rate | Corrected union | × PES 1.0525 | Added | Hidden share of 3rd-plus | Per-person gap | Aggregate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (a) current | — | 0.888 | **42.78M** | 45.03M | +1.81M | 11.2% | −$6,864 | −$293.2bn |
| (b) one step | — | 0.781 | **44.02M** | 46.33M | +3.05M | 17.5% | −$6,711 | −$294.9bn |
| (c) compound | 0.25 | 0.751 | 44.43M | 46.76M | +3.46M | 19.4% | −$6,662 | −$295.5bn |
| (c) compound | 0.5 | 0.697 | **45.25M** | 47.63M | +4.28M | 23.0% | −$6,566 | −$296.7bn |
| (c) compound | 0.75 | 0.574 | 47.73M | 50.23M | +6.76M | 32.0% | −$6,299 | −$300.2bn |
| (d) compound, Hispanic | 0.5 | 0.741 | 44.57M | 46.91M | +3.60M | 20.0% | −$6,645 | −$295.7bn |
| (e) calibrated | 0.5 | 0.743 | 44.55M | 46.88M | +3.58M | 19.9% | −$6,648 | −$295.7bn |

The per-person gap and aggregate use the lane's arm 5 on the Duncan–Trejo selectivity row, where an
attriter's gap shrinks by the share of the education gap that their 0.76 extra years of schooling close. With more attriters, the per-person gap narrows and the
aggregate grows, because attriters still carry a negative balance. [CALCULATION]
`derived/population_arms.csv` [2026-09-28: the Duncan–Trejo row is now the years-convention sensitivity;
the measured generation split is in §5.]

Arm (c) at ρ = 0.5 (0.697) sits beside the lane's existing Duncan–Trejo 1994–2006 row (0.708, 45.08M).
That row was the top of the published range, and it now falls near the middle. Even so, (c) at ρ = 0.75
stays well under the 1970 reinterview bound (51.8M).

## 3. Lineage cost

[2026-09-28: this section's figures predate audit §E and the generation split; §5 has the current
ones.] Reproduced first: central −$1,297,150.363389 at 0% and −$514,635.245007 at 3%. Every stored row used
below reproduces to 1e-6. The lane's `lineage()` loop is copied into `propagate.py`, with the attriter
share looked up by generation. With a flat schedule, the copy equals the original bitwise on every row.

| Lineage row | Old | (b) | (c) | (d) | (e) |
|---|---:|---:|---:|---:|---:|
| Central, 0% | −$1,297,150 | same | same | same | same |
| Central, 3% | −$514,635 | same | same | same | same |
| 2b legalised year 10, 0% / 3% | −$1,272,572 / −$502,214 | same | same | same | same |
| Never legalised, statutory; statutory + priced 2026 | −$854,686; −$899,451 | same | same | same | same |
| **2a G4+ mixed profile, 0%** | −$1,291,973 | −$1,287,024 | −$1,286,857 | −$1,288,139 | −$1,288,185 |
| 2a, 3% | −$514,264 | −$513,910 | −$513,900 | −$513,991 | −$513,994 |
| 2a × 2b (mixed, legalised y10), 0% | −$1,267,394 | −$1,262,446 | −$1,262,279 | −$1,263,561 | −$1,263,607 |
| Supplementary: mix from G3, 0% | −$1,270,393 | −$1,265,445 | −$1,265,278 | −$1,266,560 | −$1,266,606 |

The central does not move. The rows the lane publishes (central, 3%, legalisation, senior rules) all
run `convergence = "selfid"`. On that path `g3plus_profile` returns the self-ID profile before reading
the attrition inputs. A NaN-poisoned attrition dict returns the identical central. The attrition effect
(2a minus central) goes from +$5,178 (0.40%) to +$10,126 (0.78%) on (b), +$10,293 (0.79%) on (c), and
+$9,011 / +$8,965 (0.69%) on (d) / (e). At 3% it goes from +$371 to +$641–735. The effect stays small
because inside the 100-year window G4 (born year 62) is 0.38 of a person and G5 (born year 91) lives nine
years. The G4+ blend is linear in the attriter share, and (b) equals the rescaled 2a effect to 1e-6.
Lineage persons (3.05) do not depend on identification. [CALCULATION] `derived/lineage_arms.csv`

The supplementary row is not in the brief. In the lane, 2a blends attriters only from G4, but the
lane's own premise puts 11.2% of G3 among attriters too. Starting the blend at G3 moves 2a by a further
+$21,580 on (a), which is larger than the identity-loss correction itself. It is still 2.1% of the central.

**Sponsored-parent lane (entry 241).** `lineage_sponsored_parents_2026_09_27/common.py` pins
`convergence: "selfid"` and `arms.py` never overrides it. Its arms therefore move by exactly 0, below
the brief's 0.1% re-run threshold, so they were not re-run. [2026-09-28: re-run after audit §E; every
arm moves by +$8,988 at 0% and +$1,237 at 3%, and the channels are unchanged in dollars.]

## 4. Published figures that move

[2026-09-28: the dollar rows below predate audit §E and the generation split; §5 lists what replaces them.
The population counts are unchanged.]

| Figure | Now | Becomes |
|---|---|---|
| Ladder 158 / population memo / INDEX line: "42–45M once attrition and coverage are added" | 42.78M central, 45.0M with PES | (b) 44.0–46.3M; (c, ρ 0.5) 45.3–47.6M; (d)/(e) 44.6–46.9M |
| Ladder 158: "+1.8M central" correction; memo headline "third generation 11%" | +1.81M; 11.2% hidden | +3.05M, 17.5% (b); +4.28M, 23.0% (c) |
| Ladder 158: per-person gap after attriters −$6,864; aggregate −$291–301bn | −$6,864; −$293.2bn on the central row | −$6,711, −$294.9bn (b); −$6,566, −$296.7bn (c) |
| Ladder 158: "+4.1M only at 1990s rates" | top of range | now inside the (c) range; no longer an outer bound |
| Ladder 159: "attrition 0.4%" | +$5,178 | 0.7–0.8% (+$8,965 to +$10,293) |
| Ladder 159 headline −$1.30M / −$515k, legalisation arms, 1.9%, $418k, $355–390k | — | unchanged |
| Ladder 241 | — | unchanged |
| Floor 41.8M (third-generation attriters only) | — | unchanged; it uses no fourth-plus rate |

The INDEX population row quotes −$7,152 → −$6,921 from an older ledger vintage. The lane's arm 5 as it
reproduces today gives −$7,105 → −$6,864, the memo's figures. The arms above shift that endpoint by
+$153 (b) and +$298 (c).

## 5. Update 2026-09-28: survival before reproduction and the generation split

Two upstream corrections: the lineage lane's births now need a parent alive at 29 (conceptual audit
2026-09-27 §E), and the population lane's arm 5 and the lineage lane's row 2a now use the measured
generation split ([carryover_identity_2026_09_27 §2](../carryover_identity_2026_09_27/RESULT.md)). Under
the split, hidden persons lost at the third-generation rate (11.19% of the corrected third-plus) keep
1 − C3 = 0.2242 of the self-identified gap (C3 0.7758, SE 0.6436), and persons lost later keep all of it.
The copy of `lineage()` here carries the §E change, and `verify.py` still finds it bitwise equal to the
lane's. Counts, unions and hidden shares do not change. [CALCULATION: `propagate.py`, `verify.py` PASS; two
reruns, the second byte-identical] [2026-10-05: C3 is now 0.5567 (SE 0.2457), the IPUMS-CPS basic monthly
frame 1994–2026 pooled with NLSY97, so G3-rate losses keep 0.4433. `propagate.py` finds the central split row
by its "(central)" label instead of by value. `verify.py` checks arm (a) against the population lane's published
split row and per person = aggregate / population after on every arm. PASS; the second rerun is identical,
10/10. (g3_identity_pooled_2026_10_05, monthly frame)]

**Population total, arm 5 values** (ρ 0.5 for the compounding arms):

| Arm | Added | Lost at G3 rate / later | Split: per person | Split: aggregate | Years convention (was the table's): per person / aggregate |
|---|---:|---:|---:|---:|---:|
| (a) current | 1.81M | 1.81M / 0 | −$6,853 | −$292.7bn | −$6,864 / −$293.2bn |
| (b) one step | 3.05M | 1.95M / 1.10M | −$6,792 | −$298.5bn | −$6,711 / −$294.9bn |
| (c) compound | 4.28M | 2.09M / 2.20M | −$6,735 | −$304.3bn | −$6,566 / −$296.7bn |
| (d) compound, Hispanic | 3.60M | 2.01M / 1.59M | −$6,766 | −$301.1bn | −$6,645 / −$295.7bn |
| (e) calibrated | 3.58M | 2.01M / 1.57M | −$6,767 | −$301.0bn | −$6,648 / −$295.7bn |

Under the split, more identity loss widens the aggregate by more, because every later loss carries the
identifiers' −$5,143. Across ρ, (c) runs from −$300.4bn (0.25) to −$315.9bn (0.75).
[CALCULATION: `derived/population_arms.csv`]
[2026-10-05: at the monthly-frame C3 the split columns read (a) −$6,901, −$294.7bn; (b) −$6,842, −$300.7bn;
(c) −$6,787, −$306.6bn; (d) −$6,817, −$303.3bn; (e) −$6,818, −$303.2bn. Across ρ, (c) runs from −$302.7bn to
−$318.6bn. Counts and the years-convention column do not move. (g3_identity_pooled_2026_10_05, monthly frame)]

**Lineage cost:**

| Lineage row | 2026-09-27 | Now (split; same under every schedule) | Years convention (a) / (b) / (c) / (d) / (e) |
|---|---:|---:|---:|
| Central, 0% / 3% | −$1,297,150 / −$514,635 | −$1,288,162 / −$513,398 | — |
| 2a G4+ mixed profile, 0% | −$1,291,973 | −$1,283,352 | −$1,283,671 / −$1,279,378 / −$1,279,236 / −$1,280,347 / −$1,280,387 |
| 2a, 3% | −$514,264 | −$513,054 | −$513,077 / −$512,769 / −$512,761 / −$512,840 / −$512,843 |
| 2b legalised year 10, 0% / 3% | −$1,272,572 / −$502,214 | −$1,263,584 / −$500,977 | — |
| Never legalised: statutory; + priced 2026 | −$854,686; −$899,451 | −$845,697; −$890,463 | — |
| 2a × 2b, 0% | −$1,267,394 | −$1,258,773 | — |
| Supplementary: mix from G3, 0% | −$1,270,393 | −$1,262,910 | — |

The attrition effect (2a minus central) is +$4,810 (0.37%) under the split in every arm. Under the years
convention it is +$4,491 (0.35%) on (a) and +$7,775 to +$8,926 (0.60–0.69%) on (b)–(e); at 3%, +$322 and
+$556 to +$638. Before these corrections the same effect ran from +$5,178 (0.40%) to +$10,126 (0.78%) on
(b). [CALCULATION: `derived/lineage_arms.csv`]
[2026-10-05: at the monthly-frame C3 the "Now" column reads 2a −$1,284,710 (0%) and −$513,151 (3%), 2a × 2b
−$1,260,132, and the supplementary mix from G3 −$1,270,041. The attrition effect is +$3,452 (0.27%) in every
arm. The central, 2b, never-legalised and years-convention figures do not move. (g3_identity_pooled_2026_10_05,
monthly frame)]

**Published figures, replacing §4's dollar rows.** Ladder 158's per-person gap after attriters is −$6,853
and the aggregate −$292.7bn on the central arm, −$291.5bn to −$335.1bn across the bounds (population lane
RESULT §5). Ladder 159's lineage is −$1.29M / −$513k, and its attrition row is 0.37%, with no identity-loss
schedule moving it. For ladder 241, every arm moves by §E only. [2026-10-05: −$6,901 and −$294.7bn on the
central arm and −$292.4bn to −$338.3bn across the bounds; ladder 159's attrition row is 0.27%.
(g3_identity_pooled_2026_10_05, monthly frame)]

## Limits

- (b)–(e) are [MODEL] extrapolations. They apply a *birth-stage* loss, measured on co-resident
  children as the household respondent reported it, to every later generation. They leave out
  switching after childhood in either direction. They inherit the civic lane's equal-fertility-per-couple
  assumption, which the lane itself suspects overstates the step (arm (e) is the correction).
- The 4th-plus generation mix (ρ) is unobserved. The population figures for (c)–(e) move more with ρ
  than with the choice between them.
- The lineage 2a effect assumes attriters keep about 20% of the self-ID gap (Duncan–Trejo selectivity via
  the population lane's arm 5). A different retained share scales every 2a delta proportionally.
  [2026-09-28: the 20% divided by the union's gap; against the self-ID gap the Duncan–Trejo share is 27.6%.
  Under the generation split, G3-rate losses keep 22.4% and later losses 100%, so the schedules no longer
  move 2a (§5).] [2026-10-05: 44.3% at the monthly-frame C3. (g3_identity_pooled_2026_10_05, monthly frame)]
- Resident stock and lineage accounting only; no admission counterfactual; no policy claim.
- [2026-09-28] The generation split rests on C3 = 0.78 (SE 0.64), pooled from 44–55 CPS adults and 11
  NLSY97 adults (`carryover_identity_2026_09_27` §4). At C3 0.907 (CPS 2022–26) the central aggregate is
  −$291.5bn. The rule that later losses keep the whole gap rests on one direct measurement, the
  co-resident one-step G4 adults (c −0.35 to −0.86 on BA+). [2026-10-05: C3 is now 0.557 (SE 0.246), from 526
  unique G3 non-identifiers at 25+ in the CPS basic monthly files 1994–2026 and the same 11 NLSY97 adults.
  (g3_identity_pooled_2026_10_05, monthly frame)]

## Reproduce

```sh
# from the repository root; ~1 min (the population arms reload the CPS extract)
uv run --no-project python3 infra/immigration-fiscal/identity_loss_propagation_2026_09_27/propagate.py
uv run --no-project python3 infra/immigration-fiscal/identity_loss_propagation_2026_09_27/verify.py   # PASS, rc 0
```

`propagate.py` stops with `[BLOCKED]` if either upstream central fails to reproduce. A second run leaves
`derived/` byte-identical (`diff -rq`, rc 0). Imports set `sys.dont_write_bytecode`, and no file in an
upstream lane was created or modified (`find -newer BRIEF.md` is empty). The lineage lane's recorded input
hashes still match.

| File | Contents |
|---|---|
| `derived/arms.csv` | arm, consumer, metric, old, new, delta (population at ρ 0.5, lineage rows, entry 241) |
| `derived/population_arms.csv` | every arm × ρ: rate, corrected third-plus, union, × PES, added, hidden shares, arm 5 gap; since 2026-09-28 also the split's counts (G3 rate, later) and its per-person and aggregate gap |
| `derived/lineage_arms.csv` | every arm × lineage row: old, new, delta, % of old, persons |
| `derived/schedules.csv` | r_g for G3–G8 by arm (population p3 and the lineage's rounded input) |
| `derived/audit.json` | losses, arm definitions, ρ, reproduction checks |

claude-opus-5-5

**Verdict:** Identification that keeps falling after G3 moves the size of the Mexican-origin lineage. It barely moves its cost. The population total's arm 3 central rises from 42.78M to 44.02M if G4+ takes one more step (b), and to 45.25M if the loss compounds (c, with an assumed generation mix). The published "42–45M" becomes about 44–46M on (b) and 45–48M on (c). The hidden share of the third-plus rises from 11.2% to 17.5% (b) or 23.0% (c). The lineage cost's central (−$1,297,150; −$514,635 at 3%) and all its legalisation arms are unchanged to the cent, because they use the self-ID profile and never read the identification rate. Only arm 2a, the attrition-corrected mix, moves: its effect roughly doubles, from +$5,178 (0.40%) to +$10,126 (0.78%) on (b). Entry 241 does not move. [CALCULATION] Rates after G4 in (b)–(d) are [MODEL] extrapolations of a birth-stage loss (see Limits).

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

The population lane's `main()` runs unmodified, writing to `_cache/`. Its five outputs are byte-identical
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
`derived/population_arms.csv`

Arm (c) at ρ = 0.5 (0.697) sits beside the lane's existing Duncan–Trejo 1994–2006 row (0.708, 45.08M).
That row was the top of the published range, and it now falls near the middle. Even so, (c) at ρ = 0.75
stays well under the 1970 reinterview bound (51.8M).

## 3. Lineage cost

Reproduced first: central −$1,297,150.363389 at 0% and −$514,635.245007 at 3%. Every stored row used
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
the brief's 0.1% re-run threshold, so they were not re-run.

## 4. Published figures that move

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

## Limits

- (b)–(e) are [MODEL] extrapolations. They apply a *birth-stage* loss, measured on co-resident
  children as the household respondent reported it, to every later generation. They leave out
  switching after childhood in either direction. They inherit the civic lane's equal-fertility-per-couple
  assumption, which the lane itself suspects overstates the step (arm (e) is the correction).
- The 4th-plus generation mix (ρ) is unobserved. The population figures for (c)–(e) move more with ρ
  than with the choice between them.
- The lineage 2a effect assumes attriters keep about 20% of the self-ID gap (Duncan–Trejo selectivity via
  the population lane's arm 5). A different retained share scales every 2a delta proportionally.
- Resident stock and lineage accounting only; no admission counterfactual; no policy claim.

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
| `derived/population_arms.csv` | every arm × ρ: rate, corrected third-plus, union, × PES, added, hidden shares, arm 5 gap |
| `derived/lineage_arms.csv` | every arm × lineage row: old, new, delta, % of old, persons |
| `derived/schedules.csv` | r_g for G3–G8 by arm (population p3 and the lineage's rounded input) |
| `derived/audit.json` | losses, arm definitions, ρ, reproduction checks |

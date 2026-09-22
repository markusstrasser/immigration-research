# Practitioner recut of the ledger arms grid — result

**Verdict:** On the pinned September 19 ledger, the conventions a budget modeler would run
put the Mexican-origin union's annual expanded balance between **−$290bn and −$190bn**
around the central **−$217bn**. The full switch design spans −$496bn to −$76bn over the 63
admissible cells and reaches +$41bn only with every congestible service free. Charging
defense, net interest and general government per capita is a second object: −$502bn to
−$402bn, central −$429bn. The range printed in the ledger's own RESULT.md (−$548bn to
−$87bn over 144 cells, central −$254bn) is the pre-repair September 17/18 build. None of
these hulls is a confidence interval; the replicate standard error of any cell is $8–10bn.

Object: `ledger_absolute_2026_09_17`, union of the three Mexican-origin target groups,
income-year 2024, household-shared allocation, D and P on, E zero in the central (inside
R750). Values are billions of 2024 dollars per year, costs negative.

## Named cells

| Cell | Definition | $bn | SE |
|---|---|---:|---:|
| Central | F 0, E 0, C 25/75, R central | −217.3 | 8.7 |
| Practitioner pessimistic, grid part | R all per capita, C all capital | −284.6 | 9.1 |
| **Practitioner pessimistic** | + enforcement targeted (netted), federal general government at the administration elasticity 0.824 | **−290.5** | 9.1 |
| Practitioner optimistic, functions only | G at cross-state function elasticities, K and D at the within-district school elasticity 0.836 | −203.6 | 8.6 |
| **Practitioner optimistic** | + state-local interest on general debt at zero, as item F treats federal interest | **−190.1** | 8.6 |
| Stretch: school m 0.63 on all dialled items | 0.63 on G, K, P, D and the per-capita part of R | −121.8 | 8.4 |
| Stretch: same plus 0.63 on base school current spending | base school is not on the dial; point only | −79.0 | — |
| Wishful corner | R all zero, C per capita (least negative grid cell) | −76.1 | 7.9 |
| No congestible services | m = 0, taxes and transfers only | +40.9 | 8.0 |
| Second object: public goods per capita on the central | F per capita | −429.0 | 9.6 |
| Second object: public goods by federal taxes paid | F proportional to federal tax | −335.8 | 6.9 |
| Second object: stacked corner | F per capita on the pessimistic grid cell (most negative grid cell) | −496.2 | 10.1 |
| Orientation: personal-source allocation | the same account, published | −239.2 | — |

[CALCULATION: `derived/named_cells.csv`; SEs from `replicates.npz`, 4/160 × Σ(rep − full)².]

## Hulls

| Hull | Low | Central | High | Members |
|---|---:|---:|---:|---|
| Practitioner | −290.5 | −217.3 | −190.1 | strict: R all per capita, C all capital, E targeted (netted), F general government at 0.824; lenient: G at cross-state elasticities, interest consistent across levels, K and D at 0.836 |
| Design grid | −496.2 | −217.3 | −76.1 | all 63 admissible F × E × C × R cells |
| Design grid plus dial | −496.2 | −217.3 | +40.9 | the grid and the marginality dial from 0 to 1 |
| Second object, public goods per capita | −502.1 | −429.0 | −401.8 | the practitioner hull with F per capita added |

## Switch moves against the central

| Switch | Δ $bn | SE | Side | In set | Who runs it |
|---|---:|---:|---|---|---|
| R all zero | +92.2 | 1.7 | lenient | no | nobody: zeroes veterans' cash, federal pensions and justice, which are records-based |
| R all per capita | −58.5 | 1.8 | strict | yes | average-cost budget shops spreading every non-entitlement federal function per head |
| R housing 604 by reported SPM subsidy | −0.4 | 0.8 | strict | yes | records-based refinement of the central |
| C 100% capital | −8.8 | 0.4 | strict | yes | the older incidence convention |
| C per capita | +49.0 | 1.2 | lenient | no | nobody: headcount is not an incidence theory |
| C borne by consumers (consumption proxy) | +27.1 | 1.0 | lenient | no | minority incidence view; disclosed |
| F per capita | −211.7 | 2.0 | strict | second object | average-cost public goods: defense −101.6, net interest −105.8, general government −4.2 |
| F proportional to federal taxes paid | −118.5 | 3.0 | strict | second object | benefit-principle variant |
| F general government at 0.824 | −3.5 | 0.03 | strict | yes | the measured-response arm; small here because state-local administration sits inside G |
| E stock, only with R all zero | −2.7 | 0.1 | strict | no | stacked on a zeroed justice function; the grid's own restriction |
| E stock plus border flow, only with R all zero | −5.3 | 0.1 | strict | no | same, with Border Patrol |
| E targeted with R central (netted) | −2.4 | 0.1 | strict | yes | the cell the admissibility rule removed, without the double count |
| G at cross-state function elasticities | +9.5 | 0.1 | lenient | yes | police 1.037, fire 1.085, highways 0.727, parks 0.948, libraries 0.974, administration 0.824; 72% of G held at 1 |
| G interest on general debt at zero | +13.5 | 0.1 | lenient | yes | consistency with item F's treatment of federal interest; interest is 8.1% of G |
| K and D at school elasticity 0.836 | +4.2 | 0.1 | lenient | yes | within-district, pupil-weighted |
| K and D at school elasticity 0.735 | +6.7 | 0.1 | lenient | no | within-district, unweighted; lower bound |

[CALCULATION: `derived/switch_moves.csv`; elasticities from
`scaling_test_2026_09_20/derived/state/estimates.csv` (year effects, all years) and
`derived/school_estimates.csv` (within district, state-year effects); G composition from
`derived/g_composition.csv`.]

## Gross flows behind the net

| Line | $bn |
|---|---:|
| Gross receipts | 417.0 |
| Gross outlays | −634.3 |
| Net | −217.3 |
| Replicate SE of the central | 8.7 |

[CALCULATION: `derived/gross_flows.csv`.]

## Gates

Nine, all passed on the published build (`derived/audit.json`): 63 grid cells and SEs
reproduced to 1e-6 $bn with no inadmissible rows; the 21-point curve and m\* = 0.158
reproduced; the central is the grid's central cell; the headcount-share carrier equals
the union's population over the resident population (0.12024); the F split reconciles to
the item's national dollars after TRICARE; G's gross and fee parts have the expected
signs; the gross flows sum to the central; the practitioner hull is ordered and negative;
every stretch and dropped cell sits above the lenient bound.

## Limits

Convention hulls, not confidence intervals. The cross-state elasticities are descriptive
size gradients held as sensitivities by the September 20 scaling decision. G's composition
is national. Base school current spending is off the dial. The personal-source allocation
is a different allocation of the same account, not a switch. Per-function responses on
the whole account belong to `full_account_2026_09_20`.

claude-opus-5[1m]

**Verdict:** Both gaps are closed and both new items push the same way. The district cost-to-serve differential (item D) is a **cost** for Mexican-origin pupils and a **receipt** for the white reference, because Hispanic pupils sit in districts spending $474 per pupil above their state's mean while white pupils sit $624 below it. Non-school state and local capital (item P) is close to a common per-capita charge and barely moves the gap. The union's complete absolute goes from **−$253.93bn to −$263.22bn**, and the complete common-age gap against third-plus non-Hispanic whites widens from **−$7,095 to −$7,224 per standardized person**. Switching both items off reproduces **−253.931979bn** to the dollar.

**One deviation from the brief, stated up front.** The brief's item P formula — total state and local capital outlay less elementary-and-secondary capital outlay — double-counts $239.5bn nationally, because item G already charges it. In the 2022 Census of Governments Table 1, lines 69 to 112 are the *functional* breakdown of line 66 direct general expenditure and each function's capital outlay sits **inside** its function total; line 67 is the same dollars cut by character, not an addition to them. Item G is line 66 less education, public welfare, hospitals, health and correction, so it already carries the capital of every function it keeps — highways, sewerage, parks, natural resources, solid waste and the rest. The briefed quantity is built and reported as the `briefed_gross` arm; the **central arm is `net_of_item_G`**, which charges only what nothing else charges. Both endpoints are given below.

[DATA: Census F-33 FY2024 district finance file (elsec24t.txt, 14,077 districts); NCES CCD LEA membership SY2023-24 (ccd_lea_052_2324_l_1a_073124.csv, 3,813,878 rows); 2022 Census of Governments state-local Table 1]
[INFERENCE: a differential is a composition effect across districts, not a cost of the pupil]
[UNVERIFIED: the capital split between items G and P is exact only for the functions that publish a capital sub-line]

## Files

- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/district_differential.py` (new)
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py` (items D and P, `--off`, `--out-dir`)
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/check_gates.py` (14 new gates)
- `derived/district_differential_by_state.csv` (new, 51 jurisdictions)
- `params/params.json` — new `district` group, 4 keys, all `status: verified`

## Part 1 — item D, district cost-to-serve differential

### Build

13,639 of the 14,077 F-33 districts matched the CCD on `NCESID` = `LEAID`. 395 were dropped for a missing per-pupil or membership value and 97 for a per-pupil value outside $3,000 to $80,000, leaving **13,147** districts. Per-pupil current spending is `TCURSPND * 1000 / ENROLL`; the CCD is long, so district totals come from `TOTAL_INDICATOR = "Derived - Education Unit Total minus Adult Education Count"` and the race groups from `"Derived - Subtotal by Race/Ethnicity and Sex minus Adult Education Count"` summed over `SEX`. CCD `White` is already non-Hispanic: the CCD race categories are mutually exclusive and `Hispanic/Latino` is its own.

### Coverage gate

The all-pupil enrolment-weighted mean over the F-33 state summary per-pupil figure runs **0.8715 to 1.0860** across 51 jurisdictions. **50 of 51 clear the 10% tolerance.** Vermont fails at 0.8715 and is charged a differential of zero.

Vermont's failure is structural, not a join error: its supervisory unions and technical centres report $431.4M of current spending against **zero enrolment**, so they carry no weight in any of the three means and the surviving level sits below the state summary. Michigan (0.9021) is the same shape through its intermediate districts. A unit with no pupils cannot bias a difference of pupil-weighted means, so the gate is a level test and Vermont's zeroing is conservative rather than necessary.

### Differentials, dollars per pupil

| state | all-pupil mean | Hispanic mean | white mean | Hispanic − all | white − all | coverage |
|---|---|---|---|---|---|---|
| California | 20,215 | 20,797 | 19,091 | **+582** | **−1,124** | 0.9723 |
| Texas | 12,815 | 13,158 | 12,423 | **+343** | **−392** | 0.9938 |
| Illinois | 21,560 | 22,778 | 19,978 | **+1,218** | **−1,582** | 0.9900 |
| Arizona | 12,222 | 12,253 | 11,733 | **+30** | **−490** | 1.0183 |

Nationally, pupil-weighted: Hispanic **+$473.8**, white **−$623.7**. Hispanic-minus-all is positive in 30 of 51 states; white-minus-all is positive in only 4. The largest positives are Massachusetts (+2,317), New York (+2,316), Rhode Island (+2,010) and Illinois (+1,218) — states where Hispanic enrolment concentrates in high-spending urban districts. The largest negative is Alaska (−3,273), where the highest-spending districts are remote and almost entirely Alaska Native.

### Item D by group

| group | $bn | per person | per pupil | se $bn | common-age gap vs white $/person |
|---|---|---|---|---|---|
| Mexico-born | −0.661 | −54 | −1,740 | 0.034 | **−123** |
| 2nd gen | −1.168 | −82 | −339 | 0.054 | **−115** |
| 3rd+ self-ID | −0.918 | −64 | −273 | 0.042 | **−102** |
| **union** | **−2.746** | **−67** | **−383** | 0.083 | **−115** |
| 3rd+ NH white | **+10.971** | +63 | +576 | 0.169 | 0 |
| all natives | +9.173 | +32 | +223 | 0.193 | −34 |

**The sign is a cost for every Mexican-origin group and a receipt for the white reference**, and D widens the union's common-age gap against whites by **$115 per standardized person**, which is almost exactly item K's contribution (−$116). Read the per-pupil column with care: the charge is allocated across the whole SPM unit, as every pupil-based item in this lane is, so a group's dollars over a group's own pupils is not the state differential. The Mexico-born figure of −$1,740 is that artefact — Mexico-born adults share SPM units with US-born pupils counted in the second-generation group. The union's +$576 per white pupil is the number that recovers the source: it matches the national pupil-weighted white-minus-all of −$624 once unit-sharing is allowed for.

The national sum of D is **+$8.5bn**, not zero, because only Hispanic and white pupils carry a rate and white pupils are the larger group. D is a redistribution around each state's own mean, not a level.

The all-native reference carries no separate rate. Its D total is nonzero only because the white reference and the third-plus self-identified Mexican-origin group are inside it; every record that is neither a target nor the white reference is charged zero.

## Part 2 — item P, non-school state and local capital

### The overlap with item G

2022 Census of Governments, Table 1, `2022_US_WY`, US total, dollars:

| line | quantity | $bn |
|---|---|---|
| 67 | direct general capital outlay, all functions | 371.256 |
| 74 | elementary and secondary capital outlay | 84.758 |
| 70 − 74, +82, +95 | education-beyond-school, hospitals and correction capital | **47.001** |
| 67 − 70 − 82 − 95 | capital already inside the item G residual | **239.497** |

The three add back to line 67 exactly, and that identity is now a gate. The briefed quantity, line 67 − line 74 = **$286.498bn**, contains the $239.497bn item G already charges.

### Overlap with item K

Item K prices school capital from the Census F-33 FY2024 district file at **$136.2bn** of capital outlay plus interest on school debt. The Census of Governments line 74 is **$84.8bn** of elementary and secondary capital outlay in 2022. These are not the same dollars: different year, different universe, and interest on school debt sits in Census of Governments line 110 rather than in line 67 at all. The national reconciliation now carries the two separately and says so on the line.

### Item P by group, central arm `net_of_item_G`

National target $47.001bn in 2022, $48.849bn after the 1.039312 state-local deflator; charged $49.249bn over the civilian household population, ratio **1.00820** against item G's 1.00943 and a population ratio of 0.99005.

| group | central `net_of_item_G` $bn | per person | briefed `briefed_gross` $bn | per person |
|---|---|---|---|---|
| Mexico-born | −1.910 | −156 | −10.843 | −887 |
| 2nd gen | −2.277 | −159 | −12.768 | −891 |
| 3rd+ self-ID | −2.359 | −165 | −12.957 | −903 |
| **union** | **−6.546** | **−160** | **−36.568** | **−894** |
| 3rd+ NH white | **−25.438** | **−147** | −155.124 | −896 |
| all natives | −41.793 | −147 | −253.641 | −894 |

P is nearly a common per-capita charge: it moves the union's common-age gap against whites by only **−$14** per standardized person, all of it state composition.

## The complete account after both items

### Union waterfall, central arms, $bn

| step | item | Mexico-born | 2nd gen | 3rd+ self-ID | union | union se |
|---|---|---|---|---|---|---|
| 0 | base | +6.63 | +10.69 | +32.92 | **+50.24** | 7.47 |
| 1 | G | −43.46 | −48.84 | −23.43 | −115.73 | 7.79 |
| 2 | K | −48.48 | −57.71 | −32.27 | −138.46 | 7.96 |
| 3 | **P** | −50.39 | −59.98 | −34.63 | **−145.01** | 7.98 |
| 4 | **D** | −51.05 | −61.15 | −35.55 | **−147.75** | 8.00 |
| 5 | U | −53.25 | −64.78 | −39.17 | −157.20 | 8.12 |
| 6 | I | −54.64 | −66.84 | −40.45 | −161.94 | 8.19 |
| 7 | M | −65.47 | −78.08 | −53.53 | −197.09 | 8.34 |
| 8 | N | −71.24 | −84.58 | −60.33 | −216.15 | 8.34 |
| 9 | E | −73.96 | −84.58 | −60.33 | −218.87 | 8.35 |
| 10 | C | −65.79 | −73.20 | −45.33 | −184.32 | 8.75 |
| 11 | X | −54.52 | −59.98 | −32.10 | −146.60 | 8.62 |
| 12 | R | −86.75 | −99.51 | −75.48 | −261.74 | 8.83 |
| 13 | F | −86.75 | −99.51 | −75.48 | −261.74 | 8.83 |
| 14 | S | −88.23 | −99.51 | −75.48 | **−263.22** | 8.85 |

The white reference ends at −$390.75bn and all natives at −$966.95bn.

### Headline movements

| quantity | before (D and P off) | after |
|---|---|---|
| union complete absolute | −253.931979bn | **−263.224141bn** |
| union complete common-age gap vs white, $/standardized person | −7,095 | **−7,224** (se 302) |
| union complete age-matched gap vs white, $bn | −354.3 | **−361.1** (se 12.0) |
| union complete common-age gap vs all natives | −4,928 | **−5,023** (se 257) |
| arms matrix range over 144 combinations | −548.37 to −87.04 | **−557.67 to −96.33** |
| break-even marginality dial m\* | 0.1204 | **0.1167** |
| national account position | −966.7bn | −1,007.4bn |
| national residual, unpriced or coverage | −1,624.1bn | −1,583.4bn |
| outlay coverage of the consolidated budget | 0.6296 | **0.6341** |

The arms matrix still never turns positive. The most negative corner is F per capita, E stock-plus-flow, C all-capital, R all-per-capita at −$557.67bn; the least negative is F zero, E zero, C per-capita, R all-zero at −$96.33bn.

Complete common-age gaps, all groups, $ per standardized person (se):

| group | vs 3rd+ NH white | vs all natives |
|---|---|---|
| Mexico-born | −7,783 (385) | −5,582 (352) |
| 2nd gen | −7,565 (617) | −5,364 (589) |
| 3rd+ self-ID | −6,270 (461) | −4,070 (445) |
| union | **−7,224 (302)** | **−5,023 (257)** |

## Off-switch reproduction

```
$ OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py \
    --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json \
    --off D --off P --out-dir <scratch>
...
   12    R -115.139252    -252.446798 8.784940                   cps_records
   13    F    0.000000    -252.446798 8.784940           central_arm_is_zero
   14    S   -1.485181    -253.931979 8.808802                   cps_records

arms matrix union absolute range: -548.37bn to -87.04bn over 144 combinations
break-even m* = 0.12044407952168636
items dropped for want of a verified parameter: ['P', 'D', 'S(states without a verified line)']
```

**−253.931979bn, exactly the prior step-13 endpoint**, together with the prior arms range of −548.37bn to −87.04bn. The off run writes to a scratch directory and never touches `derived/`.

## Runs

Both from the repository root, both exit 0.

```
$ ... absolute_ledger.py --params .../params/params.json ; echo $?
[capital] 2022 state-local direct general capital outlay $371.3bn: $84.8bn elementary and
secondary, $239.5bn already inside the item G general-services residual, $47.0bn unpriced
(briefed gross arm would charge $286.5bn)
[gate 0] reproduced +50.23821bn vs stored +50.23821bn, residual $0.00 -> PASS
[gap anchor] 8 upstream partial gaps reproduced
[national] account position -1,007.4bn vs consolidated -2,590.8bn, residual -1,583.4bn;
outlay coverage 0.634, receipt coverage 0.710
[district] coverage ratios 0.8715 to 1.0860 over 51 jurisdictions; 1 failed the 10% gate and
carry a zero differential ['Vermont'] -> PASS
[capital] item P charged 49.2bn of 48.8bn, ratio 1.00820 vs item G 1.00943 and population
ratio 0.99005 -> PASS
[sibling] general_services_per_person_vs_residual_agg_published_range: 3,904.78 -> PASS
[sibling] federal_public_goods_per_person_rebased_to_the_2023_denominator: 5,340.81 -> PASS
arms matrix union absolute range: -557.67bn to -96.33bn over 144 combinations
break-even m* = 0.11668838327241572
items dropped for want of a verified parameter: ['S(states without a verified line)']
PASS: 186 item rows, 90 waterfall rows, 144 arm combinations, 21 marginality points
BUILD_EXIT=0
```

```
$ ... check_gates.py ; echo $?
  PASS  national_total_reconciliation   G|nominal2022=1.0094; G|deflated2024=1.0094;
        K|central=0.9244; P|net_of_item_G=1.0082; P|briefed_gross=1.0101; E|stock=1.0000;
        C|wage25_capital75=0.9975; X|per_capita=0.9901; F|per_capita=0.9901
  PASS  item_D_district_differential_was_built                51 jurisdictions, coverage
        ratios 0.8715 to 1.0860
  PASS  item_D_every_state_clears_the_coverage_gate_or_carries_a_zero_differential
        1 failed the 10% gate and are zeroed: ['Vermont']
  PASS  item_D_covers_all_51_jurisdictions                    51 jurisdictions
  PASS  item_D_parameters_match_the_written_district_table    51 states agree to a tenth of a cent
  PASS  item_D_differential_signs_are_reported                Hispanic-minus-all positive in
        30 of 51 states, white-minus-all positive in 4
  PASS  item_D_is_in_the_items_table                          union -2.746bn
  PASS  item_P_capital_charge_was_built                       arm net_of_item_G
  PASS  item_P_reconciles_to_the_national_non_school_capital_total   charged 49.25bn of
        48.85bn, ratio 1.00820 vs population ratio 0.99005
  PASS  item_P_shares_item_G_per_capita_convention            P 1.00820 vs G 1.00943,
        difference -0.00124
  PASS  item_P_capital_split_is_exhaustive                    elementary and secondary 84.8bn
        + inside item G 239.5bn + item P 47.0bn = 371.3bn vs Census line 67 371.3bn
  PASS  item_P_parsed_capital_total_matches_census_line_67
  PASS  item_P_follows_item_K_in_the_waterfall                base G K P D U I M N E C X R F S
  PASS  items_D_and_P_are_on_the_marginality_dial             P True, D True
  PASS  no_item_was_switched_off_at_the_command_line          none
  PASS  brief_final_step_endpoint_still_reported              step 13 cumulative -261.74bn
  PASS  marginality_endpoint_matches_the_waterfall            m=1 gives -263.2241bn,
        waterfall ends at -263.2241bn

50/50 gates passed
GATES_EXIT=0
```

Every gate the lane already had still passes, including gate 0 to the dollar, the eight upstream partial-gap anchors, both sibling-lane cross-checks and the five ratio-inversion checks. 36 gates before, 50 now.

## What this does not settle

The capital split between items G and P is exact only for the functions the Census of Governments gives a capital sub-line: education, hospitals, highways, correction, natural resources, parks, sewerage and solid waste. About $79.8bn of 2022 capital outlay sits in functions with no sub-line — airports, ports, housing and community development, general public buildings, health, public welfare and the unallocable residual. Some of that belongs to functions item G excludes, so item P at $47.0bn is a lower bound on unpriced non-school capital and item G's implied $239.5bn is an upper bound on what it already carries. The briefed gross arm is the other end: it assumes item G carries no capital at all, which the table says is false.

The district differential is a composition fact about where pupils sit, measured on FY2024 finance against SY2023-24 membership. It is not evidence that a Hispanic pupil costs more to educate. It says the average Hispanic pupil attends a district that spends $474 per pupil above its state's mean while the average white pupil attends one $624 below it, and the ledger charges each group the spending it actually faces instead of the state average.

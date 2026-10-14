claude-opus-5-5

# Main case v7: v6 at the personal allocation, with child credits, the taxes on job capital and v6's two measured residuals

**Verdict:** Main case v7 is v6 plus five items: **$339.55–423.65bn** (339.552 / 423.649). The ends are specifications
16 / 11 in both methods, set and cash. Counting benefits when paid (the cash set), it is **$264.43–348.52bn**
(264.426 / 348.523). Per member of the 42.75M lineage that is **$7,942–9,909** (cash set $6,185–8,152). Against v6
($389.08–461.48bn) the set moves −49.531 / −37.831bn and the cash set −42.973 / −36.841bn. [CALCULATION: `main_case.cjs` →
`derived/summary.json` `v7`]

| $bn a year, low / high | Set | Cash set |
|---|---|---|
| v6 (ends 48 / 11) | 389.083 / 461.480 | 307.399 / 385.364 |
| 5. `personal_allocation`: the group total read at the personal allocation (the low end moves from 48 to 16) | +16.704 / 0 | +22.272 / 0 |
| 5b. `child_credits`: the child credits that cross the group's boundary in mixed tax units, the added people's included | +4.717 / +4.717 | +4.717 / +4.717 |
| 6. `job_capital_taxes`: the taxes on the business capital that serves the group's jobs | −71.771 / −43.367 | −71.771 / −43.366 |
| 7. `white_end_tax_keys`: the lineage members priced as third-plus whites, with their income taxes on the case's keys | +1.086 / +1.086 | +1.086 / +1.086 |
| 8. `row4_frame`: five v4 items on audit row 4's 39.71M instead of the CPS's published weights | −0.267 / −0.267 | +0.723 / +0.722 |
| the edit sets' interactions (six pairs) | 0 / 0 | 0 / 0 |
| **v7 − v6** | **−49.531 / −37.831** | **−42.973 / −36.841** |
| **v7** | **339.552 / 423.649** | **264.426 / 348.523** |
| per member of 42,752,213 | $7,942 / 9,909 | $6,185 / 8,152 |

[CALCULATION: `summary.json` `v7.change_by_item`, `v7.interactions`] The rows add to the printed totals, here and in every
table below; Approximations lists each controlled-rounding step.

Item 5 changes only the low end. v6's low end was specification 48, which uses the shared allocation. The group total
is the change for all other residents, so v7 reads it at the personal allocation alone, and the low end becomes
specification 16, v6's lowest personal one. v6 read this way is 405.786 / 461.480 (cash set 329.670 / 385.364). Items 5b–8
are cell shifts, and the band reads them at that allocation. Item 6 is v7's largest change: the corporate, business
property and other production taxes on the capital that works with the group now leave with it. Items 7 and 8 are the
two measured residuals v6 states beside its headline (ladder 298); v7 adds them to the case.

The case is **adopted** (2026-10-14, `decisions/2026-10-14-main-case-v7.md`): `package.cjs` STATUS is `adopted`,
both payloads carry `adopted: "2026-10-14"`, and `contract.cjs` lists no type change. All five gates pass on the
adopted build:
- G1: 128 gates in `main_case.cjs`;
- G2: the contract, with every v6 file, column, row and key in place;
- G3: with the new items off, v6's own `main_case.cjs`, `sign_reversal.cjs` and `lineage_addition.cjs` reproduce v6's
  10 derived files byte for byte;
- G4: 10 patterns, 120 checks, and 35 consumer gates recorded as needing code;
- G5: `rerun_lane.py` IDENTICAL: 26/26, exit 0.

The companion readings are rebuilt on v7 (section Companion readings):
- the count's arms a and c: $326.11–408.02bn and $352.99–439.27bn;
- C3 ± 1 SE: $335.65–427.38bn;
- the count by ancestry share: $225.95–342.35bn;
- the school low side: $310.52–397.08bn;
- the shared allocation: $307.81–394.89bn, or $7,200–9,237 per member.

The source lanes' files are read as delivered, and their hashes travel in the payloads:
- `mixed_unit_credits_2026_10_14/derived/item.json` (sha256 2773e34d4cb0…), through `sources.cjs`;
- `job_capital_taxes_2026_10_14/derived/item.json` (a9c747113ecf…), through `sources.cjs`;
- `white_replacement_2026_09_28/derived/limits_oct07.csv` (645102daac73…);
- `row4_class_2026_09_29/derived/row4_oct07_inputs.json` (0fe2a4673cb1…), its other inputs and its
  `row4_oct07.json`, the oracle.

No other lane was edited.

## The items

The registry is v6's four items, then five new ones (`package.cjs` REGISTRY, `NEW_IDS`):

| # | Item | Kind and edits | Source (reading) | Alone on v6, set | Alone on v6, cash set | In the cash set |
|---|---|---|---|---|---|---|
| 5 | `personal_allocation`: the group total at the personal allocation | allocation: the case's specifications are v6's personal ones (0–31 in v6's numbering); no edits (count 0); `meta.allocation` | the 2026-10-14 review, "For the operator" item 1 | 405.786 / 461.480 | 329.670 / 385.364 | yes |
| 5b | `child_credits`: credits non-member filers claim for member children, less member filers' credits for non-member children whose claim continues, with head-of-household status | edit set: 9 cell shifts on the personal cells, edits 769–777 (cash set 765–773) | `mixed_unit_credits_2026_10_14` (`R3_with_status`) | 389.083 / 466.197 | 307.399 / 390.081 | yes |
| 6 | `job_capital_taxes`: the taxes on the business capital that serves the group's jobs | edit set with responses: 32 cell shifts, edits 778–809 (cash set 774–805), and four `meta.responses` entries | `job_capital_taxes_2026_10_14` (central) | 309.828 / 418.113 | 228.145 / 341.997 | yes |
| 7 | `white_end_tax_keys`: W's income taxes on the case's own keys | edit set: 8 cell shifts, one receipt shift expanded to the eight incidence rules, edits 810–817 (cash set 806–813) | `white_replacement_2026_09_28` (`limits_oct07.csv`, arm `g3_rate_mix`), as `row4_oct07.cjs` prices it | 387.334 / 462.566 | 305.651 / 386.451 | yes |
| 8 | `row4_frame`: the owner property key, Part A accrual, the tax on benefits, the state price index and the OASDI ratio on row 4's frame | edit set: 30 cell shifts, edits 818–847 (cash set 20, edits 814–833) | `row4_class_2026_09_29` (`row4_oct07.cjs:108-231`, ported) | 388.808 / 461.212 | 308.122 / 386.086 | the owner key and the state index |

"Alone on v6" applies one item to v6. Item 5 alone is v6 at its 32 personal specifications. Items 5b–8 alone keep v6's
rule, the band over all 64 specifications, so their low end stays at specification 48 (checked on `per_spec.csv`):
there item 5b is 0, because the credits lane measured the personal cells only, and items 6–8 price the shared cells.
[CALCULATION: `summary.json` `v7.items` `alone_on_v6`]

**Item 5b**, from the credits lane's `item.json`, on the personal cells (the shared cells carry 0):
- the union: −$1.775bn of the group's `federal_income_tax` at the seven `federal_liability` scenarios
  and −$1.642bn at `federal_gap_high_agi`, plus +$2.524bn of `refundable_tax_credits` at its
  key `refundable_credits`. The lane's edits omit `federal_gap_high_agi`. The case puts the receipt shift there by its
  own rule for a shift at the reference rule (`V6.expand`: the group's target at that rule over the reference,
  0.925208 on `model.json` at the personal allocation) [APPROX];
- the added people: the lane's G3+ term, $213.97 per member, on the 1.957M added people the lineage
  prices as G3+ (the later losses and 1 − C3 of the G3-rate attriters). It is split across the two lines in G3+'s own
  receipt and spending proportions: +$0.419bn of net cost. The added people priced as whites take 0
  [ASSUMPTION: the lane did not measure them]. The switch is `LINEAGE` in `item_child_credits.cjs`, on.

Both lines respond at 1. The item's 9 edits carry 111 parts: `union_<G>:<lane part>[:<scenario>]` and
`lineage_g3plus:<line>[:<scenario>]`. Each edit's `by` is its parts' sum. At the end specifications:

| Part ($bn) | Change |
|---|---|
| A, forward (credits non-member filers claim for member children), receipt | +1.928 / +1.928 |
| A, forward, refundable spending | +2.754 / +2.754 |
| B, reverse (member filers' credits for non-member children whose claim continues), receipt | −0.454 / −0.454 |
| B, reverse, refundable spending | −0.230 / −0.230 |
| C, head-of-household status, forward | +0.317 / +0.317 |
| Cr, head-of-household status, reverse | −0.016 / −0.016 |
| the added people priced as G3+, receipt | +0.197 / +0.197 |
| the added people priced as G3+, refundable spending | +0.221 / +0.221 |
| **total** | **+4.717 / +4.717** |

By generation, the union's part is G1 −0.024 / −0.024, G2 +1.253 / +1.253 and G3+ +3.069 / +3.069, which is the lane's
`by_generation` (gated, 1e-9). The added people's part is +0.419 / +0.419. [CALCULATION: `summary.json`
`v7.change_by_item.child_credits`]

**Item 6** re-keys four receipt lines at every receipt scenario: `corporate_capital`, `corporate_labor`,
`remaining_production_property` and `other_production_taxes`. The group's amount on each becomes its job-capital amount,
and each line responds at the lane's response for the specification's reading:
- corporate tax leaves whole at the low reading and only its normal-return share at the high, 0.37 (the lane's
  `normal_return`, from Treasury OTA Technical Paper 5);
- business property tax responds at r_b 0.8806 and other production taxes at 1, at both readings;
- mining's cells carry no tax in the key, so its taxes stay at response 0: corporate 12.177, business
  property 21.072 and other production 28.463 ($bn of the national
  lines). The residential parts of documentary taxes and special assessments ($26.629bn) stay out of the other
  production key too.

The key does not depend on the incidence scenario, by construction: it keys where the capital is, not who bears the
tax. So every scenario takes the same key on its own cell totals, and with one response on both corporate lines the
group's corporate amount is the key times 663.685bn at all eight scenarios. This is the item's rule,
not an approximation.

In v6 the four lines respond at 0, the engine's default for indirect receipts, so the item's change is minus each
line's response times its whole new amount. On the payload model at the reference scenario (personal / shared):

| Lane line | National, $bn | Response | Key share | The group's amount before | After |
|---|---|---|---|---|---|
| corporate (`corporate_capital`, `corporate_labor`) | 663.685 | 1 low / 0.37 high | 6.27% / 6.92% | 28.093 / 32.641 | 45.086 / 50.308 |
| business property (`remaining_production_property`) | 273.445 | 0.8806 | 7.35% / 7.88% | 8.049 / 9.903 | 21.556 / 23.383 |
| other production taxes (`other_production_taxes`) | 145.258 | 1 | 4.94% / 5.30% | 4.276 / 5.261 | 7.701 / 8.354 |

"After" includes the 3.04M added people. Their amounts are their share of the case's wage key (G3+-priced
0.318%, white-priced 0.270% at personal) times the lane's G3plus and white_nh factors times each line's
national. [CALCULATION: `corrections.json` `meta.job_capital_taxes`] The change at the end specifications:

| Part ($bn) | Change |
|---|---|
| union G1 | −21.813 / −13.488 |
| union G2 | −22.483 / −13.471 |
| union G3+ | −22.186 / −13.306 |
| added people priced as G3+ members | −2.599 / −1.559 |
| added people priced as whites | −2.690 / −1.543 |
| **total** | **−71.771 / −43.367** |

By line: corporate −45.086 / −16.682, business property −18.984 / −18.984, other production taxes
−7.701 / −7.701. The union's part is −66.481 / −40.265 and the added people's −5.290 / −3.102.
[CALCULATION: `summary.json` `v7.change_by_item.job_capital_taxes`] The production module's capital-tax term stays 0
at every case specification, so nothing counts twice (gated).

**Item 7** re-keys the income taxes of W, the lineage members the case prices as third-plus non-Hispanic whites: C3
× the G3-rate attriters, 1,082,721 people (`meta.lineage.members.white`). v6 prices their income taxes on the white
lane's keys, and item 7 moves them to the case's own keys. The white lane measured the move (`limits_oct07.csv`, arm
`g3_rate_mix`, read and not recomputed). It is +1.086bn at the personal allocation (+$1,003 per
person) and −1.748bn at the shared (−$1,615), the same at both ends and in both bases (accrual for
the set, cash for the cash set).

The item is a receipt shift of minus the move on the group's `federal_income_tax`, which responds at 1. The case's
rule expands it to every incidence rule, as the row-4 class lane prices it (`row4_oct07.cjs:232-234`). That gives 8
edits, with parts `lineage_whites:income_tax_keys:federal_income_tax:<scenario>`. At v7's ends, both personal, it adds
+1.086bn, set and cash. Alone on v6 it gives the row-4 lane's `white` row at that lane's specifications 48 /
11, −1.748 / +1.086 (gated, 1e-9, set and cash). [CALCULATION: `corrections.json` `meta.white_end_tax_keys`]

**Item 8** reprices five v4 items that summed the CPS's published weights where the account prices audit row 4's
39.71M (`row4_class_2026_09_29/RESULT.md`). The row-4 class lane priced them on v6 (`row4_oct07.cjs`). The item ports
that construction (`:108-231`) and reads the lane's inputs, gated equal to the values the lane recorded:
`derived/row4_oct07_inputs.json`, `row4_state_index.json` and `price_rekeys.json`, with kappa from
`main_case_decomposition_2026_09_29/derived/summary_sept29.json`. Each component has a union rule and a rule for the
added people:

| v4 item | The union (39.71M) | The added people (G: priced as G3+; W: priced as whites) | Cash set |
|---|---|---|---|
| owner property key | `owner`: the owner-occupied property cell at the reference rule times (1/kappa − 1) | `owner_national_key`: G's owner cell times the national key's change on row 4 | yes |
| Part A accrual | `part_a`: Part A accrual at row 4 less at published weights, on the Trustees arm | `part_a_split`: G's Part A × f_pa × the generation split's G3+ change in Part A | no |
| the tax on benefits | `benefit_tax`: the group's tax on benefits at published less row-4 weights, on `federal_income_tax` | `benefit_tax`: G's × (the national key's ratio − 1), W's × (the white lane's rule-3 ratio − 1) | no |
| state price index | `state_index`: the three state-price lines × (the row-4 index ratio − 1); general sales and licences by the factor's change | `state_index`: G's cells, by the same rule | yes |
| OASDI ratio | `oasdi_ratio`: (ratio_net at row 4 less at published) × the union's OASDI receipts | `ss_split`: G's Social Security × f_ss at row 4 × the split's G3+ change; `ss_factor`: G's and W's × the change in f_ss | no |

Part A, the tax on benefits and the OASDI ratio touch the pension switch, so they enter the set only. The set has 30
edits with 130 parts, and the cash set 20 with 80. Receipts expand over the incidence rules by
the case's rule, as the lane does. The change at the end specifications, set:

| v4 item ($bn) | The union | The added people |
|---|---|---|
| owner property key | +0.341 / +0.341 | −0.001 / −0.001 |
| Part A accrual | −1.028 / −1.028 | −0.045 / −0.045 |
| the tax on benefits | −0.028 / −0.028 | −0.002 / −0.002 |
| state price index | +0.365 / +0.364 | +0.016 / +0.017 |
| OASDI ratio | +0.123 / +0.123 | −0.008 / −0.008 |
| **total** | **−0.227 / −0.228** | **−0.040 / −0.039** |

The item's set change is −0.267 / −0.267. In the cash set the owner key and the state index give +0.723 / +0.722
(union +0.707 / +0.706, added people +0.016 / +0.016). The union's part by generation is G1 +0.260 / +0.259, G2 −0.294 / −0.294
and G3+ −0.193 / −0.193. [CALCULATION: `summary.json` `v7.change_by_item.row4_frame`] Alone on v6 the item is the row-4
lane's `row4_class` row at 48 / 11: −0.275 / −0.267 (cash set +0.722 / +0.722). Its union parts are the lane's
`union_joint` (−0.218 / −0.228) and its added people's parts `lineage_joint` (−0.057 / −0.040); each is
gated at 1e-9, set and cash.

The lane prices the union whole, so the generation tags follow a rule. `owner` and `state_index` sit on each
generation's own cells of the September 29 generation models; they add to the union's (gated). `part_a`,
`oasdi_ratio` and `benefit_tax` go by the generation split's pension shares (`generation_account_2026_09_24/v4_split.cjs:300-313`),
the rule the case's split already applies to item pension_tr2026's union parts: a generation's change is its row-4
share of the row-4 total less its published share of the published total. Each edit's union parts add to the lane's
union formula (1e-9). The alternative tags the reruns' own groups. Row 4 reweights only Mexico-born people, so it would
put the whole of `part_a` (−1.028) on G1. The tags move no total, only the split by generation.

## Items jointly

The decomposition in the Verdict is exact. v7 − v6 is the sum of four terms:
- item 5's move of the ends: v6 at its 32 personal specifications less v6 at all 64;
- each edit set alone on v6 at v7's end specifications;
- the edit sets' interactions, all six pairs run, which are zero (at most 5e−13bn at any specification): at fixed
  responses the cost is linear in the cells the items shift, and item 6 re-keys lines no other item edits;
- the move of the ends beyond item 5, 0 / 0.

At every specification the case moves from v6 by −66.234 / −37.830 across the personal specifications and
−81.277 / −49.584 across the shared ones. The cash set moves by −65.245 / −36.841 and −80.280 / −48.587.
[CALCULATION: `summary.json` `v7.change_at_every_specification`]

The rest of v6's figures move with the case. v6 is read at its own ends, v7 at its own:

| Row ($bn, low / high) | v6 | v7 |
|---|---|---|
| without the capital return | 352.50 / 400.42 | 302.44 / 362.58 |
| general government at 0 | 356.38 / 413.59 | 306.85 / 375.76 |
| option A (beside) | 372.32 / 438.65 | 322.79 / 400.82 |
| 7% capital return (beside) | 480.54 / 542.90 | 432.34 / 505.07 |
| school low side, within-district (0.8489) | 361.26 / 434.91 | 310.52 / 397.08 |
| school low side, within-district as the response (0.836) | 358.82 / 432.72 | 307.98 / 394.88 |
| K-12 capital at the pupil share | 388.91 / 460.53 | 338.92 / 422.70 |
| range | 311.89–515.60 (quadrature 353.57–483.99) | 262.26–477.73 (quadrature 303.10–446.16) |
| the frozen-services welfare (CBO preferred), both allocations | −83.64 / 27.52 | −45.40 / 109.20 |
| the frozen-services welfare (CBO preferred), personal allocation | −83.64 / 18.12 | −45.40 / 84.76 |
| the personal break-even (`sign_reversal.csv`) | −9.05% / −0.66% | −0.32% / 15.01% |
| the shared break-even | −7.03% / 1.58% | 4.58% / 21.12% |

[DATA: `main_case_bands.csv` of both lanes; `sign_reversal.csv` (the oct07 and oct14 columns; its `allocation` and
`in_band` columns mark the case's rows); `summary.json` `range`]

## Arms

Each arm row in `main_case_bands.csv` is the whole v7 case with one item at the arm
(`caseOf(OCT05, CANDIDATE, {item: arm})`). Its payload, applied by consumer.cjs, gives the row's band, with ends 16 / 11
in both methods (gated). v6's arms are rebuilt on v7 beside their v6 rows. The new items' arms come from the source
lanes' own arms: the credit readings, and each job-capital arm with one input changed. Items 7 and 8 have none. At
`pension_tr2026_combined_funds`, item 8's OASDI components scale with the arm's level (Approximations).

| Arm row | Set | From the case | Cash set | v6's row |
|---|---|---|---|---|
| `pension_tr2026_combined_funds` (the same 2026 inputs on the Trustees' combined OASDI funds, the convention of SSA's money's-worth notes and the Trustees' headline, which assumes a law moving funds between OASI and DI) | 340.593 / 424.691 | +1.041 / +1.041 | 264.426 / 348.523 | 390.203 / 462.520 |
| `retiree_health_mu_low` (mu low: all state-local OPEB over state plans 1.326 (CRR SLP 48 over Pew's 2016 gap)) | 339.175 / 423.263 | −0.377 / −0.386 | 264.049 / 348.137 | 388.716 / 461.094 |
| `retiree_health_mu_high` (mu high: 2.300, symmetric about the central 1.813 [ASSUMPTION]) | 339.929 / 424.035 | +0.377 / +0.386 | 264.802 / 348.909 | 389.449 / 461.866 |
| `retiree_health_rho_one` (rho = 1: state-local GASB 75 normal cost equal to employer contributions (accrual equals pay-go)) | 338.149 / 422.211 | −1.403 / −1.438 | 263.023 / 347.085 | 387.719 / 460.042 |
| `retiree_health_rho_high` (rho high: 1.506, the federal military plan's normal cost over benefits paid) | 341.707 / 425.858 | +2.155 / +2.209 | 266.580 / 350.732 | 391.177 / 463.689 |
| `retiree_health_military_low` (military retirees' civilian-provider care at MERHCF's purchased care only, $9.7bn) | 340.008 / 424.106 | +0.456 / +0.456 | 264.882 / 348.979 | 389.578 / 461.936 |
| `retiree_health_military_high` (military retirees' civilian-provider care with all pre-65 care, $22.4bn) | 339.434 / 423.532 | −0.118 / −0.118 | 264.308 / 348.405 | 388.955 / 461.362 |
| `retiree_health_no_federal` (state and local only: the federal civilian swap and the military care left in place) | 340.256 / 424.322 | +0.704 / +0.672 | 265.129 / 349.195 | 389.862 / 462.152 |
| `added_age_mix_cohort_at_birth` (the cohort reading: each band at the child-stage loss rate of the cohorts born in it (the report at birth persists), which the within-cohort table does not support) | 327.831 / 412.869 | −11.721 / −10.780 | 253.559 / 338.597 | 383.514 / 452.025 |
| `added_age_mix_rough_keys` (the central mix on the rough-key route: every cell of a line times the white lane's rough re-key factor for the line (band_lines.py), which gives one age profile to both allocations) | 339.464 / 423.485 | −0.088 / −0.164 | 264.293 / 348.314 | 390.132 / 461.315 |
| `child_credits_R1_with_status` (the lane's reading R1_with_status (3.184bn on the union)) | 338.400 / 422.497 | −1.152 / −1.152 | 263.273 / 347.370 | — |
| `child_credits_R2_with_status` (the lane's reading R2_with_status (4.405bn on the union)) | 339.667 / 423.764 | +0.115 / +0.115 | 264.540 / 348.638 | — |
| `child_credits_R3_without_status` (the lane's reading R3_without_status (3.998bn on the union)) | 339.220 / 423.317 | −0.332 / −0.332 | 264.094 / 348.191 | — |
| `job_capital_taxes_mining_as_other_industries` (mining's three taxes respond as other industries' do (the build before 2026-10-14)) | 331.676 / 416.796 | −7.876 / −6.853 | 256.550 / 341.670 | — |
| `job_capital_taxes_normal_return_share` (corporate at TP-5's normal-return share (0.37) at both readings) | 367.956 / 423.649 | +28.404 / 0 | 292.830 / 348.523 | — |
| `job_capital_taxes_normal_return_share_0_25` (the high reading's corporate response at Power and Frerick's 2003-2013 normal-return share (Treasury OTA Working Paper 111, abstract)) | 339.552 / 429.060 | 0 / +5.410 | 264.426 / 353.933 | — |
| `job_capital_taxes_normal_return_share_by_industry` (the high reading's corporate response at each industry's normal-return share (Power and Frerick Table 1, 2011-2013), as the union's personal effective share) | 339.552 / 427.138 | 0 / +3.489 | 264.426 / 352.012 | — |
| `job_capital_taxes_plain_wage_share` (the plain wage share in place of the industry key: every line's base at each group's share of all CPS wages on this lane's frame) | 329.753 / 420.179 | −9.799 / −3.470 | 254.626 / 345.053 | — |
| `job_capital_taxes_foreign_source_removed` (federal tax on foreign-source corporate income removed from the corporate base (IRS SOI TY2021)) | 343.327 / 425.046 | +3.775 / +1.397 | 268.200 / 349.919 | — |
| `job_capital_taxes_business_land_at_0` (business land at response 0: the land part of business property tax stays) | 341.163 / 425.261 | +1.611 / +1.611 | 266.037 / 350.134 | — |
| `job_capital_taxes_business_land_at_1` (business land at response 1: the whole business property tax leaves) | 336.979 / 421.076 | −2.573 / −2.573 | 261.853 / 345.950 | — |
| `job_capital_taxes_floor` (the floor: CBO's labour share of corporate tax only, at the case's wage key; the other lines at response 0) | 397.881 / 453.574 | +58.329 / +29.925 | 322.755 / 378.448 | — |
| `job_capital_taxes_case_wage_key` (the case's wage key (the status rules at the on-books lane's shares) in place of all CPS wages: each generation's targets times its share of the case's wage key over its plain share on this lane's frame) | 342.824 / 425.682 | +3.272 / +2.033 | 267.698 / 350.555 | — |

[CALCULATION: `summary.json` `v7.arms`]

## Companion readings

The record quotes five readings beside v6's case. Each is rebuilt on v7 as a whole-case row in `main_case_bands.csv`,
with a cash row wherever v6 has one. v7 adds a sixth, the shared allocation: the reading for distribution inside the
group and for comparisons between groups, where both sides share alike. `summary.json` `v7.companions` holds the
detail, and none is left unbuilt.

| Reading ($bn, low / high) | v6 | v7, set | v7, cash set | v7 per member, set |
|---|---|---|---|---|
| the count's arm a: the fourth-plus generation lost at the third generation's rate, no later losses (1.81M added) (`lineage_arm_a`; ends 16 / 11) | 378.000 / 445.254 | 326.110 / 408.019 | 252.933 / 334.842 | $7,854 / 9,827 (41.52M) |
| the count's arm c: losses compounding at rho 0.5 past the third generation (4.27M added) (`lineage_arm_c`; ends 16 / 11) | 400.158 / 477.698 | 352.987 / 439.272 | 275.911 / 362.196 | $8,025 / 9,987 (43.98M) |
| C3 one standard error below the central, 0.5567 - 0.2457, at arm b's counts (`lineage_c3_minus_se`; ends 16 / 11) | 391.912 / 465.373 | 343.449 / 427.379 | 268.379 / 352.309 | $8,033 / 9,997 (42.75M) |
| C3 one standard error above the central, 0.5567 + 0.2457, at arm b's counts (`lineage_c3_plus_se`; ends 16 / 11) | 386.253 / 457.586 | 335.655 / 419.919 | 260.472 / 344.736 | $7,851 / 9,822 (42.75M) |
| C3 ± 1 SE, the outer span | 386.253 / 465.373 | 335.655 / 427.379 | 260.472 / 352.309 | |
| Ancestry share, G4+ at nothing (`ancestry_share_g4_at_nothing`; ends 16 / 11) | 274.874 / 320.835 | 225.954 / 285.564 | 171.506 / 231.116 | $7,557 / 9,551 (29.90M) |
| Ancestry share, G4+ at its bound (`ancestry_share_g4_at_bound`; ends 16 / 11) | 325.196 / 374.793 | 272.934 / 342.352 | 210.779 / 280.197 | $7,778 / 9,757 (35.09M) |
| Ancestry share, the outer span | 274.874 / 374.793 | 225.954 / 342.352 | 171.506 / 280.197 | |
| School low side, within-district b 0.836 (`school_within_district`; ends 24 / 3) | 361.258 / 434.909 | 310.522 / 397.079 | none (set only, as v6) | |
| The shared allocation (`shared_allocation`; ends 48 / 43) | 389.083 / 444.478 (ends 48 / 43) | 307.805 / 394.894 | 227.119 / 314.208 | $7,200 / 9,237 (42.75M) |

The cash set of the count by ancestry share is $171.51–280.20bn, and of the shared allocation $227.12–314.21bn.
v6 read at its shared specifications is 389.083 / 444.478.

Each lineage option's change from v7 splits into the option's own change on v6 (at v6's ends) and how much more or
less the items move the case there:

| Option | Row − v7, set | The option on v6 | The items there less at the case | The items at the option |
|---|---|---|---|---|
| arm_a | −13.442 / −15.631 | −11.082 / −16.226 | −2.360 / +0.595 | −51.890 / −37.235 |
| arm_c | +13.435 / +15.623 | +11.075 / +16.218 | +2.360 / −0.595 | −47.171 / −38.425 |
| c3_minus_se | +3.897 / +3.730 | +2.829 / +3.894 | +1.068 / −0.164 | −48.463 / −37.994 |
| c3_plus_se | −3.897 / −3.730 | −2.829 / −3.894 | −1.068 / +0.164 | −50.598 / −37.667 |

The options rebuild every item on the option's lineage, as v6's do:
- item 6's added people take their job-capital amounts from the option's own cells;
- item 5b's added people part takes the option's G3+-priced count;
- item 7 scales with W's count at the option [APPROX];
- item 8's added people parts come from the option's part models.

The ancestry-share rows split the items' union parts by their generation tag (`union_<G>`), and their added people's
parts go with the added people. Item 5 moves both scenarios' ends to the personal specifications (16 / 11).
[CALCULATION: `ancestry_share.cjs`, `summary.json` `v7.companions`]

## The lineage's addition, by part

`lineage_addition.cjs` splits the 3.04M added people's cost and the lineage's addition at the case's end
specifications (16 low, 11 high; each figure the two methods' mean). It writes only `derived/lineage_addition.json`;
56 gates pass. The last column is v6 read at the same specifications.

| $bn a year, low / high | persons | set | per person, set | cash set | per person, cash | v6 at 16 / 11, set |
|---|---:|---:|---:|---:|---:|---:|
| later losses, priced as identified third-plus members of the same ages | 1,094,828 | 12.939 / 14.843 | $11,819 / 13,557 | 11.262 / 13.165 | $10,286 / 12,024 | 13.947 / 15.360 |
| G3-rate attriters, (1 − C3) × G3+ + C3 × white | 1,944,892 | 8.870 / 12.996 | $4,561 / 6,682 | 5.033 / 9.159 | $2,588 / 4,709 | 11.686 / 14.115 |
| all added people | 3,039,720 | 21.809 / 27.839 | $7,175 / 9,158 | 16.295 / 22.324 | $5,361 / 7,344 | 25.633 / 29.475 |
| the union's response to the larger group | | −0.294 / −0.312 | | −0.294 / −0.311 | | −0.298 / −0.315 |
| the lineage's addition | | 21.515 / 27.527 | | 16.001 / 22.013 | | 25.335 / 29.159 |
| the union-only case (39.71M) | 39,712,493 | 318.037 / 396.122 | $8,008 / 9,975 | 248.425 / 326.510 | $6,256 / 8,222 | 380.451 / 432.321 |
| v7, the case (42.75M) | 42,752,213 | 339.552 / 423.649 | $7,942 / 9,909 | 264.426 / 348.523 | $6,185 / 8,152 | 405.786 / 461.480 |

The items change the added people's cost by −3.824 / −1.636 (later losses −1.008 / −0.517, G3-rate attriters
−2.816 / −1.119). By item, these are the items' added people's parts, which each item's section prints: items 5b and 7
raise the cost, items 6 and 8 lower it (they add to the change, 1e-9). [CALCULATION: `derived/lineage_addition.json`;
the parts, `summary.json` `v7.change_by_item.<item>.lineage`]

## The payloads

- **`derived/corrections.json`** has 848 edits: v6's 769, then item 5b's 9 (769–777), item 6's 32
  (778–809), item 7's 8 (810–817) and item 8's 30 (818–847). Item 5 adds none.
- **`derived/corrections_cash.json`** has 834: v6's 765, then 9 (765–773), 32
  (774–805), 8 (806–813) and 20 (814–833).
- **`meta.responses`** adds item 6's four entries after v6's: `receipt: true`, override `receipt:<line>`, with low and
  high the lane's two readings. Every specification's `line_responses` carries them after v6's line responses.
- **`meta.allocation`** (item 5) has `group_total: "personal"`, the rule, the reason, the specifications and the shared
  reading's use. A consumer that runs consumer.cjs on all 64 specifications takes the band over those at
  `group_total`.
- **`meta.child_credits`** holds the lane's reading, rule, sign, scope, net, SE, by_generation, its own edits and parts,
  scales, arms and beside. `added_people` holds the applied lineage term: `term_bn`, `per_member_usd`, the count, the
  scale and `g3plus_by_line`. `source` gives the file and its sha256.
- **`meta.job_capital_taxes`** holds the rule and the amounts formula. By line, it has the national, response, key
  share and the group's amounts before and after. It also has by_generation, the factors, the added people's wage
  shares, the effect at the reference scenario, the production term's rule, the arms and the source.
- **`meta.white_end_tax_keys`** holds the rule, W's count, the move by allocation and per person, the basis, the
  option rule and the source.
- **`meta.row4_frame`** holds the rule, each component's rule, the components applied in this set, the set-only
  components, the generation rule, the lane's values, the counts, `pension_block` (the arm rule's factors) and the
  source with every input file's sha256.
- **`meta.items`** names v6's four items, then the five new ones. Each applied edit set has `{first, count}` and its
  parts. `personal_allocation` has count 0.
- **The lineage payloads** are v6's files byte for byte (gated); the added people's lineage block is v6's.
- **Stamps.** While v7 is the candidate, `meta.adopted` is `null`. `status` reads "candidate: main case v7, not
  adopted (decisions/2026-10-14-main-case-v7.md not yet written); …", and `case` extends v6's text with the five
  items. An arm or a lineage option is a variant: adopted null, status `variant: …`.

## The item mechanism

v7 wraps v6's package (`package.cjs` `caseOf(B, ids, sel, lineage)`). v6's items build v6's case exactly (`V6.caseOf`).
The v7 layer then builds the new edit sets on that case's models and appends their edits after v6's
(`forItems7`). Four extensions:
- **an allocation item**, kind `allocation`: it changes no edit, only the specification set. `specsFor({allocation})`
  gives `personal` (the case), `shared` or `all`, and `evalPackage`, `central` and `band` take the same option.
  `MAIN_SPECS` is the 32 personal specifications, `SHARED_SPECS` the 32 shared and `ALL_SPECS` the 64.
- **responses on an edit set**: item 6's `responses` become `meta.responses` entries and every specification's
  `line_responses`. A variant built on candidate v4's route gets them after the route (`fixReceipts`, gated equal to the
  engine's route at the case's own options).
- **re-keying by model**: item 6's `editsAt(m)` re-keys any model's four lines to the job-capital amounts on that
  model's cells, so an option or a fill-in method keeps the item's rule.
- **fixed amounts**: items 5b, 7 and 8 shift cells by fixed amounts. An option that moves the national total of a line
  they edit stops in the package (`withItems`), as v6's fixed-amount items do. Items 7 and 8 also stop without the
  lineage item `added_age_mix`, and item 8 stops on a pension block whose Part A is not item pension_tr2026's.

## Gates

- **G1** (`main_case.cjs`, 128 gates, all pass):
  - v6 re-derives. Its package gives v6's per-specification costs, band and cash set exactly, and its payloads are
    v6's files.
  - The case at all 64 specifications is v6 plus the items' change, the methods' mean (1e-9). The change is
    consumer.cjs on v7's payload less consumer.cjs on v6's.
  - v6 at the personal allocation is the review's $405.786–461.480bn at 16 / 11.
  - Both methods find the ends at 16 / 11 over the 32 case specifications, set and cash.
  - Each new item alone matches its source:
    - item 5 gives v6's costs at the personal specifications exactly;
    - item 5b gives the lane's net at every personal specification and 0 at the shared ones, and its added people's
      parts are the lane's per-member term times the G3+-priced count;
    - item 6 sets the four lines' targets to the lane's amounts, with national totals and cell totals unchanged, and
      its change is minus the responses times the amounts. Its union part at each end is minus the lane's
      `central_bn` at that end's reading and allocation, −66.481 / −40.265 (1e-9);
    - items 7 and 8 give the row-4 lane's rows at its specifications 48 / 11, set and cash, and item 8's inputs are
      the lane's recorded ones (exact; the added people's at the case's counts, 1e-12).
  - Gate 4(a), a control and not a published arm: every group (the union and the added people) keyed at its share of
    the case's own wage key, every factor 1 and the four lines at response 1. Its change is minus the whole group's
    wage-key share (0.081013 / 0.088076, personal / shared) times the three lines' national total (1082.388bn), at
    every case specification (1e-9): −87.687bn at the personal specifications and −95.332bn at the shared.
  - Gate 4(b), across lanes: the control's union part at specification 11 is minus the job-capital lane's union
    `plain_wage_share.personal` times that total, −81.325bn (1e-6). The shared figure at 48, −87.219bn, goes
    beside. The job-capital lane gates its own form, −80.977bn personal / −86.849bn shared, on its frame. The case's wage key over the
    September 27 probe's employer_hi share is 1.004295 / 1.004268 (personal / shared), a number and not a scaling factor.
  - Item 8 at `pension_tr2026_combined_funds` is the case's item with the three OASDI components scaled
    (1e-12; Approximations).
  - The interactions are run, and what they leave is zero. The parts add to each item's change. The parts by
    generation add to the union's change, and item 6's lines add to its change.
  - The payload models give the methods' mean (1e-9), and so does consumer.cjs, with no package.
  - The variants, the arms, the companions and the history rows are gated.
- **G2** (`contract.cjs`). Every v6 file, column, row and key is present. The additions are listed:
  - 40 band rows;
  - the `per_spec.csv` columns `in_band`, `oct07_cost_bn`, `item_child_credits_bn`, `item_job_capital_taxes_bn`, `item_white_end_tax_keys_bn`, `item_row4_frame_bn`, `items_v7_interaction_bn`, last;
  - the `sign_reversal.csv` columns `oct14_low`, `oct14_high`, `allocation`, `in_band` and 2 rows (the frozen-services welfare at the
    personal allocation);
  - the meta subtrees.

  Two relocations are documented: v6's `change_at_fixed_specifications` and `range.items_at_the_case_data` move under
  `.oct07_case` (168 paths). One type change is documented: `meta.adopted`, string to null, while v7 is
  the candidate.
- **G3** (`generality.cjs`). v6's own scripts, unmodified, run on this package with the new items off (main_case.cjs 129, sign_reversal.cjs 22, lineage_addition.cjs 41
  gates). They write v6's 10 derived files byte for byte.
- **G4** (`api_check.cjs`). 10 patterns and 120 checks pass. 35 consumer gates need
  code (`derived/api_check.json` `consumer_code`): 14 found by running the consumer's call pattern and
  21 by reading the cited lines (`basis`). Patterns 1–7 run seven consumers' call patterns, as v6's G4 does,
  on the 32 specifications. Pattern 8 is the October 5 package's guards (`viaCandidate`, `followNationals`), pattern
  9 the item API and pattern 10 the shared reading.
  - The generation split adds to v7 at every specification (1e-9) under rules R6–R9: the items' `union_<G>` parts on
    generation G, their added people's parts on G3+ with the lineage.
  - The household split's pension gate misses on v7 by item pension_tr2026's added people's parts and item 8's parts
    on `social_security` and `medicare`, exactly (1e-9); its record says what to count.
  - An arm's payload gives its band row.
  - A lineage option is a variant whose payload gives its row.
  - The guards stop: an unknown item or arm, items out of order, a meta key a payload already has, and a model that
    moves a fixed-amount line (`social_security` for item pension_tr2026, `refundable_tax_credits` for item 5b,
    `modeled_owner_property` for item 8).
- **G5**. Command:

  ```
  uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_2026_10_14 "node {lane}/main_case.cjs" "node {lane}/sign_reversal.cjs" "node {lane}/lineage_addition.cjs" "node {lane}/api_check.cjs" "node {lane}/contract.cjs" "node {lane}/generality.cjs" --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/package.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/sources.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/item_job_capital.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/item_child_credits.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/item_row4.cjs --allow-unrun infra/immigration-fiscal/main_case_2026_10_14/ancestry_share.cjs
  ```

  Result: IDENTICAL: 26/26, exit 0. The six `--allow-unrun` files are modules the scripts load.

## Approximations and assumptions

- **[APPROX] Item 5b's receipt edit at `federal_gap_high_agi`** is the case's own rule, not the lane's: the reference
  shift times the group's target there over the reference (0.925208), −$1.642bn on the union. The
  lane's edits omit that scenario. The case evaluates at the reference scenario, `cbo_collective`, so no band moves.
- **[ASSUMPTION] Item 5b's added people priced as whites take 0.** The lane measured the G3+ term only.
- **Item 5b's shared reading carries a weight artifact.** The credits lane found that the shared allocation's
  within-unit split is unweighted, worth about +$0.93bn of net cost on four lines. v7's total is personal, so it
  touches only the shared companion row.
- **[ASSUMPTION] Item 6's added people work in the industries the lane's G3plus and white_nh factors describe.** They
  take those factors at their own share of the case's wage key. The CPS cannot see them, so their industry mix is not
  measured.
- **[APPROX] Item 6's union old amounts by generation** are the September 29 generation models' cells (convention a).
  They add to the union's cells exactly (gated), so only the split by generation depends on them.
- **Item 6 inherits its lane's measurement and rules**, including the responses (`meta.job_capital_taxes`
  `lines.<g>.response`, the lane's `responses_rule`). The owners keep the same after-tax return, so P and F do not
  move.
- **[ASSUMPTION] Mining's taxes stay**, at response 0 on all three lines and both readings: the lane's rule, at the
  team lead's ask, for a fixed, world-priced resource that is still extracted without the group. The arm
  `job_capital_taxes_mining_as_other_industries` prices them as other industries' taxes.
- **The job-capital lane's beside readings are not case rows.** The brief makes the lane's arms the case's arm rows;
  the 21 readings in its `beside_net_cost_change_bn` stay in the lane. Read as the union's change
  (personal, low / high) against the central's −66.481 / −40.265, the two that move it most are `bea_housing_split` (−74.419 / −48.203) and `mining_severance_0` (−71.248 / −44.076).
  The lane's own finding for the high end, corporate tax at the group's normal-return share by industry scaled to
  TP-5's level, gives −66.481 / −42.900.
- **[APPROX] Item 7 at another lineage option** is the white lane's move times W's count there over the case's: the
  per-person move at the case's age mix, also at an age-mix arm. At the case the factor is 1 exactly.
- **[APPROX] Item 8 at `pension_tr2026_combined_funds`.** The row-4 lane measured the pension components on the
  Trustees arm (separate funds). The combined-funds arm has the same Part A block but another OASDI level. There
  `oasdi_ratio` scales by the arm's ratio_net over the Trustees arm's (1.009709), and `ss_split` and `ss_factor`
  by its f_ss over v6's (1.008587). The row-4 move is taken as relative to the level. Holding the Trustees arm's
  dollars instead would differ by +0.0011bn at the personal allocation and +0.0012bn at the shared (`meta.row4_frame.pension_block.scaling_bn` on that arm's payload).
  Any other pension block stops the item.
- **[ASSUMPTION] Item 8's generation tags** for `part_a`, `oasdi_ratio` and `benefit_tax` follow the case's split
  rule for pension parts (section The items), not the reruns' own groups. No total depends on them.
- **Variants.** Item 6 re-keys every variant's model (`editsAt`), so the four lines hold the job-capital amounts on
  the option's cells. The fixed amounts of items 5b, 7 and 8 stay the case's, as v6's fixed-amount items do.
- **The `adopted` row in `main_case_bands.csv` is v7**, the candidate, under v6's row name for the contract. v6's own
  rows are `oct07_case` and `oct07_cash_set`.
- **The companion readings** carry v6's assumptions (item 3's arm-b age mixes at the lineage options; the
  ancestry-share split rules), with the new items split by their generation tags.
- **Rounding.** Every figure is its file's value rounded once. Where rounded parts would not add to their printed
  total, the parts take controlled rounding (largest remainder; a part that prints 0 never moves). The steps: the set's change printed as v7 less v6 (−49.531 / −37.831), against its own rounding −49.531 / −37.830; the set's change: personal_allocation at the low end rounded up so the parts add; the cash's change printed as v7 less v6 (−42.973 / −36.841), against its own rounding −42.974 / −36.841; the cash's change: personal_allocation at the low end rounded up so the parts add; the cash's change: job_capital_taxes at the high end rounded up so the parts add; job capital by part: union_G1 at the low end rounded down so the parts add; job capital by part: union_G3plus at the high end rounded up so the parts add; item 8, union and added people: added people at the high end rounded up so the parts add; item 8, the union by v4 item: state_index at the low end rounded down so the parts add; item 8, the union by v4 item: state_index at the high end rounded down so the parts add; item 8, the added people by v4 item: state_index at the low end rounded down so the parts add; item 8 by generation: G1 at the high end rounded down so the parts add; option c3_minus_se: on v6 at the low end rounded down so the parts add; option c3_plus_se: on v6 at the low end rounded up so the parts add; the added people (set): later losses at the high end rounded up so the parts add; the lineage's addition (set): the union's response at the high end rounded down so the parts add; the items on the added people, by part: G3-rate attriters at the low end rounded up so the parts add.

## Consumers

This is the brief for the propagation to `oct14`. A consumer that applies the payload whole, evaluates it through
`package.cjs` and takes the band over `MAIN_SPECS` (or `central()`) gets all five items with no code change. A consumer
that does something else needs code where it hard-codes v6's ends (48 / 11), spans all 64 specifications, or splits
the case by generation, household or person. v6's rules R1–R4 still apply as written (`main_case_2026_10_07/RESULT.md`,
Consumers). Five rules join them:

- **R5, `personal_allocation` (set and cash).** The case's specifications are v6's personal ones, 0–31 in v6's
  numbering (`MAIN_SPECS`, 32 per method), and the ends are 16 (low) and 11 (high) in both methods (`summary.json`
  `v7.end_specifications`).
  - The shared allocation stays available for distribution inside the group and for comparisons between groups:
    `SHARED_SPECS` (32–63), `ALL_SPECS` (all 64), and `specsFor`, `evalPackage` and `central` with
    `{allocation: "personal" | "shared" | "all"}`. Its rows are `shared_allocation` and `shared_allocation_cash_set`.
  - `specsFor(o)` without an allocation gives the 32 personal specifications, so indexing it by v6's numbers finds no
    specification 48.
  - A consumer that runs `consumer.cjs` `evaluateAll()` gets all 64 specifications and takes the band over those at
    `meta.allocation.group_total` (`"personal"`). A payload without `meta.allocation` keeps v6's rule.
  - `per_spec.csv` keeps all 128 rows. Its `in_band` column marks the 32 personal specifications per method.
- **R6, `child_credits` (set and cash).** Fixed cell shifts on the personal cells; the shared cells carry 0.
  - The edits (`meta.items` `child_credits` `edits.first`, `count` 9): `federal_income_tax` at all eight incidence
    rules and `refundable_tax_credits` at key `refundable_credits`.
  - Parts `union_<G>:<lane part>[:<scenario>]` go to generation G. Parts `lineage_g3plus:<line>[:<scenario>]` go to
    the added people, with the lineage on G3+ (`meta.child_credits.added_people`: `term_bn`, `per_member_usd`,
    `g3plus_by_line`).
- **R7, `job_capital_taxes` (set and cash).** Four receipt lines re-keyed at every scenario: `corporate_capital`,
  `corporate_labor`, `remaining_production_property` and `other_production_taxes`.
  - The edits: 32 cell shifts, whose new target is the job-capital amount on the model's own cells. National totals
    hold.
  - Four `meta.responses` entries (`receipt: true`, override `receipt:<line>`), with low and high at the lane's two
    readings. They differ by reading for corporate tax (`corporate_capital`, `corporate_labor`): 1 at the low reading and 0.37 at the high, so a consumer that reads one response for both ends gets one end wrong. Every specification's `line_responses` carries each at the specification's reading;
    `consumer.cjs` `lineResponses()` reads them, and a rebuild from `P.LINE_RESPONSES` gets them.
  - Parts `union_<G>:<line>:<scenario>` go to generation G. Parts `lineage_g3plus:` and `lineage_whites:` go to the
    added people, with the lineage on G3+.
  - The four lines responded at 0 before. The whole new amount responds, not only the shift: a consumer that prices
    the item as response × shift misses response × old amount.
  - The parts' old amounts are the September 29 generation models' cells (convention a). A consumer splitting on other
    models must re-key (`withItems()` does), not add the shifts.
- **R8, `white_end_tax_keys` (set and cash).** Eight fixed receipt shifts on `federal_income_tax`, one per incidence
  rule. Its parts `lineage_whites:income_tax_keys:federal_income_tax:<scenario>` go to the added people, with the
  lineage on G3+. `meta.white_end_tax_keys` has `move_bn`, `per_person_usd`, `count` and `scale`.
- **R9, `row4_frame` (set 30 edits, cash 20).** Fixed cell shifts on the owner property, state-price, general sales,
  licence, `federal_income_tax`, `social_security` and `medicare` cells.
  - Parts `union_<G>:<component>:<line>:<cell>` go to generation G. Parts `lineage_g3plus:` and `lineage_whites:` go
    to the added people, with the lineage on G3+.
  - `meta.row4_frame.components_applied` lists the components in this set; Part A, the tax on benefits and the OASDI
    ratio are set only (`set_only`).
  - A consumer that checks the union's pension accrual against `meta.pension_accrual` (the household split does) takes
    R9's parts on `social_security` and `medicare` out first: they move the union to row 4, while `ratio_net` and
    `part_a_accrual_bn` keep v6's published-weight values (G4 records it).

**Where consumers hard-code 48 / 11.** One pass at 2026-10-14 17:55 JST, outside this lane:

```
rg -n -g '*.{cjs,js,py,mjs}' -g '!**/derived/**' -g '!**/_cache/**' -e '\b48\b[^0-9\n]{0,14}\b11\b' infra/immigration-fiscal
```

It finds 238 lines. Intersected with the lanes whose code names the live case (`oct07` or
`main_case_2026_10_07`), it leaves ten consumer lanes:
- `black_comparator_rough_2026_09_28`: `engine_lines.cjs:118`, `rekey.py:3`, `rekey_sept29.py:12`;
- `break_conditions_2026_09_29`: `engine_breaks_sept29.cjs:17`, `engine_breaks_sept29.cjs:128`, `tables.py:80`, `tables_oct05.py:344`, `engine_breaks.cjs:7`, `engine_breaks.cjs:126`, `engine_breaks.cjs:182`, `tables_oct07.py:515`, `tables_sept29.py:263`;
- `debt_legacy_2026_09_23`: `debt_legacy.py:376`, `debt_legacy.py:394`, `debt_legacy.py:411`;
- `figures_2026_09_22`: `build_data.cjs:85`;
- `generation_account_2026_09_24`: `run_generations.cjs:61`, `run_generations.cjs:962`, `run_generations_v4.cjs:5`, `run_generations_v5.cjs:5`, `run_generations_v5.cjs:293`, `run_generations_v5.cjs:296`, `run_generations_v5.cjs:297`, `run_generations_v6.cjs:4`, `run_generations_v6.cjs:34`, `run_generations_v6.cjs:472`, `run_generations_v6.cjs:476`, `run_generations_v6.cjs:477`;
- `late_arrival_account_line_2026_09_27`: `run_cells.cjs:697`;
- `legacy_comparators_2026_09_30`: `group_lines.py:10`;
- `main_case_decomposition_2026_09_29`: `decompose.cjs:41`, `decompose.cjs:184`;
- `white_replacement_2026_09_28`: `engine_lines.cjs:118`, `rekey_sept29.py:9`;
- `world_ledger_2026_09_27`: `generation_lines.cjs:9`.

Three more lanes in the intersection produce v6 or its items and stay on oct07: `main_case_2026_10_07`,
`job_capital_taxes_2026_10_14` and `row4_class_2026_09_29`. Twelve lanes name the live case with no literal 48 / 11;
their ends follow `MAIN_SPECS` or a pinned band: `assumption_explorer_2026_09_21`, `closed_budget_2026_10_06`, `distribution_weights_2026_09_23`, `historical_backcast_2026_09_20`, `indian_full_account_2026_09_29`, `number_drift_audit_2026_09_29`, `overview_2026_09_28`, `pension_legacy_2026_09_30`, `sept24_propagation_2026_09_24`, `uncertainty_propagation_2026_09_22`, `winners_losers_2026_09_24`, `within_group_distribution_2026_09_29`. The other lanes with a literal 48 / 11 are earlier
cases or producers, plus `tax_key_heldout_2026_09_28` (`ends.cjs`), which v6's RESULT lists among its consumers. Peers
have uncommitted edits in some of these lanes, so the lines are the working tree's at that time.

**What G4 found.** `derived/api_check.json` `consumer_code` holds 35 records: consumer, line, what it does
today and the change it needs on v7, found by running the consumer's call pattern (14) or reading its code
(21). The propagation workers run each lane on oct14 and locate its stops there.

Notes:
- **Locate items by `meta.items`**: `edits.first` and `count`, never positions. The set has 848 edits and the
  cash set 834. personal_allocation has count 0.
- **The four new responses** are in `meta.responses` after v6's entries, and in every specification after v6's line
  responses. A consumer that builds its own specifications from a fixed list misses them, and its job-capital lines
  then respond at 0.
- **The stamp.** While v7 is the candidate, `meta.adopted` is `null` and the status starts "candidate: main case v7,
  not adopted". A consumer that checks `meta.adopted` (`debt_legacy.py`'s v5_parts) waits for the adoption.
- **The oracle.** Each consumer gates its oct14 total against `main_case_bands.csv`: `adopted` and `cash_set`.
- **The companion readings** are the rows `lineage_<option>`, `ancestry_share_<scenario>` and `shared_allocation`
  (each with `_cash_set`), and `v7.companions` in `summary.json`.
- **The item inputs stay on oct07:** the credits and job-capital lanes' `item.json`, the white lane's
  `limits_oct07.csv`, the row-4 lane's oct07 files, and v6's four producers. Rebuilt on oct14, each would add its item
  twice. The white and row-4 lanes' other outputs are a consumer's and move to oct14.
- **Comparators.** The comparator groups take R7 too, at the job-capital lane's `white_nh` or `black_nh` factor (`item.json` `factor`), so both sides keep the same rule. The credits lane measured item 5b's crossing for the Mexican-origin union and its G3+-priced added people only. Items 7 and 8 correct this account's own keys and frame; whether a comparator needs a counterpart is open.

## For the parent

- **Adoption.** Write `decisions/2026-10-14-main-case-v7.md`. Then:
  1. in `package.cjs`, set `STATUS` to `adopted` (`ADOPTED` is 2026-10-14; the stamp gate checks that the decision
     file exists);
  2. in `contract.cjs`, delete the two `TYPE_CHANGES` entries (`meta.adopted` is a string again);
  3. rerun the chain and G5.

  The adoption changes the payloads' stamps only. The edits, lines, responses and every band stay as they are.
- **The pinned files**, on the adopted run (consumers pin the committed bytes):
  - `corrections.json` fde682e75d23148bb9177726f596374b63ab9027acc49e7d6b546947d89d0958;
  - `corrections_cash.json` 581701613b7f3c8086437100334e3818ebe062dc57e2e486f14897208b05de97;
  - `summary.json` b30720cff0c29637ab6f74d809829fdbfc4b82a00a45fa286e3f0c1c5c183582.

  The payloads record each source file's hash (`meta.child_credits.source`, `meta.job_capital_taxes.source`,
  `meta.white_end_tax_keys.source`, `meta.row4_frame.source`), so an edit to any of them changes their bytes. Rerun
  the chain after any such edit.
- **Two choices of mine to confirm:**
  - item 8 at `pension_tr2026_combined_funds`: the OASDI components scale with the arm's level (sent to you with the
    numbers; Approximations). Holding the Trustees arm's dollars differs by +0.0011bn at the personal allocation and +0.0012bn at the shared, and a rerun of that arm
    at row-4 weights would be a new Python measurement;
  - item 8's generation tags for the pension components: the case's split rule, not the reruns' groups (section The
    items). I recommend the split's rule, because the generation account then splits item 8's pension parts the way it
    splits item pension_tr2026's.
- **The row-4 lane's new checker.** A peer's uncommitted `row4_class_2026_09_29/row4_oct14.cjs` expects payload item
  `row4_frame` (kind `edit_set`, `edits.first` and `count`) whose edits, summed per cell, equal its export's cell shifts
  (1e-9), with `meta.adopted` "2026-10-14" and `meta.allocation.group_total` "personal". Item 8 has those cells and
  that layout, so the checker can pass only after the adoption.
- **Peer files on an earlier build.** `white_replacement_2026_09_28/derived/*_oct14*` (untracked, mtimes 17:11–17:15)
  were built on this lane's 16:59 files, the three-item build, before items 7 and 8 and item 5b's added people. They
  need a rerun on these files. Item 7 keeps reading `limits_oct07.csv`.
- **The Census coverage bound** is yours, as briefed; nothing here builds it.
- **The propagation.** Rules R5–R9 above, 35 consumer gates needing code, and the hard-coded 48 / 11 list.

## Files

- `package.cjs`: the v7 registry over v6's, `caseOf`, `forItems7`, `specsFor`, the specification sets, the stamps and
  `fixReceipts`.
- `sources.cjs`: where items 5b and 6 read their lanes' files; it stops while a lane's verdict says pending, stub or
  in progress.
- `item_child_credits.cjs`: item 5b's builder (switch `LINEAGE`, on).
- `item_job_capital.cjs`: item 6's builder (`editsAt`, the responses by reading, the control block for gate 4).
- `item_row4.cjs`: items 7 and 8's builders, ported from `row4_oct07.cjs`, with the lane's inputs and oracle.
- `ancestry_share.cjs`: v6's count by ancestry share with v7's generation tags.
- `main_case.cjs`: G1 and the derived files.
- `sign_reversal.cjs`: v6's measures with the oct14, `allocation` and `in_band` columns, and the frozen-services
  welfare at the personal allocation.
- `lineage_addition.cjs`: the lineage's addition by part on v7.
- `contract.cjs` (G2), `generality.cjs` (G3) and `api_check.cjs` (G4).
- `derived/`:
  - `corrections.json`, `corrections_cash.json`, `lineage_payload.json` and `lineage_payload_cash.json`;
  - `main_case_bands.csv`, `components.csv`, `per_spec.csv`, `summary.json`, `sign_reversal.csv` and
    `lineage_addition.json`;
  - the gate records `contract.json`, `generality.json` and `api_check.json`.

**Run order**, about 90 seconds on this run (G5's rerun of all six took 88 seconds):

```
node main_case.cjs && node sign_reversal.cjs && node lineage_addition.cjs && node api_check.cjs && node contract.cjs && node generality.cjs
```

## Log (append-only; times from `date` or file mtimes)

- 2026-10-14 13:52 JST — lane created; reading the brief, CLAUDE.md, the v6 assumption review and main_case_2026_10_07.
- 2026-10-14 14:07 JST (the message's timestamp in the transcript) — asked jobcap to confirm the `item.json` contract the
  stub followed.
- 2026-10-14 14:11 JST (transcript) — sent the parent seven design points the brief leaves open, with my default for
  each:
  - items 7 and 8 not built;
  - item 6's edit form;
  - the other receipt scenarios at the lane's key share times each cell's total [APPROX];
  - the ceiling gate's form;
  - `sign_reversal.csv` keeps v6's measures and adds oct14 columns;
  - item 6 stops without the age-mix lineage item;
  - `per_spec.csv`'s columns.

  No reply.
- 2026-10-14 15:16 JST (transcript) — the credits lane rewrote `item.json` at 15:15 (sha256 2773e34d…). Its lineage
  block asks the v7 lane to apply its G3+ term to the 1.957M G3+-priced added people (+$0.419bn); the brief says union
  only. Asked the parent. Built union-only behind `LINEAGE`, with the lane's three arms as arm rows. No reply.
- 2026-10-14 15:22–15:28 JST (scratch log mtimes) — first full runs, on the delivered credits file and the job-capital
  stub. `main_case.cjs` passed all its gates. `lineage_addition.cjs` failed only its v6 gate, because v6's API has no
  allocation option; fixed with a personal-band helper. `sign_reversal.cjs` passed.
- 2026-10-14 15:39–15:46 JST (chain log mtimes; `date` 15:43) — the chain on the stub. G1, `sign_reversal.cjs`,
  `lineage_addition.cjs` (56 gates) and G4 (111 checks) passed. G2 failed on v6's `range.items_at_the_case_data`, which
  v7 moves under `.oct07_case`; documented as a second relocation, then G2 PASS. G3 PASS in 316 s while other lanes
  ran (59 s alone at 15:53).
- 2026-10-14 15:48 JST (transcript) — asked the parent whether item 6's corporate response is {low 1, high 0.37}: the
  parent's notes say so, the brief says low = high. No reply; at 15:56 the job-capital lane's verdict lists it among
  the parent's asks.
- 2026-10-14 15:50–15:53 JST (derived mtimes; `date` 15:52) — the job-capital lane filled its verdict, and the case built
  on its file (sha256 4d0169f6…) at $330.44–386.13bn. Found and fixed: item 6's parts by generation were 0 in
  `summary.json`, because its `union_<G>` parts lack the ":" the split looked for. A gate now checks that the
  generations add to the union, and another that item 6's lines add to its change. Removed the stub files (`_stub/`);
  `sources.cjs` names no stub.
- 2026-10-14 15:56 JST (`date`) — the job-capital lane's verdict went back to "PROBE IN PROGRESS". The parent's asks
  rebuild its central: mining's taxes at response 0, corporate at {low 1, high 0.37}, the whole other-production line
  keyed. The chain stopped at `sources.cjs` [BLOCKED], as designed. At 15:57 I sent jobcap the shape the reader
  accepts.
- 2026-10-14 16:02 JST (`date`) — `item_job_capital.cjs` now takes a line's response as a number or {low, high}. Tested on
  the lane's previous file with corporate set to {1, 0.37}: G1 passes, and v7 is $330.44–415.56bn on that input
  [scratch, not a result].
- 2026-10-14 16:21 JST (`date`) — re-read every consumer line G4 cites, at HEAD (52e2ccfb for those files). Corrected:
  - the back-cast, distribution, world-ledger and household rows do not hard-code 48 / 11: their ends follow
    `MAIN_SPECS`. The back-cast stops on the specification count instead, and distribution's premise of a shared low end
    is silent;
  - the winners lane's ends follow the package too, but its gate at `:176` reads receipt overrides at their low
    response. It stops once item 6's corporate entries differ by reading;
  - each record now carries `basis`, "run" or "read";
  - G4's arm check evaluates an arm's payload at the arm's own specifications.

  G4 passes on the scratch inputs: 114 checks, 34 consumer gates (14 run, 20 read).
- 2026-10-14 16:39 JST (`date`) — the job-capital lane's verdict still reads PROBE IN PROGRESS, and its `item.json` is
  still the 15:50 file, so the case waits. Meanwhile I re-read the remaining cited consumer lines at HEAD (no consumer
  file has changed since 52e2ccfb). Corrected:
  - the comparators' `ENDS {48, 11}` stops on v7 rather than staying silent. `P.specsFor(oo)` gives the 32 personal
    specifications, so `specs[48]` is undefined, and `evaluateFull` throws (tested on v6's package);
  - the world ledger's `beside_extra.py:125` CASE_SET is gated at `:511`, so it stops;
  - public charge and post-2024 law read the decomposition's oct05 frame, which v7 leaves unchanged.

  Added one consumer record, basis "read": the uncertainty lane gives R7's four receipt overrides their account key's
  spread (`propagate.py:814-841`), while item 6's amounts sit on the job-capital lane's industry wage key.
- 2026-10-14 16:43 JST (the watcher's clock) — the job-capital lane delivered: its verdict is final ($66.5bn low,
  $40.3bn high on the union at the personal allocation), and its `item.json` (sha256 bf813d29…) was written 16:39:37.
  Every line's response is now {low, high}, `central_bn` is by reading, mining's cells are out of every line's base, and
  the residential parts are out of the other production base. `item_job_capital.cjs` now reads `central_bn` by reading
  and gates it as the sum of response × group_bn. `main_case.cjs` gates item 6's union part at each end against the
  lane's central at that end's reading (1e-9).
- 2026-10-14 16:48 JST (`date`) — the chain and G5 on that file passed: G5 IDENTICAL 25/25, exit 0.
- 2026-10-14 16:49 JST (item.json mtime 16:49:11) — the lane rewrote `item.json` (sha256 a9c74711…). It renamed two
  arms, added the arm `normal_return_share` and changed its beside rows; the central did not change. I asked jobcap to
  signal when the file was final, and waited until the lane had been quiet for four minutes (16:56). Its 16:52 log
  entry says "Final."
- 2026-10-14 16:59 JST (`date`) — the chain and G5 on the final files (job capital a9c74711…, credits 2773e34d…):
  - G1 113 gates;
  - `sign_reversal.cjs`, `lineage_addition.cjs` (56 gates);
  - G4: 114 checks, 35 consumer gates (14 run, 21 read);
  - G2 and G3 (v6's 129, 22 and 41 gates; 10 files byte for byte);
  - G5 IDENTICAL 25/25, exit 0.

  v7 is $338.31–422.41bn, cash set $262.20–346.30bn. This RESULT was then filled from the derived files by a scratch
  script, with every number rounded once and the controlled rounding listed. Not committed: the parent reviews and
  commits.
- 2026-10-14 17:27 JST (`item_child_credits.cjs` mtime) — the parent's answers came in after 16:59 (transcript):
  - items 7 and 8 in, in the order 5, 5b, 6, 7, 8;
  - item 5b's lineage term on;
  - the `federal_gap_high_agi` receipt edit by the case's rule [APPROX];
  - item 6's key rule stated as a rule;
  - gates 4(a)/(b) in place of the ceiling gate;
  - `allocation` and `in_band` columns in `sign_reversal.csv`;
  - a slimmed Consumers section.

  Item 5b rebuilt with `LINEAGE` on: 9 edits, the added people's +$0.419bn split in G3+'s line proportions, and the
  gap edit at 0.925208 of the reference shift.
- 2026-10-14 17:28–17:38 JST (patch-file mtimes) — items 7 and 8 built in a new `item_row4.cjs`. It ports
  `row4_oct07.cjs:108-231` and reads that lane's inputs, with item 8's union components tagged by generation by the
  case's split rule. Updated `package.cjs`, `main_case.cjs` (gates 4(a)/(b), each item alone against `row4_oct07.json`),
  `sign_reversal.cjs`, `lineage_addition.cjs`, `api_check.cjs` (R8, R9 and the guards) and `ancestry_share.cjs`. A
  scratch run of `main_case.cjs` passed every gate at 17:34 (log mtime). Then I added a guard: item 8 stops on a
  pension block that is not item pension_tr2026's.
- 2026-10-14 17:38 JST (`chain3.log` mtime) — the chain stopped at `main_case.cjs`: that guard blocked item 8 at the
  arm `pension_tr2026_combined_funds`, whose OASDI level differs.
- 2026-10-14 17:45 JST (`item_row4.cjs` mtime) — sent the parent the arm rule with my recommendation, and built it
  provisionally: at that arm (the same Part A block) `oasdi_ratio` scales by 1.009709 and `ss_split` and `ss_factor` by
  1.008587 [APPROX]. Holding the Trustees arm's dollars would differ by about $0.0012bn. Any other block still stops.
  The arm's parts are gated in `main_case.cjs` (1e-12).
- 2026-10-14 17:46–17:49 JST (log mtimes) — a scratch run of `main_case.cjs` passed. The chain then failed one G4 check:
  the household split's pension gate also misses by item 8's parts on `social_security` and `medicare`. The check and
  its consumer record now count them. G4 passed with 120 checks and 35 consumer gates.
- 2026-10-14 17:52 JST (`chain3.log` and `g5.log` mtimes) — the chain and G5 on the final build: all six scripts rc 0,
  and G5 IDENTICAL 26/26, exit 0. v7 is $339.55–423.65bn and the cash set $264.43–348.52bn.
- 2026-10-14 17:55 JST (`date`) — the hard-coded 48 / 11 pass for the Consumers section (one `rg` over `.cjs`, `.js`
  and `.py`; 238 lines). This RESULT was then filled from the derived files by a scratch script. Not committed: the
  parent reviews and commits.
- 2026-10-14 18:04 JST (`date`) — found a peer's white-lane `*_oct14` files (mtimes 17:11–17:15). They were built on
  this lane's three-item files of 16:59, so they predate items 7 and 8; flagged for the parent. Refilled this RESULT.
- 2026-10-14 18:11 JST (parent): adopted. Decision `decisions/2026-10-14-main-case-v7.md` written; STATUS set to
  `adopted` in `package.cjs` and the two TYPE_CHANGES entries removed from `contract.cjs`. Chain rerun (exit 0;
  G3 byte for byte) and G5 IDENTICAL 26/26, exit 0. Only the stamps changed.

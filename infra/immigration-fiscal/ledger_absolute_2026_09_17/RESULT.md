<!-- fiscal-repair-2026-09-19 -->
**Current fiscal release (September 19):** [Repaired yearly and lifetime calculation index](../../../research/immigration-yearly-lifetime-cost-repair-2026-09-19.md) supersedes affected annual, household-financing and lifetime figures below. It reports both allocation conventions, actual-age survival NPVs and unresolved coverage. Earlier text and calculations remain historical evidence; unrelated findings are unchanged.

**Verdict:** Completing the account does not preserve the sign of the partial balance, and it does not rescue the gap either. The Mexican-origin union's measured partial absolute of **+$50.24bn** becomes **−$253.93bn** once every priceable omitted item is charged under the central conventions. The age-standardized gap against third-plus non-Hispanic whites widens from **−$5,795 to −$7,095 per standardized person**, and the age-matched total from **−$290.6bn to −$354.3bn**. That endpoint is a convention, not a measurement: across the 144 combinations of the four contested arms the union absolute runs from −$548.37bn to −$87.04bn and never turns positive. The account is dominated by average-cost public services, so the break-even marginality dial sits at **m\* = 0.120**. Summed over all civilian-household residents the account reaches a position of −$966.7bn against a consolidated FY2024 position of −$2,590.8bn, covering 63% of consolidated outlays and 71% of consolidated receipts; the −$1,624.1bn residual is reported, not forced.

## Audit correction — September 19, 2026

**The −$263bn endpoint and the national reconciliation are provisional.** Item G retains gross state/local highway spending while item R includes federal transportation outlays; intergovernmental grants are not consistently netted. The reconciliation also adds federal outlays to state/local direct spending while crediting only state/local own-source revenue. The same grant can therefore be charged twice. Some education/Medicaid overlap is already netted; do not subtract all grants indiscriminately. User charges and miscellaneous revenue also require reconciliation. A revised endpoint needs function- and vintage-matched consolidation; this audit does not assert a corrected total or a sign reversal. The same-age partial-account benchmark gaps remain descriptive results. [SOURCE: fiscal audit evidence; Census definitions and FHWA FA-5]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](../../../research/immigration-five-day-cross-check-2026-09-19.md).


claude-opus-5[1m]

[DATA: CPS ASEC 2025 public-use file, income year 2024, 142,125 person records, 58,147 SPM units, full and 160 replicate weights; MEPS 2024 full-year donor transport]
[INFERENCE: every item is an accounting scenario, a published aggregate times a measured exposure, not an observed payment]
[UNVERIFIED: the allocation conventions are choices; the arms matrix, not the standard errors, is the honest width of the result]

## Files

- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py`
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/check_gates.py`
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/ledger_absolute_2026_09_17/README.md`
- `derived/`: `items_by_group.csv` (168 rows), `waterfall.csv` (84), `arms_matrix.csv` (144), `marginality_curve.csv` (21), `complete_gaps.csv` (8), `complete_gaps_by_item.csv`, `national_reconciliation.csv`, `audit.json`

Every reported number comes from `params/params.json` (sha256 in `audit.json`) or from an in-repo cache named in the source column. **No number came from the placeholder file.** The builder refused all 13 non-verified entries; `params_used` lists the 46 parameters consumed.

### Waterfall, central arms, $bn

| step | item | Mexico-born | 2nd gen | 3rd+ self-ID | union | union se | flag |
|---|---|---|---|---|---|---|---|
| 0 | base | +6.6 | +10.7 | +32.9 | +50.2 | 7.5 | cps_records |
| 1 | G | -43.5 | -48.8 | -23.4 | -115.7 | 7.8 | cps_records |
| 2 | K | -48.5 | -57.7 | -32.3 | -138.5 | 8.0 | cps_records |
| 3 | D | -48.5 | -57.7 | -32.3 | -138.5 | 8.0 | dropped_no_verified_parameter |
| 4 | U | -50.7 | -61.3 | -35.9 | -147.9 | 8.1 | cps_records |
| 5 | I | -52.1 | -63.4 | -37.2 | -152.6 | 8.1 | cps_records |
| 6 | M | -62.9 | -74.6 | -50.3 | -187.8 | 8.3 | cps_records |
| 7 | N | -68.7 | -81.1 | -57.1 | -206.9 | 8.3 | external_add_no_se |
| 8 | E | -71.4 | -81.1 | -57.1 | -209.6 | 8.3 | cps_records |
| 9 | C | -63.2 | -69.8 | -42.0 | -175.0 | 8.7 | cps_records |
| 10 | X | -51.9 | -56.5 | -28.8 | -137.3 | 8.6 | cps_records |
| 11 | R | -84.2 | -96.1 | -72.2 | -252.4 | 8.8 | cps_records |
| 12 | F | -84.2 | -96.1 | -72.2 | -252.4 | 8.8 | central_arm_is_zero |
| 13 | S | -85.7 | -96.1 | -72.2 | -253.9 | 8.8 | cps_records |

### Complete absolute balance, crude per person at each group's own age mix

| group | at step 12 $bn | complete (step 13) $bn | crude per person $ |
|---|---|---|---|
| Mexico-born | -84.2 | -85.7 | -7,010 |
| 2nd gen | -96.1 | -96.1 | -6,702 |
| 3rd+ self-ID | -72.2 | -72.2 | -5,034 |
| union | -252.4 | -253.9 | -6,209 |
| 3rd+ NH white | -376.3 | -376.3 | -2,174 |
| all natives | -934.3 | -934.3 | -3,294 |

### Age-standardized: the complete-account gap against each reference

| group | reference | partial common-age gap $/person | complete common-age gap $/person | partial age-matched $bn | complete age-matched $bn |
|---|---|---|---|---|---|
| Mexico-born | 3rd+ NH white | -6,562 (321) | -7,651 (384) | -103.1 (4.9) | -120.8 (5.7) |
| Mexico-born | all natives | -5,056 (294) | -5,484 (351) | -85.2 (4.3) | -94.7 (5.0) |
| 2nd gen | 3rd+ NH white | -5,943 (469) | -7,435 (617) | -113.7 (5.1) | -139.3 (5.9) |
| 2nd gen | all natives | -4,437 (445) | -5,269 (589) | -84.3 (4.1) | -100.0 (4.7) |
| 3rd+ self-ID | 3rd+ NH white | -4,622 (371) | -6,149 (460) | -73.8 (4.9) | -94.2 (5.6) |
| 3rd+ self-ID | all natives | -3,116 (357) | -3,982 (445) | -45.6 (4.4) | -56.4 (4.9) |
| union | 3rd+ NH white | -5,795 (245) | -7,095 (302) | -290.6 (10.6) | -354.3 (12.0) |
| union | all natives | -4,289 (207) | -4,928 (257) | -215.0 (8.3) | -251.0 (9.3) |

### Items, union

| item | arm | central | union $bn | per person $ | se $bn | common-age gap vs white $/person | source |
|---|---|---|---|---|---|---|---|
| G | nominal2022 |  | -159.69 | -3,905 | 1.52 | -191 | cache:22slsstab1.xlsx |
| G | deflated2024 | yes | -165.97 | -4,058 | 1.57 | -198 | cache:22slsstab1.xlsx + params:deflator |
| K | central | yes | -22.73 | -556 | 0.44 | -116 | params:k12 F-33 capital, interest and fall membership by state |
| U | central | yes | -9.44 | -231 | 0.45 | -82 | params:underreporting |
| I | central | yes | -4.74 | -116 | 0.15 | -59 | params:improper_payments |
| I | zero |  | +0.00 | +0 | 0.00 | +0 | convention |
| M | central | yes | -35.15 | -859 | 0.40 | +64 | params:meps_coverage |
| M | zero |  | +0.00 | +0 | 0.00 | +0 | convention |
| E | zero |  | +0.00 | +0 | 0.00 | +0 | convention |
| E | stock | yes | -2.72 | -66 | 0.07 | -76 | params:enforcement,unauthorized |
| E | stock_plus_flow |  | -5.26 | -129 | 0.14 | -148 | params:enforcement,unauthorized,city_migrant |
| E | stock_pew_secondary |  | -1.91 | -47 | 0.05 | -54 | params:enforcement,unauthorized (Pew, secondary) |
| C | wage25_capital75 | yes | +34.55 | +845 | 1.13 | -1,732 | params:omb,corporate |
| C | per_capita |  | +83.59 | +2,044 | 0.77 | +0 | params:omb,corporate |
| C | all_capital |  | +25.78 | +630 | 1.39 | -2,050 | params:omb,corporate |
| X | per_capita | yes | +37.72 | +922 | 0.35 | +0 | params:omb,corporate |
| X | consumption_proxy |  | +27.80 | +680 | 0.40 | -313 | params:omb,corporate |
| R | central | yes | -115.14 | -2,815 | 1.86 | +840 | cache:omb_hist03z1_fy2027.xlsx + params:omb |
| R | all_per_capita |  | -183.18 | -4,479 | 1.69 | -0 | cache:omb_hist03z1_fy2027.xlsx + params:omb |
| R | central_housing_by_reported_subsidy |  | -115.57 | -2,826 | 2.05 | +703 | cache:omb_hist03z1_fy2027.xlsx + params:omb |
| R | all_zero |  | +0.00 | +0 | 0.00 | +0 | convention |
| F | zero | yes | +0.00 | +0 | 0.00 | +0 | convention |
| F | per_capita |  | -215.08 | -5,259 | 1.99 | -0 | cache:omb_hist03z1_fy2027.xlsx |
| F | proportional_to_federal_tax |  | -120.39 | -2,944 | 3.08 | +3,106 | cache:omb_hist03z1_fy2027.xlsx |
| S | half_inside_meps | yes | -1.49 | -36 | 0.13 | -40 | params:state_medicaid_undocumented, assembled from individual verified state lines |
| S | none_inside_meps |  | -2.97 | -73 | 0.26 | -80 | params:state_medicaid_undocumented, assembled from individual verified state lines |
| S | all_inside_meps |  | +0.00 | +0 | 0.00 | +0 | params:state_medicaid_undocumented, assembled from individual verified state lines |
| N | midpoint |  | -19.07 | -466 | 0.00 | +99 | external:institutional_bound_2026_09_17 |

### Arms matrix, union absolute $bn

144 combinations, from -548.4bn to -87.0bn.

| corner | F | E | C | R | union $bn |
|---|---|---|---|---|---|
| most negative | per_capita | stock_plus_flow | all_capital | all_per_capita | -548.4 |
| least negative | zero | zero | per_capita | all_zero | -87.0 |

### National reconciliation against the consolidated FY2024 position

| block | line | $bn |
|---|---|---|
| consolidated | federal outlays FY2024 | -6,735.3 |
| consolidated | federal receipts FY2024 | +4,919.9 |
| consolidated | state and local direct general expenditure | -4,185.3 |
| consolidated | state and local general revenue from own sources | +3,409.9 |
| consolidated | consolidated position | -2,590.8 |
| known part of the residual | item F charged at zero in the central arm | -1,788.7 |
| known part of the residual | OMB function 950 undistributed offsetting receipts | -146.7 |
| known part of the residual | OMB function 920 allowances | -0.0 |
| known part of the residual | state and local capital outlay | -385.9 |
| residual | unpriced or coverage | -1,624.1 |
| coverage | account outlays as a share of consolidated outlays | 0.630 |
| coverage | account receipts as a share of consolidated receipts | 0.709 |
| coverage | civilian household population over resident population | 0.990 |

### Marginality curve

| m | union absolute $bn | per person $ |
|---|---|---|
| 0.00 | +34.8 | +850 |
| 0.25 | -37.4 | -915 |
| 0.50 | -109.6 | -2,679 |
| 0.75 | -181.8 | -4,444 |
| 1.00 | -253.9 | -6,209 |

Break-even m\* = 0.1204

### Dropped for want of a verified parameter

- **D** — district F-33 x CCD Hispanic/white per-pupil differentials not verified
- **S(states without a verified line)** — priced for 6, 8, 17, 36, 41, 53 only; not priced: mn_minnesotacare_undocumented_state_cost: not verified; ma_health_safety_net_state_cost: not verified; co_cover_all_coloradans_children_state_cost: not verified; ca_undocumented_total_general_fund_2024_25: not verified

### What remains unpriced

- OMB function 920 allowances and 950 undistributed offsetting receipts
- federal and state capital stock other than school capital
- the reported housing-subsidy base in the CPS (SPM_CAPHOUSESUB sits outside the account's selected non-cash transfers); federal housing assistance is instead carried whole as OMB subfunction 604 inside item R
- Social Security under-reporting: its admin/survey ratio is 1.0881, above 1, and the brief applies Social Security only when that ratio is below 1
- item S outside the waterfall: the brief's waterfall order does not include it, so the state coverage charge is reported per item but not accumulated
- state and local capital outlay outside K-12
- deficit finance: the account charges outlays, not the tax burden that would fund them
- emigration, mortality and any lifetime or dynamic margin

## The two ways to read the endpoint

The crude per-person column above puts each group at its own age mix, so it is not comparable across groups; the Mexican-origin groups are younger than the white reference and a younger population buys less Social Security and Medicare. The age-standardized table is the comparable one, and it is the one that answers "compared with whom". Both starting values reproduce the upstream lane's published estimates exactly, which is an executed gate: the partial common-age gap for the union against third-plus non-Hispanic whites is **−$5,795.3** and the partial age-matched total is **−$290.59bn**. (The figure −5,734 quoted in the request does not appear in `estimates.csv` for any of the thirteen scenarios; the nearest are the head-weighted arm at −5,692 and the renter-property arm at −5,634.)

Completing the account widens the gap by about 22% for the union, and the widening is not uniform: the third-plus self-identified group's gap against whites widens most in proportional terms, from −$4,622 to −$6,149, because the items that fall on native-born residents with children and property are the ones being added.

## Where the conventions bite

The endpoint is not driven by the Mexican-origin groups' own behaviour. Charging state and local general services per capita costs the union $165.97bn on its own, and it is a charge every resident bears. The three items that actually distinguish the groups are small: enforcement at $2.72bn, the institutional add at $19.07bn, and state-funded coverage at $1.49bn. What moves the absolute balance is the decision to charge average cost for services the partial account left out entirely.

The same point in reverse: the flat per-capita items have a common-age gap against the white reference of exactly zero by construction, verified to 5e-16 relative. They move every absolute balance and change no relative one.

## The marginality dial: what is on it and what is not

Scaled by m, because they are average-cost charges for congestible services:

- **G**, state and local general services, −$165.97bn
- **K**, K-12 capital outlay and interest, −$22.73bn
- **D**, dropped, so zero either way
- **F**, federal pure public goods, zero in the central arm, so the dial does nothing to it here
- **the per-capita part of R only**, −$100.00bn: the 750 remainder, 500 net, 550 net, 600 net and 400 transportation

Fixed at m = 1, because they are records-based charges tied to a specific person or receipt:

- **U** −$9.44bn, **I** −$4.74bn, **M** −$35.15bn, **N** −$19.07bn, **E** −$2.72bn, **S** −$1.49bn, **C** +$34.55bn, **X** +$37.72bn
- **the records-based part of R**, −$15.14bn: 700 veterans net of VA medical per veteran, 602 by federal pension income, and the BOP Mexican-national share of 753

At m = 0 the union balance is **+$34.77bn**, which decomposes as

```
  50.238  base partial account
+ 18.738  U + I + M + E + C + X + S, the named records-based items
- 19.069  N, the institutional external add
- 15.135  the records-based part of R
= 34.773
```

Your arithmetic omitted item X, +$37.72bn, and item S, −$1.49bn. The dialled total is −$288.70bn, so m\* = 34.773 / 288.705 = **0.1204**.

## National reconciliation against the consolidated FY2024 position

Summed over all 336.7M civilian-household residents rather than the target groups, the account reaches **−$966.7bn**. The consolidated position built from the same parameters is **−$2,590.8bn**: federal receipts of $4,919.9bn less outlays of $6,735.3bn, plus state and local own-source general revenue of $3,409.9bn less direct general expenditure of $4,185.3bn, the state-local figures being 2022 Census of Governments amounts inflated by the same 1.039312 factor item G uses. The residual is **−$1,624.1bn**, labelled unpriced or coverage.

The residual is reported, never solved for, and a gate fails if it comes back near zero. Candidate explanations are listed with their signs in `national_reconciliation.csv` rather than netted into an exact decomposition: item F charged at zero is worth $1,788.7bn on its own, function 950 undistributed offsetting receipts −$146.7bn, and state and local capital outlay outside K-12 −$385.9bn. Those over-explain the residual, which means the account also charges things the consolidated position nets differently and leaves some receipts uncovered; the account covers **63.0% of consolidated outlays and 70.9% of consolidated receipts**, against a civilian-household-to-resident population ratio of 0.990.

## Housing allocation: does per capita under- or over-charge?

Subfunction 604, federal housing assistance of $70.0bn, is charged per capita in the central arm. Allocated instead by each record's share of the reported SPM capped housing subsidy, the union's R item moves from −$115.14bn to −$115.57bn, a difference of **−$0.43bn or −$10 per person**, and the common-age gap against whites moves from +$840 to +$703 per standardized person. So the per-capita convention **under-charges** the Mexican-origin groups for housing assistance, by $137 per standardized person in gap terms. The effect is real but an order of magnitude smaller than the choice of whether to charge general services at all.

## Two corrections to my own implementation

The researcher lane's verified CPS data dictionary caught two defects in my first build.

1. **Veteran status.** I had allocated function 700 over `VET_YN = 1`, receipt of veterans' payments, 2,385 records. The veteran-status item is `PEAFEVER = 1`, ever served on active duty, 6,936 records. Corrected.
2. **Federal pension.** I had used `DST_SC1/DST_SC2 = 2`. Those are retirement *distributions* on a different code set, where 2 is a union pension. The pension source fields are `PEN_SC1/PEN_SC2`, where 3 is a federal government pension. CPS carries no separately valued federal pension amount, only `PNSN_VAL`, the all-source total, so subfunction 602 is allocated by total pension income among people flagged with a federal source. **16.8%** of the dollars so allocated sit with people who also hold a non-federal pension, which bounds the over-attribution.

A third correction came from the researcher's classification note: OMB has no Medicaid subfunction and subfunction 551 is health care services, far broader. Function 550 is netted by NHEA 2023 federal Medicaid of $592.6bn, leaving $318.69bn charged per capita rather than the $56.95bn that netting 551 would have left.

## What the netting removes, so nothing is charged twice

| function | gross $bn | netted out | net charged $bn |
|---|---|---|---|
| 700 veterans | 325.6 | subfunction 703 VA hospital and medical care, already in the MEPS transport | 187.1 |
| 500 education | 306.4 | subfunction 501, federal K-12 aid already inside state per-pupil spending | 201.0 |
| 550 health | 911.3 | NHEA federal Medicaid, already in the MEPS transport | 318.7 |
| 600 income security | 670.5 | subfunctions 603, 605, 609 already in the CPS transfer fields, and 602, charged separately | 92.3 |
| 750 justice | 83.8 | nothing; the BOP Mexican-national share of 753 goes to Mexico-born noncitizens per head | 83.8 |

Two more outside item R. ICE ERO total already contains custody, transport, alternatives to detention and fugitive operations, so the enforcement item adds ERO total, EOIR and appropriated USCIS and never the custody line on top. Federal housing assistance is carried whole as subfunction 604, so housing was removed from the under-reporting item.

## Transfer under-reporting

The researcher published admin/survey ratios that are reciprocals of the survey/administrative coverage ratios. The builder re-derives each from the published coverage vector and refuses to run if any inversion fails; all five agree exactly.

| program | published coverage | admin/survey | applied | national increment $bn |
|---|---|---|---|---|
| SNAP | 0.531 | 1.8832 | yes | +40.74 charged |
| TANF | 0.500 | 2.0000 | yes | +7.76 charged |
| SSI | 1.019 | 0.9814 | yes, as a credit | −1.09 charged |
| UI | 0.577 | 1.7331 | yes | +18.38 charged |
| Social Security | 0.919 | 1.0881 | **no** | 108.04 **not** charged |
| housing | null | null | no | carried whole as subfunction 604 |

Social Security is excluded because the brief applies it only when its admin/survey ratio is below 1. That is the largest discretionary exclusion in the account: applying it would charge $108.04bn nationally and move the union endpoint to roughly −$264bn.

## Dropped for want of a verified parameter

- **Item D**, the district cost-to-serve differential, is not priced; the district F-33 file and the Common Core of Data membership-by-race file were not reduced to a verified per-state differential. Its ELL arm is also unbuilt: the ELL weights were verified but the ACS share of 5–17-year-olds with limited English by group and state, which the arm multiplies, was not.
- **Item S** is priced for six states from individual verified budget lines: New York $3.000bn, California $2.800bn (adults 26–49 only, a partial-population floor), Illinois $0.538bn, Oregon $0.363bn and Washington $0.036bn (both biennial, halved to an annual rate), Colorado $0.050bn. Minnesota, Massachusetts, Colorado's children's expansion and California's all-ages total were not verified and are not priced. The 50% already-inside-MEPS split is the brief's stated convention, not a parameter; the 0% and 100% arms bracket it.

Nothing else was dropped and no item was zeroed by substituting a value.

## What remains unpriced

- OMB function 920 allowances and function 950 undistributed offsetting receipts.
- Federal and state capital stock other than school capital; state and local capital outlay outside K-12.
- The CPS reported housing-subsidy base itself, which sits outside the account's selected non-cash transfers.
- Social Security under-reporting, by the brief's rule, quantified above.
- Deficit finance. The account charges outlays, not the tax burden that would fund them.
- Emigration, mortality and every lifetime or dynamic margin.

## Uncertainty, and what it does not cover

Standard errors are the CPS 160-replicate SDR only: $8.81bn on the union absolute endpoint, $302 on the complete common-age gap against whites, $12.0bn on the complete age-matched total. The base account reproduces the upstream lane's CPS-only error of $7.473981bn exactly. The upstream MEPS donor error of $7.71bn is **not** carried and item M's own donor uncertainty is not propagated at all. The institutional add enters with no standard error and is flagged. None of this covers the arms, which span $461bn and dominate every sampling interval by a factor of fifty.

The institutional add carries definitional mismatches recorded in `audit.json`: its white reference is native non-Hispanic white rather than third-plus, its US-born Mexican group does not condition on parents' birthplace, and its union population is 39.38M against the CPS union's 40.90M.

## Executed gates: 36 of 36

New in this pass: the partial common-age and age-matched gaps must reproduce the upstream `estimates.csv` values (8 checked); the complete gaps must equal the base plus the summed item contributions for both references; the national account lines must sum to the reported position; the national residual must be finite, reported and not near zero; and the brief's step-12 endpoint must remain visible alongside step 13.

Carried over: gate 0 reproduces the upstream union absolute of +$50,238,214,249 to the dollar before any item is computed; the reused constructions still match the sibling lane's published $3,738–$4,240 band and $5,341 figure; the cached OMB Table 3.1 agrees with the fetched Table 3.2 parameters on all 16 shared functions; every admin/survey ratio is the reciprocal of its published coverage ratio; flat per-capita items reconcile to the population ratio and cancel from the age-standardized gap.

## Verification

```
cd /Users/alien/Projects/immigration-research && OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/absolute_ledger.py \
  --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json
EXIT=0
```

```
[inversion] ssi: published coverage 1.019 -> admin/survey 0.9814 (recomputed 0.9814) -> PASS
[inversion] ui: published coverage 0.577 -> admin/survey 1.7331 (recomputed 1.7331) -> PASS
[inversion] social_security: published coverage 0.919 -> admin/survey 1.0881 (recomputed 1.0881) -> PASS
[stage] replicate aggregation
[gap anchor] 8 upstream partial gaps reproduced
[national] account position -966.7bn vs consolidated -2,590.8bn, residual -1,624.1bn; outlay coverage 0.630, receipt coverage 0.709
[sibling] general_services_per_person_vs_residual_agg_published_range: 3,904.78 -> PASS
[sibling] federal_public_goods_per_person_rebased_to_the_2023_denominator: 5,340.81 -> PASS

=== union waterfall (central arms) ===
 step item     item_bn  cumulative_bn    se_bn                          flag
    0 base    0.000000      50.238214 7.473981                   cps_records
    1    G -165.969959    -115.731744 7.789012                   cps_records
    2    K  -22.730762    -138.462506 7.963317                   cps_records
    3    D    0.000000    -138.462506 7.963317 dropped_no_verified_parameter
    4    U   -9.442781    -147.905287 8.076536                   cps_records
    5    I   -4.738353    -152.643640 8.149480                   cps_records
    6    M  -35.150381    -187.794021 8.295461                   cps_records
    7    N  -19.068559    -206.862581 8.295461            external_add_no_se
    8    E   -2.716778    -209.579359 8.305865                   cps_records
    9    C   34.549967    -175.029392 8.705472                   cps_records
   10    X   37.721846    -137.307546 8.585569                   cps_records
   11    R -115.139252    -252.446798 8.784940                   cps_records
   12    F    0.000000    -252.446798 8.784940           central_arm_is_zero
   13    S   -1.485181    -253.931979 8.808802                   cps_records

arms matrix union absolute range: -548.37bn to -87.04bn over 144 combinations
break-even m* = 0.12044407952168636
items dropped for want of a verified parameter: ['D', 'S(states without a verified line)']
PASS: 168 item rows, 84 waterfall rows, 144 arm combinations, 21 marginality points
```

```
cd /Users/alien/Projects/immigration-research && OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
  infra/immigration-fiscal/ledger_absolute_2026_09_17/check_gates.py
EXIT=0

  PASS  artefact_present:items_by_group.csv                                      
  PASS  artefact_present:waterfall.csv                                           
  PASS  artefact_present:arms_matrix.csv                                         
  PASS  artefact_present:marginality_curve.csv                                   
  PASS  artefact_present:complete_gaps.csv                                       
  PASS  artefact_present:complete_gaps_by_item.csv                               
  PASS  artefact_present:national_reconciliation.csv                             
  PASS  artefact_present:audit.json                                              
  PASS  gate0_passed                                                             residual $0.00
  PASS  gate0_matches_live_upstream_estimate                                     audit 50,238,214,249 vs upstream 50,238,214,249
  PASS  waterfall_starts_at_the_gated_absolute                                   +50.23821bn
  PASS  parameters_all_verified                                                  all consumed parameters are verified
  PASS  national_total_reconciliation                                            G|nominal2022=1.0094; G|deflated2024=1.0094; K|central=0.9244; E|stock=1.0000; C|wage25_capital75=0.9975; X|per_capita=0.9901; F|per_capita=0.9901
  PASS  flat_items_reconcile_to_the_population_ratio                             population ratio 0.99005 over 2 flat items
  PASS  common_charge_cancellation                                               X|per_capita=4.97e-16; F|per_capita=-5.74e-16
  PASS  replicate_se_finite                                                      
  PASS  reused_constructions_match_their_source_lane                             general_services_per_person=3,905; federal_public_goods_per_person_rebased_to_the_2023_denominator=5,341
  PASS  admin_survey_ratios_are_the_reciprocal_of_the_published_coverage_ratios  snap 1/0.531=1.8832; tanf 1/0.5=2.0; ssi 1/1.019=0.9814; ui 1/0.577=1.7331; social_security 1/0.919=1.0881
  PASS  omb_cache_agrees_with_the_fetched_parameters                             16 functions compared
  PASS  items_table_finite                                                       168 rows
  PASS  union_equals_the_sum_of_the_three_targets                                max |union - sum of parts| = 2.842e-14 bn
  PASS  waterfall_steps_add_up                                                   every step matches
  PASS  waterfall_endpoint_is_additive                                           union -253.9320bn vs parts -253.9320bn
  PASS  arms_matrix_contains_the_waterfall_endpoint                              -253.9320bn vs -253.9320bn
  PASS  arms_matrix_is_the_full_grid                                             144 rows, grid 144
  PASS  partial_gaps_reproduce_the_upstream_estimates                            8 common-age gaps checked against estimates.csv
  PASS  complete_gaps_are_the_base_plus_the_item_contributions                   8 group-reference pairs add up
  PASS  complete_gaps_cover_both_references                                      8 rows over ['all_native', 'third_plus_nh_white']
  PASS  national_account_lines_sum_to_the_reported_position                      lines -966.7bn vs reported -966.7bn
  PASS  national_residual_is_reported_and_finite                                 residual -1,624.1bn, outlay coverage 0.630, receipt coverage 0.709
  PASS  national_residual_is_a_real_unforced_quantity                            the residual is reported, never solved for; a residual near zero would mean it had been forced
  PASS  brief_final_step_endpoint_still_reported                                 step 12 cumulative -252.45bn
  PASS  marginality_grid                                                         21 points from 0.0 to 1.0
  PASS  marginality_curve_is_linear_in_m                                         
  PASS  break_even_m_star_consistent                                             m* = 0.120444, union absolute there = +1.42e-14 bn
  PASS  marginality_endpoint_matches_the_waterfall                               m=1 gives -253.9320bn, waterfall ends at -253.9320bn

36/36 gates passed
```

---

## Revision, September 18, 2026 — items D and P are now priced

The result above is the account **without** the district cost-to-serve
differential and **without** non-school state and local capital. It is
reproducible from the current code with `--off D --off P`, which returns the
step-13 endpoint of **−253.931979bn** to the dollar. The full extension result,
with its build, its gates and its one deviation from the brief, is in
[`RESULT_extension.md`](RESULT_extension.md).

**What changed.** Item D charges each state's Hispanic-minus-all per-pupil
differential to Mexican-origin public pupils aged 5-17 and its white-minus-all
differential to the third-plus non-Hispanic white reference, from the Census F-33
FY2024 district finance file joined to the NCES CCD LEA membership file for
school year 2023-24. Item P charges the state and local capital outlay that
neither item K nor item G already carries, per capita by state of residence.

**Concept affected: the completeness of the absolute account.** Both items were
listed as gaps in the original result. Item D is the only item in the account
whose sign differs between the target groups and the white reference: Hispanic
pupils attend districts spending $474 per pupil above their state's mean while
white pupils attend districts $624 below it, so D is a cost for the Mexican-origin
union and a receipt for the white reference. That makes it a gap-widening item of
roughly item K's size. Item P is close to a common per-capita charge and moves
the gap by $14 per standardized person.

| quantity | this result (D and P off) | with D and P |
|---|---|---|
| union complete absolute | −253.93bn | **−263.22bn** |
| union complete common-age gap vs 3rd+ NH white, $/person | −7,095 (302) | **−7,224 (302)** |
| union complete age-matched gap vs white, $bn | −354.3 (12.0) | **−361.1 (12.0)** |
| union complete common-age gap vs all natives, $/person | −4,928 (257) | **−5,023 (257)** |
| arms matrix range, 144 combinations | −548.37 to −87.04 | **−557.67 to −96.33** |
| break-even marginality dial m\* | 0.1204 | **0.1167** |
| national account position | −966.7bn | −1,007.4bn |
| national residual, unpriced or coverage | −1,624.1bn | −1,583.4bn |
| outlay coverage of the consolidated budget | 0.6296 | **0.6341** |

The waterfall now runs G, K, P, D, U, I, M, N, E, C, X, R, F, S, so the brief's
final step F is step 13 and item S is step 14. The sign of the completed account
is unchanged and the arms matrix still never turns positive.

**The deviation.** The extension brief defined item P as total state and local
capital outlay less elementary-and-secondary capital outlay. That double-counts
$239.5bn, because the Census of Governments functional lines carry each
function's capital inside the function total and item G already charges every
function it retains. The briefed quantity is built as the `briefed_gross` arm and
reported; the central arm charges only the $47.0bn nothing else charges.


## Revisions — fiscal repair, September 19, 2026

Grant/fee ownership, veterans and enforcement double counting, real discounting and age-profile propagation were corrected. The $263bn/$2,246/89% and flat-shift lifetime headlines are superseded; the birth-policy inference remains withdrawn. See [current results](../../../research/immigration-yearly-lifetime-cost-repair-2026-09-19.md) and its linked decision record.

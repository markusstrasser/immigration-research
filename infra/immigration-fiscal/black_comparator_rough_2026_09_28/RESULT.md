**Verdict:** Group-specific mortality materially lowers the Black comparator; exact full-case imputation symmetry remains unresolved. New tables correct production symmetry, status-only receipt rules, comparator pension eligibility/frame and scalar coverage, while preserving the frozen v7 and old rough outputs as controls.
<!-- P7 symmetric comparator evidence -->

## P7 comparator audit, 2026-10-14

All dollar figures below are billions a year, personal allocation, v7 specifications 16 / 11. These are modeled annual removal/accounting costs, not observed lifetime contributions. Each row changes only its named policy from the current raw rough comparator. The identified union has 39.712M people; its lineage overlay brings it to 42.752M. White A1 uses that lineage count; Black keeps its own 41.954M count. [DATA: frozen case meta.lineage.counts; symmetric_results_oct14.csv/population]

| One change from current rough central | Rough lineage change | A1 white change | Black change, own count |
|---|---:|---:|---:|
| production_own | 0.000 / 0.000 | -0.391 / -0.257 | -0.677 / -0.445 |
| production_zero | 11.910 / 7.834 | 0.000 / 0.000 | 0.000 / 0.000 |
| source_payroll_proxy | 0.027 / 0.027 | -0.023 / -0.023 | -0.062 / -0.062 |
| status_rules_fixed_union_benefits | 14.416 / 14.416 | -2.683 / -2.683 | -0.456 / -0.456 |
| status_rules_coupled_accrual | 17.932 / 17.932 | -2.683 / -2.683 | -0.456 / -0.456 |
| mortality_group | 0.000 / 0.000 | -1.979 / -1.979 | -19.611 / -19.611 |
| accrual_row4 | 0.000 / 0.000 | 0.000 / 0.000 | -0.000 / -0.000 |
| pension_symmetric_frame_status | 0.000 / 0.000 | -0.003 / -0.003 | -2.149 / -2.149 |
| mortality_symmetric_frame_status | 0.000 / 0.000 | -1.982 / -1.982 | -21.524 / -21.524 |
| combined_rules_only | 17.932 / 17.932 | -5.081 / -4.948 | -22.723 / -22.491 |
| combined_zero_production | 29.841 / 25.766 | -4.690 / -4.690 | -22.046 / -22.046 |

[CALCULATION: symmetric_comparators_oct14.py → derived/symmetric_results_oct14.csv. The $5bn review bar is evaluated in the CSV exceeds_5bn field, independently at each end; a comparator delta does not alter the frozen headline.]

The own-production changes are below the bar; zero production for everyone moves the lineage over it at both ends. Mortality is over the bar for Black, below it for whites. Status-only receipt changes on the union exceed the bar; their fiscal effect depends on whether its already-earned pension liabilities are fixed or coupled to payer dollars. Source payroll proxy alone is a diagnostic, not an adopted correction. Row-4-only comparator ratios are below the bar. [CALCULATION: table and CSV]

## Combined table and comparison denominators

| Rule | Rough lineage cost | A1 white cost | Black cost, own count | White gap vs rough / case lineage, low | Black minus rough / case lineage, low |
|---|---:|---:|---:|---:|---:|
| legacy_raw | 315.765 / 397.795 | -196.385 / -83.848 | 422.746 / 501.121 | 512.150 / 535.937 | 106.980 / 83.194 |
| production_own | 315.765 / 397.795 | -196.776 / -84.106 | 422.068 / 500.675 | 512.541 / 536.328 | 106.303 / 82.516 |
| production_zero | 327.675 / 405.629 | -196.385 / -83.848 | 422.746 / 501.121 | 524.060 / 547.846 | 95.070 / 71.284 |
| combined_rules_only | 333.697 / 415.726 | -201.466 / -88.796 | 400.022 / 478.629 | 535.163 / 541.018 | 66.325 / 60.470 |
| combined_zero_production | 345.607 / 423.561 | -201.075 / -88.539 | 400.699 / 479.075 | 546.682 / 552.537 | 55.093 / 49.238 |

Both-end comparison columns are in symmetric_comparisons_oct14.csv. The old white gap 512.150 / 481.643 and Black-minus-lineage 106.980 / 103.326 use the rough lineage, not the frozen case. Holding the exact case numerator instead gives 535.937 / 507.498 and 83.194 / 77.472 before any comparator status correction. Those latter values alone reproduce the reviewer’s claimed “case-rule” gap, so they are not evidence of a newly executed all-group status rule. [CALCULATION: legacy_raw comparison rows]

**Full row 13 remains unresolved.** The source averages matched hot-deck shares and a separate base × matched / pooled share ratio. That ratio is not additive over group partitions. No unique conserved all-group record vector is declared by the source. The new status arm applies the same origin-specific on-books flag/rules to every group’s records, using wage and a separate statutory self-payroll key. Income tax applies status after the existing personal IRS/CBO rake and renormalizes on row 4; it does not preserve the rake margins or reproduce the whole frozen aggregate imputation stack. All combined rows therefore carry full_row13_symmetric=false. A full matched replay was not substituted for the undeclared ratio extension. [DATA: combine_onbooks_lane.assemble; status_keys_oct14.build; ASSUMPTION: status after the carrier rake]

Pension rows with basis=symmetric also apply the same all-origin source status and statutory payer definition to comparator eligibility and exclude military members. Pure mortality_group retains the old source frame to isolate the life-table change. The prior Black frame included military people and flagged unauthorized status only for Mexico-born people; those defects are independently corrected in the combined arm. General controls retain the original frames. The union’s frozen pension numerator remains fixed in the isolated status arm; the coupled arm uses exact engine cash/accrual payer-dollar rates including post-pension edits. Never multiply new payroll by the old R9 ratio calibrated to the raw payroll denominator. [DATA: mortality_comparators.symmetric_frame; status_keys_oct14.engine_accrual_rates]

## Population standardization

| Rule, accrual | Black own cost | At lineage count | Scaling increase | Per Black person |
|---|---:|---:|---:|---:|
| legacy_raw | 422.746 / 501.121 | 430.784 / 510.649 | 8.038 / 9.528 | $10,076 / $11,944 |
| combined_rules_only | 400.022 / 478.629 | 407.628 / 487.730 | 7.606 / 9.101 | $9,535 / $11,408 |

This is linear accounting standardization at fixed per-person amounts. It is not a new CES counterfactual for removing a larger group. All own/scaled populations and per-person values are printed in the Black lane’s symmetric_population_oct14.csv; every per-person equality passes at 1e-9. [CALCULATION: that file]

## White measures for quoting

| Arm, A1 whites | Allocated balance | Responsive budget cost | Resource cost incl. capital and production | Contribution to others |
|---|---:|---:|---:|---:|
| legacy_raw | -13.907 / -13.907 | -230.524 / -141.823 | -196.385 / -83.848 | 196.385 / 83.848 |
| combined_rules_only | -9.217 / -9.217 | -235.214 / -146.514 | -201.466 / -88.796 | 201.466 / 88.796 |

Allocated balance is all assigned receipts less assigned spending, before response assumptions. Responsive budget cost is spending saved less receipts lost. Resource cost adds the imputed return on public capital and subtracts the modeled production benefit. Contribution to others is its sign reversal, not the allocated balance. Neither capital return nor pension accrual is current borrowing. A2–A4, both bases and all arms are in symmetric_white_measures_oct14.csv. Exact full-row13 “case rules” is not an available measure. [CALCULATION: CSV fields; FRAMING-SENSITIVE: contribution as removal resource surplus]

## Hispanic mortality arm beside the case

The identified-union 2026 payable/net Hispanic-proxy change is +13.931 at both ends. The added-profile extension is bounded at +0.957–0.962; the whole-lineage change is +14.888–14.893. The case would be 354.440–354.445 at the low end and 438.537–438.542 at the high. The narrow interval bounds missing added pension-dollar splits, not mortality uncertainty. [CALCULATION: symmetric_hispanic_arm_oct14.csv; ASSUMPTION: pooled Hispanic tables for actual lineage members, including those priced with white monetary rates]

The quoted +19.6 is stale scheduled-benefit prose. The preserved executed 2025 payable/net arm is +14.897 / 14.270 (pension_accrual_2026_09_28/derived/case_beside.csv); neither is an executed 2026 whole-lineage number. New added-profile rows use the case’s measured band mixes and full-precision Hispanic/general factors. Their unknown dollar split is bounded, never typed or invented. [DATA: pension lane RESULT historical and final tables; mortality CSV added_profile rows]

## Gates, sampling and remaining limits

- Existing raw rough outputs reproduce before any change, at their 5e-5bn printed precision; frozen engine formula and lineage addition close at 1e-9bn.
- The principal union production terms reproduce at 1e-8bn; all 161 skill-income columns conserve their national sums at 1e-6bn, ACS cells at 1e-6 persons. Production uses official pwwgt0; fiscal rough keys use rounded MARSUPWT/100. The count normalization is kept separate from the principal production control.
- All 24 status line/rule national closures pass at 1e-6bn; record IDs, duplicates/missing joins and scenario-weight conservation fail closed.
- NVSS 2024 sex-specific primary spreadsheets are pinned in inputs/pins.json, parsed directly, and checked for year/sex/complete ages. The general Note 2025.7 denominator stays general; group mortality changes the 2026 numerator. Medicare qualification stays observed; survival to 65 is already inside the pension PV.
- Every scalar in both the full and identified dumps has a declared comparator policy. Unknown, duplicated or full-only lineage scalars stop; summary scalars are never added as a second cost.
- Production SDR SEs are in symmetric_results_oct14.csv; status receipt-shift conditional SDR SEs are in symmetric_status_sampling_oct14.csv. These hold count, flags, carrier and requested age mix fixed; they do not estimate complete fiscal uncertainty, reimputation uncertainty or life-table uncertainty.

[CALCULATION: executable gates and focused tests. SOURCE: NVSS primary URLs in each lane’s inputs/pins.json.]

| Conditional status receipt shift, same both ends | Estimate | Paired SDR SE |
|---|---:|---:|
| mex, 39.712M | -14.416 | 1.408 |
| blk, 41.954M | +1.041 | 0.391 |
| w3, 42.752M | +5.453 | 0.382 |

Comparator mixed-unit credit crossings are deferred: no comparator event-level crossing was measured, and the union’s 5b term cannot be scaled by head count. The new combined table preserves the union term and carries no fabricated comparator term. An eligibility- and frame-consistent rerun of the crossing source is required; the reviewer’s guessed range is not source evidence. Full row13 is deferred because the principal declares no conserved comparator policy for its nonlinear ratio, not because of execution cost. [UNVERIFIED: comparator crossings; DATA: existing v7 R6 policy]

Medical/justice and other rough proxies remain the inherited declared keys; this does not turn rough comparisons into observed causal group effects. The LLM research instrument can affect framing; numeric claims here rest on primary files, executable controls and an independent code review. [INFERENCE; DATA: existing lane rules; notes/llm-bias-caveat.md]

## Reproduce

```sh
node infra/immigration-fiscal/white_replacement_2026_09_28/production_state_oct14.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/accrual_white.py --mortality
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/accrual_black.py --mortality
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/status_keys_oct14.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/symmetric_comparators_oct14.py
uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/render_symmetric_result.py
```

The first inspected build alone uses --pin; reruns verify the pins without rewriting them. Legacy run_oct14.sh remains the historical rough-output route. New live sensitivity commands are above; old output files are preserved, never refreshed from a new policy.

## Execution log

2026-10-14T12:21:58Z (from date): initial integrated build exited 0 in 21.435s, peak 2.243GB; expanded status/mortality controls and independent review follow. Final check receipts and exact changed-path manifest are in the assigned comparators-result.md. Times/memory use Python perf_counter/getrusage, not time -l.

## Preserved earlier results

**Verdict:** A rough re-key of the adopted September 27 case to non-Hispanic Black residents puts the cost of removing the group at **$549bn (low end) to $595bn (high end) a year**, or **$13,100–14,200 per member**. The engine's Mexican-origin figure is $7,900–9,500, so the Black figure is **1.5–1.7× per member**; against the same rough method run on the Mexican-origin group it is 1.6–1.7×. The normalized gap, which charges each group its population share of the all-resident deficit, is **−$468bn, −$11,165 per member**, against the engine's −$6,700 to −7,200 for the Mexican-origin group. The Black gap is larger on Medicaid, police, courts and prisons, and welfare. It is smaller on Social Security and Medicare, because the group is older, and on income taxes, because its earnings per adult are higher. The same rough method comes out 3–7% below the engine on the Mexican-origin cost and 7–15% below on its gap, so the Black figures are more likely low than high. Offences by non-Hispanic Black offenders cost their victims **$185bn** in 2024 at the victim lane's prices, including **$73bn to non-Black victims**. The national total is $508bn. This is a comparator for a question the operator asked, not an engine run and not part of any headline. [CALCULATION: `rekey.py`, `victim_cost.py` → `derived/`]

Model: claude-opus-5-5

Lane `infra/immigration-fiscal/black_comparator_rough_2026_09_28/`, written 2026-09-28 19:22 JST (from `date`) from the lead's scratch runs of 17:45 and 18:40, ported unchanged.

## Budget re-key

$bn a year, 2024 dollars. Low end is spec 48 (shared allocation, GDP normalization, general government 0.60, 2% return on capital); high end is spec 11 (personal allocation, cash normalization, 0.85, 3%). [DATA: `derived/rekey_summary.csv`]

| | Mexican-origin, engine | Mexican-origin, rough | Non-Hispanic Black, rough |
|---|---:|---:|---:|
| Population (CPS ASEC 2025) | 40.90m | 40.90m | 41.95m |
| Cost of removal, low / high | 321.8 / 387.4 | 310.8 / 359.0 | **549.0 / 595.2** |
| per member | $7,869 / $9,472 | $7,599 / $8,779 | **$13,086 / $14,188** |
| of which capital return | 33.8 / 55.7 | 33.8 / 55.2 | 34.5 / 56.8 |
| of which production gain (subtracted) | 13.3 / 8.8 | 13.3 / 8.8 | 0 |
| Normalized gap, low / high | −273.3 / −296.4 | −253.8 / −252.1 | **−468.4 / −468.4** |
| Cost without Social Security, Medicare and their payroll taxes | 364.4 / 423.8 | 355.2 / 403.5 | 477.4 / 523.6 |

The last row removes Social Security, Medicare, railroad retirement and pension guaranty spending, and the payroll taxes and premiums that fund them. For the young Mexican-origin group that raises the cost, since it pays more into those programs than it draws. For the Black group it lowers it, since it draws $72bn more than it pays in.

**Gap by program, low end.** Negative means the group pays in less, or draws more, than its population share of the national line. [DATA: `derived/rekey_gap_by_program.csv`]

| Program group | Mexican-origin, engine | per member | Non-Hispanic Black, rough | per member |
|---|---:|---:|---:|---:|
| Income taxes | −216.9 | −$5,304 | −174.4 | −$4,157 |
| Payroll taxes and Medicare premiums | −69.1 | −$1,690 | −43.5 | −$1,036 |
| Sales, excise, customs, fees | −46.9 | −$1,147 | −26.9 | −$640 |
| Capital, property, production taxes | −131.5 | −$3,215 | −112.2 | −$2,674 |
| Social Security and Medicare | +199.2 | +$4,871 | +62.1 | +$1,481 |
| Medicaid | −3.0 | −$73 | −63.5 | −$1,515 |
| Schools and colleges | −45.1 | −$1,103 | −26.9 | −$641 |
| Police, courts, prisons | −7.2 | −$177 | −46.3 | −$1,104 |
| SNAP, SSI, housing, cash aid, credits, other welfare | −25.0 | −$611 | −69.7 | −$1,662 |
| Veterans and military medical | +14.4 | +$353 | −12.3 | −$293 |
| Per-head lines: government, defense, interest, roads | +57.9 | +$1,415 | +45.1 | +$1,075 |
| **Total** | **−273.3** | **−$6,682** | **−468.4** | **−$11,165** |

### Method

The engine is dumped at both ends by `engine_lines.cjs` into `derived/engine_lines.json`: every national line, the Mexican-origin amount, the response and the capital components, with the two methods averaged. `rekey.py` then charges each national line to a group by a key share and applies the engine's response to it.

- **CPS ASEC 2025 keys** (income year 2024), civilian non-institutional plus children under 15, run on the Mexican-origin union from `admin_benefit_keys_2026_09_24/cps_keys.py` and on non-Hispanic Black (`PEHSPNON==2 & PRDTRACE==2`, Black alone):
  - federal and state income tax at the tax unit, split equally among members;
  - OASDI earnings to the 2024 cap of $168,600 and HI earnings;
  - consumption as household income^0.7 [INFERENCE];
  - capital income (interest, dividends, rent) and property value;
  - program dollars for Social Security, SSI, unemployment, veterans, workers' compensation and cash assistance;
  - SPM-unit SNAP, housing and energy subsidies split per member;
  - pupils aged 5–17 and college enrollment.
- **Income taxes.** CPS misses the top tail. The group's CPS tax dollars are charged against the national line rather than scaled up to it.
- **Per-head lines** take the engine's own per-head share, scaled to the group by its CPS population.
- **Medical lines, Black group.** MEPS 2024 (`RACETHX==3`) shares of each payer's spending: Medicare 10.3%, VA 15.3%, TRICARE 11.8%, other public 5.4% [DATA: `derived/keys.csv`]. Medicaid blends T-MSIS 2023 long-term services and supports at 20.865% of LTSS spending ($47.7bn of $228.6bn) [DATA: `ltss_share_2026_09_23/derived/taf_race_ethn.csv`] with MEPS's 18.3% for the rest. The LTSS weight is $228.6bn over total Medicaid spending of $870bn [TRAINING-DATA]. The blend is 19.0%.
- **Justice, Black group.** The rule is the adopted justice lane's (`cj_use_allocation_2026_09_23`):
  - prisons at the non-Hispanic Black share of state prisoners, 33.1% (SPI 2016) [DATA: `research/immigration-crime-race-ethnicity-2026-09-05.md`];
  - non-border police half by arrests, half per head;
  - courts 60% by arrests, 40% per head;
  - arrests at 26.6%, the Black share of all 2019 arrests (FBI Table 43A) [TRAINING-DATA];
  - the rest per head.

  The weighted share is 21.3%.
- **Refundable credits.** 45% of the line is EITC and ACTC, keyed on CPS credits; the rest is keyed per head [INFERENCE].
- **Schools.** K-12 is 74% of education services [INFERENCE], keyed on pupils; the rest is keyed on college enrollment. The engine's Mexican-origin-specific repricing lines (school reprice, college re-key, lane constants) are zero for the Black group.
- **Capital return.** The engine's stocks, responses and rate are applied with the group's pupil, HI-earnings, justice, health or per-head key.
- **Production gain.** None for the Black group; removal of a native-born group is not scored for complementarity here.
- **Old-age lines.** Keyed as above; see the last table row.

**Calibration.** On the Mexican-origin group the same keys give $310.8bn against the engine's $321.8bn at the low end (−3.4%) and $359.0bn against $387.4bn at the high end (−7.3%). The gap comes out 7.1% and 15.0% low. The rough keys miss the engine's hot-deck admin keys, its allocation arms and its lane-specific repricing.

### Limits

- **Allocation arms.** The Black gap is the same at both ends because rough key shares do not change with the engine's allocation arm; only responses and the capital rate move the cost.
- **CPS program dollars.** CPS under-reports SNAP, SSI and cash assistance. Shares are unaffected only if under-reporting is the same across groups, which is not checked here.
- **Missing lines.**
  - Uncompensated care is not keyed separately.
  - Shelter and the dataset-audit lines of the September 24 case are not keyed separately.
  - Justice uses 2016 and 2019 shares.
- **Scope.** Black alone; multiracial Black residents are outside the group.

## Victim cost of violent offences

2024 victimisations and homicides at Miller et al. 2021 victim-only prices in 2024 dollars, the victim lane's central price set [DATA: `crime_victim_cost_2026_09_23/derived/unit_costs_victim_only_2024usd.csv`]. Full cost includes quality of life; tangible is medical, work and property loss. [DATA: `derived/victim_cost_summary.csv`, `derived/victim_cost_by_offence.csv`]

| Offences by non-Hispanic Black offenders | Non-Black victims | Black victims | All victims |
|---|---:|---:|---:|
| Full cost, $bn | **72.9** | 112.4 | **185.2** |
| of which homicide, $bn (deaths) | 16.3 (1,820) | 83.6 (9,322) | 99.9 (11,142) |
| Tangible cost, $bn | 10.2 | 25.2 | 35.4 |
| Non-fatal victimisations | 1.15m | 0.57m | 1.72m |

Non-Black victims by offence: rape and sexual assault $21.9bn (104,017), aggravated assault $17.2bn (210,598), homicide $16.3bn (1,820), simple assault $15.2bn (735,204), robbery $2.3bn (102,475).

**National.** Every 2024 victimisation and homicide at the same prices comes to **$507.9bn**: 20,162 homicides and 6.67m non-fatal victimisations. Black offenders account for 36.5% of that cost and 55.3% of homicides. The Mexican-origin union's cost to others is $28.9bn at the victim lane's central [DATA: `crime_victim_cost_2026_09_23/derived/arms.csv`].

**Method.**
- **Non-fatal.** NCVS 2024 victimisations by victim race and offence [DATA: `ncvs_victim_offender_2026_09_18/derived/ndash_rate_by_victim_race.csv`] × P(offender Black | victim race) from the pooled 2022–2024 matrix, with unknown offenders spread in proportion [DATA: `matrix_pooled_2022_2024.csv`].
- **Homicide.** CDC WONDER 2024 victims, not-stated allocated, × SHR 2024 P(offender non-Hispanic Black | victim group) [DATA: `crime_victim_cost_2026_09_23/derived/`].
- **Second arm.** The 2019 matrices by crime type give $73.3bn and $188.1bn.

**Limits.**
- NCVS offender race is the victim's perception, and the pooled shares cover all violent crime rather than each offence.
- NCVS excludes victims under 12 and commercial robbery.
- The Mexican-origin lane checked NCVS against police records for Hispanic offenders; that check is not run here for Black offenders.

## Who the groups are

CPS ASEC 2025, income year 2024. Household size is person-weighted. [DATA: `derived/cps_profile.csv`]

| | Mexican-origin union | Non-Hispanic Black | All residents |
|---|---:|---:|---:|
| Population | 40.90m | 41.95m | 336.73m |
| Under 18 | 29.6% | 24.3% | 21.7% |
| 65 and over | 7.7% | 14.3% | 18.3% |
| Household size | 4.03 | 3.19 | 3.26 |
| Income per person | $29,230 | $35,726 | $48,853 |
| Working, ages 25–64 | 78.8% | 76.6% | 80.3% |
| Earnings per adult, 25–64 | $44,477 | $48,324 | $64,473 |
| Earnings per worker, 25–64 | $56,460 | $63,113 | $80,259 |

## Reproduce

From the repository root; `rekey.py` and `victim_cost.py` read the CPS ASEC 2025 zip in `gen_ledger_extension_2026_09_16/_cache/` and MEPS 2024 under `sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/`.

```sh
node infra/immigration-fiscal/black_comparator_rough_2026_09_28/engine_lines.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/rekey.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/victim_cost.py
```

## v4 case (sept29), 2026-09-29

claude-opus-5-5

**Status, 2026-09-29 21:50 JST (from `date`): done; every gate passed; nothing committed (the lead commits).** The run was resumed after the machine rebooted at 20:51 JST. In this run the sept29 steps and every gate, both `rerun_lane.py` passes included, were rerun, and three outputs were added: `rule_alternatives_sept29.csv`, `attribution_sept29.csv` and `attribution_buckets_sept29.csv`. The log is at the end of this section.

**Verdict (sept29).** On the adopted v4 case the rough re-key puts the cost of removing the 41.95M non-Hispanic Black residents at **$542.1bn (spec 48) to $590.1bn (spec 11) a year** on the case's accrual basis, or **$12,921 / 14,064 per member**. The engine's Mexican-origin union costs **$9,353 / 10,950 per member**: the case's $371.4146 / 434.8410bn over the 39,712,493 people the account prices. The Black figure is therefore **1.38× / 1.28× the Mexican-origin figure per member**. Against the same rough method run on the union ($9,455 / 10,691) it is 1.37× / 1.32×. On the September 27 case (ladder 259) it was $549.0 / 595.2bn, and 1.66× / 1.50× the engine's union per member. [CALCULATION: `rekey_sept29.py` → `derived/rekey_summary_sept29.csv`]

| $bn a year, spec 48 / 11 | Mexican-origin, engine | Mexican-origin, rough | Non-Hispanic Black, rough |
|---|---:|---:|---:|
| Persons (the per-member denominator) | 39,712,493 | 39,712,493 | 41,954,494 |
| **Cost of removal, accrual basis (the case)** | 371.4 / 434.8 | 375.5 / 424.6 | **542.1 / 590.1** |
| per member | $9,353 / 10,950 | $9,455 / 10,691 | **$12,921 / 14,064** |
| NH Black per member over this column | 1.38 / 1.28 | 1.37 / 1.32 | |
| Cost of removal, cash set (pension switch off) | 294.7 / 361.8 | 294.9 / 344.0 | 525.8 / 573.8 |
| per member | $7,421 / 9,111 | $7,425 / 8,662 | $12,532 / 13,676 |
| NH Black per member over this column | 1.69 / 1.50 | 1.69 / 1.58 | |
| Normalized gap, cash set | −270.0 / −292.9 | −264.5 / −262.8 | −471.2 / −471.2 |
| per member | −$6,798 / −7,375 | −$6,659 / −6,616 | −$11,230 / −11,230 |
| Cost without Social Security, Medicare and their payroll taxes, accrual basis | 338.6 / 399.3 | 337.8 / 386.9 | 460.2 / 508.2 |
| of which capital return | 34.4 / 57.2 | 34.5 / 56.8 | 36.9 / 60.5 |
| of which production gain (subtracted) | 11.7 / 7.7 | 11.7 / 7.7 | 0 |

On the accrual basis, at the low end, the Black group costs $3,568 per member more than the engine's union. [CALCULATION: `derived/rekey_by_program_sept29.csv`] The parts add to that total with controlled rounding.

| Program | Per member |
|---|---:|
| Social Security and Medicare | +$1,691 |
| Medicaid | +$1,355 |
| Welfare | +$979 |
| Veterans and military medical | +$636 |
| Police, courts and prisons | +$609 |
| No production gain | +$294 |
| Property, per-head lines and capital | +$314 |
| Schools | −$645 |
| Income, payroll and sales taxes (the Black group pays more) | −$1,665 |
| **Difference** | **+$3,568** |

**Why the ratio fell from September 27.** The table gives each step's cost in $bn, with one decimal and controlled rounding. [CALCULATION: `derived/attribution_sept29.csv`, `derived/attribution_buckets_sept29.csv`]

| Step | NH Black | Mexican-origin, rough |
|---|---|---|
| September 27 case, published weights (ladder 259) | 549.0 / 595.2 | 310.8 / 359.0 |
| Audit row-4 weights | +3.1 / +3.9 | +6.3 / +5.7 |
| sept29's lines, nationals and responses; no group state-priced or miles-keyed | −21.4 / −20.5 | −26.0 / −26.4 |
| State prices and road miles for each group (rule 4): the cash set | −4.9 / −4.8 | +3.8 / +5.7 |
| The pension accrual (rule 3): the case | +16.3 / +16.3 | +80.6 / +80.6 |
| **sept29 case** | **542.1 / 590.1** | **375.5 / 424.6** |

- **The accrual** moves the ratio. On the cash set the ratio is 1.69 / 1.50, about where it stood on September 27 (1.66 / 1.50); the accrual takes it to 1.38 / 1.28. It adds $80.6bn to the union, whose young workers' accruals replace small current benefits: Social Security +$52.0bn, Medicare +$26.4bn. It adds only $16.3bn to the Black group: Medicare +$15.1bn (1.55 of Part A accrual per HI tax dollar), income tax +$5.6bn (the tax on benefits leaves the receipts) and Social Security −$4.4bn.
- **sept29's lines** cut the Black cost by $21.4bn, nearly all of it in capital, property and production taxes ($21.4bn). A line-level check through the library breaks this down [CALCULATION: scratch check, not a lane output]:
  - receipts lost rise on owner-occupied property (+$20.5bn, item 5's response of 0.763), tenant-occupied property (+$10.3bn), the smaller enterprise line (+$5.0bn) and personal property (+$0.9bn);
  - they fall on public housing's split, where the rough housing-subsidy key gives the group 33.5% of public housing's deficit (−$15.3bn).

  These lines add to the $21.4bn with controlled rounding.
- **Rule 4** cuts it by $4.9bn. The group lives where police and prisons cost less per resident (police index 0.97, corrections per prisoner 0.86): −$5.3bn at the low end.

**Rules.** This lane runs through the white lane's library (`white_replacement_2026_09_28/rekey_sept29.py`). The five rules in that lane's section "v4 case (sept29)" apply unchanged. Each alternative for the Black group is priced in `derived/rule_alternatives_sept29.csv` [CALCULATION]:

| Alternative | Change in the NH Black cost, $bn |
|---|---|
| Rule 2: the two new receipt lines at the keys of the lines v4 split them from | −2.3 |
| Rule 3a: every group at the union's accrual per tax dollar | −12.4 |
| Rule 3b: the case's benefit-tax rule at each end | 0.0 / −0.4 |
| Rule 4: the group at national prices and the September 27 road keys | +4.9 / +4.8 |

This lane adds three rules of its own.

- **The group's accrual** (`accrual_black.py`).
  - It uses the pension lane's model at its central settings: payable benefits, entry-age attribution, the Trustees' new-issue rates, general mortality, and Note 2025.7 ratios by the age-adjusted career level.
  - The group is the pension frame's persons with `PEHSPNON` 2 and `PRDTRACE` 2.
  - Every foreign-born member's career starts at arrival (`PEINUSYR` midpoints). This extends the pension lane's rule for the Mexico-born to every immigrant in the group.
  - *Alternative:* every member starts at 21. That gives a net ratio of 1.0174 and Part A of 1.4386, instead of 1.0396 and 1.5522: **−$7.1bn**.
- **The relative benefit-tax rate.**
  - The group's rate is not measured: the pension lane ran Tax-Calculator for the union only.
  - A statutory proxy applies the section 86 thresholds to tax-unit income other than benefits, taxed at the 2024 bracket rate. It gives the union 0.586 against its measured 0.523.
  - The group's proxy of 0.629 is scaled by that ratio, to 0.5625 [INFERENCE].
  - *Alternative:* the unscaled proxy, **−$0.1bn**.
- **The normalized gap is on the cash set only.** It charges each group its population share of the national balance. The national lines are cash totals, so an accrued pension has no national counterpart. The accrual basis reports the cost only.

**Per-member denominators.** The Black group's own CPS count is 41,954,494; row-4 weights leave it unchanged. The union's is the account's 39,712,493, never the CPS's 40.9M.

**The brief's two traps.**
1. `rekey.py:218` prices every line at national × share. The v4 correction lines and the September 24 union-only lines have national 0, so they would be 0 for every group, silently. Here the v4 lines are priced for each group from its own residence and driving (rule 4), and the union-only lines stay at the engine's amounts for the union alone (rule 5).
2. `rekey.py:199` looks up `BLK_EXTERNAL[lid]` for the Black group, which raises a KeyError on the new receipt lines. Here they are keyed (rule 2).

A setup gate fails if a line lacks a key or if a national-0 line with an amount lacks a rule.

**Gates (this run, after the reboot).**
1. **Old cases unchanged.** `rerun_lane.py` with `engine_lines.cjs`, `rekey.py` and `victim_cost.py`, the new scripts allowed unrun, reports **IDENTICAL, 24/24 files** (21:36 JST). In the first cycle (21:15), before the bucket file existed, it reported 23/23.
2. **sept29 outputs.** Each step exits 0 with no failed gate:
   - `engine_lines.cjs sept29` and `sept29_cash`;
   - `accrual_black.py`, whose gate checks that the union's OASDI ratios (1.018378 payable, 1.297788 scheduled), its Part A accrual of $41.137bn and its benefit-tax timing of 0.083884 reproduce the pension lane;
   - `rekey_sept29.py`, with 129 gates, the library's included.
3. **Oracle.** Through the library:
   - the dumps are `main_case_bands.csv`'s `adopted` row, $371.4146 / 434.8410bn, and its `cash_set` row, $294.7011 / 361.8175bn, to 5e-5;
   - the lane's cost formula reproduces each dump to 1e-9;
   - this lane's September 27 cost, gap, old-age and capital columns reproduce `rekey_summary.csv` on published weights, to 5e-5.
4. **Two passes after the sept29 run.** Two `rerun_lane.py` passes with all seven commands report **IDENTICAL, 24/24 files, both passes** (21:38 and 21:39 JST). The first cycle's two passes also matched, 23/23.

**Reproduce (sept29), after the September 27 list above.**

```sh
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
node $B/engine_lines.cjs sept29
node $B/engine_lines.cjs sept29_cash
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/accrual_black.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/rekey_sept29.py   # after the white lane's accrual_white.py and v4_inputs.py
```

**New files (no existing output moved).**
- Scripts: `accrual_black.py` and `rekey_sept29.py`.
- In `derived/`: `accrual_ratios.csv`, `benefit_tax_proxy.csv`, `engine_lines_sept29.json`, `engine_lines_sept29_cash.json`, `rekey_summary_sept29.csv`, `rekey_by_program_sept29.csv`, `rekey_line_shares_sept29.csv`, `rule_alternatives_sept29.csv`, `attribution_sept29.csv` and `attribution_buckets_sept29.csv`.

`engine_lines.cjs` gained the case argument and is byte-identical to the white lane's copy; its default output is unchanged. Commit this lane with the white lane, whose `rekey_sept29.py` it imports.

### Log

- 2026-09-29 20:14 JST: resumed after the weekly usage limit stopped the run at 17:24 JST (per the lead). Only this stub had been written; the reads and probes before the stop were not saved in the lane.
- 2026-09-29 20:35 JST: confirmed so far [CALCULATION]:
  - `engine_lines.cjs` takes a case argument; the default still writes `derived/engine_lines.json` byte for byte. `sept29` and `sept29_cash` write `engine_lines_sept29.json` ($371.41 / 434.84bn at 48 / 11) and `engine_lines_sept29_cash.json` ($294.70 / 361.82bn).
  - `accrual_black.py` → `derived/accrual_ratios.csv`: NH Black OASDI accrual 1.0907 per tax dollar payable (1.3754 scheduled), net 1.0396 of the tax on benefits; Part A 1.552 per HI tax dollar. The union reproduces the pension lane (gate). With every member entering at 21 instead of immigrants at arrival: 1.0673 and 1.439. All residents: 1.0355, net 0.9496, Part A 1.140.
  - Relative benefit-tax rate: 0.5625, a statutory proxy scaled by the union's measured / proxy ratio (`derived/benefit_tax_proxy.csv`; the proxy gives the union 0.586 against the measured 0.523, and third-plus whites 0.974 against the white lane's assumed 1.0) [INFERENCE].
- 2026-09-29 20:42 JST: first sept29 run, all gates passed (71) [CALCULATION: `rekey_sept29.py` → `derived/rekey_summary_sept29.csv`]: NH Black $542.1 / 590.1bn on the case's accrual basis ($12,921 / 14,064 per member, 1.38× / 1.28× the engine union's $9,353 / 10,950 per member); on the cash set $525.8 / 573.8bn (1.69× / 1.50× the union's $7,421 / 9,111). Normalized gap on the cash set −$471.2bn (−$11,230 per member) against the engine union's −$270.0 / −292.9bn. With the group at national prices and the September 27 road keys instead of its own (the alternative to rule 4): $547.0 / 594.9bn.
- 2026-09-29 21:03 JST: the machine rebooted at 20:51 JST and the scratch logs were lost. Resumed from the recovered transcript: the sept29 code and outputs were on disk and parsed complete. This lane's gate-1 logs were lost, so every gate was rerun.
- 2026-09-29 21:12–21:27 JST: added `rule_alternatives_sept29.csv` (with this lane's benefit-tax and career-entry alternatives), `attribution_sept29.csv` and `attribution_buckets_sept29.csv`. The alternative to rule 4 now calls `rule4="union"` (formerly `local=False`). The summary values are unchanged.
- 2026-09-29 21:13–21:26 JST and 21:35–21:40 JST: two full gate cycles, both clean for this lane. The second is the one reported under Gates above.
- 2026-09-29 21:50 JST: this section written; status line set.

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`), the rough re-key puts the cost of removing the
41.95M non-Hispanic Black residents at **$541.7 / 589.7bn** a year on the case's accrual basis, **$12,912 / 14,055 per
member**: $0.4bn below sept29's $542.1 / 590.1bn, from v5's responses alone, since the group keeps its own count. The
engine's union now costs **$9,129 / 10,789 per member** (v5's $390.29 / 461.24bn over the lineage's 42,752,213), so
the Black figure is **1.41× / 1.30× the Mexican-origin figure per member** (sept29 1.38× / 1.28×). Against the rough
union on 42.75M ($9,224 / 10,548) it is 1.40× / 1.33× (sept29 1.37× / 1.32×); on the cash set 1.74× / 1.52× the
engine's union (sept29 1.69× / 1.50×). [CALCULATION: `rekey_sept29.py --case oct05` → `derived/rekey_summary_oct05.csv`]]

[2026-10-07: the oct05 files are rebuilt on the IPEDS keys for Pell and public higher education, a defect fix decided in
the v6 propagation (the white lane's section "v6 case (oct07)", "The IPEDS keys"). On them the NH Black group costs
**$530.7 / 578.0bn**, $12,650 / 13,778 per member, **1.39× / 1.28×** the engine's union per member (1.37× / 1.31× the
rough union's; cash set 1.71× / 1.49×): Pell +$2.97bn, public higher education by IPEDS use −$12.74bn, the college
stock −$1.25 / 1.88bn. The tables below keep the rough keys of September 27. [CALCULATION:
`derived/rekey_summary_oct05.csv`; the white lane's `ipeds_terms_oct05.csv`]]

claude-opus-5-5 (v5consC)

**Rule.** The white lane's section "v5 case (oct05)" applies (the case lane's Consumers row: both sides on 42.75M).
The union's side is the rough union on the identified 39,712,493 at v5's responses, plus the 3,039,720 added people at
the case lane's own amounts on every line (its G3+ and white parts), which the CPS keys cannot see. [ASSUMPTION] The
NH Black group is a population of its own, not a slice of the union's size, so it keeps its CPS count of 41,954,494
and only v5's responses move it; the comparison is per member. Kept on the identified 39.71M at v5's responses
instead, the engine's union is $371.12 / 434.53bn, $9,345 / 10,942 per member, and the ratio stays 1.38× / 1.28× (cash
1.69× / 1.50×). [CALCULATION: the union dumps' costs in this run's gates over 39,712,493]

| $bn a year, spec 48 / 11 | Engine union, oct05 | Rough union, oct05 | **NH Black, oct05** | NH Black, sept29 |
|---|---:|---:|---:|---:|
| Persons (the per-member denominator) | 42,752,213 | 42,752,213 | 41,954,494 | 41,954,494 |
| **Cost of removal, accrual basis (the case)** | 390.3 / 461.2 | 394.3 / 451.0 | **541.7 / 589.7** | 542.1 / 590.1 |
| per member | $9,129 / 10,789 | $9,224 / 10,548 | **$12,912 / 14,055** | $12,921 / 14,064 |
| NH Black per member over this column | 1.41 / 1.30 | 1.40 / 1.33 | | 1.38 / 1.28 (engine) |
| Cost of removal, cash set | 307.4 / 383.4 | 307.5 / 365.6 | 525.4 / 573.4 | 525.8 / 573.8 |
| NH Black per member over this column | 1.74 / 1.52 | 1.74 / 1.60 | | 1.69 / 1.50 (engine) |
| Normalized gap, cash set | −277.4 / −306.0 | −271.9 / −275.9 | −471.2 / −471.2 | −471.2 / −471.2 |

[CALCULATION: `derived/rekey_summary_oct05.csv`; the sept29 column from `rekey_summary_sept29.csv`]

On the accrual basis, at the low end, the Black group costs $3,783 per member more than the engine's union (sept29
$3,568). The parts add to that total with controlled rounding, and the same rounding reproduces the sept29 table above
part for part. [CALCULATION: `derived/rekey_by_program_oct05.csv`, scratch tabulation]

| Program | Per member, oct05 | sept29 |
|---|---:|---:|
| Social Security and Medicare | +$1,662 | +$1,691 |
| Medicaid | +$1,371 | +$1,355 |
| Welfare | +$991 | +$979 |
| Veterans and military medical | +$624 | +$636 |
| Police, courts and prisons | +$629 | +$609 |
| No production gain | +$279 | +$294 |
| Property, per-head lines and capital | +$310 | +$314 |
| Schools | −$670 | −$645 |
| Income, payroll and sales taxes (the Black group pays more) | −$1,413 | −$1,665 |
| **Difference** | **+$3,783** | **+$3,568** |

The gap per member widens because the union's per-member cost falls: the added people cost the case $6,309 / 8,790
each against the identified union's $9,345 / 10,942. They pay more tax per head than the identified members: the
engine union's income, payroll and sales taxes per member rise from $10,285 (sept29) to $10,537, which is why the tax
row narrows. [CALCULATION: `rekey_by_program_sept29.csv`, `rekey_by_program_oct05.csv`]

**Attribution** (`derived/attribution_oct05.csv`). Steps 1–3 rebuild the September 29 chain on the identified union at
v5's responses, so step 1 also carries the response move: the NH Black step 3 is $541.7 / 589.7bn (sept29 $542.1 /
590.1bn) and the rough union's is $375.2 / 424.2bn (sept29 $375.5 / 424.6bn). Step 4 adds the lineage: +$19.18 /
26.72bn to the rough union, nothing to the NH Black group.

**Rule alternatives on oct05** (`derived/rule_alternatives_oct05.csv`; change in the NH Black cost, $bn): rule 2
−2.2 (sept29 −2.3); rule 3a −12.4; rule 3b 0.0 / −0.4; rule 4 +4.9 / +4.8; the uncalibrated benefit-tax proxy −0.1;
every career starting at 21 −7.1. Rule 2's moves by $0.1bn through v5's responses on the two receipt lines; the others
move by less than $0.001bn.

**Gates.** `rekey_sept29.py --case oct05`: 147 gates, exit 0, the library's lineage gates included (the case and union
dumps are the bands and the September 29 case plus the response move; the case less the union is the lane's G3+ and
white parts, 1e-9; step 4 moves the union by the added people's cost and the NH Black group not at all). The sept29 run
rewrites its six files byte for byte (129 gates). `rerun_lane.py` with all twelve commands (the three September 27
ones, the four sept29 ones and the five oct05 ones): **IDENTICAL 34/34, exit 0** (2026-10-06 00:39:29–00:40:01 JST).

**Reproduce (oct05), after the sept29 list and the white lane's oct05 dumps.**

```sh
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
for c in oct05 oct05_cash oct05_union oct05_union_cash; do node $B/engine_lines.cjs $c; done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/rekey_sept29.py --case oct05
```

New in `derived/`: `engine_lines_oct05.json`, `engine_lines_oct05_cash.json`, `engine_lines_oct05_union.json`,
`engine_lines_oct05_union_cash.json`, `rekey_summary_oct05.csv`, `rekey_by_program_oct05.csv`,
`rekey_line_shares_oct05.csv`, `rule_alternatives_oct05.csv`, `attribution_oct05.csv` and
`attribution_buckets_oct05.csv`. `engine_lines.cjs` stays byte-identical to the white lane's copy; `rekey_sept29.py`
gained `--case`.

## v6 case (oct07), 2026-10-07

[Round 2, later on 2026-10-07: every group's income taxes moved to the case's own keys. The figures in this section
use the CPS-dollar rule, now the `cost_cps` arm; the current figures are in "v6 round 2" below.]

[2026-10-07: on main case v6 (`oct07`, `../main_case_2026_10_07/`), with every group on the IPEDS keys for Pell and
public higher education, the rough re-key puts the cost of removing the 41.95M non-Hispanic Black residents at
**$527.9 / 575.3bn** a year on the case's accrual basis, **$12,583 / 13,712 per member**: $2.8 / 2.7bn below v5's
$530.7 / 578.0bn on the same keys. At the low end Social Security and Medicare fall by $2.74bn (the 2026 Trustees'
separate-funds path), the per-head lines by $1.64bn (retiree health takes $1.92bn of pay-go benefits out of other
federal benefits; its accrual adds to the other lines) and schools, police and welfare rise by $1.57bn (retiree
health's accrual and item 4's tuition term, +$0.33bn). Item 4's hospital term stays beside the central, at the team
lead's decision; with it the group would cost $527.5 / 574.9bn. The engine's union costs **$9,101 / 10,794 per member**
(v6's $389.08 / 461.48bn over the lineage's 42,752,213), so the Black figure is **1.38× / 1.27× the Mexican-origin
figure per member** (v5 on the same keys 1.39× / 1.28×; on the rough keys of September 27 it was 1.41× / 1.30×).
Against the rough union on 42.75M ($9,249 / 10,605) it is 1.36× / 1.29× (v5 1.37× / 1.31×); on the cash set 1.71× /
1.49× the engine's union (v5 1.71× / 1.49×). [CALCULATION: `rekey_sept29.py --case oct07` →
`derived/rekey_summary_oct07.csv`, `rekey_by_program_oct07.csv` against `rekey_by_program_oct05.csv`]]

claude-opus-5-5 (prop-d)

**Rules.** The white lane's section "v6 case (oct07)" applies: the items by kind from `meta.items`, both sides of the
union on 42.75M, the NH Black group on its own CPS count of 41,954,494. For the items:
- [ASSUMPTION] Item 1 (the 2026 separate-funds path): `accrual_black.py --case oct07` prices the NH Black group and
  all residents on the same path as the union, through the pension lane's code (the white lane's `tr2026_path.py`),
  at the 2025 run's relative benefit-tax rates. Net OASDI accrual per tax dollar, 2025 reports → 2026 path: NH Black
  (immigrants from arrival) 1.039625 → 1.020794, all residents 0.949586 → 0.930832, the union 0.973667 → 0.953547.
  [DATA: `derived/accrual_ratios_oct07.csv`]
- [ASSUMPTION] Item 2 (retiree health): its national-scale edits reach the group through the rough keys' shares of
  the lines. Other federal benefits lose $19.8bn of pay-go retiree benefits, −$1.9bn for the group at its Social
  Security key; the accrual adds $1.6bn across service lines (schools +$0.7bn, police +$0.4bn).
- Items 3 and 4 are the union's (its added people's ages; its user fees and education keys), so they do not move the
  NH Black group directly.
- [ASSUMPTION] **The IPEDS keys** (the white lane's section "The IPEDS keys": a defect fix of the rough keys, every
  group on oct05 and oct07, sept29 kept). The NH Black group is the whole of its race, so it takes IPEDS's Black
  shares: public higher education by cost-weighted use, 9.9% (the CPS college key gave it 15.3%), Pell 19.2% (its
  Social Security key gave it 9.7%), and on oct07 tuition at 9.5% (θ = 1). Hospital charges by its MEPS payer shares
  are priced beside the central (the white lane's hospital bullet).
  Parts on oct07: Pell +$2.97bn, use −$12.79bn, the college stock −$1.25 / 1.88bn, tuition +$0.33bn; in all −$10.74 /
  11.37bn ($538.6 / 586.7bn on the rough keys of September 27); the hospital term beside, −$0.44bn. On oct05, without
  the tuition term, −$11.02 / 11.65bn. [CALCULATION: the white lane's `derived/ipeds_terms_oct07.csv`,
  `ipeds_terms_oct05.csv`]
- [ASSUMPTION] Tuition residency θ = 1 for a race stays (the lead's decision): at θ 0.5 / 1.5 the group costs $528.5 /
  575.8bn and $527.3 / 574.7bn. [CALCULATION: the white lane's `derived/limits_oct07.csv`]

| $bn a year, spec 48 / 11 | Engine union, oct07 | Rough union, oct07 | **NH Black, oct07** | NH Black, oct05 (IPEDS keys) |
|---|---:|---:|---:|---:|
| Persons (the per-member denominator) | 42,752,213 | 42,752,213 | 41,954,494 | 41,954,494 |
| **Cost of removal, accrual basis (the case)** | 389.1 / 461.5 | 395.4 / 453.4 | **527.9 / 575.3** | 530.7 / 578.0 |
| per member | $9,101 / 10,794 | $9,249 / 10,605 | **$12,583 / 13,712** | $12,650 / 13,778 |
| NH Black per member over this column | 1.38 / 1.27 | 1.36 / 1.29 | | 1.39 / 1.28 (engine) |
| Cost of removal, cash set | 307.4 / 385.4 | 309.9 / 369.9 | 514.3 / 561.7 | 514.4 / 561.7 |
| NH Black per member over this column | 1.71 / 1.49 | 1.69 / 1.55 | | 1.71 / 1.49 (engine) |
| Normalized gap, cash set | −278.9 / −309.7 | −275.5 / −281.5 | −462.4 / −462.4 | −461.4 / −461.4 |

[CALCULATION: `derived/rekey_summary_oct07.csv`; the oct05 column from `rekey_summary_oct05.csv`]

On the accrual basis, at the low end, the Black group costs $3,482 per member more than the engine's union (v5 on the
same keys $3,520; on the rough keys of September 27 $3,738 and $3,783). The parts add to that total with controlled
rounding. [CALCULATION: `derived/rekey_by_program_oct07.csv`, `rekey_by_program_oct05.csv`, scratch tabulation]

| Program | Per member, oct07 | oct05 (IPEDS keys) |
|---|---:|---:|
| Social Security and Medicare | +$1,680 | +$1,662 |
| Medicaid | +$1,368 | +$1,371 |
| Welfare | +$986 | +$991 |
| Veterans and military medical | +$628 | +$624 |
| Police, courts and prisons | +$636 | +$629 |
| No production gain | +$279 | +$279 |
| Property, per-head lines and capital | +$242 | +$351 |
| Schools | −$902 | −$974 |
| Income, payroll and sales taxes (the Black group pays more) | −$1,435 | −$1,413 |
| **Difference** | **+$3,482** | **+$3,520** |

- The IPEDS keys move the schools row by −$304 per member on oct05 and −$297 on oct07 (use −$305, tuition +$8), and
  the per-head and capital row by +$41 on both (Pell +$71, the college stock −$30). [CALCULATION: the white lane's
  `ipeds_terms_oct05.csv` and `ipeds_terms_oct07.csv` over 41,954,494]
- From v5 to v6 the per-head and capital row narrows by $109: the engine union's per-head lines rise by $3.5bn with
  the fee item's Pell key (+$3.87bn), the Black group's fall by $1.6bn (retiree health's pay-go benefits leave other
  federal benefits), and the engine's capital return falls by $0.6bn. The schools row narrows by $72: the
  union's schools and colleges fall by $2.0bn (the fee item's education keys against retiree health's accrual and the
  added people's younger ages) and the Black group's rise by $1.0bn (retiree health's accrual and the tuition term).
  The Social Security and Medicare row widens by $18, as the union's accrual falls by more per member than the
  group's. [CALCULATION: `rekey_by_program_oct07.csv` against `rekey_by_program_oct05.csv`]

**Attribution** (`derived/attribution_oct07.csv`). Steps 1–3 rebuild the September 29 chain on the identified union
at v6's responses: the NH Black step 3 is $527.9 / 575.3bn and the rough union's $375.1 / 423.9bn (v5 on the same keys
$375.2 / 424.1bn). Step 4 adds the lineage: +$20.34 / 29.47bn to the rough union (v5 +$19.18 / 26.72bn), nothing to the
NH Black group.

**Rule alternatives on oct07** (`derived/rule_alternatives_oct07.csv`; change in the NH Black cost, $bn): rule 2
−2.2 (v5 −2.2); rule 3a −12.7 (v5 −12.4; the union's accrual per tax dollar is the 2026 path's); rule 3b 0.0 / −0.4;
rule 4 +4.9 / +4.8 (v5 the same); the uncalibrated benefit-tax proxy −0.1; every career starting at 21 −7.1.

**Gates.** `rekey_sept29.py --case oct07`: 192 gates, exit 0, the white library's item and IPEDS gates included (the
payload's meta is v5's but for the items; the union dumps are v5's plus the edit sets' union parts and the
capital-return move; the added people are v5's plus the items' lineage parts, the lineage item and its interactions,
1e-9; the accrual files' union is the case's 2026 arm; the NH Black group takes IPEDS's Black shares, 1e-12 relative).
`accrual_black.py --case oct07` gates the union against the arm's row (5e-9). The sept29 run rewrites its files byte
for byte (129 gates); the oct05 run on the IPEDS keys passes 161 gates, and with the keys off it reproduces the
committed oct05 files. `engine_lines.cjs` stays byte-identical to the white lane's copy, and the four oct07 dumps equal
the white lane's.

**Reproduce (oct07), after the oct05 list and the white lane's `ipeds_keys.py` and oct07 accrual run.**

```sh
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/rekey_sept29.py --case oct05
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/accrual_black.py --case oct07
for c in oct07 oct07_cash oct07_union oct07_union_cash; do node $B/engine_lines.cjs $c; done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/rekey_sept29.py --case oct07
```

New in `derived/`: `accrual_ratios_oct07.csv`, `engine_lines_oct07.json`, `engine_lines_oct07_cash.json`,
`engine_lines_oct07_union.json`, `engine_lines_oct07_union_cash.json`, `rekey_summary_oct07.csv`,
`rekey_by_program_oct07.csv`, `rekey_line_shares_oct07.csv`, `rule_alternatives_oct07.csv`, `attribution_oct07.csv` and
`attribution_buckets_oct07.csv`; six oct05 files rebuilt on the IPEDS keys. `accrual_black.py` gained `--case oct07`
(its default outputs are unchanged); `rekey_sept29.py` gained the oct07 case.

### Log (times from `date`)

- 2026-10-07, after 14:28 JST: the team lead decided to apply the IPEDS keys to every comparator on oct05 and oct07
  (a named defect fix; sept29 kept).
- 15:16:23–15:16:30 (file times): in place, sept29 (129 gates, byte for byte), oct05 (161 gates) and oct07 (192 gates)
  on the IPEDS keys.
- After 15:16 the team lead decided that item 4's hospital term comes out of every comparator's central on oct07 and
  stays beside (the white library's `HOSPITAL_ON = False`), and that θ = 1 for a race stays, with 0.5–1.5 printed.
  v6 is final.
- 16:42:17–16:42:26 (by `date`): oct05 (161 gates) and oct07 (192 gates) rerun in place, exit 0. The oct05 files and
  the oct07 dumps and accrual file are unchanged; six oct07 files change (`rekey_summary`, `rekey_by_program`,
  `rekey_line_shares`, `rule_alternatives`, `attribution`, `attribution_buckets`).
- 16:59:43–17:00:51 (by `date`): `rerun_lane.py` with all eighteen commands (the three September 27 ones, the four
  sept29 ones, the five oct05 ones and the six oct07 ones of the reproduce blocks): **IDENTICAL 45/45, exit 0**. It
  ran after the white lane's final rerun (16:55:28–16:58:52), whose `ipeds_keys.json`, oct07 accrual files and library
  this lane reads.

## v6 round 2: income taxes on the case's own keys (oct05, oct07), 2026-10-07

[2026-10-07, round 2: every group's income taxes now take the case's own keys. Under those keys, removing the 41.95M
non-Hispanic Black residents costs others **$501.2 / 548.6bn** a year on the case's accrual basis, **$11,947 / 13,076
per member**. On the CPS-dollar rule, which charged a group only the income tax it reports to the CPS, the figure was
$527.9 / 575.3bn (the v6 section above). The group pays $26.69bn more income tax at both ends and on both bases:
federal +$23.19bn, state +$3.29bn and other personal +$0.21bn. Per member it is **1.31× / 1.21× the engine's union**
(was 1.38× / 1.27×) and 1.34× / 1.28× the rough union on 42.75M (was 1.36× / 1.29×). The rough union itself pays $15.12bn
more. [CALCULATION: `rekey_sept29.py --case oct07` → `derived/rekey_summary_oct07.csv`, `income_tax_keys_oct07.csv`]]

claude-opus-5-5 (prop-d)

**Rules.** The white lane's section "v6 round 2" applies:
- Federal income tax takes v4 item 3's IRS-raked key.
- State and other personal taxes take the state-liability key.
- Both ends use the shared allocation, with the personal one beside.
- No group takes a union-only correction.
- The CPS-dollar rule, the proportional spread and the capital arm stay beside.

The NH Black group's federal share goes from 0.0615 to **0.0711** (+15.7%, below the average slice's +19.7%). Its
state share goes from 0.0766 to **0.0827**. Under the personal allocation the shares are 0.0719 and 0.0827.
[DATA: `derived/income_tax_keys_oct07.csv`]

| $bn a year, spec 48 / 11 | Engine union, oct07 | Rough union, oct07 | **NH Black, oct07** | NH Black, oct05 |
|---|---:|---:|---:|---:|
| Persons (the per-member denominator) | 42,752,213 | 42,752,213 | 41,954,494 | 41,954,494 |
| **Cost of removal, accrual basis (the case)** | 389.1 / 461.5 | 380.3 / 438.3 | **501.2 / 548.6** | 504.0 / 551.3 |
| per member | $9,101 / 10,794 | $8,896 / 10,251 | **$11,947 / 13,076** | $12,013 / 13,141 |
| NH Black per member over this column | 1.31 / 1.21 | 1.34 / 1.28 | | 1.32 / 1.22 (engine) |
| Cost of removal, cash set | 307.4 / 385.4 | 294.8 / 354.8 | 487.7 / 535.0 | 487.7 / 535.0 |
| NH Black per member over this column | 1.62 / 1.41 | 1.69 / 1.54 | | 1.62 / 1.42 (engine) |
| Normalized gap, cash set | −278.9 / −309.7 | −260.4 / −266.3 | −435.7 / −435.7 | −434.7 / −434.7 |
| On the CPS-dollar rule (`cost_cps`), accrual | | 395.4 / 453.4 | 527.9 / 575.3 | 530.7 / 578.0 |

[CALCULATION: `derived/rekey_summary_oct07.csv`, `rekey_summary_oct05.csv`]

At the low end on accrual, the Black group costs $2,846 per member more than the engine's union. On the CPS-dollar
rule the difference was $3,482, and v5 on the case's keys gives $2,884. Only the tax row moves. The parts add to the
total with controlled rounding.

| Program | Per member, oct07 | CPS-dollar rule (v6 section) | oct05 |
|---|---:|---:|---:|
| Social Security and Medicare | +$1,680 | +$1,680 | +$1,662 |
| Medicaid | +$1,368 | +$1,368 | +$1,371 |
| Welfare | +$986 | +$986 | +$991 |
| Veterans and military medical | +$628 | +$628 | +$624 |
| Police, courts and prisons | +$636 | +$636 | +$629 |
| No production gain | +$279 | +$279 | +$279 |
| Property, per-head lines and capital | +$242 | +$242 | +$351 |
| Schools | −$902 | −$902 | −$974 |
| Income, payroll and sales taxes (the Black group pays more) | **−$2,071** | −$1,435 | −$2,049 |
| **Difference** | **+$2,846** | +$3,482 | +$2,884 |

[CALCULATION: `derived/rekey_by_program_oct07.csv`, `rekey_by_program_oct05.csv`; scratch tabulation, which reproduces
the v6 section's column from the pre-round-2 files]

- **The arms** (accrual, $bn):
  - The CPS-dollar rule gives $527.9 / 575.3bn.
  - The proportional spread gives $495.4 / 542.8bn.
  - With capital-side taxes responding, the cost is $374.8 / 422.2bn. With the top tail now inside the central, this
    is also the both-arms figure.
  - At national prices (rule 4's alternative) the cost is $506.2 / 553.4bn.
  - Under the personal allocation it is $499.4 / 546.8bn, and with item 4's hospital term, beside the central,
    $500.8 / 548.2bn.
  - At tuition residency θ 0.5 / 1.5 it is $501.8 / 549.2bn and $500.7 / 548.0bn.

  [CALCULATION: `rekey_summary_oct07.csv`; the white lane's `ipeds_terms_oct07.csv`, `limits_oct07.csv` and
  `income_tax_keys_oct07.csv`]
- **The like-for-like delta** against the rough union is −$120.9 / −110.3bn on accrual, against −$132.5 / −121.9bn on
  the CPS-dollar rule: the rough union pays $15.12bn more as well.
- **Rule alternatives** (`rule_alternatives_oct07.csv`): each one's change in the NH Black cost is the v6 section's;
  only the levels move.
- **Attribution** (`attribution_oct07.csv`): step 5 moves the NH Black group by −$26.69bn and the rough union by
  −$15.12bn, each gated to minus its income-tax lines' move (1e-9).

**Gates.** `rekey_sept29.py --case oct07` passes 211 gates and exits 0; `--case oct05` passes 180. They include the
white library's round-2 gates (the white lane's section) and each step-5 gate. The `cost_cps` arm reproduces the v6
section's costs, and `rekey_line_shares` moves only on the three income-tax lines. sept29 is unchanged.

**Files.** New in `derived/`: `income_tax_keys_oct05.csv` and `income_tax_keys_oct07.csv`. Changed, for oct05 and
oct07: `rekey_summary` (it gains the four arm columns and `delta_like_for_like_cps_bn`), `rekey_by_program`,
`rekey_line_shares`, `rule_alternatives`, `attribution` (step 5) and `attribution_buckets`. The dumps and accrual files
do not move. The reproduce list is the v6 section's.

### Log (round 2; times from `date` or the files' clock)

- 2026-10-07 20:15:21 and 20:19:18 (log times): `--case oct05` (180 gates) and `--case oct07` (211 gates) ran in place,
  exit 0.
- 21:07:28–21:08:37 (by `date`): the first `rerun_lane.py` with the v6 section's 18 commands reported **DIFFERS, 46/47**
  (exit 1). The changed file was `income_tax_keys_oct05.csv`, which the 20:15 oct05 run wrote before the white
  library's last edit to `tax_key_rows()` (20:16:04, file time). That edit renamed the two base columns (`cps_record_tax_bn` and
  `cps_rough_key_tax_bn` became `cps_case_key_base_bn` and `cps_rough_key_base_bn`) and gave the other-personal-tax row
  the base of its own rough key, `fit`: $111.33bn and $147.70bn, where the stale file showed the state base, $25.74bn
  and $41.08bn. No share, amount or cost changed. The rerun rewrote the file.
- 21:09:13–21:10:21 (by `date`): the same rerun again: **IDENTICAL 47/47, exit 0**.
- 21:49:49–21:51:23 (by `date`): the same rerun after the white library relabelled the columns of its CPS-totals file
  and the white lane added `income_tax_parts.py`: **IDENTICAL 47/47, exit 0**. This lane writes no CPS-totals file,
  and none of its figures moved.

### 2026-10-14 18:28:21 JST — v7 propagation, completed leaves and stopped comparator

After `CASE_FINAL` named adopted commit `148ed1ea`, final Consumers, The items and the decision were re-read and
payload hashes checked. The computed route is `oct14`, personal ends 16/11; earlier outputs remain unchanged.
Four final engine dumps reproduce $339.55201782952685 / $423.64926070050683bn, cash
$264.4255736155055 / $348.52281648648557bn. These are engine account totals; no final NH Black cost is asserted.
The white lane's `check_dumps_oct14.py` validates both lanes' leaves with 64 gates: adopted/cash bands at 5e-5,
cost and lineage accounting at 1e-9 and R7 responses at 1e-12. Case/source/dump hashes are pinned in
`derived/engine_lines_oct14_meta.json`. [CALCULATION: `derived/engine_lines_oct14*.json`]

The white lane's pension-free `export_keys_oct14.py` exports this lane's raw personal key shares using canonical
`TK.case_keys`, the gated row-4 frame and final lineage counts. `income_tax_keys_oct14_meta.json` pins case, raw
inputs, code and CSV hashes, explicitly labels its limited scope, and reports W's receipt-key residual
+1.932434339213529e-7bn at both ends/bases after the adopted item. This exceeds the required 1e-9 contract.
[CALCULATION: `derived/income_tax_keys_oct14.csv` and `derived/income_tax_keys_oct14_meta.json`]

The final rough run exits 1 at R9, before writing comparator totals. **Exact unresolved question:** how should
the rough identified-union OASDI net ratio, Part A per-tax rate and benefit-tax calibration use
`meta.row4_frame.values`, given that its state and owner keys already use row-4 weights? Final Consumers specifies
engine pension reconstruction, which still passes at 1e-9, but not this rough calibration. Both live wrappers
preflight the question and stop before writing. Rough totals and attribution remain unvalidated.

R7 code applies the comparator's own wage share and the source's `black_nh` factors, at the same personal ends
and responses as the union. Corporate carrier totals are split proportionally. **Credit asymmetry:** the mixed-unit
credit crossing was measured for the union and the added G3+-priced people only; no NH Black crossing is measured
or invented. Final Consumers leaves items 7/8 comparator counterparts open. [DATA: final case `RESULT.md`
Consumers; `job_capital_taxes_2026_10_14/derived/item.json`; CALCULATION: white library `rekey_sept29.py`]

Candidate oct14 rough outputs were preserved in `_cache/prop-d-candidate-oct14/`; the scratch
`comparator-quarantine.json` records each move and hash. Final dumps/raw-key leaves stay in `derived/`. The initial
leaf-only rerun (four dumps, shared dump checker and raw-key exporter) ended **IDENTICAL 55/55, exit 0**; rough
pricing, accrual and the full wrapper are explicitly excluded. This is partial coverage, not a validated move of
the complete comparator. The final source/metadata repeat is recorded in the worker evidence file.

## v7 wave 2 (2026-10-14): rough pension rule resolved

The parent defines the rough union as legacy pension amounts plus only R9 union pension parts, carried exactly by the payload (kRN included). The shared library derives effective rates on the same rough payroll/benefit bases; all other R9 parts are already represented by rough row-4 keys. Its SS, Medicare and benefit-tax equality gates pass at 1e-9, as does the Consumers R9 cash/accrual identity. Black and white central ratios retain their own weights. Rule 3a uses the effective union Part A rate and the source white_rule3_ratio; its legacy gross-OASDI alternative is explicitly labelled. Mixed-unit credits remain measured only for the union and its G3+-priced added people. [CALCULATION: white library rekey_sept29.py; derived/rekey_summary_oct14.csv]

- 2026-10-14 19:07 JST — full re-key exit 0, 5.13s, max RSS 1707.9MiB. NH Black accrual costs: 422.7455 / 501.1208bn on 41,954,494 people; union rough costs 315.7654 / 397.7945bn on the 42.75M lineage. These account/model rows preserve their different counts. All adopted-case and R9 gates pass.

Live reproduction: sh infra/immigration-fiscal/black_comparator_rough_2026_09_28/run_oct14.sh after white run_oct14.sh. The full reproducibility receipt executes every wrapper child explicitly, profiling accrual_black.py during that required repeat; run_oct14.sh is the only allow-unrun entry (its equivalent child sequence is run, and shell syntax checked). Earlier keyed outputs remain unchanged.

- 2026-10-14 19:09:57 JST — full live producer sequence rerun: IDENTICAL 62/62, exit 0, 83.15s, max RSS 1776.7MiB. Every producer was rerun; the pension child was profiled during this repeat. [CALCULATION: wave-2 rerun_black_wave2.py and rerun_lane.py]

### Round-2 final execution — 2026-10-15

Adopted b35ac8fb, personal16/11, coverage-inclusive lineage45,230,062.30075857. Full actual producer route passed66tests; full White byte rerun208/208, full standalone Black96/96, both exit0 with no script-coverage exemptions. The later renderer-only trailing-newline fix and this appended receipt are checked separately for byte idempotence; no numerical artifact changes. Mixed conventions and both own-mortality profile bounds remain explicitly beside each other. Item11 is lineage-only and every gap includes its exclusion. [CALCULATION: prop8/d-white-final-rerun.log, d-black-final-rerun.log, d-render-final-rerun.log; DATA: derived/symmetric_*_oct15.csv]

<!-- oct15 second round-2 comparator fixes -->

## Round-2 comparator fixes — 2026-10-15

This section supersedes the earlier mixed-engine comparison readings. Every gap uses the complete lineage and comparator on the rough engine at the personal ends. The exact case lineage is reported separately in the bridge, itemized by evaluated line, public-capital return, production and post-engine amount. [CALCULATION: symmetric_comparisons_oct15.csv; lineage_engine_bridge_oct15.csv]

The two mortality conventions are lineage whole-population with comparators own-group (mixed conventions), and every group on its own mortality. The own-lineage sensitivity transports source coefficients onto live pension amounts and bounds the unresolved added-profile split; it is not an independent status-specific mortality remeasurement. Cash is unchanged. [CALCULATION: mortality_conventions.py; symmetric_audit_oct15.json]

| Mortality / profile; accrual, $bn low / high | Rough lineage | White | White gap | Without item 11 | Case minus rough bridge |
|---|---:|---:|---:|---:|---:|
| mixed mortality conventions, none | 362.784 / 450.927 | -202.445 / -90.222 | 565.229 / 541.149 | 554.489 / 526.618 | 6.207 / 8.275 |
| own-group mortality, low | 366.523 / 454.667 | -202.445 / -90.222 | 568.969 / 544.889 | 558.229 / 530.357 | 6.207 / 8.275 |
| own-group mortality, high | 366.527 / 454.671 | -202.445 / -90.222 | 568.973 / 544.893 | 558.233 / 530.361 | 6.207 / 8.275 |

Item 11 is measured for the lineage only; white and Black mixed-unit removal remains unmeasured. Every gap row carries this label and the exact lineage-only amount. Removing item 11 shows its arithmetic size; it does not measure the comparator counterpart. Item 10 also remains lineage-only. Comparator coverage remains absent under the recorded own-price source limitation. [DATA: symmetric_audit_oct15.json; CALCULATION: comparison_contract.py]

| Black minus rough lineage; accrual, $bn low / high | Own count | Equal lineage count | Equal count without item 11 |
|---|---:|---:|---:|
| mixed mortality conventions, none | 40.555 / 28.365 | 72.045 / 65.786 | 82.785 / 80.318 |
| own-group mortality, low | 36.815 / 24.626 | 68.305 / 62.046 | 79.045 / 76.578 |
| own-group mortality, high | 36.811 / 24.622 | 68.301 / 62.042 | 79.041 / 76.574 |

Equal-count Black costs hold each end’s per-person cost fixed at the lineage count from population_v8.with_coverage; own-count results are beside them. This linear accounting standardization does not solve a new CES removal. [CALCULATION: symmetric_population_oct15.csv]

| Item 9, own job-capital domestic-source change ($bn) | Low | High |
|---|---:|---:|
| A1_third_plus_nh_white | 11.089 | 4.103 |
| A3_third_plus_nh_white_at_union_ages | 10.229 | 3.785 |
| nh_black_rough | 4.210 | 1.558 |

| Status and pension fixes; accrual, $bn low / high | Before cost | Bracket only change | Payroll only change | Joint change | Exact scenario selection change | After cost |
|---|---:|---:|---:|---:|---:|---:|
| A1_third_plus_nh_white | -202.081 / -89.858 | 0.114 / 0.114 | -0.478 / -0.478 | -0.364 / -0.364 | 0.000 / 0.000 | -202.445 / -90.222 |
| A3_third_plus_nh_white_at_union_ages | -89.713 / 17.968 | -0.002 / -0.002 | -0.390 / -0.390 | -0.392 / -0.392 | -5.100 / -5.100 | -95.205 / 12.477 |
| A4_third_plus_nh_white_stationary | -149.590 / -41.507 | 0.082 / 0.082 | -0.438 / -0.438 | -0.356 / -0.356 | -1.140 / -1.140 | -151.086 / -43.003 |
| nh_black_rough | 404.233 / 480.187 | -0.330 / -0.330 | -0.564 / -0.564 | -0.894 / -0.894 | 0.000 / 0.000 | 403.338 / 479.293 |

The bracket and payroll cells hold the other fix off; the joint cell applies both. The final scenario selection step includes the exact civilian record mask, population scaling and A3/A4 age weights; it is not an isolated age effect. Pension numerator conservation and status-input hash checks are enforced before selection. [CALCULATION: round2_changes_oct15.csv; mortality_comparators.py; status_keys_oct14.py]

Reproduce with `sh infra/immigration-fiscal/white_replacement_2026_09_28/run_oct15.sh`. These are modeled annual removal costs. [CALCULATION: run_oct15.sh]

## R2C40 final receipt — 2026-10-15T03:58:49+09:00

Own-mask comparator item11 is now measured and applied post-evaluator, with pinned paired gap SEs. [FRAMING-SENSITIVE] The labeled one-sided gap is preserved immediately below the measured row. Full White 210/210, full Black 96/96, C8 source-only 77/77, legacy annual-only 39/39, pension 43/43, Indian independent fiscal 71/71: all IDENTICAL, exit 0. Exact baselines unchanged; no feedback into M5; no annual charge to legacy stock. Break tables and Indian social/combined rows remain withheld. [CALCULATION: parent scratch c40-*-rerun.json/log; c40-validation.json; prop-d-result.md]

<!-- oct15 C40 measured comparator mixed-unit removal -->

## Measured comparator mixed-unit removal (R2C40) — 2026-10-15

This section supersedes every earlier C40 reading with the comparator side at zero. Item 11 now enters A1 White and Black published costs after evaluation. The evaluator remains the unadjusted M5 calibration input. Other membership or age-standardized White definitions (A2/A3/A4) remain unmeasured; their own-age removal term is not silently reused. [CALCULATION: comparison_contract.py; symmetric_comparators_oct14.py]

[FRAMING-SENSITIVE] Both sides rest on whole-person static removal. These are conditional 2024 modeled amounts, with current-year survivor terms in both sets and no spousal-pension model. Only the item11 gap uncertainty is reported: it uses the signed lineage-minus-comparator replicate vectors in the pinned source gaps.csv, never component-SE quadrature. [DATA: ../mixed_unit_comparators_2026_10_15/derived/{white,black}_summary.json and gaps.csv]

| Own-mask item11, $bn | Low / high | Own count |
|---|---:|---:|
| A1 White | -35.394141 / -17.804446 | 173,053,897.03 |
| Black | -2.333671 / +0.646664 | 41,954,493.92 |

A1 scales by the exact live lineage count / own count; Black central stays at its own count. Both groups also have separately labeled population standardizations. All contrasts below use the rough engine on both sides; the exact case-minus-rough bridge remains separate. Completion and coverage remain lineage-specific under the earlier source limitations. [CALCULATION: symmetric_comparisons_oct15.csv; symmetric_population_oct15.csv; symmetric_white_population_oct15.csv; lineage_engine_bridge_oct15.csv]

| Basis / mortality / profile; lineage-minus-comparator, $bn low / high | A1 at lineage count | Black own count | Black at lineage count |
|---|---:|---:|---:|
| accrual, mixed mortality conventions, none: measured both sides | 574.479874 / 545.802639 | -38.220926 / -29.012041 | -69.529082 / -66.482989 |
| One-sided gap (comparator item11 at zero) | 565.229118 / 541.149197 | -40.554597 / -28.365377 | -72.044953 / -65.785837 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |
| accrual, own-group mortality, low: measured both sides | 578.219592 / 549.542357 | -34.481207 / -25.272322 | -65.789363 / -62.743271 |
| One-sided gap (comparator item11 at zero) | 568.968837 / 544.888916 | -36.814879 / -24.625658 | -68.305234 / -62.046119 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |
| accrual, own-group mortality, high: measured both sides | 578.223499 / 549.546265 | -34.477300 / -25.268415 | -65.785456 / -62.739363 |
| One-sided gap (comparator item11 at zero) | 568.972744 / 544.892823 | -36.810971 / -24.621751 | -68.301327 / -62.042211 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |
| cash, mixed mortality conventions, none: measured both sides | 404.394899 / 375.717664 | -128.188209 / -118.979324 | -160.156061 / -157.109968 |
| One-sided gap (comparator item11 at zero) | 395.144144 / 371.064223 | -130.521880 / -118.332659 | -162.671931 / -156.412816 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |
| cash, own-group mortality, low: measured both sides | 404.394899 / 375.717664 | -128.188209 / -118.979324 | -160.156061 / -157.109968 |
| One-sided gap (comparator item11 at zero) | 395.144144 / 371.064223 | -130.521880 / -118.332659 | -162.671931 / -156.412816 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |
| cash, own-group mortality, high: measured both sides | 404.394899 / 375.717664 | -128.188209 / -118.979324 | -160.156061 / -157.109968 |
| One-sided gap (comparator item11 at zero) | 395.144144 / 371.064223 | -130.521880 / -118.332659 | -162.671931 / -156.412816 |
| Item11 paired gap SE (conditional, not full-cost SE) | 5.883572 / 5.843094 | 5.122122 / 5.120987 | 5.212657 / 5.213276 |

The measured own-count and equal-count base-route gaps are also retained in the pinned source below. This base route uses whole-population mortality and its original status/production rules; it is distinct from the combined-rule sensitivities above. [DATA: source gaps.csv]

| Base route / basis / count, $bn low / high | Measured both sides |
|---|---:|
| white, set, own_count: measured both sides | 1133.102480 / 774.857913 |
| One-sided gap (comparator item11 at zero) | 1097.708339 / 757.053467 |
| white, set, lineage_count: measured both sides | 551.132559 / 522.606525 |
| One-sided gap (comparator item11 at zero) | 541.881803 / 517.953084 |
| white, cash, own_count: measured both sides | 714.976539 / 356.731972 |
| One-sided gap (comparator item11 at zero) | 679.582398 / 338.927526 |
| white, cash, lineage_count: measured both sides | 384.234677 / 355.708643 |
| One-sided gap (comparator item11 at zero) | 374.983922 / 351.055202 |
| black, set, own_count: measured both sides | -79.417624 / -69.977048 |
| One-sided gap (comparator item11 at zero) | -81.751295 / -69.330384 |
| black, set, lineage_count: measured both sides | -112.569692 / -109.273820 |
| One-sided gap (comparator item11 at zero) | -115.085563 / -108.576668 |
| black, cash, own_count: measured both sides | -144.299396 / -134.858820 |
| One-sided gap (comparator item11 at zero) | -146.633067 / -134.212156 |
| black, cash, lineage_count: measured both sides | -176.427141 / -173.131268 |
| One-sided gap (comparator item11 at zero) | -178.943011 / -172.434116 |

Reproduce with `sh infra/immigration-fiscal/white_replacement_2026_09_28/run_oct15.sh`. The SHA256 pins stop `[BLOCKED]` on a changed summary or paired-SE source. [CALCULATION: run_oct15.sh]

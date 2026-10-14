**Verdict:** The spending identity is material, but neither its marginal spending mix nor its propensity is measured. Mortality weighting raises the PM row; a life-year valuation lowers it much more. The crash-capacity decrease depends on a disputed density interpretation. Incoming volunteer hours remain a conditional proxy, and city taxes are already counted. No unique combined correction is identified; the named stacks below are conditional and are not adopted.

## Current spending and pollution

Frame: 2024 dollars, effects on other residents, frozen v7 personal endpoints 16/11. Both the cash set and the accrual set receive the same current-spending correction. [DATA: frozen case payloads; `derived/case_inputs.json`]

The current saving is H = −direct fiscal response − induced receipts = cash-set cost − capital return + private WTP. The pension promises excluded by CASH, the imputed capital return and the private WTP are not current tax-funded purchasing power. The union is the identified-members contribution at full-case responses, obtained by removing declared lineage edits/parts and restoring base production; it is not a newly optimized standalone case. [CALCULATION: `case_inputs.cjs` → `derived/case_inputs.json`]

| Population basis | Current H, low / high ($bn) |
|---|---:|
| identified_union_at_case_responses | 213.335 / 269.579 |
| lineage | 226.605 / 286.995 |

Assume all H is spent in 2024 at the national average emissions intensity [ASSUMPTION]. CE is the lane's survey spending denominator; PCE is the official national-accounts alternative, fixed at the February 2025 vintage. Neither estimates the marginal spending mix or the marginal propensity to consume. CE and PCE have different coverage; their difference is a calibration sensitivity, not an interval. Tessum's inherited personal-consumption attribution includes private investment allocated with consumption, so the per-dollar calculation conditionally lets that investment follow spending. [SOURCE: pinned BEA Table 8; inherited Tessum model; `inputs/pins.json`]

| Population | Denominator | PM re-spending alone | Government mirror | Joint change, low / high ($bn) |
|---|---|---:|---:|---:|
| identified_union_at_case_responses | CE | -19.197 / -24.258 | 6.079 | -13.118 / -18.179 |
| identified_union_at_case_responses | PCE | -10.330 / -13.053 | 6.079 | -4.251 / -6.975 |
| lineage | CE | -20.181 / -25.559 | 6.544 | -13.637 / -19.015 |
| lineage | PCE | -10.860 / -13.754 | 6.544 | -4.316 / -7.210 |

[CALCULATION: `respending.py` → `derived/items.csv`, `spending_components.csv`]. These task-1-only changes hold the old mortality/exposure convention. The government mirror restores the old excluded row, with its use 1.1 and responding share .55 still assumed. A separate `pm25_government_mirror_budget_mix_arm` uses exact current public-consumption shrinkage at uniform public-spending emissions intensity; it is an alternative, not a second government row.

Restaurant and consumer-scale re-spending are beside arms: restaurant psi becomes psi × (1−H/group spending), while the consumer-scale demand arm scales its row by effective demand. Extra money does not restore absent customers or population. The population and customer-count regressors in the existing grocery/network estimates therefore do not identify a causal spending correction. Cuisine composition remains unchanged. [ASSUMPTION; CALCULATION: `derived/items.csv`, named `*_demand_arm` rows]

## Individual corrections and stack

On the measured receiver ages and common national mortality rates, the identified union's PM self-share is 11.5902%, versus the current exposure share 19.1161%; its uniform-VSL row becomes $74.428bn. Geography/source attribution L/iota/E remain model assumptions. See the air lane's mortality table for conditional survey SEs and life-year ages; these are not SEs for the source model or the counterfactual. [CALCULATION: air lane `mortality_items.py` → `derived/mortality_items.csv`, `mortality_context.json`]

The one-change rows below are compared to the brief's preserved $439.435316 / $532.847640bn pairing, not a moving peer output. They use the case's existing source-key lineage extrapolations with the receiver boundary held at the identified union. The unobserved added recipients have not thereby become observed. The crash producer also supplies a separately declared exchangeable-recipients correction for an outside-lineage arm; never apply that correction twice. [DATA: `inputs/baseline_totals_oct14.csv`; producer declarations]

| Task / arm | CE change, low / high ($bn) | PCE change, low / high ($bn) |
|---|---:|---:|
| 1: respending_plus_old_government_mirror | -13.212 / -19.015 | -4.087 / -7.210 |
| 2: mortality_self_share | 6.902 / 6.902 | 6.902 / 6.902 |
| 3: VSLY_0 | -42.615 / -42.615 | -42.615 / -42.615 |
| 3: VSLY_0.03 | -35.563 / -35.563 | -35.563 / -35.563 |
| 4: all_density | -3.804 / -5.314 | -3.804 / -5.314 |
| 4: multivehicle_only | 0.426 / 0.595 | 0.426 / 0.595 |
| 5: primary_food_displacement_1.0 | 2.678 / 2.678 | 2.678 / 2.678 |
| 5: any_food_displacement_1.0 | 5.756 / 5.756 | 5.756 / 5.756 |
| 7: city_size_tax | 0.000 / 0.000 | 0.000 / 0.000 |

[CALCULATION: `stack.py` → `derived/one_fix_deltas.csv`]. The over-$5bn flags are in that table. The VSLY rows already include mortality reweighting and replace the uniform-VSL row; never add tasks 2 and 3. No replicate SE identifies a marginal propensity or displacement.

For task 5, CPS household food-pantry/free-meal receipt is measured. Incoming volunteer labour is not. The 2023 CEV questionnaire has no organization types, so the proxy transports the detailed 2015 person-task shares, then assumes equal service per recipient household and mean volunteer hours. Full displacement of the primary-food proxy is below $5bn; the any-food proxy exceeds it. Displacement 0/.5/1 is an assumption bracket, not an estimated distribution. Gross out, incoming proxy and net are all in the benefits lane's `volunteering_flows.csv`; apply its delta columns to the parent's boundary-corrected outgoing level. [DATA: pinned CPS Food Security and Volunteering files; CALCULATION: benefits lane `social_receipts.py`]

Task 7's premise is false: the existing gross city earnings gain is after-tax private earnings plus induced receipts. The taxes are already inside the social row. Additional tax credit is zero. [CALCULATION: benefits lane `derived/city_tax_decomposition.csv`; traced scale producer and production receipt partition]

The named illustrative stacks below use all-density crash response, zero displaced volunteering and no effective-demand market arm. They recompute the mortality–re-spending interaction instead of summing isolated task 1 and task 2. The social pairing's low-end raw-coded justice footing reduces H relative to the main fiscal low end, using the exact frozen band difference. CO2 stays outside every stack. [CALCULATION: `stack.py` → `derived/conditional_stacks.csv`, `integration.json`]

| Valuation | Denominator | Changed pairing, low / high ($bn) |
|---|---|---:|
| uniform, rate 0 | CE | 428.402 / 514.052 |
| uniform, rate 0 | PCE | 438.233 / 526.771 |
| VSLY, rate 0 | CE | 387.555 / 477.035 |
| VSLY, rate 0 | PCE | 391.364 / 481.963 |
| VSLY, rate 0.03 | CE | 393.370 / 482.303 |
| VSLY, rate 0.03 | PCE | 398.037 / 488.342 |

The full conditional grid also varies crash interpretation, food proxy, displacement, market-demand response and the PM/crash recipient boundary. The `lineage_exchangeable` arm removes the added receivers from PM and crash harm at the average nonmember receipt rate; that is an assumption, and other channels are held. It is not a confidence interval, a point recommendation or a completed estimate of all effects on the entire lineage's remaining residents. Unknown source–receiver geography and incoming volunteering remain unresolved. [INFERENCE]

## Carbon and binding caps, beside

EPA 2023's actual annual-2024 appendix row is parsed, rather than interpolating rounded 2020/2030 cells; IWG's actual 2024 row is parsed too. Both are inflated from 2020 dollars with the inherited BLS CPI. Gross consumption CO2 subtracts Mexico-born members' origin footprint at .85 of Mexico's GCB consumption CO2 per head, adds remittance-funded Mexican emissions and subtracts current US re-spending emissions. US-born members' origin counterfactual remains their nonexistence, as in the original lane. Mexico's observed country mean and the migrant selection multiplier are distinct; .85 and the 11% US damage share remain assumptions. [SOURCE: EPA Table A.5.1; IWG Table A-1; pinned GCB/OWID; ASSUMPTION: original CO2 weights, selection and damage share]

| Carbon valuation | Denominator | Lineage damage to other US residents, low / high ($bn) |
|---|---|---:|
| epa2023_2pct | CE | 10.238 / 9.567 |
| epa2023_2pct | PCE | 11.402 / 11.040 |
| iwg2021_3pct | CE | 2.707 / 2.530 |
| iwg2021_3pct | PCE | 3.015 / 2.919 |

[CALCULATION: `derived/co2_beside.csv`]. Identified-union rows, gross/origin/remittance/re-spending emissions, national damages and unit valuations are separate columns. All carbon rows remain beside the total.

Binding-cap share of marginal consumption-associated precursor emissions is None (unidentified). Program price/bank evidence in the air lane does not establish that a whole year's SO2/NOx emissions are fixed at the cap, and seasonal 12-state evidence is not the national annual inventory. Agriculture, transport and other precursors need their own source/spending bridge. No cap-zero multiplier is silently imposed. [DATA: air lane `derived/binding_caps.json`, pinned primary program files; INFERENCE]

## Producer contract, checks and reproduction

`derived/items.csv` preserves the existing item schema and adds population_basis/end/spending_denominator/comparator/beneficiary/valuation/overlap. `pm25_respending` and `pm25_government_mirror_legacy_response` are components; `pm25_joint_respending_government` is their alternative sum. Budget-mix government is an alternative to legacy government. Market-demand rows are beside. Carbon is never additive to the stack. `derived/one_fix_deltas.csv` contains isolated deltas; `conditional_stacks.csv` contains complete named conditional readings. No shared consumer is wired here; parent integration owns row replacement and recipient-boundary choices.

Positive controls: frozen cash band/capital at 1e-9bn; original PM and government rows at source rounding; row4 count bridge; primary-table unique row/shape; pin verification; current-budget identity; independent stack closure at 1e-9bn. Source PDF parsing handles repeated continued-table headings; an initial last-heading split discarded 2024 and failed loudly, fixed by a unique numeric-row schema guard. No tolerances were loosened. [DATA: `derived/audit.json`, `integration.json`]

The checks are deterministic accounting/source/replication checks, not validation of the assumed epidemiological and economic causal effects. The research instrument is an LLM; inherited assumptions and new empirical inputs are kept distinct to limit instrument bias. [INFERENCE]

```sh
node infra/immigration-fiscal/social_respending_2026_10_14/case_inputs.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_respending_2026_10_14/pin_inputs.py --check
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_respending_2026_10_14/respending.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_respending_2026_10_14/stack.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_respending_2026_10_14/check_outputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_respending_2026_10_14/render_result.py
```

Log: 2026-10-14 22:07:41 JST, recorded parent checkpoint from `date`; producer first successful run 2.975s, RSS197,918,720 bytes. Final rerun evidence is appended in the task's external result file, measured with Python perf_counter/resource. Git metadata remains untouched. [DATA: execution outputs]

## Round-2 corrections

2026-10-15 JST. Earlier sections/logs above remain the round-1 record. Source sender/receiver quantities and H retain the frozen v7 producer frame; road capacity uses the native oct15 key. The Sept24 consumer applies the oct15 resource account and complete denominator. [CALCULATION: producer tables; Sept24 consumer]

- Denominator: CE central → PCE central. CE is a labelled units sensitivity. Both standalone stack execution and consumers require the complete source-pin registry and matching funding/denominator accounting bases.
- Crash rule: all-density → multivehicle-only. On PCE, uniform DOT VSL, zero incoming displacement and the identified-union PM/crash receiver boundary: 441.175 / 532.107 → 446.686 / 539.849bn. These named producer scenarios retain their declared frozen social quantities; the native oct15 road capacity and all-channel crime valuation are applied.
- PM mortality: total plume deaths are reweighted for receptor mortality before membership shares. Nonfatal illness retains exposure dollars. The source lane's dated correction records the before/after deaths and harm; national source attribution and local reference-mixture assumptions remain explicit.
- One mortality basis: crime, PM and crashes use uniform DOT VSL centrally. Life-year readings apply to all three together and preserve nonmortality dollars. The PM-only life-year pseudo-pairings are removed. The registry fails on a missing channel, mixed basis or discount rate.
- All-channel life-year producer scenarios beside: 401.190 / 496.475bn at 0%, 406.449 / 501.259bn at 3%. These are alternatives to the uniform scenario, never added to it.
- Re-spending funding: the consumer moves frozen v7 H to v8 resource arithmetic under an explicit current-resource treatment of unclassified cash amounts. Completion production lacks separate P/F. Resource alternatives add capital and subtract signed private production income plus city earnings/taxes, deferring promises or adding the set-minus-cash bridge as wealth-equivalent promises. Fixed labour supply makes native private WTP equal included after-tax market income; other timing/spendability assumptions remain conditional.
- One joint pairing: the consumer joins crime, PM, crash capacity, congestion and volunteering replacements, with accounting interaction closure ≤1e-9bn and with/without round-1 readings. The producer's pre-round-1 crime replacement and the consumer's already-corrected P7 delta are separate fields, preventing double counting. Behavioural cross-channel interactions are unmeasured.
- Publication: outputs are staged before rename; readers verify generation hash receipts before and after loading. Interrupted multi-file publication fails closed. Scientific gates raise explicitly under python -O.

Below-bar log only: CPI-only fear WTP versus income-updated VSL; shared descendant exposure; within-age mortality; PM-only re-spending; government mirror both ends and legacy .55; outsider source–receptor bound; saving/propensities; SO2 cap offset. No extra central adjustment is made. [DATA: round-2 review packets]

[CALCULATION: derived/integration.json; 576 conditional rows; derived/conditional_stacks.csv. Reproduce with the commands above and this lane's full pytest suite.]

### Execution log

2026-10-15 03:23:39 JST (`date`): source dependency receipts now bind the exact pin registry, case-input bytes, producer code and upstream generation. Both publication and readers reject missing edges, changed inputs and individually valid bundles from different generations. The original frozen pairing's PM/crash sender levels are pinned separately and removed before inserting exact new levels; historical producer deltas cannot silently substitute for that baseline. All gates raise explicitly. Thirteen basis, publication, sender-level and mortality-registry regressions pass. Final seven-command reproduction is recorded in the parent result. [CALCULATION: `test_publication_contract.py`, `test_accounting_basis.py`, `test_valuation_registry.py`]

Below-bar reviewer estimates retained only as unverified log leads: CPI-only fear inflation versus income-updated VSL +$2.5–2.8bn; one shared descendant-exposure perturbation across crime/PM/crashes −$0.7–5.7bn jointly. No estimate is adopted or independently verified here. [UNVERIFIED: round-2 review packets]

2026-10-15 06:01:26 JST (`date`, parent): rerun on corrected v8 (`d1a24d47`), IDENTICAL 25/25, exit 0. The producer scenarios price on the frozen v7 package, so none of this lane's figures move; `inputs/pins.json` re-pins `service_response_long_run_2026_09_27/derived/net_change_oct15.json`, whose values are unchanged (its recorded source hashes moved). The Sept24 consumer carries the corrected fiscal row: joint pairing $462.163473 / 561.630823bn.

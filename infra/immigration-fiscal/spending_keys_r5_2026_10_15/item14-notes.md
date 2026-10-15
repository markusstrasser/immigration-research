**Verdict:** [DEGRADED] A program-complete measured key is unavailable. The delivered partial conditional item rekeys a source-defined retirement block; it preserves the current key on every unresolved component. It is not a measured resolution of WB06.

`build_item()` in `income_security.py` returns the JSON-serializable item. Default output is `inputs/admin_item.json`. `effective_key_ratio` has personal/shared ratios; each named arm has the same field. `build_item(require_complete=True)` and CLI `--require-complete` stop `[BLOCKED]`. The parent owns the package adapter, full v8 endpoint calculation and joint evaluation. No git operations were performed.

The data register was checked first: the case-vintage BEA workbook and CPS sources are already local; SSA and CMS sources supplement them. Source transcriptions, URLs and cache hashes are in `inputs/admin_sources.json`. [DATA]

BEA CY2024 consumption is $167.818bn: federal $30.536bn, state/local $137.281bn, plus $0.001bn published rounding. T3.15.5 reports consumption **plus gross investment**, with federal subfunctions: disability $1.636bn, retirement $2.501bn, welfare/social services $11.875bn, unemployment $0.003bn, other $18.644bn. State/local has disability $5.699bn and welfare/social services $135.343bn. Federal investment is $4.123bn; state/local $3.761bn. These are parsed from the pinned workbook, with label, year, unit and closure gates. [SOURCE: BEA T3.15.5 lines 72–77,115–117; T3.17 lines 10,20,31,124,133; file/hash in generated JSON]

T3.15.5 footnote 1 explicitly identifies retirement as administering OASI and railroad retirement, excluding employee pension plans. A proportional consumption/investment bridge gives retirement consumption $2.203483539629bn = $2.501bn × $30.536bn/$34.659bn. This is a modelled split, not a measured consumption cell. The no-investment and all-investment arms put retirement consumption at $2.501bn and zero; both are feasible given the federal $4.123bn investment total. All other federal consumption, all state/local consumption and published rounding retain the current cash-assistance-dollar key. [SOURCE: pinned BEA footnote; CALCULATION; ASSUMPTION]

The retirement block uses CPS positive `SS_VAL` caseload, rather than benefit dollars. This combines OASI and DI and does not separately identify railroad beneficiaries; the key is an explicit program proxy. SSA's own CY2024 administrative expenses are $4.939bn OASI and $2.508bn DI; SSI FY2024 administration is $4.796bn including state-supplement user fees. OASI alone exceeds BEA's retirement C+GI block, so direct insertion would fail the accounting bridge. The agency values are recorded beside and never enter central values. [SOURCE: SSA official administrative-expense table and SSI25 IV.E1; URLs in inputs/admin_sources.json]

The CPS headcount is gated by the existing `world_ledger_2026_09_27/population_basis.py` row-4 implementation: 39,712,493.331188 people, source mask records and totals checked against the pinned declaration. Read only the required columns. Caseload proxy shares are exported with weighted national/target totals and unweighted positive-key records. [CALCULATION: income_security.py; DATA: pinned CPS ASEC2025 income2024]

| Key | Personal share | Shared share |
|---|---:|---:|
| Current cash-assistance dollars | 0.164399306 | 0.175039691 |
| OASDI positive-key persons | 0.049725856 | 0.052019331 |
| SSI positive-key persons | 0.081162344 | 0.080893013 |
| SNAP SPM-unit exposure | 0.162418528 | 0.162418528 |
| Medicaid own coverage | 0.193723647 | 0.193723647 |
| UI positive-key persons | 0.121946793 | 0.125952325 |
| Workers compensation positive-key persons | 0.140936936 | 0.151630552 |
| Population | 0.118352664 | 0.118352664 |

These are survey proxies on the account's row-4 frame, not administrative ethnic caseload estimates. SNAP is household-unit exposure; shared cash-program caseloads spread own receipt equally within SPM units. Positive dollar fields identify reported receipt; absent claims and underreporting remain. Child-welfare caseload has no account key and remains null. [CALCULATION]

Central effective shares are personal 0.162893621 and shared 0.173424410, giving ratios 0.9908412929568114 and 0.990771912054947 relative to current keys. On the original row-4 exposure alone, the changes are −$0.252681058663bn and −$0.271073338604bn. These **are not v8 endpoint effects**: they omit v8 descendants, completion, mixed-unit and coverage prices. The parent evaluates those interactions. [CALCULATION]

The historical dataset-audit row 12 recorded about −$7.5bn for a population key on its then-current frame. The same unexpanded national exposure on current row-4 keys gives −$7.727455363496bn personal (−$9.513103598515bn shared); do not append that historical correction to v8. Whole-line population and program-key alternatives, plus state-welfare residual alternatives, are explicitly `SCENARIO_NOT_MEASURED_PROGRAM_MIX`. They are neither a confidence interval nor an identified correction. [DATA: dataset_integrity_2026_09_23/spending.md:52; CALCULATION]

CMS's primary FY2024 Medicaid Financial Management Report `ADM - National Totals` row64 gives total administrative expenditures $40,359,656,171, financed by $24,617,521,810 federal and $15,742,134,361 state. The columns close to the same total. They are financing shares, not two additive government-level consumption masses. Fiscal/calendar timing, territories, capital, fees and BEA classification remain unbridged, so these amounts stay beside. [SOURCE: downloaded official CMS zip; hash and URL in inputs/admin_sources.json]

The checked official SNAP activity-report route describes FY2023 data as of December2024; no FY2024 administrative mass was verified there. The federal reimbursement percentage does not identify a program mass. Census's 2024 technical documentation says vendor and cash-assistance categories were consolidated into E79 from survey2022. Thus E79 does not provide clean SNAP/Medicaid/TANF/child-welfare administration weights. [SOURCE: official USDA report page route and Census technical documentation, cited in inputs/admin_sources.json]

The state/local accounting candidate splits consumption into $5.698bn disability (T3.16:113 minus T3.12:28) and residual welfare $131.583bn. It is exported as `ACCOUNTING_BRIDGE_NOT_PROGRAM_WORKLOAD`; WC is not silently assigned to disability because the current-program workload mapping was not verified. Unemployment administration should not be moved into state/local income security merely because federal grants finance it: this BEA function has no separate state/local UI cell. [CALCULATION; SOURCE: pinned tables]

Items 9–10 require consistent treatment of the added-lineage and completion exposure. The executed adapter reprices those source amounts by the partial key ratio. The adopted item11 stack has no income-security administration component: its source terms are taxes/credits, resource-key movements, Medicaid/ACA and SNAP (`mixed_unit_removal_2026_10_14/round2.py:93–149`). Its amount stays fixed under this retirement-only partial arm. A future complete SNAP/Medicaid administration bridge would need an explicit workload interaction with that benefit-removal model; multiplying the whole mixed-unit scalar would be wrong. Item12's typed income-security coverage component is repriced. Items13 and15 have no common source line. The ratios do not establish uniform caseload composition across added-person profiles. [CODE; CALCULATION; LIMIT]

Verification: four tests pass (strict complete-measurement failure, BEA closures/bounds, only the retirement block changes, CMS financing closure/cache transcription). Full measurement run: 6.272 seconds, maximum RSS 283,738,112 bytes, from Python `perf_counter`/`getrusage`. Raw inputs remain read-only; downloaded bytes are confined to `_cache/admin/`. [CALCULATION]

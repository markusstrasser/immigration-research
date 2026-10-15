**Verdict:** Item13 is revised in the appended **L1 step3** section: compensation, four service-benefit lines and a separate VA medical part lower v8 by **$18.918438766bn** at both ends in set and cash (**$418.271340/member**). VA medical uses **$89.742bn [DATA]** actual FY2024 outlays with a declared **[APPROXIMATION]** FY-to-CY consumption bridge; its change is **−$5.904991128bn**. BEA classifies Community Care as a transfer, so the three-account mass is central. Items14/15 are unchanged. Earlier sections remain historical and are superseded where step3 revises them. No case adoption or git writes.

The estimand is the change in v8's conditional annual net cost to other US residents, in 2024 dollars. It is an accounting scenario under the supplied fixed-defense and functional-response rules, not an identified causal effect of removing people. The 45,230,062.300759-person lineage and all v8 items 1–12 remain fixed. Negative changes lower net cost. [FRAMING-SENSITIVE; CALCULATION: `derived/case_changes.json`]

## Full-lineage measurements

| Candidate item | Set low / high change, $bn | Cash low / high change, $bn | Change per member low / high, $ |
|---|---:|---:|---:|
| 13 Veterans compensation | −10.144536217 / −10.144536217 | −10.144536217 / −10.144536217 | −224.287469 / −224.287469 |
| 14 Partial retirement administration | −0.297511640 / −0.297511640 | −0.297511640 / −0.297511640 | −6.577741 / −6.577741 |
| 15 College function response | −4.088275291 / −4.279311499 | −4.088275291 / −4.279311499 | −90.388451 / −94.612107 |

These are changes at personal specifications **16 / 11**, averaged over the case's two allocation methods. The methods are evaluated separately; their changes differ and both are preserved. Cash switches only the inherited OASDI/Part A accounting; these spending items have the same changes in both sets. [CALCULATION: `evaluate.cjs`, `derived/case_changes.csv`]

Unchanged v8 reproduces **365.791930255 / 455.981784589** in the set and **281.752563676 / 371.942418010** in cash, within the required 1e-6bn. A purely additive check of all three conditional central arms gives **351.261607108 / 441.260425233**, cash **267.222240529 / 357.221058654**. This check is not a v9 case or a newly optimized band. [CALCULATION]

## Item 13: veterans compensation

The spending builder maps BEA T3.12 line18, CY2024 **$180.525bn**, to `veterans_pension_disability`, with response1. Its preferred `veterans` key is **CPS VET_VAL benefit dollars**, not veteran headcount (`full_account_spending_2026_09_20/builder.py:114,202–205`). The existing key is applied to each new component. Separate group pension and compensation receipt shares are not observed. [DATA; CODE]

VA's FY2026 Congressional Submission, Volume3 p147, FY2024 **actual net outlays**, reports compensation **157.781014**, pension **3.161729**, burial **0.351874bn**. The central composition bridge excludes burial from the pension/disability benefit block and preserves the national BEA total: pension fraction **0.01964505476335767**, compensation fraction **0.9803549452366423**. `derived/item13.json` records the resulting modeled CY split. There is no independently identified CY other-program residual; burial inclusion is an explicit arm. [SOURCE: `inputs/va_budget_2024_excerpt.txt`, source URL/hash in `inputs/veterans_sources.json`; ASSUMPTION: FY composition transported to CY]

Under the parent's rule, service compensation responds0 because defense positions are replaced; means-tested pensions respond1. No new current-service normal cost is added. Treasury Note13 confirms the legal/accounting distinction: means-tested pensions have only current-payable liabilities, whereas compensation is actuarially valued. Its **FY2024 compensation benefits paid $176.2bn** differs from VA budget net outlays; it is not a substitute for the VA cell or an exact CY BEA component. The Treasury amount provides a separate composition arm. Its **$290.7bn actuarial expense** is never used as a current-service normal cost. [SOURCE: `inputs/treasury_note13_excerpt.txt`; PARENT RULE; FRAMING-SENSITIVE]

The full v8 exposure before repricing is approximately **$10.347820bn** including coverage and native completion edits. Central removes **$10.144536bn**, retaining means-tested pensions. Source-defined composition arms give changes **−10.143924885** (obligations), **−10.165411772** (Treasury compensation mixed with VA pension), and **−10.122405295bn** (burial retained at response1), at both ends and in both sets. Unchanged is0. These are accounting/timing alternatives, not a confidence interval. [CALCULATION]

BEA's methodology starts from monthly outlays and adjusts payment timing, survivor programs, foreigners and territories. A fiscal-year share is therefore **not an observed CY2024 split**. Exact monthly component outlays with BEA's adjustments, or distinct group receipt shares, would supersede this proxy. [SOURCE: [BEA MP5, p46](https://apps.bea.gov/scb/pdf/national/nipa/Methpap/methpap5.pdf); LIMIT]

## Item 14: income-security administration

The exact BEA consumption anchor is **$167.818bn**: federal30.536, state/local137.281 and published rounding0.001. Source-defined C+GI subfunctions and levels, accounting subtractions, caseload numerators/denominators and record counts are exported in `derived/item14.json`; details and primary links are in [item14-notes.md](item14-notes.md). [SOURCE; CALCULATION]

Only federal retirement has a clean source definition here: BEA T3.15.5 footnote1 identifies OASI/railroad administration, excluding employee pensions. Its C+GI is2.501bn. Proportional conversion using the federal consumption/C+GI ratio gives **2.203483539629bn** retirement consumption. This conversion is modeled. The CPS positive-SS_VAL caseload is an OASDI proxy, not an exact OASI/railroad count. All unresolved federal and state/local consumption stays on its existing key. [SOURCE; ASSUMPTION]

Caseloads use the authoritative row4 reweight gate: **39,712,493.331188** people. Measured shares include OASDI, SSI, SNAP exposure, Medicaid coverage, UI and WC; the child-welfare key is explicitly null. SSA administration (CY2024 OASDI7.447bn; FY2024 SSI4.796bn) and CMS FY2024 Medicaid administration40.359656171bn are recorded **beside**. Agency expenses/financing shares do not identify additive CY NIPA consumption masses. No FY2024 SNAP-administration mass was verified. [CALCULATION; SOURCE: `inputs/admin_sources.json`]

The personal central effective key ratio is **0.9908412929568114**. Applying that conditional ratio to the full existing income-security exposure, including completion and typed coverage parts, changes32.484bn by **−0.297511640bn**. Retirement consumption0..2.501bn gives **0 to −0.337681947bn**. A whole-line population-key scenario gives **−9.098457674bn**; the old dataset-audit row12 recorded about−7.5bn on its earlier frame. These are different frames/constructions, so the older number is shown beside rather than appended. All whole-line and welfare-residual alternatives are labeled scenarios. [CALCULATION; DATA: dataset-integrity `spending.md:52`]

**The requested complete item14 measurement is unfinished at the source-bridge level.** `build_item(require_complete=True)` stops `[BLOCKED]`; `complete_measured_key` is null. Needed evidence is program-level consumption, net of investment/sales/transfers and with consistent FY/CY and government-level scope, plus child-welfare workload. A larger central re-key cannot be inferred from known caseload shares alone. [LIMIT]

## Item 15: college budget response

IPEDS FY2022–23 public GASB finance contains measured instruction/support, research, public service, hospital, auxiliary and revenue totals. The bridge excludes research centrally because BEA already removes R&D investment/sales; university hospitals sit outside the education function. Auxiliaries enter net of their own sales. Under the parent rule, instruction/support and tuition respond1, public service0, and unclassified other1 centrally. These stipulated functional responses are not estimated elasticities. [SOURCE; ASSUMPTION: [item15-notes.md](item15-notes.md), `college.py`, primary pins in `derived/item15.json`]

The conditional IPEDS net bridge is **176.219906840bn**: responsive156.091161501 plus invariant public service20.128745339. It maps proportionally to BEA S&L higher-education net consumption229.963bn; the existing allocated federal block gives consolidated exposure **234.029706937839bn**. The resulting net response is **0.8857748497320679**. The proportional scope/vintage bridge remains an assumption; it is not an exact reconciliation. [CALCULATION]

Tuition loss stays at response1: the existing union fee-disparity correction **1.844604621183bn** is held fixed. Pell and education-benefit transfers stay fixed. The original union operating use share **0.11589579410930383** is preserved exactly. Added-person operating use is recovered from their typed college capital keys, an explicit proxy because the capital category also includes a small library/other component. Central uses `U + (full_capital_use − U_capital)`; unadjusted and uniform-U-ratio arms expose that transport choice. [CODE; DATA; LIMIT]

The college capital return follows the same response centrally, holding assets, keys and the case's2%/3% rates fixed; this includes the fee offset, completion and coverage. A separate asset-use arm uses the expense mix including research, since research buildings need not disappear merely because research production is absent from consumption. [PARENT RULE; ASSUMPTION]

| College arm | Low / high change, $bn, set and cash |
|---|---:|
| Central | −4.088275291 / −4.279311499 |
| Educational sales assigned to public service | −0.945063136 / −0.989223880 |
| Unclassified other fixed | −11.479210357 / −12.015608878 |
| All public service outside education | 0 / 0 |
| Capital expense mix, central operating bridge | −4.327005424 / −4.637406698 |
| Capital key directly proxies operating | −4.112764215 / −4.303800423 |
| Uniform operating/capital use ratio | −4.083506572 / −4.274542781 |

All other source-scope/tuition arms are in `derived/case_changes.csv`. The retained-research diagnostic is not recommended as a second subtraction. No state enrollment formula was verified for the separately budgeted research/public-service blocks. Exact in-scope functions, educational sales attribution and function-specific assets would supersede the central proxy. [LIMIT; CALCULATION]

## Package contract and interactions

`items.cjs` exports `REGISTRY` and `buildItem(number, {B: v8_api}, arm, which)`. Each build returns `edits:[]`, `parts:{}` and `meta.<item>.by_end.{low,high}` with `total_bn`, line/population parts and `by_method`. This follows the post-engine form of items11/12; line parts live inside the post-engine block and `record.parts_by_line`, not edit-cell parts. **`total_bn` is the method mean.** For each method evaluation use `postEngineFor(built, reading, method)`; use `method_mean` only when aggregating methods explicitly. No automatic v9 package insertion occurs. [CODE]

The payload applies at frozen personal16/11 under these rules. A parent that changes earlier items, profiles, endpoints or generation incidence must reprice/revalidate rather than reuse fixed amounts. Generation splits for all original engine parts have not been measured; these payloads promise line parts, not complete generation incidence. [LIMIT]

- Item9: no corporate/receipt line touched; foreign-source tax scope stays fixed.
- Item10: native child edits already inside engine cells, completion line/capital carriers included once. Zero-valued completion parts remain inspectable.
- Item11: source `round2.py:93–149` contains taxes/credits, resource keys, Medicaid/ACA and SNAP, with no veteran-compensation, income-security-administration or college component. Its scalar and its typed coverage component stay fixed. A future complete program-administration bridge would need a fresh workload interaction.
- Item12: only matching typed coverage fiscal/capital parts are repriced. No blanket multiplication of coverage, mixed units, residual calibration, K12 or the total education line.
- Items13–15 have disjoint source spending/capital parts and add at fixed endpoints. Other proposed round5 items are not packaged here.

## Reproduction and validation

Run from the repo root:

```sh
sh infra/immigration-fiscal/spending_keys_r5_2026_10_15/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/spending_keys_r5_2026_10_15 \
  "uv run --no-project python3 {lane}/measure_run.py --log /private/tmp/spending-keys-replay.json -- sh {lane}/run_all.sh"
```

The wrapper runs all measurement modules, evaluates unchanged v8 and the item arms, then runs the lane tests. `measure_run.py` records `date`, Python `perf_counter`, `getrusage` peak RSS and command exit status, failing above2.5GB. Raw source files stay read-only. Downloads are confined to ignored `_cache/` (under0.03GB; disk checked first). The CMS cache URL/hash is in `inputs/admin_sources.json`; existing BEA/CPS/IPEDS inputs are registered elsewhere. VA/Treasury primary excerpts are archived with source PDF hashes. [METHOD]

Read-only Astra code review found no confirmed material defect in the frozen-endpoint adapter. One stale item11 interaction sentence was corrected against the actual source stack. Empirical bridge limitations remain; review does not turn modeled attribution into observed effects. LLM source selection and framing remain an instrument limitation. [CHECK; LIMIT]

Validation log, from `date` and Python measurements:

- 2026-10-15 11:35:21 JST: final source build, endpoint evaluation and **16 tests passed**, exit0; 23.443s; peak401,899,520bytes.
- 2026-10-15 11:36:40 JST: canonical `rerun_lane.py` **IDENTICAL:27/27**, exit0; 18.951s outer/18.481s lane; peak396,771,328bytes. Every new script is reached, no EOL or uncovered-script failure.
- 2026-10-15 11:37:48 JST: upstream v8/user-fee diffs empty; no case module edited. Source/runtime receipts are in scratch `p7/v9/{run_all.log,build_timing.json,rerun.log,rerun_timing.json,rerun_child_timing.json}`.

No Git staging, commit, merge or peer-lane edit was performed. The complete persistent changed-path list, including ignored caches and scratch evidence, is in the task's `p7/v9/L1-changed-paths.md`.

## Revisions — 2026-10-15, L1 step2

The parent extended fixed defense to every service-earned military/veterans cost. Item13 keeps its id **`veterans_compensation`**, number13, and the post-engine package form. The accepted compensation split stays unchanged: compensation0, means-tested pension1. Four further whole benefit lines take response0; mixed consumption is removed only if its military national subblock can be bridged from a primary source. Items14/15 retain their delivered values. [PARENT RULE; FRAMING-SENSITIVE]

### Applied parts and generations

Changes below are $bn/year, identical at personal16/11 and in set/cash. They include the current engine amounts, selected completion carriers and matching typed coverage parts. Convention a puts each person in their own generation; b uses the existing linked-parent/minor routing. Both are the existing v8 **imputation-method mean** generation account. The separate union method totals remain available; these conventions are not imputation methods. [CALCULATION: `derived/item13_by_generation.csv`; `derived/case_changes.json`]

| Part / source line | Key | Convention a G1 | G2 | G3+ | Total |
|---|---|---:|---:|---:|---:|
| Compensation, `veterans_pension_disability` subblock | veterans | −0.617550058 | −3.711914960 | −5.815071199 | −10.144536217 |
| Extension, `veterans_other` | va_medical | −0.161011663 | −0.577943699 | −1.081097212 | −1.820052574 |
| Extension, `veterans_readjustment` | veterans | −0.039747821 | −0.238912665 | −0.374279629 | −0.652940115 |
| Extension, `veterans_life_insurance` | veterans | −0.001566743 | −0.009417241 | −0.014753012 | −0.025736996 |
| Extension, `military_medical` | tricare | −0.036785933 | −0.134203191 | −0.199192614 | −0.370181737 |
| Extension subtotal | | −0.239112160 | −0.960476795 | −1.669322467 | −2.868911422 |
| Revised item13 | | −0.856662217 | −4.672391754 | −7.484393666 | −13.013447638 |

| Part / source line | Convention b G1 | G2 | G3+ | Total |
|---|---:|---:|---:|---:|
| Compensation, `veterans_pension_disability` subblock | −0.617550058 | −3.743568611 | −5.783417548 | −10.144536217 |
| Extension, `veterans_other` | −0.166905258 | −0.576316370 | −1.076830946 | −1.820052574 |
| Extension, `veterans_readjustment` | −0.039747821 | −0.240950011 | −0.372242282 | −0.652940115 |
| Extension, `veterans_life_insurance` | −0.001566743 | −0.009497547 | −0.014672705 | −0.025736996 |
| Extension, `military_medical` | −0.075321435 | −0.122139982 | −0.172720320 | −0.370181737 |
| Extension subtotal | −0.283541257 | −0.948903910 | −1.636466254 | −2.868911422 |
| Revised item13 | −0.901091315 | −4.692472521 | −7.419883802 | −13.013447638 |

Full precision closes to1e-9; independently rounded rows may differ in the last displayed digit. The applied four national cells are BEA T3.12 lines20/19/14/16: **37.526 / 11.391 / 0.449 / 7.157bn**. The builder's preferred keys are traced at `full_account_spending_2026_09_20/builder.py:111–116,202–205,221–227`. `veterans` is CPS VET_VAL dollars; `va_medical` is transported MEPS TOTVA24 and `tricare` is TOTTRI24. T3.12 footnote3 defines the military line as care for active-duty dependents at nonmilitary facilities; footnote4 includes private-provider VA reimbursements from2015. It does not represent all TRICARE care. [DATA: pinned `Section3All_xls.xlsx`, SHA in `derived/item13.json`; CODE]

The extension comprises **−2.741916315bn** on engine lines, **−0.028935618bn** on selected completion carriers and **−0.098059489bn** on coverage. Zero-response alternative-key carriers remain zero. Compensation remains **−10.144536216603bn**, retaining approximately **0.203283673bn** in means-tested pensions. The `compensation_only` arm reproduces the delivered item13. [CALCULATION]

### Change from unchanged v8

| Reading | v8 low / high, $bn | v8 + revised13 low / high, $bn | Change low / high, $bn |
|---|---:|---:|---:|
| Set | 365.791930255 / 455.981784589 | 352.778482617 / 442.968336951 | −13.013447638 / −13.013447638 |
| Cash | 281.752563676 / 371.942418010 | 268.739116038 / 358.928970371 | −13.013447638 / −13.013447638 |

Per45,230,062.300759 members, compensation changes **−$224.287469**, the extension **−$63.429305**, and revised item13 **−$287.716775** at each end in both sets. The method-specific revised totals are **−13.128267392bn** (`b_hotdeck_union_matched`) and **−12.898627884bn** (`b_matched_over_pooled`); their canonical mean is reported above. Generation cells are not falsely presented as independently measured method-specific splits. [CALCULATION]

With accepted14/15 also applied at the same frozen ends, the additive check becomes **348.392695687 / 438.391513812bn**, cash **264.353329107 / 354.352147232bn**. This is a conditional fixed-endpoint check, not a new case or re-optimized band. [CALCULATION]

### VA hospital consumption: verified presence, unverified mass excluded

The pinned BEA T3.17 consumption cells are CY2024 **306.539bn** health, comprising **179.700bn federal** and **126.839bn state/local**. T3.16's current expenditures include transfers and cannot substitute for consumption. BEA's [health reconciliation, section2.2](https://www.bea.gov/sites/default/files/papers/BEA-WP2020-8.pdf) and [PCE methodology](https://bea.gov/sites/default/files/papers/BEA-WP2025-7.pdf) place veterans' hospital medical care in government consumption. The engine charges the aggregate health line on **`health_other = TOTVA24+TOTTRI24+TOTOFD24+TOTSTL24`**. After the existing civilian OPEB swap, the line's current national amount is **308.358754899bn**. Thus VA hospital care is indeed carried here. [SOURCE; DATA; CODE]

VA's [FY2026 submission Vol1](https://department.va.gov/wp-content/uploads/2025/06/2026-Volume-1-Supplemental-Information-Appendices.pdf), printed pp71–72,82, supplies **FY2024 actual net outlays**, bn: Medical Services70.484, Support10.372, Facilities8.886, Community Care31.388. The four total121.130; excluding Community Care leaves89.742. Departmental Toxic Exposures Fund outlays19.457 include **16.305** in hospital/medical function703; that function's net outlays total138.543. Source cells and PDF hashes are archived in `inputs/{medical_bridge.json,va_medical_fy2024_excerpt.txt}`. FY2025 figures here are enacted/estimated, not actual. [SOURCE]

**[UNVERIFIED]** Neither89.742 nor138.543 identifies VA's CY2024 NIPA consumption. The remaining bridge needs medical TEF's direct/purchased split, capital purchases versus consumption of fixed capital, research/EHR treatment, sales/receipt netting, territory and payment-timing adjustments. [BEA Handbook chapter9](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf), pp9-2,9-10–11, explicitly requires translation of budget outlays into consumption, investment and transfers; its archived excerpt is `inputs/bea_consumption_scope_excerpt.txt`. Unlike compensation's measured FY composition transported onto a fixed CY benefit line, there is no measured VA/other-federal **consumption** composition here. Calendar transport alone cannot repair the economic-account mismatch. [SOURCE; INFERENCE]

For transparency, a **beside-only [UNVERIFIED] diagnostic** transports89.742bn outlays one-for-one to CY and divides by the current health-line national308.358754899bn. On the current `health_other` key, including its selected completion and typed coverage, it would remove **5.904991128bn**, or **$130.554565/member**, in both sets/ends. Convention a splits that −1.464899956 / −1.696993025 / −2.743098146bn, b −1.684309631 / −1.626455838 / −2.594225658bn. These are hypothetical key allocations, not measured VA group use, a NIPA estimate or a bound. They appear only in `unverified_medical_diagnostic`, outside all central payload/joint totals. The central national VA consumption mass is **null**, not zero. `health_services`, `state_price_health_services`, its civilian OPEB addition and all other federal/state/local health portions stay unchanged. [UNVERIFIED; CALCULATION]

### Remaining military-service inventory

| Source/line | Current engine key/treatment | Step2 action |
|---|---|---|
| Military pension current-service normal cost in defense consumption | population, defense response0 | Already fixed; no added retirement-benefit line |
| Military facilities, MERHCF normal cost | defense, response0 | Already fixed |
| Military pension legacy interest in domestic_interest | population, response0 | Already fixed |
| Military retiree civilian-provider care in other_federal_benefits | all_cash, line1; existing retiree_health removes19.797540984bn nationally | Keep existing removal once; do not zero the whole mixed line |
| State veterans benefits within other_state_benefits, T3.12:42 | population preferred; veterans alternative | [UNVERIFIED] national veteran portion; mixed with Alaska dividends/crime-victim payments, excluded |
| VA share of mixed health capital | health_other | [UNVERIFIED] VA stock/CFC/return bridge, excluded |
| Mixed government administration, VA sales/fees and veterans housing/loan accounts | various; no separately identified service-earned national subblock | [UNVERIFIED] outside central; cannot zero a mixed line merely because an alternative veterans key exists |

The existing pension and retiree-health source traces locate the first four rows: `pension_legacy_2026_09_30/pension_legacy.py:212–214,922–924`, `public_pension_legacy_2026_10_07/RESULT.md:39–51,79–83`, and `main_case_2026_10_07/package.cjs`'s `retiree_health` national edits. Military pension benefits do not appear as an additional disjoint government social-benefit leaf; normal costs are already in compensation/defense. No military retirement payment is newly added or removed. [CODE; DATA; EXISTING PRIMARY-SOURCE TRACE]

### Interactions, guards and delivery

Item9 changes receipts only and remains fixed. Item10's native edits remain inside their engine cells; its selected source-key carriers are priced once, while alternative carriers with response0 stay0. Item11's declared mixed-unit removal includes taxes/credits, resource keys, Medicaid/ACA and SNAP; it has no new part on these four military-service lines. Its post-engine amount and typed coverage counterpart remain fixed. Item12's matching source-side/source-line coverage parts are repriced by their recorded generation; **the coverage source's own generation attribution stays fixed in both conventions**. No uniform coverage scaling or fresh CPS population estimate is used. Items14/15 touch disjoint source parts and stay unchanged. [CODE; CALCULATION]

`item13_generations.cjs` reads existing generation corrections and models, using `v8_split.evaluator` for actual selected keys/carrier responses. Every line/population's before, after and delta sums from three generations to the union method mean at1e-9. The adapter stores compensation and extension separately in `by_end.by_part`, plus line/generation parts in `by_generation.a/b`; `derived/item13_by_generation.csv` exposes them. Callers still apply each method through `postEngineFor`; no case module was edited. Medical-source guards reject missing actual cells or conflated TEF scope, and unbridged consumption cannot enter central. [CODE; TEST]

Validation and exact changed-path manifest are appended in the task's `p7/v9/L1-result.md` and `L1-step2-changed-paths.md`. Reproduce using the original `run_all.sh` and rerun command above. No staging, commits, merges, git configuration/ref updates or edits to peer lanes.

Step2 validation: final build **2026-10-15 12:03:50 JST**, exit0, **20 tests passed**,35.563611s,526,516,224bytes peak RSS. Canonical rerun **2026-10-15 12:04:35 JST**, exit0, **IDENTICAL:33/33**,36.915070s outer /36.537183s child,426,475,520bytes peak RSS. Source Python compiles in memory; the two changed/new CJS modules pass `node --check`. Native read-only Astra review found no confirmed material defect and independently exercised the in-memory evaluator and10 scoped tests. Its source/caller coverage and limits are in `l1-step2-native-code-review.md`; the CLI invocation failed sandbox initialization and is not credited as a review. Primary PDFs/layout text are preserved in ignored `_cache/medical/` with hashes matching the archived excerpts. [CHECK]

## Revisions — 2026-10-15, L1 step3: VA medical in central

**Verdict:** Item13 now includes the separate `va_medical` part, **−$5.904991128bn**, bringing the item to **−$18.918438766bn** at both personal16/11 ends in set and cash (**−$418.271340/member**). The item retains id `veterans_compensation`, number13. Items14/15 are unchanged. This supersedes step2's exclusion of the medical mass. [CALCULATION]

**[DATA]** VA FY2026 Budget Vol1 pp71–72,82 reports FY2024 actual net outlays: Medical Services70.484 + Medical Support and Compliance10.372 + Medical Facilities8.886 = **89.742bn**. **[APPROXIMATION]** That fiscal-year mass is transported one-for-one to CY2024, under the parent's declared FY-to-CY rule. BEA investment, CFC, sales, purchased-care, territory and timing adjustments are not performed. The separate medical TEF amount is outside this three-account approximation. This is not an observed NIPA decomposition or an observed group-specific VA-use effect. Sources/hashes: `inputs/medical_bridge.json`, `inputs/va_medical_fy2024_excerpt.txt`.

**Community-care classification resolved:** [BEA County Personal Income Concepts and Methods, Part V p58, paragraphs5.43–5.44](https://www.bea.gov/system/files/methodologies/BEA-County-Personal-Income-Concepts-and-Methods.pdf#page=68) puts veterans' community care in personal current transfer receipts and describes payments to private providers when VA cannot provide care. The pinned NIPA T3.12 line20 footnote4 also includes private-facility reimbursements from2015. Thus Community Care is excluded from central government consumption. Its full FY account is not equated to the CY veterans-other transfer total. Exact source excerpt/hash: `inputs/bea_va_community_care_excerpt.txt`. [SOURCE; INFERENCE]

### Frozen-endpoint changes

| Set | v8 + revised13 low / high, $bn | Item13 change low / high, $bn | Item13 change/member, $ | Result/member low / high, $ |
|---|---:|---:|---:|---:|
| set | 346.873491490 / 437.063345823 | -18.918438766 / -18.918438766 | -418.271340 | 7669.091614 / 9663.116158 |
| cash | 262.834124910 / 353.023979244 | -18.918438766 / -18.918438766 | -418.271340 | 5811.049367 / 7805.073911 |

The denominator is the unchanged **45,230,062.300759**-member lineage. Each method remains separately evaluated and stored; generation conventions a/b are the existing canonical method-mean generation account. The figures are conditional fixed-defense accounting changes at frozen endpoints. [FRAMING-SENSITIVE; CALCULATION]

### Line and generation changes

All cells below are $bn/year and apply at both ends in both sets. The existing source keys and generation routing are held fixed. All engine/completion/coverage parts, including zero-valued alternative carriers, are exported in `derived/item13_by_generation.csv`; arms also retain full generation parts in `derived/case_changes.json`. [CALCULATION]

| Convention | Part / source line | G1 | G2 | G3+ | Total |
|---|---|---:|---:|---:|---:|
| a | compensation / `veterans_pension_disability` | -0.617550058 | -3.711914960 | -5.815071199 | -10.144536217 |
| a | extension / `veterans_other` | -0.161011663 | -0.577943699 | -1.081097212 | -1.820052574 |
| a | extension / `veterans_readjustment` | -0.039747821 | -0.238912665 | -0.374279629 | -0.652940115 |
| a | extension / `veterans_life_insurance` | -0.001566743 | -0.009417241 | -0.014753012 | -0.025736996 |
| a | extension / `military_medical` | -0.036785933 | -0.134203191 | -0.199192614 | -0.370181737 |
| a | va_medical / `health_services` | -1.464899956 | -1.696993025 | -2.743098146 | -5.904991128 |
| a | Revised item13 | -2.321562174 | -6.369384779 | -10.227491813 | -18.918438766 |
| b | compensation / `veterans_pension_disability` | -0.617550058 | -3.743568611 | -5.783417548 | -10.144536217 |
| b | extension / `veterans_other` | -0.166905258 | -0.576316370 | -1.076830946 | -1.820052574 |
| b | extension / `veterans_readjustment` | -0.039747821 | -0.240950011 | -0.372242282 | -0.652940115 |
| b | extension / `veterans_life_insurance` | -0.001566743 | -0.009497547 | -0.014672705 | -0.025736996 |
| b | extension / `military_medical` | -0.075321435 | -0.122139982 | -0.172720320 | -0.370181737 |
| b | va_medical / `health_services` | -1.684309631 | -1.626455838 | -2.594225658 | -5.904991128 |
| b | Revised item13 | -2.585400946 | -6.318928359 | -10.014109460 | -18.918438766 |

Convention a uses each person's own generation; b uses the existing linked-parent/minor routing. The typed coverage source's own generation attribution is retained in both conventions. Each part/source-line/population's before, after and delta closes to the union at1e-9bn. [CODE; CHECK]

**VA medical application and item12 interaction:** the selected mass divided by the current `health_services` national amount308.358754899bn gives fraction **0.291031140106251**. Its current `health_other` key is retained. Only the VA subblock takes response0. The residual federal/state/local health consumption, civilian OPEB amount, state-price corrections and mixed health capital are held fixed. The medical changes by population are engine **-5.636002465bn**, completion **-0.063806446bn**, coverage **-0.205182217bn**. Only item12's matching typed health spending parts are repriced; its mixed-unit, capital, calibration and other source-line parts are held fixed. [CALCULATION; CODE]

Items9–11 are held fixed; item10's native cells and selected completion carriers are already included once. The accepted compensation and four full service-benefit extensions remain **−10.144536217 / −2.868911422bn**. Items14/15 are disjoint and unchanged. VA capital and the other unbridged military subblocks remain outside this item. [CODE]

### National-mass arms

| Arm | National mass, $bn | VA medical change, $bn | Full item13 change, $bn | Full item13/member, $ |
|---|---:|---:|---:|---:|
| va_medical_services_only | 70.484 | -4.637821696 | -17.651269334 | -390.255251 |
| central | 89.742 | -5.904991128 | -18.918438766 | -418.271340 |
| va_medical_four_accounts | 121.130 | -7.970310170 | -20.983757808 | -463.933869 |

The arms use the same key, responses, endpoints and other items in set/cash. The all-four-account arm is the requested scope diagnostic: Community Care is classified as a transfer, already represented by the separate `veterans_other` removal. Adding it to consumption risks overlap. These arms are not confidence bounds or exact BEA consumption estimates. [SOURCE; APPROXIMATION]

With unchanged items14/15 also applied, the fixed-endpoint additive check is **342.487704559 / 432.486522684bn**, cash **258.448337980 / 348.447156105bn**. No v9 adoption or endpoint optimization is performed. [CALCULATION]

### Validation and handoff

- 2026-10-15 12:13:53 JST: full build and **22 tests passed**, exit0; 38.597620s; peak531,316,736bytes RSS.
- 2026-10-15 12:14:49 JST: canonical rerun **IDENTICAL: 34/34 files unchanged (backup removed)**, exit0; 42.564709s; peak431,570,944bytes RSS.
- Changed Python compiled in memory; all three changed CJS files passed `node --check`.
- First build correctly failed a new test's assumption that synthetic completion carriers use the source key directly; they use engine key `k`. Corrected the test to check selected health carriers and zero alternatives, then reran the complete suite.
- Scoped native Astra read-only code review: PASS for the scoped L1 step3 implementation. No material correctness defect confirmed. Receipt: `l1-step3-code-review.md` in task scratch.

Every changed or regenerated persistent path is enumerated in `L1-step3-changed-paths.md` in task scratch; `L1-changed-paths.md` links this supplement. No git writes or peer-lane edits. Python `perf_counter` and `resource.getrusage` supply timing/RSS; `/usr/bin/time -l`, `ps` and `sysctl` were not used.

## Item 21

**Verdict:** The restricted-payer central key raises the residual's measured allocation materially. At fixed personal ends16/11, the standalone item adds **$24.042151050 / $24.370900274bn** to v8, identically in set/cash. On the preserved prior v9 principal at its common capital rate, the direct item adds **$24.068802708bn at both ends**; item16/17 count interactions are separate below. These are conditional use-proxy calculations, not an observed causal fiscal effect or an adopted case. [CALCULATION: derived/item21_case_changes.json; FRAMING-SENSITIVE]

### National mass and source construction

The current line is308.358754899bn: federal179.700 plus state/local126.839 plus health OPEB1.819754899. The VA consumption approximation89.742bn stays on its old key and retains item13's zero response. Item21 replaces the key only on **218.616754899bn**, the line times one minus the VA fraction. Residual plus VA closes to the national line within1e-9bn. `state_price_health_services` follows the new key. Fixed user-fee offsets retain their source keys/dollars. [DATA: derived/item21_snapshot.json; CALCULATION: derived/item21.json]

The donor sample, exposure and age×nativity cell means are the source `build/meps_health_transport_2024.py::read_meps/donor_model`: positive person weights, nonnegative ages, known nativity, uninsured-inclusive cell means, and the existing CPS infant exposure exclusion. The new payment variable is **TOTOFD24 + TOTSTL24**. The old variable also includes VA and TRICARE. The 2024 donor masses, $bn, are: [DATA: sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip; CALCULATION: health_residual.py]


| Payer | 2024 donor mass, $bn |
|---|---|
| VA | 64.554760621 |
| TRICARE | 28.723750808 |
| Other federal | 2.848940390 |
| State/local | 6.752310049 |

VA and TRICARE are **90.667503%** of the old donor mass. The new donor mass is9.601250440bn. These are survey payment masses, not the NIPA program composition. The account's CPS-transported raw totals are separately exported for published and row4 weights in `national_donor_mass`; they need not equal the original MEPS masses. Every raw national key normalizes to1. [CALCULATION: derived/item21.json]

The live payload's ethnic construction was traced through `main_case_2026_09_24/package.cjs::medicalShifts` and `generation_account_2026_09_24/run_generations.cjs::scaledSplit`. The all-donor national raw denominator stays fixed; the pooled ethnic ratio changes the Mexican-origin numerator. The published-weight ethnic increment is transported onto the row4 account and reconciled across generations exactly as the source does. The old health translation is rebuilt against the September29 generation payload within1.95e-10bn, then the new-minus-old key is applied to the actual source amounts. This preserves the OPEB scale and later fixed fee edits. Both source generation conventions close to the same total. [CODE; CHECK: health_residual.py::target, derived/item21_gates.json]

**Missing source row resolved explicitly:** the pooled `ratios.csv` has plain `ofd_stl`, but its producer's `WINSOR_MEASURES` omits `ofd_stl`. `health_ratios.py` therefore constructs the requested `winsor_p995` rows inside this lane from the same pooled2016–2024 frame. It imports the source estimator read-only, with PERWT/9, medical CPI, pooled strata/PSUs and joint numerator/denominator covariance. Caps are cell-specific weighted99.5th percentiles across all donors, including zero spenders; a zero cap follows the source's uncapped convention. The ten published plain OFD+STL and ten published winsor other-public rows are independent ratio/SE/count oracles. No producer was edited. [DATA: medical_ethnicity_pooled_2026_09_23/_cache/pooled.parquet, derived/ratios.csv; CODE: health_ratios.py]

### Group shares, old against new

Shares below are percent of the full national health line, with held fee amounts retained; coverage is expressed as a residual-key-equivalent share by undoing only the residual fraction on the changed spending dollars. They are allocation diagnostics, not VA shares under the new key: VA keeps the old amounts. The sum includes the lineage, completion and missing people once. [CALCULATION: derived/item21_shares.csv]


| Population / profile | Generation | Old % | New % |
|---|---|---|---|
| original_union / identified | G1 | 1.581184 | 9.376584 |
| original_union / identified | G2 | 1.804942 | 2.385770 |
| original_union / identified | G3plus | 2.482228 | 2.651210 |
| added_lineage / lineage_later_g3 | G3plus | 0.129012 | 0.169886 |
| added_lineage / lineage_g3_rate_g3 | G3plus | 0.132079 | 0.146492 |
| added_lineage / lineage_g3_rate_white | G3plus | 0.146419 | 0.146419 |
| completion / native_nonreporters | G3plus | 0.004365 | 0.007213 |
| completion / reporters | G3plus | 0.071100 | 0.082295 |
| coverage / source_missing_people | G1 | 0.051162 | 0.372520 |
| coverage / source_missing_people | G2 | 0.086026 | 0.118104 |
| coverage / source_missing_people | G3plus | 0.091447 | 0.106204 |
| All counted parts |  | 6.579964 | 15.562698 |

The added G3 and white profiles use their own source five-year age-band unit models. The white model already uses an OFD/STL-style payer construction, so central white amounts remain unchanged. Item10's observed nonreporters use their own source age-band prices; reporters use their source completion anchors. These are separate population transports: observed union and reporters use their own raw within-generation donor driver; hidden G3/white people use their own age profiles; native children use their own records. This finer allocation assumption differs from collapsing every G3 amount into a single record driver plus a flat net calibration. Every population's changed dollars independently closes to its declared amount. [CODE: health_residual.py; CHECK: test_health_residual.py]

### Fixed-endpoint amounts and arms

All figures are $bn/year. V8 remains unchanged at365.791930255/455.981784589 set and281.752563676/371.942418010 cash before this item. The v9 baseline is the **preserved prior principal**,344.023286152/412.555074128 set and260.390590432/328.922378407 cash, not the live API's exclusion fallback. `inputs/item21_v9_base.json` pins the source summary hash, selected IDs, ends and common real rate; reruns do not regenerate that historical input. The API supplies the health price context only. [DATA: main_case_2026_10_15/derived/summary.json; inputs/item21_v9_base.json; CHECK: health_evaluate.cjs]


| Arm | V8 direct delta low / high | V9 direct delta low / high | V9 item16 delta low / high | V9 conditional item17 delta low / high |
|---|---|---|---|---|
| central | 24.042151050 / 24.370900274 | 24.068802708 / 24.068802708 | -0.065195754 / -0.065195754 | 0.002846072 / 0.002846072 |
| population | 17.810995840 / 18.060017237 | 17.831183974 / 17.831183974 | -0.195436976 / -0.195436976 | 0.000626669 / 0.000626669 |
| no_ethnicity | 17.916369572 / 18.162459844 | 17.936320080 / 17.936320080 | -0.079804556 / -0.079804556 | 0.003125824 / 0.003125824 |
| plain_pooled | 31.195987740 / 31.623139444 | 31.230616876 / 31.230616876 | -0.075068503 / -0.075068503 | 0.003002279 / 0.003002279 |
| old_key | 0.000000000 / 0.000000000 | 0.000000000 / 0.000000000 | 0.000000000 / 0.000000000 | 0.000000000 / 0.000000000 |

Population, no ethnic translation, plain pooled translation and old key are arms, never central. The old-key arm changes every reported population, generation, line, set, endpoint, coverage and count component by zero. Arms are construction diagnostics, not confidence bounds. Source health dollars and item21 deltas are imputation-method invariant; both methods are evaluated, not inferred from one method. [CALCULATION: derived/item21_arms.csv; CHECK: health_evaluate.cjs]


| Base + direct item21 | Set | Result low / high, $bn | Item21 per member low / high, $ |
|---|---|---|---|
| standalone_v8 | set | 389.834081305 / 480.352684863 | 531.552 / 538.821 |
| standalone_v8 | cash | 305.794714726 / 396.313318283 | 531.552 / 538.821 |
| v9_base | set | 368.092088861 / 436.623876836 | 532.142 / 532.142 |
| v9_base | cash | 284.459393141 / 352.991181116 | 532.142 / 532.142 |

Including the separately exported item16 plus conditional item17 increments gives a central combined increment of24.006453026 / 24.006453026bn. This is a signed-price calculation on the existing source coverage/count kernels, not a parent-case adoption or fresh optimization. The per-member denominator above remains45,230,062.300759; item21 changes prices and no population metadata. [CALCULATION: derived/item21_v9_coverage.json]

The direct central pieces at the v9 rate0.020810698764238 are: [CALCULATION: derived/item21_parts.csv]


| Population | Low, $bn | High, $bn |
|---|---|---|
| original_union | 22.903218533 | 22.903218533 |
| added_lineage | 0.143646389 | 0.143646389 |
| completion | 0.036527801 | 0.036527801 |
| coverage | 0.985409986 | 0.985409986 |

### Capital and held exposure

S&L health structures365.979bn follow the new key. In the optional equipment-and-software sensitivity, the87.919783604bn S&L health equipment stock follows the same key when present, with no invented reporter/coverage carrier: its additional item21 change is0.151280866/0.226921299bn at the source2%/3% rates. Federal nondefense health structures106.019bn remain on the old key: the pinned FAAt701 line43 and the capital lane do not supply a VA/non-VA split. No consumption VA fraction is applied to a mixed capital stock. The unbridged federal equipment/R&D split also remains outside this item. [DATA: capital_return_services_2026_09_27/derived/engine_components.json; CODE: capital_return.py:675–685,773,840–842; CHECK: test_health_item.cjs]


| Held federal structures exposure | Low, $bn | High, $bn |
|---|---|---|
| engine_bn | 0.133164704 | 0.199747057 |
| completion_bn | 0.001507587 | 0.002261381 |
| coverage_bn | 0.004847945 | 0.007271917 |
| gross_held_return_bn | 0.139520237 | 0.209280355 |
| gross_held_group_stock_bn | 6.976011838 | 6.976011838 |

These are gross old-key exposures before separately held fee offsets, at source2%/3%; they are not a proposed federal re-keying benefit or a debt flow. The national stock is held, including any VA capital embedded in it. [CALCULATION: derived/item21_exposures.json]

### Sparse cells and uncertainty

2024 donor cell n/positive-n and mean dollar use (sampling SE) are below. Positive means OFD+STL>0; these are raw person counts, not effective sample sizes. [CALCULATION: derived/item21_key_cells.csv]


| Age | Nativity | n / positive n | Mean $ (SE) |
|---|---|---|---|
| 0-17 | us_born | 3372 / 39 | 15.833 (5.840) |
| 0-17 | foreign_born | 173 / 3 | 8.330 (6.743) |
| 18-34 | us_born | 2674 / 46 | 12.520 (5.081) |
| 18-34 | foreign_born | 466 / 12 | 65.212 (47.100) |
| 35-49 | us_born | 2458 / 49 | 17.977 (6.643) |
| 35-49 | foreign_born | 872 / 36 | 33.308 (16.489) |
| 50-64 | us_born | 2820 / 69 | 46.701 (23.432) |
| 50-64 | foreign_born | 802 / 42 | 93.764 (74.266) |
| 65+ | us_born | 4177 / 84 | 33.134 (9.759) |
| 65+ | foreign_born | 662 / 15 | 37.545 (18.898) |

Pooled2016–2024 transport ratios, Mexican origin/all donors. Central uses winsor; plain is an arm. Counts are common to both specifications; SEs are the source pooled survey-design ratio SEs. [CALCULATION: derived/item21_ratios.csv]


| Age | Nativity | Winsor ratio (SE) | Plain ratio (SE) | n Mexican / all | Positive Mexican / all |
|---|---|---|---|---|---|
| 0-17 | us_born | 0.821815 (0.160957) | 0.900126 (0.349675) | 12007 / 50220 | 198 / 849 |
| 0-17 | foreign_born | 0.471992 (0.273372) | 0.330510 (0.200071) | 384 / 2083 | 11 / 57 |
| 18-34 | us_born | 0.698366 (0.112879) | 0.630748 (0.187035) | 6461 / 37094 | 138 / 925 |
| 18-34 | foreign_born | 1.725697 (0.258596) | 2.354287 (0.603259) | 2483 / 7593 | 109 / 213 |
| 35-49 | us_born | 1.065143 (0.204577) | 1.005841 (0.358975) | 2733 / 30101 | 104 / 995 |
| 35-49 | foreign_born | 1.510442 (0.185822) | 2.014693 (0.356385) | 4825 / 12703 | 338 / 584 |
| 50-64 | us_born | 0.821735 (0.172208) | 0.995815 (0.473092) | 1784 / 34731 | 103 / 1643 |
| 50-64 | foreign_born | 1.360634 (0.159048) | 1.596899 (0.400972) | 3503 / 10607 | 262 / 569 |
| 65+ | us_born | 1.156375 (0.272767) | 1.423024 (0.593220) | 1351 / 39404 | 60 / 1647 |
| 65+ | foreign_born | 0.922760 (0.315933) | 0.647660 (0.263900) | 1682 / 7235 | 79 / 319 |

The small 2024 payer masses and sparse positive cells make transport noisy; foreign-born Mexican-origin children have only11 pooled positive observations. Pooling and winsorization reduce some sensitivity but do not identify the missing NIPA program composition. **This is a health-use proxy:** the residual combines administration/services with different programs, and their allocation is unmeasured here. There is no IHS-eligible population model in these donor cells, so this key cannot establish IHS spending incidence. No joint fiscal confidence interval is claimed from these ratio SEs; donor and transport uncertainty are not propagated into the account total. [LIMIT; INFERENCE]

### Integration, gates and reproduction

`items.cjs` registers `health_residual_key`, number21, `post_engine`; `deltaParts(21,…)` returns typed line/population/generation parts. `derived/item21.json` supplies source2%/3% dollar and capital-stock deltas. The parent must pass `health_residual_rate = RATE.rateFor(meta.one_rate,s)` when applying the adapter; changing `s.rate` alone does not express item20's selected common-rate post-engine treatment. Missing accounting-set identity, unknown arms, missing stock deltas and non-closing parts fail loudly. [CODE: items.cjs, health_item.cjs]

For parent coverage integration, use **`derived/item21_v9_coverage.json`** and **`derived/item21_v9_count_parts.csv`** at the pinned common rate; `item21_coverage.json`/`item21_count_parts.csv` are the source2%/3% versions. Each arm has `sets[which].scenarios[scenario].ends[end]`, typed `decomposition.line_parts`, declared item12 deltas, count scenarios, and `item_overrides`. Add these **dollar increments** to the existing source coverage/count output; append typed count rows. Preserve the parent's counts and population metadata. The item17 override is joint minus item16; item16 and item17 are not independently additive marginal changes. Capital is revalued before all coverage/count integrations, including adult/minor and generation splits. [CODE: health_coverage.py; DATA: derived/item21_v9_coverage.json]

The parent's coverage replacement must remove the adapter's own `population=coverage` amount exactly once before replacing it with the integrated coverage amount. Items9/11/18, fixed fees, VA and federal health stock stay on their own rules. Items13 and21 share a national line but act on disjoint VA and residual consumption subblocks; S&L capital and state-price corrections belong to21. Item12 and items16/17 are explicitly repriced rather than flat-scaled. Parent noncentral lineage/coverage choices require their own stated transport; the supplied source arms are separately measured and are not silently central prices. No `main_case_2026_10_16` file is written by this lane. [CODE; LIMIT]

Run from repo root:

```sh
sh infra/immigration-fiscal/spending_keys_r5_2026_10_15/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/spending_keys_r5_2026_10_15 "sh {lane}/run_all.sh"
```

Gates cover raw national key closure; residual+VA national mass; old published key/union parity and full old ethnic-translation reconstruction; old-key zero through every source/rate/coverage/count arm; unchanged v8 and frozen prior-v9 baseline; both methods and accounting sets; generation convention closure; separate population closure; typed coverage/count closure; and common-rate capital-only revaluation. Review and measured run receipts are recorded in the item21 append of `L1-result.md`. Timing/RSS use Python `perf_counter` and `resource.getrusage`; dates come from `date`. [CHECK]


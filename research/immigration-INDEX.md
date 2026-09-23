# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

For **what our data show**, first use the [dataset register](immigration-dataset-register.md)
and the relevant analysis README to locate inputs, variables and executed outputs.
The [raw-file manifest](../sources/immigration-fiscal/data/MANIFEST.md) records storage;
the [reproduction-input guide](../infra/immigration-fiscal/REPRODUCTION_INPUTS.md)
records acquisition and joins. Check local availability, including ignored files,
before treating an old roadmap item or an uncomputed table as missing data.

Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.

Status: rows without a tag are live. Memos superseded on 2026-09-05 under the [material inference repair](../decisions/2026-09-05-material-inference-repair.md) are listed once, in the Historical section at the end, with their successors; their bodies are retained verbatim below a `historical-snapshot` marker for provenance and must not be cited as current. Index refreshed 2026-09-16 (session a73215f4). CA vs Texas routing added 2026-09-21.

## Core State

[Measured school growth and pupil-level checks](immigration-school-peer-checks-2026-09-20.md):
actual Texas/California enrollment and staffing; ECLS-K white US-born pupils'
scores conditional on starting scores and school, including retained-K forms.
Mixed classroom associations, explicit uncertainty and causal limits replace
using the illustrative 10% enrollment stress case as an observed change.

[Executed causal checks](immigration-causal-execution-2026-09-20.md): actual
Chalfin crime-data translation and 21 public school-finance synthetic-control models;
count/rate identities, weak-IV intervals, donor influence and calendar limits.
[Incumbent school-capacity harm](immigration-school-capacity-harms-2026-09-20.md)
adds conditional learning-loss estimates and withdraws the old $0/no-harm claim.
Neither exercise adds an identified national dollar term.

Civil custody, criminal offenses and fiscal spending: [detention/crime measurement scope](immigration-detention-crime-and-fiscal-scope-2026-09-20.md). ACS institutional counts cannot separate immigration detention; government custody spending remains a cost, with intergovernmental payments consolidated once.

Crime selection by arrival cohort ([lane](../infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/RESULT.md), ladder 196): Mexico-born arrival cohorts from 1975 to 2019 do not show rising positive selection on custody. Butcher and Piehl's result covers all immigrants and is measured in percentage points. The interstate movers' advantage is their schooling. The 2000 census assigned a US birthplace to most institutionalized Mexican-origin men whose birthplace it allocated, so 2000-census immigrant institutional rates (Butcher–Piehl, Rumbaut) run low for the foreign-born. The size of that bias is under an external count check.

**Detention spending investigation completed through September 20, 2026:**
[FY2024 reconciled accounts, verified custody subtotal and identification limits](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).
Expired-funding records have been acquired and reconciled; the unresolved pieces
are custody allocation and matched local expenses/receipts, not missing account
downloads. Start with the [reuse handoff](immigration-verification-handoff.md#detention-crime-and-spending-reuse-before-researching)
and [specific records needed](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/RECORDS_NEEDED.md).
No exact national total is identified by the examined files; this is not a claim
that such a total is impossible in principle.

Latest complete annual account: [national reconciliation and conditional net effects](immigration-complete-annual-account-2026-09-20.md).
**Adopted main case (September 23): $203–250bn/year conditional net cost to other US
residents.** It adds three changes:
- general government responds at 0.59–0.84 instead of zero;
- courts, police and prisons are charged by use;
- the under-charged part of uncompensated hospital care is keyed to uninsured use.

With non-school education budgets fixed as well, the cost is $159–213bn. The proportional-service
benchmark is $308–341bn ([main-case lane](../infra/immigration-fiscal/main_case_2026_09_23/RESULT.md),
[decision](../decisions/2026-09-23-main-case-general-government-and-use-keys.md)). The September 20
versions were **$165–197bn**, **$121–160bn** and **$270–289bn**; the notes below quote them where
they were computed on them. Production is held fully adjusted while service responses vary;
these transferred short-run assumptions do not identify a long-run effect.
The production term's perfect-substitution assumption now has an executed sensitivity: a
[native–immigrant nest](immigration-production-term-nativity-nest-2026-09-22.md) gives +$17.9 / +$27.1bn
at ε = 3 against +$8.8 / +$13.3bn (ladder 176). The same file's jobs put that elasticity near 6,
where the computed neighbors ε = 5 and ε = 7 give about +$13–22bn and would put the band near
$157–194bn; the directly estimated low-skill elasticities 8.7–17.9 (ladder 181) give
+$10–18bn and a band near $160–196bn. The band is not re-run. These shifts are against the
September 20 band; the same production shifts apply to the adopted one.
Sampling plus donor error is about **±$12bn (1 SE)** per headline case; the September 20 main band's
95% intervals run **$141–221bn** together (not re-propagated for the adopted case), and across constructions the assumptions dominate (ladder 184,
[uncertainty lane](../infra/immigration-fiscal/uncertainty_propagation_2026_09_22/RESULT.md)).
The **$262–357bn** proportional-service grid includes weaker proxy stress tests.
The report now regenerates all category comparisons and composition diagnostics.
Fixed-service cases can be positive; property-receipt and service-quality effects
remain unresolved. See the [response decision](../decisions/2026-09-20-category-service-response.md).
"CBO-informed" covers two inputs only: CBO's tax-incidence rules and its 63–66%
school-spending response with economic-affairs and recreation budgets fixed. Since September 23
general public services respond at **0.59–0.84**, from cross-state scale: administration spending
rises 0.842% per 1% of population. Defense, existing interest and business subsidies stay at
**zero response by assumption**, not by a CBO estimate
([scope memo](immigration-education-administration-scope-2026-09-20.md)).

[Real fiscal and social costs](immigration-real-fiscal-and-social-costs-2026-09-23.md)
(September 23, ladder 188–193) prices the channels the headline left out. Two are now in the
adopted main case:
- courts, police and prisons by use, **+$5.9bn** ($1.7bn with census ethnicity codes as recorded);
- the government part of uncompensated hospital care, **+$3.7–5.7bn**.

Beside the fiscal headline, as social costs:
- crimes by group members against other residents cost the victims **$29bn** a year ($15–45bn;
  $43bn on arrest shares);
- unreimbursed hospital care costs **$3.2–5.6bn**;
- housing nets other residents **+$0.7–3.5bn**, while their renters pay $22–58bn more;
- road congestion costs other residents **$19bn** a year in time and fuel ($8–35bn), with road
  budgets fixed as in the main case.

Wages move **$66–166bn** from less- to more-educated natives. Fiscal plus social costs come to
**$248–307bn a year** at central values ($212–340bn full span). The transfers are not added, but they run from poorer
to richer residents: outside the budget the bottom four fifths lose $80.7bn a year and the top
fifth gains $46.0bn. The fiscal cost is progressive if financed by tax shares and regressive if
by equal cuts per person (ladder 194).

[Objections and answers](immigration-objections-faq-2026-09-21.md): fifteen standard
objections (age, fixed public goods, payroll taxes without benefits, off-budget gains,
second generation, reference group, education, single year, legacy cohorts, ageing,
policy reading, crime, elder care, native–immigrant complementarity, California vs Texas),
each steel-manned and routed to its executed table.

[California vs Texas](immigration-california-texas-fiscal-geography-2026-09-21.md):
same Mexican-origin share (~32%); common-age gap vs **local** whites **−$12,133** (CA) vs
**−$7,479** (TX) on the shared all-age ledger; LA **−$17,196**, Houston **−$7,493**. Share
does not produce the coastal dollar gap. Not the $165–197bn account. NY is 1.4% of US
Mexican-origin; SF has no single-metro gap.

[Seven papers from the Marginal Revolution archive, read in full](immigration-marginal-revolution-leads-read-2026-09-21.md):
headline unchanged. The nursing-home channel is bounded at **$2.3–14.6bn a year** of Medicaid
spending for the Mexico-born ($5.6bn preferred); it transfers weakly because 1.2% of Mexican
immigrants work in health occupations. The 2025 municipal-bond paper cannot identify the
service-response share. The production term's perfect-substitution assumption is now executed
(ladder 176): on this account's jobs the relevant elasticity is near 6, and the term rises by
about half, to roughly $13–22bn; at the direct estimates of ladder 181 it rises $2–5bn. The removal model's $27–80bn is a different population and a
different elasticity (ladder 166).

[Cumulative 2005–2024 back-cast](immigration-historical-backcast-2026-09-20.md):
no past year is measured. Actual BEA budgets, each benefit programme's own series and
ACS population by year, with the 2024 relative position held or income-adjusted, give
**$1.3–2.2tn (10y), $2.0–3.3tn (15y), $2.4–3.9tn (20y)** for the September 20 main net-cost
case, 2024 dollars, no interest; the whole-budget rules alone give $1.4–2.0tn, $2.0–3.1tn and
$2.4–3.8tn. On the adopted $203–250bn anchor the whole-budget rules give **$1.7–2.5tn, $2.5–3.7tn
and $3.0–4.6tn**; the programme-by-programme version is not re-run. 2020–2021 supply 29–39% of the ten-year total under the rules that follow the benefit spike (over a third in the programme version) and 20% under the flat carry. Measured trend (ACS):
per-capita income 0.52→0.61 of the national figure over 2008–2024, median household
income 0.78→0.91, full-time men's earnings 0.64→0.75 with the gain in 2016–2019 and
2021–2023 and none in 2024. Model ranges, not intervals; a measured series needs the
account rebuilt on each ASEC file. Not comparable with ladder 137's forward debt path.

[Executed service-scaling test](immigration-service-scaling-test-2026-09-20.md):
school panel spending elasticity .735 unweighted/.836 pupil-weighted; across-district
prediction favors proportional spending over universal 3/4 or 5/6. Ten state-service
within-panel estimates are imprecise. Complexity theory supplies an exact finite-cost
sensitivity, not another discount on the CBO-informed account.

[Policy effects and new administrative outcomes](immigration-policy-causal-evidence-2026-09-20.md)
checks Secure Communities victimization/reporting, Mariel school spending and
H-2B employer benefits; records the direct Mexican-inflow crime replication route.
Adds a verified 72 MB BEA/IRS county panel, with source units, missing years and
geographic coverage preserved. Immigration-only offenses carry no automatic
victim-harm charge. These findings do not change the conditional national total.

Scope checks: [education and administration](immigration-education-administration-scope-2026-09-20.md)
shows which staffing costs are already included and isolates the general-government
response assumption. The [executed state/local response test](immigration-administration-response-test-2026-09-20.md)
is too imprecise to identify an actual fixed/variable share; the 25% illustration
remains an assumption. [Fourth-generation coverage](immigration-fourth-generation-scope-2026-09-20.md)
now separates observed G3 (2.870m) and G4+ (2.073m), leaving 9.399m unresolved
within the existing G3+ total. Additional checks find 25–32k adjacent-year CPS
candidates and an independent GSS adult benchmark; neither imputes the residual.
Exact G4 versus G5+ remains unmeasured. No fiscal total changes.
[Age-adjusted generation estimates](immigration-later-generation-estimates-2026-09-20.md)
give 3.51–3.83m generic G4+ adults under central assumptions; missing-age and
grandparent scenarios span 2.71–4.71m before sampling error. Historical Pew is
lower, and PSID exact-generation completeness awaits authenticated data access.
[Ancestry and outcomes](immigration-ancestry-outcomes-evidence-2026-09-20.md)
adds a direct Pew schooling comparison of identifiers and nonidentifiers, the
newly acquired historical MASP family data, and the verified SIPP linkage route.
It supplies no national all-descendant fiscal or crime correction.
Later same-day execution completes MASP/Pew sensitivities and stops this search:
public SIPP birthplace fields are region recodes, relevant samples are small,
and PSID's current conditions prohibit the proposed AI use. See the linked
ancestry-outcomes memo's continuation and [stopping decision](../decisions/2026-09-20-ancestry-outcome-data-ceiling.md).
[Program-fraud trace index](immigration-fraud-trace-index-2026-09-20.md) links SNAP,
childcare, adult-day and hospice cases to records, separating paid losses, billings,
allegations and duplicate fiscal attribution. No fraud adjustment has been estimated.

Preceding partial account: [four executed fiscal checks](immigration-four-fiscal-checks-2026-09-20.md).
Measured public-school enrollment raises the partial deficit to **$259.38bn shared
/$283.20bn personal**. Matched-year tax units locate the national income-tax
shortfall mainly at high incomes; healthcare and national-account checks retain
material unresolved scope/attribution. These are all-age resident balances,
not policy effects or confidence bounds. [National coverage detail](immigration-national-coverage-execution-2026-09-20.md).

Gap diagnosis: [which assumptions should change and better data](immigration-gap-diagnosis-and-data-2026-09-19.md)
decomposes the school discrepancy: the fixed enrollment rate explains 63–64% of
the all-child CA/TX shortfall and almost all the national Hispanic shortfall.
Verifies the public October CPS enrollment route, matched-year tax comparisons,
health-data boundaries and restricted-access limits. National accounting coverage
remains the larger completeness issue; execution is linked above.

Executed reality checks: [administrative earnings, benefit totals and pupil counts](immigration-administrative-checks-2026-09-19.md)
compare the uncalibrated model with unused official observations. National wages
are 2.25% above SSA employer records; wage-recipient and payroll coverage still
differ. The receipt-gap mechanism survives this check. Pupil exposure and older
benefit-reporting factors need refinement; the memo separates raw errors from
uniform-calibration sensitivities. These do not validate a causal ethnic cost.

Test design: [necessary fiscal implications and administrative tests](immigration-fiscal-reality-checks-2026-09-19.md)
shows that the current partial account assigns lower receipts **and lower spending**
per Mexican-origin resident than per other resident. Priorities are tax/earnings
distributions, current transfer totals, Medicaid eligibility costs and public-pupil
counts; CA/TX records and source-reuse limits are linked. Read the executed results
above for the outcome; exact state administrative-eligibility matching remains unavailable.

Previous three checks: [observed2024 fiscal refresh and national reconciliation](immigration-macro-reconciliation-2026-09-19.md)
produced the **$234.34bn shared/$256.26bn personal** annual version, superseded by
the September20 enrollment correction above;
[matched skill/capital/tax benefits](immigration-matched-benefits-2026-09-19.md)
gives $6–19bn long-run production gains in the source-centered grid, with larger
conditional capital-tax effects requiring ownership/overlap accounting;
[projection back-tests](immigration-projection-backtest-2026-09-19.md) find the
NRC debt rule failed, no general optimistic schooling bias, and material
education/parentage/exit sensitivities. These govern the older releases below.
They are calculation notes, not a complete net-cost estimate or narrative essay.

Fiscal scale and benefits: [population-normalized comparison, national reconciliation and production-benefit scenarios](immigration-benefits-and-macro-scale-2026-09-19.md) reports the per-person fiscal gap, macro anchors and remaining national coverage, and a same-population earnings extraction with an illustrative $13–26bn fixed-capital benefit channel. It is not a total welfare estimate or bound; sector price estimates cannot be added without matching populations and overlap.

Education-specific fiscal evidence: [annual comparisons, lifetime uncertainty and methods](immigration-education-fiscal-and-methods-2026-09-19.md) separates below-HS from HS-only, five origin regions, current stocks and recent arrivals; retains same-education and all-education native references. Adds joint survey uncertainty, material healthcare-matching tests and explicit institutional-cost scenarios. Below-HS Mexican-born adults outperform below-HS natives in the baseline common-age comparison, while HS-only do worse; this qualifies blanket origin-based rankings. These remain resident-account models, not admission effects.

Earlier repaired fiscal profiles: [yearly and lifetime results](immigration-yearly-lifetime-cost-repair-2026-09-19.md). The $217.32bn/$239.24bn annual source vintage is superseded by the finance refresh and September20 school correction above. Lifetime comparisons retain pinned age profiles, conditional survival and explicit discount/allocation assumptions; they are not validated admission forecasts. The [September19 cross-check](immigration-five-day-cross-check-2026-09-19.md) and birth-versus-arrival budget remain superseded/withdrawn. Narrative and essay writing are operator-owned.

[Practitioner range for the September 19 ledger](immigration-ledger-practitioner-range-2026-09-22.md):
the conventions a budget modeler would run put the union's annual expanded balance at
**−$290bn to −$190bn** around −$217bn (ladder 172); the full 63-cell design spans −$496bn to
−$76bn, and the −$548/−$87bn range still printed in the ledger's RESULT.md is the stale
September 17 build. Public goods per capita is a second object (−$502 to −$402bn). Convention
hulls, not confidence intervals.

Consistent accounting and raw histories: [all-age fiscal and later-generation findings](immigration-all-age-and-lineage-findings-2026-09-17.md) rebuilds the expanded account on one population with CPS/MEPS uncertainty, tests fixed-budget attribution and common ages, and reconstructs IIMMLA generations/outcomes. Large benchmark shortfalls persist; absolute partial balances, allocation effects and outcome-specific generation differences are reported separately (ladder 123–124). Within-state and metro matching: CA **−$12,133** / TX **−$7,479** vs local whites; LA **−$17,196** (ladder 125, 128). Pair with the [CA–TX geography note](immigration-california-texas-fiscal-geography-2026-09-21.md).

All-age claim audit: [fiscal benchmark gaps, remittances and later generations](immigration-aggregate-and-generation-audit-2026-09-17.md) reproduces the $212bn/$153bn partial-account differences, exposes their positive absolute balance, and corrects the remittance ceiling and incompatible ancestry definitions.

Country comparisons: [five-year LATAM economic comparison and dataset expansion](immigration-latam-benchmark-comparison-2026-09-17.md) uses explicit birthplace benchmarks, first/second generations, common age/sex standards and survey uncertainty; distinguishes measured economic gaps from crime, trust, fiscal and genetic claims.

Expanded transfer check: [other LATAM countries, distance selection and the Somali counterexample](immigration-latam-selection-transfer-2026-09-17.md) compares origin/cohort outcomes and narrows the earlier BA-share selection interpretation; distinguishes evidence for individual genetic effects from unsupported genetic attribution of migrant-group differences.

Origin scope and trust: [LATAM, Southeast Asia and social trust](immigration-latam-southeast-asia-trust-2026-09-17.md) checks the latest located unauthorized-origin stock estimates, limits Mexican-to-LATAM extrapolation, separates Southeast Asian economic outcomes, and weighs local cooperation costs against claims of inevitable or centuries-long trust decline.

Latest executed frontier: [stronger findings and remaining limits](immigration-frontier-execution-2026-09-17.md), with [reproduction and coverage](../infra/immigration-fiscal/frontier_execution_2026_09_17/README.md). Adds official NLS variance validation and adult outcomes, three-year disability and full-denominator trust, NYC exposure accounting, fiscal reconciliation, raw-mirror Bracero wage reconstruction, and bounded H-2B/automation/institutions checks (ladder 115–120). These qualifications govern earlier score, trust, disability and fiscal headlines.

Research priorities: [stronger questions across domains](immigration-research-question-frontier-2026-09-17.md) separates verified descriptions, policy identification, transfer and value judgments; ranks remaining score, selection, incidence and causal-design work; and marks cultural/institutional/environmental questions needing their own outcomes.

Latest completed collection analysis: [organized surveys and conclusions](immigration-organized-surveys-analysis-2026-09-17.md), with [NLS parent reconstruction](immigration-nlsy97-parent-linkage-2026-09-17.md), [Pew generations and denominators](immigration-pew-generation-denominators-2026-09-17.md), and [public LNS author replications](immigration-lns-public-replications-2026-09-17.md). These update the earlier audit below (ladder112–114). [Named local library](../infra/immigration-fiscal/new_datasets_2026_09_17/library/README.md) accounts for the downloads and their duplicates.

Latest supplied-data audit: [immigration-new-datasets-and-conclusions-2026-09-17.md](immigration-new-datasets-and-conclusions-2026-09-17.md) covers all13 files, valid joins, Pew ancestry selection, NLS export gaps and recovered outcomes, GSS coding repairs, and corrections to CILS/IIMMLA floor/parity interpretations (ladder107–111).

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-political-trajectory-county-panel-2026-09-19.md` | County panel 2000–2024: Mexican-origin share growth has no effect on Democratic share or turnout with state×year FE; composition worth +0.29 points nationally vs −2.80 from the group's own swing; CA–TX gap is conversion not composition (66 vs 23 in low-Mexican counties); tuition laws track group size, restrictive laws track the rest of the electorate | Any "they vote us into X" or vortex claim; the input side of ladder 97/102; the CA–TX comparison |
| `immigration-lineage-cost-century-2026-09-19.md` | Historical conditional −$1.30M white-reference lineage gap; incomplete coverage, 101 original intervals, no validated admission cost. Current projection checks qualify education, parentage, policy and exit assumptions | Any lifetime/lineage figure; read projection checks first |
| `immigration-mexican-origin-population-total-2026-09-19.md` | Mexican-origin population by generation: 40.97M self-ID, 42–45M with attrition and coverage (floor 41.8M); Duncan–Trejo attrition reproduced and found halved (third generation 11% vs 28%); ancestry question gives fewer, not more; attriters narrow the per-person gap by about $230 (−$7,152 → −$6,921 on the September 19 ledger) | Any total for the Mexican-origin lineage; any attrition correction; the 0.82 coverage-ratio trap |
| `immigration-unauthorized-population-size-2026-09-19.md` | Unauthorized stock by definition (broad 14.6–16.7M for 2024–25, narrow 8–9.5M), coverage grid (PES 4.99% vs CMS 22%; ACS/CPS weights already embed the 2024 migration revision), stock-flow 16.7M for Jan 2025, falling since; no definition reaches 40M | Any unauthorized headcount; any claim of 20M+ or 40M; comparing the CPS residual to gross inflows |
| [Parents' legal status by education](../infra/immigration-fiscal/parent_status_2026_09_23/RESULT.md) | 2026-09-23, ladder 185: Mexico-born parents of US-born minors, imputed unauthorized: below high school 47–62% (1.51M parents), high school 37–52%, all 38–51%; US-born minors in the lowest-education Mexican families with no legal parent present 45–62%, all 30–41% (5.0M children). Current status, not status at birth; range is the Medicaid rule. Ladder 186: their US-born children do worse while parents stay unauthorized (poverty +10–20 pts, college −12–14 pts at 18–24, CPS 2025) and match legal entrants' children once parents legalized (IIMMLA 2004). Ladder 187: of Mexican adults getting green cards in 2003, 55% had once entered without papers and 77% of those used 245(i), closed to post-2001 petitions; about 1% of unauthorized Mexicans legalized that year; 2026 routes need a citizen or resident spouse or parent (I-601A, interview abroad), cancellation of removal (4,000 a year) or a U visa (288k pending); a US-born child cannot waive a parent's ten-year bar | Birthright-citizenship questions; any claim that low-skill parents are almost all unauthorized; "children of illegals do worse/better"; "how easy is it to get legal status" |
| `immigration-cultural-output-and-variety-saturation-2026-09-19.md` | Creative labour per head at matched SES 0.72–0.74 of whites (music at parity), awards 0.47→0.65 of the BA+ benchmark, Mexican-restaurant variety elasticity 0.18 in group share (saturates by a 10–20% local share; national counterfactual not identified), 12% of US cooks Mexico-born, Latin music 8–9% of revenue | Any "cultural enrichment" or "contributes nothing" claim; any argument that variety benefits scale with population |
| `immigration-hedonic-replay-2026-09-19.md` | Original-data replay recovers all six historical coefficients/SEs and stronger IV diagnostics; matched historical means and medians both negative. Modern exercise is not equivalent; old custom J output disabled | Read before claiming a replication failure, era change or identified composition-amenity price |
| `immigration-hedonic-composition-amenity-2026-09-19.md` | Contemporary housing sensitivity exercise: matched ACS/Zillow outcome sensitivity and no identified amenity dollar price. Exact-reproduction and established measurement-explanation claims superseded by the replay note | Any attempt to dollarize neighbourhood composition or reuse Saiz–Wachter's historical estimate today |
| [Clemens–Pritchett calibration](immigration-clemens-pritchett-calibration-mexican-origin-2026-09-19.md) | Equations and parameter sensitivity reproduce; earnings/fiscal/attitude substitutions do not measure the paper's TFP-assimilation rate, so the negative optimum is conditional | Reusing the new institutional-transmission framework |
| `immigration-local-spending-composition-2026-09-18.md` | Local-budget associations do not show the predicted law-and-order shift; failed IV does not prove a null and treatment differs from unauthorized-arrival study | Claiming causal spending effects or a replication failure |
| `immigration-ncvs-victim-offender-off-the-murder-margin-2026-09-18.md` | Victim/perceived-offender distributions; corrected Hispanic $90.91 annual CJS scenario reproduces, but severity is imputed and victim ethnicity does not identify taxpayer incidence; age adjustment is a proxy | Separating measured incident distributions from cost scenarios |
| `immigration-apportionment-seats-attributable-2026-09-18.md` | 24-seat fixed-location count counterfactual for Mexican-origin residents; depends on size and uneven geography; not ethnic seat ownership or an immigration-policy/election effect | Representation counterfactuals |
| [Current yearly/lifetime calculation index](immigration-yearly-lifetime-cost-repair-2026-09-19.md) | Repaired program ownership, personal/shared annual balances, actual-age survival NPVs, real discounts and explicit unresolved coverage | Reusing any September yearly or lifetime scalar |
| [Practitioner range, Sept 19 ledger](immigration-ledger-practitioner-range-2026-09-22.md) | 2026-09-22, ladder 172: practitioner hull −$290 to −$190bn around −$217bn; design hull −$496 to −$76bn (+$41bn with the dial at zero); public-goods object −$502 to −$402bn; stale 144-cell range stamped | Quoting any range for the ledger, or choosing between its conventions |
| [Elderly public medical by ethnicity, MCBS 2023](immigration-elderly-medical-by-ethnicity-2026-09-22.md) | 2026-09-22, ladder 173: Hispanic/white public payments at 65+ 1.27 (CI 0.97–1.56), total spending equal, Medicaid 9×, income reverses the sign; with the MEPS Mexican-origin check (ladder 175) the 65+ ethnicity dimension is unsigned, about −40% to +56% | Any claim about elderly medical cost by origin; the re-aged and lifetime 65+ cells |
| [Mexican-origin medical on the transport's MEPS file](immigration-mexican-origin-medical-transport-check-2026-09-22.md) | 2026-09-22, ladder 175: Mexican-origin/all-donor public spending 0.89 at 65+ (CI 0.61–1.18), 0.69 at 18–64 (excludes 1); Medicaid 3.3× but Medicare, out-of-pocket and private lower; 65+ translation $2.7bn less (SE 6.7); all-ages unusable (one record) | Any ethnicity adjustment to the medical transport; read with the MCBS row |
| [Production term under imperfect substitution](immigration-production-term-nativity-nest-2026-09-22.md) | 2026-09-22, ladder 176: native–immigrant nest inside the skill cells doubles the production term at ε = 3 (+$27.1 / +$17.9bn GDP / cash against +$13.3 / +$8.8bn); natives +$54bn, other foreign-born −$46bn, about 85% nets out. Job overlap on the same file centers the elasticity near 6 (sketch about 4–9); the computed neighbors ε = 5 and ε = 7 give +$21.5 / +$14.2bn and +$19.2 / +$12.6bn. Union-as-own-branch variant structurally unverified; headline band not re-run | Any reading of the account's production term or the removal-model comparison (FAQ 14) |
| [Return migration selectivity, ENADID 2018/2023](immigration-mexico-return-migration-selectivity-2026-09-22.md) | 2026-09-22, ladder 174: returnees from the US hold about one year less schooling than Mexico-born stayers (tertiary −12 to −14 points), men only; short-window returnees are better educated (22–28% tertiary); departures unmeasured on schooling | Any attrition or exit assumption; reading US arrival-cohort education trends |
| `immigration-lifetime-longevity-and-social-security-timing-2026-09-18.md` | Historical mortality/timing study; flat-shift results superseded by current calculation index; invalid SSA accrual adjustment disabled | Tracing earlier lifetime claims |
| `immigration-marginal-revolution-claims-audit-2026-09-18.md` | Source archive and commentator comparisons; schooling-loan HARD grade and claim totals withdrawn by the September 19 audit; resident accounting is not a full cost-benefit analysis | Reusing a commentator rebuttal |
| `immigration-first-generation-crime-cost-weighted-2026-09-18.md` | Texas all-age cost-weighted foreign-born charge ratio 0.79 vs all US-born; adult/18–39 versions change denominators only; DHS-record explanation corrected | Comparing status, age and charge denominators |
| `immigration-new-conclusions-audit-2026-09-17.md` | Adversarial correction of fertility, automation, disability, agglomeration and political-cost conclusions; proposed family-migration-history classification with public/restricted data limits | Reusing ladder 93–97, the political dollar range, or “third generation” as a complete ancestry category |
| `immigration-clarity-update-2026-09-05.md` | Current integrated findings: fiscal account, Black wage/crime groups, missing residents and recording failures | Answering what the completed audit and data expansion established |
| `immigration-second-order-effects-2026-09-05.md` | Concise evidence by mechanism: incumbent welfare, capacity, institutions and conditional restrictions | What second-order costs establish, and what remains unmeasured |
| `immigration-fiscal-account-2024-2026-09-05.md` | CPS2025 taxes/credits/transfers, MEPS2024 health and actual public-pupil exposure | Comparing annual fiscal components beyond the older payroll proxy |
| `immigration-measurement-uncertainty-2026-09-05.md` | Missing status versus missing people; two-sided selection and crime recording thresholds | Treating untracked residents or selective enforcement as a settled correction factor |
| `immigration-wage-race-strata-2026-09-05.md` | ACS2019/2024 race × nativity wages, earnings, employment and worker-only estimates | Pooling Black, White and Hispanic native/foreign-born wage populations |
| `immigration-crime-race-ethnicity-2026-09-05.md` | BJS2022/2023 imprisonment rates and SPI2016 joint prisoner composition | Separating Black people in crime statistics or treating White as non-Hispanic/native |
| `immigration-crime-statistics-bias-mechanisms-2026-09-16.md` | Mechanisms by which immigrant-vs-native crime statistics mislead: status-identification timing, residual relabelling, exposure denominators, immigration offences as crime, non-recording of ethnicity; signs and magnitudes | Citing any immigrant/native crime ratio without its extract date, denominator definition and offence scope; evaluating "police won't record" claims |
| `immigration-generational-crime-mechanisms-2026-09-16.md` | Why first-generation immigrants offend less than the second: 2018–2026 within-family, survival, register and quasi-experimental evidence; the gap is an adult-arrival floor; mechanism scoreboard (legal status, parental resources, peers, selection, culture, measurement); European age-standardization and widening residuals; new angles | Any claim about "the second generation" and crime, generational assimilation, age at arrival, or what causes the first-generation advantage |
| `immigration-mexican-origin-generation-incarceration-2026-09-16.md` | Central memo, §1–§18 (ladder 65–97, corrections 98–103, then 104–106): the 3.5× recomputed (1.7–1.9×, 1.68× pooled 2020–24); generation shares; origin cells; offence mix; EU data regimes; Pueyo repro; mechanisms and the origin-mean regression; the September 16 extended per-adult-year ledger (historical; the September 19 same-age second-generation gap is −$7,521) (−$8.3k to −$8.9k second generation, status split, residuals, remittances, disability); housing/capacity/schools/coercion/agglomeration; consumption and wealth; attitudes by generation; automation (unpriced); political externality (proposed dollar range withdrawn by September 17 audit) | Any "second generation counted as native" argument, the 3.5× figure, or a Mexican vs other-origin comparison |
| `immigration-secgen-origin-divergence-mechanisms-2026-09-16.md` | Why second generations diverge by parental origin: ranked mechanisms with identification grades (parental legal status 1.24 yr IRCA-IV; parental English A− IV; attrition both directions; selectivity small at individual level; no identified ethnic-capital or resettlement estimate; family structure wrong sign); five CPS/ACS tests | Any claim that culture, discrimination, selectivity or legal status explains an origin gap in second-generation outcomes |
| [Indian-origin residents: treasury, coordination, giving, vote](immigration-indian-origin-fiscal-coordination-politics-2026-09-18.md) | Favorable working-age partial-ledger contrast; raw/conditional civic participation and approximate uncertainty; cross-survey education benchmarks do not identify a voting decomposition; adjudicated favoritism limited to one firm | Origin comparisons on matched accounts and civic populations |
| [Indian 2nd/3rd generation at white ages](immigration-indian-later-generation-fiscal-2026-09-21.md) | 2026-09-21: G2 age-std gap **+$23,692 (se 5,482)** on the 2025 extended ledger; G3+ race/ID n=49, **+$11,806 (se 8,150)**, does not reject white parity; 5-year own-tax G3 **+$4,101 (se 3,880)** with 2023 below whites; ACS US-born Asian Indian 25–64 mean PINCP **+$59k** vs US-born NH whites, 65–80 cell below. IT mix is **8%/4%** of the CPS-G2 / ACS-ancestry employed-earnings gap; dropping IT leaves G2 at +$47k. H-1B is G1 only (proxy 30% of India-born 25–64, lowest-net G1 arm) | Same-age Indian descendant fiscal claims; “they only look good because they are young”; treating native self-ID as G3; “it’s all software/H-1B” |
| [Indian vs white physicians: malpractice and fraud](immigration-indian-physician-malpractice-fraud-2026-09-21.md) | 2026-09-21: no US Indian-vs-White malpractice or fraud rate (NPDB has neither race nor school country). IMGs: fraud exclusion aOR **0.95** (ns), any exclusion **1.30**, health-crime **1.62** (Chen/Jena 2018). US paid-claim difference vs USMGs is small/null nationally (GAO 2010); Illinois ~1.2× paid claims, not more discipline; Caribbean not India is the negligence outlier. Rankings are AU/UK *school-country* complaint rates: India OR **1.61** in Australia (7th of named high-risk countries), UK GMC performance assessments ~**5×** UK-trained (mid-pack; Bangladesh 13×). Medicare internist IMGs have *lower* 30-day mortality (Tsugawa 2017) | “Indian doctors are worse / more fraudulent”; mixing IMG with Indian-origin; transferring UK GMC rates to US NPDB |
| [High-education origin screen](../infra/immigration-fiscal/high_skill_origin_screen_2026_09_21/RESULT.md) | 2026-09-21, ladder 168: 19 birthplace groups on the education-by-origin account; none clearly negative; Philippines-born at zero for an age reason; degree holders from Venezuela (−$19,402) and Pakistan/Bangladesh (−$12,947) far below native degree holders, India +$7,545; Russia/Ukraine-born positive, with 42% of their elderly on Medicaid (ACS), which the account does not see. Ladder 169: at the native age mix India +$29,174 → +$21,832, Venezuela → −$877, Mexico → −$5,684; ordering survives | "High-skill immigrants are all fiscally positive" claims; "young groups only look good" objections; choosing an origin for an ACS-based account (Bangladesh, Armenia) |
| [Muslim-majority origins: fiscal position, attitudes, extremism counts, mosque funding](immigration-muslim-origins-funding-outcomes-2026-09-21.md) | 2026-09-21: high-education Muslim-majority birthplaces fiscally positive, weak groups are refugee-route origins and Bangladesh; Pew 2017 (religion observed): degrees and $100k+ incomes at the public's rate, more under $30k, violence rejected at the public's rate; Cato: 3,046 murders by foreign-born terrorists in 50 years, 97.8% on 9/11, native-born not counted; Europe much worse and its author says it does not transfer; mosque funding has no ledger by statute, survey has no foreign item, median budget $80k; Alavi (Iran) litigation status unverified; **2026-09-22 microdata (§2a, ladder 177):** nativity does not move the attitude items, the violence figure is foreign-born South Asian and reversed by their US-born children, US-born Muslims are two populations; **NIS 2003 cohort (§2b, ladder 179):** the Muslim employment deficit at admission (−10.4 points) is composition (−0.8 with country of birth) and the pay-rate gap is zero | Questions about Muslim immigrants, Islamism or mosque funding; Europe-to-US transfer claims |
| [Second generation by parental origin, IPUMS-CPS 1994–2025](immigration-second-generation-by-origin-2026-09-22.md) | 2026-09-22, ladder 178: the US-born children of Mexican immigrants close 76% of the first generation's no-high-school gap but 31% of the college gap (−29.8 → −20.6 points against third-plus non-Hispanic whites at the same age, sex and year), 59% of employment, 66% of log income; self-identified third-plus Mexicans sit at the second generation's level; 1994–2025 the second generation's college gap widened (−17.4 → −22.5) while its no-high-school gap narrowed and its income gap stayed flat; Mexico is the only top-ten parental birthplace whose second generation is behind on college. Descriptive, cross-sectional; SEs are lower bounds | Any claim about convergence or stalling by generation; FAQ 5; the generation ledger's flat first-to-second fiscal gap |
| [Admission route against origin religion](../infra/immigration-fiscal/admission_route_2026_09_21/RESULT.md) | 2026-09-21, ladder 171, design fixed before the data: across 66 birthplaces the employment-route share predicts how a degree converts (+29 points of degree holders earning $100k+ from 10% to 50% employment route); the origin's Muslim share carries no earnings penalty among degree holders and predicts women's employment 13–17 points lower whatever the route; by the pre-set rule the test is not settled; ecological | "Is it the origin or how they were admitted?"; claims about Muslim-majority origins; routes as the policy lever |
| [Military service by ancestry](../infra/immigration-fiscal/civic_service_by_ancestry_2026_09_21/RESULT.md) | 2026-09-21, ladder 170: US-born men of Asian Indian ancestry ever on active duty 1.05% against 6.6–7.8% for English, German, Irish ancestry; holds among degree holders and at ages 25–34; Korean and Filipino at the white rate, Mexican-ancestry degree holders above it (8.2%); parental income and metro not held constant | Questions about civic attachment of high-skill groups; a behavioural companion to ladder 152's giving, volunteering and turnout |
| [Homicide victims, offenders and treasury cost](immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md) | Cleared-case victim/offender distributions; $1.5–1.8m treasury scenario assumes conviction and prison sentencing, not an expected cost per cleared case | Reusing homicide cost or victim-incidence figures |
| [Enclave neighborhood quality and informality](immigration-enclave-neighborhood-quality-and-informality-2026-09-18.md) | 2026-09-18 | AHS 2023 at equal income/tenure/metro/crowding: Mexico-born householders no likelier in inadequate units, fewer abandoned buildings, better neighborhood ratings; only trash-within-half-block survives (+0.87 pp, Hispanic; ns for Mexican origin); SF inspector litter association falls two-thirds within neighborhoods, Mexican-origin t 1.5; LA 311 income-driven; Mission Street storefronts 90.9% registered vs 83.6% citywide, Chinatown 90.5%; H2 falsified | Any "they can't maintain their neighborhoods" or "those shops aren't legit" claim; AHS neighborhood-item coding |
| [School flight and public goods](immigration-school-flight-and-public-goods-2026-09-18.md) | School-flight effect unestablished; district revenue associations and state aid responses; voucher evidence includes non-test-score benefits, so immigration-attributable defensive tuition remains unpriced | Interpreting school choice and public spending |
| [Native displacement onto transfers](immigration-native-displacement-to-transfers-2026-09-18.md) | Adverse-to-hypothesis associations coexist with failed identification; not a causal null; baseline association is a diagnostic, and single-instrument scalar sign does not change 2SLS | Claims about displacement onto welfare or disability |
| [California vs Texas fiscal geography](immigration-california-texas-fiscal-geography-2026-09-21.md) | Same ~32% Mexican-origin share; CA −$12,133 vs TX −$7,479 vs local whites (shared all-age ledger); LA −$17,196 vs Houston −$7,493; NY 0.50m; SF gap not estimated; not the complete-account total | "It's just California"; "share catching up explodes the national gap"; asking for SF/NY |
| [Metro-matched gaps](../infra/immigration-fiscal/metro_match_2026_09_17/RESULT.md) | National per-person gap unchanged by metro matching (−$5,734 → −$5,797 vs whites); six published metros all adverse; nominal $, no PPP | Single-metro vs-white figures; claiming geography matching erases the gap |
| [Native sorting (Tiebout)](immigration-native-sorting-tiebout-2026-09-18.md) | CA and TX already at the same Mexican-origin share; IRS/ACS sorting tracks tax rates not that share; TX AGI inflow; moving motives unresolved | Explaining native migration or assigning its revenue cost |
| [Who pays the fiscal gap](immigration-fiscal-gap-incidence-who-pays-2026-09-18.md) | Historical $2,246/household and 89% state-local superseded; rebuilt financing requires explicit correctional-payer sensitivity and remains imposed incidence | Reusing household burden or payer-share figures |
| [Housing supply, demand and rents: California against Texas](immigration-housing-supply-ca-tx-2026-09-22.md) | 2026-09-22, ladder 180: Texas permits 2.2–2.5× California's per resident on average over 2000–2024 (1.4× in 2004 to 3.7× in 2009), but California's stock outgrew its population 2010–2024 (1.77 vs 2.31 people per added unit) [FRAMING-SENSITIVE]; same demand shift moves coastal-CA rents 2.0–2.5× Houston's on Saiz elasticities; 152 of 168 metros: +0.030 log points of 2015–2026 rent growth per point of Mexican-origin share change within state, elasticity interaction not identified; 2024 PUMS: native NH white adults leave CA at −11.7/1,000, steeper without a degree; TX flat. Descriptive, no instrument | Any rent, zoning or "Texas builds" claim; the housing channel of FAQ 4 and 15; modelling a stock counterfactual (§6 says why not) |
| [Rents and values against the 2000–2010 inflow, instrumented](../infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/RESULT.md) | 2026-09-22, ladder 183: per point of foreign-born share, rents +1.4% (SE 1.4, null containing Saiz's 1) and values +11.6% (2.9; +5.7% with the 2000 level) with the ancestry instrument; settlement instrument 2.5–5.7× larger and rejected by Hansen J; no inelastic-metro amplification (223 Saiz-matched metros); all-foreign-born, one cycle | Quoting a causal rent or value effect for a decade; using the Saiz mechanical response (ladder 180) as a rent prediction |
| [Second instrument for the 2000–2010 inflow](../infra/immigration-fiscal/ancestry_instrument_2026_09_22/RESULT.md) | 2026-09-22, ladder 182: the public ancestry push-pull prediction (F 63.9 vs 29.1, passes the baseline-level test the settlement instrument fails, Mexico a third of its variance) halves the SSI response to −0.28 (0.06) and makes the public-assistance response a null (−0.10 ± 0.19); Hansen J rejects the pair; the displacement lane's negative claim stands at smaller size | Quoting the displacement lane's public-assistance coefficient; choosing an instrument for any 2000–2010 metro design |
| [US low-skill effect papers: what joins the account](immigration-us-lowskill-effects-integration-2026-09-22.md) | 2026-09-22, ladder 181: fourteen primary texts read in full; the removal model's ε = 3 rests on a firm-level 1.26 (95% CI 0.12–2.39) and a calibrated 4.6 whose authors' aggregate is ≈9, while direct low-skill estimates are 8.7 (Caiumi–Peri) and 17.9 (Piyapromdee); computed on the nest, ε = 8.7 and 17.9 give +$18.0 / +$11.9bn and +$15.6 / +$10.3bn (GDP / cash) against the published +13.3 / +8.8bn, a $2–5bn headline move rather than $9–14bn, not applied; ten papers feed four stand-alone sections (wage incidence, removal and jobs, housing horizons, selection) and none carries a fiscal line | Placing any of these papers in an essay section; choosing ε for FAQ 14; reusing the ancestry-instrument files (Wilson–Zhou's rejected instrument, F 6.80) or the Bracero package |
| [Employment-entry displacement, US metros](immigration-employment-entry-displacement-2026-09-18.md) | Recent metro causal effect unresolved; preserve weak-stage and placebo results, withdraw small/negative scalar explanation and college-control proof | Running or interpreting recent settlement-share IVs |
| [Institutions and liberal norms by generation](immigration-institutions-and-liberal-norms-by-generation-2026-09-18.md) | GSS/ANES survey contrasts by generation and reference; response-style share unidentified; political-violence item requires behaviorally validated replication | Interpreting norms, institutions and survey measurement |
| [Mexico-born arrival cohorts](immigration-mexican-arrival-cohorts-2026-09-18.md) | 2026-09-18; age cut 2026-09-22 | Cohort quality 1975–2024: LTHS among new arrivals 82% → 33%, BA+ 3% → 22%; wage residual U-shaped; migrants' schooling +2.37 yr vs Mexico 15+ +2.20, selection flat on the slope. Same-age INEGI 2020 sheet 13 vs ACS 2019 0–5 YSM: LTHS 9–13 pp below origin in every band 25–54, gap not larger for younger births; BA+ within 3 pp except n=233. US stayers; ACS secundaria-as-HS. [Companion](immigration-mexican-origin-age-attainment-2026-09-22.md) | Any "earlier Mexican cohorts were better" or "the surge was Mexican" claim |
| [Consumer prices and native women's hours](immigration-consumer-price-and-native-hours-2026-09-18.md) | Extrapolated worker-removal scenarios; $21.8bn combines private gains and tax receipts and is not a bound on total benefits or a matched offset to the all-generation account; goods-price evidence is not a failed services replication | Comparing benefits on a common policy and population |
| [Claim scorecard: Smith, Caplan, Decker, Nowrasteh](immigration-claim-scorecard-2026-09-18.md) | September 19 corrections govern the retained rows: no CBO-per-capita refutation of incumbent welfare; no fee/loan falsification from a benchmark shortfall; counts withdrawn | Matching the actual claim before grading a rebuttal |
| [Yglesias claims audit](immigration-yglesias-claims-audit-2026-09-21.md) | 2026-09-21: 40 claims and 15 concessions from 15 primary pieces; he has conceded the skill gradient (2021), housing (2025), asylum and enforcement (2023–25); unsupported: the 2020 universals, a loose reading of Borjas, and a welfare-wall remedy that does not reach most of the gap; no fiscal number in his own voice (the CBO posts are guests') | Quoting or rebutting Yglesias; the matching rule applied before grading |
| [Canon citation audit](immigration-canon-citation-audit-2026-09-17.md) | 2026-09-17 | Most-cited low-skill immigration papers ranked by Semantic Scholar and OpenAlex counts (S2 fragments Borjas 2003 and Card 1990; every affected row tagged), 26 papers audited: one defective result per side (Borjas 2017 Mariel; Longhi 2005 as an estimate), over-citation the dominant failure (8 of 13 pro, 4 of 13 con), pro canon rests on the shift-share instrument Jaeger–Ruist–Stuhler show is biased against short-run effects and con canon on fixed-capital skill cells biased the other way; CIS/Heritage absent from the citation record | Citing any canonical immigration paper for a claim; "the literature shows" arguments on either side |
| [Study integrity audit](immigration-study-integrity-audit-2026-09-23.md) | 2026-09-23: 26 external studies behind the crime, legalization and children's conclusions traced from data capture; none fabricated; the repo went beyond its source 18 times (14 favourable to immigration, 3 against, 1 both), mostly composition (two-thirds of studies overstated on each side), plus two double standards that favour immigration (Lott against Light; Freedman–Owens–Bohn's ethnicity proxy) | Citing a causal estimate on crime, legalization or children's outcomes; dismissing a study for a flaw |
| [IGM panel immigration polls](immigration-igm-panel-audit-2026-09-17.md) | 2026-09-17 | Every IGM/Clark Center immigration poll (13 polls, 22 statements, 986 responses from the site's CSVs): all on legal admission, none on unauthorized immigration; the 2013 low-skill statement at 52% panel agreement with 17 of 24 agreers giving no reason and the same panel agreeing low-skilled Americans lose; per-comment audit against the ledger; weighted/unweighted gap is partly a denominator change | Any "economists agree immigration is good" claim, or citing the IGM low-skill poll |
| [Bookmark claims and commentator source notes](immigration-essay-angles-from-bookmarks-2026-09-16.md) | Source-grounded claims, commentator positions and research questions from the operator's bookmarks; retain as evidence notes | Locating original statements and source coverage |
| `immigration-conduct-denominators-2026-09-05.md` | Corrected Texas native denominator, official SPI recode, recent custody/fraud and audits | Reusing old SPI rates or cumulative convictions as a current rate |
| `immigration-admission-work-access-2026-09-05.md` | Reconciled admission distributions, 2026 EAD/refugee data and undercount assumptions | Equating new entries, adjustments, application queues and resident cohorts |
| `immigration-sipp-2024-benefits-2026-09-05.md` | Actual calendar2024 selected benefits with 240 replicate weights | Comparing benefit receipt or interpreting coarsened arrival bins |
| `immigration-welfare-use-by-generation-2026-09-16.md` | Welfare use by immigrant generation (CPS ASEC 2024–25): gen2 34.6% vs gen3+ 29.4%, 1.5 pts after age adjustment, below gen3+ within white/Black/Asian; cash lowest in gen2 | Any claim about the second or third generation's welfare use, or reading CIS generation tables |
| `immigration-mexican-origin-by-generation-2026-09-16.md` | Mexican-origin residents by generation (CPS ASEC 2024–25): education, work, earnings, poverty, welfare; Borjas–Katz wage effect; fiscal and crime cross-refs; what is conclusive vs contested vs unmeasurable | Any claim about Mexicans' economic or crime impact by generation |
| `immigration-local-cost-incidence-2026-09-05.md` | NYC financing, household-nights, enrollment and school-spending definitions | Converting gross services into per-person or net welfare costs |
| `immigration-material-repair-report-2026-09-05.md` | Current material repair status, source corrections and validation evidence | Reusing numerical or causal conclusions from older memos |
| `immigration-cohort-clarity-2026-09-05.md` | All-native versus Mexico-born partial fiscal comparison; actual 2019/2024 recent-entry profiles and discriminating next checks | Asking whether the newer intake differs, what Somali-origin data establish, or which fiscal ranking is supported |
| `immigration-recent-cohort-data-availability-2026-09-05.md` | Verified ACS/SIPP/CPS release periods, actual SSD paths and administrative counting limits | Assuming 2025/2026 microdata are already available or equating admissions with residents |
| `immigration-cohort-narratives-2026-09-05.md` | Targeted official X sample on recent cohorts, refugee/fraud and Somali claims with primary checks | Reusing current cohort or group-generalization narratives |
| `immigration-framing-refresh-2026-09-05.md` | Recent evidence integrated: work rights, adjustment, housing, victimization and policy mechanisms | Choosing the next empirical comparison or interpreting current narratives |
| `immigration-recent-papers-2026-09-05.md` | June–September primary papers/revisions with designs, dates and access limits | Quoting recent labor, housing, fiscal or enforcement research |
| `immigration-recent-narratives-2026-09-05.md` | Current essays/news and selective official X sample; counterexamples and claim checks | Repeating current public arguments |
| `immigration-dataset-proxy-refresh-2026-09-05.md` | BLS/BPS/ICE acquisitions and BEA audit, provenance and principal checks | Using recent outcomes, capacity proxies or enforcement counts |
| `immigration-conceptual-audit-2026-09-05.md` | Material audit: SIPP household/person and education errors; GDP/incumbent and CRS mistakes; Cato mischaracterization; global-gains arithmetic; conditional crime-bias sign | Reusing June fiscal-proxy figures or the dismantling synthesis; these corrections supersede the specified claims |
| `immigration-main-question-reset.md` | What the repo is actually trying to answer | Reframing the project or proposing new scope |
| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
| `immigration-epistemic-check.md` | Framing-sensitive guardrails | Politically charged synthesis |
| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
| `immigration-source-incentive-regrade-2026-06-23.md` | Source-incentive heuristics for prioritizing checks; grades are not truth probabilities or evidence weights | Assessing source incentives while verifying methods and primary tables |
| `immigration-dataset-register.md` | Use-case-oriented data register | Asking "what data do we have?" |
| `immigration-dataset-roadmap.md` | **Acquisition roadmap** (2026-06-24) — 12 targets, several since acquired (SCAAP, Texas DPS arrests, SPI 2016, USSC, NIS; check the [register](immigration-dataset-register.md) first), chosen to fill the crime + benefit-side gaps | Asking "what data should we get next?"; planning acquisition |
| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |
| `immigration-friend-reproduce-guide.md` | **Clone → build → read → query** for a human collaborator | Sharing reasoning + reproduction steps |
| `immigration-redteam-2026-06-25.md` | Red-team of the current position; status as of 2026-09-05 | Closing out a conclusion; before publishing |
| `immigration-preregistration-ledger.md` | Frozen predictions written before the gated datasets land | Interpreting a new gated-data result; checking for post-hoc drift |
| `immigration-interpreted-insights-2026-06-24.md` | Interpreted insights from the June frontier pass, repaired 2026-09-05 | Quoting a June-era interpretation |

## Scouting frontier (2026-06-24)

Candidate outputs from a parallel scout pass to extend the graph — **feed the graph, not yet canonical; review before citing.**

| File | What |
|------|------|
| `immigration-dataset-roadmap-additions-2026-06-24.md` | More datasets beyond the roadmap (AZ crime-by-status ICPSR 39107, BJS NCRP corrections flow, SSA EPUF earnings, LEHD PSEO, OECD fiscal) |
| `immigration-dataset-roadmap-batch3-2026-06-24.md` | Batch 3 — 14 datasets across 8 axes (labor-status, health, tax, housing, innovation, international, enforcement, flows): NAWS, DOL OFLC, NHIS, AHRQ HCUP, IRS ITIN, SSA Earnings Suspense File, AHS, PatentsView + immigrant-inventor linkage, StatCan IMDB, TRAC, MMP, DHS Yearbook, UK Dustmann-Frattini |
| `immigration-dataset-roadmap-batch4-us-2026-06-24.md` | Batch 4 US-micro (7) — crime victimization (NCVS), 2nd-gen longitudinal (CILS, Add Health, NLSY97), health (NHANES, NLMS mortality), food security (CPS-FSS) |
| `immigration-dataset-roadmap-batch4-intl-2026-06-24.md` | Batch 4 international/flows (6) — OECD-DIOC, World Bank KNOMAD remittance-outflow leakage, USCIS admin flows, Census of Governments fiscal capacity, ORR refugee survey, German IAB-SOEP |
| `immigration-dataset-roadmap-batch5-benefit-2026-06-24.md` | Batch 5 benefit (5, **vein saturated**) — NSF NSCG (immigrant scientists), SED (foreign PhD stay-rates), SEVIS + Open Doors (foreign-student contribution), HSLS09 (2nd-gen→earnings panel); CE/BFS/Kauffman skipped (nativity-blind) |
| `immigration-dataset-roadmap-batch5-cost-2026-06-24.md` | Batch 5 direct-cost welfare-admin (6, **vein saturated**) — SSI / TANF / NVSS-Natality by citizenship (verified); HUD / WIC / NSDUH carded with honest no-nativity-on-public-product flags |
| `immigration-paper-gaps-2026-06-24.md` | Missing/under-weighted papers (Ousey-Kubrin meta-analysis, Light 2020, Abramitzky 2024 incarceration series, sanctuary/enforcement nulls) |
| `immigration-claim-candidates-2026-06-24.md` | 17 falsifiable claims (crime C1–C7, 2nd-gen S1–S4, sharp tests Q1–Q6) each paired to a settling dataset |
| `immigration-integration-opportunities-2026-06-24.md` | 12 graph-wiring fixes; spine = INT-06 canonical status/citizenship harmonization table |
| `immigration-acquisition-gaps-2026-06-24.md` | What is still worth acquiring: datasets, narratives, papers |
| `immigration-clemens-method-check-2026-06-24.md` | Clemens GE versus partial-equilibrium method check |
| `immigration-gated-data-specs-2026-06-25.md` | Acquisition specs for gated datasets (IPUMS-CPS second-generation extract and others) |

## Frontier expansion (2026-06-25)

Historical five-domain research/acquisition pass. DOI resolution checks bibliographic identity; it does not verify an effect size or inference. September corrections in confidence-ladder entries 52–60 and the linked memos supersede affected June claims. The coverage matrix records a search episode, not proof that economics or crime research is exhausted.

| File | What | Consult before |
|------|------|----------------|
| `immigration-research-coverage-matrix-2026-06-25.md` | **The map** — per-domain saturation-vs-frontier + the 5-agent integration log + synthesis verdict | Asking "what research is left?"; planning the next acquisition |
| `immigration-economics-disconfirmers-2026-06-25.md` | Mariel artifact (Clemens-Hunt), Colas-Sachs GE ~$750, CBO −$0.9T federal surge, Dustmann-Frattini UK | Quoting the Borjas wage spine or NAS net-cost as settled |
| `immigration-policy-frontier-2026-06-25.md` | Legalization→crime CAUSAL cluster (jobs channel); enforcement≈null; DACA + refugee evals | Crime/policy causal claims; "does enforcement reduce crime?" |
| `immigration-crime-frontier-2026-06-25.md` | Crime outcomes, generational evidence, ecological versus individual estimates and source limits | Generalizing beyond the measured justice outcome and population |
| `immigration-sociology-frontier-2026-06-25.md` | Trust meta-analysis, selection and generational measurement limits | Inferring social or institutional mechanisms |

## Fiscal Ledger

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-fiscal-impact-unauthorized-memo.md` | **[pre-repair, March 2026; status banner added 2026-09-21]** Literature memo: federal/state-local split, wage debate, child-attribution dispute. Its NAS "second generation net positive" statements are all-origin, not the Mexican-origin result | The literature and the child-attribution dispute; **not** a current fiscal bottom line (use Core State) |
| `immigration-full-spectrum-costs-unauthorized-memo.md` | Non-ledger costs: congestion, courts, labor-law erosion, backlash | Claiming "hidden" costs beyond taxes/transfers |
| `immigration-unified-scenarios-memo.md` | Scenario comparison across methods | Converting arguments into a bounded range |
| `immigration-state-local-cost-examples-ny-ca-tx.md` | Concrete state/local examples | Generalizing from national ledgers to local burden |
| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |
| `immigration-adversarial-review.md` | Strongest case against our own position | Closing out a conclusion or writing a public-facing memo |
| `immigration-path-to-minus-200k-scenario-audit.md` | Scenario audit of the `-$200k` per-person path; April model, see the fiscal account for current units | Reusing a lifetime scalar |

## Data Stack

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
| `immigration-borjas-supply-shock-panel-2026-06-23.md` | **Built** real 1980–2023 immigrant-share-by-skill panel from IPUMS census/ACS (`borjas_supply_shock_panel`); <HS share 9.8%→40.8% | Citing the supply-shock *quantity*; do NOT read it as a wage verdict (that's the Card-vs-Borjas debate) |
| `immigration-restrictionist-arguments-steelman-2026-06-15.md` | **Steel-man** restrictionist chains: Borjas, BGH, NAS/Orrenius, Gould, Razin, FAIR | Arguing against immigration; follow their logic |
| `immigration-restrictionist-corpus-parse-2026-06-15.md` | **Full marker-modal parse** of 8 restrictionist PDFs → perspectives, narratives, generators S06–S14 | Deep read of restrictionist corpus; generator mining |
| `immigration-restrictionist-corpus-full-extract-2026-06-15.md` | **Section-by-section full read** of all 9 papers (~220 claims, 62 sections) | Authoritative claim register after full parse |
| `immigration-restrictionist-dataset-integration-2026-06-15.md` | **Paper → dataset → DuckDB** map; Tier A–C acquire list | Planning integration after restrictionist corpus read |
| `immigration-thesis-generator-audit-2026-06-16.md` | Cross-disciplinary generator/self-prompt audit (economics, micro/macro, urbanism, psychology, narrative) | Running divergence/convergence loops; asking what to search next |
| `immigration-knowledge-delta-agent-loop-2026-06-16.md` | Two-day delta + parent-controlled agent loop (claim inventory → probe → converge → review) | Starting a full immigration research epoch; pairing with generator audit |
| `../notes/immigration-lifetime-sweep-protocol.md` | Mandatory post-sweep workflow (theory → 5 models → thesis burst → disconfirm → round N+1) | Structuring research cycles |
| `../notes/immigration-lifetime-synthesis-diverge-cookbook.md` | **Prompt template / cookbook** — full diverge↔converge loop, subagent JSON schema, synthesis prompt | Running sweeps; adapting to new topics |
| `immigration-public-data-acquisition-2026-04-11.md` | What public files were actually staged locally | Assuming a dataset has been acquired |
| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
| `immigration-next-data-upgrades.md` | Highest-value missing acquisitions | Planning the next data tranche |
| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
| `immigration-school-service-complexity-2026-04-11.md` | Built district/state school-side context layer from `SAIPE` + school finance + current NCES directory, plus bounded `ELSi` probe | Doing district school-burden or school-service-complexity analysis |
| `immigration-surge-threshold-dataset-frontier-2026-04-21.md` | Dataset frontier and research designs that can actually identify surge and threshold effects | Asking what data and empirical design would settle nonlinear local-capacity questions |
| `immigration-prototype-progress.md` | Current prototype state | Claiming the model is further along than it is |
| `immigration-public-mvp-meps-module-2026-04-11.md` | Built MEPS health-cost module for the public MVP | Using MEPS-derived health-cost outputs |
| `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` | Weighted ACS stock cut by education bucket plus current lifetime-estimate status | Asking for `<HS` / `HS` / `some college` counts or state shares |
| `immigration-local-burden-puma-layer.md` | PUMA/local burden layer | Moving from state averages to sub-state analysis |
| `immigration-stage2-county-bridge-batch.md` | County bridge build status | County-level joining or school/housing overlays |
| `immigration-next-agent-handoff-2026-04-11.md` | April 2026 next-agent handoff; process record, superseded in practice by the reproduce guide and the September memos | Assuming an April to-do list is still open |

## Interpretation & External Debate

Current cross-media coverage: [podcast, YouTube and Substack audit](immigration-media-perspectives-audit-2026-09-20.md) checks 16 media pieces with explicit access limits, maps claims to existing evidence, adds visa-mobility/H-1B/Dutch study screens, and distinguishes high-skill selection from low-skill evidence. The user-linked Reddit bibliography remains inaccessible and ungraded.

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-clark-respondent-audit.md` | How to read the Clark poll without overclaiming | Saying "economists agree" |
| `immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md` | Unified comparative audit with one quantitative framework across all three commentators | Wanting a more decisive first-principles comparison |
| `immigration-claims-matrix-2026-04-11.md` | One-page verified/inferred/unresolved claim ledger for artifacts and commentators; 2026-06-16 scoped to quick ledger, not latest tensor | Making a quick final assertion; confirm latest fiscal/school rows in verified findings and running fixes |
| `immigration-david-d-friedman-claims-audit-2026-04-11.md` | Named audit of David D. Friedman claims with a first-principles quantitative pass | Checking libertarian open-borders arguments against the repo and official sources |
| `immigration-bryan-caplan-claims-audit-2026-04-21.md` | Claim-by-claim audit of Bryan Caplan with a causal graph tying his optimistic channels to current surge, housing, fiscal, and political-response evidence | Evaluating Caplan directly rather than treating him as generic open-borders rhetoric |
| `immigration-sumner-claims-audit-2026-09-22.md` | Claim-by-claim audit of Scott Sumner's surge, wage, housing, Social Security and scale claims against his own pages, with the pasted AI critique graded cosign / throw out / complement; the Social Security "best solution" quote does not exist; the Trustees sensitivity is 0.38% of payroll (about $2.6tn of $22.6tn), not $1.5tn; CBO surge routed to FAQ 16 | Quoting Sumner; the "CBO says the surge shrinks the deficit" objection; the Social Security financing claim |
| `immigration-economist-one-pager-2026-04-22.md` | Short public-facing one-pager on why the strongest pro-immigration economics rhetoric keeps answering the wrong question | Needing a concise forwardable version rather than a full memo |
| `immigration-economist-debate-sheet-2026-04-22.md` | Quote-driven debate sheet mapping economist claims to the hidden move, failure mode, and strongest repo-backed counter | Wanting direct quotes and fast counters for debate or adversarial writing |
| `immigration-economist-rhetorical-failures-2026-04-22.md` | Bounded memo on the strongest fair critique of mainstream pro-immigration economics rhetoric: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, denominator masking, and political-economy underspecification | Asking how to kill the strongest economist arguments without overclaiming beyond the repo's current evidence |
| `immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md` | Named audit of Noah Smith and Nicholas Decker claims | Checking pundit or commentator claims against the repo and official sources |
| `immigration-economist-dismantling-2026-06-25.md` | June dismantling pass (corrected 2026-09-05): fundamental fair-is-the-weapon dismantling of the pro-immigration canon across 3 tiers (Commentators: Smith/Decker/CATO; Academic Foundations: Card-Peri/Clemens; Popular Books: Hernandez/*Streets of Gold*); grants the repo-confirmed core, kills only the coordinate-switches, quotes the canon's own primary texts | Building any step-by-step takedown of pro-immigration arguments; wanting the synthesis across all 7 targets |
| `immigration-dismantle-noah-smith-2026-06-25.md` | Corrected claim-by-claim assessment: average gains, local costs, projections and welfare incidence | Comparing Smith's exact populations and claims |
| `immigration-dismantle-decker-2026-06-25.md` | Corrected returns-to-scale, incumbent welfare and global-gains arithmetic | Using GDP/person or complementarity to infer welfare |
| `immigration-dismantle-cato-2026-06-25.md` | Corrected descendant accounting and allocation sensitivity; no uncomputed sign reversal | Citing the historical $14.5T or descendant-inclusive estimates |
| `immigration-dismantle-hernandez-2026-06-25.md` | Corrected annual-versus-lifetime NAS figures, inventor attribution and crime scope | Evaluating book claims using primary evidence |
| `immigration-low-skill-origin-incidence-memo.md` | Why origin mix and household structure matter | Treating low-skill immigration as one undifferentiated object |
| `immigration-fiscal-deceptive-data-reading-pack.md` | Common bad-faith or sloppy readings of the data | Debunking a chart, thread, or pundit claim |
| `immigration-fiscal-camarota-cis-testimony-audit.md` | Restrictionist benchmark audit | Using CIS/Camarota as baseline evidence |
| `immigration-crime-rates-unauthorized-vs-native-born.md` | Crime-rate evidence review | Mixing crime claims into a fiscal memo |
| `immigration-agi-reframing.md` | Off-mainline strategic reframing | Pulling the project into speculative macro territory |
| `immigration-recent-literature-surge-threshold-audit-2026-04-21.md` | Post-2023 economics literature on surge and threshold effects | Claiming the literature has or lacks a threshold result |
| `immigration-jre-2460-rachel-wilson-claims.md` | JRE #2460 Rachel Wilson claims 1–10 verification | Checking podcast claims |
| `immigration-jre-2460-claims-11-20.md` | JRE #2460 claims 11–20 verification | Checking podcast claims |
| `immigration-jre-2460-exa-crosscheck.md` | Exa Answer API cross-check of the JRE #2460 verifications | Trusting an answer-engine verdict |

## Causal-design layer (2026-04-18)

April 2026 county/receiver causal layer. Its analyses were superseded on 2026-09-05 (causal-lever, threshold and receiver-node claims withdrawn) and are listed under Historical; the two provenance records below remain live. The analysis result files under `sources/immigration-causal/data` were lost with the SSD tree in August 2026 and are deliberately not rebuilt (see the [data availability memo](immigration-recent-cohort-data-availability-2026-09-05.md), Revisions).

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction and later downgrade that left the annual wage/employment split unresolved | Wanting the evolution of reasoning itself traced rather than only the latest stance |
| `immigration-receiver-data-acquisition-2026-04-23.md` | Staged 2024 ACS PUMS, EOIR Case Data 2026-0301, and QWI county-quarter receiver panel with hashes, limits, and next kill-test sequence | Asking what new datasets were acquired for the receiver-node/capacity theory |

## Raw Data & Warehouse

Paths as of 2026-09-16. The `sources` symlink points at `/Volumes/2TBPNY/research-data`; builds run with `bash ../infra/immigration-fiscal/reproduce.sh` (staged builds since 1ee53c4). What survived the August 2026 SSD loss, what was re-acquired and which April analysis outputs are gone: `immigration-recent-cohort-data-availability-2026-09-05.md` (Revisions).

| File | Topic | Consult before |
|------|-------|----------------|
| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
| `../warehouse/immigration.duckdb` | Unified warehouse (context + lifetime + fiscal union, schema-namespaced); `immigration_context.duckdb` beside it is the aggregate warehouse | Querying state/origin/context data |
| `../infra/immigration-fiscal/reproduce.sh` | `doctor`, `download`, `verify`, `build`, `query`, `package` entry points | Rebuilding or extending the warehouses |
| `../sources/immigration-causal/data/lehd/qwi_state_panel.parquet` | LEHD QWI `se` state × quarter × industry × education panel 2003–2023, re-pulled 2026-09-16 (`ACQUIRED.md` beside it) | Using QWI earnings; it has no nativity variable |
| `../sources/immigration-causal/data/cbp/raw/` | CBP southwest-border encounter CSVs FY22–FY26 (April) | Counting encounters versus arrivals |

## Quick Start

If the question is:

1. `What do we currently think?` Start with `immigration-clarity-update-2026-09-05.md`, then `immigration-second-order-effects-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` and `immigration-measurement-uncertainty-2026-09-05.md`. `immigration-material-repair-report-2026-09-05.md` says what changed and why; the September entries (52–64) at the top of `immigration-confidence-ladder.md` give claim confidence. Everything below a `historical-snapshot` marker is provenance, not current.
2. `Is low-skill immigration good or bad for natives?` The findings table in `immigration-clarity-update-2026-09-05.md`, the mechanisms in `immigration-second-order-effects-2026-09-05.md`, the annual partial balance in `immigration-fiscal-account-2024-2026-09-05.md` and `immigration-sipp-2024-benefits-2026-09-05.md`, and the Mexico-born versus all-native comparison in `immigration-cohort-clarity-2026-09-05.md`. `immigration-economist-effects-matrix.md` (April) is for how economists frame the question, not for numbers.
3. `Crime?` `immigration-conduct-denominators-2026-09-05.md` and `immigration-crime-race-ethnicity-2026-09-05.md` for the corrected rates; `immigration-crime-statistics-bias-mechanisms-2026-09-16.md` for how the statistics mislead; `immigration-generational-crime-mechanisms-2026-09-16.md` for first versus second generation; `immigration-crime-frontier-2026-06-25.md` and `immigration-crime-rates-unauthorized-vs-native-born.md` carry dated revisions.
4. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `immigration-recent-cohort-data-availability-2026-09-05.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
5. `Can we model this ourselves?` Start with `immigration-friend-reproduce-guide.md` and `../infra/immigration-fiscal/reproduce.sh`; the current model is described in `immigration-fiscal-account-2024-2026-09-05.md`; `immigration-lifetime-fiscal-data-stack-2026-04-10.md` is the April design note.
6. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` (April ACS cut; the fiscal account carries the current education definitions).
7. `How do I run the next fiscal/generator sweep?` Start with `immigration-knowledge-delta-agent-loop-2026-06-16.md`, then `../notes/immigration-lifetime-synthesis-diverge-cookbook.md`, `../notes/immigration-lifetime-sweep-protocol.md` and `immigration-thesis-generator-audit-2026-06-16.md`; check `immigration-material-repair-report-2026-09-05.md` before reusing any June fiscal generator.

## Historical (superseded 2026-09-05)

Retained verbatim for source and correction provenance under the [material inference repair decision](../decisions/2026-09-05-material-inference-repair.md). Each file keeps its dated corrections above a `<!-- historical-snapshot:start superseded=2026-09-05 -->` marker; do not cite the numbers or causal claims below that marker as current. Read the successor first.

| File | Former section | Was | Superseded by |
|------|----------------|-----|---------------|
| `immigration-verified-findings-report-2026-04-10.md` | Core State | Historical findings with September corrections and current-report link | `immigration-clarity-update-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` (September corrections sit above the snapshot marker) |
| `immigration-confidence-ladder.md` | Core State | Claim confidence by tier | `immigration-clarity-update-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` (its September entries 52–64, above the snapshot marker, are live) |
| `immigration-claims-evolution-ledger-2026-04-23.md` | Core State | Claim-by-claim evolution ledger with takeaways and recurring misunderstandings | `immigration-material-repair-report-2026-09-05.md` |
| `immigration-fiscal-welfare-ledger-map.md` | Core State | Unifying map — "positive vs negative?" decomposed into 4 coordinates × the full fiscal+benefit ledger set; maps generator clusters A–U | `immigration-second-order-effects-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` |
| `immigration-conclusion-audit-running-fixes.md` | Core State | Live overclaim/denominator/layer fix ledger | `immigration-material-repair-report-2026-09-05.md` |
| `immigration-urbanism-frontier-2026-06-25.md` | Frontier expansion (2026-06-25) | Biggest yield — Wilson-Zhou (2026) causal housing magnitudes (+2.2% prices/+1.4% rents) + the MSA rent×fb-share panel dataset map (Zillow acquired; WRLURI/Geocorr/LODES spec'd) | `immigration-second-order-effects-2026-09-05.md`, `immigration-recent-papers-2026-09-05.md` |
| `immigration-costs-causal-analysis.md` | Fiscal Ledger | DAG and causal-path discipline | `immigration-second-order-effects-2026-09-05.md`, `../decisions/2026-09-05-material-inference-repair.md` |
| `immigration-country-fiscal-tensor-2026-06-15.md` | Data Stack | Built country fiscal tensor + rollup anchors (union DuckDB) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-federal-distribution-findings-2026-06-15.md` | Data Stack | Distribution pass — school units, federal proxy white vs Mexico | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` | Data Stack | EU27 / UK / Caucasian natives / low-skill corridors — federal proxy + matched-education | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-school-burden-per-adult-2026-06-15.md` | Data Stack | per_pupil × kids/adult — three-layer annual (`v_three_layer_annual`) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-sweep-cycles-13-22-2026-06-15.md` | Data Stack | Diverge/synthesis cycles 13–22 (school burden build) — rushed SQL pass, superseded by 23–32 and same-universe guard; do not cite old `$771/+748` origin school/net rows | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-sweep-cycles-23-32-2026-06-15.md` | Data Stack | Full protocol sweeps 23–32: NAS college+ NPV, school weights, lifetime flip, converge; origin school/net rows partly superseded by same-universe guard | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-mexico-npv-population-synthesis-2026-06-15.md` | Data Stack | Mexico NPV multiply-out, ACS denominator, Biden stock vs encounters, full ledger stack (Q+R) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-lifetime-country-approx-brainstorm-2026-06-15.md` | Data Stack | Brainstorm: country lifetime +/- with 1st/2nd/3rd order stacks | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-lifetime-dataset-brainstorm-2026-06-15.md` | Data Stack | Brainstorm + tier map for lifetime proxies; `setup-lifetime.sh` acquisition | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-lifetime-fiscal-generators.md` | Data Stack | 563 DuckDB parameter claims; 106 MD / 104 DuckDB generators (MD-only Q06, S15) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-lifetime-unified-theory-2026-06-15.md` | Data Stack | Living synthesis — unified theory + 5 formal models + critique matrix (update each sweep) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-net-negative-dataset-frontier-2026-06-15.md` | Data Stack | Datasets to test net-negative fiscal/local-cost claims (+ disconfirmation) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-scenario-composition-2026-06-15.md` | Data Stack | Integrated SIPP+MEPS+federal+local scenario ledgers | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-public-mvp-readiness-2026-04-11.md` | Data Stack | What is ready for a public-use MVP | `immigration-material-repair-report-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` |
| `immigration-public-mvp-sipp-meps-bridge-2026-04-11.md` | Data Stack | Completed SIPP-to-MEPS bridge and expected-health output | `immigration-material-repair-report-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` |
| `immigration-dismantle-card-peri-2026-06-25.md` | Interpretation & External Debate | Published +0.6% native / −6.7% prior-immigrant model result; corrected local-design and QWI limits | `immigration-material-repair-report-2026-09-05.md`, `immigration-economist-dismantling-2026-06-25.md` |
| `immigration-dismantle-clemens-2026-06-25.md` | Interpretation & External Debate | Corrected global model versions, fixed-gain arithmetic, rate/stock and housing scope | `immigration-material-repair-report-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |
| `immigration-dismantle-streets-of-gold-2026-06-25.md` | Interpretation & External Debate | Conditional mobility survives; corrected rank, convergence, sample and book-coverage objections | `immigration-material-repair-report-2026-09-05.md` |
| `immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md` | Interpretation & External Debate | Audit of the Open Borders “double world GDP” slogan, cited papers, repo capacity constraints, and apartheid framing | `immigration-conceptual-audit-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-threshold-first-panel-2026-04-21.md` | Interpretation & External Debate | First joined-data threshold pass using BPS permits, HUD PIT/HIC, election shift, and receiver-city costs | `immigration-second-order-effects-2026-09-05.md`, `../decisions/2026-09-05-material-inference-repair.md` |
| `immigration-threshold-causal-levers-2026-04-21.md` | Interpretation & External Debate | Normalized threshold associations and limits of causal lever identification | `immigration-second-order-effects-2026-09-05.md`, `../decisions/2026-09-05-material-inference-repair.md` |
| `immigration-causal-synthesis-2026-04-18.md` | Causal-design layer (2026-04-18) | Cycle synthesis: Saiz × E-Verify findings, observed mandate-margin wage read; not global Card-vs-Borjas verdict | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-causal-everify-card-vs-borjas.md` | Causal-design layer (2026-04-18) | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | `immigration-material-repair-report-2026-09-05.md`, `immigration-recent-papers-2026-09-05.md` |
| `immigration-causal-saiz-elasticity-rent.md` | Causal-design layer (2026-04-18) | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Causal-design layer (2026-04-18) | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | Causal-design layer (2026-04-18) | IRS SOI × ACS moved-from-abroad flow comparison for “newcomer burden” | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-causal-surge-2021-2024.md` | Causal-design layer (2026-04-18) | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | `immigration-material-repair-report-2026-09-05.md`, `immigration-conduct-denominators-2026-09-05.md` |
| `immigration-county-outcome-panel-2026-04-21.md` | Causal-design layer (2026-04-18) | QCEW + IRS domestic migration + threshold spine: county wages, employment, domestic migration, and political response in one frame | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-capacity-frontier-2026-04-21.md` | Causal-design layer (2026-04-18) | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-capacity-falsification-2026-04-21.md` | Causal-design layer (2026-04-18) | Corrected falsification pass with clean `2017–2018` and `2018–2019` annual pre-COVID windows, `1,000`-draw permutation inference, division/state leave-out, explicit window metadata, and wage-threshold null benchmarking | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-frontier-rethink-2026-04-22.md` | Causal-design layer (2026-04-18) | Zoomed-out rethink after the corrected falsification pass; demotes the annual county panel to a screening surface and ranks the better next frontiers | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-receiver-failure-atlas-2026-04-22.md` | Causal-design layer (2026-04-18) | Receiver-node overload atlas joining shelter load, permits, spending, and political shift from `2018–2024` | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-resident-weighted-exposure-2026-04-22.md` | Causal-design layer (2026-04-18) | Resident-, renter-, and child-weighted correction to the newcomer and stress-exposure framing | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-open-borders-break-even-bounds-2026-04-22.md` | Causal-design layer (2026-04-18) | Converts the repo’s conservative open-borders calibration into explicit break-even loss bounds and housing-absorption requirements | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-receiver-counterfactuals-2026-04-22.md` | Causal-design layer (2026-04-18) | National-CoC synthetic-control style counterfactuals for `NYC`, `Denver`, `Boston`, `Chicago`, and `Bexar`, including ratio outcomes, absolute-load checks, and donor-pool exclusions | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-receiver-node-kill-test-2026-04-23.md` | Causal-design layer (2026-04-18) | End-to-end nine-node kill test joining ACS 2024 exposure, PUMA bridge, EOIR broad/strict court pressure, QWI labor outcomes, shelter/capacity, and political shift | `immigration-second-order-effects-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` |
| `immigration-full-spectrum-costs-scoring-model.md` | (not previously indexed) | Full-spectrum fiscal and welfare channels: inclusion requires compatible evidence | `immigration-second-order-effects-2026-09-05.md` |
| `immigration-msa-rent-elasticity-panel-2026-06-25.md` | (not previously indexed) | MSA rents and elasticity: descriptive correlations with an incomplete crosswalk | `immigration-second-order-effects-2026-09-05.md`, `immigration-recent-papers-2026-09-05.md` |
| `immigration-public-mvp-profiling-findings-2026-04-11.md` | (not previously indexed) | Immigration public MVP profiling findings — 2026-04-11 | `immigration-material-repair-report-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` |
| `immigration-public-mvp-variable-dictionary-2026-04-11.md` | (not previously indexed) | Immigration public MVP variable dictionary — 2026-04-11 | `immigration-material-repair-report-2026-09-05.md`, `immigration-fiscal-account-2024-2026-09-05.md` |
| `immigration-theory-verdicts-2026-06-25.md` | (not previously indexed) | Generator-bank checks — corrected evidentiary status | `immigration-material-repair-report-2026-09-05.md` |

<!-- knowledge-index
generated: 2026-09-16T13:06:38Z
hash: manual-september-route-refresh-2026-09-16

table_claims: 97

end-knowledge-index -->

# What survives consistent accounting and stricter family histories?

**Finding, September 17, 2026:** the large Mexican-origin annual fiscal **benchmark shortfall survives** the accounting repair. In the expanded main account it is $291bn against third-plus non-Hispanic whites, or $215bn against all natives. Across the named expanded-account sensitivity runs, the corresponding point estimates span approximately **$236–315bn and $188–229bn**. These are differences from reference profiles, not measured net fiscal costs. The main account's own included-component balance is **+$50bn**. The range is a set of mostly one-at-a-time model sensitivities, not a confidence interval or a bound over all possible assumptions. [MODEL-BASED DESCRIPTION; [generator and definitions](../infra/immigration-fiscal/all_age_ledger_2026_09_17/README.md), `derived/estimates.csv`; baseline and health-omission diagnostic excluded from the sensitivity range.]

Three additional findings matter. Allocation rules move tens of billions between generations; a common age distribution still shows smaller gaps in the later-generation populations; and stricter IIMMLA definitions retain the educational disadvantage of its G4+ sample while rejecting an across-the-board crime deterioration story. These are different cross-sectional populations and outcomes, not observations of one lineage through time. [MEASUREMENT + INFERENCE; sections below.]

## 1. The consistent all-age fiscal result

The earlier calculation combined an all-age base with adult-only additions. This rebuild applies the expanded components to the same civilian household population, with identical allocation and age rules on both sides of each contrast. It includes modeled employee and employer payroll/income taxes, selected cash/noncash benefits, sales and owner property taxes, public K–12, a school-lunch overlap correction and transported public medical costs. The last two tax categories, schooling and medical costs are modeled allocations rather than individual receipts. [METHOD; source-parameter details in the linked README.]

**CPS ASEC 2025, income year 2024, with MEPS 2024 health and the held mixed-year state parameters.** Dollar amounts are annual billions; populations are millions. Unit dollars are shared over SPM resource-unit members in this main specification; health is assigned directly by age/birthplace. All reference gaps below match eight age bands. [MODEL-BASED DESCRIPTION]

| Observed population | People | Absolute partial balance | Gap vs third-plus NH whites | Gap vs all natives |
|---|---:|---:|---:|---:|
| Mexico-born foreign-born | 12.22 | +6.63 | −103.10 | −85.16 |
| Native, at least one Mexico-born parent | 14.33 | +10.69 | −113.72 | −84.28 |
| Native, two US-area-born parents, Mexican self-ID | 14.34 | +32.92 | −73.77 | −45.56 |
| Observed union | 40.90 | **+50.24** | **−290.59** | **−215.00** |

[SOURCE: `all_age_ledger_2026_09_17/derived/estimates.csv`, scenario `all_age_shared`. The union is not an estimate of every person with Mexican ancestry: later nonidentifiers are missing from its third-plus category.]

The combined main-account pointwise 95% sampling intervals are **+$29.2 to +$71.3bn** for the absolute partial balance, **−$313.5 to −$267.7bn** for the white-reference gap, and **−$233.8 to −$196.2bn** against all natives. These incorporate CPS replicate uncertainty and the full covariance of the MEPS donor estimates. They condition on model parameters and transport assumptions; they do not cover survey undercoverage, all measurement error or omitted components. The Mexico-born absolute interval alone includes zero. [SOURCE: same output; METHOD.]

A nonracial reference is available without inventing “biological Americans”: **all natives with two US-area-born parents**. Its main gap is **−$212.31bn**, close to the all-native result. A different reference, natives excluding the observed Mexican-origin target categories, yields **−$240.48bn**. The all-native average includes the native target groups and therefore partially draws the comparison toward itself. Each reference answers a stated comparative question; none measures genetic ancestry. [SOURCE: same output; FRAMING-SENSITIVE.]

The absolute +$50.24bn would be erased by approximately **$1,228 per target resident in additional net omitted annual costs**, holding everything else fixed. That is an arithmetic break-even, not evidence about how large omitted costs actually are. Corporate taxes could add receipts; institutional care and other spending could add costs. Equal per-person public-good charges cancel from the reference gap but reduce absolute balances. The generator verifies that cancellation in every replicate. [CALCULATION + LOGIC; 50.238214bn / 40.896574m; no complete fiscal surplus claimed.]

## 2. Allocation changes the story of which generation carries the balance

An annual household account does not come with a uniquely correct assignment to individual generations. Sharing parents' earnings with children differs from assigning earnings to earners and schooling to children. Both can answer useful questions; neither establishes the causal cost of a generation. Unequal person weights introduce a further complication: merely moving dollars within a household can change estimated national dollars. The independent construct review identified this as a testable issue. [METHOD / INFERENCE]

The controlled test therefore applies the **same SPM-head weight to each unit's component dollars**, while holding person-weighted populations and direct medical costs fixed. Reassignment preserves every national component budget in all 161 weight vectors. Taxes/cash move to recorded people, employer payroll to earners, schooling to children; other household components stay shared. The exhaustive residual includes all other records, so a target-group transfer cannot vanish off-ledger. [SOURCE: `fixed_budget_transfers.csv`, `audit.json`; [review disposition](../notes/immigration-construct-review-2026-09-17.md).]

| Fixed-budget accounting rule | Observed union's absolute partial balance | White-reference gap | All-native gap |
|---|---:|---:|---:|
| Shared unit dollars | +$45.20bn | −$283.25bn | −$209.10bn |
| Person-source assignment | +$30.09bn | −$235.83bn | −$187.66bn |
| Paired change | **−$15.11bn** | **+$47.42bn** | **+$21.44bn** |

The white gap narrows even while the target's absolute balance falls, because the assigned reference balance falls more. The paired white-gap change has a conditional 95% interval of **+$38.62 to +$56.23bn**. Its component changes are approximately +$34.40bn from tax assignment, −$9.26bn from cash transfers, +$6.98bn from employer payroll and +$15.30bn from schooling. These sum to the total change; they are attribution effects in a fixed account, not economic gains. [SOURCE: `fixed_budget_attribution.csv`, `fixed_budget_gap_decomposition.csv`.]

Within the target union, person-source assignment moves the first generation's absolute balance up **$25.98bn**, second generation down **$9.38bn**, and third-plus down **$31.71bn**. The remaining **+$15.11bn** goes to all other records. Therefore “the second generation costs the most” is not a robust causal reading of an allocation table. Neither is the opposite claim that shifting dollars onto children reveals their complete lifetime cost. [SOURCE: same paired output; cancellation in `fixed_budget_transfers.csv`; INFERENCE.]

Other named sensitivities retain a large relative shortfall: narrower child age bands change the main white gap by only **−$1.47bn**; adding insurance to health matching gives **−$314.61bn**; adding modeled renter property-tax pass-through gives **−$284.37bn**. The latter two change model assumptions, not just survey noise. No result is selected as the uniquely true incidence rule. [SOURCE: `estimates.csv`; MODEL SENSITIVITY.]

## 3. A common age distribution shows partial convergence in observed populations

Dividing each group's age-matched total by its population still weights age-specific differences by that group's age composition. For an interpretable generation comparison, this lane also gives **every group the same white-reference age distribution**. The figures below are annual dollars per standardized person, against the same reference. [METHOD; `standardized_gap_per_person`.]

| Population | Shared allocation, person weights | Person-source allocation, person weights |
|---|---:|---:|
| Mexico-born | −$6,562 | −$6,888 |
| Mexican-parent second generation | −$5,943 | −$5,278 |
| Mexican third-plus self-ID | −$4,622 | −$4,571 |

[SOURCE: `estimates.csv`; the fixed-budget arms produce the same point ordering. All six pointwise 95% sampling intervals remain below zero.]

The third-plus minus first-generation standardized balance difference is **+$1,939** (95% interval +$766 to +$3,112) under sharing, or **+$2,317** (+$1,051 to +$3,582) under person-source assignment. However, the second-to-third-plus improvement is +$1,321 (+$296 to +$2,345) under sharing and +$707 (−$752 to +$2,165) under person-source assignment. The first-to-second contrast under sharing also includes zero: +$618 (−$592 to +$1,829). Thus the first-to-third-plus difference is supported under both allocation rules; neither rule supports improvement at every adjacent generation step. These are pointwise descriptive intervals, not a family-transition or multiple-comparison-adjusted causal test. [SOURCE: `generation_contrasts.csv`; shared donor/reference covariance retained.]

The defensible claim is **persistent shortfalls alongside partial convergence across observed generation categories**. It is not “no assimilation,” complete convergence, or proof of inherited group causes. The categories differ in birth cohort, migration selection, parents, intermarriage, destination and self-identification; standardizing age does not erase those differences. [INFERENCE]

## 4. Stricter IIMMLA histories preserve some findings and weaken others

IIMMLA 2004 is an unweighted five-county Los Angeles sample, ages **20–40**, not a national descendant panel. The earlier audit's 20–39 caption was incorrect. Reconstructing respondent and parent US birth, explicit foreign-grandparent answers, and country/nativity consistency changes the source-coded Mexican-self-ID G3/G4+ counts from **212/189 to 196/187**. The G3 reduction removes 13 unknown-grandparent histories and 3 internally conflicting grandparent profiles; the G4+ reduction removes 2 Mexico-born respondents. These conservative raw definitions do not prove the publisher's broader coding wrong. [SOURCE: [raw reconstruction and codebook rules](../infra/immigration-fiscal/iimmla_sensitivity_2026_09_17/README.md), `source_to_strict_counts.csv`, `audit.json`; [ICPSR 22627](https://www.icpsr.umich.edu/web/ICPSR/studies/22627).]

Restricting both groups to valid raw outcomes yields **192 G3 and 182 G4+**. Unknown/refused raw crime answers remain missing; known raw answers agree with supplied outcomes across the entire 4,655-person file. [MEASUREMENT]

| Outcome | Strict G3 | Strict G4+ | G4+ minus G3 |
|---|---:|---:|---:|
| BA or higher | 40/192 = 20.83% | 25/182 = 13.74% | −7.10pp |
| No high-school credential | 30/192 = 15.63% | 40/182 = 21.98% | +6.35pp |
| Ever arrested, respondent | 57/192 = 29.69% | 36/182 = 19.78% | −9.91pp |
| Ever reform school/detention/jail/prison | 29/192 = 15.10% | 24/182 = 13.19% | −1.92pp |

[SOURCE: `iimmla_sensitivity_2026_09_17/derived/rates.csv` and `contrasts.csv`, strict generic common-raw-endpoint rows; local unweighted sample percentages.]

Age/sex checks distinguish the outcomes. BA attainment is **22.45% vs 7.59% among men**, but **19.15% vs 18.45% among women**. The G3/G4+ BA difference also persists at ages 25–40, 24.16% vs 14.96%. Arrest is lower in G4+ within the examined age/sex cuts. The small incarceration difference reverses among men, **24.49% vs 25.32%**, and among all respondents 25–40, **15.44% vs 15.75%**. Small cells, local sampling, different ages and retrospective exposure prevent strong population or causal conclusions. [SOURCE: `subgroup_rates.csv`, `composition.csv`; these are exploratory sensitivity cuts, not prespecified confirmatory hypotheses.]

Origin verification also matters: **178 of the 196 strict self-identified G3 respondents** have a matched Mexico-born grandparent answer. Sixteen report other foreign grandparent countries without confirmed Mexico birth; two have unresolved foreign-country details. Across all sampled identities, 180 qualify, including two coded Black non-Hispanic. G4+ cannot receive symmetric exact-Mexican-origin verification without great-grandparent birthplace. Those two nonidentifiers do not estimate national ethnic attrition. [SOURCE: `audit.json`; SCOPE.]

The better classification is a **family migration-history profile**: respondent birthplace/arrival age; each parent's birthplace; each observed grandparent's birthplace; known/unknown status; birth and arrival cohorts; and self-identification as a separate field. “One Mexico-born grandparent out of four” is meaningful when all four were observed. It is not “genetically one-quarter Mexican,” and an unknown grandparent is not a US-born grandparent. This preserves mixed origins and makes each dataset's actual coverage visible. [MEASUREMENT PRINCIPLE]

## 5. Which larger claims do these data answer?

| Question | Current support | Missing discriminator |
|---|---|---|
| Are measured fiscal profiles lower than a stated resident benchmark? | Yes, substantially in these accounts; magnitude depends on reference/allocation | Reconciled omitted components and better donor/parameter transport |
| Is admitting another specified cohort a net fiscal loss? | Not identified by a resident-stock reference gap | A no-additional-admission or alternative-intake counterfactual, lifetime paths and budget response |
| Do current residents gain in welfare? | Not identified by this fiscal account | Incumbent worker/owner/renter effects, prices, services, time horizon and distributional weights |
| Do later-generation schooling and criminal-justice outcomes move together? | The held local data show different directions across outcomes | Representative lineage follow-up, outcome-specific exposure and missingness |
| Do all LATAM groups resemble the Mexican-origin average? | Existing country results contradict that blanket transfer | Larger, comparable country/parent cells; separate crime/trust measurements |
| Does persistence identify a genetic mechanism or inevitable trust decline? | No causal identification here | Evidence distinguishing those mechanisms from selection, cohort, family, institutions and measurement |

[INFERENCE tied to measured scope. For the country row, the [five-year CPS comparison](immigration-latam-benchmark-comparison-2026-09-17.md) finds several near-benchmark economic point estimates, especially Cuban-parent descendants, while precise joint parity remains unestablished. The [trust/SEAsia review](immigration-latam-southeast-asia-trust-2026-09-17.md) concerns different evidence; neither is replaced by this Mexican-origin ledger.]

This distinction is economically consequential. A hypothetical entrant paying a net $5,000 while a native reference pays $10,000 has a −$5,000 reference gap, yet adds +$5,000 directly compared with no entrant, before indirect effects. A real policy can instead compare alternative entrants, in which case differences between their profiles matter. Specifying that counterfactual makes the reference-gap calculation useful without turning it into the wrong fiscal object. [ILLUSTRATIVE ALGEBRA, not an estimate.]

Primary literature reinforces the distinction. NAS separates immigrants' direct flows from changes in incumbents' flows and from lifetime projections. CBO's July 2024 federal surge forecast explicitly modeled broader economic effects; its separate June 2025 report estimated **$9.2bn direct state/local cost in 2023**, or $9.8bn under an alternative broader construction. These are dated, differently scoped estimates, not amounts to add to this annual Mexican-origin account. A favorable federal forecast does not erase local costs. [SOURCE: [NAS conceptual chapter](https://www.nationalacademies.org/read/23550/chapter/12), [CBO federal report](https://www.cbo.gov/publication/60569), [CBO local report](https://www.cbo.gov/publication/61256).]

Clemens's capital-tax adjustment models additional capital income accompanying an extra worker; it is not the allocation of a fixed corporate-tax pot by current ownership. Colas–Sachs models indirect fiscal benefits through incumbent labor-market responses, but its held working paper explicitly retains a burden for high-school dropouts. These channels warrant a separate policy model; they cannot simply be added to one another or assumed to reverse every adverse result. [SOURCE: [Clemens2023](https://www.cgdev.org/publication/fiscal-effect-immigration-reducing-bias-influential-estimates), [Colas–Sachs working paper](https://hdl.handle.net/10419/282044), held manuscript2022 despite its local filename's2024 label.]

The next highest-value improvement is therefore **counterfactual evidence**, not another expansion of one burden scalar: calibrate a specified intake by age, origin, eligibility and destination; reconcile federal/state/local components; test spending and incumbent-response assumptions. For later-generation claims, the binding gap is symmetric origin histories including nonidentifiers and representative follow-up. Current data already support sizeable, outcome-specific differences; stronger ancestry or policy claims require those additional observations. [INFERENCE / DEFEATERS]

## Validation and revisions

The raw all-age run produced1,144 estimates with baseline reproduction,35 adult component mean/SE anchors, every-scenario component reconciliation, all161-vector union/fixed-budget identities, donor gradients and paired covariance. Independent in-task reviews examined the scientific constructs, fiscal estimator and IIMMLA raw logic. External GPT/Claude review remains unperformed because automatic approval review blocked packet egress pending explicit user permission. [SOURCE: lane audit files and [review disposition](../notes/immigration-construct-review-2026-09-17.md).]

LLM framing can favor either a large-cost narrative or optimistic omitted benefits. This analysis retains the adverse benchmark gaps, positive partial balance, allocation sensitivity, incomplete stepwise convergence and mixed IIMMLA outcomes together. Sampling intervals and sensitivity ranges remain distinct; neither is a complete identification bound. [INSTRUMENT / QUANT-BIAS]

- **2026-09-17:** [Decision](../decisions/2026-09-17-fix-accounting-and-generation-comparisons.md) advances the previous aggregate audit with a raw all-age extension and strict family-history analysis, while preserving earlier estimates as historical constructions.

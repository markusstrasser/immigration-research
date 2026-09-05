# Immigration — Interpreted Insights (2026-06-24; repaired 2026-09-05)

**Verdict:** The defensible conclusions concern specific populations, observed outcomes and fiscal ledgers. Several June exports exceeded those boundaries: race restriction was called matching, CBO projections were treated as realized gains or a proven ceiling, fiscal balances were treated as incumbent welfare, and administrative coverage was treated as a national bound. This version replaces those inferences. Numerical conviction scores in the historical record are judgment labels, not calibrated probabilities. [INFERENCE]

## Crime comparisons and generations

Light, He & Robey’s Texas study and Cato’s Texas conviction series report lower unauthorized than native rates for their observed outcomes/populations. They share important underlying administrative data; multiple analyses are not wholly independent replications. Arrest, conviction and incarceration differ from latent offending and from a policy’s causal crime effect. [SOURCE: https://doi.org/10.1073/pnas.2014704117; https://www.cato.org/policy-analysis/illegal-immigrant-murderers-texas-2013-2022]

Cato’s 2023 incarceration rates yield `1−613/1,221 = 49.8%` lower for unauthorized versus all natives and `1−626/891 = 29.7%` after excluding Black respondents from both groups. These are different descriptive populations. The restriction does not standardize the remaining race distribution or other covariates, so the 20.1-point difference is not an estimated correction to a biased rate. Nor can this national incarceration comparison adjust a Texas arrest estimate. [SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf; RECALCULATION; INFERENCE]

If `a` is the second-generation share among natives, `r_native = a·r_2 + (1−a)·r_3+`. Evidence that the second generation exceeds the first (`r_2>r_1`) does not establish that it exceeds third-and-higher generations. Area-level immigrant-share studies do not identify individual generational offending; selected jail interviews do not give population rates. [SOURCE: studies reviewed in https://www.ojp.gov/pdffiles1/nij/grants/310356.pdf, pp. 11–12; INFERENCE]

Enforcement has possible removal/incapacitation, deterrence and reporting channels. A lower observed immigrant rate does not determine the net effect of a particular enforcement policy. Underreporting can affect recorded offending as well as police-recorded victimization; an insignificant policy estimate is not evidence of exact zero. [SOURCE: https://www.nber.org/papers/w32109; INFERENCE]

## Fiscal accounting, GDP and welfare

CBO’s July 2024 report **projects** about $897B lower covered federal deficits from its 2021–2026 surge over 2024–2034. It includes revenue, mandatory spending and net interest, excluding discretionary appropriations and state/local budgets. Its illustrative proportional discretionary-spending case adds about $0.2T. The exclusion requires a coverage caveat; it does not prove the headline is a ceiling. The $8.9T nominal-GDP gain is a separate output projection and must not be added to fiscal revenue or treated as incumbent income. [SOURCE: https://www.cbo.gov/publication/60165]

A NAS age-25 less-than-high-school figure of −$109k is a fiscal NPV for a specified scenario, not an estimate of incumbent natives’ total welfare. The published Clemens correction can change the sign under its capital-tax assumptions, but this repository has not reproduced both sides in one matched microsimulation. Do not splice an annual cash-flow estimate, a different cohort’s NPV and a dynamic model result into one accounting identity. [SOURCE: https://www.nationalacademies.org/read/23550/chapter/13; https://doi.org/10.2139/ssrn.3982027; INFERENCE]

The project’s earlier Mexico SIPP/ACS annual estimate of +$1,519 per adult (+$12.9B aggregate) is withdrawn pending the household/person allocation and education-code rebuild documented in the September decision. It is not valid support for a net fiscal, assimilation or native-comparison conclusion. [SOURCE: ../decisions/2026-09-05-material-inference-repair.md]

NAS Table 9-6’s approximate first/second/third-plus-generation state/local balances (−$1,600, +$1,700, +$1,300) are **annual 2011–2013 averages per independent person including allocated dependents**, not lifetime NPVs. Adding later-generation averages and dividing by the first-generation deficit does not yield a dynasty return: they are not linked descendants, and horizon, population weights and allocation must match. [SOURCE: https://www.nationalacademies.org/read/23550/chapter/14; INFERENCE]

Cato’s historical first-generation balance does not secretly bank future descendant taxes. Its combined-generation alternative includes child/second-generation costs and taxes; no matched state/local sensitivity here shows that removing either public-goods or child-allocation assumption necessarily reverses the sign. See [the repaired Cato memo](immigration-dismantle-cato-2026-06-25.md). [SOURCE: https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023; INFERENCE]

Cost concentration and aggregate gains can coexist, but a positive aggregate need not make every group better off and no compensation is automatic. Conversely, one local cost or negative fiscal balance is not proof of net national welfare loss. Higher rent payments transfer resources between tenants and owners and can accompany real crowding or construction effects; the whole rent increase is not lost national output. Migrant income gains, incumbent income, fiscal balances and global welfare must be measured separately before assigning welfare weights. [INFERENCE]

## What SCAAP counts can establish

BJA’s FY2023 SCAAP solicitation covers qualifying incarceration during **July 1, 2021–June 30, 2022**, not calendar-year 2023 offending. The program reimburses part of qualifying correctional costs for people meeting its criminal-conviction, custody-duration and immigration-status definitions. “Criminal alien” in this program must be interpreted through those definitions, not equated casually with either all foreign-born people or every noncitizen. [SOURCE: https://bja.ojp.gov/news/now-available-fy-2023-state-criminal-alien-assistance-program; https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/overview]

The June parse reported approximately 7.8M confirmed-status inmate-days, 6.5M unresolved-status days and $210.4M in awards. These are historical program-extract totals retained as approximate descriptive counts, not a fresh September database verification. The unresolved category is prefiltered by applicants’ reasonable belief, not proof that every unresolved person has a particular citizenship or immigration status. [SOURCE: local parser `infra/immigration-fiscal/build/parse_scaap_awards.py` and BJA award/solicitation files; current aggregate checksum UNVERIFIED]

Adding all unresolved submitted days to confirmed submitted days gives a sensitivity scenario for that submitted record set. It is **not a national upper bound**: nonparticipating jurisdictions, ineligible custody and classification error remain outside it. Inmate-days are cumulative custody person-time, not a point-in-time prisoner stock, unique offenders or offense incidence. Dividing by a matched total-inmate-day denominator can produce a custody share; it still does not give a population offending rate. [INFERENCE]

Awards are formula-based partial reimbursements and differ from full costs. A reimbursement-per-day ratio cannot by itself recover a jurisdiction’s marginal or total cost; it also need not be unrelated to costs, since salary and custody measures enter the formula. Award concentration describes the program, not the national crime distribution. [SOURCE: https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/funding; INFERENCE]

State totals such as SCAAP days, foreign-born population, LEP enrollment and Medicaid enrollment may co-scale with population. A raw correlation does not identify an immigration effect, but co-scaling alone does not prove every adjusted relationship spurious. Require aligned years, coverage, denominators and a defensible causal design. ACS foreign-born aggregate counts are publicly available; restricted microdata are not necessary for every denominator. [INFERENCE]

## Assimilation and local outcome proxies

The synthetic-arrival-cohort builder observes different people in repeated cross-sections, aged 25–64, relative to all natives in that age range. Changing ages, period effects, selective exit and arrival-decade composition remain. Its positive-income mean does not describe people with zero/negative income. Thus convergence in those cells is descriptive, not a within-person causal assimilation rate or a test that rules out fixed-trait explanations. Recent ACS also lacks parental birthplace for a direct second-generation-by-origin classification; the CPS parental-birthplace design answers a separate cross-generational comparison. [SOURCE: `infra/immigration-fiscal/build/build_immigrant_assimilation_profile.py`; `infra/immigration-fiscal/build/load_cps_second_gen.py`; INFERENCE]

The QWI outcome used for E-Verify is **average monthly earnings of stable/full-quarter employees**, with no nativity variable in the sex-by-education API. It is not hourly pay or native-born earnings, and a nonsignificant estimate cannot establish a native-wage null. [SOURCE: https://api.census.gov/data/timeseries/qwi/se/variables.html]

## Provenance and unresolved empirical questions

The June inventory, local reproduction status and corpus weights are historical workflow metadata; they are not current holdings or evidence that a claim is true. Raw data now exist under `/Volumes/2TBPNY/research-data/immigration-fiscal/data`; the former `sources` symlink does not establish absence. Corpus-weight averages and uncalibrated conviction scores do not measure evidential bias or calibrated probabilities. [SOURCE: current path inspection; INFERENCE]

Open questions include matched national unauthorized offending, policy-specific enforcement effects, the rebuilt full fiscal ledger, linked-descendant fiscal effects and causally identified assimilation. Those are genuine empirical limits, not proof that the effects are zero or of a favored sign.

## Revisions

- **2026-06-25 — cross-model red-team (GPT-5.5 + Gemini, two non-Claude labs).** Five confirmed corrections applied; full adjudication in `immigration-redteam-2026-06-25.md`. (1) §2.1 second-generation crime convictionscore **0.88 → 0.65** — both labs flagged it as inconsistent with the node's own null-to-weakly-protective, non-unauthorized-specific evidence. (2) §1.3 federal heading reframed "RAISED/CUT" → "**CBO *projects***" + added the discretionary-baseline accounting-artifact caveat (direction supported, magnitude is a projection ceiling). (3) §1.1 "Direction is **bulletproof**" → "robust across independent datasets." (4) §2.2 enforcement "**null-to-HARMFUL**" reframed as a genuine trade-off (removal/incapacitation vs reporting-suppression; net sign contested) — the prior version omitted incapacitation. (5) Heritage-vs-Clemens skepticism asymmetry noted (the instrument-tilt the operator flagged, caught in our own scores). The red-team tightened the headline; it did not overturn it.

- **2026-09-05 — Replaced proxy, accounting and generational exports with matched estimands** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Historical revision entries above describe the earlier state, including conclusions superseded here.

## Historical quoted text retained verbatim

These are quotations retained from the June memo, not a renewed endorsement of their surrounding inference.

> **Instrument-bias caveat** (`notes/llm-bias-caveat.md`): this analysis is produced through a frontier LLM whose post-training carries a soft progressive prior, strongest exactly on immigration/crime/justice framings. Mitigation here is structural, not stylistic — every load-bearing magnitude below is anchored to a **nonpartisan or against-interest** primary source (CBO, NAS, BJA, PNAS/AER; Cato corrections that *shrink* Cato's own headline). Direction claims that rest on advocacy sources are deflated or flagged. Read the framing-sensitive section as the place the instrument's thumb is most likely on the scale.

> **Honest framing:** most roadmap crime/mobility datasets are **not downloaded**. For these nodes, conviction is "what the existing peer-reviewed corpus expects," not what this stack has computed. The SHARP/killable versions require micro-data the warehouse lacks.

## Historical quoted strings retained verbatim

These quotations, hypotheses and labels appeared in the June working memo. They are retained for provenance; they are not a renewed endorsement or certification as primary-source quotations. Current conclusions and source scope are above.

"Highest-conviction node in the entire crime picture"

"the adjustment changes the sign of lifetime net fiscal impact: from –$109,000 to at least +$128,000 without including children and grandchildren."

"this is not a general equilibrium effect… an instantaneous, static effect… at partial equilibrium (fixed factor prices)."

"represent only a portion of the criminal alien population."

"know or reasonably believe are undocumented criminal aliens"

"top-5 incl. FL, not the named top-4."

"what the literature expects, not locally computed."

"43 states + PR + VI; 8 of 51 states+DC absent incl. DC"

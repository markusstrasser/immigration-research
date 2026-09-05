# Immigration — Falsifiable Claim Candidates (2026-06-24; designs repaired 2026-09-05)

**Status:** Proposals, not pre-graded findings. The seventeen IDs are retained, but invalid tests and predetermined outcomes are replaced below. A source locator or automated confidence score does not settle a claim. Administrative data can still have coverage/classification errors; a peer-reviewed design can still depend on disputed assumptions. [INFERENCE]

**Common requirement:** State the measured outcome, population, denominator, horizon and counterfactual before testing. Estimate uncertainty rather than treating failure to reject as equality. A test of a different estimand cannot confirm or falsify the original by sign alone. [INFERENCE]

## C1. Texas status-group arrest comparisons

Estimate the original status-group rate, then separately estimate a common-covariate-standardized comparison if numerator and denominator both contain compatible race/age/sex fields. Non-Black restriction alone is not matching. National incarceration ratios cannot predict or correct Texas felony-arrest ratios. Data: Light replication, DOI10.3886/E124923V1; compatible Texas population counts. Do not assume a below50% result. [INFERENCE where design guidance]

## C2. Citizenship-specific prison prevalence

Use SPI2016 design weights and a citizenship denominator for the same date, ages and geographic prison universe. SPI is a survey of people in state/federal prisons, not a census of all jail/prison custody; ACS institutional group quarters are not identical to that universe. Noncitizen is not unauthorized. A disagreement need not falsify an estimate for a different population. Data: BJS SPI, ICPSR37692; ACS citizenship counts. [INFERENCE where design guidance]

## C3. Federal conviction composition by offense

Tabulate USSC citizenship and offense categories with a stated person/case and fiscal-year unit. Show with/without immigration offenses. Do not presume overrepresentation disappears after exclusion; federal convictions, nonresident defendants and immigration offenses require their own comparison population. The result is not a total US offending rate. Source: https://www.ussc.gov/research/datafiles. [INFERENCE where design guidance]

## C4. Sanctuary-policy effects within a specified design

Choose a policy definition, treatment date, outcome and counterfactual, then report effects and confidence intervals. A null estimate is not proof that all sanctuary policies have zero effect. Generic NIBRS joins need reporting-coverage checks and plausible treatment timing; a convenient comparison group is not automatically a valid control. Source: https://doi.org/10.1073/pnas.2014673117. [INFERENCE where design guidance]

## C5. Net crime effects of specified enforcement programs

Separate observed offenses, victimization, reporting, deterrence and incapacitation. Secure Communities and287(g) are different interventions. Failure to detect a net reduction does not prove deterrence/incapacitation is absent. Report policy-specific intervals and risks to identification. Source: https://www.nber.org/papers/w32109. [INFERENCE where design guidance]

## C6. ICE docket numerator audit — invalid rate proposal withdrawn

Do not divide cumulative criminal-noncitizen docket counts by unauthorized stock or arbitrarily annualize them. Those records lack the matching event dates, offender/residence universe and risk time required for an annual native comparison. A valid proposed test is to reconcile docket categories and count definitions; a rate study needs separately obtained dated events and matched person-time. Source: https://homeland.house.gov/wp-content/uploads/2024/09/24-01143-ICEs-Signed-Response-to-Representative-Tony-Gonzales.pdf. [INFERENCE where design guidance]

## C7. Removal-policy effect on a clearly named population

Define whether the outcome concerns the US locality losing a resident, the origin-country locality receiving a deportee, or a household’s victimization. These are not interchangeable. An aggregate county effect cannot directly test the removed person’s incapacitation effect. Verify the proposed instrument and its exclusion restriction before analysis; IZA dp12413 remains a source lead, not an identification certificate. [INFERENCE where design guidance]

## S1. Generational fiscal balances on one accounting basis

Reproduce NAS Table9-6 as annual2011–2013 state/local averages per independent person including dependents. It is not a lifetime-NPV or linked-dynasty ranking. Later-generation positive averages do not by themselves offset a particular parent cohort’s costs. A different lifetime microsimulation does not falsify the historical annual table. Source: https://www.nationalacademies.org/read/23550/chapter/14. [INFERENCE where design guidance]

## S2. Child income rank at a fixed parental rank

Compare predicted child ranks for the same parental rank, cohort and origin, using both intercept and slope. A lower rank-rank slope alone does not mean lower upward mobility. Read the study’s supported origin groups and child/parent sample definition; do not assume near-universality from a headline. Source: https://www.aeaweb.org/articles?id=10.1257/aer.20191586. [INFERENCE where design guidance]

## S3. Second-generation observed crime outcomes

Compare first, second and third-plus generations within compatible samples and outcomes. Parity with third-plus generations would erase a first-generation advantage but would not imply excess relative to other natives. Selected jail samples and area-level shares cannot settle individual population rates. Verify that proposed OpportunityAtlas releases contain the exact parental-nativity/incarceration cross-tabulation before promising a test. Source lead: https://opportunityinsights.org/data/. [INFERENCE where design guidance]

## S4. Benefit receipt by age, citizenship and generation

Separate descriptive group means from a within-person or lineage transition. Naturalization and benefit eligibility are selected and age-dependent. A noncitizen/naturalized comparison does not establish second-generation receipt. Use compatible SIPP/CPS definitions and rebuilt person-level benefit allocations; do not reuse the invalid household-to-person donor result. Source lead: https://www.cato.org/sites/cato.org/files/2022-03/BP-137.pdf. [INFERENCE where design guidance]

## Q1. Refugee annual fiscal crossover versus cumulative balance

Evans–Fitzgerald’s synthetic cohort of arrivals aged18–45 shows annual taxes tending to exceed benefits after year8; that is not cumulative fiscal payback at year8. They estimate about+$21k discounted over20years for their covered taxes/benefits. HHS’s historical multi-cohort account is a different estimand. Reproduce costs, horizon, refugee imputation and discounting separately. Sources: https://www.nber.org/papers/w23498; https://leo.nd.edu/assets/240441/44914_w23498.pdf. [INFERENCE where design guidance]

## Q2. Emergency Medicaid account reconciliation

Use the CBO/CMS spending scope, reference years, federal/state split and eligibility definitions. Emergency Medicaid is not total immigrant medical spending and can include legally present ineligible noncitizens. A smaller program total does not by itself falsify a broader MEPS/SIPP spending estimate. Source: https://www.cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf. [INFERENCE where design guidance]

## Q3. Matched NAS/Clemens scenario reproduction

Reproduce the specified age/education/horizon and capital-tax assumptions before comparing signs. Clemens’s correction uses a partial-equilibrium framework under stated assumptions, not a blanket GE truth. Failure of an unmatched local microsimulation to reproduce a published scenario is a mismatch, not disproof. Sources: NAS2017; https://doi.org/10.2139/ssrn.3982027. [INFERENCE where design guidance]

## Q4. Ownership versus firm formation

Verify the ABS schema, survey unit, owner nativity and eligible firm population first. Ownership stock is not a founder flow, job creation or the net employment effect of immigration. Population ownership prevalence needs an owner count and compatible people denominator; firm counts with multiple owners cannot be substituted silently. Source: https://www.census.gov/data/developers/data-sets/abs.html. [INFERENCE where design guidance]

## Q5. CBO state/local surge account on its own horizon

The approximate −$2.1k per added resident is a derived quotient of rounded2023 totals, not a universal per-person loss. Adding federal or descendant effects may change the sign, but positivity is not guaranteed by S1. Reproduce the same population, time, coverage and counterfactual before combining ledgers. Source: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf. [INFERENCE where design guidance]

## Q6. SCAAP submitted custody and reimbursement trends

Tabulate qualifying inmate-days and awards within comparable participating jurisdictions and custody reference periods. FY award labels are not offense years; awards are partial reimbursement, not total or marginal costs. Unknown-status records and participation changes prevent a national ceiling or a clean offending trend. Sources: https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/overview; BJA annual solicitations. [INFERENCE where design guidance]

## Priority and historical screening record

Repair the invalid C6 rate conversion, S2 mobility test, Q4 ownership/founding substitution and Q1 payback definition before acquisition. Other candidates require schema/coverage probes and a written estimand; do not rank them by expected agreement with the corpus.

The June automated screening log is retained below as a historical tool output, not an endorsement of its verdicts or probability calibration.

## Verification log (this pass)

| Claim | Tool | Verdict | Confidence |
|---|---|---|---|
| S1 (2nd-gen top net contributors) | verify_claim/Exa | supported | 0.9 |
| C4 (sanctuary no crime increase) | verify_claim/Exa | supported | 1.0 |
| S2 (2nd-gen mobility > native) | verify_claim/Exa | supported | 1.0 |
| C5 (enforcement reduces crime) | verify_claim/Exa | **contradicted** | 0.95 |
| S4 (per-capita welfare rises by generation) | verify_claim/Exa | supported | 1.0 |
| Q1 (refugee 8-yr break-even, 20-yr net+) | verify_claim/Exa | supported | 1.0 |

Note: Exa /answer is web-grounded, not adversarial cross-model; treat confidences as a triage signal, not a final grade. All six were sense-checks of the claim *direction*; the ledger entry must still be settled against the paired primary dataset.


## Revisions

- **2026-09-05 — Replaced invalid falsification tests and predetermined signs.** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Earlier dated revision entries describe the historical state, including superseded conclusions.

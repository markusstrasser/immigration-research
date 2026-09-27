# Strong objections without discarding real costs

**Verdict:** The strongest remaining attacks concern connections between models,
not the legitimacy of counting public services, victim suffering or institutional
risk. This pass confirms an unreconciled public-payroll response, identifies a
material mixed-household exposure, and finds a proposed preferences term whose
population-removal interpretation exceeds its source. It also catches a stale
claim that incorrectly dismisses amenity harm. None supplies a defensible new
aggregate total or establishes a reversal of the conditional annual result.
[INFERENCE; evidence and rebuttals below]

September 28, 2026. Adversarial research brief, starting at `ab66513`. Target:
the reasoning supporting the September 27 annual account and its broader social
extensions. Frame: effects on other US residents, including other immigrants.
This is a continuation of the [September 27 audit](immigration-conceptual-audit-2026-09-27.md),
not a rerun of every source or a new adopted model. The question is what a strong
critic could establish, regardless of political affiliation. [SCOPE]

The strongest skeptical case survives: employers' or consumers' gains need not
compensate taxpayers, renters, competing workers or victims; preserving a service
can require costly resources even when GDP rises; some institutional and amenity
effects are poorly represented in market income. The burden of proof is the
size, incidence and causal connection of each term. It is not a requirement that
every real harm first appear in a wage regression. [INFERENCE; the existing
[second-order synthesis](immigration-second-order-effects-2026-09-05.md)]

## 1. Public workers have an employer: the production and budget models must agree

**New modeling gap; size and net direction unresolved.** The production builder
puts civilian public and private workers' positive earnings into the same two
skill groups. The model changes their wages and divides the resulting income
change into private income P and induced tax receipts F. The fiscal engine prices
services using baseline assigned spending multiplied by response coefficients;
it does not receive those wage changes. [CODE: [production builder](../infra/immigration-fiscal/matched_benefits_2026_09_19/builder.py),
lines 92–121; [income partition](../infra/immigration-fiscal/matched_benefits_2026_09_19/model.py),
91–107; [fiscal engine](../infra/immigration-fiscal/assumption_explorer_2026_09_21/engine.js), 165–178]

Hold the public workforce and its output fixed. If an included public employee
receives one additional dollar of gross pay, their after-tax gain and the induced
tax receipt sum to one dollar. Their public employer also pays one dollar. At
equal fiscal/private dollar weights this transfer cancels. Applying only the
worker side fails that consistency check. If nominal public budgets instead stay
fixed, employment, output or service quality must adjust. [DERIVATION, conditional
on the stated public-sector response; government consumption includes employee
compensation, [BEA definition](https://www.bea.gov/help/glossary/government-consumption-expenditures)]

The [fiscal probe](../infra/immigration-fiscal/conceptual_audit_2026_09_28/probe_fiscal.cjs)
changes the substitution elasticity from 1.5 to 2 to 2.5 in one package specification.
Production plus induced receipts changes from $11.772bn to $8.791bn to $7.014bn,
while direct fiscal response stays at −$313.288bn and the imputed capital return
at $34.153bn. These are diagnostic annual 2024-dollar model values, not the adopted
band or a correction to it. They verify the separation of the two calculations.
[CALCULATION]

**Defense worth keeping:** public pay can be sticky, and empirical spending
responses may already contain price changes. It remains unverified whether the
adopted spending response includes the payroll change implied by the production
model. Sticky public pay would instead require a corresponding production-side
restriction. Neither a missing dollar amount nor a government-output or capital
double count has been established. The
smallest useful repair is a public-pay scenario with a matching payroll term,
or explicit fixed public pay with the production side adjusted consistently.
Purchased inputs then need the same check. [INFERENCE / PROPOSED TEST]

## 2. Mixed households make assigned benefits different from avoidable benefits

**Newly quantified exposure; no estimated fiscal correction.** On the original
canonical CPS source frame, 6.970 million people outside the target share an SPM
resource unit with target members; 1.538 million are children under 18. There are
8.684 million target members in these mixed units. An SPM resource unit is not
necessarily a family, and these counts do not identify spouses or caregiving ties.
[CALCULATION: [population probe](../infra/immigration-fiscal/conceptual_audit_2026_09_28/probe_population.py);
ASEC 2025 baseline weights, before the later population correction]

The spending builder divides observed unit benefits among existing members and
allocates national totals using the resulting group shares. It does not recalculate
eligibility or household resources after a member disappears. Personal and shared
allocation variants therefore do not bracket a household's behavioral response.
[CODE: [builder](../infra/immigration-fiscal/full_account_spending_2026_09_20/builder.py),
157–169, 198–244 and 264–273]

As a diagnostic of exposure, 16.35% of the target's raw assigned SNAP dollars
are in mixed units, as are 18.37% of housing-support dollars and 21.26% of WIC
dollars. These are shares of uncalibrated CPS allocations, not shares of the
adopted spending total or amounts to subtract. Losing an earner could increase
remaining members' support; losing a dependent could reduce it by a different
amount than their assigned share. Joint tax liabilities and unpaid care also need
their own treatment. [CALCULATION / INFERENCE]

**Defense worth keeping:** assigning observed incidence is a legitimate exercise.
The gap appears when an assigned benefit is called a payment saved by a policy.
A useful next test is one program's actual benefit rule on mixed units, holding
the remaining people fixed and stating what happens to earnings. That would test
a fiscal response without pretending to reconstruct alternative family histories.
[PROPOSED TEST]

There is a broader welfare implication. Where relationships exist, family life,
unpaid care and companionship can benefit the very outside-group residents the
account includes. They cannot all be dismissed as benefits only to excluded
migrants. Equally, this exposure count does not measure those benefits or establish
an offset to the headline. Historical absence and disruption of present families
are different comparisons. [UNQUANTIFIED MECHANISM]

## 3. Benefiting from preferences does not establish the policy loss removed

**Confirmed overstatement in a proposed extension; outside the adopted headline.**
The preferences producer estimates losses to white natives relative to alternative
selection policies, then uses beneficiary shares to attribute part to Mexican-origin
residents. Its source explicitly distinguishes transfers, procurement premiums
already in public spending, and policy causation. The consumer nevertheless labels
the attributed part “the part the counterfactual removes” and adds it to its
`with_proposed` scenario. [DATA/CODE: [producer](../infra/immigration-fiscal/affirmative_action_cost_2026_09_24/RESULT.md),
63–80 and 310–339; [consumer](../infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py),
544–559, 1604–1616, 1744–1753 and 2259–2262]

The consumer's central attributed loss is $0.58bn annually. Its taxpayer-premium
portion is about $37.1m: the source's $0.4773bn DBE premium times 0.0782, then the
consumer's rescaling from $0.58402805bn of component estimates to its rounded
$0.58bn total. An exact $37.1m duplicate is **not established**: procurement prices,
fiscal allocation keys and service/capital responses have not been matched.
[CALCULATION: [source rows](../infra/immigration-fiscal/affirmative_action_cost_2026_09_24/derived/channels.csv);
the source describes weak, transported evidence and scenario ranges]

**Strong critique:** removing one eligible group may transfer opportunities to
other eligible groups who remain in the beneficiary population. It need not end
the preference or return every seat, job and contract to white natives. The
beneficiary share supplies neither the policy response nor the replacement allocation.
[INFERENCE]

**Defense worth keeping:** displaced applicants' lost opportunities can be real.
A transfer to excluded target members can be a cost to included people under this
frame. “It is only a transfer” does not refute that. Preserve the distributional
scenario, but label its replacement rule, carry gains to other included recipients,
and reconcile the procurement premium before adding it to a fiscal-plus-social sum.
This is not a reason to erase discrimination or contracting inefficiency.
[INFERENCE / PROPOSED TEST]

## 4. A repaired source still became an unwarranted zero in synthesis

The wider synthesis said housing prices show no amenity discount. The corrected
hedonic source instead reproduces the historical coefficients and leaves the modern
composition-amenity dollar effect unidentified. That is a substantive difference:
an unresolved contemporary effect does not establish no harm. The stale synthesis
claim is corrected in this pass, preserving the earlier wording in its revision
record. The adjacent innovation claim also needed qualification: its source's
corrected patent scenario has a positive point estimate with very wide uncertainty.
It establishes neither zero effect nor a defensible dollar offset. Both channels
remain unpriced here. [DATA: [hedonic replay](immigration-hedonic-replay-2026-09-19.md), 71–77;
[scale/innovation correction](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md), 36–45;
[social-cost synthesis](immigration-real-fiscal-and-social-costs-2026-09-23.md), §8]

House prices combine demand, supply, school quality, crime, housing quality and
sorting. Higher aggregate prices do not prove better amenities; lower relative
prices do not identify a pure dislike of ethnicity. Nor can a capitalized school,
crime or tax effect automatically be added to those same underlying losses.
Keep the amenity question open and specify the overlap before monetization.
[INFERENCE from the source's identification limits]

## 5. Two tempting attacks that do not kill the fiscal result

**“Everyone is negative because the government runs a deficit.”** This is a strong
objection to reading an assigned negative balance as special evidence about a
group. It is not an automatic correction to the incremental account. The engine
separately reports the assigned balance, the gap against an average resident and
the response-weighted fiscal change. The baseline national deficit is already
explicit. [DATA/CODE: [annual account](immigration-complete-annual-account-2026-09-20.md),
82–108; fiscal engine, 175–187]

The defensible conditional interpretation holds the baseline financing burden
common and values the incremental public-resource difference dollar for dollar
for the remaining residents. A claim about actual long-run welfare then needs
the tax, spending or debt adjustment that delivers it. The National Academies
likewise makes future budget policy an explicit scenario choice and cautions
against transporting small-change partial-equilibrium results to large flows.
Its particular results are not a correction to our different population and
annual comparison. [SOURCE: [2017 report, chapter 8](https://www.nationalacademies.org/read/23550/chapter/13),
pp.409–412 and 461–462; INFERENCE]

**“Equally poor natives cost money too.”** A matched comparison is needed to
support an origin-specific explanation; it is not needed to describe actual
costs under current policy. Matching on earnings also matches a major tax base.
Conversely, an unadjusted origin gap cannot identify culture, discrimination or
an immutable group characteristic. The existing [education-specific analysis](immigration-education-fiscal-and-methods-2026-09-19.md)
already separates these questions and includes favorable same-education comparisons.
Retain both the actual composition and the conditional comparison. [INFERENCE]

## 6. Nonlinearity: a generation share is not a marginal immigrant's effect

The existing generation code is careful: it allocates one union experiment along
a proportional path, and separately exports standalone generation removals. In its
GDP-normalized reference, the union production-plus-receipts benefit is $13.323bn;
the three standalone experiments sum to $6.252bn. Cash normalization gives $8.791bn
versus $4.125bn. The standalone experiments also have different remaining populations.
They therefore cannot be added as if they partitioned one common counterfactual.
[DATA/CALCULATION: [production export](../infra/immigration-fiscal/generation_account_2026_09_24/derived/production_by_generation.json);
population probe; [generator](../infra/immigration-fiscal/generation_account_2026_09_24/production.py), 10–18]

This confirms why “generation shares of the union account” is the right description.
The attribution is not broken. Dividing it by adults does not identify an additional
adult's causal effect. Similarly, counting half a child's lineage avoids duplicate
attribution without establishing whether that birth would have occurred with a
different partner. Both issues need an explicit policy baseline before admission
or historical-population conclusions follow. [INFERENCE; [lineage construction](../infra/immigration-fiscal/lineage_cost_2026_09_19/README.md)]

## 7. Keep the wider costs, and test the right outcomes

“Economists only examine narrow channels” is too general: the National Academies
has an entire chapter covering housing, prices, innovation, growth and nonmarket
activity. A particular wage or peer-effects study can still leave the relevant
harm outside its design. Criticize that specific boundary. [SOURCE:
[chapter 6](https://www.nationalacademies.org/read/23550/chapter/10), pp.279–282]

| Channel worth retaining | Strong defense of counting it | Connection a critic can reasonably demand |
|---|---|---|
| Schools and service capacity | Teachers, buildings and preserving quality use resources; zero cash adjustment can conceal deterioration. | Couple spending and capacity to residual quality. Count harm remaining after the chosen response, rather than also charging the harm that response prevents. |
| Crime and intimidation | Deaths, injuries and fear matter beyond criminal-justice spending; a below-average offending rate need not imply zero additional victims. | Distinguish attributed victim harm from a policy's preventable harm, including changes in other offending and victim exposure. |
| Housing and neighborhood change | A rent transfer can materially hurt renters even when owners gain; displacement and moving costs can be real. | Show recipients and losses, supply adjustment, geography and any amenity component without repeating capitalized effects. |
| Trust and institutions | Cooperation, impartial administration, rights and public safety have value beyond wages. | Measure the particular behavior or institutional outcome. Party share, confidence and a national cultural average are not interchangeable with performance. |
| Environment and congestion | Time, noise, emissions and crowding can impose costs outside the budget. | Identify affected residents, changed activity and capacity; do not infer total exposure from population alone. |
| Family, care, variety and innovation | Benefits to other residents can occur outside measured income too. | Apply the same causal and transport standards; distinguish unpriced mechanisms from known dollar offsets. |

[INFERENCE / PROPOSED TESTS grounded in the existing [school-capacity evidence](immigration-school-capacity-harms-2026-09-20.md),
[victim-cost definition](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md),
[political-panel limits](immigration-political-trajectory-county-panel-2026-09-19.md),
[trust analysis](immigration-latam-southeast-asia-trust-2026-09-17.md),
[congestion scope](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md)
and the household diagnostic above. This table introduces no empirical effect size.]

Two principles preserve legitimate breadth. First, conditioning on school-year
effects or state-year effects can remove common capacity or political channels.
A conditional null cannot rule those out; the missing channel is still not proof
of harm. The relevant memos already disclose this. Second, a policy-created
constraint does not erase a cost. If cost is C(population, policy), changing
population under existing zoning or benefit rules is one legitimate comparison;
changing both population and policy is another. Their interaction makes a unique
allocation of moral blame impossible from that cost difference alone. Count the
conditional cost, then assess feasible adaptation separately. [DERIVATION / INFERENCE]

## What to change, and what to retain

Retain the conditional annual account and measured service/victim burdens. Correct
the amenity-zero and innovation-null assertions. Treat the preferences removal label as unsupported
without its allocation rule. Add a consistent public-pay scenario and a mixed-unit
benefit test before claiming that these interfaces are settled. Keep nonmonetized
institutional and amenity outcomes visible without assigning them arbitrary dollars.
[RECOMMENDATION]

The most useful presentation is an explicit account of what is priced, what is
conditional, and what remains unpriced, followed by coherent favorable and adverse
scenarios using the same beneficiaries and horizon. It should permit a reader to
reject a debatable extension while still seeing the costs supported independently.
These recommendations do not change the project's central question or analysis
protocol, and no new joint scenario was executed in this audit. [FRAMING-SENSITIVE]

## Verification, coverage and disconfirmation

- Three independent read-only passes covered fiscal/production accounting,
  demographic and household counterfactuals, and broader social channels. Their
  consequential claims were checked against current generators, outputs and
  source definitions. The [saved probes and instructions](../infra/immigration-fiscal/conceptual_audit_2026_09_28/README.md)
  preserve the reproducible new diagnostics; generated outputs are ignored.
- Rejected: P plus F is not itself a tax double count; the code conserves their
  partition. No new public-capital duplicate was established. The national deficit
  is not an automatic offset. Transfer status does not invalidate a loss to the
  chosen beneficiaries. A null or unpriced result does not establish zero harm.
- Existing qualifications on crime attribution, county fixed effects, lineage,
  ethnic identity and hedonic identification were reused rather than reported
  as newly discovered defects. Production-input, service-price and covariance
  issues remain in the September 27 audit; none was silently assumed repaired.
- External verification on September 28: searched National Academies fiscal-budget
  assumptions and NBER optimal-immigration/redistribution methods; read the relevant
  National Academies chapter-8 passages, chapter-6 introduction, and BEA's government
  consumption definition. The NBER 26154 abstract was located, but web access to its
  full PDF failed; it is not used as new substantive evidence in this memo.
- Skipped: no new crime, environmental or institutional causal estimation; no
  complete public/private sector model, household microsimulation or alternative
  demographic history; no new favorable aggregate. Active school-systemwide,
  enforcement/rent and world-ledger work was not treated as completed evidence.
  Restricted administrative validation and the earlier medical covariance gap
  remain outside this pass.
- Direction audit: payroll and household findings have unresolved net corrections;
  the preferences objection limits an adverse proposed add-on; the amenity repair
  restores the possibility of adverse effects and the innovation repair restores
  the source's unresolved benefit possibility. This is not a vote count on the
  overall sign. [EVIDENCE SYMMETRY]

This is LLM-assisted, politically sensitive research. The [instrument caveat](../notes/llm-bias-caveat.md)
applies to source selection and framing. Reproducible arithmetic establishes the
diagnostics; it does not validate the counterfactual or substitute for judgment.

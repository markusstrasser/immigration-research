# Conceptual audit: what the newer models still do not establish

Date: 2026-09-27. **Adversarial research memo.** Scope: the annual account and the
September 26–27 extensions, building on the
[September 25 audit](immigration-weekly-conceptual-audit-2026-09-25.md).
Starting HEAD `d0971a8`; the new annual case was committed as `f3031ab` during this
review. Its reported range is $321.8–387.4bn per year under its selected assumptions.
World-ledger and September 27 downstream propagation work remained in progress
when examined. Draft instructions below are not described as completed estimates.
[DATA: git history; [main-case result](../infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md)]

**Verdict:** Yes, there are consequential flaws. The strongest concern is that
different kinds of dollars and different counterfactuals are being passed between
otherwise careful calculations. An imputed capital return becomes a borrowing
requirement; a policy's return per net fiscal dollar becomes the recipient's value
per dollar spent; current schooling becomes selection before migration; and a
married-person percentage becomes a descendant birth-cohort percentage. Several
new results therefore need narrower conclusions or a different bridge. None of
the checks here establishes that the conditional annual-cost sign reverses.
[INFERENCE; evidence below]

The model's strength is explicit accounting and unusually extensive sensitivity
work. The weakness is that reproducing all component totals can validate a shared
assumption without testing whether the components answer the same question.
My research judgment is to prioritize the bridges below over adding more cost
categories. [INFERENCE / RECOMMENDATION]

The perspective of the existing headline is other US residents; the prospective
world account includes migrants and source-country residents. These are distinct
welfare objectives. This LLM-assisted audit is also an imperfect instrument: I
tested objections that would raise and lower the apparent cost, retained strong
rebuttals, and distinguish errors from choices the operator has deliberately made.
[FRAMING-SENSITIVE; [instrument note](../notes/llm-bias-caveat.md)]

| Priority | Finding | Status and consequence |
|---|---|---|
| Highest | Current-account/resource costs are not borrowing flows | Existing debt interpretation lacks a capital-account bridge; new capital-return propagation would deepen the problem |
| Highest | World brief substitutes MVPF for willingness to pay | Confirmed primary-source error in a proposed calculation |
| High | World components do not share a comparator | Provisional sum has overlapping wage endpoints and missing Mexico harm levels |
| High | Selection and nonlinear transmission conclusions exceed the measurements | Measured ranks survive; pre-migration and slope-asymmetry conclusions need narrowing |
| High | Identity attrition changes statistical unit | The 6–7% descendant-loss calculation and its cumulative-retention inference do not follow |
| Medium | Operations, infrastructure stock and congestion share an untested response | Coherent scenario possible; current sensitivities do not jointly vary the dependent terms |
| Smaller, confirmed | Internal public transfers fail subgroup conservation | Bias favors the group; actual exposure still needs source decomposition |

## 1. Keep resource cost, displaced benefits and borrowing separate

The new case adds **$33.80–55.69bn/year of imputed public-capital return**, producing
the difference between its $288.02–331.68bn engine result and $321.82–387.37bn total.
At its fixed low/high specifications, the federal portion of that return is
$0.827bn/$1.740bn; the remainder is state/local. These are modeled annual
opportunity costs at selected real rates, not observed additional payments.
[CALCULATION: [accounting probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_accounting.py),
reading `main_case_long_run_2026_09_27/derived/per_spec.csv`, specs 48/11]

**The strongest defense is correct:** capital tied up in schools, roads and utilities
has an opportunity cost. BEA explicitly explains that its general-government
consumption measure includes depreciation but omits a net return on assets.
Adding that return can improve a resource-cost account. It does not create a cash
payment or establish which households finance it. [SOURCE:
[BEA NIPA Handbook chapter 9](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf), pp. 9-2–9-4; INFERENCE]

But the [propagation brief](../infra/immigration-fiscal/sept27_propagation_2026_09_27/BRIEF.md)
places the return in direct fiscal response A and directs the debt and financing
consumers to include it. The existing [debt model](../infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py)
already carries responsive NIPA current spending into `programme_federal()` and
compounds the resulting flow in `stock()`. There is no conversion from depreciation
to gross investment and capital transactions before borrowing. The new return had
not yet been implemented in that consumer at review time. [DATA/CODE]

For a borrowing calculation the relevant national-account bridge is:

`net lending = current saving + depreciation + net capital transfers received
               − gross investment − net purchases of nonproduced assets`.

BEA distinguishes this financing requirement from current saving. In the repo's
pinned 2024 federal table, current saving is −$1,874.456bn and net lending is
−$2,106.222bn: a **$231.766bn national difference**. The probe reconstructs the
latter within source rounding. This is a diagnostic of the accounting basis,
**not a group correction**; the group's incremental capital flows are still
unidentified. [SOURCE: [BEA's explanation](https://apps.bea.gov/scb/issues/2026/01-january/0126-government-receipts-expenditures.htm);
DATA: pinned `Section3All_xls.xlsx`, `T30200-A`, lines 37, 42, 45–49; CALCULATION: accounting probe]

Stationary replacement investment could make depreciation approximate annual
investment. That assumption is insufficient for an actual 2005–2023 borrowing
history, and it still does not make an imputed return a payment. The
[school-capital lane](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md)
itself distinguishes cash and accrual costs and reports capital outlay exceeding
depreciation. The debt caller does not consume that bridge. The sign of a full
cash-basis repair is open: omitted net investment could raise financing needs while
removing imputations could lower them. [DATA/CODE; INFERENCE]

**Capped benefits reveal the same distinction from another direction.** The
propagation brief says rental-assistance and LIHEAP slots would pass to other
eligible households when group recipients are absent. Under that stipulated
counterfactual, spending stays fixed; other households lose benefits in the
with-group world. The annual welfare burden can still be real, but the budget
response is zero. At a dollar-for-dollar recipient valuation, reclassifying the
new $4.532bn rental line need not change aggregate incumbent welfare; it changes
who loses, whether taxes must change, and what can be accumulated into debt.
[DATA: brief, item 6; CALCULATION: accounting probe; INFERENCE]

**Needed:** retain separate cash-financing, resource-cost and displaced-beneficiary
columns. Reconcile actual/incremental investment and capital transfers before any
debt accumulation. For a fixed capped program, put the opportunity loss on the
excluded eligible recipients and price its value explicitly. This is not a proposal
to delete public capital or capped benefits from welfare. [RECOMMENDATION]

## 2. The world-ledger brief uses the wrong denominator from the welfare paper

The [world brief](../infra/immigration-fiscal/world_ledger_2026_09_27/BRIEF.md), section B,
labels ranges 0.65–1.04, negative through 1.20, and 0.40–1.63 as willingness to pay
per spending dollar. Hendren and Sprung-Keyser's published introduction labels
these **marginal values of public funds (MVPFs)**. Its denominator is net government
cost including fiscal feedback, not initial expenditure. The paper's food-stamp
valuation of 0.62 is a different object. [SOURCE:
[Hendren and Sprung-Keyser, QJE 2020](https://academic.oup.com/qje/article/135/3/1209/5781614), Abstract, introduction I.A and food-stamp discussion]

Let gross expenditure be G, additional fiscal cost be F, and recipient willingness
to pay be V. Then `MVPF = V/(G+F)` while the requested valuation multiplier is `V/G`.
In an illustrative cash transfer with G=1, V=1 and lost tax receipts F=0.25, the
MVPF is 0.8 although the recipient values the dollar at one dollar. Multiplying
spending by 0.8 and separately charging that fiscal feedback miscounts the same
mechanism. [DERIVATION; illustration, not an estimate]

The brief orders primary-paper verification and the result was still pending.
This is therefore a caught specification error, not evidence of an erroneous
completed world total. Preserve separate initial expenditure, recipient value,
third-party value, fiscal feedback and net cost before applying any ratio.
[DATA; RECOMMENDATION]

A related transport problem concerns Medicaid. Finkelstein, Hendren and Luttmer's
Oregon valuation model assigns substantial benefits to parties previously bearing
uncompensated care, not just insured recipients; about 60% of gross spending is
such transfers. Its reported recipient value of roughly 0.5–1.2 per dollar uses
**net** costs. A low patient valuation per gross dollar does not mean the remaining
dollars disappear from world welfare. Conversely, the provider transfer cannot
simply be added when the alternative is a patient absent from the US. The insured
versus uninsured treatment needs a bridge to US versus Mexico residence and to
the existing uncompensated-care lines. [SOURCE:
[Finkelstein, Hendren and Luttmer](https://pmc.ncbi.nlm.nih.gov/articles/PMC8081392/), framework and welfare analysis; INFERENCE]

## 3. A world sum requires the same alternative world on every row

The provisional approximately +$150bn world sum referenced by the brief is not a
completed repo result. Its starter arithmetic combines the first generation's
place premium with within-group wage effects and US in-group crime harm. The
source [winners/losers code](../infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py),
`group_frame()`, correctly presents these as separate diagnostics. The error arises
when they are summed. [DATA/CODE: brief's cited `scratchpad/placegain.md`, section 9;
`group_frame.csv` and `group_frame()`]

**Wages:** the place premium is calculated from actual US earnings, while the CES
diagnostic compares those earnings with hypothetical US earnings if group labor
were absent. Let these be `E_US`, `E_US*`, and Mexico earnings `E_MX`. A migration
gain is `E_US − E_MX`. Adding `E_US − E_US*` repeats part of the first generation's
equilibrium wage effect. A valid decomposition would instead be
`(E_US − E_US*) + (E_US* − E_MX)`. The US-born portions require their own comparator;
deleting the entire wage row does not by itself yield a corrected world estimate.
[DERIVATION; DATA/CODE: `group_frame()` observed `PEARNVAL` and subsequent wage rows]

**Crime and other welfare levels:** subtracting all US victim harm to migrants
without a Mexico counterpart implicitly uses zero harm abroad. The same issue
applies to schooling, health care, taxes and amenities. For a residence comparison,
the terms are differences between two worlds. National Mexico averages alone would
not establish the right counterfactual for the selected migrants. This omission
could move the result in either direction. [INFERENCE; DATA/CODE: in-group victim row]

**Descendants and time:** the brief proposes the same person born and raised in
Mexico. That can define a controlled rearing comparison. A historical no-migration
policy also changes parents' matching, fertility and who exists. Nonidentity does
not imply zero value for descendants; it requires an explicit population convention.
Likewise, today's pupils and today's adult G2 earners are different cohorts.
Excluding all schooling investment value because it appears in G2 earnings needs
an explicit stationary-flow argument, or a cohort model with future returns and
terminal human capital. [INFERENCE / FRAMING-SENSITIVE; DATA: brief sections A–B;
[annual-account comparison](immigration-complete-annual-account-2026-09-20.md)]

**Finite welfare changes:** even a chosen weighting needs the right mathematics.
Under illustrative log-income utility, an income ratio 2.46 implies a utility
change `log(2.46)=0.900`. Multiplying the income gain by inverse destination income
gives 0.593; inverse origin income gives 1.460. Neither endpoint approximation is
the finite log change. This is algebra, not measured migrant utility. A moral
weight is the operator's choice; the calculation must consistently implement it.
[DERIVATION / FRAMING-SENSITIVE]

**Needed:** before weighting, assign every row its beneficiary, initial state,
alternative state, time window, and quantity-versus-transfer status. Require
matching endpoints or a telescoping decomposition. A missing comparator remains
unknown rather than becoming zero. [RECOMMENDATION]

## 4. The selection curve measures some outcomes after the supposed selection

The [selection lane](../infra/immigration-fiscal/selection_curve_2026_09_27/RESULT.md)
and [trajectory synthesis](immigration-generational-trajectory-mexican-indian-2026-09-27.md)
infer that selection at home adds little once US position is known. But
`cps_curve.py` ranks **current US-observed education** against origin birth-cohort
education. It includes all foreign-born adults aged 25–64; the loaded arrival-year
variable does not restrict this calculation. Education completed after immigration
is therefore part of the supposed selection measure. [DATA/CODE:
[cps_curve.py](../infra/immigration-fiscal/selection_curve_2026_09_27/cps_curve.py),
G1 frame and `origin_selection_pct`]

The saved [generation probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_generations.py)
finds **25.20% definitely arrived before age 18** in the pooled G1 frame; grouped
dates and unknown arrival codes permit up to 33.54%. For Mexico the bounds are
26.74–38.40%; for India 10.14–13.32%. These are person-weighted shares of pooled
1994–2025 records, not unique people, regression-origin weights or confidence
intervals. The date uncertainty is propagated rather than replaced by midpoints.
[CALCULATION; DATA: pinned cached CPS frame and source DDI]

**Rebuttal:** these ranks validly describe how immigrants observed in the US compare
with origin peers. Their measured association is not invalidated. But they cannot
establish that **premigration** selection adds little, because the predictor
already contains outcomes of the destination environment. Even adult arrivals
can acquire further schooling. [INFERENCE]

The next discriminating comparison is arrivals definitely 25+ and, separately,
recent adult arrivals, with retained origin/sample coverage reported. Keep the
existing descriptive axis while narrowing its interpretation. The corrected slope's
direction is unknown. [RECOMMENDATION / GAP]

**The nonlinear-transmission claim also needs narrowing.** The lane says
“Nonlinearity: yes” from separately fitted below/above-median slopes. The actual
slope difference was not tested. A paired 10,000-draw origin bootstrap on exactly
its 78-origin sample and G2-count weights gives:

| Outcome | Below-minus-above slope | 95% origin-bootstrap interval |
|---|---:|---:|
| Education percentile | 0.374 | −0.114 to 0.829 |
| Earnings percentile | 0.466 | −0.419 to 1.269 |

These are diagnostics under the lane's own origin-resampling convention, not
survey-design or causal intervals. The point pattern survives; distinct
transmission rates remain uncertain. Failure to distinguish them does not prove
equal slopes. [CALCULATION: generation probe; DATA: `origin_curve.csv`, `n_g1 >= 100`]

## 5. Identity attrition is being inferred with the wrong denominator

The [civic result](../infra/immigration-fiscal/civic_trajectory_mexican_2026_09_27/RESULT.md),
child-identification section, multiplies roughly 40% G3+ outmarriage by 16%
non-Hispanic identification among mixed-couple children. It interprets the product
as 6–7% loss per descendant birth cohort and as support for cumulative G4+
identification of 0.888. The first percentage counts **Mexican-origin married
people**; the second counts **children**. An endogamous couple contributes two
origin spouses, while a mixed couple contributes one. [DATA/CODE:
[asec_intermarriage.py](../infra/immigration-fiscal/civic_trajectory_mexican_2026_09_27/asec_intermarriage.py),
spouse and child tabulations]

In a two-couple-type, equal-fertility illustration, person outmarriage q=0.402
implies a mixed-couple fraction `2q/(1+q)=0.5735`. With the lane's Hispanic child
retention of 0.843675, loss would be 8.96%, versus the naive 6.28%. **Neither is a
new empirical estimate**: actual fertility, generation-mixed pairs and child
weights matter. The example disproves the proposed conversion. [CALCULATION:
generation probe]

Two further boundaries matter. Mexican and Hispanic identification are different:
the lane's children of Mexican × other-Hispanic couples are 97.2% Hispanic but only
55.0% Mexican. And descendants whose parents already ceased identifying are
outside the identifying-parent frame. Current child-stage retention cannot validate
cumulative lineage retention or bound its outcome bias. Labeling the multiplication
rough does not fix either issue. [DATA: civic result; INFERENCE]

**Needed:** retain the observed spouse/child tables; withdraw the 6–7% cohort
interpretation and its validation of 0.888. Tabulate directly on unique weighted
children, with both parents' known generation and separate Mexican/Hispanic
outcomes. Deeper unidentified lineage remains a gap, not proof that its outcomes
equal those of whites. [RECOMMENDATION]

## 6. Road operations, capital stock and physical capacity need a joint scenario

The source scaling regressions measure state highway/park **current operations**
against population. The newer models apply those responses to consumption
including depreciation, capital stocks' opportunity return, and physical highway
lanes used for congestion. These are different quantities. Fewer residents can
reduce maintenance and labor without removing lanes; a smaller network can also
change route length and access. [DATA/CODE:
[state regression](../infra/immigration-fiscal/scaling_test_2026_09_20/state_analyze.py),
[congestion bridge](../infra/immigration-fiscal/service_response_long_run_2026_09_27/congestion.py);
INFERENCE]

The [capital result](../infra/immigration-fiscal/capital_return_services_2026_09_27/RESULT.md)
explicitly admits that if physical capital stays fixed, its depreciation and return
would not be saved. Yet the congestion sensitivity varying network adjustment
leaves the fiscal move fixed. It is therefore a congestion sensitivity, not a
coherent bound on the combined fiscal-and-traffic scenario. The road/park capital
block is $6.18/$12.47bn at the two ends; the change to congestion from network
shrinkage is −$5.17/−$7.14bn. These are dependent assumptions, not independent
additive error bars. [DATA: capital result and service `derived/net_change.json`]

**Rebuttal:** a stationary smaller economy could coherently have a smaller public
capital stock. This is a valid declared scenario. The state operations regression
does not estimate that physical stock response. Recompute operations, depreciation,
return, capacity and congestion jointly under fixed-stock, replacement-adjustment
and smaller-stationary-network cases. [INFERENCE / RECOMMENDATION]

There is also a narrower workload ambiguity. For `C(N)=aN^b`, a population removal
share s implies `C[1−(1−s)^b]`. The highway code uses this response factor at
s=12.02%, then applies it to a resource key k=8.06%. The probe reproduces $11.977bn
for that hybrid, $17.866bn for the population law, or $11.908bn if resources are
the workload variable throughout. **The $5.889bn gap is an alternative model,
not a correction.** Heterogeneous use can justify a hybrid, but it needs its own
workload assumption. The small finite-form discrepancy is less important than
which demand variable is appropriate. [CALCULATION:
[fiscal probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_fiscal.cjs)]

## 7. Internal transfers should not change a consolidated group's cost

The new case charges a federal housing subsidy at a housing-support key while
crediting it inside government-enterprise surplus at a population key. The result
already acknowledges the mismatch. A new test adds a synthetic $1bn to both
public-sector legs on a cloned model, with no new resources or services and capital
disabled. The attributed cost falls by **$40.75–43.19 million**, depending on the
fill-in method. The national balance does not change. [CALCULATION: fiscal probe;
DATA/CODE: main-case result, housing-overlap section, and package receipt re-key]

This is a confirmed conservation failure favoring the target group. Its actual
size is not the synthetic $1bn exposure and was not established here. Consolidate
the internal transfer before assigning keys, or use one attributed amount on both
legs. Do not change the entire enterprise key to housing support. [INFERENCE /
RECOMMENDATION]

The objection that all capital returns should be reduced again for user-fee
financing fails: the account already credits the fees through net consumption or
enterprise surplus. Internal-transfer conservation and subtracting fees twice are
different issues. [SOURCE: BEA chapter 9 above; DATA: capital/main-case definitions]

## Additional checks worth keeping distinct

- **IR-5 eligibility clocks:** `late_arrival_tail_2026_09_27/per_admission.py`
  describes five years of continuous LPR residence and bars Medicare during the
  first five modeled years. SSA specifies that the relevant five years of
  continuous US residence need not all be in LPR status. The new-entrant scenario
  can still be appropriate; reusing its clock for a long-resident adjuster can
  delay eligibility incorrectly. Separate arrival, qualifying residence, LPR date,
  work credits and program rules. No NPV correction is estimated here.
  [SOURCE: [SSA POMS GN 00303.800, A.3–4](https://secure.ssa.gov/apps10/poms.Nsf/lnx/0200303800);
  DATA/CODE: [per_admission.py](../infra/immigration-fiscal/late_arrival_tail_2026_09_27/per_admission.py)]
- **Fraud versus birth cohorts:** the active lane is a design, not a completed
  inference. A 21-year-lagged birth pattern can explain admissions' scale while
  fraud coexists; a residual can reflect processing, policy, sibling structure or
  timing. It cannot identify a fraud rate without an independently observed fraud
  mechanism or audit denominator. [INFERENCE; DATA:
  [brief](../infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/BRIEF.md)]
- **The missing decision comparator:** the stock-absence account does not rank
  admitting a future worker, admitting that worker with possible later parents,
  retaining a long-resident adjuster, and replacing an admission with another
  applicant. A parent channel should enter through its conditional probability,
  timing and incremental effect relative to that parent's actual alternative.
  Negative aggregate stock accounting alone cannot choose among those policies.
  This is an unbuilt decision model, not a newly discovered arithmetic defect.
  [INFERENCE / RECOMMENDATION; DATA: annual-account scope and recent IR-5 adjustment revision]

## What survives, what is missing, and where effort should go

**Retained:** the annual account's stated incumbent perspective; observed generation
means and the broad within-sample Indian advantage; the descriptive origin ranks;
the usefulness of public-capital opportunity cost; and the production account's
existing private-income/induced-tax identity. Generation cross-sections being
different from linked families, small Indian G3 samples, the earlier adjustment
versus arrival issue, and the general conditional nature of service responses
are already disclosed. They are not new discoveries of this audit. [DATA:
linked results, current trajectory synthesis, September 25 audit and revisions]

**Correct or narrow:** borrowing interpretations lacking a financing bridge; MVPF
as a valuation multiplier; summing incompatible world-ledger endpoints;
premigration-selection language; established nonlinear transmission; descendant
attrition from the spouse-share multiplication; internal-transfer attribution;
and LPR-tenure wording where used as the Medicare residence clock. [INFERENCE]

**Unresolved:** a revised debt number, a complete world-welfare sign, cumulative
unobserved-lineage outcomes, physical public-capital adjustment, and future-policy
rankings. The completed checks identify neither a sign reversal nor a defensible
replacement headline. [GAP]

My priority is: first distinguish fiscal cash flows from welfare costs, correct
the world-paper denominator, and enforce one comparator across world rows. Then
run the child-denominator and adult-arrival comparisons, and build a joint public
capacity scenario. Only after those should the additional precision propagate
into lifetime totals, winner counts or normative break-even weights. [RECOMMENDATION]

The recurring blind spot is a change of object at a handoff: resources to cash,
net cost to gross outlay, outcomes to selection, spouses to children, marginal
estimates to a large population change. A durable check would record the object
being handed over and test one conservation law or falsifiable bridge, alongside
the existing numerical replay. Adoption of a changed research protocol is left to
the operator; this memo does not modify it. [INFERENCE / RECOMMENDATION]

## Verification and coverage

Evidence symmetry: the audited set contains adverse incumbent-cost estimates,
favorable migrant place gains, and mixed generation comparisons. The transfer
conservation repair raises attributed costs; the borrowing-basis repair has no
established direction; the world endpoint corrections require generation-specific
recalculation; the slope and lineage findings reduce certainty rather
than identify a fiscal sign. There is no defensible vote-count of these heterogeneous
findings as evidence for or against immigration. [INFERENCE]

Three independent lanes covered fiscal responses/enterprises, generation/IR-5,
and world welfare. The parent read their evidence and disputed or narrowed
findings before synthesis. Every executed diagnostic is preserved in the
[probe directory](../infra/immigration-fiscal/conceptual_audit_2026_09_27/README.md).
The audit's code changes are confined to those read-only diagnostics; the audited
models and concurrent peer work were not changed.

Primary external checks on September 27: BEA chapter 9 and its saving/borrowing
explanation; Hendren–Sprung-Keyser publisher text (definition, reported ratios and
food stamps); Finkelstein–Hendren–Luttmer full author text (framework, transfers and
denominators); SSA's residence rule. Search focused on the exact BEA accounting
identity; the other known source URLs were opened directly. No secondary web
summary substitutes for these definitions. The HSK and Medicaid excerpts were
verified in HTML because cached PDF body extraction was unreliable.

Coverage limitations: no full re-estimation of raw fiscal microdata, no source-country
income/crime acquisition, no corrected child-level attrition estimate, no rewritten
public-capital model, and no exhaustive re-audit of the already-reviewed crime,
voting or ancestry-IV literature. Those omissions limit numerical corrections and
new causal claims; they do not prevent the bounded findings above. The existing
September 25 revisions were read to avoid relabeling completed corrections as new
flaws. Active drafts are dated evidence, not a frozen release certification.

# Conceptual audit: what the newer models still do not establish

Date: 2026-09-27. **Adversarial research memo.** Scope: the annual account and the
September 26–27 extensions, building on the
[September 25 audit](immigration-weekly-conceptual-audit-2026-09-25.md).
Starting HEAD `d0971a8`; the new annual case was committed as `f3031ab` during this
review. Its reported range is $321.8–387.4bn per year under its selected assumptions.
World-ledger and September 27 downstream propagation work remained in progress
when examined. Draft instructions below are not described as completed estimates.
[DATA: git history; [main-case result](../infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md)]

**Later September 27:** the [expanded audit below](#second-pass-inputs-production-uncertainty-and-demography)
covers the areas left open in the first pass. Some initial findings have since been
corrected; the revision record distinguishes those repairs from outstanding work.

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

## Second pass: inputs, production, uncertainty and demography

**Verdict:** Three further interpretations need correction: an incomplete sampling
error is not necessarily a lower bound; the service-price calculation does not
establish numerical inclusion in the production benefit; and the sponsored-parent
calibration does not identify a lifetime sponsorship probability. A small lineage
survival inconsistency is also confirmed. Tax/benefit construction survived the
checks without a new consequential defect. A disclosed production-input omission
is larger than its earlier proportional approximation suggested, but still small
relative to the annual account. [INFERENCE; diagnostics below]

This pass began at `27859e1`, after the sponsored-parent outputs were committed.
It keeps the September 27 annual account, September 26 sampling calculation and
September 19 lineage ledger separate. Their dollars and denominators do not form
one correction to the headline. [DATA / FRAMING-SENSITIVE]

### A. Missing covariance need not increase uncertainty

The earlier propagation result says to read its roughly $10.9bn sampling standard
error as a floor because correction uncertainties are omitted. But one omitted
correction is calculated from the **same 160 CPS replicate weights** as the account.
Its covariance is recoverable. The
[uncertainty probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_uncertainty.py)
reproduces all ten central administrative-benefit corrections and their SEs, and
all 64 published September 26 schools-case CPS SEs, within `1e-8bn`.
[DATA/CODE: [propagation](../infra/immigration-fiscal/uncertainty_propagation_2026_09_22/propagate.py),
`adopted_cases`; [benefit producer](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/compare.py),
`rekey`, `main`; [floor claim](../infra/immigration-fiscal/sept24_propagation_2026_09_24/RESULT.md), uncertainty section]

Hold administrative inputs, ACS shares, other corrections and model choices fixed.
Vary the central benefit-rekeying factor alongside the corresponding account
replicate. The new signed deviation is added to the existing receipts-minus-spending
deviation before calculating variance:

`Var(account + correction) = Var(account) + Var(correction) + 2 Cov(account, correction)`.

| September 26 schools case; sampling diagnostic, $bn unless stated | Result across 64 specifications |
|---|---:|
| Published CPS SE | 8.950–9.059 |
| Benefit-factor/account covariance, bn² | −4.215 to −4.129 |
| Correlation | −0.422 to −0.398 |
| Joint first-order CPS SE | 8.541–8.665 |
| Joint CPS SE including the factor-product interaction | 8.545–8.670 |
| Published combined SE with benefits appended separately | 10.990–11.092 |
| Combined SE replacing only that block with joint covariance | 10.597–10.709 |

[CALCULATION: uncertainty probe; the last row retains the other published source
variances and independence assumptions. Point estimates do not change.]

The strongest defense is that the method discloses missing sources and already
has a perfect-positive-correlation stress. That remains useful. It does not prove
a lower bound: omitted dependent terms can reduce variance, and an envelope over
represented source SEs does not restore an omitted within-source relationship.
Call the result a **partial sampling approximation whose net error is unresolved**.
These diagnostic SEs are not replacement headline intervals. [INFERENCE]

The medical bridge is a related, unresolved case. The corrected key uses an
estimated pooled ethnic ratio, with 2024 donors overlapping the old donor base.
Scaling the old gradient by the corrected dollar level omits the derivative of
that ratio and its covariance with the base. The pooled translator already has
joint influence vectors: its five-line p99.5 correction has an $8.039bn SE before
LTSS and package scaling. Adding that SE independently would also be wrong.
Model-specification ranges do not substitute for its sampling distribution.
[DATA/CODE: [pooled translator](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/translate.py),
`main`, lines 278–311; [translation table](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/derived/translation_account.csv)]

At this pass's inspection, the September 27 uncertainty extension was still
pending. This finding concerns the executed September 24/26 bridge and what its
successor must handle; it is not a claim that an unfinished September 27 run has
published an incorrect interval. [DATA: `later_cases.json` and the propagation lane's pending-work record]

### B. Similar benefit totals do not establish overlap

The household-services lane says its $21.84bn gross consumer-price benefit,
$11.94bn after netting native dropout wage gains, is already inside the production
term. Its numerical check compares $11.94bn with $8.8–13.3bn. Two bridges fail:

1. `hours_tax.py` changes the immigration shock to the Mexican-origin union but
   retains **consumer units scaled by the native-householder share and all native
   dropout earnings**. The wage base includes US-born target members and excludes
   other foreign-born workers. Native-headed consumer units can contain mixed-nativity
   households; their expenditure base is not the main account's set of remaining
   persons, which excludes the whole target and includes everyone else.
2. $8.8–13.3bn is **private welfare plus induced receipts, P+F**. On these fixed-hours,
   full-capital-adjustment specifications, P alone is about −$0.16/−$0.24bn under
   cash/GDP normalization. Falling within the P+F range is not a decomposition of
   either P or P+F, particularly across two different models.

[DATA/CODE: [service producer](../infra/immigration-fiscal/care_household_services_2026_09_23/hours_tax.py),
lines 314–341; [overlap ruling](../infra/immigration-fiscal/care_household_services_2026_09_23/RESULT.md),
Part A and overlap item 1; CALCULATION:
[production probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_production.py), published baseline]

**The no-add decision remains defensible.** Both exercises capture consequences
of labor supply, so blindly adding them could double-count. But “overlapping
alternative calculation, not reconciled” is supported; “these exact benefits are
already included” is not. Correct the beneficiaries, identify the producer losses
and tax effects, and reconcile a sector-price calculation to aggregate welfare
before declaring either an additional gain or exact containment. This audit does
not add $21.84bn or $11.94bn to the account. [INFERENCE / RECOMMENDATION]

The construction-price calculation has a stronger connection: its input costs
come from the same factor-wage changes. Treating that price effect as a view of
the production model is reasonable. That does not validate the distinct empirical
household-services calculation. [DATA/CODE:
[construction lane](../infra/immigration-fiscal/construction_housing_supply_2026_09_23/RESULT.md);
INFERENCE]

### C. A known production-input omission is now quantified

The adopted tax package reweights Mexico-born people outside California and Texas
to ACS targets, but its production inputs retain the old CPS earnings composition.
The source explicitly discloses this omission and approximates its size by scaling
the production gain proportionately with a wage-key change. The CES gain depends
on skill composition, so that shortcut is unreliable.
[DATA: [CPS correction result](../infra/immigration-fiscal/cps_imputation_keys_2026_09_23/RESULT.md),
limitations and unfinished items; CODE: current production import chain]

Recalibrating the same two-skill CES with the **already adopted population weights**
changes P+F from $8.791/$13.323bn to $7.683/$11.680bn under cash/GDP normalization.
Holding every other account component fixed, that raises incumbent cost by
**$1.107/$1.643bn**, versus the earlier rough $0.2–0.3bn approximation. With the five
existing matched hot-deck seeds on those weights, the corresponding mean P+F is
$7.861/$11.931bn. The latter is a sensitivity construction, not an adopted replacement
estimator; seed spread is not a survey confidence interval.
[CALCULATION: production probe; income year 2024, fixed hours, full private-capital adjustment,
sigma 2, labor share 0.65; no national re-raking after the adopted row-4 reweight]

This is **disclosed unfinished propagation, not a newly hidden defect**. The core
production equations correctly subtract the opportunity income of released private
capital and make ownership and fiscal recycling explicit. No new defect in those
identities was established. Public-capital consistency remains the separate issue
in section 6. [DATA/CODE:
[production model](../infra/immigration-fiscal/matched_benefits_2026_09_19/model.py); INFERENCE]

### D. Sponsored-parent calibration is a scenario, not an observed lifetime rate

The new lane's conclusion invokes the rate at which Mexican citizens actually
petition. Its 0.619 naturalization probability is calculated as today's naturalized
stock divided by that stock plus today's eligible LPR stock. This is a cross-sectional
share. It does not identify the probability that a newly admitted 25-year-old will
ever naturalize, nor the distribution of waiting times. Yet the model gives that
probability to each founder and puts naturalization five years after LPR status,
with parent admission one year later.
[DATA/CODE: [naturalization-share definition](../infra/immigration-fiscal/origin_attachment_mexico_2026_09_27/naturalization_share.py);
[sponsorship arms](../infra/immigration-fiscal/lineage_sponsored_parents_2026_09_27/arms.py),
`NAT_RATE`, `tracks`, `run_track`]

The official report already cached for calibration reports median LPR duration
before naturalization of seven years across all origins and nine for North America
in FY2024. Those are conditional on naturalizing, not replacement Mexico-specific
cohort probabilities. They nevertheless show why first-eligibility timing needs
its own justification. [SOURCE: [OHSS FY2024 report, Table 8](https://ohss.dhs.gov/topics/immigration/naturalizations/annual-flow-report/fy-24-naturalizations-flow-report),
verified in the lane's cached primary HTML; live retrieval returned 403]

The lifetime parent-admission probability is a second bridge. The code correctly
labels IR-5 admissions divided by newly eligible citizens a **steady-state flow
ratio**, with an untested equal-hazard assumption across native and naturalized
petitioners. The second estimator is not independent validation. Algebraically:

`stock estimate / flow estimate = assumed parent exposure years / (eligible stock / eligible inflow)`.

The admissions numerator cancels. Its reported agreement within 10% amounts to
24.359 parent-life years divided by a 22.375-year stock/inflow ratio: **1.089**.
That is a useful internal scale check, not evidence that either statistic identifies
the new founder's lifetime risk. [CALCULATION:
[sponsorship probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_sponsorship.py);
DATA: `derived/calibration.csv` in the sponsorship lane]

The timing matters even holding both probability parameters fixed. Delay admission
from founder-year 6 to year 10 or 16, age the parent from 60 to 64 or 70, and retain
the lane's survival and pricing rules: the added fiscal cost (absolute channel magnitude) falls from
$24,518 to $21,955 or $15,664 undiscounted, and from $12,138 to $10,717 or $7,046 at
3%, per original founder. These are **conditional sensitivities**, not estimated
corrections; delayed naturalization could also change petition probability, which
this probe holds fixed. [CALCULATION: sponsorship probe]

The lane already discloses equal hazards, recent-flow instability and later-age
arms. Its calibrated channel can remain small under those assumptions. Narrow the
opening conclusion accordingly. Estimating the actual channel requires linked or
cohort-specific naturalization and petition hazards, parent age/survival, sibling
sharing, adjustment versus new entry and return migration. The apparent precision
of 1.9% does not identify those transitions. [INFERENCE / RECOMMENDATION]

### E. Survival prices descendants but does not limit their births

`lineage.py` multiplies each generation's count by TFR/2, then survival-weights
that generation's fiscal life. It never requires the parent to survive until the
model's single childbearing age, 29. Halving survival at age 29 in a diagnostic
leaves every subsequent birth count unchanged. The fertility inputs are period
rates or ratios among living women; they do not already include the missing
parental cohort survival. [CODE/DATA:
[lineage recurrence](../infra/immigration-fiscal/lineage_cost_2026_09_19/lineage.py), `lineage`;
[fertility construction](../infra/immigration-fiscal/lineage_cost_2026_09_19/inputs.py), `fertility`;
CALCULATION: sponsorship probe]

Within the existing point-birth/common-life-table convention, multiply first births
by survival from founder age 25 to 29, and later births by survival from birth to
29. Those factors are 0.99596 and 0.98143. On the original central lineage case,
this moves the Mexican-minus-white gap from −$1,297,150 to −$1,288,162 undiscounted
and from −$514,635 to −$513,398 at 3%: **$8,988 and $1,237**, respectively. It reduces
the modeled adverse gap by about 0.7% and 0.2%, with no sign change. This is a small
internal inconsistency, not a challenge to the whole result. [CALCULATION]

The broader demographic omissions are already stated: period rather than cohort
profiles, no emigration, fixed fertility/convergence rules, and century-end
truncation. A joint model would also condition eligibility and later transitions
on actual residence and earnings histories. Those are outstanding modeling choices;
this audit has not estimated their combined direction. [DATA: lineage README,
limits; sponsored-parent RESULT, omitted work; INFERENCE]

### F. Checks that did not produce a new consequential flaw

The tax/benefit pass traced raw receipt and spending keys, shared versus personal
allocation, administrative scaling, status/imputation corrections and pooled MEPS
transport through the September 24 package into September 27. Prior nonrefundable-
credit, premium-tax-credit, Medicare-key and LTSS problems are not newly discovered
live defects. Unequal-person-weight allocation already has separate fixed-budget
sensitivity work. Matching and administrative raking still do not identify the
unobserved incomes or exact subgroup service use. [DATA/CODE: full-account builders;
dataset-integrity audit; September 24 package and CPS correction result]

One tested medical interaction was small: recomputing the ethnic ratio after the
adopted age/nativity composition change moves the five gross medical corrections
by a net **+$0.062bn before LTSS**, with individual signs mixed. This is not a final
account correction. The larger public-health-services payer proxy is already
declared and accompanied by alternatives; this pass did not identify its net bias.
[CALCULATION:
[medical-composition probe](../infra/immigration-fiscal/conceptual_audit_2026_09_27/probe_medical_composition.py);
DATA: spending contract and pooled-medical translation]

The fresh crime check read the current incident/victim-price construction, ethnic
and victim-group bridges, and detention boundary. It retains the explicit
limitations: Hispanic-to-Mexican allocation is a proxy, replacement offending is
not modeled, and victim prices are not budget payments. The newer lane already
removes criminal-justice costs and the nonfatal homicide-risk double count. No new
material defect was established in that bounded review. Housing's causal estimates
remain qualified by the September 25 instrument audit; the price/production overlap
was inspected here, without a new causal re-estimation.
[DATA/CODE: [victim-cost lane](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md)
and `victim_cost.py`; [custody boundary](immigration-detention-crime-and-fiscal-scope-2026-09-20.md);
[detention reconciliation](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md);
construction and housing-transfer lanes]

### What remains unexamined after this pass

This is now a broader audit, not an exhaustive certification. It has not validated
tax imputations against restricted administrative microdata, jointly re-estimated
all correction errors, built an endogenous demographic projection, or repeated
the crime/housing literature and raw-data acquisition. The medical joint derivative,
policy-specific counterfactual and coherent public-capacity path remain substantive
open work. No checked discrepancy supplies a defensible replacement annual headline.
[COVERAGE / GAP]

The additional checks have mixed directions: updated production inputs raise the
annual cost, survival reduces the adverse lineage gap, and joint CPS covariance
narrows the tested sampling component. The service and sponsorship bridges have
no identified net correction. These are different estimands, not quantities to
add or votes on a policy conclusion. [EVIDENCE SYMMETRY]

My priority remains a coherent set of connected estimates: the same population,
beneficiaries, history and covariance must survive each handoff. More detailed
subgroup output is useful only to the extent those connections hold. For the next
correction round, the recoverable CPS covariance and production reweight are
concrete; the service-price bridge and sponsorship hazards need narrower claims
until their different objects are reconciled. [RECOMMENDATION]

## Revisions

- 2026-09-27, second pass: extended coverage at the operator's request. Added
  uncertainty, benefit-boundary and sponsorship-calibration findings, a small
  survival recurrence diagnostic, and negative results on input construction.
  The four additional probes reproduce their baselines before changing an input.
- 2026-09-27, repairs observed during the follow-up: commit `2104b9e` corrected the
  world/propagation briefs' MVPF, comparator and noncash-debt instructions;
  `b222e28` records the Medicare residence-clock qualification; `1fd0ce2`, `d75963b`
  and `bb3de6f` execute and integrate the arrival-age, slope and child-denominator
  corrections. `d26a737` records internal-transfer repair as deferred, and
  `05db980` briefs further identity-loss propagation. These narrow the live
  issues in the first-pass snapshot; a corrected instruction or brief is not
  verification of every downstream consumer. [DATA: verified git history;
  [earlier adoption decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)]

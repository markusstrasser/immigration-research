# Remaining adults' work around household departures in SIPP

**Verdict:** The validated records show small average changes in employment and
weekly job hours over the first three months after an adult co-resident leaves.
Earnings do not show a stable common response across the two observable kinds
of departure. This is useful descriptive evidence about selected household
separations; it does not identify the work response to deportation or justify
changing v9. Failure to establish a change is not proof of no change.
[CALCULATION; INFERENCE: linked outputs below]

This follows the [raw-study and data audit](immigration-v9-household-departure-evidence-2026-10-16.md).
The single link is the departing member's absence → **the same remaining adult's
own employment, hours and earnings**. The departing person's lost income is not
included. No household-income total or fiscal total is estimated here.

## What the records support

We used the public **2025 SIPP release, reference year 2024**, and its original
schema, dictionary and guide. The primary cohort requires three months of
co-residence, a valid split at month t, and a focal adult aged 18–64 just before
the split who remains at the previous address at t. Later focal moves and
returns remain in the primary cohort. Simultaneous departures count once for
each remaining adult; only that adult's first eligible event is used.
[SOURCE: [Census guide](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2025_SIPP_Users_Guide.pdf),
pp.19–21, 33–41; CALCULATION:
[protocol](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/protocol.md),
[event checks](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/event_audit.json)]

- **Both adults individually tracked:** 149 remaining adults in 78 original
  sample units pass the event rules. Every departing-person pair also matches
  the residence-spell boundary and disappearance from the focal adult's
  relationship-ID roster. There are 181 directed pairs because some adults lose
  more than one co-resident. After outcome availability, employment/earnings use
  147 adults; hours use 146. [CALCULATION]
- **Proxy-roster departures (“Type-2”):** 278 remaining adults in 145 sample units
  pass the separate within-year identity-set rules; 277 have complete outcomes.
  The person who left has no independent interviewed-person record. Stable
  within-focal age/sex and fixed Type-2 identifiers corroborate these histories,
  but destination, reason and cross-focal identity are not independently known.
  These are a separate sample, not extra observations to pool with tracked exits.
  [SOURCE; CALCULATION]

The earlier 214-person screen was deliberately looser. Calendar-window,
prior-co-residence and universe checks narrow it. One additionally eligible
adult turns 65 in the departure month; the declared **baseline-age** rule
correctly retains him/her. An independent reconstruction reconciled the final
event keys and every pair-level validation flag. This is internal survey-record
validation, not external confirmation of addresses or interview answers.
[CALCULATION: [independent event audit](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/event_validation.md)]

## How work changed

Each entry compares that same person's **average in t−3…t−1** with their
**average in t…t+2**, including nonworkers. These windows restrict events to
April–October 2024. The following are unweighted means of individual changes;
brackets are **95% original-sample-unit cluster-bootstrap intervals**. They
describe the selected observed cohorts, not all U.S. departures. [CALCULATION]

| Outcome | Both adults tracked | Proxy-roster departure |
|---|---:|---:|
| Employed at any point in the month | **−0.91 pp** [−3.60, +1.72]; 73.02% → 72.11% | **−0.96 pp** [−3.22, +1.30]; 78.58% → 77.62% |
| Average weekly job hours | **+0.26 h** [−1.04, +1.77]; 29.75 → 30.02 | **−0.65 h** [−1.79, +0.41]; 30.39 → 29.74 |
| Personal monthly earnings/profits | **+$784** [−$29, +$1,929]; $6,545 → $7,330 | **−$87** [−$273, +$100]; $5,618 → $5,531 |

[CALCULATION: [all estimates and sensitivities](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/changes.csv),
[outcome availability](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/attrition.csv).
Employment is a probability, so changes are percentage points, not percent.
Earnings are nominal 2024 dollars, using Census's equal-month-length
`TPEARN_ALT`; they include profits/losses and are not take-home income.]

The [six monthly means](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/monthly.csv)
and [trajectory figure](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/trajectories.png)
show the timing within these windows. [CALCULATION]

Most adults show no recorded change between the two three-month averages:
**141/147** tracked adults have unchanged employment, **123/146** unchanged
hours and **103/147** unchanged earnings. In the proxy-roster sample the counts
are **255/277**, **210/277** and **176/277**. The median change is zero for each
outcome in both cohorts. SIPP derives these monthly records from retrospective
work-spell reports, with limited reported changes within a spell; this flatness
must not be mistaken for payroll-level evidence that every small adjustment was
absent. [CALCULATION: [distributions](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/distributions.csv);
SOURCE: Census guide pp.70–74]

The tracked earnings result needs particular restraint. Its immediate
t−1→t change is **−$41** [−$344, +$181], whereas its three-month-average change
is positive. With fully reported residence IDs **and spell boundaries**, the
mean becomes **+$115** [−$180, +$407] among 60 adults. This changes the sample,
not merely the precision. Removing records with allocated visible earnings
components does not eliminate the positive mean (+$1,275 [−$94, +$3,110],
83 adults). There is no single robust earnings coefficient to select from
these constructions. The full-cohort estimates remain the principal results;
no favorable trim replaces them. [CALCULATION: changes/distributions above]

Three adults with the largest absolute earnings changes contribute **+$709**
of the full sample's **+$784** mean increase. This post hoc influence check
helps explain the instability; it does not remove those observations.
[CALCULATION: [influence diagnostics](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/influence.json)]

December survey weights give tracked changes of **−0.93 pp** [−3.77, +1.91],
**+0.30 h** [−1.09, +1.68], and **+$739** [−$217, +$1,694]. The proxy-roster
figures are **−0.67 pp** [−2.74, +1.39], **−0.44 h** [−1.67, +0.79], and
**−$223** [−$646, +$200]. These intervals use all 240 official December
replicates and Fay BRR, k=.5. Weights do not repair selection into observed
departures or complete follow-up. [CALCULATION: changes.csv; SOURCE: guide
pp.153–160; [weight receipt](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/replicate_receipt.json)]

## Ordinary change and population limits

A same-calendar-month benchmark uses adults with stable prior co-residence and
no recorded adult loss at t. It standardizes by month, sex, broad age and prior
employment; a second version also uses children present. Future departures and
later focal moves do not exclude controls. All principal event adults find
supported comparison strata. [CALCULATION:
[benchmark and pre-trend checks](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/benchmark.csv)]

Relative to this benchmark, tracked adults change employment by **−0.88 pp**
[−3.68, +1.90] and hours by **+0.35** [−1.05, +1.89]; the proxy-roster changes
are **−0.84 pp** [−3.09, +1.21] and **−0.62 hours** [−1.65, +0.44]. Tracked
earnings show a positive contrast, **+$862** [+$31, +$2,075]; adding children to
the standardization gives +$875 [+$51, +$2,074]. The proxy-roster earnings
contrast is −$77 [−$266, +$99]. The positive tracked contrast is retained, not
dismissed because it runs against a preferred story. It is an observational,
tail-sensitive earnings difference; neither matching nor its interval makes
the household exit exogenous. These benchmark intervals use 1,999 Poisson
original-sample-unit bootstrap draws, retaining shared event/control clusters.
Before departure, the tracked earnings change relative to this benchmark is
+$170 [−$69, +$505], and the proxy-roster hours contrast is −0.54 h
[−1.32, +0.17]. These pre-trends do not establish parallel counterfactual paths.
[CALCULATION; INFERENCE: benchmark.csv, `pre_trend` rows]

This sample also poorly represents a spouse's removal. There are only **seven**
tracked and **21** proxy-roster spouse/partner departures. Their hours changes
are +2.14 [0, +6.43] and −1.78 [−6.30, +2.46], respectively. Such small
subgroups give weak uncertainty estimates; an interval collapsing to zero for
an unchanged tiny cell is not evidence of known zero population variation.
Most tracked pairs carry the released code “other nonrelative”; that constructed
code does not establish that they were roommates. Younger departing adults and
older remaining adults are common. [CALCULATION; SOURCE: event_validation.md]

Tracked movers have observed domestic destinations. Type-2 destinations and
departure reasons are unavailable. Voluntary moves, relationship changes,
school, work and housing pressures can jointly determine departure and work.
The findings therefore leave the deportation/forced-loss and full-lineage
counterfactual bridges unresolved. [SOURCE; INFERENCE]

## Measurement and checks

Employment includes partial-month jobs (`RMESR=1…5`) and qualifying unpaid
family work. Numeric hours and earnings, including zero and negative profits,
are retained. Missing values become zero only under the documented no-job and
earnings-variable-universe rules while the person remains in the survey
universe; explicit unpaid family workers can have zero
earnings but unknown hours. Other employed/missing records remain missing.
[SOURCE: [definitions](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/definitions.md);
CALCULATION: [coding receipt](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/derived/outcome_coding.json)]

The aggregate allocation flags are all recode flag 9 where numeric, so they
cannot select “reported” outcomes directly. We inspected 393 available raw
component flags and report separate visible-component sensitivities. These do
not certify undisclosed job components. The complete output also retains sex,
children, partner/other, prior departing-worker status, persistence, common
outcome cohorts, calendar-month earnings and unpaid-zero sensitivities. No
computed specification is silently selected as the answer. [CALCULATION]

An independent analyst reproduced all eight unweighted principal summaries and
all eight December-weighted summaries, including the replicate-weight
intervals, without importing the analysis implementation. Synthetic tests cover
whole-household moves, simultaneous departures, subsequent focal moves,
baseline-age birthdays, zero/missing rules and family-level resampling.
Source files are hash-pinned and retained read-only. [CALCULATION:
[lane and reproduction](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/README.md)]

The [review record](../infra/immigration-fiscal/sipp_departure_work_2026_10_16/review.md)
separates raw-record and numerical verification from the Gemini/Astra critique
of the final claims. Neither reviewer identified a material claim error;
their agreement does not supply causal identification. [CALCULATION; INFERENCE]

The useful conclusion is narrower than “adults compensate” or “adults stop
working”: **these observed ordinary separations show little average employment
or hours change over three months, with uncertain and sample-sensitive earnings
changes.** More precise forced-departure evidence could change that conclusion
for the target population. No v9 or existing figures-page update is made.
[INFERENCE]

Instrument check: LLM-assisted analysis retained increases, decreases, nulls,
the positive benchmark contrast and measurement failures under the same rules.
No sign or statistical-significance target governed the result.

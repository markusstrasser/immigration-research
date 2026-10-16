# Remaining adults' work after a household departure

**Verdict:** There is direct evidence that affected adults change their work, in
both directions. We have not verified a credible average U.S. earnings or hours
effect that can calibrate v9. The useful new result is a concrete data route:
**existing SIPP records can follow the same remaining adults around household
separations**. A preliminary record-level probe finds concrete candidate
transitions to audit; the final valid sample and its precision remain untested.
It does not identify deportations or a causal effect.
[SOURCE; DATA; INFERENCE: evidence below]

This audits one link: **a co-resident leaves → remaining adults change their own
work**. The target is the change in those adults' earnings, employment and hours,
over a stated period, compared with their work had the person stayed. Lost
earnings of the departed person, total household income, children's work and
community-wide enforcement exposure are different outcomes or treatments. The
[previous sensitivity](immigration-v9-household-work-response-2026-10-16.md)
priced hypothetical changes; this memo investigates whether evidence can select
one. Its materiality convention remains unchanged. [INFERENCE]

## What the direct U.S. studies establish

**Boyce and Launius (2020)** interviewed 125 Pima County households after an
immigration arrest. Of these, 64 reported shifting earning responsibilities:
26 sought more hours, 10 another job, and 28 previously non-employed people
sought work. The last group comprised 19 spouses and nine adult/teen children.
These are retrospective reports of **seeking work**, not measured realized
hours or earnings. Service-site snowball recruitment, mixed detention/removal/
release outcomes, and no untreated comparison prevent interpreting the counts
as a population causal effect. No sampling uncertainty for these counts is
reported. [SOURCE: [original article](https://doi.org/10.1177/2331502420973976),
Research Design and Employment and Education;
[underlying report](https://bmi.arizona.edu/sites/bmi.arizona.edu/files/BMI-Immigration-Dragnet-2019.pdf),
pp. 9–10, 21, 32–33]

**KFF's 2018 original interviews** document both mechanisms in separated
families: some adults took more work, while others reduced or stopped working
because the absent partner had supplied childcare. The study interviewed 20
affected families and 12 providers. It gives no average hours/earnings change,
control group or uncertainty interval. It establishes that these responses
occur, not their net frequency or magnitude. [SOURCE:
[Artiga and Lyons](https://www.kff.org/racial-equity-and-health-policy/family-consequences-of-detention-deportation-effects-on-finances-health-and-well-being/),
Issue Brief, financial hardship]

Two more substantial family studies do not close the measurement gap. Urban's
*Facing Our Future* follows 85 families after immigration arrests, but its income
table mixes departed, released and remaining workers. It cannot isolate the
remaining adults' response. *Between the Lines* follows families after an actual
Mexican-parent deportation with a comparison group, but its quantitative
outcomes concern children and family hardship; exposed-family follow-up is
substantially worse. Neither retrieved paper supplies the required adult work
effect. Their raw questionnaires or person-level data were not obtained.
[SOURCE: [Chaudry et al., Tables 1.3 and 3.1](https://www.urban.org/sites/default/files/publication/28331/412020-Facing-Our-Future.PDF);
[Martinez-Donate et al., Tables 1–3](https://doi.org/10.1016/j.jmh.2024.100233)]

## The closest new deportation study has a different treatment

Light, Andersen and Hendel's *Deportation's Fallout: Evidence from Denmark* is
listed as just accepted by the *American Journal of Sociology*. Its institutional
research summary describes lower employment and earnings among spouses after a
**deportation order**, including effects where the order was not executed.
The authors' abstract describes employment recovering within a year and slower
earnings recovery. This is a relevant lead, but cannot yet be treated as a
verified effect of physical departure. [SOURCE:
[publisher record](https://doi.org/10.1086/742317),
[researchers' institutional summary](https://rockwoolfonden.dk/udgivelser/partnere-til-udvisningsdoemte-kriminelle-arbejder-mindre/)]

We retrieved the **public replication code and authors' saved figure outputs**
from [Harvard Dataverse](https://doi.org/10.7910/DVN/BVCW55). The code confirms
court-order timing, individual spouses' outcomes, a month −7 reference, person
fixed effects and **90% confidence intervals**. Figure 2 gives the following
coarse visual readings; exact coefficient tables were not embedded:

| Months after conviction/order | Spouse employment estimate | Approximate 90% interval |
|---|---:|---:|
| 6 | −4 percentage points | −7 to 0 pp |
| 12 | −1 pp | −5 to +3 pp |
| 18 | +1 pp | −4 to +5 pp |

These are rounded readings of published notebook pixels, **not a re-estimation**.
They suggest an initial drop and estimates near zero later, with substantial
uncertainty. Earnings recover less in the saved figures, but no exact earnings
coefficient is asserted. The figures already show some deterioration before the
order; the estimate is not a clean change at the moment of physical departure.
[SOURCE: notebook cells 8/12, `dynamic_did.py`, `figure_2.py`,
[code anchors and source record](../notes/v9-household-response-evidence-2026-10-16/direct.md)]

Migration is consequential to interpretation: the saved informative-attrition
test reports p=.004, and unrestricted missing-outcome bounds span zero after
the order. Model-based reweighting/imputation retains the early negative pattern,
but does not prove migration irrelevant. The comparison is convicted noncitizens
with versus without an order; its causal reading needs defensible parallel
counterfactual changes. [SOURCE: notebook cells 18/22 and population code;
INFERENCE]

Individual records require Statistics Denmark approval. The full manuscript,
exact coefficient/SE tables and complete identification arguments remain
unverified; saved outputs were inspected, not regenerated. Denmark's welfare
system, spouse composition and the order-versus-departure distinction prevent
using this as a U.S. physical-removal parameter. [SOURCE: package README;
LIMIT; INFERENCE]

## Adjacent studies constrain the story, not the U.S. parameter

The strongest reason not to assume one sign is that the departure removes both
income and help, and replacement income changes the response. The source reads
below were selected to test that proposition and to retain null/imprecise
results. They are not pooled. [INFERENCE]

| Original study and population | Remaining adult outcome | What it can establish here |
|---|---|---|
| Coyne et al. (AER 2024), U.S. widows aged 58–61, linked tax/SSA records | Table 1: earnings +$1,290 (SE $545) among those ineligible for survivor benefits; −$605 (SE $461) among eligible widows. Participation +2.048 pp (SE 0.874) versus −1.690 pp (SE 0.866). | A strong income-replacement mechanism and heterogeneous responses. These are death/age/insurance-specific estimates, not a deportation elasticity; the negative earnings estimate is imprecise. |
| Gibson, McKenzie and Stillman (REST 2011), Tonga–New Zealand migration lottery, remaining adults aged 18–45 | Final Table 8, controlled IV: female employment −5.3 pp (SE 9.5), male +9.0 pp (SE 16.7), at a mean of ten months after migration. | Randomized migration opportunity with very imprecise individual work estimates. Voluntary migration and remittances differ from forced removal. Insignificance does not establish no response. |
| Bruns (2017), U.S. mothers in Fragile Families, partner incarceration | Table 2, controls plus lagged work: +1.191 weekly hours (SE 0.879), not statistically distinguishable from zero. | A measured but observational association; incarceration and the partner definition do not guarantee a newly absent co-resident. |

[SOURCE: [Coyne et al.](https://doi.org/10.1257/aer.20190813), Table 1;
Gibson et al. final-paper source and exact version in the
[source reads](../notes/v9-household-response-evidence-2026-10-16/analogs.md);
[Bruns original full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5629979/), Table 2.]

Coyne's death dynamics average years 1–3 after death; dollar amounts above retain
the paper's units, whose price year was not verified. They are not 2024 dollars
for the fiscal account. The earlier Gibson working paper gives different
coefficients; only the final article's estimates are used here. [SOURCE; LIMIT]

The source notes also retain Danish spouse-death estimates and Swedish
monitoring-versus-custody estimates. They reinforce the insurance and treatment
distinctions but do not supply the missing U.S. physical-departure parameter;
they are omitted from the compact table for that reason. [SOURCE; INFERENCE]

These numbers are estimates of individuals' work outcomes, not changes in the
whole household's income or public finances. The source notes retain sample,
timing, design and access limits. Secure Communities studies of country-origin/
city exposure are also kept separate: even a valid policy effect is not the
effect conditional on one's own household member leaving. [INFERENCE;
SOURCE: [policy boundary](../notes/v9-household-response-evidence-2026-10-16/policy-boundary.md)]

## A dataset route we actually checked

**SIPP is the first practical choice.** We opened the local public-use 2023,
2024 and 2025 archives and inspected the actual identifiers, monthly residence,
spouse/cohabitor links, employment, job-hours and earnings fields. The 2025 file
covers reference year 2024. Its 32,052 people contribute 379,215 person-months;
18,801 people also appear in the 2024 release, and 11,040 appear in all three
releases. These are unweighted archive/identifier counts, not population totals.
[DATA: [feasibility receipt](../notes/v9-household-response-evidence-2026-10-16/data/sipp_probe.json);
SOURCE: [data audit and dictionaries](../notes/v9-household-response-evidence-2026-10-16/data.md)]

A deliberately preliminary within-year screen found **214 remaining adults**
across **232 person-event months** where a separately tracked adult co-resident
moved to a different residence while the focal adult stayed. A separate screen
found 544 focal adults whose prior adult co-resident appeared only in the
limited-information roster and whose slot then disappeared. The second screen
is weaker: slot disappearance must be validated against stable-person sets and
roster coding. It retains 453 candidate person-event months with employment
observed for three months before and three including/after disappearance.
Neither count is a verified departure count, and the two screens must not be
added. No outcome change has been estimated. [DATA; LIMIT]

Subgroup support can shrink sharply: only 36 of the six-month Type-2 candidates
have a Mexican-identifying focal adult. That is not the v9 remaining-nonmember
population, nor a count of departures by Mexican co-residents. It warns against
assuming that an overall screen guarantees enough observations for any desired
subgroup. No power calculation has established a usable target-specific
coefficient. [DATA; INFERENCE]

The useful next analysis is therefore a **descriptive within-person study of
verified household separations**, preserving employment exits and entries,
hours and earnings separately. It should keep a fixed baseline adult cohort,
classify reasons/duration where observed, distinguish lost earners from lost
potential caregivers, and report movers, re-entry and nonresponse instead of
silently dropping them. Pre-event trajectories and future-departure comparisons
can test some confounding, but cannot make divorce, moving or other endogenous
exits exogenous. There is no verified deportation identifier or complete v9
lineage definition in this route. Employment and earnings missingness also need
separate treatment: an earnings blank can mean no in-universe job, while some
employed records have blanks too. Dropping all blanks or replacing all with zero
would distort the question.
[INFERENCE]

NLSY97 is a useful second route for marital/cohabitation changes and work histories;
the local archive and relevant IDs were verified. CPS is less suitable for this
question because it follows sampled addresses rather than movers. PSID and HRS
have relevant longitudinal structures, but their current AI-use restrictions
make them unsuitable for agent processing here; only their documentation was
inspected. The detailed data note records the exact fields, access conditions
and unresolved event-classification problems. [SOURCE; DATA:
[data feasibility](../notes/v9-household-response-evidence-2026-10-16/data.md)]

## Implication for v9 and the figures

The evidence supports **behavioral adjustment and competing signs**. It does
not select the uniform earnings change used in the earlier sensitivity, establish
a common response for all remaining adults, or demonstrate a decisive fiscal
correction. Earnings cannot be inferred from employment alone, an initial shock
cannot be treated as permanent, and full-lineage removal requires a separate
population/counterfactual bridge even from a good localized departure study.
**V9 and the figures remain unchanged.** [INFERENCE]

The check is falsifiable: a verified individual departure date, the same adult's
pre/post work outcomes, a defensible comparison and tracked relocation would
support or reject a response independently of this memo. Recovering the full
manuscript and numerical tables for the Danish study would improve that source
assessment; a cleaned
SIPP sample would establish actual U.S. separation patterns. Neither alone
licenses a deportation parameter or a mechanical addition to v9. [INFERENCE]

Instrument check: this is LLM-assisted research on a politically charged topic.
The search retained increased work, reduced work, and imprecise/null results;
the same population, selection and causal standards apply to each. The search
did not establish that no direct U.S. estimate exists. It established what the
retrieved originals and inspected data currently support. [FRAMING-SENSITIVE]

The raw-file replay preserved the quoted feasibility counts. The
[Gemini/Astra critique and complete dispositions](../notes/v9-household-response-evidence-2026-10-16/review.md)
retain the same conclusion; their suggestions were checked against original
schemas and records rather than accepted by agreement.

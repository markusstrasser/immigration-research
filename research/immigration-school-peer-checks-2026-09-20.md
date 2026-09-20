# Measured enrollment and white pupils' classroom outcomes

**Finding, September 20, 2026:** The earlier 10% enrollment increase was a
stress scenario. Actual state totals are available. Public student microdata also
permit the requested comparison conditional on starting achievement and school.
The executed estimates allow adverse effects but do not identify a causal
immigration effect or an annual national cost. [SOURCE/MODEL OUTPUT: below]

## Actual enrollment and capacity

| State / observed period | Total enrollment change | Recent-immigrant program count change |
|---|---:|---:|
| Texas, 2018–19 to 2023–24 | +99,326, **+1.83%** | 107,133 → 158,832, +51,699 |
| Texas, 2022–23 to 2023–24 | +12,804, **+0.23%** | 122,504 → 158,832, +36,328 |
| California, 2023–24 to 2024–25 | −31,469, **−0.54%** | 189,634 → 236,958, +47,324 |

[MEASUREMENT/CALCULATION: [TEA Tables2/14](https://tea.texas.gov/data-reports/school-performance/accountability-research/enroll-2023-24-0.pdf),
[CDE total enrollment](https://www.cde.ca.gov/ds/ad/cefenrollmentcomp.asp),
[CDE immigrant counts](https://www.cde.ca.gov/sp/ml/t3immdemgraphics.asp).]

Texas teacher FTE rose **4.56%**, 358,450.1 → 374,799.9, over the five-year
interval; all staff rose **7.84%**. Pupils per teacher FTE fell **15.15 → 14.76**.
These are statewide ratios, not classroom sizes. They do not establish an
immigration-caused hiring share, disprove local shortages, or say what staffing
would have been without immigration. [MEASUREMENT/CALCULATION:
[2019 staff](https://rptsvr1.tea.texas.gov/cgi/sas/broker?_debug=0&_program=perfrept.perfmast.sas&_service=marykay&ccyy=2019&id=S&lev=S&prgopt=reports%2Ftapr%2Fstaff.sas),
[2024 staff](https://rptsvr1.tea.texas.gov/cgi/sas/broker?_debug=0&_program=perfrept.perfmast.sas&_service=marykay&ccyy=2024&lev=S&prgopt=reports%2Ftapr%2Fstaff.sas).]

Recent-immigrant program status means ages3–21, born outside the states/DC/PR,
with at most three full US school years. It excludes descendants and earlier
immigrants. Its stock change is not arrivals: pupils also age out of eligibility.
The residual total minus this count is not a native-born population. California's
two totals have some coverage differences; Texas includes early education while
California includes transitional K. Do not interpret the residual decline as
native displacement. [SOURCE/INFERENCE: state definitions in sources above.]

California's nominal supplemental Title III immigrant grants were **$12.32m in
2023–24, $17.56m in 2024–25**. These are not total education spending; eligible
funded-LEA pupils and previous-fall reference dates differ from statewide counts.
They cannot supply the spending response in the earlier 10% scenario.
[SOURCE: CDE TableII, linked above.]

## Executed student comparison

The ECLS-K 1998 cohort contains **10,549** children classified as non-Hispanic
white, born in the 50 states/DC, with English as primary home language. Complete
model samples are smaller. Public and private schools are included. The data
identify teacher-reported LEP classmates and classroom racial composition;
neither is a complete count of immigrant classmates. US-born ELs, fluent
immigrants and immigrant descendants prevent equating these exposures.
[MEASUREMENT: [source/field card](../infra/immigration-fiscal/school_peer_checks_2026_09_20/DATASET_CARD.md).]

The comparison controls earlier reading **and** math scores flexibly, sex,
baseline age, socioeconomic composite and assessment interval. School fixed
effects compare children in different classrooms within the same school.
Kindergarten uses fall1998 exposure and spring1999 outcomes. The next follow-up
uses spring2000 classroom composition and scores, controlling both 1998 and
1999 scores. Spring2000 is a terminal classroom observation, not a verified
year-long assigned exposure. [MODEL SPECIFICATION]

**Any LEP classmate versus none**, in outcome-wave standard deviations:

| Outcome / follow-up | Pupils / schools | Starting-score adjustment only | Also school fixed effects | 95% interval, school-FE model |
|---|---:|---:|---:|---:|
| Kindergarten reading | 8,321 / 698 | −0.008 | **+0.004** | **[−0.056,+0.065]** |
| Kindergarten math | 8,319 / 698 | −0.020 | **−0.026** | **[−0.085,+0.033]** |
| Spring2000 reading | 6,639 / 667 | −0.055 | **−0.040** | **[−0.111,+0.031]** |
| Spring2000 math | 6,639 / 667 | +0.006 | **−0.056** | **[−0.136,+0.024]** |

[MODEL OUTPUT: [generator and reproduction](../infra/immigration-fiscal/school_peer_checks_2026_09_20/README.md),
`derived/results.json`. Same observations in each row's adjustment comparisons.]

The fixed-effects estimates are not uniformly smaller or more favorable than
the simpler estimates. None of the four intervals excludes zero. That permits
meaningful adverse effects, especially in the later follow-up; it does not
establish no harm. A linear **+10 percentage-point LEP-share** comparison yields
reading/math **−0.004/−0.015 SD** in kindergarten and **−0.011/−0.016 SD** in
spring2000; all four intervals include zero. Those are classroom percentage
points, not a 10% increase in school enrollment. [MODEL OUTPUT/INFERENCE]

The requested **all-white versus other classroom** comparison is also retained.
With baseline and school adjustment, spring2000 math is **+0.104 SD**,
95% **[+0.031,+0.177]**, n6,521. Reading is **+0.029 SD**,
**[−0.041,+0.098]**. Kindergarten estimates are **−0.011 reading/+0.020 math**,
both with intervals crossing zero. This is an adjusted association with racial
composition, not an immigrant, Mexican-origin or causal treatment effect.
Its positive math association must not be hidden, nor assigned a cause these
data do not identify. [MODEL OUTPUT/INFERENCE]

## What was checked, and what remains confounded

- All three specifications use a common sample for their given exposure/outcome.
  Repeated kindergarten pupils' separate teacher forms are harmonized instead
  of implicitly dropping them. Doing so weakens the initial spring2000 any-LEP
  reading/math estimates from about **−0.058/−0.080** to **−0.040/−0.056**.
  The initial values are superseded, not alternative preferred headlines.
- Invalid assessment-age intervals are excluded explicitly. The kindergarten
  comparison loses26 previously usable records; the change is small. The raw
  values remain untouched. IRT scale scores are explicitly cleared by NCES's
  published theta erratum; the affected theta fields are not used.
- Eight falsifications ask whether **future** classroom composition predicts
  already-realized kindergarten learning, controlling initial scores and the
  corresponding initial exposure. None rejects at a nominal5% level; intervals
  are wide. These checks cannot certify random teacher/class assignment.
- All48 fitted comparisons and eight falsifications are saved. Intervals are
  individual normal CR1 school-cluster intervals, not simultaneous, full survey
  design, or national transport intervals. A single favorable/adverse cell is
  exploratory. Classroom-share slopes have only roughly30–55 effective schools
  supplying exposure variation; hundreds of nominal schools overstate that
  source of independent information.

[MODEL QA: executable code and independent numerical checks in the lane;
[NCES theta erratum](https://nces.ed.gov/pubs2010/2010052.pdf).]

Independent reconstruction verified **all32 adjusted models**, including the
all-white contrasts: sample counts, coefficients and school-cluster SEs agree
to below9e-16. An altered coefficient correctly fails verification even with
Python optimization. This verifies the calculations, not their causal assumptions.
[EXECUTION: lane `verify.py`, `derived/final_verification.json`.]

**Unresolved:** teachers may be assigned stronger/weaker pupils within school;
families move; scores measure baseline ability imperfectly; teacher counts and
missingness can be selective. Early baseline scores already reflect exposures
before measurement, so adjustment changes the target to subsequent learning.
Within-school comparisons remove common school conditions and cannot recover
the full schoolwide resource effect. The sample's mean LEP exposure is about2%,
not a modern high-concentration setting. None of these issues is repaired merely
by a more flexible regression. [INFERENCE]

## Stronger causal route and existing studies

The strongest next target is **pupils enrolled before an externally driven
arrival shock**, followed whether they stay or move. Link their prior scores,
birthplace, classroom/grade placement, arrival dates and teacher assignments.
Use externally driven timing and age composition to predict arrivals, test
pre-shock trends and assignment balance, and estimate schoolwide effects
separately from within-school peer effects. Treat staffing/class size as
mechanisms after estimating the total effect. This is a proposed identification
design, not an already validated instrument. [PROPOSAL/INFERENCE]

Relevant evidence is already stronger than a cross-sectional school average:
Florida's published sibling design gives white-pupil reading **−0.0007 SD**,
95% **[−0.0201,+0.0187]**, per+10pp foreign-born exposure. Its main table does
not control prior scores; a separate check does, with a changed sample/exposure
window. The Haiti earthquake study supplies an external arrival shock, but the
checked subgroup is not specifically native-white. [SOURCE:
[Florida published Table5](https://www.anderson.ucla.edu/sites/default/files/document/2025-06/diversityinschools.pdf),
[Haiti working paper](https://caldercenter.org/sites/default/files/2024-11/WP%20180_0.pdf).]

Contrary evidence: Cho's **2011 manuscript** estimates white-pupil reading
**−0.037 SD**, SE0.023, for any-ELL exposure in its restricted English-classroom
sample. This is not a verified final2012 table or our replication. Its short
panel combines pupil fixed effects with lagged achievement, which raises a
separate dynamic-panel issue. Its claim of public-language-field suppression
does not describe the populated fields in the final public file inspected here;
exact sample/checkbox-code equivalence remains unverified.
[SOURCE: [Cho manuscript, Tables3/5](https://paa2011.populationassociation.org/papers/110005);
INFERENCE on specification and release equivalence.]

Other checked comparisons are kept at their measured scope: the
[Delaware working paper](https://edworkingpapers.com/sites/default/files/ai23-818.pdf)
studies new EL entrants, 27% of whom were US-born, without a native-white table;
[North Carolina](https://link.springer.com/article/10.1186/s40176-016-0074-y)
defines its native sample by never-LE status. Neither directly answers the
birthplace-specific question. Gaastra–Labanca's publisher abstract was a contrary
IV lead, but no accessible full table was verified, so no numerical result from
it is included. [SOURCE/SCOPE]

The held2011 ECLS cohort has usable scores and classroom EL counts but suppresses
child birthplace and teacher/external school IDs. It does not supply a drop-in
native-born replication. FDOE student records could implement the stronger
birthplace/arrival design, but require an approved research request and secure
access; no approved records or request are claimed here.
[SOURCE: [dataset card](../infra/immigration-fiscal/school_peer_checks_2026_09_20/DATASET_CARD.md),
[FDOE process](https://www.fldoe.org/accountability/accountability-reporting/external-research-requests/).]

## Crime novelty and accounting

Yes: the broad crime pattern and the Chalfin property-down/assault-up result were
already in the notes before the execution. The new work reproduced archived
models and supplied numerical fragility checks. The concrete new project
correction is that all1,282 available `dlogpc_*` values are changes in **log
counts**, despite rate-suggesting names. It was verification and measurement
repair, not a major new crime conclusion. [SOURCE: git `b163624` versus `2ce16e7`;
[executed crime note](immigration-causal-execution-2026-09-20.md).]

No national dollar amount is added. Observed education spending already includes
teachers; any separately established learning harm would need distinct welfare
accounting and an annual/lifetime conversion. The earlier10% scenario remains
a conditional calculation, with these observed results taking precedence when
describing actual enrollment. Null, adverse and favorable findings are retained;
LLM choice of specifications and sources remains an instrument limitation.
[ACCOUNTING CONVENTION/INFERENCE]

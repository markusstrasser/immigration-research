# School capacity and harm to incumbent children

**Finding, September 20, 2026:** Resource shortages can reduce learning, including
among white US pupils. The checked studies do not identify how much immigration
caused those shortages nationally, or a national annual dollar loss to native-born
white children. The earlier **$0 classroom-harm conclusion is withdrawn**; the
channel is **unpriced**. Small within-school peer estimates do not rule out a
schoolwide capacity effect. [SOURCE/INFERENCE: evidence below]

## Conditional estimate of resource dilution

For an illustrative 10% enrollment increase, let funding grow by `r × 10%`:

`spending per pupil / baseline = (1 + 0.10r) / 1.10`.

Assume $15,000 annual spending per pupil in **2018 dollars**, equal resource needs,
and a shortfall sustained for **four years**. This is an explicit scenario base,
not an estimate of current national spending or actual immigration-driven enrollment.

| Funding response | Per-pupil resources | Annual loss per pupil | Conditional four-year score effect |
|---|---:|---:|---:|
| No increase | −9.09% | $1,364 | −0.043 SD |
| Funding grows 5% | −4.55% | $682 | −0.022 SD |
| Funding grows 10% | unchanged | $0 | zero through funding dilution |

[MODEL OUTPUT] Calibration: Jackson–Mackevicius (2024) estimates an average
**0.0316 SD** score gain from $1,000 additional annual per-pupil spending sustained
four years. Its 90% range across contexts is **[−0.004,+0.067] SD**, wider than the
confidence interval around its average. Reversing/scaling that range gives
**[−0.091,+0.005] SD** with no funding response and **[−0.046,+0.003]** with half
response. These are transported calibration ranges, not immigration confidence
intervals or estimates specifically for native-white pupils.
[SOURCE: [published paper](https://kirabojackson.com/pdfs/jackson-mackevicius-2024-school-spending-policy.pdf), pp.413–414/424, Table2;
[DOI](https://doi.org/10.1257/app.20220279)]

Transport requires approximately linear, reversible effects, comparable useful
inputs and duration. Full headcount funding need not cover extra language needs;
spare capacity can reduce crowding. If teacher numbers grow at the same rate as
funding, pupil–teacher ratios rise 10%, 4.76%, or zero in these scenarios; that is
not an observed class-size response. Teacher and spending effects must not be
added as independent harms when they describe the same resource loss. [ASSUMPTIONS]

There is direct evidence from actual cuts: Jackson–Wigger–Xiong (2021), Table6,
estimates **−0.0267 SD** in white pupils' NAEP scores per $1,000 per-pupil spending
cut in **2015 dollars**, SE0.00566; approximate normal 95% CI **[−0.0378,−0.0156]**.
The design uses pre-recession reliance on state funding interacted with recession
timing, controlling state trends and economic-shock predictors. This is a white
category, not a native-born-only sample. Its state-level spending treatment cannot
separate subgroup exposure from subgroup responsiveness. It supports the resource
mechanism, conditional on the instrument; it does not establish an immigration
effect. [SOURCE: [published paper](https://kirabojackson.com/pdfs/jackson-wigger-xiong-2021-school-spending-cuts.pdf), Tables1/5/6;
[DOI](https://doi.org/10.1257/pol.20180674)]

## Direct immigrant-exposure evidence and its limits

All intervals below are source-table arithmetic, `estimate ± 1.96 SE`, conditional
on the original design. They are not pooled, simultaneous, or new microdata estimates.

| Evidence | Measured population and contrast | Finding |
|---|---|---|
| Florida, Figlio et al., ReStud2024, Table5 | US-born white, English at home; +10pp cumulative foreign-born school-cohort exposure; sibling design | Math **+0.0128 SD**, CI **[−0.0082,+0.0338]**. School×year effects absorb common schoolwide resource shocks. Mixed-origin exposure; not Mexican-specific. |
| North Carolina, Diette–Oyelere2017 | Grades4–8; “native” means never limited-English, not verified nativity | No significant average white-pupil LE effect; small adverse subgroup effects remain. School×year adjustment also removes common shocks. No exact subgroup CI recovered here. |
| Hamburg, Economic Journal2026, Table10 | German-born children; +1pp refugee share, conditional on no preparatory-class offer | **+0.0027 SD**, CI **[−0.0087,+0.0141]**. Controls pupil–teacher ratio/cohort size; cannot bound total crowding. German-born is not ethnic-white. |
| Denmark, ESR2023, Table3 | Native study population; any refugee arrival between tests | Reading **−0.010 SD**, CI **[−0.0276,+0.0076]**; mathematics **−0.010**, CI **[−0.0296,+0.0096]**. Binary-arrival contrast, not per refugee. |
| Italy, Ballatore–Fort–Ichino2018, Table2 | One immigrant replaces a native at fixed class size; class-formation-rule IV | Language **−1.58 percentage points correct**, CI **[−3.09,−0.071]**. Adverse peer evidence; not class-size crowding. Weak conditional first stages constrain inference. |

[SOURCES: [Florida full text](https://www.anderson.ucla.edu/sites/default/files/document/2025-06/diversityinschools.pdf),
[North Carolina full text](https://link.springer.com/article/10.1186/s40176-016-0074-y),
[Hamburg full text](https://academic.oup.com/ej/article/136/676/1217/8249266),
[Denmark full text](https://academic.oup.com/esr/article/39/3/352/6843667),
[Italy author paper](https://www.andreaichino.it/wp-content/uploads/2019/02/ichino_ballatore_fort.pdf)]

The Italian paper's approximately 0.16 SD uses a school-aggregate score
distribution; it cannot be compared directly with US pupil-score SDs. The immigrant
conditional first-stage F is about2.8, so its conventional interval is not a
weak-IV-robust bound. Conversely, favorable/null US estimates cannot establish
that all native pupils or all second-generation exposure carry zero harm. [INFERENCE]

## Germany: what PISA establishes

The OECD Germany note reports immigrant-background pupils rising **13%→26%**
between2012 and2022, a2022 mathematics gap of **59 points**, and **73%** of pupils
attending schools whose principals reported instruction hindered by teacher
shortages, versus57% in2018. These establish composition, gaps and reported
constraints, not immigration's causal contribution.
[SOURCE: [OECD Germany country note](https://www.oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/germany_1a2cf137-en.html)]

Holding the2022 group means fixed, changing group weights by13pp lowers the overall
mean by `0.13 × 59 = 7.67` points even with no loss to incumbent pupils. This is
an illustration of composition, not a decomposition of the historical decline.
PISA parental-birthplace groups are not racial groups. [CALCULATION/INFERENCE]

## Accounting, execution and correction

The relevant causal chain is arrival → enrollment/language needs → staffing and
instruction → incumbent outcomes. Estimate its total effect before controlling
for post-arrival staffing; investigate mechanisms separately. A credible next
design needs arrival variation, pre-arrival spare capacity and matched incumbent
outcomes, not just school immigrant shares. Public CCD/finance data do not alone
identify native birth or exogenous arrivals. [INFERENCE]

Additional teachers and buildings already included in fiscal spending cannot be
charged again as quality loss. A separate residual attainment loss can belong in
welfare accounting, but a lifetime earnings NPV cannot be added directly to annual
spending. No national dollar term is added here. [ACCOUNTING CONVENTION]

Reproduce all arithmetic with
[`school_spillovers.py`](../infra/immigration-fiscal/causal_execution_2026_09_20/school_spillovers.py).
Source estimates are transcribed; no original student data were acquired or
re-estimated. Independent primary-table checks verified both spending calibrations.
Contrary/null/adverse findings are retained together; LLM source selection remains
an instrument limitation. This is an evidence note, not essay narrative.

## Revisions

- 2026-09-20: withdraw the September16 school-angle memo's $0/no-US-harm/blanket
  second-generation exclusion, and the corresponding ladder81 and §13 summaries.
  The decisive distinction is peer exposure versus total resource capacity;
  [decision record](../decisions/2026-09-20-school-quality-unpriced.md).

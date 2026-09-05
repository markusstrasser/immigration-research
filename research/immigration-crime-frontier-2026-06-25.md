# Immigration — Crime Frontier (2026-06-25; interpretation repaired 2026-09-05)

**Verdict:** The checked literature supports lower observed justice-system rates for several US immigrant populations and generally null-to-negative area-level associations. It does not establish a universal unauthorized offending rate, a zero causal effect in every setting, or inevitable second-generation deterioration. The June search was bounded, and dataset access descriptions below are leads rather than a current access audit. [SOURCE references below; INFERENCE]

## What the new evidence measures

- **Marie & Pinotti (2024), JEP, international review:** Nationality-group overrepresentation in some European justice data and a small average local causal effect can coexist. Composition, policing and legal labor-market access are possible explanations, with designs and contexts differing across studies. This review does not make all country-specific or policy-specific effects zero. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.38.1.181]
- **Light & Anadon, NIJ 308552:** California/Texas administrative recidivism evidence is relevant to subsequent recorded contacts among sampled people. Deportation and other exits change the population still observable; an unobserved risk set limits interpretation as an offending probability. [SOURCE: https://www.ojp.gov/pdffiles1/nij/grants/308552.pdf]
- **El Paso studies, NIJ 309524:** Study 2 interviewed 273 people booked into county jails; 24 interviews occurred after release in the community. The report compares prior offenses and measured risk among selected justice-involved people. Risk-assessment scores are not new observed crimes, and being interviewed outside jail does not make this a representative community sample. Associations between acculturation and risk in this sample do not identify within-person assimilation or population-wide generational change. Conditioning on arrest/booking can change associations between immigration status and offending. [SOURCE: https://www.ojp.gov/pdffiles1/nij/grants/309524.pdf, pp. 17, 47; INFERENCE] The related 2026 manuscript remains a source lead: https://psycnet.apa.org/manuscript/2026-50707-001.pdf.
- **RTI/NIJ 310356:** Uses model-imputed unauthorized shares and police records at census-tract level in selected jurisdictions in 2019. The report finds no statistically significant association between estimated unauthorized shares and the examined arrest outcomes in its controlled specifications, while authorized shares have negative associations in some destination/offense categories. This is an ecological association. It cannot identify who committed an offense, establish a causal zero, or show that authorized immigrants uniquely cause a protective effect. A significant coefficient and an insignificant coefficient are not necessarily significantly different. Its second-generation discussion on pp. 11–12 reviews earlier individual studies; it is not a new generational result from the tract analysis. [SOURCE: https://www.ojp.gov/pdffiles1/nij/grants/310356.pdf, pp. ES-2, 1–4; INFERENCE]

## Victimization, reporting and offending

**Xie & Baumer (2021)** and subsequent NCVS work concern victimization and reporting. Citizenship/nativity identifies neither unauthorized status exactly nor the perpetrator’s status. A lower victimization rate cannot directly validate a lower offending rate. [SOURCE: https://doi.org/10.1111/1745-9125.12278; https://pmc.ncbi.nlm.nih.gov/articles/PMC8849556/; INFERENCE]

Cato’s 2025 NCVS analysis reports lower immigrant victimization and higher personal reporting in its comparisons. Those between-group levels do not refute a causal chilling effect of a change in enforcement. Cato’s pro-immigration position also makes this no automatic “against-interest” finding. [SOURCE: https://www.cato.org/policy-analysis/immigrants-cut-victimization-rates-boost-crime-reporting; INFERENCE]

Gonçalves, Jácome & Weisburst study enforcement changes and report lower reporting and higher victimization in affected populations. Their design concerns a policy margin and victims, not a direct estimate of unauthorized perpetrators’ crime rates. Reporting changes can affect recorded offenses and resulting arrests/convictions as well as police-recorded victimization. Homicide occurrence is relatively well recorded, but offender identification, case clearance, conviction and immigration-status classification still matter. [SOURCE: https://www.nber.org/papers/w32109; INFERENCE]

## Generations and origin

Some individual studies find second-generation offending above the first generation and closer to third-and-higher-generation peers. This does not establish that second-generation rates exceed the latter group. Algebraically, `r_native = a·r_2 + (1−a)·r_3+`; the native benchmark exceeds `r_3+` only when `r_2 > r_3+`. Selected jail studies, an area’s immigrant-origin share and a review of prior studies are not interchangeable individual evidence. [SOURCE: Bersani studies cited in NIJ 310356; INFERENCE]

Repeated arrival-cohort cross-sections also do not follow the same people. Age, period, age at entry, return migration, mortality and changing cohort composition remain alternatives to within-person assimilation. [INFERENCE]

## Useful dataset leads and their limits

| Dataset | What it can contribute | Limit relevant to the claim |
|---|---|---|
| AARIN / ICPSR 39107 | Detailed interviews and status information among its sampled justice-involved respondents | Selection into arrest and interview; self-report is not a population offending rate without an appropriate sampling design |
| NCVS | Victimization, reporting and available citizenship/nativity fields | No exact unauthorized perpetrator denominator; pooling years requires survey weights and design-based precision |
| NIBRS / police records | Recorded offenses and case characteristics | Do not infer nativity/status coverage from crime categories; check the specific schema and reporting coverage |
| Texas DPS | Status-linked arrests/convictions for the covered population | Status updates, event/person definitions, denominator timing and classification lag need explicit handling |
| SCAAP | Program-submitted qualifying inmate-days and reimbursement | Custody person-time, not population offending; unresolved-status and nonparticipation gaps |

Sources: https://www.icpsr.umich.edu/web/NACJD/studies/39107; https://bjs.ojp.gov/data-collection/ncvs; https://www.dps.texas.gov/section/crime-records; https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/overview. These are acquisition/review leads, not a claim that all needed restricted files were obtained.

## Disconfirmation and remaining limits

Lott’s Arizona interpretation faces a serious classification critique. This memo has not independently reconstructed the underlying agency data and must not call the sign reversal independently reproduced or definitive. A tool-generated confidence score adds no primary evidence. See the bounded source review in [the crime-rate memo](immigration-crime-rates-unauthorized-vs-native-born.md). [SOURCE: linked memo and its primary/critique references; INFERENCE]

The checked studies do not establish a general US immigrant crime wave. They also do not settle every current-surge cohort, origin, crime type or enforcement policy. Arrest/conviction/incarceration evidence and area-level policy evidence constrain different hypotheses; no one of them substitutes for all the others. [INFERENCE]


## Revisions

- **2026-09-05 — Rebuilt the frontier around sampling units and observable outcomes** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Historical revision entries above describe the earlier state, including conclusions superseded here.

## Historical quoted strings retained verbatim

These quotations, hypotheses and labels appeared in the June working memo. They are retained for provenance; they are not a renewed endorsement or certification as primary-source quotations. Current conclusions and source scope are above.

"disproportionately represented among offenders in numerous host countries"

"Unauthorized Immigration, Crime, and Recidivism: Evidence from Texas"

"Research into Immigration and Crime … Synthetic Population,"

"Does more immigration lead to more violent and property crimes? 30 OECD countries 1988–2018,"

"Immigrant status, citizenship, and victimization risk … new findings from NCVS,"

"Immigrants Cut Victimization Rates, Boost Crime Reporting"

"at least 142% more likely to be convicted,"

"immigrants (esp. first-generation) commit less crime than the US-born"

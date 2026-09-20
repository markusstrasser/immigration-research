# Later-generation estimates: GSS, CPS and independent checks

Date: 2026-09-20. [MODEL / MEASUREMENT INDEX] Population composition only; no
annual-dollar, fiscal-incidence or policy-effect estimate is changed.

**Finding:** Recent GSS surveys, adjusted to the CPS2025 adult age distribution,
give **3.51–3.83m generic G4+ adults** under the central missing-data assumption.
Allowing unknown grandparents and ages to differ gives a **2.71–4.71m conditional
sensitivity envelope** before sampling error. The older Pew source gives a lower
central estimate. Exact G4 versus G5+ remains unresolved.
[SOURCE: [generators, formulas, input locks and checks](../infra/immigration-fiscal/generation_estimation_2026_09_20/README.md).]

## Population and question

[MEASUREMENT] Target: **8.183369m CPS2025 civilian-household Mexican-identifying
adults**, native with two US-area-born parents, all education levels. This is
the adult portion of the existing G3+ category, not all 40.897m Mexican-origin
residents. Target age shares are 20.30% at 18–24, 42.89% at 25–44, 24.64% at 45–64,
12.17% at 65+. No person is added to the account.

[DEFINITION] Generic G4+ means four US-born grandparents among people identifying
as Mexican. A foreign-born grandparent defines generic G3 but need not be from
Mexico. Neither category proves the country of more distant ancestors. The
existing [observed CPS split](immigration-fourth-generation-scope-2026-09-20.md)
remains unchanged; this analysis estimates aggregate composition without
assigning missing individual histories.

## Executed main estimates

[MODEL] Within each age group, the central scenario uses the G4+ fraction among
GSS respondents with known grandparents. It assumes unknown-grandparent and
unknown-age reports are ignorable for those within-age proportions, and that
the survey-period proportions transfer to the CPS2025 population. The rows
below use preferred WTSSNRPS with original pooled survey weight mass.

| GSS source | Generic G4+ share of adult G3+ | Adults, millions | Approximate conditional 95% sampling interval, millions |
|---|---:|---:|---:|
| 2016–2024 | 45.26% | 3.704 | 2.991–4.416 |
| 2021–2024 | 42.85% | 3.506 | 2.613–4.399 |
| 2016–2024 excluding 2021 | 46.21% | 3.782 | 3.010–4.554 |

The full grid also changes the official weight and normalizes each full survey
year to equal mass before the Mexican-domain selection. Central estimates span
3.506–3.828m. This spread is a specification sensitivity, not a confidence interval.
The 2021 exclusion tests the collection-mode change documented in
[NORC's methodological primer](https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/2021%20XSEC%20Methodological%20Primer.pdf);
it is not a causal estimate of interview-mode effects.

Sampling calculations retain the full GSS stratum/PSU frame, within-survey
covariances and all 160 CPS replicates. Reported intervals use the sum of source
SEs to bound unknown source covariance at first order and a small-domain t
reference. They exclude period/frame transport, identity selection and reporting
error. They are not all-uncertainty intervals. [SOURCE:
[NORC design guidance](https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/GSS%20design%20variables.pdf);
[subpopulation degrees of freedom](https://www.stata.com/manuals/svysubpopulationestimation.pdf), pp.4–6;
generated `standardized_scenarios.csv` and `audit.json`.]

## Missing histories and children

| Construction, preferred2016–2024 source | Adult G4+, millions |
|---|---:|
| Known-age respondents, all unknown grandparents non-G4 versus G4 | 3.330–4.178 |
| Also allow unknown ages to enter unfavorable/favorable age cells | 3.050–4.619 |
| Previous row expanded by conditional sampling endpoints | 2.369–5.439 |

[MODEL / OUTER ENVELOPE] Across all 12 source specifications, the missing-age and
grandparent envelope is **2.712–4.705m adults**, or 33.14–57.50% of adult G3+.
Expanding endpoints by their conditional sampling intervals gives 1.896–5.707m.
These envelopes are deliberately conservative and are not sharp jointly
achievable bounds or simultaneous confidence regions. Source-to-target
transport remains assumed throughout.

For children, current CPS reports 1.634m G4+ and 2.204m unresolved; the child
envelope is therefore 1.634–3.838m without applying adult rates. Adding these
inside each CPS replicate yields an **all-age conditional G4+ envelope of
4.346–8.543m**, or about 11–21% of the existing 40.897m population, before sampling
expansion. Including the endpoint sampling intervals widens it to 3.391–9.749m.
This is not an estimate of exact fourth generation. [SOURCE: CPS target
replicates and generated scenario rows; unchanged parent-link classifier.]

## Independent surveys: agreement is incomplete

[MEASUREMENT / MODEL] Pew 2015 identifiers provide 160 Mexican-origin adults born
in the US to two US-born parents. After matching the same CPS age shares, the
distribution is 55.96% generic G3 / 32.45% G4+ / 11.59% unknown. The central within-age
missing-at-random construction gives **37.29% G4+**, equivalent to 3.052m if that
historical distribution were transferred to 2025. This is lower than recent
GSS. Age adjustment alone does not remove period, coverage or questionnaire
differences. No design-correct Pew subgroup CI is claimed; its release lacks
sufficient variance information. Two unresolved-age cases are excluded from
age standardization and retained in the source audit.
[SOURCE: original Pew SAVs/codebooks;
[Pew methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/);
generated `historical/pew_standardized.csv`.]

Pew's 44 nonidentifiers are a different target: their corresponding G4+ share is
53.52% with 18.97% grandparents unknown, or 64.52% under the central construction.
They are not mixed into the CPS-identifying population. This is evidence that
identity selection can matter, not a measured count of missing descendants.

NLSY97 supplies 220 retained Mexican/Chicano-identifying adults born 1980–1984,
native with two native biological parents. Its observed G4+ share is 45.04%,
with 17.56% unknown; the central ratio is 54.64% with a 44.30–64.98% design interval.
The corresponding GSS approximate birth-cohort sample has only 36 people; its
central 62.51% interval is 31.37–93.65%. Some narrower birth-year definitions
have no usable domain degrees of freedom. Thus the cohort comparison is
compatible but weak validation. NLSY's original identity nonresponse and
2023 retention remain selection limits.
[SOURCE: held NLSY family/base/design extracts;
[official sampling-design guide](https://www.nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects);
generated `historical/design_cohort_estimates.csv`.]

[INFERENCE] Do not average these sources into a single supposedly stronger
estimate: Pew is historical, its nonidentifiers answer a different population
question, and NLSY follows a selected birth cohort. None establishes that age
alone makes the current CPS missing-history subset exchangeable with donors.

## PSID completeness audit: access remains unresolved

[SOURCE-CHECKED] PSID's 2023 family codebook contains 567 Mexican-origin reference
persons and 364 spouses/partners, **931 adult-role records before ancestor
completeness or weight restrictions**. FieldsER85120/ER84993 identify origin;
ER85113/ER84986 give state of birth with territories/foreign births pooled.
These do not by themselves identify Mexican birthplace.
[SOURCE: [2023 family codebook](https://psidonline.isr.umich.edu/documents/psid/codebook/FAM2023ER_codebook.pdf), pp.1039,1041,1113–1115.]

Historical country-of-birth variables ER33422 (1997) and ER33525 (1999) exist, but
their applicable interview universes are selective. FIMS can link biological
great-grandparents. No core/FIMS microdata are held; official retrievals reached
PSID registration/conditions-of-use gates or an HTTP403 challenge. The existing
ICPSR login does not establish PSID access. No joint completeness count was computed.
[SOURCE: [individual codebook](https://psidonline.isr.umich.edu/documents/psid/codebook/IND2023ER_codebook.pdf), pp.598–600,623–624;
[FIMS manual](https://simba.isr.umich.edu/FIMS/FIMS_UG.pdf);
[PSID data access](https://simba.isr.umich.edu/data/data.aspx).]

The [prepared extraction specification](../infra/immigration-fiscal/generation_estimation_2026_09_20/PSID_ACCESS.md)
defines the exact files, variables and completeness counts. Actual data access
is still needed. A large raw Mexican sample would not guarantee enough complete
great-grandparent histories.

## Decision impact and verification

- **Improved:** a reproducible aggregate estimate with explicit missingness and
  sampling uncertainty, plus an independent historical discrepancy.
- **Unchanged:** individual CPS histories, fiscal totals, exact G4/G5 classification
  and generation-specific fiscal outcomes. Population shares alone do not reveal
  the outcome distribution within unresolved records.
- **What would tighten it:** representative recent grandparent/great-grandparent
  histories, better response follow-up, or linked PSID records with demonstrably
  adequate completeness and population coverage.

Source hashes, unique joins, official NLSY variance benchmark, boundary tests
and independent raw-data reproduction passed. LLM-assisted synthesis remains
subject to the project's [instrument caveat](../notes/llm-bias-caveat.md); the
generators and primary sources are the evidence.

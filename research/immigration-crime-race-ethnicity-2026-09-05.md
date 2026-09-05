**Verdict:** Black prisoners can and should be reported separately in the held SPI data. The official 2016 prisoner composition is **33.10% non-Hispanic Black, 30.08% non-Hispanic White, and 22.38% Hispanic of any race**. Birthplace and citizenship can be cross-tabulated with these categories. These are **shares of prisoners, not group crime or incarceration rates**. None of the 15 data tables in the held Texas replication archive supplies a race/ethnicity split, so its immigration-status rates cannot be separated into Black and White rates. [DATA: reproducible files below]

# Crime, race and ethnicity: what the observed fields identify

Date: 2026-09-05. This is a descriptive source audit responding to the request to separate Black people in the crime statistics. It extends the [conduct-denominator repair](immigration-conduct-denominators-2026-09-05.md). The comparison frame is explicit group reporting, not treating race as an explanation of offending. No existing crime loader or canonical database was changed by this lane.

## Categories and available joints

The SPI source provides separate Hispanic-origin and multiple-response race questions, plus an official combined recode. For a mutually exclusive main table, use the source's **non-Hispanic Black**, **non-Hispanic White**, **Hispanic of any race**, and remaining categories. Keep non-Hispanic multiracial people separate. A supplementary **Black regardless of ethnicity, alone or in combination** measure is also calculated; it overlaps Hispanic and multiracial categories and must not be added to them. [SOURCE: ICPSR37692 DS0001 codebook, V1951–V1957 and RV0003, printed pp.898–900,906–907; [SPI source record](https://www.icpsr.umich.edu/web/NACJD/studies/37692)]

| Held source | Race and Hispanic ethnicity | Birthplace/nativity | Citizenship or legal status | What can be split here |
|---|---|---|---|---|
| SPI 2016 DS0001 public-use microdata; version March 28, 2024 | V1951 ethnicity; V1952–V1957 multiple race indicators; RV0003 combined recode | V0945: United States versus other country; V0951: years lived in U.S. | RV0004: citizen, noncitizen, missing; no authorized/unauthorized distinction | Joint prisoner composition by recorded race/ethnicity × birthplace × citizenship |
| Light–He–Robey Texas replication, 2012–2018; Pew variants stop in 2017 | Absent in **all 15** archived DTA schemas, including detailed offenses and conviction variants | Source-defined native-born versus immigrant aggregate groups | Unauthorized/legal immigrant groups; some files split naturalized people from legal immigrants | Existing aggregate status comparisons only; no race-specific numerator or denominator |
| SCAAP FY2023 and FY2024 award tables | No person-level race or ethnicity columns | No birthplace or nativity columns | Jurisdiction-level confirmed/unknown custody days, not individual status histories | Jurisdiction custody exposure and awards; no race × status rates |
| Located Texas DPS cumulative release through May 31, 2026 | Located status/offense count table has no joint race/ethnicity cells | No matched birthplace population | Administrative identified-unauthorized counts; cumulative since June 2011 | No population rate by race; direct PDF download previously timed out |
| USSC citizenship crosswalk entries in repository code | No corresponding local offender microdata acquired in the inspected source tree | Not established from actual data here | Existing codebook mappings remain explicitly unverified | No computed USSC race/status result |

[SOURCE: `analysis/source-schema.json`, actual table columns and prior source archive; [Light replication](https://www.openicpsr.org/openicpsr/project/124923/version/V1/view); [FY2024 SCAAP table](https://bja.ojp.gov/funding/scaap-fy24-awards.pdf); [DPS release locator](https://www.dps.texas.gov/sites/default/files/documents/administration/crime_records/pages/illegalarstconv.pdf)]

**Citizenship and birthplace remain distinct.** A U.S. citizen reporting birth in another country is not automatically a naturalized citizen: the public-use variables do not establish citizenship at birth. V0945 is therefore labeled reported birthplace, not silently equated to the Census nativity definition. Neither Black nor Hispanic ethnicity supplies unauthorized status, religion or national origin. [SOURCE: SPI V0945, RV0004 and suppressed country-of-citizenship fields V0946–V0949; INFERENCE about the identification limit]

The historical FBI NIBRS instrument also records race and Hispanic ethnicity separately. White and Hispanic can coexist on one record. That establishes a coding distinction, not a correction factor that can be imposed on the Texas status aggregates. The calculations here do not infer citizenship or birthplace from race. [SOURCE: [FBI NIBRS guide](https://ucr.fbi.gov/nibrs/nibrs_dcguide.pdf), arrestee elements49–50, historical instrument; SPI codebook]

## Recent official imprisonment rates, a separate comparison

The latest final *Prisoners* report located in this bounded search is **Prisoners in2023**, published **September30,2025**. Its Table6 supplies these national rates per100,000 adults of the same group:

| Year-end | Non-Hispanic Black | Non-Hispanic White | Hispanic, any race |
|---|---:|---:|---:|
| 2022 | 1,196 | 229 | 603 |
| 2023 | 1,218 | 231 | 606 |

The numerator is prisoners **age18+ sentenced to more than one year** under state/federal jurisdiction at December31. Census resident denominators refer to January1 following. These are official adjusted estimates: BJS corrects administrative race/Hispanic reporting using prisoner-survey distributions, including SPI2016. They are not fresh self-reports from every prisoner. [SOURCE: [BJS Table6 and methodology pp.43–44](https://bjs.ojp.gov/document/p23st.pdf); [publication date](https://bjs.ojp.gov/library/publications/prisoners-2023-statistical-tables)]

These figures show substantial descriptive imprisonment differences. They combine sexes and adult ages without standardization, contain no nativity/status split, and do not measure a causal race effect. They cannot repair the Texas status-by-race gap or supply denominators for SPI counts. No2024/2025 final race-specific prison-rate table was acquired. [DATA: source PDF and `analysis/bjs_p23st_table6_adult_rates.csv`; INFERENCE]

## Reproduced prisoner composition

The unit is a person in the SPI's 2016 adult state/federal prison population. The sample has **24,848 respondents**; summing V1585 gives **1,421,724 weighted prisoners**. All denominators in this section are prisoner counts. The survey's age target is 18+, and the previous audit verified every observed age is at least18. Source-weighted estimates below are rounded, not exact administrative counts. [SOURCE: [SPI study design and universe](https://www.icpsr.umich.edu/web/NACJD/studies/37692); DATA]

| Official disjoint category | Sample n | Weighted prisoners, rounded | Share of all weighted prisoners |
|---|---:|---:|---:|
| Non-Hispanic Black | 7,452 | 470,550 | 33.10% |
| Non-Hispanic White | 8,389 | 427,675 | 30.08% |
| Hispanic, any race | 5,393 | 318,173 | 22.38% |
| Non-Hispanic multiracial | 2,715 | 149,715 | 10.53% |
| Non-Hispanic American Indian/Alaska Native | 360 | 20,460 | 1.44% |
| Non-Hispanic Asian/Native Hawaiian/Pacific Islander | 227 | 14,043 | 0.99% |
| Non-Hispanic other | 7 | 617 | 0.04% |
| Uncategorized/missing | 305 | 20,491 | 1.44% |

[DATA: `analysis/spi_race_composition.csv`; official RV0003 classification. Rounded percentages may not total exactly100.]

The requested split also survives a joint tabulation, rather than assuming all Black or Hispanic prisoners belong to one immigration group:

| Prisoner subgroup | NH Black weighted prisoners (sample n) | NH White weighted prisoners (sample n) | Hispanic-any-race weighted prisoners (sample n) |
|---|---:|---:|---:|
| Reported U.S. birthplace | 458,213 (7,239) | 417,141 (8,195) | 206,610 (3,338) |
| Reported other-country birthplace | 9,531 (167) | 9,223 (172) | 110,703 (2,036) |
| Birthplace unresolved | 2,806 (46) | 1,310 (22) | 860 (19) |
| Current noncitizen, separate overlapping panel | 5,364 (101) | 3,459 (61) | 81,629 (1,504) |

The first three rows partition each column; the last row is a separate citizenship slice and must not be added to them. The full output further separates citizens and noncitizens within each birthplace/race cell. For example, the other-country-born NH Black sample contains **101 noncitizens and66 citizens**. Small cells support only cautious descriptive reporting; no survey-design standard errors were calculated. [DATA: `analysis/spi_joint_race_official.csv`]

The broader Black indicator counts **9,403 respondents**, or **587,365 weighted prisoners**, because it includes people reporting Black alongside another race and/or Hispanic origin. There are **697 Black-and-Hispanic respondents** (42,345 weighted prisoners). Likewise **1,729 White-and-Hispanic respondents** represent89,118 weighted prisoners. These observed overlaps demonstrate why raw “Black,” raw “White,” and “Hispanic” cannot be presented as three disjoint categories. [DATA: `analysis/spi_overlapping_race_indicators.csv`]

## Missing ethnicity and the source recode

There are **36 respondents with unknown Hispanic origin** in the upcoded V1951 field, representing **2,305.86 weighted prisoners**, or **0.1622%** of the total. The official RV0003 assigns31 of those respondents to categories labeled non-Hispanic. This is explained by the archived BJS reconstruction syntax: Hispanic=yes takes priority; otherwise the program proceeds through the race indicators without requiring Hispanic=no. The analyzer reconstructs that exact ordering and matches **every official RV0003 value**. This is a verified source convention, not evidence of deliberate misreporting. [SOURCE: `source-derived-syntax.txt`, lines60–80, extracted byte-for-byte from the official SPI archive; DATA]

To make this visible, outputs preserve both the official recode and a variant that labels every unknown V1951 response ethnicity-unresolved. Holding recorded race classifications fixed, deterministic allocations of unknown ethnicity produce these ranges:

| Prisoner share | All unknown ethnicity assigned to the excluding category | All eligible unknown ethnicity assigned to the including category |
|---|---:|---:|
| Hispanic, any race | 22.3794% | 22.5416% |
| Non-Hispanic Black, official single-race classification | 33.0516% | 33.0971% |
| Non-Hispanic White, official single-race classification | 30.0429% | 30.0814% |

These are **missing-ethnicity bounds conditional on recorded race**, not confidence intervals or bounds on all misclassification. They do not resolve the305 uncategorized race/ethnicity records or hypothetical misreporting among recorded responses. The upcoded questionnaire answers are not themselves wholly unprocessed raw responses: BJS incorporates some open-ended answers into existing categories. [SOURCE: codebook printed pp.15–18; DATA: `analysis/spi_unknown_ethnicity_bounds.csv`]

## What this does and does not change

The aggregate native-born comparator in Texas must not be described as non-Hispanic White. Separating Black people could change a comparison, but the held Texas data cannot determine the size or direction of that change. Applying a national prisoner race share to Texas arrest charges would mix geography, outcome, custody duration, years and population denominators. It is therefore not a valid racial adjustment. [INFERENCE from the measured universes]

Likewise, a larger share of prisoners does not by itself establish a higher population crime rate. A population-rate comparison needs a matching population denominator and compatible race/ethnicity, age, sex, geography, citizenship/nativity and year definitions. Prison stock also reflects detection, prosecution, sentencing and time served. Neither the within-prison tables nor a race control by itself identifies a causal effect of immigration or race. [INFERENCE; measurement framework in the conduct-denominator audit]

**Disconfirmation:** The user concern that racial pooling can hide a different comparison is valid as a possibility. The actual files disconfirm any claim that all measured Hispanic people are merely coded White or that the current Texas rate has already been recomputed against a White comparator. Conversely, separating groups does not establish the hypothesis that Black people explain the entire native/immigrant gap. That decomposition remains unavailable here. These conclusions are symmetric across the possible direction of a future properly matched comparison. [DATA; INFERENCE]

Coverage differs by source: SPI describes2016; Texas replication describes2012–2018; the new BJS report supplies2022–2023 race-specific imprisonment rates. None identifies the crime of the2021–2024 arrival cohort, and a2024 release date does not make SPI observations current. The four most recent complete calendar years,2022–2025, have **no joint race × immigration-status population crime rate** in the held artifacts audited here. This is a local data ceiling, not a claim that no such data could be obtained elsewhere. [SOURCE: source metadata and inspected schemas]

## Reproduction and scope

```bash
uv run --with pandas --with pyreadstat python3 \
  infra/immigration-fiscal/build/analyze_conduct_race.py \
  --data-root /Volumes/2TBPNY/research-data/immigration-fiscal/data \
  --output .scratch/clarity-next-20260905/conduct-race/analysis \
  --bjs-report .scratch/clarity-next-20260905/conduct-race/p23st.pdf

uv run --with pandas --with pyreadstat python3 -m unittest discover \
  -s infra/immigration-fiscal/tests -p test_conduct_race.py -v
```

Archive: `.scratch/clarity-next-20260905/conduct-race/`. The source-schema JSON enumerates every column of all15 Light DTA files, not just a keyword search over filenames. Source codebooks, source reconstruction syntax, hashes, numerical outputs and missingness tables support the conclusions. Six focused tests validate category conservation, overlapping race/ethnicity, missingness, source reconstruction and invalid inputs. No canonical database is opened by the analyzer.

**Included:** all15 Light tables; SPI public-use microdata fields, codebook and official reconstruction syntax; the3.98MB BJS *Prisoners in2023* report and extracted adult-rate table; prior FY2023/FY2024 SCAAP schemas and DPS/FBI primary-source anchors; existing USSC placeholder mappings as unverified; the new analyzer, tests and outputs. **Skipped:** wage statistics (parent's parallel lane); new paid X (unnecessary); restricted individual Texas records (not publicly acquired; a separate access process is needed); immigration-status rate estimation without matched denominators (unidentified); current-cohort and ideological-extremism estimates (no suitable joint fields/time period); edits to existing loaders, indices or canonical databases (parent-owned).

## Revisions

- **2026-09-05 — Separated measured race and ethnicity from immigration status.** Added an explicit Black category and joint prisoner tables; preserved Hispanic-any-race and multiracial distinctions; exposed the official recode's handling of unknown Hispanic responses. The source convention was checked against primary reconstruction code instead of treating labels as complete observations. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).

# Is first-generation crime costlier per offence? Texas felony arrests weighted by social cost

## Current correction — September 19, 2026

**Verdict:** Retain the all-age pooled foreign-born cost-weighted charge ratio of 0.79 against all US-born Texans. The 0.59 “per-adult” ratio and the 18–39 arm change only population denominators, not the ages of charged people; they are denominator scenarios, not age-specific or age-standardized charge rates. The legal-immigrant classification is also not “anyone with a DHS record”: the primary classifies DHS-designated undocumented people separately and combines designated-legal people, other noncitizens not designated undocumented, and foreign-born citizens in the legal group. A status-mismatch explanation for the cost premium is unestablished. [SOURCE: [Light, He and Robey, Materials and Methods](https://www.pnas.org/doi/10.1073/pnas.2014704117); lane weighting code; INFERENCE]

This correction governs conflicting claims in the retained assessment below. Evidence and scope: [five-day cross-check](immigration-five-day-cross-check-2026-09-19.md).

## Retained assessment and evidence

**Verdict:** No for the undocumented, partly for legal immigrants. Weighting each felony arrest charge by its McCollister social cost moves the undocumented ratio to the US-born from 0.40 to 0.43 per capita (0.31 to 0.33 per adult): their offence mix is not costlier. Legal immigrants (naturalized included) are charged 0.78 times as often as the US-born but carry 1.01 times the cost per capita (0.75 per adult), because their homicide charges run at parity and their sexual-assault charges at 1.6 to 2.0 times the US-born rate in every year. The foreign-born pooled land at 0.63 by count and 0.79 by cost per capita, 0.48 and 0.59 per adult. The comparator is all US-born Texans, not US-born whites, and the legal/undocumented boundary rests on DHS record matching, so the pooled row is the robust one. [SOURCE: `infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/derived/firstgen_cost_weighted.csv`]

Date: 2026-09-18. Lane: `infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/`. Extends ladder 48 (first-generation conviction and arrest rates lower) and ladder 78 (cost-weighted excess of US-born Mexican-origin adults over US-born whites), which had no first-generation arm.

## 1. Data and construction

Light, He and Robey's replication package (openICPSR 124923) carries Texas Department of Public Safety felony arrest charges 2012–2018 by year, offence category and immigration status: US-born citizens, legal immigrants (naturalized included), and the undocumented, with denominators from the Center for Migration Studies (2012–18) and Pew (2012–17), and a variant that splits legal immigrants into non-naturalized and naturalized. Status is assigned by DHS IDENT biometric matching at booking. Each row is an arrest charge, not a person or a conviction; the repo's denominator memo reproduced the 2018 violent-felony ratio of 0.457 from the same files. [SOURCE: doi:10.1073/pnas.2014704117; `immigration-conduct-denominators-2026-09-05.md` §1]

Fifteen categories. Seven carry a McCollister, French and Fang (2010) unit cost in 2024 dollars: homicide $13.1M, sexual assault $351k, aggravated assault $156k, robbery $62k, arson $31k, burglary $9.4k, theft $5.1k (published totals, CPI-U factor 1.457, the same table the crime-cost lane uses). Drugs, traffic (felony DWI), weapons, obstruction, other sex offences, kidnapping and "all other" are priced at zero in arm A; arm B prices other sex offences as sexual assault and kidnapping as aggravated assault and moves no ratio by more than 0.01. Three cost lines: criminal-justice cost only (the treasury line), tangible (victim losses, criminal-justice, offender career), and total (with pain, suffering and the statistical value of life). [SOURCE: `../infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py` MCC table]

Rates are pooled 2012–2018 charges over pooled population, per 100,000 persons per year, the paper's convention. Because immigrants have fewer children per capita than the US-born, a per-capita denominator overstates their rate relative to a per-adult one; the ACS PUMS API gives Texas adult shares of 70.2% for the US-born, 91.1% for non-citizens (the proxy for the undocumented) and 94.9% for legal immigrants, so per-adult ratios are the per-capita ratios times 0.74 to 0.77. An 18–39 arm is in the CSV. [SOURCE: ACS 2018 1-year PUMS, Texas, CIT × AGEP; `derived/audit.json`]

## 2. Results (CMS denominators, arm A)

| Group | Charges per capita | Cost-weighted, total | Cost-weighted, treasury only | Homicide charges | Sexual-assault charges |
|---|---|---|---|---|---|
| Undocumented | 0.40 (0.31 per adult) | 0.43 (0.33) | 0.41 (0.31) | 0.39 | 0.62 |
| Legal immigrants, naturalized included | 0.78 (0.58) | 1.01 (0.75) | 0.95 (0.71) | 1.04 | 1.72 |
| Foreign-born pooled | 0.63 (0.48) | 0.79 (0.59) | 0.75 (0.56) | 0.79 | 1.31 |
| Split: legal non-naturalized | 0.77 (0.59) | 1.20 (0.93) | 1.11 (0.86) | 1.25 | 2.54 |
| Split: naturalized | 0.79 (0.57) | 0.87 (0.63) | 0.84 (0.60) | 0.88 | 1.12 |

Ratios to US-born citizens; per-adult ratios in parentheses. Pew denominators reproduce every cell within 0.02. Per-year legal-immigrant sexual-assault ratios: 1.84, 2.01, 1.79, 1.61, 1.58, 1.65, 1.60; per-year undocumented homicide ratios 0.26 to 0.55. [SOURCE: `derived/firstgen_cost_weighted.csv`, `per_year_check.py` output]

The mix premium, cost ratio over count ratio, is 1.07 for the undocumented, 1.30 for legal immigrants, 1.25 for the foreign-born pooled, 1.56 for legal non-naturalized and 1.11 for the naturalized. The US-born base is $69 per person-year of criminal-justice cost, $167 tangible and $976 total, with homicide 40%, 54% and 65% of those lines. [CALCULATION]

## 3. What this does and does not say

- **The undocumented mix is ordinary.** Their ratio is 0.39 on homicide, 0.45 on the four violent categories and 0.40 overall, so cost weighting changes nothing. The channel the question proposed does not exist for this group in this record. [SOURCE: table above]
- **The legal-immigrant premium is real in the record and sits on the status boundary.** It is concentrated in the non-naturalized class, whose denominator is a residual (ACS non-citizens minus the CMS undocumented estimate) and whose numerator includes anyone with a DHS record at booking, including visa overstayers and prior deportees the CMS count would call undocumented. Moving charges across that boundary moves both the undocumented and the legal rates. The pooled foreign-born row is immune to it: 0.79 per capita and 0.59 per adult on the total-cost line. [INFERENCE from the classification rules; SOURCE: denominator memo §1]
- **The comparator is all US-born Texans.** The file has no race. Against US-born whites, whose felony rate is below the pooled native rate, every immigrant ratio rises; ladder 78's US-born Mexican-origin excess is measured against whites and is not comparable to these rows. The Mexican-born share of Texas's foreign-born is not in the file and is not asserted here. [UNVERIFIED]
- **Zero-priced categories bias both immigrant groups down.** Felony DWI carries crash victim costs that McCollister does not price; the undocumented traffic ratio (0.56) is above their all-felony ratio and the legal-immigrant ratio is 1.27, so pricing it would raise both. [INFERENCE]
- **Arrest charges, not offences.** Reporting, detection, charging and clearance all sit between an offence and a charge; the homicide memo's clearance conditioning (white victims 84% cleared, Hispanic 64%) applies. Charges per person are also not persons per charge. [SOURCE: ladder 143]

## 4. Disconfirmation attempted

Pew denominators, the naturalized split, arm B pricing, per-adult and 18–39 standardisation, and per-year stability were run; none reverses a row. The one test not available is the same weighting on convictions: Cato's Texas conviction series by offence (2013–2022) reports lower homicide and sexual-assault conviction rates for illegal immigrants than for natives, consistent with the undocumented row, and does not publish a legal-non-naturalized split at the offence level in a form on disk. [SOURCE: ladder 48; `immigration-crime-rates-unauthorized-vs-native-born.md` §Cato]

## Sources

Light, He & Robey 2020, PNAS 117(51), doi:10.1073/pnas.2014704117, replication package openICPSR 124923 (local copy under `~/research-data/immigration-fiscal/data/external/crime_frontier/light_texas/`). McCollister, French & Fang 2010, Drug Alcohol Depend 108(1–2):98–109. ACS 2015 and 2018 1-year PUMS via api.census.gov. Instrument note: LLM-assisted; every number above is reproduced by the scripts named in the lane README.


## Revisions — September 19, 2026

Corrected the interpretation at the point of reuse; original calculations and evidence are retained. See the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md) and linked audit for the claim-specific reason.

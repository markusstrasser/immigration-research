---
date: 2026-09-05
concept: recent-arrival-comparability
status: adopted-for-this-analysis
relations:
  complements: 2026-09-05-material-inference-repair
  qualifies: 2026-09-05-person-donor-support
---
# 2026-09-05: Separate recent-entry profiles from stock fiscal transport

## Context

The user asked whether natives contribute more than Mexicans and whether newer arrivals make older immigration findings inapplicable. Existing recipients included only white natives, although the native SIPP donors already covered all natives. The 2024 national ACS raw files were present on the SSD; a verified 2019 baseline was missing. Birthplace, legal status, entry year and religion answer different questions.

## Alternatives considered

1. Reuse the old white-native/Mexico ratio: wrong comparator for all natives.
2. Apply stock SIPP donor means to recent2024 recipients: adds unvalidated duration/period transport.
3. Compare old and new arrivals within2024: confounds duration with cohort.
4. Compare equal entry windows across2019/2024, then standardize duration/age/sex: directly measures resident differences, still not policy causation.
5. Use border encounters, court cases or LPR awards as the new resident denominator: incompatible events/status transitions and selection.
6. Generalize from salient Somali/refugee cases: lacks the population denominator and confuses outcomes/programs.

## Decision

Extend the **2023 stock partial account** to all natives without changing the warehouse, and compare its payroll component against observed ACS earnings under the same formula. Report civilian noninstitutionalized recipient sensitivity because that better matches the SIPP target universe. Do not present a full fiscal sign or origin-specific causal estimate.

Use **2019 entries2016–19 versus2024 entries2021–24**, ages25–64, employment per adult and earnings including zeros/losses. Preserve all80 replicate weights and their covariance within a survey. Apply verified R-CPI-U-RS common-dollar factors, then a1–3-year-entry sensitivity with equal duration or age×sex×duration weights. Those fixed weights define a synthetic comparison population. Keep surviving residents distinct from arrivals and nationality distinct from beliefs/conduct.

## Evidence

The [cohort analysis](../research/immigration-cohort-clarity-2026-09-05.md) calculates all-native partial balance$3,707.56 versus Mexico-born$2,370.97; the gap is driven by payroll rather than greater selected transfers to Mexico-born adults. The newer cohort has higher employment and lower real earnings; both directions survive the fixed demographic/duration sensitivity. Recent Mexican education and earnings improve. Somalia-born people are0.104% of the measured all-age recent cohort, with only30 sampled people.

Official PUMS record/population and non-controlled SDR anchors reproduce. Independent raw-sample calculations and four statistical/window tests pass. Source release constraints and targeted X evidence are in the linked availability/narrative memos. These are descriptive and model-conditional results, not identification of an administration's effect.

## Revisit if

New ACS/SIPP releases, a valid admission/work-authorization link, differential survey-coverage evidence, cohort attrition data or a defensible external policy shock changes the measured population or identifies a causal comparison. Re-estimate a full ledger only with compatible components and explicit uncertainty; use the measured partial gap as an omitted-component break-even threshold, not a full-fiscal verdict.

## Supersedes

The all-native answer supersedes use of the white-native comparator for that question. No central research question, causal tree, constitutional rule or canonical warehouse is changed. The dataset register's earlier claim that synthetic cohorts remove the cohort-quality confound is explicitly qualified.

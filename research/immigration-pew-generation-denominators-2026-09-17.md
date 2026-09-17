# Pew generations: language, American identification and political denominators

**Verdict:** Seven independent Pew surveys show large generation differences in reported English proficiency, and three show increasing perceived similarity to a typical American. Democratic identification does not rise monotonically across generations. Its first-to-second-generation ordering reverses when the denominator changes from all respondents to those reporting a major-party affiliation. These describe selected survey groups; they do not identify causal assimilation, ancestry-complete populations or convergence with non-Hispanic whites. [SOURCE: primary supplied SAVs/questionnaires; [generator](../infra/immigration-fiscal/new_datasets_2026_09_17/pew/harmonize.py), independently checked [aggregate output](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/generation_outcomes.csv).]

## Scope and classification

The 2011, 2012, 2013 religion, 2014, 2015, 2016 and 2018 surveys contain 14,116 records. This is a count of survey records, not verified unique individuals across years. Each samples self-identified Latino adults; the 401-person nonidentifier supplement remains separate and belongs to the previously analyzed 2015–2016 ancestry calibration. No respondent-ID joins across surveys are made. The 2013 analysis uses the full-sample `totalwt`, which addresses its oversampling of non-Catholics and non-Mexicans, rather than a questionnaire-form weight. [SOURCE: packaged methodology, [comparability and eight-input coverage](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/comparability.csv).]

G1 means respondent born outside the US/Puerto Rico according to the geographic item; G2 means respondent born there with at least one parent born elsewhere; G3+ means respondent and both parents born there. Citizenship at birth abroad is not measured by this classification. One known foreign-born parent establishes G2; one known US-born parent plus an unknown parent does not establish G3+. A separate sensitivity treats Puerto Rico as a migration origin. Neither scheme identifies Mexican-specific grandparent birthplace or genetic ancestry. [SOURCE: direct own/mother/father birthplace value labels in [verification metadata](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/verification.json).]

## Language and perceived American similarity

Across the seven surveys, the share reporting that they converse in English **very well** is 22.2–27.8% for G1, 77.0–83.7% for G2, and 74.5–88.7% for G3+. These are ranges across survey-year point estimates, not confidence intervals. G3+ falls below G2 in 2011 and 2014 under the main definition; treating Puerto Rico as a migration origin changes that ordering. The large G1–G2 difference persists in every survey under both definitions. The direct four-option proficiency question is used throughout, not interview language or an inconsistent composite. [SOURCE: `generation_outcomes.csv`, `english_very_well`, valid-response weighted percentages.]

The same typical-American question is available in three surveys:

| Survey | G1 valid / total; weighted % | G2 valid / total; weighted % | G3+ valid / total; weighted % |
|---|---:|---:|---:|
| 2011 | 662/728; 35.56% | 212/219; 63.02% | 254/265; 68.66% |
| 2013 | 2,587/2,865; 39.78% | 871/900; 63.82% | 1,221/1,288; 69.57% |
| 2015 | 713/790; 37.11% | 312/330; 65.99% | 344/356; 72.35% |

The ordering persists under both Puerto Rico conventions and the age/sex composition sensitivity. It measures perceived similarity to a typical American; it does not establish patriotism, loyalty, trust, democratic values or exclusive American identification. [SOURCE: direct question and generated tables.]

## Party identification: denominator reversal

Reported Democratic identification or leaning among all respondents is higher in G2 than G1 in all seven surveys. G3+ is below G2 in six of seven under the main definition, with 2011 the retained counterexample. Under the Puerto-Rico-as-migration definition it is below G2 in all seven. Small adjacent-generation gaps are not asserted to be statistically distinguishable. [SOURCE: `generation_outcomes.csv`, `dem_all`; all seven rounded published toplines reproduce.]

For a sharper denominator check, use only the five 2013–2018 surveys with the later party wording and the same 10,759 records with known generation, age band and sex. Normalize each survey's weights to sum to one on this base **before** party-response conditioning. This is an equal-survey mixture, not a pooled population-year national estimate. [SOURCE: [denominator audit](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/denominator_audit.csv).]

| Generation | Base n | Reported D/lean-D n | Reported R/lean-R n | Residual n | Weighted reported D / all | Weighted D / (D+R) |
|---|---:|---:|---:|---:|---:|---:|
| G1 | 5,913 | 3,415 | 1,080 | 1,418 | 55.89% | 75.05% |
| G2 | 2,121 | 1,289 | 524 | 308 | 61.04% | 71.93% |
| G3+ | 2,725 | 1,613 | 718 | 394 | 56.97% | 67.00% |

Counts are unweighted; they are not the numerators of the weighted percentages. The raw G2–G1 comparison is **+5.15 percentage points** on reported D/all and **−3.13 points** on D/(D+R). Both use the same initial sample and base weights. This is a change of estimand, not proof that unknown respondents oppose Democrats. The arithmetic identity is:

`reported D / all = reported (D + R) / all × D / (D + R)`.

G2 has a larger reported major-party share but a smaller Democratic share conditional on reporting a major party. The residual category includes explicit neither/other, don't know and refusal; these remain separately tabulated where the instrument permits, and the 2013 combined category cannot be split. [SOURCE: [party residuals](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/party_residuals.csv); [independent arithmetic verifier](../infra/immigration-fiscal/new_datasets_2026_09_17/pew/verify_harmonized.py).]

Descriptive survey-year controls give +5.28 and −3.16 points; adding age-band/sex controls gives +5.89 and −3.01. Restricting to reported Mexican origin also retains the reversal. These regressions do not identify a causal generational effect; conditioning on major-party reporting can itself change selection. We show raw same-base arithmetic first so the result does not depend on a model specification. [SOURCE: [composition sensitivities](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized/composition_sensitivity.csv).]

The earlier **58.67%** Democratic estimate for NSL2015 used valid composite categories. Among all respondents the result is **55.86%**, matching Pew's published rounded 56%; among D/R identifiers or leaners it is **73.04%**. These are three denominators applied to the same survey, not incompatible facts. Any reuse of ladder107 must carry its valid-category denominator. [SOURCE: supplied NSL2016 questionnaire/topline, lines2662–2694; direct reconstruction of 2015 composite membership.]

## What the analysis changes

The strongest supported interpretation is that language, perceived American similarity and party attachment are distinct dimensions. An undifferentiated claim of persistent nonassimilation is inconsistent with the language and similarity measurements. Conversely, the measured gradients do not establish convergence on every civic, fiscal or crime outcome. [INFERENCE]

The principal competing explanation for group differences is composition: age/cohort, origin mix, citizenship, arrival age and continued Latino self-identification. Within-year comparisons, Puerto Rico alternatives and the Mexican-origin sensitivity address parts of this explanation; they do not remove it. No design-based standard errors or equivalence tests are claimed. Kish effective sample sizes measure weight concentration, not cluster/stratum uncertainty. [METHOD; source tables carry valid n, excluded weight and effective n.]

**Discriminating evidence:** comparable questions in a family-history-defined sample including nonidentifiers and a same-year non-Hispanic-white benchmark, with arrival/citizenship information and survey design variables. Disappearance or reversal there would undermine a broad population or trajectory interpretation. The next action for these data is to preserve separate outcomes and explicit denominators, not select whichever denominator supports a preferred political story. [INFERENCE]

LLM instrument check: politically congenial and inconvenient patterns were retained, including the 2011 partisan counterexample and both denominator signs. The evidence is the source coding and reproducible arithmetic; an AI narrative adds no independent support. No fiscal or crime result is inferred from these attitude measures. [METHOD]

## Reproduction

From the repository root:

```bash
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/harmonize.py --lane-dir infra/immigration-fiscal/new_datasets_2026_09_17 --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/pew/verify_harmonized.py --output-dir infra/immigration-fiscal/new_datasets_2026_09_17/derived/pew_harmonized
```

Validation: all seven survey sizes and primary rounded party benchmarks; all six supplied party composites; explicit birthplace and proficiency coding; preserved unknown parents; both Puerto Rico conventions; partition sums; same-base weighted denominator arithmetic; weighted-regression normal equations. All pass. The other substantive questions in the eight surveys were not tested by this bounded lane; their presence is not evidence for a conclusion.

# PIAAC adult skills among later-generation degree holders

**Verdict:** The final adult-skills check is inconclusive. Hispanic BA-or-higher holders have lower literacy and numeracy point estimates than non-Hispanic-white holders in both separately analyzed releases, but all four main approximate 95% intervals include zero. BA-only and age/sex-adjusted checks remain inconclusive. This is weak directional consistency with unequal skills behind equal credential labels, not a precise adult skill-gap estimate or evidence of equivalent skills. Further subdivision of these public samples has diminishing returns. [SOURCE: derived/piaac/means.csv, contrasts.csv]

## Population and outcome

Both releases restrict to household adults **ages 25–65**, US-born themselves and reporting that both the mother/female guardian and father/male guardian were US-born. Compare self-identified Hispanic respondents of any race with non-Hispanic-white respondents. BA+ is highest credential EDCAT8 6–8; BA-only is exactly 6. Associate/professional ISCED5B code5 is excluded. Missing birthplace is not assigned to US-born. [SOURCE: held 2016667REV_codebook.pdf, printed pp376 and1354; exact coding in analyze_piaac.py]

This is a generic later-generation proxy using parents/guardians. The public files do not identify Mexican ancestry, distinguish third from fourth generation, or recover ancestry nonidentifiers. The age-band endpoint includes age65. The restriction does not prove that every qualification was earned in the US. [SOURCE: primary field definitions for J_Q04A/J_Q06A/J_Q07A, RACETHN_5CAT and AGEG5LFSEXT; [US background questionnaire](https://nces.ed.gov/surveys/piaac/2014-en-household-bq.html)]

Outcomes are adult literacy and numeracy **score points on the PIAAC 0–500 scales**, assessed in English. They are not ASVAB percentiles, IQ points, institution rankings, or measures of learning caused by a particular school. English/Spanish background interviews do not change the English-only assessment. Age, field of study, later skill use and language exposure can influence these skills independently of institutional quality. [SOURCE: [NCES handbook](https://nces.ed.gov/StatProg/handbook/pdf/piaac.pdf); INFERENCE for causal interpretation]

## Primary estimates

Differences are Hispanic minus non-Hispanic white. The 2012/14 file is the official combined national household sample. The separate 2017 sample is analyzed independently, with no concatenation, assumed cross-release covariance, or pooled effect estimate. [SOURCE: raw releases and source hashes in derived/piaac/audit.json]

| Release | Outcome | Hispanic mean | White mean | Difference | Approximate 95% interval |
|---|---|---:|---:|---:|---:|
| 2012/14 | Literacy | 301.27 | 311.85 | −10.58 | [−26.35, +5.19] |
| 2012/14 | Numeracy | 296.02 | 302.05 | −6.02 | [−25.11, +13.06] |
| 2017 | Literacy | 302.96 | 309.16 | −6.20 | [−17.35, +4.95] |
| 2017 | Numeracy | 287.03 | 299.53 | −12.50 | [−26.44, +1.45] |

Every mean uses the final survey weight and all ten domain plausible values; differences and their uncertainty are computed jointly rather than treating group estimates as independent. [SOURCE: derived/piaac/means.csv, contrasts.csv]

| Release | Hispanic BA+ n / Kish effective n | White BA+ n / Kish effective n | Hispanic BA-only n |
|---|---:|---:|---:|
| 2012/14 | 32 / 24.15 | 1,100 / 873.84 | 21 |
| 2017 | 28 / 22.66 | 640 / 506.88 | 22 |

All selected degree holders have all ten literacy and numeracy values. Kish n describes unequal weights only; it is **not** the variance estimator or full design-adjusted sample size. The largest Hispanic respondent weight is 8.28% of the BA+ group in 2012/14 and 7.74% in 2017. These are small, selected domains even though the full releases contain 8,670 and3,660 respondents. [SOURCE: derived/piaac/means.csv and audit.json]

## Prespecified checks

Before viewing the outcome estimates, the computation specified BA-only sensitivity and a descriptive age/sex adjustment. The latter is a weighted linear projection on Hispanic status, female status, and indicators for the five-year age bands (terminal band60–65), recomputed under every plausible value and replicate weight. It assumes a common additive Hispanic coefficient across these covariates; it is not a causal effect or a nonparametric matched-sample comparison. No selected respondent lacks sex, and all fitted full/replicate design matrices have full rank. [SOURCE: analyze_piaac.py; derived/piaac/adjustment_support.csv]

| Release | Credential / adjustment | Literacy difference [approximate95% interval] | Numeracy difference [approximate95% interval] |
|---|---|---:|---:|
| 2012/14 | BA+; age/sex adjustment | −14.09 [−28.62, +0.44] | −10.27 [−27.17, +6.63] |
| 2017 | BA+; age/sex adjustment | −6.21 [−16.89, +4.46] | −11.13 [−24.46, +2.20] |
| 2012/14 | BA-only; unadjusted | −7.05 [−26.20, +12.11] | −3.46 [−28.65, +21.72] |
| 2017 | BA-only; unadjusted | −2.97 [−16.69, +10.75] | −9.89 [−27.05, +7.27] |
| 2012/14 | BA-only; age/sex adjustment | −9.22 [−26.19, +7.75] | −5.91 [−29.34, +17.52] |
| 2017 | BA-only; age/sex adjustment | −3.55 [−15.48, +8.39] | −8.20 [−23.68, +7.28] |

None resolves the uncertainty. The correlated outcomes and overlapping credential/adjustment checks are not sixteen independent confirmations. No equivalence margin was specified, and absence of a clear difference is not an equivalence result. [SOURCE: derived/piaac/contrasts.csv; INFERENCE]

## Methods and validation

For each of ten plausible values, the full-weight mean or difference is recomputed with SPFWT1–SPFWT45. The JK2 sampling variance is the **sum**, not the average, of squared replicate deviations. Average these ten sampling variances and add 1.1 times the sample variance of the ten full-weight estimates. The resulting SE accounts for both survey sampling and plausible-value uncertainty. The 35 additional nominal replicate columns are not additional independent replicates. [SOURCE: [2012/14 technical report](https://nces.ed.gov/pubs2016/2016036.pdf), §8.3, for JK2; [NCES2020225](https://nces.ed.gov/pubs2020/2020225.pdf), §3.1 equations3b–3e, for PV pooling]

Reported intervals are **approximate, pointwise normal intervals**, estimate±1.96SE. Exact small-domain/PV-adjusted degrees of freedom were not established. Fixed-t45 columns in the machine export are only an illustrative widening, not certified NCES finite-sample intervals. They do not change the inconclusive assessment. No multiple-outcome adjustment is claimed. [SOURCE: method verification; [NCES technical notes](https://nces.ed.gov/surveys/piaac/2023/technical_notes.asp), Statistical Procedures; INFERENCE]

The principal national checks apply the same age25–65 restriction but no degree, birthplace, or race restriction. The calculations reproduce **both means and SEs** at official published rounding:

| Release / outcome | Reproduced mean (SE) | Published mean (SE) |
|---|---:|---:|
| 2012/14 literacy | 271.39098 (1.00565) | 271 (1.0) |
| 2012/14 numeracy | 257.94414 (1.17386) | 258 (1.2) |
| 2017 literacy | 270.55591 (1.30248) | 271 (1.3) |
| 2017 numeracy | 255.03939 (1.44104) | 255 (1.4) |

Published sources: [Digest2018 Table507.15](https://nces.ed.gov/programs/digest/d18/tables/dt18_507.15.asp), [Digest2019 Table507.15](https://nces.ed.gov/programs/digest/d19/tables/dt19_507.15.asp). Cases without proficiency values are excluded consistently; no arbitrary scores are assigned to literacy-related nonrespondents. A failed benchmark stops the code before subgroup estimation. [SOURCE: derived/piaac/benchmarks.csv]

Independent verification reads the original SAS archive and CSV, imports no analyzer functions, uses scalar weighted sums and pivoted-QR regression instead of the analyzer's matrix sums/normal equations, and reproduces all16 means,16 contrasts,4 benchmarks and16,560 full/replicate/PV estimates. The largest scalar discrepancy is1.17e-10. A separate national BA+ check also matches published literacy304(SE1.6) and numeracy295(SE1.8) for2012/14. This validates the arithmetic and credential coding, not exact small-domain interval coverage. [SOURCE: verify_piaac.py; derived/piaac/verification.json; [Digest2016 Table507.15](https://nces.ed.gov/programs/digest/d16/tables/dt16_507.15.asp)]

Reproduce from the repository root with cached dependencies:

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --no-project --with pandas --with scipy python3 infra/immigration-fiscal/education_quality_2026_09_20/analyze_piaac.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --no-project --with pandas --with scipy python3 infra/immigration-fiscal/education_quality_2026_09_20/verify_piaac.py
```

The original inputs remain read-only in the sibling project. Source paths/hashes, full replicate/PV estimates, selected source extracts, population composition and regression support are regenerated under ignored `derived/piaac/`. The pooled2012/14 national codebook was inspected; the separate2017 codebook download remained incomplete. Shared Cycle1 definitions, actual field support/design metadata, and independent2017 benchmark replication support this computation; this is not a claim of a complete standalone2017 codebook audit. [SOURCE: acquisition/field audit; generated audit.json]

## Stopping decision

The [earlier NLSY result](RESULT.md) remains a selected adolescent-preparation comparison among later Mexican-identifying graduates. PIAAC tests a broader Hispanic population over a wider age range with adult literacy/numeracy scales. It neither exactly replicates nor overturns NLSY. It supplies directional evidence with insufficient precision to settle the adult contrast. Neither study establishes university teaching quality or a complete Mexican-descendant denominator. [INFERENCE from the two executed comparisons]

Close this public-data avenue after the authorized PIAAC check. Reopen only for a materially larger sample measuring ancestry independently of current identity and recording relevant skills or degree-awarding institutions, or a clearly relevant published analysis. More subgroup slicing of these files cannot create the missing information. See [decision record](../../../decisions/2026-09-20-close-degree-quality-avenue.md). [INFERENCE]

Instrument check: LLM-assisted analysis was constrained by primary definitions, published mean/SE benchmarks, declared sensitivity checks and independent arithmetic. Both a gap and equality remain compatible with parts of the observed uncertainty; the conclusion does not promote either to a settled group claim. [INFERENCE]

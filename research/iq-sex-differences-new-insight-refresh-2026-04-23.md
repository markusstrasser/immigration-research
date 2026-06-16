# IQ Sex Differences - New Insight Refresh

**Date:** 2026-04-23  
**Question:** Is there any new insight into the intelligence sex-differences debate after the current repo evolution, local memos, and recent literature?
**Tier:** Deep  

## Bottom Line

Yes, but not as a new "men are smarter" or "women are smarter" headline.

The best new insight is that the debate should now be split into three different estimands that popular arguments keep collapsing:

1. **manifest composite advantage** - what a published full-scale or achievement composite says
2. **latent trait advantage** - what survives after factor modeling / invariance discipline
3. **surface-family advantage** - whether the observed gap lives in evaluation, school knowledge, applied/reasoning, spatial/matrix, speed/process, or adult accumulation

The new 2026 pro-male meta-analysis is useful because it strengthens the adversarial case for a small adult male manifest-composite advantage, but it does **not** resolve the latent-`g` question. Its own discussion concedes that latent-method studies often point to no difference or female-favoring results. [SOURCE: https://openpsych.net/files/submissions/11_Meta-analysis_of_sex_differences_in_intelligence.pdf; DOI: `10.26775/OP.2026.03.10`]

So the repo's stronger position is not weakened. It becomes sharper:

> A small male adult full-scale/composite advantage may be real on some manifest batteries, while a battery-independent latent-`g` advantage remains unproven; the real structure is a surface-family decomposition.

[INFERENCE]

## Claims Table

| # | Claim | Evidence | Confidence | Status |
|---|---|---|---:|---|
| 1 | The 2026 OpenPsych meta-analysis is a serious adversarial datum for a small adult male manifest-composite advantage, but not decisive for latent `g`. | Adult full-scale result is male-favoring; latent-method issue is explicitly bracketed and admitted unresolved. [SOURCE: OpenPsych PDF, DOI `10.26775/OP.2026.03.10`] | 0.70 | VERIFIED AS ADVERSARIAL DATUM |
| 2 | The repo should distinguish "manifest full-scale ability" from "latent `g`" more explicitly than before. | OpenPsych's strongest finding is manifest/high-quality full-scale pooling; local repo already has mixed latent findings and weighted HSLS two-factor evidence. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`] | 0.78 | INFERENCE |
| 3 | PISA 2022 is now the best public replication target for the repo's PISA 2018 process/DIF branch. | OECD exposes cognitive item files and questionnaire timing files; the three public SPSS archives are now staged locally and pass zip validation. [SOURCE: https://webfs.oecd.org/pisa2022/index.html; DATA: `sources/iq-sex-diff/data/pisa2022/ACQUIRED.md`] | 0.86 | VERIFIED |
| 4 | The Italy/INVALSI 2009-2023 paper adds a useful "amplifier" frame: high-achievement contexts may magnify whichever sex is already ahead in the domain. | Province/year meta-analysis finds higher mean achievement associated with larger boys' math advantage and girls' reading advantage. [SOURCE: https://icajournal.scholasticahq.com/article/155775.pdf] | 0.65 | USEFUL BUT SECONDARY |
| 5 | Local latent work now makes the "surface-family" claim stronger than the March frontier memo did. | Weighted HSLS lavaan rejects one school-math factor and supports tested-vs-evaluation factors; Add Health shows grade-family heterogeneity without obvious weaker female predictive returns. [SOURCE: `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`; `research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md`] | 0.78 | HARDENING |
| 6 | The newest evolutionary frame supports multidimensional decomposition more than a one-number sex ranking. | Geary 2026 frames cognition as evolved, developmentally modulated networks and explicitly points to sex differences in fluid abilities, variance, and large-scale-network organization. [SOURCE: https://icajournal.scholasticahq.com/article/154815.pdf] | 0.62 | THEORY-SUPPORTED INFERENCE |
| 7 | The most robust adult-ish specific-ability datum remains mental rotation, not global intelligence. | A 2026 systematic review/meta-analysis of post-2010 mental-rotation studies reports male advantage `d = 0.60`, with heterogeneity and test-format dependence. [SOURCE: https://doi.org/10.1177/17470218261419079] | 0.80 | VERIFIED SPECIFIC-ABILITY DATUM |
| 8 | PISA 2022 raw public plausible values replicate the expected surface-family split: boys lead math overall, girls lead reading strongly, science is near-null, and math subscale gaps are largest on space/shape and formulating. | Local `STU_QQQ_SPSS.zip` pass: math female-minus-male `-6.37` points, reading `+20.59`, science `-1.23`; `MCSS -10.99`, `MPFS -11.37`. [DATA: `sources/iq-sex-diff/data/pisa2022/pisa2022_pv_gender_summary.tsv`] | 0.86 | RAW PUBLIC-DATA PASS |
| 9 | The public PISA 2022 cognitive and timing files are not just nominally available; their metadata exposes the needed item/process surface for the next test. | Local metadata probe: `STU_COG` has `5,023` columns including `417` math, `1,266` reading, and `694` science cognitive item/process columns; `STU_TIM` has `154` questionnaire timing columns. [DATA: `sources/iq-sex-diff/data/pisa2022/pisa2022_metadata_probe.txt`] | 0.84 | ACQUIRED / METADATA-PROBED |

## New External Evidence

### 1. 2026 OpenPsych meta-analysis: useful, not decisive

The new paper reports a male adult full-scale/general-ability advantage in its preferred adult analysis and argues that this likely reflects `g`. [SOURCE: https://openpsych.net/files/submissions/11_Meta-analysis_of_sex_differences_in_intelligence.pdf; DOI: `10.26775/OP.2026.03.10`]

Reasons to treat it as an adversarial datum rather than a canonical update:

1. The search process was not formally tracked. [SOURCE: OpenPsych PDF]
2. Heterogeneity remains very high in the preferred full-scale adult analysis. [SOURCE: OpenPsych PDF]
3. Only a tiny share of effect sizes are latent estimates; the paper says latent differences were accepted, but latent calculation was used in only `2.8%` of cases. [SOURCE: OpenPsych PDF]
4. The authors explicitly say whether the full-scale difference is due to `g` is unclear, then lean on priors. [SOURCE: OpenPsych PDF]
5. They also acknowledge that latent-method studies tend to suggest no sex difference or female-favoring results. [SOURCE: OpenPsych PDF]

Interpretation: it raises the pressure on any too-confident "strict null" claim, but it does not defeat the repo's battery-independent skepticism. [INFERENCE]

### 2. Italy/INVALSI 2026: achievement context as amplifier

The new Italy paper uses INVALSI population-level assessments across grades, provinces, and years through 2023. It reports the familiar male math / female reading pattern, but the useful addition is moderator structure:

- higher overall provincial achievement is associated with a larger boys' math advantage
- higher overall achievement is also associated with a larger girls' reading advantage
- female university enrollment shifts the balance toward girls
- the authors caution against transporting the result to more homogeneous or non-tracked systems

[SOURCE: https://icajournal.scholasticahq.com/article/155775.pdf]

Interpretation: this is not direct intelligence evidence, but it is a strong warning against a simple "better environment eliminates gaps" story. Better contexts may amplify domain strengths, while institutional paths can shift observed achievement in sex-specific ways. [INFERENCE]

### 3. PISA 2022: a live replication target

OECD's PISA 2022 database exposes public student questionnaire, cognitive item, and questionnaire timing data files. [SOURCE: https://www.oecd.org/en/data/datasets/pisa-2022-database.html; https://webfs.oecd.org/pisa2022/index.html]

Probe results:

| File | URL | Size | Status |
|---|---|---:|---|
| Cognitive item SPSS | `https://webfs.oecd.org/pisa2022/STU_COG_SPSS.zip` | `480,779,795` bytes | acquired / zip-valid |
| Questionnaire timing SPSS | `https://webfs.oecd.org/pisa2022/STU_TIM_SPSS.zip` | `218,079,470` bytes | acquired / zip-valid |
| Student questionnaire SPSS | `https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip` | `682,364,259` bytes | acquired / zip-valid |
| Cognitive item SAS | `https://webfs.oecd.org/pisa2022/STU_COG_SAS.zip` | `687,940,075` bytes | live |

[DATA: `curl -I -L` probes run 2026-04-23]

This matters because the local PISA 2018 branch is close to saturation. The best public replication is no longer "another 2018 process regression"; it is:

1. port the PISA 2018 item-family / response-time pipeline to PISA 2022
2. test whether the `space_shape`-style content-family residual survives the revised 2022 math framework
3. test whether the timing/process decoupling replicates
4. use official 2022 process/content subscales as a bridge

[INFERENCE]

### 4. Evolutionary frame: useful if it is kept dimensional

Geary's 2026 evolutionary framework is the most useful recent "evolution" source I found, but only if it is not over-read. It argues for studying intelligence across multiple evolved functions, development, neural-network organization, and gene/environment pathways; it also says the evolutionary approach gives insight into sex differences in cognition, including fluid abilities, variance, and differential `DMN` / `FPN` organization. [SOURCE: https://icajournal.scholasticahq.com/article/154815.pdf]

This does **not** license a clean conclusion that one sex has higher global intelligence. It does license a stronger prior that sex differences, where real, should be uneven by surface and mechanism:

- spatial / mental-rotation surfaces can show a male advantage
- processing speed / schooling / evaluation surfaces can show different patterns
- context and development can amplify or dampen observed gaps
- latent `g` can stay hard to adjudicate because batteries mix these surfaces differently

[INFERENCE]

That makes the evolutionary update a point for the repo's decomposition model, not a replacement for it.

### 5. Specific ability update: mental rotation remains the cleanest large surface

The 2026 mental-rotation systematic review/meta-analysis identified `41` relevant post-2010 studies and `59` effect sizes, reporting a male advantage of `d = 0.60` with `95% CI [0.54, 0.67]`. It also reports substantial heterogeneity and says the classic `MRT` produced the greatest effect size. [SOURCE: https://doi.org/10.1177/17470218261419079]

Interpretation: this strengthens the "some cognitive surfaces are genuinely sex-differentiated" side of the debate. It does not settle global intelligence because mental rotation is a specific spatial surface, and the effect partly depends on task format. [INFERENCE]

### 6. PISA 2022 official gender summary: tail asymmetry matters

The OECD's official PISA 2022 report gives a useful public-data bridge and a check on the local raw-file pass:

- boys outperformed girls in mathematics by `9` score points on average across OECD countries
- boys outperformed girls in math in `40` countries/economies; girls outperformed boys in `17`
- among the weakest-performing `10%`, girls outperformed boys by `4` points on average across OECD countries
- no country/economy had a larger share of girls than boys among top math performers

[SOURCE: https://www.oecd.org/en/publications/pisa-2022-results-volume-i_53f23881-en/full-report/equity-in-education-in-pisa-2022_4008c06e.html]

Interpretation: this is exactly the kind of non-Gaussian surface evidence the repo should track. The mean and the upper tail point male in math, while the lower tail is not simply "boys better everywhere." [INFERENCE]

### 7. PISA 2022 raw plausible-value pass: the subscale geometry replicates the decomposition frame

After confirming SSD access, I staged the public `PISA 2022` student questionnaire SPSS archive and ran a first descriptive plausible-value pass. [DATA: `sources/iq-sex-diff/data/pisa2022/ACQUIRED.md`]

Script:

- [pisa2022_pv_gender_pass.py](/Users/alien/Projects/research/sources/iq-sex-diff/pisa2022_pv_gender_pass.py)

Outputs:

- [pisa2022_pv_gender_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa2022/pisa2022_pv_gender_summary.tsv)
- [pisa2022_pv_gender_country.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa2022/pisa2022_pv_gender_country.tsv)

First-pass weighted descriptive results:

| scale | female-minus-male points | female-minus-male d |
|---|---:|---:|
| `MATH` | `-6.37` | `-0.064` |
| `READ` | `+20.59` | `+0.186` |
| `SCIE` | `-1.23` | `-0.012` |
| `MCSS` space/shape | `-10.99` | `-0.100` |
| `MPFS` formulating | `-11.37` | `-0.103` |
| `MCUD` uncertainty/data | `-2.62` | `-0.024` |
| `MPIN` interpreting/evaluating | `-3.09` | `-0.029` |

Country-level direction checks:

| scale | countries | male-favoring | female-favoring | median gap |
|---|---:|---:|---:|---:|
| `MATH` | `80` | `56` | `24` | `-6.18` |
| `MCSS` | `76` | `65` | `11` | `-10.33` |
| `MPFS` | `76` | `65` | `11` | `-11.10` |
| `READ` | `80` | `0` | `80` | `+25.36` |
| `SCIE` | `80` | `33` | `47` | `+1.77` |

This is not a latent-`g` adjudication. It is stronger than the official narrative summary for the repo's purpose because it shows where the math gap sits inside the 2022 public subscales: `space_shape` and `formulating` are the largest male-leaning surfaces, while `uncertainty_data` and `interpreting/evaluating` are much closer to null. [INFERENCE]

Limit: this first pass uses final student weights and averages across plausible values. It does not yet use replicate weights for sampling variance, nor does it touch the cognitive item/process files. [DATA]

### 8. PISA 2022 cognitive/timing metadata: the next test is now concrete

The remaining replication task is no longer blocked on acquisition. The local metadata probe confirms:

| file | columns | relevant exposed surface |
|---|---:|---|
| `STU_QQQ_SPSS.zip` | `1,278` | `110` plausible-value columns, `80` replicate weights |
| `STU_COG_SPSS.zip` | `5,023` | `417` math cognitive item/process columns; `1,266` reading; `694` science |
| `STU_TIM_SPSS.zip` | `172` | `154` questionnaire timing columns |

[DATA: `sources/iq-sex-diff/data/pisa2022/pisa2022_metadata_probe.txt`; SCRIPT: `sources/iq-sex-diff/pisa2022_metadata_probe.py`]

This changes the practical frontier from "can we get the public data?" to "do the PISA 2018 process/DIF findings replicate under the 2022 framework?" [INFERENCE]

## Integration With Local Repo Evolution

The repo has already moved past "measurement matters" into a stronger latent-family claim.

Key local updates:

1. Weighted `HSLS` lavaan rejects a one-factor school-math model and supports a two-factor `tested_math` / `evaluation_math` model with practical scalar comparability by sex. [SOURCE: `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`]
2. The broad bachelor-level prediction-noninvariance story weakens under scalar factor scores; the surviving STEM signal is sparse. [SOURCE: `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`]
3. Add Health public grades are coherent but too heterogeneous for a lazy one-factor evaluation scalar, and obvious female predictive discounting is not present in the pilot. [SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md`]
4. PISA 2018 public `TT/V` process data do not coherently reduce the residual content-family ordering after ability-residualized process adjustment. [SOURCE: `research/iq-sex-differences-pisa2018-process-residualized-dif.md`]
5. PISA 2022 public plausible values show a male-leaning math surface concentrated most strongly in `space_shape` and `formulating`, a strong female reading surface, and near-null science. [DATA: `sources/iq-sex-diff/data/pisa2022/pisa2022_pv_gender_summary.tsv`]
6. Open matrix-style ICAR data show a male-leaning matrix pattern that strengthens on harder/later items without a simple item-reach explanation. [SOURCE: `research/iq-sex-differences-raven-open-data.md`]

The new synthesis is therefore:

> The strongest surviving model is not "sex difference in intelligence." It is "sex-by-surface-family geometry." Manifest composites can lean male, evaluation surfaces can lean female, matrix/spatial surfaces can lean male, process speed/timing can lean female or burden female, and broad latent `g` remains unresolved because all of those surfaces enter batteries differently.

[INFERENCE]

## Disconfirmation

What would kill this new synthesis:

1. A modern, representative, multi-battery, measurement-invariant study finding the same sex difference direction across latent `g`, matrix/spatial, school-knowledge, processing-speed, and evaluation surfaces. [INFERENCE]
2. A PISA 2022 replication showing the 2018 content-family residuals disappear under the newer framework and timing/process handling. [INFERENCE]
3. Restricted transcript data showing that transcript theta fully absorbs the female evaluation-family residual and makes GPA/recommendation surfaces behave like tested math. [INFERENCE]
4. A raw representative Raven/matrix dataset showing no male hard-item gradient once exposure and completion are aligned. [INFERENCE]

The 2026 OpenPsych paper does **not** satisfy condition 1 because it is mostly a manifest-effect synthesis, not a same-sample multi-battery latent-invariance adjudication. [INFERENCE]

## Practical Next Step

The highest-value next public move is a **PISA 2022 replication packet**, not a new generic literature review.

Completed setup:

1. acquired and zip-validated `STU_COG_SPSS.zip`, `STU_TIM_SPSS.zip`, and `STU_QQQ_SPSS.zip`
2. staged them under the SSD-backed `sources/iq-sex-diff/data/pisa2022/` path
3. ran `sources/iq-sex-diff/pisa2022_pv_gender_pass.py` on `STU_QQQ_SPSS.zip` to get official plausible-value gender gaps by scale
4. metadata-probed `STU_COG` and `STU_TIM`

Minimum remaining version:

1. port the 2018 scripts:
   - `pisa2018_dif_theta_logit_pass.py`
   - `pisa2018_time_dif_theta_pass.py`
   - `pisa2018_process_residualized_dif_pass.py`
2. compare 2018 vs 2022 by official content/process family, item format, and timing residuals

Stop rule: if PISA 2022 reproduces the timing-score decoupling and residual content-family ordering, the repo can harden the public measurement branch. If it does not, the PISA 2018 branch gets demoted to a framework-specific result. [INFERENCE]

## Search And Probe Log

- Read local state: `iq-sex-differences-current-position.md`, `claim-register.md`, `novel-synthesis-roadmap.md`, `alpha-research-program.md`, `frontier-refresh-2026-03-06.md`.
- Read local post-March latent/process memos: `hsls-lavaan-weighted-pass.md`, `weighted-mtmm-sensitivity.md`, `addhealth-evaluation-invariance-pilot.md`, `pisa2018-process-residualized-dif.md`, `raven-open-data.md`.
- Searched web for 2026 intelligence / sex-difference / PISA / DIF updates.
- Inspected:
  - OpenPsych 2026 meta-analysis PDF
  - INVALSI Italy 2026 PDF
  - Geary 2026 evolutionary framework PDF
  - Hervin & Gibson 2026 mental-rotation meta-analysis
  - Nature 2025 first-grade math-gap article
  - OECD PISA 2022 database and technical pages
  - arXiv process-DIF reduction paper
- Probed PISA 2022 public file URLs with HTTP HEAD before staging.
- Staged and validated `PISA 2022` `STU_QQQ_SPSS.zip`, `STU_COG_SPSS.zip`, and `STU_TIM_SPSS.zip` to the SSD-backed data path.
- Ran `sources/iq-sex-diff/pisa2022_pv_gender_pass.py` and wrote descriptive plausible-value gender gaps for total math, reading, science, and PISA 2022 math subscales.
- Ran `sources/iq-sex-diff/pisa2022_metadata_probe.py` and wrote a metadata inventory for the staged questionnaire, cognitive item/process, and timing files.

## Bottom-Line Verdict

The new insight is a sharper fork:

- **Accept as plausible:** small adult male advantage on some manifest full-scale composites.
- **Do not accept yet:** battery-independent male latent-`g` advantage.
- **Promote:** surface-family decomposition as the main explanatory object, now backed by recent evolutionary theory, PISA 2022 raw subscale geometry, PISA 2022 tail asymmetry, and post-2010 mental-rotation evidence.
- **Next test:** PISA 2022 public replication of the PISA 2018 timing/DIF branch.

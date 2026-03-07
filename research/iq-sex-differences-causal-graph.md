# IQ Sex Differences - Narrative Map and Causal Graph

**Date:** 2026-03-05
**Question:** How should we engage the outside narratives on IQ and sex differences, and what analyses can recursively harden or soften the causal graph?

---

## Summary Position

The current evidence supports a middle position:

1. **Taleb is directionally right** about construct inflation, reification, and overclaiming from noisy psychometric summaries. [SOURCE: https://nassimtaleb.org/2019/01/iq-pseudoscientific-swindle/; https://nassimtaleb.org/2025/05/iq-pseudoscientific-swindle-argument-closed/]
2. **Cremieux is closer on the sex-differences literature itself**: means are unresolved, specifics and variability matter more than slogans, and battery/model choices can change conclusions. [SOURCE: https://www.cremieux.xyz/p/sex-differences-in-intelligence]
3. **Gwern is more curator than combatant** on this exact question. His archive is useful because the papers he hosts strongly emphasize either null overall `g` differences with specific-ability differences, or mixed results that depend on measurement. [SOURCE: https://gwern.net/doc/iq/2022-reynolds.pdf; https://gwern.net/doc/iq/2007-johnson.pdf; https://gwern.net/doc/iq/2012-irwing.pdf]
4. **Scott Alexander's angle is relevance, not psychometric adjudication**: even modest average differences can matter in tails, preferences, or institutional distributions. Useful as a check against dismissing all small differences as irrelevant; not sufficient to settle the measurement question. [SOURCE: https://slatestarcodex.com/2017/08/07/contra-grant-on-exaggerated-differences/; https://slatestarcodex.com/2017/08/01/gender-imbalances-are-mostly-not-due-to-offensive-attitudes/]
5. **Andrew Gelman's angle is measurement humility**: do not take latent constructs or predictive summary statistics more seriously than the data justify, and do not smuggle causal language into weak observational evidence. [SOURCE: https://statmodeling.stat.columbia.edu/2009/07/02/the_arthur_jens/; https://statmodeling.stat.columbia.edu/2020/01/28/are-gwas-studies-of-iq-educational-attainment-problematic/]

My stance:

- do **not** treat IQ as fake
- do **not** treat IQ as a uniquely clean measure of deep ability
- do **not** treat sex differences in overall `g` as settled
- do treat battery composition, task format, timing, and practice channels as first-order explanations to test

---

## How To Use The Narratives

### Taleb

Use Taleb as an **adversarial check against reification**.

He is strongest on:

- the gap between predictive utility and metaphysical confidence
- the over-translation from test scores to broad claims about life success
- the slippage from statistical association to causal interpretation

He is weakest when the critique becomes so broad that IQ is treated as nearly useless by default. The evidence does not support going that far. [INFERENCE]

### Cremieux

Use Cremieux as an **adversarial check against null-friendly wishful thinking**.

He is strongest on:

- not pretending the literature cleanly supports female advantage or perfect equality
- forcing attention onto variability, tails, and specific abilities
- noticing when battery construction can generate headline conclusions

He is weakest when strong social conclusions are drawn from mixed psychometric evidence before the causal graph is identified and tested. [INFERENCE]

### Gwern

Use Gwern as a **bibliographic hub**.

The most useful Gwern-hosted items for this project are:

- Reynolds et al. 2022 for the "no reliable general-intelligence gap, but real specifics" summary [SOURCE: https://gwern.net/doc/iq/2022-reynolds.pdf]
- Johnson and Bouchard 2007 for `g` masking stronger residual sex differences [SOURCE: https://gwern.net/doc/iq/2007-johnson.pdf]
- Irwing 2012 for the strongest mainstream small-male-`g` argument [SOURCE: https://gwern.net/doc/iq/2012-irwing.pdf]

I did **not** find a single clear Gwern essay staking an original polemical position on this exact dispute. [INFERENCE]

### Scott Alexander

Use Scott as a **relevance check**.

His main use here is the reminder that:

- small mean differences can still matter at tails
- differences in interests and preferences may matter even when means are close
- "the average effect is small" does not settle institutional composition

That is useful, but it does **not** resolve whether the measured cognitive differences are biological, socialized, or partly artifactual. [INFERENCE]

### Gelman

Use Gelman as a **statistical-discipline check**.

His role here is not as a substantive theorist of sex differences, but as a reminder that:

- latent constructs should not be treated as directly observed
- causal language should not be smuggled into predictive models
- psychometric elegance can outrun evidential strength

[SOURCE: https://statmodeling.stat.columbia.edu/2009/07/02/the_arthur_jens/; https://statmodeling.stat.columbia.edu/2020/01/28/are-gwas-studies-of-iq-educational-attainment-problematic/]

---

## Causal Graph

### Observation

Sex differences are larger and more stable in some **specific tasks** than in overall `g`, and the direction of composite differences changes with battery composition, timing, and scoring rules. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-timing-channels.md`]

### Null

If there is no large stable sex difference in general intelligence, then task design, practice, timing, motivation, and sample composition can produce the observed mixture of male-favoring, female-favoring, and null results. [INFERENCE]

### Graph Sketch

```text
Sex
  -> biology / hormones / development
      -> latent spatial ability
      -> fine-motor speed
      -> reaction-time / sensorimotor speed

Sex
  -> socialization / interests / practice
      -> reading-writing fluency
      -> classroom compliance / homework
      -> technical-mechanical exposure
      -> anxiety / test familiarity

Family SES / health / schooling quality
  -> nutrition / development
  -> education
  -> literacy and numeracy practice

Test design
  -> item content
  -> time bonus / strict limits
  -> subtest inclusion
  -> composite weighting

Norming / scaling
  -> observed scaled scores
  -> composite means

Selection / attrition / sample composition
  -> published group gaps

All upstream nodes
  -> observed subtest scores
  -> latent factor estimates
  -> tails / variability
  -> later education / work outcomes
```

---

## Nodes To Harden Or Soften

### Node 1 - Latent Spatial Ability Difference

**Claim:** males have a real average advantage in spatial / rotation ability that is not reducible to speed alone.

**Current lean:** harden. [SOURCE: Johnson and Bouchard 2007, https://gwern.net/doc/iq/2007-johnson.pdf; Resnick 1993, https://pubmed.ncbi.nlm.nih.gov/8424863/]

**What would harden it further:**

- unspeeded or low-speed spatial tasks still showing male advantage
- within-family replication
- cross-cultural replication with similar magnitude

**What would soften it:**

- sex gap collapsing after controlling response time, practice, and item familiarity
- no gap in low-schooling or pre-literacy samples

### Node 2 - Clerical Processing-Speed Difference

**Claim:** females have a real average advantage on clerical coding / scanning / naming tasks.

**Current lean:** harden for the tasks themselves, soften for "general speed factor." [SOURCE: Roivainen 2011, doi:10.1016/J.LINDIF.2010.11.021; Daseking et al. 2017, doi:10.1016/J.PAID.2017.04.003]

**What would harden it further:**

- replication across batteries and cohorts
- persistence after adjusting for education and literacy proxies

**What would soften it:**

- disappearance on nonclerical speed tasks
- strong mediation through reading/writing fluency or fine-motor speed

### Node 3 - Schooling / Practice / Literacy Channel

**Claim:** part of the observed female advantage on processing-speed style tasks is caused by schooling-linked practice rather than a broad latent speed factor.

**Current lean:** moderate. [SOURCE: Roivainen 2011, doi:10.1016/J.LINDIF.2010.11.021]

**What would harden it:**

- larger female gaps on letter/number/coding tasks than on reaction-time tasks
- attenuation after controlling reading volume, handwriting/keyboard fluency, homework, or grades
- stronger gaps in high-literacy and school-intensive contexts

**What would soften it:**

- same female advantage in preschool or low-literacy samples
- same female advantage on abstract nonclerical speed tasks

### Node 4 - Fine-Motor / Physiological Channel

**Claim:** part of the female advantage on coding-like tasks reflects fine-motor or neurological differences rather than literacy practice.

**Current lean:** plausible but underdetermined. [SOURCE: Roivainen et al. 2021, doi:10.1186/s40359-021-00698-0]

**What would harden it:**

- independent prediction from pegboard/fine-motor measures after literacy controls
- similar gap across cultures with different literacy practice patterns

**What would soften it:**

- mediation collapsing once literacy and schooling behavior are added

### Node 5 - Test-Design / Timing Channel

**Claim:** timing rules and subtest choice materially alter the observed sex gap.

**Current lean:** harden. [SOURCE: `research/iq-sex-differences-timing-channels.md`; Pearson WAIS-IV documentation]

**What would harden it further:**

- large difference between Block Design and Block Design No Time Bonus by sex
- cross-battery replications where adding PSI-like tasks shifts composite means

**What would soften it:**

- little change after removing timed tasks or time bonuses

### Node 6 - Norming / Composite-Weight Channel

**Claim:** composite scores can differ by sex because the battery weights broad abilities differently, even if subgroup means are not forced by norming.

**Current lean:** harden. [SOURCE: Daseking et al. 2017; `research/iq-sex-differences-timing-channels.md`]

**What would harden it:**

- FSIQ versus GAI comparisons across countries
- reweighted composites from the same raw subtests

**What would soften it:**

- similar subgroup gaps across alternative composite specifications

### Node 7 - Selection / Sample Composition

**Claim:** some observed sex gaps are partly sample artifacts.

**Current lean:** moderate. [SOURCE: Helland-Riise et al. 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11433340/]

**What would harden it:**

- comparable batteries showing different gaps in military versus civilian or volunteer versus representative samples
- evidence of sex-selective participation

**What would soften it:**

- same gaps in representative and convenience samples

### Node 8 - Life-Outcome Relevance

**Claim:** narrow subtest differences translate into meaningful productivity or success differences.

**Current lean:** soft until separately tested. [SOURCE: `notes/iq-sex-differences-context-open-questions.md`]

**What would harden it:**

- longitudinal models showing large incremental predictive power of spatial or clerical speed measures after controls

**What would soften it:**

- predictive value disappearing after broader ability, education, SES, and personality controls

---

## Dataset Inventory

### Local Acquisition Status (2026-03-05)

- `ICAR / SAPA` is local under `sources/iq-sex-diff/data/icar/`, including the
  raw CSV plus codebook and scoring-key files.
- `NLSY79` and `NLSY97` public-use cohort bundles are local under
  `sources/iq-sex-diff/data/nlsy/`.
- An extracted `ASVAB` / `AFQT` variable map now exists at
  `sources/iq-sex-diff/data/nlsy/nlsy_asvab_variables.tsv`, generated from the
  bundled SAS syntax via `sources/iq-sex-diff/extract_nlsy_asvab_vars.py`.
- `PIAAC` main public-use CSVs are local under `sources/iq-sex-diff/data/piaac/`
  for `USA`, `Germany`, `Italy`, `Finland`, `Japan`, and `Netherlands` where
  available in the initial pull.
- `PIAAC` log/process files are still missing from the local tree and remain the
  main open acquisition gap.

### Tier 1 - Public / Public-Use, Strongest Immediate Targets

1. **NLSY79 public-use data**
   - Why it matters:
     - nationally representative U.S. cohort
     - ASVAB subtests include `Coding Speed`, `Numerical Operations`, `Mechanical Comprehension`, `Auto & Shop`, verbal sections
     - many sibling pairs in-sample, enabling within-family designs
     - long-run education, earnings, jobs, marriage, fertility, health outcomes
   - Useful nodes:
     - Node 1 spatial/mechanical
     - Node 3 schooling/practice
     - Node 5 battery/task-type
     - Node 8 life outcomes
   - Access:
     - public-use via NLS Investigator
   - Sources:
     - ASVAB content: https://www.bls.gov/nls/nlsy79/topical-guide-to-data/education/aptitude-achievement-intelligence-scores.htm
     - public-use access: https://www.bls.gov/nls/getting-started/accessing-data.htm
     - sibling structure: https://www.bls.gov/nls/nlsy79/topical-guide-to-data/household/composition.htm

2. **NLSY97 public-use data**
   - Why it matters:
     - newer U.S. cohort
     - CAT-ASVAB in Round 1
     - education and labor-market outcomes through adulthood
     - supports cross-cohort comparison with NLSY79
   - Useful nodes:
     - Node 3 schooling/practice
     - Node 5 task-type stability across cohorts
     - Node 8 outcomes
   - Sources:
     - cohort overview and AFQT cross-cohort availability: https://www.bls.gov/nls/nlsy97.htm
     - CAT-ASVAB note: https://www.bls.gov/nls/getting-started/glossary.htm

3. **PIAAC Cycle 1 / Cycle 2 public-use files**
   - Why it matters:
     - adult international cognitive-assessment data
     - public-use CSV/SPSS/SAS files
     - rich education and earnings variables
   - Useful nodes:
     - Node 3 schooling and literacy channels
     - Node 7 cross-country sample composition
     - Node 8 adult outcomes
   - Sources:
     - OECD PUFs: https://www.oecd.org/en/data/datasets/piaac-1st-cycle-database.html
     - direct PUF index: https://webfs.oecd.org/piaac/index.html
     - U.S. PUF download page: https://ies.ed.gov/use-work/resource-library/data/data-file/program-international-assessment-adult-competencies-piaac-20122014-u-s-national-supplement-public

4. **PIAAC log file data**
   - Why it matters:
     - public-use process data
     - can be linked to main PUFs by `SEQID`
     - allows analysis of time-on-task, first action, and interaction counts
   - Useful nodes:
     - Node 3 practice versus speed behavior
     - Node 5 timing / process channels
   - Sources:
     - public log-file note: https://www.oecd.org/en/data/datasets/piaac-1st-cycle-database.html
     - summary of available process indicators: https://link.springer.com/chapter/10.1007/978-3-030-47515-4_10

5. **ICAR / SAPA open data**
   - Why it matters:
     - open cognitive battery with matrix reasoning, verbal reasoning, letter-number series, and 3D rotation
     - large online sample of about 97,000 participants
   - Useful nodes:
     - Node 1 spatial ability
     - Node 7 sample-composition sensitivity
   - Limitation:
     - convenience / online sample, not representative
   - Sources:
     - dataset description: https://www.scholars.northwestern.edu/en/datasets/selected-icar-data-from-the-sapa-project-development-and-initial-/
     - data paper: https://openpsychologydata.metajnl.com/article/10.5334/jopd.25/

### Tier 2 - Very Useful But With More Friction

1. **NLSY79 Child and Young Adult**
   - Why it matters:
     - intergenerational design
     - family environment and child assessments
   - Useful nodes:
     - Node 3 schooling / family effects
     - Node 8 long-run pathways
   - Source:
     - https://www.bls.gov/nls/nlsy79-children.htm

2. **Restricted NLS geocode / school files**
   - Why it matters:
     - local school and county context
     - lets us test neighborhood / school-quality channels directly
   - Useful nodes:
     - Node 3 schooling context
     - Node 7 sample and place effects
   - Source:
     - https://www.bls.gov/nls/getting-started/accessing-data.htm

---

## Immediate Analysis Agenda

For the execution order, estimands, and stop rules that turn this agenda into a
real DOE, see `research/iq-sex-differences-doe.md`.

### Analysis 1 - NLSY79 sibling fixed-effects decomposition

**Question:** within the same family, do brothers still outperform sisters on mechanical/spatial-type subtests while sisters outperform brothers on coding/clerical speed?

**Why first:** best direct attack on family-level confounding with immediate public-use feasibility.

**Output:**

- sex coefficient by subtest with family fixed effects
- tail analysis
- later earnings/occupation models by subtest profile

### Analysis 2 - NLSY79 versus NLSY97 cohort replication

**Question:** did the subtest pattern change across cohorts as schooling, literacy, and gender norms changed?

**Why:** strongest quasi-temporal test of the schooling/practice narrative.

### Analysis 3 - PIAAC main file plus log-file process indicators

**Question:** do men and women differ more in accuracy or in process behavior, and how much does education mediate those gaps?

**Why:** directly tests whether speed/process channels are separable from attained skill.

### Analysis 4 - FSIQ-style reweighting experiment

**Question:** if we reweight subtests from the same dataset, how much can the overall sex gap move?

**Why:** directly quantifies the composite-weight node.

**Need:** a dataset with enough subtests in multiple domains, ideally NLSY or ICAR open data.

### Analysis 5 - Criterion-validity check

**Question:** does clerical processing speed have meaningful incremental predictive power for earnings, occupational complexity, or status after controls?

**Why:** directly tests the popular-culture leap from subtest gap to life-success gap.

---

## Causal Check

**Most likely cause (65%):** the observed literature is generated by a mix of real specific-ability differences, schooling/practice channels, and battery-design choices, with no clean single latent-`g` story dominating all contexts. [INFERENCE]

**Top alternative (20%):** there is a true stable male advantage in general intelligence, and the rest is mostly noise or politically motivated measurement design. This is weaker because null and female-tilting findings recur in batteries and contexts that are not well explained by that simple story. [INFERENCE]

**Falsifier:** a representative, preregistered, multi-battery dataset with item-level timing and rich schooling covariates showing the same sex gap direction across reweightings, timing manipulations, and factor models. [INFERENCE]

**Decision impact:** stop arguing at the slogan layer. Move to node-by-node falsification using NLSY, PIAAC/log files, and ICAR/SAPA. [INFERENCE]

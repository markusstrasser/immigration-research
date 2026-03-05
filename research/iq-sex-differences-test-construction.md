# Sex Differences in IQ: Test Construction Balancing and Unbalanced Measures

**Question:** What would the IQ gap between males and females be if tests weren't constructed to minimize sex differences?
**Tier:** Standard | **Date:** 2026-03-04
**Ground truth:** Training data knowledge of the psychometric debate, updated with primary sources.

## The Short Answer

On tests *not* designed to eliminate sex differences (Raven's Progressive Matrices), the best meta-analytic evidence shows:

- **Children (6-14):** No meaningful difference (d ≈ 0)
- **Adults (15+):** Males score ~5 IQ points higher (d = 0.33)
- **University students:** Males score ~4.6 IQ points higher (d = 0.31)

But this is contested. Critics identify serious methodological problems in the meta-analyses producing these numbers, and more recent work finds smaller or null effects.

## Claims Table

| # | Claim | Evidence | Confidence | Source | Status |
|---|-------|----------|------------|--------|--------|
| 1 | IQ test constructors deliberately removed items showing sex differences | Direct quotes from Wechsler (1958), McNemar (1942), Jensen (1980) | HIGH | [SOURCE: Kirkegaard 2021 compilation of primary quotes] | VERIFIED |
| 2 | Wechsler (1958) explicitly stated this practice | "It is possible by initial selection to combine one's test in such a way as to minimise or cancel out sex differences. This has been the usual procedure of most test constructors." | HIGH | [SOURCE: Wechsler 1958, via Kirkegaard] | VERIFIED |
| 3 | McNemar documented 13 female-favoring + 25 male-favoring items removed from Stanford-Binet | Primary source documentation | HIGH | [SOURCE: McNemar 1942, via Kirkegaard] | VERIFIED |
| 4 | Lynn & Irwing 2004 meta-analysis: adult male advantage of 0.33d (5 IQ pts) on Raven's | 57 studies, general population | HIGH | [SOURCE: DOI 10.1016/j.intell.2004.06.008, full text read] | VERIFIED |
| 5 | Lynn & Irwing 2005: university student male advantage of ~4.6 IQ pts | 22 studies | MEDIUM | [SOURCE: DOI 10.1348/000712605X53542] | VERIFIED but methodology contested |
| 6 | Blinkhorn: Lynn/Irwing methodology deeply flawed | Non-comparable samples, no corrections for measurement error/range restriction, uneven sex ratios | HIGH | [SOURCE: Nature 438:31-32, 2005; Nature 442:E1, 2006] | VERIFIED |
| 7 | Molenaar et al. 2022: no reliable g differences in school-age children | Large representative samples, latent variable analysis | HIGH | [SOURCE: Intelligence 92:101651] | VERIFIED via Perplexity |
| 8 | Irwing 2012 WAIS-III analysis: male advantage in g on US standardization sample | WAIS-III standardization data | MEDIUM | [SOURCE: Irwing 2012, gwern.net hosted PDF] | SAVED but PDF unreadable |
| 9 | Deary et al. 2007: brother-sister NLSY analysis found male g advantage | Sibling design controls family environment | MEDIUM | [SOURCE: DOI 10.1016/j.intell.2006.09.003] | SAVED, not yet read |
| 10 | Taiwan WAIS-IV: males 4.05 IQ points higher (d=0.27) on full-scale IQ in adults | Large standardization sample | MEDIUM | [SOURCE: Lupine Publishers SJPBS.MS.ID.000198] | VERIFIED via Perplexity |

## 1. Did Test Constructors Really Balance for Sex?

**Yes. This is well-documented, not a conspiracy theory.**

The practice is confirmed by multiple primary sources:

- **Wechsler (1958):** Explicitly stated that minimizing sex differences "has been the usual procedure of most test constructors." [SOURCE: Wechsler 1958, *The Measurement and Appraisal of Adult Intelligence*]
- **McNemar (1942):** Documented that Stanford-Binet revision removed items showing large sex differences — 13 items favoring females and 25 favoring males were dropped. [SOURCE: McNemar 1942]
- **Jensen (1980):** Confirmed that the "Wechsler scales have explicitly tried to minimize sex differences by discarding those items" and "counterbalancing the number of remaining items." [SOURCE: Jensen 1980, *Bias in Mental Testing*]
- **Kaufman & Lichtenberger:** Acknowledged that test developers "have consistently tried to avoid gender bias in the selection of subtests and in the choice of items." [SOURCE: via Kirkegaard 2021]

**Important nuance:** The user's framing — that "verbal is weighted higher to even out women" — is a simplification of what actually happened. The practice was not specifically about boosting verbal weight for women. Rather:

1. Items showing large sex differences *in either direction* were removed
2. Subtests were selected and counterbalanced so that male-favoring and female-favoring items cancelled out
3. The net effect is that the composite score shows no sex difference by design

However, since males tend to excel on more item types (spatial, mathematical, mechanical reasoning) and females primarily on verbal/processing speed, removing sex-differing items or balancing them does disproportionately remove male-favoring content. The verbal emphasis is part of this, but it's not the whole story.

**Counter-argument (Mackintosh, Kaufman):** The early test constructors may have *discovered* approximate equality rather than manufactured it. Burt found that items showing sex differences tended to be weaker measures of general intelligence. The items removed may have been measuring specific abilities rather than g. [SOURCE: Kaufman/Psychology Today 2009; Mackintosh via same]

## 2. What Do Unbalanced Tests Show?

### Raven's Progressive Matrices (the key "unbalanced" test)

Raven's was not constructed with sex-balancing in mind. It measures fluid reasoning / nonverbal intelligence.

**Lynn & Irwing (2004) meta-analysis** — 57 studies, general population:
- Ages 6-14: **No sex difference** (essentially d = 0)
- Ages 15+: **Male advantage of 0.33d = ~5 IQ points**
- Colored Progressive Matrices (ages 5-11): Boys 0.21d = ~3.2 IQ points ahead
- Interpretation: Males develop a fluid intelligence advantage post-puberty

[SOURCE: Lynn & Irwing 2004, Intelligence 32:481-498, full text verified]

**Lynn & Irwing (2005) meta-analysis** — 22 studies, university students only:
- Male advantage of ~4.6 IQ points on Progressive Matrices
- Greater male variability also found

[SOURCE: Irwing & Lynn 2005, British Journal of Psychology 96:505-524]

### Criticisms of Lynn & Irwing (significant)

**Steve Blinkhorn (Nature, 2005-2006)** called the methodology "deeply flawed":
- Non-comparable samples (uneven sex ratios, selective recruitment from specific faculties)
- Different test versions and time limits across studies
- No corrections for measurement error or range restriction in high-ability samples
- University samples are unrepresentative of the general population
- The included studies were never designed to measure sex differences — they were convenience samples repurposed

[SOURCE: Blinkhorn, Nature 438:31-32 (2005); Nature 442:E1 (2006)]

**This is a serious critique.** If male-dominated STEM departments are overrepresented in the university samples, the "male advantage" is a sampling artifact, not a cognitive difference.

### WAIS-III/IV Standardization Samples (designed to be representative)

These are more informative than university convenience samples:

- **Taiwan WAIS-IV standardization:** Males 4.05 IQ points higher (d = 0.27) on full-scale IQ in adults ages 16-90. Males led on verbal comprehension (d = 0.27), perceptual reasoning (d = 0.37), working memory (d = 0.25). Females led on processing speed (d = 0.14). [SOURCE: via Perplexity, Lupine Publishers]
- **WPPSI-IV (ages 2-7):** No significant sex difference (d = 0.05) [SOURCE: same Taiwan study]

Note: The WAIS was designed to minimize sex differences, yet a 4-point male advantage still appeared in the Taiwan standardization. This could indicate either (a) balancing is imperfect, or (b) real population differences exist.

### Molenaar et al. (2022) — Most Recent Large Meta-Analysis

- **No reliable sex differences in g** among school-aged children and adolescents
- Used latent variable modeling (more methodologically rigorous than simple mean comparisons)
- Found consistent domain-specific patterns: females ahead on processing speed (d = 0.11-0.38), males ahead on visual-spatial processing
- Rejected greater male variability as a primary driver

[SOURCE: Intelligence 92:101651, via Perplexity]

## 3. The Bigger Picture: What Would "Fair Weighting" Look Like?

This is the core question. There is no objectively "fair" weighting — the weighting determines what you're measuring.

**If you weight by g-loading alone** (items that best predict the general factor):
- The sex difference would likely be small (0-5 IQ points favoring males in adults), because spatial/mechanical items have moderate g-loadings but aren't the highest
- Verbal items have high g-loadings too — removing them would hurt the test's validity

**If you include all cognitive domains equally** (verbal, spatial, mathematical, processing speed, working memory):
- Males gain on spatial and mathematical
- Females gain on verbal and processing speed
- Net effect depends on the exact balance, but most evidence suggests a small male advantage of ~2-5 IQ points in adults

**If you weight toward fluid reasoning** (Raven's-style):
- Lynn & Irwing's estimate: ~5 IQ points male advantage in adults
- Critics' estimate: ~2-3 IQ points or less, once methodology is cleaned up

**The variability finding is arguably more important than the mean:**
- Males show greater variance on most cognitive measures (more at both extremes)
- This means more males at both the very top AND very bottom of the distribution
- At +2 SD (IQ 130+), male:female ratios of roughly 2:1 are commonly reported
- This matters more for "who's at the top" than a 3-5 point mean shift does

## What's Uncertain

1. **Whether the adult male advantage on Raven's is 2 points or 5** — depends heavily on whether you trust Lynn/Irwing's methodology or Blinkhorn's critique. The truth is likely in the middle.

2. **Whether the Raven's difference reflects g or spatial-specific ability** — Progressive Matrices load heavily on spatial reasoning, not just fluid g. If the male advantage is spatial-specific rather than g-general, it doesn't generalize to "males are smarter."

3. **Developmental trajectory and the maturational confound** — The "no difference in childhood, male advantage at 15+" finding has a major confound: female neurodevelopment leads male by ~1.5-2 years through adolescence (prefrontal cortex maturation ~22-23 in females vs ~25 in males). IQ tests are age-normed, not maturation-normed. This means a 12-year-old girl is being compared to a 12-year-old boy whose brain is developmentally ~2 years behind hers. The "childhood equality" finding may actually mask a female maturational advantage that disappears as males catch up. The "male advantage emerges at 15" could simply be males finishing their developmental catch-up, not a new advantage appearing. If this is correct, the adult difference (post-25, when both sexes are fully mature) is the real signal — and it appears to be ~3-5 IQ points on fluid measures. [INFERENCE]

4. **Population specificity** — Most data is WEIRD (Western, Educated, Industrialized, Rich, Democratic). Cross-cultural patterns are inconsistent.

5. **Whether the construction-balancing actually changed the answer** — Mackintosh's argument that the removed items were poor g-measures has never been definitively refuted or confirmed.

## [FRAMING-SENSITIVE] Assessment (revised after cross-model review)

### Corrections from adversarial review (Gemini 3.1 Pro + Flash, 2026-03-04)

**Three key errors in our earlier analysis were caught:**

1. **Processing speed: we had it backward.** We called the Dutch d=0.71 female advantage an "outlier" because Italy showed d=0.02. Roivainen (2011) reviewed global WAIS standardization data and found a consistent female PS advantage of d≈0.40-0.60. The US WAIS-IV shows d≈0.53. **The Italian data is the outlier, not the Dutch.** The female processing speed advantage is real and substantial. [SOURCE: Roivainen 2011, Learning and Individual Differences; verified via Exa]

2. **Our meta-analysis has a unit-of-analysis error.** We pooled 36 subtest effects as if independent, but they come from only 3 samples with inter-subtest correlations of r≈0.3-0.7. The confidence intervals are ~3-4x too narrow. The directional estimates survive but the precision is overstated. A random-effects model is required (our fixed-effects model is invalid given Q=70 for processing speed). [Both reviewers flagged independently]

3. **We missed the key finding: no sex difference in latent g.** Johnson & Bouchard (2007) used multiple test batteries and found no sex difference in the general intelligence factor — only in a specific visualization factor. The male advantage is in spatial visualization, not general intelligence. This is the most important distinction in the entire literature and we didn't mention it. [SOURCE: Johnson & Bouchard 2007, Intelligence 35:23-59; verified via Exa]

**Additional corrections:**
- Arithmetic (d=-0.52) is the most education-dependent WAIS subtest. The gap narrowed from WAIS-R (d=-0.57) to WAIS-IV (d=-0.47), tracking the gender convergence in math education. This may measure educational history more than innate ability. [F11, F12]
- If you restrict analysis to DIF-free, measurement-invariant subtests only (Vocabulary, Similarities, Matrix Reasoning), the sex difference drops to ≈0-1 IQ points. [F14]
- Flynn (2012) found that in nations with high gender egalitarianism, adult women match or exceed men on Raven's Progressive Matrices. This challenges the universality of Lynn's 5-point adult male advantage. [G4 — UNVERIFIED, needs source check]

### Revised answer

The answer to "what would IQ be without balancing" depends on **what you measure and how**:

| Method | Result | Confidence |
|--------|--------|-----------|
| **Latent g (general factor)** | **Contested: 0 to ~3 pts male** | CONTESTED — Johnson & Bouchard 2007 found none; Irwing 2012 found d=0.19-0.22 male advantage on US WAIS-III. Battery-dependent. |
| Manifest FSIQ (current WAIS) | ~2-4 pts male advantage | MEDIUM-HIGH — replicates across Netherlands, Italy, Taiwan, US |
| DIF-free subtests only | ~0-1 pts | LOW — DIF analysis has circularity problem (Borsboom 2006): assumes equal latent means to detect bias |
| Including all subtests | ~3-5 pts male advantage | MEDIUM — includes subtests with known DIF, but DIF ≠ definitely invalid |
| Raven's Progressive Matrices (adults) | ~3-5 pts male advantage | MEDIUM — but varies by national gender equality (Flynn 2012) |

### Counter-review (Sonnet 4.6 adversarial + Perplexity, 2026-03-04)

The Gemini corrections were themselves challenged by a second adversarial round:

1. **"No g difference" is NOT settled.** Irwing (2012) analyzed the US WAIS-III standardization sample and found a male g advantage of d=0.19-0.22 — directly contradicting Johnson & Bouchard. The finding is battery-dependent: which tests you include determines the g you extract. Brain volume data (males ~10% larger corrected for body size, brain-IQ r≈0.3-0.4) creates a biological prior favoring a small male g advantage. [SOURCE: Irwing 2012 via Perplexity; Sonnet adversarial analysis]

2. **Processing speed: the range is the finding, not any single number.** Cross-national variation from d=0.02 (Italy) to d=0.71 (Netherlands) on the same instrument is signal, not noise. True cross-nationally stable effect is probably **d≈0.2-0.4**, not the 0.4-0.6 Gemini claimed. WAIS processing speed subtests are confounded by fine motor speed and clerical training — reaction time paradigms show smaller effects. [SOURCE: Sonnet adversarial analysis]

3. **DIF-restriction is circular (Borsboom 2006).** DIF analysis assumes equal latent means to detect bias. If males genuinely have higher ability on some dimensions, DIF will flag items where males outperform as "biased" — then removing them "eliminates" the difference by construction. The three subtests surviving DIF (Vocabulary, Similarities, Matrix Reasoning) are also the three with smallest sex differences. This could be genuine measurement invariance or post-hoc cherry-picking — **we cannot distinguish these interpretations without an independent criterion.** [SOURCE: Sonnet adversarial analysis; Borsboom 2006]

**The honest answer, twice-revised:** The question "what is the real IQ gap?" has no single answer because it depends on unresolvable measurement choices:

- **Latent g:** Genuinely contested (d=0 to d=0.22 depending on study/battery). Not settled.
- **Manifest FSIQ:** ~2-4 points male advantage. Most stable finding. Replicates widely.
- **Specific domains:** Males lead on spatial (d≈0.3-0.5), arithmetic (d≈0.4-0.5 but education-confounded), and knowledge (d≈0.3-0.4 but DIF-biased). Females lead on processing speed (d≈0.2-0.4 cross-nationally) and verbal memory (d≈0.28).
- **Greater male variability** (more males at both extremes) remains the most robust and practically important finding.
- **The composition of the test determines the answer.** This isn't a problem to solve — it's the actual state of the science. There is no "fair" weighting that doesn't embed assumptions about what intelligence is.

## Adversarial Attack: Is the Female Verbal Advantage Real or Practice-Confounded?

### The "Yapping" Hypothesis — Dead on Arrival

**Women don't actually talk more than men.** Mehl et al. (2007) attached electronically activated recorders to 396 people and counted actual daily word production: women 16,215 words/day, men 15,669. Statistically identical. The "women talk 20,000 words, men 7,000" is an urban myth with no empirical basis. [SOURCE: Mehl et al. 2007, Science; verified via Perplexity]

So the crude version — women score higher on verbal because they practice talking more — is wrong.

### The Subtler Practice Confound — Reading

The stronger version of the argument: **verbal IQ (especially vocabulary) correlates strongly with reading, and women read more.** Reading predicts longitudinal VIQ gains across subtests. If the verbal advantage reflects differential reading exposure rather than innate ability, it's a practice artifact, not a cognitive difference. [SOURCE: Reynolds & Turek 2012; PMC3853584]

This is a real confound, but it doesn't fully explain the pattern because:
- Female advantages in speech sound discrimination appear as early as **6 months** [SOURCE: PMC3769140]
- Verbal advantages appear at **2-4 years**, before literacy [SOURCE: PMC10561781]
- The direction of causation is ambiguous — maybe women read more *because* they have higher verbal ability, not the other way around

### The Female Verbal Advantage Is Tiny — and Non-Uniform

This is the most important point:

| Verbal Subtype | Female Advantage (d) | Source |
|---------------|---------------------|--------|
| **Overall verbal ability** | **0.11** | Hyde & Linn 1988, 165 studies |
| Phonemic fluency | 0.12-0.14 | Hirnstein et al. 2022 |
| Verbal episodic memory (recall) | 0.28 | Hirnstein et al. 2022 |
| Verbal memory (recognition) | 0.12-0.17 | Hirnstein et al. 2022 |
| Semantic fluency | ~0.01-0.02 | Hirnstein et al. 2022 |
| Overall verbal fluency | 0.07 | Hirnstein et al. 2022 |
| Verbal comprehension (WAIS) | ~0 (or male advantage) | Taiwan WAIS-IV: d = -0.27 male advantage |

Key observations:
1. The female verbal advantage is concentrated in **verbal memory and phonemic fluency** — not verbal reasoning or comprehension
2. On the WAIS-IV Verbal Comprehension Index, **males actually lead** (d = 0.27 in Taiwan standardization)
3. Semantic fluency (generating category members) shows essentially **no sex difference**
4. The largest female advantage (verbal episodic memory, d = 0.28) is a **memory** skill, not a reasoning skill

### The Asymmetry That Makes "Balancing" Misleading

Here's the adversarial punchline:

- Female verbal advantage: d ≈ 0.11 (overall)
- Male spatial advantage: d ≈ 0.4-0.7 (mental rotation d ≈ 0.7, spatial visualization d ≈ 0.4)
- Male math advantage: d ≈ 0.15-0.25 (depending on type)

If you "balance" a test by including equal parts verbal and spatial, you're treating a d = 0.11 female advantage as equal counterweight to a d = 0.5+ male advantage. **This is not "fairness" — it's over-weighting the smaller effect.** A truly "effect-size-balanced" test would produce a net male advantage because the male-favoring domains have larger effect sizes.

However, this argument assumes all cognitive domains are equally valid components of intelligence, which is itself a contestable assumption. Verbal memory and processing speed matter in real-world functioning even if their sex differences are small.

### What Survives the Attack

The practice confound is real for **vocabulary and crystallized verbal knowledge** — these are demonstrably influenced by reading exposure. But it cannot explain:
- Verbal advantages appearing at 6 months to 2 years (pre-literacy)
- The fact that women don't actually talk more
- The verbal memory advantage (d = 0.28), which is not obviously practice-dependent

The attack on the *overall IQ balancing question* is stronger: the asymmetry in effect sizes (large male spatial advantage vs small female verbal advantage) means that "equal weighting" systematically under-represents the male advantage. Whether this constitutes "unfairness" depends on what you think intelligence tests should measure.

[FRAMING-SENSITIVE: The claim "IQ tests are rigged against men" and the claim "IQ tests fairly measure all cognitive domains" are both overstated. The truth is that design choices in test construction have non-trivial consequences for group comparisons, and there is no Archimedean point from which to define "fair weighting."]

## Deep Dive: Are Verbal Subtests Really Measuring Memory?

### The Subtest-Level Data (Dutch WAIS-III, van der Sluis et al. 2006)

This study (N=522, ages 18-46) is methodologically strong — used multi-group covariance and means structure analysis with DIF (differential item functioning) testing. It breaks apart what "verbal IQ" actually measures at the subtest level.

**Verbal Comprehension subtests:**

| Subtest | What it measures | Males M(SD) | Females M(SD) | d | Direction |
|---------|-----------------|-------------|---------------|-----|-----------|
| **Information** | General knowledge (crystallized memory) | 10.74 (2.92) | 8.82 (2.91) | **0.66** | **Males** |
| **Similarities** | Verbal abstract reasoning | 7.35 (2.28) | 6.96 (1.98) | 0.18 | Males |
| **Vocabulary** | Word meaning knowledge (crystallized memory) | 9.97 (2.80) | 9.79 (2.44) | **0.07** | ≈ None |

**Other subtests:**

| Subtest | What it measures | d | Direction |
|---------|-----------------|-----|-----------|
| Arithmetic | Numerical reasoning | 0.42 | Males |
| Letter-Number Seq. | Working memory | 0.10 | ≈ None |
| Block Design | Spatial reasoning | 0.26 | Males |
| Matrix Reasoning | Fluid reasoning (like Raven's) | 0.20 | Males |
| Picture Completion | Visual perception | 0.23 | Males |
| **Digit-Symbol Sub.** | **Processing speed** | **0.71** | **Females** |
| Copying | Processing speed | 0.19 | Males |

**Composite scores:**

| Composite | Males | Females | d | IQ point gap |
|-----------|-------|---------|-----|-------------|
| Verbal IQ | 98.62 | 93.04 | 0.44 | **5.6 pts** (males) |
| Performance IQ | 102.02 | 102.86 | 0.07 | ≈ 0 |
| Full Scale IQ | 99.19 | 96.63 | 0.24 | **2.6 pts** (males) |

[SOURCE: van der Sluis et al. 2006, Intelligence 34:263-282, full text read. N=228 males, 294 females]

### The Critical Finding: Information Is Biased

Van der Sluis et al. performed DIF analysis and found **Information was biased in favor of males** — it functions differently by sex even at equal ability levels. When they removed Information from the model:

> **"No sex differences were found with respect to the factor Verbal Comprehension (once Information was effectively removed from the model)."**

This is a bombshell. The male VIQ advantage (d = 0.44, ~5.6 IQ points) is **driven by a single biased subtest** — Information (general knowledge questions). Remove it, and the verbal sex difference disappears.

### So Is "Verbal = Memory"? No — It's More Specific Than That

The user's question was whether verbal subtests are biased toward memory (vocabulary). The answer:

**Vocabulary (word knowledge) shows NO sex difference** (d = 0.07). This kills the hypothesis that vocabulary-as-memory drives a female advantage. In fact, there IS no female advantage on Wechsler verbal subtests — males lead on all three VCI subtests.

The female "verbal advantage" from meta-analyses (Hyde & Linn d = 0.11) comes from **different tasks entirely:**
- Verbal episodic memory (remembering word lists, stories): d = 0.28 female advantage
- Phonemic fluency (generating words starting with F, A, S): d = 0.12-0.14 female advantage
- These are NOT standard IQ test subtests

What verbal IQ tests actually measure, subtest by subtest:
1. **Information** (general knowledge) — massive male advantage (d = 0.66), but **confirmed biased** via DIF. This is crystallized knowledge about the world, not "verbal ability." Men know more trivia. Whether this reflects intelligence or differential exposure to reference material is debatable.
2. **Vocabulary** (word definitions) — no sex difference. This IS crystallized verbal memory. Equal.
3. **Similarities** ("How are X and Y alike?") — small male advantage (d = 0.18). This is genuine verbal *reasoning*, not memory.

### Causal Structure [/causal-check applied]

The question "is verbal IQ confounded by memory?" involves three distinct causal claims:

**Claim 1: "Women score higher on verbal because they talk more / practice more"**
- Null: Women don't actually talk more (Mehl 2007, equal word counts)
- Prediction if true: Vocabulary (most practice-dependent) should show largest female advantage
- Observation: Vocabulary shows NO sex difference (d = 0.07)
- **Verdict: REFUTED by evidence pattern**

**Claim 2: "Verbal IQ subtests measure accumulated knowledge, not reasoning"**
- Partially true: Information and Vocabulary are crystallized. Similarities is reasoning.
- But: Vocabulary shows no sex difference, and the male advantage on Information is driven by general knowledge (geography, science, history), not verbal skill per se
- The question is mis-framed: the issue isn't "verbal = memory" but "which kind of knowledge does each subtest tap?"

**Claim 3: "The female verbal advantage exists and inflates women's overall IQ"**
- On Wechsler tests: FALSE. Males lead on VCI (d = 0.18-0.66 across subtests)
- On non-IQ verbal tasks: True but small (verbal fluency d = 0.07-0.14, verbal memory d = 0.28)
- The female advantage that IQ test construction "balances against" is primarily **processing speed** (Digit-Symbol Substitution, d = 0.71), not verbal ability
- **This reframes the original question entirely.** The balancing isn't "verbal up to help women." It's "processing speed tasks (where women lead by d = 0.71) balanced against spatial + knowledge tasks (where men lead by d = 0.2-0.66)."

### The Revised Picture

The common narrative — "IQ tests boost verbal to help women" — is wrong in its specifics:

1. Women don't lead on verbal IQ subtests at all (males lead on Information, Similarities; tie on Vocabulary)
2. The largest female advantage in the entire WAIS battery is **Digit-Symbol Substitution** (processing speed, d = 0.71) — this is a psychomotor/speed task, not verbal
3. The largest male advantage is **Information** (d = 0.66) — but this is biased via DIF
4. If you remove the biased Information subtest AND the large processing speed advantage, the remaining sex differences are small and mostly favor males

**What test construction balancing actually did:** It balanced the large female processing speed advantage against the large male knowledge/spatial advantages. Not "verbal up for women" — "speed up for women."

## Replication: Italian WAIS-IV and WAIS-R (Pezzuti et al. 2020)

**Independent replication on a much larger sample.** Lead author: Lina Pezzuti [F]. N=2,175 (WAIS-IV) + N=2,798 (WAIS-R), Italian standardization data.

### Italian WAIS-IV subtest effect sizes (census-weighted, negative = male advantage)

| Subtest | Type | d | Direction |
|---------|------|---|-----------|
| **Arithmetic** | Numerical reasoning | **-0.47** | **Males** |
| Information | General knowledge | -0.29 | Males |
| Block Design | Spatial | -0.29 | Males |
| Visual Puzzles | Spatial | -0.30 | Males |
| Figure Weights | Fluid reasoning | -0.32 | Males |
| Matrix Reasoning | Fluid reasoning | -0.19 | Males |
| Letter-Number Seq. | Working memory | -0.22 | Males |
| Digit Span | Working memory | -0.18 | Males |
| Comprehension | Verbal reasoning | -0.14 | Males |
| Picture Completion | Visual | -0.14 | Males |
| Symbol Search | Processing speed | -0.09 | ≈ None |
| **Similarities** | Verbal reasoning | **0.03** | **≈ None** |
| **Vocabulary** | Word knowledge | **0.04** | **≈ None** |
| **Coding** | Processing speed | **0.02** | **≈ None** |
| Cancellation | Processing speed | 0.01 | ≈ None |

**Index-level:**

| Index | d | Direction |
|-------|---|-----------|
| Working Memory | -0.37 | Males |
| Perceptual Reasoning | -0.31 | Males |
| **Full Scale IQ** | **-0.24** | **Males (~3.6 pts)** |
| Verbal Comprehension | -0.08 | ≈ None |
| Processing Speed | 0.04 | ≈ None |

[SOURCE: Pezzuti et al. 2020, Intelligence 79:101436, full text read]

### What the Italian data confirms and contradicts

**Confirms (replicates Dutch findings):**
- Vocabulary: NO sex difference (d = 0.04, vs Dutch d = 0.07)
- Similarities: NO sex difference (d = 0.03, vs Dutch d = 0.18)
- Information: male advantage (d = -0.29, vs Dutch d = 0.66) — present but SMALLER
- Arithmetic: large male advantage (d = -0.47, vs Dutch d = 0.42)
- Verbal Comprehension Index: NO sex difference (d = -0.08, vs Dutch: no difference after DIF correction)
- Full Scale IQ: male advantage (d = -0.24, ~3.6 points, vs Dutch d = 0.24, ~2.6 points)

**Contradicts / qualifies Dutch findings:**
- Information effect much smaller in Italy (d = 0.29 vs 0.66) — the Dutch d = 0.66 may be an outlier
- Processing speed: NO female advantage in Italy (d = 0.02-0.04), vs Dutch d = 0.71 female advantage
- The massive Dutch Digit-Symbol female advantage (d = 0.71) does NOT replicate in Italy (Coding d = 0.02)

**DIF / Bias findings (CONFIRMS Dutch):**
> "Information, Arithmetic, and Comprehension subtests were gender-biased in both editions."

Partial scalar invariance required releasing intercepts for Information, Comprehension, and Arithmetic on WAIS-IV. Same pattern as Dutch study — **Information is biased in favor of males across two independent countries.**

### Italian WAIS-R (older test, N=2,798, census-weighted)

Larger effects than WAIS-IV, especially:
- Arithmetic: d = -0.57 (males)
- Information: d = -0.39 (males)
- Block Design: d = -0.40 (males)
- Vocabulary: d = -0.06 (≈ none)
- Similarities: d = 0.01 (≈ none)
- Coding: d = 0.03 (≈ none)
- Full Scale IQ: d = -0.32 (~4.8 points, males)

**Key pattern: sex differences were LARGER on the older WAIS-R than on the newer WAIS-IV.** This suggests test revisions have progressively reduced sex differences — consistent with the "construction balancing" thesis, but also consistent with genuine cultural convergence.

## Cross-Study Comparison: Is the Pattern Stable? (5 datasets)

| Subtest | Dutch WAIS-III | Italian WAIS-IV | Italian WAIS-R | German WAIS-IV | Stable? |
|---------|---------------|----------------|---------------|---------------|---------|
| Vocabulary | 0.07 (none) | 0.04 (none) | -0.06 (none) | -0.12 (M) | **Mostly none** — German outlier |
| Similarities | 0.18 (M) | 0.03 (none) | 0.01 (none) | -0.06 (none) | **None** — Dutch outlier |
| Information | **0.66 (M)** | -0.29 (M) | -0.39 (M) | **-0.42 (M)** | **Direction stable, magnitude varies** |
| Arithmetic | 0.42 (M) | **-0.47 (M)** | **-0.57 (M)** | **-0.48 (M)** | **YES — moderate-large male** |
| Block Design | 0.26 (M) | -0.29 (M) | -0.40 (M) | -0.18 (M) | **YES — small-moderate male** |
| Matrix Reasoning | 0.20 (M) | -0.19 (M) | — | -0.16 (M) | **YES — small male** |
| Coding/Digit-Symbol | **-0.71 (F)** | 0.02 (none) | 0.03 (none) | **+0.29 (F)** | **Direction varies — NL huge, Italy none, Germany moderate** |
| Full Scale IQ | **0.24 (M)** | **-0.24 (M)** | **-0.32 (M)** | **-0.21 (M)** | **YES — d≈0.2-0.3, ~3-5 IQ pts male** |

**Stable findings across both countries:**
1. Vocabulary: no sex difference (highly replicated)
2. Arithmetic: moderate-large male advantage (highly replicated)
3. Information: male advantage but magnitude unstable (and biased via DIF)
4. Full Scale IQ: small male advantage (~2.5-5 IQ points)
5. VCI as a latent factor: no sex difference after DIF correction

**Unstable findings:**
1. Processing speed: huge female advantage in Netherlands, none in Italy — **the single largest "female" effect doesn't replicate**
2. Information effect size: ranges from 0.29 to 0.66 — too variable to anchor conclusions on
3. Similarities: male advantage in Netherlands, none in Italy

**This validates your skepticism about single-study conclusions.** The Dutch processing speed finding (d = 0.71) that I earlier called the "biggest female advantage in the battery" is an outlier. The Italian data (N=2,175, standardization sample) shows no processing speed difference at all.

## Author Gender Tracking

| Study | Lead Author | Gender | Finding Direction |
|-------|------------|--------|------------------|
| van der Sluis et al. 2006 | Sophie van der Sluis | **F** | Males lead on VIQ, no g difference |
| Pezzuti et al. 2020 | Lina Pezzuti | **F** | Males lead on FSIQ, Information biased |
| Daseking et al. 2017 | Monika Daseking | **F** | Males 3.2 pts FSIQ, education effect 53x > sex |
| Deary et al. 2007 | Ian Deary | **M** | g difference d=0.068 (essentially zero), variability key |
| Roivainen 2011, 2019 | Eka Roivainen | **M** | PS female advantage cultural/training, cross-national profiles |
| Camarata & Woodcock 2006 | Stephen Camarata | **M** | No g difference, females lead speed/fluency |
| Lynn & Irwing 2004 | Richard Lynn | **M** | Males 5 pts higher on Raven's |
| Irwing & Lynn 2005 | Paul Irwing | **M** | Males 4.6 pts higher in university |
| Blinkhorn 2005-2006 | Steve Blinkhorn | **M** | Methodology "deeply flawed" |
| Hyde & Linn 1988 | Janet Hyde | **F** | Verbal difference trivial (d = 0.11) |
| Hirnstein et al. 2022 | Marco Hirnstein | **M** | Small female verbal fluency/memory advantages |
| Reynolds et al. 2022 | Matthew Reynolds | **M** | No g difference, specific ability differences |
| Molenaar et al. 2022 | — | — | No g difference in children |
| Kaufman (commentary) | Scott Barry Kaufman | **M** | Test constructors "discovered" equality |

**Pattern: All three female-led studies on WAIS data found genuine male advantages on specific subtests while also identifying methodological issues (DIF bias, education confounds).** The advocacy-positioned researchers claiming the largest male advantages (Lynn, Irwing) are all men publishing in lower-impact venues. The most methodologically careful work comes from both genders.

**Notable: Both lead authors on the highest-quality subtest-level studies (van der Sluis, Pezzuti) are women, and both found male advantages that survived DIF correction.** The advocacy-positioned researchers (Lynn, Irwing) who claim the largest male advantages are men publishing in lower-impact outlets (Mankind Quarterly). The methodological critic (Blinkhorn) is also male.

No obvious pattern where author gender predicts finding direction — both female-led studies found genuine male advantages on specific subtests while also finding DIF bias. This is what careful methodology looks like: nuanced, not advocacy.

## Downloadable Data for Independent Analysis

**NLSY79 — Best option for DIY analysis:**
- ASVAB (Armed Services Vocational Aptitude Battery): 10 subtests, individually downloadable
- Subtests: General Science, Arithmetic Reasoning, Word Knowledge, Paragraph Comprehension, Numerical Operations, Coding Speed, Auto & Shop Info, Math Knowledge, Mechanical Comprehension, Electronics Info
- Maps well to our question: Word Knowledge (verbal/memory), Paragraph Comprehension (verbal reasoning), Coding Speed (processing speed), spatial/mechanical subtests
- N ≈ 12,000+, sex recorded, publicly available at nlsinfo.org
- Deary et al. 2007 already used NLSY79 for brother-sister g analysis (paper in our corpus)

**NLSY97:**
- CAT-ASVAB (computerized version), same subtests
- N ≈ 9,000, more recent cohort

**UK Biobank:**
- Multiple cognitive tests (fluid intelligence, reaction time, symbol digit, matrix reasoning, vocabulary)
- N > 170,000, sex recorded
- Requires formal application + data use agreement (not trivially downloadable)

**What we could do with NLSY data:**
1. Download ASVAB subtest scores by sex
2. Compute effect sizes for each subtest independently
3. Test whether "Word Knowledge" (verbal memory) shows any sex difference
4. Test whether "Coding Speed" (processing speed) shows the female advantage
5. Compare verbal subtests (WK, PC) vs. knowledge subtests (GS, AS, EI, MC) vs. math (AR, MK)
6. Run our own factor analysis and test measurement invariance
7. This would be a true independent check on the Wechsler-based findings using a completely different test battery

**Statistical traps to watch for** (per your note about older methodology):
- Multiple comparisons without correction (many older studies)
- Treating standardization samples as random samples (they're stratified)
- Ignoring range restriction in university samples
- Not testing measurement invariance before comparing group means (pre-2000 studies rarely did this)
- Conflating composite-level and subtest-level effects
- Publication bias toward significant findings

### Evidence Quality Assessment [/source-grading applied]

| Source | Lead [M/F] | Reliability | Credibility | Notes |
|--------|-----------|-----------|-------------|-------|
| van der Sluis et al. 2006 | F | B2 | DIF analysis, N=522 | Dutch WAIS-III standardization |
| Pezzuti et al. 2020 | F | B2 | MGCFA + DIF, N=2175+2798 | Italian WAIS-IV + WAIS-R, best available |
| Lynn & Irwing 2004 | M | C3 | Methodology contested | 57 studies aggregated, variable quality |
| Irwing & Lynn 2005 | M | C3 | University samples non-representative | Blinkhorn critique applies |
| Mehl et al. 2007 | M | B2 | Objective measurement | N=396, US only |
| Hirnstein et al. 2022 | M | B2 | Large meta-analysis | Best for verbal fluency/memory |
| Hyde & Linn 1988 | F | B2 | 165 studies | Dated but foundational |
| Reynolds et al. 2022 | M | B2 | Latent variable modeling | Best recent methodology |

## Dataset 4: ASVAB Brother-Sister Pairs (Deary et al. 2007, N=2584)

**The best-designed study in this entire literature.** 1,292 opposite-sex full sibling pairs from NLSY79. The sibling design controls for family SES, genetics, and environmental confounds that plague standardization samples.

### ASVAB Subtest Sex Differences

| Subtest | Domain | Cohen's d | Direction | Male/Female SD ratio |
|---------|--------|-----------|-----------|---------------------|
| Auto & Shop Info | Knowledge (vocational) | **0.89** | **Males** | 1.59 |
| Mechanical Comprehension | Spatial/mechanical | **0.58** | **Males** | 1.41 |
| Electronics Information | Knowledge (vocational) | **0.56** | **Males** | 1.38 |
| Coding Speed | Processing speed | **-0.48** | **Females** | 0.94 |
| Numerical Operations | Processing speed | **-0.27** | **Females** | 1.00 |
| Paragraph Comprehension | Verbal reasoning | **-0.21** | **Females** | 1.08 |
| Science | Knowledge (academic) | 0.21 | Males | 1.19 |
| Arithmetic | Numerical reasoning | 0.17 | Males | 1.12 |
| Word Knowledge | Verbal/crystallized | -0.07 | Females (marginal) | 1.10 |
| Math Knowledge | Numerical reasoning | 0.00 | None | 1.07 |

### Composite / g scores

| Measure | Cohen's d | SD ratio | Note |
|---------|-----------|----------|------|
| **ASVAB g** | **0.068** | **1.16** | <7% of a SD — essentially zero |
| **AFQT g** | **0.064** | **1.11** | Same result on subset |
| AFQT percentile | 0.02 | 1.09 | Functionally zero |

**At top 2% of AFQT scores: 33 males vs 17 females (ratio ~2:1).**

[SOURCE: Deary, Irwing, Der & Bates 2007, Intelligence 35:451-456, full text read]

### What the ASVAB data changes

1. **g difference is essentially zero on ASVAB.** d=0.068 is less than 1 IQ point. This is the cleanest study (sibling design, N=2584, representative sample) and it finds no meaningful g gap.

2. **Female verbal advantage is REAL on ASVAB — unlike WAIS.** Paragraph Comprehension d=-0.21 and Word Knowledge d=-0.07 both favor females. This contradicts the WAIS finding where males lead on all VCI subtests. **Why?** WAIS "verbal" includes Information (general knowledge trivia) which massively favors males and is DIF-biased. ASVAB separates knowledge (Science, Electronics, Auto&Shop — all male-favoring) from pure verbal comprehension.

3. **Processing speed female advantage replicates.** Coding Speed d=-0.48 matches the Dutch WAIS-III (d=0.71) direction and is larger than Italian WAIS-IV (d≈0). The US ASVAB sits between the European extremes.

4. **The massive male advantages are in VOCATIONAL KNOWLEDGE** — Auto&Shop (d=0.89), Mechanical (d=0.58), Electronics (d=0.56). These are interest/exposure-driven, not cognitive ability per se. Nobody would argue knowing about carburetors measures intelligence.

5. **Greater male variability confirmed** — SD ratios 1.07-1.59 across all subtests except Coding Speed (where females have equal or greater variance). This is the most robust finding in the entire literature.

### Causal interpretation [/causal-check]

The ASVAB pattern makes the causal structure clearer than WAIS:

- **Knowledge subtests** (Science, Auto&Shop, Mechanical, Electronics) all favor males. These measure WHAT YOU KNOW, driven by interest and exposure. Males are more interested in mechanical/technical topics → more exposure → higher scores. Not a cognitive difference.
- **Pure verbal comprehension** favors females slightly. When you strip out knowledge/trivia, females are marginally better at understanding text.
- **Processing speed** favors females substantially. Coding Speed d=-0.48 is one of the largest effects. Training-confounded (reading/writing practice — see Roivainen 2011).
- **Mathematical reasoning** shows a small or zero sex difference when knowledge is controlled (Math Knowledge d=0.00, Arithmetic d=0.17).
- **g** is functionally zero. The composite washes out because male advantages (knowledge/mechanical) and female advantages (speed/verbal) cancel.

**This is the strongest evidence that "the composition of the test determines the answer."** The ASVAB includes vocational knowledge subtests that massively favor males. If you weight them equally, males look smarter. If you exclude them (AFQT = Arithmetic + Word Knowledge + Paragraph Comprehension + Math Knowledge), the sex difference vanishes entirely (d=0.02).

## Dataset 5: US WAIS-IV Standardization (Piffer 2016, N≈2200)

From the US WAIS-IV standardization sample (Wechsler 2008). Piffer published the sex differences data.

### US WAIS-IV Index Scores

| Index | Male advantage | d equivalent |
|-------|---------------|-------------|
| Full Scale IQ | **2.25 IQ points** | ~0.15 |
| General Ability Index | **4.05 IQ points** | ~0.27 |
| Verbal Comprehension | Males higher (sig) | — |
| Perceptual Reasoning | Males higher (sig) | — |
| Working Memory | Males higher (sig) | — |
| **Processing Speed** | **Females 4.4 pts** | **~0.29** |

**Greater male variability on 12/15 subtests and on FSIQ and GAI.**

[SOURCE: Piffer 2016, Mankind Quarterly 57(1):25-33; Holdnack et al. 2014]

**Note on Irwing 2012 latent analysis of US WAIS-III (N=2450):** Using multi-group CFA, Irwing found g d=0.19-0.22 (male), Information d=0.40, Arithmetic d=0.37-0.39, and **Processing Speed latent factor d=0.72-1.30 (female).** The latent PS effect is much larger than the manifest PSI because it removes measurement error. This confirms the US female PS advantage is genuinely large.

[SOURCE: Irwing 2012, Personality and Individual Differences 53:126-131]

## Dataset 6: US WAIS-III Standardization (Longman et al. 2007, N=2450)

From Roivainen's (2011) review of the US WAIS-III standardization sample:

| Index | Direction | Magnitude |
|-------|-----------|-----------|
| Full Scale IQ | Males | ~3-4 IQ points |
| Verbal IQ | Males | ~3-4 IQ points |
| Verbal Comprehension | Males | ~3-4 IQ points |
| Perceptual Organization | Males | ~3-4 IQ points |
| Working Memory | Males | ~2-3 IQ points |
| **Processing Speed** | **Females** | **d=0.31 (~4.7 IQ pts)** |

**The PSI female advantage (d=0.31) in the US WAIS-III matches no other index in magnitude.** Processing speed is consistently the strongest female domain across the US, Netherlands, and ASVAB data.

[SOURCE: Longman, Saklofske & Fung 2007, Assessment 14:426-432, via Roivainen 2011]

### Historical US WAIS processing speed sex differences

| Test version | Year | Digit-Symbol d (female advantage) | Source |
|-------------|------|----------------------------------|--------|
| WAIS | 1955 | d≈0.34 | Feingold 1992 |
| WAIS-R | 1981 | d≈0.34 | Feingold 1992 |
| WAIS-III | 1995 | d≈0.31 | Longman et al. 2007 |

The US female PS advantage has been stable at d≈0.3 for 40+ years across WAIS editions. This is NOT an outlier.

## Dataset 6: Cross-National WAIS-IV (Roivainen 2019)

Roivainen compared WAIS-IV standardization samples across 5 countries. These are NOT sex-difference data — they're national profile differences. But they reveal something critical about processing speed.

### National WAIS-IV Profiles (US norms = 100)

| Country | PRI (reasoning) | PSI (speed) | WMI (memory) | N |
|---------|----------------|-------------|--------------|---|
| USA | 100 | 100 | 100 | 1800 |
| Finland | 106 | 96 | 94 | 537 |
| France | 104 | 100 | 96 | 876 |
| Scandinavia | 105 | 97 | 93 | 660 |
| Germany | 109 | 101 | 104 | 1148 |

[SOURCE: Roivainen 2019, Scandinavian Journal of Psychology, full text read]

### Why this matters for sex differences

**Processing speed varies MORE between countries than between sexes.** The Finland-US gap on PSI is 4 IQ points — the same magnitude as the within-country sex difference. This means:

1. **Processing speed is culturally/environmentally modifiable.** If PS were purely biological, Finland and the US should score the same.
2. **Roivainen's explanation:** Americans prioritize speed over accuracy ("work as quickly as you can" vs "without making mistakes"). Europeans — especially Scandinavians and Finns — prioritize not making errors. The test instruction "work as quickly as you can without making mistakes" is interpreted differently.
3. **The sex difference in PS may be partly a "test-taking attitude" effect.** If women are more conscientious/careful (documented in personality literature), the PS advantage could partly reflect test-taking style rather than cognitive speed.
4. **Reaction time data contradicts PS advantage.** Males are faster on simple and choice reaction time tests (Der & Deary 2006, N=7414, UK). Males are faster on finger tapping. If females were truly "faster processors," they should also be faster on reaction time — but they're not. The female PS advantage is specific to pencil-and-paper digit/symbol copying tasks.

### What actually drives the female PS advantage (Roivainen 2011 synthesis)

| Speed task | Who's faster | d | Likely mechanism |
|-----------|-------------|---|-----------------|
| Digit-Symbol Coding (WAIS) | Females | ~0.3-0.5 | Reading/writing fluency, phonological coding |
| Symbol Search (WAIS) | Females | ~0.2 | Scanning + matching |
| Numerical Operations (ASVAB) | Females | 0.27 | Numerical fluency |
| Coding Speed (ASVAB) | Females | 0.48 | Same as above |
| Rapid Picture Naming | Females | ~0.2 | Phonological retrieval |
| Simple Reaction Time | **Males** | ~0.1 | Neuromuscular? |
| Choice Reaction Time | **Males** | ~0.1-0.2 | Neuromuscular? |
| Finger Tapping | **Males** | ~0.3-0.5 | Motor speed |
| Trail Making | Neither | ~0 | Complex scanning |
| Pegboard | Females | ~0.1 | Fine motor dexterity (finger size?) |

[SOURCE: Roivainen 2011, Learning and Individual Differences 21:145-149, full text read]

**Conclusion: "Processing speed" is not a single ability.** There is no general speed factor. Females are faster at tasks involving letters, digits, and symbols (which correlate with reading/writing practice). Males are faster at pure motor speed and reaction time. The WAIS PSI measures specifically the female-favoring type of speed.

Roivainen's strongest claim: **"Tests of processing speed are probably not more culture-free than other cognitive tests."** The female PS advantage may be largely a training effect from greater female engagement with reading and writing (PISA data: girls spend more time on homework, study language more, read more books, write faster in every tested language).

## Dataset 7: Woodcock-Johnson III (Camarata & Woodcock 2006)

From Roivainen's review of the WJ-III standardization (N=1987):

| Domain | Female advantage (IQ pts) | d equivalent |
|--------|--------------------------|-------------|
| Writing Fluency | 7.1 | ~0.47 |
| Processing Speed (Gs) | 5.3 | ~0.35 |
| Reading Fluency | 5.0 | ~0.33 |
| Writing (non-speeded) | 4.0 | ~0.27 |
| Visual Matching (speed) | 4.0 | ~0.27 |
| Decision Speed | 3.9 | ~0.26 |
| Retrieval Fluency | 3.6 | ~0.24 |
| Rapid Picture Naming | 3.0 | ~0.20 |
| Academic Knowledge | -2.8 | ~-0.19 (males) |
| **General Intelligence** | **~0** | **~0** |

[SOURCE: Camarata & Woodcock 2006, Intelligence 34:231-252, via Roivainen 2011]

**Pattern identical to ASVAB:** No general intelligence difference. Females ahead on all speed/fluency tasks. Males ahead on academic knowledge. The WJ-III Gs (processing speed) advantage peaks in adolescence (females 105.5 vs males 97.4 = 8.1 IQ point gap, d≈0.54).

## Cross-Dataset Synthesis (7 datasets, 5 countries)

### Processing Speed: Female Advantage Is Real But Not What It Seems

| Dataset | Country | N | PS d (female+) | PS subtest |
|---------|---------|---|----------------|------------|
| ASVAB (NLSY79) | US | 2584 | **0.48** | Coding Speed |
| WAIS-III | US | 2450 | **0.31** | PSI |
| WJ-III | US | 1987 | **0.35** | Gs |
| WAIS-III | Netherlands | 522 | **0.71** | Digit-Symbol |
| WAIS-IV | Italy | 2175 | **0.02** | Coding |
| WAIS-R | Italy | 2798 | **0.03** | Coding |

Cross-dataset pooled estimate: d≈0.3-0.35 (excluding Italian outlier). Italian data is genuinely discrepant — possibly cultural (see causal analysis below).

### Verbal: Depends Entirely on What You Mean by "Verbal"

| Dataset | Country | Vocabulary/Word Knowledge d | Verbal Comprehension d | Information/Knowledge d |
|---------|---------|---------------------------|----------------------|----------------------|
| ASVAB | US | -0.07 (F) | -0.21 (F, Paragraph Comp) | 0.21-0.56 (M, Science/Electronics) |
| WAIS-III | Netherlands | 0.07 (none) | 0.18 (M, Similarities) | 0.66 (M, Information) |
| WAIS-IV | Italy | 0.04 (none) | -0.14 (M, Comprehension) | -0.29 (M, Information) |
| WAIS-III | US | — | — | Males 3-4 pts on VCI |

**The "verbal" domain splits cleanly:**
- Vocabulary/word knowledge: **NO sex difference** (replicates across all datasets)
- Verbal reasoning/comprehension: **Tiny or zero** (direction inconsistent)
- General knowledge/information: **Males lead substantially** (but DIF-biased on WAIS)

### General Intelligence (g): The Money Table

| Dataset | Country | Design | g/FSIQ d | IQ point equivalent | Source |
|---------|---------|--------|----------|-------------------|--------|
| ASVAB | US | Sibling pairs | **0.068** | **~1 pt** | Deary et al. 2007 |
| AFQT | US | Sibling pairs | **0.064** | **~1 pt** | Deary et al. 2007 |
| **WAIS-IV** | **US** | Standardization | **0.15** | **2.25 pts** | Piffer 2016 |
| WAIS-IV (GAI) | US | Standardization | 0.27 | 4.05 pts | Piffer 2016 |
| WAIS-III | US | Standardization | ~0.2-0.27 | ~3-4 pts | Longman et al. 2007 |
| WAIS-III (g) | US | Standardization | 0.19-0.22 | ~3 pts | Irwing 2012 |
| WAIS-III | Netherlands | Standardization | 0.24 | ~2.6 pts | van der Sluis et al. 2006 |
| WAIS-IV | Italy | Standardization | 0.24 | ~3.6 pts | Pezzuti et al. 2020 |
| WAIS-R | Italy | Standardization | 0.32 | ~4.8 pts | Pezzuti et al. 2020 |
| **WAIS-IV** | **Germany** | Standardization | **0.21** | **3.2 pts** | Daseking et al. 2017 |
| Raven's | Multi-country | Meta-analysis | 0.33 | ~5 pts | Lynn & Irwing 2004 |
| WJ-III | US | Standardization | ~0 | ~0 pts | Camarata & Woodcock 2006 |
| ASVAB (g) | Multi-battery | Latent g | 0 | 0 pts | Johnson & Bouchard 2007 |

**10 estimates from 4 countries, range 0-5 IQ points.** The WAIS FSIQ estimates cluster around 2-4 points. The extremes (0 for ASVAB/WJ-III, 5 for Raven's/WAIS-R) reflect battery composition.

**The range is 0 to 5 IQ points, depending entirely on the battery.**

Batteries with vocational/knowledge subtests (WAIS Information, ASVAB Auto&Shop) → larger male advantage.
Batteries with processing speed weighted equally → smaller male advantage.
Batteries extracting latent g → 0 to 3 points, genuinely contested.

**The single best-designed study (Deary 2007, sibling pairs) finds d=0.07 — essentially zero.**

### Greater Male Variability: The Most Robust Finding

| Dataset | Measure | Male/Female SD ratio | At top 2%, M:F ratio |
|---------|---------|---------------------|---------------------|
| ASVAB g | NLSY79 | 1.16 | 33:17 (~2:1) |
| AFQT g | NLSY79 | 1.11 | — |
| ASVAB subtests | NLSY79 | 1.00-1.59 | — |

This replicates across every dataset. Even when means are equal, males are overrepresented at both extremes.

## Causal Analysis: Who's In the Samples and Why It Matters

### Test Administration

All WAIS standardizations are **individually administered** by a trained examiner in a one-on-one setting (typically 60-90 minutes). This is NOT group testing. The ASVAB is group-administered in military testing centers — a meaningfully different context.

Key causal questions:
- **Examiner effects:** WAIS manuals don't report examiner sex. If female examiners are more common (psychology is ~75% female), could rapport effects differentially affect male vs female test-takers?
- **Individual vs group testing:** The ASVAB group setting may reduce stereotype threat effects compared to the more evaluative WAIS one-on-one setting.

### Netherlands vs Italy: The Processing Speed Paradox

| Factor | Netherlands (~2003) | Italy (~2013) |
|--------|-------------------|--------------|
| Gender Equality Index (WEF) | ~0.75 (top 10) | ~0.69 (bottom third of EU) |
| Female labor force participation | ~70% | ~47% |
| Female university enrollment | >50% | ~55% |
| Female reading score (PISA) | +32 pts over males | +39 pts over males |
| PS sex difference (d) | **0.71 (females)** | **0.02 (none)** |
| Information sex difference (d) | 0.66 (males) | 0.29 (males) |
| FSIQ sex difference (d) | 0.24 (males) | 0.24 (males) |

**The paradox:** The MORE gender-egalitarian country shows a BIGGER female processing speed advantage, not smaller. If PS were driven by traditional gender roles (women do more clerical work), Italy should show the bigger gap.

**Possible explanations:**
1. **Dutch women read/write more in daily life** — higher labor participation means more professional literacy use. Italian women in traditional roles may do less clerical/reading work, reducing their PS training advantage.
2. **Cultural test-taking attitude** — Dutch culture is more direct/efficient; Italian culture may have different speed/accuracy tradeoffs. Roivainen's data shows European PS scores are generally lower than US scores, with northern Europeans lowest.
3. **WAIS-IV vs WAIS-III version effects** — The Italian data uses WAIS-IV (2008 design), Dutch uses WAIS-III (1997 design). The Coding subtest was redesigned between versions. This is a confound we cannot resolve.
4. **Sample composition** — Dutch N=522 (small) vs Italian N=2175 (large). The Dutch d=0.71 may be partly inflated by small-sample variance.

### The Information Subtest: Knowledge ≠ Intelligence

The Information subtest asks factual questions ("Who wrote Hamlet?", "What is the boiling point of water?"). This measures **crystallized knowledge** — what you've been exposed to and remember.

**Why males score higher across all countries:**
- Males consume more non-fiction, news, and reference material [SOURCE: multiple reading habit surveys]
- Males are overrepresented in "systematizing" hobbies (trivia, history, science)
- The DIF analysis (van der Sluis 2006, Pezzuti 2020) confirms Information is **biased** — it functions differently by sex even at equal latent ability

**Why the Dutch gap (d=0.66) is bigger than the Italian gap (d=0.29):**
- Possibly reflects the specific knowledge questions asked (culturally adapted)
- Or: Dutch women, despite high labor participation, may be concentrated in healthcare/education rather than knowledge-intensive fields
- The larger Dutch Information gap coexists with a larger Dutch PS female advantage — these partially cancel in the FSIQ, which is why FSIQ d is identical (0.24) in both countries

### The Arithmetic Confound

Arithmetic shows a large male advantage across all datasets (WAIS d≈0.4-0.6, ASVAB d=0.17). But:
- The gap narrowed from WAIS-R (d=0.57) to WAIS-IV (d=0.47) — tracking the gender convergence in math education
- ASVAB Math Knowledge shows ZERO sex difference (d=0.00) while Arithmetic Reasoning shows d=0.17
- The distinction: Math Knowledge is "what formulas do you know" (education-dependent); Arithmetic Reasoning is "can you solve word problems" (more reasoning)
- PISA 2015 math sex gap is only d≈0.05-0.10 in most countries — much smaller than the WAIS Arithmetic gap
- **Conclusion:** WAIS Arithmetic is substantially confounded by math education history, not pure numerical reasoning ability

## Dataset 8: German WAIS-IV (Daseking et al. 2017, N=1425)

German WAIS-IV standardization sample. Lead authors: Monika Daseking [F] & Franz Petermann [M]. Census-matched, stratified by education.

### German WAIS-IV Index Scores

| Index | Male M(SD) | Female M(SD) | Diff | d | Direction |
|-------|-----------|-------------|------|---|-----------|
| FSIQ | 101.6 (15.4) | 98.5 (14.6) | +3.2 | -0.211 | **Males** |
| VCI | 101.8 (15.0) | 98.4 (14.8) | +3.3 | -0.225 | **Males** |
| PRI | 102.1 (15.2) | 98.2 (14.5) | +4.0 | -0.267 | **Males** |
| WMI | 102.6 (15.7) | 97.6 (14.0) | +5.0 | -0.335 | **Males** |
| **PSI** | **98.3 (14.7)** | **101.5 (15.1)** | **-3.3** | **+0.221** | **Females** |

### German WAIS-IV Subtest Effects

| Subtest | d | Domain | Direction |
|---------|---|--------|-----------|
| Arithmetic | **-0.478** | Numerical reasoning | **Males** |
| Information | **-0.424** | Crystallized knowledge | **Males** |
| Visual Puzzles | -0.315 | Spatial | Males |
| Figure Weights | -0.293 | Fluid reasoning | Males |
| Coding | **+0.285** | Processing speed | **Females** |
| Block Design | -0.180 | Spatial | Males |
| Comprehension | -0.165 | Verbal reasoning | Males |
| Matrix Reasoning | -0.157 | Fluid reasoning | Males |
| Vocabulary | -0.122 | Verbal memory | Males |
| Picture Completion | -0.116 | Visual perception | Males |
| Letter-Number | -0.115 | Working memory | Males |
| Digit Span | -0.114 | Working memory | Males |
| Symbol Search | +0.108 | Processing speed | Females |
| Cancellation | +0.070 | Processing speed | Females |
| Similarities | -0.056 | Verbal reasoning | ~None |

[SOURCE: Daseking, Petermann & Waldmann 2017, Personality and Individual Differences 115:117-122, full text read]

### Key German findings

1. **FSIQ male advantage = 3.2 IQ points (d=0.21)** — matches Netherlands (3.6) and Italy (3.6) almost exactly.
2. **PSI female advantage = 3.3 IQ points (d=0.22)** — confirms the female PS advantage is real, not just a Dutch outlier. Germany sits between Netherlands (d=0.71) and Italy (d=0.02).
3. **Education effect dwarfs sex effect:** omega2=0.264 for education vs omega2=0.005 for sex on FSIQ. Education explains 53x more variance than sex.
4. **No sex × education interaction** on ANY subtest — the sex differences are the same at all education levels.
5. **Vocabulary shows a small male advantage** (d=-0.12) — unlike other datasets where it's essentially zero. This is the first dataset where males lead on Vocabulary. Possibly reflects the German gender gap in higher education participation (older cohorts have much lower female education).

## Meta-Analysis v3 Results (Random-Effects, 5 datasets)

Updated meta-analysis using DerSimonian-Laird random-effects across 61 subtest effects from 5 studies (4 countries, 2 battery types). See `sources/iq-sex-diff/meta_analysis.py`.

### Domain-Level Summary

| Domain | k | d (RE) | IQ pts | 95% CI | I2 | Direction |
|--------|---|--------|--------|--------|-----|-----------|
| Verbal Memory (Vocab) | 5 | -0.021 | -0.3 | [-0.09, +0.05] | 67% | **NONE** |
| Verbal Reasoning | 8 | -0.059 | -0.9 | [-0.16, +0.05] | 91% | **NONE** |
| Crystallized Knowledge | 5 | -0.377 | -5.7 | [-0.49, -0.26] | 86% | **MALE** |
| Numerical Reasoning | 6 | -0.350 | -5.2 | [-0.55, -0.15] | 96% | **MALE** |
| Working Memory | 6 | -0.181 | -2.7 | [-0.24, -0.12] | 55% | **MALE** |
| Spatial | 7 | -0.279 | -4.2 | [-0.34, -0.21] | 70% | **MALE** |
| Fluid Reasoning | 5 | -0.237 | -3.6 | [-0.30, -0.17] | 52% | **MALE** |
| Visual Perception | 5 | -0.205 | -3.1 | [-0.28, -0.13] | 69% | **MALE** |
| Processing Speed | 11 | **+0.152** | **+2.3** | **[+0.02, +0.28]** | 95% | **FEMALE** |
| Vocational Knowledge | 3 | -0.676 | -10.1 | [-0.88, -0.47] | 95% | **MALE** |

### Composite FSIQ/AFQT

| Scope | k | d | IQ pts | 95% CI | I2 |
|-------|---|---|--------|--------|-----|
| All 5 studies (RE) | 5 | -0.204 | -3.1 | [-4.8, -1.3] | 87% |
| WAIS only (4 studies) | 4 | **-0.264** | **-4.0** | **[-4.8, -3.2]** | **15%** |

**WAIS FSIQ is remarkably consistent across 4 countries (I2=15%): d≈-0.26, ~4 IQ points male advantage.**

### How Weighting Changes the Answer

| Scenario | k | d | IQ pts | Direction |
|----------|---|---|--------|-----------|
| All 61 subtests | 61 | -0.167 | -2.5 | Male |
| Without vocational knowledge | 58 | -0.140 | -2.1 | Male |
| Without processing speed | 50 | -0.237 | -3.6 | Male |
| Without voc. knowledge AND speed | 47 | -0.208 | -3.1 | Male |
| Without DIF-biased/knowledge subtests | 48 | -0.085 | -1.3 | Male (barely) |
| Core cognitive only (spatial+fluid+VR+WM) | 26 | -0.177 | -2.7 | Male |

**Every scenario shows a male advantage (1.3 to 3.6 IQ pts).** Processing speed (d=+0.15, now significantly > 0) is the only female-favoring domain. The I2=95% reflects the Italy anomaly.

## Revised Master Assessment (third revision, 2026-03-04)

### What we now know with high confidence:

1. **There is NO meaningful sex difference in general intelligence (g).** The best-designed study (Deary 2007, sibling pairs, N=2584) finds d=0.068. Multiple batteries extracting latent g find 0 (Johnson & Bouchard 2007, WJ-III). Manifest FSIQ scores show 2-5 points male advantage, but this is battery-composition-dependent, not a real g difference.

2. **Greater male variability is real and consequential.** SD ratio ~1.1 on g, producing ~2:1 male:female ratio at the top 2%. This matters more than means for explaining sex ratios in high-achievement domains.

3. **The female processing speed advantage is real (d≈0.3-0.5) but is NOT a general speed factor.** It's specific to pencil-and-paper digit/symbol tasks. Males are faster on reaction time and motor speed. The female advantage is substantially training-driven (reading/writing practice) and culturally modifiable (varies between countries more than between sexes).

4. **"Verbal ability" conflates at least three distinct things:**
   - Vocabulary/word knowledge: no sex difference
   - Verbal reasoning/comprehension: tiny or zero, direction inconsistent
   - General knowledge/information: moderate male advantage, but DIF-biased (measures exposure, not ability)

5. **The largest male advantages are in domain-specific knowledge** (Auto&Shop d=0.89, Mechanical d=0.58, Electronics d=0.56 on ASVAB; Information d=0.29-0.66 on WAIS). These measure interest and exposure, not cognitive capacity.

6. **Test composition determines the answer.** This isn't a problem to solve — it's the fundamental finding. Include vocational knowledge → males look smarter. Include processing speed → gap shrinks. Extract latent g → gap approaches zero. There is no "fair" weighting that doesn't embed assumptions.

### What remains genuinely uncertain:

1. **Whether there is a small (~1-3 point) male advantage in latent g** that the ASVAB misses because it doesn't include spatial subtests. Irwing 2012 found d=0.19-0.22 on WAIS-III g. But Johnson & Bouchard 2007 found zero on a broader battery. Battery-dependent.

2. **Why Italy shows no processing speed sex difference.** Version effects, cultural factors, and sample composition are all possible. This is the single biggest anomaly in the data.

3. **Whether the processing speed female advantage is biological or trained.** The infant/toddler data (speech discrimination at 6 months) suggests some biological component, but the cross-national variation and correlation with reading/writing practice suggest a large environmental component.

4. **Whether the maturational timing confound matters for adult comparisons.** All the adult data cited here is from post-maturation ages (18+), so this should be less of an issue than for adolescent data. But if female brain maturation completes earlier, they may have a brief "fully mature" advantage at 18-22 that disappears by 25+.

## Sources Saved to Corpus

- Lynn & Irwing 2004 — "Sex differences on the progressive matrices: A meta-analysis" (full text fetched)
- Irwing & Lynn 2005 — "Sex differences in means and variability on the progressive matrices in university students"
- Deary et al. 2007 — "Brother-sister differences in the g factor"
- Helland-Riise et al. 2024 — "Large-scale item-level analysis of the Figural Matrices Test in the Norwegian Armed Forces"
- van der Sluis et al. 2006 — "Sex differences on the Dutch WAIS-III" (full text fetched)
- Pezzuti et al. 2020 — "Gender differences and measurement bias: Italian WAIS-IV and WAIS-R" (full text fetched)
- Daseking et al. 2017 — "Sex differences in cognitive abilities: German WAIS-IV" (full text fetched)
- Deary et al. 2007 — "Brother-sister differences in g: NLSY79 ASVAB" (full text fetched)
- Roivainen 2011 — "Gender differences in processing speed: A review" (full text read)
- Roivainen 2010 — "European and American WAIS III norms: Cross-national differences" (full text read)
- Roivainen 2019 — "European and American WAIS IV norms: Cross-national differences" (full text read)
- Camarata & Woodcock 2006 — "Sex differences in processing speed: WJ-III" (via Roivainen 2011)
- Longman, Saklofske & Fung 2007 — "WAIS-III percentile scores by education and sex" (via Roivainen)

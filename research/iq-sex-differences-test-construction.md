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

## [FRAMING-SENSITIVE] Assessment

The answer to "what would IQ be without balancing" depends on what you consider a legitimate intelligence test to measure. If you think spatial reasoning and fluid reasoning deserve more weight than they currently get, the male advantage is real and ~3-5 IQ points in adults. If you think current tests already measure what matters (a mix of all cognitive domains), the balancing reflects a genuine design choice, not political manipulation, and the true difference is 0-3 points.

**The honest answer:** There is *probably* a small male advantage in mean adult IQ of ~3-5 points on tests not constructed to eliminate it, concentrated in fluid/spatial reasoning. But the methodological quality of the studies claiming the larger numbers (5+ points) is questionable, and the greater male variability finding (which is more robust) matters more practically than the mean difference.

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

## Sources Saved to Corpus

- Lynn & Irwing 2004 — "Sex differences on the progressive matrices: A meta-analysis" (full text fetched)
- Irwing & Lynn 2005 — "Sex differences in means and variability on the progressive matrices in university students"
- Deary et al. 2007 — "Brother-sister differences in the g factor"
- Helland-Riise et al. 2024 — "Large-scale item-level analysis of the Figural Matrices Test in the Norwegian Armed Forces"

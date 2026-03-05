ℹ Starting chat {"provider": "anthropic", "model": "claude-sonnet-4-6", "stream": false, "reasoning_effort": null}
# Adversarial Analysis of Three Claims on Sex Differences in IQ

---

## CLAIM 1: "Johnson and Bouchard 2007 found no sex difference in latent g. The male advantage is only in visualization, not general intelligence."

### (a) Strongest Counter-Argument

This is a **selective citation that misrepresents the broader literature** and arguably misrepresents Johnson & Bouchard themselves.

The critical methodological issue: latent g is *extracted from whatever subtests you feed it*. If your battery is dominated by verbal and memory tasks where females perform well, the extracted g factor will be contaminated by those loadings. The "no sex difference in g" finding is partly an artifact of **which tests constitute the battery**. Johnson & Bouchard themselves noted that when visualization-heavy tests are included, males show advantages that partially load onto g. The question of whether visualization *is* g-loaded or merely a *correlate* of g is not settled — it's the thing being disputed.

More damaging: **Colom, Lynn, and others have argued that the g-factor sex difference question cannot be answered by simply extracting g from a battery, because batteries differ in g-saturation**. Lynn's (2012) review across multiple datasets found consistent male advantages of 3-5 IQ points in *total* IQ, which he attributes to greater male brain volume (a genuine finding, d ≈ 0.9-1.0 for brain volume, with established correlations to IQ of r ≈ 0.3-0.4). If brain volume predicts IQ, and males have substantially larger brains *controlling for body size*, this is a biological prior that the "no g difference" finding has to explain away, not merely ignore.

Additionally, **Irwing (2012)** reanalyzed WAIS standardization data and found male advantages on g using confirmatory factor analysis. The Johnson & Bouchard finding is **one study using one battery** — Project Talent data — and has not been robustly replicated with the same methodology across independent batteries.

The claim also conflates "no difference found in this study" with "no difference exists," which is a straightforward inference error that would not be tolerated in any other domain.

### (b) Evidence Required to Accept

- Consistent replication across **at least 5 independent batteries** with varying subtest composition, all showing g-invariance across sex using CFA with equivalent model fit
- A **credible mechanistic account** of why males have ~10% larger brains (corrected for body size) with established IQ-brain correlations, yet show no g advantage
- Demonstration that visualization subtests are **not g-loaded** (i.e., low g-saturation in multiple batteries), which would actually undermine the claim rather than support it — because if visualization is g-loaded and males outperform on it, that *is* a g difference
- Pre-registered replication of the Johnson & Bouchard methodology in a new dataset

### (c) Honest Probability: **25%**

The "no g difference" claim is theoretically coherent but empirically contested and methodologically fragile. The brain volume data alone creates a substantial prior against it. I'd say there's a meaningful male advantage in g of perhaps 2-4 points that is being obscured by battery composition choices and political incentives in how studies are designed and reported.

---

## CLAIM 2: "The female processing speed advantage is real and substantial (d=0.4-0.6 globally). The Italian WAIS-IV data (d=0.02) is the outlier, not the Dutch (d=0.71)."

### (a) Strongest Counter-Argument

This claim is doing something statistically suspicious: **it is deciding which data points count as "outliers" based on whether they conform to the expected finding**, which is circular reasoning dressed as meta-analytic judgment.

The Italian WAIS-IV standardization sample is a **nationally representative normative sample** — it is not a convenience sample, not a clinical sample, not an unusual population. If you are going to dismiss d=0.02 from a nationally representative Italian sample as an "outlier," you need a principled reason that doesn't amount to "it disagrees with what we expected." 

The cross-national variation in processing speed sex differences is itself **theoretically important and underexplored**. If d ranges from 0.02 to 0.71 across Western nations using the *same instrument* (WAIS-IV), this is not noise — this is signal. It suggests the "female processing speed advantage" is **culturally or educationally mediated**, not a robust biological universal. That finding should *reduce* confidence in a strong biological claim, not be explained away.

Furthermore, **processing speed subtests on the WAIS (Coding, Symbol Search) are heavily confounded with fine motor speed, clerical training, and test-taking strategy**. Females outperform on these specific tasks, but whether this reflects a genuine neural processing speed advantage or differential socialization in careful, methodical task execution is unresolved. Studies using **reaction time paradigms** — which strip out motor and strategic components — show much smaller or inconsistent sex differences in raw processing speed.

The d=0.4-0.6 figure also comes disproportionately from older studies and from paper-and-pencil paradigms where female advantages in fine motor control and handwriting fluency contaminate the measure.

### (b) Evidence Required to Accept

- A **pre-registered meta-analysis** with explicit, theory-derived outlier exclusion criteria established *before* seeing the data
- Demonstration that the Italian-Dutch discrepancy is explained by **sampling error** (with appropriate power calculations) rather than genuine population differences
- Processing speed advantages replicating at d=0.4+ using **computerized reaction time tasks** that eliminate motor confounds
- Cross-national invariance testing showing the *same* processing speed factor loads equivalently across Italian and Dutch samples, confirming measurement equivalence before comparing means

### (c) Honest Probability: **35%**

I actually think there is a real female advantage in processing speed on psychomotor/clerical tasks, but the claim that d=0.4-0.6 is the "true" effect and Italy is the outlier is **not well-supported**. The cross-national variance is genuine and theoretically meaningful. I'd put the true cross-nationally stable effect closer to d=0.2-0.3, with substantial cultural moderation. The Gemini review is overconfident here in a direction that happens to favor female performance.

---

## CLAIM 3: "If you restrict to DIF-free, measurement-invariant subtests (Vocabulary, Similarities, Matrix Reasoning), the sex difference drops to approximately 0-1 IQ points."

### (a) Strongest Counter-Argument

This is the **most methodologically problematic claim of the three**, and I'd argue it represents a fundamental misuse of DIF analysis.

**The core problem:** Differential Item Functioning analysis is designed to identify items that function differently across groups *after controlling for the latent trait*. But if males genuinely have higher latent ability on some dimensions, DIF analysis will systematically **flag as "biased" those items on which males actually outperform** — because the analysis assumes equal latent traits as a baseline. This creates a tautological procedure: you remove items showing sex differences, then conclude there are no sex differences. This is not psychometric rigor; it is circular by construction.

This critique is not fringe. **Borsboom (2006)** and others have argued that DIF analysis cannot distinguish genuine ability differences from measurement bias without an independent criterion — which we don't have for sex differences in g. The procedure **assumes the conclusion**.

Second, the specific subtests selected — Vocabulary, Similarities, Matrix Reasoning — are **not a representative sample of cognitive ability**. They happen to be subtests where sex differences are smallest. Vocabulary and Similarities show consistent female advantages in verbal fluency; Matrix Reasoning shows near-parity. Selecting these three and calling them "the unbiased core" is **subtest cherry-picking** rationalized post-hoc through DIF analysis.

Third, **measurement invariance testing** across sex has been conducted on full WAIS batteries and generally supports *configural and metric* invariance — meaning the factor structure is the same — but this is compatible with mean differences in latent factors. Establishing measurement invariance does not establish equal latent means; it establishes that the *measurement instrument* works equivalently. The Gemini review appears to conflate these.

Fourth, the practical implication of this claim — that we should only use three subtests for sex comparisons — would be **rejected outright** in any other group comparison context as methodologically indefensible. We don't restrict race comparison studies to "DIF-free" items selected by the same procedure; the reason this procedure is being applied here is that it produces a desired result.

### (b) Evidence Required to Accept

- A **simulation study** demonstrating that the DIF-exclusion procedure correctly recovers zero differences when the true difference is zero, AND correctly recovers non-zero differences when the true difference is non-zero — i.e., that it is not biased toward null findings
- An **independent criterion** for identifying "biased" vs. "genuinely differentiating" items that does not assume equal latent means
- Replication of the 0-1 IQ point finding using **external validity criteria**: if the DIF-free subtests are the true measure of g, they should predict real-world outcomes (income, job performance, educational attainment) *better* than the full battery — otherwise we have no reason to prefer them
- Pre-registration of the DIF analysis criteria before examining sex differences

### (c) Honest Probability: **15%**

This is the weakest of the three claims. The DIF-restriction procedure is methodologically circular in this application, the subtest selection is not representative, and the conclusion conveniently eliminates the very differences under investigation. I would not accept this as evidence of "no sex difference" any more than I would accept a study that measured only spatial rotation and concluded females have lower IQ. The probability this reflects the true state of affairs rather than methodological artifact is low.

---

## Summary Table

| Claim | Core Problem | My Probability |
|-------|-------------|----------------|
| No g difference (J&B 2007) | Battery composition determines g extraction; brain volume data ignored | 25% |
| Female PS advantage d=0.4-0.6 | Cross-national variance is real signal, not noise; motor confounds unaddressed | 35% |
| DIF-restriction → 0-1 IQ point difference | Circular by construction; cherry-picked subtests; conflates measurement with latent means | 15% |

**Overall assessment:** The Gemini review appears to be applying more skepticism to findings of male advantages than to findings of female advantages or null findings. That asymmetric skepticism is itself a methodological bias that should be named explicitly.

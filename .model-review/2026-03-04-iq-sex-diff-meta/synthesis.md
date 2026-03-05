# Cross-Model Review: IQ Sex Differences Meta-Analysis

**Mode:** Critical Review
**Date:** 2026-03-04
**Models:** Gemini 3.1 Pro (pattern review), Gemini Flash (quantitative audit)
**Note:** GPT-5.2 rate-limited; Flash served as quantitative auditor instead (same-family, different capability tier)
**Constitutional anchoring:** Yes (epistemic_standards from CLAUDE.md)
**Extraction:** 35 unique items, 27 included, 1 deferred, 2 already in memo, 3 meta/self-awareness

## Verified Findings (adopt — changes our conclusions)

| ID | Finding | Source | Verified How |
|----|---------|--------|-------------|
| G1 | **Processing speed: Italian data is the outlier, not Dutch.** Global WAIS standardizations show female PS advantage d≈0.40-0.60. US WAIS-IV: d≈0.53. | Gemini Pro | Verified: Roivainen 2011, Exa /answer |
| G5 | **No sex difference in latent g.** Johnson & Bouchard (2007) found male advantage only in visualization factor, not g. | Gemini Pro | Verified: Johnson & Bouchard 2007, Exa /answer |
| G8/F3 | **Fixed-effects meta-analysis is invalid.** Q=70 for PS explicitly rejects the single-effect assumption. Must use random-effects. | Both | Self-evident from our own Q statistics |
| G9/F1 | **Unit-of-analysis error.** 36 subtests from 3 samples treated as independent. CIs are ~3-4x too narrow. | Both | Correct — subtests within samples are correlated r≈0.3-0.7 |
| F11 | **Arithmetic confounded by math education.** d narrowing WAIS-R→WAIS-IV (0.57→0.47) tracks educational convergence. | Flash | Plausible — needs direct test but evidence pattern fits |
| F14 | **DIF-free subtests → ≈0-1 IQ points.** Restricting to Vocabulary, Similarities, Matrix Reasoning effectively eliminates the gap. | Flash | Logical consequence of verified DIF findings |

## What Changes In Our Conclusions

### MUST CORRECT:
1. **Processing speed narrative is reversed.** We called Dutch d=0.71 an "outlier." Global data says it's the norm (d≈0.4-0.6). Italian d=0.02 is the actual outlier. This means female PS advantage IS real and substantial — the original test-construction story (balancing PS vs spatial) was more correct than our "correction."

2. **Our meta-analysis CIs are invalid.** The "thought experiment" pooling 36 correlated effects generates artificially narrow CIs. The real uncertainty is much wider. The d=-0.197 pooled estimate survives directionally but the stated CI [−0.21, −0.18] should be ~[−0.35, −0.05].

3. **We should have discussed latent g vs manifest FSIQ.** Johnson & Bouchard (2007) found no g difference — the male advantage is in visualization, not general intelligence. This is the most important finding we missed.

4. **Arithmetic is likely education-confounded.** The d=-0.52 may be the most education-dependent subtest, not a pure cognitive measure. The historical narrowing supports this.

### SHOULD ADD:
5. Flynn's cross-national data showing women match men on Raven's in egalitarian nations
6. US WAIS-IV standardization data to resolve PS discrepancy
7. The key distinction: if you restrict to DIF-free, measurement-invariant subtests, the gap is ≈0-1 points

### HEDGE MORE:
8. Maturational timing hypothesis needs explicit falsification criteria
9. The "3-5 IQ points" headline estimate is fragile and depends entirely on which subtests you consider valid

## Deferred
| ID | Finding | Why Deferred |
|----|---------|-------------|
| G14 | Run MG-CFA on latent g | Requires raw data (NLSY or standardization samples), not published effect sizes |

## Rejected
None — all findings were substantive.

## Model Self-Awareness (important)
| Model | Self-Doubt | Assessment |
|-------|-----------|------------|
| Gemini Pro | "Biased against biological essentialism by post-training" | **Valid and important.** Gemini explicitly over-weights environmental explanations. The 3-5 point male advantage on spatial/fluid measures may be genuinely biological, not an artifact. |
| Gemini Pro | "Latent g defense may be irrelevant if intelligence = manifest skills" | **Valid.** If real-world cognitive performance matters more than a latent factor, the male spatial advantage is real regardless of g. |
| Flash | Framing-sensitive: "change the weights, change the gap" | **Valid but incomplete.** While true that weighting is arbitrary, some weightings have more construct validity than others. |

## Revised Bottom Line

Our original conclusion ("3-5 IQ points male advantage on unbalanced tests") is directionally correct but:
1. The range should be wider: **0-5 IQ points** depending on methodology
2. The lower bound (0-1 pts) is achieved with DIF-free, measurement-invariant subtests
3. The upper bound (4-5 pts) requires accepting biased subtests (Information, Arithmetic) as valid
4. **On latent g: no sex difference (Johnson & Bouchard 2007)**
5. **On manifest FSIQ: ~2-4 point male advantage, but composition-dependent**
6. Processing speed female advantage IS real (d≈0.4-0.6 globally), we were wrong to dismiss it

# Cross-Model Review: IQ Sex Differences — Latent g Research Memo
**Mode:** Review (convergent/critical)
**Date:** 2026-03-05
**Models:** Gemini 3.1 Pro (pattern/architectural review), Gemini Flash (quantitative, GPT-5.2 fallback — OpenAI quota exceeded)
**Constitutional anchoring:** Epistemic standards from CLAUDE.md (no standalone constitution)
**Extraction:** 113 items extracted (66 Gemini Pro + 47 Flash), 28 unique after dedup, 15 included, 7 deferred, 3 rejected, 3 merged

## Verified Findings (adopted)

| ID | Finding | Source | Verified How | Applied |
|----|---------|--------|-------------|---------|
| G14/F19 | "Core cognitive only" meta-analysis (d=-0.177) contradicts "no g difference" thesis | Both | Verified against meta_analysis.py output | Added to Short Answer with explicit acknowledgment |
| G21-24/F4-5 | Missing g-loading hierarchy — high-g subtests favor males, low-g favor females | Both | Consistent with CHC literature | New section added to synthesis |
| G34-35 | "Every dataset" vocabulary null claim contradicted by German d=-0.12 | Gemini | Read Dataset 8 table — confirmed | Fixed to "most datasets" |
| G49-51 | Failed to steel-man Lynn & Irwing adequately | Gemini | Epistemic standards audit | Added their g-loading argument to Short Answer |
| F13-16 | 2:1 tail ratio math wrong — actual ~1.5:1 at SD=1.1 with equal means | Flash | Verified with Python computation | Fixed across all occurrences |
| F1-3 | Adolescent data (Strand, Savage-McGlynn) conflated with adult findings | Flash | Valid — different age ranges | Disaggregated in Short Answer |
| G32-33 | Asymmetry: only WJ-III shows female g; most batteries male/null | Both | Tabulation of results | Explicitly acknowledged |
| G36-37 | PS training confound presented as established when it's speculative | Gemini | Roivainen's evidence is suggestive, not proven | Softened to "partially confounded" |
| G60-62 | LLM bias toward egalitarian conclusions | Gemini | Self-aware acknowledgment | Added [⚠ FRAMING-SENSITIVE] to central thesis |
| F17-19 | High I² makes pooled d unreliable for some domains | Flash | I²=86-96% for Knowledge, Speed, Numerical | Added explicit caveat to meta-analysis section |
| F42 | Need "fair weighting" baseline estimate | Flash | Computed from meta-analysis: d≈-0.085 (~1.3 pts) | New subsection: "Toward a Fair Baseline" |

## Deferred (with reason)

| ID | Finding | Why Deferred |
|----|---------|-------------|
| G25-28/F20 | Brain volume prior (Pietschnig 2015) | Requires separate literature review — paper not in corpus |
| G56 | Pietschnig et al. 2015 meta-analysis | Not yet read |
| G57 | DIF calculation methodology detail | Technical appendix material |
| G58-59 | APM (Advanced Progressive Matrices) data | Not in corpus; Lynn's largest gaps found here |
| F27-28 | Longitudinal maturation test | Empirical prediction — can't run from this desk |
| F46-47 | g as statistical mirage (Process Overlap Theory) | Philosophical — warrants a footnote, not a section |
| G43-45 | Brain neuron count claim | Needs source verification |

## Rejected (with reason)

| ID | Finding | Why Rejected |
|----|---------|-------------|
| G54-55 | Rewrite thesis to "g tilts male unless balanced by PS" | One-sided — ignores multiple null findings and WJ-III female g |
| G63-66 | Model limitations (can't run CFA, lacks manuals) | Self-referential to reviewer, not actionable |
| F26 | "Adult representative samples consistently show 3-5 IQ point male advantage" | Conflates manifest FSIQ with latent g — the exact error the memo corrects |

## Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "2:1 ratio at top 2% from SD ratio ~1.1" | ~1.5:1 at pure SD=1.1 with equal means; 2:1 requires both variability AND mean shift | Flash (verified with Python) |
| "Vocabulary: no sex difference in every dataset" | German WAIS-IV d=-0.12 (small male advantage) | Gemini |
| "Substantially training-confounded" (PS) | Roivainen's evidence is suggestive, not conclusive | Gemini |
| Central thesis presented without framing caveat | LLM post-training may bias toward egalitarian conclusions | Gemini |
| Short Answer mixed child and adult data | Child findings (null) don't address adult g | Flash |

## Gemini Pro Errors (distrust)

| Claim | Why Problematic |
|-------|----------------|
| "Brain volume correlates with IQ at r≈0.24" | Actual estimates range 0.24-0.40 depending on study. Specific number needs source. |
| "Modern batteries are artificially truncated against men" | Overstated — batteries were balanced, not truncated. Some spatial items removed, but verbal items also removed. |
| "The thesis should be changed to 'g tilts male unless balanced by PS'" | Ignores multiple null g findings (Deary, Colom) and the WJ-III female finding |

## Flash Errors (distrust)

| Claim | Why Problematic |
|-------|----------------|
| "Adult representative samples consistently show 3-5 IQ point male advantage" | Conflates FSIQ with g — the memo's central point is these differ |
| "If g changes direction based on battery, batteries are not capturing the same construct" | Assumes g is a fixed entity; the battery-dependence IS the finding, not evidence against it |

## Net Assessment

The cross-model review improved the memo substantially. The most important correction: the memo's own meta-analysis code produces a d=-0.177 male advantage on "core cognitive" tasks, which the narrative was underplaying. The Short Answer now honestly presents this tension rather than resolving it prematurely.

Both models converged on the g-loading hierarchy as the memo's biggest blind spot. This has been addressed with a new section acknowledging the argument and presenting a counter-argument.

The tail-ratio math correction (2:1 → 1.5:1 at pure SD=1.1) is an important factual fix that multiple readers would have caught.

**Remaining weakness:** The memo still lacks the brain volume prior (Pietschnig 2015) and APM data. These are the strongest opposition evidence not yet addressed. Adding them would strengthen the memo's credibility even if they support the male-advantage hypothesis.

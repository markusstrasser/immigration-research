# Cross-Model Review Extraction & Disposition
**Topic:** IQ Sex Differences — Latent g Research Memo
**Date:** 2026-03-05
**Models:** Gemini 3.1 Pro (pattern review), Gemini Flash (quantitative, GPT fallback)

## Disposition Table

Items merged where both models raised the same point. INCLUDE = will fix in memo. DEFER = valid but out of scope now. REJECT = wrong or not applicable.

| ID | Claim (short) | Source | Disposition | Reason |
|----|--------------|--------|-------------|--------|
| G14/F19 | Core cognitive d=-0.177 contradicts "no g difference" thesis | Both | **INCLUDE** | Verified against meta_analysis.py output. The memo must acknowledge this. |
| G21-24/F4-5 | Missing g-loading hierarchy (Spearman's Hypothesis) — high-g subtests favor males | Both | **INCLUDE** | Valid gap. The memo treats all subtests equally but g-loadings matter for which subtests define g. |
| G25-28/F20 | Brain volume prior (10% larger, r≈0.24 with IQ) not addressed | Both | **DEFER** | Valid biological argument but requires separate literature review (Pietschnig 2015). Note in memo as gap. |
| G29-31/F6-8 | DIF circularity (Borsboom 2006) insufficiently addressed | Both | **INCLUDE** | Memo mentions it in earlier section but doesn't reconcile with Short Answer. Needs explicit caveat. |
| G34-35 | German Vocabulary d=-0.12 contradicts "every dataset" null claim | Gemini | **INCLUDE** | Factual error. Fix "every dataset" to "most datasets." |
| G49-51 | Failed to steel-man Lynn & Irwing | Gemini | **INCLUDE** | Epistemic standards violation. Add g-loading argument as opposition's best case. |
| G54-55 | Rewrite thesis to "g tilts male unless balanced by PS" | Gemini | **REJECT** | Goes too far — the WJ-III female g finding and multiple null findings make this one-sided. But the core cognitive finding (d=-0.177) needs acknowledgment. |
| G36-37 | PS training confound is speculative | Gemini | **INCLUDE** | Fair. Soften language from "substantially training-confounded" to "partially training-confounded (evidence mixed)." |
| G16-17 | Over-reliance on Savage-McGlynn as Raven's defeater | Gemini | **INCLUDE** | Valid — N=926 is modest. Add Flynn (2017) and Murphy (2023) as supporting evidence, note APM gap. |
| G56 | Address Pietschnig 2015 brain volume meta-analysis | Gemini | **DEFER** | Separate literature not in corpus. Note as future work. |
| G57 | Detail DIF calculation methodology | Gemini | **DEFER** | Technical detail better suited for a methods appendix. |
| G58-59 | Examine APM (Advanced Progressive Matrices) | Gemini | **DEFER** | APM data not in corpus. Note as gap. |
| G60-62 | LLM bias toward egalitarian conclusions | Gemini | **INCLUDE** | Add [⚠ FRAMING-SENSITIVE] tag to the central thesis. Self-aware about potential bias. |
| F13-16 | 2:1 tail ratio math is wrong at SD=1.1 — actual is ~1.5:1 at IQ 130 | Flash | **INCLUDE** | Verified: at pure SD ratio 1.1 with equal means, top 2% ratio is ~1.5:1, not 2:1. The Deary data shows 33:17 (1.94:1) but that includes the d=0.068 mean shift. Fix the claim. |
| F17-19 | High I² (86-96%) makes pooled d meaningless for some domains | Flash | **INCLUDE** | Valid statistical point. Add caveat to meta-analysis interpretation. |
| F1-3 | Maturational confound — adolescent data shouldn't anchor adult conclusions | Flash | **INCLUDE** | Valid. Strand (age 11-12) and Savage-McGlynn (7-18) don't address adult g. Disaggregate in Short Answer. |
| F27-28 | Testable prediction: longitudinal maturation test | Flash | **DEFER** | Good prediction but we can't run it. Note as future empirical test. |
| F29-32 | Testable prediction: IT/RT should show female advantage if PS is cognitive | Flash | **INCLUDE** | Already partially addressed (males faster on RT) but strengthen this as a testable prediction. |
| F38 | Fix "2:1 at top 2%" to "1.5:1" or specify mean shift required | Flash | **INCLUDE** | Merge with F13-16. |
| F39 | Disaggregate adult vs child in Short Answer | Flash | **INCLUDE** | Merge with F1-3. |
| F40 | Promote RT vs Coding contradiction | Flash | **INCLUDE** | Already in memo but needs more prominence. |
| F42 | Define "fair" weighting baseline (~1.3 IQ pts) | Flash | **INCLUDE** | Good idea — pick DIF-free subtests and compute. |
| F46-47 | g may be a statistical mirage (Process Overlap Theory) | Flash | **DEFER** | Philosophical point. Beyond scope but worth a footnote. |
| G32-33 | Asymmetry: only WJ-III shows female g; most batteries show male or null | Gemini | **INCLUDE** | Valid. The "50/50 arbitrariness" framing is misleading. Acknowledge the asymmetry. |
| G38-42 | PS is low-g, spatial/fluid are high-g; male advantages are in high-g domains | Both | **MERGE WITH G21-24** | Same point about g-loading hierarchy. |
| G43-45 | Brain neurons + test construction removal of spatial items | Gemini | **DEFER** | Brain neuron claim needs source verification. Test construction removal already covered. |
| G47-48 | Speed vs fluid reasoning centrality to intelligence | Gemini | **MERGE WITH G21-24** | Part of g-loading argument. |
| G63-66 | Model limitations (can't run CFA, lacks manuals) | Both | **REJECT** | Self-referential to the reviewer, not actionable for the memo. |

## Coverage Count
- Total extracted: 113 (66 Gemini + 47 Flash)
- After dedup/merge: ~28 unique items
- INCLUDE: 15
- DEFER: 7
- REJECT: 3
- MERGE: 3 (merged into INCLUDE items)

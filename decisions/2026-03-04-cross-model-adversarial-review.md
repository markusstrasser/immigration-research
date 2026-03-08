---
id: 2026-03-04-cross-model-adversarial-review
concept: methodology
repo: research
decision_date: 2026-03-04
recorded_date: 2026-03-07
provenance: backfilled
status: accepted
initial_leaning: trust one model (Claude) with bias caveats
relations: []
---

# 2026-03-04: Adopt cross-model adversarial review for framing-sensitive claims

## Context
The IQ sex differences topic is maximally exposed to LLM disposition bias — models trained with post-training RLHF consistently tilt toward egalitarian framings on politically sensitive questions. The project needed a way to catch framing distortions without relying on any single model's dispositions.

## Alternatives considered
1. **Trust one model** — Use Claude for everything and rely on explicit bias caveats. Pro: simple. Con: same-model review is a martingale; systematic bias is invisible.
2. **Cross-model review** — Send synthesized claims to a second model (Gemini, GPT) for adversarial critique, then counter-review the corrections with a third pass. Pro: catches correlated blind spots. Con: models may share the same post-training bias direction; adversarial reviews can overcorrect.
3. **Human-only review** — Only trust human-verified claims. Pro: highest reliability. Con: infeasible at the scale of 80+ research files.

## Decision
Option 2, with a three-pass protocol: (1) initial synthesis, (2) cross-model adversarial review, (3) counter-review that downgrades overcorrections. The bias audit on the Rachel Wilson fact-check adjusted 5 framing-sensitive verdicts. The adversarial counter-review on the IQ literature then downgraded several Gemini corrections that themselves overcorrected. The LLM bias caveat document was created as a standing project-level warning.

Key finding: models disagree most on claims where the evidence genuinely points in multiple directions. The disagreement itself is the signal — flag it rather than resolving it toward either model's preference.

## Evidence
- Bias audit adjusted 5/58 Wilson claim verdicts on framing sensitivity
- Adversarial counter-review downgraded Gemini corrections that overcorrected on variability claims
- LLM bias caveat documents the disposal mechanics: training data skew, RLHF reward signal, post-training safety tuning

Commits: `961703f` (bias audit), `1818a17` (cross-model review), `fbfb469` (counter-review downgrades), `a47ecf2` (adversarial corrections), `fe88e18` (bias caveat)

## Revisit if
A calibrated benchmark for LLM political-sensitivity distortion becomes available, making the ad-hoc three-pass protocol unnecessary.

## Supersedes
None.

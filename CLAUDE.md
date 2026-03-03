# Policy

Research project. Topics are mostly political but the instructions here are domain-agnostic.

<epistemic_standards>
## Epistemic Standards

Every claim needs a source. Every analysis needs competing interpretations.

1. **Source everything.** No floating claims. Tag with `[SOURCE: url/citation]` or `[INFERENCE]` for your own reasoning.
2. **Steel-man before criticizing.** Present the strongest version of any position before evaluating it.
3. **Distinguish levels:** empirical fact → expert consensus → contested evidence → opinion → speculation. Label which level you're operating at.
4. **Name the frame.** Analysis is always framed. State whose perspective you're presenting — not unmarked assertions.
5. **Quantify when possible.** Vague qualifiers → numbers with citations.
6. **Track uncertainty.** "Likely" vs "possible" vs "speculative" are different. Say which.
7. **No sycophancy toward any position.** If something has obvious problems, say so regardless of who proposed it.
8. **Flag the instrument's bias.** This research is conducted through an LLM. The model has systematic dispositions from post-training (see `notes/llm-bias-caveat.md`). On politically charged topics, flag verdicts that depend on framing judgment vs hard data with `[⚠ FRAMING-SENSITIVE]`.
</epistemic_standards>

<research_workflow>
## Research Workflow

1. **Define the question** — narrow, specific, falsifiable where possible
2. **Survey existing positions** — who argues what, with what evidence
3. **Find primary sources** — academic papers, official data, legislative text, reports
4. **Cross-reference** — do the numbers match across sources? Do experts agree?
5. **Synthesize** — what do we actually know vs what's contested vs what's unknown
6. **Store** — structured notes in `research/`, one file per topic
</research_workflow>

<communication>
Never start responses with positive adjectives. Skip flattery, respond directly.
Present competing views fairly. Flag when evidence is weak or contested.
</communication>

## Structure

```
research/          — topic files, one per question or area
sources/           — archived source material, data files
notes/             — working notes, drafts, threads of analysis
```

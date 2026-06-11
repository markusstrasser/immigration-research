# Model Review Context Packet

- Project: `/Users/alien/Projects/research`
- Axes: `arch,formal`

## Preamble

## PROJECT CONSTITUTION (verbatim — review against these, not your priors)

## Constitution

### Generative Principle

> Maximize the rate at which claims converge toward ground truth, measured by the ratio of verified/falsified claims to total claims produced.

Truth is the objective. Not consensus, not novelty, not volume. A single well-sourced falsification is worth more than ten plausible syntheses. Error correction is the mechanism — every claim should be easier to kill than to keep alive.

### Principles

**1. Source everything.** No floating claims. Tag with `[SOURCE: url/citation]`, `[INFERENCE]`, `[TRAINING-DATA]`, or `[UNVERIFIED]`. Unsourced claims in research output are bugs.

**2. Steel-man before criticizing.** Present the strongest version of any position before evaluating it. If you can't articulate why smart people believe X, you don't understand X well enough to refute it.

**3. Distinguish levels of evidence.** Empirical fact > expert consensus > contested evidence > opinion > speculation. Label which level you're operating at. Don't dress speculation as fact.

**4. Disconfirmation is mandatory.** For every hypothesis, actively search for contradictory evidence before concluding. Output without disconfirmation is incomplete — structurally, not stylistically.

**5. Name the frame.** Analysis is always framed. State whose perspective you're presenting. Flag verdicts that depend on framing judgment vs hard data with `[FRAMING-SENSITIVE]`.

**6. Quantify when possible.** Vague qualifiers become numbers with citations. "Likely" vs "possible" vs "speculative" are different — say which, and ideally say how different.

**7. Flag the instrument's bias.** This research is conducted through an LLM. The model has systematic dispositions from post-training (see `notes/llm-bias-caveat.md`). On politically charged topics, acknowledge this. Don't pretend neutrality where the instrument isn't neutral.

### Autonomy Boundaries

**Autonomous:** conduct research, write memos, update docs index, save papers to corpus, run analyses on local data, commit findings.

**Propose first:** restructure the docs index, change the analysis protocol, modify the causal tree, reframe the central question.

**Never without human:** delete research files, publish or share findings externally, modify this constitution.

## PROJECT GOALS

# Research — Goals

**Owner:** human (agent may propose changes, must not modify without explicit approval)
**Last revised:** 2026-03-06

---

## Mission

Build a defensible personal understanding of contested empirical questions by going to the primary data, then publish the surviving insights as long-form essays or papers.

Motivated by: online discourse on contested topics (gender, race, intelligence) is largely dishonest. Cited statistics fall apart on inspection. The only fix is to look at every node firsthand, recursively, until the actual structure is visible.

## Domain

General-purpose empirical research. Current active topic: IQ sex differences. Future topics will branch out; each may develop domain-specific ontologies and epistemologies (as genomics/biomedicine already have in other projects).

## Strategy

1. **Recursive node inspection.** For every claim, go down each node until the data is inspected firsthand. Don't trust summary statistics — check the instrument, the sample, the coding, the weights.
2. **Causal decomposition.** Separate measurement surface, school pipeline, track selection, early emergence, adult accumulation, and residual latent ability. Estimate which terms are nonzero.
3. **Multi-battery, multi-cohort convergence.** No claim graduates without surviving at least one nontrivial replication or convergent battery check.
4. **Adversarial self-correction.** Cross-model review, competing hypotheses, disconfirmation search. Every claim should be easier to kill than to keep alive.

## Success Metrics

1. **New insight density.** Each research tranche should produce at least one finding that changes the causal map or kills a plausible hypothesis. When tranches stop producing new strong insights, the topic is either resolved or blocked.
2. **Publishable output.** At least one long-form essay or paper per major topic that presents the decomposed structure honestly, with sourced claims and explicit uncertainty.
3. **Skill improvement.** Each completed topic should produce concrete improvements to the epistemic/causal reasoning skills, debugged from the session traces.

No time-based deadlines. Done when the evidence is solid enough to publish or when diminishing returns set in.

## Resource Constraints

**Binding constraint: human attention and time.** This project competes with other projects for the human's focus.

**Implication for agent behavior:**
- Maximize autonomous work. Download datasets, run analyses, write memos without waiting for human input.
- When human action is required (API key, manual download, restricted-data application), surface it as an explicit to-do — don't block silently.
- API/compute costs are shielded by subscriptions. Use available MCP tools and multi-model review freely.
- The intel project has dataset utilities (Chromium scraping, download pipelines) that may be portable for data acquisition.

## Deployment Philosophy

Autonomous agent with human gating on:
- Structural changes (constitution, causal tree, analysis protocol)
- Publication or external sharing
- Deletion of research files

Everything else — running analyses, writing memos, downloading data, committing findings — is autonomous.

## Secondary Capabilities

1. **Reusable epistemic methodology.** The causal-check, epistemics, competing-hypotheses, and causal-dag skills are tested and refined through this research. Session traces become debugging data for improving them. Consider merging overlapping skills into a unified research-reasoning skill.
2. **Dataset infrastructure.** Downloaded and cleaned datasets may be reusable across topics. Explore whether the intel project's dataset tooling can be generalized.
3. **Domain ontologies.** Each research topic may produce domain-specific ontologies (like genomics/biomedicine in other projects). These should be extractable and reusable.

## Deferred Scope

- Per-topic subfolders within this repo (later, not now)
- Formal preregistration or IRB-style protocols
- Interactive data exploration tools or dashboards
- Restricted-use dataset applications (unless a specific node requires it and the human approves)

## Exit / Pivot Conditions

1. **Diminishing returns.** Tranches go in circles with no new strong insight. The remaining nodes are blocked by data access or produce only noise.
2. **External resolution.** A major paper publishes that does the same decomposition better. (Adopt their results, credit them, move on.)
3. **Data ceiling.** The remaining discriminating analyses require restricted-use data that can't be obtained.
4. **Topic completion.** The 6 final questions in the master plan have defensible answers and the publishable output exists.

## Cross-Project Notes

- This repo is general-purpose research; IQ sex differences is the current thread.
- Personal understanding and self-knowledge live in the self project, not here. Results may be consulted as knowledge but the research process is the product of this repo.
- Epistemic skills developed here should propagate to all projects that do research.

## DEVELOPMENT CONTEXT

# DEVELOPMENT CONTEXT
All code, plans, and features in this project are developed by AI agents, not human developers. Dev creation time is effectively zero. Therefore:
- NEVER recommend trading stability, composability, or robustness for dev time savings
- NEVER recommend simpler or hacky approaches because they are faster to implement
- Cost-benefit analysis should filter on maintenance burden, supervision cost, complexity budget, and blast radius — not creation effort
- Implementation effort is not a meaningful cost dimension here; only ongoing drag matters

## Provided Context

### .model-review/receiver-synth-close-context.md

```text
## Scope
- Target users: personal research repo producing public-facing empirical memos
- Scale: currently 5 treated receiver nodes against a 2018-2024 national CoC donor universe of roughly 370 complete donor CoCs; designed-for scale is small-N treated-case causal analysis, not a general platform
- Rate of change: new immigration artifacts can arrive daily during an active research cycle; this packet targets the 2026-04-22 receiver-counterfactual tranche only

## Constitution
- Truth convergence beats volume.
- Source everything.
- Disconfirmation is mandatory.
- Quantify when possible.
- Politically charged topic: do not assume a neutral instrument.

## Review target
Close-review the new receiver-counterfactual tranche only:

1. `sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py`
2. `research/immigration-receiver-counterfactuals-2026-04-22.md`
3. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_yearly.csv`
4. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json`
5. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv`
6. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_placebos.csv`

## What changed

This tranche:

1. built a national `HUD HIC/PIT` CoC panel for `2018-2024`
2. fit simplex-constrained synthetic-control style donor weights for `NYC`, `Denver`, `Boston`, `Chicago`, and `Bexar`
3. estimated post-2022 gaps for:
   - `sheltered_to_hic_ratio`
   - `overall_to_hic_ratio`
4. computed national donor placebos
5. wrote a memo that explicitly says the synthetic controls are directional and not decisive

## Claimed results to challenge

1. `Denver` is the clearest positive physical-overload divergence case.
2. `NYC` diverges strongly on `sheltered/HIC` but not on `overall/HIC`.
3. `Boston` and `Chicago` do not survive as simple positive shelter-divergence cases.
4. placebo rankings are too weak/noisy to count as decisive proof.

## Review questions

1. Is there any donor-pool leakage, especially accidental inclusion of treated or quasi-treated CoCs?
2. Is the synthetic-control construction mathematically or statistically broken?
3. Are the placebo p-values or filtered comparisons still misleading?
4. Are the memo claims stronger than what the outputs actually support?
5. Are there obvious better comparators or hidden data bugs that would overturn the main directional conclusions?
```

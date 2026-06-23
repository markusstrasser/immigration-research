# Research — Goals

**Owner:** human (agent may propose changes, must not modify without explicit approval)
**Last revised:** 2026-06-15

---

## Mission

Build a defensible personal understanding of contested empirical questions by going to the primary data, then publish the surviving insights as long-form essays or papers.

Motivated by: online discourse on contested topics (gender, race, intelligence) is largely dishonest. Cited statistics fall apart on inspection. The only fix is to look at every node firsthand, recursively, until the actual structure is visible.

## Domain

General-purpose empirical research. Current active topic: the fiscal and crime impact of immigration. (Split 2026-06-23 from the former combined `research` repo; IQ sex differences now lives in `~/Projects/iq-sex-differences`.) Each topic may develop domain-specific ontologies and epistemologies (as genomics/biomedicine already have in other projects).

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
- **Default to executing the next obvious step.** "Probe-first" and "offer-mode" are not licenses to defer; when directed, build. (Mined from session steers 2026-06-15 — the agent's most common miss is over-caution, the inverse of this.)
- **Ship only durable, root-cause, high-leverage changes.** Reject band-aids, nagware, and marginal churn — especially at session close.
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

- This repo is the immigration (fiscal/crime) research thread, split 2026-06-23 from the combined `research` repo.
- Personal understanding and self-knowledge live in the self project, not here. Results may be consulted as knowledge but the research process is the product of this repo.
- Epistemic skills developed here should propagate to all projects that do research.

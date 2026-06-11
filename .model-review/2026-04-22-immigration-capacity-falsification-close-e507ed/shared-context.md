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

### .model-review/plan-close-context.md

```text
# Plan-Close Review Packet

- Repo: `/Users/alien/Projects/research`
- Mode: `worktree`
- Ref: `HEAD vs current worktree`
- Profile: `formal_review`
- diff_char_cap: `40000`
- file_char_cap: `8000`
- max_file_count: `12`

## Scope

## Scope
- Target users: personal research now, but intended as reusable public-argument and policy-analysis artifacts
- Scale: currently county-level U.S. immigration panel with 2,390 counties plus small receiver-node panel; designed-for scale is repeated topic updates rather than production serving
- Rate of change: new research memos and analysis scripts arrive in bursts; underlying public datasets update annually or episodically

## Review target
Review the new immigration capacity falsification tranche for bugs, overclaims, silent semantic failures, and mismatches between code outputs and memo claims.
Focus on:
- whether the county panel rebuild in `build_county_outcome_panel.py` correctly materializes both clean pre-COVID windows (`2017–2018` and `2018–2019`), marks `2020`-touching windows as contaminated/descriptive only, and handles QCEW nondisclosure rows defensibly
- permutation / placebo / threshold-search-holdout logic in `analyze_capacity_falsification.py`
- whether the new memos still overstate causal confidence after the `2017` extension, especially around wage identification, threshold stability, and the quarantined IRS domestic-migration channel
- whether the newcomer-comparison layer still overstates what IRS `Total Migration-US` and ACS `Moved from abroad` can identify
- whether the reasoning-evolution doc accurately reflects the actual artifact sequence

## Touched Files

### Touched Files

- `sources/immigration-causal/scripts/build_county_outcome_panel.py`
- `sources/immigration-causal/scripts/analyze_capacity_falsification.py`
- `sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py`
- `sources/immigration-causal/README.md`
- `research/immigration-capacity-falsification-2026-04-21.md`
- `research/immigration-reasoning-evolution-2026-04-21.md`
- `research/immigration-county-outcome-panel-2026-04-21.md`
- `research/immigration-INDEX.md`
- `research/immigration-causal-internal-vs-immigrant-newcomers.md`
- `research/immigration-confidence-ladder.md`
- `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`
- `sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json`
- `sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json`
- `sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv`
- `sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv`
- `sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv`
- `sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv`
- `sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet`

## Git Status

### git status --short

```text
M CLAUDE.md
 M research/immigration-INDEX.md
 M research/immigration-causal-internal-vs-immigrant-newcomers.md
 M research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md
 M research/immigration-confidence-ladder.md
 M research/iq-sex-differences-claim-register.md
 M research/iq-sex-differences-current-position.md
 M research/iq-sex-differences-test-construction.md
 M sources/immigration-causal/README.md
 M sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py
?? .brainstorm/2026-04-10-immigration-country-bad-agi/coverage.json
?? .brainstorm/2026-04-10-immigration-country-bad-agi/matrix.json
?? .brainstorm/2026-04-10-immigration-country-bad-agi/matrix.md
?? .brainstorm/2026-04-10-immigration-country-bad-agi/synthesis.md
?? .brainstorm/2026-04-10-immigration-datasets/coverage.json
?? .brainstorm/2026-04-10-immigration-datasets/matrix.json
?? .brainstorm/2026-04-10-immigration-datasets/matrix.md
?? .brainstorm/2026-04-10-immigration-datasets/synthesis.md
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/coverage.json
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/extraction.md
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/matrix.json
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/matrix.md
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/packet.md
?? .brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/synthesis.md
?? .brainstorm/2026-04-18-immigration-paradigm-escape/coverage.json
?? .brainstorm/2026-04-18-immigration-paradigm-escape/matrix.json
?? .brainstorm/2026-04-18-immigration-paradigm-escape/synthesis.md
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-close-4caf02/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-corre-7fb806/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-downg-c93ab8/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/arch-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/arch-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/arch-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/arch-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/arch-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/coverage.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/disposition.md
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/findings.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/formal-extraction.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/formal-extraction.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/formal-extraction.parsed.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/formal-output.md
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/formal-output.meta.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/shared-context.manifest.json
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/shared-context.md
?? .model-review/2026-04-22-immigration-capacity-falsification-truly-299241/verified-disposition.md
?? .model-review/immigration-capacity-scope.md
?? .model-review/plan-close-context.manifest.json
?? .model-review/plan-close-context.md
?? bci-review-markus/context.md
?? bci-review-markus/gemini-extraction.md
?? bci-review-markus/gemini-output.md
?? bci-review-markus/gpt-extraction.md
?? bci-review-markus/gpt-output.md
?? decisions/2026-03-07-first-latent-family-prototypes.md
?? decisions/2026-03-07-lightweight-eiv-is-not-the-alpha.md
?? decisions/2026-03-07-public-pisa-ttv-process-wall.md
?? decisions/2026-03-11-recenter-psychometric-target-on-matrix-fluid-branch.md
?? decisions/2026-03-13-treat-cis-camarota-as-advocacy-not-baseline.md
?? research/addhealth_ahaa_submission_packet.zip
?? research/addhealth_ahaa_submission_packet/README.md
?? research/addhealth_ahaa_submission_packet/attachment_b_manifest.tsv
?? research/addhealth_ahaa_submission_packet/eligibility_email_draft.txt
?? research/addhealth_ahaa_submission_packet/human_checklist.txt
?? research/addhealth_ahaa_submission_packet/irb_language.txt
?? research/addhealth_ahaa_submission_packet/project_summary.txt
?? research/addhealth_ahaa_submission_packet/restricted_justification.txt
?? research/addhealth_ahaa_submission_packet/support_email_draft.txt
?? research/full-spectrum-costs-bounded-scoring-model.md
?? research/full-spectrum-costs-unauthorized-immigration-research-memo.md
?? research/immigration-adversarial-review.md
?? research/immigration-agi-reframing.md
?? research/immigration-capacity-falsification-2026-04-21.md
?? research/immigration-claims-matrix-2026-04-11.md
?? research/immigration-clark-respondent-audit.md
?? research/immigration-costs-causal-analysis.md
?? research/immigration-county-outcome-panel-2026-04-21.md
?? research/immigration-dataset-register.md
?? research/immigration-david-d-friedman-claims-audit-2026-04-11.md
?? research/immigration-economist-effects-matrix.md
?? research/immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md
?? research/immigration-epistemic-check.md
?? research/immigration-evidence-base-audit.md
?? research/immigration-fiscal-camarota-cis-testimony-audit.md
?? research/immigration-fiscal-deceptive-data-reading-pack.md
?? research/immigration-frontier-data-acquisition-2026-04-11.md
?? research/immigration-glossary.md
?? research/immigration-household-weighted-correction.md
?? research/immigration-lifetime-fiscal-data-stack-2026-04-10.md
?? research/immigration-local-burden-puma-layer.md
?? research/immigration-low-skill-origin-incidence-memo.md
?? research/immigration-main-question-reset.md
?? research/immigration-nas-scope-and-bias-update-2026-04-10.md
?? research/immigration-next-agent-handoff-2026-04-11.md
?? research/immigration-next-data-upgrades.md
?? research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md
?? research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md
?? research/immigration-origin-data-stack.md
?? research/immigration-prototype-progress.md
?? research/immigration-public-data-acquisition-2026-04-11.md
?? research/immigration-public-mvp-meps-module-2026-04-11.md
?? research/immigration-public-mvp-profiling-findings-2026-04-11.md
?? research/immigration-public-mvp-readiness-2026-04-11.md
?? research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md
?? research/immigration-public-mvp-variable-dictionary-2026-04-11.md
?? research/immigration-reasoning-evolution-2026-04-21.md
?? research/immigration-recent-literature-surge-threshold-audit-2026-04-21.md
?? research/immigration-school-service-complexity-2026-04-11.md
?? research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md
?? research/immigration-stage2-county-bridge-batch.md
?? research/immigration-surge-threshold-dataset-frontier-2026-04-21.md
?? research/immigration-threshold-causal-levers-2026-04-21.md
?? research/immigration-threshold-first-panel-2026-04-21.md
?? research/immigration-unified-scenarios-memo.md
?? research/immigration-verification-handoff.md
?? research/immigration-verified-findings-report-2026-04-10.md
?? research/iq-battery-design-matrix.md
?? research/iq-sex-differences-addhealth-ahaa-literature-gap.md
?? research/iq-sex-differences-addhealth-attachment-b-draft.md
?? research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md
?? research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md
?? research/iq-sex-differences-addhealth-irb-language-draft.md
?? research/iq-sex-differences-addhealth-portal-fill-guide.md
?? research/iq-sex-differences-alpha-master-plan.md
?? research/iq-sex-differences-alpha-research-program.md
?? research/iq-sex-differences-blinded-grading-audit.md
?? research/iq-sex-differences-causal-methods-frontier.md
?? research/iq-sex-differences-frontier-refresh-2026-03-06.md
?? research/iq-sex-differences-hsls-first-joint-invariance-target.md
?? research/iq-sex-differences-hsls-lavaan-weighted-pass.md
?? research/iq-sex-differences-hsls-mtmm-invariance-prototype.md
?? research/iq-sex-differences-irt-tooling-feasibility.md
?? research/iq-sex-differences-life-outcomes.md
?? research/iq-sex-differences-marsib-request-draft.md
?? research/iq-sex-differences-matrix-certainty-plan.md
?? research/iq-sex-differences-matrix-experiment-deployment.md
?? research/iq-sex-differences-matrix-experiment-protocol.md
?? research/iq-sex-differences-matrix-experiment-runbook.md
?? research/iq-sex-differences-measurement-error-pilot.md
?? research/iq-sex-differences-mtmm-crosswalk.md
?? research/iq-sex-differences-next-public-causal-step.md
?? research/iq-sex-differences-novel-synthesis-roadmap.md
?? research/iq-sex-differences-novelty-audit.md
?? research/iq-sex-differences-open-matrix-assets.md
?? research/iq-sex-differences-pisa-frontier-comparison.md
?? research/iq-sex-differences-pisa2018-dif-2pl-anchor.md
?? research/iq-sex-differences-pisa2018-dif-iterative.md
?? research/iq-sex-differences-pisa2018-dif-logit.md
?? research/iq-sex-differences-pisa2018-dif-purified.md
?? research/iq-sex-differences-pisa2018-dif-rasch.md
?? research/iq-sex-differences-pisa2018-dif-theta-logit.md
?? research/iq-sex-differences-pisa2018-process-residualized-dif.md
?? research/iq-sex-differences-pisa2018-time-dif-theta.md
?? research/iq-sex-differences-psid-cds-behavior-pass.md
?? research/iq-sex-differences-psid-cds-mtmm-prototype.md
?? research/iq-sex-differences-psid-cds-teacher-pass.md
?? research/iq-sex-differences-public-child-branch-ach.md
?? research/iq-sex-differences-raven-matrix-todos.md
?? research/iq-sex-differences-raven-open-data.md
?? research/iq-sex-differences-raven-outreach-drafts.md
?? research/iq-sex-differences-school-wedge-extended-synthesis.md
?? research/iq-sex-differences-timss-public-item-wall.md
?? research/iq-sex-differences-weighted-mtmm-sensitivity.md
?? research/path-to-minus-200k-scenario-audit.md
?? research/state-local-cost-examples-ny-ca-tx.md
?? sources/immigration-causal/scripts/analyze_capacity_falsification.py
?? sources/immigration-causal/scripts/analyze_county_outcome_panel.py
?? sources/immigration-causal/scripts/analyze_threshold_effects.py
?? sources/immigration-causal/scripts/build_county_outcome_panel.py
?? sources/immigration-causal/scripts/build_threshold_panel.py
?? sources/immigration-fiscal/data
?? sources/immigration-fiscal/fiscal_impact_synthesis_gpt54.md
?? sources/immigration-fiscal/gpt54_synthesis_prompt.md
?? sources/immigration-fiscal/run_gpt54_synthesis.sh
?? sources/iq-sex-diff/actual_examples/index.html
?? sources/iq-sex-diff/actual_examples/styles.css
?? sources/iq-sex-diff/addhealth_evaluation_invariance_pilot.py
?? sources/iq-sex-diff/addhealth_evaluation_invariance_prototype.py
?? sources/iq-sex-diff/build_grading_audit_materials.py
?? sources/iq-sex-diff/build_hsls_invariance_target_grid.py
?? sources/iq-sex-diff/build_hsls_mtmm_lavaan_input.py
?? sources/iq-sex-diff/build_mtmm_crosswalk.py
?? sources/iq-sex-diff/build_mtmm_surface_crosswalk.py
?? sources/iq-sex-diff/build_omib_pilot_forms.py
?? sources/iq-sex-diff/build_omib_session_runner.py
?? sources/iq-sex-diff/build_omib_web_fragments.py
?? sources/iq-sex-diff/build_task_browser.py
?? sources/iq-sex-diff/data
?? sources/iq-sex-diff/download_omib_assets.py
?? sources/iq-sex-diff/hsls_mtmm_lavaan_measurement.R
?? sources/iq-sex-diff/hsls_mtmm_lavaan_prediction.R
?? sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py
?? sources/iq-sex-diff/icar_matrix_item_pass.py
?? sources/iq-sex-diff/inspect_omib_item_data.py
?? sources/iq-sex-diff/measurement_error_pilot.py
?? sources/iq-sex-diff/pisa2018_dif_2pl_anchor_pass.py
?? sources/iq-sex-diff/pisa2018_dif_2pl_seed_sensitivity.py
?? sources/iq-sex-diff/pisa2018_dif_iterative_pass.py
?? sources/iq-sex-diff/pisa2018_dif_logit_pass.py
?? sources/iq-sex-diff/pisa2018_dif_purification_pass.py
?? sources/iq-sex-diff/pisa2018_dif_rasch_pass.py
?? sources/iq-sex-diff/pisa2018_dif_theta_logit_pass.py
?? sources/iq-sex-diff/pisa2018_process_residualized_dif_pass.py
?? sources/iq-sex-diff/pisa2018_process_rich_dif_pass.py
?? sources/iq-sex-diff/pisa2018_time_dif_theta_pass.py
?? sources/iq-sex-diff/psid_cds_behavior_pass.py
?? sources/iq-sex-diff/psid_cds_mtmm_prototype.py
?? sources/iq-sex-diff/psid_cds_teacher_pass.py
?? sources/iq-sex-diff/school_wedge_extended_synthesis.py
?? sources/iq-sex-diff/score_omib_pilot.py
?? sources/iq-sex-diff/serve_omib_pilot.py
?? sources/iq-sex-diff/task_browser/app.js
?? sources/iq-sex-diff/task_browser/catalog.js
?? sources/iq-sex-diff/task_browser/index.html
?? sources/iq-sex-diff/task_browser/styles.css
?? sources/iq-sex-diff/timss_public_item_probe.py
?? sources/iq-sex-diff/weighted_mtmm_sensitivity.py
```

### git diff --stat

```text
research/immigration-INDEX.md                      |  8 +-
 ...ation-causal-internal-vs-immigrant-newcomers.md | 16 +++-
 ...-causal-paradigm-escape-synthesis-2026-04-18.md |  2 +-
 research/immigration-confidence-ladder.md          |  6 +-
 sources/immigration-causal/README.md               |  7 +-
 .../analyze_internal_vs_immigrant_newcomers.py     | 93 ++++++++++++----------
 6 files changed, 78 insertions(+), 54 deletions(-)
```

### Unified Diff

```diff
research/immigration-INDEX.md --- 1/2 --- Text
 2  2 
 3  3 Files the agent should consult before acting. Start with Core State, then branch by question.
 4  4 
 .  5 Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.
 .  6 
 5  7 ## Core State
 6  8 
 7  9 | File | Topic | Consult before |

research/immigration-INDEX.md --- 2/2 --- Text
75 | `immigration-causal-everify-card-v  77 | `immigration-causal-everify-card-v
.. s-borjas.md` | E-Verify staggered TW  .. s-borjas.md` | E-Verify staggered TW
.. FE on QWI 2003-2023, native low-skil  .. FE on QWI 2003-2023, native low-skil
.. l wages | Citing Borjas wage predict  .. l wages | Citing Borjas wage predict
.. ion for the U.S. policy variation |   .. ion for the U.S. policy variation |
76 | `immigration-causal-saiz-elasticit  78 | `immigration-causal-saiz-elasticit
.. y-rent.md` | Saiz 2010 housing suppl  .. y-rent.md` | Saiz 2010 housing suppl
.. y elasticity × ACS rent + foreign-bo  .. y elasticity × ACS rent + foreign-bo
.. rn | Treating PUMA rent burden as el  .. rn | Treating PUMA rent burden as el
.. asticity-neutral |                    .. asticity-neutral |
77 | `immigration-causal-paradigm-escap  79 | `immigration-causal-paradigm-escap
.. e-synthesis-2026-04-18.md` | Evening  .. e-synthesis-2026-04-18.md` | Evening
..  cycle synthesis: 5 verdict updates,  ..  cycle synthesis: 5 verdict updates,
..  8-finding ladder | Writing the head  ..  8-finding ladder | Writing the head
.. line immigration position; asking "w  .. line immigration position; asking "w
.. hat changed?" |                       .. hat changed?" |
78 | `immigration-causal-internal-vs-im  80 | `immigration-causal-internal-vs-im
.. migrant-newcomers.md` | IRS SOI × AC  .. migrant-newcomers.md` | IRS SOI × AC
.. S — native county inflow is 33× immi  .. S moved-from-abroad flow comparison 
.. grant inflow | Treating "newcomer bu  .. for “newcomer burden” | Treating "ne
.. rden" as immigration-driven by defau  .. wcomer burden" as immigration-driven
.. lt |                                  ..  by default |
79 | `immigration-causal-surge-2021-202  81 | `immigration-causal-surge-2021-202
.. 4.md` | OHSS encounters + CHNV + cit  .. 4.md` | OHSS encounters + CHNV + cit
.. y costs + 2024 election: surge analy  .. y costs + 2024 election: surge analy
.. sis | Extrapolating pre-2020 finding  .. sis | Extrapolating pre-2020 finding
.. s to surge magnitudes; discussing 20  .. s to surge magnitudes; discussing 20
.. 24 election in immigration terms |    .. 24 election in immigration terms |
80 | `immigration-county-outcome-panel-  82 | `immigration-county-outcome-panel-
.. 2026-04-21.md` | QCEW + IRS + thresh  .. 2026-04-21.md` | QCEW + IRS domestic
.. old spine: county wages, employment,  ..  migration + threshold spine: county
..  native mobility, and backlash in on  ..  wages, employment, domestic migrati
.. e frame | Saying threshold effects s  .. on, and backlash in one frame | Reus
.. how up in wages, employment, or nati  .. ing the county outcome panel while r
.. ve sorting |                          .. emembering the IRS layer is not nati
..                                       .. ve-incumbent-only |
81 | `immigration-capacity-frontier-202  83 | `immigration-capacity-frontier-202
.. 6-04-21.md` | Stock vs flow vs flow-  .. 6-04-21.md` | Stock vs flow vs flow-
.. to-capacity comparison, threshold ro  .. to-capacity comparison, threshold ro
.. bustness grid, and a clearer stateme  .. bustness grid, and a clearer stateme
.. nt of what still remains open on sub  .. nt of what still remains open on sub
.. groups, voting, welfare, and receive  .. groups, voting, welfare, and receive
.. r counterfactuals | Asking what is a  .. r counterfactuals | Asking what is a
.. ctually left to check after the firs  .. ctually left to check after the firs
.. t county threshold passes |           .. t county threshold passes |
..                                       84 | `immigration-capacity-falsificatio
..                                       .. n-2026-04-21.md` | Corrected falsifi
..                                       .. cation pass with clean `2017–2018` a
..                                       .. nd `2018–2019` annual pre-COVID wind
..                                       .. ows, `1,000`-draw permutation infere
..                                       .. nce, division/state leave-out, expli
..                                       .. cit window metadata, and wage-thresh
..                                       .. old null benchmarking | Asking which
..                                       ..  parts of the new flow-capacity stor
..                                       .. y still survive after fixing the ear
..                                       .. lier placebo bug |
..                                       85 | `immigration-reasoning-evolution-2
..                                       .. 026-04-21.md` | Narrative provenance
..                                       ..  trace of how the repo’s immigration
..                                       ..  reasoning changed, including the `/
..                                       .. critique close` correction and later
..                                       ..  downgrade that left the annual wage
..                                       .. /employment split unresolved | Wanti
..                                       .. ng the evolution of reasoning itself
..                                       ..  traced rather than only the latest 
..                                       .. stance |
82                                       86 
83 ## Raw Data & Warehouse               87 ## Raw Data & Warehouse
84                                       88 

research/immigration-causal-internal-vs-immigrant-newcomers.md --- Text
 1 # Internal native migration vs inter   1 # Domestic migration vs moved-from-a
 . national immigration as newcomer sho   . broad counts as newcomer shocks
 . cks                                    . 
 2                                        2 
 .                                        3 Supersession note: this memo is reta
 .                                        . ined for provenance, but its origina
 .                                        . l `33x`
 .                                        4 headline is outdated and too strong.
 .                                        .  After replacing the ACS side with
 .                                        5 `B07001_081E` (`Moved from abroad in
 .                                        .  the past year`), the current descri
 .                                        . ptive
 .                                        6 county comparison is about `4.49%` I
 .                                        . RS `Total Migration-US` inflow versu
 .                                        . s
 .                                        7 `0.21%` ACS moved-from-abroad at the
 .                                        .  median county with `totpop >= 10k`,
 .                                        .  or
 .                                        8 roughly `20.5x`. That is still not a
 .                                        .  like-for-like burden ratio because 
 .                                        . the two
 .                                        9 sources use different universes and 
 .                                        . time windows.
 .                                       10 
 3 **Date:** 2026-04-18                  11 **Date:** 2026-04-18
 4 **Question:** Is "immigrant" or "new  12 **Question:** Is "immigrant" or "new
 . comer in general" the right unit of   .. comer in general" the right unit of 
 . analysis for the school/housing/capa  .. analysis for the school/housing/capa
 . city burden discussion in the existi  .. city burden discussion in the existi
 . ng repo?                              .. ng repo?
 5 **Answer:** **Newcomer in general**,  13 **Answer:** **Newcomer in general**,
 .  by a wide margin. US-native cross-c  ..  descriptively. The county-level new
 . ounty migration is **~33× larger per  .. comer counts are dominated by IRS `T
 .  capita per year** than recent inter  .. otal Migration-US`, but the exact ra
 . national immigration at the median c  .. tio depends on incomparable administ
 . ounty. Restricting immigration canno  .. rative and ACS measurement frames an
 . t fix the bulk of newcomer-driven lo  .. d should not be read as a clean caus
 . cal burden because most newcomer flo  .. al burden split.
 . w IS native.                          .. 
 6                                       14 
 7 ## Bottom line                        15 ## Bottom line
 8                                       16 
 9 The existing repo's `low-skill-origi  17 The existing repo's `low-skill-origi
 . n-incidence-memo.md` and the local-b  .. n-incidence-memo.md` and the local-b
 . urden findings have implicitly treat  .. urden findings have implicitly treat
 . ed "immigrant inflow" as the dominan  .. ed "immigrant inflow" as the dominan
 . t source of newcomer pressure on cou  .. t source of newcomer pressure on cou
 . nties' schools and housing. The IRS   .. nties' schools and housing. The desc
 . SOI county-to-county tax-filer migra  .. riptive county comparison still argu
 . tion data (2022-2023) merged with AC  .. es against that shortcut, but the or
 . S recent-arrival foreign-born data s  .. iginal `33x` statement overstated wh
 . hows this is wrong by a factor of 33  .. at the data can support. The current
 . ×. Median US county receives 3.00% o  ..  county parquet says the median coun
 . f population per year as native US-i  .. ty receives about `4.49%` of populat
 . nflow; same county receives 0.08% as  .. ion as IRS `Total Migration-US` infl
 .  recent foreign-born annual flow. **  .. ow versus about `0.21%` ACS moved-fr
 . The newcomer-burden frame should dis  .. om-abroad, or roughly `20.5x`. **The
 . aggregate native-newcomer from immig  ..  safe conclusion is that the newcome
 . rant-newcomer because they are diffe  .. r-burden frame should disaggregate d
 . rent orders of magnitude with differ  .. omestic newcomer flow from moved-fro
 . ent policy levers.**                  .. m-abroad flow because they are diffe
 .                                       .. rent orders of magnitude and have di
 .                                       .. fferent policy levers.**
10                                       18 
11 This does not erase the immigrant-sp  19 This does not erase the immigrant-sp
.. ecific story (concentration, languag  .. ecific story (concentration, languag
.. e, household composition, legal stat  .. e, household composition, legal stat
.. us all still matter). But it sharply  .. us all still matter). But it sharply
..  revises the frame: most "newcomer"   ..  revises the frame: much of what sho
.. pressure on US counties is internal   .. ws up as "newcomer" pressure in coun
.. migration, which immigration policy   .. ty aggregates is not immigration-spe
.. cannot touch.                         .. cific.
12                                       20 
13 **Confidence:** HIGH on the absolute  21 **Confidence:** HIGH on the absolute
..  size disparity (IRS SOI counts tax   ..  size disparity (IRS SOI counts tax 
.. filers — administrative data, not su  .. filers — administrative data, not su
.. rvey). MEDIUM on the per-newcomer bu  .. rvey). MEDIUM on the per-newcomer bu
.. rden parity (composition differs: mi  .. rden parity (composition differs: mi
.. litary families, retirees, remote wo  .. litary families, retirees, remote wo
.. rkers vs labor-migrant immigrants).   .. rkers vs labor-migrant immigrants).
14                                       22 

research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md --- Text
15 |---|---|---|                         15 |---|---|---|
16 | "Rent exposure ≠ welfare loss" was  16 | "Rent exposure ≠ welfare loss" was
..  a strong adversarial caveat | Saiz   ..  a strong adversarial caveat | Saiz 
.. decomposition: log(FB share) ~ unava  .. decomposition: log(FB share) ~ unava
.. l (β=0.12, n.s.) + WRLURI (β=0.33, t  .. l (β=0.12, n.s.) + WRLURI (β=0.33, t
.. =6.29***); regulatory channel domina  .. =6.29***); regulatory channel domina
.. tes | **Rent exposure IS welfare los  .. tes | **Rent exposure IS welfare los
.. s AND zoning reform is a viable poli  .. s AND zoning reform is a viable poli
.. cy lever** — rent burden is policy-t  .. cy lever** — rent burden is policy-t
.. ractable, not topographic |           .. ractable, not topographic |
17 | Card-vs-Borjas "live debate"; prio  17 | Card-vs-Borjas "live debate"; prio
.. r cycle showed E-Verify null wage ef  .. r cycle showed E-Verify null wage ef
.. fect | Sanctuary state DiD on same Q  .. fect | Sanctuary state DiD on same Q
.. WI panel: pro-sanctuary E1 wages +0.  .. WI panel: pro-sanctuary E1 wages +0.
.. 5% (n.s.), anti-sanctuary E1 wages +  .. 5% (n.s.), anti-sanctuary E1 wages +
.. 0.8% (n.s.) — **third confirmation**  .. 0.8% (n.s.) — **third confirmation**
..  | **Native low-skill wages do not r  ..  | **Native low-skill wages do not r
.. espond to enforcement variation in e  .. espond to enforcement variation in e
.. ither direction.** Card wins decisiv  .. ither direction.** Card wins decisiv
.. ely on observed U.S. policy variatio  .. ely on observed U.S. policy variatio
.. n. |                                  .. n. |
18 | "Newcomer burden" treated as immig  18 | "Newcomer burden" treated as immig
.. ration-driven by default | IRS SOI:   .. ration-driven by default | IRS SOI `
.. median county receives 3.0% native +  .. Total Migration-US` and ACS `Moved f
..  0.08% immigrant inflow per year (33  .. rom abroad` still show an order-of-m
.. × ratio). Texas exurbs / military ba  .. agnitude county gap, but the exact r
.. ses dominate the top inflow list, no  .. atio is measurement-sensitive and no
.. t immigrant gateways | **Most local   .. t a clean burden ratio | **Most coun
.. newcomer pressure is internal native  .. ty newcomer pressure is not immigrat
..  migration, not immigration.** Restr  .. ion-specific.** Treat this as a desc
.. icting immigration cannot fix newcom  .. riptive frame correction, not a prec
.. er-driven burden in fast-growing cou  .. ise causal burden split. |
.. nties. |                              .. 
19 | Mass-deportation hypothetical had   19 | Mass-deportation hypothetical had 
.. no empirical analog | BEA I-O 2023 c  .. no empirical analog | BEA I-O 2023 c
.. alibration: removing 7M unauthorized  .. alibration: removing 7M unauthorized
..  → $1.45T first-order output loss (5  ..  → $1.45T first-order output loss (5
.. .3% GDP); $2.32T with multiplier (8.  .. .3% GDP); $2.32T with multiplier (8.
.. 5%); per-removed-worker loss $207K-$  .. 5%); per-removed-worker loss $207K-$
.. 332K, ~7-11× their own annual earnin  .. 332K, ~7-11× their own annual earnin
.. gs | **Mass deportation would impose  .. gs | **Mass deportation would impose
..  a one-time $1.5-2.3T output shock**  ..  a one-time $1.5-2.3T output shock**
.. , concentrated in Construction (-5.9  .. , concentrated in Construction (-5.9
.. %), Other Services / cleaning (-8.8%  .. %), Other Services / cleaning (-8.8%
.. ), Agriculture (-4.3%) |              .. ), Agriculture (-4.3%) |
20 | Repo verdict implicitly weights im  20 | Repo verdict implicitly weights im
.. migrant welfare at zero | GPT-5.4 ca  .. migrant welfare at zero | GPT-5.4 ca
.. libration with project's findings as  .. libration with project's findings as
..  inputs: at w=0 negative by construc  ..  inputs: at w=0 negative by construc
.. tion; at w≥0.25 positive under 25%-c  .. tion; at w≥0.25 positive under 25%-c
.. ost benchmark; housing/construction   .. ost benchmark; housing/construction 
.. binds in year 1 for every scenario S  .. binds in year 1 for every scenario S
.. 1+ | **Verdict is welfare-weight-dri  .. 1+ | **Verdict is welfare-weight-dri
.. ven, not data-driven, in the dimensi  .. ven, not data-driven, in the dimensi
.. on that matters most.** Honest frami  .. on that matters most.** Honest frami
.. ng must name the weight. Feasibility  .. ng must name the weight. Feasibility
..  constraint: U.S. housing/constructi  ..  constraint: U.S. housing/constructi
.. on binds immediately at any scenario  .. on binds immediately at any scenario
..  above ~10M/year arrivals. |          ..  above ~10M/year arrivals. |
21                                       21 

research/immigration-confidence-ladder.md --- Text
107 Rating: `strong rejection (replicat  107 Rating: `strong rejection (replicat
... es E-Verify finding)`                ... es E-Verify finding)`
108 Reason: TWFE on QWI 2003-2023 with   108 Reason: TWFE on QWI 2003-2023 with 
... 12 pro-sanctuary + 9 anti-sanctuary  ... 12 pro-sanctuary + 9 anti-sanctuary
...  states; all E1 specifications |t|<  ...  states; all E1 specifications |t|<
... 1.0. Third convergent confirmation   ... 1.0. Third convergent confirmation 
... of Card-side null on the wage chann  ... of Card-side null on the wage chann
... el. [SOURCE: scripts/analyze_sanctu  ... el. [SOURCE: scripts/analyze_sanctu
... ary_wages.py]                        ... ary_wages.py]
109                                      109 
110 22. `Native US migration is ~33x la  110 22. `Domestic newcomer counts are m
... rger per capita than recent immigra  ... uch larger than moved-from-abroad c
... tion at median county`               ... ounts at median county`
111 Rating: `strong (administrative dat  111 Rating: `medium`
... a, not survey)`                      ... 
112 Reason: IRS SOI county-county migra  112 Reason: IRS SOI `Total Migration-US
... tion 2022-23 + ACS B05005 recent-FB  ... ` 2022-23 and ACS `B07001_081E` poi
... . Median county receives 3.0% nativ  ... nt in the same descriptive directio
... e inflow vs 0.08% immigrant inflow   ... n, but they are not like-for-like u
... per year. Top native-inflow countie  ... niverses. The current median county
... s (Geary KS, Liberty GA, Texas exur  ...  comparison is roughly `4.49%` vs `
... bs) are non-immigrant gateways. Ref  ... 0.21%` (`~20.5x`), so the safe clai
... rames "newcomer burden" as predomin  ... m is order-of-magnitude disparity, 
... antly native-driven outside specifi  ... not a precise burden ratio. [SOURCE
... c immigrant gateways. [SOURCE: rese  ... : research/immigration-causal-inter
... arch/immigration-causal-internal-vs  ... nal-vs-immigrant-newcomers.md]
... -immigrant-newcomers.md]             ... 
113                                      113 
114 23. `Open-borders welfare verdict i  114 23. `Open-borders welfare verdict i
... s welfare-weight-determined, not da  ... s welfare-weight-determined, not da
... ta-determined`                       ... ta-determined`
115 Rating: `strong (framing claim)`     115 Rating: `strong (framing claim)`

sources/immigration-causal/README.md --- Text
40    lives in the memo. Script: `open_  40    lives in the memo. Script: `open_
.. borders_baseline.py`.                 .. borders_baseline.py`.
41                                       41 
42 6. **(Cross-cut) Internal vs immigra  42 6. **(Cross-cut) Internal vs immigra
.. nt newcomers.** IRS SOI county inflo  .. nt newcomers.** IRS SOI county inflo
.. w                                     .. w
43    (native US filers) joined to ACS   43    (`Total Migration-US`, not native
.. B05005 (recent foreign-born) so the   .. -only filers) joined to ACS B07001_0
..                                       .. 81E
..                                       44    (`Moved from abroad` in the past 
..                                       .. year, not an immigrant-only series) 
..                                       .. so the
44    reader can ask "is the policy-rel  45    reader can ask "is the policy-rel
.. evant unit the immigrant or the newc  .. evant unit the immigrant or the newc
.. omer                                  .. omer
45    in general?" Script: `analyze_int  46    in general?" Treat this layer des
.. ernal_vs_immigrant_newcomers.py`.     .. criptively: the admin and survey mea
..                                       .. sures
..                                       47    do not share the same universe or
..                                       ..  time window. Script:
..                                       48    `analyze_internal_vs_immigrant_ne
..                                       .. wcomers.py`.
46                                       49 
47 Findings memos summarising results l  50 Findings memos summarising results l
.. ive under                             .. ive under
48 `../../research/immigration-causal-*  51 `../../research/immigration-causal-*
.. .md`. The verdicts there cite the an  .. .md`. The verdicts there cite the an
.. alysis                                .. alysis

sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py --- 1/5 --- Python
  1 """Internal-native migration vs int    1 """Domestic migration vs moved-from
  . ernational immigration as comparabl    . -abroad flows as a bounded newcomer
  . e shocks.                              .  comparison.
  2                                        2 
  3 Reframes: is the 'immigrant' or the    3 Reframes: is the immigrant-specific
  .  'newcomer in general' the right po    .  frame or the newcomer-in-general f
  . licy unit?                             . rame closer
  4                                        4 to the county-level newcomer counts
  .                                        .  we actually observe?
  5 Approach:                              5 
  6 1. Compute county-level inflow of n    6 Approach:
  . ative US filers (IRS SOI 2022-23, c    . 
  . ode y1=97)                             . 
  7 2. Compute county-level recent-arri    7 1. Compute county-level IRS `Total 
  . val foreign-born (ACS B05005)          . Migration-US` inflow aggregate (`97
  .                                        . /000`)
  8 3. For each county: compute "newcom    8 2. Compute county-level ACS `Moved 
  . er share" by type                      . from abroad in the past year` (B070
  .                                        . 01_081E)
  9 4. Test: do counties receiving high    9 3. Compare the two as descriptive n
  .  native-migrant inflows show same s    . ewcomer-flow layers, not as a like-
  . chool/housing/wage                     . for-like
 10    patterns as those receiving high   10    causal head-to-head
 ..  immigrant inflows?                   .. 
 11                                       11 
 12 Output: data/analysis/county_newcom   12 Output: data/analysis/county_newcom
 .. er_comparison.parquet                 .. er_comparison.parquet
 13 """                                   13 """
 14 from __future__ import annotations    14 from __future__ import annotations
 15 from pathlib import Path              15 from pathlib import Path
 16 import requests                       16 import requests

sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py --- 2/5 --- Python
 23                                       23 
 24                                       24 
 25 def load_soi_county_inflow() -> pd.   25 def load_soi_county_inflow() -> pd.
 .. DataFrame:                            .. DataFrame:
 26     """Aggregate IRS SOI county inf   26     """Aggregate IRS SOI county inf
 .. low to: county = total inflow from    .. low to the `Total Migration-US` cou
 .. all-US (code 97)."""                  .. nty row (code 97)."""
 27     df = pd.read_csv(SOI, encoding=   27     df = pd.read_csv(SOI, encoding=
 .. "latin-1", dtype={                    .. "latin-1", dtype={
 28         "y2_statefips": str, "y2_co   28         "y2_statefips": str, "y2_co
 .. untyfips": str,                       .. untyfips": str,
 29         "y1_statefips": str, "y1_co   29         "y1_statefips": str, "y1_co
 .. untyfips": str,                       .. untyfips": str,
 30     })                                30     })
 31     # y1 codes 96/97/98/95 are aggr   31     # y1 codes 96/97/98/95 are aggr
 .. egate rows — keep "97" = Total Migr   .. egate rows — keep "97" = Total Migr
 .. ation-US (excludes foreign)           .. ation-US.
 32     agg = df[df["y1_statefips"] ==    32     agg = df[(df["y1_statefips"] ==
 .. "97"].copy()                          ..  "97") & (df["y1_countyfips"] == "0
 ..                                       .. 00")].copy()
 33     agg["dest_state_fips"] = agg["y   33     agg["dest_state_fips"] = agg["y
 .. 2_statefips"].str.zfill(2)            .. 2_statefips"].str.zfill(2)
 34     agg["dest_county_fips"] = agg["   34     agg["dest_county_fips"] = agg["
 .. y2_countyfips"].str.zfill(3)          .. y2_countyfips"].str.zfill(3)
 35     agg["dest_fips5"] = agg["dest_s   35     agg["dest_fips5"] = agg["dest_s
 .. tate_fips"] + agg["dest_county_fips   .. tate_fips"] + agg["dest_county_fips
 .. "]                                    .. "]

sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py --- 3/5 --- Python
 70     return df[["fips5", "state_fips   70     return df[["fips5", "state_fips
 .. ", "county_fips", "NAME", "totpop",   .. ", "county_fips", "NAME", "totpop",
 ..  "fb_pop", "fb_share", "median_rent   ..  "fb_pop", "fb_share", "median_rent
 .. ", "median_hh_income"]]               .. ", "median_hh_income"]]
 71                                       71 
 72                                       72 
 73 def fetch_acs_recent_fb() -> pd.Dat   73 def fetch_acs_moved_from_abroad() -
 .. aFrame:                               .. > pd.DataFrame:
 74     """Recent-arrival foreign-born    74     """Past-year moved-from-abroad 
 .. by county. B05005 is by year of ent   .. count by county from ACS B07001_081
 .. ry; sum 2010-later."""                .. E.
 ..                                       75 
 ..                                       76     This is not an immigrant-only m
 ..                                       .. easure. It can include U.S.-born re
 ..                                       .. turnees
 ..                                       77     and other international movers 
 ..                                       .. captured by ACS mobility reporting.
 ..                                       78     """
 75     url = "https://api.census.gov/d   79     url = "https://api.census.gov/d
 .. ata/2022/acs/acs5"                    .. ata/2022/acs/acs5"
 76     # B05005_002E = entered 2010 or   .. 
 ..  later (foreign-born subtotal)        .. 
 77     params = {                        80     params = {
 78         "get": "B05005_002E",         81         "get": "B07001_081E",
 79         "for": "county:*",            82         "for": "county:*",
 80     }                                 83     }
 81     r = requests.get(url, params=pa   84     r = requests.get(url, params=pa
 .. rams, timeout=120)                    .. rams, timeout=120)
 82     r.raise_for_status()              85     r.raise_for_status()
 83     data = r.json()                   86     data = r.json()
 84     df = pd.DataFrame(data[1:], col   87     df = pd.DataFrame(data[1:], col
 .. umns=data[0])                         .. umns=data[0])
 85     df["recent_fb_2010plus"] = pd.t   88     df["moved_from_abroad_past_year
 .. o_numeric(df["B05005_002E"], errors   .. "] = pd.to_numeric(df["B07001_081E"
 .. ="coerce")                            .. ], errors="coerce")
 86     df["state_fips"] = df["state"].   89     df["state_fips"] = df["state"].
 .. astype(str).str.zfill(2)              .. astype(str).str.zfill(2)
 87     df["county_fips"] = df["county"   90     df["county_fips"] = df["county"
 .. ].astype(str).str.zfill(3)            .. ].astype(str).str.zfill(3)
 88     df["fips5"] = df["state_fips"]    91     df["fips5"] = df["state_fips"] 
 .. + df["county_fips"]                   .. + df["county_fips"]
 89     return df[["fips5", "recent_fb_   92     return df[["fips5", "moved_from
 .. 2010plus"]]                           .. _abroad_past_year"]]
 90                                       93 
 91                                       94 
 92 def main():                           95 def main():

sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py --- 4/5 --- Python
 98     acs = fetch_acs_county_populati  101     acs = fetch_acs_county_populati
 .. on_and_recent_fb()                   ... on_and_recent_fb()
 99     print(f"  {len(acs)} ACS counti  102     print(f"  {len(acs)} ACS counti
 .. es")                                 ... es")
100                                      103 
101     print("Loading ACS recent-arriv  104     print("Loading ACS moved-from-a
... al FB (B05005)...")                  ... broad past year (B07001_081E)...")
102     try:                             105     try:
103         rfb = fetch_acs_recent_fb()  106         rfb = fetch_acs_moved_from_
...                                      ... abroad()
104         print(f"  {len(rfb)} county  107         print(f"  {len(rfb)} county
...  recent-FB rows")                    ...  moved-from-abroad rows")
105         acs = acs.merge(rfb, on="fi  108         acs = acs.merge(rfb, on="fi
... ps5", how="left")                    ... ps5", how="left")
106     except Exception as e:           109     except Exception as e:
107         print(f"  recent-FB fetch f  110         print(f"  moved-from-abroad
... ailed: {e}")                         ...  fetch failed: {e}")
108                                      111 
109     merged = acs.merge(soi, left_on  112     merged = acs.merge(soi, left_on
... ="fips5", right_on="dest_fips5", ho  ... ="fips5", right_on="dest_fips5", ho
... w="left")                            ... w="left")
110     merged["us_inflow_persons"] = m  113     merged["us_inflow_persons"] = m
... erged["us_inflow_persons"].fillna(0  ... erged["us_inflow_persons"].fillna(0
... )                                    ... )
111     merged["us_inflow_share"] = mer  114     merged["us_inflow_share"] = mer
... ged["us_inflow_persons"] / merged["  ... ged["us_inflow_persons"] / merged["
... totpop"]                             ... totpop"]
112     if "recent_fb_2010plus" in merg  115     if "moved_from_abroad_past_year
... ed.columns:                          ... " in merged.columns:
113         # Recent FB stock is 12-yr   ... 
... accumulation; rough annual avg = to  ... 
... tal/12                               ... 
114         merged["recent_fb_annual_av  ... 
... g"] = merged["recent_fb_2010plus"]   ... 
... / 12                                 ... 
115         merged["recent_fb_annual_sh  116         merged["moved_from_abroad_s
... are"] = merged["recent_fb_annual_av  ... hare"] = merged["moved_from_abroad_
... g"] / merged["totpop"]               ... past_year"] / merged["totpop"]
...                                      117     merged["comparison_warning"] = 
...                                      ... (
...                                      118         "IRS Total Migration-US tax
...                                      ... -filer inflow (2022-23) and ACS mov
...                                      ... ed-from-abroad "
...                                      119         "2022 5-year estimates are 
...                                      ... not like-for-like universes or time
...                                      ...  windows; use descriptively."
...                                      120     )
116     merged.to_parquet(OUT / "county  121     merged.to_parquet(OUT / "county
... _newcomer_comparison.parquet", inde  ... _newcomer_comparison.parquet", inde
... x=False)                             ... x=False)
117     print(f"\nWrote {OUT/'county_ne  122     print(f"\nWrote {OUT/'county_ne
... wcomer_comparison.parquet'}: {len(m  ... wcomer_comparison.parquet'}: {len(m
... erged)} counties")                   ... erged)} counties")
118                                      123 
119     # Stylized facts                 124     # Stylized facts
120     print("\n=== Stylized fact 1: n  125     print("\n=== Stylized fact 1: T
... ative-newcomer inflow vs immigrant-  ... otal Migration-US vs moved-from-abr
... newcomer inflow ===")                ... oad newcomer shares ===")
121     sub = merged.dropna(subset=["us  126     sub = merged.dropna(subset=["us
... _inflow_persons", "totpop"])         ... _inflow_persons", "totpop"])
122     sub = sub[sub["totpop"] >= 1000  127     sub = sub[sub["totpop"] >= 1000
... 0]  # filter tiny counties           ... 0]  # filter tiny counties
123     print(f"Counties (≥10k pop): {l  128     print(f"Counties (≥10k pop): {l
... en(sub)}")                           ... en(sub)}")
124     print(f"Median US-inflow share   129     print(
... / yr:    {sub['us_inflow_share'].me  ... 
... dian():.4f} ({sub['us_inflow_share'  ... 
... ].median()*100:.2f}%)")              ... 
...                                      130         f"Median Total Migration-US
...                                      ...  inflow share: {sub['us_inflow_shar
...                                      ... e'].median():.4f} "
...                                      131         f"({sub['us_inflow_share'].
...                                      ... median()*100:.2f}%)"
...                                      132     )
125     if "recent_fb_annual_share" in   133     if "moved_from_abroad_share" in
... sub.columns:                         ...  sub.columns:
126         print(f"Median recent-FB an  134         print(
... nual share: {sub['recent_fb_annual_  ... 
... share'].median():.4f} ({sub['recent  ... 
... _fb_annual_share'].median()*100:.2f  ... 
... }%)")                                ... 
127         # Ratio                      135             f"Median moved-from-abr
...                                      ... oad share:     {sub['moved_from_abr
...                                      ... oad_share'].median():.4f} "
128         ratio = sub["us_inflow_shar  136             f"({sub['moved_from_abr
... e"] / sub["recent_fb_annual_share"]  ... oad_share'].median()*100:.2f}%)"
... .replace(0, np.nan)                  ... 
...                                      137         )
129         print(f"Median US-inflow /   138         print("Comparison note: the
... FB-inflow ratio: {ratio.median():.1  ... se are different measurement univer
... f}x")                                ... ses and should not be treated as a 
...                                      ... causal burden ratio.")
130                                      139 
131     print("\n=== Stylized fact 2: c  140     print("\n=== Stylized fact 2: c
... ounties with HIGHEST native inflow   ... ounties with HIGHEST Total Migratio
... ===")                                ... n-US inflow ===")
132     top_us = sub.nlargest(15, "us_i  141     top_us = sub.nlargest(15, "us_i
... nflow_share")[["NAME", "totpop", "u  ... nflow_share")[["NAME", "totpop", "u
... s_inflow_persons", "us_inflow_share  ... s_inflow_persons", "us_inflow_share
... ", "median_rent"]]                   ... ", "median_rent"]]
133     print(top_us.to_string(index=Fa  142     print(top_us.to_string(index=Fa
... lse))                                ... lse))
134                                      143 
135     if "recent_fb_annual_share" in   144     if "moved_from_abroad_share" in
... sub.columns:                         ...  sub.columns:
136         print("\n=== Stylized fact   145         print("\n=== Stylized fact 
... 3: counties with HIGHEST recent-FB   ... 3: counties with HIGHEST moved-from
... inflow share ===")                   ... -abroad share ===")
137         top_fb = sub.nlargest(15, "  146         top_fb = sub.nlargest(15, "
... recent_fb_annual_share")[["NAME", "  ... moved_from_abroad_share")[["NAME", 
... totpop", "recent_fb_annual_avg", "r  ... "totpop", "moved_from_abroad_past_y
... ecent_fb_annual_share", "median_ren  ... ear", "moved_from_abroad_share", "m
... t"]]                                 ... edian_rent"]]
138         print(top_fb.to_string(inde  147         print(top_fb.to_string(inde
... x=False))                            ... x=False))
139                                      148 
140     # Quintile comparison            149     # Quintile comparison
141     print("\n=== Stylized fact 4: r  150     print("\n=== Stylized fact 4: r
... ent and income by inflow type quint  ... ent and income by inflow type quint
... ile ===")                            ... ile ===")
142     sub["us_q"] = pd.qcut(sub["us_i  151     sub["us_q"] = pd.qcut(sub["us_i
... nflow_share"], 5, labels=["Q1 lowes  ... nflow_share"], 5, labels=["Q1 lowes
... t", "Q2", "Q3", "Q4", "Q5 highest"]  ... t", "Q2", "Q3", "Q4", "Q5 highest"]
... )                                    ... )
143     print("\nBy US-NATIVE inflow qu  152     print("\nBy Total Migration-US 
... intile:")                            ... inflow quintile:")
144     print(sub.groupby("us_q", obser  153     print(sub.groupby("us_q", obser
... ved=True).agg(                       ... ved=True).agg(
145         n=("NAME", "count"),         154         n=("NAME", "count"),
146         median_inflow_share=("us_in  155         median_inflow_share=("us_in
... flow_share", "median"),              ... flow_share", "median"),

sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py --- 5/5 --- Python
149         median_fb_share_overall=("f  158         median_fb_share_overall=("f
... b_share", "median"),                 ... b_share", "median"),
150     ).to_string())                   159     ).to_string())
151                                      160 
152     if "recent_fb_annual_share" in   161     if "moved_from_abroad_share" in
... sub.columns:                         ...  sub.columns:
153         sub2 = sub.dropna(subset=["  162         sub2 = sub.dropna(subset=["
... recent_fb_annual_share"]).copy()     ... moved_from_abroad_share"]).copy()
154         sub2["fb_q"] = pd.qcut(sub2  163         sub2["fb_q"] = pd.qcut(sub2
... ["recent_fb_annual_share"], 5, labe  ... ["moved_from_abroad_share"], 5, lab
... ls=["Q1 lowest", "Q2", "Q3", "Q4",   ... els=["Q1 lowest", "Q2", "Q3", "Q4",
... "Q5 highest"])                       ...  "Q5 highest"])
155         print("\nBy RECENT-FOREIGN-  164         print("\nBy MOVED-FROM-ABRO
... BORN inflow quintile:")              ... AD inflow quintile:")
156         print(sub2.groupby("fb_q",   165         print(sub2.groupby("fb_q", 
... observed=True).agg(                  ... observed=True).agg(
157             n=("NAME", "count"),     166             n=("NAME", "count"),
158             median_inflow_share=("r  167             median_inflow_share=("m
... ecent_fb_annual_share", "median"),   ... oved_from_abroad_share", "median"),
159             median_rent=("median_re  168             median_rent=("median_re
... nt", "median"),                      ... nt", "median"),
160             median_hh_income=("medi  169             median_hh_income=("medi
... an_hh_income", "median"),            ... an_hh_income", "median"),
161             median_us_inflow_share=  170             median_us_inflow_share=
... ("us_inflow_share", "median"),       ... ("us_inflow_share", "median"),
```

## Current File Excerpts

### sources/immigration-causal/scripts/build_county_outcome_panel.py

```text
"""Build county outcome panel by joining threshold spine to QCEW and IRS domestic migration.

Outputs:
- data/outcomes/county_qcew_2017_2024.parquet
- data/outcomes/county_outcome_panel.parquet
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent.parent / "data"
ANALYSIS = DATA / "analysis"
OUT = DATA / "outcomes"
OUT.mkdir(parents=True, exist_ok=True)

THRESHOLD_PANEL = DATA / "threshold" / "analysis" / "county_threshold_election_panel.parquet"
IRS_INFLOW = DATA / "internal_migration" / "county_inflow_2022_23.csv"
IRS_OUTFLOW = DATA / "internal_migration" / "county_outflow_2022_23.csv"
QCEW_DIR = DATA / "qcew"

QCEW_OUT = OUT / "county_qcew_2017_2024.parquet"
PANEL_OUT = OUT / "county_outcome_panel.parquet"
AUDIT_OUT = OUT / "county_outcome_panel_audit.json"

QCEW_WINDOWS = (
    {
        "base_year": 2017,
        "end_year": 2018,
        "label": "clean_pre_covid_early",
        "touches_2020": False,
        "window_role": "presurge_check",
        "contaminated": False,
        "reason": "Second clean annual pre-COVID window for pretrend checks.",
    },
    {
        "base_year": 2018,
        "end_year": 2019,
        "label": "clean_pre_covid",
        "touches_2020": False,
        "window_role": "presurge_check",
        "contaminated": False,
        "reason": "Clean annual pre-COVID window.",
    },
    {
        "base_year": 2018,
        "end_year": 2020,
        "label": "covid_overlap_long",
        "touches_2020": True,
        "window_role": "descriptive_only",
        "contaminated": True,
        "reason": "Touches 2020 annual average and mixes pre-COVID with pandemic-transition conditions.",
    },
    {
        "base_year": 2019,
        "end_year": 2020,
        "label": "covid_onset",
        "touches_2020": True,
        "window_role": "descriptive_only",
        "contaminated": True,
        "reason": "Touches 2020 annual average and should not be read as a clean pretrend or post period.",
    },
    {
        "base_year": 2020,
        "end_year": 2021,
        "label": "covid_rebound",
        "touches_2020": True,
        "window_role": "descriptive_only",
        "contaminated": True,
        "reason": "Starts in 2020 annual average and remains pandemic-transition contaminated.",
    },
    {
        "base_year": 2021,
        "end_year": 2022,
        "label": "surge_overlap_short",
        "touches_2020": False,
        "window_role": "descriptive_overlap",
        "contaminated": False,
        "reason": "Valid descriptive overlap window; not a clean presurge check.",
    },
    {
        "base_year": 2021,
        "end_year": 2023,
        "label": "surge_overlap_medium",
        "touches_2020": False,
        "window_role": "descriptive_overlap",
        "contaminated": False,
        "reason": "Valid descriptive overlap window; not a clean presurge check.",
    },
    {
        "base_year": 2023,
        "end_year": 2024,
        "label": "post_surge_clean",
        "touches_2020": False,
        "window_role": "post_period",
        "contaminated": False,
        "reason": "Clean post window that does not touch 2020.",
    },
    {
        "base_year": 2021,
        "end_year": 2024,
        "label": "surge_full_span",
        "touches_2020": False,
        "window_role": "main_post_period",
        "contaminated": False,
        "reason": "Main post-surge span; descriptive/summary window rather than presurge placebo.",
    },
)


def load_qcew_year(year: int) -> pd.DataFrame:
    path = QCEW_DIR / f"{year}_annual_singlefile.zip"
    usecols = [
        "area_fips",
        "own_code",
        "industry_code",
        "agglvl_code",
        "qtr",
        "disclosure_code",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
    ]
    parts: list[pd.DataFrame] = []
    for chunk in pd.read_csv(path, compression="zip", dtype=str, usecols=usecols

... [truncated for review packet] ...

       "annual_avg_emplvl_missing": int(panel[f"annual_avg_emplvl_{year}"].isna().sum()),
            "annual_avg_wkly_wage_missing": int(panel[f"annual_avg_wkly_wage_{year}"].isna().sum()),
            "total_annual_wages_missing": int(panel[f"total_annual_wages_{year}"].isna().sum()),
            "annual_avg_emplvl_nonpositive": int(panel[f"annual_avg_emplvl_{year}"].fillna(0).le(0).sum()),
        }

    def add_log_change(prefix: str, window_meta: dict[str, object]) -> None:
        base_year = int(window_meta["base_year"])
        end_year = int(window_meta["end_year"])
        base_col = f"annual_avg_{prefix}_{base_year}"
        end_col = f"annual_avg_{prefix}_{end_year}"
        out_col = f"qcew_{'employment' if prefix == 'emplvl' else 'wkly_wage'}_log_change_{base_year}_{end_year}"
        zero_base_flag = f"{out_col}_zero_base"
        missing_flag = f"{out_col}_missing_input"
        panel[zero_base_flag] = panel[base_col].fillna(0) <= 0
        panel[missing_flag] = panel[base_col].isna() | panel[end_col].isna()
        ratio = pd.Series(panel[end_col]).div(panel[base_col]).where(panel[base_col] > 0)
        ratio = ratio.map(lambda x: pd.NA if pd.isna(x) or x <= 0 else x)
        ratio = pd.to_numeric(ratio, errors="coerce")
        panel[out_col] = ratio.map(lambda x: None if pd.isna(x) else math.log(x))
        audit[f"{out_col}_zero_base_count"] = int(panel[zero_base_flag].sum())
        audit[f"{out_col}_missing_input_count"] = int(panel[missing_flag].sum())
        audit[f"{out_col}_nonmissing_count"] = int(panel[out_col].notna().sum())
        audit["qcew_window_metadata"][out_col] = {
            **window_meta,
            "metric": "employment" if prefix == "emplvl" else "weekly_wage",
            "missing_input_count": int(panel[missing_flag].sum()),
            "nonmissing_count": int(panel[out_col].notna().sum()),
            "zero_base_count": int(panel[zero_base_flag].sum()),
            "nondisclosure_missing_base_count": int(((panel[base_col].isna()) & (~panel[end_col].isna())).sum()),
            "nondisclosure_missing_end_count": int(((~panel[base_col].isna()) & (panel[end_col].isna())).sum()),
            "analysis_sample_missing_recent_fb_share_mean": (
                None if not panel[missing_flag].any() else float(panel.loc[panel[missing_flag], "recent_fb_annual_share"].mean())
            ),
            "analysis_sample_nonmissing_recent_fb_share_mean": (
                None if not (~panel[missing_flag]).any() else float(panel.loc[~panel[missing_flag], "recent_fb_annual_share"].mean())
            ),
            "analysis_sample_missing_permit_rate_mean": (
                None if not panel[missing_flag].any() else float(panel.loc[panel[missing_flag], "permit_rate_per_1k"].mean())
            ),
            "analysis_sample_nonmissing_permit_rate_mean": (
                None if not (~panel[missing_flag]).any() else float(panel.loc[~panel[missing_flag], "permit_rate_per_1k"].mean())
            ),
        }

    for window_meta in QCEW_WINDOWS:
        add_log_change("emplvl", window_meta)
        add_log_change("wkly_wage", window_meta)

    panel.to_parquet(PANEL_OUT, index=False)
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")
    return panel


def main() -> int:
    panel = build_panel()
    print(f"Wrote {QCEW_OUT}, {PANEL_OUT}, and {AUDIT_OUT}")
    print(f"County panel rows: {len(panel):,}")
    print(
        panel[
            [
                "fips5",
                "county_name",
                "state_name",
                "annual_avg_emplvl_2018",
                "annual_avg_emplvl_2024",
                "annual_avg_wkly_wage_2018",
                "annual_avg_wkly_wage_2024",
                "annual_avg_emplvl_2021",
                "annual_avg_wkly_wage_2021",
                "net_us_migration_share_2022_23",
            ]
        ].head(5).to_string(index=False)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### sources/immigration-causal/scripts/analyze_capacity_falsification.py

```text
"""Falsification and robustness checks for the county capacity-frontier results.

This pass separates:
- descriptive stress-object checks using contemporaneous load/capacity
- stricter falsification checks using a pre-surge permit baseline
- exploratory threshold search diagnostics
"""
from __future__ import annotations

import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

DATA = Path(__file__).parent.parent / "data"
PANEL = DATA / "outcomes" / "county_outcome_panel.parquet"
BPS_ZIP = DATA / "threshold" / "bps" / "BPS_Compiled_202601.zip"
OUT_DIR = DATA / "outcomes" / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_SUMMARY = OUT_DIR / "county_capacity_falsification_summary.json"
OUT_PERM = OUT_DIR / "county_capacity_permutation_results.csv"
OUT_PRETREND = OUT_DIR / "county_capacity_pretrend_results.csv"
OUT_OVERLAP = OUT_DIR / "county_capacity_overlap_results.csv"
OUT_GEO = OUT_DIR / "county_capacity_geographic_leaveout.csv"
OUT_THRESH = OUT_DIR / "county_capacity_threshold_search_holdout.csv"
OUT_THRESH_NULL = OUT_DIR / "county_capacity_threshold_search_null.csv"
OUT_THRESH_SURFACE = OUT_DIR / "county_capacity_threshold_surface.csv"
OUT_MONO = OUT_DIR / "county_capacity_monotonicity.csv"
OUT_SAMPLE = OUT_DIR / "county_capacity_sample_accounting.json"
PANEL_AUDIT = DATA / "outcomes" / "county_outcome_panel_audit.json"

RNG = np.random.default_rng(20260421)
PERMUTATIONS = 1000
THRESHOLD_SPLITS = 60
THRESHOLD_NULL_SPLITS = 60

STATE_TO_DIVISION = {
    "Connecticut": "New England",
    "Maine": "New England",
    "Massachusetts": "New England",
    "New Hampshire": "New England",
    "Rhode Island": "New England",
    "Vermont": "New England",
    "New Jersey": "Middle Atlantic",
    "New York": "Middle Atlantic",
    "Pennsylvania": "Middle Atlantic",
    "Illinois": "East North Central",
    "Indiana": "East North Central",
    "Michigan": "East North Central",
    "Ohio": "East North Central",
    "Wisconsin": "East North Central",
    "Iowa": "West North Central",
    "Kansas": "West North Central",
    "Minnesota": "West North Central",
    "Missouri": "West North Central",
    "Nebraska": "West North Central",
    "North Dakota": "West North Central",
    "South Dakota": "West North Central",
    "Delaware": "South Atlantic",
    "District of Columbia": "South Atlantic",
    "Florida": "South Atlantic",
    "Georgia": "South Atlantic",
    "Maryland": "South Atlantic",
    "North Carolina": "South Atlantic",
    "South Carolina": "South Atlantic",
    "Virginia": "South Atlantic",
    "West Virginia": "South Atlantic",
    "Alabama": "East South Central",
    "Kentucky": "East South Central",
    "Mississippi": "East South Central",
    "Tennessee": "East South Central",
    "Arkansas": "West South Central",
    "Louisiana": "West South Central",
    "Oklahoma": "West South Central",
    "Texas": "West South Central",
    "Arizona": "Mountain",
    "Colorado": "Mountain",
    "Idaho": "Mountain",
    "Montana": "Mountain",
    "Nevada": "Mountain",
    "New Mexico": "Mountain",
    "Utah": "Mountain",
    "Wyoming": "Mountain",
    "Alaska": "Pacific",
    "California": "Pacific",
    "Hawaii": "Pacific",
    "Oregon": "Pacific",
    "Washington": "Pacific",
}


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (math.nan, math.nan)
    phat = k / n
    denom = 1 + (z**2) / n
    center = (phat + (z**2) / (2 * n)) / denom
    half = z * math.sqrt((phat * (1 - phat) + (z**2) / (4 * n)) / n) / denom
    return (center - half, center + half)


def joint_mode_pair(df: pd.DataFrame, source: str) -> dict[str, float | int | None]:
    sub = df[df["source"] == source].copy()
    if sub.empty:
        return {
            "joint_mode_recent_quantile": None,
            "joint_mode_permit_quantile": None,
         

... [truncated for review packet] ...

train"].sum())
        n = int(len(thresh_null))
        lo, hi = wilson_interval(k, n)
        actual_wage = thresh[thresh["outcome"] == "wage"].copy()
        surface_actual = thresh_surface[thresh_surface["source"] == "actual"].copy()
        surface_null = thresh_surface[thresh_surface["source"] == "null_search"].copy()
        actual_joint_mode = joint_mode_pair(thresh_surface, "actual")
        null_joint_mode = joint_mode_pair(thresh_surface, "null_search")
        null_summary = {
            "search_target": "wage",
            "selection_rule": "maximize abs(HC3 t-stat) on train wage interaction",
            "evaluation_role": "within_outcome_holdout_under_permuted_recent_flow",
            "null_design": "within_state_permuted_recent_flow",
            "splits": n,
            "median_test_abs_t": float(thresh_null["test_abs_t"].median()),
            "share_test_sign_matches_wage_train": float(thresh_null["test_sign_matches_wage_train"].mean()),
            "share_test_sign_matches_wage_train_ci_low": lo,
            "share_test_sign_matches_wage_train_ci_high": hi,
            **null_joint_mode,
            "delta_vs_actual_wage_sign_match": float(actual_wage["test_sign_matches_wage_train"].mean() - thresh_null["test_sign_matches_wage_train"].mean()),
            "delta_vs_actual_wage_median_abs_t": float(actual_wage["test_t"].abs().median() - thresh_null["test_abs_t"].median()),
            "actual_joint_mode_share": float(surface_actual["selection_share"].max()),
            "null_joint_mode_share": float(surface_null["selection_share"].max()),
            "actual_top3_share": float(surface_actual["selection_share"].nlargest(3).sum()),
            "null_top3_share": float(surface_null["selection_share"].nlargest(3).sum()),
        }
        null_summary["actual_joint_mode_recent_quantile"] = actual_joint_mode["joint_mode_recent_quantile"]
        null_summary["actual_joint_mode_permit_quantile"] = actual_joint_mode["joint_mode_permit_quantile"]
        null_summary["actual_joint_mode_cell_share"] = actual_joint_mode["joint_mode_cell_share"]

    return {
        "sample_accounting": sample,
        "permutation": perm_records,
        "lead_exposure_and_post_with_presurge_controls": pretrend_records,
        "overlap_windows_current_load": overlap_records,
        "geographic_leaveout": geo_summary,
        "threshold_search_metadata": {
            "search_target": "wage",
            "selection_rule": "maximize abs(HC3 t-stat) on train wage interaction",
            "search_grid_recent_quantiles": [60, 65, 70, 75, 80, 85, 90],
            "search_grid_permit_quantiles": [25, 50],
            "evaluation_role": "holdout transfer to wage, margin, and employment",
            "null_design": "within-state permuted recent-flow",
            **joint_mode_pair(thresh_surface, "actual"),
        },
        "threshold_search_holdout": thresh_summary.to_dict(orient="records"),
        "threshold_search_null_wage_only": null_summary,
        "threshold_surface": thresh_surface.to_dict(orient="records"),
        "monotonicity": mono.to_dict(orient="records"),
    }


def main() -> int:
    df, sample = prepare()
    perm = permutation_check(df)
    pretrend = pretrend_check(df)
    overlap = overlap_check(df)
    geo = geographic_leaveout(df)
    thresh = threshold_search_holdout(df)
    thresh_null = threshold_search_null(df)
    thresh_surface = threshold_surface(thresh, thresh_null)
    mono = monotonicity(df)
    summary = build_summary(sample, perm, pretrend, overlap, geo, thresh, thresh_null, thresh_surface, mono)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(
        f"Wrote {OUT_SUMMARY}, {OUT_PERM}, {OUT_PRETREND}, {OUT_OVERLAP}, "
        f"{OUT_GEO}, {OUT_THRESH}, {OUT_THRESH_NULL}, {OUT_THRESH_SURFACE}, "
        f"{OUT_MONO}, and {OUT_SAMPLE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py

```text
"""Domestic migration vs moved-from-abroad flows as a bounded newcomer comparison.

Reframes: is the immigrant-specific frame or the newcomer-in-general frame closer
to the county-level newcomer counts we actually observe?

Approach:
1. Compute county-level IRS `Total Migration-US` inflow aggregate (`97/000`)
2. Compute county-level ACS `Moved from abroad in the past year` (B07001_081E)
3. Compare the two as descriptive newcomer-flow layers, not as a like-for-like
   causal head-to-head

Output: data/analysis/county_newcomer_comparison.parquet
"""
from __future__ import annotations
from pathlib import Path
import requests
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
SOI = DATA / "internal_migration" / "county_inflow_2022_23.csv"
OUT = DATA / "analysis"


def load_soi_county_inflow() -> pd.DataFrame:
    """Aggregate IRS SOI county inflow to the `Total Migration-US` county row (code 97)."""
    df = pd.read_csv(SOI, encoding="latin-1", dtype={
        "y2_statefips": str, "y2_countyfips": str,
        "y1_statefips": str, "y1_countyfips": str,
    })
    # y1 codes 96/97/98/95 are aggregate rows — keep "97" = Total Migration-US.
    agg = df[(df["y1_statefips"] == "97") & (df["y1_countyfips"] == "000")].copy()
    agg["dest_state_fips"] = agg["y2_statefips"].str.zfill(2)
    agg["dest_county_fips"] = agg["y2_countyfips"].str.zfill(3)
    agg["dest_fips5"] = agg["dest_state_fips"] + agg["dest_county_fips"]
    agg = agg.rename(columns={"n1": "us_inflow_returns", "n2": "us_inflow_persons", "agi": "us_inflow_agi_kusd"})
    return agg[["dest_fips5", "dest_state_fips", "dest_county_fips", "us_inflow_returns", "us_inflow_persons", "us_inflow_agi_kusd"]]


def fetch_acs_county_population_and_recent_fb() -> pd.DataFrame:
    """Pull ACS 2022 5-yr county-level: total pop + foreign-born + recent-arrival FB.

    Variables:
    - B01003_001E: total population
    - B05002_013E: foreign-born population
    - B05005_002E + B05005_004E (combined ENT 2010-later approx): recent FB
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        "get": "NAME,B01003_001E,B05002_013E,B05002_001E,B25064_001E,B19013_001E",
        "for": "county:*",
    }
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns={
        "B01003_001E": "totpop",
        "B05002_013E": "fb_pop",
        "B05002_001E": "totpop_b05002",
        "B25064_001E": "median_rent",
        "B19013_001E": "median_hh_income",
    })
    for c in ("totpop", "fb_pop", "totpop_b05002", "median_rent", "median_hh_income"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    df["county_fips"] = df["county"].astype(str).str.zfill(3)
    df["fips5"] = df["state_fips"] + df["county_fips"]
    df["fb_share"] = df["fb_pop"] / df["totpop"]
    return df[["fips5", "state_fips", "county_fips", "NAME", "totpop", "fb_pop", "fb_share", "median_rent", "median_hh_income"]]


def fetch_acs_moved_from_abroad() -> pd.DataFrame:
    """Past-year moved-from-abroad count by county from ACS B07001_081E.

    This is not an immigrant-only measure. It can include U.S.-born returnees
    and other international movers captured by ACS mobility reporting.
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        "get": "B07001_081E",
        "for": "county:*",
    }
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["moved_from_abroad_past_year"] = pd.to_numeric(df["B07001_081E"], errors="coerce")
    df["state_fips"] = df["state"].astype(str).str.zfill(2)
    df["county_fips"] = df["county"].astype(str).str.zfill(3)
    df["fips5"] = df["state_fips"] + df["county_fips"]
    return df[["fips5", "moved_from_abroad_past_

... [truncated for review packet] ...

nty destinations with US-inflow data")

    print("Loading ACS county totals...")
    acs = fetch_acs_county_population_and_recent_fb()
    print(f"  {len(acs)} ACS counties")

    print("Loading ACS moved-from-abroad past year (B07001_081E)...")
    try:
        rfb = fetch_acs_moved_from_abroad()
        print(f"  {len(rfb)} county moved-from-abroad rows")
        acs = acs.merge(rfb, on="fips5", how="left")
    except Exception as e:
        print(f"  moved-from-abroad fetch failed: {e}")

    merged = acs.merge(soi, left_on="fips5", right_on="dest_fips5", how="left")
    merged["us_inflow_persons"] = merged["us_inflow_persons"].fillna(0)
    merged["us_inflow_share"] = merged["us_inflow_persons"] / merged["totpop"]
    if "moved_from_abroad_past_year" in merged.columns:
        merged["moved_from_abroad_share"] = merged["moved_from_abroad_past_year"] / merged["totpop"]
    merged["comparison_warning"] = (
        "IRS Total Migration-US tax-filer inflow (2022-23) and ACS moved-from-abroad "
        "2022 5-year estimates are not like-for-like universes or time windows; use descriptively."
    )
    merged.to_parquet(OUT / "county_newcomer_comparison.parquet", index=False)
    print(f"\nWrote {OUT/'county_newcomer_comparison.parquet'}: {len(merged)} counties")

    # Stylized facts
    print("\n=== Stylized fact 1: Total Migration-US vs moved-from-abroad newcomer shares ===")
    sub = merged.dropna(subset=["us_inflow_persons", "totpop"])
    sub = sub[sub["totpop"] >= 10000]  # filter tiny counties
    print(f"Counties (≥10k pop): {len(sub)}")
    print(
        f"Median Total Migration-US inflow share: {sub['us_inflow_share'].median():.4f} "
        f"({sub['us_inflow_share'].median()*100:.2f}%)"
    )
    if "moved_from_abroad_share" in sub.columns:
        print(
            f"Median moved-from-abroad share:     {sub['moved_from_abroad_share'].median():.4f} "
            f"({sub['moved_from_abroad_share'].median()*100:.2f}%)"
        )
        print("Comparison note: these are different measurement universes and should not be treated as a causal burden ratio.")

    print("\n=== Stylized fact 2: counties with HIGHEST Total Migration-US inflow ===")
    top_us = sub.nlargest(15, "us_inflow_share")[["NAME", "totpop", "us_inflow_persons", "us_inflow_share", "median_rent"]]
    print(top_us.to_string(index=False))

    if "moved_from_abroad_share" in sub.columns:
        print("\n=== Stylized fact 3: counties with HIGHEST moved-from-abroad share ===")
        top_fb = sub.nlargest(15, "moved_from_abroad_share")[["NAME", "totpop", "moved_from_abroad_past_year", "moved_from_abroad_share", "median_rent"]]
        print(top_fb.to_string(index=False))

    # Quintile comparison
    print("\n=== Stylized fact 4: rent and income by inflow type quintile ===")
    sub["us_q"] = pd.qcut(sub["us_inflow_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
    print("\nBy Total Migration-US inflow quintile:")
    print(sub.groupby("us_q", observed=True).agg(
        n=("NAME", "count"),
        median_inflow_share=("us_inflow_share", "median"),
        median_rent=("median_rent", "median"),
        median_hh_income=("median_hh_income", "median"),
        median_fb_share_overall=("fb_share", "median"),
    ).to_string())

    if "moved_from_abroad_share" in sub.columns:
        sub2 = sub.dropna(subset=["moved_from_abroad_share"]).copy()
        sub2["fb_q"] = pd.qcut(sub2["moved_from_abroad_share"], 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
        print("\nBy MOVED-FROM-ABROAD inflow quintile:")
        print(sub2.groupby("fb_q", observed=True).agg(
            n=("NAME", "count"),
            median_inflow_share=("moved_from_abroad_share", "median"),
            median_rent=("median_rent", "median"),
            median_hh_income=("median_hh_income", "median"),
            median_us_inflow_share=("us_inflow_share", "median"),
        ).to_string())


if __name__ == "__main__":
    main()
```

### sources/immigration-causal/README.md

```text
# immigration-causal — reproducible analysis bundle

This directory contains the data acquisition + analysis pipeline behind the
April 2026 "immigration causal" research cycle in
`research/immigration-causal-*`. Everything here is meant to be reproduced from
scratch by an outside reader.

## What this cycle does

Five mini-investigations sharing the same panel infrastructure:

1. **Card vs Borjas (E-Verify wages).** TWFE on QWI state × industry × education
   panel, 2003-2023. Test whether tighter unauthorized labor supply (E-Verify
   mandates) raises native low-skill wages (Borjas) or has null/negative effect
   (Card). Companion regression on employment quantities to separate the two
   margins. Scripts: `analyze_everify_wages.py`, `analyze_everify_employment.py`.

2. **Saiz × rent.** Merge Saiz (2010, QJE) MSA housing-supply elasticities with
   ACS 2022 median rent and foreign-born share. Tests whether immigrant rent
   burden concentrates in inelastic MSAs. Decomposes elasticity into
   topography (`unaval`) vs regulation (`WRLURI`) channels to determine
   whether zoning reform is a viable lever. Scripts:
   `merge_saiz_rent_immigrant.py`, `saiz_decomposition.py`.

3. **Sanctuary DiD.** Two-sided design — pro-sanctuary states (CA, IL, OR…) vs
   anti-sanctuary states (TX SB 4, FL SB 168, AL HB 56, AZ SB 1070…) on QWI
   wages. Cross-checks the E-Verify wage finding via a different policy axis.
   Script: `analyze_sanctuary_wages.py`. Sanctuary panel hand-compiled from
   primary legal sources (state codes, executive orders) — see MANIFEST.

4. **Mass-deportation calibration.** Partial-equilibrium industry-by-industry
   shock from 100% removal of unauthorized workers. Uses BEA Use Tables (labor
   share, output) × Pew/CMS unauthorized employment shares × literature labor
   demand elasticities (-0.3 to -0.5). Order-of-magnitude bounds, not a
   forecast. Script: `mass_deportation_sim.py`.

5. **Open-borders sensitivity.** Clemens (2011) Place Premium parameters into a
   scenario table: world stocks, rich-quartile absorption capacity, transition
   horizons. The script does the arithmetic; the binding-constraint reasoning
   lives in the memo. Script: `open_borders_baseline.py`.

6. **(Cross-cut) Internal vs immigrant newcomers.** IRS SOI county inflow
   (`Total Migration-US`, not native-only filers) joined to ACS B07001_081E
   (`Moved from abroad` in the past year, not an immigrant-only series) so the
   reader can ask "is the policy-relevant unit the immigrant or the newcomer
   in general?" Treat this layer descriptively: the admin and survey measures
   do not share the same universe or time window. Script:
   `analyze_internal_vs_immigrant_newcomers.py`.

Findings memos summarising results live under
`../../research/immigration-causal-*.md`. The verdicts there cite the analysis
parquets/CSVs that this pipeline produces in `data/analysis/`.

## Quickstart

```bash
# 1. clone the parent research repo, then:
cd sources/immigration-causal

# 2. acquire all external datasets (~50 MB total)
bash setup.sh

# 3. run the analysis pipeline end-to-end
bash run_all.sh
```

Outputs land in `data/analysis/` (parquet, CSV, JSON, plain-text logs).

## Requirements

- **Python 3.11+**
- **uv** (https://github.com/astral-sh/uv) — every script is invoked via
  `uv run --with <deps> python3 …` so dependencies are resolved per script;
  no `pip install` step needed.
- **Disk:** ~50 MB raw data, ~5 MB analysis outputs.
- **Network:** scripts hit
  - `api.census.gov` (ACS 1-yr, 5-yr; QWI timeseries) — no API key required
    for the volumes used here (well below the 500 calls/day anonymous limit)
  - `apps.bea.gov` (BEA Supply-Use tables, public)
  - `irs.gov` (SOI county inflow/outflow CSVs, public)
  - `web.mit.edu` (Saiz 2010 MSA elasticity .dta, hosted on Albert Saiz's
    MIT Urban Economics Lab page)

  No authenticated APIs. Run from a network that doesn't block these hosts.

## Data acquisition order

`setup.sh` fetches in this order; each step is independent:

1. Saiz 2010 MSA elasticity (.dta) → `data/saiz/`
2. BEA Supply-Use Summary 1997-2023 (.xlsx, in AllTablesSUP.zip) → `data/bea_io/`
3. IRS SOI county inflow + outflow 2022-23 (.csv) → `data/internal_migration/`
4. Clemens (2011, JEP) Place Premium PDF → `data/clemens/`  *(reference only)*
5. WRLURI 2018 → **SKIPPED**: the canonical Wharton link
   (`real-estate.wharton.upenn.edu/wp-content/uploads/2024/.../WRLURI-2018.zip`)
   has been intermittently dead since early 2025. The Saiz 2010 .dta already
   ships with `WRLURI` and `unaval` columns from the original 2008 build, which
   is what `saiz_decomposition.py` actually uses. The 2018 refresh is desirable
   for sensitivity but not required.

The QWI state panel and ACS state-level immigrant share are fetched live by the
analysis scripts themselves (`pull_qwi_state_panel.py`,
`pull_acs_state_immigrant_share.py`) on first run. They cache as parquet under
`data/lehd/`. The QWI pull takes ~5-10 minutes (36 batched API calls).

The hand-compiled `everify_state_mandates.csv` and `sanctuary_state_panel.csv`
ship with the repo (small, source-cited in MANIFEST.md). They are not
re-acquired by `setup.sh`.

## Layout

```
scripts/                     analysis + acquisition Python
data/                        gitignored; populated by setup.sh + run_all.sh
  saiz/                      Saiz 2010 MSA elasticity (.dta)
  bea_io/                    BEA Use/Supply tables (.xlsx)
  lehd/                      QWI state panel + ACS state immigrant share
  everify/                   hand-compiled E-Verify mandate panel (in repo)
  sanctuary/                 hand-compiled sanctuary state panel (in repo)
  internal_migration/        IRS SOI county inflow/outflow
  clemens/                   Clemens 2011 PDF + open-borders calibration JSON
  daca/                      DACA timeline notes (in repo)
  wrluri/                    intentionally empty — see MANIFEST gotcha
  foged_peri/                placeholder for future Foged-Peri replication
  analysis/                  outputs from run_all.sh
MANIFEST.md                  per-dataset provenance + checksums
setup.sh                     re-acquire all external data
run_all.sh                   run analysis pipeline in dependency order
```

## Reproducibility caveats

- ACS API 2020 1-yr was withdrawn (COVID). The puller skips that year.
- QWI release cadence: cells are refreshed quarterly; numbers will shift
  slightly across vintages. This snapshot is dated 2026-04-18.
- Census API will return HTTP 200 with empty JSON if you exceed the daily
  anonymous quota — re-run the puller with an API key
  (`CENSUS_API_KEY` env var, free) if you hit this.
- All hand-compiled panels (E-Verify, sanctuary) document their primary
  sources in MANIFEST.md. They are append-only; corrections add a row, not
  edit one.

## Licence / attribution

Code: same licence as parent repo. Data: each dataset retains its source
licence (see MANIFEST.md). Memos in `research/` are author-owned analysis;
attribute as "Strasser, immigration-causal cycle 2026-04-18" if cited.

<!-- knowledge-index
generated: 2026-04-19T04:19:20Z
hash: 3ad1a955a1ff

cross_refs: research/immigration-causal-*.md

end-knowledge-index -->
```

### research/immigration-capacity-falsification-2026-04-21.md

```text
# Immigration capacity falsification pass — 2026-04-21

**Question:** After correcting the earlier placebo bug, what survives real falsification pressure in the county `flow/capacity` result, and what has to be narrowed?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior frontier memo argued that `recent immigrant flow relative to local build capacity` was the cleaner county stress object for wages, employment, and local sorting pressure than stock share alone. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]  
**Instrument note:** This is a politically charged topic; treat the synthesis as a repo artifact to be checked against raw outputs, not as neutral narration from a bias-free instrument. [SOURCE: notes/llm-bias-caveat.md]

## Bottom line

1. The county `load/capacity` signal is still **structurally real on the descriptive side**. It beats `1,000` within-state permutations at the floor `p<=0.001`, survives leave-one-division-out, and remains strongly monotone across load deciles. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. The old `2021–2022` placebo section was mislabeled because it used overlapping treatment windows. After rebuilding the panel, moving the permit baseline back to `2017–2019`, and extending QCEW to add a second clean pre-COVID window (`2017–2018`), the annual presurge evidence still does **not** yield a clean causal reading. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
3. The annual-data causal split is now **provisional, not settled**:
   - `wage story`: not clean either, because the two clean presurge windows move in opposite directions (`2017–2018` positive, `2018–2019` weak negative), which looks more like unstable lead-exposure association than a stable causal pretrend test [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
   - `employment story`: remains more suspicious, because both clean presurge windows are already negative [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
   - any stronger wage-versus-employment split that leans on `2019–2020` or `2020–2021` is still contaminated by COVID-era annual averaging and should be treated as unverified pending quarterly or better pre-2020 reruns [INFERENCE]
4. The threshold result no longer supports a generic “real family across outcomes” claim. It now supports a **wage-tuned exploratory threshold search that beats the null on performance but not on stable location**. Wage holdout sign stability beats the null strongly, while the selected cutoff surface is diffuse, transfer to `margin` is poor, and transfer to `employment` is only moderate. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv]
5. The right updated claim is:
   - `flow/capacity` is a robust county stress marker [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
   - it is a strong descriptive stress marker, but the annual county panel still does not cleanly identify the wage channel as causal [INFERENCE]
   - county employment effects remain harder to separate f

... [truncated for review packet] ...

ication_summary.json]

## What now fails

1. `We found a clean generic post-surge causal threshold from the county panel alone.`  
This is too strong. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]

2. `The annual-data wage-versus-employment causal split is already settled.`  
Too strong. Even after moving the permit baseline back to `2017–2019` and adding a second clean pre-COVID window, the wage-side presurge association flips sign while employment stays negative, so the annual county panel still does not cleanly identify the split. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json]

3. `The threshold story generalizes equally well to wages, employment, and politics.`  
False in the corrected pass. Margin transfer is poor. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]

## Best current formulation

The strongest defensible version is:

1. `flow/capacity is a robust and highly structured county stress marker` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. `it is a strong descriptive stress marker consistent with local strain amplification, but not itself clean causal proof` [INFERENCE]
3. `the annual county panel still does not cleanly identify the wage channel, because the clean presurge wage windows are unstable while employment remains suspicious` [INFERENCE]
4. `receiver-city shelter and service counterfactuals are still the best next causal design` [INFERENCE]
5. `policy relevance remains high` [FRAMING-SENSITIVE] [INFERENCE] because the county stress marker is strong even where the causal partition is incomplete

## Repo stance update

The repo's current best position should now be:

1. `descriptive confidence`: high [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. `causal confidence on a clean wage-versus-employment split from the annual county panel`: low [INFERENCE]
3. `causal confidence on the broader stress-marker result`: moderate [INFERENCE]
4. `policy relevance`: still high [FRAMING-SENSITIVE] [INFERENCE], but only if phrased as a stress-marker claim rather than a clean threshold-identification claim

## Revisions

### 2026-04-22

The first draft of this memo treated `2021–2022` overlap windows as placebo/pretrend evidence. After `/critique close` flagged that as a real semantics bug, the county panel was rebuilt with earlier QCEW windows, the falsification script was rewritten around a true presurge permit baseline, and the threshold section was downgraded again once the exported threshold surface showed diffuse cutoff selection. The next close review still objected that one clean pre-COVID window was not enough, so the county panel was extended to `2017` and the annual controls were rerun. That extension weakened the stronger wage-side causal reading further: the clean presurge wage windows are unstable, while employment stays negative in both clean windows. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/verified-disposition.md]
```

### research/immigration-reasoning-evolution-2026-04-21.md

```text
# Immigration reasoning evolution — 2026-04-21

**Purpose:** Record how the repo's immigration reasoning changed across this cycle, including where later falsification forced a real correction.  
**Status note:** This is a narrative reconstruction from dated memos, local review artifacts, and the current git history. It is not a formally versioned decision log. Treat chronology claims as `[INFERENCE]` unless a dated artifact or commit is named explicitly.  
**Instrument note:** Politically charged topic; keep the raw artifacts in view and do not treat this file as a neutral substitute for them. [SOURCE: notes/llm-bias-caveat.md]

## Artifact basis

1. [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md)
2. [immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md](/Users/alien/Projects/research/research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md)
3. [immigration-threshold-first-panel-2026-04-21.md](/Users/alien/Projects/research/research/immigration-threshold-first-panel-2026-04-21.md)
4. [immigration-threshold-causal-levers-2026-04-21.md](/Users/alien/Projects/research/research/immigration-threshold-causal-levers-2026-04-21.md)
5. [immigration-county-outcome-panel-2026-04-21.md](/Users/alien/Projects/research/research/immigration-county-outcome-panel-2026-04-21.md)
6. [immigration-capacity-frontier-2026-04-21.md](/Users/alien/Projects/research/research/immigration-capacity-frontier-2026-04-21.md)
7. [.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md](/Users/alien/Projects/research/.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md)
8. [immigration-capacity-falsification-2026-04-21.md](/Users/alien/Projects/research/research/immigration-capacity-falsification-2026-04-21.md)
9. [.model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md](/Users/alien/Projects/research/.model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md)
10. commit `2cdd801` (`[analysis] Measure capacity frontier — compare stock flow and load`) [SOURCE: git history]
11. commit `1097c77` (`[research] Audit Bryan Caplan claims — score open-borders arguments`) [SOURCE: git history]

## Starting point: stop answering the scalar question

The initial attractors were all too coarse:

1. `open borders create huge gains`
2. `immigration hurts locals`
3. `economists disagree`

The real improvement started when the repo stopped answering the scalar question and split the ledgers:

1. `global`
2. `national aggregate`
3. `destination per capita`
4. `native local` [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md]

That was the first durable move from rhetoric toward incidence. [INFERENCE]

## Phase 1: open-borders rhetoric gets bounded

Reading the actual open-borders papers moved the repo from:

1. `freer migration might double world GDP`

to:

1. `large global gains remain plausible`
2. `literal doubling is not a realistic central forecast`
3. `the optimistic result depends on rich-country capacity staying largely intact` [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]

This was the first place where destination capacity became a first-order part of the reasoning rather than an afterthought. [INFERENCE]

## Phase 2: surge regime breaks the old evidence hierarchy

The repo then stopped treating pre-2020 Card/Borjas-style marginal labor shocks as the whole game. The `2021–2024` surge pushed the evidence search toward:

1. shelter saturation
2. state/local budgets
3. housing absorption
4. backlash under concentrated arrivals [SOURCE: research/immigration-causal-surge-2021-2024.md]

That reframed the proje

... [truncated for review packet] ...

k negative, so the annual wage channel is not cleanly identified from this panel [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
3. both clean annual pre-COVID employment windows are already negative, which keeps employment more suspicious than wages in the annual design [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
4. post-`2023–2024` wage and employment effects still survive annual controls, but the clean annual windows do not justify treating either channel as settled causal identification [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
5. the IRS `97/000` layer is total domestic migration, not a native-incumbent-only series, so the corrected falsification pass quarantines that channel from the main claim set [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv]

This is the current best correction:

1. `descriptive stress-marker claim`: survives strongly
2. `wage-side surge amplification`: still plausible, but not cleanly identified from the annual county panel
3. `employment-side surge amplification`: more suspicious because the clean presurge employment windows are already negative
4. `wage-versus-employment causal split from the annual panel`: not settled
5. `generic county threshold story across all outcomes`: too strong

## Phase 9: the threshold claim gets demoted, not killed

The corrected threshold search no longer supports a sweeping “real threshold family” line. It now supports:

1. wage-search performance that beats a null search
2. a **diffuse** cutoff surface rather than one stable breakpoint
3. poor transfer to margin
4. only moderate transfer to employment [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]

So the repo did **not** end at:

1. `thresholds are fake`

It ended at:

1. `threshold-search evidence exists for wages, but stable cutoff location does not`

## What the repo now actually believes

The current best position is:

1. `global-gains arguments survive only at bounded margins and with capacity caveats`
2. `destination-country incidence is mostly a capacity problem, not a stock-share problem`
3. `county flow/capacity is a strong stress marker`
4. `the annual county panel does not cleanly identify the wage channel, and employment remains more obviously confounded by presurge weakness`
5. `receiver-city synthetic controls remain the best next causal design`
6. `IRS domestic migration can still be useful descriptively, but not as a native-sorting claim without additional identification`

## Why this file exists

Without this trace, later work can easily flatten two different things into one:

1. `we changed our mind because new data arrived`
2. `we changed our mind because a critique found a real bug in our reasoning`

Both happened here. The second one matters more. [INFERENCE]

## Revisions

### 2026-04-22

The first draft of this file narrated the earlier falsification pass as if its “pretrend” downgrade were already sound. After the corrected county panel and first review artifacts landed, the file was rewritten to distinguish the bug-triggered correction from the evidence that still survives after that correction. A later review forced one more downgrade: the annual design needed a second clean pre-COVID window and an explicit `2017–2019` permit baseline. Once that extension landed, the annual wage windows no longer supported a clean causal reading either, while employment stayed negative in both clean presurge windows. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/verified-disposition.md] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
```

### research/immigration-county-outcome-panel-2026-04-21.md

```text
# Immigration county outcome panel: labor, domestic migration, and backlash

Supersession note: this memo is an earlier county-outcome pass. For the current stance, read [immigration-capacity-falsification-2026-04-21.md](/Users/alien/Projects/research/research/immigration-capacity-falsification-2026-04-21.md), which extends QCEW back to `2017`, adds explicit window metadata, and downgrades the causal confidence of the wage/employment story.

**Question:** After joining official county QCEW annual outcomes to the threshold panel, what actually moves in high-immigration, low-capacity counties: employment, wages, IRS domestic migration, politics, or some narrower combination?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior threshold pass showed that capacity variables mattered more than immigrant-stock variables, but it still did not directly price county labor outcomes. This memo adds county labor outcomes and an IRS domestic net-migration layer to the same county spine. That IRS layer is `Total Migration-US`, not a native-incumbent-only measure. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv]

## Bottom line

1. **The first county-outcome pass looked more like a wage-growth story than an employment-collapse story.** In counties with very high recent immigration and low permit throughput, countywide weekly wage growth from `2021` to `2024` is about `1.5 pp` lower, while employment growth is not significantly lower in this first reduced-form pass. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. **Backlash and labor do not load on exactly the same moderator in this first pass.** In the top recent-immigration counties, both `low permit` and `high rent burden` predict more GOP shift, but the wage-growth penalty attaches to `low permit`, while IRS domestic net out-migration attaches more to `high rent burden`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. **That is a better causal decomposition than “immigration hurts the local economy.”** The data now point to:
   - `permit throughput / housing-supply response` as the wage and backlash moderator
   - `rent burden / affordability` as the domestic-migration / sorting moderator
   - `shelter and legal regime` as the receiver-city crisis amplifier
   - no strong evidence here of a broad county employment collapse [INFERENCE]

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | High recent-immigration counties with low permit throughput show slower county wage growth | HC3 OLS: `high_recent_fb × low_permit ≈ -1.49 pp` on `2021–2024` QCEW weekly wage log growth, `t≈-3.15`, `p≈0.0017`; result survives with rent burden added | HIGH | [county_outcome_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json), [county_outcome_lever_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv) | VERIFIED |
| 2 | The same interaction does not produce a clear county employment-growth penalty | HC3 OLS: `high_recent_fb × low_permit ≈ -0.33 pp`, `t≈-0.67`, `p≈0.50` on QCEW employment log growth | HIGH | [county_outcome_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json) | VERIFIED |
| 3 | In top recent-immigration counties, wage and employment medians improve as permit capacity rises | Q5 surge counties: median employment growth `2.72 -> 5.04 -> 6.15 -> 8.55 pp`; median weekly wage growth `11.00 -> 10.75 -> 11.45 -> 13.13 pp` across permit quartiles | HIGH | [county_outcome_bins.csv](/Users/alien/Project

... [truncated for review packet] ...

l/data/outcomes/analysis/county_outcome_lever_comparison.csv]

So IRS-measured domestic migration appears to respond more to direct affordability pressure than to permit scarcity alone. That is suggestive for sorting, but it is not a native-incumbent-only result. [INFERENCE]
This is why `rent burden` still matters, even though it is not the best wage moderator.

### 5) Politics responds to both scarcity and affordability

In this broader outcome-panel sample, the backlash result is more mixed than in the earlier threshold-only memo:

1. `high_recent_fb × low_permit ≈ +0.75 pp`, `p≈0.064` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. `high_recent_fb × high_rent_burden ≈ +0.75 pp`, `p≈0.038` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]

That is a plausible refinement rather than a contradiction.

The earlier pass asked which moderator best explained backlash on a narrower threshold frame and found permit throughput cleaner. This pass says that once you look at the high-immigration tail alongside labor and mobility outcomes, politics responds to both:

1. inability to add supply
2. direct cost pressure felt by residents [INFERENCE]

## What changed from the prior position?

Before this pass, the repo could say:

1. capacity thresholds are real
2. shelter saturation is real
3. backlash is worse in constrained places
4. labor conclusions at the county threshold level were still mostly missing

Now it can also say:

1. the first broad county labor response is slower wage growth, not strong job loss [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]
2. permit throughput is the wage-side moderator in this first pass [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. rent burden is the cleaner IRS domestic-migration moderator [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
4. politics sits on top of both channels [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv] [INFERENCE]

## Best current causal formulation

The best public-data formulation is now:

1. **`low permit throughput` is the main county wage-growth bottleneck under high recent immigration in this first pass.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. **`high rent burden` is the stronger IRS domestic-migration signal.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. **`political backlash` responds to both scarcity and affordability.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
4. **`employment collapse` is not the clean county-level story in this panel.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]
5. **receiver-city crisis severity still depends on shelter stock and institutional regime, which the county panel cannot replace.** [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]

## What remains uncertain

1. QCEW is county-total employment and wages, not native-only outcomes. It is a strong local labor barometer, not a native-incidence estimator. [INFERENCE]
2. QCEW weekly wages are nominal. In low-permit counties with faster shelter-cost pressure, the nominal wage penalty likely understates any real wage penalty. [INFERENCE]
3. IRS SOI migration is filer-based, not a full resident microflow. [INFERENCE]
4. This is still reduced-form county evidence, not a structural model with endogenous housing supply, relocation, and sector composition. [INFERENCE]
5. The shelter/legal-regime story still needs the receiver-node panel and ideally `HMIS/LSA` for a fuller local-capacity account. [SOURCE: research/immigration-surge-threshold-dataset-frontier-2026-04-21.md]
```

### research/immigration-INDEX.md

```text
# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.

## Core State

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-main-question-reset.md` | What the repo is actually trying to answer | Reframing the project or proposing new scope |
| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
| `immigration-verified-findings-report-2026-04-10.md` | Current verified findings snapshot | Answering "what do we know?" |
| `immigration-confidence-ladder.md` | Claim confidence by tier | Making strong claims or publishing conclusions |
| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
| `immigration-epistemic-check.md` | Framing-sensitive guardrails | Politically charged synthesis |
| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
| `immigration-dataset-register.md` | Use-case-oriented data register | Asking "what data do we have?" |
| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |

## Fiscal Ledger

| File | Topic | Consult before |
|------|-------|----------------|
| `fiscal-impact-unauthorized-immigration-research-memo.md` | Main fiscal memo: federal/state-local split, wage debate, child-attribution dispute | Any fiscal bottom line |
| `full-spectrum-costs-unauthorized-immigration-research-memo.md` | Non-ledger costs: congestion, courts, labor-law erosion, backlash | Claiming "hidden" costs beyond taxes/transfers |
| `immigration-unified-scenarios-memo.md` | Scenario comparison across methods | Converting arguments into a bounded range |
| `immigration-costs-causal-analysis.md` | DAG and causal-path discipline | Proposing controls, mediators, or attribution rules |
| `state-local-cost-examples-ny-ca-tx.md` | Concrete state/local examples | Generalizing from national ledgers to local burden |
| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |
| `immigration-adversarial-review.md` | Strongest case against our own position | Closing out a conclusion or writing a public-facing memo |

## Data Stack

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
| `immigration-public-data-acquisition-2026-04-11.md` | What public files were actually staged locally | Assuming a dataset has been acquired |
| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
| `immigration-next-data-upgrades.md` | Highest-value missing acquisitions | Planning the next data tranche |
| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
| `immigration-school-service-complexity-2026-04-11.md` | Built district/state school-side context layer from `SAIPE` + school finance + current NCES directory, plus bounded `ELSi` probe | Doing district school-burden or school-service-complexity analysis |
| `immigration-surge-threshold-dataset-frontier-2026-04-

... [truncated for review packet] ...

tion-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS moved-from-abroad flow comparison for “newcomer burden” | Treating "newcomer burden" as immigration-driven by default |
| `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
| `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS domestic migration + threshold spine: county wages, employment, domestic migration, and backlash in one frame | Reusing the county outcome panel while remembering the IRS layer is not native-incumbent-only |
| `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
| `immigration-capacity-falsification-2026-04-21.md` | Corrected falsification pass with clean `2017–2018` and `2018–2019` annual pre-COVID windows, `1,000`-draw permutation inference, division/state leave-out, explicit window metadata, and wage-threshold null benchmarking | Asking which parts of the new flow-capacity story still survive after fixing the earlier placebo bug |
| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction and later downgrade that left the annual wage/employment split unresolved | Wanting the evolution of reasoning itself traced rather than only the latest stance |

## Raw Data & Warehouse

| File | Topic | Consult before |
|------|-------|----------------|
| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
| `../sources/immigration-fiscal/data/derived/immigration_context.duckdb` | Main derived DuckDB warehouse | Querying state/origin/context data |
| `../sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql` | Warehouse build script | Rebuilding or extending the DuckDB |
| `../sources/immigration-fiscal/data/derived/stage3_proto/` | Prototype local-context build outputs | Using tract/PUMA prototype artifacts |

## Quick Start

If the question is:

1. `What do we currently think?` Start with `immigration-verified-findings-report-2026-04-10.md`, then `immigration-confidence-ladder.md`.
2. `Is low-skill immigration good or bad for natives?` Start with `immigration-economist-effects-matrix.md`, then `fiscal-impact-unauthorized-immigration-research-memo.md`, then `full-spectrum-costs-unauthorized-immigration-research-memo.md`.
3. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
4. `Can we model this ourselves?` Start with `immigration-lifetime-fiscal-data-stack-2026-04-10.md`, then `immigration-public-data-acquisition-2026-04-11.md`, then `immigration-frontier-data-acquisition-2026-04-11.md`, then the DuckDB build files.
5. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md`.

<!-- knowledge-index
generated: 2026-04-19T04:47:48Z
hash: 25555c17344c

table_claims: 12

end-knowledge-index -->
```

### research/immigration-causal-internal-vs-immigrant-newcomers.md

```text
# Domestic migration vs moved-from-abroad counts as newcomer shocks

Supersession note: this memo is retained for provenance, but its original `33x`
headline is outdated and too strong. After replacing the ACS side with
`B07001_081E` (`Moved from abroad in the past year`), the current descriptive
county comparison is about `4.49%` IRS `Total Migration-US` inflow versus
`0.21%` ACS moved-from-abroad at the median county with `totpop >= 10k`, or
roughly `20.5x`. That is still not a like-for-like burden ratio because the two
sources use different universes and time windows.

**Date:** 2026-04-18
**Question:** Is "immigrant" or "newcomer in general" the right unit of analysis for the school/housing/capacity burden discussion in the existing repo?
**Answer:** **Newcomer in general**, descriptively. The county-level newcomer counts are dominated by IRS `Total Migration-US`, but the exact ratio depends on incomparable administrative and ACS measurement frames and should not be read as a clean causal burden split.

## Bottom line

The existing repo's `low-skill-origin-incidence-memo.md` and the local-burden findings have implicitly treated "immigrant inflow" as the dominant source of newcomer pressure on counties' schools and housing. The descriptive county comparison still argues against that shortcut, but the original `33x` statement overstated what the data can support. The current county parquet says the median county receives about `4.49%` of population as IRS `Total Migration-US` inflow versus about `0.21%` ACS moved-from-abroad, or roughly `20.5x`. **The safe conclusion is that the newcomer-burden frame should disaggregate domestic newcomer flow from moved-from-abroad flow because they are different orders of magnitude and have different policy levers.**

This does not erase the immigrant-specific story (concentration, language, household composition, legal status all still matter). But it sharply revises the frame: much of what shows up as "newcomer" pressure in county aggregates is not immigration-specific.

**Confidence:** HIGH on the absolute size disparity (IRS SOI counts tax filers — administrative data, not survey). MEDIUM on the per-newcomer burden parity (composition differs: military families, retirees, remote workers vs labor-migrant immigrants).

## Method

### Data
- **IRS SOI county-to-county migration 2022-2023** — administrative tax-filer migration. Aggregate row code y1=97 = "Total Migration-US" (excludes foreign). 4.6 MB CSV per file (inflow + outflow). Reports number of returns, exemptions, and aggregate AGI by destination county. [SOURCE: irs.gov/pub/irs-soi/countyinflow2223.csv]
- **ACS 2022 5-yr** — county-level B01003 (totpop), B05002 (foreign-born stock), B05005_002E (foreign-born entered 2010-or-later, ≈ recent arrivals 12-year window), B25064 (median rent), B19013 (median income).
- **Match:** state_fips × county_fips (FIPS5). 9,120 county-merged rows after one-to-many join (county-fips repeated due to multiple inflow source rows; stylized facts use medians robust to this).

### Definitions
- "Native US-inflow" = aggregate annual exemption count moving across counties from anywhere in the US (per IRS SOI). Most are US-born; small share are settled foreign-born already in the US who change county.
- "Recent foreign-born annual flow" = foreign-born population entered 2010-or-later (per ACS B05005), divided by 12 to annualize the 12-year accumulation.
- Both measured as share of destination county population.

## Stylized facts

### Fact 1: native flow is ~33× larger per year
Median county (≥10,000 pop, n=7,286):
- Native US-inflow share: **3.00% per year**
- Recent FB annual flow: **0.08% per year**
- Ratio: **33×**

### Fact 2: top counties by NATIVE inflow are military bases and Sun Belt exurbs
| County | Pop | Inflow share | Median rent |
|--------|-----|--------------|-------------|
| Geary County, KS (Fort Riley) | 36,247 | **16.4%** | $1,132 |
| Long County, GA | 16,804 | 15.7%

... [truncated for review packet] ...

on is the dominant newcomer flow into US counties; immigration is a small fraction in absolute terms`** — `STRONG`. Median county receives 3.0% native + 0.08% immigrant inflow per year (33× ratio). [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

### Adversarial review §3 (school burden too coarse)
The earlier review flagged that district school-burden was under-modeled. This finding adds: **the school burden of immigrant-origin children may be misattributed**. A district in Comal County TX (12% native inflow, low immigrant inflow) faces school capacity strain that is overwhelmingly native-driven. A district in Miami-Dade FL faces strain that is more immigrant-driven. The right policy intervention differs.

## Honest limits

1. **Composition of native vs immigrant newcomers differs sharply.**
   - Native newcomers in top-list counties: military families (Fort Riley, Fort Stewart), retirees (Florida), DC-area government workers, exurb developers
   - Immigrant newcomers in top-list counties: working-age labor migrants, family-reunification, refugees
   - Per-newcomer school enrollment, per-newcomer rent payment, per-newcomer wage competition all differ
   - The "33× ratio" is gross flow ratio, not "burden equivalence"

2. **Geography of impact differs.**
   - County aggregate masks within-county sorting
   - Immigrants concentrate in specific neighborhoods/PUMAs; natives sort more diffusely
   - The local impact at the school-attendance-zone or ZIP level may have different relative magnitudes
   - Texas exurbs (top native-inflow) sprawl across new construction, so capacity can scale; older-city PUMAs in Miami-Dade can't

3. **IRS SOI undercount.**
   - Tax filer migration misses non-filers (very-low-income, students, undocumented)
   - These omissions affect the immigrant comparison too — both sides probably undercounted
   - Direction of bias on the ratio is ambiguous

4. **Annualization of B05005 12-year stock is rough.**
   - Recent FB flow is not constant over 2010-2022
   - Mexican-origin flow declined 2008-2018, NTCA flow rose 2018+
   - The 0.08% number is a 12-year average, may understate 2020-2022 flow
   - Even doubling it (0.16%) leaves a 19× ratio — the qualitative finding is robust to large adjustments

5. **What this does NOT settle.**
   - Immigration's effect on schools, wages, rent at PUMA / neighborhood scale (where it's concentrated)
   - The compositional integration concerns (language, cultural, visibility)
   - Whether second-generation outcomes differ between high-native-inflow and high-immigrant-inflow counties
   - Federal fiscal incidence (still requires the SIPP fix from prior cycle)

## Decision-relevant claim

Any future repo memo that says "newcomer burden in county X" without distinguishing native-newcomer from immigrant-newcomer flow is using a misleading frame. The correct framing is: "X% of newcomer flow is native (Y), Z% is immigrant (W)." County-level data routinely makes this disaggregation, so there's no excuse for the conflated frame.

For the project's central question ("which low-skill immigration flows degrade local-system capacity"), this finding doesn't kill the question — it adds a comparative anchor: most school/housing/service strain in fast-growing US counties is being absorbed without immigration as the proximate cause. Wherever immigration IS the proximate cause (Miami-Dade, Hudson NJ, San Jose CA, Colfax NE), it operates at much smaller scale than internal native migration in equally-stressed Sun Belt exurbs.

[SOURCE: data/internal_migration/county_inflow_2022_23.csv]
[SOURCE: data/analysis/county_newcomer_comparison.parquet]
[SOURCE: scripts/analyze_internal_vs_immigrant_newcomers.py]
[SOURCE: api.census.gov/data/2022/acs/acs5 (B05005, B05002, B25064, B19013)]

<!-- knowledge-index
generated: 2026-04-19T04:19:50Z
hash: 309f7e3f68b3

cross_refs: research/immigration-causal-internal-vs-immigrant-newcomers.md

end-knowledge-index -->
```

### research/immigration-confidence-ladder.md

```text
# Immigration confidence ladder

Date: 2026-04-10

Scale:
1. `strong`
2. `medium`
3. `weak`
4. `contextual-only`

Rule:
A metric can be statistically clean and still be only `contextual-only` for the question we are asking.

## Strong

1. `ACS origin / education / recency composition counts`
Rating: `strong`
Reason: these are direct weighted ACS summaries, not inferred fiscal objects. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_origins.sql]

2. `PUMA-level median gross rent as destination cost exposure`
Rating: `strong`
Reason: official ACS geography, directly observed, useful as exposure context. It is not a welfare scalar. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]

3. `Household-normalized school-age child metrics after WGTP correction`
Rating: `strong`
Reason: the prior proxy was wrong; the corrected household join is materially better and uses the right unit. [SOURCE: /Users/alien/Projects/research/research/immigration-household-weighted-correction.md]

4. `Claim that the Clark “agree” papers are scope-limited rather than obviously false`
Rating: `strong`
Reason: that conclusion survives repeated paper review and is consistent with the actual paper scopes. [SOURCE: /Users/alien/Projects/research/research/immigration-economist-effects-matrix.md]

## Medium

5. `Federal versus state/local incidence split as a research frame`
Rating: `medium`
Reason: official sources strongly support the split, but our own warehouse only partially models the federal side. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

6. `County CHAS housing-stress shares`
Rating: `medium`
Reason: good background stress metric, but not immigrant-attributable marginal burden. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_stage2_incidence_context.py]

7. `State school-spending per pupil as school-pressure context`
Rating: `medium`
Reason: official and clean, but too coarse for marginal burden or district-specific claims. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql]

8. `Housing-heavy versus school-heavy origin-group typology`
Rating: `medium`
Reason: useful descriptive shorthand for destination exposure, but still proxy-based and sensitive to geography choice. [SOURCE: /Users/alien/Projects/research/research/immigration-local-burden-puma-layer.md]

9. `Descendant upside as a real channel`
Rating: `medium`
Reason: the long-run literature supports it, but sign and magnitude are heterogeneous and horizon-dependent. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.nber.org/system/files/working_papers/w33961/w33961.pdf]

## Weak

10. `Area-weighted PUMA-to-county bridge`
Rating: `weak`
Reason: land area is not people, renters, students, or immigrant households. This is a convenience bridge, not a precise exposure model. [SOURCE: /Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py]

11. `IRS county migration balance as burden evidence`
Rating: `weak`
Reason: at best it is contextual mobility climate. It is not immigrant-specific and not causal. [SOURCE: /Users/alien/Projects/research/research/immigration-stage2-county-bridge-batch.md]

12. `Federal-positive versus federal-negative origin ranking from ACS income and benefit proxies`
Rating: `weak`
Reason: this is not a tax-transfer microsimulation. It is a partial proxy stack. [SOURCE: /Users/alien/Projects/research/research/immigration-low-skill-origin-incidence-memo.md]

13. `Magnitude claims for local school burden from current warehouse`
Rating: `weak`
Reason: district assignment, ELL intensity, migrant com

... [truncated for review packet] ...

 multiplier (~1.6) $2.32T. Per-removed-worker loss $207K-$332K. Most affected: Construction (-5.9%), Other services / cleaning (-8.8%), Agriculture (-4.3%). Calibration consistent with E-Verify empirical finding (-6% E1 employment under 50% compliance). [SOURCE: scripts/mass_deportation_sim.py]

## Surge layer added 2026-04-18 (late evening)

25. `Title 42 lift was not the surge cause; surge was a regime shift starting Dec 2022`
Rating: `medium`
Reason: SWB encounters peaked Jan-Mar 2023 at 50K+/month BEFORE Title 42 lift (May 2023). Lift coincided with April-May lull, then gradual rebuild to surge levels. Pre/post comparison is composition-driven, not policy-causal. [SOURCE: research/immigration-causal-surge-2021-2024.md]

26. `CHNV parole did not substitute legal flow for illegal flow; it added on top`
Rating: `strong`
Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023. Encounters from CHNV nationalities ROSE 787% post-program, not fell. Refutes the stated rationale that legal pathway would reduce irregular migration. [SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]

27. `Receiver-city local fiscal load was real and concentrated`
Rating: `strong (administrative data)`
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M peak; Denver $89M (with cuts to other services). Combined ~$5B+/yr peak across major receivers. System-collapse claim has empirical bite. [SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers`
Rating: `medium (correlation, multiple confounders)`
Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***). Top receivers (Bronx +11pp, Queens +11pp, Hidalgo +10pp, Cameron +10pp, El Paso +10pp, Miami-Dade +9pp) swung massively toward Trump. Confounders include national Hispanic realignment, inflation, and policy-endogenous busing destinations. Magnitude implausibly large for non-immigration causes alone. [SOURCE: research/immigration-causal-surge-2021-2024.md]

29. `Static-cycle Card-wins finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation`
Rating: `meta-update on prior entries 17, 19, 21`
Reason: Prior entries claim "decisive Card-side win for U.S. policy variation." True for variation 2008-2021 (E-Verify, sanctuary). The 2021-2024 surge is a regime shift outside that variation. Linear extrapolation is not warranted. Surge-period wage estimates remain to be done (require ACS PUMS 2023). [SOURCE: research/immigration-causal-surge-2021-2024.md]

## Two weakest assumptions

1. `Federal-side proxy ledger`
Current shortcut: infer federal incidence from income plus selected benefit flags.
Why weak: taxes, credits, SNAP, SSI, Medicaid, payroll taxes, and household composition are not directly modeled.

2. `Coarse local burden bridge`
Current shortcut: state school-spend plus PUMA rent plus area-weighted county overlays.
Why weak: local service burden depends on actual district context, renter mix, crowding, tract population, and school-age distribution, not land area.

## Practical reading rule

If a conclusion depends mainly on items `10` through `16`, present it as a hypothesis or descriptive tendency, not a settled result.

<!-- knowledge-index
generated: 2026-04-19T04:47:35Z
hash: 7c9873d31903

cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-surge-2021-2024.md, research/research/immigration-adversarial-review.md, research/research/immigration-economist-effects-matrix.md, research/research/immigration-household-weighted-correction.md, research/research/immigration-local-burden-puma-layer.md, research/research/immigration-low-skill-origin-incidence-memo.md, research/research/immigration-stage2-county-bridge-batch.md

end-knowledge-index -->
```

### research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md

```text
# Paradigm-escape cycle synthesis (2026-04-18, evening)

**Cycle goal:** Run Paths A + B + C from the brainstorm — sharpen the prior cycle's findings (Saiz decomposition, Foged-Peri lag, mass-deportation simulation) AND escape the prior frame (open-borders calibration, internal-native comparison, sanctuary city DiD).

**Inputs to this synthesis:**
1. `immigration-causal-internal-vs-immigrant-newcomers.md` — IRS SOI × ACS comparison
2. `data/clemens/gpt54_calibration_review.md` — GPT-5.4 sensitivity + binding-constraint analysis (Clemens 2011 calibration)
3. `data/analysis/saiz_decomposition.parquet` + console output — regulatory vs topographic channel
4. `data/analysis/sanctuary_twfe_results.csv` — sanctuary state DiD on QWI
5. `data/analysis/mass_deportation_summary.json` — BEA I-O 11M removal simulation

## Bottom line — five updates to the repo's verdict

| Pre-cycle position | New evidence | Updated verdict |
|---|---|---|
| "Rent exposure ≠ welfare loss" was a strong adversarial caveat | Saiz decomposition: log(FB share) ~ unaval (β=0.12, n.s.) + WRLURI (β=0.33, t=6.29***); regulatory channel dominates | **Rent exposure IS welfare loss AND zoning reform is a viable policy lever** — rent burden is policy-tractable, not topographic |
| Card-vs-Borjas "live debate"; prior cycle showed E-Verify null wage effect | Sanctuary state DiD on same QWI panel: pro-sanctuary E1 wages +0.5% (n.s.), anti-sanctuary E1 wages +0.8% (n.s.) — **third confirmation** | **Native low-skill wages do not respond to enforcement variation in either direction.** Card wins decisively on observed U.S. policy variation. |
| "Newcomer burden" treated as immigration-driven by default | IRS SOI `Total Migration-US` and ACS `Moved from abroad` still show an order-of-magnitude county gap, but the exact ratio is measurement-sensitive and not a clean burden ratio | **Most county newcomer pressure is not immigration-specific.** Treat this as a descriptive frame correction, not a precise causal burden split. |
| Mass-deportation hypothetical had no empirical analog | BEA I-O 2023 calibration: removing 7M unauthorized → $1.45T first-order output loss (5.3% GDP); $2.32T with multiplier (8.5%); per-removed-worker loss $207K-$332K, ~7-11× their own annual earnings | **Mass deportation would impose a one-time $1.5-2.3T output shock**, concentrated in Construction (-5.9%), Other Services / cleaning (-8.8%), Agriculture (-4.3%) |
| Repo verdict implicitly weights immigrant welfare at zero | GPT-5.4 calibration with project's findings as inputs: at w=0 negative by construction; at w≥0.25 positive under 25%-cost benchmark; housing/construction binds in year 1 for every scenario S1+ | **Verdict is welfare-weight-driven, not data-driven, in the dimension that matters most.** Honest framing must name the weight. Feasibility constraint: U.S. housing/construction binds immediately at any scenario above ~10M/year arrivals. |

## What this cycle didn't settle

- **Federal microsim** still broken (SSD blocker from prior cycle; SIPP HHINC bug). Highest-leverage single fix that remains.
- **Foged-Peri 6-yr lag** deferred (disk-constrained ACS PUMS pull; lower marginal value than completed items).
- **DACA pre-post**, **Diversity Visa lottery**, **Immigration judge IV** — Tier 1 brainstorm items not executed this cycle.
- **Sending-country welfare** — still unaddressed, but partially subsumed by the open-borders calibration which forces the question.
- **Comparative international regimes** — Tier 3 brainstorm item not executed.

## Synthesis of the two cycles (2026-04-18 morning + evening)

### Eight findings now in the repo

| # | Finding | Confidence | Method |
|---|---------|------------|--------|
| 1 | E-Verify mandates do not raise native low-skill wages | STRONG REJECTION of Borjas | TWFE on QWI 2003-23, 9 states |
| 2 | E-Verify mandates reduce E1 employment in exposed industries ~6% (marginal) | MEDIUM | Same |
| 3 | Sanctuary policy variation produces n

... [truncated for review packet] ...

ata/clemens/gpt54_calibration_review.md]

24. `Mass deportation of 7M unauthorized would impose ~$1.5-2.3T one-time output shock (5-8% GDP)`
Rating: MEDIUM (calibration not estimate)
Reason: BEA I-O 2023 partial-equilibrium with industry FB-share assumptions;
consistent with E-Verify -6% E1 employment finding under 50% compliance
[SOURCE: scripts/mass_deportation_sim.py]
```

## Methodological note

This cycle used **GPT-5.4 (high-then-medium reasoning effort) for the open-borders sensitivity analysis** because the question required parameter sensitivity reasoning across 5 sections that exceeds Claude's typical chain-of-thought depth. The first dispatch hit the max-tokens-includes-reasoning footgun (24K budget exhausted by reasoning, 0 visible output). The second dispatch with 48K budget and concatenated single context file produced a 16.5KB structured response. The result was integrated into the synthesis above.

This is the right division of labor: **Claude orchestrates and runs analyses on local data; GPT-5.4 handles parameter-sensitivity reasoning over a fixed framework.** Routing per `~/.claude/rules/llmx-routing.md`.

## What to do next (priority order)

1. **Mount SSD and re-run Saiz×PUMA + warehouse merges** — the Saiz finding is at MSA level; the existing warehouse has PUMA-level data that would sharpen everything. Same blocker as morning cycle.
2. **Fix SIPP donor library + run federal microsim** — same call from 2026-04-10. Highest-leverage single fix on the repo.
3. **Run DACA pre-post on ACS PUMS** — the design is documented, just needs execution. Free up disk first.
4. **Run Foged-Peri 6-yr lag replication** — also disk-constrained but smaller. Could explain Card-side wage finding via lag distribution.
5. **Sending-country welfare ledger** — natural extension of open-borders frame.
6. **Comparative international regimes** — Gulf Kafala / Canada points / Germany 2015 to test what's regime-specific.
7. **Diversity Visa lottery RCT** — true random assignment data for cleanest causal evidence.
8. **Immigration judge IV** — TRAC EOIR data for de facto policy.

Items 1-4 should be sequential; 5-8 can run independently in parallel cycles.

## Honest reflection

This was a productive cycle, but the *data* additions did not produce paradigm shifts — they sharpened existing positions. The two findings that genuinely change the repo's framing are:
- **Internal-native migration comparison** (the 33× ratio) — disrupts the "newcomer = immigrant" frame
- **Welfare-weight reframing of open-borders** — names the implicit zero-weight assumption that drives the verdict

The other findings (Saiz decomposition, sanctuary DiD, mass-deportation sim) are confirmatory or refining. Useful, not transformative.

The biggest *interpretation* lever remains the welfare-weight question, which is a values choice that no additional empirical work resolves. The repo can either (a) make the implicit zero weight explicit and own it, (b) shift to a documented non-zero weight and re-grade everything, or (c) report multiple weighted scenarios as scenario analysis. Option (c) is honest; (a) and (b) are equally legitimate but should stop hiding the choice.

[SOURCE: research/immigration-causal-everify-card-vs-borjas.md]
[SOURCE: research/immigration-causal-saiz-elasticity-rent.md]
[SOURCE: research/immigration-causal-synthesis-2026-04-18.md]
[SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]
[SOURCE: data/clemens/gpt54_calibration_review.md]
[SOURCE: data/analysis/sanctuary_twfe_results.csv]
[SOURCE: data/analysis/mass_deportation_summary.json]
[SOURCE: scripts/saiz_decomposition.py]

<!-- knowledge-index
generated: 2026-04-19T04:21:56Z
hash: cb845f425587

cross_refs: research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-synthesis-2026-04-18.md

end-knowledge-index -->
```

### sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json

```text
{
  "rows": 2390,
  "elect_counties": 2390,
  "qcew_counties": 3284,
  "qcew_missing_counties": 0,
  "irs_inflow_missing_rows": 0,
  "irs_outflow_missing_rows": 0,
  "qcew_non_disclosure_rows_by_year": {
    "2017": 1,
    "2018": 2,
    "2019": 0,
    "2020": 0,
    "2021": 0,
    "2022": 0,
    "2023": 2,
    "2024": 0
  },
  "qcew_non_disclosure_rows_in_analysis_sample_by_year": {
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0,
    "2022": 0,
    "2023": 0,
    "2024": 0
  },
  "irs_migration_layer": {
    "source": "IRS county-to-county migration files",
    "codes_used": [
      "97/000 inflow",
      "97/000 outflow"
    ],
    "interpretation": "Total Migration-US aggregate, not a native-incumbent-only measure."
  },
  "qcew_nondisclosure_policy": {
    "trigger": "disclosure_code == 'N'",
    "treatment": "Mask annual_avg_emplvl, total_annual_wages, and annual_avg_wkly_wage to missing before numeric coercion.",
    "implication": "Any log-change window with a suppressed endpoint inherits missingness rather than silently keeping a coerced numeric value."
  },
  "qcew_missing_cells_by_year": {
    "2017": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2018": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2019": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2020": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2021": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2022": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2023": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    },
    "2024": {
      "annual_avg_emplvl_missing": 0,
      "annual_avg_wkly_wage_missing": 0,
      "total_annual_wages_missing": 0,
      "annual_avg_emplvl_nonpositive": 0
    }
  },
  "qcew_window_metadata": {
    "qcew_employment_log_change_2017_2018": {
      "base_year": 2017,
      "end_year": 2018,
      "label": "clean_pre_covid_early",
      "touches_2020": false,
      "window_role": "presurge_check",
      "contaminated": false,
      "reason": "Second clean annual pre-COVID window for pretrend checks.",
      "metric": "employment",
      "missing_input_count": 0,
      "nonmissing_count": 2390,
      "zero_base_count": 0,
      "nondisclosure_missing_base_count": 0,
      "nondisclosure_missing_end_count": 0,
      "analysis_sample_missing_recent_fb_share_mean": null,
      "analysis_sample_nonmissing_recent_fb_share_mean": 0.0013689445336571397,
      "analysis_sample_missing_permit_rate_mean": null,
      "analysis_sample_nonmissing_permit_rate_mean": 15.013658082802595
    },
    "qcew_wkly_wage_log_change_2017_2018": {
      "base_year": 2017,
      "end_year": 2018,
      "label": "clean_pre_covid_early",
      "touches_2020": false,
      "window_role": "presurge_check",
      "contaminated": false,
      "reason": "Second clean annual pre-COVID window for pretrend checks.",
      "metric": "weekly_wage",
      "missing_input_count": 0,
      "nonmissing_count": 2390,
      "zero_base_count": 0,
      "nondisclosure_missing_base_count": 0,
      "nondisclosure_missing_end_count": 0,
      "analysis_sample_missing_recent_fb_share_m

... [truncated for review packet] ...

 post-surge span; descriptive/summary window rather than presurge placebo.",
      "metric": "weekly_wage",
      "missing_input_count": 0,
      "nonmissing_count": 2390,
      "zero_base_count": 0,
      "nondisclosure_missing_base_count": 0,
      "nondisclosure_missing_end_count": 0,
      "analysis_sample_missing_recent_fb_share_mean": null,
      "analysis_sample_nonmissing_recent_fb_share_mean": 0.0013689445336571397,
      "analysis_sample_missing_permit_rate_mean": null,
      "analysis_sample_nonmissing_permit_rate_mean": 15.013658082802595
    }
  },
  "qcew_employment_log_change_2017_2018_zero_base_count": 0,
  "qcew_employment_log_change_2017_2018_missing_input_count": 0,
  "qcew_employment_log_change_2017_2018_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2017_2018_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2017_2018_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2017_2018_nonmissing_count": 2390,
  "qcew_employment_log_change_2018_2019_zero_base_count": 0,
  "qcew_employment_log_change_2018_2019_missing_input_count": 0,
  "qcew_employment_log_change_2018_2019_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2018_2019_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2018_2019_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2018_2019_nonmissing_count": 2390,
  "qcew_employment_log_change_2018_2020_zero_base_count": 0,
  "qcew_employment_log_change_2018_2020_missing_input_count": 0,
  "qcew_employment_log_change_2018_2020_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2018_2020_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2018_2020_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2018_2020_nonmissing_count": 2390,
  "qcew_employment_log_change_2019_2020_zero_base_count": 0,
  "qcew_employment_log_change_2019_2020_missing_input_count": 0,
  "qcew_employment_log_change_2019_2020_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2019_2020_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2019_2020_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2019_2020_nonmissing_count": 2390,
  "qcew_employment_log_change_2020_2021_zero_base_count": 0,
  "qcew_employment_log_change_2020_2021_missing_input_count": 0,
  "qcew_employment_log_change_2020_2021_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2020_2021_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2020_2021_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2020_2021_nonmissing_count": 2390,
  "qcew_employment_log_change_2021_2022_zero_base_count": 0,
  "qcew_employment_log_change_2021_2022_missing_input_count": 0,
  "qcew_employment_log_change_2021_2022_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2021_2022_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2021_2022_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2021_2022_nonmissing_count": 2390,
  "qcew_employment_log_change_2021_2023_zero_base_count": 0,
  "qcew_employment_log_change_2021_2023_missing_input_count": 0,
  "qcew_employment_log_change_2021_2023_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2021_2023_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2021_2023_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2021_2023_nonmissing_count": 2390,
  "qcew_employment_log_change_2023_2024_zero_base_count": 0,
  "qcew_employment_log_change_2023_2024_missing_input_count": 0,
  "qcew_employment_log_change_2023_2024_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2023_2024_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2023_2024_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2023_2024_nonmissing_count": 2390,
  "qcew_employment_log_change_2021_2024_zero_base_count": 0,
  "qcew_employment_log_change_2021_2024_missing_input_count": 0,
  "qcew_employment_log_change_2021_2024_nonmissing_count": 2390,
  "qcew_wkly_wage_log_change_2021_2024_zero_base_count": 0,
  "qcew_wkly_wage_log_change_2021_2024_missing_input_count": 0,
  "qcew_wkly_wage_log_change_2021_2024_nonmissing_count": 2390
}
```

### Omitted Files

```text
(Omitted 6 additional touched files from excerpts.)
```
```

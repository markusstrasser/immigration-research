# Research — Getting to the Truth

## Purpose
This repo pursues empirical questions with the rigor of investigative scholarship. Topics vary (currently IQ sex differences) but the methodology is constant: primary sources, competing interpretations, falsifiable claims, honest uncertainty.

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

## Git Workflow

All commits to main. No branches.

```
[scope] Verb thing — why
```

Scopes: `[research]` (findings), `[analysis]` (data work), `[docs]` (index/notes), `[infra]` (tooling/config).

## Tools Available

### Skills (symlinked from `~/Projects/skills/`)
- **researcher** — autonomous research orchestration with epistemic rigor
- **epistemics** — bio/medical/scientific evidence hierarchy
- **causal-dag** — DAG-first causal analysis, back-door criterion validation
- **causal-robustness** — post-estimation sensitivity analysis (PySensemakr)
- **causal-check** — lightweight causal reasoning discipline
- **competing-hypotheses** — Analysis of Competing Hypotheses (ACH)
- **model-review** — cross-model adversarial review
- **entity-management** — versioned knowledge management
- **source-grading** — NATO Admiralty System for source/info grading
- **project-upgrade** — autonomous codebase improvement
- **google-workspace** — Google Workspace automation

### MCP Servers (`.mcp.json`)
- **exa** — semantic web search, entity enrichment, deep research
- **research** (papers-mcp) — Semantic Scholar (220M+ papers), corpus management, claim verification
- **brave-search** — independent web index (triangulation with Exa)
- **perplexity** — grounded AI answers, deep research, reasoning
- **paper-search** — arXiv, PubMed, bioRxiv, medRxiv, Google Scholar
- **meta-knowledge** — cross-project knowledge base (hook designs, agent patterns, research findings)
- **context7** — library documentation lookup

## Structure

```
research/          — topic files, one per question or area
sources/           — archived source material, data files
notes/             — working notes, drafts, threads of analysis
```

## Research & Docs Index

Files the agent should consult before acting. Start with the current-state files, then drill down.

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-current-position.md` | Current best synthesized take, established vs open claims, next discriminating tests | Answering "what do we know now?", updating summaries, deciding what matters next |
| `research/iq-sex-differences-claim-register.md` | Claim-level ledger with status, confidence, provenance, and falsifiers | Making or revising any strong claim about sex differences, `g`, schooling, or measurement artifacts |
| `research/iq-sex-differences-decisive-causal-tree.md` | Explicit causal tree showing which nodes are already live, which remain open, and which analyses can actually kill them | Proposing new causal stories, prioritizing DOE, or deciding what would count as a decisive next result |
| `research/iq-sex-differences-master-plan.md` | Canonical end-to-end roadmap with stage order, experiments, statistics, literature tracks, validation ladder, and completion criteria | Planning the remaining project, deciding what "solid" means, or assigning the next tranche of work |
| `research/iq-sex-differences-execution-plan.md` | Ordered work plan with stages, estimands, outputs, and stop rules | Choosing the next tranche, assigning work, or checking what "done" means before moving to the next node |
| `research/iq-sex-differences-frontier-literature-audit.md` | Audit of 2023-2025 literature showing which pieces the frontier already sees and what this repo may be integrating better | Answering whether the repo has a genuinely new synthesis, checking recent-paper updates, or aligning the causal tree to the latest literature |
| `research/iq-sex-differences-model-review-2026-03-06.md` | Cross-model blind-spot review of the current project state, including what Gemini and GPT criticism survived local scrutiny | Reusing the latest external-model critique, deciding what to soften in the canonical claims, or checking whether a proposed interpretation already failed the blind-spot review |
| `research/iq-sex-differences-early-school-intake.md` | Operational intake note for the early-school node, including why `NLSCYA` goes first, `ECLS-K:2011` second, and `ECLS-K` third | Starting Stage 2, choosing which early-school dataset to parse next, or checking whether `ECLS` is actually locally usable |
| `research/review-1-audit.md` | Audit of the external GPT review, including what was adopted vs rejected | Reusing claims from `review-1.md`, revising the `NLSY97` Stage A interpretation, or choosing the next data pass |
| `research/iq-sex-differences-evaluation-placement-node.md` | Grade-test wedge, evaluation / placement asymmetry, and why grades are not clean ability proxies | Using grades, honors, recommendations, or school-linked placement variables in causal models |
| `research/iq-sex-differences-dataset-expansion.md` | Which external datasets are actually staged, partial, metadata-only, or access-gated | Planning dataset acquisition, deciding what can be run now, or checking whether a cited dataset is local versus aspirational |
| `research/iq-sex-differences-nces-datalab-acquisition.md` | Exact NCES `Online Codebook` API path, landed `HSLS` / `ELS` / `NELS` bundles, and the `HS&B` server failure | Touching NCES longitudinal data acquisition, deciding whether `HSLS` / `ELS` / `NELS` are truly local, or debugging the `HS&B` access path |
| `research/iq-sex-differences-analysis-protocol.md` | Frozen estimands, score rules, weights, and covariate blocks | Running models, comparing datasets, or questioning field choices |
| `research/iq-sex-differences-doe.md` | Full staged research program and decision thresholds | Planning new analyses or new dataset acquisition |
| `research/iq-sex-differences-next-node-validation.md` | Why the `NLSY97` quantitative anomaly is the active causal fork | Choosing the next causal node or evaluating the `NLSY97` sign flip |
| `research/iq-sex-differences-pisa2018-item-split.md` | First public `PISA 2018` item/process pass showing broad male-leaning math with heterogeneous item-level gaps | Discussing whether school-age disagreement is generic process burden versus item-family heterogeneity |
| `research/iq-sex-differences-pisa2018-framework-proxy.md` | Proxy content/context decomposition of `PISA 2018` units showing the current school-age item geometry by framework family | Discussing whether the school-age split is coherent by content family, or deciding what the next `PISA` hardening step should be |
| `research/iq-sex-differences-pisa2018-dif-proxy.md` | First ability-conditioned `PISA 2018` item-fairness pass, separating raw item gaps from residual content-family effects | Discussing school-age item fairness, deciding whether `space_shape` survives conditioning, or choosing between `TIMSS` porting and heavier IRT / anchor-item work |
| `research/iq-sex-differences-pisa2018-dif-leaveout.md` | Contamination-aware `PISA 2018` follow-up using focal-item and focal-family leave-out matching scores | Using the current best `PISA` conditioning result, checking whether the residual family ordering survived the blind-spot fix, or deciding whether full IRT is still worth the marginal gain |
| `research/iq-sex-differences-nlscya-early-school-first-pass.md` | First local early-school pass showing how `PIAT Math`, reading comprehension, and `PPVT` behave in public `NLSCYA` | Discussing whether the early-school node is already locally resolved or deciding what `ECLS-K:2011` needs to replicate |
| `research/iq-sex-differences-eclsk2011-early-school-first-pass.md` | First `ECLS-K:2011` replication of the early-school node, showing near-parity kindergarten math and male widening by spring first/second grade | Discussing whether early-school emergence is real, whether `NLSCYA` generalizes, or what the older `ECLS-K` cohort must now adjudicate |
| `research/iq-sex-differences-eclsk-early-school-first-pass.md` | Older `ECLS-K` replication of the early-school node, showing broad school-entry math already modestly male and more male by spring first grade | Discussing whether the two `ECLS` cohorts align, whether `NLSCYA` is the outlier score family, or what the next early-school alignment step should be |
| `research/iq-sex-differences-early-school-ach.md` | Formal ACH and causal-check memo on the `NLSCYA` versus `ECLS` early-school anomaly | Deciding whether the live early-school disagreement is mainly score-family, sample-frame, cohort shift, or artifact |
| `research/iq-sex-differences-early-school-score-alignment.md` | First bridge pass aligning child math to same-wave reading, showing the raw `NLSCYA` anomaly mostly collapses directionally | Discussing whether the early-school conflict is real, checking the ACH prediction, or choosing the next child-score alignment step |
| `research/iq-sex-differences-early-school-age-matched-alignment.md` | Second bridge pass using explicit overlapping age windows, showing the child-level sign conflict stays gone and the remaining difference is magnitude | Discussing whether the child branch is directionally resolved, or deciding whether to stay on child alignment versus move back to the late-school transcript node |
| `research/iq-sex-differences-item-face-validity-audit.md` | Direct inspection of released `PISA` items and official `ASVAB` sample items, separating visible construct-loading from overread claims about obvious bias | Making page-level claims about "biased items," deciding whether visible item burden matches the current content-family results, or checking whether the repo has any face-valid smoking gun |
| `research/iq-sex-differences-nlsy97-piat-cat-pass.md` | Same-cohort `PIAT Math` versus `CAT-ASVAB` pass showing where the `NLSY97` anomaly actually lives | Discussing whether `NLSY97` reflects broad quantitative ability, a `Math Knowledge` wedge, or a school-surface effect |
| `research/iq-sex-differences-timss-cognitive-split.md` | Focused `TIMSS` knowing / applying / reasoning memo that tests whether the `NLSY97` wedge generalizes across school-age batteries | Discussing whether the active node is really about school-knowledge surfaces versus applied / reasoning and track selection |
| `research/iq-sex-differences-nlsy97-stage-a.md` | Current best internal evidence on process / precision vs raw `NLSY97` quantitative gap | Discussing whether the raw `NLSY97` female edge is real |
| `research/iq-sex-differences-piaac-frontier.md` | Adult numeracy by country and education | Discussing education-stratified adult numeracy patterns |
| `research/iq-sex-differences-piaac-age-occupation.md` | Adult numeracy by age band and broad occupation | Discussing whether age or occupation creates vs amplifies the adult numeracy gap |
| `research/iq-sex-differences-second-pass-results.md` | [current] `NLSY79` same-sample schooling pass | Discussing schooling / practice attenuation in the within-family design |
| `research/iq-sex-differences-first-pass-results.md` | [historical] initial `NLSY79` pass | Recovering earlier assumptions or checking how the same-sample correction changed the story |
| `research/iq-sex-differences-nlsy97-replication.md` | [historical] raw cohort replication before Stage A | Recovering the pre-process view of the `NLSY97` anomaly |
| `research/iq-sex-differences-verification.md` | Literature audit of the repo's main conclusions | Making literature claims about overall `g`, variability, or domain differences |
| `research/iq-sex-differences-causal-graph.md` | Outside narratives, causal graph, and harden/soften nodes | Mapping Taleb / Cremieux / Gwern / Gelman style arguments into testable nodes |
| `research/iq-sex-differences-test-construction.md` | [historical, monolith] original long-form research memo | Needing the original stitched narrative and full extracted notes |
| `notes/iq-sex-differences-context-open-questions.md` | Outcome relevance, schooling-confounding, and popular-culture argument spillover | Asking whether any of these subtest gaps matter for productivity, earnings, or life outcomes |

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

## Analysis Quick-Start

```bash
# Run any analysis script
uv run python3 sources/iq-sex-diff/<script>.py

# Data lives in sources/iq-sex-diff/data/<dataset>/
# Output TSVs land alongside the data or in the same data subdir
```

Key script families: `pisa2018_dif_*.py` (measurement/DIF), `psid_cds_*.py` (child/family), `*_first_pass.py` / `*_pass.py` (dataset surface passes), `*_prototype.py` (latent models). Dependencies in `sources/iq-sex-diff/pyproject.toml`.

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
decisions/         — concept-level pivots, approach selections, methodology shifts
sources/           — archived source material, data files
notes/             — working notes, drafts, threads of analysis
```

## Decision Journal (`decisions/`)

Records of concept-level pivots — when an interpretation shifts, a methodology is adopted/dropped, a causal node gets resolved or reopened. One file per decision, `YYYY-MM-DD-slug.md`. Template in `decisions/.template.md`. Records use YAML frontmatter for machine-readable metadata (concept grouping, typed relations, provenance).

**When to write:** path-dependent interpretation choices, dropping a hypothesis after evidence, adopting a new dataset/method that forecloses alternatives, resolving a causal fork where the reasoning is costly to reconstruct. Do NOT write for: parameter tweaks, routine implementation, local execution details.

**Research memos:** when updating with revised understanding, add a dated `## Revisions` entry at the bottom linking to the triggering decision. Only for claim/interpretation/confidence changes — not for wording or organization edits. The git diff shows what changed; the revision note says *why*. Commits touching `research/` or `decisions/` need a non-empty body naming the concept affected.

**Cross-repo:** Cross-repo decisions live canonically in one repo (usually the repo where the evidence lives). Affected repos get a one-line stub: `See [repo]/decisions/YYYY-MM-DD-slug.md`.

## Research & Docs Index

Files the agent should consult before acting. Start with the current-state files, then drill down.

### Core State

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-current-position.md` | Synthesized position, established vs open claims | Answering "what do we know?", updating summaries |
| `research/iq-sex-differences-claim-register.md` | Claim ledger with status, confidence, falsifiers | Making/revising strong claims |
| `research/iq-sex-differences-decisive-causal-tree.md` | Causal tree: live nodes, open nodes, killing analyses | Proposing causal stories, prioritizing DOE |
| `research/iq-sex-differences-master-dag.md` | ASCII DAG: background → scores → school → adult → outcomes | Asking "what causes what?", checking control validity |
| `research/iq-sex-differences-node-table.md` | Node-by-node DAG table with proxies and coefficients | Checking which nodes have estimates |
| `research/iq-sex-differences-master-plan.md` | End-to-end roadmap with stages and completion criteria | Planning remaining project |
| `research/iq-sex-differences-execution-plan.md` | Ordered work plan with estimands and stop rules | Choosing next tranche |
| `research/iq-sex-differences-analysis-protocol.md` | Frozen estimands, score rules, weights, covariates | Running models, comparing datasets |
| `research/iq-sex-differences-doe.md` | Full staged research program and decision thresholds | Planning new analyses or dataset acquisition |

### Strategy & Novelty

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-novel-synthesis-roadmap.md` | Strongest defensible claims, paper-shaped directions | Reframing contribution, choosing next design |
| `research/iq-sex-differences-novelty-audit.md` | Literature-backed audit: known vs distinct | Making novelty claims |
| `research/iq-sex-differences-alpha-research-program.md` | Where genuine alpha remains, next designs with info value | Planning next research tranche |
| `research/iq-sex-differences-alpha-master-plan.md` | Full alpha execution plan with estimands and stop rules | Choosing what runs first vs parallel |
| `research/iq-sex-differences-next-level-research-plan.md` | Higher-leverage work beyond public observational frontier | Choosing between more datasets vs new designs |
| `research/iq-sex-differences-causal-methods-frontier.md` | Which newer causal machinery helps here and which does not | Proposing proximal/transport/hidden-mediator upgrades |
| `research/iq-sex-differences-frontier-literature-audit.md` | 2023-2025 literature audit | Checking if synthesis is genuinely new |
| `research/iq-sex-differences-frontier-refresh-2026-03-06.md` | Latest literature refresh confirming integration novelty | Checking whether findings are already established |
| `research/iq-sex-differences-model-review-2026-03-06.md` | Cross-model blind-spot review (Gemini + GPT) | Reusing external critique, softening claims |

### Battery & Measurement

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-battery-design-matrix.md` | Battery-family matrix: time limits, speed, adaptive behavior | Checking whether a battery is speeded vs power |
| `research/iq-sex-differences-raven-open-data.md` | Public Raven raw-data status vs local ICAR follow-up | Claiming public Raven data are in hand |
| `research/iq-sex-differences-matrix-certainty-plan.md` | Certainty ladder for matrix/Raven branch | Getting more certainty on matrix branch |
| `research/iq-sex-differences-open-matrix-assets.md` | Usable open matrix assets: ICAR, MaRs-IB, OMIB | Checking what matrix data is available now |
| `research/iq-sex-differences-matrix-experiment-protocol.md` | Smallest randomized matrix-study design using OMIB | Moving from observational to experimental |
| `research/iq-sex-differences-matrix-experiment-deployment.md` | Deployable OMIB pilot run path and checklist | Actually fielding the OMIB timing pilot |
| `research/iq-sex-differences-matrix-experiment-runbook.md` | Operational deployment guide for OMIB pilot | Ready-to-run experiment checklist |
| `research/iq-sex-differences-marsib-request-draft.md` | Ready-to-send MaRs-IB data request | Requesting non-public MaRs-IB data |
| `research/iq-sex-differences-timing-channels.md` | Processing speed and timing design rationale | Challenging claims about female-friendly speed correction |
| `research/iq-sex-differences-item-face-validity-audit.md` | Released PISA/ASVAB item inspection | Making claims about "biased items" |

### PISA 2018 Measurement Branch

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-pisa2018-item-split.md` | Item/process pass: broad male-leaning math, heterogeneous items | School-age process burden vs item-family heterogeneity |
| `research/iq-sex-differences-pisa2018-framework-proxy.md` | Content/context decomposition by framework family | School-age split coherence by content family |
| `research/iq-sex-differences-pisa2018-dif-proxy.md` | First ability-conditioned item-fairness pass | School-age item fairness, `space_shape` conditioning |
| `research/iq-sex-differences-pisa2018-dif-leaveout.md` | Contamination-aware leave-out matching follow-up | Current best PISA conditioning result |
| `research/iq-sex-differences-pisa2018-dif-iterative.md` | Iterative purification: what survives anchor updating | Whether family ordering is anchor artifact |
| `research/iq-sex-differences-pisa2018-dif-logit.md` | Binary-response weighted binomial confirmation | Whether ordering is linear-model artifact |
| `research/iq-sex-differences-pisa2018-dif-rasch.md` | Anchored-Rasch with separate male/female calibration | Strongest latent-item sensitivity pre-IRT |
| `research/iq-sex-differences-pisa2018-dif-theta-logit.md` | Latent-anchor DIF conditioned on Rasch theta | Whether ordering is constructed-score artifact |
| `research/iq-sex-differences-pisa2018-dif-2pl-anchor.md` | 2PL anchor sensitivity — branch saturated | Whether stronger 2PL bought new certainty |
| `research/iq-sex-differences-pisa2018-dif-purified.md` | Fixed-anchor purified pass from low-DIF anchor core | Whether ordering survives anchor rescoring |
| `research/iq-sex-differences-pisa2018-process-nuisance.md` | Process-style nuisance prototype (time/visit/count) | Whether simple process style explains residual |
| `research/iq-sex-differences-pisa2018-process-residualized-dif.md` | Strongest process-DIF reduction with residualized TT/V | Whether public process branch has headroom |
| `research/iq-sex-differences-pisa2018-time-dif-pilot.md` | Response-time DIF pilot: broad female-slower timing | Whether timing explains the score pattern |
| `research/iq-sex-differences-pisa2018-time-dif-theta.md` | Theta-conditioned timing pass with latent anchor | Whether timing is broad vs family-localized |
| `research/iq-sex-differences-pisa-frontier-comparison.md` | Comparison with older PISA 2003 Rasch literature | Whether current PISA result is novel |
| `research/iq-sex-differences-irt-tooling-feasibility.md` | Local environment IRT feasibility | Whether "run full IRT next" is executable |
| `research/iq-sex-differences-timss-public-item-wall.md` | Why public TIMSS files block item-level DIF | Whether TIMSS item-level pass is feasible |
| `research/iq-sex-differences-timss-cognitive-split.md` | TIMSS knowing/applying/reasoning split | Whether NLSY97 wedge generalizes across batteries |
| `research/iq-sex-differences-timss-frontier.md` | TIMSS 2019/2015 Advanced grade surfaces and tracking | International school-age math comparisons |

### Early-School / Child Branch

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-early-school-intake.md` | Early-school node intake: NLSCYA → ECLS-K:2011 → ECLS-K | Starting Stage 2 |
| `research/iq-sex-differences-nlscya-early-school-first-pass.md` | NLSCYA: PIAT Math, reading, PPVT | Whether early-school is locally resolved |
| `research/iq-sex-differences-eclsk2011-early-school-first-pass.md` | ECLS-K:2011: near-parity K, male widening by 1st/2nd | Whether early-school emergence is real |
| `research/iq-sex-differences-eclsk-early-school-first-pass.md` | Older ECLS-K: school-entry math already modestly male | Whether two ECLS cohorts align |
| `research/iq-sex-differences-early-school-ach.md` | ACH on NLSCYA vs ECLS disagreement | Whether disagreement is score-family vs cohort |
| `research/iq-sex-differences-early-school-score-alignment.md` | Bridge pass: NLSCYA anomaly collapses directionally | Whether early-school conflict is real |
| `research/iq-sex-differences-early-school-age-matched-alignment.md` | Age-matched bridge: sign conflict gone, magnitude differs | Whether child branch is directionally resolved |
| `research/iq-sex-differences-child-bridge-multi-anchor.md` | Multi-anchor bridge: PSID CDS male-leaning, PPVT exception | Whether bridge is reading-only |
| `research/iq-sex-differences-child-bridge-rank-sensitivity.md` | Rank-based sensitivity: same ordering after percentile rank | Whether child bridge is raw-scale artifact |
| `research/iq-sex-differences-psid-cds-first-pass.md` | PSID CDS cleaned family-linked child panel | Making PSID child claims |
| `research/iq-sex-differences-psid-cds-behavior-pass.md` | PSID CDS caregiver-rated behavior block | Whether behavior explains early-school bridge |
| `research/iq-sex-differences-psid-cds-teacher-pass.md` | PSID CDS teacher behavior/competence/math-reading ratings | Whether teacher reports dissolve child bridge |
| `research/iq-sex-differences-psid-cds-mtmm-prototype.md` | Child MTMM prototype with teacher-rating method structure | Whether child branch has formal latent support |
| `research/iq-sex-differences-public-child-branch-ach.md` | Competing-hypotheses closure for public child branch | Whether public child branch is still open |
| `research/iq-sex-differences-next-public-causal-step.md` | Best remaining public-data causal design (PSID CDS sibling FE) | Choosing next public-data analysis |

### Late-School / Wedge Branch

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-next-node-validation.md` | Why NLSY97 quantitative anomaly is the active fork | Choosing next causal node |
| `research/iq-sex-differences-nlsy97-stage-a.md` | Best internal evidence on NLSY97 process/precision | Whether raw NLSY97 female edge is real |
| `research/iq-sex-differences-nlsy97-piat-cat-pass.md` | PIAT Math vs CAT-ASVAB: where the anomaly lives | Whether NLSY97 is broad QA vs Math Knowledge |
| `research/iq-sex-differences-nlsy97-transcript-deep-pass.md` | Wedge survives PIAT, design, exposure, school-offer controls | Whether anomaly is alive after transcript unpacking |
| `research/iq-sex-differences-nlsy97-course-dag-robustness.md` | Late-school DAG and sensemakr sensitivity | Proposing new late-school regressions |
| `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md` | Behavior/compliance/climate blocks don't explain MK wedge | Whether behavior explains NLSY97 anomaly |
| `research/iq-sex-differences-evaluation-placement-node.md` | Grade-test wedge and why grades aren't clean ability proxies | Using grades/honors/placement in causal models |
| `research/iq-sex-differences-hsls-wedge-first-pass.md` | First HSLS:09 grade-test wedge confirmation | Replicating wedge beyond NLSY |
| `research/iq-sex-differences-hsls-wedge-refinement.md` | HSLS mechanism refinement: school-process block doesn't compress | Whether HSLS wedge is shallow process artifact |
| `research/iq-sex-differences-els-wedge-first-pass.md` | ELS replication: tested math male, evaluation female | Whether wedge survives outside HSLS |
| `research/iq-sex-differences-nels-wedge-first-pass.md` | NELS replication: older cohort, evaluation still female | Whether wedge is newer-cohort-specific |
| `research/iq-sex-differences-school-wedge-synthesis.md` | Cross-cohort synthesis: NLSY97, HSLS, ELS, NELS | What the late-school wedge consists of |
| `research/iq-sex-differences-school-wedge-extended-synthesis.md` | Extended synthesis adding Add Health and PSID TAS | Whether wedge survives beyond NCES cohorts |
| `research/iq-sex-differences-school-wedge-mechanism-triage.md` | Cross-cohort mechanism triage: behavior/identity blocks insufficient | Whether wedge is explained by measured mechanisms |

### Latent-Family / MTMM Branch

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-mtmm-crosswalk.md` | Trait/method crosswalk mapping datasets to MTMM workstreams | Starting latent-family branch |
| `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md` | HSLS: tested and evaluation math are not one factor | Whether late-school wedge has formal latent support |
| `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md` | Add Health: evaluation factor coherent, prediction mixed | Whether evaluation family is real beyond HSLS |
| `research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md` | Add Health evaluation measurement and prediction invariance pilot | Testing evaluation factor coherence, latent vs surface models |
| `research/iq-sex-differences-weighted-mtmm-sensitivity.md` | Weighted sensitivity: HSLS/Add Health split survives weighting | Whether latent branch is unweighted artifact |
| `research/iq-sex-differences-measurement-error-pilot.md` | Lightweight EIV: high reliability, modest geometry changes | Whether attenuation correction generates major new result |

### Transition / Outcome Branch

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-psid-tas-transition-first-pass.md` | PSID TAS: GPA, SAT/ACT, wedges, within-family | Making PSID transition claims |
| `research/iq-sex-differences-addhealth-school-surface-first-pass.md` | Add Health: grades, attainment, grade-to-attainment models | What Add Health adds to the story |
| `research/iq-sex-differences-addhealth-public-pair-note.md` | Add Health public within-family: no clean pair ID | Proposing public within-family Add Health |
| `research/iq-sex-differences-ffcws-achievement-first-pass.md` | FFCWS: anchor-sensitive child math, female college residual | What FFCWS adds to child/transition branches |
| `research/iq-sex-differences-school-outcome-decomposition.md` | Outcome decomposition: school surfaces partial, child battery weak | Whether public outcome branch adds life-course split |
| `research/iq-sex-differences-school-outcome-interactions.md` | Predictive-validity interactions: grade slopes not weaker for girls | Whether female school surfaces are inflated |
| `research/iq-sex-differences-mediator-design.md` | Frozen DAG-valid mediator design for outcome branch | Using "mediation" or "direct effect" language |

### Datasets & Access

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-dataset-expansion.md` | Dataset access status: staged, partial, metadata-only, gated | Planning acquisition, checking what's local |
| `research/iq-sex-differences-dataset-cards.md` | Detailed local dataset field mappings and variable availability | Checking exact variables available per dataset |
| `research/iq-sex-differences-dataset-roadmap.md` | Complete dataset status including access and analysis progress | Planning acquisition order |
| `research/iq-sex-differences-additional-datasets.md` | Pre-PSID prospect datasets beyond current stack | Considering new acquisition targets |
| `research/iq-sex-differences-remaining-dataset-frontier.md` | Ranked remaining datasets with access status by causal node | Deciding what to acquire next |
| `research/iq-sex-differences-access-playbook.md` | Live access states for external frontier | Whether acquisition is credentials vs licensing |
| `research/iq-sex-differences-nces-datalab-acquisition.md` | NCES API path, landed HSLS/ELS/NELS, HS&B failure | Touching NCES data acquisition |

### Restricted Data (Add Health / AHAA)

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-restricted-data-plan.md` | Restricted-data frontier: Add Health best path, NCES paused | Planning restricted-data acquisition |
| `research/iq-sex-differences-addhealth-ahaa-application-scope.md` | Add Health/AHAA request scope and project language | Starting the Add Health request |
| `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md` | File-level AHAA crosswalk: official names → DAG priorities | Filling Attachment B |
| `research/iq-sex-differences-addhealth-contract-checklist.md` | Filing checklist: portal steps, IRB, security | Actually filing the request |
| `research/iq-sex-differences-addhealth-attachment-b-draft.md` | Copy-ready Attachment B language | Filling the portal form |
| `research/iq-sex-differences-addhealth-portal-fill-guide.md` | Field-by-field portal handoff | Opening the live portal |
| `research/iq-sex-differences-addhealth-irb-language-draft.md` | Copy-ready IRB wording for restricted Add Health | Drafting/revising IRB text |
| `research/iq-sex-differences-addhealth-ahaa-literature-gap.md` | AHAA literature-gap audit: repo decomposition still distinct | Whether AHAA branch creates new information |
| `research/addhealth_ahaa_submission_packet/README.md` | Submission-ready handoff folder | Filing the Add Health request |

### Adult / Historical

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-piaac-frontier.md` | Adult numeracy by country and education | Education-stratified adult numeracy |
| `research/iq-sex-differences-piaac-age-occupation.md` | Adult numeracy by age band and occupation | Whether age/occupation creates vs amplifies gap |
| `research/iq-sex-differences-second-pass-results.md` | [current] NLSY79 same-sample schooling pass | Schooling/practice attenuation in within-family design |
| `research/iq-sex-differences-first-pass-results.md` | [historical] initial NLSY79 pass | Recovering earlier assumptions |
| `research/iq-sex-differences-nlsy97-replication.md` | [historical] raw cohort replication before Stage A | Pre-process view of NLSY97 anomaly |
| `research/iq-sex-differences-verification.md` | Literature audit of repo conclusions | Literature claims about `g`, variability, domains |
| `research/iq-sex-differences-causal-graph.md` | Outside narratives and harden/soften nodes | Mapping Taleb/Cremieux/Gwern/Gelman arguments |
| `research/iq-sex-differences-test-construction.md` | [historical, monolith] original long-form memo | Needing original stitched narrative |

### Experiment Designs

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-blinded-grading-audit.md` | Blinded grading/recommendation audit design | Working on school-evaluation branch |

### External Fact-Checks

| File | Topic | Consult before |
|------|-------|----------------|
| `research/jre-2460-rachel-wilson-claims.md` | 5-agent verification of 58 Wilson feminism/history claims | Historical feminism, suffrage, family economics facts |
| `research/jre-2460-claims-11-20.md` | Wilson JRE #2460 fact-check: suffrage and coverture claims | Wilson's specific historical/legal facts |
| `research/jre-2460-exa-crosscheck.md` | Cross-validation of multi-agent vs Exa verdicts | Comparing multi-agent vs external fact-check |
| `research/jiang-xueqin-prediction-scorecard.md` | Credibility audit of geopolitical commentator (~60% accuracy) | Evaluating Jiang assertions |

### Notes & Context

| File | Topic | Consult before |
|------|-------|----------------|
| `notes/iq-sex-differences-context-open-questions.md` | Outcome relevance, schooling-confounding, pop-culture spillover | Whether subtest gaps matter for outcomes |
| `research/review-1-audit.md` | Audit of external GPT review | Reusing review-1 claims |

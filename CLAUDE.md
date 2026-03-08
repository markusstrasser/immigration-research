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

| File | Topic | Consult before |
|------|-------|----------------|
| `research/iq-sex-differences-current-position.md` | Current best synthesized take, established vs open claims, next discriminating tests | Answering "what do we know now?", updating summaries, deciding what matters next |
| `research/iq-sex-differences-claim-register.md` | Claim-level ledger with status, confidence, provenance, and falsifiers | Making or revising any strong claim about sex differences, `g`, schooling, or measurement artifacts |
| `research/iq-sex-differences-decisive-causal-tree.md` | Explicit causal tree showing which nodes are already live, which remain open, and which analyses can actually kill them | Proposing new causal stories, prioritizing DOE, or deciding what would count as a decisive next result |
| `research/iq-sex-differences-master-dag.md` | One inspectable ASCII DAG for the current project, showing the upstream background nodes, score-generation layer, school-pipeline nodes, adult accumulation, and the outcome branch | Asking “what causes what?”, deciding which nodes are upstream versus downstream, or checking whether a proposed control variable is a background confounder or a descendant |
| `research/iq-sex-differences-node-table.md` | Strict node-by-node table mapping the master DAG to parents, children, observed proxies, example local coefficients, and current status | Asking which nodes actually have estimated coefficients, what the background causes mean operationally, or whether a specific part of the DAG is structural versus empirically quantified |
| `research/iq-battery-design-matrix.md` | Battery-family matrix for time limits, speed reward, adaptive/ceiling behavior, and what "exhaust items" actually means across `WAIS`, `WJ`, `SB5`, `Raven`, `CAT-ASVAB`, `CogAT`, and `PISA` | Answering whether a battery is really measuring untimed "raw talent", checking which batteries are speeded versus power-oriented, or avoiding category errors about "running out of items" |
| `research/iq-sex-differences-raven-open-data.md` | Exact status of public `Raven` raw-data recovery versus the local `ICAR` matrix-only follow-up, including what the `OSF` / supplementary routes did and did not yield | Claiming that public `Raven` raw data are already in hand, asking what open matrix-style data we can analyze ourselves, or checking whether harder matrix items are more male-leaning in the best current local open dataset |
| `research/iq-sex-differences-matrix-certainty-plan.md` | Branch-specific certainty ladder for the matrix / Raven-like question, including the DAG, why OVB robustness is secondary here, and which next studies would actually change the posterior | Answering “how do we get more certainty on the matrix branch?”, deciding whether the matrix result is saturated, or choosing between more observational slicing and a real matrix-specific design upgrade |
| `research/iq-sex-differences-open-matrix-assets.md` | Exact status of the currently usable open matrix assets, separating `ICAR`, `MaRs-IB`, and the fully recovered `OMIB` repository | Deciding whether another open matrix dataset is actually in hand, checking whether `MaRs-IB` raw rows are public, or seeing what can be used immediately for an original study |
| `research/iq-sex-differences-matrix-experiment-protocol.md` | Smallest original randomized matrix-study design that can test timing and item-design channels using the local `OMIB` assets | Moving from observational matrix claims to a direct experiment, choosing the first manipulations, or seeing how the local `OMIB` package should actually be used |
| `research/iq-sex-differences-marsib-request-draft.md` | Ready-to-send request for the non-public `MaRs-IB` participant-level data | Taking the next step once the public `MaRs-IB` archive dead-ends, or asking what exactly should be requested from the authors |
| `research/iq-sex-differences-psid-cds-behavior-pass.md` | Family-linked `PSID CDS` child behavior/compliance split showing what a common caregiver-rated behavior block does and does not explain | Asking whether generic child behavior/compliance explains the public early-school bridge, or deciding whether the next child mechanism needs school-facing rather than caregiver-facing variables |
| `research/iq-sex-differences-next-public-causal-step.md` | Highest-value remaining public-data causal design, centered on `PSID CDS` sibling fixed effects for the early-school branch | Choosing the next public-data causal analysis, deciding whether to keep working on child versus late-school nodes, or checking what would actually reduce uncertainty now |
| `research/iq-sex-differences-next-level-research-plan.md` | Ranked agenda for genuinely higher-leverage work beyond the current public observational frontier, including restricted-data upgrades, process-data rescoring, formal mediation, and original experiments | Deciding what could still produce novel insight, choosing between more datasets versus new designs, or checking whether the next step is another regression or a real identification upgrade |
| `research/iq-sex-differences-master-plan.md` | Canonical end-to-end roadmap with stage order, experiments, statistics, literature tracks, validation ladder, and completion criteria | Planning the remaining project, deciding what "solid" means, or assigning the next tranche of work |
| `research/iq-sex-differences-execution-plan.md` | Ordered work plan with stages, estimands, outputs, and stop rules | Choosing the next tranche, assigning work, or checking what "done" means before moving to the next node |
| `research/iq-sex-differences-frontier-literature-audit.md` | Audit of 2023-2025 literature showing which pieces the frontier already sees and what this repo may be integrating better | Answering whether the repo has a genuinely new synthesis, checking recent-paper updates, or aligning the causal tree to the latest literature |
| `research/iq-sex-differences-model-review-2026-03-06.md` | Cross-model blind-spot review of the current project state, including what Gemini and GPT criticism survived local scrutiny | Reusing the latest external-model critique, deciding what to soften in the canonical claims, or checking whether a proposed interpretation already failed the blind-spot review |
| `research/iq-sex-differences-early-school-intake.md` | Operational intake note for the early-school node, including why `NLSCYA` goes first, `ECLS-K:2011` second, and `ECLS-K` third | Starting Stage 2, choosing which early-school dataset to parse next, or checking whether `ECLS` is actually locally usable |
| `research/review-1-audit.md` | Audit of the external GPT review, including what was adopted vs rejected | Reusing claims from `review-1.md`, revising the `NLSY97` Stage A interpretation, or choosing the next data pass |
| `research/iq-sex-differences-evaluation-placement-node.md` | Grade-test wedge, evaluation / placement asymmetry, and why grades are not clean ability proxies | Using grades, honors, recommendations, or school-linked placement variables in causal models |
| `research/iq-sex-differences-dataset-expansion.md` | Which external datasets are actually staged, partial, metadata-only, or access-gated | Planning dataset acquisition, deciding what can be run now, or checking whether a cited dataset is local versus aspirational |
| `research/iq-sex-differences-remaining-dataset-frontier.md` | Ranked remaining external datasets after the current local stack, with current access status and which causal node each one would still attack | Deciding what to acquire next beyond the local stack, checking whether another dataset would actually reduce uncertainty, or distinguishing family panels from transcript/test linkage targets |
| `research/iq-sex-differences-access-playbook.md` | Exact live access states for the remaining external frontier, plus the now-resolved `PSID CDS/TAS` acquisition | Touching the remaining external frontier, deciding whether acquisition is blocked by credentials versus licensing, or avoiding circular scraping attempts |
| `research/iq-sex-differences-psid-cds-first-pass.md` | First cleaned public-use `PSID CDS` result, including the family-linked child panel build, hygiene fixes, weighted early-school surfaces, and within-family aligned checks | Making claims about the new `PSID` child evidence, deciding whether the child branch still lacks a family-linked panel, or checking whether `PSID` is still only an access problem |
| `research/iq-sex-differences-psid-tas-transition-first-pass.md` | First cleaned public-use `PSID TAS` transition result, including normalized GPA surfaces, `SAT/ACT` surfaces, aligned GPA-versus-tested wedges, and within-family checks | Making claims about the new `PSID` transition evidence, deciding whether the school-linked wedge extends into early-adult outcomes, or checking the 2019 weight caveat |
| `research/iq-sex-differences-addhealth-school-surface-first-pass.md` | First canonical public-use `Add Health` school-surface pass, including wave I parent-background handling, wave II grade surfaces, wave IV attainment, DAG-valid grade-to-attainment models, and robustness checks | Making claims about what `Add Health` does and does not add, checking whether the broad school-performance family replicates outside the NCES / `PSID` stack, or avoiding overreading public `Add Health` as a transcript/test adjudication dataset |
| `research/iq-sex-differences-addhealth-public-pair-note.md` | Public-file probe showing that the current local `Add Health` waves expose sibling/twin flags but no obvious recoverable pair identifier for a clean within-family design | Proposing any public within-family `Add Health` extension, deciding whether that branch is actually available now, or avoiding circular file-hunting |
| `research/iq-sex-differences-ffcws-achievement-first-pass.md` | First public `FFCWS` child/transition pass showing anchor-sensitive Year 9 math-versus-verbal geometry and a female-leaning Year 22 college-exposure residual that survives the Year 9 battery plus baseline family background | Making claims about what `FFCWS` adds to the child and transition branches, checking whether the school-linked wedge survives in a different cohort, or deciding whether anchor sensitivity is now a cross-cohort problem rather than an `NLSY` quirk |
| `research/iq-sex-differences-school-outcome-decomposition.md` | Public-use outcome decomposition showing that adolescent school/evaluation surfaces explain a meaningful but partial share of the female later-attainment edge in `Add Health`, while the observed early-childhood battery barely attenuates the later female college-years residual in `FFCWS` | Discussing whether the public outcome branch adds a real life-course split, checking why attenuation cannot be read as direct-effect identification, or deciding whether the next honest step is mediator design versus restricted transcript/process access |
| `research/iq-sex-differences-school-outcome-interactions.md` | Public-use predictive-validity interaction pass showing that `Add Health` grade slopes are not materially weaker for girls and that `FFCWS` child-score interactions are mostly negative but imprecise, with `PPVT` the only near-nonzero case | Discussing whether female school surfaces are obviously inflated and low-value, checking whether downstream returns differ by sex on the staged public cohorts, or deciding whether stronger outcome claims now require richer selective outcomes or restricted data |
| `research/iq-sex-differences-mediator-design.md` | Frozen DAG-valid mediator design for the outcome branch, separating total effects, descriptive attenuation, predictor-value checks, and what would count as identified mediation | Using the words “mediation,” “direct effect,” or “explained by” on the outcome branch, planning a new attainment model, or checking whether a proposed decomposition is structurally valid |
| `research/iq-sex-differences-restricted-data-plan.md` | Operational plan for the remaining restricted-data frontier, showing that `Add Health` restricted-use / `AHAA` is the best live path while `NCES` `HSTS` / `NAEP` routes are scientifically valuable but administratively paused | Planning restricted-data acquisition, deciding what to apply for now, or avoiding stale assumptions about the `NCES` application path |
| `research/iq-sex-differences-addhealth-ahaa-application-scope.md` | Exact `Add Health` restricted-use / `AHAA` request scope, bundle families, causal DAG target, and copy-ready project language for the application | Starting the actual `Add Health` request, deciding which transcript/curriculum files to ask for, or avoiding a bloated restricted-use application |
| `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md` | File-level `AHAA` crosswalk mapping official component names and file names (`edumsov`, `edu1`, `edutmsum`, `edugrad`, `eduocr`, `eduwgt`, etc.) onto the project DAG and request priorities | Filling `Attachment B`, checking which exact transcript/curriculum files to request, or translating conceptual transcript needs into actual `AHAA` file names |
| `research/iq-sex-differences-addhealth-contract-checklist.md` | Practical filing checklist for the `Add Health` restricted-use request, including portal steps, attachments, IRB/security requirements, and the main ways to bloat or stall the contract | Actually filing the `Add Health` request, preparing `Attachment B`, or avoiding administrative mistakes that do not show up in the science memos |
| `research/iq-sex-differences-addhealth-attachment-b-draft.md` | Copy-ready draft language for the `Add Health` restricted-use `Attachment B` data-details / justification section | Filling the portal/request form quickly, translating the scope memo into application text, or keeping the restricted-use request narrow and technically coherent |
| `research/iq-sex-differences-nces-datalab-acquisition.md` | Exact NCES `Online Codebook` API path, landed `HSLS` / `ELS` / `NELS` bundles, and the `HS&B` server failure | Touching NCES longitudinal data acquisition, deciding whether `HSLS` / `ELS` / `NELS` are truly local, or debugging the `HS&B` access path |
| `research/iq-sex-differences-analysis-protocol.md` | Frozen estimands, score rules, weights, and covariate blocks | Running models, comparing datasets, or questioning field choices |
| `research/iq-sex-differences-doe.md` | Full staged research program and decision thresholds | Planning new analyses or new dataset acquisition |
| `research/iq-sex-differences-next-node-validation.md` | Why the `NLSY97` quantitative anomaly is the active causal fork | Choosing the next causal node or evaluating the `NLSY97` sign flip |
| `research/iq-sex-differences-pisa2018-item-split.md` | First public `PISA 2018` item/process pass showing broad male-leaning math with heterogeneous item-level gaps | Discussing whether school-age disagreement is generic process burden versus item-family heterogeneity |
| `research/iq-sex-differences-pisa2018-framework-proxy.md` | Proxy content/context decomposition of `PISA 2018` units showing the current school-age item geometry by framework family | Discussing whether the school-age split is coherent by content family, or deciding what the next `PISA` hardening step should be |
| `research/iq-sex-differences-pisa2018-dif-proxy.md` | First ability-conditioned `PISA 2018` item-fairness pass, separating raw item gaps from residual content-family effects | Discussing school-age item fairness, deciding whether `space_shape` survives conditioning, or choosing between `TIMSS` porting and heavier IRT / anchor-item work |
| `research/iq-sex-differences-pisa2018-dif-leaveout.md` | Contamination-aware `PISA 2018` follow-up using focal-item and focal-family leave-out matching scores | Using the current best `PISA` conditioning result, checking whether the residual family ordering survived the blind-spot fix, or deciding whether full IRT is still worth the marginal gain |
| `research/iq-sex-differences-pisa2018-dif-iterative.md` | Iterative `PISA 2018` purification pass showing what survives repeated anchor updating rather than a one-shot fixed anchor set | Deciding whether the `PISA` residual family ordering is still just an anchor artifact, reusing the strongest current local `PISA` hardening step, or checking what remains open before full IRT |
| `research/iq-sex-differences-pisa2018-dif-logit.md` | Binary-response `PISA 2018` confirmation showing whether the same family ordering survives a weighted binomial item model with country fixed effects | Deciding whether the local `PISA` ordering is only a linear-model artifact, checking the strongest non-IRT item-model confirmation, or deciding whether the next step must now be full latent-variable psychometrics |
| `research/iq-sex-differences-pisa2018-dif-rasch.md` | Anchored-Rasch `PISA 2018` sensitivity showing whether the same family ordering survives separate male/female latent-item calibration within each country | Deciding whether the local `PISA` ordering is still just a matching-score artifact, checking the strongest current latent-item sensitivity short of weighted multi-group IRT, or judging whether the public `PISA` branch is close to saturation |
| `research/iq-sex-differences-pisa2018-dif-theta-logit.md` | Latent-anchor `PISA 2018` DIF pass showing whether the same family ordering survives once the focal item models are conditioned on a Rasch-based anchor `theta` rather than a hand-built anchor score | Deciding whether the local `PISA` ordering is still just a constructed-score artifact, checking the strongest hybrid local psychometric pass short of weighted joint IRT, or judging whether the public `PISA` branch is now saturated |
| `research/iq-sex-differences-pisa2018-time-dif-theta.md` | Theta-conditioned `PISA 2018` response-time pass showing whether the broad female-slower timing pattern survives the same latent anchor upgrade used on the score branch | Deciding whether timing still looks broad rather than family-localized under the strongest current local match surface, checking whether the process branch is still live, or judging whether the local `PISA` timing story is now saturated |
| `research/iq-sex-differences-pisa-frontier-comparison.md` | Direct comparison between the repo’s current `PISA 2018` hardening stack and older `PISA 2003` Rasch / item-family literature | Deciding whether the current `PISA` result is actually novel, checking where the repo aligns with older direct comparators, or keeping novelty claims honest on the measurement branch |
| `research/iq-sex-differences-irt-tooling-feasibility.md` | Short feasibility note on what the local environment can and cannot honestly support for weighted multi-group IRT right now | Deciding whether “run full IRT next” is actually executable here, checking why the current local branch stopped at hybrid psychometrics, or choosing between a tooling upgrade and a restricted-data pivot |
| `research/iq-sex-differences-pisa2018-dif-purified.md` | Fixed-anchor purified `PISA 2018` pass showing whether the residual content-family ordering survives when the matching score is rebuilt from a narrower low-DIF anchor core | Deciding whether the `PISA` family ordering is still alive after an anchor-based rescoring, checking whether the repo’s measurement-branch novelty is improving, or judging whether full IRT is still the next marginal gain |
| `research/iq-sex-differences-pisa2018-process-nuisance.md` | First process-style nuisance prototype on `PISA 2018`, testing whether non-focal time/visit/count style materially compresses the surviving residual family ordering after leave-out matching | Deciding whether simple process style is enough to explain the residual `PISA` family geometry, or whether the next measurement step should be a real process-data rescoring / response-time DIF pass |
| `research/iq-sex-differences-pisa2018-time-dif-pilot.md` | First same-ability response-time DIF pilot on `PISA 2018`, showing broad female-slower timing across content families but weak alignment between time geometry and the localized score-residual geometry | Deciding whether timing is the master explanation of the surviving `PISA` score pattern, or whether the score and time layers should be treated as distinct process footprints |
| `research/iq-sex-differences-nlscya-early-school-first-pass.md` | First local early-school pass showing how `PIAT Math`, reading comprehension, and `PPVT` behave in public `NLSCYA` | Discussing whether the early-school node is already locally resolved or deciding what `ECLS-K:2011` needs to replicate |
| `research/iq-sex-differences-eclsk2011-early-school-first-pass.md` | First `ECLS-K:2011` replication of the early-school node, showing near-parity kindergarten math and male widening by spring first/second grade | Discussing whether early-school emergence is real, whether `NLSCYA` generalizes, or what the older `ECLS-K` cohort must now adjudicate |
| `research/iq-sex-differences-eclsk-early-school-first-pass.md` | Older `ECLS-K` replication of the early-school node, showing broad school-entry math already modestly male and more male by spring first grade | Discussing whether the two `ECLS` cohorts align, whether `NLSCYA` is the outlier score family, or what the next early-school alignment step should be |
| `research/iq-sex-differences-early-school-ach.md` | Formal ACH and causal-check memo on the `NLSCYA` versus `ECLS` early-school anomaly | Deciding whether the live early-school disagreement is mainly score-family, sample-frame, cohort shift, or artifact |
| `research/iq-sex-differences-early-school-score-alignment.md` | First bridge pass aligning child math to same-wave reading, showing the raw `NLSCYA` anomaly mostly collapses directionally | Discussing whether the early-school conflict is real, checking the ACH prediction, or choosing the next child-score alignment step |
| `research/iq-sex-differences-early-school-age-matched-alignment.md` | Second bridge pass using explicit overlapping age windows, showing the child-level sign conflict stays gone and the remaining difference is magnitude | Discussing whether the child branch is directionally resolved, or deciding whether to stay on child alignment versus move back to the late-school transcript node |
| `research/iq-sex-differences-child-bridge-multi-anchor.md` | Multi-anchor child bridge pass showing that `PSID CDS` stays male-leaning across reading, passage, letter-word, and mean-verbal anchors while `NLSCYA` stays male under reading/mean-verbal and `PPVT` remains the unstable exception | Deciding whether the early-school bridge is still reading-only, checking whether `PPVT` overturns the child branch, or judging how much multi-anchor evidence now exists |
| `research/iq-sex-differences-child-bridge-rank-sensitivity.md` | Rank-based child bridge sensitivity pass showing the same broad ordering after percentile-rank transformation, with `PSID CDS` still male-leaning across anchors and `PPVT` still the weak exception | Deciding whether the child bridge is just a raw-scale artifact, checking whether Stage 2 is basically closed on public data, or choosing between psychometric refinement and moving back to the late-school frontier |
| `research/iq-sex-differences-item-face-validity-audit.md` | Direct inspection of released `PISA` items and official `ASVAB` sample items, separating visible construct-loading from overread claims about obvious bias | Making page-level claims about "biased items," deciding whether visible item burden matches the current content-family results, or checking whether the repo has any face-valid smoking gun |
| `research/iq-sex-differences-els-wedge-first-pass.md` | First public-use `ELS` replication showing later tested math male-leaning while school-linked track and evaluation surfaces tilt female | Checking whether the school-linked wedge survives outside `HSLS`, deciding what public `ELS` can and cannot identify, or judging whether behavior/compliance explains the external split |
| `research/iq-sex-differences-hsls-wedge-refinement.md` | First `HSLS` mechanism refinement showing that the obvious pre-follow-up homework, belonging, self-efficacy, teacher-encouragement, and math-teacher climate block does not materially compress the transcript-grade/track wedge | Checking whether the `HSLS` wedge is just a shallow school-process artifact, deciding whether the school-linked node survives a first mechanism stress test, or choosing between more local refinement and new external replication |
| `research/iq-sex-differences-nels-wedge-first-pass.md` | First public-use `NELS` replication showing later tested math male-leaning or near null while school-linked evaluation surfaces tilt female and transcript math quantity stays near neutral | Checking whether the school-linked wedge is newer-cohort-specific, deciding whether transcript quantity behaves like grades/recognition, or judging how much older-cohort `NELS` narrows the school-pipeline story |
| `research/iq-sex-differences-school-wedge-synthesis.md` | Cross-cohort late-school synthesis separating tested math, GPA/grades, evaluation, track, and transcript quantity across `NLSY97`, `HSLS`, `ELS`, and `NELS` | Discussing what the late-school wedge actually consists of, deciding which surface family replicates most cleanly, or avoiding pooled “school pipeline” rhetoric |
| `research/iq-sex-differences-school-wedge-extended-synthesis.md` | Extended school/transition synthesis adding public `Add Health` and family-linked `PSID TAS` to the late-school family map | Answering whether the wedge survives beyond transcript-rich NCES cohorts, deciding if the evaluation-versus-tested split extends into transition/adult panels, or checking whether the late-school synthesis is still just a narrow cohort artifact |
| `research/iq-sex-differences-school-wedge-mechanism-triage.md` | Cross-cohort mechanism triage showing that the obvious measured behavior / identity / climate / anchor blocks mostly move tested-math surfaces and do not eliminate the evaluation family or the `NLSY97` school-knowledge residual | Deciding whether the late-school wedge is already explained by measured behavior/exposure blocks, choosing between more local regression slicing and restricted transcript/process access, or reusing the best current causal triage on the school-pipeline node |
| `research/iq-sex-differences-timss-public-item-wall.md` | Probe note showing why the staged public `TIMSS` Grade 8 files are usable for domain summaries but not yet for item-level DIF hardening | Deciding whether a `TIMSS` item-level pass is actually feasible, avoiding fake item-DIF claims on public `TIMSS`, or checking whether the current wall is access-related versus parser-related |
| `research/iq-sex-differences-nlsy97-piat-cat-pass.md` | Same-cohort `PIAT Math` versus `CAT-ASVAB` pass showing where the `NLSY97` anomaly actually lives | Discussing whether `NLSY97` reflects broad quantitative ability, a `Math Knowledge` wedge, or a school-surface effect |
| `research/iq-sex-differences-nlsy97-course-dag-robustness.md` | Explicit late-school DAG and sensitivity pass separating the total `sex` effect from the course-exposure effect and showing why many tempting controls are structurally invalid | Proposing any new late-school regression, deciding whether a control set is admissible, or interpreting `sensemakr` / omitted-confounding results for the `NLSY97` anomaly |
| `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md` | First pre-test late-school mechanism pass showing that the available `NLSY97` behavior/compliance and climate/fairness blocks do not materially explain the female `Math Knowledge` and transcript-GPA wedge | Deciding whether homework, absence, suspension, or school-climate variables are the main internal explanation of the `NLSY97` anomaly, or whether effort should move to external replication |
| `research/iq-sex-differences-nlsy97-transcript-deep-pass.md` | First deep late-school transcript pass showing the `NLSY97` wedge survives `PIAT`, design, exposure, and school-offer controls while `Arithmetic Reasoning` stays separate | Discussing whether the late-school anomaly is still alive after transcript unpacking, or deciding whether the next node is behavior/compliance versus evaluation |
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

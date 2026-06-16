# IQ Sex Differences - Causal Methods Frontier

**Date:** 2026-03-07  
**Purpose:** determine whether newer causal methods can create real identification gains for this project, or whether they mainly add notation without solving the actual bottlenecks.

Companion files:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-alpha-master-plan.md`
- `research/iq-sex-differences-alpha-research-program.md`
- `research/iq-sex-differences-next-level-research-plan.md`
- `research/iq-sex-differences-mediator-design.md`

---

## 1. Direct Answer

No, plain `do`-calculus is not the missing ingredient here. [INFERENCE]

The main bottlenecks are:

1. measurement error and latent-score attenuation
2. cross-dataset surface mismatch
3. descendant-heavy mediator structures on the outcome branch
4. missing or weakly justified proxy structure

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-mediator-design.md`; https://meth.psychopen.eu/index.php/meth/article/view/15773; https://www.jmlr.org/papers/v24/21-0950.html]

The best modern upgrades are therefore:

1. measurement-error-aware latent causal estimation and `EIV` correction
2. joint measurement plus prediction invariance
3. interventional / stochastic mediation on **manipulable downstream nodes**, not on sex itself
4. proximal mediation or proximal-ID methods **only if** valid proxy structure can be defended
5. transportability / data fusion only if explicit source-target overlap and selection diagrams can be justified

[INFERENCE]

The wrong move would be to jump straight to “new do-calculus” language while the project still lacks either:

1. defendable proxy pairs
2. common cross-dataset latent anchors
3. a manipulable treatment decomposition

[INFERENCE]

---

## 2. Causal-Check Summary

**Observation:** the repo now has a stable multi-dataset pattern of recurring surface families, but the public observational branch is near saturation and the remaining uncertainty is mostly about measurement, mediation, and transport across partially incompatible datasets. [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-school-wedge-extended-synthesis.md`; `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`]

**Null:** one more dataset or one more descendant-heavy regression is enough; no new method class is needed. [INFERENCE]

**Residual after null:** the remaining uncertainty is mostly structural. Several modern methods could help, but only if their identifying assumptions map to the actual sex / transcript / evaluation / test-score DAG. [INFERENCE]

**Geometry:** repeated convergence across observational datasets, repeated psychometric hardening on `PISA`, and clear dependence on latent-method distinction rather than just raw mean gaps. [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-execution-plan.md`]

**Most likely cause (0.68):** the next ceiling is measurement and identification mismatch, not lack of more observational coefficients. [INFERENCE]

**Top alternative (0.22):** one restricted transcript dataset plus standard latent modeling will answer most of the remaining questions without any newer causal theory. [INFERENCE]

**Falsifier:** a recent integrated design already combining transcript strength, latent measurement correction, process-DIF reduction, and prediction invariance on the same sex-gap problem. [INFERENCE]

**Decision impact:** prioritize method classes that directly attack measurement and mediator structure. Downgrade methods that require proxy or transport assumptions the repo cannot yet defend. [INFERENCE]

---

## 3. The Actual DAG Problem

The current problem is not “estimate the causal effect of a treatment with measured confounders.” It is closer to:

```text
Sex -> latent_trait_family
Sex -> school_behavior
Sex -> school_evaluation
Sex -> transcript_strength*
Sex -> tested_surface*
Sex -> adult_outcomes

Background -> school_behavior
Background -> school_evaluation
Background -> transcript_strength*
Background -> tested_surface*
Background -> adult_outcomes

School_context -> school_evaluation
School_context -> transcript_strength*
School_context -> tested_surface*
School_context -> adult_outcomes

school_behavior -> school_evaluation
school_behavior -> tested_surface*
school_evaluation -> transcript_strength*
school_evaluation -> adult_outcomes
transcript_strength* -> adult_outcomes
tested_surface* -> adult_outcomes

U_latent -> observed_grade_indicators
U_latent -> observed_test_indicators
U_latent -> observed_process_indicators
```

`*` marks nodes that are partly latent or measured with error. [INFERENCE]

That means three separate method classes are being conflated if we are not careful:

1. latent measurement construction
2. causal identification with sequential mediators
3. cross-dataset transport or fusion

[INFERENCE]

Plain `do`-calculus helps only with `2` and `3`, and only after the measurement layer is represented honestly. [INFERENCE]

---

## 4. Ranked Methods

## 4.1 Measurement-Error-Aware Latent Causal Estimation

**Best immediate upgrade.**

### Why it matters

Recent work shows that two-step causal models using sum scores or factor-score plug-ins can yield attenuated standardized effects relative to latent-variable models, and that `EIV` correction can remove much of that bias. [SOURCE: https://meth.psychopen.eu/index.php/meth/article/view/15773]

Recent latent-predictor work makes the same point from the regressor side: latent predictors create attenuation bias, common corrections can themselves be biased, and split-sample / correlation-based correction can outperform naive practice. [SOURCE: https://arxiv.org/pdf/2507.22218]

### What it helps here

1. outcome-side attenuation in test-score and latent-family models
2. predictor-side attenuation when using composite school surfaces
3. better comparison between tested, evaluation, and transcript factors

[INFERENCE]

### Current fit to the repo

High. The repo already has:

1. `HSLS` tested versus evaluation latent-family prototypes
2. `Add Health` evaluation-factor prototypes
3. `PSID CDS` child trait-plus-method prototypes

[SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`; `research/iq-sex-differences-psid-cds-mtmm-prototype.md`]

### Main weakness

This does not solve causal identification by itself. It solves measurement attenuation first. [INFERENCE]

### Verdict

This is still the right measurement direction, but the first empirical public-data pilot says the lightweight version is modest on the current `HSLS` and `Add Health` families because reliability is already fairly high. So the real remaining gain is heavier weighted joint latent modeling or restricted transcript-theta work, not simple public `EIV` correction by itself. [SOURCE: `research/iq-sex-differences-measurement-error-pilot.md`]

The same practical lesson now holds on the public `PISA` process branch. A stronger ability-residualized non-focal `TT/V` nuisance-trait pass still does not coherently compress the residual score-family ordering. That means public `TT/V` alone are close to saturated as a process-DIF reduction surface. If the repo wants a real process-based reduction result, the next honest move is richer confidential log data or a heavier joint score-time latent model. [SOURCE: `research/iq-sex-differences-pisa2018-process-residualized-dif.md`; https://www.cambridge.org/core/services/aop-cambridge-core/content/view/69A15CC6FFB38BDCB1F9C0FBDE550A6D/S0033312325100720a.pdf/div-class-title-reducing-differential-item-functioning-via-process-data-div.pdf; https://webfs.oecd.org/pisa2018/index.html#_Toc14472]

---

## 4.2 Joint Measurement Plus Prediction Invariance

### Why it matters

Millsap explicitly emphasizes that empirical work rarely studies measurement invariance and prediction invariance together in the same high-stakes setting. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]

### What it helps here

It answers the more meaningful question:

> Is a given surface family both measuring the same thing and predicting the same thing across sex?

[INFERENCE]

### Current fit to the repo

High. The repo already has first prototypes:

1. `HSLS` tested-math versus evaluation-math split
2. `Add Health` evaluation holdout

[SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`]

### Main weakness

The current local versions are still prototypes, not weighted joint multigroup latent regressions. [SOURCE: `research/iq-sex-differences-current-position.md`]

### Verdict

This is the best second local upgrade after measurement correction. [INFERENCE]

---

## 4.3 Interventional / Stochastic Mediation On Downstream Nodes

### Why it matters

Longitudinal mediation with latent growth or multilevel structure is hard because post-treatment confounding breaks standard natural direct/indirect effect logic. Separable or related interventional effects can help in some longitudinal settings. [SOURCE: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-024-02358-4]

### Critical correction

This does **not** justify talking as if sex itself has separable effects in the strong interventionist sense. Sex is not a manipulable treatment in the way these methods usually assume. [INFERENCE]

For immutable or socially bundled characteristics like sex or race, the cleaner move is either:

1. total-effect background-adjusted descriptions
2. intervention analysis on downstream manipulable nodes
3. cue-based or component-based experiments

[SOURCE: https://www.marcellodibello.com/race-causality-discrimination/readings/Greiner-Rubin-Cause-Immutable-2010.pdf; http://www.omarwasow.com/race_causation_6_1.pdf; https://link.springer.com/content/pdf/10.1007/s11577-026-01054-z.pdf]

### What it helps here

1. interventions on evaluation rules
2. interventions on timing/format/process
3. interventions on recommendation or track-allocation mechanisms

[INFERENCE]

### Current fit to the repo

Medium, but only if reframed away from “separable effects of sex” and toward downstream policy/process interventions. [INFERENCE]

### Verdict

Useful, but only after tightening the estimand. [INFERENCE]

---

## 4.4 Proximal Mediation And Hidden-Mediator Methods

### Why it matters

Proximal mediation extends mediation analysis to settings with unmeasured confounding when valid proxy variables of the hidden confounding mechanism are available. [SOURCE: https://par.nsf.gov/servlets/purl/10428415]

Hidden-mediator work extends front-door and mediation results to settings where the mediator is unobserved but error-prone proxies are measured. [SOURCE: https://arxiv.org/pdf/2111.02927]

### What it could help here

Potentially:

1. latent transcript strength measured by course/grade proxies
2. latent evaluation measured by grades/recommendations/recognition
3. hidden school-engagement structures if genuine proxy pairs exist

[INFERENCE]

### Main assumptions

1. valid treatment-inducing and outcome-inducing proxy roles
2. relevance / completeness-type conditions
3. correct bridge-function structure or semiparametric estimation setup

[SOURCE: https://export.arxiv.org/pdf/2109.11904v2.pdf; https://www.jmlr.org/papers/v24/21-0950.html; https://arxiv.org/abs/2304.04374]

### Why this is not an automatic fit

Most candidate proxies in this repo are themselves descendants of sex or of mediators:

1. school behavior
2. grades
3. recommendations
4. transcript summaries

Those are not automatically valid proximal proxies just because they are noisy or correlated. [INFERENCE]

The 2024 automation paper on selecting proxy variables is interesting, but it is built around linear-model identifiability conditions and does not remove the need for substantive causal justification. [SOURCE: https://proceedings.mlr.press/v235/xie24b.html]

### Verdict

Promising for a restricted transcript/evaluation branch, but not yet justified on the current public stack. [INFERENCE]

---

## 4.5 Partial Identification With Proxies

### Why it matters

If completeness fails or only one proxy type is available, proximal point identification may be impossible, but proxy information can still yield bounds. [SOURCE: https://arxiv.org/abs/2304.04374]

### What it helps here

This is the right fallback if:

1. proxy structure is plausible but incomplete
2. the repo wants defensible bounds instead of brittle point estimates

[INFERENCE]

### Current fit to the repo

Low-to-medium. It becomes relevant only after the proxy map is drawn and point identification looks unjustified. [INFERENCE]

### Verdict

Not the next move, but a credible safety valve. [INFERENCE]

---

## 4.6 Transportability / Data Fusion With Proxies

### Why it matters

Transportability and data-fusion methods formalize when causal information from one environment can be transferred to another. Classical selection-diagram work comes straight out of do-calculus. [SOURCE: https://arxiv.org/abs/1503.01603; https://ftp.cs.ucla.edu/pub/stat_ser/r450-reprint.pdf]

Newer proxy-based transport work extends that logic when the target domain observes only proxies of hidden confounders. [SOURCE: https://openreview.net/forum?id=8owMKkQIy0] [PREPRINT]

### What it could help here

In principle:

1. transcript-rich source plus test-rich target
2. process-rich source plus outcome-rich target
3. combining partially overlapping cohorts without pretending they are exchangeable

[INFERENCE]

### Why it is not immediate

The repo does not yet have a clean source-target pair with:

1. the same causal query
2. explicit selection differences
3. shared bridge variables or defended proxy mappings

[INFERENCE]

Without that, transport language becomes decorative. [INFERENCE]

### Verdict

Medium-term alpha, not the best immediate analysis. [INFERENCE]

---

## 5. Research Incentives And Blind Spots

This is not about accusing individual authors of bad faith. It is about local optimization by field. [INFERENCE]

### 5.1 Psychometric fairness researchers

Strengths:

1. invariance
2. DIF
3. process-data interpretation

Blind spot:

They often stop before prediction, transcript strength, or later outcomes. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2; https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/]

### 5.2 Causal-methods researchers

Strengths:

1. formal identification
2. sharp assumptions
3. proxy / hidden-variable theory

Blind spot:

They often optimize theorems under strong proxy or transport assumptions without asking whether educational datasets actually contain defensible proxy roles. [INFERENCE]

### 5.3 Education-econ and sociology researchers

Strengths:

1. transcript pathways
2. recommendations
3. attainment consequences

Blind spot:

They often treat grades, course ladders, and test scores as if they were interchangeable or sufficiently measured without explicit latent measurement correction. [SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf; `research/iq-sex-differences-school-wedge-extended-synthesis.md`]

### 5.4 Intelligence researchers

Strengths:

1. construct-level debate
2. latent-factor arguments
3. domain-specific ability differences

Blind spot:

They usually stop before transcript, evaluation, process, and outcome integration. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-novelty-audit.md`]

---

## 6. Where The Alpha Actually Is

The alpha is not “use do-calculus because it sounds deep.” [INFERENCE]

The alpha is:

1. use measurement-error-aware latent modeling before causal decomposition
2. restrict mediation language to manipulable downstream nodes
3. use proximal methods only where the proxy structure is explicitly defended
4. use transport/data-fusion only where source-target overlap is graphically explicit

[INFERENCE]

The best distinct contribution remains:

> the sex-gap literature is better represented as a problem of recurring surface families with different causal parents than as one stable object called “IQ” or “math ability.”

[SOURCE: `research/iq-sex-differences-novel-synthesis-roadmap.md`; `research/iq-sex-differences-novelty-audit.md`]

Newer causal methods help only insofar as they sharpen one of those families without collapsing the distinction. [INFERENCE]

---

## 7. Ranked Next Moves

1. **Treat the local latent measurement-correction pilot as complete and bounded.** It already shows that simple public attenuation correction does not materially change the current `HSLS` / `Add Health` geometry. [SOURCE: `research/iq-sex-differences-measurement-error-pilot.md`]
2. **Keep building weighted joint measurement plus prediction invariance** on the strongest late-school family pair. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`]
3. **Treat the restricted `AHAA` branch as the first place where interventional mediator language becomes serious**, because transcript-strength and evaluation-residual nodes can then be separated cleanly. [SOURCE: `research/iq-sex-differences-addhealth-ahaa-application-scope.md`]
4. **Only after the proxy map is explicit**, test whether proximal mediation or hidden-mediator methods are actually admissible on a transcript/evaluation subproblem. [SOURCE: https://export.arxiv.org/pdf/2109.11904v2.pdf; https://arxiv.org/pdf/2111.02927]
5. **Use data fusion / transportability only if** source-target diagrams and common bridge variables are explicit enough to write down a non-hand-wavy transport query. [SOURCE: https://arxiv.org/abs/1503.01603; https://ftp.cs.ucla.edu/pub/stat_ser/r450-reprint.pdf; https://openreview.net/forum?id=8owMKkQIy0] [PREPRINT]

---

## 8. Bottom Line

The best answer to “is there some new do-calculus or the like that could help us?” is:

> Yes, but not in the naive way. The modern upgrades that actually fit this repo are measurement-error-aware latent modeling first, interventional mediator designs on manipulable downstream nodes second, and proximal / transport methods only where proxy and source-target assumptions are explicitly defensible.

[INFERENCE]

If the repo skips that order, it will import sophisticated causal language without reducing the real uncertainty. [INFERENCE]

## Revisions

### 2026-03-07

Refined the methods-frontier recommendation after the first empirical public measurement-error pilot. The main update is that lightweight public `EIV` correction on the current `HSLS` and `Add Health` latent-family branch moves little because reliability is already fairly high, so the real remaining gain is heavier weighted joint latent modeling or restricted transcript-theta work. See `research/iq-sex-differences-measurement-error-pilot.md`. [SOURCE: `research/iq-sex-differences-measurement-error-pilot.md`]

Refined the process-DIF recommendation after the stronger public `PISA` residualized nuisance-trait pass. The main update is that public `TT/V` alone do not coherently reduce the residual content-family ordering even after obvious ability leakage is removed, so further public process tweaks are close to saturation. See `research/iq-sex-differences-pisa2018-process-residualized-dif.md`. [SOURCE: `research/iq-sex-differences-pisa2018-process-residualized-dif.md`]

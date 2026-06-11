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
- permutation / placebo / holdout-threshold logic in `analyze_capacity_falsification.py`
- whether the new memos overstate causal confidence after the falsification pass
- whether the reasoning-evolution doc accurately reflects the actual artifact sequence

## Touched Files

### Touched Files

- `sources/immigration-causal/scripts/analyze_capacity_falsification.py`
- `research/immigration-capacity-falsification-2026-04-21.md`
- `research/immigration-reasoning-evolution-2026-04-21.md`
- `research/immigration-INDEX.md`
- `CLAUDE.md`

## Git Status

### git status --short

```text
M CLAUDE.md
 M research/immigration-INDEX.md
 M research/iq-sex-differences-claim-register.md
 M research/iq-sex-differences-current-position.md
 M research/iq-sex-differences-test-construction.md
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
?? .model-review/immigration-capacity-scope.md
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
CLAUDE.md                     | 2 +-
 research/immigration-INDEX.md | 2 ++
 2 files changed, 3 insertions(+), 1 deletion(-)
```

### Unified Diff

```diff
CLAUDE.md --- Text
118 | Topic | Prefix | Index | Files |   118 | Topic | Prefix | Index | Files |
119 |-------|--------|-------|-------|   119 |-------|--------|-------|-------|
120 | IQ sex differences | `iq-sex-diff  120 | IQ sex differences | `iq-sex-diff
... erences-*` | `research/iq-sex-diffe  ... erences-*` | `research/iq-sex-diffe
... rences-INDEX.md` | 118 |             ... rences-INDEX.md` | 118 |
121 | Immigration (fiscal/crime) | `imm  121 | Immigration (fiscal/crime) | `imm
... igration-*` | `research/immigration  ... igration-*` | `research/immigration
... -INDEX.md` | 30 |                    ... -INDEX.md` | 32 |
122                                      122 
123 New topics: create `research/<topic  123 New topics: create `research/<topic
... >-INDEX.md`, add a row here, use `<  ... >-INDEX.md`, add a row here, use `<
... topic>-*` prefix for all files.      ... topic>-*` prefix for all files.
124                                      124 

research/immigration-INDEX.md --- Text
79 79 | `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
80 80 | `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS + threshold spine: county wages, employment, native mobility, and backlash in one frame | Saying threshold effects show up in wages, employment, or native sorting |
81 81 | `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
.. 82 | `immigration-capacity-falsification-2026-04-21.md` | Permutation, placebo, leave-one-state-out, monotonicity, and holdout-threshold validation for the county capacity results | Asking which parts of the new flow-capacity story actually survive falsification |
.. 83 | `immigration-reasoning-evolution-2026-04-21.md` | Timeline of how the repo’s immigration reasoning changed, including where later falsification narrowed earlier causal confidence | Wanting the evolution of reasoning itself traced rather than only the latest stance |
82 84 
83 85 ## Raw Data & Warehouse
84 86
```

## Current File Excerpts

### sources/immigration-causal/scripts/analyze_capacity_falsification.py

```text
"""Falsification and robustness checks for the county capacity-frontier results."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

DATA = Path(__file__).parent.parent / "data"
PANEL = DATA / "outcomes" / "county_outcome_panel.parquet"
OUT_DIR = DATA / "outcomes" / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_SUMMARY = OUT_DIR / "county_capacity_falsification_summary.json"
OUT_PERM = OUT_DIR / "county_capacity_permutation_results.csv"
OUT_PLACEBO = OUT_DIR / "county_capacity_placebo_results.csv"
OUT_LOSO = OUT_DIR / "county_capacity_leave_one_state_out.csv"
OUT_THRESH = OUT_DIR / "county_capacity_threshold_validation.csv"
OUT_MONO = OUT_DIR / "county_capacity_monotonicity.csv"

RNG = np.random.default_rng(20260421)
OCCUPANTS_PER_UNIT = 2.5
PERMUTATIONS = 300
THRESHOLD_SPLITS = 60


def prepare() -> pd.DataFrame:
    df = pd.read_parquet(PANEL).copy()
    df = df.dropna(
        subset=[
            "margin_shift",
            "fb_share",
            "recent_fb_annual_share",
            "permit_units_2021_2024",
            "permit_rate_per_1k",
            "state_name",
            "log_pop",
            "annual_avg_emplvl_2021",
            "annual_avg_emplvl_2022",
            "annual_avg_emplvl_2023",
            "annual_avg_emplvl_2024",
            "annual_avg_wkly_wage_2021",
            "annual_avg_wkly_wage_2022",
            "annual_avg_wkly_wage_2023",
            "annual_avg_wkly_wage_2024",
            "net_us_migration_share_2022_23",
        ]
    ).copy()
    df = df[df["totpop"] >= 10000].copy()
    df["annual_recent_fb_persons"] = df["recent_fb_annual_share"] * df["totpop"]
    df["annual_permit_units"] = df["permit_units_2021_2024"] / 4.0
    df["annual_housing_capacity_persons"] = df["annual_permit_units"] * OCCUPANTS_PER_UNIT
    df["recent_fb_per_permit_unit"] = df["annual_recent_fb_persons"] / df["annual_permit_units"].replace(0, np.nan)
    finite = df["recent_fb_per_permit_unit"].replace([np.inf, -np.inf], np.nan).dropna()
    p99 = float(finite.quantile(0.99))
    df["recent_fb_per_permit_unit_w99"] = df["recent_fb_per_permit_unit"].clip(upper=p99)
    df["log_recent_fb_per_permit_unit_w99"] = np.log1p(df["recent_fb_per_permit_unit_w99"])

    for col in ("fb_share", "recent_fb_annual_share", "log_recent_fb_per_permit_unit_w99"):
        std = df[col].std(ddof=0)
        df[f"z_{col}"] = (df[col] - df[col].mean()) / std

    df["wage_log_change_2021_2022"] = np.log(df["annual_avg_wkly_wage_2022"] / df["annual_avg_wkly_wage_2021"])
    df["wage_log_change_2021_2023"] = np.log(df["annual_avg_wkly_wage_2023"] / df["annual_avg_wkly_wage_2021"])
    df["wage_log_change_2023_2024"] = np.log(df["annual_avg_wkly_wage_2024"] / df["annual_avg_wkly_wage_2023"])
    df["employment_log_change_2021_2022"] = np.log(df["annual_avg_emplvl_2022"] / df["annual_avg_emplvl_2021"])
    df["employment_log_change_2021_2023"] = np.log(df["annual_avg_emplvl_2023"] / df["annual_avg_emplvl_2021"])
    df["employment_log_change_2023_2024"] = np.log(df["annual_avg_emplvl_2024"] / df["annual_avg_emplvl_2023"])
    df["wage_acceleration_2023_2024_vs_2021_2022"] = df["wage_log_change_2023_2024"] - df["wage_log_change_2021_2022"]
    df["employment_acceleration_2023_2024_vs_2021_2022"] = df["employment_log_change_2023_2024"] - df["employment_log_change_2021_2022"]
    return df


def fit_term(df: pd.DataFrame, outcome: str, term: str, formula: str) -> dict[str, float]:
    model = smf.ols(formula.format(outcome=outcome), data=df).fit(cov_type="HC3")
    return {
        "beta": float(model.params.get(term, np.nan)),
        "t_stat": float(model.tvalues.get(term, np.nan)),
        "p_value": float(model.pvalues.get(term, np.nan)),
        "adj_r2": float(model.rsquared_adj),
        "n": int(model.nobs),
    }


def permutation_check(df: pd.DataFrame) -> pd.DataFra

... [truncated for review packet] ...

lope = np.polyfit(agg["load_decile"], agg[col], 1)[0]
        rows.append({"series": col, "spearman_rho": float(rho), "spearman_p": float(pval), "decile_linear_slope_pp": float(slope)})
    out = pd.DataFrame(rows)
    out.to_csv(OUT_MONO, index=False)
    return out


def build_summary(
    perm: pd.DataFrame,
    placebo: pd.DataFrame,
    pretrend_adj: pd.DataFrame,
    loso: pd.DataFrame,
    thresh: pd.DataFrame,
    mono: pd.DataFrame,
) -> dict[str, object]:
    def pick_perm(outcome: str) -> dict[str, float]:
        row = perm[perm["outcome"] == outcome].iloc[0]
        return row.to_dict()

    def pick_placebo(window: str) -> dict[str, float]:
        row = placebo[placebo["outcome_window"] == window].iloc[0]
        return row.to_dict()

    def loso_summary(outcome: str) -> dict[str, float | str]:
        sub = loso[loso["outcome"] == outcome].copy()
        worst = sub.loc[sub["t_stat"].abs().idxmin()]
        return {
            "min_abs_t": float(sub["t_stat"].abs().min()),
            "median_abs_t": float(sub["t_stat"].abs().median()),
            "max_abs_t": float(sub["t_stat"].abs().max()),
            "worst_state": str(worst["left_out_state"]),
            "worst_state_t": float(worst["t_stat"]),
            "worst_state_beta": float(worst["beta"]),
        }

    thresh_summary = (
        thresh.groupby("outcome", observed=True)
        .agg(
            splits=("split", "count"),
            median_test_beta=("test_beta", "median"),
            median_test_t=("test_t", "median"),
            share_test_p_lt_005=("test_p", lambda x: float((x < 0.05).mean())),
            share_same_sign=("test_beta", lambda x: float((np.sign(x) == np.sign(x.median())).mean())),
            modal_recent_quantile=("selected_recent_quantile", lambda x: int(pd.Series(x).mode().iloc[0])),
            modal_permit_quantile=("selected_permit_quantile", lambda x: int(pd.Series(x).mode().iloc[0])),
        )
        .reset_index()
    )

    return {
        "permutation": {
            "margin_shift": pick_perm("margin_shift"),
            "wkly_wage_log_change": pick_perm("wkly_wage_log_change"),
            "employment_log_change": pick_perm("employment_log_change"),
            "net_us_migration_share": pick_perm("net_us_migration_share"),
        },
        "placebo_windows": {
            "wage_2021_2022": pick_placebo("wage_2021_2022"),
            "wage_2021_2023": pick_placebo("wage_2021_2023"),
            "wage_2023_2024": pick_placebo("wage_2023_2024"),
            "wage_accel_2324_vs_2122": pick_placebo("wage_accel_2324_vs_2122"),
            "employment_2021_2022": pick_placebo("employment_2021_2022"),
            "employment_2021_2023": pick_placebo("employment_2021_2023"),
            "employment_2023_2024": pick_placebo("employment_2023_2024"),
            "employment_accel_2324_vs_2122": pick_placebo("employment_accel_2324_vs_2122"),
        },
        "post_with_pretrend_control": pretrend_adj.to_dict(orient="records"),
        "leave_one_state_out": {
            "margin": loso_summary("margin"),
            "wage": loso_summary("wage"),
            "employment": loso_summary("employment"),
            "net_migration": loso_summary("net_migration"),
        },
        "threshold_validation": thresh_summary.to_dict(orient="records"),
        "monotonicity": mono.to_dict(orient="records"),
    }


def main() -> int:
    df = prepare()
    perm = permutation_check(df)
    placebo = placebo_check(df)
    pretrend_adj = post_with_pretrend(df)
    loso = leave_one_state_out(df)
    thresh = threshold_validation(df)
    mono = monotonicity(df)
    summary = build_summary(perm, placebo, pretrend_adj, loso, thresh, mono)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT_SUMMARY}, {OUT_PERM}, {OUT_PLACEBO}, {OUT_LOSO}, {OUT_THRESH}, and {OUT_MONO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### research/immigration-capacity-falsification-2026-04-21.md

```text
# Immigration capacity falsification pass — 2026-04-21

**Question:** After the capacity-frontier pass, what survives real falsification pressure, and what has to be narrowed?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior memo found that `flow relative to local build capacity` was a stronger county stress object than generic immigrant share for wages, employment, and native sorting. This pass tests whether that is random, state-specific, overfit, or spuriously post-hoc. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]

## Bottom line

1. The `load-capacity` result is **not random noise**. It survives within-state permutation tests, leave-one-state-out checks, and strong monotonicity tests. [DATA]
2. The result is **not just Texas or one border artifact**. Leaving out Texas weakens some `t` statistics but does not flip the sign. [DATA]
3. The threshold family is **real but not knife-edge**. Holdout validation repeatedly re-selects roughly the `q80 recent-flow x q50 permit` family, but out-of-sample significance is only moderate. [DATA]
4. The strongest causal reading does **not** survive intact. High-load counties were already on weaker wage and employment paths in earlier windows, and the `2023–2024 minus 2021–2022` acceleration terms are basically null. [DATA]
5. The right upgraded claim is:
   - `flow/capacity` is a robust stress marker
   - it likely matters causally as an amplifier
   - the current county design does **not** isolate a clean post-surge break by itself [INFERENCE]

## New artifacts

1. [analyze_capacity_falsification.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/analyze_capacity_falsification.py)
2. [county_capacity_falsification_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json)
3. [county_capacity_permutation_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv)
4. [county_capacity_placebo_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_placebo_results.csv)
5. [county_capacity_leave_one_state_out.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_leave_one_state_out.csv)
6. [county_capacity_threshold_validation.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv)
7. [county_capacity_monotonicity.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | The county `load-capacity` signal is much stronger than a random within-state reassignment | All four key outcomes beat 300 within-state permutations with empirical `p≈0.0033` | HIGH | [county_capacity_permutation_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv) | VERIFIED |
| 2 | The sign is not driven by a single state | Leave-one-state-out keeps the sign for margin, wages, employment, and net migration; worst-case `|t|` remains material | HIGH | [county_capacity_leave_one_state_out.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_leave_one_state_out.csv) | VERIFIED |
| 3 | Decile monotonicity is real, not a binning accident | Spearman trends are strong and correctly signed across the deciles for all four outcomes | HIGH | [county_capacity_monotonicity.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv) | VERIFIED |
| 4 | The broad `q80 flow x q50 permit` threshold family generalizes better than a single exact cutoff | Repeated split-sample threshold search

... [truncated for review packet] ...

 3) Monotonicity: the gradient is real

Across load-capacity deciles:

1. `margin shift`: Spearman `rho≈+0.83`, `p≈0.0029` [DATA]
2. `wage growth`: `rho≈-0.93`, `p≈0.00011` [DATA]
3. `employment growth`: `rho≈-0.96`, `p≈7.3e-06` [DATA]
4. `net migration`: `rho≈-1.00`, effectively exact monotonic decline [DATA]

That is stronger than a single binary threshold. It says:

1. the county stress object behaves like a gradient, not just a yes/no threshold [INFERENCE]

## 4) Threshold validation: real family, weak knife-edge claim

Repeated split-sample threshold search does not choose one perfect breakpoint every time. But it does keep returning the same neighborhood:

1. modal `recent-flow` quantile: `80`
2. modal `permit` quantile: `50`

Holdout behavior:

1. `wage`: same sign in about `98%` of splits; `p<0.05` in about `35%` [DATA]
2. `margin`: same sign in about `88%` of splits; `p<0.05` in about `20%` [DATA]
3. `employment`: same sign in about `95%` of splits; `p<0.05` in about `12%` [DATA]

This supports:

1. `real threshold family`

It does **not** support:

1. `we know the exact breakpoint`
2. `the holdout evidence is overwhelmingly sharp`

## 5) Placebos and pre-trends: the strongest causal claim weakens

This is the most important correction.

The load-capacity variable already predicts weaker earlier windows:

1. `wage 2021–2022`: negative, `p≈0.026` [DATA]
2. `wage 2021–2023`: negative, `p≈0.0027` [DATA]
3. `employment 2021–2022`: negative, `p≈6.6e-05` [DATA]
4. `employment 2021–2023`: negative, `p≈5.7e-07` [DATA]

So the high-load counties were already structurally weaker before the full post-surge period. That means the county panel alone cannot support the strongest version of:

1. `surge caused the whole observed gap`

### Acceleration test

The cleanest acceleration check is:

`(2023–2024 change) - (2021–2022 change)`

Results:

1. `wage acceleration`: near zero, `p≈0.923` [DATA]
2. `employment acceleration`: near zero, `p≈0.582` [DATA]

This is the main reason to narrow the claim.

### Post-period with pre-trend control

If you control the `2021–2022` pre-trend and ask whether `load-capacity` still predicts the `2023–2024` outcome:

1. `wage post with pre-trend control`: negative, `p≈0.020` [DATA]
2. `employment post with pre-trend control`: negative, `p≈2.8e-06` [DATA]

So the post-period effect does not disappear entirely. But it is no longer honest to present this as a clean acceleration story. [INFERENCE]

## What now survives

1. `flow relative to local build capacity` is a robust county stress marker [DATA]
2. it is not random, not a one-state artifact, and not a binning accident [DATA]
3. it aligns strongly with wages, employment, native out-migration, and politics in the expected directions [DATA]

## What now fails

1. `We found a clean post-surge causal threshold from the county panel alone.`  
This is too strong. The pre-trend evidence cuts against it. [DATA]

2. `The threshold is a single sharp breakpoint.`  
Too strong. The holdout search supports a family of thresholds rather than one exact line. [DATA]

## Best current formulation

The strongest defensible version is:

1. `flow/capacity is a robust and highly structured stress marker`
2. `it likely operates as a real amplifier of local strain`
3. `the county panel does not yet isolate how much of that is a surge-specific break versus preexisting county weakness`

That means the next real identification move should be:

1. receiver-city shelter synthetic controls on national `CoC` data
2. not one more overfit county breakpoint regression

## Implication for the repo stance

The repo's best current position should now be:

1. `descriptive confidence`: high
2. `causal confidence on pure surge acceleration`: moderate to low
3. `policy relevance`: still high, because the risk marker is strong even if the full causal partition is unresolved

That is stricter than the intermediate capacity-frontier read, and it is the correct tightening.
```

### research/immigration-reasoning-evolution-2026-04-21.md

```text
# Immigration reasoning evolution — 2026-04-21

**Purpose:** Record how the repo's reasoning changed across the recent immigration cycle so later work can distinguish `new evidence`, `new framing discipline`, and `claims we had to narrow after falsification`.

## Starting point

The broad live question was initially easy to answer badly:

1. `open borders create huge gains`
2. `immigration hurts locals`
3. `economists disagree`

Those were too scalar.

The actual evolution was toward:

`which ledger, for whom, through which capacity constraint, under what scale?`

## Phase 1: break the scalar frame

### Prior loose intuition

The older open-borders literature made it too easy to slide from:

1. `migrant gains are huge`
2. `aggregate output rises`

to:

1. `immigration is good overall`

### What changed

The first durable correction was the `incidence split`:

1. `global ledger`
2. `national aggregate ledger`
3. `destination per-capita ledger`
4. `native-local ledger`

Artifacts:

1. [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](/Users/alien/Projects/research/research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md)
2. [immigration-claims-matrix-2026-04-11.md](/Users/alien/Projects/research/research/immigration-claims-matrix-2026-04-11.md)

### Reasoning update

The repo stopped asking:

1. `is immigration good or bad?`

and started asking:

1. `who gains?`
2. `who pays?`
3. `at what level of aggregation?`

## Phase 2: the open-borders headline gets narrowed

### Prior loose intuition

The classic line was:

1. `freer migration might double world GDP`

### What changed

Reading the actual papers and cross-checking against local capacity work showed:

1. `large global gains` survive
2. `realistic doubling` does not
3. the strongest papers are upper-bound or stylized
4. the key omitted channels are housing, congestion, politics, and destination capacity

Artifact:

1. [immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md](/Users/alien/Projects/research/research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md)

### Reasoning update

The repo moved from:

1. `huge gains therefore broadly decisive`

to:

1. `global gains are plausible at bounded margins`
2. `the strongest headline claims rely on heroic destination-capacity assumptions`

## Phase 3: the surge changes what counts as relevant evidence

### Prior loose intuition

A lot of the older U.S. literature was still Card-vs-Borjas style marginal variation:

1. small labor shocks
2. older local labor-market designs
3. weak wage effects

### What changed

The `2021–2024` surge showed that the relevant regime can shift:

1. receiver cities hit shelter and budget thresholds
2. county politics moved sharply in surge-exposed places
3. older marginal-policy findings did not settle large-flow, concentrated-arrival questions

Artifact:

1. [immigration-causal-surge-2021-2024.md](/Users/alien/Projects/research/research/immigration-causal-surge-2021-2024.md)

### Reasoning update

The repo moved from:

1. `small average wage effects likely settle the story`

to:

1. `surge and threshold regimes need separate treatment`

## Phase 4: threshold reasoning starts with capacity, not stock

### Prior loose intuition

The obvious threshold candidate was:

1. `foreign-born share crosses X`

### What changed

The first joined threshold pass and lever pass showed:

1. `permit throughput` matters more than generic stock share for labor stress
2. `rent burden` matters for native sorting
3. `shelter saturation` matters in receiver nodes
4. some cities can incur large costs before a clean `ratio > 1` rule triggers

Artifacts:

1. [immigration-threshold-first-panel-2026-04-21.md](/Users/alien/Projects/research/research/immigration-threshold-first-panel-2026-04-21.md)
2. [immigration-threshold-causal-levers-2026-04-21.md](/Users/alien/Projects/research/research/immigrati

... [truncated for review packet] ...

s recent immigrant flow relative to annual build capacity`

## Phase 8: falsification narrows the causal claim

### Prior loose intuition

After the capacity-frontier pass, it would have been easy to overread the result as:

1. `we found the surge threshold`
2. `flow/capacity cleanly causes the post-surge deterioration`

### What changed

The falsification pass did five things:

1. **Permutation**
   The load-capacity result is far stronger than randomized within-state assignments. This supports `not noise`. [DATA]

2. **Leave-one-state-out**
   The sign survives leaving out every state. This supports `not a single-state artifact`. [DATA]

3. **Monotonicity**
   The decile ordering is strongly monotone for politics, wages, employment, and native migration. This supports `structured gradient`, not arbitrary binning. [DATA]

4. **Threshold holdout validation**
   The `q80 flow x q50 permit` family repeatedly reappears, but holdout significance is only moderate rather than overwhelming. This supports `real but not knife-edge`. [DATA]

5. **Placebo and pre-trend checks**
   High-load counties were already on weaker wage and employment trajectories before the full post-surge window. The acceleration terms are basically null. This weakens the strongest causal reading. [DATA]

Derived artifacts:

1. [analyze_capacity_falsification.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/analyze_capacity_falsification.py)
2. [county_capacity_falsification_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json)

### Reasoning update

This is the most important epistemic narrowing in the cycle.

The repo moved from:

1. `flow/capacity is the causal threshold`

to:

1. `flow/capacity is a robust stress marker`
2. `it likely matters causally as an amplifier`
3. `but the current county design does not fully separate surge effects from structurally weaker preexisting counties`

That is a real downgrade in causal confidence and should stay visible.

## Phase 9: what is blocked, and what is the right next counterfactual?

### Subgroup composition

The subgroup/origin warehouse cited by earlier memos is not actually rebuildable from current local repo contents alone. The core DuckDB, build scripts, and ACS raw inputs are missing. That means:

1. no valid rerun of origin/pathway/family-structure subgroup analysis right now
2. no fake precision on ethnic or pathway splits

### Receiver-city counterfactuals

The best next counterfactual design is not county labor synthetic control. It is:

1. `2018–2024` national `CoC-year` shelter synthetic controls from the HUD `PIT/HIC` files
2. separate unit-level designs for `NYC`, `Chicago`, `Denver`, `Boston`
3. `Bexar` handled separately as a border/transit case

This is stronger than trying to force synthetic controls on the short county labor panel.

## Current best position

The current repo stance should now be read as:

1. `global gains` are still possible, but only while destination capacity degradation stays bounded
2. `stock share` still matters most for broad backlash politics
3. `flow relative to capacity` is the cleaner labor, native-sorting, and stress object
4. the county evidence supports a `robust strain gradient`
5. the county evidence does **not** yet justify the strongest `post-surge causal threshold` claim
6. subgroup/pathway composition is blocked until the old warehouse or raw ACS inputs are restored
7. the best next causal design is shelter synthetic control on national `CoC` data

## Why this doc exists

Without this trace, later work could easily flatten the sequence into:

1. `we found a threshold`

That would be wrong.

What we actually found is:

1. a better stress variable
2. a more defensible incidence split
3. a stronger descriptive gradient
4. a weaker causal acceleration claim than the intermediate pass seemed to suggest

That evolution should remain visible.
```

### research/immigration-INDEX.md

```text
# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

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
| `immigration-surge-threshold-dataset-frontier-2026-04-21.md` | Dataset frontier and research designs that can actually identify surge and threshold effects | Asking what data and empirical design would settle nonlinear local-capacity questions |
| `immigration-prototype-progress.md` | Current prototype st

... [truncated for review packet] ...

----|----------------|
| `immigration-causal-synthesis-2026-04-18.md` | Cycle synthesis: Saiz × E-Verify findings, Card-vs-Borjas verdict | Saying "Borjas vs Card is unresolved" or "rent exposure is just price discovery" |
| `immigration-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS — native county inflow is 33× immigrant inflow | Treating "newcomer burden" as immigration-driven by default |
| `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
| `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS + threshold spine: county wages, employment, native mobility, and backlash in one frame | Saying threshold effects show up in wages, employment, or native sorting |
| `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
| `immigration-capacity-falsification-2026-04-21.md` | Permutation, placebo, leave-one-state-out, monotonicity, and holdout-threshold validation for the county capacity results | Asking which parts of the new flow-capacity story actually survive falsification |
| `immigration-reasoning-evolution-2026-04-21.md` | Timeline of how the repo’s immigration reasoning changed, including where later falsification narrowed earlier causal confidence | Wanting the evolution of reasoning itself traced rather than only the latest stance |

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

### CLAUDE.md

```text
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

Research & evidence:
- **research** — one-shot research with source grading
- **research-ops** — autonomous research loops, knowledge compilation, training-data diff
- **bio-verify** — bio/medical/scientific claim verification with evidence hierarchy
- **analyze** — causal/DAG/hypotheses/forensic analysis modes
- **observe** — session retrospectives, architectural patterns, supervision audits
- **review** — adversarial review (model-review, verify, close)
- **brainstorm** — divergent ideation via systematic perturbation
- **negative-space-sweep** — discover what's MISSING from an optimized system
- **de-slop** — adversarial editor for AI-generated prose patterns

Workflow & project:
- **upgrade** — full codebase audit and improvement
- **improve** — harvest findings, suggest skills, maintain quality
- **goals** — project goals and constitutional principles elicitation
- **constitution** — constitution authoring for projects
- **entity-management** — versioned knowledge management for entities
- **trending-scout** — scan for new AI/agent developments

Data acquisition:
- **data-acquisition** — probe→stage→register pattern for external da

... [truncated for review packet] ...

e** — persistent headless browser daemon
- **google-workspace** — Google Workspace automation (Drive, Sheets, Gmail, Calendar)
- **scientific-drawing** — Typst/CeTZ, TikZ, D2, Asymptote diagrams
- **modal** — Modal serverless Python cloud compute
- **llmx-guide** — llmx CLI routing and gotchas
- **model-guide** — frontier model selection and prompting

### MCP Servers (`.mcp.json`)
- **exa** — semantic web search, entity enrichment, deep research
- **research** (research-mcp) — Semantic Scholar, corpus management, claim verification, preprint surveillance
- **brave-search** — independent web index (triangulation with Exa)
- **agent-infra** — cross-project knowledge base (hook designs, agent patterns, research findings)
- **firecrawl** — web scraping and structured extraction
- **parallel** — deep web research via Parallel Task API (lite/core/ultra tiers)
- **context7** — library documentation lookup

## Structure

```
GOALS.md           — human-owned mission, strategy, success metrics (read at session start)
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

## Research Topics

Each topic has a file prefix and its own index. Read the relevant topic index when working on that topic — don't load all indexes.

| Topic | Prefix | Index | Files |
|-------|--------|-------|-------|
| IQ sex differences | `iq-sex-differences-*` | `research/iq-sex-differences-INDEX.md` | 118 |
| Immigration (fiscal/crime) | `immigration-*` | `research/immigration-INDEX.md` | 32 |

New topics: create `research/<topic>-INDEX.md`, add a row here, use `<topic>-*` prefix for all files.

**Unprefixed files:** Some older files (`jre-2460-*`, `review-1*`, `fiscal-impact-*`, `full-spectrum-costs-*`, `zion/`) predate the prefix rule. When touching them, migrate to the right topic prefix; don't create new unprefixed files.

## Cross-Topic Notes

| File | Topic | Consult before |
|------|-------|----------------|
| `notes/llm-bias-caveat.md` | LLM instrument bias on politically charged topics | Any politically sensitive analysis |
| `notes/fact-check-prompt-template.md` | Multi-agent fact-check template | Running fact-check sweeps |
| `notes/exa-answer-evaluation.md` | Exa /answer accuracy evaluation | Choosing Exa vs alternatives |

<!-- knowledge-index
generated: 2026-04-19T04:06:29Z
hash: ff7356d91502

cross_refs: decisions/.template.md, decisions/YYYY-MM-DD-slug.md, research/<topic>-INDEX.md, research/immigration-INDEX.md, research/iq-sex-differences-INDEX.md

end-knowledge-index -->
```
```

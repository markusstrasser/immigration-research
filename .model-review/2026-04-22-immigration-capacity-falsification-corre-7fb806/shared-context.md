# Model Review Context Packet

- Project: `.`
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

- Repo: `.`
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
- whether the county panel rebuild in `build_county_outcome_panel.py` correctly materializes the new `2018–2020` windows used by falsification
- permutation / placebo / holdout-threshold logic in `analyze_capacity_falsification.py`
- whether the new memos overstate causal confidence after the falsification pass
- whether the reasoning-evolution doc accurately reflects the actual artifact sequence

## Touched Files

### Touched Files

- `sources/immigration-causal/scripts/build_county_outcome_panel.py`
- `sources/immigration-causal/scripts/analyze_capacity_falsification.py`
- `sources/immigration-causal/data/qcew/ACQUIRED.md`
- `research/immigration-capacity-falsification-2026-04-21.md`
- `research/immigration-reasoning-evolution-2026-04-21.md`
- `research/immigration-INDEX.md`

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
research/immigration-INDEX.md | 2 ++
 1 file changed, 2 insertions(+)
```

### Unified Diff

```diff
research/immigration-INDEX.md --- Text
79 79 | `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
80 80 | `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS + threshold spine: county wages, employment, native mobility, and backlash in one frame | Saying threshold effects show up in wages, employment, or native sorting |
81 81 | `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
.. 82 | `immigration-capacity-falsification-2026-04-21.md` | Corrected falsification pass with true `2018–2020` QCEW pretrend windows, `1,000`-draw permutation inference, division leave-out, explicit sample accounting, and wage-threshold null benchmarking | Asking which parts of the new flow-capacity story still survive after fixing the earlier placebo bug |
.. 83 | `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction that split the wage and employment stories | Wanting the evolution of reasoning itself traced rather than only the latest stance |
82 84 
83 85 ## Raw Data & Warehouse
84 86
```

## Current File Excerpts

### sources/immigration-causal/scripts/build_county_outcome_panel.py

```text
"""Build county outcome panel by joining threshold spine to QCEW and IRS migration.

Outputs:
- data/outcomes/county_qcew_2018_2024.parquet
- data/outcomes/county_outcome_panel.parquet
"""
from __future__ import annotations

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

QCEW_OUT = OUT / "county_qcew_2018_2024.parquet"
PANEL_OUT = OUT / "county_outcome_panel.parquet"


def load_qcew_year(year: int) -> pd.DataFrame:
    path = QCEW_DIR / f"{year}_annual_singlefile.zip"
    usecols = [
        "area_fips",
        "own_code",
        "industry_code",
        "agglvl_code",
        "qtr",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
    ]
    parts: list[pd.DataFrame] = []
    for chunk in pd.read_csv(path, compression="zip", dtype=str, usecols=usecols, chunksize=500_000):
        mask = (
            (chunk["own_code"] == "0")
            & (chunk["industry_code"] == "10")
            & (chunk["agglvl_code"] == "70")
            & (chunk["qtr"] == "A")
            & (chunk["area_fips"].str.len() == 5)
            & (~chunk["area_fips"].str.endswith("000"))
        )
        sub = chunk.loc[mask, ["area_fips", "annual_avg_emplvl", "total_annual_wages", "annual_avg_wkly_wage"]].copy()
        if len(sub):
            parts.append(sub)
    df = pd.concat(parts, ignore_index=True)
    df["year"] = year
    for col in ("annual_avg_emplvl", "total_annual_wages", "annual_avg_wkly_wage"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.rename(columns={"area_fips": "fips5"})
    return df


def build_qcew_panel() -> pd.DataFrame:
    frames = [load_qcew_year(year) for year in range(2018, 2025)]
    qcew = pd.concat(frames, ignore_index=True)
    qcew = qcew.drop_duplicates(["fips5", "year"]).sort_values(["fips5", "year"]).reset_index(drop=True)
    return qcew


def load_native_inflow() -> pd.DataFrame:
    df = pd.read_csv(
        IRS_INFLOW,
        encoding="latin-1",
        dtype={"y2_statefips": str, "y2_countyfips": str, "y1_statefips": str, "y1_countyfips": str},
        usecols=["y2_statefips", "y2_countyfips", "y1_statefips", "y1_countyfips", "n1", "n2", "agi"],
    )
    df = df[(df["y1_statefips"] == "97") & (df["y1_countyfips"] == "000")].copy()
    df["fips5"] = df["y2_statefips"].str.zfill(2) + df["y2_countyfips"].str.zfill(3)
    for col in ("n1", "n2", "agi"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.rename(
        columns={
            "n1": "us_inflow_returns_2022_23",
            "n2": "us_inflow_persons_2022_23",
            "agi": "us_inflow_agi_kusd_2022_23",
        }
    )[["fips5", "us_inflow_returns_2022_23", "us_inflow_persons_2022_23", "us_inflow_agi_kusd_2022_23"]]


def load_native_outflow() -> pd.DataFrame:
    df = pd.read_csv(
        IRS_OUTFLOW,
        encoding="latin-1",
        dtype={"y1_statefips": str, "y1_countyfips": str, "y2_statefips": str, "y2_countyfips": str},
        usecols=["y1_statefips", "y1_countyfips", "y2_statefips", "y2_countyfips", "n1", "n2", "agi"],
    )
    df = df[(df["y2_statefips"] == "97") & (df["y2_countyfips"] == "000")].copy()
    df["fips5"] = df["y1_statefips"].str.zfill(2) + df["y1_countyfips"].str.zfill(3)
    for col in ("n1", "n2", "agi"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.rename(
        columns={
            "n1": "us_outflow_returns_2022_23",
            "n2": "us_outflow_persons_2022_23",
            "agi": "us_outflow_agi_kusd_2022_23",
        }
    )[["fips5", "us_outflow_returns_2022_23", "us_outflow_persons_2022_23", "us_outflow_agi_kusd_2022_23"]]


def build_panel() -> pd.DataFrame:
    elect = pd.read_parquet(THRESHOLD_PANEL)
    elect["fips5"] = elect["fips5"].astype(str).str.zfill(5)
    qcew = build_qcew_panel()
    inflow = load_native_inflow()
    outflow = load_native_outflow()

    qcew.to_parquet(QCEW_OUT, index=False)

    qcew_wide = (
        qcew.pivot(index="fips5", columns="year", values=["annual_avg_emplvl", "total_annual_wages", "annual_avg_wkly_wage"])
        .sort_index(axis=1)
    )
    qcew_wide.columns = [f"{name}_{year}" for name, year in qcew_wide.columns]
    qcew_wide = qcew_wide.reset_index()

    panel = elect.merge(qcew_wide, on="fips5", how="left").merge(inflow, on="fips5", how="left").merge(outflow, on="fips5", how="left")
    for col in (
        "us_inflow_persons_2022_23",
        "us_outflow_persons_2022_23",
        "us_inflow_returns_2022_23",
        "us_outflow_returns_2022_23",
        "us_inflow_agi_kusd_2022_23",
        "us_outflow_agi_kusd_2022_23",
    ):
        panel[col] = panel[col].fillna(0)

    panel["net_us_migration_persons_2022_23"] = panel["us_inflow_persons_2022_23"] - panel["us_outflow_persons_2022_23"]
    panel["net_us_migration_share_2022_23"] = panel["net_us_migration_persons_2022_23"] / panel["totpop"]
    panel["us_outflow_share_2022_23"] = panel["us_outflow_persons_2022_23"] / panel["totpop"]
    def add_log_change(prefix: str, base_year: int, end_year: int) -> None:
        base_col = f"annual_avg_{prefix}_{base_year}"
        end_col = f"annual_avg_{prefix}_{end_year}"
        out_col = f"qcew_{'employment' if prefix == 'emplvl' else 'wkly_wage'}_log_change_{base_year}_{end_year}"
        ratio = pd.Series(panel[end_col]).div(panel[base_col]).where(panel[base_col] > 0)
        ratio = ratio.map(lambda x: pd.NA if pd.isna(x) or x <= 0 else x)
        ratio = pd.to_numeric(ratio, errors="coerce")
        panel[out_col] = ratio.map(lambda x: None if pd.isna(x) else math.log(x))

    for base_year, end_year in (
        (2018, 2019),
        (2019, 2020),
        (2020, 2021),
        (2021, 2022),
        (2021, 2023),
        (2023, 2024),
        (2021, 2024),
    ):
        add_log_change("emplvl", base_year, end_year)
        add_log_change("wkly_wage", base_year, end_year)

    panel.to_parquet(PANEL_OUT, index=False)
    return panel


def main() -> int:
    panel = build_panel()
    print(f"Wrote {QCEW_OUT} and {PANEL_OUT}")
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
OUT_THRESH = OUT_DIR / "county_capacity_threshold_validation.csv"
OUT_THRESH_NULL = OUT_DIR / "county_capacity_threshold_null.csv"
OUT_MONO = OUT_DIR / "county_capacity_monotonicity.csv"
OUT_SAMPLE = OUT_DIR / "county_capacity_sample_accounting.json"

RNG = np.random.default_rng(20260421)
OCCUPANTS_PER_UNIT = 2.5
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


def extract_pre_surge_permits() -> pd.DataFrame:
    keep_years = {"2018", "2019", "2020"}
    with zipfile.ZipFile(BPS_ZIP) as zf:
        with zf.open("New_Master_python_2026_01.csv") as raw:
            wrapper = io.TextIOWrapper(raw, encoding="utf-8", newline="")
            reader = pd.read_csv(
                wrapper,
                usecols=["PERIOD", "LOCATION_TYPE", "YEAR", "FIPS_C

... [truncated for review packet] ...

DataFrame,
) -> dict[str, object]:
    perm_records = perm.to_dict(orient="records")
    pretrend_records = pretrend.to_dict(orient="records")
    overlap_records = overlap.to_dict(orient="records")

    geo_summary = []
    for leaveout_type in ("division", "state"):
        sub = geo[geo["leaveout_type"] == leaveout_type].copy()
        for outcome in ("margin", "wage", "employment", "net_migration"):
            out_sub = sub[sub["outcome"] == outcome].copy()
            worst = out_sub.loc[out_sub["t_stat"].abs().idxmin()]
            geo_summary.append(
                {
                    "leaveout_type": leaveout_type,
                    "outcome": outcome,
                    "min_abs_t": float(out_sub["t_stat"].abs().min()),
                    "median_abs_t": float(out_sub["t_stat"].abs().median()),
                    "worst_unit": str(worst["leaveout_unit"]),
                    "worst_t": float(worst["t_stat"]),
                    "worst_beta": float(worst["beta"]),
                }
            )

    thresh_summary_rows = []
    for outcome, sub in thresh.groupby("outcome", observed=True):
        k = int(sub["test_sign_matches_train"].sum())
        n = int(len(sub))
        lo, hi = wilson_interval(k, n)
        thresh_summary_rows.append(
            {
                "outcome": outcome,
                "splits": n,
                "median_test_beta": float(sub["test_beta"].median()),
                "median_test_abs_t": float(sub["test_t"].abs().median()),
                "share_test_p_lt_005": float((sub["test_p"] < 0.05).mean()),
                "share_sign_matches_train": float(sub["test_sign_matches_train"].mean()),
                "share_sign_matches_train_ci_low": lo,
                "share_sign_matches_train_ci_high": hi,
                "modal_recent_quantile": int(pd.Series(sub["selected_recent_quantile"]).mode().iloc[0]),
                "modal_permit_quantile": int(pd.Series(sub["selected_permit_quantile"]).mode().iloc[0]),
            }
        )
    thresh_summary = pd.DataFrame(thresh_summary_rows)

    null_summary = {}
    if len(thresh_null):
        k = int(thresh_null["test_sign_matches_train"].sum())
        n = int(len(thresh_null))
        lo, hi = wilson_interval(k, n)
        null_summary = {
            "splits": n,
            "median_test_abs_t": float(thresh_null["test_abs_t"].median()),
            "share_sign_matches_train": float(thresh_null["test_sign_matches_train"].mean()),
            "share_sign_matches_train_ci_low": lo,
            "share_sign_matches_train_ci_high": hi,
            "modal_recent_quantile": int(pd.Series(thresh_null["selected_recent_quantile"]).mode().iloc[0]),
            "modal_permit_quantile": int(pd.Series(thresh_null["selected_permit_quantile"]).mode().iloc[0]),
        }

    return {
        "sample_accounting": sample,
        "permutation": perm_records,
        "pretrend_and_post_with_presurge_controls": pretrend_records,
        "overlap_windows_current_load": overlap_records,
        "geographic_leaveout": geo_summary,
        "threshold_validation": thresh_summary.to_dict(orient="records"),
        "threshold_null_wage_only": null_summary,
        "monotonicity": mono.to_dict(orient="records"),
    }


def main() -> int:
    df, sample = prepare()
    perm = permutation_check(df)
    pretrend = pretrend_check(df)
    overlap = overlap_check(df)
    geo = geographic_leaveout(df)
    thresh = threshold_validation(df)
    thresh_null = threshold_null(df)
    mono = monotonicity(df)
    summary = build_summary(sample, perm, pretrend, overlap, geo, thresh, thresh_null, mono)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(
        f"Wrote {OUT_SUMMARY}, {OUT_PERM}, {OUT_PRETREND}, {OUT_OVERLAP}, "
        f"{OUT_GEO}, {OUT_THRESH}, {OUT_THRESH_NULL}, {OUT_MONO}, and {OUT_SAMPLE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### sources/immigration-causal/data/qcew/ACQUIRED.md

```text
# QCEW acquisition record

Date acquired: 2026-04-21

| Year | File | Source | SHA256 |
|---|---|---|---|
| 2018 | `2018_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2018/csv/2018_annual_singlefile.zip` | `7a5f948c28ef7f5498bb3522d36c80eb6ca8fed1942159dc897286f648b6115e` |
| 2019 | `2019_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2019/csv/2019_annual_singlefile.zip` | `ce3b0bbab9098170cd7f646908e6dfa6181db4119edfdb21f80ae415be1eae29` |
| 2020 | `2020_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2020/csv/2020_annual_singlefile.zip` | `dbc9eea24a9dd1d7d5c011defba76e47f6d938b714933c851517e2737d02be44` |
| 2021 | `2021_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2021/csv/2021_annual_singlefile.zip` | `96fc23b5f16adeaed7a97ae4063bb59feda1471c635082c4ccdcd6c42882d209` |
| 2022 | `2022_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2022/csv/2022_annual_singlefile.zip` | `29f852b0f6405615b45e41d40e930d2e93dd8cecab505f8395b0ceb50061551d` |
| 2023 | `2023_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2023/csv/2023_annual_singlefile.zip` | `6284aff110a81196803c4f2ab8613a511838878d1763b8a1a8a21231200b8f61` |
| 2024 | `2024_annual_singlefile.zip` | `https://data.bls.gov/cew/data/files/2024/csv/2024_annual_singlefile.zip` | `334ac1ec9101f516ed9698859a165666c6f6d08a51b35cb5fc1e1bf62e06b0da` |
```

### research/immigration-capacity-falsification-2026-04-21.md

```text
# Immigration capacity falsification pass — 2026-04-21

**Question:** After correcting the earlier placebo bug, what survives real falsification pressure in the county `flow/capacity` result, and what has to be narrowed?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior frontier memo argued that `recent immigrant flow relative to local build capacity` was the cleaner county stress object for wages, employment, and native sorting than stock share alone. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]  
**Instrument note:** This is a politically charged topic; treat the synthesis as a repo artifact to be checked against raw outputs, not as neutral narration from a bias-free instrument. [SOURCE: notes/llm-bias-caveat.md]

## Bottom line

1. The county `load/capacity` signal is still **structurally real on the descriptive side**. It beats `1,000` within-state permutations at the floor `p<=0.001`, survives leave-one-division-out, and remains strongly monotone across load deciles. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. The earlier “pretrend” critique was partly right for the **wrong test**. The old `2021–2022` placebo section was mislabeled because it used overlapping treatment windows. After rebuilding the panel with true `2018–2020` QCEW outcomes and a pre-surge permit baseline, wage pretrends look mostly weak before `2020`, but employment pretrends are already negative. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
3. The strongest defensible causal split is now asymmetric:
   - `wage story`: more plausibly surge-amplified, because true pre-2020 wage pretrends are weak, yet post-`2023–2024` wage effects remain negative after presurge controls [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
   - `employment story`: more confounded, because employment is already weaker in `2018–2019` and `2019–2020` before the surge-era overlap windows [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
4. The threshold result no longer supports a generic “real family across outcomes” claim. It now supports a **wage-tuned exploratory threshold** around `q60 recent-flow x q50 permit`, with holdout sign stability that clearly beats a null search, while transfer to `margin` is poor and transfer to `employment` is only moderate. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_null.csv]
5. The right updated claim is:
   - `flow/capacity` is a robust county stress marker [SOURCE]
   - it likely matters causally for wage-side strain [INFERENCE]
   - county employment effects are harder to separate from preexisting weakness [INFERENCE]
   - the county panel is still not enough to settle the full local-incidence causal graph by itself [INFERENCE]

## New artifacts

1. [analyze_capacity_falsification.py](./sources/immigration-causal/scripts/analyze_capacity_falsification.py)
2. [county_capacity_falsification_summary.json](./sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json)
3. [county_capacity_sample_accounting.json](./sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json)
4. [county_capacity_permutation_results.csv](./sources/immigration-causal/data/outcomes/analysis/county_capacity_

... [truncated for review packet] ...

usal/data/outcomes/analysis/county_capacity_threshold_validation.csv]
2. `employment`: sign matches training in `81.7%` of splits, `95% CI ≈ [70.1%, 89.4%]`, median `|t|≈0.74` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv]
3. `margin`: sign matches training in only `10%` of splits [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv]

### Null search

Under the same search procedure with within-state permuted `recent-flow`:

1. wage sign matches training only `35%` of the time, `95% CI ≈ [24.2%, 47.6%]` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_null.csv]
2. median holdout `|t|≈0.79` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_null.csv]

So the threshold search does beat the null for **wage**. It does **not** justify a sweeping “real family across outcomes” line. [INFERENCE]

## 7) Rival explanations

The strongest alternatives are still:

1. `selection into structurally weaker counties`
2. `regional growth and decline patterns that co-move with both immigration pressure and local outcomes`
3. `timing blur from the ACS recent-arrival proxy`

What the current pass rules out:

1. pure random reassignment [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv]
2. a one-state or one-division artifact [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]

What it does **not** fully rule out:

1. preexisting employment weakness
2. omitted local shocks that align with both build constraints and immigrant inflow
3. county-selection dynamics rather than a pure post-surge break

## What now survives

1. `flow relative to local build capacity` is a robust county stress marker [SOURCE]
2. the county signal is not random, not a one-state artifact, and not a binning accident [SOURCE]
3. wage-side post effects remain after presurge controls [SOURCE]
4. a wage-tuned exploratory threshold beats a null search [SOURCE]

## What now fails

1. `We found a clean generic post-surge causal threshold from the county panel alone.`  
This is too strong. [SOURCE]

2. `The pretrend critique kills the whole county result.`  
Also too strong. It survives for employment more than for wages. [SOURCE]

3. `The threshold story generalizes equally well to wages, employment, and politics.`  
False in the corrected pass. Margin transfer is poor. [SOURCE]

## Best current formulation

The strongest defensible version is:

1. `flow/capacity is a robust and highly structured county stress marker` [SOURCE]
2. `it likely operates as a real amplifier of local wage strain` [INFERENCE]
3. `employment effects are more confounded by preexisting county weakness` [INFERENCE]
4. `receiver-city shelter and service counterfactuals are still the best next causal design` [INFERENCE]

## Repo stance update

The repo's current best position should now be:

1. `descriptive confidence`: high [SOURCE]
2. `causal confidence on wage-side surge amplification`: moderate [INFERENCE]
3. `causal confidence on employment-side amplification`: low to moderate [INFERENCE]
4. `policy relevance`: still high, but [FRAMING-SENSITIVE] because the county marker is strong even where the causal partition is incomplete [INFERENCE]

## Revisions

### 2026-04-22

The first draft of this memo treated `2021–2022` overlap windows as placebo/pretrend evidence. After `/critique close` flagged that as a real semantics bug, the county panel was rebuilt with `2018–2020` QCEW outcomes and the falsification script was rewritten around a true presurge permit baseline. That correction narrowed the wage critique, preserved the employment critique, and collapsed the generic threshold-family claim into a wage-only exploratory result. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]
```

### research/immigration-reasoning-evolution-2026-04-21.md

```text
# Immigration reasoning evolution — 2026-04-21

**Purpose:** Record how the repo's immigration reasoning changed across this cycle, including where later falsification forced a real correction.  
**Status note:** This is a narrative reconstruction from dated memos, local review artifacts, and the current git history. It is not a formally versioned decision log. Treat chronology claims as `[INFERENCE]` unless a dated artifact or commit is named explicitly.  
**Instrument note:** Politically charged topic; keep the raw artifacts in view and do not treat this file as a neutral substitute for them. [SOURCE: notes/llm-bias-caveat.md]

## Artifact basis

1. [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](./research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md)
2. [immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md](./research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md)
3. [immigration-threshold-first-panel-2026-04-21.md](./research/immigration-threshold-first-panel-2026-04-21.md)
4. [immigration-threshold-causal-levers-2026-04-21.md](./research/immigration-threshold-causal-levers-2026-04-21.md)
5. [immigration-county-outcome-panel-2026-04-21.md](./research/immigration-county-outcome-panel-2026-04-21.md)
6. [immigration-capacity-frontier-2026-04-21.md](./research/immigration-capacity-frontier-2026-04-21.md)
7. [.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md](./.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md)
8. [immigration-capacity-falsification-2026-04-21.md](./research/immigration-capacity-falsification-2026-04-21.md)
9. commit `2cdd801` (`[analysis] Measure capacity frontier — compare stock flow and load`) [SOURCE: git history]
10. commit `1097c77` (`[research] Audit Bryan Caplan claims — score open-borders arguments`) [SOURCE: git history]

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

That reframed the project from `average wage effect` toward `flow x capacity x composition x regime`. [INFERENCE]

## Phase 3: the threshold object changes from stock to capacity

The first threshold pass did not confirm the naive `% foreign-born crosses 

... [truncated for review packet] ...

dows as placebo/pretrend evidence
2. it used a post-treatment permit denominator in the earlier-window section [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]

That led to an overly broad downgrade:

1. `high-load counties were already weaker`
2. `the strongest causal reading basically fails`

The critique was correct to reject that wording. [SOURCE]

## Phase 7: critique-close forces the real correction

`/critique close` produced the key correction artifact:

1. the placebo semantics were wrong
2. the threshold sign-stability metric was misstated
3. zero-permit exclusion needed to be explicit
4. geographic robustness needed to be stronger than leave-one-state-out [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]

That is the pivot where the reasoning evolution stops being just “more evidence” and becomes “error correction changed the conclusion.” [INFERENCE]

## Phase 8: corrected falsification splits wages from employment

After rebuilding the county panel with `2018–2020` QCEW and rewriting the falsification script around a true pre-surge permit baseline, the corrected picture is:

1. the descriptive load/capacity marker survives permutations, leave-one-division-out, and monotonicity [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
2. wage pretrends before `2020` are mostly weak, so the old blanket pretrend critique was too broad [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
3. employment pretrends are already negative before the surge windows, so the employment story remains materially confounded [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
4. post-`2023–2024` wage and employment effects still survive controls for true presurge windows [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]

This is the current best correction:

1. `wage-side surge amplification`: plausible
2. `employment-side surge amplification`: much less clean
3. `generic county threshold story across all outcomes`: too strong

## Phase 9: the threshold claim gets demoted, not killed

The corrected threshold search no longer supports a sweeping “real threshold family” line. It now supports:

1. a wage-tuned exploratory threshold around `q60 recent-flow x q50 permit`
2. holdout wage sign stability that beats a null search
3. poor transfer to margin
4. only moderate transfer to employment [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]

So the repo did **not** end at:

1. `thresholds are fake`

It ended at:

1. `threshold evidence exists, but it is outcome-specific and still exploratory`

## What the repo now actually believes

The current best position is:

1. `global-gains arguments survive only at bounded margins and with capacity caveats`
2. `destination-country incidence is mostly a capacity problem, not a stock-share problem`
3. `county flow/capacity is a strong stress marker`
4. `wage-side local effects are more credibly surge-amplified than employment-side effects`
5. `receiver-city synthetic controls remain the best next causal design`

## Why this file exists

Without this trace, later work can easily flatten two different things into one:

1. `we changed our mind because new data arrived`
2. `we changed our mind because a critique found a real bug in our reasoning`

Both happened here. The second one matters more. [INFERENCE]

## Revisions

### 2026-04-22

The first draft of this file narrated the earlier falsification pass as if its “pretrend” downgrade were already sound. After the corrected county panel and review artifacts landed, the file was rewritten to distinguish the bug-triggered correction from the evidence that still survives after that correction. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
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

jas verdict | Saying "Borjas vs Card is unresolved" or "rent exposure is just price discovery" |
| `immigration-causal-everify-card-vs-borjas.md` | E-Verify staggered TWFE on QWI 2003-2023, native low-skill wages | Citing Borjas wage prediction for the U.S. policy variation |
| `immigration-causal-saiz-elasticity-rent.md` | Saiz 2010 housing supply elasticity × ACS rent + foreign-born | Treating PUMA rent burden as elasticity-neutral |
| `immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | Evening cycle synthesis: 5 verdict updates, 8-finding ladder | Writing the headline immigration position; asking "what changed?" |
| `immigration-causal-internal-vs-immigrant-newcomers.md` | IRS SOI × ACS — native county inflow is 33× immigrant inflow | Treating "newcomer burden" as immigration-driven by default |
| `immigration-causal-surge-2021-2024.md` | OHSS encounters + CHNV + city costs + 2024 election: surge analysis | Extrapolating pre-2020 findings to surge magnitudes; discussing 2024 election in immigration terms |
| `immigration-county-outcome-panel-2026-04-21.md` | QCEW + IRS + threshold spine: county wages, employment, native mobility, and backlash in one frame | Saying threshold effects show up in wages, employment, or native sorting |
| `immigration-capacity-frontier-2026-04-21.md` | Stock vs flow vs flow-to-capacity comparison, threshold robustness grid, and a clearer statement of what still remains open on subgroups, voting, welfare, and receiver counterfactuals | Asking what is actually left to check after the first county threshold passes |
| `immigration-capacity-falsification-2026-04-21.md` | Corrected falsification pass with true `2018–2020` QCEW pretrend windows, `1,000`-draw permutation inference, division leave-out, explicit sample accounting, and wage-threshold null benchmarking | Asking which parts of the new flow-capacity story still survive after fixing the earlier placebo bug |
| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction that split the wage and employment stories | Wanting the evolution of reasoning itself traced rather than only the latest stance |

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
```

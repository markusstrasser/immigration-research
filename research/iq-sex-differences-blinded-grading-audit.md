# IQ Sex Differences - Blinded Grading / Recommendation Audit

**Date:** 2026-03-07  
**Purpose:** convert the school-evaluation node into a direct randomized audit with runnable materials, explicit estimands, and a preregistration-ready analysis outline.

Companion files:

- `sources/iq-sex-diff/build_grading_audit_materials.py`
- `sources/iq-sex-diff/data/grading_audit/README.md`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_packet_manifest.tsv`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_randomization_template.tsv`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_materials_checklist.tsv`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_name_pairs.tsv`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_evaluator_instructions.md`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_rubric_template.md`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_prereg_analysis_outline.md`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_math_packet_template.md`
- `sources/iq-sex-diff/data/grading_audit/grading_audit_recommendation_packet_template.md`

## 1. Why This Branch Exists

The late-school observational stack is now strong enough that the correct next move is to randomize the evaluation layer itself.

Across `HSLS`, `ELS`, `NELS`, `PSID TAS`, and public `Add Health`, the most stable female-leaning school/transition family is `evaluation`: grades, recognition, recommendations, and closely related school-performance outputs. Tested-math surfaces are more male or null, and raw course quantity is less stable than the evaluation family. [SOURCE: `research/iq-sex-differences-school-wedge-extended-synthesis.md`; `research/iq-sex-differences-school-wedge-mechanism-triage.md`; `research/iq-sex-differences-current-position.md`]

That does **not** identify evaluator bias by itself.

It does justify a direct randomized audit because the observational branch has already done the descriptive job. [INFERENCE]

## 2. What The Existing Literature Already Says

This branch should not pretend to be the first time anyone randomized evaluation.

Relevant prior work:

1. Terrier (2020) uses blind versus non-blind scores to show girls receive more favorable teacher evaluations in French middle-school math, with downstream consequences for science-track selection. [SOURCE: https://www.sciencedirect.com/science/article/pii/S0272775718307714]
2. Francis et al. (2024) report that white males were more likely to be recommended for AP Calculus at the same apparent preparedness, and that name-blind review did not remove the gap. That is direct motivation for separating grading from recommendation in this branch. [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]
3. Gil-Hernández et al. (2024) run a factorial teacher-evaluation experiment and show that ascribed-status cues can affect teacher judgments. [SOURCE: https://sociologicalscience.com/download/vol_11/august/SocSci_v11_743to776.pdf]
4. Null or weak-bias results also exist. A recent randomized teacher-assessment preprint reports no strong ethnicity or gender bias on otherwise identical assignments. That is a useful disconfirming prior: this audit should not prespecify the sign. [SOURCE: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5937709]

So the novelty here is narrower:

1. a direct audit targeted at the repo's exact `school-evaluation` node
2. explicit separation of `grading` versus `recommendation`
3. direct connection to the existing school-wedge synthesis rather than a standalone evaluator-bias paper

[INFERENCE]

## 3. Causal Check

> **Observation:** school-linked evaluation surfaces are the most stable female-leaning late-school family in the current repo, while tested-math surfaces are not. [SOURCE: `research/iq-sex-differences-school-wedge-extended-synthesis.md`]
>
> **Null:** if the wedge is driven entirely by real classroom performance bundles, transcript strength, or other non-evaluator channels, then holding packet content fixed and randomizing the visible student marker should not materially move grading or recommendation outcomes. [INFERENCE]
>
> **Residual after null:** if outcomes still move, evaluator-visible identity is doing causal work on at least part of the school-evaluation node. [INFERENCE]

- `P(cause)`: `0.58` that a direct randomized audit will show some nonzero evaluator effect on at least one school-evaluation surface. [INFERENCE]
- `Top alternative`: `0.30` that the late-school wedge is mostly real performance / school-pipeline structure and the randomized evaluator effect will be near zero. [INFERENCE]
- `Falsifier`: balanced randomized packets with no condition differences on grading or recommendation and tight uncertainty bounds. [INFERENCE]
- `Decision impact`: this branch is worth running because either sign of the result changes the repo's main causal story. [INFERENCE]

## 4. DAG

The design should stay structurally simple.

```text
packet_quality ------------------------------+
task_family ---------------------------------+--------------------+
subject_family ------------------------------+                    |
rubric_emphasis (if randomized) -------------+                    |
evaluator_stringency -------------------------+                    v
assignment_order / fatigue ------------------> [grade / recommendation]
                                                             ^
                                                             |
randomized_visible_identity --> evaluator_perception --------+
```

Interpretation:

1. `randomized_visible_identity` is the treatment.
2. `grade / recommendation` is the outcome.
3. `packet_quality`, `task_family`, and `subject_family` are design-stage or precision-stage variables, not mediators.
4. `evaluator confidence`, `time spent`, and `comment tone` are downstream and should not be used as primary adjustment variables in the treatment-outcome model. [INFERENCE]

## 5. Core Design

### 5.1 Treatments

Minimum first wave:

1. `blind`
2. `male_coded`
3. `female_coded`

Optional second-wave factor:

1. `rubric_emphasis = correctness/mastery`
2. `rubric_emphasis = effort/behavior`

The optional factor should **not** be added in the first pilot unless packet construction and evaluator count are already stable. [INFERENCE]

### 5.2 Task families

The first package assumes two task families:

1. `grading`
2. `recommendation`

That separation is non-negotiable because the literature and the repo both imply that recommendation/gatekeeping can move differently from raw grading. [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html; `research/iq-sex-differences-next-level-research-plan.md`]

### 5.3 Suggested packet families

The generated packet manifest uses six base packets:

1. `math_borderline_A`
2. `math_strong_B`
3. `writing_borderline_C`
4. `ap_calc_recommend_D`
5. `honors_ela_recommend_E`
6. `teacher_comment_F`

Why these:

1. two math grading packets test whether any effect is strongest near an evaluative margin
2. one writing grading packet acts as a negative-control subject family
3. one AP-calculus recommendation packet tests the strongest current gatekeeping lead
4. one honors-ELA recommendation packet tests whether any recommendation effect is broader than math
5. the comment packet is optional; it exists only if the human team wants text-tone coding in wave 1

[SOURCE: `sources/iq-sex-diff/data/grading_audit/grading_audit_packet_manifest.tsv`; `research/iq-sex-differences-next-level-research-plan.md`]

## 6. Materials Rules

The package assumes the following content discipline.

### 6.1 Allowed to vary

1. student marker only
2. blind ID versus name

### 6.2 Not allowed to vary

1. actual work product
2. prompt wording
3. rubric language
4. transcript/profile content
5. score band or prior-course information

### 6.3 Human decision still required

Choose one:

1. **real student work**
2. **synthetic benchmark work**

Tradeoff:

1. real work increases ecological validity but raises FERPA / IRB / de-identification burden
2. synthetic benchmark work is cleaner for packet control but less natural

The first pilot should prefer synthetic or fully transcribed/de-identified work unless there is already institutional approval for real student artifacts. [INFERENCE]

## 7. Randomization

The generator writes a balanced placeholder schedule to:

- `sources/iq-sex-diff/data/grading_audit/grading_audit_randomization_template.tsv`

Current defaults:

1. `36` evaluators
2. each evaluator sees all packet bases once
3. each evaluator sees only one identity version of a given packet base
4. conditions are balanced by `evaluator x packet_base_id`

That schedule is deployment-ready as a scaffold, not as a final ledger. The final ledger must be frozen after human packet selection and evaluator recruitment. [INFERENCE]

## 8. Outcomes And Estimands

### 8.1 Primary outcomes

1. `score_numeric`
2. `recommend_binary`
3. `honors_binary`

### 8.2 Optional secondary outcomes

1. `confidence_optional`
2. `comment_tone`
3. `free_text_notes`

### 8.3 Primary contrasts

Within packet family:

1. `female_coded - blind`
2. `male_coded - blind`
3. `female_coded - male_coded`

Those are intention-to-treat contrasts on evaluator-visible identity, not mediation estimates. [INFERENCE]

## 9. Analysis Plan

The prereg-style outline is packaged at:

- `sources/iq-sex-diff/data/grading_audit/grading_audit_prereg_analysis_outline.md`

Primary analysis:

1. randomization inference
2. permutation tests
3. packet-family-specific contrasts

Secondary precision model, descriptive only:

`outcome ~ C(condition) + C(packet_base_id) + C(evaluator_id) + C(packet_order_bin)`

Why this is enough:

1. the treatment is randomized
2. evaluator and packet fixed effects improve precision
3. the design does not need aggressive covariate adjustment

[SOURCE: `sources/iq-sex-diff/data/grading_audit/grading_audit_prereg_analysis_outline.md`; https://www.cambridge.org/core/journals/experimental-economics/article/permutation-tests-for-experimental-data/4FDAEE783F1A617C941D7F7DAEA90FE5]

## 10. What Not To Control For

Do **not** put these into the primary treatment model:

1. evaluator confidence
2. evaluator time spent
3. narrative feedback tone
4. guessed study condition

These are post-treatment or ambiguous descendants once the packet is assigned. [INFERENCE]

This is a randomized design, so `/causal-robustness` is not the main tool. Attrition checks and randomization balance matter more here than omitted-variable sensitivity. [INFERENCE]

## 11. Ready Now

This branch is actually packaged now.

Ready artifacts:

1. protocol memo
2. packet manifest
3. randomization template
4. materials checklist
5. evaluator instructions
6. rubric template
7. preregistration-style analysis outline
8. packet templates
9. deterministic material-generation script

[SOURCE: `sources/iq-sex-diff/build_grading_audit_materials.py`; `sources/iq-sex-diff/data/grading_audit/README.md`]

## 12. Still Human-Gated

The real remaining gates are:

1. final packet content
2. evaluator recruitment
3. deployment venue
4. IRB / FERPA review if real student work is used
5. final frozen assignment ledger

That is a real wall. It is not something the repo can automate away. [INFERENCE]

## 13. Stop Rules

1. If no asymmetry appears under randomization, stop using evaluator discrimination as the default explanation of the school-evaluation family.
2. If asymmetry appears only in recommendation and not grading, narrow the claim to gatekeeping.
3. If asymmetry appears only in one subject family, keep the claim subject-specific.
4. If blind versus visible identity matters more than male-coded versus female-coded identity, treat the live mechanism as `visibility of identity` rather than a simple directional sex bias. [INFERENCE]

## 14. Minimum Viable First Study

If the human team wants the smallest serious pilot:

1. use `math_borderline_A`, `writing_borderline_C`, and `ap_calc_recommend_D`
2. recruit `30-36` evaluators
3. keep only `blind`, `male_coded`, `female_coded`
4. skip rubric-emphasis variation
5. skip text-tone coding if evaluator burden is a risk

That pilot is strong enough to answer the narrow first question:

> is any part of the current school-evaluation wedge directly reproducible under randomized identity cues?

[INFERENCE]

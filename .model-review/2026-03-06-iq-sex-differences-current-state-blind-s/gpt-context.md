# REVIEW CONTEXT

# Review Target

Topic: IQ / sex-differences project current state and causal program through the PISA 2018 DIF-style proxy pass.

Task for reviewers:
- Red-team the current project state, not the whole repo.
- Focus on blind spots, invalid inferences, construct mismatch, conditioning errors, overclaiming, underclaiming, and the best next discriminating analyses.
- Assume no constitution or goals file exists; review for internal coherence and evidence discipline.

Highest-value materials:
1. research/iq-sex-differences-current-position.md
2. research/iq-sex-differences-claim-register.md
3. research/iq-sex-differences-analysis-protocol.md
4. research/iq-sex-differences-execution-plan.md
5. research/iq-sex-differences-master-plan.md
6. research/iq-sex-differences-pisa2018-dif-proxy.md
7. research/iq-sex-differences-item-face-validity-audit.md
8. research/iq-sex-differences-nlsy97-piat-cat-pass.md
9. research/iq-sex-differences-hsls-wedge-first-pass.md
10. research/iq-sex-differences-timss-cognitive-split.md
11. research/iq-sex-differences-early-school-age-matched-alignment.md

Specific review questions:
1. Which current claims are too strong, too weak, or mismatched to the evidence?
2. What are the biggest remaining methodological blind spots?
3. Is the PISA DIF-style proxy pass valid enough to update the causal tree, or is it more fragile than currently stated?
4. Are we underestimating any alternative explanation for the current cross-battery pattern?
5. What should be the next 3 analyses in strict priority order?


<doc path='research/iq-sex-differences-current-position.md'>
# IQ Sex Differences - Current Position

**Date:** 2026-03-05
**Purpose:** current synthesized view of the project after literature verification, `NLSY79`, `NLSY97`, `PIAAC`, `TIMSS`, and the first transcript-rich `HSLS` pass.

This file is the shortest reliable entry point for other agents.

For claim-level provenance and reversibility, see `research/iq-sex-differences-claim-register.md`.
For execution rules, see `research/iq-sex-differences-analysis-protocol.md`.
For the explicit causal tree and discriminating-node logic, see `research/iq-sex-differences-decisive-causal-tree.md`.
For the operational stage order and deliverables, see `research/iq-sex-differences-execution-plan.md`.
For the full end-to-end roadmap, validation ladder, and stage-completion criteria, see `research/iq-sex-differences-master-plan.md`.

---

## Scope

This file answers four questions only:

1. what the project has established
2. what the project has weakened
3. what remains open
4. what the next discriminating analyses are

It is **not** a substitute for the full literature memo or the full DOE. [INFERENCE]

## Evidence Recital

1. The literature does **not** establish a single stable, battery-independent sex difference in general intelligence `g`; domain differences are more stable than overall composite differences. [SOURCE: `research/iq-sex-differences-verification.md`]
2. In `NLSY79`, the same-sample schooling pass only partly attenuates female verbal / clerical edges and does not collapse male quantitative / mechanical patterns. [SOURCE: `research/iq-sex-differences-second-pass-results.md`]
3. In `PIAAC`, adult numeracy is male-leaning across country-waves, education groups, age bands, and broad occupation groups in the current local snapshot. [SOURCE: `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-piaac-age-occupation.md`]
4. In `TIMSS`, broad school math shifts femaleward from Grade 4 to Grade 8 in the overlap countries, while `TIMSS Advanced` upper-track mathematics remains male-leaning. That makes "math gap" an explicitly multi-surface object in the project. [SOURCE: `research/iq-sex-differences-timss-frontier.md`]
5. In `NLSY97`, the raw quantitative female edge is fragile; on the larger `process_core` sample it moves from same-sample base `+0.037` to adjusted `-0.041`. That is a real robustness warning, but the current Stage A block should be read as a stress test rather than clean mechanism identification because it mixes nuisance, mechanism, and descendant variables. [SOURCE: `research/iq-sex-differences-nlsy97-stage-a.md`; `research/review-1-audit.md`]
6. The project has already exposed one concrete data-handling risk: the first frozen `NLSY97` sex field was wrong for the local public extract and had to be corrected. [SOURCE: `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-analysis-protocol.md`]
7. In the first transcript-rich `HSLS` pass, girls are near parity at baseline math and slightly below boys on the later standardized math surface, but clearly above boys on transcript math GPA, and that wedge persists within common highest-math ladders. [SOURCE: `research/iq-sex-differences-hsls-wedge-first-pass.md`]
8. In the new same-cohort `NLSY97` `PIAT`/`CAT` pass, the female-looking quantitative signal does not generalize across youth math surfaces: `PIAT Math` is slightly male-leaning / near null in the overlap sample, `Arithmetic Reasoning` is slightly male-leaning / near null, and the female signal is concentrated in `Math Knowledge`. [SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`]
9. In the focused `TIMSS` cognitive split, broad school-math surfaces move femaleward from Grade 4 to Grade 8 most strongly on `knowing`, while `TIMSS Advanced` remains male-leaning across all domains and especially on `reasoning`. [SOURCE: `research/iq-sex-differences-timss-cognitive-split.md`]
10. In the first `PISA 2018` item/process pass, broad math is male-leaning, `43/60` math items are male-leaning, and the female-positive items do not cluster cleanly by simple burden quartile or generic time/visit load. [SOURCE: `research/iq-sex-differences-pisa2018-item-split.md`]
11. The newest frontier literature suggests some male-favoring broad school-math divergence can emerge very early after school entry, which means late-school transcript and advanced-track mechanisms are not sufficient as a full causal story. [SOURCE: `research/iq-sex-differences-frontier-literature-audit.md`]
12. In the `PISA 2018` framework-proxy pass, the item heterogeneity is now visibly structured: proxy `space_shape` is the most male-leaning content family, `change_relationships` is next, and proxy `uncertainty_data` is closest to parity. [SOURCE: `research/iq-sex-differences-pisa2018-framework-proxy.md`]
13. In the first local `NLSCYA` early-school pass, `PIAT Math` standard scores are female-leaning at younger ages and move toward parity by later childhood, so the local early-school node does not yet support a simple immediate male-edge story. [SOURCE: `research/iq-sex-differences-nlscya-early-school-first-pass.md`]
14. In the first `ECLS-K:2011` early-school replication, math is near parity in kindergarten and then becomes male-leaning by spring first and second grade, while reading stays female-leaning throughout. [SOURCE: `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`]
15. In the older `ECLS-K` school-entry cohort, broad math is already modestly male-leaning in kindergarten and becomes more male-leaning by spring first grade, while reading stays female-leaning throughout. [SOURCE: `research/iq-sex-differences-eclsk-early-school-first-pass.md`]
16. In the first early-school score-alignment pass, the raw `NLSCYA` female-looking math edge mostly collapses once math is anchored to same-wave reading. All three local child cohorts then show male-leaning `math minus reading` residuals. [SOURCE: `research/iq-sex-differences-early-school-score-alignment.md`]
17. In the age-matched early-school bridge, `NLSCYA` and `ECLS-K:2011` remain directionally aligned across overlapping `84` to `126` month windows: both show male-leaning `math minus reading` residuals, with `ECLS-K:2011` more male-leaning in magnitude. [SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`]
18. In the new public item face-validity audit, released `PISA` items and official `ASVAB` sample items do not show an obvious overt sex-coded “smoking gun,” but they do show clear construct-loading differences between spatial-layout, graph/table, and formula-schooling burdens. [SOURCE: `research/iq-sex-differences-item-face-validity-audit.md`]
19. In the first `PISA 2018` DIF-style conditioning pass, the broad raw male item lean shrinks sharply once item responses are conditioned on within-country OECD math ability, but a smaller residual content-family geometry survives: `space_shape` remains the most male-residual family, while `uncertainty_data` moves to near parity. [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`]

## Current Best Take

### Established enough to use operationally

1. The measurement layer is first-order, not a nuisance footnote. Battery composition, timing, adaptivity, score construction, and subgroup-specific process variables can materially change the sign or magnitude of observed sex gaps. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-timing-channels.md`; `research/iq-sex-differences-nlsy97-stage-a.md`]
2. Domain-specific differences are more stable than any single overall `g` story. Male-favoring spatial / mechanical / adult numeracy surfaces and female-favoring clerical-speed surfaces replicate more cleanly than any battery-independent composite gap. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-second-pass-results.md`]
3. School math is not a single stable surface either. `TIMSS` broad Grade 8 math and `TIMSS Advanced` upper-track math point in different directions, which raises the priority of curriculum, track, and selection nodes. [SOURCE: `research/iq-sex-differences-timss-frontier.md`]
4. The strong version of the "schooling / educator attention explains most of the pattern" story is weakened. Current local evidence supports it as a partial channel for some verbal / clerical surfaces, not as a master explanation. [SOURCE: `research/iq-sex-differences-second-pass-results.md`]
5. The raw `NLSY97` quantitative female edge should no longer be treated as strong evidence for a general female quantitative advantage. More narrowly: the current Stage A pass is enough to kill a confident “`NLSY97` discovered a real female quant edge” story, but not enough to identify a dominant causal mechanism. [SOURCE: `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-next-node-validation.md`; `research/review-1-audit.md`]
6. The school-linked evaluation / placement node is now materially stronger than it was before the raw NCES work. The current `HSLS` footprint says grades and some placement surfaces are not just noisy versions of tested math. [SOURCE: `research/iq-sex-differences-hsls-wedge-first-pass.md`; `research/iq-sex-differences-evaluation-placement-node.md`]
7. The current `NLSY97` anomaly is narrower than “female quantitative advantage.” The best-supported local description is a school-knowledge / `Math Knowledge`-heavy wedge, not a broad same-cohort female edge across all available youth math surfaces. [SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`]
8. The `TIMSS` cognitive split is directionally consistent with that narrower description: `knowing` moves femaleward faster than `applying` from Grade 4 to Grade 8, but advanced-track mathematics remains male-leaning and especially male on `reasoning`. [SOURCE: `research/iq-sex-differences-timss-cognitive-split.md`]
9. The first `PISA 2018` pass weakens any simple “generic process burden explains the school-age split” story. The broad `PISA` math surface is male-leaning, and the item-level heterogeneity does not sort cleanly by burden quartile alone. [SOURCE: `research/iq-sex-differences-pisa2018-item-split.md`]
10. The first `PISA 2018` framework-proxy pass says the remaining school-age heterogeneity is not random: the strongest male-leaning block is the proxy `space_shape` family, while proxy `uncertainty_data` is closest to parity. [SOURCE: `research/iq-sex-differences-pisa2018-framework-proxy.md`]
11. The causal tree now needs an explicit early-school emergence node, but the old “child cohorts point in opposite directions” summary is too crude. After the reading-anchor and age-matched bridge passes, the local child cohorts align directionally; the remaining disagreement is degree and timing, not sign. [SOURCE: `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-decisive-causal-tree.md`; `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md`]
12. The new public item audit is consistent with the current measurement-surface story: what is visually salient is construct-loading, not an obvious overtly sex-coded page design. That is useful as a sanity check, but it is still weaker than real DIF or invariant-item analysis. [SOURCE: `research/iq-sex-differences-item-face-validity-audit.md`]
13. The new `PISA` DIF-style pass says the school-age measurement node is now sharper than “raw item heterogeneity.” A large share of the raw family geometry compresses under ability conditioning, but a residual family pattern remains, strongest in `space_shape` and weakest in `uncertainty_data`. [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`]
13. The first local `PISA` item-fairness pass now sharpens the measurement story. A lot of the raw school-age male lean attenuates after conditioning on overall math ability, but the residual geometry is still not neutral: `space_shape` remains the clearest male-residual family and `uncertainty_data` is the cleanest near-parity family. [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`]

### Not established

1. A large stable male advantage in battery-independent general ability is **not** established by the current project state. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-nlsy97-stage-a.md`]
2. A strong "female-favoring pedagogy is masking a true male `g` advantage" story is **not** established either. The current footprint is too measurement-sensitive for that conclusion. [INFERENCE from `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-piaac-frontier.md`]
3. "`g` is bullshit" is too strong. A weaker claim is better supported: `g` is a useful but theory-laden summary, and sex-gap claims about it are much less clean than popular discussion implies. [⚠ FRAMING-SENSITIVE] [INFERENCE from `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-causal-graph.md`]

## Current Causal Read

> **Observation:** the project sees stable domain asymmetries, unstable composite gaps, one fragile `NLSY97` quantitative reversal, and a broadly male-leaning adult numeracy surface. [SOURCE: `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-piaac-frontier.md`]
>
> **Null:** if there is no large stable sex difference in battery-independent general ability, then construct mismatch, task design, timing, adaptive scoring, schooling-linked practice, and sample-selection effects can generate the observed pattern. [INFERENCE]
>
> **Residual after null:** some specific male-favoring domains remain large and stable enough that a pure "all artifact" story is also too weak. [SOURCE: `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-piaac-frontier.md`]

- `P(cause)`: `0.72` that the main disagreement in this project is driven more by measurement / construct / process differences than by a large stable sex difference in general ability. [INFERENCE]
- `Top alternative`: `0.18` that there is a true small male advantage on some highly `g`-loaded quantitative / spatial surfaces, but current batteries and school-exit surfaces obscure it. [INFERENCE]
- `Falsifier`: a preregistered, measurement-invariant, transcript-aware, multi-battery study showing the same male advantage across balanced batteries after process correction. [INFERENCE]
- `Decision impact`: the next work should attack the score surface and construct map before making stronger claims about latent general ability. [INFERENCE]

## Live Data-Collection And Measurement Risks

1. **Manifest / coding risk:** one concrete field-selection bug already occurred in `NLSY97`; similar issues are plausible in other public extracts. [SOURCE: `research/iq-sex-differences-second-pass-results.md`]
2. **Construct mismatch risk:** `ASVAB quantitative`, `CAT-ASVAB quantitative`, `PIAAC numeracy`, `PISA math`, and `TIMSS math` are not interchangeable merely because they all sound mathematical. [SOURCE: `research/iq-sex-differences-next-node-validation.md`; `research/iq-sex-differences-analysis-protocol.md`]
3. **Adaptive-score risk:** completion, routing, posterior variance, and process-quality variables can matter enough to distort subgroup means. [SOURCE: `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-next-node-validation.md`]
4. **Selection risk:** same-sample versus unrestricted estimates already moved some coefficients materially before any controls were added. [SOURCE: `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-nlsy97-stage-a.md`]
5. **Age-surface risk:** adult numeracy, broad school math, upper-track advanced math, and school-exit adaptive quantitative tests should not be read as the same developmental surface. [SOURCE: `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-next-node-validation.md`; `research/iq-sex-differences-timss-frontier.md`]
6. **Bad-control risk:** the first `NLSY97` Stage A process block mixes room-condition nuisance with score-generation descendants such as `items_complete` and posterior variance, so coefficient movement in that pass is not clean causal identification. [SOURCE: `research/review-1-audit.md`; `sources/iq-sex-diff/nlsy97_stage_a_pass.py`]
7. **Evaluation / placement risk:** grades, honors, recommendations, and some school-linked placement variables do contain sex-coded evaluation / classroom-performance signals in the first transcript-rich `HSLS` pass, so they should be treated as mechanism surfaces rather than clean latent-ability proxies. [SOURCE: `research/iq-sex-differences-evaluation-placement-node.md`; `research/iq-sex-differences-hsls-wedge-first-pass.md`]
8. **Extra-missing-code risk:** later-added transcript and `PIAT` fields in `NLSY97` use additional negative missing codes beyond the earlier Stage A surfaces, so local scripts must clean those explicitly before modeling. [SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`]
9. **Early-stage omission risk:** if the project only models adolescent and adult surfaces, it can misattribute an early-emerging broad school-math divergence to later transcript, label, or advanced-track mechanisms. [SOURCE: `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-decisive-causal-tree.md`]

## Next Discriminating Analyses

1. Recover the fully official `PISA 2018` compendium or perform a second independent framework coding so the current proxy content-ordering can be hardened or reversed explicitly. [SOURCE: `research/iq-sex-differences-pisa2018-framework-proxy.md`]
2. Deeper `NLSY97` transcript-course pass using the high school transcript course payload instead of only the derived summary fields. The child branch is directionally stable enough now that the highest-leverage unresolved node has shifted back to the localized late-school anomaly. [SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md`]
3. If the late-school pass still leaves ambiguity, return to the child bridge with composition-aware reweighting or a stronger psychometric bridge than reading. [SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`]
4. Cohort check in `ELS:2002`: replicate the transcript-grade-course wedge with another U.S. school-to-college panel and see whether the `HSLS` / `NLSY97` school-surface pattern survives. [SOURCE: `research/iq-sex-differences-hsls-wedge-first-pass.md`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-dataset-cards.md`]
5. If the project needs stronger evidence on item fairness rather than just item-family heterogeneity, move from face-valid inspection to formal item-level DIF / invariant-item rescoring on the `PISA` and `TIMSS` surfaces already staged locally. [SOURCE: `research/iq-sex-differences-item-face-validity-audit.md`; `research/iq-sex-differences-pisa2018-framework-proxy.md`]
6. Port the same DIF-style pass to `TIMSS` so the residual `space_shape` / `uncertainty_data` ordering can be checked on a second school-age battery before upgrading to a heavier IRT / anchor-item pass. [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`; `research/iq-sex-differences-timss-cognitive-split.md`]

## Reading Order For Other Agents

1. Start here for the current state.
2. Read `research/iq-sex-differences-claim-register.md` before asserting any strong claim.
3. Read `research/iq-sex-differences-decisive-causal-tree.md` before proposing new causal stories or DOE branches.
4. Read `research/iq-sex-differences-master-plan.md` before choosing the next tranche of work or proposing a new experiment sequence.
5. Read `research/iq-sex-differences-execution-plan.md` for the shorter operational stage order.
6. Read `research/iq-sex-differences-early-school-intake.md` before starting Stage 2 or assuming the `ECLS` payloads are ready in the same way as `NLSCYA`.
7. Read `research/iq-sex-differences-dataset-expansion.md` before assuming an external dataset is local or ready.
8. Read `research/iq-sex-differences-analysis-protocol.md` before running models or comparing datasets.
9. Read `research/iq-sex-differences-pisa2018-item-split.md` and `research/iq-sex-differences-pisa2018-framework-proxy.md` before discussing the school-age measurement node.
10. Read `research/iq-sex-differences-nlscya-early-school-first-pass.md`, `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`, `research/iq-sex-differences-eclsk-early-school-first-pass.md`, `research/iq-sex-differences-early-school-score-alignment.md`, `research/iq-sex-differences-early-school-age-matched-alignment.md`, and `research/iq-sex-differences-early-school-intake.md` before making claims about early-school emergence.
11. Read `research/iq-sex-differences-nlsy97-piat-cat-pass.md` and `research/iq-sex-differences-timss-cognitive-split.md` before discussing the quantitative anomaly.
12. Read `research/iq-sex-differences-frontier-literature-audit.md` before making claims about whether the project is ahead of, behind, or aligned with the recent literature.
13. Read `research/iq-sex-differences-next-node-validation.md` and `research/iq-sex-differences-nlsy97-stage-a.md` for the earlier state and remaining open-node logic.
14. Read `research/iq-sex-differences-verification.md` before making literature claims about overall `g`.
15. Read `research/iq-sex-differences-item-face-validity-audit.md` before making page-level claims about “obvious bias in the items” or conflating visible construct-loading with proven psychometric unfairness.
16. Read `research/iq-sex-differences-pisa2018-dif-proxy.md` before making claims about residual item unfairness on `PISA` or treating the raw item-family geometry as the final school-age measurement story.
</doc>

<doc path='research/iq-sex-differences-claim-register.md'>
# IQ Sex Differences - Claim Register

**Date:** 2026-03-05
**Purpose:** claim-level ledger for what the project currently thinks, why, and what could reverse it.

This file is for traceability. It is not a narrative memo.

Statuses:

- `hardened`: current project state supports using the claim operationally
- `softened`: claim remains possible but current evidence weakened it
- `open`: active unresolved node
- `rejected for now`: current evidence is not good enough to carry the claim

---

## Hardened Claims

| ID | Claim | Status | Confidence | Latest update | Main provenance | What would soften it |
| --- | --- | --- | ---: | --- | --- | --- |
| `C1` | The literature does not establish a single battery-independent sex difference in general intelligence `g`. | `hardened` | `0.70` | `2026-03-05` | `research/iq-sex-differences-verification.md` | A preregistered, representative, measurement-invariant multi-battery study finding the same sex gap direction and magnitude across balanced batteries and factor models. |
| `C2` | Domain-specific sex differences are more stable than overall composite differences. | `hardened` | `0.80` | `2026-03-05` | `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-piaac-frontier.md` | Cross-battery evidence showing the domain surfaces collapse once format and timing are aligned. |
| `C3` | Male-favoring spatial / mechanical surfaces are real enough that an "all artifact" story is too weak. | `hardened` | `0.80` | `2026-03-05` | `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-second-pass-results.md` | Unspeeded and within-family replications showing the gap largely disappears after practice / familiarity alignment. |
| `C4` | Female-favoring clerical-speed surfaces are real at the task level, even if the broader "general speed" interpretation remains weaker. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-second-pass-results.md` | Evidence that the gap disappears once coding-like task features are removed. |
| `C5` | The measurement layer is first-order: timing, construct choice, adaptivity, and score construction can materially change conclusions. | `hardened` | `0.85` | `2026-03-05` | `research/iq-sex-differences-timing-channels.md`; `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-analysis-protocol.md` | Stable results across raw, latent, invariant-item, and process-aware scoring surfaces. |
| `C16` | "Math gap" is not a single stable surface: in the current local TIMSS pass, broad Grade 4 math is male-leaning, broad Grade 8 math is near parity to slightly female-leaning, and TIMSS Advanced upper-track math is male-leaning again. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-timss-frontier.md` | A corrected or transcript-linked reanalysis showing the broad Grade 8 and advanced surfaces converge once track, content, and sample selection are aligned. |
| `C15` | Grades, honors, recommendations, and some school-linked placement variables are contaminated enough by evaluation / behavior / classroom-performance channels that they should not be treated as clean latent-math proxies. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-evaluation-placement-node.md`; `research/iq-sex-differences-hsls-wedge-first-pass.md` | Transcript-rich replications showing little or no residual grade-test wedge once ladder and prior math are fixed. |
| `C17` | In the current `HSLS` transcript-covered sample, girls are near parity at baseline math, slightly below boys on the later standardized math surface, but clearly above boys on transcript math GPA, and that wedge persists within common highest-math ladders. | `hardened` | `0.80` | `2026-03-05` | `research/iq-sex-differences-hsls-wedge-first-pass.md` | An audit showing the wedge is an artifact of miscoding, weights, or missing-code handling, or a replication showing the surfaces converge once aligned differently. |
| `C18` | In the same-cohort `NLSY97` `PIAT`/`CAT` overlap, the female-looking quantitative signal is not broad across youth math surfaces: `PIAT Math` and `Arithmetic Reasoning` are slightly male-leaning / near null, while the female signal is concentrated in `Math Knowledge`. | `hardened` | `0.80` | `2026-03-05` | `research/iq-sex-differences-nlsy97-piat-cat-pass.md` | A code audit showing the overlap build or missing-code handling is wrong, or an aligned youth replication where `PIAT`-like and `Math Knowledge`-like surfaces move together instead of splitting. |
| `C19` | In focused `TIMSS` domain results, the largest Grade 4 to Grade 8 femaleward shift is on `knowing`, while `TIMSS Advanced` remains male-leaning across domains and most strongly male on `reasoning`. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-timss-cognitive-split.md` | A corrected domain audit or cross-battery school-age replication showing the cognitive-domain pattern collapses once item format and track are aligned. |
| `C20` | In the first `PISA 2018` item/process pass, the broad math surface is male-leaning, most math items are male-leaning (`43/60`), and the female-positive items do not sort cleanly by simple burden quartile or generic time/visit load. | `hardened` | `0.70` | `2026-03-05` | `research/iq-sex-differences-pisa2018-item-split.md` | A framework-linked reanalysis showing the apparent heterogeneity is mainly an artifact of the first-pass family definition or country aggregation. |
| `C21` | Recent frontier literature indicates some male-favoring broad school-math divergence can emerge very early after school entry, so a purely late-school transcript or advanced-track explanation is too narrow. | `hardened` | `0.65` | `2026-03-05` | `research/iq-sex-differences-frontier-literature-audit.md` | Early-school cohort analyses showing little or no male-favoring widening after school entry once scaling, age, and weighting are aligned. |
| `C25` | In the first `ECLS-K:2011` early-school replication, math is near parity in kindergarten and then becomes male-leaning by spring first and second grade, while reading stays female-leaning throughout. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-eclsk2011-early-school-first-pass.md` | An extract or weight audit showing the observed wave pattern is wrong, or aligned early-school rescoring collapsing the male-widening math pattern. |
| `C26` | In the older `ECLS-K` school-entry cohort, broad math is modestly male-leaning from kindergarten and more male-leaning by spring first grade, while reading stays female-leaning throughout. | `hardened` | `0.75` | `2026-03-05` | `research/iq-sex-differences-eclsk-early-school-first-pass.md` | An extract or weight audit showing the older `ECLS-K` early-school pattern is wrong, or aligned rescoring collapsing the math-widening pattern. |
| `C28` | In the first early-school score-alignment pass, the raw `NLSCYA` female-looking math gap mostly collapses once math is anchored to same-wave reading, and all three local child cohorts show male-leaning `math minus reading` residuals. | `hardened` | `0.80` | `2026-03-05` | `research/iq-sex-differences-early-school-score-alignment.md` | A stronger bridge analysis showing the reading-anchor result is misleading and the aligned `NLSCYA` residual flips back female once age and score-family are handled better. |
| `C27` | The current early-school anomaly is more likely a score-family mismatch with sample-frame differences secondary than a real cohort shift or pure data artifact. | `hardened` | `0.85` | `2026-03-05` | `research/iq-sex-differences-early-school-ach.md`; `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md` | A stronger bridge analysis showing the `NLSCYA` / `ECLS` disagreement stays large or reopens directionally after better age and score-family alignment. |
| `C29` | In the age-matched child bridge, `NLSCYA` and `ECLS-K:2011` remain directionally aligned across overlapping `84` to `126` month windows: both are male-leaning on `math minus reading`, with `ECLS-K:2011` more male-leaning in magnitude. | `hardened` | `0.85` | `2026-03-05` | `research/iq-sex-differences-early-school-age-matched-alignment.md` | A stronger psychometric or composition-aware bridge showing the age-matched `NLSCYA` residual turns female or diverges directionally from `ECLS-K:2011`. |
| `C30` | In the inspected public item materials, the strongest visible difference is construct-loading rather than overt sex-coded wording: released `PISA` items and official `ASVAB` sample items visibly split across spatial-layout, graph/table, and formula-schooling burdens. | `hardened` | `0.60` | `2026-03-05` | `research/iq-sex-differences-item-face-validity-audit.md` | Broader public-item inspection showing that the apparent burden split was a cherry-picked impression or that equally many released items visibly contradict it. |
| `C31` | In the first `PISA 2018` DIF-style conditioning pass, much of the broad raw male item lean attenuates after conditioning on country-standardized overall math ability, but residual content-family structure remains: `space_shape` is still the most male-residual family and `uncertainty_data` is closest to parity. | `hardened` | `0.70` | `2026-03-06` | `research/iq-sex-differences-pisa2018-dif-proxy.md` | A fuller item-response / invariant-item analysis showing the residual family ordering disappears or reverses once the conditioning score is rebuilt without contamination from the target items. |

## Softened Claims

| ID | Claim | Status | Confidence | Latest update | Main provenance | What would re-harden it |
| --- | --- | --- | ---: | --- | --- | --- |
| `C6` | Schooling / educator attention explains most of the observed sex-gap structure. | `softened` | `0.25` | `2026-03-05` | `research/iq-sex-differences-second-pass-results.md` | Richer pre-test schooling and practice variables compressing same-sample clerical and verbal coefficients by `40%+` while leaving sample composition stable. |
| `C7` | `NLSY97` raw quantitative results show a broad female quantitative advantage. | `softened` | `0.15` | `2026-03-05` | `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-next-node-validation.md`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md` | Same-age replications showing the female edge on both `PIAT`-like and `CAT`-like math surfaces after aligned age and timing adjustment. |
| `C8` | Education composition alone explains the disagreement between `NLSY97` and adult numeracy surfaces. | `softened` | `0.20` | `2026-03-05` | `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-piaac-age-occupation.md` | A harmonized youth or young-adult battery showing the same female quantitative edge after education stratification. |
| `C24` | A simple immediate male broad-math divergence after school entry is already locally established across the project's early-school surfaces. | `softened` | `0.40` | `2026-03-05` | `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-nlscya-early-school-first-pass.md`; `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`; `research/iq-sex-differences-eclsk-early-school-first-pass.md` | Aligned score-family work showing the `NLSCYA` / `ECLS` disagreement mostly disappears in favor of a common near-zero or female-leaning early-school math shape. |

## Open Claims

| ID | Claim | Status | Confidence | Latest update | Main provenance | What would decide it |
| --- | --- | --- | ---: | --- | --- | --- |
| `C9` | The `NLSY97` quantitative sign flip is mainly a battery-local construct / item-family / school-knowledge surface effect rather than a broad latent quantitative edge. | `open` | `0.65` | `2026-03-05` | `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-next-node-validation.md`; `research/review-1-audit.md`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-timss-cognitive-split.md` | Same-age replications showing `PIAT`-like, applied, `knowing`, and `Math Knowledge`-heavy surfaces all moving together after aligned age, item-format, and track adjustment. |
| `C10` | There is a true small male advantage on some highly `g`-loaded quantitative / spatial surfaces, obscured by current battery disagreement. | `open` | `0.25` | `2026-03-05` | `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-piaac-frontier.md` | Measurement-invariant, transcript-aware multi-battery evidence showing the same direction after process correction. |
| `C11` | Female clerical-speed advantages are substantially mediated by literacy / schooling practice rather than a broad latent speed factor. | `open` | `0.45` | `2026-03-05` | `research/iq-sex-differences-causal-graph.md`; `research/iq-sex-differences-second-pass-results.md` | Nonclerical speed tasks, preschool samples, and richer schooling-practice controls. |
| `C12` | Adult numeracy gaps are partly amplified by field, occupation, or post-school accumulation rather than being created there. | `open` | `0.60` | `2026-03-05` | `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-piaac-age-occupation.md` | Better field-of-study / track proxies and younger adult surfaces. |
| `C22` | Early-school emergence is a separate causal node from later transcript / evaluation and advanced-track selection, and should be modeled explicitly rather than absorbed into `SchoolPipeline`. | `open` | `0.90` | `2026-03-05` | `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-decisive-causal-tree.md`; `research/iq-sex-differences-nlscya-early-school-first-pass.md`; `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`; `research/iq-sex-differences-eclsk-early-school-first-pass.md`; `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md` | Early-school cohort analyses showing the later school-surface geometry is already fully present at entry or does not widen after school entry. |
| `C23` | In the current `PISA 2018` framework-proxy pass, the school-age item heterogeneity is structured rather than random: proxy `space_shape` is the most male-leaning content family and proxy `uncertainty_data` is closest to parity. | `open` | `0.60` | `2026-03-05` | `research/iq-sex-differences-pisa2018-framework-proxy.md` | An official-compendium or independent-coder reanalysis showing the current content-family ordering is mostly a proxy-coding artifact. |
| `C32` | The residual `PISA 2018` content-family pattern after ability conditioning is evidence for item-family heterogeneity, but not yet proof of formal DIF because the pass conditions on OECD plausible values that likely contain target-item information. | `open` | `0.75` | `2026-03-06` | `research/iq-sex-differences-pisa2018-dif-proxy.md` | An explicit anchor-item or full IRT DIF pass that either confirms the same residual ordering or shows it was mainly a plausible-value conditioning artifact. |

## Rejected For Now

| ID | Claim | Status | Confidence | Latest update | Main provenance | Why rejected for now |
| --- | --- | --- | ---: | --- | --- | --- |
| `C13` | Men clearly have a large battery-independent general-ability advantage once female-favoring pedagogy is controlled. | `rejected for now` | `0.10` | `2026-03-05` | `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-nlsy97-stage-a.md` | Current evidence is too construct-sensitive and too mixed across batteries to support this. |
| `C14` | `g` is useless or purely circular, so the project should abandon psychometric analysis. | `rejected for now` | `0.10` | `2026-03-05` | `research/iq-sex-differences-causal-graph.md`; `research/iq-sex-differences-verification.md` | The psychometric surfaces still carry stable structure and predictive content; the better critique is overclaiming, not total uselessness. |

## Known Data And Measurement Risks

| Risk ID | Risk | Evidence | Action |
| --- | --- | --- | --- |
| `R1` | Manifest / field-selection errors can change conclusions. | The first frozen `NLSY97` sex field was wrong for the local extract. [SOURCE: `research/iq-sex-differences-second-pass-results.md`] | Keep dataset cards and frozen field manifests current. |
| `R2` | Construct names hide real non-equivalence. | `ASVAB quantitative`, `PIAAC numeracy`, and school math are not the same object. [SOURCE: `research/iq-sex-differences-analysis-protocol.md`; `research/iq-sex-differences-next-node-validation.md`] | Force construct crosswalks before cross-dataset rhetoric. |
| `R3` | Sample restriction can masquerade as causal attenuation. | Same-sample bases already moved some coefficients before controls. [SOURCE: `research/iq-sex-differences-second-pass-results.md`; `research/iq-sex-differences-nlsy97-stage-a.md`] | Keep unrestricted, same-sample base, and adjusted estimates separate. |
| `R4` | Adaptive scoring and process variables may distort subgroup means. | `NLSY97` process / precision block materially changed the quantitative sign. [SOURCE: `research/iq-sex-differences-nlsy97-stage-a.md`] | Prioritize process-aware replications and DIF checks. |
| `R5` | The current `NLSY97` Stage A block mixes nuisance controls with mediators and score-generation descendants. | The local process block includes `items_complete`, posterior variance, and effort-type variables, so coefficient movement there is not clean causal identification. [SOURCE: `research/review-1-audit.md`; `sources/iq-sex-diff/nlsy97_stage_a_pass.py`] | Separate design-only, mechanism, and bad-control stress-test specifications. |
| `R6` | School-linked variables can embed evaluation / placement and behavior signals, not just curriculum exposure. | Grade/test wedge literature suggests that grades and teacher-assessed surfaces can diverge from standardized performance in sex-coded ways, and the first `HSLS` pass now shows that wedge directly in a transcript-rich public-use sample. [SOURCE: `research/iq-sex-differences-evaluation-placement-node.md`; `research/iq-sex-differences-hsls-wedge-first-pass.md`] | Run explicit grade-test wedge and observability audits before treating grades / honors / placement as ability controls. |
| `R7` | Later-added `NLSY97` transcript and `PIAT` fields use additional negative missing codes that are not automatically covered by the original Stage A parser assumptions. | The new same-cohort `PIAT`/`CAT` pass had to explicitly recode transcript and `PIAT` negative values to missing before modeling. [SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`] | Keep field-specific missing-code cleaning explicit for new `NLSY97` surfaces. |
| `R8` | If the project only models adolescent and adult datasets, it can misattribute an early-emerging broad school-math divergence to later transcript, label, or advanced-track mechanisms. | Recent frontier literature says some male-favoring broad school-math divergence appears quickly after school entry, while the current local tree has been richer on later-school surfaces than on early-school ones. [SOURCE: `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-decisive-causal-tree.md`] | Build and run the early-school tranche before letting late-school mechanisms absorb all broad school-math movement. |
| `R9` | Early-school direction can look contradictory if raw child math scales are compared without an internal anchor. | Raw `NLSCYA` `PIAT Math` and raw `ECLS` broad school-entry math point in different directions, but the first reading-anchor pass removes most of that directional conflict. [SOURCE: `research/iq-sex-differences-nlscya-early-school-first-pass.md`; `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`; `research/iq-sex-differences-eclsk-early-school-first-pass.md`; `research/iq-sex-differences-early-school-score-alignment.md`] | Keep at least one internal anchor or bridge when comparing child math surfaces across datasets. |
| `R10` | Older `ECLS-K` later-wave age fields are not all on the same month scale, so naive age matching can silently become invalid. | In the local older `ECLS-K` extract, wave `5` age takes values `1` to `6` while waves `1` to `4` use month-scale ages, so late child bridging must not reuse it as if it were comparable. [SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`] | Verify a defensible recode or recover an alternative older `ECLS-K` late-wave age field before using late child age matching in that cohort. |
| `R11` | Face-valid item inspection is easy to overread into claims about fairness or latent ability. | The new public item audit shows visible construct-loading but cannot by itself establish statistical DIF, operational-bank bias, or latent-trait distortion. [SOURCE: `research/iq-sex-differences-item-face-validity-audit.md`] | Treat item inspection as a mechanism sanity check only; require formal item-level DIF / invariant-item work before making stronger fairness claims. |
| `R12` | The new `PISA` DIF-style pass uses OECD plausible values that likely contain information from the target items, which can attenuate or distort residual item effects. | The first item-fairness pass conditions each item on country-standardized `PV1MATH` to `PV10MATH` averages rather than on a custom anchor-item or invariant-item scale. [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`] | Treat the current pass as a proxy only; upgrade to explicit anchor-item or IRT DIF analysis before making stronger fairness claims. |

## Maintenance Rule

When a later doc changes one of these claim states, update this file and cite the new document in the `Main provenance` column.
</doc>

<doc path='research/iq-sex-differences-analysis-protocol.md'>
# IQ Sex Differences Stage -1 / 0A Protocol

**Date locked:** 2026-03-05
**Scope:** freeze the next empirical pass before running `ICAR`, `NLSY79`, `NLSY97`, or `PIAAC` models.
**Machine-readable companion:** `sources/iq-sex-diff/stage0_config.py`

---

## Purpose

This file is the pre-analysis lock for the next work tranche.

It freezes:

1. sign convention
2. estimands
3. ICAR composite grid
4. NLSY79 sibling-pair construction
5. score-layer and weight-layer handling
6. numeric decision thresholds already defined in the DOE

Anything that changes after this file should be treated as an amendment, not as a silent refactor.

## Sign Convention

All descriptive sex gaps use:

`d = (mean_female - mean_male) / pooled_sd`

Interpretation:

- positive values favor females
- negative values favor males

This matches the sign used in the timing-channel note and avoids switching polarity across files.

## Frozen Estimands

### 1. Subtest Mean Gap

Primary descriptive estimand for any subtest or domain:

`d = (mean_female - mean_male) / pooled_sd`

### 2. Within-Family NLSY79 Gap

Primary fixed-effects estimand:

`y_if = alpha_h + beta*female_i + gamma1*age_1981_i + gamma2*older_sibs_1979_i + epsilon_if`

Where:

- `alpha_h` is a household fixed effect using `HHID_1979`
- `female_i` is built from `SAMPLE_SEX_1979`
- `age_1981_i` is `AGE OF R 81`
- `older_sibs_1979_i` is `# SIBS OLDER THAN R 79`

Interpretation:

- `beta` is the within-household sex difference for the chosen subtest
- this is a shared-family-confounding test, not a full environment-purge

### 3. ICAR Composite Sensitivity

The overall sex gap is estimated across the frozen weight grid in [stage0_config.py](/Users/alien/Projects/research/sources/iq-sex-diff/stage0_config.py):

- `equal_weights`
- `verbal_heavy`
- `matrix_heavy`
- `spatial_heavy`

No additional composite weights may be added after inspecting the gaps unless they are marked as post-hoc.

## Frozen Dataset-Specific Score Rules

### ICAR

- Use the raw item matrix in `sapaICARData18aug2010thru20may2013.csv`
- Use the public domain key in `superKey60.tab`
- Score domain means from the fixed item groups:
  - `ln`
  - `mr`
  - `r3d`
  - `vr`
- Require at least `3` scored items per domain because the public SAPA release uses planned missingness and some domains top out at `4` administered items
- Treat the dataset as sample-descriptive and unweighted

### NLSY79

Primary score layer:

- use 1981 ASVAB section **scale scores**
- not raw section labels and not mixed raw / XRND scores

Frozen primary subtests:

- `R0616200` arithmetic reasoning
- `R0616400` word knowledge
- `R0616600` paragraph comprehension
- `R0616800` numerical operations
- `R0617000` coding speed
- `R0617200` auto and shop
- `R0617400` math knowledge
- `R0617600` mechanical comprehension
- `R0617800` electronic information

Sensitivity score layer:

- where available, use the later XRND ability scores for:
  - arithmetic reasoning
  - word knowledge
  - paragraph comprehension
  - math knowledge

Weight rule:

- descriptive ASVAB summaries use `R0614700`
- general background summaries can use `R0216101`
- sibling fixed-effects models are unweighted primary estimates

Missing-data rule:

- treat negative NLSY special codes as missing

### NLSY97

Primary score layer:

- use CAT-ASVAB ability estimates from the public-use XRND fields
- combine the public `POS` and `NEG` fields into one signed score
- use `R0536300` / `KEY!SEX_1997` as the respondent-sex field for this extract
- do not use `R0001000` for sex-gap estimation in the local public-use file because it is largely missing here

Frozen score surface:

- general science
- arithmetic reasoning
- word knowledge
- paragraph comprehension
- numerical operations
- coding speed
- auto information
- shop information
- math knowledge
- mechanical comprehension
- electronic information
- assembling objects

Summary-only sensitivity:

- `R9829600` math-verbal percentile

Weight rule:

- descriptive summaries use `R1236200`

### PIAAC

- analyze country files separately before any pooled estimate
- use all 10 plausible values per domain
- use `SPFWT0` plus the released replicate-weight system
- use `VARSTRAT`, `VARUNIT`, `VEMETHOD`, `VEFAYFAC`, and `VENREPS` as released
- detect delimiter by file family in the current local snapshot:
  - `p1` U.S. files are pipe-delimited
  - `p1` non-U.S. files are comma-delimited
  - current `p2` files are semicolon-delimited
- treat `p1` as the primary education-stratified surface because the current local `p2` files do not expose `EDCAT6/7/8`

## Frozen Domain Definitions

### NLSY79

- `clerical_speed` = mean of z-scored `numerical_operations` and `coding_speed`
- `verbal` = mean of z-scored `word_knowledge` and `paragraph_comprehension`
- `quantitative` = mean of z-scored `arithmetic_reasoning` and `math_knowledge`
- `mechanical` = mean of z-scored `auto_shop` and `mechanical_comprehension`
- `mechanical_plus_electronic` = mean of z-scored `auto_shop`, `mechanical_comprehension`, and `electronic_information`

### NLSY97

- `clerical_speed` = numerical operations + coding speed
- `verbal` = word knowledge + paragraph comprehension
- `quantitative` = arithmetic reasoning + math knowledge
- `mechanical` = auto information + shop information + mechanical comprehension

### ICAR

- `vr`
- `ln`
- `mr`
- `r3d`

## Frozen Covariate Blocks

### Block A: Descriptive

- sex only

### Block B: Minimal Pre-Test Demography

- sex
- age at test or closest age proxy
- race / ethnicity where available

### Block C: Shared-Family FE

- household fixed effect
- sex
- age at test proxy
- older-siblings count as birth-order proxy

### Block D: Pre-Test Schooling / Practice Proxies

Allowed variables are only those clearly measured before or at the test window.

For the first NLSY79 pass, the frozen candidate block is:

- `R0614900` ASVAB high-school grade status in 1981
- `R0006500` mother highest grade completed
- `R0007900` father highest grade completed
</doc>

<doc path='research/iq-sex-differences-execution-plan.md'>
# IQ Sex Differences - Execution Plan

**Date:** 2026-03-05
**Purpose:** convert the current causal tree into an execution sequence that can reduce uncertainty quickly and decisively.

This is the operational companion to:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-decisive-causal-tree.md`
- `research/iq-sex-differences-analysis-protocol.md`
- `research/iq-sex-differences-master-plan.md`

For the full end-to-end roadmap, literature tracks, validation ladder, and completion criteria, read `research/iq-sex-differences-master-plan.md` first. This file remains the shorter execution-order companion.

---

## Objective

The next tranche should answer one narrow question:

> after separating measurement surface, school pipeline, and track selection, is there any stable residual that still looks like a battery-invariant sex difference in general ability?

That means the plan is **not**:

1. run more generic pooled regressions
2. keep re-estimating the same composite on new samples
3. argue from one battery to all batteries

The plan **is**:

1. kill or harden the highest-value nodes in order
2. use the smallest number of analyses that create qualitatively different footprints
3. keep destructive and downstream controls out of the primary specs

---

## Current Node Ranking

From the current project state, the active nodes are:

1. `MeasurementSurface`
2. `SchoolPipeline`
3. `EarlySchoolEmergence`
4. `TrackSelection`
5. `AdultAccumulation`
6. residual `LatentGeneralGap`

Current probabilities are in `research/iq-sex-differences-decisive-causal-tree.md`.

Operational consequence:

- attack Nodes `1` and `2` first
- make Node `3` explicit before overloading transcript and track explanations
- only then attack Node `4`
- postpone stronger claims about Node `6` until the earlier nodes are materially reduced

---

## Execution Sequence

## Stage 1 - `PISA 2018` Item-Family And Timing Decomposition

**Priority:** highest
**Node attacked:** `MeasurementSurface`, then `SchoolPipeline`
**Why first:** `PISA 2018` is already local, public, large, item-level, and process-rich.

**Status:** raw item/process pass, framework-proxy pass, face-valid item audit, and first DIF-style conditioning pass are now executed in `research/iq-sex-differences-pisa2018-item-split.md`, `research/iq-sex-differences-pisa2018-framework-proxy.md`, `research/iq-sex-differences-item-face-validity-audit.md`, and `research/iq-sex-differences-pisa2018-dif-proxy.md`. The active Stage 1 task is now either `TIMSS` porting of the same residual screen or a heavier `PISA` anchor-item / IRT upgrade.

### Questions

1. Do female-tilting math surfaces concentrate in school-knowledge-heavy item families?
2. Do applied / reasoning-heavy or high-friction process items tilt differently?
3. Do timing, actions, or revisit patterns explain part of the apparent surface split?

### Primary estimands

1. sex gap on `PV1MATH` to `PV10MATH`
2. sex gap on item-family subscores
3. sex gap on timing / actions / revisit summaries
4. sex coefficient on item response under item fixed effects and item-family interactions

### Core methods

1. weighted descriptive gaps with replicate-weight variance
2. item-family decomposition
3. multilevel logistic or linear probability item models with item fixed effects
4. optional DIF screen on highest-value item clusters

### Success criteria

1. if school-knowledge-heavy items tilt female while applied / reasoning items do not, Node `1` hardens
2. if timing / action controls materially compress the female-tilting item families, Node `1` hardens further
3. if all item families move together, Node `1` softens and latent-domain explanations strengthen

### Output artifacts

1. `research/iq-sex-differences-pisa2018-item-split.md`
2. `research/iq-sex-differences-pisa2018-framework-proxy.md`
3. `research/iq-sex-differences-item-face-validity-audit.md`
4. `research/iq-sex-differences-pisa2018-dif-proxy.md`
5. `sources/iq-sex-diff/data/pisa/pisa2018_item_family_gaps.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_process_gaps.tsv`
7. `sources/iq-sex-diff/data/pisa/pisa2018_item_models.tsv`
8. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_proxy.tsv`
9. `sources/iq-sex-diff/data/pisa/pisa2018_dif_content_summary.tsv`
10. `sources/iq-sex-diff/data/pisa/pisa2018_dif_context_summary.tsv`
11. `sources/iq-sex-diff/data/pisa/pisa2018_dif_anchor_candidates.tsv`

### Stop rule

Do not proceed to fancy latent modeling until the first descriptive item-family geometry is visible.

---

## Stage 2 - Early-School Emergence Pass

**Priority:** highest
**Node attacked:** `EarlySchoolEmergence`
**Why second:** recent literature says some broad school-math divergence may open within the first years of schooling, and the repo already has local early-school datasets staged.

**Status:** three first-pass cohorts now exist locally, the first reading-anchor pass is done, and the age-matched bridge is done. The active early-school task is now to explain the remaining aligned magnitude mismatch rather than the old sign conflict. See `research/iq-sex-differences-early-school-intake.md`, `research/iq-sex-differences-early-school-score-alignment.md`, and `research/iq-sex-differences-early-school-age-matched-alignment.md`.

### Datasets

1. `ECLS-K`
2. `ECLS-K:2011`
3. `NLSCYA`

### Questions

1. Is the broad math gap near zero at entry and then male-favoring after the first school years?
2. Does early-school growth look different from the later `school-knowledge / transcript / labels` family now visible in `NLSY97` and `HSLS`?
3. Is the early-school surface broad math, or does it already show content-family splitting?

### Primary estimands

1. sex gap in early math at entry wave
2. sex gap in early math at later elementary waves
3. within-child or repeated-wave change in the sex gap across the first school years
4. early math versus early reading profile where the battery allows it

### Core methods

1. repeated-wave weighted descriptive gaps
2. cohort-comparable scaling checks
3. growth or difference models with frozen sign conventions
4. sensitivity to sample analyzability and school-entry age

### Success criteria

1. near-zero or female-leaning entry plus early male widening hardens Node `3`
2. stable male lean on both `ECLS` cohorts but weaker / later lean on raw `NLSCYA` that collapses under reading anchoring points to score-family mismatch rather than killing Node `3`
3. no meaningful widening across aligned child score families weakens the need for a separate early-school node

### Output artifacts

1. `research/iq-sex-differences-nlscya-early-school-first-pass.md`
2. `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`
3. `research/iq-sex-differences-eclsk-early-school-first-pass.md`
4. `research/iq-sex-differences-early-school-score-alignment.md`
5. `research/iq-sex-differences-early-school-age-matched-alignment.md`

### Stop rule

Do not let adolescent transcript or advanced-track stories absorb early broad-school divergence until this pass is run.

---

## Stage 3 - Deep `NLSY97` Transcript Payload Pass

**Priority:** highest
**Node attacked:** `SchoolPipeline`
**Why third:** this is the cohort that generated the anomaly, and current evidence says the anomaly is localized, but it should now be interpreted after the early-school node is separated out.

### Questions

1. Does the female-looking `Math Knowledge` signal stay localized once raw transcript ladder and course payload are unpacked?
2. Do transcript ladder, credits, and GPA move together, or are they different surfaces?
3. Does the grade-test wedge survive within narrower course ladders and transcript-defined exposure sets?

### Primary estimands

1. sex gap by transcript-defined course ladder
2. sex gap by transcript-defined math credits and GPA
3. residual wedge:
   - `transcript_math_gpa ~ female + PIAT + ladder + design block`
   - `PIAT ~ female + transcript_math_gpa + ladder + design block`
   - `MathKnowledge ~ female + PIAT + ladder + design block`

### Core methods

1. transcript-payload parsing and harmonization
2. same-sample specification curve
3. residual wedge models
4. subgroup checks by age-at-test and grade-at-test

### Success criteria

1. if `Math Knowledge` and transcript GPA stay female-tilting while `PIAT` / `AR` do not, Node `2` hardens
2. if the wedge collapses after raw transcript alignment, Node `2` softens materially

### Output artifacts

1. `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`
2. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_ladder_gaps.tsv`
3. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_wedge_models.tsv`

### Stop rule

Do not use grades or transcript variables as nuisance controls in any general-ability claim unless this pass first shows they are not wedge surfaces.

---

## Stage 4 - `ELS:2002` Grade-Test-Course Wedge Replication

**Priority:** high
**Node attacked:** `SchoolPipeline`
**Why fourth:** `HSLS` could still be idiosyncratic; `ELS` decides whether the wedge is cohort-specific or structural.

### Questions
</doc>

<doc path='research/iq-sex-differences-pisa2018-dif-proxy.md'>
# IQ Sex Differences - PISA 2018 DIF-Style Proxy Pass

**Date:** 2026-03-06
**Purpose:** move the `PISA 2018` school-age measurement node from raw item-family heterogeneity toward an actual fairness-style conditional item pass.

This is **not** full multi-group IRT. It is a first-pass DIF-style screen using the local public `PISA 2018` item extract and the OECD plausible-value math surface.

---

## Why This Pass Matters

Before this pass, the project had:

1. raw item-gap geometry
2. framework-proxy content-family geometry
3. public item face-validity inspection

What it did **not** have was a conditional item pass answering:

> after conditioning on overall within-country math ability, which item families still show residual sex tilt?

That is the right next question if the project wants to separate:

1. broad score-level sex differences
2. content-family differences
3. possible item-level distortion

---

## Method

### Data

Inputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`

### Conditioning surface

I used:

`math_avg = mean(PV1MATH ... PV10MATH)`

then standardized that **within country** using student weights:

`math_country_z`

So the comparison is not “girls versus boys in richer or poorer countries,” but:

`female residual at the same relative math level inside country`

### Item model

For each scored math item:

`item_score ~ female + math_country_z + female*math_country_z + country_FE`

Implementation details:

1. country fixed effects were handled by weighted within-country demeaning
2. weighted least squares used `W_FSTUWT`
3. standard errors are cluster-robust by country

Interpretation:

1. `uniform_female_beta` = conditional residual item tilt at the same within-country math level
2. `female*math_country_z` = nonuniform DIF-style proxy

This is a **screen**, not a final latent-trait fairness model. [INFERENCE]

---

## Main Results

### 1. Conditioning compresses the raw content-family gaps sharply

Weighted mean raw item gap versus weighted mean conditioned residual:

| content family | raw item gap `d` | conditioned uniform beta |
| --- | ---: | ---: |
| `space_shape` | `-0.061` | `-0.015` |
| `change_relationships` | `-0.053` | `-0.011` |
| `quantity` | `-0.036` | `-0.006` |
| `uncertainty_data` | `-0.023` | `+0.000` |

So the first decisive update is:

`a large share of the raw PISA item-family gap is ability-surface rather than pure item distortion`

That matters because it softens any claim that raw item geometry alone proves school-age unfairness.

### 2. `space_shape` still has the clearest residual male tilt

Even after conditioning, `space_shape` remains the most male-tilting content family on average:

1. `space_shape`: `-0.015`
2. `change_relationships`: `-0.011`
3. `quantity`: `-0.006`
4. `uncertainty_data`: `~0`

This is smaller than the raw geometry, but it does **not** disappear.

So the content-family ordering survives, just in compressed form.

### 3. `uncertainty_data` is basically neutral on average after conditioning

This is the cleanest family-level result in the pass.

Raw:

- `uncertainty_data = -0.023`

Conditioned:

- `uncertainty_data = +0.000`

That means the weak male tilt on raw data-display items is mostly gone once overall math level is held fixed.

### 4. Residual uniform DIF-style signals are item-specific, not generic

Most male-tilting residual items:

1. `Cash Withdrawal Q01`: `-0.076`
2. `Crazy Ants Q01`: `-0.052`
3. `Chair Lift Q02`: `-0.052`
4. `Running Time Q01`: `-0.050`
5. `Speeding Fines Q03`: `-0.049`
6. `Containers Q01`: `-0.044`
7. `Wooden Train Set Q01`: `-0.041`

Most female-tilting residual items:

1. `Seats in a Theatre Q01`: `+0.060`
2. `Employment Data Q02`: `+0.055`
3. `Part Time Work Q01`: `+0.052`
4. `Medicine doses Q01`: `+0.049`
5. `Carbon Tax Q02`: `+0.045`

These residuals are much narrower than the raw broad score story. They look like localized item-family / format / context effects, not a uniform whole-battery reversal.

### 5. Nonuniform DIF-style effects are mostly small

The nonuniform interaction term is generally weak at the family level:

1. `space_shape`: `+0.001`
2. `quantity`: `+0.001`
3. `change_relationships`: `-0.005`
4. `uncertainty_data`: `-0.005`

The biggest item-level nonuniform signals are still modest. The strongest was:

- `Wooden Train Set Q01`: about `-0.040`

So the current local `PISA` evidence points much more strongly to **uniform residual item-family tilt** than to big sex-by-ability slope reversals.

---

## Best Read

This pass changes the project in a useful way.

Before:

- raw `PISA` item geometry showed structured heterogeneity

Now:

- conditioning on OECD math ability removes a lot of that raw heterogeneity
- but it does **not** remove it all
- the remaining residual structure still points most clearly at `space_shape`
- `uncertainty_data` now looks close to measurement-invariant on average in this first pass

So the right update is:

`the PISA school-age measurement story is not “raw item gaps are fake,” and it is not “PISA is obviously biased.” It is “most raw content-family differences shrink under conditioning, but a smaller residual geometry survives, strongest in space-shape items.”`

---

## What Hardens

1. `MeasurementSurface` remains live, but it now looks more specific.
2. The strongest residual school-age content-family asymmetry is still in `space_shape`.
3. The weakest family after conditioning is `uncertainty_data`, which makes the raw/content split more interpretable.
4. The item-level fairness question should now focus on localized residual clusters, not a generic whole-test indictment.

## What Softens

1. The strongest reading of the raw `PISA` item-gap geometry as evidence of broad item unfairness.
2. The idea that all school-age content families retain equally strong residual sex tilt after ability conditioning.

## What Remains Open

1. whether full multi-group IRT / invariant-item rescoring would compress the residual `space_shape` pattern further
2. whether `TIMSS` shows the same residual family ordering
3. whether the highest-residual items cluster by format in a way the current proxy map is still missing

---

## Anchor Candidates

The pass also produced a first anchor-item list for a later invariant-item proxy score.

Lowest combined uniform + nonuniform residual items in this pass include:

1. `Number Check`
2. `Fence`
3. `Computer Game`
4. `Thermometer Cricket`
5. `Pipelines`

That is useful for Stage `1B`, but not yet decisive by itself because booklet rotation limits anchor coverage. [INFERENCE]

---

## Causal-Check Summary

- `P(cause)`: `0.75` that the school-age `PISA` disagreement is partly a content-family / residual measurement-surface problem rather than a generic process-burden problem or a broad female-favoring math surface.
- `Top alternative`: `0.15` that the surviving residual family pattern would mostly disappear under fuller IRT / invariant-item rescoring.
</doc>

<doc path='research/iq-sex-differences-nlsy97-piat-cat-pass.md'>
# IQ Sex Differences - NLSY97 PIAT vs CAT Pass

**Date:** 2026-03-05
**Purpose:** test whether the `NLSY97` quantitative sign flip looks like a broad youth math advantage for females, or a narrower test-surface wedge inside the same cohort.

Script: [nlsy97_piat_cat_pass.py](/Users/alien/Projects/research/sources/iq-sex-diff/nlsy97_piat_cat_pass.py)

Outputs:

- [nlsy97_piat_cat_extract.parquet](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_extract.parquet)
- [nlsy97_piat_cat_overlap_extract.parquet](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_overlap_extract.parquet)
- [nlsy97_piat_cat_surface_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_surface_gaps.tsv)
- [nlsy97_piat_cat_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_models.tsv)
- [nlsy97_piat_cat_cross_surface.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_cross_surface.tsv)
- [nlsy97_piat_cat_transcript_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_transcript_models.tsv)

Official anchors:

- `NLSY97` CAT-ASVAB appendix: <https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-10-cat-asvab-scores>
- `NLSY97` child assessments / PIAT: <https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/other-assessments/child-assessments>
- `NLSY97` high school transcript survey: <https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/high-school-transcript-survey>

---

## Question

The unresolved node was:

> is the `NLSY97` female-leaning quantitative result a broad youth math signal, or a battery-local surface effect?

The cleanest same-cohort falsification is `PIAT Math` versus `CAT-ASVAB` quantitative inside the overlap sample.

Why this pass matters:

1. `PIAT Math` is a second math surface inside the same cohort
2. `CAT-ASVAB` and `PIAT` can be compared on the same respondents
3. if the female-looking result is broad and latent, it should show up on both surfaces
4. if it is construct-local, the sign should diverge inside the same overlap sample

## Data Handling

### Surfaces added

- `CV_PIAT_STANDARD_SCORE_1997`
- `CV_PIAT_PERCENTILE_SCORE_1997`
- `ASVAB` test month and year
- age in months at the 1997 interview
- 1997 self-reported math-honors items
- high school transcript math surfaces:
  - `TRANS_CRD_GPA_MATH_HSTR`
  - `TRANS_MATHPIPE_HSTR`
  - `TRANS_TOT_MATH_HSTR`
  - `TRANS_TOT_ADV_MATH_HSTR`

### Important hygiene rule

The transcript and `PIAT` fields use additional negative missing codes beyond the earlier Stage A surfaces. This pass explicitly recodes those negative values to missing before any standardization or modeling. That matters because transcript variables use codes such as `-6`, `-7`, `-8`, and `-9` in the public-use file.

### Sample geometry

- weighted-sex valid `NLSY97` core: `6,748`
- nonmissing `PIAT` standard score 1997: `4,518`
- `PIAT` / `CAT` overlap with age and test-date fields: `3,738`

The official `PIAT` topical guide says the assessment was fielded in Round 1 for the age/grade-eligible youth subset, not the entire cohort. So this is a same-cohort youth-subset test, not a full-cohort generalization.

## Main Result

The female-looking `NLSY97` quantitative signal does **not** replicate as a broad math advantage on the alternate surface.

Inside the same `PIAT`/`CAT` overlap sample `n=3,738`:

- `PIAT Math`: `d = -0.046`, `95% CI (-0.110, +0.017)`
- `Arithmetic Reasoning`: `d = -0.036`, `95% CI (-0.100, +0.027)`
- `Math Knowledge`: `d = +0.132`, `95% CI (+0.071, +0.192)`
- `Quantitative = AR + MK`: `d = +0.052`, `95% CI (-0.009, +0.114)`

So the observed female-leaning signal is concentrated in `Math Knowledge`, not in `Arithmetic Reasoning`, and not on `PIAT Math`.

That is the key empirical footprint.

## Design-Only Models

Using only:

- age in months
- `ASVAB` test month
- `ASVAB` test year

the same overlap sample gives:

- `PIAT Math`: female beta `-0.052`, `95% CI (-0.114, +0.009)`
- `Arithmetic Reasoning`: female beta `-0.024`, `95% CI (-0.087, +0.039)`
- `Math Knowledge`: female beta `+0.151`, `95% CI (+0.093, +0.210)`
- `Quantitative`: female beta `+0.069`, `95% CI (+0.009, +0.130)`

So basic design alignment does not collapse the split. If anything, it sharpens it.

## Cross-Surface Wedge

The strongest diagnostic models are the conditional cross-surface fits.

### Conditional on `PIAT Math`

From [nlsy97_piat_cat_cross_surface.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_cross_surface.tsv):

- `Quantitative ~ female + PIAT + age + test date`:
  - female beta `+0.109`
  - `95% CI (+0.070, +0.147)`
- `Arithmetic Reasoning ~ female + PIAT + age + test date`:
  - female beta `+0.015`
  - `95% CI (-0.027, +0.058)`
- `Math Knowledge ~ female + PIAT + age + test date`:
  - female beta `+0.188`
  - `95% CI (+0.147, +0.228)`

### Conditional on `CAT Quantitative`

- `PIAT ~ female + quantitative + age + test date`:
  - female beta `-0.106`
  - `95% CI (-0.145, -0.067)`

Interpretation:

1. once `PIAT Math` is held fixed, the female residual lives almost entirely in `Math Knowledge`
2. once `CAT quantitative` is held fixed, `PIAT Math` still tilts male
3. that is not the footprint of one broad female math advantage
4. it is the footprint of a real same-cohort surface wedge

## Transcript Math Surfaces

Later high school transcript math surfaces remain female-favoring:

- transcript math GPA full-valid `d = +0.218`
- transcript math pipe full-valid `d = +0.085`
- transcript total math credits full-valid `d = +0.094`

And they stay female-favoring even conditional on `PIAT` or conditional on `CAT quantitative`:

- `transcript_math_gpa ~ female + PIAT + age + test date`: female beta `+0.259`
- `transcript_math_gpa ~ female + quantitative + age + test date`: female beta `+0.215`

That does **not** show that girls have higher IQ.

It does show that school-linked math outputs inside `NLSY97` move in a different direction from the alternate youth test surface.

## Causal Read

### What this pass hardens

1. The `NLSY97` anomaly is **not** a broad same-cohort female math result.
2. The anomaly is more local than the earlier project state allowed.
3. The local female-looking signal is concentrated in `Math Knowledge` and school-linked transcript surfaces.
4. `Arithmetic Reasoning` and `PIAT Math` do not carry the same female edge.

### What this pass weakens

1. a generic "girls are ahead on youth quantitative ability in `NLSY97`" story
2. a pure process-only explanation, because the divergence is not broad across the entire `CAT` quantitative surface
3. a same-sample missingness-only story, because the wedge survives inside the explicit overlap sample

### Best current explanation

The most defensible read is:

> the `NLSY97` sign flip is mainly a construct-local school-knowledge surface effect, not evidence of a broad female quantitative advantage.

That still leaves open whether the local surface difference is driven more by:

- item content / format
- curriculum exposure
- evaluation / placement channels
- some mixture of all three

But it is no longer clean to describe `NLSY97` as a simple counterexample to the male-leaning quantitative / numeracy pattern.

## Causal-Check Update

- `P(cause)`: `0.60` that the `NLSY97` quantitative anomaly is mainly a battery-local construct / item-family / school-knowledge surface effect.
- `Top alternative`: `0.20` that recent course exposure and school-linked knowledge accumulation create a real near-school-exit female edge on learned-math surfaces.
- `Falsifier`: a same-age youth battery where `PIAT`-like and `CAT Math Knowledge`-like surfaces point the same direction after aligned age and timing adjustment.
- `Decision impact`: stop using raw `NLSY97 quantitative` as generic evidence about overall quantitative ability or IQ; use it as evidence about a narrower `Math Knowledge`-heavy school-exit surface.

## Limitations

1. `PIAT` is only available for the youth-eligible subset, not the entire `NLSY97` cohort.
2. transcript variables are collected later and are selection-sensitive; they are useful mechanism surfaces, not clean nuisance controls.
3. this pass still does not have item-level `CAT` routing or DIF decomposition, so the exact item-family mechanism remains open.

## Best Next Step

The next highest-value analyses are now:

1. item-family and format decomposition in `PISA 2018` / `TIMSS 2019`, especially applied/problem-solving versus learned school-knowledge surfaces
2. `ELS` or further `HSLS` transcript replication of the grade / test / ladder wedge
3. if feasible, a deeper `NLSY97` transcript-course pass using the high school transcript course payload rather than only the derived summary fields
</doc>

<doc path='research/iq-sex-differences-hsls-wedge-first-pass.md'>
# IQ Sex Differences - HSLS Wedge First Pass

**Date:** 2026-03-05
**Purpose:** first transcript-rich `HSLS:09` pass on the grade-test wedge and
course-ladder node using the newly staged public-use respondent file.

**Primary files:**

- `sources/iq-sex-diff/hsls_wedge_first_pass.py`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_extract.parquet`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_frontier_sample.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`

## Bottom Line

The first `HSLS` pass finds a real school-surface wedge.

In the transcript-covered core sample (`n = 13,506`), girls are near parity at
baseline math, slightly below boys on the later standardized math surface, but
substantially above boys on transcript math GPA. That wedge persists inside the
common highest-math ladders.

So the project should stop treating transcript GPA or course placement as clean
ability proxies. But this does **not** prove simple female underplacement or
simple teacher bias as the whole mechanism.

## Observation Geometry

> **Observation:** in the transcript-covered `HSLS` core sample, weighted
> female-minus-male differences are `d = -0.017` at baseline math
> (`X1TXMTSCOR`), `d = -0.046` at the later math test (`X2TXMTSCOR`), but
> `d = +0.247` for transcript math GPA (`X3TGPAMAT`) and `d = +0.208` for GPA
> in the highest math course (`X3TGPAHIMTH`). [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`]
>
> **Null:** if transcript GPA, course placement, and standardized math all track
> the same latent math surface closely once prior math is known, then sex gaps
> should shrink toward zero and point in the same direction across those
> surfaces. [INFERENCE]
>
> **Residual after null:** the gaps point in opposite directions even within the
> same transcript-defined highest-math ladders. [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`]
>
> **Geometry:** persistent cross-surface wedge, not a single all-surface gap.
> [INFERENCE]
>
> **Magnitude:** controlled female coefficient is about `-0.051` on the later
> math test but `+0.227` on transcript math GPA once baseline math, ladder, and
> credits are included. [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`]
>
> **Lag window:** baseline grade-9 math to later school transcript surfaces.
> [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`]

## Raw Surface Audit

The working public-use file was:

- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`

The core overlap required:

1. valid sex
2. positive transcript-compatible weight `W3W1W2STUTR`
3. transcript coverage `X3TCOVERAGE = 1`
4. nonmissing baseline math, later math, highest-math ladder, transcript math
   GPA, and highest-math GPA

That yields:

- `core_n = 13,506`

The public-use file does carry the needed surfaces directly:

- baseline and later math scores: `X1TXMTSCOR`, `X2TXMTSCOR`
- transcript ladder: `X3THIMATH`
- transcript math credits: `X3TCREDMAT`, `X3TCREDAPMTH`
- transcript GPA surfaces: `X3TGPAMAT`, `X3TGPAHIMTH`, `X3TGPAWGT`
- transcript-compatible longitudinal weight: `W3W1W2STUTR`

## Main Results

### Overall weighted gaps

From `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`:

- baseline math: `d = -0.017`
- later math test: `d = -0.046`
- transcript math GPA: `d = +0.247`
- highest-math-course GPA: `d = +0.208`
- honors-weighted overall GPA: `d = +0.348`
- total math credits: `d = +0.076`
- AP/IB math credits: `d = -0.021`

That is already enough to say the transcript surface is not just mirroring the
standardized math surface.

### Within common highest-math ladders

From `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`:

- `Algebra II`: test `d = -0.109`, GPA `d = +0.232`
- `Precalculus`: test `d = -0.126`, GPA `d = +0.209`
- `AP/IB Calculus`: test `d = -0.234`, GPA `d = +0.153`
- `Calculus`: test `d = -0.139`, GPA `d = +0.161`
- `Probability and statistics`: test `d = -0.116`, GPA `d = +0.412`

So the wedge is not just “girls take different courses.” It remains visible
inside the same highest-math course categories.

### Weighted model table

From `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`:

- later math test with baseline + ladder + credits:
  - `beta_female = -0.051`
  - `95% CI = [-0.087, -0.015]`
- transcript math GPA with baseline + current test + ladder + credits:
  - `beta_female = +0.227`
  - `95% CI = [0.185, 0.268]`
- highest-math-course GPA with the same block:
  - `beta_female = +0.195`
  - `95% CI = [0.148, 0.242]`
- `precalc_plus ~ female + baseline_math`:
  - `beta_female = +0.041`
  - `95% CI = [0.017, 0.065]`

That last line matters: this does **not** look like a simple story where girls
are held out of advanced math given the same baseline.

## Causal Read

### What this does support

1. `HSLS` contains a real grade-test wedge on the school-math surface.
2. Grades and some placement surfaces are not interchangeable with standardized
   math.
3. A simple “girls are just obviously better on school math” reading is too
   strong, because the standardized test surface remains slightly male-leaning.
4. A simple “girls are just underplaced” reading is also too strong, because
   girls are slightly more likely to reach `precalculus+` conditional on
   baseline math in this first pass.

### What this does not support

1. It does **not** prove teacher bias as the dominant mechanism.
2. It does **not** prove the `HSLS` math test is itself sex-biased.
3. It does **not** prove anything final about latent general ability.

## Causal-Check Verdict

- `P(cause) = 0.55` that the main school-surface story here is a real
  evaluation / performance / transcript wedge: grades and course-linked school
  outputs encode something systematically more female-favoring than the tested
  math surface. [INFERENCE]
- `Top alternative = 0.25`: the `HSLS` standardized math surface itself is
  missing female-relevant classroom competence or is format-sensitive enough to
  understate female performance. This is less specific because the current pass
  does not yet use item/process data. [INFERENCE]
- `Falsifier`: a transcript-rich replication showing that once baseline math,
  course ladder, and transcript completeness are aligned, the GPA/test wedge
  shrinks near zero or flips to the same sign across surfaces. [INFERENCE]
- `Decision impact`: treat grades and course-placement variables as mechanism
  surfaces or strata, not as clean nuisance controls in the main causal model.
  Also stop using a generic “female underplacement” story as the default
  transcript explanation. [INFERENCE]

## Why `HSLS` Won The First Pass

`ELS` remains useful, but the immediate public-use `HSLS` surface was cleaner
for this question.

On the first raw audit:

- `HSLS` exposed varying transcript ladder, transcript GPA, transcript credits,
  and score variables directly in the staged student file
- several candidate `ELS` transcript summary variables appeared non-varying or
  effectively unusable in the first public-use pass, so it was the worse first
  surface for this exact wedge analysis

That is a workflow decision, not a final judgment on `ELS`.

## Next Best Moves

1. `ELS` viability audit:
   - determine which transcript/GPA/course variables survive in usable public
     form
   - replicate the wedge if the overlap is real
2. `NLSY97` same-cohort `PIAT Math` versus `CAT-ASVAB`:
   - test whether the `HSLS` wedge pattern appears inside the cohort that
     generated the raw female quantitative anomaly
3. `PISA 2018` / `eTIMSS` process pass:
   - test whether item format and process traces explain part of the remaining
     school-test surface
</doc>

<doc path='research/iq-sex-differences-timss-cognitive-split.md'>
# IQ Sex Differences - TIMSS Cognitive Split

**Date:** 2026-03-05
**Purpose:** test whether the `NLSY97` `Math Knowledge` wedge has a broader footprint in school-math batteries by separating `TIMSS` into `knowing`, `applying`, and `reasoning` surfaces.

Script: [timss_cognitive_split.py](/Users/alien/Projects/research/sources/iq-sex-diff/timss_cognitive_split.py)

Inputs:

- [timss_2019_grade_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_gaps.tsv)
- [timss_2019_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_summary.tsv)
- [timss_2019_grade_paired_deltas.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_paired_deltas.tsv)
- [timss_advanced_2015_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_gaps.tsv)
- [timss_advanced_2015_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_summary.tsv)

Outputs:

- [timss_cognitive_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_summary.tsv)
- [timss_cognitive_grade_paired.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_paired.tsv)
- [timss_cognitive_grade_contrasts.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_contrasts.tsv)
- [timss_cognitive_advanced_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_advanced_summary.tsv)
- [timss_cognitive_advanced_contrasts.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_advanced_contrasts.tsv)

Official sources:

- TIMSS 2019 international database: <https://timssandpirls.bc.edu/timss2019/international-database/>
- TIMSS Advanced 2015 international database: <https://timssandpirls.bc.edu/timss2015/advanced/international-database/>

---

## Question

The `NLSY97` same-cohort pass showed:

1. `Math Knowledge` female-leaning
2. `Arithmetic Reasoning` near null / slightly male
3. `PIAT Math` near null / slightly male

That suggests a narrower school-knowledge surface, not one generic math gap.

The `TIMSS` question is:

> does broad school math show the same kind of split when we separate `knowing` from `applying` and `reasoning`?

## Main Result

Yes, with an age-and-track twist.

### Grade 4

- `overall_math`: `d = -0.069`
- `knowing`: `d = -0.111`
- `applying`: `d = -0.043`
- `reasoning`: `d = -0.097`

At Grade 4, `knowing` is actually **more male-leaning** than `applying`, not less.

### Grade 8

- `overall_math`: `d = +0.017`
- `knowing`: `d = +0.029`
- `applying`: `d = -0.002`
- `reasoning`: `d = +0.017`
- `algebra`: `d = +0.088`

By Grade 8, `knowing` becomes the most female-tilting cognitive surface in the broad school sample, with `applying` closest to parity.

### Grade 8 minus Grade 4 shift

Across overlap countries:

- `overall_math`: `+0.076`
- `knowing`: `+0.139`
- `reasoning`: `+0.113`
- `applying`: `+0.043`

So the largest femaleward shift is in `knowing`, not in `applying`.

### TIMSS Advanced 2015

Upper-track advanced math flips back male:

- `overall_advanced_math`: `d = -0.148`
- `knowing`: `d = -0.127`
- `applying`: `d = -0.111`
- `reasoning`: `d = -0.195`
- `geometry`: `d = -0.205`
- `algebra`: `d = -0.142`
- `calculus`: `d = -0.105`

So the broad-population Grade 8 femaleward move does not carry into the advanced-track surface.

## What This Means

This does **not** perfectly replicate the `NLSY97` pattern.

It does something more useful:

1. it shows that school-math sex gaps are highly sensitive to cognitive subtype and academic stage
2. it shows that `knowing` moves femaleward faster than `applying` from Grade 4 to Grade 8
3. it shows that upper-track advanced math remains male-leaning across all cognitive domains, especially `reasoning`

That is directionally consistent with a **school-knowledge / curriculum / track** story, not with one simple latent general-math difference.

## Best Causal Read

### What this strengthens

1. The live `NLSY97` anomaly is unlikely to be a pure fluke.
2. School-knowledge-heavy surfaces can move differently from other math surfaces.
3. Track selection matters enough to reverse broad-population direction by the time we reach advanced mathematics.

### What this weakens

1. a single “boys better at math” story
2. a single “girls better at school math” story
3. the idea that one cognitive-domain label settles the latent-trait question

### Cleanest synthesis

The best-supported synthesis is:

> broad school-math surfaces become more female-tilting with age, especially on `knowing`, but advanced-track math remains male-leaning, especially on `reasoning`.

That maps cleanly onto the current project state:

- `NLSY97 Math Knowledge` female-leaning
- `PIAT` and `Arithmetic Reasoning` not female-leaning
- `HSLS` transcript math surfaces female-leaning
- `TIMSS Grade 8 knowing` slightly female-leaning
- `TIMSS Advanced reasoning` clearly male-leaning

## Causal-Check Update

- `P(cause)`: `0.65` that the active quantitative disagreement is driven mainly by school-knowledge / curriculum / track surfaces rather than one battery-invariant latent quantitative gap.
- `Top alternative`: `0.20` that item format and scaling alone are doing most of the work, with little substantive schooling or track mechanism behind them.
- `Falsifier`: a transcript-aware school dataset where `knowing`, `applying`, `reasoning`, and advanced-track math all move together once exposure and track are aligned.
- `Decision impact`: the next datasets should be used to split `school knowledge`, `applied/problem-solving`, and `advanced-track selection` instead of talking about “math” as one object.

## Next Step

The best next external extension is still `PISA 2018` item-format decomposition, because it can test:

1. school-knowledge-heavy versus applied/problem-solving items
2. digital/item-format effects
3. whether the Grade 8 `TIMSS` pattern is specific to `TIMSS` or generalizes to another large school-age battery
</doc>

<doc path='research/iq-sex-differences-early-school-age-matched-alignment.md'>
# IQ Sex Differences - Early-School Age-Matched Alignment

**Date:** 2026-03-05
**Purpose:** tighten the child-score bridge after the first reading-anchor pass by comparing `NLSCYA` and `ECLS-K:2011` on explicit overlapping age windows rather than broad wave labels.

This is the second bridge step after the early-school ACH and the first score-alignment pass.

---

## Question

The live question after the first score-alignment pass was:

> once the raw directional conflict is removed, does the remaining `NLSCYA` versus `ECLS` difference survive explicit age matching, or was wave-level comparison still exaggerating the disagreement?

The prediction from the current causal tree was:

1. the sign conflict should stay dead under age matching
2. the remaining difference should shrink to a magnitude / timing problem
3. `NLSCYA` should not reopen a female-leaning child-math contradiction once math is anchored to same-age reading

---

## Data Surface

Inputs:

1. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
2. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
3. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`

New analysis script:

1. `sources/iq-sex-diff/early_school_age_matched_alignment.py`

Outputs:

1. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_pairs.parquet`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_gaps.tsv`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_models.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_compare.tsv`

Important note:

1. older `ECLS-K` wave `5` carries an age field on a non-month scale (`1` to `6` in the local extract), so it is not usable for the late child age-matched bridge and is treated as support only through the valid earlier-age windows

---

## Method

For each dataset:

1. pair math and reading within the same child-wave
2. require the paired math and reading age fields to match exactly up to a small numeric tolerance
3. assign explicit age bins in months:
   - `84_90`
   - `90_96`
   - `96_102`
   - `102_108`
   - `108_114`
   - `114_120`
   - `120_126`
   - `126_132`
4. standardize math and reading within each dataset-age-bin
5. compute:
   - `math_z`
   - `reading_z`
   - `math_minus_reading_z`
6. estimate weighted female-minus-male `d` on all three outcomes
7. run weighted `math_z ~ female + reading_z` within each dataset-age-bin

Interpretation:

1. `math_minus_reading_z` asks whether math is relatively more male-leaning than reading at the same child age
2. `female` in `math_z ~ female + reading_z` asks whether girls still retain a math advantage once the same-age reading surface is held fixed

This is still a bridge analysis, not a full psychometric harmonization.

---

## Main Results

### 1. The directional bridge holds under explicit age matching

Across every overlapping `NLSCYA` and `ECLS-K:2011` bin from `84` to `126` months, aligned `math_minus_reading_z` remains male-leaning in both datasets.

`NLSCYA math_minus_reading_z`

1. `84_90`: `-0.186`
2. `90_96`: `-0.185`
3. `96_102`: `-0.135`
4. `102_108`: `-0.227`
5. `108_114`: `-0.266`
6. `114_120`: `-0.354`
7. `120_126`: `-0.124`

`ECLS-K:2011 math_minus_reading_z`

1. `84_90`: `-0.369`
2. `90_96`: `-0.467`
3. `96_102`: `-0.502`
4. `102_108`: `-0.550`
5. `108_114`: `-0.474`
6. `114_120`: `-0.552`
7. `120_126`: `-0.444`

So the first score-alignment result was not a wave-label artifact. The child-level sign conflict stays gone under explicit age matching.

### 2. The remaining disagreement is magnitude, not sign

Relative to `ECLS-K:2011`, `NLSCYA` is consistently less male-leaning on the aligned math-versus-reading surface.

Difference in aligned `math_minus_reading_z`:

1. `84_90`: `+0.183`
2. `90_96`: `+0.283`
3. `96_102`: `+0.367`
4. `102_108`: `+0.323`
5. `108_114`: `+0.208`
6. `114_120`: `+0.198`
7. `120_126`: `+0.320`

The project should now stop talking as if `NLSCYA` directionally contradicts the `ECLS` cohorts. It does not. The remaining question is why the aligned `ECLS-K:2011` surface is more male-leaning at the same ages.

### 3. Conditional-on-reading models say the same thing

Female coefficient in weighted `math_z ~ female + reading_z`:

`NLSCYA`

1. `84_90`: `-0.111`
2. `90_96`: `-0.135`
3. `96_102`: `-0.082`
4. `102_108`: `-0.126`
5. `108_114`: `-0.081`
6. `114_120`: `-0.324`
7. `120_126`: `-0.128`
8. `126_132`: `+0.006`

`ECLS-K:2011`

1. `84_90`: `-0.206`
2. `90_96`: `-0.285`
3. `96_102`: `-0.281`
4. `102_108`: `-0.331`
5. `108_114`: `-0.288`
6. `114_120`: `-0.367`
7. `120_126`: `-0.285`
8. `126_132`: `-0.381`

So the same-age conditional math residual is negative in both datasets through almost the full overlap range. `NLSCYA` simply stays closer to parity.

### 4. The older `ECLS-K` cohort still supports the earlier-age geometry

Where older `ECLS-K` has valid month-scale ages, the aligned residual is also male-leaning:

1. `84_90`: `-0.298`
2. `90_96`: `-0.298`
3. `96_102`: `-0.393`

That keeps the older cohort consistent with the general direction of the bridge, even though its later age field is not usable for direct late-child matching.

---

## Causal Update

### What hardens

1. the first alignment result was real, not a wave-label convenience
2. the early-school anomaly is now best understood as a magnitude mismatch after alignment, not a sign contradiction
3. score-family mismatch remains the leading explanation for why raw `PIAT Math` looked different from raw `ECLS` broad math

### What softens

1. any remaining narrative that `NLSCYA` directionally contradicts early male broad-math emergence
2. the need to keep reopening the early-school sign question

### What remains open

1. why aligned `ECLS-K:2011` is still more male-leaning than aligned `NLSCYA` at the same ages
2. whether the remaining gap is mostly sample-frame composition, scale-family intensity, or residual age-structure mismatch inside the public pairable subsamples
3. whether a stronger psychometric bridge than reading can shrink the remaining magnitude gap further

---

## Best Read

The early-school branch is materially cleaner again.

The best current read is:

1. the project no longer has a real early-school directional conflict
2. after explicit age matching, `NLSCYA` and `ECLS-K:2011` still point the same way
3. the remaining disagreement is that `ECLS-K:2011` is more male-leaning than aligned `NLSCYA` at the same ages

That means the early-school node is now good enough to stop absorbing time as a “maybe it is all contradictory” objection. The next high-value move can shift back toward the late-school transcript node.

---

## Causal-Check Summary

- `P(cause)`: `0.85` that the raw early-school anomaly was mainly score-family mismatch, with residual magnitude differences left over after alignment.
- `Top alternative`: `0.10` that sample-frame composition explains most of the remaining aligned magnitude gap.
- `Falsifier`: a stronger bridge analysis showing aligned `NLSCYA` turns female again or a composition-aware reweighting that makes the datasets diverge directionally.
- `Decision impact`: stop treating the child branch as directionally unresolved. The next major tranche should focus on the deeper `NLSY97` transcript payload pass unless a better psychometric child bridge becomes easy to run.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/early_school_age_matched_alignment.py`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_pairs.parquet`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_gaps.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_models.tsv`
5. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_compare.tsv`
</doc>

# IQ Sex Differences - Node Table

**Date:** 2026-03-06
**Purpose:** turn the master DAG into a node-by-node table showing what each node means, what it points to, which observed proxies exist locally, and which coefficients we actually have.

This file is the strict companion to:

- `research/iq-sex-differences-master-dag.md`
- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-analysis-protocol.md`

---

## Scope

This table does **not** pretend that every causal node has one universal coefficient.

The project now has two different objects:

1. **structural arrows** such as `Test design -> observed score` or `School evaluation -> attainment`
2. **estimated local edges** such as `female -> math_grade_points` in `Add Health`

This file only records coefficients where the repo has actually estimated them. Everything else stays structural. [INFERENCE]

---

## Conventions

- `Hardened` = supported enough to use operationally
- `Live` = real node, but still mechanism-open or only partially measured
- `Open` = unresolved or only weakly identified
- `Context` = important background node, but not yet separately estimated as its own object

---

## 1. Background Nodes

| Node | Main parents | Main children | Main observed proxies | Example local coefficients we have | Status | Current read |
|------|--------------|---------------|------------------------|------------------------------------|--------|--------------|
| `Sex` | none inside the project DAG | every downstream sex-gap surface | sex/female indicators across all local cohorts | not one coefficient; examples are surface-specific, such as `female -> math_grade_points = +0.226` in `Add Health`, `female -> h4ed2 = +0.601` background-only in `Add Health`, and `female -> college_years = +0.637` background-only in `FFCWS` | `Hardened` | upstream by definition, but clearly not acting through one single observed channel [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_models.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_attainment_decomposition.tsv`] |
| `Family SES` | none inside the school-age DAG | early environment, school behavior, transcript access, later attainment | income, poverty, public assistance, parental occupation | in wave I `Add Health`, `any_parent_public_assist d = -0.016`; in `FFCWS`, poverty enters every main child/outcome model as `cm1inpov` | `Context` | clearly upstream and admissible as background adjustment, but not itself the main explanatory object of the sex differences project [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_parent_background.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_models.tsv`] |
| `Parent education` | none inside the school-age DAG | early environment, school behavior, transcript exposure, later attainment | `parent_ed_max`, maternal education categories | in wave I `Add Health`, `parent_ed_max d = -0.041`; in `FFCWS`, `mother_education_cat` is part of the baseline adjustment block | `Context` | standard pre-treatment background cause, small measured sex imbalance in the staged `Add Health` sample [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_parent_background.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_joint_models.tsv`] |
| `Family structure` | none inside the school-age DAG | behavior, attendance, school surfaces, later attainment | resident mother/father, family structure categories | in wave I `Add Health`, `resident_mother d = +0.079`, `resident_father d = -0.058` | `Context` | real background node; measured sex imbalance is not huge in the staged `Add Health` sample, but it is not zero either [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_parent_background.tsv`] |
| `Race / ethnicity` | none inside the school-age DAG | school context, background opportunity structure, transcript/test surfaces, attainment | race/ethnicity categories in all main U.S. cohorts | no single canonical coefficient yet; used as background stratifier or adjustment surface in `NLSY97`, `Add Health`, and `FFCWS` models | `Context` | should be treated as a social/institutional background stratifier in this repo, not as a biological claim [SOURCE: `research/iq-sex-differences-mediator-design.md`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_joint_models.tsv`] |
| `Cohort / country / policy regime` | none inside the DAG | test design, school pipeline, adult accumulation | dataset identity, cohort year, country-wave | not one coefficient; the empirical footprint is cross-surface sign instability across `NLSY79`, `NLSY97`, `PIAAC`, `TIMSS`, and `PISA` | `Hardened` | this is one reason the repo stopped talking about a single invariant “math gap” or “IQ gap” object [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-timss-frontier.md`; `research/iq-sex-differences-piaac-frontier.md`] |
| `School context / institution quality` | background nodes plus cohort/policy | behavior, evaluation, transcript exposure, track, test surfaces | teacher encouragement, climate, school-offer fields, school administrator surfaces where available | no single cross-cohort coefficient; in `HSLS`, adding homework/self-efficacy/belonging/teacher-climate shifts later tested math from `-0.079` to `-0.045` on the common sample while GPA/track wedges survive | `Live` | clearly matters, but public-use measures are noisy and partial; current measured school-climate blocks move tested math more than they eliminate evaluation wedges [SOURCE: `research/iq-sex-differences-hsls-wedge-refinement.md`; `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_family_summary.tsv`] |

---

## 2. Measurement And Child Nodes

| Node | Main parents | Main children | Main observed proxies | Example local coefficients we have | Status | Current read |
|------|--------------|---------------|------------------------|------------------------------------|--------|--------------|
| `Test design / score construction` | cohort/policy, instrument choice | every observed score surface | timing, item family, adaptivity, scoring rules, process-data features | `PISA 2018` leave-out residual family effects: `space_shape = -0.015`, `change_relationships = -0.010`, `quantity = -0.002`, `uncertainty_data = +0.003`; `NLSY97` Stage A same-sample quantitative moves `+0.037 -> -0.041` under the large process/precision block | `Hardened` | first-order node; not a nuisance. This is one of the clearest project findings now [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_content_summary.tsv`; `research/iq-sex-differences-nlsy97-stage-a.md`] |
| `Behavior / compliance / engagement` | sex, background, school context | observed scores, evaluation, transcript observability | homework, absence, suspension, effort, items completed, rapid guessing, response time | in the school-wedge mechanism summary, behavior-heavy blocks tend to move tested-math surfaces more than evaluation-family surfaces; example: one tested-math block moves `-0.173 -> -0.072`, while evaluation-family mean shifts are small (`-0.008`, `+0.018`, `+0.025`) | `Live` | real node, but not the whole explanation. Measured behavior/compliance has not killed the evaluation family or the `Math Knowledge` wedge [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_family_summary.tsv`; `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`] |
| `Observed reading / verbal surface t0` | latent verbal profile, test design, early environment, selection | early-school bridge, later relative math-vs-verbal geometry | reading, passage comprehension, letter-word, `PPVT`, mean-verbal anchors | child aligned math-minus-verbal surfaces are male-leaning under most anchors: `PSID CDS pooled mean_verbal d = -0.388`, `NLSCYA pooled mean_verbal d = -0.121`, `FFCWS applied_minus_mean_verbal beta = -0.031`; `PPVT` is the unstable anchor | `Hardened` | the project now has enough child verbal anchors to stop treating reading alone as the bridge; `PPVT` remains the weak exception [SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_models.tsv`; `research/iq-sex-differences-child-bridge-multi-anchor.md`] |
| `Observed math / quantitative surface t0` | latent quantitative profile, test design, early environment, selection | early-school divergence, later pipeline | child applied problems / broad math surfaces | public child branch now points in one direction after alignment, not two. Raw `NLSCYA` was the anomaly; aligned child residuals are male-leaning across `ECLS`, `PSID CDS`, and most `NLSCYA` anchors | `Hardened` | the old sign conflict is basically dead on the aligned child surface; remaining disagreement is magnitude and anchor choice, not direction [SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`; `research/iq-sex-differences-psid-cds-first-pass.md`; `research/iq-sex-differences-child-bridge-rank-sensitivity.md`] |
| `EarlySchoolEmergence` | child verbal/math surfaces, school context, sex | later school math pipeline | `ECLS-K`, `ECLS-K:2011`, `NLSCYA`, `PSID CDS` | the local child branch is not one raw coefficient, but broad school-entry math is near parity or modestly male early and more male later in both `ECLS` cohorts, while aligned child `math minus verbal` surfaces are male-leaning across all public child cohorts | `Hardened` | this is now a real node, not a late-school artifact. The remaining issue is psychometric refinement, not existence [SOURCE: `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`; `research/iq-sex-differences-eclsk-early-school-first-pass.md`; `research/iq-sex-differences-child-bridge-rank-sensitivity.md`] |

---

## 3. School Pipeline Nodes

| Node | Main parents | Main children | Main observed proxies | Example local coefficients we have | Status | Current read |
|------|--------------|---------------|------------------------|------------------------------------|--------|--------------|
| `School evaluation / grades / recommendations` | sex, background, school context, behavior/compliance, transcript exposure | transcript progression, attainment | math GPA, English GPA, recognition, recommendations, honors | `Add Health`: `female -> math_grade_points = +0.226`, `english_grade_points = +0.353`; school-wedge family summary: `gpa mean beta = +0.256`, `evaluation mean beta = +0.127`; `PSID TAS`: `hs_gpa_norm d = +0.289`, `college_gpa_norm d = +0.383` | `Hardened` | strongest stable female-leaning late-school family in the repo [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_models.tsv`; `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`] |
| `Transcript exposure / course ladder / credits` | evaluation, school context, early-school divergence, track | school-knowledge accumulation, attainment | transcript math credits, ladder, high-course indicators | school-wedge family summary: `transcript_quantity mean beta = +0.068`, `transcript_academic_quantity = +0.193`; but older `NELS` says transcript quantity is near neutral compared with evaluation surfaces | `Live` | real node, but less stable than grades/evaluation. This is one reason “girls just take more math” is too simple [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `research/iq-sex-differences-nels-wedge-first-pass.md`] |
| `Track selection / advanced participation` | background, school context, evaluation, transcript exposure, early-school divergence | advanced tested surfaces, later field choice | `precalc_plus`, `algebra II+`, `trig/precalc/calc`, advanced-track membership | school-wedge family summary: `track mean beta = +0.045`; `HSLS` and `ELS` both show female-leaning advanced-course reach conditional on baseline surfaces | `Live` | stable enough to keep, but not interchangeable with transcript quantity or grades [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `research/iq-sex-differences-hsls-wedge-first-pass.md`; `research/iq-sex-differences-els-wedge-first-pass.md`] |
| `Observed school-knowledge test` | school-knowledge accumulation, test design, sex, selection | field choice, attainment | `Math Knowledge`, school-knowledge-heavy item families | school-wedge family summary: `tested_math_knowledge mean beta = +0.167`; in same-cohort `NLSY97`, the female anomaly localizes here, not in `PIAT` or `Arithmetic Reasoning` | `Hardened` | this is the cleanest current late-school anomaly node [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`] |
| `Observed applied / reasoning test` | latent quantitative/spatial profile, test design, track, selection | field choice, attainment | `PIAT Math`, `Arithmetic Reasoning`, broad standardized math, `SAT math`, `ACT`, `TIMSS Advanced reasoning` | school-wedge family summary: `tested_math mean beta = -0.053`; `PSID TAS`: `sat_math d = -0.355`, `act_composite d = -0.119`; `PSID TAS` family FE `sat_math_minus_reading_z beta_female = -0.423` | `Hardened` | stable male or null family overall, and notably different from the school-knowledge and evaluation families [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_family_fe.tsv`] |

---

## 4. Transition And Outcome Nodes

| Node | Main parents | Main children | Main observed proxies | Example local coefficients we have | Status | Current read |
|------|--------------|---------------|------------------------|------------------------------------|--------|--------------|
| `Field / major / occupation / adult use` | grades, transcript exposure, track, tested surfaces, background | adult accumulation, attainment | college years, attainment, broad field/occupation proxies | public-use branch is partial, but `Add Health` and `FFCWS` already show that school/evaluation and early-child test surfaces relate differently to later attainment | `Live` | important node, but still undermeasured on the current public stack. This is where restricted transcript/process access or better later outcomes matter most [SOURCE: `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-restricted-data-plan.md`] |
| `Adult accumulation / use-dependent amplification` | field/occupation/adult use, background | adult numeracy, attainment | age-band and occupation-group variation in adult numeracy | in `PIAAC`, male numeracy remains across age bands and broad occupation groups; the current read is that age/occupation amplify rather than create the adult numeracy pattern | `Live` | plausible amplifier, not yet isolated as an independently estimated causal coefficient [SOURCE: `research/iq-sex-differences-piaac-age-occupation.md`] |
| `Observed adult numeracy / adult tested surfaces` | adult accumulation, prior tested surfaces, test design | attainment | `PIAAC numeracy`, `SAT math`, `ACT`, `PSID TAS` aligned transition surfaces | `PIAAC` remains male-leaning across country, education, age, and occupation cells; `PSID TAS` keeps male-leaning `SAT math` and female-leaning GPA surfaces in the same transition panel | `Hardened` | real node, but not evidence by itself of a battery-invariant male `g` gap [SOURCE: `research/iq-sex-differences-piaac-frontier.md`; `research/iq-sex-differences-piaac-age-occupation.md`; `research/iq-sex-differences-psid-tas-transition-first-pass.md`] |
| `Attainment / later outcomes` | background, grades/evaluation, tested surfaces, transcript exposure, field/use | terminal observed outcome in the current DAG | college years, educational attainment | `Add Health`: female `h4ed2` `+0.601 -> +0.422` after `PVT + grades`; `FFCWS`: female `college_years` `+0.637 -> +0.625` after the Year 9 battery | `Hardened` as an observed surface, `Open` as a mechanism endpoint | current public outcome branch says adolescent school/evaluation accumulation and early-child cognition are not the same thing. It does **not** yet identify mediation cleanly [SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_attainment_decomposition.tsv`; `research/iq-sex-differences-mediator-design.md`] |
| `Residual latent general-ability gap` | hypothetical common cause behind multiple observed surfaces | many observed score families | no direct public proxy | no battery-invariant local coefficient exists. This is exactly the claim that remains unresolved after the earlier nodes are separated out | `Open` | still the final open question, not the starting premise [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-decisive-causal-tree.md`] |

---

## 5. Bottom Line

The main operational takeaway is simple:

1. the repo now has actual coefficients for several **observed families**
2. the repo does **not** yet have one coefficient for each **causal node**
3. the strongest estimated families are:
   - female-leaning `evaluation / GPA`
   - male-leaning `applied / reasoning / adult numeracy`
   - female-leaning localized `school-knowledge`
4. the strongest unresolved object is still the residual battery-invariant `g` claim

[INFERENCE]


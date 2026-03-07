# IQ Sex Differences - Frontier Literature Audit

**Question:** are the newest papers already seeing the same thing this repo is seeing, or is the repo surfacing a genuinely under-integrated pattern?

**Tier:** Deep  
**Date:** 2026-03-05

---

## Ground Truth

What the local project already knows:

1. the disagreement is surface-dependent, not battery-invariant
2. the `NLSY97` female-looking quantitative signal is concentrated in `Math Knowledge`, not `PIAT Math` or `Arithmetic Reasoning`
3. `HSLS` shows a grade/test wedge in math
4. `TIMSS` broad school math and `TIMSS Advanced` behave differently
5. the first `PISA 2018` pass suggests broad male-leaning math with heterogeneous item surfaces, but not a simple time/visit-burden explanation

[SOURCE: `research/iq-sex-differences-current-position.md`]

---

## Evidence Recital

The recent literature I actually found and checked breaks into three strands:

### 1. Measurement / process / invariance

1. `Giofrè et al. 2024` used the nonverbal `Leiter-3` and reported similar male and female general cognitive capacity, with specific male advantages on some spatial-manipulation tasks and female advantages on nonverbal Stroop / attention-control tasks. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/]
2. `Rodríguez-Cancino & Concha-Salgado 2023` reported full sex invariance on the `WISC-V` in their Chilean sample, while noting prior studies that found only partial scalar invariance in some sex comparisons. [SOURCE: https://www.mdpi.com/2079-3200/11/9/180]
3. `Stoevenbelt et al. 2023` argued that strict time limits can inflate male-favoring math gaps: in their timed mathematics data, they found larger gender differences on the latent completion factor than on latent mathematics ability. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC10311959/]
4. `Leng et al. 2024` used `TIMSS 2019` response-process data and found boys responded faster on average than girls across 10 countries, with moderate to strong negative correlations between mathematics ability and response speed. [SOURCE: https://www.ilsa-gateway.org/papers/examining-gender-differences-timss-2019-using-multiple-group-hierarchical-speed-accuracy]
5. `Li et al. 2024` used `PIAAC 2012` numeracy process data to interpret gender DIF and concluded that timing and action-sequence features helped explain subgroup behavior differences on DIF items; they explicitly warn that process differences can affect fairness and interpretation. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/]

### 2. School pipeline / grade-test wedge / labels / beliefs

1. `Adamecz et al. 2025` found that objective math ability explains only a small share of the gender gap in math self-assessment, with parental overestimation of boys and underestimation of girls explaining a large share of the self-assessment gap. [SOURCE: https://link.springer.com/article/10.1007/s00148-025-01087-2]
2. `García-Echalar, Poblete, and Rau 2024` found teacher value-added helped reduce the math test-score gender gap in Chile by about `16.9%`, with larger reductions in some subgroups and with female math teachers. [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0927537124000836]
3. `Ugalde 2025` found standardized proficiency labels affected women’s advanced math enrollment decisions but did not change men’s advanced-course decisions. [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0167268125001969]
4. `Chen et al. 2024` used `HSLS:09` and found gender-ability stereotypes, attainment values, and course-taking patterns jointly predicted later computing-major choice. [SOURCE: https://ideas.repec.org/a/spr/reihed/v65y2024i8d10.1007_s11162-023-09751-w.html]

### 3. Developmental timing / broad school math / track-like divergence

1. `Martinot et al. 2025` reported that boys and girls entered first grade with nearly identical math scores in France, but a male-favoring gap became highly significant after four months of schooling and reached about `0.20 SD` after one year; the authors argue the gap increased with schooling rather than age. [SOURCE: https://pubmed.ncbi.nlm.nih.gov/40500443/]
2. `Kuhfeld & Burchinal 2025` reported that girls no longer start kindergarten ahead in math and that boys pull ahead during elementary school, in a large U.S. assessment dataset. [SOURCE: https://edworkingpapers.com/ai25-1297]
3. `Balducci et al. 2025` found in `PISA` that mathematics is more likely to be an intraindividual strength for boys than girls across achievement levels, while reading is more likely to be an intraindividual strength for girls. [SOURCE: https://icajournal.scholasticahq.com/article/146580-the-stem-conundrum-sex-differences-in-intraindividual-academic-strengths-and-the-gender-equality-paradox-across-academic-achievement-levels]

---

## Executive Verdict

1. The frontier literature is already seeing the **pieces** of the repo’s causal tree.
2. It is **not** already presenting those pieces as one integrated cross-battery explanation very often.
3. The strongest recent support for the repo is that measurement/process, school-linked beliefs/evaluation, and developmental timing all matter, but they are mostly studied in separate silos.
4. The strongest recent challenge to the repo is `Martinot et al. 2025`: the school-related male-favoring math gap can open extremely early, so a pure late-school `Math Knowledge` story is too narrow.
5. The strongest recent constraint on overclaiming is that some modern batteries do show sex invariance and still yield null general-ability differences with specific subtest differences; so “it’s all measurement artifact” is too strong.
6. The repo’s genuinely useful candidate insight is the integrated one: `school-knowledge / transcript / labels / self-concept` surfaces may form one family, while `applied / reasoning / advanced-track` surfaces form another.
7. I did **not** find a 2023-2025 paper that cleanly tests that exact family split across multiple batteries and developmental stages.

---

## Claims Table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | Recent psychometric papers still tend to report null overall sex differences in general cognition with specific subtest differences rather than a large universal gap. | `Leiter-3` nonverbal battery found similar general capacity with specific male spatial and female attention-control differences. | High | https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/ | VERIFIED |
| 2 | Measurement invariance is live in the recent literature, but results vary by battery and sample. | `WISC-V` Chile study found full sex invariance; prior cited studies found only partial scalar invariance in some groups/subtests. | High | https://www.mdpi.com/2079-3200/11/9/180 | VERIFIED |
| 3 | Timing and response-process effects are an active recent explanation for observed gender gaps in math testing. | Timed math tests can show larger completion-factor gaps than latent ability gaps; TIMSS and PIAAC process-data papers use speed/revisits/DIF interpretation directly. | High | https://pmc.ncbi.nlm.nih.gov/articles/PMC10311959/ ; https://www.ilsa-gateway.org/papers/examining-gender-differences-timss-2019-using-multiple-group-hierarchical-speed-accuracy ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/ | VERIFIED |
| 4 | School-linked beliefs, assessments, and labels are active channels in recent research, not just downstream trivia. | Parent/teacher assessment bias, teacher VA, and performance labels all shift math-related perceptions or pathways. | High | https://link.springer.com/article/10.1007/s00148-025-01087-2 ; https://www.sciencedirect.com/science/article/abs/pii/S0927537124000836 ; https://www.sciencedirect.com/science/article/abs/pii/S0167268125001969 | VERIFIED |
| 5 | Recent developmental work suggests a male-favoring school-math gap can emerge very early, after school entry. | Nature 2025 French data show near-zero gap at school entry and ~0.20 SD male-favoring gap after one year. | High | https://pubmed.ncbi.nlm.nih.gov/40500443/ | VERIFIED |
| 6 | The frontier literature mostly studies measurement/process, school-pipeline, and developmental/track patterns separately rather than in one integrated model. | Direct inference from the paper set retrieved across three search axes. | Medium | [INFERENCE from the sources above] | INFERENCE |
| 7 | The repo’s current integrated “surface-family” hypothesis is under-articulated in the recent literature. | I did not find a recent paper explicitly linking `Math Knowledge`-like surfaces, transcript wedges, `TIMSS knowing`, and advanced-track divergence in one empirical program. | Medium | [INFERENCE from the search log below] | INFERENCE |

---

## What The Frontier Already Knows

### 1. Measurement and process can distort apparent sex differences

That is not a novel repo insight.

Recent papers already argue that:

1. strict timing can create larger sex gaps on completion/speed than on latent math ability [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC10311959/]
2. response speed and revisit behavior differ by sex in `TIMSS 2019` process data [SOURCE: https://www.ilsa-gateway.org/papers/examining-gender-differences-timss-2019-using-multiple-group-hierarchical-speed-accuracy]
3. DIF interpretation improves when process data are brought in, because behavior differences can drive apparent item unfairness [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/]

So the repo is **not ahead** merely by saying “measurement surface matters.”

### 2. School-linked surfaces are not clean ability proxies

That is also not novel in isolation.

Recent papers already show:

1. boys’ and girls’ self-assessed math ability diverges more than their objective ability, and parent/teacher assessments matter [SOURCE: https://link.springer.com/article/10.1007/s00148-025-01087-2]
2. teacher effects can compress standardized math gaps [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0927537124000836]
3. test-score labels can change advanced-course enrollment for girls more than for boys [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0167268125001969]
4. stereotypes, identity, and course-taking move later computing choices in `HSLS` [SOURCE: https://ideas.repec.org/a/spr/reihed/v65y2024i8d10.1007_s11162-023-09751-w.html]

So the repo is **not ahead** merely by saying “school pipeline matters.”

### 3. Broad school math and later pathways differ over time

The recent developmental literature is moving here too.

Most importantly, `Martinot et al. 2025` shows the male-favoring school-math gap can open quickly after school entry rather than only late in schooling. [SOURCE: https://pubmed.ncbi.nlm.nih.gov/40500443/]

That means our current local story should not be too centered on high-school-only or transcript-only mechanisms.

---

## What The Repo May Actually Be Adding

The potentially frontier-adjacent contribution is **integration**:

1. psychometric papers study invariance, DIF, timing, and process inside one battery
2. education papers study grades, labels, aspirations, teachers, and course-taking
3. developmental papers study when gaps open
4. advanced/upper-tail papers study subject strengths or participation

But those literatures are usually not stitched into one causal tree.

The repo’s current best candidate for a genuinely useful synthesis is:

> there may be one family of `school-knowledge / transcript / labels / self-concept` surfaces, and a different family of `applied / reasoning / advanced-track` surfaces, with measurement/process effects modulating both

That exact cross-battery family split is **not something I found explicitly tested** in the recent papers above. [INFERENCE]

That is the part worth keeping and testing harder.

---

## What The Recent Papers Force Us To Learn

### 1. Add an early-school emergence node

The `Nature 2025` first-grade paper is a real update.

It says the search for mechanisms cannot begin only in adolescence or only with transcript/course variables. Some part of the divergence may already be emerging very early in schooling. [SOURCE: https://pubmed.ncbi.nlm.nih.gov/40500443/]

### 2. Do not overstate the “everything is measurement artifact” thesis

`Leiter-3` and `WISC-V` work show that some batteries can be sufficiently invariant by sex while still producing:

1. null general-ability differences
2. specific subtest/task differences

So the better thesis is:

- measurement issues are first-order
- but some stable task-specific differences remain even when measurement looks acceptable

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/ ; https://www.mdpi.com/2079-3200/11/9/180]

### 3. Keep labels, expectations, and self-concept inside the causal graph

The recent pipeline literature says these are not fluff variables.

They can plausibly alter:

1. advanced-course uptake
2. self-assessed competence
3. later major choice

even at similar measured ability levels. [SOURCE: https://link.springer.com/article/10.1007/s00148-025-01087-2 ; https://www.sciencedirect.com/science/article/abs/pii/S0167268125001969 ; https://ideas.repec.org/a/spr/reihed/v65y2024i8d10.1007_s11162-023-09751-w.html]

---

## Best Current Answer

No, the repo is probably **not** discovering that measurement/process matters, or that school-linked beliefs and labels matter, or that developmental timing matters. The frontier knows those pieces.

Yes, the repo may be onto a better **organizing structure** than most recent papers use:

1. separate surface families instead of talking about one “math gap”
2. separate broad-population school math from advanced-track math
3. connect psychometric process effects to school-pipeline wedges instead of treating them as unrelated subfields

That is a real intellectual step, but it is not yet a confirmed discovery. It is still a synthesis hypothesis.

The strongest candidate for “something the frontier is not yet saying cleanly” is:

> the `NLSY97 Math Knowledge` anomaly, the `HSLS` grade-test wedge, the `TIMSS knowing` shift, and the broad-vs-advanced divergence may all be manifestations of one broader school-surface family rather than contradictory evidence about latent general ability

That is plausible. It is **not yet proven**. [INFERENCE]

---

## Disconfirmation

Things in the recent literature that push back on the repo:

1. `Martinot et al. 2025` says the male-favoring math gap can emerge after only months of schooling, which weakens a purely late-school explanation. [SOURCE: https://pubmed.ncbi.nlm.nih.gov/40500443/]
2. `WISC-V` and `Leiter-3` work show we should not simply reclassify all sex differences as measurement contamination. [SOURCE: https://www.mdpi.com/2079-3200/11/9/180 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/]
3. `Teacher value-added` shows school factors can narrow gaps, not only enlarge them, so the school node should not be treated as one-directional “bias against girls” or “bias against boys.” [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0927537124000836]

---

## Search Log

### Axes used

1. psychometric / measurement / response-process
2. school-pipeline / grades / labels / self-assessment
3. developmental timing / school stage / advanced-track divergence

### Useful hits

1. `Leiter-3` 2024: general null, specific task differences
2. `WISC-V` invariance 2023: battery-level invariance by sex
3. `Stoevenbelt` 2023: timing/completion-factor gap
4. `Leng` 2024: TIMSS response speed/revisits
5. `Li` 2024: PIAAC process-based DIF interpretation
6. `Adamecz et al.` 2025: self-assessment and parent/teacher wedge
7. `García-Echalar et al.` 2024: teacher VA and math gap
8. `Ugalde` 2025: labels and advanced course enrollment
9. `Martinot et al.` 2025: first-grade emergence
10. `Kuhfeld & Burchinal` 2025: early-grade U.S. math pattern

### Noise or lower-value hits

1. blogs/substacks repeating old arguments without new evidence
2. preprints or fringe outlets on `g` that mostly recycle the same battery disputes
3. broad “gender and STEM” papers that do not distinguish test surface from school pipeline

### Main thing I did **not** find

I did not find a recent mainstream paper that explicitly integrates:

1. process/timing/DIF
2. transcript/grades/labels/self-concept
3. broad school math versus advanced-track math

into one cross-battery causal account.

That absence is not proof of novelty. It is a search result worth taking seriously.

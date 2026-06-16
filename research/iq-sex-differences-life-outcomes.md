# IQ Sex Differences - Life Outcomes And Criterion Validity

**Date:** 2026-03-11  
**Purpose:** answer a narrower question than the main psychometric memo: which cognitive components retain independent predictive value for later outcomes once broader ability and obvious schooling-shaped or clerical-speed confounds are taken seriously.

## Bottom Line

The best current answer is:

1. broad cognitive ability remains the strongest broad predictor of academic and work outcomes in the reviewed literature, not narrow clerical processing speed. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001; Nye et al. 2022, doi:10.1007/s10869-022-09796-1] [Grade: B1]
2. among broad specific abilities, `Gc` is the most consistent independent predictor of academic achievement, while `Gf` matters most for mathematics-heavy outcomes. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001] [Grade: B2]
3. within the speed family, domain-specific fluency measures survive better than general processing speed. Reading fluency and arithmetic fluency can add predictive value after broader cognitive controls; generic reaction-time or perceptual-speed style measures look weaker. [SOURCE: Cheng et al. 2022, doi:10.3390/jintelligence10010001; Ritchie et al. 2013, doi:10.1037/a0030820; Ritchie et al. 2015, doi:10.1037/a0038981] [Grade: B1]
4. for job performance, some narrow abilities do add incremental validity beyond `GMA`, including processing speed, but this is a task-performance and training-performance result, not a general earnings or life-success result. [SOURCE: Nye et al. 2022, doi:10.1007/s10869-022-09796-1] [Grade: B2]
5. in the current repo's public-use outcome branch, later attainment is more clearly linked to adolescent school-evaluation surfaces and to some tested math surfaces than to any generic clerical-speed measure. [SOURCE: `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-school-outcome-interactions.md`] [DATA]

The practical implication is narrow:

- current evidence does **not** support treating female-favoring clerical-speed gaps as a proxy for broad productivity or life-success advantages. [INFERENCE from the sources above] [Grade: B1]
- current evidence also does **not** support dismissing all speed measures as irrelevant, because some speed-like narrow abilities retain criterion validity in speed-rewarding task ecologies. [INFERENCE from Nye et al. 2022; Cheng et al. 2022] [Grade: B2]

## Evidence Recital

1. **Zaboski et al. 2018** meta-analyzed relations between CHC broad abilities and academic achievement and found that psychometric `g` had by far the largest relation across academic domains, typically explaining more variance than all broad abilities combined. Only `Gc` showed medium-to-large effects across achievement domains, while `Gf` was importantly related to mathematics. Most other broad abilities explained less than `10%` of the variance. [SOURCE: doi:10.1016/j.jsp.2018.10.001; accessible PDF: https://gwern.net/doc/iq/2018-zaboski.pdf] [Grade: B2]
2. **Ritchie et al. 2013** reported that education was associated with higher later-life IQ scores but not with faster cognitive processing speed on elementary measures such as reaction and inspection time in the Lothian Birth Cohort. [SOURCE: doi:10.1037/a0030820; PubMed: https://pubmed.ncbi.nlm.nih.gov/23276218/] [Grade: B2]
3. **Ritchie et al. 2015** found that education was associated with later cognitive test scores via direct effects on specific skills rather than via `g`, and they explicitly framed the earlier 2013 result as showing no relation of education to elementary processing-speed measures despite links to IQ-type scores. [SOURCE: doi:10.1037/a0038981; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC4445388/] [Grade: B2]
4. **Cheng et al. 2022** separated general processing speed from specific processing speed and found that, after controlling for age, gender, nonverbal matrix reasoning, spatial abilities, and visual attention, specific processing speed measures such as reading fluency and arithmetic fluency predicted later mathematics and language achievement, while general processing speed did not. Incremental `ΔR^2` values for the surviving specific-speed predictors were roughly `0.044` to `0.072` for later mathematics outcomes. [SOURCE: doi:10.3390/jintelligence10010001; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8788420/] [Grade: B2]
5. **Nye et al. 2022** meta-analyzed cognitive ability and job performance and found that narrow abilities added incremental validity beyond `GMA` for task performance (`ΔR^2 = 0.16`), training performance (`ΔR^2 = 0.33`), and organizational citizenship behavior (`ΔR^2 = 0.09`). In their SEM analyses, the narrow abilities with the weakest loadings on the general factor, especially general knowledge and processing speed, had some of the largest residual paths to job-performance outcomes after accounting for latent `GMA`. [SOURCE: doi:10.1007/s10869-022-09796-1; accessible PDF: https://gwern.net/doc/iq/ses/2022-nye-2.pdf] [Grade: B2]
6. In the repo's local public outcome work, `Add Health` grades strongly predict later attainment for both sexes with no clean evidence of weaker female returns, and `FFCWS` applied math is one of the strongest observed predictors of later college exposure. These results are not speed-centered and do not license a broad “clerical speed drives life outcomes” story. [SOURCE: `research/iq-sex-differences-school-outcome-interactions.md`; `research/iq-sex-differences-school-outcome-decomposition.md`] [DATA]

## Claim Table

| ID | Claim | Status | Confidence | Provenance |
| --- | --- | --- | ---: | --- |
| `LO1` | For broad academic outcomes, the strongest durable predictor remains overall cognitive ability rather than narrow clerical speed. | `supported` | `0.80` | Zaboski et al. 2018; Ritchie et al. 2015. [SOURCE: doi:10.1016/j.jsp.2018.10.001; doi:10.1037/a0038981] [Grade: B1] |
| `LO2` | `Gc` is the most consistent broad specific survivor for academic achievement; `Gf` survives mainly for mathematics-heavy outcomes. | `supported` | `0.78` | Zaboski et al. 2018. [SOURCE: doi:10.1016/j.jsp.2018.10.001] [Grade: B2] |
| `LO3` | Generic processing speed is weaker than domain-specific fluency once broader reasoning, spatial ability, and attention controls are included. | `supported` | `0.74` | Cheng et al. 2022; Ritchie et al. 2013; Ritchie et al. 2015. [SOURCE: doi:10.3390/jintelligence10010001; doi:10.1037/a0030820; doi:10.1037/a0038981] [Grade: B1] |
| `LO4` | Some narrow speed-related abilities still add predictive value for job performance beyond `GMA`, especially in task and training settings. | `supported` | `0.68` | Nye et al. 2022. [SOURCE: doi:10.1007/s10869-022-09796-1] [Grade: B2] |
| `LO5` | Direct evidence that generic processing speed independently predicts earnings or occupational status after childhood ability, education, and family controls is still thin in the reviewed open source base. | `open` | `0.60` | Current review found much stronger evidence for school achievement and job performance than for wages or status. [INFERENCE from the source base above] [Grade: B3] |
| `LO6` | Current evidence does not justify translating female clerical-speed advantages into a broad claim about who will do better in life. | `supported` | `0.77` | Supported by `LO1` through `LO5` plus the local public outcome branch. [INFERENCE from the sources above and local data] [Grade: B1] |

## Outcome Family By Outcome Family

### 1. Academic achievement and attainment

The academic-outcome literature is the clearest.

- `g` is strongest overall across academic domains. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001] [Grade: B2]
- `Gc` is the broad specific ability with the most stable independent academic relevance, especially for reading-heavy outcomes. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001] [Grade: B2]
- `Gf` matters most for mathematics, but not as a universal academic winner across all domains. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001] [Grade: B2]
- broad `Gs` does not emerge as the main survivor in that meta-analysis. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001] [Grade: B2]
- when speed survives, it is more often specific academic fluency: reading fluency and arithmetic fluency, not general speed. [SOURCE: Cheng et al. 2022, doi:10.3390/jintelligence10010001] [Grade: B2]

This matters for the repo because the female speed advantage is strongest on school-like clerical tasks. The current academic-validity literature implies that the broad survivor is not generic clerical speed but the more content-linked school and knowledge surfaces. [INFERENCE] [Grade: B2]

### 2. Job performance

The job-performance literature is narrower but still useful.

- `GMA` remains a strong predictor of task and training performance. [SOURCE: Nye et al. 2022, doi:10.1007/s10869-022-09796-1] [Grade: B2]
- narrow abilities can add incremental validity over `GMA`, especially the narrow abilities least collinear with it. In the updated meta-analysis this included general knowledge, visual processing, and processing speed. [SOURCE: Nye et al. 2022, doi:10.1007/s10869-022-09796-1] [Grade: B2]
- the biggest incremental gains in that paper are for task performance, training performance, and `OCB`, not for a broad life-success criterion. [SOURCE: Nye et al. 2022, doi:10.1007/s10869-022-09796-1] [Grade: B2]

So the honest read is:

- processing speed is **not** useless
- but its surviving value appears task-ecology-specific
- that is a much narrower claim than “processing speed determines who succeeds in life”

[INFERENCE] [Grade: B2]

### 3. Earnings and occupational status

This is the weakest part of the source base reviewed here.

- the open, directly inspected literature in this pass gives much better evidence for academic achievement and job performance than for wages or occupational status
- the current repo also does not yet have a strong local direct test of `clerical_speed -> earnings` after broader controls

So the current answer for wages and status is not “no effect.” It is “not demonstrated cleanly here.” [INFERENCE] [Grade: B3]

## What The Local Repo Adds

The current repo does not directly solve the full criterion-validity question, but it already sharpens it in one important way:

- in `Add Health`, grade and evaluation surfaces predict later attainment for both sexes and do not show the simple “female school surfaces are inflated and low-value” footprint [SOURCE: `research/iq-sex-differences-school-outcome-interactions.md`] [DATA]
- in `FFCWS`, applied math is one of the strongest observed predictors of later college years, while the female later-college residual survives the Year 9 battery [SOURCE: `research/iq-sex-differences-school-outcome-decomposition.md`] [DATA]

That makes the criterion-validity map more plural:

1. broad school-evaluation surfaces matter
2. some tested math surfaces matter
3. generic clerical speed has not earned the right to stand in for either one

[INFERENCE] [Grade: B2]

## Causal Check

> **Observation:** female advantages are most stable on clerical-speed style tasks, but the criterion-validity literature reviewed here does not show that generic clerical speed is the main surviving predictor of broad later outcomes once broader cognitive controls are included. The strongest survivors are broader ability, `Gc`, some `Gf`, school-evaluation surfaces, and task-specific fluencies. [SOURCE: Zaboski et al. 2018, doi:10.1016/j.jsp.2018.10.001; Cheng et al. 2022, doi:10.3390/jintelligence10010001; Nye et al. 2022, doi:10.1007/s10869-022-09796-1; `research/iq-sex-differences-school-outcome-decomposition.md`; `research/iq-sex-differences-school-outcome-interactions.md`] [Grade: B1]
>
> **Null:** if clerical-speed gaps were mostly a broad productivity channel, generic speed measures should retain strong, cross-domain predictive value for later school, work, earnings, and status outcomes after broader ability controls. [INFERENCE] [Grade: B2]
>
> **Residual after null:** the reviewed evidence instead points to domain-specific fluency, broader knowledge, and broader reasoning as the more durable survivors. Processing speed still matters in some job and training ecologies, but not as a universal criterion-validity champion. [INFERENCE] [Grade: B1]

- `P(cause)`: `0.70` that the broad criterion-validity story is carried more by general ability, `Gc`, `Gf`, and school-evaluation accumulation than by generic clerical processing speed. [INFERENCE] [Grade: B1]
- `Top alternative`: `0.20` that processing speed is more generally important, but the current psychometric measures are too contaminated by literacy and motor demands to show its real generality. [INFERENCE] [Grade: B2]
- `Falsifier`: a large longitudinal dataset where low-clerical, low-motor speed measures still predict earnings or occupational status strongly after childhood ability, education, family background, and literacy practice are held fixed. [INFERENCE] [Grade: B2]
- `Decision impact`: do not treat female clerical-speed findings as a shortcut to conclusions about broad life success. If the repo wants to argue practical consequence, the next valid targets are grades, tested math, transcript structure, and selective work/field outcomes, not generic symbol-search rhetoric. [INFERENCE] [Grade: B1]

## What This Changes

What hardens:

1. the criterion-validity question is separable from the psychometric sex-gap question
2. broad school and knowledge surfaces matter more for life-outcome claims than generic clerical speed does
3. the strongest current evidence for a surviving speed signal is task-specific fluency or specific job/task ecologies

What stays open:

1. whether low-clerical speed measures predict earnings or occupational status after the full control set
2. whether transcript-linked or restricted datasets would show that school-evaluation and tested-math surfaces have materially different later returns by sex
3. whether some occupation families reward speed enough that narrow female speed advantages matter materially there even if they do not generalize broadly

## Next Step

If the repo wants to push this question beyond synthesis, the highest-value next designs are:

1. a direct local `clerical_speed` outcome pass in `NLSY79` / `NLSY97` with explicit DAG discipline and a frozen control ladder
2. a restricted transcript/process design linking school-evaluation surfaces, tested math, and later selective outcomes
3. a direct comparison between low-clerical speed measures and school-like coding/fluency measures on the same later outcomes


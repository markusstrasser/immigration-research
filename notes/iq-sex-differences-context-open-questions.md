# IQ Sex Differences - Context, Confounding, and Life Outcomes

**Date:** 2026-03-05
**Status:** Scoping note for follow-up research
**Why this exists:** `research/iq-sex-differences-test-construction.md` asks what the tests are measuring. It does **not** settle what causes observed score differences or whether narrow score differences matter for real-world outcomes.

---

## Split The Question

The popular discussion usually collapses three different questions into one:

1. **Measurement question:** do male-female score differences change with battery construction?
2. **Causal question:** are the observed differences biological, socialized, practice-driven, schooling-driven, or some mixture?
3. **Practical-value question:** even if a narrow subability difference is real, does it matter for education, work, earnings, innovation, leadership, or family formation?

These should be kept separate. The current repo memo mainly answers **Question 1**. The next stage should answer **Questions 2 and 3**.

---

## Question A - How To De-Confound Schooling, Attention, and Practice

### Observation

Education explains much more variance than sex in at least one WAIS-IV sample, and one of the clearest female advantages appears on school-like timed symbol / coding tasks rather than on every conceivable speed measure. [SOURCE: Daseking et al. 2017, doi:10.1016/J.PAID.2017.04.003; Roivainen 2011, cited in `research/iq-sex-differences-test-construction.md`]

### Null

Part of the observed female advantage on coding / scanning style tasks could reflect schooling-linked practice, literacy volume, compliance with classroom-style task demands, or teacher-mediated reinforcement rather than a broad underlying speed factor. [INFERENCE]

### What Would Actually Discriminate Causes

1. **Pre-literacy / preschool samples.**
   If the same gap appears before sustained schooling, the schooling explanation weakens.

2. **Within-family designs.**
   Opposite-sex siblings, twins, and adoption designs reduce family-level confounding.

3. **Natural experiments in schooling exposure.**
   School-entry cutoff rules, compulsory-schooling reforms, or policy changes can test whether more schooling shifts the gap.

4. **Task decomposition within the same people.**
   Compare:
   - reaction time
   - pencil-and-paper coding / symbol search
   - untimed reasoning
   - literacy-heavy scanning tasks

   If the female advantage is large on school-like clerical tasks but absent on low-schooling reaction-time tasks, that supports a training / task-format explanation more than a general speed-factor explanation. [INFERENCE]

5. **Mediator measurement.**
   Measure reading volume, handwriting or keyboard fluency, grades, teacher ratings, homework time, and classroom behavior, then test whether these mediate the gap.

6. **Item-level DIF and measurement invariance.**
   Before making causal claims, confirm the test is measuring the same latent trait in both groups.

### Shape-Constrained Predictions

If schooling / practice is a major driver, we should expect:

- bigger female advantages on clerical, scanning, coding, and fluency tasks than on reaction-time tasks
- cross-national variation tracking school regime or literacy practice
- attenuation of the gap after controlling for education-related mediators

If a broad biological speed factor is the main driver, we should expect:

- the same direction across reaction time, coding, and non-schooled samples
- much less sensitivity to schooling intensity or literacy practice

### Current Lean

**Most likely cause (60%):** some observed sex differences, especially in processing-speed style tasks, are at least partly task-format and schooling-practice effects rather than clean readouts of a general speed factor. [INFERENCE]

**Top alternative (25%):** a broader biological speed factor explains most of the female advantage, and schooling only modulates its expression. [INFERENCE]

**Falsifier:** large pre-school or low-schooling samples showing the same female advantage across both reaction-time and clerical processing-speed measures. [INFERENCE]

**Decision impact:** do not treat "female advantage on coding/symbol search" as equivalent to "female advantage in economically meaningful productivity" without a separate criterion-validity argument. [INFERENCE]

---

## Question B - Does Processing Speed Matter For Success In Life?

### Core point

A mean difference on a psychometric subtest does **not** automatically imply a meaningful difference in real-world productivity, status, or long-run success. That requires separate evidence on **criterion validity**. [INFERENCE]

### Why this is a different research question

The existing memo is about **test-score structure**. The life-outcome question is about whether a narrow ability has incremental predictive value for:

- earnings
- occupational complexity
- promotions
- academic completion
- entrepreneurship
- patents / publication
- leadership
- household stability

after controlling for broader ability, education, family background, personality, and domain skill. [INFERENCE]

### Likely popular-culture error

Popular discourse often moves from:

`processing-speed difference -> intelligence difference -> productivity difference -> life-success difference`

That chain is usually asserted, not demonstrated. Each arrow needs evidence. [INFERENCE]

### What the next agent should test

1. Does processing speed predict life outcomes **after** controlling for:
   - general cognitive ability
   - education
   - socioeconomic background
   - conscientiousness / self-control
   - occupation / industry

2. Are any sex differences in processing speed large enough to matter at the **tails**, not just at the mean?

3. Is the predictive value concentrated in specific task ecologies:
   - clerical work
   - inspection / monitoring
   - test-taking
   - air-traffic-control style environments

   rather than in most knowledge work?

4. Do spatial / mechanical differences have more occupational consequence than processing-speed differences in technical fields?

### Current Lean

**Most likely conclusion (70%):** narrow score differences in processing speed are psychometrically real but often over-interpreted in public debate. Their practical importance probably depends heavily on the task ecology and may be small once broader ability, education, and non-cognitive traits are controlled. [INFERENCE]

**Top alternative (20%):** processing speed has large independent economic relevance across many modern occupations and has been systematically underestimated in public debate. [INFERENCE]

**Falsifier:** strong longitudinal evidence showing that processing speed retains large independent effects on earnings or occupational status after standard controls. [INFERENCE]

**Decision impact:** do not use processing-speed findings as a proxy for "who will do better in life" until the criterion-validity literature is reviewed directly. [INFERENCE]

---

## Suggested Sorting

Keep the files split like this:

- `research/iq-sex-differences-verification.md`
  The evidence audit of what the current memo gets right and wrong.
- `notes/iq-sex-differences-context-open-questions.md`
  The scoping note for causal confounding and life-outcome relevance.

If the next agent does a full literature review on the life-outcomes question, promote it to:

- `research/iq-sex-differences-life-outcomes.md`

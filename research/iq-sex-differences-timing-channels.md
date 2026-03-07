# IQ Sex Differences - Timing Channels, Spatial Tasks, and Processing Speed

**Date:** 2026-03-05
**Question:** Were processing-speed components or timing rules added to broad intelligence batteries in order to "even out" male advantages on spatial tasks?

---

## Short Answer

There is **no direct evidence** in the official test-development material that processing-speed components or timing rules were added to equalize male-female outcomes. The official rationale is psychometric and theoretical: better discrimination among higher-ability examinees, updated factor structure, and broader construct coverage. [SOURCE: Pearson WAIS-IV Q&A, https://www.pearsonassessments.com/store/en/usd/p/100000392.html; Pearson WAIS-IV introduction slides, https://www.pearsonclinical.asia/content/dam/school/global/clinical/us/assets/wais-iv/presentation-introducing-the-wais-iv.pdf]

More importantly, the observed data do **not** behave like a generic female-favoring "speed correction." In the WAIS standardization samples already extracted in this repo, **speeded spatial / fluid tasks remain male-favoring and are often more male-favoring than Matrix Reasoning**, which is less tightly speeded. [SOURCE: `sources/iq-sex-diff/timing_channel_analysis.py`; van der Sluis et al. 2006; Pezzuti et al. 2020; Daseking et al. 2017]

---

## What Those Numbers In The Script Actually Are

The values like:

- `matrix_reasoning = -0.157`
- `Coding = 0.285`
- `Visual Puzzles = -0.315`

are **not design coefficients chosen by the test maker**. They are **observed effect sizes** (`Cohen's d`) computed from the published male and female means and standard deviations in norm samples or extracted from papers that already reported equivalent statistics. [SOURCE: Daseking et al. 2017, Table 3, doi:10.1016/J.PAID.2017.04.003; `sources/iq-sex-diff/german_wais4_effects.py`]

What test designers actually choose is:

1. which subtests are included
2. whether a subtest has a time bonus or a strict time limit
3. how raw scores are transformed to scaled scores in the **overall** norm sample
4. how much each subtest contributes to composites like FSIQ

[SOURCE: Pearson WAIS-IV product page; Pearson WAIS-IV Q&A]

So the script is measuring the consequences of those design choices in real samples. It is not reproducing the design choices themselves. [INFERENCE]

---

## Why "Mean 100" Is Not A Tautology

Yes, IQ composites are normed to have a mean of about `100` in the **overall standardization sample**. But that does **not** force every subgroup to have a mean of `100`.

The German WAIS-IV norm data show this directly:

- male `FSIQ = 101.61`
- female `FSIQ = 98.45`
- male `PSI = 98.26`
- female `PSI = 101.55`

[SOURCE: Daseking et al. 2017, Table 3, doi:10.1016/J.PAID.2017.04.003]

Using the male and female subgroup sizes from the same table, the weighted overall FSIQ mean is still about `99.96`, which is the point of norming. The subgroup means remain different. [SOURCE: Daseking et al. 2017, Table 3; calculation reproduced locally]

If subgroup equality were built in mechanically, those subgroup means would also be equal. They are not. Standardization fixes the **overall scale**, not equality between male and female groups. [INFERENCE]

---

## What The Official Test Materials Say

### WAIS-IV

Pearson's official WAIS-IV FAQ says:

1. **Block Design keeps time bonus points because higher-ability examinees tend to perform the task faster.** Without the bonus, the subtest loses discrimination at higher ability levels. [SOURCE: Pearson WAIS-IV Q&A, lines 762-765 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
2. **Visual Puzzles and Figure Weights have strict time limits for the same reason**: higher-ability examinees solve them faster, and with enough time lower-ability examinees can eventually get some items right. [SOURCE: Pearson WAIS-IV Q&A, lines 766-768 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
3. **Matrix Reasoning only has a 30-second guideline, not a strict limit,** because extra time generally does not convert low-ability responses into correct ones. [SOURCE: Pearson WAIS-IV Q&A, lines 766-768 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
4. **WAIS-IV deliberately increased the contribution of Processing Speed to the FSIQ** relative to WAIS-III, but the stated reason is a revised conception of intelligence and four-factor structure, not sex balancing. [SOURCE: Pearson WAIS-IV product page, lines 673-675 and 742-746 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
5. The WAIS-IV development slides say the revision **reduced emphasis on time bonus** and added a **Block Design No Time Bonus (BDN)** process score. [SOURCE: Pearson WAIS-IV introduction slides, lines 33-34 and 128-130 at https://www.pearsonclinical.asia/content/dam/school/global/clinical/us/assets/wais-iv/presentation-introducing-the-wais-iv.pdf]

### ASVAB

The official ASVAB technical bulletin says the ASVAB subtests are designed as **power subtests, not speeded subtests**, and that the time limits are set so that **virtually all examinees can finish**. [SOURCE: ASVAB Technical Bulletin No. 4, lines 424-429 at https://www.officialasvab.com/wp-content/uploads/2019/08/asvab_techbulletin_4.pdf]

That matters because it means a timed test is not automatically a speed-dominated test. Some batteries use liberal time limits to preserve "best performance" rather than to reward fast responding directly. [INFERENCE]

---

## Direct Answer To The User's Example

If you solve a spatial item early, whether that improves your score depends on the subtest:

1. **Block Design:** yes, speed can increase the score because time bonus points exist. [SOURCE: Pearson WAIS-IV Q&A, lines 762-765 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
2. **Visual Puzzles / Figure Weights:** yes, speed matters because these have strict time limits. [SOURCE: Pearson WAIS-IV Q&A, lines 766-768 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
3. **Matrix Reasoning:** mostly accuracy, not bonus speed. There is a 30-second guideline, but extra time may be allowed for delayed correct responses. Finishing far earlier does not itself add points. [SOURCE: Pearson WAIS-IV Q&A, lines 766-768 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]
4. **ASVAB-type power subtests:** speed is less central because time limits are intentionally liberal. [SOURCE: ASVAB Technical Bulletin No. 4, lines 424-429 at https://www.officialasvab.com/wp-content/uploads/2019/08/asvab_techbulletin_4.pdf]

So the answer is **not** "speed never matters" and **not** "all spatial tasks are secretly processing-speed tasks." It varies by subtest design.

---

## Repo Analysis I Ran

I used the extracted effect sizes already in this repo and compared:

- **Matrix Reasoning** as the less speeded comparison point
- **speeded spatial / fluid tasks**: Block Design, Visual Puzzles, Figure Weights
- **clerical processing-speed tasks**: Coding, Symbol Search, Cancellation / Digit-Symbol

The script is here: `sources/iq-sex-diff/timing_channel_analysis.py`

### Result

Across the Dutch WAIS-III, Italian WAIS-IV, and German WAIS-IV samples:

- Matrix Reasoning mean effect: about `d = -0.18` (male advantage)
- Speeded spatial / fluid mean effect: about `d = -0.29` (larger male advantage)

Within each study, the speeded spatial / fluid tasks were **more male-favoring** than Matrix Reasoning:

- Dutch WAIS-III: contrast `-0.06`
- Italian WAIS-IV: contrast `-0.11`
- German WAIS-IV: contrast `-0.11`

[SOURCE: `sources/iq-sex-diff/timing_channel_analysis.py`]

This is the opposite of what we would expect if timing inside spatial tasks were mainly acting as a female-favoring equalizer. [INFERENCE]

---

## Additional Check: FSIQ Versus GAI

In the German WAIS-IV sample, the male advantage was:

- **FSIQ:** 3.16 IQ points
- **GAI:** 4.07 IQ points

GAI excludes Working Memory and Processing Speed, so the smaller male advantage on FSIQ is consistent with PSI pulling the overall composite somewhat toward females. [SOURCE: Daseking et al. 2017, Table 3, doi:10.1016/J.PAID.2017.04.003]

But this still does **not** show that PSI was added for sex balancing. It only shows that including PSI changes the composite. The official documentation says the reason was a revised intelligence model and test-design logic. [SOURCE: Pearson WAIS-IV product page, lines 673-675 and 742-746 at https://www.pearsonassessments.com/store/en/usd/p/100000392.html]

---

## Causal Check

**Observation:** Explicit processing-speed subtests sometimes pull broad composites toward females, but speeded spatial / fluid subtests do not become female-favoring; they remain male-favoring and often more strongly so than Matrix Reasoning. [SOURCE: Pearson WAIS-IV Q&A; `sources/iq-sex-diff/timing_channel_analysis.py`]

**Null:** Timing was included to improve psychometric discrimination and capture constructs the test designers regarded as part of intelligence, not to engineer sex parity. [SOURCE: Pearson WAIS-IV Q&A; Pearson WAIS-IV product page]

**Residual after null:** Increasing the weight of Processing Speed in FSIQ can incidentally reduce an otherwise male-favoring composite gap. [SOURCE: Pearson WAIS-IV product page; Daseking et al. 2017]

**Geometry:** mixed pattern, not a universal directional shift. Female advantages cluster in clerical naming/coding/scanning tasks, not in speeded tasks of every kind. [SOURCE: Roivainen 2011, doi:10.1016/J.LINDIF.2010.11.021]

**Most likely cause (75%):** WAIS timing rules and PSI inclusion reflect psychometric discrimination plus updated theory, with sex-difference consequences being incidental rather than the design objective. [INFERENCE]

**Top alternative (15%):** some revisions incidentally or implicitly favored female-leaning subtests enough that the practical effect resembles balancing, even if not stated explicitly. This is weaker because the official design documents do not mention sex balancing, and the speeded spatial tasks do not move in the female direction. [INFERENCE]

**Falsifier:** internal design documents or technical reports explicitly stating that PSI weighting or time-bonus structure was chosen to offset sex differences; or strong public data showing that removing time from spatial tasks eliminates the male advantage. [INFERENCE]

**Decision impact:** do not describe PSI or timed scoring as an intentional "girl-balancing mechanism." The better claim is narrower: some batteries include task types that favor females, which can shift the composite, but the effect is construct-specific and does not generalize to all speeded spatial tasks. [INFERENCE]

---

## Related Evidence On Untimed Mental Rotation

An older but directly relevant study tested whether male advantages in mental rotation disappear without time pressure. They did **not**: males still scored higher on an unspeeded Mental Rotations Test, so slower female responding was not a sufficient explanation of the gap. [SOURCE: Resnick 1993, PMID 8424863, https://pubmed.ncbi.nlm.nih.gov/8424863/]

That strengthens the conclusion above: removing time pressure does not obviously erase the spatial effect. [INFERENCE]

---

## Epistemic Limits

1. I did **not** locate a public raw item-level normative dataset for sex-by-time-limit analyses in WAIS or ASVAB.
2. The repo analysis therefore uses extracted study tables plus official test-development materials.
3. The strongest next step would be raw-data access to:
   - Block Design versus Block Design No Time Bonus by sex
   - PiCAT versus timed CAT-ASVAB by sex
   - item-level response times on Matrix Reasoning, Visual Puzzles, and Figure Weights

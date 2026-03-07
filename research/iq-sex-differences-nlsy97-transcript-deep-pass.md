# IQ Sex Differences - NLSY97 Transcript Deep Pass

**Date:** 2026-03-06
**Dataset:** `NLSY97` public-use respondent extract plus added `PIAT`, 1997 self-reported math-course flags, transcript math summaries, and school-offer fields
**Purpose:** test whether the late-school `NLSY97` anomaly survives after separating `design`, `course exposure`, `evaluation`, `school offer`, and `transcript destination` surfaces

---

## Question

Does the female-looking `NLSY97` quantitative signal disappear once late-school course and transcript surfaces are unpacked, or does it remain localized to `Math Knowledge` and school-linked outputs?

## Findings

1. The basic same-cohort split still holds. In the `PIAT` overlap sample, `PIAT Math` is slightly male-leaning (`d = -0.048`) and `Arithmetic Reasoning` is near-null to slightly male (`d = -0.036`), while `Math Knowledge` is female-leaning (`d = +0.141`) and transcript math GPA is more strongly female-leaning (`d = +0.222`). Transcript math credits are female-leaning too, though less strongly, and transcript advanced-math credits are only weakly female-leaning / near null (`d = +0.066`). [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_surface_gaps.tsv`]
2. Simple course-exposure stories do not explain the wedge. Relative to boys, girls are less likely to report `algebra2+` (`-0.143`), `precalc+` (`-0.169`), and `calc+` (`-0.200`) in the `PIAT` overlap sample. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_binary.tsv`]
3. The `Math Knowledge` wedge survives `PIAT` anchoring plus design and self-reported exposure blocks. In the overlap sample, the female coefficient on `Math Knowledge` is `+0.161` in the base same-sample model, `+0.188` after the design block, and `+0.167` after the exposure block. The corresponding `Quantitative` coefficient is `+0.085`, `+0.109`, and `+0.092`. `Arithmetic Reasoning` stays near zero in those same blocks. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`]
4. School-offer controls do not erase the wedge either. After adding transcript school-offer and program fields, the female coefficient remains `+0.148` on `Math Knowledge` and `+0.082` on `Quantitative`, while `Arithmetic Reasoning` stays near zero. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`]
5. Transcript destination controls shrink the composite but do not turn the localized split into a broad male advantage. In the destination-stress model, `Arithmetic Reasoning` turns male (`-0.077`), `Math Knowledge` stays female (`+0.136`), and the `Quantitative` composite falls to a small, non-significant female residual (`+0.033`). [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`]
6. Transcript outcomes themselves remain female-leaning after `PIAT` and design / exposure controls on much larger samples than the earlier evaluation-heavy slice. For example, `transcript_gpa_math_hstr ~ female + PIAT + design` gives `+0.259`, and `transcript_total_academic_math_hstr ~ female + PIAT + exposure` gives `+0.193`. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_transcript_models.tsv`]
7. The only place the wedge collapses cleanly is the evaluation-heavy block, but that block is too attrited to settle the mechanism. The progression sample drops from about `3,645-3,750` in the base / design / exposure models to `239` in `evaluation_stress`, and transcript-outcome models drop from roughly `1,568-2,500` to `125-183`. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_transcript_models.tsv`]
8. Transcript math-pipeline groups keep the wedge geometry alive. In the transcript-`advanced` pipe, `PIAT Math` and `Arithmetic Reasoning` are male-leaning (`-0.320`, `-0.278`), `Math Knowledge` is near parity (`+0.029`), and transcript math GPA is female-leaning (`+0.219`). In the `middle` pipe, `PIAT Math` and `Arithmetic Reasoning` are male-leaning, while `Math Knowledge` and transcript GPA remain female-leaning. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_by_mathpipe.tsv`]

## Interpretation

The late-school `NLSY97` anomaly survives the first real transcript pass, but not as a broad quantitative edge.

The current best description is:

- `Math Knowledge` stays female-leaning after `PIAT`, design, and self-reported course exposure
- `Arithmetic Reasoning` does not
- transcript math GPA and transcript math-credit surfaces stay female-leaning
- advanced transcript destinations shrink the composite residual but do not unify the surfaces

That is a stronger same-cohort case for a `school-knowledge / transcript / evaluation` family distinct from alternate tested-math surfaces.

It is **not** yet a clean mechanism result, because the one block that really collapses the wedge is also the one with the worst attrition and the most downstream evaluation variables.

## Causal Read

> **Observation:** in the same cohort, girls are not taking more advanced self-reported math in 1997, yet `Math Knowledge` and transcript math surfaces remain female-leaning relative to `PIAT Math` and `Arithmetic Reasoning`. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_binary.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`]
>
> **Null:** if the `NLSY97` sign flip is just broad latent quantitative ability, then once `PIAT` baseline, design, and course exposure are aligned, the female residual should mostly disappear across the math surfaces together. [INFERENCE]
>
> **Residual after null:** the wedge stays localized to `Math Knowledge` and transcript math outputs, while `Arithmetic Reasoning` does not move with it. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_transcript_models.tsv`]

- `P(cause)`: `0.72` that the late-school `NLSY97` anomaly is mainly a `school-knowledge / transcript / evaluation-family` wedge rather than a broad same-cohort female quantitative advantage. [INFERENCE]
- `Top alternative`: `0.18` that the current wedge is still mostly a behavior / compliance / observability story that the present transcript pass does not model cleanly enough. [INFERENCE]
- `Falsifier`: an external transcript-rich replication or same-cohort behavior-aware pass where `Math Knowledge`, transcript math GPA, and alternate tested-math surfaces all converge after adequate exposure and engagement adjustment. [INFERENCE]
- `Decision impact`: the next late-school step should separate `behavior / compliance` from `evaluation`, not reopen the already-weakened “girls simply took more advanced math” story. [INFERENCE]

## Data-Hygiene Note

One real transcript bug was fixed during this pass: `transcript_mathpipe_hstr` uses codes `100..800`, not `1..8`. The initial group-label map silently zeroed the grouped destination table and suppressed the destination-stress block. The current outputs are post-fix. [SOURCE: `sources/iq-sex-diff/nlsy97_transcript_deep_pass.py`; `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_diagnostics.tsv`]

## Outputs

- `sources/iq-sex-diff/nlsy97_transcript_deep_pass.py`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_extract.parquet`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_overlap_extract.parquet`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_surface_gaps.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_binary.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_by_mathpipe.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_by_highest.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_transcript_models.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_diagnostics.tsv`

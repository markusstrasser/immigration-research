# Brief: is women's pay less tied to skill? (NLSY97)

Operator, 2026-09-29, on ladder 272 (second-generation Hispanic daughters' pay gap to white women does not widen,
and is about zero at equal schooling): "well because women have fake jobs and is not related to skill".

## Hypothesis to test, steel-manned

Women, and Hispanic daughters especially, work more often in jobs where pay is set by credential schedules, union
or civil-service grades, or reimbursement rates rather than by output: government, public schools, hospitals and
health support, social services, administration. Such pay tracks measured skill less. So a zero or positive pay
gap for daughters at equal schooling or AFQT says little about skill.

Competing explanations to test against it:
- **Employment selection** (Neal and Johnson 1996, JPE 104(5)): fewer Hispanic daughters work, so the workers are
  positively selected. [TRAINING-DATA: verify the citation and the finding from a primary source before relying on it]
- **Place**: Hispanic daughters live in higher-wage metros (California, big Texas metros) than the average white woman.

## Starting point (do not redo)

`infra/immigration-fiscal/career_trajectories_2026_09_29/` (RESULT.md, analyze.py, extract.py). Generation groups
come from its parent linkage (`new_datasets_2026_09_17/derived/nlsy_family/family_analysis_rows.csv`, hash-pinned
in analyze.py). Its results: at equal AFQT the G2 Hispanic women's gap to G3+ NH white women is +0.113 (0.055)
at 25–27 and +0.093 (0.069) at 35–40. G2 Hispanic men: −0.047 → −0.041. At equal education, women's hourly
pay at 35–40 is +0.082 (0.044). **Positive control: your pipeline must reproduce the +0.113 / +0.093 before you
add anything.** Reuse its functions by import or copy with a pointer; do not edit that lane.

## Tasks

1. **Skill slope by sex.** Among workers at 35–40 (the lane's worker definition), regress log hourly pay on AFQT
   percentile (and on AFQT plus highest degree), separately for men and women, in G3+ NH white and pooled. Report
   the slope per 10 AFQT points with bootstrap SEs (the lane's Rao–Wu scheme). The hypothesis predicts a flatter
   slope for women.
2. **Sector of the main job.** From the full archive (`sources/reused-surveys/nlsy/nlsy97_all_1997-2023.zip`,
   hash in extract.py), extract for rounds 2013–2023: class of worker (government vs private vs self-employed),
   industry (YEMP_INDCODE-2002.*) and occupation (YEMP_OCCODE-2002.*) of the main job, plus CV_MSA and census
   region. Identify the main job by the codebook's rules (read the NLSY97 employer-roster documentation; select
   fields by question name and survey year as extract.py does, never by guessed reference numbers; check non-skip
   counts against the codebook). Classify a "credential-pay sector": public administration, public or private
   education, health care and social assistance, plus any government employer. Report the shares of G2 Hispanic
   and G3+ NH white women and men in it at 35–40.
3. **Where the daughters' premium sits.** Re-estimate the equal-AFQT gap for women (a) in the credential-pay
   sector, (b) in the rest of the private sector, and (c) with region or MSA controls. The hypothesis predicts the
   premium sits in (a) and vanishes in (b).
4. **Selection.** Neal–Johnson-style check: median regression of log hourly pay with non-workers imputed below the
   median (state the rule), and a bound with non-workers at the bottom. Does the daughters' premium survive?

## Rules

- Write `RESULT.md` first, opening with `**Verdict:**`, and append as you go. Tag every number
  ([CALCULATION: script → file], [DATA: …], [SOURCE: …], [TRAINING-DATA]). Report n and SE with every gap.
- Scripts and tracked outputs in this directory: `extract.py`, `analyze.py`, `derived/*.csv`. Raw pulls go to
  `_cache/` (git-ignored). CSV with `lineterminator="\n"`. Use `OPENBLAS_NUM_THREADS=1 uv run --no-project python3`.
- The archive CSV is 8 GB inside the zip: stream it with pandas `usecols` and `chunksize`, never materialize it.
- Do not commit. Do not touch other lanes, the evidence map, the ladder or any memo.
- Name the variable. Do not call a job "fake": report sector, class of worker and the pay–skill slope.
- Stop and report if the main-job identification or the class-of-worker field cannot be verified against the
  codebook. Do not guess.

## Parent correction (2026-09-29, received after the first RESULT)

Quoted from the parent's message:

> Brief correction from the parent, after checking career_trajectories derived/gaps.csv (age 35-40, w_round, arm edu_afqt, G2 Hispanic vs G3+ NH white).
> - The +0.113 / +0.093 are TOTAL earnings including non-workers as zero, not a workers-only figure.
> - At equal edu+AFQT at 35-40: women employment +0.031 (0.030), hourly_pay +0.134 (0.048). Men employment −0.027 (0.025), hourly_pay +0.007 (0.048).
>
> So the brief's selection story (fewer daughters work) is contradicted at equal skill, and place cannot explain a sex difference because sons share the geography. Adjust as follows:
> 1. Keep task 4 (selection) as a short check only, and state that employment at equal skill is not lower.
> 2. Keep region/MSA controls, but frame them as applying to both sexes.
> 3. NEW, task 5, the reference group. White women with the same AFQT may choose lower-paid, flexible jobs when married to high earners. Extract marital status (CV_MARSTAT or the codebook's equivalent) and, if available, spouse/partner income for 2013-2023. Re-estimate the daughters' equal-AFQT hourly premium against (a) never-married or unpartnered white women only, and (b) with marital-status controls for both groups.
> 4. The core test is unchanged: is the women's hourly premium concentrated in credential-pay sectors (government, education, health and social assistance)? Run the same split for sons.
> Update BRIEF.md with a dated "Parent correction" section quoting this, then continue.

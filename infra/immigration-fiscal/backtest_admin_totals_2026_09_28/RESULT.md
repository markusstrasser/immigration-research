claude-opus-5-5

**Verdict:** No pre-registered check misses, so no key correction is proposed. The two checks with power hit:
births to Mexican-origin mothers (14.43% of births predicted, 14.36% in NVSS 2024, and the state distribution within
noise) and the group's share of Medicaid-paid births (18.9% predicted, 20.5% actual, inside ±10%). The second is a
hit by the tolerance rule only: the prediction is significantly low (+8.1%, z 2.4, 95% interval +1.5% to +14.8%), and
the naive baseline 2 lands closer. Sized by the frozen rule it would be about +$0.2–0.3bn [TRAINING-DATA cost per
birth], under the $2bn follow-up trigger. (Added after the cross-lab review.) The three dollar
keys have no power. Refundable credits: δ +0.09 / +0.11, or +$1.6 / +$1.8bn at 48 / 11, with a 95% interval of
about −$5 to +$8bn. SSI: δ +0.96 / +0.95 against SSA's federally administered total, driven by California's state
supplement, which the line does not pay; against federal SSI alone δ is +0.17 / +0.15, a hit (+$0.8 / +$0.7bn).
Social Security: δ −0.01, or −$0.4 / −$0.6bn [DATA: derived/check_calls.csv, derived/scores.csv].

# Back-test: do the account's keys predict where administrative dollars land?

Lane opened 2026-09-28 from `BRIEF.md` (commit 78ca741). Pre-registered: phase 1 writes the predictions,
baselines and tolerances (`PREDICTIONS.md`, `derived/predictions.csv`) before any external figure is
opened; the parent commits them; phase 2 scores. Nothing outside this directory is edited. Nothing is
committed, staged or stashed.

## Calls

Every statistic is scored with the frozen `estimators.py` against the adopted reading; `PREDICTIONS.md` is
unchanged. δ is the misstatement of the group's dollars on a key: positive means the key gives the group too little.
The dollars are ΔG = L × hf × (s′ − s) at the point estimate, the change in the group's dollars on the line at each
end. None is a candidate, because nothing missed.

| Check | Target | Verdict statistic, adopted reading (shared / personal) | Call | Dollars at 48 / 11 (95% interval) |
|---|---|---|---|---|
| 1. Refundable credits | SOI TY2023, EIC + ACTC by state | δ +0.090 / +0.109; SE 0.193 / 0.204; τ 0.113 / 0.122 | no power | +$1.56 / +$1.75bn (−5.44 to +7.57 / −5.06 to +7.64) |
| 2. SSI | SSA Table 7.B7, federally administered payments, 2024 | δ +0.958 / +0.954; SE 0.872 / 0.880; τ 0.414 / 0.415 | no power | +$4.29 / +$4.27bn (−3.87 to +10.58 / −3.96 to +10.60) |
| 2. Social Security | SSA OASDI Table 3, December 2024 | δ −0.006 / −0.010; SE 0.138 / 0.142; τ 0.034 / 0.035 | no power (declared) | −$0.36 / −$0.57bn (−16.65 to +15.55 / −16.55 to +15.04) |
| 3a. Births, Mexican-origin mothers | NVSS 2024 (WONDER) | share 14.43% against 14.36% (error −0.5%, SE 7.6%); distribution D 0.058 (noise 0.041, Wald 6.33 < 11.07) | hit | — |
| 3b. Births, Mexico-born mothers | NVSS 2024 | share 4.10% against 5.11% (+24.9%, SE 16.9%); D 0.079 (noise 0.075) | no power (declared) | — |
| 3c. Medicaid-paid births | NVSS 2024, source of payment | group share 18.93% against 20.46% (+8.1%, SE 3.4%) | hit | not sized: no miss |

[DATA: derived/check_calls.csv, derived/scores.csv, derived/power.csv]

Both ends return the same call on every check. For credits the HC3 term (0.193) sets the SE, well above the
sampling term (0.116), so the state model's misfit rather than the sample costs the power. For SSI, HC3 (0.872)
doubles the sampling term (0.433) because of California. For Social Security the sampling term dominates (0.138
against HC3 0.124), and the declared no-power follows from a tolerance of 3.4% [DATA: derived/scores.csv].

**Secondary misses.** Two kinds of secondary statistic miss, and neither has a key behind it:

- The Medicaid-paid share as a level: 26.8% of women 15–44 covered in 2024, against Medicaid paying for 57.2% of
  Mexican-origin mothers' births (40.2% of all births). This was declared "expected to miss low". The readings
  for mothers of infants (36.0%) and for infants' own coverage (45.4%) miss too.
- Births to Mexico-born mothers, distribution of infants: D 0.133, Wald 15.4. Post-hoc note 5 covers its sample.

**Other secondaries.**

- SSI against federal SSI alone: hit, δ +0.168 / +0.154 (SE 0.350 / 0.353), +$0.80 / +$0.73bn. This is the only
  dollar-key statistic with power. Against December 2024 (Tables 10 × 11): no power, δ +0.98 / +0.97.
- Credits against other targets, all no power: refundable EITC + ACTC δ +0.070 / +0.087; EITC alone
  +0.052 / +0.071; ACTC alone +0.178 / +0.197.
- The published reading, all no power: credits δ −0.068 / −0.063, SSI +0.95 / +0.94, Social Security
  −0.017 / −0.021. ASEC 2024 against TY2023, the matched year: credits −0.123 / −0.119.
- Births: the Mexican-origin count, 512.3k against 521.1k (+1.7%), hits; the infants' distribution has no power
  (D 0.093). The Mexico-born count, 145.4k against 185.6k (+27.6%), has no power.
- Medicaid, the group's Medicaid-paid share over all mothers' share: 1.362 against 1.425 (+4.6%), a hit. Mothers of infants: a
  ratio of 1.316 and a share of 18.4%, both no power. Infants' own coverage: a ratio of 1.327, a hit, and a share
  of 19.1%, no power.

[DATA: derived/scores.csv, derived/target_national.csv]

## Against the baselines

As declared, the prediction beats a baseline when its error is smaller.

| Statistic | Prediction | Baseline 1 | Baseline 2 | Beats |
|---|---|---|---|---|
| Credits, D over 51 areas | 0.064 | 0.059 (no SSN rule) | 0.098 (population) | baseline 2 only |
| SSI, D | 0.107 | 0.117 (population) | 0.123 (age 65+) | both |
| Social Security, D | 0.024 | 0.059 (population) | 0.037 (age 65+) | both |
| 3a national share, absolute error | 0.07pp | 0.46pp (women 15–44) | 2.53pp (civilians) | both |
| 3a distribution, D | 0.058 | 0.055 (union women 15–44) | 0.061 (union residents) | baseline 2 only |
| 3c group share, absolute error | 1.53pp | 6.56pp (share of women 15–44) | 1.09pp (share of Medicaid-covered persons, all ages) | baseline 1 only |
| 3c ratio, absolute error | 0.063 | 0.425 (no difference) | 0.212 (all-age coverage ratio) | both |

[DATA: derived/dissimilarity.csv, derived/scores.csv]

The credit prediction's D has a sampling SE of 0.011, so its 0.005 gap to the no-rule baseline is noise
[DATA: derived/dissimilarity.csv].

The adopted reading does better than the published one in California; over the whole state distribution its D gain
(0.007) is inside D's sampling SE (0.011). (Softened after the cross-lab review; it first said "beats".) The
state-aware flag moved California's predicted share from 11.30% to 10.12%, and SOI's is 10.08%. California's error
is −10.8% (z −2.3) in the published reading and −0.4% (z −0.1) in the adopted one, and D falls from 0.071 to
0.064 [DATA: derived/state_errors.csv, derived/dissimilarity.csv]. By the declared reading, audit row 4 and the
state-aware flag moved the credit key the right way. The adopted |δ| is larger than the published one (0.090 against
0.068), so the two measures split, and California is the clearer signal.

## Diagnostics

These were declared in advance, and they change no call.

| Diagnostic | Credits | SSI | Social Security |
|---|---|---|---|
| δ without CA | +0.139 / +0.170 | +0.118 / +0.095 | −0.058 / −0.070 |
| δ without TX | −0.072 / −0.059 | +1.35 / +1.31 | −0.046 / −0.053 |
| δ with the other-foreign-born control (γ) | +0.119 / +0.135 (0.40 / 0.21) | +0.79 / +0.80 (1.29 / 1.17) | +0.061 / +0.061 (−0.34 / −0.28) |
| The brief's slope on the group's share of residents (HC1 SE) | 0.287 (0.262) | 1.04 (0.44) | 0.003 (0.073) |

State errors A_s / P_s − 1, with z, in the adopted reading:

| State | Credits | SSI, federally administered | Social Security |
|---|---|---|---|
| CA | −0.4% (−0.1) | +40.5% (4.2) | +1.0% (0.4) |
| TX | +18.2% (3.1) | +5.1% (0.4) | +0.8% (0.3) |
| AZ | −6.3% (−0.4) | +10.1% (0.4) | −7.6% (−1.1) |
| NM | −3.7% (−0.3) | −18.7% (−0.9) | +1.5% (0.3) |
| NV | +5.5% (0.4) | −20.8% (−0.9) | +6.8% (0.9) |
| CO | +10.7% (0.7) | −39.8% (−1.2) | −13.7% (−1.8) |
| IL | +2.5% (0.2) | +0.9% (0.0) | +3.1% (0.6) |

[DATA: derived/diagnostics.csv, derived/state_errors.csv]

## Candidate corrections: none

No verdict statistic and no secondary δ missed. Step 3 of the phase 2 procedure in `PREDICTIONS.md` therefore enters
nothing into the September 27 package, and `derived/candidate_shifts.json` is empty. The secondary misses carry no
correction under the pre-registered rules. The Medicaid share's level readings were declared likely misses, because
pregnancy widens eligibility, and the adopted Medicaid key is MEPS spending by age band rather than a coverage count.
A distribution miss moves no national key (`PREDICTIONS.md`, check 3). The Medicaid group share hit, so its dollar
sizing does not run.

## Post-hoc notes

These notes were written after the administrative figures were seen. They change no call.

1. **SSI's primary target.** It includes California's federally administered state supplement: $3.26bn of the
   national $3.41bn [DATA: derived/targets.csv]. The account's SSI line pays federal SSI only, so it does not
   include the supplement. Against federal SSI alone, California's error falls from +40.5% (z 4.2) to +4.4%
   [CALCULATION: SSA's federal-only share 12.93% over the predicted 12.38%], and δ falls from +0.96 to +0.17, a
   hit. Named gap 2 expected state-administered supplements outside SSA's figures. The supplement that matters is
   administered federally, so it sits inside them. Were I choosing now, federal SSI would be the primary target,
   because it is what the line pays.
2. **Where the credit misfit sits.** Across all 51 areas, the five largest residuals by |z|, with the group's share
   of each state's predicted credits, are [CALCULATION: derived/predictions.csv against derived/targets.csv]:
   - Florida +29.8% (z 4.5), group 5.5%;
   - Texas +18.2% (z 3.1), group 44.0%;
   - Washington −29.4% (z −2.8), group 35.7%;
   - Georgia +24.1% (z 2.6), group 9.2%;
   - West Virginia −22.1% (z −2.4), group 1.9%.

   The three where the group is small widen HC3 without bearing on the group. The two where it is large point in
   opposite directions, and δ changes sign without Texas. [INFERENCE] State differences in take-up and erroneous
   claims (named gap 2) fit this pattern better than a group effect does. In Texas and Washington, the lane cannot
   separate the two.
3. **The SSN rule.** The no-rule series scores δ −0.10 / −0.09 and the rule +0.09 / +0.11
   [DATA: derived/scores.csv], so SOI's totals sit about halfway between the two, and each is within one SE of
   zero. The components differ. With the rule, EITC scores δ +0.05 / +0.07 (no rule: −0.19 / −0.18) and ACTC
   scores +0.18 / +0.20 (no rule: +0.09 / +0.10). None of them has power. [INFERENCE] If anything, the rule removes
   about the right amount of EITC and slightly too much ACTC. The test cannot resolve either.
4. **Births to Mexico-born mothers.** NVSS counts 185.6k and the frame 145.4k
   [DATA: derived/target_national.csv, derived/scores.csv]. The Mexican-origin total matches, so the gap is in the
   mother's birthplace, not in the number of infants. The frame puts 28% of the group's births with Mexico-born
   mothers; NVSS puts 36% there [CALCULATION: 145.4 / 512.3; 185.6 / 521.1]. The reported Mexico-born share of
   Medicaid-paid births shows the same gap: 4.0% against 7.7%. By the frozen rule the gap has no power, and it is
   immaterial for a year's account. [INFERENCE] A generation split that reads the co-resident mother's birthplace in
   the CPS would put too few infants with a Mexico-born parent.
5. **The Mexico-born infants' miss** rests on 41 sample infants, and its NM+NV+CO cell rests on one
   [DATA: derived/predictions.csv, sample_persons]. With cells this thin, the replicate covariance is itself noisy.
   The estimator check never tested the size of the distribution call, so the miss is weak evidence. For the same
   group, the verdict series of children 0–2 (173 sample children) has no power.
6. **A sharper SSI test exists.** The SSI Annual Statistical Report 2024 also has Table 14 ("Foreign-born
   recipients, by region, country of origin, eligibility category, and age, December 2024") and Table 31
   (noncitizen recipients by state, December 2024) [SOURCE: `_cache/ssa_ssi_asr24.xlsx`, sheet titles only]. They
   count the group's foreign-born recipients directly, where state totals only let δ infer them. Only their titles
   were read here, so a later pre-registered test can still be blind to their numbers.

## Sources and reproduction

- `derived/sources.json` holds the primary files, their hashes and their routes. The quoted definitions, titles,
  query blocks and totals are in `reads/`: `irs_soi_ty2023.md`, `ssa_ssi_2024.md`, `ssa_oasdi_2024.md` and
  `cdc_wonder_natality_2024.md`.
- `targets.py` parses the raw pulls into `derived/targets.csv` (target, state, value, share) and
  `derived/target_national.csv`. It stops unless each source holds the 51 areas, and unless SSA's federal SSI plus
  supplement equals the total in every state.
- `score.py` imports the frozen `estimators.py` and writes `derived/scores.csv`, `check_calls.csv`,
  `dissimilarity.csv`, `state_errors.csv`, `diagnostics.csv` and `candidate_shifts.json`.
- Rerun from the repository root. `targets.py` needs openpyxl.

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/backtest_admin_totals_2026_09_28 \
  "node {lane}/line_amounts.cjs" "uv run --no-project python3 {lane}/predict.py" \
  "uv run --no-project python3 {lane}/estimator_check.py" \
  "uv run --no-project --with openpyxl python3 {lane}/targets.py" "uv run --no-project python3 {lane}/score.py" \
  --allow-unrun infra/immigration-fiscal/backtest_admin_totals_2026_09_28/estimators.py
```

## Log

- Phase 1 started. Blindness screen of the repo by file name and match counts only (no values read):
  - IRS SOI county files for tax years 2011–2022 sit in
    `causal_evidence_2026_09_20/raw/county_outcomes/raw/irs_soi/county/` and carry county EITC and ACTC;
    state sums for those years are therefore in the repo, unopened. California FTB CalEITC reports sit in
    `california_program_costs_2026_09_23/_cache/`, unopened.
  - No SSA state file is in the repo by name; `admin_transfer_checks_2026_09_19` holds national totals.
  - Several memos and lanes mention births to Mexican(-born) mothers and Medicaid-paid births
    (`demo_momentum_2026_09_16`, `ir5_fraud_and_cohorts_2026_09_27`, `external_benchmarks_2026_09_24`,
    the confidence ladder); unopened.
- Definitions read, numbers not: the SOI 2023 state data guide (AGI_STUB 0 = state total; A59660 is the whole
  EIC, A59720 its refundable part, A11070 the ACTC), the WONDER natality expanded help (mother's residence,
  Mexican origin, mother's birth country, five payer categories, 1–9 births suppressed) and SSA's table of
  contents. SSA's site refused scripted fetches; its contents page was read through a browser session.
- The prediction was first built on the builder's published keys with the audit's paper rule at 0.60. The
  adopted case keys these lines with the CPS lane's stack instead (audit row 4's weights, the state-aware flag,
  the on-books lane's origin shares; `main_case_2026_09_24/package.cjs`), so the prediction now rebuilds that
  stack before its fill-in step with the lane's own functions. The earlier reading stays as the "published"
  secondary. The change matters: the state-aware flag moves California's predicted credit share from 11.30% to
  10.12%, and the no-rule baseline now sits 0.185 in δ from the prediction instead of 0.074
  [DATA: derived/predictions.csv, derived/power.csv].
- Gates: builder keys 9.7e-17, paper rule 1.4e-15, stored stack cells of the four lines reproduced with a
  0.0 bn gap [DATA: derived/prediction_audit.json].
- Scoring frozen in `estimators.py` before any administrative figure: δ's standard error is the larger of the
  replicate and HC3 terms (the first draft added a HC1 term to the replicate term, which counts sampling error
  twice). A synthetic check on the frame's own replicates finds the estimator unbiased, 96–98% coverage and a
  3–4% false-miss rate [DATA: derived/estimator_check.csv].
- Power before looking: credits powered by sampling only just (sampling SE 0.103 / 0.106 against τ 0.113 /
  0.122); SSI powered (0.331 / 0.335 against 0.414 / 0.415) but coarse; Social Security declared no power;
  births of Mexican-origin mothers powered for the national share and the six-cell distribution of children
  0–2; Mexico-born mothers declared no power; the Medicaid group share powered (relative SE 3.4% against 10%)
  [DATA: derived/power.csv].
- Predictions, baselines, tolerances and the phase 2 procedure: `PREDICTIONS.md`. Frozen for the parent's commit.
- Phase 2 opened on the parent's go after its commit 883182b. Its rerun matched 16 of 16. From here on,
  `PREDICTIONS.md`, `predict.py`, `estimators.py`, `estimator_check.py`, `line_amounts.cjs` and their outputs are
  untouched.
- Fetches:
  - IRS SOI's state file came by curl.
  - SSA's three workbooks came through a browser download, because SSA refuses scripted requests. The SSI
    Annual Statistical Report gives December figures by state; the calendar-2024 totals by state, split into
    federal SSI and federally administered supplementation, are Table 7.B7 of the Annual Statistical Supplement
    2025. That table became the primary as declared ("calendar 2024 totals are used if SSA publishes them by
    state"), and December 2024 became a secondary.
  - WONDER's API refuses sub-national location, so the five natality exports came from the D149 web form, with
    the five-category payer variable.
  - Every file is hashed in `derived/sources.json`, and the quotes are in `reads/`.
- Parsing gates, all passed:
  - SOI's US row equals the 51 areas plus OA and PR.
  - SSA 7.B7's federal SSI plus supplement equals its total in every state, to $1k.
  - No state's Mexican-origin birth cell is suppressed, and the Mexican-origin payer cells sum to the state
    export's national count, 521,149.
- The first scoring run wrote each births baseline row twice into `derived/dissimilarity.csv`, because they were
  appended inside the series loop. This was fixed before the final run. No call reads those rows.
- Scored: no miss on any verdict statistic, and no candidate. The calls, baselines, diagnostics and post-hoc notes
  are above.
- Rerun with the five commands above: `[rerun] IDENTICAL: 31/31 files unchanged`, exit 0. It ran before the last
  edits to this file, which no script reads or writes. The browser session is closed.

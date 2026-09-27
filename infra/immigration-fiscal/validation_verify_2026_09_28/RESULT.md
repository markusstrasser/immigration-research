claude-opus-5-5

**Verdict:** The memo's numbers are accurate. All 125 numbers in its opening lines and sections 1–3 match
their lane outputs at the precision the memo prints [CALCULATION: `derived/memo_check.csv`]. That count
includes five numbers from the held-out tax lane, which a022fc6 added to the memo's tax paragraph during this
check. Four of the five lanes rerun to byte-identical outputs. The fifth, the audit lane, differs only because
`snap_loso.json` records the git commit it ran at. All 38 lane tests pass [DATA: rerun logs, below]. Transcripts show that all four
follow-up lanes wrote their design before any score was printed. One design addition came later: the
schools lane added the NAEP quality check behind "46 of 51" after its first prediction scores. Four construct
points qualify the memo's reading, though none changes a number:
- The Mariel joint model does not fit its own training years. Its normalized RMSE is 29–34% within 1970–1976.
  Dade's federal revenue exceeds every donor's in 6 of 7 of those years, so "fails its own prediction check"
  is at root a failure to fit.
- 46% of the 2024 MEPS respondents aged 65+ were also 2023 respondents. They sit in both the training pool
  and the repeat-2023 baseline.
- The GSS count of "eight of nine" includes one exact duplicate, so the distinct count is seven of eight. The
  lane chose its baseline after the model's results were known; the memo omits that.
- In `benchmarks.py`, "corroborates" means a materiality rule: an implied change of at most $2bn in 54 of 61
  rows, and a ratio within 0.8–1.25 in the other 7.

Two memo claims go beyond these lanes. The first is the blanket statement that each lane saved its design
before calculating results. The second, in section 1, is that later income-gradient corrections address the
IRS-distribution failure. The held-out tax lane now shows they do so only below $1M. Across all 19 bins the
final key still misses by 23.5pp. [CALCULATION / INFERENCE]

# Verification of the validation and back-testing memo

Lane: `infra/immigration-fiscal/validation_verify_2026_09_28/`. Brief: `BRIEF.md` (commit 68a5d0a). Subject:
`research/immigration-validation-and-backtesting-2026-09-28.md` and its five lanes (df05631). The memo checked
is the af2d01b text plus one bracket that a022fc6 added to the section 3 tax paragraph at 04:27 JST. The
bracket carries ladder 249's result from `tax_key_heldout_2026_09_28`, and its numbers are checked against
that lane. This lane reran the five lanes and tabulated every memo number against their outputs. It also
checked each test's construct and read the Codex transcripts that built the lanes. It edits nothing outside
this directory. The
reruns rewrote the five lanes' ignored `derived/` outputs. Afterwards, each `derived/` was compared with a
snapshot taken before the reruns and now matches it byte for byte. That required restoring the audit lane's
`snap_loso.json`, which differs only in its `head` field.

## 1. Reruns

Each lane was rerun with `scripts/rerun_lane.py`, using the commands in its README or RESULT
(`rerun_lanes.sh` holds them). There were two passes. Pass 1 used the version of the script that compares
`derived/` only. Pass 2 used defd058, which also compares every file a commit of the lane would carry. The
lead committed defd058 during this lane. Tests ran after each rerun, with `-p no:cacheprovider` added to
pytest so a test run writes nothing into a lane. [DATA: `rerun_lanes.sh`; logs in the session scratchpad
`bg/vv_*.log`, `bg/vv2_*.log`]

| Lane | Commands | Pass 1 | Pass 2 | Tests | NOT RUN |
|---|---|---|---|---|---|
| validation_audit | `gss_baseline.py`; `snap_loso.py` | rc 1, DIFFERS: 3/4 unchanged, `snap_loso.json` CHANGED | rc 1, DIFFERS: 8/9 unchanged, `snap_loso.json` CHANGED | none in lane | none |
| validation_schools | `validate.py --source-root …` | rc 0, IDENTICAL 10/10 | rc 0, IDENTICAL 15/15 | 7 unittest OK | none |
| validation_medical | `acquire.py` (verifies cached pins, no download); `analysis.py` | rc 0, IDENTICAL 6/6 | rc 0, IDENTICAL 14/14 | 6 pytest passed | none |
| validation_fiscal_years | `analysis.py --source-root …` (`--with xlrd`) | rc 0, IDENTICAL 6/6 | rc 0, IDENTICAL 12/12 | 19 pytest passed | none |
| validation_mariel | `joint_budget.py` (`--with scipy pandas numpy`) | rc 0, IDENTICAL 9/9 | rc 0, IDENTICAL 14/14 | 6 unittest OK | none |

**The audit lane's DIFFERS is a design defect, not a numeric change.** In both passes, the diff against the
original file is one line: `"head": "5654458…"` became the checkout's HEAD at the time, `68a5d0a…` in pass 1
and `a022fc6…` in pass 2. `snap_loso.py:113` writes `git rev-parse HEAD` into the output. Any later commit
therefore makes a byte-identical rerun impossible. Every SNAP number is unchanged. [DATA: `diff` of
`snap_loso.json` against the pre-run snapshot]

**None of the five lanes tracks its outputs.** Each `.gitignore` ignores `derived/`. The repository's
convention is tracked `derived/` summaries (CLAUDE.md, Structure), so no number in the memo exists in git.
Checking any of them means rerunning against ignored upstream inputs. The outputs are small except the
schools `predictions.parquet` (18.6 MB): 24 KB for audit, 36 KB for medical, 72 KB for fiscal, 1.2 MB for
Mariel, and about 0.5 MB for schools without the parquet. The documented commands also pin `UV_CACHE_DIR`
to three `/private/tmp` caches, which a reboot can clear; the Mariel lane's first runs failed on scipy until
a cache existed. [DATA: `.gitignore` files, `du`; SOURCE: `design_order_audit.md`, Mariel section]

## 2. Every memo number against its lane

`check_memo.py` holds 125 checks: the 4 numbers in the memo's opening lines, 32 in section 1, 31 in section
2 and 58 in section 3. Five of the section 3 numbers are in the a022fc6 bracket: 23.5pp, 8.4pp, 18.5pp and
$3.2bn / $3.1bn, checked against `tax_key_heldout_2026_09_28/derived/scores.csv` and
`main_case_change.csv`. The memo's verdict paragraph contains no numbers. Every check first asserts that the
memo text contains the quoted literal. It then reads the value from the lane output, or from the cited
earlier lane or memo for section 1. A value matches when rounding it to the memo's precision reproduces the
memo's number. **Result: 125 match, 0 mismatch.** Two runs are byte-identical. The full table, with file and
column for each value, is `derived/memo_check.md` (the same rows as `memo_check.csv`). [CALCULATION]

The brief's named numbers:

| Memo | Lane value | Lane file: column | Status |
|---|---:|---|---|
| GSS model/frozen G2 4.59/5.67 | 4.5925 / 5.6663 | `validation_audit/derived/gss_baseline.json`: `model_tv_pp`, `naive_tv_pp` (english_only) | match |
| G3 2.80/5.16 | 2.7987 / 5.1640 | same | match |
| G4+ 3.39/9.24 | 3.3861 / 9.2431 | same | match |
| pre2021 G2 3.29 vs 2.72 | 3.2928 / 2.7215 | same, english_only_pre2021 | match |
| SNAP MAE 5.16 → 5.69 | 5.1626 → 5.6882 | `snap_loso.json`: `all_valid_states.{raw,corrected}.mae_pp` | match |
| SNAP RMSE 8.13 → 8.79 | 8.1301 → 8.7879 | same, `rmse_pp` | match |
| Schools .182 / .202 | .18196 / .20154 | `validation_schools/derived/scores.csv`: `log_rmse`, prepandemic current all, district fit and score, `free_trend` / `proportional_trend` | match |
| Schools .169 / .175 | .16928 / .17469 | same, initial-pupil fit and score, `proportional` / `free_trend` | match |
| $5.86m / $7.09m | 5.8647 / 7.0922 | same, district fit and score, `level_mae` ÷ 1e6 | match |
| −3.46% / +5.50% / +1.99% | −3.4584 / +5.5020 / +1.9924 | `joint_observed.csv` (all): `pupils/current/teachers_growth_percent` | match |
| 46 of 51 | 46 of 51 | `state_resource_quality.csv`, reading grade 4: pupil/teacher ratio fell and `score_change` < 0 | match |
| Medical 1.114 (.151) / 1.009 (.109) | 1.1142 (.1508) / 1.0086 (.1087) | `validation_medical/derived/diagnostics.csv`: MCBS2022 / MEPS2022 ratio | match |
| .106 (.186) vs .420 (.177) | .1056 (.1858) / .4195 (.1765) | `cross_survey_gaps.csv`, public_common | match |
| 95% interval [−.259, +.470] | −.2587, +.4699 | gap ± 1.96 SE | match |
| 85.1% Medicare | 85.14% | `payer_decomposition.csv`: .357178 of .419534 | match |
| .374 / .411 / .293 | .3743 / .4107 / .2929 | `diagnostics.csv`: MCBS minus MEPS ratios (uniform age-sex; raw vs tail-mean; p99 caps) | match |
| −.074 (.137) vs −.202 | −.0739 (.1370) / −.2021 | `retrospective_2024.csv`: mexican public_common, `error`, `error_se` | match |
| Fiscal .495 → .415 | .4953 → .4150 | `validation_fiscal_years/derived/scores.csv`: mean `absolute_error_pp`, primary, frozen_share / composition_transport | match |
| IRS 25.20 / 2.43 / 24.06 | 25.202 / 2.430 / 24.062 | `irs_distribution.csv`: ½Σ\|`error_pp`\| by arm | match |
| 4.77pp / $90.86bn | 4.7691 / 90.861 | `scores.csv`, policy_stress, federal_after_shared, composition_transport: −`error_pp`, −`conditional_union_error_bn` | match |
| Mariel 39.75% / 26.65% vs 16.02% | 39.747 / 26.647 / 16.021 | `validation_mariel/derived/june30_scores.csv`: `joint_normalized_rmse_pct`, pre_holdout | match |

The section 1 table also matches:
- Earnings ratios .6919 and .6866, their intervals, and the Mexico-born ratios .6851 and .6458 match
  `same_year_tax_2026_09_20/derived/acs_cps_comparison.csv`.
- Wages of $11,105.6bn against $11,103.2bn (+0.021%) and the 6.09% recipient shortfall match
  `ssa_comparisons.csv`.
- The income-2024 figures, +2.25% and 5.27%, match the administrative-checks memo table.
- The school residuals (+17k/+27k, SEs 69k/59k, 154k with SE 69k) match the cited memo text.
- The California SNAP shares, 43.989% and 44.078%, match
  `admin_benefit_keys_2026_09_24/derived/share_comparisons.csv`. The memo cites the lane's RESULT.md, which
  does not state these numbers.
- The federal-tax figures match: 13.73% in `irs_national.csv`, and $489.8bn and $200.2bn in
  `irs_bracket_summary.csv`.

Three figures outside the table also match:
- the school location factor, k = 1.034;
- the medical ratios .845 (.089) and 1.265 (.152), from this lane's reproduced diagnostics, and the pooled
  1.005 (.056), from the pooled lane's text;
- the scaling scores, 12,370 districts with .301/.233/.223/.203/.192, from
  `scaling_test_2026_09_20/derived/school_cv.csv`.

The broader screen keeps the same ranking. [CALCULATION: `derived/memo_check.md` rows 5–43]

## 3. Construct checks

### Was each baseline fixed before scoring?

The question was answered from the raw Codex transcripts, which record ordered, timestamped file writes
and runs. [SOURCE: `design_order_audit.md`, a subagent's read-only transcript audit.] I checked three of its
claims against the rollouts myself:
- The schools worker's line 143 printed the first scores at 01:36:27 JST.
- Its line 194, at 01:39:54, adds "Availability extension before reading quality outcomes" (state NAEP) to
  `Design.md`.
- The Mariel design's SHA-256 `a503844c…` equals `design_sha256` in `summary.json`.

| Lane | Design written (JST, 09-28) | First scores printed | Design changed after scores? |
|---|---|---|---|
| schools | 01:29:22 | 01:36:27 | **Yes, once (01:39:54).** It added the state NAEP join behind "46 of 51". Split, arms, baselines and sample were unchanged. The design text says the join came before the NAEP values were read. |
| medical | 01:28:19 (amended 01:31:41, before scoring) | 01:35:57 | No. The script gained a sensitivity the design lacks (`include_unknown_birthplace`, .845 → .843) after scoring; its RESULT discloses this. |
| fiscal_years | 01:30:13 (two source-guard fixes before scoring) | 01:39:08 | No. |
| Mariel | 01:32:12, in the same patch as `joint_budget.py` | 01:36:11 | No; the hash is unchanged from creation to commit. |
| audit: GSS | no design file | — | The README says the frozen-distribution baseline "was selected after the original results were known". The memo does not say so. |
| audit: SNAP | frozen rules in the script docstring | — | The docstring says the rule was frozen before scoring. The validity screen had already used the outcome; both the memo and the README disclose this. |

All designs call themselves retrospective: the source years had been inspected before. That label is
accurate. [SOURCE: transcripts, per `design_order_audit.md`]

### Do training and test data overlap?

- **GSS.** Training is cohorts 1961–71 in survey years to 1996; the test is cohorts from 1972 in 1998–2024.
  A guard in `projection_backtest_2026_09_19/cohorts.py:31–33` rejects any cohort overlap. The model uses
  the test period's parent-education mix, as the memo says. [DATA: code]
- **SNAP.** Rho is fitted without the held-out state. That state's validity classification did use its
  administrative share, which is disclosed. [DATA: `snap_loso.py:86–95`]
- **Schools.** The periods share an endpoint: FY2000→2010 predicts FY2010→2019, and FY2001→2019 predicts
  FY2019→2024. No test-period spending enters training, and a lane test checks that. Noise in the shared
  FY2010 or FY2019 level enters both periods' changes with opposite signs. [INFERENCE]
- **Medical, 2024 retrospective.** The years are disjoint: the pool is 2016–2023. The respondents are not.
  2,206 of 4,847 respondents aged 65+ in 2024 (46%) are 2023 respondents from MEPS panel 28. They are in
  the training pool and in the repeat-2023 baseline. The lane's SE keeps this covariance and its RESULT
  says so; the memo does not. Correlated sampling error favors the repeat-2023 baseline, so the "four of six"
  pooled wins come despite it. [CALCULATION: `medical_ethnicity_pooled_2026_09_23/_cache/pooled.parquet`
  DUPERSID; INFERENCE]
- **Medical, 2022 against 2023.** Both surveys reuse respondents across the two years:
  - In MEPS, 1,836 of 4,504 respondents aged 65+ in 2023 (41%) were also 2022 respondents.
  - MCBS panels overlap too, but the PUF IDs cannot link them. The lane says so; the memo's "previously
    unused external measurement check" does not.

  The file is new; the people are partly the same. [CALCULATION; SOURCE: medical RESULT §1]
- **Fiscal years.** The primary split runs from ASEC2023 to ASEC2025. The CPS 4-8-4 rotation puts a
  household in March supplements of at most two consecutive years, so these two samples should be disjoint.
  The secondary split, ASEC2023 to ASEC2024, overlaps, and the lane says so. The IRS diagnostic compares
  population tables. [INFERENCE: CPS design]
- **Mariel.** The fit covers 1970–1976 and the prediction 1977–1979, as in the code. No later Dade outcome
  enters; a lane test checks that. [DATA: `joint_budget.py`]

### Is each score on the unit the memo names?

Yes, for every number checked:
- **Schools.** .182/.202 are district-unweighted log RMSE and .169/.175 are fitted and scored with
  initial-pupil weights. The dollar figures ($5.86m, $7.09m) are district-unweighted mean absolute level
  errors in 2020 dollars, as the memo says. The weighting decides the winner. The best unweighted arm is the
  separate growth/shrink response at .1815, which the memo omits; the best pupil-weighted arm is
  proportional at .1693. [CALCULATION: `construct_checks.csv`]
- **Medical.** All figures are ratios of Hispanic to non-Hispanic white mean payments; the memo calls them
  "ratio errors, not dollar corrections".
- **Fiscal.** Errors are percentage points of the union's share. Dollars appear only when multiplied by the
  national CPS total, which the memo labels "conditional".
- **IRS.** Total variation in percentage points. The CPS side uses `FEDTAX_BC`, which is before refundable
  credits (`FEDTAX_AC = FEDTAX_BC − ACTC − EITC`, `analysis.py:136`). The IRS side uses Table 1.2 "Income tax
  after credits". That is a matched concept.
- **Mariel.** The score is an RMSE normalized by treated training means, floored at 1% of training revenue.
  The memo does not mention the floor, and nothing in it depends on the floor. [DATA: code]

### Does the medical 2022 comparison use the same populations as 2023?

It uses the same definitions, and the misalignment between the surveys is about the same in both years.
- **Same code path in both years** (`analysis.py:102–168`): ages 65+; Medicare-ever in MEPS (`MCREV == 1`,
  known birthplace); CMS age codes 2–3 in MCBS; Hispanic against non-Hispanic white; Medicare plus Medicaid
  payments. The MEPS pool maps each year's suffixed variables the same way
  (`medical_ethnicity_pooled_2026_09_23/meps_pool.py:140–162`).
- **Same frame gap in both years.** MCBS excludes anyone with any facility, hospice or institutional event.
  I verified this in the pinned CMS guide ("excludes beneficiaries who had a Facility interview during the
  year or who incurred any facility, hospice, or institutional events or costs"). MEPS represents 1.26×
  (2022) and 1.27× (2023) as many Hispanic beneficiaries as MCBS, and 1.05× and 1.02× as many white ones.
- **Different samples.** Record counts: MEPS 545/3,600 (2022) and 447/3,196 (2023); MCBS 543/4,281 and
  632/4,454.

[CALCULATION: `construct_checks.csv`; SOURCE: CMS Microdata PUF User Guide, pinned in
`fiscal_access_2026_09_20/_cache/methodology/`]

### Is "corroborates" in `benchmarks.py:27–35` the materiality rule the memo describes?

Yes. Rows with an implied main-case effect get "corroborates" when |effect| ≤ $2bn at both ends. Rows
without one get it when the external/account ratio lies in [0.8, 1.25]. Neither branch is a statistical
test. The memo describes only the first. Of the 61 "corroborates" rows in `benchmarks.csv`, 54 come from
the $2bn rule and 7 from the ratio band. A missing end is treated as 0, through `np.nan_to_num`.
[DATA: `benchmarks.py:27–36`; CALCULATION: `construct_checks.csv`]

### Mariel: the failure is a fit failure

Measured on the training years, the joint model's normalized RMSE is already 33.7% for the relative
weighting and 29.1% for the common unit. On the held-out years it is 39.75% and 26.65%. Dade's federal
intergovernmental revenue exceeds every donor's in 6 of 7 training years. Its total expenditure and revenue
lie inside the donor range, with 2–3 donors larger. Weights that are nonnegative and sum to one cannot
reproduce an endpoint above every donor. One shared weight vector must fit all six endpoints, so that
endpoint pulls the joint fit off. The memo's conclusion holds: this construction has weak predictive
support. The reason is that it cannot match Dade before the event, and the 1977–1979 holdout adds little to
that. [CALCULATION: `construct_checks.csv`; DATA: `causal_execution_2026_09_20/mariel/work/scm-june-only-panel.csv`]

### GSS: eight of nine includes a duplicate

The English-only and all-languages G4+ rows are the same sample, with identical errors and respondent
counts. There are eight distinct comparisons, and the model wins seven. The memo's "which overlap and are
not nine independent replications" is correct but understates this. [CALCULATION: `construct_checks.csv`]

## 4. Memo claims beyond what the lanes compute

1. **§3, opening:** "Each lane saved its split, score and alternatives before calculating the new
   results." This is true of the prediction tests. It is not true of everything section 3 reports:
   - The schools NAEP check ("46 of 51") entered the design after the first prediction scores.
   - The medical lane's unknown-birthplace sensitivity was added after scoring.
   - The GSS baseline in §2 was selected after the model's results were known.
2. **§1, federal-tax row:** "Later income-gradient corrections address this class of discrepancy." None of
   the five lanes tests this; the fiscal lane scores only the released CPS tax variable (24.06pp). The
   held-out tax lane, finished during this check, tests it, and the result is only partly favorable:
   - Across all 19 bins, the final calibrated key scores 23.5pp against IRS 2023, against 24.1pp before
     CBO's gradient.
   - With the bins from $1M pooled, the gradient cuts the miss from 18.5pp to 8.4pp. Frozen IRS 2022 shares
     score 2.4pp.

   The corrections therefore address the discrepancy below $1M, not the top of the distribution. The
   section 3 bracket reports this; the section 1 sentence still reads as unqualified.
   [DATA: `tax_key_heldout_2026_09_28/derived/scores.csv`]
3. **§3, medical:** "a previously unused external measurement check." The file is new, but MCBS panels share
   respondents across years (the lane says so). The memo's "neither equivalence nor a significant
   year-to-year change" stands; the samples are not independent.
4. **§3, Mariel:** "fails its own prediction check." It is correct as a comparison with the baseline. The
   lane does not compute the training-period fit, which already fails (above). This is a gap in what the
   lane computes, not an overstatement by the memo.

Everything else in the verdict and sections 1–3 is either computed by the lanes or labelled as inference or
limitation. That covers mixed transport results, weighting-dependent school rankings, medical disagreement
surviving the tested explanations, and component-only scope. [INFERENCE]

## Limits of this check

- Upstream inputs were not rebuilt: the GSS transition cells, the admin-benefit arrays, the MEPS pool, the
  F33/CCD panels, the ASEC ZIPs and the GFD panel. The reruns prove the five lanes reproduce from those
  inputs, not that the inputs are right.
- Seven section 1 values were checked against the cited memo or lane text, not recomputed: the school
  residuals, the 2024 wage and recipient comparisons, the pooled 1.005 (.056), the 13 Mexican-origin
  respondents and k = 1.034.
- The transcript audit rests on transcripts in which inter-agent messages are encrypted. The fiscal design's
  claim "Parent reviewed the design before scoring" cannot be confirmed; the exchange 70 s before the design
  was written is unreadable.
- This check was run by an LLM. Its selection of construct questions carries the dispositions described in
  `notes/llm-bias-caveat.md`. The numeric table is mechanical and fails loudly on any literal it cannot find
  in the memo. [METHOD]

## Reproduction

From the repository root:

```sh
# the five lanes (reruns rewrite their ignored derived/; snap_loso.json will differ by its head field)
for k in audit schools medical fiscal mariel; do bash infra/immigration-fiscal/validation_verify_2026_09_28/rerun_lanes.sh $k; done
# this lane (two runs byte-identical)
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/validation_verify_2026_09_28 \
  "uv run --no-project python3 {lane}/check_memo.py" \
  --allow-unrun infra/immigration-fiscal/validation_verify_2026_09_28/rerun_lanes.sh
```

## Files

- `check_memo.py`: the 125 memo checks and the construct facts. It reads only; it writes `derived/`.
- `derived/memo_check.csv`, `derived/memo_check.md`: every memo number with its lane value, source and
  status.
- `derived/construct_checks.csv`: computed construct facts:
  - the GSS duplicate;
  - the embedded git head;
  - the best school arm by weighting;
  - medical records and population ratios by year;
  - Mariel's training-period fit and convex-hull counts;
  - the benchmark branches.
- `design_order_audit.md`: a transcript audit of design-before-scoring order, with line references into the
  Codex rollouts, verbatim from the subagent; three claims spot-checked, as above.
- `rerun_lanes.sh`: the five lanes' documented reproduction commands.

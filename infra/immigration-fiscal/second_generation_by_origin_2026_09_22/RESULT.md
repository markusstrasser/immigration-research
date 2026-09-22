# Second generation by parental origin — IPUMS-CPS ASEC 1994–2025 (cluster-V V02)

**Verdict:** Mexican-origin gaps close substantially but not fully in the second generation, and
they close unevenly across the ladder: about three quarters of the first-generation deficit in
high-school completion is gone, but only about three tenths of the deficit in college completion.
Over 1994–2025 the Mexican second generation's college gap **widens** while its no-high-school gap
keeps narrowing, and its adjusted income gap is flat. For most other origins the first generation
is already at or above the third-plus non-Hispanic white reference, so there is no deficit to
close and the closing ratio is not an interpretable quantity. All five gates pass; 30 tests pass.

Model self-report: claude-opus-5[1m]

Universe: 2,874,753 civilian adults 25–64 from 32 ASEC samples, 1,696,418 households, `ASECWT`
weighted `[CALCULATION: derived/audit.json § universe]`. Reference group throughout: third-plus
generation, non-Hispanic white. All gaps are adjusted for age band × sex × survey year. Standard
errors are in parentheses and come from a 200-draw household-cluster bootstrap; they are **lower
bounds** (see Limits).

---

## 1. Mexico — the closing ratios

`[CALCULATION: derived/closing_ratios.csv, taxonomy region_gen_union, origin Mexico, period all]`

A closing ratio of 1 means the second generation has reached the reference; 0 means it has closed
nothing. Gaps are in the outcome's own units (percentage points for shares, log points for income).

| outcome | 1st-gen gap | 2nd-gen gap | closing ratio | 95% bootstrap interval | raw ratio |
|---|---|---|---|---|---|
| Bachelor's or more | −0.2984 (0.0010) | −0.2060 (0.0023) | **0.310 (0.0077)** | 0.293 – 0.326 | 0.396 |
| No high-school credential | +0.4964 (0.0015) | +0.1184 (0.0021) | **0.762 (0.0044)** | 0.753 – 0.768 | 0.797 |
| Employed | −0.1005 (0.0013) | −0.0408 (0.0023) | **0.594 (0.0227)** | 0.548 – 0.640 | 0.763 |
| Log total personal income | −0.5985 (0.0045) | −0.2047 (0.0079) | **0.658 (0.0134)** | 0.633 – 0.688 | 0.730 |
| Log wage and salary income | −0.5945 (0.0034) | −0.2212 (0.0055) | 0.628 (0.0091) | 0.609 – 0.646 | 0.690 |
| In the labor force | −0.0843 (0.0012) | −0.0287 (0.0022) | 0.659 (0.0268) | 0.607 – 0.712 | 0.955 |
| Women in the labor force | −0.2154 (0.0019) | −0.0315 (0.0031) | 0.854 (0.0147) | 0.827 – 0.883 | 0.968 |
| Any wage income | −0.0987 (0.0013) | −0.0297 (0.0024) | 0.699 (0.0242) | 0.654 – 0.745 | 1.006 |
| Coresident children, women 40–49 | +0.7835 (0.0092) | +0.2407 (0.0213) | 0.693 (0.0278) | 0.643 – 0.749 | 0.646 |

Unweighted counts behind the Mexico rows: 161,785 first generation and 50,183 second generation for
the share outcomes; 131,323 and 45,246 for log income `[CALCULATION: derived/closing_ratios.csv]`.

The education split is the finding. The bottom of the distribution converges fast — a Mexican
immigrant is 49.6 points more likely than the reference to hold no high-school credential, the
US-born child of Mexican immigrants only 11.8 points. The top does not: the 29.8-point college
deficit is still a 20.6-point deficit in the second generation, and the ratio 0.310 is estimated
tightly enough (bootstrap interval 0.293 – 0.326) that it is not a sampling artefact.

**Convergence appears to stall after the second generation.** Third-plus-generation adults who
self-identify as Mexican sit essentially where the second generation sits, not closer to the
reference `[CALCULATION: derived/adjusted_gaps.csv, region_gen_union, period all]`:

| outcome | 2nd gen (Mexican parent) | 3rd+ Mexican self-ID | 3rd+ other |
|---|---|---|---|
| Bachelor's or more | −0.2060 (0.0023) | −0.2013 (0.0018) | −0.1451 (0.0010) |
| No high-school credential | +0.1184 (0.0021) | +0.1147 (0.0017) | +0.0640 (0.0008) |
| Employed | −0.0408 (0.0023) | −0.0541 (0.0021) | −0.0924 (0.0011) |
| Log total personal income | −0.2047 (0.0079) | −0.2244 (0.0064) | −0.2035 (0.0034) |

Read that comparison with care. The third-plus self-identified group is defined by who still calls
themselves Mexican, and ethnic attrition is selective on exactly the outcomes in this table; this
lane measures the self-identified group and does not correct for it. `[INFERENCE]` The repo's
lineage work is at [`research/immigration-mexican-origin-by-generation-2026-09-16.md`](../../../research/immigration-mexican-origin-by-generation-2026-09-16.md).

## 2. Mexican second generation over three periods

`[CALCULATION: derived/period_trends.csv, region_gen_union, group Mexico|2nd_gen_all]`

| outcome | 1994–2004 | 2005–2014 | 2015–2025 | change, first to last |
|---|---|---|---|---|
| **level** Bachelor's or more | 0.1243 | 0.1658 | 0.2130 | **+0.0888** (0.0049) |
| **gap** Bachelor's or more | −0.1737 | −0.1956 | −0.2254 | **−0.0517** (0.0051) |
| **level** No high-school credential | 0.2490 | 0.1867 | 0.1184 | **−0.1306** (0.0052) |
| **gap** No high-school credential | +0.1685 | +0.1346 | +0.0850 | **−0.0835** (0.0053) |
| **level** Employed | 0.7351 | 0.7395 | 0.7610 | +0.0259 (0.0061) |
| **gap** Employed | −0.0510 | −0.0325 | −0.0390 | +0.0120 (0.0062) |
| **level** Log total personal income | 9.6686 | 10.0389 | 10.2458 | +0.5772 (0.0198) |
| **gap** Log total personal income | −0.2170 | −0.1611 | −0.2240 | −0.0070 (0.0205) |

In one line: the Mexican second generation gained 8.9 points of college completion and shed 13.1
points of no-high-school over three decades, yet its college gap to third-plus non-Hispanic whites
widened by 5.2 points because the reference group gained 12.0 points of college over the same
stretch `[CALCULATION: derived/period_trends.csv, group 3rd+_NH_white]`, while its
no-high-school gap narrowed by 8.4 points and its adjusted income gap did not move
(−0.007, SE 0.021).

The Mexican closing ratios themselves are stable across periods
`[CALCULATION: derived/closing_ratios.csv, origin Mexico]`:

| outcome | 1994–2004 | 2005–2014 | 2015–2025 |
|---|---|---|---|
| Bachelor's or more | 0.321 (0.016) | 0.335 (0.011) | 0.312 (0.011) |
| No high-school credential | 0.710 (0.008) | 0.743 (0.008) | 0.798 (0.007) |
| Employed | 0.615 (0.035) | 0.685 (0.039) | 0.503 (0.045) |
| Log total personal income | 0.657 (0.026) | 0.718 (0.020) | 0.627 (0.021) |

The first generation also improved over the same period: the Mexican first generation's
no-high-school rate fell from 0.654 to 0.464 and its college rate rose from 0.049 to 0.095
`[CALCULATION: derived/period_trends.csv, group Mexico|1st_foreign_born]`. Its naturalization rate
rose from 0.230 to 0.316 `[CALCULATION: derived/period_trends.csv, outcome us_citizen_g1]`.

## 3. Other origins — the closing ratio mostly does not apply

`[CALCULATION: derived/adjusted_gaps.csv, region_gen_union, period all]`, gap ÷ SE shown so the
sign is unambiguous. A positive college number means the first generation is **ahead** of the
third-plus non-Hispanic white reference.

| origin | college gap, 1st gen | t | college gap, 2nd gen | income gap, 1st gen | income gap, 2nd gen |
|---|---|---|---|---|---|
| Mexico | −0.2984 (0.0010) | −293 | −0.2060 (0.0023) | −0.5985 (0.0045) | −0.2047 (0.0079) |
| Central America | −0.2650 (0.0022) | −119 | −0.0823 (0.0071) | −0.4943 (0.0094) | −0.0576 (0.0192) |
| US outlying | −0.1723 (0.0034) | −50 | −0.1692 (0.0036) | −0.3666 (0.0108) | −0.1981 (0.0161) |
| Caribbean | −0.1237 (0.0025) | −49 | +0.0282 (0.0051) | −0.2753 (0.0086) | +0.0153 (0.0166) |
| South America | −0.0159 (0.0033) | −5 | +0.0781 (0.0080) | −0.2785 (0.0097) | +0.0990 (0.0228) |
| Europe | +0.1059 (0.0028) | +38 | +0.1068 (0.0022) | −0.0350 (0.0094) | +0.1467 (0.0079) |
| Africa | +0.0820 (0.0048) | +17 | +0.1736 (0.0130) | −0.1891 (0.0139) | +0.1466 (0.0383) |
| Canada | +0.1672 (0.0061) | +27 | +0.0709 (0.0055) | +0.0944 (0.0240) | +0.1146 (0.0164) |
| Asia | +0.1897 (0.0018) | +108 | +0.2110 (0.0039) | −0.1051 (0.0060) | +0.1817 (0.0128) |

Only Mexico, Central America, `US outlying` and the Caribbean have a first-generation college
deficit large enough for a closing ratio to mean anything. For Asia, Europe, Africa and Canada the
first generation is already ahead on education and the second generation is further ahead on
income, so the ratio's denominator is a surplus and the number in `closing_ratios.csv` should not
be read as convergence. The arithmetic breaks down visibly where the denominator is near zero:
Canada's employment ratio is 20.7 with a bootstrap SE of 2,290
`[CALCULATION: derived/closing_ratios.csv]`. Those rows are shipped as computed and flagged here,
not trimmed.

`US outlying` is the one group that barely moves: a −0.172 college gap in the first generation and
−0.169 in the second, a closing ratio of 0.018 (0.029). It is dominated by Puerto Rico-born adults,
who are US citizens by birth: Puerto Rico is 89.7% of that category's first-generation weight, from
19,915 of its 22,114 observations `[CALCULATION: derived/audit.json § us_outlying_composition]`.
IPUMS `NATIVITY` files them as foreign-born, which is why they appear in a first generation at all.

Among the ten largest single parental birthplaces, Mexico is the only one whose second generation
is still behind the reference on college completion
`[CALCULATION: derived/adjusted_gaps.csv, country_gen_union, period all]`. Second-generation
college gaps: China +0.354, Poland +0.195, Ireland +0.146,
Philippines +0.103, Germany +0.077, Canada +0.071, Cuba +0.067, Italy +0.061, England +0.053,
Mexico −0.206.

---

## Gates

| gate | result |
|---|---|
| G1 manifest sha256 | **PASS** — `a510e7a9695486945fc87618b98e2f8d51f7d0d7df35f01319a70564ea8065a2` matches `cps_2ndgen.manifest.json` before any read |
| G2 loader reproduction | **PASS** — 37/37 rows of `sources/immigration-fiscal/derived/lifetime/cps_second_gen_by_origin.csv` rebuilt, max abs diff **0.00e+00** against a 1e-9 tolerance |
| G3 population anchor | **PASS** — ASEC 2025 vs `gen_ledger_extension_2026_09_16`, worst relative difference **4.9e-08** against a 0.5% tolerance |
| G4 DDI codes | **PASS** — 17 code groups printed with their DDI labels and asserted; recorded in `derived/audit.json` |
| G5 cell floor and finite SEs | **PASS** — 3,296 cells, 3,172 gaps, 745 ratios reported, all at n ≥ 100 with finite SEs; 344 cells suppressed below the floor |

G3 detail `[CALCULATION: derived/audit.json § gates.G3_population_anchor]`, civilian adults 25–64:

| group | this lane | ledger | relative difference |
|---|---|---|---|
| mexico_born | 9,446,563 (n=4,318) | 9,446,563 (n=4,318) | 2.8e-08 |
| mexican_second_gen | 5,614,637 (n=2,452) | 5,614,636 (n=2,452) | 4.9e-08 |
| third_plus_nh_white | 87,647,855 (n=36,287) | 87,647,853 (n=36,287) | 2.5e-08 |
| mexican_third_plus_selfid | 5,526,182 (n=2,477) | 5,526,182 (n=2,477) | 1.4e-08 |

Every weighted least squares fit returned status `ok`; no rank-deficient fallback was taken
`[CALCULATION: derived/audit.json § wls_status]`.

### Verification commands

```
$ uv run --no-project python3 -m pytest infra/immigration-fiscal/second_generation_by_origin_2026_09_22/ -q
..............................                                           [100%]
30 passed in 0.51s
```

```
$ OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 \
    infra/immigration-fiscal/second_generation_by_origin_2026_09_22/analysis.py
[G1] manifest sha256
       PASS a510e7a9695486945fc87618b98e2f8d51f7d0d7df35f01319a70564ea8065a2
[G2] reproduce cps_second_gen_by_origin
       PASS 37 rows, max abs diff 0.00e+00
[G3] ASEC 2025 population anchor vs gen_ledger_extension_2026_09_16
       mexico_born                ipums      9,446,563 ledger      9,446,563  rel 2.80e-08
       mexican_second_gen         ipums      5,614,637 ledger      5,614,636  rel 4.94e-08
       third_plus_nh_white        ipums     87,647,855 ledger     87,647,853  rel 2.45e-08
       mexican_third_plus_selfid  ipums      5,526,182 ledger      5,526,182  rel 1.35e-08
[sample] 2014 by HFLAG: 0=313,395,422, 1=313,443,194; 2013/2015 2013=311,116,170,
         2015=316,167,949 -> dropping HFLAG=1
[load] analysis frame
       2,874,753 civilian adults 25-64, 32 ASEC years
[origins] top ten parental birthplaces: Mexico, Canada, Italy, Germany, Philippines,
          England, China, Cuba, Poland, Ireland
[origins] 'US outlying' first generation: 22,114 obs, largest is Puerto Rico at 89.7% of weight
       1,696,418 households, 512 age-band x sex x year cells, 83 fine groups
[estimate] point estimates
[bootstrap] 200 household-cluster draws, seed 20260922
       draw 200/200    36.6s
[G5] reporting floor and finite standard errors
       PASS 3296 cells, 3172 gaps, 745 ratios; 344 cells suppressed below n=100
[done] 37.3s
```

## Sample decisions that move the numbers

`[CALCULATION: derived/audit.json § sample_decisions]`

**The 2014 ASEC is in the extract twice.** The 5/8 traditional file weights to 313,395,422 and the
3/8 income-redesign file to 313,443,194, against 311,116,170 in 2013 and 316,167,949 in 2015.
Keeping both double counts 2014. This lane keeps `HFLAG = 0` so the income questions stay
comparable with 1994–2013. The loader table that gate G2 rebuilds double counted 2014 the same
way until 2026-09-22, when `build/load_cps_second_gen.py` received the same `HFLAG` rule and the
table was regenerated (the Mexican rows moved in the third decimal); G2 now reproduces the
corrected table exactly. This lane's own numbers still differ from the loader's because of the
civilian universe, the first-generation origin rule and the `US outlying` category.

Armed forces (`EMPSTAT` = 1) are dropped, matching the ledger's `PRPERTYP = 2` civilian-adult
universe. `NATIVITY = 0` is dropped. The first generation takes its origin from its own birthplace,
the second generation from the father's birthplace when he is foreign-born and the mother's
otherwise; the committed loader uses parental birthplace for everyone, first generation included.
Birthplaces in general codes 100–120 go to a tenth category, `US outlying`, which the loader's
nine-region map leaves unassigned.

## Limits

Copied from `derived/audit.json § limitations` without softening.

- Descriptive. Cross-sectional generation contrasts are not the same families followed over time;
  the first generation observed in a period is not the parent generation of the second generation
  observed in the same period.
- Origin-group differences confound selection into migration, cohort of arrival, destination, legal
  status and period with anything transmitted within families.
- Age and sex adjustment plus survey-year fixed effects remove composition on those margins only.
  Education, state of residence and legal status are NOT controlled, by design: they are outcomes
  or endogenous to the comparison.
- `NCHILD` counts coresident own children, not completed fertility (see
  [`research/immigration-gated-data-specs-2026-06-25.md`](../../../research/immigration-gated-data-specs-2026-06-25.md)
  section 1).
- `EDUC` is a categorical attainment code; college_plus and less_than_hs are shares built from the
  DDI code list, and no years-of-schooling scale is imputed.
- `INCTOT` and `INCWAGE` are nominal as reported, not deflated; survey-year fixed effects absorb
  the common price level within a year but period means in levels are not comparable across periods
  and only the gaps to the same-year reference are.
- Income means are conditional on positive income, so they mix a participation margin into the
  level; positive_wage is reported alongside for that reason.
- Standard errors ignore the CPS PSU design AND the CPS rotation panel (about half of each March
  sample returns the following March), so they are lower bounds twice over.
- IPUMS `NATIVITY` treats people born in US outlying areas and people born abroad to American
  parents as foreign-born, so a small number of US citizens by birth sit in the first generation
  here. The ledger's `PRCITSHP` rule treats them as native; that difference is why the G3 anchor
  uses `CITIZEN` rather than `NATIVITY`.
- The loader table reproduced in G2 (`build/load_cps_second_gen.py`; a local derived file under
  `sources/`, not tracked) kept both 2014 ASEC files until 2026-09-22 and now drops the 3/8
  redesign file as this lane does; its cells still differ from this lane's in universe (armed
  forces kept), origin rule (parental birthplace for the first generation too) and the missing
  `US outlying` category.

One limit not in the audit list, added here because section 1 invites the comparison: the
third-plus Mexican self-identified group is defined by self-report, and ethnic attrition selects on
the outcomes being measured. `[INFERENCE]`

## Files

Covered:

- `analysis.py` — gates, estimator, bootstrap, outputs. sha256 `04ef78587673ab13…` (after the
  2026-09-22 loader note; the estimator is unchanged and every number above reproduced)
  `[CALCULATION: derived/audit.json § analysis_py_sha256]`
- `test_analysis.py` — 30 tests: the weighted least squares shortcut against a dense dummy
  regression on synthetic data, the planted-gap and composition-confounding cases, the cluster
  bootstrap against an independent-person bootstrap, and the DDI code assertions
- `derived/cells.csv` (3,296), `derived/adjusted_gaps.csv` (3,172),
  `derived/closing_ratios.csv` (745), `derived/period_trends.csv` (834), `derived/audit.json`
- `README.md` — run instructions, definitions, estimator, gate table

Skipped, with reasons:

- **A years-of-schooling scale.** The brief asks for college-or-more and less-than-high-school
  shares from the `EDUC` codes. Converting the attainment codes to years would be an assumption
  that is not in the DDI, so it is not made.
- **Deflated income.** Nominal as reported; the brief specifies log `INCTOT` and log `INCWAGE` and
  the survey-year fixed effects handle the cross-sectional comparison. Level comparisons across
  periods are flagged as not comparable rather than silently deflated.
- **Replicate-weight standard errors.** The extract has no replicate weights, so the household
  bootstrap the brief specifies is the only option; it is reported as a lower bound rather than
  presented as a design-correct standard error.
- **Nothing outside this lane directory was written**, and no commit was made.

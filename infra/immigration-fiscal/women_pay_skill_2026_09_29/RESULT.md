claude-opus-5-5

**Verdict:** The NLSY97 does not support "women's pay, and the daughters' pay especially, is not tied to skill."

- **Where the premium sits.** Compare G2 Hispanic daughters with G3+ non-Hispanic white women at equal education and
  AFQT, at 35–40. Their hourly-pay premium is not concentrated in credential-pay sectors (government, education,
  health, social assistance). The sons show the same inside-versus-outside pattern.
- **Where the sex difference sits.** The daughters-minus-sons difference is +0.04 (0.11) inside those sectors and
  +0.10 (0.09) outside them.
- **Skill slope.** Women's pay rises with AFQT at least as steeply as men's.
- **Reference group.** White women with high-earning partners are paid more at equal skill, not less. Reweighting
  within marital-status cells leaves the daughters' premium at +0.15 (0.05); regression controls for marital status
  and partner earnings leave +0.14.
- **Test language.** Matching on the ASVAB math subtests alone (arithmetic reasoning plus mathematics knowledge)
  instead of AFQT leaves the premium at +0.127 (0.050). The daughters score about the same percentile on math as on
  verbal (38.8 against 37.8), so the verbal half of AFQT does not under-rate them.
- **Selection.** Employment at equal skill is not lower for the daughters. The premium survives non-workers placed
  at the bottom.
- **Place.** Region × urban status lowers the premium from 0.13 to 0.10 for daughters, and lowers the sons' gap by a
  similar 0.03.

[CALCULATION: `analyze.py` → `derived/*.csv`; Rao–Wu bootstrap over NLSY97 variance PSUs, 300 replicates, the
career lane's scheme and seed. Log hourly pay, worker person-years at 35–40, G2 Hispanic minus G3+ NH white of the
same sex, reference reweighted to G2 education × AFQT cells unless stated.]

| Test | Hypothesis predicts | Daughters | Sons |
|---|---|---|---|
| Premium, all workers | — | +0.134 (0.048), n=271 / 1,088 | +0.012 (0.048), n=269 / 1,213 |
| (a) Credential-pay sector | premium sits here | +0.164 (0.065), n=136 / 538 | +0.125 (0.097), n=52 / 254 |
| (b) All other sectors | premium vanishes | +0.096 (0.068), n=159 / 599 | −0.008 (0.055), n=220 / 986 |
| Pay–AFQT slope per 10 pctl points, G3+ white | women flatter | 0.092 (0.008) | 0.077 (0.008) |
| Premium within marital-status cells (reweighting) | premium shrinks | +0.151 (0.053), n=269 / 1,088 | +0.030 (0.055), n=267 / 1,213 |
| Premium with marital status + partner-earnings controls (regression) | premium shrinks | +0.138 (0.045) | +0.030 (0.047) |
| Premium at equal education × math-only score (AR + MK) | premium shrinks if verbal under-rates | +0.127 (0.050), n=324 / 1,274 | +0.009 (0.047), n=309 / 1,313 |
| Premium with region × CBSA status (regression) | — | +0.100 (0.055) | −0.027 (0.051) |
| Median premium, non-workers at the bottom | premium shrinks | +0.160 (0.053) | +0.057 (0.055) |

## Positive control

This lane's own pull of the archive reproduces the career lane's `derived/gaps.csv` exactly: all 288 cells
(25–27 and 35–40, raw, education and education × AFQT arms, both sexes, three target groups), estimate and SE to six
significant digits. `analyze.py` stops with `[BLOCKED]` if any cell differs. [CALCULATION: `derived/positive_control.csv`]

- G2 Hispanic women, education × AFQT arm, **total earnings including non-workers as zero**: +0.113 (0.055) at 25–27
  and +0.093 (0.069) at 35–40, n=330 and 324.
- **Same arm at 35–40, components:**
  - Employment: women +0.031 (0.030), men −0.027 (0.025).
  - Hourly pay: women **+0.134 (0.048)**, men +0.007 (0.048).
- **Which premium is tested.** The premium in question is an hourly-pay premium, so this lane tests hourly pay.
- **Meaning of "equal-AFQT".** It is the career lane's `edu_afqt` arm. The white reference is reweighted to the G2
  cells of education at 25 (five degree categories plus unknown) × AFQT tercile, with missing AFQT as its own tercile.

## Core test: is the daughters' premium in credential-pay sectors? (Task 3a/b, with the sons)

The subsets are worker person-years whose main job in that round is in the named sector. The career lane's
reweighting is done within each subset. [CALCULATION: `derived/sector_gaps.csv`]

| Subset | Daughters: raw | Daughters: educ. at 25 | Daughters: educ. × AFQT | Sons: educ. × AFQT | Daughters − sons, educ. × AFQT |
|---|---|---|---|---|---|
| All workers | −0.044 (0.046) | +0.083 (0.045) | +0.134 (0.048) | +0.012 (0.048) | +0.122 (0.066) |
| (a) Credential-pay sector | +0.002 (0.074) | +0.092 (0.066) | **+0.164 (0.065)** | +0.125 (0.097) | +0.039 (0.113) |
| (b) Other sectors | −0.093 (0.057) | +0.070 (0.057) | **+0.096 (0.068)** | −0.008 (0.055) | **+0.104 (0.090)** |
| (b′) Other sectors, employees only | −0.106 (0.060) | — | +0.105 (0.074) | −0.015 (0.047) | +0.120 (0.090) |
| (a) − (b) | +0.096 (0.089) | +0.022 (0.083) | +0.068 (0.090) | +0.133 (0.101) | — |
| Government employer only (small) | −0.003 (0.117) | +0.057 (0.104) | +0.118 (0.101) | +0.127 (0.129) | −0.009 (0.156) |

Sample sizes, G2 / reference persons:

| Subset | Daughters | Sons |
|---|---|---|
| All workers | 271 / 1,088 | 269 / 1,213 |
| (a) Credential-pay sector | 136 / 538 | 52 / 254 |
| (b) Other sectors | 159 / 599 | 220 / 986 |
| (b′) Other sectors, employees only | 144 / 520 | 189 / 858 |
| Government employer only | 66 / 215 | 36 / 168 |

- **Inside versus outside.** The credential-pay point estimate is larger for both sexes. The (a)−(b) difference is
  about one SE for both.
- **The daughters–sons difference** is where the credential-pay story would have to show, and it does not. It is
  +0.04 (0.11) inside credential-pay jobs and +0.10 (0.09) outside them.
- **Education at 25 only.** The daughters' premium is +0.070 outside those sectors and +0.092 inside.
- **Small cells.** Sons in the credential-pay sector (52) and the government-only cells are small and flagged
  `small_cell`.

## Task 5: the reference group (marital status and partner earnings)

**Fields, rounds 2013–2023.**

- **Marital status:** `CV_MARSTAT`, marital or cohabitation status at the interview (10 codes, collapsed here to
  four: married with spouse present; cohabiting; never married and not cohabiting; previously married or spouse
  absent and not cohabiting).
- **Partner earnings:** `YINC-2350` (any spouse or partner in the income year), `YINC-2400`/`2600` (partner's wage
  and salary income, the same calendar year as the respondent's pay) and the `YINC-2700` bracket midpoint where only
  a bracket was given ($300,000 for the open top).
- **Terciles** of partner earnings are taken among partnered worker-years at 35–40, per sex. For women the cuts are
  $40,000 and $75,000; for men, $20,000 and $50,000. The partner questions' universe is "R is married/living with
  partner".

[SOURCE: codebook `U34514.00`, `U42831.00`–`U42837.00`; CALCULATION: `derived/partner_shares.csv`]

| Women's worker-years at 35–40 | G3+ NH white | G2 Hispanic |
|---|---|---|
| Married, spouse present | 61.0% (1.6) | 57.6% (3.6) |
| Cohabiting | 13.4% (0.9) | 14.7% (2.1) |
| Never married, not cohabiting | 11.6% (1.0) | 13.9% (2.5) |
| Previously married or spouse absent, not cohabiting | 13.8% (1.0) | 13.1% (1.7) |
| Partner in the top earnings tercile (> $75,000) | 25.5% (1.2) | 18.0% (2.5) |

**(b) Controls for both groups.** Weighted regression over worker-years; n = 271 G2 / 1,088 white women and
269 / 1,213 men. [CALCULATION: `derived/partner_controls.csv`]

| Spec | Daughters | Sons |
|---|---|---|
| Education × AFQT cells | +0.132 (0.046) | +0.007 (0.047) |
| + marital/cohabitation status | +0.128 (0.046) | +0.032 (0.047) |
| + partner-earnings tercile | +0.138 (0.045) | +0.030 (0.047) |
| + region × CBSA status | +0.111 (0.054) | −0.003 (0.049) |

**Partner-earnings tercile coefficients (women, both groups pooled).** These are relative to no partner, at equal
education × AFQT and marital status:

- Top tercile: **+0.256 (0.054)**.
- Middle tercile: +0.067 (0.047).
- Bottom tercile: −0.043 (0.060).

Women with high-earning partners are paid more at equal measured skill, not less. That is assortative matching on
something the AFQT and degree cells miss, not a flexible-job discount. The daughters have fewer such partners
(18% against 26%), so holding partner earnings fixed raises their premium slightly.

**(b′) Within marital-status cells (reweighting).** Both groups are split into the four marital or cohabitation
statuses. In each status, the white reference is reweighted to the G2 education × AFQT cells. The status gaps are
then pooled with G2 worker-year shares. The same is done with partner-earnings cells. [CALCULATION:
`derived/partner_cells.csv`]

| Cell | Daughters, n G2 / ref | Daughters, educ. × AFQT | Sons, educ. × AFQT |
|---|---|---|---|
| Married, spouse present | 157 / 703 | +0.129 (0.068) | −0.002 (0.067) |
| Cohabiting | 62 / 206 | +0.177 (0.143) | +0.046 (0.099) |
| Never married, not cohabiting | 45 / 144 | +0.193 (0.122) | +0.086 (0.113) |
| Previously married or spouse absent, not cohabiting | 46 / 197 | +0.174 (0.154) | +0.017 (0.179) |
| **Pooled over marital cells** | 269 / 1,088 | **+0.151 (0.053)** | **+0.030 (0.055)** |
| No spouse or partner | 92 / 306 | +0.158 (0.114) | +0.067 (0.082) |
| Partner earnings, bottom tercile | 109 / 349 | +0.296 (0.092) | −0.031 (0.100) |
| Partner earnings, middle tercile | 102 / 439 | +0.133 (0.088) | −0.063 (0.076) |
| Partner earnings, top tercile | 63 / 361 | −0.082 (0.089) | +0.141 (0.113) |
| **Pooled over partner-earnings cells** | 270 / 1,088 | **+0.147 (0.050)** | **+0.030 (0.050)** |

- **Where the premium disappears.** The one cell with no daughters' premium is women whose partner is in the top
  earnings tercile, above $75,000. There, the white reference is the best-paid group of white women.
- **Pooled estimates.** Pooling within cells gives the same premium as the unconditional comparison, with or
  without the math-only score (`edu_math` rows: +0.134 over marital cells, +0.125 over partner cells).

**(a) Restricted white references.** [CALCULATION: `derived/partner_gaps.csv`]

| White reference / G2 sample | Daughters, educ. × AFQT | n G2 / ref | Sons, educ. × AFQT |
|---|---|---|---|
| All (baseline) | +0.134 (0.048) | 271 / 1,088 | +0.012 (0.048) |
| (a1) Ref never married, not cohabiting; all G2 | +0.248 (0.094) | 271 / 144 | +0.291 (0.066) |
| (a2) Ref not married or cohabiting; all G2 | +0.200 (0.072) | 271 / 339 | +0.197 (0.055) |
| (a3) Both not married or cohabiting | +0.170 (0.106) | 89 / 339 | +0.071 (0.079) |
| (a4) Both married or cohabiting | +0.122 (0.053) | 208 / 864 | +0.000 (0.056) |
| (a5) Ref with a top-tercile partner; all G2 | −0.129 (0.070) | 271 / 361 | −0.186 (0.066) |

- **Restricting the reference to unpartnered white women raises the premium,** for sons as much as daughters.
  Unpartnered white adults of either sex are paid less at equal skill. That group is selected low, so (a1) and (a2)
  are not fair benchmarks.
- **The like-for-like comparisons, (a3) and (a4),** keep the daughters' premium (+0.17, +0.12) and the sons' null.
- **The reference the hypothesis points to,** white women married to high earners, is the best-paid group, not a
  discounted one.

## Task 6: math-only test scores (the language test)

**Score construction.** The CAT-ASVAB subtest ability estimates are `ASVAB_{AR,MK,WK,PC}_ABILITY_EST_{POS,NEG}`,
theta with three implied decimals, split into a positive and a negative variable. The NLS AFQT recipe is rebuilt:

- Each subtest's theta becomes a weighted percentile within three-month birth cohorts.
- The math score is AR + MK, re-percentiled the same way; the verbal score is WK + PC.
- NLS used custom ASVAB weights; this uses the 1997 base weight.

[SOURCE: codebook `R97053.00`–`R97072.00`, `R98296.00`]

**Check.** The rebuilt full AFQT (MK + AR + 2 × verbal) correlates **0.99993** with the published
`ASVAB_MATH_VERBAL_SCORE_PCT` over 7,093 respondents. Only respondents with a published AFQT are scored, so the
missing-score cell is unchanged. [CALCULATION: `derived/test_scores.csv`]

Gap at 35–40 to G3+ NH white of the same sex, with the reference reweighted to education at 25 × score tercile:

| Arm | Daughters: hourly pay | Daughters: total earnings | Sons: hourly pay | Sons: total earnings |
|---|---|---|---|---|
| Education × AFQT | +0.134 (0.048) | +0.093 (0.069) | +0.007 (0.048) | −0.041 (0.059) |
| Education × math only (AR + MK) | **+0.127 (0.050)** | +0.081 (0.069) | +0.009 (0.047) | −0.032 (0.058) |
| Education × verbal only (WK + PC) | +0.127 (0.044) | +0.068 (0.066) | +0.008 (0.047) | −0.044 (0.059) |

n = 324 G2 / 1,274 white women and 309 / 1,313 men.

Weighted mean percentiles (1997 base weight, respondents with scores):

| | AFQT | Math | Verbal |
|---|---|---|---|
| G3+ NH white women (n=1,283) | 59.9 (1.0) | 57.9 (1.0) | 59.4 (1.0) |
| G2 Hispanic women (n=262) | 37.9 (2.3) | 38.8 (2.3) | 37.8 (2.3) |
| G3+ NH white men (n=1,371) | 56.8 (1.1) | 56.2 (1.1) | 55.6 (1.1) |
| G2 Hispanic men (n=269) | 35.5 (2.2) | 37.1 (2.3) | 34.6 (2.0) |

- **Math against verbal.** The daughters trail white women by about the same amount on math as on verbal (19 and 22
  points). Matching on math alone moves their premium by −0.006.
- **By sector.** The sector split is unchanged on math-only cells: credential-pay +0.158 (0.072), other sectors
  +0.088 (0.063), daughters minus sons +0.032 (0.118) inside and +0.097 (0.087) outside. [CALCULATION:
  `derived/sector_gaps.csv`, arm `edu_math`]
- **Conclusion.** Under-measurement through the verbal subtests does not explain the premium. [CALCULATION]

## Task 1: skill slope by sex

Weighted least squares of log hourly pay on AFQT percentile, per 10 percentile points, over worker person-years at
35–40 (the career lane's worker definition: positive earnings, 100+ hours, pay $2–$500), round weights. Degree is
the highest degree at that round. Respondents without an ASVAB score are dropped here only.
[CALCULATION: `derived/slopes.csv`]

| Group | Spec | Men | Women | Women − men |
|---|---|---|---|---|
| G3+ NH white | AFQT | 0.077 (0.008), n=1,037 | 0.092 (0.008), n=941 | +0.015 (0.011) |
| G3+ NH white | AFQT + degree | 0.038 (0.011) | 0.047 (0.009) | +0.009 (0.014) |
| G2 Hispanic | AFQT | 0.052 (0.018), n=191 | 0.093 (0.017), n=199 | +0.041 (0.026) |
| G2 Hispanic | AFQT + degree | 0.026 (0.020) | 0.059 (0.019) | +0.033 (0.028) |
| Pooled, all respondents | AFQT | 0.085 (0.005), n=2,522 | 0.090 (0.005), n=2,501 | +0.005 (0.008) |
| Pooled, all respondents | AFQT + degree | 0.047 (0.006) | 0.045 (0.005) | −0.003 (0.008) |

- **By sex.** Women's pay tracks AFQT as closely as men's. G2 Hispanic daughters' pay tracks it more closely than
  their brothers'.
- **By sector.** Without degree controls, the AFQT slope in the credential-pay sector is somewhat flatter than
  elsewhere: white women −0.024 (0.015), pooled women −0.013 (0.010). With degree held it is equal: +0.002 (0.017)
  and +0.007 (0.012). There, the return to test scores runs through the credential.
- **Level in those sectors.** Pay still rises with skill there: 0.079 (0.010) per 10 points for white women and
  0.107 (0.021) for G2 Hispanic women.

## Task 2: sector of the main job

**Main job.** `CV_MAINJOB_FLG` gives the roster loop of the current or most recent employer as of the interview
date, per the codebook ("the loop number listed corresponds to position of the job on the roster, in the created
variables, and in the questionnaire data"). It is verified in the codebook for rounds 2013–2023.

- **Industry and occupation** are the 2002 Census codes on that roster loop (`YEMP_INDCODE-2002`,
  `YEMP_OCCODE-2002`). 96–100% of main jobs have an industry code, by round.
- **Timing.** Pay is the career lane's calendar-year earnings over hours for the year before the interview, so the
  job and the pay year overlap without coinciding.

[SOURCE: NLSY97 1997–2023 codebook in the archive, `U34362.00`; DATA: `derived/main_job.csv`]

**Class of worker.** `YEMP-58500` (government / private for-profit / non-profit / unpaid family / armed forces) is
asked only of employers "not ongoing from DLI" and not self-employed. For a continuing employer, `analyze.py` carries
the latest earlier answer forward by employer ID (`YEMP_UID`, round-and-loop of first report), back to 1997.
Self-employment comes from the roster flag `YEMP_SELFEMP`.

- **Check.** 2023 is the only round with a roster class of worker for every employer (`YEMP_COW`). The carry-forward
  agrees with it on 4,781 of 4,819 employee main jobs (99.2%), and on 3,239 of 3,268 (99.1%) continuing employers,
  whose value came entirely from earlier rounds.
- **Coverage.** Class of worker is known for 95–97% of employee main jobs in each round.

[SOURCE: codebook `U37436.00`, `U37426.00`, `U62240.00`; DATA: `derived/main_job.csv`]

**Credential-pay sector** = 2002 Census industry 7860–7890 (education), 7970–8290 (health care), 8370–8470 (social
assistance), 9370–9590 (public administration) or 9670–9890 (military), or a government or armed-forces class of
worker in any industry.

Shares of worker person-years at 35–40, round weights. [CALCULATION: `derived/sector_shares.csv`]

| | G3+ NH white women | G2 Hispanic women | G3+ NH white men | G2 Hispanic men |
|---|---|---|---|---|
| Credential-pay sector | 47.0% (1.8) | 45.8% (3.6) | 19.2% (1.3) | 18.6% (2.5) |
| Government employer | 17.7% (1.4) | 21.3% (2.9) | 12.9% (1.1) | 13.1% (2.2) |
| Non-profit | 14.1% (1.1) | 8.6% (1.9) | 4.5% (0.5) | 5.1% (1.5) |
| Private for-profit | 54.7% (1.8) | 57.1% (3.3) | 68.8% (1.5) | 67.2% (2.6) |
| Self-employed | 9.8% (0.8) | 8.1% (1.5) | 11.5% (0.9) | 12.6% (1.7) |
| Class of worker unknown | 3.5% | 4.4% | 2.1% | 1.9% |
| Sector unknown (no industry code, not government) or no main job | 2.4% | 1.2% | 3.0% | 2.6% |
| Worker-years (persons) | 2,496 (1,088) | 598 (271) | 2,783 (1,213) | 568 (269) |

- **By sex.** Women hold 2.4 times men's share of credential-pay jobs.
- **Daughters against white women.** There is no difference, apart from a government share 3.6 points higher,
  within about one SE.
- **By industry,** G2 Hispanic and white women are similar:

  | Industry | G2 Hispanic women | G3+ NH white women |
  |---|---|---|
  | Education | 14.9% | 16.4% |
  | Health care | 19.1% | 20.0% |
  | Social assistance | 4.1% | 3.8% |
  | Public administration | 5.9% | 4.3% |

## Task 3c: place (both sexes)

This is a weighted regression over worker-years with education × AFQT cell fixed effects. For daughters it returns
+0.132 (0.046) where the reweighting gave +0.134. [CALCULATION: `derived/place_gaps.csv`]

| Spec | Daughters | Sons |
|---|---|---|
| Education × AFQT cells | +0.132 (0.046) | +0.007 (0.047) |
| + census region | +0.106 (0.052) | −0.023 (0.051) |
| + region × CBSA status | +0.100 (0.055) | −0.027 (0.051) |
| + region × CBSA status + credential-pay sector | +0.102 (0.054) | −0.023 (0.051) |

- **Same shift for both sexes.** 44% of G2 Hispanic women's worker-years and 41% of G2 Hispanic men's are in the
  West, against 17–19% of white workers'. Place lowers both sexes' gap by about 0.03, so it cannot explain the
  daughters–sons difference.
- **Geography limit.** The public file has no state or metro identifiers, so a California or big-Texas-metro wage
  level beyond the regional average stays in both sexes' gaps. [DATA: codebook `U34516.00`, CV_MSA is CBSA
  residence status only; GAP]

## Task 4: selection (short check)

Employment at equal education and AFQT is not lower for the daughters: +0.031 (0.030) in log share with positive
earnings at 35–40. [CALCULATION: `derived/positive_control.csv`]

**Median check.** Person-level mean log hourly pay at 35–40, weighted medians, with the reference reweighted to G2
cells. Non-workers were interviewed with valid earnings in the window but had no worker-year there. The median
premium is:

- **Workers only:** +0.127 (0.053), n=271 / 1,088.
- **Non-workers placed below the median (the bound):** +0.160 (0.053), n=324 / 1,274. Comparable white women
  include more non-workers than the daughters, 19.7% against 15.9%.
- **Neal-2004-style rule:** +0.131 (0.056). It uses mean pay at 31–34 or 41–42 where observed. Failing that, it
  imputes below the median when the last degree is high school or less, and drops the rest.

For sons the bound gives +0.057 (0.055). [CALCULATION: `derived/selection.csv`]

**Rule sources.**

- **Neal and Johnson 1996.** The citation is verified: "The Role of Premarket Factors in Black-White Wage
  Differences", *JPE* 104(5):869–895, doi:10.1086/262045. [SOURCE: Crossref] Their median-regression assumption,
  that non-participants' offers lie below the median, is taken from MIT 14.662 (2015) lecture 20 notes.
  [SOURCE: ocw.mit.edu MIT14_662S15_lecnotes20.pdf] The NBER w4968 PDF is an image scan that extracts as garbled
  text, so I did not read the paper's own rule.
- **Neal 2004.** Its selective rule is taken from Albrecht, van Vuuren and Vroman. [SOURCE: IZA DP 8005]

## What remains, and what would change it

- **Named explanations tested:**
  - credential-pay sector;
  - the pay–AFQT slope;
  - employment selection;
  - marital status and partner earnings;
  - region × urban status;
  - verbal under-measurement (math-only matching).

  None removes the daughters' premium or the daughters–sons difference. [CALCULATION]
- **Still untested: skills the ASVAB does not measure at all,** such as grades and non-cognitive traits. The
  archive has a self-reported average letter grade for the most recent school year (`ASVAB_AVG_GRADE_REC`), not used
  here. [GAP]
- **Untested: metro wage levels within the West.** This needs the restricted geocode file. [GAP]
- **Occupation within sector.** Occupation is extracted but not used. [GAP]
- **Scope.** Hispanic means 1997 screener ethnicity, 57–62% Mexican origin (career lane). The cohort is 1980–84
  births. All results are descriptive. [DATA: career lane `person_counts.csv`]
- **Timing.** The job and marital status are as of the interview; pay and partner earnings are for the calendar year
  before. [INFERENCE]

## Coverage

- **Done.**
  - Positive control.
  - Tasks 1–4.
  - Parent correction (BRIEF.md, dated section): selection reduced to a short check, place framed for both sexes,
    the sector split run for sons, and Task 5.
- **Parent correction 2 (BRIEF.md, dated section).**
  - Task 5 was already present; within-cell reweighting (5b′) was added.
  - Task 6, the math-only test, was added.
- **Additions not in the brief.**
  - Sector-split slopes.
  - Employee-only and government-only subsets.
  - Daughters-minus-sons differences with bootstrap SEs.
  - Partner-earnings coefficients.
- **Skipped.**
  - A median regression with covariates. The environment has no scipy or statsmodels, and the validation command
    uses no extra wheels. Reweighting to cells is used instead.
  - Metro identity. It is not in the public file.
  - Occupation analysis.
- **Fields.** 1,056 fields (`derived/field_inventory.csv`). Every field's count of non-skipped values equals the
  codebook total, asserted in `extract.py`.
- **Reproduction.**
  - `extract.py` streams the archive CSV in 1,000-row chunks from inside the zip, about 4 minutes. It ran three
    times (1,018, 1,048, then 1,056 fields). After each new pull, every earlier analysis CSV was byte-identical to
    the previous run's, except the files that gained new rows (`field_inventory.csv`; `sector_gaps.csv` gained the
    `edu_math` arm).
  - `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/women_pay_skill_2026_09_29/analyze.py`
    exits 0 in about 3 s. Two consecutive runs leave all 13 `derived/*.csv` byte-identical (shasum).

## Log

- 2026-09-29 02:34 JST — stub written.
- 2026-09-29 02:44 JST — `extract.py` ran: 1,018 fields; all non-skip counts match the codebook.
- 2026-09-29 02:49 JST — `analyze.py` ran: positive control 288/288 identical; Tasks 1–4. Rerun identical.
- 2026-09-29 02:55 JST — parent correction received and quoted in BRIEF.md; marital and partner fields added
  (1,048 fields, counts match); Task 5, sons' sector split and sex differences run; rerun identical; RESULT
  restructured.
- 2026-09-29 02:58 JST — parent correction 2 quoted in BRIEF.md. Added ASVAB subtest thetas (1,056 fields, counts
  match), Task 6 math-only and verbal-only arms (rebuilt AFQT r=0.99993), and Task 5b′ within-cell reweighting.
  Rerun: exit 0, 13/13 identical.

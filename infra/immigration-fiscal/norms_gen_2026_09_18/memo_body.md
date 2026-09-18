claude-opus-5[1m]

# Institutions and liberal-democratic norms by generation — Hispanic and Mexican-origin Americans against non-Hispanic whites and white subgroups

**Verdict:** On institutional confidence there is no deficit to converge from: Hispanic and Mexican-origin first-generation respondents are *more* confident in American institutions than non-Hispanic whites, and the third-plus generation lands at parity (adjusted gap on the 13-institution index +0.001 scale points, SE 0.018). On civil liberties there is a large first-generation deficit that closes to the level of white conservatives and white non-graduates by the third generation (Stouffer 15-item scale, adjusted: G1 −1.58, G3+ −0.42 against whites overall, −0.03 against white conservatives, −0.28 against white non-graduates). On police violence Hispanics are *less* approving than whites at every generation. What does not converge is the economic role of government, and that gap is about a fifth of the internal white ideological spread on the same items. The one measured norm that stays outside the white range is endorsement of political violence in the American National Election Studies, +10.1 points adjusted at the third generation against a white conservative-to-liberal spread of 8.3 points; that item is also the one with the best-documented measurement problems. A large share of the apparent first-generation deficit is response style rather than attitude: first-generation respondents differentiate far less between survey scenarios, and that differentiation gap closes across generations alongside the substantive gaps. Run on Mexican-origin respondents alone the pattern reproduces, with one exception: on the anti-American Muslim clergyman items the Mexican-origin third generation is still −0.25 scale points below whites overall (SE 0.09) and has not reached the white-non-graduate level.

Model self-report: `claude-opus-5[1m]`, running as the `norms_gen_2026_09_18` lane.

## Frame

These are stated survey attitudes, not behaviour. Nothing here measures whether anyone obeys a law, serves on a jury, accepts an election result or commits an act of violence. Attitude items of this kind predict behaviour weakly and are sensitive to wording, language, mode and social desirability; the response-style evidence in section A6 shows that sensitivity operating inside this very sample. [FRAMING-SENSITIVE]

The comparison is deliberately not "Hispanics versus an idealised white American". Non-Hispanic whites are internally heterogeneous by ideology and education, often more so than the Hispanic-white difference being tested, so every adjusted table below also reports the gap against white conservatives, white liberals and whites without a bachelor's degree, and reports the white conservative-to-liberal and graduate-to-non-graduate spread on the same item as a yardstick. Where the white internal spread on an item is near zero, a ratio to it is meaningless and is not used.

Cross-sectional generations are not lineages. Third-generation Hispanics observed in 2000-2024 descend from earlier migration cohorts, not from today's first generation, and ethnic attrition means the most assimilated descendants of Hispanic immigrants are the least likely to still identify as Hispanic. That biases the measured third generation *away* from convergence, so the convergence results below are conservative and the non-convergence results are upper bounds. [INFERENCE, standard in the Duncan-Trejo literature; see confidence-ladder entry 107 on the Pew identity-selection evidence]

## Data and method

**GSS 1972-2024 cumulative, release R3a** [SOURCE: `raw/GSS_stata/gss7224_r3a.dta`, obtained by the `attitudes_gen_2026_09_16` lane from https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip]. The analysis window is **2000-2024**, thirteen survey rounds, because `HISPANIC` (Hispanic specific origin, with `2` = Mexican, Mexican American, Chicano) does not exist before 2000. The institutional-confidence and Stouffer batteries themselves run back to the early 1970s, but no Hispanic identifier accompanies them, so the earlier rounds cannot enter. [SOURCE: GSS codebook; variable present-by-year check in `derived/item_coverage.csv`]

**ANES 2020 and 2024 time series**, the public CSV releases held locally by the prior lane [SOURCE: `raw/anes_timeseries_2020_csv_20220210/`, `raw/anes_timeseries_2024_csv_20260519/`]. Every ANES variable identifier below was read out of the shipped user-guide codebook PDFs by `cb_index.py`, never recalled; the extracted index is `derived/cb_index.json`.

**Generation coding** is reused verbatim from the prior lane, including the repair recorded at confidence-ladder entry 110: GSS `PARBORN` codes 3, 5 and 7 do not establish a foreign-born parent and leave generation unknown rather than assigning second generation. G1 is foreign-born (`BORN=2`); G2 is US-born with at least one foreign-born parent (`PARBORN` in 1, 2, 4, 6, 8); G3+ is US-born with both parents US-born (`PARBORN=0`). Unknown-generation respondents are excluded from every named group, whites included. ANES uses respondent birthplace and parental nativity the same way.

**Weights and variance.** GSS uses `WTSSNRPS`, NORC's nonresponse-adjusted post-stratification weight, with `WTSSPS` for 2000 and 2002 where the former does not exist. Variance is the stratified with-replacement design estimator over `VSTRAT` and `VPSU`, summing each stratum's centred PSU influence squares with the `n_h/(n_h−1)` factor, all 1,146 full-sample strata and 5,837 PSUs retained with zero influence outside each analysis domain. This is the design contract established by the `frontier_execution_2026_09_17/social` lane and recorded at confidence-ladder entry 117. ANES uses the full-sample pre-election weight for pre-election items and the post-election weight for post-election items, with the ANES variance stratum and variance unit.

**Adjusted models** are weighted least squares with design-linearised standard errors, so any linear contrast between coefficients carries its own correct standard error. Controls are age, age squared, years of education, log constant-dollar family income with a missingness flag, and survey-year fixed effects built inside each estimation sample. Education is a mediator of assimilation as well as a confounder, so raw and adjusted are both reported throughout; the honest reading lies between them. For the education-subgroup comparison the education control is dropped, since education is the splitting variable there.

**Gates.** Three, all passing before any result below was read.

1. The vectorised design-covariance implementation reproduces the explicit stratum loop to 1.6e-11 on random influence matrices (`gate_var.py`).
2. The full estimation stack reproduces the `frontier_execution_2026_09_17/social` adjusted GSS trust gaps to within 0.004 percentage points on both coefficient and standard error: −11.811 (1.546), −11.217 (2.008), −9.726 (1.990) against that lane's published −11.81 (1.55), −11.22 (2.01), −9.73 (1.99), n = 13,912 (`gate_prior.py`).
3. The ANES loader reproduces nine pooled means and standard errors from `attitudes_gen_2026_09_16/anes_gen_results.csv`, including the net in-group thermometer by generation and the white third-plus immigration-restriction share (`gate_anes.py`). The weighted Hispanic generation shares reproduce exactly: 2020 gives .276 / .334 / .389 and 2024 .282 / .399 / .319.

**Cell sizes.** Mexican-origin cells are thin and get thinner on split-ballot modules. On the confidence and tolerance batteries Mexican-origin cells run 263-625 per generation, which is usable. On the 2004 / 2014 / 2024 ISSP national-identity module they run 25-109, which is not; those tables are reported with all-Hispanic pooling alongside (46-212 per generation) and should be read as suggestive. Every cell carries its unweighted n in the tables. `AMIMP`, `AMPROUD` and `ETHSPKOK` are absent from release R3a and could not be run [SOURCE: `derived/item_coverage.csv`].

---

## A1. Confidence in institutions

The first generation is *more* confident in American institutions than native non-Hispanic whites, on eleven of thirteen institutions, and confidence falls toward the white level across generations. On the three-branch government index the adjusted first-generation premium is +0.287 scale points (SE 0.020) on a 1-3 scale, the third-plus generation +0.040 (0.025). On the all-thirteen index the third-plus gap is +0.001 (0.018): exact parity. The generational decline is precise, not a wash: third-plus minus first is −0.119 (0.022) on the thirteen-item index and −0.248 (0.030) on the government index.

Two institutions break the pattern. Confidence in the **military** is lower among Hispanics at every generation and does not converge (adjusted G3+ −8.6 points, SE 2.3). Confidence in **Congress** starts far above the white level (20.0 percent versus 6.2 saying "a great deal") and falls most of the way by the third generation.

The white internal spread is the yardstick. On the thirteen-institution index the entire white conservative-to-liberal difference is −0.038 scale points, so the first-generation Hispanic premium of +0.109 over white liberals is roughly three times the whole white ideological range on that measure. On the military, where whites genuinely divide, the conservative-to-liberal spread is 19.2 points and Hispanic third-plus respondents sit at the white-liberal end (+3.2 against white liberals, −16.1 against white conservatives).

### A1 raw. Share saying 'a great deal' of confidence, percent (design SE, unweighted n)

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Executive branch of the federal government | 17.0 (1.9) 601 | 12.0 (1.9) 433 | 18.7 (2.5) 485 | 18.2 (1.3) 1165 | 12.4 (1.5) 662 | 16.2 (1.8) 817 | 12.5 (0.4) 13097 | 16.6 (0.8) 3443 | 11.6 (0.6) 4873 | 10.8 (0.4) 8638 | 16.5 (0.7) 4448 |
| Congress | 21.2 (2.1) 593 | 13.1 (2.1) 430 | 12.5 (2.1) 490 | 20.0 (1.4) 1164 | 11.9 (1.5) 659 | 10.0 (1.5) 821 | 6.2 (0.3) 13097 | 5.8 (0.6) 3451 | 5.8 (0.4) 4875 | 6.8 (0.4) 8628 | 4.7 (0.4) 4458 |
| US Supreme Court | 31.3 (2.4) 589 | 25.0 (2.6) 431 | 29.1 (2.8) 490 | 32.5 (1.7) 1154 | 25.8 (2.1) 663 | 26.0 (2.1) 817 | 27.6 (0.5) 13014 | 24.0 (0.9) 3435 | 30.9 (0.9) 4853 | 25.2 (0.6) 8553 | 33.1 (0.9) 4450 |
| The military | 43.1 (2.5) 604 | 42.4 (3.0) 435 | 45.7 (2.8) 490 | 45.5 (1.7) 1185 | 45.8 (2.5) 665 | 44.4 (2.2) 823 | 53.6 (0.6) 13155 | 40.4 (1.1) 3457 | 61.0 (0.9) 4886 | 55.9 (0.7) 8696 | 48.1 (0.9) 4448 |
| The press | 10.7 (1.5) 605 | 11.9 (2.1) 438 | 11.1 (1.8) 496 | 13.3 (1.2) 1184 | 10.9 (1.6) 668 | 10.1 (1.4) 829 | 7.6 (0.3) 13144 | 14.2 (0.8) 3455 | 3.8 (0.3) 4884 | 6.8 (0.3) 8680 | 9.6 (0.6) 4453 |
| The scientific community | 37.6 (2.5) 583 | 37.4 (2.9) 429 | 46.0 (2.8) 485 | 38.4 (1.8) 1148 | 38.9 (2.3) 658 | 45.3 (2.2) 808 | 44.2 (0.6) 12827 | 62.5 (1.1) 3414 | 35.0 (0.9) 4782 | 38.9 (0.7) 8386 | 56.5 (1.0) 4430 |
| Education | 40.5 (2.6) 617 | 31.0 (2.9) 444 | 27.4 (2.4) 490 | 39.3 (1.8) 1206 | 29.3 (2.3) 681 | 26.3 (2.0) 824 | 20.3 (0.4) 13184 | 23.2 (1.0) 3462 | 17.0 (0.7) 4886 | 20.8 (0.5) 8726 | 19.1 (0.7) 4447 |
| Major companies | 15.0 (1.7) 601 | 14.3 (2.1) 433 | 17.5 (2.0) 494 | 15.2 (1.2) 1168 | 13.8 (1.6) 666 | 16.8 (1.6) 828 | 18.2 (0.4) 13042 | 12.4 (0.7) 3428 | 23.0 (0.8) 4842 | 16.4 (0.5) 8606 | 22.4 (0.8) 4425 |
| Banks and financial institutions | 17.2 (1.8) 614 | 18.8 (2.3) 444 | 18.8 (2.4) 492 | 20.8 (1.5) 1205 | 19.0 (1.9) 675 | 18.2 (1.9) 827 | 19.3 (0.4) 13183 | 14.5 (0.8) 3458 | 21.6 (0.8) 4894 | 19.5 (0.5) 8719 | 18.8 (0.7) 4453 |
| Organised religion | 24.4 (2.0) 603 | 20.3 (2.6) 434 | 21.3 (2.3) 490 | 23.7 (1.5) 1175 | 18.7 (2.0) 665 | 18.2 (1.7) 821 | 19.1 (0.5) 12942 | 11.5 (0.7) 3418 | 25.1 (0.8) 4807 | 19.4 (0.5) 8525 | 18.2 (0.7) 4406 |
| Medicine | 44.2 (2.5) 620 | 36.2 (3.1) 443 | 41.7 (3.0) 492 | 41.9 (1.8) 1214 | 36.0 (2.5) 678 | 37.8 (2.3) 827 | 37.9 (0.5) 13186 | 44.1 (1.1) 3454 | 35.1 (0.9) 4886 | 34.8 (0.7) 8720 | 45.1 (0.9) 4455 |
| Organised labour | 16.5 (2.1) 548 | 18.5 (2.4) 409 | 17.0 (2.2) 455 | 16.9 (1.5) 1063 | 18.1 (1.9) 624 | 14.8 (1.6) 765 | 12.5 (0.4) 12139 | 16.3 (0.9) 3210 | 9.3 (0.6) 4511 | 13.5 (0.5) 8020 | 9.9 (0.6) 4108 |
| Television | 10.3 (1.5) 619 | 11.9 (2.1) 440 | 11.4 (1.6) 494 | 10.3 (1.0) 1214 | 11.2 (1.6) 672 | 10.9 (1.3) 829 | 8.0 (0.3) 13148 | 9.2 (0.6) 3440 | 5.4 (0.4) 4889 | 8.8 (0.4) 8707 | 5.9 (0.4) 4430 |

### A1 raw. Confidence indices, 1-3 scale where 3 is a great deal

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Index: executive + Congress + Supreme Court (1-3) | 2.021 (0.027) 572 | 1.875 (0.032) 418 | 1.851 (0.037) 478 | 2.020 (0.019) 1114 | 1.872 (0.025) 642 | 1.809 (0.028) 802 | 1.772 (0.006) 12860 | 1.784 (0.011) 3404 | 1.755 (0.010) 4806 | 1.749 (0.007) 8422 | 1.824 (0.009) 4427 |
| Index: all 13 institutions (1-3) | 2.045 (0.018) 493 | 1.978 (0.024) 373 | 1.985 (0.024) 419 | 2.048 (0.014) 947 | 1.969 (0.018) 573 | 1.951 (0.019) 708 | 1.953 (0.004) 11310 | 1.967 (0.007) 3043 | 1.927 (0.007) 4248 | 1.939 (0.005) 7344 | 1.986 (0.006) 3955 |

### A1 raw. Three-point confidence means, 3 = a great deal and 1 = hardly any

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Executive branch of the federal government | 1.91 (0.03) 601 | 1.79 (0.04) 433 | 1.80 (0.04) 485 | 1.92 (0.02) 1165 | 1.81 (0.03) 662 | 1.75 (0.03) 817 | 1.68 (0.01) 13097 | 1.79 (0.02) 3443 | 1.61 (0.01) 4873 | 1.64 (0.01) 8638 | 1.76 (0.01) 4448 |
| Congress | 1.98 (0.03) 593 | 1.79 (0.04) 430 | 1.73 (0.04) 490 | 1.95 (0.02) 1164 | 1.78 (0.03) 659 | 1.66 (0.03) 821 | 1.57 (0.01) 13097 | 1.58 (0.01) 3451 | 1.53 (0.01) 4875 | 1.58 (0.01) 8628 | 1.55 (0.01) 4458 |
| US Supreme Court | 2.18 (0.03) 589 | 2.04 (0.04) 431 | 2.05 (0.04) 490 | 2.18 (0.02) 1154 | 2.04 (0.03) 663 | 2.01 (0.03) 817 | 2.07 (0.01) 13014 | 1.98 (0.02) 3435 | 2.13 (0.01) 4853 | 2.03 (0.01) 8553 | 2.16 (0.01) 4450 |
| The military | 2.32 (0.03) 604 | 2.26 (0.04) 435 | 2.33 (0.04) 490 | 2.35 (0.02) 1185 | 2.30 (0.03) 665 | 2.30 (0.03) 823 | 2.46 (0.01) 13155 | 2.25 (0.02) 3457 | 2.56 (0.01) 4886 | 2.48 (0.01) 8696 | 2.40 (0.01) 4448 |
| The press | 1.74 (0.03) 605 | 1.68 (0.04) 438 | 1.65 (0.04) 496 | 1.76 (0.02) 1184 | 1.66 (0.03) 668 | 1.60 (0.03) 829 | 1.57 (0.01) 13144 | 1.81 (0.01) 3455 | 1.38 (0.01) 4884 | 1.54 (0.01) 8680 | 1.64 (0.01) 4453 |
| The scientific community | 2.27 (0.03) 583 | 2.30 (0.04) 429 | 2.35 (0.04) 485 | 2.28 (0.02) 1148 | 2.33 (0.03) 658 | 2.35 (0.03) 808 | 2.37 (0.01) 12827 | 2.59 (0.01) 3414 | 2.25 (0.01) 4782 | 2.30 (0.01) 8386 | 2.53 (0.01) 4430 |
| Education | 2.30 (0.03) 617 | 2.15 (0.04) 444 | 2.09 (0.04) 490 | 2.28 (0.02) 1206 | 2.12 (0.03) 681 | 2.06 (0.03) 824 | 2.00 (0.01) 13184 | 2.10 (0.01) 3462 | 1.91 (0.01) 4886 | 2.00 (0.01) 8726 | 2.01 (0.01) 4447 |
| Major companies | 1.94 (0.03) 601 | 1.94 (0.03) 433 | 1.96 (0.03) 494 | 1.93 (0.02) 1168 | 1.93 (0.03) 666 | 1.93 (0.03) 828 | 2.00 (0.01) 13042 | 1.87 (0.01) 3428 | 2.08 (0.01) 4842 | 1.97 (0.01) 8606 | 2.08 (0.01) 4425 |
| Banks and financial institutions | 1.91 (0.03) 614 | 1.94 (0.04) 444 | 1.93 (0.04) 492 | 1.97 (0.02) 1205 | 1.93 (0.03) 675 | 1.89 (0.03) 827 | 1.96 (0.01) 13183 | 1.84 (0.01) 3458 | 2.02 (0.01) 4894 | 1.95 (0.01) 8719 | 1.97 (0.01) 4453 |
| Organised religion | 2.00 (0.03) 603 | 1.92 (0.04) 434 | 1.91 (0.04) 490 | 1.98 (0.03) 1175 | 1.90 (0.03) 665 | 1.85 (0.03) 821 | 1.92 (0.01) 12942 | 1.70 (0.01) 3418 | 2.06 (0.01) 4807 | 1.91 (0.01) 8525 | 1.92 (0.01) 4406 |
| Medicine | 2.34 (0.03) 620 | 2.24 (0.04) 443 | 2.24 (0.04) 492 | 2.30 (0.02) 1214 | 2.23 (0.03) 678 | 2.20 (0.03) 827 | 2.26 (0.01) 13186 | 2.35 (0.02) 3454 | 2.23 (0.01) 4886 | 2.21 (0.01) 8720 | 2.38 (0.01) 4455 |
| Organised labour | 1.97 (0.03) 548 | 2.01 (0.04) 409 | 1.98 (0.04) 455 | 1.96 (0.02) 1063 | 2.01 (0.03) 624 | 1.95 (0.03) 765 | 1.83 (0.01) 12139 | 1.99 (0.01) 3210 | 1.70 (0.01) 4511 | 1.86 (0.01) 8020 | 1.78 (0.01) 4108 |
| Television | 1.74 (0.03) 619 | 1.70 (0.04) 440 | 1.71 (0.03) 494 | 1.74 (0.02) 1214 | 1.66 (0.03) 672 | 1.68 (0.03) 829 | 1.63 (0.01) 13148 | 1.70 (0.01) 3440 | 1.51 (0.01) 4889 | 1.65 (0.01) 8707 | 1.58 (0.01) 4430 |

### A1 adjusted. Gap in the 'great deal' share, percentage points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Executive branch of the federal government | +8.2 (1.4) | +0.9 (1.7) | +4.7 (1.9) | -3.5 (2.3) | +8.0 (2.0) | +0.7 (2.1) | +7.2 (2.5) |
| Congress | +12.3 (1.5) | +3.7 (1.6) | +2.4 (1.4) | -9.9 (2.0) | +13.2 (2.1) | +4.7 (2.1) | +4.6 (2.0) |
| US Supreme Court | +10.0 (1.8) | +1.2 (2.2) | +1.0 (2.1) | -9.0 (2.6) | +10.5 (2.4) | +1.1 (2.6) | +4.1 (2.7) |
| The military | -10.6 (1.9) | -7.7 (2.7) | -8.6 (2.3) | +2.0 (2.8) | -15.3 (2.7) | -11.4 (3.2) | -7.8 (2.9) |
| The press | +5.9 (1.2) | +3.7 (1.7) | +2.7 (1.4) | -3.2 (1.7) | +3.9 (1.5) | +4.7 (2.2) | +3.7 (1.8) |
| The scientific community | +2.4 (2.0) | -5.3 (2.6) | +2.2 (2.2) | -0.3 (2.8) | +4.6 (2.6) | -6.3 (3.2) | +3.3 (2.6) |
| Education | +16.9 (1.8) | +7.3 (2.3) | +5.4 (2.0) | -11.5 (2.5) | +17.8 (2.6) | +9.0 (2.9) | +6.1 (2.4) |
| Major companies | +0.3 (1.4) | -2.5 (1.7) | -0.2 (1.7) | -0.5 (2.1) | +1.4 (1.9) | -1.3 (2.1) | +0.4 (2.2) |
| Banks and financial institutions | +2.8 (1.6) | -0.7 (2.0) | -1.2 (1.8) | -4.0 (2.2) | -0.2 (2.0) | -1.3 (2.4) | -1.0 (2.3) |
| Organised religion | +5.7 (1.6) | +2.2 (2.0) | +1.0 (1.7) | -4.7 (2.3) | +7.1 (2.2) | +3.9 (2.6) | +3.7 (2.2) |
| Medicine | +8.8 (2.0) | -2.8 (2.6) | +0.5 (2.3) | -8.3 (2.8) | +13.3 (2.6) | -2.3 (3.3) | +4.4 (2.8) |
| Organised labour | +2.2 (1.6) | +1.4 (2.0) | -0.1 (1.6) | -2.4 (2.2) | +0.8 (2.3) | +0.8 (2.5) | +1.7 (2.2) |
| Television | -0.3 (1.1) | +1.3 (1.7) | +1.6 (1.4) | +1.9 (1.6) | -1.0 (1.5) | +1.5 (2.2) | +1.7 (1.7) |

### A1 adjusted. Confidence indices, scale points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Index: executive + Congress + Supreme Court (1-3) | +0.287 (0.020) | +0.093 (0.027) | +0.040 (0.025) | -0.248 (0.030) | +0.304 (0.028) | +0.100 (0.033) | +0.076 (0.033) |
| Index: all 13 institutions (1-3) | +0.120 (0.015) | +0.010 (0.019) | +0.001 (0.018) | -0.119 (0.022) | +0.126 (0.018) | +0.021 (0.024) | +0.029 (0.022) |

### A1 adjusted. Three-point confidence means, scale points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Executive branch of the federal government | +0.296 (0.025) | +0.118 (0.032) | +0.079 (0.034) | -0.218 (0.040) | +0.307 (0.035) | +0.111 (0.038) | +0.127 (0.043) |
| Congress | +0.352 (0.024) | +0.135 (0.032) | +0.048 (0.029) | -0.304 (0.036) | +0.385 (0.033) | +0.148 (0.041) | +0.099 (0.040) |
| US Supreme Court | +0.204 (0.026) | +0.025 (0.035) | -0.008 (0.032) | -0.212 (0.038) | +0.220 (0.034) | +0.043 (0.041) | +0.021 (0.040) |
| The military | -0.125 (0.025) | -0.140 (0.037) | -0.136 (0.034) | -0.010 (0.040) | -0.178 (0.034) | -0.174 (0.044) | -0.114 (0.043) |
| The press | +0.220 (0.025) | +0.125 (0.034) | +0.061 (0.029) | -0.159 (0.036) | +0.220 (0.032) | +0.151 (0.043) | +0.103 (0.036) |
| The scientific community | +0.024 (0.025) | -0.037 (0.031) | +0.000 (0.028) | -0.024 (0.036) | +0.047 (0.033) | -0.055 (0.040) | +0.002 (0.036) |
| Education | +0.266 (0.025) | +0.100 (0.034) | +0.057 (0.030) | -0.208 (0.037) | +0.287 (0.034) | +0.137 (0.041) | +0.084 (0.038) |
| Major companies | +0.000 (0.022) | -0.027 (0.029) | -0.038 (0.029) | -0.038 (0.035) | +0.024 (0.032) | -0.007 (0.037) | -0.014 (0.034) |
| Banks and financial institutions | +0.052 (0.027) | -0.011 (0.033) | -0.057 (0.032) | -0.109 (0.040) | +0.019 (0.035) | -0.014 (0.039) | -0.023 (0.040) |
| Organised religion | +0.096 (0.028) | +0.046 (0.035) | -0.015 (0.032) | -0.112 (0.040) | +0.137 (0.036) | +0.085 (0.045) | +0.038 (0.039) |
| Medicine | +0.125 (0.027) | -0.038 (0.034) | -0.048 (0.032) | -0.173 (0.039) | +0.203 (0.034) | -0.023 (0.045) | -0.005 (0.041) |
| Organised labour | +0.074 (0.027) | +0.046 (0.031) | +0.037 (0.027) | -0.037 (0.036) | +0.062 (0.037) | +0.017 (0.038) | +0.063 (0.035) |
| Television | +0.063 (0.023) | +0.009 (0.034) | +0.030 (0.029) | -0.033 (0.035) | +0.037 (0.032) | +0.034 (0.043) | +0.050 (0.035) |

### A1 adjusted. Where the Hispanic generations sit against white subgroups

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| Index: executive + Congress + Supreme Court (1-3) | +30.0 (2.2) | +5.3 (2.7) | +3.3 (2.7) | +6.0 (2.6) | -2.0 (1.4) | +10.0 (1.1) |
| Index: all 13 institutions (1-3) | +14.6 (1.6) | +2.8 (1.9) | -1.0 (1.8) | +1.4 (1.8) | -3.8 (1.0) | +5.9 (0.8) |
| Executive branch of the federal government | +8.9 (1.5) | +5.7 (1.9) | +0.5 (2.0) | +6.0 (1.9) | -5.2 (0.9) | +6.0 (0.8) |
| Congress | +12.2 (1.5) | +2.3 (1.5) | +2.5 (1.5) | +2.5 (1.4) | +0.1 (0.7) | -0.7 (0.6) |
| US Supreme Court | +6.8 (1.9) | -2.4 (2.2) | +5.3 (2.2) | +2.5 (2.1) | +7.6 (1.3) | +8.6 (1.1) |
| The military | -17.4 (2.0) | -16.1 (2.4) | +3.2 (2.5) | -9.7 (2.4) | +19.2 (1.4) | -8.7 (1.2) |

## A2. Civil liberties: the Stouffer tolerance battery

This is where a real first-generation deficit exists, and it is large. On the classic fifteen-item scale (allow an atheist, a racist, a communist, a militarist and a homosexual to speak, to teach and to have a book in the library) the adjusted first-generation gap is −1.58 scale points (SE 0.20), second generation −1.27 (0.22), third-plus −0.42 (0.18). Convergence is precise: third-plus minus first is +1.16 points (0.25).

Against the honest comparators the third generation has arrived. Against white conservatives the third-plus gap is −0.03 scale points (0.19); against whites without a bachelor's degree −0.28 (0.20). Neither is distinguishable from zero. Against white liberals it is −1.02 (0.19), and the white conservative-to-liberal spread is itself 0.98 points while the white graduate-to-non-graduate spread is 1.63 points. On this battery the education cleavage inside the white population is 3.9 times the Hispanic third-generation gap against whites overall.

The item-level detail matters. Tolerance of a **homosexual** speaking, teaching or publishing is at or above the white level in every Hispanic generation, including the first. Tolerance of a **racist** shows the steepest generational gradient of any item (allow a racist to speak: 34.4, 46.1, 55.0 percent against 63.1 for whites; adjusted gaps −22.9, −12.3, −4.6). The **anti-American Muslim clergyman** items, fielded from 2008, show the largest first-generation deficit of all (allow him to speak: 16.1 percent against 48.9 for whites) and converge to white-conservative and white-non-graduate parity by the third generation (three-item scale, adjusted G3+ −0.04 against white conservatives, −0.07 against white non-graduates) while remaining −0.51 against white liberals.

### A2 raw. Tolerance scales

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Stouffer 15-item tolerance scale (0-15) | 8.23 (0.25) 391 | 9.35 (0.27) 263 | 10.17 (0.25) 305 | 8.26 (0.18) 702 | 9.59 (0.23) 390 | 10.18 (0.20) 468 | 10.70 (0.05) 8652 | 11.62 (0.07) 2305 | 10.35 (0.08) 3158 | 10.10 (0.06) 5723 | 12.09 (0.06) 2921 |
| 9-item core scale, atheist/racist/communist (0-9) | 4.35 (0.15) 465 | 5.09 (0.14) 337 | 5.45 (0.15) 364 | 4.41 (0.11) 856 | 5.12 (0.13) 498 | 5.45 (0.11) 584 | 5.95 (0.03) 9999 | 6.43 (0.04) 2670 | 5.82 (0.05) 3671 | 5.64 (0.04) 6578 | 6.67 (0.04) 3413 |
| 3-item scale, anti-American Muslim clergyman (0-3) | 0.51 (0.05) 415 | 1.04 (0.08) 298 | 1.04 (0.09) 284 | 0.55 (0.04) 735 | 1.05 (0.07) 433 | 1.16 (0.07) 481 | 1.40 (0.02) 7262 | 1.83 (0.04) 1949 | 1.28 (0.03) 2644 | 1.18 (0.02) 4671 | 1.90 (0.03) 2591 |

### A2 raw. Tolerant-answer share, percent

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Let an anti-religionist speak | 58.0 (2.7) 540 | 72.3 (3.0) 386 | 76.6 (3.1) 394 | 62.1 (1.9) 995 | 72.0 (2.5) 571 | 75.4 (2.4) 640 | 82.8 (0.4) 11052 | 90.5 (0.7) 2858 | 81.2 (0.7) 4015 | 78.6 (0.6) 7397 | 93.3 (0.5) 3647 |
| Let a racist speak | 32.7 (2.5) 546 | 45.6 (3.3) 382 | 55.3 (3.2) 393 | 34.4 (1.9) 997 | 46.1 (2.6) 569 | 55.0 (2.5) 637 | 63.1 (0.6) 10976 | 66.2 (1.1) 2850 | 65.4 (0.9) 3991 | 59.1 (0.7) 7331 | 72.6 (1.0) 3637 |
| Let a communist speak | 50.7 (2.9) 517 | 60.3 (3.3) 368 | 60.5 (3.4) 389 | 48.3 (2.1) 947 | 60.7 (2.7) 542 | 63.5 (2.6) 627 | 72.9 (0.6) 10914 | 83.9 (0.9) 2842 | 71.4 (0.9) 3981 | 66.2 (0.7) 7267 | 89.0 (0.7) 3639 |
| Let a militarist speak | 47.7 (2.6) 472 | 57.3 (3.5) 304 | 71.1 (3.3) 339 | 47.1 (2.1) 838 | 60.5 (2.8) 452 | 70.9 (2.5) 522 | 73.1 (0.6) 9759 | 82.0 (0.9) 2489 | 71.2 (0.9) 3544 | 67.6 (0.7) 6593 | 86.7 (0.7) 3158 |
| Let a homosexual speak | 80.7 (2.1) 471 | 84.6 (2.8) 307 | 87.5 (2.0) 336 | 81.2 (1.6) 848 | 86.2 (2.2) 457 | 88.1 (1.6) 520 | 87.8 (0.4) 9744 | 94.5 (0.6) 2494 | 84.3 (0.8) 3531 | 84.1 (0.5) 6585 | 96.9 (0.3) 3151 |
| Let an anti-American Muslim clergyman speak | 15.6 (2.1) 419 | 38.0 (3.7) 308 | 35.7 (3.6) 284 | 16.1 (1.5) 747 | 37.5 (3.1) 446 | 42.9 (2.7) 484 | 48.9 (0.8) 7378 | 63.1 (1.4) 1982 | 46.0 (1.3) 2680 | 40.9 (0.9) 4747 | 67.2 (1.2) 2631 |
| Let an anti-religionist teach | 48.3 (2.6) 617 | 60.8 (2.9) 461 | 68.9 (2.5) 474 | 50.9 (1.9) 1153 | 61.8 (2.4) 681 | 68.5 (1.9) 782 | 67.0 (0.5) 12904 | 82.0 (0.8) 3439 | 60.4 (0.9) 4719 | 61.3 (0.6) 8408 | 80.2 (0.8) 4486 |
| Let a racist teach | 34.4 (2.5) 625 | 33.9 (2.8) 458 | 44.9 (2.9) 476 | 33.9 (1.8) 1171 | 33.9 (2.3) 683 | 42.8 (2.2) 783 | 45.8 (0.5) 12880 | 46.1 (1.1) 3419 | 46.2 (0.9) 4704 | 43.9 (0.7) 8400 | 50.3 (1.0) 4471 |
| Let an anti-American Muslim clergyman teach | 15.7 (2.0) 502 | 24.0 (2.7) 377 | 26.2 (3.0) 369 | 16.1 (1.5) 920 | 24.4 (2.2) 553 | 28.0 (2.3) 631 | 34.3 (0.6) 9387 | 47.6 (1.2) 2581 | 29.8 (1.0) 3431 | 28.5 (0.7) 5877 | 47.1 (1.1) 3509 |
| Keep an anti-religious book | 63.0 (2.7) 536 | 75.6 (2.9) 383 | 75.6 (2.7) 393 | 63.1 (1.9) 979 | 75.5 (2.4) 562 | 76.7 (2.1) 635 | 79.4 (0.5) 10947 | 89.7 (0.7) 2845 | 74.5 (0.9) 3970 | 75.0 (0.7) 7311 | 89.9 (0.7) 3628 |
| Keep a racist book | 41.8 (2.8) 541 | 48.5 (3.3) 381 | 62.7 (3.1) 394 | 45.4 (2.1) 981 | 49.1 (2.7) 564 | 61.1 (2.5) 637 | 67.6 (0.6) 10907 | 72.2 (1.1) 2834 | 66.2 (1.0) 3970 | 64.3 (0.7) 7271 | 75.7 (1.0) 3628 |
| Keep an anti-American Muslim clergyman's book | 21.4 (2.7) 417 | 43.5 (3.6) 305 | 40.5 (3.6) 286 | 24.7 (2.1) 741 | 44.1 (2.9) 442 | 44.0 (2.8) 485 | 55.8 (0.7) 7387 | 70.4 (1.3) 1989 | 51.3 (1.2) 2682 | 48.7 (0.9) 4754 | 71.9 (1.3) 2633 |

### A2 adjusted. Tolerance scales, scale points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Stouffer 15-item tolerance scale (0-15) | -1.583 (0.196) | -1.269 (0.222) | -0.424 (0.183) | +1.159 (0.254) | -1.368 (0.268) | -1.422 (0.263) | -0.342 (0.227) |
| 9-item core scale, atheist/racist/communist (0-9) | -1.081 (0.119) | -0.754 (0.127) | -0.388 (0.112) | +0.693 (0.158) | -0.980 (0.165) | -0.745 (0.148) | -0.358 (0.147) |
| 3-item scale, anti-American Muslim clergyman (0-3) | -0.513 (0.054) | -0.278 (0.072) | -0.168 (0.069) | +0.345 (0.081) | -0.444 (0.071) | -0.271 (0.083) | -0.255 (0.091) |

### A2 adjusted. Tolerance against white subgroups, scale points

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| Stouffer 15-item tolerance scale (0-15) | -1.230 (0.206) | -0.034 (0.194) | -1.019 (0.187) | -0.281 (0.198) | -0.984 (0.099) | +1.634 (0.087) |
| 9-item core scale, atheist/racist/communist (0-9) | -0.961 (0.124) | -0.244 (0.118) | -0.723 (0.116) | -0.292 (0.117) | -0.479 (0.061) | +0.867 (0.054) |
| 3-item scale, anti-American Muslim clergyman (0-3) | -0.419 (0.059) | -0.042 (0.073) | -0.507 (0.076) | -0.071 (0.073) | -0.465 (0.043) | +0.660 (0.040) |

## A3. Rule of law, policing and civic values

**Obedience as a child value** starts far above the white level and converges in a single generation. Ranking obedience first or second among desirable child qualities: Mexican first generation 42.9 percent, second 20.2, third-plus 24.2, against 18.8 for whites overall and 23.4 for white conservatives. The adjusted first-generation gap is +16.1 points (1.9); by the third it is +3.2 (1.8), which is −1.6 (1.9) against white conservatives and +2.1 (1.9) against white non-graduates. Third-plus minus first is −12.9 points (2.4).

**Approval of police force** runs the other way. Hispanics of every generation are *less* willing to approve a policeman striking a citizen than whites are, and the gap narrows but does not close (adjusted: −40.0, −22.3, −11.4 points). At the third generation that is −16.9 against white conservatives and −7.2 against white liberals, so the Hispanic third generation is outside the white range on the permissive side of nothing: it is less permissive than white liberals. The same holds for the four-scenario force index.

**Punitiveness** converges upward. Death-penalty support goes 46.2, 60.9, 67.5 percent against 71.8 for whites, adjusted gaps −30.4, −9.7, −4.2; the third generation is +18.1 points more punitive than white liberals and −15.7 less than white conservatives. Support for gun permits, marijuana legalisation and the view that courts are too harsh all move from a distinctively immigrant position toward the white distribution.

### A3 raw. Rule of law, policing and civic values

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Obedience ranked 1st or 2nd child quality | 42.9 (2.6) 573 | 20.2 (2.4) 425 | 24.2 (2.7) 482 | 41.2 (1.8) 1124 | 21.5 (1.9) 649 | 22.0 (2.0) 804 | 18.8 (0.5) 12408 | 8.9 (0.6) 3259 | 23.4 (0.8) 4591 | 22.8 (0.6) 8183 | 9.3 (0.5) 4215 |
| Courts deal with criminals too harshly | 22.3 (1.8) 734 | 18.5 (2.3) 457 | 15.7 (2.1) 508 | 18.9 (1.3) 1346 | 21.8 (2.1) 679 | 16.2 (1.6) 805 | 10.3 (0.3) 13685 | 21.0 (0.9) 3248 | 5.6 (0.4) 5204 | 9.3 (0.4) 9627 | 12.8 (0.7) 4048 |
| Courts not harsh enough | 58.5 (2.1) 734 | 64.5 (2.9) 457 | 70.7 (2.4) 508 | 59.9 (1.6) 1346 | 62.3 (2.4) 679 | 66.1 (2.0) 805 | 69.4 (0.6) 13685 | 53.5 (1.1) 3248 | 75.6 (0.8) 5204 | 73.4 (0.6) 9627 | 59.0 (1.1) 4048 |
| Favours the death penalty | 44.1 (2.1) 851 | 61.1 (2.5) 629 | 68.6 (2.2) 678 | 46.2 (1.6) 1618 | 60.9 (2.1) 941 | 67.5 (1.8) 1114 | 71.8 (0.4) 18321 | 48.0 (0.9) 4855 | 83.0 (0.6) 6809 | 76.8 (0.5) 12085 | 59.9 (0.8) 6224 |
| Favours police permits to buy a gun | 83.0 (1.6) 644 | 70.7 (2.9) 491 | 70.9 (3.3) 504 | 84.4 (1.2) 1224 | 72.4 (2.3) 737 | 70.2 (2.4) 844 | 68.5 (0.5) 13851 | 83.9 (0.8) 3711 | 56.3 (0.9) 5059 | 66.3 (0.7) 8958 | 73.8 (0.8) 4883 |
| Marijuana should be legal | 22.4 (2.2) 504 | 51.1 (3.6) 300 | 53.2 (3.5) 348 | 22.0 (1.8) 945 | 52.6 (2.9) 460 | 56.8 (2.7) 563 | 51.1 (0.7) 9491 | 72.3 (1.1) 2359 | 38.1 (1.1) 3546 | 49.8 (0.8) 6597 | 54.4 (1.1) 2886 |
| Ever approves police striking a citizen | 24.5 (2.2) 489 | 49.5 (3.4) 323 | 65.7 (3.3) 373 | 28.8 (1.9) 936 | 53.7 (2.8) 501 | 63.9 (2.5) 618 | 77.9 (0.5) 10402 | 75.8 (1.0) 2702 | 83.6 (0.7) 3860 | 74.4 (0.6) 6989 | 86.6 (0.7) 3404 |
| …after vulgar language | 13.5 (1.7) 531 | 10.6 (2.0) 350 | 5.4 (1.3) 398 | 12.6 (1.3) 1009 | 9.7 (1.5) 540 | 6.9 (1.2) 655 | 8.6 (0.3) 11022 | 5.3 (0.5) 2852 | 11.0 (0.6) 4070 | 9.4 (0.4) 7441 | 6.6 (0.6) 3572 |
| …questioning a murder suspect | 31.2 (2.3) 594 | 22.8 (2.6) 433 | 19.0 (2.3) 490 | 28.8 (1.6) 1161 | 23.6 (2.1) 662 | 17.1 (1.6) 820 | 11.7 (0.4) 13026 | 8.3 (0.6) 3422 | 12.7 (0.6) 4828 | 13.9 (0.5) 8598 | 6.4 (0.4) 4417 |
| …a citizen escaping custody | 49.6 (2.4) 597 | 58.1 (3.0) 431 | 64.2 (2.6) 485 | 49.4 (1.8) 1162 | 59.0 (2.4) 652 | 64.2 (2.1) 808 | 76.0 (0.5) 12800 | 68.8 (1.0) 3352 | 81.1 (0.7) 4780 | 75.1 (0.6) 8479 | 78.0 (0.8) 4310 |
| …a citizen attacking the officer | 70.7 (2.4) 531 | 73.4 (3.3) 354 | 84.6 (2.3) 398 | 70.1 (1.8) 1010 | 72.6 (2.6) 543 | 84.5 (1.8) 655 | 92.3 (0.3) 11081 | 90.6 (0.7) 2846 | 93.9 (0.5) 4107 | 91.4 (0.4) 7484 | 94.4 (0.5) 3588 |
| Share of 4 police-force scenarios approved | 40.7 (1.5) 487 | 40.9 (1.6) 329 | 43.3 (1.2) 377 | 39.9 (1.1) 911 | 41.3 (1.3) 498 | 43.0 (1.0) 618 | 47.1 (0.2) 10394 | 43.6 (0.5) 2679 | 49.5 (0.4) 3875 | 47.3 (0.3) 7005 | 46.7 (0.4) 3380 |

### A3 adjusted. Rule of law and policing, percentage points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Obedience ranked 1st or 2nd child quality | +16.1 (1.9) | +4.1 (1.9) | +3.2 (1.8) | -12.9 (2.4) | +16.1 (2.7) | +2.6 (2.4) | +4.4 (2.4) |
| Courts deal with criminals too harshly | +7.5 (1.3) | +8.0 (2.2) | +3.6 (1.6) | -3.9 (2.0) | +11.0 (1.9) | +4.7 (2.4) | +3.2 (2.0) |
| Courts not harsh enough | -13.0 (1.8) | -4.2 (2.5) | -2.4 (2.1) | +10.5 (2.5) | -16.2 (2.4) | -2.7 (3.0) | +1.0 (2.4) |
| Favours the death penalty | -30.4 (1.7) | -9.7 (2.1) | -4.2 (1.9) | +26.2 (2.5) | -35.5 (2.3) | -9.7 (2.6) | -4.1 (2.2) |
| Favours police permits to buy a gun | +20.2 (1.5) | +7.0 (2.3) | +4.5 (2.2) | -15.6 (2.5) | +20.2 (1.9) | +5.7 (2.9) | +5.2 (3.0) |
| Marijuana should be legal | -31.0 (2.0) | -7.2 (2.8) | +0.1 (2.5) | +31.2 (3.0) | -32.3 (2.5) | -9.1 (3.4) | -1.7 (3.2) |
| Ever approves police striking a citizen | -40.0 (2.0) | -22.3 (2.7) | -11.4 (2.5) | +28.6 (3.1) | -42.8 (2.4) | -25.7 (3.4) | -8.7 (3.3) |
| …a citizen escaping custody | -23.3 (2.0) | -13.7 (2.5) | -8.7 (2.2) | +14.6 (2.8) | -22.3 (2.7) | -13.2 (3.1) | -8.5 (2.7) |
| …a citizen attacking the officer | -20.1 (1.9) | -18.4 (2.5) | -6.7 (1.8) | +13.4 (2.6) | -19.4 (2.4) | -17.2 (3.2) | -6.5 (2.3) |
| Share of 4 police-force scenarios approved | -7.1 (1.2) | -5.2 (1.3) | -3.4 (1.0) | +3.7 (1.5) | -6.1 (1.5) | -5.2 (1.6) | -3.0 (1.3) |

### A3 adjusted. Against white subgroups, percentage points

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| Obedience ranked 1st or 2nd child quality | +11.7 (2.0) | -1.6 (1.9) | +9.8 (1.8) | +2.1 (1.9) | +11.5 (1.0) | -10.8 (0.9) |
| Favours the death penalty | -40.4 (1.7) | -15.7 (1.9) | +18.1 (2.0) | -7.7 (1.9) | +33.7 (1.1) | -18.9 (1.0) |
| Favours police permits to buy a gun | +32.5 (1.7) | +17.8 (2.4) | -10.3 (2.4) | +5.8 (2.3) | -28.0 (1.3) | +8.8 (1.1) |
| Ever approves police striking a citizen | -45.4 (2.1) | -16.9 (2.6) | -7.2 (2.7) | -10.9 (2.6) | +9.7 (1.2) | +8.5 (1.0) |
| Share of 4 police-force scenarios approved | -9.4 (1.2) | -5.8 (1.1) | -0.3 (1.1) | -3.5 (1.0) | +5.5 (0.6) | -0.9 (0.5) |
| Courts deal with criminals too harshly | +11.2 (1.4) | +7.8 (1.6) | -6.1 (1.8) | +4.5 (1.6) | -13.9 (1.0) | +5.1 (0.8) |

## A4. Role of government

This is the one domain where the earlier finding of non-convergence survives intact, reproducing confidence-ladder entry 87. On "government should reduce income differences" the adjusted gaps are +0.603, +0.582, +0.459 scale points on a seven-point scale; third-plus minus first is −0.144 (0.112), which is not distinguishable from zero. The same pattern holds for "government should improve living standards" and "government should do more".

The comparator changes how large this looks. The white conservative-to-liberal spread on the same seven-point item is 2.18 scale points. The Hispanic third-generation deviation from the white mean, 0.46 points, is 21 percent of that, and it places the third generation between white moderates and white liberals (−0.68 against white liberals, +1.50 against white conservatives). This is a real and persistent difference in the preferred size of government. It is not a difference in kind from differences that already exist inside the native white population.

### A4 raw and adjusted. Role of government

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Government should reduce income differences (1-7) | 4.99 (0.11) 610 | 5.03 (0.11) 441 | 4.64 (0.10) 494 | 4.96 (0.08) 1191 | 4.98 (0.09) 670 | 4.78 (0.08) 828 | 4.09 (0.02) 13166 | 5.26 (0.04) 3464 | 3.06 (0.03) 4882 | 4.16 (0.03) 8704 | 3.94 (0.04) 4451 |
| Government should improve living standards (1-5) | 3.55 (0.07) 601 | 3.45 (0.07) 438 | 3.35 (0.07) 490 | 3.53 (0.05) 1178 | 3.42 (0.06) 664 | 3.39 (0.05) 823 | 2.98 (0.01) 12997 | 3.60 (0.02) 3441 | 2.49 (0.02) 4824 | 2.98 (0.02) 8568 | 2.96 (0.02) 4418 |
| Government should do more (1-5) | 3.47 (0.07) 586 | 3.39 (0.07) 427 | 3.20 (0.07) 480 | 3.56 (0.05) 1142 | 3.38 (0.06) 652 | 3.29 (0.06) 806 | 2.78 (0.01) 12877 | 3.42 (0.02) 3394 | 2.26 (0.02) 4795 | 2.79 (0.02) 8473 | 2.75 (0.02) 4394 |

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Government should reduce income differences (1-7) | +0.603 (0.084) | +0.582 (0.090) | +0.459 (0.088) | -0.144 (0.112) | +0.590 (0.110) | +0.579 (0.110) | +0.317 (0.100) |
| Government should improve living standards (1-5) | +0.432 (0.054) | +0.274 (0.059) | +0.284 (0.052) | -0.148 (0.071) | +0.431 (0.073) | +0.266 (0.072) | +0.238 (0.065) |
| Government should do more (1-5) | +0.676 (0.048) | +0.424 (0.059) | +0.394 (0.057) | -0.282 (0.070) | +0.565 (0.068) | +0.409 (0.071) | +0.307 (0.070) |
| Welfare spending too little | +0.040 (0.021) | +0.079 (0.024) | +0.076 (0.024) | +0.036 (0.031) | +0.013 (0.029) | +0.069 (0.029) | +0.043 (0.028) |

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| Government should reduce income differences (1-7) | +1.585 (0.088) | +1.497 (0.090) | -0.682 (0.092) | +0.466 (0.089) | -2.179 (0.049) | -0.040 (0.051) |
| Government should improve living standards (1-5) | +0.877 (0.057) | +0.762 (0.056) | -0.317 (0.055) | +0.307 (0.053) | -1.079 (0.030) | +0.080 (0.027) |
| Government should do more (1-5) | +1.160 (0.051) | +0.912 (0.060) | -0.233 (0.060) | +0.413 (0.058) | -1.144 (0.032) | +0.052 (0.031) |

## A5. National identity and pluralism

The ISSP national-identity modules (2004, 2014 and a partial 2024 fielding) are thin, with Mexican-origin cells of 25-109 and all-Hispanic cells of 46-212. Read directionally.

Hispanic respondents are not less committed to a demanding conception of American identity than whites are; on several items they are more so. Saying it is very important to **respect America's laws and institutions** runs 79.5 percent in the first generation against 64.5 for whites overall and 68.5 for white conservatives (adjusted first-generation gap +19.1 points, SE 3.9). Saying it is very important to **speak English** runs 86.4 against 77.2. Saying it is very important to have **been born in America** is *higher* among second-generation Hispanics (56.9) than among whites (40.5). The one identity item where Hispanics sit clearly below whites is having **American citizenship** (adjusted −3.8 at the third generation, and −18.5 against white conservatives).

On pluralism, agreement that it is impossible for people who do not share American customs to become fully American is statistically identical between Hispanic generations and whites (adjusted third-plus −0.03 scale points, SE 0.12). Agreement that ethnic minorities never fit into the American mainstream is *lower* in the Hispanic third generation than among whites (−0.33, SE 0.13). Preference for "would rather be a citizen of America than of any other country" rises across generations to parity (adjusted third-plus +0.03, SE 0.11). On the three-way assimilation item, almost no Hispanic first- or second-generation respondent picks "immigrants should give up their culture of origin" — but neither do most whites; 5.6 percent of whites and 8.9 percent of white conservatives pick it. The overwhelming modal answer in every group is the bicultural option.

### A5 raw. National identity, share saying 'very important' to being truly American, percent

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Having American citizenship | 67.3 (5.3) 109 | 67.7 (5.9) 92 | 61.9 (5.6) 108 | 65.9 (4.0) 212 | 69.7 (4.8) 141 | 66.7 (4.2) 174 | 73.7 (1.2) 2393 | 43.5 (3.1) 412 | 82.4 (2.1) 604 | 78.1 (1.3) 1535 | 64.4 (2.2) 858 |
| Having been born in America | 48.5 (6.2) 104 | 55.7 (6.8) 85 | 48.4 (5.6) 105 | 38.8 (4.9) 198 | 56.9 (5.1) 133 | 46.0 (4.5) 172 | 40.5 (1.4) 2384 | 16.5 (2.6) 415 | 37.5 (2.8) 601 | 49.6 (1.7) 1526 | 21.4 (1.8) 858 |
| Being able to speak English | 84.8 (4.9) 73 | 78.9 (5.3) 56 | 73.2 (6.3) 70 | 86.4 (3.4) 130 | 80.2 (5.0) 86 | 71.0 (5.3) 106 | 77.2 (1.2) 1519 | 53.9 (4.8) 175 | 81.6 (2.5) 261 | 81.5 (1.4) 1022 | 66.6 (2.8) 497 |
| Respecting America's laws and institutions | 76.7 (4.6) 108 | 65.4 (5.8) 89 | 58.8 (5.6) 105 | 79.5 (3.4) 210 | 63.6 (4.9) 137 | 63.7 (4.6) 171 | 64.5 (1.2) 2369 | 51.7 (3.3) 403 | 68.5 (2.6) 597 | 63.9 (1.4) 1517 | 65.9 (2.1) 852 |
| Having American ancestry | 22.5 (5.2) 99 | 29.1 (5.4) 91 | 18.2 (3.8) 104 | 23.1 (4.1) 198 | 26.0 (4.3) 139 | 20.9 (3.4) 171 | 22.5 (1.1) 2372 | 6.5 (1.5) 412 | 19.8 (1.9) 599 | 28.2 (1.4) 1516 | 10.4 (1.3) 856 |
| Being a Christian | 42.0 (5.6) 101 | 40.6 (6.5) 88 | 26.7 (4.9) 105 | 38.2 (4.8) 199 | 34.8 (4.9) 134 | 25.3 (3.9) 170 | 31.9 (1.2) 2325 | 7.5 (2.1) 405 | 36.9 (2.6) 586 | 36.9 (1.5) 1486 | 21.5 (1.9) 839 |
| Feeling American | 53.7 (6.4) 106 | 47.8 (5.8) 91 | 51.9 (5.8) 107 | 55.6 (5.0) 207 | 51.9 (4.9) 139 | 51.8 (4.6) 174 | 59.9 (1.1) 2327 | 34.9 (3.4) 394 | 63.4 (2.7) 580 | 64.1 (1.3) 1498 | 51.1 (2.1) 829 |
| Having lived in America most of one's life | 55.3 (7.2) 69 | 58.9 (9.0) 55 | 51.1 (6.4) 67 | 49.8 (5.1) 123 | 63.9 (6.9) 85 | 48.0 (5.5) 103 | 48.5 (1.5) 1514 | 24.7 (4.2) 175 | 39.8 (3.8) 261 | 55.9 (1.8) 1019 | 30.4 (2.4) 495 |

### A5 raw. Pluralism items, agreement means

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Would rather be a citizen of America than anywhere else (1-5) | 3.94 (0.12) 102 | 4.08 (0.13) 90 | 4.37 (0.13) 108 | 4.06 (0.09) 201 | 4.18 (0.10) 137 | 4.40 (0.10) 174 | 4.48 (0.03) 2387 | 3.93 (0.08) 414 | 4.71 (0.04) 604 | 4.55 (0.03) 1526 | 4.34 (0.05) 861 |
| Impossible for those not sharing customs to become fully American (1-5) | 2.97 (0.13) 64 | 2.79 (0.14) 50 | 2.76 (0.15) 68 | 2.83 (0.10) 112 | 2.73 (0.11) 79 | 2.74 (0.12) 104 | 2.73 (0.03) 1500 | 2.43 (0.08) 176 | 2.71 (0.08) 259 | 2.86 (0.04) 1004 | 2.41 (0.06) 496 |
| There are things about America that make me ashamed (1-5) | 2.87 (0.13) 99 | 3.62 (0.16) 88 | 3.63 (0.14) 107 | 2.93 (0.09) 194 | 3.61 (0.12) 137 | 3.67 (0.11) 172 | 3.72 (0.03) 2378 | 4.15 (0.05) 410 | 3.64 (0.06) 598 | 3.65 (0.03) 1519 | 3.88 (0.05) 859 |
| America should follow its own interests (1-5) | 3.06 (0.15) 96 | 3.16 (0.15) 81 | 3.16 (0.10) 108 | 3.01 (0.10) 188 | 3.17 (0.12) 123 | 3.12 (0.10) 176 | 3.27 (0.03) 2326 | 2.74 (0.07) 395 | 3.58 (0.05) 586 | 3.39 (0.03) 1483 | 3.00 (0.05) 843 |
| Ethnic minorities never fit into the American mainstream (1-5) | 2.97 (0.24) 28 | 2.17 (0.20) 31 | 1.91 (0.13) 46 | 2.76 (0.15) 69 | 2.23 (0.18) 59 | 1.88 (0.13) 68 | 2.25 (0.03) 1779 | 1.99 (0.08) 217 | 2.40 (0.07) 329 | 2.33 (0.03) 1314 | 2.01 (0.05) 465 |
| Minorities must adapt to American culture (1-5) | 3.22 (0.27) 25 | 3.60 (0.19) 31 | 3.33 (0.15) 46 | 3.51 (0.13) 67 | 3.64 (0.13) 59 | 3.51 (0.13) 68 | 3.59 (0.03) 1782 | 3.42 (0.08) 218 | 3.68 (0.07) 329 | 3.65 (0.03) 1317 | 3.40 (0.05) 465 |
| America should limit immigration to protect its way of life (1-5) | 2.70 (0.20) 28 | 2.83 (0.21) 40 | 3.05 (0.24) 33 | 2.72 (0.14) 57 | 2.83 (0.15) 63 | 3.11 (0.18) 66 | 3.06 (0.05) 1142 | 2.05 (0.06) 398 | 3.74 (0.06) 406 | 3.28 (0.06) 580 | 2.61 (0.06) 561 |
| Immigrants undermine American culture (1-4) | 1.34 (0.09) 45 | 1.85 (0.07) 30 | 1.55 (0.14) 36 | 1.45 (0.10) 80 | 1.76 (0.10) 46 | 1.69 (0.13) 54 | 1.72 (0.04) 636 | 1.50 (0.10) 135 | 1.73 (0.07) 240 | 1.82 (0.04) 438 | 1.46 (0.06) 198 |

### A5 adjusted. National identity and pluralism

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Having American citizenship | -7.4 (4.2) | +1.7 (5.0) | -3.8 (4.2) | +3.7 (5.6) | -9.0 (5.7) | -0.9 (6.1) | -8.9 (4.7) |
| Having been born in America | -7.8 (4.7) | +17.5 (5.5) | +4.4 (4.6) | +12.3 (5.7) | -4.2 (6.7) | +15.1 (6.7) | +5.7 (5.4) |
| Being able to speak English | +7.5 (3.6) | +8.3 (5.2) | -3.8 (5.3) | -11.4 (5.9) | +3.8 (5.1) | +6.0 (5.3) | -3.2 (6.4) |
| Respecting America's laws and institutions | +19.1 (3.9) | +7.9 (5.0) | +5.0 (4.5) | -14.1 (5.9) | +16.7 (5.0) | +10.6 (5.8) | +1.0 (5.2) |
| Having American ancestry | -3.6 (3.9) | +7.3 (4.4) | +0.0 (3.4) | +3.6 (5.0) | -8.1 (5.6) | +9.5 (5.3) | -2.6 (4.3) |
| Being a Christian | +5.8 (4.7) | +12.7 (4.8) | -1.6 (4.1) | -7.4 (6.0) | +7.1 (5.7) | +19.0 (6.3) | +0.6 (5.5) |
| Feeling American | -2.3 (5.3) | +2.8 (5.1) | -1.5 (4.5) | +0.9 (7.0) | -7.3 (6.5) | -1.0 (5.7) | -1.1 (4.8) |
| Having lived in America most of one's life | -3.7 (5.9) | +20.4 (7.6) | +1.0 (5.5) | +4.7 (7.4) | -0.7 (8.4) | +13.2 (9.3) | +1.2 (6.8) |

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Would rather be a citizen of America than anywhere else (1-5) | -0.384 (0.098) | -0.114 (0.098) | +0.033 (0.105) | +0.417 (0.139) | -0.562 (0.127) | -0.196 (0.116) | +0.009 (0.135) |
| Impossible for those not sharing customs to become fully American (1-5) | -0.055 (0.109) | -0.008 (0.123) | -0.032 (0.116) | +0.023 (0.141) | +0.008 (0.136) | -0.001 (0.146) | -0.082 (0.152) |
| There are things about America that make me ashamed (1-5) | -0.769 (0.095) | -0.199 (0.119) | -0.106 (0.116) | +0.663 (0.142) | -0.768 (0.136) | -0.192 (0.156) | -0.119 (0.142) |
| America should follow its own interests (1-5) | -0.317 (0.106) | -0.034 (0.123) | -0.125 (0.096) | +0.193 (0.130) | -0.356 (0.153) | -0.070 (0.151) | -0.092 (0.103) |
| Ethnic minorities never fit into the American mainstream (1-5) | +0.492 (0.156) | +0.015 (0.172) | -0.325 (0.133) | -0.817 (0.201) | +0.630 (0.248) | -0.038 (0.203) | -0.308 (0.129) |
| Minorities must adapt to American culture (1-5) | -0.038 (0.128) | +0.097 (0.128) | +0.049 (0.144) | +0.088 (0.195) | -0.344 (0.262) | +0.032 (0.177) | -0.139 (0.151) |
| America should limit immigration to protect its way of life (1-5) | -0.496 (0.169) | -0.018 (0.163) | +0.143 (0.179) | +0.640 (0.231) | -0.845 (0.229) | -0.005 (0.213) | +0.172 (0.218) |
| Immigrants undermine American culture (1-4) | -0.476 (0.103) | -0.077 (0.106) | -0.102 (0.136) | +0.374 (0.163) | -0.628 (0.116) | +0.009 (0.080) | -0.292 (0.134) |

## A6. Instrument checks: how much of this is response style?

Two checks were built from the same data, neither of which is an attitude.

**Scenario differentiation.** The four police-force items run from a very weak justification (the citizen said vulgar things) to a very strong one (the citizen was attacking the officer). Whites separate these by 83.7 points. Hispanic first-generation respondents separate them by 57.3. By the third generation the separation is 77.6. The adjusted first-generation deficit in differentiation is −0.231 (0.023) and the third-generation deficit −0.048 (0.023), converging by +0.183 (0.032).

**Battery differentiation.** The within-respondent standard deviation across the thirteen confidence items is 0.534 in the Hispanic first generation against 0.596 among whites, converging to 0.578 by the third generation; adjusted, −0.050 (0.009) falling to −0.012 (0.008).

Both checks say the same thing. First-generation respondents give less differentiated answers across a battery than whites do, and that differentiation gap closes across generations on the same schedule as the substantive gaps. Some unknown share of the measured first-generation deficit in tolerance, and of the measured first-generation surplus in institutional confidence, is therefore an artefact of how the instrument is being answered rather than of what is believed. This cuts in both directions: it inflates the apparent first-generation deficit on the tolerance battery *and* inflates the apparent first-generation surplus on the confidence battery, and it makes the measured convergence partly a convergence in survey competence. No correction is attempted; the checks are reported so the convergence estimates are not read as purely substantive.

### A6. Instrument checks, raw then adjusted

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| INSTRUMENT: attacker minus vulgar-language approval | 0.569 (0.030) 520 | 0.627 (0.039) 346 | 0.791 (0.028) 394 | 0.573 (0.021) 987 | 0.629 (0.031) 528 | 0.776 (0.022) 648 | 0.837 (0.005) 10926 | 0.853 (0.008) 2825 | 0.829 (0.008) 4043 | 0.821 (0.006) 7372 | 0.877 (0.007) 3545 |
| INSTRUMENT: within-person SD over 13 confidence items | 0.544 (0.010) 493 | 0.541 (0.013) 373 | 0.579 (0.011) 419 | 0.534 (0.008) 947 | 0.552 (0.010) 573 | 0.578 (0.008) 708 | 0.596 (0.002) 11310 | 0.606 (0.003) 3043 | 0.613 (0.003) 4248 | 0.590 (0.002) 7344 | 0.610 (0.003) 3955 |

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| INSTRUMENT: attacker minus vulgar-language approval | -0.231 (0.023) | -0.191 (0.031) | -0.048 (0.023) | +0.183 (0.032) | -0.231 (0.031) | -0.191 (0.038) | -0.034 (0.028) |
| INSTRUMENT: within-person SD over 13 confidence items | -0.050 (0.009) | -0.039 (0.010) | -0.012 (0.008) | +0.038 (0.011) | -0.037 (0.011) | -0.049 (0.013) | -0.011 (0.011) |

---

## B. ANES 2020 and 2024: explicit democratic-norms items

Generation coding is possible in **both** years: ANES 2020 and 2024 each carry respondent birthplace, parental nativity and number of foreign-born grandparents [SOURCE: `V201554`/`V201553`/`V201555` and `V241507`/`V241506`/`V241509`, codebooks]. The grandparent item additionally separates a true third generation (at least one foreign-born grandparent, n = 247) from fourth-plus (n = 255) among Hispanic respondents; both appear in `derived/anes_raw_means.csv`.

Pooled Hispanic cells run 350-510 per generation and Mexican-origin cells 158-227, so ANES contrasts are roughly three times noisier than the GSS ones. Items carried only in one year (the CSES6 democracy and courts items in 2024; the CSES5 populism and minorities-adapt items in 2020) have cells of 60-180 and are labelled in the tables.

On the brief's headline item, **"would it be helpful if presidents could work on the country's problems without paying attention to what Congress and the courts say"**, Hispanics are more permissive than whites overall (adjusted third-plus +4.0 points, SE 2.8) and indistinguishable from white conservatives (+2.0, SE 3.0) and from whites without a degree (+1.1, SE 2.9). The white ideological spread on this item is 7.5 points and the white education spread 10.2 points, both larger than the Hispanic gap.

On **"a strong leader is good for the United States even if the leader bends the rules"** the Hispanic third generation is +3.6 points against whites overall, −8.3 against white conservatives and +20.7 against white liberals, inside a white conservative-to-liberal spread of 29.0 points.

On the 2024 CSES6 items, agreement that **democracy is preferable to any other kind of government** is lower among Hispanics than among whites overall (−3.0, SE 4.9) but identical to whites without a degree (−0.4, SE 5.2), and agreement that **the courts should be able to stop the government acting beyond its authority** is *higher* among Hispanic third-generation respondents than among whites (+8.1, SE 3.4). Trust in the federal government is higher among Hispanics at every generation (+6.5 at the third, SE 2.3), reproducing the Abrajano-Alvarez finding on political as opposed to generalised trust.

**The exception is political violence.** The share saying political violence is at least a little justified runs 30.3, 29.0, 26.4 percent across Hispanic generations against 12.0 for whites; adjusted gaps +16.1, +10.4, +10.1 points. At the third generation that is +14.1 against white conservatives, +5.8 against white liberals and +9.6 against whites without a degree, and the white conservative-to-liberal spread is only 8.3 points. This is the single measured norm on which the Hispanic position sits outside the internal white range and does not visibly converge.

On the **authoritarian child-rearing battery** the Hispanic third generation scores +0.16 scale points above whites overall (SE 0.08), −0.24 against white conservatives and −0.07 against white non-graduates, against a white conservative-to-liberal spread of 1.25 points.

**ANES cannot detect convergence.** No ANES generational contrast is distinguishable from zero: political violence third-plus minus first is −6.0 points with a standard error of 4.1, the authoritarian scale −0.19 (0.13), the strong-leader item +0.07 (0.05). These are underpowered nulls, not evidence of flatness, and they should not be read against the precise GSS convergence estimates as though the two disagreed. The GSS has thirteen rounds and cells four to twenty times larger.

### B raw. ANES 2020 + 2024 pooled, percent

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| President acting without Congress and the courts would be helpful | 20.3 (4.1) 158 | 23.7 (3.8) 225 | 22.4 (4.6) 192 | 18.8 (2.5) 353 | 22.0 (2.9) 418 | 20.7 (2.7) 508 | 14.5 (0.5) 8745 | 7.6 (0.7) 2645 | 16.3 (0.9) 3440 | 18.9 (0.8) 4561 | 7.5 (0.5) 4097 |
| A strong leader is good even if the leader bends the rules | 31.3 (6.2) 137 | 32.0 (4.6) 195 | 36.6 (4.6) 174 | 32.5 (4.0) 298 | 26.7 (3.1) 366 | 37.8 (3.3) 442 | 33.7 (0.8) 7928 | 14.6 (1.0) 2448 | 45.6 (1.3) 3112 | 39.6 (1.1) 4062 | 24.1 (0.9) 3789 |
| Democracy is preferable to any other kind of government (2024) | 66.5 (8.5) 59 | 56.1 (6.8) 95 | 66.8 (7.8) 71 | 70.2 (5.5) 128 | 62.6 (5.6) 166 | 67.6 (4.6) 179 | 74.8 (1.3) 3089 | 83.6 (1.6) 942 | 79.9 (1.6) 1242 | 70.2 (1.9) 1550 | 82.9 (1.3) 1522 |
| Courts should stop the government exceeding its authority (2024) | 71.4 (8.1) 59 | 65.8 (6.3) 96 | 90.3 (4.0) 72 | 73.7 (5.2) 128 | 72.6 (4.4) 168 | 85.7 (3.0) 181 | 79.3 (1.1) 3093 | 88.9 (1.4) 942 | 80.7 (1.6) 1244 | 74.0 (1.5) 1552 | 88.7 (0.9) 1523 |
| The people, not politicians, should make policy (2020) | 33.9 (6.5) 76 | 41.0 (7.4) 99 | 53.8 (6.6) 102 | 38.0 (4.2) 167 | 43.8 (5.7) 198 | 51.5 (3.9) 261 | 52.8 (1.1) 4832 | 54.1 (1.7) 1503 | 53.4 (1.7) 1870 | 54.6 (1.5) 2507 | 50.2 (1.4) 2266 |
| Votes are counted fairly all or most of the time | 63.2 (5.5) 138 | 56.5 (5.1) 198 | 65.1 (4.1) 174 | 68.2 (3.8) 300 | 64.7 (3.5) 371 | 64.0 (3.3) 445 | 69.9 (0.7) 7965 | 91.4 (0.9) 2459 | 58.2 (1.1) 3125 | 62.3 (1.0) 4076 | 83.0 (0.8) 3809 |
| Political violence at least a little justified | 35.2 (5.2) 156 | 29.0 (4.2) 224 | 30.6 (4.7) 193 | 30.3 (3.3) 351 | 29.0 (3.1) 420 | 26.4 (2.6) 507 | 12.0 (0.5) 8767 | 15.8 (1.1) 2644 | 7.2 (0.7) 3449 | 13.7 (0.6) 4579 | 9.5 (0.6) 4100 |
| Satisfied with the way democracy works in the US | 55.5 (6.2) 137 | 62.8 (5.2) 194 | 51.6 (4.6) 173 | 59.6 (4.5) 297 | 63.5 (4.0) 364 | 57.6 (3.1) 441 | 64.5 (0.8) 7902 | 55.1 (1.5) 2438 | 72.1 (1.0) 3102 | 62.9 (1.2) 4040 | 67.0 (1.0) 3788 |
| Trusts the federal government always or most of the time | 23.1 (4.5) 157 | 17.2 (3.9) 227 | 10.9 (3.2) 193 | 21.8 (2.8) 354 | 18.2 (2.7) 425 | 18.0 (2.3) 509 | 12.9 (0.4) 8792 | 15.6 (0.9) 2651 | 12.4 (0.8) 3459 | 13.2 (0.7) 4596 | 12.5 (0.6) 4107 |
| Trusts election officials a great deal or a lot | 24.7 (4.1) 158 | 37.0 (4.4) 226 | 31.0 (4.3) 190 | 23.4 (2.8) 356 | 31.8 (2.8) 423 | 31.5 (2.8) 507 | 21.2 (0.6) 8792 | 10.9 (1.1) 2658 | 27.1 (1.0) 3455 | 25.2 (0.9) 4587 | 14.9 (0.8) 4116 |
| Minorities should adapt to US customs (2020) | 27.5 (5.4) 78 | 29.4 (5.9) 100 | 27.0 (5.1) 102 | 41.5 (4.9) 169 | 36.8 (3.5) 199 | 36.8 (4.5) 261 | 54.2 (1.1) 4838 | 27.7 (1.5) 1504 | 72.7 (1.2) 1871 | 59.4 (1.4) 2509 | 45.6 (1.4) 2270 |
| Being born in the US matters for being American | 49.1 (5.9) 137 | 60.9 (5.0) 194 | 48.7 (5.1) 172 | 43.3 (4.1) 299 | 56.0 (3.6) 365 | 50.9 (3.3) 440 | 49.2 (0.8) 7911 | 22.3 (1.3) 2441 | 59.0 (1.1) 3106 | 57.5 (1.0) 4049 | 35.1 (1.1) 3786 |
| Obedience over self-reliance | 48.9 (6.3) 139 | 35.2 (4.5) 197 | 38.8 (4.9) 173 | 53.6 (4.3) 301 | 39.8 (3.6) 368 | 43.8 (3.6) 444 | 39.0 (0.8) 7931 | 15.4 (1.1) 2446 | 51.1 (1.2) 3105 | 47.6 (1.1) 4067 | 24.8 (0.9) 3785 |
| Respect for elders over independence | 64.1 (5.2) 139 | 68.4 (4.6) 198 | 58.6 (4.7) 174 | 71.1 (3.2) 302 | 67.8 (3.2) 370 | 65.2 (3.1) 444 | 68.0 (0.8) 7933 | 40.0 (1.3) 2440 | 81.5 (1.0) 3114 | 76.1 (1.1) 4072 | 54.5 (1.1) 3781 |
| Good manners over curiosity | 69.4 (5.6) 139 | 75.5 (3.8) 198 | 56.5 (5.6) 173 | 68.8 (3.7) 302 | 70.1 (3.0) 370 | 63.4 (3.5) 445 | 55.5 (0.8) 7936 | 24.4 (1.2) 2445 | 67.6 (1.0) 3111 | 66.5 (1.1) 4074 | 37.0 (1.0) 3784 |
| Well behaved over being considerate | 38.8 (5.5) 139 | 41.8 (4.8) 198 | 30.4 (4.1) 173 | 40.7 (3.8) 302 | 38.2 (3.2) 370 | 31.4 (2.9) 444 | 23.7 (0.7) 7942 | 9.7 (0.9) 2448 | 28.7 (1.2) 3113 | 28.6 (1.0) 4074 | 15.3 (0.7) 3788 |

| Item | Mex G1 | Mex G2 | Mex G3+ | Hisp G1 | Hisp G2 | Hisp G3+ | White G3+ | W lib | W cons | W no BA | W BA+ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Authoritarian child-rearing scale (0-4) | 2.21 (0.17) 139 | 2.20 (0.11) 197 | 1.84 (0.13) 173 | 2.34 (0.11) 301 | 2.15 (0.08) 368 | 2.04 (0.09) 443 | 1.86 (0.02) 7897 | 0.90 (0.03) 2436 | 2.29 (0.03) 3094 | 2.19 (0.03) 4056 | 1.32 (0.02) 3764 |

### B adjusted. Gap versus non-Hispanic white third-plus generation, percentage points

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| President acting without Congress and the courts would be helpful | +2.0 (2.5) | +4.3 (2.9) | +4.0 (2.8) | +2.0 (3.9) | +1.9 (4.1) | +5.2 (3.8) | +5.7 (4.6) |
| A strong leader is good even if the leader bends the rules | -3.4 (4.2) | -7.6 (3.4) | +3.6 (3.2) | +7.0 (5.1) | -6.4 (6.5) | -2.4 (4.8) | +2.7 (4.7) |
| Democracy is preferable to any other kind of government (2024) | -1.7 (5.2) | -4.9 (5.3) | -3.0 (4.9) | -1.3 (7.0) | -3.4 (8.3) | -10.9 (6.9) | -3.7 (7.8) |
| Courts should stop the government exceeding its authority (2024) | -4.0 (5.1) | -3.2 (4.6) | +8.1 (3.4) | +12.1 (5.7) | -4.4 (8.0) | -9.3 (6.7) | +12.5 (4.3) |
| The people, not politicians, should make policy (2020) | -14.8 (4.6) | -9.5 (5.6) | -1.7 (3.9) | +13.1 (5.1) | -19.3 (6.8) | -12.9 (7.3) | +0.0 (6.7) |
| Votes are counted fairly all or most of the time | +2.4 (3.8) | +1.2 (3.4) | -0.8 (3.0) | -3.2 (4.8) | +0.9 (5.7) | -6.2 (5.1) | +1.3 (4.1) |
| Political violence at least a little justified | +16.1 (3.1) | +10.4 (3.1) | +10.1 (2.6) | -6.0 (4.1) | +20.3 (4.7) | +9.5 (4.2) | +13.7 (4.6) |
| Satisfied with the way democracy works in the US | -3.8 (4.4) | +4.2 (4.2) | -2.7 (3.3) | +1.1 (5.6) | -7.0 (5.8) | +3.9 (5.2) | -7.6 (4.5) |
| Trusts the federal government always or most of the time | +9.1 (2.7) | +7.9 (2.7) | +6.5 (2.3) | -2.6 (3.7) | +10.2 (4.4) | +7.0 (3.8) | -0.4 (3.3) |
| Trusts election officials a great deal or a lot | -0.4 (2.8) | +4.7 (3.0) | +6.3 (2.9) | +6.6 (4.1) | -0.7 (4.2) | +9.0 (4.4) | +5.4 (4.3) |
| Minorities should adapt to US customs (2020) | -14.1 (6.0) | -10.6 (3.5) | -12.2 (4.6) | +1.8 (8.1) | -30.0 (7.3) | -18.4 (5.7) | -21.2 (5.4) |
| Being born in the US matters for being American | -9.8 (4.3) | +4.5 (3.8) | +0.4 (3.1) | +10.3 (5.1) | -6.9 (6.2) | +8.5 (5.2) | -2.0 (4.8) |
| Obedience over self-reliance | +11.5 (4.6) | +2.2 (3.5) | +5.1 (3.6) | -6.3 (5.9) | +4.0 (6.6) | -2.5 (4.6) | +0.5 (5.0) |
| Respect for elders over independence | +0.9 (3.5) | +3.9 (3.2) | -0.5 (3.0) | -1.4 (4.6) | -8.8 (4.6) | +4.9 (4.7) | -6.3 (4.7) |
| Good manners over curiosity | +9.0 (3.9) | +13.1 (3.3) | +6.1 (3.3) | -2.9 (4.5) | +6.0 (5.9) | +17.9 (3.9) | -0.9 (5.3) |
| Well behaved over being considerate | +13.9 (3.8) | +11.2 (3.2) | +5.3 (3.0) | -8.6 (4.4) | +9.9 (5.4) | +14.1 (4.8) | +3.9 (4.2) |

| Item | H G1 | H G2 | H G3+ | H G3+ − G1 | M G1 | M G2 | M G3+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Authoritarian child-rearing scale (0-4) | +0.351 (0.117) | +0.297 (0.076) | +0.160 (0.085) | -0.191 (0.132) | +0.109 (0.174) | +0.336 (0.113) | -0.028 (0.129) |

### B adjusted. Against white subgroups

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| President acting without Congress and the courts would be helpful | +0.2 (2.7) | +2.0 (3.0) | +9.5 (2.9) | +1.1 (2.9) | +7.5 (1.3) | -10.2 (1.0) |
| A strong leader is good even if the leader bends the rules | -14.6 (4.2) | -8.3 (3.4) | +20.7 (3.3) | -0.9 (3.2) | +29.0 (1.7) | -15.3 (1.5) |
| Democracy is preferable to any other kind of government (2024) | -6.3 (5.4) | -7.7 (5.0) | -10.4 (5.0) | -0.4 (5.2) | -2.7 (2.2) | +8.9 (2.4) |
| Courts should stop the government exceeding its authority (2024) | -5.5 (5.3) | +6.6 (3.7) | +0.5 (3.5) | +11.8 (3.7) | -6.0 (2.1) | +11.9 (2.0) |
| The people, not politicians, should make policy (2020) | -15.7 (4.6) | -2.6 (4.3) | -3.1 (4.4) | -3.4 (4.1) | -0.5 (2.4) | -4.7 (1.9) |
| Votes are counted fairly all or most of the time | +14.1 (3.8) | +11.7 (3.2) | -20.2 (3.2) | +4.4 (3.1) | -31.8 (1.4) | +18.9 (1.4) |
| Political violence at least a little justified | +20.0 (3.2) | +14.1 (2.8) | +5.8 (2.9) | +9.6 (2.7) | -8.3 (1.4) | -2.5 (0.8) |
| Satisfied with the way democracy works in the US | -10.4 (4.6) | -9.6 (3.5) | +6.3 (3.3) | -1.5 (3.4) | +15.9 (1.8) | +3.6 (1.6) |
| Trusts the federal government always or most of the time | +9.9 (2.8) | +7.4 (2.5) | +2.8 (2.5) | +6.6 (2.4) | -4.6 (1.3) | -0.1 (1.0) |
| Trusts election officials a great deal or a lot | -6.7 (3.0) | -0.5 (3.0) | +16.0 (2.9) | +3.6 (3.0) | +16.5 (1.4) | -9.3 (1.2) |
| Minorities should adapt to US customs (2020) | -30.0 (5.8) | -29.7 (4.9) | +12.2 (4.4) | -16.6 (4.6) | +41.9 (1.5) | -14.8 (1.9) |
| Being born in the US matters for being American | -18.3 (4.2) | -8.8 (3.3) | +24.7 (3.5) | -5.2 (3.3) | +33.6 (1.7) | -20.4 (1.4) |
| Obedience over self-reliance | +0.7 (4.7) | -6.4 (3.6) | +25.4 (3.7) | -0.8 (3.8) | +31.8 (1.6) | -20.5 (1.4) |
| Respect for elders over independence | -10.7 (3.4) | -13.0 (3.1) | +24.5 (3.0) | -6.5 (3.2) | +37.4 (1.8) | -20.4 (1.6) |
| Good manners over curiosity | -1.5 (4.0) | -5.4 (3.4) | +33.9 (3.5) | -2.0 (3.6) | +39.3 (1.7) | -28.4 (1.7) |
| Well behaved over being considerate | +9.4 (4.1) | +0.4 (3.2) | +17.3 (3.2) | +2.4 (3.1) | +17.0 (1.5) | -11.6 (1.2) |

| Item | H G1 vs W cons | H G3+ vs W cons | H G3+ vs W lib | H G3+ vs W no BA | W cons − W lib | W BA+ − W no BA |
|---|---:|---:|---:|---:|---:|---:|
| Authoritarian child-rearing scale (0-4) | -0.021 (0.119) | -0.244 (0.087) | +1.009 (0.089) | -0.071 (0.092) | +1.254 (0.048) | -0.811 (0.041) |


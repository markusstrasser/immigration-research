# Where Mexican adult arrivals sit in Mexico's schooling distribution, by arrival cohort

**Verdict:** Middle, a little above the median, in every arrival cohort from 1975–79 to
2020–23, with no cohort-by-cohort rise. Mexico-born adults who arrived in the US at age 20 or
older rank at a mean percentile of 0.51–0.56 (SE 0.002–0.007) among Mexican residents of their own
sex and birth year in the Mexican census nearest their arrival, where 0.50 is a random draw from
Mexico; 11–21% of them fall in their cohort's bottom fifth and 15–25% in its top fifth
[CALCULATION: `position.py`; DATA: `derived/position_main.csv`]. Men rank 0.49–0.55 and women
0.53–0.59. On the main coding, arrivals through 2005–09 had fewer people than Mexico at both ends
(less incomplete primary, less tertiary) and the 2015–19 and 2020–23 arrivals have more at both
ends; that label is less robust than the rank. The 1980s and 1990s arrivals ranked no higher than
the late-1970s arrivals (0.517–0.530 against 0.551), so the "increasingly positive selection" that
Butcher and Piehl measured on institutionalization does not show up in schooling. The one change
that recurs whenever the reference census is held fixed is that arrivals since 2010 rank
0.02–0.07 above the 2000–09 arrivals. Pooled ranks stay within 0.44–0.60 in every
specification computed, including an undercount of the least-schooled non-citizens by 1.75
combined with half of US high-school diplomas re-read as Mexican secundaria; by sex the range is
0.45–0.62. The reference census and the US survey move the rank most (up to 0.07 and 0.06).

Lane: `claude-opus-5-5[1m]`, 2026-09-23, from `BRIEF.md`. It fills the gap that §8 of
[the arrival-cohort memo](../../../research/immigration-mexican-arrival-cohorts-2026-09-18.md)
left open ("an origin attainment distribution **by birth cohort** … was not retrieved here.
**[UNVERIFIED]**"). §8 compared migrant means with Mexico's national 15+ mean; this lane places
each migrant within their own sex and birth year.

## 1. The two questions

**Middle, top or bottom?** Middle. A rank of 0.51–0.56 means the average adult arrival had more
schooling than 51–56% of the Mexicans born in the same year and still living in Mexico
[DATA: `derived/position_main.csv`]. The bottom fifth is under-represented (11–21% of migrants
against 20% by construction) and the top fifth roughly proportional (15–25%). Women are placed
higher than men in every cohort, by 0.01–0.09 [CALCULATION: Table 2]. Men alone sit at the median
(0.49–0.55). This matches the "intermediate" half of Chiquiar and Hanson's "intermediate or
positive selection" on US census data; §6 sets it against the Mexican-data studies that find
negative selection.

**Did each cohort come from higher up than the last?** No. The main series reads 0.551 (1975–79),
0.517, 0.517, 0.530, 0.528, 0.549, 0.510, 0.563, 0.531, 0.540 (2020–23) [DATA:
`derived/position_main.csv`]. Holding the reference census fixed (Table 4 rows ref2000, ref2010,
ref2020) or the survey as well (rows acs2019_ref2020, acs2024_ref2020):

- The 1980s and 1990s cohorts rank no higher than the late-1970s cohort, beyond sampling error,
  in any series.
- The post-2010 cohorts rank above the 2000–09 cohorts by 0.027–0.053 against the 2000 census,
  0.053–0.070 against the 2010 census (0.563 vs 0.510 is the main pair), 0.045–0.059 against the
  2020 census, 0.021–0.043 in the 2019 ACS and 0.049–0.068 in the 2024 ACS [CALCULATION:
  differences of Table 4 cells].
- Against the 1980s and 1990s cohorts, the post-2010 cohorts are 0.00–0.05 higher in the main
  series, −0.01 to +0.02 in the 2019 ACS, and 0.03–0.08 higher against a fixed 2010 or 2020
  census or in the 2024 ACS [CALCULATION: same]. The switch from census to ACS instruments
  accounts for 0.02–0.03 of the fixed-census gaps (§3b), and the 2020 ACS break affects the 2024
  row.

Butcher and Piehl's claim is about crime, not schooling. Their words: "the newly arrived
immigrants in the 1980s and 1990s seem to be particularly unlikely to be involved in criminal
activity, consistent with increasingly positive selection along this dimension" — measured as
institutionalization of all foreign-born men aged 18–40 in the 1980–2000 censuses, with Mexico
never broken out [SOURCE: NBER w13229, as read and quoted in
`../crime_selection_cohorts_2026_09_23/RESULT.md` Part 1]. The schooling data here cannot confirm
or refute a trend in offending; they show that the 1980s and 1990s arrivals were not drawn from
higher in Mexico's schooling distribution than their predecessors. Schooling position is not a
measure of ability or of propensity to offend [INFERENCE].

## 2. Main results

Mexico-born, arrived at age 20 or older, first US survey at 0–5 years since arrival except
1980–84 and 1990–94 (6–10 years; no census falls earlier), placed against the Mexican census
nearest the arrival window. "Clamped" is the weighted share of migrants born too late to be 20 on
that census day, compared with Mexico's 20–24 group. "Tails" compares migrants with Mexico in the
bottom (C1) and top (C5) categories: middle = fewer in both, top = fewer at the bottom and more at
the top, bottom = the reverse, both tails = more in both.

**Table 1. Pooled** [CALCULATION: `position.py`; DATA: `derived/position_main.csv`]

| Arrival cohort | US survey | Mexico census | n | Ridit (SE) | Bottom fifth (SE) | Top fifth (SE) | Clamped | Tails |
|---|---|---|---|---|---|---|---|---|
| 1975-1979 | 1980 | 2000 | 17,038 | 0.551 (0.002) | 0.113 (0.003) | 0.214 (0.003) | 0.00 | middle |
| 1980-1984 | 1990 | 2000 | 16,409 | 0.517 (0.003) | 0.182 (0.003) | 0.195 (0.003) | 0.00 | middle |
| 1985-1989 | 1990 | 2000 | 27,800 | 0.517 (0.002) | 0.195 (0.003) | 0.195 (0.003) | 0.00 | middle |
| 1990-1994 | 2000 | 2000 | 36,636 | 0.530 (0.002) | 0.167 (0.002) | 0.198 (0.002) | 0.00 | middle |
| 1995-1999 | 2000 | 2000 | 56,793 | 0.528 (0.002) | 0.171 (0.002) | 0.194 (0.002) | 0.00 | middle |
| 2000-2004 | 2005 | 2000 | 9,557 | 0.549 (0.004) | 0.155 (0.005) | 0.218 (0.005) | 0.14 | middle |
| 2005-2009 | 2010 | 2010 | 6,402 | 0.510 (0.005) | 0.202 (0.006) | 0.152 (0.005) | 0.00 | middle |
| 2010-2014 | 2015 | 2010 | 3,682 | 0.563 (0.006) | 0.167 (0.008) | 0.235 (0.009) | 0.08 | top |
| 2015-2019 | 2019 | 2020 | 3,649 | 0.531 (0.007) | 0.206 (0.010) | 0.208 (0.009) | 0.00 | both tails |
| 2020-2023 | 2024 | 2020 | 4,862 | 0.540 (0.006) | 0.213 (0.008) | 0.245 (0.008) | 0.06 | both tails |

**Table 2. By sex** (each sex placed against Mexican residents of the same sex) [DATA:
`derived/position_main.csv`]

| Arrival cohort | Men ridit (SE) | Men bottom fifth | Men top fifth | Men tails | Women ridit (SE) | Women bottom fifth | Women top fifth | Women tails |
|---|---|---|---|---|---|---|---|---|
| 1975-1979 | 0.521 (0.003) | 0.131 | 0.175 | middle | 0.589 (0.003) | 0.091 | 0.263 | top |
| 1980-1984 | 0.494 (0.003) | 0.201 | 0.157 | middle | 0.546 (0.004) | 0.158 | 0.241 | top |
| 1985-1989 | 0.498 (0.003) | 0.209 | 0.160 | middle | 0.541 (0.003) | 0.177 | 0.239 | top |
| 1990-1994 | 0.523 (0.002) | 0.174 | 0.176 | middle | 0.536 (0.002) | 0.161 | 0.217 | middle |
| 1995-1999 | 0.515 (0.002) | 0.182 | 0.172 | middle | 0.545 (0.002) | 0.157 | 0.222 | middle |
| 2000-2004 | 0.537 (0.006) | 0.165 | 0.198 | middle | 0.565 (0.005) | 0.140 | 0.245 | middle |
| 2005-2009 | 0.495 (0.006) | 0.220 | 0.123 | bottom | 0.529 (0.006) | 0.179 | 0.188 | middle |
| 2010-2014 | 0.552 (0.008) | 0.176 | 0.210 | middle | 0.576 (0.009) | 0.156 | 0.265 | top |
| 2015-2019 | 0.492 (0.010) | 0.243 | 0.166 | bottom | 0.578 (0.009) | 0.162 | 0.258 | top |
| 2020-2023 | 0.518 (0.008) | 0.240 | 0.221 | both tails | 0.569 (0.008) | 0.176 | 0.277 | both tails |

**Table 3. Five categories: migrant share / Mexican share for the same sex × birth-year mix**
[DATA: `derived/position_main.csv`]. C1 none or primary incomplete; C2 primary complete to
secundaria grade 2; C3 secundaria complete to upper secondary incomplete; C4 upper secondary
complete; C5 any tertiary year (§5 gives the mapping). Gaps are migrant minus Mexico.

Pooled:

| Arrival cohort | C1 | C2 | C3 | C4 | C5 | C1 gap (SE) | C5 gap (SE) |
|---|---|---|---|---|---|---|---|
| 1975-1979 | 0.396 / 0.464 | 0.320 / 0.241 | 0.104 / 0.119 | 0.101 / 0.069 | 0.080 / 0.108 | -0.068 (0.004) | -0.028 (0.002) |
| 1980-1984 | 0.340 / 0.390 | 0.279 / 0.247 | 0.169 / 0.149 | 0.113 / 0.087 | 0.099 / 0.126 | -0.050 (0.004) | -0.027 (0.003) |
| 1985-1989 | 0.287 / 0.315 | 0.243 / 0.244 | 0.203 / 0.194 | 0.142 / 0.110 | 0.124 / 0.137 | -0.028 (0.003) | -0.013 (0.002) |
| 1990-1994 | 0.217 / 0.258 | 0.268 / 0.243 | 0.227 / 0.235 | 0.183 / 0.125 | 0.105 / 0.138 | -0.041 (0.002) | -0.033 (0.002) |
| 1995-1999 | 0.184 / 0.218 | 0.270 / 0.239 | 0.240 / 0.267 | 0.199 / 0.131 | 0.108 / 0.144 | -0.034 (0.002) | -0.037 (0.002) |
| 2000-2004 | 0.137 / 0.189 | 0.267 / 0.238 | 0.196 / 0.288 | 0.287 / 0.138 | 0.113 / 0.148 | -0.051 (0.005) | -0.035 (0.004) |
| 2005-2009 | 0.142 / 0.152 | 0.230 / 0.196 | 0.199 / 0.295 | 0.277 / 0.147 | 0.151 / 0.209 | -0.009 (0.006) | -0.058 (0.006) |
| 2010-2014 | 0.126 / 0.149 | 0.175 / 0.190 | 0.187 / 0.295 | 0.278 / 0.155 | 0.234 / 0.211 | -0.023 (0.007) | +0.023 (0.009) |
| 2015-2019 | 0.113 / 0.095 | 0.147 / 0.144 | 0.175 / 0.301 | 0.276 / 0.195 | 0.288 / 0.264 | +0.018 (0.009) | +0.024 (0.011) |
| 2020-2023 | 0.117 / 0.070 | 0.114 / 0.126 | 0.141 / 0.303 | 0.321 / 0.220 | 0.307 / 0.281 | +0.048 (0.006) | +0.026 (0.009) |

Men:

| Arrival cohort | C1 | C2 | C3 | C4 | C5 | C1 gap (SE) | C5 gap (SE) |
|---|---|---|---|---|---|---|---|
| 1975-1979 | 0.392 / 0.425 | 0.317 / 0.242 | 0.108 / 0.126 | 0.100 / 0.064 | 0.084 / 0.141 | -0.034 (0.005) | -0.058 (0.003) |
| 1980-1984 | 0.328 / 0.348 | 0.272 / 0.246 | 0.176 / 0.161 | 0.117 / 0.084 | 0.107 / 0.161 | -0.020 (0.005) | -0.053 (0.003) |
| 1985-1989 | 0.277 / 0.282 | 0.243 / 0.240 | 0.214 / 0.207 | 0.143 / 0.107 | 0.124 / 0.164 | -0.005 (0.004) | -0.041 (0.003) |
| 1990-1994 | 0.197 / 0.228 | 0.261 / 0.238 | 0.240 / 0.252 | 0.193 / 0.119 | 0.110 / 0.162 | -0.031 (0.003) | -0.053 (0.003) |
| 1995-1999 | 0.171 / 0.195 | 0.275 / 0.236 | 0.251 / 0.284 | 0.200 / 0.127 | 0.103 / 0.158 | -0.023 (0.002) | -0.056 (0.002) |
| 2000-2004 | 0.134 / 0.173 | 0.268 / 0.234 | 0.200 / 0.302 | 0.293 / 0.134 | 0.104 / 0.157 | -0.039 (0.006) | -0.053 (0.006) |
| 2005-2009 | 0.145 / 0.135 | 0.231 / 0.193 | 0.201 / 0.308 | 0.290 / 0.149 | 0.133 / 0.215 | +0.010 (0.008) | -0.082 (0.007) |
| 2010-2014 | 0.112 / 0.127 | 0.175 / 0.186 | 0.202 / 0.311 | 0.296 / 0.157 | 0.215 / 0.218 | -0.015 (0.009) | -0.003 (0.012) |
| 2015-2019 | 0.129 / 0.085 | 0.159 / 0.142 | 0.200 / 0.303 | 0.274 / 0.201 | 0.238 / 0.268 | +0.043 (0.013) | -0.030 (0.013) |
| 2020-2023 | 0.124 / 0.066 | 0.132 / 0.127 | 0.149 / 0.305 | 0.316 / 0.224 | 0.280 / 0.278 | +0.058 (0.008) | +0.001 (0.011) |

Women:

| Arrival cohort | C1 | C2 | C3 | C4 | C5 | C1 gap (SE) | C5 gap (SE) |
|---|---|---|---|---|---|---|---|
| 1975-1979 | 0.401 / 0.512 | 0.325 / 0.239 | 0.098 / 0.110 | 0.101 / 0.074 | 0.074 / 0.065 | -0.111 (0.006) | +0.009 (0.003) |
| 1980-1984 | 0.354 / 0.440 | 0.287 / 0.249 | 0.162 / 0.135 | 0.109 / 0.091 | 0.089 / 0.085 | -0.086 (0.005) | +0.004 (0.003) |
| 1985-1989 | 0.301 / 0.357 | 0.244 / 0.248 | 0.189 / 0.178 | 0.142 / 0.114 | 0.125 / 0.104 | -0.056 (0.004) | +0.021 (0.003) |
| 1990-1994 | 0.235 / 0.285 | 0.275 / 0.247 | 0.215 / 0.221 | 0.174 / 0.131 | 0.102 / 0.117 | -0.050 (0.003) | -0.016 (0.002) |
| 1995-1999 | 0.200 / 0.248 | 0.264 / 0.244 | 0.225 / 0.246 | 0.197 / 0.136 | 0.114 / 0.126 | -0.049 (0.003) | -0.012 (0.002) |
| 2000-2004 | 0.141 / 0.210 | 0.265 / 0.243 | 0.189 / 0.269 | 0.279 / 0.143 | 0.125 / 0.136 | -0.068 (0.006) | -0.010 (0.006) |
| 2005-2009 | 0.140 / 0.172 | 0.228 / 0.200 | 0.197 / 0.280 | 0.262 / 0.145 | 0.174 / 0.203 | -0.033 (0.007) | -0.029 (0.008) |
| 2010-2014 | 0.141 / 0.175 | 0.176 / 0.194 | 0.171 / 0.276 | 0.257 / 0.152 | 0.255 / 0.203 | -0.033 (0.010) | +0.052 (0.012) |
| 2015-2019 | 0.095 / 0.107 | 0.133 / 0.146 | 0.146 / 0.299 | 0.279 / 0.188 | 0.346 / 0.259 | -0.012 (0.009) | +0.088 (0.015) |
| 2020-2023 | 0.109 / 0.075 | 0.089 / 0.124 | 0.129 / 0.301 | 0.328 / 0.215 | 0.344 / 0.284 | +0.034 (0.008) | +0.060 (0.013) |

The C3 and C4 columns carry a signature worth reading before the tails. From the 2000–04 cohort
on, migrants hold C4 (upper secondary complete) at 1.4–2.1 times Mexico's rate and C3 (secundaria
complete, no upper-secondary diploma) at 0.47–0.68 times it [CALCULATION: Table 3 ratios]. A
migrant flow that finished upper secondary twice as often as its cohort while finishing
university less often is possible, but the pattern is also what US surveys would show if Mexican
secundaria completers report a US high-school diploma, the over-reporting Ibarraran and Lubotsky
flag (§6). The `secundaria_as_diploma` variants below price it.

## 3. What moves the rank

**Table 4. Ridit under every specification computed** [CALCULATION: `position.py`; DATA:
`derived/position_all_specs.csv`]. Blank cells were not computed: the check would repeat the
main spec, or the cohort had not yet arrived by that survey.

Pooled:

| Specification | 1975-1979 | 1980-1984 | 1985-1989 | 1990-1994 | 1995-1999 | 2000-2004 | 2005-2009 | 2010-2014 | 2015-2019 | 2020-2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| main | 0.551 | 0.517 | 0.517 | 0.530 | 0.528 | 0.549 | 0.510 | 0.563 | 0.531 | 0.540 |
| nearest_or_next_census | 0.551 | 0.517 | 0.517 | 0.530 | 0.528 | 0.537 | 0.510 | 0.556 | 0.531 | 0.540 |
| ref2000 |  |  |  |  |  |  | 0.558 | 0.590 | 0.585 | 0.602 |
| ref2010 | 0.544 | 0.506 | 0.502 | 0.509 | 0.503 | 0.510 |  |  | 0.573 | 0.580 |
| ref2020 | 0.518 | 0.483 | 0.481 | 0.488 | 0.478 | 0.481 | 0.483 | 0.528 |  |  |
| acs2019_ref2020 | 0.530 | 0.516 | 0.526 | 0.510 | 0.509 | 0.488 | 0.499 | 0.520 | 0.531 |  |
| acs2024_ref2020 | 0.492 | 0.489 | 0.500 | 0.494 | 0.492 | 0.479 | 0.485 | 0.536 | 0.534 | 0.547 |
| arrival_age_18plus | 0.543 | 0.510 | 0.512 | 0.525 | 0.523 | 0.550 | 0.503 | 0.559 | 0.527 | 0.535 |
| arrival_age_25plus | 0.578 | 0.535 | 0.524 | 0.536 | 0.534 | 0.551 | 0.522 | 0.567 | 0.538 | 0.548 |
| arrival_age_20plus_certain | 0.571 | 0.523 | 0.522 | 0.531 | 0.530 | 0.548 | 0.514 | 0.567 | 0.532 | 0.544 |
| not_enrolled | 0.540 | 0.493 | 0.491 | 0.520 | 0.517 | 0.543 | 0.503 | 0.552 | 0.521 | 0.532 |
| both_sex_reference | 0.557 | 0.521 | 0.520 | 0.530 | 0.530 | 0.550 | 0.510 | 0.562 | 0.530 | 0.538 |
| credential_convention | 0.551 | 0.517 | 0.517 | 0.530 | 0.528 | 0.549 | 0.510 | 0.563 | 0.531 | 0.540 |
| split_neutral / low / high | 0.551 | 0.517 | 0.517 | 0.530 | 0.528 | 0.549 | 0.510 | 0.563 | 0.531 | 0.540 |
| 12th_no_diploma_as_upper_secondary | 0.551 | 0.521 | 0.522 | 0.535 | 0.533 | 0.551 | 0.513 | 0.566 | 0.534 | 0.544 |
| secundaria_as_diploma_0.25 | 0.551 | 0.514 | 0.511 | 0.522 | 0.518 | 0.532 | 0.495 | 0.548 | 0.516 | 0.519 |
| secundaria_as_diploma_0.5 | 0.551 | 0.510 | 0.504 | 0.513 | 0.507 | 0.516 | 0.479 | 0.533 | 0.500 | 0.499 |

Men:

| Specification | 1975-1979 | 1980-1984 | 1985-1989 | 1990-1994 | 1995-1999 | 2000-2004 | 2005-2009 | 2010-2014 | 2015-2019 | 2020-2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| main | 0.521 | 0.494 | 0.498 | 0.523 | 0.515 | 0.537 | 0.495 | 0.552 | 0.492 | 0.518 |
| nearest_or_next_census | 0.521 | 0.494 | 0.498 | 0.523 | 0.515 | 0.525 | 0.495 | 0.544 | 0.492 | 0.518 |
| ref2000 |  |  |  |  |  |  | 0.537 | 0.584 | 0.542 | 0.597 |
| ref2010 | 0.518 | 0.485 | 0.484 | 0.505 | 0.491 | 0.499 |  |  | 0.544 | 0.567 |
| ref2020 | 0.497 | 0.466 | 0.466 | 0.485 | 0.467 | 0.470 | 0.467 | 0.515 |  |  |
| acs2019_ref2020 | 0.509 | 0.492 | 0.508 | 0.498 | 0.510 | 0.488 | 0.482 | 0.498 | 0.492 |  |
| acs2024_ref2020 | 0.452 | 0.459 | 0.484 | 0.479 | 0.479 | 0.473 | 0.483 | 0.518 | 0.519 | 0.527 |
| arrival_age_18plus | 0.512 | 0.488 | 0.494 | 0.517 | 0.510 | 0.538 | 0.487 | 0.547 | 0.487 | 0.512 |
| arrival_age_25plus | 0.548 | 0.512 | 0.501 | 0.530 | 0.519 | 0.537 | 0.503 | 0.558 | 0.501 | 0.526 |
| arrival_age_20plus_certain | 0.540 | 0.500 | 0.502 | 0.524 | 0.516 | 0.537 | 0.497 | 0.555 | 0.493 | 0.523 |
| not_enrolled | 0.509 | 0.471 | 0.472 | 0.514 | 0.504 | 0.533 | 0.488 | 0.542 | 0.483 | 0.512 |
| both_sex_reference | 0.555 | 0.524 | 0.522 | 0.542 | 0.527 | 0.546 | 0.498 | 0.552 | 0.490 | 0.513 |
| credential_convention, split_* | 0.521 | 0.494 | 0.498 | 0.523 | 0.515 | 0.537 | 0.495 | 0.552 | 0.492 | 0.518 |
| 12th_no_diploma_as_upper_secondary | 0.521 | 0.497 | 0.502 | 0.528 | 0.520 | 0.539 | 0.497 | 0.554 | 0.495 | 0.522 |
| secundaria_as_diploma_0.25 | 0.521 | 0.490 | 0.491 | 0.514 | 0.505 | 0.520 | 0.478 | 0.535 | 0.476 | 0.497 |
| secundaria_as_diploma_0.5 | 0.521 | 0.486 | 0.484 | 0.505 | 0.494 | 0.502 | 0.461 | 0.518 | 0.460 | 0.477 |

Women:

| Specification | 1975-1979 | 1980-1984 | 1985-1989 | 1990-1994 | 1995-1999 | 2000-2004 | 2005-2009 | 2010-2014 | 2015-2019 | 2020-2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| main | 0.589 | 0.546 | 0.541 | 0.536 | 0.545 | 0.565 | 0.529 | 0.576 | 0.578 | 0.569 |
| nearest_or_next_census | 0.589 | 0.546 | 0.541 | 0.536 | 0.545 | 0.553 | 0.529 | 0.570 | 0.578 | 0.569 |
| ref2000 |  |  |  |  |  |  | 0.581 | 0.596 | 0.622 | 0.607 |
| ref2010 | 0.577 | 0.531 | 0.523 | 0.513 | 0.519 | 0.526 |  |  | 0.605 | 0.598 |
| ref2020 | 0.546 | 0.504 | 0.501 | 0.490 | 0.493 | 0.495 | 0.503 | 0.544 |  |  |
| acs2019_ref2020 | 0.551 | 0.542 | 0.547 | 0.520 | 0.509 | 0.488 | 0.514 | 0.542 | 0.578 |  |
| acs2024_ref2020 | 0.528 | 0.524 | 0.518 | 0.507 | 0.504 | 0.485 | 0.487 | 0.556 | 0.550 | 0.574 |
| arrival_age_18plus | 0.584 | 0.539 | 0.537 | 0.533 | 0.542 | 0.568 | 0.524 | 0.574 | 0.575 | 0.566 |
| arrival_age_25plus | 0.613 | 0.560 | 0.552 | 0.541 | 0.553 | 0.569 | 0.544 | 0.577 | 0.580 | 0.577 |
| arrival_age_20plus_certain | 0.608 | 0.548 | 0.547 | 0.538 | 0.547 | 0.564 | 0.535 | 0.581 | 0.578 | 0.571 |
| not_enrolled | 0.579 | 0.519 | 0.515 | 0.526 | 0.533 | 0.557 | 0.522 | 0.563 | 0.566 | 0.560 |
| both_sex_reference | 0.559 | 0.518 | 0.519 | 0.519 | 0.533 | 0.556 | 0.525 | 0.573 | 0.578 | 0.573 |
| credential_convention, split_* | 0.589 | 0.546 | 0.541 | 0.536 | 0.545 | 0.565 | 0.529 | 0.576 | 0.578 | 0.569 |
| 12th_no_diploma_as_upper_secondary | 0.589 | 0.549 | 0.546 | 0.541 | 0.550 | 0.567 | 0.532 | 0.579 | 0.580 | 0.573 |
| secundaria_as_diploma_0.25 | 0.589 | 0.542 | 0.535 | 0.529 | 0.535 | 0.549 | 0.515 | 0.563 | 0.562 | 0.549 |
| secundaria_as_diploma_0.5 | 0.589 | 0.539 | 0.529 | 0.521 | 0.525 | 0.534 | 0.500 | 0.549 | 0.547 | 0.529 |

The recent cohorts in other ACS years: 2015–19 arrivals 0.555 (SE 0.008) in the 2020 ACS and
0.529 (0.007) in the 2021 ACS; 2020–23 arrivals 0.536 (0.006) in the 2023 ACS
[DATA: `derived/position_all_specs.csv`, specs `survey2020`, `survey2021`, `survey2023`].
The ridit uses only cut points both sides share, so it does not depend on how straddling US bins
are split; the split rules change only the five-category shares.

**The tails label is less robust than the rank.** Pooled "tails" by specification
[DATA: `derived/position_all_specs.csv`]:

| Specification | 1975-79 | 1980-84 | 1985-89 | 1990-94 | 1995-99 | 2000-04 | 2005-09 | 2010-14 | 2015-19 | 2020-23 |
|---|---|---|---|---|---|---|---|---|---|---|
| main (also nearest_or_next, all three arrival-age variants, both_sex, credential, neutral split, 12th, both secundaria variants) | middle | middle | middle | middle | middle | middle | middle | top | both | both |
| ref2000 |  |  |  |  |  |  | top | top | top | both |
| ref2010 | middle | middle | middle | middle | middle | middle |  |  | top | both |
| ref2020 | middle | middle | bottom | middle | middle | middle | bottom | middle |  |  |
| acs2019_ref2020 | middle | middle | middle | bottom | bottom | bottom | bottom | bottom | both |  |
| acs2024_ref2020 | bottom | bottom | bottom | bottom | bottom | bottom | bottom | both | both | both |
| not_enrolled | middle | middle | bottom | middle | middle | middle | middle | top | both | both |
| split_low | middle | bottom | bottom | bottom | bottom | bottom | middle | top | both | both |
| split_high | middle | middle | top | middle | middle | middle | middle | top | both | both |

The C1 comparison for 1980–2004 turns on how the 1990 "grade 5–8" and 2000/2005 "grade 5 or 6"
bins are split between C1 and C2 (`split_low` puts them all in C1). The 2024-ACS row is affected
by the 2020 break in §3b.

### 3a. The reference census

The same Mexican birth cohorts look more schooled in each later census: against the 2020 census
the pre-2010 cohorts rank 0.03–0.07 lower than against the nearest census, and against the 2000
census the post-2005 cohorts rank 0.03–0.06 higher [CALCULATION: Table 4, rows ref2000/ref2010/
ref2020 vs main]. Mortality selection among older Mexicans, adult certification programmes,
return migrants re-entering the Mexican count and young adults still studying in the earlier
census could each contribute; this lane does not separate them [INFERENCE]. The main
specification uses the census nearest the arrival window, which measures the Mexican cohort
closest to the time the migrants left. The 2000–04 cohort is compared with a 2000 census in which
14% of its weight was under 20 (and compared with the 20–24 group, not all of whom had finished
school); using the 2010 census for those migrants lowers its rank from 0.549 to 0.537 (row
`nearest_or_next_census`).

### 3b. The US instrument

**Census long form versus ACS.** Every cohort observed in the 2000 census ranks higher in the
2005 ACS and then roughly flat through 2019 (§4). The ACS 2000–2004 use the same education
categories as the long form (the same set of EDUCD codes appears in both [DATA: extracts #3 and
#12]) and observe the same cohorts within 0–4 years of it. They already show the higher rank, so
the jump belongs to the survey rather than to return migration or US schooling acquired after
2000:

**Table 5. Same cohorts, census 2000 long form vs ACS** [CALCULATION: `instrument_checks.py`;
DATA: `derived/instrument_checks.csv`; IPUMS extracts #3 and #12]

| Arrival cohort | Survey | n | Edited or allocated | HS diploma share | Ridit (SE) | Ridit, education as reported |
|---|---|---|---|---|---|---|
| 1985-1989 | census 2000 long form | 33,045 | 0.125 | 0.143 | 0.545 (0.002) | 0.537 |
| 1985-1989 | ACS 2000 | 620 | 0.093 | 0.143 | 0.573 (0.013) | 0.563 |
| 1985-1989 | ACS 2000-2004 | 7,869 | 0.070 | 0.171 | 0.573 (0.004) | 0.567 |
| 1985-1989 | ACS 2005 | 5,467 | 0.063 | 0.188 | 0.567 (0.005) | 0.563 |
| 1990-1994 | census 2000 long form | 36,636 | 0.136 | 0.157 | 0.530 (0.002) | 0.521 |
| 1990-1994 | ACS 2000 | 681 | 0.089 | 0.179 | 0.550 (0.013) | 0.541 |
| 1990-1994 | ACS 2000-2004 | 8,282 | 0.069 | 0.194 | 0.554 (0.004) | 0.545 |
| 1990-1994 | ACS 2005 | 5,568 | 0.063 | 0.223 | 0.553 (0.005) | 0.546 |
| 1995-1999 | census 2000 long form | 56,793 | 0.151 | 0.175 | 0.528 (0.002) | 0.517 |
| 1995-1999 | ACS 2000 | 948 | 0.108 | 0.228 | 0.558 (0.013) | 0.544 |
| 1995-1999 | ACS 2000-2004 | 12,138 | 0.090 | 0.226 | 0.559 (0.004) | 0.550 |
| 1995-1999 | ACS 2005 | 7,943 | 0.068 | 0.261 | 0.564 (0.004) | 0.558 |

The ACS 2000–2004 place each cohort 0.024–0.031 above the long form (0.021–0.037 by sex), with or
without allocated records [CALCULATION: Table 5 differences; by sex in
`derived/instrument_checks.csv`]. The ACS 2001–02 and 2003–04 pairs agree with the pooled figure
to within 0.01 (in the CSV). Which instrument is closer to the truth is not identified here. The
higher ACS rank comes with a higher high-school-diploma share, so the secundaria-as-diploma
question (Table 3 note) and the survey question are probably the same problem [INFERENCE].

**CPS.** The 1990–94 cohort at 0–5 years since arrival in the March 1994 and 1995 CPS ranks
0.494 (SE 0.014, n = 934): men 0.453 (0.020), women 0.537 (0.015), against 0.530, 0.523 and 0.536
in the 2000 census at 6–10 years [CALCULATION: `cps_check.py`; DATA:
`derived/cps_check_1990_94.csv`; IPUMS-CPS extract in
`sources/immigration-fiscal/data/external/cps/`]. The gap mixes instrument, sampling (2.5 SE) and
the departure of less-schooled men between 1995 and 2000; the within-ACS drift in §4 suggests
departures after the first observation move the rank by at most 0.03.

**A 2020 break in the ACS.** For a fixed set of people (arrived 1975–2009 at 20+, aged 25+), the
share reporting "no schooling completed", among records whose education was not edited or
allocated, rises from 0.075 (2012) to 0.092 (2019), then jumps to 0.130 (2020) and reaches 0.146
(2024), while grade 6 falls from 0.173 (2019) to 0.141 (2020) [CALCULATION: `instrument_checks.py`;
DATA: `derived/acs_break_2020.csv`]. People do not lose schooling, so the ACS from 2020 onward
records this population lower at the bottom; the cause (mode of response, questionnaire, editing)
is not identified here [INFERENCE]. It lowers every cohort's rank in the 2024 ACS row of Table 4
and inflates C1 for the 2020–23 cohort, whose main survey is the 2024 ACS (C1 0.117 against
Mexico's 0.070). The 2015–19 cohort's excess C1 (0.113 against 0.095) was measured in the 2019
ACS, before the break.

### 3c. Allocated education

The Census Bureau fills missing education by allocation; IPUMS flags it (QEDUC). Dropping edited
or allocated records lowers every cohort's rank, by 0.008–0.018 pooled and 0.004–0.021 by sex
[CALCULATION:
`instrument_checks.py`; DATA: `derived/instrument_checks.csv`; IPUMS extract #13]:

| Arrival cohort | Survey | Edited or allocated | Pooled: all → as reported | Men | Women |
|---|---|---|---|---|---|
| 1975-1979 | 1980 | 0.142 | 0.551 → 0.535 | 0.521 → 0.504 | 0.589 → 0.573 |
| 1980-1984 | 1990 | 0.081 | 0.517 → 0.504 | 0.494 → 0.480 | 0.546 → 0.531 |
| 1985-1989 | 1990 | 0.081 | 0.517 → 0.507 | 0.498 → 0.488 | 0.541 → 0.531 |
| 1990-1994 | 2000 | 0.136 | 0.530 → 0.521 | 0.523 → 0.515 | 0.536 → 0.526 |
| 1995-1999 | 2000 | 0.151 | 0.528 → 0.517 | 0.515 → 0.501 | 0.545 → 0.536 |
| 2000-2004 | 2005 | 0.088 | 0.549 → 0.540 | 0.537 → 0.526 | 0.565 → 0.558 |
| 2005-2009 | 2010 | 0.123 | 0.510 → 0.501 | 0.495 → 0.482 | 0.529 → 0.524 |
| 2010-2014 | 2015 | 0.149 | 0.563 → 0.555 | 0.552 → 0.542 | 0.576 → 0.568 |
| 2015-2019 | 2019 | 0.168 | 0.531 → 0.523 | 0.492 → 0.478 | 0.578 → 0.574 |
| 2020-2023 | 2024 | 0.204 | 0.540 → 0.522 | 0.518 → 0.497 | 0.569 → 0.555 |

Dropping allocated records assumes they are missing at random within the cohort, so this is a
sensitivity check, not a correction. The Census Bureau's own 2015 PUMS gives the same 2010–14
figures as IPUMS to four decimals (ridit 0.5632), a 14.9% allocation share (FSCHLP) and 0.555 with
allocated records dropped [CALCULATION: `acs_pums_check.py`; DATA: `derived/acs_pums_check.csv`].

### 3d. Undercount of the least-schooled

Fernández-Huertas Moraga's abstract: "The discrepancy is primarily due to an undercount of
unskilled migrants in U.S. sources" (quoted from the RePEc record in memo §8). The test
multiplies the weight of non-citizen migrants in C1 by k. Non-citizens include legal
permanent residents, so this overstates the base the undercount applies to.

**Table 6. Ridit under an undercount of k, alone and combined with half of US diplomas read as
secundaria** [CALCULATION: `position.py`; DATA: `derived/undercount_sensitivity.csv`]

| US coding | Arrival cohort | Non-citizen share | k=1 | k=1.25 | k=1.5 | k=1.75 | Migrant C1 (k=1 → 1.75) | Mexico C1 | k for ridit 0.5 | k for C1 = Mexico |
|---|---|---|---|---|---|---|---|---|---|---|
| as coded | 1975-1979 | 0.89 | 0.551 | 0.532 | 0.515 | 0.501 | 0.396 → 0.523 | 0.464 | 1.78 | 1.36 |
| as coded | 1980-1984 | 0.81 | 0.517 | 0.499 | 0.483 | 0.468 | 0.340 → 0.435 | 0.390 | 1.24 | 1.30 |
| as coded | 1985-1989 | 0.91 | 0.517 | 0.496 | 0.478 | 0.462 | 0.287 → 0.389 | 0.315 | 1.20 | 1.16 |
| as coded | 1990-1994 | 0.90 | 0.530 | 0.514 | 0.499 | 0.485 | 0.217 → 0.304 | 0.258 | 1.48 | 1.28 |
| as coded | 1995-1999 | 0.94 | 0.528 | 0.513 | 0.499 | 0.486 | 0.184 → 0.263 | 0.218 | 1.48 | 1.25 |
| as coded | 2000-2004 | 0.96 | 0.549 | 0.536 | 0.524 | 0.513 | 0.137 → 0.199 | 0.189 | 2.06 | 1.48 |
| as coded | 2005-2009 | 0.95 | 0.510 | 0.497 | 0.484 | 0.473 | 0.142 → 0.223 | 0.152 | 1.19 | 1.08 |
| as coded | 2010-2014 | 0.93 | 0.563 | 0.550 | 0.538 | 0.526 | 0.126 → 0.197 | 0.149 | 2.36 | 1.23 |
| as coded | 2015-2019 | 0.94 | 0.531 | 0.519 | 0.508 | 0.497 | 0.113 → 0.180 | 0.095 | 1.68 | 0.82 |
| as coded | 2020-2023 | 0.95 | 0.540 | 0.526 | 0.513 | 0.501 | 0.117 → 0.186 | 0.070 | 1.77 | 0.54 |
| diploma 0.5 | 1975-1979 | 0.89 | 0.551 | 0.532 | 0.515 | 0.501 | 0.396 → 0.523 | 0.464 | 1.78 | 1.36 |
| diploma 0.5 | 1980-1984 | 0.81 | 0.510 | 0.492 | 0.476 | 0.462 | 0.340 → 0.435 | 0.390 | 1.13 | 1.30 |
| diploma 0.5 | 1985-1989 | 0.91 | 0.504 | 0.485 | 0.467 | 0.452 | 0.287 → 0.389 | 0.315 | 1.05 | 1.16 |
| diploma 0.5 | 1990-1994 | 0.90 | 0.513 | 0.497 | 0.483 | 0.470 | 0.217 → 0.304 | 0.258 | 1.21 | 1.28 |
| diploma 0.5 | 1995-1999 | 0.94 | 0.507 | 0.493 | 0.480 | 0.467 | 0.184 → 0.263 | 0.218 | 1.12 | 1.25 |
| diploma 0.5 | 2000-2004 | 0.96 | 0.516 | 0.504 | 0.493 | 0.483 | 0.137 → 0.199 | 0.189 | 1.35 | 1.48 |
| diploma 0.5 | 2005-2009 | 0.95 | 0.479 | 0.466 | 0.455 | 0.444 | 0.142 → 0.223 | 0.152 | ≤ 0.5 at k=1 | 1.08 |
| diploma 0.5 | 2010-2014 | 0.93 | 0.533 | 0.521 | 0.509 | 0.498 | 0.126 → 0.197 | 0.149 | 1.70 | 1.23 |
| diploma 0.5 | 2015-2019 | 0.94 | 0.500 | 0.488 | 0.478 | 0.468 | 0.113 → 0.180 | 0.095 | ≤ 0.5 at k=1 | 0.82 |
| diploma 0.5 | 2020-2023 | 0.95 | 0.499 | 0.487 | 0.475 | 0.464 | 0.117 → 0.186 | 0.070 | ≤ 0.5 at k=1 | 0.54 |

As coded, an undercount of 1.19–2.36 brings each cohort to the median; with half of diplomas
re-read as secundaria, 1.05–1.78, and three ACS-era cohorts are already at or below it. The 1980
census has no diploma item, so the 1975–79 rows do not change. The brief's range of k (1.1–1.75)
therefore spans "a little above the median" to "a little below it"; it does not reach "bottom".

### 3e. Coding and population variants

- **Some college.** "Some college, less than one year" counts as upper secondary complete (C4);
  "one or more years, no degree" is tertiary attended (C5) in the main convention and upper
  secondary in `credential_convention`, where C5 requires a short-cycle credential or four or more
  years, matching INEGI's ISCED 5–8. The ridit does not change; C5 does (in the CSV).
- **12th grade, no diploma** sits between Mexican upper-secondary grade 2 and completion; treating
  it as completion raises ranks by 0.000–0.005.
- **Secundaria reported as a diploma.** Moving 25% or 50% of US regular-diploma holders to
  "secundaria complete" lowers ACS-era ranks by 0.015–0.021 and 0.030–0.041, and 1990–2000
  census ranks by 0.003–0.010 and 0.007–0.021; the 1980 census has no diploma item
  [CALCULATION: Table 4 differences]. The true share is not known.
- **Arrival age** 18+ changes ranks by −0.008 to +0.001; 25+ raises them by 0.002–0.027;
  requiring arrival age 20 on the earliest possible birthday changes them by −0.001 to +0.020.
- **US schooling.** Dropping migrants enrolled at the survey lowers ranks by 0.006–0.026, a lower
  bound on schooling added in the US since those no longer enrolled may also have studied there.
- **Both-sex reference** (each migrant against both sexes of their birth year) narrows the gap
  between men and women; the pooled rank moves by at most 0.006.

## 4. Survivors

The same arrival cohort observed in later surveys, against its main reference census
[CALCULATION: `position.py`; DATA: `derived/survivor_drift.csv`]:

| Arrival cohort | Mexico census | 1980 | 1990 | 2000 | 2005 | 2010 | 2015 | 2019 | 2024 |
|---|---|---|---|---|---|---|---|---|---|
| 1975-1979 | 2000 | 0.551 | 0.514 | 0.534 | 0.551 | 0.535 | 0.527 | 0.557 | 0.517 |
| 1980-1984 | 2000 |  | 0.517 | 0.535 | 0.563 | 0.545 | 0.533 | 0.547 | 0.517 |
| 1985-1989 | 2000 |  | 0.517 | 0.545 | 0.567 | 0.551 | 0.556 | 0.562 | 0.535 |
| 1990-1994 | 2000 |  |  | 0.530 | 0.553 | 0.554 | 0.540 | 0.551 | 0.532 |
| 1995-1999 | 2000 |  |  | 0.528 | 0.564 | 0.551 | 0.547 | 0.559 | 0.539 |
| 2000-2004 | 2000 |  |  |  | 0.549 | 0.548 | 0.541 | 0.551 | 0.541 |
| 2005-2009 | 2010 |  |  |  |  | 0.510 | 0.523 | 0.526 | 0.512 |
| 2010-2014 | 2010 |  |  |  |  |  | 0.563 | 0.554 | 0.572 |
| 2015-2019 | 2020 |  |  |  |  |  |  | 0.531 | 0.534 |
| 2020-2023 | 2020 |  |  |  |  |  |  |  | 0.540 |

Between each cohort's first ACS observation and the 2019 ACS its rank moves by −0.030 to
+0.016, across the 2008 switch to single-grade coding; the 2000→2005 jump is the instrument (§3b)
and the 2019→2024 fall coincides with the 2020 break [CALCULATION: differences of this table]. So
departures after the first observation move the rank little on the ACS. ENADID puts male
returnees 1.3–1.6 years of schooling below non-migrant men and finds women returnees
indistinguishable from non-migrant women [SOURCE:
`../enadid_return_selectivity_2026_09_22/RESULT.md`, verdict]. Departures before the first US
observation are not measured here; the CPS check (§3b) bounds them for one cohort.

## 5. Method

**Estimand.** For each arrival cohort (1975–79 … 2015–19, 2020–23) of Mexico-born people who
arrived at age 20 or older (18+ and 25+ as variants): the migrant-weighted mean, over migrants,
of each migrant's percentile rank in the attainment distribution of Mexican residents of the same
sex and birth year, with ties spread (ridit: rank = share below + half the share tied; 0.5 is a
random draw); the share of migrants in each fifth of that distribution; and five-category shares
next to Mexico's shares for the migrants' sex × birth-year mix.

**Origin side.** INEGI census tabulations by sex × five-year age × level and grade, pinned with
URL, size and sha256 in `sources.json` [SOURCE: `sources.json`]:

- 2000: XII Censo, tabulados básicos, national *Características educativas* PDF, Educación 5
  (primaria grades), 7 (secundaria and técnico con primaria), 8 (media superior, parts 1–2) and
  9 (profesional grades), parsed with `pdftotext -layout` and checked row by row against each
  table's population identity.
- 2010: Censo, cuestionario básico, Educación 8, 10, 11, 12 (grades) and 14 (levels and grado
  promedio, the anchor).
- 2020: Censo, cuestionario básico, Educación 11 (levels and grades) and 13 (ISCED, the anchor),
  from the repository's staged workbook.
- Not used: the 2015 Intercensal workbook was fetched and pinned, but for five-year age groups it
  gives primaria as one total and media superior and superior without grades, so neither the
  C1/C2 nor the C3/C4 boundary can be drawn by birth cohort. No national 1990 education-by-age
  tabulation was found on inegi.org.mx, so 2000 is the earliest reference.
- IPUMS International (the brief's preferred origin source) refused the extract: HTTP 401, the
  account is not registered to IPUMS International [DATA: `extracts.py submit` output].

Origin anchors [CALCULATION: `origin_inegi.py`; DATA: `derived/origin_anchors.csv`]: the 2010
mean years on the shared scale are within 0.051 years of INEGI's grado promedio in every sex × age
cell (median 0.029), and its media-superior and superior shares match Educación 14 exactly; the
2020 C1–C3 share matches sheet 13's ISCED 0–2 within 0.0006 and the credential-convention C5
matches ISCED 5–8 within 0.003; 2020 mean years differ from INEGI's by up to 0.126 (median 0.087).
That gap is not traced; the scale fixes years for levels INEGI may count differently, such as
posgrado and técnico courses [INFERENCE]. National 15+ mean years on the scale
are 7.48 (2000), 8.61 (2010) and 9.66 (2020) [CALCULATION: `derived/origin_five.csv`] against
INEGI's published 7.5, 8.6 and 9.7 [SOURCE: INEGI, quoted in memo §8].

**Migrant side.** IPUMS USA extract #3: every Mexico-born (BPL 200) record in the 1980, 1990 and
2000 5% censuses and the ACS 2005–2024, with SEX, BIRTHYR, YRIMMIG, CITIZEN, EDUCD, SCHOOL and
household ids; extract #12 adds the ACS 2000–2004 and extract #13 the QEDUC flag for all of them.
All three files match the sha256 IPUMS publishes [DATA: `_cache/*.manifest.json`]. Extract #3
reproduces the held panel's Mexico-born record counts exactly (1980 112,105; 1990 217,948; 2000
450,076; 2010 94,850; 2023 92,321) [DATA: `_cache/us_mexborn.data.csv.gz` vs
`ipums_usa_borjas_panel`]. Arrival cohort comes from YRIMMIG (bracketed in 1980 and 1990; the
bracket's first year sets the cohort and its midpoint the arrival age); arrival age is YRIMMIG −
BIRTHYR, uncertain by about a year.

**Shared scale and mapping** (`levels.py`, `position.py`, `origin_inegi.py`):

| Level | Mexico (INEGI) | US (IPUMS EDUCD; ACS SCHL) | Category |
|---|---|---|---|
| L0 | sin escolaridad, preescolar | no schooling, nursery, kindergarten | C1 |
| L1–L5 | primaria grades 1–5 | grades 1–5 | C1 |
| L6 | primaria 6 | grade 6 | C2 |
| L7–L8 | secundaria 1–2; técnico con primaria (split by 2010 grade shares) | grades 7–8 | C2 |
| L9 | secundaria 3 | grade 9 | C3 |
| L10–L11 | media superior 1–2 (prepa, técnico con secundaria) | grades 10–11 | C3 |
| L11b | (none) | 12th grade, no diploma | C3 |
| L12 | media superior 3+, normal básica | high-school diploma, GED, some college < 1 year; 1980 "finished grade 12" | C4 |
| L13a | licenciatura 1–3 | 1+ years of college, no degree | C5 (C4 under the credential convention) |
| L13b | técnico con preparatoria / técnico superior | associate degree | C5 |
| L16 | licenciatura 4+, posgrado | bachelor's or higher | C5 |

Bins that span levels: 1980 years of college without degree information (L13a–L13b); 1990
"grade 5–8" (L5–L8) and "some college, no degree" (L12–L13a); 2000 and ACS 2000–2007 "nursery to
grade 4" (L0–L4), "grade 5 or 6" (L5–L6) and "grade 7 or 8" (L7–L8); Mexican 2000 profesional
1–3, which includes técnico con preparatoria (L13a–L13b). The ridit uses the finest partition
whose cut points exist on both sides for the survey and census compared, so it needs no split.
Five-category shares split a straddling US bin by the same arrival cohort's own single-grade
distribution in the ACS 2008–2012 (main), by Mexico's distribution within the bin (neutral), or
wholly to the lower or upper category (bounds).

**Birth-year matching.** A birth year straddles two five-year age groups on census day; the
Mexican reference mixes them by the share of the year before census day (2000: 44/366; 2010:
162/365; 2020: 74/366). Migrants too young to be 20 on that day are compared with the 20–24
group (reported as "clamped").

**Reference census.** Main: 2000 for arrivals 1975–2004, 2010 for 2005–14, 2020 for 2015–23
(nearest held census to the window; for 2015–19 the 2015 Intercensal would be as near but lacks
the grades). Variants: the next census for migrants under 20 at the nearest one; each fixed
census, restricted to migrants aged 20 or older on its census day; and one survey for all cohorts
(ACS 2019 or 2024, against 2020).

**Standard errors.** Taylor linearisation with households as with-replacement clusters, strata
ignored. On the 2015 PUMS the Census Bureau's 80 replicate weights give SEs 0.72–0.93 times the
linearised ones, so the linearised SEs are conservative [DATA: `derived/acs_pums_check.csv`]. The
INEGI tables used are complete counts, so the origin shares carry no sampling error.

## 6. Competing evidence

- **Chiquiar & Hanson (2005)**, US and Mexican census data 1990–2000: "in terms of observable
  skills there is intermediate or positive selection of immigrants from Mexico" [SOURCE: NBER
  w9242, quoted in memo §8]. This lane's US-data rank of 0.51–0.56 agrees with "intermediate".
- **Fernández-Huertas Moraga (2011)**, a Mexican household survey "that identifies emigrants
  before they leave", 2000–2004 emigrants: "less (more for females) schooling than nonmigrant
  Mexicans, evidence of negative selection"; "The discrepancy is primarily due to an undercount
  of unskilled migrants in U.S. sources" [SOURCE: RePEc abstract, quoted in memo §8]. The sex pattern matches Table 2 (women above men). The undercount needed to
  bring this lane's cohorts to the median is 1.19–2.36 as coded and 1.05–1.78 with the diploma
  correction (Table 6).
- **Ibarraran & Lubotsky (2007)**, 2000 Mexican census: negative selection. As summarised by
  Rendall and Parker, they "noted that differences in Mexican and U.S. school systems may lead to
  over-reporting of high school graduate levels of educational attainment among Mexican-born
  individuals in U.S. data sources" and that "the Census Bureau imputes the education for as many
  as a fifth of Mexican-born individuals in the U.S., but using predictor variables not including
  nativity" [SOURCE: Rendall & Parker 2014, PMC4435733; I&L not read directly]. Measured here:
  8–20% of records edited or allocated, worth 0.008–0.018 of pooled rank (§3c); the diploma
  over-report is consistent with Table 3's C3/C4 pattern and is priced, not measured (§3e).
- **Rendall & Parker (2014)**, *Population and Development Review* 40(3):421–446, four Mexican
  surveys: "strongly negative educational selection of Mexican migrants throughout the 1990s and
  2000s". For circular migrants (over 80% male), the share who continued past lower secondary was
  "8 and 12 percentage points lower than for all 18 to 54 year old residents in the 1992 and 1997
  years, and as much as 18 and 21 percentage points lower … in the 2002 and 2009 years"; they
  became "increasing[ly] more negatively selected" from 1992 to 2009 [SOURCE:
  https://doi.org/10.1111/j.1728-4457.2014.00692.x, PMC4435733 full text]. Their migrants are
  people back in Mexico, whom ENADID finds negatively selected among men; this lane's are people
  still in the US. Part of the disagreement is who is counted, part is the US measurement priced
  in §3 [INFERENCE].

The two sides split by data source, as Rendall and Parker note: US sources give intermediate to
positive selection, Mexican sources negative [SOURCE: PMC4435733]. This lane uses US sources for
migrants and cannot escape their biases; it can say how large the biases would have to be. An
undercount of 1.19–2.36 alone, or half of diplomas re-read as secundaria together with an
undercount of up to 1.78, puts each cohort at the median (Table 6). No stress test moves the
pooled rank below 0.44 or above 0.60.

## 7. Limits

1. The origin side is five-year tabulations, not microdata; birth years are mixed across two age
   groups, and the 1975–99 cohorts are placed against the 2000 census, up to 25 years after they
   left, because no 1990 table was found.
2. The Mexican reference is the population still in Mexico at the census, not the full birth
   cohort, and it drifts upward within cohorts across censuses (§3a).
3. US instruments disagree by up to 0.06 for the same cohort (CPS 0.494, census 0.530, ACS 0.554
   for 1990–94), and the ACS shifted in 2020 (§3b). No instrument here is validated against
   Mexican records.
4. The undercount test proxies "likely unauthorized" with non-citizens, and the diploma share φ is
   unknown; both are priced, not estimated.
5. First observation is at 6–10 years for the 1980–84 and 1990–94 cohorts; departures before the
   first observation are unmeasured except by the CPS check.
6. Attainment is measured after arrival, so it includes schooling obtained in the US.
7. Schooling position is one observable. It does not measure unobserved ability (Fernández-Huertas
   Moraga's second explanation) or propensity to offend (Butcher and Piehl's dimension).
8. The main table's sampling error (SE ≤ 0.010) is small next to the specification spread
   (0.44–0.62); the specification spread is the real uncertainty.

## 8. What did not complete

- IPUMS International microdata for Mexico: refused, account not registered. Registering the
  account would allow single-year birth cohorts, 1990 and 1995 references, and origin by state or
  place size (Rendall and Parker's mechanism).
- A 1990 INEGI national education-by-age table: not found.
- The 2015 Intercensal: fetched, not used (no grade detail by age).
- Why the ACS 2020 break and the census/ACS gap occur: measured, not explained.

## 9. Reproduce

From the repository root. The IPUMS key is read from
`infra/immigration-fiscal/acquire/config.local.env` and never printed.

```sh
L=infra/immigration-fiscal/schooling_selection_position_2026_09_23
# IPUMS USA extracts (a new submission gets a new number; _cache/extracts.json records it)
uv run --no-project python3 $L/extracts.py submit --only usa          # #3
uv run --no-project python3 $L/extracts.py submit --only usa_acs0004  # #12
uv run --no-project python3 $L/extracts.py submit --only usa_qeduc    # #13
uv run --no-project python3 $L/extracts.py wait --max-minutes 45
uv run --no-project python3 $L/parallel_fetch.py usa 3 us_mexborn 10            # checks IPUMS sha256
uv run --no-project python3 $L/parallel_fetch.py usa 12 us_mexborn_acs0004 10
uv run --no-project python3 $L/parallel_fetch.py usa 13 us_mexborn_qeduc 10
# INEGI fetch, origin tables, main analysis and every check (needs poppler's pdftotext)
sh $L/reproduce.sh
```

`reproduce.sh` runs `fetch_inegi.py`, `origin_inegi.py`, `position.py`, `cps_check.py`,
`acs_pums_check.py` and `instrument_checks.py` in order. On 2026-09-23 `derived/` was emptied and
rebuilt three times with `reproduce.sh`. The last two rebuilds, both made with the final scripts,
agree byte for byte on all 11 tables; the first agrees with them on every row it has (the
combined undercount rows and the ACS-break table were added after it) [DATA: comparison by
`cmp`; rebuild logs in the session scratchpad].

## Files

- Scripts: `fetch_inegi.py`, `origin_inegi.py`, `levels.py`, `position.py`, `cps_check.py`,
  `acs_pums_check.py`, `instrument_checks.py`, `extracts.py`, `ipums_api.py`,
  `parallel_fetch.py`, `reproduce.sh`.
- Outputs (aggregates only): `derived/origin_levels.csv`, `origin_five.csv`,
  `origin_anchors.csv`, `position_main.csv`, `position_all_specs.csv`, `survivor_drift.csv`,
  `undercount_sensitivity.csv`, `instrument_checks.csv`, `acs_break_2020.csv`,
  `cps_check_1990_94.csv`, `acs_pums_check.csv`.
- Pins: `sources.json` (INEGI), `_cache/*.manifest.json` (IPUMS). Microdata stay in the
  git-ignored `_cache/`.

This analysis was produced through an LLM, whose post-training leans on politically charged
questions like this one (`notes/llm-bias-caveat.md`); the numbers above are reproducible from the
scripts regardless of framing, but the choice of which variants to run and how to word the verdict
is [FRAMING-SENSITIVE].

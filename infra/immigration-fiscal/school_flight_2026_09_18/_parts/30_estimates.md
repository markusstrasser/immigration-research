---

## 3. Estimates

Coefficients with standard errors in parentheses. `*` p<0.10, `**` p<0.05, `***` p<0.01. Metro regressions are weighted by the base-year enrolment of the group in the outcome and use HC1 or metro-clustered standard errors; district regressions are weighted by enrolment and clustered on the district.

### 3.1 Metro panel: does the native private share rise with the Hispanic share?

Long differences are over 2008-2023. A coefficient of 0.10 means that a 10-point rise in the Hispanic share of enrolled children raises the private share of US-born non-Hispanic white children by 1 point.

**Long difference 2008-2023, outcome = change in private share of US-born non-Hispanic white children**

| level | d hisp_share | d fb_share |
|---|---|---|
| elem | +0.154 (0.095) | -0.284 (0.195) |
| sec | +0.078 (0.073) | -0.145 (0.114) |
| all | +0.137 (0.083) | -0.305** (0.152) |

**Horse race: is the response specific to the Hispanic share? (all three entered together)**

| level | d hisp_share | d asian_share | d black_share |
|---|---|---|---|
| elem | +0.119 (0.099) | -0.323 (0.237) | -0.057 (0.148) |
| sec | +0.079 (0.074) | -0.124 (0.183) | +0.047 (0.092) |
| all | +0.112 (0.084) | -0.424* (0.231) | +0.009 (0.131) |

**Generation split: first-generation (largely English-learner) vs second-generation Hispanic children**

| level | d hisp foreign-born share | d hisp US-born share |
|---|---|---|
| elem | -0.129 (0.245) | +0.208** (0.094) |
| sec | -0.095 (0.151) | +0.093 (0.073) |
| all | -0.145 (0.194) | +0.196** (0.086) |

**Is the response white-specific?**

| level | all US-born non-Hispanic | US-born Hispanic |
|---|---|---|
| elem | +0.107 (0.086) | +0.007 (0.105) |
| sec | +0.055 (0.066) | -0.016 (0.058) |
| all | +0.096 (0.082) | +0.001 (0.083) |

**Two-way fixed effects (metro and year), levels not differences**

| level | hisp_share | fb_share |
|---|---|---|
| elem | +0.107 (0.080) | -0.224 (0.137) |
| sec | +0.042 (0.058) | -0.066 (0.083) |
| all | +0.114 (0.072) | -0.213** (0.107) |

**2SLS on the 2000-base shift-share instrument**

| level | instrument | coefficient (SE) | first-stage F | n |
|---|---|---|---|---|
| elem | 2SLS (z_fb) | -0.202 (0.788) | 32.9 | 333 |
| elem | 2SLS (z_mex) | +0.303 (0.678) | 12.5 | 333 |
| elem | 2SLS (z_fb) | +0.700 (1.545) | 5.3 | 327 |
| elem | 2SLS (z_mex) | -0.081 (0.433) | 22.7 | 327 |
| sec | 2SLS (z_fb) | +0.062 (2.339) | 0.4 | 329 |
| sec | 2SLS (z_mex) | -0.111 (0.237) | 52.4 | 329 |
| sec | 2SLS (z_fb) | -0.682 (0.659) | 3.0 | 322 |
| sec | 2SLS (z_mex) | -0.096 (0.196) | 117.8 | 322 |
| all | 2SLS (z_fb) | -0.282 (1.240) | 4.2 | 333 |
| all | 2SLS (z_mex) | +0.046 (0.389) | 33.5 | 333 |
| all | 2SLS (z_fb) | +5.625 (13.470) | 0.2 | 330 |
| all | 2SLS (z_mex) | -0.108 (0.285) | 68.8 | 330 |

The instrument's first-stage strength is reported so that weak-instrument estimates can be discounted rather than quoted.

**Reverse-timing placebo.** The early change in the private share is regressed on the *later* change in the Hispanic share. A non-zero coefficient means the association is a pre-trend, not a response.

| level | coefficient (SE) | n |
|---|---|---|
| elem | +0.018 (0.058) | 331 |
| sec | +0.065 (0.056) | 323 |

**Influence checks, secondary level**

| sample | coefficient on Δ Hispanic share (SE) | n |
|---|---|---|
| drop 5 largest metros | +0.080 (0.076) | 324 |
| drop California | +0.065 (0.080) | 303 |

**Counts, the specification comparable to Betts & Fairlie's ratio.** Both sides are expressed per 100 children enrolled in the base year, so the coefficient is the number of US-born non-Hispanic white children moved into private school per additional child in the public schools. The second row of each pair adds the metro's total enrolment growth as a control, because a growing metro adds Hispanic public pupils and white private pupils at the same time.

| level | control | per Hispanic child added | per foreign-born child added | n |
|---|---|---|---|---|
| elem | none | +0.101*** (0.027) | -0.075 (0.099) | 333 |
| elem | + total enrolment growth | -0.127*** (0.041) | -0.355*** (0.095) | 333 |
| sec | none | +0.103*** (0.016) | +0.091 (0.073) | 329 |
| sec | + total enrolment growth | -0.117*** (0.031) | -0.054 (0.056) | 329 |
| all | none | +0.113*** (0.020) | -0.007 (0.094) | 333 |
| all | + total enrolment growth | -0.135*** (0.039) | -0.270*** (0.076) | 333 |

### 3.2 District finance: does spending or local tax effort fall?

Outcomes are per pupil in 2020 dollars unless the name says otherwise. A coefficient of 1,000 on `hisp_share` means that moving a district from 0% to 100% Hispanic raises the outcome by $1,000 per pupil, so a 10-point rise is worth $100.

**A district+year FE, treatment = Hispanic share of enrolment**

| outcome | coefficient (SE) | n |
|---|---|---|
| pp_current | -2277.261*** (698.598) | 38,084 |
| pp_instruction | -1074.655*** (378.069) | 38,084 |
| pp_rev_local | -4660.072*** (664.794) | 38,084 |
| pp_rev_proptax | -3088.217*** (598.453) | 34,745 |
| pp_rev_state | +1344.571* (735.512) | 38,084 |
| pp_rev_total | -3024.046*** (1070.020) | 38,084 |
| local_effort | -0.087*** (0.024) | 24,856 |
| proptax_effort | -0.069*** (0.023) | 22,854 |

**B district+state-year FE, treatment = Hispanic share of enrolment**

| outcome | coefficient (SE) | n |
|---|---|---|
| pp_current | -1108.646* (635.773) | 38,084 |
| pp_instruction | -597.373* (308.811) | 38,084 |
| pp_rev_local | -4471.702*** (686.571) | 38,084 |
| pp_rev_proptax | -3692.699*** (664.467) | 34,745 |
| pp_rev_state | +2808.533*** (704.226) | 38,084 |
| pp_rev_total | -1062.852 (1093.177) | 38,084 |
| local_effort | -0.072*** (0.020) | 24,856 |
| proptax_effort | -0.065*** (0.018) | 22,854 |

**Poterba-style: county elderly share (centred on its mean) and its interaction with the Hispanic share, district and state-year fixed effects. The Hispanic-share coefficient is therefore the effect at the average elderly share.**

| outcome | hisp_share | share65_c | hisp_x_65 |
|---|---|---|---|
| pp_current | -989.618 (643.896) | +4916.913*** (1767.611) | +5954.359 (6621.924) |
| pp_rev_local | -4418.892*** (707.114) | +2027.194 (3517.690) | -2370.337 (7280.544) |
| pp_rev_proptax | -3644.610*** (687.898) | +2260.363 (2924.931) | +566.064 (6876.561) |

**Ethnic fractionalisation index instead of the Hispanic share**

| outcome | elf |
|---|---|
| pp_current | -473.986* (265.363) |
| pp_rev_local | +1155.358** (474.800) |

**Long difference: 2000-2019, state FE**

| outcome | d_hisp_share |
|---|---|
| d_pp_current | -1565.754*** (590.534) |
| d_pp_instruction | -752.825*** (264.732) |
| d_pp_rev_local | -4954.862*** (860.607) |
| d_pp_rev_proptax | -3768.508*** (685.844) |
| d_pp_rev_state | +2811.946*** (643.806) |
| d_pp_rev_total | -1783.519 (1159.842) |

**Long difference: 2000-2010, state FE**

| outcome | d_hisp_early |
|---|---|
| d_pp_current | -89.930 (677.637) |
| d_pp_instruction | — |
| d_pp_rev_local | -3336.251*** (579.420) |
| d_pp_rev_proptax | -2827.744*** (480.504) |
| d_pp_rev_state | — |
| d_pp_rev_total | — |

**Reverse-timing placebo. The EARLY change in the outcome is regressed on the LATER change in the Hispanic share; a non-zero coefficient means the association is a pre-trend, not a response. (d outcome 2000-2010 on d hisp 2010-2019, state FE)**

| outcome | d_hisp_late |
|---|---|
| d_pp_current | -29.559 (853.961) |
| d_pp_rev_local | -1254.350 (769.052) |
| d_pp_rev_proptax | -122.334 (623.347) |

### 3.3 California school bond and parcel-tax measures

| specification | treatment | coefficient (SE) | n |
|---|---|---|---|
| pct: yes vote share, year+threshold FE | hisp_share | +0.042** (0.019) | 2,954 |
| pct: yes vote share, year+threshold FE | elf | +0.007 (0.037) | 2,954 |
| pct: yes vote share, + elderly share | hisp_share | +0.040** (0.019) | 2,954 |
| pct: yes vote share, + elderly share | share65 | -0.078 (0.221) | 2,954 |
| passed: passed (LPM), year+threshold FE | hisp_share | +0.088 (0.058) | 2,954 |
| passed: passed (LPM), year+threshold FE | elf | -0.012 (0.082) | 2,954 |
| passed: passed (LPM), + elderly share | hisp_share | +0.083 (0.059) | 2,954 |
| passed: passed (LPM), + elderly share | share65 | -0.174 (0.650) | 2,954 |

### 3.4 Size: what the coefficient implies in head counts and dollars

Mechanical projection of the long-difference coefficient onto the observed Hispanic-share change. These are **not** measured head counts, and the 95% interval is carried through so the width is visible.

| level | region | Δ Hispanic share | natives moved (point) | 95% interval | tuition, $m | state aid shifted, $m |
|---|---|---|---|---|---|---|
| elem | national (panel metros) | +0.045 | 79,811 | -17,361 to 176,984 | 735 | 765 |
| elem | California | +0.019 | 2,194 | -477 to 4,866 | 20 | 21 |
| elem | Texas | +0.014 | 1,808 | -393 to 4,009 | 17 | 17 |
| sec | national (panel metros) | +0.079 | 48,612 | -41,172 to 138,396 | 750 | 466 |
| sec | California | +0.066 | 2,694 | -2,282 to 7,670 | 42 | 26 |
| sec | Texas | +0.070 | 2,967 | -2,513 to 8,448 | 46 | 28 |
| all | national (panel metros) | +0.059 | 156,139 | -30,123 to 342,401 | 1,997 | 1,497 |
| all | California | +0.038 | 6,705 | -1,294 to 14,703 | 86 | 64 |
| all | Texas | +0.036 | 6,684 | -1,289 to 14,656 | 85 | 64 |


claude-opus-5[1m]

## Audit correction — September 19, 2026

**Private-school welfare cost remains unpriced.** The later DC voucher trial is not the only randomized US evidence, and a test-score null does not show tuition buys no benefits. The earlier federal DC evaluation found a graduation benefit; the later evaluation also found attendance, perceived-safety and satisfaction benefits. Neither identifies immigration-induced switching or its net welfare value. Preserve the observed revenue associations and test-score findings; withdraw the claim that these experiments settle the defensive-expenditure classification. A weak or invalid migration instrument also does not establish a null, and a nonzero national scalar cannot mechanically weaken a single-window IV. [SOURCE: official IES evaluation records and independent IV probe in the mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


**Verdict:** NOT REPRODUCED in modern US data. Betts & Fairlie's one-native-per-four-immigrants
holds up as a citation — the phrase is verbatim in their abstract, for secondary school, from
1980–1990 Census data — but nothing like it survives in 2008–2023 metro data. The raw count
specification gives about **one US-born non-Hispanic white child into private school per ten
Hispanic children added to the public schools**, and that estimate **reverses to −0.12 to −0.14
once the metro's total enrolment growth is controlled**: it was measuring population growth, not
substitution. The share specification is **not significant at any level** on the full 334-metro
panel (+0.154, SE 0.095 elementary; +0.078, SE 0.073 secondary), the **foreign-born** share
carries a *negative* coefficient, and the part of the Hispanic share that predicts anything is the
**US-born second generation**, not immigrant arrival — the opposite of Betts & Fairlie's
non-English-speaking mechanism. Nationally the private share *fell* from 11.7% to 10.0% while the
Hispanic share of public enrolment rose from 16.4% to 28.9%.

The public-goods response is real but confined to one margin. Within a state and year, a district
whose Hispanic share rises loses **$447 of local revenue per pupil per 10 points** (SE $69) and
**$369 of property-tax revenue**, with local tax effort down 6.5% of its mean; **state aid offsets
about 60%**, and total revenue and per-pupil spending are statistically unchanged. Poterba's
elderly-share direction does not appear at all, the fractionalisation index gives the opposite sign
to the Hispanic share on local revenue, and in 2,954 California school tax measures higher-Hispanic
districts vote *more* for bonds, not less.

On the accounting: a switch raises measured GDP in the short run by roughly the tuition, and
**lowers** it in the long run, because average private tuition ($12,790 in 2021-22) is about
three-quarters of average public current spending per pupil ($17,846 in FY2024). The tuition is a
real resource cost borne by the family; the lost state aid is a transfer between districts; local
property tax does not move; the only fresh real costs are duplicated capacity and — if the child's
outcomes do not improve — the defensive-expenditure deadweight. In the one clean US randomised
evaluation, switching produced two years of significantly *worse* maths and no reading gain.

Scaled honestly, the point estimates imply about **156,000** white native children moved into
private school across 334 metros over 2008–2023, some $2.0bn of tuition and $1.5bn of state aid
reallocated — but the underlying coefficient is insignificant, so the interval spans zero, and the
same period saw national private enrolment fall by about 450,000 for unrelated reasons.

# School flight, the public-goods response, and what a private-school switch does to the accounts

Lane `infra/immigration-fiscal/school_flight_2026_09_18/`. Agent dispatched 2026-09-18.
Provenance tags: [SOURCE: …] [DATA] [INFERENCE] [TRAINING-DATA] [UNVERIFIED] [GAP]
[FRAMING-SENSITIVE].

Three linked questions the repo has not measured:
1. Does the native private-school share rise when the Hispanic / foreign-born share of
   schoolchildren rises?
2. Does per-pupil spending, local tax effort, or bond support fall as districts become
   more ethnically heterogeneous?
3. When a native family moves a child to private school, what is a real resource cost,
   what is a transfer, and does the tuition buy a measurable outcome gain?

**Data quality note.** Two defects were found and fixed during the build, both recorded
because they changed results. The Census PUMS endpoint returned records outside the
requested age range for California 2010, inflating that state-year 13-fold; every
state-year is now audited against its own cross-year median (`audit_kids.py`,
`derived/kids_audit.csv`, 257 state-years, all inside ±25% after the fix). And the metro
panel initially grouped on state as well as metro, splitting every multi-state metro and
dropping it from the balanced panel; §5.7 reports how much that changed the estimate.

---

## 1. The literatures, verified where verification was possible

Full verification with page-level quotes: `infra/immigration-fiscal/school_flight_2026_09_18/LIT.md`.

### 1.1 Betts & Fairlie 2003 — the "one per four" figure is exactly the paper's own

[SOURCE: Betts & Fairlie, "Does immigration induce native flight from public schools into
private schools?", Journal of Public Economics 87 (2003) 987–1012, DOI
10.1016/S0047-2727(01)00164-5; PDF at
http://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf]

The abstract says it verbatim: "For every four immigrants who arrive in public high
schools, it is estimated that one native student switches to a private school." The
repo's paraphrase is accurate. Four qualifications change how much weight it carries.

**It is secondary school only.** At primary level the estimated coefficients are
*negative and insignificant* (GLS −0.794, SE 0.838). The authors: "there is no evidence
of a statistically significant link between immigration inflows and changes in native
parents' decisions about whether to send their children to private schools at the primary
level" (p. 1003). Roughly four-fifths of K-12 enrolment is below grade 9, so the channel
is switched off for most of the school system.

**The design is a two-period first-differenced metro panel, not an IV.** 1980 and 1990
Census microdata, 132 metropolitan areas, Borjas–Sueyoshi two-stage probit. The IV
robustness check gives 3.90 (SE 2.31), and the authors themselves write "The IV model is
thus not at all conclusive" (p. 1002).

**It is about non-English-speaking immigrants, and white natives.** The coefficient on the
non-English-speaking immigrant share is significant and the English-speaking one is not;
flight is "almost purely from non-English-speaking immigrants" (pp. 1003–1005). Table 5:
"the addition of one immigrant to the public school system leads 0.28 white natives to
switch from public to private schools" (p. 1006).

**The aggregate implication is small — and the authors say so.** Their own simulation:
across the 132 metros the private secondary rate would have risen from 10.29% to 10.64%
over 1980–1990, "an increase of 0.34 percentage points or 3.3%," with an arc elasticity of
0.143, and "Clearly, at the national level trends in the immigrant share are unlikely to
have led to major swings in the enrolment shares of public high schools" (p. 1008). The
metro-level predictions are where the action is: +1.34 pp in Los Angeles, +1.42 pp in San
Francisco, +2.51 pp in Miami.

One design limitation the authors flag: the native Black share is a comparison regressor
with almost no variation over 1980–1990 (+0.5 pp), so its small insignificant coefficient
is not evidence that Black composition fails to drive flight (fn. 26, p. 1002). The older
desegregation literature is the place to look for that; see §5.

### 1.2 Poterba 1997 — the elderly result holds, the racial-difference result does not

[SOURCE: Poterba, "Demographic structure and the political economy of public education,"
JPAM 16(1) 1997, 48–66; working-paper version NBER WP 5677, July 1996, read in full at
https://www.nber.org/system/files/working_papers/w5677/w5677.pdf, cached at
`_cache/poterba_w5677.pdf`. [UNVERIFIED] whether the published JPAM tables differ from the
WP tables — the numbers below are the WP's.]

Design: 48 continental states, four years only (1961, 1971, 1981, 1991), log real per-child
K-12 spending. The elderly-share result is solid: coefficient −0.276 (SE 0.121) with state
and time effects, an elasticity of about −0.25; a one-standard-deviation rise in the
elderly share (0.108 → 0.130) cuts per-pupil spending by about 5% (p. 16). It weakens and
loses significance once urban share is controlled (−0.155, SE 0.125). The school-age share
elasticity is about −1.0: a bigger child cohort does not get proportionately more money.

The racial result is weaker than its reputation. The variable is the *level* difference
(nonwhite share of ages 5–17) minus (nonwhite share of 65+), entered additively — **there
is no elderly × race interaction term in the paper**. With state and time effects the
coefficient is −0.621 (SE 0.394), which Poterba describes as "not statistically
significant at standard confidence levels" (p. 21); a one-point rise in the nonwhite share
of children cuts log per-child spending by about 0.6%. The standard deviation of the
variable is only 0.047, so identifying variation is thin. The abstract's claim that the
elderly effect is "particularly large when the elderly residents and the school-age
population are from different racial groups" rests on that insignificant additive
coefficient plus the contrast with Table 6, where the same variable predicts *higher*
non-education spending, significantly. **A memo should cite the −0.25 elderly elasticity
and must not present the racial-difference result as an estimated interaction.**


### 1.3 Alesina, Baqir & Easterly 1999 — [GAP], not verified from the paper

The brief asked for the magnitude by which shares of spending on productive public goods
fall as ethnic fragmentation rises in US cities and counties, with the fractionalisation
measure used and the authors' own caveats. **The literature agent was cut off by a rate
limit before retrieving the paper, so no figure from it is reported here.**
[UNVERIFIED — the specific unverified claim is: "shares of US city and county spending on
education, roads, sewers and trash removal fall as ethnic fractionalisation rises, by a
magnitude the paper reports." Nothing in this memo depends on it.] The one thing this memo
can say about that literature is the identification objection in §5.2, which is verified.

### 1.4 Hopkins 2009, "The diversity discount" — [GAP], not verified from the paper

Same cause. [UNVERIFIED — the unverified claim is: "increasing ethnic and racial diversity
prevents local tax increases, by a magnitude and in a locality panel the paper reports."]
The California ballot-measure result in §3.3 is this memo's own test of the same
proposition, and it comes out with the opposite sign.

Two further items in the brief were left unverified for the same reason and are recorded
here rather than quietly dropped: the Louisiana Scholarship Program results, and Altonji,
Elder & Taber (2005) on selection in Catholic-school effect estimates. The switcher-outcome
conclusion in §5.4 therefore rests on the DC Opportunity Scholarship Program evaluations
alone, which is one randomised programme in one city, not the whole voucher literature.


---

## 2. Data and designs

Everything below is built in `infra/immigration-fiscal/school_flight_2026_09_18/`; scripts
are listed in the RESULT file with runnable commands.

**(a) Metro panel of child school type.** ACS 1-year PUMS, children aged 5–17, one cell
per PUMA × race/ethnicity × nativity × school level, for 2005, 2008, 2010, 2015 and 2023
(`pull_kids.py`). The 2013 and 2018 waves were dropped mid-run for throughput; the
remaining five span the whole window and every long difference used below ends on one of
them. PUMA counts are allocated to counties by the MCDC Geocorr
population allocation factor for the PUMA vintage in force that year and summed into the
fixed OMB February-2013 metropolitan delineation — the same geography construction as
`employment_entry_2026_09_18/build_panel.py`, whose crosswalk files are reused
(`build_metro.py`). The outcome is the private share among US-born non-Hispanic white
children, private / (private + public).

The treatment is the Hispanic (or foreign-born) share of **all enrolled children**, public
and private together, not of public enrolment. This matters. If white families leave the
public schools, the Hispanic share *of public enrolment* rises mechanically, so regressing
the white private share on it builds in a positive coefficient by construction. Betts &
Fairlie use the immigrant share of the public-school population and handle this through
their first-differenced structure; the all-enrolled denominator used here removes the
mechanical channel directly, at the cost of not being the identical object.

Two measurement caveats, both material:

- ACS `SCH` = 3 is "private school, private college, **or home school**." The private
  share therefore includes home-schooled children and rises mechanically with the growth
  of home schooling, which accelerated sharply after 2020. Comparisons that straddle 2020
  are contaminated by this and are labelled where they appear.
- Nativity is the *child's*, not the parents'. "US-born non-Hispanic white" is a proxy for
  Betts & Fairlie's "native"; it is close, because almost all non-Hispanic white children
  are US-born, but it is not identical to their definition.

**(b) District finance panel.** NCES Common Core of Data district membership by race,
the CCD directory (county, CBSA, English-learner counts), and the Census F-33 district
finance file, for 2000, 2005, 2010 and 2019, pulled district-by-state-by-year from the
Urban Institute Education Data Portal (`pull_districts.py`, `build_districts.py`). The
last wave is 2019 rather than 2020 because Urban's CCD enrolment year 2020 is the autumn
of 2020, when enrolment fell sharply for pandemic reasons unrelated to anything here.
Per-pupil denominators use the F-33's own membership count for the finance year, not the
CCD count, because the two are offset by a school year; CCD counts are used only for the
race shares, where the offset is immaterial.
The F-33 is the same source the repo reads locally for FY2024 in
`ledger_absolute_2026_09_17/district_differential.py`; Urban is used only because the
panel needs 2000–2020 and only the FY2024 file is staged locally. Urban's F-33
redistribution stops at 2020 — 2021 and later return zero rows, checked 2026-09-18, so
the panel cannot be carried to the FY2024 file the repo holds locally.
Money is deflated to 2020 dollars with the FRED CPI-U annual average. Screens: regular
operating districts, non-charter, at least 100 pupils, per-pupil current spending inside
$3,000–$80,000, the same plausibility band the repo's FY2024 loader uses. County elderly
share and median household income come from Census 2000 SF1 and the ACS 5-year
(`pull_county_controls.py`) for the Poterba-style control.

**(c) California ballot measures.** Every school-district bond and parcel-tax measure in
the California Elections Data Archive, the Secretary of State / CSU Sacramento joint
archive, taken from the `justindbk/ceda` mirror of the CSUS portal (`ceda_bonds.py`).
The outcome is the yes vote share, which is threshold-independent, plus a pass indicator
with the required-majority category as a control — Proposition 39 (November 2000) cut the
school-bond threshold from two-thirds to 55%, so a raw pass rate is not comparable across
that date. Districts are matched from the ballot-measure place name to the CCD district
name; the match rate is reported and unmatched measures are listed.

**What the repo already had.** `school_angle_2026_09_16` found no measured cost to
incumbent students from immigrant or English-learner concentration in US data, and priced
the classroom channel at $0 per pupil-year. `ledger_absolute_2026_09_17` found that
Hispanic pupils attend districts spending **$474 per pupil above** their state's mean
while white pupils attend districts **$624 below** it. That cross-sectional fact is the
first warning against expecting spending to fall with the Hispanic share: in levels, it
is higher.


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


---

## 4. What a private-school switch does to GDP, to wealth, and to the public accounts

This is the operator's question, and the accounting has to be kept separate from the
welfare reading. Four distinct things happen when a native family moves one child from a
public school to a private one.

### 4.1 Measured GDP: it rises, but by less than the tuition

BEA measures general government output at the cost of its inputs, because that output is
not sold. The NIPA handbook is explicit and uses schools as its example: "The value of the
services that are provided by government free of charge, whether to individual members of
society (such as education at public elementary schools) or to society as a whole (such as
national defense or law enforcement), is included in government consumption expenditures."
Government consumption expenditures are "Valued as gross output, based on costs of inputs,
of federal and of state and local general government less sales to other sectors and
own-account investment" [SOURCE: BEA, NIPA Handbook, Chapter 9, "Government Consumption
Expenditures and Gross Investment," pp. 9-3 to 9-7; cached at `_cache/bea_nipa_ch09.pdf`].
Private school tuition paid by households is personal consumption expenditure.

So the switch moves the child's education from the government-consumption line of GDP to
the PCE line. The net change in measured GDP is

    ΔGDP  =  (cost of producing the private school place)  −  (reduction in the district's
             cost of producing the public place)

and **not** the tuition. Two cases:

- **Short run, enrolment-lagged funding, fixed staffing.** The district does not shed a
  teacher when one child leaves. Its input costs are unchanged, so government consumption
  is unchanged and PCE rises by the tuition. Measured GDP rises by roughly the full
  tuition. This is the case the operator described, and it is right for a single family in
  a single year.
- **Long run, enrolment adjusts.** The district eventually sheds marginal cost, and the
  comparison of unit costs then decides the sign. Average private tuition was **$12,790**
  in 2021-22, about $13,700 in 2024 dollars; average public current spending per pupil in
  FY2024 was **$17,846** [SOURCE: NCES Digest 2023 table 205.50; Census F-33 FY2024
  district file `elsec24t.txt`, 13,252 districts and 46.37m pupils, computed in
  `derived/f33_fy2024_per_pupil.csv`]. Private production of a school place costs roughly
  three-quarters of what the public place it replaces costs. **In the long run a switch
  therefore lowers measured GDP**, by something of the order of $4,000 per pupil-year.
  This is the opposite of the short-run direction, and both are accounting artefacts of
  valuing government output at input cost rather than statements about welfare.

A caution on the private side. Most US private K-12 schools are nonprofit, and NIPA
measures nonprofit output at cost too, with tuition recorded as the household's purchase
of that output. Sticker tuition also understates the resource cost where schools are
subsidised by donations or by a religious order's below-market labour, and overstates it
where tuition covers capital or endowment building. Treat the tuition figure as an
approximation to the private production cost, not an identity. [INFERENCE]

### 4.2 The family's position: this is a real resource cost, and it may buy nothing measurable

The tuition is not a transfer to another household. It purchases teaching services that are
really produced, so real resources are consumed. The household's consumption of everything
else, or its saving, falls by that amount.

Whether that consumption is *welfare-improving* depends on what the switch buys. If the
family would have received an equivalent education free, the tuition is a **defensive
expenditure**: it purchases relative position — peer composition, perceived safety, class
size — rather than additional real output. Defensive expenditure adds to GDP and subtracts
from welfare, the same way spending on locks does. This is the single most
[FRAMING-SENSITIVE] judgement in the memo, and it is empirically testable: the test is
whether switchers' measured outcomes improve.

The switcher-outcome evidence is summarised in §5.4. The short version is that the
credible experimental estimates of moving a child from a public school to a private one
with a voucher cluster near zero and include large negative results, which makes the
defensive-expenditure reading the better-supported one for the average switcher. It does
not follow that no family gains; it follows that the average measured academic gain is not
what the tuition is buying.

### 4.3 The public school's revenue: mostly a transfer, with a real diseconomy attached

Three components move in different directions.

| Component | What happens when one native child leaves | Resource cost or transfer |
|---|---|---|
| State formula aid | Falls, roughly by the state's marginal per-pupil aid rate; average state revenue was $9,589 per pupil in FY2024 | **Transfer** — the money is reallocated to other districts or other state uses |
| Local property tax revenue | Unchanged — the family still lives there and still pays; $5,815 per pupil in FY2024 | **Neither** — no flow changes |
| Federal categorical aid | Largely unchanged, since it tracks poverty and EL counts, not the departing child | **Neither** |
| Marginal instructional cost | Falls, but by less than average cost in the short run | **Real**, but a saving, not a cost |
| Fixed cost per remaining pupil | Rises: the same building, administration and transport over fewer pupils | **Real diseconomy** |

The headline consequence is not a district revenue collapse. Losing a pupil while keeping
the property tax base can *raise* revenue per remaining pupil, because the local share is
now divided among fewer children. The genuine resource cost is the duplication: an empty
seat in the public school plus a newly-built seat in the private one, plus the second
transport system. The genuine transfer is the state-aid reallocation, which is a
distributional question between districts, not a cost to the economy.

### 4.4 The median voter: the effect that is neither a cost nor a transfer

The family that leaves also leaves the public school's political constituency. It keeps
paying school taxes but no longer consumes the service, which moves its preferred level of
school spending down. If the departing families are disproportionately those with the
highest willingness to pay for school quality — and Betts & Fairlie's finding that flight
is concentrated among white natives at secondary level implies they are — then flight
shifts the median voter in local school elections.

This is the mechanism that links §4 back to §1.2 and to the fragmentation literature. It
is not an accounting entry. It shows up later, as lower bond passage rates, lower parcel
taxes, and lower local revenue per pupil, and that is exactly what design (b) and the
California bond analysis test directly.

### 4.5 Summary of the accounting

| Item | Direction | Classification |
|---|---|---|
| Private tuition paid | + to PCE | Real resource use; **defensive expenditure** to the extent outcomes do not improve |
| Public school input costs | Unchanged short run, − long run | Real |
| Measured GDP | + in the short run, ambiguous in the long run | Accounting artefact of valuing government output at cost |
| Household net worth / other consumption | − by the tuition | Real, borne by the family |
| State enrolment-linked aid to the district | − | **Transfer** between districts |
| Local property-tax revenue | Unchanged | Neither |
| Fixed cost per remaining pupil | + | Real diseconomy |
| Median voter for school taxes | Shifts against spending | Political-economy effect, measured in §3 |


---

## 5. Disconfirmation

The brief required four checks to be run before reading the results, plus the standard
adversarial search. They are reported here whether or not they favour the hypothesis.

### 5.1 The national aggregate goes the wrong way

This is the largest single piece of evidence against a strong flight story, and it needs
no model. Over the period in which the Hispanic share of US public-school enrolment rose
from **16.4% (2000) to 28.9% (2022)**, the private share of total K-12 enrolment **fell**
from 11.7% (2001) to 10.0% (2021). Private enrolment fell in absolute terms, from 5.92m
(1995) to 5.47m (2021). [SOURCE: NCES Digest of Education Statistics 2023, tables 203.50
and 205.10; figures transcribed to `derived/nces_national_context.csv`]

The regional pattern is the same shape. The West absorbed the largest Hispanic increase
(32.2% → 44.2% of public enrolment, 2000 to 2022) and has the country's **lowest** private
share, which also fell, from 10.0% (1995) to 8.3% (2021). The South went from 14.5% to
29.0% Hispanic and its private share went from about 9.8% to 9.5%.

This does not refute a within-metro effect — the national series is dominated by the
collapse of Catholic-school enrolment, by tuition rising far faster than prices (average
private tuition roughly tripled in nominal terms between 1999-2000 and 2021-22, from
$4,570 to $12,790), and by the growth of charter schools, which absorb exit from a public
district without appearing as private enrolment. But it does bound the aggregate
magnitude hard, and it is consistent with Betts & Fairlie's own aggregate simulation, in
which the national private secondary share rises by only 0.34 points over a decade.

**Charter schools are the largest unmeasured competing exit route.** A native family
leaving a diversifying district for a charter school shows up in this memo's data as a
*public*-school pupil, because ACS `SCH` = 2 covers public charters. Any flight estimate
here is therefore a lower bound on total exit, and the share of exit routed through
charters grew enormously over the window. [INFERENCE]


### 5.2 The fragmentation-and-public-goods link is contested on identification, not on data

The strongest published attack is not a failed replication but a collinearity argument.
Kustov & Pardelli [SOURCE: "Ethnoracial Homogeneity and Public Outcomes: The (Non)effects
of Diversity," *American Political Science Review* 112(4) 2018, 1096–1103, DOI
10.1017/S0003055418000308] argue that "it is often impossible to identify the effects of
diversity due to its collinearity with the share of disadvantaged groups." In US data,
high ethnic fractionalisation and high minority share are nearly the same variable, so
"diversity reduces public goods" and "minority share reduces public goods" cannot be
separated. They break the collinearity using Brazilian municipalities and find that "more
homogeneous Afro-descendant communities have lower provision" — the sign flips to
homogeneity of the disadvantaged, not diversity. Their conclusion is that the result
"cast[s] doubt on the reliability of previous findings related to the benefits of local
ethnoracial homogeneity for public outcomes."

This bears directly on the design in §3.2. A negative coefficient on the Hispanic share or
on a fractionalisation index in US district data is exactly the object Kustov & Pardelli
say is not identified. It is reported below as an association, not as a diversity effect.

### 5.3 Putnam's diversity-and-trust finding does not survive re-analysis of his own data

Abascal & Baldassarri [SOURCE: "Love Thy Neighbor? Ethnoracial Diversity and Trust
Reexamined," *American Journal of Sociology* 121(3) 2015, 722–782, DOI 10.1086/683144]
re-run Putnam's 2000 Social Capital Community Benchmark Survey analysis on 29,733
respondents. Their result: "the association between diversity and self-reported trust is a
compositional artifact attributable to residential sorting: nonwhites report lower trust
and are overrepresented in heterogeneous communities." In the replication, "the HHI does
not significantly predict any of the five indicators of social capital" in the national
sample, and fails in four of five in the full sample. They also note that Putnam reported
only the one model of five that survives.

The residual finding is the one that matters here: "Only for whites does living among
out-group members — not in diverse communities per se — negatively predict trust." That
locates the mechanism in the majority group's response to out-group share, which is
consistent with a native-flight story but is not the same claim as "diversity erodes
community."

**Steel-man of the other side.** Abascal & Baldassarri condition on individual race,
citizenship, tract white share and tract citizen share. A defender of Putnam can reply
that this over-controls: if the mechanism by which diversity acts *is* composition, then
conditioning on the treatment's own components and calling the residual a null is not a
refutation. That is a live specification dispute, not a settled kill.

### 5.4 Does the tuition buy a better outcome? The cleanest US experiment says no

This is the evidence that decides whether §4.2's tuition is a defensive expenditure.

The DC Opportunity Scholarship Program is the one large randomised US urban voucher
evaluation, a lottery among oversubscribed applicants, evaluated by the federal Institute
of Education Sciences over three years.

| Horizon | Math, scholarship users | Reading, scholarship users | Significance |
|---|---|---|---|
| Year 1 | −7.3 percentile points | −4.9 percentile points | Math significant, reading not |
| Year 2 | −10.0 percentile points | −3.8 percentile points | Math significant, reading not |
| Year 3 | +0.2 percentile points | −2.1 percentile points | Neither significant |

[SOURCE: Dynarski et al., NCEE 2017-4022 p. xii; Dynarski et al., NCEE 2018-4010 p. xiii;
Webber et al., NCEE 2019-4006 pp. 4 and 10. Year-1 effect sizes −0.09 reading and −0.12
math.] The three-year synthesis: "The program had no effect on reading achievement in any
of these years. However, for mathematics, negative impacts reported in the first two years
were not found in the third year."

Two details cut against reading this as a story about bad private schools for poor
children. First, the year-1 negative impacts were concentrated among students **not**
coming from low-performing schools — that is, among exactly the families whose public
alternative was decent, which is the situation of the suburban switcher in the flight
estimates. Second, the year-3 convergence to zero is not explained by scholarship
attrition; the evaluators considered and rejected that.

Moving a child from a public school to a private one, in the only clean US experiment,
produced two years of worse maths and no detectable reading benefit at any horizon. That
is the best available evidence that the tuition in §4.2 is buying peer composition and
perceived safety rather than measured learning, and it supports treating the spend as
largely defensive. The transfer to self-paying suburban families is an extrapolation and
is flagged as such in §6.


### 5.5 The count coefficient reverses sign once metro growth is held fixed

This is the most important disconfirmation in the memo, and it kills the headline that the
count specification appears to deliver.

Regressing the change in US-born non-Hispanic white private enrolment on the change in
Hispanic public enrolment, both per 100 base-year pupils, gives about **+0.10** at every
level: roughly one white native child into private school per ten Hispanic children added
to the public schools. It is highly significant and it looks like a smaller version of
Betts & Fairlie's one-per-four.

It is an artefact of metro growth. A metro whose child population is growing adds Hispanic
public pupils and white private pupils in the same years, for the same reason. Adding the
metro's total enrolment change as a control flips the sign:

| level | raw | with total enrolment growth controlled |
|---|---|---|
| elementary | +0.101 (0.028) | **−0.127 (0.041)** |
| secondary | +0.103 (0.016) | **−0.117 (0.031)** |
| all ages 5–17 | +0.113 (0.021) | **−0.135 (0.039)** |

Conditional on how fast the metro's child population grew, a metro that added more
Hispanic public pupils added **fewer** white native private pupils. The same control turns
the foreign-born count coefficient from −0.075 to −0.355 at elementary level. Any "natives
per immigrant" ratio computed from these data without a growth control is measuring
population growth, not substitution.

### 5.6 The foreign-born share has the wrong sign; the Hispanic association is with the second generation

Three results in §3.1 point the same way, and all three cut against an immigration-driven
flight story specifically.

- **The foreign-born share of enrolled children carries a negative coefficient**, −0.284
  at elementary and −0.305 for all ages (the latter significant at 5%). Metros where the
  foreign-born share of children rose faster saw the white native private share rise
  *less*, not more.
- **Entered together, it is the US-born Hispanic share that predicts, not the foreign-born
  Hispanic share**: +0.208 (0.094) against −0.129 (0.245) at elementary. Betts & Fairlie
  found the opposite — that flight responds almost purely to non-English-speaking
  immigrants. Whatever the association here is, it is not a response to immigrant arrival.
- **The Asian share carries a negative coefficient throughout**, −0.323 at elementary and
  −0.424 for all ages. So this is not a general response to non-white composition, and a
  "diversity" reading of it fails its own falsification test in the opposite direction from
  the one the brief anticipated.

### 5.7 The share-based association does not survive the full metro sample

On the corrected 334-metro panel the share specification is **not statistically
significant at any level**: +0.154 (0.095) at elementary, +0.078 (0.073) at secondary,
+0.137 (0.083) for all ages. An earlier run on a 291-metro sample, which had dropped every
metro spanning a state line, gave +0.218 (0.084) at elementary and was significant. The
difference is the sample, not the method: restoring New York, Chicago, Washington,
Philadelphia, Kansas City, Charlotte, Memphis and Portland weakens the coefficient by a
third and widens its standard error.

The reverse-timing placebo is clean — the 2008–2010 change in the private share does not
move with the 2010–2023 change in the Hispanic share, +0.018 (0.058) at elementary — so
what is there is not a pre-trend. Dropping the five largest metros or all of California
leaves the secondary coefficient at +0.080 and +0.065, so it is not driven by a few places
either. There is simply not much there.

The instrumented estimates add nothing. The 2000-base shift-share instrument gives
coefficients from −0.28 to +0.30 with standard errors of 0.4 to 2.3, and one first-stage F
of 0.38, which is a degenerate first stage rather than a weak one. Ladder entry 136 already
recorded that this instrument dies after 2008 and that is what the first stages show.

### 5.8 District spending does not fall — state equalisation absorbs the local decline

The brief anticipated that many states send more money to high-English-learner districts,
so the sign on spending might be positive. That is close to what happens, and the
decomposition by revenue source shows the mechanism cleanly. Within a state and year, per
unit of Hispanic enrolment share:

| flow | coefficient, 2020 dollars per pupil | per 10 points of Hispanic share |
|---|---|---|
| local revenue | −4,472 (687) | −$447 |
| local property-tax revenue | −3,693 (664) | −$369 |
| state revenue | +2,809 (704) | +$281 |
| total revenue | −1,063 (1,093) | −$106, not significant |
| current spending | −1,109 (636) | −$111, marginal |
| instructional spending | −597 (309) | −$60 |

The local decline is large and precise; state aid offsets roughly 60% of it; total revenue
and spending are statistically indistinguishable from unchanged. The repo's own FY2024
cross-section pointed the same way: Hispanic pupils sit in districts spending **$474 per
pupil above** their state's mean, white pupils **$624 below** it.

Three further checks:

- **Pre-trend.** The 2000–2010 change in spending does not move with the 2010–2019 change
  in the Hispanic share, −$30 (854). For local revenue the placebo coefficient is −$1,254
  (769), against a contemporaneous −$3,336 (579) in the same window, so most of the
  local-revenue result is contemporaneous rather than a pre-existing trend, but not all of
  it.
- **Poterba's direction fails here.** The county elderly share carries a *positive*
  coefficient on per-pupil spending, +$4,917 (1,768), and its interaction with the Hispanic
  share is insignificant, +$5,954 (6,622). There is no demographic-mismatch effect in this
  panel.
- **Fractionalisation does not reproduce the Hispanic pattern.** The index gives −$474
  (265) on spending and **+$1,155 (475)** on local revenue, the opposite sign to the
  Hispanic share. That is exactly the collinearity problem Kustov & Pardelli describe in
  §5.2: in US data, "diversity" and "minority share" are different variables only in the
  places where they disagree, and where they disagree these two give different answers.

### 5.9 California districts with more Hispanic pupils vote *more* for school taxes

Across 2,954 matched school-district bond and parcel-tax measures from 1998 to 2024, the
Hispanic enrolment share is **positively** associated with the yes vote share: +0.043
(0.019), significant at 5%, with year and required-threshold fixed effects. The pass
indicator moves the same way, +0.088 (0.058), not significant. Adding the county elderly
share does not change it. The fractionalisation index is flat, +0.007 (0.037).

A ten-point higher Hispanic share goes with a 0.43-point higher yes share. That is small,
and it is a between-district comparison carrying every difference between high- and
low-Hispanic districts, so it is not a causal estimate. But the diversity-discount
prediction is that this coefficient is negative, and in the largest available US archive of
local school tax elections it is positive.


---

## 6. What is not identified here

Stated plainly, because several of these are fatal to a causal reading and the estimates
should not be quoted without them.

**The metro design has no exogenous variation after 2008.** The 2000-base shift-share
instrument is the repo's own, and ladder entry 136 already records that it is weak after
2008: the national inflow it shifts largely stopped. First-stage F statistics are reported
with every 2SLS line below. Where the F is low the 2SLS estimate is a weak-instrument
artefact and is labelled as such, not read as a causal estimate.

**Sorting is not separated from switching.** A metro's Hispanic share can rise because
immigrants arrive or because natives leave the metro entirely. Residential flight and
school flight produce the same correlation in this design. Betts & Fairlie face the same
problem and control for log native 5–18 population; this memo's metro fixed effects absorb
the level but not the change. Anything called "flight" here could be either.

**Homeschooling is inside the private share.** ACS `SCH` = 3 pools private school with
home school. Homeschooling roughly doubled around 2020-21 for reasons that have nothing to
do with immigration. Any specification whose window crosses 2020 confounds the two, and
the 2023 endpoint is the most affected observation in the panel.

**Charters are inside the public share.** See §5.1. This biases the measured flight
coefficient toward zero by an amount that grew over the window.

**The district design cannot separate a demand response from a formula response.** With
state × year fixed effects, the comparison is between districts inside the same state in
the same year, so a state's overall formula change is absorbed. But a formula that
*targets* English-learner or low-income districts moves money exactly where the Hispanic
share is rising, inside the state, in the same year. The coefficient on the Hispanic share
is then a mixture of the political-economy effect the memo is looking for and the
mechanical effect of categorical funding. The memo reports both the total and the
decomposition by revenue source (local, state, federal), which is the closest this design
gets to separating them, and it is not close enough to call causal.

**The California bond analysis is cross-sectional in the Hispanic share.** Districts are
matched to their nearest panel wave, and the identifying variation is largely between
districts, not within. It therefore carries every omitted variable that makes high-Hispanic
districts different — income, home-ownership, the age structure of the electorate. It is
reported as a description of the association, with an elderly-share control, and nothing
stronger.

**The count and share specifications answer different questions and disagree.** The count
regression is the one comparable to Betts & Fairlie's ratio, and it is the one contaminated
by metro growth; the share regression is immune to growth but is insignificant. There is no
specification here that is both comparable to the published ratio and clean. That is the
honest state of the evidence, not a result to be resolved by picking one.

**The district local-revenue result is not separated from income sorting.** Within a state
and year, a district whose Hispanic share rises is also a district whose households are
getting poorer relative to its neighbours. Local revenue per pupil falls mechanically with
the property tax base, with no change in anyone's willingness to tax themselves. The
effort measure — local revenue per pupil over county median household income — is meant to
absorb that, and it still falls, but county income is a coarse deflator for a district-level
base and cannot carry the claim on its own.

**Nothing here identifies the welfare question.** Whether the tuition in §4 is a defensive
expenditure depends on a counterfactual — what the same child would have achieved in the
public school — that no design in this memo touches. The evidence bearing on it is the
voucher literature in §5.4, which is about children who moved *with a subsidy*, from
mostly low-income families, and may not transfer to the self-paying suburban switcher who
is the subject of the flight estimates.


---

## 7. Sources

**Papers.** Full quotes, page numbers and confidence tags are in
`infra/immigration-fiscal/school_flight_2026_09_18/LIT.md`.

- Betts, J. & Fairlie, R. (2003). "Does immigration induce native flight from public
  schools into private schools?" *Journal of Public Economics* 87(5-6), 987–1012.
  [SOURCE: http://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf]
- Poterba, J. (1997). "Demographic structure and the political economy of public
  education." *Journal of Policy Analysis and Management* 16(1), 48–66; working paper
  NBER WP 5677. [SOURCE: https://www.nber.org/system/files/working_papers/w5677/w5677.pdf]
- Alesina, A., Baqir, R. & Easterly, W. (1999). "Public goods and ethnic divisions."
  *Quarterly Journal of Economics* 114(4), 1243–1284.
- Hopkins, D. (2009). "The diversity discount: when increasing ethnic and racial diversity
  prevents tax increases." *Journal of Politics* 71(1), 160–177.

**Data.**

- ACS 1-year PUMS, 2005–2023, via the Census API `acs/acs1/pums` (children 5–17).
  [SOURCE: https://api.census.gov/data/{year}/acs/acs1/pums]
- Census 2000 SF1 and ACS 5-year county tables for the elderly-share control.
  [SOURCE: https://api.census.gov/data/2000/dec/sf1, .../acs/acs5]
- MCDC Geocorr PUMA→county allocation factors (puma2k, puma12, puma22) and the OMB
  February-2013 metropolitan delineation, both reused from
  `employment_entry_2026_09_18/_cache/`. [SOURCE: https://mcdc.missouri.edu/]
- NCES Common Core of Data and Census F-33 district finance, 2000–2020, via the Urban
  Institute Education Data Portal.
  [SOURCE: https://educationdata.urban.org/api/v1/school-districts/ccd/]
- NCES Digest of Education Statistics 2023, tables 203.50 (public enrolment by race),
  205.10 (private share) and 205.50 (private enrolment and average tuition).
  [SOURCE: https://nces.ed.gov/programs/digest/d23/tables/dt23_203.50.asp and siblings]
- California Elections Data Archive, yearly workbooks, via the `justindbk/ceda` mirror of
  the CSU Sacramento portal. [SOURCE: https://github.com/justindbk/ceda]
- FRED CPI-U annual average (CPIAUCSL) for deflation.
  [SOURCE: https://fred.stlouisfed.org/series/CPIAUCSL]
- BEA, *NIPA Handbook*, Chapter 9, "Government Consumption Expenditures and Gross
  Investment," for the treatment of government output.
  [SOURCE: https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf]

**Repo lanes reused.** `school_angle_2026_09_16` (incumbent-student effects),
`ledger_absolute_2026_09_17` (F-33 and CCD loaders, district cost-to-serve differential),
`employment_entry_2026_09_18` (metro geography, 2000-base shift-share instrument).

**Instrument bias.** This analysis was produced by a language model on a politically
charged topic; see `notes/llm-bias-caveat.md`. The specific risk here is asymmetric
scepticism — applying harder disconfirmation to results that cut one way than the other.
The mitigations used were to preregister the disconfirmation checks in the brief before
looking at any estimate, to report every specification run rather than a selection, and to
write out the aggregate national series in §5.1 that cuts against the hypothesis before
estimating anything.



## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).

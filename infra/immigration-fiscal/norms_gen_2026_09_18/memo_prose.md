claude-opus-5[1m]

# Institutions and liberal-democratic norms by generation — Hispanic and Mexican-origin Americans against non-Hispanic whites and white subgroups

**Verdict:** On institutional confidence there is no deficit to converge from: Hispanic and Mexican-origin first-generation respondents are *more* confident in American institutions than non-Hispanic whites, and the third-plus generation lands at parity (adjusted gap on the 13-institution index +0.001 scale points, SE 0.018). On civil liberties there is a large first-generation deficit that closes to the level of white conservatives and white non-graduates by the third generation (Stouffer 15-item scale, adjusted: G1 −1.58, G3+ −0.42 against whites overall, −0.03 against white conservatives, −0.28 against white non-graduates). On police violence Hispanics are *less* approving than whites at every generation. What does not converge is the economic role of government, and that gap is about a fifth of the internal white ideological spread on the same items. The one measured norm that stays outside the white range is endorsement of political violence in the American National Election Studies, +10.1 points adjusted at the third generation against a white conservative-to-liberal spread of 8.3 points; that item is also the one with the best-documented measurement problems. A large share of the apparent first-generation deficit is response style rather than attitude: first-generation respondents differentiate far less between survey scenarios, and that differentiation gap closes across generations alongside the substantive gaps. Run on Mexican-origin respondents alone the pattern reproduces, with one exception: on the anti-American Muslim clergyman items the Mexican-origin third generation is still −0.25 scale points below whites overall (SE 0.09) and has not reached the white-non-graduate level. The origin-country anchor points the other way from all of this and does not survive contact with it: World Values Survey wave 7 has 71.6 percent of Mexicans rating a strong leader who need not bother with parliament and elections as good against 38.1 percent of Americans, and 21.3 percent expressing confidence in the police against 68.8 percent, yet Mexican-origin Americans show no trace of a deficit on the American versions of these questions. Section C explains why most of that contrast is the two surveys asking about different objects rather than evidence about transmission.

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

<<### A1 raw. Share saying 'a great deal' of confidence, percent (design SE, unweighted n)>>

<<### A1 raw. Confidence indices, 1-3 scale where 3 is a great deal>>

<<### A1 raw. Three-point confidence means, 3 = a great deal and 1 = hardly any>>

<<### A1 adjusted. Gap in the 'great deal' share, percentage points>>

<<### A1 adjusted. Confidence indices, scale points>>

<<### A1 adjusted. Three-point confidence means, scale points>>

<<### A1 adjusted. Where the Hispanic generations sit against white subgroups>>

## A2. Civil liberties: the Stouffer tolerance battery

This is where a real first-generation deficit exists, and it is large. On the classic fifteen-item scale (allow an atheist, a racist, a communist, a militarist and a homosexual to speak, to teach and to have a book in the library) the adjusted first-generation gap is −1.58 scale points (SE 0.20), second generation −1.27 (0.22), third-plus −0.42 (0.18). Convergence is precise: third-plus minus first is +1.16 points (0.25).

Against the honest comparators the third generation has arrived. Against white conservatives the third-plus gap is −0.03 scale points (0.19); against whites without a bachelor's degree −0.28 (0.20). Neither is distinguishable from zero. Against white liberals it is −1.02 (0.19), and the white conservative-to-liberal spread is itself 0.98 points while the white graduate-to-non-graduate spread is 1.63 points. On this battery the education cleavage inside the white population is 3.9 times the Hispanic third-generation gap against whites overall.

The item-level detail matters. Tolerance of a **homosexual** speaking, teaching or publishing is at or above the white level in every Hispanic generation, including the first. Tolerance of a **racist** shows the steepest generational gradient of any item (allow a racist to speak: 34.4, 46.1, 55.0 percent against 63.1 for whites; adjusted gaps −22.9, −12.3, −4.6). The **anti-American Muslim clergyman** items, fielded from 2008, show the largest first-generation deficit of all (allow him to speak: 16.1 percent against 48.9 for whites) and converge to white-conservative and white-non-graduate parity by the third generation (three-item scale, adjusted G3+ −0.04 against white conservatives, −0.07 against white non-graduates) while remaining −0.51 against white liberals.

<<### A2 raw. Tolerance scales>>

<<### A2 raw. Tolerant-answer share, percent>>

<<### A2 adjusted. Tolerance scales, scale points>>

<<### A2 adjusted. Tolerance against white subgroups, scale points>>

## A3. Rule of law, policing and civic values

**Obedience as a child value** starts far above the white level and converges in a single generation. Ranking obedience first or second among desirable child qualities: Mexican first generation 42.9 percent, second 20.2, third-plus 24.2, against 18.8 for whites overall and 23.4 for white conservatives. The adjusted first-generation gap is +16.1 points (1.9); by the third it is +3.2 (1.8), which is −1.6 (1.9) against white conservatives and +2.1 (1.9) against white non-graduates. Third-plus minus first is −12.9 points (2.4).

**Approval of police force** runs the other way. Hispanics of every generation are *less* willing to approve a policeman striking a citizen than whites are, and the gap narrows but does not close (adjusted: −40.0, −22.3, −11.4 points). At the third generation that is −16.9 against white conservatives and −7.2 against white liberals, so the Hispanic third generation is outside the white range on the permissive side of nothing: it is less permissive than white liberals. The same holds for the four-scenario force index.

**Punitiveness** converges upward. Death-penalty support goes 46.2, 60.9, 67.5 percent against 71.8 for whites, adjusted gaps −30.4, −9.7, −4.2; the third generation is +18.1 points more punitive than white liberals and −15.7 less than white conservatives. Support for gun permits, marijuana legalisation and the view that courts are too harsh all move from a distinctively immigrant position toward the white distribution.

<<### A3 raw. Rule of law, policing and civic values>>

<<### A3 adjusted. Rule of law and policing, percentage points>>

<<### A3 adjusted. Against white subgroups, percentage points>>

## A4. Role of government

This is the one domain where the earlier finding of non-convergence survives intact, reproducing confidence-ladder entry 87. On "government should reduce income differences" the adjusted gaps are +0.603, +0.582, +0.459 scale points on a seven-point scale; third-plus minus first is −0.144 (0.112), which is not distinguishable from zero. The same pattern holds for "government should improve living standards" and "government should do more".

The comparator changes how large this looks. The white conservative-to-liberal spread on the same seven-point item is 2.18 scale points. The Hispanic third-generation deviation from the white mean, 0.46 points, is 21 percent of that, and it places the third generation between white moderates and white liberals (−0.68 against white liberals, +1.50 against white conservatives). This is a real and persistent difference in the preferred size of government. It is not a difference in kind from differences that already exist inside the native white population.

<<### A4 raw and adjusted. Role of government>>

## A5. National identity and pluralism

The ISSP national-identity modules (2004, 2014 and a partial 2024 fielding) are thin, with Mexican-origin cells of 25-109 and all-Hispanic cells of 46-212. Read directionally.

Hispanic respondents are not less committed to a demanding conception of American identity than whites are; on several items they are more so. Saying it is very important to **respect America's laws and institutions** runs 79.5 percent in the first generation against 64.5 for whites overall and 68.5 for white conservatives (adjusted first-generation gap +19.1 points, SE 3.9). Saying it is very important to **speak English** runs 86.4 against 77.2. Saying it is very important to have **been born in America** is *higher* among second-generation Hispanics (56.9) than among whites (40.5). The one identity item where Hispanics sit clearly below whites is having **American citizenship** (adjusted −3.8 at the third generation, and −18.5 against white conservatives).

On pluralism, agreement that it is impossible for people who do not share American customs to become fully American is statistically identical between Hispanic generations and whites (adjusted third-plus −0.03 scale points, SE 0.12). Agreement that ethnic minorities never fit into the American mainstream is *lower* in the Hispanic third generation than among whites (−0.33, SE 0.13). Preference for "would rather be a citizen of America than of any other country" rises across generations to parity (adjusted third-plus +0.03, SE 0.11). On the three-way assimilation item, almost no Hispanic first- or second-generation respondent picks "immigrants should give up their culture of origin" — but neither do most whites; 5.6 percent of whites and 8.9 percent of white conservatives pick it. The overwhelming modal answer in every group is the bicultural option.

<<### A5 raw. National identity, share saying 'very important' to being truly American, percent>>

<<### A5 raw. Pluralism items, agreement means>>

<<### A5 adjusted. National identity and pluralism>>

## A6. Instrument checks: how much of this is response style?

Two checks were built from the same data, neither of which is an attitude.

**Scenario differentiation.** The four police-force items run from a very weak justification (the citizen said vulgar things) to a very strong one (the citizen was attacking the officer). Whites separate these by 83.7 points. Hispanic first-generation respondents separate them by 57.3. By the third generation the separation is 77.6. The adjusted first-generation deficit in differentiation is −0.231 (0.023) and the third-generation deficit −0.048 (0.023), converging by +0.183 (0.032).

**Battery differentiation.** The within-respondent standard deviation across the thirteen confidence items is 0.534 in the Hispanic first generation against 0.596 among whites, converging to 0.578 by the third generation; adjusted, −0.050 (0.009) falling to −0.012 (0.008).

Both checks say the same thing. First-generation respondents give less differentiated answers across a battery than whites do, and that differentiation gap closes across generations on the same schedule as the substantive gaps. Some unknown share of the measured first-generation deficit in tolerance, and of the measured first-generation surplus in institutional confidence, is therefore an artefact of how the instrument is being answered rather than of what is believed. This cuts in both directions: it inflates the apparent first-generation deficit on the tolerance battery *and* inflates the apparent first-generation surplus on the confidence battery, and it makes the measured convergence partly a convergence in survey competence. No correction is attempted; the checks are reported so the convergence estimates are not read as purely substantive.

<<### A6. Instrument checks, raw then adjusted>>

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

<<### B raw. ANES 2020 + 2024 pooled, percent>>

<<### B adjusted. Gap versus non-Hispanic white third-plus generation, percentage points>>

<<### B adjusted. Against white subgroups>>


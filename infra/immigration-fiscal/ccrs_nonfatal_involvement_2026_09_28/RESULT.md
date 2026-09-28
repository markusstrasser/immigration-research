**Verdict:** California's crash records do not show Hispanic drivers causing injury crashes out of proportion to how often they are the innocent party in them, which is the exposure proxy. In two-vehicle injury crashes of 2022–2024, their at-fault odds are **0.98** those of non-Hispanic drivers (95% CI 0.97–0.99; 0.95 against non-Hispanic white drivers). In property-damage-only crashes the ratio is 1.15 (1.14–1.16), and in fatal crashes 1.06 (0.96–1.17). The crash lane's non-fatal multi-vehicle cost base is 92% injury, so the involvement multiplier for it comes out at **m = 1.00**, not the 1.063 the lane took from fatal-crash culpability. The lane's non-fatal multi-vehicle component drops from $34.7bn to $32.6bn. Its central (a) drops from $44.5bn to **$42.1bn**, and its normalized (b) from −$2.6bn to **−$5.0bn**. The fault-based row that the operator added to the social rows drops from $45.8bn to **$42.3bn**, and its normalized value from $0.0bn to −$3.4bn. The main threat is hit-and-run: the fleeing driver's race is missing in 59–67% of those crashes. The lane's m holds only if the drivers who fled were about 73% Hispanic. If they resemble identified at-fault drivers who hit the same victims in the same county, the share is 45%. [CALCULATION: `ccrs_qie.py` → `derived/qie_or_table.csv`, `derived/crash_component_revision.csv`, `derived/hit_and_run_break_even.json`]
claude-opus-5-5

# Non-fatal crash involvement of Hispanic drivers in California (CCRS quasi-induced exposure)

Lane opened 2026-09-28 22:15 JST (from `date`). It tests the per-mile involvement multiplier
m = (1 + OR)/2 = 1.063 that `road_crash_externality_2026_09_28` (commit 5b6d859) carries from
fatal-crash culpability in FARS. The test uses the California Highway Patrol's crash records
(CCRS, data.ca.gov) for fatal, injury and property-damage-only (PDO) two-vehicle crashes. The
crash lane itself is not edited; `ccrs_qie.py` imports its `crash_model.py` read-only.

California's Hispanic residents are **80.0% Mexican-origin**: 12,859,953 of 16,069,214 (80.3% in
2023). [SOURCE: ACS 2024 1-year B03001_004E/_003E, state 06, via api.census.gov;
`_cache/acs1_2024_B03001_ca.json`] CCRS race is the officer's single-choice entry (Asian, Black,
Hispanic, Other, White, or blank). It is neither the driver's self-report nor an origin. It cannot
separate Mexican-origin drivers, and a Hispanic driver can be entered as white or other.

## Method, fixed before the first odds ratio was computed (22:35 JST)

- **Sample.** Crashes of 2022–2024 with:
  - exactly two parties, both motor-vehicle drivers (party type `Driver`);
  - exactly one party at fault;
  - no on-duty emergency vehicle;
  - no private-property flag (NHTSA's cost base counts trafficway crashes only);
  - no hit-and-run flag on the crash or on either party;
  - both drivers' race recorded.

  Duplicate report numbers within an agency keep the highest report version. "At fault" is the
  officer's primary-collision-factor party: `IsAtFault` matches the primary-collision-factor
  party number in 383,689 of 383,713 joined 2024 cases. Not at fault is coded blank. [DATA]
- **Severity** is the worst injury in the crash:
  - fatal: killed > 0 or a fatal injury record;
  - severe: suspected serious injury (legacy code "severe");
  - other visible: suspected minor injury (legacy "other visible");
  - complaint of pain: possible injury (legacy "complaint of pain");
  - PDO: nobody injured or killed.
- **Estimators.** For group g against reference set R:
  - QIE odds ratio, (at-fault g / not-at-fault g) ÷ (at-fault R / not-at-fault R), computed crude
    and as Mantel–Haenszel within county × year;
  - mixed-pair odds ratio, (g at fault with an R driver) ÷ (R at fault with a g driver). It does not
    depend on who meets whom.

  The 95% intervals come from 400 stratified multinomial bootstrap draws of crashes (200 for the
  three injury sub-classes).
- **Central, chosen before the first odds ratio.** The within-county QIE odds ratio against all
  non-Hispanic drivers, pooled over 2022–2024, mirrors the lane's within-state FARS figure. Injury
  and PDO values of m are combined with the PDO row's share of the lane's non-fatal multi-vehicle
  cost base as the weight: 8.4%, $60.1bn of $716.0bn. [CALCULATION from `crash_model.py`
  constants; `derived/apply_meta.json`] The other estimators are checks.
- **Hit-and-run crashes** are left out of the central. They are handled with bounds and a
  break-even instead.

Sample flow, 2022–2024 [DATA: `derived/sample_flow.csv`]:

| Step | Crashes |
|---|---:|
| Crash rows | 1,232,240 |
| Deleted and duplicate report versions dropped | 1,231,199 |
| Two parties, both drivers | 661,195 |
| Exactly one at fault | 613,644 |
| No on-duty emergency vehicle | 603,307 |
| Not on private property | 596,495 |
| No hit-and-run flag | 450,086 |
| Both races recorded (primary sample) | **429,913** |

## Odds-ratio table

Primary sample, 2022–2024 pooled. "Crashes" counts all crashes in the sample at that severity.
The count columns cover only Hispanic drivers and the reference group. The mixed-pair counts are
Hispanic-at-fault / reference-at-fault crashes between the two groups.
[CALCULATION: `derived/qie_or_table.csv`, `derived/pair_counts.csv`]

**Against all non-Hispanic drivers (central reference):**

| Severity | Crashes | Hispanic at fault / not | Non-Hispanic at fault / not | QIE crude | QIE within county × year (95% CI) | Mixed pairs (95% CI) [counts] | m = (1+OR)/2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fatal | 2,736 | 1,258 / 1,218 | 1,478 / 1,518 | 1.061 | 1.065 (0.962–1.173) | 1.073 (0.957–1.199) [585 / 545] | 1.032 |
| Severe injury | 12,375 | 5,396 / 5,297 | 6,979 / 7,078 | 1.033 | 1.036 (0.986–1.088) | 1.041 (0.984–1.103) [2,488 / 2,389] | 1.018 |
| Other visible injury | 62,810 | 26,381 / 26,862 | 36,429 / 35,948 | 0.969 | 0.967 (0.947–0.989) | 0.962 (0.938–0.987) [12,013 / 12,494] | 0.984 |
| Complaint of pain | 121,636 | 54,310 / 54,670 | 67,326 / 66,966 | 0.988 | 0.987 (0.974–1.002) | 0.985 (0.970–1.002) [24,223 / 24,583] | 0.994 |
| **All injury** | 196,825 | 86,089 / 86,832 | 110,736 / 109,993 | 0.985 | **0.984 (0.973–0.994)** | 0.981 (0.969–0.993) [38,724 / 39,467] | **0.992** |
| **PDO** | 230,352 | 107,996 / 100,508 | 122,356 / 129,844 | 1.140 | **1.150 (1.136–1.163)** | 1.168 (1.153–1.184) [51,942 / 44,454] | **1.075** |
| All non-fatal, unweighted | 427,177 | 194,085 / 187,340 | 233,092 / 239,837 | 1.066 | 1.070 (1.061–1.078) | 1.080 (1.070–1.090) [90,666 / 83,921] | 1.035 |

**Against non-Hispanic white drivers:**

| Severity | Hispanic at fault / not | White at fault / not | QIE crude | QIE within county × year (95% CI) | Mixed pairs (95% CI) [counts] | m |
|---|---:|---:|---:|---:|---:|---:|
| Fatal | 1,258 / 1,218 | 1,001 / 979 | 1.010 | 1.026 (0.918–1.152) | 1.020 (0.895–1.178) [361 / 354] | 1.013 |
| Severe injury | 5,396 / 5,297 | 4,330 / 4,448 | 1.046 | 1.055 (0.994–1.106) | 1.027 (0.956–1.098) [1,499 / 1,459] | 1.027 |
| Other visible injury | 26,381 / 26,862 | 20,498 / 20,219 | 0.969 | 0.968 (0.949–0.990) | 0.962 (0.933–0.995) [6,737 / 7,003] | 0.984 |
| Complaint of pain | 54,310 / 54,670 | 34,400 / 32,409 | 0.936 | 0.935 (0.920–0.954) | 0.939 (0.917–0.964) [11,868 / 12,636] | 0.968 |
| All injury | 86,089 / 86,832 | 59,230 / 57,076 | 0.955 | 0.955 (0.942–0.970) | 0.953 (0.935–0.971) [20,104 / 21,099] | 0.977 |
| PDO | 107,996 / 100,508 | 63,627 / 67,808 | 1.145 | 1.158 (1.143–1.175) | 1.169 (1.150–1.192) [26,266 / 22,466] | 1.079 |
| All non-fatal, unweighted | 194,085 / 187,340 | 122,857 / 124,884 | 1.053 | 1.059 (1.049–1.069) | 1.064 (1.053–1.079) [46,370 / 43,565] | 1.029 |

The three estimators agree to within 0.03 in every row. Injury odds ratios sit at 0.980–0.988 in each year. PDO sits at 1.144–1.153. Fatal is noisy:
0.97, 1.10 and 1.15. [DATA: `derived/qie_or_by_year.csv`] For context against white drivers,
Black drivers show 1.03 in injury and 1.30 in PDO, Asian drivers 0.85 and 0.82, and "other"
drivers 0.92 and 0.98. [DATA: `derived/qie_or_other_groups_vs_white.csv`]

### Check against FARS (fatal crashes)

| Sample | Hispanic at fault / not (killed) | Non-Hispanic at fault / not (killed) | Odds ratio |
|---|---:|---:|---:|
| CCRS 2022–2024, all drivers in two-driver fatal crashes | 1,258 / 1,218 | 1,478 / 1,518 | 1.061 (crude), 1.065 (within county × year) |
| CCRS 2022–2024, killed drivers only | 744 / 360 | 897 / 489 | 1.127 |
| FARS 2023, killed drivers, California | 150 / 133 | 164 / 166 | 1.142 |
| FARS 2023, killed drivers, national | 1,068 / 719 | 4,008 / 2,644 | 0.980 |

[CALCULATION: `derived/killed_driver_check.csv`; FARS read from the crash lane's
`_cache/fars2023/` with its culpability rule] The national FARS line reproduces the lane's crude
0.98, which is the positive control for this re-implementation. In California the two sources
agree on killed drivers, 1.13 and 1.14. Adding the surviving drivers of the same fatal crashes
lowers the ratio to 1.06. At-fault Hispanic drivers die in their crashes more often than at-fault
non-Hispanic drivers, so killed-driver designs overstate the group's culpability, by about 6% in
California. [INFERENCE] The lane's 1.13 comes from killed drivers only.

Coverage of fatal crashes is complete. CCRS records 3,909 fatal crashes and 4,256 deaths for
2023, against FARS California's 3,826 and 4,169 (102%). [DATA: `derived/coverage_by_year.csv`]

## Sobriety, hit-and-run, licence and insurance by race

Two-driver trafficway crashes, including hit-and-run, 2022–2024. [DATA: `derived/driver_traits_by_race.csv`]

| Share of drivers | Fatal: Hispanic | Fatal: non-Hispanic | Injury: Hispanic | Injury: non-Hispanic | PDO: Hispanic | PDO: non-Hispanic |
|---|---:|---:|---:|---:|---:|---:|
| At fault, had been drinking | 29.8% | 22.0% | 10.7% | 6.7% | 9.5% | 6.4% |
| At fault, drinking and under the influence | 25.6% | 18.6% | 9.1% | 5.2% | 8.0% | 5.0% |
| At fault, under drug influence | 9.9% | 12.9% | 0.53% | 0.66% | 0.39% | 0.56% |
| Not at fault, had been drinking | 6.5% | 4.7% | 1.5% | 1.4% | 1.0% | 0.9% |
| At fault, licence class U | 32.8% | 18.7% | 18.6% | 7.2% | 20.7% | 7.2% |
| At fault, aged 14–24 (of stated ages) | 27.8% | 18.0% | 28.0% | 20.5% | 27.2% | 20.6% |
| At fault, male | 82.4% | 76.2% | 66.7% | 59.1% | 71.1% | 62.6% |

For non-Hispanic white drivers alone, the at-fault drinking shares are 20.7% (fatal), 7.0%
(injury) and 7.1% (PDO).

- **Alcohol.** The Hispanic excess is concentrated among at-fault drivers. Among not-at-fault
  drivers the drinking shares are close, 1.5% against 1.4% in injury crashes, so officers are not
  simply recording drinking more often for Hispanic drivers. With both drivers sober, the odds
  ratios are 0.962 (injury), 1.135 (PDO) and 1.105 (fatal). [DATA: `derived/qie_or_sensitivity.csv`]
- **Hit-and-run.** Across all trafficway crashes, 85,561 at-fault drivers who fled have no race
  recorded. Of the 5,208 fled at-fault drivers whose race was recorded, 2,317 (44.5%) were
  Hispanic. That is close to the Hispanic share of all at-fault drivers with race recorded
  (45.4%). As a rate, 0.59% of Hispanic at-fault drivers are recorded as having fled, against
  0.55% of white drivers. These figures measure identification, not flight. Hispanic drivers make
  up 44.2% of the not-at-fault drivers in hit-and-run crashes and 43.8% in other crashes.
  [DATA: `derived/at_fault_drivers_hit_and_run_by_race.csv`, `derived/not_at_fault_race_mix_by_hit_and_run.csv`]
- **Licence.** The layout lists licence class `U` without defining it. Its pattern resembles
  FARS's unlicensed rates (17.6% of Hispanic against 4.9% of non-Hispanic killed drivers). But
  identified fled drivers almost never carry `U` (0.7% against 12.5% of other at-fault drivers),
  so it is a value entered at the scene. Reading it as "unlicensed" is an [INFERENCE]. Mexican
  licences are rare: 2,241 of 824,705 Hispanic drivers in 2022–2024 (0.3%). [DATA: `derived/licence_class_u_shares.json`,
  `derived/licence_state_top_codes_by_race.csv`]
- **Insurance.** The CCRS export has **no financial-responsibility or insurance field**.
  [DATA: `_cache/rawdata_template.txt`] The lane's insured-share assumption (0.72) stays untested.

## Implied m and revised crash components

Only the non-fatal parts change:
- the multi-vehicle non-fatal component ($34.67bn), by m_mv / 1.063, with m_mv the cost-weighted
  injury and PDO m;
- the non-fatal part of the non-motorist component ($4.27bn of $7.74bn), by the injury m / 1.063.

The fatal parts ($0.05bn multi-vehicle, $3.47bn non-motorist) and single-vehicle ($2.02bn) keep
the lane's m. (a) and (b) are the requested scaling. For (b), the lane's (1 − 1/R) is applied
per component, with R = 0.888 × that component's m. The fault-based columns re-evaluate the
lane's formula with the measured odds ratio, which in that variant enters as OR/2. The lane's
central is reproduced exactly before any change: $44.480bn, −$2.646bn and $45.776bn.
[CALCULATION: `derived/crash_component_revision.csv`, `derived/apply_meta.json`]

| Scenario | m, non-fatal MV | m, non-fatal NM | Non-fatal MV $bn | (a) absolute $bn | (b) normalized $bn | Fault-based $bn | Fault-based normalized $bn |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lane central (FARS) | 1.063 | 1.063 | 34.67 | 44.48 | −2.65 | 45.78 | 0.01 |
| **CCRS central: QIE within county × year, against all non-Hispanic** | **0.999** | **0.992** | **32.57** | **42.09** | **−5.04** | **42.34** | **−3.43** |
| Same, 95% CI low / high | 0.993 / 1.004 | 0.987 / 0.997 | 32.39 / 32.74 | 41.89 / 42.29 | −5.24 / −4.84 | 42.05 / 42.62 | −3.72 / −3.15 |
| Against non-Hispanic white | 0.986 | 0.977 | 32.14 | 41.61 | −5.52 | 41.65 | −4.12 |
| Mixed pairs, against all non-Hispanic | 0.998 | 0.991 | 32.55 | 42.07 | −5.06 | 42.31 | −3.46 |
| Severity-weighted (police injury classes mapped onto MAIS rows) | 1.009 | 0.992 | 32.89 | 42.41 | −4.72 | 42.81 | −2.96 |
| Hit-and-run: fled drivers imputed from victim race and county | 1.003 | 0.996 | 32.71 | 42.25 | −4.88 | 42.57 | −3.20 |
| Hit-and-run: fled drivers' Hispanic odds ×2 | 1.036 | 1.024 | 33.79 | 43.44 | −3.69 | 44.29 | −1.48 |
| Hit-and-run: break-even, odds ×3.67 | 1.063 | 1.046 | 34.67 | 44.41 | −2.71 | 45.70 | −0.07 |
| Hit-and-run: every unidentified fled driver Hispanic | 1.128 | 1.099 | 36.77 | 46.72 | −0.40 | 49.05 | 3.28 |
| Hit-and-run: no unidentified fled driver Hispanic | 0.919 | 0.924 | 29.98 | 39.22 | −7.90 | 38.20 | −7.57 |

- **Per member.** At the central, the non-motorist non-fatal part is $3.98bn. The but-for total
  is $1,029 per member, against the lane's $1,088.
- **Full re-evaluation.** Re-evaluating the full formula also moves the fault share inside the
  liability term. That gives (a) $42.47bn and (b) −$5.09bn at the central, within $0.4bn of the
  scaling.
- **Fatal m.** Using CCRS's all-driver fatal m (1.032) for the fatal and single-vehicle parts as
  well would remove about another $0.2bn. It is not applied, since the brief covers non-fatal
  parts only.

The grid ranges of the lane ($5.7–145.1bn) are not recomputed. The non-fatal m moves the central
by about 5%, which is small against the traffic-volume elasticity that sets the grid's spread.
[INFERENCE]

## Disconfirmation

The strongest case for keeping the lane's 1.063 or raising it has four parts. Hit-and-run drivers
who are never identified could be disproportionately Hispanic. Officers could record race
inaccurately. Reporting could be selective. And California's Hispanic drivers could be safer
than the national Mexican-origin group. Each is checked below.

1. **Missing race in hit-and-run crashes (the largest threat).**
   - Of the clean two-driver trafficway crashes, 24.5% are hit-and-run: 32% of PDO and 13.5% of
     injury crashes. The at-fault driver's race is missing in 59% (injury) and 67% (PDO) of them.
     Outside hit-and-run, missing race is balanced by role: 4.0% of at-fault against 4.0% of
     not-at-fault drivers in injury crashes, and 2.4% against 2.1% in PDO crashes. There it does
     not tilt the ratio. [DATA: `derived/race_missing.csv`]
   - Bounds: if every unidentified fled driver were Hispanic, the injury odds ratio would be 1.20
     and PDO 1.89, giving m 1.128 and $46.7bn. If none were, m is 0.919 and $39.2bn. Imputing from
     the victim's race and county gives 0.992 and 1.162, and m 1.003.
     [DATA: `derived/hit_and_run_bounds.csv`]
   - The lane's m returns at a Hispanic odds multiplier of 3.67 on fled drivers. The fled pool
     would then be 73% Hispanic among injury crashes and 75% among PDO crashes, against 45% and
     47% under imputation. [CALCULATION: `derived/hit_and_run_break_even.json`,
     `derived/hit_and_run_mnar_sensitivity.csv`]
   - Plausibility, for the break-even:
     - Unlicensed immigrants do flee more. Lueders, Hainmueller and Lawrence (2017) find that
       California's AB60 licences reduced hit-and-runs. [SOURCE: PNAS abstract via Europe PMC;
       effect size not read]
     - Suppose licence class U means unlicensed, and such drivers flee F times as often. Class U
       covers 19.5% of Hispanic and 5.5% of white at-fault drivers. Even F = 50 raises m only to
       1.046, short of 1.063. [CALCULATION: `derived/hit_and_run_licence_flight_model.csv`]
     - Identified fled drivers are 44.5% Hispanic, no more than at-fault drivers generally. Only
       about 6% of fled at-fault drivers are ever identified by race, though, so this is weak
       evidence.
2. **Officer race coding.**
   - Race is the officer's call. The not-at-fault (exposure) shares match an external benchmark
     roughly: Hispanic drivers are 44.1% of not-at-fault drivers in injury crashes and 43.6% in PDO
     crashes. They are 42.5% of California workers who drive to work (alone, plus half of
     carpoolers). White drivers are 29.0% and 29.4% of not-at-fault drivers against 31.7% of
     commuters. [SOURCE: ACS 2024 1-year B08105I, B08105H, B08301; DATA: `derived/acs_ca_checks.csv`]
   - Commuting is not all driving, so this checks the coding's aggregate level only.
   - Misclassification that does not depend on fault pulls every odds ratio toward 1. Its size is
     unknown. [GAP]
3. **Bias in at-fault assignment.**
   - West (2018) studies crash investigations, where dispatch is independent of the driver's race.
     State police cite drivers of another race more often: +2.96 percentage points for
     Hispanic/white pairs, against a mean citation rate near 45%. [SOURCE: West 2018 working
     paper, §4.1 and Table 3, read as `_cache/west.txt`]
   - If fault assignment carried a similar own-race tilt, and most investigating officers are
     non-Hispanic, the Hispanic odds ratios here would be biased upward. The true m would then be
     further below 1.063, not above it. The race mix of CHP and local officers was not retrieved.
     [GAP]
   - The data do not show discretion driving the PDO excess. It is largest in rear-end crashes
     (1.35 against all non-Hispanic), where fault follows from which car struck which. It is 1.00
     in broadside and 0.99 in sideswipe PDO crashes. [DATA: `derived/qie_or_sensitivity.csv`]
   - Citation, the discretionary step after fault, shows much higher Hispanic odds ratios among
     cited at-fault drivers: 1.29 in injury and 1.50 in PDO crashes, with 5.9% of injury crashes
     cited. That fits either West's citation bias or more citable violations. The fault flag used
     here is assigned on every report.
4. **Representativeness of CCRS.**
   - CHP writes 52% of crash reports and local agencies 48%.
   - Local coverage is incomplete. LAPD contributes about 11.8k crashes a year, against
     16.4–16.7k on LAPD's own open-data portal (71%). San Diego police report almost no PDO
     crashes: 89 of 11,102. [DATA: `derived/top_reporting_agencies.csv`;
     `_cache/lapd_open_data_count_*.json`, data.lacity.org d5tf-ez2w]
   - The PDO sample is 68% CHP; the injury sample is 45% CHP.
   - Nationally, about 60% of PDO crashes and 32% of injury crashes are never reported to police.
     [SOURCE: Blincoe et al. 2023, DOT HS 813 403, executive summary, read as the crash
     lane's `_cache/blincoe.txt`]
   - A PDO crash is more likely to reach the police when the at-fault driver has no licence or
     insurance, because the other driver needs a report. That would inflate the Hispanic at-fault
     share among reported PDO crashes. This is plausible but unmeasured. [INFERENCE]
   - The odds ratios also differ by agency. For PDO, CHP gives 1.19 and local agencies 1.07; for
     injury, 1.02 and 0.95.
   - For these reasons the injury ratio (0.98) is the better-measured one. It carries 92% of the
     lane's non-fatal multi-vehicle cost.
5. **The exposure assumption of quasi-induced exposure.** The mixed-pair estimator conditions on
   the two groups having met, so assortative mixing cannot bias it. It gives the same answers:
   0.981 for injury, 1.168 for PDO. Culpability rises with severity: 0.967 for other visible
   injury, 0.987 for complaint of pain, 1.036 for severe and 1.065 for fatal crashes. The mapping
   onto the lane's cost rows is therefore uncertain. The severity-weighted variant, with police
   classes mapped onto MAIS rows, gives m 1.009 and $42.4bn.
6. **Age and sex.** Hispanic at-fault drivers are younger and more often male. Adjusted for the
   driver's age band and sex, the odds ratios fall to 0.946 (injury), 1.118 (PDO) and 0.916
   (fatal). The lane needs the group's actual drivers, so the unadjusted figures are the right
   inputs. The adjusted ones show that composition explains the PDO and fatal excess in part.
   [DATA: `derived/qie_or_age_sex_adjusted.csv`]
7. **Transport to the national Mexican-origin group.**
   - California is one state. The lane's Mexican-coded FARS ratio (1.47) comes mostly from Texas
     and Arizona death certificates, where coding looks uneven. CCRS cannot separate Mexican
     origin.
   - In California, FARS and CCRS agree for killed drivers (1.14 and 1.13).
   - Whether Texas or Arizona Hispanic drivers are more culpable in non-fatal crashes is untested.
     Texas CRIS records ethnicity. [GAP]
8. **The instrument.** This result lowers a cost attributed to the group. On politically charged
   topics the LLM doing the analysis has its own tilt (`notes/llm-bias-caveat.md`). The central
   was fixed before any odds ratio was seen. The one input that could reverse the conclusion, the
   race of fled drivers, is carried as explicit bounds and a break-even rather than set to a
   convenient value.

[FRAMING-SENSITIVE] The reference group changes the (a) total by $0.5bn: all non-Hispanic
drivers give $42.1bn and non-Hispanic white drivers $41.6bn. The fault-based row is the one the
operator added to the account (decision `2026-09-28-social-items-pollution-crashes`). Its revision,
$45.8bn to $42.3bn, is the decision-relevant figure.

## What would change the verdict

- Evidence that unidentified hit-and-run drivers in California are over 70% Hispanic.
- Evidence that officers under-assign fault to Hispanic drivers in injury crashes.
- A Texas or Arizona injury-crash odds ratio well above 1.06.

## Files covered and skipped

Covered:

| File or source | Used for |
|---|---|
| `_cache/ccrs/{crashes,parties,injuredwitnesspassengers}_{2022,2023,2024}.csv.gz` (data.ca.gov CKAN package `ccrs`, fetched on Modal; sha256 in the sibling `.json`, re-verified locally) | all counts and odds ratios |
| `_cache/rawdata_template.txt` (CCRS export layout, CHP 9/27/2024) | field definitions; no insurance field |
| `_cache/ckan_ccrs.json` | resource list and sizes; 2025 partial |
| `_cache/acs1_2024_B03001_ca.json`, `_cache/acs1_2023_B03001_ca.json`, `_cache/acs1_2024_B08105_ca.json` (api.census.gov) | Mexican-origin share; commuter benchmark |
| `_cache/lapd_open_data_count_{2022,2023,2024}.json` (data.lacity.org) | LAPD coverage check |
| `_cache/west_2018_racial_bias_police_investigations.pdf` (read as `west.txt`) | abstract, §2.3 and the main estimate |
| `_cache/epmc_lueders.json`, `_cache/epmc_24529097.json` (Europe PMC) | Lueders et al. 2017 and Torres et al. 2014 abstracts |
| Crash lane: `crash_model.py` (imported read-only, no bytecode written), `derived/fars_group_2023.json` (through that import), `_cache/fars2023/FARS2023NationalCSV/` (California check), `_cache/blincoe.txt` (unreported shares), `RESULT.md` | the formulas, positive control, cost weights, FARS check |

Skipped:

| Source | Reason |
|---|---|
| CCRS 2016–2021 and 2025–2026 | the brief asks for the latest three full years; 2025 is partial (34 MB crashes file against 185–198 MB) |
| SWITRS through TIMS | CCRS has party race; TIMS needs registration |
| Alpert, Smith & Dunham 2004 (not-at-fault crash drivers as a racial benchmark) | the open-access link returned an HTML bot page [GAP] |
| Lueders et al. 2017, size of the hit-and-run effect | PNAS 403, PMC bot page, Europe PMC full text 500; only the abstract's direction is used [GAP] |
| Torres et al. 2014 (J Safety Res; FARS against roadside survey) | abstract read; says Hispanic drivers are less often in single-vehicle crashes and face the same risk at each BAC; not used in numbers |
| CHP and local officer race composition | not retrieved; needed to size any own-race bias [GAP] |
| Texas CRIS party ethnicity | out of scope for this lane [GAP] |
| Exa and Firecrawl | Exa MCP not connected in this session; Firecrawl returns 402 per the brief |

Next queries if re-dispatched:
- Texas CRIS person-level ethnicity, for quasi-induced exposure in the state with most
  Mexican-coded FARS deaths.
- CHP 555 manual definitions of licence class `U`. SWITRS party files are believed to carry a
  financial-responsibility code [TRAINING-DATA, unverified]; TIMS SWITRS would test insurance by
  race.
- CHP officer race shares, to size a West-type bias.
- Lueders et al. 2017 full text, for the hit-and-run effect size, to calibrate the flight ratio F.

## Reproduce

```sh
# data.ca.gov answers this machine's region with Cloudflare 1009, so the pull runs on Modal
cd infra/immigration-fiscal/ccrs_nonfatal_involvement_2026_09_28
modal run acquire_ccrs_modal.py::probe          # writes _cache/ckan_ccrs.json
modal run acquire_ccrs_modal.py::fetch --names "Raw Data Template,Crashes_2024,Parties_2024,InjuredWitnessPassengers_2024,Crashes_2023,Parties_2023,InjuredWitnessPassengers_2023,Crashes_2022,Parties_2022,InjuredWitnessPassengers_2022"
modal volume get ccrs-2026-09-28 / _cache/ccrs/
gzip -dc _cache/ccrs/rawdata_template.docx.gz > _cache/rawdata_template.docx && textutil -convert txt -output _cache/rawdata_template.txt _cache/rawdata_template.docx
# ACS inputs (key from acquire/config.local.env; redact it from any output)
#   2024/acs/acs1?get=NAME,B03001_001E,B03001_003E,B03001_004E,...&for=state:06 -> _cache/acs1_2024_B03001_ca.json
#   2024/acs/acs1?get=NAME,B08301_001E,B08301_003E,B08301_004E,B08105I_001E,B08105I_002E,B08105I_003E,
#                     B08105H_001E,B08105H_002E,B08105H_003E&for=state:06 -> _cache/acs1_2024_B08105_ca.json
cd -
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ccrs_nonfatal_involvement_2026_09_28/ccrs_qie.py
```

The analysis takes about 15 seconds. A rerun between 22:53 and 22:57 JST left every `derived/`
file byte-identical (bootstrap seed 20260928).

## Log (times from `date`)

- 2026-09-28 22:15 JST: stub written. Read the crash lane's `crash_model.py`, then probed
  data.ca.gov CKAN for the CCRS crashes, parties and injured resources and their sizes.
- 2026-09-28 22:28 JST: data in hand.
  - data.ca.gov returns Cloudflare error 1009 (region banned) to this machine, so CKAN and the
    downloads ran on Modal (`acquire_ccrs_modal.py`, app ap-vJ4y0rF3XQOGymvUdpP0Uw for the probe).
  - CKAN package `ccrs` has 34 resources: one crashes, parties and injured CSV per year, 2016–2026.
    2025 is partial (crashes file 34 MB against 185–198 MB for 2022–2024), so the three latest
    full years are 2022–2024.
  - Nine CSVs, 1.43 GB raw and 186 MB gzipped; sha256 re-verified locally after the relay.
    [DATA: `_cache/ccrs/*.csv.gz` and `*.json`]
  - The export layout (`_cache/rawdata_template.txt`, CHP 9/27/2024) has:
    - party race (A/B/H/O/W; blank = not stated; recorded by the officer);
    - `IsAtFault` and `IsHitAndRun`;
    - two sobriety/drug codes;
    - age, sex, licence class and licence state.

    It has **no financial-responsibility or insurance field**. Not at fault is coded blank, not
    False: 17 False against 383,931 True in 2024. The at-fault party equals the
    primary-collision-factor party in 383,689 of 383,713 joined cases.
  - Coverage: 405–417k crashes a year, 52% from CHP and 48% from local agencies. Each year has
    3,750–4,330 fatal crashes, 226–237k injured people and 241–245k PDO crashes.
  - Race is blank for 12.8% of 2024 drivers, mostly among at-fault drivers: 30,521 at-fault
    hit-and-run drivers and 41,417 other at-fault drivers, against 21,007 not-at-fault drivers.
    [DATA]
  - California: 80.0% of Hispanic residents are Mexican-origin (ACS 2024; 80.3% in 2023).
- 2026-09-28 22:35 JST: method and central fixed in this file before the first odds ratio.
- Between 22:35 and 22:49 JST (no `date` call between them): first full run of `ccrs_qie.py`.
  - Injury 0.984, PDO 1.150, fatal 1.065 against all non-Hispanic drivers.
  - The positive control reproduces the lane's $44.480bn, −$2.646bn and $45.776bn.
  - Central revision: $42.1bn, −$5.0bn; fault-based $42.3bn.
- 2026-09-28 22:49 JST: added the hit-and-run break-even (k = 3.67; 73–75% Hispanic fled
  drivers), the severity-weighted variant (m 1.009) and the ACS commuter benchmark (Hispanic
  42.5%).
- 2026-09-28 22:50–22:51 JST: licence-mediated flight model. The first run defined identified
  fled drivers by the crash flag; corrected to the party flag. Class U is almost absent among
  identified fled drivers (0.7%), so F is kept as a free parameter; even F = 50 gives m 1.046.
- By 2026-09-28 22:53 JST: LAPD open-data counts (16,417 / 16,461 / 16,720) against CCRS
  (about 11.8k a year).
- Between 22:53 and 22:57 JST (no `date` call between them): `sys.dont_write_bytecode` set
  before importing the crash lane; the probe entrypoint now writes `_cache/ckan_ccrs.json`; the
  rerun left every `derived/` file byte-identical.
- 2026-09-28 22:57 JST: this file written in full. The crash lane's RESULT.md, as edited by the
  lead in b79039d, now carries the fault-based row in the social rows; this lane's revision of that
  row is $45.8bn → $42.3bn.

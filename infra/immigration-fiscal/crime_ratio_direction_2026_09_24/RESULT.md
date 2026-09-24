**Verdict:** The one-way lean is real in custody and arrest records and in the victim-cost lane's survey count. It is not real in the offender ratios.

On the leading reading the NIBRS murder ratio (Hispanic ÷ non-Hispanic white) stays at **2.30**. Across 18 allocation methods it ranges 2.12–2.42: arrestee validation gives −8%, covariate imputation up to +5%, and SHR nationally −1% to +6%. Robbery goes from 4.22 to **4.15** (−1.6%) once reporting to police is weighed; that change cannot be told apart from zero, and the band is 3.65–4.29. Of the counter items, White subtraction is absent from this frame (it adds 0) but overstates arrest-table ratios in TX+AZ by 7% for murder and 14% for robbery. The 2020 census coverage error, if it carries into the denominators, lowers both ratios by another 6.5% (murder 2.15, robbery 3.88).

Inside the account, booking in TX+AZ records 3.8% fewer Hispanic arrestees than the offender segment of the same incident (true share ×1.040). Carried to the national arrest key, that proposes **+$0.87bn**, taking the main case from $203.2–249.6bn to $204.1–250.5bn. The corrected jail share (14.4% → 19.1%) moves only the BJS check arm (+$1.54bn, against the audit's +$2.45bn bound). An ACS facility-recording sensitivity of +$1.99bn is the operator's call. Beside the account, victims' harm rises from $28.92bn to **$30.93bn** (+$2.00bn), because NCVS table 13 gives Hispanic members of mixed offender groups no share. Unknown-offender imputation moves the murder cost by only −$0.08bn to +$0.37bn.

Certainty differs by finding:

| Finding | Confidence |
|---|---|
| The jail count and the table-13 rule understate | High |
| The size of the national booking transfer | Moderate |
| The offender-ratio band (±8%, centred near zero) | Two-sided |

Model self-report: claude-opus-5-5[1m]. A lane adopts nothing. Every dollar figure below is a proposed change or a sensitivity, and each is marked as inside the account or beside it. The main-case bands below are simple additions of lane deltas; to get the real figure, run the adopted set through `main_case_2026_09_23/main_case.js`. [CALCULATION: all figures from the scripts listed under Reproduce]

## Proposed changes

| Finding | Line | Now | Proposed | Δ $bn | Status |
|---|---|---|---|---:|---|
| Booking records 3.8% fewer Hispanic arrestees than the offender segment of the same incident (true share ×1.040) | justice key, arrest-keyed dollars (inside) | RR 1.1454 | RR 1.1913 | **+0.87** (+0.33 to +0.95) | proposed; carrying the TX+AZ factor to national arrests is [INFERENCE] |
| ACS facility records under-record Hispanic origin, f = 0.897 | prisons key (inside) | 0.1419 | 0.1583 | +1.99 (+0.62 to +3.28; −0.14 without federal detention) | one-sided sensitivity, operator's call |
| BJS jail share 14.4% → 19.1% (survey odds ratios) | prisons, BJS check arm | 0.1428 | 0.1546 | +1.54 against the adopted key (+0.93 to +2.09) | check only; no adopted number moves |
| NCVS table 13 counts no Hispanic in mixed offender groups | victims' harm, non-fatal (beside) | $28.92bn | $30.93bn | **+2.00** (0 to +4.03) | proposed; θ = 0.498 is the NIBRS mixed-group fraction |
| Imputation of unknown homicide offenders (SHR) | victims' harm, murder (beside) | $9.16bn | unchanged | −0.08 to +0.37 | no change |
| White subtraction | arrest key | — | — | 0 | the key is Hispanic ÷ all; no NH-white construction |
| 2020 census coverage (PES) | per-capita ratios | — | ratios −6.5% | 0 | cancels in dollars |

[CALCULATION: dollar_effects.py → derived/dollar_effects.csv]

Main-case arithmetic, by addition:
- booking alone: $203.2–249.6bn → $204.1–250.5bn;
- booking plus the ACS sensitivity: $206.1–252.5bn.

Safety responds at 1.0 in every service construction, so a justice-key change passes 1:1 into the band. [SOURCE: `cj_use_allocation_2026_09_23/RESULT.md` lines 26 and 100; `decisions/2026-09-23-main-case-general-government-and-use-keys.md` line 42, as read by the Arm 4 worker]

## Net by item, NIBRS murder and robbery (Hispanic ÷ NH white; TX+AZ 2022–23, the lane's central universe)

| Item | Brief's expected direction | Murder (central 2.30) | Robbery (central 4.22) | Evidence |
|---|---|---|---|---|
| Unknown offenders, victim-conditional covariates (15 methods) | up | 2.29–2.42 (−0.5% to +5.0%) | 4.17–4.36 (−1.3% to +3.3%) | Arm 1, NIBRS |
| Arrestee validation of the imputation (3 samples) | — | 2.12–2.24 (−7.9% to −2.8%) | 3.71–4.03 (−12.1% to −4.4%) | Arm 1 |
| Same, SHR national 2024 (lane 2.74) | up | 2.71–2.91 (−1.0% to +6.4%) | — | Arm 1, SHR |
| Clearance gap by victim ethnicity | up | already inside the central (unknowns are allocated within victim group) | same | Arm 1 |
| Reporting to police | up | not applicable | ×0.984 → 4.15 (−1.6%; SE about ±11%) | Arm 3, NCVS 2012–24 |
| White subtraction (the brief's counter item) | down | 0 in this frame; +6.8% in arrest tables | 0 in this frame; +14.0% in arrest tables | Arm 5 |
| Census 2020 coverage, if carried into denominators | down | ×0.935 → 2.15 | ×0.935 → 3.88 | PES [UNVERIFIED carry-through] |
| **Net, leading reading** | | **2.30 (band 2.12–2.42); 2.15 with census** | **4.15 (band 3.65–4.29); 3.88 with census** | derived/ratio_adjustments.csv, arm `net` |

[CALCULATION: ratio_adjustments.py → derived/ratio_adjustments.csv]

On Hispanic ÷ all residents:
- murder: 1.00 (0.96–1.02);
- robbery: 0.92, or 0.96 once reporting is weighed (police data under-show Hispanic offenders among robbers by 5%, against NH Black offenders, whose robberies are reported more).

[CALCULATION: same file]

The understatements the brief lists land on custody, arrests and the survey count, not on these ratios.

## Method

Every arm builds on the finished lanes and edits none of them. The NIBRS lane's code is imported read-only from `offender_ethnicity_nibrs_2026_09_23`, and the victim-cost lane runs through that lane's `victim_cost_rerun.py` helper.

- **Positive control first.** `nibrs_base.py` reproduces the NIBRS lane's `rates_by_spec.csv` (5 specifications × 5 offences) to a max |dRR| of 4.9e-07 [CALCULATION: nibrs_base.py]:

  | Offence | Central | All unknowns non-Hispanic | All unknowns Hispanic |
  |---|---:|---:|---:|
  | Murder | 2.3034 | 1.5311 | 3.9281 |
  | Robbery | 4.2193 | 2.3643 | 9.7471 |

  `test_positive_control.py` holds this check and four more. All five pass. [CALCULATION: pytest, 5 passed]
- **Arm 1, NIBRS.** `nibrs_restage.py` re-stages the TX/AZ/CA 2022–23 zips to victimisation rows carrying:
  - the lane's cell keys, victim age and sex, weapon, gang flag, location and hour;
  - clearance;
  - the 13 fractional offender classes;
  - arrestees by class.

  The rows sum to the lane's staged cells exactly (max |diff| 0).

  `nibrs_impute.py` then replicates the lane's allocation "a" at row level (murder 2.3034, robbery 4.2193, gate PASS) and replaces its cell probabilities with three families of estimates:
  - empirical-Bayes nested cells, `p = (n·p̂ + κ·p_parent)/(n + κ)`, over agency, weapon, victim sex-age, location, hour, gang, and arrest or exceptional clearance, with κ = 5, 20 or 100;
  - multinomial logits;
  - an arrestee fill.

  For race-known, ethnicity-unknown offenders, the logit split uses q_r = P(H)·π(r|H) / (P(H)·π(r|H) + P(NH r)). `nibrs_checks.py` adds the arrestee validation, the booking comparison and the recording-threshold bands.
- **Arm 1, SHR.**
  - `shr_impute.py` uses MAP `SHR76_25a.csv` (sha256 pinned; justifiable homicides excluded, 2019–2024) and reproduces the victim-cost lane's design: P(first offender Hispanic | victim group) from cleared, ethnicity-known cases × 2024 WONDER deaths.
  - Gates: P = 0.719019, 0.102000, 0.048795 and 0.108808, and RR 2.7379, all PASS.
  - The same three families are then applied, and checked by 5-fold cross-validation.
- **Arms 2–3.**
  - **Data.** `ncvs_select.py` uses BJS's NCVS Select files through the open API (`gcuy-rt5g` victimizations, `r4j4-fdwx` population; no login). It gates 2022–24 violent totals, 2024 offence counts, the Hispanic 12+ population and Hispanic reporting rates against *Criminal Victimization, 2024*. It also reproduces NCJ 250747 table 6 (2012–15) to within 0.45 points on reporting and 1.2% on counts. [CALCULATION: ncvs_log.txt]
  - **Pooling.** Rates pool annual victimizations over annual person-years.
  - **Standard errors.** A within-year bootstrap, scaled by the design effect measured against BJS's published SEs (1.29).
  - **Reconciliation with the victim-cost lane.** `ncvs_units.py` reconciles the Select file with the table-13 matrix that lane uses.
- **Arm 4.** The Arm 4 worker's scripts are `jail_share.py`, `jail_bjs_arm.py`, `jail_jurisdictions.py`, `jail_acs_gq.py` and `jail_census_gq.py`; its notes are in `_cache/jail/ARM4_RESULT.md`. I verified the worker's numbers before using them in three ways:
  1. **Primary tables.** Each survey and ASJ pair, and the 2023 count, checked against the saved BJS text (below).
  2. **Re-runs.** All five scripts re-run from cache give byte-identical outputs.
  3. **Hand re-derivation.** The central BJS-arm key re-derived by hand gives 0.2186 × 0.70734 = 0.1546, +$1.541bn (gate in `dollar_effects.py`).
- **Arm 5.** `arm5_white_subtraction.py` runs the route-B construction (`crime_cost_2026_09_16/crime_cost.py`) on NIBRS arrestees beside the true NH-white count. The construction is White × (ethnicity panel ÷ race panel) − all Hispanic.
- **Dollars.**
  - **Victims' harm.** `dollar_effects.py` reproduces the victim-cost central ($28.9229bn full, $4.5014bn tangible), then reruns it once per SHR imputation row and once per mixed-group θ.
  - **Justice key.** The arrest-keyed dollars are linear in the Hispanic arrest ratio. The cj lane's RR→1 sensitivity is −$2.750bn at RR 1.1454, so $21.67bn is keyed on arrests. [DATA: `cj_use_allocation_2026_09_23/derived/summary.json`; CALCULATION: dollar_effects.py]

## Results by arm

### Arm 1: victim-conditional imputation of unknown offenders

**Unknowns do lean Hispanic, through their victims.**
- Among murders with an unknown offender, 42.4% of victims are Hispanic, against 36.3% where the offender is identified.
- Unknown-offender murders are also more often firearm (84.9% against 78.1%), street (28.7% against 18.6%) and night (33.6% against 27.1%).

[DATA: derived/nibrs_unknown_covariate_balance.csv]

The lane's central already allocates unknowns within state-year × offence × victim group, so it absorbs the victim-side lean. What remains is whether other covariates shift the split *within* victim group.

**NIBRS TX+AZ, 794,058 victimisations** [CALCULATION: nibrs_impute.py → derived/nibrs_imputation_specs.csv]:

| Method family | Murder H÷NHW | Robbery | Aggravated assault |
|---|---:|---:|---:|
| central (replicated) | 2.303 | 4.219 | 2.235 |
| one covariate added (7 methods) | 2.294–2.362 | 4.213–4.360 | 2.231–2.295 |
| nested chains (5 methods) | 2.291–2.390 | 4.208–4.344 | 2.258–2.325 |
| multinomial logits (2) | 2.395–2.418 | 4.166–4.182 | 2.293–2.297 |
| arrestee fill | 2.300 | 4.219 | 2.232 |

The upward methods are the ones that condition on agency. Chains with agency first give 2.34–2.39 for murder; the chain with agency last gives 2.29. The same holds in SHR below, where the logit without agency falls to 2.72, and cross-validation shows the agency logit over-predicting the Hispanic share for NH-white victims.

**Arrestee validation** points the other way. 1,267 victimisations have offenders recorded without ethnicity but an arrestee booked with it. In them:
- the arrestees are **20.5%** Hispanic;
- the central imputes **32.9%**;
- the chain and logit impute 29.3% and 29.2%.

The resulting validation factors are:

| Sample | Factor | Murder | Robbery |
|---|---:|---:|---:|
| All agencies | 0.62 | 2.12 | 3.71 |
| Without the 35 booking-discordant agencies | 0.67 | 2.14 | 3.77 |
| Also without Lake Havasu City | 0.87 | 2.24 | 4.03 |

The sample is small and sits mostly in Lake Havasu City, Fort Worth, Gilbert and Harris County, while most unknown mass is in Houston (15.9%), San Antonio (12.9%) and Dallas. Booking also under-records Hispanics (below), which biases this validation down. [CALCULATION: nibrs_checks.py → derived/nibrs_validation_factor.csv, derived/nibrs_validation_adjusted.csv]

Where both segments are recorded, they agree: a single recorded offender and single arrestee pair shows 95.8% Hispanic → Hispanic and 0.2% non-Hispanic → Hispanic. [DATA: derived/nibrs_arrestee_validation.csv]

**SHR national (lane 2.7379 for 2024, 2.7691 for 2022–24):**

| Method family | 2024 | 2022–24 |
|---|---:|---:|
| Single covariates | 2.71–2.78 | 2.74–2.79 |
| Chains | 2.748–2.789 (+0.4% to +1.9%) | 2.815–2.875 |
| Logits | 2.716–2.913 (−0.8% to +6.4%) | 2.780–2.907 |

Hispanic offenders' share of all homicides is 18.8–19.3% against the lane's 19.1% (2024). [CALCULATION: shr_impute.py → derived/shr_imputation_specs.csv]

Cross-validation on known offenders, 2022–24:

| Model | Log-loss | Predicted Hispanic share, NH-white victims (actual 0.1053) | Predicted, California (actual 0.475) |
|---|---:|---:|---:|
| Victim group only | 0.672 | — | 0.373 |
| Chain | 0.646 | 0.1080 | 0.475 |
| Logit | 0.615 | 0.1092 | — |

So the logits' higher ratios come with a 3.7% over-prediction in exactly the cell that drives Hispanic ÷ NH white. [CALCULATION: derived/shr_imputation_cv.csv]

**Clearance does differ by victim ethnicity.**

| Measure | Hispanic victims | NH-white victims | Source |
|---|---:|---:|---|
| Murder, offender identified | 0.890 | 0.918 | NIBRS central agencies |
| Murder, offender ethnicity recorded | 0.772 | 0.854 | NIBRS central agencies |
| Murder, arrest | 0.455 | 0.530 | NIBRS central agencies |
| Robbery, offender identified | 0.871 | 0.848 | NIBRS central agencies |
| Robbery, arrest | 0.182 | 0.230 | NIBRS central agencies |
| SHR homicides solved, 2024 | 0.772 | 0.880 | SHR |
| SHR homicides solved, 2022–24 | 0.725 | 0.868 | SHR |

The brief's 64% against 84% comes from the homicide memo's own window. The gap biases a cleared-only design. It does not bias the central designs, which apply each victim group's cleared distribution to all of that group's victims. [DATA: derived/nibrs_clearance_by_victim.csv; CALCULATION: derived/shr_impute_log.txt]

**The recording-threshold pattern** is composition, not imputation. By agency recording band, murder Hispanic ÷ NH white is:

| Recording band | Hispanic ÷ NH white |
|---|---:|
| [0.50, 0.80) | 3.05 |
| [0.80, 0.95) | 1.86 |
| [0.95, 1.00] | 1.79 |

Allocations a and k show the same slope, while Hispanic ÷ all stays at 0.99–1.03 in every band. [CALCULATION: derived/nibrs_threshold_bands.csv]

### Arm 2: victim survey against police records

**NCVS perceived offender, Hispanic ÷ NH white**, 2012–24, victim-conditional allocation, with design-scaled SE [CALCULATION: ncvs_select.py → derived/ncvs_offender_ratios.csv]:

| Offence | NCVS US | NCVS South+West | NIBRS TX+AZ | NCVS H÷all (US) | NIBRS H÷all |
|---|---:|---:|---:|---:|---:|
| Robbery | 1.80 (0.21) | 1.95 (0.28) | 4.22 | 1.11 (0.10) | 0.92 |
| Aggravated assault | 1.45 (0.12) | 1.23 (0.13) | 2.23 | 1.15 (0.08) | 1.09 |
| Simple assault | 1.04 (0.06) | 0.90 (0.05) | 1.74 | 0.91 (0.04) | 1.10 |
| Rape/sexual assault | 1.32 (0.16) | 1.18 (0.19) | 1.75 | 1.14 (0.10) | 1.18 |

**Geography mismatch.** NCVS identifies only four census regions. Texas and Arizona are two of the many states in its South+West cell, so no NCVS cell matches the NIBRS agencies. [INFERENCE]

**The gap is in the reference group, not the Hispanic numerator.** NH Black ÷ NH white robbery is 5.14 in NCVS against 22.73 in NIBRS, and NCVS's robbery Hispanic ÷ all is *above* NIBRS's. [CALCULATION: derived/ncvs_offender_ratios.csv; DATA: `offender_ethnicity_nibrs_2026_09_23/derived/rates_by_spec.csv`] Police-recorded NH-white robbery in TX+AZ is low relative to every other group. So NCVS does not show that NIBRS understates Hispanic robbery. It shows that the NH-white denominator differs, by construct or place.

**Reconciled: the Select file against table 13.** Hispanic-offender victimizations in the Select file run 19% above the victim-cost lane's table-13 count (2022–24; 2,796k against 2,350k). The cause is BJS's multiple-offender rule, not the unit:
- Table 13 counts a group as Hispanic "where all offenders were perceived to be of Hispanic origin". It puts groups "perceived as various races, including incidents where one or more offenders were perceived as Hispanic" under Other. [SOURCE: *Criminal Victimization, 2024* (NCJ 310547) table 13, footnotes b and c, `ncvs_victim_offender_2026_09_18/_cache/cv24/cv24t13.csv`]
- Row by row, the Select Hispanic excess matches its Other deficit:

  | Victim group | Hispanic excess | Other deficit |
  |---|---:|---:|
  | Black victims | 13.8k | 13.9k |
  | White victims | 263k | 245k |
  | All rows | 446k | 411k |

- The row totals equal N-DASH exactly (1.086, 1.061, 1.075 and 1.085 victimizations per incident).
- The White-offender column matches to 1.003.

[CALCULATION: ncvs_units.py → derived/ncvs_victimizations_per_incident.csv, derived/ncvs_victimization_factor.csv]

For all violent crime 2022–24, Hispanic ÷ NH white is:

| Coding of mixed groups | Hispanic ÷ NH white |
|---|---:|
| Table-13 rule | 0.933 |
| Mixed groups at the NIBRS Hispanic fraction 0.498 | 1.021 |
| Mixed groups at 0.498, matched part only | 1.010 |
| Select coding | 1.110 |

The table-13 figure reproduces the NCVS lane's rates, 13.91 ÷ 14.85 = 0.937. [CALCULATION: derived/ratio_adjustments.csv, arm `2 multiple-offender rule`]

Consequences:
- The NCVS ratios in the first table (Select coding) are upper bounds on the Hispanic side.
- The victim-cost lane's table-13 count is the lower bound. The dollar effect is under Dollars.

### Arm 3: reporting to police

The brief's hypothesis is falsified: crimes with Hispanic victims or offenders are reported *more*.

**All violent crime, 2012–24:**

| Group | Share reported |
|---|---:|
| Hispanic victims | 46.3% (SE 1.6) |
| NH-white victims | 43.4% (0.8) |
| Hispanic-offender crimes | 47.7% (1.9) |
| NH-white-offender crimes | 43.8% (1.0) |
| Within-group Hispanic (victim H / offender H) | 49.0% (2.6) |
| Within-group NH white | 44.7% (1.1) |

[CALCULATION: derived/ncvs_reporting.csv; the gates reproduce CV2024 table 5, 47.8% for 2023 and 48.0% for 2024]

**Robbery** is level: offender H 56.6% (5.0) against NH white 55.7% (3.7).

**Police-visible factor.** This is P(offender Hispanic) among reported crimes over the same among all crimes, for known offenders:

| Offence | Factor (SE) |
|---|---|
| All violent | 1.048 (0.036); 1.130 (0.079) in 2022–24 |
| Robbery | 0.951 (0.074) |
| Aggravated assault | 1.012 (0.061) |
| Simple assault | 1.051 (0.055) |
| Rape and sexual assault | 1.207 (0.161) |

[CALCULATION: derived/ncvs_police_visible_factors.csv]

Weighting police-recorded ratios back to all crimes (rows `3 reporting to police`):

| Offence | 2012–24 | 2022–24 (noisier) |
|---|---|---|
| Robbery | ×0.984 H÷NHW | ×0.854 |
| Aggravated assault | ×0.956 | ×0.797 |

Every row points at police data slightly *over*-showing Hispanic ÷ NH white. Robbery's Hispanic ÷ all rises 5%, because NH Black-offender robberies are reported at 65%. [CALCULATION: derived/ratio_adjustments.csv]

Caveat: the Select file's Hispanic-offender class includes mixed groups (Arm 2).

### Arm 4: jail ethnicity recording (worker's run, verified here)

**Checked against saved primary text:**
- The 2023 jail count: *Jail Inmates in 2023* table 5, 95,700 Hispanic of 664,200 (14.41%). [SOURCE: ji23st.txt line 712, table 5 "Persons held in local jails, by race/ethnicity, 2013–2023"]
- The five self-report surveys against same-year ASJ counts [SOURCE: pji96.txt table 3; pjimy96.txt table 7; pji02.txt table 1; pjim02.txt table 10; svpjri0809.txt table 6; svpjri1112.txt table 7; jim11st.txt, the 2008 and 2011 columns]:

  | Survey | Survey share | Same-year ASJ | Odds ratio |
  |---|---:|---:|---:|
  | SILJ 1989 | 17.4 | 14.3 | 1.262 |
  | SILJ 1996 | 18.5 | 15.6 | 1.228 |
  | SILJ 2002 | 18.5 | 14.7 | 1.317 |
  | NIS-2 | 158,500 / 769,700 = 20.59 | 128,500 / 785,533 = 16.36 | 1.326 |
  | NIS-3 | 159,300 / 712,200 = 22.37 | 113,900 / 735,601 = 15.48 | 1.573 |

- My own arithmetic reproduces each odds ratio and their post-2000 mean, 1.405. [CALCULATION]

**Result.** Applying the mean odds ratio to the 2023 ASJ gives **19.1% (17.1–20.9%)**. BJS's own 2023 prison adjustment gives 19.09%, but it transfers a prison odds ratio of 1.401 from a gated parse of *Prisoners in 2023* appendix table 1. [CALCULATION: jail_share.py → derived/jail_share_estimates.csv]

**Effect on the justice-by-use line.**

| Arm | Key | Δ $bn | Range |
|---|---:|---:|---|
| BJS check, published 14.4% | 0.1428 | — | — |
| BJS check, corrected 19.1% | 0.1546 | **+1.54** against the adopted 0.1419 | +0.93 to +2.09 |
| BJS check at the arrest share (the audit's bound) | — | +2.45 | — |
| ACS custody key ÷ f, f = 0.897 | 0.1583 | **+1.99** | +0.62 to +3.28 over the ACS 2023 one-year rows with federal detention; −0.14 without it; up to +3.79 on the five-year file |

- The adopted prisons key is ACS custody, so the corrected check changes no adopted number.
- The ACS sensitivity is one-sided. f rests on the same survey and SPI inputs as the BJS arm, so the two corrected keys agree partly by construction.

[CALCULATION: jail_bjs_arm.py → derived/jail_bjs_arm.csv (78 rows), derived/jail_acs_key_sensitivity.csv (34 rows)]

**Other sources.**
- **State systems.** Connecticut pretrial runs at 1.8–2.0× adult parity and Delaware at 0.86–0.95×. Both are unified state systems outside the ASJ, so neither calibrates the national correction. Colorado's 2020 county-jail report gives 22% as a floor. [CALCULATION: derived/jail_jurisdictions.csv]
- **Census.** The 2010 census recorded Hispanic prisoners at 0.80 of BJS's adjusted share. [CALCULATION: derived/jail_acs_record_ratio.csv]

Full method list and steel-man: `_cache/jail/ARM4_RESULT.md`.

### Arm 5: the White-subtraction counter item

**In the NIBRS offender frame the construction is absent**, so it contributes 0: classes are disjoint (HW, HB, …, NHW, …, UW, …).

**On NIBRS arrestees**, route B overstates Hispanic ÷ NH white by the amounts below, because 3.4% of Hispanic arrestees (5.4% for robbery) are not coded White:

| Universe | Murder | Robbery | All five offences |
|---|---:|---:|---:|
| TX+AZ central | +6.8% (2.28 → 2.43) | +14.0% (2.95 → 3.36) | +3.8% |
| Adults only | +6.4% | +11.6% | +3.5% |
| Texas, all agencies | +7.4% | +15.3% | +4.2% |
| Arizona, all agencies | +3.3% | +10.8% | +3.6% |
| California | −1.7% | +2.8% | −2.0% |

In California the race-panel rescaling offsets the subtraction; without the rescaling, California gives +2.3% to +3.7%.

The adult White-coded shares reproduce the audit's: AZ 95.46%, TX 96.96% and CA 98.57% here, against 95.5%, 96.9% and 98.6% printed there. The brief's "1–5%" holds for all offences pooled; robbery, with its small NH-white base, runs 11–15%.

The construction feeds `crime_cost_2026_09_16` route B and `nibrs_arrests_2026_09_16`. It feeds no line of the account, because the arrest key is Hispanic ÷ all. [CALCULATION: arm5_white_subtraction.py → derived/arm5_white_subtraction.csv]

### Found on the way

1. **Booking discordance** (in the brief's direction, on arrests).
   - Of 213,452 single-offender, single-arrestee victimisations with both ethnicities recorded, 3,442 offenders recorded Hispanic were booked non-Hispanic, and 252 the other way.
   - The Hispanic share is 38.76% in the offender segment against 37.27% among arrestees, a factor of **1.040**. By subset:

     | Subset | Factor |
     |---|---:|
     | Offenders 18+ | 1.041 |
     | Murder | 1.015 |
     | Robbery | 1.038 |
     | Texas | 1.044 |
     | Arizona | 1.000 |

   - Harris County books 1,681 of 4,389 (38.3%) offender-recorded Hispanics as non-Hispanic; 35 Texas agencies exceed 5%.
   - A Harris County study found arrests 27% Latino against 43% of the county. [CALCULATION: dollar_effects.py → derived/booking_factors.csv; nibrs_checks.py → derived/nibrs_offender_arrestee_discordance.csv; SOURCE: UCI Social Justice Collaboratory, March 2023, p. 10, `_cache/jail/sjc_latinos_in_cjs_march_2023.pdf`]
   - Dropping the discordant agencies moves arrestee murder from 2.28 to 2.53 and robbery from 2.95 to 3.38. Composition changes too, so only the within-incident factor is used for dollars. [CALCULATION: derived/nibrs_arrestee_ratios_booking.csv]
2. **Mixed offender groups** (in the brief's direction, on victims' harm; Arm 2 above).
   - The victim-cost lane named this limit ("Mixed groups fall under 'Other'", its RESULT.md limit 5) but had no microdata to size it. [SOURCE: `crime_victim_cost_2026_09_23/RESULT.md` lines 404–406]
   - In NIBRS TX+AZ, 16,096 victimisations have groups mixing Hispanic and non-Hispanic offenders. Their mean Hispanic fraction is **0.498** (murder 0.495, robbery 0.495). [CALCULATION: derived/nibrs_mixed_group_hispanic_fraction.csv]
3. **Census coverage** (against the brief's direction, on ratios only).
   - The 2020 Post-Enumeration Survey measured a Hispanic net undercount of 4.99% and a non-Hispanic white alone overcount of 1.64% (nation −0.24%, not significant). [SOURCE: Census Bureau press release, 2022-03-10, `_cache/pes/census_pes_2022_03_10.html`]
   - If the ACS denominators inherit it, per-capita Hispanic ÷ NH white is overstated by 7.0%, a factor of 0.935, and Hispanic ÷ all by 5.5%. [CALCULATION]
   - Whether the population-estimates base carries the undercount was not verified [UNVERIFIED].
   - In dollars it cancels: A_T × RR and the victim-cost rates × population both scale with the same count. [INFERENCE]

## Dollars

**Justice key, inside the account** (adopted main case $203.2–249.6bn):

| Item | Δ $bn |
|---|---:|
| Arrest key × 1.0401 (booking, all ages and offences) | **+0.869** |
| Arrest key × 1.0411 (offenders 18+) | +0.890 |
| Arrest key × 1.0439 (Texas only) | +0.951 |
| Arrest key × 1.0150 (murder factor) | +0.326 |
| Arrest key × 1.0003 (Arizona) | +0.006 |
| Prisons, ACS ÷ f at the central f 0.897 | +1.986 |
| Prisons, ACS ÷ f, ACS 2023 one-year rows | −0.135 (no federal detention) to +3.277 |
| Prisons, ACS ÷ f, five-year rows | up to +3.794 |
| Census 2010 prisons analog, f 0.796 (outer) | +4.420 |
| Prisons, BJS check arm | +1.541 on the check, 0 on the main case |
| White subtraction | 0 |
| Census coverage | 0 |
| Offender-ratio imputation (the key does not use NIBRS offender ratios) | 0 |

[CALCULATION: derived/dollar_effects.csv]

The booking row's national transfer is [INFERENCE]. It is zero if national arrest tables book ethnicity as offender segments record it. Arizona's 1.000 shows that not every state books like Texas.

**Victims' harm, beside the account** (victim-cost central $28.92bn full, $4.50bn tangible):

| Item | Full, $bn | Tangible, $bn | Δ full |
|---|---:|---:|---:|
| Mixed groups θ = 0 (lane) | 28.92 | 4.50 | 0 |
| θ = 0.4977 (NIBRS mixed-group fraction) | **30.93** | 4.71 | **+2.00** |
| θ = 0.4977, only the excess matched by the Other deficit | 30.77 | 4.70 | +1.85 |
| θ = 0.5 | 30.94 | 4.71 | +2.01 |
| θ = 1 (Select coding) | 32.95 | 4.93 | +4.03 |
| Murder, 17 SHR imputation rows (2024 window) | 28.85–29.30 | 4.48–4.60 | −0.08 to +0.37 |
| Murder, 2022–24 window rows, against their own lane row ($29.25bn) | — | — | −0.07 to +0.17 |

[CALCULATION: derived/dollar_effects.csv]

- The mixed-group change touches the non-fatal lines only; murder stays at $9.16bn.
- Reporting to police changes nothing here, because the NCVS count already includes unreported crime.

## What would change it

- **A national NIBRS file with both offender and arrestee segments** would replace the TX+AZ booking factor. At Arizona's 1.000 the +$0.87bn goes to 0; if other large sheriffs book like Harris, it rises.
- **Arrestee validation from the agencies holding the unknown mass** (Houston, San Antonio, Dallas) would narrow the murder band. That band is −8% to +5% and set by a sample of 1,267.
- **The NCVS internal file**, with offender counts and each offender's perceived origin, would replace θ = 0.498 (borrowed from police-recorded groups).
- **A jail system publishing self-reported against recorded ethnicity** (Harris County's dashboard is [BLOCKED]) would test the 19.1% directly. The survey correction assumes the 2002–2012 odds ratios hold in 2023.
- **Census Bureau documentation of the estimates base** would settle whether the 6.5% census factor applies at all.

## Limits

- **Geography.** NIBRS is TX+AZ, agencies recording ≥ 50% of offender ethnicity. NCVS is national or regional. SHR is national. No arm puts all three on one footprint.
- **Group.** Everything here is Hispanic, not Mexican-origin. The account scales Hispanic to the target group with its own shares.
- **Perception.** NCVS offender ethnicity is perceived. NIBRS offender ethnicity is recorded, often from victims and witnesses. They measure different things.
- **Validation sample.** The arrestee validation is small, concentrated in four agencies, and biased downward by booking discordance.
- **Arm 4.** The jail correction rests on survey respondents reweighted on administrative race. Survey selection has an unknown direction (NIS-2: 17% refused; `_cache/jail/ARM4_RESULT.md`).
- **Instrument.** This lane was run through an LLM with known dispositions on politically charged topics (`notes/llm-bias-caveat.md`). Every number above regenerates from the scripts, and rows against the leading reading are kept in the CSVs.

## Blocked

- [BLOCKED] Harris County jail by ethnicity: charts.hctx.net/jailpop is an embedded Power BI report with no export.
- [BLOCKED] Cook County Sheriff data page: HTTP 403.
- [BLOCKED] Maricopa County: no primary publication found.
- [BLOCKED] Colorado jail reports after 2020: the report URLs do not resolve, the Tableau export returns 404, and ors.colorado.gov fails DNS.
- [BLOCKED] Arrest shares by ethnicity for CT, DE and CO: CIUS table 69 has no ethnicity; the CDE API was not tried.
- [BLOCKED] data.ojp.gov: DNS failure. Worked around through api.ojp.gov.
- [BLOCKED] NCVS number of offenders: not in the Select file.
- [BLOCKED] A national NIBRS booking comparison: only TX/AZ/CA are staged.
- Not attempted: TX TCJS, CA BSCC, LA County jail data.

## Every specification (method columns)

- **`derived/ratio_adjustments.csv`** (690 rows; the brief's table). One row for each specification below, plus these arms:

  | Arm | Rows |
  |---|---:|
  | `2 multiple-offender rule` | 4 |
  | `3 reporting to police` | 9 |
  | `5 White subtraction` | 53 |
  | `booking discordance` | 40 |
  | `counter-item: census coverage` | 5 |
  | `net` | 16 |

  The `net` rows for murder and robbery are:
  - allocation band low and high;
  - central × reporting;
  - low and high × reporting;
  - central, low and high × reporting × census.
- **`nibrs_imputation_specs.csv`** (16 methods × 5 offences):
  - central (lane allocation a, replicated);
  - one covariate added at κ 20: +agency, +victim sex and age, +weapon, +location, +hour, +gang flag, +arrest and exceptional clearance;
  - chain agency>weapon>victim sex-age>location>hour at κ 5, 20 and 100;
  - chain weapon>victim sex-age>location>hour>agency (κ 20);
  - chain arrest-exc>agency>weapon>victim sex-age (κ 20);
  - multinomial logit, all covariates incl. agency, at C = 1 and C = 0.1;
  - arrestee fill for ethnicity-unknown offenders, else central.
- **`nibrs_validation_adjusted.csv`**:
  - central;
  - validation-adjusted, all agencies (factor 0.62);
  - without booking-discordant agencies (0.67);
  - also without Lake Havasu City (0.87).
- **`shr_imputation_specs.csv`** (windows 2024 and 2022_2024, 18 methods each):
  - victim lane (cleared, ethnicity-known, by victim group);
  - victim group only with race-known splits;
  - single covariates: +state, +weapon, +victim age and sex, +circumstance class, +situation (multiple victims);
  - chains: state>weapon>victim age-sex>agency at κ 20, 5 and 100; state>agency>weapon>victim age-sex; state>circumstance>weapon>victim age-sex;
  - multinomial logits: all covariates incl. state and agency at C = 1 and C = 0.1; without circumstance; without circumstance or agency; without circumstance with victim-group interactions;
  - solved only, ethnicity-missing split within race by state.
- **`shr_imputation_cv.csv`**:
  - models: victim group only; chain state>weapon>victim age-sex>agency; logit all covariates; logit without circumstance; logit without circumstance with victim-group interactions;
  - strata: all known, circumstance undetermined, weapon unknown, victim Hispanic, victim NH white, California, Texas.
- **`ncvs_offender_ratios.csv`** (432 rows): years {2012–2024, 2017–2024, 2022–2024} × region {US, South+West, South, West} × allocation {victim, known, b, c, victim reported to police only, victim not reported only} × 6 offence groups.
- **Other NCVS files**:
  - `ncvs_reporting.csv`: 3 windows × 6 offences × victim, offender and pair groups;
  - `ncvs_police_visible_factors.csv`: 2 windows × 5 offences × 5 victim groups × {p_all, p_reported, factor, rep_H, rep_NHW};
  - `ncvs_control_rhovo_t6.csv`;
  - `ncvs_victimizations_per_incident.csv`: 2022, 2023, 2024 and pooled, victim × offender cells, rows and columns;
  - `ncvs_victimization_factor.csv`.
- **Arrestee and booking files**:
  - `nibrs_arrestee_ratios_booking.csv`: universes all central agencies, without discordant agencies, without Harris only; × all ages and adults;
  - `booking_factors.csv`: the 7 universes in the Dollars table;
  - `nibrs_offender_arrestee_discordance.csv`: by agency;
  - `nibrs_threshold_bands.csv`: 4 bands × allocations a, k, b, c;
  - `nibrs_arrestee_validation.csv`, `nibrs_clearance_by_victim.csv`, `nibrs_unknown_covariate_balance.csv`, `nibrs_mixed_group_hispanic_fraction.csv`.
- **`arm5_white_subtraction.csv`**: 4 universes (TX+AZ central, TX, AZ, CA) × 2 ages × 6 offence rows, with route-B and no-rescale constructions.
- **`dollar_effects.csv`** (110 rows):
  - 36 SHR murder rows;
  - 5 mixed-group rows;
  - 7 booking rows;
  - White-subtraction and census rows;
  - 26 BJS check-arm jail methods;
  - 34 ACS ÷ f rows.
- **Arm 4 worker files**:
  - `jail_share_estimates.csv`: 26 methods, listed in `_cache/jail/ARM4_RESULT.md`;
  - `jail_bjs_arm.csv`: 26 methods × overlap rules none, prison_share and jail_share;
  - `jail_acs_key_sensitivity.csv`: 34 rows;
  - `jail_acs_record_ratio.csv`, `jail_jurisdictions.csv`, `jail_acs_gq.csv`, `jail_acs_adults.csv`, `jail_census_gq.csv` (1.6 MB of county rows; trim before committing if unwanted), `jail_census2020_counties.csv`, `jail_state_comparison_2019.csv`, `jail_share_summary.json`.

## Reproduce (repository root)

```sh
L=infra/immigration-fiscal/crime_ratio_direction_2026_09_24
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/nibrs_base.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/nibrs_restage.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn python3 $L/nibrs_impute.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn python3 $L/nibrs_checks.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn python3 $L/shr_impute.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/ncvs_select.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/ncvs_units.py
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
for s in jail_acs_gq jail_census_gq; do OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 $L/$s.py 2>&1 | sed 's/key=[^&]*/key=REDACTED/g'; done
for s in jail_share jail_bjs_arm jail_jurisdictions; do OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 $L/$s.py; done
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/arm5_white_subtraction.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn python3 $L/dollar_effects.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 $L/ratio_adjustments.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn --with pytest python3 -m pytest $L/ -q
```

Every script is cache-first. Raw pulls are in `_cache/` (ignored); the NIBRS zips and stages are read in place from `offender_ethnicity_nibrs_2026_09_23/_cache/`. The first run of `ncvs_select.py` fetches the two NCVS Select files with curl. Runtime is about 5.5 minutes, most of it the bootstrap.

**Covered:** all five arms, the positive control, the booking, mixed-group and census items, and dollars for both lines.

**Not covered:** the NIBRS-lane cost arms (`victim_cost_rerun.py` arms that use NIBRS national shares). These move in proportion to the Arm 1 national shares in `nibrs_imputation_specs.csv`; they are not the victim-cost central, and they are not re-costed here.

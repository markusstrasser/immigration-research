**Verdict:** Police records show that NCVS victims under-perceive Hispanic offending. They also
show that Hispanic offenders' victims are mostly Hispanic, far more than the NCVS matrix has
them. The two corrections nearly cancel. On police-recorded inputs, the 2024 victim cost to
other residents is **$28.6bn full and $4.4bn tangible**, against the victim lane's NCVS central
of $28.9bn and its arrest-share arm of $43.1bn [CALCULATION: `victim_cost_rerun.py` →
`derived/cost_arms.csv`].

The data are Texas and Arizona, 2022–2023. NIBRS agencies cover all of Texas's population and
61–64% of Arizona's.
There, Hispanic residents aged 12+ offend at 1.7–2.3 times the non-Hispanic white rate for
murder, rape and assault, and 4.2 times for robbery. Against all residents the ratio is
0.92–1.18. Assigning every offender of unknown ethnicity to one side bounds the white ratios at
1.25–9.75 [DATA: `derived/rates_by_spec.csv`].

Carried to the nation, Hispanic offenders commit 19–24% of 2024 non-fatal violent
victimisations (bounds 13–35%). The NCVS perception puts it at 14–18% and 2019 arrests at
18–29% [CALCULATION]. But 70–81% of Hispanic offenders' victims in Texas and Arizona are
Hispanic. Carried to national residential patterns that becomes 62–73%, against about 40% in
the NCVS matrix [DATA; CALCULATION].

Two structures agree with each other. The preferred one puts NIBRS's offender-given-victim
shares, calibrated to national SHR homicide, on NCVS's self-reported victim counts. It gives
$24.8–30.3bn across 20 specifications. Taking both offender and victim shares from NIBRS gives
$29.4bn ($24.3–37.4bn).

Changing only the offending share, as the $43.1bn arm does, gives **$40.0bn** ($32.3–52.0bn).
That was this lane's pre-planned central. It fails an adding-up check against NCVS victim
counts: it implies Hispanic offenders commit about 16% of assaults on non-Hispanic victims
nationally, about twice what police records support. The $43.1bn arm fails the same check
[CALCULATION: `derived/consistency_with_ncvs_victims.csv`].

On the custody footing (institutional ratio 1.118), the preferred arm gives $32.0bn against
the lane's $32.3bn. The structure choice is the parent's; see "What the parent must check".

Model self-report: claude-opus-5-5[1m]. Lane `infra/immigration-fiscal/offender_ethnicity_nibrs_2026_09_23/`,
September 23, 2026. Nothing committed.

## Headline

| 2024, $bn a year, cost to other residents | Tangible | Full | Outside non-fatal victims |
|---|---:|---:|---:|
| Victim lane central (NCVS perceived offenders) | 4.50 | 28.92 | 401,735 |
| Victim lane arrest-share arm (2019 adult arrests, NCVS victim mix) | 5.60 | 43.12 | 577,464 |
| **Preferred: victim-conditional, SHR-calibrated (NIBRS)** | **4.37** | **28.59** | 365,485 |
| same, calibrated to SHR 2022–2024 instead of 2024 | 4.45 | 29.39 | 379,831 |
| same, range over 20 specifications, allocation bounds included | 4.02–4.50 | 24.82–30.32 | |
| Offender share and victim mix both from NIBRS | 4.44 | 29.40 | 384,370 |
| same, range over 27 specifications | 3.95–5.27 | 24.31–37.39 | |
| Victim-conditional, uncalibrated | 4.04 | 25.39 | 304,684 |
| same, range over 20 specifications | 3.75–5.51 | 22.39–39.92 | |
| Offender share only, NCVS victim mix kept (pre-planned; like for like with the arrest arm) | 5.49 | 40.04 | 597,695 |
| same, range over 27 specifications | 4.75–6.68 | 32.32–51.98 | |
| Arrest-calibrated translation: offender share only / with NIBRS victim mix | 6.13 / 4.88 | 46.64 / 33.75 | 706,146 / 456,220 |
| Custody footing (ACS institutional ratio 1.118): preferred arm / victim lane | 4.88 / 5.03 | 31.97 / 32.34 | |

[CALCULATION: `derived/cost_arms.csv`; the two reference rows reproduce the victim lane's
published values (gates in `derived/cost_log.txt`)] Murder is $9.16bn in every row: homicide stays on
the victim lane's WONDER × SHR inputs, as the brief requires. In the preferred arm murder is
32% of the full cost, $699 full and $107 tangible per group member (÷ 40,896,574)
[CALCULATION].

## Data and coverage

**Route.** The FBI Crime Data Explorer serves state NIBRS files at
`nibrs/incident/{year}/{ST}-{year}.zip` through its signed-URL store, with **no API key**. The
key layout comes from the 2025-02-08 archive.org mirror `fbi-cde` and was confirmed live
[SOURCE: `fetch_nibrs.py`; sizes and sha256 in `derived/source_manifest.csv`]. The victim and
homicide lanes' limit, that CDE data after 2019 need an API key, does not apply to this bulk
store. Texas, Arizona and California files for 2022 and 2023 total 456 MB. A disk preflight ran before each
download, with 40–43 GB free. The FBI participation file and the CDE agency lists came from the
same store. Tables used: `agencies`, `NIBRS_month`, `incident`, `OFFENSE`, `OFFENDER`,
`VICTIM`, `VICTIM_OFFENSE`, `ARRESTEE`.

| State-year | NIBRS agencies | Population covered, all agencies | Covered, agencies recording ethnicity ≥ 50% | Hispanic residents covered (≥ 50%) | Mexican share of covered Hispanics | Violent victimisations in ≥ 50% agencies | Target incidents | Victimisations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TX 2022 | 1,063 | 1.006 | 0.931 | 0.898 | 0.813 | 0.928 | 430,077 | 491,358 |
| TX 2023 | 1,362 | 1.013 | 0.969 | 0.965 | 0.810 | 0.953 | 429,958 | 490,584 |
| AZ 2022 | 89 | 0.605 | 0.430 | 0.338 | 0.829 | 0.707 | 48,139 | 58,654 |
| AZ 2023 | 92 | 0.637 | 0.507 | 0.433 | 0.842 | 0.786 | 51,490 | 63,168 |
| CA 2022 | 559 | 0.417 | 0.284 | 0.278 | 0.857 | 0.712 | 164,645 | 197,408 |
| CA 2023 | 630 | 0.610 | 0.442 | 0.434 | 0.850 | 0.746 | 256,431 | 305,672 |

[DATA: `derived/coverage_by_state_year.csv`] Coverage is FBI population × months reported ÷ 12,
summed over non-tribal agencies, divided by the ACS 5-year state population. Overlapping
jurisdictions push Texas slightly above 1. The FBI participation file gives 98.6% and 99.2% for
Texas, 62.2% and 62.6% for Arizona, and 54.0% and 64.3% for California; it counts agencies,
not months [DATA: `_cache/ucr_participation_1960_2025.csv`; gate: Texas within 5%]. Phoenix
PD, Tucson PD and the Maricopa sheriff are missing from Arizona 2022. "Target" incidents
contain at least one of the five offences or intimidation (13C); these two columns count every
victim type and all agencies.

**California stays a sensitivity.** Only 28–44% of its population is covered by agencies that
record offender ethnicity for at least half of offenders. Offender ethnicity is recorded for
51–64% of its victimisations by offence, against 68–87% in Texas (all agencies) [DATA: `derived/unknown_offender_shares.csv`].
It enters as `states=CA` and `states=TX+AZ+CA`.

**Mexican origin (ACS 1-year B03001).** Of Hispanic residents, 80.2% (2022) and 79.6% (2023)
are of Mexican origin in Texas, 85.3% and 86.1% in Arizona, and 80.6% and 80.3% in California.
Within the agencies recording ethnicity the shares are 81% in Texas, 83–84% in Arizona and
85–86% in California [DATA: `derived/acs1_state_b03001.csv`,
`derived/coverage_by_state_year.csv`]. The brief's "about 85–90%" holds for Arizona only.
NIBRS records Hispanic ethnicity only, so every rate below is for Hispanic residents of any
origin. The victim lane's population-share step from Hispanic to Mexican origin (s = 0.5975)
is kept unchanged.

## Offending rates, Texas and Arizona 2022–2023 (central)

**Numerator.** Victimisations of individuals aged 12+ (the NCVS universe), by offence:
- murder 09A;
- rape and sexual assault 11A–11D;
- robbery 120;
- aggravated assault 13A;
- simple assault 13B.

A victim hit by several of these offences in one incident counts once, at the most serious.
Each recorded offender carries 1/n of the victimisation.

**Groups.** Groups are disjoint: Hispanic of any race, then non-Hispanic white, Black and other.
Raw "White" is never used.

**Denominator.** Residents aged 12+ of the covered jurisdictions. For each agency this is the
FBI population × months ÷ 12 × the ACS 5-year composition of its place, or of its county net of
every city with its own police. Only agencies recording offender ethnicity for at least half of
known offenders enter.

**Unknowns.** Offenders who are unknown, or recorded without ethnicity, are allocated in
proportion to recorded offenders, within state-year × offence × victim ethnicity, and within
recorded race. Bounds (b) and (c) assign them all non-Hispanic or all Hispanic.

**National translation.** Relative rates carry to the national 2024 population aged 12+:
`S = RR_H·P_H / Σ_g RR_g·P_g`. The assumption is that Texas–Arizona relative rates hold
nationally [INFERENCE]. [CALCULATION: `nibrs_rates.py`]

| Offence | Victimisations | Per 100,000 aged 12+ a year: Hispanic / NH white / all | Hispanic vs NH white (b–c) | Hispanic vs all residents (b–c) | NH Black vs NH white | Hispanic share of offending, TX+AZ (b–c) | National Hispanic share (b–c) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Murder | 3,810 | 7.3 / 3.1 / 7.2 | **2.30** (1.53–3.93) | 1.00 (0.78–1.41) | 8.63 | 0.357 (0.279–0.502) | **0.202** (0.149–0.314) |
| Rape/sexual assault | 36,730 | 82.4 / 47.2 / 69.8 | **1.75** (1.25–2.79) | 1.18 (0.98–1.50) | 3.26 | 0.421 (0.350–0.537) | **0.239** (0.188–0.334) |
| Robbery | 49,966 | 87.1 / 20.6 / 95.0 | **4.22** (2.36–9.75) | 0.92 (0.66–1.50) | 22.73 | 0.327 (0.237–0.536) | **0.188** (0.128–0.354) |
| Aggravated assault | 170,185 | 352.2 / 157.6 / 323.5 | **2.23** (1.42–3.75) | 1.09 (0.84–1.45) | 6.76 | 0.388 (0.301–0.518) | **0.222** (0.162–0.326) |
| Simple assault | 533,367 | 1,111.8 / 638.2 / 1,013.7 | **1.74** (1.46–2.24) | 1.10 (1.00–1.26) | 4.24 | 0.391 (0.357–0.451) | **0.220** (0.195–0.265) |

[CALCULATION: `derived/rates_by_spec.csv`, specs `central`, `alloc=b`, `alloc=c`] Hispanic
residents are 0.357 of the covered population aged 12+ and 0.187 of the national population
aged 12+ (NCVS 2024: 53,539,670 of 286,373,220) [DATA: `derived/national_populations.csv`].

Set against the victim lane's cross-check, NIBRS's non-fatal ratios (1.74–4.22) sit far above
the NCVS perceived ratio of 0.94. The homicide ratio of 2.30 is near the lane's WONDER × SHR
homicide ratio of 2.74 and BJS's 2023 adult imprisonment ratio of 2.62 [SOURCE:
`../crime_victim_cost_2026_09_23/RESULT.md`, cross-check table].

These are crude rates per resident aged 12+, with no age standardisation. The cost calculation
needs crude rates, because it counts offences that happen. Any reading of the ratio as
propensity at equal age would need standardisation, which this lane did not do [INFERENCE].

### Every specification

Each cell gives the Hispanic ÷ non-Hispanic white rate, then the national Hispanic share.

| Specification | Murder | Rape/sexual assault | Robbery | Aggravated assault | Simple assault |
|---|---:|---:|---:|---:|---:|
| central (TX+AZ, 2022–2023, fractional attribution, allocation a, agencies ≥ 50%) | 2.30 / 0.202 | 1.75 / 0.239 | 4.22 / 0.188 | 2.23 / 0.222 | 1.74 / 0.220 |
| alloc=a0 (proportional at offence level) | 2.19 / 0.203 | 1.77 / 0.243 | 4.27 / 0.195 | 2.18 / 0.219 | 1.76 / 0.221 |
| alloc=b (unknowns all non-Hispanic) | 1.53 / 0.149 | 1.25 / 0.188 | 2.36 / 0.128 | 1.42 / 0.162 | 1.46 / 0.195 |
| alloc=c (unknowns all Hispanic) | 3.93 / 0.314 | 2.79 / 0.334 | 9.75 / 0.354 | 3.75 / 0.326 | 2.24 / 0.265 |
| alloc=k (recorded offenders only) | 2.18 / 0.202 | 1.82 / 0.246 | 4.31 / 0.195 | 2.18 / 0.219 | 1.77 / 0.222 |
| agencies: ethnicity recorded ≥ 0% | 2.23 / 0.200 | 1.72 / 0.236 | 4.11 / 0.185 | 2.21 / 0.221 | 1.73 / 0.219 |
| agencies: ethnicity recorded ≥ 80% | 1.83 / 0.190 | 1.56 / 0.223 | 3.11 / 0.189 | 1.90 / 0.217 | 1.71 / 0.220 |
| agencies: ethnicity recorded ≥ 95% | 1.79 / 0.183 | 1.44 / 0.208 | 2.56 / 0.194 | 1.82 / 0.216 | 1.66 / 0.214 |
| agencies: offender-ethnicity start date by 1 January | 2.37 / 0.206 | 1.78 / 0.244 | 4.31 / 0.190 | 2.29 / 0.226 | 1.73 / 0.220 |
| agencies: 12 months reported | 2.32 / 0.204 | 1.75 / 0.241 | 4.20 / 0.188 | 2.23 / 0.222 | 1.73 / 0.220 |
| states=TX | 2.32 / 0.204 | 1.79 / 0.245 | 4.15 / 0.189 | 2.26 / 0.226 | 1.75 / 0.224 |
| states=AZ | 2.04 / 0.183 | 1.61 / 0.182 | 3.93 / 0.187 | 1.92 / 0.186 | 1.64 / 0.175 |
| states=CA | 2.81 / 0.201 | 2.18 / 0.232 | 2.79 / 0.153 | 1.94 / 0.192 | 1.68 / 0.188 |
| states=TX+AZ+CA | 2.41 / 0.201 | 1.87 / 0.243 | 3.56 / 0.189 | 2.15 / 0.219 | 1.71 / 0.212 |
| year=2022 | 2.21 / 0.203 | 1.70 / 0.241 | 4.08 / 0.189 | 2.29 / 0.225 | 1.69 / 0.216 |
| year=2023 | 2.42 / 0.201 | 1.79 / 0.238 | 4.37 / 0.187 | 2.18 / 0.220 | 1.79 / 0.224 |
| attribution=first (first offender carries all) | 2.28 / 0.202 | 1.75 / 0.239 | 4.22 / 0.187 | 2.25 / 0.223 | 1.74 / 0.220 |
| attribution=anyH (Hispanic if any offender is) | 2.64 / 0.221 | 1.78 / 0.243 | 5.32 / 0.215 | 2.37 / 0.232 | 1.84 / 0.229 |
| attribution=allH (Hispanic only if all are; the NCVS rule since 2021) | 2.00 / 0.184 | 1.71 / 0.236 | 3.32 / 0.162 | 2.10 / 0.213 | 1.65 / 0.211 |
| victims: all ages | 2.30 / 0.204 | 1.71 / 0.244 | 4.23 / 0.188 | 2.24 / 0.223 | 1.74 / 0.220 |
| victims: individuals + officers | 2.30 / 0.202 | 1.75 / 0.239 | 4.22 / 0.188 | 2.22 / 0.223 | 1.73 / 0.219 |
| denominator: all ages (national: Census NC-EST2024) | 2.09 / 0.205 | 1.58 / 0.243 | 3.83 / 0.190 | 2.03 / 0.225 | 1.58 / 0.223 |
| simple assault incl. intimidation 13C | 2.30 / 0.202 | 1.75 / 0.239 | 4.22 / 0.188 | 2.23 / 0.222 | 1.72 / 0.214 |
| translation: rate vs all residents × national population share | 2.30 / 0.187 | 1.75 / 0.221 | 4.22 / 0.171 | 2.23 / 0.204 | 1.74 / 0.205 |
| incidents with an arrest only | 2.10 / 0.188 | 2.00 / 0.264 | 3.07 / 0.206 | 1.86 / 0.213 | 1.59 / 0.218 |
| states=TX+AZ+CA, alloc=b | 1.44 / 0.138 | 1.22 / 0.179 | 1.85 / 0.122 | 1.33 / 0.156 | 1.37 / 0.182 |
| states=TX+AZ+CA, alloc=c | 4.16 / 0.315 | 3.07 / 0.344 | 7.88 / 0.347 | 3.58 / 0.320 | 2.25 / 0.259 |

Hispanic rate ÷ rate of all residents, by specification:

| Specification | Murder | Rape/sexual assault | Robbery | Aggravated assault | Simple assault |
|---|---:|---:|---:|---:|---:|
| central | 1.00 | 1.18 | 0.92 | 1.09 | 1.10 |
| alloc=a0 | 1.01 | 1.20 | 0.95 | 1.08 | 1.10 |
| alloc=b | 0.78 | 0.98 | 0.66 | 0.84 | 1.00 |
| alloc=c | 1.41 | 1.50 | 1.50 | 1.45 | 1.26 |
| alloc=k | 1.01 | 1.21 | 0.95 | 1.08 | 1.10 |
| agencies: ethnicity recorded ≥ 0% | 1.01 | 1.18 | 0.93 | 1.10 | 1.10 |
| agencies: ethnicity recorded ≥ 80% | 1.01 | 1.15 | 1.01 | 1.12 | 1.14 |
| agencies: ethnicity recorded ≥ 95% | 0.99 | 1.08 | 1.03 | 1.11 | 1.11 |
| agencies: offender-ethnicity start date by 1 January | 1.01 | 1.20 | 0.92 | 1.10 | 1.10 |
| agencies: 12 months reported | 1.00 | 1.18 | 0.91 | 1.09 | 1.09 |
| states=TX | 0.97 | 1.18 | 0.87 | 1.06 | 1.08 |
| states=AZ | 1.37 | 1.25 | 1.61 | 1.32 | 1.21 |
| states=CA | 1.36 | 1.40 | 1.21 | 1.29 | 1.25 |
| states=TX+AZ+CA | 1.08 | 1.25 | 1.03 | 1.16 | 1.13 |
| year=2022 | 1.01 | 1.19 | 0.92 | 1.09 | 1.08 |
| year=2023 | 1.00 | 1.17 | 0.92 | 1.08 | 1.11 |
| attribution=first | 1.00 | 1.18 | 0.91 | 1.09 | 1.10 |
| attribution=anyH | 1.07 | 1.19 | 1.02 | 1.12 | 1.13 |
| attribution=allH | 0.93 | 1.17 | 0.81 | 1.05 | 1.06 |
| victims: all ages | 1.01 | 1.20 | 0.92 | 1.09 | 1.10 |
| victims: individuals + officers | 1.00 | 1.18 | 0.92 | 1.09 | 1.09 |
| denominator: all ages | 0.95 | 1.12 | 0.87 | 1.04 | 1.04 |
| simple assault incl. intimidation 13C | 1.00 | 1.18 | 0.92 | 1.09 | 1.07 |
| translation: rate vs all residents | 1.00 | 1.18 | 0.92 | 1.09 | 1.10 |
| incidents with an arrest only | 0.95 | 1.27 | 1.00 | 1.06 | 1.10 |
| states=TX+AZ+CA, alloc=b | 0.81 | 0.99 | 0.73 | 0.89 | 1.01 |
| states=TX+AZ+CA, alloc=c | 1.50 | 1.59 | 1.59 | 1.52 | 1.31 |

[CALCULATION: `derived/rates_by_spec.csv`; the log is `derived/rates_log.txt`]

Outside the allocation bounds, the national Hispanic share stays within 0.15–0.26.

Raising the recording threshold to 95% lowers every Hispanic ÷ white ratio (robbery
4.22 → 2.56, murder 2.30 → 1.79, simple assault 1.74 → 1.66). It moves the national shares by at
most 3 points, because the white and Black rates move with it [CALCULATION].

## Unknown ethnicity and recording

| Agencies | State | Offence | Victimisations | No offender recorded | Offender recorded, ethnicity unknown | … of which recorded race White | Ethnicity recorded |
|---|---|---|---:|---:|---:|---:|---:|
| central (≥ 50%) | TX | Murder | 3,548 | 0.098 | 0.131 | 0.016 | 0.770 |
| central (≥ 50%) | TX | Rape/sexual assault | 32,579 | 0.040 | 0.120 | 0.034 | 0.840 |
| central (≥ 50%) | TX | Robbery | 47,671 | 0.126 | 0.169 | 0.021 | 0.705 |
| central (≥ 50%) | TX | Aggravated assault | 157,213 | 0.111 | 0.103 | 0.022 | 0.786 |
| central (≥ 50%) | TX | Simple assault | 482,740 | 0.030 | 0.054 | 0.025 | 0.915 |
| central (≥ 50%) | AZ | Murder | 262 | 0.053 | 0.086 | 0.045 | 0.860 |
| central (≥ 50%) | AZ | Rape/sexual assault | 4,151 | 0.180 | 0.213 | 0.071 | 0.608 |
| central (≥ 50%) | AZ | Robbery | 2,295 | 0.244 | 0.139 | 0.042 | 0.617 |
| central (≥ 50%) | AZ | Aggravated assault | 12,972 | 0.124 | 0.121 | 0.055 | 0.755 |
| central (≥ 50%) | AZ | Simple assault | 50,627 | 0.075 | 0.108 | 0.061 | 0.817 |
| all | TX | Murder | 3,710 | 0.097 | 0.155 | 0.038 | 0.748 |
| all | TX | Rape/sexual assault | 34,869 | 0.041 | 0.160 | 0.066 | 0.800 |
| all | TX | Robbery | 49,640 | 0.130 | 0.189 | 0.038 | 0.681 |
| all | TX | Aggravated assault | 166,245 | 0.112 | 0.137 | 0.050 | 0.751 |
| all | TX | Simple assault | 514,866 | 0.031 | 0.101 | 0.063 | 0.868 |
| all | AZ | Murder | 348 | 0.098 | 0.223 | 0.147 | 0.679 |
| all | AZ | Rape/sexual assault | 5,059 | 0.186 | 0.291 | 0.134 | 0.523 |
| all | AZ | Robbery | 2,886 | 0.264 | 0.223 | 0.101 | 0.513 |
| all | AZ | Aggravated assault | 16,241 | 0.136 | 0.228 | 0.139 | 0.636 |
| all | AZ | Simple assault | 63,419 | 0.075 | 0.232 | 0.157 | 0.693 |
| all | CA | Murder | 1,516 | 0.166 | 0.316 | 0.159 | 0.519 |
| all | CA | Rape/sexual assault | 23,425 | 0.119 | 0.374 | 0.230 | 0.507 |
| all | CA | Robbery | 40,286 | 0.178 | 0.302 | 0.122 | 0.519 |
| all | CA | Aggravated assault | 111,247 | 0.120 | 0.289 | 0.174 | 0.592 |
| all | CA | Simple assault | 225,609 | 0.051 | 0.304 | 0.206 | 0.644 |

[DATA: `derived/unknown_offender_shares.csv`; shares of victimisations, 2022–2023 pooled]

Unknowns are not random. Offenders with no record at all concentrate in robbery, aggravated
assault and murder, where offenders go unidentified, and in rape in Arizona. Offenders recorded
as White with unknown ethnicity are the class most likely to hide Hispanic offenders
[INFERENCE]. They are 1.6–3.4% of victimisations in the central Texas agencies and 4.2–7.1% in
Arizona's [DATA].

Share of violent victimisations by the agency's rate of recording offender ethnicity (all
offences, known offenders):

| State-year | ≈ 0 | (0, 0.25] | (0.25, 0.5] | (0.5, 0.8] | (0.8, 0.95] | (0.95, 1] |
|---|---:|---:|---:|---:|---:|---:|
| TX 2022 | 0.035 | 0.027 | 0.009 | 0.524 | 0.254 | 0.151 |
| TX 2023 | 0.003 | 0.024 | 0.020 | 0.338 | 0.404 | 0.212 |
| AZ 2022 | 0.123 | 0.036 | 0.078 | 0.323 | 0.322 | 0.118 |
| AZ 2023 | 0.015 | 0.050 | 0.116 | 0.343 | 0.378 | 0.098 |
| CA 2022 | 0.197 | 0.033 | 0.057 | 0.331 | 0.370 | 0.013 |
| CA 2023 | 0.181 | 0.025 | 0.047 | 0.405 | 0.307 | 0.035 |

[DATA: `derived/recording_rate_distribution.csv`; agency rates in `derived/agency_recording_rates.csv`]
The threshold sensitivity (0%, 50% central, 80%, 95%) is in the specification tables above.

## Incident offenders and arrestees

| Offence | Arrestees, all ages: Hispanic ÷ NH white (b–c) | Incident offenders: Hispanic ÷ NH white | Arrestees: Hispanic share, TX+AZ | Offenders: Hispanic share, TX+AZ | Adult arrestees: Hispanic ÷ NH white (b–c) |
|---|---:|---:|---:|---:|---:|
| Murder | 2.28 (2.09–2.55) | 2.30 | 0.355 | 0.357 | 2.18 (2.01–2.45) |
| Rape/sexual assault | 1.76 (1.62–1.93) | 1.75 | 0.445 | 0.421 | 2.00 (1.85–2.16) |
| Robbery | 2.95 (2.68–3.23) | 4.22 | 0.357 | 0.327 | 2.74 (2.53–3.00) |
| Aggravated assault | 1.65 (1.54–1.81) | 2.23 | 0.365 | 0.388 | 1.71 (1.60–1.87) |
| Simple assault | 1.49 (1.40–1.63) | 1.74 | 0.378 | 0.391 | 1.52 (1.44–1.66) |

[CALCULATION: `derived/arrestee_rates.csv`, `derived/offenders_vs_arrestees.csv`] Arrestees'
ethnicity is unknown for only 2.9–4.0%, so their bounds are tight.

For murder and rape, arrestees and incident offenders agree. For robbery, aggravated
assault and simple assault, incident offenders give higher Hispanic ratios than arrestees. Recording ethnicity from
victims' descriptions for non-arrested offenders could inflate those ratios, but the
"incidents with an arrest only" specification gives robbery 3.07 and aggravated assault 1.86,
closer to the arrestee values (2.95 and 1.65). Differential clearance could also produce the gap. The data
cannot separate the two [INFERENCE].

**Translation check against national arrests.** The same national translation, applied to
Texas–Arizona adult arrestees, can be compared with FBI 2023 national arrest shares by
ethnicity (Table 43C, held by the arrests lane):

| Offence | Adult arrestees | Ethnicity unknown | Hispanic ÷ NH white | Translated national share | FBI 2023 Table 43C share | Difference |
|---|---:|---:|---:|---:|---:|---:|
| Murder | 1,821 | 0.040 | 2.18 | 0.191 | 0.217 | −0.026 |
| Rape/sexual assault | 3,452 | 0.035 | 2.00 | 0.265 | 0.309 | −0.044 |
| Robbery | 7,620 | 0.029 | 2.74 | 0.194 | 0.266 | −0.072 |
| Aggravated assault | 45,832 | 0.031 | 1.71 | 0.200 | 0.266 | −0.066 |
| Simple assault | 145,585 | 0.031 | 1.52 | 0.205 | 0.228 | −0.023 |

[CALCULATION: `derived/translation_check_arrests_vs_table43c.csv`; national adults from Census
NC-EST2024, July 2023] The translation under-predicts national Hispanic arrest shares by 2.3–7.2
points. Two explanations fit, and this lane cannot separate them:
- Table 43C covers only agencies that report ethnicity, and that panel may over-weight
  high-Hispanic areas.
- Hispanic relative offending may be higher outside Texas and Arizona.

The "arrest-calibrated translation" arms scale each national share by the ratio of FBI share to
translated share (1.11–1.37). They are an upper sensitivity. The 2023 Table 43C shares run above
the 2019 shares used by the victim lane's arrest arm, which would push that arm above $43.1bn
[INFERENCE].

## Homicide: NIBRS against the SHR (check only)

| Source, 2022–2023 | State | Victims | Cleared, offender ethnicity known | Hispanic share of offenders | P(offender Hispanic \| victim Hispanic) | P(offender Hispanic \| victim NH white) | Hispanic share of Hispanic offenders' victims |
|---|---|---:|---:|---:|---:|---:|---:|
| SHR (MAP) | Texas | 3,815 | 2,781 | 0.354 | 0.730 | 0.164 | 0.743 |
| NIBRS 09A, first offender | Texas | 3,859 | 2,869 | 0.370 | 0.747 | 0.164 | 0.788 |
| SHR (MAP) | Arizona | 893 | 577 | 0.409 | 0.730 | 0.206 | 0.653 |
| NIBRS 09A, first offender | Arizona | 421 | 264 | 0.333 | 0.704 | 0.121 | 0.695 |

[DATA: `derived/homicide_check_nibrs_vs_shr.csv`; SHR sha256 gated against the homicide lane's
pin] In Texas, NIBRS and SHR agree within 2 points on who offends (0.370 against 0.354;
0.747 against 0.730; 0.164 against 0.164). NIBRS puts more of Hispanic offenders' victims
in-group (0.788 against 0.743). Arizona's NIBRS covers
under half the SHR victims (Phoenix, Tucson and Maricopa are missing in 2022).

The central NIBRS murder rates translate to a national Hispanic share of 0.202 (0.149–0.314).
The victim lane's WONDER × SHR share is 0.191 [CALCULATION].

## Victims of Hispanic offenders

Share of Hispanic offenders' victims who are **not** Hispanic, among victims of known
ethnicity (victim ethnicity unknown for 3.5–7.8%):

| Specification | Murder | Rape/sexual assault | Robbery | Aggravated assault | Simple assault |
|---|---:|---:|---:|---:|---:|
| central (TX+AZ) | 0.216 | 0.271 | 0.300 | 0.217 | 0.195 |
| alloc=a0 | 0.299 | 0.321 | 0.359 | 0.289 | 0.225 |
| alloc=b | 0.223 | 0.263 | 0.294 | 0.225 | 0.193 |
| alloc=c | 0.377 | 0.380 | 0.416 | 0.351 | 0.268 |
| alloc=k | 0.223 | 0.263 | 0.294 | 0.225 | 0.193 |
| agencies: ethnicity recorded ≥ 0% | 0.215 | 0.266 | 0.296 | 0.211 | 0.189 |
| agencies: ethnicity recorded ≥ 80% | 0.230 | 0.281 | 0.326 | 0.223 | 0.194 |
| agencies: ethnicity recorded ≥ 95% | 0.215 | 0.273 | 0.247 | 0.190 | 0.188 |
| agencies: offender-ethnicity start date by 1 January | 0.214 | 0.272 | 0.302 | 0.218 | 0.196 |
| agencies: 12 months reported | 0.215 | 0.268 | 0.299 | 0.216 | 0.193 |
| states=TX | 0.210 | 0.256 | 0.289 | 0.208 | 0.184 |
| states=AZ | 0.304 | 0.452 | 0.507 | 0.366 | 0.337 |
| states=CA | 0.236 | 0.286 | 0.350 | 0.255 | 0.244 |
| states=TX+AZ+CA | 0.222 | 0.276 | 0.321 | 0.230 | 0.207 |
| year=2022 | 0.204 | 0.271 | 0.306 | 0.223 | 0.199 |
| year=2023 | 0.228 | 0.270 | 0.294 | 0.211 | 0.191 |
| attribution=first | 0.216 | 0.270 | 0.297 | 0.217 | 0.195 |
| attribution=anyH | 0.234 | 0.275 | 0.317 | 0.226 | 0.205 |
| attribution=allH | 0.196 | 0.267 | 0.286 | 0.209 | 0.185 |
| victims: all ages | 0.211 | 0.237 | 0.299 | 0.213 | 0.195 |
| victims: individuals + officers | 0.218 | 0.271 | 0.300 | 0.223 | 0.200 |
| incidents with an arrest only | 0.255 | 0.240 | 0.340 | 0.215 | 0.195 |
| states=TX+AZ+CA, alloc=b | 0.231 | 0.265 | 0.317 | 0.237 | 0.205 |
| states=TX+AZ+CA, alloc=c | 0.368 | 0.379 | 0.415 | 0.348 | 0.277 |

[CALCULATION: `derived/victim_ethnicity_of_hispanic_offenders_by_spec.csv`; specifications that
change only denominators or the translation have the central's victim split and are omitted.
Central counts by victim group are in `derived/victims_of_hispanic_offenders_central.csv`]

**Against the victim lane.** The victim lane takes the national non-Hispanic share of the
group's non-fatal victims from the NCVS matrix: 0.596 [SOURCE: its "Victims outside the group"].
In Texas and Arizona, police records put it at 0.19–0.30. That is the local figure, where
Hispanic residents are 36% of the population aged 12+ against 19% nationally, so it must be
carried to the nation before comparing.

Two transfers do that. Both use the logistic tract-exposure model
`P = mean_w σ(logit e_t + δ)`, where e_t is the tract's Hispanic share of residents (ACS
2020–2024 B03001, 83,608 tracts). δ is fitted on Texas and Arizona and applied to all US tracts
[CALCULATION: `nibrs_rates.py` `exposure_transfer`, `offender_given_victim`].

*Victim given offender* (tracts weighted by Mexican-origin residents): P(victim Hispanic |
offender Hispanic) nationally is:
- murder 0.710;
- rape 0.651;
- robbery 0.618;
- aggravated assault 0.708;
- simple assault 0.734.

For non-Hispanic offenders it is 0.067–0.081, and 0.194 for robbery. The murder row validates
against national SHR 2024 without adjustment: 0.710 against 0.738, and 0.077 against 0.077.
NCVS, by contrast, gives 0.404 and 0.140 [DATA: `derived/victim_exposure_transfer.csv`].

*Offender given victim* (the victim lane's homicide design): P(offender Hispanic | victim
group), Texas–Arizona → nation → nation calibrated to SHR:

| Offence | Hispanic victims | Non-Hispanic victims |
|---|---|---|
| Murder | 0.723 → 0.601 → **0.719** | 0.128 → 0.057 → **0.069** |
| Rape/sexual assault | 0.760 → 0.643 → **0.756** | 0.192 → 0.090 → **0.107** |
| Robbery | 0.473 → 0.346 → **0.468** | 0.190 → 0.087 → **0.104** |
| Aggravated assault | 0.738 → 0.618 → **0.734** | 0.144 → 0.065 → **0.078** |
| Simple assault | 0.780 → 0.666 → **0.775** | 0.129 → 0.058 → **0.070** |
| *Benchmarks* | SHR 2024 0.719 (2022–2024 0.702); NCVS 0.331 | SHR 2024 0.069 (2022–2024 0.073); NCVS 0.106 |

[CALCULATION: `derived/offender_given_victim_transfer.csv`, which holds every specification; the
SHR non-Hispanic benchmark weights the three non-Hispanic victim groups by WONDER 2024 deaths]

The calibration adds the logit shift that makes the murder row match national SHR 2024 (0.749
for Hispanic victims, 0.240 for non-Hispanic) to every offence. The 2022–2024 target is a
sensitivity.

**Is the SHR target representative, and why calibrate?** The SHR holds only reporting agencies'
victims: 2,376 Hispanic victims in 2024 against 3,776 Hispanic homicide deaths in WONDER. State
by state:

| Measure (P(offender Hispanic \| victim Hispanic)) | 2024 | 2022–2024 |
|---|---:|---:|
| SHR, all reporting states (pooled cases) | 0.719 (n = 1,509) | 0.702 (n = 4,957) |
| SHR, state values weighted by Hispanic residents (states with ≥ 20 cases; share of Hispanic residents covered) | 0.726 (0.86) | 0.703 (0.93) |
| SHR outside TX, AZ and CA | 0.676 (n = 774) | 0.644 (n = 2,332) |
| Model with the Texas–Arizona δ, outside TX, AZ and CA (same case weights) | 0.490 | 0.488 |
| SHR, TX and AZ / model, TX and AZ | 0.757 / 0.715 | 0.738 / 0.714 |
| SHR, CA / model, CA | 0.786 / 0.726 | 0.785 / 0.726 |
| Model, nation (the uncalibrated arm) | 0.601 | 0.601 |

[CALCULATION: `shr_benchmark_check.py` → `derived/shr_benchmark_check.csv`,
`derived/shr_benchmark_by_state.csv`] Reweighting states by residents barely moves the target.
Which agencies report is not what drives it.

Outside the Southwest the tract model under-predicts in-group homicide badly: 0.49 against
0.64–0.68. For example (model against SHR, 2022–2024), Colorado 0.53 against 0.73, North
Carolina 0.36 against 0.66, and Georgia 0.40 against 0.72. Hispanic–Hispanic homicide is more concentrated than
residential mixing implies. That is the case for the calibrated arm.

For non-Hispanic victims the same pattern holds: SHR 0.052 against a model 0.039 outside the
three states. Weighted by residents rather than cases, the SHR non-Hispanic value is 0.083. The
case-weighted 0.070 is the relevant one for victims [INFERENCE].

The calibration assumes the model misses non-fatal violence by the same logit shift as
homicide. That is untested outside Texas, Arizona and California [INFERENCE].

## Consistency with NCVS victim counts

The victim lane prices victimisations that NCVS counts by the victim's own ethnicity, which is
reliable. Any arm must therefore satisfy the identity
`v_H = S·P(victim H | offender H) + (1 − S)·P(victim H | offender non-H)`, where v_H is NCVS's
Hispanic share of victims (0.158–0.236 by offence, pooled 2022–2024 N-DASH). Each arm implies:

| Offence | Arm | Hispanic share of offending | Hispanic share of their victims | Implied P(offender H \| victim H) | Implied P(offender H \| victim non-H) |
|---|---|---:|---:|---:|---:|
| Rape/sexual assault | NCVS perception (victim lane) | 0.138 | 0.364 | 0.317 | 0.104 |
| | offender share only (NIBRS share, NCVS victim mix) | 0.239 | 0.364 | 0.550 | 0.181 |
| | offender share and victim mix from NIBRS | 0.239 | 0.651 | 0.985 | 0.099 |
| | 2019 arrests (victim lane arm) | 0.292 | 0.364 | 0.671 | 0.220 |
| | victim-conditional, SHR-calibrated | 0.210 | 0.570 | 0.756 | 0.107 |
| Robbery | NCVS perception | 0.175 | 0.491 | 0.364 | 0.117 |
| | offender share only | 0.188 | 0.491 | 0.390 | 0.125 |
| | offender share and victim mix from NIBRS | 0.188 | 0.618 | 0.492 | 0.094 |
| | 2019 arrests | 0.230 | 0.491 | 0.479 | 0.154 |
| | victim-conditional, SHR-calibrated | 0.190 | 0.580 | 0.468 | 0.104 |
| Aggravated assault | NCVS perception | 0.150 | 0.384 | 0.350 | 0.111 |
| | offender share only | 0.222 | 0.384 | 0.518 | 0.164 |
| | offender share and victim mix from NIBRS | 0.222 | 0.708 | 0.957 | 0.078 |
| | 2019 arrests | 0.255 | 0.384 | 0.594 | 0.188 |
| | victim-conditional, SHR-calibrated | 0.186 | 0.649 | 0.734 | 0.078 |
| Simple assault | NCVS perception | 0.144 | 0.400 | 0.327 | 0.105 |
| | offender share only | 0.220 | 0.400 | 0.499 | 0.160 |
| | offender share and victim mix from NIBRS | 0.220 | 0.734 | 0.917 | 0.071 |
| | 2019 arrests | 0.184 | 0.400 | 0.417 | 0.134 |
| | victim-conditional, SHR-calibrated | 0.194 | 0.703 | 0.775 | 0.070 |

[CALCULATION: `derived/consistency_with_ncvs_victims.csv`, which also holds the uncalibrated and
2022–2024-calibrated conditional arms]

**Arms that keep NCVS's victim mix.** The offender-only arm and the 2019-arrest arm imply that
Hispanic offenders commit 13–22% of the violence against non-Hispanic victims nationally. In
Texas and Arizona, where Hispanic residents are 36% of the population, the NIBRS value is
0.13–0.19. The national SHR homicide value is 0.069. In NIBRS the assault values sit at the
homicide level (0.129–0.144 against 0.128). Nationally, assault should therefore sit near 0.07,
not 0.16. These arms overstate cross-group offending about twofold, and non-Hispanic victims
carry most of the cost [INFERENCE].

**The NIBRS-only arm.** It gets the non-Hispanic victims right (0.071–0.099) but implies more
Hispanic victims than NCVS reports (implied P 0.92–0.99; robbery 0.49). That error falls mostly on in-group
victims, which the cost excludes. This is why it lands near the preferred arm.

**The victim-conditional arm** satisfies the identity by construction. Its implied national
Hispanic offending share is 0.186–0.210, or 0.99–1.12 times the population share. That lies
between the NCVS perception (0.138–0.175) and NIBRS's direct translation (0.188–0.239)
[CALCULATION].

**Why the NCVS matrix is attenuated** [INFERENCE]. Across offences NCVS puts 36–49% of Hispanic
offenders' victims as Hispanic. NIBRS puts 70–81% in Texas and Arizona, and SHR puts 74%
nationally for homicide. The most economical explanation is misperception: victims misclassify
some offenders' ethnicity, which mixes the victim × offender matrix toward independence.
Could police records instead overstate in-group offending, for example by recording an unseen
offender's ethnicity from the victim's? Incidents with an arrest, where the offender is booked,
show the same pattern: P(victim Hispanic | offender Hispanic) there is 0.66–0.81 (robbery
0.66, murder 0.75, rape 0.76, aggravated assault 0.79, simple assault 0.81).
Unreported crime is unlikely to explain the gap. The victim lane found equal reporting to
police by offender ethnicity (45.1% against 45.9%). NCVS's all-offenders-Hispanic rule for
mixed groups lowers its Hispanic count but does not change within-group mixing much here: the
`attribution=allH` specification moves the victim split by at most 2 points.

## Victim cost re-run

**Method.** The victim lane's model is imported, not copied: `victim_cost.py` supplies prices,
the incidence builder and `run()`. Its setup is replicated without writing any file.

**Gates.** Before any NIBRS input is used, the gates reproduce the lane's central ($28.9229bn
full, $4.5014bn tangible) and its arrest-share arm ($43.1199bn) [CALCULATION:
`derived/cost_log.txt`].

**Held fixed from the victim lane:**
- 2024 NCVS national victimisations by offence (CV2024 table 1);
- the Hispanic → Mexican-origin population share s = 0.5975;
- the in-group share m = 0.786 of Hispanic victims;
- Miller 2021 victim-only prices;
- homicide from WONDER × SHR.

**Arms.**
- *Offender share only*: 2024 victimisations × NIBRS national Hispanic share, with NCVS's
  victim mix. This is the lane's own code path for its arrest-share arm.
- *Offender share + NIBRS victim mix*: the same, with the outside-victim share taken from the
  victim-given-offender transfer, (1 − P) + P·(1 − m).
- *Victim-conditional*: NCVS 2024 victimisations split by self-reported victim ethnicity × NIBRS
  P(offender Hispanic | victim group). Outside share = (V_NH·P_NH + V_H·P_H·(1 − m)) ÷
  (V_H·P_H + V_NH·P_NH).

Full cost ($bn) by specification and arm:

| Specification | Offender share only (NCVS victim mix) | Offender share + NIBRS victim mix | Victim-conditional | Victim-conditional, SHR-calibrated |
|---|---:|---:|---:|---:|
| central | 40.04 | 29.40 | 25.39 | **28.59** |
| alloc=a0 | 40.15 | 29.49 | 28.05 | 27.15 |
| alloc=b | 33.51 | 25.09 | 22.39 | 29.08 |
| alloc=c | 51.95 | 37.34 | 37.82 | 24.99 |
| alloc=k | 40.35 | 29.63 | – | – |
| agencies: ethnicity recorded ≥ 0% | 39.78 | 29.23 | 25.56 | 28.26 |
| agencies: ethnicity recorded ≥ 80% | 38.97 | 28.69 | 25.69 | 28.33 |
| agencies: ethnicity recorded ≥ 95% | 38.01 | 28.05 | 25.06 | 27.66 |
| agencies: offender-ethnicity start date by 1 January | 40.46 | 29.69 | – | – |
| agencies: 12 months reported | 40.11 | 29.45 | – | – |
| states=TX | 40.63 | 29.80 | 25.08 | 28.76 |
| states=AZ | 33.93 | 25.42 | 29.00 | 25.25 |
| states=CA | 36.96 | 27.42 | 31.77 | 25.57 |
| states=TX+AZ+CA | 39.76 | 29.25 | 27.04 | 28.31 |
| year=2022 | 40.08 | 29.44 | 25.31 | 29.09 |
| year=2023 | 40.01 | 29.38 | 25.47 | 28.12 |
| attribution=first | 40.05 | 29.41 | 25.38 | 28.57 |
| attribution=anyH | 41.10 | 30.12 | 26.27 | 27.21 |
| attribution=allH | 39.02 | 28.73 | 24.59 | 30.32 |
| victims: all ages | 40.29 | 29.58 | 24.93 | 28.15 |
| victims: individuals + officers | 40.03 | 29.40 | – | – |
| denominator: all ages | 40.47 | 29.69 | – | – |
| simple assault incl. intimidation 13C | 39.84 | 29.28 | – | – |
| translation: rate vs all residents | 37.65 | 27.83 | – | – |
| incidents with an arrest only | 40.88 | 30.02 | 25.67 | 28.09 |
| states=TX+AZ+CA, alloc=b | 32.32 | 24.31 | 23.46 | 29.03 |
| states=TX+AZ+CA, alloc=c | 51.98 | 37.39 | 39.92 | 24.82 |

[CALCULATION: `derived/cost_arms.csv`, with tangible cost, outside victims and implied shares
per row] The conditional arms were not run for the seven specifications marked "–". Two of them
(denominator, translation) cannot change the conditional share. The other five (alloc=k, start
date, 12 months, officers, intimidation) were left out of the transfer run; they move the other
two arms by at most 1%. For the conditional arm, calibration pins
murder to the SHR. Allocation choices move murder's local share most, so the calibrated shift
absorbs them and bounds (b) and (c) invert. The uncalibrated conditional column carries the
allocation bound for that structure: $22.4–37.8bn.

Also computed: arrest-calibrated translation, $46.64bn offender share only and $33.75bn with
the NIBRS victim mix. Texas–Arizona victims as observed, untransferred: $26.78bn. Conditional
arm calibrated to SHR 2022–2024: $29.39bn [CALCULATION].

Price and scaling sensitivities on the central specification (tangible / full, $bn):

| Sensitivity | Offender share only | Offender share + NIBRS victim mix | Victim-conditional, SHR-calibrated |
|---|---:|---:|---:|
| McCollister 2010 prices, risk of homicide removed | 3.20 / 40.32 | 2.45 / 30.96 | 2.39 / 30.43 |
| Miller + US DOT 2024 VSL for murder | 5.49 / 44.87 | 4.44 / 34.24 | 4.37 / 33.43 |
| Hispanic victims all in-group (non-Hispanic victims only) | 4.28 / 33.28 | 2.95 / 19.76 | 2.99 / 20.29 |
| ACS institutional ratio 1.118 (custody footing) | 6.14 / 44.76 | 4.97 / 32.88 | 4.88 / 31.97 |
| ACS institutional ratio 0.901 | 4.95 / 36.08 | 4.00 / 26.49 | 3.94 / 25.76 |

[CALCULATION: `derived/cost_arms.csv`, specs `central; …`]

By offence, full $bn with outside victims in brackets:

| Offence | Victim lane central | Offender share only | Offender share + NIBRS victims | Victim-conditional, SHR-calibrated |
|---|---:|---:|---:|---:|
| Rape/sexual assault | 6.95 (33,029) | 12.05 (57,259) | 8.24 (39,145) | 8.16 (38,781) |
| Aggravated assault | 6.87 (84,110) | 10.17 (124,454) | 6.45 (78,970) | 5.97 (73,091) |
| Simple assault | 5.03 (243,302) | 7.68 (371,757) | 4.73 (229,259) | 4.42 (213,948) |
| Robbery | 0.92 (41,295) | 0.99 (44,224) | 0.82 (36,996) | 0.88 (39,664) |
| Murder | 9.16 (1,021) | 9.16 | 9.16 | 9.16 |

[CALCULATION: `derived/cost_by_offence_nibrs_central.csv`; victim lane from its
`derived/cost_by_offence_central.csv`]

Share of the group's non-fatal victimisations that fall on other residents:

| Offence | NCVS (victim lane) | NIBRS transferred | Victim-conditional, SHR-calibrated | TX/AZ as observed |
|---|---:|---:|---:|---:|
| Rape/sexual assault | 0.714 | 0.488 | 0.552 | 0.427 |
| Robbery | 0.614 | 0.514 | 0.544 | 0.450 |
| Aggravated assault | 0.698 | 0.443 | 0.490 | 0.384 |
| Simple assault | 0.686 | 0.423 | 0.447 | 0.367 |

[CALCULATION: `derived/outside_share_by_offence.csv`, `derived/cost_by_offence_nibrs_central.csv`]

## What the parent must check

1. **The structure choice.** The pre-planned central was "offender share only" ($40.0bn), like
   for like with the $43.1bn arm. The preferred victim-conditional arm ($28.6bn) was adopted
   after the adding-up check failed the pre-planned arm. The check itself is structural and
   does not depend on the result's direction, but the switch came after seeing results. Both
   are reported, and the choice belongs to the parent.
2. **The calibration assumption.** The calibrated arm assumes non-fatal violence departs from
   residential mixing as homicide does. The homicide evidence is strong: the tract model
   predicts 0.49 outside the Southwest where SHR shows 0.64–0.68. For non-fatal offences it is
   untested. The uncalibrated arm ($25.4bn) is the lower reading.
3. **The attenuation inference.** That NCVS misperception attenuates its victim × offender
   matrix is an inference. The arrest-only incidents and the SHR support it.
4. **The national translation.** Texas–Arizona relative rates are assumed to hold nationally.
   The arrestee version falls 2.3–7.2 points short of FBI 2023 national arrest shares. The
   arrest-calibrated arms give $46.6bn (NCVS victim mix) and $33.8bn (NIBRS victim mix).
5. **Coverage.** Arizona is thin: 43–51% of residents are in agencies recording ethnicity, and
   the large Phoenix-area agencies are missing in 2022. Texas drives every result (`states=TX` ≈
   central).
6. **Mexican share.** Texas's Mexican share of Hispanic residents is 80%, below the brief's
   85–90%. The rates are for Hispanic residents; the victim lane's s is unchanged.
7. **The arrest arm.** The $43.1bn arm keeps NCVS's victim mix, the same mixing that inflates
   the offender-only arm. It also uses 2019 arrest shares, and the 2023 shares are higher.
8. **Correcting a limit.** The CDE bulk store needs no API key. The victim and homicide lanes'
   limit ("CDE data after 2019 need an API key") does not apply to it, so post-2019 NIBRS by
   state is reachable.

## Limits

1. **Hispanic, not Mexican origin.** NIBRS has no origin field. Covered Hispanic residents are
   81–86% Mexican origin [DATA].
2. **Police-recorded ethnicity** is partly taken from victims' and witnesses' descriptions. The
   arrest-only specification, where police meet the offender, gives similar ratios and victim
   splits [CALCULATION].
3. **Unknowns are wide for robbery.** Allocation bounds span 2.36–9.75 for robbery
   (Hispanic ÷ white) and 0.128–0.354 for the national share. The central allocation assumes
   unknown offenders resemble known ones within the victim-ethnicity cell and recorded race
   [INFERENCE].
4. **Crude rates.** There is no age or sex standardisation. The Hispanic population aged 12+ is
   younger, so part of the ratio against whites is age composition. The cost calculation is
   unaffected; interpretation is [INFERENCE].
5. **Geography.** Three steps assume the pattern transfers beyond Texas and Arizona: the rate
   translation, the tract-exposure transfer and the SHR calibration. Each is checked against a
   national benchmark (FBI Table 43C for arrests, SHR for homicide). None is checked for
   non-fatal offences outside the Southwest.
6. **NCVS inputs kept.** National 2024 victimisations, victim ethnicity shares and the
   victim-lane matrix carry NCVS sampling error, which is not propagated here. The victim lane's
   ±$2.0bn one-SE figure applies to its own arm.
7. **Denominators.** Agency jurisdictions are matched to ACS places by name; FBI and ACS
   populations must agree within a factor of 2. Sheriffs take their county net of every city
   with its own police. Unmatched agencies fall back to county composition, 0.2–3.9% of covered
   population [DATA: `derived/coverage_by_state_year.csv`].
8. **Homicide** stays on the victim lane's inputs. NIBRS murder is a check only.
9. **Instrument bias.** This lane was produced through an LLM; see `notes/llm-bias-caveat.md`.
   The choices that move the number most are explicit arms. The structure switch lowered the
   preferred figure against the pre-planned arm, and is flagged as such (item 1 above).

## Covered and skipped

**Covered:**
- the brief;
- the victim lane's RESULT.md, model and derived inputs (imported, never edited);
- NIBRS 2022–2023 for Texas, Arizona and California: agencies, months, incidents, offences,
  offenders, victims, victim–offence links and arrestees;
- the FBI participation file and the CDE agency lists;
- ACS 5-year place and county composition (B03002, B03001, B01001 and the H, I and B
  iterations) and ACS 1-year state B03001;
- the victim lane's cached tract B03001;
- the MAP SHR (sha256-pinned);
- the NCVS lane's N-DASH and victim × offender matrix;
- the arrests lane's FBI 2023 Table 43C and Census NC-EST2024 files.

**Skipped, with reasons:**
- *Victim–offender relationship segment.* The cost does not use it. It could test whether
  in-group victimisation is concentrated among family and acquaintances, which bears on the
  attenuation inference.
- *Offender age and sex.* No standardisation (limit 4).
- *California as central.* Its coverage and ethnicity recording are inadequate (above); it is
  reported as a sensitivity only.
- *States outside the brief.* A NIBRS state outside the Southwest with good ethnicity recording
  (Colorado, Washington) would test the calibration for non-fatal violence directly. That is the
  most useful next step.
- *NIBRS 2024 and property crime.* Neither was asked for. The victim lane keeps property crime
  outside its totals.

## Sources

| Item | Source |
|---|---|
| Incident, offender, victim and arrestee records, TX/AZ/CA 2022–2023 | FBI NIBRS state files, Crime Data Explorer signed-URL store `nibrs/incident/{year}/{ST}-{year}.zip`; sha256 in `derived/source_manifest.csv` |
| Agency participation and jurisdictions | FBI `ucr_participation_1960_2025.csv` (CDE store); CDE `/LATEST/agency/byStateAbbr/{ST}` |
| Place and county population by Hispanic origin, race and age | ACS 5-year 2018–2022 and 2019–2023, tables B03002, B03001, B01001, B01001H, B01001I, B01001B, Census API (`acs_denominators.py`) |
| Mexican share of Hispanic residents, by state | ACS 1-year 2022 and 2023, B03001 |
| Tract Hispanic share | ACS 2020–2024 5-year B03001 by tract, the victim lane's cache (`../crime_victim_cost_2026_09_23/_cache/`) |
| National population aged 12+ | NCVS 2024 (`../ncvs_victim_offender_2026_09_18/derived/cv_population_12plus.csv`); Census NC-EST2024 by age (`../nibrs_arrests_2026_09_16/_cache/`) |
| National arrest shares by ethnicity | FBI *Crime in the United States 2023*, Table 43C (`../nibrs_arrests_2026_09_16/arrests_by_ethnicity_2023.csv`) |
| Homicide by victim and offender | Murder Accountability Project SHR compilation `SHR76_25a.csv` (sha256 `eeedbf5e…b88a12`), homicide lane cache |
| Victim ethnicity shares and perceived-offender matrix, 2022–2024 | BJS N-DASH and *Criminal Victimization* tables via the NCVS lane |
| Prices, incidence builder, homicide inputs, s and m | `../crime_victim_cost_2026_09_23/victim_cost.py` and its `derived/` (imported) |

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
L=infra/immigration-fiscal/offender_ethnicity_nibrs_2026_09_23
# 456 MB into $L/_cache (disk preflight per file; cached files are skipped)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_nibrs.py participation agencies-TX agencies-AZ agencies-CA TX-2022 TX-2023 AZ-2022 AZ-2023 CA-2022 CA-2023
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a      # Census key, never printed
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acs_denominators.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/nibrs_stage.py TX-2022 TX-2023 AZ-2022 AZ-2023 CA-2022 CA-2023
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/nibrs_rates.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/shr_benchmark_check.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/victim_cost_rerun.py
```

Scripts:
- `fetch_nibrs.py`: CDE store, parallel range download, preflight, manifest.
- `acs_denominators.py`
- `nibrs_stage.py`: per state-year aggregate cells in `_cache/stage/`.
- `nibrs_rates.py`: rates, bounds, specifications, arrestees, translation check, homicide check,
  both transfers; gates for Texas coverage, NCVS population, tract cache, Table 43C and the SHR
  pin.
- `shr_benchmark_check.py`
- `victim_cost_rerun.py`: imports the victim lane; gates reproduce its central and arrest arm.

Raw files stay in `_cache/`, which is ignored. `derived/` holds aggregates only, plus
`rates_log.txt` and `cost_log.txt`.

claude-opus-5-5[1m]

**Verdict:** Charging public order and safety by use raises the target's share of BEA line 4 from $62.43bn to **$68.37bn (+$5.94bn, +9.5%)** in the central key set, which moves the CBO-informed band from $165.1–197.4bn to **$171.1–203.3bn**. [CALCULATION: `allocate.py` → `derived/key_sets.csv`] Custody is the most secure part: $2.63bn of the increase comes from prisons, where the target holds 14.2% of institutional residents aged 18–64 against 12.0% of residents. Police and courts add $3.22bn, and that part rests on a 2019 FBI arrest share. If Hispanic adults were not over-represented in arrests, the central would be +$3.19bn. If the 2019 arrest ratio fell by 2023 as BJS's Hispanic imprisonment ratio did, the central would be +$4.44bn. Across the brief's key families the change runs from −$1.03bn to +$8.65bn, a band of $164.1–206.0bn. With the adjusted Hispanic-to-Mexican scaling alone, it runs from +$1.48bn to +$8.65bn.

The $2.917bn of ICE custody outlays and all CBP spending are **already inside line 4** and already charged per head. The ICE custody therefore moves inside line 4 rather than being added on top. Keying the interior share by use adds $0.10bn. If CBP border spending and border-arrest custody were not charged to the resident stock at all, the target would carry $3.11bn less, and the central would be +$2.84bn with a band of $168.0–200.2bn. That boundary call is the lead's to make (see "ICE custody and CBP").

## Change from the per-head $62.425bn

Everything not named in a row stays at the central key: police half arrests, half per head; prisons on the ACS adjusted custody share; courts 60% criminal; ICE interior custody on the central bed-day share; CBP per head.

| Key set | Target $bn | Change $bn | CBO-informed band $bn |
|---|---:|---:|---:|
| Per head, reference (positive control) | 62.43 | 0 | 165.1–197.4 |
| **Central** | **68.37** | **+5.94** | **171.1–203.3** |
| Police by offending (arrest share) | 70.58 | +8.15 | 173.3–205.5 |
| Police by victimization | 64.16 | +1.74 | 166.9–199.1 |
| Police by NCVS perceived offender (disconfirmation arm) | 62.58 | +0.16 | 165.3–197.5 |
| Prisons by raw ACS custody (no generic-Hispanic reallocation) | 66.48 | +4.06 | 169.2–201.4 |
| Prisons by BJS prisons+jails check (2023), adjusted scaling | 68.47 | +6.05 | 171.2–203.4 |
| Raw Hispanic→Mexican scaling everywhere | 64.10 | +1.67 | 166.8–199.1 |
| Courts 50% / 75% criminal | 68.20 / 68.62 | +5.78 / +6.20 | — |
| ICE interior share low / high | 68.28 / 68.51 | +5.86 / +6.08 | — |
| CBP and border-arrest ICE custody not charged to the target | 65.26 | +2.84 | 168.0–200.2 |
| Grid of 216 sets (3 police keys × 4 prison keys × 3 court shares × 3 ICE shares × 2 scalings) | 61.40–71.07 | −1.03 to +8.65 | 164.1–206.0 |

[CALCULATION: `derived/key_sets.csv`, `summary.json` → `one_at_a_time_change_bn`] Safety responds at 1.0 in every service construction of `full_account_2026_09_20/derived/service_response_components.csv`. Each change above therefore also passes 1:1 into the proportional ($269.8–288.7bn) and other benchmarks. [DATA] Against the account's `adults` alternative key ($56.07bn), the central is $12.30bn higher.

Sensitivities that sit outside the grid, each applied to the central set: [CALCULATION: `summary.json` → `sensitivity_delta_bn`]

| Change to the central assumption | Δ $bn | Central becomes |
|---|---:|---:|
| Hispanic adult arrest rate equal to the national rate (RR 1.0 instead of 1.145) | −2.75 | +3.19 |
| Arrest ratio carried from 2019 to 2023 by BJS's Hispanic-to-all adult imprisonment ratio (1.416 → 1.317), giving RR 1.066 [INFERENCE] | −1.50 | +4.44 |
| Hispanic-to-Mexican arrest scaling at its 2016 ACS value (m/p 1.079 instead of 1.145) | −1.24 | +4.70 |
| Target members beyond the ACS Mexican-coded count (8.2% at 18–64) at national rather than Mexican-coded rates | −0.71 | +5.23 |
| ICE ERO non-custody ($2.35bn, all funding years) keyed by Mexico's ERO arrest share | +0.59 | +6.54 |
| BEA Table 3.15.5 subline shares instead of Table 3.16 | −0.03 | +5.91 |
| Victimization key counts children under 12 at the same relative rate (police-victimization set only) | +1.44 | victimization set +3.18 |

## Central choice and reasons

| Subline, 2024 $bn | National | Per head | Central key | Target share | Use $bn | Change |
|---|---:|---:|---|---:|---:|---:|
| Police excluding CBP and ICE custody | 210.69 | 25.33 | ½ arrests + ½ per head | 0.1307 | 27.54 | +2.21 |
| CBP, inside police | 23.87 | 2.87 | per head | 0.1202 | 2.87 | 0 |
| ICE custody, border-arrest part | 1.97 | 0.24 | per head | 0.1202 | 0.24 | 0 |
| ICE custody, interior part | 0.95 | 0.11 | Mexico interior bed-day share | 0.2265 | 0.21 | +0.10 |
| Fire | 80.17 | 9.64 | per head | 0.1202 | 9.64 | 0 |
| Law courts | 80.19 | 9.64 | 60% arrests + 40% per head | 0.1328 | 10.65 | +1.01 |
| Prisons | 121.32 | 14.59 | ACS custody 18–64, adjusted | 0.1419 | 17.22 | +2.63 |
| **Line 4** | **519.15** | **62.43** | | **0.1317** | **68.37** | **+5.94** |

[CALCULATION: `derived/central_split.csv`, `cj_allocation.csv`]

- **Prisons, adjusted ACS custody.** Three estimates agree: the 2024 1-year ACS gives 0.1419, the 2020–2024 5-year ACS 0.1396, and the BJS prisons+jails check 0.1428. The BJS check takes its Hispanic total from BJS counts, 20.19% of prisoners and jail inmates in 2023, the same as the ACS institutional share (20.19%). It shares the ACS Mexican/Hispanic ratio. The raw ACS key is unstable: 0.1264 in the 1-year file and 0.1150 in the 5-year. The instability comes from ACS's residual "Other Hispanic" code (HISP 24). Its institutional rate at 18–64 is 3.9% for natives, 3.4 times the all-native rate. That points to institutional records with no detailed origin, not a real group. [DATA: `derived/acs_hisp_nativity_gq.csv`; INFERENCE]
- **Police, half arrests and half per head.** Patrol, calls for service and traffic serve everyone, while arrests, booking and investigation follow offending. No source here pins the split; half and half is the brief's patrol-protects-everyone key. [INFERENCE / FRAMING-SENSITIVE] The pure offending key relies on the 2019 FBI arrest share. Victims' reports contradict it: NCVS 2022–2024 puts Hispanic perceived offending at 0.80 times the national rate, where arrests put it at 1.15. [DATA: `ncvs_victim_offender_2026_09_18/derived/rates_by_victim_and_offender_2022_2024.csv`] The pure victimization key ignores work driven by offenders.
- **Courts, 60% criminal.** Prosecution and public defense are wholly criminal, and court dockets also carry civil, family and traffic cases. No held or quickly found source splits BEA "law courts" spending, so the share is an assumption tested at 50% and 75%. Moving across that range shifts the result by −$0.17bn to +$0.25bn. [INFERENCE]
- **ICE interior custody.** The allocation uses official FY2024 shares and one assumption, stated with its bound in the next section.

## ICE custody and CBP (task 3)

**Both are already in line 4.** USAspending File A tags ICE Operations and Support (070-0540, $9.856bn gross outlays FY2024) and CBP's operating, fee and procurement accounts ($24.85bn; only a $0.42bn Puerto Rico transfer account sits elsewhere) under function "Administration of Justice", subfunction 751 "Federal law enforcement activities". BEA's concordance maps OMB "Administration of justice" to NIPA "Public order and safety". BEA federal POS current expenditure in CY2024 ($82.81bn) is close to OMB function 750 FY2024 outlays ($83.79bn). [DATA: `detention_reconciliation_2026_09_20/_cache/dhs_fy2024_fileab.zip`; SOURCE: [BEA, Survey of Current Business, June 2000, p. 21](https://apps.bea.gov/scb/pdf/National/NIPAREL/2000/0600gf.pdf); DATA: OMB Historical Table 3.2, `sources/immigration-fiscal/data/external/omb_hist_fy2027/hist03z2_fy2027.xlsx`] Adding the $2.917bn on top of line 4 would count it twice; the [custody/crime rule](../../../research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md) requires any detention breakout to reconcile to the account's totals first. The script carves the custody outlays and CBP ($23.87bn: subfunction-751 CBP gross outlays excluding procurement and construction) out of the police subline. Their basis differs from NIPA: fiscal-year gross outlays, not calendar-year consumption. [INFERENCE]

The official FY2024 shares of the Mexico-citizenship group: [SOURCE: [ICE FY2024 Annual Report](https://www.ice.gov/doclib/eoy/iceAnnualReportFY2024.pdf) Fig. 15 and appendix; ICE FY2024 detention workbook; [OHSS monthly tables, November 2024](https://ohss.dhs.gov/sites/default/files/2025-01/2025_0116_ohss_immigration-enforcement-and-legal-processes-tables-november-2024.xlsx), cells rounded to 10]

| Measure, FY2024 | Mexico | Total | Share | All $2.917bn keyed by it |
|---|---:|---:|---:|---:|
| Detained population, end of FY2024 | 5,089 | 37,684 | 13.5% | $0.39bn |
| Book-ins to ICE detention | 69,360 | 277,910 | 25.0% | $0.73bn |
| Removals | 87,298 | 271,484 | 32.2% | $0.94bn |
| ERO administrative (interior) arrests | 43,570 | 113,430 | 38.4% | — |
| Per head, reference | | | 12.0% | $0.35bn |

Central: only interior custody is attributed to residents. The ICE-arrest share of FY2024 average daily population (12,232 of 37,722, 32.4%, $0.946bn) is keyed by Mexico's interior bed-day share, estimated at **22.6%**. That estimate applies Mexico's ERO arrest share (38.4%) with the Mexican-to-other length-of-stay ratio of 0.47. The ratio follows from the detained-stock share of 13.5% against the book-in share of 25.0%. The assumption is that the ratio is the same for interior and border arrests. [CALCULATION; INFERENCE] The end-of-year snapshot caps the interior share at 37.3% (all 5,089 Mexican detainees among the 13,633 ICE-arrest detainees); the all-agency detained share of 13.5% is the low arm. The border-arrest part stays per head. Target ICE custody is $0.45bn against $0.35bn per head.

**CBP, one sentence:** CBP spending follows the flow of people and goods across the border, not the offending, victimization or custody of residents, so no resident use key applies to it. It keeps the reference per-head key in every set. Zeroing it treats border spending as fixed with respect to the resident stock, the way the account treats defense, and lowers the charge by $2.87bn, plus $0.24bn of border-arrest custody.

## Mexico-born and US-born

Keys that identify nativity: per head (CPS target: 12.22m Mexico-born, 29.9%), ACS custody by nativity, and ICE (Mexican nationals only). Arrest and NCVS keys carry no nativity. [DATA: CPS ASEC 2025 canonical target; `derived/central_split.csv`]

| Central, $bn | Mexico-born | US-born | Not identified |
|---|---:|---:|---:|
| Per head, reference | 18.65 | 43.77 | — |
| Central, identified parts only | 13.47 | 33.23 | 21.67 (arrest-keyed police and courts) |
| Central, arrest parts split like custody (26.2% Mexico-born) [INFERENCE] | 19.15 | 49.22 | — |
| Prisons alone: per head → custody key | 4.36 → 4.51 | 10.23 → 12.70 | — |

The custody key raises the charge almost entirely on the US-born. At 18–64, ACS institutional residents per household resident are 0.79% for the Mexico-born (adjusted) and 1.43% for US-born Mexican-origin adults. The corresponding all-origin rates are 0.44% for the foreign-born and 1.21% for natives. [CALCULATION]

**Check against the prisoner survey.** In the 2016 Survey of Prison Inmates, 34.9% of Hispanic state and federal prisoners report birth outside the United States. In ACS 2016, 27.9% of Hispanic institutional residents aged 18–64 are foreign-born; the 2024 figure is 27.1%. [DATA: SPI 2016 V0945 × RV0003, weighted; the counts match the [2026-09-05 audit](../../../research/immigration-crime-race-ethnicity-2026-09-05.md) to within one person (gate); `derived/acs_hisp_nativity_gq.csv`] Both sources put the foreign-born well below their 46.6% share of Hispanic residents aged 18–64 in 2016. In the same year the ACS share is lower. The universes differ: the ACS adds jails, ICE detention and non-correctional institutions. The definitions differ too: the SPI records reported birthplace, which the audit does not equate with Census nativity. [INFERENCE] The survey carries no Mexican detail. If the ACS understated the foreign-born share of custody by the same odds ratio (1.38), the Mexico-born part of the prisons charge would rise from 26.2% to 33.0%. That would move $1.16bn from the US-born to the Mexico-born column and leave the total unchanged. [CALCULATION: `summary.json` → `nativity_check`]

## Method

1. **Sublines.** BEA Table 3.17 has no police/fire/courts/prisons split; Table 3.16 does. The Table 3.16 sublines sum exactly to its POS total: police 237,742 + fire 80,261 + law courts 80,274 + prisons 121,449 = $519,726m. That total exceeds Table 3.17 line 4 ($519,153m) by POS social benefits ($518m) plus a $55m federal residual. The sublines are scaled by 519,153/519,726 so they sum to line 4 exactly (gate). Table 3.15.5 (consumption plus investment) shares are a cross-check (−$0.03bn). [DATA: pinned workbook `Section3All_xls.xlsx`, SHA 69b5c7ae…]
2. **Positive control.** From `incidence_keys.csv`: 40,896,574 / 336,727,803 = 0.121453 within CPS, times the pool fraction 0.990053 and $519.153bn, gives $62.425443bn. This equals the `allocations.csv` value to 1e-9. [CALCULATION]
3. **Custody key.** For each nativity n: share = Σ T(n,18–64) × I_adj(M,n) / HH(M,n) ÷ I(all,18–64). T is the CPS target count, I is ACS institutional residents (TYPEHUGQ=2) and HH is ACS household residents. I_adj adds the "Other Hispanic" institutional excess above the all-origin rate for nativity n, allocated to Mexican by its share of the named-Hispanic population. Allocating by institutional share instead gives 0.1436. BJS check: Hispanic sentenced prisoners at yearend 2023 (282,700 of 1,210,308) plus jail inmates at midyear 2023 (95,700 of 664,200) make up 20.19%, the same as the ACS institutional share. The 65,552 state and federal prisoners held in local jails sit in both counts; removing them moves the share to 20.07–20.40%, depending on their unknown composition. That share times the Mexican share of Hispanic institutional residents (0.6535 adjusted, 0.5815 raw) times the CPS/ACS scaling (1.0824) gives 0.1428. The first run used the 2022 prison count (19.98%, key 0.1413). *Prisoners in 2023* reprints the 2022 row unchanged (gate). [SOURCE: BJS, *Prisoners in 2023*, Tables 3 and 14, extract `bjs_p23st_extract.txt`; *Jail Inmates in 2023*, Table 5; CALCULATION]
4. **Arrest key.** Share = A_T × RR_H × m/p. A_T = 0.1077, the target's share of adult residents. RR_H = 1.145: 18.78% of adult arrests in the FBI 2019 Table 43C ethnicity panel against 16.40% of adults (ACS 2019). m/p = 0.6535/0.5710: the Mexican share of Hispanic institutional residents over the Mexican share of the Hispanic population, both at 18–64. This is the brief's explicit Hispanic-to-Mexican scaling. [DATA: `crime_cost_2026_09_16/crime_cost.py` T43C_TOTAL; CALCULATION]
5. **Victimization key.** The target's share of residents aged 12+ (0.1132) times the Hispanic-to-national ratio of violent incidents per resident 12+ in NCVS 2022–2024 (0.978). This assumes the Mexican-origin rate equals the Hispanic rate. [DATA; INFERENCE]
6. **Band.** Every change enters `cbo_category_lag_non_school_full` at response 1.0: new band = [165.12 + Δ, 197.38 + Δ]. [DATA: `service_response_summary.csv`]

## Hispanic coding in the sources

These checks apply the [2026-09-05 race and ethnicity audit](../../../research/immigration-crime-race-ethnicity-2026-09-05.md), read after the first run. None of them changes the central.

- **FBI arrests.** The key uses Table 43C's ethnicity panel, Hispanic of any race. The FBI records race and Hispanic ethnicity as separate fields, so the race panel's White column includes Hispanic arrestees and cannot stand in for it. [SOURCE: audit, FBI NIBRS guide]
- **BJS prisons and jails.** BJS prisoner counts by race and Hispanic origin are estimates adjusted with the 2004 and 2016 prisoner surveys, not fresh self-reports. [SOURCE: *Prisoners in 2023*, Table 3 source note; audit] Jail counts come from administrative reports in the Annual Survey of Jails, with no such adjustment listed. Their Hispanic share (14.4%) is well below the prison share (23.4%); how much of that gap is coding was not established. [SOURCE: *Jail Inmates in 2023*, Table 5]
- **ACS origin coding.** Detailed Hispanic origin was imputed item by item for 0.33% of Hispanic institutional residents aged 18–64: 0.23% of Mexican-coded and 0.45% of generic "Other Hispanic" residents, against 0.58% of Hispanic household residents. The generic institutional excess is therefore reported as generic, not produced by item imputation. FHISP marks item imputation only; whether records imputed whole into group quarters carry the flag was not checked. [DATA: `derived/acs_hisp_allocation_1864.csv`]
- **Survey of Prison Inmates 2016.** The public file records Hispanic origin as yes or no (V0015, V1951), suppresses country of citizenship (V0946–V0949) and records birthplace only as the United States or another country (V0945). It cannot name Mexican origin, so it cannot test the Hispanic-to-Mexican scaling; it supplies the nativity check above.
- **Texas.** None of the 15 Light–He–Robey replication tables carries race or ethnicity, and the located Texas DPS status-by-offense table has no race or ethnicity cells. Texas therefore cannot key Hispanic or Mexican-origin arrests, and its status comparisons pool all immigrants against all natives. [SOURCE: audit]
- **What the keys measure.** Arrests and prison stock record use of police and prisons. They also reflect detection, prosecution, sentencing and time served, so they are not offending rates. That is the right quantity for a use key and the wrong one for a crime-rate claim. [INFERENCE, following the audit's measurement point]

## Limits

- **Institutional residence is not correctional custody.** ACS cannot separate correctional, noncorrectional and ICE custody, so every custody share in this file is institutional residence at 18–64. Bound on the ICE part: removing all 5,089 Mexican nationals in ICE custody and all 37,684 detainees moves the share from 0.1419 to 0.1418 (−$0.02bn). The correctional-only BJS check gives 0.1428. The ICE count is a bound on the effect, not a subtraction that yields a corrected rate. [DATA; INFERENCE]
- **Frame.** [FRAMING-SENSITIVE] The custody key charges the target for Mexican-origin people in custody. They sit outside the CPS civilian-household target, in the account's other-resident headcount. That fits the absent-target comparison only if the absent population includes its institutional members.
- **Arrest share.** The arrest share is from 2019, covers adults only and comes from an ethnicity-reporting panel covering 70% of the population. The crime-cost lane judged that the reporting agencies lean toward high-Hispanic states, which would bias the share upward; that was not verified here. [INFERENCE] The 2023 and 2024 national totals from the FBI Crime Data Explorer report race but not ethnicity (probed; cached in `_cache/cde/`). BJS's Hispanic-to-all adult imprisonment ratio fell from 1.416 in 2019 to 1.317 in 2023. Carrying the arrest ratio down by the same proportion gives −$1.50bn. The imprisonment ratio also moves with federal immigration prosecutions and time served, so it is a weak proxy for arrests. [DATA: *Prisoners in 2023*, Table 6; INFERENCE] Cost-weighting would push the other way: in the same table, Hispanic shares are higher for aggravated assault (25%), robbery (23%) and rape (29%) than overall (18.8%), and lower for larceny (14%). [DATA; INFERENCE]
- **Scaling assumptions.** Carrying the custody ratio over to arrests (m/p = 1.14) is an assumption. So is giving the extra 8.2% of target members the Mexican-coded rates; they include non-identifiers, who are plausibly lower-risk (−$0.71bn at national rates). The adjusted ratio also moves between files: 1.15 in the 2020–2024 5-year ACS and 1.08 in ACS 2016 (−$1.24bn at the 2016 value). Unadjusted, it runs 0.95–1.02.
- **What the keys leave out.** Community supervision (probation and parole) is inside prisons spending but keyed like custody; its Hispanic share was not obtained [UNVERIFIED direction]. The victimization key is violent crime only; property victimization by Hispanic origin is not in the held NCVS tables. Federal law-enforcement and federal-court immigration-offense caseloads, EOIR and USCIS (the latter also in subfunction 751) are not keyed separately.
- **Mismatched years.** BEA is CY2024, ICE/CBP FY2024, arrests 2019, BJS 2023, NCVS 2022–2024, ACS 2024 and CPS March 2025. The prisoner-survey check is 2016.
- **Scope.** These are costs of government services, not crime harm. No victim-harm price is added, per the account's crime-harm rule.
- **Instrument.** This allocation was built with an LLM on a politically charged topic. Each key's inputs and its disconfirming arm (NCVS offender, raw scaling, CBP boundary) are exported so the choices can be checked independently. [INFERENCE]

## Covered / skipped

Covered:
- BEA sublines with gates and the positive control.
- Fire per head.
- Prisons on the ACS 1-year and 5-year keys (raw, adjusted by population share and by institutional share), the BJS check and the ICE bound.
- Police on three keys plus the NCVS arm, with CBP and ICE custody carved out.
- Courts at three criminal shares.
- ICE custody under all three brief options plus the interior central and its bounds.
- ERO non-custody as a sensitivity only.
- The nativity split where keys allow it, with a labeled proxy otherwise.
- The effect on the band.
- The 2026-09-05 race and ethnicity audit, read after the first run:
  - the BJS check moved to *Prisoners in 2023*, with a gate that the 2022 row was not restated;
  - the bound for prisoners counted in both the prison and jail totals;
  - the SPI 2016 birthplace check against ACS 2016, read from the held microdata;
  - the ACS origin allocation flag;
  - two arrest-key sensitivities (2023 carry-forward, 2016 scaling).

Skipped, with reasons:
- **National arrests by ethnicity after 2019.** The Crime Data Explorer totals carry race only, and the ethnicity endpoints return 404.
- **Split of judicial and legal spending.** The BJS Justice Expenditure and Employment series does not split it into courts, prosecution and defense.
- **Probation and parole tables by Hispanic origin.** They were not found at the guessed BJS URLs. After a few attempts they were recorded as a gap rather than guessed.
- **Property victimization by Hispanic origin.** It is not in the held tables.
- **NCVS microdata.** The ICPSR login wall already recorded by the NCVS lane still applies.
- **Federal arrest, EOIR and USCIS keys.** Not built. Each is small against line 4, and none has a held key.
- **Texas arrest data and SPI Mexican detail.** The Texas files carry no race or ethnicity. The SPI public file carries no Mexican origin or country of birth.
- **USSC offender data.** It covers federal offenders only, and no microdata is held locally (audit).
- **Edits outside this directory and commits.** Out of scope per the brief.

## Reproduce

From the repository root; `acs_pull.py` needs the Census key in `infra/immigration-fiscal/acquire/config.local.env`, and its output passes through a redaction filter.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cj_use_allocation_2026_09_23/acs_pull.py 2>&1 | sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cj_use_allocation_2026_09_23/allocate.py
```

`allocate.py` runs 38 gates. They cover:
- source pins, including the SPI 2016 file (sha256 98970270…);
- label and sum checks, the positive control and the canonical target count;
- parser checks against the ICE, OHSS and BJS tables, plus the BJS cross-vintage check;
- the SPI birthplace counts against the audit;
- exact conservation of line 4 in all 576 key sets.

Outputs in `derived/`:
- `cj_allocation.csv`: subline × key → national, target, other, target share, nativity split;
- `key_sets.csv`, `central_split.csv` and `summary.json`;
- `key_inputs.csv`: every share with its source;
- the ACS tabulations `acs_hisp_nativity_gq.csv` (2024 1-year and 5-year; 2016 at 18–64), `acs_hisp_allocation_1864.csv` and `acs2019_adults.csv`.

The BJS prison tables are read from the tracked `bjs_p23st_extract.txt`, pdftotext output of the held PDF (sha256 22a4cbe8…). Raw pulls are in the ignored `_cache/`: ACS JSON; BJS `ji23stt01–05.csv` (Table 5 sha256 3736d8c1…); the OHSS workbook (sha256 aba84741…); the BEA concordance PDF (sha256 d86bba7c…); CDE probes.

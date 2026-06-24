# Immigration public MVP variable dictionary — 2026-04-11

## Purpose

This is the minimum variable dictionary for the public-use lifetime-fiscal MVP.

The point is not completeness.
The point is to prevent semantic mistakes while wiring the first modules.

## `SIPP 2024`

Core file:
- [pu2024_csv.zip](sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip)

Naming rules from the official guide:
1. `A*` = status flags
2. `E*` = edited variables
3. `R*` = recoded variables
4. `T*` = public-use topcoded / bottom-coded / collapsed variables [SOURCE: [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf), local `pdftotext` extract around section `6.1`]

### High-confidence `SIPP` variables

1. `SSUID`
   - person/household longitudinal identifier family [SOURCE: local header inspection in [public_mvp_input_profile_2026-04-11.json](sources/immigration-fiscal/data/derived/public_mvp_input_profile_2026-04-11.json)]
   - use: longitudinal linking base
   - confidence: `Medium`

2. `PNUM`
   - person number within the sample unit [SOURCE: local header inspection]
   - use: person-level linking under `SSUID`
   - confidence: `Medium`

3. `WPFINWGT`
   - final person weight [SOURCE: [SIPP_Data_Primer_MAY24.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/SIPP_Data_Primer_MAY24.pdf), local `pdftotext` extract]
   - use: descriptive weighting
   - confidence: `High`

4. `TAGE`
   - public-use age variable; `T*` means public-use collapsed/topcoded form [SOURCE: official naming rules + local header inspection]
   - use: working-age slice
   - confidence: `Medium`

5. `EBORNUS`
   - edited nativity / born-in-U.S. field [SOURCE: official naming rules + local header inspection]
   - use: nativity split
   - confidence: `Medium`
   - caveat: code meanings still need explicit decode before publication

6. `ECITIZEN`
   - edited citizenship field [SOURCE: official naming rules + local header inspection]
   - use: citizenship stratification
   - confidence: `Medium`
   - caveat: code meanings still need explicit decode before publication

7. `TYRENTRY`
   - public-use year-of-entry field [SOURCE: local header inspection + debug sampling]
   - use: recent-arrival classification
   - confidence: `Medium`

8. `EORIGIN`
   - edited origin field [SOURCE: official naming rules + local header inspection]
   - use: origin grouping
   - confidence: `Medium`
   - caveat: codebook decoding still needed

9. `EHISPAN`
   - edited Hispanic-origin field [SOURCE: official naming rules + local header inspection]
   - use: ethnicity split
   - confidence: `Medium`

10. `ERACE`
   - edited race field [SOURCE: official naming rules + local header inspection]
   - use: race split
   - confidence: `Medium`

11. `TPEARN`
   - monthly total earnings from all jobs [SOURCE: [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf), local `pdftotext` extract around page `73`]
   - use: labor-income transition model
   - confidence: `High`

12. `TSNAP_AMT`
   - public-use SNAP amount field [SOURCE: local header inspection + naming rules]
   - use: SNAP amount modeling
   - confidence: `Medium`

13. `TTANF_AMT`
   - public-use TANF amount field [SOURCE: local header inspection + naming rules]
   - use: TANF amount modeling
   - confidence: `Medium`

14. `TSSI_AMT`
   - public-use SSI amount field [SOURCE: local header inspection + naming rules]
   - use: SSI amount modeling
   - confidence: `Medium`

### `SIPP` variables we should not use casually

1. `A*` variables as if they were substantive values
   - they are status flags, not the underlying measure [SOURCE: official naming rules]

2. `TPEARN` as annual income
   - it is monthly total earnings [SOURCE: official guide]

3. `ECITIZEN` or `EBORNUS` code values without explicit codebook decode
   - current profiler uses raw-code frequencies only [SOURCE: [public_mvp_input_profile_2026-04-11.json](sources/immigration-fiscal/data/derived/public_mvp_input_profile_2026-04-11.json)]

## `MEPS HC-251`

Core files:
- [h251dat.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip)
- [h251dta.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dta.zip)
- [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)

### High-confidence `MEPS` variables

1. `PERWT23F`
   - person weight [SOURCE: `h251su.txt`]
   - use: weighted descriptive estimates
   - confidence: `High`

2. `AGE23X`
   - age as of end of 2023 [SOURCE: `h251su.txt` label block]
   - use: working-age slice
   - confidence: `High`

3. `SEX`
   - sex [SOURCE: `h251su.txt`]
   - use: demographic controls
   - confidence: `High`

4. `RACETHX`
   - race/ethnicity composite [SOURCE: `h251su.txt`]
   - use: descriptive stratification
   - confidence: `High`

5. `HISPANX`
   - Hispanic flag/category [SOURCE: `h251su.txt`]
   - use: ethnicity split
   - confidence: `High`

6. `BORNUSA`
   - person born in the U.S. [SOURCE: `BORNUSAF` value labels in `h251su.txt`]
   - code values:
     - `1` = yes
     - `2` = no
   - use: nativity split
   - confidence: `High`

7. `YRSINUS`
   - years lived in the U.S., categorical [SOURCE: `YRSINUSF` value labels in `h251su.txt`]
   - code values:
     - `1` = less than 1 year
     - `2` = 1 to <5 years
     - `3` = 5 to <10 years
     - `4` = 10 to <15 years
     - `5` = 15 years or more
   - use: rough tenure-in-U.S. grouping
   - confidence: `High`

8. `INSURC23`
   - annual insurance category [SOURCE: `INSURC23F` value labels in `h251su.txt`]
   - for under-65:
     - `1` = any private
     - `2` = public only
     - `3` = uninsured
   - use: insurance-status module
   - confidence: `High`

9. `TOTEXP23`
   - total health care expenditure, 2023 [SOURCE: `h251su.txt` labels]
   - use: total medical spending module
   - confidence: `High`

10. `TOTSLF23`
   - total paid by self/family [SOURCE: `h251su.txt` labels]
   - use: out-of-pocket burden
   - confidence: `High`

11. `TOTMCR23`
   - total paid by Medicare [SOURCE: `h251su.txt` labels]
   - use: Medicare incidence
   - confidence: `High`

12. `TOTMCD23`
   - total paid by Medicaid [SOURCE: `h251su.txt` labels]
   - use: Medicaid incidence
   - confidence: `High`

13. `TOTPRV23`
   - total paid by private insurance [SOURCE: `h251su.txt` labels]
   - use: private payer mix
   - confidence: `High`

14. `TOTSTL23`
   - total paid by other state/local sources [SOURCE: `h251su.txt` labels]
   - use: state/local medical incidence
   - confidence: `High`

## Immediate implementation rule

For the next build:

1. `SIPP` is the transition / transfers / labor spine.
2. `MEPS` is the health-cost module.
3. `IRS SOI county` is context only, not microsim tax truth.
4. `Synthetic SIPP` and `PSID` remain pending upgrades.

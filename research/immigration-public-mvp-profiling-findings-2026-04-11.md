# Immigration public MVP profiling findings — 2026-04-11

## Scope

This memo records the first lightweight profiling pass over the newly staged public-use datasets for the immigration lifetime-fiscal project.

It is intentionally narrow:

1. verify what the files actually contain
2. identify what can be modeled now
3. record the assumptions that failed immediately

It is **not** a final fiscal estimate.

## Artifacts produced

Profiler script:
- [profile_public_mvp_inputs.py](sources/immigration-fiscal/data/derived/profile_public_mvp_inputs.py)

Profiler output:
- [public_mvp_input_profile_2026-04-11.json](sources/immigration-fiscal/data/derived/public_mvp_input_profile_2026-04-11.json)

Supporting readiness memo:
- [immigration-public-mvp-readiness-2026-04-11.md](research/immigration-public-mvp-readiness-2026-04-11.md)

## Verified findings

### 1. `SIPP 2024` is the correct public-use transition spine

Verified facts:
1. The downloaded archive contains a single `pu2024.csv` payload of about `3.43GB`. [SOURCE: local unzip listing of [pu2024_csv.zip](sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip)]
2. The header contains `5203` fields. [SOURCE: local profiler output in [public_mvp_input_profile_2026-04-11.json](sources/immigration-fiscal/data/derived/public_mvp_input_profile_2026-04-11.json)]
3. The public file contains the key immigration/fiscal bridge fields we needed to verify exist: `EBORNUS`, `ECITIZEN`, `TYRENTRY`, `EORIGIN`, `EHISPAN`, `ERACE`, `WPFINWGT`, `TPEARN`, `TSNAP_AMT`, `TTANF_AMT`, `TSSI_AMT`. [SOURCE: same JSON artifact]

Interpretation:
1. `SIPP 2024` can support a serious public-use transition model for work, transfers, nativity, and household structure. [INFERENCE]
2. This is enough to stop saying "ACS is all we have". [INFERENCE]

### 2. The `SIPP` naming conventions matter enough to invalidate naive use

Official guidance from the `2024 SIPP Users Guide`:
1. variables starting with `A` are status flags
2. variables starting with `E` are edited variables
3. variables starting with `R` are recoded variables
4. variables starting with `T` are public-use topcoded, bottom-coded, or collapsed variables [SOURCE: [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf), local `pdftotext` extract from section `6.1`]

Real consequence:
1. The first pass incorrectly treated some `A*` fields as substantive values.
2. That was wrong.
3. The profiler was corrected to use `TAGE`, `TYRENTRY`, and `TPEARN` instead of `AAGE`, `AYRENTRY`, and `APEARN`. [SOURCE: local script revision in [profile_public_mvp_inputs.py](sources/immigration-fiscal/data/derived/profile_public_mvp_inputs.py)]

Interpretation:
1. `SIPP` can support the public MVP, but only with codebook-level discipline. [INFERENCE]
2. Variable-prefix sloppiness will generate fake empirical results quickly. [INFERENCE]

### 3. `TPEARN` is monthly, not annual

The `2024 SIPP Users Guide` states that `TPEARN` / `TPEARN_ALT` are `monthly total earnings from all jobs`. [SOURCE: [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf), local `pdftotext` extract around page `73`]

Interpretation:
1. Any annual-income interpretation of `TPEARN` would be wrong. [INFERENCE]
2. The current profiler output uses the correct label: `foreign_working_age_mean_monthly_total_earnings_TPEARN`. [SOURCE: profiler JSON]

### 4. The first `SIPP` sample pass is good enough for module design, not for national point estimates

From the first streamed sample of `200,000` rows:
1. weighted foreign-born share in the sampled rows is about `14.55%` using `EBORNUS == 2` as the foreign-born inference. [SOURCE: profiler JSON] [INFERENCE]
2. among sampled foreign-born working-age rows, about `22.4%` have `TYRENTRY >= 2014`, so the public file can support a meaningful `recent-arrival` branch. [SOURCE: profiler JSON]
3. sampled foreign-born working-age monthly total earnings on `TPEARN` are about `$6,932`. [SOURCE: profiler JSON]
4. sampled positive-transfer shares are low on `TSNAP_AMT`, `TTANF_AMT`, and `TSSI_AMT` in this first pass. [SOURCE: profiler JSON]

Caveats:
1. This is a streamed sample from the first `200,000` rows, not a full-file national estimate. [SOURCE: profiler JSON notes]
2. `EBORNUS` and `ECITIZEN` code meanings were not yet decoded from the public documentation in this pass, so those code-to-meaning mappings remain partially inferred. [SOURCE: profiler JSON notes]

Interpretation:
1. `SIPP` is empirically useful now for transition modeling.
2. It is not yet ready to be cited as a clean national estimate layer until we do a fuller weighted pass and decode the remaining categorical fields. [INFERENCE]

### 5. `MEPS HC-251` is strong enough for a health-cost module right now

Verified facts:
1. The public files are on disk in `.dat`, `.dta`, and documentation form. [SOURCE: local files under `sources/immigration-fiscal/data/external/stage3/ahrq/meps/`]
2. The SAS setup file shows the health spending variables we need: `TOTEXP23`, `TOTSLF23`, `TOTMCR23`, `TOTMCD23`, `TOTPRV23`, `TOTSTL23`. [SOURCE: [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)]
3. The setup file also shows `BORNUSA`, `YRSINUS`, `RACETHX`, `HISPANX`, `PERWT23F`, and `INSURC23`. [SOURCE: same setup file]

Interpretation:
1. `MEPS` closes the payer-incidence and medical-spending side of the public model better than the current warehouse does. [INFERENCE]

### 6. `MEPS` suggests foreign-born age 25-64 adults are cheaper on observed annual medical spending than U.S.-born adults

Using the full `h251.dat` file, parsing only selected fields through the official SAS layout:
1. `BORNUSA == 1` (`Yes`, born in the U.S.) has weighted mean total 2023 health expenditures of about `$7,973`. [SOURCE: profiler JSON + `BORNUSAF` label in [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)]
2. `BORNUSA == 2` (`No`, not born in the U.S.) has weighted mean total 2023 health expenditures of about `$4,626`. [SOURCE: same]
3. Medicaid-paid mean spending is about `$1,065` for U.S.-born vs about `$623` for foreign-born in the age `25-64` slice. [SOURCE: same]
4. Positive Medicaid-paid share is very similar: about `16.41%` U.S.-born vs `16.16%` foreign-born. [SOURCE: same]

Interpretation:
1. A public-use health-cost module will likely pull the low-skill immigrant ledger less negative than a crude "high Medicaid burden" story would suggest. [INFERENCE]
2. That is not enough to settle lifetime fiscal impact, but it is enough to reject a simplistic assumption that foreign-born working-age adults are obviously more expensive in annual medical spending. [INFERENCE]

### 7. `MEPS` also shows a different insurance mix for foreign-born adults

The `INSURC23` value labels are:
1. `1` = `<65 any private`
2. `2` = `<65 public only`
3. `3` = `<65 uninsured` [SOURCE: `INSURC23F` labels in [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)]

Within the age `25-64` slice:
1. U.S.-born adults are mostly code `1` (`<65 any private`). [SOURCE: profiler JSON]
2. Foreign-born adults are also mostly code `1`, but with a larger uninsured code `3` mass than U.S.-born adults. [SOURCE: profiler JSON]

Approximate implication from the weighted code masses:
1. foreign-born age `25-64` look materially more uninsured than U.S.-born age `25-64` in `MEPS 2023`. [INFERENCE]

Interpretation:
1. This likely lowers direct public medical spending relative to natives, while increasing out-of-pocket / uninsurance exposure. [INFERENCE]
2. That matters for fiscal accounting, but it is not the same thing as "better welfare". [FRAMING-SENSITIVE]

### 8. `YRSINUS` in `MEPS` is categorical, not literal years

Official `MEPS` labels for `YRSINUS` are categories:
1. `1` = less than `1 year`
2. `2` = `1` to `<5 years`
3. `3` = `5` to `<10 years`
4. `4` = `10` to `<15 years`
5. `5` = `15 years or more` [SOURCE: `YRSINUSF` labels in [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)]

Interpretation:
1. The initial arithmetic mean of `YRSINUS` should not be read as literal years in the U.S.
2. The corrected profiler now reports `YRSINUS` code distributions instead. [SOURCE: profiler JSON]
3. Most foreign-born age `25-64` weight mass in this file sits in category `5` (`15 years or more`). [SOURCE: profiler JSON]

## Realization log

### Realization 1

`SIPP` is powerful enough to matter, but easy enough to misuse that a casual pass is dangerous.

Why this matters:
1. The naming conventions are not cosmetic.
2. They change the meaning of the variable completely.
3. The public MVP needs a small variable dictionary before it needs a giant ingest. [INFERENCE]

### Realization 2

`MEPS` is stronger than expected for the health-cost side.

Why this matters:
1. We do not need to guess health-cost incidence anymore.
2. We can build that module now, using public data already on disk. [INFERENCE]

### Realization 3

The SSD `IRS SOI` mirror is still the wrong object for household tax microsimulation.

Why this matters:
1. County aggregates are useful context.
2. They do not solve the federal-tax layer.
3. We still need the actual individual `IRS SOI` public-use file or an equivalent calibration object. [SOURCE: [immigration-public-mvp-readiness-2026-04-11.md](research/immigration-public-mvp-readiness-2026-04-11.md)]

### Realization 4

The public MVP should be built as a modular scenario engine, not as a one-shot scalar NPV calculator.

Why this matters:
1. `SIPP` gives transitions.
2. `MEPS` gives payer incidence.
3. `PSID` would give descendant / family dynamics.
4. `Synthetic SIPP` would tighten the earnings-transfer spine.
5. None of these by itself yields a one-number ground truth. [INFERENCE]

### Realization 5

The strongest immediate next step is not more acquisition. It is a variable dictionary and a minimal ingest plan.

Why this matters:
1. We now have enough data to start building.
2. The failure mode is no longer `missing files`.
3. The failure mode is `wrong semantics`. [INFERENCE]

## Recommended next build order

1. Create a small `SIPP` variable dictionary for the immigration/fiscal slice: nativity, citizenship, year of entry, monthly earnings, SNAP, TANF, SSI, household identifiers, weights. [INFERENCE]
2. Ingest `MEPS` from the `.dta` or continue using the fixed-width parser, and build the health-cost module. [INFERENCE]
3. Acquire the individual `IRS SOI` public-use file or lock down its access path. [INFERENCE]
4. Get `PSID` through its Data Center to support descendant dynamics. [INFERENCE]
5. Apply for `Synthetic SIPP` to narrow the gap to linked admin trajectories. [SOURCE: [Synthetic SIPP page](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html)]

## Hard stop claims

These claims would still be too strong right now:

1. "We have replaced NAS."
2. "We can estimate undocumented-specific lifetime taxpayer value from public data alone."
3. "County IRS SOI solves the federal tax microsim problem."
4. "The first `SIPP` sample pass is a national point estimate."

Those are not true yet. [INFERENCE]

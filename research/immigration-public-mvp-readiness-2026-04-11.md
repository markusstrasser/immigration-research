# Immigration public-use MVP readiness — 2026-04-11

## Bottom line

We now have enough public-use data on disk to build a materially better `public MVP` lifetime-fiscal model than the current ACS-only / NAS-overlay state. We do **not** yet have enough to replace a linked administrative model for undocumented-specific or fine-origin lifetime estimates.

The correct interpretation is:

1. `SIPP 2024` gives the short-run household, earnings, and program-participation spine.
2. `MEPS HC-251` gives the health-cost and payer-incidence side.
3. `IRS SOI` on the SSD gives county aggregates and migration context, but **not** the individual Public Use File needed for tax microsimulation.
4. `Synthetic SIPP` exists and is obtainable, but it is application-gated and synthetic by design.
5. `PSID` public data exist and are usable for descendant / long-run family dynamics, but acquisition is account/session-gated enough that scripted download is brittle.

## What is now verified on disk

### `SIPP 2024`

Local path:
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip`

Verified local facts:
- Zip contains one file: `pu2024.csv`
- Compressed payload listing shows file length `3,433,662,421` bytes `[SOURCE: local unzip listing, 2026-04-11]`
- Header inspection shows `5203` columns `[SOURCE: local header inspection, 2026-04-11]`
- Header includes the immigration-relevant fields `EBORNUS`, `ECITIZEN`, `AYRENTRY`, `EORIGIN`, `EHISPAN`, `ERACE` `[SOURCE: local header inspection, 2026-04-11]`

Implication:
- This is not a toy supplement. It is a real longitudinal household survey spine with nativity / citizenship / year-of-entry fields present in the public file.

What is now built:
- `sipp_public_mvp_cells_2024.csv` is now available and has `98` working-age profile cells [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/sipp_public_mvp_cells_2024.meta.json`].

### `MEPS HC-251`

Local paths include:
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dta.zip`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251doc.pdf`

Verified local facts:
- `h251dat.zip` contains one file: `h251.dat`, length `73,878,695` bytes `[SOURCE: local unzip listing, 2026-04-11]`
- `h251dta.zip` contains one file: `h251.dta`, length `47,062,321` bytes `[SOURCE: local unzip listing, 2026-04-11]`
- SAS setup file exposes `BORNUSA`, race/ethnicity fields, monthly Medicaid indicators `MCD*`, Medicare indicators `MCARE*`, and spending totals like `TOTMCD23` `[SOURCE: local grep of h251su.txt, 2026-04-11]`

Implication:
- Use the Stata file, not the ASCII fixed-width file, unless there is a parsing problem.
- MEPS gives payer-specific medical spending and insurance exposure, but does **not** appear to expose a clean citizenship / undocumented-status field in the inspected public setup material.

### `SIPP -> MEPS bridge`

Artifacts:
- [sipp_meps_bridge_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv)
- [sipp_meps_expected_health_cost_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv)
- [sipp_meps_bridge_cells_2024.meta.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.meta.json)

Verification:
- `sipp_rows_input`: `98`
- `meps_rows_input`: `81`
- `sipp_rows_matched_exact`: `98`
- `sipp_rows_matched_group_fallback`: `0`
- `sipp_rows_unmatched`: `0`
- `bridge_rows_written`: `294`
- `expected_rows_written`: `98`

Interpretation:
- SIPP-to-MEPS mapping is complete under exact age-band/nativity-code matching for all current rows; bridge output is now expected-health ready for scenario scoring.

### `IRS SOI` already on the SSD

Local path:
- `/Volumes/SSK1TB/corpus/irs_soi`

Verified local facts:
- Directory families present: `990_index`, `corporate`, `county`, `exempt_org` `[SOURCE: local bounded find, 2026-04-11]`
- County files include annual aggregates like `22incyallagi.csv` `[SOURCE: local bounded find, 2026-04-11]`
- `22incyallagi.csv` is county/state aggregate tabulation with headers like `STATEFIPS, STATE, COUNTYFIPS, COUNTYNAME, agi_stub, N1, ...` `[SOURCE: local CSV header inspection, 2026-04-11]`

Implication:
- The SSD mirror is useful for county tax-base context and some calibration.
- It is **not** the IRS individual Public Use File and cannot stand in for household tax microsimulation.

## What the official sources say about the missing pieces

### `Synthetic SIPP`

Official Census page says:
- researchers must submit an application
- once approved, Census provides SecureFTP credentials
- there are `four` data files, each about `3-4 GB`
- users can download SAS or Stata versions
- Census explicitly warns users not to publish unvalidated results without requesting validation against the confidential gold-standard files `[SOURCE: https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html]`

Implication:
- `Synthetic SIPP` is public-accessible in the broader sense, but not open-click downloadable like ACS.
- It is the strongest public stand-in for linked `SIPP-SSA-IRS`, but it remains synthetic and validation-sensitive.

### `PSID`

Official PSID FAQ says:
- the `Data Center` is the main automated mechanism for obtaining customized files
- downloads can be generated in ASCII, SAS, SPSS, and Stata formats
- packaged files also exist for users who prefer them `[SOURCE: https://psidonline.isr.umich.edu/Guide/FAQ.aspx?Type=ALL]`

Implication:
- `PSID` public data are real and accessible.
- The practical blocker is web/session gating, not nonexistence.
- It is a good long-run family / descendant dataset, but not an immigrant-tax administrative spine.

### `IRS SOI individual Public Use File`

Official IRS page states:
- individual public-use microdata files are available for tax years `2012-2015`
- they are statistically altered to protect confidentiality `[SOURCE: https://www.irs.gov/statistics/soi-tax-stats-individual-public-use-microdata-files]`

Implication:
- There is a public microdata tax file, but it is not what is currently mirrored on `SSK1TB`.
- If we want a tax microsim calibration layer, we should acquire the official individual PUF rather than pretending county SOI is enough.

## What each dataset can credibly do

### `SIPP 2024`

Strong use cases:
1. household transitions
2. program participation profiles
3. short-run earnings / employment dynamics
4. nativity / citizenship / year-of-entry stratification
5. public-use federal benefit exposure modeling

Weak use cases:
1. exact tax liability
2. undocumented-status identification
3. lifetime earnings paths without extrapolation
4. descendant adult outcomes
5. return migration and old-age cost modeling

Assessment:
- `Strong` for the transition model
- `Medium` for near-term federal transfer modeling
- `Weak` for terminal lifetime NPV without added modules

### `MEPS HC-251`

Strong use cases:
1. medical spending incidence
2. payer mix
3. Medicaid / Medicare utilization profiles
4. health-cost calibration by household/person profiles

Weak use cases:
1. immigrant legality
2. fine-origin lifetime trajectories
3. descendant modeling
4. longitudinal lifetime fiscal paths by itself

Assessment:
- `Strong` for health-cost incidence
- `Weak` for immigration-specific identification

### `IRS SOI county aggregates`

Strong use cases:
1. county tax-base context
2. filing / AGI distribution context
3. broad destination calibration

Weak use cases:
1. household tax microsimulation
2. immigrant-specific tax liability
3. undocumented-specific anything

Assessment:
- `Medium` for contextual calibration
- `Contextual-only` for lifetime fiscal modeling

### `Synthetic SIPP`

Strong use cases:
1. public-use stand-in for linked earnings / benefit trajectories
2. monthly transitions richer than plain SIPP
3. validation-oriented synthetic analysis before secure-data escalation

Weak use cases:
1. exact rare-group estimates
2. undocumented-specific lifetime values
3. clean replacement for true linked admin data

Assessment:
- `Strong` for a public-use fiscal microsim spine
- `Medium` to `Weak` where exactness or rare cells matter

### `PSID`

Strong use cases:
1. intergenerational persistence
2. family formation and household structure over long horizons
3. descendant and mobility modules

Weak use cases:
1. direct immigrant legal-status identification
2. tax admin truth
3. large-sample origin-by-origin immigrant fiscal analysis

Assessment:
- `Strong` for descendant dynamics
- `Weak` for immigrant-specific tax/budget incidence by itself

## What remains genuinely blocked

These are not solved by the acquired public files:

1. undocumented-status identification over time
2. actual tax-return histories linked to immigrant households
3. descendant adult outcomes for small immigrant-origin cells with strong precision
4. return migration / mortality / late-life-cost paths for undocumented or low-skill immigrant subgroups
5. a clean federal-state-local integrated ledger without additional modeling assumptions

Those are the reasons a public-use model still cannot honestly claim to have fully replaced `NAS`.

## What we should build next

### `Phase 1: public MVP scaffold`

1. Keep `SIPP 2024` zipped for now; do not fully expand it until we profile ingestion disk impact more carefully.
2. Bridge the SIPP module to MEPS expected health-cost cells for scenario inputs (now present).
3. Use `MEPS h251.dta` as the default ingest target, not the fixed-width `.dat`.
4. Acquire the official `IRS SOI` individual Public Use File, because the SSD mirror does not contain the right object for tax microsimulation.
5. Acquire `PSID` via its Data Center or packaged files manually if scripted fetch remains brittle.
6. Apply for `Synthetic SIPP` now rather than later; it is the only high-value public-use upgrade that materially narrows the admin-data gap.

### `Phase 2: model modules`

1. `SIPP module`
   - transition model for income, work, benefits, household composition
2. `MEPS module`
   - health spending / payer incidence by profile
3. `SIPP-MEPS bridge module`
   - expected health-cost profile for each SIPP cell
4. `IRS PUF module`
   - federal tax mapping / calibration
5. `PSID module`
   - descendant and long-run family dynamics
6. `ACS / existing warehouse bridge`
   - map current immigrant-origin composition into the public MVP modules

## What not to do

1. Do not use county `IRS SOI` aggregates as if they were an individual tax microdata replacement.
2. Do not use `MEPS` as if it solved immigration-status identification.
3. Do not use `SIPP 2024` alone as if it solved lifetime fiscal impact.
4. Do not claim public-use data can currently identify undocumented-specific lifetime taxpayer value with high confidence.

## Best current interpretation

We now have a credible path to a `public-use de-biased fiscal model`.

We do **not** yet have a `public-use final answer`.

The strongest path from here is:

1. acquire `IRS SOI` individual PUF
2. secure `Synthetic SIPP` access
3. ingest `MEPS` through the `.dta`
4. get `PSID` through the Data Center
5. then build the public MVP as a scenario engine rather than a fake-precise scalar estimator

### `Phase 3: bridge integration`

1. consume `sipp_meps_expected_health_cost_cells_2024.csv` directly in the scenario score layer, alongside SIPP transfer and earnings cells
2. preserve bridge match and imputation provenance in any downstream output

## Additional artifacts staged during this pass

### `Synthetic SIPP` local support files

Downloaded:
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/census/sipp/SSB_Application_clean_07.02.24.docx`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/census/sipp/GSF_v7_Codebook.pdf`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/census/sipp/SSB_Request_Guidelines_May_2024.docx`
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/census/sipp/CLEARANCE_REQUEST_MEMO_SSBupdate_5.24.24.docx`

These matter because they convert `Synthetic SIPP` from a vague future idea into a concrete application path.

### `IRS SOI` page snapshot

Downloaded:
- `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/irs/irs_soi_individual_puf_page.html`

This is useful as a local record of the current official IRS framing that the individual PUF exists for tax years `2012-2015`, but is not exposed on-page as an obvious static file link in the fetched markup.

### `PSID`

`PSID` FAQ content was successfully retrieved through Exa crawling for research purposes, but direct `curl` fetch to the live site failed with transport/session errors during this pass. Treat that as an acquisition-friction issue, not a nonexistence issue.

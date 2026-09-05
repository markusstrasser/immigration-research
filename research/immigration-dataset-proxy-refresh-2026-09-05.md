**Verdict:** Three dataset families were procured and inspected, and the principal checks now ran: June ICE detention exits reconcile to the raw workbook; matched June–August BLS employment counts fell for both native and foreign-born groups across a population-control revision; all 780 BEA 2024 hierarchy checks balance exactly. Three dataset families plus an existing BEA corpus support descriptive and accounting conclusions, not a national causal fiscal/crime effect of immigration. [DATA; INFERENCE]

# Dataset and proxy refresh — 2026-09-05

**Mode:** acquisition and descriptive screen. **Recent-source window:** June 5–September 5, 2026. Release dates and observation vintages are distinguished. **Frame:** incumbent labor outcomes, local capacity and explicit fiscal components. Entrant welfare and total national net fiscal value are outside these measurements. The selection is LLM-conducted; mirrored tests for favorable and unfavorable narratives are stated to counter selection bias.

## Existing inventory and actual gaps

The current [dataset register](immigration-dataset-register.md) already covers ACS PUMS, QWI/QCEW, PIT/HIC/BPS threshold assets, CHAS, SAFMR, Zillow, historical SNAP, DHS annual/budget reports and Texas crime replication. The [current receiver-node correction](immigration-receiver-node-kill-test-2026-04-23.md) states that QWI has no nativity, court venue is not residence, and the area-weighted PUMA bridge is not a validated county estimate. The acquisitions target these measurement gaps rather than rescore that nine-node screen. [SOURCE]

Read-only inventory used `/Volumes/2TBPNY/research-data/immigration-fiscal/data` because the repository source links are broken. A broader SSD filename search located `/Volumes/2TBPNY/corpus/bea_data/SAINC/SAINC35__ALL_AREAS_1929_2024.csv`, with its neighboring definition XML and footnotes. The project register's HIC/BPS entries were recognized before acquisition; the exact mounted legacy causal path remains unresolved. BPS files acquired here are specified new vintages, while no HIC/PIT duplicate was pulled. [DATA; GAP]

**Staging:** `.scratch/frontier-20260905/datasets/`. **Reproducer:** `uv run --no-project --with openpyxl python3 infra/immigration-fiscal/acquire/refresh-frontier-20260905.py`. **Manifest/inspection:** `manifest.json`, `inspection.json`, `principal_checks.json`. Source files are never overwritten; HEAD probes and a 25 MB per-file ceiling were used. The initial acquisition brought 17 data/documentation/license files totaling 2,017,629 bytes, with zero acquisition errors. The manifest now also registers the 58,060-byte pinned GitHub tree: 18 files, 2,075,689 bytes. Probes, generated audits and run logs are additional small artifacts. [DATA]

The script bootstraps an absent `probes/vera-tree.json` from the pinned GitHub tree `a6bf48e2627323f01827d52776f0d08023c410ba`; it requires an exact tree ID and a complete, non-truncated listing before proceeding. It preserves an existing file and refuses a wrong tree without overwriting it. The absent-probe fetch, unchanged-file reuse, and wrong-tree refusal were actually exercised in isolated temporary staging directories; all passed. Existing raw data were untouched. Reproducer validation: `uv run --no-project --with openpyxl python3 .scratch/frontier-20260905/datasets/validate_refresh_script.py`, logged in `reproducer-validation.log`. [DATA]

## Candidate mechanisms, estimands and falsifiers

| Candidate / status | Supported estimand | Proxy failure | Join key / time | Can falsify which narrative? |
|---|---|---|---|---|
| **BLS CPS nativity — ACQUIRED** | Native/foreign-born employment counts, employment-population ratios and unemployment rates, nationally | Age/composition, population controls, nonresponse, seasonality; no legal status or local treatment comparison | Nativity × metric × calendar month; 16+ national | Blanket “all native outcomes deteriorated while immigrant employment grew” can fail on actual native ratios. Better native outcomes do not prove immigration caused them. |
| **County BPS — REFRESH ACQUIRED** | Authorized private residential units; reported versus estimated quantity | Permits are not completed/occupied units; demolitions and unpermitted housing omitted | State+county FIPS × year/month; retain boundary version | Uniform supply rigidity can fail where authorization expands. Authorization alone cannot falsify shortage of completed housing. |
| **ICE detention — ACQUIRED** | Detention stock, initial book-ins, final book-outs and subset removed | Enforcement-selected population; exits are not all removals; incomplete month; events not arrival/stock counts | Fiscal year × year_month plus observation cutoff/source date | “All detention exits are deportations” can be tested from release reasons. “More detention proves more arrivals” is not warranted. |
| **BEA SAINC35 — EXISTING AUDITED** | Gross transfer receipts by retirement/medical/income-maintenance component | No nativity, tax side or complete expenditure ledger; nested categories overlap | GeoFIPS × LineCode × calendar year | Can test whether specified means-tested programs account for aggregate growth. Retirement/Medicare growth alone cannot falsify immigrant attribution: immigrants can receive those programs too. |
| **HUD HIC/PIT — EXISTING, NO DUPLICATE** | Program beds and people counted on one January night | Program inventory excludes parts of migrant hotel/shelter system; PIT misses many housed/doubled-up migrants; CoC != county | CoC × year with explicit crosswalk | Flat utilization need not mean no load if capacity expanded; rising PIT cannot automatically be assigned to immigration. |
| **SNAP May 2026 state tables — VERIFIED AVAILABLE, NOT STAGED** | Participants, households and gross benefits; amount/caseload decomposition | Mixed-status households, eligibility and benefit-policy changes; no taxes | State × month, fiscal/calendar convention explicit | Higher spending need not mean more immigrant recipients if benefit levels explain it. |
| **FBI reporting coverage/status denominator — GAP** | Agency coverage and reported offenses; status rates only with compatible population denominator | Agency reporting differs from victim reporting; national FBI totals lack unauthorized-status denominator | ORI × month/year, months reported, population served | Measured crime change can fail a propensity interpretation if coverage shifts explain it; a general national panel cannot establish undocumented/native rates. |

These are seven different measurement mechanisms, not independent causal estimates. Outcomes, detention throughput, supply authorization, fiscal receipts, program capacity, benefit caseloads and reporting coverage must remain distinct. [INFERENCE]

## Actual row/schema inspection

### BLS_CPS_NATIVITY_MONTHLY

[Official Table A-7 dictionary](https://www.bls.gov/webapps/legacy/cpsatab7.htm); [example direct API payload](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU02073395?startyear=2021&endyear=2026). BLS measures nativity, not immigration legal status. These NSA series cover civilian noninstitutional population aged 16+. Levels are thousands; rates/ratios are percentages. Employment-population ratio divides by population; unemployment rate divides by labor force. Native-born includes people born abroad to a U.S.-citizen parent. January population-control changes can disrupt levels. [SOURCE]

The raw API JSONs yield **544 series-month rows, 8 series, 2021-01–2026-08**, with **0 duplicate series/date keys** and **8 missing reported values**. All eight missing values are October 2025; BLS footnote 9 attributes their unavailability to the lapse in appropriations. Missing markers are preserved, never converted to zero. These are data-integrity counts, not sampling-error estimates. [DATA: source JSON footnotes and derived CSV]

Latest month (2026-08):

| Nativity | Metric | Value | Unit |
|---|---|---:|---|
| foreign_born | population | 48504 | thousand persons |
| foreign_born | employed | 30780 | thousand persons |
| foreign_born | employment_population_ratio | 63.5 | percent |
| foreign_born | unemployment_rate | 3.4 | percent |
| native_born | population | 226911 | thousand persons |
| native_born | employed | 131887 | thousand persons |
| native_born | employment_population_ratio | 58.1 | percent |
| native_born | unemployment_rate | 4.6 | percent |

Series mapping: `LNU000` population, `LNU020` employed, `LNU023` employment-population ratio, `LNU040` unemployment rate; suffix `73395` foreign-born, `73413` native-born. Preserve source footnotes. Compare matching calendar months and counts beside ratios; do not infer immigration effects from national co-movement. Age/education/sex-standardized CPS microdata remain needed for native distributional outcomes. [SOURCE; INFERENCE]

**Vintage:** through August 2026; retrieved September 5. **License:** federal public-use statistics. The codebook was read via the official BLS table in Exa/web; direct HTTP to the page returned 403, whereas its statistical API worked. A local dictionary excerpt is provided alongside staging.

### CENSUS_BPS_COUNTY_2025_2026

[Official program](https://www.census.gov/permits); [county directory](https://www2.census.gov/econ/bps/County/). Annual 2025 was released May 14, 2026, outside the recent-release window. May–July current-month files were posted June 24, July 24 and August 25, inside it. [SOURCE]

Schema: survey date; state/county FIPS; region/division; county name; buildings/units/value for one-unit, two-unit, 3–4-unit and 5+-unit buildings, followed by corresponding reported-subset fields. Raw dual headers are preserved. All acquired data rows have **30 fields**, zero blank/special-marker cells, and keys audited as follows. FIPS must stay zero-padded strings. [DATA]

| File | County rows | Duplicate date/FIPS keys | Authorized units | Reported subset units |
|---|---:|---:|---:|---:|
| co2025a.txt | 3029 | 0 | 1431616 | 1298881 |
| co2605c.txt | 3019 | 0 | 120665 | 93838 |
| co2606c.txt | 3018 | 0 | 130677 | 102726 |
| co2607c.txt | 3018 | 0 | 129049 | 100591 |

Example principal row: annual 2025 Autauga County, Alabama (`01`+`001`) reports 200 one-unit buildings/units and 82,131,895 in value; the reported subset also contains 200 units. May 2026 uses survey-date code `202605`, not fiscal-month indexing. [DATA: raw file rows]

These sums are **gross units authorized in the source file's permit universe**, not net completed housing or immigration-attributable supply. Reported-subset units must not be added to total units. The larger fields include estimation/imputation; do not use reported fractions as uncertainty weights until the detailed survey methodology is read. Annual and monthly totals have incompatible time bases for a simple growth-rate comparison. [INFERENCE]

**Codebook:** raw headers plus `bps/documentation-index.html` (a locator, not a substitute for the complete methodological document). **License:** federal public-use data. **Gap:** a verified completion/occupancy series is needed to turn authorization into effective capacity.

### ICE_DETENTION_VERA_ARCHIVE

[Agency source](https://www.ice.gov/detain/detention-management#stats); [Vera archive/README](https://github.com/vera-institute/ice-fytd-stats). Vera states that raw ICE workbooks are preserved apart from filenames and separately supplies processed tables. This is primary administrative data reached through an advocacy organization's archive; it is not independent corroboration of the agency. [SOURCE]

The newest eligible FY2026 file in the captured archive is `2026-07-20_FY26_detentionStats07202026.xlsx`; this does **not** establish that July 20 was ICE's latest release as of September 5. Raw Git blob: `c7ae1944677aa023e2fce06f9fd27309d88df254`. The processed monthly summary has **94 data rows** and **9 columns**. The script inspected every raw sheet's nonempty rows and stored sheet dimensions/sample rows in `inspection.json`. [DATA]

Last three processed-source rows:

| year_month | fiscal_year | initial_bookins | adp | final_bookouts | final_bookouts_release_to_remove | percent_of_final_bookouts_as_removals | table_date | file_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026_05 | 2026 | 34079 | 58191.71 | 36196 | 29597 | 81.77 | 2026-07-11 | 2026-07-21 |
| 2026_06 | 2026 | 43138 | 59425.33 | 34551 | 27679 | 80.11 | 2026-07-11 | 2026-07-21 |
| 2026_07 | 2026 | 17525 | 65634.42 | 15681 | 12251 | 78.13 | 2026-07-11 | 2026-07-21 |

The July row is partial relative to the source cutoff; do not compare it to a complete month. Detention average daily population is an average stock, book-ins are flows and removed book-outs are only one exit category. Detention removals omit other removal processes; neither book-ins nor exits measure arrivals or net immigration. [SOURCE: README and raw workbook footnotes; INFERENCE]

Missing cells by source field: year_month=0; fiscal_year=0; initial_bookins=0; adp=0; final_bookouts=60; final_bookouts_release_to_remove=60; percent_of_final_bookouts_as_removals=60; table_date=0; file_date=0. Duplicate fiscal-year/month keys: zero. The README is the processed codebook and `Footnotes` is the raw workbook dictionary. The completed-June principal check below verifies header/date alignment and both exit cells. A complete row-for-row audit of all historical Vera transformations was not performed; this validation certifies the specified June observation, not the entire time series. [DATA; GAP]

**License:** archived `ice/License.md` permits research/nonprofit use and restricts dissemination/commercial use; keep the staged dataset local, outside tracked/public data. Both raw and processed files retain their acquisition chain.

### BEA_SAINC35_1929_2024 — existing corpus discovered

Principal: `/Volumes/2TBPNY/corpus/bea_data/SAINC/SAINC35__ALL_AREAS_1929_2024.csv`. **Bytes:** 1813615; **SHA-256:** `497d84f5613b5d2a33e580840cc3dd19b6ac0f012f10187718016d09b2c768b7`; **rows read:** 2644, comprising 2640 104-field data rows and four one-field source/footnote rows. New download: none. [DATA]

Columns include GeoFIPS, GeoName, Region, TableName, LineCode, IndustryClassification, Description, Unit and years 1929–2024. Geography values carry surrounding padding/quotes; strip them deliberately and exclude note rows before asserting key uniqueness. Preserve `(NA)` and suppression codes. The existing `SAINC35__definition.xml` and `SAINC35__Footnotes.html` are adjacent codebook files. [DATA]

A source row for the United States in 2024 is **4,555,385,000 thousand nominal dollars** of personal current transfer receipts (LineCode 1000). This is a gross receipt total for all recipients, not immigrant spending or net fiscal cost. Components include Social Security, Medicare, Medicaid, income maintenance and unemployment insurance. Parent/subtotal rows overlap; summing them double counts. Taxes, other expenditures and individual nativity are absent. [DATA; INFERENCE]

Original acquisition date was not reconstructed, so this is **discovered existing**, not “acquired September 5.” It can decompose a state-year benefits numerator after matching geography and denominator data. It cannot identify immigrants' use of those programs. [INFERENCE]

## Completed principal checks — 2026-09-05

All results in this section are generated by `principal_checks()` in the acquisition script and saved to `principal_checks.json`. The associated BLS table is `bls/matched_calendar_months.csv`. The script was rerun successfully on the acquired files; no new large data were downloaded. [DATA]

### ICE: June 2026 raw-to-processed equality, including the cutoff

**Exact raw version:** `2026-07-20_FY26_detentionStats07202026.xlsx`, SHA-256 `f83255a56773a7f7a53e46a72ed3bf742397db03eaf14f6abe3f9b07744d28a6`. In `Detention FY26`, cell A36 names the FY2026 book-out table, K37 is **Jun**, K38 is the total, and K71 is the **Release to Remove** total. `Footnotes!B60` gives an observation cutoff of July 11, 2026 and a run date of July 12. The processed CSV's June row has `table_date=2026-07-11` and `file_date=2026-07-21`. Thus June is a completed calendar month, and the July 20 archive filename / July 21 processed file date are not mistaken for observation dates. [DATA: workbook cells and CSV]

| June quantity | Raw workbook | Processed CSV | Difference |
|---|---:|---:|---:|
| All final detention book-outs | 34,551 | 34,551 | 0 |
| Release-to-remove book-outs | 27,679 | 27,679 | 0 |
| Other final book-outs, derived | 6,872 | 6,872 | 0 |
| Removal-exit share of all final book-outs | 80.11% | 80.11% | 0.00 pp |

The share is 27,679 / 34,551, rounded to the source's two decimals. This directly rejects equating **all detention exits with removal exits** for June. It says nothing by itself about all-agency removals, new arrivals, unique migrant stocks, net fiscal value or crime. The raw workbook separately labels an ICE-removals table; that is a different ledger. [DATA; INFERENCE]

### BLS: matching months, with both denominators and outcomes

The script matched January–August 2025 to the same months of 2026 for both nativity groups: 16 comparisons with all four metrics present. The table below shows June–August, the observation months corresponding to this refresh's recent window; the full January–August output is retained. Population and employment are **thousands of people**, employment-population ratios and unemployment rates are **percent**. Every change is the later source estimate minus the earlier estimate; these are unadjusted descriptive differences, not causal effects or control-adjusted changes. [DATA]

| Month | Nativity | Population 2025 → 2026 | Employed 2025 → 2026 | Δ employed, thousands | E/P ratio 2025 → 2026 | Δ E/P, pp | Unemployment 2025 → 2026 |
|---|---|---:|---:|---:|---:|---:|---:|
| June | Native-born | 224,450 → 226,602 | 132,652 → 131,997 | −655 | 59.1 → 58.3 | −0.8 | 4.4 → 4.6 |
| July | Native-born | 225,276 → 227,173 | 133,035 → 132,315 | −720 | 59.1 → 58.2 | −0.9 | 4.7 → 4.6 |
| August | Native-born | 225,458 → 226,911 | 132,474 → 131,887 | −587 | 58.8 → 58.1 | −0.7 | 4.6 → 4.6 |
| June | Foreign-born | 49,135 → 48,564 | 31,231 → 30,725 | −506 | 63.6 → 63.3 | −0.3 | 4.1 → 3.6 |
| July | Foreign-born | 48,510 → 48,109 | 30,764 → 30,486 | −278 | 63.4 → 63.4 | 0.0 | 4.1 → 3.3 |
| August | Foreign-born | 48,543 → 48,504 | 30,814 → 30,780 | −34 | 63.5 → 63.5 | 0.0 | 4.4 → 3.4 |

The measured June–August pattern is **employment counts down in both groups**, with a larger fall in the native employment-population ratio. This does not fit a literal claim that these same months show rising foreign-born counts replacing falling native counts. It also does not establish that native outcomes were unaffected: the raw ratios worsened. Population changes must remain beside employment changes; foreign-born population estimates are not net-migration counts. No uncertainty intervals or statistical significance tests were constructed. [DATA; INFERENCE]

**The 2026 population-control break matters to this comparison.** BLS's [March 6, 2026 release](https://www.bls.gov/news.release/archives/empsit_03062026.pdf) and [population-adjustment note](https://www.bls.gov/web/empsit/cps-pop-control-adjustments.pdf) explain that the revised January 2026 data incorporated new controls with the February release, after a shutdown-related delay. December 2025 and earlier official estimates were not revised. When applied to December 2025, the new controls lowered aggregate employment by 1,432 thousand and the aggregate employment-population ratio by 0.5 pp. That is a measurement-comparability issue affecting levels **and ratios**; matching calendar months does not remove it. These aggregate adjustments have **not** been applied to either nativity subgroup, and cannot simply be allocated between them. NSA comparisons also retain composition, sampling and residual seasonal differences; they identify no displacement or enforcement effect. [SOURCE; INFERENCE]

### BEA: total-versus-component hierarchy validated

The 2024 principal CSV yielded **2,640 data rows and 60 geography codes**, after excluding the four note rows and trimming geography padding. GeoFIPS/LineCode keys are unique. The script tested **13 declared parent-to-child identities in every geography: 780 checks, zero nonzero residuals**, in thousands of nominal dollars. These are exact source-table accounting checks, not a measure of statistical precision or nativity attribution. [DATA]

For the United States, the major levels reconcile as follows:

| Source hierarchy | Total, thousands of dollars | Component sum | Residual |
|---|---:|---|---:|
| 1000: all personal current transfers | 4,555,385,000 | 2000 government-to-individual 4,415,019,000 + 3000 nonprofit 76,787,000 + 4000 business-to-individual 63,579,000 | 0 |
| 2000: government-to-individual | 4,415,019,000 | retirement/disability 1,491,218,000 + medical 2,076,151,000 + income maintenance 343,016,000 + unemployment 36,434,000 + veterans 229,990,000 + education/training 97,851,000 + other 140,359,000 | 0 |
| 5000: refundable-credit memorandum block | 228,809,000 | EITC 69,441,000 + additional child tax credit 27,847,000 + other credits 131,521,000 | 0 |

**The refundable-credit block is not another top-level component.** The principal `SAINC35__Footnotes.html`, footnote 14, explicitly says refundable credits are already included in the preceding lines/totals; footnotes 15–17 locate their corresponding categories. Adding LineCode 5000 to LineCode 1000 would double count **228,809,000 thousand dollars ($228.809 billion)** in the U.S. 2024 ledger. The dollar conversion is arithmetic, not an immigration-cost estimate. The hierarchy passes do not make aggregate transfers immigrant-specific or net of taxes. [SOURCE: adjacent BEA footnotes; DATA; INFERENCE]

## Recent-source and disconfirmation audit

- **Recent releases/data refresh:** BLS through August 2026; Census May–July 2026 permit files; July 2026 ICE archive; [USDA SNAP page](https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap) updated August 20 with May 2026 observations. [SOURCE]
- **Older vintages retained honestly:** BPS annual 2025, BEA through 2024, existing HIC/PIT and historical Texas crime replication. They are not presented as new 2026 observations. [DATA]
- **Concrete disconfirmer, tested:** the completed-June raw anchor shows 6,872 of 34,551 detention exits were outside the removal-exit category. This falsifies “every detention exit is a deportation” for that month. It does not imply removals are harmless, nor establish whether total enforcement rose or fell. [DATA; INFERENCE]
- **Symmetric tests:** native outcomes can improve or deteriorate; permits can reveal capacity response or continued constraint; transfer growth can reside in means-tested or retirement/medical components. No preferred direction licenses weaker source/denominator checking. [INFERENCE]

## Parent integration block

Parent owns `immigration-dataset-register.md` and INDEX. Append/update these cards; hashes and URLs are in the manifest below.

| ID | Acquisition status/path | Key/vintage/license | Limit |
|---|---|---|---|
| BLS_CPS_NATIVITY_MONTHLY | Acquired 2026-09-05; `.scratch/frontier-20260905/datasets/bls/` | series ID × month; 2021-01–2026-08; federal public-use | NSA national nativity, no legal status; 8 missing values retained |
| CENSUS_BPS_COUNTY_2025_2026 | Acquired 2026-09-05; `.scratch/frontier-20260905/datasets/bps/` | county FIPS × month/year; 2025 annual and May–July 2026; federal public-use | Authorized units, not completions; reported versus estimated distinguishable |
| ICE_DETENTION_VERA_ARCHIVE | Acquired 2026-09-05; `.scratch/frontier-20260905/datasets/ice/` | FY/year_month/cutoff; July archive; research/nonprofit license | Selected detention flows; incomplete last month; mirrored raw and processed distinct |
| BEA_SAINC35_1929_2024 | Discovered existing 2026-09-05; `/Volumes/2TBPNY/corpus/bea_data/SAINC/` | GeoFIPS × LineCode × year; 1929–2024; federal source | Gross receipts, nested hierarchy; no nativity/tax side |

The labor, completed-month ICE and BEA hierarchy checks above were run, and the county permit totals/reporting subsets were computed above. Their results remain descriptive or accounting quantities; no causal regression was run. [DATA]

## Gaps and next queries

- [GAP] Native hourly wages and stratified labor outcomes require CPS microdata, not QWI or these national aggregates.
- [GAP] Enforcement versus arrivals needs compatible full-flow accounting: next queries `OHSS monthly tables 2026 removals returns`, `CBP FY2026 nationwide encounters CSV`, `ICE non-detained removals`. Encounters, book-ins and detention stocks cannot be added as unique immigrants.
- [GAP] Agency ORI/coverage panels and exact Texas status-denominator vintage reconciliation remain necessary for crime. The acquisition does not update a national undocumented crime rate.
- [GAP] SNAP May 2026 state tables are verified available but not downloaded; direct page returned 403. Existing historical SNAP data were not duplicated.
- [GAP] Mounted paths/vintages for legacy causal HIC/BPS assets remain unresolved. A register entry is a locator, not principal-file validation.
- Transport findings: BLS webpage 403 but API succeeded; BEA ZIP endpoint returned HTML and existing corpus made download unnecessary; Exa crawling requires `urls` array; Vera README's `raw_data` differs from actual `raw` directory, resolved from GitHub's tree. These were access/locator issues, not evidence of dataset absence. A large audit serialization was truncated by the tool output budget; the memo used a compact verified structured export instead. [DATA]

## Source-file provenance and hashes

All following source files were acquired 2026-09-05. Acquisition and verification timestamps are distinct in `manifest.json`: reruns preserve the recorded acquisition time and verify existing bytes against their previous hashes. A reused file without a prior record receives an unknown acquisition timestamp rather than a fabricated download time. A missing mounted BEA source makes the full run fail instead of silently skipping its principal checks. [DATA]

**Reproduction boundary:** the retained local files reproduce this snapshot. ICE URLs are pinned to the captured Git tree, while the BLS API and Census endpoints can revise their contents; a later clean reacquisition is not guaranteed to match these bytes and must be compared with this manifest. The complete principal-check run requires the mounted BEA path listed above. No claim of portable, archive-independent byte reproduction is made. [INFERENCE]

**Final integration check:** `validate_final_integration.py` reran the script with network calls forbidden: all 18 source hashes and the complete principal-results hash stayed unchanged. It restored the 17 initial acquisition timestamps from the first captured manifest, retained them on rerun, and left the tree's exact pre-manifest acquisition time unknown. It also exercised rejection of a changed cached source without overwrite and an explicit failure when the BEA source is unavailable. All passed; see `final-integration-validation.log`. [DATA]

| File | Bytes | SHA-256 | URL |
|---|---:|---|---|
| `probes/vera-tree.json` | 58060 | `2062c42664151410aae58107e783c400e197bb8149e2b2b76865c474d5c6965a` | [pinned tree](https://api.github.com/repos/vera-institute/ice-fytd-stats/git/trees/a6bf48e2627323f01827d52776f0d08023c410ba?recursive=1) |
| `bls/LNU00073395.json` | 6229 | `3095ec399b270083390fdad7007e59258a4812adbafda762c9c6fbf0e6c4009c` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU00073395?startyear=2021&endyear=2026) |
| `bls/LNU02073395.json` | 6229 | `aff56ecf1dc57475989d11888b90c42e08d7cb11bef1a46de5ed0d692789dd24` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU02073395?startyear=2021&endyear=2026) |
| `bls/LNU02373395.json` | 6162 | `dd9542e108f9f1ef2894e20f2a600fd173e62e84d8d7908de39d57a661a3865c` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU02373395?startyear=2021&endyear=2026) |
| `bls/LNU04073395.json` | 6095 | `813f1118d54e4162c2a09099fe4114e31f5d2c5b069febbe66f021d713551c75` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU04073395?startyear=2021&endyear=2026) |
| `bls/LNU00073413.json` | 6296 | `5e7f8efbf49eebb2a37bf5487df0e9f0a7711d18acaa0cc28ffd1abc8af10f31` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU00073413?startyear=2021&endyear=2026) |
| `bls/LNU02073413.json` | 6296 | `cb04054e5fdcd7b3743936a70a7b4d52eaabebc26c1ce23a2b7278ab0b9afb7e` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU02073413?startyear=2021&endyear=2026) |
| `bls/LNU02373413.json` | 6162 | `3dc6dce76f44dab575dfd1db0a39eff67bccc356469360dcba0a4c6fbf3d3b7e` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU02373413?startyear=2021&endyear=2026) |
| `bls/LNU04073413.json` | 6095 | `d3a7b40277799776f80d95d7464394f49e75152ba861d642936b70c8ec8057f7` | [source](https://api.bls.gov/publicAPI/v2/timeseries/data/LNU04073413?startyear=2021&endyear=2026) |
| `bps/co2025a.txt` | 375314 | `5d523b1ff172c886ee7f2bc770c82c8c5470b5aaaec5f63441a18c621c80b30e` | [source](https://www2.census.gov/econ/bps/County/co2025a.txt) |
| `bps/co2605c.txt` | 421326 | `01107c5d4578079ab2c66eb3ed1a88f1a1d9d1c294452bff3d2e81ebb78392c8` | [source](https://www2.census.gov/econ/bps/County/co2605c.txt) |
| `bps/co2606c.txt` | 422387 | `f31a92ccd5cb5374e16be5c4da0f41e316a61d862075c609a2d7cbec1c5e0501` | [source](https://www2.census.gov/econ/bps/County/co2606c.txt) |
| `bps/co2607c.txt` | 422033 | `8ad8c46c010b903757ca5f74dea20f6bc7237452a038261da5e0c322877a345c` | [source](https://www2.census.gov/econ/bps/County/co2607c.txt) |
| `bps/documentation-index.html` | 15793 | `283dc155ccffb9eb67f0db563b80e358b106a4c4fc74d3cb83dff8b7040fef6e` | [source](https://www2.census.gov/econ/bps/Documentation/) |
| `ice/2026-07-20_FY26_detentionStats07202026.xlsx` | 251974 | `f83255a56773a7f7a53e46a72ed3bf742397db03eaf14f6abe3f9b07744d28a6` | [source](https://raw.githubusercontent.com/vera-institute/ice-fytd-stats/a6bf48e2627323f01827d52776f0d08023c410ba/raw/FY2026/2026-07-20_FY26_detentionStats07202026.xlsx) |
| `ice/monthly_detention_summary.csv` | 5628 | `1420908cbe4d247e206b3e8b941a196d1a0f7d83748bd26953748e6c5839a3fc` | [source](https://raw.githubusercontent.com/vera-institute/ice-fytd-stats/a6bf48e2627323f01827d52776f0d08023c410ba/processed_data/monthly_detention_summary.csv) |
| `ice/README.md` | 50831 | `b476c8e4e040764d69d816015d401d55e564106a2734635d9a14fde2fdf2f984` | [source](https://raw.githubusercontent.com/vera-institute/ice-fytd-stats/a6bf48e2627323f01827d52776f0d08023c410ba/README.md) |
| `ice/License.md` | 2779 | `2d7704715f3da0b4af7e1512c374464675b9aab9bcf0534af671dc40ddacfc89` | [source](https://raw.githubusercontent.com/vera-institute/ice-fytd-stats/a6bf48e2627323f01827d52776f0d08023c410ba/License.md) |

## Files included / skipped

**Included:** this memo; `infra/immigration-fiscal/acquire/refresh-frontier-20260905.py`; ignored staging with raw sources, probes, manifest, inspection, `principal_checks.json`, `bls/matched_calendar_months.csv`, isolated reproducer smoke checks and run logs.

**Skipped:** shared register/INDEX (parent ownership); raw warehouses and existing source files (read-only); duplicate BEA/HIC/PIT/historical SNAP downloads (existing corpus); new status-crime rate dataset (no compatible acquired denominator); external publication (not requested). No commit was made.

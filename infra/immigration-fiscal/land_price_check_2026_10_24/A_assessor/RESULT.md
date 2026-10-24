DeepSeek V4.1 Flash 1017 (deepinfra)

**Verdict:** Priced 3 of 5 counties from California assessor land values on 2022–2024 base-year
single-family parcels, in 2024 dollars: **Los Angeles $4,100,151/acre** (IQR $2.66M–$6.08M, n=135,601),
**San Diego $1,826,388/acre** (IQR $0.65M–$3.93M, n=104,357), **San Bernardino $641,824/acre**
(IQR $0.29M–$1.13M, n=56,380). Orange and Santa Clara are **left out, not guessed**: Orange's assessor
sells roll products only in person or by written request and publishes no parcel-level land-value/base-year
roll; Santa Clara's public parcel data carries no assessed values and no base year.

## Method (source family A — assessor land values on recently transferred parcels)

Under Prop 13 a parcel's assessed value is reset to market on a change of ownership, and the assessor
splits it into land and improvements. So `land value` on a parcel whose base year (or last transfer) is
2022–2024 is a market-based land value at the transfer date. Per county:

1. Pull **single-family residential** parcels with base year / last transfer 2022, 2023 or 2024 from the
   county assessor roll (attribute tables only, via the portal's query API; no geometry downloaded).
2. Pull **lot area** for the same parcels (county parcel layer `Shape__Area` or the assessor `acreage`
   field).
3. `acres = area / 43560`; `land $/acre = land value / acres`.
4. Undo the Prop 13 cap to recover the base-year value: `base_value = roll_value / 1.02^(roll_year − base_year)`
   (Prop 13 caps the annual inflation factor at 2%).
5. Convert base-year dollars to **2024 dollars** with the S&P CoreLogic Case-Shiller metro index (annual
   averages of the monthly FRED series). No FHFA land-price data — and nothing built on it — was opened
   or used at any point.
6. Report the **median** and the **25th/75th percentiles** of parcel `land $/acre` (2024 $).

Common filters: real single-family use codes; lot 0.03–5.0 acres; land value ≥ $10,000. The trims remove
data artifacts (e.g. $9 land values on 10-acre rows) and rural/estate rows; medians move 0.1% (LA),
2% (SD) and 1.2% (SB) relative to the untrimmed sample.

## Results

| County | FIPS | $/acre 2024 | IQR low | IQR high | n | Roll year used | Index |
|---|---|---|---|---|---|---|---|
| Los Angeles | 06037 | **4,100,151** | 2,656,562 | 6,077,696 | 135,601 | 2024 | CS Los Angeles (LXXRSA) |
| San Diego | 06073 | **1,826,388** | 650,035 | 3,933,379 | 104,357 | 2026 | CS San Diego (SDXRSA) |
| San Bernardino | 06071 | **641,824** | 285,088 | 1,131,508 | 56,380 | 2026 | CS Los Angeles (LXXRSA, proxy) |

Case-Shiller annual averages used: Los Angeles 2022 = 404.14, 2023 = 410.23, 2024 = 437.16;
San Diego 2022 = 403.84, 2023 = 407.21, 2024 = 438.54.

### Los Angeles (06037) — priced
- 138,365 SFR rows on the **2024** roll with base year 2022–2024; 137,694 had a parcel area (99.5%
  match on AIN); **135,601** after trims. Median **$4,100,151/acre**, IQR **$2,656,562–$6,077,696**.
- Cohort check (2024 $/acre median): 2022 base → $4.12M (n=66,380), 2023 → $4.12M (n=46,575),
  2024 → $4.00M (n=22,646). The three cohorts agree within 3%.
- Unadjusted (no Case-Shiller step) median is $3,962,859/acre; the year adjustment moves it +3.5%.
- ZIP-level sanity (unadjusted $/acre): 90210 Beverly Hills $11.3M, 90265 Malibu $5.9M,
  90045 Westchester $8.2M, 91001 Altadena $4.7M, 91342 Sylmar $2.9M, 93550 Palmdale $1.1M,
  93551 Lancaster $0.87M.
- Land share of total assessed value (land/(land+improvement)) is 0.74 median in this sample vs 0.635
  county-wide for all 1.49M SFR parcels on the 2024 roll — the recent-transfer sample is land-heavy
  but not an artifact of the split.

### San Diego (06073) — priced
- 106,217 SFR parcels whose last recorded document is dated 2022–2024; **104,357** after trims.
  Median **$1,826,388/acre**, IQR **$650,035–$3,933,379**.
- Cohort medians (2024 $/acre): 2022 → $1.845M (n=35,971), 2023 → $1.834M (n=31,786),
  2024 → $1.812M (n=36,531). Unadjusted median $1,842,192.
- Land share of value is 0.54 median, vs 0.74 in LA — consistent with cheaper land relative to structures.
- Sensitivity: restricting to lots ≤ 1 acre (urban lots) gives $2,051,205/acre (n=96,650).

### San Bernardino (06071) — priced
- 89,962 rows in the county's `SINGLE FAMILY RESIDENTIAL` class with base year 2022–2024; after keeping
  only improved detached descriptions (SFR, PUD, PUD DEMINIMUS) and applying the trims, **56,380**.
  Median **$641,824/acre**, IQR **$285,088–$1,131,508**.
- Cohort medians (2024 $/acre): 2022 → $641,824 (n=21,671), 2023 → $641,097 (n=16,977),
  2024 → $650,265 (n=17,892).
- The county class also contains VACANT LAND, CONDO, MANUF HOME and DUPLEX rows; including them
  (class-wide, n=74,838) gives $541,278/acre. Lots ≤ 1 acre give $612,745/acre.
- Land share of value is 0.27 median — the cheapest-land of the three counties, consistent with the
  high-desert half of the county.

## Sources (with locators and quotes)

**LA roll** — LA County "Parcel Data 2021-2025" table service, layer `Parcel_Data`
<https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/Parcel_Data_2021_Table/FeatureServer/0>
(data.lacounty.gov item `70d93266f45a4080a97b285a471493cd`). Query:
`RollYear='2024' AND UseType='SFR' AND (Roll_LandBaseYear='2022' OR '2023' OR '2024')` → 138,365 rows.
Data dictionary (item `0d3ac33a76e1495bb7fc522a8085729c`, "Assessor Parcel Data Roll 2026"):
*"Land Value | Roll Land Value | 999,999,999"*, *"Land Base Year | Roll Land Base Year | YYYY"*,
*"Property Use Code"*, *"Recording Date | YYYYMMDD"*.

**LA area** — "LA County Residential Parcels" (DPH GIS, snapshot 2024-01-09), layer 1
<https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/ResidentialParcels_LACounty_010924download_allCB20_HD22_attributes/FeatureServer/1>
— field `Shape__Area`; the service returns `"units": "esriFeet"` with
`{"wkid": 102645, "latestWkid": 2229}` (NAD83 California State Plane Zone 5, US feet), so area is ft².
Not used: `Assessor_Parcel_Roll_2021_2025.zip` (884,621,406 bytes) — above the 300 MB per-file cap.

**San Diego** — SANDAG/SanGIS "Parcels" hosted feature service, layer 0
<https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0>. Item description:
*"Parcels represent taxable pieces of property. A parcel is created by the San Diego County
Assessor/Recorder/County Clerk (ARCC) to identify a specific portion of real property that is taxed at a
certain rate for a certain owner."* Fields used: `asr_land` (assessor land value), `asr_impr`, `acreage`
(assessor acres, ft² fallback `SHAPE__Area`), `docdate` (MMDDYY of last recorded document), `asr_landuse`
(11 = single family residential; 571,385 parcels, 565,109 with 1 unit). Roll year inferred as **2026**:
2026-dated transfers are present but still carry pre-transfer capped values, while 2025 transfers carry
reassessed values — i.e. the layer is the 2026 lien-date roll (layer `lastEditDate` 2026-10-06).

**San Bernardino** — "Parcels with Redacted Owner Name" (SBCountyDPW / County_Of_San_Bernardino), layer 0
<https://services.arcgis.com/aA3snZwJfFkVyDuP/arcgis/rest/services/Parcels_for_San_Bernardino_County/FeatureServer/0>
(item snippet: *"This dataset contains County of San Bernardino parcel polygons."*). Fields used:
`LandValue` (text, e.g. `"173,189"`), `ImprovementValue`, `Acreage` (0.25 = acres), `BaseYear`
(`"2022"`), `AssessClass` (`"SINGLE FAMILY RESIDENTIAL"`), `AssessDescription` (`"SFR"`). The layer
contains 21,559 parcels with `BaseYear='2026'`, so the values are the 2026 roll.

**Index** — S&P CoreLogic Case-Shiller, FRED `LXXRSA` (Los Angeles) and `SDXRSA` (San Diego),
<https://fred.stlouisfed.org/series/LXXRSA>, <https://fred.stlouisfed.org/series/SDXRSA>; annual averages
computed from the monthly series. CPI-U (`CPIAUCSL`) was checked as an alternative and differs by <1% for
the 2022→2024 step.

**Orange County (06059, not priced)** — ocassessor.gov "Assessor Roll Products":
*"Assessor roll products are ONLY AVAILABLE in-person at our Public Service Center or by written request…
If you would like to review property data online, please continue to ParcelQuest."*
(<https://www.ocassessor.gov/page/assessor-roll-products>). The county parcel service
(<https://www.ocgis.com/arcpub/rest/services/Map_Layers/Parcels/FeatureServer/0>) exposes only
`ASSESSMENT_NO`, `SITE_ADDRESS`, `YEAR_BUILT`, `NBR_BEDROOMS` — no land value, no base year. The only
public roll attributes with land value are the Treasurer-Tax Collector's secured-tax layers, which stop at
2021-22 (`ALV`/`AIV`/`TAV` per APN) and carry no base year or transfer date, so they cannot identify
2022–2024 transfers.

**Santa Clara (06085, not priced)** — the county's open "Parcels" dataset (FY 2026) on data.sccgov.org
(`ubcd-cewv`) has columns `apn, tax_rate_area, situs_*, jurisdiction, shape_length, shape_area` and no
assessed values, land value, or base year; the county Socrata catalog returns no parcel-level assessment
dataset (searches for "assessor", "secured", "value"). The Assessor's own site (asr.santaclaracounty.gov)
returns HTTP 403 to programmatic requests. No public parcel-level land-value + base-year roll was found,
so no number is reported.

## Limitations

- **What the number is.** Assessor land value is the assessor's allocation of a transfer price between
  land and improvements, not a vacant-land transaction price. Where an assessor under-allocates to land
  (older, dense neighborhoods) the $/acre is biased down; where a teardown is assessed land-heavy it is
  biased up. Read it as "assessor land value per acre", not "land sale price per acre".
- **Base year ≠ sale date, exactly.** Prop 13 reassessment happens on a change of ownership, but
  parent-child/age-55 exclusions, entity transfers and Proposition 8 declines mean a minority of parcels
  carry a base year that does not reflect a market reset. This adds noise, not a consistent bias.
- **San Diego's base year is a proxy.** SANDAG publishes the last recorded document date, not the
  assessor's base-year field; a non-deed recording would misclassify a parcel. The monotonic rise of
  cohort values with transfer year (2010 $1.05M → 2020 $1.59M → 2024 $1.88M per acre) is what a
  base-year field looks like, so the proxy behaves.
- **Roll-year assumption.** LA's roll year is explicit (`RollYear='2024'`). For San Diego and San
  Bernardino the values are the 2026 roll; if San Diego's were the 2025 roll, its 2024-cohort deflator
  would change by 2% and the county median by ~0.5%.
- **Index mismatch.** Case-Shiller is a *house* price index (land + structure); land is more volatile.
  San Bernardino has no Case-Shiller metro of its own and uses Los Angeles as a proxy (CPI-U would give a
  similar answer for this 2-year step).
- **Trims.** LA: untrimmed (any lot > 0) median $4,094,921 vs $4,100,151 reported. San Diego: $1,791,416
  vs $1,826,388. San Bernardino (SFR+PUD rows): $636,304 vs $643,880; only 1.4% of rows are dropped. The
  bigger swing in SB is the *class* definition, not the trims: the county's SINGLE FAMILY RESIDENTIAL
  class also carries VACANT LAND, CONDO, MANUF HOME and DUPLEX rows, and including them gives $541,278.
- County-wide medians include rural and high-desert parcels; the ≤1-acre urban cut is reported above for
  each county ($4.17M LA, $2.05M SD, $0.61M SB).

## Log (JST)

- 2026-10-24 19:41 — created `A_assessor/`, wrote RESULT.md stub; data.lacounty.gov is now an ArcGIS Hub,
  so the Socrata API is gone.
- 2026-10-24 19:44 — found the LA assessor roll table services; `Assessor_Parcel_Roll_2021_2025.zip` is
  884 MB (over the 300 MB cap) → used the feature service query API.
- 2026-10-24 19:47 — LA roll has no lot area; located "LA County Residential Parcels" (2,167,513
  residential parcels with `Shape__Area` in CA State Plane ft).
- 2026-10-24 19:56 — pulled 138,365 LA SFR rows (2024 roll, base 2022–24) + 137,694 areas; joined on AIN.
- 2026-10-24 20:00 — LA stats: median $4,100,151/acre, IQR $2.66M–$6.08M, n=135,601.
- 2026-10-24 20:10 — San Diego: SANDAG parcels (1,089,056 rows) with `asr_land`, `acreage`, `docdate`;
  pulled 106,217 transfers 2022–24 and the full 571,385-parcel SFR population for cohort checks.
- 2026-10-24 20:20 — San Diego stats: median $1,826,388/acre, IQR $0.65M–$3.93M, n=104,357.
- 2026-10-24 20:30 — San Bernardino: SBCounty parcels with `LandValue`, `BaseYear`, `Acreage`;
  89,962 class rows → 56,380 after description + trims; median $641,824/acre.
- 2026-10-24 20:35 — Orange: assessor roll products are in-person/written-request only; public parcel
  layer has no values → excluded. Santa Clara: no public parcel-level assessment data → excluded.
- 2026-10-24 20:42 — wrote `prices.csv` (3 rows) and this file.

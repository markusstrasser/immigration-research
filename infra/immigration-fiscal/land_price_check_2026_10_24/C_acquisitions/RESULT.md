DeepSeek V4.1 Flash 1017

**Verdict:** Priced 4 of 5 counties from government land-acquisition records (2015–2024), in 2024 dollars: Los Angeles **$1,391,000/acre (n=2)**, San Diego **$550,653/acre (n=9)**, Santa Clara **$2,690,330/acre (n=2)**, San Bernardino **$134,223/acre (n=4)**. Orange County is **not priced** — I could not find a single arms-length, land-only, price-and-acreage-disclosed public acquisition in the county in 2015–2024 that I could verify; every Orange item I reached was either an improved property, a conveyance/lease, or disclosed no price. n is far below the 10/county target: California agencies rarely buy vacant urban land, and when they do the price is often in closed session. The medians above are therefore indicative, not precise; LA and Santa Clara rest on 2 observations each.

## What this measures

Price per acre that a public agency actually paid (or was authorised to pay) for land, excluding the value of buildings. Two price bases appear in the data and are labelled in `acquisitions.csv`:

- **purchase price / not-to-exceed** — board-authorised amount (San Bernardino, San Jose, Long Beach, City of LA). For Long Beach the *authorised* ceiling ($1,105,000) is used, not the $1,050,000 listing price.
- **land_cost** — City of San Diego's own accounting field, which is separate from `building_cost`; rows with `building_cost > 0` were dropped.

Deflation: **CPI-U** (FRED `CPIAUCSL`, monthly, seasonally adjusted) annual averages, base 2024 = 313.698. I did **not** use FHFA's land-price series or anything built on it, and did not open it.

## Method

1. Enumerated agency record systems that publish price *and* acreage. Legistar's public Web API (`https://webapi.legistar.com/v1/{client}`) exposes full agenda-item text for San Bernardino County, San Jose, Long Beach, Chula Vista, San Marcos, Huntington Beach, Santa Clara (city), LAUSD, OCTA and Metro; I pulled all 2015–2024 items whose titles mention acquisition/purchase/condemnation plus a property word, then downloaded and text-extracted the attached staff reports (pdftotext) and searched for price + area in the same passage.
2. Where a city publishes an acquisition register, used it directly (City of San Diego `city_owned_properties`, which has `land_cost`, `building_cost`, `file_acres`, `year_acquired`).
3. For rural/open-space context only, used the Wildlife Conservation Board's approved-project feature service (WCB, `ds672`), filtered to `Type='Acquisition'`, 2015–2024.
4. Excluded: any acquisition of an improved property where land value was not split out (e.g. San Bernardino's Colton office buildings $3.225M/3.35 ac, 2015; Barstow Head Start $818,861/1.02 ac, 2018; Colton 851 S Cooley $14.5M/6.84 ac, 2018; San Jose 517 W St John $5.1M/0.44 ac with warehouse, 2023). Also excluded easement-only purchases, tax-deed sales, and inter-agency transfers with no price.
5. Classified urban vs rural/open-space by location. Remote desert/mountain parcels (Mojave, Joshua Tree, Newberry Springs, Oro Grande, Cedar Glen) are kept in `acquisitions.csv` with `urban=no` and are **out of** the medians.

Reproduce: `python3 C_acquisitions/build.py` (reads `_cache/cpi.csv`), `python3 C_acquisitions/wcb_rural.py`.

## Results (urban, land-only, 2024 dollars)

| County | FIPS | $/acre 2024 | low–high | n | years |
|---|---|---|---|---|---|
| Los Angeles | 06037 | 1,391,000 | 953,760 – 1,828,241 | 2 | 2017, 2019 |
| San Diego | 06073 | 550,653 | 296,977 – 708,772 | 9 | 2015–2023 |
| Santa Clara | 06085 | 2,690,330 | 2,080,980 – 3,299,679 | 2 | 2020–2021 |
| San Bernardino | 06071 | 134,223 | 112,331 – 224,313 | 4 | 2015–2016 |
| Orange | 06059 | — not priced — | — | 0 | — |

Low/high are the 25th/75th percentile where n ≥ 4, and min/max where n < 4.

### Los Angeles (n=2)

- **Taylor Yard G2, Cypress Park, 2017-03-01 — 42.0 ac, $60,000,000 → $1,428,571/ac nominal ($1,828,241 in 2024$).** City of LA bought the vacant former railyard for a river park. Source: <https://tayloryardriverprojects.lacity.gov/about-taylor-yard-g2-projects> — *"The G2 Parcel was purchased by the City of Los Angeles in March 2017 for $60 million."* Acreage: <https://engineering.lacity.gov/about/divisions/projects-taylor-yard-100-acre-partnership> — *"G2 is a Los Angeles River-adjacent, approximately 42-acre property."*
- **Tanaka Park, 1400 W Wardlow Rd, Long Beach, 2019-06-11 — 61,926 sq ft (1.4216 ac), $1,105,000 → $777,279/ac nominal ($953,760 in 2024$).** City bought the land it had leased as a park since 2001. Source: Long Beach item 19-0555 staff report R-39, <https://longbeach.legistar1.com/longbeach/attachments/d0ecf7a0-c7a2-40f4-b894-3a670fa4668a.pdf> — *"…for the purchase of certain real property at 1400 West Wardlow Road … in an amount not to exceed $1,105,000"*; *"The Subject Property measures approximately 61,926 square feet"*; *"1.4 acres of land."*

Two observations is not a median worth defending. Metro, the largest urban land buyer in the county, discloses prices only in closed session: of 233 Metro property/acquisition agenda items 2015–2025 that I pulled and text-mined, only one contained a price attached to an area. LA County's own real-estate items sit behind a board-agenda system with no bulk interface. I did not substitute a guess.

### San Diego (n=9, City of San Diego register)

Source for all nine: <https://data.sandiego.gov/datasets/city-owned-properties/>, CSV <https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv>, fields `site_name, year_acquired, land_cost, building_cost, file_acres`. Every row used has `building_cost = 0`.

| Site | Year | acres | land_cost | $/ac nominal | $/ac 2024 |
|---|---|---|---|---|---|
| San Ysidro Library | 2015 | 1.55 | 830,000 | 535,484 | 708,772 |
| Fairbrook Neighborhood Park | 2015 | 3.40 | 344,000 | 101,176 | 133,918 |
| Pacific Highlands Ranch Community Park | 2016 | 13.60 | 6,595,974 | 484,998 | 633,915 |
| Fairmount Fire Station (future) | 2017 | 1.28 | 325,000 | 253,906 | 324,941 |
| Del Sur Neighborhood Park | 2018 | 5.04 | 196,400 | 38,968 | 48,683 |
| Dennery Ranch Neighborhood Park | 2021 | 9.21 | 7,732,183 | 839,542 | 971,914 |
| Fire Station #49 (future) | 2022 | 2.11 | 2,944,000 | 1,395,261 | 1,495,732 |
| McGonigle Canyon Neighborhood Park | 2023 | 6.15 | 3,289,411 | 534,864 | 550,653 |
| San Carlos Branch Library | 2023 | 0.52 | 150,000 | 288,462 | 296,977 |

Quotes are field values, e.g. `site_name=DENNERY RANCH NEIGHBORHOOD PARK; land_cost=7732183.0; building_cost=0.0; file_acres=9.21; grantor=TRI-POINT HOMES IE-SD, INC`.

Note the two low outliers (Fairbrook, Del Sur) are purchases from homebuilders — parkland-dedication prices, plausibly below market. Excluding them moves the median from $550,653 to $633,915.

### Santa Clara (n=2)

- **SW corner E Alma Ave & Senter Rd, San Jose, 2020-02-25 — 4.95 ac, $8,500,000 → $1,717,172/ac ($2,080,980 in 2024$).** Source: San Jose item 20-182 memorandum, <https://sanjose.legistar1.com/sanjose/attachments/edbf5624-8db4-49a5-a94c-93f226c8fe44.pdf> — *"…for the purchase by the City of 4.95 acres located at the southwest corner of East Alma Avenue and Senter Road … for a price of $8,500,000, inclusive of a $100,000 buyer holdback for qualified environmental remediation expenses."*
- **1138 Olinder Ct, San Jose, 2021-05-24 — 1.1 ac (47,916 sf), $3,135,300 → $2,850,273/ac ($3,299,679 in 2024$).** Source: item 21-1329, <https://sanjose.legistar1.com/sanjose/attachments/04b228ac-4bd5-43d2-8fea-c2fc99bf3865.pdf> — *"…purchase by the City of approximately 1.1 acres (47,916 square feet) of land located at the northeast corner of Olinder Court and Felipe Avenue … for a price of $3,135,300."*

### San Bernardino (n=4 urban)

All from San Bernardino County Board of Supervisors real-estate items (Legistar client `sanbernardino`); the motion text itself carries price and acreage.

- **Sunhill Dr, Victorville, 2015-10-06 — 2.49 ac, $115,000 → $46,185/ac ($61,131 in 2024$).** *"approximately 2.49 acres of vacant land … for a purchase price of $115,000"* (item HIST-243498).
- **SE corner San Bernardino Ave & Carob Ave, uninc. Fontana, 2016-05-24 — 0.94 ac, $100,000 → $106,383/ac ($139,047 in 2024$).** *"approximately 0.94 acres of vacant land … for a purchase price of $100,000"* (item HIST-253847).
- **Tokay St terminus, Victorville, 2016-08-23 — 5.0 ac, $495,000 → $99,000/ac ($129,398 in 2024$).** *"approximately five acres of vacant land at the terminus of Tokay Street in the City of Victorville … for a purchase price of $495,000"* (item HIST-255940).
- **14677 Merrill Ave, uninc. Fontana, 2016-08-23 — 2.54 ac, $933,000 → $367,323/ac ($480,108 in 2024$).** *"approximately 2.54 acres of vacant land, for a purchase price of $933,000"* (item HIST-255884).

Locator URL for each: `https://webapi.legistar.com/v1/sanbernardino/matters?$filter=substringof('<distinctive word>',MatterTitle)` returns the item with `MatterTitle` containing the quoted text. The 2019–2024 items in this series (Bloomington, Phelan, Yucca Valley, Hesperia) have short titles and their attachments did not disclose acreage in the text I could extract, so they are not included.

### Orange (06059) — not priced

OCTA's Legistar library has 16 acquisition items 2015–2025, but the only one with substantive detail is an internal audit of I-405 right-of-way practices (item 17-774) that contains no parcel prices. OC Board of Supervisors staff reports reachable through `ocagendaext.oc.gov` that matched "acquisition + acres" were flood-control/lease/conveyance items with no land price, and the 2021–22 Grand Jury report on county land transactions confirms the county routinely handles these without public price disclosure. I found no arms-length, land-only purchase with both price and acreage. Reporting a number here would be a guess, so the county is omitted.

## Rural / open-space land, kept separate (not comparable)

Wildlife Conservation Board approved acquisition projects, 2015–2024, deflated to 2024$ (`rural_wcb_summary.csv`). Source: WCB Approved Projects `ds672` feature service, <https://services2.arcgis.com/Uq9r85Potqm3MfRV/arcgis/rest/services/biosds672_fpu/FeatureServer/0>, fields `TotalCost`, `Acres`, `dtmBoardAp`, `Type='Acquisition'`.

| County | n projects | median $/acre 2024 | IQR |
|---|---|---|---|
| Los Angeles | 19 | 40,144 | 16,055 – 124,991 |
| Orange | 5 | 114,661 | 58,191 – 272,811 |
| San Diego | 45 | 19,102 | 7,296 – 32,104 |
| Santa Clara | 10 | 7,733 | 5,835 – 10,210 |
| San Bernardino | 26 | 8,900 | 3,716 – 14,433 |

San Bernardino's own desert acquisitions in `acquisitions.csv` land in the same band: $654/ac (Mojave quarry) to $43,568/ac (Cedar Glen), median $13,864. That is one to two orders of magnitude below the urban figures — which is exactly why the task's urban/rural split matters. `TotalCost` is project cost and may include transaction or restoration costs, so these are upper bounds on land price.

## Limitations

- **n is 2–9, not 10+.** Only Los Angeles, San Diego, Santa Clara and San Bernardino are priced. Orange is not.
- **What governments buy is not a random sample of urban land.** Parks, library/fire sites and flood-control parcels are chosen for public purpose; some (notably developer parkland dedications in San Diego) transact below market. Government buyers also pay relocation and goodwill costs not captured here.
- **Price basis varies** (authorised ceiling vs recorded land cost vs board-approved purchase price). Ceilings can exceed final price.
- **Deflation is national CPI-U, not a metro land index.** LA/Orange/SD/Santa Clara land inflation 2015–2024 probably exceeded CPI; using CPI likely understates the 2024 equivalent for older observations. I deliberately avoided FHFA's land series and Case-Shiller (the latter measures repeat-sale house prices, not land).
- **Vintage mix.** San Bernardino's usable urban observations are all 2015–2016; LA's are 2017 and 2019; Santa Clara's 2020–2021. Cross-county comparison therefore mixes cycles.
- **Acreage definitions** are as stated by the agency (gross parcel area; no net-of-dedication adjustment).
- Several transactions are "not to exceed" or include small escrow/title add-ons excluded from the per-acre figure (stated in the row notes where relevant).

## Log

- 19:41 — created `C_acquisitions/`, wrote `RESULT.md` with `**Verdict:** in progress`.
- 19:44–19:58 — probed Legistar Web API clients; found working tenants: `sanbernardino`, `sanjose`, `longbeach`, `huntingtonbeach`, `chulavista`, `sanmarcos`, `santaclara`, `lausd`, `octa`, `metro`. Pulled 2015–2024 matters for each (Metro 244, San Bernardino 2,125, San Jose 647, Long Beach 1,477, etc.).
- 19:50–20:05 — Metro board-report PDFs downloaded and text-mined (150 docs); only one item (2021-0380) paired a price with an area → Metro abandoned as a price source. Cache trimmed to text only (~8 MB).
- 20:05–20:20 — downloaded and text-mined staff reports for Long Beach, San Jose, Huntington Beach, Chula Vista, San Marcos, Santa Clara, San Bernardino (≈600 PDFs, text kept, PDFs deleted; `_cache` ≈ 30 MB).
- 20:20–20:35 — found City of San Diego's `city_owned_properties` register (land_cost / building_cost / file_acres) → 9 usable urban rows.
- 20:35–20:45 — parsed San Bernardino Board of Supervisors motion text (price and acreage are in the title) → 10 land-only rows, 4 urban.
- 20:40 — pulled CPI-U (`CPIAUCSL`) from FRED; computed annual averages (2024 = 313.698).
- 20:45 — pulled WCB `ds672` feature service, 1,066 projects 2015–2024, 411 acquisitions; computed rural medians.
- 20:48 — wrote `acquisitions.csv` (23 rows), `prices.csv` (4 counties), `rural_wcb_summary.csv`; finalised this file.

**Verdict:** After California legalized street vending, licensed restaurants did not lose ground where
vending is common. The one exception is weak and not significant: full-service restaurant counts in
2019.

In 2019, the one clean year after SB 946, per 10 points of Hispanic share:
- restaurant establishments in Los Angeles County ZIPs moved +0.1% (SE 0.3);
- food-service taxable sales in the county's 80 cities moved +0.2% (SE 0.15);
- across California counties, net of the same gradient in other states, the estimates ran from −1.0%
  to +0.9% (SE 0.3–0.6).

By 2022–2023 all three are positive.

**The exception.** The most direct measure of pre-law vending is LAPD vending arrests in 2010–2016, by
City ZIP. Against it, full-service restaurant counts lean negative in 2019:
- −0.7% per log point of arrests (SE 0.7), and −1.1% (SE 0.6) without downtown;
- that is roughly 20–70 of the 3,344 full-service restaurants in those ZIPs, relative to arrest-free
  ZIPs; at the 95% bound, about 170.

The unweighted county comparison leans the same way (−1.0% per 10 points, SE 0.6). But none of this
is significant, and county employment does not follow. Limited-service restaurants, the closer
substitute for street food, show nothing (+0.2%, SE 0.5).

**The statewide gap.** California restaurant employment grew 0–1.6% slower than in comparable counties
elsewhere in 2019, and 1.7–4.0% slower by 2022–2023. The gap does not point to vending:
- it began in 2018;
- grocery shows it too;
- payroll rose, the minimum-wage pattern;
- it sits inside the range other states produce (permutation p 0.48–0.96).

**Size.** Street food is small: about $150m a year in the City of Los Angeles, 1.3% of its restaurant
sales (0.6–2.6%). Even if every dollar came out of restaurants, owners statewide would lose about
$0.4bn a year at the margin ($0–1.2bn).

Evidence: B for "no detectable loss after legalization"; C for the arrest-hotspot lean and the size
bound.

Lane: `vending_restaurants_2026_09_24`, 2026-09-24/25.

Operator's question: "california being flooded with dirt and crime and foodtrucks from illegals not
needing the same scrupels as normal business and driving other business that are honest out of
business?"

This lane prices the competition channel. On dirt, section 9 reports what exists; crime is outside
this lane. Taxes on vendors' earnings are already in the adopted account (section 8).

Model self-report: claude-opus-5-5[1m] (Opus 5.5, 1M context). Literature reads were done by a
researcher subagent on the same model (`reads/`).

## At a glance

| Measure | 2019 (clean year) | 2022–2023 | Source |
|---|---|---|---|
| LA County ZIPs: full-service restaurant establishments, per 10 pts Hispanic share | +0.1% (SE 0.3) | +1.4% | [CALCULATION: `analyze_zip.py` → `derived/zip_event_summary.csv`] |
| Same, limited-service | +0.0% (SE 0.25) | +0.5% | same |
| Same, all food service and drinking places (722) | −0.1% (SE 0.2) | +1.1% | same |
| Same, grocery (placebo) | −0.3% (SE 0.3) | −1.1% | same |
| City of LA ZIPs: full-service establishments, per log point of 2010–2016 vending arrests | −0.7% (SE 0.7); −1.1% (SE 0.6) without downtown | +0.0% (log) / −1.0% (Poisson) | [CALCULATION: `analyze_zip_downtown.py` → `derived/zip_arrests_no_downtown.csv`] |
| Same, limited-service | +0.2% (SE 0.5) | −0.0% / −0.8% | same |
| LA County cities: food-service taxable sales, per 10 pts, unweighted / population-weighted | +0.2% (0.15) / +0.3% (0.15) | +0.5% / +1.2% | [CALCULATION: `analyze_sales.py` → `derived/sales_event_summary.csv`] |
| California counties, triple difference: full-service establishments, per 10 pts | −1.0% (0.6) / −0.0% (0.3) | +1.2% / +0.8% | [CALCULATION: `analyze_county.py` → `derived/county_triple_summary.csv`] |
| Same, limited-service employment | −0.7% (0.6) / −0.2% (0.4) | +1.1% / +2.5% | same |
| California vs other states: restaurant (7225) employment, QCEW, 4 specifications | −0.4% to +0.1% (SE 0.3–0.6) | −4.0% to −1.7% | [CALCULATION: `derived/county_event_summary.csv`] |
| Street food, City of Los Angeles, share of restaurant taxable sales | 1.1% (0.6–2.3%) | 1.2% (0.6–2.5%) | [CALCULATION: `size_rows.py` → `derived/size_by_year.csv`] |

## 1. What the laws changed (verified from the texts)

| Law | Dates | What it changed | Source |
|---|---|---|---|
| SB 946 (Lara), Statutes 2018 ch. 459 | Approved and filed 17 Sep 2018; in force 1 Jan 2019 | Adds Gov. Code §§51036–51039. A city or county may regulate sidewalk vendors only through a program meeting §51038. It may require a permit, a business licence and a CDTFA seller's permit (§51038(c)(4)–(5)). It may not cap vendor numbers or confine vendors to areas, except for "objective health, safety, or welfare concerns". §51038(e): "perceived community animus or economic competition does not constitute an objective health, safety, or welfare concern." Violations carry only administrative fines ($100/$200/$500; vending without a required permit $250/$500/$1,000), and pending criminal prosecutions are dismissed (§51039). The Retail Food Code still applies to food vendors (§51037(b)). | [SOURCE: https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180SB946, chaptered text and Legislative Counsel's digest; in-force date from Cal. Const. art. IV §8(c)(1), "January 1 next following a 90-day period from the date of enactment", https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CONS&sectionNum=SEC.%208.&article=IV] |
| SB 972 (Gonzalez), Statutes 2022 ch. 489 | Approved and filed 23 Sep 2022; in force 1 Jan 2023 | Amends the California Retail Food Code. It creates the "compact mobile food operation" (a cart, stand or person, nonmotorized) and widens "limited food preparation" (hot and cold holding, reheating food prepared at an approved facility). A cottage food operation or microenterprise home kitchen may act as commissary for up to two carts. Counties may pre-approve standard cart plans and cut permit fees. Vendors of prepackaged non-hazardous food or whole produce on 25 sq ft or less are exempt. Retail Food Code violations by these operators become punishable only by administrative fine. | [SOURCE: https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202120220SB972, digest and §§113818, 114368 et seq.; LA County DPH: "On September 23, 2022, Governor Newsom signed SB 972 … The new law became effective on January 1, 2023", http://publichealth.lacounty.gov/eh/business/compact-mobile-food-operation.htm, fetched 2026-09-24] |
| City of Los Angeles, LAMC §42.13 (Sidewalk and Park Vending Program) | Permit required from 1 Jan 2020 (Ord. 186,478, eff. 18 Dec 2019) | "Beginning on January 1, 2020, Vending without a Sidewalk and Park Vending Operating Permit shall be unlawful." The permit fee is now $27.51 (Ord. 188,305, eff. 11 Aug 2024). The city repeats the state rule that "economic competition does not constitute an objective health, safety or welfare concern" (§42.13 C.1). A permit also needs a city Business Tax Registration Certificate, a state seller's permit and, for food, a county public health permit. | [SOURCE: https://codelibrary.amlegal.com/codes/los_angeles/latest/lamc/0-0-0-130544, §42.13 B.2–B.3, C.1, read 2026-09-24; https://streetsla.lacity.org/vending, fetched 2026-09-24] |

## 2. What legalization changed in practice

**Criminal enforcement in Los Angeles had largely ended before SB 946.** LAPD arrests under the old
ban (LAMC §42.00, excluding 42.00(c), soliciting employment) ran as follows:

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|---|---|
| 916 | 682 | 789 | 1,219 | 934 | 357 | 117 | 27 | 4 | 1 |

[DATA: LA open data `yru6-6re4`, 5,097 rows, 5,046 of them vending; the city's filtered view
`7fnr-292v` holds the same rows; `fetch_lapd.py` → `derived/lapd_vending_arrests_year.csv`]

So in the City of Los Angeles, a 2019 event date measures the state law and the permit regime, not the
end of arrests.

**Few vendors became licensed.**
- **City permits.** The city planned for about 16,000 permits a year at $541. It sold an average of
  944 a year from FY2019-20 to FY2022-23, against a Bureau of Street Services estimate of 50,000
  vendors, 10,000 of them selling food [SOURCE: City Administrative Officer, Sidewalk and Park Vending
  Fee Study Update, CF 13-1493-S15, 25 Jul 2023, p. 3, `reads/cao_2023_vending_fee_study.md`; CLA
  report CF 13-1493, 26 Nov 2014, p. 2, `reads/cla_2014_sidewalk_vending_status.md`].
- **Food permits.** By June 2021 "only 165 out of an estimated 10,000 sidewalk food vendors" held
  permits [SOURCE: UCLA School of Law et al., *Unfinished Business*, June 2021, p. 12,
  `reads/ucla_law_unfinished_business_2021.md`]. A news report of a StreetsLA figure puts active
  permits at 687 in September 2024, 53 of them for food [SOURCE: secondary, MyNewsLA 5 Feb 2025; the
  StreetsLA report itself was not found].
- **Unincorporated county areas.** The County Department of Economic Opportunity had "Supported 9
  CMFO permits" and issued 26 vending registration certificates by January 2026. A Board motion
  estimates "50,000+ unpermitted sidewalk vendors in the County" [SOURCE: EDPC agenda slides, 15 Jan
  2026; Mitchell–Solis motion, 21 May 2024, p. 2; `reads/lacounty_cmfo_counts_2024_2026.md`].

Almost all street food therefore stayed unlicensed after legalization. What changed for vendors is the
penalty: an administrative citation instead of arrest and a criminal record.

**No direct vending series exists below the city.** MyLA311's public extracts for 2015–2025 carry only
sanitation and streetlight request types. The newer MyLA311 Cases files (March 2025–2026, 63 types)
have no vending type; "Obstructions" is the nearest and does not identify vendors [DATA:
data.lacity.org `ms7h-a45h`, `ndkd-k878`, `eq98-9f8w`, `h65r-yf5i`, `73a2-6ar5`, `2cy6-i7zn`, grouped
by type, 2026-09-24]. [VERIFIED NEGATIVE] No public permit-by-ZIP file was found in the city's
catalog. The LAPD arrest file is the only direct pre-2018 measure below the city, and it mixes vending
with enforcement effort.

## 3. Data and gates

| Source | Rows and keys checked | Gate |
|---|---|---|
| County Business Patterns 2012–2023, county × NAICS (722, 7225, 722511, 722513, 722330, 445110) | 427–3,227 counties per code and year; header ESTAB, EMP, PAYANN, state, county; body shape checked | US NAICS 722 from the API equals the published flat files exactly in 2019 (672,602 establishments, 12,330,989 employees) and 2023 (714,532; 12,644,827). County sums excluding Puerto Rico are within +0.10–0.11% (establishments) and +0.02–0.03% (employment). **Pass** [DATA: `derived/cbp_fetch_audit.json`] |
| ZIP Business Patterns 2012–2023, 284 LA County ZCTAs | ZIP, ESTAB, EMPSZES; empty ZIP chunks (HTTP 204) handled | LA-ZIP sums fall 0.69–0.75% short of the CBP county totals for 722511 and 722513 in 2012 and 2019. **Pass** [DATA: `derived/zip_gate.json`] |
| ZIP Business Patterns, six placebo counties | 70–163 ZCTAs per county | same construction |
| QCEW 2014–2023, county, private (7225, 722511, 722513, 722330, 445110) | Industry slices; the API has no 2012–2013 slices (HTTP 404) | County rows for 7225 sum to 98.2–99.0% of the national private row every year (the gap is undisclosed counties). **Pass** [DATA: `derived/qcew_fetch_audit.json`] |
| CDTFA taxable sales, 2015–2025, counties (58) and cities (483), groups C08 and C04 | Four quarters per unit-year; disclosure flags recorded | Counties complete in every year; some cities lack a quarter in 2024. The models keep units with 11 complete, unflagged years: 56 counties, and 80 of the 88 LA County cities. The eight dropped are Avalon, Bradbury, Hidden Hills, La Habra Heights, Palos Verdes Estates, Pomona, Rolling Hills and San Marino. **Pass** [DATA: `derived/cdtfa_fetch_audit.json`] |
| ACS 2013–2017 five-year: counties (3,142), California ZCTAs (1,764), places, placebo-state ZCTAs | Census sentinel values set missing | — |
| ACS EEO Tabulation 2014–2018, EEOALL1R (Hispanic share of food preparation and serving workers) | Published for 1,440 EEO county sets; mapped to 3,142 counties by the Census crosswalk | County-set food-prep workers sum to 9,579,938 against the national row's 9,579,900 (rounding); the national Hispanic share is 24.5%. |
| LAPD LAMC 42.00 arrests 2010–2019 | 5,097 rows; 5,046 vending; all located | 5,014 arrests in 2010–2016 fall in 99 ZCTAs; none is unlocated |

## 4. Design (fixed before the first outcome regression)

**Exposure, measured before 2018.**
- ACS 2013–2017 five-year estimates: the Hispanic, Mexican-origin and Mexico-born shares of
  residents, by county and by ZCTA.
- The Hispanic share of workers in food preparation and serving occupations, from the EEO Tabulation
  2014–2018, by county set.
- Inside the City of Los Angeles, the direct measure: log(1 + LAPD vending arrests, 2010–2016).

**Outcomes.**
- CBP 2012–2023 by county: establishments, mid-March employment and annual payroll for 722511,
  722513, 722330 and 7225, with 445110 grocery as the placebo.
- ZBP establishment counts for LA County ZIPs. ZIP files carry no employment or payroll below the
  all-industry total.
- QCEW county private employment, establishments and wages.
- CDTFA taxable sales for food services and drinking places (C08) and food and beverage stores (C04),
  by county and city.

**Comparisons.**
- (a) California counties against other states' counties, in two pools. P1 is every non-California
  county with a Hispanic share of at least 10% (680 counties). P2 is five nearest neighbours per
  California county on Hispanic share, log 2017 restaurant employment and 2012–2017 restaurant
  employment growth (181 distinct controls). County and year fixed effects, California × year, 2018
  omitted. Standard errors are clustered by county. A placebo-state permutation gives inference with
  one treated state.
- (a2) Triple difference: exposure × year and exposure × California × year, with county and state ×
  year fixed effects. State × year effects absorb anything common to California.
- (b) Within LA County: ZIP and year fixed effects, exposure × year, clustered by ZIP, on ZIPs present
  in all 12 years with at least 1,000 residents.
- COVID: 2019 is reported alone. 2020–2021 are shown but not interpreted. 2022–2023 are reported
  separately. Pre-period coefficients and a joint pre-trend test accompany every specification.

**Added after seeing data, and labelled as such:**
- the ZIP employment index. It proved invalid: from 2017, ZBP publishes a size-class row only when
  unsuppressed, and in 2019 class counts sum to the total in 64 of 263 LA full-service ZIPs;
- a trend-adjusted ZIP version, fitted because the pre-trend tests failed;
- the six-county ZIP placebo;
- the triple-difference placebo states;
- the arrest design without downtown, and its conversion into establishments
  (`analyze_zip_downtown.py`).

## 5. Results

### 5.1 What happened, before any model

| NAICS | Area | Establishments 2018→2019 | 2018→2023 | Employment 2018→2019 | 2018→2023 |
|---|---|---|---|---|---|
| 7225 restaurants | California | +0.6% | +4.6% | +0.3% | +1.6% |
| 7225 | Rest of US | +0.7% | +7.1% | +0.7% | +3.7% |
| 7225 | LA County | +1.0% | +4.0% | −0.3% | +0.2% |
| 722511 full-service | California | +0.6% | −1.4% | −0.3% | −6.7% |
| 722511 | Rest of US | +0.4% | +2.3% | +0.4% | −3.0% |
| 722513 limited-service | California | −0.4% | +6.1% | +1.0% | +6.9% |
| 722513 | Rest of US | +0.4% | +6.4% | +0.6% | +7.3% |
| 722330 mobile food | California | +13.2% | +78.0% | +6.5% | +56.6% |
| 722330 | Rest of US | +24.4% | +130.5% | +26.3% | +171.5% |
| 445110 grocery | California | +0.2% | +4.2% | +0.2% | +4.0% |
| 445110 | Rest of US | −2.3% | −3.0% | +0.9% | +7.1% |

[DATA: CBP county sums, `descriptive.py` → `derived/descriptive_ca_us.csv`; employment sums treat
suppressed small-county cells as zero, so they are approximate]

California's restaurants grew more slowly than the rest of the country after 2018, mostly in
full-service. Limited-service restaurants, whose price and format sit closest to street food, grew
about as fast as elsewhere.

### 5.2 California against other states (design a)

Log points × 100 (about percent). Ranges run across the four specifications: two pools × unweighted or
population-weighted. The permutation p comes from the placebo-state rank (P1 pool).

| Outcome | 2019 | SE | 2022–2023 | Pre-trend passes (p > 0.1) | Permutation p 2019 / 2022–23 |
|---|---|---|---|---|---|
| Restaurants (7225) employment, QCEW | −0.4 to +0.1 | 0.3–0.6 | −4.0 to −1.7 | 4 of 4 | 0.88–0.96 / 0.65–0.69 |
| Restaurants (7225) employment, CBP | −1.6 to −0.8 | 0.4–0.8 | −3.8 to −2.3 | 3 of 4 | 0.48–0.60 / 0.60–0.68 |
| Full-service employment, CBP | −2.4 to −1.2 | 0.5–1.1 | −5.1 to −3.3 | 0 of 4 | 0.48–0.64 / 0.48–0.64 |
| Full-service payroll, CBP | +0.9 to +1.6 | 0.4–0.8 | −2.7 to +0.4 | 0 of 4 | — |
| Limited-service employment, CBP | −0.4 to +1.6 | 0.6–1.1 | −2.8 to −1.2 | 2 of 4 | 0.88–1.00 / 0.72–0.84 |
| Mobile food (722330) establishments, CBP | −8.5 to −2.5 | 3.0–5.7 | −19.6 to −4.1 | 4 of 4 | 0.53–0.93 / 0.67–0.87 |
| Grocery employment, CBP (placebo) | −2.3 to −0.2 | 0.6–1.7 | −3.8 to +0.2 | 0 of 4 | 0.88–0.96 / 0.71–0.96 |
| Grocery employment, QCEW (placebo) | −0.6 to −0.1 | 0.5–0.8 | −0.2 to +1.6 | 4 of 4 | — |

[CALCULATION: `analyze_county.py` → `derived/county_event_summary.csv`, `derived/county_event_coefs.csv`,
`derived/county_permutation.csv`]

This design cannot attribute California's slower restaurant growth to vending, for four reasons:
- **The full-service path turns before the law.** California full-service employment had been gaining
  on the controls, from −5.0% in 2012 to +1.3% in 2017 against matched counties (2018 = 0). It lost
  1.3–3.5 points in 2018, a year before SB 946, across the four specifications, and 1.2–2.4 more in
  2019.
- **Payroll rose while employment fell.** In 2019 payroll rose +0.9% to +1.6% for full-service and
  +2.2% to +3.1% for limited-service. Displaced sales would cut both. The pattern fits California's
  minimum wage for large employers: $11 in 2018, $12 in 2019 and $15.50 by 2023, with higher city
  schedules [TRAINING-DATA].
- **Grocery fell too.** California grocery employment fell against the same controls (CBP 2022–23
  −3.8% population-weighted).
- **Other states produce gaps as large.** Every California estimate sits inside the spread that other
  high-Hispanic states produce against the same pool (permutation p 0.48–1.00).

### 5.3 Where vending is common, inside California (design a2)

Per 10 percentage points of the county's Hispanic share, net of the same gradient in other states
(state × year fixed effects). The first figure is unweighted, the second population-weighted.

| Outcome | 2019 | 2022–2023 | Placebo-state permutation p, 2019 | Placebo p10 to p90, 2019 |
|---|---|---|---|---|
| Full-service establishments | −1.0 (0.6) / −0.0 (0.3) | +1.2 / +0.8 | 0.77 / 1.00 | −5.4 to +3.4 / −2.5 to +4.8 |
| Full-service employment | +0.6 (0.6) / +0.0 (0.3) | +3.0 / +2.9 | 0.84 / 0.97 | −7.2 to +6.4 / −3.3 to +4.6 |
| Limited-service establishments | +0.9 (0.5) / +0.1 (0.3) | +2.3 / +1.9 | 0.71 / 0.92 | −1.8 to +4.0 / −2.0 to +3.1 |
| Limited-service employment | −0.7 (0.6) / −0.2 (0.4) | +1.1 / +2.5 | 0.86 / 0.86 | −3.0 to +7.3 / −3.9 to +4.8 |
| Mobile food establishments | +1.8 (2.9) / +2.6 (2.2) | +6.3 / +10.5 | one placebo state only | — |
| Grocery employment (placebo) | +0.6 (0.9) / −0.2 (0.4) | +0.9 / −1.5 | 0.81 / 1.00 | −5.3 to +6.2 / −5.0 to +4.5 |

[CALCULATION: `analyze_county.py`, `analyze_triple_placebo.py` → `derived/county_triple_summary.csv`,
`derived/triple_placebo_summary.csv`]

**Scale of the contrast.** Los Angeles County is 48% Hispanic and the least Hispanic California county
is 7%, so the LA contrast is about four units of the table. The most negative 2019 entry, −1.0% (SE
0.6), then implies about −4% for full-service establishments in LA against the least Hispanic county,
with a 95% interval of −8.5% to +0.7%. Every 2022–2023 entry is positive.

**Pre-trends** pass for full-service (p 0.10–0.59). They fail for limited-service when weighted by
population (establishments p 0.018, employment p 0.004).

**Exposure variants.**
- The Mexico-born share gives the most negative 2019 estimates. Its per-10-point unit is larger: the
  share runs from 0.7% to 29.4% across California counties and is 13.2% in Los Angeles. Estimates:
  - limited-service employment −2.3% (1.7) / −2.2% (1.2);
  - full-service establishments −3.2% (1.8) / −0.7% (1.1).

  All of them turn positive by 2022–2023.
- The food-prep workers' Hispanic share gives restaurant estimates within ±0.7% in 2019.

**Power.** The placebo-state spread (p10–p90 of roughly ±3–7% per 10 points) is much wider than the
county-clustered SEs. The county designs therefore rule out large effects only. The ZIP and city
designs below are sharper.

### 5.4 Los Angeles County ZIPs (design b) and six placebo counties

**By Hispanic share.** Per 10 points of the ZIP's Hispanic share, log establishments, ZIPs present in
all years:

| County | Full-service 2019 | 2022–23 | Limited-service 2019 | 2022–23 | All food service 2019 | 2022–23 |
|---|---|---|---|---|---|---|
| **Los Angeles (SB 946)** | **+0.1** | **+1.4** | **+0.0** | **+0.5** | **−0.1** | **+1.1** |
| Maricopa, AZ | −0.5 | −0.6 | +0.5 | −0.1 | +0.4 | +0.7 |
| Harris, TX | −0.4 | −1.2 | −0.4 | −0.1 | −0.2 | −0.6 |
| Dallas, TX | +0.8 | +0.8 | +0.1 | −0.9 | −0.3 | −1.0 |
| Bexar, TX | −0.4 | −1.8 | −0.3 | −0.3 | −0.2 | −2.1 |
| Cook, IL | 0.0 | +2.1 | −0.1 | +0.3 | +0.1 | +1.7 |
| Miami-Dade, FL | −1.2 | −2.1 | +0.2 | −1.7 | −0.2 | −1.7 |

[CALCULATION: `analyze_zip.py`, `analyze_zip_placebo.py` → `derived/zip_event_summary.csv`,
`derived/zip_placebo_summary.csv`. LA SEs in 2019 are 0.2–0.3. LA pre-trend tests: full-service
p 0.048, limited-service 0.11, all food service 0.63]

The six placebo counties are large, heavily Hispanic counties outside California, which SB 946 does
not reach. Chicago legalized food carts in 2015 [TRAINING-DATA], so Cook County's change falls inside
its pre-period.
- **2019.** Los Angeles ranks second to fourth of the seven counties.
- **2022–2023.** Only Cook County does better on full-service and on all food service, and none does
  better on limited-service.
- **Trend-adjusted.** Los Angeles full-service restaurants had already been gaining in Hispanic ZIPs
  before the law, at about +0.3% a year per 10 points. Net of that trend, the 2019 deviation is +0.2%
  (SE 0.4). The 2022–2023 deviation is +0.6% (log) or −0.4% (Poisson) [CALCULATION:
  `derived/zip_trend_adjusted.csv`].

**By vending arrests, the direct measure.** Inside the City of Los Angeles, exposure is log(1 + LAPD
vending arrests, 2010–2016). The most-arrested ZCTAs:
- 90057 Westlake–MacArthur Park, 980 arrests;
- 90015 South Park and the Fashion District, 944;
- 90011, 356, and 90037, 260, both in South LA;
- 90028 Hollywood, 354;
- 90021, 259, and 90013, 248, both downtown.

| Per log point of arrests | 2019 | 2022–2023 | Implied establishments against arrest-free ZIPs, 2019 (95%) |
|---|---|---|---|
| Full-service, all 98 City ZIPs, log | −0.7 (0.7) | +0.0 | −57 (−171 to +57) |
| Full-service, same, Poisson | −0.3 (0.6) | −1.0 | −21 (−121 to +79) |
| Full-service, without six downtown ZIPs, log | −1.1 (0.6) | +0.5 | −72 (−147 to +4) |
| Full-service, same, Poisson | −0.5 (0.4) | −1.1 | −33 (−91 to +26) |
| Limited-service, all City ZIPs, log / Poisson | +0.2 (0.5) / +0.0 (0.4) | −0.0 / −0.8 | +15 / +2 |
| All food service (722), all City ZIPs, log / Poisson | +0.6 (0.4) / +0.1 (0.3) | +0.1 / −0.1 | +135 / +33 |

[CALCULATION: `analyze_zip_downtown.py` → `derived/zip_arrests_no_downtown.csv`; the all-ZIP rows
reproduce `analyze_zip.py`. Pre-trend p for full-service: 0.07–0.24.]

**Size.** The City's arrest-sample ZIPs held 3,344 full-service restaurants in 2018. The pre-specified
design puts the 2019 shortfall in arrest hotspots at 21–57 restaurants (0.6–1.7%); without downtown,
the figure is 33–72. A shortfall of zero is not ruled out, and the 95% bound is about 170 (5%).

**Trend-adjusted (post hoc).** Removing the pre-2018 trend makes 2022–2023 more negative. That trend
was upward and imprecise: +0.45% to +0.63% a year per log point, SE 0.3–0.5. After removal, 2022–2023
comes to −1.3% to −3.0% per log point. In 90057, where log arrests ≈ 6.9, that is −9% to −21%.

**Downtown is not the explanation.** Dropping the six downtown ZIPs removes 35% of the arrests and
leaves the estimates unchanged or larger. So the pattern is not downtown's post-2020 loss of office
workers.

**Why this is a lean, not a finding:**
- it is not significant at 5% in any specification;
- limited-service restaurants show nothing in the same ZIPs;
- all food-service establishments did not fall there (2019 +0.6%, SE 0.4).

It has company in one other design. Full-service establishment counts also lean negative in 2019 in
the unweighted county triple difference: −0.7% to −3.2% per 10 points across the three exposures,
each less than 1.8 SE from zero (section 5.3). That lean does not carry over to employment or to the
population-weighted fits, and it is positive by 2022–2023. This is the result that would move most
with better data.

### 5.5 Taxable sales (CDTFA, California only)

Per 10 points of Hispanic share; C08 is food services and drinking places, C04 food and beverage stores.

| Unit | Outcome | 2019 | 2022–2023 | 2024–2025 |
|---|---|---|---|---|
| 56 counties | C08 sales | +0.1% (0.15) / +0.1% (0.13) | +2.6% / +2.5% | +3.0% / +2.2% |
| 56 counties | C08 minus C04 | −0.0% (0.3) / −0.3% (0.3) | +2.0% / −0.6% | +2.1% / −0.9% |
| 80 LA County cities | C08 sales | +0.2% (0.15) / +0.3% (0.15) | +0.5% / +1.2% | +0.8% / +1.3% |
| 80 LA County cities | C08 minus C04 | +0.7% (0.3) / +0.5% (0.2) | +0.3% / +0.7% | −0.1% / +0.6% |
| 80 LA County cities | C08 seller's-permit outlets | +0.2% (0.16) / +0.1% (0.16) | +1.4% / +1.1% | +1.5% / +1.1% |

[CALCULATION: `analyze_sales.py` → `derived/sales_event_summary.csv`]

C08 includes permitted vendors and food trucks. So these rows would show a sales shift from restaurants
to unpermitted street food; they would not show a shift to permitted vendors, a small group (section 2).

**Size of the contrast.** Beverly Hills is the least Hispanic city in the sample (6%) and Maywood the
most (98%). Between them, the city-level 2019 estimate implies +1.8% for Maywood's restaurant sales
(95% interval −0.8% to +4.5%) [INFERENCE: 9.2 × (0.20 ± 1.96 × 0.15)].

**Power.** Suppose Bogotá's cross-sectional elasticity (−0.044, section 7) held in Los Angeles. Then
a doubling of vending in Maywood, with none in Beverly Hills, would cut Maywood's restaurant sales by
3.0% relative. The interval excludes that [INFERENCE].

**Pre-trends** pass for the city C08 series (p 0.36, 0.16). They fail for three others:
- the county C08 series (p 0.04, 0.08);
- the county difference against grocery (p 0.000, 0.03);
- the population-weighted city difference (p 0.004).

### 5.6 Licensed food trucks (722330)

The brief asks whether licensed trucks grow or shrink where unlicensed vending rises.
- **Against other states:** California's employer food trucks grew more slowly than elsewhere: +78%
  against +131% in 2018–2023, and −2.5% to −8.5% in the 2019 event study (permutation p 0.53–0.93).
- **Inside California:** they grew faster in more Hispanic counties, +1.8% (SE 2.9) and +2.6% (SE 2.2)
  per 10 points in 2019, and +6% to +11% by 2022–2023. The unweighted pre-trend fails (p 0.0002).
- **At ZIP level:** the series cannot be used. After the 2017 publication change it covers only 12–31
  LA ZIPs a year [DATA: `derived/zip_722330_counts.csv`].

No finding that unlicensed vending crowded out licensed trucks, and no winners-and-losers row: the sign
is mixed.

## 6. How big street food is

| Year | Street food, City of LA ($m) | City of LA restaurant taxable sales, C08 ($m) | Share | Band |
|---|---|---|---|---|
| 2015 | 104 | 8,195 | 1.27% | 0.63–2.54% |
| 2018 | 112 | 9,705 | 1.15% | 0.58–2.31% |
| 2019 | 115 | 10,215 | 1.13% | 0.57–2.26% |
| 2022 | 134 | 10,922 | 1.23% | 0.61–2.46% |
| 2023 | 144 | 11,439 | 1.26% | 0.63–2.51% |
| 2024 | 150 | 11,570 | 1.29% | 0.65–2.59% |

[CALCULATION: `size_rows.py` → `derived/size_by_year.csv`, one year at a time; every year 2015–2025 is
in the file]

- **Construction.** Street food is 10,000 food vendors × $10,098 revenue per vendor in 2014, restated
  each year by the CPI for food away from home (BLS CUUR0000SEFV). The vendor count is the Bureau of
  Street Services estimate [SOURCE: CLA, CF 13-1493, 26 Nov 2014, p. 2]. The revenue figure is a 2014
  student survey of Westlake vendors [SOURCE: Economic Roundtable, *Sidewalk Stimulus*, 2015, p. 3;
  the report's own total, "over $100 million", p. 5; `reads/sidewalk_stimulus_2015.md`].
- **Band.** Both inputs are weak: an unsourced count and a convenience sample. The band is therefore
  half to double. The report itself is internally inconsistent: "three-quarters" of 50,000 vendors
  selling merchandise implies 12,500 food vendors, not 10,000.
- **California.** Scaling the city's figure by Hispanic residents (7.9×) gives $1.17bn in 2024, 1.05%
  of the state's $111.6bn C08 sales. Los Angeles probably has the densest street-food trade in the
  state, so this is an upper extrapolation.

If every street-food dollar in the City of Los Angeles came out of a restaurant's till, the city's
restaurants would have lost about 1.3% of sales (0.6–2.6%).

Two forces pull the true displacement away from one-for-one, in opposite directions:
- Vendors reportedly avoid selling food in front of restaurants (Kettles 2004, as summarized in
  *Sidewalk Stimulus*, p. 10). That would push displacement below one-for-one.
- The bound covers diverted sales only. Vendors might also cost nearby businesses through crowded
  sidewalks. Bogotá's cross-section puts that cost at several times vendors' own sales: vendors were
  2% of corridor sales, yet removing all of them raises shop sales 14% in the authors' simulation
  (section 7).

The change regressions in section 5 would pick up such costs wherever vending grew after
2019; the bound would not.

## 7. What the literature says

Read and quoted by the reader subagent. Notes are in `reads/`, with page-anchored quotes checked
against the parsed text; the summary is in `reads/LIT_US.md`.
- **Sidewalk Stimulus (Economic Roundtable, 2015).** Size as above. Its restaurant evidence is thin. It
  compares businesses on the same census block as a 2011–2012 vendor arrest with all others,
  2007–2011, as raw means with no controls: "Restaurants, near a street vendor, added one more job
  when compared to those far away" (p. 13). Grade D as evidence of any effect: vendors choose busy
  blocks. It was underwritten by East LA Community Corporation, a member of the LA Street Vendor
  Campaign. Under rule 3 that carries no weight in the grade.
- **Anenberg and Kung (2015, *Journal of Urban Economics*), working-paper version read.** Food trucks'
  advantage is mobility and variety. In Washington DC, mobility adds 7.6 trucks a week, "or 18% of the
  average number of nearby brick-and-mortar stores" (p. 27). It measures no restaurant outcome, so it
  informs neither side of the displacement question.
- **Carpenter and Sweetland, *Food Truck Truth* (Institute for Justice, 2022).** A dynamic county
  panel (CBP 2005–2016; Arellano-Bond, ethnic-diversity instrument). The lagged effect of employer
  food trucks on restaurant establishments is +1.837 restaurants per truck (SE 1.277, p 0.150; 95%
  interval about −0.67 to +4.34) across all counties.
  - Grade C−: it counts establishments only, about one truck per county, and its instrument has no
    credible exclusion restriction.
  - It quotes the restaurant side: "[W]hen there's a whole bunch (of trucks), we see a significant
    drop in sales" (p. 24).
  - The Institute litigates against food-truck limits; per rule 3 that carries no weight either.
- **Rocha, Sánchez and García (2009, *Desarrollo y Sociedad* 63), Bogotá.** The closest thing found
  to an estimate of vendors' effect on nearby formal shops. It is a cross-section of 694 surveyed
  establishments in four commercial corridors, 2004, controlling for each shop's 2003 scale.
  - The elasticity of shop sales to vendors on the block is −0.044 (p 0.08); for employment it is
    −0.05 (p < 0.01) (Cuadro 4, p. 263). Vendors were "tan sólo 2%" (only 2%) of corridor sales
    (p. 246). Removing all vendors raises shops' sales 14% and jobs 16% in the simulation, but cuts
    jobs in commerce as a whole by 2.1% (p. 263).
  - The authors argue the bias runs toward zero, because formal commerce attracts vendors, and
    concede reverse causality is unsolved (p. 264).
  - The shops are retail, not restaurants. Grade C.
  - Commissioned by the Bogotá chamber of commerce, the formal businesses' body; no weight under rule
    3.
- **Ulyssea (2018, *American Economic Review* 108(8)), Brazil.** A structural model of informal firms
  competing with formal ones. It finds 41.9% of informal firms stay informal for the cost advantage
  and could survive formally (p. 2036).
  - Enforcement that nearly eliminates informal firms raises the value of always-formal firms 7.4%
    (Table 5). It lowers welfare 6.7% and low-skill wages 8.5% (pp. 2043–2044).
  - "Low-productivity formal firms benefit the most" from enforcement (p. 2042).
  - The signs carry over to Los Angeles; the magnitudes do not, since Brazil's informal share of firms
    is 69%. Grade B as a model, not evidence on LA.
- **Erickson, *Street Eats, Safe Eats* (Institute for Justice, 2014).** Licensed vendors' sanitation;
  see section 9. Grade B− for the licensed comparison.

No study found estimates the effect of street-vending legalization on restaurants [VERIFIED NEGATIVE:
four searches covering SB 946, New York's permit caps and Chicago's 2015 cart ordinance, logged in
`reads/LIT_US.md`].

**Lean of the reading set.** Four of the sources read come from vendor-side sponsors and one from a
business-side sponsor. The restaurant-side documents found last were not read [GAP]: the California
Restaurant Association's LA Times op-ed (29 Jul 2026) and the Cal Cities city attorneys' whitepaper on
SB 946 enforcement. The restaurant complaint is therefore represented mainly by Bogotá, Ulyssea's
model and quotes inside the other reports.

## 8. Who wins and who loses

$bn a year in 2024 dollars, California unless stated. Written to `derived/winners_losers_rows.csv`.
Rows whose values are all non-negative are magnitudes in the stated direction. The two "measured"
rows are signed from the group's side (positive = better off), with direction set by the central.

| Group | Channel | Direction | Low | Central | High | Basis | Relation to account | Counterfactual |
|---|---|---|---|---|---|---|---|---|
| Licensed restaurant owners | Change after legalization: 2019 gradient of restaurant sales on Hispanic share across counties, applied to 2024 sales, × 0.35 margin | gain | −0.16 | +0.16 | +0.47 | measured | beside | pre-2019 regime |
| Licensed restaurant owners | Bound: every street-food dollar taken from restaurants, lost at the margin | loss | 0 | 0.41 | 1.17 | modelled | beside | no street food |
| Restaurant workers | Change after legalization: same regression × payroll per sales dollar (0.37) | gain | −0.17 | +0.17 | +0.50 | measured | beside | pre-2019 regime |
| Restaurant workers | Bound: payroll on every displaced street-food dollar, before re-employment | loss | 0 | 0.44 | 0.87 | modelled | overlaps: production term | no street food |
| Vendors (City of LA, 10,000 food vendors) | Net income: revenue less the 71% spent on inputs (Sidewalk Stimulus p. 4) | gain | 0.022 | 0.043 | 0.087 | modelled | beside | no street food; vendors' next-best earnings not deducted |
| Vendors | Gain from legalization itself: no arrests or records, fewer confiscations | gain | — | — | — | unpriced | beside | pre-2019 regime |
| Vendors' customers | Cheaper, closer food; variety | gain | — | — | — | unpriced | overlaps: consumer_price_benefit | no street food |
| Budget | Income and payroll tax on vendors' earnings | loss | — | — | — | unpriced here | **inside** | earnings reported like wages |
| Budget (City of LA) | Sales tax not remitted on street food at 9.5% | loss | 0.007 | 0.014 | 0.028 | modelled | beside | all vending taxed |
| Budget (City of LA) | Vending program cost net of permit receipts, FY2023-24 | loss | 0.0036 | 0.0036 | 0.0036 | measured | beside | no city program (the LAPD enforcement it replaced is not netted) |
| Residents near vending | Litter, obstruction, noise | loss | — | — | — | unpriced | beside | no street food |

- **Restaurant owners and workers.**
  - *Measured rows.* The measured change is centred on a small gain. For owners its interval runs from
    a loss of $0.16bn to a gain of $0.47bn.
  - *Bound rows.* These answer a different question: what if street food, which predates the law,
    took every dollar from restaurants? Measured and bound rows must not be added. Per establishment,
    the owners' bound is $5,160 a year (central) across California's 79,700 restaurants.
  - *Arrest hotspots.* The lean in section 5.4 is 21–57 City full-service restaurants (33–72 without
    downtown), if causal. It sits inside the bound.
- **How the ledger reads these rows.** `winners_losers_2026_09_24` reads the two measured rows as
  beside the account and keys them to California restaurant owners and workers (its `key_map.csv`).
  The bounds stay in its role table.
- **Budget: which correction carries the taxes.**
  - Income and payroll taxes on off-books earnings, vendors' included, are inside the adopted main
    case. They sit in the September 24 "Tax records" change: the Census tax model's status and
    compliance, CPS fill-ins, the Mexico-born recount and the state-aware status flag (audit rows 2,
    13 and 4). That change lowers the group's recorded taxes and adds +$19.9/+21.2bn to the net cost;
    the on-books share is its main sensitivity [SOURCE: `../main_case_2026_09_24/RESULT.md`, "What is
    in it" and the sensitivity table].
  - The channel's size is $1.5–3.4k per unauthorized adult a year [SOURCE:
    `../informal_channel_2026_09_16/RESULT.md` §4].
- **Sales tax.** Not in those corrections. The account allocates actual general sales tax by
  consumption, so tax never collected on street food is outside the totals. The only error it leaves
  is a small over-allocation to heavy street-food buyers [INFERENCE].
- **Residents.** Unpriced because no vending complaint series exists (section 2). The enclave lane found
  LA's dumping and graffiti gradients by Hispanic share vanish once income enters
  [SOURCE: `../../../research/immigration-enclave-neighborhood-quality-and-informality-2026-09-18.md`
  §9]. That tells nothing about vending specifically.

## 9. Steel-man, disconfirmation and symmetry

**The case that vendors hurt restaurants, at its strongest.** Unlicensed vendors pay no rent, no
health-permit or plan-check fees and no workers' compensation. Most pay no sales tax: the Economic
Roundtable itself puts unremitted sales tax at "At a minimum, $33 million" a year in the city (p. 6).
They can undercut a taqueria next door on price, and SB 946 bars cities from limiting them to protect
competitors (§51038(e)). Bogotá's cross-section finds lower sales at shops on blocks with more
vendors. Ulyssea's model finds formal firms, especially low-productivity ones, gain when informal
competitors are suppressed.

**What the data would show if that dominated.** Restaurant counts, jobs and taxable sales would fall
after 2019 where vending is dense (Hispanic neighbourhoods, arrest hotspots). The fall would show
against other places and other metros, and most of all in limited-service restaurants.
- *Demographic exposures:* zero in 2019 and the opposite sign in 2022–2023.
- *Arrest hotspots and the unweighted county comparison:* full-service restaurant counts in the
  predicted direction in 2019, but small, not significant and absent in limited-service (sections 5.3
  and 5.4).

**The case that vendors complement restaurants.** Street food sells at a lower price and later hours,
often to a different customer, and it adds foot traffic. The data do not prove this either. Positive
2022–2023 gradients also fit COVID-era shifts, such as restaurants in lower-income Hispanic
neighbourhoods recovering faster than downtown and Westside dining.

**Symmetry checks.**
- **Rule 1.** Every causal estimate here carries its SE and population. Where the placebo spread is
  wider than the SE, both are given.
- **Rule 2, a flaw both sides share.** Studies are graded on design, not sponsor. The advocacy-side
  studies (Sidewalk Stimulus, Food Truck Truth) and the chamber-of-commerce study (Bogotá) are graded
  that way. The restaurant-side claim quoted by IJ ("a significant drop in sales") is an anecdote
  with no data behind it, and is graded the same way.
- **Rule 4, the lean of this lane's own findings.** Across the specifications computed, the 2019 point
  estimates split both ways near zero, and most 2022–2023 point estimates favour "no harm". The
  negative results are reported in full:
  - California against other states on full-service employment. It is traced to timing, grocery and
    payroll; that attribution is itself a judgement.
  - Full-service establishment counts in 2019, in the arrest hotspots and the unweighted county
    comparison. These are not explained away and are carried into the verdict. The no-downtown check
    was run to test a benign explanation; it failed, and that is reported too.
- **Rule 5.** Benefits (vendors' income, customers) are listed beside costs. Customers are unpriced,
  as are residents' nuisance costs.

**Dirt.** This lane does not measure sanitation. The only inspection comparison covers licensed
vendors. In LA County in 2009–July 2012, violations per inspection averaged 3.6 for trucks, 2.4 for
carts and 7.8 for restaurants, with no adjustment for menu risk [SOURCE: Erickson, *Street Eats, Safe
Eats*, Institute for Justice 2014, LA section, Table 5; `reads/ij_street_eats_safe_eats_2014.md`].
Unpermitted vendors, the group the operator's question is about, are not inspected at all. "Over 73%
of surveyed sidewalk food vendors" sell food the county classes as high-risk [SOURCE: UCLA Law 2021,
p. 10].

[FRAMING-SENSITIVE]
- "Honest business" is the operator's framing.
- Since 2019, unpermitted vending can be penalized only by citation, and most vendors remain
  unlicensed. Whether that is dishonest competition is a value judgement.
- The data speak only to whether restaurants lost business.

## 10. Limits

- **Change, not level.** Street food was already widespread before 2019. These designs measure what
  changed after legalization. The level effect of street food on restaurants is not identified, and
  the size bound (section 6) stands in for it.
- **No measured vending series after 2019.** Exposure is demographic (Hispanic, Mexico-born and
  food-worker shares) or enforcement-based (pre-law arrests, City of LA only). If vending grew after
  2019 somewhere other than where these proxies point, the designs miss it.
- **Establishments and employment, not margins.** A restaurant that stays open with thinner margins
  shows up only in taxable sales and payroll. Those are measured at city and county level, not per
  business.
- **COVID and minimum wages** dominate 2020–2023 and differ between California and every control.
  2019 is the only clean year, and it is one year after the law. Vendor entry may have been gradual,
  and COVID cut the series before any slow response could show.
- **Instrument.** An LLM assembled this lane (`notes/llm-bias-caveat.md`). Specification choices were
  written into section 4 before outcomes were run. The additions made afterwards are listed there.

**Would change it:**
- a vending series by neighbourhood and year: county CMFO permits by address, StreetsLA citations by
  location, or card-transaction data on vendors;
- establishment-level restaurant revenue near vending corridors (card-spend panels) showing sales
  falling where vending rose after 2019, especially at limited-service restaurants;
- the arrest-hotspot lean becoming significant with full-service revenue or exits by address;
- a second clean post-law year without COVID. None exists.

## 11. Reproduce

From the repository root (Census key: `set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a`):

```sh
L=infra/immigration-fiscal/vending_restaurants_2026_09_24
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_cbp.py                                  # gate: US 722 vs flat files
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 $L/fetch_acs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_zbp.py                                  # gate in analyze_zip.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_qcew.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/fetch_cdtfa.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with shapely --with pyshp python3 $L/fetch_lapd.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 $L/fetch_zbp_placebo.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/descriptive.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 $L/analyze_county.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 $L/analyze_triple_placebo.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 $L/analyze_zip.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 $L/analyze_zip_downtown.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with openpyxl python3 $L/analyze_zip_placebo.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 $L/analyze_sales.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/size_rows.py
uv run --no-project python3 $L/render_tables.py && uv run --no-project python3 $L/assemble_result.py
```

The CPI series for the size table was fetched once to `_cache/bls/` (BLS API v2, series CUUR0000SEFV,
annual averages 2014–2025); `size_rows.py` reads it from there.

## Appendix: every computed specification

Generated by `render_tables.py` from `derived/`; do not edit by hand.

### A0. Pre-period coefficients of the headline specifications

Log points x 100 (SE), 2018 = 0; per 10 points of the share or per log point of arrests. QCEW starts in 2014 and CDTFA in 2015. Every other specification's pre-period coefficients are in the `derived/*_coefs.csv` files.

| specification | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 |
|---|---|---|---|---|---|---|
| (a) QCEW 7225 employment, P1, unweighted |  |  | -1.8 (1.2) | -1.9 (0.9) | -1.2 (0.9) | -0.3 (0.6) |
| (a) CBP full-service employment, P2, unweighted | -5.0 (2.2) | -3.3 (2.0) | -1.8 (2.0) | -0.8 (1.8) | -1.2 (1.7) | +1.3 (1.1) |
| (a2) full-service establishments, Hispanic share, unweighted | +0.5 (1.3) | +0.9 (1.4) | +1.2 (1.3) | +0.2 (1.4) | -0.6 (1.0) | +0.2 (0.8) |
| (a2) limited-service employment, Hispanic share, pop-weighted | -0.4 (0.7) | -0.8 (0.7) | -1.8 (0.8) | -1.2 (0.7) | -0.5 (0.5) | -0.2 (0.4) |
| (b) LA ZIPs full-service, Hispanic share | -1.6 (0.7) | -1.5 (0.6) | -1.5 (0.6) | -1.6 (0.5) | -0.9 (0.5) | -0.7 (0.3) |
| (b) LA ZIPs limited-service, Hispanic share | +0.8 (0.6) | +1.4 (0.6) | +0.7 (0.6) | +0.7 (0.4) | +0.5 (0.4) | +0.3 (0.2) |
| (b) City ZIPs full-service, arrests | -3.4 (2.2) | -3.0 (2.1) | -4.2 (2.3) | -3.1 (1.3) | -2.8 (1.2) | -1.4 (0.7) |
| (b) City ZIPs full-service, arrests, Poisson | -2.3 (1.6) | -2.8 (1.3) | -3.1 (1.2) | -2.5 (1.1) | -1.5 (0.7) | -0.9 (0.4) |
| sales: LA County cities C08, unweighted |  |  |  | -0.4 (0.3) | -0.3 (0.2) | -0.2 (0.1) |
| sales: counties C08, pop-weighted |  |  |  | -0.6 (0.3) | -0.4 (0.2) | -0.1 (0.1) |



### A1. California against other states' counties (design a), every specification

Log points x 100 (about percent). b2019 is the 2019 coefficient with its county-clustered SE; b2022-23 the mean of 2022 and 2023; pre p the joint test of 2012-2017 (QCEW 2014-2017); perm p the placebo-state rank p-value (P1 only).

| source | NAICS | outcome | pool | weight | CA/controls | b2019 (SE) | b2020-21 | b2022-23 | pre p | perm p 2019 | perm p 2022-23 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cbp | 722511 | estab | P1 | none | 57/581 | -0.1 (1.0) | -1.2 | -2.9 | 0.84 |  |  |
| cbp | 722511 | estab | P1 | pop | 57/581 | -0.2 (0.4) | -2.5 | -5.1 | 0.00 |  |  |
| cbp | 722511 | estab | P2 | none | 57/180 | -0.5 (1.1) | -2.0 | -4.7 | 0.65 |  |  |
| cbp | 722511 | estab | P2 | pop | 57/180 | -0.5 (0.5) | -3.2 | -6.0 | 0.00 |  |  |
| cbp | 722511 | emp | P1 | none | 54/516 | -1.8 (1.0) | -9.7 | -3.3 | 0.00 | 0.48 | 0.64 |
| cbp | 722511 | emp | P1 | pop | 54/516 | -1.2 (0.5) | -7.9 | -3.8 | 0.00 | 0.64 | 0.48 |
| cbp | 722511 | emp | P2 | none | 54/178 | -2.4 (1.1) | -9.0 | -3.5 | 0.07 |  |  |
| cbp | 722511 | emp | P2 | pop | 54/178 | -2.0 (0.5) | -9.9 | -5.1 | 0.00 |  |  |
| cbp | 722511 | payann | P1 | none | 56/557 | +1.6 (0.8) | -9.4 | +0.4 | 0.00 |  |  |
| cbp | 722511 | payann | P1 | pop | 56/557 | +1.1 (0.4) | -7.3 | -1.9 | 0.00 |  |  |
| cbp | 722511 | payann | P2 | none | 56/180 | +1.1 (0.8) | -6.8 | +0.4 | 0.00 |  |  |
| cbp | 722511 | payann | P2 | pop | 56/180 | +0.9 (0.5) | -8.7 | -2.7 | 0.00 |  |  |
| cbp | 722513 | estab | P1 | none | 55/569 | -0.5 (0.8) | -2.7 | -0.4 | 0.31 |  |  |
| cbp | 722513 | estab | P1 | pop | 55/569 | -1.0 (0.4) | -2.4 | -0.9 | 0.00 |  |  |
| cbp | 722513 | estab | P2 | none | 55/179 | -0.4 (0.9) | -2.5 | -0.6 | 0.56 |  |  |
| cbp | 722513 | estab | P2 | pop | 55/179 | -1.3 (0.5) | -3.3 | -2.0 | 0.00 |  |  |
| cbp | 722513 | emp | P1 | none | 53/517 | +0.7 (0.9) | -4.1 | -2.3 | 0.69 | 0.88 | 0.84 |
| cbp | 722513 | emp | P1 | pop | 53/517 | +0.0 (0.6) | -2.9 | -1.2 | 0.05 | 1.00 | 0.72 |
| cbp | 722513 | emp | P2 | none | 53/174 | +1.6 (1.1) | -3.2 | -2.8 | 0.49 |  |  |
| cbp | 722513 | emp | P2 | pop | 53/174 | -0.4 (0.7) | -3.6 | -2.6 | 0.00 |  |  |
| cbp | 722513 | payann | P1 | none | 54/540 | +2.8 (0.9) | -0.9 | +1.2 | 0.00 |  |  |
| cbp | 722513 | payann | P1 | pop | 54/540 | +2.2 (0.7) | +1.0 | +0.8 | 0.00 |  |  |
| cbp | 722513 | payann | P2 | none | 54/178 | +3.1 (1.1) | +0.2 | -1.3 | 0.01 |  |  |
| cbp | 722513 | payann | P2 | pop | 54/178 | +2.7 (1.0) | +0.6 | -0.4 | 0.00 |  |  |
| cbp | 722330 | estab | P1 | none | 27/119 | -2.5 (4.0) | -3.7 | -4.1 | 0.53 | 0.93 | 0.87 |
| cbp | 722330 | estab | P1 | pop | 27/119 | -6.0 (3.0) | -11.4 | -11.8 | 0.15 | 0.53 | 0.67 |
| cbp | 722330 | estab | P2 | none | 27/53 | -8.0 (5.7) | -10.7 | -14.0 | 0.99 |  |  |
| cbp | 722330 | estab | P2 | pop | 27/53 | -8.5 (3.6) | -17.5 | -19.6 | 0.95 |  |  |
| cbp | 722330 | emp | P1 | none | 10/15 | +1.1 (12.3) | -10.4 | -7.8 | 0.02 |  |  |
| cbp | 722330 | emp | P1 | pop | 10/15 | -7.5 (8.5) | -19.4 | -14.4 | 0.00 |  |  |
| cbp | 722330 | emp | P2 | none | 10/7 | -1.2 (10.5) | +4.8 | +17.0 | 0.01 |  |  |
| cbp | 722330 | emp | P2 | pop | 10/7 | -9.2 (7.8) | -14.8 | -5.2 | 0.00 |  |  |
| cbp | 722330 | payann | P1 | none | 16/62 | -4.1 (8.0) | -20.2 | -24.4 | 0.00 |  |  |
| cbp | 722330 | payann | P1 | pop | 16/62 | -6.0 (4.9) | -23.2 | -20.0 | 0.00 |  |  |
| cbp | 722330 | payann | P2 | none | 16/29 | +4.7 (8.4) | -2.5 | -6.9 | 0.02 |  |  |
| cbp | 722330 | payann | P2 | pop | 16/29 | -3.3 (6.5) | -17.4 | -11.8 | 0.00 |  |  |
| cbp | 445110 | estab | P1 | none | 56/448 | +1.2 (1.7) | +3.9 | +6.6 | 0.01 |  |  |
| cbp | 445110 | estab | P1 | pop | 56/448 | +1.4 (0.7) | +3.3 | +3.4 | 0.02 |  |  |
| cbp | 445110 | estab | P2 | none | 56/159 | +0.9 (1.9) | +3.7 | +6.6 | 0.01 |  |  |
| cbp | 445110 | estab | P2 | pop | 56/159 | +1.4 (0.9) | +2.6 | +2.3 | 0.06 |  |  |
| cbp | 445110 | emp | P1 | none | 53/281 | -1.4 (1.7) | +0.2 | -0.5 | 0.00 | 0.88 | 0.96 |
| cbp | 445110 | emp | P1 | pop | 53/281 | -0.2 (0.6) | -1.4 | -3.5 | 0.00 | 0.96 | 0.71 |
| cbp | 445110 | emp | P2 | none | 53/103 | -2.3 (1.7) | +0.0 | +0.2 | 0.01 |  |  |
| cbp | 445110 | emp | P2 | pop | 53/103 | -1.3 (0.7) | -1.3 | -3.8 | 0.00 |  |  |
| cbp | 445110 | payann | P1 | none | 53/295 | +3.2 (1.5) | +7.5 | +2.4 | 0.03 |  |  |
| cbp | 445110 | payann | P1 | pop | 53/295 | +1.8 (0.6) | +4.0 | -0.5 | 0.02 |  |  |
| cbp | 445110 | payann | P2 | none | 53/108 | +3.6 (1.5) | +7.7 | +3.8 | 0.00 |  |  |
| cbp | 445110 | payann | P2 | pop | 53/108 | +1.6 (0.9) | +3.8 | +0.1 | 0.03 |  |  |
| cbp | 7225 | emp | P1 | none | 56/572 | -1.4 (0.7) | -6.4 | -3.3 | 0.12 | 0.60 | 0.68 |
| cbp | 7225 | emp | P1 | pop | 56/572 | -0.8 (0.4) | -4.1 | -2.3 | 0.01 | 0.48 | 0.60 |
| cbp | 7225 | emp | P2 | none | 56/181 | -1.6 (0.8) | -5.8 | -3.7 | 0.80 |  |  |
| cbp | 7225 | emp | P2 | pop | 56/181 | -1.3 (0.4) | -5.4 | -3.8 | 0.32 |  |  |
| qcew | 7225 | estabs | P1 | none | 51/415 | +0.5 (0.5) | -2.2 | -4.4 | 0.00 |  |  |
| qcew | 7225 | estabs | P1 | pop | 51/415 | +0.5 (0.3) | -1.4 | -2.7 | 0.00 |  |  |
| qcew | 7225 | estabs | P2 | none | 51/147 | +0.2 (0.6) | -2.7 | -4.8 | 0.00 |  |  |
| qcew | 7225 | estabs | P2 | pop | 51/147 | +0.1 (0.4) | -2.3 | -3.7 | 0.00 |  |  |
| qcew | 7225 | emp | P1 | none | 51/415 | -0.4 (0.5) | -7.0 | -3.0 | 0.24 | 0.96 | 0.65 |
| qcew | 7225 | emp | P1 | pop | 51/415 | +0.1 (0.3) | -4.0 | -1.7 | 0.44 | 0.88 | 0.69 |
| qcew | 7225 | emp | P2 | none | 51/147 | -0.3 (0.6) | -5.6 | -4.0 | 0.31 |  |  |
| qcew | 7225 | emp | P2 | pop | 51/147 | -0.1 (0.3) | -6.0 | -3.2 | 0.29 |  |  |
| qcew | 7225 | wages | P1 | none | 51/415 | +0.9 (0.6) | -4.3 | -0.7 | 0.00 |  |  |
| qcew | 7225 | wages | P1 | pop | 51/415 | +1.0 (0.4) | -2.5 | -0.5 | 0.00 |  |  |
| qcew | 7225 | wages | P2 | none | 51/147 | +0.7 (0.7) | -2.7 | -2.0 | 0.00 |  |  |
| qcew | 7225 | wages | P2 | pop | 51/147 | +0.8 (0.5) | -4.1 | -1.5 | 0.00 |  |  |
| qcew | 722511 | emp | P1 | none | 53/399 | +0.2 (0.7) | -11.3 | -4.9 | 0.36 |  |  |
| qcew | 722511 | emp | P1 | pop | 53/399 | -0.3 (0.4) | -9.2 | -4.4 | 0.39 |  |  |
| qcew | 722511 | emp | P2 | none | 53/154 | -0.1 (0.7) | -10.3 | -6.5 | 0.22 |  |  |
| qcew | 722511 | emp | P2 | pop | 53/154 | -0.8 (0.4) | -12.1 | -6.8 | 0.04 |  |  |
| qcew | 722513 | emp | P1 | none | 51/494 | -0.9 (0.8) | -4.2 | -2.6 | 0.00 |  |  |
| qcew | 722513 | emp | P1 | pop | 51/494 | +0.5 (0.3) | -0.9 | +0.2 | 0.04 |  |  |
| qcew | 722513 | emp | P2 | none | 51/165 | -0.1 (0.9) | -2.6 | -2.6 | 0.14 |  |  |
| qcew | 722513 | emp | P2 | pop | 51/165 | +0.5 (0.5) | -2.0 | -0.4 | 0.10 |  |  |
| qcew | 445110 | emp | P1 | none | 43/218 | -0.1 (0.8) | +0.5 | -0.2 | 0.27 |  |  |
| qcew | 445110 | emp | P1 | pop | 43/218 | -0.4 (0.5) | +0.5 | +1.6 | 0.24 |  |  |
| qcew | 445110 | emp | P2 | none | 43/92 | -0.6 (0.8) | +0.1 | +0.4 | 0.51 |  |  |
| qcew | 445110 | emp | P2 | pop | 43/92 | -0.4 (0.6) | -0.6 | +1.1 | 0.27 |  |  |


### A2. Triple difference (design a2), every specification

Per 10 points of the exposure share; state x year fixed effects.

| NAICS | outcome | exposure | weight | CA/other counties | d2019 (SE) | d2020-21 | d2022-23 | pre p |
|---|---|---|---|---|---|---|---|---|
| 722511 | estab | hisp_share | none | 57/2658 | -1.0 (0.6) | +0.2 | +1.2 | 0.33 |
| 722511 | estab | hisp_share | pop | 57/2658 | -0.0 (0.3) | +0.6 | +0.7 | 0.59 |
| 722511 | estab | mexborn_share | none | 57/2658 | -3.2 (1.8) | -0.0 | +2.4 | 0.88 |
| 722511 | estab | mexborn_share | pop | 57/2658 | -0.6 (1.1) | +1.9 | +1.9 | 0.28 |
| 722511 | estab | foodprep_hisp_share | none | 57/2658 | -0.7 (0.5) | -0.2 | +1.0 | 0.21 |
| 722511 | estab | foodprep_hisp_share | pop | 57/2658 | +0.0 (0.3) | +0.3 | +0.3 | 0.38 |
| 722511 | emp | hisp_share | none | 54/2305 | +0.6 (0.6) | +1.1 | +3.0 | 0.10 |
| 722511 | emp | hisp_share | pop | 54/2305 | +0.0 (0.3) | +2.4 | +2.9 | 0.44 |
| 722511 | emp | mexborn_share | none | 54/2305 | +1.8 (2.1) | +1.7 | +7.3 | 0.16 |
| 722511 | emp | mexborn_share | pop | 54/2305 | +1.7 (1.0) | +8.6 | +10.1 | 0.09 |
| 722511 | emp | foodprep_hisp_share | none | 54/2305 | +0.4 (0.7) | +0.7 | +2.3 | 0.65 |
| 722511 | emp | foodprep_hisp_share | pop | 54/2305 | +0.1 (0.3) | +1.8 | +2.1 | 0.63 |
| 722513 | estab | hisp_share | none | 55/2522 | +0.9 (0.5) | +1.0 | +2.3 | 0.66 |
| 722513 | estab | hisp_share | pop | 55/2522 | +0.1 (0.3) | +1.0 | +1.9 | 0.02 |
| 722513 | estab | mexborn_share | none | 55/2522 | +2.2 (1.6) | +3.2 | +5.8 | 0.50 |
| 722513 | estab | mexborn_share | pop | 55/2522 | +0.1 (0.9) | +2.6 | +5.4 | 0.08 |
| 722513 | estab | foodprep_hisp_share | none | 55/2522 | +0.5 (0.5) | +0.3 | +0.9 | 0.58 |
| 722513 | estab | foodprep_hisp_share | pop | 55/2522 | -0.2 (0.3) | +0.5 | +1.3 | 0.02 |
| 722513 | emp | hisp_share | none | 53/2233 | -0.7 (0.6) | -0.6 | +1.1 | 0.15 |
| 722513 | emp | hisp_share | pop | 53/2233 | -0.2 (0.4) | +2.2 | +2.5 | 0.00 |
| 722513 | emp | mexborn_share | none | 53/2233 | -2.3 (1.7) | -2.6 | +1.4 | 0.16 |
| 722513 | emp | mexborn_share | pop | 53/2233 | -2.2 (1.2) | +4.4 | +5.0 | 0.04 |
| 722513 | emp | foodprep_hisp_share | none | 53/2233 | -0.3 (0.5) | -0.9 | +0.2 | 0.07 |
| 722513 | emp | foodprep_hisp_share | pop | 53/2233 | -0.4 (0.4) | +1.7 | +1.8 | 0.00 |
| 722330 | estab | hisp_share | none | 27/273 | +1.8 (2.9) | +5.3 | +6.2 | 0.00 |
| 722330 | estab | hisp_share | pop | 27/273 | +2.6 (2.2) | +7.7 | +10.5 | 0.25 |
| 722330 | estab | mexborn_share | none | 27/273 | +3.9 (10.1) | +15.7 | +16.1 | 0.00 |
| 722330 | estab | mexborn_share | pop | 27/273 | +3.7 (8.6) | +12.6 | +26.4 | 0.02 |
| 722330 | estab | foodprep_hisp_share | none | 27/273 | +2.0 (2.9) | +4.8 | +5.0 | 0.00 |
| 722330 | estab | foodprep_hisp_share | pop | 27/273 | +2.1 (2.1) | +5.4 | +7.1 | 0.58 |
| 722330 | emp | hisp_share | none | 10/20 | -2.1 (14.0) | +1.4 | -11.7 | 0.00 |
| 722330 | emp | hisp_share | pop | 10/20 | +7.9 (15.4) | +10.1 | +9.2 | 0.00 |
| 722330 | emp | mexborn_share | none | 10/20 | -53.6 (39.1) | -104.8 | -87.2 | 0.00 |
| 722330 | emp | mexborn_share | pop | 10/20 | -43.8 (39.6) | -69.5 | -20.4 | 0.00 |
| 722330 | emp | foodprep_hisp_share | none | 10/20 | +8.2 (11.8) | -2.8 | +14.8 | 0.01 |
| 722330 | emp | foodprep_hisp_share | pop | 10/20 | +11.5 (9.3) | +4.2 | +25.0 | 0.00 |
| 445110 | estab | hisp_share | none | 56/1969 | +0.2 (0.8) | +0.3 | +0.5 | 0.17 |
| 445110 | estab | hisp_share | pop | 56/1969 | -0.4 (0.4) | -0.0 | +0.1 | 0.04 |
| 445110 | estab | mexborn_share | none | 56/1969 | +1.6 (2.8) | +1.0 | +0.3 | 0.11 |
| 445110 | estab | mexborn_share | pop | 56/1969 | -1.2 (1.5) | -1.4 | -3.3 | 0.01 |
| 445110 | estab | foodprep_hisp_share | none | 56/1969 | -0.0 (1.1) | -0.6 | -1.0 | 0.13 |
| 445110 | estab | foodprep_hisp_share | pop | 56/1969 | -0.7 (0.4) | -0.6 | -1.2 | 0.02 |
| 445110 | emp | hisp_share | none | 53/1257 | +0.6 (0.9) | -0.2 | +0.9 | 0.08 |
| 445110 | emp | hisp_share | pop | 53/1257 | -0.2 (0.4) | -1.6 | -1.5 | 0.04 |
| 445110 | emp | mexborn_share | none | 53/1257 | +1.7 (2.7) | +1.2 | +4.0 | 0.13 |
| 445110 | emp | mexborn_share | pop | 53/1257 | -0.7 (1.3) | -4.9 | -4.8 | 0.01 |
| 445110 | emp | foodprep_hisp_share | none | 53/1257 | +0.4 (1.1) | -1.8 | -1.4 | 0.16 |
| 445110 | emp | foodprep_hisp_share | pop | 53/1257 | -0.2 (0.4) | -1.8 | -2.2 | 0.00 |


### A3. Triple difference, California against placebo states (Hispanic share)

p10/p90 are the 10th and 90th percentiles of the same coefficient with each other state (20+ counties) in California's place.

| NAICS | outcome | weight | placebo states | CA d2019 | placebo p10-p90 | perm p | CA d2022-23 | placebo p10-p90 | perm p |
|---|---|---|---|---|---|---|---|---|---|
| 445110 | emp | none | 26 | +0.6 | -5.3 to +6.2 | 0.81 | +0.9 | -5.8 to +14.8 | 0.85 |
| 445110 | emp | pop | 26 | -0.2 | -5.0 to +4.5 | 1.00 | -1.5 | -4.2 to +23.6 | 0.74 |
| 722330 | estab | none | 1 | +1.8 | -0.8 to -0.8 | 0.50 | +6.2 | -9.0 to -9.0 | 1.00 |
| 722330 | estab | pop | 1 | +2.6 | +0.2 to +0.2 | 0.50 | +10.5 | -4.0 to -4.0 | 0.50 |
| 722511 | emp | none | 37 | +0.6 | -7.2 to +6.4 | 0.84 | +3.0 | -10.0 to +7.5 | 0.47 |
| 722511 | emp | pop | 37 | +0.0 | -3.3 to +4.6 | 0.97 | +2.9 | -20.8 to +4.2 | 0.47 |
| 722511 | estab | none | 38 | -1.0 | -5.3 to +3.4 | 0.77 | +1.2 | -3.7 to +13.3 | 0.90 |
| 722511 | estab | pop | 38 | -0.0 | -2.5 to +4.8 | 1.00 | +0.7 | -2.0 to +8.0 | 0.79 |
| 722513 | emp | none | 35 | -0.7 | -3.0 to +7.3 | 0.86 | +1.1 | -4.7 to +14.7 | 0.94 |
| 722513 | emp | pop | 35 | -0.2 | -3.9 to +4.8 | 0.86 | +2.5 | -6.8 to +6.4 | 0.42 |
| 722513 | estab | none | 37 | +0.9 | -1.8 to +4.0 | 0.71 | +2.3 | -3.2 to +8.7 | 0.55 |
| 722513 | estab | pop | 37 | +0.1 | -2.0 to +3.1 | 0.92 | +1.9 | -1.6 to +5.5 | 0.39 |


### A4. Los Angeles County ZIPs (design b), every specification

Per 10 points of the share, or per log point of 2010-2016 LAPD vending arrests (City of LA ZIPs). The employment index rows are invalid (size classes suppressed from 2017) and are shown only because they were computed.

| NAICS | exposure | outcome | ZIPs | b2019 (SE) | b2020-21 | b2022-23 | pre p | note |
|---|---|---|---|---|---|---|---|---|
| 722511 | hisp_share | log_estab | 258 | +0.1 (0.3) | +1.2 | +1.4 | 0.05 |  |
| 722511 | hisp_share | estab_poisson | 258 | +0.1 (0.2) | +0.6 | +0.8 | 0.00 |  |
| 722511 | hisp_share | log_emp_index | 258 | +3.0 (1.7) | +5.7 | +6.9 | 0.05 | invalid |
| 722511 | mexborn_share | log_estab | 258 | +0.5 (0.9) | +3.9 | +4.1 | 0.13 |  |
| 722511 | mexborn_share | estab_poisson | 258 | -0.0 (0.7) | +1.8 | +2.1 | 0.00 |  |
| 722511 | mexborn_share | log_emp_index | 258 | +7.7 (4.5) | +16.5 | +19.4 | 0.04 | invalid |
| 722511 | arrests | log_estab | 98 | -0.7 (0.7) | -0.6 | +0.0 | 0.20 |  |
| 722511 | arrests | estab_poisson | 98 | -0.3 (0.6) | -1.0 | -1.0 | 0.07 |  |
| 722511 | arrests | log_emp_index | 98 | +6.2 (4.2) | +0.7 | +2.6 | 0.08 | invalid |
| 722513 | hisp_share | log_estab | 262 | +0.0 (0.2) | +0.9 | +0.5 | 0.11 |  |
| 722513 | hisp_share | estab_poisson | 262 | +0.2 (0.2) | +0.9 | +0.7 | 0.02 |  |
| 722513 | hisp_share | log_emp_index | 262 | -1.6 (1.3) | +1.4 | -0.8 | 0.04 | invalid |
| 722513 | mexborn_share | log_estab | 262 | +0.4 (0.6) | +2.6 | +1.3 | 0.01 |  |
| 722513 | mexborn_share | estab_poisson | 262 | +0.6 (0.5) | +2.4 | +1.4 | 0.00 |  |
| 722513 | mexborn_share | log_emp_index | 262 | -3.8 (3.4) | +3.6 | -1.9 | 0.02 | invalid |
| 722513 | arrests | log_estab | 98 | +0.2 (0.5) | -0.2 | -0.0 | 0.17 |  |
| 722513 | arrests | estab_poisson | 98 | +0.0 (0.4) | -0.5 | -0.8 | 0.43 |  |
| 722513 | arrests | log_emp_index | 98 | -5.7 (3.7) | -2.6 | -5.4 | 0.75 | invalid |
| 722 | hisp_share | log_estab | 271 | -0.1 (0.2) | +0.9 | +1.1 | 0.63 |  |
| 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +0.7 | +1.1 | 0.02 |  |
| 722 | hisp_share | log_emp_index | 271 | +0.5 (0.7) | +2.9 | +2.0 | 0.08 | invalid |
| 722 | mexborn_share | log_estab | 271 | +0.1 (0.4) | +2.5 | +2.9 | 0.76 |  |
| 722 | mexborn_share | estab_poisson | 271 | +0.2 (0.3) | +2.1 | +2.8 | 0.22 |  |
| 722 | mexborn_share | log_emp_index | 271 | +2.4 (2.3) | +7.8 | +4.8 | 0.23 | invalid |
| 722 | arrests | log_estab | 102 | +0.6 (0.4) | +0.2 | +0.1 | 0.68 |  |
| 722 | arrests | estab_poisson | 102 | +0.1 (0.3) | -0.1 | -0.1 | 0.60 |  |
| 722 | arrests | log_emp_index | 102 | +4.8 (3.5) | +3.2 | +1.3 | 0.38 | invalid |
| 445110 | hisp_share | log_estab | 214 | -0.3 (0.3) | -0.6 | -1.1 | 0.03 |  |
| 445110 | hisp_share | estab_poisson | 214 | -0.2 (0.3) | -0.8 | -1.2 | 0.02 |  |
| 445110 | hisp_share | log_emp_index | 214 | -10.5 (4.7) | -7.9 | -12.2 | 0.66 | invalid |
| 445110 | mexborn_share | log_estab | 214 | -0.8 (0.9) | -2.1 | -3.5 | 0.04 |  |
| 445110 | mexborn_share | estab_poisson | 214 | -0.6 (0.9) | -2.6 | -3.7 | 0.05 |  |
| 445110 | mexborn_share | log_emp_index | 214 | -26.3 (12.0) | -19.0 | -28.5 | 0.42 | invalid |
| 445110 | arrests | log_estab | 81 | -0.9 (0.9) | -0.2 | -1.0 | 0.27 |  |
| 445110 | arrests | estab_poisson | 81 | -0.1 (0.7) | -0.3 | -1.2 | 0.10 |  |
| 445110 | arrests | log_emp_index | 81 | -30.1 (13.0) | -14.9 | -19.2 | 0.01 | invalid |


### A4b. Los Angeles County ZIPs, trend-adjusted (added after the pre-trend tests failed)

Exposure x linear trend estimated on 2012-2018; dev = deviation from that trend.

| NAICS | exposure | outcome | ZIPs | pre-trend per year (SE) | dev2019 (SE) | dev2022-23 (SE 2022, 2023) |
|---|---|---|---|---|---|---|
| 722511 | hisp_share | log_estab | 258 | +0.3 (0.1) | +0.2 (0.4) | +0.6 (0.9, 1.0) |
| 722511 | hisp_share | estab_poisson | 258 | +0.3 (0.1) | -0.0 (0.3) | -0.4 (0.6, 0.7) |
| 722511 | mexborn_share | log_estab | 258 | +0.5 (0.3) | +0.9 (1.1) | +2.6 (2.7, 3.1) |
| 722511 | mexborn_share | estab_poisson | 258 | +0.8 (0.2) | -0.3 (0.8) | -1.0 (1.6, 2.0) |
| 722511 | arrests | log_estab | 98 | +0.5 (0.4) | -0.2 (1.3) | -1.4 (2.4, 3.0) |
| 722511 | arrests | estab_poisson | 98 | +0.5 (0.3) | -0.2 (0.8) | -2.5 (1.2, 1.8) |
| 722513 | hisp_share | log_estab | 262 | -0.2 (0.1) | +0.1 (0.3) | +1.1 (0.8, 0.8) |
| 722513 | hisp_share | estab_poisson | 262 | -0.1 (0.1) | +0.2 (0.2) | +1.1 (0.6, 0.6) |
| 722513 | mexborn_share | log_estab | 262 | -0.5 (0.3) | +0.2 (0.8) | +2.9 (1.9, 2.1) |
| 722513 | mexborn_share | estab_poisson | 262 | -0.4 (0.2) | +0.4 (0.6) | +2.6 (1.4, 1.6) |
| 722513 | arrests | log_estab | 98 | -0.1 (0.2) | +0.1 (0.6) | +0.4 (1.3, 1.6) |
| 722513 | arrests | estab_poisson | 98 | -0.2 (0.2) | +0.1 (0.6) | -0.2 (1.4, 1.7) |
| 722 | hisp_share | log_estab | 271 | +0.0 (0.1) | -0.0 (0.3) | +1.1 (0.6, 0.6) |
| 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +0.2 (0.2) | +1.1 (0.4, 0.4) |
| 722 | mexborn_share | log_estab | 271 | -0.1 (0.2) | +0.0 (0.7) | +3.1 (1.6, 1.7) |
| 722 | mexborn_share | estab_poisson | 271 | +0.1 (0.1) | +0.4 (0.4) | +2.7 (1.0, 1.2) |
| 722 | arrests | log_estab | 102 | -0.2 (0.3) | +0.7 (0.6) | +1.0 (1.4, 1.6) |
| 722 | arrests | estab_poisson | 102 | +0.1 (0.1) | +0.3 (0.5) | -0.2 (0.8, 1.0) |
| 445110 | hisp_share | log_estab | 214 | -0.2 (0.1) | -0.1 (0.4) | -0.4 (1.1, 1.3) |
| 445110 | hisp_share | estab_poisson | 214 | -0.1 (0.1) | +0.0 (0.5) | -0.5 (0.9, 1.1) |
| 445110 | mexborn_share | log_estab | 214 | -0.5 (0.4) | -0.5 (1.2) | -1.4 (2.7, 3.3) |
| 445110 | mexborn_share | estab_poisson | 214 | -0.3 (0.4) | -0.4 (1.2) | -2.3 (2.4, 2.9) |
| 445110 | arrests | log_estab | 81 | -0.5 (0.4) | -0.5 (1.3) | +1.1 (2.6, 3.5) |
| 445110 | arrests | estab_poisson | 81 | -0.6 (0.3) | +0.4 (1.1) | +1.5 (2.5, 3.4) |


### A4c. City of LA ZIPs by 2010-2016 vending arrests, with and without downtown (added after seeing results)

Per log point of arrests. Downtown = ZCTAs 90012, 90013, 90014, 90015, 90017, 90021 (90071 is already out, under 1,000 residents). Implied = coefficient x sum over ZIPs of exposure x 2018 establishments: establishments against an arrest-free ZIP.

| NAICS | sample | outcome | ZIPs | estab 2018 | b2019 (SE) | b2022-23 | pre p | trend-adjusted dev2022-23 | implied estab 2019 (95%) | implied estab 2022-23 |
|---|---|---|---|---|---|---|---|---|---|---|
| 722511 | all City ZIPs | log_estab | 98 | 3344 | -0.7 (0.7) | +0.0 | 0.20 | -1.4 | -57 (-171 to +57) | +4 |
| 722511 | all City ZIPs | estab_poisson | 98 | 3344 | -0.3 (0.6) | -1.0 | 0.07 | -2.5 | -21 (-121 to +79) | -86 |
| 722511 | without downtown | log_estab | 92 | 3024 | -1.1 (0.6) | +0.5 | 0.24 | -1.3 | -72 (-147 to +4) | +34 |
| 722511 | without downtown | estab_poisson | 92 | 3024 | -0.5 (0.4) | -1.1 | 0.14 | -3.0 | -33 (-91 to +26) | -74 |
| 722513 | all City ZIPs | log_estab | 98 | 3299 | +0.2 (0.5) | -0.0 | 0.17 | +0.4 | +15 (-66 to +95) | -2 |
| 722513 | all City ZIPs | estab_poisson | 98 | 3299 | +0.0 (0.4) | -0.8 | 0.43 | -0.2 | +2 (-63 to +68) | -67 |
| 722513 | without downtown | log_estab | 92 | 3031 | +0.2 (0.6) | +1.1 | 0.01 | +1.6 | +18 (-66 to +101) | +80 |
| 722513 | without downtown | estab_poisson | 92 | 3031 | -0.0 (0.5) | +0.2 | 0.01 | +1.2 | -0 (-66 to +65) | +18 |
| 722 | all City ZIPs | log_estab | 102 | 8965 | +0.6 (0.4) | +0.1 | 0.68 | +1.0 | +135 (-58 to +328) | +32 |
| 722 | all City ZIPs | estab_poisson | 102 | 8965 | +0.1 (0.3) | -0.1 | 0.60 | -0.2 | +33 (-106 to +173) | -20 |
| 722 | without downtown | log_estab | 96 | 8132 | +0.5 (0.5) | +0.6 | 0.87 | +1.9 | +90 (-88 to +268) | +110 |
| 722 | without downtown | estab_poisson | 96 | 8132 | -0.1 (0.3) | +0.2 | 0.87 | +0.1 | -13 (-136 to +110) | +29 |
| 445110 | all City ZIPs | log_estab | 81 | 748 | -0.9 (0.9) | -1.0 | 0.27 | +1.1 | -18 (-53 to +17) | -21 |
| 445110 | all City ZIPs | estab_poisson | 81 | 748 | -0.1 (0.7) | -1.2 | 0.10 | +1.5 | -3 (-29 to +23) | -23 |
| 445110 | without downtown | log_estab | 78 | 725 | -1.1 (0.9) | -1.7 | 0.04 | +0.3 | -20 (-53 to +13) | -33 |
| 445110 | without downtown | estab_poisson | 78 | 725 | -0.2 (0.6) | -1.5 | 0.04 | +0.9 | -3 (-27 to +20) | -29 |


### A5. ZIP design in placebo counties (same specification)

| county | NAICS | exposure | outcome | ZIPs | b2019 (SE) | b2022-23 | b2012 | pre p |
|---|---|---|---|---|---|---|---|---|
| 06037 los angeles | 722511 | hisp_share | log_estab | 258 | +0.1 (0.3) | +1.4 | -1.6 | 0.05 |
| 06037 los angeles | 722511 | hisp_share | estab_poisson | 258 | +0.1 (0.2) | +0.8 | -1.8 | 0.00 |
| 06037 los angeles | 722511 | mexborn_share | log_estab | 258 | +0.5 (0.9) | +4.1 | -3.6 | 0.13 |
| 06037 los angeles | 722511 | mexborn_share | estab_poisson | 258 | -0.0 (0.7) | +2.1 | -4.9 | 0.00 |
| 06037 los angeles | 722513 | hisp_share | log_estab | 262 | +0.0 (0.2) | +0.5 | +0.8 | 0.11 |
| 06037 los angeles | 722513 | hisp_share | estab_poisson | 262 | +0.2 (0.2) | +0.7 | +0.6 | 0.02 |
| 06037 los angeles | 722513 | mexborn_share | log_estab | 262 | +0.4 (0.6) | +1.3 | +2.6 | 0.01 |
| 06037 los angeles | 722513 | mexborn_share | estab_poisson | 262 | +0.6 (0.5) | +1.4 | +2.0 | 0.00 |
| 06037 los angeles | 722 | hisp_share | log_estab | 271 | -0.1 (0.2) | +1.1 | -0.1 | 0.63 |
| 06037 los angeles | 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +1.1 | -0.3 | 0.02 |
| 06037 los angeles | 722 | mexborn_share | log_estab | 271 | +0.1 (0.4) | +2.9 | +0.1 | 0.76 |
| 06037 los angeles | 722 | mexborn_share | estab_poisson | 271 | +0.2 (0.3) | +2.8 | -0.6 | 0.22 |
| 06037 los angeles | 445110 | hisp_share | log_estab | 214 | -0.3 (0.3) | -1.1 | +1.3 | 0.03 |
| 06037 los angeles | 445110 | hisp_share | estab_poisson | 214 | -0.2 (0.3) | -1.2 | +1.2 | 0.02 |
| 06037 los angeles | 445110 | mexborn_share | log_estab | 214 | -0.8 (0.9) | -3.5 | +4.1 | 0.04 |
| 06037 los angeles | 445110 | mexborn_share | estab_poisson | 214 | -0.6 (0.9) | -3.7 | +2.9 | 0.05 |
| 48201 harris | 722511 | hisp_share | log_estab | 111 | -0.4 (0.5) | -1.2 | +2.9 | 0.25 |
| 48201 harris | 722511 | hisp_share | estab_poisson | 111 | -0.3 (0.4) | -0.4 | +1.7 | 0.37 |
| 48201 harris | 722511 | mexborn_share | log_estab | 111 | -1.1 (1.3) | -3.1 | +7.0 | 0.41 |
| 48201 harris | 722511 | mexborn_share | estab_poisson | 111 | -1.2 (1.1) | -1.2 | +4.9 | 0.44 |
| 48201 harris | 722513 | hisp_share | log_estab | 126 | -0.4 (0.3) | -0.1 | +1.5 | 0.19 |
| 48201 harris | 722513 | hisp_share | estab_poisson | 126 | -0.3 (0.3) | -0.3 | +1.3 | 0.20 |
| 48201 harris | 722513 | mexborn_share | log_estab | 126 | -1.3 (0.8) | -0.4 | +3.7 | 0.13 |
| 48201 harris | 722513 | mexborn_share | estab_poisson | 126 | -1.3 (0.8) | -1.2 | +3.3 | 0.23 |
| 48201 harris | 722 | hisp_share | log_estab | 126 | -0.2 (0.3) | -0.6 | +2.5 | 0.04 |
| 48201 harris | 722 | hisp_share | estab_poisson | 126 | -0.3 (0.3) | -0.5 | +1.7 | 0.03 |
| 48201 harris | 722 | mexborn_share | log_estab | 126 | -0.8 (0.7) | -1.8 | +6.2 | 0.04 |
| 48201 harris | 722 | mexborn_share | estab_poisson | 126 | -1.1 (0.7) | -1.7 | +4.6 | 0.05 |
| 48201 harris | 445110 | hisp_share | log_estab | 87 | +0.0 (0.6) | +1.3 | +0.5 | 0.03 |
| 48201 harris | 445110 | hisp_share | estab_poisson | 87 | +0.1 (0.5) | +0.9 | +1.5 | 0.04 |
| 48201 harris | 445110 | mexborn_share | log_estab | 87 | -0.2 (1.4) | +2.6 | +4.3 | 0.01 |
| 48201 harris | 445110 | mexborn_share | estab_poisson | 87 | +0.0 (1.3) | +1.9 | +4.9 | 0.02 |
| 48113 dallas | 722511 | hisp_share | log_estab | 68 | +0.8 (1.1) | +0.8 | +2.0 | 0.69 |
| 48113 dallas | 722511 | hisp_share | estab_poisson | 68 | +0.4 (0.5) | +0.6 | +1.1 | 0.71 |
| 48113 dallas | 722511 | mexborn_share | log_estab | 68 | +1.8 (2.6) | +1.8 | +6.1 | 0.31 |
| 48113 dallas | 722511 | mexborn_share | estab_poisson | 68 | +0.9 (1.1) | +0.8 | +3.8 | 0.25 |
| 48113 dallas | 722513 | hisp_share | log_estab | 77 | +0.1 (0.5) | -0.9 | -0.5 | 0.04 |
| 48113 dallas | 722513 | hisp_share | estab_poisson | 77 | +0.0 (0.4) | -0.3 | -0.5 | 0.18 |
| 48113 dallas | 722513 | mexborn_share | log_estab | 77 | -0.3 (1.1) | -2.9 | -1.3 | 0.37 |
| 48113 dallas | 722513 | mexborn_share | estab_poisson | 77 | -0.3 (0.8) | -1.5 | -1.7 | 0.41 |
| 48113 dallas | 722 | hisp_share | log_estab | 80 | -0.3 (0.5) | -1.0 | -1.0 | 0.00 |
| 48113 dallas | 722 | hisp_share | estab_poisson | 80 | -0.1 (0.3) | +0.2 | -0.1 | 0.42 |
| 48113 dallas | 722 | mexborn_share | log_estab | 80 | -1.0 (1.1) | -3.4 | -1.7 | 0.06 |
| 48113 dallas | 722 | mexborn_share | estab_poisson | 80 | -0.4 (0.6) | -0.9 | -0.1 | 0.85 |
| 48113 dallas | 445110 | hisp_share | log_estab | 54 | +1.6 (1.0) | +0.3 | +3.2 | 0.05 |
| 48113 dallas | 445110 | hisp_share | estab_poisson | 54 | +1.8 (0.8) | +0.9 | +3.0 | 0.02 |
| 48113 dallas | 445110 | mexborn_share | log_estab | 54 | +3.7 (2.4) | +1.0 | +12.2 | 0.06 |
| 48113 dallas | 445110 | mexborn_share | estab_poisson | 54 | +4.2 (2.0) | +2.3 | +10.1 | 0.02 |
| 48029 bexar | 722511 | hisp_share | log_estab | 56 | -0.4 (0.8) | -1.8 | +0.4 | 0.03 |
| 48029 bexar | 722511 | hisp_share | estab_poisson | 56 | -0.1 (0.8) | -0.7 | -0.1 | 0.00 |
| 48029 bexar | 722511 | mexborn_share | log_estab | 56 | -0.1 (3.3) | -7.9 | +4.0 | 0.13 |
| 48029 bexar | 722511 | mexborn_share | estab_poisson | 56 | -0.3 (3.3) | -6.9 | +0.3 | 0.01 |
| 48029 bexar | 722513 | hisp_share | log_estab | 56 | -0.3 (0.8) | -0.3 | +3.4 | 0.01 |
| 48029 bexar | 722513 | hisp_share | estab_poisson | 56 | +0.7 (0.4) | -0.2 | +2.2 | 0.01 |
| 48029 bexar | 722513 | mexborn_share | log_estab | 56 | -1.8 (2.6) | +0.4 | +11.8 | 0.03 |
| 48029 bexar | 722513 | mexborn_share | estab_poisson | 56 | +0.6 (1.9) | -0.6 | +9.1 | 0.02 |
| 48029 bexar | 722 | hisp_share | log_estab | 63 | -0.2 (0.6) | -2.1 | +3.5 | 0.00 |
| 48029 bexar | 722 | hisp_share | estab_poisson | 63 | +0.2 (0.4) | -0.3 | +1.8 | 0.02 |
| 48029 bexar | 722 | mexborn_share | log_estab | 63 | -1.4 (2.3) | -11.1 | +13.9 | 0.03 |
| 48029 bexar | 722 | mexborn_share | estab_poisson | 63 | -0.3 (1.6) | -3.5 | +9.1 | 0.10 |
| 04013 maricopa | 722511 | hisp_share | log_estab | 110 | -0.5 (0.6) | -0.6 | -1.8 | 0.24 |
| 04013 maricopa | 722511 | hisp_share | estab_poisson | 110 | -0.4 (0.6) | -0.6 | -0.1 | 0.68 |
| 04013 maricopa | 722511 | mexborn_share | log_estab | 110 | -1.2 (1.6) | -3.0 | -2.0 | 0.46 |
| 04013 maricopa | 722511 | mexborn_share | estab_poisson | 110 | -1.2 (1.6) | -3.6 | +1.9 | 0.63 |
| 04013 maricopa | 722513 | hisp_share | log_estab | 110 | +0.5 (0.4) | -0.1 | +0.7 | 0.05 |
| 04013 maricopa | 722513 | hisp_share | estab_poisson | 110 | +0.7 (0.3) | +0.4 | +0.9 | 0.13 |
| 04013 maricopa | 722513 | mexborn_share | log_estab | 110 | +1.5 (1.0) | -0.7 | +3.1 | 0.01 |
| 04013 maricopa | 722513 | mexborn_share | estab_poisson | 110 | +1.9 (0.9) | -0.3 | +2.4 | 0.07 |
| 04013 maricopa | 722 | hisp_share | log_estab | 119 | +0.4 (0.3) | +0.7 | +0.2 | 0.85 |
| 04013 maricopa | 722 | hisp_share | estab_poisson | 119 | +0.1 (0.3) | +0.6 | +0.7 | 0.13 |
| 04013 maricopa | 722 | mexborn_share | log_estab | 119 | +0.9 (0.9) | +0.1 | +1.6 | 0.68 |
| 04013 maricopa | 722 | mexborn_share | estab_poisson | 119 | +0.2 (0.7) | -0.5 | +2.5 | 0.05 |
| 04013 maricopa | 445110 | hisp_share | log_estab | 66 | +0.4 (0.8) | -1.0 | +2.4 | 0.12 |
| 04013 maricopa | 445110 | hisp_share | estab_poisson | 66 | +0.3 (0.8) | -1.0 | +2.6 | 0.35 |
| 04013 maricopa | 445110 | mexborn_share | log_estab | 66 | +0.7 (2.2) | -2.5 | +7.6 | 0.11 |
| 04013 maricopa | 445110 | mexborn_share | estab_poisson | 66 | +0.1 (2.2) | -2.8 | +7.9 | 0.37 |
| 17031 cook | 722511 | hisp_share | log_estab | 140 | +0.0 (0.4) | +2.1 | -0.7 | 0.28 |
| 17031 cook | 722511 | hisp_share | estab_poisson | 140 | +0.4 (0.4) | +2.4 | -1.6 | 0.16 |
| 17031 cook | 722511 | mexborn_share | log_estab | 140 | +0.0 (1.1) | +5.2 | -2.0 | 0.60 |
| 17031 cook | 722511 | mexborn_share | estab_poisson | 140 | +0.7 (0.9) | +6.1 | -3.1 | 0.36 |
| 17031 cook | 722513 | hisp_share | log_estab | 150 | -0.1 (0.5) | +0.3 | -0.2 | 0.56 |
| 17031 cook | 722513 | hisp_share | estab_poisson | 150 | +0.2 (0.4) | +0.1 | +0.6 | 0.76 |
| 17031 cook | 722513 | mexborn_share | log_estab | 150 | -0.2 (1.4) | +1.1 | -0.5 | 0.45 |
| 17031 cook | 722513 | mexborn_share | estab_poisson | 150 | +0.8 (1.1) | +0.2 | +1.4 | 0.45 |
| 17031 cook | 722 | hisp_share | log_estab | 157 | +0.1 (0.4) | +1.7 | -0.6 | 0.29 |
| 17031 cook | 722 | hisp_share | estab_poisson | 157 | +0.3 (0.3) | +1.4 | -0.9 | 0.28 |
| 17031 cook | 722 | mexborn_share | log_estab | 157 | +0.3 (1.0) | +4.8 | -1.4 | 0.49 |
| 17031 cook | 722 | mexborn_share | estab_poisson | 157 | +0.7 (0.6) | +3.6 | -1.4 | 0.45 |
| 17031 cook | 445110 | hisp_share | log_estab | 111 | +0.2 (0.4) | +0.4 | -0.6 | 0.70 |
| 17031 cook | 445110 | hisp_share | estab_poisson | 111 | +0.5 (0.4) | +0.6 | -0.4 | 0.54 |
| 17031 cook | 445110 | mexborn_share | log_estab | 111 | +0.3 (1.0) | +0.1 | -3.3 | 0.72 |
| 17031 cook | 445110 | mexborn_share | estab_poisson | 111 | +0.9 (0.9) | +0.7 | -2.2 | 0.32 |
| 12086 miamidade | 722511 | hisp_share | log_estab | 66 | -1.2 (0.7) | -2.1 | +0.5 | 0.40 |
| 12086 miamidade | 722511 | hisp_share | estab_poisson | 66 | -1.0 (0.7) | -2.1 | +1.1 | 0.56 |
| 12086 miamidade | 722511 | mexborn_share | log_estab | 66 | -4.9 (12.1) | +6.2 | -6.3 | 0.02 |
| 12086 miamidade | 722511 | mexborn_share | estab_poisson | 66 | -0.5 (9.9) | +1.9 | -5.1 | 0.15 |
| 12086 miamidade | 722513 | hisp_share | log_estab | 68 | +0.2 (0.5) | -1.7 | -0.8 | 0.69 |
| 12086 miamidade | 722513 | hisp_share | estab_poisson | 68 | +0.1 (0.5) | -2.2 | -1.0 | 0.59 |
| 12086 miamidade | 722513 | mexborn_share | log_estab | 68 | -6.2 (6.1) | -9.1 | -19.2 | 0.00 |
| 12086 miamidade | 722513 | mexborn_share | estab_poisson | 68 | -1.8 (5.2) | -3.9 | -14.5 | 0.00 |
| 12086 miamidade | 722 | hisp_share | log_estab | 71 | -0.2 (0.4) | -1.7 | -0.8 | 0.68 |
| 12086 miamidade | 722 | hisp_share | estab_poisson | 71 | -0.5 (0.4) | -2.2 | -0.5 | 0.91 |
| 12086 miamidade | 722 | mexborn_share | log_estab | 71 | +4.1 (3.4) | +5.4 | -2.3 | 0.95 |
| 12086 miamidade | 722 | mexborn_share | estab_poisson | 71 | +2.8 (3.8) | +4.5 | -2.3 | 0.01 |
| 12086 miamidade | 445110 | hisp_share | log_estab | 62 | -0.4 (0.7) | +0.6 | -1.4 | 0.14 |
| 12086 miamidade | 445110 | hisp_share | estab_poisson | 62 | +0.2 (0.6) | +0.7 | -0.6 | 0.12 |
| 12086 miamidade | 445110 | mexborn_share | log_estab | 62 | -1.1 (4.1) | -0.4 | -44.2 | 0.00 |
| 12086 miamidade | 445110 | mexborn_share | estab_poisson | 62 | +1.7 (3.2) | -1.0 | -18.1 | 0.00 |


### A6. Taxable sales (CDTFA), every specification

Per 10 points of the share. l_c08 food services and drinking places; l_c04 food and beverage stores (placebo); l_diff their difference; l_permits C08 seller's permits (cities: outlets) in Q4.

| level | exposure | outcome | weight | units | b2019 (SE) | b2020-21 | b2022-23 | b2024-25 | pre p |
|---|---|---|---|---|---|---|---|---|---|
| county | hisp_share | l_c08 | none | 56 | +0.1 (0.1) | +2.7 | +2.6 | +3.0 | 0.04 |
| county | hisp_share | l_c08 | pop | 56 | +0.1 (0.1) | +4.1 | +2.5 | +2.2 | 0.08 |
| county | hisp_share | l_c04 | none | 56 | +0.1 (0.3) | -0.0 | +0.6 | +0.9 | 0.00 |
| county | hisp_share | l_c04 | pop | 56 | +0.5 (0.2) | +1.8 | +3.1 | +3.1 | 0.25 |
| county | hisp_share | l_diff | none | 56 | -0.0 (0.3) | +2.7 | +2.0 | +2.1 | 0.00 |
| county | hisp_share | l_diff | pop | 56 | -0.3 (0.3) | +2.4 | -0.6 | -0.9 | 0.03 |
| county | hisp_share | l_permits | none | 56 | +0.2 (0.3) | +0.7 | +1.9 | +2.8 | 0.12 |
| county | hisp_share | l_permits | pop | 56 | +0.6 (0.3) | +1.5 | +2.5 | +3.8 | 0.27 |
| county | mexborn_share | l_c08 | none | 56 | +0.7 (0.5) | +6.2 | +6.3 | +7.4 | 0.06 |
| county | mexborn_share | l_c08 | pop | 56 | +0.2 (0.4) | +11.6 | +7.6 | +6.8 | 0.52 |
| county | mexborn_share | l_c04 | none | 56 | +0.5 (1.0) | +0.3 | +1.6 | +2.7 | 0.00 |
| county | mexborn_share | l_c04 | pop | 56 | +1.4 (0.8) | +5.1 | +9.1 | +9.3 | 0.25 |
| county | mexborn_share | l_diff | none | 56 | +0.3 (1.1) | +6.0 | +4.7 | +4.7 | 0.00 |
| county | mexborn_share | l_diff | pop | 56 | -1.2 (0.9) | +6.4 | -1.5 | -2.5 | 0.10 |
| county | mexborn_share | l_permits | none | 56 | +0.1 (0.8) | +1.2 | +3.8 | +5.7 | 0.06 |
| county | mexborn_share | l_permits | pop | 56 | +1.0 (0.9) | +3.4 | +6.2 | +9.0 | 0.20 |
| city | hisp_share | l_c08 | none | 80 | +0.2 (0.2) | +2.8 | +0.5 | +0.8 | 0.36 |
| city | hisp_share | l_c08 | pop | 80 | +0.3 (0.2) | +3.4 | +1.2 | +1.3 | 0.15 |
| city | hisp_share | l_c04 | none | 80 | -0.5 (0.2) | -0.2 | +0.3 | +0.9 | 0.29 |
| city | hisp_share | l_c04 | pop | 80 | -0.2 (0.1) | +0.1 | +0.5 | +0.8 | 0.10 |
| city | hisp_share | l_diff | none | 80 | +0.7 (0.3) | +3.0 | +0.3 | -0.1 | 0.10 |
| city | hisp_share | l_diff | pop | 80 | +0.5 (0.2) | +3.3 | +0.7 | +0.6 | 0.00 |
| city | hisp_share | l_permits | none | 80 | +0.2 (0.2) | +0.8 | +1.4 | +1.5 | 0.10 |
| city | hisp_share | l_permits | pop | 80 | +0.1 (0.2) | +0.7 | +1.1 | +1.1 | 0.00 |
| city | mexborn_share | l_c08 | none | 80 | +0.6 (0.4) | +7.4 | +1.5 | +2.0 | 0.17 |
| city | mexborn_share | l_c08 | pop | 80 | +0.7 (0.4) | +7.5 | +2.4 | +2.9 | 0.08 |
| city | mexborn_share | l_c04 | none | 80 | -0.6 (0.4) | -0.5 | +0.1 | +1.8 | 0.71 |
| city | mexborn_share | l_c04 | pop | 80 | -0.3 (0.4) | -0.4 | +0.4 | +1.1 | 0.17 |
| city | mexborn_share | l_diff | none | 80 | +1.2 (0.6) | +7.9 | +1.4 | +0.2 | 0.17 |
| city | mexborn_share | l_diff | pop | 80 | +1.1 (0.6) | +7.9 | +2.0 | +1.8 | 0.00 |
| city | mexborn_share | l_permits | none | 80 | +0.6 (0.4) | +2.1 | +3.9 | +4.0 | 0.09 |
| city | mexborn_share | l_permits | pop | 80 | +0.6 (0.5) | +2.0 | +3.0 | +2.6 | 0.01 |

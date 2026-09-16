**Verdict:** Essentially the entire 2009→2021 rise in Hispanic violent-offence state prisoners is (a) a change in how BJS estimates Hispanic origin, not behaviour. BJS published two estimates for the *same reference date* — 31 December 2009 — on two bases: 117,800 Hispanic violent prisoners (Prisoners in 2010, App. Table 16b, p.28) and 159,800 (Prisoners in 2011, App. Table 16, p.29). That restatement alone is +42,000, against a memo-reported 2009→2021 rise of +42,300. On a consistent basis the Hispanic violent stock went 159,800 → 160,100, i.e. **+0.2% in count and −22.5% per capita**, versus white −23.8% and −20.6%. Splitting the +42,300: **coding ≈ +42,000 (99%)**, age ≈ 0 (ageing *lowered* the Hispanic male imprisonment rate 6.1%), stock-flow ≈ 0 for the count (it explains the violent *share* rise, 55.8%→71.6%, in full), real behavioural change **negative, not positive**. Texas, which codes Hispanic ethnicity directly and applies no survey adjustment, shows the Hispanic imprisonment rate falling 39.0% against white 17.7% over the same span.

Model self-report: claude-opus-5[1m]

[UNVERIFIED] where marked; all BJS counts below were read from the PDFs this session (`pdf/`, `txt/`) and the two anchor values verified.

## Verification of anchors

| Check | Required | Found | Source |
|---|---|---|---|
| 2009 Hispanic violent | 117,800 | 117,800 | p10 App. Table 16b, p.28 |
| 2009 NH white violent | 265,600 | 265,600 | p10 App. Table 16b, p.28 |
| 2021 Hispanic violent | 160,100 | 160,100 | p22st Table 17, p.29 |
| 2021 NH white violent | 176,400 | 176,400 | p22st Table 17, p.29 |
| TDCJ FY2009 on-hand total | printed total | 155,076 (Black 57,127 / White 47,971 / Hispanic 49,197 / Other 781) | TDCJ Statistical Report FY2009, Demographic Highlights p.6 |
| TDCJ FY2021 on-hand total | printed total | 117,876 (38,547 / 39,735 / 38,914 / 680) | TDCJ Statistical Report FY2021, Demographic Highlights p.6 |

PASS on all six.

## 1. Year-by-year series (sentenced prisoners under **state** jurisdiction)

`national_series.csv` / `national_series.py`. Per-100k uses Census Vintage resident population (NH white alone; Hispanic any race).

| Ref. year | Report (table) | Estimation basis | White total | Hisp. total | White violent | Hisp. violent | W/100k | H/100k | Hisp. violent share |
|---|---|---|---|---|---|---|---|---|---|
| 2008 | p10 App.T16a | NIS 2008–09 / pre-2010 | 532,000 | 209,000 | 264,200 | 113,400 | 132.1 | 241.3 | 54.3% |
| **2009** | **p10 App.T16b** | **NIS 2008–09 / pre-2010** | **532,000** | **212,100** | **265,600** | **117,800** | **132.9** | **243.4** | **55.5%** |
| 2008 | p11 App.T15 *(restated)* | SISCF 2004 ratio | 469,076 | 280,716 | 232,700 | 152,700 | 116.3 | 324.9 | 54.4% |
| **2009** | **p11 App.T16 *(restated)*** | **SISCF 2004 ratio** | **467,290** | **287,568** | **231,500** | **159,800** | **115.8** | **330.2** | **55.6%** |
| 2010 | p11 T9 | SISCF 2004 ratio | 468,528 | 289,429 | 231,800 | 164,200 | 117.8 | 325.1 | 56.7% |
| 2011 | — | *no offence × ethnicity table published* | | | | | | | |
| 2012 | p13 T14 | SISCF 2004 ratio | 462,600 | 271,700 | 228,100 | 162,900 | 115.7 | 307.9 | 60.0% |
| 2013 | p14 App.T4 | SISCF 2004 ratio | 468,600 | 274,200 | 223,900 | 162,300 | 113.5 | 302.2 | 59.2% |
| 2014 | p15 App.T5 | SISCF 2004 ratio | 451,100 | 261,000 | 210,400 | 152,900 | 106.7 | 280.6 | 58.6% |
| 2015 | p16 T13 | SISCF 2004 ratio | 403,600 | 278,600 | 190,100 | 167,700 | 96.3 | 303.3 | 60.2% |
| 2016 | p17 T13 | SPI 2016 ratio | 401,100 | 278,400 | 190,900 | 168,100 | 96.7 | 297.5 | 60.4% |
| 2017 | p18 T14 | SPI 2016 ratio | 394,800 | 274,300 | 188,700 | 166,800 | 95.6 | 290.6 | 60.8% |
| 2018 | p19 T14 | SPI 2016 ratio | 394,800 | 274,300 | 190,800 | 168,900 | 96.9 | 288.7 | 61.6% |
| 2019 | p20st T17 | SPI 2016 ratio | 386,700 | 266,500 | 192,600 | 176,000 | 97.9 | 296.3 | 66.0% |
| 2020 | p21st T17 | SPI 2016 ratio | 327,300 | 226,800 | 178,600 | **179,500** | 93.2 | 290.5 | 79.1% |
| **2021** | **p22st T17** | **SPI 2016 ratio** | **321,700** | **224,300** | **176,400** | **160,100** | **92.0** | **255.8** | **71.4%** |

Three comparisons off that table:

| | Hisp. violent | White violent | Hisp. per 100k | White per 100k |
|---|---|---|---|---|
| A. Memo (2009 old basis → 2021) | 117,800 → 160,100 **+35.9%** | −33.6% | 243.4 → 255.8 **+5.1%** | −30.8% |
| B. Consistent basis (2009 restated → 2021) | 159,800 → 160,100 **+0.2%** | −23.8% | 330.2 → 255.8 **−22.5%** | −20.6% |
| C. Pure method effect (same date, 31 Dec 2009) | 117,800 → 159,800 **+35.7%** | −12.8% | — | — |

C reproduces A to within 0.2 percentage points. The rise is the restatement.

**Where the basis changed, and whether the count steps.** Two discontinuities, both at the estimation basis and not at any behavioural boundary. (i) Between *Prisoners in 2010* and *Prisoners in 2011*, BJS moved from a National Inmate Survey 2008–09 adjustment to a 2004 Survey of Inmates in State Correctional Facilities ratio and restated 2008–2010; the Hispanic violent count steps +35–37% and the white count steps −12–13% at every restated year. BJS flags it in p10's own footnotes: *"Data source used to estimate race and Hispanic origin changed in 2010. Use caution when comparing to prior years."* (ii) From *Prisoners in 2017* (2016 data) BJS switched to the 2016 Survey of Prison Inmates; that transition is smooth (2015→2016: white 190,100→190,900, Hispanic 167,700→168,100), because by then BJS was blending the two survey ratios with time-varying weights rather than switching outright (p22st Methodology, p.43).

**Mechanism, quantified by BJS itself.** *Prisoners in 2016*, Table 5 (p.6), compares the administrative NPS distribution with SPI self-report for the same male state-prison population: Hispanic 16.6% administrative versus 21.1% self-reported; white 39.0% versus 30.6%. Administrative prison records under-record Hispanic origin by about a quarter in relative terms and absorb the difference into "white". The whole BJS adjustment exists to correct that, and the size of the correction is the size of the apparent "rise". Appendix table 1 of p22st shows the raw material: Alabama reports 0 Hispanic prisoners out of 26,421; Georgia reports 1,994 out of 48,439.

## 2. Offence composition over time

The Hispanic violent count does **not** rise smoothly. On the memo's mixed-basis comparison it appears to jump +38% between 2009 and 2012; on a consistent basis it is flat across the entire series (159,800 in 2009, 162,900 in 2012, 167,700 in 2015, 168,900 in 2018, 160,100 in 2021) while the Hispanic population grew about 29%. The sub-offence "rises" in the memo behave the same way: Hispanic rape/other-sexual-assault is 22,000 on the 2009 old basis but 33,500 on the restated 2009 basis, against 42,800 in 2021, so roughly three-quarters of the reported +95% is restatement.

## 3. State systems with stable Hispanic coding

**Texas — PASS, and it contradicts the national picture.** TDCJ has coded Hispanic ethnicity as a separate category for decades and applies no survey adjustment.

| TDCJ on-hand (prison + state jail + SAFP) | Total | NH white | Hispanic | Hisp. share | White/100k | Hisp./100k | H/W | Violent share |
|---|---|---|---|---|---|---|---|---|
| 31 Aug 2009 | 155,076 | 47,971 | 49,197 | 31.7% | 415.5 | 537.7 | 1.29 | 50.8% |
| 31 Aug 2021 | 117,876 | 39,735 | 38,914 | 33.0% | 341.7 | 328.2 | 0.96 | 62.7% |
| change | −24.0% | | | +4.1% rel. | **−17.7%** | **−39.0%** | | |

Texas Hispanic imprisonment per capita fell more than twice as fast as white, and the Texas Hispanic *share* of prisoners moved +4.1% relative. The BJS national Hispanic share moved +41.5% relative on the memo's basis and **+4.4% on the consistent basis** — matching Texas almost exactly. Populations: ACS 1-year B03002, state 48 (2009: NH white 11,546,095, Hispanic 9,149,688; 2021: 11,627,221 and 11,857,387).

Caveat: TDCJ publishes race and offence as separate marginals in the Demographic Highlights table and no race × offence cross-tab, so the Texas figures are all-offence, not violent-specific. The all-offence result is still decisive against a coding-neutral reading, because the violent share rose for the Texas population as a whole (50.8% → 62.7%) without any ethnicity recoding.

**California — BLOCKED.** CDCR "Offender Data Points" exists only for 2016–2019 (`cdcr.ca.gov/research/offender-outcomes-characteristics/offender-data-points/`); there is no 2009 or 2021 edition, the CDCR prison-census archive returns 404, and the Internet Archive was serving `429 Too Many Requests` and then a "Temporarily Offline" page during this run. No CA ethnicity × offence figures were obtained for either year. This is the one step in the brief not completed.

## 4. Age

Direct standardisation, `age_standardise.py`. Rates: BJS p10 App. Table 15 (p.27, 2010) and p22st Table 13 (p.24, 2022), male, state + federal, sentence over 1 year. Populations: ACS 1-year PUMS via the Census API `tabulate` endpoint, PWGTP-weighted males by band (cached in `pop_cache/`).

| Hispanic males 18+ | per 100,000 |
|---|---|
| 2010 actual (2010 rates, 2010 age structure) | 1,906.3 |
| 2022 counterfactual (2010 rates, 2022 age structure) | 1,790.3 |
| 2022 actual | 1,129.8 |
| total change | −776.5 (−40.7%) |
| attributable to age structure | **−116.0 (−6.1%)** |
| attributable to age-specific rates | −660.5 |

Ageing pushed the Hispanic male imprisonment rate **down** 6.1%, accounting for 14.9% of the observed all-age decline. The Hispanic male population did age, but it aged past the 30–34 peak into bands where rates are lower. The same calculation for non-Hispanic white men gives an age effect of −39.2 per 100k, or −6.8%, so age structure explains none of the Hispanic/white divergence. The age effect is computed with 2010 rates held fixed in both terms, so it depends only on the two population distributions and is not sensitive to the estimation-basis problem in §1.

Two limits. BJS publishes no age × offence × ethnicity table, so this is all-offence, not violent-specific; ageing does push the violent *share* up, because violent prisoners are concentrated in older bands. And the 2010 rate table sits on the NIS 2008–09 basis while 2022 sits on the blended SPI basis, so the *levels* carry basis noise even though the age effect does not.

## 5. Stock–flow

No NCRP admissions-by-offence-by-ethnicity series was found for 2009–2021. The usable flow source is *Prisoners in 2012: Trends in Admissions and Releases, 1991–2012* (p12tar9112), new court commitments to state prison by race, Hispanic origin and most serious offence:

| | 2001 | 2006 | 2011 |
|---|---|---|---|
| Hispanic violent new court commitments | 21,821 | 24,882 | 24,893 |
| NH white violent new court commitments | 36,963 | 38,738 | 36,952 |

Hispanic violent admissions were flat in count from 2006 while the Hispanic population grew about 26% over the decade, so per-capita violent admissions fell roughly a fifth; white per-capita admissions were flat. Behaviourally the flow converged downward.

Mean time served, initial releases, BJS *Time Served in State Prison, 2016* (tssp16, Table 1): violent 4.7 years overall, murder 15.0, rape/sexual assault 6.2, robbery 4.7, assault 2.5; property 1.8, drug 1.8, public order 1.7. Stock is roughly admissions × mean time served, and the stock over-weights long sentences by the ratio of their duration to the mean, so the 2021 violent stock reflects admissions centred around 2012–2014 while the non-violent stock tracks current-year admissions almost one for one.

That is why the violent *share* rose without any behavioural change. Hispanic state-prison stock on the consistent basis:

| | 2009 (p11) | 2021 (p22st) | change |
|---|---|---|---|
| violent | 159,800 | 160,100 | +0.2% |
| property | 43,100 | 19,000 | −55.9% |
| drug | 49,400 | 22,600 | −54.3% |
| public order | 34,000 | 21,900 | −35.6% |
| non-violent total | 126,500 | 63,500 | −49.8% |
| violent share | 55.8% | 71.6% | |

Had the violent stock drained at the non-violent rate it would be 80,216 rather than 160,100. The 79,884 difference is the stock-flow lag, and it is the whole of the violent-share rise. The 2020 column makes the mechanism visible: COVID court closures cut total stock from 1,221,288 to 1,043,705 in one year while the violent stock barely moved, pushing the Hispanic violent share to 79.1% before it fell back to 71.4%.

## Caveats

- p11's restatement is BJS's own estimate, not ground truth. The claim here is not that 159,800 is correct but that 117,800 and 160,100 are not comparable, and that the modern series is continuous with 159,800.
- BJS now blends the SISCF 2004 and SPI 2016 ratios with weights that vary by distance in years from each survey (p22st Methodology, p.43), so the adjustment drifts continuously through the series rather than stepping once. Year-to-year Hispanic counts carry method noise of unknown size.
- The 2020 estimates are visibly unstable: Hispanic aggravated/simple assault is 53,000 (2019), 65,300 (2020), 47,100 (2021), and Hispanic violent exceeds white violent only in 2020.
- p18 (2017) and p19 (2018) print identical race totals, 394,800 white and 274,300 Hispanic, for different reference years. The percentage tables are internally consistent with those totals, so this is BJS reusing a distribution, not a transcription error here. [UNVERIFIED as to BJS intent]
- 2011 has no published offence × ethnicity table.
- California was not obtained (§3).
- Resident populations for the per-100k columns are rounded Census Vintage figures carried over from the prior session's script for comparability; they are not the January-1 bases BJS itself uses, so the per-capita levels differ slightly from BJS's published imprisonment rates.

## Files

All under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/hisp_violent_stock_2026_09_16/`:

- `RESULT.md` — this file
- `national_series.py`, `national_series.csv` — year-by-year BJS series, transcriptions with report and page provenance
- `age_standardise.py`, `pop_cache/` — direct standardisation, ACS PUMS population cache
- `state_and_flow.py` — Texas per-capita check and stock-flow model
- `pdf/` — BJS *Prisoners in* p09–p22st, plus tssp16 (Time Served in State Prison, 2016)
- `txt/` — `pdftotext -layout` extractions of the above
- `state/` — TDCJ Statistical Reports FY2009, FY2010, FY2021 (PDF + text); the FY2022 download was truncated and is unusable

# Pueyo thread reproduction — Spain, Italy, UK, Eurostat

**Verdict:** Four of five charts reproduce from primary sources; the fifth (London) reproduces
arithmetically but rests on a denominator the chart caption misdescribes.

| # | Chart | Verdict | Largest discrepancy | The caveat that matters most |
|---|---|---|---|---|
| 1 | Spain, population share by origin (INE) | **Reproduced** | mean 0.006 pp over 20 countries | It is the Padrón at **1 Jan 2022**, not a current figure. Spain's foreign population grew ~21% by 2025. |
| 2 | Spain, prison share and ratio (Instituciones Penitenciarias) | **Reproduced** | Albania 24.9x chart vs 22.8x (2022 denominator) or 19.6x (2024) | The left panel is the share of **foreign** prisoners, not of the total prison population, and the whole table excludes Catalonia. |
| 3 | Italy, violent crime by citizenship (ISTAT) | **Partly reproduced** | Algeria 17.1x chart vs 13.5x recomputed | Correcting for irregular residents moves every ratio **down** ~8-11%, the opposite of what "adjusted for est. irregular pop." implies. |
| 4 | London, sex-offence prosecutions (Met FOI) | **Reproduced arithmetically, denominator misdescribed** | Afghanistan 74.2 vs 18.7 per 10,000 on census denominators | Denominators are the 2021 **Annual Population Survey**, not the census, and are rounded to the nearest 1,000 at values where the survey is unreliable. |
| 5 | Eurostat, sexual assault index 2014=100 | **Reproduced** | Ireland 165.3 chart vs 143.8 recomputed (+15%) | England and Wales has **no Eurostat data after 2018**; that line stops mid-chart. |

[UNVERIFIED] — figures below are recomputed from the sources named; chart values are read off the
published images by pixel measurement and carry roughly ±2% reading error.

---

## 1. Spain — share of total population by country of origin

Source identified: INE **Estadística del Padrón Continuo**, table 03005 ("Población extranjera por
Nacionalidad, provincias, Sexo y Año"), stock at **1 January 2022**, by nationality, divided by the
INE ECP resident population at the same date (47,486,727).

| Country | Chart % | Padrón 1 Jan 2022 | Recomputed % |
|---|---|---|---|
| Morocco | 1.83 | 883,243 | 1.86 |
| Romania | 1.31 | 627,478 | 1.32 |
| Colombia | 0.66 | 314,679 | 0.66 |
| United Kingdom | 0.61 | 293,171 | 0.62 |
| Italy | 0.56 | 275,654 | 0.58 |
| China | 0.47 | 223,999 | 0.47 |
| Venezuela | 0.44 | 212,064 | 0.45 |
| Ecuador | 0.25 | 119,885 | 0.25 |
| Senegal | 0.18 | 83,260 | 0.18 |

Mean absolute gap 0.006 pp, maximum 0.03 pp, across all 20 countries. This is an exact
reproduction. Full table in `spain/spain_population_share_padron2022.csv`.

The caveat is vintage. On current INE data (1 Jan 2025, `spain/spain_population_share_by_origin.csv`)
the Latin American shares are far higher: Colombia 1.38% by nationality and 1.99% by country of
birth, against 0.66% on the chart. Spanish naturalisation after two years' residence pulls the
nationality series down and the birthplace series up, so "country of origin" is doing real work here.

## 2. Spain — prison population by nationality

Source: **Informe General 2024**, Secretaría General de Instituciones Penitenciarias
(`spain/Informe-General_2024_firecrawl_norm.txt`, text extracted from the ministry PDF via Firecrawl;
direct download is blocked by Cloudflare, HTTP 403). The ten nationalities on the chart are exactly
the top ten of **Tabla 49** (mean monthly stock of foreign prisoners, 2024).

Administrative scope: these are **Administración General del Estado** figures, which exclude
Catalonia, since Catalonia runs its own prison service. Denominators are all-Spain, so every rate
below is biased low, and unevenly so, because Catalonia hosts a large share of Spain's Moroccan,
Pakistani and Romanian residents.

Key totals from Tablas 4 and 44 (means for 2024, AGE):

| | Spanish nationals | Foreigners |
|---|---|---|
| Prisoners | 34,630 | 13,850 |
| of which pre-trial (preventivos) | 4,138 | 4,035 |
| Pre-trial share | 11.9% | **29.1%** |

Foreign nationals are **2.44x** more likely than Spaniards to be held pre-trial rather than under
sentence. At year-end 2024 foreigners were 29.3% of all prisoners against 13.7% of the population.

**Rates on current denominators** (Eurostat `migr_pop1ctz` for Spain, mean of 1 Jan 2024 and 2025,
which mirrors INE). Average foreigner 206.5 per 100,000; Spanish national 82.1 per 100,000, so the
average foreigner is **2.51x** the Spaniard.

| Country | Prisoners | Population | Per 100k | x avg foreigner | x Spaniard | Chart |
|---|---|---|---|---|---|---|
| Algeria | 974 | 82,175 | 1,185 | 5.74 | 14.4 | 6.8 |
| Dominican Rep. | 386 | 65,286 | 591 | 2.86 | 7.2 | 3.4 |
| Morocco | 3,792 | 944,846 | 401 | 1.94 | 4.9 | 2.3 |
| Ecuador | 440 | 128,561 | 342 | 1.66 | 4.2 | 1.6 |
| Senegal | 309 | 95,320 | 324 | 1.57 | 4.0 | 1.7 |
| Brazil | 262 | 103,884 | 252 | 1.22 | 3.1 | 1.3 |
| Colombia | 1,480 | 627,506 | 236 | 1.14 | 2.9 | 1.2 |
| Romania | 1,136 | 614,866 | 185 | 0.89 | 2.3 | 1.0 |
| Peru | 346 | 240,094 | 144 | 0.70 | 1.8 | 1.0 |

Ordering matches the chart exactly. Ecuador, Senegal, Brazil, Colombia and Romania match within 0.1x.
Algeria, the Dominican Republic and Morocco come out 15-20% below the chart, which is what using a
2022 rather than a 2024 denominator would do. The 2022-denominator variant is in
`spain/spain_prison_ratios_padron2022.csv`.

**Albania, the 25x claim.** Neither INE's Estadística Continua de Población nor Eurostat publishes
Albania separately for Spain; the last primary figure is the Padrón at 1 Jan 2022.

| Denominator | Value | Per 100k | x avg foreigner | x Spaniard |
|---|---|---|---|---|
| Padrón 1 Jan 2022 (INE 03005) | 5,022 | 5,695 | 27.6 | 69 |
| Extrapolated to 1 Jan 2024 at the 2019-22 growth rate of 18.6%/yr | 7,065 | 4,048 | 19.6 | 49 |

The chart's 24.9x (measured) sits inside that band, so the claim survives, but it is a denominator
artefact as much as a crime fact: 286 prisoners divided by a resident community of five to seven
thousand. The Albanian resident count grew from 2,549 in 2018 to 5,022 in 2022, so the denominator is
both tiny and moving fast, and anyone in Spain for trafficking who never registered on the padrón is
in the numerator but not the denominator.

The report gives no offence breakdown by nationality, so the transit-trafficking explanation cannot
be tested against it. What the report does show (Tabla 48) is that drug and public-health offences
account for 13.71% of charges against foreign prisoners in 2024, **down** from 15.63% in 2021, while
property offences rose to 32.30% from 30.52% and sexual offences held at 3.20%.
Pre-trial status is not published by nationality either, so the 29.1% foreign pre-trial share cannot
be attributed to Albanians specifically. [INFERENCE] The chart's left panel reads about 30% for
Morocco against 27.4% in Tabla 49; including Catalonia, which the report excludes, would raise
Morocco's share, which is the likeliest explanation.

## 3. Italy — violent crime rate by citizenship

Sources: ISTAT SDMX dataflow `IT1,73_230_DF_DCCV_AUTVITTPS_2` (alleged offenders reported by the
police to the judicial authority, foreigners by country of citizenship) and `..._1` (by Italian /
foreign citizenship, summed over sex and age), year 2023. Denominators: ISTAT
`29_317_DF_DCIS_POPSTRCIT1_1` resident foreigners by citizenship, mean of 1 Jan 2023 and 2024;
Italian citizens from Eurostat `migr_pop1ctz`.

"Violent crime" is not a published ISTAT aggregate at country level, so I used the 13 offence codes
that exist in both files with no parent/child double counting: intentional, attempted and infant
homicide, manslaughter, blows, culpable injuries, menaces, stalking, kidnapping, sexual violence,
sexual activity with a minor, robbery, extortion. ISTAT's own four-code "violent crimes" grouping
(blows, intentional homicide, sexual violence, stalking) omits stalking at country level, so it
cannot be used for this comparison.

Baseline: Italian citizens 203.9 per 100,000; all foreigners 1,003.7 per 100,000, a ratio of 4.92x.

| Country | Population | Offenders | Per 100k | x Italians | x Italians, ISMU-adjusted | Pallesen chart |
|---|---|---|---|---|---|---|
| Tunisia | 106,408 | 3,960 | 3,722 | 18.3 | 16.8 | 17.8 |
| Algeria | 18,618 | 514 | 2,761 | 13.5 | 12.4 | 17.1 |
| Gambia | 23,708 | 582 | 2,455 | 12.0 | 11.1 | 9.6 |
| Morocco | 413,717 | 8,413 | 2,034 | 10.0 | 9.2 | 11.8 |
| Nigeria | 126,066 | 2,022 | 1,604 | 7.9 | 7.2 | 6.4 |
| Bosnia and Herzegovina | 20,016 | 320 | 1,599 | 7.8 | 7.2 | 10.9 |
| Egypt | 154,674 | 2,309 | 1,493 | 7.3 | 6.7 | 10.2 |
| Côte d'Ivoire | 30,188 | 435 | 1,441 | 7.1 | 6.5 | 7.3 |
| Dominican Republic | 29,681 | 412 | 1,388 | 6.8 | 6.3 | 6.4 |
| Colombia | 22,006 | 268 | 1,218 | 6.0 | 5.5 | 5.8 |
| Afghanistan | 17,257 | 191 | 1,107 | 5.4 | 5.0 | 5.5 |
| Cuba | 24,144 | 235 | 973 | 4.8 | 4.4 | 5.3 |
| Senegal | 113,822 | 1,089 | 957 | 4.7 | 4.3 | 5.2 |
| Serbia | 30,257 | 244 | 806 | 4.0 | 3.6 | 5.7 |

My unadjusted numbers land close to the chart's *adjusted* numbers (Tunisia 18.3 vs 17.8, Côte
d'Ivoire 7.1 vs 7.3, Dominican Republic 6.8 vs 6.4, Afghanistan 5.4 vs 5.5), with Algeria, Bosnia and
Egypt 25-35% low and Gambia and Nigeria high.

**The irregular-population adjustment is the unresolved problem.** ISMU's XXIX Rapporto sulle
migrazioni puts the irregular foreign presence in Italy at **458,000** on 1 January 2023, 7.9% of a
total foreign presence of 5,775,000, down from 506,000 a year earlier
(https://www.ismu.org/xxix-rapporto-sulle-migrazioni-2023-comunicato-stampa-13-2-2024/). ISMU also
counts 176,000 "regolari non residenti", legally present but off the population register. Adding
those to the denominator multiplies it by 1.088 and 1.122 respectively, so every foreign ratio falls
by 8.1% or 10.9%. A chart "adjusted for est. irregular pop." should therefore sit *below* an
unadjusted one. The chart sits above mine. Either the adjustment was applied per country in a way I
cannot reconstruct, or it went the other way. Without Pallesen's offence list and per-country
irregular estimates this cannot be settled. Full table:
`italy/italy_violent_offender_rates_2023.csv`.

Also note the numerator is police reports of alleged offenders, as the chart says. That is upstream
of any court finding.

## 4. London — prosecutions for sex offences per 10,000

Both source files recovered from the Centre for Migration Control post of 28 July 2025
(https://www.migrationcentral.co.uk/p/up-to-47-of-sexual-offence-charges): the Met's FOI response
and CMC's own analysis workbook. CMC's "Top 10" sheet reproduces the chart exactly, Afghanistan
74.17, Eritrea 65.71, Algeria 56.36, Somalia 54.62, Sudan 42.86.

**What the numerator is.** Persons proceeded against, defined in the workbook as a distinct count of
custody records where the detainee received at least one charge *or an out-of-court disposal* for a
sexual offence, extracted by **arrest date**, 1 Jan 2018 to 31 Dec 2024. Out-of-court disposals
include simple cautions, community resolutions and penalty notices. These are not prosecutions in the
CPS sense and are certainly not convictions. The rates are **seven-year cumulative**, not annual;
Afghanistan's 74 per 10,000 is about 10.6 per 10,000 per year.

The Met's raw file splits nationality labels mid-period ("Afghanistan" 2018-2022, "Afghan" 2022-2024;
likewise Albania/Albanian). CMC merged them correctly. Counts below five are suppressed as "<5" and
CMC imputed them inconsistently, as 2 in some cells and 1 in others; the effect is a unit or two per
country.

**What the denominator is.** The workbook's own Data sheet says population came from the **2021
Annual Population Survey**, nationality basis, and explains that the census was rejected because its
"passport held" field omits many of the relevant countries. Pueyo's caption says 2021 census
denominators. That is wrong. The APS figures are rounded to the nearest 1,000 and several sit at
5,000-12,000, where ONS treats country-level APS estimates as unreliable.

Recomputing on 2021 census country of birth for London (ONS census-observations API,
`country_of_birth_190a`, region E12000007):

| Nationality | Persons 2018-24 | APS pop | Rate (CMC) | Census country of birth | Rate (census) | Factor |
|---|---|---|---|---|---|---|
| Afghanistan | 89 | 12,000 | 74.2 | 47,706 | 18.7 | 4.0 |
| Eritrea | 46 | 7,000 | 65.7 | 15,563 | 29.6 | 2.2 |
| Algeria | 62 | 11,000 | 56.4 | 18,767 | 33.0 | 1.7 |
| Somalia | 71 | 13,000 | 54.6 | 66,288 | 10.7 | 5.1 |
| Sudan | 30 | 7,000 | 42.9 | 9,552 | 31.4 | 1.4 |
| Albania | 43 | 12,000 | 35.8 | 34,773 | 12.4 | 2.9 |
| Iraq | 21 | 7,000 | 30.0 | 30,365 | 6.9 | 4.3 |
| UK-born baseline | 4,631 | 7,128,000 | 6.5 | 5,223,867 | 8.9 | — |

Nationality and country of birth are different concepts and the true denominator lies between them,
since many Afghan-born or Somali-born Londoners hold British passports and would appear in the
British numerator. But the choice moves Afghanistan from 11.4x the British rate to 2.1x, so the
headline is a denominator choice as much as a finding. CMC's own summary block is the defensible
version: 2,809 non-British against a 1,944,000 APS non-British population, 14.4 per 10,000, versus
6.5 for British, a ratio of **2.22x**. Full table: `uk/uk_london_sex_offence_rates.csv`.

Population growth after 2021 cuts the same way. The census predates the Afghan resettlement schemes,
so the 2021 denominator is too small for Afghans by 2024, pushing the rate up further. I did not
retrieve Home Office resettlement counts.

## 5. Eurostat — growth of sexual assault, index 2014 = 100

Series identified by pixel measurement of the chart against all three candidate codes: it is
`crim_off_cat`, unit `P_HTHAB`, **ICCS 03012 "sexual assault"** (not ICCS 0301 "sexual violence" and
not 03011 "rape"). Requests are in `eurostat/request_urls.txt`; full series in
`eurostat/eurostat_sexual_violence_rates.csv` and `eurostat/eurostat_index_2014_100.csv`.

| Country | Chart 2024 (measured) | Recomputed ICCS03012 | Gap | Recomputed ICCS0301 |
|---|---|---|---|---|
| France | 273.0 | 262.4 | +4.0% | 299.8 |
| Denmark | 204.2 | 191.8 | +6.5% | 216.3 |
| Spain | 174.9 | 167.8 | +4.2% | 198.6 |
| Ireland | 165.3 | 143.8 | +15.0% | 155.1 |
| Austria | 136.0 | 126.5 | +7.5% | 145.8 |
| Sweden | 110.3 | 101.2 | +9.0% | 114.6 |
| Netherlands | 105.5 | 99.0 | +6.6% | 94.7 |
| England and Wales | line ends at 2018, ~168 | 164.0 at 2018, nothing after | — | 199.4 at 2018 |

The gap is uniformly positive and modest, consistent with Eurostat's 29 April 2026 revision
post-dating Pueyo's extraction. Shape, ranking and the 2018 truncation all reproduce.

**England and Wales genuinely stops in 2018** in this table, for all three ICCS codes. The chart shows
that correctly, as a line ending mid-plot, but nothing on the chart tells the reader why.

### Recording and legal breaks in the period

Every series below carries at least one definitional break inside 2014-2024. I make no claim about
what drives the growth; these are the documented discontinuities.

- **Germany, 10 November 2016.** 50. Strafrechtsänderungsgesetz rewrote §177 StGB on a "Nein heißt
  Nein" basis and created a new offence of sexual harassment (§184i) covering groping, which had not
  previously been a criminal offence. BGBl. I S. 2460; https://dejure.org/gesetze/StGB/177.html
- **Austria, 1 January 2016.** Strafrechtsänderungsgesetz 2015 extended §218 StGB "sexuelle
  Belästigung" to any intensive touching of a sexual body region.
  https://www.bmfwf.gv.at/frauen-und-gleichstellung/gewalt-gegen-frauen/rechtliche-grundlagen-zu-gewalt-an-frauen/strafrechtsaenderungsgesetz-2015.html
- **Ireland, 2017.** Criminal Law (Sexual Offences) Act 2017 restructured the sexual offences code.
- **Sweden, 1 July 2018.** Consent-based reform of Chapter 6 of the Criminal Code; all sexual acts
  must be voluntary, and a new negligent-rape offence was created.
  https://en.wikipedia.org/wiki/Sexual_consent_in_law (dates corroborated by
  https://www.mdpi.com/2673-6756/5/3/38)
- **France, 3 August 2018.** Loi n° 2018-703 (Schiappa) created the offence of "outrage sexiste",
  extended limitation periods for offences against minors and raised penalties. The #MeToo reporting
  surge from late 2017 overlaps it.
- **Denmark, 1 January 2021.** Lov amending §§216 and 228 of the Penal Code to a consent basis,
  passed 17 December 2020. https://en.wikipedia.org/wiki/Sexual_consent_in_law
- **Spain, 7 October 2022.** Ley Orgánica 10/2022 ("solo sí es sí") abolished the abuso/agresión
  distinction and folded all non-consensual sexual acts into "agresión sexual", which mechanically
  moves offences into the ICCS sexual-assault category. Amended April 2023.
- **Netherlands, 1 July 2024.** Wet seksuele misdrijven raised maximum sentences and redefined
  aanranding and verkrachting. https://www.rijksoverheid.nl/themas/recht-veiligheid-en-defensie/seksuele-misdrijven/wet-seksuele-misdrijven
- **England and Wales.** The series is police-recorded crime, which rose sharply after Operation
  Yewtree (2012-13) and after HMIC's 2014 crime-data-integrity inspection forced compliance with the
  National Crime Recording Standard. The Eurostat series ends in 2018 regardless.

---

## Files

- `spain/` — `Informe-General_2024_firecrawl_norm.txt` (ministry report text), `padron_03005.csv`
  (INE Padrón by nationality 1998-2022), `ine_56936_*.json` / `ine_56937_birth_last.json` (ECP by
  nationality and by birthplace), `eurostat_migr_pop1ctz_ES.json`, `compute_spain.py`, and four CSVs:
  `spain_prison_rates.csv`, `spain_prison_ratios_padron2022.csv`,
  `spain_population_share_padron2022.csv`, `spain_population_share_by_origin.csv`.
- `italy/` — `offenders_by_country_2022_2024.csv`, `offenders_by_citizenship_2022_2024.csv`,
  `popstr_raw.csv`, `eurostat_migr_pop1ctz_IT.json`, `dsd_*.json`, `dataflows.json`,
  `compute_italy.py`, `italy_violent_offender_rates_2023.csv`.
- `uk/` — `met_foi_sexual_offence_cases_proceeded_against.xlsx` (Met FOI response),
  `cmc_analysis_sexual_offences_by_nationality_2018_2024.xlsx` (CMC workbook),
  `ons_cob190_rgn.json` (census country of birth by region), `compute_uk.py`,
  `uk_london_sex_offence_rates.csv`.
- `eurostat/` — `crim_off_cat_ICCS0301.json`, `..._ICCS03011.json`, `..._ICCS03012.json`,
  `build_index.py`, `eurostat_sexual_violence_rates.csv`, `eurostat_index_2014_100.csv`,
  `eurostat_chart_vs_recomputed.csv`.
- Every directory carries a `request_urls.txt` with the exact request URLs used.
- `measure_spain_chart.py` — pixel measurement of the Spain prison chart.

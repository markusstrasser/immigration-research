**Verdict:** The "Mexican second generation is 3.5× native whites" figure is Rumbaut's 2000-census table (US-born Mexican-origin men 18–39 incarcerated 5.90% vs 1.71% for native non-Hispanic whites). It pools second and third-plus generations, and it is 23 years old. Recomputed from ACS 1-year PUMS via the Census API, the same ratio is 2.56× (2010), 1.91× (2019) and 1.72× (2023), or about 2.1× in 2019–2023 once prison records coded generically "Hispanic" are reallocated. US-born Mexican-origin men now institutionalize at about the all-native rate (1.92% vs 2.05% in 2023), so counting them as "native" no longer inflates the native benchmark; removing them moves it by 0.02 points. The Mexican-origin population is 39.0M (CPS 2024): 31% immigrants, 35% second generation, 34% third-plus, and the third-plus share is understated by ethnic attrition. Among low-skill origins, Salvadorans and Guatemalans, Vietnamese, Chinese and (by 2023) Cambodians, Laotians and Hmong have US-born rates at or below Mexican-Americans', and Vietnamese and Chinese second generations out-attain native whites in education and earnings. [SOURCE: Rumbaut et al. 2006 Table 1; Census API ACS PUMS tabulations in `infra/immigration-fiscal/acs_institutional_2026_09_16/`; Census CPS ASEC 2024 generation Table 4; ABJP 2021; Sakamoto et al. 2022; Feliciano & Rumbaut 2019] [INFERENCE where marked]

# Mexican-origin population by generation and the incarceration comparator, 2000–2023

## 1. Where the 3.5× comes from, and what it pools

Rumbaut, Gonzales, Komaie, Morgan & Tafoya-Estrada 2006, Table 1 (2000 census 5% PUMS, men 18–39 in correctional institutions): foreign-born Mexican 0.70%, US-born Mexican 5.90%, native non-Hispanic white 1.71%, all US-born 3.51%, all foreign-born 0.86%, native Black 11.61%. 5.90/1.71 = 3.45. [SOURCE: https://escholarship.org/uc/item/8798n03x, Table 1, verified this session]

The authors flag the pooling themselves: "Almost all of the U.S.-born among those of Latin American and Asian origin can be assumed to consist of second-generation persons—with the exceptions of the Mexicans and Puerto Ricans, who may include among the U.S.-born a sizable but unknown number of third-generation persons." The census and ACS have no parental birthplace, so "US-born Mexican" is a second-plus-third-plus-generation mixture defined by Hispanic self-identification. The one US dataset that separates the Mexican second generation from third-plus non-Hispanic whites on a justice outcome (NLSY97, Inkpen 2024) finds no significant difference in time to first arrest; see [generational crime mechanisms](immigration-generational-crime-mechanisms-2026-09-16.md) §1.

## 2. Recomputation, 2010–2023 (ACS 1-year PUMS, Census API `tabulate`)

Men 18–39, share in institutional group quarters (TYPE/TYPEHUGQ = 2), PWGTP-weighted. Script, raw tabulations and the full CSV (Hispanic origins, non-Hispanic races, Asian detail, native and foreign-born) are in `infra/immigration-fiscal/acs_institutional_2026_09_16/`.

| Men 18–39 | 2000 (Rumbaut) | 2010 | 2019 | 2023 |
|---|---|---|---|---|
| US-born Mexican-origin | 5.90 | 4.37 | 2.82 | 1.92 |
| … adjusted for generic-Hispanic coding | — | 4.43 | 3.11 | 2.36 |
| Foreign-born Mexican | 0.70 | 2.34 | 1.87 | 1.13 |
| Native non-Hispanic white | 1.71 | 1.71 | 1.48 | 1.12 |
| All native-born | 3.51 | 3.24 | 2.64 | 2.05 |
| All native-born excluding Mexican-origin | — | 3.14 | 2.62 | 2.07 |
| Native non-Hispanic Black | 11.61 | 9.83 | 7.54 | 6.43 |
| Ratio US-born Mexican / native white (raw; adjusted) | 3.45 | 2.56; 2.60 | 1.91; 2.10 | 1.72; 2.11 |
| Mexican-origin share of native men 18–39 | ~5% | 8.3% | 11.2% | 11.7% |

Definitions and biases, each direction stated:
- **Institutional GQ, not "correctional".** ACS PUMS TYPE=2 pools correctional, nursing, psychiatric and juvenile facilities; Rumbaut used the 2000 correctional category. For men 18–39 the non-correctional share is small and similar across groups. [INFERENCE]
- **ICE detention counts as correctional GQ** in the ACS, so foreign-born rates after 2000 are inflated relative to Rumbaut's 2000 figure; the 2010 foreign-born Mexican 2.34% is not comparable to 0.70%. Native rates are unaffected. [SOURCE: [bias mechanisms memo](immigration-crime-statistics-bias-mechanisms-2026-09-16.md)] 
- **Generic "Hispanic" prison records.** HISP=24 ("all other Hispanic") native men run 4.6–9.0% institutionalized, 3–4× any named origin, and 42,087 of them were institutionalized in 2023 against 95,986 Mexican-origin. Correctional-facility records often carry "Hispanic" without origin. The adjusted row reallocates the HISP=24 excess above the all-native rate to named origins by population share; it is a bound, not a measurement. [INFERENCE]
- **Ethnic attrition** runs the other way: about 30% of third-generation Mexican-origin youth do not self-identify, and leavers are positively selected, so a self-ID "US-born Mexican" rate is biased up (Duncan & Trejo; [generational crime mechanisms](immigration-generational-crime-mechanisms-2026-09-16.md) §6 angle 3). Neither bias is quantified here; they partly offset.
- **Age structure inside 18–39** is younger for Mexican-Americans than for native whites, which raises the Mexican rate at peak-offending ages. Not standardized here.
- ACS 1-year samples are about one-fifth the 2000 5% PUMS; the small Asian-detail and Central American cells are noisy (Cambodian native 2023: 333 weighted institutional from a handful of records).

**Measurement checks added after the 2024–26 literature audit.** (1) Sabol, Johnson & Lynch 2025 show the 2023 ACS race redesign is a break: among Hispanic identifiers the share also reporting white fell from about 60% (2019) to 26% (2023), and single-race versus multi-race coding moves Black/white disparity ratios by 20%. Our white cell is non-Hispanic, so the Hispanic reclassification does not touch it; the multi-race shift does. Re-pulling native non-Hispanic white men 18–39 as "white alone or in combination" (RACWHT) instead of "white alone" (RAC1P=1) gives white rates 1.527% (2019) and 1.151% (2023) against 1.481% and 1.117%, so the ratio moves from 1.905 to 1.848 in 2019 and from 1.719 to 1.668 in 2023. The 3% shift is the same in both years and the 2019→2023 convergence is unchanged. (2) Glassman (Census SEHSD-WP2025-07) reports that 45.1% of the 2023 incarcerated ACS population is fully synthetic, up from 35.4% in 2019, with only sex, age, race, ethnicity and citizenship observed on the administrative records that feed the imputation; the rates in this section use exactly those variables plus Hispanic origin, so they are the safest cross-tab the file supports, and any 2023 GQ cross-tab on income or education would not be. (3) Prison Gerrymandering Project 2024: correctional facilities failed to report Hispanic status for over a quarter of people in the 2020 Census GQ operation, an independent confirmation of the under-recording the HISP=24 reallocation addresses. [SOURCE: Sabol, Johnson & Lynch, *Am J Crim Just* 50 (2025) 1374–1400, doi:10.1007/s12103-025-09810-1, Table 2 and text re-read 2026-09-16; https://www2.census.gov/library/working-papers/2025/demo/sehsd-wp2025-07.pdf; https://www.prisonersofthecensus.org/news/2024/10/30/group_quarters_errors/; `../infra/immigration-fiscal/acs_institutional_2026_09_16/white_denominator_sensitivity.py`]

## 3. Does counting the second generation as "native" hide the crime cost?

Two separate claims get merged in that argument.

1. **"Immigrants have lower crime rates than natives" is first-generation-specific.** True and documented across the repo: the adult-arrival floor does not transmit ([generational crime mechanisms](immigration-generational-crime-mechanisms-2026-09-16.md)). The Mexican lineage as a whole (immigrants plus descendants) sits between native whites and the native average, not below both.
2. **"The native benchmark is inflated by second-generation crime."** Arithmetically `r_native = a·r_2 + (1−a)·r_3+` ([crime memo](immigration-crime-rates-unauthorized-vs-native-born.md) §comparator identity). Including Mexican-Americans raises the native benchmark only if their rate exceeds the rest of natives'. In 2000 it did (5.90 vs 3.51), but they were ~5% of native men 18–39, so removing them moves the benchmark from 3.51 to about 3.38. In 2023 their rate (1.92) is below the all-native rate (2.05); removing them raises the benchmark to 2.07. The inflation claim is real in 2000 and gone by 2019–2023. [INFERENCE from the table above]

What survives is the white-comparator version: against native non-Hispanic whites the Mexican-origin US-born rate is 1.7–2.1× in 2023, down from 3.5× in 2000. Whether that residual is behaviour, arrest and prosecution exposure, age structure, or coding is not identified by GQ counts.

## 4. How many second and third generation

Census CPS ASEC 2024, Table 4 (Hispanic origin by generation), Mexican origin, all ages:

| Year | First gen | Second gen | Third-plus | Total |
|---|---|---|---|---|
| 2005 | 10.97M (39.8%) | 8.65M (31.3%) | 7.97M (28.9%) | 27.6M |
| 2015 | 11.75M (33.0%) | 12.66M (35.5%) | 11.22M (31.5%) | 35.6M |
| 2024 | 12.10M (31.0%) | 13.79M (35.3%) | 13.13M (33.6%) | 39.0M |

[SOURCE: https://www2.census.gov/programs-surveys/demo/tables/foreign-born/2024/cps2024/2024_asec_generation_table4.xlsx, copied to the infra folder]. For comparison, March 2001 CPS: 38% / 21% + 9% mixed-parentage / 32% (Jiménez 2017, Table 1). The immigrant share has fallen from 40% to 31% in two decades while the US-born generations grew by 14M. Third-plus is a self-identification count; the true third-plus Mexican-ancestry population is larger by the attrition rate (Duncan & Trejo: 83% of third-generation children of Mexican ancestry identify as Hispanic).

Second generation here is CPS parental birthplace (either parent Mexican-born); Puerto Ricans are 92% third-plus by the same table because island birth counts as US birth.

## 5. Other low-skill immigrant groups against the Mexican benchmark

"Better" needs an outcome. Three outcomes, same sources throughout:

| Origin (parents low-skill) | US-born inst. 2000 → 2023 (men 18–39) | Second-gen BA (CPS 2010–15, ages 30–39, SoCal) | ABJP mobility at p25, sons |
|---|---|---|---|
| Mexico | 5.90 → 1.92 | 23.5% | above US-born; one of three modern origins with a >5 log-point second-gen earnings gap remaining |
| El Salvador / Guatemala | 3.01 → 0.89 / 1.01 | — (earnings below third-plus whites before mid-30s, Villarreal & Tamborini 2023) | above US-born at p25, below at p75 |
| Dominican Rep. | 3.71 → 1.43 | — | above US-born; first-gen gap −60 log points |
| Vietnam | 5.60 → 0.30 | 54.9% | first-gen gap −60 log points, second gen closes it; outcomes above whites (Sakamoto et al. 2022) |
| Cambodia / Laos / Hmong | 7.26 → 1.35 / 1.60 / 0.84 | 35.2% (pooled) | below whites on SES, above Blacks and Hispanics (Sakamoto et al. 2022) |
| China (incl. low-skill Fuzhounese) | 0.65 → 0.12 | 81.8% | among the most upwardly mobile |
| Haiti, Jamaica | — | — | the only modern origins whose sons at p25 do not exceed the US-born |
| Native non-Hispanic white | 1.71 → 1.12 | 43.1% | reference |

[SOURCE: Rumbaut 2006 Table 1; ACS PUMS CSV in infra folder; Feliciano & Rumbaut 2019 Table 1, DOI 10.1080/01419870.2019.1667507; Abramitzky, Boustan, Jácome & Pérez 2021, AER 111(2), Figs 1, 3, 4; Sakamoto, Iceland & Siskar 2022, Population Research and Policy Review 41; Villarreal & Tamborini 2023, Demography, DOI 10.1215/00703370-10924116]

Reading. On incarceration the Central American second generation (nearly all second generation, because the wave is recent) ran at half the Mexican US-born rate in 2000 and, for Salvadorans and Guatemalans, at or below native whites by 2023 (Hondurans 1.65%, above), with parents less educated than Mexican parents. Vietnamese and Chinese are the clear "aspirational" low-skill cases: refugee and Fuzhounese parents with little schooling, second generations that out-attain native whites. Cambodian, Laotian and Hmong second generations started worst (7.26% in 2000) and now sit near Mexican-Americans on incarceration and above Hispanics on income. Dominicans track Mexicans. Haitian and Jamaican children are the one documented case of no mobility advantage at the bottom. Feliciano's selectivity result is the organizing fact: second-generation attainment follows how positively selected the parents were relative to their origin country, and Mexican migrants are the least selected large stream ("hyposelected", Lee & Zhou), which also makes Mexican-origin the group whose third-plus generation is largest, oldest and most exposed to ethnic attrition. Which unauthorized streams are the more selected ones (Indian, Chinese, recent Venezuelan and Colombian arrivals) is a composition question this memo does not settle. [INFERENCE]

## 6. What this changes in the repo

- [Confidence ladder](immigration-confidence-ladder.md) entry on second-generation coding ("Light-TX has no generation variable → unaddressable in current crime data"): the pooled US-born-by-origin comparator IS addressable in ACS GQ counts, and the 2019–2023 numbers show the native-benchmark inflation is gone even though the white-comparator gap remains. The pending CPS second-generation loader still cannot settle crime (no outcome variable).
- Any citation of "3.5×" should carry the year (2000), the pooling (second plus third-plus, self-ID) and the current value (1.7–2.1×, 2023).

## 7. Why did the ratio fall? A state decomposition and the detection-technology hypothesis

Operator hypothesis (2026-09-16): the convergence is a technology effect, with the street crime Mexican-Americans are exposed to becoming easier to detect and less profitable while white crime is more sophisticated and less detectable, and "all crime decreased since better cameras and algorithms".

**State decomposition (same ACS tabulations, `by_state.py`, `for=state:` filter):**

| Men 18–39, US-born Mexican vs native NH white | 2010 | 2023 |
|---|---|---|
| California: Mexican / white / ratio | 3.91 / 1.79 / **2.19×** | 1.73 / 0.75 / **2.30×** |
| Texas | 4.69 / 2.14 / 2.19× | 2.58 / 1.53 / 1.69× |
| All other states | 4.61 / 1.67 / 2.76× | 1.66 / 1.11 / 1.50× |
| US | 4.37 / 1.71 / 2.56× | 1.92 / 1.12 / 1.72× |

Three readings. (1) California's decarceration (realignment 2011, Prop 47 2014, Prop 57 2016) halved both groups' rates and left the ratio unchanged; it is not the source of national convergence. (2) The convergence is in Texas and the rest of the country, where the white native rate fell by a third while the Mexican-American rate fell by almost two-thirds. (3) The US-born Mexican-origin population outside California and Texas nearly doubled (1.09M → 2.01M men 18–39), so part of the national change is the second generation growing up in new destinations with lower rates. [SOURCE: `by_state_result.txt`] [INFERENCE for the readings]

**What the detection-technology hypothesis predicts, and what the record shows.**

- *Detection did not improve.* If cameras, phones and databases raised the probability of catching offenders, clearance rates would rise. FBI clearance by arrest fell for violent crime from 47.5% (2000) to 45.5% (2019) to 36.7% (2022), for property crime from 16.7% to 17.2% to 12.1%, and for homicide from 93% (1962) to 64% (1994), 61% (2019) and 54% (2020) (Cook & Mancik 2023, *Annual Review of Criminology*, DOI 10.1146/annurev-criminol-022422-122744). Cook and Mancik's preferred explanation is a rising evidentiary standard for arrest; prison admissions per homicide rose while clearance fell. The falling clearance is concentrated in gun homicides with Black victims. So "algorithms catch street criminals more often" is not what happened at the arrest margin. [SOURCE: https://drugpolicyfacts.org/table/clearance (FBI UCR series); Cook & Mancik 2023]
- *Timing.* The large crime decline was 1991–2000, before camera networks, license-plate readers or predictive tools existed at scale; the second decline (2007–2014) precedes most of them too. Incarceration peaked in 2008–09 and fell for policy reasons (drug and property reclassification, sentencing reform, COVID releases) on top of lower crime. The institutionalization series here is mostly a punishment series, not a crime series. [INFERENCE; policy chronology is standard]
- *The version with evidence is opportunity and deterrence, not detection.* Farrell, Tseloni, Mailley & Tilley 2011 (*JRCD* 48(2), DOI 10.1177/0022427810391539): electronic immobilizers and central locking drove the vehicle-theft collapse, and reduced "debut" crimes may have cut onset into other offending. Edlund & Machado, "It's the Phone, Stupid: Mobiles and Murder" (NBER w25883): county antenna build-out lowered 1990s homicide, with effects concentrated in urban counties, among Black and Hispanic young men, and in gang and drug-related killings; the mechanism is that phones dissolved turf-based street dealing and its profits. Klick, MacDonald & Stratmann 2012 find state-level phone penetration associated with fewer rapes and assaults, not property crime. Doleac 2017 (*AEJ: Applied* 9(1)): DNA database expansions deter profiled offenders and reduce crime rates. This is the operator's mechanism in a specific form: technology removed the profit from the crime types to which young urban Hispanic and Black men were most exposed (turf drug markets, car theft), and that shows up as fewer of them entering the system. It is a 1990s–2000s story that would explain the 2000→2010 step better than the 2010→2023 one. [SOURCE: the four papers, abstracts and NBER text read this session]
- *"White crime is more sophisticated."* Fraud and financial crime are under-prosecuted, so an incarceration comparator understates white *harm*; but native whites in prison are there mainly for drugs, violence and property, the same offences as everyone else, and the white native rate also fell by a third. The relevant white-specific 2010s shock is the opioid and methamphetamine wave in rural and small-town areas, where jail incarceration rose while urban jails emptied; that is the leading candidate for why white rates fell less outside California, and it is a drug-epidemic effect, not a detection-technology one. [INFERENCE; the rural-jail divergence is documented by Vera's Incarceration Trends but not re-verified here]

**Where this leaves the hypothesis.** Rejected in the "better cameras and algorithms → more detection → less crime" form: detection fell. Supported in the "technology removed the opportunity and profit from street crime types" form for the 1990s, with published causal evidence that the effect was concentrated among young Hispanic and Black men. Untested for 2010–2023, where the within-state pattern (flat ratio in California, convergence elsewhere) points to differential drug-epidemic exposure and to compositional change in where the second generation grows up. The decisive next test is offence composition: if the Mexican-American decline is disproportionately drug and property offences while the white decline is not, the opportunity story survives into the 2010s; BJS National Prisoner Statistics by Hispanic origin × offence can show it. [INFERENCE]

## 8. Offence composition: what the decline was made of (BJS, non-Hispanic white vs Hispanic)

BJS publishes sentenced state prisoners by most serious offence × race/Hispanic origin (Prisoners in 2010, App. Table 16b for 2009; Prisoners in 2022 Statistical Tables, Tables 16–17 for 2021). Categories: violent (murder, manslaughter, rape/sexual assault, robbery, assault, other), property (burglary, larceny, motor-vehicle theft, fraud, other), drug (possession vs trafficking/other), public order (weapons, DUI, other). No Mexican-origin or nativity split exists; jails have no national offence × ethnicity table. Script and CSV: `acs_institutional_2026_09_16/bjs_offense_by_ethnicity.py`; the year-by-year series, Texas check, age standardisation and stock-flow model are in `hisp_violent_stock_2026_09_16/`.

**Basis correction (2026-09-16, later the same day).** The first version of this section compared 2009 counts from *Prisoners in 2010* with 2021 counts from *Prisoners in 2022* and reported Hispanic violent prisoners +36% (117,800 → 160,100). That comparison is invalid. *Prisoners in 2011* restates 31 December 2009 on the estimation basis used ever since (SISCF-2004 ratio, later blended with SPI-2016): Hispanic total 287,568 not 212,100, Hispanic violent 159,800 not 117,800, white total 467,290 not 532,000 (App. Table 8, p. 26; verified by the parent from the PDF). BJS's own footnote in the 2010 report says the race/Hispanic data source changed and prior years are not comparable. Administrative prison records under-record Hispanic origin by about a quarter and absorb the difference into "white" (Prisoners in 2016 Table 5: Hispanic 16.6% administrative vs 21.1% self-reported; Alabama reports zero Hispanic prisoners of 26,421), and the survey adjustment that corrects this is the size of the apparent "rise". All figures below are on the consistent basis.

| State prisoners, 2009 (restated) → 2021 | NH white count | per 100k | Hispanic count | per 100k |
|---|---|---|---|---|
| Total | 467,290 → 321,700 (−31%) | −28% | 287,568 → 224,300 (−22%) | −40% |
| Violent | 231,500 → 176,400 (−24%) | −21% | 159,800 → 160,100 (0%) | −22% |
| Property | 111,000 → 57,600 (−48%) | −46% | 43,100 → 19,000 (−56%) | −66% |
| Drug | 69,200 → 48,200 (−30%) | −27% | 49,400 → 22,600 (−54%) | −65% |
| Public order | — | — | 34,000 → 21,900 (−36%) | −50% |
| Violent share of prisoners | 50% → 55% | | 56% → 71% | |
| Drug-possession share, 2021 | 4.9% | | 2.7% | |

[SOURCE: BJS p11 App. Table 8 (2009 restated); BJS p22st Tables 16–17; resident populations Census Vintage 2009/2021, rounded]

Male imprisonment rate per 100,000 (state + federal, sentence > 1 year), 2010 → 2022 [SOURCE: p10 App. Table 15; p22st Table 13]:

| Age | NH white | Hispanic | ratio |
|---|---|---|---|
| 20–24 | 638 → 229 (−64%) | 1,908 → 663 (−65%) | 2.99× → 2.90× |
| 25–29 | 980 → 514 (−48%) | 2,707 → 1,462 (−46%) | 2.76× → 2.84× |
| 30–34 | 1,061 → 732 (−31%) | 2,808 → 1,774 (−37%) | 2.65× → 2.42× |
| 35–39 | 995 → 813 (−18%) | 2,486 → 1,747 (−30%) | 2.50× → 2.15× |

Readings.
- **"Just using" is not what prisons hold.** Drug possession is 2.7% of Hispanic and 4.9% of white state prisoners; drug offences of any kind are 10% and 15%. Simple possession is a jail and probation phenomenon and after 2014 mostly a misdemeanour in the largest Hispanic states. [INFERENCE on the jail point]
- **The decline for both groups is property and drug, and Hispanics fell faster on every category per capita**, including violent (−22% vs −21%). This is the offence mix the opportunity and policy stories predict (immobilizers, phones, drug-sentencing reform).
- **The Hispanic violent share rose from 56% to 71% because the non-violent stock drained, not because the violent stock grew.** Mean time served (BJS Time Served 2016): violent 4.7 years, murder 15.0, property and drug 1.8. Had the violent stock drained at the non-violent rate it would be 80,000, not 160,000; the difference is sentence-length lag. Hispanic violent new court commitments were flat in count 2006–2011 (24,900) while the population grew a quarter (Prisoners in 2012 admissions series), so the flow fell per capita too.
- **Texas, which codes Hispanic origin directly with no survey adjustment, confirms the direction:** Hispanic imprisonment per capita −39% vs white −18%, 2009–2021, Hispanic share of prisoners +4% relative, matching the consistent-basis national +4% (TDCJ Statistical Reports FY2009 and FY2021, Demographic Highlights p. 6). California could not be obtained (CDCR archives unavailable).
- **Ageing lowered the Hispanic male rate**, by 6.1% on direct standardisation (2010 age-specific rates on 2022 age structure), about the same as for white men (−6.8%); age explains none of the divergence.
- **Age-specific male rates fell in parallel** at 20–29 (both −46% to −65%, ratio flat near 2.9×) and faster for Hispanics at 30–39. The sentenced-prison series therefore shows the same convergence as the ACS institutional series for US-born Mexican men (§2), only muted because it pools all Hispanics including the foreign-born and excludes jails.

**For the technology hypothesis**: the decline is vehicle theft, burglary and drugs for both groups, which fits the opportunity form; the violent residual is where technology has the least documented effect. The earlier reading that the Hispanic violent stock "did not fall" is withdrawn.

## 9. Does the US collect worse data than Europe, and is it political?

Operator question (2026-09-16), checked against six bounded X full-archive searches (178 posts, May–Sept 2026, $0.89; raw JSONL in `x_pull_2026_09_16/`) and primary sources.

**What the X discourse looks like.** The Danish and Swedish debates argue over official register tables (Statistics Denmark and Justice Ministry indices, Brå, the Rockwool 2026 study; a Council of Europe commissioner's "no link" claim was the week's flashpoint with 500-like replies quoting the tables). The anglophone debate is about absence: "Canada doesn't collect", "the UK refuses to release", "Australia doesn't collect country of birth", "NYPD doesn't track nationality", "the US doesn't collect national origin for immigrant or second-gen offenders". The US-specific debate is stuck on one dataset, Texas DPS, described as "the only state-level agency consistently tracking immigration status". Grok reply-bots supply Danish indices to threads in every language. [SOURCE: X pull, sample not representative]

**The structural fact.** European tables exist because of population registers: a personal ID number links birth, parents' birthplace, residence, education, income and convictions for everyone. The Rockwool 2026 study (Andersen, Andersen, Bäckman, Christensen, van Hazebroek, Mitchell, Nieuwbeerta, Skardhamar et al., Study Paper 283) runs full-population male 15–30 conviction data for Denmark 1991–2017, Norway 1993–2017, Sweden 1991–2017, the Netherlands 2006–2017 and New Zealand 2007–2017 with Blinder-Oaxaca decompositions on own and parental education, employment and income. Findings: convictions fell for every group in every country; about 70% of the immigrant gap is composition, and in Denmark and Norway in 2017 the composition-adjusted immigrant gap is negligible; the descendant gap is not composition, remaining over 200% above comparable majority men in Denmark and the Netherlands; New Zealand's non-Western groups convict *below* the majority. A companion 2026 analysis splits MENAPT from Southeast Asian origin: SE Asian immigrants and descendants have matched or undercut ethnic Danes since 2007–08, MENAPT descendants stay about 3× comparable Danes after controls. [SOURCE: https://en.rockwoolfonden.dk/publications/a-statistical-decomposition-of-nativity-gaps-in-criminal-convictions-using-full-population-data-from-five-developed-democracies/ and the Danish summaries; not yet read in full] The US has no register, no personal ID linkage across agencies, and the Census dropped the parental-birthplace question after 1970 (CPS restored it in 1994; ACS never had it). That is why the whole US second-generation literature rests on NLSY97, Add Health and CILS cohorts and on the self-ID "US-born Mexican" cell used in §2.

**What is political, checked.**
- *United Kingdom*: the Ministry of Justice refused a June 2025 FOI request for convictions 2018–2024 by nationality and offence; the Information Commissioner ordered disclosure on 22 June 2026; the government appealed to the First-tier Tribunal on 17 July 2026. The prison population by nationality is published quarterly (FNOs 12% of prisoners; Albanian, Irish, Polish, Romanian, Indian largest), and ONS holds no crime-by-migrant-status breakdown. [SOURCE: https://www.migrationcentral.co.uk/p/labour-government-launches-legal (advocacy source; the ICO decision itself not retrieved); GOV.UK OMSQ Q3 2025; ONS FOI 30 Jan 2026]
- *United States*: FBI arrest data record race compulsorily and Hispanic ethnicity optionally, nativity never; BJS prisoner statistics carry race/Hispanic but nativity only through the self-report Survey of Prison Inmates ([race/ethnicity memo](immigration-crime-race-ethnicity-2026-09-05.md)); sanctuary statutes in several states bar local agencies from recording immigration status; DHS/ICE encounter data are not linked to court outcomes. These are choices, and they have partisan valence in both directions (status non-recording is a left policy; the 1970 parental-birthplace drop and the absence of a register are older and bipartisan). [INFERENCE on valence]

**The asymmetry the debate misses.** On *legal status* the US has the best data in the world and Europe has none: Texas DPS fingerprint-matches every arrestee against DHS records, which is how the conviction-rate comparisons in the [crime memo](immigration-crime-rates-unauthorized-vs-native-born.md) exist; Danish and Swedish registers do not know who is undocumented. On *ancestry and generation* Europe is far ahead and the US measures descendants only through ethnic self-identification, which attrits selectively (§2). So "the US has worse data" is right for the second-generation question and wrong for the unauthorized-immigrant question, and each side of the debate leans on the dataset that favours it. [INFERENCE]

**The linked file exists and has not been tabulated (2026-09-16 audit).** Opportunity Insights' cleared extract for the 1978–83 birth cohorts carries, per child, the tax-record parent link, parental income rank, each parent's country of birth (2000 long form or 2005–15 ACS) and the child's 2010 institutionalization status. The public release of the country-of-origin cut (Online Table 6a/6b, 51 countries) is income rank only: Mexican-parentage children at parental p25 reach rank 43.2 against 41.2 for children of US-born parents; El Salvador 46.0, Vietnam 58.3, China 61.9, Haiti 39.9. Every Opportunity Insights incarceration product is race × gender × geography × parental income, with no nativity dimension; the CJARS Justice Outcomes Explorer carries age, sex and race/ethnicity only; the Abramitzky–Boustan–Jácome–Pérez–Torres 2024 incarceration series is first generation vs US-born throughout. So "second-generation incarceration by parental origin" is one disclosure request against a file that already exists, not new data collection, and nobody has filed it. Abramitzky et al. 2021 did not hold the microdata ("available only in aggregate form"), so it is a Census-side tabulation, not a rerun of their package. The 1880–1940 full-count censuses record both parents' birthplaces and institutional group quarters, so the historical second-generation series is computable from public IPUMS. [SOURCE: https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6a_parametric.csv, values re-read 2026-09-16; https://www2.census.gov/programs-surveys/cjars/technical-documentation/file-layouts/2022/cjars_joe_2022_st_variable_metadata.json; lane `../infra/immigration-fiscal/secgen_linkage_2026_09_16/RESULT.md`]

## 10. Reproducing the @tomaspueyo European compilation (2026-09-15)

Operator ask: can the thread https://x.com/tomaspueyo/status/2099900501680701530 be reproduced. Four lanes rebuilt every chart from the named official source; per-lane reports, scripts, request bodies and tidy CSVs in `infra/immigration-fiscal/pueyo_repro_2026_09_16/`. Thread text and charts archived in `source_thread/`. [SOURCE: lane RESULT.md files; parent spot-checked Danish numerators by independent API calls and German raw files]

| Chart | Source | Reproduces? | What changes on inspection |
|---|---|---|---|
| Denmark violent crime by origin 2010–22 (raw) | STRAFNA4 / FOLK1C | Yes, all 20 bars within 0.04 (Kuwait 10.1×, Somalia 9.8×, Lebanon 8.7×) | Small cells: Kuwait 226 persons, Algeria 83 |
| Denmark 12 crime types by origin (Pallesen) | STRAFNA4 / FOLK1C | Yes, 54/60 bars within 1×; Somalia rape 19.6× vs 20×, robbery 33.3× vs 33×, attempted homicide 26.9× vs 27× | "Palestine" is not a Statistics Denmark category; the bar is Lebanon+Kuwait+Jordan (2% error). "Ex-Yugoslavia" excludes Bosnia, Croatia, N. Macedonia |
| Denmark adjusted for age, sex, year | not open | No open table crosses offence × age × sex × origin | Best substitute (all offences, STRAFNA3) removes 19–44% of each gap; chart implies 13–58%; consistent, unverifiable |
| Denmark "share of men convicted" (ft.dk) | Parliamentary answer 2019-20 REU 291 | Yes, all 34 bars within 0.5 pp | Cumulative conviction prevalence to age 30, men born 1985–87. Not convictions per arrest; carries no information on profiling, which is what the thread uses it for |
| Germany ranking (avg of total, violent, sexual, homicide ratios) | PKS 2025 T62 / AZR 31.12.2025 | Yes, 19/20 bars within 0.2; "murder" is key 892500 | Immigration-law offences (which only foreigners can commit) are inside "total": Algeria total 23.0× → 18.0×, Georgia 18.6× → 11.9×, aggregate non-German 3.38× → 2.78×. 19.5% of non-German suspects had no lawful residence and cannot be in the denominator; Algeria records 0.40 suspects per registered resident per year, 53% immigration offences. Violent (3.80×) and sexual (1.94×) ratios barely move |
| Germany "+50% Muslim premium" | same + World Bank GDP | +48% on his ≥10k sample (t = 2.0) | +16% and not significant on all 175 nationalities; +27% population-weighted; age-sex share control changes nothing (collinear) |
| Sweden suspects by origin | Brå 2021:9 Table B6 | Yes, all 32 bars | Chart uses the unstandardised column and drops B6's highest bar (Other Africa 5.89). Brå's controls cut foreign-born excess 2.51× → 1.76× |
| Norway "charges per 1,000 inhabitants" | SSB commissioned tables 2024-12-09 | Yes, 9/9 to two decimals | The column is men 15–24 resident in Oslo, charges (not persons) cumulated 2020–23. National all-ages Somali rate 78 per 1,000 over four years vs 9.7 for non-immigrants; the chart's 483 is not a national or annual rate |
| Finland sexual offences by nationality 2023 | StatFin 13jg | No | No year 2000–25, counting method or numerator/denominator pairing yields the plotted values; Ukraine plotted 11.4 vs series max 5.5. 49 of 60 nationalities have <20 suspects; Congo's 101.6 rests on 9. Chart is from a paywalled newspaper |
| Spain population shares | INE Padrón 1 Jan 2022 | Yes, mean gap 0.006 pp | Three years older than the prison data |
| Spain prison ratio by nationality | Informe General 2024 Table 49 | Yes, ordering exact; Albania 24.9× vs 19.6–27.6× depending on denominator year | Excludes Catalonia; left panel is share of foreign, not all, prisoners; foreigners 29.1% pre-trial vs 11.9% Spaniards. Albania's denominator is 2,549–5,022 residents |
| Italy violent crime by citizenship (Pallesen) | ISTAT SDMX, 13 offence codes | Partly: Tunisia 18.3× vs 17.8×, Côte d'Ivoire 7.1 vs 7.3; Algeria, Bosnia, Egypt 25–35% below chart | ISMU's 458k irregulars plus 176k legal non-registered would move every ratio down 8–11%; the chart's "adjusted for irregular pop." sits above unadjusted, direction unexplained |
| London sex-offence "prosecutions" | Met FOI via Centre for Migration Control | Arithmetic yes | Numerator is charges or out-of-court disposals by arrest date, cumulative 2018–24; denominators are 2021 Annual Population Survey nationality rounded to 1,000 (Afghanistan 12,000), not the census as captioned. On census country of birth Afghanistan is 18.7 not 74.2 per 10,000 and 2.1× not 11.4× the British rate; the true nationality denominator lies between. CMC's own aggregate: non-British 2.22× British |
| England & Wales arrests | Daily Mail FOI | Not independently reproducible (numerators not public) | — |
| Eurostat sexual-assault index 2014=100 | crim_off_cat ICCS 03012 | Yes within 4–15% (April 2026 revision) | England & Wales has no Eurostat data after 2018 (the line stops). Consent-law rewrites: Germany 2016, Austria 2016, Ireland 2017, Sweden 2018, France 2018, Denmark 2021, Spain 2022, Netherlands 2024 |

**What survives.** The origin ordering is real and stable across countries: MENAPT and Horn-of-Africa origins sit far above natives in Denmark, Sweden, Norway, Germany and Italy on every measure, and Southeast and East Asian origins sit at or below natives. That much reproduces from official data wherever it exists.

**What does not.** (1) The magnitudes at the top are inflated by construction in three countries: immigration-law offences and non-resident suspects in Germany, a young-men-in-Oslo column mislabelled as a national rate in Norway, and survey denominators of 7,000–13,000 in London. (2) The "controls for age, sex, economics and education" claim rests on one age-sex-year chart that cannot be checked; where full controls exist (Brå 2021, Rockwool 2026, §9) they cut the immigrant gap by 30–70% and leave the descendant gap. (3) The profiling rebuttal uses a chart that measures something else. (4) The Finland chart cannot be produced from Statistics Finland's own table. (5) Two charts carry relabelled categories ("Palestine", "Ex-Yugoslavia") not disclosed on the chart. (6) The thread's summary claim that total crime fell only because natives aged while immigrants offset it is asserted, not shown, in any chart. [INFERENCE for the summary judgments; each row cites its lane]

**Repo consequence.** The registry pull folder now has Danish country-of-origin rates by 94 offence types 2008–2024 (`denmark/dk_origin_rates.csv`), German PKS-by-nationality with and without immigration offences (`germany/de_nationality_rates.csv`), the Brå B6 standardised and unstandardised columns, the SSB Oslo/national charge tables, Spanish prison-by-nationality, ISTAT offender rates by citizenship and the Eurostat series, all re-pullable. These supersede the thread as the citation for any European origin comparison.

## 11. Why low-skill origins diverge in the second generation: a measured test and the mechanism evidence

Operator ask: explain claim 74 (§5) or research it. Two lanes: a CPS build (`infra/immigration-fiscal/secgen_selectivity_2026_09_16/`) and a literature memo ([second-generation divergence mechanisms](immigration-secgen-origin-divergence-mechanisms-2026-09-16.md)).

**The measured test.** Census CPS ASEC microdata API, 2019–2024 pooled, US-born adults 25–44 with a foreign-born parent, parental origin = father's birth country (mother's if father US-born), 29 origins with ≥150 respondents. Verified against Census generation tables within 0.74% (all ages), 0.64% (18–64) and 0.58% (Mexican second generation). Parent spot check: 2023 single-year, father-Mexico-born cell gives 23.3% BA+ against the pooled 22.0%.

| Parental origin | 2nd-gen BA+ % | 2nd-gen <HS % | 1st-gen BA % | Origin-country BA % | Selectivity (1st-gen − origin) |
|---|---|---|---|---|---|
| India | 84.9 | 1.0 | 87.4 | 12.1 | +75 |
| China | 78.4 | 3.2 | 64.6 | 7.7 | +57 |
| Vietnam | 63.1 | 2.2 | 31.7 | 11.5 | +20 |
| Philippines | 55.4 | 1.1 | 57.5 | 18.1 | +39 |
| Jamaica | 50.6 | 4.0 | 35.2 | 11.0 | +24 |
| Cuba | 48.2 | 3.5 | 32.2 | 15.3 | +17 |
| Haiti | 44.8 | 2.4 | 24.8 | 4.5 | +20 |
| Cambodia | 39.0 | 7.1 | 18.1 | 4.6 | +14 |
| Dominican Rep. | 37.0 | 5.7 | 23.3 | 14.4 | +9 |
| Laos | 34.3 | 4.9 | 17.7 | 5.2 | +13 |
| El Salvador | 30.9 | 5.6 | 10.5 | 8.4 | +2 |
| Guatemala | 28.2 | 8.2 | 9.1 | 5.7 | +3 |
| Mexico | 22.0 | 10.3 | 9.9 | 17.0 | **−7** |
| 3rd+ gen NH white | 47.0 | 3.6 | | | |
| 3rd+ gen Hispanic | 26.9 | 8.0 | | | |

Weighted least squares of second-gen BA+ share on the selectivity index across the 29 origins: R² = 0.91, slope 0.81 (HC1 SE 0.05), robust across ten specifications including a cohort-matched one (pre-2000 adult arrivals vs Barro-Lee 1990 origin attainment). Mexico's residual is −1.7 points (−0.4 with dummies): Mexican-American second-generation attainment is exactly what the only large negatively selected stream predicts, not an anomaly. Refugee origins do not deviate as a class in the main spec (+5, p = 0.34); Vietnam alone over-performs its prediction by 17–26 points, Laos and Cambodia sit at or below it. The honest limit, stated by the lane: origin-country attainment on its own has no predictive power (R² = 0.008), so the index is only narrowly separable from parents' own education level (R² 0.91 vs 0.86). What the data establish is that second-generation attainment tracks first-generation attainment nearly one for one at the group level; whether "relative to origin" adds anything is not cleanly identified in 29 points. [SOURCE: `secgen_by_origin.csv`, `regressions.json`] [INFERENCE on the identification limit]

**The mechanism evidence** (memo, ranked by identification × plausible share):

1. **Parental unauthorized status** (Bean et al. 2011, IIMMLA, IRCA-eligibility instrument): 1.24 years of child schooling (2SLS), 1.5 (OLS), 2.0 raw. Mexican and Central American by construction; near zero for refugee-origin and East Asian samples. The best-identified Mexican-specific factor, but "largest" is not established because nothing comparable exists for other origins.
2. **Parental English** (Bleakley & Chin 2008, critical-period IV, N = 164,559): cuts child dropout by about 80% of its mean. A-grade identification, origin-blind, so it explains levels, not why Vietnamese children beat Mexican ones.
3. **Measurement**: ethnic attrition is positively selected for Hispanics (+0.76 years) and negatively for Asians (−0.6), inflating the measured gap from both ends; but the only explicit correction ever computed is about 0.1 years, and the "third-generation stagnation" is partly a third-versus-fourth-plus pooling artefact. Do not cite it as "the stagnation is an artefact".
4. **Selectivity relative to origin** at the individual level (Feliciano & Lanuza 2017): 0.3–0.5 child-years for a 40-percentile gap. Small once absolute parental education is held, consistent with the CPS result above.
5. Age at arrival before 14 gives native-equal outcomes (Evans & Fitzgerald 2017), which is the 1.5-generation refugee story; phenotype effects for Mexican-Americans of about 1.5 years light-vs-dark (Murguía & Telles 1996, Texas strong, California about zero); Chetty et al. 2020 Hispanic child rank 43 vs white 45 at parent rank 25, no origin breakdown.
6. **No identified estimate exists** for ethnic capital or co-ethnic institutions, or for refugee resettlement support on the second generation. Family structure runs the wrong way: second-generation Mexican-American women bear children later, not earlier. No paper decomposes the Asian–Latino second-generation gap on one dataset.

**Reading.** The origin ranking is mostly parents' education, transmitted at about 0.8 points of BA share per point. Mexico sits on that line. The Mexican-specific residual mechanisms with evidence are parental legal status and, for the third generation, measurement. The Vietnamese over-performance is the one real anomaly in the table and has no identified explanation; ethnic-institution accounts of it are narrative. The highest-value next pull is Chetty et al.'s online mobility tables by parental country of birth, which no memo has used. [INFERENCE]

## 12. Closing the "partial ledger" objection: employer payroll, sales, property and K-12 by generation

The annual ledger in the [by-generation memo](immigration-mexican-origin-by-generation-2026-09-16.md) §5 counts modeled personal payroll, federal and state income tax after refundable credits, cash transfers and SPM non-cash resources. It omits employer-side payroll, sales and excise, property tax and the K-12 cost of the unit's children. A lane re-ran the same generator (`build/analyze_cps_fiscal_2025.py`, imported, not re-implemented; baseline reproduced to $0.17) on CPS ASEC 2025 and added the four items with published rates: 6.2% OASDI to the $168,600 cap plus 1.45% HI on wage and salary income; Tax Foundation 2024 combined state and local sales rates on a 0.35 taxable share of SPM resources (ITEP effective-rate arm as sensitivity); ACS 2023 state effective property rates on owners' house value (renters zero, pass-through arm as sensitivity); Census FY2024 per-pupil current spending ($17,619 national, by state) on children 5–17 times the ACS public-pupil ratio 0.80.

Difference from third-plus non-Hispanic whites, adults 25–64, dollars per adult per year, equal-all-members allocation, SDR se in parentheses:

| | All natives | All 2nd gen | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|---|
| Taxes minus selected transfers (baseline) | −1,313 (106) | −122 (413) | −6,066 (353) | −4,916 (456) | −8,016 (338) |
| + employer payroll | −182 | 5 | −946 | −637 | −1,594 |
| + sales/excise | −53 | −7 | −266 | −157 | −457 |
| + property | −133 | 0 | −548 | −505 | −795 |
| − K-12 | −38 | −204 | −460 | −64 | −660 |
| **Extended balance** | −1,719 (124) | −327 (488) | **−8,286 (443)** | −6,279 (546) | −11,522 (402) |

Every addition widens the Mexican second-generation gap, to 137% of baseline; the eight sensitivity arms span −8,123 (renter pass-through) to −8,555 (differential pupil ratio); the adults-only allocation gives −10,633 (se 587). The all-origin second generation stays level with whites on every row. The reason is structural: the baseline gap is already a tax gap (−$6,965 in modeled taxes, with cash transfers $994 *lower*), and the three added taxes are functions of the same earnings and house values, while K-12 scales with children (0.27 pupils per Mexican-second-generation adult against 0.20). What still lies outside the ledger and could in principle move it: institutional care, corporate tax incidence, accrued rather than received Social Security and Medicare, pure public goods (the largest discretionary choice in any such accounting), and general-equilibrium wage effects. None of these is a candidate to flip the sign, because the sign follows from 25% BA attainment against 44% and earnings 71% of whites'. Sales and property rows are modeled from aggregate rates, not observed. [SOURCE: `../infra/immigration-fiscal/gen_ledger_extension_2026_09_16/RESULT.md`, `extended_ledger_result.txt`; IRS Pub. 15 (2024); Tax Foundation 2024 sales-tax table; ITEP *Who Pays?* 7th ed.; Census ASSF FY2024 Summary Table 8; ACS 2023 B25103/B25077] [FRAMING-SENSITIVE: children of the Mexican second generation are third generation, and their schooling is charged to the parents' unit exactly as SNAP and school lunch already are]

## Revisions

- 2026-09-16 — Created. Concept: generational comparator for the Mexican-origin population; supersedes nothing, refines the confidence-ladder coding-bias entry.
- 2026-09-16 — Added §7: state decomposition (California ratio flat 2.19→2.30×; convergence is Texas and other states) and the detection-technology hypothesis assessed against clearance rates and the phone/security/DNA literature.
- 2026-09-16 — Added §8: BJS offence composition 2009→2021 and age-specific imprisonment rates 2010→2022, white vs Hispanic.
- 2026-09-16 — Added §9: EU vs US data regimes from an X discourse sample plus primary checks (Rockwool 2026 five-country decomposition; UK MoJ FOI appeal).
- 2026-09-16 — Added §10: four-lane reproduction of the Pueyo European compilation; origin ordering reproduces, several headline magnitudes are construction artefacts.
- 2026-09-16 — §8 corrected to the consistent BJS estimation basis (Prisoners in 2011 restatement of 2009). The Hispanic violent count is flat, per capita −22%; the earlier +36% was a coding-basis artefact. Withdrawn: "the violent stock did not fall for Hispanics". Lane: `hisp_violent_stock_2026_09_16/`.
- 2026-09-16 — Added §11: CPS selectivity test (R² 0.91, Mexico on the line) and ranked mechanism evidence for second-generation origin divergence.
- 2026-09-16 — §9 gains the linked-data audit: no published second-generation incarceration by parental origin exists; the Opportunity Insights 1978–83 file has both ingredients and publishes income rank only. Lane: `secgen_linkage_2026_09_16/`.
- 2026-09-16 — Added §12: the annual ledger extended with employer payroll, sales, property and K-12; the Mexican second-generation gap widens from −$6,066 to −$8,286 per adult. Lane: `gen_ledger_extension_2026_09_16/`.
- 2026-09-16 — §2 gains the measurement checks from the 2024–26 literature audit (Sabol 2025 race redesign: white-denominator sensitivity moves the ratio 3% in both years; Glassman 2025 synthetic share; 2020 Census GQ Hispanic non-reporting). Lane: `newdata_lit_2026_09_16/`.

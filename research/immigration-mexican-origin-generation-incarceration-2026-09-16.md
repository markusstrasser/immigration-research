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

BJS publishes sentenced state prisoners by most serious offence × race/Hispanic origin (Prisoners in 2010, App. Table 16b for 2009; Prisoners in 2022 Statistical Tables, Tables 16–17 for 2021). Categories: violent (murder, manslaughter, rape/sexual assault, robbery, assault, other), property (burglary, larceny, motor-vehicle theft, fraud, other), drug (possession vs trafficking/other), public order (weapons, DUI, other). No Mexican-origin or nativity split exists; jails (short stays, pretrial) have no national offence × ethnicity table. Transcription and per-capita script: `bjs_offense_by_ethnicity.py`, output in `bjs_offense_by_ethnicity_result.txt`.

| State prisoners, 2009 → 2021 | NH white count | per 100k | Hispanic count | per 100k |
|---|---|---|---|---|
| Total | 532,000 → 321,700 (−40%) | −37% | 212,100 → 224,300 (+6%) | −18% |
| Violent | −34% | −31% | +36% | +5% |
| … murder | −34% | −31% | −1% | −24% |
| … robbery | −55% | −53% | 0% | −23% |
| … assault | −19% | −15% | +68% | +30% |
| … sexual assault | −33% | −30% | +95% | +50% |
| Property | −56% | −55% | −45% | −57% |
| … motor-vehicle theft | −68% | −67% | −72% | −79% |
| Drug | −35% | −32% | −45% | −58% |
| Public order | −32% | −30% | +37% | +6% |
| Violent share of prisoners | 50% → 55% | | 56% → 71% | |
| Drug-possession share, 2021 | 4.9% | | 2.7% | |

[SOURCE: BJS p10 App. Table 16b; BJS p22st Tables 16–17; resident populations Census Vintage 2009/2021, rounded]

Male imprisonment rate per 100,000 (state + federal, sentence > 1 year), 2010 → 2022 [SOURCE: p10 App. Table 15; p22st Table 13]:

| Age | NH white | Hispanic | ratio |
|---|---|---|---|
| 20–24 | 638 → 229 (−64%) | 1,908 → 663 (−65%) | 2.99× → 2.90× |
| 25–29 | 980 → 514 (−48%) | 2,707 → 1,462 (−46%) | 2.76× → 2.84× |
| 30–34 | 1,061 → 732 (−31%) | 2,808 → 1,774 (−37%) | 2.65× → 2.42× |
| 35–39 | 995 → 813 (−18%) | 2,486 → 1,747 (−30%) | 2.50× → 2.15× |

Readings.
- **"Just using" is not what prisons hold.** Drug possession is 2.7% of Hispanic and 4.9% of white state prisoners; drug offences of any kind are 10% and 15%. Simple possession is a jail and probation phenomenon and after 2014 mostly a misdemeanour in the largest Hispanic states. [INFERENCE on the jail point]
- **The decline for both groups is property and drug.** Motor-vehicle theft stock fell by two-thirds to three-quarters for both, burglary by half, drug by a third to a half. This is the offence mix the opportunity and policy stories predict (immobilizers, phones, drug-sentencing reform), and it is where the Hispanic decline exceeded the white decline per capita.
- **The violent stock did not fall for Hispanics** (+36% in count, +5% per capita) while it fell a third for whites, and the Hispanic prison population is now 71% violent, the most violent-heavy of any group. Three non-behavioural contributors are known and none is quantified here: long sentences make violent stock lag flows by decades; the Hispanic population aged into prime imprisonment ages (median age 27 → 30); and state prison records increasingly code Hispanic origin separately instead of folding it into white, which moves people from the white to the Hispanic column (BJS itself flags a 2010 source change). The +95% in sexual-assault stock is not credible as behaviour. [INFERENCE]
- **Age-specific male rates fell in parallel.** At 20–29 both groups fell 46–65% and the Hispanic/white ratio is unchanged at about 2.8–3.0×; at 30–39 the Hispanic rate fell faster. So the sentenced-prison series for all Hispanics (foreign-born included, all origins) shows less convergence than the ACS institutional series for US-born Mexican-origin men (§2, 2.56× → 1.72×). The difference is what the ACS adds (jails, federal, ICE) and who it isolates (US-born, Mexican). The jail component is exactly the short-stay drug and property churn that reforms emptied. [INFERENCE]
- **For the technology hypothesis**: the offence mix of the decline (vehicle theft, burglary, drugs) fits the opportunity form. The violent residual, which is most of what remains, is where technology has had the least documented effect and where the Hispanic/white ratio is stable.

## Revisions

- 2026-09-16 — Created. Concept: generational comparator for the Mexican-origin population; supersedes nothing, refines the confidence-ladder coding-bias entry.
- 2026-09-16 — Added §7: state decomposition (California ratio flat 2.19→2.30×; convergence is Texas and other states) and the detection-technology hypothesis assessed against clearance rates and the phone/security/DNA literature.
- 2026-09-16 — Added §8: BJS offence composition 2009→2021 and age-specific imprisonment rates 2010→2022, white vs Hispanic.

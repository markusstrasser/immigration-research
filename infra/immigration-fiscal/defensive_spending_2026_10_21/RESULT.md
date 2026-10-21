claude-opus-5-5

# Defensive spending, guard labor, talent allocation, and the Japan comparison — lane 2026-10-21

**Verdict:** The US does carry a much larger defensive economy than Japan, but the gap is in
prisons, police and the military, not in guards or trust, and none of it is identified as caused by
the Mexican-origin group. Nothing is added to the account.

- **Guards are no different.** Private guards are 0.88 per 100 jobs in the US and 0.87 in Japan.
- **Police and prisons are.** US police and detectives are 0.61 per 100 jobs against Japan's 0.39.
  Corrections staff are 0.28 against 0.03, and the incarcerated are 1.20 against 0.06.
- **Public order and defence spending follow.** Public order and safety is 1.81% of GDP in the US
  against 1.12% in Japan; defence is 3.03% against 1.05% (COFOG 2023).
- **The US has many more lawyers.** It has 395 bar-admitted lawyers per 100k, or 223 counting
  employed lawyers only. Japan has 37, or 65 adding judicial scriveners and patent attorneys.
- **No "efficient, high-trust Japan" behind the cheap lunch.** Japan's food service produces 30% of
  US value added per hour, the yen is about 40% undervalued on the Big Mac index, and Japanese say
  "most people can be trusted" less often than Americans (34% vs 37%).

Within the US, across 389 metros, guard employment does not rise with the Mexican-origin share
once income, poverty, size, Black share and region are controlled. The coefficient is +0.0001
(SE 0.0015) unweighted and −0.0049 (0.0031) weighted. This matches the priced private-security row
(−$0.6bn). Police and corrections jobs do rise with that share (+0.0164, SE 0.0042), but the police
part disappears once the ten border metros are dropped. The corrections part survives (+0.0040,
0.0012, weighted). Prisons and detention sit where the land is, not where the offenders live, and
the account already charges justice by use. The literature identifies no output cost of lawyers or
guards beyond their wage bill: Murphy–Shleifer–Vishny's law coefficient is "not structural", and
Hsieh et al. is a calibrated barrier model. So the operator's "lawyer who could have been a
scientist" channel is real in principle but has no defensible dollar figure.
[CALCULATION: `defensive.py` → `derived/*.csv`] [SOURCE: `sources_literature.md`] [FRAMING-SENSITIVE]

**Switzerland (added 15:27, descriptive only).** Switzerland has the lowest measured defensive
labor of the three:
- narrow guard labor 0.93 per 100 employed and ISCO protective services 0.85;
- incarcerated 0.14;
- 133 bar-association lawyers per 100k.

Its finance employment share (5.5%) matches the US's (5.2%). Its foreign nationals are 63% EU/EFTA.
French and German nationals are more tertiary-educated than the Swiss. Kosovo, Serbia and Türkiye
nationals have about three times the Swiss crude suspect rate.

**Natural experiments (speculative branch).** Three designs clear the bar:
- German refugee dispersal: generalized trust unchanged, .00 (.01).
- Italy, a shift-share design: municipal security budgets up via fear.
- Chile, a shift-share design: households' security and block-guard hiring up, with victimization
  not significant.

None measures time use or attention, so that branch stops.

Evidence level: the occupational counts are **measured**. The cross-country comparisons are on
partly different bases (stated per row). The within-US results are **correlations**. This lane was
produced through an LLM; see `notes/llm-bias-caveat.md`.

Provenance: [SOURCE: per-row citations below] [DATA: derived/*.csv] [CALCULATION: scripts in this lane] [INFERENCE: verdicts] [UNVERIFIED: anything so marked]

## Scope

Operator ask 2026-10-21: lost productivity as a generative channel (talent pulled into lawyering,
guarding, judging); Japan as a low-defensive-cost, high-trust comparator; intangibles that show up as
GDP while raising everyone's costs (exitgroup "Mom is working for Moloch").

Questions 1–5 from the dispatch: guard labor (US vs Japan, lawyers per capita), defensive expenditure
in GDP, allocation of talent, within-US cross-section against Mexican-origin / low-skill immigrant
share, Japan's cheap meals and low theft.

Already priced (not to be re-added): the pairing's social rows in
`sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json`, amenity sorting ($7–15bn),
trust channel held off the ledger in `crime_cost_2026_09_16/RESULT.md`.

## Prior repo work found before pre-registration (not re-derived)

- `guard_labor_2026_09_16/` (2026-09-16): 51-state ACS PUMS guard-share regression. Foreign-born
  share +0.0196 pp/pp (SE 0.0070) with controls; **Hispanic share −0.0004 (0.0037)**; fragile to
  NV/HI/DC; public police+corrections $/capita null with controls. Cites Bove–Elia–Ferraresi 2021
  (Italy, IV: +0.12–0.30 pp of municipal budget per pp immigrants).
- `social_costs_unpriced_2026_09_28/` item 2 (adopted 2026-09-28): private security
  (contract guards $34.5bn, in-house guards $26.3bn, systems $30.3bn) allocated by offending share
  minus population share; Mexican-origin central −$0.6bn, now the priced household and commercial
  security rows. Its `guard_black.py` reruns the state regression: Hispanic share null in every spec.
- So question 4's state-level answer exists. This lane adds a metro cross-section with the
  occupation detail the state lane lacked (police, corrections, guards, lawyers separately).

## Pre-registration (written 2026-10-21 15:11 JST, before any magnitude below was looked up)

**Q1 Guard labor and lawyers.**
- Narrow guard labor = police and sheriff's officers + detectives + correctional officers and
  jailers + bailiffs + private security guards + private detectives + gaming surveillance + their
  first-line supervisors, as a share of employment. US from BLS OEWS May 2024 national (SOC 33-xxxx,
  23-1011); Japan from the 2020 Population Census occupation table (保安職業従事者 and its minor
  groups) or the Labour Force Survey, cross-checked against administrative counts (National Police
  Agency guard-industry report for 警備員, police 定員). Firefighters are reported separately and
  excluded from guard labor (they defend against fire, not people).
- Bowles–Jayadev broad guard labor (adds military, prisoners, unemployed, supervisory labor): quoted
  from their papers for the US and the rich-country ranking; recomputed only for the narrow and
  "narrow + military + prisoners" definitions, where admin counts exist for both countries.
- Lawyers: bar-admitted lawyers per 100,000 (ABA 2024 count; JFBA 弁護士 count). Fair-comparison
  arm adds Japan's 司法書士 (judicial scriveners) and 弁理士 (patent attorneys), each shown on its own
  row; 行政書士 and 税理士 shown beside, not added (their US analogues are not lawyers).
- Cross-country: ILOSTAT ISCO-08 sub-major group 54 (protective services, includes firefighters)
  share of employment, latest year, for the US, Japan and other rich countries that report it.

**Q2 Defensive expenditure in GDP.** Literature figures quoted as published (Nordhaus–Tobin 1972
regrettable necessities; Leipert's defensive-expenditure accounts). Own comparable components, % of
GDP, latest common year, each row separate: COFOG 02 defence, COFOG 03 public order and safety
(OECD/IMF general government), private security services output, legal services output. A sum is
shown only across rows measured on the same basis in both countries.

**Q3 Allocation of talent.** Read MSV 1991, Baumol 1990, Hsieh–Hurst–Jones–Klenow 2019 for (i) the
estimated output effect, (ii) the variation used, (iii) whether it is identified or a cross-country
correlation. No dollar figure unless a paper identifies an elasticity transferable to US lawyers or
guards; the default opportunity cost of defensive labor is its wage bill, which the security rows
already price.

**Q4 Within-US metro cross-section.** Unit: OEWS May 2024 MSAs (workplace employment), n ≈ 390.
Outcomes (per 100 jobs): (a) guards 33-9032; (b) police + corrections + detectives + bailiffs
(33-3012, 33-3021, 33-3051, 33-3011); (c) lawyers 23-1011. Regressor of interest: Mexican-origin
share of population (ACS 2023 5-year B03001); second regressor in separate models: foreign-born
share. Controls: log median household income, poverty rate, log population, Black share, Census
region dummies, and violent-crime rate (FBI 2019 MSA table) in a separate column because crime may
mediate. OLS with HC1 SEs, unweighted and population-weighted. Robustness: drop Las Vegas, Reno,
Atlantic City, Honolulu, Washington DC metros (gaming/tourism/federal). Report b, SE, n, R²; implied
share of national guard labor linked to the group = b × group share ÷ mean outcome. This is a
correlation; identification would need a shift-share or enforcement-shock design (e.g. Secure
Communities rollout) with guard employment as outcome.

**Q5 Japan prices and theft.** For each candidate cause (exchange rate and price level, wages,
rents, deflation, competition/density, crime, trust, institutions such as koban and lost-property
law, age structure), one primary measurement and the evidence that separates it from the others.
Homogeneity is credited only with evidence that separates it from income, policing, culture and age.

**Attribution rule.** Size of channel first; then the share plausibly linked to immigration, with
its identification; nothing the account already prices (private/commercial security, victims,
property crime, business crime, amenity sorting) is added.

## Plan change 1 (logged 2026-10-21 15:27 JST, operator additions at 15:11, 15:13, 15:14)

Written before any Swiss magnitude or natural-experiment result was looked up.

- **Switzerland joins Q1–Q3 as a third descriptive comparator**, with the same definitions:
  - narrow guard labor (police, corrections, private guards) per 100 employed, from
    administrative counts (cantonal and federal police staffing, prison staff, the Swiss security
    industry or BFS STATENT NACE 80);
  - ILOSTAT ISCO-08 group 54 on the same survey basis as the US and Japan rows;
  - incarcerated per 100 employed (BFS);
  - lawyers per 100k residents (Swiss Bar Association members and cantonal registers, both shown).
  - Military is reported beside, not added: Switzerland's militia army has few full-time soldiers,
    so a headcount is not comparable.
  - **Occupational and industry mix**: ILOSTAT employment shares by ISIC section, with finance
    and insurance (K) shown for CH, US and JP, and ISCO major groups. A high-productivity reading
    is checked against financialization.
- **Swiss immigrant intake is reported by origin and skill, never as a foreign-born share
  comparable to the US Mexican-origin share.** It covers EU/EFTA vs third-country shares, top
  nationalities and tertiary share of recent arrivals. Where BFS publishes outcomes by nationality
  (employment, occupation, criminal convictions), EU nationals are contrasted with Balkan and
  Turkish nationals as the within-Switzerland contrast.
- **All cross-country comparisons stay descriptive.** They carry no causal claim and no dollar
  figure.
- **Speculative branch: does a low-friction, high-trust environment free work time and
  attention?** It is included only through a natural experiment that moves a place's group
  composition and measures trust, defensive spending or labor, or time use. Bar: as-good-as-random
  or policy-assigned variation in composition (refugee dispersal, a policy opening), a measured
  outcome on one of those three, and a stated first stage.
  - Candidates: Dinesen & Sønderskov registry exposure (Denmark); Dustmann, Vasiljeva & Damm 2019
    (Danish dispersal); Swedish and Norwegian dispersal papers; Beerli, Ruffner, Siegenthaler & Peri
    2021 (Swiss cross-border opening); Mariel.
  - Each is reported with its sign. If none clears the bar, the branch stops with that statement.

## Log (times from `date`)

- 2026-10-21 15:09 JST stub; 15:11 pre-registration written, before magnitudes.
- 15:18–15:25 JST data pulled, `defensive.py` run; literature fork returned `sources_literature.md`;
  15:25 post-hoc border arm added (labelled as post-hoc below); results written.

## Q1. Guard labor and lawyers, US vs Japan

[DATA: `derived/guard_labor_us_japan.csv`, `derived/guard_lawyer_summary.csv`, `derived/ilo_isco54_shares.csv`]

| Per 100 employed | US | Japan | Bases |
|---|---:|---:|---|
| Police and detectives (incl. supervisors) | 0.606 | 0.390 | US OEWS May 2024; JP NPA police officers 定員 2024 |
| Corrections and bailiffs | 0.283 | 0.026 | JP MOJ 刑務官 定員 2025 |
| Private guards, detectives, gaming surveillance | 0.883 | 0.871 | JP NPA 警備員 584,868, end-2023 |
| **Narrow guard labor** | **1.771** | **1.287** | |
| Active military | 0.826 | 0.338 | DMDC 1,273,828; JP SDF ≈227k [TRAINING-DATA] |
| Incarcerated | 1.202 | 0.061 | BJS 1,852,900; JP ≈40.9k [UNVERIFIED digit read] |
| Narrow + military + incarcerated | 3.799 | 1.686 | |
| ISCO-08 group 54, one survey basis (incl. firefighters) | 1.44 (2025) | 1.73 (2023) | ILOSTAT LFS |

Denominators: US OEWS wage-and-salary jobs (154.19M), Japan LFS employment via ILOSTAT (67.14M).
The bases differ: OEWS excludes the self-employed, and Japan's numerators are administrative
counts. The ISCO-54 row is the only like-for-like comparison, and on it Japan is higher. Japan's 54
probably includes some SDF and certainly includes its large construction-site traffic-guard
workforce. [INFERENCE] On every basis, Japan does not employ fewer private guards per worker than
the US.

Bowles–Jayadev's broad measure (US 26.1% of the labor force in 2002) is 15.7 points supervisors,
4.8 unemployed, 1.8 military, 1.5 prisoners and 2.2 guards. Japan is not in their 18-country table,
and that table excludes police and private guards. The US is second of 18 (22.2%), behind Greece,
mainly on supervisors and prisoners. They write that none of their correlations (Gini r = 0.40,
conflict index r = 0.61, trust r = −0.14) is identified [SOURCE: `sources_literature.md` §A].

Lawyers per 100k residents:

| Count | Per 100k |
|---|---:|
| US, ABA active lawyers (1,322,649) | 394.9 |
| US, OEWS-employed lawyers (747,750) | 223.3 |
| Japan, 弁護士 (45,808) | 36.8 |
| Japan, adding 司法書士 23,156 and 弁理士 11,745 | 64.9 |
| Japan, also adding 行政書士 51,619 (beside) | 106.4 |
| Japan, 税理士 81,280 (beside, not lawyers) | 65.4 |

On the fairest pairing (US employed lawyers against Japan's three litigation-capable professions),
the US ratio is 3.4×. Against the most generous Japanese count it is 2.1×. Baumol's own Japan
passage attributes the low litigation to rules, such as the Fair Trade Commission's permission
requirement for antitrust suits, not to character [SOURCE: `sources_literature.md` §C].

US wage bills, 2024 (OEWS mean × employment): police and detectives $81.1bn, corrections $28.4bn,
private guards $60.5bn, lawyers $136.7bn.

## Q2. Defensive expenditure in GDP

[DATA: `derived/cofog_defence_order_2023.csv`, OECD Table 11 general government, ÷ World Bank GDP]

| 2023, % of GDP | US | Japan |
|---|---:|---:|
| Defence (COFOG 02) | 3.03 | 1.05 |
| Public order and safety (COFOG 03) | 1.81 | 1.12 |
| of which police / fire / courts / prisons | n/a in OECD file | 0.59 / 0.33 / 0.09 / 0.04 |

The public-order gap is 0.69 points of GDP, about $190bn at US 2023 GDP. Private security services
(NAICS 561611/561612/561621, about $68bn in 2022, from `social_costs_unpriced_2026_09_28`) are
about 0.26% of US GDP; Japan's 警備業 sales were not obtained [GAP]. No sum across the two countries
is shown because the private rows do not match. Literature, as published: Nordhaus–Tobin's
regrettable and overhead expenses rose from 8% to 16% of GNP over 1929–65, mostly defence. Leipert
finds German defensive costs at 6.8% → 11.6% of GDP over 1970–88 across six spheres; his security
sub-share was not obtained [GAP]. Japan's 1973 NNW deducted pollution, commuting and traffic
accidents and had no police line [SOURCE: `sources_literature.md` §B]. These are classification
exercises: "defensive" is a judgment about purpose, not an estimate of what would be produced
without the threat.

## Q3. Allocation of talent

- **Murphy–Shleifer–Vishny 1991.** Cross-country growth 1970–85, 91 countries. Law enrollment
  share: −0.031 (0.025) with GDP control only; −0.078 (0.040) with Barro controls in the
  large-enrollment sample. It is significant in one of four columns. The authors: "we cannot
  interpret these relationships as structural". **Correlation.**
- **Baumol 1990.** Historical illustration; "none of the material approaches anything that
  constitutes a formal test". **Not evidence of magnitude.**
- **Hsieh–Hurst–Jones–Klenow 2019.** 20–40% of US growth in output per person (1960–2010) from
  falling barriers to women and Black men in a calibrated Roy model. **Model-imputed**, and the
  mechanism is barriers, not rent-seeking.
- **Magee's lawyer curve** ("36% too many lawyers ... $220 billion") did not survive Epp's
  replication, and Magee concedes his state results "were not particularly robust".

[INFERENCE] The identified cost of a guard or lawyer is the output they would otherwise produce.
Under competitive pay that is their wage, already a resource cost wherever the account prices
security or justice. The "lawyer who could have been a scientist" adds a wedge only if science's
social return exceeds its private return. That wedge is plausible (R&D spillovers) but no study
ties it to the size of the legal or guard sector. No dollar figure is defensible.

## Q4. Within-US metro cross-section

[DATA: `derived/metro_panel.csv`, `derived/metro_regressions.csv`, `derived/metro_match_stats.json`]
393 OEWS MSAs; ACS matched 393/393, FBI 2018 crime matched 321. Guards are non-missing in 389
metros and police plus corrections in 265 (OEWS suppression). Coefficients are jobs per 100 jobs
per percentage point of Mexican-origin share, HC1 SEs. "Linked" = b × population-weighted mean
share (11.9–12.3% across samples) ÷ mean outcome, a correlation-based share, not a causal one.

| Outcome | Spec | Unweighted b (SE) | Weighted b (SE) | Linked share (U / W) |
|---|---|---|---|---|
| Guards | bivariate | 0.0027 (0.0013) | 0.0023 (0.0030) | 3.6% / 3.0% |
| Guards | controls + region | 0.0001 (0.0015) | −0.0049 (0.0031) | 0.1% / −6.6% |
| Guards | + violent crime (n 319) | −0.0000 (0.0018) | −0.0020 (0.0030) | ~0 / −3.0% |
| Guards | drop gaming/tourism/DC | 0.0004 (0.0015) | −0.0040 (0.0029) | 0.6% / −5.6% |
| Police + corrections | controls + region (n 265) | 0.0164 (0.0042) | 0.0074 (0.0024) | 27% / 12% |
| Police only | controls + region | 0.0104 (0.0031) | 0.0025 (0.0019) | 24% / 5.7% |
| Police only | drop border metros [post-hoc] | 0.0074 (0.0055) | −0.0006 (0.0018) | 16% / −1.3% |
| Corrections only | controls + region | 0.0080 (0.0030) | 0.0043 (0.0013) | 46% / 25% |
| Corrections only | drop border metros [post-hoc] | 0.0059 (0.0023) | 0.0040 (0.0012) | 33% / 22% |
| Lawyers | controls + region | −0.0021 (0.0006) | −0.0061 (0.0016) | −4.8% / −14% |

Foreign-born share, by contrast, predicts more guards: +0.0077 (0.0034) unweighted and +0.0118
(0.0053) weighted with controls. That reproduces the state lane's sign. Foreign-born share bundles
high-income gateway metros (New York, Miami, San Jose), and guards cluster there.

Readings:
- **Guards.** Null for the Mexican-origin share in every controlled specification. That agrees
  with the state lane (Hispanic −0.0004) and with the priced private-security row (−$0.6bn).
- **Police.** The positive association is a border effect. Weighted, it vanishes when San Diego,
  El Centro, Yuma, Tucson, Sierra Vista, Las Cruces, El Paso, Laredo, McAllen and Brownsville are
  dropped. OEWS counts federal officers where they work, so Border Patrol and port staff land in
  these metros.
- **Corrections.** The association survives but is a workplace measure. Prisons and immigration
  detention are sited in low-cost metros (Central Valley, south Texas) and hold people from the
  whole state. The account charges justice and custody by use, so a group's share of corrections
  is already in the fiscal ledger whatever the prison's location.
- **Lawyers.** Fewer lawyers per job where the Mexican-origin share is high, the opposite sign to
  a "defensive lawyering" story.

**Identification.** None. To identify the effect you would need exogenous variation in group
presence, such as a shift-share on 1980 settlement × national inflows, or the Secure Communities
rollout (Hines–Peri 2019 find removals did not change police personnel), with guard employment by
place of service as the outcome. No US paper identifies a private-guard response to Mexican-origin
or low-skill immigrant presence (`sources_literature.md` §E). Bove–Elia–Ferraresi identify a
public-security budget response in Italy that runs through fear, which the account prices in its
fear row.

## Q5. Japan's cheap meals and low theft

| Candidate cause | Evidence | Verdict |
|---|---|---|
| Exchange rate and price level | Big Mac ¥480 vs $6.01, yen ≈41% undervalued (July 2025) | Explains a large share of the "cheap" in dollars |
| Low service wages | Minimum wage ¥1,055 (FY2024) ≈ $7; part-time ad wage ≈¥1,180 | Explains the rest of the low price |
| Productivity | Food and accommodation services at 30.2% of US value added per hour (JPC, PPP, 2020); quality adjustment closes only 10–20 points | Japan is **less** efficient here, not more |
| Generalized trust | "Most people can be trusted": Japan 34%, US 37% (IVS wave 7) | Japan is not a higher-trust society on this measure |
| Assurance and institutions | Yamagishi: Americans more trusting, Japanese rely on committed relations; West: lost-property law (koban hand-in duty, 5–20% finder's fee) explains wallet returns beyond altruism | Order rests on monitoring and rules, much of it unpaid enforcement that occupation counts miss |
| Low crime | Japan theft ≈389 per 100k recorded (2023); Roberts–LaFree: economic stress, certainty of punishment and age structure predict Japanese crime better than social-disorganization measures | Supported; US comparison cell not read [GAP] |
| Homogeneity | No paper found that separates it from income, policing, age and institutions | Not credited |

[INFERENCE] The cowork café where nothing is stolen is low theft, which is real. It rests on a
certain-punishment, high-monitoring regime and an old population, not on a stock of generalized
trust that the US lacks. The $6 lunch is a low-wage, weak-yen, low-productivity service sector.
Neither travels to the US by removing a population group.

## Steelmen

**"A large hidden defensive economy linked to the group."** The US defensive sector is large:
police, corrections and private guards cost $170bn in wages, and public order runs 0.7 points of
GDP above Japan. GDP counts all of it as output (Bowles–Jayadev, Nordhaus–Tobin), so growth figures
overstate welfare. The Moloch essay's repurchase mechanism, buying a house in a safe school district,
is real and is the amenity-sorting row. Bove–Elia–Ferraresi show immigration can raise security
budgets through fear. The metro police-and-corrections association with the Mexican-origin share is
positive and survives controls. The strongest version: unpaid enforcement (neighbours, norms) is
invisible guard labor, so a group that lowers it would raise paid guard labor without leaving a
trace in crime data.

**"Defensive labor tracks inequality, crime and policy, and is already priced."** The US–Japan gap
is carried by incarceration (1.20 vs 0.06 per 100 employed), police (0.61 vs 0.39) and the military
(0.83 vs 0.34), not by private guards (0.88 vs 0.87). That points to crime levels and sentencing
policy. Within the US the guard association with the Mexican-origin share is null, and the police
association vanishes off the border. Corrections staffing follows prison siting. The account
already prices the group's crime through victims, fear, private and commercial security, business
crime and justice by use, and amenity sorting at $7–15bn.

[INFERENCE] The second steelman fits the measured pattern better. The first rests on unmeasured
informal enforcement, which this lane cannot see.

## Attribution and overlap

| Channel | Size (US, 2024 $) | Share plausibly linked to the group | Identification | Added to the account? |
|---|---|---|---|---|
| Private guards | $60.5bn wages | ≈0 (metro null; state null) | correlation | No: private and commercial security rows |
| Police and detectives | $81.1bn wages | ≈0 off the border; border staffing is immigration enforcement | correlation | No: justice by use (crime); enforcement is a policy choice [GAP: confirm the account's treatment of CBP/ICE staffing] |
| Corrections | $28.4bn wages | not separable from siting | correlation | No: custody key charges by use |
| Lawyers | $136.7bn wages | negative association | correlation | No |
| Talent-misallocation wedge | unmeasured | unmeasured | none | No |
| Defence | 3.0% of GDP | none | — | zero response by assumption (standing case rule) |

## Gaps and next queries

- [GAP] Japan 警備業 sales and legal-services output for a like-for-like private defensive share of
  GDP (Economic Census for Business Activity, 警備業 売上高).
- [GAP] Japan SDF 現員 and prison population: read the MOD 資料67 and MOJ 矯正統計 23-00-03
  tables directly.
- [GAP] Check whether the account carries CBP/ICE staffing as a cost of the group before using the
  border police association in any ledger.
- [GAP] Workplace vs residence: rerun corrections with ACS residence-based occupation (C24010) to
  separate prison siting from local demand.
- Next query for an identified design: shift-share of Mexican inflows on county guard employment
  from QCEW NAICS 561612 by place, 1990–2020.

## Reproduce

```sh
# from the repository root; downloads go to this lane's ignored _cache/
# OEWS via Wayback (bls.gov 403s curl): web.archive.org/web/20261004165530id_/https://www.bls.gov/oes/special-requests/oesm24nat.zip
#                                       web.archive.org/web/20260926212011id_/https://www.bls.gov/oes/special-requests/oesm24ma.zip
# FBI 2018 Table 6: ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018/tables/table-6/table-6.xls/output.xls
# ACS 2023 5-year CBSA: B01003, B03001_001/004, B05002_001/013, B19013, B17001_001/002, B03002_004 (Census API, key)
# ILOSTAT: rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_OC2_NB_A&ref_area=...&sex=SEX_T&timefrom=2015&format=.csv
# OECD COFOG: sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NASEC10@DF_TABLE11,/A.USA+JPN............?startPeriod=2022
# World Bank GDP (LCU): api.worldbank.org/v2/country/USA;JPN/indicator/NY.GDP.MKTP.CN?date=2022:2024&format=json
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with xlrd python3 \
    infra/immigration-fiscal/defensive_spending_2026_10_21/defensive.py
```

Deviations from the pre-registration:
- Suppressed detective and bailiff cells are counted as 0 within police plus corrections.
- Police-only and corrections-only outcomes and the border-metro arm were added after the first
  results, and are labelled post-hoc.
- Japan legal-services output and private-security sales were not obtained.
- Crime is from 2018, not 2019, because the 2019 table returns 404.

## Switzerland (plan change 1; descriptive only, no causal or dollar claims)

[DATA: `derived/guard_lawyer_summary.csv` CH column, `derived/ilo_isco54_shares.csv`,
`derived/employment_mix_us_jp_ch.csv`] [SOURCE: `sources_switzerland.md`, each cell quoted there]
Logged 2026-10-21 15:34 JST.

| Per 100 employed (CH: ILOSTAT 2024 employment, 4.89M) | US | Japan | Switzerland |
|---|---:|---:|---:|
| Narrow guard labor (police + prison security + private guards) | 1.77 | 1.29 | 0.93 |
| ISCO-08 group 54, one survey basis | 1.44 | 1.73 | 0.85 |
| Incarcerated | 1.20 | 0.06 | 0.14 |
| Military | 0.83 | 0.34 | professional 0.06; militia beside |
| Lawyers per 100k residents | 395 (ABA) / 223 (employed) | 37 (弁護士) / 65 (wide) | 133 (bar association, independent practice) |

The Swiss counts are mostly FTE, which understates them against headcounts given high part-time
work. The ISCO row, a headcount, agrees: Switzerland has the lowest protective-service share of the
three. Swiss police density is 214 per 100k, 31st of 34 European countries (KKPKS). The private
security count (over 23,000) is a secondary figure from the security trade association.

Employment mix, % of employment (latest ILOSTAT year: US/CH 2025, JP 2023):

| ISIC section | US | Japan | CH |
|---|---:|---:|---:|
| K Finance and insurance | 5.17 | 2.31 | 5.45 |
| M Professional, scientific, technical | 6.19 | 2.29 | 9.34 |
| C Manufacturing | 9.65 | 14.53 | 11.84 |
| O Public administration and defence | 3.74 | 3.69 | 5.24 |
| Q Health and social work | 14.80 | 13.51 | 15.52 |

| ISCO major group | US | Japan | CH |
|---|---:|---:|---:|
| 1 Managers | 11.70 | 1.83 | 8.77 |
| 2 Professionals | 23.00 | 19.80 | 26.64 |
| 5 Service and sales | 14.71 | 30.93 | 13.15 |
| 9 Elementary | 10.38 | 7.40 | 5.82 |

[INFERENCE] Finance's employment share in Switzerland (5.5%) is about the US's (5.2%). On
employment, Swiss productivity is not a story of an unusually large finance workforce. Finance's
**value-added** share was not pulled [GAP], and is where financialization would show if it does.
Switzerland's tilt is toward professionals and manufacturing and away from elementary jobs.

**Intake by origin and skill.** These are nationality counts (BFS STATPOP, end-2024). Switzerland
naturalizes slowly, so nationality and birthplace differ. These counts are not comparable to the US
Mexican-origin share.
- 2.48M foreign nationals, of whom 63% are EU/EFTA.
- Top nationalities: Italy 342k, Germany 330k, Portugal 257k, France 171k, Kosovo 116k, Spain 99k,
  Türkiye 78k, North Macedonia 71k.
- Tertiary-educated share (SAKE 2024): France 62%, Germany 59%, Swiss 37.5%, Italy 31%, third
  countries 30%, Portugal 15%. Kosovo, Serbia and Türkiye are pooled into "other nationalities" in
  the published table [GAP].

**Within-Switzerland contrast** (police-registered suspects per 1,000 residents of each
nationality, 2023, not age or sex adjusted):

| Nationality | Suspects per 1,000 |
|---|---:|
| Swiss | 6.1 |
| Germany | 7.9 |
| France | 8.4 |
| Italy | 9.3 |
| Portugal | 11.7 |
| North Macedonia | 15.4 |
| Bosnia | 16.1 |
| Serbia | 19.5 |
| Kosovo | 20.0 |
| Türkiye | 20.0 |

BFS's age-sex-restricted indicator (men 18–34) finds EU/EFTA rates "similar" to Swiss and other
European rates higher. Its chart cells were not read [GAP]. ILO unemployment (2024) is 3.1% for
Swiss nationals and 7.4% for foreign nationals; no single-nationality split was obtained [GAP].
[INFERENCE] Within Switzerland, the Northwest-EU intake resembles the Swiss on crime and exceeds
them on schooling. The Balkan/Turkish intake shows about three times the Swiss suspect rate before
age adjustment. A "30% foreign yet high trust" reading mostly describes the first group.

## Speculative branch: natural experiments (plan change 1)

[SOURCE: `sources_natural_experiments.md`, 15 entries with quoted cells] Bar: policy-assigned or
as-good-as-random composition change, a stated first stage, and an outcome in {trust, defensive
spending or labor, time use}.

| Design | Outcome | Finding | Clears? |
|---|---|---|---|
| Albarosa & Elsner, WB WP 9913: German 2015–16 refugee dispersal (policy-assigned) | generalized trust; crime worry | per doubling of county asylum seekers: trust .00 (.01); crime worry .01 (.01); caution toward foreigners +.019, significant | Yes, trust |
| Bove, Elia & Ferraresi, JLEO: Italian municipalities, shift-share + historical IV | security budget share | +0.12–0.30 pp per pp immigrants, via fear not crime | Yes (shift-share), spending |
| Ajzenman, Dominguez & Undurraga 2023 AEJ:Applied: Chile, shift-share, F 17.35 | home security; block-guard hiring; victimization | home security +10.03 (4.70); neighbours' security incl. block guards +12.44 (4.06); victimization 3.50 (5.21) n.s. | Yes (shift-share), defensive spending and labor |
| Dinesen & Sønderskov 2015 (Danish registry exposure) | trust | negative, small | No: self-selected residence |
| Dustmann, Vasiljeva & Damm 2019; Couttenier et al. 2019 AER; Lange & Sommerfeld; Gehrsitz & Ungerer; Hangartner et al.; Mariel; Beerli et al. 2021 | votes, crime, hostility, wages, firm outcomes | — | Design yes, outcome outside the bar |

[INFERENCE] Three designs clear the bar.
- The only policy-assigned one (Germany) finds no change in generalized trust or crime worry, but
  more caution toward foreigners.
- Two shift-share designs (Italy, Chile) find defensive spending rising without a matching rise in
  victimization, so through fear or misperception.
- **No design measures natives' time use or attention.** That part of the branch stops here.
- No design involves a US Mexican-origin inflow, and Chile's inflow (Venezuelan, Peruvian, Haitian)
  and Italy's municipal budgets do not transfer to US dollars. No dollar figure is drawn.
- Overlap: a fear-driven precaution response beyond offending is not in the private-security row,
  which is allocated by offending share. It may be partly in the fear row (φ share of the
  willingness-to-pay excess). The split is not identified [GAP].

Log: 15:27 plan change 1 written before Swiss or natural-experiment magnitudes; 15:2x two forks
returned `sources_switzerland.md` and `sources_natural_experiments.md`; 15:34 `defensive.py` rerun
with CH rows and `mix()`; sections written.

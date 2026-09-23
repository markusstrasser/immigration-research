**Verdict:** In 2024 the offences the 40.9m Mexican-origin residents commit against other
US residents cost those victims about **$4.5bn in tangible losses** (medical and mental-health
care, lost earnings and household work, property) and about **$29bn in full victim cost**
(tangible plus pain, suffering and lost quality of life, plus the statistical value of the
lives lost) [CALCULATION: `victim_cost.py` → `derived/arms.csv`]. One-at-a-time sensitivities
put the full cost at **$23–34bn** and the tangible cost at **$2.5–5.5bn**. Stacking every low
or every high choice gives **$15–45bn** full and **$1.3–6.0bn** tangible; this deliberately
wide envelope is not a confidence interval. **Murder accounts for 32% of the full cost**
(26–43% across arms) and 54% of the tangible cost. The central estimate is about 1,020
killings and 402,000 non-fatal violent victimisations of other residents a year. Per member
of the group, that is **$707 full and $110 tangible** a year. The earlier +$1,421 figure is
a relative measure; the difference is explained below. Property crime, on an arrest-share
proxy, adds about **$1.3bn** and is reported separately. The largest single correction is
that McCollister's non-fatal unit costs include a risk-of-homicide premium: 76% of its
aggravated-assault price. Once homicides are counted from death records, that premium counts
the same deaths twice. [FRAMING-SENSITIVE: absent-target frame; the valuation of pain and
statistical life is a willingness-to-award or willingness-to-pay convention, not an
expenditure]

Model self-report: claude-opus-5-5[1m]. Lane `infra/immigration-fiscal/crime_victim_cost_2026_09_23/`,
September 23, 2026.

## Headline

| 2024, $bn a year, cost to other residents | Tangible | Full |
|---|---:|---:|
| **Central** (Miller et al. 2021 victim-only prices) | **4.50** | **28.92** |
| Same incidents, McCollister 2010 prices with risk of homicide removed | 2.47 | 29.58 |
| Same incidents, Miller 2021 non-fatal + US DOT 2024 VSL ($13.7m) for murder | 4.50 | 33.76 |
| One-at-a-time range over all 16 sensitivity arms | 2.47–5.52 | 23.45–34.04 |
| Envelope: every low / every high choice stacked, all three price sets | 1.33–6.01 | 15.41–45.34 |
| NCVS sampling error on the non-fatal part, one SE (understated, see limits) | ±0.21 | ±2.04 |
| Murder's share of the central total | 53.8% | 31.7% |
| Per group member (÷ 40,896,574) | $110 | $707 |
| Per group member aged 12+ (÷ 33,206,257) | $136 | $871 |
| *Separate, not in the totals:* property crime, arrest-share proxy | 1.27–1.38 | same (no QoL priced) |

[CALCULATION: `derived/arms.csv`, `derived/ncvs_sampling_error_central.csv`, `derived/property_proxy.csv`]

The complete account's CBO-informed net cost to other residents is $165–197bn a year
[SOURCE: `research/immigration-complete-annual-account-2026-09-20.md`, Result]. If the full
victim cost were entered as part of its omitted-effects term Z, it would raise that net cost
by about 15–18%. The tangible cost alone would raise it by 2–3%. Whether Z takes the full or
tangible measure is a framing choice this lane does not make. It adds nothing to the memo or
account.

## Result by offence (central)

| Offence | Hispanic-offender incidents, 2024 | Group incidents | Group victimisations | Victims outside the group | Victim-only unit cost, tangible / full (2024$) | Tangible $bn | Full $bn | Share of full |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| Murder | 3,852 | 2,302 | 2,302 | 1,021 | 2,372,050 / 8,963,763 | 2.42 | 9.16 | 31.7% |
| Rape / sexual assault | 71,699 | 42,842 | 46,259 | 33,029 | 9,993 / 210,442 | 0.33 | 6.95 | 24.0% |
| Aggravated assault | 186,821 | 111,630 | 120,455 | 84,110 | 6,615 / 81,697 | 0.56 | 6.87 | 23.8% |
| Simple assault | 549,988 | 328,629 | 354,753 | 243,302 | 3,538 / 20,653 | 0.86 | 5.03 | 17.4% |
| Robbery | 104,374 | 62,366 | 67,220 | 41,295 | 8,027 / 22,289 | 0.33 | 0.92 | 3.2% |
| **Total** | 916,734 | 547,768 | 590,988 | 402,757 | | **4.50** | **28.92** | |

[CALCULATION: `derived/cost_by_offence_central.csv`; victim-group detail in
`derived/cost_by_victim_and_offence_central.csv`]

Across victim groups, non-Hispanic white victims carry $11.52bn of the $19.77bn non-fatal full
cost, Other (non-Hispanic Asian, American Indian, Pacific Islander and multiracial) $3.12bn,
non-Hispanic Black $2.78bn and non-Mexican Hispanic $2.35bn. Among murder victims outside the
group there are 348 non-Mexican Hispanics, 310 non-Hispanic whites, 301 non-Hispanic Black
people and 62 others.

## Method

`victim cost = Σ_offence (incidents committed by the group) × (share with a victim outside the group) × (victim-only unit cost)`

The frame, beneficiary set and crime-harm rule are the brief's. In the absent-target
comparison the group's offences against other residents do not occur. Any replacement
offending, deterrence change or change in other residents' own offending is **not modelled**
[FRAMING-SENSITIVE].

### Incidents

**Non-fatal violence.** The NCVS lane's pooled 2022–2024 victim × perceived-offender matrix,
published BJS tables, provides the input [DATA: `../ncvs_victim_offender_2026_09_18/derived/matrix_pooled_2022_2024.csv`].
1. Hispanic-offender incidents per 2024 = pooled incidents ÷ pooled Hispanic person-years 12+
   (156,526,080) × the 2024 NCVS Hispanic population 12+ (53,539,670), victim row by victim row.
2. **Unknown offender ethnicity (18.3% of incidents)** is allocated in proportion to each
   victim row's known offenders, which raises Hispanic-offender incidents by 22–24%. The low
   arm drops them. Those incidents happened; a known-only count is a lower bound.
3. Incidents are converted to victimisations, the unit the prices use, with each victim
   group's N-DASH victimisations per incident: 1.086 white, 1.061 Black, 1.075 Hispanic and
   1.085 Other.
4. The offence mix is each victim group's own 2022–2024 N-DASH mix, as in the NCVS lane. A
   sensitivity uses the 2019 Hispanic-offender serious-violence share by victim group; it moves
   the total by 0.2%.

**Homicide.** National victims come from CDC WONDER final 2024 deaths, "Assault (homicide)"
GR113-127: 20,162 deaths, of which 3,776 Hispanic, 5,070 non-Hispanic white, 10,294
non-Hispanic Black, 945 non-Hispanic other and 77 not stated (allocated proportionally). The
values were parsed from the homicide lane's cached XML and checked cell by cell against its
CSV [DATA: `derived/wonder_2024_homicide_victims.csv`]. The offender split is the share of
cleared, ethnicity-known 2024 victims whose first recorded offender is Hispanic. The Murder
Accountability Project SHR file was sha256-checked and justifiable homicide excluded. That
share is 0.719 for Hispanic victims (n = 1,509), 0.102 for non-Hispanic white (n = 2,000),
0.049 for non-Hispanic Black (n = 3,279) and 0.109 for non-Hispanic other (n = 193)
[DATA: `derived/shr_p_offender_given_victim.csv`]. Applying those shares to all victims
imputes unsolved and ethnicity-missing cases at the rate observed for the same victim group.
The result is **3,852 killings by Hispanic offenders, 19.1% of 2024 homicide deaths**. As a
cross-check, the Hispanic share of adult murder arrests is 19.8% in FBI 2019 Table 43C
[DATA: `derived/fbi_2019_table43c_adult_arrests.csv`]. A victim is attributed to the first
recorded offender. Among victims whose first offender is Hispanic, 27.5% died in incidents with
more than one offender [DATA: `derived/homicide_inputs_log.txt`]. Arms use the 2019–2024
distribution, cleared cases only (a hard lower bound) and the homicide lane's joint-pair
imputed victim distribution.

**Property crime.** This line uses an explicit arrest-based proxy and stays outside the
totals. The inputs are 2024 NCVS household burglaries (1,103,790), motor-vehicle thefts
(841,120) and other thefts (10,618,790) [SOURCE: BJS *Criminal Victimization, 2024*, table 2].
They are multiplied by the Hispanic share of adult arrests in the FBI 2019 ethnicity panel
(burglary 0.203, larceny 0.142, motor-vehicle theft 0.253), then by the same population share
and by the non-fatal outside-victim share. **Caveat:** arrests are not offences. Property
crime clears at low rates, so arrestees are a selected sample. The panel covers 229.7m people
in agencies that report ethnicity and skews toward high-Hispanic states. The household
survey also misses business victims. The estimate is $1.27bn with Miller prices and $1.38bn
with McCollister prices [CALCULATION: `derived/property_proxy.csv`].

Drug offences, immigration-only offences and other offences without a victim are excluded,
as the rule requires.

### Hispanic to Mexican origin

Neither survey records Mexican origin. **Central: the population share.** Mexican-origin
residents commit the Hispanic incidents in proportion to their share of Hispanic residents
aged 12+, measured within one survey. In CPS ASEC 2025, the rebuilt union reproduces the
complete account's 40,896,574 exactly and contains 33,206,257 people aged 12+. Divided by
55,573,390 Hispanic civilians aged 12+, that gives **s = 0.5975**
[DATA: `derived/target_population_cps2025.csv`]. The alternative applies the NCVS rate
directly to the target population using the NCVS denominator, giving 0.6202 (+3.8%).

**Sensitivity: the ACS institutional-rate ratio.** ACS 2020–2024 5-year PUMS data for men aged
18–39, pooled across nativity, give a Mexican institutional rate of 1.824% and 2.025% for all
listed Hispanic origins. That makes the ratio **0.901**. Reallocating the generic "Other
Hispanic" category, whose 8.6–10.3% rate is a known prison-coding artefact, raises it to
**1.118** [DATA: `../acs_institutional_2026_09_16/acs5_2020_2024_origins.csv`;
`derived/scaling_hispanic_to_mexican.csv`]. Institutionalisation is not offending: this ratio
proxies relative offending and says nothing about detention [SOURCE: detention scope memo].

### Victims outside the group

Victims who are not Hispanic are all other residents. Hispanic victims are other residents
unless they are themselves of Mexican origin. The NCVS and SHR record only whether a victim is
Hispanic, so the in-group share *m* of a Mexican-origin offender's Hispanic victims comes from
an exposure index. ACS 2020–2024 table B03001 gives the Mexican share of Hispanic neighbours
around the average Mexican-origin resident: **0.786 by tract** (84,401 tracts), 0.744 by
county, 0.729 by state and 0.586 nationally [DATA: `derived/mexican_share_of_hispanic_exposure.csv`].
The tract value is central. Co-ethnic sorting within tracts and violence among family and
acquaintances make the true *m* higher, so the estimate leans toward more outside victims
[INFERENCE].

| Share of the group's victims who are other residents | Lower bound (non-Hispanic victims only) | Estimate (plus non-Mexican Hispanics, *m* = 0.786) |
|---|---:|---:|
| Non-fatal violence | 0.596 | 0.682 |
| Homicide | 0.292 | 0.444 |

[CALCULATION: `derived/outside_victim_shares_central.csv`] The lower bound is itself an arm
($23.45bn full). The non-fatal lower bound is one minus the positive-control same-group share:
1 − 0.404 = 0.596. The unknown-offender allocation leaves it unchanged to three decimals.

### Victim-only unit costs, 2024 dollars

| Offence | Miller 2021: tangible / full | McCollister 2010, risk of homicide removed: tangible / full | Excluded from Miller (public services, adjudication and sanctioning, perpetrator work loss) |
|---|---|---|---:|
| Murder | 2,372,050 / 8,963,763 | 1,074,537 / 12,299,701 | 1,029,897 |
| Rape / sexual assault | 9,993 / 210,442 | 7,930 / 296,718 | 1,171 |
| Robbery | 8,027 / 22,289 | 2,384 / 9,633 | 13,189 |
| Aggravated assault | 6,615 / 81,697 | 1,792 / 21,366 | 7,164 (pooled assault) |
| Simple assault | 3,538 / 20,653 | not priced; Miller value carried | 7,164 (pooled assault) |

[CALCULATION: `derived/unit_costs_victim_only_2024usd.csv`; CPI-U 2008→2024 1.456970 and
2017→2024 1.279736]

- **Miller et al. (2021)** [SOURCE: *J Benefit-Cost Anal* 12(1):24–54, doi:10.1017/bca.2020.36,
  Table 5, held PDF; 85 transcribed values gated against its text]. Victim-only means medical,
  mental health, productivity and property loss, plus quality of life. Murder productivity is
  the present value of lost earnings and household work; its quality-of-life value is net of
  work loss, so the two do not overlap. Miller states that its quality-of-life values
  **exclude a risk-of-death component** and that homicides committed during other crimes are
  counted as homicides "to avoid double counting". The design therefore matches a count of
  deaths from death records. Rape and other sexual assault are pooled at Miller's Table 4
  incidence (0.562 rape). Miller prices assault as one category, 84.1% simple assault by
  count. The pooled victim-only cost is split at the NCVS lane's aggravated-to-simple cost
  ratio, *k* = 3.9556: the simple-assault tangible is scaled by injury share and property loss
  is held flat. The split reproduces Miller's pooled cost exactly (gate).
- **McCollister, French & Fang (2010)** [SOURCE: *Drug Alcohol Depend* 108:98–109,
  doi:10.1016/j.drugalcdep.2009.12.002, Tables 3–5, parsed from the PMC JATS record]. For
  murder, tangible = the present value of lifetime earnings ($737,517 in 2008 dollars) and
  full = the Viscusi–Aldy VSL ($8,442,000), which contains the earnings. For non-fatal
  offences, both the earnings-based and the VSL-based **risk-of-homicide** components are
  removed, leaving corrected victim cost plus pain and suffering. The next section explains
  why.
- **US DOT 2024 VSL**, $13.7m, is used for murder in the third price set [SOURCE: DOT
  departmental guidance, via `../homicide_cost_2026_09_18/derived/external_params.json`].
- Government criminal-justice costs, which are already in the fiscal ledger, and offender or
  crime-career costs are excluded throughout. Public services (police, fire, EMS, victim
  services) are government costs and are excluded too.

## The risk-of-homicide double count

McCollister Table 4 builds non-fatal intangible costs from pain and suffering **plus** a
"corrected risk-of-homicide cost". The paper defines that cost as the probability that the
offence leads to a homicide times the VSL. Its Table 3 victim cost carries the matching
earnings-based slice [SOURCE: McCollister 2010, section 2 and Tables 3–5, quoted in
`derived/run_log.txt` gates]. In 2024 dollars:

| McCollister total per offence | Total | Of which risk of homicide (VSL-based) | Of which CJS + crime career |
|---|---:|---:|---:|
| Aggravated assault | 155,924 | 118,871 (76%) | 15,687 |
| Robbery | 61,644 | 25,641 (42%) | 26,370 |
| Rape / sexual assault | 350,802 | 2,083 (0.6%) | 52,001 |
| Murder | 13,087,784 | — | 788,083 |

[CALCULATION: `derived/mccollister_total_decomposition_2024usd.csv`] NCVS assaults are
non-fatal by construction, and this lane counts every death as a murder. Keeping the premium
would count each death once at VSL as a murder and again, in expectation, inside the assault
and robbery prices. **Priced at McCollister's totals as the older lanes used them, the same
outside victims would cost $46.8bn instead of $28.9bn** [CALCULATION: diagnostic in
`derived/run_log.txt`].

Two held lanes inherit this double count:

- `crime_cost_2026_09_16` routes A1, A2 and B price aggravated assault at $155,924 and robbery
  at $61,644 alongside murder. Its "tangible" arm also uses the uncorrected victim cost, which
  contains the earnings-based slice.
- `ncvs_victim_offender_2026_09_18` prices aggravated assault at $155,924 in its social-cost
  tables. More importantly, one anchor of its *k* (10.31) is Miller's pooled assault minus
  McCollister's aggravated-assault total, which includes the risk-of-homicide premium. With
  the premium stripped, that anchor falls to about 1, below the survey's injury (1.88) and
  arrest (1.93) floors. Only the floor bounds *k* from below; no clean upper anchor remains.
  The central *k* = 3.96 is inherited here; *k* = 1.93 lowers the full total by 4%
  [CALCULATION: arm "assault cost ratio k at the NCVS injury/arrest floor 1.93"].

These lanes were not edited. Their re-pricing is left to the parent.

## Positive controls and gates (all PASS; `derived/run_log.txt`)

- **NCVS rate:** 2,177,710 Hispanic-offender incidents / 156,526,080 person-years =
  **13.9128** per 1,000 residents 12+. The same-group share is **0.40444**; both equal the
  NCVS lane.
- **McCollister in 2024 dollars:** murder **$13,087,784** and aggravated assault **$155,924**,
  parsed from the primary tables and inflated, exactly equal the crime_cost lane's values.
- **McCollister Table 4:** pain and suffering + corrected risk of homicide = total intangible
  for all 7 offences used.
- **Miller Table 5:** 85 transcribed values appear in the PDF text. Rows close to published
  rounding: rape, other sexual assault and burglary are each off by $1.
- **Assault split:** reconstructs Miller's pooled victim-only assault cost for both *k* values.
- **Target union:** reproduces 40,896,574.2. WONDER XML parse equals the homicide lane's CSV.
  The SHR sha256 equals its pin. CV2024 Table 2 and FBI Table 43C values are parsed from the
  files.
- **Victimisations per incident:** within the NCVS lane's 1.06–1.09.
- **Hand check:** the white-victim non-fatal cell reproduces by hand ($11.52bn full).
  Re-running `victim_cost.py` leaves `derived/` byte-identical.

## One-at-a-time sensitivities

| Arm | Tangible $bn | Full $bn | Murder share of full | Full per person |
|---|---:|---:|---:|---:|
| **central** | **4.50** | **28.92** | **0.316** | **$707** |
| McCollister 2010 prices, risk of homicide removed | 2.47 | 29.58 | 0.425 | $723 |
| Miller non-fatal + DOT 2024 VSL for murder | 4.50 | 33.76 | 0.414 | $826 |
| assault cost ratio *k* = 1.93 | 4.50 | 27.76 | 0.330 | $679 |
| NCVS unknown-offender incidents dropped | 4.12 | 25.30 | 0.362 | $619 |
| incidents not converted to victimisations | 4.35 | 27.44 | 0.334 | $671 |
| NCVS 2024 alone, not pooled 2022–2024 | 4.80 | 31.91 | 0.287 | $780 |
| 2019 Hispanic-offender serious share by victim | 4.51 | 28.99 | 0.316 | $709 |
| rate × target (NCVS denominator) | 4.67 | 30.02 | 0.316 | $734 |
| ACS institutional ratio 0.901 | 4.06 | 26.06 | 0.316 | $637 |
| ACS institutional ratio 1.118 | 5.03 | 32.34 | 0.316 | $791 |
| Hispanic victims all in-group (lower bound on outside share) | 3.41 | 23.45 | 0.257 | $573 |
| *m* at county exposure 0.744 | 4.72 | 30.00 | 0.326 | $734 |
| *m* at national share 0.586 (ignores geography; implausible) | 5.52 | 34.04 | 0.355 | $832 |
| homicide: SHR 2019–2024 distribution | 4.47 | 28.81 | 0.314 | $704 |
| homicide: cleared cases only | 3.97 | 26.91 | 0.265 | $658 |
| homicide: joint-pair imputed victim distribution | 4.68 | 29.58 | 0.332 | $723 |
| envelope low / high, Miller | 2.36 / 6.01 | 15.41 / 38.97 | | $377 / $953 |
| envelope low / high, McCollister | 1.33 / 3.31 | 16.93 / 39.96 | | $414 / $977 |
| envelope low / high, Miller + DOT VSL | 2.36 / 6.01 | 17.66 / 45.34 | | $432 / $1,109 |

The low envelope stacks: known-only NCVS, no victimisation conversion, ratio 0.901,
non-Hispanic victims only, cleared homicides only and *k* = 1.93. The high envelope stacks:
ratio 1.118, county *m*, joint-imputed homicide victims, NCVS 2024 alone and the NCVS
denominator. Prices account for more of the spread in the full measure. The in-group rule
and the unknown-offender treatment account for more of the spread in incidence.

## Difference from the earlier +$1,421

The crime_cost lane's +$1,421 is **US-born Mexican-origin minus US-born non-Hispanic white,
per adult aged 25–64**. It rests on a prison-stock route: ACS institutional shares × BJS
offence mix ÷ time served. The Mexican-origin absolute level on that route was $2,820 per
adult, of which $841 was corrections and $1,979 victim cost [SOURCE:
`../crime_cost_2026_09_16/RESULT.md` §4]. This lane differs on six counts:

1. **Absolute, not relative.** In the absent-target comparison the group's offences against
   others disappear; no white-level cost is netted out. A white-reference difference answers a
   replacement counterfactual.
2. **Outside victims only.** Offences against the group's own members are excluded. Priced the
   same way, all of the group's victims cost $49.0bn full and $8.5bn tangible; the outside
   share is 59% of that.
3. **Victim-only prices.** Corrections and all criminal-justice costs are excluded, as are
   public services, offender work loss and crime-career costs.
4. **No risk-of-homicide premium on non-fatal offences.** The same outside incidents at the
   older McCollister totals cost $46.8bn, not $28.9bn (×1.62).
5. **Denominator.** Per person of all ages and generations (40.9m), not per US-born adult aged
   25–64. Spread only over the group's 20.6m adults aged 25–64, the all-victim cost would be
   about $2,380 per adult. This is a rough consistency check against the $1,979 victim part of
   the stock route, not a comparable estimate, because it charges all ages' offending to
   adults aged 25–64.
6. **Flow route.** Victimisations and deaths in 2024 are counted directly. Prisoners are not
   amortised over time served.

## Limits, stated plainly

1. **Perceived ethnicity.** NCVS offender ethnicity is the victim's perception. SHR ethnicity
   is police-recorded and missing for about a third of cleared cases. Misperception lands
   directly on the rate.
2. **No Mexican-origin identifier** exists in either survey. The population share assumes
   Mexican-origin and other Hispanic residents offend at the same rate per resident aged 12+
   and have the same victim distribution. The ACS ratio (0.90–1.12) brackets 1 but measures
   institutionalisation, not offending [INFERENCE].
3. **The in-group share of Hispanic victims** comes from residential exposure, not from
   victim-offender data. It leans toward counting too many outside victims (see above).
4. **Sampling error is understated.** The ±10% one-SE figure for the non-fatal part uses BJS
   generalized-variance SEs summed in quadrature across years. The NCVS rotating panel
   correlates adjacent years, and the unknown-offender allocation adds variance that is not
   counted. The Hispanic → Black and Hispanic → Other cells have SEs of 37–39%.
5. **Mixed-offender groups.** From 2021, NCVS codes an incident as Hispanic-offender only if
   every offender was perceived Hispanic. Mixed groups fall under "Other", so the group's
   share of multi-offender violence is understated. Homicide attribution uses the first
   recorded offender.
6. **Unit costs** are willingness-to-award (Miller) or VSL/jury-award (McCollister)
   valuations, not expenditures. The simple/aggravated split rests on an unsourced ratio *k*.
   NCVS counts of rape and sexual assault sit well below other surveys. Both NCVS counts and
   Miller unit costs are used, which is consistent with an NCVS incidence base.
7. **Coverage.** Victims under 12 (outside NCVS) and violence inside prisons and jails are
   omitted. Business victims, fraud and white-collar crime are omitted. Impaired-driving
   crashes are also omitted. Miller prices an impaired-driving crash at $83,743 including its
   risk of death and counts 10,874 impaired-driving deaths in 2017 (Tables 5 and 7), but no
   source here attributes crash involvement by ethnicity. All of these omissions bias the total
   down.
8. **Year mix.** NCVS pooled 2022–2024 rates are applied to 2024 populations. Homicide is
   2024. The property proxy uses 2019 arrest shares, the latest year this lane found in a
   primary table with ethnicity. FBI CDE data after 2019 need an API key.
9. **Instrument bias.** This lane was produced through an LLM; see `notes/llm-bias-caveat.md`.
   The choices that move the number most are explicit arms. The risk-of-homicide correction
   lowers the cost; the unknown-offender allocation and the non-Mexican-Hispanic share raise
   it.

## Covered / skipped

**Covered:**

- The brief, the crime-harm rule, the detention/crime scope memo and the complete account's
  frame and Z term.
- NCVS lane derived files: matrix, rates, populations, N-DASH, simple-assault prices, the
  Miller price set and the 2019 crime-type matrix. Its cached Miller 2021 PDF text and CV2024
  Table 2 were also used.
- Crime_cost lane unit-cost rows as the positive control. The McCollister primary tables were
  re-parsed from PMC.
- Homicide lane SHR file, WONDER XML, joint-imputed matrix and DOT VSL parameter.
- ACS institutional origins CSV, CPS ASEC 2025 through the ledger builder, and ACS B03001 by
  tract (51 state calls).
- FBI 2019 Table 43C, fetched and parsed.

**Skipped, with reasons:**

- *Homicide offenders by ethnicity from FBI CDE for 2024.* The CDE API needs a key, as the
  homicide lane found. The SHR compilation already carries 2024 offender ethnicity, so the
  gap did not bind.
- *Post-2019 arrest shares by ethnicity.* The same CDE key barrier applies. The property proxy
  uses 2019 and says so.
- *NCVS microdata.* ICPSR requires a login (NCVS lane). No single-offender, relationship or
  mixed-group reallocation was possible beyond the published tables.
- *Property crime in the totals.* It is reported as a bounded, separate proxy, as the brief
  allows.
- *Drug and immigration-only offences.* No victim price, per the rule.
- *Impaired driving, child maltreatment, fraud and in-custody violence.* No ethnicity-matched
  incidence source was available here; each is listed as an omission above.
- *Editing memos, the confidence ladder, the INDEX or the older lanes' prices.* These were out
  of scope. The double-count finding is reported to the parent instead.

## Sources

| Item | Source |
|---|---|
| Violent incidents by victim and perceived offender, 2022–2024; offender marginal; NCVS population 12+ | BJS *Criminal Victimization* 2022–2024 data tables (table 13 and appendix tables), via `../ncvs_victim_offender_2026_09_18/derived/` |
| Victimisations and offence mix by victim group | BJS N-DASH static CSV `racehispanicorigin_all.csv`, via the NCVS lane |
| 2024 property victimisations | BJS *Criminal Victimization, 2024* (NCJ 310547), table 2, `cv24t02.csv` in the NCVS lane cache |
| Homicide deaths 2024 by Hispanic origin and race | CDC WONDER D158, Underlying Cause of Death 2018–2024, GR113-127, cached XML in `../homicide_cost_2026_09_18/_cache/` |
| Homicide victim × first offender, 2019–2024 | FBI Supplementary Homicide Reports, Murder Accountability Project compilation `SHR76_25a.csv` (sha256 `eeedbf5e…b88a12`), murderdata.org |
| Adult arrests by ethnicity, 2019 | FBI *Crime in the United States 2019*, Table 43C, ucr.fbi.gov (parsed .xls) |
| Unit costs, 2008$ | McCollister, French & Fang (2010), *Drug Alcohol Depend* 108(1–2):98–109, doi:10.1016/j.drugalcdep.2009.12.002, PMC2835847 (OAI JATS record) |
| Unit costs, 2017$ | Miller, Cohen, Swedler, Ali & Hendrie (2021), *J Benefit-Cost Anal* 12(1):24–54, doi:10.1017/bca.2020.36, Tables 4, 5, 7 (held PDF) |
| Simple-assault injury scaling and *k* | `../ncvs_victim_offender_2026_09_18/derived/simple_assault_unit_cost.csv`, `miller2021_price_set.csv` |
| VSL | US DOT, *Departmental Guidance on Valuation of a Statistical Life*, 2024 base year $13.7m, via `../homicide_cost_2026_09_18/derived/external_params.json` |
| CPI-U | BLS CUUR0000SA0 annual averages, via `../ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv` |
| Target population | CPS ASEC 2025 public-use file, rebuilt with `../gen_ledger_extension_2026_09_16/extend_ledger.py` masks |
| Institutional-rate ratio | ACS 2020–2024 5-year PUMS, `../acs_institutional_2026_09_16/acs5_2020_2024_origins.csv` |
| Mexican share of Hispanic neighbours | ACS 2020–2024 5-year detailed table B03001 by tract, Census API |

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
L=infra/immigration-fiscal/crime_victim_cost_2026_09_23
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 $L/fetch_sources.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/target_population.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acs_exposure.py   # Census key, 51 calls, cached
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/homicide_inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/victim_cost.py
```

Scripts: `fetch_sources.py` (McCollister JATS record, FBI Table 43C, source manifest),
`target_population.py`, `acs_exposure.py`, `homicide_inputs.py` and `victim_cost.py` (model,
gates and every arm). Raw pulls are in `_cache/` (ignored), with sha256 values in
`derived/source_manifest.csv`. `derived/` holds every intermediate: `target_population_cps2025.csv`,
`mexican_share_of_hispanic_exposure.csv`, `scaling_hispanic_to_mexican.csv`,
`shr_p_offender_given_victim.csv`, `shr_victim_by_first_offender.csv`,
`wonder_2024_homicide_victims.csv`, `unit_costs_victim_only_2024usd.csv`,
`mccollister_total_decomposition_2024usd.csv`, `cost_by_victim_and_offence_central.csv`,
`cost_by_offence_central.csv`, `outside_victim_shares_central.csv`,
`ncvs_sampling_error_central.csv`, `arms.csv`, `property_proxy.csv`,
`fbi_2019_table43c_adult_arrests.csv` and the three console logs.

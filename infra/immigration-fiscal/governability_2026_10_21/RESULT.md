claude-opus-5-5

# Governability and policy costs of immigration as a political issue — lane 2026-10-21

**Verdict:** No governability or policy channel here yields a defensible dollar figure, and every one that runs through government action is response-mediated, so none is added to the group's cost. Sizes, what each holds fixed, and identification [INFERENCE on data cited per section]:

| Q | Channel | Size found | Identification | Dollars |
|---|---|---|---|---|
| 1 | Migration policy uncertainty (BBD) | US index 545 in 2024, 1,663 in 2025 (1995–2011 = 100); UK 2,347, Germany 805 in 2025 | Coverage count; the only category-specific VAR (Fraser & Üngör 2019) finds no significant output decline | None: BBD's overall-index elasticities do not transfer to a self-normalized sub-index |
| 2 | Cordon-sanitaire governability (ParlGov, 35 countries, 1980–2023) | Primary measure: formation +6.6 days (SE 4.1), duration −1% (SE 9%) per 10 pp, both null. Four-country named-cordon check: formation +29 days (SE 13), cabinets 38% shorter (−0.48 log, SE 0.12), with SEs overstated as precise | Country and decade FE; vote share endogenous; the cost sits in the other parties' exclusion rule | None |
| 3 | Salience: composition vs volume | Literature: salience follows inflow shocks and media coverage (Hatton; Carvalho et al. 2024); own panel not run (data access) [GAP]. Switzerland: intake 63% EU/EFTA (Germans 58% and French 61% tertiary vs Swiss 37%), yet 40% named immigration a top worry in 2014 and the mass-immigration initiative passed with 50.3%. Within-country, origin drives individual penalties: ex-Yugoslav and Turkish naturalization applicants get +13–15 pp no votes (Hainmueller & Hangartner 2013) | Associational; the naturalization result is a natural experiment | n/a |
| 4 | Canada 2022–24 | ~1M+/yr growth, ~3%; rents +8.2% y/y (Oct 2023, 40-year high); "too much immigration" 27→44→58%; PR target 500k→395k | Case; BoC does not quantify the rent effect | None; the rent effect is an economic channel (priceable with an elasticity not found), the reversal is response-mediated |
| 5 | Restrictionist vs economic-populist governments | Meloni, PiS and Fidesz improved balances vs peers (+0.4 to +1.3 pp) with growth ≈ peers; Trump I −2.1 pp; the worst cases are economic populists (Venezuela, Ecuador, Mexico) | 11 descriptive cases, not causal | None [FRAMING-SENSITIVE] |

Both directions, briefly. The cost case rests on record formations where a large party is shunned (Belgium, the Netherlands, Sweden, Germany), coverage-driven uncertainty at many times its base, and Canada, where a selected intake still broke consensus once it outran housing. The small case rests on the null primary governability measure, ordinary formations wherever the excluded party was brought in, no measured output effect of migration uncertainty, and restrictionist governments that were not fiscally reckless. The evidence favors the small reading on fiscal and output outcomes. The governability strain is real where a cordon binds, and its size depends on a choice by the other parties. Ladder 102 is not recomposed.

Provenance: [DATA] published series and tables pulled by the scripts here · [SOURCE: per-question citations below] · [INFERENCE] verdicts · [UNVERIFIED] until each block says otherwise.

Scope: operator ask 2026-10-21 (via team lead). Five questions: (1) BBD immigration policy-uncertainty, (2) cordon-sanitaire vote share vs cabinet governability (ParlGov), (3) salience vs composition or volume of arrivals, (4) Canada 2022–24 housing case, (5) policy record of immigration-restricting vs economic-populist governments.

Attribution rule: report the channel's size first, then the share plausibly linked to immigration with its identification. Any effect that runs through a political response is labelled **response-mediated** and is never added to the group's cost. Ladder 97/102 (populism→GDP chain) stays withdrawn; nothing here recomposes it.

## Log (times from `date`)

- 2026-10-21 15:09 JST stub written (time from the first `date` call, made right after the stub).
- 2026-10-21 15:10 JST pre-registration written below, before any series, coefficient or table for Q1–Q5 was fetched. Honest limit: the instrument has training-data priors on several of these magnitudes (BBD's VAR responses, FST's headline, Canada's 2023 population growth); the methods below were fixed without looking them up here.

- 2026-10-21 15:12 JST Q1 appended. 15:14 Q2 appended (leave-one-out added post hoc, labelled). 15:16 Q3–Q5 appended; Q3 fell back to literature (Eurobarometer country-year MIP not a small download). Verdict written.
- 2026-10-21 15:17 JST `rerun_lane.py` IDENTICAL 10/10, exit 0. Not committed (dispatch: analysis agents do not commit).
- 2026-10-21 15:18 JST **plan change (operator, relayed 15:11 and 15:13 JST):** Q3 gains Switzerland as a named case. Report, before looking up magnitudes: (a) the composition of the foreign population by origin (BFS: EU/EFTA vs third countries; top nationalities, i.e. Germany, Italy, Portugal, France vs former Yugoslavia/Kosovo, Turkey) with skill levels by origin group; the foreign-born share is a headline only; (b) salience (the gfs.bern/UBS Worry Barometer "foreigners" item, if obtainable) and vote outcomes (2014 mass-immigration initiative, 2020 limitation initiative, SVP vote share) against that mix; (c) the within-Switzerland contrast by origin, if any source gives salience, campaign targeting or vote-relevant outcomes by origin group (the 1990s–2000s Balkan-origin debate, SVP campaigns); (d) whether direct democracy channels the issue without cordon-style exclusion (SVP inside the consensus cabinet). Standing rule from 15:13: for every country compared, report origin and skill mix, never the foreign-born share alone. Applied retroactively to the Canada case.
- 2026-10-21 15:20 JST Switzerland block appended to Q3 (q3_switzerland.py, BFS SAKE asset 35367255 + STATPOP 2024); Canada origin/skill note added; verdict row 3 updated. 15:21 `rerun_lane.py` IDENTICAL 13/13, exit 0.

## Pre-registration (2026-10-21 15:10 JST, before data)

**Q1 policy uncertainty.**
- Data: BBD US categorical EPU workbook (policyuncertainty.com), the immigration column if one exists; the US Migration Fear Index (FRED USEPUFEARINDX, already cited by the attention lane) as context only.
- Report: monthly level, 1985–latest mean, the 2024 mean, the top 5 months, and the immigration index's ratio to the overall EPU in 2024.
- Dollar rule: compute an output effect only if BBD (or a peer-reviewed paper) estimates the macro or firm response to the immigration category itself, or states that the overall-index elasticities apply to categories. Otherwise no dollars. The overall-index VAR responses may be quoted as context, with the reason they do not transfer.

**Q2 coalition governability (ParlGov, European/OECD parliamentary democracies, elections 1980–latest).**
- Units: one row per election (formation), one row per cabinet (duration).
- Regressor X1 (primary): vote share in the preceding election of ParlGov family "Right-wing" (radical right) parties that held no cabinet post in that country in the previous 20 years ("excluded radical right"). X2: X1 plus communist/radical-left parties (ParlGov "Communist/Socialist") under the same never-governed rule ("excluded both sides"). A named-cordon list (BE VB 1991+, FR FN/RN, DE AfD, SE SD 2010–2021) is reported as a small-sample check only.
- Outcomes: (a) formation days = election date to start date of the first cabinet whose election_id is that election (log(1+days)); (b) cabinet duration in days = start to the next cabinet's start in that country, log; (c) early election = next election held more than 180 days before the statutory term ends (statutory term table hard-coded, [TRAINING-DATA]).
- Specification: OLS, country FE and decade FE, SE clustered by country. Report per 10 pp of X. Two versions: without controls, and with the effective number of parliamentary parties (ENPP, from seat shares). ENPP is partly a mediator (an excluded party mechanically raises fragmentation), so the no-control version is the total association, the ENPP version the residual association.
- Not identified: vote share is endogenous to the grievances, fragmentation and crises that also make governments hard to form; no instrument is used. Legislative output: only if a cross-country law count is available in a small download; otherwise [GAP].

**Q3 salience: composition vs volume.**
- Primary data: Standard Eurobarometer "two most important issues facing (OUR COUNTRY)", immigration %, country × year; volume = Eurostat immigration (`migr_imm1ctz`) per 1,000 residents; composition = first-time asylum applicants (`migr_asyappctza`) as a share of immigration, and non-EU share of immigration. Country and year FE, SE clustered by country; coefficients standardized (per 1 SD within-country).
- If country-year Eurobarometer MIP data are not obtainable as a small download, fall back to the published literature (Dennison & Geddes 2019 and successors), quoted, plus Gallup MIP for the US.
- Named cases, descriptive: Canada (points-selected intake, low salience to ~2023), Gulf states and Singapore (high foreign shares, no citizenship path). For each, the share and the salience evidence found; no regression.
- The test cannot separate composition from the elite framing that follows a type of flow (Alrababa'h et al. 2024 is the warning).

**Q4 Canada 2022–24.** Statistics Canada population estimates (permanent and non-permanent residents, quarterly), rents (CPI rent index or CMHC average rent), house prices, salience (Environics Focus Canada "too much immigration" series; any MIP-type poll), and the 2023–24 reversals (study-permit cap, levels plans). Report the timeline and any published estimate of the rent or price effect of the population surge (Bank of Canada, CMHC, peer-reviewed). Attribution: the housing effect of population growth is an economic channel; the policy reversal is response-mediated.

**Q5 backlash-government policy by type.** Cases: immigration-restricting (Meloni 2022–, PiS 2015–23, Fidesz 2010–, Trump I 2017–21) and economic populists from FST's list (left-wing; e.g. Kirchner, Chávez/Maduro, Syriza, AMLO). Outcomes from IMF WEO (datamapper API): general-government net lending % GDP and real GDP growth, tenure average minus the 5 years before, and growth relative to a named peer group (euro area, CEE EU members, advanced economies, Latin America). Spreads quoted from published sources only. FST's own left/right split quoted from the paper. Descriptive; no causal claim; [FRAMING-SENSITIVE] on which governments count as which type.

## Q1 Policy uncertainty (appended 2026-10-21 15:12 JST)

[DATA: derived/q1_migration_epu_annual.csv, derived/q1_migration_epu_summary.csv; CALCULATION: q1_uncertainty.py]

**The series.** BBD's US categorical EPU has no immigration category: the workbook's 11 columns are monetary, fiscal, taxes, spending, health care, national security, entitlements, regulation, financial regulation, trade, sovereign debt. "immigration policy" is one term in the regulation term list (policyuncertainty.com/categorical_terms.html). The immigration series BBD publish is separate: the **Migration Policy Uncertainty Index** (and the Migration Fear Index) for the US, UK, Germany and France, quarterly from 1990. Site definition, quoted: "We construct our Migration Policy Uncertainty Index in the same way, except we instead count articles with at least one term from each of M, E, P and U term sets. We normalize each index to a mean value of 100 from 1995 to 2011." [SOURCE: https://www.policyuncertainty.com/immigration_fear.html]

| Index (1995–2011 = 100) | 2015 | 2016 | 2024 | 2025 | Peak quarter |
|---|---|---|---|---|---|
| US migration policy uncertainty | 134 | 400 | 545 | 1,663 | 2,068 (2025Q1) |
| UK | 524 | 2,215 | 1,511 | 2,347 | 3,042 (2024Q4) |
| Germany | 222 | 577 | 802 | 805 | 1,353 (2025Q1) |
| France (ends 2019Q4) | 304 | 478 | — | — | 585 (2016Q4) |
| US migration fear | 127 | 168 | 201 | 328 | 432 (2026Q1) |

The level since 2016 is a large multiple of the 1995–2011 base in all four countries, and the US index in 2025 is 3× its 2024 level (the enforcement drive and its litigation). These are ratios to a small base: the workbook does not give article counts, so the index cannot say what share of all policy-uncertainty coverage is about migration. [GAP: raw article shares]

**Dollar rule outcome: no dollar figure.** BBD's macro responses are estimated for the overall index. Quoted from the NBER version: "a policy uncertainty innovation equivalent to the actual EPU increase from 2005-06 to 2011-12 foreshadows declines of about 6% in gross investment, 1.2% in industrial production and 0.35% in employment … These VAR results are not necessarily causal" (a 90-point shock to the overall index). [SOURCE: https://www.nber.org/papers/w21633] They do not state that these apply to sub-indices, and a point on a migration index normalized to its own tiny base is not a point on the overall index. The one study that estimates responses to the migration indices themselves, Fraser & Üngör (Otago WP, 2019), finds mixed and mostly null output effects. Quoted from its abstract: "both indices are associated with decreases in industrial production in all countries except Germany" and "innovations in the migration related uncertainty indices do not foreshadow significant declines in output"; its panel regressions find no significant link to GDP growth, and fear-index innovations go with *lower* unemployment. [SOURCE: https://ourarchive.otago.ac.nz/esploro/outputs/workingPaper/Migration-Fears-Policy-Uncertainty-and-Economic/9926479251701891] So the pre-registered condition fails: the overall elasticities do not transfer, and the category-specific estimate is a recursive bivariate VAR (not causal) with no significant output effect. [INFERENCE]

**Steelman, cost side.** Uncertainty about the rules for hiring foreign workers is the textbook case of the Bernanke option-value channel: H-1B, H-2A/B and TPS rules change by executive action and court order, and sectors that depend on them (agriculture, construction, meat-packing, tech) delay hiring and capital. A national VAR would miss this sectoral cost. **Steelman, small side.** The aggregate tests that exist find nothing, the index levels are driven by coverage of a contested topic rather than by measured business uncertainty, and the 2025 spike is coverage of a policy response (response-mediated by construction). [GAP] A sectoral design (H-2A-dependent counties' hiring around rule changes; firm 10-K mentions of immigration rules) is the test that could find a cost; none was found in this bounded search.

Attribution: the index measures uncertainty about **policy**, so any cost it carries is response-mediated (it exists because government changes or might change the rules), and none of it is added to the group's cost. What it holds fixed: nothing; it is a coverage count.

## Q2 Coalition governability (appended 2026-10-21 15:14 JST)

[DATA: ParlGov development release, data through 2023-06 (parlgov.org/data/parlgov-development_csv-utf-8/); derived/q2_elections.csv, q2_cabinets.csv, q2_coefficients.csv; CALCULATION: q2_governability.py, run with `--with statsmodels`]

Sample: 35 countries (ParlGov's EU/OECD set), elections and cabinets from 1980. Deviation from the pre-registration: Switzerland and Cyprus are dropped because their executives are not formed by parliament (decided before the regressions ran, when the country list was first printed). Median formation 30 days; median cabinet 599 days; 34% of elections came early.

Coefficients per 10 points of vote share, country and decade fixed effects, SE clustered by country:

| Outcome | Excluded radical right (X1, primary) | X1 + ENPP | Excluded both sides (X2) | X2 + ENPP | Named cordon list (4 countries) | Cordon + ENPP |
|---|---|---|---|---|---|---|
| Formation, days (n 394) | +6.6 (4.1) | +3.5 (3.3) | +5.0 (2.7) | +2.5 (2.3) | +28.6 (12.8) | +24.1 (11.6) |
| Formation, log(1+days) | +0.17 (0.12) | +0.11 (0.11) | +0.10 (0.08) | +0.05 (0.08) | +0.15 (0.40) | +0.06 (0.37) |
| Cabinet duration, log (n 640) | −0.01 (0.09) | +0.03 (0.09) | −0.04 (0.06) | −0.02 (0.06) | **−0.48 (0.12)** | −0.44 (0.13) |
| Early election, prob. (n 371) | +0.04 (0.05) | +0.02 (0.05) | +0.07 (0.04) | +0.06 (0.04) | +0.01 (0.07) | −0.01 (0.07) |

X1 has mean 3.9 and SD 6.4 points across elections; X2 has mean 8.2 and SD 9.2.

**Reading.**
- The pre-registered primary measure finds no reliable association. At the point estimate, a 10-point rise in the vote share of never-governing radical-right parties goes with formation about a week longer (t 1.6), unchanged cabinet duration, and early elections 4 points more likely; none is significant. Adding fragmentation (ENPP) halves the formation coefficient: most of the association runs through more parties in parliament. [INFERENCE]
- The named-cordon check (Belgium VB, France FN/RN, Germany AfD, Sweden SD 2010–21) gives formation +29 days and cabinets about 38% shorter per 10 points. Each sign holds when any one of the four countries is dropped. Duration ranges from −0.38 (SE 0.09) without Belgium to −0.56 (SE 0.18) without Sweden; formation from +19 days (SE 12) without Germany to +40 (SE 10) without France. This leave-one-out was added after seeing the main run. With four treated clusters, cluster-robust SEs are too small (Conley–Taber, MacKinnon–Webb), so these t-statistics overstate precision. [INFERENCE]
- Measurement limit: ParlGov sometimes records an outgoing government continuing after an election as a new non-caretaker cabinet starting on election day. Belgium 2019 shows 0 formation days, when the actual formation took until October 2020. This biases formation toward zero exactly where the cordon is strongest.
- Legislative output: no cross-country law count was found as a small download. [GAP] (Comparative Agendas law series exist for a few countries; the attention lane used them for agenda shares.)

**What it holds fixed and what it does not identify.** Country fixed effects remove stable national institutions, and decade effects remove common trends. Vote share is not assigned at random. The crises, fragmentation and distrust that raise excluded-party votes also make cabinets hard to form, so none of this is the causal effect of the cordon or of the party. The cordon itself is a choice by mainstream parties: a cost that runs through it is **response-mediated** twice, through voters and through the other parties' exclusion rule. Neither link is caused by immigrants' behavior.

**Steelman, cost.** Belgium 2010–11 (541 days) and 2019–20, the Netherlands 2017 and 2021 (225 and 299 days), Sweden 2018 (131 days) and Germany 2017 (171 days) are the longest formations in their countries' records. Each came with a record vote for a party that others refused to govern with. Caretaker periods freeze budgets and reform. **Steelman, small.** The broad measure shows nothing. Where the excluded party entered government or a support deal formation was ordinary: Italy 2022 (27 days), Sweden 2022 (36), Denmark 2001–2019 with the Danish People's Party at 12–21% (7–22 days), and Norway 2005–2013 with the Progress Party at 16–23% (35–37 days) [DATA: derived/q2_elections.csv]. That points the cost at the exclusion rule, which the other parties can change, more than at the vote. Formation days are not output. Belgium grew 2.7% in 2010 and 1.9% in 2011, against 2.1% and 1.7% for the euro area (IMF WEO, `_cache/imf_ngdp_rpch.json`). **Dollar figure: not defensible.** No study here links formation days or cabinet duration to output with identification.

## Q3 Salience: composition vs volume (appended 2026-10-21 15:16 JST)

**Route taken: the pre-registered fallback.** Country-year Eurobarometer "most important issue" data are distributed as GESIS survey files, which need registration, and no compiled country-year table was found as a small download. The panel regression was therefore not run. [GAP] What follows is the published literature and the named cases. No coefficient here is this lane's own.

- **Hatton (IZA DP 10838, 2017; EJPE 2021).** Salience and preference are different things and move differently. Quoted: "the salience of immigration depends positively on short run immigration shocks but it declines when other issues, such as unemployment, come to the forefront of public attention"; "anti-immigration preferences are positively associated with the stock of immigrants and negatively with the current inflow." Also quoted: "Across all respondents in 2008, 2010, 2012 and 2014, 7.0 percent ranked immigration as the first or second most important issue for the country but only 2.6 percent ranked it as first or second most important for them personally." Salience follows inflow **volume** shocks, and it is a judgment about the country more than about one's own life. [SOURCE: https://docs.iza.org/dp10838.pdf]
- **Carvalho, Duarte & Ruedin (EJPR 2024)**, 7 West European countries, 2002–09. Salience tracks media coverage six months earlier, controlling for foreign-population share and asylum applications. Quoted: "Media effects on the importance associated with immigration in Europe during the 2000s appear substantial and seem to show greater relevance than environmental factors, like gross domestic product (GDP) growth or changes in the size of the foreign population." One SD of immigration news share goes with +0.18–0.23 SD of salience. [SOURCE: https://doi.org/10.1111/1475-6765.12683]
- **Composition in the published panels.** The asylum share of inflows enters only as a control, so no study found here separates the skill or legal-status mix of arrivals from their number. The Swiss quasi-experiment (Alrababa'h et al. 2024, cited in the attention lane) shows that anti-immigrant voting can rise with no economic or perceived-threat effect, which points to framing over either composition or volume.
- **Canada (named case): volume, through housing, beats composition.** The intake was points-selected for permanent residents, but most of the 2022–24 surge was temporary residents (students and workers; Q4). Environics' question measures preference, not salience. The agreement that there is "too much immigration" rose from 27% (2022) to 44% (2023) to 58% (2024). Among those agreeing, housing was the reason given by 15% → 38% → 33%, while "threat to culture/values" fell from 24% to 8% (2023) and was 10% in 2024. Students as a reason: 3%. Quoted (2023): "there has been no comparable change in what Canadians think about immigrants themselves." Canada's long low-concern period is therefore no evidence that selection prevents backlash. Opinion turned within two years once volume outran housing, and the reasons people gave were about numbers, not about who came. [SOURCE: https://environicsinstitute.org/wp-content/uploads/2024/10/focus-canada-fall-2023-canadian-public-opinion-about-immigration-refugees-final-report.pdf ; https://environicsinstitute.org/wp-content/uploads/2025/11/final-report94fae631-0284-4ba5-b06a-e0aeeab5daf3.pdf ; https://www.cbc.ca/news/politics/immigration-liberals-miller-trudeau-1.7364302]
- **Gulf states and Singapore (named cases): not measured here.** The Gulf monarchies hold no competitive national elections and run no comparable most-important-issue series, so salience cannot be compared. Singapore's 2011 general election and the 2013 protest against the Population White Paper [TRAINING-DATA, not verified this session] are the counter-case: high salience with a no-citizenship-path, work-permit regime. That fits the volume reading. [GAP: Singapore IPS or REACH survey series]

- **Switzerland (named case, added by plan change 15:18 JST; appended 15:20 JST).** [DATA: derived/q3_switzerland_composition.csv, derived/q3_switzerland_education.csv; CALCULATION: q3_switzerland.py]
  - *Headline only:* about 30% of residents are foreign-born. Foreign nationals numbered 2.48M at end-2024 (BFS STATPOP).
  - *Origin mix, end-2024 (BFS STATPOP; share of foreign nationals):* EU/EFTA 62.9%: Italy 13.8%, Germany 13.3%, Portugal 10.4%, France 6.9%, Spain 4.0%, Austria 1.9%. Non-EU Europe 19.4%: Kosovo 4.7%, Türkiye 3.2%, North Macedonia 2.8%, Ukraine 2.8%. Asia 8.5%, Africa 5.1%, Americas 3.7%. The 2024 net inflow was also mostly EU/EFTA; SEM's top net-migration nationalities were Germany 14%, France 11%, Italy 11% and Portugal 7%. SEM, quoted: employment was "lediglich zwischen 8 und 11 %" of third-country immigration, family reunification 41–58%. [SOURCE: https://www.bfs.admin.ch/bfs/de/home/statistiken/bevoelkerung/migration-integration/auslaendische-bevoelkerung/zusammensetzung.html ; https://www.sem.admin.ch/dam/sem/de/data/publiservice/statistik/auslaenderstatistik/monitor/2024/statistik-zuwanderung-2024-jahr.pdf]
  - *Skill mix by origin, 2024 (BFS SAKE, permanent residents, annual means; share with tertiary education / with lower secondary only):*

    | Group | Tertiary | Lower secondary only |
    |---|---|---|
    | Swiss | 36.6% | 13.9% |
    | Germans | 58.4% | 5.8% |
    | French | 60.9% | 11.4% |
    | Italians | 29.9% | 36.1% |
    | Portuguese | 15.2% | 59.5% |
    | EU/EFTA, all | 42.1% | 25.9% |
    | Third countries, all | 28.9% | 44.5% |

    The SAKE table does not split third countries by nationality, so Kosovo and Türkiye cannot be shown separately here. [GAP] The base includes residents still in school, so lower-secondary shares include teenagers.
  - *Salience:* in the Credit Suisse/UBS Worry Barometer (gfs.bern; voters pick 5 of about 34 worries), "Zuwanderung" was named by 40% in 2014, the year of the mass-immigration vote, "halved" by 2022, at 23% in 2022 and 26% in 2024, with refugees separately at 28% (2024). gfs.bern, quoted: "Steigt die Arbeitslosigkeit, die Zuwanderung oder auch die Prämienlast, so steigen auch die jeweiligen Sorgen." [SOURCE: https://www.beobachter.ch/politik/klimawandel-energieknappheit-und-zuwanderung-die-sorgen-der-schweizerinnen-und-schweizer-593662 ; https://www.gfsbern.ch/wp-content/uploads/2023/11/credit-suisse-sorgenbarometer-2023.pdf ; https://www.gfsbern.ch/wp-content/uploads/2024/12/ubs-sorgenbarometer-2024_report-de.pdf]
  - *Votes:* the mass-immigration initiative (9 Feb 2014) passed with 50.3% yes (1,463,854 to 1,444,552; turnout 56.57%). The limitation initiative (27 Sep 2020), which would have ended free movement with the EU, failed with 61.7% no (turnout 59.5%). Both targeted **EU free movement**, the high-skill-heavy flow. [SOURCE: https://www.ejpd.admin.ch/de/volksinitiative-gegen-masseneinwanderung ; https://www.ejpd.admin.ch/de/begrenzungsinitiative]
  - *Within-Switzerland origin contrast:* Hainmueller & Hangartner (APSR 2013) study 2,400 secret-ballot municipal naturalization referendums, 1970–2003. Quoted: "The average proportion voting 'no' in the naturalization referendums is about 13-15 percentage points higher for applicants from (the former) Yugoslavia and Turkey compared to observably similar applicants from richer northern and western European countries … but no disadvantage for applicants from southern Europe"; "origin alone accounts for about 40% of the within-municipality variation"; "discrimination against applicants from Turkey and (the former) Yugoslavia increases following the rapid growth of these groups during the 1990s, discrimination against immigrants from southern European origins abates as the relative size of this group decreases." [SOURCE: https://doi.org/10.1017/s0003055412000494] Alrababa'h, Beerli, Hangartner & Ward (2024) show the EU border opening, a mainly EU, cross-border-commuter flow, raising anti-immigrant votes by 6 pp with no economic or perceived-threat effect (attention lane D).
  - *Direct democracy without exclusion:* the SVP has sat in the seven-member consensus Federal Council throughout. It holds two seats under the "magic formula" and won about 28% in 2023 [TRAINING-DATA, not verified this session]. Immigration is decided by initiative rather than by a coalition veto. Parliament then implemented the 2014 result as a weak domestic-hiring preference to keep the EU treaties [TRAINING-DATA]. Q2 excludes Switzerland because there is no formation to measure. The Swiss case therefore shows no governability cost of the cordon kind; the cost shows up as treaty uncertainty with the EU after 2014. [GAP: Swiss EPU or a bilateral-uncertainty series]
  - *What Switzerland shows [INFERENCE].* (i) National salience and vote outcomes rose against an intake that is majority EU and, among Germans and French, more tertiary-educated than the Swiss. So in Switzerland backlash does not need a low-skill or irregular mix; volume, and coverage of it, is enough (2014: 40% worried, vote passed). (ii) At the individual level, voters discriminate sharply by origin. Ex-Yugoslav and Turkish applicants face a 13–15 pp no-vote penalty that tracks those groups' growth, while southern Europeans face none. Composition therefore shapes *whom* the backlash targets, and national salience follows *how many* arrive. (iii) The US Mexican-origin case is closer in skill mix to Switzerland's Portuguese and third-country groups than to its Germans. No Swiss study found gives national salience or vote shares split by the origin of local foreigners. [GAP: municipality-level 2014 yes share against local origin mix, BFS commune data]
- **Origin and skill mix for Canada (standing rule, applied 15:20 JST).** Permanent admissions are points-selected. The 2022–24 surge was mostly temporary residents: international students were "about one-third of total newcomers in 2022" (BoC). India was the largest source of both students and PRs [TRAINING-DATA, not verified]. No skill-by-origin table was pulled. [GAP: IRCC PR and study-permit holders by citizenship; StatCan education of recent immigrants by origin]

**Reading [INFERENCE].** The evidence found favours volume shocks and media coverage over composition as drivers of salience. Composition has not been tested as a separate regressor in any source found. The idea that selection buys political peace is supported by neither Canada nor Switzerland: both turned against majority-skilled, selected or EU intakes once volume rose. Switzerland adds that composition decides whom voters penalize. Ex-Yugoslav and Turkish applicants face a 13–15 pp naturalization penalty that tracks those groups' growth; southern Europeans face none. The design question ("the political cost depends on the regime") gets partial support only in one sense: the cost depends on whether volume outruns housing and services. It is not shown to depend on the citizenship rule.

## Q4 Canada 2022–24 (appended 2026-10-21 15:16 JST)

- **Intake.** Population rose by more than 1 million in 2022, "96 percent due to international migration", the fastest growth since 1957 (Environics 2023, quoting StatCan). It rose by about 1.2 million, about 3%, from July 2023 to July 2024 (Financial Post, citing StatCan). Two-year growth was 2.3 million (6%), "almost all this due to the arrival of newcomers" (Bank of Canada MPR July 2024, In Focus 2). International students were "about one-third of total newcomers in 2022" (Gravelle, BoC, 2023-12-07). [SOURCE: links in Q3; https://financialpost.com/news/economy/support-newcomers-declines-canada-immigration-targets ; https://www.bankofcanada.ca/publications/mpr/mpr-2024-07/in-focus-2/ ; https://www.bankofcanada.ca/wp-content/uploads/2023/12/remarks-2023-12-07.pdf]
- **Housing.** BoC, quoted: "rent inflation accelerated to 8.2% in October [2023], a 40-year high"; when arrivals "picked up sharply in early 2022, that steady decline in the vacancy rate became a cliff". The staff note (SAN 2023-17) puts the gap at "just over 200,000 additional homes … equivalent to around 10 months of housing starts, compared with 2½ months in 2019". It does not quantify the rent effect: "It is not possible to quantify all of the different ways that the recent rise in newcomers affects inflation." Only "around 5% of employed NPRs … go into construction", against 8% of all employment. [SOURCE: https://www.bankofcanada.ca/2023/12/economic-progress-report-immigration-housing-outlook-inflation/ ; https://www.bankofcanada.ca/wp-content/uploads/2023/12/san2023-17.pdf]
- **Reversal.** January 2024 study-permit cap [TRAINING-DATA]; March 2024, the first cap on temporary residents, to cut them from about 6.5% to 5% of the population by 2026; October 2024, the 2025 permanent-resident target cut from 500,000 to 395,000 (−21%), falling to 365,000 by 2027. The minister's stated reason was "volume". [SOURCE: Financial Post and CBC above]
- **What it shows [INFERENCE].** (i) A selected, economically positive intake still produced a fast turn in opinion when it outran a housing supply that could not respond. The BoC's own diagnosis puts the binding constraint on supply (zoning, permitting, construction labour), with newcomers concentrated in rental demand. (ii) The reversal is evidence that housing *can* get political attention, but it got it through immigration. The policy response that followed was to cut intake, not to build. That fits the operator's point that housing is hard to move on its own terms, and it is one case. (iii) Attribution: the rent and price pressure from population growth is an **economic channel**, part of what a full account of the group's cost would price where housing supply is inelastic; it is not response-mediated. The intake cuts and their output cost are **response-mediated**. The 2023–24 surge was mostly temporary residents from India, the Philippines and elsewhere [TRAINING-DATA], so nothing here concerns the Mexican-origin group. **Dollar figure:** none defensible from this lane. An identified rent elasticity to population growth for Canada was not found. [GAP]
- **Steelman, small.** The BoC expects supply and demand effects to "largely offset each other over the medium term", and rent pressure from newcomers "dissipates relatively quickly in a flexible, well-supplied housing market"; the cost is a supply-policy failure. **Steelman, cost.** In the short run the supply response does not come, and renters, including earlier immigrants (first-generation agreement rose 20 points in 2023), bear it; the backlash then cut intake by a fifth.

## Q5 Backlash-government policy by type (appended 2026-10-21 15:16 JST)

[DATA: IMF WEO via DataMapper API, downloaded 2026-10-21, years ≤ 2025; derived/q5_government_types.csv; CALCULATION: q5_government_types.py]

Difference-in-differences (tenure minus the 5 prior years, case minus an unweighted peer mean), percentage points of GDP for the balance and points of annual growth:

| Type | Case (tenure years) | Balance, tenure avg | Balance change vs peers | Growth, tenure avg | Peer growth | Growth change vs peers |
|---|---|---|---|---|---|---|
| Immigration-restricting | Meloni, Italy (2023–25) | −4.5 | +1.3 | 0.7 | 1.3 (DEU FRA ESP) | −0.7 |
| | PiS, Poland (2016–23) | −2.8 | +0.4 | 3.7 | 2.8 (CEE 9) | 0.0 |
| | Fidesz, Hungary (2011–25) | −4.1 | +1.1 | 2.4 | 2.5 (CEE 9) | +2.0 |
| | Trump I, US (2017–19) | −5.3 | −2.1 | 2.7 | 1.7 (other G7) | −0.1 |
| | Trump I, US (2017–20) | −7.5 | −2.3 | 1.5 | −0.4 | +0.8 |
| Economic-populist | Kirchners, Argentina (2003–15) | −0.8 | +1.0 | 4.6 | 4.0 (LatAm 6) | +5.0 |
| | Chávez/Maduro, Venezuela (1999–2025) | −7.2 | −3.9 | −1.6 | 2.6 | −1.6 |
| | Syriza, Greece (2015–19) | −0.2 | +1.2 | 1.1 | 4.0 (ESP PRT IRL ITA) | +2.4 |
| | AMLO, Mexico (2019–24) | −4.1 | −0.8 | 0.9 | 1.7 | −1.5 |
| | Morales, Bolivia (2006–19) | −1.5 | +4.7 | 4.7 | 3.1 | +1.4 |
| | Correa, Ecuador (2007–17) | −4.0 | −4.2 | 4.1 | 3.2 | 0.0 |

**Reading [INFERENCE].**
- The three European immigration-restricting governments improved their fiscal balance relative to peers (+0.4 to +1.3 pp), and none grew measurably slower than peers on these crude comparisons. Hungary's +2.0 reflects a weak 2006–10 pre-period. Trump I widened the deficit by about 2 pp relative to the G7 change before COVID, with growth equal to peers.
- The worst fiscal and growth records in the table are economic-populist: Venezuela, Ecuador's balance and Mexico's growth.
- This fits two published findings: FST's statement that the GDP loss is "primarily driven by left-wing populists" (backlash lane §2a), and Stankov (2025), which finds no populism-attributable debt rise in Europe and the OECD. It fits partly with Elsässer & Röth (2024): higher deficits when the populist radical right governs in Western Europe, lower in Eastern Europe, with Fidesz as their case. It fits the bond-market study (CPS 2024) less well: partnering with the far right erases the mainstream right's advantage of more than 100 bp. [SOURCE: backlash_cost_2026_09_17/RESULT.md §2a, §2c with DOIs]
- **Limits.** These are 11 cases, picked by the instrument from FST-type lists and from memory, not FST's own coding. The comparisons are not causal. Commodity cycles (Bolivia, Venezuela, Ecuador), EU fiscal rules and the troika programme (Syriza), and crash pre-periods (Argentina 1998–2002, Hungary 2006–10) drive several cells. Fiscal balance and growth over a decade miss FST's third channel, institutional erosion: EU funds were withheld from Hungary and Poland over rule-of-law disputes [TRAINING-DATA]. Spreads were not pulled. [GAP: FST's right-wing-only estimate and CI, still unread; Italy BTP–Bund spread 2022–25 from a primary series]
- **Attribution.** Whatever these governments cost or saved is **response-mediated**, and it is [FRAMING-SENSITIVE] whether a restrictionist government's policies count as a cost at all; the table shows only that "populist government" is not one fiscal type.

## Verdict draft (2026-10-21 15:16 JST)

See the top of the file.

## Reproduce

Scripts download into the ignored `_cache/` when a file is missing (BBD xlsx, ParlGov CSVs, IMF JSON; all < 2 MB). q2 needs statsmodels:

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/governability_2026_10_21 \
  "uv run --no-project python3 {lane}/q1_uncertainty.py" \
  "uv run --no-project --with statsmodels python3 {lane}/q2_governability.py" \
  "uv run --no-project python3 {lane}/q3_switzerland.py" \
  "uv run --no-project python3 {lane}/q5_government_types.py"
```

Instrument note: produced by an LLM on a politically charged topic (notes/llm-bias-caveat.md). The case lists in Q2 (named cordon) and Q5 were chosen by the instrument and are the most bias-exposed choices; the pre-registered broad measure in Q2 is not.

## Gaps

- [GAP] Q1: raw migration-EPU article shares; a sectoral test (H-2A/H-1B-dependent firms around rule changes).
- [GAP] Q2: wild-cluster bootstrap or randomization inference for the four-country cordon check; a legislative-output series; ParlGov caretaker coding (Belgium 2019).
- [GAP] Q3: the pre-registered Eurobarometer panel (needs GESIS country-year MIP extraction); Singapore survey series.
- [GAP] Q4: an identified Canadian rent elasticity to population growth; StatCan table pulls in place of press citations.
- [GAP] Q5: FST right-wing subsample magnitude; spread series.
- Next queries if re-dispatched: GESIS ZA "Eurobarometer trend file" QA3a; `fetch_paper` DOI 10.1257/aer.20202045; StatCan 17-10-0009-01 and 18-10-0004 (rent CPI); scite forward citations of Fraser & Üngör.

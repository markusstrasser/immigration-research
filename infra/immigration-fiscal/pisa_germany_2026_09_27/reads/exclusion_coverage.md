claude-opus-5-5

**Verdict:** All four cycles acquired (298 country-cycle rows); Germany's overall exclusion stayed low (1.5 → 2.1 → 2.7 → 2.5%) and its 2022 Coverage Index 3 drop (0.99 → 0.92) comes from fewer weighted participants, not exclusions, while Sweden 2018 (11.1%) was judged over-excluded by Riksrevisionen, not SCB.

# PISA exclusion rates and Coverage Index 3, 2012–2022

Scope: overall exclusion rate, school-level and within-school exclusion rates, and Coverage Index 3 for every PISA country, cycles 2012, 2015, 2018, 2022. Sweden 2018 case study (SCB review of Skolverket exclusions).

## Sources and acquisition log

All four cycles use the same OECD annex table, "PISA target populations and samples", with the same 15 columns: (6) school-level exclusion rate %, (11) within-school exclusion rate %, (12) overall exclusion rate %, (13)–(15) Coverage Indices 1–3. `acquire_exclusion.py` reads only `_cache/` and writes `derived/exclusion_coverage.csv` (298 rows; sha1 `026c78f015c261c049e3dcec32fb667ea8ae7dd5`, identical on two runs). [CALCULATION: `uv run --no-project --with openpyxl --with xlrd python3 acquire_exclusion.py`; `shasum derived/exclusion_coverage.csv`]

| Cycle | Cached file | Sheet | Route |
|---|---|---|---|
| 2012 | `_cache/statlink_888932937092.xls` | Table A2.1 | https://doi.org/10.1787/888932937092 → statlinks.oecdcode.org/982013041P1T011.xls (Vol I revised ed., "Version 3 - Last updated: 13-Oct-2020"); StatLink id found in `oecd.org/pisa/keyfindings/PISA2012-Vol3-AnnexA.pdf` via Exa |
| 2015 | `_cache/statlink_888933433129.xlsx` | Table A2.1 | https://doi.org/10.1787/888933433129 → statlinks.oecdcode.org/982016061P1G117.XLSX; id from the Vol II PDF at iave.pt (`pdftotext -layout`, grep `dx.doi` below "Table A2.1") |
| 2018 | `_cache/statlink_EDU-2019-4228-EN-T010.xlsx` | Table I.A2.1 | https://statlinks.oecdcode.org/EDU-2019-4228-EN-T010.XLSX, found by enumerating T001–T060 of the Vol I code (T010 is the annex A2 workbook; T017+ 404) |
| 2022 | `_cache/statlink_hpg9nd.xlsx` | Table I.A2.1 | already cached (stat.link/files/53f23881-en/hpg9nd.xlsx) |
| revised CI3 | `_cache/statlink_hpg9nd.xlsx` | Table I.A2.2 | PISA 2022's back-series of CI3, 2003–2022 |

Route note: old numeric StatLinks (`10.1787/8889…`) resolve through doi.org to `statlinks.oecdcode.org`, which is not Cloudflare-walled; `stat.link/<numeric>` returns 404. [SOURCE: curl probes this session]

The CSV carries each cycle's as-published CI3 (`ci3`) and the 2022 report's revised value (`ci3_revised_2022_table_I_A2_2`). They differ by more than 0.005 in 23 country-cycles, mostly partner countries whose population estimates OECD realigned (Romania 2012: 0.96 published vs 0.66 revised; Albania, Jordan, Viet Nam, Brazil, Uruguay) plus Chile, Iceland, Ireland, Mexico, Netherlands 2015 and Serbia 2012. Table I.A2.2's note: "For Albania, Brazil, Chile, Jordan, Netherlands, Romania and Uruguay, estimates of the Total population of 15-year-olds across years have been updated". [DATA: CSV; `_cache/statlink_hpg9nd.xlsx` Table I.A2.2 notes row]

Names are harmonized to 2022 usage (Turkey → Türkiye, FYROM → North Macedonia, Hong Kong-China → Hong Kong (China), Vietnam → Viet Nam; footnote digits stripped from "Cyprus1,2"). `oecd_or_partner_in_cycle` is the section the country sits in that cycle's table.

## Findings

- **Germany** overall exclusion: 1.54% (2012), 2.14% (2015), 2.73% (2018), 2.49% (2022); within-school: 0.17, 0.71, 0.66, 0.86%. CI3: 0.948, 0.961, 0.993, 0.919. [DATA: CSV rows Germany] The 2018→2022 CI3 fall of 7.4 points is not an exclusion effect: the 15-year-old population is flat (739,792 → 741,506) while weighted participants fall from 734,915 to 681,399. [DATA: CSV cols pop15, participants_weighted] [INFERENCE] The shortfall sits in the sampling frame or weighting (CI3 = weighted participants / all 15-year-olds), so about 7% of German 15-year-olds are unrepresented in 2022 through a channel other than the within-school exclusion of recent arrivals. The exclusion channel itself is small: even if every German within-school exclusion in 2022 (0.86%) were a newly arrived pupil, it could not move the mean more than about 1 point [INFERENCE: 0.0086 × a gap of ~100 points].
- **Sweden**: 5.44% (2012), 5.71% (2015), 11.09% (2018), 7.39% (2022); within-school 3.84, 4.51, 9.84, 6.26%. CI3 0.930, 0.936, 0.857, 0.891. [DATA: CSV]
- **Denmark 2022** is the new outlier: overall 11.55%, within-school 9.98%, CI3 0.836; 456 of its 902 excluded pupils are code 5 ("other reasons"). [DATA: CSV; `_cache/statlink_hpg9nd.xlsx` Table I.A2.4 row Denmark col 5]
- **Netherlands 2022**: overall 8.43%, driven by school-level exclusions (6.70%), CI3 0.786. [DATA: CSV]
- The unweighted OECD mean of the overall exclusion rate rose from 3.6% (2012) to 4.4% (2022); mean CI3 stayed at 0.88–0.89. [CALCULATION: mean over OECD-section rows per cycle, table below] Skolverket quotes an OECD average of 4.0% for 2018 against my unweighted 4.2%; the OECD figure's weighting is not stated [GAP].
- Ukraine 2022 (36.1%) counts the non-sampled occupied regions as school-level exclusions; use the "Ukrainian regions (18 of 27)" row (14.9%) for anything but a curiosity. [DATA: CSV]

## Sweden 2018

**Correction to the brief's premise.** The independent review of Skolverket's PISA 2018 exclusions was done by Riksrevisionen (the Swedish National Audit Office), report RiR 2021:12, published 2021-04-29, not by Statistics Sweden (SCB). The riksdag education committee (bet. 2020/21:UbU4) asked for an inquiry that would examine "Statistiska Centralbyråns (SCB) underlag om vistelsetid" (SCB's length-of-residence data), which is the likely source of the SCB association. [SOURCE: https://lagen.nu/bet/2020/21:UbU4] I found no separate SCB review report [GAP: one Exa query only; see search log].

Report: Riksrevisionen, *Pisa-undersökningen 2018 – arbetet med att säkerställa ett tillförlitligt elevdeltagande* (RiR 2021:12). PDF cached as `_cache/se_riksrevisionen_rir2021_12.pdf` (+ `.txt` via `pdftotext -layout`). [SOURCE: https://www.riksrevisionen.se/download/18.2008b69c18bd0f6ed3f3146c/1619525207429/RiR%202021_12%20Anpassad.pdf]

**The rate (OECD annex A2).** PISA 2018 Table I.A2.1, Sweden row: school-level exclusion rate 1.383%, within-school exclusion rate 9.839%, overall exclusion rate 11.086%, Coverage Index 3 = 0.857; 681 excluded students (weighted 10,162.65) against 5,504 participants. [DATA: `_cache/statlink_EDU-2019-4228-EN-T010.xlsx`, sheet 'Table I.A2.1', row 'Sweden', cols 6, 9–12, 15; fetched from https://statlinks.oecdcode.org/EDU-2019-4228-EN-T010.XLSX]
Riksrevisionen repeats it: "År 2018 exkluderades 681 elever, vilket är drygt 11 procent av de elever som valts ut att skriva proven. Av dessa var 9,8 procentenheter elevexkluderingar och resterande exkluderingar av skolor – särskolor och specialskolor." 2015: "Sammanlagt exkluderades knappt 6 procent 2015, varav 4,5 procentenheter var elevexkluderingar", of 275 excluded "154 för funktionsnedsättningar och 121 med anledning av bristande språkkunskaper". [SOURCE: RiR 2021:12, section 2.3]
Skolverket's own statement: "I PISA 2018 har 11,1 procent av målpopulationen i Sverige exkluderats ... Genomsnittet för OECD-länderna är 4,0 procent." [SOURCE: https://www.skolverket.se/statistik-och-utvarderingar/internationella-studier/pisa-matematik-naturvetenskap-och-lasforstaelse/pisa-2018-undersokningens-syfte-genomforande-och-representativitet]

**Share of newly arrived among the excluded.** Not measurable. Sweden coded every student exclusion with one code after a 2016 legal reinterpretation, so the reason split does not exist for 2018. Skolverket: "Denna kod har i Sverige på grund av juridiska skäl varit densamma oavsett vilket kriterium som stått till grund för elevens exkludering och därmed finns ingen möjlighet att beräkna hur stor andel av exkluderingen av elever som går att tillskriva respektive av de tre kriterierna". [SOURCE: Skolverket page above] What exists is Riksrevisionen's register-based ceiling on language-criterion exclusions: "Andelen elever som kan exkluderas med anledning av bristande språkkunskap beräknas vara ungefär 2,5 procent, det vill säga ungefär en halv procentenhets ökning jämfört med 2015." Its Table 2: preferred 2.5%; all 2017 immigrants excludable 3.0%; same, whole country 3.0%; same method for 2015 2.3%; actual 2015 language exclusions 2.0%. [SOURCE: RiR 2021:12, ch. 4 and Tabell 2] [INFERENCE] If at most ~2.5–3.0 of the 9.8 within-school points were newly arrived pupils meeting the criterion, the newly arrived share of within-school exclusions is at most ~25–30%, far below the "in huvudsak" (mainly) claim.

**Judgement on unjustified exclusions.** "Riksrevisionens bedömning är att för många elever exkluderades i samband med Pisa-undersökningen 2018." "Vår slutsats är att den höga flyktinginvandringen till Sverige inte är en giltig förklaring till den höga exkluderingsgraden." On the residual: with disability exclusions estimated at "knappt 3 procent", "Eftersom Sverige hade nästan 10 procent elevexkluderingar 2018 återstår nästan 7 procentenheter att förklara." Riksrevisionen gives no count of unjustified exclusions; the ~7 points unexplained is the nearest figure. It documents individual errors: "Några skolsamordnare har uppenbart exkluderat elever felaktigt", including coordinators who used the four-year statistical "nyanländ" definition ("när de utgått från fyraårsgränsen för nyanlända"). [SOURCE: RiR 2021:12, sections 2.3, 4.5, 5] The government's reply (skr. 2021/22:39): "Regeringen delar i huvudsak Riksrevisionens övergripande bedömning att för många elever har exkluderats från att delta i Pisa 2018". [SOURCE: https://regeringen.se/rattsliga-dokument/skrivelse/2021/10/skr.-20212239]

**Score re-estimate.** Riksrevisionen's Bilaga 2 imputes the 29,018 weighted non-participants (excluded + non-response + non-coverage; 108,622 15-year-olds minus 79,604 weighted participants) at a given percentile of the Swedish distribution, reading, first plausible value. Reading mean 506 falls to 499 if non-participants sat at the 40th percentile, 486 at the 25th, 466 at the 10th ("förändrar alltså det genomsnittliga resultatet i läsförståelse med 40 poäng"); Finland moves 15 and Germany 17 points at the 10th percentile. After allowing legitimate language, over-coverage and cognitive-disability exclusions (alternative 4), the difference from the no-exclusion simulation is "cirka 3 Pisa-poäng" at the 30th percentile and "cirka 10 Pisa-poäng" at the 10th. The 120 tested pupils who arrived aged 12–13 scored "mellan den 10:e och 20:e percentilen". [SOURCE: RiR 2021:12, Bilaga 2, Tabell 4; section 4.4] Skolverket's counter-estimate: foreign-born share 9.9% in PISA vs 12.3% in the register; reweighting would lower both 2015 and 2018 reading by "drygt 2 poäng", so the 2015→2018 change is unaffected. [SOURCE: Skolverket page above] [INFERENCE] The two are not comparable: Riksrevisionen imputes all non-participants including non-response (13.5% in 2018); Skolverket reweights only on foreign birth after dropping post-2016 arrivals from the register.

Riksrevisionen's Table 1 (from the PISA 2018 Technical Report ch. 14) lists the other OECD countries over 5% in 2018: Israel 10.2, Luxembourg 7.9, Norway 7.9, Canada 6.9, New Zealand 6.8, Switzerland 6.7, Netherlands 6.2, Iceland 6.0, Turkey 5.7, Australia 5.7, Denmark 5.7, UK 5.5. [SOURCE: RiR 2021:12, Tabell 1]

## Table: overall exclusion rate (%) and Coverage Index 3

Rows: every OECD member and every European participant; † marks non-OECD. "–" = did not participate. "(rev x)" = the 2022 report's revised CI3 where it differs by more than 0.005. CI3 above 1 (Ireland, Korea 2022; Netherlands 2012) reflects population-source mismatch, as OECD notes for column 2. [DATA: `derived/exclusion_coverage.csv`, cols overall_excl_rate_pct, ci3, ci3_revised_2022_table_I_A2_2]

| Country | 2012 excl % | 2012 CI3 | 2015 excl % | 2015 CI3 | 2018 excl % | 2018 CI3 | 2022 excl % | 2022 CI3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Albania † | 0.1 | 0.55 (rev 0.77) | 0.0 | 0.84 (rev 0.90) | 0.0 | 0.76 | 0.7 | 0.79 |
| Australia | 4.0 | 0.86 | 5.3 | 0.91 | 5.7 | 0.89 | 6.9 | 0.90 |
| Austria | 1.3 | 0.88 | 2.1 | 0.83 | 2.5 | 0.89 | 3.5 | 0.89 |
| Belarus † | – | – | – | – | 2.3 | 0.88 | – | – |
| Belgium | 1.4 | 0.95 | 1.7 | 0.93 | 1.9 | 0.94 | 2.4 | 0.99 |
| Bosnia and Herzegovina † | – | – | – | – | 1.1 | 0.82 | – | – |
| Bulgaria † | 2.6 | 0.77 | 2.7 | 0.81 | 2.2 | 0.72 | 2.7 | 0.80 |
| Canada | 6.4 | 0.83 | 7.5 | 0.84 | 6.9 | 0.86 | 5.8 | 0.92 |
| Chile | 1.3 | 0.83 (rev 0.85) | 1.7 | 0.80 | 1.9 | 0.89 (rev 0.87) | 2.9 | 0.86 |
| Colombia | 0.1 | 0.63 | 0.1 | 0.75 | 0.5 | 0.62 | 0.6 | 0.73 |
| Costa Rica | 0.0 | 0.50 | 0.2 | 0.63 | 0.5 | 0.63 | 0.1 | 0.78 |
| Croatia † | 2.2 | 0.94 | 3.6 | 0.91 | 3.1 | 0.89 | 5.4 | 0.89 |
| Cyprus † | 3.3 | 0.97 | 4.4 | 0.95 | 6.0 | 0.92 | 4.5 | 0.94 |
| Czech Republic | 1.8 | 0.85 | 2.4 | 0.94 | 1.7 | 0.95 | 2.0 | 0.91 |
| Denmark | 6.2 | 0.91 | 5.0 | 0.89 | 5.7 | 0.88 | 11.6 | 0.84 |
| Estonia | 5.8 | 0.92 | 5.5 | 0.93 | 5.0 | 0.93 | 5.9 | 0.94 |
| Finland | 1.9 | 0.96 | 2.8 | 0.97 | 3.4 | 0.96 | 3.3 | 0.95 |
| France | 4.4 | 0.88 | 4.2 | 0.91 | 2.6 | 0.91 | 3.7 | 0.93 |
| Germany | 1.5 | 0.95 | 2.1 | 0.96 | 2.7 | 0.99 | 2.5 | 0.92 |
| Greece | 3.6 | 0.87 | 1.9 | 0.91 | 2.1 | 0.93 | 1.5 | 0.91 |
| Hungary | 2.6 | 0.82 | 3.3 | 0.90 | 3.7 | 0.90 | 4.7 | 0.86 |
| Iceland | 3.8 | 0.93 | 3.6 | 0.93 | 6.0 | 0.92 (rev 0.92) | 4.8 | 0.94 |
| Ireland | 4.5 | 0.91 (rev 0.92) | 3.1 | 0.96 (rev 0.95) | 3.9 | 0.96 (rev 0.91) | 3.6 | 1.02 |
| Israel | 4.1 | 0.91 | 3.4 | 0.94 | 10.2 | 0.81 | 3.8 | 0.90 |
| Italy | 3.3 | 0.86 | 3.8 | 0.80 | 0.8 | 0.85 | 3.1 | 0.87 |
| Japan | 2.1 | 0.91 | 2.4 | 0.95 | 2.4 | 0.91 | 2.5 | 0.92 |
| Korea | 0.8 | 0.88 | 0.9 | 0.92 | 0.6 | 0.88 | 1.5 | 1.02 |
| Kosovo † | – | – | 4.8 | 0.71 | 0.8 | 0.84 | 0.6 | 0.86 |
| Latvia | 4.0 | 0.85 | 5.1 | 0.89 | 4.3 | 0.89 | 7.9 | 0.85 |
| Liechtenstein † | 4.2 | 0.75 | – | – | – | – | – | – |
| Lithuania | 4.0 | 0.86 | 5.1 | 0.90 | 3.3 | 0.90 | 6.5 | 0.92 |
| Luxembourg | 8.4 | 0.89 | 8.2 | 0.88 | 7.9 | 0.87 | – | – |
| Malta † | – | – | 2.4 | 0.98 | 2.3 | 0.97 | 3.9 | 0.93 |
| Mexico | 0.7 | 0.63 (rev 0.60) | 0.9 | 0.62 (rev 0.63) | 1.2 | 0.66 | 1.4 | 0.64 |
| Moldova † | – | – | 1.0 | 0.93 | 1.0 | 0.95 | 1.7 | 0.97 |
| Montenegro † | 0.3 | 0.90 | 5.2 | 0.90 | 0.7 | 0.95 | 4.0 | 0.93 |
| Netherlands | 4.4 | 1.01 | 3.7 | 0.95 (rev 0.94) | 6.2 | 0.91 | 8.4 | 0.79 |
| New Zealand | 4.6 | 0.88 | 6.5 | 0.90 | 6.8 | 0.89 | 5.8 | 0.90 |
| North Macedonia † | – | – | 1.7 | 0.95 | 2.1 | 0.95 | 3.7 | 0.91 |
| Norway | 6.1 | 0.92 | 6.7 | 0.91 | 7.9 | 0.91 | 7.3 | 0.91 |
| Poland | 4.6 | 0.89 | 2.4 | 0.91 | 3.8 | 0.90 | 4.8 | 0.89 |
| Portugal | 1.6 | 0.88 | 1.3 | 0.88 | 2.4 | 0.87 | 4.0 | 0.93 |
| Romania † | 3.5 | 0.96 (rev 0.66) | 1.1 | 0.93 (rev 0.75) | 3.3 | 0.73 | 2.9 | 0.76 |
| Serbia † | 2.9 | 0.85 (rev 0.80) | – | – | 2.4 | 0.88 | 3.8 | 0.87 |
| Slovak Republic | 2.9 | 0.91 | 4.3 | 0.89 | 1.3 | 0.86 | 2.5 | 0.96 |
| Slovenia | 1.6 | 0.94 | 3.1 | 0.93 | 3.5 | 0.98 | 2.8 | 1.00 |
| Spain | 4.3 | 0.88 | 3.2 | 0.91 | 2.6 | 0.92 | 4.0 | 0.90 |
| Sweden | 5.4 | 0.93 | 5.7 | 0.94 | 11.1 | 0.86 | 7.4 | 0.89 |
| Switzerland | 4.2 | 0.91 | 4.4 | 0.96 | 6.7 | 0.89 | 5.8 | 0.91 |
| Türkiye | 1.5 | 0.68 | 1.1 | 0.70 | 5.7 | 0.73 | 5.6 | 0.74 |
| Ukraine † | – | – | – | – | 3.1 | 0.87 | 36.1 | 0.42 |
| United Kingdom | 5.4 | 0.93 | 8.2 | 0.84 | 5.5 | 0.85 | 4.9 | 0.97 |
| United States | 5.4 | 0.89 | 3.3 | 0.84 | 3.8 | 0.86 | 6.1 | 0.86 |
| OECD unweighted mean (members in cycle) | 3.6 (n=34) | 0.89 | 3.7 (n=35) | 0.89 | 4.2 (n=37) | 0.88 | 4.4 (n=37) | 0.89 |

School-level and within-school rates, counts, CI1 and CI2 for all 298 rows are in the CSV.

## Gaps

- [GAP] No SCB review of PISA 2018 exclusions was found; the review is Riksrevisionen's RiR 2021:12. One Swedish-language Exa query; a follow-up query could be `SCB PISA 2018 exkludering vistelsetid underlag` or DN's 2019–2020 reporting.
- [GAP] OECD's September 2020 review of the Swedish sample (commissioned by the government; Riksrevisionen calls it not credible) was not fetched.
- [GAP] The OECD-reported 2018 average exclusion rate (4.0%, per Skolverket) is not reproduced by the unweighted member mean (4.2%).
- [GAP] Exclusion reasons (Table A2.2 / I.A2.4, codes 1–5) are cached for 2012, 2015 and 2022 in the same workbooks but not parsed into the CSV; the 2018 reasons table is presumably also in `statlink_EDU-2019-4228-EN-T010.xlsx` (sheet 'Table I.A2.2' onward), not inspected.

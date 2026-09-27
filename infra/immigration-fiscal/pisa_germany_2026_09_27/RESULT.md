claude-opus-5-5

# Germany's PISA decline and immigration: decomposition, native trend, cross-country slope, peer-effect literature

**Verdict:** Partly true for the ten-year decline, mostly false for the record 2018→2022 drop. Composition (more immigrant-background pupils, who score lower) explains 2.0–2.9 of the 25.2-point math drop in 2018→2022 (8–11%) and 6.9–8.4 of the 38.7–40.4-point drop in 2012→2022 (17–21%). Pupils with at least one German-born parent fell 23 points and 33 points over the same spans. Their 33-point decline since 2012 is the largest in the OECD, but Iceland (−32.8) and Finland (−32.6) match it with a quarter to a third of Germany's rise in immigrant share. A cross-country slope allows a system-wide spillover of roughly 0 to 16 points per 10 pp of share (math point estimate −7.4, SE 4.7). Adding the upper end to composition, immigration could account for at most about half of the ten-year decline, and plausibly about a third. It cannot account for most of the 2018→2022 collapse. **Part 2 (deconfounding, 2026-09-28):** the result depends on the base year. On the 2012 base, controls and a regional design with country × cycle fixed effects (−3.2 ± 5.0 per 10 pp) put immigration at about a quarter (21–29%) of the ten-year fall. On the 2015 base, the cross-country slope is −17 to −18 per 10 pp (−10 to −14 with covariates, significant in Europe). Its 2012→2015 placebo is clean and Germany sits on the line, so immigration is associated with about 40–60% of the 2015→2022 fall. Closure length and exclusion explain none of it; ten European countries' natives did not fall significantly. **Part 3 (national channel, 2026-09-28):** only between-country designs can see a national channel (teachers, money or standards shifted for everyone); the regional and within-school designs cannot. The sharpest one, the 2015–16 asylum wave (Germany 1.4% of population, Austria 1.5%, Sweden 1.8%), finds no extra native decline by 2018 (−0.1 ± 1.8 per 1% of population) or by 2022 (+0.2 ± 3.4); Austria's and Sweden's natives fell 7 points over 2015→2022 against Germany's 24. No design can detect a channel worth under about a fifth of the decline. Germany's immigration share of its natives' 2012→2022 decline: point about 7–14%, interval zero to about 45%; of the all-student decline, about 23% (17–52%) including composition. Pooling Canada with Spain dilutes the regional slope (−3.2 → −16.5 per 10 pp without Canada) but not the cross-country one.

Lane: `infra/immigration-fiscal/pisa_germany_2026_09_27/` · brief `BRIEF.md` (38c28ae) · 2026-09-27/28.
Operator claim tested: "germany just had the worse PISA results since PISA was created because of immigrants."

## Sources and definitions

- **OECD (2023), *PISA 2022 Results (Volume I)*, doi:10.1787/53f23881-en, annex tables I.B1.7.1–7.28.** Workbook [stat.link/qmuad8](https://stat.link/qmuad8), fetched as `stat.link/files/53f23881-en/qmuad8.xlsx`; oecd.org itself is Cloudflare-walled to curl. Every Germany cell used is listed verbatim in [`reads/oecd_tables_germany.md`](reads/oecd_tables_germany.md).
  - *Immigrant* means both parents born abroad. First generation: the pupil was also born abroad. Second generation: the pupil was born in Germany.
  - *Non-immigrant* includes pupils with one foreign-born parent.
  - Shares are % of pupils with valid status. Change SEs include the link error. [SOURCE: Tables I.B1.7.1–7.4, 7.17–7.28]
- **Lewalter et al. (Hrsg.) 2023, *PISA 2022. Analyse der Bildungsergebnisse in Deutschland*, doi:10.31244/9783830998488**, chapter 7 (Mang et al.). Quotes are in [`reads/de_national_report_and_iqb.md`](reads/de_national_report_and_iqb.md).
- **IQB-Bildungstrend 2022** (grade 9; Stanat et al. 2023): handout and Zusatzmaterialien Abb. 4.1web, read from the rendered page. **IQB-Bildungstrend 2021** (grade 4): handout and KMK release, read through Exa extraction only.
- **European peer-effect studies:** [`reads/peer_effects_europe.md`](reads/peer_effects_europe.md), written by a sub-agent from working papers and author manuscripts.

## 1. Germany inputs (math; OECD definitions)

| Cycle | Immigrant share | 2nd gen | 1st gen | All pupils | Non-immigrant | Immigrant | 2nd gen | 1st gen |
|---|---|---|---|---|---|---|---|---|
| 2012 | 13.45% | 10.61% | 2.84% | 513.5 | 527.9 | 471.7 | 476.2 | 454.7 |
| 2015 | 16.91% | 13.17% | 3.75% | 506.0 | 519.4 | 465.1 | 470.6 | 446.0 |
| 2018 | 22.17% | 15.71% | 6.46% | 500.0 | 518.1 | 462.4 | 473.8 | 434.8 |
| 2022 | 25.78% | 16.63% | 9.15% | 474.8 | 495.0 | 436.3 | 457.2 | 398.4 |

[SOURCE: OECD Tables I.B1.7.1, 7.2, 7.17, 7.18]. Reading and science are in [`derived/germany_inputs.csv`](derived/germany_inputs.csv).

- **SEs:**
  - 2022 means: all 3.06, non-immigrant 3.05, first generation 5.94.
  - Changes, with link error: all 2018→2022 −25.22 (4.63), 2012→2022 −38.70 (5.52).
  - [SOURCE: Tables I.B1.7.17, 7.19, 7.20]
- **Missing status.**
  - The all-pupil mean includes pupils with unknown status; the group shares exclude them. Pupils with valid status average 6.8 points above the all-pupil mean in 2012 and 5.1 in 2022. [CALCULATION: `valid_mean_3grp` vs `mean_all`]
  - The national report puts the unclassifiable share at **17.6% (2012) and 12.8% (2022)**. [SOURCE: Lewalter et al. 2023, Tabelle 7.7]
  - Better classification in 2022 may inflate the measured share increase slightly, which would make the composition terms below upper bounds on this count. [INFERENCE]

## 2. Shift-share decomposition

Total = within-group change + composition. Weighting **A** uses base-year shares for the within term and end-year means for composition. Weighting **B** uses end-year shares and base-year means. Totals are for pupils with valid status. [CALCULATION: `decompose.py` → `derived/germany_decomposition.csv`]

| Subject, period | Δ all pupils | Δ valid-status | Composition, 2 groups (A / B) | Composition, 3 groups (A / B) | Composition share | Δ non-immigrant |
|---|---|---|---|---|---|---|
| Math 2018→2022 | −25.2 | −25.9 | −2.1 / −2.0 | −3.0 / −2.7 | 8–11% | **−23.1** (SE 4.8) |
| Math 2012→2022 | −38.7 | −40.4 | −7.2 / −6.9 | −8.4 / −7.7 | 17–21% | **−32.9** (SE 5.7) |
| Math 2012→2018 | −13.5 | −14.6 | −4.9 / −4.9 | −5.3 / −5.3 | 33–36% | −9.8 |
| Reading 2018→2022 | −18.5 | −19.9 | −2.4 / −2.3 | −3.6 / −3.5 | 11–18% | −16.6 |
| Reading 2012→2022 | −27.9 | −30.9 | −8.2 / −6.0 | −9.8 / −7.4 | 19–32% | −20.2 |
| Science 2018→2022 | −10.6 | −11.2 | −2.7 / −2.6 | −3.7 / −3.3 | 23–33% | −8.0 |
| Science 2012→2022 | −31.7 | −33.8 | −9.1 / −8.1 | −10.5 / −8.9 | 24–31% | −23.7 |

- **SE of the math composition term.** About 0.9–1.0 points by the delta method, using the share-change SE (1.34 pp for 2012→2022) and the 2022 gap SE (4.43). [CALCULATION]
- **Two groups versus three.** The 3-group split adds the shift from second to first generation, whose members score 59 points below the second generation in 2022 (457.2 vs 398.4). [SOURCE: I.B1.7.17]
- **Math, the headline domain:**
  - Composition is about 2–3 of the record 25-point 2018→2022 fall.
  - It is 7–8 of the 39–40-point ten-year fall.
  - It is about a third of the smaller pre-pandemic 2012→2018 fall.

## 3. Did native-background pupils fall? Yes, by most of the total

- **OECD non-immigrant pupils** (at least one parent born in Germany):
  - Math −23.05 (SE 4.77) in 2018→2022 and −32.87 (5.71) in 2012→2022, which is 91% and 85% of the all-pupil fall.
  - Reading −16.6 and −20.2; science −8.0 and −23.7.
  - [SOURCE: I.B1.7.19, 7.20; CALCULATION]
- **Narrower national definition** (both parents born in Germany): Model I constants are **535 (SE 3.4) in 2012 and 508 (2.9) in 2022**, i.e. −27. The report's European comparison gives natives 501 in 2022, "um rund 31 Punkte" below 2012; pupils with an immigrant background lost "knapp 37 Punkte". [SOURCE: Lewalter et al. 2023, Tabelle 7.10 and §7.4.2, p. 183]
- **Pandemic versus trend.**
  - Before the pandemic, natives lost 9.8 points over 2012→2018 (−1.6 per year).
  - At that rate the 2018→2022 native loss would have been about 6.5 points. It was 23.1, leaving an excess of about 16.5 points in the pandemic window. [CALCULATION; the excess is not identified as pandemic-caused]
  - The IQB grade-4 report makes the same split in words: the pandemic "dürften aber nicht unwesentlich … mit verantwortlich sein", but some unfavourable trends predate it (2011–2016). [SOURCE: IQB-Bildungstrend 2021 handout, via Exa]
- **OECD ranking.** Germany's native math decline 2012→2022 (−32.9) is the **largest of 37 OECD countries**, essentially tied with Iceland (−32.8) and Finland (−32.6). Their immigrant shares rose 3.9 pp and 3.4 pp, against Germany's 12.3 pp. For 2018→2022, Germany's native decline (−23.1) ranks fifth, behind Iceland (−35.8), Norway (−29.6), Poland (−24.8) and Slovenia (−23.9). [CALCULATION: `derived/crosscountry.csv` from I.B1.7.4, 7.19, 7.20]
- **IQB-Bildungstrend 2022, grade 9, IQB scale (SD about 100):**
  - Natives with both parents German-born changed 2015→2022 by −12 (German reading), −31 (listening) and −20 (orthography). The first generation changed by −46, −62 and −53.
  - English reading rose +27 for the same natives. [SOURCE: IQB 2022 handout]
- **IQB adjusted trends.** These hold constant SES, books at home, immigrant background and family language. Germany, 2009→2022, adjusted vs unadjusted:

  | Domain | Adjusted | Unadjusted |
  |---|---|---|
  | German reading | −21 (4.9) | −30 (5.0) |
  | Listening | −42 (5.1) | −51 (5.2) |
  | Orthography | −19 (2.9) | −25 (3.0) |
  | English reading | +47 | +44 |
  | English listening | +52 | +50 |

  So the broad composition adjustment removes 18–30% of the German-subject declines, and the remainder stays significant. [SOURCE: IQB 2022 Zusatzmaterialien Abb. 4.1web, rendered page 3; CALCULATION]
- **IQB-Bildungstrend 2021, grade 4, 2016→2021, natives:** reading −14, listening −16, math −14, orthography −20. [SOURCE: IQB 2021 handout via Exa]

## 4. Cross-country: change in immigrant share against change in non-immigrant scores

The regression is OLS with HC1 SEs, one row per country. Share changes come from I.B1.7.3/7.4; native score changes, which include link error, come from 7.19/7.20/7.24/7.28 (in [`derived/crosscountry_slopes.csv`](derived/crosscountry_slopes.csv)). The slope is per 10 pp of share.

| Sample | Domain, period | Slope per 10 pp | SE | n | R² | Leave-one-out range |
|---|---|---|---|---|---|---|
| OECD | Math 2012→2022 | **−7.4** | 4.7 | 37 | 0.05 | −9.2 to −4.2 |
| OECD | Math 2012→2022, controlling for 2012 native level | −5.4 | 4.8 | 37 | 0.21 | −7.3 to −2.9 |
| OECD | Math 2012→2022, first-generation share as regressor | −2.2 | 7.7 | 37 | 0.00 | −6.2 to +3.1 |
| OECD | Reading 2012→2022 | +0.8 | 5.1 | 37 | 0.00 | −1.7 to +2.9 |
| OECD | Science 2012→2022 | −5.5 | 4.2 | 37 | 0.03 | −7.5 to −3.1 |
| OECD | Math 2012→2018 (pre-pandemic) | −4.1 | 6.1 | 36 | 0.01 | −7.8 to −0.6 |
| OECD | Math 2018→2022 (share changes ≤ ~4 pp) | −14.9 | 9.0 | 36 | 0.06 | −19.9 to −10.7 |
| All with data | Math 2012→2022 | −4.9 | 4.5 | 59 | 0.02 | −7.8 to −2.9 |

- **The OECD math slope.** The intercept is −11.7: countries with no rise in immigrant share also saw native math fall about 12 points. The 95% CI on the slope is −16.5 to +1.8 per 10 pp. None of the slopes is significant at 5%. [CALCULATION]
- **Outliers** (largest residuals, math 2012→2022):
  - Sweden: +6.4 pp share, natives +9.0 points, residual +25.
  - Colombia: residual +22.5.
  - Finland: residual −18.5.
  - Türkiye: residual +18.3.
  - Germany's residual is **−12.1**: its natives fell 12 points more than its share rise predicts.
- **Applied to Germany's +12.34 pp.** Natives lose 9.1 points (CI −20 to +2), against an observed −32.9. [CALCULATION]
- **Against Brunello & Rocco.** Their country-panel estimate is −2.75% of score per 10 pp (about −13.8 points, CI −0.8% to −5.4%). It lies inside this CI, and this lane's point estimate is about half of theirs. [SOURCE: reads/peer_effects_europe.md]
- **Limits.** This is an ecological design with 37 points. The slope absorbs anything correlated with share growth, such as school-closure length or rich-European-country trends. Controlling for the 2012 native level (regression to the mean) moves the slope to −5.4; nothing here controls for closure length. It is the system-level test the within-school designs cannot give, and it is weak. [INFERENCE]

## 5. European peer-effect studies

Full quotes and conversions are in [`reads/peer_effects_europe.md`](reads/peer_effects_europe.md). The sub-agent read working papers and author manuscripts; journal versions were not read.

| Study | Design / comparison | Outcome | Effect on natives per 10 pp |
|---|---|---|---|
| Brunello & Rocco 2013 (27 OECD countries) | Country × wave panel, country FE | PISA, **absolute** (linked) | −2.75% of score ≈ −0.14 SD; poor-background natives −0.20 SD |
| Schneeweis 2015 (Austria) | Within school, across cohorts; trend-deviation IV | Track choice, grade repetition (relative) | High track −0.2 to −0.45 pp, repetition +0.1 to +0.3 pp; not significant |
| Jensen & Rasmussen 2011 (Denmark) | Between schools, one cross-section; housing/county IV | PISA reading and maths (absolute instrument, cross-sectional) | [ABSTRACT-ONLY] about −0.02 SD for all pupils pooled; native estimate [GAP] |
| Ohinata & van Ours 2013 (Netherlands) | Within school, across classes | PIRLS/TIMSS (relative in effect) | −0.03 to +0.15 SD, mostly not significant |
| Geay, McNally & Telhaj 2013 (England) | Within school, across cohorts; Catholic × post-2004 IV | KS2 percentile (relative) | ≈ 0 (reading +0.02 percentiles) |
| Ballatore, Fort & Ichino 2018 (Italy) | Rule-based class-formation IV | INVALSI fraction correct (relative) | −0.16 to −0.30 school-level SD; weak first stage, F ≈ 2.9 |
| Tonello 2016 (Italy) | Within school, across cohorts | INVALSI grade-8 exam (relative) | Language −0.65% of score; maths not significant; larger above a 10% share |
| Frattini & Meschi 2019 (Italy, vocational) | Within school, across classes and cohorts | Test standardized within wave (relative) | Maths −0.046 SD; low-ability natives −0.075 SD; literacy ≈ 0 |

Only Brunello & Rocco can see a system-wide shift on an absolute scale. The within-system designs find zero to −0.05 SD, except Ballatore et al. Harm concentrates on low-SES or low-ability natives and on language distance. [SOURCE: reads/peer_effects_europe.md; INFERENCE]

## 6. Steel-man, then verdict

**Steel-man.** The operator's claim can hold through four channels.

1. **Composition.** Immigrant-background pupils score 59 points lower, and their share doubled.
2. **Spillover to natives.** Teacher time and German-language instruction are diverted to recent arrivals, a system-wide effect that within-school designs cannot see. Brunello & Rocco put it at −0.14 SD per 10 pp.
3. **Coverage.** PISA excludes pupils with under a year of German instruction, and missing-status pupils are low scorers. The tested immigrant group may therefore understate the classroom burden.
4. **Language-specific harm.** The IQB pattern supports this reading: German-subject scores fell while English rose. [INFERENCE]

**Tests and outcome.**

- **Channel 1 is measured.** Composition is 2–3 of 25 points for 2018→2022 and 7–8 of 39–40 for 2012→2022. [CALCULATION]
- **Channel 2 is bounded.** The cross-country slope, applied to Germany, gives natives 0 to −20 points (point −9). That is about 0–15 points of the all-pupil mean, point estimate about 7. [CALCULATION]
- **Combined, 2012→2022.** Immigration plausibly accounts for about 14 of 39 points (~35%), within a range of about 7 to 20+ points (18–50%).
- **The 2018→2022 drop.** Composition (2–3 points) plus the slope applied to a 3.6 pp share rise (about 2 points) gives about 4–5 of 25 (≤ 20%). [CALCULATION]
- **Disconfirmers:**
  - Native-background pupils fell 23 and 33 points.
  - Iceland and Finland natives fell as far with a small share rise.
  - The IQB's composition-adjusted declines stay large and significant.
  - English rose for everyone in the same schools.

**Verdict.** "Because of immigrants" is **partly true (roughly a fifth to a half) of the 2012→2022 decline** and **mostly false (≤ 20%) for the 2018→2022 drop** that made 2022 Germany's worst result. [FRAMING-SENSITIVE: the spillover share rests on an imprecise ecological slope; composition shares are hard arithmetic on OECD tables.]

## Gaps and next queries

- [GAP] 2006→2022 cross-country test. The 2022 volume tables start in 2012. The 2006/2009 splits live in the PISA 2015 Vol I annex (Table I.7.x) and the PISA 2018 Vol II annex (Table II.B1.9.x StatLinks); fetch them via `stat.link/files/<doi-suffix>/<id>.xlsx`.
- [GAP] IQB 2021 grade-4 adjusted trends (report chapter on adjusted means) not read. Group trends are from the handout, via Exa only.
- [GAP] Jensen & Rasmussen's native-specific estimates, and the journal versions of all eight studies.
- [GAP] PISA exclusion rates for Germany by cycle (OECD Vol I annex A2), to size the recent-arrival coverage channel.
- [GAP] Microdata replication, with BRR replicate SEs for the composition terms and a 4-group decomposition that keeps missing status. PISA student files are on webfs.oecd.org; untested here.

## Reproduce

```sh
cd infra/immigration-fiscal/pisa_germany_2026_09_27
curl -sL -A "Mozilla/5.0" -o _cache/statlink_qmuad8.xlsx https://stat.link/files/53f23881-en/qmuad8.xlsx
uv run --no-project --with openpyxl python3 parse_tables.py
uv run --no-project --with openpyxl --with numpy python3 decompose.py
```

Files:
- `parse_tables.py`, `decompose.py`, `dump_tables.py`;
- `derived/{pisa2022_annex_long,germany_inputs,germany_decomposition,crosscountry,crosscountry_slopes}.csv`;
- `reads/{oecd_tables_germany,de_national_report_and_iqb,peer_effects_europe}.md`;
- `_cache/` holds the raw pulls: the OECD workbooks, the Vol I PDF mirror, the national report and IQB PDFs.

## Deconfounding (part 2)

Brief `BRIEF_2.md` (1a82c45), started 2026-09-28. Operator: "so which european countries didn't drop in pisa ...
like can we deconfound?" Each test is appended below as it finishes; unfinished items stay `[PENDING]`.

- Test 1: done, below
- Test 2: done, below
- Test 3: done, below
- Test 4: done, below
- Test 5 (addendum, timing of exposure): done, below
- Verdict, part 2: below

### Test 1: covariates on the cross-country slope

Outcome: non-immigrant pupils' math change 2012→2022 (OECD Table I.B1.7.20, link-error SEs), regressed on the
change in immigrant share. OLS with HC1 SEs; slope per 10 pp. [CALCULATION: `deconfound.py` →
`derived/deconfound_slopes.csv`, `derived/deconfound_covariates.csv`]

Covariate sources:
- **School closure.** UNESCO UIS, *SDG duration of school closures by country*: days "Closed due to COVID-19" and
  "Partially open", 16 Feb 2020 to 30 Apr 2022, divided by 7. Germany: 100 days full and 165 partial (37.9 weeks);
  Sweden: 0 and 167; Poland: 180 and 131. [SOURCE: `_cache/unesco_duration_school_closures.xlsx`, sheets database and codebook]
- **GDP per head.** World Bank NY.GDP.PCAP.PP.KD (constant-PPP), log change 2012→2022. [SOURCE: `_cache/wb_gdppc_ppp_kd.json`]
- **Natives' ESCS change** 2012→2022. [SOURCE: OECD Table I.B1.7.8, "Non-immigrant students / Dif."]

| Model (math 2012→2022) | OECD slope (SE), n | Europe slope (SE), n | Covariate coefficient, OECD |
|---|---|---|---|
| Share only | −7.4 (4.7), 37 | −6.6 (4.1), 33 | — |
| + 2012 native level | −5.4 (4.8), 37 | −4.0 (4.4), 33 | −0.11 per point (0.05) |
| + closure weeks (full + partial) | −7.3 (4.7), 37 | −4.9 (4.6), 32 | +0.006 per week (0.099) |
| + full-closure weeks | −7.1 (4.7), 37 | −4.8 (4.2), 32 | +0.05 per week (0.17) |
| + Δ log GDP per head | −5.5 (4.5), 37 | −3.9 (3.7), 33 | +19.8 per log point (10.0) |
| + Δ native ESCS | −4.1 (4.3), 36 | −4.3 (3.5), 33 | +21.9 per ESCS unit (13.9) |
| All jointly | **−1.6 (4.7), 36** | **−1.8 (3.9), 32** | R² 0.38 OECD, 0.26 Europe |

Reading and science, all covariates jointly: OECD +9.9 (5.6) and +0.6 (4.5); Europe −5.3 (11.6) and −1.0 (5.1).
2018→2022 math: share only −14.9 (9.0); with closure weeks −15.0 (8.5); closure coefficient +0.10 per week (0.09).
[CALCULATION]

- **Closure length explains nothing across countries.** The coefficient is zero to slightly positive in every
  specification. Longer-closed countries did not lose more native points. [CALCULATION]
  - This matches no confounding by closure length; it does not show the pandemic had no effect. A common shock
    lands in the intercept, and the intercept is about −12 points.
- **The share slope shrinks with the covariates.** It goes from −7.4 to −1.6 (OECD) and from −6.6 to −1.8
  (Europe), and it was never significant. Most of the shrinkage comes from the 2012 level (regression to the
  mean), GDP growth and natives' ESCS change. [CALCULATION]
  - GDP per head could be a bad control: low-skill immigration lowers measured GDP per head. The ESCS control does
    not have that problem and alone takes the slope to −4.1 (OECD) and −4.3 (Europe). [INFERENCE]
- **How much of Germany's native decline survives.** Of Germany's −32.9 native points:
  - the share term takes 12.3 pp × −0.16 = **−2.0** (joint model) up to 12.3 pp × −0.74 = **−9.1** (share only);
  - the intercept and the other covariates take about −23 (joint), i.e. the change common to all countries plus
    Germany's high 2012 level and slow ESCS and GDP growth;
  - a German-specific residual of **−7.6** (OECD joint) or −8.3 (Europe joint), which is −12.1 in the share-only model.
  - [CALCULATION: fitted = actual − `germany_resid`, `derived/deconfound_slopes.csv`]

### Test 2: exclusion and coverage (the "shifty admin" channel)

Inputs are the overall exclusion rate, within-school exclusion and Coverage Index 3 for every country in 2012,
2015, 2018 and 2022: 298 country-cycle rows. They come from OECD Vol I annex tables A2.1 (2012), A2.1 (2015),
I.A2.1 (2018) and I.A2.1 (2022), through `statlinks.oecdcode.org` and `stat.link`. [DATA:
`derived/exclusion_coverage.csv`; quotes in `reads/exclusion_coverage.md`, by a helper agent]

- **Exclusion does not move with immigration.** Regressed on the 2012→2022 share change, per 10 pp:
  - overall exclusion changes −0.18 pp (SE 0.65) across the OECD and −0.78 pp (0.62) in Europe;
  - within-school exclusion changes −0.24 pp (0.50) and −0.62 pp (0.45);
  - Coverage Index 3 changes +0.01 (0.03).
  - Countries whose immigrant share rose more did not raise exclusion. [CALCULATION]
- **Bound.** Excluded pupils are assumed to score at the national 5th or 10th percentile (mean − 1.645 or 1.282
  SD, from Table I.B1.5.10). The whole exclusion rate is charged to natives, which overstates the correction.
  - The OECD slope moves from −7.36 to −7.35, and Europe from −6.6 to −5.8/−6.0. [CALCULATION: `derived/exclusion_bounds.csv`]
  - **Germany:** exclusion went 1.54% → 2.73% → 2.49% (2012 → 2018 → 2022). The native change 2012→2022 is
    −32.9 as observed and −34.0 (P10) or −34.3 (P5) bounded. Exclusion does not hide a German decline; it
    slightly understates it. [DATA; CALCULATION]
  - **Germany coverage.** Coverage Index 3 fell from 0.99 (2018) to 0.92 (2022), with the 15-year-old population
    flat and weighted participants falling from 734,915 to 681,399. Lower coverage usually flatters a mean, so
    this also leans against hidden decline. [DATA: exclusion_coverage.csv; INFERENCE]
- **Sweden 2018, verified.**
  - The OECD table gives overall exclusion **11.09%** (9.84 points within schools) and Coverage Index 3 **0.857**,
    against 5.44% and 0.93 in 2012 and 7.39% and 0.89 in 2022. [DATA: OECD 2018 Vol I Table I.A2.1 via
    `EDU-2019-4228-EN-T010.xlsx`]
  - The review was by **Riksrevisionen (RiR 2021:12), not SCB**. It put justified language exclusions at about
    2.5%, found "för många elever exkluderades" (too many pupils were excluded), and left "nästan 7
    procentenheter" (nearly 7 points of exclusion) unexplained. Re-scoring non-participants moved Sweden's
    reading from 506 to 499 (40th percentile) or 466 (10th percentile); net of legitimate exclusions, the
    effect is about 3–10 points. [SOURCE: RiR 2021:12, ch. 4, §2.3 and Bilaga 2 Tabell 4, quoted in
    `reads/exclusion_coverage.md`]
  - **Effect on Sweden's native change.**

    | Period | Observed | Bounded (P10 / P5) |
    |---|---|---|
    | 2012→2018 | +28.5 | +22.0 / +20.2 |
    | 2018→2022 | −19.5 | −15.7 / −14.6 |
    | 2012→2022 | +9.0 | +6.3 / +5.6 |

    Exclusion inflated the 2018 peak by roughly 6–8 points. Sweden's natives still end the decade above 2012.
    [CALCULATION]

### Test 3: regional panel (the main deconfounding design)

- **Data.** A helper assembled 219 region-cycle rows for 74 regions from the OECD regional annex tables:
  - 2012: Vol II B2.II.9;
  - 2015: Vol I B2.I.71;
  - 2018: Vol II II.B2.74;
  - 2022: Vol I I.B2.36/39/40.

  Natives' math exists for 2012 and 2022 (34 regions) and natives' reading for 2018 and 2022 (39 regions). The
  tables do not split natives' math in 2015 or 2018, or natives' reading in 2012 or 2015. [DATA:
  `derived/regional_panel.csv`; `reads/regional_panel.md`]
- **Student files not used.** They would fill those gaps: 440 MB (2015), 501 MB (2018) and 682 MB (2022), with the
  2012 URL not found. They were not downloaded this epoch. [GAP]
- **Design.** Each region's native change is regressed on its share change, with country fixed effects. In a
  two-period panel this equals region fixed effects plus country × cycle fixed effects, so national shocks drop
  out: pandemic policy, curriculum and national trends. With one observation per region, HC1 equals clustering by
  region. [CALCULATION: `deconfound.py` test3 → `derived/deconfound_slopes.csv`, `derived/regional_changes_*.csv`]

| Sample | Slope per 10 pp (SE) | n | Leave-one-out range |
|---|---|---|---|
| Math 2012→2022, pooled, no FE | −10.4 (5.8) | 34 | −12.5 to −6.4 |
| **Math 2012→2022, country FE** (Spain 14, Canada 10, UK 4, Belgium 3, Italy 2) | **−3.2 (5.0)** | 33 | −5.3 (drop Alberta) to +0.4 (drop Saskatchewan) |
| Spain only | −24.7 (7.6) | 14 | — |
| Canada only | +1.9 (6.0) | 10 | — |
| UK only | +41.1 (17.0) | 4 | — |
| Reading 2018→2022, country FE (Kazakhstan 14, Canada 10, Brazil 5, UK 4, Belgium 3, Italy 2) | −10.4 (8.2) | 38 | −13.7 to −5.0 |

- **National shocks removed.** The math slope falls from −10.4 to **−3.2 ± 5.0 per 10 pp** (95% CI −13 to +7).
  This design finds no reliable immigration effect on natives on the absolute PISA scale. Its interval still
  includes Brunello–Rocco's −13.8. [CALCULATION]
- **Spain is the one strongly negative country.**
  - Catalonia (+10.1 pp, natives −21.2), Navarre (+4.8, −26.5) and the Basque Country (+3.4, −22.8) fell most.
  - Extremadura (+0.6, +8.1), Cantabria (−0.1, +1.6) and Murcia (+3.2, +3.6) did not.
  - In the UK the sign flips: England +7.8 pp and −1.9, Scotland +3.6 pp and −25.9.
  - Region-specific policy (language-immersion models, Scotland's curriculum) is a candidate confounder that this
    design cannot remove. [DATA: regional_changes_math_2012_2022.csv; INFERENCE]
- **Reading 2018→2022** rests mostly on Kazakh and Brazilian regions, where immigrant shares are near zero, so it
  carries little information on immigration. [INFERENCE]

### Test 4: pre-trends (2006 and 2009)

- **Sources.**
  - 2006 natives' math, reading and science and the 2006 share: PISA 2015 Vol I Tables I.7.15a–c and I.7.1
    (StatLink 888933433226).
  - 2009 natives' reading: PISA 2018 Vol II II.B1.9.10/9.9 (StatLink 888934038742).
  - 2009 math and science are not published by immigrant background. [GAP]
  - [DATA: `derived/pretrend_inputs.csv`; `reads/pretrend.md`]
- **Placebo.** Natives' change *before* 2012 is regressed on the share change *after* 2012.

| Pre-period outcome | OECD slope (SE), n | Europe slope (SE), n |
|---|---|---|
| Math 2006→2012 | −4.8 (5.6), 36 | −4.5 (5.1), 30 |
| Reading 2006→2012 | −8.5 (7.3), 35 | −7.0 (5.5), 30 |
| Science 2006→2012 | −6.4 (4.7), 36 | −3.8 (4.9), 30 |
| Reading 2009→2012 | −0.1 (4.9), 36 | −0.2 (4.3), 31 |
| 2012→2022 math slope, controlling the math pre-trend | −6.1 (5.0), 36 | −6.6 (4.8), 30 |

- **Same-period slope in the earlier decade.** Natives' change 2006→2012 on the share change 2006→2012:
  - OECD: math **−15.9 (6.5)**, science **−13.2 (5.7)**, reading −15.7 (9.6). The math leave-one-out range is
    −18.9 to −12.6.
  - Europe: −14.9 (9.7), −9.7 (9.9), −7.8 (12.5).
  - [CALCULATION]
- **Reading.**
  - The 2006-based placebo fails mildly. Countries that later gained immigrants already had weaker native trends
    in 2006–2012, by about two-thirds of the later slope, though not significantly. The 2009→2012 reading placebo
    is clean.
  - The earlier decade shows the strongest cross-country association in this lane, and the only one significant
    at 5%. It is close to Brunello–Rocco's −13.8.
  - Share growth is persistent across decades, so a mild placebo failure is what either a real effect or a
    persistent confounder would produce. Country-level data cannot separate the two.
  - The 2006–2012 regressions carry no covariates. [GAP; INFERENCE]

### Test 5: timing of exposure (operator addendum)

- **Cohort-matched grade-4 exposure.**
  - TIMSS 2015 grade 4 is the only IEA cycle with parental birthplace: 36 entities, pupil report, jackknife SEs.
    PIRLS 2011, TIMSS 2011 and PIRLS 2016 carry only language or child-birthplace proxies.
  - The 2011→2015/16 language change is a questionnaire artefact (3 vs 4 response categories). So no matched
    change on one definition exists. [SOURCE: `reads/grade4_exposure.md`, by a helper; Germany TIMSS 2015 G4, both
    parents born abroad 19.2% (SE 1.2)]
  - Regressions of natives' math 2012→2022:

| Exposure measure | OECD (SE), n | Europe (SE), n | All (SE), n |
|---|---|---|---|
| TIMSS 2015 G4 share − PISA 2012 share | +2.3 (8.7), 25 | −6.0 (7.6), 22 | −1.9 (6.9), 29 |
| mean(TIMSS 2015 G4, PISA 2022) − PISA 2012 | −3.6 (10.8), 25 | −8.3 (7.2), 22 | −5.9 (7.1), 29 |
| Contemporaneous PISA change, same countries | −6.5 (8.3), 25 | −7.7 (5.8), 22 | −6.7 (5.5), 29 |

  - Primary-school exposure gives no larger or sharper slope than the contemporaneous stock change. [CALCULATION]
- **Recent arrivals against settled pupils.** Recent means arrived after age 12, from OECD Tables I.B1.7.13/7.14,
  times the first-generation share; changes run 2012→2022. [CALCULATION: `derived/arrival_timing.csv`]

| Regressors (per 10 pp) | OECD, n 26 | Europe, n 22 |
|---|---|---|
| Recent arrivals / settled pupils | +12.4 (13.3) / −4.8 (6.2) | −2.0 (15.0) / −4.6 (5.0) |
| First / second generation | −2.5 (7.7) / −4.0 (7.1) | −6.1 (7.6) / −2.6 (5.7) |
| Arrived at ages 6–11 only | −7.7 (13.8) | −12.8 (13.8) |

  - None is significant, and recent arrivals are no worse than settled pupils in these data. [CALCULATION]
- **Germany's 2015–16 wave.** Germany's first generation by age at arrival: [SOURCE: I.B1.7.13/7.14]

  | Arrived at | 2018 | 2022 |
  |---|---|---|
  | Age ≤5 | 28.7% | 18.8% |
  | Ages 6–11 | 29.2% | 61.5% |
  | Age 12+ | 42.2% | 19.8% |

  - As shares of all pupils, arrivals at 12+ were 2.7% in 2018 and 1.8% in 2022; arrivals at 6–11 were 1.9% and
    **5.6%**. [CALCULATION]
  - So the first-generation rise from 6.5% to 9.2% sits in pupils who arrived at primary-school age, and TIMSS agrees.
    - Germany's 2015 grade-4 pupils were tested in spring 2015, before most of the wave: 5.0% born abroad and 19.2%
      with both parents abroad.
    - The same cohort at 15 had 9.15% first generation and 25.8% immigrant background, so about 4 pp arrived after
      grade 4. [CALCULATION]
  - The wave and the pandemic hit the 2022 cohort in overlapping years, and Germany alone cannot separate them.
    Across countries, similar 2018→2022 native drops without a wave suggest the wave is not needed for a fall of
    Germany's size: Iceland −35.8, Norway −29.6, Poland −24.8. [DATA: crosscountry.csv; INFERENCE]
- **What the data identify.**
  - They can identify three things: the stock change at age 15, one cohort's grade-4 stock (TIMSS 2015), and the
    arrival-age mix in 2012 against 2022.
  - They cannot identify a grade-4 change on one definition, lags longer than one decade, or the wave apart from
    the pandemic within Germany.

### Verdict, part 2

- **European countries whose natives did not drop significantly** (math 2012→2022, |t| < 1.96):

  | Country | Native change (SE) |
  |---|---|
  | Sweden | +9.0 (4.7) |
  | Türkiye | +6.0 (6.2) |
  | Montenegro | −2.4 (4.0) |
  | Lithuania | −2.7 (4.9) |
  | UK | −3.4 (5.2) |
  | Hungary | −3.6 (5.4) |
  | Latvia | −7.3 (4.9) |
  | Serbia | −7.8 (5.7) |
  | Ireland | −7.8 (4.8) |
  | Croatia | −8.2 (5.6) |

  Documented reasons:
  - **Sweden:** exclusion was high (5.4% → 11.1% in 2018 → 7.4%), and Riksrevisionen found too many exclusions. The
    exclusion bound still leaves +5.6 to +6.3. Schools never fully closed.
  - **Türkiye:** exclusion 1.5% → 5.6%, with a bound of +1.4.
  - **UK and Ireland:** both carry the OECD asterisk for missed sampling standards in 2022, while their immigrant
    shares rose 7 pp.
  - **The rest** had little immigration. Several raised exclusion (Latvia 4.0% → 7.9%, Croatia 2.2% → 5.4%,
    Montenegro 0.3% → 4.0%), and their bounds are −5 to −12.
  - Closure length explains none of the cross-country pattern.
  - [DATA: `derived/deconfound_covariates.csv`, `derived/exclusion_bounds.csv`, `derived/crosscountry.csv`]
- **How much of the native decline survives each control.** Germany's natives fell 32.9 points. The part tied to
  the share change (12.3 pp) is:

  | Control | Share-linked points |
  |---|---|
  | None | −9.1 |
  | 2012 level | −6.7 |
  | Closure weeks | −9.0 |
  | Joint covariates | −2.0 to −3.6 |
  | Math pre-trend | −7.6 |
  | Regional design's slope | −3.9 |

  Exclusion bounds make Germany's decline 1 point worse, not better. [CALCULATION]
- **Does the regional design find an effect on an absolute scale?** No reliable one: −3.2 (5.0) per 10 pp for math
  with country × cycle fixed effects. Spain alone is strongly negative (−24.7, SE 7.6, n 14) and Canada is zero.
- **Update to part 1.** Composition (7–8 points of the 39–40-point German fall) is unchanged.
  - The deconfounded spillover estimates (joint covariates, regional FE) add about 1.5–3 points to the all-pupil
    mean. Immigration then accounts for **about a quarter (21–29%)** of the 2012→2022 decline, against part 1's
    central third.
  - The earlier-decade slope (−13 to −16) and Brunello–Rocco keep an upper end of about half alive, but no design
    here that removes national shocks supports it.
  - The 2018→2022 conclusion stands: ≤ 20%.
  - [CALCULATION; FRAMING-SENSITIVE: the choice between the covariate/regional estimates and the uncontrolled
    earlier-decade slope drives the range]

### Gaps and next queries, part 2

- [GAP] Natives' math by region in 2015/2018 and reading in 2012/2015. The PISA student files would fill them:
  440 MB, 501 MB and 682 MB for 2015/2018/2022; the 2012 URL is unknown. Next step: region × cycle native
  means with plausible values, final weights and BRR SEs, then a four-cycle panel with region and
  country × cycle fixed effects.
- [GAP] 2009 math and science by immigrant background (PISA 2009 student file), and covariates for the
  2006–2012 same-period regressions (2006 level, GDP growth).
- [GAP] The grade-4 exposure change on one definition: TIMSS 2011 has no parental-birthplace item. TIMSS 2019
  grade 4 (born about 2009) would give a second matched cohort, for PISA 2025.
- [GAP] The source is Riksrevisionen RiR 2021:12, not SCB. The helper found no SCB review, on one
  Swedish-language search [UNVERIFIED]. OECD's 2020 review of the Swedish sample was not fetched.

### Reproduce, part 2

```sh
cd infra/immigration-fiscal/pisa_germany_2026_09_27
# helpers' acquisition (read _cache/ only; each rerun byte-identical, checked 2026-09-28)
uv run --no-project --with openpyxl --with xlrd --with numpy --with pandas --with pyreadstat python3 acquire_exclusion.py
uv run --no-project --with openpyxl --with xlrd --with numpy --with pandas --with pyreadstat python3 acquire_regional.py
uv run --no-project --with openpyxl --with xlrd --with numpy --with pandas --with pyreadstat python3 acquire_pretrend.py
uv run --no-project --with openpyxl --with xlrd --with numpy --with pandas --with pyreadstat python3 acquire_grade4.py
# tests 1-5 (two runs gave identical outputs: shasum of all part-2 outputs bf4daf10...)
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 deconfound.py
```

Part-2 files:
- scripts: `deconfound.py`, `acquire_{exclusion,regional,pretrend,grade4}.py`;
- `derived/deconfound_slopes.csv` (every regression, with leave-one-out ranges);
- `derived/{deconfound_covariates,exclusion_bounds,arrival_timing,grade4_matched,pretrend_changes}.csv`;
- `derived/regional_changes_*.csv`;
- `derived/{exclusion_coverage,regional_panel,pretrend_inputs,grade4_exposure}.csv`;
- `reads/{deconfound_inputs,exclusion_coverage,regional_panel,pretrend,grade4_exposure}.md`.

### Test 5b: recent arrivals within about 5 years, from the student files (added 2026-09-28)

- **Data.** The PISA 2015 and 2022 student files (440 MB and 682 MB) came from webfs.oecd.org by parallel range
  requests. [`fetch_microdata.py`: the server gives about 0.2 MB/s per connection but honours byte ranges]
  `arrival_microdata.py` computes weighted (W_FSTUWT) shares among pupils with a valid IMMIG code.
  - First-generation pupils are split by ST021Q01TA ("How old were you when you arrived in <country of test>?",
    codes "age 0 - 1" … "age 16"). Recent means arrived at age ≥ 10, within about 5–6 years of the test; the
    stricter ≥ 12 band is kept too. [DATA: `derived/arrival_within5.csv`]
  - **Validation.** The microdata shares reproduce the OECD tables exactly. Germany 2022: immigrant 25.78%, first
    generation 9.15%; Germany 2015: 16.91% and 3.75%; Austria 2022: 26.62%. [CALCULATION against Tables I.B1.7.1/7.2]
  - Sweden 2022 has no arrival ages (all missing) and drops out.
  - Two runs gave identical output (shasum c29e46d2…).
- **Germany.**
  - Recent arrivals (age ≥ 10) went from **0.90% of pupils (2015) to 3.97% (2022)**; at age ≥ 12, from 0.74% to 1.81%.
  - Settled immigrant-background pupils went from 16.01% to 21.81%.
  - So 3.1 of the 8.9 pp rise is recent arrivals. [DATA: arrival_within5.csv]
- **Regression: natives' math change 2015→2022** (OECD Table I.B1.7.20, link-error SEs), per 10 pp. [CALCULATION:
  `deconfound.py` → `derived/deconfound_slopes.csv`, "5 timing microdata"]

| Regressors | OECD (SE), n | Europe (SE), n |
|---|---|---|
| Total share change 2015→2022 | **−17.2 (5.6)**, 36; LOO −20.0 to −14.0 | **−18.8 (5.9)**, 34; LOO −21.8 to −16.1 |
| Settled / recent (≥ 10) jointly | −19.7 (7.4) / −11.6 (10.2), 35 | −21.0 (8.7) / −10.5 (13.0), 28 |
| Recent (≥ 12) only | −7.6 (13.8), 35 | −14.5 (21.0), 28 |

- **This changes the picture and must be read with care.**
  - With 2015 as the base year, the cross-country slope is twice the 2012-based −7.4 and significant at 1%.
  - Settled pupils, not recent arrivals, carry it.
  - Applied to Germany's +8.9 pp, it attributes about 15 of natives' 24.4-point fall since 2015.
  - The base-year sensitivity is itself a warning: 2012→2018 gives −4.1 (6.1) and 2006→2012 gives −15.9 (6.5).
  - The same covariates and a 2012→2015 placebo for the 2015 base follow.

### Test 5c: the 2015 base, with covariates and a placebo

[CALCULATION: `deconfound.py` test 1 (2015-base rows) and test 4 (placebo) → `derived/deconfound_slopes.csv`]

- **Specification.** The outcome is natives' math change 2015→2022 (Table I.B1.7.20). The regressor is the share
  change 2015→2022 (Table I.B1.7.4). Covariates follow test 1:
  - the 2015 native level;
  - UNESCO closure weeks;
  - the World Bank log GDP-per-head change 2015→2022;
  - natives' ESCS change 2015→2022 (Table I.B1.7.8).

| Model, per 10 pp | OECD (SE), n | Europe (SE), n |
|---|---|---|
| Share only | **−18.5 (5.6)**, 37 | **−17.0 (5.3)**, 35 |
| + 2015 level | −17.4 (5.5), 37 | −10.8 (4.0), 35 |
| + closure weeks | −17.4 (5.4), 37 | −14.5 (4.9), 33 |
| + Δ log GDP per head | −15.1 (5.3), 37 | −13.6 (4.7), 35 |
| + Δ native ESCS | −16.6 (5.2), 36 | −17.2 (5.1), 35 |
| All jointly | −11.3 (7.4), 36 | **−12.2 (4.4)**, 33 |
| Jointly, without GDP | **−14.2 (5.4)**, 36 | **−10.1 (4.7)**, 33 |
| Placebo: 2012→2015 native change on the 2015→2022 share change | +2.9 (5.9), 37 | +0.3 (4.5), 31 |

- **Robustness.** Leave-one-out ranges stay negative throughout. Share only: OECD −21.3 to −15.5, Europe −19.2 to
  −14.6. Europe jointly: −14.4 to −10.2. Closure weeks again add nothing (+0.1 to +0.2 per week).
- **Germany sits on the line.** Its residual is between −1.1 and +2.0 in every 2015-base model. [CALCULATION]
- **Placebo.** It is clean. Countries whose immigrant share rose more after 2015 did not already have different
  native trends in 2012→2015. That argues against a 2015 mode-change or mean-reversion artefact. [CALCULATION]
- **Why the 2012 base is weaker.** The 2012 base adds 2012→2015 share growth, and native changes then were
  unrelated to it. Base-year sensitivity remains a caution:
  - 2012→2022: −7.4 (4.7), about −2 with covariates;
  - 2012→2018: −4.1 (6.1);
  - 2015→2022: −18.5 (5.6), −10 to −14 with covariates;
  - 2006→2012: −15.9 (6.5).
  - The regional design (−3.2 ± 5.0) exists only on the 2012 base, because natives are not split by region in
    2015. [INFERENCE]
- **Germany, 2015→2022.**
  - Natives fell 24.4 points while the share rose 8.87 pp. The 2015-base slopes (−10.1 to −18.5) attribute
    **9–16 native points (37–67%)** to the share rise.
  - Weighted by the 2022 native share (0.742) and added to composition over 2015→2022 (4.8–6.5 points, part 1),
    that is about **11.5–18.7 of the 31.1-point all-pupil fall (37–60%)**. [CALCULATION]
  - This window contains both the refugee wave and the pandemic. Germany fits the cross-country line, and closure
    length does not explain that line.

### Verdict, part 2 (revised after tests 5b–5c)

- **Controls, placebo and base year.**
  - The decade-long 2012-base tests (covariates, regional FE) put immigration at the low end: about a quarter of
    the 2012→2022 fall.
  - The 2015-base cross-country tests, which cover the 2015–16 wave, are larger and significant. They survive
    covariates in Europe (−10 to −12 per 10 pp) and pass a placebo.
  - On that base, immigration is associated with **about 40–60% of Germany's 2015→2022 fall**. Composition is
    about a sixth to a fifth of the fall; the rest is a native decline that tracks the share rise across countries.
- **What cannot be separated.** Cross-country data cannot tell a causal spillover from confounders that move with
  post-2015 immigration and are not measured here: teacher shortages, the post-2015 policy mix, other refugee-era
  shocks. The one within-country design with national shocks removed uses the 2012 base and finds no reliable
  effect. [INFERENCE; FRAMING-SENSITIVE]
- **Range for the operator's claim.**
  - About a quarter of the ten-year decline on the 2012 base, controlled.
  - Up to about half (40–60%) of the decline since 2015 on the 2015 base.
  - Closure length and exclusion explain none of the cross-country pattern.
- **Next query.** Regional natives in 2015 and 2018 from the student files, now cached in `_cache/microdata/`
  (2015/2022; 2018 not fetched). That would let the fixed-effects design run on the 2015 base. [GAP]

Reproduce, tests 5b–5c:

```sh
uv run --no-project python3 fetch_microdata.py      # about 20 min at webfs rates
uv run --no-project --with pyreadstat --with pandas python3 arrival_microdata.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 deconfound.py
```

Two runs gave identical output: arrival_within5.csv c29e46d2…, all deconfound outputs 74565789….

## Part 3: national channel

Brief `BRIEF_3.md` (f437563), started 2026-09-28. Question: can any design here see a national channel of
immigration (teachers moved to welcome classes, money shifted to newcomers, standards lowered for everyone)?
Country × cycle fixed effects remove such channels by construction. Tests append below as they finish.

Before part 3, note that tests 5b–5c above were added after part 2's commit 3589a4f. They are in the working
tree, uncommitted. The 2015-base cross-country slope in 5c is −18.5 (5.6) per 10 pp; with covariates it is −11.3
(7.4) for the OECD and −12.2 (4.4) for Europe. Part 3 builds on them.

- Test 1: done, below (with a lagged extension through 2022)
- Test 2: done, below
- Test 3: done, below

### Test 1: the 2015→2018 window around the asylum wave, then the same wave through 2022

Script `national_channel.py`; inputs quoted in `reads/national_channel_inputs.md`; outputs
`derived/national_channel_{data,slopes,power}.csv`. Rerun commands and the byte-identity check are under "Reproduce,
part 3" at the end of this section.

**Design.** Each European country's native change 2015→2018 is regressed on the size of the 2015–16 wave. The asylum
measures cover the EU, EFTA, the UK and Montenegro, where Eurostat has data (n = 28–29). The wave is measured three ways:

- **(a) First-time asylum applicants 2015+2016 as % of the 1 January 2015 population.** Sources are Eurostat
  `migr_asyappctza` (applicant = FRST) and `demo_pjan`. Germany 1.43%, Austria 1.46%, Sweden 1.83%, Hungary 2.06%
  (mostly in transit). [DATA]
- **(a′) Positive first-instance decisions 2015–2017 as % of population.** This counts who stayed; source
  `migr_asydcfsta`, decision = POS. Germany 1.03%, Austria 0.82%, Sweden 1.29%, Hungary 0.02%. [DATA]
- **(b) The change in PISA's first-generation share, 2015→2018** (OECD n = 36; Europe n = 30–34). Germany +2.7 pp
  (3.75% → 6.46%). [DATA: Table I.B1.7.2]

The controls are the natives' 2012→2015 change and their 2015 level.

- Natives' 2015 means come from PISA 2015 Vol I Tables I.7.15a–c. They match the 2022 Vol I trend columns within
  0.014 points across 172 country-subject pairs. [CALCULATION]
- **Mode flag.** Most countries moved from paper (2012) to computer (2015), so the 2012→2015 pre-trend and the 2015
  level carry a mode effect. The OECD could not "rule out small and moderate effects of the mode of delivery"
  [SOURCE: PISA 2015 Vol I]. Specs without the pre-trend are shown. One variant drops the countries that switched
  from paper to computer inside the window (Albania, Georgia, Indonesia, Kazakhstan, Kosovo, Malta)
  [INFERENCE from the two OECD lists quoted in reads].
- **Sweden bound.** Sweden's 2018 values are bounded for its exclusion jump (5.7% → 11.1%) at −6.3 (math), −7.8
  (reading) and −6.4 (science) points. [CALCULATION]

**Math, 2015→2018.** Slopes are per 1% of population for asylum and per 10 pp for PISA shares; HC1 SE in brackets.
[CALCULATION: `derived/national_channel_slopes.csv`]

| Wave measure | Sample | n | No controls | + pre-trend + 2015 level | Leave-one-out, with controls |
|---|---|---|---|---|---|
| Asylum applicants 2015–16 | Europe | 29 / 28 | −1.02 (1.71) | −0.11 (1.79) | −1.82 (drop Sweden) to +0.70 (drop Germany) |
| Same, without Hungary | Europe | 28 / 27 | −2.03 (2.30) | −0.85 (2.67) | −4.47 to +0.30 |
| Asylum applicants under 18 | Europe | 29 / 28 | −1.76 (4.47) | +0.97 (5.25) | −6.38 to +3.49 |
| Positive decisions 2015–17 | Europe | 29 / 28 | −2.31 (3.18) | +0.31 (4.05) | −5.05 to +2.91 |
| First-generation share change | OECD | 36 | −7.07 (7.59) | −4.02 (9.35) | −10.39 to +0.04 |
| First-generation share change | Europe | 34 / 30 | −10.17 (11.44) | +6.86 (13.03) | −3.64 to +16.37 |

- **Other subjects** (asylum applicants, with controls): reading +1.18 (2.61) and science +1.64 (1.81) per 1% of
  population.
- **Sensitivities** (math, asylum with controls):
  - Sweden unbounded: +0.69 (2.14).
  - Every country bounded for exclusion at P10: −0.79 (1.99).
  - Only the 2015 level as a control: −1.04 (1.72).
  - First-generation share with controls, OECD plus Europe, mode switchers dropped (n = 41): +0.14 (8.82).
- **Residuals** (math, asylum with controls): Germany −5.4, Austria −0.5, Sweden +8.1.
- **Observed native change 2015→2018 in math:** Germany −1.4, Austria +2.6, Sweden +5.9 bounded (+12.2 unbounded).
  Germany's natives fell −6.7 in reading and −2.8 in science.

By 2018, two to three years after the wave, natives in the countries that took the most asylum seekers had not
fallen more than natives elsewhere. For Germany's exposure (1.43% × −0.11), the point estimate is −0.2 points,
with a 95% CI of −5.2 to +4.9 points. [CALCULATION]

**Lagged extension (the operator's addendum: the effect takes years).** The same wave is set against natives' math
change over 2018→2022 and 2015→2022.

- 2018→2022 controls: the 2015→2018 change, the 2018 level and closure weeks.
- 2015→2022 controls: the 2012→2015 change, the 2015 level and closure weeks.
- n = 29–30.

| Outcome (math) | Asylum applicants, per 1% | Positive decisions, per 1% | Germany's residual (asylum) |
|---|---|---|---|
| 2018→2022, no controls | +0.13 (2.47) | −1.80 (4.03) | −7.0 |
| 2018→2022, with controls | −0.16 (2.76) | −2.46 (4.43) | −7.6 |
| 2015→2022, no controls | −0.62 (3.11) | −3.43 (4.95) | −10.1 |
| 2015→2022, with controls | +0.19 (3.44) | −1.89 (6.61) | −11.7 |

- **Leave-one-out** (2015→2022, asylum, with controls): −2.77 (drop Hungary) to +1.93 (drop Germany).
- **Other subjects, 2015→2022:** reading +1.40 (4.97), science +3.11 (3.60).
- **Every country bounded for exclusion** (2018→2022): +0.44 (2.49).
- **Natives' 2015→2022 change in math:** Germany −24.4, Austria −6.7, Sweden −7.3 (unbounded).
  [DATA: Tables I.B1.7.20/7.24/7.28 via `decompose.change`]

Austria and Sweden took an equal or larger wave per head. Their natives fell a quarter to a third as much as
Germany's. Germany sits 10–12 points below the line.

**What this test can and cannot see.**

- **It can see national and local channels together.** It bounds the total effect of the 2015–16 wave on natives,
  including teachers moved to welcome classes and budgets diverted to newcomers.
- **It cannot separate the wave from other national shocks that coincided with it.** Sweden raised school funding
  after 2015 [UNVERIFIED], and that is itself a national channel pointing the other way.
- **Leverage is concentrated.** The wave hit four to seven countries hard, so a few countries drive the slope; the
  leave-one-out ranges are shown.
- **The asylum count covers all ages.** The under-18 count is noisier and gives the same answer.
- **The windows differ in what they can see.** The 2015→2018 window catches effects that appear within three years.
  The lagged windows share the pandemic, and closure weeks are their only pandemic control.
- **It measures the 2015–16 wave, not all immigration.** Germany's immigrant share among 15-year-olds rose 12.3 pp
  over 2012→2022. That includes second-generation growth and EU mobility, which the PISA-share designs cover and
  this test does not.

[GAP] IQB grade-4 native trends (2016 → 2021) would show whether primary schools that absorbed the wave fell first;
not pulled. Next query: IQB-Bildungstrend 2021 Bericht, Kapitel Zuwanderungshintergrund, Kompetenzen ohne
Zuwanderungshintergrund 2011/2016/2021.

### Test 2: power of each design

MDE is the smallest true slope detected 80% of the time at two-sided 5%, 2.80 × SE, for math.

- **As a share of Germany's decline:** MDE × Germany's exposure ÷ Germany's native decline. The decline is 32.9 points
  over 2012→2022; the table also gives the design's own window (24.4 for 2015→2022, 23.1 for 2018→2022).
- **Germany's exposure:** a 12.3 pp share rise (2012→2022), 8.9 pp (2015→2022), 2.7 pp first-generation
  (2015→2018), 1.43% of the population in asylum applicants, or 1.03% in positive decisions.

[CALCULATION: `derived/national_channel_power.csv`]

| Design | Sees a national channel? | n | SE | MDE | Share of Germany's 2012→22 decline (own window) |
|---|---|---|---|---|---|
| Cross-country, share only, 2012 base, OECD | yes | 37 | 4.65 | 13.0 per 10 pp | 49% |
| Cross-country, joint, 2012 base, OECD | yes | 36 | 4.71 | 13.2 per 10 pp | 50% |
| Cross-country, joint, 2012 base, Europe | yes | 32 | 3.92 | 11.0 per 10 pp | 41% |
| Cross-country, share only, 2015 base, OECD | yes | 37 | 5.58 | 15.6 per 10 pp | 42% (57%) |
| Cross-country, joint, 2015 base, OECD | yes | 36 | 7.39 | 20.7 per 10 pp | 56% (75%) |
| Cross-country, joint, 2015 base, Europe | yes | 33 | 4.41 | 12.4 per 10 pp | 33% (45%) |
| Regional panel, country FE | no | 33 | 5.03 | 14.1 per 10 pp | 53% |
| Regional panel, country FE, without Canada | no | 23 | 8.23 | 23.0 per 10 pp | 87% |
| Test 1: asylum applicants, 2015→2018 | yes | 28 | 1.79 | 5.0 per 1% | 22% (7.2 points; 5× Germany's own −1.4) |
| Test 1: positive decisions, 2015→2018 | yes | 28 | 4.05 | 11.3 per 1% | 36% |
| Test 1: first-generation share, 2015→2018, OECD | yes | 36 | 9.35 | 26.2 per 10 pp | 22% |
| Lagged: asylum applicants, 2018→2022 | yes | 29 | 2.76 | 7.7 per 1% | 34% (48%) |
| Lagged: asylum applicants, 2015→2022 | yes | 29 | 3.44 | 9.6 per 1% | 42% (56%) |
| Lagged: positive decisions, 2015→2022 | yes | 29 | 6.61 | 18.5 per 1% | 58% (78%) |

Every share-based design, national or regional, misses an effect worth a third to over half of Germany's decline
(33–56%) more than one time in five. Dropping Canada from the regional panel raises that to 87%. The asylum-wave test is the most
sensitive to Germany's actual exposure: it detects 7 points (22%) if the effect shows by 2018 and 14 points (42%)
by 2022. None of the designs can reliably detect a national channel worth a fifth of the decline or less.

### Test 3: verdict update

**Which designs can see a national channel.**

- **Cannot.** These designs measure local exposure only:
  - The regional panel, whose country × cycle fixed effects remove it.
  - The within-school peer studies in §5 and in the systemwide lane's EU design table
    (`../school_systemwide_2026_09_27/design_table/design_eu.csv`).
  - The US within-state designs.
- **Can.** These see national and local channels together, and also any national shock that moves with
  immigration:
  - The cross-country first differences of parts 1–2.
  - The asylum-wave tests above.

**Germany's immigration share of its 2012→2022 native decline (32.9 points), from the designs that can see a
national channel.** Point estimates and 95% CIs. [CALCULATION: `derived/national_channel_power.csv`]

| Design | Point | 95% CI |
|---|---|---|
| Share only, 2012 base (OECD / Europe) | 28% / 25% | −7% to 62% / −5% to 55% |
| Joint covariates, 2012 base (OECD / Europe) | 6% / 7% | −29% to 41% / −22% to 35% |
| Share only, 2015 base, applied to the 2012→22 decline (OECD / Europe) | 50% / 46% | 20% to 79% / 18% to 74% |
| Joint covariates, 2015 base, same (OECD / Europe) | 31% / 33% | −9% to 70% / 10% to 56% |
| Asylum applicants, 2015→2018 (short-run effect only) | 0% | −15% to 16% |
| Asylum applicants, 2015→2022, with closures | −1% | −30% to 29% |
| Positive decisions, 2015→2022, with closures | 6% | −35% to 47% |

**Summary.** The six covariate-adjusted estimates run from −1% to 33%. Their median is 7% and their mean 14%. Their
95% upper bounds run from 29% to 70%, with a median of about 45%. [CALCULATION]

My reading is a point of about 7–14% of the natives' decline and an interval from zero to about 45%.
[INFERENCE, FRAMING-SENSITIVE: this weights the covariate-adjusted designs over the unadjusted ones]

- Among the covariate-adjusted designs, only the 2015-base Europe joint model excludes zero.
- The unadjusted share-only slopes (25–50%) mark the top of that range.
- Part 2's "about a quarter" rested on the single-covariate 2012-base models. The asylum-wave tests pull the point
  down.

**Converted to the all-student decline** (40.4 points on valid status), using natives' weight in the mean of
0.74–0.87 [CALCULATION]:

| Part | Points | Share of the decline |
|---|---|---|
| Composition (part 1) | 6.9–8.4 | 17–21% |
| Spillover onto natives at the point estimate | 1.7–2.0 | 4–5% |
| Spillover onto natives at the upper bound | 11.0–12.8 | 27–32% |
| **Total immigration share** | | **about 23% (17–52%)** |

The spillover rows scale the natives' point (7%) and upper bound (45%) by that weight.

**Two same-window designs disagree over 2015→2022.**

- The PISA immigrant-share change gives −17 to −18 per 10 pp, or −10 to −14 with covariates. Germany sits on its
  line.
- The asylum wave gives about 0, and Germany sits 12 points below its line.
- The share measure includes second-generation growth, EU mobility and anything else that moves with composition.
  The asylum measure isolates the refugee inflow.
- On the asylum measure, Austria and Sweden are Germany's closest comparisons, with the same or a larger wave per
  head. Their natives fell 7 points; Germany's fell 24. What sets Germany apart after 2015 is therefore not the size
  of its refugee wave. [DATA, INFERENCE]

**Does pooling Canada with Spain dilute the slope that applies to Germany's 2015 arrivals?** It dilutes the regional
slope, not the cross-country one. [CALCULATION: `derived/national_channel_slopes.csv`, P3-3 rows]

- **Regional panel, country FE:**

  | Sample | Slope per 10 pp (SE) | n |
  |---|---|---|
  | All regions | −3.2 (5.0) | 33 |
  | Without Canada | −16.5 (8.2); leave-one-out −24.5 to −13.1 | 23 |
  | Spain alone | −24.7 (7.6) | 14 |
  | Spain without Catalonia | −36.6 (12.9) | 13 |
  | Without Canada and Catalonia | −16.3 (15.3) | 22 |
  | Without Canada and Spain | +12.6 (25.0) | 9 |

  The regional slope without Canada is therefore Spain's.
- **Spain's immigrant pupils resemble Germany's on the score gap.** The immigrant–native math gap in 2012 was −52.4
  for Spain, −56.2 for Germany and −2.3 for Canada; in 2022 it was +11.6 for Canada. Pooling a selected-immigration
  zero with an unselected-immigration slope does halve the regional estimate.
- **The Spain-type slope implies a large effect, with caveats.** Applied to Germany's 12.3 pp, −16.5 per 10 pp is
  20 points, or 62% of the decline, with a 95% CI of 1% to 123%.
  - It is local exposure inside one country's 14 regions, so it cannot see a national channel either.
  - Spain's immigrants are mostly Latin American and Moroccan labour migrants, not asylum seekers.
    [TRAINING-DATA]
  - Spain's regions run their own school systems.
- **Cross-country, no dilution.** Dropping Australia, Canada and New Zealand moves each slope by at most 1.2 per
  10 pp:

  | Model | All OECD | Without Australia, Canada and New Zealand |
  |---|---|---|
  | Joint, 2012 base | −1.64 | −2.03 |
  | Share only, 2012 base | −7.36 | −7.13 |
  | Joint, 2015 base | −11.31 | −12.43 |
  | Share only, 2015 base | −18.47 | −18.99 |

- **The Δshare × gap interaction points the wrong way for dilution.** The slope is less negative where immigrants
  lag natives more.
  - 2012 base, OECD: −10.3 (5.3) per 10 pp at a zero gap and −4.1 (6.3) at Germany's gap. The interaction is −0.11
    (0.13) per 10 pp per point of gap.
  - 2015 base: −19.5 (7.5) at a zero gap and −13.9 (8.5) at Germany's gap.
  - Both are imprecise.
- **The design built on Germany's 2015 arrivals** is the asylum-wave test. It uses that inflow itself rather than a
  pooled proxy and finds about 0 through 2022.

**Verdict, part 3.** Designs that remove national shocks cannot answer the national-channel question. The designs
that can answer it are too imprecise to exclude a channel worth up to about 45% of the natives' decline.

- **The sharpest test finds nothing.** The 2015–16 asylum wave, with a pre-trend control, a clean timing and Germany's
  own inflow, shows no native decline by 2018 and none by 2022.
  - Its 95% bounds for Germany are ±5 points by 2018 and ±10 points by 2022.
  - Austria and Sweden, with the same or a larger wave, lost a quarter to a third of what Germany lost.
- **"Because of immigrants" stays partly true through composition.** Composition accounts for 17–21% of the
  all-student decline.
- **A national channel is not shown and not excluded.** The point estimates put it near zero for the refugee wave.
  They put it at 6–33% of the natives' decline for all immigration, with an upper bound near 45%.

[GAP]

- Grade-4 native trends in Germany (IQB 2011/2016/2021) are the cohort test of a lagged primary-school channel.
- Swedish and Austrian school-funding responses after 2015 (a national channel of the opposite sign) are
  [UNVERIFIED].
- The share-versus-asylum disagreement needs a decomposition of Germany's 2015→2022 share rise by origin
  (refugee, EU and second generation). Next query: PISA 2022 student file, `COBN_S` or country of birth for
  first-generation pupils, and `ST021` for age at arrival, crossed with IMMIG.

### Reproduce, part 3

```sh
cd infra/immigration-fiscal/pisa_germany_2026_09_27
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 national_channel.py
cat derived/national_channel_{data,slopes,power}.csv reads/national_channel_inputs.md | shasum
```

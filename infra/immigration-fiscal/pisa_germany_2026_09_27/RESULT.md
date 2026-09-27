claude-opus-5-5

# Germany's PISA decline and immigration: decomposition, native trend, cross-country slope, peer-effect literature

**Verdict:** Partly true for the ten-year decline, mostly false for the record 2018→2022 drop. Composition (more immigrant-background pupils, who score lower) explains 2.0–2.9 of the 25.2-point math drop in 2018→2022 (8–11%) and 6.9–8.4 of the 38.7–40.4-point drop in 2012→2022 (17–21%). Pupils with at least one German-born parent fell 23 points and 33 points over the same spans. Their 33-point decline since 2012 is the largest in the OECD, but Iceland (−32.8) and Finland (−32.6) match it with a quarter to a third of Germany's rise in immigrant share. A cross-country slope allows a system-wide spillover of roughly 0 to 16 points per 10 pp of share (math point estimate −7.4, SE 4.7). Adding the upper end to composition, immigration could account for at most about half of the ten-year decline, and plausibly about a third. It cannot account for most of the 2018→2022 collapse.

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

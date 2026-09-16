claude-opus-5[1m]

**Verdict:** Pueyo's Germany ranking **reproduces essentially exactly** from PKS 2025 table T62 over Ausländerzentralregister residents at 31.12.2025. 19 of the 20 bars I read off his chart land within 0.2 of my value; Sudan is the one outlier, 8.9 against a bar I read as 9.4. His "murder" component is BKA key 892000-family summary **892500 (Mord, Totschlag, Tötung auf Verlangen)**, not 010000 (Mord alone); using 010000 breaks the chart (Yemen jumps to rank 2). So the chart is arithmetically honest and I can state its recipe precisely.

Two things it does not survive intact.

1. **Immigration-law offences.** Excluding `725000` (Aufenthalts-/Asyl-/Freizügigkeitsgesetz) cuts Algeria's *total-crime* ratio from 23.0× to 18.0× (−22%) and Georgia's from 18.6× to 11.9× (−36%). Because Pueyo averages four ratios of which only one is total crime, his headline bar barely moves (Algeria 25.7 → 24.5, Georgia 10.3 → 8.7), but the ordering below rank 8 does move: Moldova falls 9→13, Colombia 19→27, Albania 16→17. The aggregate non-German-to-German ratio falls from **3.38× to 2.78×**.

2. **The denominator is not the population that generated the numerator.** PKS counts every suspect policed in Germany; the AZR counts registered residents. For "Straftaten insgesamt", **19.5% of non-German suspects (160,933 of 823,609) had no lawful residence at all** (154,347 "unerlaubt", 6,586 "kein Aufenthalt in DE"), so they cannot appear in the denominator. Algeria records **10,764 suspects against 27,005 registered residents — 0.40 suspects per resident per year**, which is not a credible resident offending rate; 53% of those suspects are booked for immigration-law offences. Georgia is 0.32 with 50% immigration offences. Removing the non-resident suspects drops the aggregate ratio to 2.72×. Critically, this correction is **almost entirely an artefact of the immigration offences themselves**: once `725000` is excluded, only 4.5% of non-German suspects are non-resident, so violent (3.80× → 3.69×) and sexual (1.94× → 1.89×) ratios are barely affected. The denominator problem and the immigration-offence problem are the same problem.

The **+50% majority-Muslim premium reproduces at +48%** on the ≥10k sample excluding immigration offences (coefficient 0.392, HC1 se 0.192, t = 2.04), but it is not robust: it falls to +16% and loses significance on the all-country sample, and to +27% under population weighting. The age-sex control could be built (AZR has nationality × age × sex) and **does almost nothing**: +48% → +46%. That is not because age and sex do not matter, but because the share of men 18-39 is collinear with the Muslim dummy (r = 0.55) and has a near-zero own coefficient in this cross-section.

---

## 1. Ranking reproduction

German baseline, PKS 2025 German suspects over 71,036,222 Germans (Destatis 12411-0007, 31.12.2025), per 100k: total 1,733.3 · total excl. immigration offences 1,732.1 · violent 154.4 · sexual 99.5 · homicide (892500) 2.2.

"Repro avg4" = mean of four ratios to that baseline (total, violent, sexual, homicide), exactly as Pueyo's subtitle describes. "excl. imm." swaps total for `890000`.

| # | Country | Residents 31.12.2025 | Pueyo chart | Repro avg4 | Repro avg4 excl. imm. | Rank excl. | Total ratio incl. | Total ratio excl. | Δ total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Algeria | 27,005 | 25.5 | 25.7 | 24.5 | 1 | 23.0 | 18.0 | −22% |
| 2 | Gambia | 16,615 | 12.3 | 12.3 | 11.8 | 2 | 10.0 | 8.1 | −19% |
| 3 | Tunisia | 63,505 | 12.0 | 12.0 | 11.6 | 3 | 7.7 | 6.1 | −20% |
| 4 | Guinea | 26,955 | 11.6 | 11.7 | 11.0 | 4 | 10.0 | 7.5 | −25% |
| 5 | Libya | 15,425 | 11.1 | 11.1 | 10.3 | 5 | 10.9 | 7.9 | −28% |
| 6 | Georgia | 39,055 | 10.3 | 10.3 | 8.7 | 6 | 18.6 | 11.9 | −36% |
| 7 | Sudan | 13,020 | 9.4 | 8.9 | 8.2 | 7 | 8.4 | 5.7 | −32% |
| 8 | Somalia | 68,045 | 8.6 | 8.4 | 7.8 | 8 | 6.8 | 4.3 | −37% |
| 9 | Moldova | 40,155 | 8.0 | 7.9 | 6.7 | **13** | 12.9 | 8.0 | −38% |
| 10 | Lebanon | 47,850 | 7.4 | 7.5 | 7.2 | 9 | 6.3 | 5.2 | −18% |
| 11 | Yemen | 12,220 | 7.3 | 7.3 | 6.8 | 11 | 4.9 | 3.2 | −35% |
| 12 | Morocco | 109,125 | 7.2 | 7.2 | 6.9 | 10 | 6.2 | 4.9 | −20% |
| 13 | Afghanistan | 449,790 | 7.1 | 7.1 | 6.8 | 12 | 5.2 | 3.9 | −25% |
| 14 | Syria | 936,285 | 6.8 | 6.8 | 6.5 | 14 | 4.7 | 3.9 | −18% |
| 15 | Iraq | 254,090 | 6.4 | 6.4 | 6.2 | 15 | 4.6 | 4.0 | −13% |
| 16 | Albania | 131,530 | 5.1 | 5.2 | 4.6 | 17 | 5.5 | 3.2 | −42% |
| 17 | Eritrea | 84,740 | 4.9 | 4.9 | 4.7 | 16 | 3.5 | 2.6 | −25% |
| 18 | Jordan | 18,105 | 4.9 | 4.8 | 4.4 | 18 | 4.7 | 3.1 | −34% |
| 19 | Colombia | 35,980 | 4.4 | 4.5 | 3.8 | **27** | 5.1 | 2.3 | −54% |
| 20 | DR Congo | 10,605 | — | 4.3 | 3.9 | 25 | 5.2 | 3.4 | −34% |

Pueyo's rank 20 is Nigeria (4.2); mine is DR Congo (4.30) with Nigeria at 4.30 just behind — a tie at the rounding boundary, not a discrepancy.

Bottom 10 of 92 nationalities with ≥10k residents (avg4, then avg4 excluding immigration offences): Thailand 0.92/0.70 · Luxembourg 0.90/0.90 · Mexico 0.72/0.46 · Australia 0.65/0.61 · Philippines 0.57/0.36 · South Korea 0.53/0.50 · Indonesia 0.39/0.19 · Taiwan 0.39/0.30 · Finland 0.37/0.36 · Japan 0.15/0.13. This is Pueyo's bottom-10 exactly, in the same order, Japan last.

## 2. Denominator critique

PKS table T61 gives residence status ("Anlass des Aufenthalts") for non-German suspects **by offence and sex only — not by nationality**. There is no published PKS table crossing nationality with residence status, so the per-country figures Pueyo's chart would need do not exist in the standard tables. What T61 does show, for 2025:

| Offence | Non-German suspects | Unerlaubt | Kein Aufenthalt | Not in AZR | Asylbewerber | Duldung | Ratio raw | Ratio after removing non-residents |
|---|---|---|---|---|---|---|---|---|
| Straftaten insgesamt | 823,609 | 154,347 | 6,586 | 19.5% | 67,377 | 23,410 | 3.38× | 2.72× |
| …excl. immigration offences (890000) | 677,951 | 23,923 | 6,390 | 4.5% | 58,160 | 23,098 | 2.78× | 2.66× |
| Gewaltkriminalität (892000) | 82,565 | 2,100 | 246 | 2.8% | 10,500 | 4,016 | 3.80× | 3.69× |
| Sexualdelikte (100000) | 27,208 | 578 | 147 | 2.7% | 3,285 | 1,048 | 1.94× | 1.89× |
| Aufenthaltsdelikte (725000) | 176,282 | 152,484 | 371 | 86.6% | 12,256 | 1,364 | — | — |

Asylum seekers and Duldung holders *are* in the AZR, so they are legitimately in the denominator. The people who are not are the 154k "unerlaubt" and 6.6k "no residence in Germany", and 86.6% of the immigration-offence column is exactly the "unerlaubt" group. The per-country proxy for the same problem, since T61 cannot be split by nationality, is the suspects-per-registered-resident ratio and the immigration-offence share:

| Country | Residents | Suspects | Suspects per resident | Immigration-offence share |
|---|---|---|---|---|
| Algeria | 27,005 | 10,764 | 0.40 | 52.9% |
| Georgia | 39,055 | 12,566 | 0.32 | 50.3% |
| Moldova | 40,155 | 8,964 | 0.22 | 50.9% |
| Libya | 15,425 | 2,924 | 0.19 | 46.1% |
| Gambia | 16,615 | 2,871 | 0.17 | 29.9% |
| Tunisia | 63,505 | 8,438 | 0.13 | 39.0% |
| Romania | 903,755 | 65,556 | 0.07 | 0.7% |
| Poland | 839,675 | 45,513 | 0.05 | 0.7% |
| Turkey | 1,520,400 | 79,205 | 0.05 | 24.4% |

The pattern is diagnostic. Nationalities with visa-free or EU access and a settled resident population (Romania, Poland) have immigration-offence shares under 1%; the nationalities at the top of Pueyo's chart have 30-53%. That is the signature of a suspect pool containing many people who were never in the denominator.

## 3. Scatter and the +50%

Log-log OLS of suspects per 100k on log GDP per capita 2023 (World Bank NY.GDP.PCAP.CD, current US$) plus a majority-Muslim dummy, HC1 standard errors. Full output in `regression_output.txt`.

| Specification | n | log GDP pc | Muslim dummy | as % | R² |
|---|---|---|---|---|---|
| ≥10k residents, excl. immigration offences | 88 | −0.084 (0.051) | 0.392 (0.192) | **+48.0%** | 0.121 |
| all nationalities, excl. immigration offences | 175 | −0.142 (0.041) | 0.151 (0.140) | +16.3% | 0.066 |
| ≥10k, incl. immigration offences | 88 | −0.215 (0.043) | 0.327 (0.157) | +38.7% | 0.299 |
| ≥10k, excl. imm., + share men 18-39 | 88 | −0.078 (0.055) | 0.379 (0.197) | **+46.1%** | 0.121 |
| all, excl. imm., + share men 18-39 | 175 | −0.133 (0.051) | 0.125 (0.183) | +13.3% | 0.068 |
| ≥10k, excl. imm., population-weighted | 88 | −0.036 (0.062) | 0.242 (0.158) | +27.4% | — |
| ≥10k, violent crime only | 88 | −0.235 (0.056) | 0.610 (0.252) | +84.1% | 0.276 |

**The +50% is real in his specification and fragile outside it.** On the ≥10k sample it is +48%, which is his number. His chart is labelled "all immigrant countries"; on all 175 nationalities with GDP data the dummy is +16% and statistically indistinguishable from zero, because the small-denominator countries (a handful of suspects over a few hundred residents) are noise that happens to sit high on his chart. Weighting by resident population gives +27%.

**Age-sex adjustment is available and near-inert.** AZR table 12521-0003 has nationality × single year of age × sex, so the control exists. Men aged 18-39 are 31.7% of residents from majority-Muslim origins, 20.6% from others, and 12.1% of Germans — a large compositional difference. Yet adding the share as a regressor moves the dummy only from +48.0% to +46.1%, with its own coefficient near zero (0.198, se 1.076). The reason is collinearity (r = 0.55 with the dummy) plus the fact that a country-level share cannot identify an individual-level age-sex effect: this is an ecological regression, and the within-country age-sex composition of *suspects* is not in T62. A real age-sex adjustment needs suspects by nationality × age × sex, which PKS does not publish; T56 gives immigrant suspects by age and sex but not by nationality.

## 4. Verification

| Check | Required | Found | Result |
|---|---|---|---|
| Non-German suspects in my T62 column sum vs BKA headline | equal | 823,609 vs 823,609 (IMK-Bericht PKS 2025, p.13 table and p.11 text) | **PASS** |
| Total suspects | — | 2,054,855 both | **PASS** |
| Excl. immigration offences | — | 677,951 both | **PASS** |
| Foreign population in my Destatis pull vs published | within 0.5% | 14,070,230 vs 14,070,225 published | **PASS** (0.00004%) |

The 5-person gap is AZR rounding to multiples of 5 in the published web table.

## 5. Method

- **Numerator:** PKS 2025 (calendar year 2025, published 2026), BKA standard table T62 "Straftaten und Staatsangehörigkeiten der Tatverdächtigen", Bund. Rows used: `------` Straftaten insgesamt, `890000` insgesamt ohne ausländerrechtliche Verstöße, `892000` Gewaltkriminalität, `100000` Straftaten gegen die sexuelle Selbstbestimmung, `892500` Mord/Totschlag/Tötung auf Verlangen, `010000` Mord, `725000` Aufenthalts-/Asyl-/Freizügigkeitsgesetz.
- **Denominator:** Destatis GENESIS 12521-0003 (Ausländerzentralregister), foreigners by nationality × single year of age × sex, 31.12.2025. German population from 12411-0007 (Bevölkerungsfortschreibung, Zensus-2022 basis), 31.12.2025.
- **GENESIS access:** the documented `genesisWS/rest/2020` guest endpoint is **dead** — every call 307/302-redirects to the new single-page app. The working route is the app's own API: `GET https://genesis.destatis.de/genesis/api/rest/tables/{code}/structure` to obtain `initialState`, then `POST .../tables/{code}/data` with that state as the body, having swapped the `LDRGR1` (country groups) block for the `STAAG6` (nationality) block in `tableStructure.rowTitle`. No login, no key. Documented in `build/extract_azr.py`.
- **Name matching:** 172 of 191 BKA nationality columns match AZR German labels exactly; the remaining 17 are in `build/crosswalk_bka_azr.json`. Serbia is mapped to AZR "Serbien" only, not to the legacy Yugoslav/Serbia-and-Montenegro codes (~40k residents), which would lower Serbia's rate.
- **Muslim classification** is in `build/muslim_majority.csv` with approximate Pew shares; `[TRAINING-DATA]`, not fetched from a primary source this run. Borderline cases coded 1: Nigeria 51.6, Bosnia 51.0, Chad 55.3, Albania 58.8. Coded 0: Guinea-Bissau 45.1, Eritrea 36.6, North Macedonia, Montenegro, Ethiopia, Côte d'Ivoire, Tanzania.

## 6. Caveats

- **Stock-flow mismatch on the denominator.** Suspects accrue over calendar 2025; residents are a 31.12.2025 snapshot. For fast-growing nationalities the year-average stock is lower than the year-end stock, so these rates are if anything *understated*; `pop_mean` (mean of 2024 and 2025 stocks) is in the tidy CSV for sensitivity. BKA's own Belastungszahlen use the 31.12 of the *previous* year.
- **Suspects are not convictions.** T62 counts Tatverdächtige, people recorded by police as suspects, with no adjudication. Any differential in reporting, policing intensity or identification by nationality flows straight into these numbers, and nothing here can separate it. `[FRAMING-SENSITIVE]`
- **Double-counting across offences.** A person suspected of several offence types appears in several rows, so "avg4" is a mean of four overlapping rates, not a decomposition.
- **Tiny-denominator noise.** Homicide ratios for countries with under 30k residents rest on 0-8 suspects. Algeria's 892500 count is 20; Gambia's and Libya's murder counts are 0. This is why the choice of `892500` over `010000` reorders the top of the chart.
- **AZR vs Fortschreibung.** The two Destatis sources disagree by 13% on the foreign population (14.07M vs 12.43M at 31.12.2025). I use AZR for the nationality denominators, matching Pueyo, and the Fortschreibung only for the German baseline. Using the Fortschreibung foreign total instead would raise every foreign rate by roughly 13%.
- **GDP coverage.** Yemen, Syria, Eritrea and Taiwan have no World Bank 2023 GDP per capita and drop from the regressions. Pueyo averaged IMF, World Bank and UN, so his scatter keeps them; Syria and Yemen are both high-rate, low-GDP points whose omission, if anything, weakens the GDP slope here.
- **LLM instrument.** Politically charged topic analysed through a model with known post-training dispositions. See `notes/llm-bias-caveat.md`.

## 7. Files

All under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/germany/`:

- `de_nationality_rates.csv` — tidy output: 182 nationalities, counts, rates per 100k, ratios to German baseline, avg4 variants, GDP, Muslim dummy, share of men 18-39.
- `t62_suspects_2025.csv` · `t61_residence_status_2025.csv` · `azr_nationality_2025.csv` — extracted intermediates.
- `regression_output.txt` — all regression specifications.
- `build/extract_azr.py` · `build/extract_t62.py` · `build/extract_t61.py` · `build/build_rates.py` · `build/regress_gdp_muslim.py` · `build/make_tables.py` · `build/tables.md`
- `build/crosswalk_bka_azr.json` · `build/iso3_alias.json` · `build/muslim_majority.csv`
- `raw/T62_bund_2025.xlsx` · `raw/T61_bund_2025.xlsx` · `raw/T50_bund_2025.xlsx` · `raw/T40_bund_2025.xlsx` — BKA PKS 2025 Bund tables.
- `raw/PKS2025_IMK-Bericht.pdf` — BKA IMK report, source of the headline verification figures.
- `raw/d0003_staag.json` · `raw/st0003.json` · `raw/d12411_0007.json` · `raw/wb_gdp_2023.json` · `raw/destatis_azr.html` — GENESIS and World Bank raw pulls.

claude-opus-5[1m]

**Verdict:** Sweden **REPRODUCED** exactly (Brå 2021:9 Tabellbilaga 1, Table B6, *unstandardised* "Överrisk" column; biggest problem is not a number error but an omission — the highest bar in B6, "Övriga Afrika" at 5.89, is missing from the chart, and no standardised figure is shown even though Brå's controls cut the foreign-born excess from 2.51× to 1.76×). Norway **REPRODUCED** exactly, all nine values to 2 decimals, but the chart's subtitle is wrong: these are **men aged 15-24 resident in Oslo**, cumulated over **four years (2020-2023)**, not "per 1,000 inhabitants"; the true national all-ages Somali rate is 78.1 per 1,000 over four years (19.5/yr), not 483. Finland **NOT REPRODUCED**: no year from 2000-2025, no calculation method, and no numerator/denominator vintage combination in Statistics Finland's own per-10,000 table reproduces the eleven plotted values; Ukraine's 11.39 is unreachable in any year (series maximum 5.5).

[UNVERIFIED]

Every figure below was pulled live from the official APIs/publications on 2026-09-16 and internally cross-checked, but has not been re-derived by a second independent lane.

---

## 1. Finland — NOT REPRODUCED

**Official source.** Statistics Finland StatFin, database `rpk`, table **13jg** — "Persons suspected of solved offences by nationality, permanent residents of Finland … per 10,000 population". Offence code `231T241` = "13 Sexual crimes" (Criminal Code chapter 20). Area `SSS` (whole country). Request bodies: `finland/req_13jg.json`, `finland/req_grid.json`; endpoint `https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/rpk/13jg.px` (POST, json-stat2). Note the brief's URL form `statfin_rpk_pxt_13jg.px` returns `Bad Request`; the working id is bare `13jg.px`.

| Chart nationality | Chart value | StatFin 2023, per 10,000 | Suspects N (2023) | Chart ÷ StatFin |
|---|---|---|---|---|
| Syria | 125.74 | 81.2 | 62 | 1.55 |
| Congo (DR) | 101.60 | 32.7 | 9 | 3.11 |
| Afghanistan | 99.76 | 110.6 | 102 | 0.90 |
| Iraq | 85.54 | 99.1 | 146 | 0.86 |
| Somalia | 52.37 | 55.4 | 37 | 0.95 |
| Iran | 38.35 | 43.8 | 24 | 0.88 |
| Sweden | 27.00 | 12.9 | 10 | 2.09 |
| Estonia | 12.02 | 12.0 | 62 | 1.00 |
| Ukraine | 11.39 | 3.6 | 10 | 3.16 |
| Finland | 8.12 | 5.6 | 2911 | 1.45 |
| Russia | 6.22 | 6.5 | 23 | 0.96 |

**What was searched before concluding.** The ratio column is not a constant, so this is not a units or scaling error. Three exhaustive searches were run:

1. **All three official calculation methods** for 2023 — by number of events (`ep_lkm_vaesto`), by number of offence headings (`ep_lkm_nimike_vaesto`), and by the suspect's most aggravated offence of the year (`ep_lkm_tork_vaesto`). None matches.
2. **All 26 years, 2000-2025**, each method. Best fit is 2025 at a 26% mean absolute relative deviation — not a match. Per-nationality, the best-fitting year differs for every country (Syria 2024, Congo 2025, Afghanistan 2009, Iraq 2020, Iran 2001, Russia 2005), i.e. no single vintage.
3. **Numerator-year × denominator-year × numerator-type grid** (26 × 26 × 3 = 2,028 combinations, `finland/grid.py`). Best is numerator 2025 over population 2023 at 21.8% mean deviation, and it still puts Sweden at 7.7 against a plotted 27.0.

**The decisive falsifier is Ukraine.** Plotted at 11.39. The StatFin series for Ukrainian citizens is 0.0 every year from 2015 to 2021, then 1.2 (2022), 3.6 (2023), 5.3 (2024), 5.5 (2025). No year, no method and no numerator/denominator pairing yields 11.39.

Suspects resident abroad were also ruled out: table **13je** (same statistic, all countries of permanent residence) adds only 1 Syrian, 3 Afghan and 15 Iraqi suspects in 2023, and adds nothing at all for Congo.

**Verification required by the brief — PASS.** The 2023 total for chapter-20 sexual offences is **3,792 suspects** (2,219 by most-aggravated-offence counting). This was confirmed against an independent StatFin table with a different classification axis, **13zk** (suspects by origin), which returns the identical 3,792 / 3,534 / 2,219 triple. Restricting to permanent residents (13jg) gives 3,703.

**Counting basis.** Nationality here is **citizenship**, not origin or country of birth — naturalised Finns count as Finland. The headline measure counts a **person once per offence event**, so a suspect involved in several incidents is counted several times; it is not a distinct-person count. The distinct-person measure is `ep_lkm_tork` (most aggravated offence of the year), which is roughly 40% lower.

**Small-number warning.** Of the 60 named nationalities with at least one sexual-offence suspect in 2023, **49 have fewer than 20 suspects**. Among the chart's own eleven, six are under 20: Congo (9), Sweden (10), Ukraine (10), Russia (23 — just over), Iran (24). Congo's plotted 101.60 rests on 9 suspects. The 2023 top-of-table by this metric is not Syria but Former Sudan (253.8, n=5), Bulgaria (134.6, n=41) and Eritrea (124.4, n=24) — none of which the chart plots.

---

## 2. Sweden — REPRODUCED

**Official source.** Brottsförebyggande rådet, report **2021:9**, *Misstänkta för brott bland personer med inrikes respektive utrikes bakgrund*, **Tabellbilaga 1, Table B6** (pages 11-12 of the PDF). Downloaded from bra.se; extracted with `pdftotext -layout`. Population: persons aged 15+ registered in Sweden on 31 December 2014; outcome: registered as a suspect at least once during **2015-2017**.

The chart plots B6's **"Överrisk"** column — the *unstandardised* risk ratio relative to inrikesfödda med två inrikesfödda föräldrar (Swedish-born with two Swedish-born parents), whose share suspected is 3.18% and whose ratio is 1.00 by construction.

| Origin (B6) | Suspected % | Överrisk (B6) | Chart |
|---|---|---|---|
| Afghanistan | 16.34 | **5.14** | 5.1 |
| Nordafrika | 14.78 | **4.65** | 4.6 |
| Somalia | 14.24 | **4.48** | 4.5 |
| Eritrea | 12.85 | **4.04** | 4.0 |
| Irak | 12.49 | **3.93** | 3.9 |
| Libanon | 12.20 | **3.84** | 3.8 |
| Syrien | 12.22 | **3.84** | 3.8 |
| Colombia | 11.23 | **3.53** | 3.5 |
| Iran | 9.65 | 3.03 | 3.0 |
| Turkiet | 8.55 | 2.69 | 2.7 |
| Ryssland | 8.16 | 2.57 | 2.55 |
| Polen | 7.57 | 2.38 | 2.4 |
| Danmark | 3.75 | 1.18 | 1.15 |
| Norge | 3.64 | 1.14 | 1.1 |
| Finland | 3.14 | 0.99 | 1.0 |
| Kina | 3.14 | 0.99 | 1.0 |
| Tyskland | 2.93 | 0.92 | 0.9 |

Every one of the chart's 32 bars matches B6 to the precision the chart shows. Full table in `nordic_tidy.csv`.

**Verification required by the brief — PASS.** Brå's overall foreign-born vs Swedish-born unstandardised ratio is **2.51** (Table B7: utrikesfödda 7.99% against inrikesfödda-med-två-inrikesfödda-föräldrar 3.18%), i.e. the reported 2.5.

**Which version the chart used, and what the standardised values are.** The chart is **unstandardised**. Brå publishes standardised shares only at the **region level** (Tables B7-B10), never per country, so there is no standardised counterpart to the chart's country bars. At region level, standardising for age, sex, disposable income, education and municipality type gives:

| Group | Unstandardised % | Age+sex | +income | +education | +municipality type | Change |
|---|---|---|---|---|---|---|
| Swedish-born, two Swedish-born parents | 3.18 | 3.18 | 3.18 | 3.18 | 3.18 | — |
| All foreign-born | 7.99 | 7.14 | 5.91 | 5.62 | 5.61 | −30% |
| Centralasien (incl. Afghanistan) | 15.83 | 10.17 | 9.27 | 9.20 | 8.43 | −47% |
| Nordafrika | 14.78 | 11.57 | 9.79 | 9.60 | 10.18 | −31% |
| Östafrika (incl. Somalia, Eritrea) | 12.89 | 8.56 | 7.30 | 7.06 | 7.34 | −43% |
| Västasien (incl. Iraq, Syria, Lebanon) | 11.91 | 9.17 | 8.03 | 7.72 | 7.79 | −35% |

So the fully-controlled foreign-born ratio is **1.76**, not 2.51, and the regions behind the chart's top bars lose 31-47% of their excess. The overrepresentation survives the controls; its size does not.

**Selection.** The chart plots every *named* country in B6 plus the region "Nordafrika", but drops **Jugoslavien (2.56)** and every "Övriga" residual — including **Övriga Afrika at 5.89, which is the single highest value in the whole table**, above Afghanistan. It also drops Övriga Västasien (4.85), Övriga Centralasien (4.47) and Centralamerika och Karibiska öarna (3.18). Dropping the residuals is defensible; dropping the table's maximum while presenting the rest as the full picture is not.

---

## 3. Norway — REPRODUCED, but the chart's subtitle is wrong

**Official source.** Statistics Norway (SSB), statistical article **"Siktelser og siktede personer etter innvandringsbakgrunn"**, published 2024-12-09 (updated 2024-12-17), attachment **`Tab 2-Siktelser (bosted).xlsx`**, sheet **"Tab2 Siktelser, menn 15-24 år"**, per-1,000 block, **column Y**, which sits under the block header **`BOSTED OSLO`** and the offence header **`¬ Vold og mishandling`**. These tables are a commissioned extract (*tabelloppdrag*), not a StatBank table — which is why the earlier lane found nothing in the open StatBank API. That earlier finding was correct about StatBank and wrong about SSB.

All nine plotted values match to two decimals:

| Chart label | Chart | SSB col Y | Charges N | Mean-annual pop |
|---|---|---|---|---|
| Norway | 32 | **31.88** (= ØVRIGE BOSATTE, residents without immigrant background) | 781 | 24,498.25 |
| Pakistan | 111 | **111.43** | 29 | 260.25 |
| Syria | 136 | **136.13** | 39 | 286.50 |
| Russia | 140 | **140.16** | 26 | 185.50 |
| Afghanistan | 160 | **160.78** | 66 | 410.50 |
| Eritrea | 241 | **241.07** | 54 | 224.00 |
| Iraq | 288 | **288.10** | 69 | 239.50 |
| Ethiopia | 289 | **289.42** | 39 | 134.75 |
| Somalia | 483 | **483.25** | 357 | 738.75 |

Arithmetic check: 357 ÷ 738.75 × 1,000 = 483.25. Exact.

**What "charges per 1,000 inhabitants" actually means here.** Four things the chart does not say:

1. **Oslo only.** Column Y is the `BOSTED OSLO` block. The whole-country column for the same population (column H) gives Somalia **269.86** and the non-immigrant baseline **35.21** — a ratio of 7.7 rather than the 15.2 the Oslo column implies.
2. **Men aged 15-24 only**, not inhabitants. The all-ages, whole-country figures (sheet "Tab2 Siktelser (bosted)", column H) are Somalia **78.12**, immigrants overall **18.39**, non-immigrant residents **9.70**.
3. **Cumulative over four years, 2020-2023.** The denominator is the *mean annual* population, so the numerator is four years of charges. Divide by four for an annual rate: Somalia 120.8 per 1,000 per year, the Norwegian baseline 8.0.
4. **Charges (siktelser), not persons.** One person can carry several charges; SSB's persons-charged table is a separate attachment (`Tab 3 - Siktede.xlsx`).

**Small numerators.** Ethiopia's 289.42 rests on **39 charges over 135 person-years**; Russia's 140.16 on **26 charges**; Pakistan's 111.43 on **29**. Only Somalia (357) has a numerator large enough for a stable rate. SSB blanks cells with small or disclosive counts, so the chart's country list is itself a survivorship selection.

**Re-pullable citation.** SSB, "Siktelser og siktede personer etter innvandringsbakgrunn", 2024-12-09, table 2 (bosted), sheet "Tab2 Siktelser, menn 15-24 år", column Y, rows 89 / 112 / 114-117 / 119 / 121-122. Local copy: `norway/ssb_tab2_siktelser_per1000.xlsx`.

---

## 4. Method

Finland: PxWeb v1 JSON-stat2 POST against `StatFin/rpk/13jg.px` and `13je.px`, metadata first, then a 26-year × 87-nationality × 6-measure grid; populations derived as count ÷ published rate × 10,000 (StatFin's own denominator, so no external population table is needed). Sweden: HTTP download of the Brå PDFs, `pdftotext -layout`, whitespace-column parse of pages 11-13. Norway: located the commissioned tables from the SSB article HTML, downloaded all four workbooks, then scanned every column of every sheet for the chart's nine values against the row labels — one column matched all nine.

## 5. Caveats

- The three charts are not comparable to one another. Finland counts suspect-events for one offence chapter by citizenship in one year; Sweden counts distinct persons suspected of any offence by country of birth over three years; Norway counts charges for one offence group by immigrant background over four years, restricted to young men in one city.
- None of the three adjusts for age or sex except Sweden's region-level standardisation, which the chart does not plot.
- All three rest on suspicion or charge, not conviction.
- Finland and Norway use registered population as denominator, so unregistered residents and short-stay visitors inflate rates where they offend.

## 6. Files

All paths under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/nordic/`.

- `nordic_tidy.csv` — 242 tidy rows, all three countries
- `build_csv.py` — builds the CSV from the raw pulls
- `finland/` — `meta_13jg.json`, `meta_13je.json`, `meta_11rm.json`, `req_13jg.json`, `req_13je.json`, `req_allyears.json`, `req_grid.json`, `req_xcheck.json`, `raw_13jg_2023.json`, `raw_13je_2023.json`, `raw_13jg_allyears.json`, `raw_13jg_grid.json`, `xcheck_13zk.json`, `fi_parsed.json`, `je_parsed.json`, `parse_fi.py`, `parse_je.py`, `sweep.py`, `grid.py`, `byyear.py`, `rpk_tables.json`
- `sweden/` — `bra_tabellbilaga1.pdf`, `bra_2021_9_rapport.pdf`, `bra_page.html`, `bra_tab1.txt`, `b6_raw.txt`
- `norway/` — `ssb_tab2_siktelser_per1000.xlsx`, `ssb_tab1a_siktelser_bosted.xlsx`, `ssb_tab1b_siktelser_gjerningssted.xlsx`, `ssb_tab3_siktede.xlsx`, `ssb2020_tab2.xlsx` (2015-2018 predecessor), `ssb_article.html`, `ssb_article_prev.html`

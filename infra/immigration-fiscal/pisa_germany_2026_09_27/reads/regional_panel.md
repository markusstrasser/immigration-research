claude-opus-5-5

**Verdict:** see final Verdict line at the end (2012→2022 math: 34 regions; 2018→2022 reading: 39; 2015 scores [GAP])

# PISA adjudicated-region panel (2012, 2015, 2018, 2022): natives' math/reading and immigrant share

Scope: sub-national units with their own PISA results; non-immigrant mean math and reading (SE), immigrant-background
share (SE), first-generation share where published. Builder: `acquire_regional.py` → `derived/regional_panel.csv`,
from `_cache/` only.

## Findings log (appended per source)

- [PENDING] 2022 Vol I annex B2 (statlink ax46rt).
- 2022: `_cache/statlink_ax46rt.xlsx` (PISA 2022 Vol I annex B2, doi 10.1787/53f23881-en). Sheet 'Table I.B2.36' header
  quoted: "Percentage of students with an immigrant background | Based on students' reports | Non-immigrant students |
  Immigrant students | All immigrant students | Second-generation immigrant students | First-generation immigrant
  students | % | S.E." 'Table I.B2.39' header: "Mathematics performance of students with an immigrant background ...
  All students | Non-immigrant students | Immigrant students ... Mean score | S.E.". 'Table I.B2.40' = reading, same
  layout. Regions (2022): Belgium 3 communities; Canada 10 provinces; Colombia Bogotá; Italy Bolzano, Trento; Spain
  17 communities + Ceuta, Melilla; UK England, N. Ireland, Scotland, Wales; Brazil 5 macro-regions; Kazakhstan 17;
  Mongolia 3; Viet Nam 3. No Australia, Mexico or US states in 2022. [SOURCE: stat.link/files/53f23881-en/ax46rt.xlsx]
- 2018: the Vol II PDF (mirror abdigm.meb.gov.tr, `_cache/pisa2018_vol2.pdf`) line 23872 quotes "Annex B2 List of
  tables available on line https://doi.org/10.1787/888934038780", including "WEB Table II.B2.72 Socio-economic status,
  by immigrant background" and "WEB Table II.B2.74 Mean reading performance and academic resilience, by immigrant
  background". Old-style StatLink DOIs redirect (302) to `statlinks.oecdcode.org/EDU-2019-4229-EN-T016.XLSX`; cached as
  `_cache/statlink_888934038780.xlsx` (3,093,499 bytes). II.B2.74 header quoted: "Percentage of immigrant students | % |
  S.E. | ... Reading performance | Average performance | Non-immigrant students | Immigrant students |
  Second-generation | First-generation | Mean score | S.E.". So 2018 has natives' READING and the immigrant share by
  region, but no first-generation SHARE column. [GAP] 2018 natives' MATH by region: no annex B2 table in Vol II's list
  splits math by immigrant background (II.B2.3 and II.B2.49 split by ESCS and gender only).
- 2012: the Vol II PDF (`_cache/pisa2012_vol2.pdf`, downloaded by a peer lane; my text dump `_cache/reg_pisa2012_vol2.txt`)
  lists "Table B2.II.9 Mathematics performance and immigrant background, by region" with StatLink
  "http://dx.doi.org/10.1787/888932964965", which redirects to `statlinks.oecdcode.org/982013051P1T005.XLS`; cached as
  `_cache/statlink_888932964965.xls` (2,266,112 bytes). Header quoted: "Percentage of students | Non-immigrant |
  Immigrant | % | S.E. | ESCS | Mathematics performance | Non-immigrant | Immigrant | Mean score | S.E.". Row check:
  "Australian capital territory | 83.847 | 1.483 | 16.153 | 1.483 | ... | 520.770 | 3.652", matching the PDF's "83.8
  (1.5) 16.2 (1.5) ... 521 (3.7)". Regions: Australia 8, Belgium 3, Canada 10, Italy 21 incl. Bolzano/Trento, Mexico
  32, Spain, UK, US states and others. [GAP] 2012: no natives' READING and no first-generation share in this table
  (Vol II annex B2 is mathematics only; 2012 math was the major domain).
- Microdata sizes (`curl -sI`, 2026-09-28): webfs.oecd.org/pisa2018/SPSS_STU_QQQ.zip content-length 500,959,458 bytes;
  pisa2022/STU_QQQ_SPSS.zip 682,364,259 bytes; pisa2015 PUF_SPSS_COMBINED_CMB_STU_QQQ.zip 404 (name to be found).
- 2015: the Vol I PDF (mirror iave.pt, `_cache/reg_pisa2015_vol1.pdf`, text `_cache/reg_pisa2015_vol1.txt`) lists the
  only regional immigrant tables as "WEB Table B2.I.71 Percentage of students with an immigrant background" and
  B2.I.72. Annex B2 StatLink "http://dx.doi.org/10.1787/888933433235" redirects to
  `statlinks.oecdcode.org/982016061P1T010.XLSX`; cached `_cache/statlink_888933433235.xlsx` (5,427,806 bytes).
  B2.I.71 header quoted: "Non-immigrant students | Immigrant students | Second-generation immigrants | First-generation
  immigrants | % | S.E." B2.I.72 header quoted: "Differences in science performance between immigrant and
  non-immigrant students ... Science performance | Non-immigrant students | ... Mean score". [GAP] 2015 natives' MATH
  and READING by region: not tabulated; only science is split. The share and first-generation share are present.
- Microdata (if the parent takes the student-file route): webfs.oecd.org/pisa/PUF_SPSS_COMBINED_CMB_STU_QQQ.zip
  (2015) content-length 440,232,149 bytes. With 2018 (500,959,458) and 2022 (682,364,259) that is 1.62 GB before
  2012 (file name not found on webfs; the 2012 files are far smaller). Total is well under 10 GB. [GAP] 2012 student
  file URL not resolved.

## Builder

`acquire_regional.py` reads only the four cached workbooks, checks each header cell it uses (fails loudly on a layout
change), strips footnote asterisks, harmonizes labels through `COUNTRY_MAP`/`REGION_MAP` (e.g. "Australian capital
territory" → "Australian Capital Territory", "Bogota" → "Bogotá", "Russian Federation" → "Russia"), refuses duplicate
region-cycle keys, keeps regions present in ≥2 cycles, and writes values at 4 decimals. `c`/`m` cells become blanks.
Run twice: both runs `shasum` 97cd4096c66aa95d57ff2045643b2f1ceb35bbb6 [CALCULATION: acquire_regional.py].
Output: 219 rows, 74 regions; 103 single-cycle regions dropped (all Mexican states, Australian states and 16 Italian
regions exist only in 2012; Viet Nam, Mongolia only in 2022; US states other than Massachusetts once each).

Spot check against the source: Ontario 2012 natives' math 515.4963 (SE 4.2076), immigrant share 43.5163, matching the
PDF's "515 (4.2)" and "43.5 (3.0)" [DATA: derived/regional_panel.csv; SOURCE: B2.II.9].

## What the panel can and cannot identify

| Cycle | natives' math | natives' reading | immigrant share | first-gen share |
|---|---|---|---|---|
| 2012 | yes (B2.II.9) | [GAP] | yes | [GAP] |
| 2015 | [GAP] | [GAP] | yes | yes (B2.I.71) |
| 2018 | [GAP] | yes (II.B2.74) | yes | [GAP] |
| 2022 | yes (I.B2.39) | yes (I.B2.40) | yes | yes (I.B2.36) |

- Natives' MATH change 2012→2022: 34 regions (Belgium 3, Canada 10, Italy Bolzano and Trento, Spain 14, UK 4,
  Bogotá) [CALCULATION].
- Natives' READING change 2018→2022: 39 regions (Kazakhstan 14, Canada 10, Brazil 5, UK 4, Belgium 3, Bolzano,
  Trento, Bogotá) [CALCULATION]. Spain's 19 communities have blank 2018 reading: the II.B2.74 cells are not numeric
  (OECD withheld Spain's 2018 reading results [TRAINING-DATA: anomalous response patterns; verify in the 2018 Vol I
  annex A9 note]). Brazil and Kazakhstan have immigrant shares near zero (Brazil North 2022: 0.48%), so they add
  little variance in the regressor; without them the reading design has 20 regions.
- The share series runs all four cycles for 34 regions, so a lagged or cumulative share (the operator's addendum) can
  be built from tables. Natives' scores cannot be built for 2015 at all, nor math for 2018, nor reading for 2012.
- Caveat: an asterisk marks regions that missed a PISA sampling standard (e.g. 2022 Canada's Alberta, BC, Manitoba,
  Newfoundland, Nova Scotia, Ontario, Quebec; all four UK countries; 2015 Spanish communities). The builder strips it;
  the flag is not carried in the CSV. [GAP] add a `flag` column if the parent wants to drop flagged cells.
- Italy's macro-areas (Nord-Ovest etc.) are not in any of these annex B2 workbooks. [GAP]
- Australia's states and US states: 2012 only in the tables (Massachusetts 2012+2015 shares).

Next queries if re-dispatched: (1) the student files 2012–2022 (≈2 GB total) with PV1–10MATH/READ, W_FSTUWT and 80
BRR replicate weights, region from STRATUM/SUBNATIO, would fill every [GAP] above and allow Australian states 2015–2022;
(2) PISA 2015 Vol I annex B2 B2.I.72 gives natives' SCIENCE 2015, usable as a 2015 point on the science scale.

## Regions and cycles (panel rows; n = cycles present)

- Argentina / CABA: 2012, 2018 (n=2)
- Belgium / Flemish community: 2012, 2015, 2018, 2022 (n=4)
- Belgium / French community: 2012, 2015, 2018, 2022 (n=4)
- Belgium / German-speaking community: 2012, 2015, 2018, 2022 (n=4)
- Brazil / Middle-West: 2018, 2022 (n=2)
- Brazil / North: 2018, 2022 (n=2)
- Brazil / Northeast: 2018, 2022 (n=2)
- Brazil / South: 2018, 2022 (n=2)
- Brazil / Southeast: 2018, 2022 (n=2)
- Canada / Alberta: 2012, 2015, 2018, 2022 (n=4)
- Canada / British Columbia: 2012, 2015, 2018, 2022 (n=4)
- Canada / Manitoba: 2012, 2015, 2018, 2022 (n=4)
- Canada / New Brunswick: 2012, 2015, 2018, 2022 (n=4)
- Canada / Newfoundland and Labrador: 2012, 2015, 2018, 2022 (n=4)
- Canada / Nova Scotia: 2012, 2015, 2018, 2022 (n=4)
- Canada / Ontario: 2012, 2015, 2018, 2022 (n=4)
- Canada / Prince Edward Island: 2012, 2015, 2018, 2022 (n=4)
- Canada / Quebec: 2012, 2015, 2018, 2022 (n=4)
- Canada / Saskatchewan: 2012, 2015, 2018, 2022 (n=4)
- Colombia / Bogotá: 2012, 2015, 2018, 2022 (n=4)
- Colombia / Cali: 2012, 2015 (n=2)
- Colombia / Manizales: 2012, 2015 (n=2)
- Colombia / Medellín: 2012, 2015 (n=2)
- Italy / Bolzano: 2012, 2015, 2018, 2022 (n=4)
- Italy / Campania: 2012, 2015 (n=2)
- Italy / Lombardia: 2012, 2015 (n=2)
- Italy / Sardegna: 2012, 2018 (n=2)
- Italy / Toscana: 2012, 2018 (n=2)
- Italy / Trento: 2012, 2015, 2018, 2022 (n=4)
- Kazakhstan / Akmola region: 2018, 2022 (n=2)
- Kazakhstan / Aktobe region: 2018, 2022 (n=2)
- Kazakhstan / Almaty: 2018, 2022 (n=2)
- Kazakhstan / Almaty region: 2018, 2022 (n=2)
- Kazakhstan / Astana: 2018, 2022 (n=2)
- Kazakhstan / Atyrau region: 2018, 2022 (n=2)
- Kazakhstan / East-Kazakhstan region: 2018, 2022 (n=2)
- Kazakhstan / Karagandy region: 2018, 2022 (n=2)
- Kazakhstan / Kostanay region: 2018, 2022 (n=2)
- Kazakhstan / Kyzyl-Orda region: 2018, 2022 (n=2)
- Kazakhstan / North-Kazakhstan region: 2018, 2022 (n=2)
- Kazakhstan / Pavlodar region: 2018, 2022 (n=2)
- Kazakhstan / West-Kazakhstan region: 2018, 2022 (n=2)
- Kazakhstan / Zhambyl region: 2018, 2022 (n=2)
- Spain / Andalusia: 2012, 2015, 2018, 2022 (n=4)
- Spain / Aragon: 2012, 2015, 2018, 2022 (n=4)
- Spain / Asturias: 2012, 2015, 2018, 2022 (n=4)
- Spain / Balearic Islands: 2012, 2015, 2018, 2022 (n=4)
- Spain / Basque Country: 2012, 2015, 2018, 2022 (n=4)
- Spain / Canary Islands: 2015, 2018, 2022 (n=3)
- Spain / Cantabria: 2012, 2015, 2018, 2022 (n=4)
- Spain / Castile and Leon: 2012, 2015, 2018, 2022 (n=4)
- Spain / Castile-La Mancha: 2015, 2018, 2022 (n=3)
- Spain / Catalonia: 2012, 2015, 2018, 2022 (n=4)
- Spain / Ceuta: 2018, 2022 (n=2)
- Spain / Comunidad Valenciana: 2015, 2018, 2022 (n=3)
- Spain / Extremadura: 2012, 2015, 2018, 2022 (n=4)
- Spain / Galicia: 2012, 2015, 2018, 2022 (n=4)
- Spain / La Rioja: 2012, 2015, 2018, 2022 (n=4)
- Spain / Madrid: 2012, 2015, 2018, 2022 (n=4)
- Spain / Melilla: 2018, 2022 (n=2)
- Spain / Murcia: 2012, 2015, 2018, 2022 (n=4)
- Spain / Navarre: 2012, 2015, 2018, 2022 (n=4)
- United Arab Emirates / Abu Dhabi: 2012, 2015 (n=2)
- United Arab Emirates / Ajman: 2012, 2015 (n=2)
- United Arab Emirates / Dubai: 2012, 2015 (n=2)
- United Arab Emirates / Fujairah: 2012, 2015 (n=2)
- United Arab Emirates / Ras Al Khaimah: 2012, 2015 (n=2)
- United Arab Emirates / Sharjah: 2012, 2015 (n=2)
- United Arab Emirates / Umm Al Quwain: 2012, 2015 (n=2)
- United Kingdom / England: 2012, 2015, 2018, 2022 (n=4)
- United Kingdom / Northern Ireland: 2012, 2015, 2018, 2022 (n=4)
- United Kingdom / Scotland: 2012, 2015, 2018, 2022 (n=4)
- United Kingdom / Wales: 2012, 2015, 2018, 2022 (n=4)
- United States / Massachusetts: 2012, 2015 (n=2)

**Verdict (final):** the annex tables give a usable regional panel for natives' math 2012→2022 (34 regions: Spain 14, Canada 10, UK 4, Belgium 3, Bolzano, Trento, Bogotá) and reading 2018→2022 (39 regions, only 20 outside low-immigration Brazil and Kazakhstan; Spain's 2018 reading is blank), with immigrant shares in all four cycles; natives' scores for 2015 (both subjects), math 2018 and reading 2012 are not tabulated, and the student files that would fill them total about 2 GB, under the 10 GB cap, so the parent decides whether to take the microdata route.

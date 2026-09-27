claude-opus-5-5

**Verdict:** 2006 native means are in hand for all three subjects (PISA 2015 Vol I, 36 of 37 OECD countries), and 2009 native means for reading only (PISA 2018 Vol II, 36 of 37); 2009 math and science by immigrant background are not published and need the 2009 student file.

# PISA 2006 and 2009 native (non-immigrant) means and immigrant shares — acquisition log

Scope: country means for non-immigrant students and the immigrant-background share, 2006 and 2009, every OECD and
European country, per subject with SEs, so native changes 2006→2012 and 2009→2012 can be computed against the
lane's 2012 values (`derived/crosscountry.csv`, PISA 2022 Vol I Tables I.B1.7.2/7.18).

Outputs: `acquire_pretrend.py` → `derived/pretrend_inputs.csv` (built from `_cache/` only).

## Log

- [DONE] located StatLink ids for PISA 2015 Vol I ch.7, PISA 2018 Vol II ch.9, PISA 2012 Vol II ch.3, PISA 2009 Vol II.
- Sources located (2026-09-28). All StatLinks resolve by curl through doi.org → statlinks.oecdcode.org (old numeric DOIs):
  - PISA 2015 Vol I PDF: `https://www.oecd.org/content/dam/oecd/en/publications/reports/2016/12/pisa-2015-results-volume-i_g1g7397c/9789264266490-en.pdf` (oecd.org content/dam is NOT Cloudflare-walled to curl). Ch.7 annex workbook `http://dx.doi.org/10.1787/888933433226` holds Tables I.7.1 (shares 2006 and 2015) and I.7.15a/b/c (science/reading/math by immigrant background, 2006 and 2015). [SOURCE: pisa2015_vol1.txt lines 33608–35584, every ch.7 table cites 888933433226]
  - PISA 2018 Vol II PDF: mirror `https://iaqse.caib.es/documentos/avaluacions/pisa/pisa_2018/pisa2018-oecd-vol2-en.pdf`. Ch.9 annex workbook `https://doi.org/10.1787/888934038742` holds Tables II.B1.9.9 (shares 2009 and 2018) and II.B1.9.10 (reading by immigrant background, 2009 and 2018).
  - PISA 2009 Vol II PDF: `https://www.oecd.org/content/dam/oecd/en/publications/reports/2010/12/pisa-2009-results-overcoming-social-background_g1g114f2/9789264091504-en.pdf`. Table II.4.1 (reading only) = `http://dx.doi.org/10.1787/888932343285` (cross-check of the 2009 reading values).
  - PISA 2012 Vol II PDF: mirror `https://www.meb.gov.tr/earged/oecd/PISA%202012-vol2%20(eng)--eBook7.pdf`. Its immigrant tables (II.3.4a/b, II.3.6a/b) give 2003 and 2012 math only; no 2006 or 2009. Table II.3.4a = `888932964927`.
- [GAP] 2009 mathematics and science by immigrant background: no published table found. PISA 2009 Vol II ch.4 tables are reading-only (Table II.4.1 title: "Percentage of students and reading performance, by immigrant status"); PISA 2018 Vol II ch.9 trend tables are reading-only; PISA 2012 Vol II trend tables compare 2003 with 2012. Closing it needs the PISA 2009 student file (plausible values, final weights, BRR replicate weights).

## Extraction (acquire_pretrend.py → derived/pretrend_inputs.csv)

Run: `uv run --no-project --with openpyxl --with xlrd python3 acquire_pretrend.py` (xlrd reads the pre-2014 `.xls`
StatLinks). Two runs give the same `shasum`: `2b678ad42c30f07e758f137db22943bcb6d5e5c7` both times [CALCULATION:
shasum after each run, 2026-09-28]. Rows: 2006 science 53, 2006 reading 52, 2006 math 53, 2009 reading 71, 2012 math
64 (cross-check rows) [CALCULATION: acquire_pretrend.py stdout]. `nat_mean` = mean of non-immigrant students;
`imm_share` = immigrant-background share (first + second generation), % of students with valid data.

Column map (quoted headers from the workbooks):
- 2006 means: Tables I.7.15a/b/c, block "Science|Reading|Mathematics performance in PISA 2006" → "Non-immigrant
  students" "Mean score", "S.E.". 2006 share: Table I.7.1, block "PISA 2006" → "Immigrant students" "%", "S.E."
  [SOURCE: `_cache/statlink_888933433226.xlsx`].
- 2009 reading means: Table II.B1.9.10, block "PISA 2009" → "Non-immigrant" "Mean score", "S.E."; share: Table
  II.B1.9.9, block "PISA 2009" → "Immigrant" "%", "S.E." [SOURCE: `_cache/statlink_888934038742.xlsx`].
- 2009 fallback (7 countries not in the 2018 volume: Azerbaijan, Dubai (UAE), Kyrgyzstan, Liechtenstein,
  Shanghai-China, Trinidad and Tobago, Tunisia): PISA 2009 Vol II Table II.4.1, "Native students" mean and
  "Students with an immigrant background (first- or second-generation)" "Percentage of students" [SOURCE:
  `_cache/statlink_888932381418.xls`, sheet T.II.4.1]. `source` column names the table on every row.
- 2012 cross-check: PISA 2012 Vol II Table II.3.4a, "Mathematics performance" "Non-immigrant" "Mean score", and
  "Percentage of students" "Immigrant" [SOURCE: `_cache/statlink_888932964927.xls`].

Spot values: Germany 2006 science 531.8 (SE 3.2), 2006 share 14.2% (SE 1.0); 2009 reading 511.2 (SE 2.6), 2009
share 17.6% (SE 1.0). Sweden 2006 science 512.0, share 10.8%; 2009 reading 507.0, share 11.7%. Poland 2006 share
0.19%, 2009 0.03% [DATA: derived/pretrend_inputs.csv].

## Cross-checks

- 2009 reading, PISA 2018 Vol II against the original PISA 2009 Vol II Table II.4.1: 57 overlapping countries, max
  |difference| 0.0002 points (Qatar) [CALCULATION: acquire_pretrend.py stdout]. The 2018 volume reprints 2009 as
  originally scaled.
- 2012 math, PISA 2012 Vol II against the lane's `crosscountry.csv` (PISA 2022 Vol I): 59 countries, median
  |difference| 0.19 points, OECD max 1.41 (New Zealand), then UK 1.27, Belgium 0.99; overall max Brazil 2.85.
  Germany 528.43 vs 527.86 (0.56). Shares agree within 0.37 pp (Sweden 14.53 vs 14.90; Germany 13.12 vs 13.45)
  [CALCULATION: inline check against derived/crosscountry.csv, 2026-09-28]. So the older volumes and the 2022 volume
  put 2012 on the same footing within about 1 point; the 2022 volume recomputed 2012 slightly (cause not stated).
  [INFERENCE] For 2006→2012 and 2009→2012 native changes, differencing against the lane's 2012 values adds under
  1.5 points of cross-volume noise for OECD countries.

## Definitions and caveats (quoted)

- Definition (PISA 2015 Vol I Annex A1): "(1) non-immigrant students (those students who had at least one parent
  born in the country), (2) second-generation immigrant students (those born in the country of assessment but whose
  parent(s) were born in another country) and (3) first-generation immigrant students ... Students with missing
  responses for either the student or for both parents were assigned missing values for this variable." [SOURCE:
  `_cache/pisa2015_vol1.txt` l.20660–20669]. Shares are therefore % of students with valid immigrant status; the
  missing are dropped from numerator and denominator. PISA 2018 Vol II uses the same definition (l.11484–11493).
- Germany: "Information on immigrant background is missing for 13.4% of the students included in Germany's PISA
  2015 sample, the highest percentage among all participating countries/economies ... The percentage of missing
  data on the student immigrant background variable in Germany has been high across PISA assessments (Table A5.10).
  For these reasons, results for Germany should be interpreted with caution." [SOURCE: l.19536–19540]. Every Germany
  row in Tables I.7.1–I.7.15 carries this note. The German national report's share including "nicht zuzuordnen"
  (17.6% → 12.8%, see reads/de_national_report_and_iqb.md) is the relevant sensitivity.
- Switzerland: "the increase in the weighted share of students with an immigrant background between previous rounds
  of PISA and PISA 2015 samples is larger than the corresponding shift in the target population according to
  official statistics" [SOURCE: l.33604–33605]. Affects Swiss 2006 vs later share changes.
- Austria 2009: PISA 2009 Vol II prints Austria (native reading 482.0, share 15.2%), but PISA 2018 Vol II lists
  Austria 2009 as "m" throughout Tables II.B1.9.9/9.10. The script follows the 2018 volume and writes no Austria
  2009 row. [INFERENCE] The 2018 volume treats Austria's 2009 data as not trend-comparable; I did not locate the
  OECD sentence stating why in this pass.
- Scale linking: past results are reported "as originally scaled"; PISA 2015 Annex A5 compares them with results
  rescaled under the 2015 approach and names large departures: Colombia science 2006→2015 ("almost entirely due to
  changes in the approach to scaling"), US science (+7 reported, +15 rescaled), Korea reading 2009→2015 (−22
  reported, −9 rescaled), Thailand reading, Denmark reading (+5 reported, +15 rescaled) [SOURCE: l.22560–22595].
  2006 science is a major-domain anchor for science; 2006 reading and math are minor domains (reading linked to the
  2000 scale, math to 2003), and 2009 reading is the major-domain anchor for reading. [TRAINING-DATA] on the anchor
  years; not verified in these PDFs.
- Missing cells: United States 2006 reading is "m" (the 2006 US reading results were withdrawn); Costa Rica did
  not take PISA 2006. [TRAINING-DATA] for the US withdrawal reason; the "m" is in Table I.7.15b.

## Coverage (countries with a native mean; every such row also carries a share)

Against the 37 OECD countries in `crosscountry.csv` (Luxembourg is absent from that list but present here):
| cycle, subject | OECD | missing | European partners (of 17 listed) |
|---|---|---|---|
| 2006 science | 36/37 | Costa Rica | 5 (Bulgaria, Croatia, Montenegro, Romania, Russia) |
| 2006 reading | 35/37 | Costa Rica, United States | 5 |
| 2006 math | 36/37 | Costa Rica | 5 |
| 2009 reading | 36/37 | Austria | 11 |
| 2009 math, science | 0 | not published | 0 |
[CALCULATION: inline coverage check over derived/pretrend_inputs.csv, 2026-09-28]

- [GAP] 2009 math and science by immigrant background. Route: PISA 2009 student file (webfs.oecd.org), PV1–5MATH /
  PV1–5SCIE, W_FSTUWT, 80 Fay BRR weights, IMMIG. Check file size first.
- [GAP] 2006 values for European partners outside PISA 2015 (Serbia, Liechtenstein, and others): PISA 2006 "Science
  Competencies for Tomorrow's World" Vol 2, ch.4 tables by immigrant status; StatLinks via the same doi.org route.
- [GAP] 2003 math by immigrant background is available at no extra cost in PISA 2012 Vol II Table II.3.4b/II.3.6b
  (StatLink 888932964927, already cached) if a longer pre-trend is wanted.

**Verdict:** 2006 non-immigrant means and shares (all three subjects; 36/37 OECD in science and math, 35/37 in reading) and 2009 reading (36/37 OECD, Austria withheld by OECD) are in `derived/pretrend_inputs.csv`, byte-reproducible and matching the older volumes' 2012 values within 1.5 points; 2009 math and science remain a [GAP] needing the student file.

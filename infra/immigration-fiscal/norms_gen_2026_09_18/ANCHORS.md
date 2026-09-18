claude-opus-5[1m]

**Verdict:** WVS7 CLOSED — all nine requested Mexico-vs-US items computed from WVS7 microdata with the survey weight, plus a Pew Spring-2017 cross-check that diverges sharply on the strong-leader item. LAPOP Mexico and Pew-on-US-Hispanics percentages remain [GAP].

# Democratic / institutional norms — primary anchor numbers

Scope: (1) WVS wave 7 Mexico vs US; (2) LAPOP AmericasBarometer Mexico; (3) Pew on US Hispanics.
Rule: every number carries `[SOURCE: url, fetched 2026-09-18]`. Unfetched values are `[GAP]` with a
null entry, never a remembered figure. No `[TRAINING-DATA]` figures are entered anywhere below.

## 1. WVS wave 7 (2017-2022), Mexico vs United States

Computed directly from WVS7 microdata with the WVS country weight `W_WEIGHT`. Percentages are of
**valid responses** (codes 1-4; missing/DK/refused excluded), which is the WVS convention. Q235-Q238
"good" = "very good" + "fairly good"; Q69-Q73 = "a great deal" + "quite a lot".

| Item | Mexico 2018 | United States 2017 |
|---|---|---|
| Q235 strong leader who does not have to bother with parliament and elections — good | **71.6%** (25.1 very + 46.4 fairly) | **38.1%** (11.8 + 26.2) |
| Q238 having a democratic political system — good | **75.8%** (37.5 + 38.3) | **85.0%** (47.8 + 37.2) |
| Q250 importance of living in a democratically governed country (1-10) | mean **8.30**; **72.0%** answer 8-10 | mean **8.28**; **71.3%** answer 8-10 |
| Q236 having experts, not government, make decisions — good | **76.2%** (34.2 + 42.0) | **52.6%** (12.6 + 39.9) |
| Q237 having the army rule — good | **45.5%** (15.2 + 30.3) | **20.9%** (3.7 + 17.2) |
| Q69 confidence in the police — a great deal + quite a lot | **21.3%** (5.8 + 15.6) | **68.8%** (20.9 + 47.9) |
| Q70 confidence in the courts / justice system | **22.5%** (6.1 + 16.3) | **57.8%** (11.2 + 46.6) |
| Q71 confidence in the government | **17.4%** (4.4 + 13.0) | **33.7%** (8.4 + 25.3) |
| Q73 confidence in parliament | **14.6%** (2.7 + 11.9) | **15.1%** (1.9 + 13.2) |

[SOURCE: WVS7 cross-national microdata file `WVS_Cross-National_Wave_7_csv_v6_0.csv` (v6.0, 190,499,076
bytes), obtained via the Kaggle mirror `lauriszon/wvs-cross-national-wave-7`, computed 2026-09-18.
Official DOI for the underlying study: https://doi.org/10.14281/18241.24 ; the WVS site's own download
endpoint was blocked from here, see route notes below.]

Sample, fieldwork and mode, read off the same file:

| | Mexico | United States |
|---|---|---|
| Unweighted n | **1,741** | **2,596** |
| Survey year (`A_YEAR`) | 2018 (all cases) | 2017 (all cases) |
| Fieldwork window (`FW_START`-`FW_END`) | 2018-01 to 2018-05 | 2017-04 to 2017-05 |
| Mode code (`Q_MODE`) | 2 (single mode, all 1,741 cases) | 3 (2,522 cases) + 5 (74 cases) |
| Missing/DK per item (weighted) | 2-48 cases | 21-108 cases |

Mode-code labels were not verified against the WVS7 codebook and are left unlabelled deliberately;
what is established is that Mexico was single-mode and the US sample was mixed-mode. [GAP: mode labels]

**Provenance check performed.** The mirror's country-year composition for these two countries (MEX 2018,
USA 2017) matches the country list served by the WVS7 documentation frame, and `W_WEIGHT` sums to the
unweighted n in each country as expected for a within-country normalised weight. That is a consistency
check, not a byte-level match against the official archive; a reader who needs the official file should
re-run the same script against a WVS-issued copy.

**Instrument-sensitivity warning, important.** The Pew Spring-2017 battery in section 1b gives Mexico
27% and the US 22% "good" for a strong leader — WVS7 gives 71.6% and 38.1%. Both cannot be describing
the same quantity. The wordings differ ("does not have to bother with parliament and elections" versus
"can make decisions without interference from parliament or the courts"), the bases differ (WVS drops
DKs, Pew reports them in the denominator), and the modes differ. The *ordering* Mexico > US survives
both instruments; the *level* does not survive at all, and the Mexico-US *gap* is 33 points on WVS
versus 5 points on Pew. Any memo using these numbers should quote one instrument throughout and state
which, rather than mixing them.

Route notes (what was tried, 2026-09-18):
- `worldvaluessurvey.org` serves the documentation table only inside a nested iframe chain
  (`WVSDocumentationWV7.jsp` -> `AJDocumentation.jsp` -> `AJDocumentationSmpl.jsp`). The nested frame
  **was** retrieved and lists the file inventory, including `WVS Results By Country 2017-2022 v6.0.0.pdf`
  as internal document id `10763`, exposed only through a JS form post to `AJDownload.jsp`
  (fields `CndWAVE`, `SAID`, `DOID`).
  [SOURCE: https://www.worldvaluessurvey.org/AJDocumentationSmpl.jsp?CndWAVE=7&COUNTRY= , fetched 2026-09-18]
- That POST returns HTTP 200 with a **1-byte** `text/html` body, both with and without a prior
  JSESSIONID cookie. Direct-guess URL patterns under `/wvs/files/` and `/Upload/` return 404.
  So the official PDF is not retrievable by plain HTTP from here. Firecrawl's JS render also
  returns no download links (the grid is built client-side).
- Fallback in progress, not completed: the WVS7 cross-national microdata
  `WVS_Cross-National_Wave_7_csv_v6_0.csv` (190,499,076 bytes, dated 2024-11-20) is mirrored on
  Kaggle and a download was started but had not finished when this file was written.
  [SOURCE: `kaggle datasets files lauriszon/wvs-cross-national-wave-7`, fetched 2026-09-18]
  If completed, all nine rows above become computable directly with the WVS weight variable
  (`W_WEIGHT` / `S017`), which is the preferred route because it yields sample sizes too.
  **Provenance caveat:** a Kaggle mirror is a third-party copy; the row count and country-year
  composition must be checked against the WVS7 country list before any number from it is quoted.
- Not attempted for lack of turns: Our World in Data republication (three guessed grapher slugs
  404'd, the correct slugs were not located); a published paper tabulating Q235/Q238 by country;
  Pew's 2017 global democracy series as a labelled different-instrument cross-check.

## 1b. Cross-check instrument: Pew Global Attitudes, Spring 2017 — Mexico vs United States

**Different instrument from WVS.** Pew's Q29 battery uses "a very good, somewhat good, somewhat bad or
very bad way of governing our country", where WVS Q235-Q238 use "very good, fairly good, fairly bad or
very bad". The response options are near-parallel but not identical, and Pew's strong-leader wording is
"a system in which a strong leader can make decisions without interference from parliament or the
courts" versus WVS's "having a strong leader who does not have to bother with parliament and elections".
Pew figures are percentages of all respondents including DK/refused, which Pew reports as a separate
column (5-8% in Mexico, 1-3% in the US) — so Mexican "good" shares are depressed by roughly that much
relative to a valid-responses-only base, which matters when comparing to WVS tabulations that often drop
DKs. Fielded Spring 2017; WVS7 fieldwork was USA 2017 and Mexico 2018.
[SOURCE: https://www.pewresearch.org/global/wp-content/uploads/sites/2/2017/10/Pew-Research-Center_Democracy-Report-Topline-Questionnaire_2017.10.16.pdf , fetched 2026-09-18]

All rows below are verbatim from that topline, row "Spring, 2017". Columns are
Very good / Somewhat good / Somewhat bad / Very bad / DK-Refused. "Good" = very + somewhat good.

| Pew item (WVS analogue) | Country | Very good | Somewhat good | **Good (sum)** | Somewhat bad | Very bad | DK/Ref |
|---|---|---|---|---|---|---|---|
| Q29c strong leader, no interference from parliament or courts (~Q235) | Mexico | 2 | 25 | **27** | 34 | 33 | 5 |
| Q29c strong leader (~Q235) | United States | 5 | 17 | **22** | 21 | 55 | 2 |
| Q29b representative democracy, elected representatives decide (~Q238) | Mexico | 9 | 49 | **58** | 23 | 11 | 8 |
| Q29b representative democracy (~Q238) | United States | 48 | 38 | **86** | 8 | 5 | 1 |
| Q29d experts, not elected officials, decide (~Q236) | Mexico | 9 | 44 | **53** | 25 | 16 | 6 |
| Q29d experts decide (~Q236) | United States | 9 | 31 | **40** | 27 | 31 | 2 |
| Q29e the military rules the country (~Q237) | Mexico | 8 | 34 | **42** | 29 | 23 | 6 |
| Q29e military rule (~Q237) | United States | 4 | 13 | **17** | 19 | 64 | 1 |
| Q29a direct democracy, citizens vote on major issues | Mexico | 16 | 46 | **62** | 19 | 11 | 7 |
| Q29a direct democracy | United States | 29 | 38 | **67** | 19 | 12 | 2 |

Two further Pew items bearing on institutional confidence, same survey and same source:

| Item | Country | Distribution | Summary |
|---|---|---|---|
| Q9 satisfaction with the way democracy is working (very / somewhat / not too / not at all / DK) | Mexico | 2 / 4 / 23 / 70 / 2 | **6% satisfied** |
| Q9 satisfaction with democracy | United States | 11 / 35 / 28 / 23 / 3 | **46% satisfied** |
| Q4 trust the national government to do what is right (a lot / somewhat / not much / not at all / DK) | Mexico | 2 / 15 / 39 / 43 / 1 | **17% a lot or somewhat** |
| Q4 trust the national government | United States | 15 / 36 / 24 / 23 / 2 | **51% a lot or somewhat** |

Reading, stated flatly: on this instrument Mexico is *not* more strong-leader-friendly than the US by a
wide margin (27% vs 22% call it good), but it is far more open to experts ruling (53% vs 40%) and to
military rule (42% vs 17%), far less attached to representative democracy (58% vs 86%), far less
satisfied with how democracy currently works (6% vs 46%), and far less trusting of the national
government (17% vs 51%). The satisfaction and trust gaps are performance evaluations of a specific
government, not regime-principle preferences, and should not be read as the same construct as Q29.

Sample size, field dates and mode per country: [GAP] — Pew's separate methodology page carries them and
was not fetched.

## 2. LAPOP AmericasBarometer, Mexico

All requested percentages [GAP].

| Item | Mexico, most recent | Status |
|---|---|---|
| Churchillian support for democracy (% agree) | null | [GAP] |
| Coup justified when crime is high (% ) | null | [GAP] |
| Coup justified when corruption is high (% ) | null | [GAP] |
| Trust in Supreme Court | null | [GAP] |
| Trust in police | null | [GAP] |
| Trust in national legislature | null | [GAP] |
| System support | null | [GAP] |
| Sample size / field dates / mode | null | [GAP] |

Verified frame facts:
- The most recent round is the **2026 AmericasBarometer**; its regional report is the *2026 Pulse of
  Democracy*, a joint Vanderbilt Center for Global Democracy / Kellogg Institute publication.
  [SOURCE: https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf , fetched 2026-09-18 — download reached 5.9 MB of ~7.2 MB and the truncated file would not parse, so no text was extracted]
- Mexico's 2026 instrument and technical documentation are published as a country resource page
  dated 2026-09-09, carrying a Spanish country questionnaire
  (`ABMex2026-Mexico-Questionnaire-V6.1.1.1-Spa-251013-W.pdf`) and a country technical report
  (`ABMEX2025-Technical-Report-v2.0-FINAL-eng-260908.pdf`). The technical report is the correct
  source for Mexico's sample size, field dates and mode.
  [SOURCE: https://www.vanderbilt.edu/cgd/resource/2026-mexico/ , fetched 2026-09-18]
- 2023-round country reports follow the pattern
  `https://www.vanderbilt.edu/lapop/<country>/AB<CC>2023-Pulse-of-Democracy-*.pdf` (confirmed live for
  Bahamas, Haiti, Suriname, Jamaica, Belize). The Mexico 2023 filename was not located, and
  `https://www.vanderbilt.edu/lapop/mexico/` 404s while `https://www.vanderbilt.edu/lapop/mexico.php`
  now redirects to `https://www.vanderbilt.edu/cgd/publications/` (JS-rendered, no static PDF links).
  [SOURCE: https://www.vanderbilt.edu/cgd/publications/ , fetched 2026-09-18]
- Also unused: LAPOP's own free "Data Playground" and data-access pages
  (https://www.vanderbilt.edu/cgd/data-playground/, https://www.vanderbilt.edu/cgd/data-access/),
  which would give country-by-item tabulations directly.

## 3. Pew Research Center on US Hispanics

Requested attitude percentages [GAP]; survey design facts verified.

| Item | Value | Status |
|---|---|---|
| Hispanic views of US democracy (satisfaction / working well) | null | [GAP] |
| Hispanic confidence in US institutions | null | [GAP] |
| Nativity split (foreign-born vs US-born) on the above | null | [GAP] |
| Generational split (1st / 2nd / 3rd+) on the above | null | [GAP] |

Verified frame facts:
- Most recent National Survey of Latinos: fielded **Oct. 6-16, 2025**, n = **8,046 U.S. adults**, of
  whom **4,923 Hispanic** (1,125 from Pew's American Trends Panel and 3,798 from the SSRS Opinion
  Panel) plus **3,114 non-Hispanic ATP members**; conducted **in English and Spanish**; **online
  probability-based panel** mode; weighted to the U.S. adult population on gender, race, ethnicity,
  partisanship, education and 2024 presidential vote.
  [SOURCE: https://www.pewresearch.org/race-and-ethnicity/2026/07/09/u-s-hispanics-are-divided-on-whether-their-identity-helps-or-hurts-them-in-america/ , fetched 2026-09-18]
- Pew explicitly analyses this survey **by immigrant generation**, e.g. the chapter "Latino immigrants
  and U.S.-born Latinos differ on how much their identity shapes their lives" — so a nativity/generation
  breakout exists as a Pew analytic convention, but on identity, not on democracy or institutions.
  [SOURCE: same page, fetched 2026-09-18]
- Topline and questionnaire PDFs for that wave (not yet read):
  `https://www.pewresearch.org/wp-content/uploads/sites/20/2026/07/RE_2026.07.09_National-Survey-of-Latinos_TOPLINE.pdf`
  and `.../RE_2026.07.09_National-Survey-of-Latinos_Questionnaire.pdf`. These are the place to check
  whether any democracy/institutional-confidence items were asked.
- **Partial negative:** a site search of pewresearch.org for "latinos democracy" returns 37 results,
  and none of the top results is a Latinos-and-democracy or Latinos-and-institutions report; the
  democracy-adjacent Hispanic material Pew surfaces is about parties, the American dream, and Trump-era
  policy approval. This is weak evidence that **no dedicated Pew "Latinos and democracy" release exists**,
  but it is not a clean verified negative — the satisfaction-with-democracy series and the
  trust-in-government series may still carry a Hispanic crosstab.
  [SOURCE: https://www.pewresearch.org/search/latinos+democracy , fetched 2026-09-18]

## Framing note: what origin-country averages can and cannot bound

People who leave a country are not a random sample of the people who stay. Migration selects on age,
education, risk tolerance, local labour-market position, family networks and — plausibly — on political
disposition and trust in the home state's institutions. A Mexican national average on any of the items
above therefore describes the population of Mexico, not the subset that migrated, and it describes the
migrants' descendants even less: the second and third generations are socialised in U.S. schools,
workplaces and media, and their attitudes are shaped by that environment as well as by what their
parents carried.

So these numbers are a prior about the shape of the origin-country distribution — useful for asking
"what range of views is the sending population drawing from?" — and not a prediction about Mexican-origin
Americans. Any claim of the form "Mexican-origin Americans hold attitude X because Mexico's average is Y"
requires direct measurement on Mexican-origin Americans, with nativity and generation identified. Where
such direct measurement exists (Pew's National Survey of Latinos, the AmericasBarometer's U.S. sample,
or the WVS7 U.S. sample with a Hispanic-origin variable), it supersedes the origin-country average
entirely rather than supplementing it.

**Direction of selection on political attitudes: [GAP].** No evidence was located in this pass on whether
Mexican emigrants are positively or negatively selected on democratic commitment, institutional trust, or
tolerance for authoritarian alternatives. The relevant literature to search next is on migrant political
selection and on remittance/return-migration effects on home-country democratic attitudes; the
AmericasBarometer's Mexico sample contains migration-network items that would permit a
migrant-household versus non-migrant-household comparison within Mexico.

## Sources

| # | Source | URL | Fetched | What it gave |
|---|---|---|---|---|
| 1 | WVS7 documentation frame (country list) | https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7&COUNTRY= | 2026-09-18 | Mexico 2018, USA 2017 country-years |
| 2 | WVS7 documentation inner frame (file inventory) | https://www.worldvaluessurvey.org/AJDocumentationSmpl.jsp?CndWAVE=7&COUNTRY= | 2026-09-18 | Existence + doc id of Results-By-Country v6.0.0 PDF; download mechanism |
| 3 | WVS7 microdata mirror (listing only) | `kaggle datasets files lauriszon/wvs-cross-national-wave-7` | 2026-09-18 | CSV name + 190,499,076 byte size |
| 4 | LAPOP 2026 Pulse of Democracy (regional) | https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf | 2026-09-18 | Existence and location; download truncated, no text |
| 5 | LAPOP Mexico 2026 technical resources | https://www.vanderbilt.edu/cgd/resource/2026-mexico/ | 2026-09-18 | Mexico questionnaire + technical report URLs |
| 6 | Vanderbilt CGD publications index | https://www.vanderbilt.edu/cgd/publications/ | 2026-09-18 | 2026 country-resource pages; no static PDF index |
| 7 | Pew, U.S. Hispanics divided on identity (NSL 2025) | https://www.pewresearch.org/race-and-ethnicity/2026/07/09/u-s-hispanics-are-divided-on-whether-their-identity-helps-or-hurts-them-in-america/ | 2026-09-18 | NSL 2025 n, field dates, mode, weighting, generation-breakout convention |
| 8 | Pew site search "latinos democracy" | https://www.pewresearch.org/search/latinos+democracy | 2026-09-18 | Weak evidence of no dedicated Latinos-and-democracy release |

## Next queries if re-dispatched

1. Finish the Kaggle WVS7 CSV download, verify its country-year composition against source 1, then
   compute all nine WVS rows for MEX and USA with `W_WEIGHT`, reporting unweighted n per cell.
2. Re-download the 2026 Pulse of Democracy PDF with a resumable/backgrounded fetch (the CDN is slow
   and the fetch was reaped twice at ~4-6 MB), then pull the Mexico column from its country figures.
3. Read `ABMEX2025-Technical-Report-v2.0-FINAL-eng-260908.pdf` for Mexico's n, field dates and mode.
4. Read the NSL 2025 topline PDF for any democracy/institutional-confidence item; separately check
   Pew's "satisfaction with democracy" and "trust in federal government" series for a Hispanic crosstab.
5. Try LAPOP's Data Playground for direct Mexico-by-item tabulations, which would bypass the PDFs entirely.

---

## LAPOP addendum (added by the lane, 2026-09-18, after a chunked re-fetch)

The 2026 *Pulse of Democracy* PDF was retrieved in full (21,426,820 bytes, 67 pages) using
HTTP range requests in 2 MB chunks with per-chunk retry; a single streamed download truncates
at roughly 6 MB on this CDN, which is what defeated the earlier attempts.
[SOURCE: https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf, fetched 2026-09-18]

**The requested Mexico percentages remain [GAP]**: Churchillian support for democracy, coup
tolerance, trust in the Supreme Court, trust in the police, trust in the legislature and system
support are all presented as country bar charts, which are images in this PDF and carry no
extractable text. Only the narrative numbers below are recoverable from the text layer.

| Item, Mexico, 2026 AmericasBarometer | Value | Regional context |
|---|---:|---|
| Crime victimization in the previous year | 33% | third highest; Ecuador 35%, Peru 34%, El Salvador lowest at 8% |
| Perceived criminal-group presence in the neighbourhood (new 2026 item) | 28% | second highest; Ecuador 29%, El Salvador 2% |
| Names law enforcement as what democracy means | 33% | regional average 30.3%; Dominican Republic highest at 46% |
| Names equality as what democracy means | 28% | regional average 25% |
| Trust in the Chinese government | 55% | |
| Trust in the United States government | 23% | one of the largest China-minus-US gaps in the region |

Regional, not Mexico-specific: asked what democracy means to them, Latin Americans name law
enforcement (30.3%), equality (25.0%) and freedom (24.4%) far more often than participation
(10.5%) or elections (9.7%).

Two qualitative statements about Mexico are in the text and are worth quoting because they bear
on the interpretation rather than supplying a number. The report groups Mexico with Peru as
countries that have "experienced… more substantial democratic backsliding", and it reports that
the positive association between its new Support for Illiberal Majoritarianism index and
Churchillian support for democracy is statistically significant in Mexico among others, meaning
that in Mexico professed support for democracy coexists with a conception of democracy centred
on majority rule rather than on checks and balances. Support for illiberal majoritarianism in
the region is not confined to backsliding countries; in most countries at least 50% of
respondents score 4 or higher on its 1-7 scale.
[SOURCE: same PDF, chapter 1 pp. 10 and 12, chapter 2 p. 31, the Support for Illiberal
Majoritarianism spotlight pp. 34-35, and the Trust in China and the U.S. spotlight p. 56,
fetched 2026-09-18]

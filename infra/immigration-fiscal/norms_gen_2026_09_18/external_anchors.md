claude-opus-5[1m]

**Verdict:** NO attitude percentages verified. Every requested value is [UNVERIFIED] / null. What is verified below is survey identity, fieldwork years, sample/field/mode for Pew only, and exact source locations. Full route detail and the emigrant-selection framing note are in `ANCHORS.md` in this directory.

Fetch date for everything below: 2026-09-18.

## 1. WVS wave 7 (2017-2022) — Mexico vs United States

| Item | Mexico | United States |
|---|---|---|
| Q235 strong leader, very+fairly good | null [UNVERIFIED] | null [UNVERIFIED] |
| Q238 democratic political system, very+fairly good | null [UNVERIFIED] | null [UNVERIFIED] |
| Q250 importance of democratic governance (mean / %8-10) | null [UNVERIFIED] | null [UNVERIFIED] |
| Q236 experts decide, very+fairly good | null [UNVERIFIED] | null [UNVERIFIED] |
| Q237 army rule, very+fairly good | null [UNVERIFIED] | null [UNVERIFIED] |
| Q69 confidence police, great deal+quite a lot | null [UNVERIFIED] | null [UNVERIFIED] |
| Q70 confidence courts, great deal+quite a lot | null [UNVERIFIED] | null [UNVERIFIED] |
| Q71 confidence government, great deal+quite a lot | null [UNVERIFIED] | null [UNVERIFIED] |
| Q73 confidence parliament, great deal+quite a lot | null [UNVERIFIED] | null [UNVERIFIED] |
| Sample size / field dates / mode | null [UNVERIFIED] | null [UNVERIFIED] |

Verified, with quote:
- Country-years are Mexico 2018 and USA 2017. Verbatim from the WVS7 country selector:
  "Mexico 2018" and "USA 2017".
  [SOURCE: https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7&COUNTRY= , fetched 2026-09-18]
- The official tabulation exists but is not retrievable by HTTP from here. Verbatim anchor text from
  the WVS7 file inventory: "WVS  Results By Country 2017-2022 v6.0.0.pdf", exposed only via a JS form
  post (`DocDownload('10763')` -> `AJDownload.jsp`). That POST returns HTTP 200 with a 1-byte
  text/html body, with and without a session cookie.
  [SOURCE: https://www.worldvaluessurvey.org/AJDocumentationSmpl.jsp?CndWAVE=7&COUNTRY= , fetched 2026-09-18]
- Microdata fallback located, not yet downloaded: "WVS_Cross-National_Wave_7_csv_v6_0.csv", 190,499,076
  bytes, created 2024-11-20, on a third-party Kaggle mirror.
  [SOURCE: `kaggle datasets files lauriszon/wvs-cross-national-wave-7`, fetched 2026-09-18]

## 2. LAPOP AmericasBarometer — Mexico

| Item | Value |
|---|---|
| Churchillian support for democracy, % agree | null [UNVERIFIED] |
| Coup justified when crime is high, % | null [UNVERIFIED] |
| Coup justified when corruption is high, % | null [UNVERIFIED] |
| Trust in Supreme Court | null [UNVERIFIED] |
| Trust in police | null [UNVERIFIED] |
| Trust in national legislature | null [UNVERIFIED] |
| System support | null [UNVERIFIED] |
| Sample size / field dates / mode | null [UNVERIFIED] |

Verified, with quote:
- Most recent round is 2026. Verbatim: "Drawing on the latest AmericasBarometer survey, the 2026 Pulse
  of Democracy examines how people across the Americas view democracy, governance, migration, ..."
  [SOURCE: https://www.vanderbilt.edu/cgd/publications/ , fetched 2026-09-18]
- Regional report PDF location: https://cdn.vanderbilt.edu/vu-wpfsx/wp-content/uploads/sites/157/2026/09/AAFF_LAPOP2026_2SET_HIGH.pdf
  (download reached 5.9 MB of ~7.2 MB before being reaped twice; truncated file fails xref parsing, so
  no number was read out of it) [SOURCE: as above, fetched 2026-09-18]
- Mexico instrument + technical documentation. Verbatim: "The 2026 AmericasBarometer technical resources
  for Mexico include the country questionnaire and technical report for this round.", linking
  `ABMex2026-Mexico-Questionnaire-V6.1.1.1-Spa-251013-W.pdf` and
  `ABMEX2025-Technical-Report-v2.0-FINAL-eng-260908.pdf`. The technical report is where Mexico's n,
  field dates and mode live; it was not read.
  [SOURCE: https://www.vanderbilt.edu/cgd/resource/2026-mexico/ , fetched 2026-09-18]

## 3. Pew Research Center — US Hispanics on democracy and institutions

| Item | Value |
|---|---|
| Hispanic views of US democracy | null [UNVERIFIED] |
| Hispanic confidence in US institutions | null [UNVERIFIED] |
| Nativity split on the above | null [UNVERIFIED] |
| Generational split on the above | null [UNVERIFIED] |

Verified, with quote — survey design of the most recent National Survey of Latinos:
- "This analysis is based on Pew Research Center's latest National Survey of Latinos, conducted from
  Oct. 6 to 16, 2025, among a sample of 8,046 U.S. adults. Some 4,923 Hispanics were surveyed, with
  1,125 respondents who are members of the Center's American Trends Panel (ATP) and 3,798 respondents
  who are members of SSRS's Opinion Panel. The survey also included 3,114 non-Hispanic ATP members."
  Mode: online probability-based panel, fielded "in English and Spanish"; weighted "by gender, race,
  ethnicity, partisan affiliation, education, presidential vote (among voters) and other factors."
  [SOURCE: https://www.pewresearch.org/race-and-ethnicity/2026/07/09/u-s-hispanics-are-divided-on-whether-their-identity-helps-or-hurts-them-in-america/ , fetched 2026-09-18]
- Pew does break this survey out by immigrant generation, but on identity rather than democracy.
  Verbatim chapter title: "Latino immigrants and U.S.-born Latinos differ on how much their identity
  shapes their lives." [SOURCE: same page, fetched 2026-09-18]
- Weak partial negative on a dedicated release: a pewresearch.org site search for "latinos democracy"
  returns "Displaying 1 - 10 of 37 results" with no Latinos-and-democracy or Latinos-and-institutions
  report among them. Not a clean verified negative — the satisfaction-with-democracy and
  trust-in-government series may still carry a Hispanic crosstab.
  [SOURCE: https://www.pewresearch.org/search/latinos+democracy , fetched 2026-09-18]
- Unread, and the right next target: the NSL 2025 topline,
  https://www.pewresearch.org/wp-content/uploads/sites/20/2026/07/RE_2026.07.09_National-Survey-of-Latinos_TOPLINE.pdf

## Framing note

Emigrants are not a random draw from the origin population; they are selected on age, education, risk
tolerance, networks and plausibly on political disposition. Mexican national averages therefore bound
nothing about Mexican-origin Americans directly. They are a prior about the shape of the origin-country
distribution, not a prediction for migrants or their descendants, and where direct measurement on
Mexican-origin Americans with nativity and generation identified exists, it supersedes the origin-country
average rather than supplementing it. Direction of selection on political attitudes: [GAP] — nothing was
located in this pass.

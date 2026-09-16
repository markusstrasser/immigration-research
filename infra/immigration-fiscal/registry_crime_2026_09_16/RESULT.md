claude-opus-5[1m]

**Verdict:** Denmark and the Netherlands succeeded with full official registry pulls (4,488 tidy rows, all validations PASS); Norway FAILED — no table combining charged persons with immigration category exists in the open SSB Statbank API, and both table ids in the brief were wrong.

Output CSV: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/a73215f4-2757-455d-9ffc-b358a9628307/scratchpad/registry-pull/registry_rates.csv`

[UNVERIFIED] — figures below are pulled live from the official APIs on 2026-09-16 and internally validated, but have not been cross-checked against the agencies' own published rate tables.

---

## 1. Denmark — SUCCESS

### Crime numerator
API: `POST https://api.statbank.dk/v1/data`
Table title verbatim (from `/v1/tableinfo`): **"Persons guilty in crimes"** (STRAFNA9), `updated=2026-04-08T08:00:00`, `latestPeriod=2025`.

```json
{"table":"STRAFNA9","format":"CSV","lang":"en","variables":[
 {"code":"KOEN","values":["M","K"]},
 {"code":"ALDER","values":["TOT","15-29","30-49","50-79"]},
 {"code":"HERKOMST","values":["TOT","1","21","24","25","31","34","35"]},
 {"code":"Tid","values":["2023","2024","2025"]}]}
```

### Population denominator
Table title verbatim: **"Population at the first day of the quarter"** (FOLK1E), `updated=2026-08-10T08:00:00`. FOLK1E was selected because it is the only DST population table whose `HERKOMST` variable carries the same western/non-western codes as STRAFNA9 (FOLK1C and FOLK2 stop at the 3-way Danish/Immigrant/Descendant split). Q1 (1 January) population is used for each calendar year.

```json
{"table":"FOLK1E","format":"CSV","lang":"en","variables":[
 {"code":"OMRÅDE","values":["000"]},
 {"code":"KØN","values":["1","2"]},
 {"code":"ALDER","values":["15","16",...,"79"]},
 {"code":"HERKOMST","values":["TOT","1","24","25","34","35"]},
 {"code":"Tid","values":["2023K1","2024K1","2025K1"]}]}
```

Years pulled: **2023, 2024, 2025**.

### Group definitions, verbatim from the API metadata
STRAFNA9 `HERKOMST (ancestry)`: `Total`, `Persons of Danish origin`, `Immigrants, total`, `Immigrants from western countries`, `Immigrants from non-western countries`, `Descendants, total`, `Descendants from western countries`, `Descendants from non-western countries`.
FOLK1E `HERKOMST (ancestry)`: `Total`, `Persons of Danish origin`, `Immigrants from western countries`, `Immigrants from non-western countries`, `Descendants from western countries`, `Descendants from non-western countries`. The two "total" rows for immigrants and descendants were built by summing western + non-western.
STRAFNA9 `ALDER (age)`: `Age, total`, `15-29 years`, `30-49 years`, `50-79 years`. `KOEN (sex)`: `Men`, `Women`.

### Headline, 2025, ages 15-79, conviction rate per 100,000

| Group | Men rate | Men index | Both sexes rate | Both index |
|---|---|---|---|---|
| Total (all persons) | 5,092.3 | 100.0 | 3,364.3 | 100.0 |
| Persons of Danish origin | 4,522.2 | 90.4 | 3,017.8 | 91.4 |
| Immigrants, total | 6,418.5 | 120.6 | 4,114.0 | 116.4 |
| Immigrants from western countries | 4,766.8 | 87.5 | 3,294.7 | 92.2 |
| Immigrants from non-western countries | 7,671.3 | 145.4 | 4,687.7 | 133.9 |
| Descendants, total | 15,486.3 | 246.6 | 10,102.9 | 246.0 |
| Descendants from western countries | 6,411.6 | 112.6 | 4,488.8 | 120.6 |
| Descendants from non-western countries | 16,722.1 | 320.8 | 10,865.7 | 314.9 |

Counts and denominators for the same rows (2025, men): Danish origin 88,304 / 1,952,683; non-western immigrants 14,999 / 195,521; non-western descendants 9,308 / 55,663; all persons 120,166 / 2,359,742.

### Standardization caveat — READ BEFORE QUOTING
The index column is **direct age standardization with all persons (HERKOMST=Total) of the same sex and year as the standard population**, all persons = 100. It is **NOT** DST's published index, which uses **indirect** standardization; do not present the two as equal or compare them numerically.
Second deviation from the brief: standardization uses the **three coarse bands 15-29 / 30-49 / 50-79**, not 5-year bands. STRAFNA9 publishes no finer age detail, so 5-year standardization is impossible from this table. The coarse bands leave substantial within-band age composition unadjusted, which biases the descendant indices upward (descendants are heavily concentrated at the young end of 15-29).

---

## 2. Netherlands — SUCCESS

API: `GET https://opendata.cbs.nl/ODataApi/odata/85658NED/TypedDataSet`
Table title verbatim: **"Verdachten; geslacht, leeftijd, herkomst, opleiding, huishoudensinkomen"** (85658NED), `Period=2010-2025`, `Modified=2026-03-27T06:30:00`.

```
?$format=json
&$select=Geslacht,Leeftijd,Geboorteland,Herkomst,Opleiding,Huishoudensinkomen,Perioden,
         TotaalVerdachtenVanMisdrijven_1,TotaalVerdachtenVanMisdrijven_8
&$filter=(Perioden eq '2023JJ00' or Perioden eq '2024JJ00' or Perioden eq '2025JJ00')
         and Opleiding eq 'T001143' and Huishoudensinkomen eq 'T001164'
```

Years pulled: **2023, 2024, 2025**. Both measures kept: `TotaalVerdachtenVanMisdrijven_1` = absolute registered suspects, `TotaalVerdachtenVanMisdrijven_8` = suspects per 10,000 residents.

**Table 85656NED was NOT used.** Its dimensions are `TypeMisdrijf, Geslacht, WelGeenWoonadresInNederland, Nationaliteit` — nationality and offence type, with no herkomst, generation or age. It cannot answer the herkomst × generation × age × sex question the brief asked for.

### Group definitions, verbatim from the API dimension tables
`Geboorteland` (generation): `Totaal`, `Geboren in NL, ouders in NL`, `Geboren in NL, één ouder geboren in NL`, `Geboren in NL, twee ouders buiten NL`, `Geboren buiten Nederland`.
`Herkomst` (origin): `Totaal`, `Nederland`, `Europa (exclusief Nederland)`, `Turkije`, `Marokko`, `Suriname`, `Nederlandse Cariben`, `Indonesië`, `Buiten Europa (excl. 5 grote herkomst...)`, `Onbekend herkomstland`.
`Leeftijd`: `Totaal`, `12 tot 18 jaar`, `18 tot 23 jaar`, `23 tot 45 jaar`, `45 tot 65 jaar`, `65 jaar of ouder`, `Overig of onbekend`.
`Geslacht`: `Totaal mannen en vrouwen`, `Mannen`, `Vrouwen`, `Onbekend`.

### Provisional flag — verbatim from the table's ShortDescription
> "De cijfers over 2024 en 2025 zijn voorlopig."
> "Voorlopige cijfers geven een onderschatting van het definitieve aantal verdachten."
> "Het voorlopige aantal verdachten in het meest recente jaar is enkele procenten lager dan het definitieve aantal."

So 2024 and 2025 are provisional and **understate** the final suspect count by a few percent; 2023 is final. The CSV's `provisional` column encodes this.

### Headline, 2025, all ages, registered suspects per 10,000 residents

By generation (herkomst = Total):

| Generation | Men | Both sexes |
|---|---|---|
| Total | 124 | 73 |
| Born in NL, both parents born in NL | 83 | 50 |
| Born in NL, one parent born in NL | 178 | 108 |
| Born in NL, both parents born abroad (2nd gen) | 453 | 265 |
| Born outside the Netherlands (1st gen) | 184 | 104 |

By origin (geboorteland = Total):

| Origin | Men | Both sexes |
|---|---|---|
| Netherlands | 83 | 50 |
| Europe (excl. NL) | 144 | 84 |
| Turkiye | 241 | 140 |
| Morocco | 473 | 265 |
| Suriname | 343 | 192 |
| Dutch Caribbean | 519 | 306 |
| Indonesia | 58 | 35 |
| Outside Europe (excl. 5 largest origin countries) | 220 | 128 |

Precision caveats: CBS rounds counts to multiples of 10 (e.g. 139,960) and publishes the per-10,000 rates as **integers**, so a published rate of 73 carries roughly ±0.7% rounding. The `population` column for the Netherlands is **derived** as count/rate×10,000, not an independently pulled denominator — see validation note below. `Onbekend herkomstland` has a count but no published rate, so its derived population is null.

---

## 3. Norway — FAILED

Both table ids in the brief are wrong, confirmed by fetching each one's metadata:
- `09405` returns HTTP 200 with title **"09405: Offences investigated, by type of offence, police decision, contents and year"** — dimensions are offence type and police decision, with no person-level or immigration dimension at all.
- `12979` returns HTTP 200 with title **"12979: Projected total fertility rate and age-specific fertility rates for women (per 1000), by region, age, alternative, contents and year"** — a fertility projection table, unrelated to crime.

Two rounds of table-list search were run against `https://data.ssb.no/api/v0/{en,no}/table/?query=...` with queries `charged`, `siktede`, `innvandringskategori`, `immigrant category charged`, `offenders immigrant`, `innvandrer`, `siktet`, `landbakgrunn kriminalitet`, `immigrants offences`, `immigration category`. The `charged` query returned 66 tables, of which 18 are person-level charged-persons tables (09412-09426, 11453, 08912) broken down by sex, age, citizenship, police decision, recidivism and place of residence. **Zero tables cross charged persons with immigration category or country background.** The nearest match is `09421: Persons charged, by group of principal offence and citizenship` — citizenship, not immigrant/Norwegian-born-to-immigrant-parents category, and without the age × sex detail requested.

No error string to report: the API answered every request with HTTP 200. The failure is that the statistic is **not published in the open Statbank API**, not that an endpoint blocked. SSB's immigrant-crime figures come from periodic analytical reports rather than a standing Statbank table. Getting Norway would require either the `09421` citizenship proxy or a non-Statbank SSB source; neither is in the brief's scope, so no Norwegian rows were written.

---

## 4. Validation — all PASS

```
rows: Denmark=288 Netherlands=4200 Norway=0 TOTAL=4488
rate recompute: n=2064 max_dev=0.0000% share>0.5%=0
  Denmark max_dev=0.000000%   Netherlands max_dev=0.0000%
latest year: DK=2025 (STRAFNA9 latestPeriod=2025)  NL=2025 (85658NED Period=2010-2025)
DK crime 'Age, total' vs sum of 3 bands (2025, Total, Men): tot=120166 bands=120166
DK crime-to-population merge: 144 band rows matched, 0 unmatched
```

- **Row counts** PASS: 288 Danish rows (band-level plus 15-79 aggregates), 4,200 Dutch rows, 0 Norwegian.
- **Rate recomputation** PASS for Denmark honestly: rates were computed here from independently pulled STRAFNA9 counts and FOLK1E denominators, so 0.000000% deviation is a real arithmetic check.
- **Rate recomputation for the Netherlands is tautological, not evidence.** CBS publishes count and rate but no denominator, so population was back-derived as count/rate×10,000. Recomputing the rate from that derived population necessarily returns the published rate. This check confirms no arithmetic bug, and it does **not** confirm CBS's own denominators.
- **Latest period** PASS: 2025 is the latest year in both pulls and matches each table's stated latest period.
- **Danish age coverage** PASS: the published `Age, total` (120,166 guilty men, 2025) exactly equals the sum of the three age bands, confirming STRAFNA9's total is 15-79 with no 80+ or unknown-age residual, so the 15-79 aggregate rows equal the published totals.

## 5. Files
- `registry_rates.csv` — tidy output, 4,488 rows, schema as specified
- `dk_crime_raw.csv`, `dk_pop_raw.csv`, `nl_raw.csv` — raw API responses
- `dk_meta.json`, `dk_meta2.json`, `nl_tableinfo.json`, `no_search.json`, `no_search2.json` — metadata and search evidence
- `probe*.py`, `pull_dk.py`, `pull_nl.py`, `compute.py` — reproducible scripts

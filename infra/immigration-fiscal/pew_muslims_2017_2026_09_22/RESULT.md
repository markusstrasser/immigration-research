claude-opus-5[1m]

# Pew 2017 U.S. Muslims — report reproduction and cuts by nativity and origin

**Verdict:** All ten report-level rows quoted in the Muslim-origins memo §2 reproduce from
the microdata within half a percentage point, so the memo's §2 table is confirmed. Two
things the report-level table hides show up in the cuts. First, the survey's design effect
runs 1.7 to 8.8, so the civilians-justified item carries a ±2.7 point standard error and
the memo's "84% against 83% for the public" comparison is well inside noise. Second, the
nativity split is not the interesting one: foreign-born and U.S.-born Muslims do not
differ on the civilians item, on accepting homosexuality, or on party, while U.S.-born
Muslims split into two populations that differ from each other far more than either
differs from immigrants. The 12% who say killing civilians can be justified is
concentrated among foreign-born South Asians, and their own U.S.-born children are the
group most opposed to it. [CALCULATION: derived/report_reproduction.csv,
derived/cuts_by_nativity.csv, derived/cuts_by_origin.csv]

Method, gates and scope are in [README.md](README.md). Standard errors in every table
below are jackknife (JRR) from the 100 replicate weights Pew ships, in percentage points.

## 1. Reproduction of the memo's §2 rows

All values [CALCULATION: derived/report_reproduction.csv].

| id | Measure | Published | Microdata | JRR SE | SRS SE | Design effect | Base n |
|---|---|---:|---:|---:|---:|---:|---:|
| B1 | Foreign born | 58 | 57.57 | 2.29 | 1.57 | 2.13 | 987 |
| B3 | College graduates | 31 | 31.26 | 2.75 | 1.47 | 3.50 | 997 |
| B4a | College graduates, foreign born | 38 | 38.48 | 3.43 | 1.94 | 3.13 | 628 |
| B4b | College graduates, U.S. born | 21 | 20.65 | 3.18 | 2.15 | 2.19 | 355 |
| B5a | Household income $100,000 or more | 24 | 24.20 | 1.97 | 1.44 | 1.88 | 888 |
| B5b | Household income under $30,000 | 40 | 40.48 | 2.14 | 1.65 | 1.69 | 888 |
| B6 | Own their home | 37 | 36.67 | 3.29 | 1.52 | 4.66 | 1,000 |
| B8 | Killing civilians often or sometimes justified | 12 | 11.53 | 2.70 | 1.01 | 7.18 | 1,001 |
| B9 | Killing civilians rarely or never justified | 84 | 83.51 | 3.48 | 1.17 | 8.81 | 1,001 |
| B11 | Homosexuality should be accepted by society | 52 | 52.37 | 2.48 | 1.58 | 2.47 | 1,001 |

Ten hits, no misses. The largest gap is 0.49 points. G3 passes.

**The denominator convention matters and is now pinned.** B8, B9 and B11 reproduce only on
the full n = 1,001 base, with volunteered "don't know" left in the denominator. On the
base of people who answered, the same items read 12.13 for often-or-sometimes, 87.87 for
rarely-or-never and 61.47 for accepting homosexuality. Rejection of violence against
civilians is therefore 88%, not 84%, among U.S. Muslims who gave an answer, and
acceptance of homosexuality is 61%, not 52%, among those who picked one of the two
statements. Anyone comparing these figures to a general-population number has to confirm
the public figure uses the same base. [CALCULATION: derived/report_reproduction.csv, rows
B8-alt, B9-alt, B11-alt]

**The brief's stated limit "no replicate weights" is wrong.** The file carries
`rpl001`–`rpl100`, and the main weight's own variable label says "Replicate weights must
be used to calculate standard errors." Appendix B names the method as jackknife repeated
replication with 100 replicates. This lane uses them, so no design-effect approximation
was needed. [CALCULATION: derived/audit.json, key `variance`]

## 2. Cuts by nativity

Foreign born n = 631, U.S. born n = 356, birthplace not reported n = 14. All values
[CALCULATION: derived/cuts_by_nativity.csv].

| Measure | U.S. born | Foreign born | Difference | SE of difference |
|---|---:|---:|---:|---:|
| U.S. citizen, U.S. born counted as citizens | 100.0 | 69.2 | −30.8 | 2.7 |
| Past year: people acted suspicious of them | 48.2 | 20.6 | −27.6 | 6.1 |
| A lot of discrimination against Muslims | 90.6 | 66.8 | −23.8 | 3.8 |
| Satisfied with the country's direction | 18.1 | 41.2 | +23.2 | 6.0 |
| Owns their home | 23.4 | 46.2 | +22.8 | 5.2 |
| Black, non-Hispanic | 32.1 | 10.7 | −21.4 | 6.8 |
| Has become more difficult to be a Muslim | 62.6 | 42.4 | −20.2 | 8.0 |
| Four-year college degree or more | 20.6 | 38.5 | +17.8 | 3.8 |
| Aged 18–29 | 44.6 | 27.8 | −16.8 | 5.3 |
| A lot in common with most Americans | 68.6 | 53.9 | −14.7 | 4.8 |
| No children ever born | 47.1 | 32.5 | −14.6 | 3.6 |
| Postgraduate or professional schooling | 6.6 | 16.1 | +9.5 | 2.8 |
| Proud to be an American | 90.3 | 96.3 | +6.0 | 2.7 |

The differences that are *not* there are as informative. Killing civilians often or
sometimes justified: +2.6 ± 4.4. Homosexuality should be accepted: −7.4 ± 7.5. Democrat
or leans Democratic: +2.3 ± 8.5. Republican or leans Republican: −2.0 ± 4.9. Employed full
time: +4.2 ± 4.9. Household income under $30,000: −8.6 ± 5.5. On the attitude items that
the memo treats as the assimilation question, immigrant and U.S.-born Muslims are
statistically indistinguishable in this survey. [CALCULATION: derived/cuts_by_nativity.csv]

Immigrants report far less personal hostility and far more satisfaction with the country
than U.S.-born Muslims, and are markedly more likely to say they are proud to be American.
That direction is stable across every foreign birth region. [CALCULATION:
derived/cuts_by_origin.csv]

## 3. Cuts by origin

Foreign born by own birth region; U.S. born by parents' birth region. Cells with an
unweighted base under 50 are flagged `n<50` in the CSV and are omitted from this table:
that removes foreign-born Americas (n = 23), Europe (n = 30) and Other/Undetermined
(n = 1), and the U.S.-born parent cells for the Americas (n = 10), Sub-Saharan Africa
(n = 13), Other Asia (n = 9), Europe (n = 7) and Other (n = 1). All values [CALCULATION:
derived/cuts_by_origin.csv].

| Measure | FB South Asia (245) | FB MENA (185) | FB Sub-Sah. Africa (80) | FB Other Asia (67) | USB, both parents U.S. born (166) | USB, ≥1 foreign parent (181) |
|---|---:|---:|---:|---:|---:|---:|
| Aged 18–29 | 27.9 | 39.9 | 23.2 | 18.8 | 25.1 | 68.6 |
| Black, non-Hispanic | 0.0 | 5.1 | 80.4 | 3.7 | 51.8 | 7.4 |
| Four-year degree or more | 43.4 | 33.2 | 27.0 | 43.3 | 13.8 | 28.2 |
| Household income under $30,000 | 47.3 | 41.6 | 47.1 | 16.1 | 56.4 | 29.2 |
| Household income $100,000+ | 22.2 | 16.8 | 23.6 | 50.7 | 16.7 | 20.2 |
| U.S. citizen | 70.9 | 65.7 | 71.1 | 63.1 | — | — |
| Owns their home | 49.4 | 29.1 | 38.6 | 52.9 | 18.1 | 29.2 |
| Employed full time | 45.1 | 34.9 | 54.2 | 49.5 | 43.3 | 36.5 |
| Mean children ever born (floor) | 1.7 | 1.6 | 2.2 | 1.6 | 1.8 | 0.4 |
| Democrat or leans Democratic | 64.4 | 63.2 | 77.7 | 91.5 | 58.9 | 80.0 |
| Republican or leans Republican | 17.2 | 3.9 | 14.8 | 7.8 | 16.8 | 12.3 |
| Satisfied with the country's direction | 46.7 | 45.6 | 17.8 | 47.6 | 23.2 | 9.6 |
| A lot of discrimination against Muslims | 68.2 | 59.7 | 83.8 | 67.1 | 92.4 | 89.8 |
| Homosexuality should be accepted | 47.6 | 45.7 | 34.5 | 60.2 | 48.4 | 66.2 |
| Killing civilians often or sometimes justified | 20.5 | 9.5 | 9.0 | 5.9 | 13.8 | 4.9 |
| … rarely or never justified | 67.3 | 86.5 | 90.6 | 87.6 | 86.0 | 91.3 |
| … no answer given | 12.2 | 4.1 | 0.4 | 6.5 | 0.2 | 3.8 |

Standard errors for every cell are in the CSV; they run 2 to 13 points for the foreign-born
cells and 2 to 18 for the U.S.-born parent cells.

### 3.1 The civilians item is a South Asian immigrant result, and it does not persist

Foreign-born South Asians are the only sizable group above the survey average on the
civilians item, at 20.5 ± 5.6, and they also have by far the highest non-response on it,
12.2 ± 5.6. Against foreign-born MENA respondents their rejection rate is 19.2 ± 9.4
points lower (z = −2.0), and their justification rate 11.0 ± 6.8 points higher (z = 1.6).
[CALCULATION: derived/cuts_by_origin.csv, contrast rows]

U.S.-born Muslims with a South Asian parent (n = 65) go the other way, hard: 96.6 ± 3.3
say rarely or never, and not one of the 65 says often or sometimes. Against foreign-born
South Asians that is +29.4 ± 7.3 on rejection (z = 4.0) and −20.5 ± 5.6 on justification
(z = −3.7). [CALCULATION: derived/cuts_by_origin.csv, contrast "U.S. born, parent from:
South Asia minus Foreign born: South Asia"]

[FRAMING-SENSITIVE] This is the opposite sign from the Denmark descendants result the memo
cites in §4, but it is a different measure (an attitude item, not a fiscal balance) and the
second generation here is much younger. Read it as evidence that the memo's §4 European
pattern does not transfer to this US attitude item, not as a fiscal claim.

### 3.2 "U.S.-born Muslims" is two populations, not one

The U.S.-born half of this survey splits into a group whose parents were also born here,
52% of it Black and non-Hispanic, and a group with at least one immigrant parent. On the
measures the memo cares about they differ more from each other than either differs from
immigrants. [CALCULATION: derived/cuts_by_origin.csv, contrast "U.S. born: at least one
foreign-born parent minus U.S. born: both parents U.S. born"]

| Measure | Difference | SE | z |
|---|---:|---:|---:|
| No children ever born | +58.3 | 6.5 | 9.0 |
| Black, non-Hispanic | −44.4 | 10.2 | −4.4 |
| Aged 18–29 | +43.5 | 6.0 | 7.2 |
| Household income under $30,000 | −27.1 | 11.1 | −2.4 |
| Three or more children ever born | −24.2 | 4.9 | −5.0 |
| High school graduate only | −23.7 | 9.5 | −2.5 |
| Past year: people acted suspicious of them | −21.2 | 8.9 | −2.4 |
| Democrat or leans Democratic | +21.1 | 8.5 | +2.5 |
| Four-year degree or more | +14.5 | 6.0 | +2.4 |

Most of the fertility, income and education gap here is age: the children-of-immigrants
group is 68.6% aged 18–29 against 25.1%, so it is largely people who have not finished
school, started earning or had children yet. The age structure is in the CSV so a reader
can see it rather than infer it. The memo's B4b row, "U.S.-born Muslims, 21% college
graduates," is a blend of a 13.8% group and a 28.2% group. [CALCULATION:
derived/cuts_by_origin.csv]

## 4. Gates

| Gate | Result |
|---|---|
| G1 zip sha256 `1117f843…5926af` and 6,121,578 bytes | PASS |
| G2 1,001 rows, 222 columns, weight finite and positive, 100 replicates | PASS |
| G3 every published B-row within 1 point | PASS, 10 of 10, largest gap 0.49 |
| G4 every variable used printed with its label in `audit.json` | PASS, 27 variables |

```
$ uv run --offline --no-project --with pyreadstat python3 -m pytest \
    infra/immigration-fiscal/pew_muslims_2017_2026_09_22/ -q
.........                                                                [100%]
9 passed in 1.26s

$ uv run --offline --no-project --with pyreadstat python3 \
    infra/immigration-fiscal/pew_muslims_2017_2026_09_22/analysis.py
G1 zip sha256+size: PASS
G2 rows=1001 weight_min=53.28 weight_max=28128.62 finite_positive=True replicates=100: PASS
  HIT  B1       Foreign born                    est= 57.57 se= 2.29 deff= 2.13 n= 987 published= 58.0 diff=-0.43
  ... (ten published rows, all HIT)
G3 misses over 1 point among published rows: 0
G4 variables printed with labels in audit.json: 27
```

## 5. Files

| Path | Contents |
|---|---|
| `analysis.py` | the whole lane; codes resolved from value labels at run time |
| `test_analysis.py` | 9 tests: the four gates plus five method guards |
| `derived/report_reproduction.csv` | 13 rows: 10 published plus 3 denominator sensitivities |
| `derived/cuts_by_nativity.csv` | 172 rows: 43 outcomes × 3 groups + 43 difference rows |
| `derived/cuts_by_origin.csv` | 900 rows: 43 outcomes × 17 groups, plus 169 rows for 4 pre-specified contrasts |
| `derived/audit.json` | hashes, weight and replicate diagnostics, 27 variables with labels |
| `README.md` | input, run commands, method, gates |
| `_cache/` | unzipped source, git-ignored |

## 6. Limits

Self-identified Muslim adults, telephone, 23 January to 2 May 2017, noninstitutionalized
only. Income is banded and pre-tax for 2016, so no dollar amount can be computed, only
band shares. Birthplace is a region, not a country: "South Asia" pools Pakistan,
Bangladesh, India and their neighbours, and "MENA" pools Iran, Egypt, Iraq and the Gulf,
so these cells cannot be joined to the country-level ACS rows in the memo's §1. Children
ever born is top-coded at four or more, so the mean is a floor. There is no
public-assistance, welfare, Medicaid or health-coverage item in any of the 222 variables,
searched by label; this survey cannot speak to benefit take-up. [CALCULATION:
derived/audit.json, key `items_searched_and_absent`]

Design effects of 1.7 to 8.8 mean the effective sample is far below 1,001, and
region-by-generation cells are small: three foreign-born regions and five U.S.-born parent
regions fall under 50 respondents and are flagged rather than dropped. Every single-cell
comparison in section 3 that is not given a z score should be read as descriptive.

The generational contrasts compare today's second generation with today's immigrants, not
with their own parents, and the second generation is far younger. Nothing here is a
cohort-followed-over-time result.

[FRAMING-SENSITIVE] The choice to report the civilians item by origin at all is a framing
decision. It is reported because the memo already quotes the topline and because the
topline conceals a real between-origin difference, with both the estimate and the
non-response rate shown so the reader can discount it.

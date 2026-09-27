claude-opus-5-5

**Verdict:** The FY2019→FY2024 doubling of Mexican IR-5 parents (34k → 63k) is a system-wide
processing surge on top of a growing birth cohort, not a Mexico-specific anomaly. IR-5 parents from
every other country rose by the same proportion (+79%, against Mexico's +84%). Mexico's share of
all IR-5 barely moved (24.4% → 25.0%), and holding it at the FY2019 share predicts 95% of the rise.
Over FY2020–24, cumulative Mexican IR-5 (198k) is 5% *below* what the FY2019 admission rate per
US-born child turning 21 would have produced (207k). The US-born children of Mexico-born mothers
turning 21 grew 34% over those five years (311k → 416k a year; NCHS natality, measured through 2004
births). At the FY2019 rate that growth alone accounts for 40% of the rise. It sets the long-run
level (R² 0.40) but not the year-to-year swings, which follow other countries' IR-5 (r 0.69, against
−0.18 for the cohort). Mexican families turn US-born children into IR-5 parents at about half the
rate of other foreign-born families (19–32% of IR-5 against 31–45% of the cohort). That is what the
statute predicts for parents who crossed without inspection, and a fraud-inflated channel would push
the other way. No measured fraud rate for parent petitions exists: USCIS never assessed them, DNA is
not required and no failure rate is published, and fraud counts pool all family categories. Fraud at
a constant low rate therefore cannot be excluded, but nothing in the data points to a fraud wave.
The one documented channel, Texas midwives who registered Mexico-born children as US-born, creates
false petitioners and is unsized. About 80% of Mexican IR-5 green cards are adjustments inside the
US (about half worldwide). The statute allows adjustment only for parents who entered lawfully
(visa, border crossing card) or hold 245(i) or military parole. Parents who crossed without
inspection must leave, face the 10-year bar, and cannot use their citizen child's hardship for a
waiver. Projection to FY2030 [MODEL: 2005+ births are not on the public file]: 38–71k a year; the
cohort turning 21 peaks in FY2028 and every variant flattens after it.

# IR-5 parents: fraud or birth cohorts? (2026-09-27)

Operator question: Mexican parents of US citizens (IR-5) rose from 34k (FY2019) to 63k (FY2024),
many adjusting inside the US. Is that fraud, or US-born children of Mexican mothers turning 21?
Full source quotes, page references and archived texts for the fraud and law sections are in
[reads/fraud_and_law.md](reads/fraud_and_law.md) (researcher read, claude-opus-5-5) and `sources/`.
The IR-5 series is read from `../late_arrival_tail_2026_09_27/derived/ir5_flow.csv`.

## 1. Measured fraud rates (brief task 1)

No source checked gives a measured fraud rate for parent (IR-5) petitions. Checked: GAO-06-259,
DHS OIG-13-97, State Report of the Visa Office ineligibility tables FY2019 and FY2021–24, 9 FAM
601.11, State PRM DNA fact sheets, and Castelano v. Clinton filings. USCIS Benefit Fraud and
Compliance Assessments were not found in published form. Rows with source, year, population,
method, page and quote: [derived/fraud_rates.csv](derived/fraud_rates.csv). `verify.py` checks
each quote against the archived text.

| Source | Population | Measure | Figure |
|---|---|---|---|
| GAO-06-259 (2006), FDNS assessment | religious-worker petitions, FY2004 sample of 220 | sampled, field-verified | 72 of 220 (33%) potential fraud [SOURCE: sources/gao_06_259_benefit_fraud_2006.txt] |
| GAO-06-259 | all USCIS applications, FY2005 | detected fraud denials | "just over 20,000"; spouses 14%; no parent split [SOURCE: same] |
| GAO-06-259 | petitions the National Visa Center returned to USCIS "that are denied or withdrawn", all categories | fraud or suspected fraud as determined by consular officers | about 900 of 2,400 a month [SOURCE: same, lines 720–722] |
| DHS OIG-13-97 (2013), p.3–4 | family I-130s, all relationships, FY2008–11 | denials/revocations for fraud | 2,557 (~640/yr), 622 with an FDNS finding; no denominator, no parent split [SOURCE: sources/dhs_oig_13-97_family_fraud_tracking_2013.txt] |
| State RVO Table XX/XIX | all immigrant-visa applicants, all countries | 212(a)(6)(C)(i) misrepresentation findings | 6,559 (FY19), 3,175 (FY21), 4,896 (FY22), 5,706 (FY23), 6,422 (FY24) [SOURCE: sources/state_rvo_tableXIX_ineligibilities_FY20*.txt] |
| State PRM P-3 DNA pilot (2008) | African refugee family units, ~3,000 persons; not IR-5 | relationships confirmed | <20% of family units fully confirmed; refusals counted as failures [SOURCE: sources/state_prm_p3_dna_fraud_factsheet_2008-12-04.txt] |

Readings:

- Detected family-based fraud runs about 640 cases a year across all I-130 relationships, well
  under 1% of I-130 decisions [INFERENCE: OIG gives no denominator; USCIS decides several hundred
  thousand I-130s a year]. A detection count cannot include undetected fraud.
- USCIS chose marriage, religious-worker and intracompany-transferee benefits as high-risk for
  assessment. Parent petitions were never assessed, so their fraud rate is unmeasured; nothing
  shows it is low.
- Consular misrepresentation findings (3–6k a year) pool every immigrant category and nationality.
  Against the 265,467 immediate-relative visas issued in FY2024 (RVO Table VIII grand total) they
  would be about 2% even if all were immediate relatives [CALCULATION: 6,422 / 265,467].
- DNA may be suggested but not required, and no IR-5 or I-130 DNA failure rate is published
  [SOURCE: sources/state_9fam_601.11_dna_excerpt.txt]. The refugee P-3 rate does not transfer:
  it covers a different population in camps without civil registries and a slot-brokering
  mechanism.
- One documented fraud channel matches the operator's suspicion: Texas border midwives registered
  US birth certificates for children born in Mexico. In Castelano v. Clinton the government
  admitted convictions and dual US/Mexican registrations. The documents read give no count, and the
  Suspect Birth Attendants list is withheld [SOURCE: sources/castelano_v_clinton_settlement_excerpts.txt].
  That channel creates false petitioners (false citizens), not false parent links.

## 2. Who can adjust inside the US (brief task 3)

Statute text from Cornell LII, archived in `sources/law_*.txt`.

- Parents are immediate relatives only once the citizen child is at least 21, and immediate
  relatives have no numerical cap [SOURCE: INA 201(b)(2)(A)(i), sources/law_8usc1151_ina201_cornell.txt].
  IR-5 flow is therefore set by the number of citizens turning 21 who have a foreign parent wanting
  a green card, plus processing capacity.
- Adjustment inside the US requires entry that was "inspected and admitted or paroled" (INA 245(a)).
  Immediate relatives are exempt from the 245(c) bars for unlawful status and unauthorized work.
  A parent who entered on a visa or border crossing card, then overstayed and worked, can therefore
  adjust once a 21-year-old citizen child petitions [SOURCE: sources/law_8usc1255_ina245_cornell.txt].
- A parent who entered without inspection can adjust only under 245(i) or through military parole
  in place. 245(i) requires being the beneficiary of a petition or labor certification filed by
  30 April 2001, plus a $1,000 fee [SOURCE: same]. Military parole covers the parent of a service
  member or veteran [SOURCE: sources/uscis_military_parole_in_place_excerpt.txt].
- Everyone else who entered without inspection must process abroad (Ciudad Juárez). After a year
  or more of unlawful presence past age 18, that person faces the 10-year bar of
  212(a)(9)(B)(i)(II). The waiver in 212(a)(9)(B)(v), and the stateside I-601A that uses it, counts
  only hardship to a citizen or LPR *spouse or parent* of the immigrant. The petitioning citizen
  child's hardship does not count [SOURCE: sources/law_8usc1182_ina212_cornell.txt; sources/law_8cfr212.7_cornell.txt].
- A parent who re-entered illegally after more than a year of unlawful presence is permanently
  barred under 212(a)(9)(C) until 10 years abroad; there is no family waiver [SOURCE: same].

**Consular issuance vs adjustment for Mexican IR-5.** State's Table VIII (by area of birth, IR-5
column) counts IR-5 visas issued abroad to Mexico-born parents; DHS counts Mexican IR-5 green cards
([reads/ir5_mexico_iv_issued.csv](reads/ir5_mexico_iv_issued.csv); `verify.py` re-reads the Mexico
row of each archived table).

| FY | Mexico-born IR-5 visas issued | Mexican IR-5 LPRs | Visa ÷ LPR | All-country visa ÷ LPR |
|---|---|---|---|---|
| 2019 | 6,855 | 34,186 | 0.20 | 0.45 |
| 2020 | 4,337 | 24,960 | 0.17 | 0.35 |
| 2021 | 7,090 | 25,798 | 0.27 | 0.56 |
| 2022 | 10,175 | 31,691 | 0.32 | 0.62 |
| 2023 | 11,617 | 52,380 | 0.22 | 0.51 |
| 2024 | 11,760 | 63,050 | 0.19 | 0.46 |

[SOURCE: sources/state_rvo_tableVIII_IR_by_birth_FY20{19..24}.txt; CALCULATION: ratios. FY2013–18
Mexico values in the reads file (9,938; 8,570; 10,382; 8,217) come from search snippets and are
[UNVERIFIED].]

About 80% of Mexican IR-5 green cards are adjustments inside the US, against about half worldwide.
Both channels grew from FY2019 to FY2024: consular +72%, in-US adjustments +88% (27.3k → 51.3k)
[CALCULATION: LPR minus visas; a visa issued late in one fiscal year becomes an LPR the next year].
The channel mix is about where it was in FY2019 for both Mexico and the world, so the surge did not
run through one channel only. Under the statute, an adjusting parent had a lawful entry, 245(i) or
parole. A fabricated parent-child link alone does not open adjustment for a parent who crossed
without inspection. USCIS and NVC backlog counts were not retrieved [GAP]. Section 3 sizes the
catch-up from the flows themselves.

## 3. Birth-cohort test (brief task 2)

**Births.** `natality_modal.py` streams each year's raw NCHS natality file (NBER mirror,
`inputs/raw/YYYY/`) on Modal and tabulates mother's birthplace, Hispanic origin, resident status,
record weight and live birth order. Field positions come from NBER's dictionaries; codes come from
the NCHS user guides (`sources/nchs_natality_codebook_excerpts.txt`). The job ran one container per
year and returned only counts. Run r2 added birth order to run r1, and `build_births.py` stops
unless r2 reproduces r1's totals exactly (it does). `build_births.py` →
[derived/births_mexico_mothers.csv](derived/births_mexico_mothers.csv).

| Birth years | Mother born in Mexico | All foreign-born mothers |
|---|---|---|
| 1980–1988 | `mplbir` (tape 138–139) = 57; record weight 2 for the 50%-sample states | `mplbir` 55 Canada, 56 Cuba, 57 Mexico, 59 rest of world |
| 1989–2002 | `mplbir` (88–89) = 57 | same codes |
| 2003–2004 | `umbstate` (96–97) = MX | `umbstate` CC, CU, MX, YY (`mbstate_rec` = 2 "includes possessions", so it is not used) |
| 2005–2010 | **[MODEL]**: the US public file has no mother's birth country ("available in the territory file only") and no nativity item. Births to mothers of Mexican Hispanic origin (`umhisp` = 1) × the Mexico-born share of those births. Central: the share held at its 2003–04 measured 0.642 (flat at 0.641–0.643 in 2001–04). High: the 1995–2004 linear trend (0.647 in 2005 → 0.665 in 2010) | not estimated |

Births exclude foreign residents, as NCHS totals do. Gate: US-resident totals equal NCHS published
totals in all 31 years (maximum difference 0.0000%) [SOURCE: sources/nchs_births_gfr_us_1909_2018.csv,
data.cdc.gov e6fc-ccez]. Births to Mexico-born mothers rose from 117k (1980) to 166k (1988), 242k
(1990), 366k (2000) and 435k (2004) [DATA: derived/births_mexico_mothers.csv]. The [MODEL] years
peak at 464k in 2007 (high 473k) and fall to 414k in 2009 (high 427k). A further 2.4–5.7k a year
were born in the US to Mexico-born mothers living abroad. Those children are citizens too; they
sit in a separate column and are not added to the main series.

A parent becomes eligible when the family's *first* US-born child turns 21, so younger siblings
add no parents. First live births are 34% of births to Mexico-born mothers (2000). Live birth order
also counts children born in Mexico, so order 1 is a lower bound on a first US-born child; total
births are the upper bound. The two indices move together (FY2019→24: +32% for first births,
+34% for all births), so no result below depends on which one is used.

**Cohort vs IR-5.** The cohort turning 21 in fiscal year t is 0.75·B(t−21) + 0.25·B(t−22).
`cohort.py` writes five tables:
[derived/cohort_vs_ir5.csv](derived/cohort_vs_ir5.csv), [derived/cohort_fit.csv](derived/cohort_fit.csv),
[derived/decomposition.csv](derived/decomposition.csv), [derived/backlog_catchup.csv](derived/backlog_catchup.csv)
and [derived/cohort_projection.csv](derived/cohort_projection.csv). The processing index is IR-5
from all countries except Mexico. It shares USCIS and State capacity shocks with Mexico but not the
Mexican cohort. Every FY2005–24 comparison uses measured births (1983–2003).

![Mexican IR-5 vs births shifted 21 years; FY2026+ cohort and the projection band are [MODEL]](derived/cohort_vs_ir5.png)

| Lag (years) | r, levels | r, Δlog vs cohort | r, Δlog vs non-Mexican IR-5 | R², cohort only | R², processing only | R², both | Cohort elasticity (both) | r, levels, first births |
|---|---|---|---|---|---|---|---|---|
| 21 | 0.66 | −0.18 | 0.69 | 0.40 | 0.66 | 0.79 | 0.31 | 0.62 |
| 22 | 0.68 | 0.00 | 0.69 | 0.43 | 0.66 | 0.80 | 0.31 | 0.66 |
| 23 | 0.69 | 0.03 | 0.69 | 0.44 | 0.66 | 0.81 | 0.32 | 0.67 |
| 24 | 0.66 | −0.13 | 0.69 | 0.43 | 0.66 | 0.81 | 0.32 | 0.65 |

[CALCULATION: cohort.py, log-log OLS on FY2005–24, n = 20 trending years; the R² values mostly
reflect shared trends and are weak evidence on their own]

- **Levels track and changes do not.** IR-5 and the cohort share a long-run trend, but year-to-year
  changes in Mexican IR-5 are uncorrelated with cohort changes (r −0.18 to 0.03). They correlate
  with changes in every other country's IR-5 (r 0.69). The link is loose even in levels: from FY2010
  to FY2015 the cohort grew 51% (191k → 288k) while Mexican IR-5 grew 30% (22.3k → 29.0k).
- **Mexico's share of IR-5 sits far below its share of the cohort.** Over FY2005–24 Mexico supplied
  19–32% of IR-5 parents, but 31–45% of US births to foreign-born mothers 21 years earlier
  (r 0.45 between the two shares; figure panel B). Mexican families convert a US-born child into
  an IR-5 parent at about half the rate of other foreign-born families. That fits the statute
  (section 2): parents who crossed without inspection mostly cannot adjust and face the 10-year bar
  abroad [INFERENCE]. A fraud-inflated channel would push the other way. One caveat applies: some
  non-Mexican IR-5 petitioners are naturalized immigrants rather than US-born children, which
  inflates the non-Mexican rate.
- **FY2019→FY2024 decomposition** of the +28.9k rise [DATA: derived/decomposition.csv]:

  | Counterfactual FY2024 | Predicted | Share of the rise |
  |---|---|---|
  | FY2019 IR-5 per child turning 21, applied to the FY2024 cohort | 45.7k | 40% |
  | Mexico keeps its FY2019 share (24.4%) of all IR-5 | 61.6k | 95% |
  | Cohort growth × non-Mexican growth, unit elasticities | 81.8k | 165% |

  The share counterfactual comes closest. Non-Mexican IR-5 has cohort growth of its own, so reading
  its whole rise as processing overstates processing somewhat. That does not change the finding:
  Mexico did not outgrow the other countries.
- **Backlog catch-up** [DATA: derived/backlog_catchup.csv]. Against FY2019 levels, Mexican IR-5
  fell short by 20.1k over FY2020–22 and overshot by 47.1k over FY2023–24; for all countries the
  figures are 119.3k and 180.7k. Cumulative Mexican IR-5 over FY2020–24 was 197.9k. The cohort path
  at the FY2019 yield (109.8 per 1,000 turning 21) gives 207.4k. The surge brought Mexico back to
  95% of the cohort-implied five-year total, not above it. IR-5 per 1,000 turning 21 ran 113
  (FY2015–19 mean), then 72–82 (FY2020–22), then 151 (FY2024).
- **The COVID years point the same way.** Mexico's share rose to 28.4% and 32.0% in FY2020–21. The
  Mexican flow is about 80% adjustments inside the US, so consular closures hit it less than the
  roughly half-consular flow from other countries [INFERENCE from section 2's channel table].

**Path to FY2030.** Births after 2004 are [MODEL], so every cohort from FY2026 on is [MODEL]. The
cohort turning 21 rises from 416k (FY2024) to 431k (FY2025, measured) and 463k in FY2028 (high
471k), then falls to 421k in FY2030 (high 433k).

| FY | Cohort turning 21 | Low: model, processing back at FY2015–19 | Mid: FY2015–19 yield held | High: FY2024 yield held | High, high-births variant |
|---|---|---|---|---|---|
| 2025 | 431k | 38.6k | 48.6k | 65.4k | 65.4k |
| 2026 [MODEL] | 443k | 38.9k | 49.9k | 67.1k | 67.5k |
| 2028 [MODEL] | 463k | 39.5k | 52.2k | 70.2k | 71.4k |
| 2030 [MODEL] | 421k | 38.3k | 47.4k | 63.7k | 65.6k |

Low = log IR5 = −2.00 + 0.308 log cohort + 0.736 log non-Mexican IR-5 (residual sd 0.15 log), with
non-Mexican IR-5 at its FY2015–19 mean. The yield variants assume an elasticity of 1 to the cohort;
the fitted elasticity is 0.31. The FY2024 yield includes the catch-up, so it is an upper bound
unless processing stays at the FY2024 pace. Range: 38–71k a year. Processing capacity decides where
the flow lands in that range, and every variant flattens or falls after FY2028; none keeps doubling
[CALCULATION: derived/cohort_projection.csv].

## 4. Disconfirmation, both ways (brief task 4)

| Test | What fraud predicts | What the cohort/processing reading predicts | Found |
|---|---|---|---|
| Mexico's share of all IR-5 in the surge | jumps if a Mexico-specific fraud channel opened | flat, because processing is shared | 24.4% (FY2019), 25.1%, 25.0% (FY2023–24); below FY2020–21. **Cohort/processing survives** |
| Mexico's IR-5 share vs its share of the cohort | above the cohort share, or rising faster than it | at or below it, lower for Mexico because EWI parents are barred | 19–32% of IR-5 against 31–45% of the cohort; r 0.45. **Cohort/processing survives** |
| FY2020–24 total vs cohort path | above | at or below | 198k vs 207k. **Cohort/processing survives** |
| Channel of the surge | concentrated in the channel with weaker checks | both channels grow | consular +72%, adjustment +88%; mix stable. **Mostly cohort/processing**; the adjustment channel grew somewhat faster |
| Parent ages | parents too young to have a 21-year-old | parents mostly 45–55 | No IR-5 age table by country exists. The sister lane bounds FY2024 Mexican IR-5 at ≤48% aged 55+, and 50,610 Mexican LPRs were aged 45–54 (`late_arrival_tail_2026_09_27/RESULT.md` §1). That fits mothers who gave birth at about 25 to children now 21–23. **Not testable directly** |
| DNA failures, OIG/GAO findings on IR-5 | published failures or findings | none | None exist in either direction. **Unmeasured** |
| Fabricated petitioners (midwife certificates) | a real, uncounted channel | irrelevant to the trend | Admitted in court, unsized. **Survives as a possible constant-level contributor** |

The birth-cohort reading does not rule out fraud at a steady low share: a constant fraud rate would
scale with the cohort and processing and be invisible to every test above. What the data rule out
is a fraud wave behind the FY2022–24 surge.

## Sources covered and skipped

Covered: NCHS natality public-use files 1980–2010 (NBER raw mirror), NCHS user guides 1980, 1989,
2003, 2004, 2005 and 2009, NCHS births 1909–2018 (data.cdc.gov), DHS OHSS IR-5 by country (via the
sister lane), State RVO Table VIII FY2019–24, Table XIX/XX FY2019 and FY2021–24, GAO-06-259, DHS
OIG-13-97, 9 FAM 601.11, State PRM P-3 fact sheets, Castelano v. Clinton filings, 8 U.S.C.
1151/1182/1255 and 8 CFR 212.7, and the USCIS military parole-in-place page.

Skipped or not found:
- USCIS BFCA reports: not published.
- USCIS I-485/I-130 pending counts and NVC documentarily-qualified backlog series: not retrieved,
  so the backlog is sized from the flows.
- RVO FY2020 Table XX: URL not found.
- RVO Table I (all-IV denominator): not archived.
- DOJ press releases on the 1990s Rio Grande Valley midwife cases: not located.
- USCIS Policy Manual Vol. 7 text on 245(i): not re-read.
- INA 212(i) full text: snippet only.
- Births 2005–2010 by mother's birthplace: not on the public file, so they are [MODEL]. The
  restricted NCHS file, CDC WONDER expanded natality (nativity only, 2007+), or ACS children by
  mother's birthplace would replace the model; firecrawl credits were exhausted and CDC blocked
  scripted PDF fetches. They affect only the FY2026+ projection.
- Petitioner's route to citizenship (US-born vs naturalized): not in the DHS tables. The cohort
  model covers US-born petitioners only, and the Mexican yield per US-born child includes any
  naturalized petitioners [GAP].
- Father's birthplace: not tabulated. Each family can produce two IR-5 parents; the mother's
  birthplace is the proxy for the family.

## Files

`natality_modal.py` (Modal tabulation, docs fetch), `build_births.py`, `cohort.py`,
`build_fraud_rates.py`, `verify.py` (34 gates: natality totals, IR-5 read-back, no break in the
Mexico-born, foreign-born and first-birth series at the 1985/1989/2003 file switches, [MODEL] labels
exactly on 2005+ births and FY2026+ projections, quotes archived, RVO Mexico rows, figure).
`verify.py` last run: `PASS: 0 failing gates`, rc 0. Run from the repository root:

```sh
modal run --detach infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/natality_modal.py::launch --run-id r2
uv run --no-project --with modal python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/natality_modal.py collect r2
uv run --no-project --with modal python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/natality_modal.py collect r1  # build checks r2 == r1
uv run --no-project python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/build_births.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with matplotlib python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/cohort.py
uv run --no-project python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/build_fraud_rates.py
uv run --no-project python3 infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/verify.py
```

`_cache/` (counts JSON, dictionaries, user-guide text) is ignored.

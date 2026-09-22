claude-opus-5[1m]

## Audit correction — September 19, 2026

**A failed design leaves an unidentified causal effect, not a null.** The baseline-level correlation is a balance/mean-reversion diagnostic, not a direct test of exclusion for an outcome change. In the 2008–2018 Mexico-born SSI arm, independently scaling the single instrument by 1, −1 and 0.001 leaves F=44.0025 and the IV coefficient +0.213008 unchanged. Negative national inflow cannot invalidate an estimate through sign alone. Placebo and dynamic-confounding concerns still prevent a causal conclusion; the probe does not validate displacement. [SOURCE: principal code and independent probe in the mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


**Verdict:** NO EVIDENCE of native displacement onto transfers, on the margins this lane could
measure, and the one margin most likely to carry it was unreachable. Applying the
Autor–Dorn–Hanson design to immigration on 2000–2010, where the shift-share instrument is alive
(first-stage F 16–29), household SSI receipt moves **−0.29 to −0.44 points per point of
foreign-born inflow** (2000–2007: −0.405, 95% [−0.661, −0.149]; with a mean-reversion control
−0.293, [−0.488, −0.099]) and public-assistance receipt **−0.35 to −1.51**. Every interval
excludes a positive transfer response of the ADH sign, and the negative sign **survives
restricting the outcome to natives only** (2005–2008, F 13.0: IV −0.490, [−0.977, −0.003]), so it
is not a composition artifact. But it is not evidence that immigration *reduces* transfer receipt
either: the instrument fails a direct exogeneity test in 61 of 100 arms, 42 of 59 placebos are
significant, the implied public-assistance effect exceeds the entire national decline over the
period, and the college control moves significantly in 7 of 36 arms. Native employment and
participation are null throughout (native no-college E/POP +0.370, [−0.687, +1.428]), which is
what Dustmann–Schönberg–Stuhler predict: their employment margin runs through reduced *entry*
into work, not exit into nonemployment, and non-entrants do not claim disability benefits.
**The decisive gap: SSDI, the one ADH category with a large significant response (+$8.40 per
$1,000/worker, SE 2.21), is not measured at all here** because SSA's county beneficiary files
returned HTTP 403. The hypothesis is untested on its most likely margin, not refuted.
The **2021–2024 surge cannot be studied with this instrument at all** — first-stage F 0.002, and
the reason is substantive: the inflow went to Atlanta and Seattle, not to Los Angeles and San
Francisco, so it did not follow the pre-1990 settlement pattern (Z-to-outcome correlation +0.020
across 350 metros). **Design B is uninformative but lands on the number in question**: earlier
Mexico-born wages move −7.18% per point of inflow, 95% [−23.83, +9.46], an interval that contains
zero, the brief's −6.7% and the verified Ottaviano–Peri −19.8% alike; the predicted ordering
(earlier immigrants lose most) does **not** appear, with 2000-and-later arrivals showing the
larger point loss. The **elasticity-transfer bound** puts the annual fiscal cost of wage incidence
on Mexican-origin workers at **$1–3 bn** scoring the actual 2021–24 inflow with Borjas, rising to
**$4–26 bn** scoring a 1990s-scale inflow with Ottaviano–Peri, where the factor-of-three width is
entirely the unresolved −6.7%-versus−19.8% question. Two corrections to the brief: the −6.7% is
**[UNVERIFIED]** and the text I could read says −19.8%; and Ottaviano–Peri's earlier-immigrant
elasticity **cannot** be applied to the second generation, who are US-born and take their native
elasticity of +1.8%.
[SOURCE: `derived/estimates.csv` (2,004 rows), `derived/estimates_pums.csv` (158 rows),
`derived/elasticity_bound.csv`, `derived/wage_bills.csv`; `estimate.py` re-runs byte-identical]

Purpose: measure two unmeasured fiscal second-order effects of low-skill immigrant inflow — (A) native labor-force withdrawal onto transfers in receiving metros (ADH China-shock design applied to immigration), and (B) wage/employment effects on earlier Mexico-born and Mexican second-generation workers.

---

## Status log

- 2026-09-18 — [UNVERIFIED] lane opened. Data routes probed and fixed (section 2). Two
  background pulls in flight: ACS 1-year metro aggregate panel 2005–2024, and ACS PUMS
  PUMA-level native/Mexico-born cells for 2005, 2008, 2021, 2024.
- 2026-09-18 — benchmarks pinned verbatim from primary text **before** any estimate exists,
  so they cannot be read back as chosen to fit (section 1).
- 2026-09-18 — [VERIFIED] all pulls complete. Aggregate metro panel 2000–2024 (14 endpoints),
  Census 2000 SF3 county endpoint with the pre-1990 base, and ACS PUMS PUMA cells for 2005,
  2008, 2021 and 2024 (203 of 204 state-years). `estimate.py` and `estimate_pums.py` re-run
  byte-identical after the final panel rebuild.
- 2026-09-18 — [VERIFIED] two measurement defects found and handled, not hidden: ACS 2005 codes
  weeks worked as continuous 1–52 while 2008 brackets it (every 2005 full-time cell discarded),
  and the ACS SNAP question begins in 2008 (2005 SNAP cells discarded). Section 7.
- 2026-09-18 — verdict written from the files, replacing the PROBE IN PROGRESS placeholder.

---

## 1. Benchmarks, stated before estimation

### Autor, Dorn & Hanson (2013), "The China Syndrome", AER 103(6)

The design this lane transplants. Their transfer result is Table 8, panel B, the dollar
change in annual transfer receipts per capita per $1,000 per-worker increase in a commuting
zone's import exposure over a decade, 1990–2007, N = 1,444 (722 CZs × two periods), 2SLS,
robust SEs clustered on state, weighted by start-of-period CZ population share:

| Transfer category | $ per capita per $1,000/worker exposure | SE | log-point version |
|---|---:|---:|---:|
| Total individual transfers | **57.73** *** | 18.41 | 1.01 *** (0.33) |
| Trade Adjustment Assistance | 0.23 | 0.17 | 14.41 * (7.59) |
| Unemployment benefits | 3.42 | 2.26 | 3.46 * (1.87) |
| SSA retirement | 10.00 * | 5.45 | 0.72 * (0.38) |
| **SSA disability (SSDI)** | **8.40** *** | 2.21 | 1.96 *** (0.69) |
| Medical (mainly Medicare/Medicaid) | 18.27 | 11.84 | 0.54 (0.49) |
| **Federal income assistance (SSI + TANF + SNAP)** | **7.20** *** | 2.35 | 3.04 *** (0.96) |
| Education/training assistance | 3.71 *** | 1.44 | 2.78 ** (1.32) |

Verbatim: "We estimate that a $1,000 increase in Chinese import exposure leads to a rise in
transfer payments of $58 per capita (1.01 log points in the logarithmic specification)." And:
"the increase in federal transfer spending on SSDI payments is large and significant, equal to
about $8 per $1,000 growth of export exposure." Their own footnote 42 records that denominating
transfers by workers rather than by residents roughly doubles the coefficient, to 113.18
(SE 41.53), because US employment is about 50% of total population.
[SOURCE: Autor, Dorn & Hanson 2013, AER 103(6):2121–68, 10.1257/aer.103.6.2121, pp. 2149–50 of
the published PDF, text extracted 2026-09-18; local copy
`infra/immigration-fiscal/displacement_transfers_2026_09_18/_cache/adh2013.pdf`]

Two features of that table matter for what this lane can conclude. First, **the elastic
categories are SSDI and federal income assistance, not unemployment insurance** — the response
is a shift onto long-duration, non-work-conditional programmes, which is precisely the margin
the brief asks about. Second, **the units are dollars per capita per $1,000 per worker of a
trade shock**, and immigration exposure has no dollar denomination. Any comparison with ADH
here has to be made in log points or in standardised units, never in dollars; that translation
is stated in section 5 before the estimates are read.

### Dustmann, Schönberg & Stuhler (2017), QJE 132(1)

Verbatim from the abstract: "the supply shock leads to a moderate decline in local native wages
and a sharp decline in local native employment … the employment response is almost entirely
driven by diminished inflows of natives into work rather than outflows into other areas or
nonemployment, suggesting that 'outsiders' shield 'insiders' from the increased competition."
[SOURCE: 10.1093/qje/qjw032, abstract, as recorded verbatim in
`research/immigration-canon-citation-audit-2026-09-17.md` §C8, fetched 2026-09-17]

**This is a disconfirming prior for design A, and it is the strongest one available.** The
cleanest exogenous immigration supply shock in the literature finds the native employment margin
running through *reduced entry into work*, and states explicitly that it is **not** running
through *outflows into nonemployment*. If displacement onto transfers were the main margin,
DSS is the design that should have found it and did not. A null in this lane is therefore the
result DSS predicts, and a positive transfer response would be the surprising finding requiring
the higher evidentiary bar.

### Ottaviano & Peri — the brief's −6.7% does not survive contact with the text I could reach

The brief asks for "the Ottaviano & Peri (2012, JEEA) long-run effect on earlier immigrants'
wages (about −6.7% per their calibration for 1990–2006 inflow; verify the number from the
paper)." **Verified against the primary text, the −6.7% figure is not in the version I could
obtain, and the version I could obtain is several times larger.**

NBER Working Paper 12497 (August 2006), which is the working-paper version of the JEEA article
and covers 1990–**2004**, Table 7 (long run, Δκ/κ = 0) and Table 8 (capital adjusting), central
specification σ = 6.6:

| Group | Long run (Table 7, σ=6.6) | As of 2004, short run (Table 8) | As of 2009 (Table 8) |
|---|---:|---:|---:|
| US-born, HS dropouts | −1.1% | −2.2% | −1.7% |
| US-born, average | +1.8% | +0.7% | +1.2% |
| Foreign-born, HS dropouts | −16.3% | −17.4% | −16.9% |
| Foreign-born, HS graduates | −23.5% | −24.6% | −24.1% |
| **Foreign-born, average** | **−19.8%** | **−20.9%** | **−20.4%** |

Verbatim from the text: "in the long run the average wage of U.S.-born workers experienced a
significant increase (+1.8%) as a consequence of immigration during the 1990-2004 period …
immigration increases the wages of U.S.-born workers at the expense of a decrease in wages of
foreign-born workers (namely, previous immigrants)" and "The group whose wage was most
negatively affected by immigration is, in our analysis, the group of previous immigrants."
[SOURCE: NBER w12497, pp. 44–45 of the PDF (Tables 7 and 8) and the introduction, extracted
2026-09-18; local copy `_cache/op_nber_w12497.pdf`, text `_cache/op_nber.txt`]

The published JEEA 2012 article is paywalled on Oxford Academic, Wiley and EconPapers, and I
could not obtain its text. The **−6.7%** figure the brief quotes is therefore marked
**[UNVERIFIED]** — it is plausibly the published version's revised number (the published article
extends the window to 2006 and reports a smaller native average gain, +0.6% rather than +1.8%,
which is consistent with a different σ calibration), but I did not read it. This matters for
section 6: using −6.7% versus −19.8% changes the elasticity-transfer bound by a factor of three,
so that section reports **both** and treats the spread as the honest range rather than picking one.

### Borjas (2003), NBER w9755 / QJE 118(4)

Verbatim from the abstract: "The analysis indicates that immigration lowers the wage of competing
workers: a 10 percent increase in supply reduces wages by 3 to 4 percent." And from the text:
"a 10 percent supply shock (i.e., an immigrant flow that increases the number of workers in the
skill group by 10 percent) reduces weekly earnings by about 4 percent."
[SOURCE: NBER w9755, abstract p. 2 and p. 15, extracted 2026-09-18; local copy
`_cache/borjas2003.pdf`]

This is a partial-equilibrium, fixed-capital, national skill-cell elasticity. It applies to
*competing workers* in the cell, native and foreign-born alike, so applying it to the Mexico-born
stock is a use the paper supports; applying it as a *native* elasticity would not be, since
Ottaviano–Peri's whole point is that the native and foreign-born incidences differ.

---

## 2. What the surge was, in numbers

Pinned before the designs so the memo can say what "the surge" means without reaching for a
press release.

**Net international migration, Census Bureau Vintage 2025 national estimates**, estimates years
running July 1 to June 30:

| Estimates year | Net international migration |
|---|---:|
| 2021 | 376,026 |
| 2022 | 1,672,112 |
| 2023 | 2,264,137 |
| 2024 | 2,734,468 |
| 2025 | 1,262,202 |
| **Sum 2021–2024** | **7,046,743** |
| Sum 2021–2025 | 8,308,945 |

[SOURCE: `www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv`,
`INTERNATIONALMIG2021`–`2025` for `NAME = United States`, downloaded 2026-09-18; local copy
`_cache/NST-EST2025-ALLDATA.csv`]

Census's own framing of the same series: net international migration "peaked at 2.7 million in
2024" and "declined to 1.3 million in 2025 (as of July 1)", and is "projected to further decline
to approximately 321,000 in 2026 if current trends continue".
[SOURCE: Census Bureau blog, "New Population Estimates Show Historic Decline in Net International
Migration", January 2026, fetched 2026-09-18]

**Foreign-born stock, ACS 1-year, national:**

| Year | Total population | Foreign-born | Share |
|---|---:|---:|---:|
| 2021 | 331,893,745 | 45,270,103 | 13.64% |
| 2023 | 334,914,896 | 47,831,411 | 14.28% |
| 2024 | 340,110,990 | 50,234,858 | 14.77% |

The foreign-born stock rose by **4.96 million** between 2021 and 2024, against 7.05 million of
cumulative net international migration — the gap is emigration, mortality and survey coverage.
[SOURCE: `api.census.gov/data/{2021,2023,2024}/acs/acs1`, tables B05002 and B01003, fetched
2026-09-18; `derived/national_stock.csv`]

**The Mexican share of it is small.** The national Mexico-born stock over the same period:
10,697,374 in 2021, 11,143,711 in 2024, a rise of **0.45 million**, which is 9% of the total
foreign-born increase. That is consistent with the repo's arrival-cohort memo, which finds
Mexico at 14.3% of foreign-born 2021–24 arrivals aged 25–54, behind a mix led by India, Cuba,
Venezuela, Colombia, China and Haiti.
[SOURCE: `derived/national_stock.csv`;
`research/immigration-mexican-arrival-cohorts-2026-09-18.md` §9]

CBO's January 2025 demographic outlook could not be retrieved — cbo.gov returned HTTP 403 to
every fetch attempt in this run. The Census series above is the authoritative figure used
throughout; **the CBO cross-check the brief asked for is not in this memo** and is listed as a
gap in section 9. [UNVERIFIED for CBO specifically]

---

## 3. Designs, and the data each one could actually reach

### What the 136 lane established, and what changes here

Ladder entry 136 (`research/immigration-employment-entry-displacement-2026-09-18.md`) found the
conventional 2000-base past-settlement instrument for **Mexican** inflow dead on 2008–2023
(pooled first-stage F 3.6, sign flips window to window, failed pre-trend placebo) because the
national Mexico-born stock stopped growing after 2008 and then fell, so the *shift* half of the
shift-share went to zero and reversed. The JRS multi-origin correction was underidentified
(current/lagged predicted inflow correlate 0.82, Shea partial R² 0.0007).

This lane does not contest any of that. It changes **two** things:

1. **It moves the window back to where the shift is large and positive.** The national
   foreign-born stock grew by 6.95 million and the Mexico-born stock by 2.56 million between
   2000 and 2007. A shift-share instrument built on those windows has something to work with,
   and it does: first-stage F of 16 to 29 on the foreign-born arm, against F 3.6 for the
   post-2008 Mexican arm.
2. **It makes the base predetermined.** The base is not the 2000 stock — which is
   contemporaneous with the start of a 2000-based window — but the **pre-1990 entry cohort**
   read off Census 2000, table P022 for all origins and PCT020 for Mexico. National pre-1990
   stock: 17,929,613 foreign-born and 4,733,886 Mexico-born; the 381 metropolitan CBSAs in the
   panel hold 96.1% and 93.7% of those respectively.
   [SOURCE: `api.census.gov/data/2000/dec/sf3`, tables P022 and PCT020 at county level, fetched
   2026-09-18; aggregated to the OMB February-2013 delineation; `derived/base_shares_pre1990.csv`]

### Geography, and a measurement finding that changed the design

Outcomes come from ACS 1-year summary tables published **at CBSA level**. The treatment does
not. The published ACS metro foreign-born share was tried first and abandoned, for a reason
worth recording because it will bite any future lane that reaches for the convenient series:

| Window | corr(level) with fixed-geography PUMS series | corr(**change**) | first-stage F, published | first-stage F, fixed-geo |
|---|---:|---:|---:|---:|
| 2005–2008 | 0.990 | 0.654 | 0.90 | **15.60** |
| 2005–2015 | 0.990 | 0.708 | 1.26 | **6.94** |
| 2013–2023 | 0.991 | 0.824 | 0.03 | 2.59 |

The **levels** agree almost perfectly; the **changes** do not, and the first stage is dead on the
published series (F 0.03 to 1.26) and alive on the fixed-geography one. Two things drive the gap: the published
series is a share of total population while the PUMS series is a share of the population aged
18–64 (the foreign-born are concentrated in working ages, so the same shock moves the
working-age share about 1.55× as much), and CBSA footprints are re-delineated between ACS
vintages, which injects noise into a difference while leaving a level almost untouched. The
treatment therefore uses the employment_entry lane's PUMS series, allocated through Geocorr into
one fixed OMB 2013 delineation. Both arms are estimated and both are in `derived/estimates.csv`;
the published-share arm is labelled and reported as failing.

For the 2000 endpoint and for 2021/2024 no fixed-geography PUMS series exists, so those windows
use the published share and inherit the weakness. This is stated again at each result.

### A second measurement finding: the Mexico leaf is suppressed at metro level

ACS table B05006 publishes the Mexico-born count for only **27 to 43** metros in a given year,
against 500-plus for the foreign-born total. The Mexico-specific arm on the aggregate route is
therefore estimated on a few dozen large metros and its intervals are correspondingly wide. The
fixed-geography PUMS series has no such suppression and carries Mexico for all 330-plus metros;
that is the arm to read for Mexico.

### Sources that could not be reached, and what replaced them

| Brief asked for | Outcome | Replacement |
|---|---|---|
| Census 1990 STF3 for a 1990 base | **Not available.** `api.census.gov/data/1990/sf3` returns 404; the 1990 endpoints are retired. No NHGIS or IPUMS key exists in this environment. | Pre-1990 **entry cohort** from Census 2000 P022/PCT020, which is a 1990-vintage settlement pattern observed in 2000 and is predetermined for every window here |
| SSA "OASDI Beneficiaries by State and County" disabled-worker counts | **Not available.** ssa.gov returned HTTP 403 to every request, with and without a browser user-agent | None. **SSDI is not measured in this lane at all**, which matters because SSDI is the ADH category with the largest and most significant response |
| BEA CAINC35 county transfer receipts | **Stale.** The bulk zip `apps.bea.gov/regional/zip/CAINC35.zip` carries a last-modified date of 2023-11-16, so it cannot cover 2021→2023. No BEA API key is available | ACS household receipt rates for SSI, public assistance and SNAP, which are survey measures of *receipt* rather than administrative measures of *dollars* |
| Census 2000 education-by-employment at county | **Not available.** SF3 P038 is the population aged 16–19, not 25–64, and SF3 has no 25–64 education × employment cross-tab | Employment outcomes start in 2005, where ACS table B23006 exists. The 2000-based windows carry **transfer outcomes only** |
| CBO January 2025 demographic outlook | **Not available.** cbo.gov returned HTTP 403 | Census Vintage 2025, section 2 |

### Disconfirmation arms, fixed before any estimate was read

1. **Placebo.** The window's own instrument against the *previous* period's outcome change. A
   significant coefficient means the instrument tracks pre-existing trends.
2. **Exogeneity test.** The instrument against the *baseline level* of the outcome. The
   shift-share exclusion restriction requires the base share to be unrelated to the outcome path
   except through immigration; if high-base metros already had high transfer receipt, that is a
   direct warning.
3. **Mean-reversion control.** The baseline level of the outcome entered as a covariate.
4. **College control.** The BA+ group, which a skill-specific supply effect should not move.
5. **Sign stability** across windows.
6. **Recovery control**, for 2021–2024 only: the 2019→2021 outcome change as a covariate.

---

## 4. Design A results: the pre-2008 windows, where the instrument is alive

Treatment is the change in the foreign-born share of the metro population, in points. Outcomes
are the percent of households receiving SSI or public assistance. 333 metros with population of
at least 100,000, weighted by 2000 population, HC1 robust standard errors. The 2000-based
windows carry transfer outcomes only, because Census 2000 has no 25–64 education × employment
table at county level (section 3).

### The estimates

| Window | Outcome | First-stage F | IV | 95% interval | IV + mean-reversion control | 95% interval |
|---|---|---:|---:|---|---:|---|
| 2000–2005 | SSI receipt | 18.7 | **−0.297** | [−0.476, −0.118] | −0.219 | [−0.364, −0.073] |
| 2000–2005 | public assistance | 18.7 | **−1.084** | [−1.685, −0.484] | −0.382 | [−0.698, −0.066] |
| 2000–2007 | SSI receipt | 21.5 | **−0.405** | [−0.661, −0.149] | −0.293 | [−0.488, −0.099] |
| 2000–2007 | public assistance | 21.5 | **−1.226** | [−1.888, −0.565] | −0.488 | [−0.804, −0.172] |
| 2000–2008 | SSI receipt | 16.3 | −0.361 | [−0.672, −0.050] | −0.102 | [−0.241, +0.038] |
| 2000–2008 | public assistance | 16.3 | −1.511 | [−2.469, −0.553] | −0.554 | [−0.997, −0.111] |
| 2000–2010 | SSI receipt | 29.1 | **−0.442** | [−0.635, −0.250] | −0.424 | [−0.596, −0.253] |
| 2000–2010 | public assistance | 29.1 | −0.986 | [−1.526, −0.447] | −0.348 | [−0.594, −0.102] |

[SOURCE: `derived/estimates.csv`, rows with `window` beginning "2000-" and `treat` =
"all foreign-born"]

**Every coefficient is negative.** Metros that received more foreign-born inflow over
2000–2010 saw household SSI and public-assistance receipt fall *relative to* other metros, not
rise. The sign is the opposite of the displacement hypothesis, it is stable across all four
windows and both outcomes, and it survives a mean-reversion control in seven of eight cells.

### Why this is not evidence that immigration reduces transfer receipt

Three things say the coefficient is not a supply effect, and they are decisive enough that the
verdict below is a null rather than a reversal.

**1. The exclusion restriction fails a direct test.** The instrument is significantly correlated
with the *baseline level* of the outcome in every window:

| Window | Z on 2000 SSI level | Z on 2000 public-assistance level |
|---|---|---|
| 2000–2005 | +0.254 (SE 0.067) | +0.387 (SE 0.098) |
| 2000–2007 | +0.167 (SE 0.044) | +0.255 (SE 0.064) |
| 2000–2010 | +0.132 (SE 0.035) | +0.201 (SE 0.051) |

Metros with a large pre-1990 immigrant settlement already had higher transfer receipt in 2000.
The instrument is 0.978 correlated with the 2000 foreign-born share itself, so what it is really
asking is "did already-immigrant metros' transfer receipt fall faster," and the answer is yes for
reasons the design cannot pin on immigration.

**2. The implied magnitudes are larger than the entire observed decline.** Over 2000–2007 the
population-weighted mean change in the foreign-born share was **+1.77 points**, while mean
household SSI receipt fell from 4.13% to 3.85% and public assistance from 3.34% to 2.12%.
Multiplying the coefficients by the mean shock:

| Estimate | Implied change at the mean shock | Actual mean change 2000→2007 |
|---|---:|---:|
| SSI, IV | −0.72 pp (−17.4% of base) | −0.28 pp |
| SSI, IV + level control | −0.52 pp (−12.6%) | −0.28 pp |
| public assistance, IV | −2.17 pp (−65.1%) | −1.22 pp |
| public assistance, IV + level control | −0.87 pp (−25.9%) | −1.22 pp |

The uncontrolled public-assistance estimate attributes to immigration **more than the whole
national fall** in public-assistance receipt over the period. That fall has a well-known cause
that has nothing to do with immigration: the post-1996 TANF caseload collapse, which was
largest where caseloads started highest, and caseloads started highest in the same large,
already-immigrant metros the instrument selects. The mean-reversion control cuts the
public-assistance coefficient by 60%, from −1.226 to −0.488, which is exactly the signature of a
mean-reverting national trend being picked up by a cross-sectional instrument. The SSI
coefficient is more robust to that control (−0.405 → −0.293), which is why SSI, not public
assistance, is the outcome worth reporting at all.

**3. Composition is in the wrong direction to rescue the displacement story, and in the right
direction to explain part of this one.** The outcome counts *all* households, immigrants
included. Non-citizen immigrant households have lower SSI and public-assistance receipt than
natives, partly by statute under the 1996 PRWORA bars. Adding immigrant households to the
denominator therefore mechanically pushes the metro receipt rate down. That is a composition
artifact, not a behavioural response, and it is the single most likely explanation for a negative
coefficient of this size. **This lane cannot separate it**, because the outcome is not split by
nativity — the ACS PUMS pull that would have split it did not complete (section 7).

### The college control, and sign stability on the post-2008 windows

The employment outcomes only exist from 2005 onward. Reading the fixed-geography arms there:

| Window | Treatment | F | no-college E/POP | BA+ E/POP (control) | SSI receipt |
|---|---|---:|---|---|---|
| 2005–2008 | all foreign-born | 15.6 | −1.83 [−3.99, +0.34] | **−1.08 [−2.03, −0.13]** | +0.07 [−0.25, +0.39] |
| 2005–2015 | all foreign-born | 6.9 | −2.76 [−4.86, −0.67] | −0.59 [−1.58, +0.40] | +0.26 [−0.04, +0.57] |
| 2005–2015 | Mexico-born | 55.2 | −0.60 [−1.30, +0.10] | **+0.49 [+0.03, +0.95]** | −0.01 [−0.14, +0.13] |
| 2008–2018 | Mexico-born | 44.1 | −0.59 [−1.02, −0.17] | **+0.42 [+0.10, +0.74]** | **+0.21 [+0.08, +0.34]** |
| 2013–2023 | Mexico-born | 74.0 | −0.34 [−0.82, +0.14] | −0.02 [−0.42, +0.38] | +0.12 [−0.01, +0.26] |
| 2018–2023 | Mexico-born | 82.3 | +0.16 [−0.33, +0.66] | +0.17 [−0.22, +0.56] | −0.01 [−0.16, +0.13] |

**The college control moves significantly in three of six rows**, and in 2005–2008 it moves in
the *same* direction as the no-college group. A supply shock concentrated on low-skill labour
should not move BA+ employment at all. When the control group moves with the treated group, the
common cause is metro labour demand, which is what the instrument was supposed to purge.

The one arm that looks like the displacement story — Mexico-born, 2008–2018, no-college E/POP
−0.59 [−1.02, −0.17] with F 44 and a college control moving the *other* way (+0.42) — sits on a
window in which the national Mexico-born stock **fell** by 0.24 million. When the shift is
negative the instrument's sign inverts, and the coefficient is then identified off metros whose
Mexican population shrank fastest, during the Great Recession. That is the failure mode ladder
136 documented, and it applies here unchanged.

**Transfer outcomes on the well-identified Mexican windows are a tight null, and the sign tracks
the sign of the national shift rather than anything about metros.** SSI receipt, all nine
fixed-geography windows, with the national Mexico-born stock change that defines each:

| Window | national Mexico shift | F | SSI receipt IV | 95% interval |
|---|---:|---:|---:|---|
| 2005–2008 | +0.44 M | 5.0 | −0.072 | [−0.358, +0.214] |
| 2005–2010 | +0.74 M | 15.4 | −0.076 | [−0.309, +0.156] |
| 2005–2015 | +0.67 M | 55.2 | −0.007 | [−0.141, +0.127] |
| 2008–2013 | +0.17 M | 11.0 | +0.149 | [−0.243, +0.542] |
| 2008–2018 | **−0.24 M** | 44.1 | **+0.213** | [+0.084, +0.341] |
| 2010–2015 | **−0.07 M** | 37.3 | +0.055 | [−0.135, +0.244] |
| 2013–2018 | **−0.41 M** | 38.8 | **+0.253** | [+0.054, +0.452] |
| 2013–2023 | **−0.67 M** | 74.0 | +0.125 | [−0.011, +0.260] |
| 2018–2023 | **−0.25 M** | 82.3 | −0.013 | [−0.160, +0.134] |

Every window with a **positive** national shift gives a negative or zero coefficient; the two
significant positive coefficients both sit on **negative**-shift windows, where the instrument's
sign is inverted and the coefficient is identified off metros whose Mexican population shrank
fastest through the Great Recession and after. That is not a stable parameter, it is the
sign-flip failure ladder 136 documented, reproduced here on a different outcome.

### Against the ADH benchmark

ADH's units and these are not commensurable in dollars: their shock is denominated in dollars of
import exposure per worker, immigration exposure has no dollar denomination, and their outcome is
transfer *dollars* per capita while this one is household *receipt* rates. The comparison that
can be made is the sign and the relative magnitude. ADH find total transfers rising by
**1.01 log points per $1,000 per worker of exposure** and SSI+TANF+SNAP rising by **3.04 log
points**, both significant at 1%. This lane finds household SSI and public-assistance receipt
**falling** with immigration exposure, at implied relative magnitudes of −13% to −65% of base at
the mean shock. **Every interval in section 4 excludes a positive transfer response of the ADH
sign.** Whether that is because immigration is not a trade shock, or because the design is
picking up mean reversion and composition, cannot be settled here — but a study set up to find
ADH-style transfer displacement did not find it, and found the opposite sign.

This is also what Dustmann, Schönberg & Stuhler predict. Their supply shock moved native
employment through "diminished inflows of natives into work rather than outflows into other areas
or nonemployment." A margin that runs through non-entry rather than exit does not generate
transfer take-up, because people who never entered work are not the people who claim SSDI or SSI.

---

## 5. Design 2: the 2021–2024 shock

### The past-settlement instrument is dead for this shock, and that is the finding

The 2021–2024 inflow did not go where the pre-1990 immigrants went. First stage of the change in
the metro foreign-born share on the pre-1990 shift-share instrument:

| Window | n | first-stage coefficient | SE | F |
|---|---:|---:|---:|---:|
| 2021–2024 | 350 | −0.002 | 0.046 | **0.002** |
| 2021–2023 | 350 | +0.065 | 0.106 | **0.370** |

For comparison, the same instrument on 2000–2007 gives F 21.5. The instrument is not weak here,
it is absent. The 15 largest metros make the reason concrete — predicted inflow against actual
change in the foreign-born share, 2021–2024:

| Metro | instrument Z | actual change (pp) |
|---|---:|---:|
| Los Angeles | 5.26 | +0.85 |
| Miami | 4.58 | +2.10 |
| New York | 3.94 | +1.38 |
| San Francisco | 3.88 | +1.18 |
| Chicago | 2.45 | +1.56 |
| Atlanta | 1.10 | **+2.24** |
| Seattle | 1.52 | **+2.12** |
| Detroit | 1.23 | +1.57 |

The metros the instrument predicts hardest (Los Angeles, San Francisco) had among the *smallest*
increases; the metros it predicts least (Atlanta, Seattle) had the largest. Correlation across all
350 metros: **+0.020**. This is consistent with the origin mix documented in the arrival-cohort
memo — a Venezuelan, Haitian, Cuban and Central American inflow has no pre-1990 settlement
pattern to follow — and with placement by shelter systems, sponsors and parole processing rather
than by 1990s networks.

**Every IV coefficient in this window is therefore uninterpretable**, and they look it: SSI
receipt +11.2 with a 95% interval of [−494, +517]. Those rows are in `derived/estimates.csv` and
are reported only so the failure is on the record.

### The OLS associations, labelled as associations

With no usable instrument, what remains is the cross-metro association between inflow and
outcome change. 350 metros, weighted by 2021 population.

| Outcome | OLS | 95% interval | + 2019→2021 recovery control | 95% interval |
|---|---:|---|---:|---|
| household SSI receipt | +0.018 | [−0.067, +0.103] | +0.012 | [−0.060, +0.085] |
| household public assistance | −0.057 | [−0.176, +0.062] | −0.028 | [−0.119, +0.063] |
| household SNAP receipt | **−0.370** | [−0.669, −0.071] | **−0.366** | [−0.665, −0.068] |
| no-college E/POP 25–64 | +0.055 | [−0.185, +0.295] | +0.030 | [−0.175, +0.236] |
| no-college LFP 25–64 | +0.071 | [−0.194, +0.336] | +0.068 | [−0.152, +0.288] |
| BA+ E/POP (control) | −0.137 | [−0.353, +0.080] | −0.071 | [−0.252, +0.111] |
| BA+ LFP (control) | −0.075 | [−0.268, +0.118] | −0.025 | [−0.194, +0.143] |

[SOURCE: `derived/estimates.csv`, `window` = "2021-2024", `design` in {2, 2-recovctl},
`estimator` in {OLS, OLS+ctl}]

Four readings, in order of what they can bear.

1. **No association with native transfer receipt.** SSI is a tight null (+0.018 [−0.067,
   +0.103]) and survives the recovery control unchanged. Public assistance is null.
2. **SNAP receipt moves the opposite way to the displacement hypothesis**, −0.370 [−0.669,
   −0.071], and the recovery control does not touch it (−0.366). Metros receiving more inflow saw
   household SNAP receipt fall faster over 2021–2024. The obvious alternative explanation is that
   these are also the metros with the strongest post-pandemic labour markets, and 2021–2024 is
   the window in which pandemic-era SNAP emergency allotments were unwound; the composition
   channel from section 4 also applies, since recent non-citizen arrivals are largely SNAP-
   ineligible and enter the household denominator.
3. **No association with native employment.** No-college E/POP +0.055 [−0.185, +0.295].
4. **The post-COVID recovery control barely matters**, which is the one reassuring result: adding
   the 2019→2021 change moves every coefficient by less than one standard error.

### The placebo says these associations are trend, not shock

The disconfirmation test that matters most here fails badly. The 2021–2024 instrument regressed
on the **2019→2021** outcome change, before the shock:

| Outcome | placebo coefficient | SE | significant? |
|---|---:|---:|---|
| household SSI receipt | +0.064 | 0.022 | yes |
| household public assistance | +0.317 | 0.042 | yes |
| household SNAP receipt | +0.455 | 0.123 | yes |
| no-college E/POP | −0.739 | 0.155 | yes |
| BA+ E/POP | −0.409 | 0.065 | yes |
| BA+ LFP | +0.011 | 0.047 | no |

Five of six placebos are significant, and for the employment outcomes the pre-period coefficient
(−0.739) is **larger in magnitude and the same sign** as the post-period reduced form (+0.297 is
the opposite sign, so worse still). High-base metros were already on divergent transfer and
employment paths in 2019–2021. Nothing in this window identifies a 2021–2024 shock effect.

### The exposure measures the brief suggested, and why they were not used

The brief offered three exposure measures. The ACS change in recently-arrived foreign-born by
metro is the direct one, and it needs a PUMS pull of all foreign-born with year of entry, which
this run's link budget could not afford on top of the pull it did run (section 9). City shelter
intake counts for New York, Chicago, Denver, Boston and Washington would give five treated units
against a national control group — a design worth running, but five units is a case study, not
this regression. USCIS pending-asylum counts by office are not a metro-level placement measure.
**The 2021–2024 arm is therefore the weakest in this memo, and its verdict is "not identified"
rather than a number.**

---

## 6. The elasticity-transfer bound

This section is arithmetic, not estimation. It asks: **if** the published elasticities are right,
how large is the annual wage loss to earlier Mexico-born workers and to the Mexican second
generation, and what does that cost the Treasury in forgone tax? Reproduce with
`elasticity_bound.py`; every row is in `derived/elasticity_bound.csv`.

### Inputs, measured here

Wage bills are computed from the held CPS ASEC 2025 file (income year 2024) using the **same
group masks** as the all-age ledger (`gen_ledger_extension_2026_09_16/extend_ledger.py` lines
228–238), so these populations line up with the ledger's per-person fiscal numbers.

| Group | Persons | Wage bill 2024 | Mean wage per earner | Average tax rate on wages |
|---|---:|---:|---:|---:|
| Mexico-born | 12.23 M | **$352.0 bn** | $47,792 | 16.9% |
| Mexican second generation | 14.35 M | **$325.5 bn** | $50,304 | 20.1% |
| Mexican third-plus self-ID | 14.38 M | $326.1 bn | $57,431 | 21.4% |
| Third-plus non-Hispanic white | 173.66 M | $6,752.3 bn | $77,053 | 29.6% |

The Mexico-born population here, 12.23 M, matches the all-age ledger's 12.22 M to 0.1%, which is
the intended cross-check. The tax rate is **FICA plus federal plus state income tax, employee
side only, divided by the group's wage bill** — an average rate, not a marginal one. The all-age
ledger stores no marginal rate, so section 6 carries three rates and labels each.
[SOURCE: `derived/wage_bills.csv`, built by `wage_bills.py` from
`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`]

### A correction to the brief's specification

The brief asks to apply the Ottaviano–Peri earlier-immigrant elasticity to "the Mexico-born stock
and the second generation's wage bill." **Ottaviano–Peri's own structure forbids the second half
of that.** Their large negative number is the effect on *foreign-born* workers, who are imperfect
substitutes for natives; that imperfect substitutability is the entire mechanism. The Mexican
second generation is US-born and takes their *native* elasticity, which is **+1.8% on average**
and **−1.1% for high-school dropouts** (NBER w12497 Table 7, σ = 6.6). Applying −19.8% to a
native-born group would contradict the paper being cited. The second generation is therefore
carried with the native elasticity, and the result is small and of ambiguous sign.

### Bound 1: an Ottaviano–Peri-scale inflow

Scope: the *cumulative* effect of fourteen years of immigration, 1990–2004, an inflow equal to
11.0% of initial employment overall and 20% for high-school dropouts. This is not a per-unit
elasticity, and it is not the 2021–2024 shock.

| Group | Elasticity applied | Annual wage change | Fiscal change (tax rate 16.9% → 35%) |
|---|---|---:|---|
| Mexico-born | −19.8% (verified, long run, σ=6.6) | −$69.7 bn | −$11.8 bn to −$24.4 bn |
| Mexico-born | −20.9% (verified, as of 2004) | −$73.6 bn | −$12.5 bn to −$25.7 bn |
| Mexico-born | −16.3% (verified, HS dropouts) | −$57.4 bn | −$9.7 bn to −$20.1 bn |
| Mexico-born | **−6.7% (the brief's figure, [UNVERIFIED])** | **−$23.6 bn** | **−$4.0 bn to −$8.2 bn** |
| Mexican second generation | +1.8% (native average) | +$5.9 bn | +$1.2 bn to +$2.1 bn |
| Mexican second generation | −1.1% (native HS dropouts) | −$3.6 bn | −$0.7 bn to −$1.3 bn |

**The unverified figure the brief supplied and the verified one differ by a factor of three**, and
that spread is the dominant uncertainty in this bound — larger than the spread across tax rates,
and larger than the second-generation term altogether. That is why the memo reports both.

### Bound 2: Borjas, applied to the actual 2021–2024 inflow

Borjas (2003): a 10% increase in a skill group's supply reduces wages by 3 to 4%, partial
equilibrium with capital fixed. The 2021–2024 foreign-born stock increase of **4.96 million** is
**2.95%** of the 2024 civilian labour force of 168.1 million, so the implied wage effect on
competing workers is −0.9% to −1.2%. Unlike Ottaviano–Peri's, this elasticity applies to
competing workers of any nativity, so it covers both groups.

| Group | Wage change | Fiscal change |
|---|---:|---|
| Mexico-born | −$3.1 bn to −$4.2 bn | −$0.5 bn to −$1.5 bn |
| Mexican second generation | −$2.9 bn to −$3.8 bn | −$0.6 bn to −$1.3 bn |
| **Both, combined** | **−$6.0 bn to −$8.0 bn** | **−$1.1 bn to −$2.8 bn** |

### What the bound does and does not say

The two bounds answer different questions and must not be added. Bound 1 is the cumulative effect
of a historical fourteen-year inflow; bound 2 is the effect of the actual three-year 2021–2024
inflow. Read as a range on the annual fiscal cost of wage incidence falling on Mexican-origin
workers, the defensible statement is:

> **$1 bn to $3 bn a year** if the recent inflow is scored with Borjas's partial-equilibrium
> elasticity, rising to **$4 bn to $26 bn a year** if a 1990s-scale inflow is scored with
> Ottaviano–Peri's structural earlier-immigrant elasticity, where the factor-of-three width inside
> that upper range is entirely the unresolved −6.7% versus −19.8% question.

Three caveats bind this hard. First, the whole exercise is a **transfer of other people's
elasticities**, and both are contested: Ottaviano–Peri's rests on a nested-CES calibration whose
substitution parameter is the object under dispute, and Borjas's national skill-cell design holds
capital fixed, which Ottaviano–Peri's own results say roughly halves the long-run effect. Second,
**a wage loss is not a deadweight loss**: most of it is a transfer to employers, consumers of
immigrant-intensive services and complementary native workers, and Cortes (2008) finds the price
channel is real. The fiscal column is forgone *tax* on that transferred wage, not lost output.
Third, applying a national elasticity to one national origin group presumes Mexican-origin workers
sit in the affected skill cells in proportion to their wage bill; the repo's own wage-residual
work says they are more concentrated there than average, so the bound is, if anything, low for
that reason and high for the reasons above.

---

## 7. Design B, and the nativity-split version of Design A

The ACS PUMS pull completed for 2005, 2008, 2021 and 2024 (Vermont is missing from 2005
only; the 8 metros spanning it are dropped from every year, so no metro changes footprint).
380 metros. This panel does two things the aggregate route could not.

**Where it is identified.** The employment_entry lane's fixed-2013-geography treatment series
exists for 2005 and 2008, and only there. The 2005→2008 window has a first stage of **F 13.0**.
Every window ending in 2021 or 2024 has to use the published ACS share and its first stage is
dead (F 0.07 to 0.87), so those rows are ordinary least squares associations and are reported as
such. Full grid in `derived/estimates_pums.csv`.

**Two measurement defects, found and handled rather than buried.**

1. **ACS 2005 codes weeks worked as a continuous 1–52 value; 2008 codes it as a bracket where
   1 = "50 to 52 weeks".** The pull's full-time-full-year test was `WKW == 1`, so in 2005 it
   selected people who worked *exactly one week*. The 2005 full-time share comes out at 0.001
   against 0.56 in 2008. **Every 2005 full-time-full-year cell is discarded** and the full-time
   wage windows start in 2008. Per-person wage measures do not use the weeks variable and keep
   2005. [SOURCE: `api.census.gov/data/{2005,2008}/acs/acs1/pums/variables.json`, `WKW` value
   ranges, checked 2026-09-18]
2. **The ACS SNAP question begins in 2008.** The 2005 SNAP cells read 0.01%, so SNAP windows
   start in 2008. The `FS` variable is present in the 2005 dictionary, which is what made this
   worth checking.

### 7a. The nativity split closes the composition objection, and the sign does not change

Section 4's caveat was that its transfer outcomes count all households, so immigrants' own low
take-up could produce a negative coefficient mechanically. Here the denominator is natives aged
25–54 below a bachelor's degree, so that channel is closed by construction. 2005→2008,
fixed-geography treatment, F 13.0, 348 metros, weighted by base-year native no-college
population.

| Outcome | OLS | reduced form on Z | 95% interval | IV | 95% interval |
|---|---:|---:|---|---:|---|
| native SSI receipt | +0.017 | **+0.174** | [+0.013, +0.335] | **−0.490** | [−0.977, −0.003] |
| native public assistance receipt | −0.062 | +0.005 | [−0.146, +0.155] | −0.013 | [−0.432, +0.406] |
| native E/POP | +0.379 | −0.132 | [−0.538, +0.275] | +0.370 | [−0.687, +1.428] |
| native LFP | +0.217 | +0.109 | [−0.158, +0.375] | −0.306 | [−1.093, +0.482] |

The first stage in this window is **negative** (−0.355, SE 0.098): metros with a large pre-1990
immigrant base saw their foreign-born share grow *less* over 2005–2008. The IV coefficient is the
reduced form divided by that negative first stage, which is why the reduced form is reported
first — it is the object the instrument actually identifies. Read directly: metros where the
immigrant share grew *less* saw native SSI receipt rise *more*. Equivalently, more inflow, less
native SSI receipt.

**The conclusion that matters:** the negative sign on transfer receipt in section 4 is **not** a
composition artifact. It survives restricting the outcome to natives only. That removes the third
of section 4's three caveats and leaves the first two — failed instrument exogeneity and mean
reversion — as the live explanations. Native employment and participation are null in every
specification, which is the DSS-consistent result.

### 7b. Design B: wages of earlier Mexico-born workers

Outcome is the log mean wage of Mexico-born workers aged 25–54 who arrived **before 2000**,
against the change in the metro foreign-born share. Coefficients are in **percent per
percentage point** of inflow. 2005→2008, F 13.0.

| Outcome | n | OLS | IV | 95% interval |
|---|---:|---:|---:|---|
| earlier Mexico-born, wage per person | 292 | −0.01 | **−7.18%** | [−23.83, +9.46] |
| earlier Mexico-born, below BA, wage per person | 288 | +0.85 | +0.52% | [−14.56, +15.60] |
| earlier Mexico-born, E/POP (pp) | 299 | −0.15 | −2.08 | [−12.23, +8.08] |
| **2000+ arrivals**, wage per person | 240 | +3.15 | −13.36% | [−39.43, +12.72] |

[SOURCE: `derived/estimates_pums.csv`, `window` = "2005-2008"]

**The point estimate lands almost exactly on the number the brief asked about, and the interval
cannot tell it apart from anything else.** −7.18% per point of inflow is close to the brief's
−6.7%, but the 95% interval [−23.8, +9.5] contains zero, contains the verified Ottaviano–Peri
long-run figure, and contains the brief's figure. A scaling is needed to compare at all, and it
is my own arithmetic, not the paper's: Ottaviano–Peri's 1990–2004 inflow was **11.0% of initial
employment**, which on a 1990 foreign-born employment share near 9% implies the share rose to
about 18%, roughly **+9 points**. Their −19.8% over +9 points is about **−2.2% per point**; the
brief's −6.7% is about **−0.74% per point**. My interval of [−23.8, +9.5] contains both, and
zero, comfortably. [INFERENCE for the scaling; the 11.0% and −19.8% are [SOURCE: NBER w12497
Table 7 and its note]]

**The predicted ordering does not appear.** The Ottaviano–Peri / Card / Manacorda-Manning-Wadsworth
prediction is that *earlier* immigrants are the largest losers. Here the 2000-and-later arrivals
show the larger wage loss (−13.4%) and the earlier arrivals the smaller (−7.2%), with both
intervals wide enough that the ordering is not established either way. The education-restricted
arm, which should show the effect most sharply if it is a low-skill supply effect, is a clean
null (+0.52% [−14.6, +15.6]).

**Two scope limits bind design B hard.** First, a 3-year window measures a short-run response,
while Ottaviano–Peri's number is the cumulative effect of fourteen years with capital adjusting;
these are not the same parameter, and the comparison above is indicative only. Second, the
"arrived before 2000" cohort is not the same people in 2005 and in 2024 — someone aged 25–54 in
2024 who arrived before 2000 was at most 29 at arrival, while the same cell in 2005 includes
people who arrived as adults in the 1980s. That composition drift is why the long windows are
reported as associations and the 3-year window carries the inference.

### 7c. The Mexican second generation cannot be done at metro level, at all

The brief asks for Mexican second-generation wages at metro level. **The ACS has carried no
parental-birthplace variable since 1970**, so the second generation is not identifiable in ACS
microdata at any geography. Only the CPS has parental nativity, and its metro identification is
limited to large areas with sample sizes that will not support a 372-metro panel. The second
generation therefore appears in this memo only as a **national wage bill** in section 6
($325.5 bn, 14.35 M people), taken from CPS ASEC 2025, and the elasticity applied to it there is
Ottaviano–Peri's *native* elasticity, for the reason given in section 6. There is no design B
estimate for the second generation and there cannot be one from ACS.

---

## 8. What is and is not identified

**The unit is a metro, not a person.** Every coefficient is a between-metro comparison. A native
who leaves the labour force in Los Angeles and claims SSI in Nevada leaves this design as a
*fall* in Los Angeles exposure and a *rise* in Nevada transfers, unattributed. Card's
native-mobility null is the reason area studies survive this objection at all, and the canon
audit rates that null as holding; but it bounds rather than removes the problem.

**No legal status.** Nothing here distinguishes a parolee from a green-card holder from a
naturalised citizen. That matters most for the transfer outcomes, because eligibility for SSI,
TANF and SNAP is status-conditional under the 1996 PRWORA bars, so the *same* inflow has
different mechanical effects on measured receipt depending on a composition this lane cannot see.

**Survey receipt, not administrative dollars.** Outcomes are ACS and Census self-reported
*receipt* rates, not program expenditure. ADH used BEA transfer dollars and SSA administrative
counts. Self-reported transfer receipt is under-reported in household surveys, and the
under-reporting rate differs by program and probably by nativity — a bias this lane cannot sign.

**SSDI is not measured.** The ADH category with the largest, most significant response
(+8.40 per $1,000/worker, SE 2.21, and +1.96 log points) has no counterpart here, because SSA's
county beneficiary files were unreachable and BEA CAINC35 does not carry SSDI. **The single most
likely place to find the effect the brief hypothesised is the one place this lane could not
look.** That is the most important gap in the memo.

**The aggregate transfer outcomes are not split by nativity; the PUMS ones are.** Sections 4 and
5 count all households. Section 7a repeats the exercise on natives only for the one window where
both the outcome and a live instrument exist, and the sign does not change — which is what lets
the memo say composition is not driving the result, for that window.

**No second generation at metro level, ever, from ACS.** ACS has carried no parental-birthplace
variable since 1970 (section 7c).

**The instrument's exclusion restriction fails a direct test** in 61 of 100 arms. That is the
binding limitation on Design A and the reason its verdict is a null rather than a reversal.

**The 2021–2024 arm identifies nothing.** First-stage F of 0.002 to 0.9 and five of six placebos
significant. Its numbers are associations and are labelled as such throughout.

---

## 9. Disconfirmation results

All six arms were specified in section 3 before any estimate was read. Five of six fail or come
back adverse, and the memo's verdict is built on that.

| Test | Result | Verdict |
|---|---|---|
| **1. Placebo** — instrument against the prior period's outcome change | **42 of 59 arms significant at 5%**. For 2005–2008 the SSI placebo is −0.147 (SE 0.037), the *same sign* as the contemporaneous effect. For 2021–2024, five of six are significant and the employment placebo (−0.739) is larger than the post-period reduced form | **FAILS** |
| **2. Exogeneity** — instrument against the baseline level of the outcome | **61 of 100 arms significant**. In the headline 2000–2007 window, Z predicts the 2000 SSI level at +0.167 (SE 0.044) and the 2000 public-assistance level at +0.255 (SE 0.064). The instrument correlates 0.978 with the 2000 foreign-born share itself | **FAILS** |
| **3. Mean-reversion control** | Cuts the public-assistance coefficient 60% (−1.226 → −0.488) and the SSI coefficient 28% (−0.405 → −0.293). The 2000–2008 SSI cell loses significance entirely (−0.361 → −0.102 [−0.241, +0.038]) | **PARTIAL** — SSI survives, public assistance largely does not |
| **4. College control** | Moves significantly in **7 of 36** fixed-geography IV arms, including *the same direction* as the no-college group in 2005–2008 (−1.08 [−2.03, −0.13]) | **FAILS for the windows where it moves** |
| **5. Sign stability** | Design A's transfer sign is stable and negative across all four 2000-based windows and both outcomes. The Mexican arm's SSI sign **tracks the sign of the national shift**, not anything about metros: negative or zero in all four positive-shift windows, positive in four of five negative-shift windows | **FAILS for the Mexican post-2008 arm; HOLDS for the 2000-based foreign-born arm** |
| **6. Recovery control** (2021–2024) | Every coefficient moves by less than one standard error when the 2019→2021 change is added | **PASSES** |
| **7. Nativity split** (added, not pre-specified) | The negative SSI sign survives restricting the outcome to natives only: IV −0.490 [−0.977, −0.003], reduced form +0.174 [+0.013, +0.335] on a negative first stage | Composition is **not** the explanation |

The one arm that would have supported the displacement hypothesis — Mexico-born, 2008–2018,
SSI +0.213 [+0.084, +0.341] with F 44 — fails tests 1, 4 and 5 simultaneously: its placebo on
2005–2008 is significant, its college control moves the other way significantly, and its sign
reverses on every positive-shift window.

---

## 10. Gaps, and what a successor lane should do first

1. **SSDI, the highest-value missing piece.** SSA's "OASDI Beneficiaries by State and County"
   files returned HTTP 403 to every request in this run. ADH's largest transfer response is SSDI.
   A successor should get those files by another route and re-run section 4's windows on
   disabled-worker counts per capita. Until then the brief's core hypothesis is **untested on its
   most likely margin**, not refuted.
2. **BEA CAINC35 is stale at the source.** The bulk zip carries a 2023-11-16 last-modified date,
   so it cannot reach 2023. A BEA API key would give the current vintage and put the outcome in
   transfer *dollars*, which is ADH's unit and would make the benchmark comparison direct rather
   than sign-only.
3. **CBO's January 2025 demographic outlook** could not be fetched (cbo.gov 403). Section 2's
   surge figures rest on Census Vintage 2025 alone, with no independent cross-check.
4. **The published JEEA version of Ottaviano–Peri.** The brief's −6.7% remains [UNVERIFIED] and
   the verified working-paper figure is −19.8%. That factor of three is the largest single
   uncertainty in section 6's bound, and it is resolvable by one library request.
5. **The city-shelter design for 2021–2024.** The past-settlement instrument is dead for this
   shock (section 5), so the only credible design is the placement shock itself: shelter intake
   counts for New York, Chicago, Denver, Boston and Washington against a synthetic control. New
   York's counts are already staged in
   `infra/immigration-fiscal/frontier_execution_2026_09_17/local/`. Five treated units is a
   case study, and should be built as one rather than as a regression.
6. **A fixed-geography treatment series for 2021 and 2024.** The whole 2021–2024 arm is weakened
   by having to use the published metro share. Extending the employment_entry lane's PUMS
   share-of-18-64 series to 2024 would cost one more all-foreign-born PUMS pull and would let
   section 5 be estimated on the same footing as section 4.
7. **Re-pull ACS 2005 with the correct weeks variable.** The 2005 full-time-full-year cells are
   unusable because `WKW` is continuous in 2005 and bracketed from 2008 (section 7). A one-year
   re-pull with `wkw >= 50` would restore the 2005→2024 full-time wage window for design B.
8. **Under-reporting.** The repo has a `ledger-underreport` lane; its adjustment factors were not
   applied to the survey receipt rates used here.

### What ran, what did not, and why

| Component | Status |
|---|---|
| ACS 1-year metro aggregate panel, 13 years 2005–2024 | complete, 6,716 metro-years |
| Census 2000 SF3 county endpoint + pre-1990 base | complete, 3,141 counties → 381 metro CBSAs |
| ACS PUMS PUMA cells, 2005/2008/2021/2024 | complete, 203 of 204 state-years (Vermont 2005 missing; the 8 metros touching it dropped from every year) |
| Aggregate estimates, 2,004 rows | complete, re-runs byte-identical |
| PUMS estimates, 158 rows | complete |
| Wage bills from CPS ASEC 2025 | complete |
| Elasticity-transfer bound | complete |
| SSA county SSDI counts | **not obtained** — HTTP 403 |
| BEA CAINC35 county transfers | **not used** — source vintage predates 2023 |
| CBO January 2025 outlook | **not obtained** — HTTP 403 |
| Census 1990 STF3 for a 1990 base | **not available** — API endpoint retired, no NHGIS key |
| Mexican second generation at metro level | **impossible from ACS** — no parental nativity since 1970 |
| City shelter-intake design | **not run** — out of scope for a regression design |

---

## 11. Sources

- Autor, D., Dorn, D. & Hanson, G. (2013), "The China Syndrome: Local Labor Market Effects of
  Import Competition in the United States", *AER* 103(6):2121–68, 10.1257/aer.103.6.2121.
  Table 8 and pp. 2149–50. Local copy `_cache/adh2013.pdf`.
- Ottaviano, G. & Peri, G. (2006), "Rethinking the Effects of Immigration on Wages", NBER
  Working Paper 12497. Tables 7 and 8. Local copy `_cache/op_nber_w12497.pdf`. The published
  JEEA 2012 version is paywalled and was not read.
- Borjas, G. (2003), "The Labor Demand Curve Is Downward Sloping", NBER Working Paper 9755,
  abstract and p. 15. Local copy `_cache/borjas2003.pdf`.
- Dustmann, C., Schönberg, U. & Stuhler, J. (2017), *QJE* 132(1), 10.1093/qje/qjw032, abstract as
  recorded in `research/immigration-canon-citation-audit-2026-09-17.md` §C8.
- Jaeger, D., Ruist, J. & Stuhler, J. (2018), NBER w24285, as recorded in the canon audit §C7 and
  used by `research/immigration-employment-entry-displacement-2026-09-18.md`.
- Census Bureau, Vintage 2025 national and state population estimates,
  `NST-EST2025-ALLDATA.csv`.
- Census Bureau ACS 1-year summary tables at CBSA level, 2005–2024: B19056, B19057, B22010,
  B23006, B05002, B05006, B01003, via `api.census.gov`.
- Census Bureau ACS 1-year PUMS, 2005/2008/2021/2024, via `api.census.gov`.
- Census 2000 Summary File 3, tables P022, P063, P064, PCT019, PCT020 at county level.
- MCDC Geocorr 2014 and 2022 PUMA→county allocation factors; OMB February-2013 CBSA delineation.
- CPS ASEC 2025 (income year 2024), held file
  `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`.
- Prior repo lanes: `employment_entry_2026_09_18` (treatment series, crosswalks, 2000 PCT019
  pull), `all_age_ledger_2026_09_17` (group definitions and population cross-check),
  `arrival_cohorts_2026_09_18` (origin mix of the 2021–24 arrivals).

### Instrument bias note `[FRAMING-SENSITIVE]`

This memo was produced by an LLM on a politically charged question, and the repo's standing
caveat (`notes/llm-bias-caveat.md`) applies. Two things are worth naming. The lane was dispatched
to look for a *cost* — native withdrawal onto transfers — and it returned a null and, in the
better-identified windows, the opposite sign. That direction of error is the one a model with a
post-training disposition toward immigration-favourable conclusions would be most likely to
produce, so the disconfirmation section is the part of this memo to audit hardest. Against that,
the same lane reports a wage-incidence bound of $1–26 bn a year falling on Mexican-origin workers
(section 6) and declines to use the more immigration-favourable of the two Ottaviano–Peri figures
without verification. The strongest claim here is a **negative** one about what the data can
support, and negative claims are the least sensitive to the instrument's disposition.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).

## Revisions — September 22, 2026

A second instrument for the 2000–2010 window, the public Burchardi–Chaney–Hassan ancestry
push-pull prediction aggregated to the same 2013 CBSAs, is stronger (F 63.9 against 29.1),
passes the baseline-level exogeneity test that the settlement instrument fails (−0.085 ± 0.083
against +0.132 ± 0.035 on the 2000 SSI level) and carries a third of its variance from Mexico
rather than two thirds. With it the household SSI response is −0.28 (SE 0.06) instead of
−0.44 (0.10) and the public-assistance response is −0.10 (0.19), a null, instead of −0.99
(0.28); Hansen J rejects the pair (p 0.011 and 0.0002). The negative claim of this memo stands;
the public-assistance association in the table above should be read as not surviving a cleaner
instrument. Employment and participation were not testable at the 2000 endpoint. Ladder 182,
[lane](../infra/immigration-fiscal/ancestry_instrument_2026_09_22/RESULT.md).

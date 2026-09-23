**Verdict:** The datasets behind the main case contain real defects. They run in both directions,
and no correction or combination changes the sign. Summed, the data and keying defects move the
$203.2–249.6bn main case by **−$29bn to +$3bn, −$13.5bn at central values**, to about $190–236bn.
The five measured corrections alone move it by about −$5bn, to $198–245bn.
[CALCULATION: `synthesis.py` → `derived/synthesis_net.csv`]

The largest items come from mapping survey records onto national budget totals, not from errors
inside the survey files:
- ACA premium tax credits are keyed as if they were EITC (−$14.2bn). Treasury paid $118.4bn of
  premium credits in 2024, 52% of BEA's refundable-credit line. The group accounts for 10.9% of
  subsidized marketplace enrollees but 23.0% of EITC and child-credit dollars.
- The Census tax model assumes every respondent is a resident filer who complies fully (+$5bn to
  +$17bn, depending on how much unauthorized work is on the books).
- The $385bn of federal income tax the CPS misses, mostly at the top, is spread by CPS liability
  (+$9.5bn).

The largest measurement discrepancy is inside the CPS. ASEC 2025 counts 12.23M Mexico-born residents.
That is 1.1–1.2M more than both ACS 2024 and ASEC 2026, and all of the excess is outside
California and Texas and among noncitizens (−$6bn to −$8bn if the ACS is right).

Ethnic categories are mishandled in three crime files:
- Police code 95–99% of Hispanic arrestees as White by race.
- BJS jail counts record Hispanics at 14.4% of inmates, against 22% of arrests.
- The ACS coded a quarter of Mexico-born inmates as generic "Other Hispanic" in 2021–2023.

The main case already corrects the ACS coding. Two memo comparisons that rested on raw or modelled
cells are corrected in this pass.

Date: 2026-09-23. Operator: "Did we ever look at issues with the datasets itself? Just formatting
errors, bad columns, weird statistics that can't be real given real world knowledge and taste? Bad
political ways to categorize etc?" and "/analyze". Brief: [BRIEF.md](BRIEF.md). Family reports,
which carry the evidence and run commands: [cps.md](cps.md), [acs.md](acs.md),
[spending.md](spending.md), [crime.md](crime.md).

## Effects on the main case

Effects are in $bn a year of cost to other residents. A negative effect means the published main
case is too high.

| # | Defect | Grade | Effect | Status |
|---|---|---|---:|---|
| 1 | BEA refundable credits ($228.8bn, Table 3.12 line 25) are keyed by CPS EITC+ACTC, where the group holds 23.0%. Treasury paid $118.4bn of premium tax credits in 2024, and the group holds 10.9% of subsidized marketplace persons | A | **−14.2** | measured (`spending_mts_credits.py`); keying confirmed in `full_account_spending_2026_09_20/builder.py` lines 120, 204 |
| 2 | The tax model treats every respondent as a resident, fully compliant filer, so receipts are keyed by modelled liability and wages and EITC/ACTC is modelled for filers without valid SSNs | B | +5.0 / +10.6 / +17.0 at 75% / 60% / 44% on-books | modelled bound; no status adjustment exists in `full_account_receipts_2026_09_20` |
| 3 | The $385bn BEA–CPS federal income tax gap is keyed by CPS liability (group 5.7%), although it is mostly top incomes and capital gains | B | **+9.5** (existing `federal_gap_high_agi` arm) | arm exists, not in the main case |
| 4 | Mexico-born count: CPS ASEC 2025 12.23M against ACS 2024 11.0M (households) or 11.15M (with group quarters) and ASEC 2026 11.1M; the excess lies outside CA+TX, among noncitizens, ~6 SE | B | −6.0 to −8.3 if the ACS is right; 0 if ASEC 2025 is | discrepancy measured; which instrument is right is not settled |
| 5 | BEA Medicaid ($954bn) is spread by a MEPS community-only key, so institutional and home-based long-term care is charged to the group at 12.3% instead of an estimated 4–8% | B | −3.6 to −15 | bounded |
| 6 | The education key puts 93% on K–12; BEA's split is 77–82% | B | **−2.2 to −4.8** | measured |
| 7 | The justice key uses FBI 2019 arrests (Hispanic RR 1.145); the repo holds 2023 and 2024 Table 43C (1.216, 1.205) | B | **+1.1** | measured |
| 8 | Unallocable state and local spending ($168.7bn) gets the administration elasticity 0.84 instead of the all-spending 0.96 | C | **+2.0** | measured |
| 9 | The MEPS donor filter drops 207 records that carry 3–4% of Medicare and Medicaid dollars | C | 0 to −2 | bounded |
| 10 | Foster care and adoption spending is keyed by WIC | C | −1 to −2 | bounded |
| — | Hispanic-origin allocation, grants at the low end, top-code swaps, sentinels, weights, birthplace flags | D | each under ±1 | measured |
| 11 | Household rental assistance ($60bn) is held fixed as a business subsidy | choice | 0 now; +7.5 if it responded | classification, not in the net |
| 12 | Income-security consumption ($168bn, mostly social services and administration) is keyed by CPS public assistance (group 16.7%) | choice | 0 now; −7.5 with a population key, −20 with an all-cash key | key choice, not in the net |

Bold marks the five measured corrections (rows 1, 3, 6, 7, 8): −$3.8bn to −$6.4bn, central −$5.1bn.

**Net.** Rows 1–10 and the small items sum to −$29.2bn, −$13.5bn and +$3.0bn at their low, central
and high values. The central uses 60% on-books for row 2, the ACS count for row 4 and the midpoint
of row 5's bound. Rows 11 and 12 are classification choices, not data errors. With them the range is
−$49bn to +$10bn.

**Combining.**
- Rows 1 and 2 share no dollars: the EITC status correction applies only to the $110.5bn of the
  line that is not premium credits.
- Rows 2 and 3 overlap on the gap part of federal receipts, by under $1bn.
- Row 4 interacts with rows 1–3 at second order, about $1bn.
- Row 5 must be combined line by line with the running pooled-MEPS ethnicity lane, which re-keys the
  same Medicaid dollars within age and nativity cells. The two are not added.
- The running CPS imputation lane re-keys the same receipt keys for hot-deck fill-ins; combine it
  with row 2 key by key.

**Row 1 in detail.** BEA footnote 6: line 25 "includes the amounts by which federal refundable tax
credits reduce personal current tax liabilities … as well as the outlays". Calendar-2024 Treasury
outlays were:
- premium credits $118.35bn;
- EITC above liability $60.13bn (October is blank in the statement);
- child credit above liability $26.29bn.

[SOURCE: Monthly Treasury Statement Table 5, api.fiscaldata.treasury.gov; `derived/spending_mts_credits.json`]
That leaves $110.5bn of the line for EITC, the child credit and their liability offsets. Two things
push the group's true premium-credit share below the 10.9% person share: credit per enrollee rises
with age, and imputed unauthorized residents cannot receive the credit. So −$14.2bn is more likely
too small than too large [INFERENCE]. The spending audit's range was −$12.0bn to −$14.4bn for
$100–120bn of premium credits. The probe reproduces −12.02 / −13.22 / −14.43.

**Checks by the parent.**
- Every CPS, crime and spending script reran byte-identical (39 derived files).
- The builders confirm the keying of line 25 and that receipts carry no status adjustment.
- The ACS count with group quarters (11.15M) is row 4's low end; households only (11.0M) is its
  high end. The CPS universe, civilian noninstitutional, lies between them.

## What would settle it

The analysis contract for this audit:
- **Leading explanation:** key mapping, two-sided, central −$13.5bn.
- **Top alternative:** the net is near zero or positive. That happens if on-books work is near SSA's
  2010 figure of 44%, ASEC 2025's count is right (row 4 at 0) and long-term care use sits at the
  mild end of row 5. The net would then be +$3bn to +$9bn.

Three measurements decide which it is:

1. **Row 2: the on-books share of unauthorized Mexico-born earnings in 2024.** The only figure held
   is SSA's 44% for 2010. A newer SSA actuarial note or an earnings-suspense estimate would place the
   row between +$5bn and +$17bn.
2. **Row 4: which Mexico-born count is right.** Candidate evidence: the ACS 2025 1-year file (check
   whether it is released), the DHS/OHSS stock estimates and the CPS monthly files for 2024–25. ASEC
   2026 already sides with the ACS.
3. **Row 5: the group's share of Medicaid long-term care.** ACS 2024 institutional residents 65+ by
   origin (nursing homes dominate that cell), and MCBS or T-MSIS long-term care users by ethnicity.
   This places the row between −$4bn and −$15bn.

**Decision impact:** nothing here reverses the sign or the ranking of results. The operator's choices
are:
- adopt the five measured corrections now (about −$5bn);
- hold rows 2, 4 and 5 as a band until measured;
- decide whether rows 11 and 12 stay classification choices.

## Categories and coding (the "political categories" question)

| Where | What | Effect | Status |
|---|---|---|---|
| NIBRS TX/AZ/CA arrestees | 95.5–98.6% of Hispanic arrestees are coded White by race. Constructions that subtract all Hispanics from White overstate Hispanic/NH-white arrest ratios by 1–5% | memos only; makes the group look worse | noted |
| BJS *Jail Inmates 2023* | Hispanic 14.4% of inmates against 18.4% of adults and 22.1% of adult arrests, flat 2013–23. BJS adjusts prisoners, not jails | weakens the justice lane's "three estimates agree"; the BJS arm would be +$2.45bn | note added to the justice lane |
| ACS 2021–2023 group quarters | 25–30% of Mexico-born inmates (by birthplace) coded generic "Other Hispanic" (2.5% in 2019, 5.4% in 2024): a processing regime, not self-identification | raw arm −$1.9bn; the central already reallocates | corrected in the central |
| Generation split, item N | institutional care counts raw HISP=02, without that reallocation | ledger −$21 to −$57 per person (~1%), $1.8bn | deferred to the next ledger rebuild |
| ACS 2020+ schooling | "no schooling completed" jumps 4.4 points for Latin American-born adults (−0.25 years); below-high-school share unchanged; natives unaffected | years-of-schooling comparisons across 2019/2020 | priced in ladder 197 |
| Census 1980 institutions | 26–29% of inmates' education allocated from household-like donors | crime-selection lane's 1980 education-held rows; direction unmeasured | noted |
| SHR | offender ethnicity missing for whole states (KY, OK 99%, MI 90%, LA 80%, CA 43%) | none after reweighting (0.1033 → 0.1024) | checked |
| CPS race | edited or allocated for 36% of G1 and 32% of G2 (the CPS has no "some other race" answer) | none on the account; anything on `PRDTRACE` for Hispanics is contaminated | noted |
| ACS 2020 race question | 5M native non-Hispanic whites moved from "white alone" to multiracial | <0.5% of per-person gaps | checked |
| CPS parents' birthplace | no "unknown" code, so every blank is hot-decked: 5.4% of G2/G3+ adults vs 2.55% of the white reference | union ≈ 0 | checked |
| 1990/2000 censuses | institution type not recorded; Rumbaut's "correctional" 2000 figures cover all institutions | FAQ 12, generation memo | corrected (7a44b69) |
| 2000 census birthplace | US birthplace allocated to 98% of allocated inmates | 3.45× → 2.7–3.0× | corrected (f88a52b, e6bcf01) |

## Memo claims corrected in this pass

- **Incarceration memo, 5-year origin table.** Central American and Dominican cells were read raw
  against whites while the Mexican cell was quoted coding-adjusted. With the same correction,
  Guatemalans read 0.99–1.26× whites, Dominicans 1.02–1.30× and Salvadorans 0.69–0.88×. So "at or
  below native whites" fails for the first two; the ordering below Mexicans holds (acs.md F5).
- **Generation memo §3.** The 18.8% "EITC use" for Mexico-born adults 25–64 is tax-model output.
  With the SSN rule applied to the imputed unauthorized it is 10.0% (cps.md 1b).
- **Justice lane RESULT.** "The Crime Data Explorer totals carry race only" missed the held 2023 and
  2024 Table 43C files (row 7), and "three estimates agree" leans on the under-recorded BJS jail
  count.
- **Bias-mechanisms memo line 25.** "4.55% incarcerated" is Rumbaut's label for institutional
  residence.

## Deferred, with reasons

- Ledger item N (+$1.8bn on the generation split): the ledger is fingerprinted, so the one-step
  reallocation waits for its next rebuild.
- ADJINC is omitted in four ACS scripts: 1.5–2% on dollar levels only; group ratios are unaffected.
- ACS earnings allocation (Mexico-born/white ratio 0.572 → 0.589): affects ACS cross-checks only.
- School allocation in the ACS: the generation split's K–12 charge is about $0.5bn low.
- Not checked: census QHISPAN (no held extract carries it), ACS housing and commute item flags, the
  cause of the 2020 schooling break, whole-person imputation rates for correctional GQ.

## Proposal (the operator adopts)

1. **Adopt now:** rows 1, 3, 6, 7 and 8 together move the main case by about **−$5bn** (−14.2,
   +9.5, −3.5, +1.1, +2.0), to about $198–245bn.
2. **Measure, then adopt:** rows 2, 4 and 5, one measurement each (above). Until then the main case
   carries them as a band of −$23bn to +$7bn beside the measured five: rows 2, 4, 5, 9, 10 and the
   small items.

## Files

- Scripts: `cps_*.py`, `acs_*.py`, `spending_*.py`, `crime_*.py`, `synthesis.py`.
- Outputs: `derived/*.csv|json`.
- Ignored `_cache/`: slim ACS parquet extracts and the Treasury statement pages.

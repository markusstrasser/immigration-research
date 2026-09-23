**Verdict:** The Mexican-origin union draws **7.4% of Medicaid long-term care dollars**, well
below the 12.25% the complete account charges it through the MEPS community key. By category, in
calendar 2023:
- nursing facilities 5.0%;
- ICF/IID 3.4%;
- mental-health facilities 5.1% (all institutional care 4.8%);
- home and community-based services 8.7%. That is 6.3% of the HCBS that CMS's T-MSIS files
  record, plus 27% of California's In-Home Supportive Services, which those files omit.

The underlying Hispanic shares come from CMS's own tables and hold steady from 2019 to 2023:
9.7% of nursing-facility dollars, 6.1% of ICF/IID and 15.4% of HCBS. Charging the $264.7bn of LTSS
(2024 scale) at the union's shares, and the rest of the line on the MEPS key without home health,
moves the main case by:

| | Low | Central | High |
|---|---:|---:|---:|
| Effect, $bn a year | −12.5 | **−11.1** | −8.1 |
| Main case, $bn a year ($203.2–249.6bn now) | 190.7–237.1 | **192.1–238.5** | 195.1–241.5 |

The low and high columns are the extremes of 960 combinations of specification choices. The
audit's bound of −3.6 to −15 contains the result; its midpoint was −9.3.

**Combining rule.** The medical-ethnicity lane's ratios apply only to the community remainder of the
line ($689.5bn). This lane's shares apply only to the LTSS dollars. Adopted together, the five
medical lines change by **−$17.7bn** at that lane's p99.5 specification, and the main case becomes
$185.5–232.0bn. Across its seven specifications the joint change runs from −8.7 to −21.1; the plain
specification gives −13.2. The p99.5 figure breaks down as:
- −3.0: that lane's published five-line change;
- −11.1: this carve-out;
- −3.6: that lane's 1.117 Medicaid ratio no longer applies to LTSS dollars.

That lane's nursing-facility bound (over-charge $4.0–6.2bn) and its combined −8.0 / −10.2 are
replaced by these figures, not added to them.

[CALCULATION: `translate.py`, `main_case_effect.js` → `derived/summary.json`, `derived/effects.csv`,
`derived/combined.csv`, `derived/main_case_effect.csv`; all gates pass]

Model: claude-opus-5-5[1m]. Date: 2026-09-23. Brief: [BRIEF.md](BRIEF.md). Audit row settled:
[`dataset_integrity_2026_09_23/README.md`](../dataset_integrity_2026_09_23/README.md) row 5,
[`spending.md`](../dataset_integrity_2026_09_23/spending.md) #3.

## Sources, graded by evidence level

A = administrative and primary. B = survey data or a published analysis of administrative data.
C = proxy or modelled.

| Source | What it gives | Hispanic or Mexican | Users or dollars | Used for | Grade |
|---|---|---|---|---|---|
| CMS / Mathematica, *Medicaid LTSS Annual Expenditures and Users*, TAF workbooks C1 (users) and C2 (expenditures), CY2019–2023 (Stepanczuk, Murray, Carpenter, Larsen, Wysocki; CY2023 release 17 Oct 2025) | LTSS by category × race/ethnicity × state; national by age | Hispanic, any race | both | every share | A |
| CMS / Mathematica, *Characteristics of People Using Medicaid LTSS, 2023* (Carpenter, Stepanczuk, Wysocki, 17 Oct 2025) | ethnicity method: self-report, with probabilities from the TAF Race and Ethnicity Imputation file when missing (p. 10); HCBS users 20.9% Hispanic (p. 2); institutional 10.0% (p. 6) | Hispanic | users | method, checks | A |
| CMS-64 Financial Management Report, FFY2023 and FFY2024 (`MAP - California`, `MAP - National Totals`) | California personal care $6.50/7.10bn, Community First Choice $11.33/13.78bn, self-directed $0.20/0.25bn | none | dollars | IHSS dollars | A |
| BEA NIPA Table 3.12, lines 33+34 (pinned workbook) | Medicaid and other medical care: $891.587bn (2023), $954.200bn (2024) | none | dollars | 2023→2024 scale | A |
| CMS / Mathematica, *Medicaid LTSS Annual Expenditures Report: FFY2020*, Appendix D table D.2 (Murray, Eckstein, Lipson, Wysocki, June 2023) | CMS-64-based LTSS by state | none | dollars | completeness test | B |
| CHCF / ATI Advisory, *Who Receives Medi-Cal Home and Community-Based Services?* (Oct 2025), from the DHCS LTSS dashboard | Latino 31%, unknown 7% of recipients in five Medi-Cal HCBS programs, 2022 (p. 2 Fig. 3); IHSS is 92% of their enrollment (p. 1) | Latino | users | IHSS share | B |
| Cohen, Dick, Estrada, Stone, *Medical Care* 2026 (MDS 3.0 + MBSF 2011–2022, 19.5m residents; abstract) | Hispanic nursing-home residents 3.92% on MDS self-report, 6.12% after adding the MBSF RTI race code | Hispanic | residents | test of the 3.2% | B |
| ACS 2024 1-year PUMS (own extract; identical to the audit's slim file on shared columns) | union (HISP 02 or Mexico-born) per Hispanic, by state, in LTSS proxy populations | Mexican and Mexico-born | persons | Hispanic→union | B (proxies: C) |
| MEPS 2024 HC-256 | Medicaid home health $53.8bn; the account's key with and without it | via age × nativity transport | dollars | remainder key | B |
| LAO, *The 2026-27 Budget: In-Home Supportive Services* (18 Mar 2026) | 2024-25 state share of nonfederal IHSS $10.3bn (82%); effective federal rate 54% | none | dollars | scale cross-check only | B |

Every number used in a calculation was parsed from the primary workbook or PDF by a script, or,
for CHCF and LAO, read from the PDF text (`pdftotext`). None comes from a search summary.

The following were not reached within the source-search budget:
- LTCFocus;
- the MDS 3.0 frequency report and the Nursing Home Data Compendium;
- MACPAC and KFF tabulations of LTSS by race.

The resident-share question they would answer is covered by Cohen et al. and the ACS, which agree
(below). The CMS TAF tables are the primary source such tabulations draw on. MCBS was not used: its
Cost Supplement PUF excludes facility residents (medical-ethnicity lane §7).

## Gates

All pass. [CALCULATION: `gate.py` → `derived/gate.json`; `meps_hh_key.py`; `main_case_effect.js`]

1. **The account's charge.** The union gets $116.91bn of the $954.2bn Medicaid line. That is its
   key share of the household pool (12.376%) times the pool fraction (0.99005): 12.2525% of the
   line.
2. **The audit's bound reproduces** at its stated 12.3% charge. The least case is −3.57: $83bn
   institutional at a true share of 8%, with no HCBS missed. The most is −14.74: $87bn plus 70% of
   $129.4bn HCBS at 4%. At the exact 12.2525% rate the bound is −3.53 / −14.66.
3. **The medical-ethnicity lane's nursing-facility bound reproduces from that lane's own input
   cells.** Its ceiling is 43,447 / 1,356,205 = 3.2036%. It charges $8.430bn and supports
   $2.204bn / $4.408bn by use.
4. **The Medicaid key rebuilds exactly**: 0.1237563 from MEPS 2024 cell means on the CPS civilian
   population.
5. **The adopted main case reproduces** through the explorer's evaluator: $203.21–249.64bn. The
   Medicaid line moves it one for one (−11.092 at both ends). The medical-ethnicity lane's five
   lines also move it one for one: its p99.5 change gives −3.003.

## What CMS's tables show, and the translation to the union

**Hispanic shares, CMS TAF, by year** [DATA: `derived/taf_race_ethn.csv`]:

| Dollars | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|
| Nursing facilities | 9.3% | 9.2% | 9.4% | 9.1% | 9.7% |
| ICF/IID | 6.4% | 6.1% | 6.3% | 6.4% | 6.1% |
| Mental-health facilities | 14.3% | 14.0% | 16.3% | 13.2% | 11.8% |
| HCBS (as recorded) | 15.1% | 14.5% | 15.0% | 14.9% | 15.4% |

Users run higher than dollars for HCBS (20.9% in 2023) because Hispanic users draw $12.8k each
against $17.3k for all users. 2021 omits Alabama ("not calculated").

**From Hispanic to the union.**
- Each state's Hispanic dollars are multiplied by the union-per-Hispanic ratio in an ACS 2024 proxy
  population. The union here is HISP 02 or born in Mexico.
- The ratio is shrunk toward the state's broad-population ratio when the state has few Hispanic
  records (weight 50 records).
- State detail matters because 47% of Hispanic HCBS dollars are in New York, Florida, Pennsylvania,
  New Jersey and Massachusetts. Their Hispanic users are mostly Puerto Rican, Dominican or Cuban:
  the ratio is 0.04–0.06 in New York and 0.06 in Florida, against 0.82 in California and 0.88 in
  Texas.

[CALCULATION: `acs_factors.py` → `derived/acs_state_factors_2024.csv`; `translate.py`]

| Proxy population, ACS 2024 | Persons | Hispanic | Union | Union per Hispanic | Used for |
|---|---:|---:|---:|---:|---|
| Institutional group quarters, 65+ | 1.43m | 6.47% (SE 0.13) | 3.04% (0.10) | 0.469 | nursing facilities (72% of their dollars are 65+) |
| same, reporting Medicaid | 0.83m | 7.98% (0.19) | 3.59% (0.12) | 0.450 | check |
| Community, on Medicaid, self-care or independent-living difficulty | 7.92m | 19.2% (0.2) | 10.0% (0.17) | 0.523 | HCBS; the under-65 part (0.556) for nursing facilities' other 28% |
| Community, on Medicaid, under 65, cognitive difficulty | 6.86m | 19.8% | 11.0% | 0.555 | ICF/IID |
| All residents | 340.1m | 20.0% | 11.6% | 0.580 | mental-health facilities (68% of dollars under 21) |

The SEs come from 80 replicate weights. Group-quarters SEs run about √2 too small, because half of
those records are donor copies (audit `acs.md` F1).

The TAF Hispanic share of HCBS users (20.9%) agrees with the ACS Hispanic share of the HCBS proxy
(19.2%). So the imputed ethnicity in TAF shows no sign of under-counting Hispanics among HCBS users.

**Union shares, TAF only, by year** [DATA: `derived/shares_by_year.csv`]:

| | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|
| Nursing facilities | 4.60% | 4.71% | 4.65% | 4.56% | 5.02% |
| ICF/IID | 3.69% | 3.36% | 3.52% | 3.57% | 3.45% |
| HCBS, as recorded (without IHSS) | 6.18% | 5.84% | 6.29% | 6.21% | 6.30% |

2023 is the highest nursing-facility year, so using it leans against the group's side of the
correction.

## Nursing facilities: the 3.2% ceiling tested

The medical-ethnicity lane charges nursing-facility Medicaid at the union's share of institutional
residents aged 65+: 3.20%, called a ceiling, or 6.41% doubled for residents under 65.

- **The denominator is right for residents.**
  - Including the other foreign-born residents that lane left out, the union is 2.98% of 65+
    institutional residents (PUMS, RELSHIPP 37).
  - The ACS Hispanic share of those residents (6.47%) matches MDS plus MBSF (6.12%, Cohen et al.
    2026).
  - The MDS self-report alone gives 3.92%, so MDS-only counts under-state Hispanic residents.
- **A resident share is not a ceiling on Medicaid dollars.**
  - Among residents who report Medicaid, the union is 3.59%.
  - CMS's Medicaid nursing-facility dollars are 9.71% Hispanic, against 6.47% of residents.
  - 28% of those dollars go to users under 65.
  - California holds 42% of Hispanic nursing-facility dollars, and its Hispanic residents are
    mostly Mexican-origin.
  - Translated, the union's dollar share is **5.0%**: 4.6–5.0% across 2019–2023 and 3.6–5.7%
    across the factor variants.
- **That lane's dollar range survives.**
  - Its use-based charge was $2.2–4.4bn; the measured charge is $3.46bn (2023 dollars).
  - Its over-charge range was $4.0–6.2bn; the measured over-charge is $4.97bn, or $5.33bn at the
    2024 scale.
  - The ceiling label is what fails: the measured share sits between its ceiling and its doubled
    share.

[CALCULATION: `acs_factors.py`, `translate.py`; SOURCE: Cohen et al. 2026 abstract, PubMed 42258359]

## HCBS, ICF/IID and mental-health facilities

- **HCBS: TAF omits California's IHSS in every year.**
  - California's personal-care, Community First Choice and 1915(j) lines are $0.00–0.01bn in TAF
    from 2019 to 2023, and CMS rates California's HCBS data "High Concern".
  - The CMS-64 FMR puts those lines at $18.02bn in FFY2023 and $21.04bn in FFY2024, which gives
    $18.78bn for calendar 2023.
  - LAO's IHSS figures imply about $27bn of total program cost in state FY2024-25 ($10.3bn is
    82% of the nonfederal share, and the nonfederal share is 46%), including administration and
    the state-only residual. That is consistent in scale. [INFERENCE]
  - IHSS enters at the Latino share of recipients (31%, or 33.3% with unknowns spread) times
    California's ratio (0.816): 27.2% to the union.
  - Without IHSS, HCBS would be 6.3% union and the effect −14.0. IHSS raises the union's HCBS share
    because California's recipients are a third Latino.

  [DATA: `derived/fmr_ltss_lines.csv`; SOURCE: CHCF p. 2; LAO 2026-27 IHSS pp. 1–10]
- **The rest of HCBS** has a union share of 6.3% in TAF. The age mix does not move it. TAF's
  under-65 share of HCBS dollars (67.9%) equals the under-65 share of the ACS proxy (68%), and the
  age-weighted ratio gives the same 8.68% overall.
- **ICF/IID**: 6.1% Hispanic, translated to 3.4% union ($0.39bn of $11.39bn at the 2024 scale).
  The ratio for Medicaid-covered people under 65 with a cognitive difficulty (0.555) and the
  all-ages ratio (0.580) give the same result.
- **Mental-health facilities**: 11.8% Hispanic, 5.1% union. Most of these dollars are psychiatric
  care for people under 21, so the all-ages ratio is used.
- **Completeness test.**
  - Each state's 2023 dollars were re-weighted by its FFY2020 ratio of CMS-64 to TAF spending, with
    California's HCBS held out because IHSS is added directly.
  - The union share falls to 0.90 of its value for institutional care and 0.98 for HCBS. Florida's
    institutional care, which TAF under-records threefold, is mostly Cuban.
  - So incomplete TAF data do not hide union dollars.
  - Texas is not in the FFY2020 report and cannot be checked this way.

  [CALCULATION: `completeness.py` → `derived/completeness_share_test.json`]

## Translation to the main case

The table uses CY2023 shares on 2024 dollars, carried at BEA's Medicaid growth
(954.200 / 891.587 = 1.0702). Figures are $bn a year. [DATA: `derived/summary.json`, `derived/effects.csv`]

| Category | Dollars 2024 | Union share | Union $ | Charged now at 12.25% | Change |
|---|---:|---:|---:|---:|---:|
| Nursing facilities | 73.66 | 5.02% | 3.70 | 9.03 | −5.33 |
| ICF/IID | 11.39 | 3.45% | 0.39 | 1.40 | −1.00 |
| Mental-health facilities | 3.44 | 5.06% | 0.17 | 0.42 | −0.25 |
| HCBS in TAF | 156.16 | 6.30% | 9.84 | 19.13 | |
| California IHSS | 20.10 | 27.2% | 5.46 | 2.46 | |
| HCBS total | 176.25 | 8.68% | 15.30 | 21.60 | −6.30 |
| Remainder of the line: key 0.12636 without home health, against 0.12376 | 689.46 | | | | +1.78 |
| **Total** | **264.74 LTSS** | **7.39%** | **19.57** | **32.44** | **−11.09** |

The remainder row matters because MEPS records $53.8bn of Medicaid home health, which is part of
HCBS. The union holds 10.9% of those dollars under the age × nativity transport. Once HCBS is
carved out, the rest of the line is keyed without them, which raises the union's key.

The brief described a narrower method: carve out only the HCBS that MEPS misses and keep the key
unchanged. It gives −10.95, so the choice does not matter.

**One-at-a-time sensitivities** on the central −11.09, in $bn:
- Nursing facilities:
  - only the 65+ institutional ratio: −11.22;
  - "Other Hispanic" excess spread (audit F4): −10.63;
  - all-65+ ratio: −11.01;
  - ACS Medicaid users instead of TAF: −12.15.
- HCBS: all-ages ratio −10.33; age-weighted −11.09.
- IHSS at 31% Latino: −11.47.
- Union scaled up to the CPS size (+4.8%): −10.16.
- 2023 dollars, no growth: −10.20.
- Diagnostics:
  - national ratios with no state detail: −10.39;
  - without IHSS: −14.04 (known to be wrong).

The full grid crosses five nursing-facility, three HCBS, two ICF/IID, two mental-health facility,
two IHSS and two union choices with the growth and remainder-key options: 960 cells, minimum −12.54,
median −10.24, maximum −8.13.

[FRAMING-SENSITIVE] Charging LTSS by use follows the operator's 2026-09-23 decision to charge
justice and uncompensated care by use. On an equal-cost-per-person convention the community key
would stand, but the account does not use that convention for any keyed benefit.

## Combining with the medical-ethnicity lane

That lane scales the whole Medicaid line by its cell-weighted ratio f (1.117 at p99.5). Once LTSS
is carved out, f applies only to the remainder:

`joint = (its five-line change) + (this lane's change) + (f − 1) × 0.99005 × (689.46 × 0.12636 − 954.2 × 0.12376)`

[DATA: `derived/combined.csv`, `derived/main_case_effect.csv`]

| That lane's spec | f | Its five-line change | Joint change | Main case |
|---|---:|---:|---:|---|
| p99.5 (its headline) | 1.117 | −3.00 (SE 8.0) | **−17.67** | 185.5–232.0 |
| plain | 1.172 | +3.18 (SE 17.7) | −13.18 | 190.0–236.5 |
| p99.9 | 1.104 | −3.11 | −17.39 | 185.8–232.2 |
| two-part | 1.150 | −5.39 | −21.09 | 182.1–228.6 |
| excl. 2020–21 | 1.182 | +8.02 | −8.65 | 194.6–241.0 |
| CPI all items | 1.164 | +2.19 | −13.94 | 189.3–235.7 |
| year-normalized | 1.155 | +0.98 | −14.85 | 188.4–234.8 |

The uncertainty on the joint figure is that lane's sampling error (SE about 8 at p99.5). This lane
adds specification spread (the grid above) but little sampling error: the TAF figures are
administrative, and the translation ratios carry 1–2% relative SEs.

For the audit's synthesis, replacing row 5's midpoint (−9.3) with −11.1 moves its net central from
−13.5 to about −15.3. [CALCULATION: arithmetic on `dataset_integrity_2026_09_23/derived/synthesis_net.csv`]

## Disconfirmation: what would make the share higher

Each item below was checked or bounded.

- **Ethnicity under-recorded in TAF.**
  - MDS self-report under-counts Hispanic residents by a third.
  - TAF uses self-report and imputes only where it is missing, so a mis-reported ethnicity stays.
  - Against that, TAF's Hispanic share of nursing-facility users (9.5%) exceeds the ACS share among
    Medicaid-covered residents (8.0%), and its HCBS share (20.9%) exceeds the ACS proxy (19.2%).
  - A 20% under-count of Hispanic nursing-facility dollars would move the effect by +0.7.
- **Texas is under-recorded** (managed LTSS, "Medium Concern", not checkable against the FFY2020
  report). A 30% shortfall in Texas HCBS, at Texas's union share (42%), would move the effect by
  about +0.7.
- **Latino IHSS recipients draw more hours than others.** Each 5 points of dollar share above the
  recipient share moves the effect by +0.8.
- **Other California HCBS missing from TAF**: 1915(i) at $1.1–1.5bn and rehabilitation at $0.8bn.
  At California's union share this moves the effect by about +0.2.
- **The union is larger than the ACS approximation.** Scaling to the CPS union moves the effect to
  −10.2. It is included in the grid, but it overstates the gap for an elderly and disabled
  population.
- **Generic "Other Hispanic" coding in ACS group quarters.** Spreading it moves the effect to −10.6.
  It is included in the grid.

**What would make the share lower, or the effect larger:**
- LTSS grew faster than total Medicaid in 2024 (FMR fee-for-service 1915(c) +15%).
- Managed-LTSS capitation exceeds the encounter payments TAF records, by about −0.3.
- Nursing facilities measured on the ACS Medicaid users give −12.1.
- Earlier years' lower nursing-facility shares.

No plausible combination brings the effect to zero. The union would need an 11.6% share of all
LTSS dollars, against 7.4% measured and 4.8% for institutional care. [INFERENCE]

## Limits

- **Years and data vintages.** Shares are for CY2023 and are applied to 2024 dollars. The ACS
  ratios are from 2024 and are held fixed across the 2019–2023 series.
- **California IHSS.** Its share comes from recipient counts, not dollars, from 2022 data and from
  a published dashboard analysis rather than microdata.
- **The union is approximated in the ACS** as HISP 02 or born in Mexico. It misses second-generation
  members who report neither.
- **The joint figure uses the medical-ethnicity lane's f**, which was estimated on MEPS Medicaid
  including home health. Its value for the non-home-health remainder is not recomputed here.
- **Mental-health DSH** ($2.9–3.7bn in the FMR) is left on the community key. It is institution-level
  and not attributable to people. Keying it by use would move the effect by about −0.2.
- **Instrument.** This analysis was run by an LLM (`notes/llm-bias-caveat.md`). Checks were run in
  both directions:
  - IHSS raised the group's charge by $3.0bn against the TAF-only reading;
  - the nursing-facility test found that lane's ceiling too low;
  - the Texas, IHSS-hours, other-California-HCBS and union-size channels, which run against the
    group, were bounded rather than dropped.

## Reproduction

From the repo root; the ACS extract takes about two minutes:

```sh
L=infra/immigration-fiscal/ltss_share_2026_09_23; export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 $L/fetch_sources.py            # Wayback bytes, hash-pinned in SOURCE_PINS.json
uv run --no-project --with openpyxl python3 $L/taf_tables.py
uv run --no-project python3 $L/acs_extract_ltss.py         # -> _cache/ (ignored)
uv run --no-project python3 $L/acs_factors.py
uv run --no-project --with openpyxl python3 $L/fmr.py
uv run --no-project python3 $L/meps_hh_key.py
uv run --no-project python3 $L/gate.py
uv run --no-project --with openpyxl python3 $L/completeness.py
uv run --no-project --with openpyxl python3 $L/translate.py
node $L/main_case_effect.js
```

A full rerun of every script left all 17 `derived/` files and `SOURCE_PINS.json` byte-identical
(md5 before and after). The ACS extract matches the integrity audit's slim 2024 file on every
shared column, record for record.

## Files

- **Covered.**
  - TAF C1/C2 workbooks for 2019–2023: all race, age and language sheets, and the DQ sheet.
  - FMR FFY2023–24, every state `MAP` sheet.
  - The FFY2020 CMS-64 LTSS report, Appendix D table D.2.
  - ACS 2024 PUMS person files a and b.
  - MEPS 2024 HC-256.
  - BEA T3.12.
  - CHCF brief; LAO IHSS report; Cohen et al. abstract.
  - Read-only derived outputs of `full_account_spending_2026_09_20`, `main_case_2026_09_23`,
    `medical_ethnicity_pooled_2026_09_23` (`bounds.csv`, `translation_account.csv`) and
    `institutional_bound_2026_09_17` (`acs_cells.csv`).
- **Skipped.**
  - LTCFocus, the MDS frequency reports and MACPAC/KFF: source-search budget; resident shares are
    covered by Cohen et al. and the ACS.
  - MCBS: its PUF excludes facility residents.
  - ACS 2017–2023 slim files: the TAF years give the time series, and 2021–2023 ACS group-quarters
    ethnicity coding is broken (audit F4).
  - TAF A/B workbooks (delivery system, rebalancing): not needed for shares.
  - FFY2020 Appendix E state detail: used only for California.
- **Scripts**: `fetch_sources.py`, `taf_tables.py`, `acs_extract_ltss.py`, `acs_factors.py`,
  `fmr.py`, `meps_hh_key.py`, `gate.py`, `completeness.py`, `translate.py`, `main_case_effect.js`.
- **Outputs**: `derived/*.csv|json`.
- **Ignored `_cache/`**: the ACS extract, Wayback copies of the CMS files, the CHCF and LAO PDFs.

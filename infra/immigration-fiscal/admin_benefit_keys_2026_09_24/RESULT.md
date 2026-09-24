**Verdict:** Administrative records do not support fear-driven under-reporting where the group's benefit dollars are largest. The CPS does not under-report Hispanic SNAP receipt or Medicaid coverage, and it over-reports Hispanic housing assistance. Hispanic receipt is under-reported for unemployment insurance (relative reporting rate ρ 0.71–0.80, in line with the linked-record literature's 0.72–0.77) and WIC (ρ 0.77–0.84), and the CPS places too few TANF dollars in California (27% of the CPS's TANF-type dollars against 48% of administrative basic assistance). Re-keying SNAP, WIC, TANF and UI on administrative state dollars and validated state ethnicity raises the union's charged transfers by $2.2bn a year (CPS replicate SE $1.1bn). The survey keys therefore make the account slightly too favourable to the group: the proposed main case is $205.5–251.8bn instead of the adopted $203.2–249.6bn. I am moderately sure of the direction, because every package except route A is positive and route A comes out at zero. I am not sure of the size: it runs from $0.4bn to $6.3bn across the bounds on unknown ethnicity. SNAP is the least settled programme, because the QC file miscodes Hispanic participants in 25 states that hold 39% of SNAP dollars.

Lane `admin_benefit_keys_2026_09_24`, 2026-09-24. This lane adopts nothing. Every figure below is a proposed change.

## Proposed change

The adopted main case (profile `cbo_category_lag_non_school_full`) is $203.207–249.640bn [DATA: `main_case_2026_09_23/derived/main_case_bands.csv`]. Its low end uses the shared allocation and its high end the personal allocation. Changes are in $bn a year of cost to other US residents; a positive change means the account under-charges the group. The band is recomputed with the explorer engine, copying the adopted-band logic of `main_case.js` (justice and uncompensated care added). The gate reproduces all three published profiles to 1e-4 [CALCULATION: `translate.js` → `derived/main_case_translation.csv`].

| Package | Change, low / high end | Main case | Read as |
|---|---|---|---|
| **central** (validated administrative state keys, dollar weights) | **+2.27 / +2.17** | **$205.5–251.8bn** | proposed |
| route A (the five states where Hispanic ≈ Mexican; ρ applied to the union) | +0.01 / −0.04 | $203.2–249.6bn | lower bound among routes |
| route B (national administrative share, all states) | +0.26 / +0.21 | $203.5–249.8bn | SNAP input unusable (see SNAP) |
| route B over the states passing the screen | +1.29 / +1.27 | $204.5–250.9bn | |
| strict screen (three-quarters of the ACS share instead of half) | +3.49 / +3.39 | $206.7–253.0bn | |
| central, Arizona treated as failing for SNAP | +3.15 / +3.05 | $206.4–252.7bn | |
| central, unknown ethnicity all non-Hispanic | +0.46 / +0.37 | $203.7–250.0bn | bound |
| central, unknown ethnicity all Hispanic | +6.30 / +6.17 | $209.5–255.8bn | bound |

The full list of 16 packages is under Results [CALCULATION: `compare.py` → `derived/line_deltas.json`, `derived/package_se.csv`; `translate.js`].

**Against the proposed audit package** ($202.9–251.1bn, `dataset_integrity_2026_09_23/synthesis.py`):

- The central change is +$1.8 to +2.3bn, which puts the package at about $205–253bn.
- Simple addition gives $205.2–253.3bn [CALCULATION: 202.9 + 2.27; 251.1 + 2.17]. `synthesis.py` itself adds its rows.
- The lines re-keyed here are SNAP, the WIC-food part of BEA line 39, the TANF part of lines 35+37, UI and housing. They do not overlap audit rows 1 and 5–9. Row 10 re-keys only the non-WIC part of line 39.
- One overlap remains. Row 13's fill-in correction sits inside the audit's tax block and re-imputes the same CPS benefit keys: SNAP +2.9%, WIC +3.9% and cash −2.5% under the union-matched hot deck; SNAP −2.6% under the matched-over-pooled method [DATA: `cps_imputation_keys_2026_09_23/RESULT.md`, benefit-key table]. This lane compares administrative data with the published keys, so the overlap is at most about $0.4bn [CALCULATION: 0.029 × 14.28 + 0.039 × 1.15 − 0.025 × 4.04 = 0.36]. The audit's central averages the union-matched method with the matched-over-pooled method, which shrinks the overlap further.
- Audit row 12 re-keys income-security consumption with a public-assistance key and stays beside the net. This lane's income-security variant (+$10.0–10.6bn) is the same key choice, so it also belongs beside the net, not in it.
- `admin_transfer_checks_2026_09_19` scaled programme totals. This lane changes only the split of each BEA total, so the two do not overlap.

## Programme by programme

ρ is the survey's reporting rate for Hispanic receipt relative to other receipt: ρ = odds(survey Hispanic share) / odds(administrative Hispanic share). Values below 1 mean Hispanic receipt is under-reported. The CPS is ASEC 2025, which reports calendar-2024 receipt [DATA: CPS ASEC 2025 public-use archive, sha256 318845a2…, read by `cps_keys.py`].

| Programme | Union $bn now | Hispanic receipt under-reported? | ρ: route A · B over valid states · B | Central change $bn (SE) | Main case |
|---|---|---|---|---|---|
| SNAP | 14.28 | **no** | 1.21 (0.13) · 1.05 (0.06) · 1.34 | −0.48 (0.76) | −0.48 |
| WIC (food part of line 39) | 1.15 | yes, modest | 0.77 (0.10) · 0.84 (0.05) · 0.80 | +0.14 (0.06) | +0.14 |
| TANF (TANF part of lines 35+37) | 4.04 / 4.28 | not within states; the CPS puts too little in CA | 0.88 (0.24) · 0.75 (0.13) · 0.57 | +1.14 (0.58) | +1.21 / +1.14 |
| UI | 4.09 / 4.19 | **yes** | 0.71 (0.13) · 0.80 (0.10) · 0.75 | +1.36 (0.55) | +1.40 / +1.36 |
| Housing | 7.54 | no, over-reported | 1.62 (0.25) · 1.24 (0.11) · 1.42 | −2.45 (0.41) | 0 (response 0) |
| Medicaid coverage (test only) | 116.9 | no | 1.03 (0.05) · — · 1.21 (REI) / 1.08 (self-report) | not re-keyed | — |
| SSI | 5.30 | [BLOCKED] | — | — | — |

Sources: [CALCULATION: `compare.py` → `derived/program_keys.csv`, personal allocation; SE from 160 CPS replicates; main-case column from `translate.js`, low / high end].

### SNAP

The fear hypothesis fails. Where QC ethnicity is usable, the CPS reports as many or more Hispanic SNAP dollars as the QC records.

- **Administrative source.** SNAP QC FY2024 public-use file, benefits (FSBEN × FYWGT) split equally over participants, the same construction as the account key [SOURCE: https://snapqcdata.net/sites/default/files/2026-08/qcfy2024_csv.zip].
- **Gates** [SOURCE: FY-2024-Tech-Doc.pdf, same folder]:
  - Table II.2's weighted individuals (40,168,146) and benefits ($7,366,534 thousand) reproduce exactly;
  - 16.55% of participants lack race/ethnicity, against the report's "about 17 percent";
  - the 20 states with at least 10% unreported equal Appendix A's list [CALCULATION: `snap_qc.py`].
- **National QC ethnicity is unusable.** The codebook "recommend[s] against using RACETHi for national tabulations" (RACETHi entry, printed p. 82). The problem is worse than missing codes: some states code Hispanic participants as not Hispanic. In New Jersey, 2.4% of known participants are Hispanic (0.1% unknown), against 47% of people in SNAP households in the ACS. Among New Jersey participants who live with an undocumented member (CTZNi = 8, printed p. 79), 0% are coded Hispanic; the national figure is 77.9%. North Carolina shows 0.8% Hispanic overall and 12.9% among participants living with an undocumented member [CALCULATION: `snap_qc.py` → `derived/admin_snap_qc_validity.csv`].
- **Validity screen.** 25 states holding 38.6% of SNAP dollars fail it, including NJ, NC, PA, OH, VA, WA, OR, TX and NM [CALCULATION: `compare.py` → `derived/admin_validity.csv`].
- **Route A** uses CA, NV and AZ. TX and NM fail the screen because 64% and 66% of their participants lack ethnicity.
  - California: QC 44.0% Hispanic (13% unknown, imputed) against CPS 44.1% (SE 3.0), ρ 1.00.
  - Pooled over the three states with administrative weights: ρ 1.21 (SE 0.13).
  - Without Arizona: ρ 1.06 (0.12) [CALCULATION: `derived/share_comparisons.csv`, `program_keys.csv`].
  - In Arizona both surveys sit far above QC. For benefit dollars split over participants, the CPS shows 59.0% (SE 9.9) against QC's 33.1%. For everyone in the home, the ACS shows 47.7% against QC's 35.0%. Arizona's T-MSIS carries almost no Hispanic codes [DATA: `derived/admin_medicaid_taf.csv`]. The screen passes Arizona (known share 0.69 of the ACS share), so the central keeps it and the no-Arizona package reports the alternative.
- **Route B over the 26 valid states:** ρ 1.05 (SE 0.06).
- **Change.** Central BV −$0.48bn (SE 0.76). The specifications built on valid states run from −$2.14bn to +$0.72bn:
  - route A applies ρ 1.21 to the union's whole share: −$2.14bn (SE 1.12);
  - without Arizona: −$0.66bn;
  - B over valid states: −$0.54bn;
  - strict screen: +$0.72bn.

  The unscreened national specifications, B (−$2.83bn) and BS (−$2.54bn), are artefacts of the miscoding.
- **Unknown ethnicity.** Bounds move BV from −$1.78bn (all unknown non-Hispanic) to +$2.32bn (all unknown Hispanic).
- **Literature (route C, primary tables checked):**
  - Hispanic-to-white dollar capture is about 0.86 in Fox et al. 2017 and 1.07 in Shantz & Fox 2018.
  - Noncitizens under-report no more than natives: net under-reporting is 49% against 49% [SOURCE: https://www.census.gov/content/dam/Census/library/working-papers/2017/demo/SEHSD-WP2017-49.pdf, Table 3 p. 25, Table 4 p. 28; https://www.census.gov/content/dam/Census/library/working-papers/2018/demo/SEHSD-WP2018-30.pdf, Tables 3–4 pp. 28, 30].

### WIC

Hispanic participation is under-reported modestly, but the dollars are small.

- **Administrative sources.** Shares come from FNS WIC Participant and Program Characteristics 2022, Appendix Table B.8 (April 2022, a census of certified participants, 42.5% Hispanic across 50 states and DC) [SOURCE: https://www.fna.usda.gov/research/wic/participant-program-characteristics-2022; DATA: `derived/admin_wic_pc.csv`, 272 gates]. States are weighted by FY2024 food costs [SOURCE: https://www.fns.usda.gov/sites/default/files/resource-files/wicagencies2024ytd-9.xlsx, sheet "Food Costs"; regions add to the $4.913bn total; `admin_state_dollars.py`].
- **ρ.** Route A gives 0.77 (0.10), in all five states; the national share gives 0.80 [CALCULATION: `program_keys.csv`].
- **Change.** +$0.14bn (SE 0.06), with a range of +$0.10bn to +$0.35bn.
- **Line share.** WIC food is 22.6% of BEA line 39: $5.057bn of calendar-2024 food against $22.385bn [DATA: FNS `37wic-monthly-9.xlsx`, BEA Table 3.12 line 39 in the pinned workbook, sha256 69b5c7ae…].
- **Literature.** No linked study splits WIC by ethnicity [GAP].

### TANF

Within states, the CPS reports Hispanic TANF receipt at about the administrative rate. The account under-charges because the CPS puts too few TANF dollars in California and New York.

- **Administrative sources.** Recipient shares come from the ACF Characteristics and Financial Circumstances of TANF Recipients FY2024, Tables 10 (TANF) and 59 (SSP-MOE) [SOURCE: https://acf.gov/system/files/filefield_paths/fy2024-characteristics.xlsx, Wayback 20260807205846; DATA: `derived/admin_tanf.csv`, 1,765 gates]. States are weighted by FY2024 basic assistance from federal TANF and state MOE funds, $7.788bn in total [SOURCE: https://acf.gov/sites/default/files/documents/ofa/fy-2024-tanf-moe-financial-data.xlsx, Table B column 6.a; it equals the U.S. total and Table A.1; `admin_state_dollars.py`].
- **ρ.** Route A gives 0.88 (SE 0.24), and TANF alone without SSP-MOE gives 0.98 (0.27). The national 0.57 mixes reporting with geography.
- **Geography.**
  - California receives 48.1% of basic-assistance dollars but only 27.1% of the CPS's TANF-type dollars.
  - New York receives 19.2% against 7.8% in the CPS.
  - Texas receives 0.3% against 7.1% in the CPS.

  [CALCULATION: `admin_state_dollars.csv`, CPS state totals in `_cache/cps_state_replicates.npz`]. The geography-only specification alone gives +$0.78bn.
- **Change.** +$1.14bn (SE 0.58), with a range of +$0.08bn (route A, TANF only) to +$1.95bn (B, all cash assistance).
- **Line share.** TANF is 38.8% of lines 35+37 ($24.458bn of $63.065bn). General assistance has no administrative ethnicity; applying the TANF factor to the whole line gives +$2.94bn [DATA: BEA Table 3.12 lines 35, 37].
- **Literature.** It points the other way on amounts: Hispanic true reporters report about twice their administrative TANF amount, which puts Hispanic-to-white dollar capture near 1.6, from small cells [SOURCE: SEHSD-WP2018-30, Tables 5–6, pp. 33, 35].

### Unemployment insurance

Hispanic receipt is under-reported, and the size matches the literature.

- **Administrative sources.** Shares come from DOL ETA 203 claimant characteristics for calendar 2024: 24.9% of claimant-weeks with known ethnicity are Hispanic [SOURCE: https://oui.doleta.gov/unemploy/csv/ar203.csv; data map 4024c6.pdf table ar203]. States are weighted by 2024 state UI benefits paid, $36.15bn [SOURCE: https://oui.doleta.gov/unemploy/csv/ar5159.csv; data map table ar5159, printed p. 58, item 302 column 14 (c45); `admin_ui.py`].
- **ρ.** Route A gives 0.71 (SE 0.13), route B over valid states 0.80 (0.10) and the national share 0.75.
- **Change.** +$1.36bn (SE 0.55), with a range of +$0.44bn (geography only) to +$1.67bn (states weighted by claimant-weeks). Bounds for unknown ethnicity run from +$0.89bn to +$2.51bn.
- **Literature, secondary** (Meyer, Wu, Stadnicki & Langetieg 2023, read through the NBER w32860 review) [SOURCE: https://www.nber.org/system/files/working_papers/w32860/w32860.pdf, Table 2 p. 34 [pdf], Table 4 p. 36 [pdf]]:
  - In the 2011 CPS, Hispanic false negatives are 51.5% against 33.2% for whites.
  - Receipt in the survey against the records is 3.4% against 6.2% for Hispanics and 4.2% against 5.9% for whites.
  - Dollar capture H/W is 0.72 in the 2011 CPS and 0.77 in the 2010 SIPP [CALCULATION from those rows].
  - These values are as transcribed by the review; the primary paper was not opened.

### Housing

The CPS over-reports Hispanic housing assistance.

- **Administrative source.** HUD Picture of Subsidized Households 2024, federal spending weighted by the head's ethnicity [SOURCE: https://www.huduser.gov/portal/datasets/assthsg.html, STATE_2024 and US_2024; dictionary pp. 1–3; `admin_hud.py`, 112 gate checks].
- **ρ.** Route A gives 1.62 (0.25) and route B 1.42.
- **Change.** The union's housing dollars fall by $1.0–2.7bn, with no effect on the main case, because the line is a subsidy with response 0.
- **Screen.** It flags 27 states for housing, mostly Southern ones where assisted households are largely Black. For HUD the low shares are probably real, not coding failures [INFERENCE]. The housing BS specification (−$2.67bn) is the better housing key. Either way the main case does not move.

### Medicaid and CHIP

Tested only; the key is not re-keyed.

- **Why it is not re-keyed.** The account's medical key is MEPS spending transported by age × US birth, not self-reported receipt. An enrollment share tests only whether the CPS captures Hispanic coverage.
- **ρ for CPS-reported coverage against TAF enrollment** [DATA: `derived/admin_medicaid_taf.csv`, from DQ Atlas TAF 2023 Release 1 and the REI 2022 national file]:
  - route A (TX, CA, NM, NV) 1.03 (SE 0.05);
  - national self-reported TAF 1.08;
  - national REI 1.21.
- **No under-reporting of coverage.** This fits the literature, read secondarily: false negatives are equal for Hispanics and whites (43.7% against 42.8%), and false positives are higher (4.5% against 2.3%) [SOURCE: w32860 Table 2, p. 34 [pdf], transcribing Davern et al. 2009a; secondary].
- **Spending by ethnicity.** No administrative source publishes total Medicaid spending by ethnicity. The long-term care part is audit row 5.

### SSI and school meals

- **SSI:** [BLOCKED] SSA publishes counts of noncitizen recipients, not ethnicity; no administrative key exists.
- **School meals** (optional): not done.

## Route C: the linked-record literature

H/W is Hispanic survey-to-administrative dollar capture divided by the same capture for white non-Hispanics. It multiplies the receipt ratio by the amount ratio among true reporters; false-positive dollars are not priced. Below 1, the CPS understates the Hispanic share. This lane's ρ compares Hispanic receipt with all non-Hispanic receipt, so it should sit somewhat above an H/W wherever Black under-reporting is larger [INFERENCE]. The literature notes are in `_cache/lit/NOTES.md`. Every number below was checked against the saved PDF text.

| Programme | Study (survey, years, states) | H/W | Read from | This lane's ρ (route A · B over valid states) |
|---|---|---|---|---|
| SNAP | Fox et al. 2017 (CPS 2010–16; IL, MD, OR, VA) | 0.86 | primary: SEHSD-WP2017-49 Tables 3–4, pp. 25, 28 | 1.21 · 1.05 |
| SNAP | Shantz & Fox 2018 (CPS 2010–16; AZ, ID, MD, MI, ND, TN, VA) | 1.07 | primary: SEHSD-WP2018-30 Tables 3–4, pp. 28, 30 | (same) |
| TANF | Shantz & Fox 2018 | ≈1.6 (receipt 0.89; amounts 2.07 vs 1.17) | primary: Tables 5–6, pp. 33, 35 | 0.88 · 0.75 |
| UI | Meyer, Wu, Stadnicki & Langetieg 2023 (2011 CPS, national) | 0.72 (0.77 in the 2010 SIPP) | **secondary**: w32860 Tables 2 and 4, pdf pp. 34, 36; primary not opened | 0.71 · 0.80 |
| Medicaid coverage | Davern et al. 2009a (2002 CPS, national) | no net ratio published; FN 43.7% vs 42.8%, FP 4.5% vs 2.3% | **secondary**: w32860 Table 2, pdf p. 34 | 1.03 (coverage, route A) |
| Medicaid coverage | Noon et al. 2019 (2011 CPS) | logit FN +0.29, FP +0.83 | **secondary**: w32860 Table 3, pdf p. 35 | (same) |
| WIC, housing | none found | — | [GAP] | WIC 0.77 · 0.84; housing 1.62 · 1.24 |

[CALCULATION for the H/W column: survey/admin receipt × survey/admin amount, Hispanic over white non-Hispanic, from the cited rows; for Fox et al. the receipt ratio comes from the printed percent under-reporting, 51% against 45%.]

- **Citizenship.** Net SNAP under-reporting is the same for noncitizens and natives, 49% against 49% [SOURCE: SEHSD-WP2017-49 Table 3, p. 25]. Noncitizen householders fail to report SNAP less often than citizens: −0.155 in the Illinois ACS and −0.204 in the SIPP. Poor English raises misses in the SIPP by +0.169 [SOURCE: https://www.nber.org/system/files/working_papers/w25143/w25143.pdf, Table 2, pdf p. 38]. No study splits Mexican origin or Spanish-language interviews, and every sample predates 2016 [GAP]. This lane's own comparison uses 2024 administrative data against the CPS ASEC 2025, so it covers the post-2016 period that the literature misses.
- **Agreement with routes A and B.**
  - UI: the literature and this lane agree (0.72–0.77 against 0.71–0.80).
  - SNAP: both find no Hispanic under-reporting large enough to move the key.
  - TANF: the literature cuts against this lane's TANF term. Hispanic true reporters overstate their amounts in seven states without California, so if that held within the states here, the TANF term would shrink. The TANF term here comes from where the dollars are paid, which the literature does not address.
  - Medicaid: the literature and this lane agree that coverage is not under-reported.

## Method

1. **Positive control first.** `cps_keys.py` rebuilds the account's SNAP target share, 0.148149840, from the CPS microdata: pwwgt0 weights, the canonical union, SPM SNAP split equally over unit members. It also rebuilds all 18 published shares in `incidence_keys.csv` to a relative 1e-9 [CALCULATION: `derived/cps_keys_gate.json`; `test_admin_keys.py`].
2. **Survey shares under the administrative definitions.** Each programme gets several CPS measures: the key's dollars, persons in receiving units, heads, households, TANF-type units and recipients. Each carries a successive-difference replicate SE (160 replicates, factor 4/160) [CALCULATION: `derived/cps_keys_national.csv`, `cps_keys_state.csv`]. ACS 2024 PUMS gives a second survey and m_s, the union's share of Hispanic recipients by state (Mexican origin or Mexico-born) [DATA: `acs_pums_2024_1yr`; `acs_check.py`, population gate 340,110,990].
3. **Specifications** [`compare.py`]:

   | Spec | Construction |
   |---|---|
   | B | National administrative share; ρ applied to every Hispanic dollar |
   | A | Route-A states pooled with administrative weights; ρ applied to the union only |
   | G | Administrative state totals with CPS state shares |
   | BS | Administrative state totals and shares |
   | GA | CPS shares corrected by route A's ρ |
   | BV (central) | BS in states that pass the screen, GA in states that fail |
   | B_screened | B computed over the states that pass the screen |

   The state specifications rebuild the union share as Σ A_s [h_s m_s + (1 − h_s) n] / Σ A_s. They divide it by the same construction on the CPS and scale the key's union share by the ratio.
4. **Dollar weights.** State totals are administrative dollars wherever a source gives them: SNAP QC benefits, ETA 5159 UI paid, ACF basic assistance, WIC food costs and HUD spending. Where the comparable CPS measure counts people (WIC, TANF), the CPS side is weighted by the key's own state dollars. The first pass weighted states by people; those versions are kept (`_participants`, `_recipients`, `_claims`) and move the central by less than $0.1bn.
5. **Validity screen.** A state's administrative ethnicity fails if at least half the records lack it, or if its known Hispanic share is below half the ACS Hispanic share of the matching population. The matching population is people in SNAP households for SNAP, all persons for UI, and people below 200% of poverty for the rest. Route A uses the five states that pass. States failing, with their share of dollars: SNAP 25 (38.6%), TANF 11 (4.3%), UI 8 (2.9%), WIC 0, housing 27 (32.9%, see Housing) [CALCULATION: `derived/admin_validity.csv`].
6. **Translation.** `translate.js` shifts the preferred key of each line by the re-keyed dollars, holding national totals fixed. It recomputes the adopted band exactly as `main_case.js` does. Package SEs sum the replicate change vectors over the transfer lines [CALCULATION: `derived/package_se.csv`].

## Results: every specification computed

Taken from `derived/program_keys.csv`, personal allocation (SNAP, WIC and housing keys do not differ by allocation). Change SEs come from CPS replicates. The last column gives the main-case change at the low and high ends [CALCULATION: `compare.py`, `translate.js`]. Rows that go against the central reading are included.

| Programme | Spec | Admin Hispanic share | Survey Hispanic share | ρ (SE) | Union $bn now | Re-keyed | Change $bn (SE) | Main case low / high |
|---|---|---|---|---|---|---|---|---|
| snap | B | 0.211 | 0.264 | 1.343 (0.056) | 14.28 | 11.46 | -2.83 (0.35) | -2.83 / -2.83 |
| snap | A | 0.419 | 0.466 | 1.207 (0.129) | 14.28 | 12.14 | -2.14 (1.12) | -2.14 / -2.14 |
| snap | G | 0.211 | 0.272 |  | 14.28 | 15.23 | +0.94 (0.40) | +0.94 / +0.94 |
| snap | BS | 0.211 | 0.264 |  | 14.28 | 11.74 | -2.54 (0.50) | -2.54 / -2.54 |
| snap | GA | 0.211 | 0.264 | 1.207 (0.129) | 14.28 | 13.67 | -0.62 (0.88) | -0.62 / -0.62 |
| snap | B_screened | 0.260 | 0.270 | 1.054 (0.058) | 14.28 | 13.75 | -0.54 (0.55) | -0.54 / -0.54 |
| snap | BV | 0.254 | 0.264 | 1.207 (0.129) | 14.28 | 13.81 | -0.48 (0.76) | -0.48 / -0.48 |
| snap | B_known | 0.210 | 0.264 | 1.352 (0.057) | 14.28 | 11.40 | -2.89 (0.35) | -2.89 / -2.89 |
| snap | BS_known | 0.210 | 0.264 |  | 14.28 | 11.67 | -2.62 (0.50) | -2.62 / -2.62 |
| snap | BV_known | 0.257 | 0.264 | 1.179 (0.126) | 14.28 | 13.97 | -0.31 (0.76) | -0.31 / -0.31 |
| snap | B_low | 0.168 | 0.264 | 1.783 (0.075) | 14.28 | 9.15 | -5.13 (0.29) | -5.13 / -5.13 |
| snap | BS_low | 0.168 | 0.264 |  | 14.28 | 8.54 | -5.75 (0.37) | -5.75 / -5.75 |
| snap | BV_low | 0.233 | 0.264 | 1.448 (0.155) | 14.28 | 12.50 | -1.78 (0.70) | -1.78 / -1.78 |
| snap | B_high | 0.333 | 0.264 | 0.719 (0.030) | 14.28 | 17.94 | +3.66 (0.55) | +3.66 / +3.66 |
| snap | BS_high | 0.333 | 0.264 |  | 14.28 | 19.65 | +5.37 (0.83) | +5.37 / +5.37 |
| snap | BV_high | 0.306 | 0.264 | 0.918 (0.098) | 14.28 | 16.61 | +2.32 (0.87) | +2.32 / +2.32 |
| snap | BV_strict | 0.272 | 0.264 | 1.057 (0.124) | 14.28 | 15.01 | +0.72 (0.88) | +0.72 / +0.72 |
| snap | A_noAZ | 0.433 | 0.447 | 1.057 (0.124) | 14.28 | 13.62 | -0.66 (1.35) | -0.66 / -0.66 |
| snap | GA_noAZ | 0.211 | 0.264 | 1.057 (0.124) | 14.28 | 14.76 | +0.47 (0.97) | +0.47 / +0.47 |
| snap | BV_noAZ | 0.267 | 0.264 | 1.057 (0.124) | 14.28 | 14.69 | +0.41 (0.81) | +0.41 / +0.41 |
| snap | GA_firstpass | 0.211 | 0.264 | 1.057 (0.124) | 14.28 | 14.76 | +0.47 (0.97) | +0.47 / +0.47 |
| wic | B | 0.432 | 0.378 | 0.798 (0.046) | 1.15 | 1.31 | +0.17 (0.05) | +0.17 / +0.17 |
| wic | A | 0.731 | 0.676 | 0.769 (0.100) | 1.15 | 1.39 | +0.25 (0.13) | +0.25 / +0.25 |
| wic | G | 0.432 | 0.391 |  | 1.15 | 1.20 | +0.06 (0.04) | +0.06 / +0.06 |
| wic | BS | 0.432 | 0.378 |  | 1.15 | 1.29 | +0.14 (0.06) | +0.14 / +0.14 |
| wic | GA | 0.432 | 0.378 | 0.769 (0.100) | 1.15 | 1.34 | +0.19 (0.08) | +0.19 / +0.19 |
| wic | B_screened | 0.432 | 0.391 | 0.842 (0.049) | 1.15 | 1.27 | +0.13 (0.05) | +0.12 / +0.12 |
| wic | BV | 0.432 | 0.378 | 0.769 (0.100) | 1.15 | 1.29 | +0.14 (0.06) | +0.14 / +0.14 |
| wic | BV_strict | 0.432 | 0.378 | 0.769 (0.100) | 1.15 | 1.29 | +0.14 (0.06) | +0.14 / +0.14 |
| wic | B_keydollars | 0.432 | 0.368 | 0.764 (0.052) | 1.15 | 1.34 | +0.20 (0.06) | +0.20 / +0.20 |
| wic | BS_keydollars | 0.432 | 0.368 |  | 1.15 | 1.32 | +0.18 (0.06) | +0.18 / +0.18 |
| wic | A_keydollars | 0.731 | 0.654 | 0.695 (0.096) | 1.15 | 1.50 | +0.35 (0.15) | +0.35 / +0.35 |
| wic | BV_keydollars | 0.432 | 0.368 | 0.695 (0.096) | 1.15 | 1.32 | +0.18 (0.06) | +0.18 / +0.18 |
| wic | B_participants | 0.425 | 0.379 | 0.825 (0.046) | 1.15 | 1.29 | +0.14 (0.05) | +0.14 / +0.14 |
| wic | BS_participants | 0.425 | 0.379 |  | 1.15 | 1.25 | +0.10 (0.05) | +0.10 / +0.10 |
| wic | A_participants | 0.726 | 0.669 | 0.763 (0.099) | 1.15 | 1.40 | +0.26 (0.13) | +0.26 / +0.26 |
| wic | BV_participants | 0.425 | 0.379 | 0.763 (0.099) | 1.15 | 1.25 | +0.10 (0.05) | +0.10 / +0.10 |
| tanf | B | 0.435 | 0.306 | 0.573 (0.086) | 4.04 | 5.87 | +1.84 (0.61) | +1.89 / +1.84 |
| tanf | A | 0.588 | 0.557 | 0.879 (0.240) | 4.04 | 4.49 | +0.45 (0.99) | +0.47 / +0.45 |
| tanf | G | 0.435 | 0.369 |  | 4.04 | 4.81 | +0.78 (0.51) | +0.83 / +0.78 |
| tanf | BS | 0.435 | 0.306 |  | 4.04 | 5.18 | +1.14 (0.58) | +1.21 / +1.14 |
| tanf | GA | 0.435 | 0.306 | 0.879 (0.240) | 4.04 | 5.08 | +1.05 (0.58) | +1.11 / +1.05 |
| tanf | B_screened | 0.453 | 0.383 | 0.750 (0.130) | 4.04 | 4.94 | +0.90 (0.60) | +0.93 / +0.90 |
| tanf | BV | 0.436 | 0.306 | 0.879 (0.240) | 4.04 | 5.17 | +1.14 (0.58) | +1.21 / +1.14 |
| tanf | B_low | 0.431 | 0.306 | 0.582 (0.088) | 4.04 | 5.82 | +1.78 (0.61) | +1.84 / +1.78 |
| tanf | BS_low | 0.431 | 0.306 |  | 4.04 | 5.15 | +1.11 (0.57) | +1.18 / +1.11 |
| tanf | BV_low | 0.433 | 0.306 | 0.881 (0.241) | 4.04 | 5.15 | +1.12 (0.58) | +1.19 / +1.12 |
| tanf | B_high | 0.449 | 0.306 | 0.541 (0.082) | 4.04 | 6.08 | +2.04 (0.63) | +2.10 / +2.04 |
| tanf | BS_high | 0.449 | 0.306 |  | 4.04 | 5.28 | +1.24 (0.59) | +1.32 / +1.24 |
| tanf | BV_high | 0.446 | 0.306 | 0.877 (0.240) | 4.04 | 5.23 | +1.19 (0.59) | +1.26 / +1.19 |
| tanf | BV_strict | 0.434 | 0.306 | 0.879 (0.240) | 4.04 | 5.18 | +1.14 (0.58) | +1.21 / +1.14 |
| tanf | BV_fullline | 0.436 | 0.306 | 0.879 (0.240) | 10.40 | 13.34 | +2.94 (1.49) | +3.11 / +2.94 |
| tanf | BV_income_security_services | 0.436 | 0.306 | 0.879 (0.240) | 27.69 | 35.50 | +7.81 (3.98) | +8.28 / +7.81 |
| tanf | B_tanf_only | 0.421 | 0.306 | 0.605 (0.091) | 4.04 | 5.67 | +1.64 (0.60) | +1.69 / +1.64 |
| tanf | BS_tanf_only | 0.421 | 0.306 |  | 4.04 | 4.97 | +0.93 (0.55) | +0.99 / +0.93 |
| tanf | A_tanf_only | 0.563 | 0.557 | 0.975 (0.267) | 4.04 | 4.12 | +0.08 (0.93) | +0.09 / +0.08 |
| tanf | BV_tanf_only | 0.422 | 0.306 | 0.975 (0.267) | 4.04 | 4.96 | +0.93 (0.56) | +0.99 / +0.93 |
| tanf | B_all_paw | 0.435 | 0.299 | 0.555 (0.056) | 4.04 | 5.99 | +1.95 (0.45) | +2.01 / +1.95 |
| tanf | BS_all_paw | 0.435 | 0.299 |  | 4.04 | 5.88 | +1.84 (0.51) | +1.95 / +1.84 |
| tanf | BV_all_paw | 0.438 | 0.299 | 0.854 (0.199) | 4.04 | 5.91 | +1.88 (0.52) | +1.99 / +1.88 |
| tanf | B_recipients | 0.399 | 0.296 | 0.631 (0.090) | 4.04 | 5.52 | +1.49 (0.54) | +1.54 / +1.49 |
| tanf | BS_recipients | 0.399 | 0.296 |  | 4.04 | 4.96 | +0.92 (0.54) | +0.98 / +0.92 |
| tanf | A_recipients | 0.586 | 0.559 | 0.897 (0.239) | 4.04 | 4.41 | +0.38 (0.96) | +0.40 / +0.38 |
| tanf | BV_recipients | 0.401 | 0.296 | 0.897 (0.239) | 4.04 | 4.97 | +0.93 (0.54) | +0.99 / +0.93 |
| ui | B | 0.245 | 0.196 | 0.749 (0.092) | 4.09 | 5.12 | +1.03 (0.52) | +1.03 / +1.03 |
| ui | A | 0.426 | 0.346 | 0.712 (0.127) | 4.09 | 5.49 | +1.40 (0.84) | +1.43 / +1.40 |
| ui | G | 0.245 | 0.208 |  | 4.09 | 4.53 | +0.44 (0.22) | +0.45 / +0.44 |
| ui | BS | 0.245 | 0.196 |  | 4.09 | 5.44 | +1.35 (0.54) | +1.38 / +1.35 |
| ui | GA | 0.245 | 0.196 | 0.712 (0.127) | 4.09 | 5.65 | +1.56 (0.68) | +1.60 / +1.56 |
| ui | B_screened | 0.252 | 0.212 | 0.801 (0.099) | 4.09 | 4.87 | +0.78 (0.49) | +0.78 / +0.78 |
| ui | BV | 0.246 | 0.196 | 0.712 (0.127) | 4.09 | 5.45 | +1.36 (0.55) | +1.40 / +1.36 |
| ui | B_low | 0.224 | 0.196 | 0.844 (0.104) | 4.09 | 4.68 | +0.59 (0.48) | +0.59 / +0.59 |
| ui | BS_low | 0.224 | 0.196 |  | 4.09 | 4.96 | +0.87 (0.49) | +0.89 / +0.87 |
| ui | BV_low | 0.225 | 0.196 | 0.833 (0.148) | 4.09 | 4.98 | +0.89 (0.50) | +0.91 / +0.89 |
| ui | B_high | 0.314 | 0.196 | 0.532 (0.065) | 4.09 | 6.56 | +2.47 (0.67) | +2.45 / +2.47 |
| ui | BS_high | 0.314 | 0.196 |  | 4.09 | 6.72 | +2.63 (0.67) | +2.69 / +2.63 |
| ui | BV_high | 0.307 | 0.196 | 0.578 (0.103) | 4.09 | 6.60 | +2.51 (0.66) | +2.57 / +2.51 |
| ui | BV_strict | 0.249 | 0.196 | 0.712 (0.127) | 4.09 | 5.48 | +1.39 (0.55) | +1.42 / +1.39 |
| ui | B_cpsrecipients | 0.245 | 0.194 | 0.741 (0.060) | 4.09 | 5.17 | +1.08 (0.34) | +1.07 / +1.08 |
| ui | BS_cpsrecipients | 0.245 | 0.194 |  | 4.09 | 5.27 | +1.18 (0.42) | +1.21 / +1.18 |
| ui | A_cpsrecipients | 0.426 | 0.356 | 0.745 (0.094) | 4.09 | 5.29 | +1.20 (0.57) | +1.22 / +1.20 |
| ui | BV_cpsrecipients | 0.247 | 0.194 | 0.745 (0.094) | 4.09 | 5.29 | +1.20 (0.42) | +1.23 / +1.20 |
| ui | B_claims | 0.248 | 0.196 | 0.740 (0.091) | 4.09 | 5.17 | +1.08 (0.53) | +1.08 / +1.08 |
| ui | BS_claims | 0.248 | 0.196 |  | 4.09 | 5.74 | +1.65 (0.57) | +1.69 / +1.65 |
| ui | A_claims | 0.431 | 0.346 | 0.698 (0.125) | 4.09 | 5.59 | +1.50 (0.86) | +1.53 / +1.50 |
| ui | BV_claims | 0.249 | 0.196 | 0.698 (0.125) | 4.09 | 5.76 | +1.67 (0.58) | +1.71 / +1.67 |
| housing | B | 0.209 | 0.272 | 1.417 (0.110) | 7.54 | 5.92 | -1.62 (0.31) | +0.00 / +0.00 |
| housing | A | 0.303 | 0.413 | 1.619 (0.253) | 7.54 | 4.89 | -2.65 (0.67) | +0.00 / +0.00 |
| housing | G | 0.209 | 0.257 |  | 7.54 | 6.69 | -0.85 (0.27) | +0.00 / +0.00 |
| housing | BS | 0.209 | 0.272 |  | 7.54 | 4.87 | -2.67 (0.33) | +0.00 / +0.00 |
| housing | GA | 0.209 | 0.272 | 1.619 (0.253) | 7.54 | 4.93 | -2.61 (0.48) | +0.00 / +0.00 |
| housing | B_screened | 0.290 | 0.336 | 1.240 (0.110) | 7.54 | 6.51 | -1.03 (0.39) | +0.00 / +0.00 |
| housing | BV | 0.215 | 0.272 | 1.619 (0.253) | 7.54 | 5.09 | -2.45 (0.41) | +0.00 / +0.00 |
| housing | BV_strict | 0.224 | 0.272 | 1.458 (0.893) | 7.54 | 5.44 | -2.11 (1.52) | +0.00 / +0.00 |
| housing | B_households | 0.209 | 0.228 | 1.123 (0.074) | 7.54 | 6.97 | -0.57 (0.31) | +0.00 / +0.00 |
| housing | BS_households | 0.209 | 0.228 |  | 7.54 | 5.74 | -1.80 (0.32) | +0.00 / +0.00 |
| medicaid | B_rei | 0.275 | 0.315 | 1.209 (0.024) | 116.91 |  |  |  |
| medicaid | B_dq_self_report | 0.299 | 0.315 | 1.078 (0.021) | 116.91 |  |  |  |
| medicaid | A | 0.580 | 0.587 | 1.027 (0.055) | 116.91 |  |  |  |
| medicaid | BS | 0.299 | 0.315 |  | 116.91 |  |  |  |
| ssi | none |  |  |  | 5.30 |  |  |  |

What the suffixes mean:

| Suffix | Meaning |
|---|---|
| `_known` / `_low` / `_high` | Unknown ethnicity handled as missing at random / all non-Hispanic / all Hispanic |
| `_strict` | Screen at three-quarters of the ACS share |
| `_noAZ` | Arizona treated as failing the screen |
| `_keydollars` | CPS side taken as the key's own dollars |
| `_participants` / `_recipients` / `_claims` | States weighted by people instead of dollars |
| `_cpsrecipients` | CPS side taken as UI recipients |
| `_tanf_only` | TANF without SSP-MOE |
| `_all_paw` | CPS side taken as all cash assistance |
| `_fullline` | TANF factor applied to all of lines 35+37 |
| `_income_security_services` | The cash key's factor applied to the consumption line (audit row 12's key choice) |
| `_households` | CPS side taken as subsidized households |
| `GA_firstpass` | This lane's first-pass SNAP central (route A from CA and NV, no screen) |

The `shared` rows are in the CSV. Packages [CALCULATION: `derived/package_se.csv`, `derived/main_case_translation.csv`]:

| Package | Members | Change on transfer lines, personal $bn (SE) | Main case change low / high | Band $bn |
|---|---|---|---|---|
| central | snap_BV wic_BV tanf_BV ui_BV housing_BV | +2.17 (1.15) | +2.27 / +2.17 | 205.5–251.8 |
| route_A | snap_A wic_A tanf_A ui_A housing_A | -0.04 (1.86) | +0.01 / -0.04 | 203.2–249.6 |
| route_B | snap_B wic_B tanf_B ui_B housing_B | +0.21 (0.93) | +0.26 / +0.21 | 203.5–249.8 |
| route_B_screened | snap_B_screened wic_B_screened tanf_B_screened ui_B_screened housing_B_screened | +1.27 (1.03) | +1.29 / +1.27 | 204.5–250.9 |
| admin_state_keys_unscreened | snap_BS wic_BS tanf_BS ui_BS housing_BS | +0.09 (0.98) | +0.19 / +0.09 | 203.4–249.7 |
| geography_only | snap_G wic_G tanf_G ui_G housing_G | +2.22 (0.79) | +2.27 / +2.22 | 205.5–251.9 |
| survey_shares_route_A_rho | snap_GA wic_GA tanf_GA ui_GA housing_GA | +2.19 (1.28) | +2.29 / +2.19 | 205.5–251.8 |
| central_strict_screen | snap_BV_strict wic_BV_strict tanf_BV_strict ui_BV_strict housing_BV_strict | +3.39 (1.26) | +3.49 / +3.39 | 206.7–253.0 |
| central_snap_noAZ | snap_BV_noAZ wic_BV tanf_BV ui_BV housing_BV | +3.05 (1.22) | +3.15 / +3.05 | 206.4–252.7 |
| central_people_weights | snap_BV wic_BV_participants tanf_BV_recipients ui_BV_claims housing_BV | +2.23 (1.15) | +2.32 / +2.23 | 205.5–251.9 |
| central_tanf_only | snap_BV wic_BV tanf_BV_tanf_only ui_BV housing_BV | +1.96 (1.14) | +2.05 / +1.96 | 205.3–251.6 |
| central_tanf_full_line | snap_BV wic_BV tanf_BV_fullline ui_BV housing_BV | +3.96 (1.82) | +4.17 / +3.96 | 207.4–253.6 |
| central_plus_income_security_services | snap_BV wic_BV tanf_BV ui_BV housing_BV tanf_BV_income_security_services | +9.98 (4.71) | +10.55 / +9.98 | 213.8–259.6 |
| central_unknown_low | snap_BV_low wic_BV tanf_BV_low ui_BV_low housing_BV | +0.37 (1.09) | +0.46 / +0.37 | 203.7–250.0 |
| central_unknown_high | snap_BV_high wic_BV tanf_BV_high ui_BV_high housing_BV | +6.17 (1.29) | +6.30 / +6.17 | 209.5–255.8 |
| first_pass_central | snap_GA_firstpass wic_BS_participants tanf_BS_recipients ui_BS_claims housing_BS | +3.15 (1.32) | +3.24 / +3.15 | 206.5–252.8 |

The first pass (people weights; SNAP ρ from CA and NV without a screen) gave +$3.2bn. The screen and dollar weights lower it to +$2.2bn, mostly because SNAP moves from +$0.47bn to −$0.48bn and UI from +$1.65bn to +$1.36bn.

Other derived files and what each row holds:

| File | Rows |
|---|---|
| `share_comparisons.csv` | Administrative, CPS and ACS Hispanic shares for the US and the five route-A states, under 18 matched definitions |
| `admin_validity.csv` | One row per programme × state, with the screen's inputs and verdict |
| `admin_snap_qc_validity.csv` | One row per state, with QC Hispanic shares among participants who live with an undocumented member, noncitizen participants and all participants |
| `admin_state_dollars.csv` | TANF basic assistance and WIC food costs by state |
| `admin_*.csv`, `cps_keys_*.csv`, `acs_recipients_2024.csv` | The inputs, each described in its script's docstring |

## What would change it

- **SNAP coding.** Administrative ethnicity for the 25 states that fail the screen would settle SNAP's sign, whether it comes from state eligibility files or a Census linkage. If QC also under-codes Hispanics in states that pass (Arizona, where both surveys sit 12–25 points higher), SNAP moves to +$0.4–0.7bn and the central to about +$3.1–3.5bn (packages `central_snap_noAZ`, `central_strict_screen`).
- **Unknown ethnicity.** If the QC's, ETA 203's and ACF's unknowns are mostly Hispanic, the central rises to +$6.2bn. If they are mostly not Hispanic, it falls to +$0.4bn. The QC evidence points to the first: 39% of participants who live with an undocumented member lack ethnicity, against 16.6% of all participants [CALCULATION: `admin_snap_qc_validity.csv`]. The central imputes them within the unit, then within the state × noncitizen-in-home × child cell.
- **Dollars per recipient by ethnicity within a state.** WIC, TANF and UI shares are shares of people. If Hispanic recipients draw fewer dollars each within a state, the WIC, TANF and UI terms shrink, and they grow if the reverse holds. The linked data give some evidence:
  - UI: administrative annual amounts are equal, $8,803 for Hispanic true recipients against $8,808 for white (2011 CPS) [SOURCE: w32860 Table 4, p. 36 [pdf]].
  - TANF: administrative amounts are lower for Hispanic recipients, $1,455 against $2,196, in seven states that exclude California [SOURCE: SEHSD-WP2018-30 Table 6, p. 35]. If that gap held within the states here, the TANF term would shrink.
- **A post-2016 linked study with citizenship or Spanish-interview splits** would test fear directly. None exists in the documents read [GAP].

## Limits

- **Hispanic is not the union.** Route A uses the five states where the union is 69–85% of Hispanics: AZ 0.854, CA 0.806, TX 0.797, NV 0.717, NM 0.685 [CALCULATION: `acs_recipients_2024.csv`]. Route B assumes the union reports like other Hispanics. m_s uses Mexican origin or Mexico-born from the ACS, which has no parental birthplace.
- **Reporting versus coverage.** The comparisons capture differences in reporting and in CPS coverage together. The administrative totals count every recipient, while CPS weights are controlled to population totals.
- **Periods differ.** WIC shares are April 2022; SNAP is FY2024; TANF is FY2024; UI and HUD are 2024; the CPS reports calendar 2024.
- **Standard errors.** They cover CPS sampling only. The QC and TANF characteristics are themselves samples, with the CA, TX, NM and NV TANF shares about ±6–7 points [DATA: `_cache/wic_tanf/NOTES.md`]. m_s is held at its ACS point estimate.
- **Small state samples.** CPS samples in the route-A states other than California are small (19–289 records per programme), hence route A's SEs of 0.10–0.25 on ρ.
- **The screen is a judgment.** The half-of-ACS threshold is reported beside three-quarters. For housing the screen misfires (see Housing), which does not affect the main case.
- **Only part of each line is re-keyed.** TANF covers 38.8% of lines 35+37 and WIC 22.6% of line 39; the rest keep their keys.
- **The literature (route C)** predates 2016, covers a few states, and has no split by Mexican origin, citizenship (except Fox et al. 2017 for SNAP) or interview language. Davern 2009a, Noon 2019 and the Meyer et al. 2023 UI paper are read through the w32860 review [DATA: `_cache/lit/NOTES.md`].

## Blocked and not done

- [BLOCKED] SSI ethnicity: SSA publishes noncitizen counts only.
- [BLOCKED] Texas and New Mexico SNAP QC ethnicity: 64–66% of participants are unknown. Both states fall back to route-A-corrected CPS shares.
- [BLOCKED] Arizona T-MSIS Hispanic codes: Arizona is absent from the Medicaid route A.
- [BLOCKED] Medicaid spending by ethnicity: not published; one 2019 TAF paper is paywalled [DATA: `_cache/medicaid/NOTES.md`].
- Not done: school meals (optional), and the primary texts of Klerman et al. 2005, Davern 2009a, Noon 2019 and Meyer et al. 2023. Crawled text of Davern 2009a and Noon 2019 sits unread in `_cache/lit/`.

## Reproduce

From the repository root. Raw pulls are cached and pinned in `_cache/*/SOURCE_PINS.json`; a changed file stops the run.

```sh
L=infra/immigration-fiscal/admin_benefit_keys_2026_09_24
for s in cps_keys snap_qc admin_wic admin_tanf admin_medicaid admin_ui admin_hud admin_state_dollars acs_check compare; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl python3 $L/$s.py || break
done
node $L/translate.js
OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl --with pytest \
    python3 -m pytest $L/ -q        # 4 passed: SNAP positive control, QC Table II.2, screen, translation gate
```

About 90 seconds in total. `acs_check.py` reads 3.4 GB of ACS CSV and takes 45 seconds. Verified from these scripts on 2026-09-24: every gate passed and 4 tests passed.

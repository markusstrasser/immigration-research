# CPS ASEC integrity audit (population spine, receipts and benefit keys)

**Verdict:** The two largest CPS defects both make the account understate the cost. Both are
modelled bounds, not measured corrections.

1. **The Census tax model assumes every respondent is a resident filer who complies fully.** The
   account's keys inherit that assumption: the receipt keys (federal and state liability, capped and
   uncapped wages, self-employment, FICA workers) and the EITC+ACTC key for refundable credits.
   Applying the status lane's rules changes the main case by **+$15.2bn to +$17.0bn at a 44%
   on-books share**. The rules zero EITC for Latin-American-born people the imputation classes as
   unauthorized and scale their other taxes and wages to the on-books share. At 60% on-books the
   change is +$9.9–11.3bn; at 75% it is +$5.0–6.0bn. Taken alone, the tax-side assumption makes the
   group look better, lowering its receipts by $8.5–20.4bn. The EITC side makes it look worse,
   cutting refundable-credit spending by $3.0–4.0bn.

   The EITC side is applied only to the part of the refundable line that is not premium tax
   credits. This follows the spending audit's re-key of that line (`spending.md` #1), so the two
   files do not count the same dollars twice. Applied to the whole line instead, the result was
   +$12.1–13.3bn at 44%. The same assumption also produces the generation memo's EITC figure for the
   first generation. Of Mexico-born adults aged 25–64, 18.8% show EITC. Applying the SSN rule to
   the imputed unauthorized drops that to **10.0%**, so about half the modelled recipients could not
   legally claim it.
2. **CPS misses top incomes.** The main case spreads the $385bn gap between BEA federal income tax
   and the CPS-modelled total by CPS liability shares. That gives the target 5.73% of a gap made up
   mostly of top incomes and capital gains (`CAP_VAL` is swapped from $90,000 up). The receipts
   lane's own `federal_gap_high_agi` arm moves the target's receipts by −$9.5bn, which is
   **+$9.5bn on cost**. That arm already exists but is not the main case.

A third defect runs the other way. **CPS ASEC 2025 counts 12.23M Mexico-born. That is 11% more
than ACS 2024 households (11.0M) and 10% more than ASEC 2026 (11.1M).** California and Texas match
the ACS within 0.5%. The whole excess, +1.23M, is in the other states, about 6 replicate SEs. If the
ACS level is right, the first generation's share of the main case is overstated by **$6.0–8.3bn**.
Everything else found is under $1bn or does not reach the headline.

## Files traced

Every CPS-based number behind the adopted main case reads **one file**: CPS ASEC 2025 public use,
`infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` (sha256
`318845a2…`, 142,125 person records, income year 2024, interviews February–April 2025). The chain
runs:

- `build/analyze_cps_fiscal_2025.py`: group masks, `FEDTAX_*`, `STATETAX_*`, `FICA`, cash and SPM
  noncash transfers, 160 replicate weights.
- `gen_ledger_extension_2026_09_16/extend_ledger.py`: employer payroll (`WSAL_VAL`), sales tax
  (`SPM_RESOURCES`), property tax (`HPROP_VAL`), K–12 exposure.
- `all_age_ledger_2026_09_17` → `ledger_absolute_2026_09_17`: the generation split.
- `full_account_receipts_2026_09_20`: liability, wage, capital, consumption and FICA-worker keys over
  BEA totals.
- `full_account_spending_2026_09_20`: EITC+ACTC key and other CPS spending keys.
- `school_enrollment_2026_09_20` feeds `full_account_2026_09_20`, which feeds
  `main_case_2026_09_23` ($203.2–249.6bn).

ASEC 2026 (`ledger_asec2026_2026_09_16`) is a stability check only. ASEC 2024 is not held and not
used.

The group masks were checked in the code. Union = 40.8966M, which reproduces the ledger.

| Group | Definition | Count |
|---|---|---:|
| G1 | `PRCITSHP` 4/5 & `PENATVTY` 303 | 12.221M |
| G2 | native & either parent `PE[FM]NTVTY` 303 | 14.333M |
| G3+ | native & both parents in US-area codes {57,60,66,69,73,78} & `PRDTHSP` 1 | 14.343M |
| White reference | native & US-area parents & `PEHSPNON` 2 & `PRDTRACE` 1 (white alone) | 173.05M |

All groups are restricted to `PRPERTYP` 2 or age < 15, which excludes armed-forces adults
(0.96M). [CALCULATION: `cps_probe.py` → `derived/cps_probe.json`]

## Defect table

Effects are on the main case in $bn a year of cost to other residents: + means the published figure
understates the cost, − means it overstates it.

| # | Item | Check | Finding | Grade | Effect on repo number | Status |
|---|---|---|---|---|---|---|
| 1 | `FEDTAX_BC`, `STATETAX_A`, `WSAL_VAL`, `FICA`, `EIT_CRED`, `ACTC_CRD` as allocation keys | Tax-model documentation; re-key with status rules | The Census model "assumes all survey respondents are U.S. residents for eligibility purposes" and full compliance. 9.54M Latin-American-born people are imputed unauthorized, 4.57M of them Mexico-born in the target. Re-keyed target shares: federal liability 5.32%→5.03%; capped wages 8.98%→8.40%; EITC+ACTC 22.9%→19.8% (44% on-books) | B | **+15.2 to +17.0** (44% on-books); +9.9–11.3 (60%); +5.0–6.0 (75%). Receipts side −8.5 to −20.4 (raw looks better). EITC side −3.0 to −4.0 on the non-PTC part only (raw looks worse); on the whole line it would be −6.3 to −7.1, net +12.1–13.3 at 44% | modelled bound |
| 1b | `EIT_CRED` > 0 as "EITC use" in `immigration-mexican-origin-by-generation-2026-09-16.md` §3 | Same assumption | Mexico-born 25–64 show 18.8% (the memo's figure, reproduced exactly). With EITC zeroed for the imputed unauthorized it is 10.0%. 46.8% of modelled G1 recipients are imputed unauthorized, so the memo's "twice the white rate" (6.5%) for G1 is about half tax-model artefact [CALCULATION: `cps_eitc_rate.py`] | B | Memo claim, not a $ figure; G2 and G3+ are unaffected | measured on imputed status |
| 1c | Country-code scheme (the class of defect in 0ef9f5a) | Codes against ASEC Appendix J; weighted counts | The account reads raw ASEC codes: 57 = US, 73 = Puerto Rico, 303 = Mexico, minimum parent code 57. Counts reproduce the Census 2024 generation table within construction differences. The IPUMS 5-digit loader fixed in 0ef9f5a (`load_cps_second_gen.py`) feeds no main-case lane | none | 0 | checked |
| 2 | BEA − CPS federal income tax gap ($384.8bn) keyed by CPS liability | CPS top-income undercoverage; `CAP_VAL` swap from $90k | The target gets 5.73% of the gap, versus 5.34% under the repo's high-AGI arm | B | **+9.5** (existing `federal_gap_high_agi` arm, not in the main case). If the gap went to the target at its ~3% capital share, the effect would be larger [INFERENCE] | measured by existing arm |
| 3 | Mexico-born count (`PENATVTY` 303, `PRCITSHP` 4/5) | Against ACS 2024 PUMS households and ASEC 2026 | 12.231M (SE 0.248) against ACS 11.005M and ASEC 2026 11.109M. CA+TX 6.30 vs ACS 6.31. Other states 5.93 (SE 0.205) vs ACS 4.70 and ASEC 2026 5.09. Noncitizens 8.13 vs ACS 7.20. Mexican-origin natives agree once timing is allowed for | B | **−6.0 to −8.3**, if the ACS level is right: G1 is 33.3% of the ledger's union net (waterfall step 14), so 8.8–10.0% of $67.7–83.2bn. The per-person figure is unchanged | measured discrepancy; which instrument is right is not settled |
| 4 | Parents' birthplace (`PXFNTVTY`/`PXMNTVTY`) | Allocation rates; donor pattern | Asked of everyone, no unknown code (minimum 57), so every blank is hot-decked. Adults with no co-resident parent: allocated 5.4% (G2 and G3+) vs 2.55% (white reference). For Mexican self-ID natives, allocated fathers are Mexico 28%, US 62%, other 9.5%; reported fathers are 41/57/2.3. The donor does not match on Mexican origin | C | Union ≈ 0: about 0.13M drop to "neither" and 0.10M non-Mexican-ID natives join G2 by allocation alone. The split shifts slightly from G2 to G3+. Under $1bn | measured |
| 5 | Birthplace (`PXNATVTY`) for G1 | Flag codes | 0.31M "refused → value" (edit) and 0.068M hot-deck, together 3.1% of G1 | D | < $1bn | measured |
| 6 | Hispanic origin (`PXHSPNON`) | Allocation rates | Union 0.56%, white reference 0.68%. G3+ is defined only by self-ID, and 0.116M of it is in on an allocated origin | D | ~ −0.5 (0.116M × −$4,223) | measured |
| 7 | Year of entry (`PXINUSYR`) | Allocation rates | 23.5% of G1 changed, 20.2% hot-deck | C for other lanes | 0 on the main case. It feeds the Borjas rule (a), the CMS/OHSS coverage arms and entry-cohort cuts | measured |
| 8 | Citizenship (`PRCITFLG`) | Allocation rates | G1: 11.4% changed (4.6% hot-deck, 4.5% carried from earlier CPS months), natives 0.2% | D | 0 on the main case: G1 takes both 4 and 5. It feeds status imputation rule (b) | measured |
| 9 | Race (`PXRACE1`) | Allocation rates | Race is changed for 36% of G1, 32% of G2 and 18% of G3+, against 1.0% of the white reference. CPS has no "some other race" answer, so those Hispanic responses are edited or allocated | D | 0: the target masks do not use race, and the reference is non-Hispanic. Anything built on `PRDTRACE` for Hispanics is contaminated | measured |
| 10 | Whole-supplement imputation (`FL_665` ≠ 1) | Rates by group | Union 17.7%, white reference 17.5%, G1 18.3%: no differential | D | Owned by `cps_imputation_keys_2026_09_23` | measured |
| 11 | Earnings item imputation (`I_ERNVAL`) | Rates by group | Adults with imputed earnings: union 30.8% vs white 24.3%. Wage dollars on imputed records: 42.0% vs 35.6% | — | Owned by `cps_imputation_keys_2026_09_23` | measured |
| 12 | Top-code swap (ERN ≥ $458k, WS ≥ $90k, SE ≥ $130k) | Exposure; tax-model input | 4.9% of union wage dollars sit in swap zones against 11.1% for the white reference. The public-use tax model runs on public-use (swapped) inputs, so taxes and incomes agree | D | Employer HI above the cap on swap-zone wages is $0.53bn for the whole union, and swap error is a fraction of that: < $0.1bn | measured |
| 13 | Sentinels | Min/max of the fields used | No 9999999-type values. Negative `ERN_VAL`/`SE_VAL` are real self-employment losses (min −9,999). Negative `FEDTAX_AC`/`STATETAX_A` are refunds. The keys clip at 0 | none | 0 | measured |
| 14 | Code contradictions | Cross-field | 4 records `PENATVTY` 303 with `PRCITSHP` 1/2; 14 `PRCITSHP` 1 with non-US birthplace; no foreign-born record with `PEINUSYR` 0. `PRDTHSP` and `PEHSPNON` agree exactly | none | 0 | measured |
| 15 | Born abroad of a US parent (`PRCITSHP` 3) born in Mexico | Where they land | 0.367M: 0.317M in G2, 0.015M in G3+, 0.036M outside the union. Treating them as native follows the census definition | D | 0 | measured |
| 16 | Age top-codes | Codes | 80 = 80–84 (7.81M), 85 = 85+ (5.87M). Account bands end at 75+ and MEPS donor bins at 65+ | none | 0 | measured |
| 17 | Weights | Totals against controls | 337.69M civilian noninstitutional (0.96M armed forces in households). Hispanic 68.53M; ACS 2024 all 68.00M, households 66.76M. 132 negative replicate weight entries (SDR allows them). No zero full weights. The controls are Vintage 2024 on a blended base | D | See row 3 for composition inside the Hispanic control | measured |
| 18 | Category: who is in the union | Ethnicity by generation | 1.41M union members do not call themselves Mexican: G1 has 0.17M non-Hispanic and 0.26M other-Hispanic; G2 has 0.41M and 0.58M. The 0.66M self-ID natives with one US and one other-country parent sit in no cell | D | [FRAMING-SENSITIVE]; population lane | covered |
| 19 | Self-ID attrition in G3+ | — | Covered by `mexican_origin_population_total_2026_09_19`: floor +0.80M, central +1.8M; per-person gap narrows, aggregate unchanged to −$4.6bn | B | 0 to +4.6 | covered |
| 20 | Coverage of recent and unauthorized arrivals | — | Covered by the same lane (arm 4: 0 to +7.6%). Row 3 cuts against that lane's premise for G1 in this file year | B | See rows 3 and 19 | covered; contradiction noted |

## Evidence behind the three priced defects

### 1. The tax model's resident and full-compliance assumption

The CPS ASEC Tax Model methods say: "Another shortcoming is the lack of citizenship data … The model
assumes all survey respondents are U.S. residents for eligibility purposes." The TY2024 user notes
add "we assume full compliance; all filers who are eligible claim and receive" credits. The
public-use tax model "is run on public-use CPS ASEC person and household file" (Appendix B).
[SOURCE: `sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/tax-model-methods-2022.pdf`,
Limitations and Appendix B; `TY2024-tax-model-external-user-notes.pdf` fn. 1]

The EITC needs a work-authorized SSN. Many unauthorized workers are paid off the books; the SSA
estimate is 44% on payroll in 2010. The status lane built these corrections as a stress but did not
connect them to the complete account. [SOURCE: `status_impute_2026_09_16/RESULT.md` §4; SSA
Actuarial Note 151]

`cps_status_keys.py` rebuilds the account's person-level keys: federal 0.0532 against 0.0533
published, capped wages 0.0898 against 0.0903, uncapped wages 0.0827 against 0.0832, EITC+ACTC 0.2290
against 0.2302. It then applies the corrections to the Borjas-residual unauthorized born in Latin
America (codes 302–399 excluding Cuba). Each key's target dollars in the account are scaled by the
ratio of the corrected share to the raw share. [CALCULATION: `derived/cps_status_keys.csv`]

The refundable column applies the EITC+ACTC share change to the non-PTC part of the line only:
0.2302 × 0.99 × $108.8–128.8bn, following `spending.md` #1. The whole-line figures are given for
reference.

| On-books share | Receipts, shared / personal | Refundable, non-PTC part | Net cost change | Whole-line net |
|---|---:|---:|---:|---:|
| 0.44 | −20.38 / −19.20 | −3.38 to −4.01 | **+15.2 to +17.0** | +12.1 / +13.3 |
| 0.60 | −14.51 / −13.67 | −3.19 to −3.78 | +9.9 to +11.3 | +7.0 / +7.8 |
| 0.75 | −9.04 / −8.52 | −3.01 to −3.57 | +5.0 to +6.0 | +2.2 / +2.7 |

Limits:

- The Borjas residual over-assigns unauthorized status, and its benefit rules are correlated with
  the outcome. Limiting the correction to Latin-American births avoids the lane's India/China H-1B
  misassignment.
- The 44% share is from 2010.
- The self-employment key does not reproduce (my 2.7% share against the account's 10.7%), but that
  line moves only $0.5bn.
- The two audits combine as follows. The spending audit's PTC re-key (−$12.0 to −$14.4bn) plus this
  file's refundable-line correction (−$3.0 to −$4.0bn) share no dollars. The receipt-side change
  here is separate from both.
- Survey under-reporting of these workers' earnings would push the other way; it is not measured
  here.

### 2. Top-income undercoverage in the federal-gap allocation

CPS-modelled federal liability reaches $2,018bn of BEA's $2,403bn; the evidence-only row leaves
$384.8bn unallocated. `cbo_collective` gives the target $137.94bn, of which $22.1bn is its 5.73%
share of the gap. `federal_gap_high_agi` gives it $128.46bn.
[DATA: `full_account_receipts_2026_09_20/derived/category_allocations.csv`]

Capital gains have been collected since 2014, but `CAP_VAL` is swapped from $90,000 up. The target's
wage share is 8.3–8.8% while its capital share is only 3.1–3.7%. That makes a 5.7% share of a gap
dominated by the top implausibly high. This is a documented sensitivity already. It is listed here
because its source is the CPS instrument and the main case does not use it.

### 3. Mexico-born count: ASEC 2025 vs ACS 2024 and ASEC 2026

Sources: `cps_vs_acs.py` → `derived/cps_vs_acs_origin.csv` and `cps_vs_acs_age.csv`;
`cps_mexico_born_gap.py` → `derived/cps_mexico_born_gap.csv`; replicate SEs from
`cps_detail_checks.py` → `derived/cps_detail_checks.json`. ACS figures are PUMS households: records
whose `SERIALNO` contains GQ are dropped.

| Count, millions | ACS 2024 households | ASEC 2025 | ASEC 2026 | ASEC 2025 ÷ ACS |
|---|---:|---:|---:|---:|
| Population | 331.72 | 337.69 | 338.56 | 1.018 |
| All Hispanic | 66.76 | 68.53 | 70.06 | 1.026 |
| Mexican self-ID | 38.29 | 40.36 | 40.63 | 1.054 |
| Mexico-born, foreign-born | 11.005 | 12.231 | 11.109 | **1.111** |
| … California + Texas | 6.307 | 6.303 | 6.021 | 1.000 |
| … all other states | 4.698 | 5.928 | 5.088 | **1.262** |
| … noncitizens | 7.201 | 8.130 | 6.768 | 1.129 |
| South American | 6.590 | 6.059 | — | 0.919 |

- The Mexico-born excess shows at every age. It is largest at 0–24 (1.18–1.20) and 55–64 (1.17).
- In 2025 the CPS sample had 3,082 Mexico-born respondents outside California and Texas; in 2026 it
  had 2,710. The mean weight of all Mexico-born records, relative to all records, went from 0.913 to
  0.878.
- The CPS rakes to a national Hispanic control by age and sex, not by origin. This is consistent
  with Hispanic control mass that the survey fails to reach among recent non-Mexican arrivals (South
  American 0.92) being carried by Mexican respondents [INFERENCE]. The Census technical
  documentation warns that Vintage 2024 controls change 2024–2025 comparisons (cpsmar25 fn. 9).
- The 2025–2026 drop (−1.12M) is larger than any plausible one-year net outflow. Part of it may be
  2025–26 nonresponse among noncitizens, so ASEC 2026 is not clean truth either.
- The population lane's arm 4 assumes the CPS under-covers the unauthorized. For G1 in this file
  year the CPS is **above** the ACS, and the whole excess is among noncitizens. The unauthorized
  lane's 4.567M Mexico-born unauthorized, a CPS 2025 residual, inherits it.

## Prior generation memos: what they settled and what remains open

| Memo | Settled | What remains, and where this file adds it |
|---|---|---|
| `research/immigration-mexican-origin-by-generation-2026-09-16.md` | The G1/G2/G3+ definitions and counts on ASEC 2025 (12.2 / 14.4 / 14.4M). Reconciles with the Census 2024 generation table. Flags self-ID in G3+ as a bias toward the less assimilated [FRAMING-SENSITIVE]. Transfer under-reporting is handled in the welfare memo | Its §3 treats `EIT_CRED` as measured use. For G1 about half is tax-model artefact (row 1b: 18.8% → 10.0%). Its "17% attrition" figure is stale, as the population memo already showed |
| `research/immigration-mexican-origin-population-total-2026-09-19.md` | Union 40.97M ± 0.38M. Attrition is measured and has halved since Duncan–Trejo (floor +0.80M, central +1.8M). The ancestry item does not recover hidden people. Coverage adds 0–7.6%, and the 1/0.82 multiplier double-counts the weighting. Child parental-birthplace allocation checked (99.2% unallocated) | Its §7 records the ACS–CPS Mexico-born gap (11.59 vs 12.23M) as "not adjudicated". Row 3 localizes it: all of it is outside CA+TX (6 SE), all among noncitizens, and ASEC 2026 falls back to 11.1M. It is priced at −$6.0 to −8.3bn. This contradicts that memo's working premise that CPS under-covers the Mexico-born. Adult parental-birthplace allocation and the donor pattern are new here (row 4) |
| `research/immigration-unauthorized-population-size-2026-09-19.md` | The CPS residual is 14.90M (Mexico-born 4.567M) against 12.97M on the ACS with the same rules. Vintage 2024 already raised NIM to cover humanitarian arrivals the ACS missed. CMS-style coverage partly double-counts. The PES supports a multiplier of 1 | It notes the 1.9M CPS–ACS gap for all countries but does not price it. For the Mexico-born the gap is the same phenomenon (noncitizens 8.13 vs 7.20M), so the CPS 4.567M inherits it. The status lane's corrections were never carried into the account's keys; row 1 does that |
| `research/immigration-aggregate-and-generation-audit-2026-09-17.md` | The all-age baseline reproduces. Asks for separate fields for own, parent and grandparent birthplace, source-coded generation, unknown history and self-ID. Rejects the claim that every omission makes the gap worse | Its request for an "unknown history" field: the ASEC has no unknown parent code, because every blank is hot-decked (row 4), so unknown history is invisible on this file. The public file can only report the allocation flag, which is 5.4% of G2/G3+ adults without a co-resident parent. Its point about omissions going both ways holds here: rows 1–2 raise the cost, row 3 lowers it |
| Commit `0ef9f5a` (IPUMS-CPS loader read every parent as "Other") | A code-scheme mismatch in `load_cps_second_gen.py`, fixed by integer division | The main-case chain reads raw ASEC codes, checked against Appendix J (row 1c). No lane in the main case imports that loader |

## What prior audits covered

- **Covered by `mexican_origin_population_total_2026_09_19`:** attrition, coverage, the ancestry
  question and parental-birthplace allocation for children (99.2% unallocated; the imputed cases
  carry slightly more attrition). This audit adds the adult allocation rates and the donor pattern.
- **Covered by `ledger_underreport_2026_09_16`:** under-reporting of transfer receipt (≤ $269 per
  adult).
- **Covered by `status_impute_2026_09_16`:** the eligibility corrections, as a separate stress. The
  new step here is carrying them into the account's keys.
- **Owned by `cps_imputation_keys_2026_09_23`:** the income and benefit hot deck. Its gate
  reproduces 70 key shares.
- **Covered by the spending audit (`spending.md`):** the premium-tax-credit part of the refundable
  line.

## Not checked, and why

- **Internal-file taxes:** the internal file (higher top-codes) cannot be reached from the public
  file. Row 2 is bounded by the existing arm instead.
- **ASEC 2024 cross-check of the Mexico-born level:** the file is not held. The Census 2024
  generation table (12.10M first-generation Mexican-origin, cited by the population lane) suggests
  the CPS ran about 1M above the ACS in 2024 too [INFERENCE].
- **Replicate SEs on the rows 1 and 3 effects:** they are shifts of a point estimate. The main
  case's statistical SE is about $12bn (ladder 184).
- **Institutional population:** CPS excludes prisons and nursing homes by design. Prisons are
  charged by use in the justice lane, and nursing homes are the ledger's external item N. The scope
  is correct; this audit adds nothing there.
- **Proxy reporting:** a household respondent reports parents' birthplace and ethnicity for others.
  Proxy status is not on the public file.

Model: claude-opus-5-5[1m] (Opus 5.5, 1M context).

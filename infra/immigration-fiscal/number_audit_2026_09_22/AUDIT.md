# Number audit: objections FAQ and INDEX Core State (HEAD dc8955b)

**Verdict:** 17 numbers are wrong or out of date. None of them changes a headline sign or band. The $165–197bn, $121–160bn and $270–289bn bands, the generation gaps, the age structures, the back-cast and the education table all reproduce.
- VERIFIED 167 CSV rows. Worker C also verified about 95 older-table figures by row without writing each one out, so about 260 in total.
- MISMATCH 9
- STALE 6
- INCONSISTENT 1
- UNTRACEABLE 0

[DATA] Values were re-derived from lane CSVs, RESULT.md files and the HEAD memos. [INFERENCE] The classifications and proposed wording are mine. Read-only audit: no research file was edited and nothing was committed.

Scope is `git show HEAD:research/immigration-objections-faq-2026-09-21.md` and `git show HEAD:research/immigration-INDEX.md` lines 16–283 (Core State). Line numbers refer to those HEAD blobs. The per-number record is in `checks.csv`. `recheck.py` re-derives every MISMATCH and STALE value:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/number_audit_2026_09_22/recheck.py
```

**Applied 2026-09-22:** items 1–10 corrected in the FAQ, the INDEX, ladder 164/180 and their source memos; item 1 also fixed at the source (`elder_care_bound.py`, commit b293a18). Item 6 was already rewritten by the day's routing. The two out-of-scope notes (back-cast "Education (193)" label, high-skill screen 17 vs 19 groups) are open.

## Items that are not VERIFIED

### 1. Elder-care bound: the numerator includes Mexico-born US citizens (MISMATCH, minor)
- **Where:** FAQ:27 ("$2.3–14.9bn"), FAQ:233–234 ("14.9% of foreign-born direct-care workers and 38.5% of the less-educated foreign-born"), FAQ:237 ("$2.3–14.9bn a year, $5.8bn at the preferred coefficient") and INDEX:69–70 ("**$2.3–14.9bn a year** … ($5.8bn preferred)").
- **Source:** `infra/immigration-fiscal/mr_leads_papers_2026_09_21/elder_care_bound.py` → `derived/elder_care_bound.csv`, with inputs from `derived/acs_care_inputs.csv`.
- **Defect:** `care_mex` and `treat_mex` sum both NATIVITY codes for POBP=303. That adds 4k care workers and 162k working-age adults who were born in Mexico to US-citizen parents. The denominators `care_fb` and `treat_all` are NATIVITY=2 only, and the Butcher–Moran–Watson treatment is foreign-born.
- **Correct values:**

  | Quantity | Quoted | Correct |
  |---|---|---|
  | Share of foreign-born care workers | 14.9% | 14.5% |
  | Share of the less-educated foreign-born | 38.5% | 37.7% |
  | Bound | $2.3–14.9bn | $2.3–14.6bn (2.28–14.60) |
  | Preferred | $5.8bn | $5.6bn (5.63) |

  The "1–9% of the headline" statement still holds (1.2–8.8%).
- **Proposed FAQ:233–237:** "The Mexico-born are 14.5% of foreign-born direct-care workers and 37.7% of the less-educated foreign-born. … Priced generously, the Medicaid nursing-facility saving attributable to the Mexico-born is $2.3–14.6bn a year, $5.6bn at the preferred coefficient weighted by who staffs care: 1–9% of the headline."
- **Proposed INDEX:69–70:** "bounded at **$2.3–14.6bn a year** of Medicaid spending for the Mexico-born ($5.6bn preferred)". FAQ:27 should use the same figure. The memo's §1 and ladder 164 carry the old values; they are outside this audit's scope.

### 2. Under-65 institutional cost change (MISMATCH, rounding)
- **Where:** FAQ:195: "custody-type institutional cost falls $1.4bn".
- **Source:** `ledger_absolute_2026_09_17/derived/age_profile_components.csv`, component N, shared, expanded, bands 0–5 re-weighted to white ages.
- **Correct value:** $1.34bn, so $1.3bn. The 65+ rise of $9.21bn is right. Bands 0–5 are all under-65 institutional cost, not custody alone. The memo at `immigration-yearly-lifetime-cost-repair-2026-09-19.md:71` says "under-65" and also prints 1.4.
- **Proposed:** "under-65 institutional cost falls $1.3bn while 65+ nursing cost rises $9.2bn".

### 3. Attriter-adjusted union gap on the older ledger (STALE)
- **Where:** FAQ:98 ("narrows the union gap to −$6,864") and INDEX:201 ("attriters narrow the per-person gap to −$6,864").
- **Source:** `mexican_origin_population_total_2026_09_19/derived/arm5_fiscal_implication.csv`, central arm, Duncan–Trejo selectivity. It gives −6,864.1, but its base is −7,105.5 from `all_age_ledger_2026_09_17`, not the pinned September 19 ledger.
- **Correct value:** the same arithmetic on `ledger_absolute_2026_09_17/derived/complete_gaps.csv` (union −7,151.9, third-plus −6,194.6) gives **−$6,921**, a narrowing of $231. FAQ 5 places the figure beside September 19 numbers, so the base matters.
- **Proposed FAQ:98:** "including those who stopped identifying narrows the union gap by about $230, to −$6,921 *(routed)*".
- **Proposed INDEX:201:** "attriters narrow the per-person gap by about $230–240 (−$7,152 → −$6,921 on the September 19 ledger)".

### 4. Second-generation per-adult ledger quoted without a vintage (STALE)
- **Where:** INDEX:228: "the extended per-adult-year ledger (−$8.3k to −$8.9k second generation, …)".
- **Source:** the incarceration memo's §12 table (−8,286 to −8,901). This is the September 16 partial ledger, which the September 19 repair replaced (INDEX:210).
- **Current comparable figure:** −$7,521 per person (SE 615), same-age, from `complete_gaps.csv`. It is a different object, so the row needs a label, not a new number.
- **Proposed:** "the September 16 extended per-adult ledger (−$8.3k to −$8.9k second generation, historical; the September 19 same-age gap is −$7,521)".

### 5. ε = 3 production-term move quoted without ladder 181 (STALE)
- **Where:**
  - FAQ:256: "would lower the $165–197bn band by $9–14bn; size, not sign"
  - INDEX:50: "which would put the band near $151–188bn"
- **Source:** `production_nativity_nest_2026_09_22/derived/nest_headline.csv`. The arithmetic at ε = 3 is exact: 9.1–13.8 and 151–188.
- **Why stale:** ladder 181 was committed at 16:55, after the FAQ's last commit at 15:55. It found ε = 3 to be the weakest-grounded value. The direct low-skill estimates give a $1.5–4.7bn move: at ε = 8.7 the band becomes $160–194bn, at ε = 17.9 $163–196bn. INDEX:245 already says "$2–5bn … rather than $9–14bn", so the FAQ and INDEX:50 are behind their own table.
- **Proposed FAQ:256:** "…would lower the $165–197bn band by $9–14bn at ε = 3, or by $2–5bn at the directly estimated low-skill elasticities (8.7 and 17.9; ladder 181); ε is not adopted."
- **Proposed INDEX:50:** "…which would put the band near $151–188bn at ε = 3 or $160–196bn at the directly estimated 8.7–17.9 (ladder 181); the band is not re-run."

### 6. Production term called open after it was executed (INCONSISTENT)
- **Where:** INDEX:72–75: "**Open:** the production term ($8.8–13.3bn) assumes perfect substitution …".
- **Conflict:** INDEX:48–51 in the same section reports the sensitivity as executed (ladders 176 and 181). The number is right; the status is wrong.
- **Proposed:** "The production term's perfect-substitution assumption is now tested (ladders 176, 181; see above); a 2026 removal model with imperfect substitution implies native wage gains of $27–80bn from half of all unauthorized workers, offset by other immigrants' losses (ladder 164–167)."

### 7. Texas and California permits "every year" (MISMATCH)
- **Where:** INDEX:242: "Texas permits 2.2–2.5× California's per resident every year 2000–2024".
- **Source:** `housing_supply_ca_tx_2026_09_22/derived/state_supply.csv`.
- **Correct values:** the annual ratio runs from 1.37 (2004) to 3.66 (2009) and is below 2.2 in 2000–2006 and 2017. The period mean is 2.21 and the mean of the annual ratios is 2.46.
- **Proposed:** "Texas permits 2.2–2.5× California's per resident on average over 2000–2024 (1.4× in 2004 to 3.7× in 2009)". Ladder 180 and the memo repeat the "every year" wording.

### 8. Metro rent regression sample size (MISMATCH)
- **Where:** INDEX:242: "168-metro cross-section: +0.030 log points rent growth per point of Mexican-origin share change within state".
- **Source:** `housing_supply_ca_tx_2026_09_22/derived/metro_regressions.csv`, specification `4_share_state_fe`.
- **Correct values:** +0.0303 (SE 0.0072) on n = 152. The 16 metros that were dropped are more elastic. On all 168 metros the annualised within-state coefficient is +0.0025 a year.
- **Proposed:** "152 of 168 metros: +0.030 log points of 2015–2026 rent growth per point of Mexican-origin share change within state (+0.0025/yr on all 168)".

### 9. Settlement against ancestry instrument (MISMATCH, minor)
- **Where:** INDEX:243: "settlement instrument 2–5× larger".
- **Source:** `housing_causal_2000_2010_2026_09_22/derived/estimates.csv`.
- **Correct values:** 2.5× for values (0.290/0.116) and 5.7× for rents (0.0776/0.0136). The lane's RESULT.md line 8 has the same understatement.
- **Proposed:** "settlement instrument 2.5–5.7× larger".

### 10. Acquisition roadmap count (STALE)
- **Where:** INDEX:277: "12 verified datasets we *don't* have yet".
- **Source:** `research/immigration-dataset-register.md`.
- **Now held:** SCAAP, the Light/He/Robey Texas arrests, SPI 2016 and the USSC 2024 tables are held or built, and NIS 2003 was analysed (ladder 179). The roadmap's statuses were never updated.
- **Proposed:** "Acquisition roadmap (2026-06-24): 12 targets, several since acquired (SCAAP, Texas DPS arrests, SPI 2016, USSC, NIS); check the register first".

## Verified but worded in a way that could mislead (no class change)
- **FAQ:40, "at any common age structure −$7,049 to −$8,716":** this is the shared allocation. Under the personal allocation the range is −$6,677 to −$7,477.
- **FAQ:52, "63–66% school-spending response" listed under "What comes from CBO":** the share is the repo's arithmetic on CBO's −0.37/−0.34 coefficients, not a CBO-published figure. CLAUDE.md and the memo say this correctly.
- **FAQ:96, "−$6,066 → −$6,499":** this comes from the September 16 second-generation adult ledger (taxes minus selected transfers), not the September 19 ledger quoted around it.
- **FAQ:218, 2019 ratio 1.91×:** the CSV gives 1.906, so 1.91× is right. The incarceration memo's line 43 prints 1.90×.
- **INDEX:82, "over a third" pandemic share:** this holds for the programme rule (35–38%). One income-adjusted case is 33.0%.
- **INDEX:169 against INDEX:173:** −$217.32bn is called a superseded annual vintage and is also quoted as the ledger's central value. Both are correct, because only this ledger carries the generation split, but side by side they can mislead.
- **Other INDEX table rows:**
  - 199: +0.29 and −2.80 come from different windows.
  - 202: "CMS 22%" is a 1.22 coverage multiplier.
  - 203: the 0.18 elasticity is the complete-states specification; all metros give 0.384.
  - 213: "Medicaid 3.3×" is measured against non-Hispanic whites; against all donors it is 1.83.
  - 228: 1.7–1.9× is institutional residence, not incarceration, and the row omits the reallocated 2.1–2.3×.

## Checked in passing, outside scope
- `historical_backcast` memo, programme table: the row reads "Education (193)", but `national_programme_index.csv` gives school at $105.4bn. The label mixes all education with the school line.
- `high_skill_origin_screen` RESULT.md: the verdict says 17 groups, but the CSV and the INDEX have 19.

## Coverage
- **FAQ:** every section was checked (anchors; "Before combining numbers"; entries 1–14; Instrument; Revisions), with 81 rows in `checks.csv`. The Instrument section has no numbers. Qualitative claims without numbers ("old-age cells reduce the measured gap") were not tested.
- **INDEX Core State prose, lines 18–176:** 47 numbers, re-derived from CSV/JSON wherever a derived file exists. Paper figures (1.2%, 21 models, 72 MB, 63–64%, 2.25%) were checked against the memo or its paper notes; the PDFs were not re-opened.
- **INDEX table rows, lines 197–230:** 50 numbers. Rows 205–207, 210, 216–217, 219–227 and 230 carry only dates or ladder references.
- **INDEX table rows, lines 231–282:** about 95 figures on 22 numeric rows. Only the non-VERIFIED rows are written out in `checks.csv`, because the worker could not write files. Rows 238–282 other than 241–253, 257–258 and 277 carry no argumentative numbers.
- **Skipped:** the INDEX outside Core State, and the working-tree drafts (out of scope by instruction). Memo-internal figures were not audited unless the FAQ or INDEX quotes them.

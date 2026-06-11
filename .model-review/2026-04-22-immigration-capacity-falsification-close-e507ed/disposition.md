# Review Findings — 2026-04-22

**19 findings** from 2 axes (1 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Archival newcomer memo is internally contradictory **[CROSS-MODEL: also GPT-5.4 (quantitative/formal)]**
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The file opens with a corrected supersession note citing ACS B07001_081E and ~20.5x ratio, but the body retains the old method (ACS B05005), old row count (9,120), and old 33x claim.
   File: research/immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Split the newcomer memo into a current version and an archival provenance appendix to remove live semantic contradictions.

---

2. **[HIGH]** Current citation graph points to semantically stale source
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Confidence ladder item 22 and the index cite the newcomer memo for downgraded claims, but the cited source still contains old 33x methodology and results in its body, breaking traceability.
   File: research/immigration-confidence-ladder.md
   Fix: Update the citation graph to point only to updated, consistent content or separate the current findings into a new file.

---

3. **[HIGH]** Missing machine-readable measurement metadata
   Category: architecture | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   There is a lack of metadata (universe, time window, unit) for analysis artifacts, leading to potential semantic drift between non-equivalent constructs like IRS and ACS migration data.
   File: 
   Fix: Attach a measurement contract JSON to each output dataset with fields for universe, time_window, unit, and comparability_warning.

---

4. **[HIGH]** Failure to source internal narrative blocks
   Category: constitutional | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Major files contain unsourced narrative blocks and stale internals, specifically in the newcomer memo where the header/body contradiction breaks traceability.
   File: research/immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Inline-source quantitative claims directly from the data artifacts and split archival notes from current content.

---

5. **[HIGH]** Threshold holdout splits may leak spatially correlated counties between train and test
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review argues that threshold_search_holdout in analyze_capacity_falsification.py appears to rely on random county-level splits (THRESHOLD_SPLITS = 60), which would contaminate holdout evaluation because nearby counties in the same state/MSA share policy and macro shocks. The example given is that training on Cook County, IL could transfer spuriously well to DuPage County, IL. The reviewer notes this may be moot if grouping is already implemented in truncated code.
   File: analyze_capacity_falsification.py
   Fix: Use GroupShuffleSplit or GroupKFold keyed by state_fips (or a coarser geography such as Census division), and assert that no group appears in both train and test for a split.

---

6. **[MEDIUM]** Newcomer script semantics were only partially cleaned
   Category: bug | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   Function fetch_acs_county_population_and_recent_fb() docstring describes old estimand (B05005_002E + B05005_004E) while the code actually requests a different set of variables (B01003, B05002, etc.).
   File: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py
   Fix: Update function docstrings and code comments to match the actual variable definitions and requests.

---

7. **[MEDIUM]** README output-path contract is stale
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   README states outputs land in data/analysis/, but the actual falsification tranche artifacts are located under data/outcomes/analysis/.
   File: sources/immigration-causal/README.md
   Fix: Correct the README to reflect the actual artifact locations in data/outcomes/analysis/.

---

8. **[MEDIUM]** ACS moved-from-abroad share uses the wrong population universe as denominator
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review flags a semantic mismatch in analyze_internal_vs_immigrant_newcomers.py at lines 114 and 116: B07001_081E (moved from abroad in the past year) is divided by B01003 total population. B07001 is defined on the population age 1 year and over, while B01003 includes infants, so the numerator and denominator are drawn from different Census universes.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Fetch and use B07001_001E (population 1 year and over) as the denominator for moved_from_abroad_share so numerator and denominator are in the same ACS universe.

---

9. **[MEDIUM]** Newcomer memo omits the direction of measurement bias in the 20.5x ratio
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says immigration-causal-internal-vs-immigrant-newcomers.md acknowledges that B07001_081E is 'not immigrant-only' but fails to state the key implication: it includes returning U.S. citizens (expats, military, students), which overstates the foreign/newcomer burden if interpreted as immigrant-only. Combined with the IRS undercount of domestic movers, the reviewer says the 20.5x domestic-to-foreign ratio should be described explicitly as a lower bound rather than a neutral cross-source comparison.
   File: immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Add explicit language that ACS moved-from-abroad includes returning U.S. citizens while IRS misses some domestic movers, so the measured 20.5x gap understates the true domestic-origin vs foreign-origin newcomer disparity.

---

10. **[MEDIUM]** Annual county panels are insufficient for causal wage-channel inference and should be retired for that question
   Category: architecture | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review argues that adding 2017-2018 pre-trends showed annual county data cannot identify a stable wage penalty around the surge and recommends stopping further pre-2017 window searches in annual data. It proposes routing future causal wage questions to higher-frequency or microdata sources such as quarterly QCEW/QWI or PUMS instead of continuing annual-panel extraction attempts.
   File: 
   Fix: Document that annual county panels are out of scope for causal wage-channel identification, and redirect future wage-causality work to quarterly or microdata sources in the index/master plan.

---

11. **[MEDIUM]** Threshold search should be framed as descriptive classification, not a causal breakpoint estimate
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review recommends preserving the downgraded interpretation of the threshold exercise. Because pre-trend evidence no longer supports a stable causal threshold, the reviewer says the threshold search should be labeled a 'descriptive vulnerability classifier' or similar exploratory stress marker rather than a 'causal breakpoint estimator.'
   File: 
   Fix: Update analysis language and downstream references so threshold outputs are consistently described as descriptive/exploratory rather than causal threshold identification.

---

12. **[MEDIUM]** Zero-base growth handling can create survivor bias if reused for sector-level QCEW
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review flags that build_county_outcome_panel.py marks zero_base_count and assigns pd.NA when x <= 0. That avoids undefined log growth, but it also drops counties moving from 0 to positive employment. The reviewer says this is harmless for total county employment but would bias analyses if the same code is reused for sector-specific panels such as construction or agriculture.
   File: build_county_outcome_panel.py
   Fix: Handle zero-to-positive transitions explicitly in sectoral reuse cases, such as by using an alternative growth transform, a separate entry indicator, or documented sample restrictions rather than silently dropping them.

---

13. **[MEDIUM]** Threshold-search confidence is qualitatively downgraded but under-quantified
   Category: performance | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The design uses only 60 actual and 60 null splits. The memo uses qualitative descriptors like 'beats the null strongly' instead of exact Monte Carlo precision or actual-vs-null differences.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Increase THRESHOLD_SPLITS and export exact uncertainty metrics like actual-null mean difference and split-seed SD.

---

14. **[MEDIUM]** Missing ACS MOE filtering for newcomer comparison
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The newcomer comparison is currently descriptive but noisy because it lacks filtering for unreliable counties based on ACS Margin of Error (MOE).
   File: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py
   Fix: Fetch ACS MOEs for B07001_081E and filter/flag counties with unreliable estimates.

---

15. **[MEDIUM]** Under-quantification of evidence strength
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Claims like 'beats null strongly' and 'policy relevance high' are not sufficiently quantified with exact effect-size deltas or uncertainty intervals.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Add exact effect-size deltas and uncertainty intervals to qualitative claims.

---

16. **[MEDIUM]** IRS and ACS newcomer shares are not directly comparable because they count different units
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review says analyze_internal_vs_immigrant_newcomers.py compares us_inflow_persons from IRS SOI n2 to ACS B07001 newcomer counts after scaling both by ACS population, but IRS n2 counts exemptions (filers plus dependents) whereas ACS B07001 counts individuals age 1+. The reviewer further notes IRS systematically misses non-filers, undocumented people, and some very low-income movers, so the reported domestic inflow share is a floor and the true domestic-vs-foreign disparity is likely larger.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Do not present IRS and ACS shares as directly equivalent without qualification; either harmonize units if possible or label the IRS-based domestic inflow share as a lower-bound floor in outputs and downstream memos.

---

17. **[MEDIUM]** Missing memo-artifact consistency linter
   Category: architecture | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The repository lacks an automated check to prevent stale-number regressions where memo text drifts from the actual data in parquet/CSV summaries.
   File: 
   Fix: Implement a linter that validates cited numbers in memos against the current output artifacts.

---

18. **[MEDIUM]** QCEW nondisclosure handling lacks an explicit assertion check
   Category: missing | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review notes that the audit log shows zero nondisclosure_missing_base_count in the current analysis sample, likely because the totpop >= 10k filter dropped counties with suppressed QCEW data. It warns that if smaller counties are later included, the current pd.to_numeric(..., errors="coerce") pathway depends on upstream handling of disclosure code N and should be guarded by an explicit consistency assertion.
   File: build_county_outcome_panel.py
   Fix: Add an assertion verifying that missing QCEW base values match the expected nondisclosure-flagged observations (for example, comparing base-column NA counts to disclosure_code_N counts) before growth calculations proceed.

---

19. **[LOW]** Legacy 'native' terminology should be removed from the immigration index and plans
   Category: style | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review recommends a terminology cleanup so IRS-based county-to-county migration is no longer described as 'native' migration. It specifically suggests sweeping research/immigration-INDEX.md and related master plans so 'native' only appears where it truly refers to native-vs-immigrant comparisons in wage literature, not domestic movers.
   File: research/immigration-INDEX.md
   Fix: Replace legacy 'native' references with 'domestic,' 'internal,' or 'Total Migration-US' in the index and related planning documents.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


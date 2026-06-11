# Review Findings — 2026-04-22

**19 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Silent deduplication of QCEW county-year records
   Category: bug | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The script uses drop_duplicates(["fips5", "year"]) without a row-count audit or assertion. This hides potential data-integrity failures or schema changes in the upstream QCEW data.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Replace silent deduplication with hard uniqueness assertions and exception logging; the build should fail if unexpected duplicates are detected.

---

2. **[HIGH]** Raw `fips5` left joins can silently drop or null counties across IRS and QCEW sources
   Category: architecture | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review warns that the panel joins `elect`, `qcew`, `inflow`, and `outflow` on `fips5`, but QCEW uses some BLS-modified county codes while IRS uses standard Census FIPS. In jurisdictions with differing conventions, the `how="left"` merges from the `elect` spine can silently produce `NaN` IRS/QCEW fields, skewing county-level aggregates without any warning or reconciliation report.
   File: build_county_outcome_panel.py
   Fix: Add explicit FIPS reconciliation and diagnostics before export, e.g. count unmatched `elect` counties in each source, print warnings, and normalize known BLS/Census county-code differences before merging.

---

3. **[MEDIUM]** Zero-denominator log changes are silently dropped instead of handled explicitly
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The reviewer cites `pd.Series(panel[end_col]).div(panel[base_col]).where(panel[base_col] > 0)` and notes that when `base_col == 0` the result becomes `NaN`. This means counties with zero base-year QCEW employment are silently excluded from change calculations rather than being treated as a distinct entry/exit case or otherwise documented.
   File: build_county_outcome_panel.py
   Fix: Handle zero-base observations explicitly: define an entry/exit category, use an alternative transformation that tolerates zeros, or at minimum report how many counties are dropped for zero baseline values.

---

4. **[MEDIUM]** Over-reification of modal threshold selection in wage analysis
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The analysis code reports the modal selected quantiles (q60 recent-flow & q50 permit) but fails to report the concentration or entropy of selections across splits. Labeling it 'the threshold' is materially too strong if the selection surface is diffuse.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Export the full threshold-selection distribution (share per quantile pair) and a concentration metric to validate the stability of the q60&q50 cell.

---

5. **[MEDIUM]** Ambiguous semantic definition of 2018-2020 pretrend windows
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The panel builder materializes pairwise changes (2018→2019 and 2019→2020) rather than a direct cumulative 2018→2020 change, creating ambiguity if downstream memos imply a single cumulative preperiod.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Rewrite memo language to specify pairwise windows or update the build script to include a true qcew_*_log_change_2018_2020 variable.

---

6. **[MEDIUM]** Missing outcome-window sample ledgers
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   There is no visible export of sample counts (N) included or excluded by outcome and reason (e.g., missing QCEW, zero permit, missing IRS), risking over-interpretation of results from shifting samples.
   File: 
   Fix: Add outcome-window sample ledgers that explicitly bound sample loss for each regression family.

---

7. **[MEDIUM]** Within-state permutation inference ignores spatial autocorrelation and may overstate significance
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that `analyze_capacity_falsification.py` uses within-state shuffles via `np.random.default_rng(20260421)`, which addresses state fixed effects but not spatial clustering of immigration loads. Counties in places like South Texas may share correlated unobservables, so permutation p-values such as `p<=0.001` may be too confident absent spatially aware inference. The reviewer says division leave-out only partially mitigates this.
   File: analyze_capacity_falsification.py
   Fix: Use spatially robust inference such as Conley standard errors or distance/cluster-aware permutations, or explicitly downgrade and document the remaining spatial-dependence limitation in the results summary.

---

8. **[MEDIUM]** Panel builder does not materialize the claimed 2018–2020 QCEW window
   Category: bug | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review says the memo claims there are 'true 2018–2020 QCEW pretrend windows,' but `build_county_outcome_panel.py` only iterates over `(2018, 2019)`, `(2019, 2020)`, `(2020, 2021)`, `(2021, 2022)`, `(2021, 2023)`, `(2023, 2024)`, and `(2021, 2024)` in the `add_log_change()` loop. The reviewer notes this creates a silent semantic disconnect unless `analyze_capacity_falsification.py` reconstructs 2018–2020 downstream.
   File: build_county_outcome_panel.py
   Fix: Add `(2018, 2020)` directly to the log-change tuple list and verify the exported panel contains `qcew_employment_log_change_2018_2020` and `qcew_wkly_wage_log_change_2018_2020`.

---

9. **[MEDIUM]** Using QCEW annual-average 2020 as a pretrend baseline mixes in COVID shock volatility
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review flags that the script filters `chunk["qtr"] == "A"`, i.e. annual averages. That means the 2020 baseline includes pre-COVID Q1, lockdown shock quarters, and recovery, so a '2018–2020 pretrend' may already be contaminated by pandemic variance. The reviewer recommends a cleaner cutoff such as 2019 Q4 or at least an explicit acknowledgement that 2020 annual averages are confounded.
   File: build_county_outcome_panel.py
   Fix: Prefer a clean pre-pandemic baseline (for example through 2019 Q4) or explicitly document that 2020 annual averages are used and treat the resulting COVID contamination as a confounder in the falsification analysis.

---

10. **[MEDIUM]** Overstated evidentiary level for real-vs-null search superiority
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The claim that the search 'clearly beats a null search' is not supported by a direct statistical test (e.g., delta statistic, CI, or p-value) comparing real and null holdout distributions in the current output.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Add a formal comparison statistic, such as a bootstrap CI for the difference in sign-match rate and median holdout absolute t-statistics between real and null runs.

---

11. **[MEDIUM]** IRS migration measure may be temporally misaligned with the QCEW outcome windows
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review says the code hardcodes IRS internal migration for `2022_23`, but those files often correspond to tax-year movement closer to TY2021–2022 rather than a contemporaneous 2022–2023 flow. Using that proxy against 2023–2024 QCEW outcomes risks interpreting a pre-surge or earlier-period mobility measure as if it aligned with the heaviest 2023–2024 shock.
   File: 
   Fix: Document the tax-year/file-vintage lag explicitly in code and memo, and if possible rename or replace the variable with one whose timing is correctly aligned to the analyzed outcome window.

---

12. **[MEDIUM]** Silent semantic failure in IRS migration zero-fill
   Category: bug | Confidence: 0.7 | Source: GPT-5.4 (quantitative/formal)
   IRS migration missingness is coded as literal zero via fillna(0). If absent rows in the source represent suppression or non-reporting rather than zero flows, the net_migration outcome is mechanically biased.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Treat IRS absent rows as missingness with an audit flag and rerun net_migration analyses to check sensitivity compared to the zero-fill method.

---

13. **[LOW]** Falsification memo uses vague pretrend language instead of reporting quantitative evidence
   Category: constitutional | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review objects to wording in `immigration-capacity-falsification-2026-04-21.md` such as 'wage pretrends look mostly weak before 2020.' It argues this violates the constitution's requirement to quantify when possible and asks for exact coefficients, p-values, or an `R^2` for the pretrend relationship rather than a qualitative label.
   File: immigration-capacity-falsification-2026-04-21.md
   Fix: Replace vague qualifiers with numeric pretrend evidence in the memo, e.g. report the estimated coefficient, confidence interval or p-value, and optionally model fit metrics for the cited pretrend tests.

---

14. **[LOW]** Memo-to-memo citation chains weaken source traceability
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Some claims rest on summary memos citing other memos rather than raw data artifacts, which violates the 'Source everything' principle for quantitative claims.
   File: 
   Fix: Replace internal memo citations with raw CSV, JSON, or commit-level citations for all quantitative and chronological claims.

---

15. **[LOW]** Sparse application of framing-sensitivity tags
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The [FRAMING-SENSITIVE] tag is used broadly at the end of the memo rather than being attached to individual policy-facing inferences, reducing granular transparency.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Tag each policy-facing sentence or inference individually as [FRAMING-SENSITIVE] to distinguish descriptive findings from policy extrapolations.

---

16. **[LOW]** IRS migration variable naming obscures the underlying tax-year timing
   Category: style | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   Separately from the timing issue itself, the reviewer argues names like `us_inflow_persons_2022_23` invite misinterpretation because they read like event-time migration rather than IRS tax-year-based movement. This creates 'cognitive drift' in causal interpretation of the DAG.
   File: build_county_outcome_panel.py
   Fix: Rename migration variables to reflect tax years explicitly, e.g. `net_us_migration_persons_ty21_22`, and preserve that naming in downstream outputs and memo text.

---

17. **[LOW]** Incomplete operationalization of rival explanations
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Rival explanations like pandemic resilience and structural decline are listed but not fully steel-maned into measurable, discriminating empirical tests.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: For each rival explanation, add one discriminating empirical test and the expected sign pattern that would distinguish it from the capacity-marker hypothesis.

---

18. **[LOW]** Circular provenance in reasoning-evolution documentation
   Category: architecture | Confidence: 0.7 | Source: GPT-5.4 (quantitative/formal)
   The provenance document cites later synthesis memos for chronology-sensitive claims, weakening the separation between bug-driven corrections and evidence-driven updates.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Recast the document as a matrix mapping each claim version to specific commit IDs, raw result files, or dated artifacts rather than narrative summaries.

---

19. **[LOW]** Tension between employment control survival and confounding claims
   Category: logic | Confidence: 0.7 | Source: GPT-5.4 (quantitative/formal)
   The reasoning-evolution doc states employment effects 'still survive controls' while also declaring employment 'materially confounded,' which may be misinterpreted as claiming substantively robust identification.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Clarify that survival-after-controls in this context does not satisfy clean identification requirements given the preexisting trends.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


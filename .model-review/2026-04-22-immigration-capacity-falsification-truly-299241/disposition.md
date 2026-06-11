# Review Findings — 2026-04-22

**17 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[CRITICAL]** IRS domestic migration extract appears to use foreign-migration code 97 instead of US-total code 96
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review claims that `build_county_outcome_panel.py` functions `load_native_inflow()` and `load_native_outflow()` filter IRS SOI migration rows with `y1_statefips == "97"` and `y2_statefips == "97"`. In standard IRS SOI migration dictionaries, `96` denotes total US migration and `97` denotes total foreign migration. If true, the script is extracting foreign inflows/outflows, renaming them as `us_inflow_returns_2022_23` / `us_outflow_returns_2022_23`, and using them to compute `net_us_migration_share_2022_23`, which invalidates the native mobility / native sorting interpretation.
   File: build_county_outcome_panel.py
   Fix: Change the IRS filter from state FIPS `97` to `96` after verifying the exact dictionary for the 2022-2023 release, then rebuild the county panel and downstream migration analyses.

---

2. **[HIGH]** "Rules out a one-state artifact" appears unsupported by the visible artifact set
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The review scope emphasized division leave-out, but the memo claims the result is not a 'one-state' artifact. The visible code and output files (county_capacity_geographic_leaveout.csv) only support division-level analysis, making the state-level claim too strong.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Either add explicit state leave-out analysis or delete 'one-state artifact' language from the memo.

---

3. **[HIGH]** Pretrend falsification baseline is endogenous because permit capacity includes 2019 while testing 2018-2019 outcomes
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review argues that the falsification script evaluates a `2018-2019` QCEW pretrend against a permit baseline from `2017-2019` via `extract_pre_surge_permits()`. Because 2019 permits can be downstream of 2018-2019 local growth, the baseline is not strictly antecedent and may introduce reverse causality into the pretrend test.
   File: analyze_capacity_falsification.py
   Fix: Restrict the pre-surge capacity baseline to years strictly before the outcome window, e.g. aggregate permits only through 2017 for the `2018-2019` pretrend specification.

---

4. **[HIGH]** Annual-average QCEW windows spanning 2020 blur the pandemic shock and may destabilize threshold searches
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review states that `build_county_outcome_panel.py` computes `2019-2020` and `2020-2021` log changes using QCEW rows filtered with `qtr == "A"` (annual averages). Annual averages for 2020 mix pre-lockdown and lockdown quarters, creating substantial measurement noise. The reviewer argues this likely contributes to the reported diffuse and unstable threshold surface.
   File: build_county_outcome_panel.py
   Fix: Avoid annual log-change windows that touch 2020, or switch to quarterly QCEW data (e.g. Q4-to-Q4 comparisons) for pandemic and post-pandemic analyses.

---

5. **[MEDIUM]** Code materializes contaminated windows without machine-readable metadata
   Category: architecture | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The final conclusion depends on NOT using 2019–2020 or 2020–2021 windows causally, but these are generated without explicit contamination flags. This creates a risk of future semantic regression where downstream scripts misuse contaminated data.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Add a window_registry artifact and label each derived window as clean_pre_covid, covid_contaminated, or post_surge.

---

6. **[MEDIUM]** "2018–2020 pretrend windows" language remains semantically loose
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The index and reasoning-evolution doc describe the tranche as using 'true 2018–2020 QCEW pretrend windows,' while the final memo says windows touching 2020 are COVID-contaminated and should not support the wage/employment split. This is a meaning bug where 'includes 2020 windows' is true but 'supports causal pretrend inference' is not.
   File: research/immigration-INDEX.md
   Fix: Align terminology across all documents to distinguish between the presence of data windows and their valid usage for causal inference.

---

7. **[MEDIUM]** Threshold-language is still under-quantified
   Category: style | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The memo uses qualitative terms like 'beats the null strongly' and 'diffuse cutoff surface' without exposing the actual margins (e.g., sign-match share difference, median |t| difference).
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Quantify threshold claims in the memo with exact margins pulled from the summary JSON/CSV artifacts.

---

8. **[MEDIUM]** Native-mobility threshold and null analyses should be rerun after correcting the IRS migration coding
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   Because the review claims the migration outcome was built from foreign IRS flows rather than domestic flows, it concludes that prior `threshold_null` and `threshold_surface` results for native sorting are not interpretable. Downstream falsification summaries based on the mislabeled migration outcome therefore need to be regenerated.
   File: 
   Fix: After correcting the IRS FIPS mapping, rerun the migration-related threshold/null analyses and refresh summary outputs such as `county_capacity_falsification_summary.json`.

---

9. **[MEDIUM]** Sample-accounting audit is not aligned to the actual clean-window claim
   Category: bug | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The script build_county_outcome_panel.py keys qcew_row_missing to annual_avg_emplvl_2021. However, the substantive clean-window claim rests on 2018–2019. A county missing data in 2018 but present in 2021 would be incorrectly counted as present for the falsification window.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Expand audit/sample accounting to per-window usable N and zero-base counts for the specific years used in the causal analysis.

---

10. **[MEDIUM]** Hardcoded occupants-per-unit scalar may systematically mis-scale housing capacity
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review flags a hardcoded `OCCUPANTS_PER_UNIT = 2.5` in the falsification workflow. The reviewer argues this embeds a single household-size assumption that may be inappropriate where immigrant household formation is larger, causing the permit-derived capacity ratio to be systematically mismeasured.
   File: analyze_capacity_falsification.py
   Fix: Parameterize the occupants-per-unit assumption or replace it with county-level external household-size estimates such as ACS-based values by FIPS.

---

11. **[MEDIUM]** "Not a binning accident" is broader than the demonstrated checks
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Evidence supports monotonicity by decile and threshold-search robustness, which protects against specific discretization artifacts but not against binning dependence in general. Invariance across multiple schemes or a continuous-specification check is missing.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Add a binning-invariance check (quintiles/ventiles) or narrow the wording from 'not a binning accident' to 'not driven by the specific threshold search.'

---

12. **[MEDIUM]** County panel does not explicitly handle QCEW privacy suppressions, risking sample-composition bias
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that `build_county_outcome_panel.py` drops duplicate or missing FIPS but does not explicitly model BLS privacy suppressions for small counties. If suppressed counties become `pd.NA` and fall out of log-change calculations, the resulting panel can systematically overweight urban and suburban counties and distort estimated capacity-frontier dynamics.
   File: build_county_outcome_panel.py
   Fix: Audit suppressed or missing QCEW county observations, quantify attrition by county type, and add explicit handling such as flags, imputation rules, or robustness checks for sample-selection bias.

---

13. **[MEDIUM]** Annual causal claims for COVID-overlap years should be explicitly blocked until quarterly QCEW is used
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review recommends suspending or demoting annual causal claims for windows overlapping 2020 because annual averages confound pre-pandemic and lockdown periods. It specifically asks for memos to acknowledge that the wage/employment split cannot be finalized without quarterly QCEW bridging late 2019 to late 2021.
   File: 
   Fix: Update analytical writeups to mark annual 2020-overlap results as provisional artifacts of data aggregation, and require quarterly QCEW before making final causal claims for that period.

---

14. **[MEDIUM]** IRS migration is treated as a generic native-mobility proxy despite undercoverage of low-income movers
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review argues that IRS migration data capture tax filers, yet the memo uses the series as a broad proxy for native mobility. This may structurally undercount low-income natives and recent movers who do not file promptly or at all, especially the population most relevant to low-skill labor-market displacement claims.
   File: build_county_outcome_panel.py
   Fix: Qualify the construct as tax-filer migration rather than generic native mobility, and validate or supplement it with additional mobility sources that better cover low-income movers.

---

15. **[MEDIUM]** Single-threshold search may be the wrong model for a diffuse cutoff surface
   Category: architecture | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review interprets the reported diffuse threshold surface as evidence against a stable scalar cutoff and in favor of heterogeneous treatment effects. Continuing to search for one universal threshold may be a misspecified modeling strategy, especially if effects vary with state housing elasticity or similar context variables.
   File: analyze_capacity_falsification.py
   Fix: Replace or complement the scalar threshold search with a heterogeneity-aware method such as a causal forest, margin tree, or threshold model conditioned on state-level elasticity measures.

---

16. **[LOW]** Inconsistent sourcing with bare placeholders
   Category: style | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   Several major claims in the memo use bare [SOURCE] placeholders rather than explicit citation-grade file paths or direct CSV/JSON links.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Replace bare [SOURCE] placeholders with explicit file paths and cite CSV/JSON outputs directly where possible.

---

17. **[LOW]** Policy relevance claim is not falsifiable
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The claim 'Policy relevance remains high' is not testable as written because it lacks a specified policy objective, welfare metric, or counterfactual.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Explicitly state whose welfare function or policy objective is being optimized, or re-label the claim as framing-sensitive.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


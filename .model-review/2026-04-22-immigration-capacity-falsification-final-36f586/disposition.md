# Review Findings — 2026-04-22

**16 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[CRITICAL]** Pretrend windows incorrectly include COVID-disrupted 2020 annual QCEW data
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review states that `build_county_outcome_panel.py` iteratively defines pretrend windows including `(2018, 2020)` and `(2019, 2020)` while pulling `annual_avg_emplvl` and `annual_avg_wkly_wage` for 2020. The reviewer argues this is a semantic failure because 2020 is not a clean pretrend year: it contains the largest pandemic-era macro shock, so any window ending in 2020 is contaminated rather than pre-treatment.
   File: build_county_outcome_panel.py
   Fix: Remove all pretrend windows that span or end in 2020. Use a true pretrend baseline such as 2017-2019, and compute post-surge changes from 2019 to 2023/2024 instead.

---

2. **[CRITICAL]** Memo's wage-versus-employment causal split may be an artifact of 2020 COVID effects
   Category: logic | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review quotes `immigration-capacity-falsification-2026-04-21.md` as saying that wage pretrends are mostly weak before 2020 while employment pretrends are already negative, and says this drove the repo's stance that employment effects are confounded by 'preexisting county weakness' while wage effects remain causally plausible. The reviewer calls this a fatal semantic error because dense urban immigration destinations had stricter COVID lockdowns, so the observed 2019-2020 employment drop may reflect pandemic shock rather than structural weakness.
   File: immigration-capacity-falsification-2026-04-21.md
   Fix: Re-run the falsification analysis on a clean 2017-2019 pretrend / 2019-to-2023-2024 design. Retract or mark the employment-confounding versus wage-causal split as unverified unless it survives that rerun.

---

3. **[HIGH]** Annual-average 2020 QCEW introduces composition bias that can distort wage and employment trends
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review claims that using 2020 `annual_avg_emplvl` and `annual_avg_wkly_wage` creates composition bias: low-wage service job losses make county employment collapse while average weekly wages can mechanically rise or remain flat. This means apparent wage resilience versus employment weakness may be an artifact of pandemic composition effects rather than a meaningful economic split.
   File: build_county_outcome_panel.py
   Fix: Avoid annual-average 2020 measures for causal trend comparisons; prefer quarterly QCEW extraction, with a pre-pandemic baseline such as Q4 2019 and endlines such as Q4 2023/Q4 2024.

---

4. **[HIGH]** Analysis acknowledges COVID contamination but does not perform the basic 2017-2019 disconfirmation test
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says the falsification memo explicitly recognizes 'COVID contamination in the 2020 annual-average' as a rival explanation, yet fails to test a clean `2017-2019` pretrend. The reviewer frames this as a mandatory disconfirmation failure: the analysis raised a clear rival hypothesis but did not execute the simplest check that could falsify the 'preexisting county weakness' narrative.
   File: immigration-capacity-falsification-2026-04-21.md
   Fix: Add a dedicated falsification pass using only 2017-2019 pretrend windows and report whether the employment weakness persists absent 2020.

---

5. **[HIGH]** Threshold-surface concentration comparison is likely apples-to-oranges
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   In 'analyze_capacity_falsification.py', 'surface_actual' is compared to 'surface_null' without filtering to the same outcome. Since the null search is wage-only, pooling wage, employment, and margin outcomes in the 'actual' set mechanically flattens the concentration metrics, potentially invalidating the comparison.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Filter 'surface_actual' to wage-only outcomes before comparing modal share and top-3 share against the null distribution.

---

6. **[MEDIUM]** Remaining bare [SOURCE] placeholders in memos
   Category: constitutional | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The corrected memo contains multiple instances of bare '[SOURCE]' tags without paths or citations. This violates the 'Source everything' principle and renders key claims non-auditable.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Perform a citation scrub and replace all bare placeholders with specific file paths or output artifact citations.

---

7. **[MEDIUM]** County panel audit does not actually audit the new 2018–2020 falsification windows
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The script 'build_county_outcome_panel.py' sets 'qcew_row_missing' based solely on 'annual_avg_emplvl_2021.isna()'. This means it fails to audit the 2018, 2019, and 2020 pretrend windows or wage data, making the memo's claim of 'explicit sample accounting' unsupported for the specific windows used in the corrected falsification.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Update the audit logic to count non-missing rows for wage and employment across every year in the falsification window (2018, 2019, 2020, 2021, 2023, 2024).

---

8. **[MEDIUM]** Falsification memo conclusion should not retain 'preexisting county weakness' without a clean pre-2020 rerun
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says `immigration-capacity-falsification-2026-04-21.md` should remove or downgrade the claim about 'preexisting county weakness' unless that pattern persists in a 2017-2019 window. It specifically recommends tagging the current wage/employment split as `[UNVERIFIED]` pending rerun, because the present conclusion may rest on contaminated 2020 evidence.
   File: immigration-capacity-falsification-2026-04-21.md
   Fix: Rewrite the memo conclusion to mark the 'preexisting county weakness' claim as provisional or retract it until a clean 2017-2019 analysis confirms it.

---

9. **[MEDIUM]** Reasoning-evolution record does not document the April 21 causal split as a COVID-driven reasoning bug
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review recommends updating `research/immigration-reasoning-evolution-2026-04-21.md` so Phase 8 records that the April 21 wage/employment split was itself an artifact of the 2020 COVID composition effect. The reviewer treats this as a second-order reasoning bug that should be preserved in the epistemic audit trail, not left implicit.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Add an explicit correction entry stating that the April 21 employment-versus-wage split was likely induced by contaminated 2020 annual QCEW measures and required revision after a 2019-baseline rerun.

---

10. **[MEDIUM]** QCEW pipeline is too coarse because annual files smear pre-pandemic and peak-pandemic periods together
   Category: architecture | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review says the pipeline defaults to QCEW `annual_singlefile.zip`, which mixes Jan-Feb 2020 pre-surge conditions with Apr-Dec 2020 pandemic disruption. This makes temporal boundaries imprecise and weakens any attempt to define clean baselines around the immigration surge.
   File: build_county_outcome_panel.py
   Fix: Extract quarterly QCEW data instead of annual averages, using tighter anchors such as Q4 2019 for baseline and Q4 2023/Q4 2024 for endpoints.

---

11. **[MEDIUM]** Spatial robustness wording may outrun the demonstrated leave-out design
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The memo claims the signal is 'not a one-state artifact', but the provided materials only verify 'division' leave-out. Division-level robustness does not necessarily prove state-level robustness.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Either add explicit leave-one-state-out results to 'county_capacity_geographic_leaveout.csv' or adjust the memo wording to refer only to census divisions.

---

12. **[MEDIUM]** Threshold null search may understate false positives by not preserving spatial autocorrelation
   Category: logic | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review warns that `analyze_capacity_falsification.py` generates a threshold null search (`threshold_null`), but the excerpt does not show whether it preserves county-to-county spatial correlation. If the null is based on naive shuffling within state, the reviewer argues it will underestimate how often diffuse clusters of significance appear by chance, making threshold findings look more exceptional than they are.
   File: analyze_capacity_falsification.py
   Fix: Implement a spatially aware null, such as Commuting Zone block permutation, block bootstrap, or another Moran's-I-preserving permutation scheme, and compare observed threshold behavior against that null.

---

13. **[LOW]** 'Zero base' audit counts are semantically contaminated by missingness
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   In 'add_log_change', 'zero_base_flag' is calculated by filling NAs with 0, meaning missing base values are counted as both 'zero_base' and 'missing_input'. This renders the '*_zero_base_count' metrics formally incorrect.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Relabel or recompute 'zero_base_count' to explicitly exclude missing bases so that categories are mutually exclusive.

---

14. **[LOW]** Review artifact is being used as empirical evidence, not just provenance
   Category: style | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The memo cites '.model-review/verified-disposition.md' to support substantive empirical claims. While appropriate for history, primary empirical support should point to raw data outputs (CSV/JSON) or code.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Relink empirical claims to primary output artifacts and reserve .model-review citations for procedural/correction history.

---

15. **[LOW]** Memo claims more window construction than the visible builder shows
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The memo claims the panel includes '2018–2020 cumulative' QCEW windows, but the builder script only shows annual levels and pairwise log changes (e.g., 2018_2019, 2018_2020). The provenance chain for the cumulative variable is incomplete.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Explicitly materialize the cumulative window in the builder script or cite the specific analysis code where it is derived.

---

16. **[LOW]** Missing memo-to-output consistency checks
   Category: architecture | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   There is a risk of narrative drift where memo claims (e.g., permutation counts, p-values) may not match the actual exported values in JSON/CSV files.
   File: 
   Fix: Implement a lightweight 'claim-check' script that asserts that values cited in the memo match the machine-readable output files.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


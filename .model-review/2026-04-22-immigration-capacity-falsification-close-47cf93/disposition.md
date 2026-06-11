# Review Findings — 2026-04-22

**19 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Immigrant inflow proxy annualizes a 12-year stock by dividing by 12
   Category: logic | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review says `analyze_internal_vs_immigrant_newcomers.py` uses ACS B05005 ('entered 2010 or later') and divides by 12 to create `recent_fb_annual_avg`. This is a stock measure spanning 12 years, not a 1-year gross flow, and it is affected by attrition from mortality and emigration. The reviewer argues this systematically understates annual immigrant inflows relative to the IRS 1-year domestic inflow metric and therefore inflates the reported domestic-to-immigrant ratio (described as about 33x).
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Replace the stock-based proxy with a true 1-year flow measure such as ACS table `B07001` ('Moved from abroad') or another annual immigration flow source before comparing against IRS 1-year internal migration.

---

2. **[HIGH]** Mislabeling of pretrend test as pure placebo
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The pretrend test is not a pure presurge placebo because the treatment numerator uses ACS 2022 5-year data (entered-2010-or-later stock) while only the permit denominator is moved to a 2017-2019 baseline. This constitutes a lead-exposure association test rather than a clean pre-treatment placebo.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json
   Fix: Rename the test family to lead-exposure presurge-window and rebuild the numerator using pre-2020 immigrant flow proxies for a true placebo.

---

3. **[HIGH]** Unreported sample attrition for zero-permit counties
   Category: missing | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Regression samples exclude 77 counties with zero prebase permits (3.2% of the panel), which are likely the most capacity-constrained edge cases. Claims about the county panel do not specify that they represent only the nonzero-prebase-permit subset.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv
   Fix: Add explicit sample-attrition reporting and include a sensitivity analysis that treats zero-permit counties as a separate structural category.

---

4. **[HIGH]** Contradictory employment effect claims across documents
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The older county-outcome memo claims employment effects are null/unclear with high confidence, while the corrected falsification pass finds negative employment associations in both pre-COVID and post-surge windows.
   File: research/immigration-county-outcome-panel-2026-04-21.md
   Fix: Apply a supersession banner to the older memo and update the index to clarify that the employment-null story is downgraded.

---

5. **[MEDIUM]** QCEW nondisclosures are handled implicitly via numeric coercion instead of explicit masking
   Category: bug | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review flags `build_county_outcome_panel.py` for relying on `pd.to_numeric(ratio, errors="coerce")` to turn QCEW suppression values into `NaN`. The audit log reportedly shows 2 nondisclosures in 2018 and 2 in 2023 (`disclosure_code == "N"`). While this survives if the cells are string garbage, it is fragile because missingness is being inferred indirectly rather than encoded from the disclosure flag before log-change calculations.
   File: build_county_outcome_panel.py
   Fix: Explicitly set `annual_avg_emplvl` and `annual_avg_wkly_wage` to `pd.NA` wherever `disclosure_code == "N"` before any ratio or log-change computation.

---

6. **[MEDIUM]** Cross-outcome transfer of threshold discovery
   Category: architecture | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   Training statistics (beta, t, p) are identical across wage, margin, and employment outcomes in validation tables, indicating that threshold discovery was tuned only for wages and transferred to other outcomes without independent discovery.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv
   Fix: Perform independent threshold searches for each outcome or explicitly label metadata to show these are wage-tuned exploratory results.

---

7. **[MEDIUM]** Pretrend check uses only one clean pre-period difference
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review notes that the fallback pretrend test uses only the clean `2018–2019` QCEW window. A single delta cannot establish whether pre-trends are parallel or structurally different; it only shows one pre-period change. The reviewer points to the reported employment failure (`t = -4.80`, `p = 1.55e-06`) and argues that without `2017–2018`, the result could reflect a one-off 2019 shock rather than a stable negative pretrend.
   File: build_county_outcome_panel.py
   Fix: Extend the QCEW extraction to include 2017 and add a `2017–2018` pretrend window so the analysis can test whether the employment divergence is persistent or anomalous.

---

8. **[MEDIUM]** Underspecified QCEW nondisclosure handling
   Category: bug | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The audit reports 4 nondisclosure rows but zero missing numeric cells, without clarifying if these rows were retained as-is, manually verified, or coerced.
   File: sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json
   Fix: Update the audit JSON to specify the exact policy for handling disclosure_code == 'N' rows (e.g., counts of rows retained vs dropped).

---

9. **[MEDIUM]** Inconsistent county universes across analysis sections
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Descriptive reporting uses 2326 counties while falsification regressions use 2313. This discrepancy weakens rhetorical contrasts between descriptive and causal findings.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json
   Fix: Harmonize the analysis samples or explicitly document the reason for the count divergence in the summary text.

---

10. **[MEDIUM]** Low absolute concentration of threshold location
   Category: performance | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The modal cutoff pair is selected in only 25% of splits, while null-search modal share reaches 16.7%, indicating that while performance may beat the null, the specific threshold location remains diffuse.
   File: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json
   Fix: Formalize threshold diffuseness using metrics like HHI or normalized entropy to prevent overclaiming location stability.

---

11. **[MEDIUM]** Nominal QCEW wage comparisons likely understate real wage penalties in low-capacity counties
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that `annual_avg_wkly_wage` is nominal while `low_permit` proxies housing inelasticity. Because low-capacity counties likely experienced higher local inflation, especially shelter inflation, nominal wage growth can mask a larger real-wage penalty. The reviewer specifically says the reported `-1.49 pp` wage penalty should be interpreted as a lower bound in real terms.
   File: immigration-county-outcome-panel-2026-04-21.md
   Fix: At minimum, add an explicit memo caveat that the nominal wage estimate likely understates the real wage loss in low-permit counties; if feasible, run a robustness check with regional price adjustments.

---

12. **[MEDIUM]** Inconsistent document provenance and timestamps
   Category: style | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The reasoning-evolution document cites revised memos dated 2026-04-21 that contain content from 2026-04-22, creating a weak provenance chain for tracking the sequence of records.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Implement standard file-level metadata for 'created' and 'last materially revised' dates across the research folder.

---

13. **[MEDIUM]** County population filter may bias the domestic-versus-immigrant newcomer ratio
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review says `analyze_internal_vs_immigrant_newcomers.py` drops counties with population below 10,000, while domestic and immigrant migrants sort into very different county types. The reviewer argues that filtering on destination county population changes the denominator mix and can bias the median inflow ratio, making the domestic-to-immigrant comparison less representative.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Run sensitivity analyses with and without the `<10k` population filter, or reweight/stratify by county density and size so the ratio is not driven by destination-composition bias.

---

14. **[MEDIUM]** Permit baseline may not map cleanly to surge-period housing throughput
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review argues that using a `2017–2019` permit baseline as the capacity measure for the `2021–2024` shock assumes stable permit-to-completion conversion. It notes that permits issued in 2019 typically become completions in 2020–2021, but the post-2021 interest-rate environment disrupted that pipeline. As a result, permits may function more as a zoning permissiveness proxy than as an estimate of housing actually added during the surge window.
   File: 
   Fix: Either incorporate completion/starts data or explicitly reframe the variable as a zoning/permissiveness proxy and test sensitivity to alternative capacity measures with shorter lag structures.

---

15. **[MEDIUM]** County outcome regressions may be vulnerable to omitted state-level or remote-work confounding
   Category: logic | Confidence: 0.5 | Source: Gemini (architecture/patterns)
   In the reviewer's self-identified blind spots, they warn that the QCEW/permit interaction (`high_recent_fb × low_permit`) may be confounded if the state-level controls or fixed effects do not adequately absorb post-COVID remote-work and Sunbelt boom dynamics. They specifically mention Texas and Florida as examples where high wages and high permits could be driven by pandemic migration patterns rather than structural housing elasticity.
   File: analyze_county_outcome_panel.py
   Fix: Verify and document the full control set and fixed effects in `analyze_county_outcome_panel.py`, and add robustness checks that better isolate state-specific pandemic booms (for example, stronger fixed effects, region-by-period controls, or leave-one-state-out tests).

---

16. **[LOW]** Persistent [DATA] placeholders in county-outcome memo
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The older county-outcome memo still contains [DATA] placeholders instead of concrete file path citations, violating the 'Source everything' principle.
   File: research/immigration-county-outcome-panel-2026-04-21.md
   Fix: Replace all remaining data placeholders with stable, versioned file paths.

---

17. **[LOW]** Missing instrument-bias caveats in index documentation
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   While caveats are present in detailed memos, the top-level README/index lacks framing notes regarding instrument bias, which may lead to misuse during downstream consumption.
   File: research/immigration-INDEX.md
   Fix: Add a topic-level framing note to the index documentation summarizing known instrument limitations.

---

18. **[LOW]** Native-flight interpretation is tested with net migration instead of gross outflow
   Category: missing | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review recommends testing IRS gross outflow against rent burden rather than relying on net migration. It argues that net migration conflates incumbent exits with deterred arrivals, so it is a poor outcome if the question is whether rent burden or capacity constraints are causing resident flight.
   File: 
   Fix: Add a specification that regresses gross outflow on `high_rent_burden` (or analogous housing-cost measures) and compare it against the existing net-migration results.

---

19. **[LOW]** Capacity ranking ignores persons-per-unit differences in permit counts
   Category: architecture | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review notes that the summary JSON says 'no persons-per-unit housing conversion is used.' It argues that comparing foreign-born counts directly to permit counts can distort capacity rankings because counties differ in the mix of single-family versus multi-family permits, especially in dense urban counties versus exurbs. This can make raw permit-based capacity measures non-comparable across places.
   File: 
   Fix: Normalize permit-based capacity using occupancy assumptions or separate single-family and multi-family permits, then test whether rankings and downstream results are robust to those adjustments.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


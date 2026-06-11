# Review Findings — 2026-04-22

**16 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** IRS 2022-2023 migration is silently used as a proxy for 2021-2022 migration
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review flags `panel["net_us_migration_persons_ty2021_2022_proxy"] = panel["net_us_migration_persons_2022_23"]` in `build_county_outcome_panel.py` as a severe semantic failure. The concern is that 2022-2023 migration occurred under a materially different rate, housing, and return-to-office environment, so equating it to 2021-2022 silently misstates the timing of the migration shock.
   File: build_county_outcome_panel.py
   Fix: Remove the proxy column or replace it with the actual 2021-2022 IRS migration file. If no true file exists, keep the gap explicit rather than encoding a mismatched year as if it were observed.

---

2. **[HIGH]** QCEW annual-average extraction hardcodes COVID contamination into 2020 outcome windows
   Category: bug | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review claims `build_county_outcome_panel.py` filters QCEW records with `chunk["qtr"] == "A"` (annual average). That means 2020 values blend pre-lockdown Q1 with the Q2 collapse and later recovery, so any 2020 log-change window is structurally contaminated by pandemic timing rather than local housing-capacity dynamics. The reviewer argues this is a self-inflicted artifact because the BLS single-file data already contain quarterly rows that could isolate cleaner comparisons.
   File: build_county_outcome_panel.py
   Fix: Extract quarterly QCEW data instead of annual averages, preferably using a consistent quarter such as Q1-to-Q1 (or another explicitly justified quarter) for 2020/2021 comparisons.

---

3. **[HIGH]** Estimand mismatch in threshold-surface null comparison
   Category: bug | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   In build_summary, actual_wage filters for 'wage', but surface_actual and surface_null may compare pooled actual outcomes against wage-only null searches. This makes concentration metrics (modal share, top-3 share) formally invalid for comparison.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Make threshold-surface comparisons outcome-matched (wage actual vs wage null) and export stratified concentration metrics.

---

4. **[MEDIUM]** Semantically broad plural 'pretrends' usage for single window
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The memo refers to 'wage pretrends', but since windows touching 2020 are downgraded as contaminated, the evidence rests on a single window (2018-2019). The plural phrasing risks laundering one clean window into a broader pattern claim.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Downgrade prose from 'wage pretrends' to 'the clean 2018-2019 wage pretrend window'.

---

5. **[MEDIUM]** Wilson CIs over repeated splits are anti-conservative
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The script applies Wilson intervals to counts over 60 splits. Because these splits use the same county sample, they are not IID Bernoulli trials; treating them as such overstates inferential precision.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Relabel as 'heuristic split-stability interval' or replace with bootstrap intervals over counties.

---

6. **[MEDIUM]** BPS year filtering relies on fragile string-prefix date matching
   Category: bug | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review states that `analyze_capacity_falsification.py` uses `str(row["Date"]).startswith(tuple(keep_years))` to retain 2018/2019/2020 rows. This is brittle because varying date formats such as `MM/YYYY`, `YYYYMM`, or parsed timestamps can silently over-select or miss records. The reviewer explicitly calls this a parsing risk that should be audited.
   File: analyze_capacity_falsification.py
   Fix: Parse the `Date` field to a real datetime or year integer and filter with an explicit year test such as `pd.to_datetime(df["Date"]).dt.year.isin([...])`.

---

7. **[MEDIUM]** Pre-surge housing-capacity baseline includes 2020 permits that likely were not available for the 2021 surge
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says the scripts use 2018-2020 permits as the pre-surge capacity measure, but units permitted in 2020 generally require 12-24 months to complete. That makes 2020 permits a poor proxy for housing stock available when the 2021 immigration surge began. The reviewer recommends defining capacity entering the surge with a lagged 2017-2019 permit window instead.
   File: build_county_outcome_panel.py
   Fix: Shift the permit baseline back one year so pre-surge capacity is built from 2017-2019 permits, or otherwise model permit-to-completion lags explicitly.

---

8. **[MEDIUM]** Threshold search is not benchmarked against a continuous capacity model
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review argues that the memo's 'diffuse threshold' result may simply reflect discretizing a continuous relationship. It says `analyze_capacity_falsification.py` searches threshold cutoffs but does not test a continuous or log-linear interaction like `surge_load * capacity_constraint` against the threshold specification, so it cannot tell whether the threshold is an artifact of arbitrary binning.
   File: analyze_capacity_falsification.py
   Fix: Add continuous and/or log-linear benchmark models and compare fit or out-of-sample performance against the threshold model using metrics such as BIC, R², or holdout error.

---

9. **[MEDIUM]** Reasoning-evolution doc claims exceed falsification memo limits
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The evolution doc describes wage-side local effects as 'more credibly surge-amplified', whereas the falsification memo calls the split 'provisional, not settled' and 'unverified pending reruns'. This creates an internal inconsistency where narrative synthesis overstates the primary evidence.
   File: research/immigration-reasoning-evolution-2026-04-21.md
   Fix: Align the evolution doc to the narrower formulation: one clean annual pre-COVID window favors wages over employment, but the contrast is not yet causally secure.

---

10. **[MEDIUM]** Threshold analysis universe restriction is understated
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The analysis excludes counties with zero permits or zero pre-surge baselines, meaning the result applies to a restricted subset, not the full county panel. The current prose understates this universe restriction.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: State the threshold-analysis universe explicitly in the memo headline claims (e.g., eligible_counties / total_counties).

---

11. **[MEDIUM]** Pandemic-period wage analyses do not control for sector-composition bias
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that the pipeline isolates private-sector totals with `own_code == "0"` and `industry_code == "10"`, then interprets wage changes across pandemic windows. It argues this is vulnerable to composition bias because layoffs hit lower-wage service workers disproportionately in 2020, mechanically raising average weekly wages among remaining workers. The reviewer says the falsification does not control for initial service-sector share or similar composition measures.
   File: analyze_capacity_falsification.py
   Fix: Control for pre-period sector composition, such as baseline service-sector employment share, or rerun wage analyses on sector-adjusted outcomes to separate composition effects from true wage pressure.

---

12. **[MEDIUM]** Lack of window-specific sample accounting in builder
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The builder's audit object stores aggregate missing counts based on a single flag rather than window-specific accounting (e.g., 2018-2019 vs 2023-2024), which undermines the 'explicit sample accounting' claim.
   File: sources/immigration-causal/scripts/build_county_outcome_panel.py
   Fix: Add a regression-by-regression sample table documenting eligible N, missing N, and exclusions for every spec.

---

13. **[LOW]** Unsourced scalar constant OCCUPANTS_PER_UNIT
   Category: constitutional | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The constant OCCUPANTS_PER_UNIT = 2.5 is used in capacity conversion but lacks an explicit source reference in the code or comments.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Source or footnote the fixed scalars used in capacity conversion.

---

14. **[LOW]** Qualitative evidence descriptions lack quantification
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Several key claims like 'beats the null strongly' and 'poor transfer' remain qualitative without exact thresholds or statistics in the memo body.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Add exact thresholds or reported statistics for qualitative phrasing in the memo appendix.

---

15. **[LOW]** Missing steel-man for smooth-response threshold interpretation
   Category: constitutional | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The memo lacks an articulation of the opposing view that there may be no stable breakpoint at all, only a smooth response surface.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Add one explicit steel-man paragraph for the null/smooth-response interpretation.

---

16. **[LOW]** Chunked Pandas QCEW extraction is described as unnecessarily slow and memory-heavy
   Category: performance | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review criticizes the current QCEW ingestion approach in `build_county_outcome_panel.py` for using `pd.read_csv(..., chunksize=500_000)` on large ZIP/CSV inputs. It argues this creates avoidable runtime and memory pressure, especially since the project already uses DuckDB elsewhere and could push filtering into `read_csv_auto(...)` instead of Python-level chunk iteration.
   File: build_county_outcome_panel.py
   Fix: Replace chunked Pandas extraction with a DuckDB query that reads the source files directly and filters rows in SQL before materializing a dataframe.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->


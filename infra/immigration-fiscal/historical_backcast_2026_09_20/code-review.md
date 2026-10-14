**Verdict:** One material historical-path inconsistency remains in the reviewed snapshot. The programme production terms silently switch from a GDP path to fixed real dollars per person; this alone moves the ten-year lineage result by $9.351bn low / $6.151bn high. A second issue in the anchored Medicaid SE was corrected in source during review; regenerated outputs still need verification.

## MEDIUM — Programme production terms change their historical rule without identifying that change

- Location: `p7_backcast.py:283–289`.
- Evidence: both production terms multiply their 2024 amount solely by union/G3+ population growth. In the existing source mapping, `backcast.py:358–359` maps `rule == "production"` to GDP, with deflation and the appropriate population-share path applied downstream. Consequently the new programme variant introduces a separate fixed-productivity assumption alongside the programme-series change. Its 2024 closure cannot detect this because both paths equal one at the anchor.
- Quantified read-only probe: take `derived/p7/programme_lines.csv`, variant/rule `programme`, parts `production_private` and `production_receipts`, years 2015–2024; multiply each part by `(GDP_y/GDP_2024) × (price_2024/price_y) × (national_population_2024/national_population_y)` and subtract its current value. GDP and prices came from the pinned Section1 workbook through `backcast.line/series`, population from pinned Section7. Cost changes: low union +$9.188302bn, low lineage +$9.350997bn, high union +$6.044234bn, high lineage +$6.151258bn. Both lineage endpoints exceed the brief's $5bn bar.
- Fix: use real GDP indexed to 2024 times the separate union/G3+ population-share paths for these terms. Alternatively expose fixed real production per person as a separately named, explicitly justified sensitivity and retain GDP for the primary programme comparison.
- Confidence: **high** on the code discrepancy and arithmetic; **medium** on intended scientific specification. An explicit decision to hold real production per person fixed would change the latter assessment, but would still require the assumption to be stated in the programme description. This is the only finding where a project-specific modeling convention could override the default correction.

## Resolved during review — Anchor-year Medicaid uncertainty

- Original location: `p7_backcast.py:339–350`; the reviewed output `derived/p7/programme_medicaid_se.csv` reported nonzero conditional SE for the identically zero 2024 adjustment: $2.273464bn low/union and $2.443297bn low/lineage.
- Cause: 2024 replicate numerators were perturbed while the same 2024 relative-use denominator was declared fixed. Conditioning on that anchor fixes both appearances of the same measurement.
- Parent added `if year == 2024: relative_reps = np.repeat(anchor.relative_use, 161)` at lines 341–342 during this review. That resolves the identified source error. Confirm regenerated 2024 correction and SE are zero and add a regression assertion. No full rerun was performed by this reviewer.
- Confidence: **high**. This concerns the conditional SE of the adjustment, not the separately reported raw survey key's SE.

## Coverage and limits

Reviewed the complete new `p7_backcast.py`, `programme_inputs.cjs`, `historical_use.py`, `acquire_p7.py`, `test_p7_backcast.py`, and `test_historical_use.py`; reviewed the diff in `backcast.py` and `backcast_categories.py`, plus relevant existing source-map, population-path, carried-component, and test code. Traced programme category cells, engine effect/amount semantics, measured pandemic EIP aggregation, and the component accrual/source mapping into their actual local source files. Inspected the emitted programme inputs, uncertainty rows, and production paths.

No additional material defect established in rate averaging, structural-zero handling, source pin checks, engine cost summation, or the available-year school/Medicaid measurement code. The tests' 2024 anchors and aggregate closure do not independently validate historical source choice.

Skipped full test execution and full pipeline regeneration because the parent had already run the deterministic suite and was regenerating outputs concurrently. Skipped external re-acquisition and primary-document reinterpretation: this was a bounded implementation review using the pinned local sources. Unchanged debt consumers and older archived cases were not exhaustively reviewed. No code or git mutations; only this requested review artifact was written.

## Parent resolution — 2026-10-14

The reviewed snapshot above is superseded on both findings. The programme production terms now use the existing real-GDP/population-share path; `test_programme_production_retains_existing_gdp_source_path` checks the emitted paths against independently loaded pinned GDP, prices and ACS counts. Regenerated Medicaid results have exactly zero anchored 2024 change and conditional SE, enforced by `test_programme_medicaid_anchor_and_covariance_receipt`. Final execution and byte-reproduction receipts are in `validation.md`.
